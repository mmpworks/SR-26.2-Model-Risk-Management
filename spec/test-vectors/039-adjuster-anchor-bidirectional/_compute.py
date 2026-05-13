# -*- coding: utf-8 -*-
"""Compute the §10.45 adjuster-anchor bidirectional byte form for FFIEC v1
test-vector case 039-adjuster-anchor-bidirectional.

§10.45 normates `chain.adjuster_anchor` operational events for independent
third-party adjusters whose activity appears on multiple parties' chains
simultaneously. Each affected party emits an anchor event; the events
cross-reference each other via `peer_party_chain_entries`.

This case pins the byte form for both sides of the bidirectional anchor:
the cedent-side entry and the reinsurer-side entry, each referencing
the other's `(run_id, seq)`.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Synthetic adjuster — Marsh Adjusting Services LLC, performing a loss
# investigation that appears on both Cape Madeline (cedent) and Polaris
# (reinsurer) chains.
ADJUSTER_ID = "marsh-adjusters-license-NY-2718281"
ADJUSTER_LEGAL_NAME = "Marsh Adjusting Services LLC"
ADJUSTER_ROLE = "loss_adjuster"
ACTIVITY_UTC = "2026-04-12T13:30:00Z"


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic activity record — the loss-adjuster's signed investigation
# report. The same canonical bytes are hash-anchored on both parties'
# chains; (c) of §10.45's bidirectional verifier dispatch confirms
# this.
ACTIVITY_RECORD_SHA256 = _sha256_of_label(
    "marsh-loss-investigation-report-2026-04-12-claim-12847-canonical"
)


# Synthetic adjuster-side signature over the activity record. The
# scheme is institution-named per CC8.1. This case uses a deterministic
# placeholder — the base64-encoded form of (SHA-256("039-marsh-...sig")
# || SHA-256("039-marsh-2")), a strict-base64 88-char form ending with
# two `=` (RFC 4648 §4 representation of a 64-byte signature).
ACTIVITY_RECORD_SIGNATURE_B64 = (
    "MK1H131ssOk/2JK9Ui6S+AJPAn3xovMh8CgMD/r5cNR8"
    "TM9zn0viFhCXgcRcexdL6arrZbwmZiFghAdA0GCbwg=="
)


# Cedent-side anchor: Cape Madeline's chain entry. References the
# reinsurer's (Polaris's) entry via peer_party_chain_entries.
CEDENT_ANCHOR = {
    "audit.adjuster_anchor.activity_record_sha256": ACTIVITY_RECORD_SHA256,
    "audit.adjuster_anchor.activity_record_signature_b64": ACTIVITY_RECORD_SIGNATURE_B64,
    "audit.adjuster_anchor.activity_utc": ACTIVITY_UTC,
    "audit.adjuster_anchor.adjuster_id": ADJUSTER_ID,
    "audit.adjuster_anchor.adjuster_legal_name": ADJUSTER_LEGAL_NAME,
    "audit.adjuster_anchor.adjuster_role": ADJUSTER_ROLE,
    "audit.adjuster_anchor.peer_party_chain_entries": [
        {
            "party_identifier": "polaris-reinsurance-bermuda",
            "party_role": "reinsurer",
            "peer_run_id": "polaris-cession-claim-2026-04-payment-loss-12847",
            "peer_seq": 4,
        },
    ],
}


# Reinsurer-side anchor: Polaris's chain entry. References the cedent's
# (Cape Madeline's) entry. The activity_record_sha256 MUST match.
REINSURER_ANCHOR = {
    "audit.adjuster_anchor.activity_record_sha256": ACTIVITY_RECORD_SHA256,
    "audit.adjuster_anchor.activity_record_signature_b64": ACTIVITY_RECORD_SIGNATURE_B64,
    "audit.adjuster_anchor.activity_utc": ACTIVITY_UTC,
    "audit.adjuster_anchor.adjuster_id": ADJUSTER_ID,
    "audit.adjuster_anchor.adjuster_legal_name": ADJUSTER_LEGAL_NAME,
    "audit.adjuster_anchor.adjuster_role": ADJUSTER_ROLE,
    "audit.adjuster_anchor.peer_party_chain_entries": [
        {
            "party_identifier": "cape-madeline-bank-and-trust",
            "party_role": "cedent",
            "peer_run_id": "cape-madeline-claim-12847",
            "peer_seq": 8,
        },
    ],
}


def main() -> None:
    cedent_canonical = jcs.canonicalize(CEDENT_ANCHOR)
    cedent_sha256 = hashlib.sha256(cedent_canonical).hexdigest()

    reinsurer_canonical = jcs.canonicalize(REINSURER_ANCHOR)
    reinsurer_sha256 = hashlib.sha256(reinsurer_canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 039-adjuster-anchor-bidirectional — "
            "pins the §10.45 chain-entry byte form for both sides of a "
            "bidirectional adjuster anchor. The cedent-side and reinsurer-"
            "side entries share activity_record_sha256 (verifier check c) "
            "and cross-reference each other via peer_party_chain_entries "
            "(verifier check b)."
        ),
        "cedent_anchor": CEDENT_ANCHOR,
        "reinsurer_anchor": REINSURER_ANCHOR,
        "expected": {
            "cedent_canonical_byte_length": len(cedent_canonical),
            "cedent_sha256": cedent_sha256,
            "reinsurer_canonical_byte_length": len(reinsurer_canonical),
            "reinsurer_sha256": reinsurer_sha256,
            "shared_activity_record_sha256": ACTIVITY_RECORD_SHA256,
        },
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # The primary pinned form is the cedent-side anchor; the reinsurer-
    # side anchor is in the second file.
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(cedent_canonical)

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"cedent_anchor {cedent_sha256}\n")
        f.write(f"reinsurer_anchor {reinsurer_sha256}\n")
        f.write(f"shared_activity_record {ACTIVITY_RECORD_SHA256}\n")

    with open(os.path.join(HERE, "expected_reinsurer_canonical.txt"), "wb") as f:
        f.write(reinsurer_canonical)

    print(f"[039] adjuster id:               {ADJUSTER_ID}")
    print(f"[039] activity record sha256:    {ACTIVITY_RECORD_SHA256}")
    print(f"[039] cedent canonical len:      {len(cedent_canonical)}")
    print(f"[039] cedent sha256:             {cedent_sha256}")
    print(f"[039] reinsurer canonical len:   {len(reinsurer_canonical)}")
    print(f"[039] reinsurer sha256:          {reinsurer_sha256}")


if __name__ == "__main__":
    main()
