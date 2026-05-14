# SR 26-2 Model Risk Management &mdash; Implementation Materials

> **Status:** Public Review Draft 2 (PRD-2) &mdash; document version `0.2.0`. **This is a public-comment draft, not a finalized standard.**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-public%20review%20draft-orange.svg)](spec/chain-of-custody-DRAFT-0.2.0.md)
[![Spec](https://img.shields.io/badge/spec-PRD--2-informational.svg)](spec/chain-of-custody-DRAFT-0.2.0.md)
[![Anchor](https://img.shields.io/badge/anchor-SR%2026--2-blueviolet.svg)](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm)

----

## What this repository is

A public corpus of model-risk-management materials assembled around the Federal Reserve's [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) supervisory letter (April 17, 2026 &mdash; joint with OCC and FDIC). SR 26-2 supersedes SR 11-7 and SR 21-8 and applies to banking organisations with over $30 billion in total assets.

The repository hosts a falsifiable, cryptographic chain of custody for AI decisions &mdash; a technical control banks can deploy under SR 26-2's risk-based regime. The letter itself lives at federalreserve.gov; this repository does not mirror it.

## The technical proposal

The FFIEC IT Examination Handbook already mandates that audit logs be **tamper-evident, integrity-protected, immutable, and complete** (Information Security booklet, AIO booklet). The AIO booklet's &sect;VII.D names the risks of AI in production but contains **no logging or audit-trail procedure for AI activity**. SR 26-2's risk-based framing leaves the choice of control to the institution. This proposal supplies one such control with four primitives, language-neutral and vendor-neutral:

1. **HMAC chain at capture** &mdash; every AI decision event is hashed with a per-process session key derived via HKDF; each event includes the SHA-256 of the previous event in the same run.
2. **Daily Merkle seal** &mdash; events for each tenant-day are aggregated into a Merkle tree; the root is published in an append-only ledger.
3. **HSM-rooted root signature** &mdash; the daily Merkle root is signed in HSM custody (FIPS 140-2 Level 3 or higher).
4. **OpenTelemetry-native wire** &mdash; events ship over OTLP using standard OTel attributes plus the chain extension fields.

The four primitives compose into a chain of custody an examiner can independently walk &mdash; without trusting the institution's vendor or the institution's ops team.

## Repository contents

This repository contains the **specification, supporting documentation, and submission materials** for the proposed standard. It is open-source under Apache-2.0. It does **not** contain a reference implementation; that work is being conducted in a separate repository and is not in scope for the public-comment review.

| Path | Purpose |
|---|---|
| [`spec/`](spec/) | The normative specification. Currently PRD-2 (`0.2.0`). |
| [`spec/test-vectors/`](spec/test-vectors/) | The conformance corpus. Positive vectors 001, 002, 003, 008, 010, 015&ndash;019; negative vectors N001 through N022. |
| [`docs/`](docs/) | Audience-segmented supporting material &mdash; design rationale, regulator-pack overlays (FFIEC, NIST CSF 2.0, NYDFS Part 500, DORA, GDPR, HIPAA, BSA/AML, FedRAMP, APAC/Korea/Bank of Israel, CFPB), control map, SOC pack, audit procedures, incident-response playbook, customer-dispute procedures, eleven auditor-stories. |
| [`docs/design/`](docs/design/) | The ten design documents (overview, primitives, chain construction, Merkle seal, HSM custody, OTLP wire, ledger server, verifier, test vectors, threat model, glossary). |
| [`submission/`](submission/) | The public-comment submission package (cover letter, executive summary, proposal body, appendices). |

## Reading order

| If you are a&hellip; | Start with&hellip; |
|---|---|
| First-time reader | [`docs/management-summary.md`](docs/management-summary.md) (5 min), then [`spec/chain-of-custody-DRAFT-0.2.0.md`](spec/chain-of-custody-DRAFT-0.2.0.md) &sect;1&ndash;&sect;4 |
| Bank examiner | [`docs/examiner-quickstart.md`](docs/examiner-quickstart.md) (5 min), [`docs/regulator-pack/handbook-mapping.md`](docs/regulator-pack/handbook-mapping.md) |
| MRM officer / model risk manager | [`docs/MRM-COMMITTEE-BRIEF.md`](docs/MRM-COMMITTEE-BRIEF.md), [`docs/management-summary.md`](docs/management-summary.md), [`spec/chain-of-custody-DRAFT-0.2.0.md`](spec/chain-of-custody-DRAFT-0.2.0.md) &sect;1&ndash;&sect;4 |
| Cryptographic reviewer | [`docs/design/09-threat-model.md`](docs/design/09-threat-model.md), [`docs/design/02-chain-construction.md`](docs/design/02-chain-construction.md), [`docs/design/03-merkle-seal.md`](docs/design/03-merkle-seal.md), [`docs/design/04-hsm-custody.md`](docs/design/04-hsm-custody.md) |
| Implementer | [`spec/chain-of-custody-DRAFT-0.2.0.md`](spec/chain-of-custody-DRAFT-0.2.0.md) end-to-end, [`spec/test-vectors/`](spec/test-vectors/) |
| Bank executive | [`docs/management-summary.md`](docs/management-summary.md), [`docs/cost-model.md`](docs/cost-model.md), [`docs/MRM-COMMITTEE-BRIEF.md`](docs/MRM-COMMITTEE-BRIEF.md) |

A complete audience-by-audience navigation lives in [`docs/INDEX.md`](docs/INDEX.md) and in &sect;13 of the spec.

## How to comment

Comments on PRD-2 are welcome via:

- **GitHub issues** &mdash; tagged `spec-proposal`, `editorial`, or `errata` per the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
- **Pull requests** against the spec text. Spec-affecting PRs follow the process in [`GOVERNANCE.md`](GOVERNANCE.md) and require spec-editor approval and the public-comment cadence documented there.
- **Security-sensitive feedback** &mdash; use the private channel in [`SECURITY.md`](SECURITY.md). Do not file public issues for live vulnerabilities.

The convergence target between PRD-N and PRD-(N+1) is *zero open gap-class findings*. Public-comment closure plus spec-editor sign-off triggers the next PRD.

## Submission posture

This corpus is being prepared as a comment-letter response to the forthcoming OCC / Federal Reserve / FDIC Request for Information on model risk management and banks' use of AI &mdash; the RFI announced in the closing language of [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) / [OCC Bulletin 2026-13](https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html) (April 17, 2026). The submission package in [`submission/`](submission/) restructures the corpus around the RFI's question set when the RFI publishes.

Secondary submission targets: Treasury FS AI RMF v2 comment cycles, NIST AI RMF Critical Infrastructure Profile, and trade-association tracks (FSSCC, BPI, ABA).

## Companion site

A rendered, navigable view of this corpus lives at **<https://mmpworks.com/mrm>** &mdash; the same markdown, with cross-link resolution, search, mermaid diagrams, and a "build a print packet" workflow for examiner and audit-committee preparation. The site does not host the SR 26-2 letter; it links out to federalreserve.gov for the authoritative text.

## Governance

This project is governed by the rules in [`GOVERNANCE.md`](GOVERNANCE.md). The intent is to transfer governance to a neutral foundation (OpenSSF, CNCF, or a banking-industry consortium) once the specification is finalized and adoption is established.

## Licensing

Apache License 2.0. The Apache patent grant matters here: the chain-of-custody primitive cannot be hostage to a future patent claim by a contributor or a downstream vendor. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by the Board of Governors of the Federal Reserve System, the Office of the Comptroller of the Currency, the Federal Deposit Insurance Corporation, the FFIEC, or any other supervisory agency. The repository name reflects the supervisory letter this work is designed to inform; adoption of any standard is solely the issuing agencies' decision.
