# Story 04 — Atrio Banking Platform (vendor-side BaaS audit read by 5 concurrent regulator audiences)

**Story file:** `docs/auditor-stories/04-atrio-banking-platform.md`
**Engagement type:** Vendor-side platform audit of a Banking-as-a-Service infrastructure (12 sponsor banks, 47 fintech programs, 2 AWS regions active-active, 24 months on chain), read concurrently by three state banking departments (Indiana, North Carolina, Georgia), the OCC, and CFPB during a coordinated examination cycle.
**Posture going in:** Multi-tenant pressure test of a vendor-side platform claim under five regulator audiences in the same building.
**Outcome posture:** Confirmation — 21 confirmations, 1 Partial (§10.15 invariant-5 cache lag, fix in flight), 1 Nit (§10.18 missing cross-reference).

## Type of audit
A vendor-side platform audit structured for the BaaS-industry coordination model: one external audit at the platform serves five regulator audiences concurrently in the same building. What makes it distinctive is the multi-tenant pressure test (12 sponsor banks × 47 fintech programs × 2 regions × 24 months) and the coordinated-examiner room next door — three state examiners, one OCC examiner, one CFPB analyst all running independent queries against partitioned credentials at the same time.

## Interested parties (spec readers)
- **FFIEC IT Examiner (FDIC / OCC / FRB)** — multi-tenant BaaS-industry coordinated-examiner cycle; cross-bank comparisons under partitioned scope.
- **FFIEC Cybersecurity Specialist Examiner** — multi-tenant scale, HSM partition discipline, supply-chain trust path under NIST CSF 2.0.
- **FFIEC Examiner-in-Charge (EIC)** — examination logistics for a coordinated-examiner room with five regulator audiences in parallel.
- **CFPB consumer-protection examiner** — consumer-protection cross-bank scope; §10.3 + §10.4 backdating-detection on consumer-complaint events; §1033 customer-data right.
- **FTC AI / privacy examiner** — UDAP / AI-driven consumer harm in a BaaS context.
- **State attorney general** — state-level UDAP and consumer-protection enforcement coordination.
- **Federal Reserve / OCC payments examiner** — sponsor-bank Fedwire / ACH cross-anchor flow.
- **Vendor management lead** — sponsor-bank vendor-management cycles read the audit report through master services agreements.
- **Chief Information Security Officer (CISO)** — 2-of-2 PIN split for every sponsor bank's HSM partition; institutional cyber posture across twelve concurrent CISOs.
- **SOC 1 / SOC 2 engagement team** — vendor-side platform audit feeds Section 4 description, control-evidence schema, CUEC verification.
- **Big-Four assurance audit** — cross-framework attestation across SOC, ISAE, ISO 27001 / 42001.
- **SDK implementer / Ledger implementer / Verifier implementer** — multi-tenant deployment exercises tenant_id discipline, IKM registry uniqueness, three-place tail acquisition, and verifier exit-code contract end-to-end.

## Top spec sections used
- **§10.1** — IKM registry uniqueness constraint at the database layer; the load-bearing structural hinge of the entire platform claim, exercised through four adversarial inserts.
- **§4.1 + §4.1.1 Model B** — HKDF tenant binding via `info=info_base||'|'||utf8(tenant_id)` plus HSM-resident PRK with SDK-side Expand; cross-bank `tenant_id` collision safe because IKMs differ.
- **§10.15 Pattern A + invariant 5** — multi-region active-active with the invariant-5 normative text removing discretion on poll-cached replication-completion events for fast-cadence tenants. Generates Partial-001.
- **§10.12** — verifier CLI exit-code contract (exit 2 for procedure-could-not-begin); the closed-enumeration codes that ground the 5×5 cross-tenant refusal matrix.
- **§10.5 + §10.7 + §10.17** — HSM custody at FIPS 140-2 Level 3 (twelve Thales Luna partitions with 2-of-2 PIN splits), software-key adapter compile-exclusion, and partition-ceremony attestation with the M&A-P1 `entity_affiliation` addition.
- **§10.16 + §4.4.6** — SaaS-edge mirror lag bounds named by four quantified numbers (median 38s, 95th-percentile SLO 84s, alerting 150s, RTO 8min); severity-classification preserved against downgrade.
- **§10.11 / §10.11.1 / §10.11.2** — ECOA translation + adverse-action reasons + FCRA §611 reinvestigation lifecycle across the seven consumer-protection fintechs; SHAP feature attributions on adverse-action reasons.
- **§10.25 + §4.4 genesis-block uniqueness** — three-place tail acquisition with the SQLite sidecar single-writer-per-run lock; real-world rejoin from a us-east-2 cluster rebuild last week (five tenants, no re-genesis).

