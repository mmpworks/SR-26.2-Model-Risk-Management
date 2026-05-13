# N027 — Invalid state transition (out of terminal state)

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §1.5 / GAP-2 state-machine primitive rejects transitions that violate the institution's CC8.1-named transitions table. This case specifically exercises the "no transition out of a terminal state" rule via a `closed → opened` transition.

## Tampering recipe

Start from case 037's transitions table (`opened → pending|closed`, `pending → decided|closed`, `decided → closed`, `closed → ∅`). Submit a single transition: `from_state = "closed"`, `to_state = "opened"`. The verifier rejects.

## Expected verifier outcome

```
exit_code: 1 (chain anomaly) on a chain context, or
validator returns:
  valid: false
  first_failure_index: 0
  reason: "transition ('closed' -> 'opened') not in transitions table"
```

A walk that includes a `closed → ⟨any⟩` step is non-conformant per §1.5 lifecycle integrity.

## What this case proves

The minimal state-machine primitive correctly enforces the transitions-table semantics across all consumers. §10.43 claim closure, §10.46 bordereau reconciliation closure, and §10.55 challenge-response all benefit from the same primitive's terminal-state-respecting walk.

## Cross-references

- Spec §1.5
- Case 037 (the positive case this negative is derived from)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §3
