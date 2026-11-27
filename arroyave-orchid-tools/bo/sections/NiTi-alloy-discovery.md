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

TABLE: NiTi-alloy-discovery | PASS (no deps file; py3.11 + BRAVE pins) | Iter2 + Iter3 main.py BO step PASS (N_GP 10-20, every 20th candidate); classifier not run (3.8M pts); MATLAB parts not runnable | PASS | 479 MB = 3 identical copies of a 122 MB LFS all_space.csv; Iter3 rerun reproduces shipped picks within 0.02 at.frac.
