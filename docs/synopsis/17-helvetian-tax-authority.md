# Story 17 — Helvetian Federal Tax Authority (civic-AI parliamentary-inquiry CONFIRMATION)

**Story file:** `docs/auditor-stories/17-helvetian-tax-authority.md`
**Engagement type:** Three-day vendor-side spec-section confirmation pass at the Helvetian Federal Tax Authority headquarters in Bern, scheduled eleven weeks before a parliamentary inquiry committee opens hearings on AI-augmented administrative-law decisions.
**Posture going in:** Confirmation — §10.51-§10.55 shipped in vendor release N+3 six months prior; agency upgraded five months in; one full quarterly public-transparency reporting cycle complete.
**Outcome posture:** Confirmation.

## Type of audit
A vendor-side confirmation engagement at parliamentary scale. The team verifies §10.51 public-transparency overlay, §10.52 public model-card binding, §10.53 hybrid post-quantum seal mandate, §10.54 decadal re-sealing discipline, and §10.55 audit-target challenge-response procedure across an AI-augmented VAT audit-target selection system in production for two years. The 60-year retention horizon (Swiss tax archive law) makes §10.53 normative-when-applicable.

## Interested parties (spec readers)
- **FINMA-equivalent (Helvetian parliamentary-inquiry context)** — parliamentary-inquiry oversight of government AI-decisioning under long retention horizons; reads §10.51-§10.55.
- **Civil society / public-interest reviewer** — transparency-overlay reader; verifies public DP-noised aggregates and challenge-response disposition records via §10.51, §10.52, §10.55.
- **Standards-body reviewer** — post-quantum migration coherence; reads §4.3.2, §10.53, §10.54 for normative alignment with NIST FIPS 204 and ISO PQC migration guidance.
- **General Counsel** — parliamentary-inquiry-response posture and FRE / FRCP-equivalent evidentiary defensibility; reads §1.1, §5.2, §10.55.
- **Chief AI / ML Officer** — civic-AI deployment-intent author; reads §10.51-§10.55 plus §4.4.2 for parliamentary-inquiry-grade deployment-intent capture.
- **Chief Compliance Officer / CRO** — multi-framework regulatory posture under parliamentary-inquiry conditions; reads §10.21-§10.23 plus §13.
- **Privacy Officer / Data Protection Officer** — Council of Europe Convention 108+ alignment; reads §10.22, §10.38 for redaction discipline and consent capture.
- **Cryptographic expert witness (Daubert)** — independent parliamentary-inquiry testimony; reads §1.1, §1.3, §1.4, §4.1-§4.3, §10.5, §10.53.
- **Verifier implementer** — post-quantum dual-signature dispatch path under §7 Steps 7 and 11; reads §10.53.
- **Academic researcher** — parliamentary-inquiry context as governance-research reference; reads §1.1-§1.5, §9, §11.
- **Big-Four assurance audit** — cross-framework attestation for civic-AI deployment under long retention.
- **AI vendor product-engineering team** — owns the §10.51-§10.55 implementation under audit.

## Top spec sections used
- **§10.51** — Public-transparency overlay; binds 11 quarterly DP-noised aggregates with mechanism, ε, seed, and cohort subtree root.
- **§10.52** — Public model-card binding via §10.19 reuse; 12 anchored revisions over 24 months.
- **§10.53** — Hybrid post-quantum seal mandate; lifts §4.3.2 from informative to normative-when-applicable for retention horizons exceeding 25 years.
- **§10.54** — Decadal re-sealing discipline; institutional CC8.1 names 2034/2044/2054/2064/2074/2084 cadence.
- **§10.55** — Audit-target challenge-response procedure; `filed → triaged → disposed` with four canonical outcomes signed under ALJ key.
- **§1.2** — Epistemic-scope clarification on public-transparency claim.
- **§4.3.2** — Algorithm rotation and dual-algorithm Variant B AND-security; the source pattern §10.53 lifts.
- **§7** — 12-step verifier procedure; Step 7 retrieves posture, Step 11 checks both signatures.

