# -*- coding: utf-8 -*-
"""N031-retrieval-merkle-tampered — auto-generated from negative/_gen_all.py.

§10.49 retrieval-set Merkle: the retrieval-set Merkle root bound into the entry is tampered; recomputation over the retrieval set does not match.

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
ABOUT = '§10.49 retrieval-set Merkle: the retrieval-set Merkle root bound into the entry is tampered; recomputation over the retrieval set does not match.'


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'retrieval merkle tampered'},'retrieval_set_merkle_root_hex':'00'+'22'*31,'retrieval_set':[{'doc_id':'kb-001','sha256':'aa'*32},{'doc_id':'kb-002','sha256':'bb'*32}]}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 11', reason='retrieval set Merkle root mismatch',
        reason_template='retrieval set Merkle root mismatch',
        exit_code=1, anomaly=None,
    )
    print("[N031-retrieval-merkle-tampered] materialized:", 'FAIL', '§7 step 11', 'retrieval set Merkle root mismatch')


if __name__ == "__main__":
    main()
