---
name: Errata (published-draft correction)
about: A factual or normative error in a published draft (PRD-N) that needs correction in PRD-(N+1)
title: "[errata PRD-?] "
labels: ["errata"]
assignees: []
---

> **Errata are factual or normative errors in a published draft.** Errata are tracked against the PRD they appeared in and corrected in the next PRD. Use this template for factual mistakes (incorrect FIPS reference, miscalculated test-vector hash, contradiction between two sections, etc.). Editorial-only fixes use the `editorial` template.

## PRD affected

<!-- e.g., PRD-1 (0.1.0-draft.1) -->

## Where

<!-- File path and section number. -->

## What is wrong

<!-- Describe the error precisely. If the error is a factual claim, cite the source that contradicts it. -->

## Severity

- [ ] **Critical** &mdash; the error invalidates a conformance claim, a security claim, or a test vector
- [ ] **Major** &mdash; the error misleads a reviewer or implementer about a normative requirement
- [ ] **Minor** &mdash; the error is inaccurate but does not cause an implementer or reviewer to draw the wrong conclusion

## Suggested correction

<!-- Either the corrected text, or a description of the correction needed. -->

## Test-vector impact

<!--
Does the correction require regenerating one or more test vectors? If yes, name the affected vectors.
-->
