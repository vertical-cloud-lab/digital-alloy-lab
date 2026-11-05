## PhaseForgePlus

_Run 2026-11-05, 03:22-03:55 UTC, shared 4-vCPU runner (load average about 12), all commands via `/tmp/sbx/clean`, one thread._

**What it is.** PhaseForgePlus (ArroyaveLab, v0.1.0, HEAD `d16826f`) tunes a CALPHAD TDB by minimising
the negative log-likelihood of ESPEI zero-phase-fraction (ZPF) residuals plus a non-equilibrium
"MLIP regularizer", using scipy CG with analytic (Jansson-derivative) gradients from a gradient-enabled
ESPEI branch by C. Kunselman. Paper: doi:10.1007/s11669-025-01222-2; software: doi:10.5281/zenodo.17519087.

### Step 1: install (PASS)

```bash
cp -a /tmp/arroyave/src/ArroyaveLab__PhaseForgePlus /tmp/arroyave/work/PhaseForgePlus
/tmp/sbx/clean bash -c 'cd /tmp/arroyave/work/PhaseForgePlus && \
  /home/runner/.local/bin/uv venv --python 3.11 /tmp/arroyave/venvs/pfp && \
  UV_PROJECT_ENVIRONMENT=/tmp/arroyave/venvs/pfp timeout 900 /home/runner/.local/bin/uv sync --frozen --python /tmp/arroyave/venvs/pfp/bin/python'
```

- CPython 3.11.18, `uv sync --frozen` (honours `uv.lock`, includes the dev group with pytest 9.1.1). 6 s (wheels cached).
- ESPEI resolves to `espei==0.8.11.dev33+g4888897ee` from
  `git+https://github.com/cjkunselman18/ESPEI.git@4888897eec880b6b9a67484dfb680d7de0a00750` (branch `Gradient-based_update`).
  Other pins: pycalphad 0.11.2, numpy 2.3.2, scipy 1.16.1, symengine 0.13.0.
- Only warning: `` warning: `build_system.requires = ["uv-build>=0.8.3,<0.13.0"]` does not contain the current uv version 0.13.7 `` (harmless).
- The branch has moved on since the lock was written: `git ls-remote` shows `Gradient-based_update` at `1e90221`, but the
  lock pins `4888897`. Everything here used the locked commit.
- **The README install path is broken (FAIL).** `pip install phaseforgeplus` (tested as `uv pip install phaseforgeplus`
  in a fresh venv `/tmp/arroyave/venvs/pfp-pypi`) installs PyPI phaseforgeplus 0.1.0 with **upstream espei 0.9.1**, because the
  git source is a `tool.uv.sources` entry that never reaches the wheel's metadata. The first objective evaluation then fails
  (`scripts/PhaseForgePlus-pypi-check.py`, `logs/PhaseForgePlus-pypi.log`):
  `TypeError: cannot unpack non-iterable numpy.float64 object` at `phaseforgeplus/utils/objective.py:29`
  (`likelihood_zpf, gradient_zpf = residual_func_zpf.get_likelihood(...)`). Only the git checkout with `uv sync` works.

### Step 2: tests (PASS, but the optimizer is untested)

```bash
/tmp/sbx/clean bash -c 'cd /tmp/arroyave/work/PhaseForgePlus && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  timeout 900 /tmp/arroyave/venvs/pfp/bin/python -m pytest -q tests -p no:cacheprovider'
```

- **18 passed, 0 failed, 13 warnings in 18.9 s.**
- But 6 tests are disabled by naming (no `test_` prefix, marked `# FIXME`): `test_main.py::optimizes_with_valid_inputs` and all 5
  tests in `test_objective.py` (`calculates_negative_log_likelihood_correctly`, `handles_empty_zpf_database`,
  `handles_empty_neq_database`, `raises_error_for_invalid_parameters`, `handles_no_symbols_to_fit`). `test_objective.py`
  collects 0 tests, so neither `objective_function` nor `PhaseForgePlus.optimize()` is exercised by CI.

### Step 3: Pt-W example (PARTIAL: runs, objective drops 70 %, cut off by a 560 s budget)

