# Changelog

All notable changes to the **document version** of this specification (the spec text, supporting documentation, and submission package) are recorded here.

This file tracks the **document version** axis. Changes to the **wire-format identifier** axis (`"v1"`) are recorded in §12 of the spec itself and are also surfaced here when they occur.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and adapted for the semver-pre-release draft cycle (`0.1.0-draft.N`).

---

## [Unreleased]

### Changed

- **§7 observed-value rendering rule (normative).** Added a normative rule to §7: whenever a verifier reason string embeds a value the verifier observed on the wire — the claimed `format_version`, `sign_payload_version`, `canonical_encoding`, or a declared floor version — the verifier MUST wrap that value in ASCII double-quotes. This resolves a fixture divergence where N023 (`format_version "V1"`) quoted the observed value while N009 (`format_version v2`), N022 (`format_version v1.1`), and the §7 step-1 reason template left it bare.

  **Decision: quote.** Three factors drove the choice. (1) **Consistency.** The rest of §7 already quotes — `sign_payload_version "X"`, `canonical_encoding "X"`, and the floor-version `"X"`/`"Y"` reasons all use double-quotes. Quoting makes step 1 join the existing convention instead of standing alone; the alternative (going bare) would have required editing four reason templates that already quote. (2) **Disambiguation.** Quoting is the only rule that stays unambiguous when the observed value contains spaces or is empty: `format_version "" not supported` reads cleanly where a bare empty value collapses into a double space, and `format_version "v1 beta" not supported` stays one token where the bare form reads as two. (3) **No signature effect.** The reason string is human-facing diagnostic output and is never signed, so quoting it has zero effect on `sign_payload` reconstruction — the byte-level `format_version` discipline (the header field bound under the seal per §4.3) is a separate concern from how the rejection reason is printed. The one factor pointing the other way — the Go reference verifier and the `07-verifier-design.md` pseudocode emitted bare — was outweighed: the Go vector-walk match was already quote-insensitive, so the corpus pin can quote without breaking the gate, and the reference rendering aligns to the dominant spec convention.

  **Scope.** The rule governs the version/encoding-identifier reason family (the values the verifier dispatches on). It deliberately does NOT touch the structured-field reason family (`unknown key_version: no IKM for (tenant=T, key_version=V)`, which renders `key=value` pairs), the enum-in-sentence family (`co-signed seal failure: algorithm X validated`), or the state-transition family (`closed → opened`). Those families have their own internally-consistent rendering conventions; folding them under the quoting rule would introduce new divergences rather than remove one. The `additional_verifications marker "<value>"` reason already quotes and is consistent with the chosen rule.

  **Re-rendered vectors.** N009 and N022 expected outputs and generators updated to the quoted form (N023 already quoted). The negative-corpus `INDEX` rows for N009 and N022 updated to match. Spec text touched: §7 step 1 reason template + new "Observed-value rendering in §7 reason strings" normative block; `docs/design/07-verifier-design.md` pseudocode; `docs/future-needs/sections-plain-english/03-wire-storage-verification.md`. The generic-form references in `regulator-pack/finding-language.md`, `examiner-quickstart.md`, `sample-report.md`, and `docs/design/02-chain-construction.md` were left unchanged — they render no observed value, so the rule does not reach them.

---

## [0.3.0] PRD-3.1 - 2026-05-24 (reference-implementation sub-release)

### Summary

PRD-3.1 ships the reference implementations for the three attribute families PRD-3 normated under Path A (REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1). Document version remains 0.3.0. Wire-format identifier remains v1. No normative spec text changed.

### Shipped

- **Section 14.6 `audit.actor.*`** reference implementations in C# (Herald.Compliance), Python (Herald.Py), and Go (ffiec verifier). Byte-identical JCS-canonical output across all three.
- **Section 14.7 `audit.reasoning.substrate_kind`** reference implementations in C# / Python / Go.
- **Section 14.8 `audit.downstream_action.*`** reference implementations in C# / Python / Go.
- **35 new conformance vectors** (050-084) pinning emitter output and verifier predicate behavior.
- **5 Phase 11 shared-primitive vectors** (049-053) materialized on disk and passing across all three implementations.
- **Kognitos-projection library** (Herald.Compliance) demonstrating TesseraSeal-to-Kognitos field mapping.
- **SDK reference documentation** for the three attribute families.
- **Framework-portability documentation** with proof-by-construction via the Kognitos projection.

### Changed (status-only)

- Section 14.12 items O-4 and O-6 status updated from FORTHCOMING to SHIPPED.
- Sections 14.6, 14.7, 14.8 "Reference-implementation status" blocks updated from "normative-but-forthcoming" to "SHIPPED -- PRD-3.1."
- Section 14.10 cross-reference summary table rows updated with SHIPPED status.

### Unchanged

- All normative spec text (sections 0-14).
- Wire-format identifier v1.
- Existing test vectors 001-049 and negative vectors N001-N029.
- Open items O-1, O-2, O-3, O-5, O-7 (remain FORTHCOMING).
- O-8 (remain EXOGENOUS).

---

## [0.3.0] - 2026-05-21 (Public Review Draft 3 / PRD-3)

### Headline

PRD-3 advances chain-of-custody on five spearheads grounded in cross-Kognitos competitive analysis and adds three net-new attribute families pre-cited by the Laura companion documentation. PRD-3 rolls forward the Stories 18-20 wave previously scheduled for PRD-4. Wire-format identifier v1 unchanged.

### Added (PRD-3 advancement appendix - section 14)

- **section 14.0** PRD-3 advancement summary (informative).
- **section 14.1** Multi-layer cryptographic defense - tightening section 1.4 narrative. No code change.
- **section 14.2** Daubert-grade testability - tightening sections 1.1 + 7 + 10.12. Adds the section 10.12 closed-enumeration footnote distinguishing implemented vs reference-implementations-forthcoming markers. Eleven of 21 markers flagged forthcoming.
- **section 14.3** Categorical exclusions by design - tightening sections 10.13.3 + 10.69 + 10.70. Section 10.70 substantive-reach limitation clarified normatively. Status: NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14.
- **section 14.4** Post-quantum cryptographic agility - tightening sections 4.1.3 + 4.3.2 + 10.53 + 10.54. Section 4.1.3 introduces optional payload_hash_alt field for HMAC-SHA-3 / HMAC-BLAKE3 dual-MAC. Status: section 4.1.3 dual-MAC + section 10.53 migration-window dispatch NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1.
- **section 14.5** Examiner runs the verifier locally - tightening sections 10.26 + 10.13.1 + 5.2.1. Sigstore-alignment language added (informative). Established-pattern framing added (Sigstore Cosign, Linux Foundation Rekor, IETF Certificate Transparency RFC 6962, OpenSSF policy precedent).
- **section 14.6** audit.actor.* family (NEW NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1). Authenticated_user_id_hash, authentication_method, session_id, delegation_chain. Closes the May-20 Richard coverage-audit gap for Kognitos Field 3 (authenticated human user identity).
- **section 14.7** audit.reasoning.substrate_kind (NEW NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1). Closed canonical enumeration: neurosymbolic, retrieval_grounded_with_citations, rule_based, post_hoc_llm_rationalization, attention_feature_importance, none, institution_named. Closes the Kognitos comparison-doc Point 8 gap.
- **section 14.8** audit.downstream_action.* family (NEW NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1). Generalized system-of-record linkage with action_kind, system_of_record_id, change_record_id_hash, applied_at_utc.
- **section 14.9** Smaller PRD-3 refinements (section 10.22 pre-MAC redaction, section 10.21 cross-vendor handover, section 10.71 cross-institution wire status, section 10.74 long-retention crypto-erasure, section 4.4.1 ISO 3166-1 pinning).
- **section 14.10** Cross-reference summary table.
- **section 14.11** Wire-format identifier confirmation (v1 unchanged).
- **section 14.12** Open items deferred to PRD-3.1 / PRD-4.

