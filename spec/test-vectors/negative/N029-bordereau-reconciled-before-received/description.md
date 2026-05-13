# N029 — Bordereau reconciled-before-received (lifecycle gap)

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.46 lifecycle integrity check catches the case where a `reconciled` event appears for a `bordereau_id` that has no prior `received` event. Per §10.46 verifier dispatch (b), `reconciled` events MUST follow `received` for the same party.

## Tampering recipe

Start from case 040 (`040-bordereau-lifecycle/`). Remove or skip event[1] (the `received` event) and submit only events [0, 2] (`published` then `reconciled`). The lifecycle is incoherent — a party reconciling against a bordereau without first acknowledging receipt of it is structurally suspect.

Alternative: change the `reconciling_party_identifier` on event[2] to a party that never emitted a `received` event for this `bordereau_id`. Same anomaly class.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.46 lifecycle integrity failure: reconciled event for bordereau_id "polaris-bordereau-2026-05" by party "polaris-reinsurance-bermuda" has no prior received event from the same party
Step: §10.46 lifecycle integrity check (b)
additional_verifications: []
```

## What this case proves

The §10.46 lifecycle integrity check enforces transition ordering. The state-machine primitive (§1.5 / GAP-2) supplies the underlying walk validation; §10.46's transitions table is `published → received → reconciled[clean|discrepancy]`, with `reconciled[discrepancy] → discrepancy_resolved`. Skipping `received` violates the transitions table.

A bordereau document that arrived through a non-chain channel and was reconciled out-of-band would still need to emit the `received` event to satisfy §10.46 — the chain is the integrity-bound retrieval substrate even when the document itself flows through a different transport.

## Cross-references

- Spec §10.46 bordereau integrity
- Spec §1.5 (the state-machine framing the §10.46 lifecycle is an instance of)
- Case 040 (the positive case this negative is derived from)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §7
