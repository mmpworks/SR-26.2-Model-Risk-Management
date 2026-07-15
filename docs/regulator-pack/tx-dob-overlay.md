# Texas Department of Banking (TX DOB) supervisor overlay

**Scope.** Companion overlay for the Texas Department of Banking (TDoB / "the Department") and Texas-chartered banks, trust companies, and money-services-business licensees adopting the chain-of-custody specification. Maps spec sections to the Texas Finance Code, Title 7 of the Texas Administrative Code, the TDoB examination framework, and the federal-agency overlays TDoB coordinates with. TDoB participates in the CSBS Nationwide Cooperative Agreement (NCA) and examines inside the FDIC / Federal Reserve cooperative program, so most day-to-day examination mechanics are FFIEC-interagency procedure that Texas adopts by reference; the Texas-specific layer (Finance Code authority, four regional offices, the 15-day state cybersecurity-incident rule, joint-enforcement mechanics) sits on top.

**Status.** Full overlay — published 2026-07-15 (PRD-3.2). Mirrors the NYDFS Part 500 overlay's depth for Texas-chartered institutions.

**How to read this overlay.** The spec's cryptographic substrate is authority-neutral (see §1 applicable-agencies, "a regulator not named above applies the chain under its own supervisory mandate without spec-amendment"). A Texas state-chartered bank produces a chain that is byte-identical in construction to a national bank's; TDoB runs the same §10.26 reference verifier and reads the same Verdict-Object. Nothing in this overlay changes the wire form or the verifier's integrity procedure. The overlay maps the Texas supervisory context onto the substrate and names the Texas-specific provenance the PRD-3.2 additions capture.

---

## 1. Texas supervisory framework

TDoB's Bank & Trust Division supervises approximately 200 state-chartered commercial banks, ~30 state-chartered trust companies, foreign bank organizations, and a substantial money-services-business (MSB) population. Texas-chartered banks are **dual-supervised**: TDoB on the state side plus a federal prudential supervisor — the **FDIC** for state-nonmember banks, the **Federal Reserve** (via the Dallas Fed) for state-member banks.

- **Texas Finance Code, Title 3** — the substantive Texas banking statute. Chapter 31 covers commercial banks (including the Subchapter B closure / conservatorship / liquidation authority); Chapter 35 covers trust companies; Chapter 37 covers state savings institutions; Chapters 151-152 cover money services businesses. The chain's safety-and-soundness anchor (§1.1 Daubert grounding, §10.5 HSM custody, §10.10 master-key rotation, §10.13 evidentiary artifacts) composes with Title 3's safety-and-soundness mandate.
- **Texas Finance Code §59.006 — customer-financial-record privacy** — the Texas analog to the federal Right to Financial Privacy Act (12 USC §3401 et seq.). Composes with the chain's §10.22 redaction discipline and §10.69 customer-disclosure subprocedure.
- **Texas Business and Commerce Code Chapter 521 — Identity Theft Enforcement and Protection Act.** Composes with §10.13.3 litigation-hold registry and §10.70 privileged-investigation overlay when investigations involve law-enforcement coordination.
- **Texas Government Code Chapter 552 — Texas Public Information Act (PIA).** Applies to TDoB's own examination records. The §10.72 FOIA-and-state-sunshine release table pins Texas PIA at the 10-business-day clock under §552.221.
- **Title 7 Texas Administrative Code, Part 2 (Department of Banking)** — the state rule layer. **7 TAC Chapter 3** covers examination procedures, supervisory enforcement, and chartered-bank operational requirements; supervisory memoranda (e.g., SM 1005, SM 1043) add Texas-specific expectations on top of FFIEC.
- **TDoB Examination Manual** — aligns with the FFIEC IT Examination Handbook and the FDIC Risk Management Manual of Examination Policies. The chain's FFIEC-aligned §10.x compositional path applies directly.

**CSBS accreditation is the examiner-quality trust substrate — and it is orthogonal to the chain's integrity trust anchor.** TDoB holds continuous CSBS accreditation (seventh consecutive reaccreditation, January 2025). Accreditation is why an alternate-year TDoB examination "counts" for federal purposes — staff quality, training, and tooling are certified comparable to federal counterparts. Note the two trust layers do not overlap and do not substitute for each other:

