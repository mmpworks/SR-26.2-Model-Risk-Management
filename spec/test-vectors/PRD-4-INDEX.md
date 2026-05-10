# PRD-4 test-vector index — vectors 049-083

> **What this doc is.** Forward-looking index of the 35 conformance test vectors that ship with the PRD-4 §10.56-§10.71 wave plus the §0.6 Navigation, §7 unknown-wire-format-kind fallthrough, and §10.21 amendments. Per-vector directories under `spec/test-vectors/049-...` through `spec/test-vectors/083-...` materialize during Phase 11-14 implementation in HPy and HCp.Chain. This index lists each vector's purpose, inputs, normative reference, and cross-references so the implementation phase has a single source of truth for the vector budget and verifier-mode coverage.
>
> **Vector count, by phase:** Phase 11 (shared primitives + spec-text scaffolding): 5 vectors (049-053). Phase 12 (Story 18 hardware + red/black): 11 vectors (054-064). Phase 13 (Story 19 frontier-AI training-provenance): 12 vectors (065-076). Phase 14 (Story 20 banking institutional): 7 vectors (077-083). Total: 35 vectors. Auditor BLOCKER #1 + #2 (test-vector renumbering collisions in Rev 1 of the manifest) closed by this allocation.

---

## Phase 11 — shared primitives (vectors 049-053)

### 049 — `unknown-wire-format-kind-fallthrough`

**Verifies.** §7 unknown-wire-format-kind fallthrough rule. PRD-3 verifier ingesting a chain with a §10.62 cross-domain transition record produces `Status: PASS` with anomaly line `unknown wire-format kind present: cross_domain_transition (count: 1)` and `additional_verifications: ['unknown_kind_present']`. Verifier exit code is `0` per §10.12's additional-verifications discipline; the marker is the dispatch surface, and institutions requiring stricter posture treat the marker as a non-PASS condition out-of-band per §7 step 5 (see §7 lines 994-996).

**Inputs.** A chain entry plus a §10.62 cross-domain transition record under format_version `"v1"`. The verifier is built before §10.62 was specified; it has no semantic interpretation of the cross-domain kind.

**Cross-reference.** §7 unknown-wire-format-kind fallthrough; §10.12 verifier exit-code contract (additional-verifications discipline); §10.62.

### 050 — `component-cryptographic-identity-puf-binding-walk`

**Verifies.** §10.58 binding-walk verifier mode for a PUF-class identity. The chain entry's `cryptographic_identity` carries an `identity_kind = "puf-response"` plus a binding hash; the verifier confirms the binding-hash structurally without challenging the component, exits `0` (PASS) with `additional_verifications: ['component_identity_binding_walk_verified']` per §10.58.

**Inputs.** §10.58 chain entry with PUF identity-kind; reference PUF response hash.

**Cross-reference.** §10.58; §10.12 verifier exit-code contract (additional-verifications discipline); §10.56 HBOM consumer; design doc 16.

### 051 — `component-cryptographic-identity-puf-challenge-walk`

**Verifies.** §10.58 challenge-walk verifier mode for a PUF-class identity. The verifier challenges the component (mocked in fixture) with a PUF challenge, validates response against the bound expected response, exits `0` (PASS) with `additional_verifications: ['component_identity_challenge_walk_verified']` per §10.58. The marker is the dispatch surface for tooling that requires challenge-walk for a particular regulatory regime.

**Inputs.** §10.58 chain entry with PUF identity-kind; mocked PUF challenge-response oracle.

**Cross-reference.** §10.58; §10.12 verifier exit-code contract (additional-verifications discipline).

### 052 — `parallel-evaluator-composition`

**Verifies.** §10.21.2 parallel-evaluator composition. Two independent evaluator chains anchored at one target (e.g., target-model-weights). Verifier confirms hash equivalence at the anchor boundary, exits `0` (PASS) with `additional_verifications: ['parallel_evaluator_anchor_verified']`. Cardinality = 2 (known-cardinality regime).

**Inputs.** Two parallel evaluation chain entries plus a §10.21.2 cross-anchor binding them at the target boundary.

**Cross-reference.** §10.21.2; §10.45, §10.50, §10.60, §10.67 (consumers).

### 053 — `registry-discovery-cross-anchor`

**Verifies.** §10.21.3 registry-discovery cross-anchor. Originating-side chain entry publishes to a mocked registry; counterpart-side chain entry references the registry publication. The vector covers two of the three normative `cross_anchor_state` values: in the `bound` state the verifier confirms hash equivalence at the registry and exits `0` (PASS) with `additional_verifications: ['registry_cross_anchor_verified']`; in the `unbound` state (counterpart institution non-participating) the verifier exits `0` (PASS) with `additional_verifications: ['cross_anchor_unbound']` and the institution's CC8.1 documents the non-participation as a residual. The third state (`published-pending-counterpart`) is not exercised in this vector — see V3 follow-up note.

