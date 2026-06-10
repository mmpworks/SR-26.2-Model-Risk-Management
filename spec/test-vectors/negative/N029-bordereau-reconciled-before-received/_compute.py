# -*- coding: utf-8 -*-
"""N029-bordereau-reconciled-before-received — auto-generated from negative/_gen_all.py.

§10.46 lifecycle: a reconciled event for a bordereau_id has no prior received event from the same party (published → reconciled, skipping received).

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
ABOUT = '§10.46 lifecycle: a reconciled event for a bordereau_id has no prior received event from the same party (published → reconciled, skipping received).'


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'lifecycle out of order','skipped':'received'},'bordereau_id':'polaris-bordereau-2026-05','reconciling_party_identifier':'polaris-reinsurance-bermuda','lifecycle':[{'seq':0,'event':'published'},{'seq':1,'event':'reconciled'}]}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='§7 step 12', reason='bordereau lifecycle out of order at seq 1',
        reason_template='bordereau lifecycle out of order at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N029-bordereau-reconciled-before-received] materialized:", 'FAIL', '§7 step 12', 'bordereau lifecycle out of order at seq 1')


if __name__ == "__main__":
    main()
