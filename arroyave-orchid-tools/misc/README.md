# The remaining ArroyaveLab repos: install and test runs (issue #235)

This covers CALPHAD, HEACalculator, akaitools, microseg_lab, CGA_Subgraph_Analysis, 2026-mulukutla-hall-petch,
Phase-Compatibility-Model-NiTi and Transformation-Strain-Model-NiTi.

Runs were made on 2026-11-05 (UTC) on a shared 4-vCPU / 15 GB runner with no GPU, no TC-Python and no Thermo-Calc
licence. Each repo got its own uv venv and a working copy. Every install and third-party script ran with secrets
stripped from the environment, limited to 1–2 threads. Torch was `2.15.0+cpu`.

In the commands below, `$V` is the venv folder, `$W` is the working-copy folder, `$S` is [`scripts/`](scripts/) and
`$R` is this folder.

## Summary

| Repo | Install | Test / example run | Outcome | Notes |
|---|---|---|---|---|
| CALPHAD | OK, no TC-Python | Plotter, composition generator, mock-TC equilibrium, pycalphad Al–Si port | PARTIAL | Needs a Thermo-Calc licence; example data file missing; Pd/Pb typo; breaks on pandas 4. Port to pycalphad: ~0.5 day (equilibrium), 1–2 days (Scheil) |
| HEACalculator | OK | 585 passed / 1 xfailed; 7 alloys; hand check | PASS | Exact match by hand; HEA rules misclassify dilute Al and Cu alloys |
| akaitools | OK | 447 passed; CLI and plots; Cu–Ni input | PASS | Niche for us |
| microseg_lab | OK (CPU torch; SAM2 built from source) | classical path ×3 images; SAM2-tiny ×1 | PASS (headless) | Needs SAM2 installed even for the classical path; ~40 s per 512² image, 92 s with SAM2 |
| CGA_Subgraph_Analysis | OK (Python 3.10) | notebook, unmodified | PASS | 72 s; Kou hot-cracking screening idea |
| 2026-mulukutla-hall-petch | OK (xgboost-cpu, no PyMC/PySR) | `make test`, `sdgrain`, `figures`, `verify`, `data` | PASS (main analysis) | Headline M15 result exact; `verify` fails on a fresh checkout; `data` breaks on matplotlib ≥ 3.10 and is slow |
| Phase-Compatibility-Model-NiTi | OK after pins | notebook + one patch cell; dataset check | PARTIAL | HEACalculator 1.x API no longer exists; δ drifts; accuracy 0.916 |
| Transformation-Strain-Model-NiTi | OK after pins | notebook | PASS (pinned) | 8 of 10 cells identical to the stored output; CV R² 0.954 |

**The findings that matter most to us:**
- **CALPHAD → pycalphad is worth doing.**
  - The repo's parallel plumbing carries over unchanged; only the TC-Python calls need swapping.
  - The Al–Si sketch here gives a 577 °C eutectic and a 597 °C liquidus at AlSi10Mg's Si level.
  - Estimate: about half a day for equilibrium and 1–2 days for Scheil.
  - The real limit is the database: there is no open equivalent of TCAL. Open databases also lack molar volumes, so a
    port reports phase mole fractions, not volume fractions.
- **microseg_lab is the most directly usable repo.** Its default target is dark voids, which in our case means LPBF
  porosity.
- **The CGA notebook's Kou hot-cracking filter** on a composition graph is a reusable idea for screening printable Al
  alloys.

## 1. CALPHAD: Thermo-Calc driver scripts with parallelisation (PARTIAL)

**What it is.** TC-Python drivers for equilibrium, property models and Scheil. Each splits a composition CSV across
worker processes, with one TC session per worker. There is no packaging, no requirements file and no tests.

**What needs TC-Python.**
- `Equilibrium/TC_Equilibrium*.py`, `Property/TC_Property*.py`, `Scheil/TC_Scheil.py` and `Setup/Diagnostics.py` all do.
- In `Setup/thermocalc_library.py`, only `collect_version_info()` does. The rest (checks, splitting, concatenation,
  logs) is plain pandas.
- `Setup/Compositions.py` (a barycentric grid generator) and `Scheil/Graph_Scheil_Curves.py` (a plotter) don't.

**Commands.**
- Venv with numpy, pandas, matplotlib, seaborn, openpyxl and pycalphad.
- `Graph_Scheil_Curves.py`: run as shipped, then again after joining `_part1.csv` and `_part2.csv` into
  `Graph_Scheil_Example.csv`.
