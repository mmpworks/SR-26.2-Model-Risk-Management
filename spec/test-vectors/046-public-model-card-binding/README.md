# Case 046 — Public model-card binding (§10.52)

## What this case verifies

Spec §10.52 is a normative narrative wrapper around §10.19. Public model-card publications hash-anchor the model card via `audit.external_artifact.*` with the institution-named kind value `"model_card"`. NO new event family — pure §10.19 reuse with the canonical kind discriminator.

## Inputs

| §10.19 attribute | Value |
|---|---|
| `kind` | `model_card` |
| `identifier` | `helvetian-vat-audit-target-model-2026-04` |
| `sha256` | `ea3bb5b10902eb8bd5008c4698060a86a350eeb30d28e3ae8bc1a0c425917297` |
| `received_at_utc` | `2026-04-15T08:00:00Z` |
| `source_party` | `helvetian-federal-tax-authority` |
| `evidentiary_role` | `public_model_card_publication` |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `438` |
| canonical SHA-256 | `21183a9e8be95ae8fbfb82171a05ee28e9066c7ea76b5354756754b4e461306f` |

## Conformance behavior

The §10.52 event uses the existing §10.19 schema unchanged. A conforming implementation:

1. Constructs the event using `audit.external_artifact.*` attributes.
2. Sets `kind = "model_card"` and `evidentiary_role = "public_model_card_publication"` (the §10.52 canonical values).
3. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.

## Why no new event family

§10.52 reuses §10.19 to avoid duplicating infrastructure for what is structurally identical to other external-artifact anchors (foreign-vendor PDFs, contract documents, signed reports). The institution-named `kind = "model_card"` discriminator lets a verifier or auditor select model-card events from the chain without out-of-band metadata.

## Cross-references

- Spec §10.52 public model-card binding
- Spec §10.19 audit.external_artifact.* (the substrate)
- Spec §10.21 cross-vendor model-handover (the handover-time companion via `audit.model_handover.model_card_sha256`)
- Design `docs/design/15-civic-ai-and-post-quantum.md` §4

## Reproduction

```
python _compute.py
```
