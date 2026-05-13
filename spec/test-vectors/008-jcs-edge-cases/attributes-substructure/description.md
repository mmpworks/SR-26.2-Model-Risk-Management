# 008-jcs-edge-cases/attributes-substructure — OTel KeyValue → flat JSON object projection

**Verifies.** §5 `attributes` / `resource` canonical projection rules. OTLP protobuf encodes attributes as repeated `KeyValue` messages with `oneof` values; the canonical projection flattens these to a JSON object with per-type rules.

## What this vector pins

1. **Flat object shape.** `attributes` is `{key: typed_value, ...}` (a JSON object), NOT `[{key, value}, ...]` (an array of records). The choice affects byte-identical conformance; the spec normates the flat-object shape.

2. **Per-type projection rules:**
   - `string` → JSON string
   - `int` (int64) → JSON integer
   - `bool` → JSON `true` / `false`
   - `double` → JSON number per RFC 8785 §3.2.2.3
   - `bytes` → JSON string under RFC 4648 base64 with padding
   - `array` → JSON array (per-element types recursively projected)
   - `kvlist` (nested) → JSON object (per the flat-object rule recursively)

3. **Key collision rejection** — two `KeyValue` entries with identical `key` strings are non-conformant.

4. **Outer-object lex sort** under JCS.

## Inputs

A canonical OTLP attribute set carrying each type plus a 3-level nested kvlist:

```
attributes = [
  KeyValue("audit.string_field", string("hello")),
  KeyValue("audit.int_field", int(42)),
  KeyValue("audit.bool_field", bool(true)),
  KeyValue("audit.double_field", double(3.14159265358979)),
  KeyValue("audit.bytes_field", bytes(0x01 0x02 0x03)),
  KeyValue("audit.array_field", array([string("a"), int(1), bool(false)])),
  KeyValue("audit.nested_kvlist", kvlist([
    KeyValue("level1.key", string("v1")),
    KeyValue("level1.nested", kvlist([
      KeyValue("level2.key", string("v2")),
      KeyValue("level2.nested", kvlist([
        KeyValue("level3.key", string("v3")),
      ])),
    ])),
  ])),
]
```

## Expected outputs

- `expected_canonical_bytes.bin` — RFC 8785 JCS-canonical encoding of the projected JSON

Expected canonical bytes (lex-sorted, no whitespace):

```json
{"audit.array_field":["a",1,false],"audit.bool_field":true,"audit.bytes_field":"AQID","audit.double_field":3.14159265358979,"audit.int_field":42,"audit.nested_kvlist":{"level1.key":"v1","level1.nested":{"level2.key":"v2","level2.nested":{"level3.key":"v3"}}},"audit.string_field":"hello"}
```

Note: `bytes(0x01 0x02 0x03)` projects as `"AQID"` (RFC 4648 base64 with padding — the 3-byte sequence requires no padding character).

## Conformance test

A v1 SDK consuming the OTLP input above and computing canonical bytes MUST produce the byte sequence in `expected_canonical_bytes.bin`.

Common implementation drift caught:
- Emitting `attributes` as an array of `{key, value}` records (the array-shape variant)
- Emitting per-value type tags (e.g., `{"audit.int_field": {"int": 42}}`) instead of bare typed values
- Re-ordering nested kvlist keys differently than top-level
- Stripping `bytes` to hex or using base64url
- Floating-point representation drift (printing `3.1415926535897900` with trailing zeros)

## Key-collision negative case

A subsidiary fixture in `negative-key-collision.json` exercises the rejection case: two `KeyValue` entries with key = `"audit.foo"`. SDKs MUST refuse at construct time with a documented error; a SDK accepting the duplicate and arbitrarily picking one is non-conformant.

## Materialization status

**Stub.** Fixture materializes in PRD-2 Phase 11-14 alongside Herald.Py and .NET SDK serialization harness.

## Cross-reference

- §5 — `attributes` / `resource` canonical projection rules
- `spec/test-vectors/008-jcs-edge-cases/otel-envelope/` — sister vector for OTel envelope projection
- RFC 8785 — JSON Canonicalization Scheme
- RFC 4648 — base64 encoding (for `bytes` values)
