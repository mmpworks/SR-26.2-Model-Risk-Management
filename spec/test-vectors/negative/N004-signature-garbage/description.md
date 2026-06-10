# N004-signature-garbage

## Expected verifier outcome

```
Status: FAIL
Step:   11
Reason: signature verification failed
```

## Tampering recipe

Start from the valid baseline (single-IKM, 5 events), signed with the corpus test key.

The generator first signs the baseline seal with the real Ed25519 test key, so `sign_payload_hex` and `signature_b64` start as a genuine, verifying pair. It then replaces `signature_b64` with 64 bytes of `0xFF` (base64-std). The substitution leaves every other field — including `sign_payload_hex` — intact. Steps 1-10 pass; the step-11 reconstruct-and-compare assertion passes (the structured fields still reconstruct the published `sign_payload`); the Ed25519 verify fails because the signature bytes no longer match.

## Fixture shape

`input.json` is a real signature-bearing fixture. The seal carries the genuine `sign_payload_hex` (the v1.0a 10-line byte form) and the garbage `signature_b64`. The verifier resolves the public key from `_keys/test-signing-key.pub.hex` (`0985603b…7f35`). The signature is reproducible: anyone holding the local-only seed regenerates the same baseline signature and applies the same documented mutation.

The generator reads the seed from `TESSERASEAL_TEST_KEY_DIR` (default `E:\dev\testing\private-keys\tesseraseal`) and FAILS with a clear message when the key directory is absent — it never falls back to placeholder bytes.

## Conformance test

Verifier MUST execute spec §7 steps 1..(11-1) cleanly and fail at step 11 with the exact reason string above. A verifier that produces `Status: PASS` is broken; a verifier that fails at a different step (or with a different reason string) is non-conforming for the rework's named-failure-mode taxonomy.

## See also

- spec §7 step 11 (the failure step)
- `docs/regulator-pack/finding-language.md` row for step 11 (the examiner-finding paragraph)
- `docs/incident-response-playbook.md` IR scenario mapped to step 11 (the institution-side response)
