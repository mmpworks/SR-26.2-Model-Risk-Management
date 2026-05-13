# State banking commissioner overlay

**Scope.** Companion overlay for state banking departments — every state chartering / supervising banks and trust companies. Maps spec sections to CSBS (Conference of State Bank Supervisors) Nationwide Cooperative Agreement (NCA), the model state regulations CSBS develops, and the largest state-banking-department-specific regimes (TX DOB, CA DFPI, MA DOB, IL IDFPR, GA DBF, FL OFR, OH ODFI, NJ DOBI, and others). The existing NYDFS-specific overlay (`nydfs-part500-overlay.md`) covers the most-named state regime; this overlay handles state-banking jurisdictions more broadly.

**Status.** Initial overlay shell. Detailed per-state guidance is forthcoming.

## State-banking-specific supervisory framework

State-chartered banks operate under dual supervisory authority — their state banking department and either the FDIC (state-nonmember banks) or the Federal Reserve (state-member banks). The chain-of-custody specification composes with both authorities; this overlay focuses on the state-banking side.

CSBS coordinates state-banking supervision through the Nationwide Cooperative Agreement (NCA) and the Multi-State MSB Examination Program. The chain-of-custody discipline composes with CSBS coordination via:

- **Multi-state examination cycles.** A state-chartered bank operating across multiple states may host CSBS-coordinated examinations. The chain's verifier output (§7 normative output format) is the citable artifact across every state's examination team; the examination team running the verifier from the institution's published artifacts (per §0.5.1) reads byte-equivalent output to every other state's team. Cross-state examiner disputes about "what did the chain say" reduce to a re-run of the verifier.
- **State-level model AI regulations.** A growing number of state regulators are developing AI-specific rules for state-chartered institutions. The chain's §1.1 Daubert grounding, §4.4.2 deployment-intent capture, §4.4.5 underwriting-features family, and §10.11 adverse-action translation form a regulator-portable evidentiary substrate; state rules referencing AI-decision documentation map onto these sections without spec amendment.
- **Visitorial Powers Act (12 USC 484) considerations.** The federal visitorial-powers regime constrains state authority over national banks but does NOT constrain state authority over state-chartered banks. The chain's verifier-driven evidence model is equally available to federal and state examiners; the chain does not implicate visitorial-powers conflicts because the institution-published artifacts (per §0.5.1) are accessible to any examiner with normal supervisory authority.

## State-specific intersection points (representative)

The largest state-banking regimes by supervised-asset volume and the chain-of-custody touchpoints each emphasises:

- **Texas Department of Banking (TX DOB).** State Banking Act (Tex. Fin. Code §31 et seq.); Texas adverse-action regulations parallel to ECOA. §10.11 / §10.11.1 / §10.11.2.
- **California Department of Financial Protection and Innovation (CA DFPI).** California Consumer Financial Protection Law (2020); California Privacy Rights Act (CPRA, 2023 amendments). §10.22, §10.38, §10.69.
- **Massachusetts Division of Banks (MA DOB).** 209 CMR 50 (cybersecurity), 209 CMR 26 (consumer protection), Mass. data-breach-notification law. §10.5, §10.13, §10.22.
- **Illinois Department of Financial and Professional Regulation (IL IDFPR).** Illinois Personal Information Protection Act (PIPA), Illinois AI-screening laws for employment decisions (AI Video Interview Act). §1.2 epistemic scope; §10.11 adverse-action translation; §10.22 redaction.
- **Georgia Department of Banking and Finance (GA DBF).** Georgia banking code, multi-state coordination through CSBS NCA. §10.13, §10.26.
- **Florida Office of Financial Regulation (FL OFR).** Florida banking code, Florida Information Protection Act. §10.22, §10.38.

NYDFS Part 500 is covered separately in [`nydfs-part500-overlay.md`](nydfs-part500-overlay.md).

## Examiner reading path

State banking commissioners and field examiners reading the spec for the first time:

1. **First-look orientation.** Read §0.5.3, §1, §1.1, §13 stakeholder entries. The CFR / regulator-pack referenced documents (NYDFS Part 500, this overlay, the joint OCC/FDIC examination overlay) provide the operational anchors.

2. **Joint federal-state examination.** Read §10.13 evidentiary artifacts, §10.26 reference verifier distribution, and the FDIC/OCC examination overlay. The same artifact list grounds both federal and state examination findings.

3. **State-specific consent order / enforcement action.** §10.13's evidentiary-artifact list is jurisdictionally portable; the state can cite the chain in a state-specific consent order using the same verifier output cited in a federal Supervisory Letter or MRA.

## Cross-reference

- §0.5.3 reading-paths-by-role — state banking commissioner reads the FFIEC IT Examiner row.
- §1 — applicable agencies enumeration names state banking departments via CSBS NCA.
- §10.13 — evidentiary artifacts (jurisdictionally portable).
- §10.26 — reference verifier distribution (state examiners run the verifier independently).
- [`nydfs-part500-overlay.md`](nydfs-part500-overlay.md) — NYDFS-specific deep-dive.
- [`fdic-occ-examination-overlay.md`](fdic-occ-examination-overlay.md) — federal-state joint examination posture.

## Forthcoming detailed content

This stub anchors state-banking-departments-broadly in the spec corpus. Detailed content (per-state walkthroughs, CSBS NCA integration patterns, state-specific consent order language) lands in a future revision after a state banking commissioner or CSBS coordinator provides operational feedback against the current §10.x normative content.
