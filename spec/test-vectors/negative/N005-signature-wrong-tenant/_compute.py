# -*- coding: utf-8 -*-
"""N005-signature-wrong-tenant — auto-generated from negative/_gen_all.py.

The seal is signed for a different tenant_id; tenant_id is bound into sign_payload, so §7 step 11 signature verification fails.

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
ABOUT = 'The seal is signed for a different tenant_id; tenant_id is bound into sign_payload, so §7 step 11 signature verification fails.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    wrong = 'tenant-ffiec-test-OTHER'
    sp = _lib.build_sign_payload_v1_0a(algorithm=_lib.ALGORITHM, format_version=_lib.FORMAT_VERSION,
        tenant_id=wrong, seal_date=audit['seal']['seal_date'],
        merkle_root_hex=audit['seal']['merkle_root_hex'], hkdf_inputs_digest_hex=audit['seal']['hkdf_inputs_digest_hex'])
    audit['seal']['sign_payload_hex'] = sp.hex(); audit['seal']['sign_payload_text'] = sp.decode('utf-8')
    audit['seal']['signed_for_tenant_id'] = wrong
    tamper = {'class':'signature wrong tenant','signed_for':wrong}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason='signature verification failed',
        reason_template='signature verification failed',
        exit_code=1, anomaly=None,
    )
    print("[N005-signature-wrong-tenant] materialized:", 'FAIL', '11', 'signature verification failed')


if __name__ == "__main__":
    main()
