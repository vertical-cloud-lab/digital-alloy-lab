# Issue #235: PhaseForge / MLIP stack (ArroyaveLab): install and test runs

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

