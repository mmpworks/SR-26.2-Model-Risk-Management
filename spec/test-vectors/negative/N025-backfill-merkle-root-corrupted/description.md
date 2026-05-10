# N025 — Backfill seal Merkle root corrupted by single-byte flip

## Status

**Stub case.** Recipe and expected verifier outcome documented here. Byte-level fixture is derived from case 035 by the tampering recipe.

## Purpose

Verify the §10.42 verifier-dispatch step 2 catches a corrupted Merkle root: the seal's apex root claims one value but the recomputed root over (baseline manifest leaves + metadata leaf) produces a different value. The mismatch is a chain-integrity failure; the verifier rejects.

## Tampering recipe

Start from case 035 (`035-backfill-seal/`). Modify ONE of the following:

**Variant A (apex root corruption):** Flip a single byte in the seal's `merkle_root_hex` (the value embedded in the v1.0b sign_payload at line 7). The signature over sign_payload no longer verifies because the bound payload changed; verifier surfaces the signature failure.

**Variant B (metadata-leaf corruption):** Modify a value in the metadata leaf (e.g., change `seal.backfill_window_end_utc` to a different timestamp). The leaf's recomputed hash differs; the recomputed Merkle root over (baseline leaves + corrupted metadata leaf) does not match the seal's claimed apex root; verifier surfaces the recomputation mismatch.

**Variant C (baseline-manifest leaf corruption):** Modify one of the 8 baseline manifest tuples (e.g., change a `sha256` value). The corresponding leaf hash changes; the recomputed Merkle root does not match the seal's claimed apex root; verifier surfaces the recomputation mismatch.

All three variants surface as integrity failures, but the *step* at which they surface differs (Variant A at step 4 / signature verification; Variants B and C at step 2 / Merkle root recomputation). The verifier's normative reason string names the step.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.42 verifier-dispatch failure: <step-specific reason>
  - Variant A: signature over v1.0b sign_payload does not verify under acquirer-HSM key
  - Variant B: backfill-seal Merkle root mismatch — recomputed root differs from seal apex root (metadata leaf modified)
  - Variant C: backfill-seal Merkle root mismatch — recomputed root differs from seal apex root (baseline manifest leaf modified)
Step: §10.42 step 2 (Merkle root verification) or step 4 (signature verification)
additional_verifications: []
```

## What this case proves

The Merkle root binding over (baseline manifest leaves + metadata leaf) is what makes the §10.42 attribute integrity claim load-bearing. Without it, an attacker with chain-write access could modify the metadata-leaf attributes (e.g., shorten the backfill window to exclude inconvenient pre-acquisition records) without the verifier detecting. The Merkle binding closes the gap; this negative case confirms the closure.

## Cross-references

- Spec §10.42 backfill seal discipline
- Spec §4.2 daily Merkle seal
- Spec §4.3 sign_payload v1.0b
- Case 035 (`035-backfill-seal/`) — the positive case this negative is derived from
- Case `negative/N003-merkle-root-altered/` — the §4.2 sibling negative case
- Design `12-successor-attestation-and-backfill.md` §6 (the threat-model alignment)
