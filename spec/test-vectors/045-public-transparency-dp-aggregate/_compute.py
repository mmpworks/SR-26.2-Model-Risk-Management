# -*- coding: utf-8 -*-
"""Compute the §10.51 public-transparency DP-bound aggregate event byte
form for FFIEC v1 test-vector case 045-public-transparency-dp-aggregate.

§10.51 normates `chain.public_transparency.published` events that bind
a DP-noised aggregate value, the DP mechanism, the ε budget, the RNG
seed, and the mechanism-version hash. Per §1.2's public-transparency
epistemic claim: chain binds the NOISED aggregate (the published
value), NOT the raw aggregate; the noise application is a separate
attestable step.

This case pins the byte form for a Helvetian-shape VAT-audits-initiated
monthly aggregate published on the public-transparency portal.

Run with: python _compute.py
"""

from __future__ import annotations

import hashlib
import json
import os

import jcs

HERE = os.path.dirname(os.path.abspath(__file__))


def _sha256_of_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


# Pinned inputs — Helvetian Federal Tax Authority publishing the noised
# count of VAT audits initiated in May 2026.
AGGREGATE_KIND = "vat_audits_initiated_count"
COVERAGE_PERIOD_START_UTC = "2026-05-01T00:00:00Z"
COVERAGE_PERIOD_END_UTC = "2026-05-31T23:59:59Z"
PUBLISHED_AT_UTC = "2026-06-15T09:00:00Z"
DP_MECHANISM = "laplace"
DP_EPSILON = 1.0
DP_SEED = 4242
# DP_DELTA absent — Laplace is pure-DP (δ=0).

# Synthetic mechanism-version hash — SHA-256 of the canonicalized
# noise-sampling-implementation source bytes. Production institutions
# bind their actual implementation hash; we use a deterministic seed.
DP_MECHANISM_VERSION_SHA256 = _sha256_of_label(
    "helvetian-laplace-noise-sampler-v2.0-2026"
)

# The published noised value. The raw aggregate would be e.g. 12,047;
# Laplace noise at ε=1.0 typically adds noise of stdev sqrt(2)/ε = 1.41,
# so the published value is the raw + sample noise. For the test-vector
# we just pin the noised value the institution claims to have published.
AGGREGATE_PUBLISHED_VALUE = 12046

# Optional cohort-subtree cross-binding — the §10.31 / §10.44 Merkle
# root over the chain entries the aggregate was computed from.
COHORT_SUBTREE_ROOT_SHA256 = _sha256_of_label(
    "helvetian-vat-audits-2026-05-cohort-subtree-merkle-root"
)


def build_event() -> dict:
    """§10.51 chain-entry payload — 9 required + 1 optional fields."""
    return {
        "audit.public_transparency.aggregate_kind": AGGREGATE_KIND,
        "audit.public_transparency.aggregate_published_value": AGGREGATE_PUBLISHED_VALUE,
        "audit.public_transparency.cohort_subtree_root_sha256": COHORT_SUBTREE_ROOT_SHA256,
        "audit.public_transparency.coverage_period_end_utc": COVERAGE_PERIOD_END_UTC,
        "audit.public_transparency.coverage_period_start_utc": COVERAGE_PERIOD_START_UTC,
        "audit.public_transparency.dp_epsilon": DP_EPSILON,
        "audit.public_transparency.dp_mechanism": DP_MECHANISM,
        "audit.public_transparency.dp_mechanism_version_sha256": DP_MECHANISM_VERSION_SHA256,
        "audit.public_transparency.dp_seed": DP_SEED,
        "audit.public_transparency.published_at_utc": PUBLISHED_AT_UTC,
    }


def main() -> None:
    event = build_event()
    canonical = jcs.canonicalize(event)
    sha256 = hashlib.sha256(canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 045-public-transparency-dp-aggregate "
            "— pins the §10.51 chain-entry byte form for a Helvetian-"
            "shape VAT-audits-initiated DP-noised monthly aggregate."
        ),
        "event": event,
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

    print(f"[045] aggregate_kind:            {AGGREGATE_KIND}")
    print(f"[045] dp_mechanism:              {DP_MECHANISM}")
    print(f"[045] dp_epsilon:                {DP_EPSILON}")
    print(f"[045] published_value:           {AGGREGATE_PUBLISHED_VALUE}")
    print(f"[045] canonical len:             {len(canonical)}")
    print(f"[045] canonical SHA-256:         {sha256}")


if __name__ == "__main__":
    main()
