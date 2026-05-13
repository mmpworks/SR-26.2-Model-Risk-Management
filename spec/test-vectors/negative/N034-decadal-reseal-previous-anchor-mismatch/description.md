# N034 — §10.54 decadal re-seal previous-generation anchor mismatch

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.54 verifier-dispatch step 4: the `seal.resealed_previous_generation_anchor_sha256` MUST reference a seal-record that exists on the chain and is the last seal of the prior generation. A forged or tampered anchor breaks the re-seal generation linkage.

## Tampering recipe

Start from case 047. Modify ONE of:

**Variant A — fabricated previous-generation anchor:** Replace `seal.resealed_previous_generation_anchor_sha256` with a SHA-256 of an arbitrary string that doesn't correspond to any seal-record on the chain. The verifier walks the chain looking for a seal-record matching the anchor; finding none is a chain-integrity failure.

**Variant B — anchor points to a non-terminal seal:** Replace the anchor with a SHA-256 of an early-period seal (mid-generation rather than terminal). The verifier finds the seal but confirms it's not the prior generation's last seal — also a failure.

**Variant C — generation-index gap:** Set `seal.resealed_generation_index = 3` while emitting the first decadal re-seal (generation index should be 1). The chain has no generation-2 anchor, so a verifier walking the generation chain finds a gap.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.54 verifier-dispatch step 4 failure — previous-generation anchor not found / not terminal / generation-index gap
additional_verifications: []
```

## What this case proves

The §10.54 generation-chain integrity requires every re-seal to reference its prior generation's terminal seal. A 60-year retention chain accumulates 5-6 generations; an auditor reading at year T+50 walks 0 → 1 → 2 → 3 → 4 → 5 to confirm the current signature is verifiable under modern cryptography. A broken generation linkage means an auditor cannot reconstruct the migration history — the chain's long-retention guarantee fails.

## Cross-references

- Spec §10.54 decadal re-sealing
- Spec §10.42 backfill seal (the precedent §10.54 follows)
- Case 047 (the positive case this negative is derived from)
