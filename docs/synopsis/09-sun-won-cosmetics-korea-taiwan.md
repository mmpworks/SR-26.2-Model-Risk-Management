# Story 09 — Sun-Won Cosmetics Group (Korea + Taiwan K-beauty multi-jurisdiction audit)

**Story file:** `docs/auditor-stories/09-sun-won-cosmetics-korea-taiwan.md`
**Engagement type:** Coordinated annual review across PIPA Section 28 cross-border transfer (Korean PIPC), PDPA Article 8 explicit-consent (Taiwan PDPC), FSS BNPL credit-scoring supervision, Taiwan FSC listed-subsidiary disclosure, and a CPRA / GDPR sweep against the e-commerce platform — three regulators, two HSMs, one chain across the Korea Strait.
**Posture going in:** TesseraSeal in production for sixteen months across four use cases (customer recommendation, inventory forecasting, multilingual chatbot, BNPL credit-scoring); 8 tenants plus a 9th cross-jurisdiction tenant for inventory; Korean HSM (Sangam-dong, KISA-certified) and Taipei HSM (Chunghwa Telecom, CNS 27001 aligned).
**Outcome posture:** Confirmation on the chain primitive; two Findings against PRD-1 spec text the engagement drove (cross-border attribute family in §4.4.1 + chained classifier_output sixth event type in §4.4.1) — the spec moved to meet the posture.

## Type of audit
Multi-jurisdiction K-beauty audit with three regulators reading the same chain through three different lenses (PIPA, PDPA, FSS, FSC). Distinct because the chain was deployed nine months early after a celebrity-endorsement controversy alleged the AI personalization had used a celebrity's biometric features without explicit consent — the chain is the cryptographic-evidence backbone for which features the recommendation models used and which were structurally excluded at ingest. The team is split: half in Seoul (Sangam-dong HQ) and half in Taipei (Xinyi District subsidiary).

## Interested parties (spec readers)
- PIPA + PDPA + FSS + Taiwan FSC — Korea / Taiwan multi-jurisdiction supervision (privacy, financial supervisor, exchange listing).
- Privacy Officer / DPO — PIPA / PDPA / GDPR alignment; tokenization architecture; cross-border-flow attestations.
- Chief AI / ML Officer — AI-system owner; deployment-intent author; routing schema and classifier_output discipline.
- Chief Compliance Officer / CRO — multi-framework regulatory posture across four supervisors.
- General Counsel — listed-subsidiary disclosure framing; celebrity-controversy lookback litigation framing.
- M&A integration lead (acquirer) / M&A integration lead (acquired entity) — parent / Taipei-listed subsidiary boundary discipline.
- Vendor management lead — Seoul AI consultancy chatbot model under §10.21 cross-vendor handover.
- AI vendor product-engineering team — chatbot model handover and cross-anchor design (counterparty side).
- Standards-body reviewer — informative; this engagement drove two normative additions to §4.4.1.
- SOC 1 / SOC 2 engagement team — Section 4 description and control-evidence schema for the partitioned letters.
- Big-Four assurance audit — cross-framework attestation across PIPA, PDPA, FSS, FSC.
- FFIEC IT Examiner — informative; analog patterns for cross-border AI under coordinated supervision.

## Top spec sections used
- **§1.4** — Three-layer compositional security holds across the strait; per-event MAC + daily Merkle seal + HSM signature each FIPS-current and jurisdiction-blind.
- **§4.1.2** — `posture=ffiec` HKDF constants byte-identical across tenants; jurisdictional binding is the per-tenant `info` parameter, not the constants.
- **§4.4.1** — The spec section this engagement drove twice: cross-border-transfer attribute family lifted to spec body (Finding-001) AND sixth event type `audit.routing.classifier_output` added with six new attributes (Finding-002).
- **§7 + §10.12** — 12-step verifier with strict-mode PASS over 365 days, 18,442 entries on BNPL; JCS self-test (NIST-P2) pre-flight.
- **§10.11.1** — ECOA-analog adverse-action reasons schema applied to FSS-jurisdiction BNPL declination via §10.11's analogy clause.
- **§10.15 Pattern B** — Per-jurisdiction `tenant_id` for KR + TW tenants (no co-mingling of key material between parent and subsidiary; FSC and PIPC both want this explicitly).
- **§10.15 Pattern A** — Single seal region (Seoul) for the cross-jurisdiction `sunwon-cross-inventory` tenant with `master.cross_region_replication_completed` synchronous-read freshness.
- **§10.17** — HSM partition-ceremony attestation across both Seoul and Taipei HSMs with `entity_affiliation` per M&A-P1 and cross-language CC8.1 discoverability for Korean and Mandarin runbooks.
- **§10.21** — Cross-vendor model-handover with M&A-G2 contract binding for the Korean chatbot model from the Seoul consultancy; M&A-G3 `contract_status` discriminator; M&A-N2 plural `audit_report_languages` array.

