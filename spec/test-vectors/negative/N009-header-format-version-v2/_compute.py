# -*- coding: utf-8 -*-
"""N009-header-format-version-v2 — auto-generated from negative/_gen_all.py.

Header format_version set to v2; §7 step 1 pre-flight rejects. Per §10.12, a step-1 value rejection still reached §7 so the exit code is Fail (1), not StructuralInputError.

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
ABOUT = 'Header format_version set to v2; §7 step 1 pre-flight rejects. Per §10.12, a step-1 value rejection still reached §7 so the exit code is Fail (1), not StructuralInputError.'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    audit['header']['format_version'] = 'v2'
    tamper = {'class':'header format_version','value':'v2'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='1', reason='format_version v2 not supported by this verifier (running v1)',
        reason_template='format_version v2 not supported by this verifier (running v1)',
        exit_code=1, anomaly=None,
    )
    print("[N009-header-format-version-v2] materialized:", 'FAIL', '1', 'format_version v2 not supported by this verifier (running v1)')


if __name__ == "__main__":
    main()
