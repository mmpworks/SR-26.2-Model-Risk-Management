---
title: Fedwire / ACH Cross-Institution Chain Integrity Articulation Overlay
status: informative
aligned-with:
  - Federal Reserve Operating Circular 6 (Fedwire Funds Service)
  - NACHA Operating Rules (Automated Clearing House)
  - 12 CFR Part 210 (Regulation J — Collection of Checks and Other Items by Federal Reserve Banks and Funds Transfers Through Fedwire)
  - 12 CFR Part 229 (Regulation CC — Availability of Funds and Collection of Checks)
  - Federal Reserve voluntary cross-institution-anchor registry documentation
date: 2026-05-09
version: 1.0.0
---

# Fedwire / ACH Cross-Institution Chain Integrity Articulation Overlay

> **What this doc is.** An articulation overlay mapping the FFIEC chain-of-custody specification onto Federal Reserve Fedwire and ACH cross-institution chain integrity, using the Federal Reserve's voluntary cross-institution-anchor registry as the discovery mechanism per §10.21.3. Written so a Federal Reserve Wholesale Payments Office examiner, a Federal Reserve Bank operations lead, a participating institution's wire-room program lead, and a counterpart institution's compliance officer can read this document alongside the spec and confirm what the chain delivers under §10.71 cross-institution discipline.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's wire-operations procedures, NACHA membership documentation, or Operating Circular 6 compliance program. The §1.2 epistemic scope applies: the chain proves what was said and that the record was not tampered with; it does not certify settlement or originate-of-funds determinations.

---

## 1. Scope and reading order

This overlay covers institutions originating or receiving Fedwire or ACH transactions and participating in the Federal Reserve's voluntary cross-institution-anchor registry. The canonical PRD-4 institutional reference is Northbridge Federal Savings (Story 20). Reading order: §10.71 (cross-institution Fedwire / ACH chain integrity); §10.21.3 (registry-discovery cross-anchor primitive); §10.21 (the underlying cross-anchor schema).

## 2. Fedwire mapping

| OC-6 element | Spec section | Operational binding |
|---|---|---|
| OC-6 §VII (Settlement) | §10.71 `audit.wire.fedwire_originated` / `fedwire_received` | IMAD/OMAD bound to chain entries on both sides |
| OC-6 §IX (Reversals and amendments) | §10.71 + §10.2 operational events | Reversal events emitted under `audit.wire.fedwire_reversal` (institution-named extension) |
| OC-6 §VIII (Cutoff times) | §10.71 publication SLA in CC8.1 | ~90 seconds post-settlement publication SLA typical for participating institutions |
| Reg J §210.27 (Sender's responsibility) | §10.71 originating-side chain entries | Originating institution's chain entry binds the wire's content hash; verifier dispatches against the registry |

## 3. ACH mapping

| NACHA Operating Rules / Regulation E element | Spec section | Operational binding |
|---|---|---|
| NACHA Article Two (Origination) | §10.71 `audit.ach.originated` | ACH trace number bound to chain entry |
| NACHA Article Three (Receiving) | §10.71 `audit.ach.received` | ACH trace number bound to receiving chain entry |
| Reg E §1005.7 (Initial disclosures) | §10.69 customer-disclosure packet (when customer requests) | Customer's ACH transactions appear in §10.69 audit-trail per institution's CC8.1 |
| ACH return / dishonor / contested | §10.71 + institution-named return events | Return events emitted under `audit.ach.return` (institution-named extension) |

## 4. Voluntary cross-institution-anchor registry (anticipated form)

§10.71's discovery mechanism presupposes a voluntary cross-institution-anchor registry under §10.21.3. The anticipated operator is the Federal Reserve (or another mutually-trusted third party serving the same role for Fedwire / ACH cross-institution composition). When such a registry operates, participating institutions publish chain-entry hashes for outbound and inbound Fedwire / ACH events to the registry within institution-named SLA. Counterparts retrieve cross-anchors mechanically; the verifier walks the registry-discovery cross-anchor and confirms hash equivalence at the boundary. Where no such registry operates, §10.71 cross-institution events emit `cross_anchor_unbound` for every transaction and the institution's CC8.1 documents the unbound posture as the operative residual.

| Registry element | Spec anchor |
|---|---|
| Registry identity | `audit.registry_discovery.registry_identity` (institution-named per CC8.1) |
| Publication identifier | `audit.registry_discovery.registry_publication_id` (registry-issued) |
| Publication SLA | Institution-named per CC8.1; characteristic ~90 seconds for Fedwire, settlement-day window for ACH |
| Counterpart institution | `audit.registry_discovery.counterpart_institution` |
| Cross-anchor state | `bound` \| `published-pending-counterpart` \| `unbound` |

Specific operator identity and current participant count are institution-side observations and live in the plain-spoken companion repository's Story-20 walkthrough, not in this normative-equivalent overlay (per §0.6's citation-indirection discipline).

## 5. `cross_anchor_unbound` documented-residual discipline

Non-participating receiving institutions surface as `cross_anchor_unbound`. The institution's CC8.1 documents:

1. The participation rate (percent of outbound volume cross-anchored).
2. The non-participating-institution policy (e.g., "originate to any institution, accept residual" vs "only originate to participating institutions").
3. The residual-monitoring cadence (how the institution tracks non-participation rate and counterpart-institution onboarding).

§10.71 does not impose participation-rate floors; the institution's CC8.1 names the discipline.

## 6. Federal Reserve examiner orientation

A Federal Reserve Wholesale Payments Office examiner walking an institution's §10.71 conformance:

1. Verifies registry participation status against the institution's CC8.1.
2. Samples Fedwire transactions over the audit period; runs the §10.71 verifier; confirms `cross_institution_chain_verified` markers on participating-counterpart wires.
3. Confirms `cross_anchor_unbound` cardinality against the institution's CC8.1 residual policy.
4. Reviews ACH transactions under the same verifier dispatch with ACH-specific publication SLA scrutiny.

## 7. Cross-references

- Spec sections: §10.21 / §10.21.3 (registry-discovery cross-anchor primitive); §10.71 (this overlay's normative anchor).
- Adjacent overlays: `cfpb-1033-overlay.md` (the §10.69 customer-disclosure overlay; ACH transactions appear in §10.69 packets); `nydfs-part500-overlay.md` (state-level wire-operations discipline); `bsa-sar-overlay.md` (SAR-tagged wire transactions).
- Design doc: `docs/design/21-cross-institution-wire.md`.
- External: Federal Reserve Operating Circular 6; NACHA Operating Rules; 12 CFR Part 210 (Regulation J); 12 CFR Part 229 (Regulation CC); 12 CFR Part 1005 (Regulation E); Federal Reserve voluntary cross-institution-anchor registry documentation.
