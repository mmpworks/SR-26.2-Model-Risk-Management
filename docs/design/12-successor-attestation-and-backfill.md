# 12 — Successor-attestation and backfill seal (§10.39 + §10.42)

> **What this doc is.** The design rationale for the cross-vendor-target M&A discipline. Spec §10.39 (`chain.successor_attestation`) and §10.42 (backfill seal) compose with §10.24 entity succession to close the chain-discontinuity gap when an acquirer absorbs a target whose pre-acquisition records are not under a Herald-conformant chain. The auditor's-lens convention applies — every design choice answers a question an auditor would ask.

## 1. The problem this solves

§10.24 already covers the institutional-succession case where the acquirer can directly continue the target's chain — same `(tenant_id, run_id)` keying, dual-signature handoff, post-succession entries seal under the to-entity. The acquirer's representation cites §10.24 by section number and the deal closes with a clean continuity story.

§10.24 does NOT cover the case where the acquired entity ran a *different vendor's* chain, ran a *baseline-diary record system* (paper-and-PDF retention with no chain at all), or ran a *mixed-shape* system (some chain, some baseline-diary). In every cross-vendor-target case, the chain *discontinues* at acquisition close because there is no acquired-side Herald-conformant chain to continue. The acquirer cannot extend the same `(tenant_id, run_id)` over records that were never in a Herald-conformant chain in the first place.

Without §10.39 + §10.42, the acquirer has three bad options:

1. **Re-key as a new genesis on day-of-close.** The chain proves nothing about pre-acquisition records — a post-close auditor asking "what did the target do in the 18 months before close?" gets the answer "we don't know cryptographically; we have the seller's binder."
2. **Hash the seller's records into the acquirer's coverage map ad hoc.** Some institutions do this informally. There is no normative section number for the acquirer's representation to cite, no signature discipline binding both parties to the inheritance, and no test-vector-pinned byte form for a verifier to confirm.
3. **Refuse to close until the target migrates onto a Herald-conformant chain.** Operationally infeasible for any deal closing within a normal M&A timeline.

§10.39 + §10.42 close the gap at the spec-section-citation level, the cryptographic-binding level, and the verifier-dispatch level.

## 2. Motivating story — Northbridge / Cape Madeline

The Story 14 narrative drives the design. Northbridge Federal Savings (an institution already running a conformant chain; Story 01 was their first engagement) acquires Cape Madeline Bank & Trust. Cape Madeline ran on a competing vendor (LedgerKnot) for the prior 14 months, then had been on a baseline-diary system for the 30 months before LedgerKnot. The acquisition close is on date D; Northbridge needs to be able to answer four questions from the acquirer's chain alone after close:

1. **What records did we inherit?** Answered by the §10.39 `baseline_manifest_sha256` — the canonicalized list of inherited artifacts, hash-bound on the acquirer's chain at close.
2. **Who attested to the inheritance?** Answered by the §10.39 `dual_signatures` — both Cape Madeline's CISO and Northbridge's CISO sign the inheritance event.
3. **Are the inherited LedgerKnot artifacts byte-identical to what the chain says they were?** Answered by §10.40 cross-anchor entries — each LedgerKnot signed daily-roll-up PDF is hashed and anchored under §10.19 `audit.external_artifact.*`.
4. **What about the 30-month baseline-diary period?** Answered by the §10.42 backfill seal — Northbridge's HSM signs a one-time seal record over the Merkle root of the canonicalized baseline-diary manifest, producing a chain-shaped integrity envelope retroactively over the inherited records.

The backfill seal is what an 18-month-lookback auditor reads to confirm Cape Madeline's pre-acquisition baseline-diary records have not been edited post-close. Without it, an audit-firm asking "show me Cape Madeline's loan-origination records from 14 months before close" gets PDFs the acquirer can hand over but no cryptographic substrate to bind their integrity. With it, the acquirer's chain alone is the integrity-bound retrieval substrate.

## 3. Why two events, not one

The design splits the cross-vendor-target work into two distinct events: the §10.39 successor-attestation event (what was inherited, who signed for it, when) and the §10.42 backfill seal record (the cryptographic substrate that lets a verifier confirm "the records are byte-identical to what the chain says"). Two reasons for the split:

