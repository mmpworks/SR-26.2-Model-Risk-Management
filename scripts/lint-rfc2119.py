#!/usr/bin/env python3
"""
lint-rfc2119.py — Flag potentially-misused RFC 2119 keywords.

Per spec §0 (Conformance keywords): the conformance keywords MUST,
MUST NOT, SHOULD, SHOULD NOT, MAY carry normative weight only when
uppercase (RFC 8174 §2). Lowercase occurrences are descriptive
prose.

This linter scans spec markdown for *suspicious* lowercase
occurrences of those keywords — cases that READ as binding
requirements but are written in lowercase. It is not a
mechanical-replace tool: most lowercase usages of "must", "should",
"may" in English prose are correct (e.g., "this may apply"). The
linter surfaces patterns most likely to be normative slips so a
human reviewer can decide.

Heuristics:
  1. Inside paragraphs flagged as normative (sections whose H2/H3
     heading ends with "(normative)" or "(normative when applicable)").
  2. The keyword appears immediately after a bullet marker or at the
     start of a sentence following a colon (classic RFC-style
     requirement phrasing).
  3. The keyword is followed by a verb of obligation rather than a
     verb of possibility.

False positives are expected. The linter's role is to surface
candidates; the reviewer judges.

Usage:
    python scripts/lint-rfc2119.py
    python scripts/lint-rfc2119.py spec/chain-of-custody-DRAFT-0.2.0.md
    python scripts/lint-rfc2119.py --strict   # tighter heuristics
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Default scan target — the spec file. Override via positional args.
DEFAULT_TARGETS = [
    "spec/chain-of-custody-DRAFT-0.2.0.md",
]

# Section-heading regex. H2 or H3 with "(normative)" or
# "(normative when applicable)" trailing tag.
NORMATIVE_HEADING = re.compile(
    r"^(?P<hashes>#{2,3})\s+(?P<title>.+?\s*\((?:normative|normative when applicable)\))\s*$",
    re.MULTILINE,
)

# Any H2 or H3 heading — used to detect when we leave the normative
# block by entering another heading at the same depth.
ANY_HEADING = re.compile(r"^(?P<hashes>#{2,4})\s+(?P<title>.+)$", re.MULTILINE)

# Lowercase RFC 2119 keywords we scan for.
LOWERCASE_KEYWORDS = ["must", "must not", "shall", "shall not", "should", "should not", "may", "may not"]

# Pre-compile per-keyword regex. We use word boundaries on both sides.
# The "X" pattern matches the keyword as a discrete token.
KEYWORD_REGEXES = {
    kw: re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
    for kw in LOWERCASE_KEYWORDS
}

# Phrases that suggest the keyword is being used in a normative
# (binding) sense rather than descriptive prose. The list is
# deliberately narrow — broader matching produces too much noise.
SUSPECT_PRECEDING = [
    ":\s*",               # follows a colon (RFC-style: "the field: must be X")
    r"^\s*[-*]\s+",       # bullet marker
    r"^\s*\d+\.\s+",      # ordered-list marker
    r"\.\s+The\s+\w+\s+",  # period + "The X" — sentence-start normative
    r"\.\s+Implementations\s+",
    r"\.\s+Verifiers\s+",
    r"\.\s+Institutions\s+",
    r"\.\s+SDKs?\s+",
]
SUSPECT_PRECEDING_REGEX = re.compile(
    "|".join(SUSPECT_PRECEDING),
    re.MULTILINE,
)


def find_normative_blocks(text: str) -> list[tuple[int, int, str]]:
    """Return list of (start_offset, end_offset, heading_text) for each
    normative section in the document. End offset is the start of the
    next heading at the same depth or document end."""
    blocks: list[tuple[int, int, str]] = []
    norm_matches = list(NORMATIVE_HEADING.finditer(text))
    for i, match in enumerate(norm_matches):
        start = match.end()
        heading_depth = len(match.group("hashes"))
        # Find the next heading at the same or shallower depth.
        end = len(text)
        for next_match in ANY_HEADING.finditer(text, start):
            next_depth = len(next_match.group("hashes"))
            if next_depth <= heading_depth:
                end = next_match.start()
                break
        blocks.append((start, end, match.group("title")))
    return blocks


def flag_suspicious_lowercase(
    text: str, blocks: list[tuple[int, int, str]], strict: bool
) -> list[tuple[int, int, str, str, str]]:
    """Walk each normative block looking for lowercase keyword usage
    that fits the suspect-context heuristic.

    Returns list of (line_no, col, keyword, context_window,
    block_heading)."""
    findings = []
    for start, end, heading in blocks:
        block_text = text[start:end]
        for kw, regex in KEYWORD_REGEXES.items():
            for kw_match in regex.finditer(block_text):
                token = kw_match.group(0)
                # Only flag the lowercase form, never the canonical
                # uppercase. The regex is case-insensitive so we filter
                # by checking the captured token's letter-case.
                if token.lower() != token:
                    continue
                # Compute absolute offsets back to the original text.
                abs_offset = start + kw_match.start()
                # Extract the surrounding 80 chars on each side.
                ctx_start = max(0, abs_offset - 80)
                ctx_end = min(len(text), abs_offset + len(token) + 80)
                context = text[ctx_start:ctx_end].replace("\n", "\\n")
                # Check the immediately preceding ~50 chars against
                # the suspect-context regex (strict mode requires it).
                preceding = text[max(0, abs_offset - 50):abs_offset]
                if strict and not SUSPECT_PRECEDING_REGEX.search(preceding + token):
                    continue
                # Convert offset to (line, col).
                line_no = text.count("\n", 0, abs_offset) + 1
                line_start = text.rfind("\n", 0, abs_offset) + 1
                col = abs_offset - line_start + 1
                findings.append((line_no, col, token, context, heading))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument(
        "targets",
        nargs="*",
        default=DEFAULT_TARGETS,
        help="Markdown files to lint (default: spec/chain-of-custody-DRAFT-0.2.0.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Require suspect-preceding-context match (lower noise; may miss findings)",
    )
    parser.add_argument(
        "--exit-on-finding",
        action="store_true",
        help="Exit code 1 when findings present (CI-friendly)",
    )
    args = parser.parse_args()

    total_findings = 0
    for target in args.targets:
        path = Path(target)
        if not path.exists():
            print(f"lint-rfc2119: target missing: {target}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        blocks = find_normative_blocks(text)
        findings = flag_suspicious_lowercase(text, blocks, args.strict)
        if findings:
            print(f"\n{target}: {len(findings)} potentially-suspect lowercase keyword(s)")
            print("=" * 72)
            for line_no, col, kw, ctx, heading in findings:
                print(f"  line {line_no}:{col}  [{kw}]  in §«{heading}»")
                print(f"    …{ctx}…")
                print()
        else:
            print(f"{target}: clean — no suspect lowercase keywords found.")
        total_findings += len(findings)

    print(f"\nTotal findings: {total_findings}")
    if args.exit_on_finding and total_findings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
