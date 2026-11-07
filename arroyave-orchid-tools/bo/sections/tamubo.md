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

TABLE: tamubo | OK (CPU torch; drop personal-fork `-e git+` line; mobbo needs pyDOE==0.3.8 + george) | exactbo 2D (scaled to 10 partitions), 3 BoTorch/sklearn EI engines, mobbo EHVI | PARTIAL (shipped exactbo config >600 s on CPU; rest PASS) | exactbo best -1.8973 vs -1.8798..-1.8912 for BoTorch, but ~150-500x slower
