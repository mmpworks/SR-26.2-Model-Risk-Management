# Case 037 — State-machine transition-validator (§1.5 / GAP-2)

## What this case verifies

Spec §1.5 frames *long-running case* records that move through ordered states under named transitions (insurance claims, regulatory disputes, audit examinations). The transition-validator + walk-validator described here is a minimal shared primitive (per §1.5 / GAP-2) consumed by §10.43 (claim-state), §10.46 (bordereau lifecycle), and §10.55 (challenge-response) — all currently normative-when-applicable.

The primitive is intentionally *domain-agnostic*. It validates:

1. A single transition `(from_state, to_state)` against a caller-supplied transitions table.
2. A sequence of transitions for coherence: each step's transition is in the table, and each step's `from_state` matches the prior step's `to_state` (no history gaps).
3. No transition out of a terminal state (a state with no outbound transitions).

This case pins the JCS-canonical byte form of the validator's structured output across four walks — happy path, invalid transition, transition-out-of-terminal, and history gap.

## What this case does NOT verify

Domain semantics (claim adjudication rules, bordereau reconciliation logic, dispute disposition policy) are NOT in scope. §10.43 and §10.46 each define their own state enumerations and their own transitions tables; the GAP-2 primitive validates the structural transitions, not the domain rules. Case 038 (claim-state) and case 040 (bordereau) pin the domain-specific byte forms.

## Inputs

A 4-state transitions table mirroring §10.43's high-level lifecycle:

```
opened   → pending, closed
pending  → decided, closed
decided  → closed
closed   → (terminal)
```

Four walks exercise the validator:

| Walk | Sequence | Expected outcome |
|---|---|---|
| A — happy path | opened→pending, pending→decided, decided→closed | valid |
| B — skips pending | opened→decided | invalid (transition not in table) |
| C — out of terminal | closed→opened | invalid (transition not in table) |
| D — history gap | opened→pending, decided→closed | invalid (prior to_state ≠ current from_state) |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `1032` |
| canonical SHA-256 | `23fd87b2a573ca29ece4015c52575f90f429c677d8278ee0fe06026d10a67b3f` |

`expected_canonical.txt` carries the bytes verbatim; `expected_canonical_sha256.txt` is the SHA-256 for quick comparison. JCS canonicalization sorts object keys lexicographically; the canonical form's nested objects appear in alphabetic order.

## Conformance behavior

A conforming implementation supporting GAP-2:

1. Constructs the structured-output dict with the same nested layout (`transitions_table`, `walks` with sub-keys per walk; each walk carries `input` and `result`).
2. Per-walk `result` is a 3-field dict: `valid` (bool), `first_failure_index` (int or null), `reason` (string).
3. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.
4. The single-transition validator accepts (from, to) iff `to` is in `transitions_table[from]`. The sequence validator additionally enforces history-gap rejection.

## Cross-references

- Spec §1.5 (the framing this primitive instantiates)
- Spec §10.43 claim-state-machine (the first §10.X consumer)
- Spec §10.46 bordereau lifecycle (the second §10.X consumer)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §3 (rationale for the seam)
- Case 038 `038-claim-state-lifecycle/` (the domain-specific consumer)
- Case 040 `040-bordereau-lifecycle/` (the lifecycle-event-family consumer)
- Negative case `negative/N027-state-machine-invalid-transition/` (transition out of terminal)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
