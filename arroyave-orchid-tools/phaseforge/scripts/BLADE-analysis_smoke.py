"""Smoke test of BLADE's analysis classes (examples 04/05) on SQS made by BLADE-run_sqs_small.py.

The upstream examples 04/05 read CONTCAR/POSCAR files written by the MLIP/TDB stage under
/Users/...; that stage did not run here, so this script converts each mcsqs bestsqs.out
(unrelaxed, ATAT lattice units with a = c = 1, scaled by 3.1 so atoms are not overlapping
in the picture) into POSCAR + CONTCAR inside a BLADE-style tree
<out>/CrHf/HEDB1_2/sqs_lev=N_a_A=x,a_B=y/ and then runs
BLADEVolume.scan_poscars and BladeVisualizer.contcar on it.
Usage: python BLADE-analysis_smoke.py <sqs_parent_dir> <out_dir> <png_path> <csv_path>
"""

import re
import sys
from pathlib import Path

import numpy as np
from pymatgen.core import Lattice, Structure

from blade.analysis.blade_visual import BladeVisualizer
from blade.analysis.blade_volume import BLADEVolume

sqs_parent = Path(sys.argv[1])
out = Path(sys.argv[2])
png = Path(sys.argv[3])
csv = Path(sys.argv[4])
phase_dir = out / "CrHf" / "HEDB1_2"

for best in sorted(sqs_parent.glob("sqsdb_lev=*/bestsqs.out")):
    m = re.match(r"sqsdb_lev=(\d+)_a=([\d.]+),([\d.]+)", best.parent.name)
    lev, xa, xb = m.groups()
    # Parse the ATAT structure file directly: 3 lines coordinate system, 3 lines supercell
    # vectors (in that system), then "x y z species" (in that system). ATAT placeholder
    # species for sublattice 'a' are 'a_A' / 'a_B'; map them to Cr / Hf.
    lines = [ln.split() for ln in best.read_text().splitlines() if ln.strip()]
    axes = np.array([[float(x) for x in ln[:3]] for ln in lines[:3]])
    cell = np.array([[float(x) for x in ln[:3]] for ln in lines[3:6]]) @ axes
    pos = np.array([[float(x) for x in ln[:3]] for ln in lines[6:]]) @ axes
    if any("," in ln[3] for ln in lines[6:]):
        print(f"skip {best.parent.name}: end-member template with multi-species sites")
        continue
    names = [{"a_A": "Cr", "a_B": "Hf"}.get(ln[3], ln[3]) for ln in lines[6:]]
    s = Structure(Lattice(cell * 3.1), names, pos * 3.1, coords_are_cartesian=True)
    s = s.get_sorted_structure()
    d = phase_dir / f"sqs_lev={lev}_a_A={xa},a_B={xb}"
    d.mkdir(parents=True, exist_ok=True)
    s.to(filename=str(d / "POSCAR"), fmt="poscar")
    s.to(filename=str(d / "CONTCAR"), fmt="poscar")
    print(f"wrote {d} ({s.composition.reduced_formula}, {len(s)} atoms)")

vol = BLADEVolume()
df = vol.scan_poscars(out / "CrHf")
print(df.to_string())
df.to_csv(csv, index=False)

viz = BladeVisualizer()
contcars = sorted(phase_dir.glob("sqs_lev=*/CONTCAR"))
viz.contcar(contcars, save=png)
print(f"saved {png}")
