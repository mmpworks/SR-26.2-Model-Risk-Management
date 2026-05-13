# NCUA examiner overlay

**Scope.** Companion overlay for National Credit Union Administration (NCUA) examiners and federally-insured credit unions adopting the chain-of-custody specification. Maps spec sections to NCUA Letters to Credit Unions, the NCUA AIRES (Automated Integrated Regulatory Examination System) tool, Federal Credit Union Act provisions, 12 CFR Chapter VII supervisory framework, and the credit-union-specific CUSO (Credit Union Service Organization) third-party-risk surface.

**Status.** Working draft — expanded 2026-05-11 with FCRA at 12 CFR Part 717, community-minimum HSM composition, and a CUSO third-party-risk worked example.

## NCUA-specific supervisory framework

The chain-of-custody specification was originally drafted against FFIEC IT Examination Handbook framing, with OCC Bulletin 2026-13 and SR 11-7 as the named anchor for model-risk-management alignment. NCUA participates in the FFIEC interagency body and aligns with the joint examination handbook; the spec's substantive content applies to federally-insured credit unions through the same FFIEC alignment that applies to OCC-supervised national banks and FRB-supervised state-member banks.

NCUA-specific guidance and regulatory framework:

- **Federal Credit Union Act, 12 USC §1751 et seq.** — the statutory framework governing federal credit unions. The chain's evidentiary posture (§1.1 Daubert grounding, §5.2 best-evidence under FRE 1001-1004, §10.13 evidentiary artifacts) composes with §1751's safety-and-soundness mandate. Specific §1751 sub-sections that intersect chain-of-custody operations include §1761b (fiduciary duty), §1786 (cease-and-desist authority), and §1787 (insurance coverage and conservatorship).
- **12 CFR Chapter VII** — NCUA regulations including Part 700 (definitions), Part 701 (organization and operation), Part 702 (prompt corrective action), Part 717 (fair credit reporting), Part 748 (security program; one of the chain's primary anchoring regulations for federal credit unions).
- **12 CFR Part 717 — Fair Credit Reporting Act for federal credit unions.** NCUA's FCRA implementation directly parallels the FRB Regulation V (12 CFR Part 222) and OCC FCRA regulations for banks. The chain composes via §10.11.2 FCRA §611 reinvestigation discipline (30-day clock, 45-day extension under §611(a)(3)), §10.69 customer-disclosure subprocedure (the chain-bound trail of disputed information), and §10.11 adverse-action notice translation. Part 717's specific subparts address:
  - **Subpart C (§717.20 — §717.22)** — affiliate marketing opt-out; the chain captures opt-out determinations as `audit.consumer_rights_request` entries under §10.74's CCPA / CPRA-parallel pattern.
  - **Subpart D (§717.30 — §717.32)** — medical-information rules; chain entries handling medical information compose with §10.73 HIPAA composition's `audit.phi.disposition` discipline where applicable.
  - **Subpart H (§717.70 — §717.83)** — fraud and active-duty alerts; chain-bound under `audit.fcra.fraud_alert` family per §10.11.2.
  - **Subpart I (§717.90)** — duties regarding the detection, prevention, and mitigation of identity theft (the Red Flags Rule). Composes with §10.13 evidentiary artifacts (identity-theft alerts produce chain-bound evidence trails) and §10.70 privileged-investigation overlay where investigations escalate to law-enforcement scope.
- **12 CFR Part 748 — Security Program, Report of Suspected Crimes, Suspicious Transactions, Catastrophic Acts and Bank Secrecy Act Compliance.** NCUA's primary information-security regulation. The chain composes via §10.5 HSM custody, §10.10 master-key rotation, §10.77 SDK-process hardening floor. Part 748 Appendix A (Guidelines for Safeguarding Member Information) is the credit-union analog to the FFIEC Information Security Booklet; the chain's §10.x operational requirements satisfy Appendix A through the same compositional path applied to FRB / OCC-supervised institutions.
- **NCUA Letters to Credit Unions** — supervisory letters serving the same examiner-orientation role that SR letters play for the Federal Reserve. Specific letters intersecting chain-of-custody operations include letters on AI/ML model use, third-party-vendor risk, and incident-response.
- **NCUA Supervisory Letter on Third-Party Risk Management.** NCUA's third-party-risk framework parallels SR 21-14 (Federal Reserve / OCC / FDIC joint guidance). The chain's vendor-management surface (§10.21 cross-vendor model-handover, §10.21.4 vendor-side entity succession, §10.39 / §10.40 cross-vendor composition manifests) composes with NCUA third-party-risk expectations. The CUSO-specific overlay below extends this composition for the credit-union-specific third-party form.

## Community-institution-minimum HSM posture for credit unions

§10.83 of the spec normates the community-institution-minimum HSM posture: managed cloud HSM (AWS CloudHSM, Azure Managed HSM, Google Cloud HSM) under FIPS 140-2 Level 3 satisfies §10.5 HSM custody at a price point reachable by community institutions. The posture applies directly to credit unions:

- **Federally-insured credit unions under $1B in assets.** Operate the community-institution-minimum posture via managed cloud HSM. The institution's CC8.1 names the chosen cloud HSM product (AWS CloudHSM Classic or v2, Azure Managed HSM, or Google Cloud HSM), the FIPS CMVP certificate number, and the §10.5 separation-of-duties posture (typically dual-control compensating control per the small-institution exemption — the §10.5 three-or-more-staff threshold is rarely met at sub-$1B credit unions).
- **Credit unions between $1B and $10B.** The community-minimum posture remains conformant; some institutions in this size band elect on-premises HSM custody (Thales nShield, Entrust nShield, AWS CloudHSM dedicated tenancy) per their risk-appetite. The chain doesn't require the more elaborate posture; §10.5's HSM-product list explicitly admits managed cloud HSM regardless of institution size.
- **Credit unions over $10B (the "complex" credit-union category under NCUA supervision).** Operate at the same posture as comparable-sized banks. §10.5 HSM custody applies identically; §10.80 three-lines-of-defense + internal-audit independence applies identically.

The cost picture: managed cloud HSM at a credit-union deployment scale (10-100 seal-job operations per day) runs $1,500-$3,000/month per cluster (institution + DR). The §10.82 RTO/RPO contract names HSM unavailability as a single-failure class with 4-hour RTO via cluster member failover; institutions running a single HSM cluster operate one HSM in primary, one in DR.

## CUSO third-party-risk worked example

Credit Union Service Organizations (CUSOs) are credit-union-affiliated third-party providers that deliver services to multiple credit unions. CUSOs are routinely the vendor for AI-driven decision-making tools used by member credit unions (consumer-loan underwriting AI, fraud-detection AI, member-service chatbots). The chain-of-custody composition with CUSO third-party risk:

**Scenario.** A CUSO ("MidwestCU AI Services") provides an AI-driven consumer-loan underwriting tool to 47 federally-insured credit unions across 8 states. NCUA examines one of the 47 credit unions ("Acme FCU") and reviews Acme FCU's vendor-management posture for the CUSO.

**Chain composition path:**

1. **CUSO-side chain.** The CUSO operates its own chain under its own `tenant_id` ("midwestcu-ai-services") capturing every model invocation across all 47 institutional clients. The CUSO's chain is the source-of-truth for model behavior; member credit unions consume the CUSO's services as a vendor relationship.

2. **Acme FCU's chain.** Acme FCU operates its own chain under `tenant_id = "acme-fcu"` capturing the credit-union-side chain entries: the loan decisions Acme FCU rendered (which reference the CUSO's model output as input), the consumer adverse-action notices Acme FCU sent under ECOA/Reg B, the FCRA reinvestigation requests under Part 717.

