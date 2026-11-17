# Edison extraction — *Explosibility of Metal Powders* (RI 6516)

Text + figure extraction of the 1964 U.S. Bureau of Mines report
**Jacobson, Cooper & Nagy, *Explosibility of Metal Powders*, Report of
Investigations 6516**, kicked off from PR #106
(branch `105-safety-considerations-of-metal-am-powder`).

Source PDF (renamed in this PR):
`literature/jacobson-explosibility-of-metal-powders-1964.pdf`

## Task

| Field | Value |
|-------|-------|
| Task ID | `537b881f-9ab9-4fab-aa49-d6b0af4b6c90` |
| Job | `job-futurehouse-data-analysis-crow-high` (ANALYSIS) |
| Data-entry (uploaded PDF) | `93c06dff-3626-4881-9dbc-cf7fdee3272b` |
| Status | success |

The PDF was uploaded with `client.store_file_content(...)` and attached to the
task via `files=["data_entry:<uuid>"]`. (Note: `create_task(files=...)` takes
`data_entry:` URIs, **not** local paths — passing a path silently attaches
nothing and the analysis crow fails at start.)

## Key artifacts

- **`artifacts/Explosibility_of_Metal_Powders_RI_6516_complete.md`** — the
  primary deliverable: full transcribed text, all 7 tables (Tables 1–4 and
  appendix A-1–A-3), all 3 figures with verbatim captions + digitized
  values/trends, an executive summary, and a section applying the findings to
  modern additive-manufacturing powder handling.
- `edison-answer.md` — the agent's final answer text (summary of what was done,
  analytical decisions, and extraction limitations).
- `artifacts/page_*.png` — rendered page images used for OCR verification.
- `artifacts/ri6516_rotated.pdf`, `ri6516_layout.txt`, `ri6516_auto.md`,
  `rot_page_*.md`, `hathi_*.bin` — intermediate OCR / layout products.
- `artifacts/537b881f-...ipynb` — the analysis notebook the crow executed.
- `artifacts_manifest.json` — full list of the 52 downloaded output entries.
- `_task_id.json` — task / data-entry identifiers for re-fetching.

## Extraction caveats (from the agent)

The source is a low-resolution, rotated public-domain scan (HathiTrust
`mdp.39015078519538`). A few characters in the widest appendix tables (the
18-column Table A-3) remain imperfect where the scan/OCR is ambiguous; these
are flagged in the document and no unreadable value was invented. Original
units are preserved, with approximate SI conversions only in the executive
summary.
