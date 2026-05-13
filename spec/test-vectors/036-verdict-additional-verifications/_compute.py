# -*- coding: utf-8 -*-
"""Compute the verdict-object JCS-canonical bytes for FFIEC v1
test-vector case 036-verdict-additional-verifications.

Spec §10.12 amendment + design `07-verifier-design.md` §11 normate the
verdict object's `additional_verifications` array as the place bonus
verifications report (§10.42 backfill-seal-verified today; the §10.12
enumeration may grow as future spec sections normate additional bonus
verifications). Exit codes 0-6 remain the closed §10.12 + §10.29
enumeration; bonus verifications travel via the array, NOT via new
exit codes.

This case pins the JCS-canonical bytes for three verdict sub-cases:

  036a — PASS with empty `additional_verifications`
  036b — PASS with `["backfill_seal_verified"]`
  036c — PASS with two values (forward-compat composition test with a
         placeholder second string)

A clean-room implementation proves it constructs the verdict object
identically across the three shapes.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Pinned closed enumeration of §10.12-amendment additional-verification
# names. Spec sections normating new bonus verifications add to this list
# additively. Today the §10.12 closed enumeration contains the single
# string below per §10.42.
KNOWN_ADDITIONAL_VERIFICATIONS = (
    "backfill_seal_verified",
    # Future spec sections normating new bonus verifications add to this
    # tuple additively. Case 036c uses a placeholder second string to
    # demonstrate the two-entry array byte form without depending on any
    # specific future spec entry.
)


# Forward-compat placeholder string used in case 036c to demonstrate
# the array's composition behavior. NOT in the §10.12 closed
# enumeration; used here only to pin a byte-correct two-entry array.
_FORWARD_COMPAT_PLACEHOLDER = "hybrid_pqc_dual_signature_verified"


def build_verdict(
    *,
    exit_code: int,
    additional_verifications: tuple[str, ...],
) -> dict:
    """Build the verdict object — two fields, byte-locked schema."""
    return {
        "additional_verifications": list(additional_verifications),
        "exit_code": exit_code,
    }


def canonicalize_and_hash(verdict: dict) -> tuple[bytes, str]:
    canonical_bytes = jcs.canonicalize(verdict)
    return canonical_bytes, hashlib.sha256(canonical_bytes).hexdigest()


SUBCASES = (
    {
        "label": "036a",
        "description": "PASS with no bonus verifications (the steady-state shape)",
        "verdict": build_verdict(exit_code=0, additional_verifications=()),
    },
    {
        "label": "036b",
        "description": "PASS with a §10.42 backfill-seal bonus verification",
        "verdict": build_verdict(
            exit_code=0,
            additional_verifications=("backfill_seal_verified",),
        ),
    },
    {
        "label": "036c",
        "description": (
            "PASS with two bonus verifications (forward-compat composition "
            "test — the second string is a placeholder demonstrating the "
            "two-entry array byte form)"
        ),
        "verdict": build_verdict(
            exit_code=0,
            additional_verifications=(
                "backfill_seal_verified",
                _FORWARD_COMPAT_PLACEHOLDER,
            ),
        ),
    },
)


def main() -> None:
    results = []
    for sub in SUBCASES:
        canonical_bytes, sha256 = canonicalize_and_hash(sub["verdict"])
        results.append({
            "label": sub["label"],
            "description": sub["description"],
            "verdict": sub["verdict"],
            "canonical_byte_length": len(canonical_bytes),
            "canonical_sha256": sha256,
            "canonical_bytes_utf8": canonical_bytes.decode("utf-8"),
        })

    input_record = {
        "_about": (
            "Input fixture for case 036-verdict-additional-verifications "
            "— pins the verdict-object JCS-canonical bytes for three "
            "sub-cases. The conformance contract is that all three "
            "sub-cases produce byte-identical output across "
            "implementations."
        ),
        "known_additional_verifications": list(KNOWN_ADDITIONAL_VERIFICATIONS),
        "subcases": results,
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # The expected_canonical.txt holds the THREE sub-case canonical byte
    # forms separated by a single LF — a reader can split on LF to recover
    # each sub-case. The expected_canonical_sha256.txt holds the three
    # sub-case hex digests separated by LF.
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        for i, r in enumerate(results):
            if i > 0:
                f.write(b"\n")
            f.write(r["canonical_bytes_utf8"].encode("utf-8"))
        f.write(b"\n")

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for r in results:
            f.write(f"{r['label']} {r['canonical_sha256']}\n")

    for r in results:
        print(
            f"[036] {r['label']}: len={r['canonical_byte_length']:3d}  "
            f"sha256={r['canonical_sha256']}"
        )


if __name__ == "__main__":
    main()
