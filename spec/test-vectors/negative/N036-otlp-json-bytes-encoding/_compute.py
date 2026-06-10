# -*- coding: utf-8 -*-
"""N036-otlp-json-bytes-encoding — auto-generated from negative/_gen_all.py.

DEFERRED-v1.x receiver-decoder hardening: an OTLP/JSON emission encodes payload_hash under padding-stripped base64; the receiver decodes to different bytes and §7 step 9 re-MAC rejects. Derived from the single baseline seq=2; the malformed-encoding marker rides on the entry.

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
ABOUT = 'DEFERRED-v1.x receiver-decoder hardening: an OTLP/JSON emission encodes payload_hash under padding-stripped base64; the receiver decodes to different bytes and §7 step 9 re-MAC rejects. Derived from the single baseline seq=2; the malformed-encoding marker rides on the entry.'


def main() -> None:
    audit = _lib.clone_baseline(n_events=5)
    e = audit['entries'][1]
    import base64 as _b64
    raw = bytes.fromhex(e['payload_hash_hex'])
    good = _b64.b64encode(raw).decode('ascii')
    bad = good.rstrip('=')  # padding-stripped (non-conformant per §4.4)
    e['otlp_json_payload_hash_b64'] = bad
    e['_malformed_encoding'] = 'padding-stripped base64 (§4.4 violation)'
    tamper = {'class':'OTLP/JSON bytes encoding','seq':2,'encoding':'padding-stripped base64'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='9', reason='payload_hash MAC mismatch at seq 2',
        reason_template='payload_hash MAC mismatch at seq <N>` (root cause: §4.4 OTLP/JSON encoding rule violation)',
        exit_code=1, anomaly=None,
    )
    print("[N036-otlp-json-bytes-encoding] materialized:", 'FAIL', '9', 'payload_hash MAC mismatch at seq 2')


if __name__ == "__main__":
    main()
