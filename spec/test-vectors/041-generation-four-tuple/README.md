# Case 041 — Generation prompt/output four-tuple binding (§10.47 + §10.48)

## What this case verifies

Spec §10.47 normates the four-tuple binding (system_prompt_sha256, user_prompt_sha256, retrieval_set_merkle_root_sha256, output_sha256) on a single chain entry per generation event. §10.48 extends with optional stochasticity-attestation fields (temperature, top_p, top_k, seed, model_version, model_weight_hash). This case pins a Lyceum-shape clinical decision support generation event with FULL §10.48 fields.

## Inputs

| Field | Value |
|---|---|
| `model_id` | `lyceum-medsynth-2026-04` |
| `model_version` | `2026-04-08-rc3` |
| `inference_at_utc` | `2026-04-12T10:30:15Z` |
| `temperature` | `0.0` |
| `top_p` | `1.0` |
| `top_k` | `0` |
| `seed` | `42` |
| `system_prompt_sha256` | `a039446f0b210d95c36426faea64420705810cb91f0d6b4efeba67fd024a5c2a` |
| `user_prompt_sha256` | `96498e3fc727881b396c3c66c34bfd8140820ec47966ed08217af3671d0ce09c` |
| `retrieval_set_merkle_root_sha256` | `2aefda83d3521600b0b408d2c3d66e0e7d6e962490703774084f57323874a148` (matches case 042) |
| `output_sha256` | `ef2f978944705ed2d7105c2c76f89b275b7ae7a15e995c298d6d69bb105160b2` |
| `model_weight_hash` | `SHA-256(canonical bytes of the lyceum-medsynth-2026-04-08-rc3 weight bundle)` |

## Expected canonical bytes

| Property | Value |
|---|---|
| canonical byte length | `813` |
| canonical SHA-256 | `dc74a6527ed19078aaa42e325c01b6bb5493a536c95111e87a88e4d11ee1cb30` |

## Cross-binding with case 042

The `retrieval_set_merkle_root_sha256` field MUST equal case 042's `expected_retrieval_set_merkle_root.txt` value. This is the cross-binding: a verifier can walk from the generation event to the per-document anchor events (case 042) and reconstruct the Merkle root, confirming what was retrieved.

## Conformance behavior

A conforming implementation:

1. Constructs the §10.47 + §10.48 event with the 12 fields above.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.
3. Validates bounds: `temperature ∈ [0.0, 2.0]`, `top_p ∈ [0.0, 1.0]`, `top_k ≥ 0`, `seed` is integer, all hash fields are 64-char lowercase hex, `inference_at_utc` is strict RFC 3339 UTC.

## Cross-references

- Spec §10.47 generation prompt/output four-tuple binding
- Spec §10.48 stochasticity attestation
- Spec §10.49 retrieval-source integrity (case 042)
- Spec §1.2 stochastic-output epistemic claim (the framing this section satisfies)
- Design `docs/design/14-generation-and-hitl.md`
- Case 042 `042-retrieval-set-merkle/` (cross-binding via Merkle root)
- Case 043 `043-output-grounding-review/` (the §10.50 review event referencing this generation)

## Reproduction

```
python _compute.py
```
