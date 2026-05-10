## Summary

<!-- One paragraph: what changed and why. Cite the regulatory or operational driver if applicable. -->

## Type of change

- [ ] Editorial / typo / clarification (no normative change)
- [ ] Documentation only (no spec change)
- [ ] **Specification change — normative** (requires unanimous spec-editor approval and the public-comment cadence in GOVERNANCE.md)
- [ ] Test-vector addition or correction
- [ ] Submission-package update
- [ ] Build / CI / governance

## Version impact

- [ ] Document version unchanged
- [ ] Document version increment expected (`0.1.0-draft.N` → `0.1.0-draft.N+1`)
- [ ] Wire-format identifier change (this is a major event — wire-format changes from `"v1"` to `"v2"` rebase every test vector and require a coordinated PRD)

## The reviewer's-lens summary

<!--
One paragraph explaining how a reviewer can verify this change without re-deriving it themselves.
Where applicable, cite:
  - The handbook section, RFI question, or regulatory framework satisfied
  - The cryptographic primitive used (and its FIPS/NIST status)
  - The deterministic output guarantees
  - The test vectors that demonstrate the property
  - The auditor-story or examiner-quickstart scene that exercises the property end-to-end
-->

## Test vectors

- [ ] No new test vectors required (no behavior change)
- [ ] Test vectors added in `spec/test-vectors/` and the JSON inputs / expected outputs are byte-stable
- [ ] Test vectors updated to reflect a wire-format-identifier change

## Spec / docs / submission updates

- [ ] No spec change
- [ ] `spec/chain-of-custody-DRAFT-0.1.0.md` updated with normative changes
- [ ] `docs/design/` updated to reflect the change's rationale
- [ ] `submission/` updated if the change affects the public-comment package
- [ ] `CHANGELOG.md` entry added under the current PRD

## Checklist

- [ ] Commits signed-off-by per `CONTRIBUTING.md` (`git commit -s`) and signed (`git commit -S`) when GPG/SSH keys are available
- [ ] No telemetry / phone-home behavior introduced
- [ ] No new dependencies on closed-source or non-permissive content
- [ ] Markdown lint passes (if a lint workflow exists)
