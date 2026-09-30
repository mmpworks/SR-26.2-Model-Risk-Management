# Proposal &mdash; FFIEC AI Chain-of-Custody as a Candidate Standard for AI Audit-Trail Integrity in Regulated Banking

> **About this document.** This proposal is being prepared as the body of a comment-letter response to the **Office of the Comptroller of the Currency / Federal Reserve Board / Federal Deposit Insurance Corporation Request for Information on model risk management and banks' use of AI**, announced in the closing language of [SR 26-2 / OCC Bulletin 2026-13 / FDIC FIL](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) (April 17, 2026).
>
> **Status:** Skeleton populated against the most-likely RFI question categories. When the RFI publishes, the section structure below is reorganized to mirror the RFI's actual question set within 14 days and the body remains substantively the same.

---

## Executive summary

See [`executive-summary.md`](executive-summary.md). Recap: The FFIEC IT Examination Handbook already mandates that audit logs be tamper-evident, integrity-protected, immutable, and complete. The AIO booklet's §VII.D names AI risks but contains **no logging or audit-trail procedure for AI activity**. SR 26-2 / OCC 2026-13 (April 17, 2026) excludes generative and agentic AI from scope. The forthcoming RFI is the lane in which AI-specific guidance will develop. This proposal offers the **chain-of-custody primitive** as a candidate AI audit-trail integrity standard, suitable for adoption in a future FFIEC AIO booklet revision or a stand-alone AI examiner procedure.

## 1. The proposal

### 1.1 The four primitives

The chain of custody is built on four primitives, each language-neutral and vendor-neutral:

1. **HMAC chain at capture.** Every AI decision event is hashed at the moment of capture using a per-process session key derived via HKDF-SHA-256 from the institution's tenant-bound input key material. Each event includes the SHA-256 of the previous event in the same run. Tampering after capture is detected.

2. **Daily Merkle seal.** Events for each tenant per UTC calendar day are aggregated into an RFC 6962 Merkle tree with leaf prefix `0x00` and node prefix `0x01` for domain separation. The root is published in an append-only ledger. Retroactive insertion, deletion, or reordering of any event is detected.

3. **HSM-rooted root signature.** The daily Merkle root is signed in HSM custody (FIPS 140-2 Level 3 or higher) using Ed25519 (FIPS 186-5). The signing key is non-extractable.

4. **OpenTelemetry-native wire.** Events ship over OTLP using standard OpenTelemetry attributes plus the chain extension fields (`ffiec.chain.*`). Institutions that operate OTel-based observability today adopt the chain as an additional attribute namespace, not a parallel system.

The four primitives compose into a chain of custody an examiner can independently walk &mdash; with a single verifier binary, against the institution's exported chain artifacts, on the examiner's own laptop &mdash; **without trusting the institution's vendor or operations team**.

### 1.2 What the chain proves and does not prove

**The chain proves:**

- (a) **What the AI said at a specific time.** The captured event records the model's response, the prompt, the tools called, the routing decision, the operational state at capture.
- (b) **That the record was not tampered with after capture.** The verification procedure rejects any modification.

**The chain does not prove:**

- (c) **That the AI's statement is factually accurate.** The chain captures what was said, not whether it was true.
- (d) **That the AI's statement complied with policy.** Policy-compliance proof requires a separate audit trail.
- (e) **That the AI's statement is free of bias.** Bias proof requires statistical population testing.

This distinction is load-bearing under cross-examination, examination-finding language, and customer-dispute response.

### 1.3 Cryptographic foundation

The chain's cryptographic posture is built on NIST-standardized primitives with **explicit security definitions** (per spec §1.3):

| Primitive | Standard | Property |
|---|---|---|
| HMAC-SHA-256 | FIPS 198-1 / RFC 2104 | EUF-CMA security for per-event MAC |
| HKDF-SHA-256 | RFC 5869 | Approved key-derivation per NIST SP 800-56C §5.4 |
| RFC 6962 Merkle (over SHA-256) | RFC 6962 + FIPS 180-4 | Second-preimage resistance for daily seal |
| Ed25519 | FIPS 186-5 / RFC 8032 | EUF-CMA for HSM-rooted signature |
| RFC 8785 JCS | RFC 8785 | Canonical JSON for MAC input |
| FIPS 140-2 Level 3 | FIPS 140-2 | HSM custody for signing key |

