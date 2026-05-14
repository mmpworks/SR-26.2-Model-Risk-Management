# Public-comment submission package

> **What this directory is.** The materials prepared for formal submission of the FFIEC AI Chain-of-Custody proposed standard to receiving bodies (regulatory agencies, working groups, trade associations).

## Primary submission target

The forthcoming **OCC / Federal Reserve / FDIC Request for Information on model risk management and banks' use of AI**, announced in the closing language of:

- [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) (April 17, 2026)
- [OCC Bulletin 2026-13](https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html) (April 17, 2026)
- [FDIC press release](https://www.fdic.gov/news/press-releases/2026/agencies-issue-revised-model-risk-guidance) (April 17, 2026)

The agencies stated they "plan to issue in the near future a request for information that addresses model risk management generally and considers, in particular, banks' use of AI, including generative AI and agentic AI and AI-based models." The submission package in this directory is being prepared on the assumption that the RFI will publish during summer 2026 with a 60&ndash;90 day comment window closing in fall 2026.

When the RFI publishes, the body of [`proposal.md`](proposal.md) is restructured around the RFI's actual question set within 14 days. The cover letter, executive summary, and appendices remain stable.

## Secondary submission targets

The same materials retarget with only a swapped cover letter to:

- **Treasury Financial Services AI Risk Management Framework** (FS AI RMF) v2 comment cycles &mdash; Treasury released v1 in February/March 2026 (230 control objectives, NIST-aligned).
- **NIST AI RMF Critical Infrastructure Profile** &mdash; concept note dropped April 7, 2026; expected to enter formal public comment in 2026.
- **FFIEC IT Examination Handbook AIO booklet** revision cycle &mdash; the booklet was last revised June 2021 and §VII.D names AI risks but contains no logging or audit-trail procedure for AI activity.
- **Trade-association working groups** &mdash; FSSCC, BPI, ABA, FS-ISAC.

## Package contents

| File | Purpose | Status |
|---|---|---|
| [`cover-letter.md`](cover-letter.md) | One-page transmittal to the receiving body | Placeholder |
| [`executive-summary.md`](executive-summary.md) | 3&ndash;5 page non-technical summary &mdash; the FFIEC-handbook gap, the four primitives, the proposal | Placeholder |
| [`proposal.md`](proposal.md) | Body &mdash; will be restructured around the RFI's question set when published | Placeholder skeleton |
| [`appendices/handbook-mapping.md`](appendices/handbook-mapping.md) | FFIEC AIO/IS handbook clause-by-clause mapping (sourced from `docs/regulator-pack/handbook-mapping.md` and reformatted for formal submission) | Placeholder |
| [`appendices/control-overlay.md`](appendices/control-overlay.md) | NIST CSF 2.0 + FS AI RMF + SR 26-2 overlay (sourced from `docs/regulator-pack/`) | Placeholder |
| [`appendices/test-vectors-summary.md`](appendices/test-vectors-summary.md) | Conformance corpus summary | Placeholder |

The full specification (`spec/chain-of-custody-DRAFT-0.2.0.md`) is attached to the submission as a rendered PDF, generated from the markdown source by Pandoc.

## Production rules

- **Cover letter**: institution-letterhead PDF, signed.
- **Executive summary**: PDF, 3&ndash;5 pages.
- **Proposal**: PDF, mapped to the receiving body's question set.
- **Appendices**: PDF, attached.
- **Spec**: PDF render of `spec/chain-of-custody-DRAFT-0.2.0.md`, with the PRD-2 banner intact and a generation-timestamp footer.

PDF generation uses Pandoc with a citation-aware LaTeX template. The build is reproducible: same source bytes &rarr; same PDF bytes (modulo embedded timestamp). The PDF render command is in [`build/render-pdf.sh`](build/render-pdf.sh) and is invoked by the `.github/workflows/render-pdf.yml` GitHub Action.

## Submission channel

For Federal Register RFIs, the standard channel is **regulations.gov** with the appropriate docket. The cover letter, executive summary, proposal, and appendices are uploaded as separate PDFs; the spec PDF is uploaded as an attachment. A short backup channel (agency direct email per the RFI's *Addresses* section) is used as a secondary.

For working-group and trade-association tracks, the channel is direct delivery to the working-group secretariat, with a copy to the project's GitHub repository as a `submission-archive/` snapshot tagged at the submission date.

## Tracking

Each submission is recorded as a row in [`submission-log.md`](submission-log.md) (created at first submission) with:

- Receiving body
- Docket / reference number
- Date submitted
- Channel used
- Materials version (PRD-N, document version, commit SHA)
- Public-comment-period close date
- Outcome (acknowledged, cited, adopted, declined &mdash; updated as known)
