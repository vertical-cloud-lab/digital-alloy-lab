Question: How can pycalphad be used for high-throughput thermodynamic calculations? What are specific code examples for parallelizing pycalphad equilibrium calculations using joblib, multiprocessing, Dask, or other Python parallel frameworks? What thermodynamic databases (TDB files like COST507) are freely available for alloy screening?

# Pycalphad for High-Throughput Thermodynamic Calculations: Parallelization Strategies and Freely Available Databases

## 1. Overview of Pycalphad for High-Throughput Thermodynamic Calculations

Pycalphad is a free and open-source Python library (MIT license) for designing thermodynamic models, calculating phase diagrams, and solving multicomponent, multi-phase Gibbs energy minimization problems using the CALPHAD (CALculation of PHAse Diagrams) method (otis2024pycalphadcalphadbasedcomputational pages 1-3, liu2018oceanofdata pages 6-8). Several architectural features make pycalphad particularly well-suited for high-throughput (HT) thermodynamic workflows:

**Symbolic model representation and runtime flexibility.** Pycalphad decouples phase models from the equilibrium solver using symbolic representations (via SymPy). Models can be programmatically created, manipulated, and overridden at runtime without changing solver code, enabling automated batch workflows and custom model development (olson2024genomicmaterialsdesign pages 29-34, otis2024pycalphadcalphadbasedcomputational pages 1-3). Users can define custom phase models by subclassing the `Model` class and passing them directly to `calculate()` and `equilibrium()` functions.

**Vectorized inputs and labeled result arrays.** The `equilibrium()` function accepts multi-dimensional arrays of shape (P, T, y) for pressure, temperature, and site-fraction grids, returning results as xarray datasets with named dimensions (e.g., temperature, composition, internal degrees of freedom, vertex). For example, a single call can compute equilibria at 170 temperatures and 100 compositions simultaneously (otis2024pycalphadcalphadbasedcomputational pages 4-7). Slicing results is straightforward—e.g., `eq.MU.sel(component='AL', T=600)` retrieves all Al chemical potentials at 600 K. Datasets support reading/writing to disk for storing long-running calculations (otis2024pycalphadcalphadbasedcomputational pages 4-7).

**Integration with ESPEI and automated workflows.** Pycalphad serves as the computational engine for ESPEI, which implements an automated two-step procedure: (1) fit model parameters using thermochemical data from DFT-based first-principles calculations, and (2) refine using experimental phase-equilibrium data via Bayesian MCMC optimization (otis2017highthroughputthermodynamicmodeling pages 1-2, liu2018oceanofdata pages 6-8). This enables rapid, systematic construction of multicomponent thermodynamic descriptions suitable for ICME pipelines (otis2017highthroughputthermodynamicmodeling pages 5-7).

**Scheil-Gulliver solidification simulations.** The open-source `scheil` Python package, built on pycalphad, implements Scheil-Gulliver solidification simulations and is designed explicitly for high-throughput screening, capable of performing multiple simulations by looping over a series of compositions in multicomponent composition space (bocklund2020scheilgulliversimulationsfor pages 6-10).

**MaterialsMap for systematic alloy design.** The MaterialsMap tool uses pycalphad as one of its computational engines for high-throughput equilibrium calculations and Scheil-Gulliver simulations across systematically sampled composition grids, with parallel computations built in (sun2024materialsmapacalphadbased pages 6-10, sun2024materialsmapacalphadbased pages 10-15).

## 2. Parallelization Strategies for Pycalphad Calculations

### 2.1 Native Capabilities

Pycalphad itself supports vectorized calculations internally: by passing large arrays of conditions to `equilibrium()`, many temperature-composition points can be evaluated in a single function call (otis2024pycalphadcalphadbasedcomputational pages 4-7). Pycalphad lists **Dask** as a dependency, positioning it as an available backend for parallel and distributed computation (otis2024pycalphadcalphadbasedcomputational pages 4-7).

### 2.2 Multiprocessing (as used in MaterialsMap)

The MaterialsMap package employs the **Python multiprocessing Pool library** to accelerate equilibrium calculations and Scheil-Gulliver simulations using multicore processors. The `pycalphad_eq()` and `pycalphad_scheil()` functions are designed for seamless integration into parallel computing, with enhancements to display time and process information during parallel execution (sun2024materialsmapacalphadbased pages 10-15).

