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

TABLE: BAREFOOT-Framework | OK on Python 3.10 with numpy==1.23.5, scipy==1.11.4, pyDOE==0.3.8 + 1-line scipy.random patch | batch-only 2D demo (5 iters x 10 truth); reification+batch single node (12 iters, 32 truth evals) | PASS (single node; SLURM demo NOT RUNNABLE) | batch-only 4.278 vs fusion 4.500 (max 5.719), 1 seed; errors logged but exit 0; Ray ~40x slower under CPU contention
