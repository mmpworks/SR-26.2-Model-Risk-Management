# Case 047 — Decadal re-sealing (§10.54)

## What this case verifies

Spec §10.54 normates the decadal re-sealing discipline as an annotated v1.0b seal record (mirrors §10.42 backfill seal's pattern). Discriminating attributes route the verifier to the §10.54 verification path. This case pins the metadata-leaf canonical bytes for a Helvetian-shape first-decadal re-seal at the 2036-12-31 boundary under Dilithium3.

## Inputs

| Field | Value |
|---|---|
| `seal.resealed_at_decadal_boundary` | `true` |
| `seal.resealed_window_start_utc` | `2026-12-31T23:59:59Z` |
| `seal.resealed_window_end_utc` | `2036-12-31T23:59:59Z` |
| `seal.resealed_under_algorithm` | `dilithium3` |
| `seal.resealed_generation_index` | `1` (the first decadal re-seal; generation 0 is the original seal) |
| `seal.resealed_baseline_manifest_sha256` | `518010463d0b8097fdaa32d66acf9e21164577cf517ade48446c0ff5c3b44e52` |
| `seal.resealed_previous_generation_anchor_sha256` | `4bd76d1d17fcdabd40fe6b2dea4b288af60ab8ae6f2734908076ff6fa3d48bf6` |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `457` |
| canonical SHA-256 | `0f47bc32665a8d021a2a5243508d2a18e2d7ed1add54c55fa0431722d35112de` |

## Conformance behavior

A conforming implementation:

1. Constructs the §10.54 metadata-leaf with the 7 required attributes.
2. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to `expected_canonical.txt`.
3. The full seal record (the v1.0b sign_payload + signatures list) is built around this metadata leaf via the Merkle composition and signing path; case 047 pins the metadata-leaf canonical bytes only.
4. Verifier dispatches on `seal.resealed_at_decadal_boundary = true` to the §10.54 verification path; recomputes the baseline-manifest SHA-256, verifies the dual-algorithm `signatures` list under §10.53, confirms the previous-generation anchor exists on the chain.

## Composition with §10.53 hybrid PQ

When the institution operates dual-algorithm posture per §10.53, the re-seal record is co-signed under both legacy (Ed25519) and PQC (Dilithium3) algorithms via the §4.2 `signatures` list. The `seal.resealed_under_algorithm` attribute names the *primary* algorithm at the re-seal moment.

## Cross-references

- Spec §10.54 decadal re-sealing
- Spec §10.42 backfill seal (the precedent §10.54 follows)
- Spec §10.36 supplemental-seal pattern
- Spec §10.53 hybrid PQ seal mandate (the dual-algorithm composition)
- Spec §4.3 sign_payload v1.0b (the wire form)
- Negative case `negative/N034-decadal-reseal-previous-anchor-mismatch/`

## Reproduction

```
python _compute.py
```
