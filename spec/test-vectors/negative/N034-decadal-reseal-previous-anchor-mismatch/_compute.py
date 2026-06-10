# -*- coding: utf-8 -*-
"""N034-decadal-reseal-previous-anchor-mismatch — auto-generated from negative/_gen_all.py.

§10.54 decadal re-sealing: the decadal re-seal's previous-anchor reference does not match the prior decade's seal apex; §7 step 11 rejects.

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
ABOUT = "§10.54 decadal re-sealing: the decadal re-seal's previous-anchor reference does not match the prior decade's seal apex; §7 step 11 rejects."


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'decadal reseal previous-anchor mismatch'},'decadal_reseal':{'seal_date':'2036-05-06','previous_anchor_hex':'00'+'33'*31,'actual_prior_decade_apex_hex':'cc'*32,'_note':'previous_anchor does not match prior decade apex'}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 11', reason='decadal re-seal previous-anchor mismatch at seal_date 2036-05-06',
        reason_template='decadal re-seal previous-anchor mismatch at seal_date <date>',
        exit_code=1, anomaly=None,
    )
    print("[N034-decadal-reseal-previous-anchor-mismatch] materialized:", 'FAIL', '§7 step 11', 'decadal re-seal previous-anchor mismatch at seal_date 2036-05-06')


if __name__ == "__main__":
    main()
