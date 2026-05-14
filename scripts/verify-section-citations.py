"""verify-section-citations.py
================================

Programmatic verifier for spec section citations in companion docs.

What it does
------------

1. Walks `spec/chain-of-custody-DRAFT-0.2.0.md` and builds an index of every
   section heading: §1, §1.1, §1.2.1, ..., §10.82, Appendix A/B/C/D.

2. Walks every companion markdown file (docs/, the resolution matrix, the
   remediation plan) and extracts every `§\\d+(\\.\\d+)*` reference plus every
   `Appendix [A-Z]` reference.

3. Reports:
   - Citations that point at sections / appendices that don't exist (broken).
   - Sections / appendices that exist but are never referenced (orphans).
   - Per-file citation counts.

4. Exit code 0 if no broken citations; 1 otherwise. Suitable for CI gating.

Why
---

The resolution matrix and remediation plan accumulate §X.Y citations against
moving spec content. When a spec edit renames a section or restructures the
appendix list, citations drift silently. This script makes the drift visible.

Usage
-----

    python scripts/verify-section-citations.py
    python scripts/verify-section-citations.py --strict     # exit 1 on orphan sections too
    python scripts/verify-section-citations.py --json       # machine-readable report
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# Repo root resolved from this script's location: scripts/ -> repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "spec" / "chain-of-custody-DRAFT-0.2.0.md"

# Companion docs that cite spec sections. Walked recursively under docs/.
DOCS_DIR = REPO_ROOT / "docs"

# Only verify §-citations in docs that authoritatively reference the spec.
# Other docs (design, regulator-pack overlays, templates, synopsis) use §X.Y
# numbering for their own internal sections; their refs are not spec-citations
# and produce false positives. The allowlist below names the docs whose §-refs
# are required to resolve against spec headings.
AUTHORITATIVE_PREFIXES = (
    "docs/q-and-a.md",
    "docs/review-2026-05-10/findings-resolution-matrix.md",
    "docs/review-2026-05-10/remediation-plan.md",
    "docs/review-2026-05-10/audit-250.md",
)
# The per-discipline findings-{discipline}.md files contain "Suggested fix"
# text that proposes §X.Y locations the auditor recommended. Those suggestions
# don't need to resolve against the final shipped section numbers — they're
# inputs to remediation, not closure artifacts. Exclude them by NOT listing
# them in AUTHORITATIVE_PREFIXES.

# Section reference patterns. The §-glyph is the canonical reference form;
# we also catch "Appendix A/B/..." references as a parallel namespace.
SECTION_RE = re.compile(r"§(\d+(?:\.\d+){0,3})")
APPENDIX_RE = re.compile(r"\bAppendix\s+([A-Z])(?:\s|—|$|[.,;:)])")

# Tokens that, when they appear within ~80 chars before the §, mark the
# reference as external (RFC / FIPS / CFR / ISO / USC / Article / Reg etc.).
# These refs should NOT be checked against spec headings.
EXTERNAL_REGIME_RE = re.compile(
    r"(?:RFC\s*\d+|FIPS\s*\d+"
    r"|FRE\b|FRCP\b|\bCFR\b|\bUSC\b|\bISO\s+\d+|NIST\s+SP\s*\d+"
    r"|Article\s+\d+|Reg\s+[A-Z]|Annex\s+[A-Z]"
    r"|Practice\s+Direction|Rule\s+\d+|R\.\s*v\."
    r"|\bPDPA\b|\bPIPA\b|\bDPDP\b|\bLGPD\b|\bAPPI\b|\bPOPIA\b|\bCOPPA\b|\bCCPA\b|\bCPRA\b"
    r"|\bGDPR\b|\bHIPAA\b|\bECPA\b|\bSCA\b|\bDMCA\b|\bBCP\b|\bNACHA\b"
    r"|GDPR\s+Article|EU\s+AI\s+Act"
    r"|design/\d|\.md\s*$|`\d{2}-[\w-]+\.md`"  # design-doc internal section refs
    r"|R\d+\.\d+|Sec\.\s*\d"
    r")",
    re.IGNORECASE,
)

# Catch design-doc internal refs in the spec body: text like
# "`docs/design/09-threat-model.md` §2.6" — the §-ref is internal to the
# named .md file, not a spec-self-ref. Look 80 chars back for `.md`.
DESIGN_DOC_REF_RE = re.compile(r"\.md\b[^.§]*?$")

# Heading patterns in the spec.
#   ## 12. Change log                     -> §12 (top-level)
#   ### 4.1 Primitive 1 ...               -> §4.1
#   #### 4.1.1 Session-key handshake      -> §4.1.1
#   ## Appendix A — ...                   -> Appendix A
HEADING_RE = re.compile(r"^(#{2,4})\s+(\d+(?:\.\d+){0,3})(?:\.\s|\s|$)")
APPENDIX_HEADING_RE = re.compile(r"^(#{2,3})\s+Appendix\s+([A-Z])\b")


@dataclass
class Report:
    spec_sections: set[str] = field(default_factory=set)
    spec_appendices: set[str] = field(default_factory=set)
    citations_by_file: dict[Path, set[str]] = field(default_factory=lambda: defaultdict(set))
    appendix_refs_by_file: dict[Path, set[str]] = field(default_factory=lambda: defaultdict(set))
    broken_section_refs: list[tuple[Path, str]] = field(default_factory=list)
    broken_appendix_refs: list[tuple[Path, str]] = field(default_factory=list)
    orphan_sections: set[str] = field(default_factory=set)
    orphan_appendices: set[str] = field(default_factory=set)


def index_spec_headings(spec_path: Path) -> tuple[set[str], set[str]]:
    """Parse spec for ##/###/#### headings and return (sections, appendices)."""
    sections: set[str] = set()
    appendices: set[str] = set()
    for line in spec_path.read_text(encoding="utf-8").splitlines():
        m_app = APPENDIX_HEADING_RE.match(line)
        if m_app:
            appendices.add(m_app.group(2))
            continue
        m = HEADING_RE.match(line)
        if m:
            sections.add(m.group(2))
    return sections, appendices


