# 18 — Frontier-AI training provenance (§10.63-§10.68)

> **What this doc is.** The design rationale for the §10.63-§10.68 primitives that close the Story-19 (Aerolith Compute) chain-of-custody gaps for frontier-AI training provenance — corpus-build chain, training-run code-and-config chain with per-step Merkle aggregation, hyperscale GPU-fleet attestation, model-weight lineage across multi-month runs, pre-deployment evaluation chain, and AI Safety Institute Reference Evaluation Program regulator-pack overlay. Auditor's-lens convention applies.

## 1. The problem this solves

Story 19 drives the design. Aerolith Compute is a US frontier-AI training laboratory — 32K-GPU training cluster in Quincy, WA; ~3,500 employees; voluntary partnership with the US AI Safety Institute (NIST AISI) Reference Evaluation Program. An inference-side conformant chain has been in production for 11 months. The training-time chain — corpus, run, fleet attestation, weight lineage, evaluation — is not in chain at all.

Five questions Aerolith and AISI must answer from the chain alone:

1. **Was this model trained on the corpus we said it was trained on?** §10.63 binds corpus-build provenance from raw shard ingest through dedup, license-screen, safety-filter, indexed-corpus production. The deployed model's training run cites the indexed-corpus content_hash; the corpus chain validates the build.
2. **What code, hyperparameters, and fleet produced this run's checkpoints?** §10.64 binds run launch (code commit, hyperparameter config, fleet manifest), per-step Merkle aggregation over per-chassis gradient contributions, and final completion bound to deployed model weights.
3. **Is the GPU fleet still the fleet we admitted?** §10.65 binds chassis admission (TPM attestation), daily re-attestation with `drift_seen` discrimination against an §10.65.2 expected-state-evolution profile, scheduler quarantine on attestation shifts, decommissioning.
4. **What lineage led to the deployed model's weights?** §10.66 binds the lineage DAG from pre-training root through SFT / RLHF / DPO / merge / interpolation transitions to deployed weights, with a Merkle root over the full DAG bound at deployment.
5. **What did the evaluations find, and what was the deployment decision?** §10.67 binds evaluation runs, results, and disposition; supports parallel-evaluator composition (lab + AISI) via §10.21.2 cross-anchor at the target-model-weights boundary.

§10.68 is the regulator-pack composition: it binds §10.63-§10.67 into the AISI Reference Evaluation Program submission framework, mapping NIST AI RMF 1.0 functions and NIST AI 800-218 secure-software-development practices onto chain entries.

Without §10.63-§10.68, AISI's evaluator cannot independently verify the training-side provenance; the integrity claim is the lab's signed engineering attestation. With §10.63-§10.68, AISI's evaluator runs verifier dispatch against the chain; the integrity claim is cryptographic.

## 2. Why training-corpus provenance is build-time, not run-time

§10.63 emits at corpus-build time, not at training-time. The corpus-build pipeline runs once per major release; the training run consumes the indexed corpus over weeks or months. Embedding corpus events in the training-run chain would (a) inflate the run chain by orders of magnitude, (b) couple corpus integrity to run integrity unnecessarily, and (c) prevent multiple training runs from sharing one corpus.

§10.63 emits four event kinds: shard ingested, dedup decision, filter pass, index built. The training-time chain references the indexed corpus by `indexed_corpus_content_hash`; verifying that the run cited the right corpus is a §10.64 verifier dispatch.

The pre-mortem flagged a failure mode: corpus binding by manifest-hash without binding the build-pipeline's transformation chain leaves a gap between "we built this corpus from these inputs" and "we trained on this corpus." §10.63 closes the gap by binding every transformation; §10.64 closes the gap by referencing the indexed corpus content_hash at run launch.

## 3. Why per-step Merkle aggregation is the right shape

A 32K-GPU training run produces gigabytes of gradient data per step at peak. Hashing every gradient byte cryptographically per step is bandwidth-prohibitive. §10.64's `gradient_aggregation_proof_hash` is a Merkle root over per-chassis gradient contributions; each leaf is the SHA-256 of one chassis's per-step contribution; leaves are sorted by chassis-id; the construction follows RFC 6962 (consistent with §4.2 daily seal).