**Inputs.** Originating chain entry; mocked registry publication; counterpart chain entry (or absence thereof for the `unbound` variant).

**Cross-reference.** §10.21.3; §10.12 verifier exit-code contract (additional-verifications discipline); §10.71 (consumer).

---

## Phase 12 — Story 18 (vectors 054-064)

### 054 — `hbom-incoming-test-clean-lifecycle`

**Verifies.** §10.56 `audit.hbom.incoming_test` event with §10.58 `cryptographic_identity` binding. Chain entry produced at incoming-test pass; verifier emits `additional_verifications: ['hbom_lifecycle_verified']`.

**Cross-reference.** §10.56; §10.58.

### 055 — `hbom-fru-integration-with-cross-anchor`

**Verifies.** §10.56 `audit.hbom.fru_integration` event with cross-anchor to original incoming-test entry. Lifecycle traversal end-to-end.

### 056 — `firmware-attestation-internal-build`

**Verifies.** §10.57 internal-build path. `audit.firmware.build` and `audit.firmware.activate` events emit on the institution's chain; activation references build directly.

**Cross-reference.** §10.57.

### 057 — `firmware-attestation-cross-supplier-build`

**Verifies.** §10.57 cross-supplier-build path via §10.21 cross-anchor. Activation references supplier's signed attestation document by hash; cross-anchor binding verified.

**Cross-reference.** §10.57; §10.21.

### 058 — `component-identity-seal-chiplet-attestation`

**Verifies.** §10.58 `seal-chiplet-attestation` identity-kind. DARPA SHIELD program chiplet attestation document hash bound to chain entry; verifier dispatches binding-walk only.

**Cross-reference.** §10.58.

### 059 — `component-identity-factory-provisioned-key`

**Verifies.** §10.58 `factory-provisioned-key` identity-kind. Manufacturer-CA-issued certificate chain validated; binding-walk succeeds.

**Cross-reference.** §10.58.

### 060 — `rma-clean-re-entry`

**Verifies.** §10.59 `audit.rma.repair_complete` chain entry with §10.58 identity re-verification. No anomalies flagged.

**Cross-reference.** §10.59.

### 061 — `rma-duplicate-binding-anomaly`

**Verifies.** §10.59 duplicate-binding-anomaly detection. Same `cryptographic_identity` bound to two `incoming_test` entries under different `serial_number` values; verifier emits anomaly line under `Status: PASS`.

**Cross-reference.** §10.59; §10.60 (referral path).

### 062 — `anti-counterfeit-cross-anchor-as6171`

**Verifies.** §10.60 sample-based-attestation cross-anchor for AS6171 destructive testing. Lot-level attestation bound; per-component chain entries inherit transitively.

**Cross-reference.** §10.60; §10.21.1.

### 063 — `red-black-projection-talon-x`

**Verifies.** §10.62 reference releasability-projection (TALON-X program filter). Deterministic projection produces byte-identical releasable-hash from a fixture red-side payload.

**Cross-reference.** §10.62.2; design doc 17.

### 064 — `red-black-black-side-hash-equivalence-walk`

**Verifies.** §10.62 black-side verifier mode. Walks black-side chain entries plus cross-domain transition record's bound releasable-hash; never sees red content; exit code `0` (PASS) with `additional_verifications: ['red_black_black_side_hash_equivalence_verified']`.

**Cross-reference.** §10.62; §10.12 (additional-verifications discipline).

---

## Phase 13 — Story 19 (vectors 065-076)

### 065 — `training-corpus-clean-build`

**Verifies.** §10.63 `audit.training_corpus.shard_ingested` and `index_built` events. Indexed corpus content_hash bound; verifier confirms.

**Cross-reference.** §10.63.

### 066 — `training-corpus-dedup-and-filter-chain`

**Verifies.** §10.63 `dedup_decision` and `filter_pass` events. Chain composes from raw shards through dedup through filters to indexed corpus.

**Cross-reference.** §10.63.

### 067 — `training-run-launch`

**Verifies.** §10.64 `audit.training_run.launch` event with cross-anchors to §10.63 indexed-corpus and §10.65 fleet manifest.

**Cross-reference.** §10.64.

### 068 — `training-run-checkpoint-merkle-aggregation`

**Verifies.** §10.64 per-step Merkle aggregation. RFC 6962 root over per-chassis gradient contributions; byte-identical across HPy and HCp.Chain.

**Cross-reference.** §10.64; §10.65 (Merkle leaf source); RFC 6962.

### 069 — `fleet-attestation-clean-evolution`

**Verifies.** §10.65 chassis attestation with `drift_seen = false`. PCR state evolution matches §10.65.2 expected-state-evolution profile.

**Cross-reference.** §10.65; §10.65.2.

### 070 — `fleet-attestation-authorized-update`

**Verifies.** §10.65 chassis attestation through an authorized firmware update. PCR shift detected and matched to profile; `drift_seen = false` (within profile).

**Cross-reference.** §10.65.2.