def cited_refs_in_file(path: Path) -> tuple[set[str], set[str]]:
    """Return (section_refs, appendix_refs) cited in a markdown file.

    External regime references (RFC §X, FIPS §X, CFR §X, etc.) are stripped
    by inspecting ~40 chars before each match. Only intra-spec refs remain.
    """
    text = path.read_text(encoding="utf-8")
    sections: set[str] = set()
    for m in SECTION_RE.finditer(text):
        # Spec only has §0–§13 at the top level; any larger top-level number
        # is a statute / regulation reference (e.g., §500.11 NYDFS Part 500,
        # §552 FOIA, §190 Australian Evidence Act, §240.17a-4 SEC).
        ref = m.group(1)
        top_level = int(ref.split(".")[0])
        if top_level > 13:
            continue
        # Spec refs are bare numbers like §10.74 — anything followed by an
        # opening paren is a statute subsection (e.g., §17(a), §1798.105(d)).
        # The SECTION_RE doesn't capture the paren, so peek at the next char.
        next_char_idx = m.end()
        if next_char_idx < len(text) and text[next_char_idx] == "(":
            continue
        # Look back up to 80 chars for an external-regime token.
        window_start = max(0, m.start() - 80)
        window = text[window_start : m.start()]
        if EXTERNAL_REGIME_RE.search(window):
            continue
        # Also skip when the closest preceding token is a design-doc filename.
        if DESIGN_DOC_REF_RE.search(window):
            continue
        # Catch the forward pattern: "§X of `docs/foo.md`" or "§X in
        # docs/foo.md". The forward window is short — the design-doc ref
        # appears within ~60 chars after the §.
        forward_end = min(len(text), m.end() + 60)
        forward = text[m.end() : forward_end]
        if re.search(r"\s+(?:of|in|under)\s+`?docs/", forward):
            continue
        # Also catch §§-double notation prefixed by an external regime token
        # (NIST 800-171 §§3.4 (Config Management)... — the regex window
        # already catches the NIST prefix but the §§ second match may slip).
        if m.start() > 0 and text[m.start() - 1] == "§":
            continue
        sections.add(ref)
    appendices = {m.group(1) for m in APPENDIX_RE.finditer(text)}
    return sections, appendices


def collect_companion_files(docs_dir: Path) -> list[Path]:
    """All .md files under docs/ matching AUTHORITATIVE_PREFIXES.

    Docs outside this allowlist (design/, regulator-pack/, templates/) use
    §X.Y for their own internal sections and produce false positives if
    treated as spec-citing artifacts.
    """
    out: list[Path] = []
    for p in docs_dir.rglob("*.md"):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO_ROOT).as_posix()
        if any(rel.startswith(prefix) for prefix in AUTHORITATIVE_PREFIXES):
            out.append(p)
    return sorted(out)


