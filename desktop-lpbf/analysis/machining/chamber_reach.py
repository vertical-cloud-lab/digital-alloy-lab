"""Chamber pocket reach check with the tool lengths actually found for sale (cam_sim.py's simulation, chamber body only).

The tooling search (tooling-bom.csv) found 3/4 in. and 1 in. carbide end mills only up to 5 in. overall length at
Lakeshore Carbide, not the 6 in. assumed in cam_sim.TOOLS. This reruns the chamber body with
  A  "long, 5 in. OAL": 1 in. and 3/4 in. at 5 in. OAL (~92 mm stick-out), 1/2 x 4 in., 3/8 x 4 in., 1/4 x 4 in.
  B  A + a slim shrink-fit / ER extension holder (32 mm nose, 160 mm gauge length) carrying a 1/2 in. end mill
     with 150 mm stick-out, and a 3/8 in. at 150 mm (finishing only)
and writes analysis/out/machining/chamber_reach.json and cam_chamber_reach_5in.png.
Run: OMP_NUM_THREADS=1 /tmp/capmem 3 xvfb-run -a -s "-screen 0 1600x1024x24" /tmp/venv/bin/python desktop-lpbf/analysis/machining/chamber_reach.py
"""
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cam_sim as CS  # noqa: E402

PARTS = pathlib.Path("/tmp/mach-work/parts")
STD = {k: v for k, v in CS.TOOLS.items() if v[3] == "std"}
LONG5 = dict(STD, **{"1 x 5 in. OAL": (25.4, 92.0, 63.0, "long"), "3/4 x 5 in. OAL": (19.05, 92.0, 50.0, "long"),
                     "1/2 x 4 in. OAL": (12.7, 64.0, 50.0, "long"), "3/8 x 4 in. OAL": (9.525, 64.0, 50.0, "long"),
                     "1/4 x 4 in. OAL": (6.35, 70.0, 35.0, "long")})
EXT = dict(LONG5, **{"1/2 in. in a 32 mm extension, 150 mm": (12.7, 150.0, 32.0, "ext"),
                     "3/8 in. in a 32 mm extension, 150 mm": (9.525, 150.0, 32.0, "ext")})


def main():
    slug = "process_chamber_body_6061_t6_6_4_l"
    tris = CS.read_stl(str(PARTS / f"{slug}.stl"))
    sbox = [-165.1, 165.1, -120.65, 120.65, -26.2, 126.2]
    out = {}
    for label, tools in (("long_5in_OAL", LONG5), ("long_5in_plus_extension", EXT)):
        sim = CS.simulate(tris, 0.5, sbox, tools)
        v = 0.125
        res = sim["res"]
        idx = np.argwhere(res)
        xyz = sim["lo"] + 0.5 * (idx + 0.5)
        inside = (np.abs(xyz[:, 0]) < 140.5) & (np.abs(xyz[:, 1]) < 95.5) & (xyz[:, 2] > -0.5)
        near_wall = inside & ((140 - np.abs(xyz[:, 0]) < 25) | (95 - np.abs(xyz[:, 1]) < 25)) & (xyz[:, 2] > 6)
        out[label] = dict(residual_cm3=round(float(res.sum() * v / 1000), 2),
                          wall_band_cm3=round(float(near_wall.sum() * v / 1000), 2),
                          wall_band_z_max=round(float(xyz[near_wall, 2].max()), 1) if near_wall.any() else None)
        print(label, out[label], flush=True)
        if label == "long_5in_OAL":
            sim.update(pitch=0.5, stl=str(PARTS / f"{slug}.stl"))
            CS.render(slug, sim, CS.OUT / "cam_chamber_reach_5in.png",
                      f"Process chamber body, 3-axis, standard + 5 in. OAL tools (longest found for sale): residual {out[label]['residual_cm3']:.1f} cm3 (red)")
    (CS.OUT / "chamber_reach.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
