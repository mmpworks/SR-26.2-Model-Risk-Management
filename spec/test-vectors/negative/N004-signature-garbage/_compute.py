# -*- coding: utf-8 -*-
"""N004-signature-garbage — auto-generated from negative/_gen_all.py.

The seal's signature is replaced with garbage bytes; §7 step 11 signature verification fails.

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
ABOUT = (
    "Real Ed25519-signed baseline (test key), then the seal's signature is "
    "replaced with garbage bytes; §7 step 11 signature verification fails. "
    "Steps 1-10 pass; the reconstruct-and-compare assertion passes (the "
    "structured fields and sign_payload_hex are untouched); the Ed25519 "
    "verify fails because the signature bytes are garbage."
)


def main() -> None:
    # Sign the baseline with the real test key (fail-loud if the key dir is
    # absent), then apply the single documented mutation: garbage signature.
    priv = _lib.load_test_signing_key()
    audit = _lib.clone_baseline(**{'n_events': 5})
    _lib.sign_seal_in_place(audit, priv)
    # 64 bytes of 0xFF, base64-std — decodes to a full-length but invalid
    # Ed25519 signature, so the verify call is reached and fails (vs a
    # malformed length that would short-circuit). The reconstruct-and-compare
    # assertion still passes because sign_payload_hex is left intact.
    import base64
    audit['seal']['signature_b64'] = base64.b64encode(b'\xff' * 64).decode('ascii')
    tamper = {'class':'signature garbage'}
    record = {'_about': ABOUT, 'tamper': tamper, 'audit_file': audit}
    _lib.write_input_json(HERE, record)
    _lib.write_expected_output(
        HERE, status='FAIL', step='11', reason='signature verification failed',
        reason_template='signature verification failed',
        exit_code=1, anomaly=None,
    )
    print("[N004-signature-garbage] materialized:", 'FAIL', '11', 'signature verification failed')


if __name__ == "__main__":
    main()
