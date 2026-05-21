# Case 036 — Verdict object with `additional_verifications` (§10.12 amendment)

## What this case verifies

Spec §10.12 normates the full schema of the verdict object the verifier
emits on its `Verdict-Object: <jcs-bytes>` trailing line. Six fields
are required on every run; one field (`operational_events_log_root`)
is optional and PRESENTs only under v1.0c seal walks. Spec §7 lines
1574-1586 cross-reference the schema and pin four byte-form examples
this test vector reproduces verbatim.

This case pins the JCS-canonical bytes for **seven** verdict sub-cases.
The first three (036a/b/c) pin the **2-field structural subset** shape
— `additional_verifications` and `exit_code` only — so an implementer
can isolate the array-shape behavior without the full-schema noise.
The next four (036d/e/f/g) pin the **full §7-normative shape** with
all six required fields plus, for 036g, the v1.0c-optional
`operational_events_log_root` field.

| Sub-case | Shape | Use case |
|---|---|---|
| 036a | 2-field subset, `additional_verifications=[]` | Array-shape only — empty |
| 036b | 2-field subset, one marker | Array-shape only — one entry |
| 036c | 2-field subset, two markers (placeholder second) | Array-shape only — composition |
| 036d | FULL 6-field, v1.0b, no bonus verifications | Steady-state PASS under v1.0b |
| 036e | FULL 6-field, v1.0b, `backfill_seal_verified` | M&A close — §10.42 backfill seal verified |
| 036f | FULL 6-field, v1.0b, two §10.69 class-disclosure markers | Rule 23 commonality production |
| 036g | FULL 7-field, v1.0c, `sibling_log_root_verified` + `operational_events_log_root` | v1.0c seal with §10.79 sibling-log binding |

The conformance contract is that all seven sub-cases produce
byte-identical output across implementations.

The structural-subset sub-cases (036a/b/c) remain in the fixture
because the array-shape rules (empty-array-not-absent on PASS-no-bonus,
composition behavior, placeholder-second-string demonstration) are
worth pinning in isolation. They are NOT the conformance bar for the
verifier's Verdict-Object emission — a verifier emitting only the
2-field subset is non-conformant per spec §10.12's six-required-fields
rule. The 2-field shapes are a building block for clean-room
implementers verifying their JCS canonicalization handles the array
correctly before they wire up the four scalar fields.

## What this case does NOT verify

The verdict object's *production behavior* — when does the verifier
emit `"backfill_seal_verified"`? — is verifier-implementation-specific
and tested by the verifier's test suite (case 035 covers the structural
backfill verification, the verifier's tests cover the dispatch logic).
Case 036 pins the structural byte form; the verifier's logic is
downstream.

## Inputs

The closed enumeration of `additional_verifications` strings under
§10.12 (consolidated table — 20 markers under v1.0c):

| String | Spec section |
|---|---|
| `backfill_seal_verified` | §10.42 |
| `sample_based_attestation_via_lot_verified` | §10.21.1 |
| `parallel_evaluator_anchor_verified` | §10.21.2 |
| `cross_anchor_unbound` | §10.21.3 |
| `unknown_kind_present` | §7 |
| `customer_disclosure_subtree_verified` | §10.69 |
| `customer_disclosure_key_derivation_verified` | §10.69 |
| `class_disclosure_subtree_verified` | §10.69 |
| `cohort_coverage_attestation_verified` | §10.69 |
| `foia_release_subtree_verified` | §10.72 |
| `foia_release_key_derivation_verified` | §10.72 |
| `privileged_investigation_full_content_returned` | §10.70 |
| `privileged_investigation_redacted_with_existence_attestation` | §10.70 |
| `cross_institution_chain_verified` | §10.71 |
| `device_revoked_seen_at_seq_N` | §10.32 |
| `cross_vendor_handover_verified` | §10.21 |
| `partial_coverage_pattern_2_verified` | §10.19 |
| `customer_disclosure_cross_tenant_inheritance_verified` | §10.69 |
| `attestation_chain_validated` | §10.77 |
| `sibling_log_root_verified` | §10.79 |

The verdict object schema (full 7-field shape under v1.0c; the 6-field
shape under v1.0a/v1.0b omits `operational_events_log_root`):

```json
{
  "additional_verifications": ["<string from the closed enumeration>"...],
  "exit_code": <integer in {0, 1, 2, 3, 4, 5, 6}>,
  "operational_events_log_root": "<sha256-lowercase-hex-64-chars>",
  "posture": "ffiec" | "vendor:<name>",
  "trust_anchor_manifest_sha256": "<sha256-lowercase-hex-64-chars or empty string>",
  "verifier_spec_version_supported": "v1.0a" | "v1.0b" | "v1.0c",
  "verifier_version": "<reproducible-build release identifier>"
}
```

JCS canonicalization sorts keys lexicographically. The actual byte
order is therefore: `additional_verifications`, `exit_code`,
`operational_events_log_root` (when present), `posture`,
`trust_anchor_manifest_sha256`, `verifier_spec_version_supported`,
`verifier_version`. Sub-case 036g demonstrates that the v1.0c-optional
`operational_events_log_root` field sorts between `exit_code` and
`posture` when present.

## Expected canonical bytes

| Sub-case | Length | Canonical SHA-256 |
|---|---:|---|
| 036a | 45 | `c79490211ce76c721560fe28d1a781e70b391353ebe3c4cf3d6aa743ab4895ba` |
| 036b | 69 | `18f280814c89104f1c728a8dbd99e87ae8d5202b6cd4a0c890e1eabccd6f6972` |
| 036c | 106 | `8062495801460b1ed1969788ebe7bcf40dce63cc9d734a3ceaea43e2cd6316a4` |
| 036d | 250 | `1555e3ece8c1901561fc359dd8848b34932428f818f8e56256d86004b6d2b098` |
| 036e | 274 | `b34d9803a9caa153a314796e3dd53c218cda1e38ec23dd0263be644786283138` |
| 036f | 324 | `829ae3f8b4e4e73f15ee40fe69b81718ba0a6e93b521f4372816f41fef077fdf` |
| 036g | 374 | `bdcc616eb4aaddf1e5506121e6dc0898d958e4bfa955b987bbdb7d3b5b2ad6a7` |