**Effective security level: 128 bits.** Appropriate for FFIEC banking-regulation horizons (typically 7-year retention) under adversaries constrained by practical computation limits. A post-quantum migration trajectory is documented in the project's cryptographic-agility roadmap.

### 1.4 Daubert four-factor grounding

The chain is engineered to survive *Daubert* / FRE 702 challenge with concrete answers from shipped artifacts:

| *Daubert* factor | Chain answer |
|---|---|
| **Testability** | The §7 verification procedure is byte-exact and ordered; the test-vector corpus contains 10 positive and 23 negative vectors that any third party can reproduce. The integrity claim is falsifiable in the Popperian sense: produce a tampered chain that the procedure does not reject, and the claim breaks. |
| **Peer review** | The spec is developed under a working-group process with periodic outside-reviewer drops; the reference implementation and test-vector corpus are open-source under Apache-2.0. |
| **Known error rate** | A false-negative requires simultaneous compromise of three independent custody layers (tenant IKM in HSM/KMS, ledger storage, HSM signing key) plus the SDK-process compromise residual. Each layer is operated under separation-of-duties controls. |
| **General acceptance** | NIST-standardized primitives. Production deployments in adjacent industries (Certificate Transparency, Trillian, financial append-only ledgers) demonstrate general acceptance of the construction class. |

## 2. RFI question category responses

> The structure below anticipates the RFI's question set. When the RFI publishes, sections are reordered and renamed to match the actual question text; the substance below remains. Section numbers in **bold** point at the spec sections that supply the technical detail.

### 2.1 Risk identification and assessment for AI

**Question shape**: How should banking organizations identify and assess risks unique to AI-based models, particularly generative and agentic AI?

**The chain's contribution.** The chain captures the operational state at every AI decision (per **§4.1, §4.4**), making *post hoc* risk identification deterministic. Risk-assessment frameworks (NIST AI RMF, Treasury FS AI RMF) consume the chain's output as evidence rather than narrative.

For generative AI: the chain captures prompt, response, tool calls, routing decisions, and output filters with full integrity binding. Hallucination, prompt-injection, and jailbreak-attempt detection programs anchor on the chain entries.

For agentic AI: the chain captures the **autonomy boundary** of every decision (per **§4.4.1 routing**, **§4.4.5 underwriting features**, **§10.21 cross-vendor model handover**). Agent-to-agent handoffs and tool-call delegation are integrity-bound.

### 2.2 Governance and accountability frameworks

**Question shape**: What governance and accountability frameworks should apply to AI-based models?

**The chain's contribution.** Chain-coverage boundary documentation per **§10.19** names what is in chain coverage versus what remains on legacy logging. This is the institution's AI-inventory substrate.

CC8.1 control description per **§10.18** is the change-management discipline for chain-affecting changes. Vendor-conformance attestation registry (per project [`GOVERNANCE.md`](../GOVERNANCE.md)) is the third-party-governance substrate.

The chain's open-source posture under Apache-2.0 with explicit foundation-transfer trajectory (OpenSSF, CNCF, or banking consortium) is responsive to accountability and durability concerns the agencies raised in 2024 Treasury feedback.

### 2.3 Validation and testing

**Question shape**: What validation and testing practices should apply to AI-based models, and how should they differ from traditional model risk management?

**The chain's contribution.** The chain provides the **evidence substrate** for validation programs, not the validation methodology itself. The institution's validation program supplies the methodology; the chain supplies the validation activity's chain entries with integrity binding.

Specific touchpoints:

- **Disparate-impact testing** &mdash; **§4.4.5 `audit.disparate_impact.*`** captures testing runs.
- **Champion / challenger testing** &mdash; **§4.4.2 deployment intent** captures swap events.
- **Regulatory sandbox testing** &mdash; **§4.4.2** captures sandbox flags.
- **Pre-deployment testing per NIST AI RMF GAI-PWG** &mdash; chain captures the testing-environment chain entries; test vectors `008-jcs-edge-cases` are the canonicalization-edge-case anchor.

### 2.4 Ongoing monitoring

