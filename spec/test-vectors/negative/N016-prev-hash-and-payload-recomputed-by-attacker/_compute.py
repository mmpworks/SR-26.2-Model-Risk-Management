# -*- coding: utf-8 -*-
"""N016-prev-hash-and-payload-recomputed-by-attacker — auto-generated from negative/_gen_all.py.

Attacker substitutes seq=4's prev_hash AND recomputes payload_hash WITHOUT the IKM (using a wrong key); the §7 step 6 structural walk catches the prev_hash substitution, and even if relaxed the MAC step would catch the attacker's MAC.

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
ABOUT = "Attacker substitutes seq=4's prev_hash AND recomputes payload_hash WITHOUT the IKM (using a wrong key); the §7 step 6 structural walk catches the prev_hash substitution, and even if relaxed the MAC step would catch the attacker's MAC."


def main() -> None:
    audit = _lib.clone_baseline(**{'n_events': 5})
    e = audit['entries'][3]
    fake_prev = bytes([0x42])*32
    # Attacker has no IKM; recompute the MAC under a wrong key so the
    # stored payload_hash is internally consistent with fake_prev but
    # not with the verifier's real session key.
    wrong_key = bytes([0x99])*32
    canonical = bytes.fromhex(e['event_canonical_hex'])
    fake_mac = _lib.hmac.new(wrong_key, fake_prev + canonical, _lib.hashlib.sha256).digest()
    e['prev_hash_hex'] = fake_prev.hex(); e['payload_hash_hex'] = fake_mac.hex()
    tamper = {'class':'prev_hash + payload recomputed by attacker','seq':4}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='6', reason='chain link broken at seq 4',
        reason_template='chain link broken at seq <N>',
        exit_code=1, anomaly=None,
    )
    print("[N016-prev-hash-and-payload-recomputed-by-attacker] materialized:", 'FAIL', '6', 'chain link broken at seq 4')


if __name__ == "__main__":
    main()
