# Issue #235: PhaseForge / MLIP stack (ArroyaveLab): install and test runs

> In this copy, `data/PhaseForgePlus-PtW-tuned.tdb` is left out because it derives from PhaseForgePlus's example Pt–W TDB, and that repo declares no licence. The Pt–W command below regenerates it. Paths under `/tmp/arroyave/` are the runner's scratch space; `results/phaseforge/` there is this folder.

This run was on 2026-11-05, 03:19–04:40 UTC, on a CPU-only runner (4 vCPU, 15 GB) shared with other agents. Every install and every third-party script ran through the scrubbed-environment wrapper `/tmp/sbx/clean`. ATAT and the GRACE model cache used `HOME=/tmp/arroyave/home`.

Repos are the shallow clones under `/tmp/arroyave/src/ArroyaveLab__<repo>`. Each was copied to `/tmp/arroyave/work/<repo>` before running.

- The PhaseForgePlus section was written by a delegated sub-agent.
- So were the BLADE, sqs-benchmark and PAIPAI sections.
- ATAT, PhaseForge and MaterialsFramework were done directly.

**MLIP used throughout:** GRACE-2L-OMAT through MaterialsFramework's `GraceCalculator`, on CPU, with tensorpotential 0.6.2.1 and TensorFlow 2.19.1. The venv is `/tmp/arroyave/venvs/paipai`: Python 3.12 with MaterialsFramework 0ec8168 `[grace]` and pycalphad 0.11.2. It was built during the PAIPAI test and reused here. MaterialsFramework requires Python `>=3.12,<3.13`, so a 3.11 venv cannot be used.

The GRACE-2L-OMAT weights (92.7 MB) download on first use and are under an **Academic Software License (non-commercial)**. On Linux, `tensorpotential` pulls `tensorflow[and-cuda]`, so the 12 NVIDIA wheels had to be removed by hand to stay CPU-only.

## ATAT (Alloy Theoretic Automated Toolkit) 3.52, a dependency of PhaseForge, BLADE and sqs-benchmark

- **Source:** `https://axelvandewalle.github.io/www-avdw/atat/atat3_52.tar.gz` (4.4 MB, sha256 `8536fb07…7c516`, tarball dated 2026-07-30).
- **Licence:** Creative Commons **Attribution-NoDerivatives 4.0 (CC BY-ND 4.0)**, per the web page and `license.txt`. Modified copies may not be redistributed, so patched ATAT scripts cannot be shared.
- **Build:** `make -j2 BINDIR=/tmp/arroyave/atat/bin/ && make BINDIR=/tmp/arroyave/atat/bin/ install`, run in `/tmp/arroyave/atat`.
  - It needs `/bin/csh`. I added `sudo apt-get install -y tcsh`.
  - `make install` writes `$HOME/.atat.rc`; that is how `sqs2tdb` and `fitfc` find `data/sqsdb`.
- **Outcome: PASS.** The build took 34 s and installed 73 binaries, including `mcsqs`, `corrdump`, `sqs2tdb`, `runstruct_vasp`, `foreachfile` and `fitfc`. There were 0 errors and 39 compiler warnings (`logs/atat-build.log`).
- **Problems found when PhaseForge drives ATAT 3.52** (details in the PhaseForge section):
  1. `sqs2tdb -cp` prints `sh: 1: Syntax error: "&" unexpected` for every SQS directory. A csh-style `>&` redirect is run by `/bin/sh`, which is dash on Ubuntu. The SQS files are still copied.
  2. On first use, `runstruct_vasp -nr` only creates `~/.ezvasp.rc` ("I have created a default ~/.ezvasp.rc configuration file for you. Please edit it…") and exits 0 without writing a POSCAR.
  3. On every later call, `runstruct_vasp -nr` writes a **2-line, empty POSCAR**, because the awk program it generates does not parse:
     `awk: tmp.awk:27: print "    if (\`echo \"$checkrelaxcutoff $relax_val\" | awk '" (if ($1 < $2) print 1; else print 0) "'\` == 1) then"` … `^ syntax error`. The awk here is GNU awk 5.
  4. With only one mcsqs process, `bestsqs.out` is never written (found by the BLADE run).

## PhaseForge (ArroyaveLab/PhaseForge @ 4f88f0d)

**What it is.** csh wrapper scripts (`sqscal`, `runstruct_MLIP`, `MLIPrelax`, `MLIPmd`, `MLIPliquid` …) plus one C++ tool (`ternary_search`). They glue ATAT's `sqs2tdb` SQS database and fitter to MaterialsFramework MLIP calculators: MLIP → SQS energies → Redlich–Kister fit → TDB. Licence GPL-3.0.

**Commands**
```sh
cp -r /tmp/arroyave/src/ArroyaveLab__PhaseForge /tmp/arroyave/work/PhaseForge
cd /tmp/arroyave/work/PhaseForge && mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/tmp/arroyave/work/PhaseForge/install && make -j2 && make install
# goal run (scripts/PhaseForge-run_sqscal.sh): PATH = venv/bin : PhaseForge/install/bin : atat/bin
sqscal -e Cu,Ni -l FCC_A1 -lv 1 -mlip Grace -model GRACE-2L-OMAT
```

**Outcome: PARTIAL.** The build works. `sqscal` runs to the end and exits 0, but every MLIP energy is missing, so the TDB it writes has no Gibbs-energy parameters. The equivalent step-by-step calculation with the same SQS, MLIP and fit model does work. It is shown below and compared with SGTE.

**Build.** `make` compiles `ternary_search` (C++14, < 2 s). `make install` then fails:
`CMake Error at cmake_install.cmake:50 (file): file INSTALL cannot find ".../third_party/lammps/src/ML-GNNP": No such file or directory.`
The `install()` rule needs the `third_party/lammps` git submodule, a LAMMPS fork. A plain or shallow clone does not have it, and the README's build instructions don't mention `--recurse-submodules`. The scripts in `bin/` are installed before the error, so the non-LAMMPS path is usable (`logs/PhaseForge-cmake-build.log`). The README's prerequisites also omit **csh/tcsh**: every script is `#!/bin/csh -f`.

