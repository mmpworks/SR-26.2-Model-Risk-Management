# NAIC Market-Conduct Examination Overlay

> **Purpose.** Operational mapping for institutions whose chain-of-custody work crosses NAIC market-conduct exam scope: primary insurers, reinsurers, retrocessionaires, and the third-party adjusters / claims administrators who support them. Anchors against spec §10.43-§10.46 (Phase 6 / Story 15) — claim-state machine, recursive cession-cohort disclosure, third-party adjuster bidirectional anchor, and bordereau lifecycle.

## 1. Why this overlay exists

NAIC market-conduct exams test how an insurer (or reinsurer, ceded into) handles claims, complaints, settlement, and recovery. The auditor needs to trace per-claim activity, confirm bordereaux reconcile cleanly between cedent and reinsurer, and follow third-party adjuster activity across all parties' chains. Without §10.43-§10.46 chain bindings, the auditor must ad-hoc-reconcile spreadsheets; with them, the chain alone is the integrity-bound retrieval substrate.

This overlay maps the §10.43-§10.46 chain artifacts to the NAIC Market Regulation Handbook examination procedures and to the operational discipline insurers and reinsurers operate around them.

## 2. Mapping table

| NAIC examination procedure | Spec section | What the chain shows |
|---|---|---|
| Claim handling — timeliness | §10.43 | `chain.claim_state.transition` events with `transition_utc` per state; auditor walks the lifecycle and confirms transitions occurred within institution's stated SLAs. |
| Claim handling — actor authority | §10.43 | `audit.claim_state.actor` + `audit.claim_state.authorizing_policy_id` / `authorizing_policy_sha256`. Auditor confirms the actor was authorized under the policy version named at transition time. |
| Claim handling — substantive decision rationale | §10.43 | `audit.claim_state.rationale`. Free-form per CC8.1; auditor reads rationale alongside the institution's claim-handling manual. |
| Multi-party reconciliation — bordereau integrity | §10.46 | Four-event lifecycle (`published` → `received` → `reconciled` → optional `discrepancy_resolved`). Auditor walks the lifecycle for each period; `bordereau_sha256` consistency across events is verifier check (d). |
| Multi-party reconciliation — discrepancies | §10.46 | `audit.bordereau.reconciliation_outcome = "discrepancy"` events trigger institutional IR program engagement; the `discrepancy_resolved` event closes the matter on chain. Open discrepancies older than the institution's SLA are exam findings. |
| Cession-cohort disclosure | §10.31 + §10.44 | Role-aware recursive subtree disclosure (`audit.disclosure.role.*`) lets the cedent expose only its claims to the reinsurer, the reinsurer expose only its retroceded claims to the retrocessionaire, etc. Auditor exercises subtree disclosure for the cohort under exam. |
| Independent third-party adjuster activity | §10.45 | `chain.adjuster_anchor` events on cedent and reinsurer chains; `peer_party_chain_entries` cross-references each side. Auditor confirms (a) bidirectional peer references resolve, (b) `activity_record_sha256` consistent across parties. |
| Reserve calculation integrity (informative) | §10.34 + §10.46 GAP-3 note | Recurring computation pattern; `audit.reserve.*` events emit per period, reconciled through bordereau. Informative for v1.0; future amendment may graduate. |

## 3. Examination workflow

A NAIC market-conduct examiner running a sample-based test on an insurer operating chain-of-custody:

1. **Sample selection.** Examiner names a sample population (e.g., 100 claims paid in calendar Q2 2026). The institution exercises §10.31 / §10.44 subtree disclosure to expose only the sampled claims' chain entries — claims outside the sample are NOT disclosed, but their existence in the parent tree is provable via the unmodified Merkle apex root.

2. **Per-claim lifecycle walk.** For each sampled claim, the examiner walks the §10.43 `chain.claim_state.transition` events in `transition_utc` order. The verifier (per spec §7) confirms (a) the lifecycle is coherent, (b) every transition is in the institution's CC8.1-named transitions table, (c) every authorizing policy hash is consistent across the claim's events.

3. **Adjuster-activity walk.** For claims that involved a third-party adjuster (institution flag in CC8.1), the examiner walks the §10.45 `chain.adjuster_anchor` events on the institution's chain AND the corresponding events on each peer party's chain. The bidirectional cross-anchor verifier confirms reverse-link consistency and shared activity-record hash.

