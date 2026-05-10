# Story 08 — NetiVa Intelligence Ltd. (multi-tenant Israeli AI vendor under nation-state threat model)

**Story file:** `docs/auditor-stories/08-netiva-tel-aviv.md`
**Engagement type:** Independent vendor-management evaluation commissioned by a $180B US OCC-regulated regional bank, cost-shared with the Israeli AI vendor, deliverable consented for Bank of Israel (Pikuach HaBankim — Directives 357 / 359 / 361 / 365 / 367 / 411 / 414) and Israeli Securities Authority — Day 1 of a 3-day visit.
**Posture going in:** TesseraSeal in production for 14 months across 23 Tier-1 customer-banks (US, UK, Singapore, Israel, Australia), ~110 tenants, two Israeli regions under §10.15 Pattern A, INCD-coordinated 18-month-dwell threat assumption.
**Outcome posture:** Confirmation; one Partial closed-by-spec at §10.17 (this engagement is in the spec change-log as the source of the section); one Nit closed against §10.18 cross-referencing.

## Type of audit
Multi-tenant SaaS vendor evaluation under a nation-state threat model — IRGC cyber and Lazarus-equivalent assumed continuously present; 23 customer-banks → 23 IKMs in dedicated FIPS 140-2 Level 3 partitions on Thales Luna 7000s at a colocation facility; ~110 `tenant_id` values under per-bank IKMs with HKDF binding. Distinct because the engagement bridges three audiences (the customer-bank's vendor-management committee, the AI vendor's audit committee, Bank of Israel + ISA on supervisory cycle) and one regulator-coordination relationship (INCD's banking-sector liaison who attended unannounced).

## Interested parties (spec readers)
- Bank of Israel + ISA + INCD (Israeli triplet) — coordinated supervision of Israeli AI vendors under nation-state threat model.
- FFIEC IT Examiner (downstream-bank-side) — US OCC-regulated customer bank's examination cycle.
- FFIEC Cybersecurity Specialist Examiner — NIST CSF 2.0 alignment, threat-model review, supply chain.
- Vendor management lead — vendor-hosted controls, supply-chain trust path, BYOC topology.
- Chief Information Security Officer (CISO) — institutional cyber posture; HSM custody under nation-state threat assumption.
- Cryptographic expert witness (Daubert) — independent testimony on chain integrity, threat model, and HSM custody.
- AI vendor product-engineering team — partner side of cross-anchor design and chain instrumentation.
- SDK implementer — capture-side library author.
- Ledger implementer — ingestion + seal job + HSM root signature.
- Verifier implementer — clean-room verifier; per-customer-bank reference-verifier distribution.
- DevSecOps / SRE on-call — multi-region resilience, run-resume, INCD tabletop posture.
- Big-Four assurance audit — cross-framework attestation reading the deliverable.

## Top spec sections used
- **§1.4** — Three-layer compositional security (per-event HMAC + daily Merkle seal + HSM signature) at 128-bit composite under NIST SP 800-175B; named unprompted as the design backbone.
- **§10.1** — IKM-registry uniqueness across 23 customer-banks; PRIMARY KEY + UNIQUE INDEX on `(bank_id, tenant_id)`; three adversarial inserts behave per spec.
- **§10.5** — FIPS 140-2 Level 3 plus EAL4+ Common Criteria elevation above the spec floor; FIA residual-risk acceptance documented in CC8.1.
- **§10.15** — Multi-region Pattern A across two Israeli regions; live-failover tested twice; spec freshness rule (synchronous-read at emission) honored on `master.cross_region_replication_completed`.
- **§10.17** — HSM partition-ceremony attestation (the spec section this engagement produced); `chain.partition_ceremony_attended` event with `attendance_pdf_sha256` and RECOMMENDED `hsm_attestation_token_b64`; cross-language CC8.1 discoverability clause.
- **§10.18** — CC8.1 and runbook cross-referencing; the Hebrew internal-ops runbook Nit closes against this rule.
- **§10.25** — Run-resume and chain-tail acquisition; the April 30 replay went through in-memory tail acquisition with ledger ingestion cross-check on `(prev_hash, seq)` monotonicity.
- **§10.69 / §10.70** — Per-customer audit-trail subset disclosure and BSA SAR / privileged-investigation overlay (forward-looking forks for the customer-bank's downstream FinCEN-filing and CFPB CID exposure).

## All cited spec sections
- **§1.2** — Epistemic scope; framing for customer-bank Day-1 onboarding.
- **§1.3** — EUF-CMA / second-preimage / EUF-CMA composition; effective security 128 bits per NIST SP 800-175B.
- **§1.4** — Compositional security across three independent layers; design backbone.
- **§2** — Out-of-scope framing.
- **§3** — `tenant_id` character class enforcement (no `|` byte; HKDF info parameter unambiguous).
- **§3.2** — Pattern selection for legacy identifiers (not engaged today).
- **§4** — Four primitives.
- **§4.1** — Per-event HMAC; HKDF tenant binding (same `tenant_id` across two banks accepted because IKMs differ).
- **§4.2** — Daily Merkle seal; defense-in-depth deletion catch.
- **§4.2.2** — Day-boundary semantics by `received_at` UTC.
- **§4.3** — `sign_payload_version = "v1.0b"` 12-line form; binds `key_versions_canon` and `hex(kms_handle_uris_digest)`.
- **§4.4** — `audit.cross_border_transfer.*` family stamped on US→IL and IL→US legs; `ffiec.chain.region` per entry.
- **§4.4.6** — SaaS-edge connector source attribution on the customer-bank Salesforce CRM mirror.
- **§5** — Wire format; RFC 8785 JCS; canonical-form exclusion; test-vector 008 NaN/Infinity case (April 30 serialization bug closed in regression).
- **§7** — 12-step verification; matrix testing 4×4 morning + 25-concurrency afternoon, all behave per §10.12.
- **§9** — Security considerations pointer to threat-model design doc; engaged at INCD tabletop.
- **§10.1** — Multi-tenant IKM registry uniqueness; cross-bank isolation by per-bank IKM.
- **§10.2** — Operational events (`chain.verification_failure`, `master.cross_region_replication_completed`, `seal.job_*`, `master_key.rotation_observed`, `connector.lag_observation`, `connector.outage`, `chain.coverage_map_published`).
- **§10.3** — Append-only enforcement at application + database-role layers; April 30 originals + replay both retained.
- **§10.4** — NTP discipline (`time.cloudflare.com` primary, `il.pool.ntp.org` backup).
- **§10.5** — FIPS 140-2 Level 3 + EAL4+ HSM custody.
- **§10.6 / §10.6.1** — 32-byte IKM minimum; HSM-internal CSPRNG (`rng_source = "hsm.thales-luna-7000"`).
- **§10.7** — Compile-time software-key adapter exclusion.
- **§10.8** — `hmac.compare_digest` for fingerprint and MAC checks.
- **§10.9** — IKM-registry retention coupled to chain-entry retention; `master_key.retired` logs override.
- **§10.10** — IKM rotation across the seal boundary; two rotations in 14 months.
- **§10.10.2** — Within-day algorithm rotation Pattern A/B (forward-readiness; not exercised).
- **§10.11** — ECOA translation discipline parent-linkage.
- **§10.11.1** — Adverse-action reasons schema stamped on AML-decision entries feeding downstream notice generation.
- **§10.12** — Verifier CLI exit-code contract; cross-tenant ACCESS_REFUSED at credential check before any chain bytes are read.
- **§10.13** — Evidentiary-artifacts retention nine years (chain plus two-year litigation buffer).
- **§10.14** — Trusted-time integration RECOMMENDED; pre-MAC vs post-MAC posture plan documented.
- **§10.15** — Multi-region Pattern A with seal-region pinning; live-failover tested twice; freshness rule synchronous-read.
- **§10.16** — SaaS-edge mirror connector for customer-bank Salesforce CRM; four numbers named (median 12s, p95 SLO 60s, alert 90s, RTO 5min); severity-classification clause.
- **§10.17** — HSM partition-ceremony attestation (this engagement is the source per §12 change-log); cross-language CC8.1 discoverability clause.
- **§10.18** — CC8.1 and runbook cross-referencing rule.
- **§10.19** — Chain-coverage map version-stamped per M&A-P3 (`coverage_map_version`, `effective_utc`, `coverage_map_sha256`); monthly re-emission cadence; external-evidentiary artifacts hash-anchored.
- **§10.21** — Cross-vendor model-handover schema with M&A-G2 contract triple (forward-readiness).
- **§10.22** — Pre-MAC SDK redaction; PPL Amendment 13 sensitive-information classification + GDPR Article 5(1)(c) co-satisfied.
- **§10.23** — Consumer-correlation index Shape 1 (chain-anchored); CFPB CID reproducible from chain alone.
- **§10.24** — Entity-succession framework (forward-readiness if vendor is acquired).
- **§10.25** — Run-resume and chain-tail acquisition; April 30 replay path; ledger ingestion cross-check; single-writer-per-run.
- **§10.26** — Reference-verifier distribution; per-customer-bank CC8.1 names implementation/version/key.
- **§10.69** — Per-customer audit-trail subset disclosure (forward-fork for downstream CFPB CID exposure).
- **§10.70** — BSA SAR / privileged-investigation overlay; downstream FinCEN-filing maps directly; role-based verifier dispatch.
- **§11** — References; pinned reference verifier release.
- **§12** — Change log naming this engagement as the source of §10.17.
- **31 USC §5318(g)** — BSA SAR filing crosses into §10.70 territory.

## Synopsis

### Audit activity
The Day-1 architecture walkthrough covered 23 customer-banks, 23 partitions on twelve PCIe Luna 7000s split across two Israeli regions, 2-of-2 PIN split between customer-bank and AI-vendor CISOs at onboarding. Three adversarial inserts on the staging IKM registry — duplicate within bank rejected, same `tenant_id` across two banks accepted (cross-bank isolation by per-bank IKM), short `tenant_id` rejected. Customer-bank verifier credential rotation runbook walkthrough at the colocation surfaced a Hebrew-only internal-ops runbook gap that became Finding-001 against the cross-language CC8.1 discoverability clause. The afternoon pulled the April 30 NaN-handling serialization-bug incident (caught by the operational verifier, closed in 6h 23m, eleven entries replayed under §10.25). The HSM partition-ceremony attendance log surfaced as paper-and-PDF rather than chain-coupled — the Partial that became §10.17 normative spec text after the engagement.

### How the spec was used

- **§1.4** — Three-layer compositional argument was the design backbone named at the threat-model exchange.
- **§10.1** — IKM-registry uniqueness held across the 23-bank scaling factor with three adversarial inserts behaving per spec.
- **§10.5 / §10.6.1** — HSM-internal CSPRNG (`rng_source = "hsm.thales-luna-7000"`) elevated above the spec-conformance floor with EAL4+ Common Criteria for the INCD threat model.
- **§10.15 Pattern A** — Held under live-failover tested twice (most recent during a maintenance window, all 23 verifiers PASS the next morning).
- **§10.25** — Carried the April 30 replay through in-memory tail acquisition with ledger ingestion cross-check.
- **§10.16** — Four-number lag-bound discipline on the customer-bank Salesforce mirror was named by quantity (no `near real-time` adjective).
- **§10.22** — Pre-MAC SDK redaction co-satisfied PPL Amendment 13 sensitive-information and GDPR Article 5(1)(c) data minimization.
- **§10.17** — HSM partition-ceremony attestation was the spec section this engagement produced — the Partial surfaced on Day 1 became normative text in the post-engagement amendment, with a 60-day commitment landing the vendor on the right side of the post-spec normative bar before the Q4 IKM rotation cycle.

### Results
Twenty Confirmations, one Partial-at-engagement-time (closed-by-spec at §10.17 — the chain-coupled `chain.partition_ceremony_attended` event with `attendance_pdf_sha256` and RECOMMENDED `hsm_attestation_token_b64`; ETA 60 days), one Nit-at-engagement-time (the Hebrew-runbook cross-language CC8.1 discoverability gap; ~4 hours total fix; closed against §10.17 cross-language clause + §10.18 cross-referencing rule jointly; closed before report filing). The April 30 NaN incident filed Directive 411 §3 at 16 minutes (well inside the 30-minute clock), met Directive 365 §3 2-hour first-restore, satisfied Directive 367 §4 cloud-and-AI logging duties — three Bank of Israel directives engaged on a single serialization bug. The customer-bank vendor-renewal posture supports a 30-day-notice OCC-acceptable framing because the chain is a property of data the bank has already received, not a service the vendor renders.