- `$S/calphad_runs.sh $W/CALPHAD $V/CALPHAD/bin/python $S`: the composition generator, plus a run of
  `TC_Equilibrium.py` against a mock `tc_python` (`$S/mock_tc_python/`), which returns made-up numbers and exists only
  to exercise the plumbing.
- `$S/calphad_pycalphad_port.py $W/CALPHAD/Setup <orchid sgte-binary>/AlSi-97Feu-LB.tdb <out>`.

**Results.**
- **Plotter:** fails as shipped. After joining the two halves it plots all 40 example materials in 22 s
  ([figure](figures/CALPHAD_scheil_material_1.png)).
- **`Compositions.py`:**
  - As shipped (Ti–V–Co at resolution 200): 1.0 s, 20,301 compositions in 8 CSVs.
  - Edited to Al–Cu–Mg–Si at resolution 20: 1,771 compositions, 969 of them quaternary.
- **`TC_Equilibrium.py` against the mock** (2 divisions on 2 cores instead of 10 on 10): the whole `__main__` ran in
  0.6 s.
  - That covers input checks, the licence inquiry, two worker CSVs, CPU logs, the execution log, and concatenation to
    `All_data.csv` (171 rows).
  - The mock's numbers are deliberately not thermodynamics.
- **pycalphad port of `Equilibrium()`**, using the repo's own helpers and the Feufel et al. (1997) Al–Si description:
  3.2 s for 5 compositions.
  - Eutectic solidus 577 °C.
  - Liquidus 649 / 629 / 597 / 578 / 697 °C for Al–2/5/9.6/12.2/20 at.% Si.
  - At 600 °C, Al–9.6Si is fully liquid.
  - These match the accepted Al–Si diagram.

**Porting estimate.** The orchestration is reused as is.
- Equilibrium: about 0.5 day. Open databases lack molar volumes, so it reports phase mole fractions instead of
  volume fractions.
- Scheil: 1–2 days, using the `scheil` package plus a liquidus/solidus temperature scan.
- The property-model scripts have no direct pycalphad equivalent.
- The binding constraint is an open Al–Si–Mg–Cu–Fe database of TCAL's scope; see [`../pycalphad-al-cu/`](../pycalphad-al-cu/).

**Problems.**
- `FileNotFoundError: [Errno 2] No such file or directory: 'Graph_Scheil_Example.xlsx'`: the plotter's input isn't
  shipped, only its two halves.
- `Pandas4Warning: Setting a value on a DataFrame via .at with a key that does not exist in the index is deprecated
  and will raise a KeyError`: `TC_Equilibrium.py` will break on pandas 4.
- `thermocalc_library.py` must be copied by hand next to each script.
- In `Compositions.py`, `PERIODIC_ORDER` has `82:'Pd'` instead of `'Pb'`, so any Pb-containing system raises
  `ValueError` in the sort key. It also runs everything at import time, so it must be edited for each new system.
- `check_temperature_limit()` has no Al, Mg, Zn or Li in its melting-point table.
- In `collect_version_info`, the name `check_database` is shadowed by its own return value.
- `if "__name__" == "__main__":` compares two string literals, so that block is dead code.
- Inputs (file name, database, core count) are hard-coded in each `__main__`; there is no CLI.

**Relevance: high as a pattern.** The one-TC-session-per-worker layout and the Scheil plotter carry over to our
TCAL/TCCU work, and the generator works for Al–Cu–Mg–Si.

## 2. HEACalculator: HEA solid-solution parameters (PASS)

**What it is.** HEACalculator 2.2.0, with a CLI, a GUI and a Python API. It computes δ, Δχ, ΔH_mix, ΔS_mix, Ω, γ, Λ,
φ, VEC and T_m, plus eight published solid-solution criteria.

**Commands.**
- Install: `uv pip install -e $W/HEACalculator pytest`.
- Tests: `pytest -q --ignore=tests/gui`.
- Compositions and hand check: `$S/heacalc_driver.py $R/data`.
- CLI: `HEACalculator search single Cu70Ni30`.

**Results.** **585 passed, 1 xfailed** in 3.1 s; the GUI tests were skipped because PyQt6 isn't installed.

| Alloy | δ % | VEC | ΔH_mix kJ/mol | ΔS_mix J/K·mol | Ω | Predicted structure |
|---|---|---|---|---|---|---|
| CoCrFeMnNi | 3.27 | 8.00 | −4.16 | 13.38 | 5.80 | FCC |
| AlCoCrFeNi | 5.78 | 7.20 | −12.32 | 13.38 | 1.83 | BCC+FCC |
| Al89.65Si10Mg0.35 | 6.01 | 3.10 | −6.87 | 2.89 | 0.42 | BCC |
| Cu70Ni30 | 1.16 | 10.70 | +3.36 | 5.08 | 2.22 | FCC |
| Cu99.1Cr0.8Zr0.1 | 0.83 | 10.95 | +0.29 | 0.45 | 2.14 | FCC |

