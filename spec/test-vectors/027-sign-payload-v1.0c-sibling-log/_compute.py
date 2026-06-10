# -*- coding: utf-8 -*-
"""Compute the §4.3 v1.0c 13-line sign_payload byte form for FFIEC v1
test-vector case 027-sign-payload-v1.0c-sibling-log.

Spec §4.3 (v1.0c amendment, normative) extends the v1.0b 12-line form
with one terminal line binding hex(operational_events_log_root) per
§10.79. The operational-events sibling Merkle tree is built under the
RFC 6962 leaf scheme — identical to the captured-event Merkle tree under
§4.2 — over the day's chain_kind = "operational" entries.

This case pins, in two sub-cases:
  (a) the non-empty day — 3 operational events
      (master.reconciliation_completed, verifier.run_completed,
      chain.verification_failure) → a 3-leaf RFC 6962 sibling root;
  (b) the empty day — zero operational events →
      operational_events_log_root = SHA-256(b"") =
      e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
      (spec §10.79 / case 027 description §"Empty-day case").

The byte form and the sibling Merkle construction are fully determined by
the spec. The ONLY piece that depends on the Go runner's fixture-field
convention is the input.json key under which the operational-events log
root is surfaced for the byte-form runner to consume. That key is held as
_OP_EVENTS_ROOT_FIELD below and is marked PENDING — see the status note in
README.md. Until Jared's v1.0c runner convention lands (the
signpayload.go reconstruction reading operational_events_log_root), this
generator is PREPARED-BUT-UNPINNED: running it emits the deterministic
byte form + sibling root, but the expected_* pins are intentionally NOT
committed and the input.json field name is provisional.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# PENDING: the input.json key the Go v1.0c byte-form runner reads for the
# operational-events log root. Jared's wave-3 commit documents the
# convention (likely "operational_events_log_root_hex" on the seal block)
# in E:\dev\ffiec\docs\design\PRD-conformance-sync-2026-06-10.md. Do NOT
# guess — this constant + the input.json write are provisional until that
# convention lands, at which point the pins get committed (see README
# status note).
# ---------------------------------------------------------------------------
_OP_EVENTS_ROOT_FIELD = "operational_events_log_root_hex"  # confirmed: ffiec @ 3a70ebd


# Pinned v1.0c sign_payload inputs — arbitrary post-amendment day per the
# case 027 description.md.
SIGN_PAYLOAD_VERSION = "v1.0c"
ALGORITHM = "ed25519"
FORMAT_VERSION = "v1"
TENANT_ID = "test-tenant-v1.0c"
SEAL_DATE = "2026-05-11"
CADENCE = "daily"
DEV_MODE = False
KEY_VERSIONS_CANON = "1"

# Captured-event Merkle root (§4.2) — synthetic for case 027; the
# per-event MAC chain is pinned in case 010 et al. Case 027 verifies the
# v1.0c byte form + the sibling-log binding, not the captured-event walk.
CAPTURED_EVENT_MERKLE_ROOT_HEX = (
    "11223344556677889900aabbccddeeff11223344556677889900aabbccddeeff"
)
HKDF_INPUTS_DIGEST_HEX = (
    "0a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9"
)
KMS_HANDLE_URIS_DIGEST_HEX = (
    "5d4f1e9c2b8a7f6e3d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d8c9b0a1f2e"
)


# §10.79 operational-events — the day's chain_kind = "operational"
# entries for the non-empty sub-case. Three events per the description:
# a master.reconciliation_completed, a verifier.run_completed, and a
# chain.verification_failure. Each leaf is the JCS-canonical bytes of the
# event under the RFC 6962 leaf scheme.
_OPERATIONAL_EVENTS = [
    {
        "chain_kind": "operational",
        "event_type": "master.reconciliation_completed",
        "seq": 1,
        "tenant_id": TENANT_ID,
        "ts_utc": "2026-05-11T01:00:00Z",
    },
    {
        "chain_kind": "operational",
        "event_type": "verifier.run_completed",
        "seq": 2,
        "tenant_id": TENANT_ID,
        "ts_utc": "2026-05-11T06:30:00Z",
    },
    {
        "chain_kind": "operational",
        "event_type": "chain.verification_failure",
        "seq": 3,
        "tenant_id": TENANT_ID,
        "ts_utc": "2026-05-11T18:45:00Z",
    },
]


# RFC 6962 leaf-hash and inner-hash domain separators (§4.2 / §10.37 /
# §10.79). Same construction as case 035.
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
    """RFC 6962 §2.1 tree hash; empty list → SHA-256(b"") per §10.79."""
    n = len(leaf_payloads)
    if n == 0:
        return hashlib.sha256(b"").digest()
    if n == 1:
        return _leaf_hash(leaf_payloads[0])
    k = _largest_power_of_2_less_than(n)
    left = _merkle_root(leaf_payloads[:k])
    right = _merkle_root(leaf_payloads[k:])
    return _inner_hash(left, right)


def operational_events_log_root_hex(events: list[dict]) -> str:
    """§10.79 sibling Merkle root over the day's operational events."""
    leaf_payloads = [jcs.canonicalize(ev) for ev in events]
    return _merkle_root(leaf_payloads).hex()


