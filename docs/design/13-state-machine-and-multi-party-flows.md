# 13 — State machines and multi-party insurance flows (§1.5 + §10.43-§10.46)

> **What this doc is.** The design rationale for the §1.5 state-machine framing and the §10.43-§10.46 cross-cutting Phase-6 work that closes the Story-15 (Polaris Reinsurance × Lloyd's) integration gaps. Auditor's-lens convention applies — every design choice answers a question an auditor would ask.

## 1. The problem this solves

Three classes of records do not fit the v1.0 spec's *discrete-decision* shape:

1. **Long-running claims.** Insurance claims live for weeks-to-years, moving through reserve-setting, adjudication, payment, recovery, and close. Each transition has an actor, a rationale, and (often) an authorizing-policy reference. The integrity claim is "the claim's lifecycle is coherent and tamper-evident across all transitions."
2. **Multi-party reconciliation.** A reinsurance cession involves cedent + reinsurer + (sometimes) retrocessionaire + (sometimes) independent third-party adjuster. The same claim activity appears on multiple parties' chains. The integrity claim is "all parties' records of the same activity are consistent."
3. **Periodic risk-cession statements.** Bordereaux summarize a period's cessions for cedent-reinsurer reconciliation. Both parties reconcile against the bordereau; discrepancies surface in NAIC market-conduct exams. The integrity claim is "the bordereau's lifecycle is coherent and the parties agree on the bytes."

Without §10.43-§10.46, an institution operating any of these flows under chain-of-custody would have to invent its own discipline ad hoc, with no normative anchor for an examiner to test against.

## 2. Motivating story — Polaris Reinsurance × Lloyd's

Story 15 drives the design. Polaris Reinsurance is Bermuda-domiciled, ceded by a US primary insurer (different vendor's product), retroceded into a Lloyd's syndicate. NAIC market-conduct exam reaches up into Polaris. The auditor needs to trace a claim's lifecycle, confirm all parties agree on bordereau contents, and follow the third-party adjuster's activity across all parties' chains.

Five questions Polaris must answer from its chain alone:

1. **What was the lifecycle of claim X?** §10.43 chain-bound transitions, walked from `opened` to `closed`.
2. **Did all parties record the same lifecycle?** §10.43 `claim_state` events appear on each party's chain; the claim's `run_id` is consistent; the cross-walk produces matching transitions.
3. **What activity did the third-party adjuster perform?** §10.45 `chain.adjuster_anchor` events bind the adjuster's signed activity record across cedent and reinsurer chains bidirectionally.
4. **Did the bordereau reconcile cleanly?** §10.46 `chain.bordereau.*` lifecycle events bind the bordereau document hash and the reconciliation outcome.
5. **Can the auditor trace from a bordereau back to the per-claim transitions that produced it?** §10.43 `audit.claim_state.bordereau_id` provides the cross-binding.

## 3. Why §1.5 is the right framing

The pre-mortem flagged GAP-2 — the claim that one state-machine primitive should serve §10.43, §10.55, and future case-management. The shared *plumbing* is real (transition validator + chain-entry attribute schema + state-history walker — about 80 LOC). The shared *semantics* is not — claim adjudication, dispute disposition, audit-finding response are genuinely different domains.

§1.5 names the framing without forcing a unified state-machine abstraction. The shared substrate lives in `_state_machine.py` (Python) / `StateMachine.cs` (.NET): minimal, domain-agnostic, ~80 LOC. The per-domain consumers (§10.43, §10.55, future) define their own state enumerations and their own transitions tables; they call into the shared validator. CUPID-Domain-based: the seam is the chain-entry schema and the transitions-table walk; everything else stays per-section.

This is the same shape Phase 5's §10.42-via-annotation reversal followed: do the small thing, not the abstract thing. Avoid the leaky base class.

## 4. Why §10.43 splits high-level enum from institution-named substates

The pre-mortem rejected both extremes. Closed-enum-only forces a US health insurer's claim flow into a Lloyd's syndicate's shape; free-form-only loses verifier dispatch power. The §3 `chain_kind` precedent provides the model: closed normative top-level enum (`opened` / `pending` / `decided` / `closed`), institution-named substates underneath (`reserve_set_initial`, `bordereau_inclusion`, `cession_payment`, `recovery_subrogation` for Polaris; different substates for a US health insurer; different again for a personal-auto carrier).

What the verifier dispatches on cross-institution: the high-level enum's lifecycle coherence (no transition out of `closed`; no `decided` before `pending` unless the institution's CC8.1 names a path that allows it). What the institution names in CC8.1: the substate-level transitions table and any prerequisite checks.

This shape lets a NAIC examiner test cross-cedent claim-cycle KPIs against the high-level enum without needing per-cedent vocabulary, while letting cedents preserve operational reporting against their own substate enumerations.

## 5. Why §10.44 reuses §10.31 + §10.37 instead of introducing a new primitive

§10.31 (single-level cohort subtree disclosure) already exists. §10.37 (depth-N hierarchical Merkle) already exists. §10.44 (cession-cohort recursive disclosure) is the *composition* of §10.31's cohort filter with §10.37's hierarchical Merkle, plus a role attribute per level. The role attribute family (`audit.disclosure.role.*`) is the only new schema; the Merkle plumbing is reused.

The pre-mortem flagged forcing recursion into §10.31 alone as awkward (which it would be — single-level subtree disclosure has no notion of nested hierarchy) AND introducing a parallel `HierarchicalDisclosure` module as duplicative (which it would be — §10.37 already does the depth>1 Merkle work). The composition path threads between both: §10.31 gets the role attribute extension; §10.37 supplies the hierarchical Merkle; §10.44 names the cross-reference for institutions to cite in CC8.1.

Implementation cost: zero new Merkle code. The role attribute schema is one block of normative text in §10.31; §10.44 is the cross-reference target.

## 6. Why §10.45 is standalone instead of a §10.21 extension

§10.21 (cross-vendor model-handover) is *deliverer→recipient* — one-way model delivery. §10.45 (third-party adjuster anchor) is *bidirectional* — the same adjuster's activity appears on multiple parties' chains, with cross-references in both directions. The directionality is opposite, and the schemas reflect that.

Piling adjuster-specific attributes onto §10.21 would have made §10.21 incoherent (it would have to admit both deliverer→recipient and bidirectional shapes under one section). Standalone §10.45 keeps the schema tight and the cross-references explicit. CUPID-Domain-based: model handover and adjuster anchoring are different domains.

§10.45 reuses §10.31's role-aware enumeration (`cedent`, `reinsurer`, `retrocessionaire`, `independent_third_party_adjuster`) — the role vocabulary is the seam where the two sections meet. The bidirectional cross-anchor is enforced at chain-walk time: `peer_party_chain_entries` lists every other party's anchor, and the verifier walks each peer's entry to confirm the reverse-link.

## 7. Why §10.46 mirrors §10.38 (lifecycle event family) instead of §10.42 (annotated seal)

The pre-mortem flagged annotated-seal-style as wrong-shape for bordereaux. Bordereaux are *events* in a lifecycle, not periodic seals: cedent publishes, reinsurer receives, parties reconcile. Multiple parties emit events about the same bordereau. §10.42's annotation pattern is for *one-time* seal records (acquisition close); §10.38's lifecycle pattern is for *multi-event* sequences (consent given → referenced → withdrawn → expired).

§10.46's four-event family (`published` → `received` → `reconciled` → `discrepancy_resolved`) maps cleanly to §10.38's shape. The bordereau document itself is an external artifact hash-anchored via §10.19; §10.46 binds the *lifecycle*, not the document bytes themselves.

The lifecycle-coherence verifier check reuses GAP-2's `_state_machine.py` primitive: `published` → `received` is in the bordereau-transitions table; `received` → `reconciled` is too; `reconciled[discrepancy]` → `discrepancy_resolved` is too; no transition out of `reconciled[clean]` (terminal for the clean path). One transitions table, four normative events.

## 8. The GAP-3 informative-only call

Reserves and other recurring computations (model retraining cycles, periodic risk-aggregation) produce ongoing balance updates rather than one-time decisions. The pre-mortem flagged that §10.34 (training-phase integrity, already normative for AI/ML) IS the existing cryptographic substrate. Any institution operating reserve-calculation under chain-of-custody can apply §10.34's pattern today — there's no normative gap to graduate.

§10.46 carries an informative note pointing actuaries at §10.34 for the cryptographic primitive, with `audit.reserve.*` as an example attribute family. The reconciliation surface is §10.46 bordereau (reserves feed into bordereaux for cession reporting). When a future Story (a pension-administrator engagement, an actuarial-firm vendor due-diligence) provides the operational driver, the section graduates to normative-when-applicable. Phase 6 ships informative.

## 9. Test-vector design

| Vector | What it pins |
|---|---|
| `037-state-machine-transition-validator` | The GAP-2 primitive's transition-table walk. Inputs: a synthetic transitions table and a sequence of (from, to) transitions. Outputs: per-transition validity bool. The vector exercises the primitive without invoking domain semantics — pure transition-table verification. |
| `038-claim-state-lifecycle` | The §10.43 chain-entry attribute byte form. Inputs: a Polaris-shaped 6-transition lifecycle (FNOL → reserve-set → adjudication → paid → recovery → closed) with synthetic actors, rationales, and authorizing policy hashes. Outputs: per-event JCS-canonical bytes + SHA-256. The Polaris substates appear as institution-named values; the high-level enum drives lifecycle integrity. |
| `039-adjuster-anchor-bidirectional` | The §10.45 chain-entry attribute byte form for both sides of a bidirectional anchor. Inputs: a synthetic adjuster activity record, signed by a deterministic adjuster key, with cedent-side and reinsurer-side anchor entries that cross-reference each other. Outputs: per-side canonical bytes + SHA-256, plus cross-walk verification that `peer_party_chain_entries` resolves correctly in both directions. |
| `040-bordereau-lifecycle` | The §10.46 lifecycle event family byte form. Inputs: a synthetic bordereau document + a four-event sequence (published → received → reconciled[clean]). Outputs: per-event canonical bytes + SHA-256, plus lifecycle-walk verification that the events form a coherent sequence. |
| `negative/N027-state-machine-invalid-transition` | A claim transitions out of `closed` (terminal state). Verifier rejects under the §1.5 lifecycle integrity discipline. |
| `negative/N028-adjuster-anchor-missing-reverse-link` | The cedent's adjuster_anchor entry references the reinsurer's chain entry, but the reinsurer's anchor entry has no `peer_party_chain_entries` referencing the cedent. Bidirectional cross-anchor fails. |
| `negative/N029-bordereau-reconciled-before-received` | A `reconciled` event appears for a `bordereau_id` that has no prior `received` event. Lifecycle gap detected. |

Both implementations (Python and .NET) read the same vectors and assert byte-identical canonical output.

## 9.5 Verifier failure-shape convention

§10.43, §10.45, and §10.46 verifiers report integrity failures using two different shapes — the choice between them is the *positional-vs-cross-record* axis:

| Failure shape | Used by | Why |
|---|---|---|
| `WalkResult` (return value) | §10.43 lifecycle walk; §10.46 lifecycle walk | Failures are *positional* — a single transition is or isn't in the table; a from-state matches or doesn't match the prior to-state. The `first_failure_index` field is the natural payload. No cross-event invariants need to throw. |
| Typed exception (`AdjusterAnchorVerificationFailureException` / `BordereauVerificationFailureException`) | §10.45 bidirectional anchor checks; §10.46 bordereau_sha256 cross-event consistency | Failures are *cross-record* — peer A says it knows peer B but peer B doesn't know peer A; or two events on the same bordereau_id have different `bordereau_sha256` values. These have no "position" in a single chain; they have a *check label* (a/b/c/d). `WalkResult.first_failure_index` would be a meaningless field. |

§10.46 uses both shapes because it has both kinds of invariant — the lifecycle walk is positional (returns WalkResult), the cross-event hash mismatch is cross-record (raises the typed exception). The split *within* §10.46 isn't a smell; it's a faithful application of the axis to a section that crosses both invariant kinds.

A future §10.X verifier writer should ask: "is this failure positional within a single chain walk, or cross-record across chains/events?" — and pick the shape accordingly. Don't introduce a third shape; the two are enough.

## 10. Auditor's-lens review

**Q1. What if a claim's `run_id` is reused across institutions (e.g., a master broker assigns the same claim ID to all downstream parties)?**
A. §10.43 binds claim state to `(tenant_id, run_id)`, not just `run_id`. Each institution's chain has its own tenant binding; the shared claim ID appears as `run_id` on each tenant's chain. The cross-walk happens via the §10.45 `peer_party_chain_entries` references and the §10.46 `bordereau_id` cross-binding, not via the `run_id` alone.

**Q2. What if an adjuster's activity record is an unstructured PDF (loss-adjuster narrative report)?**
A. The activity record is hash-anchored (`activity_record_sha256`). Canonicalization is institution-side (the institution's CC8.1 names the canonicalization — typical: SHA-256 over the raw PDF bytes for a born-digital document; SHA-256 over a JCS-canonical structured-extract JSON for an OCR'd or extracted form). The chain binds whichever the institution names; an examiner verifies against the same canonicalization.

**Q3. What if two parties' chains record the same bordereau but the SHA-256 differs?**
A. §10.46's lifecycle integrity check (d) catches it: `bordereau_sha256` MUST be consistent across `published`, `received`, and `reconciled` events. Mismatch is a chain-integrity anomaly the verifier surfaces — both parties must investigate (typically an institution-side document-version drift; one party reconciles against an outdated draft). Vector N029 covers an adjacent case (lifecycle gap).

**Q4. What if an institution operates §10.43 but never closes a claim (claim sits in `pending` forever)?**
A. Lifecycle integrity is per-walk: as long as the events that exist are coherent, the claim is valid. An open-forever claim is operationally suspect (the institution's IR program should investigate) but is NOT a chain-integrity anomaly. NAIC market-conduct exam may flag prolonged-pending as a finding, but that's audit-side judgment.

**Q5. What if a closed claim is reopened (e.g., subrogation discovers fraud six months after close)?**
A. The institution's CC8.1 names whether the transitions table allows `closed → opened` (formally a reopen). Most institutions name this as a NEW claim with a new `run_id` cross-anchored to the closed claim via §10.21-style `parent_run_id` / `parent_seq` — the original close stays terminal; the reopen is a related-but-separate lifecycle. The chain-of-custody discipline doesn't force one shape; the institution's CC8.1 names which it operates.

**Q6. What about jurisdictional layering — Lloyd's syndicate audited by both NAIC (US-side) and Lloyd's market bureau (UK-side)?**
A. §10.46 bordereaux serve both audiences. NAIC-side cedent and Lloyd's-side reinsurer reconcile against the same bordereau bytes; both regulators can independently verify the §10.46 lifecycle from their respective chain access. The §10.45 adjuster anchor is similarly cross-jurisdictional — both parties' chains carry the SAME adjuster activity hash.

**Open issue.** §10.43 does not normate retention discipline for closed claims. NAIC requires 7-year retention typically; some EU jurisdictions require longer (Solvency II Article 35). The institution's CC8.1 names the retention floor; §10.46 bordereau retention follows the same floor. A future amendment may add a normative retention floor when a regulator-driven engagement provides the trigger.
