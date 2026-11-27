## sqs-benchmark

**What it is.** ArroyaveLab/sqs-benchmark at b44ba79 compares three ways of building an SQS: ATAT `mcsqs`, SCRAPS (a cuckoo-search SRO optimiser) and random assignment. The test case is equimolar BCC NbVW, a 48-atom 4x3x2 supercell, with 10 repeats per method. The drivers (`examples/tdb_gen_bcc_{mcsqs,scraps,random}.py`) generate structures and fit TDBs through BLADE plus an MLIP (ORB). `scripts/compare_methods.py` scores every `bestsqs.out` with four metrics: a re-implemented mcsqs objective, a corrdump sum of squares, the Warren-Cowley pair deviation, and the relaxed energy. Pre-computed 10-run results are in `results/`.

**Environment.** venv `/tmp/arroyave/venvs/sqs-benchmark` (Python 3.12). `uv pip install -e .` worked and pulled matplotlib, numpy, pandas, pymatgen and pycalphad. I added BLADE 9d3859c (`-e /tmp/arroyave/work/BLADE`), ase, pillow and imageio. ATAT 3.52 was on PATH, with `HOME=/tmp/arroyave/home`, and everything ran through `/tmp/sbx/clean`.

### Commands and outcomes

| # | Command (cwd = copy in `/tmp/arroyave/work/sqs-benchmark`) | Result | Wall time |
|---|---|---|---|
| 1 | `uv pip install -e .` (+ BLADE 9d3859c) | OK | 4 s |
| 2 | `python examples/tdb_gen_bcc_mcsqs.py` (unmodified) | **FAIL**: `TypeError: BladeCompositions.__init__() missing 2 required positional arguments: 'system_size' and 'allow_lower_order'` | 15 s |
| 3 | `python examples/tdb_gen_bcc_random.py` (unmodified) | **FAIL**: same TypeError | 5 s |
| 4 | `python examples/tdb_gen_bcc_scraps.py` (unmodified) | **FAIL**: `ModuleNotFoundError: No module named 'blade.tools.blade_scraps_gen'` | 3 s |
| 5 | `python scripts/run_all.py --n-runs 1 --methods mcsqs` | **FAIL**: same `BladeCompositions` TypeError, raised inside the AST-patched driver | 6 s |
| 6 | `python scripts/compare_methods.py` (unmodified) | **FAIL**: `PermissionError: [Errno 13] Permission denied: '/Users'`. `out_dir.mkdir()` runs at import time on the hard-coded author path | 4 s |
| 7 | `python scripts/sqs-benchmark-mini.py <repo> <root> 3 20`: the benchmark's NbVW structure definition through BLADE 9d3859c's `BladeSQS`, 2 mcsqs processes, plus the repo's own `_write_bestsqs` random generator (loaded from the random driver with `ast`) | mcsqs **FAIL**: `Cluster file contains no clusters.`, mcsqs exit code 1. Cause: the BLADE cutoff unit bug (pair cutoff 2.0 Å < 1NN 2.74 Å; see the BLADE section) | 30 s |
| 8 | the same with my workaround that turns the normalised shells back into Å (cutoffs 5.482 / 5.249 / 4.476 Å = 5th / 4th / 3rd NN), 20 s and then 70 s per run | corrdump OK (125 clusters), but mcsqs printed nothing past `Initializing random supercells...` (162 candidate supercells) in 20 s or 70 s, nor in 45 s of plain `mcsqs` without `-ip`. Load average was 11 on 4 vCPUs | 121 s / 182 s / 45 s |
| 9 | `python scripts/sqs-benchmark-mini.py <repo> <root> 1 200`, then `... 2 200 2` for run 2 (2 procs x 200 s each) | **PASS**: first objective after about 90 s (run 1, load average 9) and 45 s (run 2, load average 5); best -46.241737 and -46.241572; `mcsqs -best` and `objective_functions.txt` OK | 220 s + 220 s |
| 10 | `python scripts/sqs-benchmark-run_compare.py <repo>/scripts/compare_methods.py <root> 2`, which runs the repo script unchanged except for `path0`, `path2` and `n_runs` (2 mcsqs + 2 random runs) | **PASS**: all four metrics for 4 SQS; `all_runs.csv` plus `bcc_method_comparison.png` and `bcc_objective_per_run.png` written; the SCRAPS and energy panels are empty | 2-4 s |

Not run: SCRAPS, whose C++/MPI optimiser lives in a separate repo (`ichasekatz/scraps-perpair`, not provided), and the MLIP relaxation and TDB fitting, which need the newer BLADE plus the ichasekatz MaterialsFramework fork, so the energy-per-atom metric is empty.

**Outcome: PARTIAL.** The analysis script (`compare_methods.py`) runs once re-pointed and reproduces the benchmark's mcsqs-vs-random ranking on freshly made SQS. None of the three generation drivers runs against the public BLADE (they need an unreleased BLADE API, SCRAPS and the MaterialsFramework fork). Here the mcsqs SQS came from public BLADE 9d3859c plus my cutoff workaround.

### Key numbers (`data/sqs-benchmark-all_runs_mini.csv`, 48-atom equimolar NbVW)

