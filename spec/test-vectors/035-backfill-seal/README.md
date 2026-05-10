# Case 035 — Backfill seal record (§10.42)

## What this case verifies

Spec §10.42 normates the one-time backfill seal record at acquisition close when the acquired institution's pre-acquisition records are under a non-chain shape (§10.39 `baseline_manifest_kind ∈ {"baseline_diary", "mixed"}`). The backfill seal is a v1.0b `sign_payload`-bound seal record where the additional §10.42 attributes are bound through the Merkle root via a metadata leaf. The locked v1.0b 12-line wire form is unchanged; the §10.42 attributes ride alongside via the Merkle leaf they hash into.

This case pins three byte forms:

1. **The §10.42 metadata-leaf JCS-canonical bytes.** The structure that carries `seal.backfill_at_close = true`, the window timestamps, the baseline-manifest cross-binding hash, the companion attestation run_id, and the dual_signatures.
2. **The Merkle root over (8 institutional baseline manifest leaves + 1 metadata leaf)** under RFC 6962 with the §4.2 leaf and inner hash domain separators.
3. **The v1.0b `sign_payload` form** for this seal — the 12-line newline-joined bytes the HSM signs. The signature itself is outside this case's scope; case 018 pins the v1.0b signature path generally.

## What this case does NOT verify

The Ed25519 signature byte form is NOT pinned here. Case 018 (`018-sign-payload-v1.0b/`) pins the signing path; case 035 reuses 018's recipe and pins what is distinctive about §10.42 — the metadata leaf and the Merkle composition. The `kms_handle_uris_digest_hex` and `hkdf_inputs_digest_hex` values in the sign_payload are synthetic placeholders (real values are pinned by cases 010 and 018); case 035 exercises the *structural* binding, not the cryptographic-input pin.

## Inputs

### Seal record fields (v1.0b sign_payload bound)

| Field | Value |
|---|---|
| `tenant_id` | `northbridge-federal-savings` |
| `seal_date` | `2026-04-15` (the day-of-close) |
| `sign_payload_version` | `v1.0b` |
| `algorithm` | `ed25519` |
| `format_version` | `v1` |
| `cadence` | `daily` |
| `dev_mode` | `false` (`0` in the canonical byte form) |
| `key_versions_canon` | `1` |
| `kms_handle_uris_digest_hex` | synthetic 64-char hex |

### §10.42 metadata-leaf fields

