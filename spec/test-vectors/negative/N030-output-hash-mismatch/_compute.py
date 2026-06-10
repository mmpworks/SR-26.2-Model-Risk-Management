# -*- coding: utf-8 -*-
"""N030-output-hash-mismatch — auto-generated from negative/_gen_all.py.

§10.49 generative-AI output binding: a routing/output attribute inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2 with one attribute mutated.

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
ABOUT = '§10.49 generative-AI output binding: a routing/output attribute inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects. Derived from the single baseline seq=2 with one attribute mutated.'


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    e = audit['entries'][1]
    e['event']['attributes']['ai_output_grounding'] = 'tampered-output-claim'
    e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()
    # §7 step 9 recomputes the MAC over the new canonical bytes; the stored
    # payload_hash (over the original bytes) no longer matches.
    tamper = {'class':'output hash mismatch','seq':2,'altered_attr':'ai_output_grounding'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='9', reason='payload_hash MAC mismatch at seq 2',
        reason_template='payload_hash MAC mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N030-output-hash-mismatch] materialized:", 'FAIL', '9', 'payload_hash MAC mismatch at seq 2')


if __name__ == "__main__":
    main()
