# Long-Retention Regulator Overlay (60-year horizon)

> **Purpose.** Operational mapping for institutions whose chain-of-custody work crosses long-retention regulatory regimes — where legal mandate exceeds the 7-year default and approaches or exceeds 60 years. Covers Swiss federal tax archive law, Helvetian-shape civic archives, U.S. clinical-trial archival rules (21 CFR 312.62), International Civil Aviation Organization records, defense-acquisition records (DFARS 252.204-7012). Anchors against spec §10.53 (NORMATIVE-when-applicable hybrid post-quantum seal), §10.54 (decadal re-sealing discipline), §11 GAP-6 (cryptographic-agility roadmap, normative reference), §4.3.2 (algorithm-rotation discipline).

## 1. Why this overlay exists

The 7-year retention default named in `retention-justification.md` covers the bulk of regulated data. A small but operationally critical class of records must outlive that horizon by an order of magnitude:

| Regime | Retention floor | Example record class |
|---|---|---|
| Swiss tax archive law (Helvetian-shape, Story 17) | 60 years | VAT audit decisions, tax-ruling determinations |
| U.S. clinical-trial archival (21 CFR 312.62(c)) | 2 years post-FDA approval, OR until lifespan of relevant trial subjects | adverse-event determinations |
| ICAO Annex 13 (civil-aviation incident records) | 50 years | flight-data recorder forensic chain-of-custody |
| DFARS 252.204-7012 (defense acquisition) | Up to 75 years for some classes | export-controlled record provenance |
| Long-arc litigation hold | indefinite | preserved evidence for active-pending matters |

A 7-year-keyed Ed25519 signature is comfortably secure today, but the post-quantum cryptanalysis horizon (the NIST Post-Quantum Cryptography Standardization 2024-2025 finalists; Dilithium-3, Kyber, SPHINCS+) reshapes the 30+ year horizon. An institution with a Swiss VAT audit record signed in 2026 needs that signature to remain attestable in 2086 — under cryptography that has not yet been written.

This overlay names how §10.53 (hybrid post-quantum seal) and §10.54 (decadal re-sealing) are operated to maintain that attestability across the 60-year horizon.

## 2. Mapping table

