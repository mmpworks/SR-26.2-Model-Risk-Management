# Case 039 — Adjuster anchor (§10.45) bidirectional

## What this case verifies

Spec §10.45 normates `chain.adjuster_anchor` operational events for independent third-party adjusters whose activity appears on multiple parties' chains simultaneously. This case pins the JCS-canonical bytes for both sides of a bidirectional anchor: a Marsh Adjusting Services LLC loss investigation that appears on Cape Madeline's chain (cedent side) and Polaris Reinsurance's chain (reinsurer side).

## Inputs

Both anchors share:
- `adjuster_id`: `marsh-adjusters-license-NY-2718281`
- `adjuster_legal_name`: `Marsh Adjusting Services LLC`
- `adjuster_role`: `loss_adjuster`
- `activity_record_sha256`: `a3cc053d910b28372127a755df5499c556d7bfeac7e37a7b55541b876df4010a`
- `activity_utc`: `2026-04-12T13:30:00Z`

Each anchor's `peer_party_chain_entries` references the other side's `(run_id, seq)`:

| Anchor | Peer party_role | Peer party_identifier | peer_run_id | peer_seq |
|---|---|---|---|---|
| cedent_anchor | reinsurer | polaris-reinsurance-bermuda | polaris-cession-claim-2026-04-payment-loss-12847 | 4 |
| reinsurer_anchor | cedent | cape-madeline-bank-and-trust | cape-madeline-claim-12847 | 8 |

## Expected canonical bytes

| Anchor | Canonical byte length | Canonical SHA-256 |
|---|---|---|
| cedent_anchor | 727 | `d8df3fe5cd69eb7bb408a5eacdeb31a22e0861cc6ac3ae8a862548c0d03b4101` |
| reinsurer_anchor | 702 | `03905ac5bbed6c23b86b2a3e76dff35f2d18cb7233f98e29bc7fead929048588` |
| shared activity_record | — | `a3cc053d910b28372127a755df5499c556d7bfeac7e37a7b55541b876df4010a` |

`expected_canonical.txt` carries cedent-side bytes; `expected_reinsurer_canonical.txt` carries reinsurer-side bytes.

## Conformance behavior

A conforming implementation:

1. Builds each anchor with the §10.45 attribute schema.
2. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to the pinned forms.
3. Verifier confirms (a) `peer_party_chain_entries` non-empty; (b) reverse-link consistency (each peer entry references this entry back); (c) `activity_record_sha256` consistent across both anchors.

## Cross-references

- Spec §10.45 adjuster anchor
- Spec §10.31 role-aware extension (the role enumeration §10.45 reuses)
- Spec §10.21 cross-vendor model handover (the deliverer-handover sibling)
- Spec §10.40 cross-vendor chain-merge cross-anchor (the one-way inheritance sibling)
- Design `docs/design/13-state-machine-and-multi-party-flows.md` §6 (rationale)
- Negative case `negative/N028-adjuster-anchor-missing-reverse-link/`

## Reproduction

```
python _compute.py
```
