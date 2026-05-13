# Federal Reserve supervisor overlay

**Scope.** Companion overlay for Federal Reserve Board (FRB) supervisors and FRB-supervised institutions — state-member banks, bank holding companies (BHCs), savings and loan holding companies (SLHCs), foreign banking organizations (FBOs) operating US branches under Reg K, intermediate holding companies (IHCs), and US-supervised non-bank subsidiaries under FRB consolidated supervision. Maps spec sections to SR letters, the FRB-counterpart to OCC Bulletin 2026-13, SR 21-14 (third-party risk), SR 13-19 (IT examination), the FRB consolidated-supervision framework, and CCAR / DFAST / LISCC review cycles.

**Status.** Working draft — expanded 2026-05-11 to match the depth of the NYDFS Part 500 overlay.

## FRB-specific supervisory framework

The chain-of-custody specification names SR 11-7 (Model Risk Management) and OCC Bulletin 2026-13 (the joint OCC / FRB / FDIC consolidated MRM update) as primary regulator-facing anchors. SR 11-7 is the original FRB statement; OCC Bulletin 2026-13 is the consolidated joint statement co-published by all three federal banking agencies. FRB-specific SR letter counterparts to OCC Bulletin 2026-13 are tracked alongside as they publish.

FRB-specific guidance intersecting chain-of-custody operations:

- **SR 11-7 — Model Risk Management (2011).** Foundational MRM framework. The chain's evidentiary posture composes cleanly: §1.1 Daubert grounding names SR 11-7 explicitly; §4.4.2 deployment-intent capture binds the developer / owner / validator triangle into integrity-bound chain entries; §10.33 model-update events bind artifact handoffs. The §10.33 MRM disposition discipline (`audit.mrm_disposition.recorded` events; validation-precedes-activate ordering rule; retirement-MRM-attestation REQUIREMENT for `failed_validation` / `regulatory_directive` retirements) gives FRB examiners a chain-bound walk through the SR 11-7 effective-challenge framework without consulting institution-internal MRM-meeting minutes.
- **SR 21-14 — Third-Party Relationships: Risk Management (2023 Interagency Guidance, joint with OCC + FDIC).** Vendor-management framework for FRB-supervised institutions. The chain's vendor-management surface (§10.21 cross-vendor model-handover, §10.21.4 vendor-side entity succession including Chapter 7 dissolution, §10.26 verifier-distribution discipline applied to SDK distribution, §10.39 / §10.40 composition manifest binding and cross-vendor chain-merge anchor) composes with SR 21-14's expectations on contract diligence, ongoing monitoring, and exit / contingency planning. The §10.21.4 deployer-anchoring SLA floors (1 business day for HSM-key transitions; 5 business days for other successions; 2 hours for vendor dissolution) close the SR 21-14 "ongoing monitoring" question — the deployer institution captures vendor-side events into its own chain mechanically.
- **SR 13-19 / FRB Information Technology Examination Framework.** Aligns FRB IT examination work with FFIEC IT Examination Handbook. The chain's §10.x operational requirements (§10.1 reconciliation, §10.5 HSM custody, §10.10 master-key rotation, §10.17 partition ceremony, §10.77 SDK-process hardening floor) compose with SR 13-19's IT-control expectations.
- **SR 16-11 — Supervisory Guidance for Assessing Risk Management at Supervised Institutions.** The risk-governance framework FRB applies to supervised institutions. The §10.80 three-lines-of-defense ownership map composes directly — the chain's ownership allocation across first-line (chain-operations team), second-line (MRM committee / compliance), and third-line (internal audit with normative independence discipline) gives FRB examiners a structured surface for risk-governance review.
- **SR 17-3 — Recovery and Resolution Preparedness for Certain Supervised Institutions.** Recovery-planning framework. The §10.82 RTO/RPO contract per failure class, §10.83 receivership posture (including non-cooperative receivership and cross-border resolution authorities), and §10.13 wind-down / decommissioning discipline give FRB recovery-planning reviewers the chain-of-custody continuity surface.
- **Reg K (12 CFR Part 211)** — international banking operations. FBOs operating US branches and Edge Act corporations apply the chain through their US-branch operations. The §10.15 multi-region resilience patterns (Pattern A active-active + seal-region pinning, Pattern B per-region tenant_id) compose with Reg K's home-host-country supervisory framework; the US-branch chain MUST be verifiable from US-resident artifacts (verifier binary, IKM custody, HSM cluster) without dependence on home-country systems for FRB examination. §10.83 FBO posture names the US-resident chain-coverage map discipline.
- **Reg WW (12 CFR Part 249)** — liquidity coverage ratio (LCR) reporting. Not directly chain-related but the underlying decision-making for liquidity stress testing is increasingly model-driven; institutions deploying ML-assisted liquidity-stress models bring those models under the chain via §4.4.5 underwriting-features-equivalent capture and §10.33 MRM-disposition discipline.
- **Consolidated supervision (12 USC §1841, §3106)** — bank holding companies and their non-bank subsidiaries. The §10.19 chain-coverage map names every legal-entity tenant under the consolidated perimeter so FRB consolidated supervision reads the full set; §10.24 entity-succession discipline covers intra-group reorganizations. The §10.83 consolidated-supervision posture names which `tenant_id` values are under the holding company's chain coverage.

