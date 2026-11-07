# High-Throughput CALPHAD / Thermo-Calc on HPC Clusters

> **Project**: FLAIME (Fast Learning AI for Mineral Efficiency) — Genesis Mission Topic 3B (Critical Minerals, AMMTO)
>
> **Issue**: [Can CALPHAD / ThermoCalc be run in high throughput?](https://github.com/vertical-cloud-lab/digital-alloy-lab-private/issues/3)
>
> **Short answer**: Yes — both open-source (pycalphad, Equilipy) and commercial (Thermo-Calc TC-Python) CALPHAD tools support high-throughput parallel execution. Published studies have screened up to **450,000 compositions** with TC-Python and **2 billion compositions** using ML surrogates trained on CALPHAD data. Multiple parallelization frameworks (joblib, MPI, Dask, Parsl, SLURM job arrays) have been demonstrated in the literature.
>
> **Partnership**: Thermo-Calc is providing a **letter of collaboration** for the Genesis Mission proposal, with AM Module simulations delivered as preliminary results and TC-Python running on BYU HPC. Together with Valimet (gas atomization) and AMAZEMET (ultrasonic atomization, atomizer installed at BYU), these form the three collaboration partners.

*Edison Scientific literature search results backing this analysis are in [`edison-trajectories/`](edison-trajectories/).*

---

## Table of Contents

1. [Live Demo Results](#live-demo-results)
   - [pycalphad (v0.11.1)](#pycalphad-v0111--600-calculations)
   - [Equilipy (v0.2.1)](#equilipy-v021--81-calculations)
   - [OpenCalphad (v6.106)](#opencalphad-v6106--3-calculations)
   - [Cross-Tool Comparison](#cross-tool-comparison)
   - [Key Differences](#key-differences-between-pycalphad-equilipy-and-opencalphad)
     - [Accuracy / Quality](#accuracy--quality)
     - [What is a TDB file?](#what-is-a-tdb-file)
     - [Why database availability matters](#why-database-availability-matters)
     - [TDBDB vs. commercial databases](#tdbdb-vs-commercial-databases-tcfe-tchea)
     - [What it takes to build a commercial-quality database](#what-it-takes-to-build-a-commercial-quality-database)
     - [Why CALPHAD assessments stop at ternary](#why-calphad-assessments-stop-at-ternary)
     - [Architecture comparison](#architecture-comparison)
2. [Licensing & Pricing](#licensing--pricing)
3. [Overview of Approaches](#overview-of-approaches)
4. [Open-Source: pycalphad](#open-source-pycalphad)
   - [Example 1: Parallel Screening with joblib](#example-1-parallel-screening-with-joblib)
   - [Example 2: Dask for Multi-Node Distributed Computing](#example-2-dask-for-multi-node-distributed-computing)
   - [Example 3: SLURM Job Array Pattern](#example-3-slurm-job-array-pattern)
   - [Example 4: MPI with mpi4py](#example-4-mpi-with-mpi4py)
5. [Open-Source: Equilipy (Built-in Parallel)](#open-source-equilipy)
6. [Commercial: Thermo-Calc TC-Python](#commercial-thermo-calc-tc-python)
   - [Batch Equilibrium Example](#batch-equilibrium-example)
   - [TC-Python with SLURM](#tc-python-with-slurm)
   - [Licensing Constraints](#licensing-constraints)
7. [Dedicated HT-CALPHAD Frameworks](#dedicated-ht-calphad-frameworks)
8. [ML Surrogates for Extreme Throughput](#ml-surrogates-for-extreme-throughput)
9. [Published Large-Scale Screening Examples](#published-large-scale-screening-examples)
10. [Free Thermodynamic Databases](#free-thermodynamic-databases)
11. [Best Practices](#best-practices)
12. [Architecture Patterns for BYU VCL (Topic 3B)](#architecture-patterns-for-byu-vcl-topic-3b--critical-minerals)
13. [Compelling Visualizations for Proposal](#compelling-visualizations-for-genesis-mission-proposal-topic-3b)
14. [References](#references)

---

## Live Demo Results

The following calculations were **actually executed** using three different open-source CALPHAD tools — pycalphad, Equilipy, and OpenCalphad — to verify that high-throughput CALPHAD works in practice.

### pycalphad (v0.11.1) — 600 Calculations

All 600 pycalphad equilibrium calculations succeeded with 0 errors.

### Demo 1: Single Equilibrium (Al-Fe at 1000K)

```
Database: alfe.tdb
Phases: LIQUID, BCC_A2, B2_BCC, FCC_A1, HCP_A3, AL2FE, AL13FE4, AL5FE2, AL5FE4
X(Al) = 0.30, T = 1000 K, P = 101325 Pa
→ Gibbs energy (GM) = -64,923.38 J/mol
→ Time: 0.376s
```

### Demo 2: Vectorized Temperature Sweep (50 points, Al-Mg)

pycalphad's `equilibrium()` natively supports vectorized inputs — 50 temperature points in a single call:

```
Database: Al-Mg_Zhong.tdb (6 phases)
X(Mg) = 0.10, T = 300–1000 K (50 steps)
→ 50 equilibria in 0.425s (117.7 calcs/sec)
→ GM range: [-46,168, -9,503] J/mol
```

### Demo 3: Parallel Screening (100 points, Al-Fe)

10 compositions × 10 temperatures = 100 independent equilibrium calculations:

```
Serial:   100 calcs in 9.16s  (10.9 calcs/sec)
Parallel: 100 calcs in 8.18s  (12.2 calcs/sec, 4 workers)
Speedup:  1.12x (limited by 2-CPU sandbox — expect near-linear on HPC)
Success:  100/100 (0 errors)
```

Sample output:
| X(Al) | T (K) | GM (J/mol) |
|-------|--------|------------|
| 0.050 | 500 | -20,276 |
| 0.050 | 644 | -26,872 |
| 0.050 | 789 | -34,584 |
| 0.050 | 933 | -43,387 |
| 0.050 | 1078 | -53,300 |

### Demo 4: Higher Throughput (500 points)

25 compositions × 20 temperatures = 500 equilibrium calculations:

```
500 calcs in 39.16s (12.8 calcs/sec, 4 workers)
Success: 500/500 (0 errors)
```

> **Extrapolation**: At ~3.2 calcs/sec/core on this sandbox (12.8 calcs/sec total with 4 workers), a 64-core HPC node would achieve ~205 calcs/sec, completing **100,000 equilibria in ~8 minutes**. A 10-node SLURM job array (640 cores) would finish **1 million calculations in ~8 minutes**.

### Demo Script

<details>
<summary>Click to expand the full demo script (runs in ~50 seconds)</summary>

```python
"""
pycalphad High-Throughput CALPHAD Demo
Runs real equilibrium calculations with built-in test databases.
Requirements: pip install pycalphad
"""
import time
import json
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from pycalphad import Database, equilibrium, variables as v

DB_DIR = os.path.join(os.path.dirname(__import__('pycalphad').__file__),
                      'tests', 'databases')
ALFE_TDB = os.path.join(DB_DIR, 'alfe.tdb')
ALMG_TDB = os.path.join(DB_DIR, 'Al-Mg_Zhong.tdb')

def calc_eq_point(args):
    """Compute equilibrium at one composition-temperature point."""
    x_al, temp, db_path = args
    from pycalphad import Database, equilibrium, variables as v
    db = Database(db_path)
    components = ["AL", "FE", "VA"]
    all_phases = list(db.phases.keys())
    try:
        result = equilibrium(
            db, components, all_phases,
            {v.X("AL"): x_al, v.T: temp, v.P: 101325, v.N: 1}
        )
        return {
            "X_AL": round(float(x_al), 4),
            "T": float(temp),
            "GM": float(result.GM.values.squeeze()),
        }
    except Exception as e:
        return {"X_AL": round(float(x_al), 4), "T": float(temp), "error": str(e)}

if __name__ == "__main__":
    # Demo 1: Single equilibrium
    dbf = Database(ALFE_TDB)
    eq = equilibrium(dbf, ["AL", "FE", "VA"], list(dbf.phases.keys()),
                     {v.X("AL"): 0.3, v.T: 1000, v.P: 101325, v.N: 1})
    print(f"Single eq: GM = {float(eq.GM.values.squeeze()):.2f} J/mol")

    # Demo 2: Vectorized sweep
    dbf_mg = Database(ALMG_TDB)
    temps = np.linspace(300, 1000, 50)
    eq_sweep = equilibrium(dbf_mg, ["AL", "MG", "VA"], list(dbf_mg.phases.keys()),
                           {v.X("MG"): 0.1, v.T: temps, v.P: 101325, v.N: 1})
    print(f"Vectorized: {len(temps)} points computed")

    # Demo 3+4: Parallel screening
    for n_comp, n_temp, label in [(10, 10, "100-pt"), (25, 20, "500-pt")]:
        tasks = [(float(x), float(t), ALFE_TDB)
                 for x in np.linspace(0.05, 0.95, n_comp)
                 for t in np.linspace(500, 1800, n_temp)]
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(calc_eq_point, tasks))
        elapsed = time.time() - t0
        valid = [r for r in results if "error" not in r]
        print(f"{label}: {len(valid)}/{len(tasks)} OK in {elapsed:.1f}s "
              f"({len(tasks)/elapsed:.1f} calcs/sec)")
```
</details>

### Equilipy (v0.2.1) — 81 Calculations

Equilipy was installed via `pip install equilipy` and tested with the AlCuMgSi_ORNL ChemSage database from the ORNL repository. All single-point and sweep calculations succeeded. Equilipy reads [**ChemSage .dat format only**](https://ornl.github.io/Equilipy/database.html) (not TDB) — this is documented by Kwon et al. 2024 (JOSS) and confirmed in the [Equilipy database docs](https://ornl.github.io/Equilipy/database.html).

#### Single Equilibrium (Al-Cu-Mg-Si at 500K)

```
Database: AlCuMgSi_ORNL_FS73.dat (ChemSage format)
Condition: Al=0.96, Mg=0.03, Si=0.01 (mass frac), T=500K, P=1atm
→ Stable phases: MG2SI(s), FCC_A1
→ Phase amounts (mass): MG2SI=0.027, FCC_A1=0.973
→ Time: 0.025s
```

#### Temperature Sweep (10 points, Al-Cu-Mg-Si, 400–900K)

```
10 calcs in 0.988s (10.1 calcs/sec)
Success: 10/10 | Errors: 0
  T=400K: 4 phases — AL5CU2(s), FCC_A1, ALCU_THETA, DIAMOND_A4
  T=567K: 4 phases — AL5CU2(s), FCC_A1, ALCU_THETA, DIAMOND_A4
  T=900K: transitions to liquid phase
```

#### Composition Sweep (20 points, Al-Mg-Si at 600K)

```
20 calcs in 1.093s (18.3 calcs/sec)
Success: 20/20 | Errors: 0
  Mg=0.010: 3 phases — MG2SI(s), FCC_A1, DIAMOND_A4
  Mg=0.040: 3 phases — MG2SI(s), FCC_A1
  Mg=0.150: transition to different phase assemblage
```

#### Batch Mode (50 points, built-in parallelism)

Equilipy's `equilib_batch()` runs with built-in multiprocessing (2 CPUs in this sandbox):

```
50 calcs in 1.862s (26.9 calcs/sec) with nCPU=2
Shows phase evolution from MG2SI+AL5CU2+ALCU_THETA+FCC_A1 at 400K
  → FCC_A1+LIQUID two-phase region at ~870K
  → fully LIQUID above ~950K
```

> **Key takeaway**: Equilipy's batch mode achieves **26.9 calcs/sec** with just 2 CPUs — faster than pycalphad's per-core rate on the same hardware. On an HPC node with MPI across 64 cores, this would extrapolate to **~860 calcs/sec**.

### OpenCalphad (v6.106) — 3 Calculations

OpenCalphad was compiled from source (`git clone + make`, requires `gfortran`) and tested with the built-in Cr-Fe TDB database. All calculations succeeded.

#### Cr-Fe Equilibria at X(Cr)=0.3

| T (K) | G (J/mol) | Stable Phases | Time (s) | Notes |
|--------|-----------|---------------|----------|-------|
| 800 | -29,777 | BCC_A2 (X(Cr)=0.198) + SIGMA (X(Cr)=0.506) | 4.27×10⁻⁴ | Two-phase: σ phase predicted |
| 1000 | -43,169 | BCC_A2 (single phase) | 1.09×10⁻³ | Single BCC solid solution |
| 1500 | -83,355 | BCC_A2 (single phase) | 6.73×10⁻⁴ | High-T single phase |

```
OpenCalphad v6.106, compiled 2026-03-08
Database: crfe.TDB (Andersson & Sundman, CALPHAD 1987)
Phases: BCC_A2, FCC_A1, SIGMA, LIQUID

Example output at 800K:
  BCC_A2:  0.668 mol, X(Fe)=0.802, X(Cr)=0.198
  SIGMA:   0.332 mol, X(Cr)=0.506, X(Fe)=0.494
  → Correctly predicts σ-phase formation in the Cr-Fe miscibility gap
```

> **Key takeaway**: OpenCalphad equilibrium calculations complete in **0.4–1.1 ms each** — roughly 1000–2500 calcs/sec per core. It uses OpenMP for parallel execution and reads standard TDB files. However, it requires compilation from source (no pip install) and has a command-line interface rather than a Python API. The [OpenCalphad-Python](https://github.com/Jerry1999/OpenCalphad-Python) and [pyopencalphad](https://github.com/dpttw/pyopencalphad) community projects provide Python bindings.

### Cross-Tool Comparison

| Tool | Install | Database Format | Single Calc Speed | Batch (2 CPU) | HPC Ready? |
|---|---|---|---|---|---|
| **pycalphad** | `pip install` | TDB | ~10 calcs/sec | 12.8 calcs/sec | ✅ joblib/Dask/MPI |
| **Equilipy** | `pip install` | ChemSage .dat | ~40 calcs/sec | 26.9 calcs/sec | ✅ Built-in MPI |
| **OpenCalphad** | Compile from source | TDB | ~1000–2500 calcs/sec | N/A (CLI) | ✅ OpenMP + TQ library |

### Key Differences Between pycalphad, Equilipy, and OpenCalphad

#### Accuracy / Quality

All three tools implement the same underlying CALPHAD formalism — minimizing Gibbs energy using sublattice models (Compound Energy Formalism). **Given identical thermodynamic parameters as input, they produce the same equilibrium results.** The speed differences come from implementation language and solver strategy, not from thermodynamic accuracy.

The quality of CALPHAD results depends almost entirely on the **database** (the assessed interaction parameters), not the software. A well-assessed database on any of these tools will give accurate predictions; a poorly fitted database will give poor predictions on all of them. This is why database availability (see below) matters as much as the software choice.

#### What is a TDB file?

A **TDB** (Thermodynamic DataBase) file is the standard text format for storing CALPHAD thermodynamic parameters. Originally defined by Thermo-Calc AB, it has become the de facto standard across most CALPHAD software. A TDB file contains:
- **Element definitions** — which elements are modeled
- **Phase definitions** — crystal structures and sublattice models (e.g., FCC_A1 with 2 sublattices)
- **Gibbs energy functions** — temperature-dependent polynomials for pure elements and stoichiometric compounds
- **Interaction parameters** — L-parameters describing mixing behavior between elements in each phase (these are the key "assessed" values fitted to experimental data)

Example snippet from a TDB file:
```
ELEMENT AL FCC_A1 26.982 4577.3 28.322 !
ELEMENT FE BCC_A2 55.845 4489.0 27.280 !

PHASE FCC_A1 % 2 1 1 !
CONSTITUENT FCC_A1 :AL,FE : VA: !

PARAMETER G(FCC_A1,AL:VA;0) 298.15
    -7976.15+137.093*T-24.3671*T*LN(T); 6000 N !

PARAMETER L(FCC_A1,AL,FE:VA;0) 298.15 -76066.1+18.6758*T; 6000 N !
```

The `L(FCC_A1,AL,FE:VA;0)` line is an assessed interaction parameter — the result of fitting to experimental phase diagram and thermochemical data. These parameters are what make a database valuable, and producing them requires significant expert effort.

**ChemSage .dat files** (used by Equilipy) contain the same types of thermodynamic data but in a different binary/text format originally from FactSage. The formats are not interchangeable — you cannot use a TDB file in Equilipy or a .dat file in pycalphad without conversion.

#### Why database availability matters

There are **766+ freely available TDB files** indexed by TDBDB (van de Walle et al. 2018), covering a wide range of alloy systems from published literature. pycalphad and OpenCalphad can read any of these. Equilipy's ChemSage .dat format has far fewer freely available databases (ORNL provides a handful: AlCuMgSi, AlFeSi), making it less flexible for exploring new alloy systems unless you already have .dat files from FactSage.

Commercial databases (Thermo-Calc's TCFE, TCHEA, TCNI, etc.) represent years of expert assessment and cover broader composition/temperature ranges with higher confidence, but are licensed separately on top of the software license.

#### TDBDB vs. commercial databases (TCFE, TCHEA)

The key distinction is **scope and consistency**, not fundamental methodology. Both free and commercial databases use the same CALPHAD formalism — the difference is how many systems have been rigorously assessed and how well they work together in multicomponent predictions.

| Aspect | TDBDB (free TDB files) | TCFE (Thermo-Calc steels) | TCHEA (Thermo-Calc HEAs) |
|---|---|---|---|
| **What it is** | Indexed collection of 766+ TDB files from 528 published papers | Professionally assessed database for Fe-based alloys | Professionally assessed database for high-entropy alloys |
| **Systems assessed** | Varies by file — each TDB covers 1 paper's scope (typically 1–5 binaries/ternaries) | ~350+ binary, ~175+ ternary subsystems, all mutually consistent (TCFE12) | 307 binary, 493 higher-order subsystems (TCHEA4); earlier TCHEA1 had 15 elements, 105 binaries, 200 ternaries (Mao et al. 2017, 203 cit.) |
| **Consistency** | ⚠️ **Low** — each TDB was independently assessed by different researchers with different conventions, reference states, and model choices | ✅ **High** — all subsystems assessed together to ensure mutual consistency across the full composition space | ✅ **High** — same approach, focused on HEA elements |
| **Multicomponent reliability** | ⚠️ **Cannot combine** TDB files from different papers — parameters from separate assessments are not compatible | ✅ Designed for multicomponent extrapolation — parameters work together for 5+ component alloys | ✅ Same — designed for 5+ component HEA calculations |
| **Elements covered** | Broad (whatever has been published) | 29 elements: Fe + common steel alloying elements (Cr, Ni, Mo, V, W, C, N, etc.) | 26 elements (TCHEA4): typical HEA elements (Al, Co, Cr, Cu, Fe, Mn, Ni, Ti, V, etc.) |
| **Phases modeled** | Varies by file | 500+ phases including all major steel phases (ferrite, austenite, carbides, nitrides, σ, χ, Laves, etc.) | ~500 phases (TCHEA4); 163 phases in earlier TCHEA1 |
| **Validation level** | Published in peer-reviewed papers, but not cross-validated with other TDB files | Validated against extensive industrial datasets; updated annually | Validated against emerging HEA experimental literature |
| **Cost** | **Free** | ~$2K–5K/yr academic | ~$2K–5K/yr academic |
| **Best use** | Quick screening, binary/ternary prototyping, education | Production multicomponent predictions for steels | Production predictions for HEAs/CCAs |

**Key insight**: The 766 TDB files in TDBDB are **not 766 interchangeable databases** — they are 766 separate, independently assessed parameter sets that generally cannot be mixed. If Paper A assessed Al-Cu-Mg and Paper B assessed Al-Cu-Si, you cannot simply merge their TDB files to get a reliable Al-Cu-Mg-Si prediction. The parameters may use different reference states, different sublattice models, or different interaction parameter orders. Commercial databases like TCFE solve this by assessing all subsystems together in a single consistent framework.

**When free TDB files are sufficient**: For binary and ternary phase diagram calculations within the scope of a single published assessment, free TDB files can be just as accurate as commercial databases — the parameters come from the same CALPHAD methodology and are fitted to the same types of experimental data. Many published HT-CALPHAD screening studies (e.g., Wang & Xiong 2020, 450K compositions) use free TDB files successfully for ternary systems.

**When commercial databases are needed**: For multicomponent alloy design (4+ elements) where you need reliable extrapolation across the full composition space. This is where the consistency advantage matters most — predicting a 5-component Fe-Cr-Ni-Mo-C steel requires all 10 binary and 10 ternary subsystems to work together coherently.

**Published comparisons**: Several studies have directly compared database predictions:
- **Ravi & Wolverton (2005, 36 cit.)** compared two commercial Al-alloy databases and found both qualitative differences (phases present in one but absent in another) and quantitative differences in phase fractions — these discrepancies would be even larger between independent free TDB files.
- **Wertz, Miller & Senkov (2018, 29 cit.)** tested 8 Pandat databases across ~29,000 ternary compositions and found that each fully assessed binary raised ternary prediction agreement by ~20%.
- **Gorsse & Senkov (2018, 131 cit.)** showed that extrapolation from binaries alone produces correct quaternary predictions only when binary miscibility gaps are absent, binary intermetallics are few, and no ternary intermetallics exist — conditions rarely met in practice.

#### What it takes to build a commercial-quality database

Building a database like TCFE or TCHEA from scratch is a massive undertaking requiring both extensive experimental data and specialized optimization expertise. Understanding this effort helps explain why these databases cost thousands per year.

**The CALPHAD assessment process** (for a single binary system):

1. **Literature survey** — Collect all published experimental data: phase boundaries, invariant reaction temperatures, enthalpies of mixing/formation, heat capacities, activity coefficients, vapor pressures, EMF measurements, etc.

2. **Critical evaluation** — Assess data quality, resolve contradictions between different experimental studies, assign weights to more reliable measurements.

3. **Model selection** — Choose appropriate thermodynamic models for each phase (e.g., Compound Energy Formalism for ordered phases, Redlich-Kister polynomials for disordered solutions, sublattice models for intermetallics).

4. **Parameter optimization** — Fit the Gibbs energy parameters (L-parameters, G-parameters) to reproduce all the experimental data simultaneously. This is done using tools like Thermo-Calc's PARROT module or open-source alternatives like ESPEI (Extensible Self-optimizing Phase Equilibria Infrastructure).

5. **Validation** — Compare calculated phase diagrams, thermodynamic properties, and driving forces against experimental data not used in fitting. Check for thermodynamic self-consistency.

**Experimental data needed per binary system**:

| Experiment type | Typical number needed | What it provides |
|---|---|---|
| **Calorimetry** (DSC, DTA) | 3–10 compositions | Enthalpies of mixing/formation, heat capacities, transformation temperatures |
| **Phase equilibria** (isothermal annealing + SEM/EDS/XRD) | 5–15 samples across composition/temperature | Phase boundaries, tie-lines, invariant reactions |
| **Diffusion couples** | 2–5 couples at different temperatures | Interdiffusion coefficients, phase boundary compositions |
| **Activity measurements** (EMF, Knudsen cell, vapor pressure) | 3–8 compositions | Chemical potentials, partial Gibbs energies |
| **Crystallography** (XRD, neutron diffraction) | 2–5 compositions | Phase identification, lattice parameters, site occupancies for sublattice models |

**Total**: ~15–40 distinct experiments per binary system, each requiring sample preparation, heat treatment (days to weeks for equilibration), and characterization.

**Effort estimates**:

| Scope | Typical effort | Experiments | What you get |
|---|---|---|---|
| **1 binary system** | 1–2 person-years | 15–40 experiments | Reliable phase diagram + thermodynamic properties for A-B |
| **1 ternary system** | 1–3 person-years | 20–60 additional experiments | Isothermal sections, liquidus projection for A-B-C |
| **TCFE-scale database** (29 elements) | ~50–100+ person-years cumulative | Thousands of experiments (built on decades of published literature) | Consistent multicomponent database for steels |
| **TCHEA-scale database** (26 elements) | ~30–60+ person-years cumulative | Hundreds to thousands of experiments | Consistent database for HEAs |

**Open-source assessment alternatives**:

- **ESPEI** ([github.com/PhasesResearchLab/ESPEI](https://github.com/PhasesResearchLab/ESPEI)) — Open-source Bayesian parameter optimization tool by Phases Research Lab (Penn State). Can automate much of step 4, but still requires curated experimental data as input. Published by Bocklund et al. (2019, *J. Phase Equilib. Diff.*).
- **PyCalphad + ESPEI workflow** — Enables fully open-source database development: collect experimental data → run ESPEI optimization → produce TDB file → validate with pycalphad. This is the path to building custom databases without commercial software.
- **First-principles (DFT) data** — Ab initio calculations (e.g., using VASP, Quantum ESPRESSO) can supplement experimental data for enthalpies of formation, providing data for systems where experiments are expensive or difficult. Projects like AFLOW and Materials Project provide pre-computed DFT energies for many intermetallic compounds.

**Bottom line**: Recreating a TCFE-quality database would require hundreds of person-years of accumulated assessment work and thousands of experiments. However, for a *specific* alloy system (e.g., a particular 4-component space), a targeted assessment is feasible within a single PhD project (3–5 years) using ESPEI + pycalphad + targeted experiments. This is the practical path for academic labs — assess the specific systems you need rather than building a general-purpose commercial database.

#### Why CALPHAD assessments stop at ternary

A common observation is that published CALPHAD database assessments almost always cover binary (A-B) and ternary (A-B-C) systems, but rarely quaternary or higher. This is by design, not a limitation.

**The extrapolation principle**: CALPHAD's core architectural assumption is that multicomponent thermodynamics can be predicted by *extrapolating* from assessed binary and ternary interactions. For a solution phase, the Gibbs energy of mixing in a multicomponent system is built from weighted sums of binary interaction parameters using geometric models (Muggianu, Kohler, or Toop extrapolations). The Muggianu model — the most common — computes the excess Gibbs energy of an N-component system entirely from pairwise (binary) L-parameters:

```
G_excess(A,B,C,D,...) = Σᵢ<ⱼ xᵢxⱼ Σₖ Lₖ(i,j)(xᵢ - xⱼ)ᵏ + ternary corrections
```

This means that once you have assessed all the binaries and added ternary correction terms where needed, you can *predict* quaternary, quinary, and higher-order equilibria without fitting any additional parameters. This extrapolation works because:

1. **Physics**: In most metallic systems, pairwise atomic interactions dominate. Three-body and higher-order interactions exist but are typically much weaker.

2. **Empirical validation**: Decades of CALPHAD practice have shown that binary+ternary extrapolation produces reliable multicomponent predictions for most engineering alloys. The entire field of computational alloy design (ICME) relies on this assumption — commercial databases like TCFE and TCHEA are used daily to predict 5–10+ component alloys from binary/ternary assessments.

3. **Cost-benefit**: The number of subsystems grows combinatorially. A 5-component system has 10 binaries and 10 ternaries. A 10-component system has 45 binaries and 120 ternaries — already a massive assessment effort. Quaternary combinations (C(10,4) = 210) would be prohibitive, and the marginal improvement is usually small.

**Why assessments stop at ternary (and when they don't)**:

| Level | What's assessed | Why stop here? |
|---|---|---|
| **Binary** (A-B) | Full A-B phase diagram + thermodynamic properties | Foundation — always needed |
| **Ternary** (A-B-C) | Ternary interaction parameters where binary extrapolation fails — ternary intermetallics, ternary miscibility gaps, asymmetric solubility effects | Usually sufficient — catches most important higher-order effects |
| **Quaternary** (A-B-C-D) | Quaternary interaction parameters — *rarely needed* | Only when specific quaternary compounds or effects are experimentally observed (e.g., σ-phase stabilization in Fe-Cr-Ni-Mo). Quaternary L-parameters do exist in some commercial databases |
| **Quinary+** | Almost never assessed | No known systems where quinary interactions are significant enough to justify assessment |

**When binary+ternary extrapolation fails** (Gorsse & Senkov 2018, 131 cit.):
- **Ternary intermetallic compounds** that don't exist in any of the constituent binaries (e.g., Heusler phases)
- **Ternary miscibility gaps** absent in the binaries
- **Asymmetric higher-order interactions** in complex phases like σ (sigma) or χ (chi)
- **Order-disorder transitions** that only emerge in multicomponent compositions

In these cases, ternary corrections are added. But quaternary corrections are almost never needed — the error from missing them is typically smaller than the experimental uncertainty in the data used to fit the binary/ternary parameters.

**The practical takeaway**: When CALPHAD predicts a 6-component alloy's phase diagram, it's *not* using independently assessed 6-component data — it's extrapolating from a web of assessed binary and ternary subsystems. This is both the power and the risk of CALPHAD: the power is that you can predict an astronomically large composition space from a manageable number of assessments; the risk is that the extrapolation can fail for systems with strong higher-order interactions. This is why database *consistency* (all subsystems assessed together, as in TCFE/TCHEA) matters more than database *size* — inconsistent binary/ternary parameters produce unreliable multicomponent extrapolations.

**Implications for HT-CALPHAD screening**: Binary/ternary extrapolation is why high-throughput CALPHAD screening works at all — you can screen millions of multicomponent compositions computationally because each equilibrium calculation only needs the pre-assessed binary/ternary parameters. But the screening results should be validated experimentally for the most promising compositions, because extrapolation failures are hard to predict a priori.

#### Architecture comparison

These three open-source CALPHAD tools take fundamentally different architectural approaches:

| Aspect | pycalphad | Equilipy | OpenCalphad |
|---|---|---|---|
| **Language** | Pure Python (NumPy/SciPy) | Python wrapper around Fortran solver | Fortran (with optional Python bindings) |
| **Solver approach** | Symbolic energy models + SciPy minimization | Gibbs energy minimization via ChemApp-style Fortran core | Global minimization with grid-based starting points |
| **Speed per core** | ~3–10 calcs/sec | ~20–40 calcs/sec | ~1,000–2,500 calcs/sec |
| **Why the speed gap** | Pure Python overhead; symbolic differentiation at runtime | Compiled Fortran solver, but Python marshalling overhead | Native compiled Fortran; no interpreter overhead |
| **Database format** | TDB (standard) | **ChemSage .dat only** (FactSage 7.3 compatible) | TDB (standard) |
| **Database availability** | 766+ TDB files via TDBDB; COST507; MatCalc open DBs | Limited — requires .dat files (ORNL provides a few: AlCuMgSi, AlFeSi) | Same TDB ecosystem as pycalphad |
| **Parallelism** | External: joblib, Dask, MPI (user must implement) | **Built-in**: native batch mode with automatic MPI parallelism | OpenMP threading; TQ library for programmatic access |
| **Python integration** | Native — designed as a Python library | Native — `pip install equilipy` | CLI-based; community Python wrappers exist (pyopencalphad, OpenCalphad-Python) |
| **Ease of use** | ⭐⭐⭐ Easiest — pure Python, well-documented, Jupyter-friendly | ⭐⭐ Easy install, but limited database ecosystem | ⭐ Requires gfortran + compile from source; interactive CLI |
| **Best for** | Rapid prototyping, education, custom workflows | Production HPC screening with MPI; FactSage-compatible workflows | Maximum single-core throughput; large-scale OpenMP screening |
| **Origin** | Academic (Otis & Liu, Penn State/U. Wisconsin) | ORNL (Kwon et al. 2024, JOSS) | NIST/KTH (Sundman et al.) |
| **License** | MIT | Open-source | GNU GPL |
| **Active development** | Yes (v0.11.1, 2024) | Yes (v0.2.1, 2024) | Yes (v6.106, 2024) |

**When to use each:**

- **pycalphad**: Best starting point for most users. Pure Python means easy debugging, Jupyter integration, and access to the largest TDB database ecosystem (766+ files via TDBDB). Speed is adequate for screening up to ~100K compositions on an HPC node. The joblib/Dask/MPI patterns shown below scale well.

- **Equilipy**: Choose when you need **built-in parallelism without writing parallel code** — just call `equilipy.equilib()` in batch mode and it handles MPI distribution automatically. The tradeoff is being locked into ChemSage .dat databases (not TDB), which limits available thermodynamic data. Ideal if your workflow already uses FactSage.

- **OpenCalphad**: Choose when **raw speed matters** — at 1,000–2,500 calcs/sec/core, it's ~100–250x faster than pycalphad. This makes million-point screenings feasible on a single node. The tradeoff is harder setup (compile from source) and CLI-oriented workflow, though the TQ Fortran library enables programmatic access. Best for large-scale production runs after prototyping with pycalphad.

---

## Licensing & Pricing

> **Summary**: Thermo-Calc pricing is by quote; Pandat is $12K–20K/yr academic; JMatPro is ~$5.7K/yr. Open-source alternatives (pycalphad, OpenCalphad, Equilipy) are **free** and have no processor limits.

### Cost Comparison

| Software | Type | Academic Price (est.) | Commercial Price | Processor Limit | Notes |
|---|---|---|---|---|---|
| **pycalphad** | Open-source (MIT) | **Free** | **Free** | **None** | Python; reads TDB files; community databases |
| **OpenCalphad** | Open-source (GNU) | **Free** | **Free** | **None** | Fortran; TDB compatible; NIST-supported |
| **Equilipy** | Open-source | **Free** | **Free** | **None** | Built-in MPI parallelism; Fortran solver |
| **Thermo-Calc** | Commercial | By quote | By quote | 32 logical processors per license | Assessed databases (TCFE, TCHEA, TCNI, etc.) |
| **TC-Python SDK** | Commercial add-on | Included in some ANSP; otherwise extra | Separate license | Same 32-proc cap | Python scripting API for Thermo-Calc |
| **Pandat** | Commercial | $12,000/yr (base); $20,000/yr (with precipitation) | Higher | N/A | CompuTherm; single-user non-transferable |
| **JMatPro** | Commercial | ~$5,710/yr | Higher | N/A | Sente Software; material properties focus |
| **MatCalc** | Commercial | Free community edition available | Paid | N/A | Austrian; precipitation kinetics focus |

### Thermo-Calc Licensing Details

| License Type | Description |
|---|---|
| **Single User Node Locked (SUNLL)** | Fixed to one computer and one user |
| **Network License (NWL)** | Multiple users at one site via FlexLM |
| **Academic Network Site Package (ANSP)** | Up to 99 concurrent students; includes faculty licenses |
| **Free Student Version** | Limited features; individual study only |
| **TC-Python SDK** | Add-on license for Python scripting; required for HT workflows |

> **Key constraints for HPC**: TC-Python is capped at **32 logical processors per license** (documented by Kwon et al. 2024 in the Equilipy paper). For HPC-scale screening (>32 cores), you need either multiple licenses or open-source alternatives.

### Pricing Sources
- Thermo-Calc: [Request a quotation](https://thermocalc.com/request-a-quotation/) — no public pricing
- Pandat: [$12K/yr base, $20K/yr with precipitation module](https://www.asminternational.org/pandat/) (ASM International)
- JMatPro: [$5,710/yr academic](https://www.procurement.msstate.edu/procurement/bids/223-100.pdf) (Mississippi State University sole source notice)
- pycalphad: [Free (MIT license)](https://pycalphad.org/)
- OpenCalphad: [Free (GNU license)](https://www.opencalphad.com/)
- Equilipy: [Free (open-source)](https://doi.org/10.21105/joss.06875)

### Recommendation for BYU VCL (Topic 3B — Critical Minerals)

**Start with pycalphad (free)** for immediate HT screening of **Al-Zr and Al-Mn-Cr-Zr** composition spaces using TDBDB/COST507 TDB files. This requires $0 in licensing and has no processor limits. For multicomponent (4+ element) refinement of top candidates, upgrade to **TCAl10** via Thermo-Calc — essential for consistent Al-Zr-Mn-Cr quaternary predictions where free TDB files from different papers cannot be combined. BYU has already demonstrated Thermo-Calc CALPHAD simulations running on BYU's HPC clusters and received AM Module simulations from Thermo-Calc as preliminary results.

**Topic 3B framing:** The screening pipeline targets **critical mineral substitution** — discovering Al alloys that eliminate dependence on supply-constrained Mg, Sc, and REE additions while maintaining or exceeding AM-relevant mechanical properties. The mineral-burden objective (weighted sum of critical mineral content) is integrated as a CALPHAD screening criterion alongside phase stability and crack resistance. This aligns with the AMMTO mission and DOE Genesis Mission Topic 3B (Securing America's Critical Minerals Supply).

**Partnership context:** Thermo-Calc is providing a **letter of collaboration** for the Genesis Mission proposal. Together with Valimet (gas atomization) and AMAZEMET (ultrasonic atomization, atomizer installed at BYU), these form the three collaboration partners. Eight additional partners provide letters of support: Ames National Lab, Fehrmann Alloys, Taylor Sparks (U of Utah), Ashley Speer, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, and Keith Brown.

> **Important note on database costs**: Commercial CALPHAD databases (TCFE, TCNI, TCHEA, TCAl, etc.) are sold **separately** from the software license and can represent a significant additional expense (Andersson et al. 2002; Vary 2023). For Topic 3B, **TCAl10 is the priority database** (Al alloys with Zr, Mn, Cr coverage). TCFE12/13 are not needed for the primary Al-Zr/Al-Mn-Cr-Zr focus.

> **Equilipy caveat**: While Equilipy has excellent built-in MPI parallelism, it currently (v0.1.5) only reads **ChemSage .dat format** (compatible with FactSage 7.3), not the standard .tdb format used by Thermo-Calc and pycalphad (Kwon et al. 2024). This limits database compatibility.

*Full Edison Scientific literature analysis on CALPHAD licensing is in [`edison-trajectories/calphad_licensing.md`](edison-trajectories/calphad_licensing.md).*

### Thermo-Calc Contacts & AM Module

#### Primary Contact: a Thermo-Calc specialist

**A Thermo-Calc specialist** — Thermo-Calc Software Inc. (North America office), based in McMurray, PA. He is the primary point of contact for academic partnerships, licensing, training, and technical engagement in North America.

| | |
|---|---|
| **Role** | Thermo-Calc Software Inc. (US) |
| **Location** | 4160 Washington Road, McMurray, PA 15317 |
| **Email** | info@thermocalc.com (general); individual contact via [thermocalc.com/contact-us](https://thermocalc.com/contact-us/) |
| **Phone** | +1 (724) 731-0074 |

| **Notable** | Runs AM Module training courses |

The Thermo-Calc specialist can address all of the following for BYU:
1. **Clarification of current BYU licenses** — what databases/versions are included
2. **Upgrade pricing** to more recent Thermo-Calc versions and databases
3. **AM Module** availability, pricing, and proof-of-concept setup
4. **TC-Python SDK** access for HPC workflow integration

#### Additive Manufacturing (AM) Module

The Thermo-Calc **AM Module** (introduced 2023b, printability maps added 2024b) simulates PBF-LB and PBF-EB melt pool behavior using CALPHAD-derived thermophysical properties. It is available as an add-on to the main Thermo-Calc license.

**Inputs:**
- Alloy composition (from CALPHAD database — TCFE, TCNI, TCHEA, TCAl, etc.)
- Process parameters: laser power, scan speed, beam diameter, layer thickness, preheat temperature
- Build geometry: substrate thickness, powder bed properties

**Outputs:**
- Melt pool dimensions (width, depth, length) and geometry
- **Printability maps** (2024b+): keyholing, lack-of-fusion, and balling defect boundaries as function of power vs. scan speed
- Temperature fields and cooling rates
- Solidification conditions (temperature gradient G, solidification velocity R, G/R ratio)
- Phase fractions and microsegregation predictions (via Scheil solidification)

**Python control (TC-Python API):**
- Full AM Module functionality is accessible via TC-Python, enabling:
  - Automated parameter sweeps across power–speed space
  - Batch printability map generation for multiple alloys
  - Integration into larger optimization workflows (e.g., Bayesian optimization)
  - Example: `system.with_additive_manufacturing()` → set process conditions → calculate

**Compatible databases:** TCFE13+, TCNI12+, TCAl9+, TCHEA6+ (each sold separately)

**Key limitation:** No Marangoni convection or recoil pressure modeling — the module uses a conduction-mode thermal model, which may underpredict keyhole depth at high energy densities.

**Pricing:** The AM Module is an add-on to the base Thermo-Calc license. Academic pricing is not published — request a quote from Thermo-Calc.

**Key research groups using TC AM Module:**
- Sheikh & Arroyave (Texas A&M) — HT HEA printability screening, *Nature Comput. Mater.* 2025
- Hussain et al. (Chalmers) — CM247LC PBF-LB simulation, 2024
- Pak et al. (CMU) — Agentic AI + TC for LPBF alloy evaluation, *arXiv* 2025
- Sargent et al. (UC Davis/Pittsburgh) — TC-Python + DICTRA for solidification cracking, 2021

#### AM Module Steady-State Input Parameters

The following parameters are required for a steady-state AM Module calculation (provided by Thermo-Calc's account manager):

| Section | Parameter | Default Value |
|---|---|---|
| **Global Settings** | Gas pressure | 100,000 Pa |
| | Temperature unit | Celsius |
| | Base plate temperature | 30.0 °C |
| | Ambient temperature | 23.0 °C |
| | Fluid flow incl. Marangoni effect | Enabled |
| | Separate powder material properties | Enabled |
| | Powder density | 80% of solid |
| **Geometry** | Height | 2.0 mm |
| | Mesh | Coarse |
| **Heat Source** | Profile | Gaussian |
| | Power | 200.0 W |
| | Absorptivity | Calculated |
| | Prefactor | 1.0 |
| | Wavelength | 1064.0 nm |
| | Beam radius | 40.0 µm |
| | Keyhole model | Enabled |
| | Beam quality factor M² | 1.0 |
| **Scanning Strategy** | Scanning speed | 1000.0 mm/s |
| | Layer thickness | 40.0 µm |
| **Boundary Conditions** | Radiation emissivity | 0.8 |
| | Convective heat transfer coeff. | 20.0 W/m² |
| | Evaporation | Enabled |
| **Calculation Type** | Mode | Single Point |

**Note on absorptivity for aluminum:** The AM Module calculates absorptivity from electrical resistivity of the liquid phase. This works well for steels and nickel alloys but requires a pre-factor adjustment for aluminum alloys due to oxide film (Al₂O₃) effects. Calibration via cross-sectional melt pool measurements (width + depth) is recommended (Thermo-Calc's account manager, personal communication, April 2026). **For Topic 3B Al-Zr alloys:** Zr additions may alter the oxide layer characteristics (ZrO₂ formation) and solidification path (peritectic vs. eutectic), potentially requiring different absorptivity pre-factors than AlSi10Mg. Initial calibration with AlSi10Mg baseline, then Al-Zr validation, is the recommended approach.

#### Proof-of-Concept Status

**Status (April 2026):** Thermo-Calc has provided AM Module simulations for BYU as preliminary results — these demonstrate melt pool geometry and process parameter predictions for AlSi10Mg baseline and Al-Zr candidate compositions. Additionally, BYU has run Thermo-Calc CALPHAD simulations on BYU's HPC clusters, confirming the TC-Python + SLURM integration pathway. Thermo-Calc is providing a **letter of collaboration** for the Genesis Mission proposal (Topic 3B — Critical Minerals).



#### Edison Scientific Analysis of Discussion (task `eb5a3fde`)

Key strategic findings from Edison ANALYSIS of the Thermo-Calc call transcript (full analysis in `edison-trajectories/thermocalc_discussion_analysis.md`). Note: The original analysis described an advisory-only model. Since then, Thermo-Calc has **upgraded to a letter of collaboration** with AM Module simulations provided as preliminary results and TC-Python running on BYU HPC:

1. **Thermo-Calc collaboration model:** Thermo-Calc is providing a **letter of collaboration** for the Genesis Mission proposal, with AM Module simulations delivered as preliminary results and TC-Python + TCAl10 for HPC CALPHAD screening on BYU clusters. Support includes advisory hours, student training, and reciprocal data exchange (BYU provides first systematic Al-Zr LPBF melt pool validation data for TC).
2. **Five confirmed AM Module outputs:** (a) melt pool shape, (b) process maps, (c) G/R solidification conditions, (d) equiaxed-to-columnar transition, (e) thermal profiles. Crack susceptibility is in base TC (Scheil), NOT the AM Module.
3. **Recommended hybrid architecture for Topic 3B:** pycalphad ($0) for 100K+ Al-Zr/Al-Mn-Cr-Zr phase screening with mineral-burden filter → TC-Python + TCAl10 for top 1,000 multicomponent refinements → TC AM Module for top 50–100 printability maps. Mineral-burden objective integrated at Stage 1 as a scalarized criterion alongside phase stability and crack resistance.
4. **BOFN integration:** AM Module outputs map to the 9-node DAG: melt pool geometry → Node 2 (energy delivery), process maps → Node 3 (scan strategy), G/R + equiaxed transition → Node 4 (thermal management). Proposed new Node 0.5 (AM Printability) as second computational filter before experiments. Mineral-burden as Node 0 multi-objective criterion.
5. **Absorptivity calibration as Month 1–2 deliverable:** Print 5–10 single tracks with AlSi10Mg (baseline), cross-section, compare to AM Module predictions — concrete early result that also generates data valuable to Thermo-Calc. Al-Zr alloys will require separate calibration due to different oxide behavior and solidification characteristics. Preliminary AM Module simulations from TC are in hand to anchor these comparisons.
6. **License budget:** to be set from a Thermo-Calc quote.
7. **Open-source value gap:** pycalphad/OpenCalphad handle phase equilibria identically, but melt pool simulation, process maps, absorptivity prediction, and equiaxed transition modeling have NO open-source equivalent.

#### Edison Scientific Analysis — Topic 3B CALPHAD Strategy (task `1e432b28`)

Key findings from Edison ANALYSIS reframing the CALPHAD strategy for Topic 3B (Critical Minerals). Full analysis in `edison-trajectories/thermocalc_3b_calphad_strategy.md`.

**CALPHAD screening criteria for Al-Zr/Al-Mn-Cr-Zr:**
- **Key phases to screen:** L1₂-Al₃Zr (metastable, provides coherent precipitation strengthening), D0₂₃-Al₃Zr (equilibrium), Al₆Mn (orthorhombic), Al₁₂Mn (icosahedral/quasicrystal precursor), Al₁₃Cr₂, Al₄₅Cr₇. These differ fundamentally from the Al-Si eutectic + Mg₂Si phases in Al-Si-Mg systems.
- **Screening criteria:** (1) Solidification range (liquidus–solidus gap) for crack susceptibility, (2) Volume fraction of strengthening precipitates (L1₂-Al₃Zr), (3) Freezing range and Scheil crack susceptibility index, (4) Absence of deleterious intermetallics (coarse Al₆Mn), (5) **Mineral-burden score** (weighted critical mineral content).
- **Mineral-burden formulation:** `MB = Σᵢ wᵢ · xᵢ` where wᵢ = USGS supply risk weight for element i, xᵢ = mole fraction. Multi-objective: minimize MB while maximizing predicted yield strength proxy and minimizing crack susceptibility. This is unique to Topic 3B and has no competitor equivalent in published HT-CALPHAD screening.

**Database assessment:**
- Free TDBDB coverage for Al-Zr binary is good (multiple assessed TDBs available). Al-Mn, Al-Cr binaries also covered. However, Al-Mn-Cr and Al-Zr-Mn ternaries have limited free coverage, and quaternary Al-Zr-Mn-Cr requires TCAl10 for consistent predictions.
- **TCAl10 is essential** for the multicomponent screening stage — free TDBs cannot be combined across papers for quaternary+ systems.

**Key differences from Al-Si-Mg:**
- Al-Zr alloys have a PERITECTIC solidification path (not eutectic like Al-Si). This changes the Scheil simulation behavior and crack susceptibility predictions.
- Zr has very low solubility in Al (~0.28 wt% at peritectic, ~0.01 wt% at room temperature). LPBF rapid solidification can extend this dramatically — CALPHAD equilibrium predictions need to be complemented with Scheil non-equilibrium calculations.
- Al-Mn forms complex intermetallic sequences that are more sensitive to database accuracy than Al-Si eutectic.

**Thermo-Calc collaboration for 3B:**
- **Letter of collaboration** emphasizes: (1) AM Module enables critical mineral substitution by predicting printability of novel Zr/Mn/Cr-containing Al alloys that have NO published LPBF parameter windows, (2) reciprocal value — BYU provides first systematic Al-Zr LPBF melt pool validation data for TC, (3) AMMTO mission alignment — reducing supply chain vulnerability of structural Al alloys.
- Thermo-Calc has already provided AM Module simulations as preliminary results and BYU has run TC-Python CALPHAD simulations on BYU's HPC clusters.
- AM Module demo includes Al-Zr composition alongside AlSi10Mg baseline to demonstrate relevance to Topic 3B.

---

## Overview of Approaches

CALPHAD calculations are **embarrassingly parallel** — each composition–temperature equilibrium is an independent Gibbs energy minimization requiring no inter-task communication (Roos & Zietsman 2022; Kwon et al. 2024). This makes them ideal for HPC.

| Framework | CALPHAD Engine | Parallelization | Scale Demonstrated | License |
|---|---|---|---|---|
| **pycalphad + joblib** | pycalphad | `multiprocessing.Pool` / joblib | Single-node, ~10K calcs | MIT (free) |
| **pycalphad + Dask** | pycalphad | `dask.distributed` + SLURM | Multi-node cluster | MIT (free) |
| **Equilipy** | Equilipy (Fortran) | Built-in MPI via `mpi4py` | 8,096 calcs benchmarked | Open-source |
| **MaterialsMap** | pycalphad / TC macros | `multiprocessing.Pool` | Ternary grids (903 pts) | Open-source |
| **exaPD** | pycalphad + LAMMPS | Parsl + SLURM executors | Exascale HPC | Open-source |
| **CAROUSEL** | MatCalc (extensible) | Threaded workers + SQL | 1,000–3,000 Scheil cases | Open-source |
| **Malac-Distmas** | Pandat / TC / pycalphad | Server–client + SQL + ANN | 10K+ tasks distributed | Open-source |
| **TC-Python batch** | Thermo-Calc | Python `multiprocessing` | 450K compositions | Commercial |
| **TC-Python + DNN surrogate** | Thermo-Calc (training) | ML inference | 2 billion compositions | Commercial+ML |

---

## Open-Source: pycalphad

[pycalphad](https://pycalphad.org/) (Otis & Liu 2017, 195 citations) is the leading open-source Python CALPHAD library. Key features for HT:

- **Vectorized inputs**: `equilibrium()` accepts multi-dimensional arrays, computing many T/X points in a single call
- **xarray outputs**: Results as labeled datasets for direct integration with pandas/matplotlib/scikit-learn
- **Symbolic models**: Customizable phase models via SymPy — models can be subclassed and overridden at runtime
- **Dask dependency**: Listed as a dependency, positioning it for distributed computation
- **ESPEI integration**: Automated parameter fitting with Bayesian MCMC for building thermodynamic descriptions

### Example 1: Parallel Screening with joblib

Screens Al-Cu-Mg ternary compositions for solidus temperature using the free COST507 database:

```python
"""
High-throughput equilibrium screening with pycalphad + joblib.
Screens Al-Cu-Mg ternary compositions for solidus temperature.

Refs: MaterialsMap pattern (Sun et al. 2024, Materialia),
      pycalphad HT modeling (Otis & Liu 2017, JOM)
"""
import numpy as np
from pycalphad import Database, equilibrium
from pycalphad import variables as v
from joblib import Parallel, delayed
import json
import os

# Load database (COST507 is freely available for Al alloys)
DB_PATH = "cost507R.tdb"
COMPONENTS = ["AL", "CU", "MG", "VA"]
PHASES = ["LIQUID", "FCC_A1", "HCP_A3", "THETA"]

# Cache the Database once per worker process to avoid repeatedly
# parsing the TDB file inside each task.
_DBF = None


def get_database():
    global _DBF
    if _DBF is None:
        _DBF = Database(DB_PATH)
    return _DBF


def calc_solidus(comp_al, comp_cu, temp_range):
    """Calculate solidus temperature for a given Al-Cu-Mg composition."""
    comp_mg = 1.0 - comp_al - comp_cu
    if comp_mg < 0 or comp_mg > 1:
        return None

    dbf = get_database()
    try:
        result = equilibrium(
            dbf, COMPONENTS, PHASES,
            {
                v.X("CU"): comp_cu,
                v.X("MG"): comp_mg,
                v.T: temp_range,
                v.P: 101325,
                v.N: 1.0,
            }
        )
        # Extract Gibbs energy — keep outputs minimal for IPC efficiency
        gm = float(result.GM.values.squeeze().min())
        return {
            "Al": float(comp_al),
            "Cu": float(comp_cu),
            "Mg": float(comp_mg),
            "GM_min": gm,
        }
    except Exception as e:
        return {"Al": float(comp_al), "Cu": float(comp_cu), "error": str(e)}


def main():
    # Generate composition grid
    cu_range = np.linspace(0.01, 0.30, 30)
    mg_range = np.linspace(0.01, 0.15, 15)
    temp_range = np.arange(400, 950, 5)  # K

    compositions = []
    for cu in cu_range:
        for mg in mg_range:
            al = 1.0 - cu - mg
            if al > 0:
                compositions.append((al, cu, temp_range))

    # Adjust n_jobs to match SLURM allocation
    n_jobs = int(os.environ.get("SLURM_CPUS_PER_TASK", 8))
    print(f"Running {len(compositions)} calculations on {n_jobs} cores...")

    results = Parallel(n_jobs=n_jobs, verbose=10)(
        delayed(calc_solidus)(al, cu, temps)
        for al, cu, temps in compositions
    )

    valid_results = [r for r in results if r is not None and "error" not in r]
    with open("solidus_screening_results.json", "w") as f:
        json.dump(valid_results, f, indent=2)
    print(f"Completed: {len(valid_results)}/{len(compositions)} calculations")


if __name__ == "__main__":
    main()
```

### Example 2: Dask for Multi-Node Distributed Computing

Using [dask-jobqueue](https://jobqueue.dask.org/) to scale across an entire SLURM cluster:

```python
"""
Distributed CALPHAD screening with pycalphad + Dask on SLURM.
Scales across multiple nodes automatically.

Refs: Dask patterns analogous to BigChem (Hicks & Martinez 2024);
      pycalphad lists Dask as dependency (Otis & Liu 2024)
"""
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import dask.bag as db
import numpy as np
from pycalphad import Database, equilibrium
from pycalphad import variables as v


# Cache the Database once per worker process to avoid repeatedly
# parsing the TDB file inside each task.
_DBF = None


def get_database():
    global _DBF
    if _DBF is None:
        _DBF = Database("cost507R.tdb")
    return _DBF


def compute_equilibrium(params):
    """Worker function: compute equilibrium for one composition."""
    comp_cu, comp_mg, temperature = params
    dbf = get_database()
    components = ["AL", "CU", "MG", "VA"]
    phases = ["LIQUID", "FCC_A1", "HCP_A3", "THETA"]

    try:
        result = equilibrium(
            dbf, components, phases,
            {v.X("CU"): comp_cu, v.X("MG"): comp_mg,
             v.T: temperature, v.P: 101325, v.N: 1.0}
        )
        gm = float(result.GM.values.squeeze())
        return {"Cu": comp_cu, "Mg": comp_mg, "T": temperature, "GM": gm}
    except Exception as e:
        return {"Cu": comp_cu, "Mg": comp_mg, "T": temperature, "error": str(e)}


def main():
    cluster = SLURMCluster(
        queue="compute",
        cores=16,
        memory="32GB",
        walltime="02:00:00",
        processes=16,
        local_directory="/tmp",
        job_extra_directives=[
            "--partition=compute",
            "--account=my_allocation",
        ],
    )
    cluster.scale(jobs=10)  # 10 SLURM jobs = 160 workers
    client = Client(cluster)
    print(f"Dashboard: {client.dashboard_link}")

    # Generate parameter grid
    cu_vals = np.linspace(0.01, 0.40, 40)
    mg_vals = np.linspace(0.01, 0.20, 20)
    temps = np.arange(500, 1200, 25)

    params = [
        (cu, mg, t)
        for cu in cu_vals for mg in mg_vals for t in temps
        if cu + mg < 0.99
    ]
    print(f"Total calculations: {len(params)}")

    bag = db.from_sequence(params, npartitions=160)
    results = bag.map(compute_equilibrium).compute()

    import json
    valid = [r for r in results if "error" not in r]
    with open("dask_calphad_results.json", "w") as f:
        json.dump(valid, f, indent=2)
    print(f"Completed: {len(valid)}/{len(params)}")

    client.close()
    cluster.close()


if __name__ == "__main__":
    main()
```

### Example 3: SLURM Job Array Pattern

The most robust approach for HPC — SLURM handles parallelism, fault tolerance comes naturally:

**`submit_calphad_array.sh`:**
```bash
#!/bin/bash
#SBATCH --job-name=calphad_screen
#SBATCH --output=calphad_%A_%a.out
#SBATCH --error=calphad_%A_%a.err
#SBATCH --array=0-99              # 100 independent tasks
#SBATCH --cpus-per-task=4         # 4 cores per task for joblib
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --partition=compute

module load anaconda3
conda activate calphad_env

python calphad_worker.py \
    --task-id $SLURM_ARRAY_TASK_ID \
    --total-tasks $SLURM_ARRAY_TASK_COUNT \
    --output-dir results/
```

**`calphad_worker.py`:**
```python
"""
SLURM array worker: processes a subset of the composition grid.

Refs: exaPD SLURM pattern (Zhang et al. 2025);
      TC-Python HT screening (Zhang et al. 2022; Ghassemali & Conway 2022)
"""
import argparse
import json
import os
import numpy as np
from pycalphad import Database, equilibrium
from pycalphad import variables as v
from joblib import Parallel, delayed


def generate_composition_grid():
    """Generate full composition grid (shared across all workers)."""
    cu_vals = np.linspace(0.01, 0.40, 50)
    mg_vals = np.linspace(0.01, 0.20, 25)
    temps = [600, 700, 800, 900, 1000, 1100]  # K
    grid = [
        (float(cu), float(mg), float(t))
        for cu in cu_vals for mg in mg_vals for t in temps
        if cu + mg < 0.95
    ]
    return grid


# Cache the Database once per worker process to avoid repeatedly
# parsing the TDB file inside each task.
DB_PATH = "cost507R.tdb"
_DBF = None


def get_database():
    global _DBF
    if _DBF is None:
        _DBF = Database(DB_PATH)
    return _DBF


def compute_one(cu, mg, t):
    """Compute equilibrium for one condition."""
    dbf = get_database()
    components = ["AL", "CU", "MG", "VA"]
    phases = ["LIQUID", "FCC_A1", "HCP_A3", "THETA"]
    try:
        result = equilibrium(
            dbf, components, phases,
            {v.X("CU"): cu, v.X("MG"): mg, v.T: t, v.P: 101325, v.N: 1.0}
        )
        return {
            "Cu": cu, "Mg": mg, "T": t,
            "GM": float(result.GM.values.squeeze()),
        }
    except Exception as e:
        return {"Cu": cu, "Mg": mg, "T": t, "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", type=int, required=True)
    parser.add_argument("--total-tasks", type=int, required=True)
    parser.add_argument("--output-dir", type=str, default="results")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    grid = generate_composition_grid()
    chunk = grid[args.task_id :: args.total_tasks]
    print(f"Task {args.task_id}: processing {len(chunk)}/{len(grid)} calculations")

    n_jobs = int(os.environ.get("SLURM_CPUS_PER_TASK", 4))
    results = Parallel(n_jobs=n_jobs)(
        delayed(compute_one)(cu, mg, t) for cu, mg, t in chunk
    )

    outfile = os.path.join(args.output_dir, f"results_{args.task_id:04d}.json")
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Task {args.task_id}: saved {len(results)} results to {outfile}")


if __name__ == "__main__":
    main()
```

**`merge_results.py`** (run after all array tasks complete):
```python
"""Merge results from all SLURM array tasks into a single file."""
import glob
import json

all_results = []
for path in sorted(glob.glob("results/results_*.json")):
    with open(path) as f:
        all_results.extend(json.load(f))

valid = [r for r in all_results if "error" not in r]
print(f"Total: {len(all_results)}, Valid: {len(valid)}, Errors: {len(all_results) - len(valid)}")

with open("all_calphad_results.json", "w") as f:
    json.dump(valid, f, indent=2)
```

### Example 4: MPI with mpi4py

For true multi-node parallelism with minimal overhead (inspired by Equilipy and Roos & Zietsman 2022):

```python
"""
MPI-based parallel CALPHAD screening.
Run with: mpirun -np 16 python mpi_calphad.py

Refs: Equilipy equilib_batch (Kwon et al. 2024, JOSS);
      MPI equilibrium scaling (Roos & Zietsman 2022)
"""
from mpi4py import MPI
from pycalphad import Database, equilibrium
from pycalphad import variables as v
import json

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    comps = [
        {"AL": xa, "CU": xb, "MG": 1 - xa - xb}
        for xa in [i * 0.05 for i in range(1, 19)]
        for xb in [j * 0.05 for j in range(1, 19)]
        if xa + xb < 0.95
    ]
    temps = [800, 900, 1000, 1100]
    tasks = [(c, t) for c in comps for t in temps]
    chunks = [tasks[i::size] for i in range(size)]
else:
    chunks = None

my_tasks = comm.scatter(chunks, root=0)

dbf = Database("cost507R.tdb")
my_results = []
for comp, t in my_tasks:
    try:
        result = equilibrium(
            dbf, ["AL", "CU", "MG", "VA"],
            ["LIQUID", "FCC_A1", "HCP_A3"],
            {v.X("CU"): comp["CU"], v.X("MG"): comp["MG"],
             v.T: t, v.P: 101325, v.N: 1.0}
        )
        my_results.append({
            "comp": comp, "T": t,
            "GM": float(result.GM.values.squeeze()),
            "rank": rank,
        })
    except Exception as e:
        my_results.append({"comp": comp, "T": t, "error": str(e), "rank": rank})

all_results = comm.gather(my_results, root=0)
if rank == 0:
    flat = [r for sub in all_results for r in sub]
    with open("mpi_calphad_results.json", "w") as f:
        json.dump(flat, f, indent=2)
    valid = [r for r in flat if "error" not in r]
    print(f"Completed: {len(valid)}/{len(flat)} on {size} ranks")
```

---

## Open-Source: Equilipy

[Equilipy](https://doi.org/10.21105/joss.06875) (Kwon et al. 2024) is a newer open-source alternative specifically designed for HT-CALPHAD with **built-in parallel computation**:

- **Core**: Fortran equilibrium solver interfaced with Python via F2PY
- **Parallelism**: Built-in `equilib_batch()` distributes work via `mpi4py`
- **No license limits**: Unlike TC-Python's 32-processor cap, Equilipy scales freely
- **Performance**: Benchmarked on 8,096 equilibrium calculations with speeds comparable to TC-Python and PanPython
- **HPC-native**: Designed for Linux-based HPC clusters

```python
# Equilipy batch calculation (built-in parallelism)
from equilipy import equilib_batch

# Automatically distributes across all available MPI processes
results = equilib_batch(
    database="cost507.tdb",
    conditions=conditions_array,  # array of (T, P, compositions)
)
```

---

## Commercial: Thermo-Calc TC-Python

[TC-Python](https://thermocalc.com/products/software-development-kits/tc-python/) provides access to Thermo-Calc's assessed commercial databases (TCFE, TCNI, TCHEA, etc.) with a scripting API.

### Batch Equilibrium Example

```python
"""
High-throughput screening with TC-Python batch equilibrium.
Screens Fe-Cr-Ni compositions for phase stability.

Refs: Sundar et al. 2025 (J Mater Res); Vary 2023;
      Wang & Xiong 2020 (npj Comput Mater)
"""
from tc_python import *
import numpy as np
import csv


def main():
    with TCPython() as session:
        system = (
            session
            .select_database_and_elements("TCFE12", ["Fe", "Cr", "Ni"])
            .get_system()
        )

        batch_calc = system.with_batch_equilibrium_calculation()

        cr_vals = np.linspace(0.05, 0.30, 26)
        ni_vals = np.linspace(0.05, 0.25, 21)
        temperature = 1073.15  # 800°C

        calc_id = 0
        calc_id_to_comp = {}  # Track actual compositions per calc_id
        for cr in cr_vals:
            for ni in ni_vals:
                if cr + ni < 0.95:
                    batch_calc.set_condition_for_calculation(
                        calc_id,
                        ThermodynamicQuantity.temperature(), temperature,
                    )
                    batch_calc.set_condition_for_calculation(
                        calc_id,
                        ThermodynamicQuantity.mole_fraction_of_a_component("Cr"), cr,
                    )
                    batch_calc.set_condition_for_calculation(
                        calc_id,
                        ThermodynamicQuantity.mole_fraction_of_a_component("Ni"), ni,
                    )
                    calc_id_to_comp[calc_id] = (float(cr), float(ni))
                    calc_id += 1

        print(f"Running {calc_id} batch equilibrium calculations...")
        batch_result = batch_calc.calculate()

        with open("tc_batch_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["calc_id", "Cr", "Ni", "GM", "stable_phases"])
            for i in range(calc_id):
                cr, ni = calc_id_to_comp[i]
                try:
                    gm = batch_result.get_value_of(
                        i, ThermodynamicQuantity.gibbs_energy_of_a_phase("*")
                    )
                    phases = batch_result.get_stable_phases(i)
                    writer.writerow([i, cr, ni, gm, ";".join(phases)])
                except Exception as e:
                    writer.writerow([i, cr, ni, "", f"error: {e}"])

        print(f"Results saved to tc_batch_results.csv")


if __name__ == "__main__":
    main()
```

### TC-Python with SLURM

```bash
#!/bin/bash
#SBATCH --job-name=tc_python_ht
#SBATCH --output=tc_python_%A_%a.out
#SBATCH --array=0-19
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --partition=compute

# TC-Python requires license server access
export TC_LICENSE_FILE=27007@license-server.university.edu
export TC_INSTALL_DIR=/opt/thermocalc/2024b

module load anaconda3
conda activate tc_python_env

python tc_python_worker.py \
    --task-id $SLURM_ARRAY_TASK_ID \
    --total-tasks $SLURM_ARRAY_TASK_COUNT
```

### Licensing Constraints

> **Critical finding from Edison Scientific literature search**: TC-Python permits only **up to 32 logical processors per license** (Kwon et al. 2024). This is the primary motivation for open-source alternatives.

| Aspect | Details |
|---|---|
| **Processor cap** | 32 logical processors per TC-Python license |
| **License type** | Network license (FlexLM) required for HPC |
| **SDK license** | Separate from base Thermo-Calc installation |
| **MATLAB SDK** | Requires additional MATLAB license |
| **Failure rate** | ~5% of calculations may fail (Sundar et al. 2025) |
| **Recommendation** | Use pycalphad/Equilipy for preliminary screening; TC-Python for refined predictions on shortlisted candidates |

---

## Dedicated HT-CALPHAD Frameworks

Several purpose-built frameworks exist for orchestrating large-scale CALPHAD campaigns:

### Malac-Distmas (Gao et al. 2022, 57 citations)
Server–client distributed task management system for HT-CALPHAD:
- SQL-backed task queue with status tracking (created → downloaded → executing → completed/failed)
- Load balancing across heterogeneous compute resources
- Fault tolerance with automatic retry of failed tasks
- **ANN densification**: Embedded neural network predicts intermediate results, reducing total CALPHAD runs needed
- Supports TC (via TCM batch files), Pandat (PBFX), and pycalphad
- Demonstrated: 10,201 diffusion tasks in 4.4 hours; 101 precipitation tasks in 24 minutes

### CAROUSEL (Ständer et al. 2023)
Open-source framework for HT microstructure simulations:
- SQL-backed data management with GUI
- Threaded worker distribution
- Supports equilibrium, Scheil, and precipitation kinetics
- Demonstrated: 1,000–3,000 Scheil cases with strong/weak scaling analysis
- Extensible to different CALPHAD implementations (demonstrated with MatCalc)

### exaPD (Zhang et al. 2025)
Exascale-ready workflow for phase diagram construction:
- Uses [Parsl](https://parsl-project.org/) as global task controller with `SlurmProvider`
- `@python_app` task decorators with futures-based dependency management
- Heterogeneous CPU/GPU scheduling with separate executors
- **Resumable workflows**: Per-task "DONE" markers allow interrupted runs to continue
- Near-ideal scaling demonstrated on HPC

### MaterialsMap (Sun et al. 2024, 10 citations)
CALPHAD-based tool for composition pathway design:
- Auto-generates composition grids for ternary/higher-order systems
- Uses `multiprocessing.Pool` for parallel pycalphad/Scheil calculations
- Built-in feasibility/crack susceptibility mapping

---

## ML Surrogates for Extreme Throughput

When screening beyond ~10⁵ compositions, **ML surrogate models trained on CALPHAD data** provide orders-of-magnitude speedup:

| Study | Training Data | Surrogate | Screening Scale | Speedup |
|---|---|---|---|---|
| Vazquez et al. 2023 (31 cit.) | TC-Python (Al-Co-Cr-Fe-Mn-Nb-Ni) | Deep Neural Network | 500K+ compositions | R² > 0.96 |
| Wang et al. 2025 (1 cit.) | TC-Python (Ni superalloys, 750K points) | ML models | **2 billion** compositions | Days → minutes |
| Gao et al. 2022 (57 cit.) | Malac-Distmas outputs | ANN densification | Interpolation of gaps | ~10× fewer CALPHAD runs |

**Workflow**: Generate 10K–100K high-quality CALPHAD training points → Train DNN/GP surrogate → Screen millions of candidates via inference → Validate top candidates with full CALPHAD.

---

## Published Large-Scale Screening Examples

*Source: Edison Scientific LITERATURE_HIGH search*

| Reference | Alloy System | Compositions | Methods | Parallelization | Key Results |
|---|---|---|---|---|---|
| Wang & Xiong 2020 (73 cit.) | HSLA-115 steel | **450,000** | Equilibrium + ICME models | TC-Python batch + surrogates | Optimized success probability from 55.3% → 99.996% for AM builds |
| Wang et al. 2025 (1 cit.) | Ni superalloys | **150,000** (→2B via ML) | Equilibrium at multiple T | TC-Python (TCNI12), ~11 days direct | ML screened 2B compositions → 228 candidates |
| Vary 2023 | Cr-Fe-Ni-Mo-Ti | **65,568** | Point equilibria (2 databases) | TC batch mode from CSV | No SDK license needed; tiled 2D visualization |
| Sundar et al. 2025 (7 cit.) | Ni-Cr-Co-Al-Fe | **~2,000** (1,889 retrieved) | Phase diagrams, Scheil, CTE, diffusivities | Python multiprocessing + TC-Python on HPC | Bayesian optimization explored only 7% of space |
| Ghassemali & Conway 2022 (26 cit.) | General review | N/A | Solidus/solvus, phase fractions, lattice params | TC-Python automated batch | "Islands of interest" rapid scanning strategy |
| Zhang et al. 2022 (11 cit.) | Al-Mg-Zn-Cu | Systematic grid | Eutectic identification | TC-Python loop (serial) | Found quaternary eutectic; Tmax=2500K cap needed |
| Zhang et al. 2019 (32 cit.) | 6016 Al-alloys | **6,016** | Equilibrium solidification | pycalphad + COST507 | Validated HT screening of Al alloys |

---

## Free Thermodynamic Databases

*Source: Edison Scientific literature search — TDBDB indexes 766+ TDB files from 528 publications*

| Database | System Coverage | URL/Source | Notes |
|---|---|---|---|
| **COST 507** | Al-based, Mg-based, Ti-based light alloys | [NIST Materials Data Repository](https://materialsdata.nist.gov/dspace/xmlui/handle/11256/618) | European COST Action 507; validated for HT screening of 6016 Al-alloys (Zhang et al. 2019) |
| **TDBDB** | 766+ TDB files from literature | [avdwalle.github.io/tdbdb](https://avdwalle.github.io/tdbdb/) | Indexed search engine for TDB files (van de Walle et al. 2018, 52 cit.) |
| **SGTE Pure Elements** | Unary reference data | [sgte.net](https://www.sgte.net/) | Foundation for all multicomponent CALPHAD; Dinsdale (1991) |
| **MatCalc Open DBs** | Al, Fe, Ni systems | [matcalc.at](https://www.matcalc.at/index.php/databases/open-databases) | Open subset of MatCalc databases |
| **OpenCalphad** | Test databases | [opencalphad.com](http://www.opencalphad.com) | GNU license; includes Python interface (Sundman et al. 2015, 198 cit.) |
| **NIST Solder Database** | Pb-free solder alloys | NIST Materials Data Repository | Focused on solder systems |
| **Widom Alloy Database** | Various alloy systems | NIST Repository | Community-contributed alloy data |
| **pycalphad examples** | Al-Fe (subset of COST507) | [github.com/pycalphad](https://github.com/pycalphad/pycalphad) | `alfe_sei.TDB` and other tutorial files |

---

## Best Practices

Based on the Edison Scientific literature analysis:

1. **Minimize per-task I/O**: Store only essential results (phase fractions, Gibbs energy, key temperatures) to reduce serialization overhead (Hicks & Martinez 2024)

2. **Use coarse-then-fine scanning**: Rapid coarse scans over full composition space → refine in promising regions. Reduces total calculations by orders of magnitude (Ghassemali & Conway 2022)

3. **Implement fault tolerance**: Completion markers (DONE files), database-backed storage, or job-retry mechanisms for resumable workflows (Gao et al. 2022; Zhang et al. 2025)

4. **Manage temperature bounds**: Set upper limits (e.g., 2,500 K) to prevent unphysical Gibbs energy extrapolations (Zhang et al. 2022)

5. **Couple with ML surrogates**: ANN/DNN models trained on CALPHAD outputs interpolate gaps and extend screening to billions of compositions (Vazquez et al. 2023; Wang et al. 2025)

6. **Process-based parallelism**: Python's GIL means thread-based parallelism provides limited benefit. Use `multiprocessing`, joblib with `backend='loky'`, or Dask with `scheduler='processes'` (Sun et al. 2024)

7. **Account for licensing**: TC-Python: 32-processor cap per license. Use open-source alternatives (pycalphad, Equilipy) for embarrassingly parallel scaling; TC-Python for refined predictions (Kwon et al. 2024)

---

## Architecture Patterns for BYU VCL (Topic 3B — Critical Minerals)

### Recommended: Three-Stage Funnel for Mineral-Efficient Alloy Discovery

```
Stage 1: pycalphad + TDBDB/COST507 TDB (free, unlimited parallelism)
  → SLURM job array on BYU supercomputer (100-1000 tasks)
  → Screen 100,000+ Al-Zr and Al-Mn-Cr-Zr compositions
  → Criteria: solidification range, L1₂-Al₃Zr precipitate fraction,
    Scheil crack susceptibility, mineral-burden score
  → Filter to top 1,000 candidates

Stage 2: TC-Python + TCAl10 (commercial, assessed DB — essential for quaternary+)
  → Refine multicomponent predictions on Al-Zr-Mn-Cr shortlist
  → Full Scheil solidification with reliable ternary/quaternary interactions
  → Compute diffusion coefficients, microsegregation, crack susceptibility index
  → Filter to top 50–100 candidates

Stage 3: TC AM Module (commercial add-on — simulations already provided by TC as preliminary results)
  → Printability maps (power vs. speed) for shortlisted compositions
  → Melt pool geometry, G/R, equiaxed-to-columnar transition
  → Generate final candidate list (~10–20 for experimental validation)
  → Note: Al-Zr alloys have PERITECTIC solidification — different defect
    boundaries than eutectic Al-Si systems

Stage 4 (optional): ML surrogate for >100K scale
  → Train DNN on Stage 1/2 outputs
  → Screen millions of compositions via inference
  → Include mineral-burden as surrogate output
```

**Mineral-burden objective (unique to Topic 3B):** At Stage 1, each composition is scored with `MB = Σᵢ wᵢ · xᵢ` where wᵢ is the USGS supply risk weight for element i and xᵢ is the mole fraction. The screening filter minimizes MB while maximizing predicted strengthening phase fraction and minimizing crack susceptibility — a multi-objective criterion that no published HT-CALPHAD screening study has implemented.

### Scaling Estimates

| Configuration | Calcs/Hour | Notes |
|---|---|---|
| pycalphad, 1 core | ~600–3,000 | Depends on system complexity |
| pycalphad, 16 cores (1 node) | ~8,000–40,000 | Near-linear scaling |
| pycalphad, 100 nodes × 16 cores | ~500K–2M | SLURM job array |
| Equilipy, MPI multi-node | Similar to pycalphad | Built-in parallelism, no license limit |
| TC-Python batch, 1 session | ~1,000–5,000 | Optimized batch mode |
| TC-Python, 20 SLURM jobs | ~20K–100K | License-limited (32 proc/license) |
| ML surrogate (inference) | ~10M+ | After training on CALPHAD data |

### Immediate Next Steps for BYU VCL (Topic 3B)

**Genesis Mission Partnership Structure:**
- **Letters of Collaboration (3):** Valimet (gas atomization), AMAZEMET (ultrasonic atomization — atomizer installed at BYU), Thermo-Calc (CALPHAD/AM Module — simulations running on BYU HPC)
- **Letters of Support (8):** Ames National Lab, Fehrmann Alloys, Taylor Sparks (U of Utah), Ashley Speer, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, Keith Brown

**Preliminary Results In Hand:**
- ✅ AMAZEMET ultrasonic atomizer installed at BYU
- ✅ AlSi10Mg tensile specimen printed at University of Utah (Taylor Sparks)
- ✅ Tensile data for the U of Utah AlSi10Mg specimen
- ✅ AlSi10Mg tensile specimen from 3D Powder Tech
- ✅ SEM and EDS for precursor powders (AlSi10Mg, Si powder) and the AMAZEMET-atomized mixture (composition change via Al wire + Si addition)
- ✅ High-temperature tensile data using a standard aluminum tensile specimen
- ✅ Thermo-Calc AM Module simulations provided by TC for BYU
- ✅ Thermo-Calc CALPHAD simulations running on BYU's HPC clusters
- ✅ Full pKGFN pipeline implementation (BoTorch 0.12+)
- ✅ Automated powder dispensing demonstration

**Remaining CALPHAD-Specific Steps:**

1. **Expand pycalphad screening** on BYU's [supercomputer](https://rc.byu.edu/) — scale from demo 600-calc runs to 10K+ Al-Zr and Al-Mn-Cr-Zr compositions using the SLURM job array pattern (Example 3 above)
2. **Search TDBDB** ([avdwalle.github.io/tdbdb](https://avdwalle.github.io/tdbdb/)) for Al-Zr, Al-Mn, Al-Cr, and Al-Zr-Mn TDB files — verify coverage of key binaries/ternaries for the target composition spaces
3. **Download COST507** from [NIST](https://materialsdata.nist.gov/dspace/xmlui/handle/11256/618) as supplemental database for Al alloy baseline screening
4. **Refine mineral-burden scoring function** — implement `MB = Σᵢ wᵢ · xᵢ` with USGS supply risk weights for Mg, Sc, REE elements; integrate as pycalphad post-processing filter
5. **Finalize TCAl10 pricing** with Thermo-Calc for Stage 2 multicomponent refinement (quote pending)
6. **Integrate AM Module results** into the three-stage funnel demonstration — use the simulations already provided by Thermo-Calc as Stage 3 proof-of-concept

### Compelling Visualizations for Genesis Mission Proposal (Topic 3B)

Based on Edison Scientific analysis (task `8028123c`, 24K chars, `edison-trajectories/calphad_visualization_recommendations.md`) reviewing published HT-CALPHAD visualization approaches and critical minerals proposal requirements:

#### Recommended 3-Figure Layout (fits ~1.5 pages of the 5-page proposal)

| Figure | Content | Generate Now? | Why It Works for DOE/AMMTO |
|---|---|---|---|
| **Fig. 1** | **(a)** Screening funnel: 100K+ compositions → Stage 1 (pycalphad + MB filter) → 1K → Stage 2 (Scheil/TC-Python) → 50-100 → Stage 3 (AM Module) → final candidates. **(b)** Bayesian optimization closed-loop schematic linking CALPHAD screening → LPBF → tensile → next batch | Yes | Communicates scale, rigor, and autonomy in one glance. Parallels proven HT-CALPHAD funnels (Zhang et al. 2025, Hastings et al. 2024) |
| **Fig. 2** | **(a)** Mineral-Burden vs. Predicted Strength Pareto front: MB = Σᵢ wᵢ·xᵢ (x-axis) vs. L1₂-Al₃Zr volume fraction or solidus (y-axis), with Sc/REE-containing benchmark alloys annotated. **(b)** Mineral criticality bar chart comparing supply-risk weights (Sc: 4.6, REE: 3.1, Mg: 2.4 vs. Zr: ~1, Mn: 0.7, Cr: 1.1 — OECD data) | Yes | **FLAIME's most distinctive figure** — no published competitor has a mineral-burden Pareto front for alloy optimization. Makes supply-chain resilience a first-class design objective |
| **Fig. 3** | **(a)** Al-Zr binary phase diagram (Al-rich corner, pycalphad + COST507 TDB) showing peritectic topology and Al₃Zr stability fields. **(b)** Scheil solidification curves for 2-3 Al-Zr compositions (Al-0.5Zr, Al-1.0Zr, Al-1.5Zr wt%) showing freezing range and intermetallic onset. Optionally **(c)** pseudo-ternary heatmap slice in Al-Mn-Cr-Zr space colored by solidus or freezing range | Yes | Real preliminary data from actual pycalphad runs = immediate credibility. Combines equilibrium + non-equilibrium analysis |

#### Priority-Ranked Visualization Types

1. **Screening funnel diagram** — Annotate composition counts at each filter stage. Published precedent: Zhang et al. (2025) 160K→1.5K; Hastings et al. (2024) 53K→2.4K; Ghassemali & Conway (2022) "four distinct steps" to "islands of selected compositions."
2. **Mineral-burden Pareto front** — Plot MB vs. strength proxy. **Unique to FLAIME**: literature review confirms no published precedent for integrating USGS supply-risk weights into CALPHAD-based multi-objective optimization. Supply risk assessed at commodity level (USGS, OECD), but never used as forward design objective in CALPHAD screening.
3. **LPBF printability map** (power vs. scan speed, colored by defect regime) — Describe as proposed Stage 3 work. Published precedent: Sheikh et al. (2025) "printability index" = fraction of defect-free processing space. Strong AMMTO appeal because it ties chemistry to manufacturability.
4. **Al-Zr phase diagram** — Compute with pycalphad now. Shows metallurgical credibility and that team can generate real thermodynamic data with open tools. Precedent: Griffiths (2020) Scheil predictions showing primary Al₃Zr precipitation.
5. **Scheil solidification curves** — Compare Al-Zr compositions showing freezing range differences. Bridges equilibrium thermodynamics to LPBF non-equilibrium conditions. Use pycalphad `scheil` package (Bocklund et al. 2020).
6. **Composition-property heatmap** — Pseudo-ternary slices with mineral-burden contours overlaid on feasibility regions. Precedent: MaterialsMap tool (Sun et al. 2024) with 903-point ternary grids and 8 feasibility map types.
7. **Mineral criticality bar chart** — Supply-risk weights from OECD/USGS making critical minerals rationale legible to non-specialist reviewers.
8. **BO loop diagram** — Closed-loop cycle showing where MB and printability enter the acquisition function. Precedent: Hastings et al. (2024) multi-objective BO with hypervolume tracking.

#### What Can Be Generated NOW as Preliminary Results

Using pycalphad with free TDB databases (COST507, TDBDB), plus Thermo-Calc AM Module simulations already provided and BYU HPC CALPHAD runs already completed:

1. **Al-Zr binary phase diagram** — Al-rich corner showing peritectic and Al₃Zr fields (`pycalphad.equilibrium()` over composition-temperature grid)
2. **Scheil solidification curves** — `from scheil import simulate_scheil_solidification` for selected Al-Zr compositions
3. **Mineral-burden scatter plot** — MB = Σᵢ wᵢ·xᵢ computed for screened compositions vs. any thermodynamic property
4. **Composition-property heatmap** — Ternary slice colored by solidus, freezing range, or precipitate fraction
5. **Screening funnel mockup** — Based on actual pycalphad run counts from our live demos (600+ calculations demonstrated)
6. **Thermo-Calc AM Module printability predictions** — Simulations already provided by Thermo-Calc for AlSi10Mg baseline and Al-Zr candidates
7. **BYU HPC CALPHAD results** — TC-Python runs on BYU supercomputer demonstrating the full Stage 2 pipeline

#### What Makes the Mineral-Burden Pareto Front Novel

Edison literature review (24K chars, citing Coulomb 2015, Nassar 2020, Helbig 2020, Ferro 2020) confirms: supply risk has been assessed at the mineral commodity level by USGS and OECD, and Helbig et al. (2020) computed supply risk at the alloy level for Ni superalloys — but these are **retrospective assessments on existing alloys**, not forward design objectives in a CALPHAD screening pipeline. The FLAIME MB Pareto front is a genuinely novel contribution merging materials informatics with supply-chain resilience.

---

## References

### Open-Source Tools
- **pycalphad**: Otis & Liu (2017) "pycalphad: CALPHAD-based Computational Thermodynamics in Python" — *JORS*, [doi:10.5334/jors.140](https://doi.org/10.5334/jors.140) (195 citations)
- **Equilipy**: Kwon et al. (2024) "Equilipy: A Python Package for Calculating Phase Equilibria" — *JOSS*, [doi:10.21105/joss.06875](https://doi.org/10.21105/joss.06875)
- **ESPEI**: Otis & Liu (2017) "High-Throughput Thermodynamic Modeling and Uncertainty Quantification for ICME" — *JOM*, [doi:10.1007/s11837-017-2318-6](https://doi.org/10.1007/s11837-017-2318-6) (59 citations)
- **scheil package**: Bocklund et al. (2020) "Scheil-Gulliver Simulations for Functionally Graded Alloys by AM using pycalphad" — [arXiv:2001.11611](https://doi.org/10.48550/arxiv.2001.11611)
- **MaterialsMap**: Sun et al. (2024) "MaterialsMap: A CALPHAD-Based Tool to Design Composition Pathways" — *Materialia*, [doi:10.1016/j.mtla.2024.102153](https://doi.org/10.1016/j.mtla.2024.102153) (10 citations)
- **OpenCalphad**: Sundman et al. (2015) "OpenCalphad – A Free Thermodynamic Software" — *IMMI*, [doi:10.1186/s40192-014-0029-1](https://doi.org/10.1186/s40192-014-0029-1) (198 citations)

### HT Frameworks
- **Malac-Distmas**: Gao et al. (2022) "A Machine Learning Accelerated Distributed Task Management System" — *Adv Powder Mater*, [doi:10.1016/j.apmate.2021.09.005](https://doi.org/10.1016/j.apmate.2021.09.005) (57 citations)
- **CAROUSEL**: Ständer et al. (2023) "CAROUSEL: An Open-Source Framework for HT Microstructure Simulations" — *IMMI*, [doi:10.1007/s40192-023-00314-6](https://doi.org/10.1007/s40192-023-00314-6)
- **exaPD**: Zhang et al. (2025) "exaPD: A Highly Parallelizable Workflow for Multi-Element Phase Diagram Construction" — [arXiv:2510.01400](https://doi.org/10.48550/arxiv.2510.01400)

### Large-Scale Screening Studies
- Wang & Xiong (2020) "Uncertainty Quantification and Composition Optimization for Alloy AM through CALPHAD-based ICME" — *npj Comput Mater*, [doi:10.1038/s41524-020-00454-9](https://doi.org/10.1038/s41524-020-00454-9) (73 citations)
- Sundar et al. (2025) "CALPHAD-based Bayesian Optimization to Accelerate Alloy Discovery" — *J Mater Res*, [doi:10.1557/s43578-024-01489-0](https://doi.org/10.1557/s43578-024-01489-0) (7 citations)
- Vazquez et al. (2023) "A Deep Neural Network Regressor for Phase Constitution Estimation in HEAs" — *npj Comput Mater*, [doi:10.1038/s41524-023-01021-8](https://doi.org/10.1038/s41524-023-01021-8) (31 citations)
- Wang et al. (2025) "Multiscale Computational Framework Linking Alloy Composition to Microstructure via ML" — *npj Comput Mater*, [doi:10.1038/s41524-025-01730-2](https://doi.org/10.1038/s41524-025-01730-2)
- Ghassemali & Conway (2022) "High-Throughput CALPHAD: A Powerful Tool Towards Accelerated Metallurgy" — *Front Mater*, [doi:10.3389/fmats.2022.889771](https://doi.org/10.3389/fmats.2022.889771) (26 citations)

### Databases
- **TDBDB**: van de Walle et al. (2018) "The Thermodynamic Database Database" — *Calphad*, [doi:10.1016/j.calphad.2018.04.003](https://doi.org/10.1016/j.calphad.2018.04.003) (52 citations)
- **COST507**: Zhang et al. (2019) "High-Throughput Thermodynamic Calculations of Phase Equilibria in Solidified 6016 Al-Alloys" — *Comput Mater Sci*, [doi:10.1016/j.commatsci.2019.05.022](https://doi.org/10.1016/j.commatsci.2019.05.022) (32 citations)

### Parallelization & Scaling
- Roos & Zietsman (2022) "Accelerating Complex Chemical Equilibrium Calculations – A Review"
- Hicks & Martinez (2024) "Massively Scalable Workflows for Quantum Chemistry: BigChem and ChemCloud" — *J Chem Phys*, [doi:10.1063/5.0190834](https://doi.org/10.1063/5.0190834) (16 citations)
