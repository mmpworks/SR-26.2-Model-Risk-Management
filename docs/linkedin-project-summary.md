# LinkedIn project summary

> **What this doc is.** The outreach copy for the LinkedIn "Projects" entry covering
> this specification and the TesseraSeal implementation behind it. It lives here so the
> public-facing description and the repository stay in step: when the spec version moves,
> this file moves with it.
>
> **Status:** draft, pending a humanization and ELI5 pass. Read the guardrails at the
> bottom before editing. They exist because a rewrite pass is where a careful claim
> quietly becomes an overclaim.

**LinkedIn entry name:** FFIEC Chain of Custody - Compliance and Auditing - TesseraSeal
**Start date:** May 2026. Ongoing.
**Link used:** `https://mmpworks.com/chain-of-custody`

---

## Description (1,980 characters; LinkedIn's limit is 2,000)

An open specification for a cryptographic chain of custody over AI decisions, for banks under the Federal Reserve's SR 26-2 model-risk framework (joint with the OCC and FDIC, April 2026).

The gap: the FFIEC IT Examination Handbook already requires audit logs to be tamper-evident, integrity-protected, immutable and complete. Its AI booklet names the risks of AI in production but gives no audit-trail procedure for AI activity. SR 26-2 leaves the control to the institution. This supplies one, language-neutral and vendor-neutral:

1. HMAC chain at capture. Every AI decision event is hashed with a per-process session key derived through HKDF, and carries the SHA-256 of the event before it.
2. Daily Merkle seal. Events for each tenant-day aggregate into a Merkle tree whose root is published to an append-only ledger.
3. HSM-rooted signature. The daily root is signed in hardware custody at FIPS 140-2 Level 3 or higher.
4. OpenTelemetry-native wire. Events ship over OTLP using standard attributes plus chain extension fields.

Together they let an examiner walk the chain independently, without trusting the institution's vendor or its operations team.

What I built:

- The normative specification, at public review draft 0.3.0 with a stable v1 wire format.
- A conformance corpus of positive and negative vectors, byte-pinned so an implementation either matches or fails.
- Reference implementations across C#, Python and Go, held to byte-identical canonical output.
- Regulator overlays mapping the control to FFIEC, NIST CSF 2.0, NYDFS Part 500, DORA, FINRA 17a-4(f) and BSA/AML.

The specification and test vectors are Apache-2.0. This is a public-comment draft rather than a finalized standard, with a submission package staged for the agencies' forthcoming request for information on AI.

Read the specification: https://mmpworks.com/chain-of-custody

TesseraSeal is the closed implementation of this work. I can walk a reviewer through that repository under an NDA.

---

## Skills attached to the entry

LinkedIn takes five.

1. Applied Cryptography
2. Regulatory Compliance
3. Software Architecture
4. OpenTelemetry
5. Technical Writing

Alternates, if a different recruiter search matters more: Distributed Systems, Risk
Management, Open Source Software Development, Go, C#.

---

## Guardrails for the humanization and ELI5 pass

Rewrite the prose. Do not move any of these lines.

| Claim in the copy | Why it is worded that way |
|---|---|
| "a submission package **staged** for the agencies' forthcoming request for information" | The package is prepared, and `submission/cover-letter.md` and `submission/executive-summary.md` are still marked placeholders because the RFI has not published. **Never** write "submitted", "filed", or "sent to the Fed." |
| "a **public-comment draft** rather than a finalized standard" | It is PRD-3.1, document version 0.3.0. It is not adopted by any regulator. **Never** write "standard", "adopted", "approved", or "in use at banks." |
| "The **specification and test vectors** are Apache-2.0" | The spec and the conformance corpus are open. The reference implementations are not all public. **Never** widen this to "the project is open source." |
| "TesseraSeal is the **closed implementation**... under an NDA" | TesseraSeal ships as a binary. Its algorithms, field layouts, cache shapes and threading are never described in outward writing. **Never** add implementation detail here. |
| "Reference implementations across C#, Python and Go, held to **byte-identical canonical output**" | This is the real constraint: all three must emit byte-identical JCS-canonical output. It is a precise claim, not a flourish. Keep the precision. |
| "public review draft **0.3.0** with a stable **v1** wire format" | Document version and wire version are different numbers and both are load-bearing. Do not merge or round them. |

Two more rules for the pass:

- **Character budget.** LinkedIn cuts the description at 2,000 characters. The current
  draft is 1,980. A humanization pass usually adds length. Count before you ship.
- **House tic list.** Fluff intensifiers, agreement markers and virtue labels are cut on
  sight. Run `python ~/.claude/hooks/tic-gate.py <file>` over the result; the hook names
  the offending words and is the source of truth for the list.

---

## Keeping this current

The description names a spec version. When the spec moves, this file moves with it, along
with the repository `README.md` badge line and the audit-trail comparison data on the
website. All three quote a version number, and all three have drifted apart before.