## All cited spec sections
- **§0.5.3** — Per-role reading-path triage table.
- **§1.2** — Epistemic-scope clarification on public-transparency claim added in this release.
- **§1.5** — Decision-event vs state-machine modeling; §10.55 challenge lifecycle composes GAP-2.
- **§4.3.2** — Algorithm rotation and dual-algorithm Variant B AND-security; source pattern lifted by §10.53.
- **§7** — Verification procedure; Step 7 posture retrieval and Step 11 dual-signature check are load-bearing for §10.53 dispatch.
- **§10.5** — HSM custody attestation; covers both Ed25519 and ML-DSA-65 keys in the same partition.
- **§10.6** — IKM minimum length (256 bits); applies to both algorithms.
- **§10.10** — IKM rotation on annual cadence for both keys.
- **§10.17** — HSM partition-ceremony attestation; two ceremony events on chain.
- **§10.19** — External-artifact family that §10.52 reuses (kind = `model_card`).
- **§10.30** — Trusted-time integration normative for streaming-mode; named as forward-leaning posture for parliamentary-defensibility-critical publication.
- **§10.31** — Per-cohort subtree disclosure; the cohort subtree-root primitive §10.51 binds.
- **§10.42** — Annotated-seal-record precedent §10.54 follows for the discriminating attributes.
- **§10.44** — Cession-cohort recursive subtree disclosure; companion to §10.31 referenced for cohort anchoring under §10.51.
- **§10.47** — Generation four-tuple binding; cross-bound from §10.55 challenges to the model invocation under review.
- **§10.49** — Retrieval-source integrity; cross-bound from §10.55 challenges to the model's reasoning.
- **§10.51** — Public-transparency overlay (`chain.public_transparency.published`); DP-noised aggregate, mechanism, ε budget, RNG seed, mechanism version.
- **§10.52** — Public model-card binding via §10.19 with kind = `model_card`.
- **§10.53** — Hybrid post-quantum seal mandate; Ed25519 (FIPS 186-5) + ML-DSA-65 (FIPS 204) on every daily seal.
- **§10.54** — Decadal re-sealing discipline (`seal.resealed_at_decadal_boundary=true`) with seven discriminating attributes including resealed window, baseline manifest hash, generation index, previous-generation anchor.
- **§10.55** — Audit-target challenge-response procedure (`audit.challenge_response.*`); four canonical outcomes (`upheld | overturned | modified | withdrawn`) with paired-attribute discipline.
- **§13** — Stakeholder navigation; "civic-AI vendor and parliamentary-inquiry context" — canonical institutional reference.
- **Appendix A.13** — `chain.partition_ceremony_attended` schema (signatories, witness, attestation_pdf_sha256, hsm_attestation_token_b64).
- **PRD-2 vector 015** — Dual-algorithm cosigned-seal byte form; production chain is byte-equivalent.
- **Vectors 045-048** — Public-transparency DP aggregate, model-card binding, decadal-resealing annotated seal record, challenge-response disposition.
- **§4.3.2 / FIPS 186-5 / FIPS 204** — Cryptographic foundations under §10.53.
- **GAP-2 + GAP-5** — Composition primitives under §10.55 lifecycle and signed disposition.

## Synopsis

### Audit activity
Three-day engagement at the agency's Bern offices. Day 1 morning walk of §10.51: 11 quarterly aggregates published October 1, each chain-bound with Laplace mechanism at ε=1.0, dp_delta absent (pure-DP). Federal Audit Office independently re-applied the DP mechanism twice in the past year and matched bound values. Day 1 mid-morning §10.52: 12 model-card revisions over 24 months anchored under §10.19 with kind = `model_card`. Day 1 afternoon reconciliation: all 11 aggregates re-verified end-to-end (read entry, pull cohort subtree root, recompute raw aggregate, re-apply DP with bound seed, compare to bound published value); 11 of 11 PASS plus negative tests confirming detection. Day 2 morning §10.53 walk: every daily seal signed under both Ed25519 and ML-DSA-65 from same HSM partition. Day 2 mid-morning §10.54: institutional CC8.1 names decadal cadence at 2034/2044/2054/2064/2074/2084 boundaries; verifier dispatch path confirmed against vector 047. Day 2 afternoon: 540 daily seals over 18 months parallel-verified across team laptops in 4 minutes; 540 of 540 dual-algorithm signatures verified. Day 3 walks the three Q3 challenge-response chains end-to-end (one overturned, two upheld); ALJ key-registry binding to Federal Justice Department verifies on all three. Memo finalizes Day 3; forwarded to the parliamentary committee.

### How the spec was used

- **§10.51 / §10.31** — Binds each published aggregate's noised value with the DP mechanism, ε, seed, mechanism version, and the cohort-subtree root from §10.31.
- **§1.2** — Epistemic-scope clarification names what the chain claims and what it does not — integrity over the noised value, not noise correctness or raw-aggregate accuracy; the Federal Audit Office audits noise application out-of-band.
- **§10.52 / §10.19** — Reuses the §10.19 `audit.external_artifact.*` family with kind = `model_card`; no new event family.
- **§10.53 / §4.3.2 / §7** — Lifts §4.3.2's dual-algorithm guidance from informative to normative-when-applicable for retention horizons exceeding 25 years; verifier dispatches at §7 Step 7 (posture) and Step 11 (signature check).
- **§10.54** — Normates a recurring re-seal record at decadal boundaries with seven discriminating attributes including the previous-generation anchor SHA-256.
- **§10.55** — Normates the `filed → triaged → disposed` lifecycle with four canonical outcomes and paired-attribute discipline; the dispositioning ALJ signs under their Federal Justice Department-issued key per GAP-5.

### Results
Five spec-section confirmations: §10.51 — 11 of 11 quarterly aggregates verifiable plus negative tests confirming detection; §10.52 — 12 model-card revisions anchored, all 12 SHA-256s match Federal Audit Office's independent verification; §10.53 — 540 of 540 daily seals dual-algorithm-verified across 18 months; §10.54 — institutional CC8.1 names decadal cadence with vector 047 confirming generation-1 dispatch path; §10.55 — three challenge-response chains end-to-end-verifiable, ALJ key registry binding resolves on all three. Zero anomalies. The agency becomes the canonical institutional reference for "civic-AI vendor and parliamentary-inquiry context" in §13.
