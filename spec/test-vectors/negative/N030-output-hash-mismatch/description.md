# N030 — Generation output_sha256 does not match canonical output bytes

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.47 four-tuple integrity claim: a generation event's `output_sha256` MUST match the SHA-256 of the canonical output bytes the chain provides as evidence. Mismatch is a chain-integrity failure.

## Tampering recipe

Start from case 041 (`041-generation-four-tuple/`). Modify ONE of:

**Variant A:** Flip a single byte in the model's output (the response text the institution provides as evidence). The `output_sha256` on the chain entry no longer matches the SHA-256 of the canonical output bytes.

**Variant B:** Flip a character in the chain entry's `output_sha256` value while leaving the actual output unchanged.

Either variant breaks the binding.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.47 four-tuple integrity failure: output_sha256 on chain entry does not match SHA-256 of canonical output bytes
additional_verifications: []
```

## What this case proves

The §10.47 four-tuple is the per-inference integrity claim. A regulator presented with the chain entry AND the alleged output bytes can verify they match by recomputing SHA-256(canonical output bytes) and comparing to `output_sha256`. Tampering with either side surfaces here.

## Cross-references

- Spec §10.47 generation prompt/output four-tuple binding
- Case 041 (the positive case this negative is derived from)
- Spec §1.2 stochastic-output epistemic claim
