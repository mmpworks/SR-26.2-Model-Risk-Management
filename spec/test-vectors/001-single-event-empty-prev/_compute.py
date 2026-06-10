# -*- coding: utf-8 -*-
"""Materialize case 001 — single event, empty prev_hash.

The smallest case: one event with seq=1, prev_hash = 32 zero bytes. The
conformance artifact this pins is the JCS-canonical event bytes for the
seq=1 event (the bytes the per-event MAC covers). The canonical-output
gate re-canonicalizes them through the Go / .NET / Python JCS
implementations and asserts byte-identity, proving the canonicalizers
agree on the foundational single-event shape.

The per-event MAC chain values (payload_hash, prev_hash) and the
hkdf_inputs_digest are pinned in input.json for cross-implementation
checks; they are reproduced from the central chain_vectors.json via the
shared spec primitives, never hand-crafted.

Run: python _compute.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "negative"))
import _lib  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    baseline = _lib.build_baseline(n_events=1)
    entry = baseline["entries"][0]
    canonical = bytes.fromhex(entry["event_canonical_hex"])

    # expected_canonical.txt — the JCS-canonical event bytes verbatim
    # (no trailing newline; a single JSON document).
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(canonical)

    canonical_sha = hashlib.sha256(canonical).hexdigest()
    with open(os.path.join(HERE, "expected_canonical_sha256.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(canonical_sha + "\n")

    record = {
        "_about": (
            "Input fixture for case 001-single-event-empty-prev. The seq=1 "
            "event uses prev_hash = 32 zero bytes (§4.1 inviolate property 5). "
            "expected_canonical.txt pins the JCS-canonical event bytes; the "
            "MAC chain values below are reproduced from chain_vectors.json via "
            "the shared spec primitives."
        ),
        "inputs": {
            "tenant_id": _lib.TENANT_ID,
            "run_id": _lib.RUN_ID,
            "seal_date": _lib.SEAL_DATE,
            "ikm_v1_hex": _lib.IKM_V1_HEX,
        },
        "expected": {
            "session_key_v1_hex": _lib.session_key(_lib.IKM_V1, _lib.TENANT_ID).hex(),
            "key_fingerprint_v1_hex": entry["key_fingerprint_hex"],
            "hkdf_inputs_digest_hex": baseline["header"]["hkdf_inputs_digest_hex"],
            "seq1_prev_hash_hex": entry["prev_hash_hex"],
            "seq1_payload_hash_hex": entry["payload_hash_hex"],
        },
        "event_canonical_bytes_utf8": canonical.decode("utf-8"),
        "event_canonical_sha256": canonical_sha,
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[001] canonical bytes len:", len(canonical))
    print("[001] canonical sha256:   ", canonical_sha)
    print("[001] seq1 payload_hash:  ", entry["payload_hash_hex"])
    assert entry["prev_hash_hex"] == "00" * 32, "seq=1 prev_hash must be 32 zero bytes"
    assert entry["payload_hash_hex"] == "e84168071562a9e866f28977a204b43abfdc959b7f84aad83c16fe790f63b049"


if __name__ == "__main__":
    main()
