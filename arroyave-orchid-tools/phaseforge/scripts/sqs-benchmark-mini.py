"""Miniature version of the sqs-benchmark mcsqs-vs-random comparison (SCRAPS omitted).

The upstream drivers (examples/tdb_gen_bcc_*.py, sqs-benchmark b44ba79) target a newer BLADE
API than ArroyaveLab/BLADE 9d3859c and fail at BladeCompositions(...). This script keeps the
benchmark's structure definition (equimolar BCC NbVW, a = 3.165 A, 4x3x2 supercell = 48 atoms,
cutoffs = 5th/4th/3rd NN, wr=20, wn=0.75, wd=1) but:
  * mcsqs runs go through BLADE 9d3859c's BladeSQS with its current signature,
    2 parallel mcsqs processes for <seconds> s each (upstream: 20 processes x 100 s);
  * random runs call the repo's own `_write_bestsqs` (+ `_prim_sites`, `_atat_abc`), loaded
    from examples/tdb_gen_bcc_random.py via `ast` without executing the rest of that driver;
  * no MLIP relaxation / TDB fitting (needs the MaterialsFramework fork + an MLIP).
Outputs land where scripts/compare_methods.py looks once its path0/path2/n_runs are patched:
  <root>/BLADE/SQS/BCCmcsqs{i}_3/...      (BladeSQS staging tree, used as compare_methods path2)
  <root>/SCRAPS/BCC_test_2/SQS/BCCrandom{i}_3/sqsdb_lev=0_a=0.33333,0.33333,0.33333/bestsqs.out
Usage: python sqs-benchmark-mini.py <sqs-benchmark checkout> <root> <n_runs> <mcsqs_seconds> [start_index]
"""

import ast
import random
import sys
import time
from pathlib import Path

import numpy as np

from blade.tools import blade_cutoff
from blade.tools.blade_sqsgen import BladeSQS

# BLADE 9d3859c bug workaround: BladeCutoff.get_shells() returns shell radii divided by the
# shortest site-site distance, but BladeSQS passes them to corrdump/mcsqs as absolute
# -2=/-3=/-4= cutoffs. For BCC with a = 3.165 A the pair cutoff became 2.0 A < 1NN (2.74 A),
# corrdump printed "Cluster file contains no clusters." and mcsqs exited with code 1.
# Here every site is a mixing site, so multiplying by the 1NN distance restores Angstrom.
# Set SQSB_NO_CUTOFF_FIX=1 to reproduce the unpatched behaviour.
import os

if not os.environ.get("SQSB_NO_CUTOFF_FIX"):
    _orig_get_shells = blade_cutoff.BladeCutoff.get_shells

    def _abs_shells(self, lattice, frac, rep, tol=1e-4):
        rel = _orig_get_shells(self, lattice, frac, rep, tol)
        frac_sc = blade_cutoff._build_supercell(frac, rep)
        df = blade_cutoff._min_image(frac_sc[1:] - frac_sc[0], rep)
        return rel * float(np.linalg.norm(df @ lattice, axis=1).min())

    blade_cutoff.BladeCutoff.get_shells = _abs_shells

repo = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
n_runs = int(sys.argv[3])
seconds = float(sys.argv[4])
start = int(sys.argv[5]) if len(sys.argv) > 5 else 1  # first run index (to add runs later)

# --- structure definition as in examples/tdb_gen_bcc_mcsqs.py ---
lattice_a = {"V": 3.030, "W": 3.165, "Nb": 3.300}
a_avg = sum(lattice_a.values()) / 3
sqsgen_levels = [{"level": 0, "compositions": [[0.33333, 0.33333, 0.33333]], "letter": ["a"]}]
mcsqs_params = {
    "use_time": True, "time": seconds, "2": 5, "3": 4, "4": 3,
    "wr": 20, "wn": 0.75, "wd": 1, "parallel_runs": 2, "stop_grace": 10,
    "super_cell_size": (4, 3, 2),
}
paths = [root, root / "BLADE", root / "sqsdb"]
for p in paths:
    p.mkdir(parents=True, exist_ok=True)

timings = []
for i in range(start, n_runs + 1):
    key = f"BCCmcsqs{i}"
    phase = {"a": a_avg, "b": a_avg, "c": a_avg, "alpha": 90, "beta": 90, "gamma": 90,
             "vectors": "1 0 0\n0 1 0\n0 0 1\n",
             "coords": "0.000000 0.000000 0.000000 a\n0.500000 0.500000 0.500000 a\n"}
    t0 = time.time()
    sqs = BladeSQS(phases_dict=phase, sqsgen_levels=sqsgen_levels, level=0, len_comp=3)
    sqs.sqs_gen(phase={"lattice": key}, paths=paths, iter=1_000_000, params=mcsqs_params)
    timings.append((key, time.time() - t0))

# --- random baseline using the repo's own writer ---
src = (repo / "examples" / "tdb_gen_bcc_random.py").read_text()
tree = ast.parse(src)
keep = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "_write_bestsqs":
        keep.append(node)
    elif isinstance(node, (ast.Assign, ast.AnnAssign)):
        target = node.targets[0] if isinstance(node, ast.Assign) else node.target
        if isinstance(target, ast.Name) and target.id in {"_prim_sites", "_atat_abc"}:
            keep.append(node)
ns = {"random": random, "np": np, "Path": Path}
exec(compile(ast.Module(body=keep, type_ignores=[]), "tdb_gen_bcc_random.py[subset]", "exec"), ns)
write_bestsqs = ns["_write_bestsqs"]

for i in range(start, n_runs + 1):
    dest = (root / "SCRAPS" / "BCC_test_2" / "SQS" / f"BCCrandom{i}_3"
            / "sqsdb_lev=0_a=0.33333,0.33333,0.33333")
    write_bestsqs(elements=["Nb", "V", "W"], fracs=[1 / 3, 1 / 3, 1 / 3],
                  supercell_size=(4, 3, 2), a=a_avg, dest=dest, seed=i)

for key, dt in timings:
    print(f"timing {key}: {dt:.1f} s")
