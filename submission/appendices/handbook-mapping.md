# Appendix A &mdash; FFIEC IT Examination Handbook mapping

> **Purpose.** This appendix maps the chain-of-custody primitives to specific control objectives in the FFIEC IT Examination Handbook so a working examiner can confirm which control objectives the chain satisfies and where supplementary evidence is still required.
>
> The full source document with extended commentary is at [`docs/regulator-pack/handbook-mapping.md`](../../docs/regulator-pack/handbook-mapping.md). The structure here is condensed for submission-package use.

---

## A.1 Information Security booklet (IS, September 2016)

| IS Section | Topic | Chain coverage |
|---|---|---|
| II.B | Information security risk identification | Threat model (`docs/design/09-threat-model.md`) enumerates adversaries A, B, C, F and their accepted residuals. |
| II.C.5 | Logical access &mdash; authentication and authorization | Session-key handshake security floor (spec §4.1.1) &mdash; workload identity attestation, mTLS, HSM-issued tokens. |
| **II.C.10** | **Activity logging and integrity (headline mapping)** | **The chain itself.** Per-event HMAC + daily Merkle seal + HSM-rooted signature. **Plus** weekly key-fingerprint reconciliation per spec §10.1; the `master.reconciliation_completed` operational event is the audit-evidence artifact. |
| II.C.11 | Incident response &mdash; detection and response | Verifier anomaly reporting (`docs/design/07-verifier-design.md` §5.1); IR playbook with dedicated scenarios for `key_fingerprint mismatch`, `unknown_key_version`, and `audit_file.truncation_detected` per [`docs/incident-response-playbook.md`](../../docs/incident-response-playbook.md). |
| **II.C.13** | **Cryptographic controls &mdash; encryption and key management** | Ed25519 in HSM custody; HMAC-SHA-256 chain construction. **Plus**: (a) per-entry `key_fingerprint = SHA-256(utf8(tenant_id) \|\| ikm)[:16]` checked before any MAC compute (spec §7 step 8); (b) IKM minimum 32 bytes per spec §10.6; (c) software-key adapter compile-time exclusion per spec §10.7. |
| II.C.20 | Software integrity &mdash; software assurance | Reproducible builds + cosign + GPG manifest; supply chain doc covers SLSA-equivalent properties per [`docs/supply-chain.md`](../../docs/supply-chain.md). |
| III.B | Audit &mdash; audit program | Verifier provides independent audit artifact; conformance corpus at `spec/test-vectors/`. |

**Headline mapping is II.C.10 (Logging).** The IS booklet requires activity logging sufficient for incident detection and forensic investigation. The chain extends this: the logs are not just present, they are *integrity-bearing* &mdash; verifiable by an independent examiner without trusting the institution's logging infrastructure.

The PRD-1 cryptographic-controls deepening (II.C.13) introduces per-entry key identity provenance via `key_fingerprint`. Examiners working II.C.13 should confirm:

1. The institution's IKM length is at least 32 bytes (spec §10.6).
2. The institution's chain entries carry valid `key_fingerprint` bytes the verifier confirms at step 8.
3. The institution's production build does NOT include the software-key adapter (no chain entries with `kms_handle_uri = "plaintext-dev"` in production).
4. The institution operates weekly key-fingerprint reconciliation per spec §10.1.

These extend the cryptographic-controls evidence beyond "HMAC + Ed25519 in HSM custody."

---

## A.2 Architecture, Infrastructure, and Operations booklet (AIO, June 2021)

| AIO Section | Topic | Chain coverage |
|---|---|---|
| II.A.1 | System architecture documentation | Design docs `docs/design/` (10 documents). |
| II.B | Resilience &mdash; availability and continuity | DR/RPO/RTO posture per [`docs/dr-and-resilience.md`](../../docs/dr-and-resilience.md). |
| II.C | Capacity management &mdash; capacity planning | Hot-path budget (spec §5); streaming Merkle for scale per `docs/at-scale-operations.md`. |
| **II.E** | **Change management &mdash; configuration management and change control** | Spec version per event (`ffiec.chain.spec`); chain-stamp `format_version` per entry AND per file header AND per signed seal payload. The `format_version` field is the load-bearing change-management primitive (spec §7 step 1). For algorithm-change events: the institution operates change management on the `algorithm` field, the `signatures` list, and declared algorithm-posture configuration per spec §7 step 11. |
| III.A | Operations &mdash; operational monitoring | Operational events (spec §10.2 catalog including `audit_file.truncation_detected` and `master_key.retired`). |
| IV | Outsourcing dependency &mdash; vendor management | BYOC and vendor-hosted topologies; supply chain; IAM permission matrix. |
| **§VII.D** | **Artificial Intelligence and Machine Learning** | **The booklet currently names AI risks but contains no logging or audit-trail procedure for AI activity. This is the gap PRD-1 closes.** The submission asks the agencies to consider the chain primitive in the next AIO booklet revision's §VII.D, or in an interim sister-agency advisory. |

