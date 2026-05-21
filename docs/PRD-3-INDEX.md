# PRD-3 index - Public Review Draft 3 of the chain-of-custody specification

> **What this doc is.** Forward-looking index for PRD-3 (document version 0.3.0). PRD-3 rolls forward what was previously scheduled as PRD-4 (the 16-section Stories 18-20 wave at vectors 049-083) and bundles five spearhead advancements grounded in the May-21 points-beyond-Kognitos engineering analysis. PRD-3 ships as a draft amendment on top of PRD-2; the PRD-2 spec text (sections 0-13) remains stable, and PRD-3 advancements land in a new section 14 advancement appendix plus targeted refinements to the named PRD-2 sections.
>
> **Wire-format identifier.** v1 unchanged. All PRD-3 additions are additive within v1.
>
> **Document version.** PRD-2 = 0.2.0; PRD-3 = 0.3.0.

---

## 1. PRD-3 framing - the headline advance

PRD-3 advances chain-of-custody on five spearheads grounded in cross-Kognitos competitive analysis (the 11 surviving points beyond the Kognitos 12-field checklist) plus three pre-cited net-new attribute families Laura companion doc anchors. The headline: PRD-3 makes the chain credible against Daubert challenge AND under post-quantum migration AND with categorically-excluded content (SAR, attorney-client, FOIA exemption 5) all without breaking the v1 wire format.

The substrate inherited from PRD-2 remains intact. The chain operates on the same three primitives (per-event HMAC, daily Merkle seal, HSM signature), produces byte-identical output across reference implementations, and verifies under the same section 7 procedure. PRD-3 raises the conformance bar on cryptographic agility, categorical exclusion discipline, and reference-verifier distribution - it does not change what the chain captures or how the chain seals.

---

## 2. What rolls forward from PRD-4+

Everything previously scheduled for PRD-4 (CHANGELOG entry 0.1.0-draft.7) lands in PRD-3 instead. This consolidates the Stories 18-20 wave (vectors 049-083) into the same draft cycle as the five spearheads. Per Steve directive 2026-05-21.

Rolled forward from PRD-4 into PRD-3:

- Section 0.6 Navigation and contextual-help URL convention (normative)
- Section 7 Unknown wire-format kind fallthrough rule (normative)
- Section 10.21 amendments (10.21.1, 10.21.2, 10.21.3)
- Section 10.56 through 10.71 (16 Stories 18-20 sections covering HBOM chain integrity, firmware-attestation, component cryptographic identity, RMA discipline, anti-counterfeit cross-anchor, CMMC overlay, red/black separation, training-corpus provenance, training-run integrity, fleet attestation, model-weight lineage, evaluation chain, AISI overlay, customer disclosure, BSA SAR overlay, cross-institution wire chain)
- Test vectors 049-083 indexed at spec/test-vectors/PRD-4-INDEX.md (rename to PRD-3-INDEX.md). 35 vectors scheduled across Phase 11 (5 shared primitives) + Phase 12 (Story 18, 11 vectors) + Phase 13 (Story 19, 12 vectors) + Phase 14 (Story 20, 7 vectors).
- Section 5.0.1 Top-level wire-format kinds (normative)

---

## 3. The five spearheads as PRD-3 advancement targets

Each spearhead anchors to existing or new spec sections. Full advancement text lives in section 14 of the spec (new advancement appendix).

### Spearhead 1 - Multi-layer cryptographic defense

| Anchor | PRD-3 action |
|---|---|
| section 1.4 compositional security | Refinement: tighten the three-layer composition narrative (per-event HMAC + daily Merkle + HSM signature) as the load-bearing answer to single-layer competitor framings. No wire-form change. |
| section 4.1, 4.2, 4.3 | Refinement: cross-reference each primitive section to section 1.4 explicitly. No new code. |
| section 10.5 HSM custody | Refinement: tighten the separation-of-duties roster discipline. Names the three distinct role-bearers (SDK capture, ledger custody, HSM custodian). |

### Spearhead 2 - Daubert-grade testability

| Anchor | PRD-3 action |
|---|---|
| section 1.1 Daubert four-factor grounding | Refinement: add explicit per-factor citation from the four shipped artifacts (spec text, test-vector corpus, reference implementation, FIPS standards). |
| section 1.3 Security definitions | Refinement: tighten the per-primitive theoretical bound language. |
| section 7 verification procedure | Refinement: explicit cross-implementation byte-equivalence claim. |
| section 10.12 verifier exit-code contract | Refinement plus footnote: add footnote distinguishing which additional_verifications markers ship today vs which are reference-implementations-forthcoming. |
| section 10.26 reference verifier distribution | Refinement: tighten the open-verifier posture. Add Sigstore-alignment as informative reinforcement. |

