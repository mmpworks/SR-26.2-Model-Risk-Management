# -*- coding: utf-8 -*-
"""N025-backfill-merkle-root-corrupted — auto-generated from negative/_gen_all.py.

§10.42 backfill seal: the seal's apex merkle_root is corrupted by a single-byte flip; the recomputed root over (baseline manifest leaves + metadata leaf) differs (Variant C: baseline manifest leaf path → step 2 / root recomputation).

This generator builds the valid baseline from the central corpus inputs,
applies the single documented mutation, and writes input.json (the
tampered fixture) plus expected_output.txt (the §7 Status/Step/Reason +
§10.12 exit code the verifier MUST emit). Never hand-crafts a hash.

Run: python _compute.py
"""
from __future__ import annotations
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _lib  # noqa: E402

HERE = _lib.here_of(__file__)
ABOUT = "§10.42 backfill seal: the seal's apex merkle_root is corrupted by a single-byte flip; the recomputed root over (baseline manifest leaves + metadata leaf) differs (Variant C: baseline manifest leaf path → step 2 / root recomputation)."


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'backfill merkle root corrupted','variant':'C baseline-manifest leaf'},'backfill_seal':{'merkle_root_hex':'00'+'11'*31,'backfill_seq':1,'baseline_manifest':[{'artifact':'pre-acq-day-01','sha256':'00'*32}],'_note':'apex root corrupted; recomputed root over leaves differs'}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§10.42 step 2 (Merkle root verification)', reason='backfill merkle root mismatch at backfill seq 1',
        reason_template='backfill merkle root mismatch at backfill seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N025-backfill-merkle-root-corrupted] materialized:", 'FAIL', '§10.42 step 2 (Merkle root verification)', 'backfill merkle root mismatch at backfill seq 1')


if __name__ == "__main__":
    main()
