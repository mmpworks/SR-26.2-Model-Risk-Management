# Negative test vectors — conformance index

> **Authoritative enumeration.** This index pins each negative vector with its `(vector slot, target §7 step or pre-flight check, expected reason string, conformance class)`. A verifier passing the corpus MUST produce the expected reason string for every `required: true` vector. Vectors marked `required: false` are aspirational or address v1.x-scope failure modes.
>
> **How a verifier uses this index.** Iterate over `required: true` vectors. For each, load the vector's `input.json` (when materialized) or operationalize the `description.md` recipe; run §7; assert the verifier's `Status / Step / Reason` output matches the expected triple. Any divergence is non-conformance.
>
> **Reason-string matching.** Substantive parts must be byte-identical to the expected. Position-dependent variants like `at seq N` are token-substituted from the test inputs (N = the entry index that triggered the failure). The constant prefix and the message family are normative.

## Conformance discipline

| Field | Meaning |
|---|---|
| `Vector` | Directory slot (N001-N038 currently shipped or stubbed) |
| `Target` | §7 step number the failure attaches to, OR `pre-flight` for file-header / structural checks |
| `Expected reason` | The reason string the verifier MUST emit. Token-substitute `<N>`, `<X>`, `<A>`, `<B>` as documented in the vector's description.md |
| `Required` | `true` = part of v1.0 conformance bar; `false` = v1.x-scoped or aspirational |
| `Materialized` | `yes` = `input.json` + `expected_output.txt` exist; `stub` = description.md only |
| `Notes` | Cross-reference to spec section, secondary failure modes, or composition notes |

## Index

### Phase 1 vectors — core MAC, fingerprint, signature integrity (N001-N023)

| Vector | Target | Expected reason | Required | Materialized | Notes |
|---|---|---|:---:|:---:|---|
| N001-payload-hash-bit-flip | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | stub | §4.1 |
| N002-events-reordered | §7 step 6 | `chain link broken at seq <N>` | true | stub | §4.1 inviolate property 2 |
| N003-merkle-root-altered | §7 step 10 | `merkle root mismatch — ledger contents do not produce sealed root` | true | stub | §4.2 |
| N004-signature-garbage | §7 step 11 | `signature verification failed` | true | stub | §4.3 |
| N005-signature-wrong-tenant | §7 step 11 | `signature verification failed` | true | stub | tenant_id binding in sign_payload |
| N006-key-fingerprint-flipped | §7 step 8 | `key_fingerprint mismatch at seq <N>: looked-up IKM does not match the entry's recorded fingerprint` | true | stub | NO MAC compute (step 8 short-circuits) |
| N007-unknown-key-version | §7 step 7 | `unknown key_version: no IKM for (tenant=<T>, key_version=<V>) at seq <N>` | true | stub | NO MAC compute |
| N008-entry-format-version-mismatch | §7 step 5 | `format_version mismatch at seq <N>` | true | stub | §3 + §4.4 |
| N009-header-format-version-v2 | §7 step 1 | `format_version v2 not supported by this verifier (running v1)` | true | stub | §7 step 1 pre-flight |
| N010-header-hkdf-digest-flipped | §7 step 2 | `header HKDF inputs do not match running v1 inputs` | true | stub | §4.1.2 vendor-flag posture check |
| N011-header-genesis-nonzero | §7 step 3 | `header genesis_hash does not match v1 constant` | true | stub | §4.1 inviolate property 5 |
| N012-cross-chain-tenant-mismatch | §7 step 4 | `cross-chain lift detected at seq <N> (event.tenant_id mismatch)` | true | stub | §4.4 tenant binding |
| N013-mid-write-truncation | pre-flight | `audit file ends mid-line — possible mid-write crash` | true | stub | §7 implementation note |
| N014-botched-rotation | §7 step 8 | `key_fingerprint mismatch at seq <N>` | true | stub | §10.10 — load-bearing rotation defence |
| N015-prev-hash-substituted | §7 step 6 | `chain link broken at seq <N>` | true | stub | §4.1 inviolate property 8 |
| N016-prev-hash-and-payload-recomputed-by-attacker | §7 step 6 | `chain link broken at seq <N>` | true | stub | §4.1 inviolate property 8 (deep) |
| N017-dual-algo-partial-coverage | §7 step 11 | `partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture` | true | stub | §4.3.2 case (b); PASS-WITH-ANOMALY |
| N018-dual-algo-not-in-posture | §7 step 11 | `algorithm not on institution's declared posture list at seal_date <date>` | true | stub | §4.3.2 case (c) |
| N019-dual-algo-one-valid-one-invalid | §7 step 11 | `co-signed seal failure: algorithm <A> validated, algorithm <B> did not` | true | stub | §4.3.2 case (e); Severe |
| N020-algorithm-key-type-mismatch | §7 step 11 | `algorithm/key-type mismatch at signature verification` | true | stub | §4.3.2 |
| N021-routing-event-tampered | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | stub | §4.4.1 routing in canonical bytes |
| N022-format-version-v1-1 | §7 step 1 | `format_version v1.1 not supported by this verifier (running v1)` | true | stub | unrecognized minor within v1 family |
| N023-format-version-case-variant | §7 step 1 | `format_version "V1" not supported by this verifier (running v1)` | true | stub | case-variant rejection |

