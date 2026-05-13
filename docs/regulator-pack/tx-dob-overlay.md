# Texas Department of Banking (TX DOB) supervisor overlay

**Scope.** Companion overlay for the Texas Department of Banking (TX DOB) and Texas-chartered banks, trust companies, and money-services-business licensees adopting the chain-of-custody specification. Maps spec sections to Texas Finance Code, the TX DOB Examination Manual, the Texas-specific operational framework, and the existing federal-agency overlays (TX DOB participates in the CSBS Nationwide Cooperative Agreement and routinely coordinates with FRB / OCC / FDIC on Texas-chartered institutions).

**Status.** Working draft — published 2026-05-11 to mirror the NYDFS Part 500 overlay's depth for Texas-chartered institutions.

## Texas-specific supervisory framework

TX DOB supervises approximately 200 state-chartered banks, 30 state-chartered trust companies, and a substantial money-services-business population. Texas-chartered institutions are dual-supervised: TX DOB on the state side + a federal prudential supervisor (FRB for state-member banks; FDIC for non-member banks). The chain composes with both supervisory regimes; this overlay names the TX-DOB-specific dimension.

Texas-specific regulatory framework:

- **Texas Finance Code Chapter 31-37** — the substantive Texas banking statute. Chapter 31 covers commercial banks; Chapter 35 covers trust companies; Chapter 37 covers state-savings institutions. The chain's safety-and-soundness anchor (§1.1 Daubert grounding, §10.5 HSM custody, §10.10 master-key rotation, §10.13 evidentiary artifacts) composes with Chapter 31-37's safety-and-soundness mandate.
- **Texas Finance Code §59.006 — bank-secrecy and customer-financial-record privacy** — the Texas analog to the federal Right to Financial Privacy Act (12 USC §3401 et seq.). The chain's §10.22 redaction discipline and §10.69 customer-disclosure subprocedure compose with §59.006's privacy framework.
- **Texas Business and Commerce Code Chapter 521 — Identity Theft Enforcement and Protection Act** — Texas's identity-theft framework. Composes with §10.13.3 litigation-hold registry (when identity-theft investigations escalate) and §10.70 privileged-investigation overlay (when investigations involve law-enforcement coordination).
- **Texas Government Code Chapter 552 — Texas Public Information Act (PIA)** — Texas's public-records framework. Applies to TX DOB itself for its examination records; institutions whose TX DOB examination records are subject to PIA requests have a different posture than those covered by the §10.72 FOIA-and-state-sunshine release subprocedure. The §10.72 state-sunshine clock table includes Texas PIA at the 10-business-day clock under §552.221.
- **7 TAC Chapter 3** — TX DOB administrative rules. Chapter 3 covers examination procedures, supervisory enforcement actions, and chartered-bank operational requirements. The chain's §10.x operational requirements provide the integrity-bound surface TX DOB examination consumes.
- **TX DOB Examination Manual** — the operational guide TX DOB examiners use. Aligns with the FFIEC IT Examination Handbook; the chain's FFIEC-aligned §10.x compositional path applies directly.

## TX DOB examination framework

TX DOB examination cycles are typically annual (small institutions) to 18-month (mid-sized institutions); larger institutions follow the FRB / OCC / FDIC schedule. The chain integrates with TX DOB examination at:

1. **IT examination integration.** TX DOB IT examiners apply the FFIEC IT Examination Handbook's IT-Audit booklet, Information-Security booklet, and Architecture/Infrastructure/Operations (AIO) booklet. The chain's §10.x operational requirements + §7 verifier procedure satisfy the IT-Audit booklet's audit-evidence expectations. Chain-bound institutions provide the verifier output as the audit-evidence artifact; TX DOB IT examiners re-verify independently using the §10.26 reference verifier.

2. **BSA/AML examination integration.** TX DOB examiners assess BSA/AML compliance under 31 CFR Part 1020 (the Federal BSA framework applied to state-chartered banks). The chain's §10.70 BSA SAR / privileged-investigation overlay provides the integrity-bound posture; SAR clock binding under `audit.bsa.sar.*` and CTR clock binding under `audit.bsa.ctr.*` give TX DOB examiners chain-bound timeline reconstruction without consulting institution-internal BSA-officer records.

3. **Trust-company examination.** TX DOB supervises state-chartered trust companies under Chapter 35 of the Finance Code. Trust-company AI deployments (trust-administration AI, beneficiary-advice AI, fiduciary-decision AI) are model-risk-relevant per SR 11-7 the same way commercial-bank AI is; the chain's §10.33 MRM disposition discipline applies identically. §10.69's estate / fiduciary disclosure procedure is particularly relevant for trust-company chains given the routine fiduciary-relationship context.

