# Story 14 — Northbridge Federal Savings (return) — bookend to Story 01, M&A integration

**Story file:** `docs/auditor-stories/14-northbridge-federal-savings-return.md`
**Engagement type:** Two-day spec-section confirmation pass on the post-merger M&A integration before the OCC's post-merger examination opens
**Posture going in:** Chained in production for 36 months across the original Northbridge perimeter; 6 months across the inherited target perimeter under the §10.24 institutional-succession composition-note amendment, paired with §10.39 successor-attestation and §10.42 backfill seal at the close of acquisition
**Outcome posture:** Confirmation engagement; the §10.39-§10.42 cross-vendor-target sections plus the §10.24 composition-note amendment exercised against production cut-over

## Type of audit
Two-day on-site at the institution's Maryland HQ for a spec-section confirmation memo before the OCC's post-merger examination opens in three weeks. The acquired institution had run a non-chain vendor for fourteen years (signed daily roll-up PDFs, no chain-of-custody product); 2,407 prior-vendor signed PDFs plus 1,823 unsigned institutional-archive PDFs constitute the pre-acquisition baseline. The cut-over window was six weeks; the institution upgraded to a release that shipped §10.39 through §10.42 six weeks before close.

## Interested parties (spec readers)
- **FFIEC IT Examiner (FDIC / OCC / FRB)** — Post-merger examination team; consumes the spec-section confirmation memo as their first read
- **M&A integration lead (acquirer)** — Diligence and post-close evidence-trail survival; reads §10.19, §10.21, §10.24, §10.39-§10.42
- **Acquired-entity transition team** — Pre-close cooperation, baseline-diary inheritance, dual-signature ceremony participation
- **Acquirer-side technical lead** — Post-close technical absorption of the acquired chain into the acquirer's coverage map
- **Chief Audit Executive (CAE)** — Calls the engagement back; partners with external auditors and OCC team
- **Audit Committee chair** — Board-level oversight of M&A integrity controls
- **General Counsel** — Legal-process posture; evidentiary defensibility of the cross-vendor-target backfill
- **Cross-vendor anchor counterparty** — Cross-vendor cross-anchor for chain-merge at M&A close (§10.40)
- **IT due-diligence lead (M&A)** — Buyer-side diligence on the target's prior-vendor PDFs
- **Big-Four assurance audit** — Cross-framework attestation across SOC, ISAE, ISO
- **Verifier implementer** — `additional_verifications: ['backfill_seal_verified']` dispatch path through §10.42
- **Reference-verifier user / OSS adopter** — Acquirer side runs the reference verifier on the inherited segment

