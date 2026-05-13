# 027 — `sign-payload-v1.0c-sibling-log`

**Verifies.** §4.3 v1.0c 13-line `sign_payload` byte-form reconstruction + §10.79 operational-events sibling Merkle log binding + verifier dispatch on `sign_payload_version = "v1.0c"`.

## What this vector pins

The v1.0c byte form extends v1.0b's 12-line form with a 13th terminal line binding `hex(operational_events_log_root)` per §10.79. The vector pins:

1. **Byte form of `sign_payload` (v1.0c, 13 lines).** A reconstructable byte sequence matching the §4.3 v1.0c definition, including the magic line, `sign_payload_version = "v1.0c"`, algorithm, format_version, tenant_id, seal_date, captured-event Merkle root, HKDF-inputs digest, cadence, dev_mode, key_versions_canon, kms_handle_uris_digest, and the new operational_events_log_root.
2. **Sibling Merkle root construction.** The operational-event Merkle root is computed under RFC 6962 leaf scheme (`SHA-256(0x00 || operational_event_canonical_bytes)` for leaves; `SHA-256(0x01 || left || right)` for internal nodes), identical to the captured-event Merkle tree under §4.2.
3. **Verifier dispatch.** A verifier reading the seal with `sign_payload_version = "v1.0c"` reconstructs the 13-line form, recomputes the operational-event Merkle root from the day's `chain_kind = "operational"` entries, and confirms byte-equality with the bound `operational_events_log_root`. On mismatch, the verifier emits `operational events log root mismatch — sibling-log contents do not produce sealed root`.
4. **Empty-day case.** When the tenant-day produced zero operational events, `operational_events_log_root` is `SHA-256(b"")` = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The signature verifies cleanly under v1.0c without operational-event content.

## Inputs

A canonical chain seal with:
- `format_version = "v1"`
- `sign_payload_version = "v1.0c"`
- `algorithm = "ed25519"`
- `tenant_id = "test-tenant-v1.0c"`
- `seal_date = "2026-05-11"` (an arbitrary post-amendment day)
- Captured-event Merkle root: derived from the day's chain entries
- HKDF-inputs digest: `SHA-256(HKDF_SALT || info_for_tenant || length_LE32)`
- `cadence = "daily"`
- `dev_mode = false`
- `key_versions_canon = "1"`
- `kms_handle_uris_digest = SHA-256(utf8("aws-kms:arn:..."))`
- Operational-events log root: computed from the day's `chain_kind = "operational"` entries (this vector materializes both a non-empty case and an empty-day case)

## Expected outputs

- `expected_sign_payload.txt` — the 13-line ASCII byte form (with `0x0A` line separators between lines; NO trailing newline on the terminal `hex(operational_events_log_root)` line)
- `expected_sign_payload_sha256.txt` — SHA-256 of the byte form (for cross-implementation byte-equivalence)
- The non-empty case includes 3 operational events (a `master.reconciliation_completed`, a `verifier.run_completed`, and a `chain.verification_failure`) and their inclusion proofs to the bound root
- The empty-day case has `operational_events_log_root = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` and zero operational-event entries

## Conformance test

A verifier processing this vector under v1.0c-aware dispatch:
1. Detects `sign_payload_version = "v1.0c"` and routes to the 13-line reconstruction
2. Reconstructs the byte form per §4.3 v1.0c definition
3. Verifies the signature against the tenant public key
4. Recomputes the operational-events log Merkle root from the day's `chain_kind = "operational"` entries
5. Confirms byte-equality between the recomputed root and the bound `operational_events_log_root`
6. Emits `Status: PASS` with `additional_verifications: ['sibling_log_root_verified']`

A v1.0b-only verifier reading this vector fails fast at §7 step 11 with `sign_payload_version "v1.0c" not supported by this verifier (running v1.0b)` — the monotonic-dispatch rule prevents reconstruction under the wrong byte form.

## Materialization status

**Stub.** The `input.json`, `expected_sign_payload.txt`, `expected_sign_payload_sha256.txt`, and per-entry canonical-bytes materialize alongside Herald.Py and the .NET SDK conformance harness in PRD-2 Phase 11-14. Implementer reading the description.md before vectors land should:
1. Build the v1.0c form per §4.3 definition
2. Construct a sibling-Merkle tree from synthetic operational events
3. Sign under the tenant's Ed25519 key
4. Run their verifier and assert PASS + the `sibling_log_root_verified` marker

The byte-exact `expected_sign_payload.txt` will be the conformance pin once vectors materialize.

## Cross-reference

- §4.3 v1.0c amendment form — the 13-line byte-form definition
- §10.79 operational events sibling Merkle log — the substrate this vector exercises
- §7 step 11 — verifier dispatch on `sign_payload_version`
- §11.1 IANA Considerations — the registry entry for `sign_payload_version` values
- `spec/test-vectors/018-sign-payload-v1.0b/` — v1.0b parallel (12-line form)
- `spec/test-vectors/019-sign-payload-v1.0b-empty-day/` — v1.0b empty-day parallel
