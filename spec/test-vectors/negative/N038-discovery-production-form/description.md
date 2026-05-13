# N038 — Discovery production form negative vector

**Targets:** §10.13.1 normative production-form requirement (line ~1989). The Rule 34 / Civil Investigative Demand discovery production packet shape.

**Failure mode pinned:** a producing party assembles a discovery packet that omits one of the §10.13.1 required artifacts (NDJSON of captured JSON entries, per-entry canonical bytes, verifier-output `Verdict-Object` per tenant-day, seal records, HSM public-key reference, trust-anchor manifest, production manifest binding the package). Two specific cases the vector exercises:

1. **Missing canonical-bytes/.** The packet ships NDJSON + Verdict-Object + seal records, but no `canonical-bytes/seq-{N}.bin` per-entry files. Opposing counsel cannot re-MAC the entries to verify.
2. **Missing production manifest.** The packet ships every artifact but no top-level production manifest with the HSM-signed bundle. The opposing-party verifier cannot validate the package's integrity as a whole.

**Verifier expected output (for each failure case):**
- Status: FAIL
- Step: (production-manifest pre-flight; not a §7 step — this is a §10.13.1 cross-check)
- Reason: `production manifest missing required artifact: canonical-bytes/` OR `production manifest absent — package not chain-of-custody conformant`

**Required for v1.0 conformance:** yes (when the institution operates §10.13.1 — normative-when-applicable for discovery production). Without this vector, two institutions building production packets produce different shapes and opposing counsel cannot cite §10.13.1 in a motion to compel a re-production.

**Materialization status:** stub. Fixture materializes alongside Herald.Compliance's discovery-pack assembly tooling in PRD-2 Phase 11-14. The vector requires a full production-pack assembly under one of the two failure modes; the conformance check verifies the assembly tool refuses to ship without the required artifact.
