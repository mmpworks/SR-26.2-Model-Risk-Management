# §10.58 binding-walk — `puf-response` identity-kind

Worked example of the §10.58 binding-walk verifier mode for a chain entry whose `cryptographic_identity` carries `identity_kind = "puf-response"`. The verifier confirms the binding-hash structurally without challenging the component; on PASS it emits `additional_verifications: ['component_identity_binding_walk_verified']` per §10.58 + §10.12.

> **Attribution.** Code in this example is extracted from the author's own implementation (MMPWorks LLC; see the conflict-of-interest disclosure in `submission/public-readme.md`), licensed under Apache 2.0. Other conformant implementations produce byte-identical output for the same inputs (verified against `spec/test-vectors/050-component-cryptographic-identity-puf-binding-walk/` once that vector lands per `spec/test-vectors/PRD-4-INDEX.md`). The implementation chosen for this example is provenance-of-code, not endorsement.

## What the example demonstrates

1. **Binding-hash construction (§10.58).** Compose the `canonical_binding_input` JSON object for a `puf-response` identity (identity_kind tag plus per-kind payload fields), apply §5 RFC 8785 JCS canonicalization, take SHA-256.
2. **Chain-entry stamping.** The chain entry carries the `cryptographic_identity` attribute payload plus the 32-byte `binding_hash` rendered as lowercase 64-character hex on the wire (per the spec's standard hex-output convention).
3. **Binding-walk verifier dispatch.** The verifier reads the chain entry, recomputes the binding-hash from the carried payload fields using the same construction, compares byte-for-byte against the stamped hash. On match: PASS with the §10.58 marker. On mismatch: FAIL with the named reason `binding-hash mismatch: canonical_binding_input non-conformant`.

## Run instructions

```
pip install jcs
python example.py
```

Output is deterministic — the example uses hard-coded inputs so the binding-hash and canonical bytes are byte-identical across runs and across conformant implementations.

## Test vector

This example's `canonical_binding_input` byte-form and binding-hash will match `spec/test-vectors/050-component-cryptographic-identity-puf-binding-walk/` once that vector lands per the PRD-4 vector-coverage matrix. Today the example serves as a draft fixture for vector 050; when the vector materializes it will reuse these inputs and outputs verbatim.

## Cross-references

- §10.58 — component cryptographic identity, identity_kind enumeration, binding-hash construction, verifier-mode dispatch
- §5 — RFC 8785 JSON Canonicalization Scheme (the universal canonicalization for hash inputs)
- §10.12 — verifier exit-code contract (exit 0 with `additional_verifications` array; new exit codes for PASS+condition cases are forbidden)
- §7 — verification procedure (the binding-walk is dispatched alongside §7 step 12 additional integrity checks)

## Files

- `example.py` — the runnable code (writer side + verifier side + demonstration block)
- `expected_output.txt` — captured stdout from running `python example.py`; byte-identical across conformant implementations
