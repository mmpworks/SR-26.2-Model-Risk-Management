# -*- coding: utf-8 -*-
"""Materialize case 010 — tenant IKM rotation mid-day.

The same tenant's IKM rotates from key_version=1 (ikm_v1) to key_version=2
(ikm_v2) mid-run. Events 1-3 under v1; events 4-5 under v2. The
conformance artifact this pins is the five JCS-canonical event documents
(NDJSON), so the canonical-output gate proves the canonicalizers agree on
the rotation chain's event shapes. The per-half key_fingerprint values,
the chain-link property, and the daily Merkle root are pinned in
input.json, reproduced from chain_vectors.json via the shared primitives.

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
    baseline = _lib.build_baseline(n_events=5, rotation=True)
    entries = baseline["entries"]

    canonical_lines = [bytes.fromhex(e["event_canonical_hex"]) for e in entries]
    blob = b"\n".join(canonical_lines)
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(blob)

    blob_sha = hashlib.sha256(blob).hexdigest()
    sha_lines = [f"full_blob {blob_sha}"]
    for e in entries:
        per = hashlib.sha256(bytes.fromhex(e["event_canonical_hex"])).hexdigest()
        sha_lines.append(f"event_seq_{e['seq']}_kv{e['key_version']} {per}")
    with open(os.path.join(HERE, "expected_canonical_sha256.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sha_lines) + "\n")

    # The rotation boundary: seq 1-3 are key_version=1, seq 4-5 key_version=2.
    assert [e["key_version"] for e in entries] == [1, 1, 1, 2, 2]
    fp_v1 = _lib.key_fingerprint(_lib.TENANT_ID, _lib.IKM_V1).hex()
    fp_v2 = _lib.key_fingerprint(_lib.TENANT_ID, _lib.IKM_V2).hex()
    for e in entries:
        want = fp_v1 if e["key_version"] == 1 else fp_v2
        assert e["key_fingerprint_hex"] == want, f"fingerprint wrong at seq {e['seq']}"

    record = {
        "_about": (
            "Input fixture for case 010-tenant-ikm-rotation-mid-day. Events 1-3 "
            "under key_version=1 (ikm_v1); events 4-5 under key_version=2 "
            "(ikm_v2). expected_canonical.txt is NDJSON: one JCS-canonical event "
            "document per line. Fingerprints, chain links, Merkle root, and the "
            "seal's key_versions list are reproduced from chain_vectors.json via "
            "the shared spec primitives."
        ),
        "inputs": {
            "tenant_id": _lib.TENANT_ID,
            "run_id": _lib.RUN_ID,
            "seal_date": _lib.SEAL_DATE,
            "ikm_v1_hex": _lib.IKM_V1_HEX,
            "ikm_v2_hex": _lib.IKM_V2_HEX,
        },
        "expected": {
            "key_fingerprint_v1_hex": fp_v1,
            "key_fingerprint_v2_hex": fp_v2,
            "chain": [
                {
                    "seq": e["seq"],
                    "key_version": e["key_version"],
                    "key_fingerprint_hex": e["key_fingerprint_hex"],
                    "prev_hash_hex": e["prev_hash_hex"],
                    "payload_hash_hex": e["payload_hash_hex"],
                }
                for e in entries
            ],
            "merkle_root_rotation_hex": baseline["seal"]["merkle_root_hex"],
            "seal_key_versions": baseline["seal"]["key_versions"],
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[010] full_blob sha256:", blob_sha)
    print("[010] merkle_root_rotation:", baseline["seal"]["merkle_root_hex"])
    print("[010] key_versions:", baseline["seal"]["key_versions"])
    assert baseline["seal"]["merkle_root_hex"] == "88b968e7c106fb2dfe0d74825ec1442af5a7236d78e54d420d394c8166ade871"


if __name__ == "__main__":
    main()
