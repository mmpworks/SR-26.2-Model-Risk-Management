# SEC enforcement / examination overlay

**Scope.** Companion overlay for Securities and Exchange Commission (SEC) examiners, enforcement attorneys, and SEC-registered institutions adopting the chain-of-custody specification. Maps spec sections to Reg S-P (privacy), Reg S-ID (identity theft red flags), Regulation Best Interest (Reg BI), the SEC Marketing Rule under the Investment Advisers Act, and the 17 CFR §240.17a-4 books-and-records retention rule for broker-dealers.

**Status.** Initial overlay shell. Detailed per-section guidance is forthcoming.

## SEC-specific supervisory framework

The chain-of-custody specification was drafted primarily against FFIEC banking supervision. SEC-supervised institutions (broker-dealers under §15 of the Securities Exchange Act, investment advisers under the Advisers Act, transfer agents, exchanges, clearing agencies) apply the chain through their own supervisory framework. The substantive cryptographic and evidentiary posture is regime-neutral; this overlay names the SEC-specific composition points.

SEC regulations intersecting chain-of-custody operations:

- **17 CFR Part 248 (Reg S-P)** — privacy of consumer financial information. The chain's §10.22 redaction discipline, §10.38 consent / lawful-basis state machine, and §10.69 customer-disclosure mode compose with Reg S-P's notice-and-opt-out framework and the 2024 amendments' breach-notification requirements.
- **17 CFR §248.201 (Reg S-ID)** — identity theft red flags rule. AI-driven identity-verification decisions captured under the chain compose with §10.11 (adverse-action translation) and §10.11.1 (ECOA reasons schema) — the same primitive carries the SEC's Red Flag determination evidence.
- **17 CFR §240.15l-1 (Regulation Best Interest)** — broker-dealer obligations on recommendations to retail customers. AI-driven recommendation systems captured under the chain bind the recommendation, the disclosed conflicts, and the basis for the recommendation under integrity-bound entries. §4.4.2 deployment-intent capture and §4.4.5 underwriting-features family compose for Reg BI evidence.
- **17 CFR §275.206(4)-1 (SEC Marketing Rule)** — investment-adviser marketing. AI-generated marketing content and personalized recommendations captured under the chain bind the content, the timestamps, and the model identifier under §4.4 OTLP wire form.
- **17 CFR §240.17a-4 — books-and-records retention.** Broker-dealers are subject to a 6-year retention floor on certain records; §240.17a-4(f) specifies WORM-equivalent retention discipline. The chain's append-only enforcement (§10.3) plus the 7-year FFIEC retention floor (§10.9 IKM registry retention) satisfies the 6-year SEC floor; the WORM-equivalence claim under §240.17a-4(f) is testable from the chain's append-only architecture.

## Civil enforcement composition

SEC civil enforcement actions under §10b-5 (securities fraud), §17(a) (offering fraud), and the analogous Advisers Act sections often turn on what an AI system told a customer and whether that statement was misleading. The chain's epistemic-scope discipline (§1.2) carries straight into this enforcement framing:

- **The chain proves what the AI said and that the record was not tampered with.** §10b-5 evidentiary record of statements made.
- **The chain does NOT prove the AI's statement was non-misleading.** Substantive misleadingness is litigated separately; the chain is the integrity foundation for the words, not the truth foundation for the claim.
- **Self-authentication under FRE 902(13) / 902(14).** §5.2 best-evidence posture + §10.13 evidentiary artifacts + §10.26 reference-verifier distribution give SEC enforcement attorneys a clean foundation citation for §240.17a-4-retained records.

## Subpoena and privilege interaction

SEC subpoenas of chain entries tagged `audit.privileged_investigation = true` under `regime = "attorney-client"` or `"attorney-work-product"` (per §10.70) follow the role-based dispatch surface: the SEC investigator sees the existence-attestation form (entries exist, are integrity-bound, are tagged) while the institution litigates privilege separately. The `sec-investigation-active` regime value is enumerated in §10.70 for institutions tagging entries under an active SEC investigation (subject to the §10.70 institution-named regime discipline including pre-registration in CC8.1, regulator visibility before first use, `regime_first_used_utc` binding, substantive-reach limitation, and `regime_scope_filter_sha256` binding).

## Examiner reading path

SEC examiners (Division of Examinations [the successor to OCIE, renamed in December 2020] / Division of Investment Management / Division of Trading and Markets / DERA — Division of Economic and Risk Analysis) read the spec through their division's lens:

1. **Broker-dealer compliance examination.** Read §1, §1.1, §1.2, §10.3 (append-only enforcement), §10.9 (retention), §10.11 (Red Flag composition), §10.13 (evidentiary artifacts). The §240.17a-4 retention claim is testable.

2. **Investment-adviser exam.** Read the same baseline plus §10.22 (redaction), §10.38 (consent / lawful-basis), §10.69 (customer-disclosure for Marketing Rule customer-complaint review).

3. **Enforcement attorney (DERA-supported).** Read §1.2 epistemic scope, §5.2 best-evidence, §10.13 evidentiary artifacts, §10.26 reference-verifier distribution. The verifier's normative output (per §7) is citable in enforcement filings.

## Cross-reference

- §1 — applicable agencies enumeration names SEC.
- §1.1 Daubert four-factor grounding — applies to SEC expert testimony under FRE 702.
- §1.2 epistemic scope — directly maps to §10b-5 / §17(a) "what did the AI say?" framing.
- §5.2 best-evidence posture — anchors §240.17a-4 retention compliance.
- §10.3 append-only enforcement — anchors §240.17a-4(f) WORM-equivalence claim.
- §10.13 evidentiary artifacts — citable in enforcement filings.
- §10.26 reference-verifier distribution — Cosign-signed, reproducible-build, citable in §240.17a-4 evidence.
- §10.70 privileged-investigation overlay — SEC subpoena interaction.
- §11 informative references — 17 CFR §240.17a-4, Reg S-P, Reg S-ID, Reg BI, Marketing Rule.

## Forthcoming detailed content

This stub anchors SEC jurisdiction in the spec corpus. Detailed content (per-CFR section walkthrough, SEC Form filing integration, specific civil-enforcement worked examples, DERA economic-analysis integration with §10.51 differential-privacy public layer) lands in a future revision.
