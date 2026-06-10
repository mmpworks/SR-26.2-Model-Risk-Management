# -*- coding: utf-8 -*-
"""N007-unknown-key-version — auto-generated from negative/_gen_all.py.

Entry seq=4's key_version set to 99 (not in the test IKM registry); §7 step 7 rejects with no MAC compute.

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
ABOUT = "Entry seq=4's key_version set to 99 (not in the test IKM registry); §7 step 7 rejects with no MAC compute."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][3]
    e['key_version'] = 99
    tamper = {'class':'unknown key_version','seq':4,'key_version':99}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='7', reason='unknown key_version: no IKM for (tenant=tenant-ffiec-test-1, key_version=99) at seq 4',
        reason_template='unknown key_version: no IKM for (tenant=<T>, key_version=<V>) at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N007-unknown-key-version] materialized:", 'FAIL', '7', 'unknown key_version: no IKM for (tenant=tenant-ffiec-test-1, key_version=99) at seq 4')


if __name__ == "__main__":
    main()