| Field | Value |
|---|---|
| `seal.backfill_at_close` | `true` |
| `seal.backfill_window_start_utc` | `2024-10-15T00:00:00Z` (Cape Madeline's earliest baseline-diary record) |
| `seal.backfill_window_end_utc` | `2026-04-15T14:00:00Z` (day-of-close) |
| `seal.backfill_baseline_manifest_sha256` | matches case 034's `baseline_manifest_sha256` |
| `seal.backfill_companion_attestation_run_id` | `northbridge-cape-madeline-close-2026-04-15` (matches case 034) |
| `seal.dual_signatures` | matches case 034's dual_signatures pair |

The metadata-leaf is JCS-canonicalized; the canonical bytes appear in `expected_canonical.txt`.

## Expected byte forms

| Property | Value |
|---|---|
| metadata leaf canonical byte length | `728` |
| metadata leaf canonical SHA-256 | `b55c05cc7a7b5245cfccfd7be293d8d2bbfe360ba6fba341809f4960a68ce3c2` |
| baseline manifest SHA-256 | `880f875178fce4c3b55ee5503c755457d1b820e24a5a90d7ad2245797f9c8488` |
| Merkle root (9 leaves: 8 baseline + 1 metadata) | `8943b16ee4fdb413e849c6909c5d79b71fa96962a5710cdd6a763bf09342c340` |
| sign_payload byte length | `286` |
| sign_payload SHA-256 | `826a53072ffbcbf74b549bca167374ffa513205b842e9d1a31117482a2fdcf0c` |

`expected_canonical.txt` carries the metadata-leaf bytes verbatim.
`expected_canonical_sha256.txt` is the SHA-256 of the metadata leaf.
`expected_sign_payload.txt` carries the v1.0b sign_payload bytes verbatim.
`expected_sign_payload_sha256.txt` is the SHA-256 of the sign_payload.
`expected_merkle_root_hex.txt` is the Merkle root over the 9 leaves.

## The bidirectional linkage with case 034

Case 034 (successor-attestation) and case 035 (backfill seal) are paired. They share:

- The same `baseline_manifest_sha256` (`880f875178fce4c3b55ee5503c755457d1b820e24a5a90d7ad2245797f9c8488`) — case 034's `baseline_manifest_sha256` field equals case 035's `seal.backfill_baseline_manifest_sha256`.
- The same companion `run_id` (`northbridge-cape-madeline-close-2026-04-15`) — case 034's `companion_backfill_seal_run_id` equals case 035's `seal.backfill_companion_attestation_run_id`.
- The same dual_signatures pair (Cape Madeline CISO + Northbridge CISO).

A verifier traversing from case 034 to case 035 (or vice versa) confirms the bidirectional linkage by these three equalities. Mismatch on any of them is a control-completeness anomaly the §10.42 verifier-dispatch path surfaces.

## Conformance behavior

A conforming implementation supporting §10.42:

1. Constructs the metadata-leaf as a JSON object with the six fields above.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.
3. Computes leaf hashes as `SHA-256(0x00 || leaf_canonical_bytes)` per RFC 6962 / §4.2.
4. Computes inner hashes as `SHA-256(0x01 || left_hash || right_hash)` per RFC 6962 / §4.2.
5. Promotes the rightmost odd leaf at any internal level per RFC 6962 §2.1 (this case has 9 leaves so the construction exercises the odd-leaf promotion).
6. Builds the v1.0b sign_payload as the 12-line newline-joined form per §4.3 and case 018's recipe.
7. On verification: the verifier recomputes the Merkle root from the institutional baseline manifest leaves and the metadata-leaf canonical bytes, compares to the seal's apex root, and dispatches to the §10.42 verification path when `metadata_leaf["seal.backfill_at_close"]` is `true`.

## Verifier dispatch

When the metadata leaf carries `seal.backfill_at_close = true`, the verifier executes the §10.42 five-step verification path:

1. Recompute the Merkle root over (baseline manifest leaves + metadata leaf).
2. Confirm the recomputed root matches the seal's apex root.
3. Confirm `metadata_leaf["seal.backfill_baseline_manifest_sha256"]` matches the SHA-256 of the canonicalized baseline manifest.
4. Confirm both `metadata_leaf["seal.dual_signatures"]` entries verify under their declared signing keys per §10.17.
5. Confirm the companion §10.39 successor-attestation event exists and its `companion_backfill_seal_run_id` references this seal's run_id.

On all five steps PASS, the verifier records `backfill_seal_verified` in the verdict's `additional_verifications` array (per §10.12 amendment; lowercase snake_case per the §10.12 marker-namespace convention) and exits with code 0. Failure at any step records the spec-named anomaly reason.

## Negative cases this fixture supports

- See `negative/N025-backfill-merkle-root-corrupted/` for the negative case where a single byte of the Merkle root is flipped — verifier surfaces the recomputation mismatch.
- See `negative/N024-acquirer-hsm-signature-mismatch/` for the negative case where the case-034 envelope's acquirer-HSM key fingerprint does not match the dual_signatures' actual signing key.

## Cross-references

- Spec §10.42 backfill seal discipline (the section this case pins)
- Spec §10.36 supplemental-seal pattern (the precedent §10.42 follows)
- Spec §10.39 successor-attestation (the companion event; case 034)
- Spec §4.2 daily Merkle seal (the base seal substrate)
- Spec §4.3 sign_payload v1.0b (the wire form)
- Design `12-successor-attestation-and-backfill.md` (the design rationale)
- RFC 6962 (Certificate Transparency Merkle tree)
- RFC 8785 (JCS canonicalization)
- Case 018 (`018-sign-payload-v1.0b/`) — the v1.0b sign_payload form pin
- Case 026 (`026-hierarchical-merkle-aggregation/`) — the hierarchical Merkle pattern §10.42 reuses
- Case 034 (`034-successor-attestation/`) — the §10.39 companion event

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
