# -*- coding: utf-8 -*-
"""Compute the GAP-5 HITL signed-review-event byte form for FFIEC v1
test-vector case 044-human-review-primitive.

GAP-5 normates a minimal shared signed-review-event primitive consumed
by §10.50 (output-grounding output review) and §10.55 (audit-target
challenge-response). The primitive is intentionally domain-agnostic —
it provides:

- A signed-review-event chain-entry schema (reviewer_id, reviewer_role,
  signed_at_utc, signature_b64, signed-canonical-bytes-of-review-payload,
  parent_run_id, parent_seq).
- Per-reviewer key-registry validation (reviewer_id resolves to a public
  key whose fingerprint matches the canonical-bytes binding).
- Cross-binding helpers (parent_run_id / parent_seq construction).

Per-domain semantics — clinical edit outcomes, challenge disposition
outcomes, etc. — stay per-section.

This case pins the canonical bytes for the GAP-5 signed-review-event
*standalone*, isolated from §10.50 wrapping. Composes with case 043
(§10.50 review event) which embeds this byte form.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic clinician reviewer.
REVIEWER_ID = "lyceum-clinician-reviewer-key-id-cardiology-2026-04"
REVIEWER_ROLE = "attending_physician"
SIGNED_AT_UTC = "2026-04-12T11:00:00Z"

# Synthetic reviewer key fingerprint (SHA-256 of a deterministic public-key
# byte-string seed). The fingerprint binds the signing-key identity to
# the chain entry; the institution's CC8.1 names the reviewer-key
# registry that resolves the reviewer_id to this fingerprint.
REVIEWER_PUBLIC_KEY_FINGERPRINT = _sha256_of_label(
    "lyceum-clinician-reviewer-pubkey-cardiology-2026-04"
)


# The review payload — the canonical bytes the reviewer signs over.
# In §10.50 use, this is the canonical bytes of the review event
# (excluding the signature itself). For the standalone primitive vector,
# we use a minimal payload that exercises the schema without invoking
# §10.50 attribute names.
REVIEW_PAYLOAD = {
    "outcome": "approved",
    "rationale_hash": _sha256_of_label("synthetic-review-rationale-text-canonical"),
    "reviewed_at_utc": SIGNED_AT_UTC,
    "subject_run_id": "subject-event-run-id-12847",
    "subject_seq": 1,
}


# Synthetic 64-byte signature placeholder. Same recipe as vector 039
# (deterministic SHA-256 chain seeded by a label, base64-encoded).
import base64

_SIGNATURE_BYTES = (
    hashlib.sha256(b"044-hitl-clinician-signature-part-1").digest()
    + hashlib.sha256(b"044-hitl-clinician-signature-part-2").digest()
)
SIGNATURE_B64 = base64.b64encode(_SIGNATURE_BYTES).decode("ascii")


def build_signed_review_event() -> dict:
    """GAP-5 signed-review-event byte form.

    Six fields. The `signed_payload_sha256` is the SHA-256 of the
    JCS-canonical bytes of the review payload — this is what the
    reviewer signs over. The signature itself binds to that hash,
    so a verifier with the reviewer's public key can verify the
    signature against the canonical bytes of the review payload.
    """
    review_payload_canonical = jcs.canonicalize(REVIEW_PAYLOAD)
    signed_payload_sha256 = hashlib.sha256(review_payload_canonical).hexdigest()
    return {
        "audit.signed_review.reviewer_id": REVIEWER_ID,
        "audit.signed_review.reviewer_public_key_fingerprint": REVIEWER_PUBLIC_KEY_FINGERPRINT,
        "audit.signed_review.reviewer_role": REVIEWER_ROLE,
        "audit.signed_review.signature_b64": SIGNATURE_B64,
        "audit.signed_review.signed_at_utc": SIGNED_AT_UTC,
        "audit.signed_review.signed_payload_sha256": signed_payload_sha256,
    }


def main() -> None:
    event = build_signed_review_event()
    canonical_bytes = jcs.canonicalize(event)
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    review_payload_canonical = jcs.canonicalize(REVIEW_PAYLOAD)
    signed_payload_sha256 = hashlib.sha256(review_payload_canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 044-human-review-primitive — pins "
            "the GAP-5 signed-review-event byte form standalone. "
            "Composes with case 043 (§10.50 review event) which embeds "
            "this byte form via audit.review.signed_review."
        ),
        "review_payload": REVIEW_PAYLOAD,
        "signed_review_event": event,
        "signed_payload_canonical_bytes_sha256": signed_payload_sha256,
        "expected": {
            "canonical_byte_length": len(canonical_bytes),
            "canonical_sha256": canonical_sha256,
        },
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(canonical_bytes)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(canonical_sha256 + "\n")

    print(f"[044] reviewer_id:               {REVIEWER_ID}")
    print(f"[044] reviewer_role:             {REVIEWER_ROLE}")
    print(f"[044] signed_payload_sha256:     {signed_payload_sha256}")
    print(f"[044] canonical len:             {len(canonical_bytes)}")
    print(f"[044] canonical SHA-256:         {canonical_sha256}")


if __name__ == "__main__":
    main()
