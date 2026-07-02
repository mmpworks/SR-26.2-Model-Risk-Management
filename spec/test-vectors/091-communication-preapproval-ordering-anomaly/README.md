# 091 — communication principal-preapproval ordering (anomaly)

Pins the §10.84 (FINRA Rule 2210) **non-conformant** arrangement: a registered
principal's approval comes AFTER the send of a retail communication.

## What this vector fixes

`expected_canonical.txt` is the JCS-canonical (RFC 8785) byte form of the same
three-event scenario as case 090, with one change: the principal's approval
`signed_at_utc` is `2026-06-01T14:00:00Z` — **after** the send's `applied_at_utc`
of `2026-06-01T12:00:00Z`.

Because approval (14:00) does not precede send (12:00), a conforming verifier
emits the soft-enforcement anomaly line under `Status: PASS`:

```
communication principal-preapproval ordering: approval did not precede send at seq 3
```

§10.84 is a **completeness** check, not a chain-integrity gate: the chain still
PASSes integrity verification; the anomaly is what a FINRA examiner or SOC
engagement reviews. `seq 3` is the send event's `seq`.

## Files

- `_compute.py` — regenerates the fixture (requires the `jcs` module).
- `input.json` — the three events plus the `expected` block (verdict = anomaly,
  the exact anomaly line, and `status = PASS`).
- `expected_canonical.txt` — JCS-canonical bytes of the scenario.
- `expected_canonical_sha256.txt` — `sha256(expected_canonical.txt)`.

## Conformance gates

- **Byte pin** — the Go corpus runner (`verifier/internal/vectors/canonical.go`)
  auto-discovers this directory and gates sha256 self-consistency + JCS
  idempotency.
- **Behavior** — the anomaly path is exercised by
  `verifier/internal/verify/communication_preapproval_test.go`
  (`TestPreapproval_ApprovalAfterSend_Anomaly` mirrors this vector's events and
  asserts the anomaly line).

Positive sibling: `090-communication-preapproval-ordering-pass`.
