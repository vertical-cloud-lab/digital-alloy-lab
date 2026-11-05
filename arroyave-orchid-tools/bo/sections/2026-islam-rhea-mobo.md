## 2026-islam-rhea-mobo

**What it is.** `rhea-mobo` (Islam, Sarıtürk et al., 2026; software DOI 10.5281/zenodo.22258223): supply-risk-aware
multi-objective BO for six-component Mo-Nb-Ta-W-Co-Hf refractory HEAs. BoTorch `SingleTaskGP` per objective in a
`ModelListGP`, analytic 5-objective EHVI, acquisition divided by an alloy supply-risk index
`R_alloy = sum(x_i R_i)` (`CostAwareEHVI`), discrete stochastic local search over a 5 mol% feasible grid. The physics
objectives (printability, yield strength, crack susceptibility, lattice misfit, Young's modulus) need licensed
TC-Python (TCHEA7) plus MaterialsFramework/ORB; a license-free synthetic toy (`rhea_mobo.toy`) and a pytest suite are
included. The most polished, best-tested repo in this group.

**Commands** (full script: `scripts/2026-islam-rhea-mobo-run.sh`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__2026-islam-rhea-mobo /tmp/arroyave/work/rhea-mobo
# toy env, exactly as in the README but CPU torch
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/rhea-mobo
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/rhea-mobo/bin/python --torch-backend cpu -r requirements-toy.txt pytest
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-default                       # README default: 8 initial, 3 additions, seed 42
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-it15-s42 --iterations 15 --seed 42
PYTHONPATH=src python -m rhea_mobo.toy --output toy-output-it15-s7  --iterations 15 --seed 7
# full env for the test suite (NOT `uv sync`, see problems)
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/rhea-mobo-full
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/rhea-mobo-full/bin/python --torch-backend cpu -e . pytest
python -m pytest tests/ -v
python scripts/predicted_correlation.py          # RF feature importance + objective correlations from data/predictions.csv
rhea-mobo                                       # production loop: needs tc_python
```

**Outcome: PASS** (tests, toy BO and analysis script); production BO loop NOT RUNNABLE without a Thermo-Calc licence
(by design, documented).

| Step | Result | Wall time |
|---|---|---|
| toy-env install (torch 2.14.1+cpu, botorch 0.18.1, gpytorch 1.15.2) | OK (uv cache warm) | 3 s |
| pytest in toy env | collection error: `ModuleNotFoundError: No module named 'pymatgen'` (test_composition needs the full env) | 19 s |
| full install `-e .` (materialsframework 1.0.0 [orb, sqsgen], orb-models 0.7.0, pymatgen 2026.10.24, torch 2.15.0+cpu) | OK, venv 1.7 GB | 16 s |
| `pytest tests/` (full env) | **24 passed**, 0 failed | 49 s |
| toy, README default (8 init + 3 additions) | OK | 12 s |
| toy, 15 additions, seeds 42 and 7 | OK | 25 s, 34 s |
| `scripts/predicted_correlation.py` | OK, 2 figures | 15 s |
| `rhea-mobo` CLI | `ModuleNotFoundError: No module named 'tc_python'` (expected) | <5 s |

**Key numbers** (synthetic toy, 1,716-point grid, 1,621 feasible, 12-point oracle Pareto front, oracle HV 29.165, ref
point (-1,...,-1)):
- README default (8 + 3, seed 42): BO reaches **0.811** of the oracle hypervolume vs **0.722** for the paired random baseline.
- 8 + 15, seed 42: BO **0.883** vs random **0.765**; seed 7: BO **0.886** vs random **0.921** (random wins on this seed).
  With 2 seeds and a toy objective this is a smoke test only, as the README itself says; the plot
  `figures/2026-islam-rhea-mobo-toy-hv.png` shows the two curves per seed.
- `figures/2026-islam-rhea-mobo-feature-importance.png`, `figures/2026-islam-rhea-mobo-objective-correlation.png`
  (downscaled from the script's 600-dpi output) reproduce the analysis of the shipped 1,716-row `data/predictions.csv`.
- Data: `data/2026-islam-rhea-mobo-toy-*-summary.json`, `data/2026-islam-rhea-mobo-toy-it15-s*-comparison.csv`.

**Problems found**
1. `uv.lock` resolves torch with CUDA wheels on x86_64 (`{ name = "nvidia-cublas", marker = "platform_machine == 'aarch64' or platform_machine == 'x86_64'" }`),
   so the documented/CI path `uv sync --all-extras` pulls several GB of NVIDIA libraries on a CPU-only box. Workaround:
   `uv pip install --torch-backend cpu -e .`.
2. The toy env from `requirements-toy.txt` cannot run the full test suite: `tests/test_composition.py:8: from pymatgen.core import Composition` ->
   `ModuleNotFoundError: No module named 'pymatgen'`. Only `test_toy.py` etc. are toy-safe; a `pytest -m toy` marker or
   `importorskip` would help.
3. `requirements-toy.txt` pins torch 2.14.1 while `-e .` resolves torch 2.15.0; both work, so the pins are tighter than needed.
4. Production loop (`rhea-mobo`, `scripts/bo_script_full.py`) imports `from tc_python import *` at module import time,
   so even `--help` fails without TC-Python: `ModuleNotFoundError: No module named 'tc_python'`.
5. Cosmetic: `FutureWarning: torch.jit.script is deprecated` from the linear-operator / gpytorch stack on torch 2.14+.
6. Config defaults (`config.py`: 50 initial samples, 200 iterations, 20 restarts, 50 raw samples) are paper-scale; the
   original campaign history is not archived (README says so), so the paper's hypervolume trajectory cannot be replayed.

**Relevance to us: high.** It is the closest drop-in for supply-risk-aware acquisition: `CostAwareEHVI` (EHVI divided by
a per-candidate index) is a ~30-line BoTorch wrapper we could reuse with an Al-alloy element risk/cost table, and the
discrete-grid local search fits composition grids. It is sequential (q=1), single-fidelity and composition-only (no
process parameters), so for LPBF we would add process dims and swap EHVI for qLogNEHVI or a multi-fidelity/BOFN model.

TABLE: 2026-islam-rhea-mobo | OK (CPU torch; avoid `uv sync`, lock pulls CUDA) | pytest 24/24; toy BO 8+3 and 8+15 x2 seeds; correlation script | PASS (production loop needs TC-Python licence) | supply-risk-weighted EHVI; BO 0.883 vs random 0.765 (seed 42), 0.886 vs 0.921 (seed 7)
