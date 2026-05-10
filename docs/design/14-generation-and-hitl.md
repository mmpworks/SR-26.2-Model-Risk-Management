# 14 — Generation prompt/output binding + HITL review (§1.2 + §10.47-§10.50)

> **What this doc is.** The design rationale for the §1.2 stochastic-output epistemic-claim amendment and the §10.47-§10.50 generation, retrieval, and review primitives that close the Story-16 (Lyceum Health) chain-of-custody gaps for generative AI under regulated review. Auditor's-lens convention applies — every design choice answers a question an auditor would ask.

## 1. The problem this solves

Spec §1.2 through v1.0 treats outputs as *deterministic decisions*. Generative AI outputs are *stochastic*: running the same prompt against the same model twice can produce different output text. The chain-of-custody discipline still applies — the chain binds what was said at time T — but the epistemic claim must qualify "given seed S, temperature T, top-p P, top-k K, model version V, model weight hash W, retrieval set Merkle root R" rather than "the model would always say this."

Without §10.47-§10.50:

1. **No binding for the inputs.** A regulator asking "what prompt produced this output?" cannot get a chain-bound answer — only the institution-side prompt registry, which the institution controls.
2. **No binding for the retrieval set.** A regulator asking "what documents did the model see?" gets the institution's RAG log, not a chain-bound retrieval-set root.
3. **No binding for the stochastic parameters.** A regulator asking "is this output reproducible?" cannot run the model with the bound seed/temperature/etc. — those parameters live in the institution's MLOps log, not the chain.
4. **No binding for the human review.** When a clinician edits a synthesis, marks it as grounded, or flags a hallucination, there is no chain-bound signature attesting to that review — only the institution's clinical-review log.

§10.47 binds (1), §10.48 binds (3), §10.49 binds (2), §10.50 binds (4). §1.2's amendment names the stochastic-output epistemic claim explicitly so the spec's framing is self-consistent.

## 2. Motivating story — Lyceum Health

Story 16 drives the design. Lyceum Health is a Boston SaaS provider of GenAI medical-literature synthesis to academic medical centers (Cleveland Clinic, Mass General, etc.). A recent FDA warning letter to a competitor in the space has elevated regulatory scrutiny; Lyceum's existing customers want vendor due-diligence audits with clinical observers in the room.

The audit produces five questions Lyceum must answer from its chain alone:

1. **What system prompt was in force when this synthesis was generated?** §10.47 `audit.generation.system_prompt_sha256` binds the hash; the institution's CC8.1 names the system-prompt-version-in-force registry the hash resolves against.
2. **What user prompt was processed?** §10.47 `audit.generation.user_prompt_sha256` (the prompt itself may contain patient-PII — the hash binds without binding the PII).
3. **What documents were retrieved at inference time?** §10.49 retrieval-set Merkle root bound on §10.47, plus per-document anchor events with PMID cross-anchors.
4. **Are stochastic parameters bound?** §10.48 `audit.generation.temperature` / `top_p` / `top_k` / `seed` / `model_version` / `model_weight_hash`.
5. **Did a clinician review this synthesis?** §10.50 review event with the clinician's signed reviewer-event under the per-reviewer signing key registered in CC8.1.

