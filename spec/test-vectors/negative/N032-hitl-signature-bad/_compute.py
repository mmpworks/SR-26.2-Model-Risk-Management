# -*- coding: utf-8 -*-
"""N032-hitl-signature-bad — auto-generated from negative/_gen_all.py.

§10.50 human-in-the-loop: the HITL reviewer signature on the seq=3 entry fails verification. Derived from the single baseline with a HITL signature attribute injected + corrupted.

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
ABOUT = '§10.50 human-in-the-loop: the HITL reviewer signature on the seq=3 entry fails verification. Derived from the single baseline with a HITL signature attribute injected + corrupted.'


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    e = audit['entries'][2]
    e['hitl_review'] = {'reviewer_id':'analyst-7','signature_b64':'Z'*88,'_note':'corrupted HITL signature'}
    tamper = {'class':'HITL signature bad','seq':3}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 11', reason='HITL reviewer signature verification failed at seq 3',
        reason_template='HITL reviewer signature verification failed at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N032-hitl-signature-bad] materialized:", 'FAIL', '§7 step 11', 'HITL reviewer signature verification failed at seq 3')


if __name__ == "__main__":
    main()