3. **Cross-vendor binding.** Each Acme FCU chain entry referencing a CUSO model invocation emits the §10.21 cross-vendor model-handover attribute family — `audit.model_handover.contract_id`, `contract_version`, `contract_hash_sha256` — binding the CUSO contract to the chain entry. The CUSO's chain-entry SHA-256 IS the upstream reference; Acme FCU's verifier walks both chains to confirm cross-vendor integrity.

4. **Vendor succession.** When the CUSO undergoes a succession event (per §10.21.4 — typically a key-rotation, channel-change, or rebrand; rarely a Chapter 11 reorganization), Acme FCU's chain anchors the CUSO's `vendor.entity_succession` event into Acme FCU's own chain via `chain.vendor_dissolution_anchored` (when applicable) or analogous anchoring per §10.21.4. The deployer-anchoring SLA floors apply (1 business day for HSM-key transitions; 5 business days for other; 2 hours for dissolution). NCUA's third-party-risk examination of Acme FCU reads the anchored events from Acme FCU's chain.

5. **NCUA examination questions answered from the chain alone:**
   - **"Is Acme FCU using a current CUSO contract?"** — Acme FCU's chain entries' `audit.model_handover.contract_id` + `contract_version` resolved against the active contract.
   - **"Did Acme FCU receive a vendor notification of HSM key change?"** — Acme FCU's chain contains the `vendor.entity_succession` anchor event with `hsm_key_fingerprint_continuity = "dual_key_rotation"`.
   - **"How does Acme FCU verify the CUSO's model outputs?"** — Acme FCU runs the §10.26 reference verifier against the CUSO's published chain artifacts; the verifier output is integrity-bound under the CUSO's HSM signature.
   - **"What is Acme FCU's exit plan if the CUSO is dissolved?"** — Acme FCU's CC8.1 names the §10.83 transitional-non-conformance posture; chain entries from the CUSO during the migration period are retained under the dissolved-CUSO's `hsm_key_fingerprint_at_dissolution` for verifier replay.

