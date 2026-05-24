# -*- coding: utf-8 -*-
"""Compute the §10.21.2 parallel-evaluator-composition byte form for FFIEC
v1 test-vector case 052-parallel-evaluator-composition.

Spec §10.21.2 normates the parallel-evaluator composition pattern: two
or more independent parties evaluate the same subject, each operating
its own chain, with the chains composing at a target-anchor boundary
via a §10.21.2 cross-anchor entry. Canonical instances: lab-internal
+ AI Safety Institute parallel evaluation chains anchored at the
target-model-weights chain entry (§10.67); cedent + reinsurer
parallel chains anchored at the claim-handover (§10.45); institutional
clinical + Cleveland Clinic observer chains anchored at output-grounding
(§10.50); etc.

This case pins the byte forms for the **lab + AISI cardinality-2 known-
cardinality regime** anchored at target-model-weights:

  - Lab evaluator chain entry (§10.21.2 cross-anchor side A)
  - AISI evaluator chain entry (§10.21.2 cross-anchor side B)
  - Combined verifier output dict pinning the §10.12 verdict the
    verifier emits when both evaluator chains resolve and the
    target-anchor hash-binding succeeds.

Per §10.21.2 verifier dispatch (spec lines 2522-2523):

  - On PASS the verifier emits `additional_verifications:
    ['parallel_evaluator_anchor_verified']`.
  - When cardinality is present and discovered evaluators < cardinality,
    the verifier emits an anomaly line under Status: PASS of the form
    `parallel-evaluator coverage incomplete: declared cardinality {N},
    observed {M}`.
  - Cardinality = 2 known-cardinality regime — both evaluators present;
    no incomplete-coverage anomaly.

The §10.21.2 schema additions on each cross-anchor entry:

  audit.parallel_evaluator.evaluator_identity (yes)
  audit.parallel_evaluator.evaluator_role (yes; enum)
  audit.parallel_evaluator.target_anchor_chain_entry_id (yes)
  audit.parallel_evaluator.evaluator_chain_entry_id (when applicable)
  audit.parallel_evaluator.cardinality (yes; integer or "dynamic")

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Pinned inputs — synthetic lab + AISI parallel-evaluator chain anchored
# at a synthetic target-model-weights chain entry. The values are
# deterministic; recipes are documented so a clean-room implementer
# can recompute byte-for-byte.
# ---------------------------------------------------------------------------

# Target-anchor chain-entry identifier — the chain entry that binds the
# target-model-weights both evaluators anchor against. Synthetic value;
# the chain entry itself is referenced by id only.
TARGET_ANCHOR_CHAIN_ENTRY_ID = (
    "target-model-weights-chain-entry-2026-05-21-frontier-model-v3-deploy"
)


def _evaluator_chain_entry_id(evaluator_identity: str) -> str:
    """Synthetic chain-entry id for an evaluator's own evaluation chain
    entry. Production ids are institution-issued; the fixture pins a
    deterministic recipe so the byte form is reproducible.
    """
    return f"evaluator-chain-entry-2026-05-21::{evaluator_identity}"


# Cardinality-2 known-cardinality regime — exactly two evaluators:
# (1) lab-internal-eval, role regulatory-equivalent (the lab's own
#     pre-deployment evaluation under voluntary partnership framing);
# (2) aisi-program-evaluation, role regulatory-equivalent (the AI
#     Safety Institute parallel chain under the AISI Reference
#     Evaluation Program).
CARDINALITY = 2

LAB_EVALUATOR_IDENTITY = "lab-internal-eval"
LAB_EVALUATOR_ROLE = "regulatory-equivalent"
LAB_EVALUATOR_CHAIN_ENTRY_ID = _evaluator_chain_entry_id(LAB_EVALUATOR_IDENTITY)

AISI_EVALUATOR_IDENTITY = "aisi-program-evaluation"
AISI_EVALUATOR_ROLE = "regulatory-equivalent"
AISI_EVALUATOR_CHAIN_ENTRY_ID = _evaluator_chain_entry_id(AISI_EVALUATOR_IDENTITY)


def build_cross_anchor_entry(
    *,
    evaluator_identity: str,
    evaluator_role: str,
    evaluator_chain_entry_id: str,
) -> dict:
    """Build a §10.21.2 cross-anchor entry's parallel-evaluator attribute
    set per spec lines 2514-2521. Keys appear in source order; JCS
    sorts lexicographically.

    Attribute names use the spec's dotted `audit.parallel_evaluator.*`
    schema verbatim. The full chain-entry envelope (the wrapping OTLP
    event, run_id, seq, payload_hash, etc.) is out of scope for this
    case — this fixture pins only the §10.21.2-specific attribute set
    that distinguishes parallel-evaluator cross-anchors from generic
    §10.21 cross-anchors.
    """
    return {
        "audit.parallel_evaluator.cardinality": CARDINALITY,
        "audit.parallel_evaluator.evaluator_chain_entry_id": evaluator_chain_entry_id,
        "audit.parallel_evaluator.evaluator_identity": evaluator_identity,
        "audit.parallel_evaluator.evaluator_role": evaluator_role,
        "audit.parallel_evaluator.target_anchor_chain_entry_id": (
            TARGET_ANCHOR_CHAIN_ENTRY_ID
        ),
    }


# Pinned placeholder values for the verdict object (matching case 036
# and case 050/051's placeholders so the composition is consistent
# across Phase 11 vectors).
PLACEHOLDER_POSTURE = "ffiec"
PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
PLACEHOLDER_SPEC_VERSION = "v1.0c"
PLACEHOLDER_VERIFIER_VERSION = "v1.0c-verifier-2026-05-15"


def build_verdict() -> dict:
    """§10.12 verdict object on §10.21.2 cross-anchor PASS. Both
    evaluator chains resolved; hash-binding verified at the target-
    anchor boundary; cardinality (2) observed matches declared.
    Marker: `parallel_evaluator_anchor_verified`.
    """
    return {
        "additional_verifications": ["parallel_evaluator_anchor_verified"],
        "exit_code": 0,
        "posture": PLACEHOLDER_POSTURE,
        "trust_anchor_manifest_sha256": PLACEHOLDER_TRUST_ANCHOR_SHA256,
        "verifier_spec_version_supported": PLACEHOLDER_SPEC_VERSION,
        "verifier_version": PLACEHOLDER_VERIFIER_VERSION,
    }


def canonicalize_and_hash(obj: dict) -> tuple[bytes, str]:
    canonical_bytes = jcs.canonicalize(obj)
    return canonical_bytes, hashlib.sha256(canonical_bytes).hexdigest()


def main() -> None:
    lab_entry = build_cross_anchor_entry(
        evaluator_identity=LAB_EVALUATOR_IDENTITY,
        evaluator_role=LAB_EVALUATOR_ROLE,
        evaluator_chain_entry_id=LAB_EVALUATOR_CHAIN_ENTRY_ID,
    )
    lab_bytes, lab_sha256 = canonicalize_and_hash(lab_entry)

    aisi_entry = build_cross_anchor_entry(
        evaluator_identity=AISI_EVALUATOR_IDENTITY,
        evaluator_role=AISI_EVALUATOR_ROLE,
        evaluator_chain_entry_id=AISI_EVALUATOR_CHAIN_ENTRY_ID,
    )
    aisi_bytes, aisi_sha256 = canonicalize_and_hash(aisi_entry)

    verdict = build_verdict()
    verdict_bytes, verdict_sha256 = canonicalize_and_hash(verdict)

    # Composed fixture pinning both evaluator entries plus the verdict
    # under a single record so a clean-room implementer can compare
    # the full §10.21.2 composition byte-for-byte.
    composed = {
        "cardinality_declared": CARDINALITY,
        "cardinality_observed": 2,
        "evaluators": [lab_entry, aisi_entry],
        "target_anchor_chain_entry_id": TARGET_ANCHOR_CHAIN_ENTRY_ID,
        "verdict": verdict,
    }
    composed_bytes, composed_sha256 = canonicalize_and_hash(composed)

    input_record = {
        "_about": (
            "Input fixture for case 052-parallel-evaluator-composition. "
            "Pins the §10.21.2 cross-anchor byte forms for a cardinality-2 "
            "known-cardinality regime (lab-internal-eval + aisi-program-"
            "evaluation) anchored at a synthetic target-model-weights "
            "chain entry. Pins (1) each evaluator's §10.21.2 attribute "
            "set in isolation; (2) the §10.12 verdict object the verifier "
            "emits on PASS — exit_code 0 with `additional_verifications: "
            "['parallel_evaluator_anchor_verified']`; (3) the composed "
            "record carrying both evaluators plus the verdict under one "
            "byte-form pin."
        ),
        "target_anchor_chain_entry_id": TARGET_ANCHOR_CHAIN_ENTRY_ID,
        "cardinality": CARDINALITY,
        "lab_cross_anchor_entry": lab_entry,
        "lab_cross_anchor_canonical_byte_length": len(lab_bytes),
        "lab_cross_anchor_canonical_sha256": lab_sha256,
        "lab_cross_anchor_canonical_bytes_utf8": lab_bytes.decode("utf-8"),
        "aisi_cross_anchor_entry": aisi_entry,
        "aisi_cross_anchor_canonical_byte_length": len(aisi_bytes),
        "aisi_cross_anchor_canonical_sha256": aisi_sha256,
        "aisi_cross_anchor_canonical_bytes_utf8": aisi_bytes.decode("utf-8"),
        "verdict": verdict,
        "verdict_canonical_byte_length": len(verdict_bytes),
        "verdict_canonical_sha256": verdict_sha256,
        "verdict_canonical_bytes_utf8": verdict_bytes.decode("utf-8"),
        "composed_record": composed,
        "composed_canonical_byte_length": len(composed_bytes),
        "composed_canonical_sha256": composed_sha256,
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # expected_canonical.txt carries the composed-record bytes as the
    # primary pin (it carries both sub-forms inside it). The
    # expected_canonical_sha256.txt opens with a `full_blob <hash>`
    # line (SHA-256 of the entire expected_canonical.txt blob — which
    # for this case equals the composed-record hash because composed
    # IS the blob), followed by the per-sub-form labeled hex digests.
    # See README §"Multi-payload vector sha256 convention".
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(composed_bytes)

    full_blob_sha256 = hashlib.sha256(composed_bytes).hexdigest()
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"full_blob          {full_blob_sha256}\n")
        f.write(f"lab_cross_anchor   {lab_sha256}\n")
        f.write(f"aisi_cross_anchor  {aisi_sha256}\n")
        f.write(f"verdict            {verdict_sha256}\n")
        f.write(f"composed_record    {composed_sha256}\n")

    print(f"[052] target anchor:               {TARGET_ANCHOR_CHAIN_ENTRY_ID}")
    print(f"[052] cardinality (declared/obs):  {CARDINALITY}/2")
    print(f"[052] lab cross-anchor len:        {len(lab_bytes)}")
    print(f"[052] lab cross-anchor SHA-256:    {lab_sha256}")
    print(f"[052] aisi cross-anchor len:       {len(aisi_bytes)}")
    print(f"[052] aisi cross-anchor SHA-256:   {aisi_sha256}")
    print(f"[052] verdict canonical len:       {len(verdict_bytes)}")
    print(f"[052] verdict SHA-256:             {verdict_sha256}")
    print(f"[052] composed canonical len:      {len(composed_bytes)}")
    print(f"[052] composed canonical SHA-256:  {composed_sha256}")


if __name__ == "__main__":
    main()
