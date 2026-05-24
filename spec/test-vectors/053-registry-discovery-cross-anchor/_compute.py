# -*- coding: utf-8 -*-
"""Compute the §10.21.3 registry-discovery cross-anchor byte form for FFIEC
v1 test-vector case 053-registry-discovery-cross-anchor.

Spec §10.21.3 normates the registry-discovery cross-anchor pattern: an
originating institution publishes a cross-anchor to a third-party
registry; a counterpart institution retrieves it. Canonical instance:
the Federal Reserve's voluntary cross-institution-anchor registry for
Fedwire and ACH (§10.71). Other registries: SWIFT-mediated international-
wire, FedNow instant-payment, FINRA broker-dealer trade-reporting,
CCP-cleared-derivatives, credit-bureau-mediated cross-institution
correlation.

This case pins TWO of the three normative `cross_anchor_state` values:

  - `bound` — both originating and counterpart sides published; cross-
    anchor verifiable; verifier emits `registry_cross_anchor_verified`.
  - `unbound` — counterpart institution non-participating in the
    registry; verifier emits `cross_anchor_unbound` and the institution's
    CC8.1 documents the non-participation as a residual.

The third state (`published-pending-counterpart` — originating side
published, counterpart not yet published) is NOT exercised in this
vector per the PRD-3 index scope ("two of the three normative
`cross_anchor_state` values"; the third state is a V3 follow-up).

The §10.21.3 schema additions on each cross-anchor entry per spec
lines 2535-2543:

  audit.registry_discovery.registry_identity (yes)
  audit.registry_discovery.registry_publication_id (yes)
  audit.registry_discovery.registry_publication_at_utc (yes)
  audit.registry_discovery.counterpart_institution (when applicable)
  audit.registry_discovery.cross_anchor_state (yes; enum)

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Pinned inputs — synthetic Federal Reserve Fedwire-registry cross-anchor
# for the `bound` variant and a parallel cross-anchor for the `unbound`
# variant. Two distinct registry publication ids; institutions named
# per spec §10.71 canonical Fedwire shape.
# ---------------------------------------------------------------------------

REGISTRY_IDENTITY = "federal-reserve-fedwire-registry"
REGISTRY_PUBLICATION_AT_UTC = "2026-05-21T15:30:00Z"

# BOUND variant — originating + receiving both participate, both
# published, cross-anchor verifies at the registry.
BOUND_PUBLICATION_ID = "fed-fedwire-xanchor-2026-05-21-pub-NBFS-cape-001"
BOUND_COUNTERPART_INSTITUTION = "cape-madeline-bank-and-trust"

# UNBOUND variant — originating institution publishes; counterpart
# institution is non-participating in the registry. Per spec §10.21.3
# the `counterpart_institution` attribute is `when applicable`; when
# the counterpart is non-participating the field is documented in CC8.1
# but the chain-entry still carries the field so the institutional
# residual is integrity-bound. The fixture emits the counterpart name
# in the unbound variant as well, mirroring spec text on residual
# documentation discipline.
UNBOUND_PUBLICATION_ID = "fed-fedwire-xanchor-2026-05-21-pub-NBFS-orphan-002"
UNBOUND_COUNTERPART_INSTITUTION = "non-participating-receiver-institution-XYZ"


def build_cross_anchor_entry(
    *,
    registry_publication_id: str,
    counterpart_institution: str,
    cross_anchor_state: str,
) -> dict:
    """Build a §10.21.3 cross-anchor entry's registry-discovery attribute
    set per spec lines 2537-2543. Keys appear in source order; JCS
    sorts lexicographically.

    Attribute names use the spec's dotted `audit.registry_discovery.*`
    schema verbatim. The full chain-entry envelope is out of scope;
    this fixture pins only the §10.21.3-specific attributes that
    distinguish registry-discovery cross-anchors from generic §10.21
    cross-anchors.
    """
    return {
        "audit.registry_discovery.counterpart_institution": counterpart_institution,
        "audit.registry_discovery.cross_anchor_state": cross_anchor_state,
        "audit.registry_discovery.registry_identity": REGISTRY_IDENTITY,
        "audit.registry_discovery.registry_publication_at_utc": (
            REGISTRY_PUBLICATION_AT_UTC
        ),
        "audit.registry_discovery.registry_publication_id": registry_publication_id,
    }


# Pinned placeholder values for the verdict object (matching case 036
# and case 050/051/052's placeholders so all Phase 11 vectors compose
# consistently).
PLACEHOLDER_POSTURE = "ffiec"
PLACEHOLDER_TRUST_ANCHOR_SHA256 = (
    "7c2a5f9b1d3e8c6a4b2f1e9d7c5a3b1f8e2d6c4a9b7e5d3c1a8f6e4d2c0b9a8e"
)
PLACEHOLDER_SPEC_VERSION = "v1.0c"
PLACEHOLDER_VERIFIER_VERSION = "v1.0c-verifier-2026-05-15"


def build_verdict(marker: str) -> dict:
    """§10.12 verdict object on §10.21.3 cross-anchor walk. The marker
    differs by state:
      - `bound`   → `registry_cross_anchor_verified`
      - `unbound` → `cross_anchor_unbound`

    Both states exit_code 0 (PASS) per §10.12 additional-verifications
    discipline — the unbound state is a documented residual, not a
    chain-integrity failure.
    """
    return {
        "additional_verifications": [marker],
        "exit_code": 0,
        "posture": PLACEHOLDER_POSTURE,
        "trust_anchor_manifest_sha256": PLACEHOLDER_TRUST_ANCHOR_SHA256,
        "verifier_spec_version_supported": PLACEHOLDER_SPEC_VERSION,
        "verifier_version": PLACEHOLDER_VERIFIER_VERSION,
    }


def canonicalize_and_hash(obj: dict) -> tuple[bytes, str]:
    canonical_bytes = jcs.canonicalize(obj)
    return canonical_bytes, hashlib.sha256(canonical_bytes).hexdigest()


def main() -> None:
    # ----- BOUND variant -----
    bound_entry = build_cross_anchor_entry(
        registry_publication_id=BOUND_PUBLICATION_ID,
        counterpart_institution=BOUND_COUNTERPART_INSTITUTION,
        cross_anchor_state="bound",
    )
    bound_bytes, bound_sha256 = canonicalize_and_hash(bound_entry)

    bound_verdict = build_verdict("registry_cross_anchor_verified")
    bound_verdict_bytes, bound_verdict_sha256 = canonicalize_and_hash(bound_verdict)

    bound_composed = {
        "cross_anchor_entry": bound_entry,
        "cross_anchor_state": "bound",
        "verdict": bound_verdict,
    }
    bound_composed_bytes, bound_composed_sha256 = canonicalize_and_hash(bound_composed)

    # ----- UNBOUND variant -----
    unbound_entry = build_cross_anchor_entry(
        registry_publication_id=UNBOUND_PUBLICATION_ID,
        counterpart_institution=UNBOUND_COUNTERPART_INSTITUTION,
        cross_anchor_state="unbound",
    )
    unbound_bytes, unbound_sha256 = canonicalize_and_hash(unbound_entry)

    unbound_verdict = build_verdict("cross_anchor_unbound")
    unbound_verdict_bytes, unbound_verdict_sha256 = canonicalize_and_hash(unbound_verdict)

    unbound_composed = {
        "cross_anchor_entry": unbound_entry,
        "cross_anchor_state": "unbound",
        "verdict": unbound_verdict,
    }
    unbound_composed_bytes, unbound_composed_sha256 = canonicalize_and_hash(unbound_composed)

    input_record = {
        "_about": (
            "Input fixture for case 053-registry-discovery-cross-anchor. "
            "Pins TWO of the three §10.21.3 normative `cross_anchor_state` "
            "values: `bound` (both sides participate; verifier emits "
            "`registry_cross_anchor_verified`) and `unbound` (counterpart "
            "non-participating; verifier emits `cross_anchor_unbound` "
            "and the institution's CC8.1 documents the non-participation "
            "as a residual). The third state `published-pending-"
            "counterpart` is not exercised in this vector per the PRD-3 "
            "index scope (V3 follow-up)."
        ),
        "registry_identity": REGISTRY_IDENTITY,
        "registry_publication_at_utc": REGISTRY_PUBLICATION_AT_UTC,
        "bound": {
            "cross_anchor_entry": bound_entry,
            "cross_anchor_canonical_byte_length": len(bound_bytes),
            "cross_anchor_canonical_sha256": bound_sha256,
            "cross_anchor_canonical_bytes_utf8": bound_bytes.decode("utf-8"),
            "verdict": bound_verdict,
            "verdict_canonical_byte_length": len(bound_verdict_bytes),
            "verdict_canonical_sha256": bound_verdict_sha256,
            "verdict_canonical_bytes_utf8": bound_verdict_bytes.decode("utf-8"),
            "composed_record": bound_composed,
            "composed_canonical_byte_length": len(bound_composed_bytes),
            "composed_canonical_sha256": bound_composed_sha256,
        },
        "unbound": {
            "cross_anchor_entry": unbound_entry,
            "cross_anchor_canonical_byte_length": len(unbound_bytes),
            "cross_anchor_canonical_sha256": unbound_sha256,
            "cross_anchor_canonical_bytes_utf8": unbound_bytes.decode("utf-8"),
            "verdict": unbound_verdict,
            "verdict_canonical_byte_length": len(unbound_verdict_bytes),
            "verdict_canonical_sha256": unbound_verdict_sha256,
            "verdict_canonical_bytes_utf8": unbound_verdict_bytes.decode("utf-8"),
            "composed_record": unbound_composed,
            "composed_canonical_byte_length": len(unbound_composed_bytes),
            "composed_canonical_sha256": unbound_composed_sha256,
        },
    }
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump(input_record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # expected_canonical.txt carries the two composed-record byte forms
    # separated by a single LF (bound first, then unbound). A reader
    # splits on LF to recover each variant. The
    # expected_canonical_sha256.txt opens with a `full_blob <hash>`
    # line (SHA-256 of the entire expected_canonical.txt blob),
    # followed by the per-sub-form labeled hex digests. See README
    # §"Multi-payload vector sha256 convention".
    blob_bytes = bound_composed_bytes + b"\n" + unbound_composed_bytes
    with open(os.path.join(HERE, "expected_canonical.txt"), "wb") as f:
        f.write(blob_bytes)

    full_blob_sha256 = hashlib.sha256(blob_bytes).hexdigest()
    with open(
        os.path.join(HERE, "expected_canonical_sha256.txt"),
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(f"full_blob               {full_blob_sha256}\n")
        f.write(f"bound_cross_anchor      {bound_sha256}\n")
        f.write(f"bound_verdict           {bound_verdict_sha256}\n")
        f.write(f"bound_composed          {bound_composed_sha256}\n")
        f.write(f"unbound_cross_anchor    {unbound_sha256}\n")
        f.write(f"unbound_verdict         {unbound_verdict_sha256}\n")
        f.write(f"unbound_composed        {unbound_composed_sha256}\n")

    print(f"[053] registry identity:           {REGISTRY_IDENTITY}")
    print(f"[053] bound cross-anchor len:      {len(bound_bytes)}")
    print(f"[053] bound cross-anchor SHA-256:  {bound_sha256}")
    print(f"[053] bound verdict SHA-256:       {bound_verdict_sha256}")
    print(f"[053] bound composed SHA-256:      {bound_composed_sha256}")
    print(f"[053] unbound cross-anchor len:    {len(unbound_bytes)}")
    print(f"[053] unbound cross-anchor SHA-256:{unbound_sha256}")
    print(f"[053] unbound verdict SHA-256:     {unbound_verdict_sha256}")
    print(f"[053] unbound composed SHA-256:    {unbound_composed_sha256}")


if __name__ == "__main__":
    main()
