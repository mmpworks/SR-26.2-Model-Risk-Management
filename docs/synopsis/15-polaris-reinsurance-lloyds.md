# Story 15 — Polaris Reinsurance x Lloyd's of London (Bermuda reinsurer + three Lloyd's syndicates ahead of NAIC market-conduct examination wave)

**Story file:** `docs/auditor-stories/15-polaris-reinsurance-lloyds.md`
**Engagement type:** Two-day pre-engagement readiness pass before the NAIC market-conduct examination wave
**Posture going in:** Chained in production for 14 months at the Bermuda reinsurer on cession-management and claim-adjudication; 9 months at the three Lloyd's syndicates; chain extends across the cedent to reinsurer to retrocessionaire boundary
**Outcome posture:** Confirmation engagement; multi-party claim-flow integrity §10.43-§10.46 production fidelity confirmed across three independent organizational tenants

## Type of audit
Two-day engagement with the team split four-and-four between Hamilton, Bermuda (AST, GMT-4) and London Lime Street (GMT in October). Time-zone difference is four hours; the team bridges by video twice daily during the overlap window. The chain crosses three independent organizational tenants (cedent syndicate to reinsurer to retrocessionaire if in play); 23 cession contracts at the reinsurer across the three syndicates produce 23 cohort subtrees per day. The NAIC market-conduct examination wave starts in eleven weeks; New York DFS, Bermuda Monetary Authority, and the PRA each receive their respective subtree disclosures.

## Interested parties (spec readers)
- **State insurance department examiner (NAIC)** — AI-decisioning evidence in personal-lines underwriting, claims triage, pricing, rate filings; primary regulator audience for the wave
- **Cedent / reinsurer / retrocessionaire** — Multi-party claim flow under the §10.43-§10.46 family; bidirectional cross-anchor counterparty
- **Independent loss adjuster (insurance)** — Cross-anchor on adjuster activity binding the same investigation under multiple parties' chains (§10.45)
- **General Counsel** — Legal-process posture across three tenants and three regulators; evidentiary defensibility of cross-jurisdiction subtree disclosures
- **Chief Compliance Officer / CRO** — Cross-jurisdiction regulatory posture (NAIC, BMA, PRA); §10.46 bordereau reconciliation discipline
- **Chief Audit Executive (CAE)** — Internal-audit ownership of the §10.43-§10.46 control evaluation; engagement-letter signatory
- **Big-Four assurance audit** — Cross-framework attestation across SOC, ISAE, ISO; multi-tenant cross-anchor verification
- **Internal audit team** — Independent verification across cedent / reinsurer / adjuster cohorts
- **Verifier implementer** — Recursive cohort-subtree disclosure dispatch (§10.44) and bidirectional adjuster-anchor verification (§10.45)
- **Standards-body reviewer** — §10.43 substate-semantics editorial pass on the December working-group agenda

