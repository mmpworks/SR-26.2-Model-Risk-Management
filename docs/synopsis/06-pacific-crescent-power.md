# Story 06 — Pacific Crescent Power & Gas (post-incident gas-pipeline AI utility audit)

**Story file:** `docs/auditor-stories/06-pacific-crescent-power.md`
**Engagement type:** NERC CIP audit-readiness assessment with PHMSA pipeline-integrity overlay; AI-only chain on a gas-pipeline leak-detection service after a near-miss methane event.
**Posture going in:** Partial deployment — chain instrumented on `pipeline-leak-detection` only; PI historian, GE iFIX SCADA, Itron OpenWay AMI, OMS, CIS, and Salesforce all legacy.
**Outcome posture:** Confirmation on the AI side; gap-finding on OT and customer-billing tiers. The §1.2 epistemic-scope distinction (chain proves what the AI said, not what the sensor measured) is the report's load-bearing sentence.

## Type of audit
Post-incident utility audit composing NERC CIP-002 through CIP-014, FERC Order 887, PHMSA pipeline-integrity expectations, and three states' PUC interest (WUTC, OPUC, CA-CPUC). Distinct because the worst-case consequence is public safety — a wrong reading and a dismissed alarm could blow up a neighborhood — which makes the §1.2 epistemic-scope question (what the chain proves vs. what it does not) the central forensic line for the executive office, the PUC, and the insurance carrier.

## Interested parties (spec readers)
- Chief Information Security Officer (CISO) — institutional cyber posture; HSM custody, IR posture, supply-chain trust path under public-safety stakes.
- Chief Compliance Officer / CRO — multi-framework regulatory posture across NERC CIP, PHMSA, and three PUCs.
- Model Risk Management chair — gas-pipeline leak-detection model lifecycle under SR 11-7-equivalent discipline.
- Chief AI / ML Officer — AI-system owner; deployment-intent author for the leak-detection service.
- General Counsel — Daubert-grounded litigation-support posture for the dismissed-alarm public-safety question.
- DevSecOps / SRE on-call — runtime, incident response, multi-region resilience; live alert verified during the engagement.
- Vendor management lead — Schneider Electric model-handover under cross-vendor schema.
- Cryptographic expert witness (Daubert) — one-page four-factor answer for any litigation that follows.
- FFIEC Cybersecurity Specialist Examiner — informative; NIST CSF 2.0 alignment readers transfer the threat-model patterns.
- State utility-regulator equivalents (WECC, PHMSA, WUTC / OPUC / CA-CPUC) — informative for spec readers; non-FFIEC analogs for the chain-coverage map under §10.19.
- Insurance carrier — needs the cryptographic dismissed-alarm evidence package.

## Top spec sections used
- **§1.2** — "Chain proves what the AI said and that the record was not tampered with; the chain does not prove the input the AI saw was true." The whole report turns on the (a)/(b) vs (c) distinction.
- **§1.4** — Three-layer compositional security (per-event HMAC + daily Merkle seal + HSM signature) is what makes the AI-side defense survive the CIP-categorized network split.
- **§4.4.6** — `audit.connector_source.*` family by analogy for the PI-to-AI ingestion adapter — the Phase 2 work item.
- **§7 / §10.12** — 12-step verifier procedure with exit-code 0 returned in four seconds during the live alert; that capture became the principal artifact for executive briefing.
- **§10.13** — Evidentiary-artifacts retention floor exposes that the PI historian's 60-day rolling audit trail is below the chain-data floor and below the NERC CIP-008-6 / CIP-009-6 3-year minimum.
- **§10.19** — Chain-coverage map enumerating chain-instrumented / not-yet-instrumented / third-party-with-inspection / external-evidentiary categories — the single artifact every regulator reads as the same picture.
- **§10.21 + §10.20** — Schneider Electric model handover with M&A-G2 contract triple and 1825-day training-data retention floor.
- **§10.24 + §10.15 + §10.25** — Forward-readiness conversation for a possible Northwest peer merger and an active-active flip to the Bonneville Power cold site.

