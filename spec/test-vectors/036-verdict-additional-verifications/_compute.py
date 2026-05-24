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

This case pins the JCS-canonical bytes for seven verdict sub-cases.
The first three (036a/b/c) pin the structural 2-field subset shape
(`additional_verifications` + `exit_code` only). The next four
(036d/e/f/g) pin the FULL §7-normative shape per spec lines 1574-1586:
six required fields plus the optional v1.0c `operational_events_log_root`.

  036a — 2-field subset, PASS with empty `additional_verifications`
  036b — 2-field subset, PASS with `["backfill_seal_verified"]`
  036c — 2-field subset, PASS with two values (forward-compat
         composition with a placeholder second string)
  036d — FULL 6-field shape, v1.0b PASS, no bonus verifications
         (matches spec §7 byte-form example 1)
  036e — FULL 6-field shape, v1.0b PASS, one bonus verification
         (matches spec §7 byte-form example 2)
  036f — FULL 6-field shape, v1.0b PASS, two bonus verifications
         under §10.69 class disclosure
         (matches spec §7 byte-form example 3)
  036g — FULL 7-field shape, v1.0c PASS with sibling-log binding
         (matches spec §7 byte-form example 4)

Sub-cases d/e/f/g use the SAME placeholder values for the four
shared fields (`posture`, `trust_anchor_manifest_sha256`,
`verifier_spec_version_supported`, `verifier_version`) the spec text
uses in its byte-form examples, so a clean-room implementer comparing
against the spec text gets identical bytes.

A clean-room implementation that produces the seven sub-case canonical
byte forms identically proves it constructs the verdict object
correctly across the full §7 shape, the v1.0c optional-field rule,
and the JCS lexicographic key-ordering discipline.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Pinned closed enumeration of §10.12 `additional_verifications` markers.
# Source of truth: spec §10.12 "Closed `additional_verifications`
# enumeration (normative)" table. The tuple below mirrors the spec table
# entry for entry; new spec sections that normate additional bonus
# verifications extend BOTH the spec table AND this tuple atomically.
#
# Sub-case 036c carries a forward-compat placeholder string that is NOT
# in this enumeration; it appears in the array to pin the two-entry
# byte form without depending on any specific second enumeration entry.
#
# Sub-case 036g uses `sibling_log_root_verified`. The §10.12 table
# extension landing in this same PR adds the marker to the table; the
# spec text at §7 line 1609 already references it in a byte-form
# example. The table extension reconciles the two locations.
KNOWN_ADDITIONAL_VERIFICATIONS = (
    "backfill_seal_verified",
    "sample_based_attestation_via_lot_verified",
    "parallel_evaluator_anchor_verified",
    "cross_anchor_unbound",
    "unknown_kind_present",
    "customer_disclosure_subtree_verified",
    "customer_disclosure_key_derivation_verified",
    "class_disclosure_subtree_verified",
    "cohort_coverage_attestation_verified",
    "foia_release_subtree_verified",
    "foia_release_key_derivation_verified",
    "privileged_investigation_full_content_returned",
    "privileged_investigation_redacted_with_existence_attestation",
    "cross_institution_chain_verified",
    "device_revoked_seen_at_seq_N",
    "cross_vendor_handover_verified",
    "partial_coverage_pattern_2_verified",
    "customer_disclosure_cross_tenant_inheritance_verified",
    "attestation_chain_validated",
    "sibling_log_root_verified",
)


# Forward-compat placeholder string used in case 036c to demonstrate
# the array's composition behavior. NOT in the §10.12 closed
# enumeration; used here only to pin a byte-correct two-entry array.
_FORWARD_COMPAT_PLACEHOLDER = "hybrid_pqc_dual_signature_verified"


def build_verdict_subset(
    *,
    exit_code: int,
    additional_verifications: tuple[str, ...],
) -> dict:
    """Build the 2-field structural-subset verdict object (sub-cases a/b/c).

    Sub-cases 036a/b/c pin the array-shape behavior in isolation. The
    full 6-field shape lives in sub-cases 036d/e/f/g via
    `build_verdict_full`.
    """
    return {
        "additional_verifications": list(additional_verifications),
        "exit_code": exit_code,
    }


