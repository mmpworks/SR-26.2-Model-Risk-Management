# Appendix B &mdash; Control overlay (NIST CSF 2.0 / FS AI RMF / SR 26-2 / DORA / NYDFS Part 500)

> **Purpose.** This appendix consolidates the chain-of-custody primitive's mappings to current-and-emerging control frameworks the receiving body's working group is likely to weigh against. The full overlay set lives in [`docs/regulator-pack/`](../../docs/regulator-pack/).

---

## B.1 NIST Cybersecurity Framework 2.0

Source: [`docs/regulator-pack/CSF-2.0.md`](../../docs/regulator-pack/CSF-2.0.md).

| CSF Function | Chain contribution |
|---|---|
| **GOVERN** (GV) | Chain-of-custody policy; working-group involvement; foundation-transfer trajectory; vendor-conformance attestation registry; chain-coverage boundary documentation per spec §10.19. |
| **IDENTIFY** (ID) | Threat model (`docs/design/09-threat-model.md`); risk inventory anchoring on the chain-coverage boundary; cross-vendor inventory per §10.21. |
| **PROTECT** (PR) | Per-event MAC, daily Merkle seal, HSM-rooted signature; the §10 operational requirements (HSM custody §10.5, IKM custody, append-only enforcement §10.3, time sync §10.4, key-fingerprint reconciliation §10.1). |
| **DETECT** (DE) | Daily verifier runs; chain-anomaly events surface as exit-code-3 detections per §10.12; operational-events catalog per §10.2. |
| **RESPOND** (RS) | IR playbook for chain-detected events; legal-disclosure posture per [`docs/legal-disclosure.md`](../../docs/legal-disclosure.md); anomaly-documentation discipline per [`docs/anomaly-documentation-template.md`](../../docs/anomaly-documentation-template.md). |
| **RECOVER** (RC) | DR/resilience posture per [`docs/dr-and-resilience.md`](../../docs/dr-and-resilience.md); run-resume / chain-tail acquisition per §10.25; multi-region resilience per §10.15. |

---

## B.2 Treasury Financial Services AI RMF

