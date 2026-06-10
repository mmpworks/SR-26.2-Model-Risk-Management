# -*- coding: utf-8 -*-
"""N038-discovery-production-form — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: §10.13.1 discovery production form. The production packet omits the per-entry canonical-bytes/ artifact; the production-manifest pre-flight refuses. Pins the missing-artifact reason.

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
ABOUT = 'DEFERRED-v1.x: §10.13.1 discovery production form. The production packet omits the per-entry canonical-bytes/ artifact; the production-manifest pre-flight refuses. Pins the missing-artifact reason.'


def main() -> None:
    record = {'_about':ABOUT,'tamper':{'class':'discovery production form missing artifact','missing':'canonical-bytes/'},'production_manifest':{'artifacts_present':['ndjson','verdict-object','seal-records','hsm-pubkey','trust-anchor-manifest'],'artifacts_missing':['canonical-bytes/']}}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='pre-flight', reason='production manifest missing required artifact: canonical-bytes/',
        reason_template='production manifest missing required artifact: <artifact>` OR `production manifest absent — package not chain-of-custody conformant',
        exit_code=1, anomaly=None,
    )
    print("[N038-discovery-production-form] materialized:", 'FAIL', 'pre-flight', 'production manifest missing required artifact: canonical-bytes/')


if __name__ == "__main__":
    main()
