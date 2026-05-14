# Executive summary — placeholder

> **This is a placeholder.** The actual executive summary is finalized against the receiving body's specific RFI / submission process. It is drafted to be circulated within a regulator without the reader needing implementation expertise.

---

## The gap

The FFIEC IT Examination Handbook already mandates that audit logs be **tamper-evident, integrity-protected, immutable, and complete** (Information Security booklet; Architecture, Infrastructure, and Operations booklet). The AIO booklet's §VII.D names the risks of AI in production but contains **no logging or audit-trail procedure for AI activity**. Examiners reviewing AI-using institutions today rely on the institution's narrative and the institution's vendor's assurances; they have no independent verification path.

The April 17, 2026 revision to the model-risk-management framework (SR 26-2 / OCC Bulletin 2026-13) explicitly excludes generative AI and agentic AI from scope, naming the forthcoming RFI as the lane in which AI-specific guidance will develop. This proposal is responsive to that lane.

## The proposal

A four-primitive chain of custody, language-neutral and vendor-neutral:

1. **HMAC chain at capture** &mdash; every AI decision event is hashed at the moment of capture using a per-process session key derived from the institution's tenant-bound input key material. Each event includes the SHA-256 of the previous event in the same run. Tampering with any event after capture is detected by the verifier.

2. **Daily Merkle seal** &mdash; events for each tenant per UTC calendar day are aggregated into an RFC 6962 Merkle tree. The root is published in an append-only ledger. Retroactive insertion, deletion, or reordering of any event in the day is detected by the verifier.

3. **HSM-rooted root signature** &mdash; the daily Merkle root is signed in HSM custody (FIPS 140-2 Level 3 or higher). The signing key is non-extractable. An attacker who can rewrite ledger storage but cannot produce HSM signatures still leaves the Merkle root mismatch detectable.

4. **OpenTelemetry-native wire** &mdash; events ship over OTLP using standard OpenTelemetry attributes plus the chain extension fields. Institutions that already operate OTel-based observability adopt the chain as an additional attribute namespace, not a parallel system.

The four primitives compose into a chain of custody an examiner can independently walk &mdash; with a single verifier binary, against the institution's exported chain artifacts, on the examiner's own laptop, **without trusting the institution's vendor or operations team**.

## What the proposal proves and does not prove

**The chain proves:**

- What the AI said at a specific time (the captured event records the model's response, the prompt, the tools called, the routing decision, the operational state at capture).
- That the record was not tampered with after capture.

**The chain does not prove:**

- That the AI's statement is factually accurate.
- That the AI's statement complied with policy.
- That the AI's statement is free of bias.

These three are separate questions answered with evidence outside the chain (the institution's policy library, fair-lending review, statistical bias testing, model-risk-management program). The chain is the **integrity foundation**, not the truth foundation.

## Why this gap matters

The model-risk-management revision (SR 26-2 / OCC Bulletin 2026-13) keeps the long-standing audit-trail expectation but offers no concrete answer to:

- *How does an examiner know the institution's record of an AI decision is the actual record produced at the time?*
- *How does an examiner verify that record without trusting the institution?*
- *How does an examiner compare two institutions' records for the same model on the same day for portfolio or supervisory cross-bank analysis?*

The four primitives produce a record that answers all three questions deterministically. Two institutions running conforming implementations of the same spec version produce **byte-identical** chain artifacts for the same logical event &mdash; making cross-institutional comparison and supervisory aggregation tractable.

## What is being asked

[The receiving body's specific question set determines this section. For the OCC/Fed/FDIC AI RFI, the asks are likely:

1. Recognition of the four primitives as a candidate audit-trail standard for AI in regulated banking.
2. Adoption guidance pointing examiners at the verifier as the independent verification path.
3. A path to a future FFIEC IT Examination Handbook AIO-booklet revision that names the chain-of-custody primitive in §VII.D or in a new dedicated section.]

## Project posture

Open-source under Apache-2.0. The patent grant matters: the chain-of-custody primitive cannot be hostage to a future patent claim. No vendor lock-in. The spec is the standard; the reference implementation is one example, not the standard itself. The project is governed transparently with the explicit intent of foundation transfer once finalized and adopted.

## What's enclosed

The proposal body, the FFIEC handbook mapping, the NIST CSF 2.0 / FS AI RMF / SR 26-2 control overlay, the conformance test-vector corpus summary, and the full specification (PRD-2, `0.2.0`).
