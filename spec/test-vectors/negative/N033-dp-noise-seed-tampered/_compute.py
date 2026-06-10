# -*- coding: utf-8 -*-
"""N033-dp-noise-seed-tampered — auto-generated from negative/_gen_all.py.

§10.51 differential-privacy overlay: the DP noise seed inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2.

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
ABOUT = '§10.51 differential-privacy overlay: the DP noise seed inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2.'


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    e = audit['entries'][1]
    e['event']['attributes']['dp_noise_seed'] = 'tampered-seed-value'
    e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()
    tamper = {'class':'DP noise seed tampered','seq':2}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='9', reason='payload_hash MAC mismatch at seq 2',
        reason_template='payload_hash MAC mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N033-dp-noise-seed-tampered] materialized:", 'FAIL', '9', 'payload_hash MAC mismatch at seq 2')


if __name__ == "__main__":
    main()
