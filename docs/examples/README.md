# Examples

Worked, runnable code demonstrating spec-conformant operations. Examples are **informative** — they make the spec concrete for implementers and public-comment readers but do not set conformance requirements. Conformance is established by the spec text and the test-vector corpus.

See [CONVENTIONS.md](CONVENTIONS.md) for attribution, scope, code-style, and contribution rules.

## Index

| Example | Section | What it demonstrates |
|---|---|---|
| [10-58-binding-walk-puf/](10-58-binding-walk-puf/) | §10.58 | Binding-walk verifier mode for the `puf-response` identity-kind: JCS-canonical JSON `canonical_binding_input` construction, SHA-256 binding-hash recompute, PASS marker emission per §10.12 additional-verifications discipline |
| [07-verifier-output-trailing-line/](07-verifier-output-trailing-line/) | §7 | Verifier output discipline: line-oriented `Status:` / `Step:` / `Reason:` / anomaly-lines form plus the normative `Verdict-Object: <jcs-bytes>` trailing line, with round-trip parse and vector-036 byte-equivalence assertion across all three sub-cases (empty / one marker / two markers) |

## Roadmap

Examples are added as the spec stabilizes. Candidate next entries (subject to vector availability per `spec/test-vectors/PRD-4-INDEX.md`):

- §10.21.2 parallel-evaluator cross-anchor walk (PASS marker + dynamic-cardinality dispatch)
- §10.21.3 registry-discovery cross-anchor in `bound` and `unbound` states
- §7 verifier output structured form (when verdict-object format normates)
- §10.42 backfill seal verification path
- §4.2 daily Merkle seal construction (RFC 6962 leaf ordering, empty-day case)

Public-comment readers and implementers who want a worked example for a specific section may open an issue requesting one.
