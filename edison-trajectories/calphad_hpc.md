Question: How can CALPHAD calculations (using pycalphad or Thermo-Calc TC-Python) be run in high throughput on HPC clusters? What are the best practices for parallelizing phase diagram and thermodynamic property calculations across many compositions? Include specific examples of SLURM job arrays, Python multiprocessing, Dask, or MPI approaches for batch CALPHAD screening of alloy compositions.

# High-Throughput CALPHAD Calculations on HPC Clusters: Parallelization Strategies and Best Practices

## 1. Introduction and the Embarrassingly Parallel Nature of CALPHAD Screening

High-throughput (HT) CALPHAD calculations—whether equilibrium phase-fraction maps, Scheil–Gulliver solidification simulations, or thermodynamic property evaluations—are fundamentally amenable to parallelization because each composition–temperature point constitutes an independent Gibbs energy minimization that requires no inter-task communication (roos2022acceleratingcomplexchemical pages 6-8, kwon2024equilipyapython pages 5-7). This "embarrassingly parallel" structure means that the primary engineering challenge is orchestrating, scheduling, and collecting results from potentially millions of independent calculations, rather than managing fine-grained inter-process data exchange (hicks2024massivelyscalableworkflows pages 6-9). Frameworks spanning simple Python `multiprocessing` pools to MPI, Parsl-based HPC workflows, and dedicated distributed task managers have all been demonstrated in the literature.

## 2. Overview of Frameworks and Tools

The following table summarizes the major parallelization approaches that have been applied to HT-CALPHAD workflows:

| Framework/Tool | CALPHAD Engine | Parallelization Method | Key Feature | Reference |
|---|---|---|---|---|
| Equilipy | Equilipy (Fortran G-minimizer) | MPI via mpi4py; equilib_batch over independent NPT points; single/multi-node | Embarrassingly parallel batch equilibrium; speeds comparable to TC-Python/PanPython | (kwon2024equilipyapython pages 1-3, kwon2024equilipyapython pages 5-7, kwon2024equilipyapython pages 3-5) |
| MaterialsMap | Thermo-Calc (TC macros); PyCalphad alternative | Python multiprocessing Pool across compositions | Auto-generate composition grids, create/run .tcm scripts, parse outputs; build feasibility/crack maps | (sun2024materialsmapacalphadbased pages 10-15) |
| exaPD | PyCalphad for PD construction; LAMMPS for free energies | Parsl workflow with SLURM executors (CPU/GPU); task-graph concurrency | Near-ideal scaling; resumable runs with DONE markers; massive MD/MC batches feeding CALPHAD | (zhang2025exapdahighly pages 10-12, zhang2025exapdahighly pages 1-2, zhang2025exapdahighly pages 12-13, zhang2025exapdahighly pages 7-9, xia2510exaamdanexascaleready pages 17-20) |
| CAROUSEL | MatCalc (example); extensible to other CALPHAD tools | Distributed task execution across many cases; threaded workers | Through-process (Scheil + precipitation) HT simulations; SQL-backed data; GUI; strong/weak scaling analyses | (stander2023carouselanopensource pages 1-3, stander2023carouselanopensource pages 3-6, stander2023carouselanopensource pages 8-11, stander2023carouselanopensource pages 11-12) |
| Malac-Distmas | Pandat (PanPrecipitation); interfaces to PyCalphad/Thermo-Calc via console/API | Distributed task manager; load-balanced scheduler over heterogeneous executors | ML densification (ANN) reduces CALPHAD calls; fault tolerance; scalable HTC orchestration | (gao2022amachinelearning pages 1-2, gao2022amachinelearning pages 2-3) |
| TC-Python batch workflows | Thermo-Calc (TC-Python) | Scripted loops over composition/temperature grids; slice grids to threads/cores | HT equilibrium/Scheil; temperature caps; JSON outputs; eutectic screening examples | (zhang2022identificationofthe pages 1-2, tripathi2021automatedapproachto pages 1-2, ghassemali2022highthroughputcalphada pages 4-5, wang2020thermodynamicinvestigationof pages 4-6, vazquez2023adeepneural pages 4-6) |
| Direct MPI for equilibrium solvers | Generic CALPHAD-style equilibrium kernels | MPI scatter/gather of independent equilibrium solves | Near-linear speedup to tens of cores; in-situ tabulation; GPU mixed-precision speedups reported | (roos2022acceleratingcomplexchemical pages 6-8) |


*Table: Side-by-side comparison of HPC parallelization options for high-throughput CALPHAD, covering engines, methods, and distinguishing features. Citations link to evidence for each framework’s approach and scaling characteristics.*

## 3. Parallelization Approaches in Detail

### 3.1 Python Multiprocessing (Single-Node)

