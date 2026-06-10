# -*- coding: utf-8 -*-
"""N008-entry-format-version-mismatch — auto-generated from negative/_gen_all.py.

Entry seq=2's format_version set to v2; §7 step 5 rejects the per-entry format mismatch.

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
ABOUT = "Entry seq=2's format_version set to v2; §7 step 5 rejects the per-entry format mismatch."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['entries'][1]['format_version'] = 'v2'
    tamper = {'class':'entry format_version mismatch','seq':2,'value':'v2'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='5', reason='format_version mismatch at seq 2',
        reason_template='format_version mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N008-entry-format-version-mismatch] materialized:", 'FAIL', '5', 'format_version mismatch at seq 2')


if __name__ == "__main__":
    main()
