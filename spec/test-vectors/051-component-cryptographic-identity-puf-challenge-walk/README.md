# Case 051 — §10.58 PUF challenge-walk

## What this case verifies

Spec §10.58 defines two verifier modes for component-cryptographic identity. Case 050 pins the **binding-walk** path (component need not be in-hand); case 051 pins the **challenge-walk** path (component MUST be in-hand). For the `puf-response` identity-kind, both modes are available.

The challenge-walk verifier challenges the component directly (PUF challenge-response, manufacturer-CA online verification) and confirms the chain entry's identity-binding matches the live component. The marker `component_identity_challenge_walk_verified` is the dispatch surface for tooling that requires challenge-walk evidence for a particular regulatory regime.

Three byte-forms are pinned:

1. The JCS-canonical bytes of the §10.58 `canonical_binding_input` JSON object — byte-identical to case 050 by design (same synthetic component appears under both walks).
2. The mocked PUF challenge-response oracle output — a structured dict pinning `puf_challenge_id`, `expected_response_hex` (the value bound on the chain entry), `live_response_hex` (the value returned by the mocked oracle at challenge-walk time), and `match` (boolean).
3. The §10.12 verdict object emitted on challenge-walk PASS: `exit_code = 0`, `additional_verifications = ["component_identity_challenge_walk_verified"]`.

## What this case does NOT verify

PUF hardware behavior, the cryptographic strength of any specific PUF construction, or the operational discipline for in-hand component custody during challenge-walk are out of scope. This case pins the **byte form** of the binding-input, the oracle output, and the verifier verdict; the cryptographic + operational layers are addressed by §10.58 spec text and the institution's CC8.1.

The mocked oracle returns the same value the chain entry binds (happy-path challenge-walk). A non-matching fixture — where `live_response_hex` differs from `expected_response_hex` and the verifier emits the binding-mismatch anomaly — is a negative-case candidate for a future N0XX vector.

A verifier invoked without the component (the typical remote-walk case) executes binding-walk only; an attempt to challenge-walk without the component fails with `Reason: challenge-walk requested but component not present` (exit code 3, configuration error per §10.12). That failure path is not pinned in this vector.

## Inputs

A synthetic PUF identity binding plus a mocked challenge-response oracle output. The component values are byte-identical to case 050.

| Field | Value |
|---|---|
| `identity_kind` | `puf-response` |
| `component_id` | `as6171-sample-component-2026-05-21-001` |
| `puf_challenge_id` | `darpa-shield-puf-challenge-class-A-2026-05` |
| `puf_response_hex` (expected) | `SHA-256("050-puf-response::component=<component_id>::challenge=<challenge_id>")` |
| `live_response_hex` (oracle) | equals `puf_response_hex` (happy path) |
| `match` | `true` |

Recipe-driven; `_compute.py` documents the synthetic-PUF-response derivation inline.

## Expected canonical bytes

| Sub-form | Length | Canonical SHA-256 |
|---|---:|---|
| `canonical_binding_input` | 238 | `8ba3334374f19abc8fab7ac00cf041bc1b9f99c546a7ee68d7c40a0e4de6b753` |
| `binding_hash_hex` | n/a (32 raw bytes) | `8ba3334374f19abc8fab7ac00cf041bc1b9f99c546a7ee68d7c40a0e4de6b753` |
| `challenge_oracle_output` | 256 | `478376b6b8d4cd84b3c828d6b5c130c6e17f1ad6f3bb809b8499f20139f15955` |
| `verdict` | 294 | `e8936ea55f7c6011ffd6d8156b2ef79a7920a7046ea33b0d3a142a821bd69e65` |

`expected_canonical.txt` carries the three sub-forms separated by single LF characters in order: binding-input, oracle-output, verdict. A reader splits on LF to recover each.

The binding-input SHA-256 matches case 050's binding-input SHA-256 byte-for-byte — that's the design intent. The cross-vector composition lets a clean-room implementer assert "same component, two walks, two verdicts" with a single binding-hash anchor.

## Conformance behavior

A conforming implementation supporting §10.58 challenge-walk:

1. Reuses the case 050 `canonical_binding_input` byte form verbatim — the binding lives on the chain entry regardless of which walk the verifier subsequently runs.
2. Constructs the challenge-response oracle output as a four-field dict (`expected_response_hex`, `live_response_hex`, `match`, `puf_challenge_id`); JCS sorts keys lexicographically.
3. On challenge-walk PASS (live response bytes match expected response bytes), emits the §10.12 verdict object with `exit_code = 0` and `additional_verifications = ["component_identity_challenge_walk_verified"]`.
4. JCS-canonicalizing all three sub-forms produces bytes byte-identical to the corresponding `expected_canonical.txt` segment.
5. The verifier MUST have the component in-hand for challenge-walk; absence triggers exit code 3 per §10.12 (not pinned in this vector).

## Composition with other cases

- Case 050 (`050-component-cryptographic-identity-puf-binding-walk/`) — the binding-walk companion. The binding-input SHA-256 is byte-identical between cases 050 and 051.
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin in the general case.
- Future negative case — `live_response_hex != expected_response_hex` triggers `binding-hash mismatch at seq N: canonical_binding_input non-conformant`.

## Cross-references

- Spec §10.58 — component cryptographic identity primitive (challenge-walk dispatch at spec lines 3606-3611)
- Spec §10.12 — verifier exit-code contract; `additional_verifications` discipline
- Case 050 (`050-component-cryptographic-identity-puf-binding-walk/`) — the binding-walk companion
- Case 036 (`036-verdict-additional-verifications/`) — full §10.12 verdict-object byte-form pin
- RFC 8785 (JCS canonicalization)
- DARPA SHIELD program documentation
- ISO/IEC 20897 (PUF security requirements)

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package.