### Spearhead 3 - Categorical exclusions by design

| Anchor | PRD-3 action |
|---|---|
| section 10.70 SAR / privileged-investigation overlay | Refinement: tighten regime_first_used_utc + regime_scope_filter_sha256 binding. Add normative substantive-reach limitation clarification. Status flag: NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14. |
| section 10.13.3 litigation-hold registry binding | Refinement: add audit.litigation_hold.* parser obligation note. Status flag: NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14. |
| section 10.69 per-customer disclosure | Refinement: tighten HKDF derivation discipline. Status flag: NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14. |

### Spearhead 4 - Post-quantum cryptographic agility

| Anchor | PRD-3 action |
|---|---|
| section 4.1.3 per-event MAC algorithm agility | New normative text: define payload_hash_alt optional field for HMAC-SHA-3 / HMAC-BLAKE3 dual-MAC. Status flag: NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PRD-3.1. |
| section 4.3.2 dual-algorithm post-quantum coexistence | Refinement: tighten the AND-security claim. No code change. |
| section 10.53 hybrid PQ seal mandate | Refinement: tighten the migration-window discipline. NIST IR 8547 2030-12-31 anchor remains in spec text; comments-surface text soften to the projected NIST PQC migration deadline. |
| section 10.54 decadal re-sealing | No change (already shipped). |

### Spearhead 5 - Examiner runs the verifier locally

| Anchor | PRD-3 action |
|---|---|
| section 10.26 reference verifier distribution | Refinement: explicit Sigstore-alignment language; clarify Herald-applies-established-open-verification-pattern framing per IP-defensibility preventive note 2. |
| section 10.13.1 discovery production form | Refinement: cross-reference the produce-a-discovery-packet code path obligation. Status: PRD-3.1 implementation. |
| section 5.2.1 FRE 902(13)/(14) self-authentication | No change. |
| section 10.12 verifier exit-code contract | See Spearhead 2 footnote. |

---

## 4. Net-new PRD-3 attribute families (Laura pre-cites)

Three net-new families land in PRD-3 section 14 appendix. All carry ASPIRATIONAL status flags.

### Section 14.1 audit.actor.* family (Seam D)

Closes the May-20 Richard coverage-audit gap for Field 3 (Authenticated human user identity):

- audit.actor.authenticated_user_id_hash (string, REQUIRED) - SHA-256 of canonicalized authenticated-user identifier (SSO-backed identity per institution CC8.1)
- audit.actor.authentication_method (string, REQUIRED) - closed enum: saml_sso, oidc_sso, mtls_workload, spiffe_workload, hsm_bearer_token, api_key_with_iam, institution_named
- audit.actor.session_id (string, RECOMMENDED) - the authentication session identifier the chain entry was emitted under
- audit.actor.delegation_chain (array, when applicable) - JCS-canonical lex-sorted array of delegated-authority identities

### Section 14.2 audit.reasoning.substrate_kind (Seam B)

Closes the May-20 Kognitos comparison-doc Point 8 gap. Closed canonical enumeration:

- neurosymbolic - the policy is the human-readable English (Kognitos English-as-Code architecture)
- retrieval_grounded_with_citations - reasoning supported by retrieved-document citations
- rule_based - deterministic rule engine
- post_hoc_llm_rationalization - reasoning generated AFTER the decision by an LLM (lowest trust class)
- attention_feature_importance - SHAP / attention-weights feature attribution
- none - no reasoning artifact captured (rare; institution CC8.1 explains)
- institution_named - per CC8.1

### Section 14.3 audit.downstream_action.* family

Closes the May-20 Richard coverage-audit recommended addition. Generalized system-of-record linkage:

- audit.downstream_action.action_kind (string, REQUIRED) - institution-named action class
- audit.downstream_action.system_of_record_id (string, REQUIRED) - institution-issued identifier for the system-of-record
- audit.downstream_action.change_record_id_hash (string, REQUIRED) - SHA-256 of the canonicalized system-of-record change record
- audit.downstream_action.applied_at_utc (RFC 3339 UTC, REQUIRED) - when the downstream system applied the change

---

## 5. Code-vs-claims audit summary

