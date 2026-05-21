# -*- coding: utf-8 -*-
"""Compute the §10.58 PUF binding-walk byte form for FFIEC v1
test-vector case 050-component-cryptographic-identity-puf-binding-walk.

Spec §10.58 normates the component-cryptographic-identity primitive.
Four identity-kinds are normative: `puf-response`, `seal-chiplet-
attestation`, `factory-provisioned-key`, `serial-lot-hash`. For every
chain entry carrying a §10.58 `cryptographic_identity`, the 32-byte
binding-hash is `SHA-256(JCS(canonical_binding_input))` where
`canonical_binding_input` is a JSON object carrying the identity-kind
tag plus per-kind payload fields.

This case pins TWO byte-forms:

  1. The JCS-canonical bytes of the `canonical_binding_input` JSON object
     for the `puf-response` identity-kind. A clean-room implementation
     constructing the same JSON object MUST produce byte-identical
     canonical bytes and therefore byte-identical 32-byte SHA-256
     binding-hash.

  2. The §10.12 verdict object emitted by a verifier running the §10.58
     binding-walk on a chain entry carrying the PUF identity. Per
     §10.58 verifier-mode dispatch: PASS (exit_code 0) with
     `additional_verifications: ['component_identity_binding_walk_verified']`.

Per spec §10.58 lines 3597-3604, the `canonical_binding_input` JSON
object for `puf-response`:

    {
      "identity_kind": "puf-response",
      "component_id": <string>,
      "puf_challenge_id": <string>,
      "puf_response_hex": <lowercase-hex string of the raw response bytes>
    }

JCS sorts keys lexicographically. Canonical key order:
`component_id`, `identity_kind`, `puf_challenge_id`, `puf_response_hex`.

Binding-walk does NOT require the component to be in-hand; the verifier
walks the chain entry's binding hash and confirms structural presence
plus per-event-MAC integrity binding. The marker is the dispatch surface
for tooling that requires binding-walk evidence.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Pinned inputs — a synthetic PUF identity binding for an institution-
# named component. The values are deterministic and reproducible from
# the recipe below; a clean-room implementer rebuilding from first
# principles gets byte-identical output.
# ---------------------------------------------------------------------------

IDENTITY_KIND = "puf-response"
COMPONENT_ID = "as6171-sample-component-2026-05-21-001"
PUF_CHALLENGE_ID = "darpa-shield-puf-challenge-class-A-2026-05"


# Synthetic 32-byte PUF response — derived deterministically from the
# component_id + challenge_id so the recipe is fully reproducible.
# Production PUF responses are 32 raw bytes from the on-die PUF; this
# fixture pins the byte-form layer, not PUF hardware behavior.
def _synthetic_puf_response_hex() -> str:
    """Deterministic 32-byte PUF response — SHA-256 of a recipe label
    so the binding-input is reproducible from first principles.
    """
    seed = f"050-puf-response::component={COMPONENT_ID}::challenge={PUF_CHALLENGE_ID}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


PUF_RESPONSE_HEX = _synthetic_puf_response_hex()


def build_canonical_binding_input() -> dict:
    """The JSON object whose JCS-canonical bytes hash to the binding-hash
    per §10.58. Keys appear in source order; JCS sorts them
    lexicographically at canonicalization time.
    """
    return {
        "identity_kind": IDENTITY_KIND,
        "component_id": COMPONENT_ID,
        "puf_challenge_id": PUF_CHALLENGE_ID,
        "puf_response_hex": PUF_RESPONSE_HEX,
    }


# Pinned placeholder values for the verdict object (matching case 036's
# full-shape placeholders so this vector composes cleanly).
PLACEHOLDER_POSTURE = "ffiec"
PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
PLACEHOLDER_SPEC_VERSION = "v1.0c"
PLACEHOLDER_VERIFIER_VERSION = "v1.0c-verifier-2026-05-15"


def build_verdict() -> dict:
    """§10.12 verdict object the verifier emits on §10.58 binding-walk
    success. PASS with `component_identity_binding_walk_verified` marker.
    """
    return {
        "additional_verifications": ["component_identity_binding_walk_verified"],
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
    binding_input = build_canonical_binding_input()
    binding_bytes, binding_sha256 = canonicalize_and_hash(binding_input)
    # The 32-byte binding-hash IS the SHA-256 of the JCS bytes per
    # §10.58. binding_sha256 above is exactly that hash; we pin it as
    # the binding_hash field so a clean-room implementer comparing
    # against the chain-entry's `cryptographic_identity.binding_hash`
    # value gets a direct match.
    binding_hash_hex = binding_sha256

    verdict = build_verdict()
    verdict_bytes, verdict_sha256 = canonicalize_and_hash(verdict)

    input_record = {
        "_about": (
            "Input fixture for case 050-component-cryptographic-identity-"
            "puf-binding-walk. Pins TWO byte-forms: (1) the JCS-canonical "
            "bytes of the §10.58 `canonical_binding_input` JSON object "
            "for the `puf-response` identity-kind, whose SHA-256 IS the "
            "32-byte binding-hash; (2) the §10.12 verdict object the "
            "verifier emits on binding-walk PASS — exit_code 0 with "
            "`additional_verifications: "
            "['component_identity_binding_walk_verified']`. The synthetic "
            "PUF response is deterministic per the recipe in _compute.py."
        ),
        "canonical_binding_input": binding_input,
        "canonical_binding_input_byte_length": len(binding_bytes),
        "canonical_binding_input_sha256": binding_sha256,
        "canonical_binding_input_bytes_utf8": binding_bytes.decode("utf-8"),
        "binding_hash_hex": binding_hash_hex,
        "verdict": verdict,
        "verdict_canonical_byte_length": len(verdict_bytes),
        "verdict_canonical_sha256": verdict_sha256,
        "verdict_canonical_bytes_utf8": verdict_bytes.decode("utf-8"),
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # expected_canonical.txt carries the binding-input bytes followed
    # by a single LF and then the verdict bytes — readers split on LF
    # to recover each sub-form. This mirrors case 036's multi-subcase
    # composition pattern.
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(binding_bytes)
        f.write(b"\n")
        f.write(verdict_bytes)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"canonical_binding_input {binding_sha256}\n")
        f.write(f"binding_hash_hex        {binding_hash_hex}\n")
        f.write(f"verdict                 {verdict_sha256}\n")

    print(f"[050] identity kind:                 {IDENTITY_KIND}")
    print(f"[050] component_id:                  {COMPONENT_ID}")
    print(f"[050] binding-input canonical len:   {len(binding_bytes)}")
    print(f"[050] binding-input SHA-256:         {binding_sha256}")
    print(f"[050] binding_hash (= input SHA-256):{binding_hash_hex}")
    print(f"[050] verdict canonical len:         {len(verdict_bytes)}")
    print(f"[050] verdict SHA-256:               {verdict_sha256}")


if __name__ == "__main__":
    main()