Upstream `example/pt-w.py` calls `pfp.optimize()` with no iteration cap (scipy CG default `maxiter` = 200 x 22 params)
and never writes a TDB. I ran a patched copy, `scripts/PhaseForgePlus-ptw-run.py`, which makes the same
`PhaseForgePlus(...)` and CG calls but stops after 560 s, logs every evaluation and writes the best point to a TDB:

```bash
/tmp/sbx/clean bash -c 'export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1 && cd /tmp/arroyave/results/phaseforge && \
  timeout 900 /tmp/arroyave/venvs/pfp/bin/python -I scripts/PhaseForgePlus-ptw-run.py \
  --data /tmp/arroyave/work/PhaseForgePlus/example/data --out /tmp/arroyave/results/phaseforge --maxiter 20 --budget 560'
/tmp/sbx/clean bash -c '... python -I scripts/PhaseForgePlus-invariants.py --tdb .../example/data/pt-w.tdb data/PhaseForgePlus-PtW-tuned.tdb \
  --labels start tuned --comps PT W VA --xel W --tmin 500 --tmax 3900 --tstep 20 --xstep 0.02 --out data/PhaseForgePlus-PtW-invariants.json'
```

- Setup: imports 3.8 s, constructor 0.7 s; 22 fitted symbols (VV0000-VV0021), 8 ZPF datasets (reference field: ASM International 2008).
- **Objective (negative log-likelihood) 6627.6 -> 2004.5 (-70 %)** in 16 evaluations / 583 s (20-55 s per evaluation on the
  shared 4-vCPU runner, load average about 12); gradient norm 1369 -> 25. Not converged: the objective was still falling
  when the budget stopped it. Largest parameter change 9.2 (kJ for the constant terms). An uncapped run could take hours here.
- **Invariant reaction (pycalphad 0.11.2 `BinaryStrategy`, 5-8 s per map):**

  | TDB | reaction found | T (K) | x(W) of phases |
  |---|---|---|---|
  | start (`example/data/pt-w.tdb`, MLIP-only PhaseForge) | L = FCC + BCC (eutectic type) | 1530.5 | FCC 0.446, L 0.465, BCC 1.000 |
  | tuned (16 evaluations) | L + BCC = FCC (peritectic type) | 2578.5 | L 0.607, FCC 0.609, BCC 1.000 |

  The example's own ASM-derived L + FCC boundary data run up to 2719 K, so the peritectic should sit at or above about
  2720 K: the short tune fixes the reaction type and moves it up by 1048 K, but it is still about 140 K low.
- In `figures/PhaseForgePlus-PtW-start-vs-tuned.png`, drawn by `scripts/PhaseForgePlus-ptw-figure.py`, the tuned
  liquidus and solidus lie on the data. The W-rich BCC solvus data (x(W) 0.95-0.99) are matched by neither TDB: both
  put the BCC boundary at x(W) of about 1.0.

### The "MLIP regularizer" is still silently empty at HEAD `d16826f` (confirmed)

The ORCHID Cu-Zr example's README says PhaseForgePlus 0.1.0's MLIP regularizer is silently empty. That still holds:

- `PhaseForgePlus.__init__` generates 3 NEQ (`HM_MIX`) blocks for Pt-W, but ESPEI's `FixedConfigurationPropertyResidual`
  keeps **0** of them, so the NEQ log-likelihood and gradient are exactly 0.0 at every point; the objective is ZPF only.
- Cause 1: `utils/helpers.py` writes `"phases": phase` (a bare string). ESPEI selects data with
  `where('phases') == [phase_name]`, which gets 0 hits per phase; wrapped as a list it gets 1 hit per phase.
- Cause 2, hidden behind cause 1: the solver key is misspelt `"sublattice_configuraations"`. With the list fix,
  ESPEI's `filter_sublattice_configurations` fails with `KeyError: 'sublattice_configurations'`.
- Cause 3 (`scripts/PhaseForgePlus-neq-fix-probe.py`, `logs/PhaseForgePlus-neq-fix-probe.log`): with both of
  the above patched in memory, ESPEI still fails with `IndexError: list assignment index out of range` at
  `espei/core_utils.py:149` (`cond_shape[cond_idx] = -1` in `ravel_conditions`). `values` has shape (1, 9), but ESPEI
  expects (P, T, configurations) = (1, 1, 9).