## All cited spec sections
- **§0.5.2** — Mermaid chain-at-a-glance diagram; institution-side opens every kickoff with it.
- **§1.1** — Daubert four-factor grounding.
- **§1.2** — epistemic scope and the SDK-process compromise residual fourth class.
- **§3 / §3.1** — definitions and tenant_id character class; legacy migration patterns in operational use (Pattern 2 controlled aliasing for three CJK/slash-bearing legacy names).
- **§4.1 / §4.1.1** — HMAC chain at capture; Model B HSM-resident PRK handshake.
- **§4.2 / §4.2.2** — daily Merkle seal; day-boundary semantics by `received_at`.
- **§4.3** — HSM-rooted root signature.
- **§4.4 / §4.4.1 / §4.4.2 / §4.4.3 / §4.4.4 / §4.4.5 / §4.4.6** — chain envelope, routing-event family with classifier_output pre-routing capture, deployment-intent (`production`/`canary`/`ab_test`/`unknown`), OTLP transport identification, severity stamping with QuickLogBuilder resolver, underwriting features and disparate-impact testing, SaaS-edge connector source attribution.
- **§5 / §5.2** — canonical-form exclusion; best-evidence content-vs-integrity split.
- **§7** — 12-step verification procedure.
- **§8** — conformance test vectors as the SDK-side gate.
- **§10.1** — key-fingerprint reconciliation; tenant_id uniqueness at IKM registry; multi-deployment global uniqueness.
- **§10.2** — operational events (full BaaS-specific catalog including `master.cross_region_replication_completed`, `connector.lag_observation`, `chain.partition_ceremony_attended`, `chain.coverage_map_published`, `consumer_index.attestation`).
- **§10.3** — append-only enforcement (dual-layer at app code and ledger-writer DB role).
- **§10.4** — NTP discipline; ledger receive timestamp authoritative.
- **§10.5** — HSM custody at FIPS 140-2 Level 3; seal-job operator role separation.
- **§10.6 / §10.6.1** — IKM minimum length and HSM-internal CSPRNG.
- **§10.7** — software-key adapter exclusion (compile-time + verifier `--strict`).
- **§10.8** — constant-time comparison.
- **§10.9** — IKM registry retention coupling.
- **§10.10 / §10.10.1** — IKM rotation crossing seal boundary; hourly cadence with multiple mixed-version seals (Cardinal National rotation 8 months ago).
- **§10.11 / §10.11.1 / §10.11.2** — ECOA translation, adverse-action reasons, FCRA reinvestigation.
- **§10.12** — verifier CLI exit-code contract (closed enum 0/1/2/3).
- **§10.13** — evidentiary-artifacts retention and FRE 901(b)(9) authentication-of-the-process.
- **§10.14** — trusted-time integration (RFC 3161 not yet adopted by the platform).
- **§10.15** — multi-region resilience Pattern A; invariant 5 normative text generates Partial-001.
- **§10.16** — SaaS-edge mirror connector lag bounds; severity-classification clause.
- **§10.17** — HSM partition ceremony attestation.
- **§10.18** — runbook cross-referencing (the missing §10.1 reference is Nit-001).
- **§10.19** — chain-coverage boundary documentation.
- **§10.22** — pre-MAC redaction discipline.
- **§10.23** — consumer-correlation index integrity (Shape 2 daily attestation).
- **§10.24** — entity succession (exercised 18 months earlier when the platform acquired a smaller BaaS competitor).
- **§10.25** — run resume and chain-tail acquisition.
- **§10.26** — reference verifier distribution discipline.
- **§10.27 / §10.28 / §10.29** — streaming cadence, streaming IKM rotation, streaming verifier procedure (used by 3 high-volume issuing-bank tenants).
- **§10.65** — hyperscale GPU-fleet attestation (platform fraud/credit/AML inference fleets).
- **§10.69** — per-customer audit-trail subset disclosure (CFPB §1033 compliance).
- **§11** — references; spec pins reference verifier version.
- (Non-spec regulatory citations: ECOA Reg B §1002.9, FCRA §611, CFPB §1033 / 12 CFR Part 1033, RFC 9101 LEI.)

## Synopsis

### Audit activity
The audit opened with an IKM-registry walkthrough — 12 banks, 47 fintechs, schema with `(bank_id, tenant_id)` PRIMARY KEY plus UNIQUE INDEX. Four adversarial inserts ran against a staging copy: duplicate-within-bank rejected, same-tenant-across-banks correctly accepted, empty-string rejected by the 2024 bug-fix check constraint, null bank_id rejected. Five examiner credentials were exercised in sequence to confirm three-layer scope partitioning, and a 5×5 credential-by-target refusal matrix returned 25 of 25 expected outcomes. A 10-random-triple Merkle reconciliation returned 10 of 10 PASS. The coordinated-examiner room ran in parallel with five regulator audiences executing independent queries. The day closed with a 1,410-run nightly verifier batch (47 fintechs × 30 days, 86 seconds wall clock, 1,410 of 1,410 PASS).

### How the spec was used

- **§10.1** — IKM registry constraint provided the structural hinge whose adversarial-insert tests grounded the entire multi-tenant claim; the four inserts mapped one-to-one against §10.1's normative semantics.
- **§10.15 invariant 5** — Clarification (poll-cached store non-conformant regardless of cache freshness window for fast-cadence tenants) made Partial-001 mechanically determinable; without the clarification, an older reading would have called a five-minute-cache-against-one-hour-seal conformant.
- **§10.16** — Severity-classification clause preserved the non-conformance bar against any downgrade of imprecise lag wording.
- **§10.26** — Distribution discipline (reproducible builds, Cosign-signed releases, SHA-256/512 manifests, SBOM) made the coordinated-examiner room functional — five examiners running independent verifier copies converged on byte-identical output.
- **§10.23 Shape 2 + §10.69** — Daily `consumer_index.attestation` plus per-customer disclosure cover the CFPB cross-bank query path.

### Results
21 confirmations, 0 Gaps, 1 Partial, 1 Nit. **Partial-001:** the `master.cross_region_replication_completed` event reads source-region count from a five-minute-stale internal cache; chain and seal correctness intact (§10.15 invariants 1-4), only invariant-5 affected; engineering ticket open with 60-day ETA, push-update mechanism replaces the cache poll. The institution had caught it internally six weeks before the audit. **Nit-001:** the platform runbook 'Multi-Tenant Operations' section omits the §10.1 cross-reference (§4.2, §10.5, §10.15, §10.16, §10.17 are correctly cross-referenced); 30-minute fix accepted same-day. The 1,410-run verifier batch returned 1,410 PASS, 0 FAIL in 86 seconds wall clock.
