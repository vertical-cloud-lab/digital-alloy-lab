"""Stock removal per setup for the five detailed parts (the frame, the floor plate, the lid, the door, the M50 module body) (cam_sim.py's simulation, standard + long tools).

For each setup direction: the volume that setup can remove, and the volume no other setup can remove (what makes the
setup necessary). Run after inventory.py:
  OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/per_setup.py
Writes desktop-lpbf/analysis/out/machining/per_setup.json (~4 min).
"""
import json
import os
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cam_sim as CS  # noqa: E402

PARTS = pathlib.Path(os.environ.get("MACH_PARTS", "/tmp/mach-work/parts"))


def main():
    meta = json.load(open(PARTS / "parts.json"))
    P = {p["slug"]: p for p in meta["parts"] if p["kind"] == "stock"}
    out = {}
    for pre, pitch, sbox, core in (("process_chamber_body", 0.5, [-165.1, 165.1, -120.65, 120.65, -11.8, 127.9], [-137.0, 137.0, -92.0, 92.0]),
                                   ("chamber_floor_plate", 0.4, [-165.1, 165.1, -120.65, 120.65, -22.7, 2.7], None),
                                   ("chamber_lid", 0.4, None, None), ("chamber_door", 0.4, None, None), ("build_module_m50_spigot", 0.4, None, None)):
        slug = next(s for s in P if s.startswith(pre))
        b = P[slug]["bbox"]
        sbox = sbox or [b[0] - 3, b[1] + 3, b[2] - 3, b[3] + 3, b[4] - 3, b[5] + 3]
        tris = CS.read_stl(str(PARTS / f"{slug}.stl"))
        lo, shape = CS.grid_for(tris, pitch, 4.0, sbox)
        vox, _ = CS.voxelize(tris, pitch, lo, shape)
        st = CS.stock_mask(lo, shape, pitch, sbox)
        if core is not None:                                   # the frame's core leaves as a slug before milling
            st &= ~CS.stock_mask(lo, shape, pitch, list(core) + [-1e9, 1e9])
        st |= vox
        waste = st & ~vox
        per = {}
        for d in CS.DIRS:
            m = np.zeros_like(vox)
            for name, (D, L, H, _) in CS.TOOLS.items():
                r, _ = CS.removable(CS.to_setup(vox, d), pitch, D, L, H)
                m |= CS.from_setup(r, d)
            per[d] = m & waste
        v = pitch ** 3
        rows = {}
        for d in CS.DIRS:
            others = np.logical_or.reduce([per[e] for e in CS.DIRS if e != d])
            rows[d] = dict(removable_cm3=round(float(per[d].sum() * v / 1000), 1), only_this_setup_cm3=round(float((per[d] & ~others).sum() * v / 1000), 2))
        out[pre] = dict(waste_cm3=round(float(waste.sum() * v / 1000), 1), setups=rows)
        print(pre, out[pre], flush=True)
    (CS.OUT / "per_setup.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
