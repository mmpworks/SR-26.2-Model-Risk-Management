# Story 19 — Aerolith Compute (frontier-AI training laboratory WISHLIST)

**Story file:** `docs/auditor-stories/19-aerolith-compute.md`
**Engagement type:** Three-day engagement at a 32,000-GPU frontier-AI training-cluster campus; the AI Safety Institute (NIST AISI) sends two observers under a coordinated-observer letter for Days 2 and 3 — first regulator-equivalent in a wishlist-drafting room.
**Posture going in:** Inference-side chain in production for 11 months on the customer-facing API path; training-side (corpus provenance, training-run code-and-config, GPU-fleet attestation, model-weight lineage, pre-deployment evaluation) NOT in chain.
**Outcome posture:** Wishlist. Story 19 is the canonical reference for §10.63-§10.68.

## Type of audit
A wishlist-drafting engagement. Day 1 confirms the inference-side chain (5 sample inferences across the 11-month audit period; all PASS); Days 2 and 3 surface six proposed §10.x sections covering frontier-model training provenance (§10.63-§10.68) with AISI as observer-stakeholder. The §10.68 AISI Reference Evaluation Program overlay is the regulator-pack item that lifts the family into AISI's submission framework.

## Interested parties (spec readers)
- **AISI / NIST AISI safety evaluator** — frontier-model pre-deployment evaluation under the AISI Reference Evaluation Program; reads §10.63-§10.68.
- **AISI coordinated-observer-program lead** — sets the observer-letter posture, reciprocity, and submission cadence; reads §10.67, §10.68.
- **Standards-body reviewer** — frontier-model training-provenance wishlist coherence; reads §0, §11, §12 plus §10.63-§10.68.
- **Chief AI / ML Officer** — frontier-AI deployment-intent author and training-side chain owner; reads §4.4.1, §4.4.2, §10.63-§10.67.
- **Model Risk Management chair** — SR 11-7 reading the training-provenance family as the integrity substrate under model documentation; reads §10.66, §10.67.
- **Chief Data Officer** — training-corpus provenance lineage; reads §10.20, §10.63 plus Appendix A.1-A.16.
- **AI vendor product-engineering team** — owns training-side instrumentation; reads §10.63-§10.67 plus §10.21 cross-anchor primitive.
- **SDK implementer** — capture-side library author for training-corpus, training-run, and fleet-attestation events.
- **Ledger implementer** — ingestion of hyperscale GPU-fleet attestation under §10.65 plus per-step Merkle aggregation under §10.64.
- **Verifier implementer** — parallel-evaluator dispatch via §10.21.2 cardinality and AISI overlay under §10.68.
- **Academic researcher** — frontier-AI safety governance research; reads §1.1-§1.5, §9, §11.
- **Cryptographic expert witness (Daubert)** — training-provenance integrity testimony; reads §1.1, §1.3, §1.4, §4.1-§4.3, §10.5, §10.65-§10.66.

## Top spec sections used
- **§10.63** — Training-corpus provenance chain (build-time); shard_ingested, dedup_decision, filter_pass, index_built events.
- **§10.64** — Training-run code-and-config chain; per-step aggregation_proof as Merkle root over per-chassis gradient contributions.
- **§10.65** — Hyperscale GPU-fleet attestation; chassis_admitted, chassis_attested, chassis_quarantined, chassis_decommissioned for ~250 chassis (32K GPUs at 128/chassis).
- **§10.66** — Model-weight lineage across multi-month runs; DAG-shaped lineage from pre-training base to deployed weights with retention commitment in CC8.1.
- **§10.67** — Pre-deployment evaluation chain; per-evaluator parallel-chain composition via §10.21.2.
- **§10.68** — AISI Reference Evaluation Program regulator-pack overlay; binds §10.63-§10.67 family into AISI submission, maps NIST AI RMF 1.0 + NIST AI 800-218.
- **§10.21** — Cross-vendor model-handover schema; the cross-anchor primitive §10.63-§10.68 reuse.
- **§10.47** — Generation four-tuple binding; in production on the inference-side path.

