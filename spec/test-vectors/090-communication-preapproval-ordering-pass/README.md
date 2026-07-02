# 090 — communication principal-preapproval ordering (pass)

Pins the §10.84 (FINRA Rule 2210) **conformant** arrangement: a registered
principal's approval precedes the send of a retail communication.

## What this vector fixes

`expected_canonical.txt` is the JCS-canonical (RFC 8785) byte form of the
three-event §10.84 scenario:

1. **communication** — carries `audit.communication.audience = "retail"`, the
   only audience Rule 2210 subjects to registered-principal pre-approval.
2. **principal_approval** — a §10.50 review event with
   `audit.review.role = "registered_principal"` (flat dotted keys). Its
   `audit.review.signed_review.audit.signed_review.signed_at_utc` (`2026-06-01T10:00:00Z`)
   is the approval time.
3. **send** — a §14.8 `audit.downstream_action` event (nested object) with
   `action_kind = "communication_sent"` and §4.4 top-level parent linkage
   (`parent_run_id` / `parent_seq`). Its `applied_at_utc` (`2026-06-01T12:00:00Z`)
   is the send time.

Because approval (10:00) precedes send (12:00), a conforming verifier emits the
§10.12 marker **`communication_principal_preapproval_verified`**.

## Files

- `_compute.py` — regenerates the fixture (requires the `jcs` module).
- `input.json` — the three events plus the `expected` block (verdict = marker).
- `expected_canonical.txt` — JCS-canonical bytes of the scenario.
- `expected_canonical_sha256.txt` — `sha256(expected_canonical.txt)`.

## Conformance gates

- **Byte pin** — the Go corpus runner (`verifier/internal/vectors/canonical.go`)
  auto-discovers this directory and gates sha256 self-consistency + JCS
  idempotency, so C#, Python, and Go reconstruct byte-identical bytes.
- **Behavior** — the marker/anomaly ordering logic is exercised by
  `verifier/internal/verify/communication_preapproval_test.go`
  (`TestPreapproval_ApprovalBeforeSend_MarkerVerified` mirrors this vector's events).

Negative sibling: `091-communication-preapproval-ordering-anomaly`.