### Rolled forward from PRD-4 (formerly 0.1.0-draft.7)

The full PRD-4 wave (sections 10.56-10.71 + section 0.6 + section 7 unknown-wire-format-kind fallthrough + section 10.21 amendments + test vectors 049-083 indexed) is consolidated into PRD-3. Document version moves from 0.2.0 (PRD-2) to 0.3.0 (PRD-3); the prior PRD-4 (0.1.0-draft.7) marker is retired. Wire-format identifier v1 unchanged.

### Code-vs-claims audit

A code-vs-claims audit grounds every PRD-3 normative claim against implementation artifacts (C# in Herald.Compliance, Python in Herald.Py, test vectors under spec/test-vectors/). Audit lives at Herald/wiki/PRD-3-CODE-VS-CLAIMS-AUDIT.md (internal). Summary:

- Spearhead 1 (Multi-layer crypto): PROVEN BY CODE + TEST
- Spearhead 2 (Daubert testability): PROVEN BY CODE + TEST
- Spearhead 3 (Categorical exclusions): CLAIMED BUT UNPROVEN; ships under Path A flag (NORMATIVE, REFERENCE IMPL FORTHCOMING PHASE 14)
- Spearhead 4 (PQ agility): PARTIALLY PROVEN; section 10.54 shipped, section 4.1.3 + section 10.53 dispatch flagged FORTHCOMING PRD-3.1
- Spearhead 5 (Examiner runs verifier): PROVEN BY CODE; integrated discovery-packet path FORTHCOMING PRD-3.1
- Three Laura pre-cited families (audit.actor.*, audit.reasoning.substrate_kind, audit.downstream_action.*): ASPIRATIONAL - reference impl FORTHCOMING PRD-3.1
- Eleven of 21 section 10.12 closed-enumeration markers are normative-but-unimplemented; PRD-3 adds the section 10.12 footnote
- Thirty-five test vectors (049-083) indexed but not materialized

### Path A applied

The canonical flag block "Reference-implementation status (normative-but-forthcoming)" is applied inline at every PRD-3 section whose reference implementation lags the spec text. Eight sections carry the flag: §4.1.3 (`payload_hash_alt`, PRD-3.1), §10.13.3 (litigation-hold registry binding, Phase 14 / Story 20 wave), §10.53 (PQ migration-window verifier dispatch, PRD-3.1), §10.69 (per-customer disclosure, Phase 14 / Story 20 wave), §10.70 (BSA SAR / privileged-investigation overlay, Phase 14 / Story 20 wave), §14.6 (`audit.actor.*`, PRD-3.1), §14.7 (`audit.reasoning.substrate_kind`, PRD-3.1), §14.8 (`audit.downstream_action.*`, PRD-3.1). The spec text is the conformance bar today; the reference implementations and corresponding test-vector materializations are the per-section landing signals. Resolves PRD-3-INDEX.md Open Question 7.

### Wire-format identifier

v1 unchanged.

### Pre-mortem reversals (recorded for posterity)

PRD-3 produced two structural reversals from the initial advancement draft:

1. **Path A vs Path B for section 10.69 + section 10.70 reference implementations.** Initial draft proposed gating PRD-3 ship on reference-impl completeness (Path B, 2-3 week delay). Reversed to Path A (ship NORMATIVE with REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14 flag) per Richard read - the spec text bar is preserved, the operational implementation can lag without violating the PRD-3 publication contract. Confirmed by Steve resolution (pending) on open question 7.
2. **Section 10.12 footnote vs separate normative carve-out.** Initial draft proposed splitting the closed-enumeration table into implemented + forthcoming halves. Reversed to a single normative footnote distinguishing the two classes - preserves the closed enumeration as the canonical contract, names which bars are testable today without restructuring the table.

---

## [0.1.0-draft.7] &mdash; 2026-05-09 (in progress, PRD-4 wave)

### Added (16 reference-spec extensions — PRD-4 wave / Stories 18-20)

The PRD-4 wave closes the §10.56-§10.71 forthcoming-stories rollup plus three normative cross-cutting additions (§0.6 Navigation, §7 unknown-wire-format-kind fallthrough, §10.21 amendments). Sixteen new sections close the Story-18 (Argent Vector Defense Systems / TALON-X), Story-19 (Aerolith Compute / AISI), and Story-20 (Northbridge acquisition close) integration gaps. Wave structured as three story-aligned phases (Phase 12-14) preceded by a Phase-11 shared-primitives wave that builds the four cross-cutting primitives consumed by the wave's wishlist sections. One candidate cross-cutting primitive (GAP-13 verifier-authorization context) deferred to PRD-5 conditional on a third consumer demonstrating structural fit. The wave's planning artifact is `docs/future-needs/gap-wish-manifest-stories-18-20.md` Rev 2.

**Cross-cutting normative additions:**

- **§0.6 Navigation and contextual-help URL convention (normative)** &mdash; documents the public-spec / plain-spoken companion repository split. URL stability and citation indirection are normative.
- **§7 Unknown wire-format kind fallthrough rule (normative)** &mdash; PRD-3 verifiers ingesting PRD-4 chains containing new wire-format kinds emit `additional_verifications: ['unknown_kind_present']` and exit code 14 under `--strict-known-kinds`. Backportable to PRD-3.1.
- **§10.21 amendments (three new subsections):** §10.21.1 sample-based-attestation pattern (consumed by §10.60); §10.21.2 independent-evaluator parallel-chain composition (consumed by §10.45, §10.50, §10.60, §10.67; closes GAP-11); §10.21.3 registry-discovery pattern (consumed by §10.71; closes GAP-14).

**Story 18 — Argent Vector Defense Systems / TALON-X (Phase 12, vectors 054-064):**

- **§10.56 Hardware bill-of-materials chain integrity** &mdash; `audit.hbom.*` family covering incoming-test, FRU integration, depot return.
- **§10.57 Firmware-attestation chain across supplier tiers** &mdash; internal-build path direct, sub-tier path via §10.21 cross-anchor.
- **§10.58 Component cryptographic identity primitive** &mdash; closed canonical four identity-kinds (PUF, SEAL chiplet, factory-provisioned key, serial+lot hash); binding-walk vs challenge-walk modes; exit code 12 (`CHALLENGE_WALK_PUF_VERIFIED`). Closes GAP-9.
- **§10.59 RMA / sustainment chain re-entry discipline** &mdash; cannibalization parent-children pattern; duplicate-binding-anomaly framework.
- **§10.60 Anti-counterfeit cross-anchor (extends §10.21.1)** &mdash; AS6171 / DARPA SHIELD via sample-based-attestation.
- **§10.61 CMMC 2.0 / NIST 800-171 / NIST 800-161 regulator-pack overlay framework** &mdash; versioned per CMMC release; deprecated-version sunset-attestation marker.
- **§10.62 Red/black separation chain integrity** &mdash; cross-domain transition record as new top-level wire-format kind; releasability-projection contract framework (§10.62.2); two verifier modes; exit code 11 (`BLACK_SIDE_PASS_RED_NOT_WALKED`). Consumes GAP-10.

**Story 19 — Aerolith Compute / AISI (Phase 13, vectors 065-076):**

- **§10.63 Training-corpus provenance chain** &mdash; build-time chain.
- **§10.64 Training-run code-and-config chain with per-step Merkle aggregation** &mdash; per-step Merkle root over per-chassis gradient contributions per RFC 6962.
- **§10.65 Hyperscale GPU-fleet attestation** &mdash; chassis-level §10.58 cryptographic identity at §10.65.1; expected-state-evolution profile (chain-published events) at §10.65.2. Closes GAP-12.
- **§10.66 Model-weight lineage across multi-month runs** &mdash; lineage DAG with merge-pattern support; institution-named retention horizon (typically 60 months).
- **§10.67 Pre-deployment evaluation chain** &mdash; parallel-evaluator composition via §10.21.2. Consumes GAP-11.
- **§10.68 AISI Reference Evaluation Program regulator-pack overlay** &mdash; versioned per AISI program release; cross-anchor reciprocity for AISI's own evaluation chains.

**Story 20 — Northbridge acquisition close (Phase 14, vectors 077-083):**

- **§10.69 Per-customer audit-trail subset disclosure** &mdash; CFPB §1033; per-customer-disclosure HKDF derivation; documented-exception list.
- **§10.70 BSA SAR / privileged-investigation overlay** &mdash; tag schema; role-based verifier dispatch; exit code 13 (`REDACTED_WITH_EXISTENCE_ATTESTATION`). Ships freestanding; GAP-13 deferred.
- **§10.71 Cross-institution Fedwire / ACH chain integrity** &mdash; Federal Reserve voluntary cross-institution-anchor registry via §10.21.3; `cross_anchor_unbound` documented residual. Consumes GAP-14.

### Changed

- **§5.0.1 Top-level wire-format kinds (NEW normative subsection)** &mdash; closes the §5 enumeration gap that was implicit at PRD-3 close. Enumerates `chain_entry`, `seal_record`, `anchor_record` (PRD-1), `cross_domain_transition` (PRD-4 v1 additive). The §7 unknown-wire-format-kind fallthrough rule references this enumeration explicitly. `format_version` boundary preserved: adding a new top-level kind to v1 is additive and does NOT increment `format_version`.
- **§10.12 Verifier CLI exit-code contract** &mdash; preserved unchanged; PRD-4's new procedural states (red-side full walk; black-side hash-equivalence walk; binding-walk; challenge-walk; SAR-cleared mode; non-cleared redacted-with-existence-attestation; unknown-kind-present) report via `additional_verifications` array per §10.12 discipline (PASS-with-condition stays exit 0 with array marker), preserving the integrator's 0-vs-non-zero contract. Earlier wave-internal references to new exit codes (11, 12, 13, 14) are reframed as `additional_verifications` markers; the §10.12 contract is unmodified.

### Reframed (post-fool/auditor pass)

- **§10.71 voluntary cross-institution-anchor registry** &mdash; reframed as a conditional discovery mechanism. Specific operator identity, participant counts, and SLA cadence live in `docs/regulator-pack/fedwire-cross-institution-overlay.md` and the plain-spoken companion repo per §0.6's citation-indirection norm. Spec normates the discovery mechanism, not the registry's existence.
- **§10.68 AISI Reference Evaluation Program** &mdash; reframed as a regulator-equivalent observer-program overlay (AISI as canonical PRD-4 instance). Specific AISI program-acceptance posture is institution-side per the program's published intake format; spec normates the overlay framework and verifier dispatch.
- **§10.45 / §10.50 / §10.60 cross-references** &mdash; back-edited to cite §10.21.2 independent-evaluator parallel-chain composition as the generalized primitive each section is now an instance of (closes auditor MAJOR #6).

### Added (design)

- `docs/design/16-hardware-supply-chain.md` — design rationale for §10.56-§10.61.
- `docs/design/17-red-black-separation.md` — design rationale for §10.62 / §10.62.2.
- `docs/design/18-frontier-ai-training-provenance.md` — design rationale for §10.63-§10.68.
- `docs/design/19-customer-disclosure.md` — design rationale for §10.69.
- `docs/design/20-privileged-investigation.md` — design rationale for §10.70.
- `docs/design/21-cross-institution-wire.md` — design rationale for §10.71.

### Added (regulator pack)

- `docs/regulator-pack/defense-cleared-environment-overlay.md` — cleared-environment + red/black operational mapping.
- `docs/regulator-pack/cmmc-overlay.md` — CMMC 2.0 / NIST 800-171 / 800-161 / DFARS articulation (§10.61.1).
- `docs/regulator-pack/aisi-overlay.md` — AISI Reference Evaluation Program articulation (§10.68.1).
- `docs/regulator-pack/cfpb-1033-overlay.md` — CFPB §1033 articulation.
- `docs/regulator-pack/bsa-sar-overlay.md` — BSA SAR / privileged-investigation articulation.
- `docs/regulator-pack/fedwire-cross-institution-overlay.md` — Fedwire / ACH cross-institution articulation.

### Added (test vectors)

35 conformance test vectors (049-083) indexed at `spec/test-vectors/PRD-4-INDEX.md`. Per-vector directories materialize during Phase 11-14 implementation. Cross-implementation byte-equivalence between HPy and HCp.Chain is gated to each phase's plain-spoken-companion repo release, NOT to PRD-4 spec freeze (auditor MAJOR #9 / pre-mortem #3 mitigation).

### Reference implementation

Reference implementation work sequenced in `docs/future-needs/gap-wish-manifest-stories-18-20.md` Rev 2 across Phases 11-17. Phases 11-14 ship HPy + HCp.Chain in tandem with per-phase byte-equivalence sign-off; Phase 16 is the final cross-implementation sweep; Phase 17 migrates Stories 1-20 to the plain-spoken companion repo and finalizes the public-spec PRD-4 working-group submission.

### Inputs to PRD-4 wave

- **Auditor punch list** (Dawn, lead-auditor framing): 18 findings — 2 BLOCKER (closed via 049-083 vector allocation), 8 MAJOR (closed), 5 MINOR, 3 NIT.
- **Pre-mortem** (the-fool, Find-the-Failure-Modes mode): 5 failure narratives; mitigations applied — §7 unknown-wire-format-kind fallthrough rule (#1), GAP-13 deferred (#2), per-phase byte-equivalence gating (#3), 35-vector budget scaled to verifier-mode cardinality (#4), AISI letter as plain-spoken-repo gate (#5).

---

## [0.1.0-draft.6] &mdash; 2026-05-09 (in progress)

### Added (5 reference-spec extensions — Phase 8 / Story 17)

The Phase 8 wave closes the §10.39-§10.55 forthcoming-stories rollup. Five new sections close the Story-17 (Helvetian Federal Tax Authority) integration gaps and the long-retention horizon:

- **§1.2 Public-transparency epistemic claim (informative — GAP-7 closure)** &mdash; new paragraph in §1.2's epistemic-scope text qualifying the public-transparency claim: the chain binds the *noised* aggregate (the value actually published), NOT the raw aggregate. The noise application is a separate attestable step the regulator audits out-of-band by re-running the DP mechanism with the chain-bound seed and mechanism-version hash. Same factual-accuracy / statistical-bias non-claim discipline as §1.2's stochastic-output paragraph (Phase 7).
- **§10.51 DP-bound public-transparency aggregate** &mdash; new `audit.public_transparency.*` chain-entry event family for institutions publishing differentially-private aggregate statistics. Eight required fields (aggregate_kind, aggregate_published_value (the noised value), coverage period bounds, published_at_utc, dp_mechanism, dp_epsilon, dp_seed, dp_mechanism_version_sha256), one paired field (dp_delta required for approximate-DP, absent for pure-DP), one optional cohort-subtree cross-binding. Closed canonical DP-mechanism enumeration: `laplace` / `gaussian` / `discrete_laplace` / `discrete_gaussian`.
- **§10.52 Public model-card binding** &mdash; institutions publishing public model cards hash-anchor each publication via §10.19 `audit.external_artifact.*` with the institution-named `kind` value `"model_card"`. NO new event family — pure §10.19 reuse with the canonical `kind` discriminator. Each model-card change emits a NEW chain entry (the chain accumulates publication history).
- **§10.53 Hybrid post-quantum seal (NORMATIVE-when-applicable LIFT)** &mdash; lifts the existing §4.3.2 dual-algorithm-cosigned-seal posture from RECOMMENDED to NORMATIVE when the institution is in scope of long-retention regimes (60-year horizon). NO new wire-format kind; test vector `015-dual-algorithm-cosigned-seal` IS the byte form.
- **§10.54 Decadal re-sealing discipline (normative when applicable)** &mdash; new annotated seal record at decadal boundaries to maintain post-quantum cryptographic agility across 60-year retention. Follows §10.42 backfill-seal's annotated-seal precedent (NO new wire-format kind). Seven metadata-leaf fields (resealed_at_decadal_boundary discriminator, window bounds, baseline manifest SHA-256, under_algorithm, generation_index ≥ 1, previous_generation_anchor_sha256). Verifier-dispatch: 4-step path (Merkle recompute, baseline cross-binding, previous-generation anchor verification).
- **§10.55 Audit-target challenge-response event family** &mdash; new `audit.challenge_response.*` chain-entry event family composing §1.5 / GAP-2 state-machine (filed → triaged → disposed) with GAP-5 HITL signed-disposition primitive. Civic-AI sibling of §10.50 (output-grounding review). Closed canonical outcome enumeration: `upheld` / `overturned` / `modified` / `withdrawn` plus institution-named outcomes per CC8.1.

### Changed

- **§11 References (GAP-6 closure)** &mdash; lifts `docs/cryptographic-agility-roadmap.md` from informative to NORMATIVE reference. Long-retention regimes operate under the rotation roadmap; §10.53 + §10.54 + GAP-6 form a coherent cryptographic-agility substrate across the 60-year horizon.
- **§4.3.2 amendment** &mdash; cross-references the §10.53 NORMATIVE-when-applicable LIFT.

### Added (design)

- **`docs/design/15-civic-ai-and-post-quantum.md`** (NEW) &mdash; design rationale for §10.51-§10.55. Auditor's-lens review covers DP-correctness audit (out-of-band), model-card publication discipline, hybrid-PQ migration, decadal re-seal generation chain, civic-AI challenge-response composition.
- **`docs/regulator-pack/civic-ai-overlay.md`** (NEW) &mdash; operational mapping of §10.51-§10.55 to EU AI Act Article 14, GDPR Article 22, OECD AI Principles, NIST AI RMF, parliamentary-inquiry / public-records requests. Covers the Helvetian Federal Tax Authority-shape audit scenario.
- **`docs/regulator-pack/long-retention-overlay.md`** (NEW) &mdash; operational mapping of §10.53 + §10.54 + GAP-6 to Swiss federal tax archive law (60 years), ICAO Annex 13 (50 years), U.S. clinical-trial archival, DFARS 252.204-7012, long-arc litigation hold.
- **`docs/design/08-test-vectors.md`** &mdash; vectors 045-048 + N033-N035 added to the index.

### Test vectors

Shipped under PRD-6 / 0.1.0-draft.6:

- `045-public-transparency-dp-aggregate` (§10.51) &mdash; Helvetian VAT-audits-initiated DP-noised monthly aggregate. Canonical bytes `731`; SHA-256 `9900eff01bce842a2a5e11ea0caa67065dc006faf355c37675a1627250e185d4`.
- `046-public-model-card-binding` (§10.52) &mdash; Helvetian VAT audit-target model card publication via §10.19 reuse with `kind = "model_card"`. Canonical bytes `438`; SHA-256 `21183a9e8be95ae8fbfb82171a05ee28e9066c7ea76b5354756754b4e461306f`.
- `047-decadal-resealing` (§10.54) &mdash; Helvetian first-decadal re-seal at 2036-12-31 boundary under Dilithium3 (generation 1). Canonical bytes `457`; SHA-256 `0f47bc32665a8d021a2a5243508d2a18e2d7ed1add54c55fa0431722d35112de`.
- `048-challenge-response-disposition` (§10.55) &mdash; Helvetian taxpayer challenge dispositioned `overturned` by an administrative-law judge. Canonical bytes `934`; SHA-256 `63d81cf7f84bffe8f59b7a74b72b17bf4b61f089fdc1202279e58afab39c66ea`.
- Negative vectors `N033` (DP noise seed tampered), `N034` (decadal re-seal previous-generation anchor mismatch), `N035` (challenge-response disposition out of order).
- §10.53 byte form is pinned by EXISTING vector `015-dual-algorithm-cosigned-seal` (NORMATIVE-when-applicable lift; no new vector).

### Reference implementation

Both Python and .NET implementations ship Phase 8 with cross-impl byte-equivalence pins:

- Python: `_public_transparency.py` (NEW, §10.51 + §10.52 with GAP-8 internal helpers — single consumer; no separate primitive), `_resealing.py` (NEW, §10.54), `_challenge_response.py` (NEW, §10.55). All three consume `_envelope_utils.py`. `_challenge_response.py` additionally consumes `_state_machine.py` and `_human_review.py`. `_resealing.py` reuses `_merkle_disclosure.py`.
- .NET: `PublicTransparency.cs`, `Resealing.cs`, `ChallengeResponse.cs` (all NEW). All three consume `EnvelopeUtils.cs`. `ChallengeResponse.cs` additionally consumes `StateMachine.cs` and `HumanReview.cs`. `Resealing.cs` reuses `MerkleDisclosure.cs`.
- Cross-impl byte-equivalence pins: vectors 045 / 046 / 047 / 048 — Python and .NET produce byte-identical canonical bytes and identical SHA-256 hex digests.

### Wire-format identifier

`"v1"` &mdash; unchanged. The Phase 8 extensions are additive within `"v1"`. New attribute families (`audit.public_transparency.*`, `audit.challenge_response.*`) and new seal-namespace attributes (`seal.resealed_*`) are additive; existing chains remain valid. §10.53 NORMATIVE-when-applicable lift uses the existing dual-algorithm signature pair from §4.3.2 (no wire-format change).

### Pre-mortem reversals (recorded for posterity)

The Phase 8 design produced six reversals from the manifest's initial calls — captured before any code was written via the-fool devil's-advocate review:

1. **GAP-8 ships as `_public_transparency.py`-internal helpers** (NOT a separate shared primitive). One consumer; CUPID-Domain — over-abstraction avoidance. Phase 6 GAP-2 (3+ consumers) and Phase 7 GAP-5 (2+ consumers) earned standalone primitive treatment; GAP-8 has not.
2. **§10.51 binds the NOISED aggregate (not raw)** + DP parameters per §1.2's public-transparency epistemic claim. The chain is the integrity foundation; DP correctness is the regulator's audit.
3. **§10.52 reuses §10.19 with `kind = "model_card"`** (NO new event family). Pure §10.19 reuse with the canonical kind discriminator.
4. **§10.53 LIFTS existing §4.3.2 dual-algorithm posture** from RECOMMENDED to NORMATIVE-when-applicable (NO new wire form; vector 015 IS the existing byte pin).
5. **§10.54 = annotated seal per §10.42 precedent** (NO new wire-format kind). Decadal re-sealing is operationally a one-time signing event at each decadal boundary — same shape as backfill-seal at acquisition close.
6. **§10.55 = parallel to §10.50** (GAP-2 state-machine + GAP-5 HITL composition). Civic-AI sibling of clinical output-grounding review; same composition shape, different domain.

---

## [0.1.0-draft.5] &mdash; 2026-05-09 (in progress)

### Added (4 reference-spec extensions, normative — Phase 7 / Story 16)

The Phase 7 wave addresses generative AI / RAG / clinical decision support under chain-of-custody. Four new sections close the Story-16 (Lyceum Health) integration gaps:

- **§1.2 Stochastic-output epistemic claim (informative — GAP-4 closure)** &mdash; new paragraph in §1.2's epistemic-scope text qualifying the "what the AI said at time T" claim for stochastic outputs: "given the bound seed, temperature, top-p, top-k, model version, model weight hash, and retrieval-set Merkle root." Reproducibility tests run out-of-band against the bound parameters; the chain is the integrity foundation, not the truth foundation. No normative §7 implications; the verifier dispatches on parameter presence + bounds, not reproducibility.
- **§10.47 Generation prompt/output four-tuple binding** &mdash; new `audit.generation.*` operational event with single-chain-entry binding for system_prompt_sha256, user_prompt_sha256, retrieval_set_merkle_root_sha256 (RECOMMENDED when RAG operates), output_sha256, model_id, inference_at_utc. Discrete-decision shape (one inference, one chain entry); streaming chunked outputs bind the complete output at stream-finish time.
- **§10.48 Stochasticity attestation (extension to §10.47)** &mdash; optional fields (temperature, top_p, top_k, seed, model_version, model_weight_hash) on the §10.47 event for institutions operating under reproducibility-bound regimes. Bounds normate `temperature ∈ [0.0, 2.0]`, `top_p ∈ [0.0, 1.0]`, `top_k ≥ 0`. Verifier dispatches on field presence; absent fields signal a non-reproducibility-bound regime.
- **§10.49 Retrieval-source integrity** &mdash; retrieval-set Merkle root bound on §10.47 + per-document anchor events (`audit.retrieval.document_anchor.*`) cross-bound via parent_run_id/parent_seq. Closed `canonical_identifier_kind` enumeration: `pmid` / `doi` / `isbn` / `institutional_doc_id` / `fda_label_id` plus institution-named values per CC8.1. Reuses §10.31 cohort subtree disclosure for selective audit; reuses §4.2 / §10.37 RFC 6962 Merkle — zero new Merkle code.
- **§10.50 Output-grounding event family** &mdash; new `audit.review.*` chain-entry event family composing §1.5 / GAP-2 state-machine (pending_review → reviewed[outcome]) with GAP-5 HITL signed-review primitive. Closed canonical outcome enumeration: `clinician_edit` / `grounding_pass` / `grounding_fail` / `hallucination_detected` plus institution-named outcomes per CC8.1.

### Added (1 cross-cutting primitive — GAP-5 closure)

- **GAP-5 HITL signed-review-event primitive** &mdash; minimal shared substrate (~100 LOC per impl) consumed by §10.50 (this Phase) and §10.55 (forthcoming Phase 8). Six-field `audit.signed_review.*` chain-entry attribute schema: reviewer_id, reviewer_role, reviewer_public_key_fingerprint, signed_at_utc, signed_payload_sha256, signature_b64. Per-reviewer key-registry Protocol; canonical-bytes signing helper. Verifier dispatch checks: (b) reviewer-key binding against registry, (c) signed-payload SHA-256 binding against canonicalized payload bytes. Cryptographic signature verification is institution-side (the primitive does NOT perform Ed25519 / ECDSA verification — that's the institution's cryptographic-library responsibility).

### Added (design)

- **`docs/design/14-generation-and-hitl.md`** (NEW) &mdash; design rationale for §1.2 amendment + §10.47-§10.50 + GAP-5. Auditor's-lens review covers stochasticity-attestation regime, empty retrieval set, clinician edit + re-review, reviewer-key revocation, model_weight_hash unknown to institution, GDPR Article 22 composition.
- **`docs/regulator-pack/healthcare-genai-overlay.md`** (NEW) &mdash; operational mapping of §10.47-§10.50 to FDA 21 CFR Part 11, HIPAA, EU AI Act Article 14, GDPR Article 22, and academic-medical-center vendor due-diligence. Covers the Lyceum × Cleveland Clinic-shape audit scenario.
- **`docs/design/08-test-vectors.md`** &mdash; vectors 041-044 + N030-N032 added to the index.

### Test vectors

Shipped under PRD-5 / 0.1.0-draft.5:

- `041-generation-four-tuple` (§10.47 + §10.48) &mdash; Lyceum-shape clinical decision support generation event with full §10.48 stochasticity attestation. Canonical bytes `813`; SHA-256 `dc74a6527ed19078aaa42e325c01b6bb5493a536c95111e87a88e4d11ee1cb30`.
- `042-retrieval-set-merkle` (§10.49) &mdash; four PubMed-anchored retrieval-document anchor events + Merkle root over their leaves. Per-anchor SHA-256 bytes `541` each. Retrieval-set Merkle root: `2aefda83d3521600b0b408d2c3d66e0e7d6e962490703774084f57323874a148`. The Merkle root cross-binds to case 041's `retrieval_set_merkle_root_sha256` field.
- `043-output-grounding-review` (§10.50) &mdash; Lyceum clinician's `grounding_pass` review composing §10.43 / §1.5 state-machine with GAP-5 HITL signed-review. Canonical bytes `847`; SHA-256 `76c9f96664ad76a281c6889be47e748df864a0c06e15f4ab3b8f62a296f69ee9`.
- `044-human-review-primitive` (GAP-5) &mdash; the standalone signed-review-event primitive shape, isolated from §10.50 wrapping. Canonical bytes `565`; SHA-256 `05c072eb447b17879661d248d11e2964ff6e34a80d0d11606dd5a53ee8d55ea7`. The primitive's byte form is embedded inside case 043's `audit.review.signed_review`.
- Negative vectors `N030` (output_sha256 mismatch), `N031` (retrieval-set Merkle root tampered), `N032` (HITL signature does not verify under declared reviewer key).

### Reference implementation

Both Python and .NET implementations ship Phase 7 with cross-impl byte-equivalence pins:

- Python: `_human_review.py` (NEW, ~140 LOC GAP-5 primitive), `_generation.py` (NEW, §10.47 + §10.48), `_retrieval_anchor.py` (NEW, §10.49), `_review.py` (NEW, §10.50). All four consume `_envelope_utils.py`. `_review.py` additionally consumes `_state_machine.py` (Phase 6) and `_human_review.py` (this Phase). `_retrieval_anchor.py` reuses `_merkle_disclosure.py`'s canonical RFC 6962 Merkle construction.
- .NET: `HumanReview.cs`, `Generation.cs`, `RetrievalAnchor.cs`, `Review.cs` (all NEW). All four consume `EnvelopeUtils.cs`. `Review.cs` additionally consumes `StateMachine.cs` and `HumanReview.cs`. `RetrievalAnchor.cs` reuses `MerkleDisclosure.cs`.
- Cross-impl byte-equivalence pins: vector 041 generation event (with §10.48 stochasticity), vector 042 first anchor + retrieval-set Merkle root, vector 043 review event with embedded signed-review, vector 044 standalone signed-review primitive.

### Wire-format identifier

`"v1"` &mdash; unchanged. The Phase 7 extensions are additive within `"v1"`. New attribute families (`audit.generation.*`, `audit.retrieval.document_anchor.*`, `audit.review.*`, `audit.signed_review.*`) are additive; existing chains remain valid.

### Pre-mortem reversals (recorded for posterity)

The Phase 7 design produced reversals from the manifest's initial calls — captured before any code was written via the-fool devil's-advocate review:

1. **§10.49 Merkle root + per-document anchors** instead of inlining all retrieval-doc hashes on §10.47. Reuses §10.31 cohort subtree disclosure for selective audit; avoids 8KB+ inline arrays per chain entry. Mirrors Phase 5's §10.42-via-annotation reversal: extend existing primitives instead of inlining.
2. **§10.50 composes state-machine + HITL** instead of being a flat event family. The `pending_review → reviewed[outcome]` lifecycle IS state-machine-shaped; combining GAP-2 (Phase 6) + GAP-5 (this Phase) + §10.50 outcome enum is the right shape. §10.55 (Phase 8 challenge response) reuses the same composition.
3. **§10.48 OPTIONAL extension fields on §10.47** instead of separate event. Preserves the "one inference, one chain entry" shape; institutions that don't operate under stochasticity attestation simply omit the fields.
4. **GAP-4 informative §1.2 amendment** instead of normative §7 impact. The chain binds the parameters; reproducibility is the regulator's audit. Same shape as §1.2's existing factual-accuracy / statistical-bias non-claims.
5. **GAP-5 minimal HITL primitive** (~100 LOC) instead of broader abstraction. Same logic as Phase 6's GAP-2 reversal: shared plumbing is small; per-domain semantics is bulk.

---

## [0.1.0-draft.4] &mdash; 2026-05-09 (in progress)

### Added (4 reference-spec extensions, normative — Phase 6 / Story 15)

The Phase 6 wave of the §10.39-§10.55 forthcoming-stories rollup addresses long-running case records and multi-party insurance flows. Four new sections close the Story-15 (Polaris Reinsurance × Lloyd's) integration gaps:

- **§1.5 Decision-event vs state-machine modeling (informative)** &mdash; new normative-framing subsection naming the seam between discrete-decision records (existing v1.0 shape) and long-running case records (claims, disputes, audit examinations, complaints, litigation holds). Frames §10.43, §10.46, and (forthcoming) §10.55 as state-machine consumers; the shared substrate lives in `_state_machine.py` / `StateMachine.cs` per GAP-2.
- **§10.43 Claim-state-machine chain entries** &mdash; new `chain.claim_state.transition` operational events for chain-of-custody-bound insurance claims. Closed normative high-level enum (`opened` / `pending` / `decided` / `closed`); institution-named substates per CC8.1. Carries actor, rationale, optional authorizing-policy reference + SHA-256, and strict RFC 3339 UTC timestamp. Consumes the GAP-2 state-machine primitive for lifecycle coherence.
- **§10.44 Cession-cohort recursive subtree disclosure (normative when applicable)** &mdash; spec-section anchor for the §10.31 role-aware extension. The `audit.disclosure.role.*` attribute family (`cedent` / `reinsurer` / `retrocessionaire` / `independent_third_party_adjuster` / `importer` / `customs_broker` / `regulator_observer` plus institution-named values) layers per-cohort subtrees through §10.37 hierarchical Merkle aggregation. **Reuses the existing §10.31 + §10.37 substrate — no new Merkle code.**
- **§10.45 Independent third-party adjuster anchor** &mdash; new STANDALONE section (NOT a §10.21 extension; the directionality is bidirectional vs §10.21's one-way deliverer→recipient). New `chain.adjuster_anchor` operational event with `peer_party_chain_entries` array enabling reverse-link verification across multi-party chains. Cross-impl byte-pin against vector 039.
- **§10.46 Bordereau integrity** &mdash; new chain-entry event family (`audit.bordereau.published` → `received` → `reconciled` → optional `discrepancy_resolved`) for periodic risk-cession statement integrity. Mirrors §10.38 consent's lifecycle pattern. Reuses GAP-2 state-machine primitive for lifecycle validation. The bordereau document itself is hash-anchored via §10.19 `audit.external_artifact.*` family. Carries the GAP-3 informative note pointing actuaries at §10.34 as the existing recurring-computation integrity substrate for reserve calculations.

### Changed

- **§10.31 Per-cohort subtree disclosure** &mdash; extended with the role-aware recursive paragraph supporting §10.44. Adds the `audit.disclosure.role.*` attribute family (party_role / party_identifier / parent_role) for multi-party flows. The single-level subtree path is unchanged; multi-party deployments opt in by emitting the role attribute.

### Added (design)

- **`docs/design/13-state-machine-and-multi-party-flows.md`** (NEW) &mdash; design rationale for §1.5 + §10.43-§10.46. Auditor's-lens review covers run_id reuse across institutions, unstructured PDF activity records, bordereau hash mismatches, claim reopens, and jurisdictional layering.
- **`docs/regulator-pack/naic-market-conduct-overlay.md`** (NEW) &mdash; operational mapping of §10.43-§10.46 to NAIC Market Regulation Handbook examination procedures. Covers the Polaris × Lloyd's-shape cross-jurisdictional scenario, third-party adjuster engagement-contract requirements, and discrepancy-handling discipline.
- **`docs/design/08-test-vectors.md`** &mdash; vectors 037-040 added to the index.

### Test vectors

Shipped under PRD-4 / 0.1.0-draft.4:

- `037-state-machine-transition-validator` (§1.5 / GAP-2) &mdash; transition-table walk validator across 4 walks (happy path, skip-pending, out-of-terminal, history-gap). Canonical bytes `1032`; SHA-256 `23fd87b2a573ca29ece4015c52575f90f429c677d8278ee0fe06026d10a67b3f`.
- `038-claim-state-lifecycle` (§10.43) &mdash; Polaris/Lloyd's-shape 6-transition lifecycle. Per-event byte hashes pinned (event[0] SHA-256 `9bf730ca86a660ec4d655ea442df2662a22ab30f6bb94c19ddfc8e3d7ba84a98`); lifecycle digest `2255016bf1b9b82cf4b6bd86fba51c48ef03504ac9fb92b061dba783201a17d7`.
- `039-adjuster-anchor-bidirectional` (§10.45) &mdash; cedent-side and reinsurer-side bidirectional anchor byte forms. Cedent SHA-256 `d8df3fe5cd69eb7bb408a5eacdeb31a22e0861cc6ac3ae8a862548c0d03b4101`; reinsurer SHA-256 `03905ac5bbed6c23b86b2a3e76dff35f2d18cb7233f98e29bc7fead929048588`.
- `040-bordereau-lifecycle` (§10.46) &mdash; clean three-event lifecycle (published / received / reconciled[clean]). Published event SHA-256 `84425701453b19eeb7758de5afda62ae85d84234721ffc1802cf07342d97f7d0`; lifecycle digest `5443f77fdc0bbe1912c2c98bd05d57f248df316562bea5806fe72826bb1342f2`.
- Negative vectors `N027` (state-machine transition out of terminal), `N028` (adjuster anchor missing reverse-link), `N029` (bordereau reconciled-before-received).

### Reference implementation

Both Python and .NET implementations ship Phase 6 with cross-impl byte-equivalence pins:

- Python: `_state_machine.py` (NEW, ~80 LOC GAP-2 primitive), `_claim_state.py` (NEW, §10.43), `_adjuster_anchor.py` (NEW, §10.45), `_bordereau.py` (NEW, §10.46). All four consume the existing `_envelope_utils.py` validators (RFC 3339, SHA-256 hex, identifier, strict base64) and `_state_machine.py` for lifecycle coherence.
- .NET: `StateMachine.cs`, `ClaimState.cs`, `AdjusterAnchor.cs`, `Bordereau.cs` (all NEW). All consume `EnvelopeUtils.cs` and `StateMachine.cs`.
- Cross-impl byte-equivalence pins: vectors 037, 038 event[0], 039 cedent, 040 published.

### Wire-format identifier

`"v1"` &mdash; unchanged. The Phase 6 extensions are additive within `"v1"`. New attribute families (`audit.claim_state.*`, `audit.adjuster_anchor.*`, `audit.bordereau.*`, `audit.disclosure.role.*`, `audit.state.transition.*`) are additive; existing chains remain valid.

### Pre-mortem reversals (recorded for posterity)

The Phase 6 design produced three reversals from the manifest's initial calls — each captured before any code was written via the-fool devil's-advocate review:

1. **GAP-2 state-machine primitive stays MINIMAL (~80 LOC)** instead of the manifest's proposed broader abstraction. The shared *plumbing* across §10.43 / §10.46 / §10.55 is real; the shared *semantics* is not. The seam is the chain-entry attribute schema and the transitions-table walk; everything else stays per-section.
2. **§10.44 reuses §10.31 + §10.37 instead of introducing a new HierarchicalDisclosure primitive.** §10.37 already does depth-N hierarchical Merkle; §10.44 is the composition of §10.31's cohort filter with §10.37's hierarchical Merkle plus a role attribute per level. Implementation cost: zero new Merkle code.
3. **§10.45 standalone instead of §10.21 extension.** §10.21 is one-way deliverer→recipient; §10.45 is bidirectional. Different domains. CUPID-Domain-based: schemas would have become incoherent under §10.21.
4. **§10.46 mirrors §10.38 consent (lifecycle event family) instead of §10.42 backfill (annotated seal).** Bordereaux are events in a lifecycle, not periodic seals. The lifecycle-coherence verifier check reuses GAP-2's `_state_machine.py` primitive.

GAP-3 (actuarial reserve-calculation integrity) ships as informative composition note in §10.46, citing §10.34 as the existing recurring-computation substrate. No graduation needed without an operational driver.

---

## [0.1.0-draft.3] &mdash; 2026-05-09 (in progress)

### Added (4 reference-spec extensions, normative — Phase 5 / Story 14)

The Phase 5 wave of the §10.39-§10.55 forthcoming-stories rollup (per `docs/future-needs/gap-wish-manifest.md`) addresses the cross-vendor-target M&A subcase. Four new sections close the §10.24 chain-discontinuity gap when an acquirer absorbs a target whose pre-acquisition records are not under a Herald-conformant chain:

- **§10.39 Institutional successor-attestation** &mdash; new `chain.successor_attestation` operational event the acquirer's chain emits at acquisition close. Carries the acquired-institution legal name, RFC 9101 LEI, baseline-manifest SHA-256, baseline-manifest kind (`prior_vendor_chain` / `prior_vendor_signed_pdfs` / `baseline_diary` / `mixed`), acquirer-HSM key fingerprint, effective UTC, §10.17 dual_signatures pair, and (when applicable) companion §10.42 backfill-seal run_id.
- **§10.40 Cross-vendor chain-merge cross-anchor (normative when applicable)** &mdash; generalizes §10.21 cross-vendor-handover for the foreign-vendor-chain inheritance case; foreign-vendor signed roll-up artifacts are hashed and anchored under §10.19's `audit.external_artifact.*` family. No new validator code — the verifier already supports anchor-attribute verification — but §10.39's normative MUST mandates emission when `baseline_manifest_kind ∈ {"prior_vendor_chain", "prior_vendor_signed_pdfs", "mixed"}`.
- **§10.41 Chain-coverage-map M&A temporal-slice extension** &mdash; extends §10.19 to require three named partitions (pre-acquisition / cut-over window / post-cut-over) in the chain-coverage map during the M&A cut-over window. The window is what an 18-month-lookback auditor reads to reconstruct the migration state at any moment of the cut-over.
- **§10.42 Backfill seal discipline** &mdash; new one-time backfill seal record at acquisition close when the acquired entity's pre-acquisition records are under a non-chain shape. The backfill seal is a v1.0b sign_payload-bound seal record where the §10.42 attributes (`seal.backfill_at_close = true`, window timestamps, baseline-manifest cross-binding hash, companion attestation run_id, dual_signatures) are bound through the Merkle root via a metadata leaf. Locked v1.0b 12-line wire form is unchanged.

### Changed

- **§10.24 Entity succession** &mdash; amended with a 3-paragraph composition note covering the cross-vendor-target subcase. The §10.24 lineage is preserved (acquirer's representation cites §10.24 by section number); the cryptographic-inheritance work lives in §10.39 / §10.40 / §10.42 as the cross-vendor-target complement.
- **§10.12 Verifier CLI exit-code contract** &mdash; amended with a normative paragraph on the `additional_verifications` array. Bonus verifications (§10.42 backfill-seal-verified, future hybrid-PQ dual-signature) report through the structured verdict's array, NOT through new exit codes. Codes 0-6 remain the closed enumeration. The discipline saves the §10.12 contract from combinatorial blow-up across the §10.27-§10.55 wave.
- **`docs/m-and-a-handoff.md`** &mdash; extended with the cross-vendor-target onboarding section (operational shapes A / B / C, cut-over window discipline, pre-close due-diligence note) and cross-references to §10.39-§10.42.

### Added (design)

- **`docs/design/12-successor-attestation-and-backfill.md`** (NEW) &mdash; design rationale for §10.39 + §10.42 paired with the four pre-mortem reversals from the Phase 5 design-review. Auditor's-lens review covers HSM-compromise, kind-enumeration motivation, shell-corp acquisition edge case, encrypted-at-rest baseline records, and the open-issue around foreign-vendor-artifact retention contracts.
- **`docs/design/07-verifier-design.md`** &mdash; new §11 on the verdict object and `additional_verifications` array discipline.
- **`docs/design/08-test-vectors.md`** &mdash; vectors 034/035/036 added to the index.

### Test vectors

Shipped under PRD-3 / 0.1.0-draft.3:

- `034-successor-attestation` (§10.39) &mdash; envelope canonical bytes pin (839 bytes; SHA-256 `1cc371b8fff05ee5bb420753c04ea6f1883297b615911dc5824e65ed1a1f1935`)
- `035-backfill-seal` (§10.42) &mdash; metadata-leaf canonical bytes pin (728 bytes; SHA-256 `b55c05cc7a7b5245cfccfd7be293d8d2bbfe360ba6fba341809f4960a68ce3c2`); Merkle root over (8 baseline + 1 metadata) leaves under canonical RFC 6962 (`8943b16ee4fdb413e849c6909c5d79b71fa96962a5710cdd6a763bf09342c340`); v1.0b sign_payload byte form (286 bytes; SHA-256 `826a53072ffbcbf74b549bca167374ffa513205b842e9d1a31117482a2fdcf0c`).
- `036-verdict-additional-verifications` (§10.12 amendment / design 07 §11) &mdash; three sub-cases pinning the verdict-object structured form: PASS empty array (45 bytes), PASS with `["backfill_seal_verified"]` (69 bytes), PASS with two values forward-compat for §10.53 (106 bytes).
- Negative vectors `N024` (acquirer-HSM signature mismatch) `N025` (backfill Merkle root corruption) `N026` (additional_verifications invalid string under `--strict`).

### Reference implementation

Both Python (`Herald.Py/src/herald/`) and .NET (`Herald/Modules/Herald.Compliance/src/Audit/Chain/`) implementations ship Phase 5 with cross-impl byte-equivalence pins:

- Python: `_envelope_utils.py` (NEW, shared base64/SHA-256/length validators), `_successor_attestation.py` (NEW, §10.39), `_backfill_seal.py` (NEW, §10.42), `_attestation.py` (refactor to consume `_envelope_utils.py`), `_verdict.py` (extended with `Verdict` dataclass + `BACKFILL_SEAL_VERIFIED` constant), `_streaming_verifier.py` (extended with `note_additional_verification` and `finalize_verdict`).
- .NET: `EnvelopeUtils.cs`, `SuccessorAttestation.cs`, `BackfillSeal.cs` (NEW), `Attestation.cs` (refactored), `VerifierVerdict.cs` (extended with `Verdict` class + `AdditionalVerifications` enum), `StreamingVerifier.cs` (extended). Builder-track helper `MAndAOnboardingBuilder.cs` provides the M&A two-record bundle from one set of inputs.
- Cross-impl byte-equivalence pins: vector 034 envelope SHA-256, vector 035 metadata-leaf SHA-256, vector 035 Merkle root, vector 036b verdict SHA-256.

### Wire-format identifier

`"v1"` &mdash; unchanged. The Phase 5 extensions are additive within `"v1"`. The §10.42 backfill seal is a v1.0b sign_payload record (NOT a new top-level wire-format kind); the §10.42 attributes ride through the Merkle leaf they hash into. The verdict object's `additional_verifications` field is metadata that travels alongside the integer exit code; the 0-vs-non-zero CLI contract is preserved.

### Pre-mortem reversals (recorded for posterity)

The Phase 5 design produced four reversals from the manifest's initial calls — each captured before any code was written via the-fool devil's-advocate review:

1. **§10.39 stays a separate primitive** (manifest agreed) but extracts a small shared `_envelope_utils.py` / `EnvelopeUtils.cs`. Forcing reuse of §10.35's platform-dispatch table would have been a leaky-base-class antipattern.
2. **No new exit code 7** for `BACKFILL_SEAL_VERIFIED`. Adding "PASS + bonus" verdicts produces combinatorial blow-up across §10.42, §10.53 (would have wanted 8/9), and future bonus verifications. The `additional_verifications` array on the structured verdict object absorbs the entire wave through one schema field.
3. **No new top-level wire-format kind for the backfill seal**. §10.36 already established the supplemental-seal annotation pattern; §10.42 follows the precedent. Wire-format identifier `'v1'` survives untouched.
4. **GAP-1 reduces to a §10.24 composition note**, not a new §10.24.2 subsection. §10.24 already covers institutional succession; the actual gap is the cross-vendor-target subcase, which §10.39 + §10.42 normate.

---

## [0.1.0-draft.2] &mdash; 2026-05-08 (in progress)

### Added (informative)

- **§0.5 How to read this document** &mdash; 30-minute reading-path on-ramp for first-time readers. Three-paragraph chain summary, one-diagram flowchart of the four primitives, role-keyed reading-path table with time budgets and companion-document anchors for twelve roles, five-minute triage path, and pointer to auditor stories / question bank / reference implementation as the layered companions to the normative spec. No wire-form change, no normative content. Inserted between §0 and §1 so a reader who opens the spec cold lands in role-orientation before normative content begins.

### Added (12 reference-spec extensions, normative)

Twelve extensions surfaced through deployment field-engagements and rolled into the reference spec under §10:

- **§10.27 Configurable seal cadence** — per-second through weekly; streaming-mode for real-time decisioning institutions.
- **§10.28 Streaming-mode IKM rotation discipline** — rotation crossing the cadence-interval boundary at sub-daily cadence.
- **§10.29 Streaming-mode verifier procedure** — incremental verdicts as the chain stream ships; new exit codes 4/5/6.
- **§10.30 Trusted-time integration normative for streaming-mode** — RFC 3161 / GPS-disciplined / NIST integration required at sub-daily cadence; new `clock.drift_detected` operational event.
- **§10.31 Per-cohort subtree disclosure** — Merkle subtree extraction for issuer / region / model-version slices; verifier partial-disclosure mode extends.
- **§10.32 Per-device session key derivation** — HKDF info parameter extended with `device_id` for edge-deployed institutions.
- **§10.33 Model-update events** — new `audit.model_update.*` family covering push / pull / verify / activate at the deployment-phase boundary.
- **§10.34 Training-phase integrity** — new `audit.training.*` family covering local_gradient / aggregation / validation / model_artifact; §1 scope expanded to include training-phase. Cross-anchored to deployment-phase via `audit.model_update.*` per §10.33.
- **§10.35 Edge-attestation primitive** — TEE / TPM / Secure Enclave attestation document bound to chain entries; verifier validates against platform-vendor attestation root at chain-walk time.
- **§10.36 Late-arriving-entry seal discipline** — Pattern A (supplemental seal) and Pattern B (rolling seal window) for offline-first edge deployments.
- **§10.37 Hierarchical Merkle aggregation** — bandwidth-efficient two-level (or N-level) Merkle for edge-deployed institutions with constrained connectivity.
- **§10.38 Consent capture** — new `audit.consent.*` family covering given / referenced / withdrawn / expired lifecycle events; supports DPDP Act, GDPR Article 6(1)(a), CCPA, PIPA, LGPD, etc.

### Changed

- **§1 Scope** updated — training-phase integrity is in scope (was previously deferred). Inference-phase and training-phase chains compose via cross-anchor patterns per §10.21 and §10.33.

### Test vectors

Shipped under PRD-2 / 0.1.0-draft.2:

- `017-merkle-inclusion-partial-disclosure` — single-leaf partial-disclosure structural fixture
- `018-sign-payload-v1.0b` — streaming-mode sign_payload pin
- `019-sign-payload-v1.0b-empty-day` — empty-day variant of the v1.0b sign_payload
- `020-streaming-seal-cadence-1s` (§10.27)
- `021-rotation-completed-event-payload` (§10.28)
- `022-streaming-verifier-incremental` (§10.29)
- `023-merkle-inclusion-proof-rfc6962` (§10.31)
- `024-per-device-derivation` (§10.32)
- `025-attestation-android-keystore` (§10.35) — Android Keystore platform; Apple-Secure-Enclave companion planned for v1.x
- `026-hierarchical-merkle-aggregation` (§10.37)
- Negative vectors `N017` through `N023` covering dual-algorithm posture cases (§7 step 11), routing-event tampering (§4.4.1), and `format_version` case-variant rejection.

Planned for v1.x (sections whose schemas ship under PRD-2 without byte-level fixtures):

- §10.30 trusted-time integration — clock-drift and trusted-time-source fixtures
- §10.33 model-update events — four-event sequence pin
- §10.34 training-phase integrity — per-device local-gradient and aggregator-side aggregation/validation fixtures
- §10.36 late-arriving-entry seal discipline — Pattern A (supplemental) and Pattern B (rolling window) fixtures
- §10.38 consent capture — four-event consent-lifecycle pin

### Wire-format identifier

`"v1"` &mdash; unchanged. All extensions are additive within `"v1"`. New attribute families (`ffiec.chain.device_id`, `ffiec.chain.attestation`, `audit.model_update.*`, `audit.training.*`, `audit.consent.*`) are additive; existing chains remain valid.

---

## [0.1.0-draft.1] &mdash; 2026-05-08

### Added

- Initial public-comment release as **Public Review Draft 1 (PRD-1)**.
- Specification text (`spec/chain-of-custody-DRAFT-0.1.0.md`) lifted from the internal v1.0-final corpus.
- Conformance test-vector corpus (`spec/test-vectors/`).
- Audience-segmented supporting documentation (`docs/`).
- Ten design documents (`docs/design/`).
- Regulator-pack overlays (`docs/regulator-pack/`) covering FFIEC, NIST CSF 2.0, NYDFS Part 500, DORA, GDPR, HIPAA, BSA/AML, FedRAMP, APAC/Korea/Bank of Israel, CFPB.
- Eleven auditor-stories (`docs/auditor-stories/`).
- §0 Version policy distinguishing document version (`0.1.0-draft.1`) from wire-format identifier (`"v1"`).
- Submission-package skeleton (`submission/`).
- MkDocs documentation-site skeleton (`website/`).

### Changed

- Specification banner updated from "v1.0-final &mdash; Issued" to "Public Review Draft 1 (PRD-1)".
- README rewritten to frame the project as a proposed standard for public comment, replacing the implementation-focused README from the development repository.

### Removed

- Reference-implementation source code (Go modules &mdash; `core/`, `ledger/`, `verifier/`) is out of scope for this repository. The reference implementation is being conducted in a separate repository.
- Internal feedback rounds (`docs/feedback/`) and feedback-scrape automation are not part of the public-comment artifact set.

### Wire-format identifier

`"v1"` &mdash; unchanged. All test vectors valid.

---

[0.1.0-draft.1]: https://github.com/smuchow1962/ffiec-chain-of-custody/releases/tag/v0.1.0-draft.1
