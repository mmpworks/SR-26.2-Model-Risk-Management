# Story 07 — Olmstead University (civil-rights threat-letter motivated higher-ed audit)

**Story file:** `docs/auditor-stories/07-olmstead-university.md`
**Engagement type:** Multi-framework higher-ed audit-readiness (FERPA + GLBA + NIH research-integrity + HHS OCR medical-center hallway-tour + civil-rights litigation defense addendum) anchored on a single chain-instrumented use case (undergraduate admissions screening AI).
**Posture going in:** AI-only chain — TesseraSeal deployed eleven months ago under a consent-to-resolve framework with a civil-rights firm; everything else legacy (Banner, Slate, IRB SQL, Salesforce advancement, faculty-led research labs, affiliated medical center).
**Outcome posture:** Confirmation on the AI side; gap-finding on the override-rationale free-text in Slate; five-regulator partitioning of the deliverable.

## Type of audit
Civil-rights-motivated AI audit against a multi-regulator stack — DOE FERPA (with an active OCR complaint), FTC GLBA Safeguards Rule, NIH research-integrity, HHS OCR HIPAA at the affiliated medical center, and a civil-rights litigation-defense addendum bridging FERPA and the override-rationale gap. Distinct because the chain was deployed in response to a disparate-impact threat letter naming override-down decisions for applicants whose AI score would have admitted them as the suspect class — the chain is the consent-to-resolve framework's principal defense, and the free-text rationale field one webhook away from the chain is the litigation exposure.

## Interested parties (spec readers)
- Department of Education OCR — Title VI / IX civil-rights enforcement; active FERPA complaint.
- Civil-rights firm investigator — disparate-impact / Title VI/VII; threat letter naming override-down decisions.
- General Counsel — Friday memo reader; legal-process and evidentiary readiness.
- Forensic accounting / litigation-support — discovery posture, FRE 902(13)/(14) certification.
- Cryptographic expert witness (Daubert) — admissibility for AI-side defense.
- Model Risk Management chair — admissions-AI lifecycle and ongoing monitoring.
- Chief AI / ML Officer — deployment-intent author; routing schema and underwriting-features-by-analogy.
- Chief Compliance Officer / CRO — multi-framework regulatory posture.
- Privacy Officer / DPO — FERPA `policy_id` / `policy_version` binding under MAC.
- FTC AI / privacy examiner — UDAP and AI-driven consumer harm; informative for higher-ed.
- HHS OCR examiner (HIPAA) — informal advisory at the affiliated medical center.
- State attorney general — state consumer-protection coordination.

## Top spec sections used
- **§1.2** — Epistemic scope: the chain proves what the AI screening system said and that the record was not tampered; it does not prove the admissions decision was right or that the override-rationale was the actual reasoning.
- **§4.4.6** — Slate webhook connector-source attribution (`audit.connector_source.*`) with stable-`run_id` discipline tied to the Slate applicant record ID — the structural form for the Phase 2 rationale-field webhook.
- **§7 + §10.12** — 12-step verifier procedure under `--posture=ffiec --strict` returning PASS in five seconds across all five reconciliation samples; pre-chain entries correctly REJECTED at step 1.
- **§10.11.1** — ECOA adverse-action reasons schema applied by analogy to the structured override decision — the chain-bound part of the disparate-impact defense.
- **§10.16** — Slate webhook four-number lag posture (median 4.2s, p95 SLO 30s, alert 60s, RTO 15min) compliant; severity-classification clause for imprecise wording.
- **§10.19** — Chain-coverage map naming Slate's free-text rationale field as outside the chain-instrumented boundary; map currently has a completeness gap that Phase 2 closes.
- **§10.20 + §10.21** — Training-pipeline integrity with M&A-G2 contract binding and external fairness-audit-vendor handover.
- **§10.22** — Pre-MAC SDK redaction with FERPA `policy_id`/`policy_version` bound under MAC.

