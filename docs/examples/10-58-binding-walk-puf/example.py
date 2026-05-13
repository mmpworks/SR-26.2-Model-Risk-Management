"""Worked example of the §10.58 binding-walk verifier mode for `puf-response`.

Demonstrates the binding-hash construction (SHA-256 over §5 RFC 8785 JCS
canonical bytes of a `canonical_binding_input` JSON object) and the binding-walk
verifier recompute that produces PASS with `additional_verifications:
['component_identity_binding_walk_verified']` per §10.58 + §10.12.

Run: pip install jcs ; python example.py

Cross-references: §5, §10.12, §10.58, §7.
"""

from __future__ import annotations

import hashlib

import jcs


# --- Construction --------------------------------------------------------

def compute_binding_hash(identity_kind: str, payload: dict[str, str]) -> bytes:
    """Compute the 32-byte binding-hash per §10.58.

    canonical_binding_input is a JSON object carrying the identity_kind tag
    plus per-kind payload fields. §5 JCS canonicalization produces byte-
    identical bytes across conformant implementations regardless of the
    object's in-memory key order.
    """
    canonical_binding_input = {"identity_kind": identity_kind, **payload}
    canonical_bytes = jcs.canonicalize(canonical_binding_input)
    return hashlib.sha256(canonical_bytes).digest()


def build_chain_entry_cryptographic_identity(
    component_id: str,
    puf_challenge_id: str,
    puf_response_hex: str,
) -> dict[str, str]:
    """Construct the §10.58 cryptographic_identity attribute payload."""
    payload = {
        "component_id": component_id,
        "puf_challenge_id": puf_challenge_id,
        "puf_response_hex": puf_response_hex,
    }
    binding_hash = compute_binding_hash("puf-response", payload)
    return {
        "identity_kind": "puf-response",
        **payload,
        "binding_hash": binding_hash.hex(),
    }


# --- Verifier ------------------------------------------------------------

def binding_walk_verify(cryptographic_identity: dict[str, str]) -> tuple[bool, str]:
    """Run §10.58 binding-walk verifier mode against the stamped identity.

    Returns (ok, marker_or_reason). On PASS, marker is the §10.58 PASS marker.
    On FAIL, the second element is the named reason string (per §7's
    byte-for-byte normative reason-string discipline).
    """
    stamped_hex = cryptographic_identity["binding_hash"]
    payload = {
        "component_id": cryptographic_identity["component_id"],
        "puf_challenge_id": cryptographic_identity["puf_challenge_id"],
        "puf_response_hex": cryptographic_identity["puf_response_hex"],
    }
    recomputed = compute_binding_hash(
        cryptographic_identity["identity_kind"], payload
    )
    if recomputed.hex() != stamped_hex:
        return False, "binding-hash mismatch: canonical_binding_input non-conformant"
    return True, "component_identity_binding_walk_verified"


# --- Demonstration -------------------------------------------------------

def main() -> None:
    component_id = "tpu-3-chassis-7-fpga-12"
    puf_challenge_id = "challenge-ffiec-prd4-050"
    puf_response_hex = (
        "5a3c9b2fae4e0d2cf1a8b6473e9d1c8a"
        "2bf5e6d4a7c3b1f8e9d2a6c4b7f3e1d5"
    )

    cryptographic_identity = build_chain_entry_cryptographic_identity(
        component_id=component_id,
        puf_challenge_id=puf_challenge_id,
        puf_response_hex=puf_response_hex,
    )

    print("--- canonical_binding_input (§5 JCS bytes) ---")
    payload_only = {k: v for k, v in cryptographic_identity.items() if k != "binding_hash"}
    print(jcs.canonicalize(payload_only).decode("utf-8"))

    print()
    print("--- chain entry's cryptographic_identity attribute ---")
    for k, v in cryptographic_identity.items():
        print(f"  {k}: {v}")

    print()
    print("--- binding-walk verifier ---")
    ok, marker_or_reason = binding_walk_verify(cryptographic_identity)
    if ok:
        print("  Status: PASS")
        print(f"  additional_verifications: ['{marker_or_reason}']")
        print("  Exit code: 0 (per §10.12)")
    else:
        print("  Status: FAIL")
        print(f"  Reason: {marker_or_reason}")
        print("  Exit code: 1 (per §10.12)")


if __name__ == "__main__":
    main()
