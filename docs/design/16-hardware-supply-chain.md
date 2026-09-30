# 16 — Hardware supply chain (§10.56-§10.61)

> **What this doc is.** The design rationale for the §10.56-§10.61 primitives that close the Story-18 (Argent Vector Defense Systems) chain-of-custody gaps for hardware bill-of-materials, firmware-attestation across supplier tiers, component cryptographic identity, RMA / sustainment chain re-entry, anti-counterfeit cross-anchor, and CMMC 2.0 regulator-pack overlay framework. Auditor's-lens convention applies.

## 1. The problem this solves

Story 18 drives the design. Argent Vector Defense Systems is a defense-electronics prime supplier — F-35 sustainment AI radar in production on a conformant chain-of-custody implementation for 7 months; ~1,847 distinct line items at the integrate-level; 47 supplier-facility pins; sub-tier suppliers in Taiwan, South Korea, Malaysia. The AI-side chain is mature. The hardware-supply-chain side is not in chain at all.

Five questions Argent Vector must answer from its chain alone:

1. **Where did this chip come from?** §10.56 binds the hardware bill-of-materials (HBOM) chain so per-component lifecycle (incoming test → FRU integration → depot return → disposition) is integrity-bound from origin through field life.
2. **Who built the firmware loaded on this device?** §10.57 binds the firmware-attestation chain across supplier tiers — internal builds direct, sub-tier-supplier builds via §10.21 cross-anchor.
3. **Is this physical component the one we admitted?** §10.58 normates the component cryptographic identity primitive enumerating identity-kinds (PUF, SEAL chiplet attestation, factory-provisioned key, serial+lot hash) with binding-walk vs challenge-walk verifier modes.
4. **Has this part been returned, repaired, cannibalized, or scrapped?** §10.59 normates RMA / sustainment chain re-entry discipline including the cannibalization parent-children pattern and the duplicate-binding-anomaly framework.
5. **Has a third-party laboratory attested to this lot's authenticity?** §10.60 cross-anchors anti-counterfeit attestation (AS6171, DARPA SHIELD) using the §10.21.1 sample-based-attestation pattern.

Plus the regulator-pack composition: §10.61 binds the family into CMMC 2.0 / NIST 800-171 / NIST 800-161 control mappings.

Without §10.56-§10.61, the supply-chain side of Argent Vector's evidentiary posture is paper-equivalent (PDF certificates, handwritten travelers, SAP records). With them, the chain is the evidentiary backbone DCMA's December review can verify.

## 2. Why §10.58 ships first as a shared primitive

§10.58 (component cryptographic identity) is consumed by §10.56 (HBOM `cryptographic_identity` field), §10.59 (RMA identity re-verification), and §10.65 (chassis-level TPM identity in the Story 19 hyperscale fleet attestation). §10.60 *composes with* §10.58 via the duplicate-binding-anomaly trigger but does not consume the primitive structurally — the §10.21.1 sample-based-attestation cross-anchor binds at the lot, not at the per-component identity.

GAP-9 in the wishlist manifest names §10.58 as a build-first shared primitive. The pre-mortem rejected lifting it later — the build-order is forced by §10.56 and §10.59 needing the identity-kind enumeration and verifier dispatch at admission time.

The four identity-kinds (PUF, SEAL chiplet, factory-provisioned key, serial+lot hash) are the closed canonical four for PRD-4. Each is grounded in deployed hardware:

- **PUF** is the gold standard for cryptographic identity — physically unclonable, challenge-response verifiable, in-die. Argent Vector's next-generation digital ASICs carry PUFs; legacy GaN PA parts do not.
- **SEAL chiplet attestation** is DARPA SHIELD-aligned — the chiplet's attestation document is signed by the SHIELD-program authority and bound to the chain at incoming test.
- **Factory-provisioned key** is the broadest identity-kind (Apple Secure Enclave, smartcard CSCAs, TPM endorsement keys). The manufacturer's CA chain validates the key.
- **Serial+lot hash** is the fallback for components without on-die identity — the identity is `SHA-256(utf8(serial_number) || utf8(lot_id))`. By construction not challenge-able.

Verifier-mode dispatch (binding-walk vs challenge-walk) handles the practical reality: most audits operate remote-walk (binding-walk only). Components in-hand at depot or incoming test allow challenge-walk. The two modes have different exit codes (12 = `CHALLENGE_WALK_PUF_VERIFIED`).

## 3. Why §10.57 supports two compositions for sub-tier suppliers

A sub-tier firmware supplier may or may not run a chain conformant to this specification. §10.57 supports both:

