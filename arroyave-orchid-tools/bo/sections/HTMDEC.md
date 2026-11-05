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

TABLE: HTMDEC | PASS (no deps file; py3.11 inferred) | bbo_python 5 BO iterations PASS after 3 patches; notebook PASS; graph script + .py export FAIL; MATLAB not runnable | PARTIAL | shipped driver NameError for any iteration>1; demo BO HV 252 vs random 257+/-9 (full space 276)