## CCAR / DFAST integration

The Comprehensive Capital Analysis and Review (CCAR) and Dodd-Frank Act Stress Test (DFAST) cycles examine large institutions' capital-adequacy decisions under stress scenarios. Model-driven inputs to CCAR / DFAST submissions (credit-loss projections, PPNR forecasts, AML-risk simulations) are model-risk-relevant per SR 11-7; chain-bound institutions bring those model inputs under the chain via §10.34 training-phase integrity + §10.33 model-update events.

CCAR / DFAST reviewers reading the chain confirm:

1. **Model inventory completeness.** Cross-reference the chain's `model_inventory.snapshot` operational events (per §10.2) against the institution's CCAR submission's named models. A model active during the stress test that is absent from the chain's inventory snapshot is a control-completeness gap.
2. **Model-update governance.** The `audit.model_update.activate` chain entries during the stress-test window MUST reference an `audit.model_validation.attestation` event in the chain (§10.33 validation-precedes-activate ordering rule). A model activated under a stress-test reference period without a chain-bound validation attestation surfaces as a CCAR control gap.
3. **MRM disposition trail.** Every CCAR-relevant model activation references an `audit.mrm_disposition.recorded` event with `outcome ∈ {approved, approved_with_conditions}`. The chain captures the MRM disposition without requiring the CCAR reviewer to consult the institution's MRM-meeting record.
4. **Posture stability during stress test.** The chain's `chain.posture_change_approved` events during the stress-test window are reviewed for unauthorized posture changes that could compromise the stress-test integrity.

## LISCC large-institution-specific guidance

The Large Institution Supervision Coordinating Committee (LISCC) supervises the largest, most complex US banking organizations under a horizontal-review framework. LISCC reviews intersect with the chain at:

- **Cross-LISCC-firm comparability.** The chain's spec-version pinning + verifier-version binding + Verdict-Object structured output let LISCC reviewers compare chain artifacts across LISCC firms without re-interpreting per-firm conventions. A LISCC horizontal review on AI-driven decision-making consumes the same Verdict-Object schema across every covered institution.
- **Tier-1 institution model inventory scale.** LISCC firms typically operate thousands of models. The chain's `model_inventory.snapshot` cadence (typically quarterly) + the `mrm_disposition_count_by_outcome` board-quarterly-attestation schema (per §10.2) compose to give LISCC reviewers an integrity-bound quarterly digest at the size of the institution's MRM program.
- **CCAR LISCC participation.** LISCC firms are routinely CCAR-supervised; the CCAR integration above applies in full to LISCC firms.

## RBO regional-banking-organization guidance

Regional Banking Organizations (RBOs) — typically $10B-$100B in total assets — operate under FRB regional bank supervision. The chain's community-institution-minimum posture (§10.83 managed-cloud-HSM) is the relevant floor; RBOs operating cloud HSM under FIPS 140-2 Level 3 are conformant. RBO supervision reads the chain at:

