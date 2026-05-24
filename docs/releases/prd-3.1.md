---
title: "PRD-3.1 Release Notes"
release: "PRD-3.1"
document-version: "0.3.0"
date: 2026-05-24
status: "SHIPPED"
---

# PRD-3.1 Release Notes

PRD-3.1 closes the reference-implementation gap for three attribute families that PRD-3 normated but flagged FORTHCOMING. The spec document version remains 0.3.0. No normative text changed. The wire-format identifier remains v1.

PRD-3 (tagged `prd-3`) shipped the normative spec text for sections 14.6, 14.7, and 14.8 with a Path A flag: "NORMATIVE -- REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1." PRD-3.1 removes that flag. The three families now carry "SHIPPED" status across C# (Herald.Compliance), Python (Herald.Py), and Go (ffiec verifier), with 35 new conformance vectors pinning byte-identical output across all three implementations.

---

## What shipped

### 1. Three attribute families -- cross-implementation reference code

**Section 14.6: `audit.actor.*` (Seam D -- authenticated human identity)**

Captures the SSO-authenticated human whose session triggered the chain entry. Complements the SDK-side workload-identity capture (section 4.1.1 SPIFFE / mTLS / HSM bearer). Four attributes: `authenticated_user_id_hash` (SHA-256 hex), `authentication_method` (seven-value closed enum), `session_id` (recommended), `delegation_chain` (JCS-canonical lex-sorted array of delegated-authority pairs).

Implementations:
- C#: `Herald.Compliance.AuditActor.BuildActorEvent(...)`
- Python: `herald.build_actor_event(...)`
- Go verifier: `verify.ValidateActorAttributes(...)`

**Section 14.7: `audit.reasoning.substrate_kind` (Seam B -- reasoning architecture marker)**

Stratifies the reasoning behind an AI decision by architecture class. Seven-value closed enum carrying a trust gradient from `neurosymbolic` (policy text IS the reasoning) to `post_hoc_llm_rationalization` (LLM-generated after the decision). Single attribute: `substrate_kind`.

Implementations:
- C#: `Herald.Compliance.ReasoningSubstrate.BuildReasoningEvent(...)`
- Python: `herald.build_reasoning_event(...)`
- Go verifier: `verify.ValidateReasoningAttributes(...)`

**Section 14.8: `audit.downstream_action.*` (generalized system-of-record linkage)**

Records what the system did downstream after the decision. Four required attributes: `action_kind` (institution-named), `system_of_record_id`, `change_record_id_hash` (SHA-256 hex), `applied_at_utc` (RFC 3339 UTC with Z suffix).

Implementations:
- C#: `Herald.Compliance.DownstreamAction.BuildDownstreamActionEvent(...)`
- Python: `herald.build_downstream_action_event(...)`
- Go verifier: `verify.ValidateDownstreamActionAttributes(...)`

All three implementations produce byte-identical JCS-canonical JSON (RFC 8785) for the same inputs. The Go verifier dispatches attribute validation as an additive check in the section 10.12 `additional_verifications` array. Attribute validation failures do not gate the core structural + MAC verification pass.

### 2. Kognitos-projection library

`Herald.Compliance.KognitosProjection` maps TesseraSeal chain entry attributes into the Kognitos 12-field AI decision-logging framework. One call, no configuration, produces a `KognitosRecord` or JSON-ready dictionary. Demonstrates by construction that TesseraSeal is a superset of Kognitos: every Kognitos field has a source in TesseraSeal, but TesseraSeal carries attributes (delegation chains, substrate kinds, Merkle seals, ECOA/GDPR-specific bindings) that Kognitos does not model.

The projection is read-only. It does not modify chain data. It is a lens, not a transform.

See: `Herald.Compliance/docs/kognitos-projection.md`

### 3. 35 new conformance vectors (050-084)

Coverage by spec section and family:

| Vector range | Section | What they pin |
|---|---|---|
| 050-059 | 14.6 `audit.actor.*` | Happy-path, all-authentication-method enum, delegation-chain (single + multi-sorted), empty-delegation-chain, SHA-256 hex validation, invalid-method rejection, malformed-hash rejection, missing-required-field rejection, composition with section 10.50 signed-review |
| 060-066 | 14.7 `audit.reasoning.substrate_kind` | All seven enum values, composition with section 10.47 generation four-tuple, invalid-enum rejection |
| 067-074 | 14.8 `audit.downstream_action.*` | Happy-path (account-status-change, payment, record-update, case-disposition), all-action-kinds, system-of-record linkage, missing-field rejection, malformed-hash rejection, wrong-timestamp-format rejection |
| 075-084 | Cross-family composition | All three families on a single entry, HMAC chain integration, Merkle root with attribute-bearing entries, cross-run isolation, Unicode handling, field-length boundary conditions |

