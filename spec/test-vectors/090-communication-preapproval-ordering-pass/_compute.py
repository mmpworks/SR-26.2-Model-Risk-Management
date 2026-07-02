# -*- coding: utf-8 -*-
"""Compute the §10.84 communication principal-preapproval ordering fixture
for FFIEC v1 test-vector case 090-communication-preapproval-ordering-pass.

§10.84 (FINRA Rule 2210) proves that a registered principal's approval
PRECEDED the send of a retail communication. This case is the conformant
arrangement: the principal's approval (signed_at_utc 10:00) precedes the
send (applied_at_utc 12:00), so a verifier emits the marker
`communication_principal_preapproval_verified`.

The fixture composes three existing event shapes — no new cryptographic
mechanism:
  - a communication event carrying audit.communication.audience = "retail";
  - a §10.50 review event with audit.review.role = "registered_principal"
    (flat dotted keys), whose signed_review.signed_at_utc is the approval;
  - a §14.8 downstream_action event (nested object) with action_kind
    "communication_sent" and §4.4 top-level parent linkage, whose
    applied_at_utc is the send.

expected_canonical.txt pins the JCS-canonical bytes of the whole
three-event scenario so two implementations reconstruct byte-identical
§10.84 arrangements. The pass/anomaly BEHAVIOR is exercised by the Go
verifier unit tests in verifier/internal/verify/communication_preapproval_test.go.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))

COMMUNICATION_RUN_ID = "anchorline-2026-q2-retail-market-commentary"
COMMUNICATION_SEQ = 1

APPROVAL_SIGNED_AT_UTC = "2026-06-01T10:00:00Z"
SEND_APPLIED_AT_UTC = "2026-06-01T12:00:00Z"

CHANGE_RECORD_ID_HASH = hashlib.sha256(
    b"anchorline-retail-commentary-send-change-record"
).hexdigest()


def communication_event() -> dict:
    return {
        "run_id": COMMUNICATION_RUN_ID,
        "seq": COMMUNICATION_SEQ,
        "audit.communication.audience": "retail",
    }


def principal_approval_event() -> dict:
    return {
        "run_id": "anchorline-principal-approval-2026-q2-commentary",
        "seq": 2,
        "audit.review.outcome": "approved",
        "audit.review.role": "registered_principal",
        "audit.review.parent_run_id": COMMUNICATION_RUN_ID,
        "audit.review.parent_seq": COMMUNICATION_SEQ,
        "audit.review.signed_review": {
            "audit.signed_review.signed_at_utc": APPROVAL_SIGNED_AT_UTC,
        },
    }


def send_event() -> dict:
    return {
        "run_id": "anchorline-send-2026-q2-commentary",
        "seq": 3,
        "parent_run_id": COMMUNICATION_RUN_ID,
        "parent_seq": COMMUNICATION_SEQ,
        "audit.downstream_action": {
            "action_kind": "communication_sent",
            "system_of_record_id": "comms-platform",
            "change_record_id_hash": CHANGE_RECORD_ID_HASH,
            "applied_at_utc": SEND_APPLIED_AT_UTC,
        },
    }


def scenario() -> dict:
    return {
        "communication": communication_event(),
        "principal_approval": principal_approval_event(),
        "send": send_event(),
    }


def main() -> None:
    canonical_bytes = jcs.canonicalize(scenario())
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 090-communication-preapproval-ordering-pass "
            "— §10.84 FINRA Rule 2210 conformant arrangement. The registered-"
            "principal approval (10:00) precedes the send (12:00); a verifier "
            "emits communication_principal_preapproval_verified."
        ),
        "scenario": scenario(),
        "expected": {
            "verdict": "marker",
            "marker": "communication_principal_preapproval_verified",
            "approval_signed_at_utc": APPROVAL_SIGNED_AT_UTC,
            "send_applied_at_utc": SEND_APPLIED_AT_UTC,
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

    print(f"[090] verdict:            marker (approval precedes send)")
    print(f"[090] approval signed_at: {APPROVAL_SIGNED_AT_UTC}")
    print(f"[090] send applied_at:    {SEND_APPLIED_AT_UTC}")
    print(f"[090] canonical len:      {len(canonical_bytes)}")
    print(f"[090] canonical SHA-256:  {canonical_sha256}")


if __name__ == "__main__":
    main()
