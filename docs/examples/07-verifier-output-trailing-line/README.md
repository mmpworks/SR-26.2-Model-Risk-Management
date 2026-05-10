# §7 verifier output — line-oriented form + Verdict-Object trailing line

Worked example of §7's verifier-output discipline: the line-oriented `Status:` / `Step:` / `Reason:` / anomaly-lines form, followed by the normative `Verdict-Object: <jcs-bytes>` trailing line that carries the closed-shape machine-readable verdict object pinned in test vector 036.

> **Attribution.** Code in this example is extracted from TesseraSeal v1.0b, licensed under Apache 2.0. Other conformant implementations produce byte-identical `Verdict-Object: <jcs-bytes>` trailing-line output for the same verdict-object inputs (verified against `spec/test-vectors/036-verdict-additional-verifications/`). The implementation chosen for this example is provenance-of-code, not endorsement.

## What the example demonstrates

1. **Verdict-object construction.** The verdict object is the JSON shape pinned in vector 036: `{"additional_verifications": [...], "exit_code": <int>}`. The `additional_verifications` array carries strings from the closed enumeration in §10.12.
2. **JCS canonicalization.** RFC 8785 JCS produces byte-identical canonical bytes across implementations. JCS sorts keys lexicographically (`additional_verifications` before `exit_code`) and uses no whitespace.
3. **Line-oriented form.** Per §7, PASS produces `Status: PASS` (one line, optionally followed by anomaly lines). FAIL produces three lines: `Status: FAIL` / `Step: N` / `Reason: <text>`. Witness mode produces `Status: PASS-STRUCTURALLY, key-bound verification skipped`.
4. **Verdict-Object trailing line.** Per §7's normative trailing-line discipline, the verifier appends `Verdict-Object: <jcs-bytes>` as the last normative line, regardless of exit code or witness mode.
5. **Round-trip parsing.** A consumer reads stdout, finds the `Verdict-Object: ` prefix, and JSON-decodes the trailing bytes — a deterministic one-pass extraction without flag dependency.
6. **All three vector-036 sub-cases.** The example produces 036a (empty additional_verifications), 036b (one marker), 036c (two markers, forward-compat composition test) and asserts each produces the byte-identical canonical SHA-256 pinned in vector 036.

## Run instructions

```
pip install jcs
python example.py
```

Output is deterministic — the example uses hard-coded inputs so the canonical bytes and SHA-256 hashes are byte-identical across runs and across conformant implementations.

## Test vector

This example's three verdict-object sub-cases byte-match `spec/test-vectors/036-verdict-additional-verifications/expected_canonical_sha256.txt`:

```
036a c79490211ce76c721560fe28d1a781e70b391353ebe3c4cf3d6aa743ab4895ba
036b 18f280814c89104f1c728a8dbd99e87ae8d5202b6cd4a0c890e1eabccd6f6972
036c 8062495801460b1ed1969788ebe7bcf40dce63cc9d734a3ceaea43e2cd6316a4
```

The example's main block reproduces these hashes from its inputs and asserts the match — running the example successfully is itself byte-equivalence proof against vector 036.

## Cross-references

- §7 — verification procedure, line-oriented output format, Verdict-Object trailing-line discipline
- §10.12 — verifier exit-code contract, additional-verifications discipline, closed-enumeration markers
- §5 — RFC 8785 JCS canonicalization (the canonical bytes for the verdict object)
- Vector 036 — pinned byte form of the verdict object; vector 036's three sub-cases are the conformance reference

## Files

- `example.py` — runnable code (verdict-object construction, line-oriented formatting, Verdict-Object trailing line, round-trip parsing, vector-036 byte-equivalence assertion)
- `expected_output.txt` — captured deterministic stdout
