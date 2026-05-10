---
title: CFPB Personal Financial Data Rights (12 CFR Part 1033) Articulation Overlay
status: informative
aligned-with:
  - 12 CFR Part 1033 (CFPB Personal Financial Data Rights, finalized October 2024)
  - 12 CFR Part 1002 (Regulation B / ECOA)
  - 12 USC §5481 et seq. (Consumer Financial Protection Act)
  - GDPR Article 15 (right of access; analogous regime, applicable for cross-jurisdictional posture)
  - CCPA / CPRA right of access (state analog)
date: 2026-05-09
version: 1.0.0
---

# CFPB §1033 Personal Financial Data Rights Articulation Overlay

> **What this doc is.** An articulation overlay mapping the FFIEC chain-of-custody specification onto the CFPB Personal Financial Data Rights rule (12 CFR Part 1033, finalized October 2024). Written so a CFPB Office of Supervision examiner, a covered entity's §1033 program lead, a covered entity's compliance officer responding to a customer's audit-trail request, and the customer's representative in a §1033 dispute can read this document alongside the spec and confirm what the chain delivers under §1033 discipline.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's §1033 program, customer disclosure procedures, or the technical-data-format specifications in 12 CFR §1033.301. The §1.2 epistemic scope applies: the chain proves what was said and that the record was not tampered with; it does not adjudicate whether the institution's data practices comply with §1033 substantively.

---

## 1. Scope and reading order

This overlay covers covered entities under §1033 (depository institutions, nondepository entities subject to the CFPB's regulatory authority) operating chain-of-custody coverage that supports per-customer audit-trail subset disclosure. The canonical PRD-4 institutional reference is Northbridge Federal Savings (Story 20). Reading order: §10.69 (per-customer audit-trail subset disclosure); §10.23 (consumer-correlation-index integrity, the customer-identification anchor); §10.31 (per-cohort subtree disclosure, the regulator-side parallel pattern); §10.69 documented-exception list; §10.70 (the reciprocal exclusion source for SAR / privileged-investigation entries).

## 2. §1033 right-of-access mapping

| §1033 element | Spec section | Operational binding |
|---|---|---|
| §1033.131 (Consumer's right to access covered data) | §10.69 customer-disclosure subprocedure | Per-customer Merkle subtree-disclosure plus customer-disclosure session key |
| §1033.221 (Authorized third-party receipt) | §10.69 + §10.21 cross-anchor | Disclosure packet bound to authorized recipient via institution-side authorization records |
| §1033.301 (Technical specifications for the consumer interface) | §10.69 disclosure packet schema; institution's API per CC8.1 | Disclosure packet composes with the institution's §1033 API |
| §1033.341 (Performance specifications) | Institution's CC8.1 SLA naming | 45-day disclosure SLA typical; institution-named per CC8.1 |
| §1033.421 (Data security; risk management) | §10.5 HSM custody; §10.69 customer-disclosure key derivation | Customer-disclosure session key bound to customer index; institution's IKM never exposed |

## 3. Customer-side independent verification

§1033 explicitly contemplates the consumer's ability to verify their data and audit trail. §10.69's per-customer-disclosure HKDF derivation produces a session key the customer's verifier reproduces; the customer-side independent-verification pattern proceeds without any access to the institution's IKM.

The customer's verifier receives:

1. The chain entries matching the customer's `audit.customer_correlation_index` in canonical-byte form.
2. The Merkle subtree-disclosure proof binding each entry to the daily seal's signed root.
3. The per-customer-disclosure session-key fragments (tenant_id binding + customer_correlation_index binding suffice).
4. The institution's published seal-record stream.
5. The `disclosure_complete_excepting` field documenting documented exclusions.

The customer's verifier emits `additional_verifications: ['customer_disclosure_subtree_verified', 'customer_disclosure_key_derivation_verified']` on PASS.

## 4. Documented-exception list

§10.69 normates four canonical exclusions:

| Exclusion | §1033 / regulatory grounding |
|---|---|
| `sar` | 31 USC §5318(g) SAR confidentiality (§10.70 reciprocal source) |
| `litigation_hold` | FRCP 37(e) preservation; institution's e-discovery program |
| `privileged_investigation` | Attorney-client, work-product, regulatory examination privilege (§10.70 broader regime) |
| `redacted_per_§10.22` | Pre-MAC SDK redaction; chain entry IS in packet with redaction-discipline-bound content |

The customer learns the categorical fact of exclusion (`['sar', 'privileged_investigation']` typically) without learning specific excluded entries.

## 5. Bureau examiner orientation

A CFPB examiner reviewing an institution's §1033 program walks:

1. The institution's CC8.1 §1033 control description naming the §10.69 subprocedure.
2. A sample of customer disclosures with verifier output (institution-side and customer-side).
3. The institution's SLA observance against §1033.341 (typically 45 days).
4. The institution's `disclosure_complete_excepting` cardinality across the sample (any institution-named additional exclusions documented in CC8.1 with legal grounding).

## 6. Cross-references

- Spec sections: §10.21 cross-anchor; §10.22 redaction discipline; §10.23 consumer-correlation-index integrity; §10.31 per-cohort subtree disclosure; §10.32 per-device session key derivation (HKDF parallel); §10.69 (this overlay's normative anchor); §10.70 BSA SAR / privileged-investigation overlay.
- Adjacent overlays: `cfpb-overlay.md` (broader Bureau articulation); `bsa-sar-overlay.md` (the §10.70 reciprocal); `gdpr-dsar-fulfillment.md` (GDPR Article 15 analog).
- Design doc: `docs/design/19-customer-disclosure.md`.
- External: 12 CFR Part 1033; 15 USC §1681 et seq. (FCRA); GDPR Article 15; CCPA / CPRA.
