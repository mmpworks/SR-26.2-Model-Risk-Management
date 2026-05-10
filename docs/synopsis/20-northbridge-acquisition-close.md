# Story 20 — Northbridge Federal Savings (banking acquisition-close CONFIRMATION)

**Story file:** `docs/auditor-stories/20-northbridge-acquisition-close.md`
**Engagement type:** Three-day engagement at a tier-1 community / regional bank during the week of the bank's acquisition of its chain vendor. Bookend to Stories 01 and 14.
**Posture going in:** Vendor chain in production for 54 months across the unified post-Cape-Madeline perimeter; §10.39-§10.42 institutional-succession sections fully operational; §10.41 cut-over partition closed at the 24-month boundary; the unified chain runs as a single seal. §10.69-§10.71 shipped in vendor release N+5 four weeks before the engagement.
**Outcome posture:** Confirmation.

## Type of audit
A vendor-side confirmation engagement plus an institutional-succession bookend. The team confirms §10.69 per-customer audit-trail subset disclosure, §10.70 BSA SAR / privileged-investigation overlay, and §10.71 cross-institution Fedwire / ACH chain integrity; runs a §10.39-§10.42 continuity check on the unified perimeter; the acquired chain vendor is itself absorbed into the institution as a wholly-owned technology services subsidiary mid-engagement.

## Interested parties (spec readers)
- **FFIEC IT Examiner (FDIC / OCC / FRB)** — examination cycle for tier-1 community / regional bank under §1033 + BSA + Fedwire participation; reads §1.1, §1.2, §7, §10.12, §10.18, §13.
- **CFPB consumer-protection examiner** — §1033 disclosure right; reads §10.11, §10.23, §10.69 for per-customer subset disclosure with documented exclusions.
- **Federal Reserve / OCC payments examiner** — Fedwire / ACH cross-institution integrity; reads §10.21.3, §10.71 for the registry-discovery cross-anchor pattern.
- **Bank end-customer (§1033 requestor)** — requests own customer-data subset disclosure; reads §10.23, §10.69.
- **Counterparty bank (Fedwire / ACH cross-anchor)** — cross-institution wire / ACH integrity counterparty; reads §10.21.3, §10.71.
- **Audit Committee chair** — board-level oversight of acquisition-close chain controls; reads §0.5.3, §1.1, §1.2, §13.
- **M&A integration lead (acquirer)** — diligence and post-close evidence-trail survival; reads §10.19, §10.21, §10.24, §10.39-§10.42.
- **General Counsel** — §1033 customer disclosure plus BSA SAR privileged-investigation posture; reads §1.1, §5.2, §10.13, §10.69, §10.70.
- **Forensic accounting / litigation-support** — BSA SAR plus customer-§1033 evidence preservation; reads §5.2, §10.13, §10.69, §10.70.
- **SOC 1 / SOC 2 engagement team** — section 4 description and CUEC verification under acquisition-close conditions; reads §7, §10.13, §10.18-§10.19.
- **Big-Four assurance audit** — cross-framework attestation across acquisition close; reads §7, §10.12-§10.13, §10.18.
- **Reference-verifier user / OSS adopter** — institution-side verifier execution against §10.69-§10.71 markers; reads §10.12, §10.26, §11.

## Top spec sections used
- **§10.69** — Per-customer audit-trail subset disclosure; CFPB §1033 customer-data right; per-customer-disclosure HKDF derivation.
- **§10.70** — BSA SAR / privileged-investigation overlay; role-based verifier dispatch (cleared full content vs redacted-with-existence-attestation).
- **§10.71** — Cross-institution Fedwire / ACH chain integrity; registry-discovery cross-anchor per §10.21.3 against voluntary Federal Reserve registry.
- **§10.39** — Institutional successor-attestation; the spirit applies to the bank's absorption of the chain vendor.
- **§10.40** — Cross-vendor chain-merge cross-anchor; operational on unified perimeter.
- **§10.41** — Chain-coverage-map M&A temporal-slice extension; cut-over partition closed at 24-month boundary.
- **§10.42** — Backfill seal discipline; baseline-diary records bound at acquisition close.
- **§10.31** — Per-cohort subtree disclosure; the mathematical primitive under §10.69 customer-disclosure.
- **§10.21.3** — Registry-discovery cross-anchor for cross-institution chains; Federal Reserve registry under §10.71.