## All cited spec sections
- **§1.1** — Daubert four-factor grounding for the litigation-defense memo.
- **§1.2** — Epistemic scope; controlled vocabulary for what the chain claims.
- **§1.3** — Security definitions (EUF-CMA per-event MAC; second-preimage Merkle; EUF-CMA HSM signature).
- **§1.4** — Compositional security across the three layers.
- **§3** — `tenant_id` keying; `chain_kind` enumeration.
- **§4.1** — Per-event HMAC; HKDF tenant binding; mid-write truncation refusal.
- **§4.1.2** — `--posture=ffiec` flag; `hkdf_inputs_digest` self-test.
- **§4.2** — Daily Merkle seal.
- **§4.3** — HSM-rooted root signature on AWS CloudHSM `us-east-2`.
- **§4.4** — OTLP envelope; `gen_ai.{request,response}.model` MUST; parent-linkage discipline.
- **§4.4.1** — Routing schema (single-provider; A/B forbidden by consent-to-resolve framework).
- **§4.4.2** — Deployment-intent (`production` posture; `policy_version` populated; CC8.1 names single-version single-region).
- **§4.4.5** — Underwriting-features-by-analogy (NAIC-P1) — feature_vector_hash, feature_categories, protected_class_proxy_flags emitted on every screening entry.
- **§4.4.6** — Slate webhook connector-source attribution; stable-`run_id` discipline.
- **§5** — Wire format; canonical-form exclusion rule.
- **§5.2** — Best-evidence posture (captured JSON content-bearing; canonical bytes integrity-bearing).
- **§6** — Storage; mid-write truncation refusal.
- **§7** — 12-step verification with witness-mode (no `--master-key`) PASS-STRUCTURALLY result.
- **§10.1** — Weekly key-fingerprint reconciliation (`unmatched_count = 0` across eleven months); medical-center tenant reserved.
- **§10.2** — Operational events (`credential.rotated`, `master_key.rotated`, `chain.coverage_map_published`).
- **§10.3** — Append-only enforcement (application + database-role layers); HMAC layer catches tamper at §7 step 9.
- **§10.4** — NTP discipline.
- **§10.5** — FIPS 140-2 Level 3 HSM custody on AWS CloudHSM.
- **§10.6 / §10.6.1** — 32-byte IKM; HSM-internal RNG (`master_key.generated` records `rng_source = "hsm.cloudhsm-classic"`).
- **§10.7** — Software-key adapter compile-time exclusion.
- **§10.8** — Constant-time comparison.
- **§10.9** — IKM-registry retention coupled to chain-entry retention.
- **§10.11** — ECOA translation entries for international applicants by analogy.
- **§10.11.1** — Adverse-action reasons schema bound under per-event MAC.
- **§10.12** — Verifier CLI exit-code contract (0 PASS, 1 FAIL, 2 structural error).
- **§10.13** — Evidentiary-artifacts retention list backing FRE 901(b)(9).
- **§10.16** — Slate webhook four-number lag bounds; severity-classification clause.
- **§10.17** — HSM partition-ceremony attestation; dual-signatures with `entity_affiliation` post-consolidation.
- **§10.18** — CC8.1 cross-referencing convention for runbooks.
- **§10.19** — Chain-coverage map; rationale-field map-completeness gap; lab enumeration; medical-center hash-anchor option via `audit.external_artifact.*`.
- **§10.20** — Training-data retention floor (540 days; 18-month deployment + 90-day investigation buffer).
- **§10.21** — Cross-vendor model-handover schema with M&A-G2 contract triple binding the fairness-audit vendor.
- **§10.22** — Redaction discipline pre-MAC at SDK boundary; FERPA policy_id/version bound under MAC.
- **§10.23** — Consumer-correlation index Shape 1 chain-anchored (student-ID derived).
- **§10.24** — Entity-succession framework forward-readiness.
- **§10.25** — Run-resume and chain-tail acquisition; DR rejoin posture.
- **§10.26** — Reference-verifier distribution; three-name CC8.1 citation.

## Synopsis

### Audit activity
The team began at the admissions-AI dashboard. A January 9 override (score 71 → 78, `STRENGTH_OF_RECOMMENDATIONS`) verified in five seconds; a February 2025 pre-chain decision correctly REJECTED at §7 step 1. Work split across four mutability profiles (admissions ledger / Banner / IRB / Salesforce), four-column IAM, the API and Slate webhook tail, the training pipeline (four hash-linked retrainings, all PASS), and a research-computing tour with two lab visits. Reconciliation sampled five admissions decisions: 5/5 AI PASS, 5/5 reviewer decision in chain, 3/5 rationale traceable, 2/5 rationale gone — both override-down decisions on applicants whose AI score would have admitted them. A medical-center hallway tour produced an informal HIPAA advisory mirroring prior healthcare findings.

### How the spec was used

- **§7 / §10.12** — 12-step procedure under `--posture=ffiec --strict` ran PASS for all five admissions decisions; exit-code contract gave structured signals; witness-mode (no `--master-key`) variant returned `PASS-STRUCTURALLY, key-bound verification skipped` for sampled entries — useful for federal litigation discovery.
- **§10.21** — M&A-G2 contract triple bound the external fairness-audit vendor's quarterly retraining.
- **§10.20** — 540-day retention floor exceeded the 18-month deployment plus 90-day buffer.
- **§4.4.6 / §10.16** — Governed the Slate webhook (compliant on the structured fields; the rationale free-text gap is upstream of capture, inside Slate).
- **§10.19** — Chain-coverage map became the partitioning tool for five regulator audiences; the rationale-field map-completeness gap is a separate finding from the underlying capture-coverage gap.
- **§1.2** — Epistemic scope is the framing that lets the litigation-defense memo distinguish what the chain proves (structured override decision and reason code) from what it does not (the free-text rationale at the moment of decision).

### Results
Five-regulator partition: FERPA — 0 Gaps on AI side, 1 Gap (override-rationale free-text not chained per §10.19), 1 Partial (Slate field-history retention). GLBA — 3 Gaps, 2 Partials (Banner 90-day audit retention, shared `aid_admin` peak-season account, paper access reviews). HIPAA — out-of-scope informal advisory mirroring prior healthcare audits. NIH — 1 Gap (no enforcement at lab level; one quantitative-finance lab does not meet expectations), 2 Partials. Civil-rights litigation defense — chain supports AI-side defense per §1.1/§1.2/§1.3/§1.4; override-rationale gap is the exposure to track. Phase 2 (12 months, funded) closes the rationale gap via §4.4.6 webhook + Slate retention extension + §10.19 map update + §10.18 CC8.1 cross-reference. Both gone-rationale cases were exactly the suspect class the threat letter named.