| Long-retention regulatory surface | Spec section | What the chain shows |
|---|---|---|
| **Swiss federal tax archive law** (60-year retention for tax decisions) | §10.53 + §10.54 | Hybrid PQ seal at the time of decision (Ed25519 + Dilithium3); decadal re-seal at each 10-year boundary under the then-current NIST PQC standard. The chain accumulates 5-6 generations across 60 years. |
| **NIST Post-Quantum Cryptography migration** (PQC standardization 2024-2030+) | §10.53 NORMATIVE-when-applicable | Institutions in scope of long-retention regimes operating after the NIST 2024 Module-Lattice signature finalist designation MUST emit hybrid Ed25519 + Dilithium3 (or successor) signatures on seal records. The "when applicable" gate is the institution's CC8.1-named retention-class policy. |
| **ICAO Annex 13 incident records** (50-year retention) | §10.54 | Decadal re-seal at 2030, 2040, 2050, 2060, 2070; original signature accumulates re-seal anchors but is itself never modified. |
| **U.S. clinical-trial archival** (until subject lifespan) | §10.54 | Re-seal at each decadal boundary for the duration of the longest-lived subject's lifetime; the re-seal generation chain is the substrate for an FDA inspector reading the record at year T+50. |
| **Long-arc litigation hold** | §10.54 + §10.36 | Records under active legal hold receive a §10.36 supplemental seal annotation marking the hold; the §10.54 decadal re-seal applies on top, accumulating both the hold annotation and the decadal anchor. |
| **Cryptographic-agility roadmap** (the institution's CC8.1-named migration plan) | §11 GAP-6 normative reference | Spec §11 lifts `docs/cryptographic-agility-roadmap.md` from informative to normative reference. The institution's CC8.1 names the algorithm-rotation policy under that normative anchor. |

## 3. Examination workflow

A regulator auditing a long-retention chain at year T+50 (e.g., a 2076 audit of a 2026 Helvetian VAT decision):

1. **Generation-chain walk.** The auditor walks the §10.54 generation chain: 0 → 1 → 2 → 3 → 4 → 5 (six seals across 60 years, each at a decadal boundary).

2. **Per-generation verification.** For each generation:
   - Confirm the seal record's `seal.resealed_under_algorithm` value matches the NIST PQC standard in force at the seal's `seal.resealed_window_end_utc`.
   - Confirm `seal.resealed_previous_generation_anchor_sha256` references the prior generation's terminal seal (no gaps in the generation chain).
   - Confirm the cryptographic signature verifies under the algorithm declared (auditor uses an algorithm-aware verifier; the institution's CC8.1 names the verifier-implementation registry).

3. **Original-signature attestability.** For the original 2026 Ed25519 + Dilithium3 hybrid seal (§10.53):
   - The Ed25519 component may no longer verify under post-2050 cryptanalytic developments — that is the point of the hybrid scheme. The Dilithium3 component is the load-bearing signature for post-2030 attestation.
   - Where Ed25519 has fallen, the §10.54 generation chain provides the integrity continuity: the 2030 re-seal under Dilithium3 anchored the original 2026 record into a generation that remained attestable.

4. **Algorithm-rotation evidence.** The institution's CC8.1 names the algorithm-rotation policy per the §11 GAP-6 normative reference. The auditor confirms each generation's algorithm is consistent with the published rotation roadmap; an unexplained algorithm divergence is a finding.

## 4. Operational shapes

### 4.1 Acquisition-time hybrid seal (§10.53)

When the institution enters scope of a long-retention regime, EVERY seal record from that point forward emits the dual-algorithm signature pair per the existing §4.3.2 dual-algorithm discipline. Test vector `015-dual-algorithm-cosigned-seal` IS the byte form; §10.53 NORMATIVE-when-applicable lift means an institution under retention-class scope MUST emit the dual signature.

### 4.2 Decadal re-seal calendar (§10.54)

Institution publishes a re-seal calendar in CC8.1 naming the decadal boundaries (typically January 1 of each decade-end year). The §10.54 record covers the closing decade's seal records as a baseline manifest; the re-seal Merkle-anchors the decade under the new algorithm.

### 4.3 Algorithm-version annotation

Each re-seal carries `seal.resealed_under_algorithm`. The canonical algorithm names (institution-named per CC8.1):

- 2026-2029: `ed25519-dilithium3-hybrid` (§10.53 normative-when-applicable lift)
- 2030-2039: `dilithium3` (NIST PQC primary)
- 2040-2049: `dilithium-V<n>` (next NIST rotation per the algorithm-rotation roadmap)
- ...

The institution's CC8.1 names the actual algorithm progression; the spec normates only the chain shape.

## 5. Worked sample finding

> **Finding 17.3 — Helvetian Federal Tax Authority, 2076 audit of 2026 VAT determination.** The 2026 VAT decision was sealed under §10.53 hybrid Ed25519 + Dilithium3. The chain accumulates five decadal re-seals (2036, 2046, 2056, 2066, 2076) under generations 1-5. The 2036 re-seal under Dilithium3 was the load-bearing post-quantum migration; subsequent re-seals followed the institution's CC8.1-named rotation policy. The original 2026 Ed25519 signature no longer verifies under 2076 cryptanalytic standards (anticipated; the rotation policy named this), but the Dilithium3 component verifies, and the §10.54 generation chain provides unbroken integrity continuity. **The 2026 decision remains chain-attestable in 2076.**

## 6. Cross-references

- Spec §10.53 hybrid post-quantum seal (NORMATIVE-when-applicable lift of §4.3.2)
- Spec §10.54 decadal re-sealing discipline
- Spec §4.3.2 algorithm-rotation discipline
- Spec §11 GAP-6 cryptographic-agility roadmap (normative reference)
- Spec §10.10 IKM rotation
- Spec §10.36 supplemental seal pattern (the precedent §10.54 follows)
- Design `docs/design/15-civic-ai-and-post-quantum.md`
- Design `docs/cryptographic-agility-roadmap.md` (the normative reference the §11 lift names)
- Test vectors `015-dual-algorithm-cosigned-seal`, `047-decadal-resealing`
- Retention justification (`retention-justification.md`) for the 7-year baseline this overlay extends