**Hand check, Cu70Ni30**, using the package's own element and pair tables:
- ΔS_mix = −R(0.7 ln 0.7 + 0.3 ln 0.3) = 5.0790 J/K·mol
- ΔH_mix = 4·(+4)·0.7·0.3 = 3.360 kJ/mol
- r̄ = 126.84 pm, so δ = 1.1561 %
- VEC = 10.70
- T_m = 1468.9 K. The package rounds this to 1469 K (documented), which moves Ω from 2.2204 to 2.2206.

Everything else matches exactly. For Al89.65Si10Mg0.35, ΔH_mix = −6.8749 kJ/mol and δ = 6.0147 %, also exact.

**Problems.** None in the code. The rules are used outside their domain, though: the VEC rule calls AlSi10Mg "BCC",
and model 2 calls Cu–Ni, a continuous FCC solid solution, "Intermetallic".

**Relevance: low to moderate.** It is a well-tested generator of descriptors for ML features, but its phase
predictions don't apply to dilute Al or Cu alloys.

## 3. akaitools: AkaiKKR output parser (PASS)

**What it is.** akaitools 0.3.1 parses and plots AkaiKKR KKR-CPA outputs (SCF, DOS, SPC/BSF) and builds input files.

**Commands.**
- Install: `pip install -e . pytest`, then `pytest -q`.
- CLI on the bundled outputs: `akaitools go tests/data/out/nife` (and `--json` on `fe`), `akaitools dos …/nife.dos`,
  and `akaitools plot dos|scf|bsf … -o $R/figures/akaitools_nife_*.png`.
- Input builder: `$S/akaitools_cuni_input.py`.

**Results.** **447 passed** in 9.1 s.
- The NiFe CPA output converged in 68 iterations, with a total moment of 1.502 μB (Ni 0.696, Fe 2.347) and
  E = −2767.2216 Ry. The bcc Fe output gives 2.169 μB.
- DOS, SCF and BSF all plot.
- A Cu70Ni30 CPA input was built, written and parsed back identically.
- AkaiKKR itself wasn't built; the parser doesn't need it.

**Problems.** Cosmetic only: the `akaitools dos` summary lists components 1, 2, 1, 2 (spin-up and spin-down blocks)
without a spin label.

**Relevance: low**, unless we run KKR-CPA on Cu–Ni or Al–Cu.

## 4. microseg_lab: microscopy segmentation, classical + SAM2 (PASS, headless)

**What it is.** A Streamlit app.
- Classical proposals: watershed, LoG, Otsu/Li, adaptive threshold, edge contours.
- A critic, then optional SAM2 refinement and an optional OpenAI/LangGraph planner.
- Its default target is "Voids", with dark polarity.

**Commands.**
- Install: `uv pip install --torch-backend cpu -r requirements.txt`. Took 7 s from cache; the venv is 1.7 GB.
- Classical run: `$S/microseg_classical.py` on the bundled `spot2_0d_0.tif`, `spot2_0d_4.tif` and `36.jpg`, with
  `--mask spot2_0d_0_mask.tif`.
- SAM2:
  - Cloned facebookresearch/sam2 and installed it with `SAM2_BUILD_CUDA=0 … --torch-backend cpu`.
  - Downloaded the `sam2.1_hiera_tiny.pt` checkpoint (156 MB, 19 s).
  - Ran `$S/microseg_sam2_cpu.py` with `fast_mode` and `runtime_budget=3` (at most 120 masks).

**Results.** These are numeric summaries only. The overlay images were left out, because they reproduce the repo's
own micrographs and the repo has no licence. Details are in `data/microseg_*_summary.json`.

| Run | Time | Candidates → selected | Area segmented | IoU vs bundled mask |
|---|---|---|---|---|
| classical, `spot2_0d_0.tif` (512²) | 41 s | 952 → 250 | 51 % | 0.596 against its complement (0.007 against the mask) |
| classical, `spot2_0d_4.tif` (512²) | 45 s | 908 → 250 | 53 % | – |
| classical, `36.jpg` (6450² scaled to 1024²) | 79 s | 716 → 183 | 1.7 % | – (good enough to skip SAM) |
| classical + SAM2-tiny, `spot2_0d_0.tif` | 92 s total | 400 proposals, 120 masks → 44 | 30 % | 0.348 against its complement |

