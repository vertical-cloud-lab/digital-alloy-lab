# Edison tasks recovered from #206's lost Oct 27 runs

Two `@claude` runs on #206 did hours of work on 27 Oct 2026 and pushed none of it: run
[40558407419](https://github.com/vertical-cloud-lab/digital-alloy-lab/actions/runs/40558407419) ("run 1", 18:16–20:45 UTC) lost
its token at minute 60, and run [40563168340](https://github.com/vertical-cloud-lab/digital-alloy-lab/actions/runs/40563168340)
("run 2", 18:47–21:06 UTC) hit a session limit. The Edison tasks they submitted stayed on Edison's platform. On 28 Oct
(#223) we listed this API key's trajectories (the 200 newest reach back to 7 Oct), took every task created between
18:16 and 21:06 UTC on 27 Oct, and downloaded each one through the API. Nothing was resubmitted. All five #206 tasks had
finished (`success`).

## The tasks

| Created (UTC) | Finished | Task | Job | From | Uploads | What it asked | Folder |
|---|---|---|---|---|---|---|---|
| 19:02:48 | 19:31:41 | `f14b36cf-9e08-4ed0-8fa4-6e747f3a684a` | literature (`paperqa3`) | run 2 | – | which studies measured Cu, Cu-Ni, Al bronze, NAB and Cu-Ni-Al in the same 1–90-day seawater test, and is there a measured Ni minimum to match 70-30? | [`f14b36cf-lit-same-test-corrosion/`](f14b36cf-lit-same-test-corrosion/) |
| 19:02:49 | 19:26:54 | `cfce38b0-cab4-4625-b966-0049fcb0920c` | literature (`paperqa3`) | run 2 | – | measured constants for a film model: O₂-reduction limit, i_corr decay to 30 days, β′ and α+κIII dissolution rates, Ni/Fe/Al effect on film transport | [`cfce38b0-lit-film-model-constants/`](cfce38b0-lit-film-model-constants/) |
| 19:23:52 | 19:59:29 | `009f44cb-d47e-42ba-8cb7-c279768d14ca` | Analysis (`data-analysis-crow-high`) | run 1 | 23 | why the Al and Cu benchmarks give such different results; the deposition index; corrosion-aware tiered | [`009f44cb-cu-vs-al-review/`](009f44cb-cu-vs-al-review/) |
| 19:50:14 | 20:24:34 | `92e929a9-38ce-45ff-855f-de856bce8435` | Analysis (`data-analysis-crow-high`) | run 2 | 11 | review of the physics-based truth: the corrosion fit, the CALPHAD grid, the nickel floor | [`92e929a9-physics-truth-review/`](92e929a9-physics-truth-review/) |
| 20:43:27 | 21:06:44 | `fe65c236-7b04-437b-b122-806f0ac8b9b9` | Analysis (`data-analysis-crow-high`) | run 1 | 13 | independent re-analysis of the results, statistics and figure | [`fe65c236-results-review/`](fe65c236-results-review/) |

Each query is in its folder's `query.md`. Two more tasks fall in the window but came from #219's atomizer run, not #206:
`a67d522e-7d56-4ad9-a324-5d8765ec4423` (20:26:22, `paperqa3-high`, risks of atomizing Cu-30Ni in the rePOWDER) and
`c5d7048c-574b-4721-98cd-847e0fbb0dbd` (20:26:23, `paperqa3-precedent`, precedents for ultrasonic atomization of Cu-Ni).
They are already committed on branch `claude/issue-219-20261027-2020`, so they are not repeated here. [`tasks.json`](tasks.json) has
the same table in machine-readable form.

Run 1's comment never reached "Send results to Edison", but it did send two Analysis tasks: `009f44cb` at 19:24 and
`fe65c236` at 20:43, two minutes before the run died. `fe65c236` finished at 21:06, so no run ever read its answer.

## What the answers say

**`f14b36cf`, same-test corrosion data** ([answer](f14b36cf-lit-same-test-corrosion/answer.md)). No published study
compares these alloy families against wrought C71500 in one 30-day test. The nearest same-test data:
- Lewis & LaQue 1981 ([10.2172/6255887](https://doi.org/10.2172/6255887)), reproducing mostly unpublished Inco data. Over
  30 days in clean seawater at 2 m/s, C70600 and C71500 corrode at the same rate (93.9 and 84.9 against 95.1 and 89.5 µm/y).
  Over 62 days at Wrightsville Beach, 90-10 loses 2.1 to 2.5× as much as 70-30. Over one year at 0.6 m/s the rates are
  C71500 20.3, C70600 30.5, aluminum bronze 43.2 and NAB 150 µm/y, but the bronze grades and their β content are unknown.
- Popplewell et al. 1973, as reproduced there: Cu-10Ni with 0, 0.3 and 1.5% Fe corrodes at 38.4, 33.0 and 12.2 µm/y over
  60 days.
- Yang 2019 ([10.26190/unsworks/21760](https://doi.org/10.26190/unsworks/21760)), polarization after 2 h in 3.5% NaCl:
  Cu 92.4, Cu-9.3Ni 55.0, Cu-18.8Ni 44.2, Cu-28.4Ni 29.0 and Cu-7Al 37.0 µm/y. The Ni benefit does not saturate by 10 wt%.
- LaQue's 78-day series: the late/early rate ratio is 0.7 for Cu, 0.36 for Cu-20Ni and 0.18 for Cu-30Ni.

Verdict: there is no measured basis for a hard ~6 wt% Ni cutoff. No matched 30-day test shows nickel-free aluminum bronze or
β-free NAB matching C71500, and no paired 1-hour/30-day ranking exists.

**`cfce38b0`, constants for the film model** ([answer](cfce38b0-lit-film-model-constants/answer.md)). None of the four
groups of constants is measured as the model needs them:
- There is no O₂-reduction limiting current for copper alloys in quiescent seawater.
- There is no 1 h, 1 d, 10 d and 30 d i_corr series or decay exponent. Yuan & Pehkonen, Kear, Wharton 2005 and Schüssler &
  Exner could not be retrieved.
- There is no phase-specific β′ or α+κIII rate. Dobson's 2024 thesis reports a 1,331 µm κIII path after 12 months in marina
  seawater, about 3.65 µm/day on average. Laser-deposited NAB (Zhao 2022) shows a 1.8–3.4 µm maximum depth after 21 days.
- There is no composition series for film ionic conductivity, only EIS film resistances (Huo 2025, Zhao 2022).

Treat these as priors, not measurements.

**`92e929a9`, review of the physics-based truth** ([answer](92e929a9-physics-truth-review/answer.md)). "I would not use
this model to justify excluding alloys below 10–15 wt% Ni." Its main findings:
- The run's floors (14.6 wt% with 70-30 as the bar, 9.2 with 90-10) are minima over 400,000 random designs. Optimized,
  they are **12.50 and 6.40 wt%**.
- The reference is the best simulated deposit (ρ = 0.908 for C71500, 0.978 for C70600), not a dense wrought coupon. A
  dense reference gives 15.97 and 6.97 wt%.
- Across 20 refits ([`refit_parameters_and_floors.csv`](92e929a9-physics-truth-review/outputs/review/refit_parameters_and_floors.csv))
  the floor runs from **0 to 16.7 wt% (70-30 bar) and 0 to 7.0 wt% (90-10 bar)**. Dropping the
  constructed Cu ratio and the one-year bronze of unknown grade removes the floor entirely.
- The interpolation is correct (within 7×10⁻¹³ of SciPy on 1,000 compositions). The grid has 864 unique compositions,
  810 converged and 54 non-converged Scheil runs, and 31 points without α at 900 °C, where the loader falls back to the
  nominal composition.
- The mappings are surrogates, and the Fe-rich solid at the solidus is not evidence of primary nucleants.
- Code issues: `feasible()` accepts out-of-box inputs, the 125 K crack screen (`F_SAFE`) is unused, near-zero-density
  designs can score, and the comments for `M_lo` (1 µA·day/cm² is 0.032 µm of Cu, not 0.3) and `tau` (3 days in the
  docstring, 10 days in `CAL`) are wrong.
- README numbers that need correcting: the 30-day 90-10/70-30 ratio is 0.9686, not 0.95. The Yang 2018 comparison is a
  30-day ratio, not a 10-day one. The 20% agreement is for electrical, not thermal, conductivity. The NAB liquidus is
  56 °C high, not 51.

This is the review that made run 2 retract its "restrict the space to Ni ≥ 10–15 wt%" conclusion at 21:06.

**`009f44cb`, why copper differs from aluminum** ([answer](009f44cb-cu-vs-al-review/answer.md), full report in
`outputs/outputs/report.md`). Every populated cell of `compare_tables.md` reproduces. The findings:
- At $100k, light pKGFN reaches 58.6% of the optimum against 73.2% for full-pipeline BOFN (4 wins and 16 losses, Wilcoxon
  p = 0.024). On aluminum the gap was 1.9 points.
- No high-fidelity pKGFN run existed at upload, so the light against high-fidelity comparison could not be made.
- Original tiered screening tests 0 of 80 new builds that pass immersion. Its shortlist (aluminum bronzes, median 4.15 wt%
  Ni) cannot pass at any process setting.
- With `tiered_ni_ref` (24.2%) as the baseline, pKGFN's speed-up falls from 17.3× to 2.14× (90% CI about 1.5–3.4). Full
  BOFN's is 2.99×.
- The Utah "density" gate is 0.5 on a multiplicative index (copper-rich median 0.43), not 99% relative density.

Ranked explanations of the gaps:
- The immersion and deposition landscape and the seed state account for the standard BO and random drops: the no-gate
  ablation recovers about 73% and 62% of them.
- The shortlist rule accounts for the tiered gap.
- For pKGFN, the long validation path and myopic KG: light pKGFN buys 40.5 Mines builds per seed but completes 6.15.
- The extra cost per chain explains little.

**`fe65c236`, re-analysis of the results** ([answer](fe65c236-results-review/answer.md), full report in
`outputs/outputs/report.md`). The means reproduce exactly, and regenerating `tables.md` changes no line. At (1, 1) and
$100k:

| Policy | % of J\* | Seeds |
|---|---|---|
| Full BOFN | 73.2 | 20 |
| BOFN + lot reuse | 72.0 | 20 |
| Production pKGFN | 58.9 | 7 |
| Light pKGFN | 58.6 | 20 |
| `tiered_ni_ref` | 24.2 | 20 |
| Standard BO | 14.4 | 20 |

The corrections:
- Stage selection is not shown to beat the full pipeline: −28.5 points on 7 matched seeds (nominal p = 0.047).
- "The lighter settings were not why pKGFN lags" is too strong: high minus light is −5.3 points with a 90% CI of −23.8 to
  +11.7.
- The standard errors use ddof = 0.
- Production pKGFN averaged 62 min per run (5.6× light), not 25–35 min (2.9×).
- The 17–20× speed-ups over spec tiered are uninformative, because their target is −7.7% of the optimum.
- `tiered_ni_ref` is missing from the speed-up table.
- No runs exist for (1, 0), (0, 1), `pkgfn_screen`, `pkgfn_audit`, `mines_only` or `funnel`.
- The figure shows light pKGFN, and its "Partial" label is ambiguous.

## The uploaded files: what came back and what is still lost

Every uploaded file came back, byte-for-byte as Edison holds it (sizes match Edison's metadata; sha256 in each
`uploads-manifest.json`). The one exception is `calphad_grid.csv`, which Edison stores as text with LF line endings:
418,694 bytes against the 419,559 uploaded. That is one byte for each of the 865 lines, the CRLF that Python's `csv`
writer emits by default. The data are identical.

- **Run 2's physics folder** ([`92e929a9-physics-truth-review/uploads/`](92e929a9-physics-truth-review/uploads/), 11 files):
  `truth_phys.py`, `calphad_grid.py`, `calphad_grid.csv` (the 864-composition pycalphad grid, MatCalc `mc_ni` v2.036),
  `calibrate_corrosion.py`, `calibration_fit.txt`, `check_phys.py`, `phys_tables.md`, `phys_tables_c70600.md`, `README.md`
  (the physics write-up) and the two literature answers as the run saved them (`same-test-rates.md`,
  `kinetics-constants.md`, from `physics/edison/`).
- **Run 1's code and results, as of 19:23** ([`009f44cb-cu-vs-al-review/uploads/`](009f44cb-cu-vs-al-review/uploads/), 23 files):
  - code: `bofn_alloy.py` (with the `BOFN_NOGATE` ablation), `policies.py` (`tiered_ni`, `tiered_ni_ref`, the F2 and F4
    fixes, the production Monte Carlo defaults; +70/−25 lines on `68e9a80`), `analyze.py`, `compare.py`, `landscape.py`,
    `needle.py` and `density.py`;
  - their outputs: `compare_tables.md`, `tables.md`, `settings.md`, `truth_tables.*` and the `.json` outputs of the three
    scripts;
  - run 1's README;
  - `cu_results.zip` with 252 runs: the headline cell, `tiered_ni`, `tiered_ni_ref`, the no-gate ablation and light pKGFN;
  - the aluminum benchmark's files (`al_*`, identical to `benchmarks/bofn-prelim/`) and its 164 runs.
- **Run 1's code and results, as of 20:43** ([`fe65c236-results-review/uploads/`](fe65c236-results-review/uploads/), 13 files):
  - the same `bofn_alloy.py`, `policies.py` and `analyze.py`, plus `plot.py`;
  - newer `README.md`, `tables.md` and `compare_tables.md`;
  - `results.zip` with 259 runs, now including **7 production-setting pKGFN seeds**;
  - both versions of the slide figure.

Never uploaded, and so still lost:
- **Run 2's opt-in edits** to `bofn_alloy.py`, `policies.py` and `run_sweep.py`: the `BOFN_TRUTH=phys` switch,
  `feasible_designs`, `rand_designs`, and the feasibility filter on candidate pools.
- Run 2's `plot_phys.py`, `analyze_phys.py`, `run_phys.sh`, `edison/lit_queries.py`, the `results-phys/` and
  `results-phys-ni10/` runs, and the `bofn_cu_phys_*.png` figures.
- Run 1's `run_sweep.py` resume check (Edison F9), and any pKGFN seed that finished after 20:43.

## Does `truth_phys.py` run against the grid as-is?

**Yes.** It imports only `torch`, `csv`, `math` and `os`, and reads `calphad_grid.csv` from its own folder. Run unmodified
from a copy of `uploads/` (torch 2.14.1, CPU), it reproduces `phys_tables.md` exactly:
- the grid has 864 points and none missing;
- m_ref = 0.8517 at ρ_m = 0.908 for C71500, and 0.8078 at 0.978 for C70600;
- all nine dense, β-free coupon rows match (Cu 116.3 µA·d/cm², ratio 3.46; 90-10 41.7, 1.24; NAB 43.3, 1.29; and the rest);
- J at the stored 70-30-bar optimum is 0.0891, as tabulated. Under the 90-10 bar the same design gives 0.1901, against a
  tabulated optimum of 0.1900 at nearly the same settings;
- 74.5% of 400,000 uniform designs are feasible, and the lowest passing Ni is 14.64 wt% (70-30 bar) and 9.20 wt% (90-10 bar).

`calibrate_corrosion.py` also runs (with `truth_phys.py` placed at `physics/truth_phys.py`, as it expects) and prints
`calibration_fit.txt` byte for byte.

`check_phys.py` does not run against #206's `bofn_alloy.py` (`68e9a80`, or run 1's version). It stops with
`AttributeError: module 'bofn_alloy' has no attribute 'feasible_designs'`, because it needs the lost opt-in edits. The
review's `outputs/review/check_phys_adapter.py` works around this with `truth_phys.feasible`.

## What is in each folder

| File | What it is |
|---|---|
| `query.md` | the query exactly as submitted |
| `answer.md` | the answer; for literature tasks, followed by its references and Edison's table artifact |
| `task.json.xz` | the task as `GET /v0.2/trajectories/{id}` returns it, with state blobs inlined (what `get_task(verbose=True)` reads) |
| `trajectory.json.xz` | the same with `history=true`: every agent state, i.e. the full trajectory |
| `runtime_config.json` | the task's runtime configuration, including the `data_entry` IDs of the uploads |
| `uploads/`, `uploads-manifest.json` | the uploaded files and their entry IDs, original paths, sizes and sha256 |
| `outputs/`, `outputs-manifest.json` | every file the task wrote (notebook, report, scripts, tables, figures, memory log), under its workspace path |
| `files.json` | Edison's provenance listing of those outputs |
| `_assemble.json` | what was copied, redacted and left out, file by file |

The JSON is compressed with xz rather than gzip because the history repeats itself: `fe65c236`'s 148 MB trajectory is
67 MB as gzip and 0.37 MB as xz. Read it with `xz -dk trajectory.json.xz`, or in Python with
`json.load(lzma.open("trajectory.json.xz"))`.

## What was changed or left out, and why

This repository is public, so:
- Email addresses are replaced by `<email removed>` everywhere outside `uploads/`: the account's address in the task
  records, authors' addresses quoted from papers, and a datasheet's sales address. `_assemble.json` counts them per file.
  `uploads/` contained none.
- Signed download URLs are removed from the manifests.
- These outputs are not committed. Their entry IDs and sha256 are in `_assemble.json` and the outputs manifests, so they can
  be fetched again:

| Left out | Why |
|---|---|
| `*.pyc` (6 files) | bytecode caches; `.gitignore` excludes them |
| `tmp/*.pkl` in the two literature tasks (27 and 99 MB) | PaperQA's pickled cache of parsed papers: third-party full text, and unsafe to unpickle |
| `009f44cb/outputs/outputs/fresh_random_truth_sample.npz` (53 MB) | a regenerable random sample of the synthetic truth |
| `009f44cb/outputs/outputs/buathong2024.pdf` | third-party paper PDF: [Buathong et al., ICML 2024](https://proceedings.mlr.press/v235/buathong24a.html) |
| `009f44cb/outputs/outputs/{copper_ded_porosity_source,ded_pore_mechanisms_source,method_source}.txt` | web text of third-party articles: [10.1007/s00170-024-14789-w](https://doi.org/10.1007/s00170-024-14789-w), [10.1038/s41467-024-45913-9](https://doi.org/10.1038/s41467-024-45913-9) and the PMLR page above |
| `92e929a9/outputs/review/{6255887,21760,ma11091777}.{json,txt}` | parsed full text of [Lewis & LaQue 1981](https://doi.org/10.2172/6255887), [Yang 2019](https://doi.org/10.26190/unsworks/21760) and [Yang et al. 2018](https://doi.org/10.3390/ma11091777) |

Edison lists each output of the three Analysis tasks twice, under two entry IDs, with identical bytes; each is saved once.
