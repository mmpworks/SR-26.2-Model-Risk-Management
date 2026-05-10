# Story 01 — Northbridge Federal Savings (FFIEC IT Handbook supplementary review, MRA verification revisit)

**Story file:** `docs/auditor-stories/01-northbridge-federal-savings.md`
**Engagement type:** FFIEC IT Handbook supplementary review (post-MRA verification revisit at a ~$45B OCC-supervised national bank with chain-of-custody stack live across customer-facing surfaces for 18 months).
**Posture going in:** External audit team encountering the chain-of-custody stack cold; institution side has been examined twice and closed an OCC MRA on customer-data integrity two quarters earlier.
**Outcome posture:** Confirmation — sixteen confirmations, one §10.16 non-conformance.

## Type of audit
A FFIEC IT Handbook supplementary review framed as a verification revisit: the bank closed an OCC MRA on customer-data integrity two quarters earlier, and this engagement is scoped to confirm the close held. What makes it distinctive is that the institution has run a full chain-of-custody stack across every customer-facing surface for 18 months and the external audit team encounters the stack cold at kickoff.

## Interested parties (spec readers)
- **FFIEC IT Examiner (FDIC / OCC / FRB)** — single-tenant baseline engagement; cycle examiner reading for first-time orientation, finding language, and report production against an institution that closed an OCC MRA cleanly.
- **FFIEC Examiner-in-Charge (EIC)** — examination logistics, repeat-finding posture, and bank-management communication when the prior MRA close is being verified.
- **Audit Committee chair** — board-level read of a clean-baseline engagement; relies on verifier output without needing to be cryptographer.
- **Chief Audit Executive (CAE)** — institution-side counterpart; signs the engagement letter, partners with external auditors, briefs the audit committee.
- **Internal audit team** — independent verification of chain controls; the canonical CAE-side readers exercising verifier procedures and §10.13 evidentiary-artifact retention.
- **Financial-statement auditor** — ICFR support; chain entries used as control-evidence inputs to financial-statement audit.
- **Reference-verifier user / OSS adopter** — reads to see how a published verifier is operated routinely against a single-tenant deployment with three independent custody layers.
- **DevSecOps / SRE on-call** — operator-side read of a live seal job that has been demonstrated to examiners on multiple cycles.

## Top spec sections used
- **§4.4 / §4.4.6** — chain-envelope attribute table and SaaS-edge connector_source family binding the CRM CDC mirror's `replay_id`, `commit_timestamp`, `commit_user`, `lag_observed_ms`, and `change_kind` under the per-event MAC.
- **§7** — the 12-step verification procedure that grounds every `herald-verify` PASS, the `--explain` trace, and the `expected_prev_hash` discipline.
- **§10.16** — the SaaS-edge mirror lag-bound clause whose normative severity-classification is the entire engagement's single Finding (downgrade prohibited).
- **§10.25** — three-place tail acquisition, single-writer-per-run lock, ledger ingestion cross-check, genesis-form anti-spoof, and fork detection — the spine of the silent-restart and fork-detection demos.
- **§4.4 + §1.4 compositional security** — the SDK / sink / verifier three-independent-layer refusal of duplicate-genesis bytes, with `HeraldComplianceErrorCode` 5060/5061/5062/5063.
- **§10.26** — verifier OSS distribution, separate repo, Cosign-signed releases, and the CC8.1 three-name citation discipline.
- **§5 / §5.2** — the canonical-form exclusion list and the captured-JSON-vs-canonical-bytes split that grounds the FRE 1001(d) best-evidence posture.
- **§10.5 + §10.7 + §10.13** — FIPS 140-2 Level 3 HSM custody, software-key adapter exclusion, and the object-lock retention window in a separate trust boundary.