1. **Supplier runs a conformant chain.** The institution's `audit.firmware.activate` event references the supplier's `audit.firmware.build` chain entry by ID. Cross-chain anchor; bidirectional verifiability.
2. **Supplier runs signed-engineering-attestation regime.** The institution's `audit.firmware.activate` event references the supplier's signed attestation document by hash. §10.21 cross-anchor; build-time integrity is the supplier's contractual commitment.

The two compositions reflect commercial reality. Argent Vector's fourteen-of-seventeen FRU firmware artifacts are built internally; three are sub-tier-supplied. Of those three, the supplier's chain-conformance varies. The spec accommodates both without forcing supplier-side chain adoption — that's a commercial-relationship change Argent Vector commits to over twenty-four months, not a spec prerequisite.

## 4. Why §10.59 includes the duplicate-binding-anomaly framework

Sonya's institutional memory from her Howard-Pace 2017 federal-vertical experience is the operational substrate for §10.59. Twice in 2017, Howard-Pace caught a supplier reworking rejected parts and re-shipping them under different SKUs. The PUF response on the second receipt matched a previously-rejected part; Howard-Pace rejected the lot, opened a supplier corrective-action, and the supplier paid for the lot.

§10.59's duplicate-binding-anomaly framework normates that detection mechanism. The verifier flags:

1. **Identity-re-verification failure** — `repair_complete` or `depot_return` event whose identity does not match `original_incoming_test`. Cause: component was swapped or restickered.
2. **Duplicate binding** — same `cryptographic_identity` bound to multiple incoming-test entries under different `serial_number` values. Cause: rejected component was re-stickered and re-submitted.
3. **Orphan re-entry** — `audit.rma.*` event without a corresponding incoming-test entry. Cause: out-of-process insertion.

Detection is *anomaly-flagged*, not chain-integrity-failed. The institution's CC8.1 names the anti-counterfeit referral path on duplicate binding (§10.60 AS6171 referral); the chain produces the signal, the institution's program produces the response.

## 5. Why §10.60 extends §10.21.1 instead of creating a new cross-anchor primitive

The §10.21.1 sample-based-attestation pattern (introduced as part of the §10.21 amendments in this same wave) is the right primitive — it handles destructive-test cases (AS6171), non-destructive-isolated cases (SHIELD chiplet attestation), and lot-vs-installed-part discrimination uniformly. §10.60 binds the SAE AS6171 / DARPA SHIELD attestation documents using §10.21.1 schema; the §10.60-specific naming is conventions on top of the primitive.

The pre-mortem rejected an anti-counterfeit-specific primitive: the §10.21.1 pattern generalizes (pharmaceutical lot acceptance, environmental-compliance sampling, biomedical-device lot release all share the structural pattern). Building §10.21.1 once and citing it from §10.60 is the right shape.

## 6. Why §10.61 is a versioned overlay framework

CMMC 2.0 has a four-year revision cadence. CMMC 3.0 (or whatever the next release is named) will introduce changed control items and possibly a different control numbering. §10.61 normates the overlay *framework* — the contract for how CMMC versions map onto chain entries — not a fixed CMMC 2.0 binding.

§10.61.1 ships in PRD-4 as the CMMC 2.0 instance. Future CMMC releases land as §10.61.2, §10.61.3, etc. Deprecated CMMC versions remain verifiable with a `sunset_attestation` marker emitted by the verifier when an institution operates under the deprecated mapping; the marker documents the institution's migration window without breaking verifiability of historical chain entries.

The same versioning pattern applies to §10.68 (AISI overlay) — both regulator-pack frameworks are versioned per regulator-program release.

## 7. Cross-references

- Spec sections: §10.21 / §10.21.1 (cross-anchor patterns); §10.56-§10.61 (this design doc's surface).
- Test vectors per `spec/test-vectors/PRD-4-INDEX.md`: §10.58 PUF binding-walk is vector 050, PUF challenge-walk is vector 051; §10.58 SEAL chiplet attestation is vector 058; §10.58 factory-provisioned key is vector 059; §10.60 anti-counterfeit cross-anchor is vector 062; §10.62 vectors are 063 (red-side reference projection) and 064 (black-side hash-equivalence walk).
- Auditor stories: Story 18 (Argent Vector Defense Systems) — the institutional-reference engagement.
- Adjacent design docs: 17-red-black-separation.md (the §10.62 sibling for cleared-environment work).
- Regulator pack: `docs/regulator-pack/cmmc-overlay.md` (§10.61.1); `docs/regulator-pack/defense-cleared-environment-overlay.md` (the cleared-facility companion).
- External: SAE AS6171; DARPA SHIELD program; CMMC 2.0 final rule (32 CFR Part 170); NIST SP 800-171 Rev 3; NIST SP 800-161r1; NIST SP 800-193 (firmware integrity).
