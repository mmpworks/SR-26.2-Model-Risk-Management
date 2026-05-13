# N026 — Verdict object carries an unknown string in `additional_verifications`

## Status

**Stub case.** Recipe and expected verifier outcome documented here. Byte-level fixture is derived from case 036 by substituting an unknown string into the array.

## Purpose

Verify the §10.12 amendment / `07-verifier-design.md` §11 conformance contract: the verifier MAY produce strings outside the closed enumeration as opaque diagnostic output, but examiner harnesses MUST treat unknown strings as opaque. Under `--strict` the verifier rejects unknown strings; under default mode the unknown string passes through unchanged.

## Tampering recipe

Start from case 036b (`036-verdict-additional-verifications/` sub-case b). Replace the `additional_verifications` array's known string with one of:

**Variant A (vendor-prefixed unknown):** `["vendor-acme.custom_diagnostic"]`. The vendor-prefix shape is institution-side diagnostic output that does not collide with spec-named enumeration strings (which lack a `vendor-` prefix per §10.12).

**Variant B (unprefixed unknown):** `["BACKFILL_SEAL_VERIFIED"]` (uppercase variant of the spec string — case-mismatch). This variant tests case-sensitivity: spec strings are lowercase; an uppercase variant is unknown.

**Variant C (typo on a known string):** `["backfill_seal_verifyed"]` (typo). Tests that the verifier does NOT silently accept fuzzy matches.

## Expected verifier outcome (default mode)

```
exit_code: 0
Status: PASS
additional_verifications: [<the unknown string passes through>]
diagnostic_output: "additional_verifications contains string outside the closed enumeration; treating as opaque vendor diagnostic"
```

## Expected verifier outcome (`--strict`)

```
exit_code: 3
Status: configuration / strict-mode rejection
Reason: §10.12 strict-mode: additional_verifications contains string outside the closed enumeration ('<unknown>')
additional_verifications: []
```

The `--strict` mode rejection is exit code 3 (configuration error) rather than exit code 1 (FAIL) because the chain itself verified — the issue is the verifier's structured output carrying a string the strict-mode contract rejects. This matches the §10.12 categorical distinction: exit 1 is a chain-integrity finding; exit 3 is a configuration / strict-mode rejection.

## What this case proves

The `additional_verifications` discipline does not enable arbitrary string injection into the verdict object's load-bearing field. Examiner harnesses can rely on the closed-enumeration contract (spec-named strings only) under strict mode; vendor-specific diagnostic output is permitted in default mode but treated as opaque. The discipline parallels the §10.12 "exit codes ≥ 4 are vendor-specific opaque" rule one level up — both fields admit institution-side extension without compromising the spec-named enumeration's authority.

## Cross-references

- Spec §10.12 verifier CLI exit-code contract (the amended section)
- Design `07-verifier-design.md` §11 (the verdict-object discipline)
- Case 036 (`036-verdict-additional-verifications/`) — the positive case this negative is derived from
