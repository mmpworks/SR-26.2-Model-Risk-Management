# Case 052 — §10.21.2 parallel-evaluator composition

## What this case verifies

Spec §10.21.2 normates the parallel-evaluator composition pattern: two or more independent parties evaluate the same subject, each operating its own chain, with the chains composing at a target-anchor boundary via a §10.21.2 cross-anchor entry. Canonical instances: lab-internal + AI Safety Institute parallel evaluation chains anchored at the target-model-weights chain entry (§10.67); cedent + reinsurer parallel chains anchored at the claim-handover (§10.45); institutional clinical + Cleveland Clinic observer chains anchored at output-grounding (§10.50); deployer + independent third-party adjuster chains (§10.45 base case).

This case pins the byte forms for the **lab + AISI cardinality-2 known-cardinality regime** anchored at target-model-weights. Both evaluators present; coverage matches declared cardinality; verifier emits PASS with `parallel_evaluator_anchor_verified`.

Three byte-forms are pinned:

1. The §10.21.2 cross-anchor attribute set for the lab evaluator.
2. The §10.21.2 cross-anchor attribute set for the AISI evaluator.
3. The composed record carrying both evaluators plus the §10.12 verdict the verifier emits on PASS.

## What this case does NOT verify

The cross-anchor walk arithmetic itself — recomputing the hash-binding from the evaluator's chain bytes and comparing to the value bound on the §10.21.2 entry — is verifier-implementation behavior; case 052 pins the **attribute-set byte form** the verifier walks, not the walk itself.

The dynamic-cardinality regime (`cardinality = "dynamic"`) is not exercised here. Case 052 pins the cardinality-2 known-cardinality regime; a future vector should pin the dynamic-cardinality byte form.

The two §10.21.2 failure modes — **target anchor unresolved** and **hash-binding mismatch** — are control-completeness anomalies the verifier emits under `Status: PASS` (chain integrity is structurally intact; the cross-anchor walk found a divergence). Those failure paths are negative-case candidates for future N0XX vectors.

## Inputs

A synthetic lab + AISI parallel-evaluator chain anchored at a synthetic target-model-weights chain entry.

| Field | Value |
|---|---|
| `target_anchor_chain_entry_id` | `target-model-weights-chain-entry-2026-05-21-frontier-model-v3-deploy` |
| `cardinality` | `2` (known-cardinality regime) |
| Lab `evaluator_identity` | `lab-internal-eval` |
| Lab `evaluator_role` | `regulatory-equivalent` |
| Lab `evaluator_chain_entry_id` | `evaluator-chain-entry-2026-05-21::lab-internal-eval` |
| AISI `evaluator_identity` | `aisi-program-evaluation` |
| AISI `evaluator_role` | `regulatory-equivalent` |
| AISI `evaluator_chain_entry_id` | `evaluator-chain-entry-2026-05-21::aisi-program-evaluation` |

The §10.21.2 attribute schema (spec lines 2514-2521) — each cross-anchor entry carries:

| Attribute | Type | Required | Description |
|---|---|---|---|
| `audit.parallel_evaluator.evaluator_identity` | string | yes | Stable identifier of the evaluator |
| `audit.parallel_evaluator.evaluator_role` | string | yes | Enum: `regulatory-equivalent`, `independent-third-party`, `co-evaluator`, `observer` |
| `audit.parallel_evaluator.target_anchor_chain_entry_id` | string | yes | Chain-entry id of the subject being evaluated |
| `audit.parallel_evaluator.evaluator_chain_entry_id` | string | when applicable | Evaluator's chain-entry identifier |
| `audit.parallel_evaluator.cardinality` | integer or string | yes | Positive integer (known-cardinality) or `"dynamic"` |

JCS sorts keys lexicographically. Canonical key order: `audit.parallel_evaluator.cardinality`, `audit.parallel_evaluator.evaluator_chain_entry_id`, `audit.parallel_evaluator.evaluator_identity`, `audit.parallel_evaluator.evaluator_role`, `audit.parallel_evaluator.target_anchor_chain_entry_id`.

## Expected canonical bytes

| Sub-form | Length | Canonical SHA-256 |
|---|---:|---|
| `lab_cross_anchor` | 407 | `831de5f3ad489804dfcae0af5b76afb882b1a96cd5e8eef37a031ddd4ae7fb76` |
| `aisi_cross_anchor` | 419 | `47193d870c68b226f707b65879af7a0d953bdc3ef43b456f284bf562b463a354` |
| `verdict` | 286 | `a97fea0bf03e41f9e5dc22740b2c0a3b6b245d77d9cfd1c90e6dd98d5ed0c620` |
| `composed_record` | 1293 | `bf9b665be389679006cf3ff698b964bca0b77d89d4ab554a443a82a73fb23abf` |

`expected_canonical.txt` carries the composed-record bytes as the primary byte-form pin (it carries both per-evaluator entries plus the verdict inside it). The per-sub-form SHA-256s in `expected_canonical_sha256.txt` allow granular comparison.

## Conformance behavior

A conforming implementation supporting §10.21.2:

1. Constructs each evaluator's cross-anchor entry as a JSON object carrying the five `audit.parallel_evaluator.*` attributes per the schema above (the fifth, `evaluator_chain_entry_id`, is `when applicable` — present here because both evaluators run TesseraSeal-conformant chains).
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to the corresponding `expected_canonical.txt` segment.
3. On §10.21.2 PASS (both evaluator chains resolved; hash-binding verified at the target-anchor boundary; cardinality matches), emits the §10.12 verdict with `exit_code = 0` and `additional_verifications = ["parallel_evaluator_anchor_verified"]`.
4. When cardinality is present and discovered evaluators are fewer than cardinality, emits the §7 anomaly line `parallel-evaluator coverage incomplete: declared cardinality {N}, observed {M}` under `Status: PASS`. This vector pins the all-evaluators-present case; the coverage-incomplete shape is not exercised here.
5. When `cardinality == "dynamic"`, MUST NOT perform an inline coverage check. The dynamic regime is not exercised in this vector.

## Composition with other cases

- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin. Case 036 lists `parallel_evaluator_anchor_verified` in its `known_additional_verifications` enumeration; case 052 pins the verdict byte form for that specific marker.
- §10.45 (`039-adjuster-anchor-bidirectional/`) — the original §10.21.2 instance for the deployer + independent adjuster pattern.
- Future Phase 13 case 075 — `evaluation-chain-parallel-lab-aisi` — exercises §10.21.2 in the AISI Reference Evaluation Program operational context; case 052 pins the underlying cross-anchor primitive that case 075 composes with.

## Cross-references

- Spec §10.21.2 — independent-evaluator parallel-chain composition (the section this case proves out)
- Spec §10.12 — verifier exit-code contract; `additional_verifications` discipline
- Spec §10.45 — independent third-party adjuster anchor
- Spec §10.50 — output-grounding event (clinical observer §10.21.2 instance)
- Spec §10.60 — anti-counterfeit cross-anchor (§10.21.2 instance)
- Spec §10.67 — pre-deployment evaluation chain (the canonical Phase-13 consumer)
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin
- Case 039 (`039-adjuster-anchor-bidirectional/`) — original §10.21.2-style bidirectional anchor pattern
- RFC 8785 (JCS canonicalization)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
