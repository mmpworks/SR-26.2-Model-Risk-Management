# FFIEC AI Chain-of-Custody &mdash; Proposed Standard

> **Status:** Public Review Draft 1 (PRD-1) &mdash; document version `0.1.0-draft.1`. **This is a public-comment draft, not a finalized standard.**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-public%20review%20draft-orange.svg)](spec/chain-of-custody-DRAFT-0.1.0.md)
[![Spec](https://img.shields.io/badge/spec-PRD--1-informational.svg)](spec/chain-of-custody-DRAFT-0.1.0.md)

---

## What this is

A proposed open standard for tamper-evident logging of AI-driven decisions in regulated financial institutions.

The FFIEC IT Examination Handbook already mandates that audit logs be **tamper-evident, integrity-protected, immutable, and complete** (Information Security booklet, AIO booklet). The AIO booklet's §VII.D names the risks of AI in production but contains **no logging or audit-trail procedure for AI activity**. This proposal closes that gap with four primitives, language-neutral and vendor-neutral:

1. **HMAC chain at capture** &mdash; every AI decision event is hashed with a per-process session key derived via HKDF; each event includes the SHA-256 of the previous event in the same run.
2. **Daily Merkle seal** &mdash; events for each tenant-day are aggregated into a Merkle tree; the root is published in an append-only ledger.
3. **HSM-rooted root signature** &mdash; the daily Merkle root is signed in HSM custody (FIPS 140-2 Level 3 or higher).
4. **OpenTelemetry-native wire** &mdash; events ship over OTLP using standard OTel attributes plus the chain extension fields.

The four primitives compose into a chain of custody an examiner can independently walk &mdash; without trusting the institution's vendor or the institution's ops team.

## Repository contents

This repository contains the **specification, supporting documentation, and submission materials** for the proposed standard. It is open-source under Apache-2.0. It does **not** contain a reference implementation; that work is being conducted in a separate repository and is not in scope for the public-comment review.

| Path | Purpose |
|---|---|
| [`spec/`](spec/) | The normative specification. Currently PRD-1 (`0.1.0-draft.1`). |
| [`spec/test-vectors/`](spec/test-vectors/) | The conformance corpus. Positive vectors 001, 002, 003, 008, 010, 015&ndash;019; negative vectors N001 through N022. |
| [`docs/`](docs/) | Audience-segmented supporting material &mdash; design rationale, regulator-pack overlays (FFIEC, NIST CSF 2.0, NYDFS Part 500, DORA, GDPR, HIPAA, BSA/AML, FedRAMP, APAC/Korea/Bank of Israel, CFPB), control map, SOC pack, audit procedures, incident-response playbook, customer-dispute procedures, eleven auditor-stories. |
| [`docs/design/`](docs/design/) | The ten design documents (overview, primitives, chain construction, Merkle seal, HSM custody, OTLP wire, ledger server, verifier, test vectors, threat model, glossary). |
| [`submission/`](submission/) | The public-comment submission package (cover letter, executive summary, proposal body, appendices). |

## Reading order

| If you are a&hellip; | Start with&hellip; |
|---|---|
| First-time reader | [`docs/management-summary.md`](docs/management-summary.md) (5 min), then [`spec/chain-of-custody-DRAFT-0.1.0.md`](spec/chain-of-custody-DRAFT-0.1.0.md) §1&ndash;§4 |
| FFIEC IT examiner | [`docs/examiner-quickstart.md`](docs/examiner-quickstart.md) (5 min), [`docs/regulator-pack/handbook-mapping.md`](docs/regulator-pack/handbook-mapping.md) |
| Cryptographic reviewer | [`docs/design/09-threat-model.md`](docs/design/09-threat-model.md), [`docs/design/02-chain-construction.md`](docs/design/02-chain-construction.md), [`docs/design/03-merkle-seal.md`](docs/design/03-merkle-seal.md), [`docs/design/04-hsm-custody.md`](docs/design/04-hsm-custody.md) |
| Implementer | [`spec/chain-of-custody-DRAFT-0.1.0.md`](spec/chain-of-custody-DRAFT-0.1.0.md) end-to-end, [`spec/test-vectors/`](spec/test-vectors/) |
| Bank executive | [`docs/management-summary.md`](docs/management-summary.md), [`docs/cost-model.md`](docs/cost-model.md), [`docs/MRM-COMMITTEE-BRIEF.md`](docs/MRM-COMMITTEE-BRIEF.md) |

A complete audience-by-audience navigation lives in [`docs/INDEX.md`](docs/INDEX.md) and in §13 of the spec.

## How to comment

Comments on PRD-1 are welcome via:

- **GitHub issues** &mdash; tagged `spec-proposal`, `editorial`, or `errata` per the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).
- **Pull requests** against the spec text. Spec-affecting PRs follow the process in [`GOVERNANCE.md`](GOVERNANCE.md) and require the spec-editor approval and public-comment cadence documented there.
- **Security-sensitive feedback** &mdash; use the private channel in [`SECURITY.md`](SECURITY.md). Do not file public issues for live vulnerabilities.

The convergence target between PRD-N and PRD-(N+1) is *zero open gap-class findings*. Public-comment closure plus spec-editor sign-off triggers the next PRD.

## Submission posture

This corpus is being prepared as a comment-letter response to the forthcoming OCC / Federal Reserve / FDIC Request for Information on model risk management and banks' use of AI &mdash; the RFI announced in the closing language of [SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) / [OCC Bulletin 2026-13](https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html) (April 17, 2026). The submission package in [`submission/`](submission/) restructures the corpus around the RFI's question set when the RFI publishes.

Secondary submission targets: Treasury FS AI RMF v2 comment cycles, NIST AI RMF Critical Infrastructure Profile, and trade-association tracks (FSSCC, BPI, ABA).

## Governance

This project is governed by the rules in [`GOVERNANCE.md`](GOVERNANCE.md). The intent is to transfer governance to a neutral foundation (OpenSSF, CNCF, or a banking-industry consortium) once the specification is finalized and adoption is established.

## Licensing

Apache License 2.0. The Apache patent grant matters here: the chain-of-custody primitive cannot be hostage to a future patent claim by a contributor or a downstream vendor. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by the FFIEC or any of its member agencies. The repository name reflects the regulatory framework this work is designed to satisfy. The FFIEC's adoption of any standard is solely the FFIEC's decision.