The leaf count at peak is on the order of the chassis count (~250 for Aerolith's 32K GPUs at 128/chassis). The Merkle aggregation cost is logarithmic in leaf count; the per-step aggregation is dominated by the per-chassis gradient compute, not by the Merkle.

The Kevin-pushback in Story 19's design conversation is preserved here: the cardinality is per-chassis, not per-GPU. Per-GPU TEEs are a future identity-granularity (§10.58 / §10.65.1 extension); per-chassis TPM is the primitive in PRD-4 hardware. When per-GPU TEEs become commodity, the §10.64 leaf cardinality lifts to per-GPU under the same Merkle pattern.

## 4. Why expected-state-evolution profile is chain-published

PCR state changes constantly during normal training — kernel modules load, drivers update, monitoring agents update. Without an expected-state-evolution profile, every routine kernel update produces a chain anomaly.

The pre-mortem identified two implementation choices: (a) profile lives only in CC8.1 (institution-side attachment); (b) profile is chain-published as an `audit.fleet.profile_updated` event. The pre-mortem's mitigation rejected (a) — public verifiers running outside the institution's IKM can't access CC8.1 by construction. §10.65.2 requires profile publication to the chain; the verifier walks both `chassis_attested` events and `profile_updated` events to dispatch `drift_seen` discrimination. Public verifiability of the discrimination is preserved.

The trade-off: institutions cannot retroactively claim a different "expected" profile after the fact. The profile evolution is an integrity-bound chain entry; institution-side governance (CC8.1 names the profile-publication cadence and review discipline) overlays on the chain-bound truth.

## 5. Why §10.67 supports parallel-evaluator composition via §10.21.2

The lab runs its internal pre-deployment evaluation. AISI runs its program evaluation under the Reference Evaluation Program. Both produce per-model evaluation chains; both anchor at the target-model-weights boundary; the chains compose via §10.21.2 cross-anchor.

The §10.21.2 primitive (lifted in this same wave) generalizes to:

- §10.45 (independent third-party adjuster anchor for reinsurance)
- §10.50 (clinical observer at output-grounding events)
- §10.60 (independent anti-counterfeit attestation laboratory)
- §10.67 (lab + AISI parallel evaluation chains)

The pattern is: a single subject (claim, output, lot, model) is evaluated by N independent parties, each running its own chain, composed at a known anchor boundary. §10.21.2 is the right shared primitive — the wishlist manifest classifies it as Both (Doc + code) because §10.67 implementation requires a shared module to handle the N-evaluator composition logic uniformly.

## 6. Why §10.68 is a versioned regulator-pack overlay

The AISI Reference Evaluation Program is in active development. The submission framework will evolve; the chain-of-custody binding to it must follow.

§10.68 normates the *overlay framework* (the contract for how AISI program versions map onto chain entries) — not a fixed AISI v1.0 binding. §10.68.1 is PRD-4's instance for the AISI Reference Evaluation Program release current at PRD-4 publication. Future AISI releases land as §10.68.2, §10.68.3, etc. The deprecated-version sunset-attestation marker pattern (introduced for §10.61 CMMC) applies symmetrically.

The pre-mortem's #5 mitigation is preserved here: the spec text's commitment to AISI as "regulator-equivalent" lives in the spec's normative text; the narrative-driven framing of "observer-stakeholder" lives in the plain-spoken companion repo's Story 19 walkthrough only. Spec submission is unaffected if AISI's actual program governance posture turns out narrower than the plain-spoken narrative; only Story 19 publication is gated on a written AISI letter.

## 7. Cross-references

- Spec sections: §10.21 / §10.21.2 (parallel-evaluator composition); §10.34 (federated training-phase integrity, the federated counterpart); §10.52 (public model-card binding); §10.54 (decadal re-sealing for long-retention model-weight regimes); §10.63-§10.68 (this design doc's surface).
- Test vectors: 064-074 (§10.63-§10.68); §10.65 fleet attestation has three vectors covering clean / authorized-update / unexplained-shift discrimination (068-070).
- Auditor stories: Story 19 (Aerolith Compute / AISI) — the institutional-reference engagement.
- Adjacent design docs: 14-generation-and-hitl.md (parallel for §10.50 clinical decision-support output grounding); 18-public-transparency.md (parallel for §10.51 civic-AI public-aggregate publication).
- Regulator pack: `docs/regulator-pack/aisi-overlay.md` (§10.68.1); `docs/regulator-pack/civic-ai-overlay.md` (sibling for civic-AI overlays).
- External: NIST AI RMF 1.0; NIST AI 800-218 (secure software development practices for AI); AISI Reference Evaluation Program documentation; TCG TPM 2.0 specification; NIST SP 800-155 (BIOS/firmware integrity); RFC 6962 (Merkle construction).