**sqscal run: Cu–Ni, FCC_A1, level 1** (Cu, Ni, and the 32-atom Cu16Ni16 SQS)
- **First run** (`logs/PhaseForge-sqscal-CuNi-FCC-lv1.log`): killed by my 840 s `timeout`, with no MLIP calculation done.
  - `runstruct_MLIP` printed only `MLIP Name=Grace` / `Model=GRACE-2L-OMAT` in each directory.
  - `sqs2tdb -fit` then reported `Found no data for energy` … `Fit completed`.
  - `sqs2tdb -tdb -oc` printed `Phases found in SGTE database:` and then **blocked**, apparently reading stdin. With `< /dev/null` it finishes in 0.1 s.
- **Cause** (`logs/PhaseForge-runstruct_MLIP-trace.log`, `csh -fx`): ATAT 3.52's `runstruct_vasp -nr` writes an empty POSCAR (ATAT item 3 above). `MLIPrelax.py` then fails with `ValueError: Empty POSCAR`, and `extract_MLIP` with `sed: can't read CONTCAR` and `numbers: Subscript out of range`. `runstruct_MLIP` only tests `-e POSCAR`, which is true for an empty file, and `sqscal` never checks exit codes.
- **Re-runs** (`-rerun.log`, `-shim.log`): `sqscal` exits 0 in 0.14 s and writes `CU_NI.tdb` containing only ELEMENT/PHASE/CONSTITUENT lines, i.e. a silent failure. I replaced `runstruct_vasp` with a POSCAR-writing shim (`scripts/PhaseForge-shim/runstruct_vasp`), but `runstruct_MLIP` under `foreachfile` still returned without relaxing. I ran out of time to trace this.
- **LIQUID** (`MLIPliquid` + `ternary_search`, MD) was not attempted. At ~2 s per force call on 1 thread for ~100–250 atoms, a 2000-step NVT run per composition and volume costs CPU-hours.

**Step-by-step equivalent** (`scripts/PhaseForge-mlip_stepwise.py`, `logs/PhaseForge-mlip_stepwise.log`)
- **Method:** the same three ATAT SQS (`sqs_lev=0_a_Cu=1`, `sqs_lev=0_a_Ni=1`, `sqs_lev=1_a_Cu=0.5,a_Ni=0.5`, 32 atoms) were read with `pymatgen.io.atat` and scaled to a Vegard volume. They were relaxed with `GraceCalculator(model="GRACE-2L-OMAT", fmax=0.005).relax()` with the full cell free (MLIPrelax uses fmax 0.001).
- **Timings:**
  - Model load plus the first EOS: 6.4 s.
  - Cu and Ni endmembers: 0.1 s and 0.2 s.
  - The 32-atom SQS: 9.1 s.
  - The whole script, including the EOS below: 23 s wall on 2 threads.

  A level-1 FCC run is therefore cheap on CPU. The cost of a full `sqscal` is dominated by LIQUID MD and `-vib` phonons, not by SQS relaxation.
- **Mixing energy:** E(Cu16Ni16) = −4.601805, E(Cu) = −3.755034, E(Ni) = −5.493778 eV/atom.

  ΔH_mix(x=0.5) = **+22.6 meV/atom = +2.18 kJ/mol**, so the level-1 fit, which has only `terms.in` 1,0 and 2,0, gives **L0(FCC_A1) = +8.72 kJ/mol**. It has no temperature dependence because there is no `-vib` term.
- **SGTE comparison:** the open SGTE CuNi-07Tur assessment (Turchanin et al. 2007, via Hallstedt's SGTE collection, doi:10.1016/j.calphad.2025.102833, CC BY 4.0) has L0 = 6877 + 4.6T J/mol (+8.26 kJ/mol at 300 K, +13.8 kJ/mol at 1500 K) and L1 = −2450 + 1.87T.

  The MLIP value therefore matches SGTE near room temperature. It lacks the large positive excess-entropy term that SGTE needs at high temperature.

**Cu–Ni phase diagram vs SGTE** (`scripts/PhaseForge-CuNi_pycalphad.py`, `data/PhaseForge-CuNi-GRACE-FCC-L0-on-SGTE07Tur.tdb`, `data/PhaseForge-CuNi-pycalphad-comparison.json`, `figures/PhaseForge-CuNi-SGTE-vs-GRACE.png`)

**Comparison model.** The comparison TDB is a hybrid: CuNi-07Tur with its FCC_A1 L0/L1 replaced by the single MLIP L0. It keeps SGTE's unaries, its magnetic TC/BM interaction terms and its LIQUID, because the MLIP liquid step was not run. Equilibria come from pycalphad 0.11.2 with a 4 K grid, LIQUID + FCC_A1, and took 4 s.

| x(Ni) | 0.05 | 0.15 | 0.25 | 0.35 | 0.45 | 0.55 | 0.65 | 0.75 | 0.85 | 0.95 |
|---|---|---|---|---|---|---|---|---|---|---|
| SGTE solidus / liquidus (K) | 1380/1392 | 1420/1452 | 1452/1500 | 1484/1544 | 1520/1580 | 1556/1612 | 1596/1640 | 1640/1664 | 1680/1692 | 1716/1716 |
| GRACE-L0 FCC + SGTE liquid (K) | 1392/1432 | 1460/1544 | 1524/1620 | 1588/1672 | 1652/1708 | 1704/1732 | 1740/1748 | 1756/1756 | 1756/1756 | 1740/1744 |

- **Solidus and liquidus:** with the MLIP FCC term, FCC is too stable against SGTE's liquid.
  - The solidus is up to **+148 K** too high (at x = 0.55) and the liquidus up to **+128 K** (at x = 0.35–0.45).
  - The freezing range widens at the Cu-rich end, for example 84 K instead of 32 K at x = 0.15.
  - A **spurious congruent maximum of about 1756 K** appears near x(Ni) ≈ 0.75–0.85, above the melting point of Ni (1728 K).

  The cause is the missing +4.6·T excess entropy in FCC, combined with a liquid that did not come from the MLIP. A consistent PhaseForge description needs the MLIP liquid, or at least a vibrational term.
- **FCC miscibility gap top:** **520 K** with GRACE, against **600 K** for SGTE (10 K grid). The regular-solution estimate L0/2R = 525 K agrees. The gap is 80 K too low.
- **Not done (time):** Al–Cu and Al–Si FCC_A1 + LIQUID.

## MaterialsFramework (ArroyaveLab/MaterialsFramework @ 0ec8168, v1.0.0)

**What it is.** A Python framework that wraps 25+ MLIP calculators behind a common `relax` / `calculate` / MD / EOS / elastic / phonon API. PhaseForge, PAIPAI and BLADE all call it. Licence GPL-3.0.

**Commands.** Install: venv `/tmp/arroyave/venvs/paipai` with `uv pip install '<copy>[grace]'` (see the PAIPAI section). Tests, run from the copy `/tmp/arroyave/work/MaterialsFramework`:
```sh
python -m pytest -q -p no:cacheprovider tests
```
EOS: `scripts/PhaseForge-mlip_stepwise.py`. It runs `GraceCalculator.calculate` on fcc conventional cells at 9 volumes within ±6 %, with a Birch–Murnaghan fit from `ase.eos`.

**Outcome: PASS.** pytest: **379 passed, 71 skipped, 0 failed in 10.5 s** (`logs/MaterialsFramework-pytest.log`). The skips are:
- `chgnet` not installed: most skips;
- `sqs2tdb binary not found`: ATAT was not on PATH for this run;
- `VASP not configured`;
- PosEGNN model missing;
- `sqsgenerator` missing.

The CI-style tests therefore don't exercise GRACE itself; the EOS run below does.

**EOS with GRACE-2L-OMAT** (`data/PhaseForge-CuNi-GRACE-energies.json`), 3–6 s per element:

| fcc | a0 (Å) GRACE | a0 exp | B (GPa) GRACE | B exp |
|---|---|---|---|---|
| Al | **4.038** (−0.3 %) | 4.05 | **78.5** (+3 %) | ≈ 76 |
| Cu | **3.611** (−0.1 %) | 3.615 | **144.5** (+3 %) | ≈ 140 |
| Ni | 3.508 (−0.5 %) | 3.524 | 201 (+8 %) | ≈ 186 |

Elastic constants were not run (time).

**Problems.**
- The package needs Python 3.12 (`requires-python >=3.12,<3.13`).
- The `[grace]` extra drags in CUDA wheels on Linux.
- Downstream repos (PAIPAI, BLADE) call keyword arguments (`device=`, `max_steps=`, `Sqs2tdb.fit(paths=…)`) that this public release lacks; see those sections.

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


## BLADE

**What it is.** BLADE ("Boride Learning and Design Engine", ArroyaveLab/BLADE at 9d3859c, commit "Version 1.2", pyproject version 0.2.0) is a Python wrapper that runs a CALPHAD workflow in four stages: enumerate N-component systems, generate SQS with ATAT `sqs2tdb -mk` / `corrdump` / `mcsqs`, relax them with an MLIP and fit a `.tdb` through MaterialsFramework's `Sqs2tdb`, then plot or tabulate the results. Its demo targets AlB2-type high-entropy diborides (HEDB1).

**Environment.** venv `/tmp/arroyave/venvs/blade` (Python 3.12, uv), ATAT 3.52 from `/tmp/arroyave/atat/bin` with `HOME=/tmp/arroyave/home`, and every command run through `/tmp/sbx/clean` with `OMP_NUM_THREADS=1`. For the TDB-stage check I used `/tmp/arroyave/venvs/paipai`, which has the upstream ArroyaveLab MaterialsFramework 0ec8168 (v1.0.0), tensorpotential 0.6.2.1, TF 2.19.1 on CPU and pycalphad (see the PAIPAI section). The shared mlip venv did not exist yet when I needed it.

### Commands and outcomes

| # | Command (cwd = copy in `/tmp/arroyave/work/BLADE`) | Result | Wall time |
|---|---|---|---|
| 1 | `uv pip install -e .` | installs, but only `blade` itself, because `pyproject.toml` has `dependencies = []` | 2 s |
| 2 | `python -c "import blade; blade.BladeSQS"` (and the other classes) | `BladeCompositions` and `BladeTDBGen` import; `BladeSQS`, `BladeCutoff` and `BLADEVolume` fail with `ModuleNotFoundError: No module named 'numpy'`; `BladeVisualizer` fails with `No module named 'imageio'` | <1 s |
| 3 | `uv pip install numpy pandas matplotlib pillow imageio ase pymatgen pycalphad` | OK | 4 s (cached) |
| 4 | `python examples/01_compositions.py` | **PASS**: 10 ternaries from 5 TMs, 10 binary+ternary systems from 4 TMs, 6 TM2+RE systems; all counts match C(n,k) | 0.03 s |
| 5 | `python examples/02_sqs_generation.py` (unmodified) | **FAIL**: `TypeError: BladeCompositions.__init__() got an unexpected keyword argument 'transition_metals'` | <1 s |
| 6 | `python examples/03_tdb_generation.py` (unmodified) | **FAIL**: same TypeError (the example also hard-codes `/Users/...` paths and `device="cuda"`) | <1 s |
| 7 | `python scripts/BLADE-run_sqs_small.py <scratch> 10 1`: example 02 with today's keyword names, the HEDB1 prototype, Cr-Hf binary only (`level=3`, giving sqsgen levels 0/1/2/5), a 2x2x2 supercell (24 atoms: 8 metal + 16 B), 1 mcsqs process for 10 s per directory | SQS made (objectives below), but **no `bestsqs.out`/`bestcorr.out`** (ATAT quirk below) and an empty `objective_functions.txt` | 121 s |
| 8 | the same with 2 mcsqs processes (`-ip=1,2`) | **PASS**: `sqs2tdb -mk` makes 5 `sqsdb_lev=*` dirs; corrdump, mcsqs and `mcsqs -best` all work and `objective_functions.txt` is written | 121 s |
| 9 | `python scripts/BLADE-analysis_smoke.py ...`: BLADEVolume (example 05) and `BladeVisualizer.contcar` (example 04, part 1) on POSCARs converted from the run-8 `bestsqs.out` | **PASS**: 4 rows in the DataFrame, combined PNG written | 6 s |
| 10 | `python scripts/BLADE-tdb_stage_check.py` (`BladeTDBGen.fit()` on the run-8 tree) with upstream MaterialsFramework | **FAIL**: `TypeError: object.__init__() takes exactly one argument (the instance to initialize)` from `GraceCalculator(steps=1000, device="cuda")` | 2 s |
| 11 | as 10, with a shim that drops `device=` (`scripts/PAIPAI-shim/sitecustomize.py`) and pycalphad added | **FAIL**: `TypeError: Sqs2tdb.fit() got an unexpected keyword argument 'paths'`. BLADE needs the ichasekatz fork of MaterialsFramework, which was not provided, so the fork was not tried | 2 s |

Not run: example 04 parts 2 and 3 (they need phase-diagram PNGs and `relaxation_live.xyz` files from the TDB stage) and `examples/tdb_gen.py` (an HPC driver for the whole pipeline that also needs the fork).

**Outcome: PARTIAL.** Composition enumeration, SQS generation with ATAT, and the volume and visualization analysis all work once the examples are fixed and shrunk. As shipped, examples 02 and 03 fail at once. The MLIP/TDB stage cannot run against ArroyaveLab's MaterialsFramework because it needs a fork with a different API.

### Key numbers (run 8, HEDB1 Cr-Hf, 24-atom cells, 2 x 10 s mcsqs per directory)
`data/BLADE-objective_functions.tsv`: objectives -85.860 (x=0.5/0.5), -46.135 (0.75/0.25), -46.139 (0.625/0.375) and -46.162 (0.875/0.125). BLADE passed `-2=2.17945 -3=2.0 -4=1.73205` to corrdump and mcsqs. Those are the 5th, 4th and 3rd shells over *all* sites divided by the B–B distance (a/√3), then used as absolute lengths; see problem 3. In this a = c = 1 cell they still give metal-pair clusters at 1.0, 1.414, 1.732 and 2.0. `figures/BLADE-contcar-smoke.png` (328 KB) shows the four unrelaxed SQS cells, and `data/BLADE-volume-smoke.csv` holds the BLADEVolume table. The volumes there come from my x3.1 scaling of a = 1, so they mean nothing physically.

### Problems found (exact messages)
1. **The examples are out of date with the API.** `examples/02_sqs_generation.py` and `03_tdb_generation.py` use `transition_metals=`, `rare_earths=`, `tm_min=`... and fail with `TypeError: BladeCompositions.__init__() got an unexpected keyword argument 'transition_metals'`. Example 01 and the README use the current `primary_elements=` names. All examples hard-code `/Users/<author>/Desktop/School/Research/...`.
2. **No runtime dependencies are declared** (`dependencies = []`), so a plain `pip install` gives `ModuleNotFoundError: No module named 'numpy'` / `'imageio'`. Users need numpy, pandas, matplotlib, pillow, imageio and ase, plus pycalphad, pymatgen, torch and MaterialsFramework for the full pipeline.
3. **Cutoff unit bug in `BladeSQS.sqs_gen`.** `BladeCutoff.get_shells()` returns shell radii *divided by the shortest distance between any two sites*, fixed sublattices included (its docstring says "dimensionless cutoff ratios"). `sqs_gen` nevertheless passes them straight to `corrdump`/`mcsqs` as `-2=`/`-3=`/`-4=`, which ATAT reads in rndstr length units. The resulting cutoffs are therefore not the requested Nth-neighbour shells. In BLADE's own HEDB1 example (a = c = 1) the scale factor is the B–B distance, 0.577, so the "5th-shell" pair cutoff becomes 2.179 instead of 1.258. That still gives clusters, so the error is easy to miss. With a real lattice constant (the sqs-benchmark BCC NbVW case, a = 3.165 Å, 1NN 2.74 Å) the cutoffs become 2.0 / 1.91 / 1.63 Å. corrdump then prints `Cluster file contains no clusters.` and every mcsqs exits with code 1 (`logs/sqs-benchmark-03a-mini-sqs-unpatched-cutoffs.log`). When every site mixes (BCC NbVW), multiplying the ratios back by the 1NN distance fixes it (`scripts/sqs-benchmark-mini.py`). For prototypes with fixed sublattices, the shells should probably also be counted on the mixing sublattice only.
4. **`parallel_runs=1` silently gives no SQS.** BLADE runs `mcsqs -ip=1..N` and then `mcsqs -best`. In ATAT 3.52, `-best` writes and runs a `findbestsqs` script that does `grep -n Objective bestcorr?*.out`. With a single file grep omits the filename, so the script fails with `./findbestsqs: 3: [: 34: unexpected operator` / `cp: cannot stat '34': No such file or directory`. `bestsqs.out`/`bestcorr.out` are never written, `_write_objective_summary` reports `No bestcorr.out found`, and `BladeSQS` itself raises nothing. It works with 2 or more processes.
5. **mcsqs often outlives `stopsqs`.** 7 of 12 mcsqs processes printed `mcsqs -ip=N ignored stopsqs; terminating` with `stop_grace=10` and were SIGTERMed (exit code -15). Their best-so-far files were still usable.
6. **The TDB stage is tied to a fork and to CUDA.** `blade_tdb_gen.py` hard-codes `GraceCalculator(steps=1000, device="cuda")` and calls `Sqs2tdb.fit(paths=..., sqsgen_levels2=...)`. Upstream MaterialsFramework 0ec8168 has neither `device` (`TypeError: object.__init__() takes exactly one argument`) nor `paths` (`TypeError: Sqs2tdb.fit() got an unexpected keyword argument 'paths'`). The README says the ichasekatz fork is required.
7. Smaller issues: `BladeCompositions.get_systems()` raises `IndexError` if no compositions were generated, and `monitor_bestcorr_parallel` writes history rows ending in `\t` instead of `\n`, so `objective_history.txt` comes out as one long line.

Scripts: `scripts/BLADE-run_sqs_small.py`, `scripts/BLADE-analysis_smoke.py`, `scripts/BLADE-tdb_stage_check.py`. Logs: `logs/BLADE-01-import-bare.log` to `logs/BLADE-08-tdb-stage-upstream-MF.log`.


## sqs-benchmark

**What it is.** ArroyaveLab/sqs-benchmark at b44ba79 compares three ways of building an SQS: ATAT `mcsqs`, SCRAPS (a cuckoo-search SRO optimiser) and random assignment. The test case is equimolar BCC NbVW, a 48-atom 4x3x2 supercell, with 10 repeats per method. The drivers (`examples/tdb_gen_bcc_{mcsqs,scraps,random}.py`) generate structures and fit TDBs through BLADE plus an MLIP (ORB). `scripts/compare_methods.py` scores every `bestsqs.out` with four metrics: a re-implemented mcsqs objective, a corrdump sum of squares, the Warren-Cowley pair deviation, and the relaxed energy. Pre-computed 10-run results are in `results/`.

**Environment.** venv `/tmp/arroyave/venvs/sqs-benchmark` (Python 3.12). `uv pip install -e .` worked and pulled matplotlib, numpy, pandas, pymatgen and pycalphad. I added BLADE 9d3859c (`-e /tmp/arroyave/work/BLADE`), ase, pillow and imageio. ATAT 3.52 was on PATH, with `HOME=/tmp/arroyave/home`, and everything ran through `/tmp/sbx/clean`.

### Commands and outcomes

| # | Command (cwd = copy in `/tmp/arroyave/work/sqs-benchmark`) | Result | Wall time |
|---|---|---|---|
| 1 | `uv pip install -e .` (+ BLADE 9d3859c) | OK | 4 s |
| 2 | `python examples/tdb_gen_bcc_mcsqs.py` (unmodified) | **FAIL**: `TypeError: BladeCompositions.__init__() missing 2 required positional arguments: 'system_size' and 'allow_lower_order'` | 15 s |
| 3 | `python examples/tdb_gen_bcc_random.py` (unmodified) | **FAIL**: same TypeError | 5 s |
| 4 | `python examples/tdb_gen_bcc_scraps.py` (unmodified) | **FAIL**: `ModuleNotFoundError: No module named 'blade.tools.blade_scraps_gen'` | 3 s |
| 5 | `python scripts/run_all.py --n-runs 1 --methods mcsqs` | **FAIL**: same `BladeCompositions` TypeError, raised inside the AST-patched driver | 6 s |
| 6 | `python scripts/compare_methods.py` (unmodified) | **FAIL**: `PermissionError: [Errno 13] Permission denied: '/Users'`. `out_dir.mkdir()` runs at import time on the hard-coded author path | 4 s |
| 7 | `python scripts/sqs-benchmark-mini.py <repo> <root> 3 20`: the benchmark's NbVW structure definition through BLADE 9d3859c's `BladeSQS`, 2 mcsqs processes, plus the repo's own `_write_bestsqs` random generator (loaded from the random driver with `ast`) | mcsqs **FAIL**: `Cluster file contains no clusters.`, mcsqs exit code 1. Cause: the BLADE cutoff unit bug (pair cutoff 2.0 Å < 1NN 2.74 Å; see the BLADE section) | 30 s |
| 8 | the same with my workaround that turns the normalised shells back into Å (cutoffs 5.482 / 5.249 / 4.476 Å = 5th / 4th / 3rd NN), 20 s and then 70 s per run | corrdump OK (125 clusters), but mcsqs printed nothing past `Initializing random supercells...` (162 candidate supercells) in 20 s or 70 s, nor in 45 s of plain `mcsqs` without `-ip`. Load average was 11 on 4 vCPUs | 121 s / 182 s / 45 s |
| 9 | `python scripts/sqs-benchmark-mini.py <repo> <root> 1 200`, then `... 2 200 2` for run 2 (2 procs x 200 s each) | **PASS**: first objective after about 90 s (run 1, load average 9) and 45 s (run 2, load average 5); best -46.241737 and -46.241572; `mcsqs -best` and `objective_functions.txt` OK | 220 s + 220 s |
| 10 | `python scripts/sqs-benchmark-run_compare.py <repo>/scripts/compare_methods.py <root> 2`, which runs the repo script unchanged except for `path0`, `path2` and `n_runs` (2 mcsqs + 2 random runs) | **PASS**: all four metrics for 4 SQS; `all_runs.csv` plus `bcc_method_comparison.png` and `bcc_objective_per_run.png` written; the SCRAPS and energy panels are empty | 2-4 s |

Not run: SCRAPS, whose C++/MPI optimiser lives in a separate repo (`ichasekatz/scraps-perpair`, not provided), and the MLIP relaxation and TDB fitting, which need the newer BLADE plus the ichasekatz MaterialsFramework fork, so the energy-per-atom metric is empty.

**Outcome: PARTIAL.** The analysis script (`compare_methods.py`) runs once re-pointed and reproduces the benchmark's mcsqs-vs-random ranking on freshly made SQS. None of the three generation drivers runs against the public BLADE (they need an unreleased BLADE API, SCRAPS and the MaterialsFramework fork). Here the mcsqs SQS came from public BLADE 9d3859c plus my cutoff workaround.

### Key numbers (`data/sqs-benchmark-all_runs_mini.csv`, 48-atom equimolar NbVW)

| run | native mcsqs-scale objective | corrdump objective | WC pair deviation |
|---|---|---|---|
| mcsqs 1 (2 procs x 200 s) | **-46.241737** (script recomputes -46.241731; mcsqs reported -46.241737) | -0.01200 | -0.00027 |
| mcsqs 2 (2 procs x 200 s) | **-46.241572** (script recomputes -46.241497) | -0.00948 | -0.00010 |
| mcsqs mean ± std (n=2) | -46.24165 ± 0.00012 | -0.0107 | -0.00018 |
| Random 1 (seed 1) | -46.238911 | -0.01817 | -0.00024 |
| Random 2 (seed 2) | -46.237020 | -0.02076 | -0.00083 |
| Random mean ± std (n=2) | -46.23797 ± 0.00134 | -0.0195 | -0.00054 |

Published 10-run means: mcsqs -46.2424 ± 0.0003 (20 procs x 100 s), Random -46.2367 ± 0.0009; corrdump means -0.0105 (mcsqs) and -0.0270 (random); WC -0.0002 (mcsqs) and -0.0016 (random). The ordering reproduces: mcsqs beats random on the native and corrdump objectives, and on mean WC. Our mcsqs corrdump (-0.0107) and WC (-0.00018) means match the published mcsqs values. Our native mcsqs mean (-46.2417, 2 procs on a loaded runner) is 0.0007 short of the published mean, which used 20 procs. The script's re-implemented objective matches the value mcsqs reports to within 8e-5 (6e-6 for run 1), which cross-checks its metric code. Figures: `figures/sqs-benchmark-mini-bcc_method_comparison.png` and `figures/sqs-benchmark-mini-bcc_objective_per_run.png` (the title hard-codes "ORB MLIP" though no MLIP ran). The mcsqs objective traces are in `data/sqs-benchmark-mcsqs_run{1,2}_objective_history.tsv`.

### Problems found (exact messages)
1. **Written against an unreleased BLADE API.** The drivers call `BladeCompositions` without `system_size`/`allow_lower_order`, pass `BladeSQS(..., sqsgen_in=, fixed_compositions=)`, call `sqs_gen(...)` without `iter`, put `"cutoff_mode": "nn"` in `mcsqs_params` but leave out `"use_time"` (9d3859c reads `params["use_time"]`), pass `BladeTDBGen(phases_dict=, output_dir=, terms_in=, tdb_params={... "calculator": "orb"})`, and import `blade.tools.blade_scraps_gen.ScrapsSQSGen`. None of these exist in ArroyaveLab/BLADE 9d3859c. pyproject does not list BLADE, MaterialsFramework or SCRAPS, so the README's install steps cannot be reproduced from public code.
2. **Hard-coded author paths with a side effect at import.** `compare_methods.py` sets `path0 = Path("/Users/<author>/Desktop/School/Research")` and calls `out_dir.mkdir(parents=True, exist_ok=True)` at module level, which gives `PermissionError: [Errno 13] Permission denied: '/Users'`. `results/all_runs.csv` also stores absolute `/Users/...` paths.
3. **corrdump cutoff disagrees with the mcsqs cutoff.** The script runs corrdump with `-3=5.18` and its comment says "4NN≈5.18". For BCC with a = 3.165 Å, though, 4NN = a·√11/2 = 5.249 Å, which is the triplet cutoff the mcsqs driver requests (`"3": 4`). Against a reference `clusters.out` made at the 4NN cutoff, every structure printed `warning: clusters=125 diffs=88 ... using 88`. Here the truncation barely mattered (recomputed vs reported objective differ by 6e-6 and 7.5e-5), but the corrdump objective leaves out the 5.25 Å triplets that mcsqs optimised.
4. **`find_bestsqs()` can pick up the template that `sqs2tdb -mk` writes** (a `bestsqs.out` whose sites read `a_A,a_B,a_C`) when mcsqs has not finished. corrdump then fails with `Unknown atom label: a_A,a_B,a_C` / `Unexpected vacancy` (`logs/sqs-benchmark-05-compare-mini.log`). The row quietly becomes None instead of being reported as "missing SQS".
5. **Cost.** On this shared runner (load average 5-11), a 48-atom ternary BCC mcsqs with cutoffs out to 5NN pairs, 4NN triplets and 3NN quadruplets needed 45-90 s just to initialise its 162 candidate supercells before printing an objective. With BLADE's defaults, runs shorter than about 90 s give no SQS at all on comparable hardware, and nothing warns about it.

Scripts: `scripts/sqs-benchmark-mini.py` (mcsqs through BladeSQS with the cutoff workaround, `SQSB_NO_CUTOFF_FIX=1` to disable; random baseline from the repo's own generator) and `scripts/sqs-benchmark-run_compare.py`. Logs: `logs/sqs-benchmark-01-install.log` to `logs/sqs-benchmark-09-compare-2mcsqs-2random.log`.


## PAIPAI

**What it is.** PAIPAI ("Package for Alloy Interstitial Predictions using Artificial Intelligence", ArroyaveLab/PAIPAI at 00ff18b) searches for low-energy arrangements of a multi-element metal lattice with interstitials. A C++17 master, `mc_paipai`, runs Metropolis Monte Carlo: it proposes metal swaps and interstitial moves or exchanges. Python workers score the proposals with an MLIP: "fast" workers do a coarse relaxation (FIRE, fmax 0.1 eV/Å, 30 steps) into a capped waiting pool, and "slow" workers refine the best candidates (fmax 0.01, 400 steps) and report back. Workers and master talk through files (`fast/.go_k`, `waiting_pool/`, `reports/`). A bash launcher, `paipai`, starts everything. The MLIP is MaterialsFramework's `GraceCalculator`, default `GRACE-2L-OMAT`. The shipped example (`example/struc.in`) is 5x5x5 BCC NbTaTiHf (250 metal atoms, 375 octahedral sites) with B2 O2.

**Environment.** g++ 13.3, CMake 3.31. venv `/tmp/arroyave/venvs/paipai` (Python 3.12) with upstream ArroyaveLab MaterialsFramework 0ec8168 `[grace]` (tensorpotential 0.6.2.1, TF 2.19.1 on CPU), pymatgen and pycalphad. The shared mlip venv did not exist yet. All runs went through `/tmp/sbx/clean` with `HOME=/tmp/arroyave/work/PAIPAI_home` (where the GRACE model is cached), `OMP_NUM_THREADS=1` and `TF_NUM_INTRAOP_THREADS=1`/`TF_NUM_INTEROP_THREADS=1`.

### Commands and outcomes

| # | Command | Result | Wall time |
|---|---|---|---|
| 0 | README verbatim: `mkdir build && cd build && cmake -DCMAKE_INSTALL_PREFIX=$HOME` | **FAIL**: `CMake Error: The source directory ".../build" does not appear to contain CMakeLists.txt.` The README leaves out `..` | <1 s |
| 1 | `cmake .. -DCMAKE_INSTALL_PREFIX=<prefix> && cmake --build . -j2 --target install` | **PASS**: installs `mc_paipai`, `paipai`, `fast_worker.py` and `slow_worker.py`; only 2 `-Wunused-result` warnings (`system()` in unused `calculateEnergyORB`/`relaxedEnergyORB`) | 8 s |
| 2 | `timeout 8 mc_paipai example/struc.in --workers 2 --steps 1` (master alone) | **PASS** (C++ side): reads 250 metal atoms, 375 interstitial sites and B2 O2, shuffles, writes `fast/POSCAR1..2` (254 atoms), `SAVE1..2` and `.go_1..2`, then waits for workers until killed | 8 s |
| 3 | `uv pip install "MaterialsFramework[grace]" "tensorflow<2.20" "tf-keras<2.20" pymatgen` | OK, but tensorpotential requires `tensorflow[and-cuda]<=2.20` on Linux, which pulled in 12 `nvidia-*-cu12` wheels. I uninstalled them, so the venv is CPU-only | 18 s |
| 4 | `python scripts/PAIPAI-check_worker_calc.py` (builds each worker's calculator exactly as written) | **FAIL**: `GraceCalculator(model=..., device="cpu", verbose=True, fmax=..., max_steps=...)` raises `TypeError: object.__init__() takes exactly one argument (the instance to initialize)`. Upstream MaterialsFramework has neither `device` nor `max_steps` (it has `steps`) | 3 s |
| 5 | Rebuild with `-DPython3_EXECUTABLE=/tmp/arroyave/venvs/paipai/bin/python` | needed: by default CMake bakes `/usr/bin/python3.12` into `bin/paipai`, and that interpreter fails with `ModuleNotFoundError: No module named 'pymatgen'` | 5 s |
| 6 | `timeout 40 paipai --input small_struc.in --fast 1 --slow 1 --steps 3` (no shim) | **HANG**: both workers die at start-up with the TypeError in #4; `mc_paipai` keeps polling `reports/` with nothing to say so; `mc.log` stays empty; killed by `timeout` (exit 124) | 42 s |
| 7 | `PYTHONPATH=scripts/PAIPAI-shim timeout 420 paipai --input small_struc.in --model GRACE-2L-OMAT --device cpu --fast 1 --slow 1 --steps 3 --temp 0.001 --pool-cap 8` | **PASS**: the whole loop runs, with the GRACE-2L-OMAT model downloaded (92.7 MB), 9 fast screens, 5 slow refinements, 3 MC steps (1 rejected, 2 accepted), and `# Finished. MC steps = 3, accepted = 2` | 65 s |

`scripts/PAIPAI-shim/sitecustomize.py` is my 20-line compatibility layer. It subclasses `GraceCalculator` to drop `device` and map `max_steps` to `steps`, and changes nothing else. `small_struc.in` comes from `scripts/PAIPAI-make_small_struc.py` and uses the same layout as the example at 2x2x2: 16 BCC metal sites (Nb8 Ta4 Ti2 Hf2, a = 3.3 Å), 24 octahedral sites, B1 O1, so 18 atoms. I skipped the shipped 254-atom example with the default 15 fast + 15 slow workers and 2000 steps; that is far beyond a shared 4-vCPU runner.

**Outcome: PARTIAL.** The C++ master builds and runs, and the full master-worker MC loop works end to end on CPU. The Python workers, however, do not run against the public ArroyaveLab MaterialsFramework without my two-keyword shim, and with the default CMake configuration they would run under the wrong interpreter. Both failures leave the master hanging silently.

### Key numbers (run 7; `data/PAIPAI-mc_small.log`, `data/PAIPAI-refined_candidates_small.csv`)
- Initial state after refinement: E = -178.18947 eV (18 atoms). Step 1: -177.86866, rejected. Step 2: -178.26369, accepted. Step 3: -178.43102 eV, accepted, a drop of 0.24 eV (13 meV/atom) from the start.
- Fast screen takes 3.3-7.8 s per candidate (18.8 s for the first, which includes the model download/load and TF graph build). Slow refine takes 5.1-19.4 s (fmax 0.01). FIRE steps take about 0.07-0.25 s each for 18 atoms on 1 thread.
- The relaxed cell (`data/PAIPAI-final_CONTCAR_small`) grew from 6.60 to 6.96 Å (`relax_cell=True`).
- Cost at the shipped example size (`scripts/PAIPAI-time_example_size.py`, `logs/PAIPAI-08-time-example-size.log`): on a 254-atom candidate that `mc_paipai` generated from `example/struc.in`, GRACE-2L-OMAT needs about 1.9 s per force call on 1 TF thread (load average 11), plus 11 s to load the model and 16 s to build the graph on the first call. One slow refinement (up to 400 FIRE steps) can therefore take up to about 13 min per thread. The default 2000 MC steps imply about 2000 refinements, roughly 100-400 CPU-hours before fast screens. That is presumably why the defaults use 15 + 15 workers and offer `--device cuda`.

### Problems found (exact messages)
1. **Worker and MaterialsFramework API mismatch.** `fast_worker.py`/`slow_worker.py` call `GraceCalculator(model=, device=, verbose=, fmax=, max_steps=)` and later set `calc.max_steps`. With ArroyaveLab MaterialsFramework 0ec8168 this gives `TypeError: object.__init__() takes exactly one argument (the instance to initialize)`. Even if the call were accepted, `max_steps` would be ignored and the default `steps=1000` used. PAIPAI does not say which MaterialsFramework version it targets.
2. **Silent hang when the workers die.** The bash launcher backgrounds the workers and never checks them; `mc_paipai` loops on `reports/` with no timeout. A worker crash (#1, a missing Python package, or the wrong interpreter) looks like a run that never progresses. `mc.log` is not flushed, so it stays empty.
3. **Interpreter chosen at build time.** `paipai.in` hard-codes `PYTHON="@Python3_EXECUTABLE@"`. CMake picks the system `python3` unless you pass `-DPython3_EXECUTABLE=`, and the README does not mention this or list the Python dependencies (pymatgen, materialsframework, tensorpotential/TensorFlow).
4. **README build steps are wrong.** `cmake -DCMAKE_INSTALL_PREFIX=$HOME` has no source dir and fails. The README also points at `/examples/` but the folder is `example/`.
5. `paipai --root DIR` is passed to the workers, but `mc_paipai` always uses `fs::path ROOT = "."`. If `--root` differs from the cwd, the master and workers watch different directories. Not exercised.
6. tensorpotential 0.6.2.1 requires `tensorflow[and-cuda]` on Linux, so a CPU-only install has to remove the 12 CUDA wheels by hand. The GRACE-2L-OMAT weights are under an "Academic Software License" (printed when they load), which matters for anything beyond academic use.

Scripts: `scripts/PAIPAI-shim/sitecustomize.py`, `scripts/PAIPAI-make_small_struc.py`, `scripts/PAIPAI-check_worker_calc.py`, `scripts/PAIPAI-time_example_size.py`. Logs: `logs/PAIPAI-00-build-readme-verbatim.log` to `logs/PAIPAI-08-time-example-size.log`, plus the worker logs `logs/PAIPAI-06-worker-*.log`. Data: `data/PAIPAI-small_struc.in`, `data/PAIPAI-mc_small.log`, `data/PAIPAI-refined_candidates_small.csv`, `data/PAIPAI-final_CONTCAR_small`.


## Summary

| repo | install | tests/examples run | outcome | notes |
|---|---|---|---|---|
| ATAT 3.52 (dependency) | Official tarball. `make -j2` + `make install`, 34 s. Needs tcsh. | Binaries used by PhaseForge, BLADE, sqs-benchmark | PASS (build) | CC BY-ND 4.0. `runstruct_vasp -nr` writes an empty POSCAR (awk syntax error in tmp.awk:27); the first call only creates `~/.ezvasp.rc`. `sqs2tdb -cp` gives a dash `"&" unexpected` error. 1 mcsqs process gives no `bestsqs.out`. |
| PhaseForge | CMake builds `ternary_search`. `make install` FAILS without the LAMMPS submodule (`ML-GNNP` missing). Needs csh. | `sqscal -e Cu,Ni -l FCC_A1 -lv 1 -mlip Grace` exits 0 with no energies and an empty TDB. Step-by-step equivalent with the same SQS and GRACE-2L-OMAT works (23 s). | PARTIAL | ΔH_mix(Cu0.5Ni0.5) = +2.18 kJ/mol, so L0(FCC) = +8.72 kJ/mol (SGTE: 6877 + 4.6T). FCC gap top 520 K vs 600 K (SGTE). With SGTE liquid: solidus/liquidus +120–148 K and a spurious ~1756 K maximum near x(Ni) 0.8. LIQUID MD, -vib, Al–Cu and Al–Si not run. sqscal never checks errors. |
| PhaseForgePlus | PASS via `uv sync --frozen` (py3.11, ESPEI cjkunselman18@4888897, 6 s). FAIL via README `pip install` (PyPI espei 0.9.1 → TypeError in objective). | pytest 18/18 pass (6 FIXME tests, including all optimizer tests, disabled). Pt–W example capped at 560 s. Cu–Ni and Al–Cu ORCHID ZPF tunes. | PARTIAL | Pt–W −logL 6628 → 2005, still falling. SGTE Cu–Ni/Al–Cu already fit ORCHID, so the tune is a no-op. MLIP regularizer still silently empty (3 bugs). ESPEI branch mutates the caller's Database. |
| MaterialsFramework | venv py3.12 (`>=3.12,<3.13`), `[grace]` CPU; CUDA wheels removed by hand | pytest 379 passed / 71 skipped / 0 failed (10.5 s). GRACE-2L-OMAT EOS of fcc Al/Cu/Ni. | PASS | Al a0 4.038 Å, B 78.5 GPa (exp 4.05 / 76). Cu 3.611 Å, 144.5 GPa (exp 3.615 / 140). GRACE weights are academic-only. Elastic constants not run. |
| BLADE | py3.12 `pip install -e .` OK, but dependencies are undeclared (8 added by hand) | ex01 PASS. ex02/ex03 FAIL as shipped (stale kwargs). Shrunk ex02 (Cr–Hf diboride, 24 atoms, ATAT mcsqs) PASS. TDB stage FAIL. | PARTIAL | mcsqs cutoffs are normalised shell ratios used as absolute lengths. The MLIP/TDB stage needs the ichasekatz MaterialsFramework fork and hard-codes CUDA. |
| sqs-benchmark | py3.12 `pip install -e .` OK (+ public BLADE) | 3 generator drivers FAIL (unreleased BLADE API, SCRAPS not public). `compare_methods` PASS after removing a hard-coded `/Users` path. | PARTIAL | NbVW 48-atom: mcsqs −46.24165 ± 0.00012 vs random −46.23797. Published ranking reproduced. |
| PAIPAI | CMake build OK in 8 s (README cmake line broken; needs `-DPython3_EXECUTABLE`). GRACE venv. | `mc_paipai` PASS. Full MC loop (18-atom NbTaTiHf+B+O, 3 steps) PASS only with a kwargs shim; as shipped the workers crash and the master hangs. | PARTIAL | E −178.19 → −178.43 eV, 65 s. The shipped 254-atom example costs ~1.9 s per force call per thread, i.e. ~100–400 CPU-h at default settings. |

**Files:** `logs/` (trimmed logs, all < 200 KB), `figures/` (PNGs < 1 MB), `data/` (TDBs, JSON, CSV generated here), `scripts/` (driver scripts and shims), `sections/` (per-repo source sections of this report).
