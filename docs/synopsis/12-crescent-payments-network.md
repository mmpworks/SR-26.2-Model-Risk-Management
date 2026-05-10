# Story 12 — Crescent Payments Network (US payments network ahead of OCC + Fed + nine state examiners + FTC inquiry)

**Story file:** `docs/auditor-stories/12-crescent-payments-network.md`
**Engagement type:** Pre-engagement readiness pass before a coordinated multi-regulator examination cycle
**Posture going in:** Chained in production for 8 months; sub-100ms decision time, billions of decisions per day; the streaming-mode design points already operational
**Outcome posture:** WISHLIST; surfaces §10.27-§10.31 streaming-mode family; the engagement is the canonical streaming-mode reference and confirms the spec sections were forward-thinking enough to anticipate institutions on this clock

## Type of audit
Two-day pre-engagement readiness pass at the network's hardened West Valley City Operations Center before the OCC + Federal Reserve, nine issuing-bank state examiners (NY DFS, CA, TX, MA, NC, IL, PA, FL, GA), and an FTC inquiry on a publicized chargeback dispute. The deliverable is a spec-section confirmation memo handed to the OCC team on Wednesday morning. The institution runs a per-second seal cadence in production across three regions for AI fraud-decisioning at ~250,000 chain entries per second peak, ~12 billion entries per day; the engagement confirms the spec's streaming-mode design points operate end-to-end at scale under live regulator review.

## Interested parties (spec readers)
- **FFIEC IT Examiner (FDIC / OCC / FRB)** — Cycle examiner; consumes the spec-section confirmation memo first; runs the streaming-mode verifier against the live production stream
- **Federal Reserve / OCC payments examiner** — Cross-institution Fedwire / ACH chain integrity (§10.21.3, §10.71)
- **FFIEC Cybersecurity Specialist Examiner** — NIST CSF alignment, threat model on the streaming-mode capture path
- **FTC AI / privacy examiner** — UDAP enforcement on the AI-driven decline path; routing-decision evidence
- **CISO** — Streaming-mode threat surface; HSM cadence under sub-daily seal
- **Model Risk Management chair** — SR 11-7 substrate under per-second cadence; deployment-intent capture for the GBM/transformer/GNN ensemble
- **Standards-body reviewer** — Streaming-mode wishlist memo feeds the next PRD
- **SDK implementer** — Streaming-mode capture path at sub-millisecond p99 budget
- **Ledger implementer** — Per-second Merkle-seal job, HSM cadence, multi-region reconciliation
- **Verifier implementer** — Streaming-mode subprocedure, exit-code contract extended with codes 4 / 5 / 6

## Top spec sections used
- **§10.27** — Configurable seal cadence (per-second through weekly); the institution runs `"per_second"`; the headline confirmation
- **§10.29** — Streaming-mode verifier subprocedure; OCC team will exercise it themselves with incremental PASS / FAIL verdicts
- **§10.30** — Trusted-time integration normative for sub-daily cadence; GPS-disciplined PTP across three regions
- **§10.31** — Per-cohort subtree disclosure; nine state examiners pull nine concurrent subtrees against the same single signed Merkle root
- **§10.28** — Streaming-mode IKM rotation discipline; production rotation completed in one second of two-key-version sealing
- **§10.12** — Verifier exit-code contract extended with streaming-state codes 4 (all-pass-so-far), 5 (anomaly), 6 (rotation-pending)
- **§7** — Twelve-step procedure with streaming-mode subprocedure
- **§10.71** — Cross-institution Fedwire / ACH chain integrity; cited for the Fed side of the room

