"""Export the chamber's body parts for print and fabrication quotes (manufacturing-route.md, round 7).

Writes, into --out (default /tmp/route/parts), each as STEP (mm) and STL (0.1 mm linear deflection), moved so the bounding
box starts at the origin:
  frame            the through-frame as drawn ("Process chamber body ...", 6061 in the model)
  floor            the bolted floor plate ("Chamber floor plate ...")
  lid, door        the lid and the drop-down door
  body_one_piece   frame + floor plate fused into one body: what a printed (or cast) chamber would be, with no floor joint.
                   The floor O-ring groove, the floor screws' holes and notches stay in the solid as drawn (a print would
                   leave them out); it is for volume and bounding box, which set a print or casting price.
and chamber_parts.json: volume, bounding box, surface area and mass in 316L / AlSi10Mg / 6061 for each.

Run:  /tmp/capmem 1500M /tmp/venv/bin/python desktop-lpbf/analysis/route/export_chamber.py [--out DIR]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parents[1] / "cad"
RHO = {"316L": 7990.0, "AlSi10Mg": 2670.0, "6061": 2700.0}   # kg/m3
WANT = {"frame": "Process chamber body", "floor": "Chamber floor plate", "lid": "Chamber lid", "door": "Chamber door"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/route/parts")
    a = ap.parse_args()
    sys.path.insert(0, str(CAD))
    import cadquery as cq
    import lpbf_low as M
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    parts = M.build(include_tray=False, module="M50", fasteners=False)
    print(f"built {len(parts)} parts in {time.time() - t0:.0f} s", flush=True)
    got = {}
    for key, prefix in WANT.items():
        hit = [p for p in parts if p.name.startswith(prefix)]
        if not hit:
            print("not found:", prefix)
            continue
        got[key] = hit[0]
    shapes = {k: p.shape for k, p in got.items()}
    if "frame" in shapes and "floor" in shapes:
        shapes["body_one_piece"] = shapes["frame"].fuse(shapes["floor"]).clean()
    rows = {}
    for key, shp in shapes.items():
        sols = shp.Solids()
        big = max(sols, key=lambda s: s.Volume())
        bb = shp.BoundingBox()
        moved = shp.translate(cq.Vector(-bb.xmin, -bb.ymin, -bb.zmin))
        step, stl = out / f"{key}.step", out / f"{key}.stl"
        cq.exporters.export(cq.Workplane().add(moved), str(step))
        cq.exporters.export(cq.Workplane().add(moved), str(stl), tolerance=0.1, angularTolerance=0.2)
        vol = sum(s.Volume() for s in sols)
        rows[key] = dict(name=got[key].name if key in got else "frame + floor plate fused (one-piece body)",
                         solids=len(sols), largest_solid_cm3=round(big.Volume() / 1e3, 1), volume_cm3=round(vol / 1e3, 1),
                         area_cm2=round(sum(s.Area() for s in sols) / 1e2, 1),
                         bbox_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
                         bbox_volume_cm3=round(bb.xlen * bb.ylen * bb.zlen / 1e3, 1),
                         mass_kg={m: round(vol * 1e-9 * r, 2) for m, r in RHO.items()},
                         files=[step.name, stl.name], step_bytes=step.stat().st_size, stl_bytes=stl.stat().st_size)
        print(key, rows[key], flush=True)
    (out / "chamber_parts.json").write_text(json.dumps(dict(built_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                                                            parts=rows), indent=1))
    print("wrote", out, f"in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
