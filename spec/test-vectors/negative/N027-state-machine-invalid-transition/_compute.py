# -*- coding: utf-8 -*-
"""N027-state-machine-invalid-transition — auto-generated from negative/_gen_all.py.

§10.43 / §1.5 state machine: a closed → opened transition (no transition out of a terminal state). The validator rejects at index 0.

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
ABOUT = '§10.43 / §1.5 state machine: a closed → opened transition (no transition out of a terminal state). The validator rejects at index 0.'


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'illegal state transition'},'transitions_table':{'opened':['pending','closed'],'pending':['decided','closed'],'decided':['closed'],'closed':[]},'walk':[{'from_state':'closed','to_state':'opened'}]}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 12', reason='state-machine illegal transition at seq 0: closed → opened',
        reason_template='state-machine illegal transition at seq <N>: <from> → <to>',
        exit_code=1, anomaly=None,
    )
    print("[N027-state-machine-invalid-transition] materialized:", 'FAIL', '§7 step 12', 'state-machine illegal transition at seq 0: closed → opened')


if __name__ == "__main__":
    main()
