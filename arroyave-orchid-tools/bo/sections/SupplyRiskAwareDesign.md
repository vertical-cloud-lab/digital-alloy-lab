## SupplyRiskAwareDesign

**What it is.** Code samples (`sradd` 0.1.0) for the paper "Supply risk-aware alloy discovery and design: A case study on
the MoNbTiVW system" (Mulukutla et al. 2024, the paper our proposal cites): rule-of-mixtures melting-point constraint,
Curtin-Maresca high-temperature yield strength, Pugh ratio / Cauchy pressure, a weighted alloy supply-risk (SR) index
with element scores and the `S1.json` indicator definition, TC-Python templates (CTE, BCC stability, density, thermal
conductivity), and a small numpy batch-MOBO ("MOBBO": RBF GP with sampled length scales, recursive EHVI,
representative-batch selection). Also ships the paper's four Pareto fronts (with/without SR, constrained/unconstrained) as
xlsx and the SR methodology workbook. No tests, no example driver, no BO campaign script.

**What the repo really contains.** GitHub's API reports size 0, but the clone has 45 tracked files (about 644 KB),
including `datafiles/*.csv` (elemental properties, elastic constants, BCC volumes, SR scores for Mo, Nb, Ti, V, W),
committed `__pycache__/*.cpython-311.pyc` and a `.DS_Store`. The API figure is just stale.

**Commands** (driver: `scripts/SupplyRiskAwareDesign-campaign.py`, plot: `scripts/SupplyRiskAwareDesign-plot.py`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__SupplyRiskAwareDesign /tmp/arroyave/work/srad-asis
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/srad
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/srad/bin/python -e /tmp/arroyave/work/srad-asis      # README path -> fails
# workaround: rebuild the src layout the pyproject expects
mkdir -p /tmp/arroyave/work/srad/src/sradd
cp -r __init__.py composition.py data.py constraints properties supply_risk mobbo datafiles /tmp/arroyave/work/srad/src/sradd/
cp pyproject.toml README.md /tmp/arroyave/work/srad/
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/srad/bin/python -e /tmp/arroyave/work/srad pytest
python -I scripts/SupplyRiskAwareDesign-campaign.py /tmp/arroyave/work/srad-run/s0 0
```

The driver evaluates the repo's own models on a 5 at.% Mo-Nb-Ti-V-W grid (every element >= 5 at.%, 3,876 alloys),
applies the repo's melting-point constraint (3,852 pass), and runs `suggest_batch` for two of the paper's scenarios:
"with SR" (maximise Curtin-Maresca YS at 1300 C and Pugh ratio, minimise SR) and "without SR" (YS and Pugh only).
Scaled down from paper settings: 10 random initial alloys, 4 batches of 5, `n_gp=10` (default 50),
`num_random_points=400` (default 2000). Seed 0, one run.

**Outcome: PARTIAL -> PASS with a packaging fix.** The README install fails as shipped; after rebuilding the `src/sradd`
layout everything imports, the data loaders work, and the batch MOBO runs end to end. Thermo-Calc helpers not run (licence).

| Step | Result | Wall time |
|---|---|---|
| `uv pip install -e .` as shipped | **FAIL**: `error: error in 'egg_base' option: 'src' does not exist or is not a directory` | 1 s |
| install with rebuilt `src/sradd` layout | OK (numpy, pandas, scipy 1.18.1, openpyxl) | 1 s |
| imports + data loaders | OK; SR scores Mo 63.97, Nb 43.79, Ti 41.33, V 60.90, W 49.17 | <1 s |
| ground truth on 3,876 alloys (YS, Pugh, SR, Tm) | OK | 1.0 s |
| campaign, with SR (3 objectives), 4 batches | OK; `suggest_batch` 34-77 s per call | ~230 s |
| campaign, without SR (2 objectives), 4 batches | OK; `suggest_batch` 5-8 s per call | ~25 s |

**Key numbers** (`figures/SupplyRiskAwareDesign-mobbo.png`, `data/SupplyRiskAwareDesign-s0-*.csv|json`):
- After 30 evaluations: hypervolume reaches **0.978** of the full-grid Pareto front without SR and **0.814** with SR (the
  3-objective front is larger, so it is harder to cover with 30 points).
- Mean SR of the found Pareto set: **50.7** with SR vs **52.9** without SR (minimum 45.6 vs 52.0). Adding SR as an
  objective steers the batch toward lower-risk alloys (Ti and Nb carry the lowest element scores), as the paper argues; one seed, so treat it as
  directional only.
- Cost: the recursive EHVI takes ~10x longer per batch with 3 objectives than with 2 (57-77 s vs 5-8 s per call on one
  thread), so going to 4-5 objectives needs a faster HV/EHVI (e.g. BoTorch box decompositions).

**Problems found**
1. Packaging mismatch: `pyproject.toml` declares `package-dir = {"" = "src"}` and package data `sradd/datafiles/*`,
   but the files sit at the repo root and there is no `src/` -> `error: error in 'egg_base' option: 'src' does not exist or is not a directory`.
   The modules import each other as `from sradd.composition import ...`, so running from the root fails too
   (`ModuleNotFoundError: No module named 'sradd'`).
2. `data.py` sets `PROJECT_ROOT = Path(__file__).resolve().parents[2]`, which also assumes the missing `src/sradd/` layout.
3. Committed build junk: `__pycache__/*.cpython-311.pyc` in five directories and `.DS_Store`.
4. README says the data are under `/datafiles/` and describes a "Quick start" that does not work; there is no example
   that runs the MOBBO loop, and no seeds or tests.
5. `Pareto_finder` and EHVI are pure-Python O(n^2) loops plus recursive HV, the main bottleneck (above).
6. The TC-Python helpers (`constraints/thermocalc.py`, `properties/thermocalc.py`) are templates with parameterised model
   names; not runnable without a Thermo-Calc licence.

**Relevance to us: high.** It is the reference implementation of the supply-risk-aware design in the paper our proposal
cites. The SR index (indicator definition in `S1.json`, element scores as CSV) is easy to extend to Al-alloy
elements (Al, Mg, Si, Zn, Cu, Sc, Zr, Er...) and to use either as an objective (as here) or as an acquisition weight (as in
rhea-mobo). The numpy MOBBO itself is slow and composition-only; we would port the SR objective into our BoTorch/BOFN stack
rather than adopt this optimiser.

TABLE: SupplyRiskAwareDesign | FAIL as shipped (`src` missing); OK after rebuilding `src/sradd` layout | MoNbTiVW grid, batch MOBBO with/without SR (10 + 4x5) | PARTIAL (packaging bug; science code PASS) | HV 0.814 (with SR) / 0.978 (without); Pareto mean SR 50.7 vs 52.9; 3-obj EHVI ~10x slower