The simplest and most widely accessible approach uses Python's `multiprocessing.Pool` to distribute independent equilibrium calculations across CPU cores on a single node. The MaterialsMap tool demonstrates this pattern: a composition grid is generated (e.g., 903 points for a ternary with `ngridpts=41`), and either pycalphad equilibrium/Scheil functions (`pycalphad_eq()`, `pycalphad_scheil()`) or Thermo-Calc macro scripts are dispatched to a multiprocessing Pool that accelerates evaluation across all compositions and reports process/time information (sun2024materialsmapacalphadbased pages 10-15). This approach is straightforward for workloads fitting on a single compute node and requires no external scheduler infrastructure. The pycalphad ecosystem, developed by Otis and Liu, underpins many such HT workflows by providing a pure-Python CALPHAD engine suitable for automated parameter selection and uncertainty quantification (otis2017highthroughputthermodynamicmodeling pages 1-2).

### 3.2 MPI-Based Parallelization (Multi-Node)

For scaling beyond a single node, Message Passing Interface (MPI) parallelization provides near-linear speedup. Studies on parallelized equilibrium solvers using MPI have demonstrated close-to-linear scaling up to approximately 24–48 cores, at which point inter-core data-transfer overhead begins to dominate (roos2022acceleratingcomplexchemical pages 6-8). The equilipy package provides a dedicated `equilib_batch()` function that treats each NPT (composition–pressure–temperature) condition as an independent calculation and distributes work across processors using `mpi4py` (kwon2024equilipyapython pages 1-3, kwon2024equilipyapython pages 5-7, kwon2024equilipyapython pages 3-5). By default, equilipy uses all available processors on a single node; for multi-node runs, users configure OpenMPI or MPICH environments. Its core Fortran equilibrium solver, interfaced with Python via F2PY, achieves computation speeds comparable to TC-Python and PanPython in benchmarks on 8,096 equilibrium calculations (kwon2024equilipyapython pages 1-3). GPU acceleration with mixed-precision strategies (single precision for most work, double for refinement) has also been explored for equilibrium solvers, yielding approximately 3× speedup in test cases (roos2022acceleratingcomplexchemical pages 6-8).

### 3.3 SLURM Job Arrays

SLURM job arrays are a natural fit for HT-CALPHAD on HPC clusters, as each array task can independently process a subset of the composition grid. The workflow involves: (1) pre-generating a CSV or database of all composition–temperature points; (2) submitting a SLURM array where each `$SLURM_ARRAY_TASK_ID` indexes into one or a chunk of points; and (3) running a Python script (using either pycalphad or TC-Python) that reads its assigned point, performs the equilibrium/Scheil calculation, and writes the result to a per-task output file. This pattern is widely used in computational materials science and is compatible with both open-source (pycalphad) and commercial (Thermo-Calc) engines. The exaPD workflow explicitly uses SLURM providers within its Parsl configuration to launch molecular dynamics and free-energy tasks on HPC clusters (zhang2025exapdahighly pages 10-12, zhang2025exapdahighly pages 7-9).

### 3.4 Parsl-Based Workflows with SLURM

The exaPD framework exemplifies a more sophisticated approach using Parsl, an open-source Python parallel programming library, as a global task controller that orchestrates thousands of independent tasks with near-ideal scalability (zhang2025exapdahighly pages 1-2). Parsl configurations specify `HighThroughputExecutor` objects with `SlurmProvider` backends, defining parameters such as `nodes_per_block`, `max_blocks`, `cores_per_worker`, and `worker_init` environment setup (xia2510exaamdanexascaleready pages 17-20). Tasks are expressed as Python functions decorated with `@python_app`, and dependencies between tasks are enforced through futures—dependent steps only execute when prerequisites complete (zhang2025exapdahighly pages 10-12). exaPD supports heterogeneous CPU/GPU scheduling by assigning different executors to different task types and achieves resumable workflows through per-task completion markers ("DONE files"), allowing interrupted runs to continue from where they left off (zhang2025exapdahighly pages 10-12). The exa-AMD framework similarly uses Parsl with dynamic provisioning and elasticity, enabling resources to grow or shrink during different workflow stages (xia2510exaamdanexascaleready pages 9-11). Post-processing steps collect outputs and feed them into pycalphad for phase diagram construction (zhang2025exapdahighly pages 12-13).

### 3.5 Dask for Distributed CALPHAD

While no published CALPHAD-specific Dask workflow was identified in the literature, the Dask `delayed` and `distributed` patterns are directly analogous to the horizontally scalable task-composition approaches described for BigChem and other distributed scientific computing frameworks (hicks2024massivelyscalableworkflows pages 4-6, hicks2024massivelyscalableworkflows pages 9-11, hicks2024massivelyscalableworkflows pages 21-25). In this pattern, each CALPHAD equilibrium calculation is wrapped as a `@delayed` function, and many such tasks are submitted to a Dask scheduler (local or cluster-wide via `dask-jobqueue` with SLURM/PBS backends). The key design principle is to keep per-task inputs/outputs small while maximizing compute intensity per task to reduce network overhead (hicks2024massivelyscalableworkflows pages 9-11). Dask's built-in fault tolerance, dashboard monitoring, and ability to scale from a laptop to hundreds of cluster nodes make it a natural choice for researchers already in the Python/Jupyter ecosystem.

