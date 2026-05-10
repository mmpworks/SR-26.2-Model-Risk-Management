# M&A and corporate transactions

> **Status:** Normative-supplement to spec §10.24 "Entity succession". Per Round-17 M&A-G1 close-out, this document is no longer informative — it is the operational supplement to the binding spec section. Acquirer's counsel cites spec §10.24 in representation drafting; this document provides the operational shapes (merger / acquisition / divestiture / spin-off / vendor-change) the institution's CC8.1 names per spec §10.18 cross-referencing rule. The spec section is the binding requirement; this document is the operational realization.
>
> **What this doc is.** Procedures for chain-of-custody operation during mergers, acquisitions, divestitures, and spin-offs. Each scenario below maps to a `chain.entity_succession` operational event under spec §10.2 with `kind` set to the matching enum value (`merger` | `acquisition` | `divestiture` | `rename` | `subsidiary_transfer`). Closes the SOC-Audit M&A partials and the Round-17 M&A-G1 entity-succession gap.

## Scenarios

| Scenario | Description |
|---|---|
| **Merger** | Two institutions combine; one chain operation absorbs the other |
| **Acquisition** | Acquirer takes over target's chain operation |
| **Divestiture** | Bank sells a unit; the unit's chain history transfers to the acquirer |
| **Spin-off** | Bank creates an independent entity; chain operations transfer |
| **Vendor change** | Institution moves chain implementation from vendor A to vendor B (institution unchanged) |

## General principles

- Past chain artifacts (events, seals) are verifiable by anyone holding the public key. Public keys are in the tenant key registry; transfer is straightforward.
- Master HMAC keys are escrowable and transferable through HSM-supported procedures.
- Signing keys are non-extractable; transfer requires regenerating per-tenant signing keys at the new HSM, with a key-rotation event documented.
- Tenant identifiers are transferable; the receiving entity may rename or retain.

## Merger

### Pre-merger preparation

Both institutions:

1. Document their chain configuration (cadence, HSM provider, master-key custodian, tenant_ids in use)
2. Prepare a public-key transfer plan (which keys move, when)
3. Identify pending chain-detected events; resolve before close

### At-close handoff

