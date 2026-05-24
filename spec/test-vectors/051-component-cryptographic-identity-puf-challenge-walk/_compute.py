# -*- coding: utf-8 -*-
"""Compute the §10.58 PUF challenge-walk byte form for FFIEC v1
test-vector case 051-component-cryptographic-identity-puf-challenge-walk.

Spec §10.58 defines two verifier modes for component-cryptographic
identity:

  - Binding-walk (case 050) — verifier walks the chain entry's
    identity-binding hash; component need not be in-hand.
  - Challenge-walk (this case) — verifier challenges the component
    directly (PUF challenge-response, manufacturer-CA online
    verification) and confirms the chain entry's identity-binding
    matches the live component. Component MUST be in-hand.

For the `puf-response` identity-kind both modes are available; this
case pins the challenge-walk verifier output.

The challenge-walk verifier produces PASS (exit_code 0) with
`additional_verifications: ['component_identity_challenge_walk_verified']`.
The marker is the dispatch surface for tooling that requires
challenge-walk for a particular regulatory regime.

This case pins THREE byte-forms:

  1. The JCS-canonical bytes of the §10.58 `canonical_binding_input`
     JSON object — the chain-entry-bound binding-input (shared shape
     with case 050; the values match case 050 verbatim so the same
     synthetic component appears under both walks).

  2. The mocked PUF challenge-response oracle output: a structured
     dict pinning `puf_challenge_id`, `expected_response_hex` (the
     value bound on the chain entry), `live_response_hex` (the
     value returned by the mocked oracle at challenge-walk time),
     and `match` (boolean — true when the bytes are equal).

  3. The §10.12 verdict object emitted on challenge-walk PASS.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Pinned inputs — shared shape with case 050 (same synthetic component
# under both binding-walk and challenge-walk). Values mirror case 050
# verbatim so the binding-input bytes are byte-identical between the
# two cases.
# ---------------------------------------------------------------------------

IDENTITY_KIND = "puf-response"
COMPONENT_ID = "as6171-sample-component-2026-05-21-001"
PUF_CHALLENGE_ID = "darpa-shield-puf-challenge-class-A-2026-05"


def _synthetic_puf_response_hex() -> str:
    """Deterministic 32-byte PUF response. Recipe matches case 050 so
    the binding-input is byte-identical between the two cases.
    """
    seed = f"050-puf-response::component={COMPONENT_ID}::challenge={PUF_CHALLENGE_ID}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


EXPECTED_RESPONSE_HEX = _synthetic_puf_response_hex()

# The mocked challenge-walk oracle returns the same value the chain
# entry binds (this is the happy-path challenge-walk; the live
# component's PUF response matches the binding). A non-matching
# fixture is a negative case (see future N0XX).
LIVE_RESPONSE_HEX = EXPECTED_RESPONSE_HEX


def build_canonical_binding_input() -> dict:
    """§10.58 `canonical_binding_input` for the `puf-response` kind.
    Shape matches case 050; values are deliberately identical so the
    binding-hash composes cleanly across the two vectors.
    """
    return {
        "identity_kind": IDENTITY_KIND,
        "component_id": COMPONENT_ID,
        "puf_challenge_id": PUF_CHALLENGE_ID,
        "puf_response_hex": EXPECTED_RESPONSE_HEX,
    }


def build_challenge_oracle_output() -> dict:
    """The mocked PUF challenge-response oracle output. Pins the byte
    form a clean-room implementer's challenge-walk harness emits when
    challenging the component (mocked here) and comparing to the
    chain-bound expected response.

    `match` is computed deterministically; on the happy path it is
    `true` (live bytes == expected bytes).
    """
    match = LIVE_RESPONSE_HEX == EXPECTED_RESPONSE_HEX
    return {
        "puf_challenge_id": PUF_CHALLENGE_ID,
        "expected_response_hex": EXPECTED_RESPONSE_HEX,
        "live_response_hex": LIVE_RESPONSE_HEX,
        "match": match,
    }


# Pinned placeholder values for the verdict object (matching case 036
# and case 050's placeholders so this vector composes cleanly).
PLACEHOLDER_POSTURE = "ffiec"
PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
PLACEHOLDER_SPEC_VERSION = "v1.0c"
PLACEHOLDER_VERIFIER_VERSION = "v1.0c-verifier-2026-05-15"


def build_verdict() -> dict:
    """§10.12 verdict object the verifier emits on §10.58 challenge-walk
    success. PASS with `component_identity_challenge_walk_verified` marker.
    """
    return {
        "additional_verifications": ["component_identity_challenge_walk_verified"],
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
    binding_hash_hex = binding_sha256

    oracle_output = build_challenge_oracle_output()
    oracle_bytes, oracle_sha256 = canonicalize_and_hash(oracle_output)

    verdict = build_verdict()
    verdict_bytes, verdict_sha256 = canonicalize_and_hash(verdict)

    input_record = {
        "_about": (
            "Input fixture for case 051-component-cryptographic-identity-"
            "puf-challenge-walk. Pins THREE byte-forms: (1) the JCS-"
            "canonical bytes of the §10.58 `canonical_binding_input` for "
            "the `puf-response` kind (byte-identical to case 050 by "
            "design — same synthetic component under both walks); (2) the "
            "mocked PUF challenge-response oracle output pinning expected "
            "vs live response and the match boolean; (3) the §10.12 "
            "verdict object on challenge-walk PASS — exit_code 0 with "
            "`additional_verifications: "
            "['component_identity_challenge_walk_verified']`."
        ),
        "canonical_binding_input": binding_input,
        "canonical_binding_input_byte_length": len(binding_bytes),
        "canonical_binding_input_sha256": binding_sha256,
        "canonical_binding_input_bytes_utf8": binding_bytes.decode("utf-8"),
        "binding_hash_hex": binding_hash_hex,
        "challenge_oracle_output": oracle_output,
        "challenge_oracle_canonical_byte_length": len(oracle_bytes),
        "challenge_oracle_canonical_sha256": oracle_sha256,
        "challenge_oracle_canonical_bytes_utf8": oracle_bytes.decode("utf-8"),
        "verdict": verdict,
        "verdict_canonical_byte_length": len(verdict_bytes),
        "verdict_canonical_sha256": verdict_sha256,
        "verdict_canonical_bytes_utf8": verdict_bytes.decode("utf-8"),
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # expected_canonical.txt carries the three sub-forms separated by
    # a single LF each — readers split on LF to recover binding-input,
    # oracle-output, and verdict in that order. The
    # expected_canonical_sha256.txt opens with a `full_blob <hash>`
    # line (SHA-256 of the entire expected_canonical.txt blob),
    # followed by the per-sub-form labeled hex digests. See README
    # §"Multi-payload vector sha256 convention".
    blob_bytes = binding_bytes + b"\n" + oracle_bytes + b"\n" + verdict_bytes
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(blob_bytes)

    full_blob_sha256 = hashlib.sha256(blob_bytes).hexdigest()
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"full_blob                {full_blob_sha256}\n")
        f.write(f"canonical_binding_input  {binding_sha256}\n")
        f.write(f"binding_hash_hex         {binding_hash_hex}\n")
        f.write(f"challenge_oracle_output  {oracle_sha256}\n")
        f.write(f"verdict                  {verdict_sha256}\n")

    print(f"[051] identity kind:                  {IDENTITY_KIND}")
    print(f"[051] component_id:                   {COMPONENT_ID}")
    print(f"[051] binding-input canonical len:    {len(binding_bytes)}")
    print(f"[051] binding-input SHA-256:          {binding_sha256}")
    print(f"[051] challenge oracle canonical len: {len(oracle_bytes)}")
    print(f"[051] challenge oracle SHA-256:       {oracle_sha256}")
    print(f"[051] verdict canonical len:          {len(verdict_bytes)}")
    print(f"[051] verdict SHA-256:                {verdict_sha256}")


if __name__ == "__main__":
    main()