- With all three patched, ESPEI keeps all 3 blocks (9 configurations each). The NEQ log-likelihood is -254.78 at the
  start, where the gradient is about 0 because the targets are the start TDB's own `HM_MIX` at 298 K, and -255.01 at the
  tuned Pt-W point, where the ZPF term is about 2000. With `weight: 0.1` (sigma about 5 kJ/mol) the anchor would be weak.
- Component order: `components = list(db.elements)` is set order, and it changed between two runs (`["W","PT"]`, then
  `["PT","W"]`), while the occupancies come from pycalphad's `X` in sorted (PT, W) order. ESPEI's
  `calculate_points_array` pairs each listed species with its listed fraction by position and does not re-sort. In runs
  that draw the `["W","PT"]` order, the patched regularizer would therefore anchor `HM_MIX` at mirrored compositions
  (x -> 1-x). Python's per-process hash seed decides which order you get. Also from the code: the block
  hard-codes `sublattice_site_ratios: [1]`, so it only suits one-sublattice phases, and `points` are indices into
  pycalphad's `calculate()` sample array, not compositions.

### Step 4: Cu-Ni and Al-Cu tuned against ORCHID ZPF data (PASS for running; the tune itself is a no-op from SGTE starts)

Both runs use PhaseForgePlus's own `objective_function` and scipy CG. Each driver copies the open SGTE file
(Hallstedt's SGTE binary collection, CC BY 4.0) and turns two interaction or compound terms into PhaseForge-style
`VV` symbols (`VV0000*1000 + VV0001*T`, `VV0002*1000 + VV0003*T`). It keeps only the phases in the data, writes the
start TDB, and passes `points=[]` because the NEQ part is empty anyway. A second run starts from deliberately
perturbed values to check that the tuner can recover them. Each evaluation takes 0.2-0.7 s because the datasets are tiny.

- **Data.** `orchid-data/espei/index.csv` has **no CU-NI entry**. The only Cu-Ni ZPF file is
  `assessed-phase-assemblages/espei-zpf-with-tie-lines/CU-NI-p359.json`, with 5 one-point-per-field points from the
  assessed handbook diagram (Chakrabarti et al., Phase Diagrams of Binary Nickel Alloys, ASM 1991). Two of those points
  are on the FCC miscibility gap, which ORCHID itself flags as not comparable with SGTE. For Al-Cu I used
  `espei/assessed/AL-CU/AlCu-21Kro.AL-CU-p74.json` (8 points, ASM handbook p74). No PhaseForge MLIP-only Cu-Ni TDB
  had appeared in `results/phaseforge/data/` by 03:52 UTC, so both Cu-Ni starts are SGTE.

```bash
/tmp/sbx/clean bash -c '... python -I scripts/PhaseForgePlus-cuni-run.py --sgte .../sgte-binary/CuNi-92Mey-LB.tdb \
  --zpf .../orchid-data/assessed-phase-assemblages/espei-zpf-with-tie-lines/CU-NI-p359.json --workdir /tmp/arroyave/work/pfp-cuni \
  --out /tmp/arroyave/results/phaseforge --maxiter 50 --budget 200 [--prefix PhaseForgePlus-CuNi-perturbed --perturb VV0000=+6 VV0002=-4]'
/tmp/sbx/clean bash -c '... python -I scripts/PhaseForgePlus-cuni-eval.py --tdb data/PhaseForgePlus-CuNi-{start,tuned,perturbed-start,perturbed-tuned}.tdb ...'
/tmp/sbx/clean bash -c '... python -I scripts/PhaseForgePlus-alcu-run.py --sgte .../sgte-binary/AlCu-04Wit.tdb \
  --zpf .../orchid-data/espei/assessed/AL-CU/AlCu-21Kro.AL-CU-p74.json --workdir /tmp/arroyave/work/pfp-alcu \
  --out /tmp/arroyave/results/phaseforge --maxiter 10 --budget 300 [--maxiter 50 --prefix PhaseForgePlus-AlCu-perturbed --perturb VV0000=+10 VV0002=+5]'
/tmp/sbx/clean bash -c '... python -I scripts/PhaseForgePlus-invariants.py --tdb data/PhaseForgePlus-AlCu-*.tdb ... --comps AL CU VA --xel CU --tmin 500 --tmax 1500 --tstep 10'
```

**Cu-Ni** (start `CuNi-92Mey-LB.tdb`, S. an Mey, Calphad 16 (1992) 255; fitted terms: L0 of LIQUID and of FCC_A1).
Cu-Ni has no three-phase invariant with FCC and liquid only, so the table reports melting range, the ORCHID tie line and
the miscibility-gap top:

| TDB | -logL | evals / s | solidus / liquidus at x(Ni)=0.5 (K) | tie line at 1559.7 K, x(Ni) L / FCC (ORCHID 0.427 / 0.546) | FCC gap top (K, 5 K grid) |
|---|---|---|---|---|---|
| SGTE start | 62.61357 | | 1535.0 / 1585.5 | 0.422 / 0.568 | 640 |
| tuned from SGTE | 62.61356 | 16 / 3.5 (CG converged) | 1538.0 / 1588.5 | 0.414 / 0.560 | 635 |
| perturbed start (L0 liquid +6 kJ, L0 FCC -4 kJ) | 65.43503 | | 1768.5 / 1815.0 | single FCC | 485 |
| tuned from perturbed | 62.61355 | 48 / 15.4 (CG converged) | 1544.0 / 1583.5 | 0.422 / 0.549 | 490 |

**Al-Cu** (start `AlCu-04Wit.tdb`, Witusiewicz et al., J. Alloys Compd. 385 (2004) 133, reduced to LIQUID, FCC_A1,
BCC_A2 and AL2CU_C16; fitted terms: L0 of LIQUID and G of theta-Al2Cu). The reduced phase set drops the Cu-rich
intermetallics, so only the Al-rich eutectic L = FCC + AL2CU_C16 is meaningful. Its handbook value is about 821 K (548 °C):

| TDB | -logL | evals / s | Al-rich eutectic L = FCC + theta (K); x(Cu) FCC / theta / L | notes |
|---|---|---|---|---|
| SGTE start | 93.92038 | | 820.6; 0.025 / 0.318 / 0.175 | |
| tuned from SGTE | 93.92036 | 18 / 4.0 (CG "converged" after 2 iterations) | 830.9; 0.027 / 0.317 / 0.166 | +10 K for a -2e-5 objective change |
| perturbed start (L0 liquid +10 kJ, theta +5 kJ) | 94.89680 | | none; theta + FCC + FCC#2 at 696 K | |
| tuned from perturbed | 93.92036 | 141 / 53 (CG: "precision loss") | L + FCC + theta at 822.6 K, but with a spurious FCC miscibility gap (FCC + FCC#2 + L at 820.1 K, FCC + theta + FCC#2 at 809.0 K) | wrong topology at the SGTE objective value |

What this shows: the machinery works on our systems and is fast when the dataset is small. Starting from SGTE, there
is nothing to tune: the gradient is about 1e-5 and the objective changes in the fifth decimal. From a perturbed start,
CG brings the objective back to the SGTE value and the melting range back within about 10 K. It does not recover the
parameters: Cu-Ni ends at 15.8 kJ / -2.27 against 12.0 kJ / 1.30, and Al-Cu at -61.6 kJ / 4.71 against
-67.1 kJ / 8.56. It also leaves clear side effects that the 5- or 8-point ZPF sets do not penalise: the Cu-Ni gap top
falls to 490 K against 640 K for SGTE, and Al-Cu gains a spurious FCC miscibility gap. With one point per phase field
the problem is under-determined. A regularizer, which here is silently empty, or denser ZPF and thermochemical data
would be needed.

### Problems found (exact error lines)

0. **README install (`pip install phaseforgeplus`) gives a non-working package**: it pulls PyPI espei 0.9.1, so
   `TypeError: cannot unpack non-iterable numpy.float64 object` (`phaseforgeplus/utils/objective.py:29`) on the first
   objective call. Use the git checkout with `uv sync --frozen`.
1. **ESPEI branch mutates the caller's Database.** `get_zpf_data` and `get_thermochemical_data` run
   `dbf.symbols.pop(key,None)` (`espei/error_functions/zpf_error.py:153`, `non_equilibrium_thermochemical_error.py:286`).
   After the first objective evaluation `pfp.db` has lost all 22 `VV` symbols: `database_symbols_to_fit(pfp.db)` and
   `len(pfp.get_initial_values())` both drop from 22 to 0. Any residual or objective built on that Database afterwards
   gets no parameters. In my first probe, a ZPF residual had been built before `objective_function`, and the run failed with
   `IndexError: list index out of range` at `espei/error_functions/zpf_error.py:235`
   (`cond_dict.update({params_keys[index]: parameters[index]})`). `copy.deepcopy(db)` does not protect against this,
   because pycalphad 0.11.2 `Database.__deepcopy__` copies only `_parameters` and shares `.symbols`. A fresh
   `Database(path)` does protect. The branch also sets attributes on the global `pycalphad.variables` module.
2. **`optimize()` never writes a tuned TDB**: it returns a scipy `OptimizeResult`. Because of item 1, simply
   dumping `pfp.db` would give a TDB with undefined `VV` symbols. My drivers write the result into a fresh load.
3. **Optimizer and objective are untested**: 6 tests are disabled with `# FIXME`, as described under Step 2.
4. **Slow objective**: `objective_function` rebuilds both ESPEI residuals, including model compilation, on every call.
   One Pt-W evaluation took 20-55 s here, so the uncapped example (CG `maxiter` 4400) could take hours.
5. **NEQ regularizer empty** (see above): `"phases"` is written as a string, the key is misspelt
   `sublattice_configuraations` (`KeyError: 'sublattice_configurations'`), and `values` has the wrong shape
   (`IndexError: list assignment index out of range`, `espei/core_utils.py:149`).
6. Warnings, none fatal:
   - `UserWarning: pkg_resources is deprecated as an API ... slated for removal as early as 2025-11-30` from
     `espei/refdata.py:43`. The locked environment is safe because it pins setuptools 80.9.0. Once setuptools drops
     `pkg_resources`, an unpinned install will fail on this import.
   - pycalphad on the example TDB: `UserWarning: The type definition character `%` was defined in the following phases:
     ['BCC_A2', 'FCC_A1', 'LIQUID'], but no corresponding TYPE_DEFINITION line was found in the TDB.`
   - The `uv_build<0.13.0` build-requirement warning shown under Step 1.
   - Al-Cu perturbed CG run ended with `Desired error not necessarily achieved due to precision loss.`

Files: `scripts/PhaseForgePlus-{ptw-run,ptw-figure,alcu-run,cuni-run,cuni-eval,invariants,pypi-check,neq-fix-probe}.py`;
`figures/PhaseForgePlus-PtW-start-vs-tuned.png`;
`data/PhaseForgePlus-PtW-{summary,trace,invariants}.json`, `data/PhaseForgePlus-PtW-tuned.tdb`;
`data/PhaseForgePlus-{AlCu,CuNi}{,-perturbed}-{start,tuned}.tdb` with their `-summary.json` and `-trace.json`;
`data/PhaseForgePlus-AlCu-invariants.json`, `data/PhaseForgePlus-CuNi-checks.json`;
`logs/PhaseForgePlus-{install,tests,ptw-example,ptw-invariants,alcu,alcu-perturbed,alcu-invariants,cuni,cuni-eval,pypi,neq-fix-probe}.log`.
The generated Al-Cu and Cu-Ni TDBs are derived from the SGTE files (CC BY 4.0, Hallstedt's collection; original
assessments cited above).

| PhaseForgePlus | PASS via `uv sync --frozen` (py3.11, ESPEI `cjkunselman18/ESPEI@4888897`, 6 s); FAIL via README `pip install` (PyPI espei 0.9.1, objective TypeError) | pytest 18/18 pass (6 FIXME tests disabled, incl. all optimizer tests); Pt-W example capped at 560 s; Cu-Ni + Al-Cu ORCHID ZPF tunes | PARTIAL | Pt-W -logL 6628 -> 2005, invariant 1531 K eutectic-type -> 2578 K peritectic (data put it at 2719 K or above); SGTE Cu-Ni/Al-Cu already fit ORCHID points (tune is a no-op; from perturbed starts the objective recovers but the parameters do not); MLIP regularizer still silently empty (3 bugs: phases string, key typo, values shape); README `pip install` broken; ESPEI branch pops VV symbols from the caller's Database |