## All cited spec sections
- **§0.5.5** — Names the layered companions (spec, auditor stories, question bank, Herald.Py).
- **§10.21** — Cross-vendor model-handover; the cross-anchor primitive used across §10.63 (license attestations), §10.66 (lineage transitions), §10.67 (parallel-evaluator), §10.68 (AISI eval results back into lab chain).
- **§10.21.1** — Sample-based-attestation cross-anchor; sample-based corpus attestation under §10.63.
- **§10.21.2** — Parallel-evaluator composition pattern with `cardinality`; AISI's evals and lab's evals are parallel chains under §10.67 anchored at target-model-weights level (cardinality = 2).
- **§10.27** — Default cadence for daily seal under which the inference-side chain runs.
- **§10.34** — Training-phase integrity from federated geometry; contrasted as antecedent that does not trivially extend to centralized hyperscale.
- **§10.35** — Edge-attestation primitive; structurally similar to §10.65 hyperscale fleet attestation but at different geometry.
- **§10.47** — Generation four-tuple binding; in production on inference path.
- **§10.48** — Stochasticity attestation; verifies on inference-side reconciliation.
- **§10.49** — Retrieval-source integrity; verifies on the RAG inference path.
- **§10.50** — Output-grounding event family; referenced as antecedent.
- **§10.54** — Decadal re-sealing; §10.66 retention horizon (60 months for frontier models) is aligned with this posture.
- **§10.58** — Component cryptographic identity primitive; chassis-level TPM is the chassis-granularity identity-kind.
- **§10.62** — Red/black separation; referenced as the parallel pattern.
- **§10.62.1** — Per-entry color-side tagging; structurally parallel to AISI's pre-disclosure / disclosable sensitivity tagging discipline.
- **§10.62.2** — Releasability-projection contract; the canonical pattern AISI's submission-filter follows.
- **§10.63** — Training-corpus provenance chain (`audit.training_corpus.shard_ingested`, `dedup_decision`, `filter_pass`, `index_built`).
- **§10.64** — Training-run code-and-config chain (`audit.training_run.launch`, `checkpoint`, `completed`); per-step aggregation_proof Merkle root over per-chassis contributions.
- **§10.65** — Hyperscale GPU-fleet attestation (`audit.fleet.chassis_admitted`, `chassis_attested`, `chassis_quarantined`, `chassis_decommissioned`).
- **§10.65.1** — Composition with §10.58; chassis-level TPM as chassis-granularity component-cryptographic-identity primitive.
- **§10.65.2** — `audit.fleet.profile_updated` event publishing the institution's expected PCR-state-evolution profile so `drift_seen` is publicly verifiable.
- **§10.66** — Model-weight lineage (`audit.model_weights.transition`, `deployed`); DAG-shaped lineage with Merkle root over the full transition graph.
- **§10.67** — Pre-deployment evaluation chain (`audit.evaluation.run`, `result`, `disposition`); §10.21.2 parallel-evaluator composition.
- **§10.68** — AISI Reference Evaluation Program regulator-pack overlay; maps NIST AI RMF 1.0 (GOVERN-1, MAP-2, MEASURE-1, MEASURE-2, MANAGE-2) and NIST AI 800-218 onto the §10.63-§10.67 surface.
- **§13** — Stakeholder navigation; "frontier-AI training laboratory" plus AI Safety Institute as regulator-equivalent observer-stakeholder become two new candidate stakeholders.
- **NIST AI RMF 1.0** — GOVERN-1, MAP-2, MEASURE-1, MEASURE-2, MANAGE-2 functions mapped under §10.68.
- **NIST AI 800-218** — Secure software development practices for AI, mapped under §10.68.
- **Vectors 065-076** — Per `spec/test-vectors/PRD-4-INDEX.md`: corpus-build chain (065-066), training-run with per-step Merkle aggregation (067-068), hyperscale fleet attestation including expected-state-evolution and unexplained-shift (069-071), model-weight lineage linear and merge (072-073), evaluation chain single and parallel-lab-AISI (074-075), AISI overlay verifier dispatch (076).

