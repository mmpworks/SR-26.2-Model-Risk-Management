# -*- coding: utf-8 -*-
"""N003-merkle-root-altered — auto-generated from negative/_gen_all.py.

The seal's merkle_root is set to garbage; §7 step 10 recomputes the root over the ledger and it does not match the sealed value.

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
ABOUT = "The seal's merkle_root is set to garbage; §7 step 10 recomputes the root over the ledger and it does not match the sealed value."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['seal']['merkle_root_hex'] = '00'*32
    tamper = {'class':'merkle root altered','new':'00'*32}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='10', reason='merkle root mismatch — ledger contents do not produce sealed root',
        reason_template='merkle root mismatch — ledger contents do not produce sealed root',
        exit_code=1, anomaly=None,
    )
    print("[N003-merkle-root-altered] materialized:", 'FAIL', '10', 'merkle root mismatch — ledger contents do not produce sealed root')


if __name__ == "__main__":
    main()
