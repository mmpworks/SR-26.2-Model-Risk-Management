# -*- coding: utf-8 -*-
"""N011-header-genesis-nonzero — auto-generated from negative/_gen_all.py.

Header genesis_hash set to non-zero bytes; §7 step 3 rejects (§4.1 inviolate property 5: seq=1 prev_hash is 32 zero bytes).

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
ABOUT = 'Header genesis_hash set to non-zero bytes; §7 step 3 rejects (§4.1 inviolate property 5: seq=1 prev_hash is 32 zero bytes).'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['header']['genesis_hash_hex'] = '01' + '00'*31
    tamper = {'class':'header genesis nonzero','value':'01'+'00'*31}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='3', reason='header genesis_hash does not match v1 constant',
        reason_template='header genesis_hash does not match v1 constant',
        exit_code=1, anomaly=None,
    )
    print("[N011-header-genesis-nonzero] materialized:", 'FAIL', '3', 'header genesis_hash does not match v1 constant')


if __name__ == "__main__":
    main()