### 3.6 Dedicated Distributed Task Management Systems

**Malac-Distmas** is a machine-learning-accelerated distributed task management system specifically designed for HT-CALPHAD computations (gao2022amachinelearning pages 1-2, gao2022amachinelearning pages 2-3). It partitions large CALPHAD screening campaigns into independent subtasks dispatched to heterogeneous executors (desktops, laptops, servers) via a server/scheduler architecture with load balancing and fault tolerance (failed tasks are retried, logged, or restored to the queue). A key innovation is the integration of an artificial neural network (ANN) that "densifies" calculation outputs by predicting intermediate thermodynamic/kinetic results, thereby reducing the total number of expensive CALPHAD runs required (gao2022amachinelearning pages 2-3).

**CAROUSEL** is an open-source framework for HT microstructure simulations that supports equilibrium, Scheil, and precipitation kinetic calculations across many alloy compositions (stander2023carouselanopensource pages 1-3, stander2023carouselanopensource pages 3-6). It features a task distribution system, SQL-backed data management, a GUI, and extensibility to different CALPHAD implementations (demonstrated with MatCalc). Performance testing with 1,000–3,000 Scheil cases showed notable speedup and parallel efficiency; instantiation overhead of the CALPHAD software limits scaling for small case counts, but becomes negligible for large workloads (stander2023carouselanopensource pages 8-11, stander2023carouselanopensource pages 11-12).

## 4. TC-Python Batch Workflows

For Thermo-Calc users, TC-Python provides a Python API for scripting batch equilibrium and Scheil calculations. The typical workflow involves: (1) generating composition grids by varying element weight/atomic percentages with specified step sizes; (2) looping over all grid points in Python, executing Thermo-Calc commands at each composition and temperature; and (3) collecting results into JSON or structured data files (zhang2022identificationofthe pages 1-2). Temperature limits are imposed (e.g., a ceiling of 2,500 K) to avoid unphysical Gibbs energy extrapolations (zhang2022identificationofthe pages 1-2). To accelerate throughput, composition grids are sliced and distributed to multiple threads or cores for parallel execution (tripathi2021automatedapproachto pages 1-2). The HT-CALPHAD review by Ghassemali and Conway emphasizes that TC-Python enables automated batch evaluation of solidus/solvus temperatures, solidification intervals, phase formation, phase fractions, compositions, and lattice parameters across large composition ranges, with practitioners typically performing rapid scans to identify "islands of interest" before deeper evaluation (ghassemali2022highthroughputcalphada pages 4-5). Wang et al. demonstrated TC-Python-based HT calculations for HSLA-115 steel design, computing equilibrium freezing ranges across large compositional sets and validating predictions against DTA experiments (wang2020thermodynamicinvestigationof pages 4-6).

## 5. Best Practices for HT-CALPHAD Parallelization

Based on the collective evidence, several best practices emerge:

1. **Minimize per-task I/O:** Keep input/output payloads small per equilibrium solve. Store only essential results (phase fractions, Gibbs energy, key temperatures) rather than full internal state, to reduce serialization and network overhead (hicks2024massivelyscalableworkflows pages 9-11).

2. **Use coarse-then-fine scanning:** Perform rapid coarse scans over the full composition space to identify promising regions, then refine grids in those regions. This reduces the total number of calculations by orders of magnitude (ghassemali2022highthroughputcalphada pages 4-5).

3. **Implement fault tolerance:** HT campaigns with thousands of calculations will inevitably encounter failures. Use completion markers (DONE files), database-backed result storage, or job-retry mechanisms to enable resumable workflows (gao2022amachinelearning pages 2-3, zhang2025exapdahighly pages 10-12).

4. **Couple with machine learning:** ANN or surrogate models trained on CALPHAD outputs can interpolate or extrapolate to fill gaps in the composition grid, substantially reducing the number of explicit equilibrium solves needed (gao2022amachinelearning pages 2-3).

5. **Manage temperature bounds carefully:** Set starting temperatures above the melting points of constituent elements and enforce global upper limits (e.g., 2,500 K) to prevent unphysical Gibbs energy extrapolations (zhang2022identificationofthe pages 1-2).

6. **Choose the right level of parallelism:** For single-node campaigns of a few thousand points, Python `multiprocessing` or equilipy's built-in batch mode suffices. For campaigns exceeding 10,000+ points or requiring multi-node scaling, MPI, Parsl, or Dask provide better resource utilization and fault tolerance (roos2022acceleratingcomplexchemical pages 6-8, kwon2024equilipyapython pages 5-7, zhang2025exapdahighly pages 1-2).