### 071 — `fleet-attestation-unexplained-shift`

**Verifies.** §10.65 chassis attestation diverging from profile. `drift_seen = true`; `audit.fleet.chassis_quarantined` event emitted.

**Cross-reference.** §10.65.

### 072 — `model-weight-lineage-linear`

**Verifies.** §10.66 linear lineage (pre-training → SFT → RLHF → deployed). Lineage DAG walks back to root cleanly; lineage_root_hash bound at deployment.

**Cross-reference.** §10.66.

### 073 — `model-weight-lineage-merge-transition`

**Verifies.** §10.66 merge-pattern lineage. Two parent checkpoints merge via interpolation; multi-parent transition recorded; DAG walk produces complete lineage.

**Cross-reference.** §10.66.

### 074 — `evaluation-chain-single-evaluator`

**Verifies.** §10.67 `audit.evaluation.run`, `result`, `disposition` events for a lab-internal evaluation cycle.

**Cross-reference.** §10.67.

### 075 — `evaluation-chain-parallel-lab-aisi`

**Verifies.** §10.67 parallel-evaluator composition via §10.21.2. Lab and AISI parallel evaluation chains anchored at target-model-weights; verifier emits both `evaluation_chain_verified` and `parallel_evaluator_anchor_verified`.

**Cross-reference.** §10.67; §10.21.2.

### 076 — `aisi-overlay-submission-verifier-dispatch`

**Verifies.** §10.68 AISI submission packet verifier dispatch. Control-by-control PASS/FAIL against the §10.63-§10.67 chain entries; submission receipt cross-anchored back into lab's chain.

**Cross-reference.** §10.68.

---

## Phase 14 — Story 20 (vectors 077-083)

### 077 — `customer-disclosure-hkdf-derivation`

**Verifies.** §10.69 per-customer-disclosure HKDF derivation. The session key derives byte-identically from `info = HKDF_INFO_BASE || '|' || utf8(tenant_id) || '|' || utf8('customer-disclosure') || '|' || utf8(customer_correlation_index)`; cross-implementation byte equivalence.

**Cross-reference.** §10.69.

### 078 — `customer-disclosure-subtree-with-exception-list`

**Verifies.** §10.69 customer-side independent verification. Customer's verifier reproduces per-event MACs from disclosure packet; emits `customer_disclosure_subtree_verified` and `customer_disclosure_key_derivation_verified`. `disclosure_complete_excepting: ['sar', 'privileged_investigation']` documented.

**Cross-reference.** §10.69; §10.70 (the exclusion source).

### 079 — `privileged-investigation-cleared-mode`

**Verifies.** §10.70 SAR-cleared verifier mode. Verifier invoked with `--role-claim bsa-sar-cleared`; full content returned; `additional_verifications: ['privileged_investigation_full_content_returned']`.

**Cross-reference.** §10.70.

### 080 — `privileged-investigation-non-cleared-redacted-with-existence`

**Verifies.** §10.70 non-cleared verifier mode. Verifier invoked without SAR-cleared role-claim; returns redacted-with-existence-attestation; exit code `0` (PASS) with `additional_verifications: ['privileged_investigation_redacted_with_existence_attestation']`.

**Cross-reference.** §10.70; §10.12 (additional-verifications discipline).

### 081 — `cross-institution-fedwire-cross-anchored`

**Verifies.** §10.71 Fedwire cross-anchored case. Originating + receiving institutions both participate; registry-discovery cross-anchor in `bound` state; verifier emits `cross_institution_chain_verified`.

**Cross-reference.** §10.71; §10.21.3.

### 082 — `cross-institution-fedwire-cross-anchor-unbound`

**Verifies.** §10.71 `cross_anchor_unbound` documented residual. Originating institution publishes; receiving institution non-participating; verifier emits `cross_anchor_unbound`.

**Cross-reference.** §10.71.

### 083 — `cross-institution-ach-variant`

**Verifies.** §10.71 ACH event family. `audit.ach.originated` and `audit.ach.received` events under settlement-day publication SLA.

**Cross-reference.** §10.71.

---

## Implementation note (Phase 11-14)

Each vector materializes during its phase as a directory `spec/test-vectors/049-...` through `spec/test-vectors/083-...` containing:

1. `README.md` — the per-vector documentation (extending the scaffold here).
2. `input.json` — the input fixture in canonical JSON.
3. `expected_canonical.txt` — the expected canonical bytes (RFC 8785 / JCS).
4. `_compute.py` — the deterministic computation script that produces `expected_canonical.txt` from `input.json` (HPy reference).
5. `expected_*.txt` — additional expected outputs per the verifier-mode dispatch (e.g., `expected_red_side_walk.txt` and `expected_black_side_walk.txt` for vector 064).

Cross-implementation byte-equivalence between HPy and HCp.Chain is gated to each phase's plain-spoken-companion repo release. The Phase-N.PS release-blocking criteria include byte-identical reproduction of the phase's vectors across both reference implementations.
