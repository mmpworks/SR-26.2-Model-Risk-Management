# Case 053 — §10.21.3 registry-discovery cross-anchor

## What this case verifies

Spec §10.21.3 normates the registry-discovery cross-anchor pattern: an originating institution publishes a cross-anchor to a third-party registry; a counterpart institution retrieves it. The Federal Reserve's voluntary cross-institution-anchor registry for Fedwire and ACH (§10.71) is the canonical instance; future analogs include SWIFT-mediated international-wire registries, FedNow instant-payment registries, FINRA broker-dealer trade-reporting registries, CCP-cleared-derivatives chain registries, and credit-bureau-mediated cross-institution-correlation registries.

This case pins **two of the three** normative `cross_anchor_state` values:

- `bound` — both originating and counterpart sides published; cross-anchor verifiable at the registry; verifier emits PASS with `registry_cross_anchor_verified`.
- `unbound` — counterpart institution non-participating in the registry; verifier emits PASS with `cross_anchor_unbound` and the institution's CC8.1 documents the non-participation as a residual.

The third state — `published-pending-counterpart` (originating side published; counterpart not yet published or non-participating) — is **NOT** exercised in this vector per the PRD-3 index scope ("two of the three normative `cross_anchor_state` values"; the third state is a V3 follow-up).

## What this case does NOT verify

The registry walk arithmetic itself — fetching the registry publication by id, verifying the registry's signature on the publication receipt, hash-equivalence at the registry — is verifier-implementation behavior; case 053 pins the **cross-anchor attribute-set byte form** and the verifier verdict, not the registry walk.

The `published-pending-counterpart` state is deliberately deferred. Per spec §10.21.3 lines 2543-2545, that state surfaces an anomaly line under `Status: PASS` indicating the binding is in flight; pinning the anomaly-line byte form is a V3 follow-up budget item.

The registry SLA (typically 90 seconds post-settlement for Fedwire) is institution-side discipline named by CC8.1; case 053 pins the chain-entry byte form, not the SLA enforcement.

## Inputs

Two cross-anchor entries — one in `bound` state and one in `unbound` state — using a synthetic Federal Reserve Fedwire registry as the canonical instance.

### Shared inputs

| Field | Value |
|---|---|
| `registry_identity` | `federal-reserve-fedwire-registry` |
| `registry_publication_at_utc` | `2026-05-21T15:30:00Z` |

### Bound variant

| Field | Value |
|---|---|
| `registry_publication_id` | `fed-fedwire-xanchor-2026-05-21-pub-NBFS-cape-001` |
| `counterpart_institution` | `cape-madeline-bank-and-trust` |
| `cross_anchor_state` | `bound` |
| verdict marker | `registry_cross_anchor_verified` |

### Unbound variant

| Field | Value |
|---|---|
| `registry_publication_id` | `fed-fedwire-xanchor-2026-05-21-pub-NBFS-orphan-002` |
| `counterpart_institution` | `non-participating-receiver-institution-XYZ` |
| `cross_anchor_state` | `unbound` |
| verdict marker | `cross_anchor_unbound` |

The §10.21.3 attribute schema (spec lines 2537-2543):

| Attribute | Type | Required | Description |
|---|---|---|---|
| `audit.registry_discovery.registry_identity` | string | yes | Stable identifier of the registry operator |
| `audit.registry_discovery.registry_publication_id` | string | yes | Registry-issued identifier under which the cross-anchor is published |
| `audit.registry_discovery.registry_publication_at_utc` | timestamp | yes | RFC 3339 UTC timestamp of registry publication |
| `audit.registry_discovery.counterpart_institution` | string | when applicable | Stable identifier of the counterpart institution |
| `audit.registry_discovery.cross_anchor_state` | string | yes | Enum: `published-pending-counterpart`, `bound`, `unbound` |

JCS sorts keys lexicographically. Canonical key order: `audit.registry_discovery.counterpart_institution`, `audit.registry_discovery.cross_anchor_state`, `audit.registry_discovery.registry_identity`, `audit.registry_discovery.registry_publication_at_utc`, `audit.registry_discovery.registry_publication_id`.

## Expected canonical bytes

| Sub-form | Length | Canonical SHA-256 |
|---|---:|---|
| `bound_cross_anchor` | 397 | `d96d42585d2996b86430501f471cabb1e7061d01fa0f70ca7f657b83ed2b637e` |
| `bound_verdict` | n/a | `94499b150bb60e28a93268d4ac2f285428ced3bff31095b397a7aaa3edbe0c23` |
| `bound_composed` | n/a | `7d63bde56591d902e2439786a3f28dfe72f474597fb3eed92015bd4f2110bf30` |
| `unbound_cross_anchor` | 415 | `33d7c08f8ad21aacfdcf29afd8d2f7a5d0d9447ace26e25a7a2754f6e2d8d0b1` |
| `unbound_verdict` | n/a | `c9240ff4ebf7d393a25178408a4b510255438c1fd3e04d573ae5a1a14c438dc4` |
| `unbound_composed` | n/a | `af734b43376d47e3f6626f1996a01b8b48fc84b84b93bda4f5876a7055f79708` |

`expected_canonical.txt` carries the two composed-record byte forms separated by a single LF (bound first, then unbound). A reader splits on LF to recover each variant.

## Conformance behavior

A conforming implementation supporting §10.21.3:

1. Constructs each cross-anchor entry as a JSON object carrying the five `audit.registry_discovery.*` attributes per the schema above (the fourth, `counterpart_institution`, is `when applicable` — present in both variants here per the spec's documented-residual discipline).
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to the corresponding `expected_canonical.txt` segment.
3. On `cross_anchor_state == "bound"`, performs registry-discovery, confirms both sides' chain entries are present and hash-equivalent, emits the §10.12 verdict with `exit_code = 0` and `additional_verifications = ["registry_cross_anchor_verified"]`.
4. On `cross_anchor_state == "unbound"`, emits the §10.12 verdict with `exit_code = 0` and `additional_verifications = ["cross_anchor_unbound"]`; the institution's CC8.1 documents the receiving-institution non-participation as a residual.
5. On `cross_anchor_state == "published-pending-counterpart"` (NOT exercised here), emits an anomaly line under `Status: PASS` indicating the binding is in flight. Byte form is a V3 follow-up.

## Composition with other cases

- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin. Case 036 lists both `cross_anchor_unbound` and `registry_cross_anchor_verified`-class markers in its `known_additional_verifications` enumeration; case 053 pins the verdict byte forms for those specific markers.
- §10.71 cross-institution wire chain — the canonical Phase-14 consumer of §10.21.3. Future vectors 081 (`cross-institution-fedwire-cross-anchored`, `bound` state) and 082 (`cross-institution-fedwire-cross-anchor-unbound`, `unbound` state) compose §10.21.3 with the §10.71 operational context; case 053 pins the underlying registry-discovery primitive.

## Cross-references

- Spec §10.21.3 — registry-discovery pattern for cross-institution cross-anchors (the section this case proves out)
- Spec §10.12 — verifier exit-code contract; `additional_verifications` discipline
- Spec §10.71 — cross-institution wire chain (Fedwire / ACH; the canonical §10.21.3 consumer)
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin
- RFC 8785 (JCS canonicalization)
- RFC 3339 (timestamp format for `registry_publication_at_utc`)
- Federal Reserve Operating Circular 6 (Fedwire)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
