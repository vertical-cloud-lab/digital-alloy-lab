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

TABLE: Kernels-BO | OK (py3.12, latest torch-cpu/gpytorch/botorch) | input-space pipeline on 40/237 kernels (151 s) + application notebook 2 trials × 10 queries (80 s); main LLM-GA notebook not run (OpenAI API) | PARTIAL | recomputed kernel distances match shipped embedding (Pearson 0.9999); composite kernel beat RBF on both 1-D benchmarks; only 71/237 grammar kernels are distinct; printability data not shipped
