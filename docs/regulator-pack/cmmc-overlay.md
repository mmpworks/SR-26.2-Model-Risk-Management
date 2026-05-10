---
title: CMMC 2.0 / NIST 800-171 / NIST 800-161 Articulation Overlay
status: informative
aligned-with:
  - CMMC 2.0 Final Rule (32 CFR Part 170)
  - NIST SP 800-171 Rev 3 (Protecting Controlled Unclassified Information)
  - NIST SP 800-161 Rev 1 (Cybersecurity Supply Chain Risk Management)
  - DFARS 252.204-7012 (Safeguarding Covered Defense Information and Cyber Incident Reporting)
  - 32 CFR Part 117 (NISPOM Rule)
date: 2026-05-09
version: 1.0.0
revision-cadence: per-CMMC-release (current §10.61.1 covers CMMC 2.0; future §10.61.2 covers next CMMC release)
---

# CMMC 2.0 Articulation Overlay (§10.61.1)

> **What this doc is.** The PRD-4 instance of the §10.61 versioned regulator-pack overlay framework, mapping CMMC 2.0 Level 3 controls — and the NIST SP 800-171 / 800-161 / DFARS underlying frameworks — onto chain entries via control-by-control PASS/FAIL verifier dispatch. Written so a DCMA reviewer, a CMMC Third-Party Assessment Organization (C3PAO) assessor, a contractor's compliance lead, and a sub-tier supplier preparing a self-assessment can read this document alongside the spec and confirm what the chain delivers under CMMC discipline.

> **What this doc is NOT.** Not a normative extension to the spec. Not a substitute for the institution's System Security Plan, Plan of Action and Milestones, or the C3PAO assessment itself. The §1.2 epistemic scope applies: the chain proves what was said and that the record was not tampered with; it does not certify CMMC compliance.

> **Versioning discipline.** This overlay tracks CMMC 2.0. When CMMC 3.0 (or whatever the next release is named) is published, a new overlay (`cmmc-3-overlay.md` or `cmmc-overlay-v2.md`) ships under §10.61.2; this overlay is preserved as the canonical CMMC 2.0 mapping with a `sunset_attestation` marker discipline per §10.61. Deprecated CMMC 2.0 chain entries remain verifiable indefinitely.

---

## 1. Scope and reading order

This overlay covers institutions in the Defense Industrial Base operating under CMMC 2.0 Level 3 (the highest CMMC level requiring an external C3PAO assessment for handling Controlled Unclassified Information). The canonical PRD-4 institutional reference is Argent Vector Defense Systems (Story 18). Reading order: §10.56-§10.62 (hardware supply chain + red/black wave); §10.61 (this overlay's normative anchor); CMMC 2.0 control-family scoping below.

## 2. Control-family mapping

| CMMC 2.0 Level 3 family | Spec sections | Operational binding |
|---|---|---|
| AC.L3-3.1.4 (Separation of Duties) | §10.17 HSM ceremony attestation; §10.70 role-based verifier dispatch | Dual-control HSM ceremonies; SAR-cleared role discipline |
| MA.L3-3.7.5 (Maintenance) | §10.59 RMA / sustainment chain re-entry | Returned components dispositioned per §10.59 cannibalization parent-children pattern |
| SC.L3-3.13.2 (Security Engineering Principles) | §10.62 red/black separation; §10.21 cross-anchor | Cross-domain modules attested via §10.21 with NSA-issued evaluation result hash |
| SI.L3-3.14.6 (Monitor Communications for Attacks) | §10.65 hyperscale fleet attestation; §10.2 operational events | `chassis_quarantined`, `connector.outage`, `clock.drift_detected` operational events |
| SR-family (Supply Chain Risk Management) | §10.56 HBOM; §10.57 firmware-attestation; §10.58 component cryptographic identity; §10.59 RMA; §10.60 anti-counterfeit | Hardware lifecycle integrity-bound from incoming test through field deployment and disposition |

## 3. NIST SP 800-171 mapping

| 800-171 family | Section count mapped | Spec anchor |
|---|---|---|
| §3.4 Configuration Management | 9 | §10.18 CC8.1 cross-referencing; §10.57 firmware-attestation |
| §3.7 Maintenance | 6 | §10.59 RMA chain re-entry |
| §3.10 Physical Protection | 6 | §10.17 HSM ceremony; §10.62.1 color-classification tagging |
| §3.13 System & Communications Protection | 16 | §10.62 red/black; §10.5 HSM custody; §5.1 transport encryption |
| §3.14 System & Information Integrity | 7 | §10.65 fleet attestation; §10.2 operational events |

## 4. NIST SP 800-161 SR mapping

SR-1 through SR-12 (supply-chain-risk-management practices) map onto §10.56-§10.60. The verifier produces SR-by-SR PASS/FAIL by walking the §10.56-§10.60 chain entries against the institution's CC8.1 supply-chain risk register.

## 5. DFARS 252.204-7012 incident-response binding

DFARS clause 252.204-7012 requires incident reporting within 72 hours of discovery. §10.2 operational events (`incident.detected`, `incident.classified`, `incident.reported`) bind the timeline; the chain produces the integrity-bound timeline for DCMA review. Composes with `docs/incident-response-playbook.md`.

## 6. DCMA / C3PAO assessor orientation

A DCMA reviewer or C3PAO assessor running an annual / triennial assessment walks:

1. The institution's chain-coverage map (§10.19) against the CMMC scope statement.
2. Per-control verifier dispatch against the chain entries (the §10.61 verifier runs the control-by-control PASS/FAIL).
3. The institution's POA&M against any control-completeness anomalies the verifier flagged.
4. The §10.56-§10.60 supply-chain wave as the SR-family evidence pack.

## 7. Cross-references

- Spec sections: §10.18 CC8.1 cross-referencing; §10.19 chain-coverage map; §10.56-§10.62 (hardware + red/black wave); §10.61 (this overlay's normative anchor).
- Adjacent overlays: `defense-cleared-environment-overlay.md` (cleared-facility companion); `fedramp-fisma-overlay.md` (broader US federal compliance regime; includes 800-171 scoping for non-DIB contexts).
- Design doc: `docs/design/16-hardware-supply-chain.md`.
- External: CMMC 2.0 Final Rule (32 CFR Part 170); NIST SP 800-171 Rev 3; NIST SP 800-161r1; DFARS 252.204-7012.