## All cited spec sections
- **§0.5.3** — Per-role reading-paths-by-role table; the natural triage tool when four regulators review the same chain artifacts.
- **§1.1** — Daubert four-factor grounding for the celebrity-controversy lookback litigation framing.
- **§1.2** — Epistemic scope; the chain proves what the AI said and that the record was not tampered with; training-data lineage and pre-chain era are out of scope by spec.
- **§1.3** — Security definitions; EUF-CMA / second-preimage / EUF-CMA composition.
- **§1.4** — Three-layer compositional security at 128-bit composite under NIST SP 800-175B.
- **§3** — `tenant_id` character class `^[A-Za-z0-9_.\-]{1,255}$`; `chain_kind` enumeration.
- **§3.1** — Legacy tenant-identifier handling; three legacy CRM identifiers under Pattern 1 / Pattern 2.
- **§4.1** — Per-tenant HKDF binding; same `tenant_id` across two banks correctly produces different session keys when IKMs differ.
- **§4.1.2** — FFIEC-conformance posture `ffiec.chain.posture = ffiec`.
- **§4.2** — Daily Merkle seal; empty-day seal continuity (Lunar New Year).
- **§4.2.1** — Cadence (daily).
- **§4.3** — `sign_payload_version = "v1.0b"` 12-line form across both HSMs.
- **§4.4** — Chain envelope, `gen_ai.{request,response}.model` MUST, parent_run_id / parent_seq.
- **§4.4.1** — Routing schema; cross-border-transfer attribute family (Finding-001 driver); classifier_output sixth event type (Finding-002 driver); required-pairing rule.
- **§4.4.2** — Deployment-intent capture (`production` for all sampled tenants).
- **§4.4.3** — OTLP transport identification (Resource attributes + recommended HTTP / gRPC headers).
- **§4.4.4** — Severity for chain-of-custody traffic (collector pass-through; receiver stamping `9..20`).
- **§4.4.5** — Underwriting features family (NAIC-P1) on BNPL credit-scoring entries.
- **§4.4.6** — SaaS-edge connector source attribution (`audit.connector_source.*`); stable-`run_id` discipline; Salesforce CDC mirror for Taiwan CRM.
- **§5** — Wire format; canonical-form exclusion rule.
- **§5.2** — Best-evidence posture under FRE 1001-1004.
- **§6** — Storage; chain-stamp byte-for-byte preservation.
- **§7** — 12-step verifier procedure; JCS self-test pre-flight; normative reason strings.
- **§10.1** — Daily key-fingerprint reconciliation against the IKM registry.
- **§10.2** — Operational events (`master_key.generated`, `chain.coverage_map_published`, `connector.lag_observation`, `connector.outage`, `chain.partition_ceremony_attended`).
- **§10.3** — Append-only enforcement at application + database-role + WORM-storage layers.
- **§10.4** — NTP discipline.
- **§10.5** — HSM custody (Seoul Sangam-dong KISA-certified; Taipei Chunghwa Telecom CNS 27001).
- **§10.6 / §10.6.1** — IKM 32-byte minimum; RNG cryptographic-strength generation; FIPS 140-3 attestation available on request.
- **§10.9** — IKM registry retention indefinite; historical entries remain verifiable.
- **§10.11** — ECOA / state-insurance analog adverse-action notice translation; CFPB-N1 `delivery_timestamp` requirement when `delivery_method` is recorded.
- **§10.11.1** — Adverse-action reasons schema applied to FSS BNPL declinations.
- **§10.13** — Evidentiary artifacts retention.
- **§10.14** — Trusted-time integration (RFC 3161 informative; not yet adopted).
- **§10.15** — Multi-region resilience — Pattern A (cross-inventory) + Pattern B (per-region tenants).
- **§10.16** — SaaS-edge capture connectors (Salesforce CDC mirror for TW CRM); four numbers named (median 18s SLO, p95 90s SLO, alert 150s, RTO 5min); steady-state actuals well under SLOs; zero alert-threshold breaches in 12 months.
- **§10.17** — HSM partition-ceremony attestation; `entity_affiliation` per M&A-P1; cross-language CC8.1 discoverability for Korean / Mandarin runbooks.
- **§10.18** — CC8.1 and runbook cross-referencing.
- **§10.19** — Chain-coverage boundary documentation; `audit.external_artifact.*` family for the BNPL training manifest hash anchor; pre-chain era as institution-side legacy-log dependency.
- **§10.20** — Training-data retention vs deployment-window discipline (24 months above the 60-90-day floor).
- **§10.21** — Cross-vendor model-handover schema for Korean chatbot model from Seoul consultancy; M&A-G2 contract binding; M&A-G3 `contract_status` discriminator; M&A-N2 plural `audit_report_languages`.
- **§10.22** — Redaction discipline (pre-MAC at SDK boundary); PIPA-compliant; PDPA-compliant.
- **§10.24** — Entity succession (no current activity; CC8.1 names the procedure for any future event).
- **§10.25** — Run resume and chain-tail acquisition; SQLite sidecar plus ledger rejoin.
- **§10.26** — Reference verifier distribution; three-name CC8.1 citation.
- **§11** — References; pinned `prd-1-verifier`.
- **§12** — Change log; §4.4 cross-border-transfer family and §4.4.1 sixth-event-type lifted to spec body — this engagement surfaced both gaps.
- **§13** — Stakeholder navigation; acquirer-side IT due-diligence entry.
- **§28** — PIPA Section 28 cross-border transfer (Korean privacy regime, named outside the spec).