7. **Account for licensing constraints:** TC-Python requires a Thermo-Calc license, which may limit the number of concurrent instances. pycalphad and equilipy are open-source alternatives that avoid this bottleneck for embarrassingly parallel scaling (sun2024materialsmapacalphadbased pages 10-15, kwon2024equilipyapython pages 1-3).

## 6. Example Code Patterns

The following code block provides pseudocode examples for five parallelization strategies: Python `multiprocessing.Pool`, SLURM job arrays, Dask delayed, MPI with `mpi4py`, and Parsl-based HPC workflows. Each pattern is annotated with the literature sources that motivated its design.

```python
# 1) Python multiprocessing.Pool for pycalphad over compositions (inspired by MaterialsMap)
# refs: (sun2024materialsmapacalphadbased pages 10-15, otis2017highthroughputthermodynamicmodeling pages 3-5, otis2017highthroughputthermodynamicmodeling pages 5-7)
import json
from itertools import product
from multiprocessing import Pool, cpu_count
# from pycalphad import Database, equilibrium, variables as v  # uncomment if pycalphad available

# Example: ternary grid X-A + X-B + X-C = 1 at fixed T,P
A, B, C = 'AL', 'CU', 'MG'  # example elements
T_vals = [900, 1000, 1100]  # K
P = 101325  # Pa
step = 0.1
comps = []
for xa in [i*step for i in range(int(1/step)+1)]:
    for xb in [j*step for j in range(int((1-xa)/step)+1)]:
        xc = 1 - xa - xb
        if xc < -1e-12:
            continue
        comps.append({A: xa, B: xb, C: xc})

def run_eq(args):
    comp, T = args
    # db = Database('Al-Cu-Mg.tdb')
    # eq = equilibrium(db, compset=[A,B,C], conds={v.T: T, v.P: P, v.X(A): comp[A], v.X(B): comp[B]}, output='GM')
    # Extract minimal results to keep outputs small (best practice)
    # result = {"T": T, "x": comp, "gm": float(eq.GM.m.min())}
    # Pseudocode placeholder result:
    return {"T": T, "x": comp, "gm": 0.0}

if __name__ == '__main__':
    tasks = [(c, T) for c, T in product(comps, T_vals)]
    # Use all local cores, but cap to avoid oversubscription on shared nodes
    nproc = min(cpu_count(), 32)
    with Pool(processes=nproc) as pool:
        results = list(pool.imap_unordered(run_eq, tasks, chunksize=16))
    with open('pycalphad_pool_results.json', 'w') as f:
        json.dump(results, f)


# 2) SLURM job array for batch CALPHAD runs (TC-Python or pycalphad)
# refs: Parsl+Slurm orchestration and massive parallel PD sampling (zhang2025exapdahighly pages 10-12, zhang2025exapdahighly pages 1-2, zhang2025exapdahighly pages 12-13),
#       TC-Python HT screening patterns (zhang2022identificationofthe pages 1-2, ghassemali2022highthroughputcalphada pages 4-5, wang2020thermodynamicinvestigationof pages 4-6)
# Save as run_array.sbatch and submit with: sbatch run_array.sbatch

# ! /bin/bash
## SBATCH --job-name=calphad_array
## SBATCH --partition=compute
## SBATCH --time=02:00:00
## SBATCH --nodes=1
## SBATCH --cpus-per-task=4
## SBATCH --mem=8G
## SBATCH --array=0-899%100  # 900 points in grid, 100 concurrent

module purge
module load python/3.10
# module load thermocalc  # if using TC-Python; ensure license server is reachable
source ~/venvs/calphad/bin/activate

INPUT_CSV=compositions.csv  # pre-generated grid of comps/temps
OUTDIR=outputs
mkdir -p "$OUTDIR"

IDX=$SLURM_ARRAY_TASK_ID
python run_batch.py --index "$IDX" --input "$INPUT_CSV" --outdir "$OUTDIR"

# (run_batch.py) Minimal Python batch worker example
# refs: (zhang2022identificationofthe pages 1-2, ghassemali2022highthroughputcalphada pages 4-5)
# import argparse, json, pandas as pd
# # from thermocalc import TCPython  # TC-Python
# # from pycalphad import Database, equilibrium, variables as v
# parser = argparse.ArgumentParser()
# parser.add_argument('--index', type=int, required=True)
# parser.add_argument('--input', type=str, required=True)
# parser.add_argument('--outdir', type=str, required=True)
# args = parser.parse_args()
# row = pd.read_csv(args.input).iloc[args.index]
# # Perform equilibrium or Scheil here via TC-Python or pycalphad
# # tc = TCPython(db='TCFE', mob_db='TCFE_MOB')  # example
# result = {"i": int(args.index), "T": row.T, "x": {k: row[k] for k in row.index if k.startswith('X_')}, "gm": 0.0}
# with open(f"{args.outdir}/result_{args.index:05d}.json", 'w') as f:
#     json.dump(result, f)


# 3) Dask delayed pattern for distributed CALPHAD screening (analogous to horizontally scalable task graphs)
# refs: distributed task orchestration patterns and map/reduce composition (hicks2024massivelyscalableworkflows pages 4-6, hicks2024massivelyscalableworkflows pages 9-11, hicks2024massivelyscalableworkflows pages 21-25)
from dask.distributed import Client
from dask import delayed, compute
# from pycalphad import Database, equilibrium, variables as v

# Option A: connect to an existing Dask scheduler provisioned via jobqueue (not shown)
client = Client("tcp://SCHEDULER:8786")  # or Client() for local testing

@delayed
def eq_task(comp, T):
    # db = Database('db.tdb')
    # eq = equilibrium(db, compset=list(comp.keys()), conds={v.T:T, v.P:101325, **{v.X(k): comp[k] for k in comp}}, output='GM')
    return {"T": T, "x": comp, "gm": 0.0}

comps_small = [{"AL": 0.3, "CU": 0.3, "MG": 0.4}, {"AL": 0.2, "CU": 0.5, "MG": 0.3}]  # example
Ts = [900, 1000, 1100]

futures = [eq_task(c, T) for c in comps_small for T in Ts]
results = compute(*futures, scheduler=client)  # list of dicts
print(results)


# 4) MPI-based parallel equilibrium with mpi4py (inspired by Equilipy equilib_batch and generic MPI scatter/gather)
# refs: Equilipy parallel batch via mpi4py (kwon2024equilipyapython pages 1-3, kwon2024equilipyapython pages 5-7, kwon2024equilipyapython pages 3-5); direct MPI parallel equilibrium scaling (roos2022acceleratingcomplexchemical pages 6-8)
from mpi4py import MPI
# from pycalphad import Database, equilibrium, variables as v
import json

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Prepare task list on rank 0
if rank == 0:
    comps = [{"AL": xa, "CU": xb, "MG": 1 - xa - xb}
             for xa in [0.0, 0.25, 0.5, 0.75, 1.0]
             for xb in [0.0, 0.25, 0.5, 0.75] if xa + xb <= 1.0]
    Ts = [900, 1000, 1100]
    tasks = [(c, T) for c in comps for T in Ts]
else:
    tasks = None

# Scatter tasks in contiguous chunks
if rank == 0:
    chunks = [tasks[i::size] for i in range(size)]
else:
    chunks = None
my_tasks = comm.scatter(chunks, root=0)

# db = Database('db.tdb')
my_results = []
for comp, T in my_tasks:
    # eq = equilibrium(db, compset=list(comp.keys()), conds={v.T:T, v.P:101325, **{v.X(k): comp[k] for k in comp}}, output='GM')
    my_results.append({"T": T, "x": comp, "gm": 0.0, "rank": rank})

# Gather to rank 0
all_results = comm.gather(my_results, root=0)
if rank == 0:
    flat = [r for sub in all_results for r in sub]
    with open('mpi_batch_results.json', 'w') as f:
        json.dump(flat, f)


# 5) Parsl-based HPC workflow (inspired by exaPD; task graph + SLURM executors)
# refs: exaPD Parsl controller, SLURM executors, heterogeneous CPU/GPU mapping, resumable tasks (zhang2025exapdahighly pages 10-12, zhang2025exapdahighly pages 1-2, zhang2025exapdahighly pages 12-13, zhang2025exapdahighly pages 7-9, xia2510exaamdanexascaleready pages 17-20)
import parsl
from parsl import python_app
from parsl.providers import SlurmProvider
from parsl.executors import HighThroughputExecutor
from parsl.launchers import SrunLauncher

parsl.load(
    parsl.Config(
        executors=[
            HighThroughputExecutor(
                label="cpu_exec",
                cores_per_worker=2,
                max_workers=1,
                provider=SlurmProvider(
                    partition="compute",
                    nodes_per_block=1,
                    init_blocks=1,
                    max_blocks=10,
                    scheduler_options="#SBATCH --cpus-per-task=2\n#SBATCH --mem=4G",
                    worker_init="module load python/3.10; source ~/venvs/calphad/bin/activate",
                    launcher=SrunLauncher(overrides="--exclusive")
                ),
            )
        ]
    )
)

@python_app(executors=["cpu_exec"])
def eq_app(comp: dict, T: float) -> dict:
    # from pycalphad import Database, equilibrium, variables as v
    # db = Database('db.tdb')
    # eq = equilibrium(db, compset=list(comp.keys()), conds={v.T:T, v.P:101325, **{v.X(k): comp[k] for k in comp}}, output='GM')
    return {"T": T, "x": comp, "gm": 0.0}

# Build task graph
grid = [
    {"AL": 0.2, "CU": 0.5, "MG": 0.3},
    {"AL": 0.4, "CU": 0.4, "MG": 0.2},
]
Ts = [900, 1000]
apps = [eq_app(c, T) for c in grid for T in Ts]
results = [a.result() for a in apps]  # blocks until complete
print(results)

# To resume after partial completion, persist outputs per-task (e.g., to JSON files) and skip existing ones,
# similar to exaPD's DONE markers pattern (zhang2025exapdahighly pages 10-12).
```