## All cited spec sections
- **§5.0.1** — Top-level wire-format kinds enumeration; §7's pre-flight dispatch keys on it; cross-institution chain entries ride at all four kinds across the Fedwire-ACH chain.
- **§7** — Verifier procedure; pre-flight dispatch.
- **§10.21** — Cross-vendor model-handover; the cross-anchor primitive §10.71 is derived from.
- **§10.21.3** — Registry-discovery cross-anchor for cross-institution chains mediated by a third-party registry (Fedwire, FedNow, FINRA); §10.71 is the canonical institutional reference for this sub-pattern.
- **§10.22** — Redaction discipline; the closed-canonical exception list under §10.69 includes `redacted_per_§10.22`.
- **§10.23** — Consumer-correlation index integrity; §10.69 customer-id mapping under Shape 1 / Shape 2.
- **§10.31** — Per-cohort subtree disclosure; the Merkle subtree-disclosure mathematics §10.69 builds on.
- **§10.39** — Entity succession (`chain.entity_succession`); legal-entity change of operator with required dual signatures bound under v1.0b seal.
- **§10.40** — Cross-vendor chain-merge cross-anchor; operational on unified perimeter.
- **§10.41** — Chain-coverage-map M&A temporal-slice extension (pre-acquisition / cut-over-window / post-cut-over); cut-over partition closed at 24-month boundary.
- **§10.42** — Backfill seal discipline (`seal.backfill_at_close=true`); one-time seal at acquisition close producing chain-shaped envelope retroactively over inherited baseline-diary records.
- **§10.69** — Per-customer audit-trail subset disclosure; per-customer-disclosure HKDF derivation, Merkle subtree-disclosure proof, documented exclusions (`sar`, `litigation_hold`, `privileged_investigation`, `redacted_per_§10.22`).
- **§10.70** — BSA SAR / privileged-investigation overlay (`audit.privileged_investigation`); role-based verifier dispatch returns full content for cleared readers, redacted-with-existence-attestation otherwise.
- **§10.71** — Cross-institution Fedwire / ACH chain integrity (`audit.wire.*`, `audit.ach.*`); registry-discovery cross-anchor per §10.21.3 against voluntary Federal Reserve registry; cross_anchor_state ∈ {`bound`, `unbound`, `published-pending-counterpart`}.
- **§13** — Stakeholder navigation; "tier-1 community / regional bank under §1033 + BSA + Fedwire participation" — canonical institutional reference.
- **Appendix A.11** — `consumer_index.*` schema family (`consumer_id_hash`, `run_id`, `seq`, `relationship`, `attestation.*`); tenant-scoped derivation §10.23 and §10.69 reference.
- **Appendix A.12** — `chain.successor_attestation` schema (acquired_entity_legal_name, baseline_manifest_kind, dual_signatures, companion_backfill_seal_run_id) §10.39 references.
- **CFPB §1033** — Personal Financial Data Rights rule; §10.69 normates the chain-integrity-bound audit-trail right.
- **31 USC 5318(g) / FinCEN form 111** — BSA filing context for §10.70.
- **Vectors 077-083** — `077-customer-disclosure-hkdf-derivation`, `078-customer-disclosure-subtree-with-exception-list` (§10.69); `079-privileged-investigation-cleared-mode`, `080-privileged-investigation-non-cleared-redacted-with-existence` (§10.70); `081-cross-institution-fedwire-cross-anchored`, `082-cross-institution-fedwire-cross-anchor-unbound`, `083-cross-institution-ach-variant` (§10.71).

## Synopsis