1. **Different shapes.** The §10.39 event is an `audit.*`-namespace operational event under §10.2 (lives in the chain entries stream). The §10.42 backfill seal is a v1.0b sign_payload seal record (lives in the seal stream). Conflating them into one shape would force a hybrid event-and-seal record that breaks the §3 `chain_kind` enumeration.
2. **Different optionality.** When the inherited records are under a foreign-vendor chain (LedgerKnot's signed roll-up PDFs), §10.39 is REQUIRED but §10.42 is NOT — the cryptographic substrate is the §10.40 cross-anchor entries (each PDF hash-bound under §10.19). When the inherited records are under a baseline-diary shape (no foreign chain), §10.42 IS required because there is no cross-anchor target. Splitting the events lets the institution emit the right complement per `baseline_manifest_kind`.

The companion linkage (§10.39 `companion_backfill_seal_run_id` ↔ §10.42 `seal.backfill_companion_attestation_run_id`) makes the bidirectional reference explicit so the verifier can traverse between them.

## 4. Why no new wire-format kind for the backfill seal

The pre-mortem on this design explicitly considered making §10.42 a *new top-level wire-format kind* alongside the existing seal-record kind. The conclusion: NO new kind. The annotation pattern is the right call.

The decision rests on the §10.36 supplemental-seal precedent. §10.36 introduced "annotated seal record + verifier-dispatches-on-attribute" as the pattern for late-arriving entries within an active operational period. The verifier reads `seal.late_pattern` on the seal record and dispatches to the §10.36 verification path. The pattern is by now a known shape across the spec; the §10.42 backfill seal occupies the same shape (one-time seal at acquisition close, annotated with `seal.backfill_at_close = true`).

Three CUPID/DRY arguments weighted the call:

1. **Wire-form preservation.** The v1.0b sign_payload form is locked. A new top-level kind would have required either (a) extending the wire-form identifier beyond `'v1'` or (b) introducing a parallel wire-form discriminator. Both are larger amendments than necessary; the annotation pattern preserves `'v1'` untouched.
2. **DRY on signing path.** A new top-level kind would have duplicated the §4.3 sign_payload binding, the HSM signing discipline, the §10.24 `dual_signatures` plumbing, and the Merkle apex-root verification. Extending the existing seal record with a discriminating attribute reuses every one of these without duplication.
3. **Verifier dispatch parity.** §10.36 already trains the verifier to dispatch on a seal-record attribute. Adding §10.42 follows the trained pattern; introducing a new kind would have required a second dispatch surface.

The trade-off accepted: a verifier that doesn't recognize `seal.backfill_at_close` falls through to the §4.2 path and produces an integrity-anomaly finding (the Merkle root over the baseline manifest does not match the day's chain entries, because there are no day-of-close chain entries). This is the desired failure mode — a §10.42-unaware verifier should NOT silently pass; it should surface the surprise. The fall-through behavior is what makes the discriminator-attribute pattern safe.

## 5. Why the verdict object's `additional_verifications` field, not exit code 7

The pre-mortem also reversed the manifest's call on exit code 7 (`BACKFILL_SEAL_VERIFIED`). The conclusion: NO new exit code. The `additional_verifications` array on the verdict object is the right place to report bonus verifications.

§10.12 defines a closed seven-element exit-code enumeration (0/1/2/3 terminal + 4/5/6 streaming-state). Adding exit code 7 says "PASS *plus* a bonus verification also passed" — that's an attribute of PASS, not a separate verdict. Worse, Story 17 (the forthcoming hybrid post-quantum work) would have wanted exit codes 8 and 9 by the same logic. Future bonus verifications would want 10, 11, 12. The exit-code enumeration becomes a combinatorial soup of "PASS + ⟨condition₁⟩", "PASS + ⟨condition₂⟩", "PASS + ⟨condition₁⟩ + ⟨condition₂⟩" — the integrator's 0-vs-non-zero contract decays.

The verdict object's `additional_verifications` array absorbs the entire wave through one schema field. Exit 0 stays exit 0; the metadata travels alongside. The closed enumeration of bonus-verification names grows additively as new spec sections normate new bonus verifications, but the exit-code enumeration stays at seven elements. CI runners and shell scripts read 0-vs-non-zero unchanged; harnesses that want the bonus information read the structured verdict.

The field is documented in `07-verifier-design.md` §11. The reference implementations are `_verdict.py` (Python) and `VerifierVerdict.cs` (.NET); the test-vector-pinned shape is `036-verdict-additional-verifications`.

## 6. Threat-model alignment

The `09-threat-model.md` adversary model has six adversary classes (A through F). The cross-vendor-target M&A discipline composes with the existing classes; it does not introduce new ones.

