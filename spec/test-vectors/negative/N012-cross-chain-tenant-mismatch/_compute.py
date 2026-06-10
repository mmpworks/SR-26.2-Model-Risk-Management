# -*- coding: utf-8 -*-
"""N012-cross-chain-tenant-mismatch — auto-generated from negative/_gen_all.py.

Entry seq=3's event.tenant_id differs from the header's; §7 step 4 detects a cross-chain lift.

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
ABOUT = "Entry seq=3's event.tenant_id differs from the header's; §7 step 4 detects a cross-chain lift."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][2]
    e['event']['tenant_id'] = 'tenant-ffiec-test-OTHER'
    e['event_canonical_hex'] = _lib.jcs_canonicalize(e['event']).hex()
    tamper = {'class':'cross-chain tenant mismatch','seq':3,'event_tenant':'tenant-ffiec-test-OTHER'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='4', reason='cross-chain lift detected at seq 3 (event.tenant_id mismatch)',
        reason_template='cross-chain lift detected at seq <N> (event.tenant_id mismatch)',
        exit_code=1, anomaly=None,
    )
    print("[N012-cross-chain-tenant-mismatch] materialized:", 'FAIL', '4', 'cross-chain lift detected at seq 3 (event.tenant_id mismatch)')


if __name__ == "__main__":
    main()
