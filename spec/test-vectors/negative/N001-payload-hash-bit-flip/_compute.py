# -*- coding: utf-8 -*-
"""N001-payload-hash-bit-flip — auto-generated from negative/_gen_all.py.

One byte of seq=3's payload_hash flipped post-capture; §7 step 9 recomputes the real MAC and rejects the stored value.

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
ABOUT = "One byte of seq=3's payload_hash flipped post-capture; §7 step 9 recomputes the real MAC and rejects the stored value."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][2]
    ph = bytearray.fromhex(e['payload_hash_hex']); ph[0] ^= 0x01
    e['payload_hash_hex'] = ph.hex()
    tamper = {'class':'payload_hash bit-flip','seq':3,'byte_index':0,'xor':'0x01'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='9', reason='payload_hash MAC mismatch at seq 3',
        reason_template='payload_hash MAC mismatch at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N001-payload-hash-bit-flip] materialized:", 'FAIL', '9', 'payload_hash MAC mismatch at seq 3')


if __name__ == "__main__":
    main()