*Code_block: Executable pseudocode illustrating five parallelization strategies for high-throughput CALPHAD on HPC: multiprocessing, SLURM job arrays, Dask delayed, MPI with mpi4py, and Parsl workflows. Inline comments cite sources that motivated each pattern and document best practices.*

## 7. Conclusion

HT-CALPHAD screening on HPC clusters is a mature and rapidly evolving practice, supported by a growing ecosystem of tools ranging from purpose-built distributed task managers (Malac-Distmas, CAROUSEL) to general-purpose parallel frameworks (multiprocessing, MPI, Dask, Parsl) integrated with CALPHAD engines (pycalphad, TC-Python, equilipy). The embarrassingly parallel nature of composition-wise equilibrium calculations makes CALPHAD workflows ideally suited for horizontal scaling, and near-linear speedup has been demonstrated up to tens of cores with MPI and near-ideal scaling with Parsl on HPC clusters (roos2022acceleratingcomplexchemical pages 6-8, zhang2025exapdahighly pages 1-2). The combination of automated grid generation, parallel equilibrium evaluation, structured result storage, and machine-learning-based densification represents the current state of the art for efficient alloy composition screening (gao2022amachinelearning pages 2-3, ghassemali2022highthroughputcalphada pages 4-5).

References

1. (roos2022acceleratingcomplexchemical pages 6-8): WA Roos and JH Zietsman. Accelerating complex chemical equilibrium calculations—a review. Unknown journal, 2022.