Each vector directory contains the canonical five-file structure: `README.md`, `input.json`, `_compute.py`, `expected_canonical.txt`, `expected_canonical_sha256.txt`.

### 4. SDK reference documentation

`Herald.Compliance/docs/sdk-reference-section-14-attributes.md` provides per-family API reference covering attribute types, closed enums, validation rules, and cross-implementation calling conventions for C# and Python.

### 5. Framework-portability capability

`Herald.Compliance/docs/framework-portability.md` documents the architectural property that lets TesseraSeal chain data serve multiple regulatory frameworks without re-engineering. Three properties make this work: attributes are additive (CUPID Composable), the chain layer is framework-neutral, and projections are read-only lenses.

Proof-by-construction: the Kognitos projection library is the first projection built on this architecture. Building a second projection for a different framework follows the same pattern with no changes to the chain layer.

### 6. Phase 2 vectorgen primitives

The TesseraSeal VectorCompiler (0.3.0) shipped Shape-A (complete) and the Phase 2 `sign_payload` primitive seam. These primitives support the next wave of conformance-vector generation. The VectorCompiler is MMPWorks-proprietary tooling; its outputs (test vectors) are Apache-2.0.

### 7. Shift runbook

`Herald.TesseraSeal.VectorCompiler/docs/shift-runbook.md` documents the operational procedure for generating, validating, and publishing conformance vectors from the VectorCompiler.

---

## Spec status updates

Section 14.12 open-items table updated:
- **O-4 (SHIPPED)**: All three section 14 attribute families implemented and pinned.
- **O-6 (SHIPPED)**: Test vectors 049-053 (Phase 11 shared primitives) materialized.
- O-1, O-2, O-3, O-5, O-7 remain FORTHCOMING.
- O-8 (cross-institution registry) remains EXOGENOUS.

Section 14.6 / 14.7 / 14.8 status lines updated from "REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1" to "SHIPPED -- C# + Python + Go + conformance vectors."

Section 14.10 cross-reference summary table rows updated with SHIPPED status.

---

## Go verifier (ffiec repo)

The Go verifier on branch `feat/prd-3.1-section-14-predicates` (commit `64ba771`) adds:
- `verifier/internal/verify/attributes.go` -- type definitions for the three attribute families
- `verifier/internal/verify/predicates.go` -- `ValidateActorAttributes`, `ValidateReasoningAttributes`, `ValidateDownstreamActionAttributes`, `ValidateEventAttributes`, `ParseEventAttributes`
- `verifier/internal/verify/predicates_test.go` -- 62 test cases covering happy-path and negative scenarios for all three families
- `verifier/internal/verify/attributes_integration_test.go` -- 40 integration tests covering cross-family composition, HMAC chain integration, delegation chain sorting, and field-level edge cases
- Additive attribute validation in the verification pipeline (`pipeline.go`) via `validateChainAttributes` -- produces `AdditionalVerification` entries without gating core structural/MAC verification

The branch is a clean two-commit fast-forward on top of `main`. 102 verifier tests pass (184 total across the workspace).

---

## What did not change

- **Document version**: remains 0.3.0. PRD-3.1 is a sub-release, not a new document version.
- **Wire-format identifier**: remains v1. All PRD-3.1 additions are additive.
- **Normative spec text**: no conformance requirements changed. The sections read the same. The status markers changed from FORTHCOMING to SHIPPED.
- **PRD-3 sections 14.0 through 14.5**: untouched.
- **PRD-3 sections 14.9 through 14.11**: untouched.
- **Existing test vectors (001-049)**: untouched.
- **Existing negative vectors (N001-N029)**: untouched.

---

## Tag plan

| Repository | Tag | Commit | Notes |
|---|---|---|---|
| ffiec-public | `prd-3.1` | (pending: commit the spec status updates first) | Status-table-only changes to `chain-of-custody-DRAFT-0.3.0.md` |
| ffiec | `prd-3.1` | (pending: merge `feat/prd-3.1-section-14-predicates` to `main` first) | Go verifier attribute-family predicates |

Both tags pending Steve's approval to merge/commit.
