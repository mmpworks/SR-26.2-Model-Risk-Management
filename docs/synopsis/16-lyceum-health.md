# Story 16 — Lyceum Health (generative-AI clinical-summary CONFIRMATION)

**Story file:** `docs/auditor-stories/16-lyceum-health.md`
**Engagement type:** Two-day vendor-side spec-section confirmation pass at a generative-AI clinical-summary vendor with an external clinical observer (academic-medical-center) present Day 1.
**Posture going in:** Confirmation — §10.47-§10.50 shipped in vendor release N five months prior; vendor upgraded four months in; external clinical observer in the room ahead of contract renewal.
**Outcome posture:** Confirmation.

## Type of audit
A vendor-side spec-section confirmation engagement. The team verifies §10.47 four-tuple binding, §10.48 stochasticity attestation, §10.49 retrieval-source integrity, and §10.50 output-grounding event family in production across 14 health-system tenants. The set-piece is a 12-minute deterministic-reproduction demonstration in front of the external clinical observer.

## Interested parties (spec readers)
- **AI vendor product-engineering team** — owns the §10.47-§10.50 implementation under audit; canonical institutional reference for generative-AI clinical-summary deployment.
- **Chief AI / ML Officer** — vendor-side AI-system owner; deployment-intent author across the 14 health-system tenants.
- **Model Risk Management chair** — reads §10.47-§10.50 as the integrity substrate under SR 11-7 model lifecycle for generative-AI clinical decision support.
- **HHS Office for Civil Rights (HIPAA) examiner** — PHI integrity and minimum-necessary discipline; reads §10.22 redaction posture and §10.5 HSM custody.
- **FDA Bioresearch Monitoring (BIMO) inspector** — ALCOA+ alignment for AI clinical decision support; reads §10.47-§10.50 for deterministic reproducibility evidence.
- **General Counsel** — malpractice-discovery and FRE 902 self-authentication posture; reads §1.1 Daubert and §1.2 epistemic-scope framing.
- **Cryptographic expert witness (Daubert)** — reads §1.1, §1.3, §1.4, §4.1-§4.3, §10.5 for malpractice-defense testimony foundation.
- **Verifier implementer** — reads §7 plus §10.12 for the deterministic-reproduction verifier path that drives the 12-minute demonstration.
- **External clinical observer / academic-medical-center clinical-AI risk committee** — observer-stakeholder on Day 1; reads Appendix A.17 reading order for clinicians and §10.68 AISI-overlay parallel pattern.
- **SOC 1 / SOC 2 engagement team** — reads §7, §10.13, §10.18-§10.19 for generative-AI control-evidence schema.
- **Big-Four assurance audit** — reads §7, §10.12-§10.13, §10.18 for cross-framework attestation including ISO 42001 alignment.
- **Forensic accounting / litigation-support** — reads §5.2, §10.13, §10.69-§10.70 for malpractice-context evidence preservation.

## Top spec sections used
- **§10.47** — Generation prompt/output four-tuple binding; the load-bearing reproducibility primitive demonstrated in the 12-minute set-piece.
- **§10.48** — Stochasticity attestation; discrete fields (temperature, top_p, top_k, seed, model_version, model_weight_hash) on the §10.47 entry that make deterministic reproduction possible.
- **§10.49** — Retrieval-source integrity; per-document anchors cross-bound to the §10.47 parent via Merkle root, the surface that closes the hallucinated-PMID failure mode.
- **§10.50** — Output-grounding event family with four canonical outcomes (`clinician_edit | grounding_pass | grounding_fail | hallucination_detected`); HITL disposition signed under clinician's institution-issued key.
- **§1.1** — Daubert four-factor framing the malpractice-defense expert witness can speak to.
- **§1.2** — Epistemic scope; clarifies what the chain claims (integrity) vs. what it does not (clinical correctness).
- **§10.52** — Public model-card binding; vendor publishes a model-card update event when new model versions deploy.
- **§10.22** — Pre-MAC redaction discipline; user prompt may carry PHI, chain binds the hash without binding the PII.

