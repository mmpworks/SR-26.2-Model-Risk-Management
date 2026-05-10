# Case 045 — Public-transparency DP-bound aggregate (§10.51)

## What this case verifies

Spec §10.51 normates `chain.public_transparency.published` events that bind a DP-noised aggregate value, the DP mechanism, the ε budget, the RNG seed, and the mechanism-version hash. Per §1.2's public-transparency epistemic claim: chain binds the *noised* aggregate (the published value), NOT the *raw* aggregate; the noise application is a separate attestable step.

## Inputs

A Helvetian-shape monthly VAT-audits-initiated count published on the public-transparency portal:

| Field | Value |
|---|---|
| `aggregate_kind` | `vat_audits_initiated_count` |
| `aggregate_published_value` | `12046` (the noised value; raw is institution-confidential) |
| `coverage_period_start_utc` | `2026-05-01T00:00:00Z` |
| `coverage_period_end_utc` | `2026-05-31T23:59:59Z` |
| `published_at_utc` | `2026-06-15T09:00:00Z` |
| `dp_mechanism` | `laplace` |
| `dp_epsilon` | `1.0` |
| `dp_seed` | `4242` |
| `dp_mechanism_version_sha256` | `SHA-256(canonical bytes of helvetian-laplace-noise-sampler-v2.0-2026)` |
| `cohort_subtree_root_sha256` | optional §10.31 / §10.44 cohort cross-binding |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `731` |
| canonical SHA-256 | `9900eff01bce842a2a5e11ea0caa67065dc006faf355c37675a1627250e185d4` |

## Conformance behavior

A conforming implementation:

1. Constructs the §10.51 event with the 9 required fields plus the optional cohort cross-binding.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.
3. Validates `dp_epsilon > 0`, `dp_mechanism` in the §10.51 enumeration (or institution-named per CC8.1), `dp_mechanism_version_sha256` is 64-char lowercase hex, all UTCs are strict RFC 3339.
4. Verifier MAY optionally verify the cohort_subtree_root cross-binding when chain access permits.

## Cross-references

- Spec §10.51 public-transparency overlay
- Spec §1.2 public-transparency epistemic claim (GAP-7)
- Spec §10.31 / §10.44 cohort subtree disclosure
- Design `docs/design/15-civic-ai-and-post-quantum.md`
- `docs/regulator-pack/civic-ai-overlay.md`
- Negative case `negative/N033-dp-noise-seed-tampered/`

## Reproduction

```
python _compute.py
```
