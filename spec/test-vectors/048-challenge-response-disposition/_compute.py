# -*- coding: utf-8 -*-
"""Compute the §10.55 challenge-response disposition byte form for FFIEC
v1 test-vector case 048-challenge-response-disposition.

§10.55 normates the challenge-response event family composing GAP-2
state-machine (filed → triaged → disposed; or filed → disposed when
triage is operationally skipped) with GAP-5 HITL primitive (signed
disposition). This case pins an `overturned` outcome — a Helvetian
taxpayer challenged an AI-flagged audit and the agency reversed the
decision after administrative-law-judge review.

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


# Helvetian-shape taxpayer challenge to a VAT audit-target selection.
ORIGINAL_DECISION_RUN_ID = "helvetian-vat-audit-target-2026-04-12-taxpayer-CH184729"
ORIGINAL_DECISION_SEQ = 1
OUTCOME = "overturned"
RATIONALE_HASH = _sha256_of_label(
    "helvetian-alj-disposition-rationale-2026-05-overturned-prior-coverage-error"
)

# GAP-5 signed-disposition by an administrative-law judge.
REVIEWER_ID = "helvetian-administrative-law-judge-key-id-CH-2026"
REVIEWER_ROLE = "administrative_law_judge"
SIGNED_AT_UTC = "2026-05-20T14:00:00Z"
REVIEWER_PUBLIC_KEY_FINGERPRINT = _sha256_of_label(
    "helvetian-alj-pubkey-CH-2026-cohort-cardiac"
)

# Signed-payload — the canonical bytes of the §10.55 disposition fields
# (excluding the signed_disposition object itself). The reviewer signs
# over this hash.
SIGNED_PAYLOAD = {
    "audit.challenge_response.original_decision_run_id": ORIGINAL_DECISION_RUN_ID,
    "audit.challenge_response.original_decision_seq": ORIGINAL_DECISION_SEQ,
    "audit.challenge_response.outcome": OUTCOME,
    "audit.challenge_response.rationale_hash": RATIONALE_HASH,
}

_SIGNATURE_BYTES = (
    hashlib.sha256(b"048-helvetian-alj-disposition-signature-part-1").digest()
    + hashlib.sha256(b"048-helvetian-alj-disposition-signature-part-2").digest()
)
SIGNATURE_B64 = base64.b64encode(_SIGNATURE_BYTES).decode("ascii")


def build_signed_disposition() -> dict:
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


def build_challenge_response() -> dict:
    """§10.55 challenge-response chain entry composing GAP-2 + GAP-5."""
    return {
        "audit.challenge_response.original_decision_run_id": ORIGINAL_DECISION_RUN_ID,
        "audit.challenge_response.original_decision_seq": ORIGINAL_DECISION_SEQ,
        "audit.challenge_response.outcome": OUTCOME,
        "audit.challenge_response.rationale_hash": RATIONALE_HASH,
        "audit.challenge_response.signed_disposition": build_signed_disposition(),
    }


def main() -> None:
    event = build_challenge_response()
    canonical = jcs.canonicalize(event)
    sha256 = hashlib.sha256(canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 048-challenge-response-disposition "
            "— pins the §10.55 chain-entry byte form for a Helvetian "
            "taxpayer challenge dispositioned 'overturned' by an "
            "administrative-law judge under GAP-5 HITL signature."
        ),
        "challenge_response": event,
        "expected": {
            "canonical_byte_length": len(canonical),
            "canonical_sha256": sha256,
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(canonical)
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w", encoding="utf-8", newline="\n",
    ) as f:
        f.write(sha256 + "\n")

    print(f"[048] outcome:                   {OUTCOME}")
    print(f"[048] original_decision_run_id:  {ORIGINAL_DECISION_RUN_ID}")
    print(f"[048] reviewer_id:               {REVIEWER_ID}")
    print(f"[048] canonical len:             {len(canonical)}")
    print(f"[048] canonical SHA-256:         {sha256}")


if __name__ == "__main__":
    main()
