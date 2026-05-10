# Story 10 — Salt Pond Toys (multi-location consumer-products recall-readiness audit)

**Story file:** `docs/auditor-stories/10-salt-pond-toys-rhode-island.md`
**Engagement type:** AI-quality and supply-chain integrity assessment ahead of (a) the annual CPSC cooperative-agreement audit, (b) the CBP CTPAT four-year revalidation due in nine months, (c) a Rhode Island AG consumer-protection lookback, and (d) a Target supplier-recall-readiness audit.
**Client:** Mid-size consumer-products manufacturer (~$320M revenue) — Newport HQ + Shenzhen QC office + Trans-Pacific Logistics LA + three contract factories in Guangdong (Shenzhen, Dongguan, Foshan).
**Posture going in:** TesseraSeal in production for eleven months across four `service.name` values under one `saltpond` tenant — `qc-vision-shenzhen`, `customs-entry-la`, `demand-forecast-newport`, `recall-traceability` — daily Ed25519 seals on AWS CloudHSM `us-east-1` per §4.3 v1.0b form.
**Outcome posture:** Confirmation on the AI services; one Partial in flight and funded mid-engagement (Section 321 de-minimis broker manual-step); two findings closed-by-spec at §10.19 + `audit.external_artifact.*` (the spec sections this engagement drove into the spec body per §12 fourth-errata change-log).

## Type of audit
Multi-location consumer-products recall-readiness audit composing CPSC cooperative-agreement scope (CPSIA Section 102 testing certificates), CBP CTPAT supply-chain security four-year revalidation, Rhode Island AG paperwork-only consumer-protection lookback, and Target supplier-recall-readiness contractual 24-hour window. Distinct because the chain was deployed eleven months ago after a 2024 inspector wrote "best characterized as recoverable rather than producible" in his closing memo on a false-alarm lead-paint scare. The chain spans three locations across twelve hours of time-zone (Newport ET + LA PT + Shenzhen CST); the bonded-carrier maritime leg is genuinely CBP's chain, and documenting the handoff is the goal rather than extending the chain into the maritime leg.

## Interested parties (spec readers)
- CPSC consumer-products safety inspector — 24-hour recall readiness; the cooperative-agreement annual audit closes the 2024 "recoverable rather than producible" inquiry.
- CBP customs / trade examiner — CTPAT four-year revalidation; CES-notice anchoring closes the only soft spot.
- Big-Four assurance audit — cross-framework attestation reading the deliverable.
- Chief Compliance Officer / CRO — multi-framework regulatory posture across CPSC, CBP, AG, and Target.
- General Counsel — FRE 902(13)/(14) self-authentication posture for litigation readiness.
- AI/ML Officer — QC vision, demand-forecast, customs-entry deployment-intent author.
- Vendor management lead — Bureau Veritas CPSIA-certificate cross-anchor; Phase 3 supplier-risk-scoring under §10.21.
- Forensic accounting / litigation-support — partial-disclosure verifier mode supports court-ordered selective production.
- M&A integration lead (acquired entity) — family-trust generational transition under §10.24 standing procedure.
- State attorney general — paperwork-only Rhode Island consumer-protection review.
- Target supplier-audit reviewer (private contractual party) — informative; the 14-minute recall response writes the audit response.
- Standards-body reviewer — informative; this engagement drove §10.19 + `audit.external_artifact.*` into PRD-1.

## Top spec sections used
- **§10.19** — Chain-coverage boundary documentation (the spec section this engagement drove into the spec body); five-category enumeration; version-stamped (v1.0, effective 2026-04-01) and chain-anchored via `chain.coverage_map_published` per M&A-P3.
- **`audit.external_artifact.*`** — Attribute family (informative, advisory; canonical at §10.19 with Appendix A.14 lookup) for hash-anchoring CES inspection notices, customs-broker case snapshots, factory access-log extracts, third-party signed PDFs, CPSIA certificates, bonded-carrier manifests; `intermediate_state` boolean attribute driven specifically by the Section 321 broker manual-step partial.
- **§10.16** — SaaS-edge capture connectors four-number lag bounds (median 30-60s, p95 SLO, alert 90-120s, RTO under one hour) for the Descartes broker-case webhook integration.
- **§4.4.6** — SaaS-edge connector source attribution (`audit.connector_source.*`) for Descartes integration; stable-`run_id` discipline tied to broker case ID.
- **§7 + §10.12** — 12-step verification with PASS in 3-4 seconds across 12 sample forecasts, 12 QC vision flagged units, 8 customs entries, all PASS.
- **§10.21.1 / §10.60** — Anti-counterfeit cross-anchor (extends sample-based-attestation) — the Bureau Veritas CPSIA-cert anchor is the canonical institutional analog.
- **§5.2 + §10.13** — Best-evidence posture (captured JSON content-bearing; canonical bytes integrity-bearing) backing FRE 902(13)/(14) self-authenticating electronic records for litigation posture.
- **§4.4.1** — Routing schema controlled-vocabulary discipline for QC override and customs broker-override workflows (no free-text rationale field by design).

