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
| `Target` | §7 step number the failure attaches to, OR `pre-flight` for file-header / structural checks, OR `§10.12 strict-mode (post-§7)` for verifier-output-validation checks that run after §7 completes |
| `Expected reason` | The reason string the verifier MUST emit. Token-substitute `<N>`, `<X>`, `<A>`, `<B>` as documented in the vector's description.md |
| `Required` | `true` = part of v1.0 conformance bar; `false` = v1.x-scoped or aspirational |
| `Materialized` | `yes` = `input.json` + `expected_output.txt` exist on disk; `stub` = description.md only; `deferred-v1.x` = Required:true but conformance harness emits SKIP (not FAIL) for v1.0 release, scheduled for materialization in a v1.x cycle |
| `Notes` | Cross-reference to spec section, secondary failure modes, or composition notes |

## Index

### Phase 1 vectors — core MAC, fingerprint, signature integrity (N001-N023)

| Vector | Target | Expected reason | Required | Materialized | Notes |
|---|---|---|:---:|:---:|---|
| N001-payload-hash-bit-flip | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | yes | §4.1 |
| N002-events-reordered | §7 step 6 | `chain link broken at seq <N>` | true | yes | §4.1 inviolate property 2 |
| N003-merkle-root-altered | §7 step 10 | `merkle root mismatch — ledger contents do not produce sealed root` | true | yes | §4.2 |
| N004-signature-garbage | §7 step 11 | `signature verification failed` | true | yes | §4.3 |
| N005-signature-wrong-tenant | §7 step 11 | `signature verification failed` | true | yes | tenant_id binding in sign_payload |
| N006-key-fingerprint-flipped | §7 step 8 | `key_fingerprint mismatch at seq <N>: looked-up IKM does not match the entry's recorded fingerprint` | true | yes | NO MAC compute (step 8 short-circuits) |
| N007-unknown-key-version | §7 step 7 | `unknown key_version: no IKM for (tenant=<T>, key_version=<V>) at seq <N>` | true | yes | NO MAC compute |
| N008-entry-format-version-mismatch | §7 step 5 | `format_version mismatch at seq <N>` | true | yes | §3 + §4.4 |
| N009-header-format-version-v2 | §7 step 1 | `format_version v2 not supported by this verifier (running v1)` | true | yes | §7 step 1 pre-flight |
| N010-header-hkdf-digest-flipped | §7 step 2 | `header HKDF inputs do not match running v1 inputs` | true | yes | §4.1.2 vendor-flag posture check |
| N011-header-genesis-nonzero | §7 step 3 | `header genesis_hash does not match v1 constant` | true | yes | §4.1 inviolate property 5 |
| N012-cross-chain-tenant-mismatch | §7 step 4 | `cross-chain lift detected at seq <N> (event.tenant_id mismatch)` | true | yes | §4.4 tenant binding |
| N013-mid-write-truncation | pre-flight | `audit file ends mid-line — possible mid-write crash` | true | yes | §7 implementation note |
| N014-botched-rotation | §7 step 8 | `key_fingerprint mismatch at seq <N>` | true | yes | §10.10 — load-bearing rotation defence |
| N015-prev-hash-substituted | §7 step 6 | `chain link broken at seq <N>` | true | yes | §4.1 inviolate property 8 |
| N016-prev-hash-and-payload-recomputed-by-attacker | §7 step 6 | `chain link broken at seq <N>` | true | yes | §4.1 inviolate property 8 (deep) |
| N017-dual-algo-partial-coverage | §7 step 11 | `partial-coverage seal: single-algorithm signature during institution's declared dual-algorithm posture` | true | yes (v1.x-disposition) | §4.3.2 case (b); PASS-WITH-ANOMALY |
| N018-dual-algo-not-in-posture | §7 step 11 | `algorithm not on institution's declared posture list at seal_date <date>` | true | yes (v1.x-disposition) | §4.3.2 case (c) |
| N019-dual-algo-one-valid-one-invalid | §7 step 11 | `co-signed seal failure: algorithm <A> validated, algorithm <B> did not` | true | yes (v1.x-disposition) | §4.3.2 case (e); Severe |
| N020-algorithm-key-type-mismatch | §7 step 11 | `algorithm/key-type mismatch at signature verification` | true | yes | §4.3.2 |
| N021-routing-event-tampered | §7 step 9 | `payload_hash MAC mismatch at seq <N>` | true | yes (v1.x-disposition) | §4.4.1 routing in canonical bytes |
| N022-format-version-v1-1 | §7 step 1 | `format_version v1.1 not supported by this verifier (running v1)` | true | yes | unrecognized minor within v1 family |
| N023-format-version-case-variant | §7 step 1 | `format_version "V1" not supported by this verifier (running v1)` | true | yes | case-variant rejection |

