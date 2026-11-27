# Arroyave group and ORCHID tools: installs, test runs and comparisons (#235)

Issue #235 asked us to "exhaustively try to install and run test runs for each of the repositories" in
[ArroyaveLab](https://github.com/ArroyaveLab) and [orchid-calphad](https://github.com/orchid-calphad). It named four
in particular: orchid-data and orchid-examples, eagar-tsai (compared with our Thermo-Calc AM-module results), and
PhaseForge / PhaseForgePlus. It also asked for comparisons of pycalphad and open databases with Thermo-Calc for Al
and Cu.

On 2026-11-05 the two orgs had **34 public repos**: 29 in ArroyaveLab and 5 in orchid-calphad. All 34 were cloned at
their default-branch heads (commits are listed in each group's report) and installed, and each got at least one test
or example run.

**How the runs were made.**
- Everything ran on a GitHub Actions runner with 4 vCPUs, 15 GB of RAM, no GPU and no Thermo-Calc licence. It was
  shared by five parallel agents, so timings are only indicative.
- Each repo got its own uv venv, with CPU-only PyTorch.
- Every third-party install and script ran with the job's secrets stripped from its environment (`/tmp/sbx/clean` in
  the logs).
- Runs were scaled down where needed (fewer BO iterations, smaller cells, shorter fits); each report says what changed.
- In the logged commands, `/tmp/arroyave/src` is the clones, `/tmp/arroyave/work` the working copies,
  `/tmp/arroyave/venvs` the venvs and `/tmp/arroyave/results/<group>` the folder here.
- No upstream issues or PRs were filed.

## What to take away

1. **eagar-tsai and the Thermo-Calc AM module**, in [`eagar-tsai/`](eagar-tsai/).
   - 101 of 102 tests pass; the 3D plot test needs OpenGL.
   - **Against our in-house AM-module maps** (Thermo-Calc's runs for us, stock AlSi10Mg and the BYU blend, on the
     `consolidation-2` branch), with the same beam, layer, hatch and preheat, and the absorptivity read off the AM
     module's own melt-pool renders (0.31 and 0.38):
     - **Lack of fusion: good agreement.** The AM module's own D/t and Dh/t tests, applied to eagar-tsai's pools,
       give the same class at 37 of 43 AlSi10Mg points. eagar-tsai's hatch-overlap line sits within 20 W of the AM
       module's from 800 to 2100 mm/s. The blend fits best with the pool edge at the liquidus: 20 of 22 points.
     - **Keyholing: no agreement.** The AM module calls keyholes at 2–4× the power at which eagar-tsai's pools reach
       W/D = 2.5 or Al's boiling point. eagar-tsai's default classifier calls 55 of 58 AlSi10Mg points keyhole,
       including all 31 the AM module calls defect-free.
     - **Keyhole-mode pools are out of reach.** The AM module's 375 W / 400 mm/s pool is 349 µm deep and 1.47 mm long;
       eagar-tsai reaches neither at any absorptivity up to 1.
     - So eagar-tsai can stand in for the AM module on the lack-of-fusion side of a map, but not for keyholing.
     - **Time-dependent melt-pool renders.** eagar-tsai's integral over past heat input, cut off at the time the beam has
       been on, gives the start-up and cool-down of a track. Drawn like the AM module's 3D renders, at the same settings
       and colour scales, its pool is a smooth half-ellipsoid with no keyhole or flow. It reaches steady width and depth
       within 0.3–0.45 mm of track and freezes 0.12–0.33 ms after the beam switches off
       ([renders and animations](eagar-tsai/README.md#time-dependent-melt-pools-drawn-like-the-am-modules-renders)).
   - eagar-tsai was also checked against what a printability map is meant to predict: measured AlSi10Mg single tracks
     ([arXiv:2507.23422](https://arxiv.org/abs/2507.23422)), using that study's calibrated absorptivity.
   - With its default criteria, only 9 of 420 points come out defect-free. It flags keyholing at 78 points where the
     measured tracks weren't keyholes, and its pools never get deeper than D/W = 0.48, against the 0.75 the study
     used to call a keyhole. It also calls lack of fusion at 92 points where the tracks were continuous.
   - A Si-enriched AlSi10Mg moves its pool by about 2 µm.
   - It is usable for Al only after refitting its thresholds to our own cross-sections, much as the AM module's own
     AlSi10Mg example needed its absorptivity scaled by 1.8.
   - `scripts/eagar_tsai_vs_am_module_inhouse.py` reruns the AM-module comparison in 23 s, and
     `scripts/eagar_tsai_vs_am_module.py private` takes an AM-module CSV export if Thermo-Calc can send one. The
     Linux-wheel and unit problems
     from Xavier's sweep are in
     [`../edison-trajectories/eagar-tsai-alsi10mg-inputs/sobol-check/`](../edison-trajectories/eagar-tsai-alsi10mg-inputs/sobol-check/).
2. **pycalphad with open databases compared with published Thermo-Calc numbers**, in [`pycalphad-al-cu/`](pycalphad-al-cu/).
   - **Where they agree:**
     - MatCalc's open mc_al reproduces published TCAL7 Al–12Si values (liquidus, eutectic, Scheil range) to within 1 K.
     - It matches TCAL6 AlSi10Mg phase fractions to within 0.0002.
     - The SGTE binaries match ORCHID's experimental invariants for Al–Cu, Cu–Al, Cu–Cr, Cu–Zr and Cu–Sn to within
       ±8 K (one Cu–Sn dataset is off by 12 K).
   - **Stock vs Si-enriched AlSi10Mg:** going from 10 to 12 % Si halves the Scheil freezing range (36 → 21.5 K) and
     raises the eutectic fraction from 0.77 to 0.95.
   - **Where the open databases fail:**
     - mc_al gets Al–Zr wrong: a 656.6 °C eutectic with no primary Al₃Zr. Use the SGTE peritectic datasets instead,
       which agree with TCAL7 and experiment (660.6–660.9 vs 660.85 °C).
     - The open Cu database misses the C63000 bronze liquidus by +70 K.
   - **Published Thermo-Calc numbers are scarce:** none were found for the AlSi10Mg liquidus/solidus, nickel-aluminium
     bronze, or Cu–Ni. That is exactly where our own Thermo-Calc runs would add the most. There are no in-house
     Thermo-Calc equilibrium or Scheil numbers in the repo yet; the in-house results are the AM-module maps above.
3. **ORCHID**, in [`orchid/`](orchid/).
   - Every repo installs and its shipped tests pass. Every headline number re-run reproduced; for example, the SGTE
     Cu–Zr one-shot recall came out at 0.722/0.728 against the README's 0.72/0.73.
   - The MCP server answered all 41 tool calls offline.
   - **For our systems the data are thin:**
     - Al–Si: 13 values, none accepted.
     - Al–Cu: 4 papers.
     - Cu–Ni: no accepted invariants.
     - Nickel-aluminium bronze and Al–Mn–Cr–Zr: nothing.
     - Al–Zr is the best-covered Al system.
   - The one-shot scorer is hard-wired to Cu–Zr.
   - Its 2,788 open TDBs (the SGTE binary collection under CC BY 4.0, plus MatCalc mc_al/mc_fe/mc_ni) are the most
     useful part for us.
4. **PhaseForge / PhaseForgePlus**, in [`phaseforge/`](phaseforge/).
   - **PhaseForge:** `sqscal -e Cu,Ni -l FCC_A1 -lv 1 -mlip Grace` exits 0 but writes an empty TDB, because it never
     checks for errors.
     - Running its steps by hand (with a shim for ATAT's broken `runstruct_vasp -nr`) gives a real TDB:
       L0(FCC, Cu–Ni) = +8.72 kJ/mol with GRACE-2L-OMAT in about 30 s. The same workaround did nothing in a fresh
       Al–Cu directory, and why is unexplained.
     - Against SGTE:
       - GRACE's Cu–Ni mixing enthalpy is 27 % high (+2.18 vs +1.72 kJ/mol at x = 0.5).
       - The miscibility-gap top is 520 K vs 600 K.
       - With the SGTE liquid, solidus and liquidus come out up to 148 K too high.
       - The Al–Cu FCC L0 is −45.3 vs −53.5 kJ/mol.
     - The liquid (MLIP molecular dynamics) wasn't run; that is the part that costs CPU-hours.
   - **PhaseForgePlus:** installs only through `uv sync --frozen`; the README's `pip install` fails with PyPI ESPEI.
     All 18 tests pass, but every optimizer test is disabled. The MLIP regularizer is silently empty.
   - **MaterialsFramework:** 379 tests pass. GRACE-2L-OMAT gives a = 4.038 Å and B = 78.5 GPa for Al (experiment
     4.05 Å, 76 GPa), and a = 3.611 Å and B = 144.5 GPa for Cu (3.615 Å, 140 GPa). The GRACE weights are licensed for
     academic, non-commercial use only.
5. **Bayesian optimization**, in [`bo/`](bo/).
   - The closest fits for our BOFN work are:
     - `2026-islam-rhea-mobo`'s supply-risk-weighted EHVI: 24/24 tests pass, and it's a small BoTorch wrapper.
     - `SupplyRiskAwareDesign`, the supply-risk paper our proposal cites. It doesn't install as shipped; rebuilt, it
       runs.
     - `PCMOBO`'s constrained multi-objective BO with policy switching.
     - The idea behind `BAREFOOT-Framework`'s multi-fidelity + batch BO. The code itself is legacy and swallows
       errors.
   - Upstream bugs worth reporting:
     - Alloy-Color-Optimization's EHVI price objective has its sign flipped; a two-line fix raises the hypervolume
       from 0.595 to 0.816.
     - HTMDEC raises `NameError` after iteration 1.
     - BRAVE's `priors.py` uses the wrong column names.
     - SupplyRiskAwareDesign is missing `src/`.
6. **Other repos**, in [`misc/`](misc/).
   - `microseg_lab`'s classical dark-void path works as an LPBF porosity segmenter, at about 40 s per 512² image on CPU.
   - The `CALPHAD` TC-Python drivers would port to pycalphad in about 0.5 day for equilibrium and 1–2 days for Scheil.
   - `HEACalculator` (585 tests) and the Hall–Petch repo (19/19 tests, headline result reproduced exactly) are solid.

## All 34 repos

Outcome codes:
- **PASS**: installs, and the smallest meaningful test or example runs (possibly after the documented pins or small
  patches).
- **PARTIAL**: some entry points run; others fail or need inputs we don't have.
- **NOT RUNNABLE**: needs a licence, an API key or HPC.

| Repo | What it is | Outcome | Key result or main problem | Report |
|---|---|---|---|---|
| [orchid-examples](https://github.com/orchid-calphad/orchid-examples) | runnable ORCHID workflows (PhaseForge+, ESPEI, one-shot MLIP diagrams) | PASS (CI tolerance) | all five quick paths regenerate. The strict sha256 check fails only on PNG bytes and one stale CRLF hash. Headlines reproduced: SGTE 0.722/0.728, GRACE 0.426/0.410, tuned 9/13 | [orchid](orchid/README.md) |
| [orchid-mcp](https://github.com/orchid-calphad/orchid-mcp) | MCP server for ORCHID data | PASS | 52/52 tests; 41 offline tool calls for Al–Cu/Si/Mg/Zr and Cu–Ni, identical on both back ends | [orchid](orchid/README.md) |
| [orchid-data](https://github.com/orchid-calphad/orchid-data) | ORCHID v2026.10 data (CC BY 4.0) | PASS | all shipped checks and 20 tests pass. DATASET_CARD counts are stale (72,359 vs 66,551 accepted). Al/Cu coverage in `orchid/data/al-cu-coverage.csv` | [orchid](orchid/README.md) |
| [orchid-bench](https://github.com/orchid-calphad/orchid-bench) | benchmark for extracting thermodynamic data from documents | PARTIAL | scorer, oracle and results reproduce exactly. The OCR route needs Tesseract; the AI/raster/Camelot routes need a private pipeline. No dependency file | [orchid](orchid/README.md) |
| [orchid-project.org](https://github.com/orchid-calphad/orchid-project.org) | website, build tools, open TDB bundle | PASS (tests) / PARTIAL (builds) | 46/46 test files pass with sibling checkouts. Several generated files are stale, and 5 builders need unpublished inputs | [orchid](orchid/README.md) |
| [eagar-tsai](https://github.com/ArroyaveLab/eagar-tsai) | Eagar–Tsai melt-pool model and printability maps | PASS | 101/102 tests (the 3D plot test needs OpenGL). Against our in-house AM-module maps: lack-of-fusion classes agree at 37 of 43 AlSi10Mg points, but its W/D ≤ 2.5 test calls 55 of 58 points keyhole where the AM module calls 15. Against measured AlSi10Mg tracks, its default criteria leave 9 of 420 points defect-free | [eagar-tsai](eagar-tsai/README.md) |
| [PhaseForge](https://github.com/ArroyaveLab/PhaseForge) | MLIP → SQS → CALPHAD TDB (with ATAT) | PARTIAL | `sqscal` writes an empty TDB but exits 0. Its steps run by hand give a Cu–Ni TDB with GRACE: L0 +8.72 kJ/mol (ΔH 27 % above SGTE), gap top 520 K vs SGTE 600 K. Not reproducible in a fresh Al–Cu directory. `make install` needs the LAMMPS submodule | [phaseforge](phaseforge/README.md) |
| [PhaseForgePlus](https://github.com/ArroyaveLab/PhaseForgePlus) | gradient tuning of CALPHAD models against ZPF data | PARTIAL | `uv sync --frozen` works; README `pip install` fails (PyPI ESPEI). 18/18 tests, optimizer tests disabled. Pt–W −logL 6628 → 2005 in 560 s. MLIP regularizer silently empty | [phaseforge](phaseforge/README.md) |
| [MaterialsFramework](https://github.com/ArroyaveLab/MaterialsFramework) | MLIP framework (GRACE, MACE, CHGNet, ORB, …) | PASS | 379 passed, 71 skipped. GRACE-2L-OMAT Al 4.038 Å / 78.5 GPa, Cu 3.611 Å / 144.5 GPa | [phaseforge](phaseforge/README.md) |
| [BLADE](https://github.com/ArroyaveLab/BLADE) | SQS + ML relaxation + TDB pipeline (borides) | PARTIAL | dependencies undeclared. ex01 passes; ex02/ex03 fail on stale kwargs, and a shrunk ex02 passes. The TDB stage needs a MaterialsFramework fork and hard-codes CUDA | [phaseforge](phaseforge/README.md) |
| [sqs-benchmark](https://github.com/ArroyaveLab/sqs-benchmark) | mcsqs vs SCRAPS vs random SQS | PARTIAL | generator drivers need an unreleased BLADE API and SCRAPS. `compare_methods` reproduces the published ranking after removing a hard-coded path | [phaseforge](phaseforge/README.md) |
| [PAIPAI](https://github.com/ArroyaveLab/PAIPAI) | Monte Carlo + MLIP for interstitials | PARTIAL | builds in 8 s. The full MC loop runs only with a kwargs shim; as shipped the workers crash and the master hangs. The shipped example would take 100–400 CPU-h | [phaseforge](phaseforge/README.md) |
| [tamubo](https://github.com/ArroyaveLab/tamubo) | TAMU BO tools | PARTIAL | exact-EI finds the best point but is 150–500× slower than BoTorch. The shipped exactbo config ran past 10 min on CPU | [bo](bo/README.md) |
| [BAREFOOT-Framework](https://github.com/ArroyaveLab/BAREFOOT-Framework) | multi-fidelity (reification) + batch BO | PASS (one node) | needs numpy < 1.24 and a SciPy patch. Fusion reached 4.50 after 32 truth evaluations vs 4.28 after 52 for batch only. Errors are logged but it exits 0. The SLURM demo can't run here | [bo](bo/README.md) |
| [PCMOBO](https://github.com/ArroyaveLab/PCMOBO) | constrained MOBO with policy switching | PASS | HEA pool: probability-of-feasibility 12/14 and bandit 8/8 feasible vs pEHVI 0/0. The LLM policy needs an OpenAI key | [bo](bo/README.md) |
| [SupplyRiskAwareDesign](https://github.com/ArroyaveLab/SupplyRiskAwareDesign) | supply-risk-aware alloy design | PARTIAL | `src/` missing, so it doesn't install as shipped. Rebuilt, its Pareto set has lower supply risk (mean SR 50.7 vs 52.9) | [bo](bo/README.md) |
| [2026-islam-rhea-mobo](https://github.com/ArroyaveLab/2026-islam-rhea-mobo) | MOBO for refractory HEAs | PASS | 24/24 tests. Supply-risk-weighted EHVI. The production loop needs TC-Python; `uv sync` pulls CUDA | [bo](bo/README.md) |
| [DGP-BO](https://github.com/ArroyaveLab/DGP-BO) | deep-GP BO for HEAs | PASS (CPU patch) | CUDA-only as shipped. Deep-GP beat cGP and MTGP in one seeded run. Breaks on gpytorch ≥ 1.12 | [bo](bo/README.md) |
| [Kernels-BO](https://github.com/ArroyaveLab/Kernels-BO) | BO over GP-kernel space | PARTIAL | kernel distances reproduce (r = 0.9999). The main notebook needs the OpenAI API, and its LPBF data isn't shipped | [bo](bo/README.md) |
| [constraint-satisfaction](https://github.com/ArroyaveLab/constraint-satisfaction) | constraint-aware BO | PASS | with priors it finds 13/24 feasible alloys vs 0 for random and pEHVI. The logged hypervolume ignores feasibility | [bo](bo/README.md) |
| [BRAVE](https://github.com/ArroyaveLab/BRAVE) | campaign-2 code and data | PARTIAL | three fixes needed (wrong column names in `priors.py`). Per-iteration inputs aren't public | [bo](bo/README.md) |
| [HTMDEC](https://github.com/ArroyaveLab/HTMDEC) | high-throughput discovery codebase | PARTIAL | the BO driver raises `NameError` after iteration 1. MATLAB parts can't run here | [bo](bo/README.md) |
| [NiTi-alloy-discovery](https://github.com/ArroyaveLab/NiTi-alloy-discovery) | NiTi BO campaign | PASS | rerunning Iter3 reproduces the shipped picks. The 479 MB is three copies of one 122 MB file | [bo](bo/README.md) |
| [Alloy-Color-Optimization](https://github.com/ArroyaveLab/Alloy-Color-Optimization) | preference-based BO for jewellery alloys | PASS (BO) | the EHVI price objective has its sign flipped; a two-line fix raises HV from 0.595 to 0.816 | [bo](bo/README.md) |
| [Initialization](https://github.com/ArroyaveLab/Initialization) | BO initialization datasets and tools | PARTIAL | the driver reproduces the first-batch result. The script has a NameError ordering bug | [bo](bo/README.md) |
| [CatBoost-SMAs](https://github.com/ArroyaveLab/CatBoost-SMAs) | CatBoost for shape-memory alloys | PASS | test R² 0.936. Needs pandas < 2 | [bo](bo/README.md) |
| [CALPHAD](https://github.com/ArroyaveLab/CALPHAD) | TC-Python drivers with parallelisation | PARTIAL | needs a Thermo-Calc licence. The plotter, generator and a mock-TC run work; a pycalphad Al–Si port sketch gives 577 °C / 597 °C | [misc](misc/README.md) |
| [HEACalculator](https://github.com/ArroyaveLab/HEACalculator) | HEA solid-solution parameters | PASS | 585 tests; hand check exact. HEA rules misclassify dilute Al and Cu alloys | [misc](misc/README.md) |
| [akaitools](https://github.com/ArroyaveLab/akaitools) | AkaiKKR output parser | PASS | 447 tests; parses and plots the bundled NiFe outputs | [misc](misc/README.md) |
| [microseg_lab](https://github.com/ArroyaveLab/microseg_lab) | classical + SAM2 microscopy segmentation | PASS (headless) | classical dark-void path ~40 s per 512² image; SAM2-tiny on CPU 92 s. Needs SAM2 installed even for the classical path | [misc](misc/README.md) |
| [CGA_Subgraph_Analysis](https://github.com/ArroyaveLab/CGA_Subgraph_Analysis) | graph screening of graded-alloy paths | PASS | notebook ran unmodified in 72 s; the Kou hot-cracking filter idea carries over | [misc](misc/README.md) |
| [2026-mulukutla-hall-petch](https://github.com/ArroyaveLab/2026-mulukutla-hall-petch) | Hall–Petch in FCC MPEAs (paper repo) | PASS (main analysis) | 19/19 tests; M15 Q² 0.731/0.694/0.694 reproduced exactly. `make verify` fails on a fresh checkout | [misc](misc/README.md) |
| [Phase-Compatibility-Model-NiTi](https://github.com/ArroyaveLab/Phase-Compatibility-Model-NiTi) | NiTi phase-compatibility model | PARTIAL | the HEACalculator 1.x API it calls no longer exists; with a one-cell shim the predictions reproduce | [misc](misc/README.md) |
| [Transformation-Strain-Model-NiTi](https://github.com/ArroyaveLab/Transformation-Strain-Model-NiTi) | NiTi transformation strain + CatBoost | PASS (pinned) | fails on current numpy/pandas/catboost. Pinned, 8/10 cells are identical and CV R² is 0.954 | [misc](misc/README.md) |

The [earlier session](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/235#issuecomment-6637612112)
counted 30 ArroyaveLab repos. On 2026-11-05 the org lists 29 public ones.

## Folder layout

| Folder | Contents |
|---|---|
| [`eagar-tsai/`](eagar-tsai/) | eagar-tsai tests, its printability map vs measured AlSi10Mg tracks, the isotherm sweep. Script: [`../scripts/eagar_tsai_vs_am_module.py`](../scripts/eagar_tsai_vs_am_module.py) |
| [`pycalphad-al-cu/`](pycalphad-al-cu/) | pycalphad + MatCalc/SGTE open databases vs published Thermo-Calc numbers and ORCHID experiments, for Al and Cu alloys |
| [`orchid/`](orchid/) | the five orchid-calphad repos |
| [`phaseforge/`](phaseforge/) | ATAT, PhaseForge, PhaseForgePlus, MaterialsFramework, BLADE, sqs-benchmark, PAIPAI |
| [`bo/`](bo/) | the 14 Bayesian-optimization / ML repos |
| [`misc/`](misc/) | the 8 remaining repos |

Each group folder has a `README.md` (the full report, with exact commands and error lines), `logs/` (trimmed),
`data/`, `figures/` and `scripts/` (our drivers and small patches; no third-party code is copied).

## Licences and what is not here

- No third-party code, database files, model weights or papers are committed. Databases are cited by name, version
  and SHA-256.
- Data derived from ORCHID and the SGTE binary collection are CC BY 4.0: cite ORCHID (see orchid-data's README) and
  Hallstedt, Calphad 89 (2025) 102833.
- ATAT is CC BY-ND 4.0, and the GRACE-2L-OMAT weights are for academic, non-commercial use only. Neither is
  redistributed.
- Some ArroyaveLab repos have no licence file. For those, only numbers and plots from our runs are committed; the
  microscopy overlays, which embed microseg_lab's sample images, and a TDB derived from PhaseForgePlus's example were
  left out.
