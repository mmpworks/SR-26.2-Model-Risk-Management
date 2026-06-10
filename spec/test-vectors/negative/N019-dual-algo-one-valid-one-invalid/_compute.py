# -*- coding: utf-8 -*-
"""N019-dual-algo-one-valid-one-invalid — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: co-signed seal, ed25519 validates, dilithium3 does not (one byte flipped). --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition + the normative co-signed-failure reason. PQ signatures are a v1.x dependency.

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
ABOUT = 'DEFERRED-v1.x: co-signed seal, ed25519 validates, dilithium3 does not (one byte flipped). --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition + the normative co-signed-failure reason. PQ signatures are a v1.x dependency.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5, 'rotation': True})
    audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']
    audit['seal']['signatures'] = [
        {'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-VALID-PLACEHOLDER'},
        {'algorithm':'dilithium3','public_key_id':'tenant-ffiec-test-1.dilithium3','signature_b64':'TEST-DILITHIUM3-INVALID-PLACEHOLDER'}]
    audit['seal']['per_algorithm_results'] = {'ed25519':'PASS','dilithium3':'FAIL'}
    audit['seal']['_deferred_v1x'] = 'PQ signatures not materialized at v1.0'
    tamper = {'class':'dual-algo one valid one invalid','valid':'ed25519','invalid':'dilithium3'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason='co-signed seal failure: algorithm ed25519 validated, algorithm dilithium3 did not',
        reason_template='co-signed seal failure: algorithm <A> validated, algorithm <B> did not',
        exit_code=1, anomaly=None,
    )
    print("[N019-dual-algo-one-valid-one-invalid] materialized:", 'FAIL', '11', 'co-signed seal failure: algorithm ed25519 validated, algorithm dilithium3 did not')


if __name__ == "__main__":
    main()
