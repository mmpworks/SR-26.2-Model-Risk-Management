# -*- coding: utf-8 -*-
"""N006-key-fingerprint-flipped — auto-generated from negative/_gen_all.py.

Entry seq=2's key_fingerprint flipped to arbitrary 16 bytes; §7 step 8 short-circuits BEFORE any MAC compute — the load-bearing ordering property.

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
ABOUT = "Entry seq=2's key_fingerprint flipped to arbitrary 16 bytes; §7 step 8 short-circuits BEFORE any MAC compute — the load-bearing ordering property."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][1]
    e['key_fingerprint_hex'] = 'ab'*16
    tamper = {'class':'key_fingerprint flipped','seq':2,'new':'ab'*16}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='8', reason="key_fingerprint mismatch at seq 2: looked-up IKM does not match the entry's recorded fingerprint",
        reason_template="key_fingerprint mismatch at seq <N>: looked-up IKM does not match the entry's recorded fingerprint",
        exit_code=1, anomaly=None,
    )
    print("[N006-key-fingerprint-flipped] materialized:", 'FAIL', '8', "key_fingerprint mismatch at seq 2: looked-up IKM does not match the entry's recorded fingerprint")


if __name__ == "__main__":
    main()
