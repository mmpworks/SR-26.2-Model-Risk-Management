# 21 — Cross-institution Fedwire / ACH chain integrity (§10.71)

> **What this doc is.** The design rationale for the §10.71 primitive that closes the Story-20 (Northbridge acquisition close) chain-of-custody gap for cross-institution Fedwire and ACH chain integrity, using the Federal Reserve's voluntary cross-institution-anchor registry as the discovery mechanism per §10.21.3 registry-discovery pattern. Auditor's-lens convention applies.

## 1. The problem this solves

Story 20 drives the design. Northbridge originates ~14,000 Fedwire transactions per month and ~280,000 ACH transactions per month. Each transaction has chain entries on the originating side; today the integrity claim ends at the institution's chain boundary. The receiving institution's chain entries — when the receiving institution also runs a conformant chain — are not bound to Northbridge's chain.

Three questions Northbridge and a counterpart institution must answer:

1. **Does the originating chain entry match the receiving chain entry?** §10.71 emits `audit.wire.fedwire_originated` on Northbridge's side and `audit.wire.fedwire_received` on the counterpart's side; both reference the Fedwire IMAD/OMAD identifiers; the chain entries are bound by the registry-discovery cross-anchor (§10.21.3).
2. **Is the counterpart institution participating in the cross-anchor registry?** The Federal Reserve's voluntary cross-institution-anchor registry (~340 participating institutions as of PRD-4) is the discovery surface. Non-participating counterparts surface as `cross_anchor_unbound` documented residuals.
3. **What is the integrity claim for ACH transactions?** ACH has different settlement-window discipline (next-day or two-day vs same-day Fedwire); §10.71's ACH event family follows the same registry-discovery pattern with institution-named ACH-specific publication SLA.

§10.71 closes the gap. Fedwire and ACH transactions originating or terminating at participating institutions become cross-institution-integrity-bound; non-participating counterparts surface as documented residuals.

## 2. Why §10.21.3 (registry-discovery) is the right primitive

The pre-mortem identified two patterns for cross-institution composition:

1. **§10.21.2 parallel-evaluator composition.** Independent evaluators of one subject (lab + AISI; cedent + reinsurer; clinical institution + observer). Parties know each other directly; the cross-anchor binds at a known boundary.
2. **§10.21.3 registry-discovery.** Cross-institution cross-anchors discovered via a third-party registry. Parties don't know each other directly; the registry mediates.

Cross-institution wires are the §10.21.3 case. Northbridge originates a Fedwire to "any participating institution"; the receiving institution may be one of the 340 registry participants or a non-participant. Discovery is registry-mediated, not party-to-party. The registry's role is publication and signed-receipt, not chain-bearing.

§10.21.3 generalizes beyond Fedwire / ACH:

- SWIFT-mediated international-wire registries (CBPR registries for cross-border payment-rails).
- FedNow instant-payment registries.
- FINRA broker-dealer trade-reporting registries (TRACE, ORF).
- CCP-cleared-derivatives chain registries.
- Credit-bureau-mediated cross-institution-correlation registries (ACAS).

The §10.21.3 primitive (lifted in this same wave) handles all of them. §10.71 is the canonical PRD-4 instance; future cross-institution surfaces compose under the same primitive.

## 3. Why the registry's role is publication and signed-receipt, not chain-bearing

The Federal Reserve does not author chain entries. The Fed validates that registry-published cross-anchors are well-formed and signed by the participating institution; the Fed does not produce chain integrity claims itself. The registry's role is the *discovery mechanism*: an institution looks up the cross-anchor for a given Fedwire IMAD/OMAD pair.

The pre-mortem flagged a failure mode: a registry-mediated cross-anchor scheme that depended on the registry signing the cross-anchors would centralize integrity authority at the Fed. §10.21.3 normates the registry as a publication-and-signed-receipt service; integrity authority remains with the participating institutions; the Fed validates well-formedness but does not bear integrity.

This is structurally similar to Certificate Transparency: the CT log publishes signed certificate appearances but does not bear PKI authority; the binding integrity is at the issuing CA. The Fed's cross-institution-anchor registry follows the same pattern.

## 4. Why `cross_anchor_unbound` is a documented residual, not a chain-integrity failure

When the receiving institution is non-participating, the originating side's chain entry has no counterpart to bind to. The verifier dispatches `cross_anchor_unbound` and the institution's CC8.1 documents the receiving-institution non-participation as a residual.

The choice not to fail-closed is operational: ~340 of the ~10,000 US financial institutions participate. Forcing fail-closed on non-participation would make Fedwire originating chains brittle to the receiving institution's chain-conformance posture. §10.21.3 normates the residual as documented and bounded; institutional CC8.1 names the participation rate (Northbridge: ~78% of outbound volume cross-anchored at PRD-4 publication).

The institution can elect a stricter posture in CC8.1 (e.g., "only originate to participating institutions") if business justification supports it. The spec doesn't impose the discipline; the institution chooses.

## 5. Why ACH and Fedwire share the §10.71 family

ACH and Fedwire have different settlement characteristics:

- **Fedwire** — same-day final settlement; ~90 seconds publication SLA to the registry.
- **ACH** — next-day or two-day settlement; ACH-specific publication SLA in CC8.1, typically within the ACH settlement window.

The chain primitives are structurally identical: an originating event, a receiving event, a registry-discovery cross-anchor between them. The institution-named publication SLA captures the cadence difference. §10.71 emits both `audit.wire.fedwire_*` and `audit.ach.*` events; an institution running both surfaces emits both event kinds under one §10.71 deployment.

Future payment rails (FedNow instant-payment, SWIFT international, hypothetical CBDC settlement) will compose under §10.71 if they share the registry-discovery pattern, or under §10.21.2 if they are direct party-to-party. The pattern selection happens at registry-design time, not at chain time.

## 6. Cross-references

- Spec sections: §10.21 / §10.21.3 (registry-discovery cross-anchor primitive); §10.71 (this design doc's surface).
- Test vectors: 079-083 (§10.71: Fedwire cross-anchored, Fedwire `cross_anchor_unbound`, ACH cross-anchored, ACH variant, registry-discovery client mock fixture).
- Auditor stories: Story 20 (Northbridge acquisition close) — the institutional-reference engagement; Vance Quintero-Brieskorn (Wire-Room Lead) and Margaret Choe (Federal Reserve Bank of Boston Wholesale Payments Office) are the program-side reference engineers.
- Adjacent design docs: 19-customer-disclosure.md and 20-privileged-investigation.md (the §10.69 / §10.70 siblings for Story 20's wishlist family).
- Regulator pack: `docs/regulator-pack/fedwire-cross-institution-overlay.md` (the operative §10.71 overlay).
- External: Federal Reserve Operating Circular 6 (Fedwire); NACHA Operating Rules (ACH); 12 CFR Part 210 (Regulation J); Federal Reserve voluntary cross-institution-anchor registry documentation; Certificate Transparency (RFC 6962, structural parallel for the registry-as-publication-mechanism design).
