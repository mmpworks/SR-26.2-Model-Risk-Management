---
title: AI Safety Institute Reference Evaluation Program Articulation Overlay
status: informative
aligned-with:
  - NIST AI Risk Management Framework 1.0
  - NIST AI 800-218 (Secure Software Development Practices for AI)
  - NIST AISI Reference Evaluation Program documentation
  - Executive Order 14110 (Safe, Secure, and Trustworthy Development and Use of AI; foundational mandate)
  - OMB M-24-10 (Advancing Governance, Innovation, and Risk Management for Agency Use of AI)
date: 2026-05-09
version: 1.0.0
revision-cadence: per-AISI-program-release
---

# AISI Reference Evaluation Program Articulation Overlay (§10.68.1)

> **What this doc is.** The PRD-4 instance of the §10.68 versioned regulator-pack overlay framework. The framework is shaped to match the *kind of program* the US AI Safety Institute (NIST AISI) Reference Evaluation Program represents — a voluntary regulator-equivalent observer program that conducts pre-deployment evaluation under publicly-documented intake terms. Whether AISI itself adopts the §10.68 overlay as an accepted intake format is a program-side decision; the overlay normates the chain-integrity-bound submission packet shape an institution MAY produce, plus the verifier dispatch a participating program MAY consume. Written so a participating frontier-AI laboratory's submission lead can prepare a chain-integrity-bound submission, and so an evaluator at any voluntary observer program can run the §10.68 verifier dispatch as part of their own intake processing if their program elects to.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's NIST AI RMF risk register, model cards, or substantive evaluation reports. The §1.2 epistemic scope applies: the chain proves what was said and that the record was not tampered with; it does not certify model safety, capability claims, or evaluation outcomes.

> **Versioning discipline.** This overlay tracks the AISI Reference Evaluation Program release current at PRD-4 publication. When the program revises its submission framework, a new overlay ships under §10.68.2; this overlay is preserved with a `sunset_attestation` marker discipline.

---

## 1. Scope and reading order

This overlay covers institutions submitting models under the AISI Reference Evaluation Program. The canonical PRD-4 institutional reference is Aerolith Compute (Story 19). Reading order: §10.63-§10.67 (training-provenance wave); §10.68 (this overlay's normative anchor); NIST AI RMF 1.0 functions; NIST AI 800-218 practices.

## 2. NIST AI RMF 1.0 function mapping

| AI RMF function | Spec sections | Operational binding |
|---|---|---|
| GOVERN-1 (Governance over AI) | §10.18 CC8.1 cross-referencing; §10.66 model-weight retention discipline | Institution's governance program documented in CC8.1; model retention horizon named |
| MAP-2 (Categorize and document AI system) | §10.52 public model-card binding; §10.63 training-corpus provenance | Model card published; corpus binding integrity-bound |
| MEASURE-1 (Identify metrics) | §10.67 evaluation chain | `audit.evaluation.run` carries `evaluation_corpus_hash`, `target_model_weights_hash` |
| MEASURE-2 (Evaluate AI system) | §10.67 evaluation chain | `audit.evaluation.result` and `audit.evaluation.disposition` bound |
| MANAGE-2 (Risk treatment) | §10.67 disposition | Deployment decisions (`ship` \| `block` \| `revise`) integrity-bound |

## 3. NIST AI 800-218 practice mapping

| 800-218 practice | Spec anchor |
|---|---|
| Plan and develop secure-by-design AI | §10.18 CC8.1 cross-referencing of AI development plan |
| Protect software (including model weights) | §10.66 model-weight lineage; §10.5 HSM custody for signing keys |
| Verify integrity of releases | §10.67 evaluation chain; §10.68 submission overlay |
| Respond to vulnerabilities | §10.2 operational events including `incident.detected` and AI-specific events |

## 4. AISI submission packet composition

A §10.68-conformant AISI submission contains:

1. **Training-corpus provenance** — §10.63 chain entries for the corpus the deployed model was trained on, with the indexed-corpus content_hash referenced.
2. **Training-run lineage** — §10.64 chain entries for the run(s) producing the deployed weights, plus per-step Merkle aggregation proofs at the institution's named cadence.
3. **Fleet attestation** — §10.65 chain entries demonstrating the GPU-fleet was attested through the run's life with `drift_seen` discrimination per the institution's expected-state-evolution profile.
4. **Model-weight lineage** — §10.66 lineage DAG from pre-training root to deployed weights.
5. **Lab-side evaluation chain** — §10.67 events for the institution's internal evaluation cycle.
6. **Cross-anchor reciprocity** — when AISI runs a parallel evaluation chain, §10.21 cross-anchor binds AISI's results back into the lab's chain.

## 5. AISI evaluator orientation

An AISI evaluator processing a submission walks:

1. The §10.68 verifier's control-by-control PASS/FAIL output against the submission packet.
2. The §10.21.2 parallel-evaluator cardinality check (lab + AISI cardinality).
3. The §10.66 retention-horizon commitment in the institution's CC8.1 (typically 60 months for frontier models).
4. The institution's chain-coverage map (§10.19) for any out-of-scope segments documented as residuals.

## 6. Cross-references

- Spec sections: §10.21 / §10.21.2 (parallel-evaluator composition); §10.34 (federated training-phase integrity, federated counterpart); §10.52 (public model-card binding); §10.63-§10.68 (training-provenance wave).
- Adjacent overlays: `civic-ai-overlay.md` (sibling for civic-AI / parliamentary contexts); `healthcare-genai-overlay.md` (sibling for clinical-decision-support generative-AI).
- Design doc: `docs/design/18-frontier-ai-training-provenance.md`.
- External: NIST AI RMF 1.0; NIST AI 800-218; AISI Reference Evaluation Program documentation; Executive Order 14110.