The bundled mask marks the bright interdendritic network. The default plan picks the dark cells instead, which is
why IoU is high only against the mask's complement. The UI and LLM features weren't run, because there is no
OpenAI key.

**Problems.**
- `run_segmentation()` builds `SAM2Wrapper` before the classical stage. Without SAM2 installed, it fails with
  `RuntimeError: SAM2 root not found: …/microseg_lab/sam2`. The driver here works around this by calling the
  classical stage directly.
- `pipeline.py` imports langchain and langgraph at module level, so the whole LLM stack must be installed even with
  the LLM off.
- `SAM2_ROOT` must point at the inner `sam2/` package, with `SAM2_CFG` under it; otherwise the config name comes out
  as `configs/sam2/configs/...`.
- The default checkpoint isn't shipped (`models/` is empty).
- `.pyc` and `.DS_Store` files are committed.
- scikit-image 0.26 deprecation warnings (`min_size`, `area_threshold`) mean it will break on scikit-image 2.0.

**Relevance: moderate.** The classical dark-voids path is a ready-made LPBF porosity segmenter, and the 512² SEM
sample shows a cellular/dendritic solidification structure. It is slow on CPU, and its thresholds would need tuning
for powder images.

## 5. CGA_Subgraph_Analysis: NbCrVWZr graph and UMAP notebook (PASS)

**What it is.** One notebook. It filters a precomputed NbCrVWZr dataset (UMAP coordinates plus CALPHAD-derived
criteria) on a composition graph, then finds the connected regions that pass every filter.

**Commands.**
- Install: Python 3.10 venv with `-r requirements.txt nbconvert`. That resolved numpy 1.26.4, pandas 2.0.3,
  networkx 3.1 and matplotlib 3.7.5.
- Run: `jupyter nbconvert --to notebook --execute "NbCrVWZr Graph Database Analysis.ipynb" --ExecutePreprocessor.timeout=900`.

**Results.** It ran unmodified in **72 s** with no errors and wrote 41 PNGs and `component_stats.xlsx`.
- The solidification-range filter keeps 3.32 % of compositions.
- The filtered graph has **10,361 connected components**. The largest four have 118, 86, 38 and 26 nodes, with mean
  log10(Kou criterion) of 1.93, 2.35, 3.22 and 2.85
  ([figure](figures/CGA_kde_kou_log10.png), [figure](figures/CGA_temp_vs_node_count.png)).

**Problems.** Minor only: UMAP figures are saved at 800 dpi (about 6 MB each), and seaborn warns about zero-variance
KDEs for single-valued elements.

**Relevance: moderate as a method.** Screening a composition graph with a Kou hot-cracking filter carries over to
printable Al alloys.

## 6. 2026-mulukutla-hall-petch: Hall–Petch in FCC MPEAs (PASS, main analysis)

**What it is.** The companion repo for an Acta Materialia manuscript on yield strength and hardness of 94 FCC
Al–Co–Cr–Cu–Fe–Mn–Ni–V alloy conditions. It has five model families, a Makefile pipeline, regression tests that lock
the paper's numbers, and the paper sources.

**Commands.**
- Install: the requirements minus PyMC, PySR/Julia and Jupyter, with `xgboost-cpu` in place of xgboost to avoid the
  `nvidia-nccl-cu13` CUDA wheel.
- Then `make test`, `make sdgrain`, `make figures`, `make verify` (also on a fresh copy) and `make data`, all with
  `PY=$V/hall-petch/bin/python`.

**Results.**
- **`make test`:** **19/19 passed** (1.4–5 s), both on the shipped data and after regenerating the descriptors. The
  regenerated descriptors match the committed ones to within 2e-13.
- **`make sdgrain`** (2.5 s) reproduces the headline exactly:
  - M15 Q² = **0.731 / 0.694 / 0.694** for 5-fold / LOO / LOBO.
  - M3: 0.666 / 0.652 / 0.625.
  - Additive SD_grain: LOO 0.668 but LOBO 0.595.
  - ΔBIC = **−20.1**; interaction t = 4.71, p = 1.0e-5.
- **`make figures`** (23 s) regenerates 18 figures. 17 differ byte-wise from the committed copies (different
  matplotlib and fonts), and 1 is new.

**Problems.**
- `make data` with matplotlib 3.11.2: `TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'` at
  `eda_analysis.py:407`. `requirements.txt` has no upper bound on matplotlib.
- With matplotlib 3.9.4, `make data` ran past a 10-minute timeout (the docs say about 1 minute). An unbuffered rerun
  shows it is slow, not hung: section-8 cross-validation alone takes more than 4 minutes on 2 threads.
