# -*- coding: utf-8 -*-
"""Compute the §10.54 decadal re-seal record byte form for FFIEC v1
test-vector case 047-decadal-resealing.

§10.54 normates the decadal re-sealing discipline as an annotated v1.0b
seal record — same shape as §10.42 backfill seal. Discriminating
attributes route the verifier to the §10.54 verification path:
- seal.resealed_at_decadal_boundary = true
- window timestamps
- baseline-manifest SHA-256 (over prior generation's seal records)
- resealed_under_algorithm
- resealed_generation_index
- resealed_previous_generation_anchor_sha256

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Helvetian-shape decadal re-seal at the 2036-12-31 decadal boundary
# (10 years after the 2026-12-31 cycle close). Generation index 1 (the
# first decadal re-seal; generation 0 is the original seal).
RESEALED_WINDOW_START_UTC = "2026-12-31T23:59:59Z"
RESEALED_WINDOW_END_UTC = "2036-12-31T23:59:59Z"
RESEALED_UNDER_ALGORITHM = "dilithium3"
RESEALED_GENERATION_INDEX = 1

# SHA-256 of the canonicalized baseline manifest (prior generation's
# seal records' content hashes, JCS-canonical sorted array).
RESEALED_BASELINE_MANIFEST_SHA256 = _sha256_of_label(
    "helvetian-tax-archive-generation-0-baseline-manifest-2026-2036"
)

# SHA-256 of the prior generation's terminal seal record (the last
# seal of the 2026-2036 generation, signed under Ed25519).
RESEALED_PREVIOUS_GENERATION_ANCHOR_SHA256 = _sha256_of_label(
    "helvetian-tax-archive-generation-0-terminal-seal-2036-12-31"
)


def build_metadata_leaf() -> dict:
    """§10.54 metadata-leaf attributes — 6 fields per §10.42 precedent."""
    return {
        "seal.resealed_at_decadal_boundary": True,
        "seal.resealed_baseline_manifest_sha256": RESEALED_BASELINE_MANIFEST_SHA256,
        "seal.resealed_generation_index": RESEALED_GENERATION_INDEX,
        "seal.resealed_previous_generation_anchor_sha256": RESEALED_PREVIOUS_GENERATION_ANCHOR_SHA256,
        "seal.resealed_under_algorithm": RESEALED_UNDER_ALGORITHM,
        "seal.resealed_window_end_utc": RESEALED_WINDOW_END_UTC,
        "seal.resealed_window_start_utc": RESEALED_WINDOW_START_UTC,
    }


def main() -> None:
    leaf = build_metadata_leaf()
    canonical = jcs.canonicalize(leaf)
    sha256 = hashlib.sha256(canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 047-decadal-resealing — pins the "
            "§10.54 metadata-leaf byte form for a Helvetian-shape "
            "first-decadal re-seal at the 2036-12-31 boundary under "
            "Dilithium3 (generation 1). Mirrors §10.42 backfill-seal's "
            "annotated-seal pattern. The full seal record (the v1.0b "
            "sign_payload + signatures list) is built around this "
            "metadata leaf via the Merkle composition and signing path; "
            "case 047 pins the metadata-leaf canonical bytes only."
        ),
        "metadata_leaf": leaf,
        "expected": {
            "canonical_byte_length": len(canonical),
            "canonical_sha256": sha256,
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(canonical)
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w", encoding="utf-8", newline="\n",
    ) as f:
        f.write(sha256 + "\n")

    print(f"[047] resealed_under_algorithm:  {RESEALED_UNDER_ALGORITHM}")
    print(f"[047] generation_index:          {RESEALED_GENERATION_INDEX}")
    print(f"[047] baseline_manifest_sha256:  {RESEALED_BASELINE_MANIFEST_SHA256}")
    print(f"[047] previous_anchor_sha256:    {RESEALED_PREVIOUS_GENERATION_ANCHOR_SHA256}")
    print(f"[047] canonical len:             {len(canonical)}")
    print(f"[047] canonical SHA-256:         {sha256}")


if __name__ == "__main__":
    main()
