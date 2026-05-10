# -*- coding: utf-8 -*-
"""Compute the §10.47 + §10.48 generation chain-entry byte form for
FFIEC v1 test-vector case 041-generation-four-tuple.

§10.47 normates the four-tuple binding (system_prompt_sha256,
user_prompt_sha256, retrieval_set_merkle_root_sha256, output_sha256)
on a single chain entry. §10.48 extends with optional stochasticity-
attestation fields (temperature, top_p, top_k, seed, model_version,
model_weight_hash).

This case pins the JCS-canonical bytes for a Lyceum-shape clinical
decision support generation event with full §10.48 stochasticity
attestation. The retrieval_set_merkle_root_sha256 is the value pinned
by case 042-retrieval-set-merkle (the bidirectional cross-binding).

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


# Synthetic Lyceum-shape clinical decision support inference.
INFERENCE_AT_UTC = "2026-04-12T10:30:15Z"
MODEL_ID = "lyceum-medsynth-2026-04"

# Four-tuple hashes (§10.47).
SYSTEM_PROMPT_SHA256 = _sha256_of_label(
    "lyceum-clinical-decision-support-system-prompt-v3.1-2026-04"
)
USER_PROMPT_SHA256 = _sha256_of_label(
    "post-mi-statin-therapy-recommendation-query-patient-de-identified"
)
# This must equal the value pinned by case 042-retrieval-set-merkle.
RETRIEVAL_SET_MERKLE_ROOT_SHA256 = (
    "2aefda83d3521600b0b408d2c3d66e0e7d6e962490703774084f57323874a148"
)
OUTPUT_SHA256 = _sha256_of_label(
    "lyceum-synthesis-response-post-mi-statin-2026-04-12-canonical"
)

# §10.48 stochasticity attestation.
TEMPERATURE = 0.0
TOP_P = 1.0
TOP_K = 0
SEED = 42
MODEL_VERSION = "2026-04-08-rc3"
MODEL_WEIGHT_HASH = _sha256_of_label(
    "lyceum-medsynth-2026-04-08-rc3-weights-bundle"
)


def build_generation_event() -> dict:
    """§10.47 + §10.48 chain-entry payload."""
    return {
        "audit.generation.inference_at_utc": INFERENCE_AT_UTC,
        "audit.generation.model_id": MODEL_ID,
        "audit.generation.model_version": MODEL_VERSION,
        "audit.generation.model_weight_hash": MODEL_WEIGHT_HASH,
        "audit.generation.output_sha256": OUTPUT_SHA256,
        "audit.generation.retrieval_set_merkle_root_sha256": RETRIEVAL_SET_MERKLE_ROOT_SHA256,
        "audit.generation.seed": SEED,
        "audit.generation.system_prompt_sha256": SYSTEM_PROMPT_SHA256,
        "audit.generation.temperature": TEMPERATURE,
        "audit.generation.top_k": TOP_K,
        "audit.generation.top_p": TOP_P,
        "audit.generation.user_prompt_sha256": USER_PROMPT_SHA256,
    }


def main() -> None:
    event = build_generation_event()
    canonical_bytes = jcs.canonicalize(event)
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 041-generation-four-tuple — pins "
            "the §10.47 + §10.48 chain-entry byte form for a Lyceum-"
            "shape clinical decision support generation event. The "
            "retrieval_set_merkle_root_sha256 value is the Merkle root "
            "pinned by case 042-retrieval-set-merkle (cross-binding)."
        ),
        "event": event,
        "expected": {
            "canonical_byte_length": len(canonical_bytes),
            "canonical_sha256": canonical_sha256,
        },
        "cross_binding_with_042": {
            "retrieval_set_merkle_root_sha256": RETRIEVAL_SET_MERKLE_ROOT_SHA256,
            "note": "Must match case 042-retrieval-set-merkle's expected_retrieval_set_merkle_root.txt",
        },
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(canonical_bytes)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(canonical_sha256 + "\n")

    print(f"[041] model_id:                  {MODEL_ID}")
    print(f"[041] model_version:             {MODEL_VERSION}")
    print(f"[041] system_prompt_sha256:      {SYSTEM_PROMPT_SHA256}")
    print(f"[041] user_prompt_sha256:        {USER_PROMPT_SHA256}")
    print(f"[041] retrieval_set_merkle_root: {RETRIEVAL_SET_MERKLE_ROOT_SHA256}")
    print(f"[041] output_sha256:             {OUTPUT_SHA256}")
    print(f"[041] canonical len:             {len(canonical_bytes)}")
    print(f"[041] canonical SHA-256:         {canonical_sha256}")


if __name__ == "__main__":
    main()