`expected_canonical.txt` carries the seven sub-case canonical byte
forms separated by a single LF; readers split on LF to recover each
sub-case.

`expected_canonical_sha256.txt` carries the seven sub-case labels and
hex digests, one per line.

## Placeholder values across 036d/e/f/g

The four sub-cases that use the full schema share identical placeholder
values for the scalar fields so the only byte differences between them
come from `additional_verifications` (and, for 036g,
`operational_events_log_root` and the `v1.0c` version strings). The
placeholders match the spec §7 byte-form examples at lines 1591, 1597,
1603, 1609 verbatim.

| Field | Value |
|---|---|
| `posture` | `"ffiec"` |
| `trust_anchor_manifest_sha256` | `"7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"` |
| `verifier_spec_version_supported` (036d/e/f) | `"v1.0b"` |
| `verifier_spec_version_supported` (036g) | `"v1.0c"` |
| `verifier_version` (036d/e/f) | `"v1.0b-verifier-2026-05-15"` |
| `verifier_version` (036g) | `"v1.0c-verifier-2026-05-15"` |
| `operational_events_log_root` (036g) | `"3e9f7c2a8b1d5e6c4a2f9e1d8c7b5a3f1e8d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"` |

A clean-room implementer constructing a verdict with the same field
values produces output byte-identical to the corresponding `036*`
sub-case.

## Conformance behavior

A conforming verifier:

1. Constructs the verdict object as a JSON object with **all six
   required fields** on every run (the v1.0c-optional
   `operational_events_log_root` PRESENTs only on v1.0c seal walks).
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical
   to the corresponding `expected_canonical.txt` sub-case for the
   matching shape.
3. Emits `additional_verifications = []` (empty array, NOT absent) on
   every non-zero exit code and on PASS with no bonus verifications.
   The empty array is structurally explicit so a consumer can detect
   "no bonus verifications" deterministically without conflating with
   "field missing." Sub-case 036d pins this shape.
4. OMITS `operational_events_log_root` from the JCS output under v1.0a
   and v1.0b seals — the field is not emitted as `null` or as an empty
   string. Sub-case 036d pins the v1.0b omission shape; sub-case 036g
   pins the v1.0c PRESENT shape.
5. Emits `trust_anchor_manifest_sha256` as an empty string (`""`) under
   witness mode or customer-disclosure mode where the verifier had no
   IKM-registry access. Otherwise the field carries the lowercase-hex
   SHA-256 of the canonicalized IKM-registry manifest the verifier
   validated at startup per §10.76.
6. Emits a known string from the closed §10.12 enumeration when the
   corresponding bonus verification PASSed. Implementations MAY emit
   vendor-specific strings outside the enumeration into a parallel
   `additional_diagnostics` field (which is opaque and NOT closed-
   enumerated); they MUST NOT contaminate `additional_verifications`
   with vendor-specific strings.
7. Preserves the integer exit code's 0-vs-non-zero contract — a PASS
   with bonus verifications still exits 0; the array does not shift
   the exit code.

## Why this case exists

The §10.12 amendment chose the structured-array approach over
alternative proposals (a new exit code per bonus verification, a
packed-bitfield exit code, or an out-of-band metadata file). Three
reasons captured in design `07-verifier-design.md` §11.3:

1. **0-vs-non-zero contract preservation.** Shell scripts read exit
   0 as PASS and non-zero as FAIL. Adding exit code 7 for
   "BACKFILL_SEAL_VERIFIED" presents as FAIL to anyone who hasn't
   read the spec.
2. **Combinatorial blow-up avoidance.** The §10.12 cryptographic-
   agility roadmap may introduce hybrid-PQ verification (and other
   bonus verifications) under future enumeration entries; further
   bonus verifications would otherwise demand exit codes 8, 9, 10, ...
   The verdict-object design absorbs the entire wave through one
   schema field.
3. **Composition.** Multiple bonus verifications can apply to the
   same chain. The array shape composes naturally; a single exit code
   cannot.

Case 036's sub-case 036f demonstrates two-marker composition under
the full schema; 036c does the same under the structural subset. A
clean-room implementer constructing the verdict for a Story-17-shaped
engagement (where the chain exercises both §10.42 and §10.53) produces
the array byte-identically to the reference implementations.

## Negative cases this fixture supports

- See `negative/N026-additional-verifications-invalid-string/` for the
  negative case where the verdict carries an unknown string in the
  array — under `--strict` the verifier rejects; under default mode
  the unknown string passes through as opaque diagnostic.

## Cross-references

- Spec §10.12 verifier CLI exit-code contract + full verdict-object
  schema (the section this case proves out)
- Spec §7 lines 1574-1586 (the Verdict-Object trailing-line discipline
  and the four byte-form examples sub-cases 036d/e/f/g reproduce)
- Spec §10.42 backfill seal discipline (sub-case 036e marker source)
- Spec §10.69 customer/class disclosure (sub-case 036f markers source)
- Spec §10.79 sibling-log binding (sub-case 036g marker and field
  source)
- Design `07-verifier-design.md` §11 (the verdict-object design
  rationale)
- Design `12-successor-attestation-and-backfill.md` (the M&A-close
  composition with case 035)
- RFC 8785 (JCS canonicalization)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