### Audit activity
Three-day engagement at the bank's Concord, New Hampshire campus. Day 1 morning walks §10.69: ~240 customer §1033 audit-trail requests per month; the per-customer-disclosure HKDF derivation `HKDF_INFO_BASE || '|' || utf8(tenant_id) || '|' || utf8('customer-disclosure') || '|' || utf8(customer_correlation_index)` is byte-identical to vector 077; the team walks eight customer disclosures (including a small-business owner from Q1 2026); each verifies in ~18 seconds against ~12,000 chain entries over 4-year retention; verifier emits `customer_disclosure_subtree_verified` and `customer_disclosure_key_derivation_verified` markers on PASS. Day 1 afternoon walks §10.70 with outside BSA-defense counsel: Q4 2025 had 11 SARs, Q1 2026 had 8; team walks three SAR-filing chains under both cleared and non-cleared verifier modes; non-cleared returns redacted-with-existence-attestation; cleared returns full content under SAR-cleared role-claim; §10.69 / §10.70 composition holds. Day 2 morning walks §10.71 with the Federal Reserve Bank of Boston Wholesale Payments Office observer on video bridge: ~14,000 Fedwires/month and ~280,000 ACH/month emit cross-institution cross-anchors; ~340 institutions participate in the Fed's voluntary registry; ~78% of outbound volume is cross-anchored; team walks five wires including a non-participating-bank `cross_anchor_unbound` documented residual and a returned wire. Day 2 afternoon: acquisition closes; institutional-succession packet executed. Day 3 walks §10.39-§10.42 continuity on the unified perimeter from the institution side. Close-out Day 3.

### How the spec was used

- **§10.69 / §10.31** — Normates a per-customer-disclosure HKDF derivation distinct from the institution's tenant key, with the Merkle subtree-disclosure mathematics from §10.31 — the customer independently verifies their data slice's chain integrity without exposing the institution's IKM or other customers' chain entries.
- **§10.69 exception list** — Closed-canonical disclosure-completeness exception list is four values: `sar`, `litigation_hold`, `privileged_investigation`, `redacted_per_§10.22`.
- **§10.70 / §10.69** — Normates the privileged-investigation tag, the role-based verifier authorization, and the §10.69 / §10.70 reciprocal composition (§10.69 excludes §10.70-tagged entries; §10.70 enforces role-based authorization at chain-walk time).
- **§10.70 access events** — SAR-cleared role access produces `audit.privileged_investigation_access` chain entries that FinCEN can audit.
- **§10.71 / §10.21.3** — Normates the wire-format, cross-anchor binding, and verifier procedure for cross-institution chain integrity via the Federal Reserve's voluntary registry — the canonical institutional reference for §10.21.3's registry-discovery cross-anchor pattern.
- **§10.39-§10.42** — Continuity check confirms the §10.41 cut-over partition closed cleanly at the 24-month boundary; the unified chain runs as a single seal across the unified perimeter.
- **§10.39 (in reverse)** — Institutional-succession spirit applies to the bank's absorption of the chain vendor — the acquired entity is itself the chain vendor, not just another instrumented institution.
- **§10.39-§10.42 + §10.69-§10.71** — Composition cited in the bank's acquisition disclosure to the OCC.

### Results
Three spec-section confirmations: §10.69 — eight customer disclosures verified, ~18 seconds per disclosure, byte-identical to vector 077; §10.70 — three SAR-filing chains verified under both cleared and non-cleared verifier modes; §10.71 — five wires walked including documented `cross_anchor_unbound` residual, Federal Reserve observer signed attestation. §10.39-§10.42 continuity check passed on unified perimeter. The bank becomes canonical institutional reference for §10.69-§10.71 and for the "tier-1 community / regional bank under §1033 + BSA + Fedwire participation" §13 stakeholder. The institutional-succession composition (§10.39 applied "in reverse" — the acquired company is the chain vendor itself) closes the bookend to Story 01's clean baseline and Story 14's M&A integrity engagement.
