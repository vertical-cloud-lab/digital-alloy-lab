# Data behind the draft panels

| File | What | Source (pinned) | Used by |
|---|---|---|---|
| `atomizer-runs-2026-11-13.csv` | The atomizer run table, Oct 2 – Nov 13, 2026 (10 runs: 5 Al, 5 C63000 bronze), copied unchanged | `atomizer-runs/runs.csv` at `8320f13` (PR #286, branch `claude/issue-219-20261125-2156`) | `figures/figS-atomizer-runs` |
| `benchmark-property-window.csv` | AlSi10Mg and Scalmalloy room-temperature tensile values from four vendor datasheets, plus the FLAIME gate targets, copied unchanged | `literature/al-lpbf-benchmark-alloys/property-window.csv` at `a25d763` (PR #285) | `figures/fig5c-draft-benchmarks` |
| `scfree-baselines-datasheets.csv` | EOS Al5X1, Höganäs Al-HS1 and Aheadd CP1 tensile rows from the vendors' data sheets (both test sets for Al5X1; 4 h and 6 h ages for Al-HS1), with `plotted` marking the rows in the draft Fig. 5c | EOS process and material data sheets, Höganäs data sheet 3312HOG-3; read and checked 2026-11-27 (this run) | `figures/fig5c-draft-benchmarks`, Table 2, SI parity table |
| `literature-alloys-campaign-paper.csv` | The campaign paper's Sc-free comparator set (data sheets and papers, each row checked against its source or marked unverifiable), copied unchanged | `al-campaign-paper/data/literature-alloys.csv` at `baca180` (branch `claude/issue-277-20261127-2117`, #277) | the reported-values front in `figures/fig5c-draft-benchmarks` |
| `bofn-prelim-summary.csv` | Mean and standard error of "best alloy printed and tested, % of true optimum" every $1,000 of spend, per policy, at κ = 0 (12 seeds) and κ = 1 (20 seeds) | `benchmarks/bofn-prelim/results/` at `3e2e167` (PR 90's branch `copilot/consider-air-force-award`, read only), normalized with that folder's own `analyze.optimum()` | `figures/fig6-draft-synthetic` |

**The run table is not yet a run record.** None of its Al rows has a weighed mass balance. The outcome classes in
`tools/make_figures.py` come from its `powder_result` and `outcome` columns and the threads cited there (#159, #219).
When the YAML run records exist (one per run, byu-vcl `run-record-template.yaml`), Fig. 2 and SI S1/S3 should be
built from those instead.

**The synthetic benchmark is not this article's result.** It is the BOFN methods paper's (#121), and the article
uses it only to lay out Fig. 6b until the twin is fitted to lab records.

Regenerate the summary: `python tools/make_figures.py --bofn-dir <path to benchmarks/bofn-prelim>` (needs torch
and botorch, because `analyze.optimum()` evaluates the hand-built truth function).