2. (kwon2024equilipyapython pages 5-7): Sun Yong Kwon, Eric Thibodeau, Plotkowski, and Ying Yang. Equilipy: a python package for calculating phase equilibria. J. Open Source Softw., 9:6875, Aug 2024. URL: https://doi.org/10.21105/joss.06875, doi:10.21105/joss.06875. This article has 2 citations.

3. (hicks2024massivelyscalableworkflows pages 6-9): Colton B. Hicks and Todd J. Martinez. Massively scalable workflows for quantum chemistry: bigchem and chemcloud. The Journal of chemical physics, Apr 2024. URL: https://doi.org/10.1063/5.0190834, doi:10.1063/5.0190834. This article has 16 citations.

4. (kwon2024equilipyapython pages 1-3): Sun Yong Kwon, Eric Thibodeau, Plotkowski, and Ying Yang. Equilipy: a python package for calculating phase equilibria. J. Open Source Softw., 9:6875, Aug 2024. URL: https://doi.org/10.21105/joss.06875, doi:10.21105/joss.06875. This article has 2 citations.

5. (kwon2024equilipyapython pages 3-5): Sun Yong Kwon, Eric Thibodeau, Plotkowski, and Ying Yang. Equilipy: a python package for calculating phase equilibria. J. Open Source Softw., 9:6875, Aug 2024. URL: https://doi.org/10.21105/joss.06875, doi:10.21105/joss.06875. This article has 2 citations.

6. (sun2024materialsmapacalphadbased pages 10-15): Hui Sun, Bo Pan, Zhening Yang, Adam M. Krajewski, Brandon Bocklund, Shun-Li Shang, Jingjing Li, Allison M. Beese, and Zi-Kui Liu. Materialsmap: a calphad-based tool to design composition pathways through feasibility map for desired dissimilar materials, demonstrated with resistance spot welding joining of ag-al-cu. Materialia, 36:102153, Aug 2024. URL: https://doi.org/10.1016/j.mtla.2024.102153, doi:10.1016/j.mtla.2024.102153. This article has 10 citations and is from a peer-reviewed journal.

7. (zhang2025exapdahighly pages 10-12): Feng Zhang, Zhuo Ye, Maxim Moraru, Ying Wai Li, Weiyi Xia, Yongxin Yao, Ryan Richard, and C. Z. Wang. Exapd: a highly parallelizable workflow for multi-element phase diagram (pd) construction. ArXiv, Oct 2025. URL: https://doi.org/10.48550/arxiv.2510.01400, doi:10.48550/arxiv.2510.01400. This article has 0 citations.