1. Combined entity declares which chain configuration prevails (typically the larger institution's)
2. Combined tenant_id naming scheme decided (usually a renaming of the smaller institution's tenant_ids to the combined entity's pattern)
3. HSM transfer: master and signing keys move under HSM-supported procedures (Thales / Entrust / cloud-provider key-export procedures)
4. Public keys updated in the tenant key registry; old public keys retained with valid_from/valid_until for past-event verification
5. Internal audit teams of both institutions concur on the handoff

### Post-merger operation

- Past events of both institutions remain verifiable against their pre-merger public keys
- New events use the combined entity's keys
- The verifier handles past events of either pre-merger entity by reading their original public key
- Combined entity's SOC report covers the combined operations starting at close

### Combined-entity tenant_id

Two patterns:

**Pattern A — Combined tenant_id from close.** New events use the combined entity's tenant_id (e.g., `tenant_megabank_post_merger`). Past events retain their pre-merger tenant_id. The combined entity's verifier runs cover both — past events under pre-merger ids, new events under combined id.

**Pattern B — Tenant_id renaming.** Past events are re-keyed (re-stored under the new tenant_id with new master_version). This is heavier; typically not done. Only used if the legal-entity continuity requires it.

Pattern A is the default. Pattern B is for cases where past chain history must legally be the combined entity's record.

## Acquisition

Same as merger from the acquirer's perspective. The target's chain operations flow into the acquirer's. The acquirer absorbs the target's tenant_ids, public keys (added to the registry), and operational procedures.

If the target is operating a chain implementation different from the acquirer's, the acquirer migrates the target onto the acquirer's chain configuration over a planned timeline (typically 6–12 months). During migration, both implementations operate; verifier output covers both.

## Divestiture

The selling institution sells a unit. The unit's chain history goes with the unit:

1. Selling institution provides the buying entity with: the unit's tenant_id, ledger snapshots covering the unit's history, the public key for past-seal verification, the master-key (escrowed via secure transfer), and the seal-job credentials
2. Buying entity provisions its own HSM and master-key custodian
3. Buying entity's first chain event under the new ownership starts with the new master_version
4. Past events remain verifiable against the original public key (held by buyer)
5. Selling institution removes the unit's tenant_id from its active operations

### Public-key transfer

The selling institution provides the public key as a flat file (PEM-encoded). The buying entity registers the key in its tenant key registry with `valid_from` (the unit's start date in the chain) and `valid_until` (the divestiture close date). The post-divestiture key is the buying entity's new key.

### Master-key transfer

Master-key transfer is HSM-vendor-specific:

- AWS CloudHSM: master-key clone procedure (vendor-supported)
- Azure Managed HSM: secure key import via Cryptographic Officer credentials
- Google Cloud HSM: key export under HSM-mediated wrap

The procedure is documented in the divestiture's IT-transition plan. Both selling and buying institutions retain the procedure documentation for audit.

### Documentation

The divestiture documentation includes:

- The chain transfer agreement
- The HSM transfer procedure executed
- The institution's control description for the chain operation (transferred to the buying entity)
- All deliverable docs (this directory) transferred to the buying entity's chain-ops team

## Spin-off

Similar to divestiture but the spin-off is a new entity created by the parent. The parent retains a stake (ownership, sometimes operational support).

The chain transfer follows the divestiture procedure. The spin-off entity becomes an independent institution with its own chain operations.

## Vendor change (institution unchanged)

The institution moves chain implementation from vendor A to vendor B. The institution's tenant_id, master key, and signing keys remain the institution's; only the runtime software changes:

1. Validate vendor B's implementation against the conformance corpus
2. Plan a parallel-operation period (vendor A still receiving events; vendor B starts receiving events)
3. At cutover, vendor A's ingest stops; vendor B's ingest is primary
4. Vendor A's ledger remains for past-event verification; vendor B's ledger is the new source-of-truth
5. Bridge events that span the cutover (if any) are re-keyed if needed (typically minor)

The chain spec is open-standards; vendor migration is structurally tractable. Past data verifies under either vendor's verifier (both produce identical output by spec).

## SOC reporting during transactions

SOC reports follow AICPA guidance:

- The SOC report covers the entity that operated the controls during the period
- For transitions mid-period, the SOC report describes both pre- and post-transition operation
- Section 4 description includes the transition timeline and the affected scopes

The chain doesn't change SOC reporting practices; it provides the artifacts the SOC firm uses.

## Examination during transactions

During M&A periods, the regulator's examination program covers both pre- and post-transition operations. The chain provides per-period verifier output. The EIC examines:

- Pre-transition chain operation (under the pre-transition entity's controls)
- Transition itself (HSM transfer, key rotation, control transition)
- Post-transition chain operation (under the new entity's controls)

The institution's transition documentation supports the examination.

## Common pitfalls

- **Forgetting to add the previous entity's public key to the new tenant key registry.** Past events become unverifiable. Mitigation: the registry retains all keys with valid_from/valid_until.
- **Master-key transfer procedure not tested before the live transfer.** A failed transfer at the live event can disrupt operations. Mitigation: dry-run the transfer in a non-production environment.
- **Tenant_id renaming without controls update.** The institution's monitoring tools may track the old tenant_id. Mitigation: the tenant_id change goes through standard change management.
- **Vendor lock-in concerns ignored.** Some vendors may resist supporting migration. Mitigation: the institution holds the keys and the standard-compliant data; migration is contractually tractable.

## Operational checklist

For any M&A or corporate transaction affecting chain operations:

- [ ] Pre-transaction: document current chain configuration
- [ ] Plan: HSM transfer procedure tested in non-production
- [ ] Plan: public-key registry updates planned
- [ ] Plan: tenant_id naming decisions made
- [ ] At-close: HSM transfer executed
- [ ] At-close: public-key registry updated
- [ ] At-close: chain operations switch to new entity
- [ ] Post-close: verifier runs successfully under both old and new public keys
- [ ] Post-close: SOC reporting covers the transition
- [ ] Post-close: regulator informed (per institution's primary regulator notification policy)

## Cross-vendor-target onboarding (§10.39 / §10.42)

The procedures above presume the *target* operated a Herald-conformant chain that the acquirer can continue under the same `(tenant_id, run_id)` keying with a §10.24 entity-succession event. The cross-vendor-target subcase — where the acquired entity operated a different vendor's chain, baseline-diary records, or paper-and-PDF retention — produces a *chain discontinuity* the §10.24 dual_signatures alone cannot bridge. §10.39 (institutional successor-attestation) and §10.42 (backfill seal) close the gap.

### Operational shape A — target on a different vendor's chain

When the acquired entity ran on LedgerKnot, AttestaCorp, or any non-Herald-conformant vendor whose verifier the acquirer does not run, the institution emits, alongside the §10.24 `chain.entity_succession` event:

1. **A §10.39 `chain.successor_attestation` event** with `baseline_manifest_kind = "prior_vendor_chain"` (or `"prior_vendor_signed_pdfs"` if only signed daily roll-up PDFs are inherited). The `baseline_manifest_sha256` is the SHA-256 of the canonicalized list of inherited foreign-vendor artifacts.
2. **§10.40 cross-anchor entries** per foreign-vendor roll-up artifact (typically per signed daily PDF) under §10.19's `audit.external_artifact.*` family. The acquirer's chain becomes the integrity-bound retrieval substrate even after the foreign vendor's service is decommissioned, provided the underlying artifact bytes are retained.

NO §10.42 backfill seal is needed in this shape — the §10.40 cross-anchors ARE the cryptographic substrate.

### Operational shape B — target on baseline-diary records

When the acquired entity's pre-acquisition records are under a non-chain shape (paper-and-PDF retention, internal audit logs, baseline-diary records), the institution emits, alongside the §10.24 event:

1. **A §10.39 `chain.successor_attestation` event** with `baseline_manifest_kind = "baseline_diary"`. The `baseline_manifest_sha256` is the SHA-256 of the canonicalized institution-named baseline manifest.
2. **A §10.42 backfill seal record** at acquisition close. The acquirer's HSM signs a v1.0b sign_payload-bound seal record covering the Merkle root of the baseline manifest leaves plus a metadata leaf carrying `seal.backfill_at_close = true`, the window timestamps, the dual_signatures, and the bidirectional companion linkage to the §10.39 event.

The backfill seal IS the cryptographic substrate. A post-close auditor verifies any inherited record's integrity by re-canonicalizing the baseline manifest, re-computing the Merkle root, and confirming the §10.42 seal's HSM signature.

### Operational shape C — mixed inheritance

When the acquired entity inherited records under a foreign-vendor chain for some periods AND under baseline-diary shape for other periods, the institution sets `baseline_manifest_kind = "mixed"` and emits BOTH the §10.40 cross-anchor entries (for the foreign-chain period) AND a §10.42 backfill seal (covering the baseline-diary period). The §10.39 event references both the cross-anchor entries (via the baseline manifest's per-tuple kind) and the §10.42 backfill seal (via `companion_backfill_seal_run_id`).

### Cut-over window discipline (§10.41)

The §10.39 attestation and §10.42 backfill seal are emitted within the cut-over window the institution's CC8.1 names per §10.41 (the chain-coverage-map M&A temporal-slice extension). The window is typically 4-12 weeks. The §10.41 three-partition coverage map (pre-acquisition / cut-over / post-cut-over) is what an 18-month-lookback auditor reads to reconstruct the migration state at any moment of the cut-over.

### Pre-close due diligence

§10.39 / §10.42 detect post-close edits to the inherited records. They do NOT detect pre-close fraud in the baseline manifest's construction. The closure for that residual is *vendor due-diligence on the target*: the buyer's audit firm tests the baseline manifest against external evidence (third-party SOC 2 reports, regulator correspondence, customer-account confirmations) before the acquirer's CISO signs the §10.39 dual_signatures. A target that submitted a fraudulent baseline manifest before close cannot be detected from the chain alone — the discipline is operational, not cryptographic.

### Cross-references

- Spec §10.24 (entity succession — the legal-entity-change event)
- Spec §10.39 (institutional successor-attestation — the cryptographic-inheritance event)
- Spec §10.40 (cross-vendor chain-merge cross-anchor — the foreign-chain inheritance pattern)
- Spec §10.41 (chain-coverage-map M&A temporal-slice extension — the cut-over window)
- Spec §10.42 (backfill seal — the cryptographic complement for baseline-diary inheritance)
- Design `docs/design/12-successor-attestation-and-backfill.md` (the design rationale)
- Test vector `034-successor-attestation` (the §10.39 envelope byte form)
- Test vector `035-backfill-seal` (the §10.42 metadata-leaf and Merkle root byte forms)