Source: [U.S. Treasury FS AI RMF v1](https://home.treasury.gov/news/press-releases/sb0401) (released February/March 2026), 230 control objectives.

The chain composes alongside FS AI RMF; it does not replace any of its 230 control objectives. The chain provides the **audit-trail integrity substrate** the FS AI RMF presupposes for control families touching:

| FS AI RMF lifecycle phase | Chain contribution |
|---|---|
| Govern | Audit-trail integrity policy; working-group involvement; foundation-transfer trajectory. |
| Map (lifecycle inventory and risk identification) | Chain-coverage boundary per §10.19; cross-vendor inventory per §10.21. |
| Measure (model performance and risk testing) | `audit.disparate_impact.*` and `audit.underwriting.features.*` per §4.4.5; deployment-intent capture per §4.4.2. |
| Manage (risk treatment and mitigation) | Override and human-in-the-loop capture via `audit.routing.*` and `audit.deployment.*`; anomaly response per IR playbook. |
| Data lifecycle | Inference-phase IN scope; **training-phase explicitly OUT of scope for v1.x** per spec §1 scope boundary. |
| Model lifecycle | Cross-vendor model-handover per §10.21; run resume / chain tail per §10.25. |
| Third-party risk | Vendor-conformance attestation registry per [`GOVERNANCE.md`](../../GOVERNANCE.md); no vendor as single point of trust. |

---

## B.3 SR 26-2 / OCC Bulletin 2026-13 (April 17, 2026)

The revised model-risk-management framework keeps the audit-trail expectation from SR 11-7 and explicitly excludes generative and agentic AI from scope. The chain composes:

| SR 26-2 expectation | Chain contribution |
|---|---|
| Robust development, validation, ongoing monitoring | The chain is the evidence substrate; the institution's validation and monitoring programs supply methodology. |
| Independent validation and effective challenge | The verifier provides independent verification; effective challenge of audit-trail integrity becomes deterministic. |
| Documentation allowing independent re-execution | §10.13 evidentiary artifacts; full event-by-event integrity binding. |
| Governance of model-risk inventory | Chain-coverage boundary per §10.19. |
| Vendor-model risk management | Vendor-conformance registry; cross-vendor anchor patterns per §10.21. |
| Override and human-in-the-loop documentation | `audit.routing.*`, `audit.deployment.*`. |
| Customer-facing adverse-action documentation | §10.11 ECOA / state-insurance translation; §10.11.1 ECOA reasons schema; §10.11.2 FCRA §611 timing. |

What the chain does NOT provide for SR 26-2: model-validation methodology, bias-testing methodology, policy-compliance evaluation, training-data integrity (out of v1.x scope).

---

## B.4 NYDFS Cybersecurity Regulation (Part 500)

Source: [`docs/regulator-pack/nydfs-part500-overlay.md`](../../docs/regulator-pack/nydfs-part500-overlay.md).

| Part 500 Section | Chain contribution |
|---|---|
| §500.6 (Audit Trail) | Direct mapping; the chain is the audit-trail integrity layer. |
| §500.7 (Access Privileges) | HSM custody and IKM custody discipline. |
| §500.11 (Third Party Service Provider Security Policy) | Vendor-conformance attestation; cross-vendor anchors. |
| §500.16 (Incident Response) | IR playbook; chain-detected events surfacing as exit-code-3 detections. |
| §500.17 (Notices to Superintendent) | Anomaly-documentation discipline supports breach-notification framework. |

---

## B.5 EU DORA articulation

Source: [`docs/regulator-pack/dora-articulation-overlay.md`](../../docs/regulator-pack/dora-articulation-overlay.md).

| DORA Article | Chain contribution |
|---|---|
| Art. 5-6 (ICT risk management framework) | Chain-coverage boundary; threat model; CC8.1 discipline. |
| Art. 8 (Identification) | Chain-coverage boundary documentation per §10.19. |
| Art. 9 (Protection and prevention) | The §10 operational requirements; HSM custody. |
| Art. 10 (Detection) | Daily verifier runs; operational-events catalog. |
| Art. 11 (Response and recovery) | IR playbook; DR posture; run-resume per §10.25. |
| Art. 17-18 (ICT-related incident management and reporting) | Chain-detected event reporting; anomaly-documentation. |
| Art. 28-29 (Third-party risk) | Vendor-conformance registry; cross-vendor anchors. |
| Art. 30 (Contractual arrangements) | Right-to-audit via verifier; institution-held public key. |

---

## B.6 GDPR (Article 32 + the family)

Source: [`docs/regulator-pack/gdpr-*.md`](../../docs/regulator-pack/) (full family).

| GDPR Article | Chain contribution |
|---|---|
| Art. 5 (principles relating to processing) | Integrity binding supports the integrity-of-processing principle (Art. 5(1)(f)). |
| Art. 6 (lawfulness of processing) | Lawful basis captured per [`gdpr-lawful-basis.md`](../../docs/regulator-pack/gdpr-lawful-basis.md). |
| Art. 16 (right to rectification) | Per [`gdpr-article-16-rectification.md`](../../docs/regulator-pack/gdpr-article-16-rectification.md). |
| Art. 17 (right to erasure) | Append-only chain accommodates erasure via tombstone + tokenization pattern; see [`gdpr-article-17-procedures.md`](../../docs/regulator-pack/gdpr-article-17-procedures.md). |
| Art. 25 (data protection by design) | Per [`gdpr-article-25-demonstrability.md`](../../docs/regulator-pack/gdpr-article-25-demonstrability.md); the chain is the demonstrability substrate. |
| Art. 32 (security of processing) | Direct mapping per [`article-32-security-mapping.md`](../../docs/regulator-pack/article-32-security-mapping.md). |
| Art. 35 (DPIA) | DPIA template per [`gdpr-dpia-template.md`](../../docs/regulator-pack/gdpr-dpia-template.md). |
| Art. 44-50 (international transfers) | Cross-border-transfer family (`audit.cross_border_transfer.*`) per spec §4.4.4; per [`international-transfers.md`](../../docs/regulator-pack/international-transfers.md). |

---

## B.7 SOC 2 Trust Services Criteria

Source: [`docs/control-map/TSC-mapping.md`](../../docs/control-map/TSC-mapping.md).

| TSC criterion | Chain contribution |
|---|---|
| CC2.1, CC4.1, CC4.2 (Information / Monitoring) | Chain artifacts are the monitoring substrate. |
| CC5.1, CC5.2 (Control activities) | The §10 operational requirements. |
| CC6.1, CC6.6, CC6.7 (Logical/physical access) | HSM custody, IKM custody, append-only enforcement. |
| CC7.2, CC7.3, CC7.4 (Detection of anomalies and incidents) | Verifier exit codes 1, 2, 3. |
| CC8.1 (Change management) | The CC8.1 control description per spec §10.18. |
| A1.1-A1.3 (Availability) | DR posture per [`docs/dr-and-resilience.md`](../../docs/dr-and-resilience.md). |
| C1.1, C1.2 (Confidentiality) | Transport encryption; tokenization; redaction. |
| PI1.1-PI1.5 (Processing integrity) | The chain itself. |
| P1-P9 (Privacy) | Privacy-by-design; redaction; consumer-correlation index. |

---

## B.8 Cross-framework integration

The chain composes consistently across NIST CSF 2.0, Treasury FS AI RMF, SR 26-2 / OCC 2026-13, NYDFS Part 500, EU DORA, GDPR, and SOC 2 TSC. Institutions running multiple frameworks in parallel use the same chain artifacts as the evidence substrate for each.

This cross-framework consistency is the **portfolio benefit** of adopting the chain: one audit-trail integrity layer supports many compliance regimes simultaneously, rather than one bespoke audit-trail per regime.
