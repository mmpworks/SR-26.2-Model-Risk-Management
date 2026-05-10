# Story 11 — Eberhardt Werkstoffe x Lumiere AI (German automotive supplier + French AI consultancy joint engagement)

**Story file:** `docs/auditor-stories/11-eberhardt-lumiere-germany-france.md`
**Engagement type:** Joint cross-vendor pre-audit ahead of EU AI Act enforcement and an OEM joint-supplier audit
**Posture going in:** Each side independently chained; the cross-vendor seam between the two chains had not been exercised under audit
**Outcome posture:** Confirmation engagement; drove §10.20 (training-data retention floor) and §10.21 (cross-vendor model-handover schema, plural-array `audit_report_languages`) into the spec body

## Type of audit
Two-country, two-company joint engagement split between Stuttgart (Mittelstand automotive-electronics supplier, 8 months chained on the OEM-facing inference path) and Paris (~80-person AI consultancy, 4 months chained on the model-development pipeline). The chain crosses the partnership boundary via the §10.21 `audit.model_handover.*` family. Five readers consume the deliverable: the EU AI Act conformity-assessment file, BSI, TISAX, LfDI Baden-Wuerttemberg + CNIL (joint GDPR), and OEM vendor-management. The engagement is the spec's named worked example for the within-EU cross-border-composition note and the plural-array `audit_report_languages` discipline.

## Interested parties (spec readers)
- **EU AI Act regulator / GDPR DPA** — EU AI Act conformity assessment, GDPR Articles 25 / 32 demonstrability; primary reader
- **BaFin / CNIL** — Germany financial supervisor + France privacy supervisor; cross-vendor partnership oversight
- **Privacy Officer / DPO** — Redaction discipline (§10.22), consent capture (§10.38), within-EU transfer posture
- **AI vendor product-engineering team** — Builds AI features that must be chain-instrumented; partner side of the §10.21 cross-anchor
- **Model provider / AI vendor (cross-vendor anchor)** — Cross-vendor cross-anchor counterparty for the model handover and parallel-evaluator chains
- **Vendor management lead** — Vendor-conformance attestation across the partnership boundary
- **IT due-diligence lead (M&A)** — Reads the §10.21 family for diligence on cross-vendor AI partnerships
- **Big-Four assurance audit** — Cross-framework attestation across SOC, ISAE, ISO 27001 / 42001
- **Verifier implementer** — Both sides ran the §7 verifier independently against their own chains
- **SDK implementer** — Capture-side library on each side emitting the §10.21 handover family

## Top spec sections used
- **§10.21** — Cross-vendor model-handover schema; the load-bearing primitive that makes two chains compose at the seam by byte-equal hash join
- **§10.20** — Training-data retention vs deployment-window discipline; the engagement drove this section's addition (90-day Lumiere retention vs 9-18-month Eberhardt deployment window)
- **§4.4.1** — `audit.cross_border_transfer.*` family; within-EU SHOULD per §10.21's worked-example paragraph
- **§7** — Twelve-step verifier procedure; PASS in 4 seconds against entries from the engagement morning and from 180 days prior
- **§5** — RFC 8785 JCS canonicalization plus SHA-256 yields the byte-identical values the cross-vendor anchor depends on
- **§10.17** — HSM partition-ceremony attestation with `entity_affiliation` field; both sides emit the event
- **§1.2** — Epistemic scope: chain proves what was deployed, not whether it was correct or unbiased
- **§10.18** — Runbook cross-referencing rule; cross-language CC8.1 discoverability for German / French / English readers