Full audit at E:/dev/Herald/Herald/wiki/PRD-3-CODE-VS-CLAIMS-AUDIT.md.

| Spearhead | Verdict | Action for PRD-3 |
|---|---|---|
| 1 Multi-layer crypto | PROVEN BY CODE + TEST | Ship refinement |
| 2 Daubert testability | PROVEN BY CODE + TEST | Ship refinement + section 10.12 footnote |
| 3 Categorical exclusions | CLAIMED BUT UNPROVEN | Path A: ship NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14 |
| 4 PQ cryptographic agility | PARTIALLY PROVEN | Ship; section 4.1.3 + section 10.53 dispatch flagged FORTHCOMING PRD-3.1 |
| 5 Examiner runs verifier | PROVEN BY CODE | Ship refinement + Sigstore-alignment language |

Three Laura pre-cited families all flagged ASPIRATIONAL - reference impl scheduled PRD-3.1.

Eleven of 21 verifier-dispatch markers in PRD-2 section 10.12 closed enumeration are normative-but-unimplemented. PRD-3 adds a footnote distinguishing implemented vs forthcoming markers.

Thirty-five test vectors (049-083) are indexed but not materialized on disk. PRD-3 recommends materializing the 5 Phase-11 shared-primitive vectors (049-053) before ship; vectors 054-083 flagged as scheduled for PRD-3.1 / Phase 12-14 release.

---

## 6. Open questions - six from points-beyond doc plus one new

Original six from the May-21 points-beyond doc:

1. Spearhead-5 framing - position examiner-runs-the-verifier-locally as single strongest distinguishing point, or kept inside a broader open-and-verifiable cluster? **RESOLVED 2026-05-21 - single strongest.** Positioning is single strongest distinguishing point per Steve's procurement-narrative read.
2. PRD-3 wave inclusion - should this document points-beyond surface in PRD-3 release notes as the procurement-narrative composite? **RESOLVED 2026-05-21 - deferred to wave-timing.** The points-beyond procurement-narrative composite lands when the wave it belongs to ships, not as a PRD-3 release-notes inclusion.
3. Categorical-exclusions framing risk - Spearhead 3 names SAR, attorney-client, regulatory-examination-privilege, grand-jury-6e in comments surface. Lead with architectural design and bury regime list, or lead with regime list? **RESOLVED 2026-05-21 - architecture-first.** Spearhead 3 framing leads with the architectural choice (the chain engineers the exclusion); the regime enumeration follows as the operational instantiation.
4. Discipline of restraint - is the 6-do-not-claim list internal or public? **RESOLVED 2026-05-21 - internal.** The discipline-of-restraint enumeration is operational guardrail for the writing team; it stays in the internal engineering surface, not in customer-facing documentation.
5. PQ-migration deadline anchor - keep 2030-12-31 hard-coded in spec, soften to the projected NIST PQC migration deadline in comments surface? **RESOLVED 2026-05-21 - keep in spec; soften in comments.** The 2030-12-31 anchor remains in spec text per NIST IR 8547. The customer-facing comments surface uses 'the projected NIST PQC migration deadline' phrasing so a date slip does not invalidate the marketing-surface copy.
6. Whitepaper 1 (Cross-institution wire) timing - wait for Fed registry, or publish ahead? **RESOLVED 2026-05-21 - wait for Fed; respond within 30 days.** Whitepaper 1 waits for the Federal Reserve voluntary cross-institution-anchor registry to publish; Herald responds within 30 days of the Fed publication.

New from the code-vs-claims audit:

7. Spearhead 3 Path A vs Path B - ship section 10.69 + section 10.70 as NORMATIVE - REFERENCE IMPLEMENTATIONS FORTHCOMING PHASE 14 (Path A, recommended), or gate PRD-3 ship on at least one reference impl shipping the primitives (Path B, 2-3 weeks delay)? **RESOLVED 2026-05-21 - Path A.** The canonical flag block "Reference-implementation status (normative-but-forthcoming)" is applied inline at every affected PRD-3 section. Sections carrying the flag: §4.1.3 (payload_hash_alt, PRD-3.1 signal), §10.13.3 (litigation-hold registry binding, Phase 14 / Story 20 wave signal), §10.53 (PQ migration-window verifier dispatch, PRD-3.1 signal), §10.69 (per-customer disclosure, Phase 14 / Story 20 wave signal), §10.70 (BSA SAR / privileged-investigation overlay, Phase 14 / Story 20 wave signal), §14.6 (audit.actor.*, PRD-3.1 signal), §14.7 (audit.reasoning.substrate_kind, PRD-3.1 signal), §14.8 (audit.downstream_action.*, PRD-3.1 signal). The spec text is the conformance bar today; the reference implementations and the corresponding test vectors are the signals that mark each section's reference-implementation landing.

