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

TABLE: DGP-BO | OK (py3.12, pinned torch 2.2.2+cpu / gpytorch 1.11; +george) | capsule entry (DGP-het, 2 iters, 36 s) after stripping .cuda(); cGP & MTGP 10 iters (~50 s each), DGP-iso 5 iters (185 s) | PASS (CPU patch) | seeded, same start (HV 7593), 5 iters: DGP-iso 9138 vs cGP 7760 vs MTGP 7600; DGP-het capsule run 7825→8372; CUDA-only as shipped; breaks on gpytorch≥1.12 (gpytorch.lazy)
