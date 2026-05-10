# Interested parties — who reads this spec

A navigation aid keyed to spec audiences. Identifies the personas (institutional roles, regulators, external audit, implementers, counterparties, observers) who read the FFIEC chain-of-custody spec, the parts most relevant to each, and the auditor stories that exercise the role in production.

This file extends spec §13 (Stakeholder navigation, lines 2861-3089) with personas the auditor-stories surface that the spec's own per-role guide does not enumerate. Where §13 already names a persona, this file copies its section pointers and adds story-engagement context.

Story numbers refer to `docs/auditor-stories/` 01-20. Companion documents live under `docs/`, `docs/regulator-pack/`, `docs/control-map/`, `docs/soc-pack/`, `docs/templates/`, and `docs/design/`.

## Persona index

| Persona | One-line role | Top spec sections | Most-relevant stories |
|---|---|---|---|
| Audit Committee chair | Board-level oversight of chain controls | §0.5.3, §1.1, §1.2, §13 | 01, 04, 14, 20 |
| Chief Audit Executive (CAE) | Leads internal audit; signs the engagement letter on the institution side | §7, §10.13, §10.18, §10.19, §13 | 01, 04, 14, 16, 20 |
| Internal audit team | Independent verification, control evaluation | §7, §10.12, §10.13, §10.18, §10.19 | 01-20 |
| Chief Information Security Officer (CISO) | Institutional cyber posture; threat-model owner | §1.3, §1.4, §4.3, §10.5, §10.7, §10.17 | 04, 06, 08, 12, 18 |
| Chief Compliance Officer / CRO | Regulatory posture, multi-framework alignment | §10.11, §10.19, §10.21, §10.22, §10.23, §13 | 02, 04, 07, 09, 13, 17 |
| Model Risk Management chair | SR 11-7 model lifecycle; chain as model-risk control | §1.1, §1.5, §4.4.2, §10.20, §10.21, §10.66, §10.67 | 02, 06, 07, 16, 19 |
| Chief AI / ML Officer | AI-system owner; deployment-intent author | §4.4.1, §4.4.2, §10.20, §10.21, §10.33, §10.47-§10.50, §10.63-§10.67 | 02, 06, 07, 13, 16, 19 |
| Chief Data Officer | Data lineage, retention, training-corpus provenance | §10.20, §10.22, §10.63, §A.1-A.16 | 07, 13, 19 |
| General Counsel | Legal-process posture, evidentiary readiness | §1.1, §5.2, §10.13, §10.55, §10.69, §10.70 | 07, 14, 16, 17, 20 |
| Privacy Officer / DPO | Tokenization, GDPR/DPDP/CCPA/PIPA alignment | §10.22, §10.23, §10.38, §10.69 | 07, 09, 11, 13, 17 |
| DevSecOps / SRE on-call | Runtime, IR, DR, BYOC | §4.3.1, §10.4, §10.15, §10.16, §10.25 | 06, 12, 14, 18 |
| Vendor management lead | Vendor-hosted, BYOC, supply-chain trust | §10.16, §10.21, §10.26, §10.40, §10.56-§10.60 | 03, 08, 11, 14, 18 |
| M&A integration lead (acquirer) | Diligence and post-close evidence-trail survival | §10.19, §10.21, §10.24, §10.39-§10.42 | 14, 20 |
| M&A integration lead (acquired entity) | Pre-acquisition cooperation; cut-over discipline | §10.24, §10.39, §10.41, §10.42 | 14, 20 |
| FFIEC IT Examiner (FDIC / OCC / FRB) | Examination cycle, finding language | §1.1, §1.2, §7, §10.12, §10.18, §13 | 01, 04, 12, 14, 20 |
| FFIEC Cybersecurity Specialist Examiner | NIST CSF alignment, threat model, supply chain | §1.3, §1.4, §10.5, §10.7, §10.17, §10.21, §10.56-§10.62 | 04, 08, 12, 18 |
| FFIEC Examiner-in-Charge (EIC) | Examination logistics, repeat-finding posture | §7, §10.12, §10.18, §10.19, §13 | 01, 04, 12, 14, 20 |
| CFPB consumer-protection examiner | §1033 disclosure, ECOA / FCRA, dispute response | §10.11, §10.11.1, §10.11.2, §10.23, §10.69 | 04, 07, 20 |
| FTC AI / privacy examiner | UDAP, AI-driven consumer harm | §1.1, §1.2, §4.4.1, §4.4.2, §10.21 | 04, 07, 12 |
| FDA BIMO inspector | ALCOA+, clinical-trial integrity | §1.1, §10.13, §10.20, §10.47-§10.50 | 02, 05, 16 |
| HHS OCR examiner (HIPAA) | PHI integrity, security-rule mapping | §10.5, §10.22, §10.38 | 02, 16 |
| Federal Reserve / OCC payments examiner | Fedwire / ACH cross-institution integrity | §10.21.3, §10.71 | 04, 12, 20 |
| DCMA contracting officer | Defense supply-chain compliance | §10.21, §10.56-§10.61 | 03, 18 |
| DCAA defense audit | Defense cost / property accounting | §10.13, §10.19, §10.56-§10.59 | 03, 18 |
| JCDSO / NSA cross-domain oversight | Red/black separation, cross-domain transition | §5.0.1, §10.62, §10.62.1, §10.62.2 | 18 |
| AISI / NIST AISI safety evaluator | Frontier-model pre-deployment evaluation | §10.63-§10.68 | 19 |
| AISI coordinated-observer-program lead | Observer-stakeholder seating, reciprocity | §10.67, §10.68 | 19 |
| State insurance department examiner (NAIC) | AI-decisioning evidence in personal-lines, claims | §4.4.2, §4.4.5, §10.11, §10.21, §10.43-§10.46 | 15 |
| State attorney general | Consumer-protection division | §1.2, §10.11, §10.22, §10.23 | 04, 07 |
| Department of Education OCR | Title VI/IX civil-rights enforcement | §4.4.5, §10.11, §10.22 | 07 |
| CPSC consumer-products inspector | 24-hour recall readiness | §10.13, §10.19, §10.21.1 | 10 |
| EU AI Act regulator / GDPR DPA | EU AI Act conformity, GDPR Art. 25 / 32 | §10.21, §10.22, §10.38 | 11 |
| Bank of Israel + ISA + INCD | Israeli triplet under nation-state threat model | §1.3, §1.4, §10.5, §10.7, §10.17, §10.21 | 08 |
| PIPA + PDPA + FSS + Taiwan FSC | Korea/Taiwan multi-jurisdiction | §10.22, §10.38, §A.4 | 09 |
| RBI + DPDP DPO | India microfinance + edge-AI consent | §10.32-§10.38 | 13 |
| BaFin / CNIL | Germany / France financial + privacy | §10.21, §10.22, §10.38 | 11 |
| FINMA-equivalent (Helvetian inquiry) | Parliamentary-inquiry-context government AI | §10.51-§10.55 | 17 |
| CBP customs / trade examiner | Import-entry filing AI, bonded-carrier handoff | §10.13, §10.19 | 10 |
| CMMC C3PAO assessor | CMMC 2.0 Level 2/3 assessment | §10.61, §10.56-§10.60 | 03, 18 |
| SOC 1 / SOC 2 engagement team | Section 4 description, control-evidence schema | §7, §10.2, §10.13, §10.18, §10.19 | 02, 04, 14, 16, 20 |
| Big-Four assurance audit | Cross-framework attestation | §7, §10.12, §10.13, §10.18 | 04, 11, 14, 16, 20 |
| Financial-statement auditor | ICFR support; chain as control-evidence input | §10.2, §10.13, §10.18 | 01, 04, 14, 20 |
| IT due-diligence lead (M&A) | Buyer-side IT diligence | §10.19, §10.21, §10.24, §10.39-§10.42 | 14, 20 |
| Cryptographic expert witness (Daubert) | Civil/criminal litigation testimony | §1.1, §1.3, §1.4, §4.1, §4.2, §4.3, §10.5 | 07, 14, 16, 17 |
| Forensic accounting / litigation-support | Evidence preservation, FRE 902(13)/(14) | §5.2, §10.13, §10.69, §10.70 | 16, 20 |
| Independent loss adjuster (insurance) | Cross-anchor on adjuster activity | §10.43, §10.45, §10.46 | 15 |
| Civil-rights firm investigator | Disparate-impact, Title VI/VII | §4.4.5, §10.11, §10.22 | 07 |
| SDK implementer | Capture-side library author | §3, §4.1, §4.4, §4.4.6, §5, §10.25, §A.1 | 04, 12, 13 |
| Ledger implementer | Ingestion + seal job + HSM root signature | §4.2, §4.3, §6, §10.3, §10.25 | 04, 12, 13 |
| Verifier implementer | §7 verifier (reference or clean-room) | §7, §10.12, §10.26, §11 | 04, 12, 14, 16, 17 |
| Reference-verifier user / OSS adopter | Distributes / runs the published verifier | §10.12, §10.26, §11 | 01, 04, 14, 20 |
| AI vendor product-engineering team | Builds AI features that must be chain-instrumented | §4.4.1, §4.4.2, §10.21, §10.33, §10.47-§10.50, §10.63-§10.67 | 08, 11, 13, 16, 19 |
| Bank end-customer (§1033 requestor) | Requests own customer-data subset disclosure | §10.23, §10.69 | 20 |
| Counterparty bank (Fedwire/ACH cross-anchor) | Cross-institution wire/ACH integrity | §10.21.3, §10.71 | 20 |
| Cedent / reinsurer / retrocessionaire | Multi-party claim flow | §10.43-§10.46 | 15 |
| Model provider / AI vendor (cross-anchor) | Cross-vendor anchor counterparty | §10.21, §10.21.2, §10.40 | 11, 14 |
| Acquirer-side technical lead | Post-close technical absorption | §10.24, §10.39-§10.42 | 14, 20 |
| Acquired-entity transition team | Pre-close cooperation, baseline-diary evidence | §10.39, §10.42 | 14, 20 |
| Standards-body reviewer | FFIEC working-group, NIST, ISO observers | §0, §1.1, §1.2, §11, §12 | 12, 13, 18, 19 |
| Academic researcher | Cryptographic / governance-research reading | §1.1-§1.5, §9, §11 | 17, 19 |
| Civil society / public-interest reviewer | Transparency-overlay readers | §10.51, §10.52, §10.55 | 17 |