The Cleveland Clinic clinical observer asks one question — "can my chief of medicine reproduce a synthesis from any chain entry?" — and Mike (the firm's vendor-architecture analyst) runs the live reproduction in twelve minutes from chain to PMID hashes to model parameters to byte-identical output.

## 3. Why §10.47 is one chain entry, not four

The pre-mortem rejected splitting the four-tuple across multiple chain entries. The reasons:

1. **Discrete-decision shape.** Regulated GenAI use cases (medical literature synthesis, regulatory summarization, clinical decision support) operate on discrete inference moments. One inference, one chain entry is the right shape — same as §10.11 ECOA adverse-action translation (one decision, one entry).
2. **Streaming is a UI concern, not a chain concern.** Chunked output for user experience is real, but the chain entry is emitted at stream-finish time, binding the complete output. Per-chunk entries would multiply chain volume by 50-200x for negligible audit value.
3. **Cross-binding cost.** Multi-entry composition adds `parent_run_id` / `parent_seq` cross-references for every input, complicating the verifier dispatch. Single entry binds everything in one canonical-bytes blob.

The single-entry design also makes §10.48 stochasticity attestation a clean optional extension (per the pre-mortem) rather than its own event.

## 4. Why §10.49 uses a Merkle root + per-document anchors, not inline hashes

The pre-mortem rejected inlining all retrieval-document hashes on the §10.47 entry. The reasons:

1. **Scale.** RAG retrieval typically returns 10-100 documents. 100 × ~80-byte hashes = ~8KB inline per inference. A Lyceum-scale deployment (estimated 4M+ inferences/month) inflates the chain by ~32GB/month for nothing the institution can audit selectively.
2. **Selective disclosure.** §10.31 cohort subtree disclosure is the existing primitive for selective audit; an inline hash array can't be subtree-disclosed. A regulator asking "show me retrievals for cardiology inferences but not oncology" can't do that with inline hashes.
3. **Cross-anchor to canonical sources.** PMIDs and DOIs are globally-canonical identifiers; §10.49's per-document anchor events carry them so a regulator-side reader can fetch the canonical document independently. An inline hash array loses this composition.

The Merkle-root approach reuses §10.31 (canonical RFC 6962 Merkle composition) — zero new Merkle code. The per-document anchor events follow the §10.40 cross-vendor-anchor pattern; the `canonical_identifier_kind` enum (`pmid`, `doi`, `isbn`, `institutional_doc_id`, `fda_label_id`) is the new schema, but each entry is small.

## 5. Why GAP-5 is a minimal shared HITL primitive

The pre-mortem (and Phase 6's GAP-2 precedent) rejected a broader HITL abstraction. The shared substrate across §10.50 (clinical edit), §10.55 (challenge disposition), and future override surfaces is:

- The signed-review-event chain entry schema: reviewer_id, reviewer_role, signed_at_utc, signature_b64, signed-canonical-bytes-of-review-event, parent_run_id/seq.
- The reviewer-key registry Protocol: an interface for resolving reviewer_id to a public key whose fingerprint matches the canonical-bytes binding.
- The cross-binding helper: parent_run_id / parent_seq construction per §4.4.

Total: ~100 LOC. Per-domain semantics (which outcomes are valid, which transitions follow, which authorizing policies apply) stay per-section. CUPID-Domain-based: the seam is the signed-review-event schema and the key-registry Protocol; everything else is the consumer's responsibility.

This is the same shape Phase 6's GAP-2 state-machine primitive followed. Two cross-cutting primitives that each consume `_envelope_utils.py` and that compose with each other (§10.50 uses BOTH) without a leaky base class.

## 6. Why §10.50 composes state-machine + HITL instead of being flat

The pre-mortem reversed the manifest's flat-event-family read. The output-review IS a state-machine: an output is generated → it's pending review → it's reviewed[outcome]. Two states, one transition, but it's a state machine.

Composing §10.50 with both GAP-2 (state-machine) and GAP-5 (HITL) gives the right shape:

| Concern | Primitive |
|---|---|
| The output's lifecycle position (pending_review → reviewed) | GAP-2 state-machine |
| The reviewer's signed attestation of the outcome | GAP-5 HITL primitive |
| The four canonical outcomes (clinician_edit, grounding_pass, grounding_fail, hallucination_detected) plus institution-named outcomes | §10.50 normative + CC8.1 extensions |

§10.55 (forthcoming Phase 8) will reuse the same composition for audit-target challenge-response — the disposition lifecycle is `pending → disposed[upheld/overturned/modified]`, and the disposition is a signed review under GAP-5. One pattern, two consumers, zero duplication.

## 7. Why GAP-4 is informative-only

§1.2 already says the chain "doesn't prove (c) factual accuracy" and "doesn't prove (e) statistical bias." Reproducibility under bound parameters is the same class of claim — the chain binds the parameters; reproducibility tests run out-of-band. The chain is the integrity foundation, not the truth foundation.

A normative reproducibility check would require the verifier to actually re-run the model — which the verifier is *deliberately* offline-only per §10.26 (no network calls, no model invocation, single binary). Adding model invocation to the verifier breaks the §10.26 distribution discipline. Reproducibility belongs to the regulator's audit, not the chain.

The §1.2 amendment is one paragraph naming the stochastic-output epistemic claim form. No normative §7 implications. The institution's CC8.1 names the regime under which §10.48 stochasticity attestation applies; the regulator's audit confirms reproducibility against the bound parameters out-of-band.

## 8. Test-vector design

| Vector | What it pins |
|---|---|
| `041-generation-four-tuple` | The §10.47 chain-entry byte form including §10.48 stochasticity-attestation extension. Inputs: synthetic system/user prompts with deterministic-byte-string seeds, retrieval-set Merkle root from a 4-document fixture, output hash, full §10.48 fields (temperature 0.0, top-p 1.0, seed 42, model "lyceum-medsynth-2026-04", model_weight_hash deterministic). Outputs: JCS-canonical bytes + SHA-256. |
| `042-retrieval-set-merkle` | The §10.49 retrieval-set Merkle root + per-document anchor event byte form. Inputs: 4 retrieved documents with PMID canonical identifiers, retrieval relevance scores, deterministic content hashes. Outputs: Merkle root over the 4 leaves, per-document anchor canonical bytes, cross-binding to vector 041's parent generation event. |
| `043-output-grounding-review` | The §10.50 review event byte form with `outcome = "grounding_pass"`. Inputs: synthetic clinician reviewer (deterministic key fingerprint), parent generation event reference, signed-review object per GAP-5. Outputs: review event canonical bytes + SHA-256 + GAP-5 signature byte form (deterministic since signing key is fixed). |
| `044-human-review-primitive` | The GAP-5 signed-review-event byte form, isolated from §10.50 wrapping. Inputs: minimal review-event payload + reviewer_id + signature. Outputs: canonical bytes + SHA-256. The vector exercises the primitive without invoking §10.50 attribute schema — pure HITL primitive shape. |
| `negative/N030-output-hash-mismatch` | The §10.47 generation event's `output_sha256` does not match the SHA-256 of the canonical output bytes the chain provides as evidence. |
| `negative/N031-retrieval-merkle-tampered` | The §10.49 Merkle root on the §10.47 generation event does not match the recomputed root over the per-document anchor events' `document_sha256` leaves. |
| `negative/N032-hitl-signature-bad` | The GAP-5 HITL signature on a §10.50 review event does not verify under the reviewer's declared public key. |

## 9. Composition matrix

The Phase 7 sections compose with prior phases as follows:

| Phase 7 section | Reuses | Why |
|---|---|---|
| §10.47 | §3 chain_kind enum (new "generation" value); §4.4 chain envelope | Standard chain-entry shape |
| §10.48 | §10.47 (extension fields, not separate event) | One inference moment, one chain entry |
| §10.49 | §10.31 (cohort subtree disclosure); §4.2 / §10.37 RFC 6962 Merkle | Existing Merkle substrate; selective audit |
| §10.50 | §1.5 / §10.43 GAP-2 state-machine; new GAP-5 HITL primitive; §10.11 (precedent) | Composition of state + signed-review |
| GAP-5 | §10.17 signatory schema | Reviewer signature shape |
| GAP-4 (§1.2 amendment) | §1.2 (a)/(c)/(e) existing structure | Same shape as factual-accuracy / statistical-bias non-claims |

## 10. Auditor's-lens review

**Q1. What if the institution doesn't operate under stochasticity attestation?**
A. §10.48 fields are absent from §10.47 events. The verifier confirms the four-tuple bind (§10.47) and does NOT validate stochasticity-attestation fields. The institution's CC8.1 names the regime; a future migration to a stochasticity-attestation regime is operationally additive (start emitting §10.48 fields on new entries; existing entries remain valid under the prior regime).

**Q2. What if the retrieval set is empty (the model answered without retrieving)?**
A. §10.49 emission is conditional. When `retrieval_set_merkle_root_sha256` is absent from §10.47 (deliberately omitted), the chain confirms "this inference did not retrieve." When present, §10.49 per-document anchor events MUST exist for every leaf in the Merkle tree.

**Q3. What if a clinician edits the output, then a second clinician re-reviews the edit?**
A. The institution's CC8.1 names whether re-reviews operate under a NEW state-machine instance (new `run_id`, fresh §10.47 generation reference) or as an institution-extended transition. Default: new instance. The first review's terminal state is `reviewed[clinician_edit]`; the re-review is a new state-machine starting from `pending_review` of the edited output.

**Q4. What if the reviewer's signing key is revoked between signing and verification?**
A. The institution's CC8.1 names the reviewer-key registry's revocation discipline. The chain binds the reviewer's key fingerprint at signing time; a revoked-but-historically-valid key still verifies the historical chain entry. Forward-only revocation: revoking a reviewer's key prevents NEW reviews from being signed under it, but does not invalidate past reviews. Same shape as §10.10 IKM rotation discipline.

**Q5. What if the model_weight_hash is unknown to the institution (closed-weight vendor model)?**
A. The institution's CC8.1 names the source of the weight hash — typically a vendor-supplied attestation. When the vendor does not supply a weight hash, the institution operates without §10.48 (the regime is not stochasticity-attestation-bound). The institution's procurement and vendor-management posture names this trade-off; the chain reflects whatever regime the institution actually operates.

**Q6. What about GDPR Article 22 (right not to be subject to automated decision-making)?**
A. §10.50's HITL signature is the chain-bound establishment of the human-in-the-loop the Article 22 exception requires. A clinician's signed review of a clinical decision support output IS the human-in-the-loop; the chain proves it. The healthcare-GenAI regulator overlay maps §10.50 to GDPR Article 22 alongside HIPAA, FDA 21 CFR Part 11, and EU AI Act Article 14.

**Open issue.** The verifier dispatch step that confirms reviewer-signature validity requires the reviewer-key registry to be available at chain-walk time. For a Lyceum-shape engagement where the audit happens 6-18 months after the inference, the registry MUST retain historical-key state for the audit window. The institution's CC8.1 names the retention; the operational discipline is in `docs/regulator-pack/healthcare-genai-overlay.md`.
