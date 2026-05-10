# Story 05 — Helmstad BioSciences (FDA BIMO pre-inspection readiness, Phase II NSCLC program)

**Story file:** `docs/auditor-stories/05-helmstad-biosciences.md`
**Engagement type:** FDA Bioresearch Monitoring (BIMO) pre-inspection readiness audit at a mid-size oncology biopharma running an AI clinical-trial-eligibility classifier on a Phase II NSCLC trial; chain live for 4 months, FDA inspectors arrive in 6 weeks.
**Posture going in:** Bifurcated readiness audit; institution-side ask is to "run BIMO readiness like the inspector will run it in six weeks."
**Outcome posture:** Gap-finding — 8 confirmations on the AI side (0 Gaps, 0 Partials); 4 Gaps + 6 Partials + 3 boundary-by-design items on the legacy side; plus one chain-revealed clinical-quality finding (EHR staging correction in the screening-to-enrollment window).

## Type of audit
A pre-inspection readiness audit framed against 21 CFR Part 11 electronic-records discipline, ICH GCP / E6(R3), and the December 2024 FDA AI/ML draft guidance. What makes it distinctive is the regulator-anticipation framing and the evidentiary cross-walk that maps chain-of-custody spec sections directly onto Part 11 inspector questions (§10.5 to Part 11 electronic-signature integrity, §4.1 to record-tamper detection, §4.3 to Part 11 §11.10 time-stamping, §10.3 to non-modification, §10.13 to Part 11 §11.10(e) documentation, §10.17 to dual-control electronic-signature ceremony, §10.22 to PHI-handling overlay).

## Interested parties (spec readers)
- **FDA Bioresearch Monitoring (BIMO) inspector** — pre-inspection readiness audit explicitly anticipating BIMO methodology; the inspector reads every artifact and runs the reference verifier in witness mode on a laptop they bring.
- **HHS Office for Civil Rights (HIPAA)** — PHI integrity in clinical-trial eligibility; minimum-necessary discipline at the pre-MAC redaction boundary.
- **Chief Compliance Officer / CRO** — combined Part 11 / ICH GCP / FDA AI/ML draft guidance posture across one engagement.
- **Model Risk Management committee chair** — eligibility-classifier deployment-intent capture and pre-deployment evaluation chain anchor SR 11-7 lifecycle reading.
- **Chief AI / ML Officer** — owns the SDK adoption scope; reads to see how a partial deployment is bounded against unchained CRO and EDC feeds.
- **Privacy Officer / Data Protection Officer** — pre-MAC redaction discipline and `disposition="redacted_at_sdk"` patterns.
- **Vendor management lead** — cross-vendor model-handover schema applied by analogy to a CRO data-delivery contract clause.
- **Internal audit team** — bifurcated readiness audit shows how to grade chain-instrumented and unchained columns against a published §10.19 coverage map.
- **Reference-verifier user / OSS adopter** — witness-mode procedure (skipping steps 7-9 that require IKM access) is the workable inspector-side path.
- **Cryptographic expert witness (Daubert)** — three-layer compositional security and HSM custody at FIPS 140-2 Level 3 grounding for clinical-trial litigation horizon.
- **Verifier implementer** — three-name CC8.1 citation discipline (implementation, version, verification key) grounds independent verification.

## Top spec sections used
- **§1.2** — epistemic scope (a/b/c/d/e); load-bearing for the April 15 patient framing — chain-integrity finding vs process-design finding distinguished.
- **§10.19** — chain-coverage map with five categories; the structural framing of the bifurcation, with `coverage_map_version`, `effective_utc`, `coverage_map_sha256`, and `chain.coverage_map_published` event per §10.2.
- **§7 + §10.12 + §10.26** — verifier procedure (12 ordered steps including witness mode), exit-code contract, and reference verifier distribution; the FDA inspector runs witness mode without the IKM and gets `PASS-STRUCTURALLY`.
- **§4.1 + §4.2 + §4.3 v1.0b** — three-layer cryptographic spine (HMAC chain at capture, daily Merkle seal under RFC 6962, HSM-rooted Ed25519 with `sign_payload_version="v1.0b"`); §1.4 compositional security made operational.
- **§10.21 + §10.20** — cross-vendor model-handover schema (`audit.model_handover.*` with model card / validation report / fairness-audit hash) and 540-day-equivalent training-data retention floor (deployment-window plus 90-day investigation buffer with GDPR Article 6(1)(f) legitimate-interests resolution).
- **§10.22** — pre-MAC redaction discipline at the SDK boundary; `audit.redaction.disposition = "redacted_at_sdk"` on every reviewer entry.
- **§10.13 + §1.1** — evidentiary-artifacts retention list and Daubert four-factor grounding; the seven-artifact evidence pack maps to FRE 901(b)(9) authentication.
- **§4.4.6 + §10.16** — SaaS-edge connector source attribution and four-number lag discipline; flagged as forward-readiness when the EDC extract migrates from daily file delivery to streaming change-stream mirror.