8. (zhang2025exapdahighly pages 1-2): Feng Zhang, Zhuo Ye, Maxim Moraru, Ying Wai Li, Weiyi Xia, Yongxin Yao, Ryan Richard, and C. Z. Wang. Exapd: a highly parallelizable workflow for multi-element phase diagram (pd) construction. ArXiv, Oct 2025. URL: https://doi.org/10.48550/arxiv.2510.01400, doi:10.48550/arxiv.2510.01400. This article has 0 citations.

9. (zhang2025exapdahighly pages 12-13): Feng Zhang, Zhuo Ye, Maxim Moraru, Ying Wai Li, Weiyi Xia, Yongxin Yao, Ryan Richard, and C. Z. Wang. Exapd: a highly parallelizable workflow for multi-element phase diagram (pd) construction. ArXiv, Oct 2025. URL: https://doi.org/10.48550/arxiv.2510.01400, doi:10.48550/arxiv.2510.01400. This article has 0 citations.

10. (zhang2025exapdahighly pages 7-9): Feng Zhang, Zhuo Ye, Maxim Moraru, Ying Wai Li, Weiyi Xia, Yongxin Yao, Ryan Richard, and C. Z. Wang. Exapd: a highly parallelizable workflow for multi-element phase diagram (pd) construction. ArXiv, Oct 2025. URL: https://doi.org/10.48550/arxiv.2510.01400, doi:10.48550/arxiv.2510.01400. This article has 0 citations.

11. (xia2510exaamdanexascaleready pages 17-20): Weiyi Xia, Maxim Moraru, Ying Wai Li, and Cai-Zhuang Wang. Exa-amd: an exascale-ready framework for accelerating the discovery and design of functional materials. ArXiv, Oct 2510. URL: https://doi.org/10.48550/arxiv.2510.01170, doi:10.48550/arxiv.2510.01170. This article has 1 citations.

12. (stander2023carouselanopensource pages 1-3): Sebastian Carrion Ständer, Nora Barschkett, and Evgeniya Kabliman. Carousel: an open-source framework for high-throughput microstructure simulations. Integrating Materials and Manufacturing Innovation, 12:289-300, Oct 2023. URL: https://doi.org/10.1007/s40192-023-00314-6, doi:10.1007/s40192-023-00314-6. This article has 2 citations and is from a peer-reviewed journal.

13. (stander2023carouselanopensource pages 3-6): Sebastian Carrion Ständer, Nora Barschkett, and Evgeniya Kabliman. Carousel: an open-source framework for high-throughput microstructure simulations. Integrating Materials and Manufacturing Innovation, 12:289-300, Oct 2023. URL: https://doi.org/10.1007/s40192-023-00314-6, doi:10.1007/s40192-023-00314-6. This article has 2 citations and is from a peer-reviewed journal.

14. (stander2023carouselanopensource pages 8-11): Sebastian Carrion Ständer, Nora Barschkett, and Evgeniya Kabliman. Carousel: an open-source framework for high-throughput microstructure simulations. Integrating Materials and Manufacturing Innovation, 12:289-300, Oct 2023. URL: https://doi.org/10.1007/s40192-023-00314-6, doi:10.1007/s40192-023-00314-6. This article has 2 citations and is from a peer-reviewed journal.

15. (stander2023carouselanopensource pages 11-12): Sebastian Carrion Ständer, Nora Barschkett, and Evgeniya Kabliman. Carousel: an open-source framework for high-throughput microstructure simulations. Integrating Materials and Manufacturing Innovation, 12:289-300, Oct 2023. URL: https://doi.org/10.1007/s40192-023-00314-6, doi:10.1007/s40192-023-00314-6. This article has 2 citations and is from a peer-reviewed journal.

16. (gao2022amachinelearning pages 1-2): Jianbao Gao, Jing Zhong, Guangchen Liu, Shenglan Yang, Bo Song, Lijun Zhang, and Zuming Liu. A machine learning accelerated distributed task management system (malac-distmas) and its application in high-throughput calphad computation aiming at efficient alloy design. Advanced Powder Materials, 1:100005, Jan 2022. URL: https://doi.org/10.1016/j.apmate.2021.09.005, doi:10.1016/j.apmate.2021.09.005. This article has 57 citations and is from a peer-reviewed journal.

17. (gao2022amachinelearning pages 2-3): Jianbao Gao, Jing Zhong, Guangchen Liu, Shenglan Yang, Bo Song, Lijun Zhang, and Zuming Liu. A machine learning accelerated distributed task management system (malac-distmas) and its application in high-throughput calphad computation aiming at efficient alloy design. Advanced Powder Materials, 1:100005, Jan 2022. URL: https://doi.org/10.1016/j.apmate.2021.09.005, doi:10.1016/j.apmate.2021.09.005. This article has 57 citations and is from a peer-reviewed journal.

