# 15 — Civic AI, post-quantum, and long-retention (§1.2 + §10.51-§10.55)

> **What this doc is.** The design rationale for the §1.2 public-transparency epistemic-claim amendment (GAP-7) and the §10.51-§10.55 primitives that close the Story-17 (Helvetian Federal Tax Authority) chain-of-custody gaps for civic-AI deployments under parliamentary inquiry, public-transparency obligations, NIST PQC migration, and 60-year tax-archive retention. Auditor's-lens convention applies.

## 1. The problem this solves

Story 17 drives the design. Helvetian's AI-augmented VAT audit-target selection scores 4.2M Swiss businesses monthly; the top 12,000 are flagged for examiner review. A National Council parliamentary inquiry committee will examine the system in 11 weeks. Swiss tax archive law mandates 60-year retention. NIST PQC migration is on the 2030 horizon.

Five questions Helvetian must answer from its chain alone:

1. **What aggregate counts has the institution published?** §10.51 binds the DP-noised aggregate published on the regulator's transparency portal.
2. **What model card was public on date X?** §10.52 binds the model-card publication trail via §10.19.
3. **Will the chain be verifiable by my grandchildren?** §10.53 lifts dual-algorithm posture to normative-when-applicable for long-retention regimes; §10.54 normates decadal re-sealing under the then-current cryptographic suite.
4. **Can taxpayers challenge the AI's audit-target selection?** §10.55 normates the challenge-response chain-bound discipline composing GAP-2 state-machine + GAP-5 HITL.
5. **What is the public-transparency epistemic claim form?** §1.2's GAP-7 addition names the DP-bound publication claim distinctly from the regulator-disclosure claim.

Without §1.2 amendment + §10.51-§10.55, every answer comes from institution-side logs — no chain-bound integrity claim. With them, the chain alone answers all five.

## 2. Why GAP-8 ships as `_public_transparency.py`-internal, not a standalone primitive

Phase 6 (GAP-2 state-machine) and Phase 7 (GAP-5 HITL) shipped standalone primitives because each had ≥2 consumers in the §10.39-§10.55 wave. GAP-8 has *one* consumer in the foreseeable wave (§10.51). CUPID-Domain-based: a "shared primitive" with one consumer is over-abstraction; the helpers belong inside the consumer module until a second use case forces externalization.

The pre-mortem flagged this: build only what's actually shared. The DP-aggregator helpers (Laplace noise application, Gaussian noise application, mechanism-version-hash computation, ε budget tracking) live as private functions in `_public_transparency.py`. If a future Phase-9+ surface adds a second DP consumer, the helpers extract cleanly to `_dp_aggregator.py`. Until then, YAGNI.

## 3. Why §10.51 binds the noised aggregate, not the raw aggregate

The pre-mortem rejected binding the raw aggregate. Two reasons:

1. **The chain becomes a side-channel for the un-noised value.** If the chain holds the raw aggregate, anyone with chain-read access (regulators, auditors, third-party verifiers, future researchers) can read sensitive un-noised data. The whole point of DP is the un-noised value is too sensitive to publish. Binding it on a public-transparency chain defeats the purpose.
2. **The integrity claim form differs.** Binding the noised aggregate means "this is what we published"; binding the raw aggregate means "this is what we measured before publishing." The first is the public-facing claim a transparency portal needs. The second is the auditor's separate claim — and the auditor verifies it out-of-band against the institution's raw substrate.

The §10.51 design parallels §10.48 stochasticity attestation: bind the *parameters* (DP mechanism, ε, seed, mechanism-version hash) so a regulator with separate access to the raw substrate can reproduce the noise application; the chain does not pretend to validate noise correctness. The chain is the integrity foundation; DP correctness is the regulator's audit.

## 4. Why §10.52 reuses §10.19 instead of introducing a new family

The pre-mortem rejected `audit.model_card.*` as a new event family. §10.19 `audit.external_artifact.*` was designed for exactly this shape: hash-anchor an external document, optionally cite a canonical identifier, bind the anchor under chain integrity. §10.40 (cross-vendor cross-anchor, Phase 5) used §10.19 for foreign-vendor PDFs; §10.52 uses it for model cards.

The institution-named `kind = "model_card"` discriminator on the existing §10.19 schema is the *only* new thing §10.52 needs. The institution's CC8.1 names the model-card canonicalization (typical: SHA-256 of UTF-8 markdown bytes). A reader interested in "what version of the model card was public on date X?" reads the chain for `kind = "model_card"` events and walks the publication history.

CUPID-Idiomatic: §10.19 is the existing pattern; §10.52 is the use-case-specific narrative wrapper. Zero new code.

## 5. Why §10.53 amends §4.3.2 instead of introducing a new wire form

The dual-algorithm pattern is fully baked into the spec since PRD-2:

- §4.2 line 393: `signatures` list schema
- §4.3.2 line 542: per-algorithm `sign_payload` (Variant B)
- §4.3.2 line 544: AND-security
- §7 step 11 line 933: verifier dispatch
- Test vector `015-dual-algorithm-cosigned-seal`: byte-pin