## All cited spec sections
- **§0.5.2** — Mermaid diagram mapping SDK capture through verifier in one frame; useful 30-second context for OT engineers.
- **§1.1** — Daubert four-factor grounding (testability, peer review, known error rate, general acceptance).
- **§1.2** — Epistemic scope; the controlled-vocabulary frame for the public-safety question.
- **§1.3** — Security definitions (HMAC EUF-CMA, Merkle second-preimage, Ed25519 EUF-CMA, 128-bit composite).
- **§1.4** — Compositional security across three independent authentication layers.
- **§2.1** — Out-of-scope framing.
- **§3** — `tenant_id` character class; chain_kind enumeration.
- **§4.1** — Per-event HMAC chain at capture, HKDF tenant binding, mid-write truncation refusal.
- **§4.1.2** — `posture=ffiec` flag; `hkdf_inputs_digest` cross-check.
- **§4.2** — Daily Merkle seal; RFC 6962 leaf/node prefixes.
- **§4.2.2** — Day-boundary semantics by ledger `received_at` UTC; `late_binding=true` for follow-up entries.
- **§4.3** — HSM-rooted root signature; `sign_payload` 6-line / v1.0a / v1.0b dispatch.
- **§4.4** — OTLP-native wire; `gen_ai.*` MUST; parent-linkage discipline.
- **§4.4.1** — Routing schema (single-provider for leak detection, schema silent by spec).
- **§4.4.2** — Deployment-intent capture (`production` posture).
- **§4.4.3** — OTLP transport identification (5 required Resource attributes).
- **§4.4.4** — Severity for chain-of-custody traffic (no severity-filter; receiver stamps 9..20).
- **§4.4.6** — SaaS-edge connector source attribution applied by analogy to the PI ingestion adapter.
- **§5** — Wire format; RFC 8785 JCS canonical bytes; canonical-form exclusion of chain-stamp fields.
- **§5.1** — TLS 1.3 transport encryption between SDK and ledger.
- **§5.2** — Best-evidence posture under FRE 1001-1004.
- **§6** — Storage discipline; chain-stamp byte-for-byte preservation.
- **§7** — 12-step verification procedure; PASS / FAIL / REJECTED outputs; JCS pre-flight self-test.
- **§10.1** — Daily key-fingerprint reconciliation (more aggressive than the RECOMMENDED weekly).
- **§10.2** — Operational events (`master_key.generated`, `chain.coverage_map_published`, etc.).
- **§10.3** — Append-only enforcement at application + database-role layers; iFIX violates both.
- **§10.4** — NTP discipline exceeded by PMU-grade GPS-disciplined master clock.
- **§10.5** — FIPS 140-2 Level 3 HSM custody (Thales Luna PCIe on CIP-categorized network).
- **§10.6 / §10.6.1** — IKM 32-byte minimum; HSM-internal CSPRNG (highest-assurance pattern).
- **§10.7** — Software-key adapter compile-time exclusion in production.
- **§10.8** — Constant-time comparison for fingerprint and MAC checks.
- **§10.9** — IKM-registry retention coupled to chain-entry retention (longer of 7 years or chain-data retention).
- **§10.10** — IKM rotation crossing the seal boundary; `key_versions=[old,new]` on day-after seals.
- **§10.11** — ECOA translation parent-linkage discipline used as the model for the dispatcher follow-up entry.
- **§10.12** — Verifier CLI exit-code contract (0 PASS, 1 FAIL, 2 could-not-begin, 3 config error).
- **§10.13** — Evidentiary-artifacts retention list backing FRE 901(b)(9) authentication.
- **§10.14** — Trusted-time integration (RECOMMENDED; PMU-grade time exceeds the SHOULD bar).
- **§10.15** — Multi-region resilience (Pattern A / B forward-readiness for active-active to BPA).
- **§10.16** — SaaS-edge connector four-number lag bounds; severity-classification clause for imprecise wording.
- **§10.17** — HSM partition-ceremony attestation (`chain.partition_ceremony_attended` with `entity_affiliation`, RECOMMENDED `hsm_attestation_token_b64` emitted).
- **§10.18** — CC8.1 cross-referencing; one Nit on the dispatcher-application runbook.
- **§10.19** — Chain-coverage map enumerating four boundary categories; `audit.external_artifact.*` for OMS work-order content-coupling.
- **§10.20** — Training-data retention floor (1825 days for the leak-detection model).
- **§10.21** — Schneider Electric cross-vendor model-handover schema with M&A-G2 contract triple and M&A-P2 training-shard manifest hash.
- **§10.22** — Redaction discipline (no redaction at SDK; absence is conformant; CEII redaction is downstream of chain).
- **§10.23** — Consumer-correlation index (Phase 4 Shape 2 if PUC consumer-keyed retrieval becomes recurrent).
- **§10.24** — Entity-succession framework for a potential Northwest peer merger.
- **§10.25** — Run resume and chain-tail acquisition; DR rejoin to the BPA cold site.
- **§10.26** — Reference-verifier distribution; three-name CC8.1 citation.
- **§10.57** — Firmware-attestation chain across supplier tiers (forward-commitment once OpenWay 5.4 ships an integrity-checking firmware artifact).
- **§11** — References; pinned verifier version.
- **§13** — Stakeholder navigation order for the report (executive → SOC → litigation).

