# -*- coding: utf-8 -*-
"""Compute the §7 unknown-wire-format-kind fallthrough verifier-output byte
form for FFIEC v1 test-vector case 049-unknown-wire-format-kind-fallthrough.

Spec §7 (PRD-3 normative; rolled forward from PRD-4 per the PRD-3 index)
normates verifier behavior when a v1 chain contains a top-level wire-format
kind the verifier was not built to walk. The rule:

  1. The verifier MUST NOT silently treat the unknown record as a chain
     entry; chain-walk steps 4-9 MUST NOT execute against it.
  2. The verifier MUST NOT FAIL the entire run on the unknown kind alone.
  3. The verifier MUST emit an anomaly line under `Status: PASS` of the
     form `unknown wire-format kind present: <kind_string> (count: N)`.
  4. The verifier MUST surface the anomaly in `additional_verifications`
     as `additional_verifications: ['unknown_kind_present']` so downstream
     tooling can dispatch on the marker programmatically.
  5. Institutions requiring stricter posture treat the marker as a non-
     PASS condition out-of-band per §7 step 5.
  6. The verifier MUST recompute the per-day Merkle root and the §11
     signature verification against the day's full leaf sequence
     including the unknown-kind records.

This case pins the JCS-canonical (RFC 8785) bytes of the structured
verifier output when a PRD-3 verifier ingests a chain containing a
§10.62 `cross_domain_transition` record (a v1 wire-format kind PRD-3
verifiers are built before). The output is the §10.12 verdict object
plus the §7 anomaly-line list, composed into a single structured-output
record so a clean-room implementation produces byte-identical bytes.

The verifier under test is a PRD-3 verifier (`v1.0c-verifier-2026-05-15`,
`verifier_spec_version_supported = "v1.0c"`) reading a chain whose
seal-day post-dates the PRD-4 amendment that introduced
`cross_domain_transition`. Per §7's PRD-3-to-PRD-4 forward-compat clause,
the verifier emits PASS plus the `unknown_kind_present` marker.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Pinned inputs — the chain under test contains ONE §10.62
# cross_domain_transition record. The verifier walks the rest of the chain
# normally; the §10.62 record triggers the fallthrough.
# ---------------------------------------------------------------------------

UNKNOWN_KIND_STRING = "cross_domain_transition"
UNKNOWN_KIND_COUNT = 1


# Pinned placeholder values for the verdict object (matching the §7
# byte-form examples and case 036's full-shape placeholders so this
# vector composes cleanly with case 036).
PLACEHOLDER_POSTURE = "ffiec"
PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
PLACEHOLDER_SPEC_VERSION = "v1.0c"
PLACEHOLDER_VERIFIER_VERSION = "v1.0c-verifier-2026-05-15"


# The structured verifier output combines (a) the §10.12 verdict object
# the verifier emits on its Verdict-Object trailing line and (b) the §7
# anomaly-line list emitted under Status: PASS. The structured record
# below pins both so a clean-room implementation can compare both
# surfaces byte-for-byte.


def build_verdict() -> dict:
    """§10.12 verdict object the verifier emits on the unknown-kind
    fallthrough path. PASS (exit_code 0) with the `unknown_kind_present`
    marker in `additional_verifications`.
    """
    return {
        "additional_verifications": ["unknown_kind_present"],
        "exit_code": 0,
        "posture": PLACEHOLDER_POSTURE,
        "trust_anchor_manifest_sha256": PLACEHOLDER_TRUST_ANCHOR_SHA256,
        "verifier_spec_version_supported": PLACEHOLDER_SPEC_VERSION,
        "verifier_version": PLACEHOLDER_VERIFIER_VERSION,
    }


def build_anomaly_line(kind_string: str, count: int) -> str:
    """§7 step 3 anomaly line — fixed byte form per spec text:
       `unknown wire-format kind present: <kind_string> (count: N)`
    """
    return f"unknown wire-format kind present: {kind_string} (count: {count})"


def build_structured_output() -> dict:
    """The structured verifier output combining verdict + anomaly lines.

    Pins both the §10.12 verdict-object bytes (emitted on the
    Verdict-Object trailing line) AND the §7 anomaly line(s) emitted
    under Status: PASS, so a clean-room implementation can compare both
    surfaces. The `status` field carries the PASS label per §7 step 3.
    """
    return {
        "anomaly_lines": [build_anomaly_line(UNKNOWN_KIND_STRING, UNKNOWN_KIND_COUNT)],
        "status": "PASS",
        "verdict": build_verdict(),
    }


def canonicalize_and_hash(obj: dict) -> tuple[bytes, str]:
    canonical_bytes = jcs.canonicalize(obj)
    return canonical_bytes, hashlib.sha256(canonical_bytes).hexdigest()


def main() -> None:
    structured_output = build_structured_output()
    structured_bytes, structured_sha256 = canonicalize_and_hash(structured_output)

    # Also pin the verdict object in isolation — composes cleanly with
    # case 036's verdict-object byte-form pins.
    verdict = build_verdict()
    verdict_bytes, verdict_sha256 = canonicalize_and_hash(verdict)

    input_record = {
        "_about": (
            "Input fixture for case 049-unknown-wire-format-kind-fallthrough. "
            "Pins the structured verifier output when a PRD-3 verifier "
            "(v1.0c-verifier-2026-05-15) ingests a chain containing a "
            "§10.62 cross_domain_transition record — a v1 wire-format kind "
            "the verifier was built before. Per §7 fallthrough rule: "
            "PASS with anomaly line `unknown wire-format kind present: "
            "cross_domain_transition (count: 1)` plus "
            "`additional_verifications: ['unknown_kind_present']`. Exit "
            "code 0 per §10.12 additional-verifications discipline."
        ),
        "unknown_kind_string": UNKNOWN_KIND_STRING,
        "unknown_kind_count": UNKNOWN_KIND_COUNT,
        "structured_output": structured_output,
        "structured_canonical_byte_length": len(structured_bytes),
        "structured_canonical_sha256": structured_sha256,
        "structured_canonical_bytes_utf8": structured_bytes.decode("utf-8"),
        "verdict_only_canonical_byte_length": len(verdict_bytes),
        "verdict_only_canonical_sha256": verdict_sha256,
        "verdict_only_canonical_bytes_utf8": verdict_bytes.decode("utf-8"),
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # expected_canonical.txt carries the structured-output bytes (the
    # primary byte-form pin). The verdict-only bytes are captured in
    # input.json and in expected_canonical_sha256.txt below for
    # composition with case 036.
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(structured_bytes)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"structured_output {structured_sha256}\n")
        f.write(f"verdict_only      {verdict_sha256}\n")

    print(f"[049] unknown kind:               {UNKNOWN_KIND_STRING}")
    print(f"[049] unknown kind count:         {UNKNOWN_KIND_COUNT}")
    print(f"[049] structured canonical len:   {len(structured_bytes)}")
    print(f"[049] structured canonical SHA-256: {structured_sha256}")
    print(f"[049] verdict-only canonical len: {len(verdict_bytes)}")
    print(f"[049] verdict-only SHA-256:       {verdict_sha256}")


if __name__ == "__main__":
    main()