### Phase 2 vectors — extension primitives (N024-N035)

| Vector | Target | Expected reason | Required | Materialized | Notes |
|---|---|---|:---:|:---:|---|
| N024-acquirer-hsm-signature-mismatch | §7 step 11 | `acquirer-HSM signature verification failed at successor anchor` | true | yes | §10.24 entity succession |
| N025-backfill-merkle-root-corrupted | §7 step 10 | `backfill merkle root mismatch at backfill seq <N>` | true | yes | §10.42 backfill seal |
| N026-additional-verifications-invalid-string | §7 step 13 | `additional_verifications entry "<X>" not in closed enumeration` | true | yes | §10.12 closed-enum discipline |
| N027-state-machine-invalid-transition | §7 step 12 | `state-machine illegal transition at seq <N>: <from> → <to>` | true | yes | §10.43 claim state-machine |
| N028-adjuster-anchor-missing-reverse-link | §7 step 11 | `adjuster anchor missing reverse link to insurer chain entry` | true | yes | §10.45 |
| N029-bordereau-reconciled-before-received | §7 step 12 | `bordereau lifecycle out of order at seq <N>` | true | yes | §10.46 bordereau lifecycle |
| N030-output-hash-mismatch | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | yes | §10.49 generative-AI output binding |
| N031-retrieval-merkle-tampered | §7 step 11 | `retrieval set Merkle root mismatch` | true | yes | §10.49 retrieval-set Merkle |
| N032-hitl-signature-bad | §7 step 11 | `HITL reviewer signature verification failed at seq <N>` | true | yes | §10.50 human-in-the-loop |
| N033-dp-noise-seed-tampered | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | yes | §10.51 DP overlay |
| N034-decadal-reseal-previous-anchor-mismatch | §7 step 11 | `decadal re-seal previous-anchor mismatch at seal_date <date>` | true | yes | §10.54 decadal re-sealing |
| N035-challenge-response-disposition-out-of-order | §7 step 12 | `challenge-response disposition out of order at seq <N>` | true | yes | §10.55 audit-target challenge-response |

### Phase 3 vectors — second-wave additions (N036-N038)

| Vector | Target | Expected reason | Required | Materialized | Notes |
|---|---|---|:---:|:---:|---|
| N036-otlp-json-bytes-encoding | §7 step 9 | `payload_hash MAC mismatch at seq <N>` (root cause: §4.4 OTLP/JSON encoding rule violation) | true | stub | §4.4 OTLP/JSON base64-with-padding |
| N037-leap-second-captured-at | §7 step 6 (false-positive) | conformant verifier emits Status: PASS with `clock-skew anomaly at seq <N>: captured_at non-monotonic across leap-second boundary; ordering preserved by seq` | true | stub | §10.4 — the negative case is a verifier that incorrectly fails on leap-second-adjacent chains |
| N038-discovery-production-form | pre-flight | `production manifest missing required artifact: <artifact>` OR `production manifest absent — package not chain-of-custody conformant` | true | stub | §10.13.1 discovery production form |

## Materialization roadmap

The Phase 1 + Phase 2 vectors (N001-N035) are scheduled for full materialization (input.json + expected_output.txt + canonical-bytes/) alongside Herald.Py reference verifier and the .NET SDK conformance harness in PRD-2 Phase 11-14. Vectors N024-N035 are currently materialized at the level needed for the §7 implementer reading the description.md; the input.json fixtures land with the SDK release. Phase 3 vectors (N036-N038) are stubs added in the second-wave audit closure pass; their materialization follows the same Phase 11-14 cycle.

## Forward-looking PRD-4 vectors (049-083)

PRD-4 wave vectors live under positive slots `049-...` through `083-...`, not under `negative/`. The PRD-4-INDEX.md at `spec/test-vectors/PRD-4-INDEX.md` enumerates the 35 vectors planned for the PRD-4 Phase 11-14 materialization. None of those are in scope for this negative-INDEX.md.

## Cross-reference

- [`README.md`](README.md) — narrative introduction to negative vectors (the `most important cases for the rework` discussion).
- [`../PRD-4-INDEX.md`](../PRD-4-INDEX.md) — positive-vector PRD-4 wave (049-083).
- [`../chain_vectors.json`](../chain_vectors.json) — pinned positive-vector bytes for `(IKM, tenant_id)` canonical inputs.
- Spec §7 — verifier procedure each vector targets.
- Spec §10.12 — `additional_verifications` closed enumeration.
