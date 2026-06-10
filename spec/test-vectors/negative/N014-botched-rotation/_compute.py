# -*- coding: utf-8 -*-
"""N014-botched-rotation — auto-generated from negative/_gen_all.py.

key_version=1 re-used for a different IKM (ikm_v2) at seq=4 (same tenant). The entry stamps key_version=1 but its fingerprint is ikm_v2's; §7 step 8 catches the fingerprint mismatch — the load-bearing per-tenant rotation defence.

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
ABOUT = "key_version=1 re-used for a different IKM (ikm_v2) at seq=4 (same tenant). The entry stamps key_version=1 but its fingerprint is ikm_v2's; §7 step 8 catches the fingerprint mismatch — the load-bearing per-tenant rotation defence."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][3]
    # Operator botched rotation: kept key_version=1 but the entry was
    # produced under ikm_v2. The fingerprint is ikm_v2's; key_version is 1.
    fp_v2 = _lib.key_fingerprint(_lib.TENANT_ID, _lib.IKM_V2)
    e['key_fingerprint_hex'] = fp_v2.hex()  # ikm_v2 fingerprint
    e['key_version'] = 1                      # but stamps generation 1
    tamper = {'class':'botched rotation','seq':4,'stamped_key_version':1,'actual_ikm':'v2'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='8', reason='key_fingerprint mismatch at seq 4',
        reason_template='key_fingerprint mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N014-botched-rotation] materialized:", 'FAIL', '8', 'key_fingerprint mismatch at seq 4')


if __name__ == "__main__":
    main()
