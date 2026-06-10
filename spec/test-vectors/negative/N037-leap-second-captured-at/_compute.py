# -*- coding: utf-8 -*-
"""N037-leap-second-captured-at — auto-generated from negative/_gen_all.py.

§10.4 leap-second: two adjacent entries' captured_at straddle a leap second (23:59:60Z then 23:59:60.5Z). A CONFORMANT verifier emits PASS with a clock-skew anomaly (ordering preserved by seq), NOT a chain-link-broken FAIL. This vector pins the conformant PASS disposition; the non-conformant reaction is the false-positive it guards against.

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
ABOUT = "§10.4 leap-second: two adjacent entries' captured_at straddle a leap second (23:59:60Z then 23:59:60.5Z). A CONFORMANT verifier emits PASS with a clock-skew anomaly (ordering preserved by seq), NOT a chain-link-broken FAIL. This vector pins the conformant PASS disposition; the non-conformant reaction is the false-positive it guards against."


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    audit['entries'][0]['event']['captured_at'] = '2026-12-31T23:59:60Z'
    audit['entries'][1]['event']['captured_at'] = '2026-12-31T23:59:60.5Z'
    # captured_at is provenance-only (NOT in the canonical MAC bytes), so
    # adding it does not change payload_hash; ordering stays seq-driven.
    tamper = {'class':'leap-second captured_at','conformant_disposition':'PASS with anomaly'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='PASS', step='', reason='clock-skew anomaly at seq 2: captured_at non-monotonic across leap-second boundary; ordering preserved by seq',
        reason_template='conformant verifier emits Status: PASS with `clock-skew anomaly at seq <N>: captured_at non-monotonic across leap-second boundary; ordering preserved by seq',
        exit_code=0, anomaly='clock-skew anomaly at seq 2: captured_at non-monotonic across leap-second boundary; ordering preserved by seq',
    )
    print("[N037-leap-second-captured-at] materialized:", 'PASS', '', 'clock-skew anomaly at seq 2: captured_at non-monotonic across leap-second boundary; ordering preserved by seq')


if __name__ == "__main__":
    main()