## All cited spec sections
- **§0.5** — reading-the-document framing; the recommended entry path for medical officers and CRO contract attorneys triaging the spec.
- **§1** — scope.
- **§1.1** — Daubert four-factor grounding (testability / peer review / known error rate / general acceptance).
- **§1.2** — epistemic scope; the load-bearing distinction.
- **§1.3** — security definitions (EUF-CMA / second-preimage / EUF-CMA composition).
- **§1.4** — three-layer compositional security.
- **§2.1** — referenced in the April 15 patient discussion.
- **§3** — definitions; `chain_kind` enumeration; tenant_id character class.
- **§4** — primitives framing.
- **§4.1 / §4.1.1 / §4.1.3** — HMAC chain at capture, Model B HSM-resident PRK handshake, per-event MAC algorithm agility (institution emits `payload_hash_alt` HMAC-SHA-3-256 as RECOMMENDED safety margin for 25-year retention horizon).
- **§4.2 / §4.2.1 / §4.2.2** — daily Merkle seal, daily cadence, day-boundary semantics by `received_at` with `late_binding=true` for late entries.
- **§4.3 / §4.3.1 / §4.3.2** — HSM-rooted Ed25519 signature with v1.0b 12-line `sign_payload`; HSM unavailability and 72-hour notification; algorithm rotation and quantum-readiness commitment.
- **§4.4 / §4.4.1 / §4.4.2 / §4.4.3 / §4.4.4 / §4.4.6** — chain envelope; routing event family; deployment-intent capture (`production` / `validation` / `regulatory_sandbox`); OTLP transport identification with five required Resource attributes; severity stamping in 9-20 range; SaaS-edge connector source attribution.
- **§5 / §5.2** — canonical-form exclusion; best-evidence content-vs-integrity split with FRE 1001(d).
- **§6** — append-only storage; chain-stamp preservation byte-for-byte.
- **§7** — 12-step verification procedure including step 12a gen_ai-completeness check; witness mode.
- **§8.4** — RFC 8032 §8.4 strict Ed25519 canonicalization.
- **§10.1** — key-fingerprint reconciliation (weekly cadence vs legacy 90-day access reviews).
- **§10.2** — operational events (full catalog including `master_key.rotated`, `master_key.rotation_observed`, `chain.partition_ceremony_attended`, `chain.coverage_map_published`).
- **§10.3** — append-only enforcement at application and database role layers.
- **§10.4** — NTP discipline.
- **§10.5** — FIPS 140-2 Level 3 HSM custody; CloudHSM Classic conformant, AWS KMS multi-tenant NOT.
- **§10.6 / §10.6.1** — IKM minimum 32 bytes; HSM internal RNG (highest-assurance pattern).
- **§10.7** — software-key adapter exclusion (compile-time + packaging double-protection).
- **§10.8** — constant-time comparison.
- **§10.10** — IKM rotation crossing seal boundary; `key_versions = [old, new]` in day-after seal.
- **§10.11 / §10.11.2** — adverse-action notice translation by analogy for clinical-trial decline notification.
- **§10.12** — verifier exit-code contract.
- **§10.13** — evidentiary-artifacts retention; FRE 901(b)(9) authentication-of-the-process foundation.
- **§10.14** — trusted-time integration (RFC 3161 not adopted; NTP per §10.4 is the foundation).
- **§10.15** — multi-region resilience (single-region today; planned for EU expansion).
- **§10.16** — SaaS-edge mirror connector lag bounds; severity-classification clause.
- **§10.17** — HSM partition ceremony attestation with `entity_affiliation` per M&A-P1.
- **§10.18** — CC8.1 and runbook cross-referencing.
- **§10.19** — chain-coverage boundary documentation (five categories); the structural spine.
- **§10.20** — training-data retention vs deployment-window discipline.
- **§10.21** — cross-vendor model-handover schema; cited by analogy for the CRO data-delivery contract clause.
- **§10.22** — pre-MAC redaction discipline.
- **§10.23** — consumer-correlation index integrity (Shape 1 chain-anchored for FDA subject-keyed retrieval).
- **§10.24** — entity succession (dormant; cited as forward-look for M&A scenarios).
- **§10.25** — run resume and chain-tail acquisition; genesis-block uniqueness anti-spoof.
- **§10.26** — reference verifier distribution discipline (three-name CC8.1 citation: implementation, version, verification key).
- **§11.10** — Part 11 §11.10 reference (electronic record requirements, including time-stamping).
- **§13** — stakeholder navigation; entry point for CRO contract attorneys.
- (Non-spec regulatory citations: 21 CFR Part 11, 21 CFR Part 820 QSR, ICH E6(R3), HIPAA Privacy Rule Safe Harbor, GDPR Article 6(1)(f), DSMB protocols, ALCOA+ nine attributes.)

