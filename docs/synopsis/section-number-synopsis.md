# FFIEC Chain-of-Custody — Section-Number Synopsis

Spec: `spec/chain-of-custody-DRAFT-0.1.0.md` (PRD-1, document version `0.1.0-draft.1`).
Wire-format identifier: `v1` (currently `sign_payload_version = "v1.0b"`).
Navigation aid keyed to section numbers; one short synopsis per heading. Informative.

| Section | Synopsis |
|---|---|
| §0 | Two independent versions: document version (PRD-N, `0.1.0-draft.N`) and wire-format identifier (`v1`); they do not move in lockstep. |
| §0.5 | Reading-the-document framing: 30-minute critical paths, role triage, and the layered companion artifacts surrounding the spec. |
| §0.5.1 | Three-paragraph elevator pitch: what is captured, how it is sealed, how it is verified. |
| §0.5.2 | Mermaid diagram mapping SDK capture, events, daily Merkle seal, HSM signature, published artifacts, and verifier into one flow. |
| §0.5.3 | Per-role reading-path triage table (executive, MRM, audit, examiner, implementer) with time budget and companion document. |
| §0.5.4 | Five-minute path: read §1.2 lists, the §4 primitives table, and your §13 stakeholder entry. |
| §0.5.5 | Names the three companions outside the spec — auditor stories, question bank, reference implementation. |
| §0.6 | Normates the contextual-help URL convention pointing into the plain-spoken companion repository, with PRD-stable URLs and a coverage-gap detector. |
| §1 | Scope: language-neutral chain-of-custody primitives covering decision-time AND training-phase integrity for AI in regulated systems. |
| §1.1 | Daubert four-factor grounding (testability, peer review, known error rate, general acceptance) plus 2026 MRM-guidance regulator-facing alignment. |
| §1.2 | Epistemic scope: the chain proves what the AI said and that the record was untampered; it does not prove truth, policy compliance, bias-freedom, or disclosure completeness. |
| §1.3 | Security definitions: per-event MAC EUF-CMA, Merkle second-preimage, Ed25519 EUF-CMA; effective security level 128 bits per NIST SP 800-175B. |
| §1.4 | Compositional security: three independent layers (per-event HMAC, daily Merkle seal, HSM signature) — single-layer compromise is insufficient to silently tamper. |
| §1.5 | Decision-event vs state-machine modeling: discrete-decision events versus long-running case lifecycles (claims, disputes, holds, audits). |
| §2 | Out of scope: runtime environment, event semantics, retention duration, specific HSM model. |
| §3 | Definitions table (event, run, tenant, IKM, session key, key_version, key_fingerprint, format_version, chain_kind, hkdf_inputs_digest, region, CC8.1, posture). |
| §3.1 | Legacy tenant-identifier handling: three migration patterns (opaque hash, controlled aliasing, reject non-conforming) for upstream IDs that violate the §3 character class. |
| §4 | The four primitives — implementation-topology framing (monolithic vs distributed both conformant) and the wire-or-on-disk observation rule. |
| §4.1 | Primitive 1 — HMAC chain at capture: per-event HMAC binding under tenant-bound session key derived via HKDF; eight inviolate properties. |
| §4.1.1 | Session-key handshake — IKM-delivered (Model A) vs session-key-delivered (Model B) postures with authentication, confidentiality, and per-tenant determinism requirements. |
| §4.1.2 | Vendor-namespaced HKDF constants vs FFIEC-conformance constants; binary at the chain-file level via `hkdf_inputs_digest`; verifier posture is explicit (`--posture=ffiec`). |
| §4.1.3 | Per-event MAC algorithm agility — RECOMMENDED `payload_hash_alt` field at v1.0b for in-band early warning; candidate-normative AND-security at v1.x. |
| §4.2 | Primitive 2 — Daily Merkle seal: events from a UTC day aggregate into an RFC 6962 Merkle tree per `(run_id, seq)`; full seal-record schema. |
| §4.2.1 | Seal cadence default daily, configurable hourly or weekly; relaxation requires examiner approval, tightening requires only notification. |
| §4.2.2 | Day-boundary semantics by ledger `received_at` UTC; late-arriving entries flagged `late_binding=true` and rolled into the next day's seal. |
| §4.3 | Primitive 3 — HSM-rooted root signature (Ed25519 over `sign_payload`); pre-amendment 6-line, v1.0a 10-line, and v1.0b 12-line forms with SLA. |
| §4.3.1 | HSM unavailability and 72-hour regulator notification SHOULD; cyber-incident notification (36 hours) is a separate path. |
| §4.3.2 | Algorithm rotation and quantum-readiness: explicit `algorithm` identifier, 30-day spec-patch SLA, dual-algorithm Variant B AND-security. |
| §4.4 | Primitive 4 — OpenTelemetry-native wire: `ffiec.chain.*` attribute namespace, collector pass-through rule, genesis-block uniqueness rule. |
| §4.4.1 | AI routing decisions: `audit.routing.*` event types (attempt, success, failover, circuit_state_change, refused, classifier_output); cross-border-transfer composition. |
| §4.4.2 | Deployment-intent capture: `audit.deployment.intent` enum (production, ab_test, canary, multi_region_drift, vendor_reroute_observed, regulatory_sandbox, disparate_impact_test_run); institution-level trigger. |
| §4.4.3 | OTLP transport identification: required Resource attributes (`ffiec.chain.spec`, `service.name/version`, `ffiec.chain.posture`, `format_version`) plus HTTP/gRPC dispatch headers. |
| §4.4.4 | Severity for chain traffic: collectors MUST NOT severity-filter chain traffic; receivers stamp `SeverityNumber` in 9..20 with `SeverityText` identifying chain-of-custody. |
| §4.4.5 | Underwriting-feature recording (`audit.underwriting.features.*`) and disparate-impact testing (`audit.disparate_impact.*`) for state DOI examination. |
| §4.4.6 | SaaS-edge connector source attribution (`audit.connector_source.*`) plus stable-`run_id` discipline that survives connector restarts. |
| §5 | Wire format: OTLP protobuf transport, RFC 8785 JCS canonical form for MAC input, canonical-form exclusion of chain-stamp fields. |
| §5.0.1 | Top-level wire-format kinds (closed enumeration): `chain_entry`, `seal_record`, `anchor_record`, `cross_domain_transition`; new kinds are additive within `format_version=v1`. |
| §5.1 | Transport encryption: TLS 1.3 minimum (TLS 1.2 sunsets 2028-01-01); discovery and policy endpoints inherit the same floor. |
| §5.2 | Best-evidence posture under FRE 1001-1004: captured JSON is content-bearing; canonical bytes are integrity-bearing; both are originals. |
| §6 | Storage: append-only mandatory (no UPDATE/DELETE); chain-stamp preservation byte-for-byte; line-oriented files require header plus `\n`-terminated lines. |
| §7 | Verification procedure: ordered 12-step walk (header pre-flight, per-event walk, per-day Merkle and signature, late-binding reporting, unknown-kind fallthrough, witness/customer-disclosure modes). |
| §8 | Conformance test vectors: `spec/test-vectors/` is the canonical corpus that pinned-byte-equivalent implementations MUST reproduce. |
| §9 | Security considerations: pointer to `docs/design/09-threat-model.md` for adversary capabilities and threat model. |
| §10 | Operational requirements (normative) — the §10.x extension surface where most institution-side discipline lives. |
| §10.1 | Key-fingerprint reconciliation at no more than weekly cadence; tenant_id uniqueness enforced at the IKM-registry layer; multi-deployment global registry MUST. |
| §10.2 | Operational events (`ledger.*`, `seal.*`, `chain.*`, `master_key.*`, `connector.*`, `chain.coverage_map_published`, `chain.entity_succession`) emitted for control evidence. |
| §10.3 | Append-only enforcement at both application code and database role layers; defense in depth against deletion. |
| §10.4 | Time synchronization: NTP discipline for application hosts and ledger; ledger `received_at` is authoritative for day-boundary partitioning. |
| §10.5 | HSM custody at FIPS 140-2 Level 3+, non-extractable signing key, separation of duties; FIA residual-risk treatment. |
| §10.6 | IKM minimum length: 32 bytes (256 bits); enforced at registry-provisioning and SDK-configure time. |
| §10.6.1 | IKM generation requirements: FIPS-validated CSPRNG (HSM internal, OS-level, dedicated hardware); weak-RNG sources enumerated as non-conformant. |
| §10.7 | Software-key adapter exclusion in production: compile-time or packaging-level exclusion; `kms_handle_uri="plaintext-dev"` and `dev_mode=true` produce verifier `--strict` refusal. |
| §10.8 | Constant-time comparison MUST for the fingerprint and MAC checks; stdlib helpers (`hmac.compare_digest` etc.) are RECOMMENDED. |
| §10.9 | IKM registry retention: every IKM generation retained as long as any chain entry that references its `key_version`. |
| §10.10 | IKM rotation crossing the seal boundary: per-entry `key_version` lookup; the day-after seal lists `key_versions=[old,new]`. |
| §10.10.1 | Hourly cadence rotation: an IKM rotation can cross multiple seal boundaries; each mixed-version seal carries `key_versions=[old,new]` until the rotation completes. |
| §10.10.2 | Within-day algorithm rotation — Pattern A (same-day cosign per §4.3.2) or Pattern B (split-day with two seal records partitioned by `covers_received_at_min/max`). |
| §10.11 | Adverse-action notice translation chain entries (ECOA and state-insurance analog): `audit.ecoa.translation.*` schema with target_language, translator_kind, output_hash, delivery. |
| §10.11.1 | ECOA adverse-action reasons schema (`audit.ecoa.adverse_action.*`): integrity-binds the structured reasons list, feature attributions, and explanation method. |
| §10.11.2 | FCRA §611 reinvestigation timing (`audit.fcra.reinvestigation.*`): 30-day clock with 45-day extension, furnisher and consumer notification timing, outcome enumeration. |
| §10.12 | Verifier CLI exit-code contract: closed enum 0 (PASS), 1 (FAIL), 2 (could-not-begin), 3 (configuration error), plus additional-verifications array discipline. |
| §10.13 | Evidentiary artifacts retention list (SDK manifest, source hash, HSM config, seal-job logs, change-management, verifier output) for FRE 901(b)(9) authentication. |
| §10.14 | Trusted-time integration: RFC 3161 RECOMMENDED for high-stakes contexts at v1.0; v1.x forward commitment names pre-MAC vs post-MAC binding choice. |
| §10.15 | Multi-region resilience — Pattern A (active-active with seal-region pinning, single seal region per tenant-day) or Pattern B (per-region `tenant_id`); seven invariants. |
| §10.16 | SaaS-edge mirror connectors: institution's CC8.1 MUST quantify median, p95 SLO, alerting threshold, and RTO; imprecise lag wording is non-conformance. |
| §10.17 | HSM partition ceremony attestation: `chain.partition_ceremony_attended` event with signatories (incl. `entity_affiliation`), witness, attendance-PDF hash, optional HSM attestation token. |
| §10.18 | CC8.1 and runbook cross-referencing: every operational runbook supporting a normative requirement MUST cite the spec section number. |
| §10.19 | Chain-coverage boundary documentation: institution's CC8.1 names each system as instrumented or not; version-stamped via `chain.coverage_map_published`; `audit.external_artifact.*` family for hash-anchors. |
| §10.20 | Training-data retention vs deployment-window discipline: training-data shard retention floor MUST be at least the longest active deployment window plus an investigation buffer. |
| §10.21 | Cross-vendor model-handover schema (`audit.model_handover.*`): provider, model_id/version, artifact + model-card + fairness hashes, multilingual audit reports, contract triple, `contract_status` enum. |
| §10.21.1 | Sub-pattern of §10.21 — sample-based-attestation cross-anchor for lot-level binding (anti-counterfeit, AS6171, DARPA SHIELD, lot-acceptance testing). |
| §10.21.2 | Sub-pattern of §10.21 — independent-evaluator parallel-chain composition with `cardinality` (integer or `"dynamic"`) and target-anchor cross-binding. |
| §10.21.3 | Sub-pattern of §10.21 — registry-discovery cross-anchor for cross-institution chains mediated by a third-party registry (Fedwire, FedNow, FINRA). |
| §10.22 | Redaction discipline: pre-MAC SDK redaction is the conformant posture; `audit.redaction.*` family records policy, paths, methods, and disposition. |
| §10.23 | Consumer-correlation index integrity: Shape 1 (chain-anchored per-consumer entries) or Shape 2 (daily `consumer_index.attestation` event) for CFPB CID-class production. |
| §10.24 | Entity succession (`chain.entity_succession`): legal-entity change of operator (merger/acquisition/divestiture/rename/subsidiary_transfer) with required dual signatures bound under v1.0b seal. |
| §10.25 | Run resume and chain-tail acquisition: three-place tail lookup (in-memory, sidecar, ledger query), single-writer-per-run, ledger ingestion cross-check, genesis-form anti-spoof, DR rejoin. |
| §10.26 | Reference verifier distribution: separate Apache-2.0 repository, reproducible builds, Cosign-signed artifacts, per-platform binaries, SBOM, three-name CC8.1 citation. |
| §10.27 | Configurable seal cadence: `per_second` through `weekly`; sub-daily cadences are streaming-mode and the `cadence` field is bound under `sign_payload`. |
| §10.28 | Streaming-mode IKM rotation: §10.10 boundary-crossing discipline applied at the cadence interval rather than the daily boundary. |
| §10.29 | Streaming-mode verifier procedure: per-event and per-cadence-interval incremental verdicts; extends §10.12 with codes 4 (all-pass-so-far), 5 (anomaly), 6 (rotation-pending). |
| §10.30 | Trusted-time integration NORMATIVE for streaming-mode institutions; `clock.drift_detected` operational event with institution-named threshold. |
| §10.31 | Per-cohort subtree disclosure: Merkle audit path over a cohort filter against the signed root; role-aware recursive extension via `audit.disclosure.role.*`. |
| §10.32 | Per-device session key derivation: HKDF info parameter binds `device_id` alongside `tenant_id`; each device's session key is independent. |
| §10.33 | Model-update events (`audit.model_update.*`): push, pull, verify, activate — parent-linked chain forming the model-rollout lifecycle. |
| §10.34 | Training-phase integrity (`audit.training.*`): local_gradient, aggregation, validation, model_artifact events for federated learning and in-house training. |
| §10.35 | Edge-attestation primitive: chain entries bind device hardware-attestation document (Android Keystore, Apple Secure Enclave, TPM 2.0, Intel SGX). |
| §10.36 | Late-arriving-entry seal discipline: Pattern A supplemental seal or Pattern B rolling seal window; verifier dispatches on `seal.late_pattern`. |
| §10.37 | Hierarchical Merkle aggregation: per-device or per-subtree Merkle root included as a leaf of the daily seal, with `seal.hierarchy` depth indicator. |
| §10.38 | Consent capture (`audit.consent.*`): given, referenced, withdrawn, expired lifecycle; `subject_id_hash` binding under DPDP / GDPR / CCPA / PIPA / LGPD. |
| §10.39 | Institutional successor-attestation (`chain.successor_attestation`): cryptographic-inheritance event when the acquired target operated a non-Herald-conformant chain. |
| §10.40 | Cross-vendor chain-merge cross-anchor: hash-anchors foreign-vendor roll-up artifacts (signed PDFs, foreign seal records) under §10.19's `audit.external_artifact.*`. |
| §10.41 | Chain-coverage-map M&A temporal-slice extension: pre-acquisition / cut-over-window / post-cut-over partitions; re-emitted via `chain.coverage_map_published` per migration tranche. |
| §10.42 | Backfill seal discipline: one-time `seal.backfill_at_close=true` seal at acquisition close producing a chain-shaped envelope retroactively over inherited baseline-diary records. |
| §10.43 | Claim-state-machine chain entries: integrity-binds insurance / loss-claim state transitions (`opened` to `pending` to `decided` to `closed`) with actor and authorizing-policy binding. |
| §10.44 | Cession-cohort recursive subtree disclosure: spec-section anchor for the §10.31 role-aware recursion under multi-party flows (cedent to reinsurer to retrocessionaire). |
| §10.45 | Independent third-party adjuster anchor (`chain.adjuster_anchor`): bidirectional cross-anchor binding the same adjuster activity under multiple parties' chains. |
| §10.46 | Bordereau integrity (`audit.bordereau.*`): periodic-cession-statement lifecycle (published, received, reconciled, discrepancy_resolved) with `bordereau_sha256` cross-binding. |
| §10.47 | Generation prompt/output four-tuple binding (`audit.generation.*`): system-prompt, user-prompt, retrieval-set Merkle root, output hashes for stochastic-GenAI integrity. |
| §10.48 | Stochasticity attestation (extends §10.47): temperature, top_p, top_k, seed, model_version, model_weight_hash for reproducibility-bound regimes. |
| §10.49 | Retrieval-source integrity: retrieval-set Merkle root over per-document anchors (`audit.retrieval.document_anchor.*`) cross-bound to the §10.47 generation event. |
| §10.50 | Output-grounding event family (`audit.review.*`): clinician_edit, grounding_pass, grounding_fail, hallucination_detected outcomes signed under the GAP-5 HITL primitive. |
| §10.51 | Public-transparency overlay (`chain.public_transparency.published`): integrity-binds the DP-noised aggregate, mechanism, epsilon budget, RNG seed, and mechanism version. |
| §10.52 | Public model-card binding: each model-card publication or update emits a §10.19 `audit.external_artifact.*` entry with `kind="model_card"`. |
| §10.53 | Hybrid post-quantum seal mandate: lifts §4.3.2 dual-algorithm (Variant B AND-security) from RECOMMENDED to NORMATIVE-WHEN-APPLICABLE for long-retention regimes. |
| §10.54 | Decadal re-sealing discipline (`seal.resealed_at_decadal_boundary=true`): periodic re-sealing of prior generations under the then-current cryptographic suite for 60-year retention. |
| §10.55 | Audit-target challenge-response procedure (`audit.challenge_response.*`): government-AI-decision filed-triaged-disposed lifecycle with signed disposition (upheld/overturned/modified/withdrawn). |
| §10.56 | Hardware bill-of-materials chain integrity (`audit.hbom.*`): incoming_test, fru_integration, depot_return events binding component cryptographic identity per §10.58. |
| §10.57 | Firmware-attestation chain across supplier tiers (`audit.firmware.build`, `audit.firmware.activate`): cross-anchor to sub-tier supplier chain or §10.21 signed-attestation regime. |
| §10.58 | Component cryptographic identity primitive: closed enum (puf-response, seal-chiplet-attestation, factory-provisioned-key, serial-lot-hash) with binding-walk vs challenge-walk dispatch. |
| §10.59 | RMA / sustainment chain re-entry discipline (`audit.rma.*`): depot_return, repair_complete, cannibalized, scrapped events; duplicate-binding-anomaly framework. |
| §10.60 | Anti-counterfeit cross-anchor (extends §10.21.1): independent third-party AS6171 / SHIELD attestation referenced from the duplicate-binding-anomaly resolution path. |
| §10.61 | CMMC 2.0 / NIST 800-171 / NIST 800-161 regulator-pack overlay framework: versioned sub-overlays per CMMC release with control-by-control PASS/FAIL verifier dispatch. |
| §10.62 | Red/black separation chain integrity: introduces the `cross_domain_transition` wire-format kind binding the red-side entry, deterministic releasable-hash projection, and module attestation. |
| §10.62.1 | Sub-pattern of §10.62 — every chain entry stamps `audit.color_classification.side` (red / black / cross-domain) and optional classification level for verifier dispatch. |
| §10.62.2 | Sub-pattern of §10.62 — releasability-projection contract (determinism, no red-side leakage, versioning, test-vector grounding) the per-program filter must satisfy. |
| §10.63 | Training-corpus provenance chain (`audit.training_corpus.*`): shard_ingested, dedup_decision, filter_pass, index_built events for model-training corpus curation. |
| §10.64 | Training-run code-and-config chain (`audit.training_run.*`): launch, checkpoint, completed events with per-step Merkle aggregation over per-chassis gradient contributions. |
| §10.65 | Hyperscale GPU-fleet attestation (`audit.fleet.*`): chassis_admitted, chassis_attested, chassis_quarantined, chassis_decommissioned for tens-of-thousands-of-GPU compute fleets. |
| §10.65.1 | Sub-pattern of §10.65 — composition with §10.58: chassis-level TPM is the chassis-granularity component-cryptographic-identity primitive. |
| §10.65.2 | Sub-pattern of §10.65 — `audit.fleet.profile_updated` event publishing the institution's expected PCR-state-evolution profile so `drift_seen` is publicly verifiable. |
| §10.66 | Model-weight lineage across multi-month runs (`audit.model_weights.transition`, `audit.model_weights.deployed`): DAG-shaped lineage with Merkle root over the full transition graph. |
| §10.67 | Pre-deployment evaluation chain (`audit.evaluation.*`): run, result, disposition events with §10.21.2 parallel-evaluator composition for lab-side and AISI-side chains. |
| §10.68 | AI Safety Institute Reference Evaluation Program regulator-pack overlay: maps NIST AI RMF and NIST AI 800-218 onto the §10.63-§10.67 surface with cross-anchor reciprocity. |
| §10.69 | Per-customer audit-trail subset disclosure: per-customer-disclosure HKDF derivation, Merkle subtree-disclosure proof, and documented exclusions (sar, litigation_hold, privileged_investigation, redacted). |
| §10.70 | BSA SAR / privileged-investigation overlay (`audit.privileged_investigation`): role-based verifier dispatch returns full content for cleared readers, redacted-with-existence-attestation otherwise. |
| §10.71 | Cross-institution Fedwire / ACH chain integrity (`audit.wire.*`, `audit.ach.*`): registry-discovery cross-anchor per §10.21.3 against a voluntary Federal Reserve registry. |
| §11 | References: normative (RFCs, FIPS, OTel, RFC 9101 LEI) and informative (FFIEC IT Handbook, SR 11-7, OCC Bulletins, Treasury FS AI RMF); pinned reference verifier release. |
| §12 | Change log (chronological): v1.0-draft to v1.0-rework to v1.0-final to v1.0-final-amendment to v1.0b, with full Round-17 close-out and prior reviewer waves. |
| §13 | Stakeholder navigation: per-role entry points (executive, audit committee, MRM, examiner, cryptographic expert, implementer) into the broader corpus and §10.x sections. |
| §A.1 | Chain envelope schema: enumerates `ffiec.chain.*` attributes (spec, format_version, run_id, seq, prev_hash, payload_hash, key_version, key_fingerprint, region) on every chain entry. |
| §A.2 | OpenTelemetry GenAI envelope (`gen_ai.*`): `request.model` and `response.model` REQUIRED on model-call entries; `provider_attestation` optional. |
| §A.3 | Audit-routing family (`audit.routing.*`): event_type, providers_attempted, provider_chosen, failover_reason, refusal_reason, circuit_state, classifier_*. |
| §A.4 | Cross-border transfer family (`audit.cross_border_transfer.*`): contract_id/version/hash, source/destination jurisdiction, lawful_basis_type. |
| §A.5 | Deployment-intent family (`audit.deployment.*`): intent, rate_filing_id, actuarial_memo_version, experiment_id, region, canary_traffic_pct, policy_version. |
| §A.6 | Underwriting-feature family (`audit.underwriting.features.*`): feature_vector_hash, feature_store_version, feature_categories, protected_class_proxy_flags. |
| §A.7 | Disparate-impact family (`audit.disparate_impact.*`): test period, methodology, protected_class_basis, air_by_class, population_hash, remediation_disposition. |
| §A.8 | Connector-source family (`audit.connector_source.*`): system, replay_id, commit_timestamp, commit_user, lag_observed_ms, change_kind. |
| §A.9 | ECOA / FCRA families (`audit.ecoa.*`, `audit.fcra.*`): pointer entry to §10.11 translation, §10.11.1 adverse-action reasons, §10.11.2 FCRA reinvestigation per-attribute detail. |
| §A.10 | Redaction family (`audit.redaction.*`): policy_id, policy_version, redacted_field_paths, redaction_method, disposition. |
| §A.11 | Consumer-correlation index (`consumer_index.*`): Shape 1 per-entry fields and Shape 2 attestation fields per §10.23. |
| §A.12 | Entity succession (`chain.entity_succession.*`): from/to legal name and LEI, effective_utc, kind, regulator_filing_id, dual_signatures, optional from/to tenant_id. |
| §A.13 | HSM partition ceremony (`chain.partition_ceremony_attended.*`): ceremony_type, partition_handle, signatories, witness, attendance_pdf_sha256, hsm_attestation_token_b64. |
| §A.14 | External artifact (`audit.external_artifact.*`) and model handover (`audit.model_handover.*`) — pointer entry referring to per-attribute detail in §10.19 and §10.21. |
| §A.15 | Service identity and resource attributes (`service.name`, `service.version`, `ffiec.chain.posture`) required at OTLP transport per §4.4.3. |
| §A.16 | Vendor-namespaced attributes (`herald.*` and similar) are out of spec scope; verifier treats them as opaque MAC-bound payload. |
| §A.17 | Recommended reading order for a clean-room implementer (definitions, primitives, wire, storage, verification, §10, then Appendix A). |
