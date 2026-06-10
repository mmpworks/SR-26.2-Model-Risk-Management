# -*- coding: utf-8 -*-
"""N004-signature-garbage — auto-generated from negative/_gen_all.py.

The seal's signature is replaced with garbage bytes; §7 step 11 signature verification fails.

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
ABOUT = "The seal's signature is replaced with garbage bytes; §7 step 11 signature verification fails."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['seal']['signature_b64'] = 'Z' * 88
    tamper = {'class':'signature garbage'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason='signature verification failed',
        reason_template='signature verification failed',
        exit_code=1, anomaly=None,
    )
    print("[N004-signature-garbage] materialized:", 'FAIL', '11', 'signature verification failed')


if __name__ == "__main__":
    main()
