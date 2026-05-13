# Specification

> **The spec is the standard.** Conforming implementations conform to the spec. The reference implementation lives in a separate repository and is one example of a conforming implementation; it is not the standard itself.

## Current state

| Document | Version | Status |
|---|---|---|
| [`chain-of-custody-DRAFT-0.2.0.md`](chain-of-custody-DRAFT-0.2.0.md) | `0.2.0` | **Public Review Draft 2 (PRD-2)** |

This is a public-comment draft, not a finalized standard. Comments and review are invited per [`../GOVERNANCE.md`](../GOVERNANCE.md). The trajectory of changes between PRD-N and PRD-(N+1) is tracked in [`../CHANGELOG.md`](../CHANGELOG.md) and in §12 of the spec.

## Two independent versions

Implementers and reviewers distinguish two versions:

- **Document version** &mdash; `0.2.0`. The state of the specification text. Increments per draft revision and finalizes to `1.0.0` when the public-comment process concludes.
- **Wire-format identifier** &mdash; `"v1"`. The byte-level construction. Stamped on every chain entry as `format_version`, embedded in the HKDF salt and info constants, and pinned by every test vector. Stable across the draft cycle so implementations build against PRD-N and remain valid under PRD-(N+1).

See §0 of the spec for the full version policy.

## Conformance

A conforming implementation:

1. Produces output that passes every test vector in [`test-vectors/`](test-vectors/) for its declared spec version.
2. Accepts as input any output produced by another conforming implementation of the same spec version.
3. Documents which spec version it implements in its release notes.

An institution running an SDK from one vendor and a ledger from another vendor and a verifier from a third should see byte-for-byte agreement on every chain artifact.

## Test vectors

[`test-vectors/`](test-vectors/) contains the canonical conformance corpus. Every primitive change ships test vectors that demonstrate the change. The corpus is the discriminator between conforming and non-conforming implementations.

## Future versioning convention

After finalization (`1.0.0`), specifications follow the form `chain-of-custody-vN.M.md`:

- `N` major &mdash; incompatible wire-format or primitive changes
- `M` minor &mdash; additive changes that an older verifier can ignore safely

Pre-finalization drafts use the semver pre-release convention (`0.1.0-draft.N`).