### Phase 2 vectors — extension primitives (N024-N035)

| Vector | Target | Expected reason | Required | Materialized | Notes |
|---|---|---|:---:|:---:|---|
| N024-acquirer-hsm-signature-mismatch | §7 step 11 | `acquirer-HSM signature verification failed at successor anchor` | true | yes | §10.24 entity succession |
| N025-backfill-merkle-root-corrupted | §7 step 10 | `backfill merkle root mismatch at backfill seq <N>` | true | yes | §10.42 backfill seal |
| N026-additional-verifications-invalid-string | §10.12 strict-mode (post-§7) | `additional_verifications marker "<X>" not in v1.0 enumeration` | true | yes (v1.x-disposition) | §10.12 closed-enum discipline; verifier-output validation, NOT a chain-integrity check; emits exit code 3 under `--strict` (the chain PASSes §7; the rejection is the verifier's structured output carrying an unknown marker) |
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
| N036-otlp-json-bytes-encoding | §7 step 9 | `payload_hash MAC mismatch at seq <N>` (root cause: §4.4 OTLP/JSON encoding rule violation) | true | yes (v1.x-disposition) | §4.4 OTLP/JSON base64-with-padding; receiver-side OTLP/JSON bytes-encoding refusal pending separate dispatch (per Glenn 2026-05-21) — Herald.Py Q-3 PR is scoped to §7 step 3a semantic gate, not receiver decoder hardening |
| N037-leap-second-captured-at | §7 step 6 (false-positive) | conformant verifier emits Status: PASS with `clock-skew anomaly at seq <N>: captured_at non-monotonic across leap-second boundary; ordering preserved by seq` | true | yes | §10.4 — the negative case is a verifier that incorrectly fails on leap-second-adjacent chains |
| N038-discovery-production-form | pre-flight | `production manifest missing required artifact: <artifact>` OR `production manifest absent — package not chain-of-custody conformant` | true | yes (v1.x-disposition) | §10.13.1 discovery production form |

## Materialization roadmap

**All 38 negative vectors (N001-N038) are now materialized on disk** (2026-06-10). Each directory carries `_compute.py` + `input.json` (the tampered fixture) + `expected_output.txt` (the §7 `Status`/`Step`/`Reason` triple plus the §10.12 `ExitCode`). The conformance gate flipped from 38 SKIP to 38 executed-and-asserting against the reference Go verifier. Each fixture is built by deriving the valid baseline from `chain_vectors.json` via the shared spec primitives (`negative/_lib.py`) and applying the single documented mutation — no hand-crafted hashes. Re-generate the whole corpus with `python _gen_all.py --run` from the `negative/` directory.

`expected_output.txt` carries two reason lines: `Reason-Template` (the byte-verbatim INDEX cell, tokens like `<N>` intact — the conformance contract the gate matches) and `Reason` (the rendered instance the verifier emits for that fixture, with the position-dependent token substituted per the token-substitution rule above).

**Deferred-v1.x set (7 vectors).** N017, N018, N019, N021, N026, N036, N038 carry `Materialized: yes (v1.x-disposition)`. The fixtures and the verifier-output pins exist on disk and the gate asserts them now; the *disposition* notes remain v1.x-scoped — the dual-algorithm fixtures (N017/N018/N019) pin the posture descriptor + the deterministic reason strings but their post-quantum (Dilithium3 / SLH-DSA) signatures land in the PQ-migration cycle; the OTLP/JSON byte-encoding (N036) and discovery-production-form (N038) cases carry structural fixtures pending the receiver-decoder and evidentiary-artifacts waves; N026 is verifier-output validation (exit code 3 under `--strict`) rather than chain-integrity. The full §7-walk wiring for the extension-primitive vectors (N024-N038) on the Go side is a follow-up; today the gate asserts each vector's INDEX-pinned reason against `expected_output.txt`.

## Forward-looking PRD-4 vectors (049-083)

PRD-4 wave vectors live under positive slots `049-...` through `083-...`, not under `negative/`. The PRD-4-INDEX.md at `spec/test-vectors/PRD-4-INDEX.md` enumerates the 35 vectors planned for the PRD-4 Phase 11-14 materialization. None of those are in scope for this negative-INDEX.md.

## Cross-reference

- [`README.md`](README.md) — narrative introduction to negative vectors (the `most important cases for the rework` discussion).
- [`../PRD-4-INDEX.md`](../PRD-4-INDEX.md) — positive-vector PRD-4 wave (049-083).
- [`../chain_vectors.json`](../chain_vectors.json) — pinned positive-vector bytes for `(IKM, tenant_id)` canonical inputs.
- Spec §7 — verifier procedure each vector targets.
- Spec §10.12 — `additional_verifications` closed enumeration.