## All cited spec sections
- **§0** — document-version vs wire-format-version separation; PRD-N to PRD-(N+1) stability.
- **§1.1** — Daubert four-factor framing in the spec text.
- **§1.2** — epistemic scope (chain proves integrity, not truth or policy compliance).
- **§1.3** — security definitions and 128-bit effective security.
- **§1.4** — compositional security across three independent custody layers (operationalized in the silent-restart demo).
- **§3** — definitions table; tenant_id character class enforced at SDK and verifier.
- **§4.1** — Primitive 1 HMAC chain at capture.
- **§4.1.3** — per-event MAC algorithm agility (HMAC-SHA-256 fixed at v1.0b).
- **§4.2** — Primitive 2 daily Merkle seal (empty-day posture is well-defined).
- **§4.2.1** — daily cadence default.
- **§4.2.2** — day-boundary semantics by `received_at` UTC; `late_binding=true` for late entries.
- **§4.3** — HSM-rooted root signature; v1.0b 12-line `sign_payload` form.
- **§4.3.2** — algorithm rotation and dual-algorithm post-quantum posture.
- **§4.4** — OTel-native wire and chain-envelope attribute table; genesis-block uniqueness.
- **§4.4.1** — AI-routing event family.
- **§4.4.2** — deployment-intent enum (production / canary / A-B).
- **§4.4.3** — OTLP transport identification with required Resource attributes.
- **§4.4.4** — severity for chain traffic; collectors MUST NOT severity-filter.
- **§4.4.6** — SaaS-edge connector source attribution (six normative attributes, stable run_id rule).
- **§5** — canonical-form exclusion rule, RFC 8785 JCS over the event.
- **§5.2** — captured JSON content-bearing, canonical bytes integrity-bearing; both originals under FRE 1001(d).
- **§7** — 12-step verification procedure with named steps 6, 8, 9, 11, 12a.
- **§10.5** — HSM custody at FIPS 140-2 Level 3+.
- **§10.6.1** — IKM CSPRNG generation requirements.
- **§10.7** — software-key adapter exclusion in production; verifier `--strict` refusal of `dev_mode=true`.
- **§10.8** — constant-time comparison MUST.
- **§10.10** — IKM rotation crossing the seal boundary.
- **§10.11 / §10.11.1 / §10.11.2** — ECOA translation, ECOA adverse-action reasons, FCRA reinvestigation timing (with FCRA §611's 30-day clock as the regulatory anchor).
- **§10.12** — verifier exit-code contract (0/1/2/3 each exercised in the engagement).
- **§10.13** — evidentiary-artifacts retention list.
- **§10.14** — trusted-time integration (HSM monotonic time vs application clock).
- **§10.15** — multi-region resilience Pattern A active-active.
- **§10.16** — SaaS-edge mirror connector lag bounds; severity-classification clause is normative; the Finding-001 anchor.
- **§10.17** — HSM partition ceremony attestation.
- **§10.18** — CC8.1 cross-referencing of operational runbooks to spec sections.
- **§10.19** — chain-coverage boundary documentation.
- **§10.20** — training-data retention vs deployment-window discipline.
- **§10.21** — cross-vendor model-handover schema.
- **§10.22** — pre-MAC redaction discipline.
- **§10.23** — consumer-correlation index integrity.
- **§10.24** — entity succession.
- **§10.25** — run resume and chain-tail acquisition (three-place lookup, single-writer lock, ingestion cross-check, fork detection).
- **§10.26** — reference verifier distribution discipline.
- **§11** — references; spec pins reference verifier version.

## Synopsis

### Audit activity
The external audit team walked the database schema, IAM elevation patterns, the API layer, the data pipeline, multi-region reconciliation, a live seal job, and a stress test of fifteen-plus verifier runs across regions, event classes, and a key-rotation boundary. Per-event MAC recomputes spanned two CloudHSM rotation boundaries; IAM auto-revocation was confirmed chain-driven rather than cron-driven; a CRM CDC event was reconciled side-by-side against its chain entry; the silent-restart and fork-detection attack class was exercised against a sandbox tenant.

### How the spec was used

- **§4.4 / §4.4.6** — Connector attribute family verified byte-for-byte.
- **§5** — Canonical-form exclusion list anchored.
- **§7** — 12-step verifier procedure executed.
- **§10.25** — Three-layer silent-restart refusal exercised.
- **§10.26** — Verifier-distribution rationale grounded.
- **§1.4** — Compositional security operational across three independently-owned code paths.
- **§10.16** — Normative severity-classification clause generated the engagement's headline finding (no engagement-team discretion to downgrade imprecise lag wording).

### Results
Sixteen confirmations, zero Gaps, zero Partials, zero Nits, and one non-conformance (Finding-001) per §10.16: the CRM mirror runbook describes the connector as "near real-time" without naming the four quantified bounds (median, 95th-percentile SLO, alerting threshold, RTO) the spec requires. The connector itself is operating correctly — reconciliation diff was zero across three independent samples including a known-noisy day — but the wording IS the testable claim and §10.16 prohibits downgrade.