| run | native mcsqs-scale objective | corrdump objective | WC pair deviation |
|---|---|---|---|
| mcsqs 1 (2 procs x 200 s) | **-46.241737** (script recomputes -46.241731; mcsqs reported -46.241737) | -0.01200 | -0.00027 |
| mcsqs 2 (2 procs x 200 s) | **-46.241572** (script recomputes -46.241497) | -0.00948 | -0.00010 |
| mcsqs mean ± std (n=2) | -46.24165 ± 0.00012 | -0.0107 | -0.00018 |
| Random 1 (seed 1) | -46.238911 | -0.01817 | -0.00024 |
| Random 2 (seed 2) | -46.237020 | -0.02076 | -0.00083 |
| Random mean ± std (n=2) | -46.23797 ± 0.00134 | -0.0195 | -0.00054 |

Published 10-run means: mcsqs -46.2424 ± 0.0003 (20 procs x 100 s), Random -46.2367 ± 0.0009; corrdump means -0.0105 (mcsqs) and -0.0270 (random); WC -0.0002 (mcsqs) and -0.0016 (random). The ordering reproduces: mcsqs beats random on the native and corrdump objectives, and on mean WC. Our mcsqs corrdump (-0.0107) and WC (-0.00018) means match the published mcsqs values. Our native mcsqs mean (-46.2417, 2 procs on a loaded runner) is 0.0007 short of the published mean, which used 20 procs. The script's re-implemented objective matches the value mcsqs reports to within 8e-5 (6e-6 for run 1), which cross-checks its metric code. Figures: `figures/sqs-benchmark-mini-bcc_method_comparison.png` and `figures/sqs-benchmark-mini-bcc_objective_per_run.png` (the title hard-codes "ORB MLIP" though no MLIP ran). The mcsqs objective traces are in `data/sqs-benchmark-mcsqs_run{1,2}_objective_history.tsv`.

### Problems found (exact messages)
1. **Written against an unreleased BLADE API.** The drivers call `BladeCompositions` without `system_size`/`allow_lower_order`, pass `BladeSQS(..., sqsgen_in=, fixed_compositions=)`, call `sqs_gen(...)` without `iter`, put `"cutoff_mode": "nn"` in `mcsqs_params` but leave out `"use_time"` (9d3859c reads `params["use_time"]`), pass `BladeTDBGen(phases_dict=, output_dir=, terms_in=, tdb_params={... "calculator": "orb"})`, and import `blade.tools.blade_scraps_gen.ScrapsSQSGen`. None of these exist in ArroyaveLab/BLADE 9d3859c. pyproject does not list BLADE, MaterialsFramework or SCRAPS, so the README's install steps cannot be reproduced from public code.
2. **Hard-coded author paths with a side effect at import.** `compare_methods.py` sets `path0 = Path("/Users/<author>/Desktop/School/Research")` and calls `out_dir.mkdir(parents=True, exist_ok=True)` at module level, which gives `PermissionError: [Errno 13] Permission denied: '/Users'`. `results/all_runs.csv` also stores absolute `/Users/...` paths.
3. **corrdump cutoff disagrees with the mcsqs cutoff.** The script runs corrdump with `-3=5.18` and its comment says "4NN≈5.18". For BCC with a = 3.165 Å, though, 4NN = a·√11/2 = 5.249 Å, which is the triplet cutoff the mcsqs driver requests (`"3": 4`). Against a reference `clusters.out` made at the 4NN cutoff, every structure printed `warning: clusters=125 diffs=88 ... using 88`. Here the truncation barely mattered (recomputed vs reported objective differ by 6e-6 and 7.5e-5), but the corrdump objective leaves out the 5.25 Å triplets that mcsqs optimised.
4. **`find_bestsqs()` can pick up the template that `sqs2tdb -mk` writes** (a `bestsqs.out` whose sites read `a_A,a_B,a_C`) when mcsqs has not finished. corrdump then fails with `Unknown atom label: a_A,a_B,a_C` / `Unexpected vacancy` (`logs/sqs-benchmark-05-compare-mini.log`). The row quietly becomes None instead of being reported as "missing SQS".
5. **Cost.** On this shared runner (load average 5-11), a 48-atom ternary BCC mcsqs with cutoffs out to 5NN pairs, 4NN triplets and 3NN quadruplets needed 45-90 s just to initialise its 162 candidate supercells before printing an objective. With BLADE's defaults, runs shorter than about 90 s give no SQS at all on comparable hardware, and nothing warns about it.

Scripts: `scripts/sqs-benchmark-mini.py` (mcsqs through BladeSQS with the cutoff workaround, `SQSB_NO_CUTOFF_FIX=1` to disable; random baseline from the repo's own generator) and `scripts/sqs-benchmark-run_compare.py`. Logs: `logs/sqs-benchmark-01-install.log` to `logs/sqs-benchmark-09-compare-2mcsqs-2random.log`.

| sqs-benchmark | uv venv py3.12, `pip install -e .` OK (+ public BLADE 9d3859c) | 3 drivers + run_all FAIL (unreleased BLADE API / SCRAPS); compare_methods FAIL as shipped (/Users mkdir), PASS re-pointed on 2 mcsqs (2x200 s) + 2 random 48-atom NbVW SQS | PARTIAL | mcsqs -46.24165 ± 0.00012 vs random -46.23797 ± 0.00134 (published -46.2424 / -46.2367), ranking and mcsqs corrdump/WC means reproduced; SCRAPS + MLIP/TDB not runnable (non-public deps); mcsqs needs 45-90 s to first output; corrdump -3=5.18 below the 5.249 Å 4NN distance |