## All cited spec sections
- **§0.5.1** — Three-paragraph elevator pitch.
- **§0.5.3** — Per-role reading-path triage table.
- **§0.5.5** — Names the three companions outside the spec (auditor stories, question bank, Herald.Py).
- **§1.1** — Daubert four-factor grounding for malpractice-defense.
- **§1.2** — Epistemic scope; integrity not clinical correctness.
- **§1.5** — Decision-event vs state-machine modeling; the §10.50 PENDING_REVIEW → REVIEWED transition rides under GAP-2.
- **§10.5** — HSM custody at FIPS 140-2 Level 3+; underlies the structural-infeasibility claim against forged §10.50 dispositions.
- **§10.10** — IKM rotation; verifier dispatches against the new key version per quarterly model updates (referenced via §10.33 in companion stories).
- **§10.22** — Redaction discipline; PHI in user prompts is hash-bound only.
- **§10.47** — Generation prompt/output four-tuple binding (system_prompt_sha256, user_prompt_sha256, retrieval_set_merkle_root_sha256, output_sha256 plus model_id and inference_at_utc).
- **§10.48** — Stochasticity attestation; per-request seed via OS CSPRNG plus discrete temperature/top_p/top_k/model_version/model_weight_hash bindings.
- **§10.49** — Retrieval-source integrity; per-document anchor leaves cross-bound to §10.47 parent via RFC-6962 Merkle root.
- **§10.50** — Output-grounding event family (`audit.review.*` namespace); four canonical outcomes; signed under clinician's key per GAP-5.
- **§10.52** — Public model-card binding; new model version emits model-card update event.
- **§10.63** — Training-corpus provenance chain; referenced as the training-side composition with §10.47 inference-side via model_id / model_weight_hash.
- **§10.68** — AISI Reference Evaluation Program overlay; referenced as the structurally parallel observer-stakeholder pattern.
- **§13** — Stakeholder navigation; "generative-AI healthcare vendor" and "health-system clinical-AI risk committee" become canonical entries.
- **Appendix A.10** — Redaction family schema (`disposition`, `pii_class`, `redaction_method_sha256`).
- **Appendix A.17** — Recommended reading order for clinicians coming to the spec fresh.
- **FRE 902** — Federal-court self-authentication context for the malpractice-defense answer.

## Synopsis

### Audit activity
Two-day vendor-side engagement. Day 1 morning whiteboard walk of §10.47, followed by a 12-minute deterministic-reproduction demonstration in front of the external clinical observer: read a §10.47 chain entry, pull system prompt and user prompt by hash, walk 15 retrieval-document anchors and recompute the Merkle root, replay the inference under the bound seed and stochasticity parameters, confirm byte-identical output. Observer selects the chain entry (an inpatient-handoff synthesis) and verifies a randomly-selected PMID's leaf inclusion. Day 1 continues through §10.48, §10.49, and §10.50 walks. Afternoon reconciliation runs 200 entries on the observer-tenant and 1,800 across the other 13 tenants; verifies all 14 reviewer-key registries; verifies 4 corpus snapshots; confirms 50/50 deterministic reproductions. Day 1 close-out covers the malpractice-discovery question with the §1.1 / §1.2 / §10.49 / §10.50 layered framing. Day 2 finalizes the memo.

### How the spec was used

- **§10.47** — Four-tuple binding (system_prompt_sha256, user_prompt_sha256, retrieval_set_merkle_root_sha256, output_sha256) plus model_id and inference_at_utc; the load-bearing primitive for the confirmation walk.
- **§10.48** — Discrete stochasticity fields that make the §10.47 four-tuple deterministically reproducible.
- **§10.49** — Retrieval set bound as a Merkle root over per-document anchor leaves cross-bound to the §10.47 parent.
- **§10.50** — Post-output review surface signed under the clinician's institution-issued key per GAP-5.
- **§1.1** — Daubert framing; load-bearing for the malpractice-discovery answer.
- **§1.2** — Epistemic-scope clarification; load-bearing for the malpractice-discovery answer.
- **Appendix A.17** — Clinician reading order.
- **§10.22** — Pre-MAC redaction handles PHI in user prompts.
- **§10.52** — Anchors model-card revisions.
- **§10.68** — AISI overlay referenced as the structurally parallel pattern for the external clinical observer role.

### Results
Four spec-section confirmations: §10.47 verified across 2,000 entries (byte-identical reproductions); §10.48 confirmed with 50/50 deterministic spot-checks; §10.49 verified across 4 corpus snapshots; §10.50 verified across 311 clinician dispositions including three `hallucination_detected` events that surfaced cleanly and triggered model-card updates under §10.52. Zero anomalies. External clinical observer renews the contract on the strength of the 12-minute reproduction. The vendor and its 14 health-system tenants becomes the canonical institutional reference for §10.47-§10.50.