## Top spec sections used
- **§10.39** — Institutional successor-attestation (eight-field envelope; `baseline_manifest_kind = "mixed"`; `companion_backfill_seal_run_id`; §10.17 `dual_signatures` pair)
- **§10.42** — Backfill seal discipline (one-time seal at close, five-step verifier dispatch path, `additional_verifications: ['backfill_seal_verified']`)
- **§10.41** — Chain-coverage map M&A temporal-slice extension (three partitions: pre-acquisition / cut-over window / post-cut-over with `out_of_chain_handoffs`)
- **§10.40** — Cross-vendor chain-merge cross-anchor (4,230 PDFs hashed and bound under §10.19's `audit.external_artifact.*`)
- **§10.24** — Entity succession + the composition-note amendment (GAP-1 closure, three paragraphs added as a wayfinder for the cross-vendor-target subcase)
- **§10.12** — Verdict object's `additional_verifications` array; codes 0-6 closed enumeration (exit code 7 explicitly rejected by pre-mortem)
- **§10.17** — Partition-ceremony attestation; the dual-signature pair structurally identical across §10.24 / §10.39 / §10.42
- **§0** — Document version (PRD-N) and wire-format identifier (`v1`) on independent axes; PRD-1 institutions still emit valid `v1` chain entries

## All cited spec sections
- **§0** — Document version vs wire-format identifier on independent axes
- **§0.6** — Contextual-help URL convention; §10.39-§10.42 wave shipped with companion-repo cross-vendor-target walkthrough URLs locked at draft time
- **§1.1** — Daubert four-factor grounding
- **§1.2** — Epistemic scope
- **§10** — Operational requirements
- **§10.5** — HSM custody at FIPS 140-2 Level 3+; current attestation on the partition ceremony
- **§10.6** — IKM minimum length conformance
- **§10.6.1** — IKM-generation requirements
- **§10.7** — Software-key adapter exclusion (production-disabled; dev-only flag in test environment)
- **§10.12** — Verdict object's `additional_verifications` array; closed enum 0-6 (exit code 7 rejected)
- **§10.17** — HSM partition-ceremony attestation; shared envelope-utility module across §10.24 / §10.39 / §10.42
- **§10.19** — `audit.external_artifact.*` family that §10.40 reuses
- **§10.21** — Cross-vendor handover pattern (referenced; §10.40 generalizes it for foreign-vendor-verifier-not-run case)
- **§10.24** — Entity succession with composition-note amendment for cross-vendor-target subcase (GAP-1 closure)
- **§10.39** — Institutional successor-attestation envelope
- **§10.40** — Cross-vendor chain-merge cross-anchor (informative)
- **§10.41** — Chain-coverage map M&A temporal-slice extension
- **§10.42** — Backfill seal discipline at acquisition close
- **§10.43** — Claim-state-machine (referenced)
- **§10.46** — Bordereau integrity (referenced)
- **§10.50** — Output-grounding event family
- **§10.53** — Hybrid post-quantum seal mandate; cited in pre-mortem against exit-code-7 combinatorial blow-up
- **§4.3** — HSM-rooted `sign_payload` form; v1.0b unchanged (the §10.42 metadata leaf is JCS-canonicalized and Merkle-included)
- **§13** — Stakeholder navigation; "acquirer-side IT due-diligence" candidate stakeholder

## Synopsis

### Audit activity
Day 1 walks §10.39 through §10.42 against operational reality: the acquired-side technical lead's verifier output `{ok: true, exit_code: 0, additional_verifications: ['backfill_seal_verified'], spec_section_dispatch_path: '§10.42 / steps 1-5 / PASS'}` on the chain segment covering the §10.39 + §10.42 records. Whiteboard walk of the §10.39 envelope: the eight fields, the `dual_signatures` pair structurally identical across §10.24 / §10.39 / §10.42 (validator lifted to a shared envelope-utility module after a devil's-advocate review pass caught divergent copies). The pre-mortem rejected exit-code-7 for combinatorial blow-up across §10.42, §10.53, future bonus verifications. The 2,407 prior-vendor PDFs plus 1,823 institutional-archive PDFs reconcile via §10.40 cross-anchor; all 4,230 hashes verify against archive contents. The §10.41 three-partition coverage map names the cut-over window's three out-of-chain dual-write loan-servicing handoffs; each was reconciled the next morning. Ten records traced end-to-end through the cut-over window: ten for ten.

### How the spec was used

- **§10.39** — Eight-field successor-attestation envelope under acquirer-HSM signature: target legal name and LEI (validated per RFC 9101), acquirer's HSM key fingerprint, baseline-manifest kind `mixed` (per §10.39 enumeration `prior_vendor_chain | prior_vendor_signed_pdfs | baseline_diary | mixed`), baseline-manifest SHA-256 over the JCS-canonicalized leaf list, companion-backfill-seal run-id linking bidirectionally to §10.42, `dual_signatures` pair (§10.17 from-entity / to-entity differentiation: target CFO + acquirer CFO), `effective_utc` at the close
- **§10.42** — Metadata leaf carries `seal.backfill_at_close = true` plus the bidirectional companion-attestation linkage; v1.0b `sign_payload`-bound seal with the metadata leaf JCS-canonicalized and Merkle-included alongside the 4,230 baseline-manifest leaves; Merkle root signed under the acquirer's HSM (key whose fingerprint is the same `acquirer_hsm_key_fingerprint` declared in §10.39)
- **§10.42 verifier dispatch** — Five steps: (1) read seal record, identify backfill via metadata-leaf discriminator; (2) recompute Merkle root, compare to apex; (3) cross-bind metadata leaf's `seal.backfill_baseline_manifest_sha256` against canonicalized baseline manifest SHA-256; (4) verify HSM signature; (5) bidirectional companion linkage to §10.39 envelope
- **§10.40 / §10.19** — Anchors the foreign-vendor PDFs under §10.19 reuse — no new event family, just a normative-when-applicable narrative
- **§10.41** — Names three partitions explicitly so the OCC examiner reads the coverage map first and audits each partition independently
- **§10.24** — Three-paragraph composition-note amendment closes GAP-1 with a wayfinder (rather than a new subsection) per pre-mortem
- **§10.12** — `additional_verifications` array carries `backfill_seal_verified` alongside exit code 0; codes 0-6 stay closed

### Results
Four spec-section confirmations in production at the post-merger institution. §10.39 successor-attestation: PASS, dual signatures verify, companion linkage resolves bidirectionally. §10.40: 4,230 cross-anchored PDFs verify against archive contents. §10.41: three named partitions, three out-of-chain handoffs documented and reconciled. §10.42: PASS, all five dispatch steps complete. §10.24 composition-note amendment exercised. The institution becomes the canonical institutional reference for cross-vendor-target M&A.
