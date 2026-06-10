# -*- coding: utf-8 -*-
"""N010-header-hkdf-digest-flipped — auto-generated from negative/_gen_all.py.

Header hkdf_inputs_digest flipped; §7 step 2 recomputes the digest from the §4.1 byte values and it no longer matches.

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
ABOUT = 'Header hkdf_inputs_digest flipped; §7 step 2 recomputes the digest from the §4.1 byte values and it no longer matches.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    d = bytearray.fromhex(audit['header']['hkdf_inputs_digest_hex']); d[0] ^= 0x01
    audit['header']['hkdf_inputs_digest_hex'] = d.hex()
    tamper = {'class':'header hkdf digest flipped','byte_index':0}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='2', reason='header HKDF inputs do not match running v1 inputs',
        reason_template='header HKDF inputs do not match running v1 inputs',
        exit_code=1, anomaly=None,
    )
    print("[N010-header-hkdf-digest-flipped] materialized:", 'FAIL', '2', 'header HKDF inputs do not match running v1 inputs')


if __name__ == "__main__":
    main()
