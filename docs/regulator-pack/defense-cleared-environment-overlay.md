---
title: Defense / Cleared-Environment Articulation Overlay
status: informative
aligned-with:
  - DoD 5220.22-M (NISPOM, National Industrial Security Program Operating Manual)
  - 32 CFR Part 117 (NISPOM Rule)
  - DD-254 (Contract Security Classification Specification)
  - NSTISSAM TEMPEST/2-95 (TEMPEST Countermeasures)
  - CNSSI 7000 (TEMPEST Countermeasures for Facilities)
  - NSA Cross-Domain Solution evaluation framework
  - CSfC (Commercial Solutions for Classified) program
date: 2026-05-09
version: 1.0.0
---

# Defense / Cleared-Environment Articulation Overlay

> **What this doc is.** An articulation overlay mapping the FFIEC chain-of-custody specification onto the cleared-environment discipline that defense-electronics primes, defense contractors, and DoD supply-chain participants operate under. Written so a DSS / DCSA Industrial Security Representative, a Joint Cross-Domain Solution Office (JCDSO) reviewer, a Facility Security Officer, and a contractor's chain-of-custody program lead can read this document alongside the spec and confirm what the chain delivers across red/black boundaries, what it does not, and which artifact discharges which obligation under DD-254 / NISPOM / TEMPEST.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's facility security program, accreditation documentation, or System Security Plans. The §1.2 epistemic scope discipline applies: the chain proves what was said and that the record was not tampered with; it does not certify TEMPEST conformance, NSA Type-1 module evaluation outcomes, or facility accreditation status.

---

## 1. Scope and reading order

This overlay covers cleared facilities operating AI-bearing systems with red/black separation. The canonical PRD-4 institutional reference is Argent Vector Defense Systems' TALON-X RDT&E program (Story 18). Reading order: §10.62 (red/black separation chain integrity); §10.62.1 (color-classification tagging); §10.62.2 (releasability-projection contract); §10.56-§10.61 (hardware supply chain side); §10.21 / §10.21.1 (cross-anchor patterns); §7 unknown-wire-format-kind fallthrough rule (governs PRD-3 verifier handling of §10.62 records).

## 2. Red/black separation mapping

| Cleared-environment requirement | Spec section | Operational binding |
|---|---|---|
| TEMPEST enclosure boundary documentation | §10.62.1 `audit.color_classification.side` | Every chain entry tagged `red` \| `black` \| `cross-domain` |
| Type-1 cross-domain module evaluation status | §10.62 cross-domain transition record | NSA-issued evaluation result hash anchored via §10.21 |
| Releasability filter version control | §10.62.2 releasability_filter_version | Institution-named versioning per CC8.1; deterministic projection contract enforced |
| Red-side chain visibility from black-side verifier | §10.62 black-side hash-equivalence walk | Exit code 11 = `BLACK_SIDE_PASS_RED_NOT_WALKED` |
| Classification-level taxonomy | §10.62.1 `audit.color_classification.classification_level` | Institution-named per CC8.1 (e.g., `secret`, `top-secret`, `unclassified-cui`, `unclassified`) |

## 3. Hardware supply-chain mapping (cleared-component context)

Cleared facilities also handle hardware supply chain under classified-bom discipline. §10.56-§10.60 apply with the added constraint that `audit.hbom.*` events for classified components carry red-side color-classification tagging and stay inside the TEMPEST enclosure. Cross-domain transitions of HBOM events (e.g., when a hardware-attestation summary needs to traverse the boundary for downstream black-side reporting) follow §10.62.

## 4. JCDSO / NSA evaluator orientation

A Joint Cross-Domain Solution Office reviewer or NSA cross-domain-solution evaluator running an audit walks:

1. **Red-side full walk** (cleared-area only) — verifies the institution's filter against the bound releasable-hash; confirms determinism; confirms no red-side content leakage in the projection.
2. **Black-side hash-equivalence walk** (typically off-site) — verifies black-side chain entries against the registry-published cross-domain transition records' releasable-hashes; produces a PASS verdict bounded by exit code 11.
3. **§10.62.2 contract-conformance check** — the per-program filter ships with at least one byte-identical test vector; the reviewer reproduces the projection from the fixture red-side payload and confirms equivalence.

## 5. Cross-references

- Spec sections: §10.21 (cross-anchor); §10.56-§10.62 (hardware + red/black wave); §7 unknown-wire-format-kind fallthrough rule.
- Test vectors: `063-red-black-projection-talon-x` (reference); paired vector for black-side walk.
- Auditor stories: Story 18 (Argent Vector / TALON-X).
- Adjacent overlays: `cmmc-overlay.md` (defense-contracting compliance regime; CMMC 2.0 controls applicable to cleared environments).
- Design doc: `docs/design/17-red-black-separation.md`.
- External: 32 CFR Part 117 (NISPOM Rule); DD-254; NSTISSAM TEMPEST/2-95; CNSSI 7000; NSA Cross-Domain Solution evaluation framework.
