# Case 044 — GAP-5 HITL signed-review-event primitive

## What this case verifies

GAP-5 normates a minimal shared signed-review-event primitive consumed by §10.50 (output-grounding output review) and §10.55 (audit-target challenge-response). The primitive provides:

1. A signed-review-event chain-entry schema (`audit.signed_review.*` attribute family with 6 fields).
2. Per-reviewer key-registry validation (reviewer_id resolves to a public key whose fingerprint matches).
3. Cross-binding helpers (parent_run_id / parent_seq).

This case pins the byte form *standalone*, isolated from §10.50 wrapping. The same byte form is embedded inside case 043's `audit.review.signed_review` field.

## Inputs

| Field | Value |
|---|---|
| `reviewer_id` | `lyceum-clinician-reviewer-key-id-cardiology-2026-04` |
| `reviewer_role` | `attending_physician` |
| `signed_at_utc` | `2026-04-12T11:00:00Z` |
| `reviewer_public_key_fingerprint` | `SHA-256(synthetic clinician pubkey bytes)` |
| `signed_payload_sha256` | `SHA-256(JCS-canonical bytes of the review-payload object)` |
| `signature_b64` | base64-encoded synthetic 64-byte signature |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `565` |
| canonical SHA-256 | `05c072eb447b17879661d248d11e2964ff6e34a80d0d11606dd5a53ee8d55ea7` |
| signed_payload_sha256 | `5d49f1585da164e3d6189ac97afea9cd454e4a4802dc3b5c9dec4bf16eed16b7` |

## Conformance behavior

A conforming implementation:

1. Builds the signed-review-event with the 6 `audit.signed_review.*` fields above.
2. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to `expected_canonical.txt`.
3. Verifier dispatches at chain-walk time: (a) looks up the reviewer's public key by `reviewer_id` against the institution's CC8.1-named registry; (b) confirms the `reviewer_public_key_fingerprint` matches the looked-up key; (c) verifies the signature against the canonical bytes whose hash is `signed_payload_sha256`.

## Cross-references

- Spec GAP-5 HITL primitive
- Spec §10.50 output-grounding event family (the first §10.X consumer)
- Spec §10.55 audit-target challenge-response (the second consumer)
- Spec §10.17 signatory schema (related signature shape)
- Case 043 (the §10.50 review event embedding this primitive byte form)

## Reproduction

```
python _compute.py
```
