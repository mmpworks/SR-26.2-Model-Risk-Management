# -*- coding: utf-8 -*-
"""Compute the §10.42 backfill-seal record byte form for FFIEC v1
test-vector case 035-backfill-seal.

Spec §10.42 normates a one-time backfill seal record at acquisition close
when the acquired institution's pre-acquisition records are under a
non-chain shape (`baseline_manifest_kind ∈ {"baseline_diary", "mixed"}`).
The backfill seal is a v1.0b sign_payload-bound seal record where the
additional §10.42 attributes are bound through the Merkle root: the root
covers the institutional baseline manifest leaves AND a metadata leaf
carrying the §10.42 attributes.

This case pins:
  (a) the §10.42 metadata-leaf JCS-canonical bytes — the structure that
      carries `seal.backfill_at_close = true`, the window timestamps, the
      baseline-manifest cross-binding hash, the companion attestation
      run_id, and the dual_signatures;
  (b) the Merkle root over (8 institutional baseline manifest leaves +
      1 metadata leaf) under RFC 6962;
  (c) the v1.0b sign_payload form for this seal (the 12-line newline-joined
      bytes the HSM signs — the signature itself is outside this vector's
      scope; case 018 pins the v1.0b form generally).

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Pinned inputs — Northbridge / Cape Madeline shaped backfill seal.
# The companion §10.39 successor-attestation event lives in case 034; the
# bidirectional linkage is enforced by reusing the same run_id and the
# same baseline-manifest SHA-256.
TENANT_ID = "northbridge-federal-savings"
SEAL_DATE = "2026-04-15"
SIGN_PAYLOAD_VERSION = "v1.0b"
ALGORITHM = "ed25519"
FORMAT_VERSION = "v1"
CADENCE = "daily"
DEV_MODE = False
KEY_VERSIONS_CANON = "1"
KMS_HANDLE_URIS_DIGEST_HEX = (
    "5d4f1e9c2b8a7f6e3d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d8c9b0a1f2e"
)
# hkdf_inputs_digest_hex — synthetic for case 035; the institutional HKDF
# inputs are pinned in case 010 et al. Surfaced into input.json so the full
# sign_payload byte form is reconstructible from the input alone.
HKDF_INPUTS_DIGEST_HEX = (
    "0a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9"
)


# §10.42 metadata-leaf inputs.
BACKFILL_AT_CLOSE = True
BACKFILL_WINDOW_START_UTC = "2024-10-15T00:00:00Z"
BACKFILL_WINDOW_END_UTC = "2026-04-15T14:00:00Z"
BACKFILL_COMPANION_ATTESTATION_RUN_ID = (
    "northbridge-cape-madeline-close-2026-04-15"
)


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic baseline manifest — same recipe as case 034. JCS-canonical
# sorted array of {kind, identifier, sha256} tuples. The cross-binding
# hash MUST match case 034's baseline_manifest_sha256.
_BASELINE_MANIFEST_TUPLES = [
    {
        "identifier": f"cape-madeline-loan-orig-{n:04d}",
        "kind": "baseline_diary_record",
        "sha256": _sha256_of_label(f"cape-madeline-loan-orig-{n:04d}"),
    }
    for n in range(8)
]
_BASELINE_MANIFEST_BYTES = jcs.canonicalize(_BASELINE_MANIFEST_TUPLES)
BACKFILL_BASELINE_MANIFEST_SHA256 = hashlib.sha256(_BASELINE_MANIFEST_BYTES).hexdigest()


# Synthetic dual_signatures — same shape as case 034. The bidirectional
# §10.39 ↔ §10.42 linkage means both events carry the same dual_signatures
# pair (same authorities sign both events at acquisition close).
DUAL_SIGNATURES = [
    {
        "entity_affiliation": "from_entity",
        "name": "Helena R. Vasquez",
        "role": "CISO",
        "signature_b64": (
            "VqK9NvDpFmK0Dc/oM7lY30+JsgcDEx8/UMDuFY3hjkJK/yNfjhMCk1ZQ"
            "qPHt8FgLKp5dzGzCyc6f3Qd0XpLq8w=="
        ),
    },
    {
        "entity_affiliation": "to_entity",
        "name": "Marcus K. Tan",
        "role": "CISO",
        "signature_b64": (
            "Qq2L4HtIfBp9KrM6w0aXyEcBkM8RzfL2VbCnDjY1nXh/oTpFxKsYbWmU"
            "rLkPvNcGdHgQzSjOaWeRtUiAsBfDqE=="
        ),
    },
]


def build_metadata_leaf() -> dict:
    """§10.42 metadata-leaf — six fields, byte-locked schema.

    The leaf is JCS-canonicalized and its SHA-256 is included as the
    final leaf in the seal's Merkle tree. The Merkle root binds both the
    institutional baseline manifest leaves and this metadata leaf; a
    tampering of any §10.42 attribute surfaces as a Merkle-root mismatch
    at verification.
    """
    return {
        "seal.backfill_at_close": BACKFILL_AT_CLOSE,
        "seal.backfill_baseline_manifest_sha256": BACKFILL_BASELINE_MANIFEST_SHA256,
        "seal.backfill_companion_attestation_run_id": BACKFILL_COMPANION_ATTESTATION_RUN_ID,
        "seal.backfill_window_end_utc": BACKFILL_WINDOW_END_UTC,
        "seal.backfill_window_start_utc": BACKFILL_WINDOW_START_UTC,
        "seal.dual_signatures": DUAL_SIGNATURES,
    }


# RFC 6962 leaf-hash and inner-hash domain separators (per §4.2 / §10.37).
_LEAF_HASH_PREFIX = b"\x00"
_INTERNAL_HASH_PREFIX = b"\x01"


def _leaf_hash(canonical_leaf_bytes: bytes) -> bytes:
    return hashlib.sha256(_LEAF_HASH_PREFIX + canonical_leaf_bytes).digest()


def _inner_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(_INTERNAL_HASH_PREFIX + left + right).digest()


def _largest_power_of_2_less_than(n: int) -> int:
    if n <= 1:
        raise ValueError(f"_largest_power_of_2_less_than requires n > 1; got {n}")
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def _merkle_root(leaf_payloads: list[bytes]) -> bytes:
    """RFC 6962 §2.1 tree hash over an ordered sequence of leaf payloads.

    Splits at the largest power of 2 strictly less than the leaf count
    (the canonical RFC 6962 split, not naive pairwise level-by-level).
    Same construction as §4.2 daily Merkle seal and §10.31 inclusion-
    proof verification.
    """
    n = len(leaf_payloads)
    if n == 0:
        return hashlib.sha256(b"").digest()
    if n == 1:
        return _leaf_hash(leaf_payloads[0])
    k = _largest_power_of_2_less_than(n)
    left = _merkle_root(leaf_payloads[:k])
    right = _merkle_root(leaf_payloads[k:])
    return _inner_hash(left, right)


def build_sign_payload(merkle_root_hex: str) -> bytes:
    """v1.0b sign_payload — the 12-line newline-joined bytes the HSM signs.

    Mirrors case 018's recipe; this function is expressed here for the
    backfill seal's cross-binding test, NOT as an alternative form. The
    backfill seal IS a v1.0b sign_payload record (locked 12-line form
    unchanged); the §10.42 attributes are bound through `merkle_root_hex`
    via the metadata leaf.
    """
    lines = [
        "ffiec.chain-of-custody.v1",
        SIGN_PAYLOAD_VERSION,
        ALGORITHM,
        FORMAT_VERSION,
        TENANT_ID,
        SEAL_DATE,
        merkle_root_hex,
        HKDF_INPUTS_DIGEST_HEX,
        CADENCE,
        "0" if not DEV_MODE else "1",
        KEY_VERSIONS_CANON,
        KMS_HANDLE_URIS_DIGEST_HEX,
    ]
    return ("\n".join(lines)).encode("utf-8")


def main() -> None:
    # Step 1: canonicalize the metadata leaf.
    metadata_leaf = build_metadata_leaf()
    metadata_leaf_bytes = jcs.canonicalize(metadata_leaf)

    # Step 2: canonicalize the 8 baseline manifest leaves.
    baseline_leaf_payloads = [
        jcs.canonicalize(tup) for tup in _BASELINE_MANIFEST_TUPLES
    ]

    # Step 3: RFC 6962 Merkle root over (baseline payloads + metadata payload).
    # _merkle_root applies LEAF_HASH internally and recurses with the
    # canonical largest-power-of-2 split.
    all_leaf_payloads = baseline_leaf_payloads + [metadata_leaf_bytes]
    merkle_root = _merkle_root(all_leaf_payloads)
    merkle_root_hex = merkle_root.hex()

    # Step 4: build the v1.0b sign_payload bytes. The signature itself is
    # outside this vector's scope (case 018 pins the v1.0b signature path).
    sign_payload_bytes = build_sign_payload(merkle_root_hex)
    sign_payload_sha256 = hashlib.sha256(sign_payload_bytes).hexdigest()

    metadata_leaf_canonical_sha256 = hashlib.sha256(metadata_leaf_bytes).hexdigest()

    input_record = {
        "_about": (
            "Input fixture for case 035-backfill-seal — the §10.42 "
            "backfill-seal record byte form. Composes with case 034 "
            "(successor-attestation) via the bidirectional run_id "
            "linkage and the shared baseline-manifest hash. The seal is "
            "a v1.0b sign_payload-bound record where §10.42 attributes "
            "are bound through the Merkle root via the metadata leaf."
        ),
        "metadata_leaf": metadata_leaf,
        "synthetic_baseline_manifest": {
            "tuples": _BASELINE_MANIFEST_TUPLES,
            "leaf_count": len(_BASELINE_MANIFEST_TUPLES),
            "canonical_byte_length": len(_BASELINE_MANIFEST_BYTES),
            "sha256": BACKFILL_BASELINE_MANIFEST_SHA256,
        },
        "sign_payload_inputs": {
            "tenant_id": TENANT_ID,
            "seal_date": SEAL_DATE,
            "sign_payload_version": SIGN_PAYLOAD_VERSION,
            "algorithm": ALGORITHM,
            "format_version": FORMAT_VERSION,
            "cadence": CADENCE,
            "dev_mode": DEV_MODE,
            "hkdf_inputs_digest_hex": HKDF_INPUTS_DIGEST_HEX,
            "key_versions_canon": KEY_VERSIONS_CANON,
            "kms_handle_uris_digest_hex": KMS_HANDLE_URIS_DIGEST_HEX,
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(metadata_leaf_bytes)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(metadata_leaf_canonical_sha256 + "\n")

    with open(os.path.join(HERE, "expected_sign_payload.txt"), "wb") as f:
        f.write(sign_payload_bytes)

    with open(
        os.path.join(HERE, "expected_sign_payload_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(sign_payload_sha256 + "\n")

    with open(
        os.path.join(HERE, "expected_merkle_root_hex.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(merkle_root_hex + "\n")

    print(f"[035] tenant_id:                    {TENANT_ID}")
    print(f"[035] seal_date:                    {SEAL_DATE}")
    print(f"[035] baseline manifest SHA-256:    {BACKFILL_BASELINE_MANIFEST_SHA256}")
    print(f"[035] metadata leaf canonical len:  {len(metadata_leaf_bytes)}")
    print(f"[035] metadata leaf SHA-256:        {metadata_leaf_canonical_sha256}")
    print(f"[035] merkle root (9 leaves):       {merkle_root_hex}")
    print(f"[035] sign_payload byte length:     {len(sign_payload_bytes)}")
    print(f"[035] sign_payload SHA-256:         {sign_payload_sha256}")


if __name__ == "__main__":
    main()
