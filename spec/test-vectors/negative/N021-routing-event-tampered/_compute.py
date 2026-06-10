# -*- coding: utf-8 -*-
"""N021-routing-event-tampered — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x: §4.4.1 routing. A routing attribute (audit.routing.provider_chosen) inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects — proving routing attributes are inside the chain-MAC-covered canonical bytes. Derived from the single baseline seq=2.

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
ABOUT = 'DEFERRED-v1.x: §4.4.1 routing. A routing attribute (audit.routing.provider_chosen) inside the canonical bytes is altered post-capture; §7 step 9 re-MACs and rejects — proving routing attributes are inside the chain-MAC-covered canonical bytes. Derived from the single baseline seq=2.'


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    e = audit['entries'][1]
    e['event']['attributes']['audit.routing.provider_chosen'] = 'tampered-provider-route'
    e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()
    # The stored payload_hash was MAC'd over the original canonical bytes;
    # the §7 step 9 recompute over the tampered routing attribute differs.
    tamper = {'class':'routing event tampered','seq':2,'altered_attr':'audit.routing.provider_chosen'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='9', reason='payload_hash MAC mismatch at seq 2',
        reason_template='payload_hash MAC mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N021-routing-event-tampered] materialized:", 'FAIL', '9', 'payload_hash MAC mismatch at seq 2')


if __name__ == "__main__":
    main()