## All cited spec sections
- **§0.5.5** — Names the three companions outside the spec (auditor stories, question bank, reference implementation)
- **§1.2** — Epistemic scope split; the chain proves deployment integrity, not modeling correctness
- **§1.3** — Security definitions (EUF-CMA HMAC, Merkle second-preimage, Ed25519 EUF-CMA)
- **§1.4** — Compositional security argument extended across the organizational boundary
- **§3** — Definitions including tenant_id character class and chain_kind enumeration
- **§3.1** — Legacy tenant-identifier handling; both sides conform natively without aliasing
- **§4.1** — Per-event HMAC at capture under tenant-bound session key
- **§4.1.1** — Session-key handshake and per-tenant deterministic derivation
- **§4.2** — Daily Merkle seal in `(run_id, seq)` ordering; empty-day discipline
- **§4.2.1** — Daily seal cadence default
- **§4.2.2** — Day-boundary semantics by ledger `received_at` UTC; late-binding flag
- **§4.3** — HSM-rooted root signature; v1.0a (10-line) and v1.0b (12-line) `sign_payload` forms
- **§4.3.1** — HSM-unavailability 72-hour notification SHOULD
- **§4.4** — OTel-native wire format; SDK-side enforcement of `gen_ai.{request,response}.model`
- **§4.4.1** — `audit.cross_border_transfer.*` and `audit.routing.*` families; classifier_output captured before routing.attempt
- **§4.4.2** — Deployment-intent enum; canary requires `canary_traffic_pct` and `policy_version`
- **§4.4.3** — OTLP transport identification (Resource attributes)
- **§4.4.4** — Severity stamping for chain traffic 9..20
- **§5** — RFC 8785 JCS canonical form for MAC input
- **§5.1** — TLS 1.3 minimum transport encryption floor
- **§7** — Twelve-step verifier procedure with normative output format
- **§8** — Conformance test-vector corpus enabling cross-vendor byte equality
- **§10.1** — Key-fingerprint reconciliation registry
- **§10.2** — Operational events (`master.cross_region_replication_completed`, `chain.coverage_map_published`)
- **§10.3** — Append-only enforcement at app and DB role layers
- **§10.4** — NTP discipline; ledger `received_at` authoritative
- **§10.5** — HSM custody at FIPS 140-2 Level 3+
- **§10.6** — IKM minimum 32 bytes
- **§10.6.1** — IKM generation requirements (FIPS-validated CSPRNG)
- **§10.8** — Constant-time comparison MUST
- **§10.10** — IKM rotation crossing the seal boundary
- **§10.10.1** — Hourly-cadence rotation discipline
- **§10.10.2** — Within-day algorithm rotation (Pattern A / B)
- **§10.12** — Verifier exit-code contract (0 PASS)
- **§10.13** — Evidentiary artifacts retention; live-trace screen recordings filed
- **§10.14** — RFC 3161 trusted-time RECOMMENDED
- **§10.15** — Multi-region resilience Pattern A (synchronous-read replication completion)
- **§10.16** — SaaS-edge connector lag bounds
- **§10.17** — HSM partition-ceremony attestation with `entity_affiliation`
- **§10.18** — Runbook cross-referencing; cross-language CC8.1 discoverability
- **§10.19** — Chain-coverage map; `audit.external_artifact.*`; CRM scoped out
- **§10.20** — Training-data retention floor; drove the §10.20 amendment (Finding #1 Partial)
- **§10.21** — Cross-vendor model-handover schema with contract triple, plural-array `audit_report_languages`, `training_data_retention_floor_days`
- **§10.21.3** — Registry-discovery cross-anchor pattern (referenced by contrast)
- **§10.22** — Pre-MAC SDK redaction discipline (`disposition = "redacted_at_sdk"`)
- **§10.24** — Entity succession; cited for hypothetical M&A continuity
- **§10.25** — Run-resume and chain-tail acquisition discipline
- **§10.26** — Reference verifier distribution (CC8.1 names verifier and version)
- **§10.66** — Model-weight lineage DAG that extends §10.21 single-handover into multi-step lineage
- **§11** — References (verifier version pinned)
- **§12** — Change log; the §10.20 + §10.21 errata cite this engagement as the worked example
- **§13** — Stakeholder navigation (BSI / LfDI / CNIL / OEM vendor-management / ISO 26262 reader paths)

## Synopsis

### Audit activity
Eight-person team split between Stuttgart and Paris on parallel CET tracks with a video bridge open for joint moments. The Stuttgart side walked the predictive-maintenance inference service (8 months sealed, OEM battery-health module, entry-of-the-day verifier PASS in 4 seconds across all twelve §7 steps; same against a 180-day-old entry). The Paris side walked the model-build pipeline on independent IKM, ANSSI-aligned OVHcloud HSM, fairness-audit hash anchored in chain. The IAM walk on the Stuttgart side was a two-AD-domain shop with schema-enforced author-approver separation on the Paris side via SDK refusal. At noon the bridge ran the load-bearing test: byte-equal compare of the model-artifact, model-card, and fairness-audit-report SHA-256s pulled from both terminals; all three matched. The 3 PM joint reconciliation traced one OEM alert through seven legs (vehicle to inference to §10.21 model-handover to model-build to fairness-audit to training-data manifest to per-shard transfer reconciliation) under fifteen minutes elapsed, byte-equal hash matches at every cross-vendor anchor.

### How the spec was used

- **§10.21** — Cross-vendor anchor was the structural feature being tested; provided the joint integrity claim without trust in either party's claim
- **§7** — Each side's chain independently verified; produced the per-chain verifier output that the cross-anchor join consumes
- **§5 / §8** — RFC 8785 JCS canonicalization plus shared test-vector corpus made byte-equal hash join achievable across the two independent implementations
- **§10.20** — Spec's resolution path for the training-data retention asymmetry surfaced mid-morning (90-day retention on the model-build side vs 9-18-month deployment window on the inference side)
- **§10.20 GDPR-tension resolution** — Article 6(1)(f) legitimate interest tied to EU AI Act Article 12 logging, with Article 35 DPIA; framed the 24-month retention commitment within ninety minutes
- **§1.2** — Epistemic scope governed the chain-vs-correctness boundary in the close-out language
- **§4.4.1** — Cross-border-transfer attribute; Finding #2 (Nit, within-EU SHOULD per §10.21's worked-example paragraph)
- **§10.21 plural-array `audit_report_languages`** — Finding #3 (Nit, fairness-audit entry singular)

### Results
Per-company: zero Gaps, zero Partials on either side. Joint: zero Gaps, one Partial (§10.20 retention floor; CAPA in flight to 24 months), two Nits (§4.4.1 cross-border-transfer emission, §10.21 plural-array fairness-audit alignment). End-to-end seven-leg trace traversable in under fifteen minutes elapsed with byte-equal hash matches at every cross-vendor anchor. Five-reader regulator matrix satisfied: EU AI Act Articles 11 / 12 / 16, BSI IT-Grundschutz + ISO 27001 + ISO/IEC 27017 + TISAX, LfDI / CNIL joint GDPR (with Nit), OEM vendor-management three questions answered explicitly, ISO 26262 trail-supporting with ISO/SAE 21434 + WP.29 R155 / R156 composing alongside. The engagement drove §10.20 and §10.21 into the spec body as the fourth errata; §10.20 names the case as its worked example and §10.21 names the within-EU exemplar in the cross-border-composition note and the plural-array discipline. Commitment from the model-build side: English fairness-audit translation in four weeks, bilingual-or-trilingual audit bodies as standing practice, 24-month retention as a permanent line in the model-supply DPA.
