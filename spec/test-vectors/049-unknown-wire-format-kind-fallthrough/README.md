# Case 049 — Unknown wire-format kind fallthrough (§7 / PRD-3)

## What this case verifies

Spec §7 (PRD-3 normative; rolled forward from PRD-4 per the PRD-3 index)
normates verifier behavior when a v1 chain contains a top-level
wire-format kind the verifier was not built to walk. The fallthrough
rule is the load-bearing forward-compat hinge: it lets a PRD-3 verifier
ingest a chain whose seal-day post-dates a PRD-4 amendment introducing
new wire-format kinds (such as §10.62 `cross_domain_transition`) without
failing the entire run.

The rule (spec §7 step 3-4):

1. The verifier MUST NOT silently treat the unknown record as a chain entry; chain-walk steps 4-9 MUST NOT execute against it.
2. The verifier MUST NOT FAIL the entire run on the unknown kind alone.
3. The verifier MUST emit an anomaly line under `Status: PASS` of the form `unknown wire-format kind present: <kind_string> (count: N)`.
4. The verifier MUST surface the anomaly in `additional_verifications` as `additional_verifications: ['unknown_kind_present']`.
5. Institutions requiring stricter posture treat the marker as a non-PASS condition out-of-band per §7 step 5.
6. The verifier MUST recompute the per-day Merkle root and the §11 signature verification against the day's full leaf sequence including the unknown-kind records — Merkle integrity holds.

This case pins the JCS-canonical bytes for the structured verifier output (verdict + anomaly line) plus the verdict object in isolation so a clean-room implementer can compare both surfaces byte-for-byte against the reference.

## What this case does NOT verify

The chain-walk arithmetic itself — Merkle root recomputation across mixed chain-entry + unknown-kind records, per-event MAC verification on the chain-entry records, signature verification on the seal record — is covered by other vectors (001-003, 015, 026). Case 049 pins the **fallthrough verifier-output shape**: how the verifier reports the unknown kind it cannot walk, not how the verifier walks the rest of the chain.

## Inputs

A chain entry plus a §10.62 `cross_domain_transition` record under format_version `"v1"`. The verifier is a PRD-3 release (`v1.0c-verifier-2026-05-15`, `verifier_spec_version_supported = "v1.0c"`) built before §10.62 was specified; it has no semantic interpretation of the `cross_domain_transition` kind.

| Field | Value |
|---|---|
| `unknown_kind_string` | `cross_domain_transition` |
| `unknown_kind_count` | `1` |
| `verifier_spec_version_supported` | `v1.0c` |
| `verifier_version` | `v1.0c-verifier-2026-05-15` |
| `posture` | `ffiec` |
| `trust_anchor_manifest_sha256` | `7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e` |

The placeholder values for `posture`, `trust_anchor_manifest_sha256`, `verifier_spec_version_supported`, and `verifier_version` match case 036's full-shape placeholders so the verdict-object byte form composes cleanly across the two cases.

## Expected canonical bytes

| Sub-form | Length | Canonical SHA-256 |
|---|---:|---|
| `structured_output` | 389 | `5b9c5410cd0d9e6fd4208daeff338f754fd4e366093d2c2e24aa5507735187cf` |
| `verdict_only` | 272 | `917235d23e1038afc990dd55d1bc8cb9011ce837eaf3fdd48cab5d40a0ce7dde` |

`expected_canonical.txt` carries the `structured_output` bytes (the primary byte-form pin); `expected_canonical_sha256.txt` carries both hex digests.

The `structured_output` record composes the §10.12 verdict and the §7 anomaly-line list under a single JCS-canonical record. JCS sorts keys lexicographically; canonical key order is `anomaly_lines`, `status`, `verdict`.

## Conformance behavior

A conforming verifier on the fallthrough path:

1. Detects the unknown wire-format kind WITHOUT crashing or treating it as a chain entry.
2. Counts records by unknown kind and emits one anomaly line per distinct kind in the form `unknown wire-format kind present: <kind_string> (count: N)`.
3. Emits the verdict object with `exit_code = 0` (PASS) and `additional_verifications = ["unknown_kind_present"]`.
4. Recomputes Merkle root and §11 signature against the full leaf sequence (including the unknown-kind records' canonical bytes); chain integrity holds.
5. Does NOT execute chain-walk steps 4-9 against the unknown kind.

## Composition with other cases

- Case 036 — the full §10.12 verdict-object byte-form pin. Case 049's `verdict_only` SHA-256 is distinct from any 036 sub-case because the `additional_verifications` array carries `unknown_kind_present` (a marker case 036 does NOT pin in isolation; 036 sub-cases pin `backfill_seal_verified`, `class_disclosure_subtree_verified`, `cohort_coverage_attestation_verified`, `sibling_log_root_verified`).
- Future Phase 12 vector 064 — `red-black-black-side-hash-equivalence-walk` — exercises the §10.62 black-side walk on a chain that emits `cross_domain_transition` records; that vector tests the BLACK-SIDE walk semantic, where case 049 tests the FALLTHROUGH semantic for a verifier that lacks §10.62 awareness entirely.

## Cross-references

- Spec §7 — verification procedure; unknown-wire-format-kind fallthrough rule (lines 1678-1686)
- Spec §10.12 — verifier exit-code contract; `additional_verifications` discipline
- Spec §10.62 — red/black separation chain integrity (the source of the `cross_domain_transition` wire-format kind)
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin
- RFC 8785 (JCS canonicalization)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
