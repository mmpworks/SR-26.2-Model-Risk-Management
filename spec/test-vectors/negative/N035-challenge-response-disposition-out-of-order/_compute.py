# -*- coding: utf-8 -*-
"""N035-challenge-response-disposition-out-of-order — auto-generated from negative/_gen_all.py.

§10.55 audit-target challenge-response: a disposition event precedes its challenge (out of order). §7 step 12 lifecycle check rejects.

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
ABOUT = '§10.55 audit-target challenge-response: a disposition event precedes its challenge (out of order). §7 step 12 lifecycle check rejects.'


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'challenge-response out of order'},'sequence':[{'seq':0,'event':'disposition'},{'seq':1,'event':'challenge'}]}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 12', reason='challenge-response disposition out of order at seq 0',
        reason_template='challenge-response disposition out of order at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N035-challenge-response-disposition-out-of-order] materialized:", 'FAIL', '§7 step 12', 'challenge-response disposition out of order at seq 0')


if __name__ == "__main__":
    main()
