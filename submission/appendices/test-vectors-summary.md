# Appendix C — Conformance test-vector corpus summary

> **Placeholder.** The formal-submission summary is generated from [`../../spec/test-vectors/`](../../spec/test-vectors/) and presents the corpus in a reviewer-readable form.

## Positive vectors (PRD-1)

| Vector | Property exercised | Spec sections |
|---|---|---|
| 001-single-event-empty-prev | Genesis chain entry; `prev_hash` = 32 zero bytes | §4.1 |
| 002-multi-event-same-run | Sequential MAC chain within one run | §4.1 |
| 003-multi-run-same-day | Cross-run chain isolation; daily Merkle aggregation across runs | §4.1, §4.2 |
| 008-jcs-edge-cases | RFC 8785 canonical-JSON edge cases | §4.1, §5 |
| 010-tenant-ikm-rotation-mid-day | `key_version` rotation crossing the seal boundary | §4.1, §10.10 |
| 015-dual-algorithm-cosigned-seal | Multi-algorithm signature transition (PQC roadmap) | §4.3 |
| 016-non-power-of-2-merkle | RFC 6962 Merkle construction with non-power-of-2 leaf counts | §4.2 |
| 017-merkle-inclusion-partial-disclosure | Partial-disclosure inclusion proofs (privacy-preserving examiner queries) | §4.2 |
| 018-sign-payload-v1.0b | Sign-payload format binding | §4.3 |
| 019-sign-payload-v1.0b-empty-day | Empty-day sealing under sign-payload format | §4.3 |

## Negative vectors

The negative corpus (N001 through N022 in [`../../spec/test-vectors/negative/`](../../spec/test-vectors/negative/)) exercises an independent threat scenario per vector:

- Cross-chain lift attempts
- MAC tampering
- Fingerprint mismatch
- Seal forgery
- JCS canonicalization divergence
- Key-rotation edge cases
- Empty-day boundary attacks
- Multi-region replay

## Conformance bar

A conforming implementation produces output that passes every positive vector and rejects every negative vector. Two conforming implementations of the same wire-format identifier (`"v1"`) produce byte-identical output for the same logical event. The corpus is the discriminator between conforming and non-conforming implementations.

## Reproducibility

Each vector ships JSON inputs and expected JSON outputs. The expected outputs are byte-stable: same inputs &rarr; same outputs across implementations, languages, and runtimes. The conformance check is byte equality, not structural equivalence.