## Synopsis

### Audit activity
Three-day engagement at the Quincy datacenter campus (two enormous datacenter boxes plus a small office building, 60 megawatts of compute). Day 1 walks the inference-side chain: ~30B chain entries over 11 months, daily-cadence seal under §10.27 default, signed under AWS CloudHSM in us-west-2; the customer-facing API path; the §10.47 four-tuple binding is in production on every inference; five sample inferences across the audit period (one hit the §10.49 retrieval-augmented-generation path) all PASS. Day 1 afternoon walks the training-cluster building (~250 chassis at 128 GPUs/chassis with per-chassis TPM attestation; 47 attestation-shift events in the last 112-day training run, 41 benign firmware updates, 6 unexplained chassis decommissionings). Days 2 and 3 with two AISI observers in the room, the team whiteboards six wishlist sections. Training-run launch records (run `r-2025-Q3-major-7`, 112 days, 6,400 checkpoints every 25 minutes) walked; model-weight lineage walked (pre-training → SFT → RLHF/DPO → red-team/eval → final pre-deployment as a DAG with merge operations). The regulator-equivalent observer's question — "was a specific corpus shard responsible? was a specific RLHF preference pair responsible?" — articulates the gap. Day 3 morning §10.68 overlay drafting with AISI present. Wishlist memo final Day 3; close-out with the lab committing as canonical institutional reference and AISI committing as observer-stakeholder.

### How the spec was used

- **§10.47 / §10.48 / §10.49** — Inference-side confirmation exercises four-tuple binding, stochasticity attestation, and retrieval-source integrity (production of previously-shipped sections in a different industry context).
- **§10.63 / §10.21.1** — Wishlist training-corpus provenance, build-time chain; training-time chain references the indexed-corpus version; sample-based corpus attestation per §10.21.1.
- **§10.64 / §10.65** — Wishlist training-run launch / checkpoint / completed events with per-step aggregation_proof normated as a Merkle root over per-chassis gradient contributions, leaves bound to §10.65 chassis attestation.
- **§10.65 / §10.65.1 / §10.58 / §10.65.2** — Wishlist hyperscale fleet attestation with §10.65.1 composing with §10.58 chassis-level TPM as the chassis-granularity identity-kind, and §10.65.2 normating the chain-published `audit.fleet.profile_updated` event so public verifiers running outside the lab's IKM can perform the `drift_seen` discrimination.
- **§10.66 / §10.54** — Wishlist model-weight lineage as a DAG including merges and interpolations with retention commitment in CC8.1 aligned to §10.54 decadal posture.
- **§10.67 / §10.21.2** — Wishlist evaluation chain with per-evaluator parallelism via §10.21.2 cardinality = 2 — lab and AISI as parallel chains anchored at target-model-weights level.
- **§10.68 / §10.62.2** — Wishlist regulator-pack overlay framework binding §10.63-§10.67 into AISI submission, mapping NIST AI RMF 1.0 functions and NIST AI 800-218 practices, with AISI's submission filter structurally parallel to a program filter under §10.62.2's releasability-projection contract.

### Results
Six wishlist sections drafted: §10.63 training-corpus provenance, §10.64 training-run code-and-config, §10.65 hyperscale GPU-fleet attestation (with sub-patterns §10.65.1 and §10.65.2), §10.66 model-weight lineage, §10.67 pre-deployment evaluation chain, §10.68 AISI pre-deployment-attestation overlay. Lab commits as canonical institutional reference for §10.63-§10.68; AISI commits as regulator-equivalent observer-stakeholder for the working-group sub-track. Commitment to §10.63-§10.68 deployment within twelve months of normative-text adoption with §10.68 fast-tracked to align with the next major model release's AISI submission. Wishlist memo goes to the trust-side counterpart, coordinated-observer copy to AISI for the AISI Reference Evaluation Program documentation track, and to the spec working group. First time a regulator-equivalent observer is present in a wishlist-drafting room.