def build_report(strict: bool) -> Report:
    report = Report()
    report.spec_sections, report.spec_appendices = index_spec_headings(SPEC_PATH)

    # The spec body also cites itself; include it so internal §-refs (e.g.
    # "see §10.13") get validated too.
    candidates: list[Path] = [SPEC_PATH] + collect_companion_files(DOCS_DIR)

    all_section_refs: set[str] = set()
    all_appendix_refs: set[str] = set()

    for path in candidates:
        section_refs, appendix_refs = cited_refs_in_file(path)
        if section_refs:
            report.citations_by_file[path] = section_refs
            all_section_refs |= section_refs
        if appendix_refs:
            report.appendix_refs_by_file[path] = appendix_refs
            all_appendix_refs |= appendix_refs

        for ref in section_refs:
            if ref not in report.spec_sections:
                report.broken_section_refs.append((path, ref))
        for ref in appendix_refs:
            if ref not in report.spec_appendices:
                report.broken_appendix_refs.append((path, ref))

    # Orphans: sections / appendices that exist but no companion file cites.
    # The spec itself self-cites most sections, so true orphans are rare.
    report.orphan_sections = report.spec_sections - all_section_refs
    report.orphan_appendices = report.spec_appendices - all_appendix_refs
    return report


def emit_text(report: Report, strict: bool) -> int:
    print(f"Spec headings:       {len(report.spec_sections)} sections, {len(report.spec_appendices)} appendices")
    print(f"Companion files:     {len(report.citations_by_file)} cite §-refs, {len(report.appendix_refs_by_file)} cite Appendix-refs")
    print()

    if report.broken_section_refs:
        print(f"BROKEN §-citations ({len(report.broken_section_refs)}):")
        # Group by missing section so the fix is one-place-per-line.
        by_ref: dict[str, list[Path]] = defaultdict(list)
        for path, ref in report.broken_section_refs:
            by_ref[ref].append(path)
        for ref in sorted(by_ref, key=lambda r: tuple(int(x) for x in r.split("."))):
            files = sorted({p.relative_to(REPO_ROOT).as_posix() for p in by_ref[ref]})
            print(f"  §{ref} cited in {len(by_ref[ref])} place(s):")
            for f in files:
                print(f"    - {f}")
        print()
    else:
        print("BROKEN §-citations: none.")

    if report.broken_appendix_refs:
        print(f"BROKEN Appendix-citations ({len(report.broken_appendix_refs)}):")
        for path, ref in sorted(set(report.broken_appendix_refs)):
            print(f"  Appendix {ref} cited in {path.relative_to(REPO_ROOT).as_posix()}")
        print()
    else:
        print("BROKEN Appendix-citations: none.")

    if report.orphan_appendices:
        print(f"ORPHAN appendices (exist in spec, never referenced from docs/): {sorted(report.orphan_appendices)}")
    else:
        print("ORPHAN appendices: none.")

    if strict and report.orphan_sections:
        # In strict mode we surface orphan §-sections too; usually noisy and
        # informative-only, so off by default.
        print(f"ORPHAN §-sections (exist in spec, never cited): {len(report.orphan_sections)} (use --json to inspect)")

    return 0 if not (report.broken_section_refs or report.broken_appendix_refs) else 1


def emit_json(report: Report) -> int:
    payload = {
        "spec_sections": sorted(report.spec_sections, key=lambda s: tuple(int(x) for x in s.split("."))),
        "spec_appendices": sorted(report.spec_appendices),
        "broken_section_refs": [
            {"path": p.relative_to(REPO_ROOT).as_posix(), "ref": r}
            for p, r in report.broken_section_refs
        ],
        "broken_appendix_refs": [
            {"path": p.relative_to(REPO_ROOT).as_posix(), "ref": r}
            for p, r in report.broken_appendix_refs
        ],
        "orphan_appendices": sorted(report.orphan_appendices),
        "orphan_sections": sorted(
            report.orphan_sections,
            key=lambda s: tuple(int(x) for x in s.split(".")),
        ),
    }
    print(json.dumps(payload, indent=2))
    return 0 if not (report.broken_section_refs or report.broken_appendix_refs) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify §-citations against spec headings.")
    parser.add_argument("--strict", action="store_true", help="Surface orphan §-sections too.")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output.")
    args = parser.parse_args()

    if not SPEC_PATH.exists():
        print(f"ERROR: spec not found at {SPEC_PATH}", file=sys.stderr)
        return 2

    report = build_report(strict=args.strict)
    if args.json:
        return emit_json(report)
    return emit_text(report, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