---

## 7. Phase plan inside PRD-3

Phase 1 (immediate): spec advancement appendix section 14 written. CHANGELOG appended with 0.3.0 entry. README.md updated to reference 0.3.0.

Phase 2 (before ship): vectors 049-053 (Phase 11 shared primitives) materialized on disk (5 vectors, ~30 minutes each).

Phase 3 (PRD-3 ship): spec/chain-of-custody-DRAFT-0.3.0.md published; spec/README.md flips current-state pointer; PRD-3-INDEX.md replaces PRD-4-INDEX.md.

Phase 4 (PRD-3.1): section 4.1.3 payload_hash_alt reference implementation (C# + Python). Section 10.69 + section 10.70 reference implementations. Test vectors 077-080 materialized.

Phase 5 (PRD-3.2 / PRD-4 wave): Vectors 054-076 materialized (Phase 12-13 Stories 18-19). Stories 18-20 reference implementations in Vidimus + TesseraSeal.

---

## 8. Release-readiness checklist

Before PRD-3 ships, the following are required:

- [ ] Steve resolution on the 7 open questions (especially Path A vs B for Spearhead 3)
- [ ] spec/chain-of-custody-DRAFT-0.3.0.md written with section 14 advancement appendix
- [ ] spec/chain-of-custody-DRAFT-0.2.0.md retained for back-reference (do NOT delete)
- [ ] spec/README.md current-state pointer updated
- [ ] CHANGELOG.md appended with 0.3.0 entry
- [ ] PRD-3-INDEX.md replaces or supplements spec/test-vectors/PRD-4-INDEX.md
- [ ] Vectors 049-053 materialized (Phase 11 shared primitives)
- [ ] Sigstore-alignment language reviewed in section 10.26 advancement
- [ ] Laura companion doc citations cross-checked against PRD-3 section 14 family names
- [ ] section 10.12 footnote drafted distinguishing implemented vs forthcoming markers
- [ ] No code committed to ffiec-public (Steve preview gate)
- [ ] Glenn audit findings reviewed by Steve

---

## 9. Coordination touchpoints

- Dawn + Heather + Laura language cleanup pass: applies the IP-defensibility preventive notes (no English-as-Code; no Herald-invented-open-verifier-pattern). Their work does not touch spec text.
- Laura 12+5 PRD-3 points page: the three pre-cited new families (audit.actor.*, audit.reasoning.substrate_kind, audit.downstream_action.*) land in section 14.1, 14.2, 14.3 respectively. regime_scope_filter_sha256 cite resolves against PRD-2 section 10.70 line 4137-4138 (no change).
- Glenn code-vs-claims audit: full audit at E:/dev/Herald/Herald/wiki/PRD-3-CODE-VS-CLAIMS-AUDIT.md.

---

## 10. File paths

- This PRD-3 index: E:/dev/ffiec-public/docs/PRD-3-INDEX.md
- PRD-3 spec advancement: E:/dev/ffiec-public/spec/chain-of-custody-DRAFT-0.3.0.md (section 14 advancement appendix)
- PRD-2 spec (preserved): E:/dev/ffiec-public/spec/chain-of-custody-DRAFT-0.2.0.md
- Code-vs-claims audit: E:/dev/Herald/Herald/wiki/PRD-3-CODE-VS-CLAIMS-AUDIT.md
- Source: points-beyond doc at E:/dev/MMP.Media/_assistant_drafts/wiki/market-research/2026-05-21-points-beyond-kognitos-12-CONSOLIDATED.md
- Source: IP-defensibility comparison at E:/dev/MMP.Media/_assistant_drafts/wiki/market-research/2026-05-21-kognitos-12pt-how-they-vs-how-we-COMPARISON.md
- Test-vector index (rolled forward): E:/dev/ffiec-public/spec/test-vectors/PRD-4-INDEX.md (rename to PRD-3-INDEX.md at PRD-3 ship)
- Reference impl (C#): E:/dev/Herald/Modules/Herald.Compliance/src/Audit/Chain/
- Reference impl (Python): E:/dev/Herald.Py/src/herald/
