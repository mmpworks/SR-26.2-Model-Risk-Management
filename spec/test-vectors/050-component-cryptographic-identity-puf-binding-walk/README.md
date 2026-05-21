# Case 050 — §10.58 PUF binding-walk

## What this case verifies

Spec §10.58 normates the component-cryptographic-identity primitive: four identity-kinds (`puf-response`, `seal-chiplet-attestation`, `factory-provisioned-key`, `serial-lot-hash`) plus a binding-hash construction rule plus a two-mode verifier dispatch (binding-walk and challenge-walk).

This case pins the **binding-walk** path for the `puf-response` identity-kind. The binding-walk verifier does NOT require the component to be in-hand; it walks the chain entry's identity-binding hash and confirms the binding is structurally present and integrity-bound by the per-event MAC. The challenge-walk path (component in-hand) is covered by case 051.

Two byte-forms are pinned:

1. The JCS-canonical bytes of the §10.58 `canonical_binding_input` JSON object — the input whose SHA-256 IS the 32-byte binding-hash.
2. The §10.12 verdict object the verifier emits on binding-walk PASS: `exit_code = 0`, `additional_verifications = ["component_identity_binding_walk_verified"]`.

## What this case does NOT verify

PUF hardware behavior, the cryptographic strength of any specific PUF construction, manufacturer-issued attestation chains, or the operational sampling discipline are all out of scope. Case 050 pins the **byte form** of the binding-input and verifier output; the cryptographic + operational layers are addressed by §10.58 spec text and the institution's CC8.1.

The `factory-provisioned-key`, `seal-chiplet-attestation`, and `serial-lot-hash` identity-kinds are not exercised here. Per the §10.58 cross-reference, vectors 058 and 059 cover the SHIELD chiplet-attestation and factory-provisioned-key byte forms (Phase 12 wave).

## Inputs

A synthetic PUF identity binding for an institution-named component. Values are deterministic; the recipe is documented inline in `_compute.py` so any reader can recompute byte-for-byte.

| Field | Value |
|---|---|
| `identity_kind` | `puf-response` |
| `component_id` | `as6171-sample-component-2026-05-21-001` |
| `puf_challenge_id` | `darpa-shield-puf-challenge-class-A-2026-05` |
| `puf_response_hex` | `SHA-256("050-puf-response::component=<component_id>::challenge=<challenge_id>")` |

The §10.58 `canonical_binding_input` JSON object schema (spec lines 3597-3603):

```json
{
  "identity_kind": "puf-response",
  "component_id": "<string>",
  "puf_challenge_id": "<string>",
  "puf_response_hex": "<lowercase-hex string of the raw response bytes>"
}
```

JCS sorts keys lexicographically. Canonical key order: `component_id`, `identity_kind`, `puf_challenge_id`, `puf_response_hex`.

## Expected canonical bytes

| Sub-form | Length | Canonical SHA-256 |
|---|---:|---|
| `canonical_binding_input` | 238 | `8ba3334374f19abc8fab7ac00cf041bc1b9f99c546a7ee68d7c40a0e4de6b753` |
| `binding_hash_hex` | n/a (32 raw bytes) | `8ba3334374f19abc8fab7ac00cf041bc1b9f99c546a7ee68d7c40a0e4de6b753` |
| `verdict` | 292 | `cab215be0fd340c0be841c4bb437ac4af7a4721de7200b1939489faf0a6b6da5` |

`expected_canonical.txt` carries the binding-input bytes followed by a single LF and then the verdict bytes; a reader splits on LF to recover each sub-form.

The binding-hash IS the SHA-256 of the binding-input bytes — they're the same 64-character hex digest, listed twice in the SHA-256 file so a clean-room implementer comparing against the chain-entry-stamped `cryptographic_identity.binding_hash` value gets a direct match.

## Conformance behavior

A conforming implementation supporting §10.58:

1. Constructs the `canonical_binding_input` JSON object with the four fields above per the spec §10.58 lines 3597-3603 schema.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to the binding-input portion of `expected_canonical.txt`.
3. Computes the 32-byte binding-hash as `SHA-256(JCS(canonical_binding_input))`; the lowercase-hex form MUST match `binding_hash_hex`.
4. On binding-walk PASS, emits the §10.12 verdict object with `exit_code = 0` and `additional_verifications = ["component_identity_binding_walk_verified"]`. JCS-canonicalizing the verdict produces bytes byte-identical to the verdict portion of `expected_canonical.txt`.
5. The verifier does NOT require the component to be in-hand for binding-walk; it walks the chain entry's binding hash and per-event MAC integrity only.

## Composition with other cases

- Case 051 (`051-component-cryptographic-identity-puf-challenge-walk/`) — uses the SAME synthetic component and the SAME `canonical_binding_input` bytes; pins the challenge-walk verdict and the mocked PUF challenge-response oracle output. The binding-input SHA-256 is byte-identical between cases 050 and 051 by design.
- Case 036 (`036-verdict-additional-verifications/`) — the §10.12 verdict-object byte-form pin in the general case. Case 050's verdict byte form is distinct because the `additional_verifications` array carries `component_identity_binding_walk_verified` (a marker case 036 does not pin in isolation).
- Future case 058 — `seal-chiplet-attestation` identity-kind binding-input byte form (Phase 12).
- Future case 059 — `factory-provisioned-key` identity-kind binding-input byte form (Phase 12).

## Cross-references

- Spec §10.58 — component cryptographic identity primitive (the section this case proves out)
- Spec §10.12 — verifier exit-code contract; `additional_verifications` discipline
- Spec §10.56 — HBOM chain (the canonical §10.58 consumer)
- Case 051 (`051-component-cryptographic-identity-puf-challenge-walk/`) — the challenge-walk companion
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin
- RFC 8785 (JCS canonicalization)
- DARPA SHIELD program documentation
- ISO/IEC 20897 (PUF security requirements)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