## All cited spec sections
- **§0.5.1** — Three-paragraph elevator pitch for executive-level orientation
- **§1.2** — Epistemic scope; the §1.2 fourth-class adversary (SDK-process compromise) becomes a tighter window for the seal-job under streaming
- **§4** — Four primitives; in-process observation explicitly NOT a spec-conformant view
- **§4.2** — Daily Merkle seal default cadence (overridden to per-second per §10.27)
- **§4.3** — HSM-rooted root signature; cadence bound under `sign_payload`
- **§7** — Twelve-step verifier procedure; streaming-mode subprocedure under §10.29
- **§10** — Operational requirements normative surface
- **§10.2** — Operational events; `clock.drift_detected` fires three times in eight months
- **§10.10** — IKM rotation crossing the seal boundary; designed for daily, extended by §10.28 for sub-daily
- **§10.12** — Verifier exit-code contract (0 / 1 / 2 / 3) extended with streaming codes 4 / 5 / 6 per §10.29
- **§10.14** — Trusted-time integration RECOMMENDED at v1.0; informative until §10.30 lifts to normative for streaming
- **§10.15** — Multi-region resilience; coordinated reconciliation Pattern A across three regions
- **§10.27** — Configurable seal cadence per-second through weekly
- **§10.28** — Streaming-mode IKM rotation discipline at cadence-interval boundaries
- **§10.29** — Streaming-mode verifier subprocedure with incremental verdicts
- **§10.30** — Trusted-time integration normative for sub-daily cadence
- **§10.31** — Per-cohort subtree disclosure (per-issuer slices for the nine state examiners)
- **§10.71** — Cross-institution Fedwire / ACH integrity with `cross_anchor_state` enum
- **§13** — Stakeholder navigation; "real-time-decisioning institution" candidate stakeholder

## Synopsis

### Audit activity
Day 1 at the hardened Operations Center walks the fan-out architecture: every authorization hits a routing layer, three model-serving regions (West Coast / Central / East Coast), each region runs a GBM + transformer + GNN ensemble within a 100ms decision budget. SDK-side latency is 0.4ms per chain entry at p99; chain stamping fits inside ~1.6ms of the 100ms budget.

The whiteboard reconciliation walks ten transactions including the FTC-inquiry tap-to-pay; per-event MAC verifies in isolation for all ten; for one transaction (this morning's), the seal will be tomorrow at 02:15 UTC under the daily-seal default — the gap that drives the streaming conversation.

The institution runs per-second seal cadence in production. ~250,000-leaf Merkle trees at peak; HSM signing on AWS CloudHSM `us-east-1` with replicas in `us-west-2` and `us-east-2`; ~86,400 Ed25519 signatures per region per day. Day 2 runs the §10.15 multi-region reconciliation walk and finalizes the spec-section confirmation memo by 4 PM.

### How the spec was used

- **§10.27** — Configurable cadence (`per_second` through `weekly`) is the headline; cadence recorded in every seal record's `cadence` field bound under `sign_payload`
- **§10.28** — Governs the production IKM rotation that completed at 03:14 UTC across all three regions; cadence-interval crossing the rotation event sealed under both prior and new key generations with `key_versions: [4, 5]`
- **§7 step 7** — Verifier dispatched per-entry `key_version` lookup across the rotation boundary
- **§10.29** — Normates the streaming verifier subprocedure consuming the live chain stream and producing incremental PASS / FAIL
- **§10.12** — Streaming codes 4 / 5 / 6 carry the incremental verdicts
- **§10.30** — Trusted-time integration normative for sub-daily cadence (GPS-disciplined master clock per region, NIST-traceable PTP fanned out to model-serving hosts, median fleet drift 18 microseconds, alerting threshold 100ms, three `clock.drift_detected` events fired and re-synced in under two minutes)
- **§10.31** — Partial-disclosure mode produces nine per-issuing-bank subtrees concurrently against the same single signed Merkle root
- **§10.71** — Cited for the Fed-side cross-institution Fedwire / ACH chain integrity story

### Results
Five-section spec-section confirmation memo delivered Wednesday morning before OCC arrival, with the §10.27-§10.31 confirmations cited in CC8.1 control description. No findings.

The deployment becomes the canonical streaming-mode reference institution: daily-cadence institutions remain the spec default, streaming-mode institutions opt in. Test vector `020-streaming-seal-cadence-1s` is the byte-identical reference; the OCC team can run their own streaming-mode verifier against the live production stream and produce byte-identical incremental verdicts.

Message to OCC: per-event integrity at capture, per-second cross-event integrity, FFIEC IT Handbook logging-integrity bar met, SR 26-2 audit-trail expectations for AI-based models met. The single remaining adjacent capability is §10.71 cross-institution Fedwire / ACH chain integrity, for which this institution is the natural canonical-adjacent reference.
