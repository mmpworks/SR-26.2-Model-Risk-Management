# Story 13 — Saraswati Microfinance (Indian NBFC, edge-AI federated learning across 15,000 ruggedized Android tablets)

**Story file:** `docs/auditor-stories/13-saraswati-microfinance.md`
**Engagement type:** Three-day pre-engagement readiness pass before RBI's IT Governance Master Direction inspection (nine weeks out)
**Posture going in:** Chained in production for 4 months on the central-inference path; edge-AI integrity is the engagement question (15,000 field-officer tablets across 1,800 branches in seven Indian states, offline-first, monthly federated-learning model updates)
**Outcome posture:** WISHLIST; surfaces §10.32-§10.38 edge / federated / training-phase family; the institution exercises every section in production and becomes the canonical federated-learning microfinance reference

## Type of audit
Three-day engagement at the institution's BKC Mumbai headquarters with the team split geographically across Mumbai-onsite and US-Eastern video bridge during the late-evening IST overlap window. Three regulatory regimes overlap: RBI IT Governance Master Direction (2024 update with explicit AI-governance expectations), DPDP Act 2023, and the institution's NIST AI RMF mapping for international funders. The architecture is structurally distinct from prior engagements (chain-in-motion at the device, in-flight on cellular, sealed at the center), so the spec sections are read against operational reality at three integrity surfaces (central inference path, edge inference path, federated-learning aggregator).

## Interested parties (spec readers)
- **RBI + DPDP DPO** — India microfinance + edge-AI consent capture; primary regulator audience
- **Chief AI / ML Officer** — Owner of the federated-learning program and the deployment-intent capture across edge and center
- **Privacy Officer / DPO** — DPDP Act §6 consent lifecycle (§10.38) bound to every credit-decision chain entry
- **AI vendor product-engineering team** — Edge SDK on Android, hardware-backed Keystore session keys, federated aggregator
- **Standards-body reviewer** — Edge / federated wishlist memo feeds the §10.32-§10.38 sub-track
- **SDK implementer** — Per-device session key derivation (§10.32), edge-attestation primitive (§10.35), late-arrival seal (§10.36)
- **Ledger implementer** — Hierarchical Merkle aggregation (§10.37) with per-device root as a leaf in the daily seal
- **Verifier implementer** — Edge-leg verifier dispatch across the three integrity surfaces
- **CISO** — TEE attestation as partial compensation for the §1.2 SDK-process-compromise residual on bring-your-own-device-class endpoints
- **Internal audit team** — Reconciliation discipline across edge / boundary / center legs

## Top spec sections used
- **§10.32** — Per-device session key derivation (`HKDF_INFO_BASE || '|' || tenant_id || '|' || device_id`); exercised across 15,000 tablets
- **§10.33** — Model-update events (`audit.model_update.push/pull/verify/activate`); the deployment-phase boundary moments of the monthly federated cycle
- **§10.34** — Training-phase integrity (`audit.training.local_gradient/aggregation/validation/model_artifact`); the federated-learning cycle's training activity
- **§10.35** — Edge-attestation primitive; chain entries carry `ffiec.chain.attestation` with Android Keystore TEE attestation document
- **§10.36** — Late-arriving-entry seal discipline; Pattern A supplemental seal for offline-first field-day workflows
- **§10.37** — Hierarchical Merkle aggregation; per-device root as a leaf in the daily seal's Merkle tree
- **§10.38** — Consent capture for DPDP Act 2023 §6; `audit.consent.given/referenced/withdrawn/expired` with `legal_basis = "dpdp_act_2023_§6"`
- **§4.1** — Per-tenant HKDF binding that §10.32 extends with the per-device sub-component

