# Design documents

> **Purpose.** Internal design notes that justify the choices in the normative specification. The auditor (Big Four / FFIEC examiner) is the advisor whose lens the design satisfies. Where a design choice could go either way, the doc explains *why we chose* the way we did and what an auditor would say to confirm or push back.

## Reading order

1. [`00-overview.md`](00-overview.md) — system overview and data flow
2. [`01-primitives-spec.md`](01-primitives-spec.md) — the four primitives, design rationale
3. [`02-chain-construction.md`](02-chain-construction.md) — HMAC chain detail (the hot path)
4. [`03-merkle-seal.md`](03-merkle-seal.md) — daily Merkle seal detail
5. [`04-hsm-custody.md`](04-hsm-custody.md) — HSM signing and key custody
6. [`05-otlp-wire.md`](05-otlp-wire.md) — OTel wire format, attribute conventions
7. [`06-ledger-server-design.md`](06-ledger-server-design.md) — `ledger/` architecture
8. [`07-verifier-design.md`](07-verifier-design.md) — `verifier/` architecture
9. [`08-test-vectors.md`](08-test-vectors.md) — conformance corpus design
10. [`09-threat-model.md`](09-threat-model.md) — adversaries and properties
11. [`10-glossary.md`](10-glossary.md) — terminology reference (consult as needed alongside the other docs)
12. [`12-successor-attestation-and-backfill.md`](12-successor-attestation-and-backfill.md) — §10.39 + §10.42 cross-vendor-target M&A discipline
13. [`13-state-machine-and-multi-party-flows.md`](13-state-machine-and-multi-party-flows.md) — §1.5 + §10.43-§10.46 state-machine framing + insurance multi-party flows
14. [`14-generation-and-hitl.md`](14-generation-and-hitl.md) — §1.2 + §10.47-§10.50 generative AI prompt/output binding + RAG retrieval integrity + HITL review
15. [`15-civic-ai-and-post-quantum.md`](15-civic-ai-and-post-quantum.md) — §1.2 + §10.51-§10.55 civic-AI public-transparency + post-quantum + decadal re-sealing + challenge-response

## The auditor's-lens convention

Every design doc closes with an **&ldquo;Auditor's-lens review&rdquo;** section. That section names the questions an auditor would ask, the answer the design provides, and any open issues where the auditor's concern is acknowledged but not yet fully resolved.

Open issues escalate to specification review per the process in [GOVERNANCE.md](../../GOVERNANCE.md).
