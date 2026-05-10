# Case 036 — Verdict object with `additional_verifications` (§10.12 amendment)

## What this case verifies

Spec §10.12 amendment + design `07-verifier-design.md` §11 normate the verdict object's `additional_verifications` array as the place bonus verifications report. The §10.42 backfill-seal verification reports `"backfill_seal_verified"`; the §10.12 enumeration may grow as future spec sections normate additional bonus verifications. Exit codes 0-6 remain the closed §10.12 + §10.29 enumeration; bonus verifications travel via the array, NOT via new exit codes.

This case pins the JCS-canonical bytes for three verdict sub-cases:

| Sub-case | Shape | Use case |
|---|---|---|
| 036a | `exit_code=0, additional_verifications=[]` | Steady-state PASS — no bonus verifications applied |
| 036b | `exit_code=0, additional_verifications=["backfill_seal_verified"]` | M&A close — §10.42 backfill seal verified |
| 036c | `exit_code=0, additional_verifications=["backfill_seal_verified", "hybrid_pqc_dual_signature_verified"]` | Forward-compat composition test — pins the two-entry array byte form using a placeholder second string |

The conformance contract is that all three sub-cases produce byte-identical output across implementations. The forward-compat sub-case 036c demonstrates the array's composition behavior; the second string is a placeholder used here only to pin the two-entry byte form. The §10.12 closed enumeration today contains only `backfill_seal_verified` per §10.42, and additional enumeration entries land here only when their corresponding spec section normates them.

## What this case does NOT verify

The verdict object's *production behavior* — when does the verifier emit `"backfill_seal_verified"`? — is verifier-implementation-specific and tested by the verifier's test suite (case 035 covers the structural verification, the verifier's tests cover the dispatch logic). Case 036 pins the structural byte form; the verifier's logic is downstream.

## Inputs

The closed enumeration of `additional_verifications` strings under §10.12 today:

| String | Spec section | Status |
|---|---|---|
| `"backfill_seal_verified"` | §10.42 | Normative |
| `"hybrid_pqc_dual_signature_verified"` | not yet enumerated by spec | Forward-compat placeholder (used in case 036c to pin the two-entry array byte form) |

The verdict object schema:

```json
{
  "additional_verifications": ["<string from the closed enumeration>"...],
  "exit_code": <integer in {0, 1, 2, 3, 4, 5, 6}>
}
```

JCS canonicalization sorts keys lexicographically: `additional_verifications` then `exit_code`.

## Expected canonical bytes

| Sub-case | Canonical byte length | Canonical SHA-256 |
|---|---|---|
| 036a | `45` | `c79490211ce76c721560fe28d1a781e70b391353ebe3c4cf3d6aa743ab4895ba` |
| 036b | `69` | `18f280814c89104f1c728a8dbd99e87ae8d5202b6cd4a0c890e1eabccd6f6972` |
| 036c | `106` | `8062495801460b1ed1969788ebe7bcf40dce63cc9d734a3ceaea43e2cd6316a4` |

`expected_canonical.txt` carries the three sub-case canonical byte forms separated by a single LF; readers split on LF to recover each sub-case.

`expected_canonical_sha256.txt` carries the three sub-case labels and hex digests, one per line:

```
036a c79490211ce76c721560fe28d1a781e70b391353ebe3c4cf3d6aa743ab4895ba
036b 18f280814c89104f1c728a8dbd99e87ae8d5202b6cd4a0c890e1eabccd6f6972
036c 8062495801460b1ed1969788ebe7bcf40dce63cc9d734a3ceaea43e2cd6316a4
```

## Conformance behavior

A conforming implementation supporting the §10.12 amendment:

1. Constructs the verdict object as a JSON object with the two fields above.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to the `expected_canonical.txt` sub-cases.
3. Emits `additional_verifications = []` (empty array, NOT absent) on every non-zero exit code and on PASS with no bonus verifications. The empty array is structurally explicit so a consumer can detect "no bonus verifications" deterministically without conflating with "field missing."
4. Emits a known string from the closed enumeration when the corresponding bonus verification PASSed. Implementations MAY emit vendor-specific strings outside the enumeration as opaque diagnostic output, but examiner harnesses MUST treat unknown strings as opaque (the discipline mirrors the §10.12 "exit codes ≥ 4 are vendor-specific" rule one level up).
5. Preserves the integer exit code's 0-vs-non-zero contract — a PASS with bonus verifications still exits 0; the array does not shift the exit code.

## Why this case exists

The §10.12 amendment chose the structured-array approach over alternative proposals (a new exit code per bonus verification, a packed-bitfield exit code, or an out-of-band metadata file). Three reasons captured in design `07-verifier-design.md` §11.3:

1. **0-vs-non-zero contract preservation.** Shell scripts read exit 0 as PASS and non-zero as FAIL. Adding exit code 7 for "BACKFILL_SEAL_VERIFIED" presents as FAIL to anyone who hasn't read the spec.
2. **Combinatorial blow-up avoidance.** The §10.12 cryptographic-agility roadmap may introduce hybrid-PQ verification (and other bonus verifications) under future enumeration entries; further bonus verifications would otherwise demand exit codes 8, 9, 10, ... The verdict-object design absorbs the entire wave through one schema field.
3. **Composition.** Multiple bonus verifications can apply to the same chain. The array shape composes naturally; a single exit code cannot.

Case 036's sub-case 036c demonstrates the composition shape so a clean-room implementer constructing the verdict for a Story-17-shaped engagement (where the chain exercises both §10.42 and §10.53) produces the array byte-identically to the reference implementations.

## Negative cases this fixture supports

- See `negative/N026-additional-verifications-invalid-string/` for the negative case where the verdict carries an unknown string in the array — under `--strict` the verifier rejects; under default mode the unknown string passes through as opaque diagnostic.

## Cross-references

- Spec §10.12 verifier CLI exit-code contract (the section this case extends)
- Spec §10.42 backfill seal discipline (the first bonus verification using this discipline; case 035)
- Spec §10.53 hybrid post-quantum seal mandate (the dual-algorithm posture dispatched at §7 step 11; §10.53 does not extend the §10.12 enumeration today, so the second-string placeholder in case 036c remains forward-compat for any future enumeration entry)
- Design `07-verifier-design.md` §11 (the verdict-object design rationale)
- Design `12-successor-attestation-and-backfill.md` (the M&A-close composition with case 035)
- RFC 8785 (JCS canonicalization)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