## All cited spec sections
- **§1.2** — Epistemic scope (chain proves what the AI said; not whether the lot was defect-free); the Yantian-reliability framing.
- **§1.3** — Security definitions; EUF-CMA / second-preimage / EUF-CMA composition.
- **§1.4** — Compositional security; layered defense including PGP signature on CPSIA certificates as independent provenance alongside the chain anchor.
- **§2.1.1** — Out-of-scope framing for the Section 321 broker manual step.
- **§3** — `tenant_id` keying (`saltpond` per §3 boundary).
- **§3.1** — Legacy-identifier handling (not in play; tenant fresh from chain inception).
- **§4.1** — Per-event MAC; HKDF tenant binding.
- **§4.2** — Daily Merkle seal; deterministic ordering by `(run_id, seq)`.
- **§4.3** — HSM-rooted root signature; `sign_payload_version = "v1.0b"` 12-line locked form.
- **§4.3.2** — Algorithm rotation; HSM key on its own quarterly cadence.
- **§4.4** — OpenTelemetry-native wire; `gen_ai.*` semconv attributes per §A.2.
- **§4.4.1** — Routing schema with controlled-vocabulary `audit.routing.refusal_reason` discipline; classifier_output event for HTS classification (Phase 2).
- **§4.4.2** — Deployment-intent capture (`audit.deployment.intent = production`).
- **§4.4.3** — OTLP transport identification on every emitted Resource.
- **§4.4.4** — Severity for chain-of-custody traffic; 11 routine, 13 SCRAP_EYE_ATTACHMENT.
- **§4.4.5** — Underwriting features by analogy (supplier-risk scoring on Phase 3 roadmap).
- **§4.4.6** — SaaS-edge connector source attribution for Descartes integration.
- **§5** — Wire format; canonical-form exclusion rule.
- **§5.2** — Best-evidence posture under FRE 1001-1004.
- **§6** — Storage; ERP audit-log retention 3 years vs chain indefinite (intentional bifurcation).
- **§7** — 12-step verification under the recall-trace tool's hood.
- **§10.1** — Daily key-fingerprint reconciliation.
- **§10.2** — Operational events (`chain.coverage_map_published`, `connector.lag_observation`, `connector.outage`, rotation events).
- **§10.3** — Append-only enforcement at both application and database-role layers.
- **§10.4** — NTP discipline; verifier audit-procedure P-7.
- **§10.5** — HSM custody on AWS CloudHSM `us-east-1`; CTO + security director separation of duties; institutional Phase 2 wiring of `chain.partition_ceremony_attended` per §10.17 ahead of next IKM rotation.
- **§10.6 / §10.6.1** — IKM 32-byte minimum; RNG cryptographic strength; FIPS 140-3 attestation available.
- **§10.8** — Constant-time comparison MUST.
- **§10.10** — IKM rotation across the seal boundary.
- **§10.10.2** — Within-day algorithm rotation (not exercised).
- **§10.11.2** — FCRA §611 reinvestigation analog for product-recall communication timing (forward-readiness).
- **§10.12** — Verifier CLI exit-code contract (0/1/2/3, ≥4 vendor-specific) including PASS-STRUCTURALLY in witness mode.
- **§10.13** — Evidentiary-artifacts retention list backing FRE 901(b)(9) authentication.
- **§10.14** — Trusted-time integration (RFC 3161 informative).
- **§10.15** — Multi-region resilience; Pattern B per-region tenant boundaries (Newport / LA / Shenzhen each have their own SDK process, region-pinned).
- **§10.16** — SaaS-edge capture connectors four-number lag bounds for Descartes; severity-classification clause makes imprecise wording non-conformance.
- **§10.17** — HSM partition-ceremony attestation (forward-commitment ahead of next IKM rotation).
- **§10.18** — CC8.1 and runbook cross-referencing (recall-trace validation cadence + Section 321 webhook + CES anchoring runbook all cross-reference §10.19).
- **§10.19** — The spec section this engagement drove; five-category chain-coverage map enumeration; version-stamped per M&A-P3; `chain.coverage_map_published` operational event.
- **§10.20** — Training-data retention floor (in-house QC vision model, two-year retention exceeds eleven-month active deployment plus 60-90-day investigation buffer).
- **§10.21** — Cross-vendor model-handover schema (not active; Phase 3 roadmap for supplier-risk scoring).
- **§10.21.1** — Sample-based-attestation cross-anchor for lot-level binding (anti-counterfeit, AS6171, DARPA SHIELD); canonical institutional analog is the Bureau Veritas anchor.
- **§10.22** — Redaction discipline (pre-MAC at SDK boundary; QC override controlled-vocabulary discipline removes redaction question by design).
- **§10.23** — Consumer-correlation index forward-readiness (Shape 2 if AG opens consumer-keyed inquiry).
- **§10.24** — Entity succession (`chain.entity_succession`); standing procedure for the family-trust generational transition over the next decade.
- **§10.25** — Run resume and chain-tail acquisition; SQLite sidecar with file locking; ledger ingestion cross-check on `(prev_hash, seq)` monotonicity.
- **§10.26** — Reference verifier distribution; three-name CC8.1 citation.
- **§10.60** — Anti-counterfeit cross-anchor extending §10.21.1 (independent third-party AS6171/SHIELD attestation reference).
- **§11** — References; pinned verifier version.
- **§12** — Change log; §10.19 + `audit.external_artifact.*` lifted to spec body in fourth errata, naming this engagement as the source.
- **FCRA §611** — External citation for reinvestigation-clock analog (forward-readiness).

