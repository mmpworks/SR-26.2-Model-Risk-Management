---
title: "PRD-3.1 External Review Package"
purpose: "Reading order and scope guide for external reviewers evaluating PRD-3.1"
date: 2026-05-24
status: "INTERNAL -- do not distribute without Steve's approval"
---

# PRD-3.1 External Review Package

This document tells an external reviewer which files to read, in what order, and what to look for when evaluating PRD-3.1.

---

## Reading order

### Pass 1: Understand what PRD-3.1 claims

1. **`docs/releases/prd-3.1.md`** (this repo) -- release notes. Establishes what shipped, what changed, what did not change. Read this first to scope the review.

2. **`spec/chain-of-custody-DRAFT-0.3.0.md` sections 14.6, 14.7, 14.8** -- the normative spec text for the three attribute families. The reviewer is checking whether the reference implementations conform to what these sections require. Key items:
   - Section 14.6 closed enum table (seven values for `authentication_method`)
   - Section 14.7 closed enum table (seven values for `substrate_kind`)
   - Section 14.8 required-field list and format constraints (`change_record_id_hash` = 64-char lowercase hex; `applied_at_utc` = RFC 3339 UTC with Z suffix)
   - Each section's "Reference-implementation status" block (should now read SHIPPED)

3. **`spec/chain-of-custody-DRAFT-0.3.0.md` section 14.12** -- the open-items status table. O-4 and O-6 should read SHIPPED. O-1/O-2/O-3/O-5/O-7 remain FORTHCOMING. O-8 remains EXOGENOUS.

### Pass 2: Verify the C# reference implementation

4. **`Herald.Compliance/src/Audit/Chain/AuditActor.cs`** -- section 14.6 emitter. Check: SHA-256 hex validation, closed-enum rejection, delegation-chain lex-sort, JCS-canonical JSON output.

5. **`Herald.Compliance/src/Audit/Chain/ReasoningSubstrate.cs`** -- section 14.7 emitter. Check: closed-enum coverage, JCS-canonical JSON output.

6. **`Herald.Compliance/src/Audit/Chain/DownstreamAction.cs`** -- section 14.8 emitter. Check: required-field enforcement, hash format validation, RFC 3339 UTC validation, JCS-canonical JSON output.

7. **`Herald.Compliance/tests/AuditActorTests.cs`**, **`ReasoningSubstrateTests.cs`**, **`DownstreamActionTests.cs`** -- unit tests for the three emitters.

### Pass 3: Verify the Python reference implementation

8. **`Herald.Py/src/herald/_audit_actor.py`** -- section 14.6 emitter (Python).

9. **`Herald.Py/src/herald/_reasoning_substrate.py`** -- section 14.7 emitter (Python).

10. **`Herald.Py/src/herald/_downstream_action.py`** -- section 14.8 emitter (Python).

### Pass 4: Verify the Go verifier

11. **`ffiec/verifier/internal/verify/attributes.go`** -- type definitions. Check: JSON field names match the spec attribute names exactly.

12. **`ffiec/verifier/internal/verify/predicates.go`** -- validation functions. Check: enum tables match section 14.6/14.7 closed enums; hash validation matches 64-char lowercase hex; RFC 3339 UTC validation requires Z suffix; delegation-chain lex-sort uses JCS-canonical JSON.

13. **`ffiec/verifier/internal/verify/predicates_test.go`** -- 62 test cases. Check: every closed-enum value has a positive test; negative tests cover rejection of unknown enum values, malformed hashes, wrong timestamp formats, unsorted delegation chains.

14. **`ffiec/verifier/internal/verify/attributes_integration_test.go`** -- 40 integration tests. Check: cross-family composition, HMAC chain integration with attribute-bearing entries.

15. **`ffiec/verifier/internal/verify/pipeline.go`** -- the verification pipeline. Check: attribute validation is additive (does not gate structural/MAC pass); `AdditionalVerification` output shape matches section 10.12 discipline.

