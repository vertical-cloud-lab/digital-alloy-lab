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

TABLE: CatBoost-SMAs | OK (py3.10; catboost 1.0.6, pandas<2, setuptools<81) | main.py unmodified, 411 s | PASS | test R² 0.936, RMSE 24.7 K over Ms/Mf/As/Af; fails on pandas≥2 / setuptools≥81 (CBFV)
