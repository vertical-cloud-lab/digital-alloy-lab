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