## Detailed personas

### Audit Committee chair / Board Risk Committee
**Role.** Board-level oversight; sets the committee's expectation of what evidence the chain provides and what it does not. Reads to confirm the chain is a control layer the committee can rely on without becoming cryptographers.
**Sections.** §0.5.3 (per-role triage), §1.1 (Daubert grounding the committee can cite), §1.2 (epistemic scope — what the chain does not prove), §13 (committee entry).
**Stories.** 01 (clean baseline), 04 (multi-tenant coordinated-examiner room), 14 (M&A integrity), 20 (acquisition close, recusal-protocol sunset).
**Companion document outside the spec.** `docs/audit-committee-summary.md`.

### Chief Audit Executive (CAE) / internal audit team
**Role.** Owns independent verification of chain controls; signs the engagement letter and partners with external auditors and examiners. Reads to scope testing, design control evaluations, and brief the audit committee.
**Sections.** §7 (verification procedure), §10.12 (verifier exit codes), §10.13 (evidentiary-artifact retention), §10.18 (CC8.1 cross-referencing), §10.19 (chain-coverage boundary), §13.
**Stories.** 01-20 — every story exercises this persona; the audit-team is the canonical CAE-side reader.
**Companion document outside the spec.** `docs/internal-audit-evidence-pack.md`, `docs/audit-procedures.md`, `docs/audit-procedures-cluster-d-addenda.md`.