### Pass 5: Verify conformance vectors

16. **`spec/test-vectors/`** -- spot-check 3-5 vectors from each range (050-059, 060-066, 067-074, 075-084). For each vector:
    - Read `README.md` for the scenario description
    - Read `input.json` for the chain entry payload
    - Run `_compute.py` and confirm it produces `expected_canonical.txt`
    - Confirm the SHA-256 of `expected_canonical.txt` matches `expected_canonical_sha256.txt`

### Pass 6: Evaluate the documentation

17. **`Herald.Compliance/docs/sdk-reference-section-14-attributes.md`** -- SDK reference. Check: attribute tables match the spec; calling conventions are clear; C# and Python examples are present.

18. **`Herald.Compliance/docs/kognitos-projection.md`** -- Kognitos projection. Check: 12-field mapping table is complete; every Kognitos field has a TesseraSeal source cited.

19. **`Herald.Compliance/docs/framework-portability.md`** -- Framework portability. Check: architectural argument is coherent; proof-by-construction claim is supported by the Kognitos projection.

---

## What to look for

### Conformance questions

- Do all three reference implementations (C#, Python, Go) produce byte-identical JCS-canonical JSON for the same inputs?
- Does the Go verifier correctly reject inputs that violate the spec constraints (wrong enum values, malformed hashes, unsorted delegation chains, non-UTC timestamps)?
- Are the conformance vectors sufficient to pin the behavior they claim to pin?

### Architectural questions

- Is the additive-verification design sound? Attribute validation failures in `additional_verifications` do not gate the core structural/MAC pass. Is that the right boundary?
- Is the Kognitos projection complete? Does every Kognitos field map to a TesseraSeal source?
- Is the framework-portability argument well-grounded? Could a reviewer build a second projection (e.g., for GDPR or SR 11-7) from the documented pattern?

### Scope questions

- PRD-3.1 claims to change NO normative spec text. Confirm that sections 14.6/14.7/14.8 body text is identical between the prd-3 tag and the PRD-3.1 state.
- PRD-3.1 claims the wire-format identifier is unchanged. Confirm v1 is still the identifier.
- PRD-3.1 claims document version is still 0.3.0. Confirm no version bump.

---

## Repository locations

| Artifact | Repository | Path |
|---|---|---|
| Spec text | ffiec-public | `spec/chain-of-custody-DRAFT-0.3.0.md` |
| Test vectors | ffiec-public | `spec/test-vectors/050-*` through `spec/test-vectors/053-*` (Phase 11 shared primitives, O-6) |
| Negative vectors | ffiec-public | `spec/test-vectors/negative/` |
| Go verifier | ffiec | `verifier/internal/verify/` |
| C# reference | Herald (umbrella) | `Modules/Herald.Compliance/src/Audit/Chain/` |
| Python reference | Herald.Py | `src/herald/` |
| SDK reference doc | Herald (umbrella) | `Modules/Herald.Compliance/docs/sdk-reference-section-14-attributes.md` |
| Kognitos projection | Herald (umbrella) | `Modules/Herald.Compliance/docs/kognitos-projection.md` |
| Framework portability | Herald (umbrella) | `Modules/Herald.Compliance/docs/framework-portability.md` |
| Shift runbook | VectorCompiler | `docs/shift-runbook.md` |
| Release notes | ffiec-public | `docs/releases/prd-3.1.md` |

---

## Note on VectorCompiler

The VectorCompiler (Herald.TesseraSeal.VectorCompiler) is MMPWorks-proprietary tooling. Its DSL, decorator system, corruption primitives, and extension seams are not part of the review package. The review covers the VectorCompiler's outputs (conformance vectors), not the tool itself. The shift runbook is included because it documents the operational procedure an external reviewer would use if they needed to regenerate vectors, but the VectorCompiler source is not distributed.
