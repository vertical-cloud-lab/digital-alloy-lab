# ArroyaveLab Bayesian-optimization / ML repositories: install and test-run report (issue #235)

Scope: the 14 BO/ML repositories of github.com/ArroyaveLab assigned to this group, from shallow clones taken on
2026-11-05. Each repo got its own uv venv under `/tmp/arroyave/venvs/<name>`, CPU-only PyTorch, a copy under
`/tmp/arroyave/work/<name>` for anything that writes, and every install or third-party run went through the
scrubbed-environment wrapper `/tmp/sbx/clean` (`OMP_NUM_THREADS=1`). The machine was a shared 4-vCPU / 15 GB runner
with no GPU, so every run was scaled down (fewer iterations, smaller initial designs, fewer GP hyperparameter samples or
MC samples). Each section says exactly what was changed. Timings are wall-clock on that shared box and are only
indicative. Results are smoke tests, mostly with one or two seeds, and are not statistical comparisons.

Outcome codes: **PASS** = installs and the smallest meaningful test/demo runs (possibly after documented environment
pins or small patches); **PARTIAL** = some entry points run, others fail or need unavailable inputs; **FAIL** = nothing
runnable; **NOT RUNNABLE** = needs a licence (Thermo-Calc/TC-Python, MATLAB), an API key (OpenAI) or HPC (SLURM/CUDA).

## Headline findings

- **Closest fits for our LPBF / Al-alloy BOFN workflow.** (1) `2026-islam-rhea-mobo`: the best-engineered repo (pytest
  24/24, license-free toy). Its `CostAwareEHVI` (EHVI divided by a composition-weighted supply-risk index) is a small
  BoTorch wrapper we can reuse with an Al element table. (2) `SupplyRiskAwareDesign`: the code behind the
  supply-risk paper our proposal cites. The SR index and data are usable, but the package does not install as shipped
  (`src/` layout missing). Rebuilt, a with-SR batch EHVI campaign finds a lower-risk Pareto set (mean SR 50.7 vs 52.9).
  (3) `PCMOBO`: clean modern BoTorch constrained MOBO with bandit/LLM acquisition switching over finite pools. It runs
  cleanly. On the 40,553-alloy HEA pool, feasibility-first acquisition beat pEHVI: 12 and 14 feasible alloys found vs 0 and 0 over two seeds.
  (4) `BAREFOOT-Framework`: the lab's multi-fidelity (reification fusion) + batch BO. Conceptually the best match for
  LPBF (cheap physics models + prints), but legacy code. It needs NumPy < 1.24 and a SciPy patch and swallows errors (exits
  0 on failure). On a quiet box its single-node fusion + batch mode works: best 4.50 after 32 truth evaluations, against
  4.28 after 52 for batch-only (one seed). Under CPU contention its Ray pool slowed down about 40x.
- **Kernel selection.** `Kernels-BO` (grammar-built composite kernels plus a kernel-distance embedding) partly ran.
  Recomputed kernel distances match the shipped embedding (r = 0.9999), and a composite kernel beat RBF on both 1-D
  benchmarks. The main search notebook needs the OpenAI API, and its LPBF printability dataset is not shipped. `DGP-BO`
  (deep GP BO, CPU after stripping `.cuda()`) gave a higher hypervolume than cGP/MTGP in one seeded 5-iteration run.
- **Common breakages.** Unpinned or stale dependencies are the main failure mode: `np.float` (NumPy >= 1.24),
  `from scipy import random`, `pyDOE` renamed to `pydoe` in 1.6, `gpytorch.lazy` removed in gpytorch >= 1.12,
  `scikit-learn-extra` without wheels past Python 3.11, `pandas >= 2`, and `setuptools >= 81` breaking CBFV. Other
  recurring problems: hard-coded CUDA (`device: "cuda"`, `.cuda()`, a `uv.lock` that resolves CUDA torch), hard-coded HPC
  paths/SLURM, unpublished per-iteration inputs, and Thermo-Calc / MATLAB-only steps.
- **Bugs worth reporting upstream** (details and exact error lines in the sections). Alloy-Color-Optimization's EHVI
  price objective is sign-flipped, and fixing it raised the final HV from 0.595 to 0.816. HTMDEC's BO driver raises
  `NameError` after iteration 1. BRAVE's `priors.py` uses wrong column names and has an index bug.
  constraint-satisfaction logs a hypervolume that ignores feasibility. tamubo's shipped exactbo example does not finish
  in 10 min on CPU.
- **Repository size anomalies.** `SupplyRiskAwareDesign` is not empty (45 tracked files, ~644 KB; the API size of 0 is
  stale). `NiTi-alloy-discovery`'s 479 MB is mostly three identical copies of one 122 MB LFS `all_space.csv`.

The five repos named most relevant come first, then the other nine.

---

## tamubo

**What it is.** "TAMU Bayesian Optimization tools" (v0.0.1, src-layout package; README clone URL points at a personal
fork, `juanesfco/tamubo`). Four sub-packages: `tamubo.exactbo` (exact/certified expected-improvement maximisation by
branch-and-bound partitioning with EI upper bounds; numpy backend, optional `cupynumeric` GPU backend), `tamubo.bo`
(BoTorch/sklearn EI baselines: grid EI and gradient `optimize_acqf`), `tamubo.mobbo` (older EHVI multi-objective BO
script using `george` GPs), `tamubo.gpugp` (GPU GP components, still a stub: the package exports nothing). No tests;
runnable examples in `examples/exactbo` and `examples/bo` on a 2D three-well test function.

