# 20 — Privileged-investigation overlay (§10.70)

> **What this doc is.** The design rationale for the §10.70 primitive that closes the Story-20 (Northbridge acquisition close) chain-of-custody gap for Bank Secrecy Act SAR / CTR chain integrity with privileged-investigation segregation, plus the broader privilege regimes (attorney-client, attorney work-product, regulatory examination privilege) that operate under role-based verifier authorization. Auditor's-lens convention applies.

## 1. The problem this solves

Story 20 drives the design. Northbridge files Suspicious Activity Reports (SARs) under 31 USC §5318(g) — eleven SARs in Q4 2025, eight in Q1 2026. Each SAR has supporting chain entries (case-open, analyst-review events, the SAR-filing event itself) that must be:

1. **Integrity-bound** for FinCEN review and law-enforcement subpoena.
2. **Privileged** under SAR confidentiality (the customer cannot be told they are filed; the institution cannot expose SAR content under §10.69 customer disclosure).
3. **Reviewable by SAR-cleared roles** (BSA officer, FinCEN reviewer, subpoena-cleared law enforcement) with full content; non-cleared readers receive existence-attestation only.

Today's chain has no primitive for this discipline. Without §10.70, SARs are tagged informally and their content protection depends on access-control discipline outside the chain — the chain treats SAR-related entries the same as any other entry.

§10.70 closes the gap with a tag schema (`audit.privileged_investigation = true` plus `regime` discriminator), role-based verifier dispatch (cleared vs non-cleared modes with different exit codes), reciprocal §10.69 / §10.70 composition (SAR entries excluded from customer disclosure), and access-trail attestation (SAR-cleared role access produces `audit.privileged_investigation_access` chain entries).

## 2. Why §10.70 is a tag, not a new wire-format kind

Unlike §10.62 (cross-domain transition record, a new top-level wire-format kind), §10.70 is a tag on existing chain-entry kinds. Two reasons:

1. **The chain entry IS a regular chain entry.** A SAR-related event (case-open, analyst-review, SAR-filing) is operationally a chain entry under `chain_kind = "operational"` or similar; the privilege is metadata about the entry, not a different structural kind.
2. **The §7 unknown-wire-format-kind fallthrough rule does NOT apply.** PRD-3 verifiers ingesting PRD-4 chains containing §10.70-tagged entries handle them as regular chain entries; the privilege tag is informative-to-non-cleared verifiers (which dispatch on it for redaction). The fallthrough rule's role (preventing silent mis-handling of new kinds) doesn't fit the §10.70 case.

The tag schema (`audit.privileged_investigation`, `audit.privileged_investigation.regime`) is additive within v1; PRD-3 verifiers ingesting tagged entries see standard chain entries plus an opaque tag. PRD-4 verifiers dispatch on the tag to determine reader-mode behavior.

## 3. Why role-based verifier dispatch is the load-bearing mechanism

