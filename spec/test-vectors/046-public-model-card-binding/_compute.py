# -*- coding: utf-8 -*-
"""Compute the §10.52 public model-card binding byte form for FFIEC v1
test-vector case 046-public-model-card-binding.

§10.52 normates that public model-card publications hash-anchor the
model card via §10.19 `audit.external_artifact.*` with the institution-
named kind value `"model_card"`. NO new attribute family — pure §10.19
reuse with the canonical kind discriminator.

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


# Helvetian VAT audit-target model card publication.
KIND = "model_card"
IDENTIFIER = "helvetian-vat-audit-target-model-2026-04"
RECEIVED_AT_UTC = "2026-04-15T08:00:00Z"
SOURCE_PARTY = "helvetian-federal-tax-authority"
EVIDENTIARY_ROLE = "public_model_card_publication"

# SHA-256 of the canonicalized model-card document bytes.
MODEL_CARD_SHA256 = _sha256_of_label(
    "helvetian-vat-audit-target-model-card-2026-04-canonical-markdown"
)


def build_event() -> dict:
    """§10.19 audit.external_artifact.* event with kind = "model_card"."""
    return {
        "audit.external_artifact.evidentiary_role": EVIDENTIARY_ROLE,
        "audit.external_artifact.identifier": IDENTIFIER,
        "audit.external_artifact.kind": KIND,
        "audit.external_artifact.received_at_utc": RECEIVED_AT_UTC,
        "audit.external_artifact.sha256": MODEL_CARD_SHA256,
        "audit.external_artifact.source_party": SOURCE_PARTY,
    }


def main() -> None:
    event = build_event()
    canonical = jcs.canonicalize(event)
    sha256 = hashlib.sha256(canonical).hexdigest()

    fixture = {
        "_about": (
            "Input fixture for case 046-public-model-card-binding — pins "
            "the §10.52 chain-entry byte form for a Helvetian model-card "
            "publication. Uses §10.19 audit.external_artifact.* schema "
            "with the institution-named kind value 'model_card' (§10.52 "
            "is a normative narrative wrapper around §10.19, NOT a new "
            "event family)."
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

    print(f"[046] kind:                      {KIND}")
    print(f"[046] identifier:                {IDENTIFIER}")
    print(f"[046] model_card_sha256:         {MODEL_CARD_SHA256}")
    print(f"[046] canonical len:             {len(canonical)}")
    print(f"[046] canonical SHA-256:         {sha256}")


if __name__ == "__main__":
    main()
