"""Worked example of §7 verifier output — line-oriented form + Verdict-Object trailing line.

Demonstrates verdict-object construction, JCS canonicalization, the line-oriented form per §7
(PASS / FAIL / PASS-STRUCTURALLY), the normative Verdict-Object trailing line, and round-trip
parsing of the trailing line out of stdout text. Asserts byte-equivalence with the three
sub-cases pinned in test vector 036 (036a empty, 036b one marker, 036c two markers).

Run: pip install jcs ; python example.py

Cross-references: §5, §7, §10.12, vector 036.
"""

from __future__ import annotations

import hashlib

import jcs


# --- Verdict object ------------------------------------------------------

def build_verdict_object(
    *, additional_verifications: list[str], exit_code: int
) -> dict[str, object]:
    """Construct the verdict-object dict pinned in vector 036.

    The shape is closed: exactly two fields, `additional_verifications` (array of
    strings from the §10.12 closed enumeration) and `exit_code` (the verifier's
    CLI exit code). Empty array is structurally explicit on every non-zero exit
    and on PASS with no bonus verifications.
    """
    return {
        "additional_verifications": list(additional_verifications),
        "exit_code": int(exit_code),
    }


def verdict_object_jcs_bytes(verdict: dict[str, object]) -> bytes:
    """JCS-canonicalize the verdict object per §5 / RFC 8785."""
    return jcs.canonicalize(verdict)


# --- Verifier output formatting ------------------------------------------

def format_verifier_output(
    *,
    status: str,
    step: int | None,
    reason: str | None,
    anomaly_lines: list[str],
    verdict: dict[str, object],
) -> str:
    """Produce the full §7 verifier output for a verifier run.

    PASS → `Status: PASS` + zero or more anomaly lines + Verdict-Object trailing line.
    FAIL → `Status: FAIL` + `Step: N` + `Reason: <text>` + Verdict-Object trailing line.
    Witness → `Status: PASS-STRUCTURALLY, key-bound verification skipped` + Verdict-Object trailing line.

    All lines terminated with 0x0A. The Verdict-Object label is exact: `Verdict-Object: ` (capitalization,
    hyphen, colon, single-space separator).
    """
    lines: list[str] = []
    if status == "FAIL":
        lines.append("Status: FAIL")
        lines.append(f"Step: {step}")
        lines.append(f"Reason: {reason}")
    elif status == "PASS-STRUCTURALLY":
        lines.append("Status: PASS-STRUCTURALLY, key-bound verification skipped")
    else:
        lines.append("Status: PASS")
        lines.extend(anomaly_lines)

    jcs_bytes = verdict_object_jcs_bytes(verdict)
    lines.append(f"Verdict-Object: {jcs_bytes.decode('utf-8')}")
    return "\n".join(lines) + "\n"


# --- Trailing-line parsing -----------------------------------------------

def extract_verdict_object(stdout_text: str) -> dict[str, object]:
    """Find the `Verdict-Object: ` line in stdout and JSON-decode the trailing bytes.

    Per §7, the line is the last normative line; implementations may append further
    diagnostic lines after it. Consumers scan for the exact prefix; the JSON-decode is
    a one-liner in any scripting language.
    """
    import json
    prefix = "Verdict-Object: "
    for line in stdout_text.splitlines():
        if line.startswith(prefix):
            return json.loads(line[len(prefix):])
    raise ValueError("Verdict-Object trailing line not found in stdout")


# --- Demonstration -------------------------------------------------------

def demo_pass(label: str, additional_verifications: list[str]) -> str:
    verdict = build_verdict_object(
        additional_verifications=additional_verifications, exit_code=0
    )
    output = format_verifier_output(
        status="PASS", step=None, reason=None, anomaly_lines=[], verdict=verdict
    )
    print(f"--- {label}: PASS, additional_verifications={additional_verifications} ---")
    print(output, end="")
    print()
    return output


def demo_fail() -> str:
    verdict = build_verdict_object(additional_verifications=[], exit_code=1)
    output = format_verifier_output(
        status="FAIL",
        step=9,
        reason="payload_hash MAC mismatch at seq 17",
        anomaly_lines=[],
        verdict=verdict,
    )
    print("--- FAIL example ---")
    print(output, end="")
    print()
    return output


def demo_pass_with_anomaly() -> str:
    verdict = build_verdict_object(
        additional_verifications=["unknown_kind_present"], exit_code=0
    )
    output = format_verifier_output(
        status="PASS",
        step=None,
        reason=None,
        anomaly_lines=["unknown wire-format kind present: cross_domain_transition (count: 1)"],
        verdict=verdict,
    )
    print("--- PASS-with-anomaly example ---")
    print(output, end="")
    print()
    return output


# --- Vector-036 byte-equivalence assertion -------------------------------

VECTOR_036_PINS = {
    "036a": {
        "verdict": {"additional_verifications": [], "exit_code": 0},
        "canonical_sha256": "c79490211ce76c721560fe28d1a781e70b391353ebe3c4cf3d6aa743ab4895ba",
    },
    "036b": {
        "verdict": {"additional_verifications": ["backfill_seal_verified"], "exit_code": 0},
        "canonical_sha256": "18f280814c89104f1c728a8dbd99e87ae8d5202b6cd4a0c890e1eabccd6f6972",
    },
    "036c": {
        "verdict": {
            "additional_verifications": ["backfill_seal_verified", "hybrid_pqc_dual_signature_verified"],
            "exit_code": 0,
        },
        "canonical_sha256": "8062495801460b1ed1969788ebe7bcf40dce63cc9d734a3ceaea43e2cd6316a4",
    },
}


def assert_vector_036_match() -> None:
    print("--- vector-036 byte-equivalence assertion ---")
    for label, pin in VECTOR_036_PINS.items():
        canonical = verdict_object_jcs_bytes(pin["verdict"])
        recomputed = hashlib.sha256(canonical).hexdigest()
        assert recomputed == pin["canonical_sha256"], (
            f"{label} mismatch: expected {pin['canonical_sha256']}, got {recomputed}"
        )
        print(f"  {label}: SHA-256 = {recomputed}  PASS")
    print()


# --- Round-trip parse demonstration --------------------------------------

def demo_round_trip(stdout_text: str, expected_verdict: dict[str, object]) -> None:
    print("--- round-trip: parse Verdict-Object from stdout text ---")
    parsed = extract_verdict_object(stdout_text)
    print(f"  parsed: {parsed}")
    assert parsed == expected_verdict, (
        f"round-trip mismatch: expected {expected_verdict}, got {parsed}"
    )
    print("  match: PASS")
    print()


def main() -> None:
    assert_vector_036_match()

    out_036a = demo_pass("036a", [])
    out_036b = demo_pass("036b", ["backfill_seal_verified"])
    out_036c = demo_pass(
        "036c", ["backfill_seal_verified", "hybrid_pqc_dual_signature_verified"]
    )
    out_fail = demo_fail()
    out_anomaly = demo_pass_with_anomaly()

    demo_round_trip(out_036a, VECTOR_036_PINS["036a"]["verdict"])
    demo_round_trip(out_fail, {"additional_verifications": [], "exit_code": 1})
    demo_round_trip(
        out_anomaly, {"additional_verifications": ["unknown_kind_present"], "exit_code": 0}
    )


if __name__ == "__main__":
    main()
