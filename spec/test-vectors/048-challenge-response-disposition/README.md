# Case 048 — Challenge-response disposition (§10.55)

## What this case verifies

Spec §10.55 normates the challenge-response event family composing GAP-2 state-machine (filed → triaged → disposed; or filed → disposed when triage is operationally skipped) with GAP-5 HITL primitive (signed disposition). This case pins an `overturned` outcome — a Helvetian taxpayer challenged an AI-flagged audit and the agency reversed the decision after administrative-law-judge review.

## Inputs

| Field | Value |
|---|---|
| `original_decision_run_id` | `helvetian-vat-audit-target-2026-04-12-taxpayer-CH184729` |
| `original_decision_seq` | `1` |
| `outcome` | `overturned` |
| `rationale_hash` | SHA-256 of canonical disposition rationale |
| `signed_disposition.reviewer_id` | `helvetian-administrative-law-judge-key-id-CH-2026` |
| `signed_disposition.reviewer_role` | `administrative_law_judge` |
| `signed_disposition.signed_at_utc` | `2026-05-20T14:00:00Z` |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `934` |
| canonical SHA-256 | `63d81cf7f84bffe8f59b7a74b72b17bf4b61f089fdc1202279e58afab39c66ea` |

## Conformance behavior

A conforming implementation:

1. Builds the §10.55 challenge-response event with the 5 attributes (original_decision_run_id, original_decision_seq, outcome, rationale_hash, signed_disposition).
2. The `signed_disposition` value is a GAP-5 signed-review-event per case 044's primitive shape.
3. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to `expected_canonical.txt`.
4. Verifier dispatches at chain-walk time: looks up the disposing reviewer's public key by `reviewer_id`, verifies the signature against the canonical bytes of `signed_payload_sha256`, confirms the four-canonical-outcome enumeration includes `overturned`.

## Composition with §10.50

§10.55 mirrors §10.50 (clinical decision support output review) — same composition (GAP-2 state-machine + GAP-5 HITL), different domain (civic-AI vs clinical), different outcome enum (`upheld | overturned | modified | withdrawn` vs `clinician_edit | grounding_pass | grounding_fail | hallucination_detected`).

## Cross-references

- Spec §10.55 audit-target challenge-response
- Spec §10.50 output-grounding event family (the clinical sibling)
- Spec §1.5 / §10.43 GAP-2 state-machine (the lifecycle substrate)
- Spec GAP-5 HITL primitive (the signed-disposition substrate)
- Case 044 (the GAP-5 primitive standalone)
- Negative case `negative/N035-challenge-response-disposition-out-of-order/`

## Reproduction

```
python _compute.py
```