4. **Money-services-business (MSB) examination.** TX DOB regulates MSBs under Chapter 151-152 of the Finance Code. AI-driven MSB decisions (sanctions screening, fraud detection, transaction monitoring) bring the chain via §10.70 BSA SAR / OFAC-investigation regime values. Cross-border-MSB activity composes with §4.4.1 cross-border data transfer attributes.

5. **DOR / enforcement-action citation.** TX DOB enforcement actions (cease-and-desist orders, civil monetary penalties, charter revocations) cite the chain's verifier output as authoritative integrity evidence. The §10.13 evidentiary artifacts list is the citation surface; TX DOB's enforcement-action analysis follows the same evidentiary path as federal-supervisor enforcement.

## TX DOB / federal-supervisor coordination

State-chartered Texas banks have a federal prudential supervisor (FRB or FDIC). TX DOB coordinates with the federal supervisor on examinations of dual-supervised institutions. The chain integrates with this coordination at:

- **Alternating-examination cycle.** TX DOB and the federal supervisor typically alternate primary-examination years. The chain artifacts (seal records, verifier output, evidentiary artifacts) are jurisdictionally portable; both supervisors consume the same chain at their respective examination cycles. The institution's CC8.1 names the supervisory-coordination framework.
- **Joint examinations.** Specific high-risk or large-institution scenarios produce joint TX DOB + federal-supervisor examinations. The chain's verifier output is single-source-of-truth; both supervisors reach the same Verdict-Object via the §7 deterministic procedure.
- **Shared evidence vault.** When TX DOB and the federal supervisor share examination evidence (under the CSBS NCA framework), the chain's §10.13.1 discovery production form is the integrity-bound delivery surface. Both supervisors verify the production manifest's SHA-256 cross-references independently.

## Examiner reading path

TX DOB examiners read the spec through these lenses:

1. **IT examination (TX DOB IT examiner).** Read §1, §1.1, §4, §7, §10.12 (verifier exit codes), §10.13 (evidentiary artifacts). The chain's verifier output grounds TX DOB examination findings the same way it grounds FFIEC IT Examiner findings.

2. **BSA/AML examiner.** Read §10.70 BSA SAR / privileged-investigation overlay, §10.13.3 litigation-hold registry, §10.69 customer-disclosure (with §10.70 exclusion composition). The chain captures the SAR / CTR clock-start moments + the BSA-officer access-trail mechanically.

3. **Trust-company examiner.** Read §10.33 MRM disposition discipline, §10.69 estate / fiduciary disclosure procedure, §10.74 deletion-request schema (for trust-relationship privacy events). Trust-relationship-specific disclosure follows the §10.69 fiduciary-authority discipline.

4. **MSB examiner.** Read §10.70 BSA SAR / OFAC-investigation regimes, §4.4.1 cross-border data transfer, §10.71 cross-institution Fedwire / ACH chain integrity (when MSB operates wire / ACH origination).

5. **Enforcement attorney.** Read §10.13 evidentiary artifacts, §10.13.1 discovery production form, §10.13.2 FRCP framing (TX-state-court parallels), §10.26 verifier distribution. The chain's verifier output is citable in TX DOB enforcement actions.

## Cross-reference

- §0.5.3 reading-paths-by-role row for FFIEC IT Examiner applies; this overlay supplements with TX DOB-specific framing.
- §1 — applicable agencies enumeration (TX DOB falls under "state banking commissioner" path).
- §10.5 — HSM custody (community-institution-minimum posture applies for smaller TX-chartered banks).
- §10.13 — evidentiary artifacts list (jurisdictionally portable; grounds TX DOB enforcement actions).
- §10.21 — cross-vendor model-handover schema.
- §10.33 — model-update events + MRM disposition discipline.
- §10.69 — customer-disclosure subprocedure (including estate / fiduciary for trust companies).
- §10.70 — BSA SAR / privileged-investigation overlay.
- §10.72 — FOIA and state-sunshine public-records release (Texas PIA at 10-business-day clock).
- `docs/regulator-pack/state-banking-overlay.md` — broader state-banking-supervision overlay; this TX-DOB-specific overlay supplements it.
- `docs/regulator-pack/federal-reserve-overlay.md` — for dual-supervised state-member banks.
- `docs/regulator-pack/fdic-occ-examination-overlay.md` — for dual-supervised non-member banks (FDIC-supervised).
