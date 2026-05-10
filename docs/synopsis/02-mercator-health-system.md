# Story 02 — Mercator Health System (HITRUST + HIPAA + FDA SaMD post-market combined assessment)

**Story file:** `docs/auditor-stories/02-mercator-health-system.md`
**Engagement type:** HITRUST CSF v11 + HIPAA Security Rule + FDA SaMD post-market combined assessment of a top-20 integrated health system; chain live on one inference path (sepsis CDS) for 90 days.
**Posture going in:** Partial deployment with an explicit institution-side ask to find and name the gaps so the remediation budget can be funded.
**Outcome posture:** Gap-finding — bifurcated assessment, AI side passes, legacy side carries 5 Gaps + 7 Partials.

## Type of audit
A combined HITRUST CSF v11, HIPAA Security Rule, and FDA SaMD post-market surveillance review framed deliberately as a bifurcated assessment. What makes it distinctive is the institution's explicit ask: a §10.19 chain-coverage map exists with one green zone (sepsis CDS, end-to-end) and one red zone (everything else), and the audit's job is to grade both halves so the budget request to extend the chain has documentation behind it.

## Interested parties (spec readers)
- **FDA Bioresearch Monitoring (BIMO) inspector** — clinical decision support read against ALCOA+; the FDA reviewer ran the published reference verifier independently against the quarterly post-market surveillance package.
- **HHS Office for Civil Rights (HIPAA)** — PHI integrity and Security Rule mapping; PHI-in-CRM and minimum-necessary discipline are central to the legacy-side findings.
- **Chief Information Security Officer (CISO)** — institution-side cyber posture and threat-model owner; the engagement is structured to fund the gap-remediation budget.
- **Model Risk Management committee chair** — SR 11-7 lifecycle reading of clinical CDS as model-risk control; deployment-intent capture and pre-launch backfill provenance are exercised.
- **Chief AI / ML Officer** — owns the AI estate and the SDK adoption scope; reads to see how a partial deployment is bounded and extended.
- **Chief Compliance Officer / CRO** — HIPAA + HITRUST + FDA multi-framework posture across one engagement.
- **Internal audit team** — bifurcated grading exercise illustrates how to scope chain-coverage testing against an explicitly-disclosed boundary.
- **SOC 1 / SOC 2 engagement team** — the §10.19 coverage-map pattern and the legacy evidentiary-substitute discipline are both directly applicable.
- **Big-Four assurance audit** — cross-framework attestation (HITRUST + HIPAA + FDA) read in one engagement.
- **Cryptographic expert witness (Daubert)** — three-layer compositional security and HSM custody contrasted against legacy single-custody-layer systems.

## Top spec sections used
- **§1.2** — epistemic scope; cited explicitly to define what the chain proves (model said X at time T, record untampered) and what it does not (clinical accuracy, policy compliance, bias).
- **§10.19** — chain-coverage map; the conceptual spine of the bifurcation, with the green zone naming chain-instrumented systems and the red zone naming evidentiary substitutes for unchained ones.
- **§4.4** — chain-envelope attribute table including the OpenTelemetry GenAI envelope (`gen_ai.request.model` and `gen_ai.response.model` REQUIRED on every model-call entry).
- **§4.4.2** — deployment-intent capture (production / canary / ab_test); the February v3.2.0 to v3.1.7 rollback was a sealed canary entry.
- **§7 / §10.12** — 12-step verification procedure and the verifier exit-code contract; FDA reviewer ran it independently.
- **§10.13** — evidentiary-artifacts retention list, contrasted against Mulesoft 6-week retention, Epic 90-day audit-view, and CRM 30-day backups.
- **§10.16 + §4.4.6** — SaaS-edge connector lag-bound discipline; flagged as a forward-looking constraint when the chain is extended to the CRM.
- **§10.5 / §10.3 / §1.4** — HSM custody, append-only storage at the storage tier, and three-layer compositional security; cited repeatedly to contrast the sepsis chain's defense-in-depth against the legacy environment's single custody layer (the engineers).