- **CSBS accreditation** certifies the *examiner's* competence, so a state exam report is interchangeable with a federal one.
- **The chain (§10.76 trust anchor)** certifies the *institution's evidence integrity*, rooted in the institution's HSM-signed IKM-registry manifest.

A verifiable chain reinforces exactly the "comparable to federal counterparts" bar accreditation depends on — it raises the verifiability of the workpapers the state exam rests on — but the chain does not depend on accreditation and accreditation does not depend on the chain.

**Regional footprint.** Headquarters is in Austin (the Banking Commissioner's seat). Field examiners deploy from four regional offices: **San Antonio, Houston, Arlington, and Lubbock**. A Texas exam team may be TDoB-only (alternating years) or a joint TDoB + FDIC / Dallas-Fed team.

---

## 2. The core trust question: "the bank signs its own evidence"

A skeptical CSBS reviewer or a hostile examiner raises this objection first, so the overlay answers it head-on. The chain's trust anchor (§10.76) is the *institution's* HSM signing key — the bank signs its own evidence. On its face that looks like "the bank marking its own homework with a fancier pen." It is not, and the reasons are mechanical, not rhetorical:

1. **Tamper-evidence, not self-attestation.** The chain does not claim the bank is honest. It claims that any alteration of a captured record *after capture* is detectable (§1.2(b)). A bank that captures a decision and later wants to change it cannot do so without producing a §7 verification failure, which is itself a Severe control-failure finding. The examiner does not have to trust the bank's good faith; the examiner runs the verifier.
2. **Three independent custody layers (§1.1, §1.4).** Producing a *verifying* forgery requires simultaneously compromising the tenant IKM (in HSM/KMS custody), the append-only ledger storage, and the HSM signing key (FIPS 140-2 Level 3) — three layers operated by different roles under separation-of-duties controls (§10.5). Compromise of any one alone surfaces as a named §7 failure.
3. **The signing key is not freely wielded.** §10.5 HSM custody + separation of duties mean the seal job, not an individual, signs the daily root; the private key is non-extractable. "The bank signed it" means "the bank's HSM seal job, under dual control, signed the daily Merkle root," not "an employee signed whatever they liked."
4. **The trust anchor is published and reconciled.** §10.76 requires the institution to publish an HSM-signed IKM-registry manifest the examiner validates at verifier startup; §10.1 fingerprint reconciliation catches a substituted IKM before any MAC is computed. An examiner who fetches the manifest from the institution's CC8.1-named endpoint and validates its signature has independent assurance of which keys are in play.

**What the chain does and does not prove for an examiner.** It proves what the institution's system recorded at a moment and that the record was not altered afterward (§1.2(a)/(b)). It does not prove the recorded decision was correct, compliant, or unbiased (§1.2(c)/(d)/(e)) — those remain the examiner's substantive review. The chain is the integrity foundation, not the truth foundation. Stating this boundary plainly is what keeps the institution's witness credible under cross-examination and keeps the examiner from over-relying on a PASS.

---

## 3. Examination integration

TDoB examination cycles are typically 12 months, extendable to 18 for eligible well-capitalized, well-managed institutions with a strong CAMELS composite below the asset threshold; larger institutions follow the federal schedule. The chain integrates at:

1. **IT examination (InTREx / FFIEC IT Handbook).** TDoB IT examiners apply the FFIEC IT Examination Handbook and the FDIC **InTREx** (Information Technology Risk Examination) program, and issue a **URSIT** rating (1-5 across Audit, Management, Development & Acquisition, and Support & Delivery; the URSIT composite feeds the CAMELS **Management** and **Sensitivity** components). Roughly 90 days before an IT exam the bank receives an **Information Technology Profile (ITP)** questionnaire through FDICconnect that scopes the exam. The chain's §10.x operational requirements + §7 verifier output satisfy the IT-Audit booklet's audit-evidence expectations; chain-bound institutions provide the verifier output as the audit-evidence artifact and TDoB IT examiners re-verify independently using the §10.26 reference verifier. InTREx core-module compliance with Appendix B to Part 364 (Interagency Guidelines Establishing Information Security Standards) maps to the chain's §10.5 / §10.77 hardening disciplines.

2. **Cybersecurity assessment (moving target).** The FFIEC retired the Cybersecurity Assessment Tool on 2025-08-31 and pointed institutions to the NIST Cybersecurity Framework 2.0; the chain's control mappings live in `CSF-2.0.md`. Institutions are expected to have a documented information-security program, a written incident-response plan, and tested cybersecurity preparedness — all surfaces the chain's operational-events discipline (§10.2) and sibling-log binding (§10.79) support.

3. **BSA/AML examination.** TDoB examiners assess BSA/AML compliance under 31 CFR Part 1020. The chain's §10.70 BSA SAR / privileged-investigation overlay provides the integrity-bound posture; SAR-clock binding under `audit.bsa.sar.*` and CTR-clock binding under `audit.bsa.ctr.*` give examiners chain-bound timeline reconstruction without consulting BSA-officer records. Note BSA records carry a **5-year** retention expectation — see §6 below for the IKM-retention implication.

4. **Trust-company examination (Chapter 35).** Trust-administration AI, beneficiary-advice AI, and fiduciary-decision AI are model-risk-relevant per SR 11-7 the same way commercial-bank AI is; §10.33 MRM disposition applies identically. §10.69's estate / fiduciary disclosure procedure is particularly relevant given the routine fiduciary-relationship context.

5. **Money-services-business examination (Chapters 151-152).** AI-driven MSB decisions (sanctions screening, fraud detection, transaction monitoring) bring the chain via §10.70 BSA SAR / OFAC-investigation regime values; cross-border-MSB activity composes with §4.4.1 cross-border transfer attributes. The parallel state cyber-incident rule for MSBs is **7 TAC §33.30**.

---

## 4. Texas 15-day cybersecurity-incident notice (7 TAC §3.24)

This is the most distinctly-Texas evidence obligation. A Texas state bank must **notify the Banking Commissioner as soon as practicable, before customer notification, and no later than 15 days** after determining that a reportable cybersecurity incident occurred; the duty must be written into the bank's incident-response plan inside its information-security program. A bank may submit the **same computer-security incident notice it files with federal regulators** (the interagency 36-hour rule) to satisfy the state notice.

The chain maps this cleanly:

- **The incident notice is a `chain_kind = "operational"` §10.2 event.** The event binds the determination moment and the notice moment. Two clocks matter: the 15-day cap from determination, and the "before customer notification" ordering.
- **The "before customer notification" ordering is chain-provable** using the §10.84 preapproval-ordering primitive: the regulator-notice event and the customer-notice event are parent-linked, and the verifier confirms `regulator_notice.applied_at_utc ≤ customer_notice.applied_at_utc` the same way §10.84 confirms approval-precedes-send. An out-of-order pair surfaces as a control-completeness anomaly under `Status: PASS`, not a chain-integrity FAIL.
- **The federal-notice-satisfies-state composition** is recorded by binding the interagency 36-hour notice artifact's hash into the operational event; the same artifact satisfies both regimes.

**Honesty boundary (per §1.2).** The chain proves the institution *recorded* a determination at time T and did not alter that record afterward. It does not independently prove the institution actually determined at time T — a back-dated determination is faithfully recorded as the institution asserts it. The ordering property ("before customer notification") is genuinely chain-proven because it is a relationship between two chain-bound events; the determination *timestamp* is institution-asserted. The examiner reads the ordering as hard evidence and treats the determination moment as an attestation the SOC engagement tests.

---

## 5. Evidence and artifact mapping

**The gap the chain fills.** Bank-exam practice today has **no cryptographic chain-of-custody**: evidence authenticity rests on bank attestation + examiner reconciliation + secure-portal transport + confidentiality. The one explicit integrity duty is the Call Report electronic-signature rule — the artifact must be "safely stored, readily retrievable, and cannot be lost or altered" — but it is framed as an aspirational control on the bank, with no independent verification. The chain turns that aspiration into a verifiable property.

**Format-agnostic artifact binding.** Only Call Reports (FFIEC 051 and family) are format-rigid; everything else is native bank documents (PDF, spreadsheet, core-system extract). The chain binds arbitrary artifacts by hash — the `audit.external_artifact.*` pattern (Appendix A.14) binds the artifact's bytes without prescribing the artifact's format. For a prescribed-format artifact (Call Report), the hash binds the prescribed bytes; for a native artifact (board minutes PDF), the hash binds whatever the bank produced. Either way the examiner gets "this is the file the bank gave us, and it has not changed" — the question reconciliation alone cannot answer.

**Reconciliation and the chain are complements, not substitutes.** Examiners establish reliability by reconciling artifacts to authoritative sources (loans → loan trial balance, balances → general ledger). Reconciliation proves internal consistency; the chain proves tamper-evidence and provenance. An examiner uses both: reconciliation for "do the numbers tie," the chain for "is this the untampered file the bank produced."

**Recommended exam-artifact-kind vocabulary.** The exam artifact set is stable and enumerable: board and committee minutes, loan files, Call Reports, general-ledger extracts, policies (loan / investment / information-security / incident-response / BSA-AML), loan and asset data downloads, and BSA records (transaction records, SAR/CTR support). Institutions binding these under the chain SHOULD use a **shared** `audit.exam_artifact.artifact_kind` vocabulary rather than purely institution-named values, so evidence is comparable across the ~200 Texas banks and across CSBS multistate examinations. The recommended values:

| `artifact_kind` | Exam artifact | Typical review |
|---|---|---|
| `board_minutes` | Board and committee minutes | Governance, approvals, management oversight |
| `loan_file` | Notes, credit memos, appraisals, collateral, LTV support | Asset-quality review |
| `call_report` | Consolidated Reports of Condition and Income (FFIEC 051 etc.) | The one prescribed-format artifact; the e-signature integrity duty |
| `gl_extract` | General-ledger extracts | Reconciliation baseline |
| `policy` | Loan / investment / infosec / IR / BSA-AML policies | Control-framework review |
| `loan_asset_download` | Loan/asset data downloads for off-site pre-analysis | Risk-focused pre-work |
| `bsa_record` | Transaction records, SAR/CTR support | BSA/AML review (5-year retention) |

The vocabulary is a recommendation, not a closed spec enumeration — the `chain_kind` closed enum (§3) stays intact for wire byte-identity; `artifact_kind` is an `audit.*`-namespace institution-named value with a recommended shared registry for portability. TDoB names its adopted vocabulary in the institution CC8.1.

**Supervisory-context provenance.** The PRD-3.2 `audit.supervisory.*` family (§14.13) records the charter and supervision context on decision entries: for a Texas state-nonmember bank, `charter_type = "state_bank"`, `primary_state_supervisor = "tx_dob"`, `federal_prudential_supervisor = "fdic"`, `dual_supervision = true` (a state-member bank sets `federal_prudential_supervisor = "frb"`). An examiner reconstructs which authority governed a decision from the entry alone. The family is integrity-bound but institution-asserted (§1.2) — the SOC engagement confirms the asserted context against the charter documents.

---

## 6. Retention and custody

**Retention windows (federal-standard, Texas adopts):**

- Examiner workpapers: **2 years or until the next examination, whichever is later**.
- Call Reports and their supporting workpapers: **3 years** after report date (longer if state law requires).
- BSA records: generally **5 years**.

**IKM-registry retention must outlive the longest evidence window.** Verifying an old chain entry requires the IKM generation that signed it (§7 step 7 IKM lookup). If the institution rotates and retires IKMs (§10.10) on a cycle shorter than the longest evidence-retention window, old evidence silently becomes unverifiable — the verifier returns `unknown key_version: no IKM for (tenant=T, key_version=V)`. The institution's CC8.1 MUST bind IKM-registry retention (§10.9) to **at least the longest applicable evidence-retention window** — with BSA records at 5 years, that is a **5-year-plus** IKM-registry floor for a bank with BSA-bound chain entries. Retired IKMs are retained (not destroyed) for the verification horizon; §10.9 already permits this, and this overlay makes the binding explicit for the Texas retention set.

**Custody boundary — institution-side vs. examiner-side.** The chain covers the **institution's** evidence (the bank is the tenant). It does not cover the **examiner's** work product: the Report of Examination (ROE), examiner workpapers, and the CAMELS/URSIT ratings are examiner-side confidential supervisory information, held under examiner-side custody (on the FDIC side, backed up to the ETS Archive Library and wiped from examiner laptops at exam close). That custody is procedural, outside the bank's chain by design. Do not over-claim: a chain PASS attests to the bank's evidence integrity, not to the examiner's workpaper handling.

**Confidentiality.** The ROE and supporting evidence are confidential supervisory information — access-controlled, not public. The chain preserves confidentiality through access-controlled disclosure keys (§10.69 / §10.70), not public release. Texas PIA (Gov't Code §552) governs TDoB's own records and is mapped in the §10.72 state-sunshine clock table (10-business-day, §552.221); a bank whose examination records are subject to a PIA request operates the §10.72 release subprocedure with the FOIA-exemption redaction discipline of §10.70.

**Examiner-access provenance.** When an examiner pulls confidential evidence through a portal (see §7), that access can itself be chain-bound using the §10.70 access-trail discipline the spec already normates for privileged-investigation reads — producing "which examiner accessed which evidence when" as a chain-bound trail rather than a purely procedural one. This is optional and institution-elected; it raises the verifiability of the access record the way the chain raises the verifiability of the evidence.

---

## 7. Transport and portals

Bank-exam transport is already portal-based and access-controlled — the chain has natural integration points at upload, association-to-request, and archive:

- **FDICconnect** — the secure FDIC↔bank portal (state-nonmember banks), with secure file exchange.
- **Banker Engagement Site (BES)** — launched September 2023 through FDICconnect; banks respond to specific information/document requests, associate responses with requests, ask the exam team questions, and manage user roles. The §10.13.1 discovery-production form is the integrity-bound packet shape delivered through BES; the packet's manifest SHA-256 lets both a state and a federal examiner verify the same production independently.
- **Examination Tools Suite (ETS)** — examiner-side; asset/loan data is archived to the ETS Archive Library and wiped from examiner laptops at exam close.
- **Federal Reserve secure channels** — for state-member banks, in place of FDICconnect.

TDoB rides the federal portals in joint exams and uses secure electronic exchange for its own. The chain artifacts (seal records, verifier output, evidentiary artifacts) are transport-agnostic (§4 topology, §5.1 discovery-endpoint transport floor); the portal is the delivery channel, and the chain is the integrity layer riding it.

---

## 8. TDoB / federal-supervisor coordination

State-chartered Texas banks have a federal prudential supervisor (FDIC or FRB). The chain integrates with the cooperative program at:

- **Alternating-examination cycle.** TDoB and the federal supervisor typically alternate primary-examination years, each able to examine independently subject to notifying the other. Chain artifacts are jurisdictionally portable; both supervisors consume the same chain at their respective cycles. The institution's CC8.1 names the supervisory-coordination framework; the `audit.supervisory.*` family (§14.13) records which authority governed which decision.
- **Joint examinations.** High-risk or large-institution scenarios produce joint TDoB + federal-supervisor teams. The chain's verifier output is single-source-of-truth; both supervisors reach the same Verdict-Object via the §7 deterministic procedure. Cross-supervisor disputes about "what did the chain say" reduce to a re-run of the verifier.
- **Shared evidence vault.** Under the CSBS NCA framework, the §10.13.1 discovery-production form is the integrity-bound delivery surface; both supervisors verify the production manifest's SHA-256 independently.

---

## 9. Enforcement

TDoB deficiencies escalate along an informal→formal ladder; the chain's verifier output and §10.13 evidentiary-artifact list are the citation surface at every rung:

- **Informal (voluntary):** Board Resolutions, Memorandum of Understanding (MOU) between the bank and the Commissioner, and Determination Letters.
- **Formal:** an order issued by the Banking Commissioner, up to a Cease-and-Desist / Consent Order. TDoB joins a federal agency in a **joint** C&D or Consent Order only after making the findings required by **TFC §35.012**.

The §10.13 evidentiary-artifacts list is jurisdictionally portable — the same Verdict-Object cited in a federal Supervisory Letter or MRA grounds a TDoB MOU or Commissioner's order. When enforcement escalates to conservatorship or receivership under the Commissioner's Texas Finance Code Title 3 authority, the succession event carries `kind = "tx_dob_conservatorship"` per §10.83's state-authority conservatorship posture, and (for a dual-supervised bank) both authorities appear in the succession `signatories` array.

---

## 10. Examiner reading path

1. **IT examination (TDoB IT examiner).** §1, §1.1, §4, §7, §10.12 (verifier exit codes), §10.13 (evidentiary artifacts), §14.13 (supervisory-context provenance), and §2 above (the "bank signs its own evidence" trust discussion). The verifier output grounds TDoB findings the way it grounds FFIEC IT Examiner findings.
2. **BSA/AML examiner.** §10.70 BSA SAR / privileged-investigation overlay, §10.13.3 litigation-hold registry, §10.69 customer-disclosure, and §6 above (the 5-year IKM-retention floor).
3. **Trust-company examiner.** §10.33 MRM disposition, §10.69 estate / fiduciary disclosure, §10.74 deletion-request schema.
4. **MSB examiner.** §10.70 BSA SAR / OFAC-investigation regimes, §4.4.1 cross-border transfer, §10.71 cross-institution Fedwire / ACH, and 7 TAC §33.30 for the MSB cyber-incident rule.
5. **Cybersecurity / incident.** §4 above (7 TAC §3.24 15-day clock), §10.2 operational events, §10.84 ordering primitive, `CSF-2.0.md`.
6. **Enforcement attorney.** §10.13 evidentiary artifacts, §10.13.1 discovery production form, §10.13.2 FRCP framing (Texas-state-court parallels), §10.26 verifier distribution, §9 above (the enforcement ladder + TFC §35.012).

---

## Cross-reference

- §0.5.3 reading-paths-by-role (State banking commissioner reads the FFIEC IT Examiner row); this overlay supplements with TDoB-specific framing.
- §1 — applicable-agencies enumeration (TDoB via the "state banking commissioner" path; state banking departments via CSBS NCA).
- §1.2 — epistemic scope (the institution-asserted boundary for `audit.supervisory.*` and the 7 TAC §3.24 determination timestamp).
- §10.5 — HSM custody (community-institution-minimum posture applies for smaller Texas-chartered banks); §10.9 — IKM-registry retention (bind ≥ 5 years for BSA-bound chains).
- §10.13 — evidentiary artifacts (jurisdictionally portable; grounds TDoB enforcement).
- §10.70 — BSA SAR / privileged-investigation overlay (and examiner-access provenance).
- §10.72 — FOIA and state-sunshine release (Texas PIA at 10-business-day clock, §552.221).
- §10.76 — verifier-side trust-anchor distribution (the published HSM-signed IKM-registry manifest that answers the "bank signs its own evidence" objection).
- §10.83 — special-institution postures (state-authority conservatorship; `tx_dob_conservatorship` succession kind).
- §10.84 — communication principal-preapproval ordering (the ordering primitive reused for the 7 TAC §3.24 "before customer notification" proof).
- §14.13 — `audit.supervisory.*` supervisory-context provenance family.
- `docs/regulator-pack/state-banking-overlay.md` — broader state-banking-supervision overlay; this TDoB-specific overlay supplements it.
- `docs/regulator-pack/federal-reserve-overlay.md` — for dual-supervised state-member banks.
- `docs/regulator-pack/fdic-occ-examination-overlay.md` — for dual-supervised non-member banks (FDIC-supervised).

## Sources

Texas Finance Code Title 3 (banks / trust companies / MSBs); Texas Government Code Chapter 552 (PIA); 7 TAC Chapter 3 (§3.24 cybersecurity-incident notice) and 7 TAC §33.30 (MSB analog); TDoB public materials (dob.texas.gov — bank & trust supervision, IT examination procedures, financial-examiner brochure, cybersecurity-incident report, customer-service publication with CSBS accreditation history); FDIC examination-policies manual (§1.1 cooperative program, §16.1 ROE), FDIC InTREx program (FIL-2016-43), FDICconnect and Banker Engagement Site (FIL-2023-049), FDIC ETS privacy-impact assessment; FFIEC IT Examination Handbook and FFIEC 051 Call Report instructions; Federal Reserve SR 18-7 (examination cycle) and FOIA supervision-records retention schedule; CSBS Nationwide Cooperative Agreement. Federal-standard vs. Texas-specific facts are distinguished inline throughout.
