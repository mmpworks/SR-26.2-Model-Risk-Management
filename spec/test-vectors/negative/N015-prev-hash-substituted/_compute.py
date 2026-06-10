# -*- coding: utf-8 -*-
"""N015-prev-hash-substituted — auto-generated from negative/_gen_all.py.

Entry seq=4's prev_hash substituted, payload_hash left alone; the §7 step 6 structural walk catches the broken link before the MAC step.

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
ABOUT = "Entry seq=4's prev_hash substituted, payload_hash left alone; the §7 step 6 structural walk catches the broken link before the MAC step."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][3]
    ph = bytearray.fromhex(e['prev_hash_hex']); ph[0] ^= 0x01
    e['prev_hash_hex'] = ph.hex()
    tamper = {'class':'prev_hash substituted','seq':4,'byte_index':0}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='6', reason='chain link broken at seq 4',
        reason_template='chain link broken at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N015-prev-hash-substituted] materialized:", 'FAIL', '6', 'chain link broken at seq 4')


if __name__ == "__main__":
    main()