## Synopsis

### Audit activity
The team worked across three video tiles (Newport ET, LA PT, Shenzhen CST) and walked four chain instruments: QC, customs, forecast, recall. A March 21 demand-forecast for plush bears verified in four seconds. The QC vision dashboard showed a Dongguan run of 31,000 plush-bear units that day with 47 flagged (43 rework, 4 SCRAP_EYE_ATTACHMENT) — and the contract-factory floor-operator badge boundary surfaced (the Shenzhen QC supervisor is the chain-recorded actor; the factory-floor operator under that supervisor is in the factory's separate access-control system). Three-location IAM showed 23 credential rotations in eleven months. The bonded-carrier handoff conversation surfaced the CES inspection notice gap. A March 27 customs entry summary verified in three seconds; an HTS 9503→9504 broker-override per CBP ruling letter was sampled. The customs pipeline mapped to five legs and five hashes; the Section 321 de-minimis broker manual-step partial drove the `audit.external_artifact.intermediate_state` boolean. The Bureau Veritas CPSIA cross-vendor anchor walked in parallel — PGP signature plus chain hash byte-for-byte match. The recall-readiness exercise on lot 25-D-0492 — three thousand eight hundred and forty units, forty-seven retailers — produced a complete cross-location trace in fourteen minutes from cold pick. Phase 2 Descartes webhook funded mid-engagement ($60K) before the July 1 CBP rule effective date.

### How the spec was used

- **§10.19** — Chain-coverage boundary documentation (normative) driven into the spec body in fourth errata per §12 change-log; the factory-floor operator badge boundary became §10.19 category 3 (third-party systems under contractual inspection) with the contract-clause inspection right and the substitute audit procedure (the Shenzhen office's quarterly contract-compliance review) named.
- **`audit.external_artifact.*`** — Attribute family (canonical at §10.19 with Appendix A.14 lookup) folded into PRD-1 in fourth errata; the CES inspection notice gap became the worked example for `audit.external_artifact.kind = ces_inspection_notice` (six attributes: kind, identifier, sha256, received_at_utc, source_party=cbp_los_angeles, evidentiary_role=chain_of_custody_handoff).
- **`audit.external_artifact.intermediate_state`** — Section 321 broker manual-step partial drove the boolean — broker-saves-at-T1, broker-submits-final-ABI-at-T2 is the spec's verbatim worked example.
- **§10.21.1** — Anti-counterfeit sample-based-attestation extended to Bureau Veritas's CPSIA-cert lot-level attestation as the canonical institutional analog.
- **§1.2** — Epistemic scope framed Yantian's reliability honestly as institutional confidence, not chain evidence.
- **§5.2 / §10.13** — Backed the FRE 902(13)/(14) self-authentication posture; the partial-disclosure verifier mode (RFC 6962 §2.1.1 audit path) supports court-ordered selective production.

### Results
Four-audience summary: CPSC — 0 Gaps, 1 Partial (Section 321 de-minimis chain coverage; in flight, funded $60K, completion by July 1), 2 Findings closed-by-spec at §10.19 + `audit.external_artifact.*` (factory-floor operator badge boundary documentation, CES-notice hash anchoring). CBP CTPAT (9 months out) — 0 Gaps; CES-notice anchoring closes the only soft spot. Rhode Island AG — 0 Gaps, paperwork-only. Target — 0 Gaps; 14-minute reconciliation well inside the 24-hour contractual window. Sixteen Confirmations including the 2024-vs-2026 comparison (the 2024 inspector wrote "recoverable rather than producible"; the 2026 chain test on lot 25-D-0492 closes the same inquiry in fourteen minutes). Phase 1 deliverable: §10.19 chain-coverage map drafted overnight, signed Friday morning. Phase 2 (by July 1): Descartes webhook with §4.4.6 connector-source attribution + §10.16 four-number bounds + CES-notice anchoring + Yantian gate-out / LA receipt rename to `bonded_carrier_manifest` + Bureau Veritas rename to `cpsia_certificate` + Shenzhen-Newport image-transfer cross-border attribute family. Phase 3 (12-18 months): supplier-risk model under §10.21 + §10.24 entity-succession runbook. This engagement was fourth errata — the next consumer-products engagement starts inside the post-amendment spec.
