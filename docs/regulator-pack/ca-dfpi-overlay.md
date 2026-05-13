# California Department of Financial Protection and Innovation (CA DFPI) supervisor overlay

**Scope.** Companion overlay for the California Department of Financial Protection and Innovation (CA DFPI) and California-chartered banks, credit unions, lenders, money transmitters, and California-licensed financial-services entities adopting the chain-of-custody specification. Maps spec sections to the California Financial Code, the CA DFPI's expanded consumer-protection authority under the California Consumer Financial Protection Law (CCFPL), the California-specific privacy framework (CCPA / CPRA / state-DOJ rules), and the federal-supervisor coordination layer.

**Status.** Working draft — published 2026-05-11 to mirror the NYDFS Part 500 overlay's depth for California-licensed institutions.

## California-specific supervisory framework

CA DFPI is the successor (since 2020) to the former Department of Business Oversight (DBO). The 2020 California Consumer Financial Protection Law (CCFPL, Assembly Bill 1864) expanded DFPI's authority substantially — DFPI now supervises a wider population than the prior DBO, including emerging financial-services categories (debt collectors, debt-settlement services, payday lenders, earned-wage access providers, certain financial-data providers, certain AI-driven financial decision systems).

California-specific regulatory framework:

- **California Financial Code Division 1.1 et seq.** — DFPI's statutory authority including Division 1.2 (state-chartered banks), Division 5 (credit unions), Division 16 (CCFPL — the consumer-protection authority expansion), Division 25 (money transmitters).
- **California Financial Code §22000 et seq. (California Financing Law)** — non-depository lenders. The chain's §10.11 ECOA / Reg B framing applies; California-specific additional disclosure under §22338 composes with §10.69 customer-disclosure subprocedure.
- **California Consumer Privacy Act (CCPA) / California Privacy Rights Act (CPRA), Cal. Civ. Code §1798.100 et seq.** — California's consumer-privacy framework. The chain's §10.74 CCPA / CPRA consumer-rights surface (deletion-request schema, correction-request family, right-to-know family, sensitive-PII-limit family, downstream-propagation array) composes directly. Cal. Code Regs. tit. 11 §7060 verifiable-consumer-request authentication procedure rides under `audit.consumer_rights_request.received_at_utc`.
- **California Insurance Information Privacy Act, Cal. Insurance Code §791** — California-specific insurance privacy framework (applies to California-licensed insurers; DFPI does not directly supervise insurers but coordinates with the CA Department of Insurance on cross-jurisdictional issues).
- **California Public Records Act, Cal. Gov't Code §7920 et seq. (recodified 2023)** — California public-records framework. Applies to CA DFPI itself for its examination records; the §10.72 state-sunshine clock table includes Cal. PRA at the 10-calendar-day clock under §7922.535.
- **CCFPL implementing regulations (10 CCR §1010 et seq.)** — DFPI's implementing regulations for the expanded authority. Cover the CCFPL's UDAP-equivalent prohibition (Cal. Fin. Code §90008 — unfair, deceptive, or abusive acts or practices), debt-collector licensing (Cal. Fin. Code §100000 et seq.), and consumer-disclosure requirements under DFPI's expanded scope.
- **DFPI Supervisory Letters / Advisory Opinions** — supervisory communications equivalent to SR letters. Specific letters intersecting chain-of-custody operations include guidance on AI/ML model use in consumer-lending decisions and third-party-vendor risk for DFPI-licensees.

## CA DFPI examination framework

CA DFPI examination cycles vary by license type. State-chartered banks under DFPI follow an 18-month or annual cycle (coordinated with FDIC or FRB on dual-supervised institutions). Non-depository licensees (lenders, money transmitters, debt collectors) face periodic examinations on shorter cycles. The chain integrates with CA DFPI examination at:

1. **State-chartered bank IT examination.** DFPI IT examiners apply the FFIEC IT Examination Handbook the same way other state-banking supervisors do. The chain's §10.x operational requirements + §7 verifier procedure satisfy IT-Audit booklet expectations. DFPI runs the §10.26 reference verifier independently.

