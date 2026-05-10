---
title: BSA SAR / Privileged-Investigation Articulation Overlay
status: informative
aligned-with:
  - 31 USC §5318(g) (Suspicious Activity Reports statutory framework)
  - 31 CFR Part 1020 (FinCEN BSA regulations for financial institutions)
  - 31 CFR §1020.320 (SAR filing requirements)
  - 12 USC §1828(x) (Federal bank examination privilege)
  - FRE 501 (privileges in federal court)
  - FinCEN Form 111 (SAR-FI; Suspicious Activity Report — Financial Institutions)
date: 2026-05-09
version: 1.0.0
---

# BSA SAR / Privileged-Investigation Articulation Overlay

> **What this doc is.** An articulation overlay mapping the FFIEC chain-of-custody specification onto Bank Secrecy Act SAR / CTR filing discipline and the broader privileged-investigation regimes (attorney-client, attorney work-product, regulatory examination privilege). Written so a BSA officer, an outside BSA-defense counsel, a FinCEN reviewer, a subpoena-cleared law-enforcement examiner, and an institution's compliance program lead can read this document alongside the spec and confirm what the chain delivers under §10.70 privileged-investigation discipline.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's BSA / AML compliance program, FinCEN-mandated SAR procedures, or the institution's privilege-management discipline. The §1.2 epistemic scope applies: the chain proves what was said and that the record was not tampered with; it does not adjudicate the substantive merit of any SAR or privilege claim.

---

## 1. Scope and reading order

This overlay covers institutions filing SARs under 31 CFR §1020.320 and operating broader privileged-investigation discipline. The canonical PRD-4 institutional reference is Northbridge Federal Savings (Story 20). Reading order: §10.70 (BSA SAR / privileged-investigation overlay); §10.69 (the reciprocal exclusion source for customer disclosure); §10.22 (redaction discipline as the parallel-but-different content-protection axis); `bsa-aml-overlay.md` (broader BSA / AML overlay).

## 2. SAR filing chain mapping

| BSA / FinCEN element | Spec section | Operational binding |
|---|---|---|
| 31 CFR §1020.320(a) (Suspicious activity reporting) | §10.70 tag schema | Chain entries supporting SAR tagged `audit.privileged_investigation = true` with `regime = "bsa-sar"` |
| 31 CFR §1020.320(c) (Filing) | §10.70 access-trail attestation | SAR-filing event itself integrity-bound; `sar_filing_id` cross-anchored to FinCEN reference |
| 31 CFR §1020.320(d) (Compliance program) | §10.18 CC8.1 cross-referencing | Institution's BSA program documented in CC8.1; §10.70 verifier dispatch named |
| 31 USC §5318(g)(2) (Confidentiality) | §10.70 role-based verifier dispatch | Non-cleared readers receive redacted-with-existence-attestation; SAR content not exposed |
| FinCEN Form 111 (SAR-FI) | §10.70 chain entries supporting the form | SAR narrative bound to the chain; FinCEN reviewers walk the chain alongside the form |

## 3. Role-based verifier dispatch

§10.70 verifier dispatches on the reader's authorization context:

| Role-claim | Mode | Exit code |
|---|---|---|
| `bsa-sar-cleared` | Full content returned | 0 (PASS) + `additional_verifications: ['privileged_investigation_full_content_returned']` |
| (no SAR-cleared role-claim) | Redacted-with-existence-attestation | 0 (PASS) + 13 (`REDACTED_WITH_EXISTENCE_ATTESTATION`) |
| `attorney-client-cleared` | Full attorney-client content returned (does NOT clear SAR content unless also `bsa-sar-cleared`) | 0 (PASS) + `additional_verifications: ['privileged_investigation_full_content_returned']` |
| (Multi-claim composition) | Cleared-content per matching role-claim; redacted-with-existence-attestation otherwise | 0 (PASS) + per-content dispatch |

The institution's CC8.1 names the role-claim taxonomy and the access-control discipline that authorizes role-claim issuance.

## 4. Reciprocal §10.69 / §10.70 composition

§10.69 customer-disclosure packets exclude §10.70-tagged entries:

- The customer's `disclosure_complete_excepting` field carries `['sar', 'privileged_investigation']` (typically).
- The customer learns there are excluded entries (categorical fact) but cannot determine specific entries.
- The chain integrity is preserved; the daily seal covers all entries including SAR entries; the chain integrity claim under the customer's session key fails for SAR entries (the customer never has the role-claim that would compute valid MACs over those entries).

## 5. Access-trail attestation

Reading §10.70-tagged content produces additional chain entries under `audit.privileged_investigation_access`:

| Attribute | Description |
|---|---|
| `reader_role_claim` | Role-claim under which access occurred |
| `reader_identity_hash` | SHA-256 of canonical reader identity (institution-named registry) |
| `accessed_entry_ids[]` | Chain-entry identifiers accessed in this read session |
| `accessed_at_utc` | Access timestamp |

The access-trail entries are themselves chain entries (NOT tagged `privileged_investigation`); FinCEN reviewers and compliance-internal audit walk them; the institution's CC8.1 names the access-trail review cadence (typically quarterly).

## 6. FinCEN reviewer / law-enforcement subpoena orientation

A FinCEN reviewer or subpoena-cleared law-enforcement examiner walking SAR-related chain entries:

1. Authenticates with `bsa-sar-cleared` role-claim per institution's CC8.1.
2. Walks the §10.70 chain entries; verifier returns full content.
3. Reviews the access-trail (`audit.privileged_investigation_access` entries) for institution-side discipline.
4. Cross-references the FinCEN-side SAR (Form 111) against the chain-bound entries via `sar_filing_id`.

## 7. Privilege-regime taxonomy (§10.70 enumeration)

| Regime | Statutory / common-law grounding |
|---|---|
| `bsa-sar` | 31 USC §5318(g) |
| `bsa-ctr-narrative` | 31 USC §5313 + FinCEN narrative discipline |
| `ofac-investigation` | 50 USC §1701 et seq. (IEEPA); 31 CFR Chapter V |
| `314a-information-sharing` | 31 USC §5311 note (USA PATRIOT Act §314(a)) |
| `attorney-client` | FRE 501; common law |
| `attorney-work-product` | FRCP 26(b)(3) |
| `internal-investigation` | Institution-named under CC8.1 |
| `regulatory-examination-privilege` | 12 USC §1828(x); state analogs |

## 8. Cross-references

- Spec sections: §10.22 redaction discipline; §10.23 consumer-correlation-index integrity; §10.69 per-customer disclosure (the reciprocal exclusion source); §10.70 (this overlay's normative anchor).
- Adjacent overlays: `bsa-aml-overlay.md` (broader BSA / AML overlay including the full event taxonomy); `cfpb-1033-overlay.md` (the §10.69 customer-disclosure overlay reciprocal).
- Design doc: `docs/design/20-privileged-investigation.md`.
- External: 31 USC §5318(g); 31 CFR Part 1020 §1020.320; 12 USC §1828(x); FinCEN Form 111; FRE 501.