### Chief Information Security Officer (CISO)
**Role.** Owns the institutional cyber-posture and threat model; cares about HSM custody, IR posture, and supply-chain trust path. Reads to confirm the chain composes with broader cyber controls and to size IR/DR for chain-detected events.
**Sections.** §1.3 (security definitions), §1.4 (compositional security), §4.3 (HSM-rooted signature), §10.5 (HSM custody), §10.7 (software-key adapter exclusion), §10.17 (HSM partition ceremony attestation).
**Stories.** 04 (multi-tenant scale), 06 (utility public-safety stakes), 08 (nation-state threat model), 12 (real-time fraud), 18 (defense-electronics red/black).
**Companion document outside the spec.** `docs/design/09-threat-model.md`, `docs/regulator-pack/CSF-2.0.md`, `docs/incident-response-playbook.md`.

### Chief Compliance Officer / Chief Risk Officer
**Role.** Multi-framework regulatory posture; reads the chain as a cross-framework control. Briefs CFPB / state DOI / international DPA examiners; owns the ECOA / FCRA / fair-lending / privacy-rights surface.
**Sections.** §10.11 (adverse-action translation), §10.19 (chain-coverage boundary), §10.21 (cross-vendor model handover), §10.22 (redaction), §10.23 (CID-class production), §13.
**Stories.** 02 (HIPAA + FDA), 04 (multi-regulator coordinated room), 07 (lawsuit-motivated AI screening), 09 (Korea + Taiwan triplet), 13 (RBI + DPDP), 17 (parliamentary inquiry).
**Companion document outside the spec.** `docs/regulator-pack/cfpb-overlay.md`, `docs/regulator-pack/multi-jurisdiction-conflict.md`.

### Model Risk Management committee chair
**Role.** SR 11-7 model lifecycle; reads the chain as the integrity substrate under model documentation, validation, and ongoing monitoring. Particularly attentive to deployment-intent capture, training-corpus integrity, and pre-deployment evaluation.
**Sections.** §1.1, §1.5 (decision-event vs state-machine), §4.4.2 (deployment intent), §10.20 (training-data retention), §10.21 (cross-vendor handover), §10.66 (model-weight lineage), §10.67 (pre-deployment evaluation).
**Stories.** 02 (clinical decision support), 06 (gas-pipeline leak detection), 07 (admissions AI), 16 (generative-AI clinical summary), 19 (frontier-model training).
**Companion document outside the spec.** `docs/MRM-COMMITTEE-BRIEF.md`.

### Chief AI / ML Officer (and Chief Data Officer where distinct)
**Role.** Owns the institution's AI estate; co-owns chain instrumentation for routing, deployment intent, training, and inference. Reads to scope SDK adoption, vendor cross-anchors, and the GenAI / federated-learning / training-provenance families.
**Sections.** §4.4.1 (routing), §4.4.2 (deployment intent), §10.20-§10.21 (training data, cross-vendor handover), §10.33 (model update), §10.47-§10.50 (GenAI four-tuple), §10.63-§10.67 (training provenance).
**Stories.** 02, 06, 07, 13 (federated-learning edge), 16 (GenAI clinical summary), 19 (frontier-model training).
**Companion document outside the spec.** `docs/edge-and-federated-ai.md`, `docs/AI-safety-evaluation-overlay.md`, `docs/regulator-pack/ai-policy-alignment.md`.

### General Counsel / institution legal team
**Role.** Owns legal-process posture: court-ordered disclosure, customer disputes, malpractice discovery, parliamentary-inquiry response, and litigation hold. Reads for evidentiary defensibility and FRE / FRCP alignment.
**Sections.** §1.1 (Daubert), §5.2 (best-evidence under FRE 1001-1004), §10.13 (evidentiary-artifact retention), §10.55 (challenge-response), §10.69 (per-customer subset disclosure), §10.70 (BSA SAR / privileged-investigation).
**Stories.** 07 (civil-rights litigation context), 14 (M&A counsel), 16 (malpractice discovery), 17 (parliamentary inquiry), 20 (acquisition + customer §1033 production).
**Companion document outside the spec.** `docs/legal-disclosure.md`, `docs/litigation-support.md`, `docs/templates/fre-902-certification.md`.

### Privacy Officer / Data Protection Officer
**Role.** GDPR, DPDP, CCPA, PIPA, PDPA alignment; tokenization architecture; consent capture; subject-access-request fulfillment. Reads for redaction discipline, consent lifecycle, and customer-rights flow.
**Sections.** §10.22 (redaction), §10.23 (consumer-correlation index), §10.38 (consent capture), §10.69 (per-customer subset disclosure).
**Stories.** 07 (admissions AI redaction), 09 (Korea + Taiwan), 11 (Germany + France EU AI Act), 13 (DPDP consent), 17 (Helvetian transparency overlay).
**Companion document outside the spec.** `docs/privacy-by-design.md`, `docs/regulator-pack/gdpr-dpia-template.md`, `docs/regulator-pack/gdpr-dsar-fulfillment.md`, `docs/regulator-pack/gdpr-article-17-procedures.md`, `docs/regulator-pack/ccpa-cpra-rights.md`, `docs/regulator-pack/childrens-data-safeguards.md`.

### DevSecOps / SRE on-call
**Role.** Owns runtime: NTP discipline, cloud HSM provisioning, multi-region resilience, run-resume after DR, IR for chain-detected events. Reads for the operational-event vocabulary and the boundary between conformant and non-conformant operational responses.
**Sections.** §4.3.1 (HSM unavailability + 72-hour notification), §10.4 (time sync), §10.15 (multi-region resilience), §10.16 (SaaS-edge connector SLO), §10.25 (run resume / chain-tail acquisition).
**Stories.** 06 (real-time public-safety alert), 12 (sub-100ms streaming), 14 (cut-over window), 18 (defense supply chain).
**Companion document outside the spec.** `docs/operator-guide.md`, `docs/cloud-hsm-guide.md`, `docs/byoc-deployment.md`, `docs/dr-and-resilience.md`, `docs/at-scale-operations.md`, `docs/incident-response-playbook.md`.

