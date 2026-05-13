# N036 — OTLP/JSON bytes-encoding negative vector

**Targets:** §4.4 OTLP/JSON encoding for `bytes` fields normative rule (line ~954).

**Failure mode pinned:** an OTLP/JSON emission encodes `ffiec.chain.payload_hash` (32 raw bytes) under one of: base64url (RFC 4648 §5 — `-_` alphabet, no `=` padding), padding-stripped base64 (alphabet correct but `=` stripped), or raw hex. The receiver-side decoder either rejects the bytes or decodes them to a value that, when reinterpreted as the payload_hash, produces a downstream MAC mismatch at §7 step 9.

**Verifier expected output:**
- Status: FAIL
- Step: 9
- Reason: `payload_hash MAC mismatch at seq N` (the verifier sees the decoded-then-re-MAC'd bytes differ from the computed MAC over the canonical input)

**Required for v1.0 conformance:** yes. The OTLP/JSON encoding rule is one of the few wire-level cross-encoding normative rules in the spec; conformance verifiers must reject the malformed encoding at the cross-MAC check.

**Materialization status:** stub. Fixture files (`input.json`, `expected_output.txt`, `canonical-bytes.bin`) materialize in PRD-2 Phase 11-14 alongside Herald.Py and the .NET SDK's OTLP/JSON serialization tests.

**Test framework note:** the vector exercises receiver-side decoding behavior. SDKs producing OTLP/JSON under §4.4 normative rules emit padding-correct base64; the negative case demonstrates what a non-conformant emitter would produce and the verifier's reaction. Two correct sides produce byte-equivalent output; this vector pins the failure mode.
