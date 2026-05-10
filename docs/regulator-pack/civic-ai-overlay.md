# Civic-AI Regulator Overlay

> **Purpose.** Operational mapping for institutions whose chain-of-custody work crosses civic / public-sector AI regulatory scope when AI augments government decisions affecting members of the public: tax-audit-target selection, immigration-status determinations, public-benefits eligibility scoring, parking/traffic enforcement automated review. Anchors against spec §10.51 (DP-bound public-transparency aggregate), §10.52 (public model-card binding), §10.55 (audit-target challenge-response), §1.2 public-transparency epistemic claim, and §1.5 / §10.43 GAP-2 state-machine framing.

## 1. Why this overlay exists

The Helvetian Federal Tax Authority (Story 17) operates AI-augmented VAT audit-target selection. A taxpayer challenges an audit selection in 2027; a parliamentary inquiry follows. The auditor needs to trace, from the chain alone:

1. What model was used to flag this taxpayer?
2. What was the published model card at the time of the decision?
3. What aggregate statistics did the agency publish about audit selection — and were they protected by differential privacy as the agency claimed?
4. Did the taxpayer's challenge follow the lifecycle (filed → triaged → disposed) the agency's policy named?
5. Who dispositioned the challenge, with what outcome, and did they sign the disposition?

Without §10.51-§10.55 chain bindings, every answer comes from agency-side logs — no chain-bound integrity claim against parliamentary scrutiny. With them, the chain alone answers all five questions.

## 2. Mapping table

| Civic-AI regulatory surface | Spec section | What the chain shows |
|---|---|---|
| **EU AI Act Article 14** (human oversight in high-risk AI) | §10.55 + GAP-5 | The administrative-law judge's signed disposition under GAP-5 establishes the human-in-the-loop the Article 14 oversight requirement names. The chain proves the review occurred, by whom, with what outcome — without semantic drift across challenges. |
| **EU AI Act Article 22** (transparency obligations for high-risk AI) | §10.51 + §10.52 | The public-transparency portal binds DP-noised aggregate statistics; the model-card publication binds the model card itself. The agency's transparency claims are chain-attestable. |
| **GDPR Article 22** (automated decision-making rights — RIGHT to obtain human intervention, contest the decision) | §10.55 | The challenge-response event family IS the chain-bound expression of the GDPR Article 22 right-to-contest. A subject challenges; the agency files; the agency disposes; the chain shows the lifecycle without drift. |
| **Swiss Federal Tax Administration Act (StG)** (audit selection transparency, parliamentary oversight) | §10.51 + §10.55 | Parliamentary inquiry into selection bias reads the public-transparency portal entries (§10.51) for the demographic distribution of audit selections; reads challenge-disposition outcome rates (§10.55) for upheld/overturned ratios per cohort. |
| **OECD AI Principles** (transparency, accountability, explicability) | §10.52 + §10.51 | The model-card publication (§10.52) is the explicability anchor; the public-transparency aggregate (§10.51) is the accountability surface. |
| **NIST SP 1270 / NIST AI RMF** (algorithmic-bias monitoring) | §10.51 cohort_subtree_root_sha256 | The aggregate's cohort-subtree cross-binding lets a regulator audit whether the published aggregate truly reflects the underlying cohort the agency claims it covers. Tampering surfaces as a Merkle-root mismatch. |
| **Parliamentary inquiry / public records request** (e.g., Swiss FoIA, US FOIA) | §10.55 disposition lifecycle | Inquiry asks "show all challenges filed in 2026 with their dispositions and dispositioning judges"; the chain's state-machine + outcome enum makes the query well-defined and tamper-evident. |
| **Public-transparency claims** (agency website "we publish noised statistics with ε ≤ 1.0 monthly") | §10.51 dp_epsilon + dp_mechanism + dp_seed | The agency's public claim about its DP budget IS chain-bound. A regulator audits the seed against the noise sampler's mechanism-version hash to confirm the agency applied the stated mechanism faithfully. |

## 3. Examination workflow

A parliamentary committee or oversight body running a civic-AI audit on a Helvetian-shape AI-augmented tax-audit deployment:

1. **Scope selection.** Committee names a scope (e.g., all VAT audit-target selections in calendar 2026; all challenges filed in the same period). The agency exercises §10.31 cohort subtree disclosure to expose only the in-scope chain entries.

2. **Per-decision walk.** For each sampled audit-target selection:
   - Walk the institution's generation event (§10.47 with kind = `civic_decision_support_output`): confirm `system_prompt_sha256` matches the agency's CC8.1-named system-prompt-version registry.
   - Confirm `model_version` matches the model-card publication (§10.52) in force at the decision's `created_at_utc`.
   - When §10.48 is operated: confirm temperature, top-p, top-k, seed, model_version, model_weight_hash all in bounds.

3. **Public-transparency audit.** For each §10.51 chain entry the agency publishes:
   - Verify the §7 step 9 MAC (chain integrity) — the institution's claimed bindings are not post-hoc.
   - Audit the `dp_seed` and `dp_mechanism_version_sha256` out-of-band against the agency's public noise-sampler implementation: re-run the noise application against the underlying raw aggregate and confirm the result matches the chain-bound `aggregate_published_value` (DP correctness audit).
   - Confirm `cohort_subtree_root_sha256` matches the recomputed Merkle root over the cohort the aggregate claims to cover.

4. **Challenge-disposition audit.** For each §10.55 chain entry:
   - Walk the §10.43 lifecycle: confirm the challenge has a `filed` event, a (possibly skipped) `triaged` event, and a `disposed` event.
   - Confirm `original_decision_run_id` references an actual generation event on the chain (no orphan dispositions).
   - Confirm the `outcome` is in the canonical four (`upheld | overturned | modified | withdrawn`) or, if institution-named, that the institution's CC8.1 names the institutional outcome enum.
   - Confirm the GAP-5 signed-disposition verifies under the dispositioning judge's registered key (per the agency's reviewer-key registry).

5. **Aggregate-level findings.** The committee enumerates aggregate metrics (overturn rate by cohort, time-to-disposition distribution, dispositions-per-judge load) directly from the chain — the state-machine + outcome-enum constraints make all queries tractable without semantic drift.

## 4. Worked sample finding

> **Finding 26.4 — Helvetian Federal Tax Authority, 2026 calendar year.** Across 12,046 VAT audit-target selections (DP-noised count published per §10.51, ε = 1.0, Laplace mechanism, dp_seed bound on chain), 184 challenges were filed (1.5% challenge rate). Of those, 96 were dispositioned `upheld`, 71 `overturned`, 14 `modified`, 3 `withdrawn`. Mean time-to-disposition was 38 days. The two administrative-law judges who dispositioned over 80% of the challenges were registered under reviewer-key fingerprints `7f2a...` and `4e8c...` per the agency's reviewer-key registry; both signatures verify under the chain-bound public-key fingerprints. No challenges show out-of-order lifecycles or unknown outcomes. **The integrity of the agency's challenge-response process is chain-attestable.**

## 5. Cross-references

- Spec §10.51, §10.52, §10.55 (the wire-format primitives)
- Spec §1.2 public-transparency epistemic claim (the chain binds the noised value)
- Spec §1.5 / §10.43 GAP-2 state-machine framing
- Design `docs/design/15-civic-ai-and-post-quantum.md`
- Test vectors `045-public-transparency-dp-aggregate`, `046-public-model-card-binding`, `048-challenge-response-disposition`
- Healthcare GenAI overlay (`healthcare-genai-overlay.md`) is the clinical sibling — same composition (GAP-2 + GAP-5), different domain