Today the posture is RECOMMENDED ("v1.x candidate-normative"). §10.53 lifts it to NORMATIVE-when-applicable for institutions in long-retention regimes during the NIST PQC migration window. The substrate is unchanged; the *normativity* is the lift.

This is the cleanest possible Phase-8 §10.53 outcome. No new wire-format kind. No new sign_payload variant. No new exit code. The existing test vector 015 becomes the §10.53 normative pin. The institutional CC8.1 names the migration window opening date and the legacy-algorithm retirement date.

A future v1.x amendment retiring Ed25519 (when NIST formally deprecates it for new use, and the dual-window has run for the policy-required transition period) flips §10.53 from "dual-algorithm during migration" to "post-quantum-only after retirement." The substrate is ready for both states.

## 6. Why §10.54 follows the §10.42 annotated-seal pattern

Phase 5's pre-mortem reversed §10.42 backfill seal from "new wire-format kind" to "annotated seal record + verifier-dispatch-on-attribute." §10.54 decadal re-sealing is operationally the same shape — a one-time signing event over a baseline manifest at each decadal boundary. Same shape, same annotation pattern, same v1.0b sign_payload byte form.

The discriminating attributes (`seal.resealed_at_decadal_boundary = true`, window timestamps, `seal.resealed_under_algorithm`, `seal.resealed_generation_index`, `seal.resealed_previous_generation_anchor_sha256`) ride on the existing seal record. The verifier dispatches on `seal.resealed_at_decadal_boundary` to the §10.54 verification path; institutions not operating long-retention regimes never see §10.54 records.

Composition with §10.53 hybrid PQ: when an institution operates both, the re-seal record is itself co-signed under both legacy and PQC algorithms via the §4.2 `signatures` list. The `seal.resealed_under_algorithm` names the *primary* algorithm at the re-seal moment.

## 7. Why §10.55 mirrors §10.50 instead of subsuming it

§10.50 (clinical decision support output review) and §10.55 (audit-target challenge-response) compose the same two primitives (GAP-2 state-machine + GAP-5 HITL). Could one section subsume both?

The pre-mortem rejected subsumption. The DOMAINS differ:

- §10.50 is *clinical* (FDA, HIPAA, EU AI Act Article 14, GDPR Article 22 in healthcare context). Outcomes: clinician_edit / grounding_pass / grounding_fail / hallucination_detected.
- §10.55 is *civic-AI* (tax authorities, regulatory enforcement, civic-benefit eligibility, parliamentary inquiry, FOIA). Outcomes: upheld / overturned / modified / withdrawn.

CUPID-Domain-based: the shared substrate IS GAP-2 + GAP-5; everything domain-specific stays per-section. Forcing one section to cover both produces a leaky base class — the outcome enumeration would be the union of both sets, the authorizing-policy regime would need to discriminate domain vs. domain, the regulator-pack overlay split would land awkwardly.

Two parallel sections, each with their own outcome enum and authorizing-policy framework, is the right shape. §10.55 cross-references §10.50 ("the clinical sibling") so a future writer adding §10.X-shape consumers sees the pattern and chooses appropriately.

## 8. Test-vector design

| Vector | What it pins |
|---|---|
| `045-public-transparency-dp-aggregate` | The §10.51 chain-entry byte form for a Helvetian-shape DP-noised VAT-audit aggregate. Inputs: aggregate kind, period, Laplace mechanism, ε=1.0, deterministic noise seed, mechanism-version hash, published value. Outputs: JCS-canonical bytes + SHA-256. |
| `046-public-model-card-binding` | The §10.52 chain-entry byte form. Inputs: §10.19 attribute set with `kind = "model_card"`, model identifier, model-card SHA-256, publication timestamp. Outputs: canonical bytes + SHA-256. (Reuses §10.19 schema; pinning the institution-named-kind value.) |
| `047-decadal-resealing` | The §10.54 metadata-leaf canonical bytes only. Inputs: decadal-boundary window timestamps, prior-generation baseline-manifest SHA-256, `seal.resealed_under_algorithm`, generation index 1, previous-generation-anchor SHA-256. Outputs: metadata-leaf canonical bytes + SHA-256. The full §10.54 seal record (with the `signatures` list per §4.2 + Merkle composition over prior-generation seal records) is built around this metadata leaf at signing time; case 047 pins only the metadata leaf so cross-impl byte-equivalence is testable without a full PQC signing harness. |
| `048-challenge-response-disposition` | The §10.55 chain-entry byte form for a Helvetian-shape taxpayer challenge to an AI-flagged audit. Inputs: original-decision cross-binding, outcome `"overturned"`, signed-disposition object per GAP-5. Outputs: canonical bytes + SHA-256. |
| `negative/N033-dp-noise-seed-tampered` | The §10.51 event's `dp_seed` is altered post-publication; reproducibility audit out-of-band would fail. |
| `negative/N034-decadal-reseal-previous-anchor-mismatch` | The §10.54 event's `seal.resealed_previous_generation_anchor_sha256` references a prior-generation seal that doesn't exist on the chain (forged generation chain). |
| `negative/N035-challenge-response-disposition-out-of-order` | The §10.55 disposition event arrives before the original-decision cross-reference is resolvable on the chain (filed → triaged → disposed lifecycle violated — or any of: disposition without prior filing, unknown decision, double-terminal disposition). Variant D (out-of-CC8.1 outcome) is a control-completeness finding, NOT a chain-integrity failure. |

