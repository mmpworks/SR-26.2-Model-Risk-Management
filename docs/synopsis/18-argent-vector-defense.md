# Story 18 — Argent Vector Defense Systems (defense-electronics WISHLIST)

**Story file:** `docs/auditor-stories/18-argent-vector-defense.md`
**Engagement type:** Two-day engagement at a defense-electronics prime contractor including a cleared-area RDT&E SCIF walk-through; CMMC 2.0 Level 3 self-certification due in eight weeks; DCMA December review eight weeks out; autonomous-systems program first flight in eleven weeks.
**Posture going in:** AI-side chain in production for 7 months on F-35 sustainment; hardware supply chain not in chain; red/black separation not in chain.
**Outcome posture:** Wishlist. Story 18 is the canonical reference for §10.56-§10.62.

## Type of audit
A wishlist-drafting engagement. Day 1 morning is a clean confirmation walk of the 7-month F-35 sustainment AI-chain deployment (~2.4M chain entries; all five sample inferences PASS). The remainder of Day 1 plus Day 2 surface seven proposed §10.x sections covering hardware supply chain (§10.56-§10.61) and red/black separation (§10.62). The §10.62 conversation happens inside the cleared-area annex SCIF; cleared-only authoring with an unclassified-by-construction projection picked up afterward.

## Interested parties (spec readers)
- **DCMA contracting officer** — defense supply-chain compliance; reads §10.21, §10.56-§10.61 plus the §10.61 CMMC overlay framework.
- **DCAA defense audit** — defense cost / property accounting; reads §10.13, §10.19, §10.56-§10.59 for incoming-test, FRU-integration, and depot-return chain integrity.
- **JCDSO / NSA cross-domain oversight** — red/black separation, cross-domain transition oversight; reads §5.0.1, §10.62, §10.62.1, §10.62.2 for the `cross_domain_transition` wire-format kind and releasability-projection determinism.
- **CMMC C3PAO assessor** — CMMC 2.0 Level 2/3 assessment; reads §10.61 plus §10.56-§10.60 for the supply-chain sub-overlays.
- **FFIEC Cybersecurity Specialist Examiner** — supply-chain controls; reads §10.21, §10.56-§10.62 for cross-sector pattern alignment.
- **CISO** — institutional cyber-posture across defense supply chain; reads §1.3, §1.4, §10.5, §10.7, §10.17 plus §10.56-§10.62.
- **Vendor management lead** — supply-chain trust path, sub-tier supplier discipline; reads §10.16, §10.21, §10.26, §10.40, §10.56-§10.60.
- **DevSecOps / SRE on-call** — runtime IR for hardware supply-chain anomalies; reads §10.4, §10.15, §10.16, §10.25, §10.56-§10.59.
- **AI vendor product-engineering team** — F-35 sustainment AI-side reference; reads §10.33, §10.35, §10.37 for airborne-fleet chain composition.
- **SDK implementer** — capture-side integration of HBOM and firmware-attestation events under §10.56-§10.57.
- **Ledger implementer** — sub-tier cross-anchor ingestion via §10.21 and §10.36 late-arrival seal discipline.
- **Standards-body reviewer** — supply-chain + red/black wishlist memo coherence; reads §0, §11, §12, §10.56-§10.62.

## Top spec sections used
- **§10.62** — Red/black separation chain integrity; introduces the `cross_domain_transition` wire-format kind; the seventh wishlist item, surfaced inside the SCIF.
- **§10.56** — Hardware bill-of-materials chain integrity; canonical-form HBOM family bound at incoming test.
- **§10.57** — Firmware-attestation chain across supplier tiers; internal-build path direct, sub-tier path via §10.21 cross-anchor.
- **§10.58** — Component cryptographic identity primitive; closed enum (PUF, SEAL chiplet, factory-provisioned key, serial+lot hash); binding-walk vs challenge-walk dispatch.
- **§10.59** — RMA / sustainment chain re-entry discipline; per-component re-entry; cannibalization as parent-children pattern.
- **§10.60** — Anti-counterfeit cross-anchor; sample-based-attestation pattern (AS6171 / DARPA SHIELD).
- **§10.61** — CMMC 2.0 / NIST 800-171 / NIST 800-161 regulator-pack overlay framework, versioned per CMMC release.
- **§10.21** — Cross-vendor model-handover schema; the cross-anchor pattern §10.56-§10.60 reuse for fab certificates, packaging travelers, sub-tier suppliers.
- **§10.35** — Edge-attestation primitive; airborne TPM signs the device-state attestation document before each F-35 chain entry.

