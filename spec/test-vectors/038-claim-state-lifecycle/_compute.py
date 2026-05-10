# -*- coding: utf-8 -*-
"""Compute the §10.43 claim-state-machine chain-entry byte form for FFIEC v1
test-vector case 038-claim-state-lifecycle.

§10.43 normates `chain.claim_state.transition` operational events for
chain-of-custody-bound insurance claims. Each transition carries the
high-level lifecycle state (closed enum), institution-named substates,
actor, rationale, authorizing-policy reference, and timestamp.

This case pins the JCS-canonical bytes for a Polaris/Lloyd's-shape
6-transition lifecycle: FNOL → reserve-set → adjudication → paid →
recovery → closed.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Synthetic claim — Polaris reinsurance cession, Cape Madeline cedent.
CLAIM_RUN_ID = "polaris-cession-claim-2026-04-payment-loss-12847"
TENANT_ID = "polaris-reinsurance-bermuda"


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Synthetic authorizing-policy document hashes.
POLICY_INTAKE_SHA256 = _sha256_of_label("polaris-claim-handling-manual-v3.2-section-4-intake")
POLICY_RESERVE_SHA256 = _sha256_of_label("polaris-reserve-setting-policy-v2.1")
POLICY_ADJUDICATION_SHA256 = _sha256_of_label("polaris-adjudication-committee-charter-v4.0")
POLICY_PAYMENT_SHA256 = _sha256_of_label("polaris-payment-authority-delegation-matrix-v1.5")
POLICY_RECOVERY_SHA256 = _sha256_of_label("polaris-subrogation-recovery-policy-v2.0")
POLICY_CLOSE_SHA256 = _sha256_of_label("polaris-claim-closure-procedure-v1.3")


# 6-event lifecycle. Each event is a `chain.claim_state.transition`
# operational event under §10.2; the byte form pinned here is the
# operational-event payload (the attribute family that lives on the
# chain entry).
TRANSITIONS = [
    {
        "audit.claim_state.actor": "polaris-intake-bot-v3",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-intake-v3.2",
        "audit.claim_state.authorizing_policy_sha256": POLICY_INTAKE_SHA256,
        "audit.claim_state.from": "opened",
        "audit.claim_state.from_substate": "fnol_received",
        "audit.claim_state.rationale": (
            "FNOL processed through automated intake; preliminary "
            "coverage check passed; routing to reserve-setting."
        ),
        "audit.claim_state.to": "opened",
        "audit.claim_state.to_substate": "reserve_set_initial",
        "audit.claim_state.transition_utc": "2026-04-02T09:14:33Z",
    },
    {
        "audit.claim_state.actor": "claim-handler-id-7392",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-reserve-v2.1",
        "audit.claim_state.authorizing_policy_sha256": POLICY_RESERVE_SHA256,
        "audit.claim_state.from": "opened",
        "audit.claim_state.from_substate": "reserve_set_initial",
        "audit.claim_state.rationale": (
            "Initial reserve set per §4.2 of the reserve-setting policy "
            "based on loss-bordereau projection. Routing to adjudication."
        ),
        "audit.claim_state.to": "pending",
        "audit.claim_state.to_substate": "adjudication_committee_review",
        "audit.claim_state.transition_utc": "2026-04-08T14:22:11Z",
    },
    {
        "audit.claim_state.actor": "adjudication-committee-id-2026-Q2-N4",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-adjudication-v4.0",
        "audit.claim_state.authorizing_policy_sha256": POLICY_ADJUDICATION_SHA256,
        "audit.claim_state.from": "pending",
        "audit.claim_state.from_substate": "adjudication_committee_review",
        "audit.claim_state.rationale": (
            "Adjudication committee approved cession at full reserve "
            "amount per §3 of charter. Cession-payment authorized."
        ),
        "audit.claim_state.to": "decided",
        "audit.claim_state.to_substate": "cession_payment_authorized",
        "audit.claim_state.transition_utc": "2026-04-15T11:00:00Z",
    },
    {
        "audit.claim_state.actor": "payment-officer-id-1184",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-payment-v1.5",
        "audit.claim_state.authorizing_policy_sha256": POLICY_PAYMENT_SHA256,
        "audit.claim_state.from": "decided",
        "audit.claim_state.from_substate": "cession_payment_authorized",
        "audit.claim_state.rationale": (
            "Payment executed via SWIFT to cedent's bordereau-recorded "
            "settlement account. Initiating subrogation review."
        ),
        "audit.claim_state.to": "decided",
        "audit.claim_state.to_substate": "recovery_subrogation_review",
        "audit.claim_state.transition_utc": "2026-04-22T15:45:08Z",
    },
    {
        "audit.claim_state.actor": "recovery-officer-id-3217",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-recovery-v2.0",
        "audit.claim_state.authorizing_policy_sha256": POLICY_RECOVERY_SHA256,
        "audit.claim_state.from": "decided",
        "audit.claim_state.from_substate": "recovery_subrogation_review",
        "audit.claim_state.rationale": (
            "Subrogation review complete; no recoverable third-party "
            "obligation identified. Routing to closure."
        ),
        "audit.claim_state.to": "decided",
        "audit.claim_state.to_substate": "recovery_complete_no_recovery",
        "audit.claim_state.transition_utc": "2026-05-01T10:30:00Z",
    },
    {
        "audit.claim_state.actor": "claim-handler-id-7392",
        "audit.claim_state.authorizing_policy_id": "polaris-policy-closure-v1.3",
        "audit.claim_state.authorizing_policy_sha256": POLICY_CLOSE_SHA256,
        "audit.claim_state.bordereau_id": "polaris-bordereau-2026-05",
        "audit.claim_state.from": "decided",
        "audit.claim_state.from_substate": "recovery_complete_no_recovery",
        "audit.claim_state.rationale": (
            "Claim closed; recorded in May 2026 bordereau under cession-"
            "payment line item. No further action required."
        ),
        "audit.claim_state.to": "closed",
        "audit.claim_state.to_substate": "closed_paid_with_no_recovery",
        "audit.claim_state.transition_utc": "2026-05-03T16:00:00Z",
    },
]


def main() -> None:
    # Per-event canonical bytes — each transition event produces its own
    # pinned hash (an integrator emits one event per transition, sealed
    # under the day's seal record).
    per_event_results = []
    for i, event in enumerate(TRANSITIONS):
        canonical_bytes = jcs.canonicalize(event)
        canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
        per_event_results.append({
            "index": i,
            "from_state": event["audit.claim_state.from"],
            "to_state": event["audit.claim_state.to"],
            "from_substate": event["audit.claim_state.from_substate"],
            "to_substate": event["audit.claim_state.to_substate"],
            "canonical_byte_length": len(canonical_bytes),
            "canonical_sha256": canonical_sha256,
        })

    # Lifecycle hash: SHA-256 over the JCS-canonical sorted array of
    # per-event SHA-256 values. Lets a verifier confirm the full lifecycle
    # is consistent with one digest.
    lifecycle_hashes = [r["canonical_sha256"] for r in per_event_results]
    lifecycle_canonical = jcs.canonicalize(lifecycle_hashes)
    lifecycle_sha256 = hashlib.sha256(lifecycle_canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 038-claim-state-lifecycle — pins the "
            "§10.43 chain-entry byte form for a Polaris/Lloyd's-shape 6-"
            "transition lifecycle (FNOL → reserve → adjudication → paid → "
            "recovery → closed). Each event's canonical bytes are pinned; "
            "the lifecycle digest is the SHA-256 over the JCS-canonical "
            "sorted array of per-event hashes."
        ),
        "claim_run_id": CLAIM_RUN_ID,
        "tenant_id": TENANT_ID,
        "transitions": TRANSITIONS,
        "per_event_results": per_event_results,
        "lifecycle_sha256": lifecycle_sha256,
    }

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(fixture, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Save the FIRST event's canonical bytes as the primary pinned form.
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(jcs.canonicalize(TRANSITIONS[0]))

    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for r in per_event_results:
            f.write(f"event[{r['index']}] {r['canonical_sha256']}\n")
        f.write(f"lifecycle {lifecycle_sha256}\n")

    print(f"[038] claim run_id:              {CLAIM_RUN_ID}")
    print(f"[038] transitions:               {len(TRANSITIONS)}")
    for r in per_event_results:
        print(
            f"[038] event[{r['index']}]: {r['from_state']:>8s}/{r['from_substate']:>32s} "
            f"-> {r['to_state']:>8s}/{r['to_substate']:>32s}  sha256={r['canonical_sha256'][:16]}"
        )
    print(f"[038] lifecycle SHA-256:         {lifecycle_sha256}")


if __name__ == "__main__":
    main()
