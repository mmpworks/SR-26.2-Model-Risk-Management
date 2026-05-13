# Case 040 — Bordereau lifecycle (§10.46)

## What this case verifies

Spec §10.46 normates the four-event chain-entry family for bordereau lifecycle integrity. This case pins the JCS-canonical bytes for a clean three-event sequence: `published` → `received` → `reconciled[clean]`. The fourth event (`discrepancy_resolved`) is exercised only in the discrepancy branch and is NOT included here.

## Inputs

A May 2026 cession bordereau:

| Index | Event kind | Key attributes |
|---|---|---|
| 0 | published | bordereau_id, period_start, period_end, bordereau_sha256, published_at_utc, cedent_party_identifier |
| 1 | received | bordereau_id, received_at_utc, receiving_party_identifier, bordereau_sha256 |
| 2 | reconciled | bordereau_id, reconciled_at_utc, reconciling_party_identifier, reconciliation_outcome (`"clean"`), reconciliation_record_sha256, bordereau_sha256 |

All three events share the same `bordereau_sha256` (`4b0d460376f50e88…`) — verifier check (d) of §10.46 confirms cross-event consistency.

## Expected canonical bytes

| Index | Event kind | Canonical bytes | SHA-256 |
|---|---|---|---|
| 0 | published | 448 | `84425701453b19eeb7758de5afda62ae85d84234721ffc1802cf07342d97f7d0` |
| 1 | received | 334 | `a9f9d612d9b0d2984f2930062c14c6313df8424ef9eb3beced988f6783d28de3` |
| 2 | reconciled | 503 | `1f5005247a3e477c74a195443b9e2a3473c527eb008ba2fefe5baf107cae4874` |
| Lifecycle digest | — | — | `5443f77fdc0bbe1912c2c98bd05d57f248df316562bea5806fe72826bb1342f2` |

`expected_canonical.txt` carries the byte form of event[0] (the `published` event); `expected_canonical_sha256.txt` lists all three per-event hashes plus the lifecycle digest.

## Conformance behavior

A conforming implementation:

1. Builds each event with the §10.46 attribute schema for its event kind.
2. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to the pinned forms.
3. Walks events in chronological order and confirms (a) `received` follows `published`; (b) `reconciled` follows `received` for the same party; (c) `bordereau_sha256` consistent across events.

## Cross-references

- Spec §10.46 bordereau integrity
- Spec §10.19 `audit.external_artifact.*` (the substrate for the bordereau document hash)
- Spec §10.38 consent capture (the lifecycle-pattern sibling)
- Spec §10.43 claim-state-machine (cross-bound via `audit.claim_state.bordereau_id`)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §7 (rationale)
- Negative case `negative/N029-bordereau-reconciled-before-received/`

## Reproduction

```
python _compute.py
```