## Synopsis

### Audit activity
The audit opened against a printed system map (green: nsclc-phase2 eligibility classifier; red: legacy regulatory and clinical-ops platforms, EDC, CRO data feeds, lab/LIMS, email/SharePoint). The eligibility classifier walked through a sealed entry from March 22, a full §7 12-step verifier procedure in 4 seconds, witness mode confirmation, and a 47-page IQ/OQ for the institutional CloudHSM with §10.17 partition ceremony chain-coupled. The IAM split contrasted chained AI service-account discipline against legacy 12-DBA UPDATE permission. A five-decision random reconciliation returned 5/5 inference PASS, 2/5 backward clean, 1/5 corrected-source discrepancy, 2/5 blocked by CRO retention; the discrepancy was an enrolled patient whose EHR staging was corrected to T3N2M1 two days after enrollment (M1 disease excludes from trial) — medical-monitor follow-up was initiated immediately. A cross-vendor contract-clause reframing converted internal friction over extending the chain into a CRO contract clause for the next renewal. A seven-artifact evidence pack was produced as the inspection-day playbook.

### How the spec was used

- **§1.2** — Epistemic-scope distinction was the engagement's load-bearing language; the chain-revealed clinical-quality finding sits at §1.2 (c) (chain accurately recorded what the model said about the input it was given; input authenticity is governed by upstream storage controls), distinguished as a process-design finding rather than a chain-integrity finding.
- **§10.19** — Chain-coverage map provided the five-category bifurcation framework with explicit boundary disclosures.
- **§7** — Witness mode (skipping steps 7-9 that require IKM access) makes the FDA inspector's verification path workable on a laptop they bring.
- **§10.26** — Reference verifier distribution discipline plus the three-name CC8.1 citation (implementation/version/verification key) ground inspector-side trust without requiring institution-side credentials.
- **§10.22** — Pre-MAC redaction posture (`disposition="redacted_at_sdk"`) makes the FDA read of the redaction policy mechanical rather than narrative.

### Results
**AI side:** 8 confirmations, 0 Gaps, 0 Partials — ALCOA+ defensible end-to-end on the surface area the chain covers; Part 11 audit-trail discipline operational. **Legacy side:** 4 Gaps + 6 Partials + 3 boundary-by-design items handled per §10.19. Gaps include legacy DBA UPDATE permission (§10.3 architectural target), LIMS same shape, Late-Effective-Date filter discoverability (§10.18), CTMS Visit Summary field history disabled (§10.22 / §4.4.6), legacy access review attests group membership not table-level modification, EDC extract has no chain (§4.4.6 forward-readiness), CTMS overwrite-able (§10.22 redaction). **Plus one chain-revealed clinical-quality finding:** classifier saw T3N2M0; EHR was corrected to T3N2M1 two days after enrollment; correction never back-fed to screening pipeline — process-design CAPA, not a chain-integrity finding.
