# Case 043 — Output-grounding review event (§10.50)

## What this case verifies

Spec §10.50 normates the output-review event family composing GAP-2 state-machine (pending_review → reviewed[outcome]) with GAP-5 HITL primitive (signed-review-event embedded as `audit.review.signed_review`). This case pins a `grounding_pass` outcome — a Lyceum-shape clinician confirmed the AI synthesis is grounded in the retrieval set.

## Inputs

| Field | Value |
|---|---|
| `parent_run_id` | `lyceum-medsynth-2026-04-12-clinical-query-12847` (matches case 041) |
| `parent_seq` | `1` |
| `outcome` | `grounding_pass` |
| `review_rationale_hash` | `SHA-256(canonical bytes of clinician rationale)` |
| `signed_review.reviewer_id` | `lyceum-clinician-reviewer-key-id-cardiology-2026-04` |
| `signed_review.reviewer_role` | `attending_physician` |
| `signed_review.signed_at_utc` | `2026-04-12T11:00:00Z` |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `847` |
| canonical SHA-256 | `76c9f96664ad76a281c6889be47e748df864a0c06e15f4ab3b8f62a296f69ee9` |

## Conformance behavior

A conforming implementation:

1. Builds the §10.50 review event with the 5 attributes (parent_run_id, parent_seq, outcome, review_rationale_hash, signed_review).
2. The `signed_review` value is a GAP-5 signed-review-event per case 044's primitive shape.
3. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to `expected_canonical.txt`.
4. Verifier dispatches at chain-walk time: looks up the reviewer's public key by `reviewer_id`, verifies the signature against the canonical bytes of `signed_payload_sha256`, confirms the four-canonical-outcome enumeration includes `grounding_pass`.

## Cross-references

- Spec §10.50 output-grounding event family
- Spec §1.5 / §10.43 GAP-2 state-machine (pending_review → reviewed transition)
- Spec GAP-5 HITL primitive (signed-review-event embedded form)
- Spec §10.11 ECOA adverse-action notice translation (the precedent §10.50 generalizes)
- Spec §10.55 audit-target challenge-response (reuses the same composition)
- Case 041 (the generation event being reviewed)
- Case 044 (the GAP-5 primitive standalone)

## Reproduction

```
python _compute.py
```