## Synopsis

### Audit activity
Two halves on a video bridge: Seoul + Taipei. The BNPL credit-scoring chain pulled an April 4 conditional decline; verifier strict-mode ran clean over 365 days and 18,442 entries; a 689-score override-to-approved by reviewer kr-rv-014 answered the FSS 2024-Q2 letter on reviewer-override capture. PASS-IT mobile-PKI integration showed one break-glass event in the last quarter (read-only, 42 minutes, justified, post-event-reviewed). The recommendation-engine chain for the Taiwan tenant ran on a distinct HSM, distinct IKM, and distinct seal cadence — §10.15 Pattern B preserves per-region cryptographic isolation. The §10.16 Salesforce CDC mirror walkthrough named the four numbers. The bridge surfaced an inventory-tenant cross-border attribute gap that the spec amendment closed in the change log. The afternoon pulled the chatbot's language-detection routing rationale (3-of-5 recoverable from the 90-day detector logs, 2-of-5 gone) and ran the §10.15 Pattern A reconciliation on `sunwon-cross-inventory` (per-region count 1832 KR + 362 TW = 2194 seal-region count match).

### How the spec was used

- **§4.4.1** — Carried two findings the engagement drove into spec body: the `audit.cross_border_transfer.*` attribute family (six attributes — `contract_id`, `contract_version`, `contract_hash_sha256`, `source_jurisdiction`, `destination_jurisdiction`, `lawful_basis_type`) on cross-jurisdiction chain entries; and the sixth event type `audit.routing.classifier_output` (six new attributes — `classifier_name`, `classifier_version`, `classifier_input_hash`, `classifier_scores`, `classifier_decision`, `classifier_confidence`) emitted BEFORE the `audit.routing.attempt` it informs, parent-linked via `parent_run_id` / `parent_seq`.
- **§10.15 Pattern B** — Preserved per-region cryptographic isolation for the KR + TW recommendation tenants.
- **§10.15 Pattern A** — Held for the cross-jurisdiction inventory tenant with synchronous-read freshness on `master.cross_region_replication_completed`.
- **§10.21** — M&A-G2 contract binding integrity-bound the Korean chatbot model handover from the Seoul consultancy.
- **§10.22** — Pre-MAC SDK redaction made the post-controversy redesign — moving feature exclusion to ingest, not at model layer — structurally provable rather than policy-provable: facial-features-from-photo and voice-features cannot enter the feature pipeline because the redaction happens before MAC computation.
- **§1.2 / §10.19 / §12** — Framed the pre-chain era retention gap honestly as institution-side legacy-log dependency.

### Results
Ten Confirmations + the pre-chain era confirmation-by-spec, two Findings against PRD-1 spec the engagement drove (Finding-001 cross-border attribute on `sunwon-cross-inventory` non-conformance; Finding-002 chained classifier_output non-conformance), one tracking Finding (Finding-003 chatbot reconciliation 3-of-5 routing rationale recoverable; closure path is Finding-002 remediation). Bundle remediation: six weeks legal + two weeks chain config; Q3 2026 target. Per-regulator partition: PIPA, PDPA, FSS, FSC each get their own letter from one chain — same answers framed for each lens. The cross-border boundary held procedurally and will hold cryptographically after Q3 once the §4.4 + §4.4.1 remediation lands. The remediation is to a normative posture the institution helped shape — the cleanest cross-border story to date because the spec moved to meet the posture.