def build_sign_payload_v1_0c(operational_events_root_hex: str) -> bytes:
    """§4.3 v1.0c 13-line form. The first twelve lines are byte-identical
    to the v1.0b form except sign_payload_version = "v1.0c"; the terminal
    line binds hex(operational_events_log_root) with NO trailing newline.
    """
    lines = [
        "ffiec.chain-of-custody.v1",
        SIGN_PAYLOAD_VERSION,
        ALGORITHM,
        FORMAT_VERSION,
        TENANT_ID,
        SEAL_DATE,
        CAPTURED_EVENT_MERKLE_ROOT_HEX,
        HKDF_INPUTS_DIGEST_HEX,
        CADENCE,
        "0" if not DEV_MODE else "1",
        KEY_VERSIONS_CANON,
        KMS_HANDLE_URIS_DIGEST_HEX,
        operational_events_root_hex,  # §10.79 terminal line, no trailing \n
    ]
    return ("\n".join(lines)).encode("utf-8")


# Pins are live: the v1.0c runner convention (operational_events_log_root_hex
# on the seal block) is committed in ffiec @ 3a70ebd, matching this generator.
PIN = True


def main() -> None:
    # Sub-case (a): non-empty day, 3 operational events.
    op_root_nonempty = operational_events_log_root_hex(_OPERATIONAL_EVENTS)
    sp_nonempty = build_sign_payload_v1_0c(op_root_nonempty)
    sp_nonempty_sha = hashlib.sha256(sp_nonempty).hexdigest()

    # Sub-case (b): empty day → SHA-256(b"").
    op_root_empty = operational_events_log_root_hex([])
    sp_empty = build_sign_payload_v1_0c(op_root_empty)
    sp_empty_sha = hashlib.sha256(sp_empty).hexdigest()

    print(f"[027] tenant_id:                      {TENANT_ID}")
    print(f"[027] seal_date:                      {SEAL_DATE}")
    print(f"[027] op-events root (3 events):      {op_root_nonempty}")
    print(f"[027] sign_payload len (non-empty):   {len(sp_nonempty)}")
    print(f"[027] sign_payload SHA (non-empty):   {sp_nonempty_sha}")
    print(f"[027] op-events root (empty day):     {op_root_empty}")
    print(f"[027] sign_payload len (empty):       {len(sp_empty)}")
    print(f"[027] sign_payload SHA (empty):       {sp_empty_sha}")
    print(f"[027] op-events root field (input):   {_OP_EVENTS_ROOT_FIELD}")

    if not PIN:
        print(
            "[027] PREPARED-BUT-UNPINNED — pins NOT written. Flip PIN=True "
            "in the commit that confirms _OP_EVENTS_ROOT_FIELD against "
            "Jared's v1.0c runner convention."
        )
        return

    # --- pin write path (enabled only when PIN is True) ---
    # Non-empty case is the primary pin; the empty-day case is surfaced
    # in input.json's sub-case block for the runner's empty-day check.
    input_record = {
        "_about": (
            "Input fixture for case 027-sign-payload-v1.0c-sibling-log — "
            "the §4.3 v1.0c 13-line sign_payload byte form binding "
            "hex(operational_events_log_root) per §10.79. Sub-case (a) is "
            "the non-empty day (3 operational events → 3-leaf RFC 6962 "
            "sibling root); sub-case (b) is the empty day "
            "(operational_events_log_root = SHA-256(b''))."
        ),
        "seal": {
            "sign_payload_version": SIGN_PAYLOAD_VERSION,
            "algorithm": ALGORITHM,
            "format_version": FORMAT_VERSION,
            "tenant_id": TENANT_ID,
            "seal_date": SEAL_DATE,
            "merkle_root_hex": CAPTURED_EVENT_MERKLE_ROOT_HEX,
            "hkdf_inputs_digest_hex": HKDF_INPUTS_DIGEST_HEX,
            "cadence": CADENCE,
            "dev_mode": DEV_MODE,
            _OP_EVENTS_ROOT_FIELD: op_root_nonempty,
        },
        "computed_canonical_fields": {
            "key_versions_canon": KEY_VERSIONS_CANON,
            "kms_handle_uris_digest_hex": KMS_HANDLE_URIS_DIGEST_HEX,
        },
        "operational_events": _OPERATIONAL_EVENTS,
        "empty_day_subcase": {
            _OP_EVENTS_ROOT_FIELD: op_root_empty,
            "sign_payload_sha256": sp_empty_sha,
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(HERE, "expected_sign_payload.txt"), "wb") as f:
        f.write(sp_nonempty)

    with open(
        os.path.join(HERE, "expected_sign_payload_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(sp_nonempty_sha + "\n")


if __name__ == "__main__":
    main()
