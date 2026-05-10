# 19 — Customer audit-trail subset disclosure (§10.69)

> **What this doc is.** The design rationale for the §10.69 primitive that closes the Story-20 (Northbridge acquisition close) chain-of-custody gap for per-customer audit-trail subset disclosure under CFPB Personal Financial Data Rights (12 CFR Part 1033) and analogous customer-data-rights regimes. Auditor's-lens convention applies.

## 1. The problem this solves

Story 20 drives the design. Northbridge Federal Savings — a US regional bank under chain-of-custody — receives ~240 §1033 customer audit-trail requests per month. A customer asks not just for their data but for the audit trail of how their data was used. Today that's a manual production ginned up from internal logs; the customer cannot independently verify the trail's integrity; the institution cannot prove that the disclosure is complete or that the un-disclosed entries are properly excluded.

Three questions the chain must answer:

1. **Can the customer verify their disclosure independently?** §10.69's per-customer-disclosure HKDF derivation produces a session key bound to the requesting customer's `customer_correlation_index` (per §10.23). The customer computes canonical hashes from the disclosed packet; the institution provides the key fragments; the customer's verifier reproduces the per-event MAC and confirms integrity without ever having access to the institution's IKM.
2. **Is the disclosure complete?** §10.69's `disclosure_complete_excepting` field enumerates documented exclusions. The customer learns the categorical fact of exclusion (`['sar', 'litigation_hold', 'privileged_investigation']` typically) without learning the specific excluded entries. The completeness claim is bounded and documented.
3. **What does the customer NOT see?** §10.70 (BSA SAR / privileged-investigation) tagged entries are excluded. Litigation-hold entries are excluded. Redacted-per-§10.22 entries are included with redaction-discipline-bound content. The exclusions are the closed canonical four.

§10.69 closes the customer-side independent-verification gap. The customer's disclosure packet is integrity-bound, customer-side independently verifiable, and bounded by documented exclusions.

## 2. Why a new HKDF derivation, not the institutional session key

The institution's tenant session key (§4.1) is bound to the institution's IKM. Sharing it with the customer would expose all customers' chain entries — the per-tenant key derives all per-event MACs.

§10.69 derives a *per-customer-disclosure* session key by binding the HKDF info parameter to the customer's correlation index:

```
session_key_customer_disclosure = HKDF-SHA-256(
    IKM=ikm,
    salt=HKDF_SALT,
    info=HKDF_INFO_BASE || '|' || utf8(tenant_id) || '|' || utf8('customer-disclosure') || '|' || utf8(customer_correlation_index),
    length=32
)
```

The customer-disclosure session key is bound to one customer index. It computes valid MACs only for chain entries whose `audit.customer_correlation_index` matches that index. A customer cannot use their key to forge or read other customers' chain entries — the cryptographic binding is one-customer-at-a-time.

The pattern parallels §10.32 (per-device session key derivation). The HKDF info enrichment is the well-trodden mechanism for per-isolation-key derivation; §10.69 reuses it for a different isolation axis (customer instead of device).

## 3. Why per-cohort subtree disclosure is the right Merkle primitive

§10.31 (per-cohort subtree disclosure) was designed for issuing-bank examiners pulling a per-bank slice of a multi-tenant payments network's chain. The mathematical primitive is the same for §10.69: walk every chain entry whose customer_correlation_index matches the requesting customer; produce a Merkle subtree-disclosure proof binding each entry to the daily seal's signed root.

Both §10.31 and §10.69 disclose subsets of a single sealed root. The difference is the cohort identifier:

- §10.31: cohort identifier is `audit.routing.issuing_bank_id` (institution-side known taxonomy).
- §10.69: cohort identifier is `audit.customer_correlation_index` (customer-side requested filter).

The verifier dispatch is symmetric. The audit-paths reveal Merkle siblings (which are hashes, not chain content); the customer cannot recover other customers' chain entries from the audit-paths.

## 4. Why the documented-exception list is normative and closed

The pre-mortem identified the exclusion-list normativity as load-bearing. Without a closed canonical four, institutions could exclude entries arbitrarily under "internal review" or "compliance investigation" labels and the customer would have no purchase to challenge the exclusion. §10.69 normates four canonical categories:

1. **`sar`** — §10.70 BSA SAR / privileged-investigation (the most common exclusion, anchored in 31 USC §5318(g) privilege).
2. **`litigation_hold`** — Institution's litigation-hold registry (anchored in FRCP 37(e) and institution-side e-discovery practice).
3. **`privileged_investigation`** — §10.70 broader privileged-investigation (attorney-client, attorney work-product, regulatory examination privilege).
4. **`redacted_per_§10.22`** — The chain entry IS in the packet but with redaction-discipline-bound content; customer sees the redacted form. (Distinct from the others — these entries appear in the packet, just with redacted bodies.)

Institution-named additional exclusions (e.g., a third-party-data-license-restricted category) are documented in CC8.1; they appear under the canonical categories' framing or as institution-extension labels with CC8.1-named legal grounding.

## 5. Why the verifier emits two `additional_verifications` markers

A §10.69-conformant verifier walking a disclosure packet emits:

- `customer_disclosure_subtree_verified` — the Merkle subtree-disclosure proof binds each entry to the daily seal's signed root.
- `customer_disclosure_key_derivation_verified` — the per-customer-disclosure session key is correctly derived from the bound HKDF inputs and reproduces the per-event MACs in the packet.

Two markers because the integrity claim has two structural components: (a) Merkle inclusion (the entries are in the sealed root), and (b) per-event MAC verification (the entries are integrity-bound by the customer-disclosure session key, which is itself derived from the institution's IKM via HKDF). A verifier that reports only one marker has only walked one half of the integrity claim.

The `additional_verifications` pattern (introduced for §7's various dispositions) is the right surface here. Customer-side counsel reading the verifier output sees both markers and can independently confirm both halves; institution-side counsel uses the same markers in litigation-defense work.

## 6. Cross-references

- Spec sections: §10.21 cross-anchor; §10.22 redaction discipline; §10.23 consumer-correlation-index integrity; §10.31 per-cohort subtree disclosure (the regulator-side parallel); §10.32 per-device session key derivation (the parallel HKDF derivation pattern); §10.69 (this design doc's surface); §10.70 BSA SAR / privileged-investigation overlay (the reciprocal exclusion source).
- Test vectors: 075-076 (§10.69 HKDF derivation; customer-side independent verification with exception list).
- Auditor stories: Story 20 (Northbridge acquisition close) — the institutional-reference engagement; Daria Klosterman in retail-banking IT is the program-side reference engineer.
- Adjacent design docs: 20-privileged-investigation.md (the §10.70 sibling defining the exclusion source); 21-cross-institution-wire.md (the §10.71 sibling for cross-institution chain integrity).
- Regulator pack: `docs/regulator-pack/cfpb-1033-overlay.md` (the operative §1033 overlay); `docs/regulator-pack/cfpb-overlay.md` (the broader CFPB overlay).
- External: 12 CFR Part 1033 (CFPB Personal Financial Data Rights); GDPR Article 15 (right of access); CCPA / CPRA right of access; PIPA Article 35 (access right); PDPA Section 21 (access right).
