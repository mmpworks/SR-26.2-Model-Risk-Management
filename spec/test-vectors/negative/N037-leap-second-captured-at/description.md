# N037 — Leap-second captured_at behavior negative vector

**Targets:** §10.4 leap-second normative paragraph (line ~1683). The `captured_at` non-monotonicity rule.

**Failure mode pinned:** a chain emits two consecutive entries within a single `run_id` whose `captured_at` values straddle a leap second. The earlier-`seq` entry has `captured_at = 2026-12-31T23:59:60Z` (UTC leap-second insertion); the later-`seq` entry has `captured_at = 2026-12-31T23:59:60.5Z`. Both timestamps are valid UTC under the leap-second rule. A naive verifier that uses `captured_at` for ordering would flag this as out-of-order; a conformant verifier MUST NOT FAIL — it uses the `seq` field as the ordering invariant.

The negative case the vector exercises: a verifier implementation that emits `chain link broken — captured_at out of order at seq N`. This is the wrong reason string. The correct reason string for genuine integrity failure is `payload_hash MAC mismatch at seq N`. A verifier emitting the wrong reason string on a leap-second-adjacent chain produces a false-negative integrity finding.

**Verifier expected output:**
- Status: PASS
- (Anomaly line under PASS, not a FAIL): `clock-skew anomaly at seq N: captured_at non-monotonic across leap-second boundary; ordering preserved by seq`
- exit code 0

The conformance test materializes a chain where a non-conformant verifier would emit a `chain link broken` reason; the conformant verifier emits PASS with the named anomaly.

**Required for v1.0 conformance:** yes. The leap-second rule is normative under §10.4; verifiers that fail on leap-second-adjacent chains break a normal-operations property.

**Materialization status:** stub. Fixture materializes in PRD-2 Phase 11-14 with Herald.Py's clock-mock test framework. The vector requires producing a chain whose two adjacent entries' `captured_at` values genuinely span a leap-second; the Herald.Py / .NET SDK clock-injection harness produces this.
