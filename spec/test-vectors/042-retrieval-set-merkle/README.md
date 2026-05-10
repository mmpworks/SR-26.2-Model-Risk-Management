# Case 042 — Retrieval-set Merkle root + per-document anchors (§10.49)

## What this case verifies

Spec §10.49 normates the retrieval-set Merkle root (bound on §10.47 generation event) AND per-document anchor events (cross-bound to the parent generation event). This case pins both surfaces for a Lyceum-shape RAG inference retrieving four PubMed articles.

## Inputs

Four retrieved documents, each carrying a PMID canonical identifier, deterministic content hash, and relevance score:

| PMID | Content label | Relevance |
|---|---|---|
| 38420190 | post-mi-statin-therapy-guidelines-2024 | 0.92 |
| 37123456 | high-intensity-statin-secondary-prevention | 0.87 |
| 39001234 | lipid-management-acs-2026-update | 0.81 |
| 37890123 | statin-intolerance-alternative-strategies | 0.65 |

All four anchor events share `parent_run_id = lyceum-medsynth-2026-04-12-clinical-query-12847`, `parent_seq = 1`, and `retrieved_at_utc = 2026-04-12T10:30:00Z`.

## Expected canonical bytes

| Anchor | PMID | Canonical bytes | SHA-256 |
|---|---|---|---|
| anchor[0] | 38420190 | 541 | `2f161466d3ba5cae...` |
| anchor[1] | 37123456 | 541 | `64103d0bc77c286c...` |
| anchor[2] | 39001234 | 541 | `9ce8bdd6646aa3a5...` |
| anchor[3] | 37890123 | 541 | `580ce887cfce1ada...` |

Full hex digests in `expected_canonical_sha256.txt`. The retrieval-set Merkle root over the four document_sha256 byte payloads (under canonical RFC 6962): `2aefda83d3521600b0b408d2c3d66e0e7d6e962490703774084f57323874a148`. This is the value bound on case 041's generation event.

## Conformance behavior

A conforming implementation:

1. Builds each anchor event with the §10.49 attribute schema (7 fields per event).
2. Canonicalizes per RFC 8785 (JCS); produces bytes byte-identical to the per-event hashes.
3. Computes the retrieval-set Merkle root via canonical RFC 6962 over the document_sha256 byte payloads (NOT the anchor-event canonical bytes — the leaves are the document content hashes).
4. Cross-binds each anchor to the parent §10.47 generation event via `parent_run_id` / `parent_seq`.

## Cross-references

- Spec §10.49 retrieval-source integrity
- Spec §10.31 cohort subtree disclosure (Merkle root composes for selective audit)
- Spec §10.40 cross-vendor cross-anchor (canonical_identifier_kind sibling pattern)
- Spec §4.2 / §10.37 RFC 6962 Merkle (the substrate)
- Case 041 (the generation event binding the Merkle root)

## Reproduction

```
python _compute.py
```
