# -*- coding: utf-8 -*-
"""Compute the §10.84 communication principal-preapproval ordering fixture
for FFIEC v1 test-vector case 091-communication-preapproval-ordering-anomaly.

§10.84 (FINRA Rule 2210) proves that a registered principal's approval
PRECEDED the send of a retail communication. This case is the NON-conformant
arrangement: the principal's approval (signed_at_utc 14:00) comes AFTER the
send (applied_at_utc 12:00), so a verifier emits the soft-enforcement anomaly
`communication principal-preapproval ordering: approval did not precede send at
seq N` under Status: PASS (the chain still passes integrity — §10.84 is a
completeness check, not a chain-integrity gate).

The fixture shape mirrors case 090 exactly except for the approval timestamp
and the expected verdict. expected_canonical.txt pins the JCS-canonical bytes
of the whole three-event scenario. The pass/anomaly BEHAVIOR is exercised by
the Go verifier unit tests in
verifier/internal/verify/communication_preapproval_test.go.

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

# Approval AFTER send — the ordering violation §10.84 surfaces.
APPROVAL_SIGNED_AT_UTC = "2026-06-01T14:00:00Z"
SEND_APPLIED_AT_UTC = "2026-06-01T12:00:00Z"
SEND_SEQ = 3

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
        "seq": SEND_SEQ,
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
    anomaly_line = (
        "communication principal-preapproval ordering: approval did not "
        f"precede send at seq {SEND_SEQ}"
    )

    fixture = {
        "_about": (
            "Input fixture for case 091-communication-preapproval-ordering-anomaly "
            "— §10.84 FINRA Rule 2210 NON-conformant arrangement. The registered-"
            "principal approval (14:00) comes AFTER the send (12:00); a verifier "
            "emits the ordering anomaly under Status: PASS (soft-enforcement)."
        ),
        "scenario": scenario(),
        "expected": {
            "verdict": "anomaly",
            "anomaly_line": anomaly_line,
            "status": "PASS",
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

    print(f"[091] verdict:            anomaly (approval AFTER send)")
    print(f"[091] approval signed_at: {APPROVAL_SIGNED_AT_UTC}")
    print(f"[091] send applied_at:    {SEND_APPLIED_AT_UTC}")
    print(f"[091] anomaly line:       {anomaly_line}")
    print(f"[091] canonical len:      {len(canonical_bytes)}")
    print(f"[091] canonical SHA-256:  {canonical_sha256}")


if __name__ == "__main__":
    main()
