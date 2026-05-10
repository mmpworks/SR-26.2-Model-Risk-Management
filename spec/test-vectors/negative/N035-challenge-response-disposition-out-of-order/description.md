# N035 — §10.55 challenge-response disposition out of order

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.55 + §10.43 GAP-2 state-machine composition: a disposition event MUST follow a `filed` (or `triaged`) state for the named challenge, and the disposition MUST reference an existing `original_decision_run_id`. Out-of-order or orphan dispositions break the lifecycle.

## Tampering recipe

Start from case 048. Modify ONE of:

**Variant A — disposition without prior filing:** Emit the §10.55 disposition entry without ever emitting the prior §10.43 `filed` state event for the challenge. The verifier walks the chain looking for the challenge's lifecycle anchor; finding none is a state-machine integrity failure (GAP-2's "no skipping initial state" invariant).

**Variant B — disposition references unknown decision:** Set `original_decision_run_id = "fabricated-decision-id-not-on-chain"`. The verifier confirms the named decision run exists on the chain; absence is a binding failure.

**Variant C — double disposition:** Emit two §10.55 disposition entries for the same `original_decision_run_id` + `original_decision_seq` pair (e.g., once `upheld`, once `overturned`). The state-machine forbids multi-disposition; the second event is a duplicate-terminal violation.

**Variant D — outcome not documented in CC8.1:** Set `outcome = "tabled_pending_appeal"`. Per spec §10.55 the outcome MAY be one of the canonical four (`upheld | overturned | modified | withdrawn`) OR an institution-named outcome documented in CC8.1. The chain-integrity verifier accepts any non-empty string; this is NOT a chain-integrity failure. It IS a CC8.1 control-completeness finding the regulator surfaces during the operational audit: an institution emitting an outcome value that does NOT appear in its published CC8.1 control description is a control-narrative-versus-implementation drift, even though the chain itself is honest.

## Expected verifier outcome

```
Variants A / B / C (chain-integrity failures):
exit_code: 1
Status: FAIL
Reason: §10.55 + §10.43 state-machine violation — disposition without prior filing / unknown decision / double terminal
additional_verifications: []

Variant D (control-completeness finding, NOT chain-integrity):
exit_code: 0 (chain-integrity is fine)
Reason: out-of-band CC8.1 control-completeness finding (regulator's audit, NOT chain verification)
```

## What this case proves

§10.55's value comes from composing GAP-2 (lifecycle integrity) with GAP-5 (signed disposition). The lifecycle invariants — every challenge has a filing, every disposition has a corresponding filing, dispositions are once-per-challenge, outcomes come from a closed enumeration — are what makes the auditor's challenge-response review tractable. A regulator opening a 2030 parliamentary inquiry into the Helvetian Federal Tax Authority needs to enumerate "all challenges filed in 2026, their dispositions, and the dispositioning judges" without semantic drift; the state-machine + enum constraints make that query well-defined.

## Cross-references

- Spec §10.55 audit-target challenge-response
- Spec §10.43 GAP-2 claim-state-machine
- Spec §1.5 state-machine framing
- Case 048 (the positive case this negative is derived from)
