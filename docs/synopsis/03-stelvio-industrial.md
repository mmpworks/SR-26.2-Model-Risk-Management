# Story 03 — Stelvio Industrial (CMMC 2.0 Level 2 readiness re-assessment with AS 9100D overlay)

**Story file:** `docs/auditor-stories/03-stelvio-industrial.md`
**Engagement type:** CMMC 2.0 Level 2 readiness re-assessment with AS 9100D quality-systems overlay at a third-generation family-owned $2.1B specialty steel mill (DoD prime supplier, ITAR §125 export-control records, downstream medical-device customer's FDA design-verification pipeline).
**Posture going in:** Partial deployment, 14 months live on three AI services only; institution-side ask is to confirm chained services pass while documenting remediation timelines for OT and IT business systems.
**Outcome posture:** Gap-finding — chained AI side passes (7 confirmations); unchained OT side carries 4 Gaps + 5 Partials; unchained IT business side carries 3 Gaps + 4 Partials.

## Type of audit
A CMMC 2.0 Level 2 readiness re-assessment with an AS 9100D quality-systems overlay; the steel mill rolls medical-device-grade and aerospace-grade flat steel and handles CUI daily. What makes it distinctive is the partial-deployment posture explicitly framed against a published §10.19 chain-coverage map: three discrete zones (chained AI services, unchained OT, unchained IT business) and the audit's organizing job is to confirm the chain-instrumented column passes while documenting Phase 2 / Phase 3 / Phase 4 remediation timelines for the rest.

## Interested parties (spec readers)
- **CMMC C3PAO assessor** — CMMC 2.0 Level 2 / NIST SP 800-171 control evaluation in a partial-deployment posture explicitly framed against a published chain-coverage map.
- **DCMA contracting officer** — defense supply-chain compliance read at a DoD prime supplier handling CUI daily.
- **DCAA defense audit** — defense cost / property accounting against a third-generation family-owned mill.
- **Vendor management lead** — partial-deployment vendor-conformance attestation across three discrete zones (chained AI, unchained OT, unchained IT business).
- **Internal audit team** — illustrates how to publish and operate a §10.19 chain-coverage map quarterly with `chain.coverage_map_published` events anchoring lookback alignment.
- **DevSecOps / SRE on-call** — operator-side read of weekly fingerprint reconciliation, Kubernetes node-drain run-resume, and four-second verifier-on-catwalk demonstration.
- **FDA Bioresearch Monitoring (BIMO) inspector** — downstream of the medical-device customer's FDA design-verification submission; the cover letter uses §1.2 verbatim language.
- **Chief Audit Executive (CAE)** — institution-side counterpart for a multi-zone remediation roadmap with executive funding decisions.
- **Reference-verifier user / OSS adopter** — the customer-question session walks a downstream party through five-step verification using the published reference verifier, witness mode, and §1.2 / §4.4.

## Top spec sections used
- **§10.19** — chain-coverage map; the engagement's organizing document. The published map names every system, rollout posture, and evidentiary substitute on one page.
- **§1.2** — epistemic scope; load-bearing for the historian-tamper-before-read scenario (§1.2 (c)) and for the downstream-customer cover letter language (§1.2 (a) and (b)).
- **§4.4.6 + §10.16** — SaaS-edge connector source attribution and quantified-lag discipline; cited as the Phase 2 historian-boundary pattern (by analogy) and as a forward-looking constraint with the forbidden-phrase severity-classification clause on watch from day one of Phase 2.
- **§4.3 v1.0b sign_payload** — 12-line form binding `key_versions_canon` and `hex(kms_handle_uris_digest)` under the Ed25519 signature; closes silent-rewrite paths the older 6-line and 10-line forms left open.
- **§7** — 12-step verification procedure with the pre-flight JCS self-test; produces the four-second catwalk PASS captured on video.
- **§10.20 + §10.21** — training-data retention floor (540 days) and cross-vendor model-handover schema; operational at the Q4 2025 predictive-maintenance regression worked example.
- **§10.26** — reference verifier distribution discipline; what makes the downstream customer's independent verification possible without trusting institution-side tooling.
- **§1.4 / §10.5 / §10.3** — three-layer compositional security operationalized at the institutional HSM under FIPS 140-2 Level 3, append-only at storage tier and database role layers, and a tamper test against the chain backing store.

## All cited spec sections
- **§1.1** — Daubert four-factor grounding.
- **§1.2** — epistemic scope (a/b/c) — the most-cited section.
- **§1.3** — security definitions and 128-bit security level.
- **§1.4** — three-layer compositional security.
- **§2.7 / §2.10** — threat-model document references for Adversary F (SDK-process compromise) and regulator-fingerprint reception.
- **§3 / §3.1** — definitions including `chain_kind` enumeration and tenant_id character class; legacy migration patterns (dormant in this engagement).
- **§4** — primitives framing.
- **§4.1 / §4.1.1 / §4.1.2 / §4.1.3** — HMAC chain at capture, Model B handshake, FFIEC posture and `hkdf_inputs_digest`, per-event MAC algorithm agility.
- **§4.2 / §4.2.1 / §4.2.2** — daily Merkle seal, daily cadence, day-boundary semantics by `received_at`.
- **§4.3 / §4.3.1 / §4.3.2** — HSM-rooted signature, HSM unavailability and 72-hour notification, algorithm rotation and Variant B AND-security.
- **§4.4 / §4.4.1 / §4.4.2 / §4.4.3 / §4.4.4 / §4.4.5 / §4.4.6** — chain envelope, routing classifier output (ITAR screening NLP), deployment-intent capture, OTLP transport identification, severity stamping, underwriting-features by analogy, SaaS-edge connector source attribution.
- **§5 / §5.1 / §5.2** — canonical-form exclusion, transport encryption (TLS 1.3 minimum, discovery endpoints inherit), best-evidence content-vs-integrity split.
- **§6** — append-only storage discipline; chain-stamp preservation.
- **§7** — 12-step verification procedure.
- **§8.4** — RFC 8032 §8.4 strict Ed25519 canonicalization (Luna refuses non-canonical forms).
- **§10** — operational requirements framing.
- **§10.1** — weekly fingerprint reconciliation.
- **§10.2** — operational events.
- **§10.3** — append-only enforcement at application and database role layers.
- **§10.4** — NTP discipline.
- **§10.5** — HSM custody at FIPS 140-2 Level 3+.
- **§10.6 / §10.6.1** — IKM minimum length and CSPRNG requirements.
- **§10.7** — software-key adapter exclusion in production (compile-time, strictest pattern).
- **§10.8** — constant-time comparison.
- **§10.9** — IKM registry retention.
- **§10.10 / §10.10.2** — IKM rotation crossing seal boundary; within-day algorithm rotation patterns.
- **§10.11** — adverse-action notice translation (dormant for manufacturing).
- **§10.12** — verifier exit-code contract.
- **§10.13** — evidentiary-artifacts retention list.
- **§10.14** — trusted-time integration (RFC 3161 not adopted).
- **§10.15** — multi-region resilience (single-region; dormant).
- **§10.16** — SaaS-edge mirror connector lag bounds; forbidden-phrase severity-classification on watch from Phase 2 day one.
- **§10.17** — HSM partition ceremony attestation.
- **§10.18** — CC8.1 and runbook cross-referencing.
- **§10.19** — chain-coverage boundary documentation; the spine of the engagement.
- **§10.20** — training-data retention vs deployment-window discipline (540-day floor operational).
- **§10.21** — cross-vendor model-handover schema (internal handover at predictive-maintenance).
- **§10.22** — pre-MAC redaction discipline.
- **§10.23** — consumer-correlation index integrity (dormant for B2B).
- **§10.24** — entity succession (dormant for family ownership).
- **§10.25** — run resume and chain-tail acquisition; closed silent-restart on the Q1 Kubernetes node drain.
- **§10.26** — reference verifier distribution discipline.
- **§10.59** — RMA / sustainment chain re-entry; cited as forward-look for Phase 2 sustainment scope.
- **§10.61** — CMMC 2.0 / NIST 800-171 / NIST 800-161 regulator-pack overlay framework.
- **§11** — references; spec pins reference verifier version.
- **§13** — stakeholder navigation entry points.
- (Non-spec regulatory citations: ITAR §125, DFARS 252.204-7012, IATF 16949, EU AI Act Article 11/12, GDPR Article 6(1)(f), CMS-0057-F.)

## Synopsis

### Audit activity
The audit ran against a printed §10.19 chain-coverage map. The reference verifier ran in four seconds on a catwalk over a 4G hotspot (captured on video for the CFO brief). A direct database UPDATE on the chain backing store was caught by the verifier at §7 step 9 (single-entry tamper) and step 10 (multi-entry Merkle); the OT historian was probed and found to have `db_owner` mutability with no row-level audit. Three IAM columns were mapped side by side: chained AI service-account discipline versus a shared `Plant_Engineer` workstation 18 months stuck on a single PLC versus SAP `SAP_ALL` with broken closure discipline. A reconciliation test traced three random QC classifications end-to-end (all PASS forward and backward); one trace landed at the medical-device customer's April 7 FDA submission. A customer-question session walked through five-step verification using §10.26 + §5.1 + §7 witness mode + §1.2 + §4.4.

### How the spec was used

- **§10.19** — Engagement's organizing document; the chain-coverage map had been published quarterly for 14 months with `chain.coverage_map_published` events anchoring lookback alignment, and the audit confirmed each cell rather than discovering boundaries per-finding.
- **§1.2** — Epistemic scope was the language threaded through every surprise (historian-tamper-before-read sits at §1.2 (c); Phase 2 hashing under §4.4.6 by analogy moves it into (a)+(b)).
- **§4.3** — v1.0b 12-line `sign_payload` form confirmed as load-bearing protection against silent `key_versions` and `kms_handle_uri` rewrites.
- **§1.2 (downstream cover letter)** — Cover letter uses §1.2 verbatim so the FDA reviewer reads the spec's language directly.
- **§10.16** — Severity-classification clause on watch from day one of Phase 2 — imprecise lag wording is non-conformance, never a Nit.

### Results
Three-zone outcome with a single severity scale and three remediation timelines. **AI side:** 7 confirmations, 0 Gaps, 0 Partials — passes CMMC 2.0 Level 2 / AS 9100D / ITAR §125 / DFARS 252.204-7012 for in-scope subset. **OT side:** 4 Gaps + 5 Partials (historian mutability, shared `Plant_Engineer` no-MFA workstation, editable TIA Portal log, Plex audit log cleared 6 months ago, HMI uninstrumented), Phase 2 in 12 months. **IT business side:** 3 Gaps + 4 Partials (`SAP_ALL` closure discipline, Dynamics field-history selectively enabled, SharePoint QMS no integrity check), Phase 3 in 18 months and Phase 4 distant. Phase 2 funding was approved on the basis of the engagement and the verifier-on-catwalk video.
