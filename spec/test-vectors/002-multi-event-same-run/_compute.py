# -*- coding: utf-8 -*-
"""Materialize case 002 — multi-event, same run.

Five events in one run under key_version=1. The conformance artifact this
pins is the five JCS-canonical event documents, one per line (NDJSON), so
the canonical-output gate re-canonicalizes each line through the Go /
.NET / Python JCS implementations and asserts byte-identity. The chain
link property (prev_hash of entry N+1 == payload_hash of entry N) and the
RFC 6962 Merkle root are pinned in input.json, reproduced from
chain_vectors.json via the shared spec primitives.

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
    baseline = _lib.build_baseline(n_events=5)
    entries = baseline["entries"]

    # NDJSON: one JCS-canonical event document per line, no trailing
    # newline on the terminal line (the gate's splitNDJSON tolerates a
    # trailing newline as framing either way; we omit it for a clean pin).
    canonical_lines = [bytes.fromhex(e["event_canonical_hex"]) for e in entries]
    blob = b"\n".join(canonical_lines)
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(blob)

    blob_sha = hashlib.sha256(blob).hexdigest()
    # Multi-payload convention: first line is full_blob, then one per event.
    sha_lines = [f"full_blob {blob_sha}"]
    for e in entries:
        per = hashlib.sha256(bytes.fromhex(e["event_canonical_hex"])).hexdigest()
        sha_lines.append(f"event_seq_{e['seq']} {per}")
    with open(os.path.join(HERE, "expected_canonical_sha256.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sha_lines) + "\n")

    # Chain-link self-check: prev_hash[N+1] == payload_hash[N].
    for i in range(1, len(entries)):
        assert entries[i]["prev_hash_hex"] == entries[i - 1]["payload_hash_hex"], \
            f"chain link broken at seq {entries[i]['seq']}"

    record = {
        "_about": (
            "Input fixture for case 002-multi-event-same-run. Five events, one "
            "run, key_version=1. expected_canonical.txt is NDJSON: one "
            "JCS-canonical event document per line. The chain-link and Merkle "
            "values are reproduced from chain_vectors.json via the shared spec "
            "primitives."
        ),
        "inputs": {
            "tenant_id": _lib.TENANT_ID,
            "run_id": _lib.RUN_ID,
            "seal_date": _lib.SEAL_DATE,
            "ikm_v1_hex": _lib.IKM_V1_HEX,
        },
        "expected": {
            "chain": [
                {
                    "seq": e["seq"],
                    "prev_hash_hex": e["prev_hash_hex"],
                    "payload_hash_hex": e["payload_hash_hex"],
                }
                for e in entries
            ],
            "merkle_root_single_hex": baseline["seal"]["merkle_root_hex"],
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("[002] events:", len(entries))
    print("[002] full_blob sha256:", blob_sha)
    print("[002] merkle_root_single:", baseline["seal"]["merkle_root_hex"])
    assert baseline["seal"]["merkle_root_hex"] == "927adc88e5d843c5847674f7245d1e3c762bacc3f0b225f3322300cddf4eefe9"


if __name__ == "__main__":
    main()