| Adversary | Concern under M&A | How §10.39 / §10.42 close it |
|---|---|---|
| A — Host-side chain tampering | Acquirer-side post-close edit of the inherited baseline manifest. | The §10.39 `baseline_manifest_sha256` is bound under the acquirer's per-event MAC; tampering surfaces at the next chain walk. The §10.42 backfill-seal Merkle root is HSM-signed; tampering surfaces at signature verification. |
| C — Server-side or privileged-insider history rewrite | Vendor-side backfill of a fictitious baseline manifest after close. | Both events require dual signatures (acquired-institution authority + acquirer authority) per §10.17. A vendor without both signatures cannot fabricate a backfill that verifies. |
| F — Edge / rotational adversary at the boundary | Cross-vendor-target chain merge at the inheritance moment. | The §10.39 attestation is the integrity-bound record of who signed at that moment; the §10.42 backfill seal is the integrity-bound substrate over the inherited records. Both bind to the cut-over window the institution's CC8.1 names per §10.41 (which is itself bound to the chain via `chain.coverage_map_published`). |

A new residual: a target that submits a *fraudulent baseline manifest* before close (the manifest the acquirer signs against is itself a lie). §10.39 / §10.42 detect post-close edits to the manifest and to the records the manifest enumerates, but they do not detect pre-close fraud in the manifest's construction. The closure for that residual is *vendor due-diligence on the target* during the deal — the buyer's audit firm tests the manifest against external evidence (third-party SOC 2 reports, regulator correspondence, customer-account confirmations) before the acquirer's CISO signs the §10.39 event. The discipline is operational, not cryptographic; it is documented in `docs/m-and-a-handoff.md` (the §10.24 normative-supplement).

## 7. Test-vector design

Three positive vectors and three negative vectors pin the byte form:

| Vector | What it pins |
|---|---|
| `034-successor-attestation` | The §10.39 envelope canonical bytes. Inputs: synthetic acquired-institution legal name, a deterministic LEI, a baseline manifest SHA-256 (computed from a labeled byte-string seed), a `baseline_manifest_kind` value, an acquirer-HSM key fingerprint, a fixed `effective_utc`, and a §10.17-shaped dual_signatures pair. Outputs: JCS-canonical bytes + SHA-256 hex. |
| `035-backfill-seal` | The §10.42 backfill-seal record canonical bytes. Inputs: a synthetic 8-leaf institutional baseline manifest, the §10.42 backfill metadata-leaf attributes, a §10.17-shaped dual_signatures pair, and the v1.0b sign_payload inputs. Outputs: metadata-leaf canonical bytes + canonical-bytes SHA-256, the Merkle root over (8 baseline leaves + 1 metadata leaf) under canonical RFC 6962, the v1.0b sign_payload form bytes + sign_payload SHA-256. The Ed25519 signature byte form itself is NOT pinned in case 035 — case 018 pins the v1.0b signing path generally; case 035 pins what is distinctive about §10.42 (the metadata-leaf shape and the Merkle composition). |
| `036-verdict-additional-verifications` | The verdict object's structured shape. Three sub-cases: PASS with empty `additional_verifications`; PASS with `["backfill_seal_verified"]`; PASS with two values (forward-compat with Story 17 hybrid PQ). Outputs: JCS-canonical bytes + SHA-256 hex per sub-case. |
| `negative/N024-acquirer-hsm-signature-mismatch` | The §10.39 acquirer-HSM key fingerprint claims one key; the dual_signatures fingerprint computes a different key. Verifier surfaces the mismatch. |
| `negative/N025-backfill-merkle-root-corrupted` | The §10.42 backfill-seal Merkle root is corrupted by a single-byte flip. Verifier surfaces the recomputation mismatch. |
| `negative/N026-additional-verifications-invalid-string` | The verdict object carries an unknown string in `additional_verifications`. Verifier (under `--strict`) rejects; under default mode the unknown string passes through as opaque diagnostic. |

Both implementations (Python and .NET) read the same vectors and assert byte-identical canonical output. The cross-impl byte-equivalence pin is the conformance oracle.

## 8. Composition with §10.41 chain-coverage-map M&A temporal-slice extension

The cut-over window the §10.39 attestation and §10.42 backfill seal are emitted within is the same window §10.41 names in the chain-coverage map's three-partition discipline (pre-acquisition / cut-over / post-cut-over). The composition is what an 18-month-lookback auditor reads to reconstruct the M&A integration state at any moment of the cut-over.

