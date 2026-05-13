---
name: Spec proposal (normative change)
about: Propose a normative change to the specification
title: "[spec-proposal] "
labels: ["spec-proposal"]
assignees: []
---

> **A spec proposal is a normative change to `spec/chain-of-custody-DRAFT-0.2.0.md`.** Spec changes follow the unanimous spec-editor approval and 14-day public-comment cadence in [GOVERNANCE.md](../GOVERNANCE.md). Editorial fixes use the `editorial` template; corrections to a published draft use the `errata` template.

## Summary

<!-- One paragraph: what should change and why. -->

## Regulatory or threat-model driver

<!--
Cite the FFIEC handbook section, the RFI question, the threat-model adversary class,
the auditor-story scene, or the examiner-quickstart scenario that motivates the change.
-->

## Proposed normative text

<!--
Either:
  (a) the proposed new spec section, written in normative style with RFC 2119 conformance keywords
  (b) the proposed change to existing spec text, with the before/after diff
-->

## Test-vector impact

<!--
Will this change require new positive vectors, new negative vectors, or modifications to
existing vectors? Sketch the vector shape if you can.
-->

## Wire-format identifier impact

<!--
Is this an additive change (wire-format identifier stays "v1") or an incompatible change
(would require "v2")? Additive changes are strongly preferred during the draft cycle.
-->

## Backward compatibility

<!--
What happens to chains produced under the current draft when this change lands?
Verifier behavior on prior-draft chains? Migration path?
-->

## Alternatives considered

<!-- What did you consider and reject, and why? -->

## Comment-period readiness

- [ ] Proposal cites at least one regulatory or threat-model driver
- [ ] Proposed normative text uses RFC 2119 conformance keywords correctly
- [ ] Test-vector impact described
- [ ] Wire-format-identifier impact named
- [ ] Backward-compatibility posture described
- [ ] At least one alternative considered