## All cited spec sections
- **§1.2** — Epistemic-scope text; chain-entry payloads unclassified by construction.
- **§5.0.1** — Top-level wire-format kinds enumeration (`chain_entry`, `seal_record`, `anchor_record`, `cross_domain_transition`); §10.62 transition record rides under the fourth kind.
- **§7** — Verifier procedure; pre-flight dispatch keys on §5.0.1 kind enumeration.
- **§9** — Security considerations pointer; routes to threat-model design doc for cross-domain adversary framing.
- **§10.10** — Verifier dispatches against new key version per quarterly model updates.
- **§10.12** — Verifier CLI exit-code contract; §10.58 binding-walk and challenge-walk both exit 0 (PASS) with marker strings in `additional_verifications`.
- **§10.21** — Cross-vendor model-handover; the cross-anchor primitive §10.56-§10.60 reuse.
- **§10.21.1** — Sample-based-attestation cross-anchor for lot-level binding; §10.60 is the canonical institutional consumer.
- **§10.33** — Model-update events (push, pull, verify, activate) bound at quarterly model updates.
- **§10.35** — Edge-attestation primitive; airborne F-35 TPMs.
- **§10.36** — Late-arriving-entry seal discipline; Pattern A (supplemental seal) fits the DCMA workflow where suppliers ship signed attestations days after delivery.
- **§10.37** — Hierarchical Merkle aggregation; per-airframe Merkle root rolling up into daily apex root makes airborne-fleet bandwidth math work.
- **§10.56** — Hardware bill-of-materials chain integrity (`audit.hbom.incoming_test`, `audit.hbom.fru_integration`, `audit.hbom.depot_return`).
- **§10.57** — Firmware-attestation chain (`audit.firmware.build`, `audit.firmware.activate`).
- **§10.58** — Component cryptographic identity primitive with binding-walk vs challenge-walk modes.
- **§10.59** — RMA / sustainment chain re-entry (`audit.rma.depot_return`, `audit.rma.repair_complete`, `audit.rma.cannibalized`, `audit.rma.scrapped`).
- **§10.60** — Anti-counterfeit cross-anchor; lot-level destructive-testing binding.
- **§10.61** — CMMC 2.0 / NIST 800-171 / NIST 800-161 regulator-pack overlay framework with sub-overlays per CMMC release.
- **§10.62** — Red/black separation chain integrity; introduces `cross_domain_transition` wire-format kind.
- **§10.62.1** — Per-entry `audit.color_classification.side` tag (red / black / cross-domain).
- **§10.62.2** — Releasability-projection contract framework; reference projection.
- **§10.65.1** — Chassis-level cryptographic identity composition that §10.58 component-identity primitives roll up into; relevant for AESA-radar chassis attestation where TEMPEST enclosure plays the chassis role.
- **§10.65.2** — Expected-state-evolution profile chain-published via `audit.fleet.profile_updated`; structurally parallel for airframe-fleet behavior-profile discipline.
- **§13** — Stakeholder navigation; "defense-electronics prime supplier" and "autonomous-systems R&D program with red/black separation" become two new candidate stakeholders.
- **CMMC 2.0** — AC.L3-3.1.4, MA.L3-3.7.5, SC.L3-3.13.2, SI.L3-3.14.6 controls and supply-chain-risk-management family.
- **NIST 800-171** — §§3.4, 3.7, 3.10, 3.13, 3.14.
- **NIST 800-161** — SR-1 through SR-12.
- **DFARS 252.204-7012** — Incident-response binding mapped under §10.61.
- **Vectors 050, 051, 058, 063, 064** — PUF binding-walk / challenge-walk, SEAL chiplet attestation, red/black projection-hash for reference filter, black-side hash-equivalence walk.

