# N032 — GAP-5 HITL signature does not verify under declared reviewer key

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the GAP-5 HITL primitive's signature integrity claim: the `signature_b64` MUST verify under the public key resolved from `reviewer_id` against the institution's CC8.1-named registry, AND the recovered signing-key fingerprint MUST match `reviewer_public_key_fingerprint`. Mismatch is a chain-integrity failure.

## Tampering recipe

Start from cases 043 + 044. Modify ONE of:

**Variant A — signature substitution:** Replace the `signature_b64` with a signature produced by a different reviewer's key. The signature does not verify under the declared `reviewer_id`'s registered public key.

**Variant B — fingerprint mismatch:** Replace the `reviewer_public_key_fingerprint` with a different SHA-256 hex string while leaving the signature intact. The fingerprint declared on the chain entry does not match the public key resolved from `reviewer_id`.

**Variant C — payload tampering:** Modify a field on the §10.50 review event (e.g., change `outcome` from `grounding_pass` to `grounding_fail`) without re-signing. The original signature still appears on the chain entry but no longer verifies against the canonical bytes whose hash is `signed_payload_sha256`.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: GAP-5 HITL signature failure: <variant-specific reason>
  - Variant A: signature does not verify under declared reviewer's public key
  - Variant B: reviewer_public_key_fingerprint on chain entry does not match the public key resolved from the institution's reviewer-key registry
  - Variant C: signed_payload_sha256 does not match the recomputed SHA-256 of the canonical bytes of the review payload (post-hoc tampering with review-event attributes)
additional_verifications: []
```

## What this case proves

The HITL primitive's three integrity surfaces — (a) signature verifies under declared key, (b) declared fingerprint matches registry-resolved key, (c) signed payload hash matches canonical-bytes recomputation — close the failure modes where an institution claims a clinician's review without producing a valid signed review, OR tampers with the review-event content post-signing.

The §10.55 audit-target challenge-response section reuses this primitive, so this negative case's fixes apply to both consumers.

## Cross-references

- Spec GAP-5 HITL primitive
- Spec §10.50 output-grounding event family
- Case 043 (the §10.50 review event embedding the signed-review primitive)
- Case 044 (the GAP-5 primitive standalone)