| Composition reference | What it provides |
|---|---|
| §10.41 pre-acquisition partition | The acquirer's coverage map *before* day-of-close. |
| Day-of-close — §10.39 + §10.42 | The cryptographic inheritance moment. The successor-attestation and backfill seal are emitted within the cut-over window's first day. |
| §10.41 cut-over window partition | Each migrated system's chain-instrumentation activation date. The successor-attestation's `companion_backfill_seal_run_id` references the §10.42 record emitted in the same window. |
| §10.41 post-cut-over partition | The unified institution's coverage map after the cut-over window closes. The post-cut-over map carries forward the §10.40 cross-anchor entries (if any) so foreign-vendor roll-up artifacts remain anchored. |

A verifier walking the period samples any week of the cut-over and finds (a) the chain-coverage-map version in force that week per §10.41, (b) the §10.39 successor-attestation event referenced by the map (if the week is the first cut-over week), and (c) the §10.42 backfill seal companion (if applicable). Reconstruction is mechanical; no institution-side narrative is required.

## 9. CC8.1 control description

The institution's CC8.1 control description names, under the M&A scenario:

- The cut-over window's start and end dates per §10.41.
- The migration tranches per §10.41.
- The §10.39 baseline-manifest canonicalization (typically JCS-canonical sorted array of `{kind, identifier, sha256}` tuples).
- The §10.39 acquirer-HSM key fingerprint and the change-management procedure governing its rotation.
- The §10.39 `baseline_manifest_kind` chosen for this engagement (`prior_vendor_chain` / `prior_vendor_signed_pdfs` / `baseline_diary` / `mixed`) and the rationale.
- The §10.40 foreign-vendor roll-up retention posture (when applicable).
- The §10.42 backfill seal's HSM signing discipline (when applicable).

The audit-firm tests the named values against the chain entries the acquirer produces post-close. CC8.1's discipline is what surfaces an institution-side mismatch (e.g., the named cut-over window does not align with the §10.41 coverage-map publications) as a control-completeness finding under audit-procedures P-6.

## 10. Auditor's-lens review

**Q1. What if the acquirer's HSM is compromised between the §10.39 attestation and the §10.42 backfill seal?**
A. The two events are emitted within the same cut-over window — typically within the same day-of-close seal — under the same HSM. A compromise during that window invalidates both events; the verifier surfaces the compromise as a signature failure on either event. The institution's CC8.1 names the day-of-close HSM-rotation discipline (typically: no rotation during the cut-over window's first 48 hours).

**Q2. Why is `baseline_manifest_kind` an enumeration rather than a free-form string?**
A. The verifier dispatches on it. `prior_vendor_chain` requires §10.40 cross-anchor entries; `baseline_diary` requires §10.42 backfill seal; `mixed` requires both. A free-form string would force the verifier into ad hoc institution-by-institution dispatch logic. The closed enumeration with an institution-named extension path (per CC8.1) is the same shape §10.24 uses for `kind`.

**Q3. What if the target had no records at all (a shell-corp acquisition)?**
A. The institution's CC8.1 names the absence; §10.39 emits with an empty baseline manifest (`baseline_manifest_sha256 = SHA-256(empty canonical-form bytes)`) and `baseline_manifest_kind = "baseline_diary"` with the rationale documented. The §10.42 backfill seal emits over the empty Merkle root. The discipline produces a chain-bound record of "we inherited no records" rather than silently omitting the inheritance event.

**Q4. What if the target's prior-vendor data is encrypted at rest with a key the acquirer cannot retrieve?**
A. The acquirer hashes the encrypted bytes (the SHA-256 over the canonicalized encrypted form is the binding hash) and emits §10.40 anchors per encrypted artifact. Decryption is a separate concern handled outside the chain; the integrity binding holds whether the bytes are decryptable or not.

**Q5. What about an acquirer who acquires multiple targets in a short window?**
A. Each target produces its own §10.39 + (§10.40 or §10.42) event family, each under its own dual_signatures pair. The acquirer's chain carries N successor-attestation events for N targets. The institution's CC8.1 names the per-target documentation; the verifier walks each independently.

**Open issue.** The §10.40 foreign-vendor anchor pattern depends on the foreign vendor's roll-up artifacts being retainable at the acquirer post-close. A foreign vendor's terms-of-service that prohibits redistribution of signed roll-up PDFs (rare but possible for some closed-circle vendor contracts) would block §10.40. The closure is contractual: the acquirer's deal-closing checklist includes a pre-close confirmation of the right to retain foreign-vendor roll-up artifacts post-close. Documented in `docs/m-and-a-handoff.md`; not closed in spec text.