**Question shape**: How should ongoing monitoring of AI-based models be structured?

**The chain's contribution.** Daily verifier runs are the post-deployment monitoring substrate. The verifier output is PASS / FAIL with named failure modes per **§10.12**. Chain-anomaly detection (verifier exit code 3) feeds the institution's IR program per [`incident-response-playbook.md`](../docs/incident-response-playbook.md).

For drift detection, the institution's monitoring program consumes the chain's `audit.disparate_impact.*` and `audit.deployment.intent` entries to detect statistical drift over time. The drift detection methodology is the institution's; the integrity-bound input data is the chain's.

### 2.5 Audit-trail integrity and documentation

**Question shape**: What audit-trail integrity and documentation practices should apply to AI-based models? **(This is the chain's primary contribution.)**

**The chain's contribution.** This question is the chain's *raison d'&ecirc;tre*. The chain delivers:

- **Tamper-evidence** at three independent layers (per-event MAC, daily Merkle seal, HSM-rooted signature).
- **Independent verifiability** via the §7 verification procedure and the open-source verifier.
- **Cross-bank comparability** &mdash; two conforming implementations produce byte-identical chain artifacts for the same logical event, enabling supervisory portfolio analysis.
- **Best-evidence posture** under FRE 1001-1004 per **§5.2**.
- **Selective production** for partial-disclosure scenarios via Merkle inclusion proofs (test vector `017`).

This category is where the chain's adoption value to the FFIEC and member agencies is highest.

### 2.6 Vendor and third-party risk

**Question shape**: How should vendor and third-party AI risks be managed?

**The chain's contribution.** The chain **deliberately neutralizes the vendor as a single point of trust**:

- The institution's IKM is held in institution-controlled HSM/KMS custody, never vendor custody.
- The verifier runs without coordination from the vendor, on the examiner's laptop, against the institution's exported artifacts.
- Cross-vendor anchor patterns per **§10.21** allow institutions to cross-link two vendors' chains in vendor-mix scenarios.
- Vendor-conformance attestation registry per [`GOVERNANCE.md`](../GOVERNANCE.md) is the project-side trust mechanism complementing vendor SOC reporting.

The auditor stories include four cross-vendor and multi-jurisdiction examples (Atrio, NetiVa, Eberhardt &times; Lumi&egrave;re, Sun-Won) demonstrating the discipline at scale.

### 2.7 Consumer protection (ECOA, FCRA, fair-lending)

**Question shape**: How should consumer-protection requirements interact with AI-based decisioning?

**The chain's contribution.**

- **§10.11 ECOA / state-insurance adverse-action translation discipline** &mdash; the chain captures the translation from model-internal reasoning to consumer-facing reasons with integrity binding.
- **§10.11.1 ECOA adverse-action reasons schema** (`audit.ecoa.adverse_action.*`).
- **§10.11.2 FCRA §611 reinvestigation timing** (`audit.fcra.reinvestigation.*` &mdash; 30-day clock, 45-day extension under §611(a)(3)).
- **§10.23 consumer-correlation index integrity** &mdash; CID-class production via Shape 1 (chain-anchored) or Shape 2 (daily attestation).
- **§10.22 redaction discipline** &mdash; for DSAR / customer-rights production while preserving partial-disclosure integrity.

These touchpoints are deliberately developed for CFPB and state-DOI examination posture and are exercised in the auditor-stories Olmstead and Pacific Crescent narratives.

### 2.8 Data integrity (training and inference)

**Question shape**: How should data integrity be assured at the training and inference phases?

**The chain's contribution and explicit scope boundary.**

- **Inference-phase integrity** &mdash; IN scope. The chain captures every inference-phase decision with full integrity binding.
- **Training-phase integrity** &mdash; OUT of scope for v1.x. Per the spec's §1 scope boundary, training-data integrity, training-pipeline reproducibility, and training-data labeling are not covered. Institutions operating training-phase integrity controls do so under separate evidence regimes; the chain composes alongside without overlap.

This boundary is intentional. The forward commitment in the spec (§1) names training-phase integrity as a candidate scope expansion for v2.x. The proposal asks the agencies to consider the appropriate forum (FFIEC working group, NIST AI RMF profile, sister-agency guidance) for the training-phase integrity question over the next 12-24 months.

### 2.9 Generative AI specific risks

**Question shape**: What unique risks does generative AI pose, and how should they be managed?

**The chain's contribution.** The chain captures generative-AI-specific events with integrity binding:

- **Prompt injection / jailbreak attempt detection** &mdash; the captured prompt is integrity-bound; the post-hoc analysis can identify injection patterns deterministically.
- **Hallucination claims and corrections** &mdash; the chain entry for the original response and the chain entry for any correction or retraction are both bound to the run.
- **Output filtering events** &mdash; chain entries for filter activations.
- **Multi-modal capture** &mdash; the chain accommodates multi-modal input/output through OpenTelemetry GenAI semantic conventions (referenced in **§4.4**).

Generative-AI risk-management frameworks (NIST AI RMF Generative Profile, Treasury FS AI RMF generative-AI considerations) consume the chain's output as their evidence substrate.

### 2.10 Agentic AI specific risks

**Question shape**: What unique risks does agentic AI pose, and how should they be managed?

**The chain's contribution.** Agentic AI risks center on **autonomy** &mdash; the agent's tool calls, sub-agent delegation, and decision authority. The chain captures all three:

- **Tool calls** &mdash; every tool call is a chain entry (`tool_call` chain-kind per §3).
- **Sub-agent delegation** &mdash; cross-run chain isolation per **§4.1** preserves the autonomy boundary of each sub-agent's run.
- **Routing decisions** &mdash; **§4.4.1** captures routing classifications with integrity binding.
- **Operational state** &mdash; the agent's authority level, override eligibility, and human-in-the-loop status at decision time are captured.

Agentic-AI risk-management requires the chain's integrity binding to make autonomy boundaries auditable in retrospect.

### 2.11 Cybersecurity risks

**Question shape**: What cybersecurity risks does AI introduce, and how should they be addressed?

**The chain's contribution.**

- **Supply-chain integrity** &mdash; **§10.26** reference verifier distribution discipline (Apache 2.0, reproducible builds, signed release artifacts, SBOM, SHA-256/SHA-512 manifests, spec-version pinning).
- **Threat-model coverage** &mdash; per **§1.1, §1.2** and [`docs/design/09-threat-model.md`](../docs/design/09-threat-model.md), the chain defends against rogue-ops-engineer, rogue-vendor, and (most of) regulator-coordinated-nation-state adversaries with named residuals.
- **Cybersecurity Specialist Examiner alignment** &mdash; per [`docs/regulator-pack/CSF-2.0.md`](../docs/regulator-pack/CSF-2.0.md), the chain maps to NIST CSF 2.0 across all six functions.

### 2.12 Operational resilience

**Question shape**: How should operational resilience be assured for AI-based systems?

**The chain's contribution.**

- **DR/RPO/RTO posture** &mdash; per [`docs/dr-and-resilience.md`](../docs/dr-and-resilience.md).
- **Run-resume / chain-tail acquisition** &mdash; **§10.25** captures DR-rejoin events with integrity binding.
- **Multi-region resilience** &mdash; **§10.15** normates the integrity invariants for multi-region deployments.
- **At-scale operational guidance** &mdash; per [`docs/at-scale-operations.md`](../docs/at-scale-operations.md) for high-volume institutions.
- **EU DORA articulation** &mdash; per [`docs/regulator-pack/dora-articulation-overlay.md`](../docs/regulator-pack/dora-articulation-overlay.md) for EU-jurisdictional institutions.

### 2.13 Explainability and transparency

**Question shape**: How should explainability and transparency requirements apply to AI-based decisioning?

**The chain's contribution.** The chain captures **what the AI said** at full fidelity. Explainability methodologies (LIME, SHAP, gradient attribution, counterfactual generation) are applied to the chain entries; the methodologies are not in spec scope.

For consumer-facing explainability:

- **§10.11 adverse-action translation discipline** &mdash; the model's reasoning is translated to consumer-facing reasons with integrity binding to the original reasoning.
- **§4.4.5 underwriting-feature recording** &mdash; the feature set used in each decision is captured.
- **§10.13 evidentiary artifacts** &mdash; the evidence framework for transparency-related disclosures.

### 2.14 Workforce and human-in-the-loop

**Question shape**: How should the human-in-the-loop posture be maintained for AI-based decisioning?

**The chain's contribution.** Override and human-in-the-loop events are chain entries:

- **§4.4.1 `audit.routing.classifier_output`** &mdash; the routing decision that determined whether human review was required.
- **§4.4.2 deployment intent** &mdash; champion/challenger and regulatory_sandbox flags that affect human-review triggers.
- **`audit.deployment.intent` family** &mdash; override-eligibility status at decision time.

Human-review chain entries are produced by the institution's review system (typically a separate chain-aware integration); the chain binds the review activity to the decision activity.

## 3. Recommended next steps

The proposal asks the agencies to:

1. **Recognize** PRD-2 as a candidate audit-trail integrity standard for AI in regulated banking.
2. **Cite** the chain-of-custody primitive in the AI RFI's response synthesis as one of the candidate solutions on the table.
3. **Pilot** the verifier on a volunteer institution to evaluate examiner-laptop deployment per [`docs/regulator-pack/deployment-package.md`](../docs/regulator-pack/deployment-package.md).
4. **Reference** the chain-of-custody primitive in:
   - The next FFIEC IT Examination Handbook AIO booklet revision (the §VII.D AI section).
   - Or, in the interim, a sister-agency advisory specific to AI audit-trail integrity.
5. **Coordinate** with NIST on the AI RMF Critical Infrastructure Profile (concept note dropped April 7, 2026) to align the chain primitive with the financial-sector profile when issued.
6. **Coordinate** with Treasury on the FS AI RMF v2 cycle to align the 230 control objectives with the chain's coverage.

## 4. Open working-group questions

The project's spec-editor team requests the agencies' working-group guidance on:

1. **Where in the FFIEC IT Examination Handbook should the chain primitive most naturally land?** Information Security booklet (extending existing audit-log requirements)? AIO booklet §VII.D (extending the AI section)? A new dedicated AI booklet (parallel to the AIO and Information Security booklets)?
2. **Is HSM custody at FIPS 140-2 Level 3 the appropriate floor**, or should systemically important institutions be expected to operate at Level 4?
3. **What retention horizon should examination procedures expect** for chain artifacts? The spec is retention-agnostic; institutional regulatory frameworks set the duration. Is FFIEC-side guidance on the floor warranted?
4. **Should training-phase integrity be expanded into v2.x** as part of an FFIEC-coordinated working group, or is the question better routed to NIST AI RMF or sister agencies (CFPB on training-data labeling, OCC on training-data integrity)?
5. **Cross-vendor anchor pattern adequacy** &mdash; does **§10.21** cover the vendor-mix scenarios examiners typically encounter?

## 5. Conclusion

The chain-of-custody primitive is offered as an open-source candidate standard, designed for the FFIEC's regulatory horizon and engineered for examiner-laptop deployment without vendor coordination. The four primitives are language-neutral, vendor-neutral, jurisdiction-neutral at the wire-format level, and survive *Daubert* under cross-examination with shipped-artifact answers.

The agencies have an audit-trail integrity gap in §VII.D of the AIO booklet and in the SR 26-2 / OCC 2026-13 framework's exclusion of generative and agentic AI. The chain closes that gap.

The project's posture is **transparent, open-source, and foundation-transfer-bound**. **Conflict-of-interest disclosure.** The author, Steve Muchow, is the founder of MMPWorks LLC, which develops commercial software that implements this specification, including TesseraSeal and Herald.Compliance. The specification, the conformance test vectors and the reference verifier are licensed under Apache-2.0, and conformance does not require any MMPWorks product. The submission stands or falls on the merit of the specification.

---

## Appendices

- [Appendix A &mdash; FFIEC handbook mapping](appendices/handbook-mapping.md)
- [Appendix B &mdash; Control overlay (NIST CSF 2.0 / FS AI RMF / SR 26-2)](appendices/control-overlay.md)
- [Appendix C &mdash; Conformance test-vector corpus summary](appendices/test-vectors-summary.md)
- [Specification PRD-2 (`spec/chain-of-custody-DRAFT-0.2.0.md`)](../spec/chain-of-custody-DRAFT-0.2.0.md) &mdash; attached as a separate PDF in the submission package.
