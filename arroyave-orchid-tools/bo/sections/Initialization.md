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

TABLE: Initialization | OK (py3.11, numpy<2 for scikit-learn-extra) | walkthrough raises by design; driver reproduces 1000 random + 60x3 k-medoid batches, 52 s | PARTIAL | composition+Sconf medoids spread first batch more than composition-only/random (median bbox 903 vs 833 vs 646); script has NameError ordering bug
