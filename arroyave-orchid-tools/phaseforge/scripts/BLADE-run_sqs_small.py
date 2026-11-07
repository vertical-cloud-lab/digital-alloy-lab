"""Shrunken version of BLADE examples/02_sqs_generation.py for a shared 4-vCPU CI runner.

Differences from the upstream example (BLADE 9d3859c):
  * BladeCompositions is called with the current keyword names (primary_elements=...,
    primary_min=...); the upstream example still uses transition_metals=/rare_earths=/tm_min=...,
    which raise TypeError.
  * Paths point at a scratch directory instead of the author's /Users/... tree.
  * Binary systems only (Cr-Hf diboride, len_comp=2, level=3 -> sqsgen levels 0,1,2,5),
    2x2x2 supercell (24 atoms: 8 metal + 16 B), 2 mcsqs processes (-ip=1,2), 10 s per directory.
    With only 1 process, ATAT 3.52 `mcsqs -best` never writes bestsqs.out (see section text).
Usage: python BLADE-run_sqs_small.py <scratch_dir> [mcsqs_seconds] [parallel_runs]
"""

import sys
import time
from pathlib import Path

from blade.tools.blade_compositions import BladeCompositions
from blade.tools.blade_sqsgen import BladeSQS

scratch = Path(sys.argv[1]).resolve()
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 10
n_parallel = int(sys.argv[3]) if len(sys.argv) > 3 else 2
path0 = scratch
path1 = scratch / "BLADE"
path2 = scratch / "sqsdb"
for p in (path1, path2):
    p.mkdir(parents=True, exist_ok=True)
paths = [path0, path1, path2]

# Phase prototype copied from examples/02_sqs_generation.py (HEDB1, AlB2-type, a-sublattice mixing)
phases = {
    "HEDB1": {
        "a": 1, "b": 1, "c": 1, "alpha": 90, "beta": 90, "gamma": 120,
        "vectors": "1 0 0\n0 1 0\n0 0 1\n",
        "coords": (
            "0.000000 0.000000 0.000000 a\n"
            "0.333333 0.666667 0.500000 B\n"
            "0.666667 0.333333 0.500000 B\n"
        ),
    }
}
phase_list = [{"generator_name": "HEDB", "lattice": "HEDB1", "supercell_size": (2, 2, 2)}]

sqsgen_levels = [
    {"level": 0, "compositions": [[1.0, 0.0]], "letter": ["a"]},
    {"level": 1, "compositions": [[0.5, 0.5]], "letter": ["a"]},
    {"level": 2, "compositions": [[0.75, 0.25]], "letter": ["a"]},
    {"level": 3, "compositions": [[0.33333, 0.33333, 0.33333]], "letter": ["a"]},
    {"level": 4, "compositions": [[0.5, 0.25, 0.25]], "letter": ["a"]},
    {"level": 5, "compositions": [[0.875, 0.125], [0.625, 0.375]], "letter": ["a"]},
    {"level": 6, "compositions": [[0.75, 0.125, 0.125]], "letter": ["a"]},
]

mcsqs_params = {
    "use_time": True,
    "time": seconds,
    "2": 5,
    "3": 4,
    "4": 3,
    "wr": 20,
    "wn": 0.75,
    "wd": 1,
    "parallel_runs": n_parallel,
    "stop_grace": 10,
}

composer = BladeCompositions(
    primary_elements=["Cr", "Hf"],
    secondary_elements=[],
    system_size=2,
    primary_min=2,
    primary_max=2,
    secondary_min=0,
    secondary_max=0,
    allow_lower_order=False,
)
composition_list = composer.generate_compositions()
unique_len_comps = composer.get_systems()
print(f"Compositions: {composition_list}")
print(f"System sizes: {unique_len_comps}")

level = 3
t0 = time.time()
for specific_phase in phase_list:
    for len_comp in unique_len_comps:
        sqs_gen = BladeSQS(
            phases_dict=phases[specific_phase["lattice"]],
            sqsgen_levels=sqsgen_levels,
            level=level,
            len_comp=len_comp,
            skip_existing_sqs=False,
        )
        params = mcsqs_params | {"super_cell_size": specific_phase["supercell_size"]}
        sqs_gen.sqs_gen(phase=specific_phase, paths=paths, iter=1_000_000, params=params)
print(f"BladeSQS.sqs_gen wall time: {time.time() - t0:.1f} s")
