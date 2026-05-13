# N028 — Adjuster anchor missing reverse-link

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.45 bidirectional cross-anchor enforcement catches the case where the cedent's anchor entry references the reinsurer's chain entry but the reinsurer's anchor entry has no `peer_party_chain_entries` referencing the cedent. The unilateral reference is non-conformant under §10.45 verifier dispatch (a)/(b).

## Tampering recipe

Start from case 039 (`039-adjuster-anchor-bidirectional/`). Modify the reinsurer-side anchor in one of two ways:

**Variant A — empty peer list:** Set `peer_party_chain_entries = []` on the reinsurer-side anchor. The cedent's anchor still references the reinsurer's `(run_id, seq)`, but the reinsurer's anchor names no peers — bidirectional verifier check (a) fails.

**Variant B — references a different cedent:** Replace the reinsurer-side anchor's `peer_party_chain_entries[0].peer_run_id` with `"some-unrelated-claim-99999"`. The reverse-link mismatches; verifier check (b) fails.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.45 bidirectional cross-anchor failure: <step-specific reason>
  - Variant A: peer_party_chain_entries is empty on the reinsurer-side anchor; bidirectional anchor requires at least one peer reference
  - Variant B: cedent-side anchor references reinsurer entry (run_id=X, seq=Y), but reinsurer-side anchor's peer_party_chain_entries does not contain a reverse reference to cedent
additional_verifications: []
```

## What this case proves

A unilateral cross-anchor (one party references the other but not vice versa) does not satisfy §10.45's bidirectional integrity claim. The verifier's reverse-link consistency check is what makes the §10.45 anchor *bidirectional* — without it, a cedent could fabricate an anchor-record naming an adjuster that didn't actually appear on the reinsurer's chain.

## Cross-references

- Spec §10.45 adjuster anchor
- Case 039 (the positive case this negative is derived from)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §6