The worked example shows the §10.21 + §10.21.4 + §10.83 disciplines composing to give NCUA third-party-risk examination a chain-only verification surface. The credit union doesn't need to maintain a parallel third-party-risk documentation system; the chain captures the load-bearing third-party events.

## AIRES integration

The NCUA's automated examination tool (AIRES) ingests structured evidence from credit unions during examination cycles. The chain's published artifacts integrate with AIRES at:

- **Daily seal records.** AIRES-ingestible as JCS-canonical JSON; the seal record's HSM signature is verifiable from the institution's published HSM public key.
- **Verifier output (Verdict-Object).** AIRES-ingestible as the structured verdict line; the Status / Step / Reason / `Verdict-Object: <jcs-bytes>` format gives AIRES a structured parse target.
- **Operational events.** §10.2 operational events (e.g., `chain.verification_failure`, `master.posture_change_detected`, `connector.outage`) feed AIRES anomaly-detection workflows.
- **Evidentiary artifact lists.** §10.13 evidentiary artifacts per period grounds AIRES file-ingest for examination evidence.

Specific AIRES integration shape (per-attribute mapping, ingestion schema, examination workflow integration) is forthcoming as NCUA AIRES team publishes integration guidance.

## Examiner reading path

NCUA examiners read the spec for the first time approach the chain through these lenses:

1. **AI/ML decision-capture examination.** Read §1, §1.1, §1.2, §4 (the four primitives), §7 (verifier procedure), §10.11 (adverse-action notice translation, including FCRA §611 reinvestigation under §10.11.2). The chain-of-custody discipline binds the credit-union's AI-driven decisions to integrity-bound records the examiner re-verifies independently per §0.5.1.

2. **FCRA Part 717 examination.** Read §10.11.2 FCRA §611 reinvestigation, §10.69 customer-disclosure subprocedure, §10.74 deletion-request schema (parallel under Part 717 affiliate-marketing opt-out), §10.13.3 litigation-hold registry (Red Flags Rule investigations).

3. **AIRES integration.** The chain's published artifacts — daily seal records, verifier output, evidentiary artifact lists per §10.13, operational events per §10.2 — are AIRES-ingestible per the integration table above.

4. **CUSO third-party-risk review.** Read §10.21 cross-vendor model-handover, §10.21.4 vendor-side entity succession (including the SLA floors), §10.39 / §10.40 cross-vendor manifests, §10.83 receivership / non-cooperative succession. The CUSO worked example above is the operational template.

5. **Document of Resolution (DOR) citation.** When examination findings rise to DOR severity, the chain's verifier output (§7 normative output format) is the citable artifact. The same §10.13 artifact list grounds DOR citations as grounds Supervisory Letters / MRA / MRIA citations for OCC and FRB. The jurisdictional name changes; the evidentiary citation does not.

## Cross-reference

- §0.5.3 reading-paths-by-role row for FFIEC IT Examiner applies to NCUA examiners; this overlay supplements with NCUA-specific framing.
- §1 — applicable agencies enumeration names NCUA explicitly.
- §10.5 — HSM custody (community-institution-minimum posture applies to credit unions).
- §10.11.2 — FCRA §611 reinvestigation (the chain's FCRA discipline that grounds Part 717 examination).
- §10.13 — evidentiary artifacts list (jurisdictionally portable; grounds DOR, Supervisory Letters, MRA/MRIA, enforcement actions).
- §10.21 — cross-vendor model-handover schema.
- §10.21.4 — vendor-side entity succession (including CUSO succession events).
- §10.26 — reference verifier distribution discipline (NCUA examiners run the verifier independently per §0.5.1).
- §10.69 — customer-disclosure subprocedure (parallel applicability under §1033 and Part 717).
- §10.83 — community-institution-minimum HSM posture + receivership posture (CUSO dissolution scenario).
- §11 informative references — Federal Credit Union Act, 12 CFR Chapter VII, 12 CFR Part 717.
