# -*- coding: utf-8 -*-
"""N020-algorithm-key-type-mismatch — auto-generated from negative/_gen_all.py.

Seal claims algorithm ed25519 but the resolved public key for public_key_id is RSA-3072; §7 step 11 reports the specific algorithm/key-type mismatch, NOT the generic signature-verification-failed.

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
ABOUT = 'Seal claims algorithm ed25519 but the resolved public key for public_key_id is RSA-3072; §7 step 11 reports the specific algorithm/key-type mismatch, NOT the generic signature-verification-failed.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 1})
    audit['seal']['public_key_id'] = 'tenant-ffiec-test-1.rsa-3072-misconfigured'
    audit['seal']['resolved_public_key_type'] = 'rsa-3072'
    tamper = {'class':'algorithm/key-type mismatch','seal_algorithm':'ed25519','resolved_key_type':'rsa-3072'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason='algorithm/key-type mismatch at signature verification',
        reason_template='algorithm/key-type mismatch at signature verification',
        exit_code=1, anomaly=None,
    )
    print("[N020-algorithm-key-type-mismatch] materialized:", 'FAIL', '11', 'algorithm/key-type mismatch at signature verification')


if __name__ == "__main__":
    main()