---

## A.3 Audit booklet (April 2012)

| Audit Section | Topic | Chain coverage |
|---|---|---|
| II | Audit program &mdash; independent assessment | Verifier is operable by internal audit, external audit, or examiner. |
| III | Audit testing &mdash; effective challenge | Conformance corpus + verifier provide testable basis. |
| IV | Audit reporting &mdash; audit findings | Verifier produces standardized PDF + JSON output per spec §10.12. |

---

## A.4 Outsourcing Technology Services booklet (June 2021)

| OTS Section | Topic | Chain coverage |
|---|---|---|
| II | Risk assessment &mdash; vendor risk | Topology-neutral spec; vendor inherits standard third-party-risk-management. |
| III | Selection &mdash; due diligence | Conformance corpus enables vendor evaluation against an objective standard; vendor-conformance attestation registry. |
| IV.B | Contracting &mdash; right to audit | Verifier is the audit artifact; institution-held public key enables independent verification. |
| V | Ongoing monitoring &mdash; vendor performance | Verifier output over time. |

---

## A.5 Cybersecurity Assessment Tool (CAT)

| CAT Domain | Chain coverage |
|---|---|
| Cyber Risk Management and Oversight | Chain-coverage boundary documentation per spec §10.19; CC8.1 control description per §10.18. |
| Threat Intelligence and Collaboration | Threat model named adversaries; supply-chain controls. |
| Cybersecurity Controls | The chain is itself a cybersecurity control covering audit-trail integrity. |
| External Dependency Management | Vendor-conformance attestation registry; cross-vendor anchor patterns per §10.21. |
| Cyber Incident Management and Resilience | IR playbook for chain-detected events; DR posture per `docs/dr-and-resilience.md`. |

---

## A.6 Development, Acquisition, and Maintenance booklet (DA&M, June 2024)

The DA&M booklet revision (the most recent FFIEC handbook update before SR 26-2) emphasizes model-lifecycle integrity touchpoints. The chain provides:

- **Acquisition phase** &mdash; vendor-conformance attestation registry as third-party-risk evidence at acquisition time.
- **Development phase** &mdash; the chain captures development-phase chain entries with full integrity binding (development testing, regulatory_sandbox flags per §4.4.2).
- **Maintenance phase** &mdash; daily verifier runs and chain-anomaly detection; CC8.1 change-management discipline per §10.18.

---

## A.7 Cross-booklet integration

The chain primarily serves the **IS booklet's logging integrity requirement (II.C.10)** and the **AIO booklet's monitoring and resilience requirements**. It supports the Audit booklet by providing an artifact independent audit can use, and the OTS booklet by allowing examination of vendor-hosted implementations through the same verifier. It is the candidate solution for the **AIO booklet's §VII.D AI gap** that the forthcoming OCC/Fed/FDIC AI RFI is expected to address.

## A.8 How to use during an IT examination

1. The examiner identifies which handbook sections are in scope for the engagement.
2. For II.C.10 (and a future §VII.D AI procedure), the chain is the headline evidence &mdash; verifier output is the artifact.
3. For supporting sections, the institution's broader controls are the headline; the chain provides one piece of evidence among several.
4. The examiner combines chain output with other examination evidence to form the overall finding.

**The chain does not replace the Handbook; it satisfies a specific portion of it.**

---

## A.9 Cross-references for working examiners

For the day-of-examination workflow, the regulator-pack documents extend this appendix:

- [`docs/regulator-pack/finding-language.md`](../../docs/regulator-pack/finding-language.md) &mdash; examination-report finding-letter language including repeat-finding and public-disclosure variants.
- [`docs/regulator-pack/sample-report.md`](../../docs/regulator-pack/sample-report.md) &mdash; what a passing examination report looks like.
- [`docs/regulator-pack/examiner-quickstart.md`](../../docs/examiner-quickstart.md) &mdash; the 5-minute orientation.
- [`docs/regulator-pack/examiner-training.md`](../../docs/regulator-pack/examiner-training.md) &mdash; the 30-minute training module.
- [`docs/regulator-pack/deployment-package.md`](../../docs/regulator-pack/deployment-package.md) &mdash; examiner-laptop deployment.
