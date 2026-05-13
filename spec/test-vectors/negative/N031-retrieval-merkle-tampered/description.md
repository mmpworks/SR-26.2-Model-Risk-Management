# N031 — Retrieval-set Merkle root mismatch

## Status

**Stub case.** Recipe and expected verifier outcome documented here.

## Purpose

Verify the §10.49 Merkle integrity claim: the `retrieval_set_merkle_root_sha256` bound on the parent §10.47 generation event MUST match the recomputed root over the per-document anchor events' `document_sha256` leaves. Mismatch is a chain-integrity failure.

## Tampering recipe

Start from cases 041 + 042. Modify ONE of:

**Variant A — apex root tampered:** Flip a character in the §10.47 event's `retrieval_set_merkle_root_sha256` value. The §10.49 verifier dispatch step (3) recomputes the Merkle root from the per-document anchor events and finds a mismatch.

**Variant B — leaf hash tampered:** Modify one document's `document_sha256` on a per-document anchor event. The recomputed Merkle root differs from the apex root on the parent §10.47 event.

**Variant C — missing document anchor:** Remove one of the per-document anchor events while leaving the §10.47 Merkle root unchanged. The recomputed root over the remaining N-1 leaves does not match the bound root over N leaves.

## Expected verifier outcome

```
exit_code: 1
Status: FAIL
Reason: §10.49 retrieval-set integrity failure: <variant-specific reason>
  - Variant A: retrieval_set_merkle_root_sha256 on parent generation event does not match recomputed root from per-document anchor events
  - Variant B: per-document anchor event's document_sha256 produces leaf hash that breaks the recomputed Merkle root
  - Variant C: per-document anchor count (N-1) does not match expected leaf count (N) implied by the parent generation event's Merkle root
additional_verifications: []
```

## What this case proves

The bidirectional integrity claim — Merkle root on the parent event AND per-document anchors that recompute to the same root — closes the failure mode where an institution claims a retrieval set on the generation event but doesn't emit the corresponding anchor events (or emits anchor events that don't match the bound root).

## Cross-references

- Spec §10.49 retrieval-source integrity
- Case 041 (parent generation event)
- Case 042 (per-document anchor events)
- Spec §4.2 / §10.37 RFC 6962 Merkle (the substrate)
