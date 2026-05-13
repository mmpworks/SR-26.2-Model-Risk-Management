# Healthcare GenAI Regulator Overlay

> **Purpose.** Operational mapping for institutions whose chain-of-custody work crosses healthcare regulatory scope when generative AI / RAG / clinical decision support is in production: vendor due-diligence audits with clinical observers, FDA warning-letter context, HIPAA business-associate review, EU AI Act Article 14 human-oversight requirements, GDPR Article 22 automated-decision-making rights. Anchors against spec §10.47-§10.50 (Phase 7 / Story 16) — generation prompt/output binding, stochasticity attestation, retrieval-source integrity, output-grounding HITL review.

## 1. Why this overlay exists

A Boston SaaS provider (Story 16's Lyceum Health) sells GenAI medical-literature synthesis to academic medical centers. After an FDA warning letter to a competitor in the space, Lyceum's customers (Cleveland Clinic, Mass General) demand vendor due-diligence audits with clinical observers in the room. The auditor needs to trace, from the chain alone:

1. What system prompt was in force when this synthesis was generated?
2. What user prompt was processed?
3. What documents were retrieved (PMIDs)?
4. Were the stochastic parameters bound?
5. Did a clinician review the output, and what was their signed conclusion?

Without §10.47-§10.50 chain bindings, every answer comes from institution-side logs — no chain-bound integrity claim. With them, the chain alone answers all five questions.

## 2. Mapping table

| Healthcare regulatory surface | Spec section | What the chain shows |
|---|---|---|
| **FDA 21 CFR Part 11** (electronic records / signatures for FDA-regulated industries) | §10.47 + §10.50 | The four-tuple binding establishes the integrity-bound electronic record; the §10.50 review event with HITL signature establishes the electronic signature for clinician-reviewed outputs. |
| **FDA warning-letter follow-through** (post-warning vendor due-diligence) | §10.47 + §10.48 | When a competitor receives an FDA warning letter for inadequate output controls, peer institutions audit their own chain-bound generation events for stochasticity binding (§10.48) and review-completeness (§10.50). The chain provides the cryptographic substrate the audit reads. |
| **HIPAA § 164.502** (PHI minimum-necessary) | §10.47 user_prompt_sha256 | The user prompt may contain PHI; binding the hash satisfies minimum-necessary by NOT binding the PHI itself into the chain. The institution's tokenization layer (per `docs/privacy-by-design.md`) maps the hash back to the PHI under controlled access. |
| **HIPAA § 164.404** (breach notification) | §10.49 retrieval-set Merkle root | Retrieved documents may contain de-identified patient data; binding only the Merkle root limits breach scope to the per-document anchor entries (which carry no PHI — only PMID/DOI canonical identifiers). |
| **EU AI Act Article 14** (human oversight) | §10.50 HITL signature | The clinician's signed review under GAP-5 establishes the human-in-the-loop the Article 14 oversight requirement names. The chain proves the review occurred, by whom, with what outcome. |
| **GDPR Article 22** (automated decision-making rights) | §10.50 HITL signature | A clinical decision support output reviewed and signed by a human IS the human-in-the-loop the Article 22 exception requires. The chain establishes this from the institution side; the patient-facing rights notification is institutional. |
| **Cleveland Clinic / academic medical center vendor due-diligence** | §10.47 + §10.49 + §10.50 | The full triad — what was generated, what was retrieved, who reviewed it — covers the standard institutional vendor-DD checklist. |

## 3. Examination workflow

A clinical observer running a vendor due-diligence audit on a Lyceum-shape GenAI deployment:

1. **Sample selection.** Observer names a sample (e.g., 50 syntheses for cardiology decisions in calendar Q1 2026). The institution exercises §10.31 cohort subtree disclosure to expose only the sampled inferences' chain entries.

2. **Per-inference walk.** For each sampled generation:
   - Walk the §10.47 chain entry: confirm `system_prompt_sha256` matches the institution's CC8.1-named system-prompt-version registry.
   - Confirm `user_prompt_sha256` (PHI-bearing prompt) is correctly bound without binding the PHI itself.
   - Confirm `output_sha256` matches the institution-provided output bytes for the inference.
   - Confirm `retrieval_set_merkle_root_sha256` matches the recomputed root over §10.49 per-document anchors.
   - When §10.48 is operated: confirm temperature, top-p, top-k, seed, model_version, model_weight_hash all in bounds and present.

3. **Retrieval audit.** For sampled inferences with retrieval, walk the §10.49 anchor events:
   - Confirm each `document_sha256` is a leaf in the parent generation's Merkle tree.
   - Confirm canonical-identifier-kind values (typically PMID for medical literature).
   - Spot-check `retrieval_relevance_score` against expected ranking patterns.

4. **Review audit.** For sampled inferences operating under HITL review (the institution's CC8.1 names which inferences require it):
   - Walk the §10.50 review event paired with each generation.
   - Confirm the GAP-5 signed-review verifies under the reviewer's registered key (per the institution's reviewer-key registry).
   - Confirm `signed_payload_sha256` matches the recomputed canonical-bytes hash.
   - Spot-check the four canonical outcomes — `clinician_edit` events should have non-empty `edited_output_sha256`; `hallucination_detected` events should trigger institutional IR-program engagement per CC8.1.

5. **Reproducibility check (when stochasticity attestation applies).** For one or more sampled inferences, the observer asks the institution to re-run the model with the bound parameters (system prompt, user prompt, retrieval set, temperature, top-p, top-k, seed, model_version, model_weight_hash) and confirm the output matches `output_sha256`. The chain itself doesn't perform this test — the chain binds the parameters; reproducibility is the regulator's audit.

## 4. Reviewer-key registry posture

§10.50 / GAP-5 depends on a per-reviewer signing-key registry. The institution's CC8.1 names:

- **Authority.** Who manages the registry (typical: institution's IT identity-management group with clinical-credentialing input).
- **Issuance.** When and how a clinician's signing key is registered (typical: at credentialing time, with the public key registered alongside the clinician's NPI / institutional ID).
- **Rotation.** Discipline for key rotation (typical: annual, or on-event for credential changes).
- **Revocation.** Forward-only revocation discipline (revoked keys verify past reviews; new reviews under the revoked key are rejected).
- **Retention.** Historical-key retention for the audit window (typical: 7 years for FDA-regulated, 10 years for malpractice-litigation-anticipated, longer for clinical research records).
- **Trust anchors.** When the institution accepts review signatures from third-party physicians (e.g., Cleveland Clinic-employed clinicians reviewing Lyceum-served outputs at Mass General), the trust anchors connecting the institutions' reviewer-key registries.

## 5. Story 16 reference — Lyceum Health

The Story 16 narrative (forthcoming) drives this overlay. The key features:

- Vendor: Lyceum Health (Boston SaaS, GenAI medical-literature synthesis)
- Customer: Cleveland Clinic (academic medical center, clinical observer in the audit room)
- Trigger: recent FDA warning letter to a competitor in the space
- Audit shape: vendor due-diligence under recurring clinical-observer engagement
- Canonical question (the "4:30 PM moment"): "Can my chief of medicine reproduce a synthesis from any chain entry?"

The §10.47-§10.50 family produces a complete chain-bound record of: per-inference four-tuples (§10.47), stochastic parameter binding (§10.48), retrieval-set Merkle roots (§10.49 + §10.31 selective disclosure), HITL clinical reviews (§10.50 + GAP-5). The Cleveland Clinic chief of medicine's reproducibility test is mechanical — re-run the model with the bound parameters; compare output hash.

## 6. Cross-references

- Spec §1.2 stochastic-output epistemic claim
- Spec §1.5 decision-event vs state-machine modeling
- Spec §10.31 / §10.44 cohort subtree disclosure
- Spec §10.47 generation prompt/output four-tuple binding
- Spec §10.48 stochasticity attestation
- Spec §10.49 retrieval-source integrity
- Spec §10.50 output-grounding event family
- Spec §10.11 ECOA adverse-action notice translation (the existing `translator_kind = "human"` precedent)
- Spec §10.55 audit-target challenge-response (forthcoming Phase 8 — civic-AI sibling)
- Design `docs/design/14-generation-and-hitl.md`
- Test vectors `041`, `042`, `043`, `044`

## 7. Operational checklist for the institution

Before each §10.47-§10.50-bound engagement (vendor due-diligence audit, regulatory inquiry, internal clinical-quality review):

- [ ] CC8.1 names the system-prompt-version registry and the cadence of updates
- [ ] CC8.1 names the model-weight-hash sourcing (vendor attestation for closed-weight models, on-disk hash for open-weight)
- [ ] CC8.1 names the reviewer-key registry authority, rotation, revocation, and retention
- [ ] CC8.1 names whether the institution operates under stochasticity attestation (§10.48 fields present) or not
- [ ] CC8.1 names the four-canonical-outcome interpretation in the institution's clinical-review workflow
- [ ] §10.31 cohort subtree disclosure is exercised against a recent inference sample
- [ ] §10.49 Merkle-root recomputation is exercised against a recent retrieval set
- [ ] §10.50 HITL signatures are spot-verified against the reviewer-key registry
- [ ] Reproducibility test is exercised against at least one sampled inference end-to-end