4. **Bordereau period reconciliation.** For each cession period falling within the exam window, the examiner walks the §10.46 four-event lifecycle. `bordereau_sha256` consistency across events is verifier check (d); `reconciliation_outcome` per period flags discrepancies for follow-up. Open discrepancies older than 90 days (or the institution's CC8.1-named SLA) are exam findings.

5. **Cross-binding verification.** Each claim transitioning to `closed` SHOULD reference the bordereau period that recorded the cession (`audit.claim_state.bordereau_id`). The examiner samples this cross-binding to confirm period-level reconciliation matches per-claim lifecycle.

## 4. Discrepancy-handling discipline

Per §10.46, when a `reconciled` event carries `reconciliation_outcome = "discrepancy"`, the institution's IR program MUST investigate. The chain-bound discipline:

1. The receiving party emits `audit.bordereau.reconciled` with `outcome = "discrepancy"` and `reconciliation_record_sha256` binding the discrepancy report.
2. Both parties engage in bilateral resolution (out-of-band correspondence, claim re-cession, period adjustment).
3. When the discrepancy is resolved, BOTH parties emit `audit.bordereau.discrepancy_resolved` with `resolving_parties = [<cedent_id>, <reinsurer_id>]` and `resolution_record_sha256` binding the resolution memorandum.
4. An open discrepancy with no `discrepancy_resolved` event after the institution's CC8.1-named SLA window is a control-completeness finding the examiner surfaces.

The chain provides the timeline; the discipline is institutional.

## 5. Third-party adjuster engagement-contract requirements

For §10.45 to operate cleanly, the engagement contract between the institution and the third-party adjuster MUST establish:

- **Adjuster-issued chain entry signing key.** The adjuster signs `activity_record_signature_b64` over the canonical activity record. The institution's CC8.1 names the public-key registry and the rotation procedure.
- **Activity-record canonicalization.** The institution's CC8.1 names how activity records (often unstructured PDFs) are canonicalized — typical: SHA-256 over the raw PDF bytes for a born-digital report; SHA-256 over a JCS-canonical structured-extract JSON for an OCR'd or extracted form. The institution and the adjuster agree on the same canonicalization.
- **Cross-chain access.** The cedent and reinsurer agree to grant each other read-credential access to anchor entries (NOT to other claim entries) so the §10.45 bidirectional verifier dispatch can resolve `peer_party_chain_entries` references.

The engagement contract is the operational anchor; the chain binds the activity.

## 6. Storey 15 reference — Polaris × Lloyd's

The Polaris Reinsurance × Lloyd's syndicate scenario (forthcoming auditor story 15) exemplifies cross-jurisdictional NAIC + Lloyd's market-bureau audit. The key features:

- Cedent: US primary insurer on a different vendor's product
- Reinsurer: Polaris Reinsurance (Bermuda-domiciled, TesseraSeal native)
- Retrocessionaire: Lloyd's syndicate (UK-side)
- Third-party adjuster: Marsh Adjusting Services LLC (NY-licensed, operating across all parties)

The §10.43-§10.46 family produces a complete chain-bound record of: per-claim lifecycles (§10.43), per-period bordereau reconciliations (§10.46), per-adjuster bidirectional activity anchors (§10.45), all rolled up into cession-cohort disclosure (§10.44 / §10.31) when the NAIC exam (US-side) or Lloyd's market-bureau exam (UK-side) calls for it.

## 7. Cross-references

- Spec §1.5 (decision-event vs state-machine modeling)
- Spec §10.31 / §10.44 (cohort + recursive subtree disclosure)
- Spec §10.43 (claim-state-machine)
- Spec §10.45 (third-party adjuster anchor)
- Spec §10.46 (bordereau lifecycle)
- Spec §10.34 (recurring-computation integrity, applicable to reserves per the GAP-3 note in §10.46)
- Design `docs/design/13-state-machine-and-multi-party-flows.md`
- Test vectors `037`, `038`, `039`, `040`

## 8. Operational checklist for the institution

Before each §10.43-§10.46-bound engagement (NAIC market-conduct exam, Lloyd's market-bureau audit, internal claim-cycle KPI reporting):

- [ ] CC8.1 names the institution-specific claim-state transitions table (with substates and authorizing policies)
- [ ] CC8.1 names the third-party adjuster public-key registry and rotation procedure
- [ ] CC8.1 names the bordereau-document canonicalization
- [ ] CC8.1 names the discrepancy-resolution SLA (typically 90 days)
- [ ] Chain entries for the period under exam are integrity-verified per §7
- [ ] Subtree disclosure for the sample population is exercised per §10.31 / §10.44
- [ ] §10.45 bidirectional anchors resolve cleanly for all sampled adjuster-involved claims
- [ ] §10.46 lifecycle walk is clean (no missing events, no `bordereau_sha256` mismatches) for all periods in scope
