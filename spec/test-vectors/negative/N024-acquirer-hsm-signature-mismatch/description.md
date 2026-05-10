# N024 — Acquirer-HSM key fingerprint does not match dual_signatures' actual signing key

## Status

**Stub case.** Recipe and expected verifier outcome documented here. Byte-level fixture is derived from case 034 by the tampering recipe.

## Purpose

Verify the §10.39 verifier-dispatch path catches the case where the envelope's declared `acquirer_hsm_key_fingerprint` does not match the public key under which the to-entity signature in `dual_signatures` actually verifies. The mismatch is a chain-integrity failure (someone signed the inheritance under a different key than the one the institution's CC8.1 names); the verifier rejects.

## Tampering recipe

Start from case 034 (`034-successor-attestation/`). Modify ONE of the following:

**Variant A (declared fingerprint corruption):** Replace the envelope's `acquirer_hsm_key_fingerprint` with a different lowercase hex SHA-256 (e.g., flip one character). The to-entity's signature in `dual_signatures` still verifies under the correct key, but the declared fingerprint claims a different key.

**Variant B (signing key substitution):** Replace the to-entity's `dual_signatures[1].signature_b64` with a signature produced under a different Ed25519 key. The declared fingerprint matches the institution's CC8.1-named key, but the signature does not verify under that key.

Both variants surface as the same anomaly class: the relationship between the declared fingerprint and the actual signing key is broken.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.39 verifier-dispatch failure: acquirer-HSM key fingerprint does not match dual_signatures signing key
Step: §10.39 acquirer_hsm_key_fingerprint cross-binding to dual_signatures (the to-entity signature in the §10.17-shaped pair MUST verify under the public key whose SHA-256 is the declared acquirer_hsm_key_fingerprint)
additional_verifications: []
```

The empty `additional_verifications` array on a non-zero exit is the steady-state shape — bonus verifications are only reported on PASS.

## What this case proves

The verifier does not silently accept a successor-attestation envelope whose declared HSM fingerprint is disconnected from the actual signing key. The cryptographic integrity of the §10.39 institutional inheritance event depends on the acquirer signing under the key the institution has committed to in CC8.1; an envelope where the two are out of sync is exactly the kind of tampering the §10.39 dispatch path was designed to catch.

## Cross-references

- Spec §10.39 institutional successor-attestation
- Spec §10.17 signatory schema
- Case 034 (`034-successor-attestation/`) — the positive case this negative is derived from
- Design `12-successor-attestation-and-backfill.md` §6 (the threat-model alignment)
