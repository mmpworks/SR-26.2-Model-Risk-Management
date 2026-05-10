# Case 034 — Successor-attestation envelope (§10.39)

## What this case verifies

Spec §10.39 normates the `chain.successor_attestation` operational event the acquirer's chain emits at acquisition close when the acquired institution's pre-acquisition records are not under a chain conformant to this specification. The envelope schema is byte-locked across implementations:

```json
{
  "acquired_entity_legal_name": "<legal name of the acquired institution>",
  "acquired_entity_lei": "<RFC 9101 LEI, 20 chars>",
  "acquirer_hsm_key_fingerprint": "<lowercase hex SHA-256, 64 chars>",
  "baseline_manifest_kind": "<one of the §10.39 enumeration>",
  "baseline_manifest_sha256": "<lowercase hex SHA-256, 64 chars>",
  "companion_backfill_seal_run_id": "<run_id of the paired §10.42 record>",
  "dual_signatures": [<from-entity §10.17 sig>, <to-entity §10.17 sig>],
  "effective_utc": "<RFC 3339 UTC>"
}
```

This case pins the JCS-canonical (RFC 8785) bytes for a Northbridge-shaped envelope (Northbridge Federal Savings acquires Cape Madeline Bank & Trust; Cape Madeline operated baseline-diary records for the prior 30 months) so a clean-room implementation proves it constructs the §10.39 envelope identically.

## What this case does NOT verify

The dual_signatures content is a synthetic placeholder. Real signatures are Ed25519 over the §10.17 signatory schema; case 034 pins the **envelope** byte form — the wrapper around the signatures — not the signatures' cryptographic validity. The Ed25519-signature byte form is covered by `018-sign-payload-v1.0b/`. Case 034 stays focused on the envelope's JCS-canonical layout.

## Inputs

| Field | Value |
|---|---|
| `acquired_entity_legal_name` | `Cape Madeline Bank & Trust` |
| `acquired_entity_lei` | `529900CMBT034FFIEC01` (synthetic 20-char LEI) |
| `baseline_manifest_kind` | `baseline_diary` (§10.39 enumeration) |
| `effective_utc` | `2026-04-15T14:00:00Z` |
| `acquirer_hsm_key_fingerprint` | `SHA-256(synthetic 32-byte HSM pubkey)` |
| `baseline_manifest_sha256` | `SHA-256(JCS-canonical 8-tuple baseline manifest)` |
| `companion_backfill_seal_run_id` | `northbridge-cape-madeline-close-2026-04-15` (links to case 035) |
| `dual_signatures` | 2 §10.17-shaped signature objects (from-entity Cape Madeline CISO + to-entity Northbridge CISO) |

The synthetic acquirer HSM pubkey and the synthetic baseline-manifest tuples are deterministic; the recipes are documented in `_compute.py` and any reader can recompute the byte values from first principles.

## Expected canonical bytes

| Property | Value |
|---|---|
| envelope canonical byte length | `839` |
| envelope canonical SHA-256 | `1cc371b8fff05ee5bb420753c04ea6f1883297b615911dc5824e65ed1a1f1935` |
| baseline manifest SHA-256 | `880f875178fce4c3b55ee5503c755457d1b820e24a5a90d7ad2245797f9c8488` |
| acquirer HSM fingerprint | `192f993a79e006034df6479a87336a5097fc5b2228c6ceb60ba2ea0653beda81` |

`expected_canonical.txt` carries the bytes verbatim; `expected_canonical_sha256.txt` is the SHA-256 for quick comparison.

JCS canonicalization sorts object keys lexicographically. The envelope's keys appear in canonical order: `acquired_entity_legal_name`, `acquired_entity_lei`, `acquirer_hsm_key_fingerprint`, `baseline_manifest_kind`, `baseline_manifest_sha256`, `companion_backfill_seal_run_id`, `dual_signatures`, `effective_utc`. Each signature object's keys also appear in canonical order: `entity_affiliation`, `name`, `role`, `signature_b64`.

## Conformance behavior

A conforming implementation supporting §10.39:

1. Constructs the successor-attestation envelope as a JSON object with the eight fields above.
2. Canonicalizes per RFC 8785 (JCS) and produces bytes byte-identical to `expected_canonical.txt`.
3. Refuses any envelope whose `baseline_manifest_kind` is outside the §10.39 enumeration with a control-completeness failure.
4. Bounds `acquirer_hsm_key_fingerprint` and `baseline_manifest_sha256` at exactly 64 lowercase hex chars per §10.39.
5. Bounds `acquired_entity_lei` at exactly 20 chars per RFC 9101.
6. Bounds `effective_utc` at RFC 3339 UTC form (always ending `Z`, no offset notation).
7. When `companion_backfill_seal_run_id` is present, the value is a non-empty string identifying the paired §10.42 record.

## Composition with §10.42 (case 035)

The `companion_backfill_seal_run_id` field anchors this attestation event to the paired §10.42 backfill seal record. Case 035 pins the backfill seal's byte form using the same `run_id` value (`northbridge-cape-madeline-close-2026-04-15`) and the same `baseline_manifest_sha256` so a verifier can confirm the bidirectional linkage.

## Negative cases this fixture supports

- A producer that emits `baseline_manifest_kind` outside the §10.39 enumeration produces canonical bytes that diverge.
- A producer that emits `acquirer_hsm_key_fingerprint` with uppercase hex chars produces canonical bytes that diverge.
- A producer that omits `dual_signatures` (or carries fewer than two signatures) produces a structurally non-conformant envelope.
- A producer that swaps the `entity_affiliation` values between the two signatures produces canonical bytes that diverge — JCS sorts the array as written, not by entity-affiliation.
- See `negative/N024-acquirer-hsm-signature-mismatch/` for the negative case where the fingerprint declared in the envelope does not match the dual_signatures' signing key.

## Cross-references

- Spec §10.39 institutional successor-attestation (the section this case pins)
- Spec §10.17 signatory schema (the dual_signatures shape)
- Spec §10.24 entity succession (the legal-entity-change paired event)
- Spec §10.42 backfill seal discipline (the cryptographic complement; case 035)
- Design `12-successor-attestation-and-backfill.md` (the design rationale)
- RFC 8785 (JCS canonicalization)
- RFC 9101 (Legal Entity Identifier)
- Case 008 (`008-jcs-edge-cases/`) — the JCS conformance bar
- Case 035 (`035-backfill-seal/`) — the §10.42 companion record

## Reproduction

```
python _compute.py
```

Depends on the Python `jcs` package (Anders Rundgren's reference RFC 8785 implementation).
