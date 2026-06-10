# -*- coding: utf-8 -*-
"""N026-additional-verifications-invalid-string — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: §10.12 strict-mode post-§7 verdict-output validation. The verdict object's additional_verifications array carries an unknown marker (Variant B: uppercase case-variant of a spec string). Under --strict the verifier rejects with exit code 3 (configuration/strict-mode); the chain itself PASSes §7. This is verifier-OUTPUT validation, not chain integrity.

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
ABOUT = "DEFERRED-v1.x: §10.12 strict-mode post-§7 verdict-output validation. The verdict object's additional_verifications array carries an unknown marker (Variant B: uppercase case-variant of a spec string). Under --strict the verifier rejects with exit code 3 (configuration/strict-mode); the chain itself PASSes §7. This is verifier-OUTPUT validation, not chain integrity."


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'additional_verifications invalid string','variant':'B uppercase case-variant'},'chain_status':'PASS (§7 integrity intact)','verdict_object':{'exit_code':0,'posture':'ffiec','additional_verifications':['BACKFILL_SEAL_VERIFIED'],'_note':'BACKFILL_SEAL_VERIFIED is an uppercase variant of the lowercase spec string; not in the v1.0 closed enumeration'}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§10.12 strict-mode (post-§7)', reason='additional_verifications marker "BACKFILL_SEAL_VERIFIED" not in v1.0 enumeration',
        reason_template='additional_verifications marker "<X>" not in v1.0 enumeration',
        exit_code=3, anomaly=None,
    )
    print("[N026-additional-verifications-invalid-string] materialized:", 'FAIL', '§10.12 strict-mode (post-§7)', 'additional_verifications marker "BACKFILL_SEAL_VERIFIED" not in v1.0 enumeration')


if __name__ == "__main__":
    main()
