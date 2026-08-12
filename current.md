# Current State
_as of 2026-08-12_

## What we're building right now
The canonical, public FFIEC AI chain-of-custody specification (PRD-3.1, document version 0.3.0, wire-format `v1`) plus its conformance test-vector corpus — a falsifiable, cryptographic chain-of-custody control banks can deploy under SR 26-2. This is the authoritative repo: spec text, test vectors, governance, and the regulator-pack overlays all live here; the Go reference implementation lives in the sibling private repo `ffiec` (which explicitly defers to this repo for anything spec-shaped). Current branch `spec/multi-payload-full-blob-hash-convention` is mid-work on a normative §7 rendering rule and new FINRA-alignment test vectors.

## Active decisions
- 2026-05-21/24: PRD-3 (0.3.0) released, then PRD-3.1 sub-release shipped reference implementations for three attribute families (§14.6 `audit.actor.*`, §14.7 `audit.reasoning.substrate_kind`, §14.8 `audit.downstream_action.*`) across C# (Herald.Compliance), Python (Herald.Py), and Go (ffiec verifier) — byte-identical JCS-canonical output required across all three. No normative spec text changed in that sub-release.
- [Unreleased] §7 observed-value rendering rule (normative): verifier reason strings that embed an observed wire value (`format_version`, `sign_payload_version`, `canonical_encoding`, floor versions) MUST wrap it in ASCII double-quotes — resolves an N023 vs. N009/N022 rendering divergence. Decision rationale (consistency + disambiguation + zero signature effect, since reason strings are never signed) recorded in full in `CHANGELOG.md`. N009/N022 vectors re-rendered to match; `regulator-pack/finding-language.md` and similar generic-form docs were deliberately left unchanged (they render no observed value).
- Real Ed25519 test key now wired in; N004/N005 materialized as live signature fixtures rather than stubs (`3d5f647`).
- FINRA alignment work in progress: 17a-4(f) audit-trail mapping + Rule 2210 principal-preapproval ordering spec'd (`e536b0b`) and given conformance vectors 090+091 (`229be58`, s10.84).
- `.gitattributes` exempts the byte-pinned vector corpus from EOL conversion (`18e7c32`) — a correctness guard for byte-exact conformance testing.

## Open questions
- The current branch `spec/multi-payload-full-blob-hash-convention` is not yet merged to `main` — confirm whether the §7 quoting rule and vectors 090/091 are ready to merge, or still under review/comment.
- README still headlines "Public Review Draft 2 (PRD-2), document version 0.2.0" while CHANGELOG and recent commits are at PRD-3.1/0.3.0 — README needs a status bump (or confirm it's intentionally lagging pending a formal PRD-3 publication announcement).
- Whether the sibling `ffiec` repo's Go verifier needs a corresponding update for the new §7 quoting rule and FINRA vectors (cross-repo sync question — see `ffiec/current.md`).

## Next action
Confirm the README PRD-2→PRD-3.1 status-bump question with Steve, then check whether `spec/multi-payload-full-blob-hash-convention` is ready to merge to `main` (it currently sits several commits ahead with FINRA vector work layered on top of the multi-payload hash-convention branch name — verify that naming still matches the branch's actual content before merging).

## Stop condition
Halt and return to Steve before merging any spec branch to `main` (spec changes here are the canonical source multiple downstream implementations depend on) and before publishing any README/status change that would represent this as a finalized standard rather than a public-comment draft.

## Needs approval
- Merging spec-affecting branches to `main` — per `GOVERNANCE.md`, requires spec-editor approval and the documented public-comment cadence.
- README status-line changes (PRD-2 → PRD-3.1) — confirm with Steve before publishing, since this is a public repo read by examiners/regulators.
- Any change to normative spec text (sections 0-14) — spec-editor review required regardless of who authors it.
