# 008-jcs-edge-cases/otel-envelope — OTel envelope canonical JSON projection conformance

**Verifies.** §5 OTel envelope canonical JSON projection rules. Two implementations consuming the same OTLP protobuf input MUST produce byte-identical canonical bytes for the `payload_hash` MAC input.

## What this vector pins

The conformance witness for the per-field projection rules in §5's "OTel envelope canonical JSON projection (normative)" table:

1. **`trace_id`** projected as 32-char lowercase hex (zero-padded; no `0x` prefix). The fixture exercises an edge case where the high bytes are zero (input bytes start with `0x00 0x00 0x12...`) so a naive implementation stripping leading zeros produces a 28-char string and a different MAC input.

2. **`span_id`** projected as 16-char lowercase hex with the same zero-padding discipline.

3. **`parent_span_id` root case** (OTLP source is 8 zero bytes) projects to the literal string `"0000000000000000"`, NOT omitted from canonical JSON. Omission and explicit-zero produce byte-distinct canonical forms under JCS.

4. **`timestamp_ns`** projected as JSON integer at the IEEE-754 safe-integer boundary. The fixture exercises `timestamp_ns = 9007199254740991` (2^53 − 1, the safe-integer max). A v1.x extension that admits values exceeding the boundary must use a string form; v1.0 conformant implementations refuse to emit values larger than 2^53 − 1.

5. **`duration_ns`** projected as JSON integer.

6. **`severity`** and **`kind`** projected as the raw OTLP enum integer (NOT the text name). The fixture exercises every `SpanKind` value (0-5) and every `SeverityNumber` value (0-24).

7. **`chain_kind`** projected as a JSON string matching one of the closed-enum values per §3.

## Inputs

A canonical OTLP `Span` carrying:
- `trace_id` = `0x0000000000001234567890abcdef1234` (high-byte-zero edge case)
- `span_id` = `0x00009876543210ab` (high-byte-zero)
- `parent_span_id` = `0x0000000000000000` (root span)
- `name` = `"test-span-with-otel-envelope-conformance-witness"`
- `timestamp_ns` = `9007199254740991` (2^53 − 1)
- `duration_ns` = `42_000_000` (42ms)
- `severity` = `INFO` (= 9 in OTLP enum)
- `kind` = `INTERNAL` (= 1 in OTLP enum)
- `chain_kind` = `"audit"`
- (minimal `attributes` and `resource` to keep the vector focused on the envelope; see `attributes-substructure/` for type-projection cases)

## Expected outputs

- `expected_canonical_bytes.bin` — RFC 8785 JCS-canonical encoding of the projected JSON
- `expected_canonical_bytes_sha256.txt` — SHA-256 of the bytes (cross-implementation check)

The expected canonical bytes contain (lex-sorted JSON):

```json
{"chain_kind":"audit","duration_ns":42000000,"kind":1,"name":"test-span-with-otel-envelope-conformance-witness","parent_span_id":"0000000000000000","severity":9,"span_id":"00009876543210ab","timestamp_ns":9007199254740991,"trace_id":"0000000000001234567890abcdef1234"}
```

(no whitespace, lex-sorted keys, integer fields as integers without quoting, hex fields as quoted lowercase-zero-padded strings)

## Conformance test

A v1 SDK serializing the OTLP `Span` above and computing canonical bytes MUST produce the exact byte sequence in `expected_canonical_bytes.bin`. SHA-256 byte-equivalence check is in `expected_canonical_bytes_sha256.txt`.

A SDK producing different bytes is non-conformant. Common implementation drift this vector catches:
- Hex encoding without zero-padding (truncating leading zeros)
- Hex encoding using uppercase letters
- Root-span `parent_span_id` omitted from canonical JSON (treated as null)
- `severity` / `kind` emitted as enum text names instead of integers
- `timestamp_ns` emitted as a string (or in scientific notation) at the boundary

## Materialization status

**Stub.** Fixture materializes in PRD-2 Phase 11-14 alongside Herald.Py and the .NET SDK conformance harness. The reference implementations produce canonical bytes from the inputs above, and the SHA-256 of those bytes IS the pinned conformance witness (a different SHA-256 means a non-conformant implementation).

## Cross-reference

- §5 — OTel envelope canonical JSON projection table
- `spec/test-vectors/008-jcs-edge-cases/attributes-substructure/` — sister vector for `attributes` / `resource` substructure projection
- `spec/test-vectors/008-jcs-edge-cases/description.md` — JCS edge-cases corpus root description
- RFC 8785 — JSON Canonicalization Scheme
