# -*- coding: utf-8 -*-
"""N013-mid-write-truncation — auto-generated from negative/_gen_all.py.

The audit file ends mid-line (writer-crash simulation): the NDJSON rendering of the file has its trailing newline removed AND the final event line is truncated mid-serialization. The verifier refuses at file pre-flight BEFORE parsing the header — §10.12 StructuralInputError (exit 2).

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
ABOUT = 'The audit file ends mid-line (writer-crash simulation): the NDJSON rendering of the file has its trailing newline removed AND the final event line is truncated mid-serialization. The verifier refuses at file pre-flight BEFORE parsing the header — §10.12 StructuralInputError (exit 2).'


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    import json as _json
    lines = [_json.dumps(audit['header'], separators=(',',':'))]
    for e in audit['entries']:
        lines.append(_json.dumps(e, separators=(',',':')))
    lines.append(_json.dumps(audit['seal'], separators=(',',':')))
    ndjson = '\n'.join(lines) + '\n'
    # Simulate the crash: drop the trailing newline and chop the last 17 bytes
    truncated = ndjson[:-1][:-17]
    audit['_ndjson_truncated'] = truncated
    audit['_ndjson_full_byte_len'] = len(ndjson.encode('utf-8'))
    audit['_truncated_byte_len'] = len(truncated.encode('utf-8'))
    tamper = {'class':'mid-write truncation','dropped_trailing_newline':True,'chopped_bytes':17}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='pre-flight', reason='audit file ends mid-line — possible mid-write crash',
        reason_template='audit file ends mid-line — possible mid-write crash',
        exit_code=2, anomaly=None,
    )
    print("[N013-mid-write-truncation] materialized:", 'FAIL', 'pre-flight', 'audit file ends mid-line — possible mid-write crash')


if __name__ == "__main__":
    main()