2. **CCPA / CPRA examination integration.** DFPI does NOT directly enforce CCPA / CPRA (that's the California Privacy Protection Agency — CPPA — under the CPRA framework). But DFPI-supervised institutions face CCPA / CPRA obligations the chain captures via §10.74. DFPI examination of DFPI-licensees' overall consumer-protection posture reads the chain's CCPA / CPRA-bound entries for evidence of compliance discipline.

3. **CCFPL UDAP examination.** DFPI's UDAP-equivalent enforcement authority under Cal. Fin. Code §90008 covers AI-driven decision-making for disparate-impact, deceptive-pricing, or unfair-discrimination concerns. The chain's §4.4.5 underwriting-features family + §10.22 redaction discipline (with the §10.74 CCPA / CPRA sensitive-PII-limit family) provide the integrity-bound evidence DFPI UDAP examination consumes.

4. **Money-transmitter examination.** Cal. Fin. Code Division 25 (money-transmitter licensing). AI-driven sanctions screening, fraud detection, and transaction monitoring bring the chain via §10.70 BSA SAR / OFAC-investigation regime values + §4.4.1 cross-border data transfer attributes.

5. **Debt-collector / debt-settlement examination.** Under DFPI's expanded CCFPL authority. AI-driven debt-collection decisions (consumer-contact strategy, collection-priority scoring, hardship-determination) compose with §10.11 ECOA-equivalent disclosure + §10.69 customer-disclosure for FDCPA-bound consumer rights. The CCPA / CPRA correction-request family (§10.74) handles consumer-asserted-error disputes.

6. **Earned-wage access (EWA) / financial-data-provider examination.** Newer license categories under DFPI. The chain's §1033-equivalent customer-data-rights surface (§10.69) applies; CCFPL-specific consumer-protection examination reads the chain's §10.74 CCPA / CPRA bindings.

## CCFPL UDAP examination — worked example

**Scenario.** "Bay Loans LLC" is a California Financing Law licensee operating an AI-driven consumer-loan underwriting tool. A California consumer files a complaint with DFPI alleging Bay Loans's AI denied her loan based on a protected-class proxy (her ZIP code, which DFPI has previously identified as a proxy for race in California consumer-lending contexts). DFPI investigates under CCFPL §90008 UDAP authority.

**Chain composition path:**

1. **DFPI's CID under CCFPL §90015.** DFPI issues a Civil Investigative Demand for Bay Loans's chain artifacts covering the consumer's loan-decision period.

2. **Bay Loans's §10.13.1 discovery production.** Bay Loans produces the §10.13.1-shaped discovery package: NDJSON entries, canonical-bytes per entry, seal records, Verdict-Object, trust-anchor manifest, production manifest. The §10.13.1 production-discipline ensures DFPI re-runs the verifier and reaches byte-identical output.

3. **Cohort-disclosure for class-affected consumers.** DFPI orders a §10.69 class-disclosure for all California consumers Bay Loans's AI rendered denials against during the relevant period whose ZIP code matched the protected-class proxy pattern. Bay Loans produces the cohort-disclosure packet under the §10.69 class-disclosure sub-mode.

4. **Protected-class proxy enumeration.** Bay Loans's `audit.redaction.protected_class_disposition` values across the cohort show whether redaction-for-anti-discrimination was operative. §10.22 protected-class proxy floor — which includes CFPB / HUD / OCC / California-DFPI published proxy lists — sets the minimum protected-class enumeration; DFPI verifies the institution's CC8.1 enumeration covers ZIP code as a proxy.

5. **Disparate-impact test composition.** §4.4.5 + §10.22 composition requires `audit.disparate_impact_test.*` evidence within the CC8.1-named cadence when `redacted_for_anti_discrimination` is operative. DFPI walks the disparate-impact test events across Bay Loans's models for the cohort period.

6. **DFPI enforcement decision.** DFPI's UDAP determination is informed by the chain evidence. The chain proves Bay Loans's posture (the bytes); DFPI's substantive review of the disparate-impact test results determines whether the posture met CCFPL § 90008's "unfair / discriminatory practice" threshold. Enforcement actions (consent orders, civil monetary penalties, license restrictions) cite the chain's Verdict-Object as authoritative integrity evidence.

The worked example shows §10.22 + §4.4.5 + §10.69 + §10.74 composing for DFPI UDAP examination. The chain captures the institution's posture; DFPI's substantive review of disparate-impact evidence determines the outcome.

## Federal-supervisor coordination

California-chartered banks have a federal prudential supervisor (FRB or FDIC). DFPI coordinates with the federal supervisor on examinations of dual-supervised institutions:

- **Alternating-examination cycle.** DFPI and the federal supervisor alternate primary-examination years; the chain is jurisdictionally portable across both.
- **CCFPL UDAP coordination with CFPB.** DFPI and CFPB coordinate on UDAP / UDAAP investigations; the chain's §10.69 compelled-disclosure backstop names CFPB CID under 12 USC §5562 as a compelled-production authority. DFPI CIDs under §90015 are recognized parallel authority.
- **Money-transmitter cross-jurisdictional coordination.** DFPI coordinates with FinCEN on BSA / AML enforcement for money transmitters; §10.70 BSA SAR overlay applies identically.

## Examiner reading path

DFPI examiners read the spec through these lenses:

1. **State-chartered bank IT examination.** Read §1, §1.1, §4, §7, §10.12 (verifier exit codes), §10.13 (evidentiary artifacts). Same path as FFIEC IT Examiner.

2. **CCFPL UDAP examiner.** Read §1.2, §4.4.5 underwriting-features, §10.11 ECOA-equivalent, §10.22 redaction (protected-class disposition), §10.69 customer-disclosure, §10.74 CCPA / CPRA additional rights surface, §10.74 deletion-request schema (CCPA §1798.105 denial-basis hash composition).

3. **Money-transmitter examiner.** Read §10.70 BSA SAR overlay, §4.4.1 cross-border data transfer, §10.71 cross-institution chain integrity.

4. **Debt-collector / debt-settlement examiner.** Read §10.11 ECOA / FCRA, §10.69 customer-disclosure with FDCPA composition, §10.74 correction-request family.

5. **Enforcement attorney.** Read §10.13 evidentiary artifacts, §10.13.1 discovery production form, §10.69 compelled-disclosure backstop (DFPI CCFPL §90015 CID parallel authority), §10.26 verifier distribution. The chain's verifier output is citable in DFPI enforcement actions.

## Cross-reference

- §0.5.3 reading-paths-by-role row for FFIEC IT Examiner applies; this overlay supplements with DFPI-specific framing.
- §1 — applicable agencies enumeration (DFPI falls under "state banking commissioner" + CCFPL-specific framing).
- §4.4.5 — underwriting-features family (CCFPL UDAP enforcement surface).
- §10.5 — HSM custody (community-institution-minimum posture for smaller DFPI-supervised institutions).
- §10.11 — ECOA / Reg B adverse-action notice translation (CCFPL UDAP composition).
- §10.13 — evidentiary artifacts list (jurisdictionally portable; grounds DFPI enforcement actions).
- §10.22 — redaction discipline (protected-class proxy floor includes CFPB / HUD / OCC enumerations).
- §10.69 — customer-disclosure subprocedure (compelled-disclosure backstop names DFPI CCFPL §90015 CID).
- §10.70 — BSA SAR / privileged-investigation overlay (money-transmitter examination).
- §10.72 — FOIA / state-sunshine release (Cal. PRA at 10-calendar-day clock).
- §10.74 — CCPA / CPRA additional rights surface (deletion-request, correction-request, right-to-know, sensitive-PII-limit families).
- `docs/regulator-pack/state-banking-overlay.md` — broader state-banking-supervision overlay; this DFPI-specific overlay supplements it.
- `docs/regulator-pack/ccpa-cpra-rights.md` — California-specific consumer-rights companion (composes with §10.74).
- `docs/regulator-pack/cfpb-overlay.md` — for CFPB / DFPI coordination on UDAP / UDAAP investigations.