§10.53 reuses existing vector `015-dual-algorithm-cosigned-seal`. The spec text §10.53 names vector 015 as the normative pin.

## 9. Auditor's-lens review

**Q1. What if the institution's transparency portal publishes both noised AND raw aggregates (e.g., raw aggregates published quarterly to a regulator behind authentication; noised aggregates published publicly)?**
A. Two separate §10.51 events, each binding what was actually published to its respective audience. The institution's CC8.1 names which audience each event serves. Both events compose under chain integrity; neither claims to bind the other audience's view.

**Q2. What if the institution operates §10.54 decadal re-sealing and a re-seal generation's algorithm is later broken?**
A. The institution emits an additional re-seal under the next-current cryptographic suite, advancing the generation index. Past generations remain on the chain as historical record; current verifiers walk the most recent re-seal generation's signature. The chain accumulates re-seal generations across the retention period; an examiner reading at year T+50 walks generations 0 → 1 → 2 → 3 → 4 to confirm the current signature is verifiable under modern cryptography.

**Q3. What if a taxpayer challenge under §10.55 is dispositioned by an administrative-law judge whose key is later compromised?**
A. Forward-only revocation per the GAP-5 reviewer-key-registry discipline. Past dispositions remain verifiable under the historically-registered key (the chain integrity-bound the fingerprint at signing time). New dispositions cannot be signed under the revoked key. Same shape as §10.10 IKM rotation discipline.

**Q4. What if §10.51 DP parameters are mis-configured (ε=10 instead of ε=1) and the noise is too weak?**
A. The chain binds ε=10 honestly. A regulator's out-of-band audit catches the misconfiguration and surfaces it as a privacy-control finding. The chain is the integrity foundation, not the privacy-correctness foundation. The institution's CC8.1 names the ε-budget bounds and the change-management procedure.

**Q5. What if the institution operates §10.55 but the original AI-decision chain entry has been edited?**
A. Chain entries are integrity-bound by per-event MAC and daily Merkle seal. An edited original-decision entry surfaces at §7 step 9 (MAC mismatch) when the chain is verified. The §10.55 disposition's `original_decision_run_id` / `original_decision_seq` cross-reference is verifiable: a verifier can walk to the original-decision entry, confirm its integrity, and confirm the §10.55 disposition references the un-tampered entry.

**Q6. What about the parliamentary-inquiry context — Steve testifies independently of Dawn's audit team?**
A. The §10.55 chain-bound dispositions are independently verifiable from the chain alone — a parliamentary-inquiry committee receives the chain artifacts and runs the verifier. Steve's separate testimony covers the technical design; Dawn's separate audit memo covers operational fidelity. Per the recusal protocol the firm has on file, Steve and Dawn submit parallel testimony; the committee receives both as independent inputs.

**Open issue.** §10.51 ε-budget *accumulation* over a coverage period (each publication consumes some of the institution's overall ε budget) is institution-side discipline; the chain binds per-publication ε but does not aggregate across publications. A future v1.x extension may add `audit.public_transparency.cumulative_epsilon_consumed` to track the running total. Documented but not closed in v1.0.

## 10. Composition matrix — Phase 8 reuses everything

| Phase 8 section | Reuses from prior phases |
|---|---|
| §10.51 | §10.31 / §10.44 cohort subtree disclosure (optional cohort-root cross-binding) |
| §10.52 | §10.19 `audit.external_artifact.*` (the substrate) |
| §10.53 | §4.3.2 (the substrate, lifted to normative-when-applicable); §4.2 `signatures` list; §7 step 11; existing vector 015 |
| §10.54 | §10.42 annotated-seal pattern; §10.36 supplemental-seal precedent; §10.53 dual-algorithm composition |
| §10.55 | §1.5 / §10.43 GAP-2 state-machine; GAP-5 HITL primitive; §10.50 composition pattern (clinical sibling) |
| GAP-6 | §11 References — list edit only |
| GAP-7 | §1.2 epistemic-scope — new sub-paragraph |
| GAP-8 | `_public_transparency.py`-internal helpers; not externalized as a primitive |

Phase 8 is the most-reuse phase of the §10.39-§10.55 wave. Three new modules (one with internal helpers); zero new primitives; zero new wire-format kinds; zero new exit codes. The wave's substrate has been built up over Phases 5-7; Phase 8 spends the substrate cleanly.
