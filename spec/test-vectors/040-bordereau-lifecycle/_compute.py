# -*- coding: utf-8 -*-
"""Compute the §10.46 bordereau-lifecycle byte form for FFIEC v1
test-vector case 040-bordereau-lifecycle.

§10.46 normates the four-event chain-entry family (`audit.bordereau.published`,
`audit.bordereau.received`, `audit.bordereau.reconciled`, `audit.bordereau.discrepancy_resolved`)
for periodic risk-cession statement integrity. Each event is a chain entry
under §10.2 with attribution. Multiple parties emit events about the same
bordereau; the shared `bordereau_sha256` cross-binds them.

This case pins the byte form for a clean four-event lifecycle:
published → received → reconciled (clean) — three events for the
happy path. The fourth event (`discrepancy_resolved`) is exercised
only in the discrepancy branch; this case does NOT include it.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Synthetic bordereau — Polaris-shape May 2026 cession bordereau.
BORDEREAU_ID = "polaris-bordereau-2026-05"
PERIOD_START_UTC = "2026-05-01T00:00:00Z"
PERIOD_END_UTC = "2026-05-31T23:59:59Z"


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic bordereau document hash. The document itself is retained
# externally; the chain binds the hash.
BORDEREAU_SHA256 = _sha256_of_label(
    "polaris-bordereau-2026-05-canonical-document-as-published"
)


# Synthetic reconciliation report hash.
RECONCILIATION_RECORD_SHA256 = _sha256_of_label(
    "polaris-bordereau-2026-05-reconciliation-report-clean"
)


# Three events forming the clean lifecycle (no discrepancy).
EVENT_PUBLISHED = {
    "audit.bordereau.bordereau_id": BORDEREAU_ID,
    "audit.bordereau.bordereau_sha256": BORDEREAU_SHA256,
    "audit.bordereau.cedent_party_identifier": "cape-madeline-bank-and-trust",
    "audit.bordereau.event_kind": "published",
    "audit.bordereau.period_end_utc": PERIOD_END_UTC,
    "audit.bordereau.period_start_utc": PERIOD_START_UTC,
    "audit.bordereau.published_at_utc": "2026-06-03T09:00:00Z",
}


EVENT_RECEIVED = {
    "audit.bordereau.bordereau_id": BORDEREAU_ID,
    "audit.bordereau.bordereau_sha256": BORDEREAU_SHA256,
    "audit.bordereau.event_kind": "received",
    "audit.bordereau.received_at_utc": "2026-06-03T14:22:00Z",
    "audit.bordereau.receiving_party_identifier": "polaris-reinsurance-bermuda",
}


EVENT_RECONCILED = {
    "audit.bordereau.bordereau_id": BORDEREAU_ID,
    "audit.bordereau.bordereau_sha256": BORDEREAU_SHA256,
    "audit.bordereau.event_kind": "reconciled",
    "audit.bordereau.reconciled_at_utc": "2026-06-08T11:45:00Z",
    "audit.bordereau.reconciliation_outcome": "clean",
    "audit.bordereau.reconciliation_record_sha256": RECONCILIATION_RECORD_SHA256,
    "audit.bordereau.reconciling_party_identifier": "polaris-reinsurance-bermuda",
}


EVENTS = [EVENT_PUBLISHED, EVENT_RECEIVED, EVENT_RECONCILED]


def main() -> None:
    per_event_results = []
    for i, event in enumerate(EVENTS):
        canonical_bytes = jcs.canonicalize(event)
        canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
        per_event_results.append({
            "index": i,
            "event_kind": event["audit.bordereau.event_kind"],
            "canonical_byte_length": len(canonical_bytes),
            "canonical_sha256": canonical_sha256,
        })

    # Lifecycle digest over per-event hashes.
    lifecycle_canonical = jcs.canonicalize([r["canonical_sha256"] for r in per_event_results])
    lifecycle_sha256 = hashlib.sha256(lifecycle_canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 040-bordereau-lifecycle — pins the "
            "§10.46 chain-entry byte form for the clean three-event "
            "lifecycle (published -> received -> reconciled[clean]). The "
            "discrepancy_resolved event is exercised only in the "
            "discrepancy branch and is NOT included here."
        ),
        "bordereau_id": BORDEREAU_ID,
        "events": EVENTS,
        "per_event_results": per_event_results,
        "lifecycle_sha256": lifecycle_sha256,
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Primary pinned form: the published event (event[0]).
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(jcs.canonicalize(EVENT_PUBLISHED))

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for r in per_event_results:
            f.write(f"event[{r['index']}] {r['event_kind']:>10s} {r['canonical_sha256']}\n")
        f.write(f"lifecycle {lifecycle_sha256}\n")

    print(f"[040] bordereau_id:              {BORDEREAU_ID}")
    print(f"[040] bordereau_sha256:          {BORDEREAU_SHA256}")
    for r in per_event_results:
        print(
            f"[040] event[{r['index']}] {r['event_kind']:>10s}  "
            f"len={r['canonical_byte_length']:3d}  sha256={r['canonical_sha256']}"
        )
    print(f"[040] lifecycle SHA-256:         {lifecycle_sha256}")


if __name__ == "__main__":
    main()