- **IT examination integration.** RBO examiners apply SR 13-19 + the FFIEC IT Examination Handbook the same way FRB IT examiners do for state-member banks; the chain's §10 operational requirements compose identically.
- **Risk-governance scaling.** §10.80 three-lines-of-defense applies; RBOs whose internal-audit function is outsourced operate the outsourcing-discipline per §10.80's normative-when-applicable framing.
- **Vendor concentration.** RBOs frequently operate with a smaller vendor roster than LISCC firms; §10.21.4 vendor-side succession discipline and the deployer-anchoring SLA floors apply at the RBO scale identically.

## FBO / Reg K branch examination

Foreign Banking Organizations operating US branches under Reg K supervision face two parallel posture questions:

- **US-branch chain conformance.** The chain MUST be verifiable from US-resident artifacts. §10.83 names the US-resident chain-coverage map, the US-resident HSM cluster, and the institution's published HSM public key (hosted at a US-resident endpoint per CC8.1). FBO supervision confirms US-resident artifacts via a US-resident verifier run at examination time.
- **Home-country chain composition.** When the FBO's home-country systems operate parallel chains, the §10.21 cross-vendor model-handover schema OR the §10.21.3 registry-discovery cross-anchor pattern composes the home-country and US-branch chains. The chain's `audit.cross_border_transfer.*` family (per §4.4.1) records cross-border data movement; FBO supervision reviews the cross-border posture against US-branch examination scope.

## Examiner reading path

FRB examiners read the spec through their supervisory lens:

1. **State-member bank IT examination (BSO).** Read §1, §1.1, §4, §7, §10.12 (verifier exit codes), §10.13 (evidentiary artifacts), §10.33 (model-update events + MRM disposition). The chain's verifier output grounds Supervisory Letter findings the same way it grounds FFIEC IT Examiner findings.

2. **Holding-company-wide review (consolidated supervision).** Read §10.19 chain-coverage map, §10.24 entity succession, §4.4.2 deployment-intent, §10.21 cross-vendor handover, §10.83 consolidated-supervision posture. The consolidated chain-coverage map names every legal-entity tenant under the consolidated perimeter; FRB consolidated supervision reads the full set.

3. **CCAR / DFAST reviewer.** Read §10.33 model-update events + MRM disposition, §10.34 training-phase integrity, §10.66 model-weight lineage, §4.4.2 deployment-intent. Confirm model inventory completeness, validation-precedes-activate ordering, MRM disposition trail.

4. **LISCC horizontal reviewer.** Read §10.12 verifier CLI exit-code contract, §7 Verdict-Object schema, §10.2 `model_inventory.snapshot` + `board.quarterly_attestation` events. Compare across LISCC firms using identical Verdict-Object structured output.

5. **RBO examiner.** Read §10.83 community-institution-minimum HSM posture, §10.80 three-lines-of-defense (including outsourced-audit discipline), §10.21 cross-vendor handover.

6. **FBO / Reg K branch examiner.** Read §10.83 FBO posture, §10.15 multi-region resilience, §4.4.1 cross-border data transfer attributes, §10.21 cross-vendor handover. The US-branch chain is verifiable from US-resident artifacts; home-country dependencies are documented residuals.

## Cross-reference

- §0.5.3 reading-paths-by-role row for FFIEC IT Examiner applies; this overlay supplements with FRB-specific framing.
- §1 — applicable agencies enumeration names FRB.
- §1.1 — Daubert four-factor grounding cites SR 11-7.
- §10.15 — multi-region resilience patterns (FBO posture).
- §10.19 — chain-coverage map (consolidated supervision).
- §10.21 — cross-vendor model-handover schema.
- §10.21.4 — vendor-side entity succession (including Chapter 7 dissolution).
- §10.24 — entity succession (BHC reorganizations).
- §10.33 — model-update events + MRM disposition discipline.
- §10.80 — three-lines-of-defense ownership map (normative-when-applicable + internal-audit independence).
- §10.82 — SLAs and operational ceilings + RTO/RPO contract.
- §10.83 — FBO posture + consolidated-supervision posture + receivership posture.
- §11 informative references — SR 11-7, SR 21-14, SR 13-19, SR 16-11, SR 17-3, OCC Bulletin 2026-13.
