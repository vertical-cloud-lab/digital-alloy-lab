# Round-3 Edison concept-outline submissions — task IDs

Submitted 2026-05-02. Per user instruction ("All to Edison analysis in separate
queries. Don't fetch"), each revised concept outline (commit 76a283d) was
uploaded as its own ANALYSIS task with an agency-matched program-manager
persona. **Results have not been polled.** A future session should fetch these
three task IDs and synthesize the responses into a Round-3 feedback document
analogous to `concept-outlines-mock-po-feedback.md`.

The submission script is `/tmp/edison_round3_submit.py` (not committed; the
prompt template lives in that script and was identical across the three tasks
except for the persona / agency-focus block).

| key             | persona                                                   | PDF                                  | file_id                                         | task_id                                  |
| --------------- | --------------------------------------------------------- | ------------------------------------ | ----------------------------------------------- | ---------------------------------------- |
| `nsf_dmref`     | NSF DMR Program Director (DMREF, NSF 25-508)              | `concept-outlines/01_nsf_dmref.pdf`  | `data_entry:fcb925a3-1c4a-48ef-b931-94e8aa25b2a7` | `4f3ccc3d-84c3-47a7-b8a9-52891f760ebb`   |
| `doe_ammto_cmi` | DOE EERE AMMTO PM coordinating with the CMI Hub Director  | `concept-outlines/02_doe_ammto_cmi.pdf` | `data_entry:f17907a5-713c-4f75-b0b4-be164f3080d6` | `3693bf31-7609-44fc-ad8b-c58f995ac98b`   |
| `darpa_dso`     | DARPA DSO Program Manager (Office-Wide BAA)               | `concept-outlines/03_darpa_dso.pdf`  | `data_entry:a549203e-2ef4-4264-a9ed-e6485187d9f5` | `7f0d73b0-603c-4234-8934-0335e64cb24c`   |

Each task asked the persona to address (a) first-impression, (b) program fit,
(c) partnership structure, (d) preliminary-results credibility, (e)
figures/layout/typography (Edison parses the PDF with pymupdf and sees the new
TikZ DAG), (f) concrete next-move email, (g) Genesis-Mission double-dipping
red-flags, and (h) **delta vs Round 2** (Edison reviewed the prior version on
2026-05-02 as task `115ffc21`).