18. (zhang2022identificationofthe pages 1-2): Jize Zhang, Rui Wang, and Yujun Zhong. Identification of the eutectic points in the multicomponent systems with the high-throughput calphad approach. Journal of Phase Equilibria and Diffusion, 43:844-857, Oct 2022. URL: https://doi.org/10.1007/s11669-022-01003-1, doi:10.1007/s11669-022-01003-1. This article has 11 citations and is from a peer-reviewed journal.

19. (tripathi2021automatedapproachto pages 1-2): Shivam Tripathi, Lok C. Fan, Michael S. Titus, and Alejandro Strachan. Automated approach to discover coherent precipitates in multi-component shape memory alloys. Computational Materials Science, 197:110651, Sep 2021. URL: https://doi.org/10.1016/j.commatsci.2021.110651, doi:10.1016/j.commatsci.2021.110651. This article has 3 citations and is from a domain leading peer-reviewed journal.

20. (ghassemali2022highthroughputcalphada pages 4-5): Ehsan Ghassemali and Patrick L. J. Conway. High-throughput calphad: a powerful tool towards accelerated metallurgy. Frontiers in Materials, Apr 2022. URL: https://doi.org/10.3389/fmats.2022.889771, doi:10.3389/fmats.2022.889771. This article has 26 citations.

21. (wang2020thermodynamicinvestigationof pages 4-6): Xin Wang, Soumya Sridar, and Wei Xiong. Thermodynamic investigation of new high-strength low-alloy steels with heusler phase strengthening for welding and additive manufacturing: high-throughput calphad calculations and key experiments for database verification. Journal of Phase Equilibria and Diffusion, 41:804-818, Jul 2020. URL: https://doi.org/10.1007/s11669-020-00828-y, doi:10.1007/s11669-020-00828-y. This article has 21 citations and is from a peer-reviewed journal.

22. (vazquez2023adeepneural pages 4-6): G. Vazquez, S. Chakravarty, R. Gurrola, and R. Arróyave. A deep neural network regressor for phase constitution estimation in the high entropy alloy system al-co-cr-fe-mn-nb-ni. npj Computational Materials, 9:1-14, Apr 2023. URL: https://doi.org/10.1038/s41524-023-01021-8, doi:10.1038/s41524-023-01021-8. This article has 31 citations and is from a peer-reviewed journal.

23. (otis2017highthroughputthermodynamicmodeling pages 1-2): Richard A. Otis and Zi-Kui Liu. High-throughput thermodynamic modeling and uncertainty quantification for icme. JOM, 69:886-892, Mar 2017. URL: https://doi.org/10.1007/s11837-017-2318-6, doi:10.1007/s11837-017-2318-6. This article has 59 citations and is from a peer-reviewed journal.

24. (xia2510exaamdanexascaleready pages 9-11): Weiyi Xia, Maxim Moraru, Ying Wai Li, and Cai-Zhuang Wang. Exa-amd: an exascale-ready framework for accelerating the discovery and design of functional materials. ArXiv, Oct 2510. URL: https://doi.org/10.48550/arxiv.2510.01170, doi:10.48550/arxiv.2510.01170. This article has 1 citations.

25. (hicks2024massivelyscalableworkflows pages 4-6): Colton B. Hicks and Todd J. Martinez. Massively scalable workflows for quantum chemistry: bigchem and chemcloud. The Journal of chemical physics, Apr 2024. URL: https://doi.org/10.1063/5.0190834, doi:10.1063/5.0190834. This article has 16 citations.

26. (hicks2024massivelyscalableworkflows pages 9-11): Colton B. Hicks and Todd J. Martinez. Massively scalable workflows for quantum chemistry: bigchem and chemcloud. The Journal of chemical physics, Apr 2024. URL: https://doi.org/10.1063/5.0190834, doi:10.1063/5.0190834. This article has 16 citations.

27. (hicks2024massivelyscalableworkflows pages 21-25): Colton B. Hicks and Todd J. Martinez. Massively scalable workflows for quantum chemistry: bigchem and chemcloud. The Journal of chemical physics, Apr 2024. URL: https://doi.org/10.1063/5.0190834, doi:10.1063/5.0190834. This article has 16 citations.

28. (otis2017highthroughputthermodynamicmodeling pages 3-5): Richard A. Otis and Zi-Kui Liu. High-throughput thermodynamic modeling and uncertainty quantification for icme. JOM, 69:886-892, Mar 2017. URL: https://doi.org/10.1007/s11837-017-2318-6, doi:10.1007/s11837-017-2318-6. This article has 59 citations and is from a peer-reviewed journal.

29. (otis2017highthroughputthermodynamicmodeling pages 5-7): Richard A. Otis and Zi-Kui Liu. High-throughput thermodynamic modeling and uncertainty quantification for icme. JOM, 69:886-892, Mar 2017. URL: https://doi.org/10.1007/s11837-017-2318-6, doi:10.1007/s11837-017-2318-6. This article has 59 citations and is from a peer-reviewed journal.