### Vendor management lead
**Role.** Vendor-hosted control evaluation, BYOC topology, supply-chain trust path, M&A vendor changes. Reads for vendor-conformance attestation procedures and cross-vendor-anchor patterns.
**Sections.** §10.16 (SaaS-edge connectors), §10.21 (cross-vendor model handover), §10.26 (reference-verifier distribution), §10.40 (cross-vendor chain-merge cross-anchor), §10.56-§10.60 (supply-chain hardware).
**Stories.** 03 (DoD prime + commercial vendors), 08 (Israeli AI vendor), 11 (Germany + France cross-vendor), 14 (M&A target's prior vendor), 18 (defense electronics).
**Companion document outside the spec.** `docs/vendor-hosted-controls.md`, `docs/vendor-conformance-attestation.md`, `docs/supply-chain.md`, `docs/herald-vendor-conformance-round-5-response.md`.

### M&A integration lead (acquirer-side and acquired-entity-side)
**Role.** Reads to scope the evidence trail surviving acquisition. Acquirer-side: scope diligence and design the cut-over plan. Acquired-entity-side: prepare baseline-diary inheritance and cooperate with the §10.39 successor-attestation ceremony.
**Sections.** §10.19, §10.21, §10.24 (entity succession), §10.39 (successor attestation), §10.40-§10.42 (cross-vendor merge, M&A coverage map, backfill seal).
**Stories.** 14 (Northbridge return — Cape Madeline acquisition), 20 (Northbridge acquires TesseraSeal — vendor-to-bank).
**Companion document outside the spec.** `docs/m-and-a-handoff.md`.

### FFIEC IT Examiner (FDIC / OCC / FRB)
**Role.** Cycle examiner reading the chain for first-time orientation, finding language, and report production. Reads to size cadence-relaxation requests and cross-bank comparisons.
**Sections.** §1.1, §1.2, §7, §10.12, §10.18, §13.
**Stories.** 01 (single-tenant baseline), 04 (multi-tenant), 12 (streaming-mode wishlist), 14 (M&A), 20 (acquisition close).
**Companion document outside the spec.** `docs/examiner-quickstart.md`, `docs/regulator-pack/examiner-training.md`, `docs/regulator-pack/sample-report.md`, `docs/regulator-pack/finding-language.md`, `docs/regulator-pack/handbook-mapping.md`, `docs/regulator-pack/deployment-package.md`, `docs/regulator-pack/examiner-approval-template.md`, `docs/regulator-pack/fdic-occ-examination-overlay.md`.

### FFIEC Cybersecurity Specialist Examiner
**Role.** NIST CSF 2.0 alignment, threat-model review, supply-chain controls, AI policy, emerging tech.
**Sections.** §1.3, §1.4, §10.5, §10.7, §10.17, §10.21, §10.56-§10.62.
**Stories.** 04 (BaaS multi-tenant), 08 (nation-state threat model), 12 (streaming), 18 (defense red/black).
**Companion document outside the spec.** `docs/regulator-pack/CSF-2.0.md`, `docs/regulator-pack/fedramp-fisma-overlay.md`, `docs/regulator-pack/nydfs-part500-overlay.md`, `docs/design/09-threat-model.md`.

### FFIEC Examiner-in-Charge (EIC)
**Role.** Examination logistics, finding language, repeat-finding posture, public-disclosure variants, and bank-management communication.
**Sections.** §7, §10.12, §10.18, §10.19, §13.
**Stories.** 01, 04, 12, 14, 20.
**Companion document outside the spec.** `docs/regulator-pack/sample-report.md`, `docs/regulator-pack/finding-language.md`, `docs/regulator-pack/examiner-approval-template.md`, `docs/first-engagement-guide.md`, `docs/portfolio-comparison-procedures.md`.

### CFPB consumer-protection examiner
**Role.** §1033 customer-data right, ECOA / FCRA, dispute response, customer-correlation-index production. Reads for translation discipline and adverse-action evidentiary anchors.
**Sections.** §10.11, §10.11.1, §10.11.2, §10.23, §10.69.
**Stories.** 04 (BaaS coordinated-examiner room), 07 (admissions AI), 20 (§1033 customer subset).
**Companion document outside the spec.** `docs/regulator-pack/cfpb-overlay.md`, `docs/customer-dispute-procedures.md`.

### FTC AI / privacy examiner
**Role.** UDAP enforcement, AI-driven consumer harm, deceptive-AI claims. Reads for routing-decision evidence and deployment-intent capture.
**Sections.** §1.1, §1.2, §4.4.1, §4.4.2, §10.21.
**Stories.** 04 (BaaS), 07 (admissions AI civil-rights threat letter), 12 (payments-network FTC inquiry).
**Companion document outside the spec.** `docs/regulator-pack/ai-policy-alignment.md`.

### FDA Bioresearch Monitoring (BIMO) inspector
**Role.** Clinical-trial integrity, ALCOA+ alignment, AI clinical decision support. Reads to confirm the chain meets ALCOA+ attribute-by-attribute.
**Sections.** §1.1, §10.13, §10.20, §10.47-§10.50.
**Stories.** 02 (Mercator sepsis CDS), 05 (Helmstad clinical-trial eligibility), 16 (Lyceum generative clinical summary).
**Companion document outside the spec.** `docs/regulator-pack/healthcare-overlay.md`, `docs/regulator-pack/healthcare-genai-overlay.md`.

### HHS Office for Civil Rights (HIPAA)
**Role.** PHI integrity and security-rule mapping; minimum-necessary discipline.
**Sections.** §10.5, §10.22, §10.38.
**Stories.** 02 (Mercator), 16 (Lyceum).
**Companion document outside the spec.** `docs/regulator-pack/hipaa-security-rule-mapping.md`, `docs/regulator-pack/hipaa-minimum-necessary.md`.

### Federal Reserve / OCC payments examiner (Fedwire / ACH)
**Role.** Cross-institution wire / ACH chain integrity. Reads for the registry-discovery cross-anchor pattern.
**Sections.** §10.21.3, §10.71.
**Stories.** 04 (BaaS sponsor-bank flow), 12 (payments network), 20 (Fedwire / ACH cross-institution).
**Companion document outside the spec.** `docs/regulator-pack/bsa-aml-overlay.md`.

### DCMA contracting officer / DCAA defense audit
**Role.** Defense supply-chain and cost-accounting compliance. Reads for hardware bill-of-materials integrity and CMMC overlay.
**Sections.** §10.13, §10.19, §10.21, §10.56-§10.61.
**Stories.** 03 (Stelvio DoD prime), 18 (Argent Vector defense electronics).
**Companion document outside the spec.** `docs/supply-chain.md`.

### JCDSO / NSA cross-domain oversight
**Role.** Red/black separation, cross-domain transition oversight. Reads for the `cross_domain_transition` wire-format kind and releasability-projection determinism.
**Sections.** §5.0.1, §10.62, §10.62.1, §10.62.2.
**Stories.** 18 (TALON-X program review).
**Companion document outside the spec.** *(none current; spec §10.62 is the normative source.)*

### AISI / NIST AISI safety evaluator
**Role.** Frontier-model pre-deployment evaluation under the AISI Reference Evaluation Program.
**Sections.** §10.63 (training-corpus provenance), §10.64 (training-run code/config), §10.65 (GPU-fleet attestation), §10.66 (model-weight lineage), §10.67 (pre-deployment evaluation chain), §10.68 (AISI overlay).
**Stories.** 19 (Aerolith Compute — first regulator-equivalent in the wishlist-drafting room).
**Companion document outside the spec.** `docs/AI-safety-evaluation-overlay.md`.

### AISI coordinated-observer-program lead
**Role.** Sets the observer-letter posture, reciprocity, and submission cadence.
**Sections.** §10.67, §10.68.
**Stories.** 19.
**Companion document outside the spec.** `docs/AI-safety-evaluation-overlay.md`.

### State insurance department market-conduct examiner (NAIC)
**Role.** AI-decisioning evidence in personal-lines underwriting, claims triage, pricing, and rate filings. Reads for deployment-intent (rate-filing-id, SERFF), underwriting-feature recording, disparate-impact testing, and multi-party claim flow.
**Sections.** §4.4.2, §4.4.5, §10.11, §10.21, §10.43-§10.46.
**Stories.** 15 (Polaris × Lloyd's NAIC market-conduct wave).
**Companion document outside the spec.** `docs/regulator-pack/naic-market-conduct-overlay.md`.

### State attorney general / consumer-protection division
**Role.** State-level UDAP and consumer-protection enforcement.
**Sections.** §1.2, §10.11, §10.22, §10.23.
**Stories.** 04, 07.
**Companion document outside the spec.** `docs/regulator-pack/cfpb-overlay.md` (state-coordination notes).

### Department of Education OCR
**Role.** Title VI / IX civil-rights enforcement in higher-education AI screening.
**Sections.** §4.4.5 (disparate-impact), §10.11, §10.22.
**Stories.** 07 (Olmstead admissions AI).
**Companion document outside the spec.** *(closest is the civil-rights guidance threaded through `docs/regulator-pack/ai-policy-alignment.md`.)*

### CPSC consumer-products safety inspector
**Role.** 24-hour recall readiness and import-cert anchor verification.
**Sections.** §10.13, §10.19, §10.21.1 (lot-level binding via independent attestation).
**Stories.** 10 (Salt Pond toys).
**Companion document outside the spec.** *(supply-chain-side guidance threaded through `docs/supply-chain.md`.)*

### EU AI Act regulator / GDPR DPA
**Role.** EU AI Act conformity assessment, GDPR Articles 25 and 32 demonstrability.
**Sections.** §10.21, §10.22, §10.38.
**Stories.** 11 (Eberhardt × Lumière Germany + France).
**Companion document outside the spec.** `docs/regulator-pack/eu-articulation-extension.md`, `docs/regulator-pack/dora-articulation-overlay.md`, `docs/regulator-pack/article-32-security-mapping.md`, `docs/regulator-pack/gdpr-article-25-demonstrability.md`, `docs/regulator-pack/gdpr-controller-vs-processor.md`, `docs/regulator-pack/gdpr-lawful-basis.md`, `docs/regulator-pack/international-transfers.md`, `docs/regulator-pack/pseudonymization-vs-anonymization.md`, `docs/regulator-pack/breach-notification-matrix.md`, `docs/regulator-pack/gdpr-ropa-template.md`, `docs/regulator-pack/gdpr-article-16-rectification.md`, `docs/regulator-pack/retention-justification.md`, `docs/regulator-pack/gdpr-dpo-consultation.md`.

### Bank of Israel + ISA + INCD (Israeli triplet)
**Role.** Coordinated supervision of Israeli AI vendors under nation-state threat model.
**Sections.** §1.3, §1.4, §10.5, §10.7, §10.17, §10.21.
**Stories.** 08 (NetiVa Tel Aviv).
**Companion document outside the spec.** `docs/regulator-pack/bank-of-israel-overlay.md`.

### PIPA (Korea) + PDPA (Taiwan) + FSS + Taiwan FSC
**Role.** Korea / Taiwan multi-jurisdiction supervision (privacy, financial supervisor, exchange listing).
**Sections.** §10.22, §10.38, §A.4 (cross-border transfer family).
**Stories.** 09 (Sun-Won Cosmetics Korea + Taiwan).
**Companion document outside the spec.** `docs/regulator-pack/korea-overlay.md`, `docs/regulator-pack/apac-overlay.md`.

### RBI + DPDP DPO (India)
**Role.** Indian banking and DPDP Act privacy supervision; consent-capture posture for federated edge-AI.
**Sections.** §10.32-§10.38.
**Stories.** 13 (Saraswati Microfinance edge-AI).
**Companion document outside the spec.** `docs/regulator-pack/apac-overlay.md`.

### BaFin / CNIL (Germany / France)
**Role.** Germany financial supervisor + France privacy supervisor; cross-vendor partnership oversight.
**Sections.** §10.21, §10.22, §10.38.
**Stories.** 11 (Eberhardt × Lumière).
**Companion document outside the spec.** `docs/regulator-pack/eu-articulation-extension.md`.

### FINMA-equivalent (Helvetian parliamentary-inquiry context)
**Role.** Parliamentary-inquiry oversight of government AI-decisioning under long retention horizons.
**Sections.** §10.51 (public transparency), §10.52 (model-card binding), §10.53 (hybrid PQ seal), §10.54 (decadal re-sealing), §10.55 (challenge-response).
**Stories.** 17 (Helvetian Federal Tax Authority).
**Companion document outside the spec.** `docs/cryptographic-agility-roadmap.md`.

### CBP customs / trade examiner
**Role.** Import-entry filing AI integrity and bonded-carrier handoff documentation.
**Sections.** §10.13, §10.19.
**Stories.** 10 (Salt Pond customs-entry filing).
**Companion document outside the spec.** *(coverage threaded through `docs/supply-chain.md` and `docs/legal-disclosure.md`.)*

### CMMC C3PAO assessor
**Role.** CMMC 2.0 Level 2 / 3 assessment, NIST SP 800-171 / 800-161 control evaluation.
**Sections.** §10.61 (CMMC overlay framework), §10.56-§10.60 (supply-chain integrity).
**Stories.** 03 (Stelvio DoD prime), 18 (Argent Vector).
**Companion document outside the spec.** `docs/supply-chain.md`.

### SOC 1 / SOC 2 engagement team
**Role.** Section 4 description, control-evidence schema, audit procedures, anomaly evaluation, CUEC verification.
**Sections.** §7, §10.2 (operational events), §10.13, §10.18, §10.19.
**Stories.** 02, 04, 14, 16, 20.
**Companion document outside the spec.** `docs/soc-pack/section-4-template.md`, `docs/soc-pack/control-evidence-events.md`, `docs/control-map/TSC-mapping.md`, `docs/control-map/CUECs.md`, `docs/templates/soc2-section3-description-of-system.md`, `docs/templates/soc2-control-matrix.md`, `docs/anomaly-documentation-template.md`, `docs/user-entity-summary.md`.

### Big-Four assurance audit
**Role.** Cross-framework attestation engagements: SOC, ISAE, ISO 27001 / 42001, integrated reporting.
**Sections.** §7, §10.12, §10.13, §10.18.
**Stories.** 04, 11, 14, 16, 20.
**Companion document outside the spec.** `docs/audit-procedures.md`, `docs/control-map/TSC-mapping.md`.

### Financial-statement auditor
**Role.** ICFR support; chain entries as control-evidence inputs to financial-statement audit.
**Sections.** §10.2, §10.13, §10.18.
**Stories.** 01, 04, 14, 20.
**Companion document outside the spec.** `docs/audit-procedures.md`, `docs/templates/records-management-program.md`.

### IT due-diligence lead (M&A)
**Role.** Buyer-side IT diligence on a target's chain. Per spec §13's "Acquirer-side IT due-diligence" entry.
**Sections.** §10.19, §10.21, §10.24, §10.39-§10.42.
**Stories.** 14, 20.
**Companion document outside the spec.** `docs/m-and-a-handoff.md`.

### Cryptographic expert witness (Daubert testimony)
**Role.** Civil and criminal litigation testimony on chain integrity, threat model, and HSM custody. Per spec §13's "Cryptographic expert" entry.
**Sections.** §1.1, §1.3, §1.4, §4.1 (HMAC chain), §4.2 (Merkle seal), §4.3 (HSM signature), §10.5 (HSM custody).
**Stories.** 07 (admissions AI civil-rights litigation context), 14 (M&A integrity), 16 (malpractice discovery), 17 (parliamentary-inquiry independent testimony).
**Companion document outside the spec.** `docs/design/02-chain-construction.md`, `docs/design/03-merkle-seal.md`, `docs/design/04-hsm-custody.md`, `docs/design/09-threat-model.md`, `docs/litigation-support.md`.

### Forensic accounting team / litigation-support
**Role.** Evidence preservation, FRE 902(13) and 902(14) certification, malpractice and fraud investigations.
**Sections.** §5.2, §10.13, §10.69, §10.70.
**Stories.** 16 (clinical malpractice context), 20 (BSA SAR + customer §1033).
**Companion document outside the spec.** `docs/litigation-support.md`, `docs/templates/fre-902-certification.md`.

### Independent loss adjuster (insurance)
**Role.** Cross-anchor on adjuster activity binding the same investigation under multiple parties' chains.
**Sections.** §10.43 (claim-state-machine), §10.45 (adjuster anchor), §10.46 (bordereau).
**Stories.** 15 (Polaris × Lloyd's).
**Companion document outside the spec.** *(coverage threaded through the §10.43-§10.46 family in the spec.)*

### Civil-rights firm investigator (disparate-impact / Title VI/VII)
**Role.** Disparate-impact and civil-rights investigations; reads for underwriting-feature evidence and adverse-action translation.
**Sections.** §4.4.5 (underwriting features + disparate-impact testing), §10.11, §10.22.
**Stories.** 07 (Olmstead admissions AI threat letter).
**Companion document outside the spec.** *(threaded through `docs/regulator-pack/ai-policy-alignment.md`.)*

### SDK implementer
**Role.** Building or porting an SDK that emits chain entries from an application process.
**Sections.** §3 (definitions), §4.1 (HMAC chain), §4.4 (OTel wire), §4.4.6 (connector source attribution), §5 (canonicalization), §10.25 (run resume), §A.1.
**Stories.** 04 (BaaS), 12 (streaming-mode), 13 (per-device session keys).
**Companion document outside the spec.** `docs/design/02-chain-construction.md`.

### Ledger implementer
**Role.** Building or operating a ledger that ingests chain entries, computes Merkle seals, and produces HSM-rooted seal records.
**Sections.** §4.2 (Merkle seal), §4.3 (HSM signature), §6 (storage), §10.3 (append-only), §10.25 (chain-tail acquisition).
**Stories.** 04, 12, 13.
**Companion document outside the spec.** `docs/design/03-merkle-seal.md`, `docs/design/04-hsm-custody.md`, `docs/design/06-ledger-server-design.md`.

### Verifier implementer
**Role.** Building or distributing a §7 verifier (the reference verifier or a clean-room implementation).
**Sections.** §7 (verification procedure), §10.12 (exit-code contract), §10.26 (distribution discipline), §11 (pinned reference release).
**Stories.** 04, 12, 14, 16, 17.
**Companion document outside the spec.** `docs/design/07-verifier-design.md`, `docs/vendor-conformance-attestation.md`.

### Reference-verifier user / OSS adopter
**Role.** Distributes or runs the published reference verifier; Apache 2.0 binary user.
**Sections.** §10.12, §10.26, §11.
**Stories.** 01, 04, 14, 20.
**Companion document outside the spec.** `docs/vendor-conformance-attestation.md`.

### AI vendor product-engineering team
**Role.** Builds AI features that must be chain-instrumented; partners with institution side on cross-anchor design.
**Sections.** §4.4.1, §4.4.2, §10.21 (cross-vendor handover), §10.33 (model-update events), §10.47-§10.50, §10.63-§10.67.
**Stories.** 08 (NetiVa Israeli AI vendor), 11 (Lumière France AI consultancy), 13 (Saraswati edge-AI), 16 (Lyceum generative clinical), 19 (Aerolith frontier-AI lab).
**Companion document outside the spec.** `docs/vendor-conformance-attestation.md`, `docs/edge-and-federated-ai.md`.

### Bank end-customer requesting §1033 disclosure
**Role.** Requests the institution produce a per-customer subset of the audit trail.
**Sections.** §10.23 (CID-class), §10.69 (per-customer subset disclosure with documented exclusions).
**Stories.** 20 (Northbridge §10.69 production).
**Companion document outside the spec.** `docs/customer-dispute-procedures.md`.

### Counterparty bank (Fedwire / ACH cross-anchor)
**Role.** Cross-institution wire / ACH integrity counterparty under the registry-discovery cross-anchor pattern.
**Sections.** §10.21.3, §10.71.
**Stories.** 20.
**Companion document outside the spec.** *(coverage threaded through `docs/regulator-pack/bsa-aml-overlay.md`.)*

### Cedent / reinsurer / retrocessionaire
**Role.** Multi-party claim flow under the §10.43-§10.46 family; bidirectional cross-anchor counterparty.
**Sections.** §10.43-§10.46.
**Stories.** 15 (Polaris × Lloyd's).
**Companion document outside the spec.** *(coverage threaded through the spec §10.43-§10.46 family.)*

### Model provider / AI vendor (cross-vendor anchor)
**Role.** Cross-vendor cross-anchor counterparty for model handovers, parallel-evaluator chains, and chain-merge at M&A close.
**Sections.** §10.21, §10.21.2, §10.40.
**Stories.** 11 (Eberhardt × Lumière live hash-match), 14 (LedgerKnot cross-anchor at Cape Madeline close).
**Companion document outside the spec.** `docs/vendor-conformance-attestation.md`.

### Acquirer-side technical lead
**Role.** Post-close technical absorption of the acquired entity's chain (or baseline-diary) into the acquirer's coverage map.
**Sections.** §10.24, §10.39, §10.40, §10.41, §10.42.
**Stories.** 14, 20.
**Companion document outside the spec.** `docs/m-and-a-handoff.md`.

### Acquired-entity transition team
**Role.** Pre-close cooperation, baseline-diary inheritance, and dual-signature ceremony participation.
**Sections.** §10.39, §10.42.
**Stories.** 14 (Cape Madeline), 20 (TesseraSeal absorbed by Northbridge Technology Services).
**Companion document outside the spec.** `docs/m-and-a-handoff.md`.

### Standards-body reviewer (FFIEC working-group, NIST, ISO)
**Role.** Reviews the spec for normative coherence, alignment with NIST and ISO frameworks, and FFIEC handbook integration.
**Sections.** §0 (versioning), §1.1, §1.2, §11 (references), §12 (change log).
**Stories.** 12 (streaming-mode wishlist memo), 13 (edge / federated wishlist memo), 18 (supply-chain + red/black wishlist memo), 19 (frontier-model training-provenance wishlist memo).
**Companion document outside the spec.** `docs/regulator-pack/handbook-mapping.md`, `docs/INDEX.md`.

### Academic researcher
**Role.** Cryptographic, governance, or AI-safety research reading the spec as a reference architecture.
**Sections.** §1.1-§1.5, §9 (security considerations), §11.
**Stories.** 17 (parliamentary-inquiry context), 19 (AISI partnership).
**Companion document outside the spec.** `docs/design/00-overview.md`, `docs/design/09-threat-model.md`.

### Civil society / public-interest reviewer
**Role.** Transparency-overlay reader; verifies public DP-noised aggregates and challenge-response disposition records.
**Sections.** §10.51 (public transparency), §10.52 (model-card binding), §10.55 (challenge-response).
**Stories.** 17 (Helvetian Federal Tax Authority public transparency).
**Companion document outside the spec.** *(public-side coverage threaded through the §10.51-§10.55 family in the spec.)*

## Persona-to-story matrix

A cross-reference matrix: which stories are most useful for which persona, given the deployment context and stakes. Rows are personas; columns are auditor stories 01-20. Mark `T` for "high relevance" and leave blank for "low/no relevance".

| Persona | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Audit Committee chair | ✓ | | | ✓ | | | | | | | | | | ✓ | | | | | | ✓ |
| Chief Audit Executive | ✓ | | | ✓ | | | | | | | | | | ✓ | | ✓ | | | | ✓ |
| Internal audit team | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CISO | | | | ✓ | | ✓ | | ✓ | | | | ✓ | | | | | | ✓ | | |
| Chief Compliance Officer / CRO | | ✓ | | ✓ | | | ✓ | | ✓ | | | | ✓ | | | | ✓ | | | |
| Model Risk Management chair | | ✓ | | | | ✓ | ✓ | | | | | | | | | ✓ | | | ✓ | |
| Chief AI / ML Officer | | ✓ | | | | ✓ | ✓ | | | | | | ✓ | | | ✓ | | | ✓ | |
| Chief Data Officer | | | | | | | ✓ | | | | | | ✓ | | | | | | ✓ | |
| General Counsel | | | | | | | ✓ | | | | | | | ✓ | | ✓ | ✓ | | | ✓ |
| Privacy Officer / DPO | | | | | | | ✓ | | ✓ | | ✓ | | ✓ | | | | ✓ | | | |
| DevSecOps / SRE on-call | | | | | | ✓ | | | | | | ✓ | | ✓ | | | | ✓ | | |
| Vendor management lead | | | ✓ | | | | | ✓ | | | ✓ | | | ✓ | | | | ✓ | | |
| M&A integration lead (acquirer) | | | | | | | | | | | | | | ✓ | | | | | | ✓ |
| M&A integration lead (acquired entity) | | | | | | | | | | | | | | ✓ | | | | | | ✓ |
| FFIEC IT Examiner | ✓ | | | ✓ | | | | | | | | ✓ | | ✓ | | | | | | ✓ |
| FFIEC Cybersecurity Specialist Examiner | | | | ✓ | | | | ✓ | | | | ✓ | | | | | | ✓ | | |
| FFIEC Examiner-in-Charge | ✓ | | | ✓ | | | | | | | | ✓ | | ✓ | | | | | | ✓ |
| CFPB consumer-protection examiner | | | | ✓ | | | ✓ | | | | | | | | | | | | | ✓ |
| FTC AI / privacy examiner | | | | ✓ | | | ✓ | | | | | ✓ | | | | | | | | |
| FDA BIMO inspector | | ✓ | | | ✓ | | | | | | | | | | | ✓ | | | | |
| HHS OCR (HIPAA) | | ✓ | | | | | | | | | | | | | | ✓ | | | | |
| Federal Reserve / OCC payments examiner | | | | ✓ | | | | | | | | ✓ | | | | | | | | ✓ |
| DCMA / DCAA defense audit | | | ✓ | | | | | | | | | | | | | | | ✓ | | |
| JCDSO / NSA cross-domain oversight | | | | | | | | | | | | | | | | | | ✓ | | |
| AISI / NIST AISI safety evaluator | | | | | | | | | | | | | | | | | | | ✓ | |
| AISI coordinated-observer-program lead | | | | | | | | | | | | | | | | | | | ✓ | |
| State insurance department examiner (NAIC) | | | | | | | | | | | | | | | ✓ | | | | | |
| State attorney general | | | | ✓ | | | ✓ | | | | | | | | | | | | | |
| Department of Education OCR | | | | | | | ✓ | | | | | | | | | | | | | |
| CPSC consumer-products inspector | | | | | | | | | | ✓ | | | | | | | | | | |
| EU AI Act regulator / GDPR DPA | | | | | | | | | | | ✓ | | | | | | | | | |
| Bank of Israel + ISA + INCD | | | | | | | | ✓ | | | | | | | | | | | | |
| PIPA + PDPA + FSS + Taiwan FSC | | | | | | | | | ✓ | | | | | | | | | | | |
| RBI + DPDP DPO | | | | | | | | | | | | | ✓ | | | | | | | |
| BaFin / CNIL | | | | | | | | | | | ✓ | | | | | | | | | |
| FINMA-equivalent (Helvetian inquiry) | | | | | | | | | | | | | | | | | ✓ | | | |
| CBP customs / trade examiner | | | | | | | | | | ✓ | | | | | | | | | | |
| CMMC C3PAO assessor | | | ✓ | | | | | | | | | | | | | | | ✓ | | |
| SOC 1 / SOC 2 engagement team | | ✓ | | ✓ | | | | | | | | | | ✓ | | ✓ | | | | ✓ |
| Big-Four assurance audit | | | | ✓ | | | | | | | ✓ | | | ✓ | | ✓ | | | | ✓ |
| Financial-statement auditor | ✓ | | | ✓ | | | | | | | | | | ✓ | | | | | | ✓ |
| IT due-diligence lead (M&A) | | | | | | | | | | | | | | ✓ | | | | | | ✓ |
| Cryptographic expert witness | | | | | | | ✓ | | | | | | | ✓ | | ✓ | ✓ | | | |
| Forensic accounting / litigation-support | | | | | | | | | | | | | | | | ✓ | | | | ✓ |
| Independent loss adjuster | | | | | | | | | | | | | | | ✓ | | | | | |
| Civil-rights firm investigator | | | | | | | ✓ | | | | | | | | | | | | | |
| SDK implementer | | | | ✓ | | | | | | | | ✓ | ✓ | | | | | | | |
| Ledger implementer | | | | ✓ | | | | | | | | ✓ | ✓ | | | | | | | |
| Verifier implementer | | | | ✓ | | | | | | | | ✓ | | ✓ | | ✓ | ✓ | | | |
| Reference-verifier user / OSS adopter | ✓ | | | ✓ | | | | | | | | | | ✓ | | | | | | ✓ |
| AI vendor product-engineering team | | | | | | | | ✓ | | | ✓ | | ✓ | | | ✓ | | | ✓ | |
| Bank end-customer (§1033 requestor) | | | | | | | | | | | | | | | | | | | | ✓ |
| Counterparty bank (Fedwire / ACH) | | | | | | | | | | | | | | | | | | | | ✓ |
| Cedent / reinsurer / retrocessionaire | | | | | | | | | | | | | | | ✓ | | | | | |
| Model provider / AI vendor (cross-anchor) | | | | | | | | | | | ✓ | | | ✓ | | | | | | |
| Acquirer-side technical lead | | | | | | | | | | | | | | ✓ | | | | | | ✓ |
| Acquired-entity transition team | | | | | | | | | | | | | | ✓ | | | | | | ✓ |
| Standards-body reviewer | | | | | | | | | | | | ✓ | ✓ | | | | | ✓ | ✓ | |
| Academic researcher | | | | | | | | | | | | | | | | | ✓ | | ✓ | |
| Civil society / public-interest reviewer | | | | | | | | | | | | | | | | | ✓ | | | |
