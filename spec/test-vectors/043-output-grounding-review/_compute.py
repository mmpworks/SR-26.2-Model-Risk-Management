# -*- coding: utf-8 -*-
"""Compute the §10.50 output-grounding review event byte form for FFIEC
v1 test-vector case 043-output-grounding-review.

§10.50 normates the output-review event family composing GAP-2 state-
machine (pending_review → reviewed[outcome]) with GAP-5 HITL primitive
(signed-review-event embedded as audit.review.signed_review). This case
pins a `grounding_pass` outcome — a clinician confirmed the AI output
is grounded in the retrieval set.

Cross-binds to case 041 (the §10.47 generation event being reviewed)
via parent_run_id / parent_seq, and embeds case 044's signed-review-event
byte form via audit.review.signed_review.

Run with: python _compute.py
"""

from __future__ import annotations

import base64
import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Cross-binding to case 041's parent generation event.
PARENT_RUN_ID = "lyceum-medsynth-2026-04-12-clinical-query-12847"
PARENT_SEQ = 1

# Review outcome: clinician approved the synthesis (grounding_pass).
OUTCOME = "grounding_pass"
REVIEW_RATIONALE_HASH = _sha256_of_label(
    "lyceum-clinician-rationale-statin-synthesis-grounded-in-retrieval-set"
)

# GAP-5 signed-review-event embedded inside audit.review.signed_review.
# Same shape as case 044, with Lyceum-specific reviewer + signature.
REVIEWER_ID = "lyceum-clinician-reviewer-key-id-cardiology-2026-04"
REVIEWER_ROLE = "attending_physician"
SIGNED_AT_UTC = "2026-04-12T11:00:00Z"
REVIEWER_PUBLIC_KEY_FINGERPRINT = _sha256_of_label(
    "lyceum-clinician-reviewer-pubkey-cardiology-2026-04"
)

# The signed payload — the canonical bytes of the §10.50 review-event
# attributes (excluding the signed_review object itself). The reviewer
# signs over this hash; a verifier with the reviewer's public key
# verifies the signature against this canonical-bytes form.
SIGNED_PAYLOAD = {
    "audit.review.outcome": OUTCOME,
    "audit.review.parent_run_id": PARENT_RUN_ID,
    "audit.review.parent_seq": PARENT_SEQ,
    "audit.review.review_rationale_hash": REVIEW_RATIONALE_HASH,
}

_SIGNATURE_BYTES = (
    hashlib.sha256(b"043-grounding-pass-signature-part-1").digest()
    + hashlib.sha256(b"043-grounding-pass-signature-part-2").digest()
)
SIGNATURE_B64 = base64.b64encode(_SIGNATURE_BYTES).decode("ascii")


def build_signed_review_object() -> dict:
    """GAP-5 signed-review-event embedded inside audit.review.signed_review."""
    signed_payload_canonical = jcs.canonicalize(SIGNED_PAYLOAD)
    signed_payload_sha256 = hashlib.sha256(signed_payload_canonical).hexdigest()
    return {
        "audit.signed_review.reviewer_id": REVIEWER_ID,
        "audit.signed_review.reviewer_public_key_fingerprint": REVIEWER_PUBLIC_KEY_FINGERPRINT,
        "audit.signed_review.reviewer_role": REVIEWER_ROLE,
        "audit.signed_review.signature_b64": SIGNATURE_B64,
        "audit.signed_review.signed_at_utc": SIGNED_AT_UTC,
        "audit.signed_review.signed_payload_sha256": signed_payload_sha256,
    }


def build_review_event() -> dict:
    """§10.50 review event composing GAP-2 state-machine with GAP-5 HITL."""
    signed_review = build_signed_review_object()
    return {
        "audit.review.outcome": OUTCOME,
        "audit.review.parent_run_id": PARENT_RUN_ID,
        "audit.review.parent_seq": PARENT_SEQ,
        "audit.review.review_rationale_hash": REVIEW_RATIONALE_HASH,
        "audit.review.signed_review": signed_review,
    }


def main() -> None:
    event = build_review_event()
    canonical_bytes = jcs.canonicalize(event)
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 043-output-grounding-review — pins "
            "the §10.50 review event byte form for a Lyceum clinician's "
            "grounding_pass review of a §10.47 generation event. Cross-"
            "binds to case 041 via parent_run_id/parent_seq; embeds the "
            "GAP-5 signed-review-event per case 044's primitive shape."
        ),
        "review_event": event,
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

    print(f"[043] outcome:                   {OUTCOME}")
    print(f"[043] parent_run_id:             {PARENT_RUN_ID}")
    print(f"[043] reviewer_id:               {REVIEWER_ID}")
    print(f"[043] canonical len:             {len(canonical_bytes)}")
    print(f"[043] canonical SHA-256:         {canonical_sha256}")


if __name__ == "__main__":
    main()
