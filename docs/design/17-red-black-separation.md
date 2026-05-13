# 17 — Red/black separation chain integrity (§10.62)

> **What this doc is.** The design rationale for the §10.62 primitive that closes the Story-18 (Argent Vector / TALON-X) chain-of-custody gap for cleared-environment systems crossing the red/black boundary via Type-1 cross-domain crypto modules. Auditor's-lens convention applies.

## 1. The problem this solves

Story 18's TALON-X RDT&E program drives the design. TALON-X is an attritable autonomous UAS — on-board AI target-classification, EO/IR-and-SAR sensor payload, Type-1 NSA-evaluated cross-domain crypto module gating the transition from classified ("red") inference output to unclassified-encrypted ("black") comms uplink, TEMPEST-qualified flight computer. Phase 2 RDT&E; first flight in eleven weeks at engagement time.

The classified subsystem (red side) operates inside a TEMPEST-shielded enclosure with a red-side HSM-coupled ledger. The crypto module strips classified metadata to a releasable form, encrypts under Type-1 algorithms, and emits to the comms uplink. The black side carries the encrypted releasable payload outward to the ground control station.

Without §10.62, the chain has two problems:

1. **The chain can't span the red/black boundary.** Today's chain captures red-side AI inference cleanly; the black-side payload is in flight; nothing chain-bound proves that the black-side payload corresponds to a specific red-side inference event without leaking red content.
2. **A black-side verifier can't attest to red-side existence without seeing red content.** A regulator (NSA evaluator, JCDSO program reviewer, AOC examiner) running outside the cleared facility needs to verify integrity claims spanning the boundary; they can't get red-side IKM or red-side content; the chain has no primitive for hash-equivalence-only attestation.

§10.62 closes both. The cross-domain transition record on the red side carries (a) the source red chain-entry id, (b) a deterministic *releasable-hash* projection of the red payload, and (c) the cross-domain module's NSA-issued attestation. The black-side chain entry carries the same releasable-hash. A black-side verifier walks the boundary by hash equivalence; never sees red content; produces a PASS verdict bounded by exit code 11 = `BLACK_SIDE_PASS_RED_NOT_WALKED`.

## 2. The releasability-projection contract

The releasable-hash is the load-bearing primitive. It must be:

1. **Deterministic.** Same red payload → same projection on every invocation. Cross-implementation byte-equivalence per the test-vector corpus.
2. **No red-side content leakage.** The projection MUST NOT contain (verbatim or by inference) any field, value, or summary derived from the red payload's classified content. Acceptable projection content is institution-named releasable categories (classification kind, decision class, releasable timestamp), counters (decision sequence number), and constants from the institution's releasable-content catalog.
3. **Versioned.** Filter referenced by version; institution-named filter version updates tracked in CC8.1 with change-management discipline.
4. **Test-vector grounded.** Each conformant per-program filter ships with at least one byte-identical test vector demonstrating the deterministic projection for a fixture red payload.

The contract is normative (§10.62.2); the per-program filter implementation is institution-determined. PRD-4 ships the TALON-X filter as the reference projection (vector `063-red-black-projection-talon-x`). Future programs (TALON-Y, hypothetical Navy autonomous-USV programs, classified medical-imaging cross-domain regimes) ship per-program filters under the same contract.

The pre-mortem flagged a failure mode: a vendor implementation that subtly leaks red-side content into the projection (e.g., projecting the rounded confidence score as a "releasable" attribute when the rounding bins still discriminate the classified-class membership). The contract's "no red-side content leakage (verbatim or by inference)" clause is the guard; the test-vector corpus demonstrates compliance for the reference filter; per-program filter reviews must prove the same.

## 3. Why §10.62 is a new top-level wire-format kind

The cross-domain transition record is structurally different from a chain entry, a seal record, or an anchor record. It binds a red chain entry on the red side, carries a releasable-hash projection bridge to the black side, and references a cross-domain module attestation. None of the existing kinds fit cleanly.

Adding §10.62 as a new top-level wire-format kind requires three normative pieces:

