"""CalculiX check of the drop-down door as a seal carrier (issue #260, PR #266).

The door FEA in analysis/fea/fea.py (case 3) loads the door with the atmosphere at vacuum and puts it on its land.
What it leaves out is the O-ring itself: squeezing a 3.53 mm FKM 75A cord 25 % along the door's ~670 mm seal path
takes ~2.8 kN (analysis/seals/seals.py, Lindley), more than the 2.4 kN the atmosphere puts on the door at full
vacuum, and at +20 mbar during a build only the two latches and the two hinges hold the door against it.

So here the door is held where it really is held (two draw latches at its top corners, two hinges at its bottom
edge), the O-ring reaction is applied to the groove floor and +20 mbar to the face inside the seal, and the door's
outward deflection along the groove floor is read as squeeze lost. Two cords: 3.53 mm (as drawn) and 1.78 mm.

Run:  OMP_NUM_THREADS=2 python desktop-lpbf/analysis/seals/door_seal_fea.py  ->  analysis/out/seals/door_seal_fea.{json,md,png}
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "fea"))
sys.path.insert(0, str(HERE))
import fea as F          # noqa: E402  (meshing, CalculiX I/O and rendering helpers)
import seals as SE       # noqa: E402  (Lindley load per length)

OUT = ROOT / "analysis" / "out" / "seals"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    parts = F.M.build()
    P = F.P
    cy = P["cy"]
    dy1, dy0 = -cy, -cy - 15.0
    door = F.part(parts, "Chamber door").shape
    m = F.mesh_shape(door, "door_seal", hmax=4.0, hmin=1.0)
    groove_floor = F.surfaces(m, F.planar("y", dy1 - 2.8))
    back = F.surfaces(m, F.planar("y", dy1))
    front = F.surfaces(m, F.planar("y", dy0))
    f_groove = F.faces_on(m, groove_floor)
    f_inside = F.faces_on(m, back, lambda c: (np.abs(c[:, 0]) <= 114) & (c[:, 2] >= 4) & (c[:, 2] <= 104))
    latch = F.nodes_on(m, front, lambda q: (np.abs(q[:, 0]) >= 100) & (np.abs(q[:, 0]) <= 124) & (q[:, 2] >= 92) & (q[:, 2] <= 110))
    hinge = F.nodes_on(m, front, lambda q: (np.abs(q[:, 0]) >= 80) & (np.abs(q[:, 0]) <= 100) & (q[:, 2] <= 30))
    if min(len(f_groove["el"]), len(latch), len(hinge)) == 0:
        raise RuntimeError("selection empty")
    a_groove = f_groove["area"].sum()
    path = 2 * (232.0 + 104.0) - (8 - 2 * np.pi) * 5.0                 # centre line, as seals.py
    gn = m["idx"][np.unique(f_groove["tri"].ravel())]
    xyz_g = m["xyz"][gn]
    px = F.nearest(m, (0.0, dy0, 101.0), latch)
    R = dict(path_mm=path, groove_floor_area_mm2=a_groove, nodes=len(m["ntags"]), elements=len(m["tets"]), cases=[])
    for cs, label in ((3.53, "3.53 mm cord at 25 % (as drawn)"), (1.78, "1.78 mm cord at 25 %")):
        F_or = SE.lindley(cs, 0.25) * path
        p_or = F_or / a_groove
        job = f"door_seal_{str(cs).replace('.', 'p')}"
        F.write_model(job, m, F.AL, F.nset("LATCH", latch) + F.nset("HINGE", hinge))
        bc = "LATCH,2,2\nHINGE,2,3\n" + f"{px},1,1\n"
        loads = "*DLOAD\n" + F.dload_lines(f_groove, p_or) + F.dload_lines(f_inside, 0.002)
        F.append(job, F.static_step(bc, loads))
        F.run_ccx(job)
        U, S, vm = F.static_results(m, job)
        uy = U[gn, 1]                     # negative = away from the chamber face = squeeze lost
        lost = -uy.min()
        i = int(np.argmin(uy))
        squeeze_mm = 0.25 * cs
        min15 = 0.15 * cs
        r = dict(cord=cs, label=label, F_oring_N=F_or, F_overpressure_N=0.002 * f_inside["area"].sum(),
                 squeeze_mm=squeeze_mm, lost_max_um=1000 * lost, lost_at=xyz_g[i].tolist(),
                 margin_to_15pct_um=1000 * (squeeze_mm - min15), vm_max=float(vm.max()),
                 latch_reaction_N=None, ok=bool(lost < squeeze_mm - min15))
        # reactions: total load is carried by latches + hinges; split by moment about the hinge line (z = -12)
        z_l, z_or = 101.0, 52.0
        r["latch_load_each_N"] = (F_or + r["F_overpressure_N"]) * (z_or + 12) / (z_l + 12) / 2
        r["hinge_load_each_N"] = (F_or + r["F_overpressure_N"]) / 2 - r["latch_load_each_N"]
        R["cases"].append(r)
        png = f"door_seal_{str(cs).replace('.', 'p')}.png"
        F.render(m, U, -U[:, 1] * 1000, OUT / png, f"Door held at latches and hinges: {label}, +20 mbar\n"
                 f"squeeze lost along the groove up to {1000 * lost:.0f} um (margin to 15 % squeeze {1000 * (squeeze_mm - min15):.0f} um)",
                 (-0.8, -1.5, 0.6), label="outward deflection (um)", mark=xyz_g[i])
        r["png"] = png
        print(f"  {label}: O-ring {F_or:.0f} N, max squeeze lost {1000 * lost:.0f} um at {np.round(xyz_g[i], 0)}, latch {r['latch_load_each_N']:.0f} N each")
    (OUT / "door_seal_fea.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    L = ["# Door as a seal carrier: CalculiX, held at its latches and hinges", "",
         f"Door: 6061-T6, 15 mm, from `cad/lpbf_low.py`. C3D10 mesh, {R['nodes']} nodes. Seal centre line {path:.0f} mm; "
         "O-ring reaction (Lindley, FKM 75A, 25 % squeeze) as a uniform pressure on the groove floor, +20 mbar on the face inside the seal; "
         "latch pads (top corners) held in y, hinge leaves (bottom) held in y and z.", "",
         "| Cord | O-ring reaction | Each latch | Each hinge | Squeeze lost, worst point | Margin to 15 % squeeze | Result |", "|---|---|---|---|---|---|---|"]
    for r in R["cases"]:
        L.append(f"| {r['label']} | {r['F_oring_N']:.0f} N | {r['latch_load_each_N']:.0f} N | {r['hinge_load_each_N']:.0f} N | {r['lost_max_um']:.0f} µm at x {r['lost_at'][0]:.0f}, z {r['lost_at'][2]:.0f} | "
                 f"{r['margin_to_15pct_um']:.0f} µm | {'OK' if r['ok'] else 'FAILS'} |")
    (OUT / "door_seal_fea.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