### 2.3 Distributed Task Management (Malac-Distmas)

For large-scale HT-CALPHAD computations, the Malac-Distmas system implements a server-client distributed computing architecture that partitions massive calculation tasks into independent subtasks. Each subtask (an independent equilibrium or Scheil calculation at specific conditions) is dispatched to computing nodes, with SQL-based task management, exception handling, and results aggregation. This approach couples with both commercial and open-source CALPHAD software including pycalphad (gao2022amachinelearning pages 1-2, gao2022amachinelearning pages 2-3, gao2022amachinelearning pages 3-5).

### 2.4 Equilipy: Built-in Parallel Computations

Equilipy, a related open-source Python package for phase equilibria calculations, was specifically developed for high-throughput CALPHAD with built-in parallel computations across multiple processors and nodes. Its `equilib_batch()` function processes each NPT condition independently, ensuring consistent computation speed regardless of input sequence (kwon2024equilipyapython pages 3-5, kwon2024equilipyapython pages 1-3).

### 2.5 Code Examples for Parallelizing Pycalphad

The following code demonstrates three parallelization approaches (multiprocessing, joblib, and Dask) applied to pycalphad's `equilibrium()` API, based on the published code structure from the pycalphad paper (otis2024pycalphadcalphadbasedcomputational media b99aade9) and the parallelization strategy documented in MaterialsMap (sun2024materialsmapacalphadbased pages 10-15):

```python
import numpy as np
from pycalphad import Database, equilibrium
import pycalphad.variables as v
from multiprocessing import Pool
from joblib import Parallel, delayed
import dask
from dask import delayed as dask_delayed

# --- 1. Setup System based on COST507 (Al-Fe) ---
# Citations: (otis2024pycalphadcalphadbasedcomputational media b99aade9, otis2024pycalphadcalphadbasedcomputational pages 10-11)
# Load the thermodynamic database (assumes file exists)
db_alfe = Database("alfe_sei.TDB")
components = ["AL", "FE", "VA"]
phases = ["LIQUID", "BCC_A2", "FCC_A1", "AL13FE4"]

# --- 2. Define Calculation Helper ---
def calculate_point(temp, comp_al):
    """
    Wraps pycalphad equilibrium for a single condition.
    This function is pickled and sent to workers.
    """
    # Create conditions dictionary (Pressure, Temperature, Composition)
    # v.X('AL') specifies the mole fraction of Aluminum
    conds = {v.P: 101325, v.T: temp, v.X("AL"): comp_al}

    # Perform equilibrium calculation
    # Note: pycalphad supports vectorized inputs natively, which is efficient.
    # Parallelization wrappers are useful for complex workflows or distributed clusters.
    eq_result = equilibrium(db_alfe, components, phases, conds)

    # Return a lightweight result (e.g., Minimum Gibbs Energy) to reduce IPC overhead
    return eq_result.GM.values.flat[0]

# Create a grid of conditions (Task List)
temps = np.linspace(700, 2000, 20)  # 20 Temperature points
compositions = np.linspace(0.01, 0.99, 20) # 20 Composition points
tasks = [(T, X) for T in temps for X in compositions]

# --- 3. Parallelization Approach A: Multiprocessing ---
# Strategy used in MaterialsMap (sun2024materialsmapacalphadbased pages 10-15)
if __name__ == "__main__":
    # Pool creates separate processes (bypassing GIL)
    with Pool(processes=4) as pool:
        # starmap executes the function with arguments from the list
        results_mp = pool.starmap(calculate_point, tasks)
    print(f"Multiprocessing: Computed {len(results_mp)} points.")

# --- 4. Parallelization Approach B: Joblib ---
# Common for scientific computing arrays
results_joblib = Parallel(n_jobs=4)(
    delayed(calculate_point)(T, X) for T, X in tasks
)
print(f"Joblib: Computed {len(results_joblib)} points.")

# --- 5. Parallelization Approach C: Dask ---
# PyCalphad dependency for distributed computing (otis2024pycalphadcalphadbasedcomputational pages 4-7)
# Create a graph of lazy tasks
lazy_results = [dask_delayed(calculate_point)(T, X) for T, X in tasks]

# Compute triggers execution (scheduler='processes' avoids GIL)
results_dask = dask.compute(*lazy_results, scheduler='processes')
print(f"Dask: Computed {len(results_dask)} points.")
```


