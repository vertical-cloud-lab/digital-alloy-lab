"""Independent check of make_fins.py's STLs: rebuild each part as a boolean union and compare.

For every row of fins.csv this builds the flange box from Carl's sizes (2026-11-20: 1.25 mm
wide, 12.6 mm deep, 2 mm tall, top face at z = 0 as in Gage's template) and the line box from
the width in the table (not from the STL), unions them with manifold3d, and checks that the
STL encloses the same solid: one watertight body, the right overall size, same volume, and
nothing left over when either solid is subtracted from the other.

    pip install numpy trimesh manifold3d
    python check_fins.py
"""

import csv
import sys
from pathlib import Path

import manifold3d as m3d
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
CX = -0.07  # mm, the template's centre line
FLANGE = ((CX - 1.25 / 2, CX + 1.25 / 2), (-12.6, 0.0), (-2.0, 0.0))  # mm: 1.25 wide, 12.6 deep, 2 tall
FIN_Y, FIN_Z = (-12.6, 0.0), (0.0, 0.05)  # the line runs end to end, 0.05 mm tall


def box(xr, yr, zr):
    size = [xr[1] - xr[0], yr[1] - yr[0], zr[1] - zr[0]]
    return m3d.Manifold.cube(size).translate([xr[0], yr[0], zr[0]])


def to_manifold(mesh):
    return m3d.Manifold(m3d.Mesh(vert_properties=np.asarray(mesh.vertices, dtype=np.float32),
                                 tri_verts=np.asarray(mesh.faces, dtype=np.uint32)))


def main():
    rows = list(csv.DictReader(open(HERE / "fins.csv", newline="", encoding="utf-8")))
    bad = 0
    for r in rows:
        mesh = trimesh.load(HERE / r["file"], process=True)
        w = float(r["rectangle_width_mm"])
        lo, hi = CX - w / 2, CX + w / 2
        ref = box(*FLANGE) + box((lo, hi), FIN_Y, FIN_Z)
        got = to_manifold(mesh)
        extra = (got - ref).volume()
        missing = (ref - got).volume()
        size = mesh.bounds[1] - mesh.bounds[0]
        size_ok = np.allclose(size, [1.25, 12.6, 2.05], atol=1e-5) and np.allclose(mesh.bounds[1][2], 0.05, atol=1e-6)
        ok = (mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
              and len(mesh.split(only_watertight=False)) == 1 and ref.num_vert() > 0 and size_ok
              and r["flange_mm"] == "1.250 x 12.600 x 2.000"
              and abs(mesh.volume - ref.volume()) < 1e-4 and extra < 1e-5 and missing < 1e-5)
        bad += not ok
        print(f"{r['set_name']:28s} {w * 1000:5.0f} um  bodies {len(mesh.split(only_watertight=False))}  "
              f"watertight {mesh.is_watertight}  size {size[0]:.3f} x {size[1]:.3f} x {size[2]:.3f}  "
              f"vol {mesh.volume:.5f} vs union {ref.volume():.5f}  "
              f"extra {extra:.1e}  missing {missing:.1e}  {'ok' if ok else 'FAIL'}")
    print(f"{len(rows) - bad} of {len(rows)} match the boolean union")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
