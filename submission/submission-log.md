# Submission log

> **Purpose.** Record of every formal submission of the proposed standard to a receiving body.

This log is updated at each submission. Each row captures:

- Receiving body
- Docket / reference number
- Date submitted
- Channel used
- Materials version (PRD-N, document version, commit SHA, PDF SHA-256)
- Public-comment-period close date
- Outcome (acknowledged, cited, adopted, declined &mdash; updated as known)

| # | Date | Receiving body | Docket | Channel | Materials | Period close | Outcome |
|---|---|---|---|---|---|---|---|
| &mdash; | &mdash; | (No submissions yet) | &mdash; | &mdash; | &mdash; | &mdash; | &mdash; |

---

## Notes

- Each submission's exact PDF artifacts are reproducible from the commit SHA recorded in the row. The `submission/build/render-pdf.sh` script regenerates from source; the resulting PDFs are byte-identical modulo embedded creation timestamps.
- The PDF SHA-256 fingerprint is recorded at submission time and cited in the cover letter so the receiving body can confirm receipt of the byte-identical artifact.
- Withdrawal or supersession of a prior submission is recorded as a new row with `Outcome: superseded by row N`.
