# -*- coding: utf-8 -*-
"""Compute the §1.5 / GAP-2 state-machine transition-validator byte form for
FFIEC v1 test-vector case 037-state-machine-transition-validator.

The §1.5 / GAP-2 framing normates a minimal state-machine primitive that
§10.43 (claim-state), §10.46 (bordereau lifecycle), and §10.55
(challenge-response) all consume. The primitive is intentionally domain-agnostic — it validates
(a) a transition (from, to) against a caller-supplied transitions table
and (b) that a sequence of transitions forms a coherent history (no gaps,
no out-of-order arrivals, no transition out of a terminal state).

This case pins the JCS-canonical bytes for a synthetic transitions-table
walk: a 4-state machine (opened → pending → decided → closed) plus a
walk that exercises the validator on each acceptance and rejection path.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# Pinned 4-state transitions table mirroring §10.43's high-level lifecycle.
TRANSITIONS_TABLE = {
    "opened": ["pending", "closed"],     # closed = e.g., immediately rejected at intake
    "pending": ["decided", "closed"],     # closed = e.g., withdrawn while pending
    "decided": ["closed"],
    "closed": [],                         # terminal
}


# Walk A — happy path through a 4-step lifecycle.
WALK_A = [
    {"from_state": "opened", "to_state": "pending"},
    {"from_state": "pending", "to_state": "decided"},
    {"from_state": "decided", "to_state": "closed"},
]


# Walk B — invalid: skips pending (opened → decided).
WALK_B = [
    {"from_state": "opened", "to_state": "decided"},
]


# Walk C — invalid: transition out of terminal state.
WALK_C = [
    {"from_state": "closed", "to_state": "opened"},
]


# Walk D — invalid: gap (first transition's from-state is not the prior's to-state).
WALK_D = [
    {"from_state": "opened", "to_state": "pending"},
    {"from_state": "decided", "to_state": "closed"},  # GAP: skipped pending → decided
]


def is_valid_transition(from_state: str, to_state: str, table: dict) -> bool:
    """Single-transition validator. Returns True iff (from, to) is in the
    caller-supplied transitions table.
    """
    return to_state in table.get(from_state, [])


def is_valid_walk(walk: list, table: dict) -> dict:
    """Sequence validator. Returns {valid: bool, first_failure_index: int|null,
    reason: str}.
    """
    if not walk:
        return {"valid": True, "first_failure_index": None, "reason": "empty walk"}
    for i, step in enumerate(walk):
        # History-gap check runs FIRST (per the production
        # _state_machine.py contract — order matters because "decided"
        # appearing after "opened -> pending" is a history gap, not an
        # invalid transition).
        if i > 0 and walk[i - 1]["to_state"] != step["from_state"]:
            return {
                "valid": False,
                "first_failure_index": i,
                "reason": (
                    f"history gap: prior to_state {walk[i - 1]['to_state']!r} "
                    f"!= current from_state {step['from_state']!r}"
                ),
            }
        if not is_valid_transition(step["from_state"], step["to_state"], table):
            return {
                "valid": False,
                "first_failure_index": i,
                "reason": (
                    f"transition ({step['from_state']!r} -> {step['to_state']!r}) "
                    f"not in transitions table"
                ),
            }
    return {"valid": True, "first_failure_index": None, "reason": "all transitions valid"}


def main() -> None:
    # The cross-impl byte pin asserts that the JCS-canonical encoding of
    # the validator's structured output is identical between Python and
    # .NET — given the same input.
    fixture = {
        "transitions_table": TRANSITIONS_TABLE,
        "walks": {
            "walk_a_happy_path": {
                "input": WALK_A,
                "result": is_valid_walk(WALK_A, TRANSITIONS_TABLE),
            },
            "walk_b_skips_pending": {
                "input": WALK_B,
                "result": is_valid_walk(WALK_B, TRANSITIONS_TABLE),
            },
            "walk_c_out_of_terminal": {
                "input": WALK_C,
                "result": is_valid_walk(WALK_C, TRANSITIONS_TABLE),
            },
            "walk_d_history_gap": {
                "input": WALK_D,
                "result": is_valid_walk(WALK_D, TRANSITIONS_TABLE),
            },
        },
    }

    canonical_bytes = jcs.canonicalize(fixture)
    canonical_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "_about": (
                    "Input fixture for case 037-state-machine-transition-validator "
                    "— pins the GAP-2 minimal primitive's transition-validator and "
                    "walk-validator output byte form. Four walks exercise (A) the "
                    "happy path, (B) an invalid transition (skipping pending), "
                    "(C) transition out of a terminal state, and (D) a history "
                    "gap (prior to_state != current from_state)."
                ),
                "fixture": fixture,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
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

    print(f"[037] transitions:               {len(TRANSITIONS_TABLE)} states")
    print(f"[037] walks:                     4 (A happy / B skip / C terminal / D gap)")
    print(f"[037] canonical len:             {len(canonical_bytes)}")
    print(f"[037] canonical SHA-256:         {canonical_sha256}")


if __name__ == "__main__":
    main()