1. **The unknown-wire-format-kind fallthrough rule (§7).** Pre-PRD-4 verifiers ingesting PRD-4 chains containing §10.62 records must NOT silently mis-handle them. The fallthrough rule (added in this same wave) requires verifiers to emit an anomaly line, dispatch on `additional_verifications: ['unknown_kind_present']`, and continue chain processing.
2. **Format-version preservation.** §10.62 is additive within `format_version = "v1"`; the wire-format-kind enumeration extension pattern was already established for PQC §10.53 dual-signature seals. §10.62 follows that precedent without breaking the v1 byte-form.
3. **Test-vector coverage of both verifier modes.** The corpus has two §10.62 vectors: red-side full walk (063) and black-side hash-equivalence walk (a sibling). Both are byte-deterministic for the reference filter.

## 4. Why two verifier modes are normative

A red-side verifier — operated inside the cleared facility with red-side IKM access — walks both red-side chain entries and the cross-domain transition record's full payload, including re-running the institution's filter against the red payload and confirming the bound releasable-hash matches. This is the institutional self-verification mode.

A black-side verifier — operated outside the cleared facility (regulator, third-party auditor, downstream ground control station) — never has red-side IKM and never sees red-side content. The black-side verifier walks black-side chain entries and the cross-domain transition record's bound releasable-hash; it confirms each black-side entry's payload hash matches the cross-domain transition record's releasable-hash for the corresponding transition. The integrity claim spans the red/black boundary by hash equivalence; the verifier produces a PASS verdict (exit code 11 marker = `BLACK_SIDE_PASS_RED_NOT_WALKED`).

The two-mode design is symmetric to §10.70's role-based dispatch (cleared vs non-cleared SAR readers), but with a structural difference: §10.62's red/black boundary is *physical and procedural* (TEMPEST enclosure, Type-1 module, classified subsystem); §10.70's privileged-investigation boundary is *role-based access discipline* (BSA officer, FinCEN reviewer, attorney-cleared). The distinction is preserved through the wishlist manifest's deferred GAP-13 lift: §10.62 and §10.70 each ship freestanding in PRD-4; the question of whether the verifier-authorization-context primitive should be lifted to a shared framework is deferred to PRD-5 conditional on a third consumer demonstrating structural fit.

## 5. Why color-classification tagging is mandatory

§10.62.1 requires every chain entry on a §10.62-conformant institution's chain to carry `audit.color_classification.side`. This isn't an optional diagnostic — verifiers walking a mixed chain need to dispatch on the side tag to determine which entries are walkable in which mode. A black-side verifier that encounters a red-side chain entry without a side tag would fail-closed (refuse to walk); the side tag is the dispatch surface.

The institution's CC8.1 names the classification-level taxonomy under `audit.color_classification.classification_level`. The black side typically carries `unclassified`; the red side carries the institution's mission-classification levels (`secret`, `top-secret`, `unclassified-cui`, etc.). The classification levels are institution-determined; the spec's role is the structural binding, not the level taxonomy.

## 6. Cross-references

- Spec sections: §7 unknown-wire-format-kind fallthrough rule; §10.12 verifier exit-code contract (exit code 11); §10.21 cross-anchor (cross-domain module attestation); §10.62 full normative section; §10.62.1 color-classification tagging; §10.62.2 releasability-projection contract.
- Test vectors: 063 (TALON-X reference projection); paired vector for black-side walk.
- Auditor stories: Story 18 (Argent Vector / TALON-X) — the institutional-reference engagement.
- Adjacent design docs: 16-hardware-supply-chain.md (the §10.56-§10.61 sibling for the supply-chain side of Argent Vector); 14-generation-and-hitl.md (parallel for §10.50 clinical decision-support).
- Regulator pack: `docs/regulator-pack/defense-cleared-environment-overlay.md`; `docs/regulator-pack/cmmc-overlay.md` (CMMC 2.0 controls applicable to cleared environments).
- External: NSTISSAM TEMPEST/2-95; CNSSI 7000; NSA cross-domain-solution evaluation framework; CMMC 2.0; CSfC (Commercial Solutions for Classified) program (parallel solutions for non-Type-1 commercial cross-domain).