## Top spec sections used
- **§10.43** — Claim-state-machine chain entries (opened / pending / decided / closed; cross-chain anchors at cession boundaries; institution-named substates governed by CC8.1)
- **§10.44** — Cession-cohort recursive subtree disclosure (23 cohorts at the reinsurer organized by cession contract; weekly subtree pulls verify byte-for-byte between reinsurer emit and Lloyd's verify across 39 pull cycles)
- **§10.45** — Independent third-party adjuster anchor (`chain.adjuster_anchor` event family with bidirectional `peer_party_chain_entries`); 142 anchors verify across three syndicates
- **§10.46** — Bordereau integrity (four-event lifecycle published / received / reconciled / discrepancy_resolved; `bordereau_sha256` cross-binding); 36 bordereaux published, 34 match, 2 discrepancies resolved
- **§10.21.2** — Parallel-evaluator composition pattern; §10.45 is its canonical instance (two independent evaluators anchored at one shared target)
- **§1.5** — Decision-event vs state-machine modeling; the GAP-2 substrate that §10.43 lifts to the claim-adjudication domain
- **§10.31** — Per-cohort subtree disclosure that §10.44 generalizes recursively for cession structure
- **§10.19** — External-artifact anchoring (referenced by contrast for the multi-party simultaneous case §10.45 dedicates a family for)

## All cited spec sections
- **§1.5** — State-machine substrate (GAP-2); the substrate §10.43 lifts to claim adjudication
- **§10.19** — External-artifact anchoring (one-way, contrasted with §10.45's bidirectional)
- **§10.21.2** — Parallel-evaluator composition; §10.45 is its canonical instance
- **§10.31** — Per-cohort subtree disclosure that §10.44 generalizes recursively
- **§10.40** — Chain-merge inheritance (one-way, contrasted with §10.45's bidirectional)
- **§10.43** — Claim-state-machine chain entries with cross-chain anchors
- **§10.44** — Cession-cohort recursive subtree disclosure
- **§10.45** — Independent third-party adjuster anchor with bidirectional `peer_party_chain_entries`
- **§10.46** — Bordereau integrity four-event lifecycle keyed on `bordereau_id` and `bordereau_sha256`
- **§13** — Stakeholder navigation; "reinsurance market-conduct examiner" candidate stakeholder

## Synopsis

### Audit activity
Day 1 opens with a joint kickoff at 8:30 AM Bermuda / 12:30 PM London on the wall screen.

The §10.43 lifecycle walk: cedent emits `chain.claim_state.transition` when a covered loss opens; the reinsurer emits its own transition with `cross_chain_anchor.cedent_chain_run_id` plus `cedent_chain_payload_sha256` binding the cedent's chain entry by run-id and SHA-256. The state-machine primitive in `_state_machine.py` runs `validate_walk` over each claim's transition sequence; 14,300 claims produce clean walks at the reinsurer over a 90-day window.

The §10.45 review at 11:30 AM walks an anchor entry showing `audit.adjuster_anchor.peer_party_chain_entries` with the cedent run-id and seq; bidirectional cross-anchor verification by activity-record SHA-256 byte-for-byte across cedent and reinsurer entries. The §10.46 bordereau lifecycle walk at 12:30 PM: 36 bordereaux across nine months, 34 match, 2 discrepancies resolved through `audit.bordereau.discrepancy_resolved` events binding the resolution-record SHA-256 and the resolving-parties array.

The 1,400-claim reconciliation runs through the afternoon — 1,000 from the marine syndicate, 250 from aviation, 150 from political-violence specialty; by Hamilton 5 PM the team is at 1,200 claims cleared, 23 subtrees extracted, 22 bordereau periods reconciled, 142 adjuster anchors verified. The Day 1 close-out surfaces a §10.43 substate-semantics question; an escalation through the firm-cleared protocol path to the spec working group confirms the read and names the December working-group editorial-pass action item already on the agenda.

### How the spec was used

- **§10.43** — Four canonical states (opened / pending / decided / closed) plus cross-chain anchors at cession boundaries are the load-bearing primitive for multi-party claim-flow integrity; institution-named substates are CC8.1-governed (marine syndicate's general average and salvage, aviation syndicate's damage-classification) so cross-jurisdiction regulators can audit claim flow without learning each institution's substate semantics
- **§10.44 / §10.31** — Generalizes per-cohort subtree disclosure to the recursive structure cession contracts produce naturally — a cession contract is a cohort, a cohort is a sub-root, and per-cohort disclosure produces sub-root + audit path to apex + leaves under that sub-root with the verifier validating the subtree against the apex under the seal's HSM signature
- **§10.44 cross-impl byte-equivalence** — Reinsurer emit and Lloyd's verify on the marine cohort for week 2026-W41 produce the same audit path, same cohort root, same apex root byte-for-byte
- **§10.45 / §10.19 / §10.40** — Normates the dedicated `chain.adjuster_anchor` event family because §10.19 (one-way external-artifact anchoring) and §10.40 (one-way chain-merge inheritance) do not cover the multi-party simultaneous case; bidirectional `peer_party_chain_entries` references make a unilateral anchor without peer reciprocation a control-completeness anomaly the verifier surfaces
- **§10.45 / §10.21.2** — Canonical instance of the parallel-evaluator composition pattern
- **§10.46** — Four-event lifecycle binds the periodic reinsurance reconciliation as a chain-bound process; verifier confirms (a) `received` follows `published` for the same `bordereau_id`, (b) `reconciled` follows `received` for the same party, (c) every `discrepancy` outcome eventually produces a `discrepancy_resolved` event, (d) `bordereau_sha256` is consistent across all three lifecycle events
- **§10.43 substate-semantics** — December editorial-pass action item; high-level transitions are what the chain binds and the verifier checks; the substate dimension is institution-side semantics under CC8.1

### Results
Four spec-section confirmations in production across the cedent / reinsurer / retrocessionaire boundary.

- **§10.43 claim-state-machine** — 14,300 transitions clean at the reinsurer, 8,400 across the three syndicates.
- **§10.44 cession-cohort subtree disclosure** — 23 cohort subtrees verify byte-for-byte across 39 weekly pull cycles.
- **§10.45 adjuster anchor** — 142 `chain.adjuster_anchor` events across three independent loss adjusters, bidirectional `peer_party_chain_entries` cross-references verify in both directions, activity-record SHA-256s match byte-for-byte across cedent-side and reinsurer-side entries, zero anomalies in 90 days.
- **§10.46 bordereau** — 36 bordereaux published, 34 match, 2 discrepancies resolved with the full four-event sequence recorded.

The substate-semantics editorial pass is on the December working-group agenda; institutional-side CC8.1 governs the substate dimension. The engagement becomes the canonical institutional reference for multi-party claim-flow integrity; the NAIC examination wave can be answered with chain output; New York DFS, Bermuda Monetary Authority, and the PRA each receive their respective subtree disclosures with byte-for-byte verifiability.

Test vectors: 037 (state-machine transition validator — the §1.5 / GAP-2 primitive), 038 (claim-state lifecycle — §10.43), 039 (adjuster-anchor bidirectional cross-binding — §10.45), 040 (bordereau lifecycle — §10.46); §10.44 has no dedicated Phase-6 vector because it generalizes the §10.31 primitive.
