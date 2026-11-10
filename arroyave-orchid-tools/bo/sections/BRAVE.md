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

TABLE: BRAVE | PASS after adding setuptools<81 (py3.11, pinned reqs) | make figures PASS; BBO main.py PASS on stand-in inputs with N_GP=2 after 3 fixes; feasibility-GPC FAIL | PARTIAL | priors.py wrong column names + index bug; table.dat missing; hard-coded 1,490,129-point space; per-iteration inputs not public
