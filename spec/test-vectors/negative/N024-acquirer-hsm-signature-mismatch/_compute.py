# -*- coding: utf-8 -*-
"""N024-acquirer-hsm-signature-mismatch — auto-generated from negative/_gen_all.py.

§10.39 successor-attestation: the envelope's declared acquirer_hsm_key_fingerprint does not match the key under which the to-entity dual_signatures entry actually verifies (Variant A: declared-fingerprint corruption).

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
ABOUT = "§10.39 successor-attestation: the envelope's declared acquirer_hsm_key_fingerprint does not match the key under which the to-entity dual_signatures entry actually verifies (Variant A: declared-fingerprint corruption)."


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'acquirer-HSM fingerprint mismatch','variant':'A declared-fingerprint corruption'},'successor_envelope':{'acquirer_hsm_key_fingerprint':'00'+'ff'*31,'dual_signatures':[{'role':'from_entity','signature_b64':'TEST-FROM-PLACEHOLDER'},{'role':'to_entity','signature_b64':'TEST-TO-PLACEHOLDER-verifies-under-real-key'}],'_note':'to_entity signature verifies under the real key; declared fingerprint points elsewhere'}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§10.39 acquirer_hsm_key_fingerprint cross-binding to dual_signatures', reason='acquirer-HSM signature verification failed at successor anchor',
        reason_template='acquirer-HSM signature verification failed at successor anchor',
        exit_code=1, anomaly=None,
    )
    print("[N024-acquirer-hsm-signature-mismatch] materialized:", 'FAIL', '§10.39 acquirer_hsm_key_fingerprint cross-binding to dual_signatures', 'acquirer-HSM signature verification failed at successor anchor')


if __name__ == "__main__":
    main()
