# N033 — §10.51 DP noise seed tampered

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.51 publication integrity claim: the chain-bound `dp_seed` and `dp_mechanism_version_sha256` MUST match what the institution actually used to apply DP noise. Tampering with the seed (post-publication) breaks the regulator's out-of-band reproducibility check.

## Tampering recipe

Start from case 045. Modify ONE of:

**Variant A — seed substitution:** Replace `dp_seed = 4242` with `dp_seed = 9999` after publication. The chain-bound canonical bytes change; the §7 step 9 MAC verification fails (the entry's `payload_hash` no longer matches the recomputed canonical bytes).

**Variant B — mechanism-version-hash substitution:** Replace `dp_mechanism_version_sha256` with a different hash. Same MAC mismatch as Variant A.

**Variant C — out-of-band reproducibility failure:** Leave the chain entry intact, but the regulator-side audit re-runs the noise application with the bound seed against the underlying raw aggregate and finds the result doesn't match the chain-bound `aggregate_published_value`. This is NOT a chain-integrity finding — the chain's binding is honest. It IS a privacy-control finding the regulator surfaces as an out-of-band correctness issue.

## Expected verifier outcome

```
exit_code: 1 (Variants A or B)
Status: FAIL
Reason: §7 step 9 MAC mismatch — chain entry's payload_hash does not match recomputed canonical bytes (post-hoc tampering with §10.51 attributes detected)

Variant C:
exit_code: 0 (chain-integrity is fine)
Reason: out-of-band privacy-correctness finding (regulator's audit, NOT chain verification)
```

## What this case proves

The chain's per-event MAC binds the §10.51 attributes against post-hoc tampering. A regulator running the noise-correctness audit out-of-band uses the chain-bound seed and mechanism-version hash to confirm the institution applied the DP mechanism faithfully. The chain is the integrity foundation; DP correctness is the regulator's audit (Variant C).

## Cross-references

- Spec §10.51 public-transparency overlay
- Spec §1.2 public-transparency epistemic claim
- Case 045 (the positive case this negative is derived from)