*Code_block: Python code demonstrating three frameworks (multiprocessing, joblib, and Dask) to parallelize thermodynamic equilibrium calculations using the pycalphad API.*

## 3. Freely Available Thermodynamic Databases (TDB Files)

Several freely available thermodynamic databases in TDB format can be used with pycalphad for alloy screening:

**COST 507** is an extensive European collaborative database containing experimentally-assessed thermodynamic functions for light-weight alloy systems, particularly Al-based, Mg-based, and Ti-based alloys (wolverton2006firstprinciplesaluminumdatabase pages 1-2). It is publicly available from the NIST Materials Data Repository. Pycalphad's own example files (e.g., `alfe_sei.TDB`) are drawn from this database, and the Al-Fe system is used as the standard demonstration because the COST 507 database "containing this subsystem is publicly available, and it allows us to test several pycalphad features simultaneously since the system contains single-sublattice solution phases, multi-sublattice ordered phases, phases with magnetic ordering and stoichiometric compounds" (otis2024pycalphadcalphadbasedcomputational pages 7-10). COST 507 has also been validated for high-throughput screening of 6016 Al-alloys (zhang2019highthroughputthermodynamiccalculations pages 1-2).

**The Thermodynamic Database Database (TDBDB)** is a specialized search and indexing effort that collects electronically available TDB files from the scientific literature. At the time of its publication, it contained 766 entries from 528 publications, aggregating data from multiple sources including the CALPHAD journal supplementary information, the NIMS database, and the NIST Materials Data Repository (walle2018thethermodynamicdatabase pages 1-2, walle2018thethermodynamicdatabase pages 3-5). Individual TDB files can be downloaded directly via URL.

**SGTE pure elements** data, assessed by the Scientific Group Thermodata Europe, provides the foundational unary thermodynamic descriptions used by virtually all multicomponent CALPHAD databases (mianiUnknownyear…demonstrationof pages 7-10, mianiUnknownyearperspectivestudyfor pages 7-10). The SGTE binary collection has also been validated and distributed in XTDB format (mianiUnknownyear…demonstrationof pages 7-10).

Additional open-access repositories include the **NIMS Database**, the **NIST Solder Database**, the **Widom Alloy Database**, **MatCalc open databases**, and **OpenCalphad test databases** (walle2018thethermodynamicdatabase pages 5-6, sundman2015opencalphada pages 14-15, walle2018thethermodynamicdatabase pages 1-2). OpenCalphad, distributed under a GNU license, provides a free thermodynamic calculation engine with accessible test databases and a programming interface callable from Python (sundman2015opencalphada pages 3-4).