The privilege boundary is *role-based access*, not physical separation (cf. §10.62 red/black). A SAR-cleared reader (BSA officer, FinCEN reviewer, subpoena-cleared law-enforcement officer) has the role-claim that authorizes full-content read; a non-cleared reader (institution-internal compliance auditor, customer's counsel, third-party regulator) has a narrower role-claim.

§10.70's verifier accepts an authorization context at invocation time — the reader's role-claims (e.g., `--role-claim bsa-sar-cleared`, `--role-claim attorney-client-cleared`). The verifier dispatches per role-claim:

- **Cleared mode.** Full chain-entry content returned. Exit code: `0` (PASS) plus `additional_verifications: ['privileged_investigation_full_content_returned']`.
- **Non-cleared mode (redacted-with-existence-attestation).** Confirms entries exist, are integrity-bound, are tagged privileged_investigation with the specified regime, but does NOT return content. Exit code: `0` (PASS) plus exit code 13 (`REDACTED_WITH_EXISTENCE_ATTESTATION`).

Multiple role-claims compose by union. A reader cleared for SAR but not for attorney-client receives full SAR content and redacted attorney-client content within the same chain walk.

## 4. Why GAP-13 (shared verifier-authorization framework) is deferred to PRD-5

The pre-mortem identified GAP-13 as a candidate for shared cross-cutting framework — both §10.62 and §10.70 carry role-based dispatch. The mitigation deferred GAP-13 to PRD-5.

The reason: §10.62's role-claim cardinality is structurally different from §10.70's. §10.62 dispatches on a 4-tuple (red/black side × cleared/non-cleared × per-program filter × deployment environment). §10.70 dispatches on a boolean (SAR-cleared or not, per role-claim). A shared framework that supports both cardinalities risks adapter complexity at both sites greater than the savings from sharing.

PRD-4 ships §10.62 and §10.70 as freestanding implementations. PRD-5 considers GAP-13 lift conditional on a third consumer demonstrating structural fit. The deferral preserves optionality without burning engineering capacity on premature abstraction.

## 5. Why access-trail attestation is normative

Reading §10.70-tagged content produces additional chain entries under `audit.privileged_investigation_access`:

- `reader_role_claim` — the role-claim under which the access occurred.
- `reader_identity_hash` — SHA-256 of canonical reader identity (institution-named identity registry).
- `accessed_entry_ids[]` — the chain-entry identifiers accessed in this read session.
- `accessed_at_utc` — timestamp.

The access-trail entries are themselves chain entries (NOT tagged `privileged_investigation`); they are visible to FinCEN reviewers and to compliance-internal audit. The institution's CC8.1 names the access-trail review cadence.

The pattern is the *Reflexive Discipline* pattern: privileged content is rare, expensive, and high-stakes; access to it must be itself integrity-bound and reviewable. FinCEN's Section 314(a) information-sharing program already imposes similar discipline; §10.70 normates it as a chain primitive.

## 6. Why the regime enumeration is broad

§10.70's `audit.privileged_investigation.regime` enumeration covers more than BSA SAR:

- `bsa-sar` — Suspicious Activity Reports.
- `bsa-ctr-narrative` — Currency Transaction Report narratives requiring privilege.
- `ofac-investigation` — OFAC sanctions screening investigations.
- `314a-information-sharing` — FinCEN 314(a) shared information.
- `attorney-client` — Attorney-client privilege.
- `attorney-work-product` — Attorney work-product doctrine.
- `internal-investigation` — Internal investigations under privilege.
- `regulatory-examination-privilege` — Bank regulatory examination privilege (12 USC §1828(x), state analogs).
- Institution-named additional regimes documented in CC8.1.

The enumeration is open at the institutional layer (institutions can add named regimes for their privilege landscape) but closed at the verifier-dispatch layer (the verifier's role-claim mechanism dispatches on the regime string consistently). Two banks operating under different state privilege regimes use different `regime` values; the verifier dispatches uniformly.

## 7. Cross-references

- Spec sections: §10.22 redaction discipline (the post-MAC vs pre-MAC binding distinction; §10.70 is a tag-based equivalent for the privilege axis); §10.23 consumer-correlation-index integrity (privileged-investigation entries still carry the customer index for institution-side cross-referencing); §10.69 per-customer disclosure (the reciprocal exclusion source); §10.70 (this design doc's surface).
- Test vectors: 077-078 (§10.70 cleared mode + non-cleared redacted-with-existence mode).
- Auditor stories: Story 20 (Northbridge acquisition close) — the institutional-reference engagement; Henry Sundberg (BSA Officer) and Lourdes Vespertine-Ó hAodha (BSA-defense outside counsel) are the program-side reference engineers.
- Adjacent design docs: 19-customer-disclosure.md (the §10.69 sibling defining the reciprocal exclusion source); 17-red-black-separation.md (the parallel role-based dispatch pattern for §10.62, with different cardinality).
- Regulator pack: `docs/regulator-pack/bsa-sar-overlay.md` (the operative §10.70 overlay); `docs/regulator-pack/bsa-aml-overlay.md` (the broader BSA / AML overlay).
- External: 31 USC §5318(g) (SAR statutory framework); 31 CFR Part 1020 (FinCEN BSA regulations); 12 USC §1828(x) (federal bank examination privilege); FRE 501 (privileges in federal court); state-law analogs for attorney-client and work-product.
