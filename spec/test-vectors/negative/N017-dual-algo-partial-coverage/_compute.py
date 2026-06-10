# -*- coding: utf-8 -*-
"""N017-dual-algo-partial-coverage — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: dual-algorithm posture. Seal carries only the ed25519 signature while the institution's declared posture is [ed25519, dilithium3]. PASS-WITH-ANOMALY (control-completeness, regardless of --strict). The Dilithium3 keypair is a v1.x materialization dependency; this fixture pins the posture descriptor + the normative anomaly reason.

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
ABOUT = "DEFERRED-v1.x: dual-algorithm posture. Seal carries only the ed25519 signature while the institution's declared posture is [ed25519, dilithium3]. PASS-WITH-ANOMALY (control-completeness, regardless of --strict). The Dilithium3 keypair is a v1.x materialization dependency; this fixture pins the posture descriptor + the normative anomaly reason."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5, 'rotation': True})
    audit['seal']['declared_algorithm_posture'] = ['ed25519','dilithium3']
    audit['seal']['signatures'] = [{'algorithm':'ed25519','public_key_id':'tenant-ffiec-test-1.ed25519','signature_b64':'TEST-ED25519-PLACEHOLDER'}]
    audit['seal']['_deferred_v1x'] = 'dilithium3 signature not materialized at v1.0'
    tamper = {'class':'dual-algo partial coverage','present':['ed25519'],'declared':['ed25519','dilithium3']}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='PASS-WITH-ANOMALY', step='11', reason="partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture",
        reason_template="partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture",
        exit_code=0, anomaly="partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture",
    )
    print("[N017-dual-algo-partial-coverage] materialized:", 'PASS-WITH-ANOMALY', '11', "partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture")


if __name__ == "__main__":
    main()