- `make verify` fails on a fresh checkout: `validate_manuscript.py` line 148, `assert definition in manuscript`, raises
  `AssertionError`. The check expects `Composition/processing`, but the paper has `Composition\slash processing`.
- `make test` calls a bare `pytest`, so it fails with `Error 127` unless the venv is on `PATH`.
- A plain `xgboost` install pulls `nvidia-nccl-cu13`.
- Importing `pysr` would download Julia; it isn't needed for the tests.

**Relevance: moderate.** It is a careful template for small-data alloy property modelling, with grouped validation
and tests that lock the paper's numbers.

## 7. Phase-Compatibility-Model-NiTi (PARTIAL)

**What it is.** λ1/λ2/λ3 from lattice parameters, a one-feature B19 vs B19′ rule, and a 186-alloy `data.csv`
(paper: doi:10.1016/j.matdes.2024.113096).

**Commands.**
- Venv with `numpy pandas CBFV HEACalculator nbconvert ipykernel`, then `setuptools<81`, `numpy==1.26.4` and
  `pandas==2.2.2`.
- Run the notebook as shipped, then again with `$S/niti_pc_add_shim.py`, which prepends one compatibility cell
  (4.9 s).
- Check the rule against `data.csv` with `$S/niti_pc_dataset_check.py`.

**Failures as shipped.**
- `ModuleNotFoundError: No module named 'pkg_resources'`: CBFV needs `setuptools<81`.
- `TypeError: HEACalculator.__init__() got an unexpected keyword argument 'csv'`: `helper.py` uses the 1.x API, and
  PyPI only has HEACalculator 2.x.

**With the patch.**
- The λ values (0.930119 / 0.931506 / 1.150677) and the example prediction (B19′, λ2 = 0.92) reproduce exactly.
- `hea_Delta` comes out at 10.30, against 10.83 stored. Across `data.csv`, HEACalculator 2.x gives δ 0.21–0.58
  percentage points lower than the stored values (r = 0.998). That doesn't change the predictions, because the rule
  doesn't use δ.
- On its own `data.csv`, B19/B19′ accuracy is 0.916 (n = 178); all 15 errors are B19 called B19′.
- λ2 MAE is 0.0067, but that is in-sample, since the rule was fit to these data.

**Relevance: low.**

## 8. Transformation-Strain-Model-NiTi (PASS after pinning)

**What it is.** A SymPy transformation-strain calculator plus a CatBoost model on `data_for_ml.csv`.

**Commands.**
- Venv with `numpy pandas sympy scikit-learn catboost CBFV nbconvert ipykernel`, pinned to the versions the notebook
  records: `setuptools<81`, `numpy==1.26.4`, `pandas==2.2.2`, `catboost==1.2.7`.
- Run the notebook with nbconvert and compare it with the stored one using `$S/nb_compare.py`.

**Failures on current versions.**
- `ModuleNotFoundError: No module named 'pkg_resources'` (from CBFV).
- With pandas 3.1.1: `TypeError: unhashable type: 'StringArray'`.
- With catboost 1.2.10 on numpy 1.26: `AttributeError: module 'numpy' has no attribute 'long'`.

**Results after pinning** (30 s).
- 8 of 10 code cells match the stored output exactly; the other two differ only in the version banner and one blank
  line.
- Maximum strain along [110]: 10.008 % in tension, 6.849 % in compression.
- CatBoost 10-fold CV R² **0.954 ± 0.009** (MAE 0.608, RMSE 0.953); `catboost.cv` best validation R² 0.9508 ± 0.0056.

**Relevance: low.**

## Files
- **`data/`:**
  - CALPHAD: `CALPHAD_AlCuMgSi_n4_d20_single_system.csv`, `CALPHAD_mock_TC_equilibrium_All_data.csv` (mock numbers,
    not thermodynamics), `calphad_pycalphad_port_AlSi.csv`.
  - HEACalculator: `heacalculator_compositions.csv`, `heacalculator_handcheck.json`.
  - microseg: `microseg_classical_summary.json`, `microseg_sam2_tiny_cpu_summary.json`.
  - The rest: `hallpetch_sdgrain_m15_validation_rerun.csv`, `niti_phase_compat_dataset_check.json`,
    `akaitools_cuni_cpa.in`.
- **`figures/`:** CALPHAD Scheil plot, CGA Kou and node-count plots, akaitools DOS/SCF/BSF, and two regenerated
  Hall–Petch figures.
- **`scripts/`:** the drivers, the mock `tc_python`, the pycalphad port and the NiTi shim.
- **`logs/`:** step logs.
