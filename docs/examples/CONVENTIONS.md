# Examples — conventions

This directory hosts worked, runnable code that demonstrates spec-conformant operations. Examples are **informative**, not normative — they exist to make the spec text concrete for implementers and public-comment readers, not to set conformance requirements.

The conformance contract is the spec text plus the test-vector corpus. Examples *illustrate* that contract; they do not establish it.

## What examples are

- **Real, runnable code.** Each example compiles or runs as-is on a current platform. Pseudo-code goes in design docs (`docs/design/`), not here.
- **Attributed.** Each example names the implementation it was extracted from, the version, and the license. Other conformant implementations produce byte-identical outputs for the same inputs; the attribution is provenance-of-code, not endorsement.
- **Self-contained.** A reader who copies the example file and runs it gets the demonstrated outcome without external context.
- **Cross-referenced to test vectors.** Each example cites the spec test vector that pins its byte-form so a reader can verify the example's output against the conformance corpus.

## What examples are NOT

- **Not normative.** Conformance is established by the spec text and test vectors, not by these examples.
- **Not comparative.** Examples never claim one implementation is better than another, never benchmark, never market. Comparative claims belong to vendor-positioned material outside this repo.
- **Not advertisements.** Vendor-specific marketing, posture statements, and product comparisons stay in vendor repos.

## Directory structure

```
docs/examples/
├── CONVENTIONS.md             (this file)
├── README.md                  (index of examples)
├── 10-58-binding-walk-puf/    (one directory per example, named <section>-<short-topic>)
│   ├── README.md              (what the example demonstrates, attribution, run instructions)
│   ├── example.py             (the runnable code)
│   └── expected_output.txt    (deterministic output for byte-form verification)
└── ...
```

Directory names lead with the spec section number (e.g., `10-58-`) so a reader navigating from the spec finds the relevant example by section.

## Attribution callout template

Every example's `README.md` opens with this fenced callout, four fields filled in:

```
> **Attribution.** Code in this example is extracted from <implementation-name> <version>,
> licensed under <license>. Other conformant implementations produce byte-identical output
> for the same inputs (verified against test vector <spec/test-vectors/NNN-name>).
> The implementation chosen for this example is provenance-of-code, not endorsement.
```

If multiple mature implementations are available to back the example honestly, list them all in the callout. The attribution exists so a reader can audit the source of the code; it is not a promotion of the named implementation.

## Code style

- **Language preference: Python.** Matches the spec test-vector `_compute.py` corpus. Examples in other languages may follow when an aspect is most clearly demonstrated in that language; cite the rationale in the example's `README.md`.
- **Line budget: ≤60 lines** of substantive code per example. Examples that exceed this should be split or moved to design docs.
- **Minimal dependencies.** Python stdlib by default. The `jcs` PyPI package is permitted for RFC 8785 canonicalization. Each `README.md` lists the exact `pip install` line a reader needs.
- **Determinism.** Examples produce byte-identical output across runs. Random values, timestamps, and other entropy sources are seeded or hard-coded.

## Test-vector cross-reference

Every example cites the spec test vector that establishes its byte-form, in the example's `README.md`:

```
**Test vector.** This example's output matches `spec/test-vectors/050-component-cryptographic-identity-puf-binding-walk/expected_canonical_sha256.txt`.
```

If the vector is a follow-up budget item per `spec/test-vectors/PRD-4-INDEX.md`, note that explicitly:

```
**Test vector.** This example demonstrates §10.58 binding-walk for `factory-provisioned-key`.
The byte-form is currently a follow-up budget item per `spec/test-vectors/PRD-4-INDEX.md` V2;
when that vector lands, this example's output will be byte-equivalent.
```

## Licensing

- **Code in examples**: Apache 2.0 (matches the reference verifier license per §10.26).
- **Prose**: CC-BY-4.0.
- Examples extracted from other-licensed implementations carry the source implementation's license, named in the attribution callout.

## What examples MUST contain

1. `README.md` with attribution callout, what-it-demonstrates summary, run instructions, expected output.
2. Self-contained code file.
3. `expected_output.txt` with byte-form output (so a reviewer can verify without running).
4. Cross-reference to the relevant spec section by name (not by line number — line numbers shift across spec revisions).
5. Cross-reference to the test vector that pins the byte-form.

## What examples MUST NOT contain

1. Comparative or marketing claims about the implementation extracted from.
2. Vendor-positioning text ("X does Y better than Z").
3. Pseudo-code or non-runnable code.
4. External network dependencies (each example runs offline).
5. Hidden state or environment dependencies (run instructions cover everything needed).

## How to add an example

1. Pick a spec section that benefits from a worked code demonstration (typically one normating a verifier behavior, hash construction, canonicalization rule, or schema).
2. Create `docs/examples/<section>-<short-topic>/`.
3. Write `example.py` (or the chosen language's equivalent) following conventions above.
4. Write `README.md` with attribution + cross-references.
5. Generate `expected_output.txt` deterministically (run the example and capture stdout).
6. Update `docs/examples/README.md` index.
7. Open a PR; the reviewer checks attribution, runnability, byte-form determinism, and cross-references.

## How to revise an example

If the spec section the example demonstrates is amended (e.g., a hash construction changes), the example MUST be regenerated and `expected_output.txt` MUST be reproduced. The PR that amends the spec includes the example regeneration in the same change-set so the example never lags the spec.
