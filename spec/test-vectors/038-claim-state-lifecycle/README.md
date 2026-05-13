# Case 038 — Claim-state lifecycle (§10.43)

## What this case verifies

Spec §10.43 normates `chain.claim_state.transition` operational events for chain-of-custody-bound insurance claims. This case pins the JCS-canonical bytes for a Polaris/Lloyd's-shape 6-transition lifecycle plus the lifecycle digest.

## Inputs

A 6-event lifecycle for a Polaris-shape reinsurance cession claim:

| Index | from_state / from_substate | to_state / to_substate |
|---|---|---|
| 0 | opened / fnol_received | opened / reserve_set_initial |
| 1 | opened / reserve_set_initial | pending / adjudication_committee_review |
| 2 | pending / adjudication_committee_review | decided / cession_payment_authorized |
| 3 | decided / cession_payment_authorized | decided / recovery_subrogation_review |
| 4 | decided / recovery_subrogation_review | decided / recovery_complete_no_recovery |
| 5 | decided / recovery_complete_no_recovery | closed / closed_paid_with_no_recovery |

Each event carries a deterministic actor, rationale, authorizing policy ID + SHA-256, and RFC 3339 UTC timestamp.

## Expected canonical bytes

Per-event SHA-256 (lowercase hex):

| Index | SHA-256 |
|---|---|
| 0 | `9bf730ca86a660ec…` (full 64 chars in `expected_canonical_sha256.txt`) |
| 1 | `818d94fd50451694…` |
| 2 | `b326c7f80c8726cd…` |
| 3 | `c71cf3e38736c98c…` |
| 4 | `1b418dee012d7380…` |
| 5 | `4ba5d8809e97428c…` |

Lifecycle SHA-256 (digest over the JCS-canonical sorted array of per-event hashes): `2255016bf1b9b82cf4b6bd86fba51c48ef03504ac9fb92b061dba783201a17d7`

`expected_canonical.txt` carries the byte form of event[0] (the FNOL → reserve_set transition); `expected_canonical_sha256.txt` lists all six per-event hashes plus the lifecycle digest.

## Conformance behavior

A conforming implementation:

1. Builds each transition event as a JSON object with the §10.43 attribute schema (8-9 fields per transition).
2. Canonicalizes each per RFC 8785 (JCS); produces bytes byte-identical to the per-event hashes.
3. Walks the events in `transition_utc` order and confirms (a) first event's `from = "opened"`, (b) every subsequent event's `from` matches prior event's `to`, (c) every transition is in the institution's CC8.1-named transitions table, (d) no event leaves `closed`.
4. Computes the lifecycle digest as SHA-256 of the JCS-canonical sorted array of per-event hashes.

## Cross-references

- Spec §10.43 claim-state-machine
- Spec §1.5 (the framing this section instantiates)
- Spec §10.46 bordereau (cross-bound via `audit.claim_state.bordereau_id` on the close event)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §4 (rationale)
- Case 037 `037-state-machine-transition-validator/` (the GAP-2 primitive this case consumes)
- Negative case `negative/N027-state-machine-invalid-transition/`

## Reproduction

```
python _compute.py
```
