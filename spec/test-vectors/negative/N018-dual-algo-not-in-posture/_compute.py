# -*- coding: utf-8 -*-
"""N018-dual-algo-not-in-posture — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: seal carries slh_dsa_shake_128s, not on the declared [ed25519, dilithium3] posture. --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition (the conformance bar) + the normative reason. PQ signatures are a v1.x dependency.

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
ABOUT = 'DEFERRED-v1.x: seal carries slh_dsa_shake_128s, not on the declared [ed25519, dilithium3] posture. --strict: FAIL (exit 1); non-strict: PASS-WITH-ANOMALY. Pins the --strict disposition (the conformance bar) + the normative reason. PQ signatures are a v1.x dependency.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5, 'rotation': True})
    audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']
    audit['seal']['signatures'] = [
        {'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-PLACEHOLDER'},
        {'algorithm':'dilithium3','public_key_id':'tenant-ffiec-test-1.dilithium3','signature_b64':'TEST-DILITHIUM3-PLACEHOLDER'},
        {'algorithm':'slh_dsa_shake_128s','public_key_id':'tenant-ffiec-test-1.slhdsa','signature_b64':'TEST-SLHDSA-PLACEHOLDER'}]
    audit['seal']['_deferred_v1x'] = 'PQ signatures not materialized at v1.0'
    tamper = {'class':'dual-algo not in posture','unexpected':['slh_dsa_shake_128s'],'declared':['ed25519','dilithium3']}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason="algorithm not on institution's declared posture list at seal_date 2026-05-06",
        reason_template="algorithm not on institution's declared posture list at seal_date <date>",
        exit_code=1, anomaly='unknown_algorithms: [slh_dsa_shake_128s]',
    )
    print("[N018-dual-algo-not-in-posture] materialized:", 'FAIL', '11', "algorithm not on institution's declared posture list at seal_date 2026-05-06")


if __name__ == "__main__":
    main()