## All cited spec sections
- **§0.5** — reading-the-document framing; the FDA reviewer used the 30-minute critical-paths triage.
- **§1.1** — Daubert four-factor grounding in spec text.
- **§1.2** — epistemic scope; the load-bearing spec citation across the engagement.
- **§1.3** — security definitions and known error rate.
- **§1.4** — three-layer compositional security (IKM, ledger storage, HSM).
- **§3** — definitions table including `chain_kind` enumeration (`audit | model_call | tool_call | routing | translation | operational`).
- **§4** — primitives framing and topology rule.
- **§4.1** — Primitive 1 HMAC chain at capture; per-tenant determinism property.
- **§4.1.1** — session-key handshake; institution runs Model B (HSM-resident PRK with SDK-side Expand).
- **§4.2** — Primitive 2 daily Merkle seal; seal record schema with `public_key_id`.
- **§4.2.1** — daily cadence default.
- **§4.2.2** — day-boundary semantics by `received_at`.
- **§4.3** — HSM-rooted root signature; algorithm rotation rules.
- **§4.3.1** — HSM unavailability and 72-hour notification SHOULD; the April 18 maintenance window invocation.
- **§4.4** — chain envelope and OpenTelemetry GenAI envelope.
- **§4.4.2** — deployment-intent enum and conditional-required `policy_version`.
- **§4.4.3** — OTLP transport identification with required Resource attributes.
- **§4.4.4** — severity for chain traffic; collectors MUST NOT severity-filter.
- **§4.4.6** — SaaS-edge connector source attribution (cited as the pattern the unchained CRM and lab pipeline would adopt).
- **§5** — canonical-form exclusion rule; what the per-event MAC covers.
- **§7** — 12-step verification procedure.
- **§10.1** — key-fingerprint reconciliation discipline (cited for AD modernization analogy).
- **§10.2** — operational events.
- **§10.3** — append-only enforcement at storage tier and database role layers.
- **§10.4** — NTP discipline for application hosts and the ledger.
- **§10.5** — HSM custody at FIPS 140-2 Level 3+.
- **§10.6** — IKM minimum length 32 bytes.
- **§10.6.1** — IKM CSPRNG generation requirements.
- **§10.7** — software-key adapter exclusion in production.
- **§10.8** — constant-time comparison MUST.
- **§10.10** — IKM rotation crossing the seal boundary.
- **§10.11** — adverse-action notice translation chain entries; cited by analogy for prior-auth adverse-determination notices and state-insurance regimes.
- **§10.11.1** — ECOA adverse-action reasons schema.
- **§10.11.2** — FCRA reinvestigation timing; cited by analogy for CMS-0057-F prior-authorization timing.
- **§10.12** — verifier CLI exit-code contract.
- **§10.13** — evidentiary-artifacts retention list.
- **§10.14** — trusted-time integration (RFC 3161); flagged as not-yet-adopted for FDA-litigation-anticipated workloads.
- **§10.15** — multi-region resilience patterns; cited for future insurance-arm tenant_id discipline.
- **§10.16** — SaaS-edge mirror connector lag bounds; flagged as a forward-looking constraint when extending the chain to the CRM.
- **§10.17** — HSM partition ceremony attestation.
- **§10.18** — CC8.1 and runbook cross-referencing to spec sections.
- **§10.19** — chain-coverage boundary documentation; the spine of the bifurcation.
- **§10.20** — training-data retention vs deployment-window discipline; applied to the pre-launch backfill 18-day overlap.
- **§10.21** — cross-vendor model-handover schema; cited as the EHR-write-back chain extension pattern.
- **§10.22** — pre-MAC redaction discipline.
- **§10.23** — consumer-correlation index integrity; cited for the editable claims ETL checksum table.
- **§10.24** — entity succession.
- **§10.25** — run resume and chain-tail acquisition; flagged for the upcoming chain extension.
- **§10.26** — reference verifier distribution; FDA reviewer used the Cosign-signed binary path.
- **§10.66** — model-weight lineage across multi-month runs; cited for v3.2.1's deployed-weights hash.
- **§10.67** — pre-deployment evaluation chain (`audit.evaluation.run/result/disposition`); cited for FDA pre-clearance evaluation.
- **§13** — stakeholder navigation entry points.
- (Non-spec regulatory citations: HIPAA §164.312 audit controls, 45 CFR 164.530(j)(2) HIPAA 6-year retention floor, Cal Insurance Code §791.10, FCRA §611.)

## Synopsis

### Audit activity
The audit was bifurcated. The AI side covered the sealed sepsis-CDS inference path (90 days of chain entries, 247 predictions per day) and an IAM split (sealed service IAM versus unchained legacy AD with 23 active temporary admins, oldest from 2019). The legacy sweep covered a Salesforce CRM with field-history disabled for storage-cost reasons (HITRUST Partial renewed three cycles unfunded), a Mulesoft Epic-billing handoff with a 6-week retention dial controlled by 8 engineers, a lab pipeline with 3-day DLQ and CloudTrail-disable-able S3, and a claims ETL with an editable checksum log. A five-alert end-to-end reconciliation test reconciled 5/5 inference, 4/5 backward (one source lab record purged 60 days ago by a now-disabled retention job), and 3/5 forward (two Epic notes rewritten post-hoc).

### How the spec was used

- **§1.2** — Epistemic scope was the most-cited section, drawing boundaries between model output, clinical judgment, and lab inputs.
- **§10.19** — Chain-coverage map provided the conceptual spine: green zone for sepsis-CDS, red zone for everything else, evidentiary substitute named for each unchained system.
- **§4.4** — Grounded the AI-side confirmations (both `gen_ai.request.model` and `gen_ai.response.model` populated, `audit.deployment.intent`/`policy_version` on every entry, `chain_kind` enumerated correctly).
- **§10.13** — Contrasted with Mulesoft 6-week and Epic 90-day retention.
- **§10.16 + §4.4.6** — Forward-looking constraints for the future CRM connector.
- **§10.26** — Verifier distribution already in operational use — the FDA reviewer had run the reference verifier independently against the prior quarter's surveillance package.

### Results
Bifurcated outcome reflecting the institution's posture. **AI side:** 8 confirmations, 0 Gaps, 0 Partials, 0 §10.16 non-conformances — audit-passes. **Legacy side:** 5 Gaps + 7 Partials across legacy AD, Mulesoft, claims DynamoDB, lab pipeline (no cross-destination reconciliation, mutable storage), claims ETL (editable checksum table), Epic boundary (rooting failure on one of five tested alerts), override reasoning (mutable Epic notes), and the CRM (PHI in unaudited free-text). The bifurcation framing was approved for the next board cycle; sequencing recommendation prioritized lab first, EHR second, billing third — protect the input side before the output side.