**Commands** (driver scripts: `scripts/tamubo-run-bo-examples.sh`, `scripts/tamubo-plot.py`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__tamubo /tmp/arroyave/work/tamubo
grep -v '^-e git+' envs/exactbo_nocp.txt > scripts/tamubo-exactbo_nocp-nogit.txt   # drop the personal-fork editable line
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/tamubo
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/tamubo/bin/python --torch-backend cpu \
   -r scripts/tamubo-exactbo_nocp-nogit.txt torch botorch==0.17.0 gpytorch==1.15.1 linear-operator==0.6 pandas pyDOE joblib -e /tmp/arroyave/work/tamubo
python examples/exactbo/minimization_2d.py      # config as shipped: max_iters 4, max_partitions 30  -> killed at 600 s
python examples/exactbo/minimization_2d.py      # config edited: max_iters 2 / 6, max_partitions 10
scripts/tamubo-run-bo-examples.sh               # examples/bo for botorch_optimize_ei, botorch_grid_ei, sklearn_grid_ei;
                                                # config edited: device "cuda"->"cpu", grid_resolution 5001->101, max_iters 5->10
uv pip install "pyDOE==0.3.8" george            # needed by mobbo
cd src/tamubo/mobbo && python main_BO.py        # n_jobs patched from cpu_count() to 2
```

**Outcome: PARTIAL -> PASS after scaling.** All three `tamubo.bo` frameworks and `exactbo` (scaled) run on CPU; the
shipped `exactbo` example config does not finish on CPU; `mobbo` runs only after adding two undeclared deps.

| Step | Result | Wall time |
|---|---|---|
| install (numpy 2.4.2, scipy 1.17.0, scikit-learn 1.8.0 pins from `exactbo_nocp.txt`; torch 2.15.0+cpu; botorch 0.17.0) | OK | 2 s (cache warm) |
| `exactbo` example, shipped config (4 iters, 30 partitions) | **timeout (rc 124) at 600 s**, stuck in iteration 3, partition 2 | 600 s |
| `exactbo`, 2 iters / 10 partitions | OK, best y = -0.901 | 29 s |
| `exactbo`, 6 iters / 10 partitions | OK, best y = **-1.8973** (dense-grid minimum -1.9102) | 223 s |
| `bo` botorch_optimize_ei, 10 iters, CPU | OK, best y = -1.8798 | 24 s (1.35 s inside BO) |
| `bo` botorch_grid_ei, 101x101 grid, 10 iters | OK, best y = -1.8912 | 12 s |
| `bo` sklearn_grid_ei, 101x101 grid, 10 iters | OK, best y = -1.8888 | 9 s |
| `mobbo/main_BO.py` (2 reps x 5 EHVI iterations, 100 LHS points, 1,000 candidates) | OK after fixes; mean HV 41.63 -> 52.24 | 41 s |

**Key numbers / plots**
- `figures/tamubo-convergence.png`: best-so-far vs iteration and cumulative compute time for the four engines.
  ExactBO reaches the best value (-1.8973 in 6 iterations) but costs 218 s of acquisition time versus 0.4-1.4 s for the
  BoTorch engines (about 150-500x more), and its box count roughly doubles per partition (5, 25, 117, ... 24,701 boxes after
  10 partitions in iteration 1).
- `data/tamubo-convergence.csv`, `data/tamubo-cpu_*.json` (per-iteration logs), `data/tamubo-mobbo-hv_curr.csv`.

**Problems found**
1. Shipped exactbo example is not CPU-feasible: with `max_partitions: 30` the run was killed at 600 s (`rc=124`) in
   iteration 3, partition 2 (`Computed EI upper bounds for 4625 target boxes`). The fitted GP length scale collapses to the
   sklearn lower bound (`ConvergenceWarning: The optimal value found for dimension 1 of parameter k1__k2__length_scale is
   close to the specified lower bound 0.01`), which loosens the EI bounds (`Max EI_hi: 6.367634, Max EI Analyzed: 0.058426`)
   and makes the partition tree explode. The committed log (`minimization_2d_withtime.json`, 2.7-9.9 s per iteration)
   was evidently produced on other hardware or settings.
2. `envs/exactbo_nocp.txt` and `envs/pytorch/requirements.user.txt` contain `-e git+https://github.com/juanesfco/tamubo.git@<sha>#egg=tamubo`,
   so `pip install -r` installs a personal fork at an old commit rather than the checkout.
3. `examples/bo/minimization_2d_config.json` hard-codes `"device": "cuda"` (and the code defaults to `"cuda"`); on a
   CPU box it must be edited to `"cpu"`. The torch path is otherwise documented only via an NVIDIA Docker image.
4. `mobbo` has undeclared dependencies and stale imports: `ModuleNotFoundError: No module named 'pyDOE'` (current PyPI
   `pydoe` 1.6.0 renamed the module to `pydoe`; needs `pyDOE==0.3.8`), then `ModuleNotFoundError: No module named 'george'`.
   It uses flat imports (`from gpModel import gp_model`) so it only runs from inside `src/tamubo/mobbo/`, spawns
   `multiprocessing.cpu_count()` joblib workers, has no seed, writes its outputs into the package directory, and names
   its EHVI results `hv_curr_rand.csv` (looks like a random-baseline name). Commented-out `/scratch/user/...` HPC paths remain.
5. `sklearn_grid_ei` does not log per-iteration `time` (the BoTorch engines do), so its cost cannot be compared from logs.
6. `tamubo.gpugp` imports cleanly but exports nothing (`dir()` is empty); `envs/gpugp.yml` and `envs/mobbo.yml` are "planned".

**Relevance to us: medium.** Useful as a reference for *certified* EI maximisation on low-dimensional problems
(2-4 LPBF process parameters), where it found a better point than gradient/grid EI at equal iterations. It does not scale
to our composition + process dimensionality on CPU, is single-objective and single-fidelity, and has no batch, cost or
supply-risk handling; the BoTorch baselines are thin wrappers we already have.

---

## BAREFOOT-Framework

**What it is.** Batch Reification/Fusion Optimization (Couperthwaite, Molkeri, Khatamsaz, Srivastava, Allaire, Arróyave,
JOM 2020, doi:10.1007/s11837-020-04396-x): multi-fidelity BO that fuses several cheap "reduced-order models" (ROMs)
with a truth model via reification (correlation-aware fusion of GPs), selects batches by k-medoids clustering of
acquisition values over many GP hyperparameter sets, and dispatches work through Ray (single node) or SLURM subprocesses
(multi-node). Flat scripts, no package, no tests; `sample_code.py` has three 2D demos (`runBatch`, `runReifi`,
`runBAREFOOT`).

**Commands** (driver: `scripts/BAREFOOT-Framework-driver.py`, which re-creates the sample configurations with smaller
budgets, caps Ray at 2 CPUs and turns the framework's swallowed exceptions into a non-zero exit)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__BAREFOOT-Framework /tmp/arroyave/work/barefoot
/tmp/sbx/clean uv venv --python 3.10 /tmp/arroyave/venvs/barefoot
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/barefoot/bin/python george imageio imageio-ffmpeg matplotlib \
    "numpy==1.23.5" pandas "pyDOE==0.3.8" ray scikit-learn scikit-learn-extra "scipy==1.11.4"
sed -i 's/^from scipy import random$/from numpy import random/' acquisitionFunc.py          # patch, see problem 1
python BAREFOOT-Framework-driver.py batch 4 100 50 10 2      # runBatch: iterLimit 10->4, hpCount 1000->100, sampleCount 50, batch 10
python BAREFOOT-Framework-driver.py full  4 100 50 10 2      # reification=True + batch=True, multiNode=0  (timeout 400 s)
TMITER=2 python BAREFOOT-Framework-driver.py full 6 20 10 5 2  # smaller full run (timeout 200 s)
TMITER=2 python BAREFOOT-Framework-driver.py full 3 20 10 5 2  # rerun on a quiet box
TMITER=2 python BAREFOOT-Framework-driver.py full 12 50 20 5 2 # reification+batch, 12 iterations (plot: scripts/BAREFOOT-Framework-plot.py)
```

**Outcome: PASS (single node) after two environment pins and one code patch.** Batch-only BO and the full
reification + batch mode both run end to end on one node. The first two fusion attempts were killed by our timeouts
while the box was saturated by other jobs; rerun on a quiet box, the same small configuration finished in 15.6 s, about
40x faster. `runBAREFOOT` itself is NOT RUNNABLE here: it writes and submits SLURM `sbatch` scripts with
`#SBATCH --mem=360G` and `cd $SCRATCH/BAREFOOT`.

| Step | Result | Wall time |
|---|---|---|
| install, Python 3.10 (ray 2.60.0, scikit-learn-extra 0.3.0, george 0.4.4) | OK | 3 s + re-pins |
| batch-only, numpy 1.26 | framework logs `CRITICAL - Optimization Code Failed` (`np.float`), **process exits 0** | 53 s |
| batch-only, numpy 1.23.5, 5 iterations x batch 10 | OK, 52 truth evaluations, best **4.278** (grid max of the truth function 5.719, i.e. 75%) | 25 s (17.7 s in BO) |
| full reification+batch, hpCount 100, 50 samples | killed at 400 s; iterations 0-3 done (15,000 acquisition evaluations each, 21-256 s per iteration), truth model not yet queried (`tmIter=5`) | 406 s |
| full, hpCount 20, 10 samples, tmIter 2 | killed at 200 s after iteration 0 (124 s; box heavily shared at the time) | 206 s |
| same, rerun on quiet box, iterLimit 3 | **OK**: truth model queried at iteration 2 (5 points), best 2.43 -> 2.88 | 22 s (15.6 s in BO) |
| full, iterLimit 12, hpCount 50, 20 samples, batch 5, tmIter 2 | **OK**: 32 truth + 71 cheap-model evaluations, best **4.500** | 101 s (95.6 s in BO) |

**Key numbers** (`figures/BAREFOOT-Framework-batch-vs-fusion.png`). Batch-only reached 4.278 after 52 truth
evaluations (75% of the grid maximum 5.719). Reification + batch reached **4.500 (79%) after 7 truth evaluations** and
stayed there through 32, while also spending 29/22/20 calls on the three cheap models
(`data/BAREFOOT-Framework-full-med-iterationData.csv`, `data/BAREFOOT-Framework-batch-it4-hp100-iterationData.csv`).
The two runs started from different random initial truth points (best -0.31 vs 2.43), and this is one seed, so it only
shows that the fusion path works, not that it is better.

**Problems found**
1. `acquisitionFunc.py:10 from scipy import random` fails on every SciPy we tried (1.9.3, 1.11.4, 1.15.3):
   `ImportError: cannot import name 'random' from 'scipy'`. It was an alias for `numpy.random`; patched to `from numpy import random`.
2. `barefoot.py:2059 ... dtype=np.float` -> `AttributeError: module 'numpy' has no attribute 'float'` on NumPy >= 1.24
   (5 occurrences in `barefoot.py`); pin `numpy<1.24`.
3. Errors are swallowed: `run_optimization` catches the exception, logs `BAREFOOT - CRITICAL - Optimization Code Failed`
   and returns, so a failed run exits with status 0. Check `BAREFOOT.log`.
4. `requirements.txt` is unpinned and `pyDOE` resolves to the 1.6 rewrite whose module is `pydoe`; the code needs
   `pyDOE==0.3.8`. `scikit-learn-extra` has no wheels past Python 3.11, so Python 3.10/3.11 is required.
5. `sample_code.runReifi` sets `reification=False` (identical to `runBatch`) and writes `data/initData` but then uses
   `calcInitData=True`, so the "ReificationOnly" demo neither fuses nor uses its file. `runBatch` builds `ROMList` but
   never passes it.
6. `ray.util.multiprocessing.Pool()` is created with no size, so it takes every CPU; Ray also writes an auth token under
   `~/.ray` and logs the host's private IP (redacted from our logs).
7. README image link and developer contacts point to a personal account; no licence for dependencies, no seeds.

**Relevance to us: high in concept, low as code.** It is the lab's original multi-fidelity + batch BO (cheap models fused
with experiments, batch selection by clustering), which is exactly the shape of our LPBF problem (Eagar-Tsai / FEM as
ROMs, prints as truth). The code is legacy (NumPy < 1.24, SciPy alias, unpinned, swallowed errors, Ray/SLURM-centric) and
slow; reimplementing the reification-fusion idea in BoTorch (multi-fidelity GP + qKG or BOFN) is a better path than reviving it.

---

## PCMOBO

**What it is.** `pcmbo` 0.1.0: constrained multi-objective BO with *portfolio-based acquisition switching* (fixed
BoTorch policies qLogPoF / qLogEHVI / qLogNParEGO / qUCB, or pEHVI/PoF on finite pools, chosen per iteration by a
bandit-UCB rule or by an LLM "arbiter" through LangGraph + OpenAI). Ships synthetic benchmarks (constrained
Branin-Currin, C2-DTLZ2, disc brake) and two finite-pool materials case studies: a 40,553-alloy Nb-Mo-Ta-V-W-Cr HEA
design space (max solidus, yield strength, Pugh ratio; min density; BCC screen) and a 3,138-candidate thermoelectric pool.
Three console entry points; no test suite, but the README gives CPU smoke commands.

**Commands** (scripts: `scripts/PCMOBO-smoke.sh`, `scripts/PCMOBO-hea-compare.sh` (seed 2 rerun: same command with `--seeds 2`), `scripts/PCMOBO-plot.py`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__PCMOBO /tmp/arroyave/work/pcmobo
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/pcmobo
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/pcmobo/bin/python --torch-backend cpu -e "/tmp/arroyave/work/pcmobo[dev]"
# README smoke runs verbatim (1 iteration each)
pcmbo-synthetic --benchmark constrained_branin_currin --policy qlogpof --seeds 1 --iterations 1 --n-init 8 --workers 1 --device cpu --acq-mc-samples 16 --acq-raw-samples 16 --acq-num-restarts 1 --results-dir runs/synthetic/smoke
pcmbo-hea  --policy pof     --seeds 1 --iterations 1 --n-init 2 ... --acq-batch-eval-size 128 --results-dir runs/hea_design/smoke
pcmbo-estm --policy qlogpof --seeds 1 --iterations 1 --n-init 3 ... --acq-batch-eval-size 128 --results-dir runs/estm_thermoelectric/smoke
# scaled-up HEA comparison: 10 initial + 15 iterations, 1 seed, 32 MC/raw samples, for pof, pehvi, bandit_ucb_switch
pcmbo-hea --policy <pol> --seeds 1 --iterations 15 --n-init 10 --workers 1 --device cpu --acq-mc-samples 32 --acq-raw-samples 32 --acq-num-restarts 1 --acq-batch-eval-size 512
```

**Outcome: PASS.** Install and all three README smoke runs succeed on CPU; the scaled HEA campaign runs for two fixed
policies and the bandit switcher. The `llm_switch` policy was not run (needs an OpenAI key; out of scope here).

| Step | Result | Wall time |
|---|---|---|
| install (torch 2.15.0+cpu, botorch 0.18.1, gpytorch 1.15.2, langchain 1.4.9, langgraph 1.2.20) | OK | 2 s (cache warm) |
| `pcmbo-synthetic --help` | OK | 2 s |
| smoke synthetic (constrained Branin-Currin, qLogPoF) | OK: 6 feasible, HV 316.6 after 1 iteration | 45 s |
| smoke HEA (PoF, n-init 2) | OK (`InputDataWarning ... std = tensor([0.])`: both initial points share the label) | 4 s |
| smoke thermoelectric (qLogPoF, n-init 3) | OK, 0 feasible after 1 iteration | 36 s |
| HEA 10 + 15 iterations: PoF / pEHVI / bandit-UCB switch | OK / OK / OK | 49 s / 41 s / 71 s |

**Key numbers** (HEA pool, seeds 1 and 2, `figures/PCMOBO-hea-feasible.png`, `data/PCMOBO-hea-campaigns.csv`).
Cumulative feasible alloys after 15 iterations:

| Policy | Seed 1 | Seed 2 | Notes |
|---|---|---|---|
| PoF | **12** | **14** | |
| bandit-UCB switch | **8** | **8** | same arm mix in both seeds: PoF 9, pEHVI 2, qLogNParEGO 2, qUCB 2; it tries every arm before exploiting |
| pEHVI | **0** | **0** | |

The feasible region is very small, so feasibility-first acquisition dominates and the bandit learns to favour it, at the
cost of its warm-start exploration. The logged scaled hypervolume stays near 1e-5 because so few feasible points exist.
The seed-2 reruns took 34 s, 37 s and 59 s.

**Problems found**
1. Namespace pollution: `pyproject.toml` installs generic top-level modules `core`, `paths`, `cli`, `engine`, `policy`,
   `benchmarks`, `acq`, `studies`, `llm_runtime` into site-packages; these can shadow or be shadowed by other packages
   (we kept it in its own venv for that reason).
2. `langchain`, `langchain-openai` and `langgraph` are hard dependencies even though only `llm_switch` uses them.
3. Torch is not declared directly (pulled via botorch), so a plain `pip install -e .` fetches the default CUDA wheel on
   Linux; use `--torch-backend cpu` or the CPU index.
4. README smoke HEA run uses `--n-init 2`, which gives a constant training label: `InputDataWarning: Data (outcome observations)
   is not standardized (std = tensor([0.], dtype=torch.float64), mean = tensor([1.], dtype=torch.float64))`.
5. `--seeds` defaults to `"1-5"`, so forgetting the flag runs five campaigns.
6. Cosmetic: `FutureWarning: torch.jit.script is deprecated` on torch 2.15.

**Relevance to us: high.** The policy-switching layer (bandit over qLogPoF/qLogEHVI/qLogNParEGO/qUCB) and the
finite-pool constrained MOBO runners are clean modern BoTorch code that could wrap our Al-alloy composition x LPBF
process candidate pools, with printability/cracking as constraints. It is single-fidelity, mostly q = 1 on the
pool studies, and has no cost or supply-risk weighting, so we would bolt on a cost-aware arm (e.g. the rhea-mobo
`CostAwareEHVI` idea) or a BOFN model.

---

## SupplyRiskAwareDesign

**What it is.** Code samples (`sradd` 0.1.0) for the paper "Supply risk-aware alloy discovery and design: A case study on
the MoNbTiVW system" (Mulukutla et al. 2024, the paper our proposal cites): rule-of-mixtures melting-point constraint,
Curtin-Maresca high-temperature yield strength, Pugh ratio / Cauchy pressure, a weighted alloy supply-risk (SR) index
with element scores and the `S1.json` indicator definition, TC-Python templates (CTE, BCC stability, density, thermal
conductivity), and a small numpy batch-MOBO ("MOBBO": RBF GP with sampled length scales, recursive EHVI,
representative-batch selection). Also ships the paper's four Pareto fronts (with/without SR, constrained/unconstrained) as
xlsx and the SR methodology workbook. No tests, no example driver, no BO campaign script.

**What the repo really contains.** GitHub's API reports size 0, but the clone has 45 tracked files (about 644 KB),
including `datafiles/*.csv` (elemental properties, elastic constants, BCC volumes, SR scores for Mo, Nb, Ti, V, W),
committed `__pycache__/*.cpython-311.pyc` and a `.DS_Store`. The API figure is just stale.

**Commands** (driver: `scripts/SupplyRiskAwareDesign-campaign.py`, plot: `scripts/SupplyRiskAwareDesign-plot.py`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__SupplyRiskAwareDesign /tmp/arroyave/work/srad-asis
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/srad
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/srad/bin/python -e /tmp/arroyave/work/srad-asis      # README path -> fails
# workaround: rebuild the src layout the pyproject expects
mkdir -p /tmp/arroyave/work/srad/src/sradd
cp -r __init__.py composition.py data.py constraints properties supply_risk mobbo datafiles /tmp/arroyave/work/srad/src/sradd/
cp pyproject.toml README.md /tmp/arroyave/work/srad/
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/srad/bin/python -e /tmp/arroyave/work/srad pytest
python -I scripts/SupplyRiskAwareDesign-campaign.py /tmp/arroyave/work/srad-run/s0 0
```

The driver evaluates the repo's own models on a 5 at.% Mo-Nb-Ti-V-W grid (every element >= 5 at.%, 3,876 alloys),
applies the repo's melting-point constraint (3,852 pass), and runs `suggest_batch` for two of the paper's scenarios:
"with SR" (maximise Curtin-Maresca YS at 1300 C and Pugh ratio, minimise SR) and "without SR" (YS and Pugh only).
Scaled down from paper settings: 10 random initial alloys, 4 batches of 5, `n_gp=10` (default 50),
`num_random_points=400` (default 2000). Seed 0, one run.

**Outcome: PARTIAL -> PASS with a packaging fix.** The README install fails as shipped; after rebuilding the `src/sradd`
layout everything imports, the data loaders work, and the batch MOBO runs end to end. Thermo-Calc helpers not run (licence).

| Step | Result | Wall time |
|---|---|---|
| `uv pip install -e .` as shipped | **FAIL**: `error: error in 'egg_base' option: 'src' does not exist or is not a directory` | 1 s |
| install with rebuilt `src/sradd` layout | OK (numpy, pandas, scipy 1.18.1, openpyxl) | 1 s |
| imports + data loaders | OK; SR scores Mo 63.97, Nb 43.79, Ti 41.33, V 60.90, W 49.17 | <1 s |
| ground truth on 3,876 alloys (YS, Pugh, SR, Tm) | OK | 1.0 s |
| campaign, with SR (3 objectives), 4 batches | OK; `suggest_batch` 34-77 s per call | ~230 s |
| campaign, without SR (2 objectives), 4 batches | OK; `suggest_batch` 5-8 s per call | ~25 s |

**Key numbers** (`figures/SupplyRiskAwareDesign-mobbo.png`, `data/SupplyRiskAwareDesign-s0-*.csv|json`):
- After 30 evaluations: hypervolume reaches **0.978** of the full-grid Pareto front without SR and **0.814** with SR (the
  3-objective front is larger, so it is harder to cover with 30 points).
- Mean SR of the found Pareto set: **50.7** with SR vs **52.9** without SR (minimum 45.6 vs 52.0). Adding SR as an
  objective steers the batch toward lower-risk alloys (Ti and Nb carry the lowest element scores), as the paper argues; one seed, so treat it as
  directional only.
- Cost: the recursive EHVI takes ~10x longer per batch with 3 objectives than with 2 (57-77 s vs 5-8 s per call on one
  thread), so going to 4-5 objectives needs a faster HV/EHVI (e.g. BoTorch box decompositions).

**Problems found**
1. Packaging mismatch: `pyproject.toml` declares `package-dir = {"" = "src"}` and package data `sradd/datafiles/*`,
   but the files sit at the repo root and there is no `src/` -> `error: error in 'egg_base' option: 'src' does not exist or is not a directory`.
   The modules import each other as `from sradd.composition import ...`, so running from the root fails too
   (`ModuleNotFoundError: No module named 'sradd'`).
2. `data.py` sets `PROJECT_ROOT = Path(__file__).resolve().parents[2]`, which also assumes the missing `src/sradd/` layout.
3. Committed build junk: `__pycache__/*.cpython-311.pyc` in five directories and `.DS_Store`.
4. README says the data are under `/datafiles/` and describes a "Quick start" that does not work; there is no example
   that runs the MOBBO loop, and no seeds or tests.
5. `Pareto_finder` and EHVI are pure-Python O(n^2) loops plus recursive HV, the main bottleneck (above).
6. The TC-Python helpers (`constraints/thermocalc.py`, `properties/thermocalc.py`) are templates with parameterised model
   names; not runnable without a Thermo-Calc licence.

**Relevance to us: high.** It is the reference implementation of the supply-risk-aware design in the paper our proposal
cites. The SR index (indicator definition in `S1.json`, element scores as CSV) is easy to extend to Al-alloy
elements (Al, Mg, Si, Zn, Cu, Sc, Zr, Er...) and to use either as an objective (as here) or as an acquisition weight (as in
rhea-mobo). The numpy MOBBO itself is slow and composition-only; we would port the SR objective into our BoTorch/BOFN stack
rather than adopt this optimiser.

---

## 2026-islam-rhea-mobo

**What it is.** `rhea-mobo` (Islam, Sarıtürk et al., 2026; software DOI 10.5281/zenodo.22258223): supply-risk-aware
multi-objective BO for six-component Mo-Nb-Ta-W-Co-Hf refractory HEAs. BoTorch `SingleTaskGP` per objective in a
`ModelListGP`, analytic 5-objective EHVI, acquisition divided by an alloy supply-risk index
`R_alloy = sum(x_i R_i)` (`CostAwareEHVI`), discrete stochastic local search over a 5 mol% feasible grid. The physics
objectives (printability, yield strength, crack susceptibility, lattice misfit, Young's modulus) need licensed
TC-Python (TCHEA7) plus MaterialsFramework/ORB; a license-free synthetic toy (`rhea_mobo.toy`) and a pytest suite are
included. The most polished, best-tested repo in this group.

**Commands** (full script: `scripts/2026-islam-rhea-mobo-run.sh`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__2026-islam-rhea-mobo /tmp/arroyave/work/rhea-mobo
# toy env, exactly as in the README but CPU torch
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/rhea-mobo
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/rhea-mobo/bin/python --torch-backend cpu -r requirements-toy.txt pytest
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-default                       # README default: 8 initial, 3 additions, seed 42
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-it15-s42 --iterations 15 --seed 42
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-it15-s7  --iterations 15 --seed 7
# full env for the test suite (NOT `uv sync`, see problems)
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/rhea-mobo-full
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/rhea-mobo-full/bin/python --torch-backend cpu -e . pytest
python -m pytest tests/ -v
python scripts/predicted_correlation.py          # RF feature importance + objective correlations from data/predictions.csv
rhea-mobo                                       # production loop: needs tc_python
```

**Outcome: PASS** (tests, toy BO and analysis script); production BO loop NOT RUNNABLE without a Thermo-Calc licence
(by design, documented).

| Step | Result | Wall time |
|---|---|---|
| toy-env install (torch 2.14.1+cpu, botorch 0.18.1, gpytorch 1.15.2) | OK (uv cache warm) | 3 s |
| pytest in toy env | collection error: `ModuleNotFoundError: No module named 'pymatgen'` (test_composition needs the full env) | 19 s |
| full install `-e .` (materialsframework 1.0.0 [orb, sqsgen], orb-models 0.7.0, pymatgen 2026.10.24, torch 2.15.0+cpu) | OK, venv 1.7 GB | 16 s |
| `pytest tests/` (full env) | **24 passed**, 0 failed | 49 s |
| toy, README default (8 init + 3 additions) | OK | 12 s |
| toy, 15 additions, seeds 42 and 7 | OK | 25 s, 34 s |
| `scripts/predicted_correlation.py` | OK, 2 figures | 15 s |
| `rhea-mobo` CLI | `ModuleNotFoundError: No module named 'tc_python'` (expected) | <5 s |

**Key numbers** (synthetic toy, 1,716-point grid, 1,621 feasible, 12-point oracle Pareto front, oracle HV 29.165, ref
point (-1,...,-1)):
- README default (8 + 3, seed 42): BO reaches **0.811** of the oracle hypervolume vs **0.722** for the paired random baseline.
- 8 + 15, seed 42: BO **0.883** vs random **0.765**; seed 7: BO **0.886** vs random **0.921** (random wins on this seed).
  With 2 seeds and a toy objective this is a smoke test only, as the README itself says; the plot
  `figures/2026-islam-rhea-mobo-toy-hv.png` shows the two curves per seed.
- `figures/2026-islam-rhea-mobo-feature-importance.png`, `figures/2026-islam-rhea-mobo-objective-correlation.png`
  (downscaled from the script's 600-dpi output) reproduce the analysis of the shipped 1,716-row `data/predictions.csv`.
- Data: `data/2026-islam-rhea-mobo-toy-*-summary.json`, `data/2026-islam-rhea-mobo-toy-it15-s*-comparison.csv`.

**Problems found**
1. `uv.lock` resolves torch with CUDA wheels on x86_64 (`{ name = "nvidia-cublas", marker = "platform_machine == 'aarch64' or platform_machine == 'x86_64'" }`),
   so the documented/CI path `uv sync --all-extras` pulls several GB of NVIDIA libraries on a CPU-only box. Workaround:
   `uv pip install --torch-backend cpu -e .`.
2. The toy env from `requirements-toy.txt` cannot run the full test suite: `tests/test_composition.py:8: from pymatgen.core import Composition` ->
   `ModuleNotFoundError: No module named 'pymatgen'`. Only `test_toy.py` etc. are toy-safe; a `pytest -m toy` marker or
   `importorskip` would help.
3. `requirements-toy.txt` pins torch 2.14.1 while `-e .` resolves torch 2.15.0; both work, so the pins are tighter than needed.
4. Production loop (`rhea-mobo`, `scripts/bo_script_full.py`) imports `from tc_python import *` at module import time,
   so even `--help` fails without TC-Python: `ModuleNotFoundError: No module named 'tc_python'`.
5. Cosmetic: `FutureWarning: torch.jit.script is deprecated` from the linear-operator / gpytorch stack on torch 2.14+.
6. Config defaults (`config.py`: 50 initial samples, 200 iterations, 20 restarts, 50 raw samples) are paper-scale; the
   original campaign history is not archived (README says so), so the paper's hypervolume trajectory cannot be replayed.

**Relevance to us: high.** It is the closest drop-in for supply-risk-aware acquisition: `CostAwareEHVI` (EHVI divided by
a per-candidate index) is a ~30-line BoTorch wrapper we could reuse with an Al-alloy element risk/cost table, and the
discrete-grid local search fits composition grids. It is sequential (q=1), single-fidelity and composition-only (no
process parameters), so for LPBF we would add process dims and swap EHVI for qLogNEHVI or a multi-fidelity/BOFN model.

---

## DGP-BO

**What it is.** The Code Ocean capsule export for "Hierarchical Gaussian Process-Based Bayesian Optimization for Materials Discovery in High Entropy Alloy Spaces" (Acta Mater., https://doi.org/10.1016/j.actamat.2025.120908; data at https://doi.org/10.5281/zenodo.15149719). It runs multi-objective EHVI-BO over the FCC FeCrNiCoCu space with three surrogates: independent GPs (cGP), a multi-task GP (MTGP) and a 2-layer deep GP (DGP, isotropic or heteroscedastic). It is plain gpytorch, with no BoTorch at run time. The ground truth comes from bundled HDF5 lookup tables (`5space-*.h5`; for example TEC and bulk modulus).

**Declared dependencies.** `environment/Dockerfile` and `gptor2_req2.yml` pin a full conda stack (CUDA 11.8): Python 3.12.3, pytorch 2.2.2, gpytorch 1.11, linear_operator 0.5.1, botorch 0.11.1, numpy 1.26.4, pandas 2.2.2, scipy 1.13.1, scikit-learn 1.4.2, h5py, pytables, pyDOE 0.3.8 and george 0.4.0. The yml's `name:` is an HPC scratch path.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__DGP-BO /tmp/arroyave/work/DGP-BO
/tmp/sbx/clean bash -c "uv venv --python 3.12 /tmp/arroyave/venvs/DGP-BO && uv pip install --python /tmp/arroyave/venvs/DGP-BO/bin/python --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple --index-strategy unsafe-best-match torch==2.2.2 gpytorch==1.11 linear_operator==0.5.1 botorch==0.11.1 numpy==1.26.4 pandas==2.2.2 scipy==1.13.1 scikit-learn==1.4.2 h5py tables pyDOE==0.3.8 joblib tqdm matplotlib"
/tmp/sbx/clean bash -c "uv pip install --python /tmp/arroyave/venvs/DGP-BO/bin/python george emcee"   # george is imported by gpModel.py
cd /tmp/arroyave/work/DGP-BO/code && bash /tmp/arroyave/results/bo/scripts/DGP-BO-patch.sh             # makes *-cpusmall.py copies
# each run: /tmp/sbx/clean timeout 300 bash -c "cd .../code && NBO=<n> NJOBS=2 python -u <script> 1"
NBO=10 python -u gp-tec-MO-11-cpusmall.py 1      # cGP-BO
NBO=10 python -u mtgp-tec-MO-11-cpusmall.py 1    # MTGP-BO
NBO=5  python -u dgp-iso-tec-MO-11-cpusmall.py 1 # DGP-BO
python -u dgp-het-tec-MO-11-cuda.py 1            # the capsule's own entry point ('code/run'), unpatched -> fails on CPU
python -u dgp-het-tec-MO-11-cpu.py 1             # same, with .cuda() stripped and n_jobs=2 (last line of DGP-BO-patch.sh); its own loop is range(2)
python -I /tmp/arroyave/results/bo/scripts/DGP-BO-summarize.py /tmp/arroyave/work/DGP-BO/code /tmp/arroyave/results/bo
SEED=0 NBO=5 python -u {gp,mtgp,dgp-iso}-tec-MO-11-seeded.py 0   # seeded copies, identical initial design
python -I /tmp/arroyave/results/bo/scripts/DGP-BO-summarize-seeded.py /tmp/arroyave/work/DGP-BO/code /tmp/arroyave/results/bo
```
**Scale-down and patches**, all in `scripts/DGP-BO-patch.sh` and applied to copies:
- The BO loop drops from **500 to 10 iterations** (cGP, MTGP) and **to 5** (DGP).
- The EHVI joblib pool drops from `cpu_count()` to 2 workers.
- `.cuda()` calls are stripped: four lines, mostly comments, in the MTGP and DGP-iso scripts, and 40 lines in the capsule's `dgp-het-tec-MO-11-cuda.py`.

The GP training epochs (500 Adam steps, 200/200/100 for DGP retraining) and the 550-point random Dirichlet candidate set per iteration are unchanged.

**Outcome: PASS with a mechanical CPU patch.** The capsule's entry point `code/run` → `dgp-het-tec-MO-11-cuda.py` (the heteroscedastic DGP, the paper's main method) is CUDA-only as shipped and fails on CPU. After a `sed` that strips its 40 `.cuda()` calls, it runs to completion on CPU at the capsule's own budget of 2 BO iterations. The cGP, MTGP and DGP-iso variants also run end-to-end on CPU at reduced BO budgets. Every run writes its pickled HV, query, mean and std traces.

**Timings.** Install took about 6 s, plus 1 s for george. cGP-BO ran 10 iterations in **49 s**, MTGP-BO 10 iterations in **53 s**, DGP-BO (iso) 5 iterations in **185 s**, about 35 s per iteration for the 2-layer DGP on 2 CPUs, and the capsule entry (DGP-het, 2 iterations) in **36 s**.

**Key numbers** (`data/DGP-BO-hv-traces.json`, `figures/DGP-BO-hv-trace.png`). Hypervolume of the observed Pareto front, in raw objective units:
- cGP: 7781 → **8138** after 10 iterations
- MTGP: 7268 → **7771** after 10 iterations
- DGP-iso: 5492 → **7565** after 5 iterations, the largest gain per iteration
- DGP-het (capsule entry, CPU): 7825 → **8372**, two recorded HV points

Each method above starts from a *different* random pair of alloys, because nothing is seeded (see problem 4). These runs show that the pipelines work. They do not rank the methods.

**Seeded comparison.** I added a one-line seed to each copy (`SEED=0`, see `DGP-BO-patch.sh`) so that all three surrogates start from the **identical** two alloys, where HV = 7593. Each then ran 5 BO iterations: cGP in 25 s, MTGP in 20 s and DGP-iso in 120 s. Final HV (`data/DGP-BO-hv-traces-seed0.json`, `figures/DGP-BO-hv-trace-seed0.png`):
- cGP: 7593 → **7760**
- MTGP: 7593 → **7600**
- DGP-iso: 7593 → **9138**

This single seed agrees with the paper's claim that DGP-BO beats cGP-BO on this problem. One seed and 5 iterations are only anecdotal, and the 550 random candidates drawn each iteration differ between methods after the first query.

**Problems found**
1. The capsule entry point is CUDA-only: `AssertionError: Torch not compiled with CUDA enabled` (from `torch/cuda/__init__.py`, `_lazy_init`, on the first `.cuda()` in `dgp-het-tec-MO-11-cuda.py`). Log: `logs/DGP-BO-codeocean-run-cuda.log`. Stripping `.cuda()` is enough to run it on CPU (log `logs/DGP-BO-dgp-het-cpu.log`). Its `********************exception**********` prints are harmless: they come from the Dirichlet sampler (`dirlet5D`) re-drawing points whose 1/32 rounding does not sum to 1.
2. Missing dependency: `ModuleNotFoundError: No module named 'george'` (`gpModel.py`, line 8). It is in the conda yml but easy to miss in a pip install. `george` 0.4.4 from PyPI works.
3. It needs the old gpytorch. Every script does `from gpytorch.lazy import DiagLazyTensor`, and with current gpytorch 1.15.2 that gives `ImportError: cannot import name 'DiagLazyTensor' from 'gpytorch.lazy'` (log `logs/DGP-BO-gpytorch-latest-import.log`). `DiagLazyTensor` is imported but never used in any script (grep), so deleting the import line would likely allow a current gpytorch.
4. No seeding anywhere: the initial design is `dirlet5D(2,5)/32` and candidates come from `np.random` with no seed, so runs are not reproducible. Output names come from `sys.argv[0][:-3]+sys.argv[1]`, so a run without an index argument crashes or, in the cuda script, writes to `../results/test1`.
5. Six near-duplicate 600–800-line scripts (`*-MO-11` vs `*-new-MO-01`, iso vs het, cuda vs not) with module-level code and no functions or CLI. There is also an empty `main.py` (1 line). `smoke_test = ('CI' in os.environ)` silently drops training to 1–2 epochs if the environment sets `CI`, which GitHub Actions does.
6. Warnings: `SyntaxWarning: invalid escape sequence '\-'` in pyDOE 0.3.8 on Python 3.12, and a sparse-tensor `UserWarning` from the DGP's `summing_matrix`.

**Relevance to us.** Medium to high for *ideas*, low for *code reuse*. MTGP and DGP surrogates that share information across correlated properties (for example density, relative density, hardness and cost) are exactly what a BOFN graph would replace or complement. The paper's point about exploiting differences in query cost between properties maps onto our multi-fidelity, cost-aware LPBF setting. The implementation is script-style and CUDA-bound. Reimplementing MTGP in BoTorch (`MultiTaskGP`, `KroneckerMultiTaskGP`) is easier than adapting this code.

---

## Kernels-BO

**What it is.** "Bayesian Optimization over Kernel Space" (Zenodo https://doi.org/10.5281/zenodo.18189227). The pipeline has four steps:
1. A grammar builds composite GP kernels from SE, PER and RQ with + and ×. Depth 2 gives 237 expressions.
2. Each pair of kernels gets an expected √JS distance, averaged by QMC over the hyperparameters.
3. Classical MDS embeds the kernels in 15-D.
4. BO runs in that embedding to *select a kernel* by log marginal likelihood (LML). It is compared against random search and an LLM-guided GA (gpt-4o-mini).

`application/` then uses the selected composite kernels for downstream BO, comparing them against an RBF baseline. The final application cell is LPBF printability multi-objective BO (qEHVI), which needs in-house data.

**Declared dependencies.** No requirements file. The README lists Python ≥ 3.9, NumPy, SciPy, PyTorch, GPyTorch, BoTorch, scikit-learn and matplotlib. The notebooks also import seaborn, pandas, tqdm.notebook (which needs ipywidgets), `openai` and `python-dotenv`.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__Kernels-BO /tmp/arroyave/work/Kernels-BO
/tmp/sbx/clean bash -c "uv venv --python 3.12 /tmp/arroyave/venvs/Kernels-BO && uv pip install --python /tmp/arroyave/venvs/Kernels-BO/bin/python --torch-backend cpu torch gpytorch botorch numpy scipy scikit-learn matplotlib seaborn pandas tqdm ipywidgets ipykernel nbconvert nbclient jupyter_client"
# (1) Kernel-space pipeline (main/input_space.ipynb logic) on a subset, checked against the shipped output/kernels_JS.csv
/tmp/sbx/clean timeout 300 /tmp/arroyave/venvs/Kernels-BO/bin/python -I /tmp/arroyave/results/bo/scripts/Kernels-BO-input-space-driver.py /tmp/arroyave/work/Kernels-BO /tmp/arroyave/results/bo 40 32
# (2) Application notebook, scaled down, executed headless (scripts/Kernels-BO-scale-notebook.py makes BO_small_dump.ipynb)
/tmp/sbx/clean timeout 480 bash -c "cd /tmp/arroyave/work/Kernels-BO/application && python -m jupyter nbconvert --to notebook --execute --allow-errors --ExecutePreprocessor.timeout=600 --ExecutePreprocessor.kernel_name=python3 --output BO_small_dump_executed.ipynb BO_small_dump.ipynb"
```
Resolved versions: torch 2.15.0+cpu, gpytorch 1.15.2, botorch 0.18.1, linear-operator 0.6.1 and numpy 2.5.4, all on Python 3.12. The latest stack works.

**Scale-down**
- (1) **40 of the 237** depth-2 kernels, chosen at random with seed 0, and **32 instead of 128** QMC samples per pair: 780 pairs instead of 27,966.
- (2) `num_trials` 5→2 and `num_queries` 30→10 in the two 1-D benchmark cells. I added one cell after each that dumps the best-so-far traces to JSON and PNG, because `MPLBACKEND=Agg` suppresses inline plots. The kernelspec changed from `bo` to `python3`.

**Outcome: PARTIAL.**
- (1) **PASS.** The pipeline reproduces the shipped embedding.
- (2) **PASS** for the Ackley-like and Dropwave-like 1-D benchmarks. **NOT RUNNABLE** for the printability cell: `FileNotFoundError: [Errno 2] No such file or directory: 'Printability_Data.csv'`, followed by `NameError: name 'mean_hv_composite' is not defined` in the plot cell.
- (3) `main/kernels-BO.ipynb`, the actual kernel search with BO, random and LLM-GA, was **not run**. It creates `OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))` and calls `gpt-4o-mini` for the GA arm, with `N_ITER = 50` per arm and several mutation rates per depth setting. That needs an external paid API and is far beyond the time budget.

**Timings.** Install took about 1 s from cache. (1) took **151 s** in total: 143 s for 780 pairs × 32 samples, or **5.7 ms per QMC sample**. Extrapolated, the notebook's full distance matrix (237 kernels × 128 samples) would take **about 5.7 h** on one core. (2) took **72–80 s** per notebook execution.

**Key numbers** (`data/Kernels-BO-input-space.json`, `figures/Kernels-BO-input-space.png`, `data/Kernels-BO-application-*-traces.json`, `figures/Kernels-BO-application-*-trace.png`)
- The grammar generates **237** kernels, matching the notebook's recorded output.
- MDS (k=15) on the 40-kernel subset: parity R² **0.9951**, relative reconstruction error 1.6e-2. The notebook reports R² 0.9999 on all 237.
- **Reproduction against the shipped `output/kernels_JS.csv`.** The squared distances I recomputed match the squared Euclidean distances in the shipped 15-D embedding with **Pearson r = 0.9999 and Spearman 0.9998** over 780 pairs. Mean D is 0.0642 here and 0.0641 shipped.
- Application, 1-D negative Ackley (maximum 0), 10 initial points + 10 EI queries, 2 trials. The composite kernel `(RQ+RQ)×RBF` reached a best of **−0.005 and −0.010**. The RBF baseline reached **−0.022 and −0.054**.
- 1-D Dropwave-like (maximum 1.0), 8 initial points + 10 queries, 2 trials. The composite `RQ+(RQ+RBF)` reached **0.930 and 0.934**. RBF reached 0.906 and 0.882.
- For context, the shipped kernel-search summary for Ackley (`output/kernel-opt_llm-pm-opt/Ackley/.../summary.txt`) shows **RBF-BO, HyperKappa-BO and random search tied at LML −1.5002 ± 0.0000**. The LLM-GA arms score between −745 and −2139.

**Problems found**
1. **Redundant search space.** Only **71 of the 237** grammar kernels are distinct once the commutativity and associativity of + and × are taken into account. The grammar adds both `(e + b)` and `(b + e)`, and both `(e * b)` and `(b * e)`. My run found 13 of 780 pairs with D < 1e-10. BO, random search and GA over kernel space therefore spend evaluations on duplicates.
2. The "√JS distance between kernels" (`distances/js.py`) is computed between the **normalized eigenvalue spectra** of the two Gram matrices, not between the GP distributions N(0, K₁) and N(0, K₂). It ignores eigenvectors and is scale-invariant, so kernels with equal spectra but different structure, or ones that differ only in output scale, collapse to distance 0. This is a methodological caveat, not a crash.
3. The main search notebook depends on an LLM: `from openai import OpenAI`, `load_dotenv()`, `model="gpt-4o-mini"`. The empty-key default `os.getenv("OPENAI_API_KEY", "")` fails only when the GA arm runs.
4. The printability data (`Printability_Data.csv`), the in-house thermal-history data and the in-house benchmark data are not shipped, so the materials application cannot be reproduced.
5. Notebook hygiene. The kernelspec is named `bo`, which needs `--ExecutePreprocessor.kernel_name=python3`. The negative-Ackley objective is named `forrester_1d`. There is a stray empty file `application/a`. The shipped CSV has an index column that the current `export_kernel_embedding(..., index=False)` would not write.
6. Warnings. `UserWarning: Converting a tensor with requires_grad=True to a scalar` comes from `js.py:19`. BoTorch raises a `NumericsWarning` 80 times, saying `ExpectedImprovement` has known numerical issues and recommending `LogExpectedImprovement`. NumPy 2 raises a `DeprecationWarning` 41 times (`__array_wrap__ must accept context and return_scalar arguments`), because the Dropwave objective `y = (1 + np.cos(12*x)) / (0.5*x**2 + 2)` applies numpy functions to torch tensors.

**Relevance to us.** High for kernel selection. A precomputed kernel embedding plus a cheap LML-driven search is a practical way to choose kernels for each BOFN node, for example process → melt-pool and composition → property, instead of defaulting to Matern-5/2. Deduplicate the grammar first and recompute D in a few hours on a small grid. The printability application (LPBF, qEHVI with composite kernels) is the closest match to our workflow, but it is not reproducible without their data.

---

## constraint-satisfaction

**What it is.** Campaign scripts for constrained multi-objective active learning over a fixed pool of 40,553 refractory HEA compositions (Nb-Mo-Ta-V-W-Cr, pre-computed CALPHAD/property columns in `design_space.csv`). Six policies share one code base: feasibility-first with physics priors as GP mean (`campaign_const_w_priors.py`), the same without priors, pEHVI x P(BCC), EHVI x POF, EHVI x correlated POF (Gaussian copula), and random. Surrogates are scikit-learn GPs (ARD RBF + white noise, `n_restarts_optimizer=10`).

**Install.** Python 3.11 (as in `constraint-satisfaction.yml`), unpinned scikit-learn / SciPy stack; resolved to numpy 2.4.6, pandas 3.1.1, scikit-learn 1.9.1, scipy 1.17.1, matplotlib 3.11.2. 3 s with a warm uv cache, no problems.
```
uv venv --python 3.11 /tmp/arroyave/venvs/constraint-satisfaction
uv pip install --python /tmp/arroyave/venvs/constraint-satisfaction/bin/python scikit-learn matplotlib pandas numpy scipy openpyxl
```

**Run (scaled down).** Defaults are seeds 1-200, 100 iterations, 25 workers. I ran five policies with `--seeds 1-2 --iterations 20 --workers 2 --plot-every 10` (driver: `scripts/constraint-satisfaction-run.sh`), then the repo's own `plot_metrics.py --auto` and my summary script `scripts/constraint-satisfaction-summarize.py`.
```
/tmp/sbx/clean bash scripts/constraint-satisfaction-run.sh
cd /tmp/arroyave/work/constraint-satisfaction && python plot_metrics.py --auto --out-dir plots_metrics
```
A single-seed smoke test (`campaign_const_w_priors.py --seeds 1 --iterations 10 --workers 1`) took 16 s.

**Outcome: PASS.** All five scripts ran to completion with exit code 0 and no warnings. Wall times (2 seeds x 20 iterations, 2 workers): const_w_priors 23 s, const_NO_priors 24 s, pEHVI 26 s, EHVI x POF 35 s, random 32 s. `plot_metrics.py --auto` wrote 10 metric plots. **`campaign_ehvi_pofcorr.py` is far slower.** Run with the same settings, it hit the 300 s `timeout` after only 3 and 2 iterations (seeds 1 and 2), against 20 iterations in 23-35 s for the other scripts. The bottleneck is the Gaussian-copula POF, which calls `scipy.stats.multivariate_normal(...).cdf` (4-D, Genz integration) on all ~40k pool points at every iteration (line 732). So that policy alone took over 100 s per iteration here (`logs/constraint-satisfaction-run-campaign_ehvi_pofcorr.log`).

**Key numbers** (`data/constraint-satisfaction-summary.csv`, `figures/constraint-satisfaction-hv.png`, `figures/constraint-satisfaction-repo_plot_metrics-TrueMeasPass_All_With_BCC.png`):
- Only **24 of 40,553** pool points satisfy every constraint (solidus, density, yield strength, Pugh ratio, single-phase BCC).
- Truly feasible alloys found after 20 iterations (mean of 2 seeds): const_w_priors **13.0**, const_NO_priors 12.5, EHVI x POF 5.0, pEHVI **0**, random **0**. Final feasibility-classifier F1: 0.81 / 0.44 / 0.68 / 0.19 / 0.00.
- Fixed-range scaled hypervolume shows the opposite ranking (pEHVI 4.98 > random 4.00 > EHVI x POF 3.61 > no-prior 3.06 > with-prior 2.50). The logged HV is computed over measured points whether or not they are feasible, so in this setting it rewards policies that ignore the constraints. Use the feasibility counts, not HV, when comparing policies.

**Problems found.**
- No dependency or path problems. The scripts take a `--data-path` flag, and `design_space.csv` ships with the repo, so nothing is missing.
- EHVI x POF and pEHVI log very large acquisition values early in a run, for example `[Seed 2, Iter 001] idx=40345 | PHASE-ONLY (non-BCC) | Pareto?=No | acq=3.071e+18`. This looks like an unnormalised EHVI term before the GP has data. It is not fatal, but it makes the first picks effectively arbitrary.
- `plot_metrics.py` hard-codes three directory names (`results_const_no_prior`, `results_const_prior`, `results_opt`); it only works on other names through `--auto`.
- The default `--workers 25` would oversubscribe most machines; set it explicitly.
- `campaign_ehvi_pofcorr.py` takes over 100 s per iteration on a 40k-point pool because of `mvn.cdf(z[i:i + POF_BATCH])` (line 732). At the default 200 seeds x 100 iterations that is out of reach without subsampling the pool or using a cheaper joint-feasibility approximation.

**Relevance to us.** High. This is the clearest ArroyaveLab example of **constraint-first BO with physics priors as GP mean functions**. It maps directly onto LPBF printability constraints (keyhole/lack-of-fusion/cracking) and Al-alloy composition constraints, with Thermo-Calc or Eagar-Tsai predictions as priors. It works on a discrete pool and does one point per iteration (no batch), in plain scikit-learn rather than BoTorch.

---

## BRAVE

**What it is.** Code, data and manuscript for HTMDEC Campaign 2 (DOI 10.5281/zenodo.21253553). It does batch Bayesian optimization over Al-V-Cr-Mn-Fe-Co-Ni-Cu with five mechanical objectives. Each objective's GP (george, SE kernel) is built on a prior mean: CatBoost models trained on the lab's database, plus a Peierls-Nabarro-type yield-strength model. The yield-strength sources are fused by reification. The acquisition is constraint-weighted EHVI, using GP-classifier feasibility probabilities, and the batch is chosen by k-medoids over the argmax picks from 1000 hyperparameter samples.

**Install.** Python 3.11 with the pinned `requirements.txt` (numpy 1.26.4, scipy 1.17.1, scikit-learn 1.6.1, scikit-learn-extra 0.3.0, george 0.4.1, catboost 1.2.10, CBFV, PyQt5). All came as wheels in 4 s from a warm cache, george included. One undeclared dependency surfaced at run time (see Problems).
```
uv venv --python 3.11 /tmp/arroyave/venvs/BRAVE
uv pip install --python /tmp/arroyave/venvs/BRAVE/bin/python -r requirements.txt
uv pip install --python /tmp/arroyave/venvs/BRAVE/bin/python "setuptools<81"   # needed by CBFV (pkg_resources)
```

**Runs.**
1. `make figures PY=/tmp/arroyave/venvs/BRAVE/bin/python` in a work copy: **PASS**, 151 s. All 7 data-driven figure scripts regenerated `fig_08/12/13/14/16/18/19` from `data/HTMDEC_Y2_db.xlsx`. Log: `logs/BRAVE-make_figures.log`; figures: `figures/BRAVE-fig_19_v_ys_feasibility-regenerated.png`, `figures/BRAVE-fig_14_boxplot-regenerated.png`.
2. BBO pipeline smoke test (`scripts/BRAVE-make_inputs.py`, `scripts/BRAVE-smoke*.sh`). The per-iteration campaign inputs (`o{1..5}_GT_y.csv`, `lhp.csv`, `tested_alloys.csv`, `feasibles.csv`, `probs.csv`, ...) are not in the repo ("available on request"). I built stand-ins: the 67 Year-2 rows of the database as tested alloys, their measured properties as objectives, 180 random 5 at.% compositions as candidates, and random length-scales. Then:
   - `prior_eval.py` (trains the 3 CatBoost priors and queries them) **failed as shipped**; it passed after two patches, taking 85 s.
   - `main.py` with `N_GP` 1000 -> 2, `Batch_size` 16 -> 4 -> 2 and `n_jobs` cpu_count -> 2, with `YS_pb` stubbed to zeros: **PASS**, 128 s, and wrote `x_query.csv`, `all_candidates.csv` and `all_improvements.csv`. An earlier attempt with `N_GP=10` timed out at 400 s after 4 of 10 hyperparameter samples. Five-objective EHVI by recursive hypervolume costs about 30-75 s per hyperparameter sample for 180 candidates on 2 cores, so the published N_GP=1000 over the full candidate space is an HPC-scale job.
   - `Probability_calculations/main.py` on a 20,000-point stand-in space: **FAIL** because of a hard-coded size (below).

**Outcome: PARTIAL.** The figures reproduce. The BBO loop runs end to end only after three fixes and with stand-in inputs. The feasibility classifier cannot run on any space other than the original 1,490,129 points, and the Peierls-Nabarro prior cannot run at all.

**Key numbers** (`data/BRAVE-smoke-results.json`):
- From the figure script: Campaign 2 has 48 alloys, 33 feasible (FCC); the YS-vs-V regression on the feasible set gives r = 0.836, slope 8.3 MPa/at.% V; the failure rate is 1.00 at 16 at.% V.
- CatBoost priors on the 180 candidates: YS median 379 MPa (range 257-602), elongation median 0.32, UTS/YS median 1.93.
- Smoke-test batch: 2 picks, with constraint-weighted EHVI 189 and 202 (normalized units).

**Problems found** (exact errors):
- An undeclared dependency: `File ".../CBFV/composition.py", line 7, in <module> import pkg_resources` -> `ModuleNotFoundError: No module named 'pkg_resources'`. The fix is `setuptools<81`, which `requirements.txt` does not list.
- `priors.py` uses column names that are not in the shipped database: `KeyError: 'YS (MPa)'`. The database uses `Yield Strength (MPa)`, `UTS/YS` and `Elong_T (%)`, not `YS (MPa)`, `UTS / YS` and `EL (%)`.
- After renaming the columns, an index-alignment bug appears: `_catboost.CatBoostError: Length of label=132 and length of data=141 is different.` The filtered frame keeps its original index, and `FeatureGenerator`'s `pd.concat` then pads rows. Fixed with `.reset_index(drop=True)` after each filter.
- `HT_FCC_YS.py` reads a data file that is not in the repo: `FileNotFoundError: [Errno 2] No such file or directory: 'table.dat'`. So the `YS_pb` prior, which `main.py` imports, cannot run.
- `Probability_calculations/main.py` hard-codes the space size (`range(149)`, `reshape(1490129,1)`): `ValueError: cannot reshape array of size 20000 into shape (1490129,1)`. Its docstring also says 1 core and 50 GB of memory.
- `main.py` sets `n_jobs=multiprocessing.cpu_count()` (joblib), which oversubscribes shared machines. It uses flat sibling imports and needs `PYTHONPATH=..`, as the README says.

**Relevance to us.** High as a design pattern: batch, multi-source/prior-informed, constraint-weighted EHVI with k-medoids batch selection, used on a real campaign of 16 alloys per batch. The fusion and feasibility pieces map onto multi-fidelity process-parameter or composition BO for LPBF. As shipped it is not a reusable library: it is a script tied to its campaign data, and it needs the fixes above. The CatBoost priors and the 5-objective EHVI are too slow for large spaces without porting to BoTorch-style batch acquisition.

---

## HTMDEC

**What it is.** Code from HTMDEC Campaign 1 (DOI 10.5281/zenodo.15027725), a high-throughput HEA discovery effort. It contains a MATLAB batch-BO implementation (EHVI, GP classifier, `.mat` iteration data); a Python port, `bbo_python/`, which runs a self-contained 2-objective demo on a 1000-alloy composition space; a composition-partition generator (`htmdec_code_01_generate_partition*.py/.ipynb`); and the campaign master table (`HTMDEC_MasterTable_Iterations_v4.xlsx`). The README is one line, and there is no dependency file.

**Install.** No dependency file. From the imports I used Python 3.11 with numpy 1.26.4, pandas 2.2.3, scipy, matplotlib, scikit-learn 1.6.1, scikit-learn-extra 0.3.0, umap-learn, tabulate and openpyxl, plus nbconvert/ipykernel to run the notebook. It installed in under 1 s from cache with no problems.
```
uv venv --python 3.11 /tmp/arroyave/venvs/HTMDEC
uv pip install --python /tmp/arroyave/venvs/HTMDEC/bin/python numpy==1.26.4 pandas==2.2.3 scipy matplotlib scikit-learn==1.6.1 scikit-learn-extra==0.3.0 umap-learn tabulate openpyxl nbconvert nbclient ipykernel
```

**Runs** (driver `scripts/HTMDEC-run.sh`; patches in `scripts/HTMDEC-package_BBO_single_iteration.patch` and `scripts/HTMDEC-graph_result.patch`).
- `bbo_python/package_BBO_single_iteration.py` as shipped: **FAIL** (`NameError`, below). With three small patches (iteration number from `$ITER`, a fixed `opt_folder`, and loading the iteration file before first use), **5 consecutive BO iterations PASS** at the shipped settings: 100 GP hyperparameter samples, batch 20, 1000-alloy space, maximizing density and heat capacity. They took 11-38 s each, 123 s in total.
- `bbo_python/graph_result.py`: **FAIL** as shipped, with a SyntaxError on Python 3.11 and a hard-coded missing input file. After patching both it still failed with a `KeyError: 'Pareto'`. I wrote my own convergence plot (`scripts/HTMDEC-convergence.py`), which uses the repo's own `pareto_maximum`/`hypervolume`.
- `htmdec_code_01_generate_partition_v3.ipynb`, executed headless with nbconvert: **PASS**, 6 s.
- `htmdec_code_01_generate_partition.py`: **PARTIAL**. The partition part runs, then the script fails at line 721 (below).
- `matlab_implementation/` (EHVI, classifier, iteration `.mat` files): **NOT RUNNABLE**, since MATLAB is not available.

**Outcome: PARTIAL.** The Python BO demo and the notebook run. The BO driver, plot script and `.py` export each need fixes, and the MATLAB code, which is the real campaign implementation, cannot run here.

**Key numbers** (`data/HTMDEC-bbo-convergence.csv`, `figures/HTMDEC-bbo-convergence.png`):
- Hypervolume over 5 BO iterations (20 then 40-120 alloys evaluated): 231.70 -> 238.66 -> 244.70 -> 245.31 -> 250.31 -> **251.99**. The full-space Pareto HV is **276.42**.
- A random-batch baseline (30 seeds, same initial 20 alloys) reaches **256.6 +/- 8.5** after 120 alloys. In this single-seed demo the BO loop does **not** beat random selection; its value sits within 1 SD below the random mean.
- From the partition notebook: 7 elements on a 5 at.% grid give T(n=7, d=20) = **230,223** compositions.

**Problems found** (exact errors):
- The shipped BO driver hard-codes `iteration_current = 2` but defines `opt_folder`/`data_input` only for iteration 1: `NameError: name 'data_input' is not defined` at line 55 (`print(f'Starting hypervolume: ...')`). Even with `iteration_current = 1`, every later iteration fails the same way at `dimensions_input_number = data_input[dimensions_input_names]...`, because the iteration file is loaded only further down.
- `graph_result.py` uses nested same-quote f-strings, which need Python >= 3.12: `SyntaxError: f-string: unmatched '['` (line 93). It reads a file that is not in the repo (`Test simulations/graph example 1/inputSpace_from1000_size20_iter6.xlsx`) and expects a `Pareto` column the BO loop never writes: `KeyError: 'Pareto'`.
- In `htmdec_code_01_generate_partition.py`, an exported scratch cell uses an undefined frame: `NameError: name 'df' is not defined` (line 721). `export_dataframe_to_csv` passes `line_terminator=`, which was removed in pandas 2.x; that path is dormant only because `save_data = False`.
- `change_directory_to_current_py_file()` does `os.chdir` to the script folder, so outputs land inside the source tree.

**Relevance to us.** Low to medium. It is a compact, readable Python batch-EHVI + k-medoids loop over a discrete composition pool, useful for teaching. It has no constraints, priors, fidelities or cost terms, and the demo does not beat random. For anything operational, BRAVE (its Campaign 2 successor) and constraint-satisfaction are the better references.

---

## NiTi-alloy-discovery

**What it is.** Campaign folders (`Iter2/`, `Iter3/`) from batch BO for NiTi-based shape-memory alloys over Ni-Ti-Cu-Hf-Zr-Pd-Co. There are three objectives (minimize hysteresis, maximize transformation enthalpy, maximize transformation strain) and an Ms > 200 C target. The engine is the same as BRAVE/HTMDEC: george GPs with prior means read from CSV, EHVI, a constraint probability from a GP classifier, and k-medoids over the argmax picks of 1000 length-scale samples. Each folder holds the real per-iteration inputs and outputs (`tested_alloys.csv`, `o{1..3}_GT_y.csv`, `lhp.csv`, priors, `x_query.csv` with the 29 alloys proposed). There is no README beyond one sentence, no requirements file, and no license.

**What is really in the 479 MB clone** (the GitHub API reports size 0). About 366 MB is **three byte-identical copies of one git-LFS file**, `all_space.csv` (122 MB, 3,812,408 candidate compositions), at `Iter2/`, `Iter2/Probability_calculations/itr2/` and `Iter3/Probability_calculations/itr3/`. The LFS objects were fetched as real data, not pointers, and `.git/lfs` holds another 117 MB. Everything else is about 7 MB: Python scripts, CSVs, MATLAB `data.mat`/`.fig`/`postprocessing_analysis.m`, a `Summary.pptx`, PNG plots, and committed `__pycache__/*.cpython-310.pyc`, which shows the authors used Python 3.10. I copied the repo to the work directory without the `all_space.csv` copies, since only the feasibility classifier uses them.

**Install.** No dependency file. From the imports I used Python 3.11 with the BRAVE pins: numpy 1.26.4, pandas 2.2.3, scipy 1.17.1, scikit-learn 1.6.1, scikit-learn-extra 0.3.0, george 0.4.1, pyDOE 0.3.8, joblib. It installed in 1 s from cache with no problems.
```
uv venv --python 3.11 /tmp/arroyave/venvs/NiTi-alloy-discovery
uv pip install --python /tmp/arroyave/venvs/NiTi-alloy-discovery/bin/python numpy==1.26.4 pandas==2.2.3 scipy==1.17.1 scikit-learn==1.6.1 scikit-learn-extra==0.3.0 george==0.4.1 pyDOE==0.3.8 joblib matplotlib
```

**Runs** (driver: `scripts/NiTi-alloy-discovery-patch_and_run.sh`). Patches, applied in the work copy only: `N_GP` 1000 -> 3/20 (Iter3) or 10 (Iter2), `Batch_size` 29 -> 3/5, joblib `n_jobs` cpu_count -> 2, and EHVI evaluated on every 20th candidate, with the prior arrays subsampled consistently.
- `Iter3/main.py`, N_GP=3, batch 3, 675 of 13,517 candidates: **PASS**, 16 s. Two of the three proposals were identical, because k-medoids over only 3 argmax picks can repeat a pick.
- `Iter3/main.py`, N_GP=20, batch 5, 675 candidates: **PASS**, 104 s. 5 distinct proposals.
- `Iter2/main.py`, N_GP=10, batch 5, 333 of 6,658 candidates: **PASS**, 16 s.
- `Probability_calculations/itr*/main.py` (GP classifier over the 3.8M-point space): **not run**. It hard-codes the space size (`for i in range(381)`, `reshape(3812408,1)`), and at the rate in BRAVE's docstring (10k points about 5 min) the full space would take about 30 CPU-hours.
- MATLAB post-processing (`postprocessing_analysis.m`, `data.mat`, `.fig`): **NOT RUNNABLE**, since MATLAB is not available.

**Outcome: PASS** for the Python BO step of both iterations, using the shipped campaign data and scaled down. The classifier was too heavy to run, and the MATLAB parts are not runnable here.

**Key numbers** (`data/NiTi-alloy-discovery-iter3-smoke-xquery.csv`):
- Iter3 smoke-test proposals land close to the 29 alloys the campaign actually proposed: the L1 distance to the nearest shipped pick is 0.02 at. frac. for 4 picks and **0.00 for 1 (an exact match)**. One example pick: Ni0.50 Ti0.30 Hf0.10 Zr0.10.
- Max EHVI per hyperparameter sample: median 4,821 (range 2,973-9,384, n=20), against median 6,184 (3,239-11,879, n=1000) in the shipped `all_improvements.csv`. These are the same order of magnitude; our candidate set was subsampled 20x.

**Problems found.**
- No README beyond one sentence, no dependency list, no license, and committed `__pycache__`.
- One 122 MB LFS file is committed three times.
- The classifier script hard-codes the space size: `pd.DataFrame(np.array(p).reshape(3812408,1))`.
- `main.py` uses `n_jobs=multiprocessing.cpu_count()`, and N_GP=1000 over the full feasible set is HPC-scale. The scripts must be run from inside each `IterN/` folder, which has flat imports and relative CSV paths.

**Relevance to us.** Medium. It is a fully worked example, with real data, of a prior-mean + EHVI + k-medoids batch loop over a 7-element composition space. Its folder-per-iteration layout is a useful template for how to archive campaign state. It has no process parameters, multi-fidelity or cost terms, and it is a script rather than a library.

---

## Alloy-Color-Optimization

**What it is.** The figure-reproduction code for "Jeweler-in-the-Loop: Personalized Alloy Color Optimization via Preference-Based BO". It runs a BoTorch `PairwiseGP` preferential-BO over 933 quinary (E1–E5, element names obfuscated) jewelry alloys whose colors came from Thermo-Calc's Optical Properties model. A two-objective EHVI variant trades color preference against alloy price ($/g). A third script regenerates colors through TC-Python.

**Declared dependencies.** From the README: numpy, pandas, matplotlib, torch, botorch, gpytorch, linear_operator and pillow (no pins, "Python 3.9+"). `color_dataset_generation.py` also needs `tc_python` and a Thermo-Calc licence with the TCNOBL3 database.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__Alloy-Color-Optimization /tmp/arroyave/work/Alloy-Color-Optimization
/tmp/sbx/clean bash -c "uv venv --python 3.12 /tmp/arroyave/venvs/Alloy-Color-Optimization && uv pip install --python /tmp/arroyave/venvs/Alloy-Color-Optimization/bin/python --torch-backend cpu numpy pandas matplotlib torch botorch gpytorch linear_operator pillow"
cd /tmp/arroyave/work/Alloy-Color-Optimization   # all three runs below are wrapped in /tmp/sbx/clean timeout 400 bash -c "..."
CUDA_VISIBLE_DEVICES= python pref_gold_optimization.py --csv color_quinary_5%.csv --color-plot images/color_progress.png --tournament-plot images/tournament_progress.png --rgb-space-plot images/rgb_projections.png
CUDA_VISIBLE_DEVICES= python multiobjective_ehvi.py --csv color_quinary_5%.csv --plot out/multiobj_objectives.png
python color_dataset_generation.py --in color_quinary_5%.csv --out /tmp/x.csv          # needs Thermo-Calc
python -I /tmp/arroyave/results/bo/scripts/Alloy-Color-Optimization-rank.py /tmp/arroyave/work/Alloy-Color-Optimization data/Alloy-Color-Optimization-summary.json
```
Resolved versions: torch 2.15.0+cpu, botorch 0.18.1, gpytorch 1.15.2, linear-operator 0.6.1, numpy 2.5.4 and pandas 3.1.1, all on Python 3.12. No scale-down was needed: the defaults are already small (pref-BO uses 3 initial points and 10 iterations with seed 42; EHVI uses 5 initial points and 15 iterations with seed 0).

**Outcome: PASS** for both BO scripts, which ran unmodified on the latest stack. **NOT RUNNABLE** for `color_dataset_generation.py`, which needs a Thermo-Calc licence: `ModuleNotFoundError: No module named 'tc_python'`.

**Timings.** Install took about 1 s from cache. Preference BO ran in **30 s** and the EHVI run in **68 s**.

**Key numbers** (`data/Alloy-Color-Optimization-summary.json`; figures `figures/Alloy-Color-Optimization-color_progress.png` and `-multiobj_objectives.png`)
- **Preference BO** reached gold-likeness **0.9968** at iteration 7, 10 evaluations in total. That is the **global maximum** of the 933-alloy dataset (rank 1/933; the runner-up is 0.9940). The best value after the 3 random initial points was 0.8503.
- **EHVI (color vs price)** raised hypervolume from 0.5023 at iteration 1 to **0.5948** at iteration 15. Every one of the 15 BO picks costs **$36.9–50.3/g**, against a dataset price range of $3.9–50.3/g with a median of $15.4/g. The first pick was the single most expensive alloy in the set. See problem 2.

**Problems found**
1. **Printed Pareto front has the wrong sign** (multiobjective_ehvi.py:323): `pareto_mask = is_non_dominated(train_obj)`. BoTorch's `is_non_dominated` assumes maximization, but `train_obj` holds the *minimized* quantities (color distance, price), so the console prints the anti-Pareto set. The run's list includes `(0.0202, $48.81/g)` and `(0.0528, $47.36/g)`, both dominated by the queried point `(0.0102, $42.50/g)`. The plot function gets it right with `is_non_dominated(-pareto_tensor)` (line 141), so only the text output is wrong. Fix: `is_non_dominated(-train_obj)`.
2. **Likely sign and scale mismatch in the EHVI acquisition**, found by reading the code and consistent with the run. `price_gp = SingleTaskGP(compositions, price_norm_all)` models **+price**, while the hypervolume partitioning uses `train_y = -train_obj`, that is **−price**, and BoTorch EHVI maximizes every model output. A higher predicted price therefore counts as *more* improvement, which matches the BO picking only the most expensive alloys. The color output is a `PairwiseGP` latent utility on an arbitrary scale, whereas the partitioning uses min–max-scaled color distance in [−1, 0]. **Empirical check:** a two-line patch (`scripts/Alloy-Color-Optimization-signfix.sh`) makes the price GP model −price and fixes the printed front. With the same seed and budget, the BO picks now span **$3.9–38.4/g**, including the cheapest alloy in the dataset at iteration 14. Final HV is **0.8158, against 0.5948** unpatched, under the script's own running scaling, so the comparison is approximate. The printed front is now a valid minimization front. Logs: `logs/Alloy-Color-Optimization-ehvi-signfix.log`; figure: `figures/Alloy-Color-Optimization-multiobj_objectives_signfix.png`. The color-scale mismatch remains. A full fix would also put both objectives on matching scales, or build the front from the latent utility.
3. Very frequent `NumericalWarning: A not p.d., added jitter of 1.0e-02 to the diagonal` from the PairwiseGP Laplace fits (15 in the pref run alone, trimmed from the logs), plus `FutureWarning: torch.jit.script is deprecated` and a BoTorch `UserWarning` about `torch.tensor(ref_point)` copy construction.
4. Running the pref script with the README paths overwrites the committed `images/*.png`. I ran it on a copy.

**Relevance to us.** Medium. Preferential BO (`PairwiseGP`) is a good pattern for human-in-the-loop judgments such as "this melt-pool cross-section or surface looks better". A cost-aware EHVI over a discrete composition set is close to our supply-risk or cost objective. Reuse the structure, not the code as is, because of the sign bug in problem 2.

---

## Initialization

**What it is.** The data and a walkthrough script behind a study of how to choose the *first batch* of a batch-BO campaign. It compares random sampling with k-medoids on composition, k-medoids on composition plus an extra materials descriptor, and "perfect" medoids taken in the normally unknown output space. It ships 4 CSV datasets: an HTMDEC Al-V-Cr-Fe-Co-Ni downselection of 2,000 rows, the HTMDEC single-system set of 49,287 rows, a Ti-V-Nb-Mo-Hf-Ta-W refractory set of 1,000 rows, and refractory experimental data of 120 rows. The BO code itself lives in another repo (trevorhastings/HTMDEC). Zenodo DOI: https://doi.org/10.5281/zenodo.17635455.

**Declared dependencies.** No requirements file. From the imports: pandas (2.2 or later, because of `option_context("future.no_silent_downcasting")`), numpy, scipy, scikit-learn, scikit-learn-extra (`KMedoids`), seaborn and matplotlib.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__Initialization /tmp/arroyave/work/Initialization
/tmp/sbx/clean bash -c "uv venv --python 3.11 /tmp/arroyave/venvs/Initialization && uv pip install --python /tmp/arroyave/venvs/Initialization/bin/python scikit-learn-extra 'numpy<2' 'pandas>=2.2' 'scikit-learn<1.6' scipy seaborn matplotlib"
# As shipped (expected to refuse):
/tmp/sbx/clean timeout 120 bash -c "cd /tmp/arroyave/work/Initialization/Datasets && /tmp/arroyave/venvs/Initialization/bin/python ../script_for_datasets_and_features.py"
# Driver (scripts/Initialization-driver.py): loads only the script's imports and function defs through ast, then runs the described workflow
/tmp/sbx/clean timeout 420 /tmp/arroyave/venvs/Initialization/bin/python -I /tmp/arroyave/results/bo/scripts/Initialization-driver.py /tmp/arroyave/work/Initialization /tmp/arroyave/results/bo 1000 60
```
I chose Python 3.11 and numpy<2 to stay inside the wheel range of scikit-learn-extra 0.3.0. The extension is compiled against the numpy 1.x ABI, and the package is unmaintained. Resolved versions: scikit-learn-extra 0.3.0, scikit-learn 1.5.2, numpy 1.26.4, pandas 3.0.6 (which worked), scipy 1.17.1 and seaborn 0.13.2.

**Outcome: PARTIAL, by design of the repo.** The shipped script is a read-only walkthrough. Its first statement is `raise ValueError('This code is not meant to be run from this file!')`. Its functions run correctly through the driver, and the paper's central experiment was reproduced at reduced scale. Scale-down: 1,000 random batches as in the script, but **60 instead of 1,000** k-medoid batches per medoid strategy. Batch size stays at 20, the dataset is HTMDEC single system with `System_Type == 4` (3,842 alloys, 50 Pareto points), and the outputs are density and solidification range, all as in the script. For the "additional dimension" I used the commented-out alternative, `elements + ['Sconf_class']`, because `System_Type` is constant inside a single-system subset.

**Timings.** Install took about 1 s from cache. The driver ran in **52 s** in total: 12 s for 60 MED-EL batches, 11 s for 60 MED-EL+S batches and 25 s for 60 PERFECT batches, at about 0.2–0.4 s per k-medoids fit on 3,842 points.

**Key numbers** (`data/Initialization-summary.csv`; figure `figures/Initialization-batch-spread-cdf.png`)

| strategy | n batches | median bounding-box area (g/cm³·K) | median mean-distance to centroid | fraction of batches containing a Pareto point |
|---|---|---|---|---|
| RAND | 1000 | 646 | 48.3 | 0.23 |
| MED-EL (elements only) | 60 | 833 | 51.3 | 0.08 |
| MED-EL+S (elements + Sconf class) | 60 | **903** | **54.1** | 0.03 |
| PERFECT (output-space medoids) | 60 | 1565 | 93.8 | 0.00 |

This reproduces the qualitative claim: adding a materials descriptor to the medoid space spreads the first batch further in output space than composition-only medoids, and both beat random sampling on median spread with far lower variance. Random sampling has a wider tail, though, and is more likely to land a Pareto point by luck.

**Problems found**
1. The script is deliberately not runnable: `ValueError: This code is not meant to be run from this file!` (line 4). Log: `logs/Initialization-script-as-is.log`.
2. Even with the guard removed, top-down execution would fail. Found by reading the code; I did not execute it, because it would first run 2,000 or more k-medoid fits. `get_medoids` is *called* at line ~251, but `calculate_medoids_with_clusters_normalized` is *defined* only at line ~259, which gives a `NameError`. `randoms_features = []` is then indexed as `randoms_features['BoundingBoxArea']`, which gives a `TypeError`. The functions also rely on globals (`elements` in `calculate_medoids_with_clusters`, `batch_size` in `calculate_medoids_with_clusters_normalized`).
3. The script uses the old repo URL (`trevorhastings/Initialization`) and `pandas.read_csv(f"{file_name}.csv")` relative to the CWD, so it must be run from `Datasets/`.
4. It depends on `scikit-learn-extra`, which is unmaintained (0.3.0, 2023), has no Python 3.12 or numpy 2 wheels, and limits the whole environment to Python 3.11 or lower with numpy<2.

**Relevance to us.** Directly useful and cheap. For a first LPBF/Al-alloy batch we can run k-medoids over composition plus a cheap physics descriptor (for example a CALPHAD freezing range or an Eagar-Tsai melt-pool depth over the process parameters) to seed batch BO. The ~40 lines of medoid logic are easy to port to `sklearn`-only code (for example `kmedoids` or our own PAM) to drop the scikit-learn-extra pin.

---

## CatBoost-SMAs

**What it is.** A single script (`main.py`) plus a 4,912-row dataset (`raw_data.csv`) that trains a CatBoost multi-output regressor (MultiRMSE loss) for the four martensitic transformation temperatures (Ms, Mf, As, Af) of shape-memory alloys. Features are CBFV/JARVIS composition descriptors plus processing variables and alloy-family categorical flags. Paper: "An interpretable boosting-based predictive model for transformation temperatures of shape memory alloys", Comput. Mater. Sci. 226 (2023) 112225, https://doi.org/10.1016/j.commatsci.2023.112225. There is no BO in it; it is a surrogate model.

**Declared dependencies.** The README lists catboost (tested with 1.0.6), numpy, pandas, CBFV and scikit-learn, with no pins and no requirements file.

**Commands**
```bash
cp -r /tmp/arroyave/src/ArroyaveLab__CatBoost-SMAs /tmp/arroyave/work/CatBoost-SMAs
# Attempt 1: Python 3.12 with the latest packages (kept as venvs/CatBoost-SMAs-py312-latest)
/tmp/sbx/clean bash -c "uv venv --python 3.12 /tmp/arroyave/venvs/CatBoost-SMAs && uv pip install --python /tmp/arroyave/venvs/CatBoost-SMAs/bin/python catboost numpy pandas CBFV scikit-learn"
/tmp/sbx/clean bash -c "uv pip install --python ... 'setuptools<81'"      # fixes error 1 below, then hits error 2
# Attempt 2 (works): Python 3.10, pinned to the paper-era stack
/tmp/sbx/clean bash -c "uv venv --python 3.10 /tmp/arroyave/venvs/CatBoost-SMAs && uv pip install --python /tmp/arroyave/venvs/CatBoost-SMAs/bin/python catboost==1.0.6 'numpy<1.24' 'pandas<2' CBFV 'scikit-learn<1.3' 'setuptools<81'"
/tmp/sbx/clean timeout 600 taskset -c 0,1 bash -c "cd /tmp/arroyave/work/CatBoost-SMAs && /tmp/arroyave/venvs/CatBoost-SMAs/bin/python main.py"
```
Resolved versions for attempt 2: catboost 1.0.6, CBFV 1.1.0, pandas 1.5.3, numpy 1.23.5, scikit-learn 1.2.2, setuptools 80.10.2. Nothing was scaled down. The script was run unmodified with the default 1,000 boosting iterations.

**Outcome: PASS** with Python 3.10 and pinned packages. It FAILS on a current stack (Python 3.12, pandas 3.1, setuptools 81 or later).

**Timings.** Install took about 5 s from the uv cache. Training and evaluation took **411 s** wall-clock on 2 pinned CPUs of the shared box. CatBoost ignores `OMP_NUM_THREADS` and spawns threads for every core it sees, hence the `taskset`.

**Key numbers** (`data/CatBoost-SMAs-metrics.json`). 1,689 rows survive cleaning. They are split 80/20 with `random_state=42`, and the four outputs are pooled:
- Train: RMSE 19.66 K, MAE 13.95 K, R² 0.966
- **Test: RMSE 24.69 K, MAE 17.03 K, R² 0.936**

**Problems found**
1. CBFV imports `pkg_resources`, which is gone from new setuptools: `ModuleNotFoundError: No module named 'pkg_resources'` (from `CBFV/composition.py`, line 7). Fix: `setuptools<81`. Log: `logs/CatBoost-SMAs-run1-py312-latest.log`.
2. With pandas 2 or later, CBFV's `generate_features(..., extend_features=True)` takes the median of the string categorical columns that `main.py` passes through (`family`, `niti_bas`, ...): `TypeError: Cannot perform reduction 'median' with string dtype` (CBFV/composition.py:325, `median_values = X[cols].median()`). Fix: `pandas<2`, which needs Python 3.11 or lower; I used 3.10 to match catboost 1.0.6 wheels. Log: `logs/CatBoost-SMAs-run2-py312-latest.log`.
3. Cosmetic: `SyntaxWarning: invalid escape sequence '\d'` at main.py:68, because `'\d+'` should be a raw string. pandas 1.5 also prints `FutureWarning: iteritems is deprecated` from catboost 1.0.6.
4. The script only prints metrics. No model, prediction or plot is saved, and there is no hyperparameter search, although the parameters were evidently tuned. There is no CLI and no seed for CatBoost itself.

**Relevance to us.** Low to medium. It is a composition plus processing tabular surrogate, not BO. The pattern (CBFV descriptors plus categorical family flags into a gradient-boosted multi-output model) could serve as a cheap prior-mean or feasibility model inside a BOFN node, but it gives no uncertainty for acquisition functions without extra work (for example CatBoost `RMSEWithUncertainty` or ensembles).

---

## Summary table

| repo | install | test/demo run | outcome | notes |
|---|---|---|---|---|
| tamubo | OK (CPU torch; drop personal-fork `-e git+` line; mobbo needs pyDOE==0.3.8 + george) | exactbo 2D (scaled to 10 partitions), 3 BoTorch/sklearn EI engines, mobbo EHVI | PARTIAL (shipped exactbo config >600 s on CPU; rest PASS) | exactbo best -1.8973 vs -1.8798..-1.8912 for BoTorch, but ~150-500x slower |
| BAREFOOT-Framework | OK on Python 3.10 with numpy==1.23.5, scipy==1.11.4, pyDOE==0.3.8 + 1-line scipy.random patch | batch-only 2D demo (5 iters x 10 truth); reification+batch single node (12 iters, 32 truth evals) | PASS (single node; SLURM demo NOT RUNNABLE) | batch-only 4.278 vs fusion 4.500 (max 5.719), 1 seed; errors logged but exit 0; Ray ~40x slower under CPU contention |
| PCMOBO | OK (CPU torch; pulls langchain/langgraph; generic top-level module names) | 3 README smokes + HEA 10+15 for PoF, pEHVI, bandit switch | PASS (llm_switch not run, needs OpenAI key) | HEA feasible found in 15 iters (seeds 1/2): PoF 12/14, bandit 8/8, pEHVI 0/0 |
| SupplyRiskAwareDesign | FAIL as shipped (`src` missing); OK after rebuilding `src/sradd` layout | MoNbTiVW grid, batch MOBBO with/without SR (10 + 4x5) | PARTIAL (packaging bug; science code PASS) | HV 0.814 (with SR) / 0.978 (without); Pareto mean SR 50.7 vs 52.9; 3-obj EHVI ~10x slower |
| 2026-islam-rhea-mobo | OK (CPU torch; avoid `uv sync`, lock pulls CUDA) | pytest 24/24; toy BO 8+3 and 8+15 x2 seeds; correlation script | PASS (production loop needs TC-Python licence) | supply-risk-weighted EHVI; BO 0.883 vs random 0.765 (seed 42), 0.886 vs 0.921 (seed 7) |
| DGP-BO | OK (py3.12, pinned torch 2.2.2+cpu / gpytorch 1.11; +george) | capsule entry (DGP-het, 2 iters, 36 s) after stripping .cuda(); cGP & MTGP 10 iters (~50 s each), DGP-iso 5 iters (185 s) | PASS (CPU patch) | seeded, same start (HV 7593), 5 iters: DGP-iso 9138 vs cGP 7760 vs MTGP 7600; DGP-het capsule run 7825→8372; CUDA-only as shipped; breaks on gpytorch≥1.12 (gpytorch.lazy) |
| Kernels-BO | OK (py3.12, latest torch-cpu/gpytorch/botorch) | input-space pipeline on 40/237 kernels (151 s) + application notebook 2 trials × 10 queries (80 s); main LLM-GA notebook not run (OpenAI API) | PARTIAL | recomputed kernel distances match shipped embedding (Pearson 0.9999); composite kernel beat RBF on both 1-D benchmarks; only 71/237 grammar kernels are distinct; printability data not shipped |
| constraint-satisfaction | PASS (py3.11, unpinned sklearn stack, 3 s) | 5 of 6 campaign scripts PASS (2 seeds x 20 iters, 23-35 s each) + plot_metrics.py; ehvi_pofcorr timed out (2-3 iters in 300 s) | PASS | with-prior finds 13/24 truly feasible alloys in 20 iters vs 0 for random/pEHVI; logged HV ignores feasibility |
| BRAVE | PASS after adding setuptools<81 (py3.11, pinned reqs) | make figures PASS; BBO main.py PASS on stand-in inputs with N_GP=2 after 3 fixes; feasibility-GPC FAIL | PARTIAL | priors.py wrong column names + index bug; table.dat missing; hard-coded 1,490,129-point space; per-iteration inputs not public |
| HTMDEC | PASS (no deps file; py3.11 inferred) | bbo_python 5 BO iterations PASS after 3 patches; notebook PASS; graph script + .py export FAIL; MATLAB not runnable | PARTIAL | shipped driver NameError for any iteration>1; demo BO HV 252 vs random 257+/-9 (full space 276) |
| NiTi-alloy-discovery | PASS (no deps file; py3.11 + BRAVE pins) | Iter2 + Iter3 main.py BO step PASS (N_GP 10-20, every 20th candidate); classifier not run (3.8M pts); MATLAB parts not runnable | PASS | 479 MB = 3 identical copies of a 122 MB LFS all_space.csv; Iter3 rerun reproduces shipped picks within 0.02 at.frac. |
| Alloy-Color-Optimization | OK (py3.12, latest botorch 0.18.1, CPU torch) | pref-BO 30 s + EHVI 68 s, defaults; TC-Python data script needs licence | PASS (BO) / NOT RUNNABLE (TC script) | pref-BO finds global best (0.9968, rank 1/933) in 10 evals; EHVI price objective sign-flipped (models +price vs −price front; 2-line fix raises final HV 0.595→0.816) and printed Pareto is anti-Pareto |
| Initialization | OK (py3.11, numpy<2 for scikit-learn-extra) | walkthrough raises by design; driver reproduces 1000 random + 60x3 k-medoid batches, 52 s | PARTIAL | composition+Sconf medoids spread first batch more than composition-only/random (median bbox 903 vs 833 vs 646); script has NameError ordering bug |
| CatBoost-SMAs | OK (py3.10; catboost 1.0.6, pandas<2, setuptools<81) | main.py unmodified, 411 s | PASS | test R² 0.936, RMSE 24.7 K over Ms/Mf/As/Af; fails on pandas≥2 / setuptools≥81 (CBFV) |

## Files produced

All paths are relative to this folder. Per-repo section sources are in `sections/`; driver scripts in `scripts/` reproduce each run (`scripts/vizstyle.py` is the shared plot style; `scripts/assemble_report.py` builds this file).

- **figures/** (21 files): `2026-islam-rhea-mobo-feature-importance.png`, `2026-islam-rhea-mobo-objective-correlation.png`, `2026-islam-rhea-mobo-toy-hv.png`, `Alloy-Color-Optimization-color_progress.png`, `Alloy-Color-Optimization-multiobj_objectives.png`, `Alloy-Color-Optimization-multiobj_objectives_signfix.png`, `BAREFOOT-Framework-batch-vs-fusion.png`, `BRAVE-fig_14_boxplot-regenerated.png`, `BRAVE-fig_19_v_ys_feasibility-regenerated.png`, `DGP-BO-hv-trace-seed0.png`, `DGP-BO-hv-trace.png`, `HTMDEC-bbo-convergence.png`, `Initialization-batch-spread-cdf.png`, `Kernels-BO-application-ackley1d-trace.png`, `Kernels-BO-application-dropwave1d-trace.png`, `Kernels-BO-input-space.png`, `PCMOBO-hea-feasible.png`, `SupplyRiskAwareDesign-mobbo.png`, `constraint-satisfaction-hv.png`, `constraint-satisfaction-repo_plot_metrics-TrueMeasPass_All_With_BCC.png`, `tamubo-convergence.png`
- **data/** (34 files): `2026-islam-rhea-mobo-toy-default-summary.json`, `2026-islam-rhea-mobo-toy-it15-s42-comparison.csv`, `2026-islam-rhea-mobo-toy-it15-s42-summary.json`, `2026-islam-rhea-mobo-toy-it15-s7-comparison.csv`, `2026-islam-rhea-mobo-toy-it15-s7-summary.json`, `Alloy-Color-Optimization-summary.json`, `BAREFOOT-Framework-batch-it4-hp100-iterationData.csv`, `BAREFOOT-Framework-full-it4-hp100-iterationData.csv`, `BAREFOOT-Framework-full-med-iterationData.csv`, `BAREFOOT-Framework-full-small2-iterationData.csv`, `BRAVE-smoke-results.json`, `CatBoost-SMAs-metrics.json`, `DGP-BO-hv-traces-seed0.json`, `DGP-BO-hv-traces.json`, `HTMDEC-bbo-convergence.csv`, `Initialization-batch-features.csv`, `Initialization-run.json`, `Initialization-summary.csv`, `Kernels-BO-application-ackley1d-traces.json`, `Kernels-BO-application-dropwave1d-traces.json`, `Kernels-BO-input-space.json`, `NiTi-alloy-discovery-iter3-smoke-xquery.csv`, `PCMOBO-hea-campaigns.csv`, `SupplyRiskAwareDesign-s0-history_with_SR.csv`, `SupplyRiskAwareDesign-s0-history_without_SR.csv`, `SupplyRiskAwareDesign-s0-summary.json`, `constraint-satisfaction-summary.csv`, `tamubo-convergence.csv`, `tamubo-cpu_botorch_grid_ei.json`, `tamubo-cpu_botorch_optimize_ei.json`, `tamubo-cpu_exactbo_it2_p10.json`, `tamubo-cpu_exactbo_it6_p10.json`, `tamubo-cpu_sklearn_grid_ei.json`, `tamubo-mobbo-hv_curr.csv`
- **scripts/** (37 files): `2026-islam-rhea-mobo-plot.py`, `2026-islam-rhea-mobo-run.sh`, `Alloy-Color-Optimization-rank.py`, `Alloy-Color-Optimization-signfix.sh`, `BAREFOOT-Framework-driver.py`, `BAREFOOT-Framework-plot.py`, `BRAVE-main.patch`, `BRAVE-make_inputs.py`, `BRAVE-priors.patch`, `BRAVE-smoke.sh`, `BRAVE-smoke2.sh`, `BRAVE-smoke3.sh`, `DGP-BO-patch.sh`, `DGP-BO-summarize-seeded.py`, `DGP-BO-summarize.py`, `HTMDEC-convergence.py`, `HTMDEC-graph_result.patch`, `HTMDEC-package_BBO_single_iteration.patch`, `HTMDEC-run.sh`, `Initialization-driver.py`, `Kernels-BO-input-space-driver.py`, `Kernels-BO-scale-notebook.py`, `NiTi-alloy-discovery-Iter2-main.patch`, `NiTi-alloy-discovery-Iter3-main.patch`, `NiTi-alloy-discovery-patch_and_run.sh`, `PCMOBO-hea-compare.sh`, `PCMOBO-plot.py`, `PCMOBO-smoke.sh`, `SupplyRiskAwareDesign-campaign.py`, `SupplyRiskAwareDesign-plot.py`, `assemble_report.py`, `constraint-satisfaction-run.sh`, `constraint-satisfaction-summarize.py`, `tamubo-exactbo_nocp-nogit.txt`, `tamubo-plot.py`, `tamubo-run-bo-examples.sh`, `vizstyle.py`
- **logs/** (105 files): `2026-islam-rhea-mobo-cli.log`, `2026-islam-rhea-mobo-install-full.log`, `2026-islam-rhea-mobo-install-toy.log`, `2026-islam-rhea-mobo-predicted-correlation.log`, `2026-islam-rhea-mobo-pytest-full.log`, `2026-islam-rhea-mobo-pytest-toyenv.log`, `2026-islam-rhea-mobo-toy-default.log`, `2026-islam-rhea-mobo-toy-it15-s42.log`, `2026-islam-rhea-mobo-toy-it15-s7.log`, `Alloy-Color-Optimization-ehvi-signfix.log`, `Alloy-Color-Optimization-ehvi.log`, `Alloy-Color-Optimization-install.log`, `Alloy-Color-Optimization-pref.log`, `Alloy-Color-Optimization-tcpython.log`, `BAREFOOT-Framework-batch-it4-hp100-npfloat-fail.BAREFOOT.log`, `BAREFOOT-Framework-batch-it4-hp100.BAREFOOT.log`, `BAREFOOT-Framework-batch-it4-hp100.log`, `BAREFOOT-Framework-full-it4-hp100.BAREFOOT.log`, `BAREFOOT-Framework-full-it4-hp100.log`, `BAREFOOT-Framework-full-med.BAREFOOT.log`, `BAREFOOT-Framework-full-med.log`, `BAREFOOT-Framework-full-small-prev.BAREFOOT.log`, `BAREFOOT-Framework-full-small.BAREFOOT.log`, `BAREFOOT-Framework-full-small.log`, `BAREFOOT-Framework-full-small2.BAREFOOT.log`, `BAREFOOT-Framework-full-small2.log`, `BAREFOOT-Framework-install.log`, `BRAVE-install.log`, `BRAVE-main-NGP2.log`, `BRAVE-make_figures.log`, `BRAVE-smoke.log`, `BRAVE-smoke2.log`, `BRAVE-smoke3.log`, `CatBoost-SMAs-install-pinned.log`, `CatBoost-SMAs-install.log`, `CatBoost-SMAs-run1-py312-latest.log`, `CatBoost-SMAs-run2-py312-latest.log`, `CatBoost-SMAs-run3-pinned.log`, `DGP-BO-cgp-nbo10.log`, `DGP-BO-codeocean-run-cuda.log`, `DGP-BO-dgp-het-cpu.log`, `DGP-BO-dgp-iso-nbo5.log`, `DGP-BO-dgp-iso-tec-MO-11-seed0-nbo5.log`, `DGP-BO-gp-tec-MO-11-seed0-nbo5.log`, `DGP-BO-gpytorch-latest-import.log`, `DGP-BO-install.log`, `DGP-BO-mtgp-nbo10.log`, `DGP-BO-mtgp-tec-MO-11-seed0-nbo5.log`, `HTMDEC-bbo-run.log`, `HTMDEC-bbo-run2.log`, `HTMDEC-bbo-run3.log`, `HTMDEC-graph_result-patched.log`, `HTMDEC-graph_result-shipped.log`, `HTMDEC-install.log`, `HTMDEC-notebook.log`, `HTMDEC-partition_py.log`, `Initialization-driver-smoke.log`, `Initialization-driver.log`, `Initialization-install.log`, `Initialization-script-as-is.log`, `Kernels-BO-application-cell-outputs.log`, `Kernels-BO-application-nbconvert.log`, `Kernels-BO-application-nbconvert2.log`, `Kernels-BO-input-space-smoke.log`, `Kernels-BO-input-space.log`, `Kernels-BO-install.log`, `NiTi-alloy-discovery-install.log`, `NiTi-alloy-discovery-iter2-NGP10.log`, `NiTi-alloy-discovery-iter3-NGP20.log`, `NiTi-alloy-discovery-iter3-run.log`, `PCMOBO-hea-bandit_ucb_switch-seed2.log`, `PCMOBO-hea-bandit_ucb_switch.log`, `PCMOBO-hea-pehvi-seed2.log`, `PCMOBO-hea-pehvi.log`, `PCMOBO-hea-pof-seed2.log`, `PCMOBO-hea-pof.log`, `PCMOBO-help-synthetic.log`, `PCMOBO-install.log`, `PCMOBO-smoke-estm.log`, `PCMOBO-smoke-hea.log`, `PCMOBO-smoke-synthetic.log`, `SupplyRiskAwareDesign-campaign-s0.log`, `SupplyRiskAwareDesign-install-asis.log`, `SupplyRiskAwareDesign-install-srclayout.log`, `constraint-satisfaction-install.log`, `constraint-satisfaction-plot_metrics.log`, `constraint-satisfaction-run-all.log`, `constraint-satisfaction-run-campaign_const_NO_priors.log`, `constraint-satisfaction-run-campaign_const_w_priors.log`, `constraint-satisfaction-run-campaign_ehvi_pof.log`, `constraint-satisfaction-run-campaign_ehvi_pofcorr.log`, `constraint-satisfaction-run-campaign_pehvi.log`, `constraint-satisfaction-run-campaign_random.log`, `constraint-satisfaction-run-const_w_priors.log`, `constraint-satisfaction-summary.log`, `tamubo-bo-botorch_grid_ei.log`, `tamubo-bo-botorch_optimize_ei.log`, `tamubo-bo-sklearn_grid_ei.log`, `tamubo-exactbo-min2d-it2-p10.log`, `tamubo-exactbo-min2d-it6-p10.log`, `tamubo-exactbo-min2d.log`, `tamubo-install-george.log`, `tamubo-install-pydoe038.log`, `tamubo-install.log`, `tamubo-mobbo-main_BO.log`