# Pinned placeholder values for the four shared fields across sub-cases
# d/e/f/g. The values match the byte-form examples in spec §7 lines
# 1591, 1597, 1603, 1609 verbatim — a clean-room implementer who
# compares against the spec text gets byte-identical output.
_PLACEHOLDER_POSTURE = "ffiec"
_PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
_PLACEHOLDER_SPEC_V1_0B = "v1.0b"
_PLACEHOLDER_SPEC_V1_0C = "v1.0c"
_PLACEHOLDER_VERIFIER_VERSION_V1_0B = "v1.0b-verifier-2026-05-15"
_PLACEHOLDER_VERIFIER_VERSION_V1_0C = "v1.0c-verifier-2026-05-15"
_PLACEHOLDER_OPERATIONAL_LOG_ROOT = (
    "3e9f7c2a8b1d5e6c4a2f9e1d8c7b5a3f1e8d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)


def build_verdict_full(
    *,
    exit_code: int,
    additional_verifications: tuple[str, ...],
    posture: str,
    trust_anchor_manifest_sha256: str,
    verifier_spec_version_supported: str,
    verifier_version: str,
    operational_events_log_root: str | None = None,
) -> dict:
    """Build the full §7-normative verdict object (sub-cases d/e/f/g).

    Six required fields per spec §7 lines 1576-1583 plus the OPTIONAL
    `operational_events_log_root` field that PRESENTs only under v1.0c
    seals (per spec line 1584's "ABSENT (JCS omits) when the seal uses
    v1.0a / v1.0b" rule).

    When `operational_events_log_root` is None, the field is OMITTED
    from the dict — JCS canonicalization then naturally omits it
    without emitting a JSON `null`. Implementers who pass `null`
    instead of omitting are non-conformant.
    """
    verdict = {
        "additional_verifications": list(additional_verifications),
        "exit_code": exit_code,
        "posture": posture,
        "trust_anchor_manifest_sha256": trust_anchor_manifest_sha256,
        "verifier_spec_version_supported": verifier_spec_version_supported,
        "verifier_version": verifier_version,
    }
    if operational_events_log_root is not None:
        verdict["operational_events_log_root"] = operational_events_log_root
    return verdict


def canonicalize_and_hash(verdict: dict) -> tuple[bytes, str]:
    canonical_bytes = jcs.canonicalize(verdict)
    return canonical_bytes, hashlib.sha256(canonical_bytes).hexdigest()


SUBCASES = (
    {
        "label": "036a",
        "description": (
            "Structural 2-field subset — PASS with no bonus verifications. "
            "Pins the empty-array shape in isolation."
        ),
        "verdict": build_verdict_subset(
            exit_code=0, additional_verifications=()
        ),
    },
    {
        "label": "036b",
        "description": (
            "Structural 2-field subset — PASS with a §10.42 backfill-seal "
            "bonus verification."
        ),
        "verdict": build_verdict_subset(
            exit_code=0,
            additional_verifications=("backfill_seal_verified",),
        ),
    },
    {
        "label": "036c",
        "description": (
            "Structural 2-field subset — PASS with two bonus verifications "
            "(forward-compat composition; second string is a placeholder "
            "demonstrating the two-entry array byte form)."
        ),
        "verdict": build_verdict_subset(
            exit_code=0,
            additional_verifications=(
                "backfill_seal_verified",
                _FORWARD_COMPAT_PLACEHOLDER,
            ),
        ),
    },
    {
        "label": "036d",
        "description": (
            "FULL §7 6-field shape — v1.0b PASS, no bonus verifications. "
            "Matches spec §7 byte-form example at line 1591."
        ),
        "verdict": build_verdict_full(
            exit_code=0,
            additional_verifications=(),
            posture=_PLACEHOLDER_POSTURE,
            trust_anchor_manifest_sha256=_PLACEHOLDER_TRUST_ANCHOR_SHA256,
            verifier_spec_version_supported=_PLACEHOLDER_SPEC_V1_0B,
            verifier_version=_PLACEHOLDER_VERIFIER_VERSION_V1_0B,
        ),
    },
    {
        "label": "036e",
        "description": (
            "FULL §7 6-field shape — v1.0b PASS with `backfill_seal_verified`. "
            "Matches spec §7 byte-form example at line 1597."
        ),
        "verdict": build_verdict_full(
            exit_code=0,
            additional_verifications=("backfill_seal_verified",),
            posture=_PLACEHOLDER_POSTURE,
            trust_anchor_manifest_sha256=_PLACEHOLDER_TRUST_ANCHOR_SHA256,
            verifier_spec_version_supported=_PLACEHOLDER_SPEC_V1_0B,
            verifier_version=_PLACEHOLDER_VERIFIER_VERSION_V1_0B,
        ),
    },
    {
        "label": "036f",
        "description": (
            "FULL §7 6-field shape — v1.0b PASS with two §10.69 "
            "class-disclosure bonus verifications. Matches spec §7 "
            "byte-form example at line 1603."
        ),
        "verdict": build_verdict_full(
            exit_code=0,
            additional_verifications=(
                "class_disclosure_subtree_verified",
                "cohort_coverage_attestation_verified",
            ),
            posture=_PLACEHOLDER_POSTURE,
            trust_anchor_manifest_sha256=_PLACEHOLDER_TRUST_ANCHOR_SHA256,
            verifier_spec_version_supported=_PLACEHOLDER_SPEC_V1_0B,
            verifier_version=_PLACEHOLDER_VERIFIER_VERSION_V1_0B,
        ),
    },
    {
        "label": "036g",
        "description": (
            "FULL §7 7-field shape — v1.0c PASS with sibling-log root "
            "binding (`operational_events_log_root` PRESENT under v1.0c). "
            "Matches spec §7 byte-form example at line 1609."
        ),
        "verdict": build_verdict_full(
            exit_code=0,
            additional_verifications=("sibling_log_root_verified",),
            posture=_PLACEHOLDER_POSTURE,
            trust_anchor_manifest_sha256=_PLACEHOLDER_TRUST_ANCHOR_SHA256,
            verifier_spec_version_supported=_PLACEHOLDER_SPEC_V1_0C,
            verifier_version=_PLACEHOLDER_VERIFIER_VERSION_V1_0C,
            operational_events_log_root=_PLACEHOLDER_OPERATIONAL_LOG_ROOT,
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
            "Input fixture for case 036-verdict-additional-verifications. "
            "Pins the verdict-object JCS-canonical bytes for seven "
            "sub-cases: three structural-subset shapes (036a/b/c, "
            "2-field) and four full-schema shapes (036d/e/f/g, 6-field "
            "v1.0b plus 7-field v1.0c). The conformance contract is "
            "that all seven sub-cases produce byte-identical output "
            "across implementations."
        ),
        "known_additional_verifications": list(KNOWN_ADDITIONAL_VERIFICATIONS),
        "subcases": results,
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # The expected_canonical.txt holds the THREE sub-case canonical byte
    # forms separated by a single LF — a reader can split on LF to recover
    # each sub-case. The expected_canonical_sha256.txt opens with a
    # `full_blob <hash>` line (SHA-256 of the entire expected_canonical.txt
    # blob — the verifier's "are the bytes I have the bytes the spec
    # intends" gate), followed by the per-sub-case labeled hex digests.
    # See README §"Multi-payload vector sha256 convention".
    blob_bytes = b""
    for i, r in enumerate(results):
        if i > 0:
            blob_bytes += b"\n"
        blob_bytes += r["canonical_bytes_utf8"].encode("utf-8")
    blob_bytes += b"\n"
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(blob_bytes)

    full_blob_sha256 = hashlib.sha256(blob_bytes).hexdigest()
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"full_blob               {full_blob_sha256}\n")
        for r in results:
            f.write(f"{r['label']} {r['canonical_sha256']}\n")

    for r in results:
        print(
            f"[036] {r['label']}: len={r['canonical_byte_length']:3d}  "
            f"sha256={r['canonical_sha256']}"
        )


if __name__ == "__main__":
    main()
