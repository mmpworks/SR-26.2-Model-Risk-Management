# -*- coding: utf-8 -*-
"""N002-events-reordered — auto-generated from negative/_gen_all.py.

Entries seq=2 and seq=3 swapped in file order without re-chaining; the structural walk at §7 step 6 finds the chain link broken.

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
ABOUT = 'Entries seq=2 and seq=3 swapped in file order without re-chaining; the structural walk at §7 step 6 finds the chain link broken.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['entries'][1], audit['entries'][2] = audit['entries'][2], audit['entries'][1]
    tamper = {'class':'events reordered','swapped':[2,3]}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='6', reason='chain link broken at seq 2',
        reason_template='chain link broken at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N002-events-reordered] materialized:", 'FAIL', '6', 'chain link broken at seq 2')


if __name__ == "__main__":
    main()
