# FFIEC AI Chain-of-Custody &mdash; Proposed Standard

> **Status:** Public Review Draft 2 (PRD-2) &mdash; document version `0.2.0`. **This is a public-comment draft, not a finalized standard.**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-public%20review%20draft-orange.svg)](spec/chain-of-custody-DRAFT-0.2.0.md)
[![Spec](https://img.shields.io/badge/spec-PRD--2-informational.svg)](spec/chain-of-custody-DRAFT-0.2.0.md)

---

A proposed open standard for tamper-evident logging of AI-driven decisions in regulated financial institutions. Prepared as a comment-letter response to the model-risk-management framework revision announced in [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) / [OCC Bulletin 2026-13](https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html) (April 17, 2026) and the forthcoming AI RFI named there.

## What this is

The FFIEC IT Examination Handbook already mandates that audit logs be **tamper-evident, integrity-protected, immutable, and complete** (Information Security booklet; Architecture, Infrastructure, and Operations booklet). The AIO booklet's §VII.D names the risks of AI in production but contains **no logging or audit-trail procedure for AI activity**. This proposal closes that gap with four primitives, language-neutral and vendor-neutral:

1. **HMAC chain at capture** &mdash; every AI decision event is hashed with a per-process session key derived via HKDF; each event includes the SHA-256 of the previous event in the same run.
2. **Daily Merkle seal** &mdash; events for each tenant per UTC calendar day are aggregated into an RFC 6962 Merkle tree; the root is published in an append-only ledger.
3. **HSM-rooted root signature** &mdash; the daily Merkle root is signed in HSM custody (FIPS 140-2 Level 3 or higher). The signing key is non-extractable.
4. **OpenTelemetry-native wire** &mdash; events ship over OTLP using standard OpenTelemetry attributes plus the chain extension fields.

The four primitives compose into a chain of custody an examiner can independently walk &mdash; with a single verifier binary, against the institution's exported chain artifacts, on the examiner's own laptop, **without trusting the institution's vendor or operations team**.

## What this proposal proves and does not prove

**The chain proves:**

- *What* the AI said at a specific time (the captured event records the model's response, the prompt, the tools called, the routing decision, the operational state at capture).
- That the record was *not tampered with after capture*.

**The chain does not prove:**

- That the AI's statement is factually accurate.
- That the AI's statement complied with policy.
- That the AI's statement is free of bias.

These three are separate questions answered with evidence outside the chain (the institution's policy library, fair-lending review, statistical bias testing, model-risk-management program). The chain is the **integrity foundation**, not the truth foundation.

## Repository contents

| Path | Purpose |
|---|---|
| [`spec/`](spec/) | Normative specification (PRD-2, `0.2.0`) and the byte-equivalence test-vector corpus. |
| [`spec/test-vectors/`](spec/test-vectors/) | Conformance corpus: positive vectors (001, 002, 003, 008, 010, 015&ndash;019, plus the §10 family) and negative vectors (N001 through N022). |
| [`submission/`](submission/) | The public-comment submission package &mdash; cover letter, executive summary, proposal body, and appendices A&ndash;C (handbook mapping, control overlay, test-vector corpus summary). |
| [`docs/`](docs/) | Audience-segmented supporting documentation: regulator-pack overlays (FFIEC, NIST CSF 2.0, NYDFS Part 500, DORA, GDPR, HIPAA, BSA/AML, FedRAMP, APAC/Korea/Bank of Israel, CFPB), SOC pack, control map, audit procedures, incident-response playbook, customer-dispute procedures, M&amp;A handoff, edge/federated AI, cryptographic-agility roadmap, and audience briefs (CEO, audit committee, MRM committee, vendor management, privacy team, legal/IR team). |
| [`docs/design/`](docs/design/) | The design corpus: twenty-one documents (overview, primitives, chain construction, Merkle seal, HSM custody, OTLP wire, ledger server, verifier, test vectors, threat model, glossary, successor attestation and backfill, state-machine and multi-party flows, generation and HITL, civic AI and post-quantum, hardware supply chain, red/black separation, frontier AI training provenance, customer disclosure, privileged investigation, cross-institution wire). |
| `LICENSE`, `NOTICE`, `CITATION.cff` | Apache-2.0 licensing and citation metadata. |
| `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | Project governance, security disclosure channel, and contributor process. |
| `CHANGELOG.md` | Spec evolution provenance. |

A complete audience-by-audience navigation lives in [`docs/INDEX.md`](docs/INDEX.md) and in §13 of the specification.

## Reading order

| If you are a&hellip; | Start with&hellip; |
|---|---|
| FFIEC IT examiner | [`docs/examiner-quickstart.md`](docs/examiner-quickstart.md) (5 min), then [`docs/regulator-pack/handbook-mapping.md`](docs/regulator-pack/handbook-mapping.md) and `submission/proposal.md` |
| Regulator (policy lane) | [`submission/executive-summary.md`](submission/executive-summary.md), then [`submission/proposal.md`](submission/proposal.md) and the appendices |
| First-time reader | [`docs/management-summary.md`](docs/management-summary.md) (5 min), then the spec body §1&ndash;§4 |
| Cryptographic reviewer | [`docs/design/09-threat-model.md`](docs/design/09-threat-model.md), `02-chain-construction.md`, `03-merkle-seal.md`, `04-hsm-custody.md` |
| Implementer | The full spec end-to-end, then [`spec/test-vectors/`](spec/test-vectors/) |
| Bank executive | [`docs/management-summary.md`](docs/management-summary.md), [`docs/cost-model.md`](docs/cost-model.md), [`docs/MRM-COMMITTEE-BRIEF.md`](docs/MRM-COMMITTEE-BRIEF.md) |
| Audit committee chair | [`docs/audit-committee-summary.md`](docs/audit-committee-summary.md) |

## How to comment

Comments on PRD-2 are welcome via:

- **GitHub issues** &mdash; tagged `spec-proposal`, `editorial`, or `errata` per the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
- **Pull requests** against the spec text. Spec-affecting PRs follow the process in [`GOVERNANCE.md`](GOVERNANCE.md) and require the spec-editor approval and public-comment cadence documented there.
- **Security-sensitive feedback** &mdash; use the private channel in [`SECURITY.md`](SECURITY.md). Do not file public issues for live vulnerabilities.

The convergence target between PRD-N and PRD-(N+1) is *zero open gap-class findings*. Public-comment closure plus spec-editor sign-off triggers the next PRD.

## What is *not* in this repository

- **The reference implementation.** Implementation work is conducted in a separate repository and is not in scope for the public-comment review. The submission stands or falls on the merit of the specification and its supporting documentation.
- **Vendor-positioned material.** This repository is vendor-neutral by design.

## Project posture

**Open-source under Apache-2.0.** The Apache patent grant matters: the chain-of-custody primitive cannot be hostage to a future patent claim by a contributor or a downstream vendor. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

**Conflict-of-interest disclosure.** The author, Steve Muchow, is the founder of MMPWorks LLC, which develops commercial software that implements this specification, including TesseraSeal and Herald.Compliance. The specification, the conformance test vectors and the reference verifier are licensed under Apache-2.0, and conformance does not require any MMPWorks product. The project is governed transparently under the rules in [`GOVERNANCE.md`](GOVERNANCE.md) with the explicit intent of foundation transfer (OpenSSF, CNCF, or a banking-industry consortium) once the specification is finalized and adoption is established.

## Citation

If you reference this specification, please cite it per [`CITATION.cff`](CITATION.cff). The current released version is **PRD-2 (`0.2.0`)**.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by the FFIEC or any of its member agencies. The repository name reflects the regulatory framework this work is designed to satisfy. The FFIEC's adoption of any standard is solely the FFIEC's decision.
