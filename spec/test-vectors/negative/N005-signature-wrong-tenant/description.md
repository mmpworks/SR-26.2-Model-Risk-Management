# N005-signature-wrong-tenant

## Expected verifier outcome

```
Status: FAIL
Step:   11
Reason: signature verification failed
```

## Tampering recipe

Start from the valid baseline (single-IKM, 5 events).

The generator builds a `sign_payload` that binds a DIFFERENT tenant_id (`tenant-ffiec-test-OTHER`) over the baseline's real merkle_root and hkdf_inputs_digest, then signs that wrong-tenant payload with the real Ed25519 test key. It publishes that wrong-tenant `sign_payload_hex` and its genuine signature on the seal, but leaves the seal's structured `tenant_id` as the real tenant. `tenant_id` is bound into `sign_payload`, so the verifier — which reconstructs `sign_payload` from the structured fields, including the claimed real tenant_id — rebuilds bytes that differ from the published wrong-tenant `sign_payload_hex`. Step 11 fails at the reconstruct-and-compare assertion, before the Ed25519 verify is reached.

## Fixture shape

`input.json` is a real signature-bearing fixture. The `signature_b64` is a genuine Ed25519 signature — it verifies over the published wrong-tenant `sign_payload_hex` — which is exactly the point: the signature is real but binds the wrong tenant. The seal also carries `signed_for_tenant_id: "tenant-ffiec-test-OTHER"` as a descriptor of the recipe. The verifier resolves the public key from `_keys/test-signing-key.pub.hex` (`0985603b…7f35`).

The generator reads the seed from `TESSERASEAL_TEST_KEY_DIR` (default `E:\dev\testing\private-keys\tesseraseal`) and FAILS with a clear message when the key directory is absent — it never falls back to placeholder bytes.

## Conformance test

Verifier MUST execute spec §7 steps 1..(11-1) cleanly and fail at step 11 with the exact reason string above. A verifier that produces `Status: PASS` is broken; a verifier that fails at a different step (or with a different reason string) is non-conforming for the rework's named-failure-mode taxonomy.

## See also

- spec §7 step 11 (the failure step)
- `docs/regulator-pack/finding-language.md` row for step 11 (the examiner-finding paragraph)
- `docs/incident-response-playbook.md` IR scenario mapped to step 11 (the institution-side response)
