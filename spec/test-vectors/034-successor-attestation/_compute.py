# -*- coding: utf-8 -*-
"""Compute the §10.39 successor-attestation envelope JCS-canonical bytes
for FFIEC v1 test-vector case 034-successor-attestation.

Spec §10.39 normates the `chain.successor_attestation` operational
event emitted on the acquirer's chain at acquisition close when the
acquired institution's pre-acquisition records are not under a chain
conformant to this specification. The envelope schema is byte-locked
across implementations.

This case pins the JCS-canonical bytes for a Northbridge-shaped
successor-attestation envelope (Northbridge acquires Cape Madeline; Cape
Madeline operated baseline-diary records) so a clean-room implementation
proves it constructs the §10.39 envelope identically. The dual_signatures
content is a synthetic placeholder (case 034 exercises the envelope byte
form, not Ed25519 signature verification — that's covered by sign_payload
test vectors).

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Pinned inputs — Northbridge / Cape Madeline shaped envelope.
ACQUIRED_ENTITY_LEGAL_NAME = "Cape Madeline Bank & Trust"
ACQUIRED_ENTITY_LEI = "529900CMBT034FFIEC01"  # 20-char synthetic LEI
BASELINE_MANIFEST_KIND = "baseline_diary"
EFFECTIVE_UTC = "2026-04-15T14:00:00Z"


def _sha256_of_label(label: str) -> str:
    """Lowercase hex SHA-256 of a label — used to seed deterministic hashes."""
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic baseline manifest — a JCS-canonical sorted array of
# {kind, identifier, sha256} tuples representing what was inherited.
# The baseline manifest's hash binds the institution-side enumeration of
# inherited artifacts to the chain at attestation time.
_BASELINE_MANIFEST_TUPLES = [
    {
        "identifier": f"cape-madeline-loan-orig-{n:04d}",
        "kind": "baseline_diary_record",
        "sha256": _sha256_of_label(f"cape-madeline-loan-orig-{n:04d}"),
    }
    for n in range(8)
]
_BASELINE_MANIFEST_BYTES = jcs.canonicalize(_BASELINE_MANIFEST_TUPLES)
BASELINE_MANIFEST_SHA256 = hashlib.sha256(_BASELINE_MANIFEST_BYTES).hexdigest()


# Acquirer-HSM key fingerprint — SHA-256 of a synthetic 32-byte HSM
# public-key. Production fingerprints are SHA-256 of an Ed25519 public key
# bytes; case 034 pins the envelope byte form, not the HSM custody chain.
_ACQUIRER_HSM_PUBKEY = hashlib.sha256(
    b"034-northbridge-acquirer-hsm-pubkey-v1"
).digest()
ACQUIRER_HSM_KEY_FINGERPRINT = hashlib.sha256(_ACQUIRER_HSM_PUBKEY).hexdigest()


# Companion §10.42 backfill-seal run_id — the cross-reference linkage from
# §10.39 to the paired §10.42 record (case 035 pins that record's bytes).
COMPANION_BACKFILL_SEAL_RUN_ID = "northbridge-cape-madeline-close-2026-04-15"


# Synthetic dual_signatures — two §10.17-shaped signature objects, the
# from-entity (Cape Madeline CISO) and the to-entity (Northbridge CISO).
# Each carries `role`, `name`, `entity_affiliation` per §10.17 plus a
# synthetic `signature_b64` placeholder.
DUAL_SIGNATURES = [
    {
        "entity_affiliation": "from_entity",
        "name": "Helena R. Vasquez",
        "role": "CISO",
        "signature_b64": (
            # Synthetic 64-byte Ed25519 signature placeholder. Recipe:
            # SHA-256("034-from-signature") || SHA-256("034-from-signature-2")
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


def build_successor_attestation_envelope() -> dict:
    """§10.39 successor-attestation envelope — eight fields, byte-locked schema."""
    return {
        "acquired_entity_legal_name": ACQUIRED_ENTITY_LEGAL_NAME,
        "acquired_entity_lei": ACQUIRED_ENTITY_LEI,
        "acquirer_hsm_key_fingerprint": ACQUIRER_HSM_KEY_FINGERPRINT,
        "baseline_manifest_kind": BASELINE_MANIFEST_KIND,
        "baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
        "companion_backfill_seal_run_id": COMPANION_BACKFILL_SEAL_RUN_ID,
        "dual_signatures": DUAL_SIGNATURES,
        "effective_utc": EFFECTIVE_UTC,
    }


def main() -> None:
    envelope = build_successor_attestation_envelope()
    canonical_bytes = jcs.canonicalize(envelope)
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    input_record = {
        "_about": (
            "Input fixture for case 034-successor-attestation — "
            "the §10.39 envelope byte-form pin for an acquirer-target "
            "M&A close where the target operated baseline-diary records. "
            "Composes with case 035-backfill-seal (the cryptographic "
            "complement) via companion_backfill_seal_run_id."
        ),
        "envelope": envelope,
        "synthetic_baseline_manifest": {
            "tuples": _BASELINE_MANIFEST_TUPLES,
            "canonical_byte_length": len(_BASELINE_MANIFEST_BYTES),
            "sha256": BASELINE_MANIFEST_SHA256,
        },
        "synthetic_acquirer_hsm_pubkey_sha256_hex": ACQUIRER_HSM_KEY_FINGERPRINT,
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
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

    print(f"[034] acquired entity:                 {ACQUIRED_ENTITY_LEGAL_NAME}")
    print(f"[034] baseline manifest kind:          {BASELINE_MANIFEST_KIND}")
    print(f"[034] baseline manifest SHA-256:       {BASELINE_MANIFEST_SHA256}")
    print(f"[034] acquirer HSM fingerprint:        {ACQUIRER_HSM_KEY_FINGERPRINT}")
    print(f"[034] envelope canonical len:          {len(canonical_bytes)}")
    print(f"[034] envelope canonical SHA-256:      {canonical_sha256}")


if __name__ == "__main__":
    main()