| Database Name | Description/Coverage | URL/Source | Notes |
|---|---|---|---|
| **COST 507** | Thermochemical database for light metal alloys (Al-based, Mg-based, Ti-based). Covers many ternary systems relevant to light alloy design. | [NIST Materials Data Repository](https://materialsdata.nist.gov/dspace/xmlui/handle/11256/618) | Originally from the European COST Action 507. A widely used open benchmark for Al-alloys (otis2024pycalphadcalphadbasedcomputational pages 10-11, otis2024pycalphadcalphadbasedcomputational pages 7-10). |
| **SGTE Pure Elements** | Standard reference data for pure elements (unary systems) assessed by the Scientific Group Thermodata Europe. | [SGTE](http://www.sgte.org) / OpenCalphad / Dinsdale (1991) | The foundation for most multicomponent CALPHAD assessments; ensures compatibility between databases (mianiUnknownyear…demonstrationof pages 7-10, saxena2013thermodynamicdatabasesand pages 18-22). |
| **TDBDB (The Thermodynamic Database Database)** | An indexed search engine and collection of TDB files extracted from scientific literature. | [TDBDB](https://avdwalle.github.io/tdbdb/) | Aggregates hundreds of TDB files (766+ entries) from various publications, facilitating high-throughput screening (walle2018thethermodynamicdatabase pages 1-2, walle2018thethermodynamicdatabase pages 3-5). |
| **NIMS Materials Database** | Thermodynamic data for various structural and functional materials. | [NIMS (National Institute for Materials Science)](https://www.nims.go.jp/eng/) | Provides valuable data in electronic formats suitable for computational thermodynamics (walle2018thethermodynamicdatabase pages 5-6, walle2018thethermodynamicdatabase pages 3-5). |
| **NIST Solder Database** | Thermodynamics of Pb-free solder alloys and related systems. | NIST Materials Data Repository | Specifically focused on solder systems; freely available (walle2018thethermodynamicdatabase pages 5-6, walle2018thethermodynamicdatabase pages 1-2). |
| **Widom Alloy Database** | Collection of alloy thermodynamic data. | Widom Project / NIST Repository | A repository referenced for alloy data (walle2018thethermodynamicdatabase pages 5-6). |
| **MatCalc Open Databases** | Open-source subset of databases provided with the MatCalc software. | MatCalc / TDBDB | Includes general purpose and specific alloy system databases (walle2018thethermodynamicdatabase pages 1-2). |
| **OpenCalphad Test Databases** | Example TDB files distributed with the OpenCalphad software. | [OpenCalphad](http://www.opencalphad.com) | Validated files useful for testing software coupling and parallel workflows (sundman2015opencalphada pages 3-4, sundman2015opencalphada pages 14-15). |
| **pycalphad Examples** | Sample TDB files included with pycalphad (e.g., `alfe_sei.TDB`). | [pycalphad GitHub](https://github.com/pycalphad/pycalphad) | Often subsets of larger databases like COST 507, used for testing and tutorials (otis2024pycalphadcalphadbasedcomputational pages 7-10). |


*Table: A summary of open-access thermodynamic databases compatible with pycalphad for high-throughput alloy screening and phase equilibrium calculations.*

## 4. Practical Considerations

When deploying pycalphad in high-throughput workflows, several practical considerations emerge from the literature:

- **Task independence:** Each equilibrium or Scheil calculation at a given set of conditions (composition, temperature, pressure) is independent, making these calculations embarrassingly parallel and well-suited for distributed computing (gao2022amachinelearning pages 2-3).
- **Process-based parallelism:** Python's Global Interpreter Lock (GIL) means that thread-based parallelism provides limited benefit for CPU-bound calculations. Process-based approaches (multiprocessing, joblib with `backend='loky'`, or Dask with `scheduler='processes'`) are preferred (sun2024materialsmapacalphadbased pages 10-15).
- **Licensing advantages:** Unlike commercial CALPHAD software, which may limit parallel processor usage (e.g., TC-Python permits only up to 32 logical processors per license), open-source tools like pycalphad and Equilipy have no such constraints, making them especially attractive for HPC environments (kwon2024equilipyapython pages 1-3).
- **Machine learning augmentation:** HT-CALPHAD workflows can be further accelerated by coupling with machine learning models to densify calculated results and reduce the total number of explicit equilibrium evaluations needed (gao2022amachinelearning pages 1-2, gao2022amachinelearning pages 3-5).

References

1. (otis2024pycalphadcalphadbasedcomputational pages 1-3): Richard Otis and Zi-Kui Liu. Pycalphad: calphad-based computational thermodynamics in python. Zentropy, pages 373-392, May 2024. URL: https://doi.org/10.1201/9781003514466-18, doi:10.1201/9781003514466-18. This article has 195 citations.

2. (liu2018oceanofdata pages 6-8): Zi-Kui Liu. Ocean of data: integrating first-principles calculations and calphad modeling with machine learning. Journal of Phase Equilibria and Diffusion, 39:635-649, Jul 2018. URL: https://doi.org/10.1007/s11669-018-0654-z, doi:10.1007/s11669-018-0654-z. This article has 44 citations and is from a peer-reviewed journal.

3. (olson2024genomicmaterialsdesign pages 29-34): G.B. Olson and Z.K. Liu. Genomic materials design: calculation of phase dynamics. Calphad, 82:102590, Sep 2024. URL: https://doi.org/10.1016/j.calphad.2023.102590, doi:10.1016/j.calphad.2023.102590. This article has 27 citations.

4. (otis2024pycalphadcalphadbasedcomputational pages 4-7): Richard Otis and Zi-Kui Liu. Pycalphad: calphad-based computational thermodynamics in python. Zentropy, pages 373-392, May 2024. URL: https://doi.org/10.1201/9781003514466-18, doi:10.1201/9781003514466-18. This article has 195 citations.

5. (otis2017highthroughputthermodynamicmodeling pages 1-2): Richard A. Otis and Zi-Kui Liu. High-throughput thermodynamic modeling and uncertainty quantification for icme. JOM, 69:886-892, Mar 2017. URL: https://doi.org/10.1007/s11837-017-2318-6, doi:10.1007/s11837-017-2318-6. This article has 59 citations and is from a peer-reviewed journal.

6. (otis2017highthroughputthermodynamicmodeling pages 5-7): Richard A. Otis and Zi-Kui Liu. High-throughput thermodynamic modeling and uncertainty quantification for icme. JOM, 69:886-892, Mar 2017. URL: https://doi.org/10.1007/s11837-017-2318-6, doi:10.1007/s11837-017-2318-6. This article has 59 citations and is from a peer-reviewed journal.

7. (bocklund2020scheilgulliversimulationsfor pages 6-10): Brandon Bocklund, Lourdes D. Bobbio, Richard A. Otis, Allison M. Beese, and Zi-Kui Liu. Scheil-gulliver simulations for the design of functionally graded alloys by additive manufacturing using pycalphad. Text, Jan 2020. URL: https://doi.org/10.48550/arxiv.2001.11611, doi:10.48550/arxiv.2001.11611. This article has 5 citations and is from a peer-reviewed journal.

8. (sun2024materialsmapacalphadbased pages 6-10): Hui Sun, Bo Pan, Zhening Yang, Adam M. Krajewski, Brandon Bocklund, Shun-Li Shang, Jingjing Li, Allison M. Beese, and Zi-Kui Liu. Materialsmap: a calphad-based tool to design composition pathways through feasibility map for desired dissimilar materials, demonstrated with resistance spot welding joining of ag-al-cu. Materialia, 36:102153, Aug 2024. URL: https://doi.org/10.1016/j.mtla.2024.102153, doi:10.1016/j.mtla.2024.102153. This article has 10 citations and is from a peer-reviewed journal.

9. (sun2024materialsmapacalphadbased pages 10-15): Hui Sun, Bo Pan, Zhening Yang, Adam M. Krajewski, Brandon Bocklund, Shun-Li Shang, Jingjing Li, Allison M. Beese, and Zi-Kui Liu. Materialsmap: a calphad-based tool to design composition pathways through feasibility map for desired dissimilar materials, demonstrated with resistance spot welding joining of ag-al-cu. Materialia, 36:102153, Aug 2024. URL: https://doi.org/10.1016/j.mtla.2024.102153, doi:10.1016/j.mtla.2024.102153. This article has 10 citations and is from a peer-reviewed journal.

10. (gao2022amachinelearning pages 1-2): Jianbao Gao, Jing Zhong, Guangchen Liu, Shenglan Yang, Bo Song, Lijun Zhang, and Zuming Liu. A machine learning accelerated distributed task management system (malac-distmas) and its application in high-throughput calphad computation aiming at efficient alloy design. Advanced Powder Materials, 1:100005, Jan 2022. URL: https://doi.org/10.1016/j.apmate.2021.09.005, doi:10.1016/j.apmate.2021.09.005. This article has 57 citations and is from a peer-reviewed journal.

11. (gao2022amachinelearning pages 2-3): Jianbao Gao, Jing Zhong, Guangchen Liu, Shenglan Yang, Bo Song, Lijun Zhang, and Zuming Liu. A machine learning accelerated distributed task management system (malac-distmas) and its application in high-throughput calphad computation aiming at efficient alloy design. Advanced Powder Materials, 1:100005, Jan 2022. URL: https://doi.org/10.1016/j.apmate.2021.09.005, doi:10.1016/j.apmate.2021.09.005. This article has 57 citations and is from a peer-reviewed journal.

12. (gao2022amachinelearning pages 3-5): Jianbao Gao, Jing Zhong, Guangchen Liu, Shenglan Yang, Bo Song, Lijun Zhang, and Zuming Liu. A machine learning accelerated distributed task management system (malac-distmas) and its application in high-throughput calphad computation aiming at efficient alloy design. Advanced Powder Materials, 1:100005, Jan 2022. URL: https://doi.org/10.1016/j.apmate.2021.09.005, doi:10.1016/j.apmate.2021.09.005. This article has 57 citations and is from a peer-reviewed journal.

13. (kwon2024equilipyapython pages 3-5): Sun Yong Kwon, Eric Thibodeau, Plotkowski, and Ying Yang. Equilipy: a python package for calculating phase equilibria. J. Open Source Softw., 9:6875, Aug 2024. URL: https://doi.org/10.21105/joss.06875, doi:10.21105/joss.06875. This article has 2 citations.

14. (kwon2024equilipyapython pages 1-3): Sun Yong Kwon, Eric Thibodeau, Plotkowski, and Ying Yang. Equilipy: a python package for calculating phase equilibria. J. Open Source Softw., 9:6875, Aug 2024. URL: https://doi.org/10.21105/joss.06875, doi:10.21105/joss.06875. This article has 2 citations.

15. (otis2024pycalphadcalphadbasedcomputational media b99aade9): Richard Otis and Zi-Kui Liu. Pycalphad: calphad-based computational thermodynamics in python. Zentropy, pages 373-392, May 2024. URL: https://doi.org/10.1201/9781003514466-18, doi:10.1201/9781003514466-18. This article has 195 citations.

16. (otis2024pycalphadcalphadbasedcomputational pages 10-11): Richard Otis and Zi-Kui Liu. Pycalphad: calphad-based computational thermodynamics in python. Zentropy, pages 373-392, May 2024. URL: https://doi.org/10.1201/9781003514466-18, doi:10.1201/9781003514466-18. This article has 195 citations.

17. (wolverton2006firstprinciplesaluminumdatabase pages 1-2): C. Wolverton and V. Ozoliņš. First-principles aluminum database: energetics of binary al alloys and compounds. Physical Review B, 73:144104, Apr 2006. URL: https://doi.org/10.1103/physrevb.73.144104, doi:10.1103/physrevb.73.144104. This article has 156 citations and is from a domain leading peer-reviewed journal.

18. (otis2024pycalphadcalphadbasedcomputational pages 7-10): Richard Otis and Zi-Kui Liu. Pycalphad: calphad-based computational thermodynamics in python. Zentropy, pages 373-392, May 2024. URL: https://doi.org/10.1201/9781003514466-18, doi:10.1201/9781003514466-18. This article has 195 citations.

19. (zhang2019highthroughputthermodynamiccalculations pages 1-2): Cong Zhang, Xue Jiang, Ruijie Zhang, Xin Wang, Haiqing Yin, Xuanhui Qu, and Zi-Kui Liu. High-throughput thermodynamic calculations of phase equilibria in solidified 6016 al-alloys. Computational Materials Science, 167:19-24, Sep 2019. URL: https://doi.org/10.1016/j.commatsci.2019.05.022, doi:10.1016/j.commatsci.2019.05.022. This article has 32 citations and is from a domain leading peer-reviewed journal.

20. (walle2018thethermodynamicdatabase pages 1-2): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

21. (walle2018thethermodynamicdatabase pages 3-5): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

22. (mianiUnknownyear…demonstrationof pages 7-10): F Miani. … demonstration of the viability and usability of an xml-based standardization for calphad thermodynamic database. a design study based on the binary sgte …. Unknown journal, Unknown year.

23. (mianiUnknownyearperspectivestudyfor pages 7-10): F Miani. Perspective study for the demonstration of the viability and usability of an xml-based standardization for calphad thermodynamic database. a design study …. Unknown journal, Unknown year.

24. (walle2018thethermodynamicdatabase pages 5-6): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

25. (sundman2015opencalphada pages 14-15): Bo Sundman, Ursula R Kattner, Mauro Palumbo, and Suzana G Fries. Opencalphad - a free thermodynamic software. Integrating Materials and Manufacturing Innovation, 4:1-15, Jan 2015. URL: https://doi.org/10.1186/s40192-014-0029-1, doi:10.1186/s40192-014-0029-1. This article has 198 citations and is from a peer-reviewed journal.

26. (sundman2015opencalphada pages 3-4): Bo Sundman, Ursula R Kattner, Mauro Palumbo, and Suzana G Fries. Opencalphad - a free thermodynamic software. Integrating Materials and Manufacturing Innovation, 4:1-15, Jan 2015. URL: https://doi.org/10.1186/s40192-014-0029-1, doi:10.1186/s40192-014-0029-1. This article has 198 citations and is from a peer-reviewed journal.

27. (saxena2013thermodynamicdatabasesand pages 18-22): S.K. Saxena. Thermodynamic databases and phase diagrams. ArXiv, pages 245-269, Jan 2013. URL: https://doi.org/10.1016/b978-0-12-394399-6.00011-4, doi:10.1016/b978-0-12-394399-6.00011-4. This article has 4 citations.