## Synopsis

### Audit activity
Two-day engagement at the prime contractor's campus. Day 1 morning walks the F-35 sustainment AI-side chain in production for 7 months: ~2.4M chain entries across a five-week audit window; per-airframe Merkle aggregation rolls up to daily apex root under §10.37; airborne TPM attestation at every entry under §10.35; quarterly model updates under §10.33. Five sample inferences spanning a model-update boundary, a state-shift anomaly that triggered a brief grounding, and clean entries; all five PASS. Day 1 post-lunch the cleared-on subset of the team enters the cleared-area annex SCIF; the cross-domain crypto module and red-side AI inference path are walked. The §10.62 schema emerges: red-side full-payload chain entry, cross-domain transition record on the red side binding source-entry-id and releasable-hash, black-side releasable-form chain entry, two verifier modes (red-side full-chain, black-side hash-equivalence-only). Out of the SCIF; unclassified projection picked up. Supply-chain operations room walk — 1,847 BOM line items, 47 supplier-facility pins, GaN-PA-4471 part, three gaps (paper certificates of conformance, paper packaging travelers, lost provenance on RMA returns). Whiteboard §10.56-§10.61. Day 2 finalizes the wishlist memo; close-out with DCMA's relationship lead in the room.

### How the spec was used

- **§10.35** — Edge-attestation exercised on the F-35 confirmation walk.
- **§10.37** — Hierarchical Merkle aggregation exercised on the F-35 confirmation walk.
- **§10.33** — Model-update events exercised on the F-35 confirmation walk.
- **§10.10** — IKM rotation against quarterly key versions exercised on the F-35 confirmation walk.
- **§1.2** — Epistemic-scope (chain-entry payloads unclassified by construction) exercised on the F-35 confirmation walk.
- **§10.56 / §10.21** — Wishlist HBOM canonical-form family bound at incoming test, with cross-anchor to fab certificates via §10.21.
- **§10.57 / §10.21 / §10.36** — Wishlist firmware-attestation chain with internal-build path direct and sub-tier-supplier path via §10.21 cross-anchor, plus §10.36 late-arrival seal discipline (Pattern A).
- **§10.58 / §10.12** — Wishlist component cryptographic identity primitive enumerating PUF / SEAL chiplet / factory-provisioned key / serial+lot hash with binding-walk vs challenge-walk dispatch under §10.12 (both exit 0; marker strings differentiate).
- **§10.59** — Wishlist RMA re-entry with cannibalization as parent-N-children pattern.
- **§10.60 / §10.21.1** — Wishlist anti-counterfeit cross-anchor consuming §10.21.1's sample-based-attestation pattern.
- **§10.61** — Wishlist regulator-pack overlay versioned per CMMC release with sub-overlays mapping CMMC controls / NIST 800-171 / NIST 800-161 / DFARS 252.204-7012.
- **§10.62 / §5.0.1** — Wishlist introduces the `cross_domain_transition` wire-format kind under §5.0.1's enumeration.
- **§10.62.1** — Normates per-entry color-side tagging.
- **§10.62.2** — Normates the deterministic releasability-projection contract.
- **§10.65.1 / §10.65.2** — Referenced for the chassis-identity composition and the chain-published expected-state-evolution profile pattern.

### Results
Seven wishlist sections drafted: §10.56 HBOM chain, §10.57 firmware-attestation, §10.58 component cryptographic identity, §10.59 RMA / sustainment re-entry, §10.60 anti-counterfeit cross-anchor, §10.61 CMMC 2.0 regulator-pack overlay, §10.62 red/black separation chain integrity. Prime contractor commits as canonical institutional reference for §10.56-§10.61 on the F-35 production side; autonomous-systems RDT&E program commits as canonical institutional reference for §10.62. Commitment to deploy §10.56-§10.62 within twelve months of normative-text adoption with §10.62 fast-tracked to align with first flight (eleven weeks out). Wishlist memo goes to DCMA for December review, JCDSO for program review, and the spec working group.