## All cited spec sections
- **§0.5.4** — Five-minute path (the §1.2 lists, the §4 four primitives, the §13 stakeholder entry); canonical short-path answer for the RBI assessor or DPDP DPO
- **§1** — Scope including training-phase integrity normatively
- **§1.2** — Epistemic scope; the SDK-process compromise residual partially compensated by Android Keystore TEE attestation under §10.35
- **§4** — Four primitives
- **§4.1** — Per-tenant HKDF base derivation that §10.32 extends per-device
- **§4.2** — Daily Merkle seal; per-tenant-day on UTC calendar boundaries
- **§4.4.2** — Deployment-intent attribute carrying `audit.deployment.model_version`
- **§6** — Storage append-only mandatory
- **§7** — Twelve-step verifier procedure; rotation handling at §7 step 7
- **§10.10** — IKM rotation crossing the seal boundary (tablet retirement case)
- **§10.11** — Adverse-action notice translation (referenced by contrast for DPDP-specific consent capture)
- **§10.19** — Chain-coverage map; RBI documentation requirement
- **§10.21** — Cross-anchor links between deployment-phase (§10.33) and training-phase (§10.34) chain entries
- **§10.23** — Consumer-correlation-index integrity (referenced as the existing privacy-regime composition pattern)
- **§10.27** — Streaming cadence (cited in contrast)
- **§10.31** — Per-cohort subtree disclosure (cited in contrast)
- **§10.32** — Per-device session key derivation
- **§10.33** — Model-update events as chain entries
- **§10.34** — Training-phase integrity (`audit.training.*` family)
- **§10.35** — Edge-attestation primitive
- **§10.36** — Late-arriving-entry seal discipline (Pattern A supplemental seal)
- **§10.37** — Hierarchical Merkle aggregation
- **§10.38** — Consent capture for DPDP Act
- **§10.64** — Training-run code-and-config chain primitive that §10.34 specializes for the federated case
- **§13** — Stakeholder navigation; "edge-deployed federated-learning institution" candidate stakeholder

## Synopsis

### Audit activity
Day 1 begins at the BKC office with an architecture walk: central inference path (server-side, full chain coverage), edge inference path (offline-first SQLite buffering, per-event MAC at capture, hardware-backed Android Keystore session key), federated-learning aggregator (monthly cycle, central pushes new global model on Day 29, tablets pull / verify / activate).

A representative field trace makes the integrity-claim asymmetry concrete: a 14:24 IST credit decision at a rural branch, tablet offline until evening when the field officer reaches a connected branch, central seal cuts at 23:00 UTC the next morning IST; up to 15 hours of integrity-claim asymmetry between per-event MAC and seal completion. Day 1's evening video bridge surfaces the edge-attestation document idea (§10.35) and the bandwidth-efficient hierarchical Merkle proof (§10.37).

Day 2 reconciles ten credit decisions across the diversity matrix (rural vs urban, pre / post-rollout, retired-tablet, disputed override, KYC-failed, repaying-on-schedule, declined-then-complained); ten-of-ten chain traces complete with full integrity claims. Day 3 delivers the spec-section confirmation memo at 09:00 IST.

### How the spec was used

- **§10.32** — Per-device HKDF extension (`HKDF_INFO_BASE || '|' || utf8(tenant_id) || '|' || utf8(device_id)`) normated so a compromised device's session key cannot forge entries for any other device, and so the next federated-learning institution does not have to roll its own
- **§10.33** — Captures the federated cycle's deployment-phase boundary moments (push / pull / verify / activate) so an examiner reads which model was active at the moment of decision directly from the chain
- **§10.34 / §1** — Lifts training-phase integrity into normative scope alongside inference-phase; the `audit.training.*` family covers `local_gradient` (privacy-preserving via hash, no underlying data), `aggregation`, `validation` against held-out test set, `model_artifact` production
- **§10.35 / §1.2** — Edge-attestation document binds device hardware-integrity state at every chain-entry production — a real strengthening of the §1.2 SDK-process-compromise residual
- **§10.36** — Pattern A supplemental seal handles tablet uploads that arrive after the daily-seal cut
- **§10.37** — Two-level Merkle (per-device Merkle root as a leaf in the daily seal) gives bandwidth efficiency for week-long no-cellular periods
- **§10.38** — `audit.consent.*` lifecycle binds DPDP Act §6 obligations to every credit-decision chain entry touching an Indian borrower
- **§10.64** — Normates the broader training-run code-and-config chain primitive that §10.34 specializes for the federated case

### Results
Seven spec-section confirmations filed in compliance-track records and cited in the institution's CC8.1 control description. No findings. The institution becomes the canonical federated-learning microfinance institutional reference. The architecture's three integrity legs (edge / boundary / center) map to the seven sections cleanly: edge-side §10.32 + §10.35 + §10.37, boundary §10.33 + §10.36, center §10.34 + §10.38. Test vectors `024-033` are the byte-identical references; `024-per-device-derivation` is the §10.32 reference. The RBI IT Governance inspection in nine weeks consumes the spec-section confirmation memo as part of the institution's CC8.1 control description; the institution's posture is defensible at full conformance across §10.32-§10.38 with each section operationally exercised in production.