## Synopsis

### Audit activity
The team conducted a clean-room split across the AI ledger and the PI historian, three-tier IAM (AI / OT / customer-billing), API and `gen_ai.*` discipline, and the sensor-to-AI path. A live medium-confidence alert on a real pipeline segment was verified in four seconds while the dispatch crew was still en route; a small leak was confirmed twenty-two minutes later. The afternoon ran a four-prediction reconciliation test (clean for recent windows, eroded past 60 days due to PI retention and paper-OMS transcription) and closed with the public-safety question framed under §1.2.

### How the spec was used

- **§1.2** — Epistemic-scope controlled vocabulary that let every reader land on the same understanding of what the chain proves (the AI said X at time T; the record was not tampered) and what it does not (whether the upstream sensor was honest).
- **§10.19** — Chain-coverage map turned three implicit-tier mutability shapes into one testable artifact every regulator could read identically.
- **§7 / §10.12** — 12-step verifier with exit-code 0 returned in four seconds across nine months and 1.6 million inferences — including live during the alert.
- **§1.4** — Compositional security across three independent layers that make the chain hold even when an attacker compromises one layer.
- **§1.1** — Daubert four-factor grounding gave the litigation-support file a one-page answer to each factor.
- **§10.13** — Named the documentary artifacts (SDK manifest, source hash, HSM config, seal-job logs, change-management, verifier output) that compose with the chain output for FRE 901(b)(9) authentication.

### Results
Three-tier summary: AI side — 0 Gaps, 0 Partials, 1 Nit (§10.18 dispatcher-runbook cross-reference, five-line fix); OT side — 5 Gaps, 6 Partials (PI 60-day retention, GE iFIX UPDATE audit, Itron 5.2 lock, shared HMI account, dispatcher_id binding, OMS work-order content-coupling, sensor-to-AI authentication, AMI override, IEC 62443-3-3 SR 7.5, historian disk sizing); customer-billing side — 3 Gaps, 4 Partials. Phase 2 (12 months) closes the AMI 5.4 upgrade, PI integrity extension, MFA, federated SSO, and `audit.connector_source.*` emission. Phase 3 (18 months) closes OMS content-coupling via `audit.external_artifact.*`. The live-alert capture became the executive-briefing artifact.
