# -*- coding: utf-8 -*-
"""Compute the §10.49 retrieval-set Merkle root + per-document anchor
event byte form for FFIEC v1 test-vector case 042-retrieval-set-merkle.

§10.49 normates two integrity surfaces: a retrieval-set Merkle root
bound on the parent §10.47 generation event, AND per-document anchor
events emitted as separate chain entries with PMID/DOI cross-anchors.

This case pins:
  (a) the four per-document anchor events' canonical bytes (one per
      retrieved document);
  (b) the retrieval-set Merkle root computed under canonical RFC 6962
      over the four per-document SHA-256 leaves.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Synthetic clinical retrieval scenario — a Lyceum-shape RAG inference
# retrieves four PubMed articles for a clinical-decision-support query
# about post-MI statin therapy.
PARENT_RUN_ID = "lyceum-medsynth-2026-04-12-clinical-query-12847"
RETRIEVED_AT_UTC = "2026-04-12T10:30:00Z"


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Four retrieved documents. Each carries a PMID (canonical PubMed
# identifier), a deterministic content hash, a relevance score, and
# the retrieved_at_utc timestamp (same across all four — one batch).
RETRIEVED_DOCUMENTS = [
    {
        "pmid": "38420190",
        "content_label": "post-mi-statin-therapy-guidelines-2024",
        "relevance_score": 0.92,
    },
    {
        "pmid": "37123456",
        "content_label": "high-intensity-statin-secondary-prevention",
        "relevance_score": 0.87,
    },
    {
        "pmid": "39001234",
        "content_label": "lipid-management-acs-2026-update",
        "relevance_score": 0.81,
    },
    {
        "pmid": "37890123",
        "content_label": "statin-intolerance-alternative-strategies",
        "relevance_score": 0.65,
    },
]


# RFC 6962 §2.1 hash-domain separators (§4.2 / §10.37 substrate).
_LEAF_PREFIX = b"\x00"
_INTERNAL_PREFIX = b"\x01"


def _leaf_hash(payload_bytes: bytes) -> bytes:
    return hashlib.sha256(_LEAF_PREFIX + payload_bytes).digest()


def _inner_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(_INTERNAL_PREFIX + left + right).digest()


def _largest_power_of_2_less_than(n: int) -> int:
    if n <= 1:
        raise ValueError(f"_largest_power_of_2_less_than requires n > 1; got {n}")
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def _merkle_root(payloads: list[bytes]) -> bytes:
    """Canonical RFC 6962 tree hash — same construction as §4.2."""
    n = len(payloads)
    if n == 0:
        return hashlib.sha256(b"").digest()
    if n == 1:
        return _leaf_hash(payloads[0])
    k = _largest_power_of_2_less_than(n)
    left = _merkle_root(payloads[:k])
    right = _merkle_root(payloads[k:])
    return _inner_hash(left, right)


def build_anchor_event(doc: dict, parent_seq: int) -> dict:
    """Build the §10.49 audit.retrieval.document_anchor.* event payload.

    The event is one chain entry per retrieved document, cross-bound to
    the parent §10.47 generation event via parent_run_id / parent_seq.
    """
    document_sha256 = _sha256_of_label(doc["content_label"])
    return {
        "audit.retrieval.document_anchor.canonical_identifier_kind": "pmid",
        "audit.retrieval.document_anchor.canonical_identifier_value": doc["pmid"],
        "audit.retrieval.document_anchor.document_sha256": document_sha256,
        "audit.retrieval.document_anchor.parent_run_id": PARENT_RUN_ID,
        "audit.retrieval.document_anchor.parent_seq": parent_seq,
        "audit.retrieval.document_anchor.retrieval_relevance_score": doc["relevance_score"],
        "audit.retrieval.document_anchor.retrieved_at_utc": RETRIEVED_AT_UTC,
    }


def main() -> None:
    # Anchor events are emitted in the order documents appear in the
    # retrieval set (the institution's CC8.1-named ordering — here:
    # by relevance score descending, the Lyceum default).
    parent_seq_base = 1  # parent_seq is 1-indexed per §4.4 first-entry convention
    anchor_events = []
    document_canonical_byte_payloads = []
    per_event_results = []

    for idx, doc in enumerate(RETRIEVED_DOCUMENTS):
        # parent_seq is the seq of the §10.47 generation event being
        # cross-bound. We use a fixed value (the synthetic generation
        # event lives at seq=1 in this test scenario).
        anchor = build_anchor_event(doc, parent_seq=parent_seq_base)
        anchor_events.append(anchor)
        canonical = jcs.canonicalize(anchor)
        sha256 = hashlib.sha256(canonical).hexdigest()
        per_event_results.append({
            "index": idx,
            "pmid": doc["pmid"],
            "content_label": doc["content_label"],
            "document_sha256": _sha256_of_label(doc["content_label"]),
            "canonical_byte_length": len(canonical),
            "canonical_sha256": sha256,
        })
        # The Merkle leaf payload is the document's SHA-256 bytes (the
        # hash itself, in raw byte form), NOT the anchor-event canonical
        # bytes. The leaf is what's bound to the parent generation event.
        # Note: we use the binary form of the SHA-256, not the hex string.
        document_sha256_bytes = bytes.fromhex(_sha256_of_label(doc["content_label"]))
        document_canonical_byte_payloads.append(document_sha256_bytes)

    # Compute the retrieval-set Merkle root over the document SHA-256 leaves.
    retrieval_set_merkle_root = _merkle_root(document_canonical_byte_payloads)
    retrieval_set_merkle_root_hex = retrieval_set_merkle_root.hex()

    fixture = {
        "_about": (
            "Input fixture for case 042-retrieval-set-merkle — pins the "
            "§10.49 chain-entry byte form for four per-document anchor "
            "events plus the Merkle root over their document_sha256 "
            "leaves under canonical RFC 6962. Composes with case 041 "
            "(generation four-tuple): the Merkle root pinned here "
            "appears as audit.generation.retrieval_set_merkle_root_sha256 "
            "on case 041's parent event."
        ),
        "parent_run_id": PARENT_RUN_ID,
        "retrieved_at_utc": RETRIEVED_AT_UTC,
        "retrieved_documents": RETRIEVED_DOCUMENTS,
        "anchor_events": anchor_events,
        "per_event_results": per_event_results,
        "retrieval_set_merkle_root_hex": retrieval_set_merkle_root_hex,
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Primary pinned form: the first anchor event (the highest-relevance retrieval).
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(jcs.canonicalize(anchor_events[0]))

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for r in per_event_results:
            f.write(f"anchor[{r['index']}] pmid={r['pmid']:>10s} {r['canonical_sha256']}\n")
        f.write(f"retrieval_set_merkle_root {retrieval_set_merkle_root_hex}\n")

    with open(
        os.path.join(HERE, "expected_retrieval_set_merkle_root.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(retrieval_set_merkle_root_hex + "\n")

    print(f"[042] parent_run_id:             {PARENT_RUN_ID}")
    print(f"[042] retrieved documents:       {len(RETRIEVED_DOCUMENTS)}")
    for r in per_event_results:
        print(
            f"[042] anchor[{r['index']}] pmid={r['pmid']:>10s} "
            f"len={r['canonical_byte_length']:3d}  sha256={r['canonical_sha256'][:16]}..."
        )
    print(f"[042] retrieval_set Merkle root: {retrieval_set_merkle_root_hex}")


if __name__ == "__main__":
    main()
