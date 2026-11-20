"""Inventory of every machined part of the low-profile desktop LPBF (issue #260, PR #266), for the machining review.

Builds the model (lpbf_low.build, M50 module, fasteners on so joints.py cuts every hole), classifies the parts the way
cad/render_build.py does (machined from stock / sheet-and-weld / bought), and writes, for each machined part:
  <out>/<slug>.brep and <slug>.stl     the solid and a tessellation (0.05 mm chordal) for the CAM and DFM scripts
  <out>/parts.json                     name, material, bbox, volume, the joint keys and hole tools joints.py cut into it

Run:  /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/machining/inventory.py [--cad DIR] [--out DIR]
      --cad defaults to desktop-lpbf/cad (use a frozen copy while someone else edits the model); --out to
      /tmp/mach-work/parts. Takes ~1-2 min.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[3]


def kind(p):
    """Copy of render_build.kind(): 'stock' (machined), 'sheet' (cut, bent, welded), 'bought', 'context', 'fastener'."""
    n = p.name
    if "context" in p.tags:
        return "context"
    if "fastener" in p.tags:
        return "fastener"
    sheet_keys = ("inlet plenum +", "outlet plenum under", "liners", "Dose chute", "Gas knife", "Reservoir M (", "Reservoir M shutter",
                  "Radiation shields", "Laser guard panels", "Sliding guard door", "Rack side panels", "Umbilical duct",
                  "Operator panel box")
    if any(k in n for k in sheet_keys):
        return "sheet"
    if p.mat in ("al6061", "mic6", "macor") and not p.mcm.startswith(("KF", "9572", "TSLOT", "SHEET")):
        return "stock"
    if p.mat == "ss316l" and any(k in n for k in ("Build module", "bottom flange", "Rod end", "Hollow piston rod", "Overflow funnel")):
        return "stock"
    if "Striker" in n:
        return "stock"
    return "bought"


def slug(name):
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s[:60]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cad", default=str(REPO / "desktop-lpbf" / "cad"))
    ap.add_argument("--out", default="/tmp/mach-work/parts")
    ap.add_argument("--module", default="M50")
    a = ap.parse_args()
    sys.path.insert(0, a.cad)
    import cadquery as cq  # noqa
    import joints as J
    import lpbf_low as M
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    parts = M.build(include_tray=False, module=a.module, fasteners=True)
    print(f"built {len(parts)} parts in {time.time() - t0:.0f} s", flush=True)
    rows, counts = [], {}
    # joint key -> fastener part numbers (main + extra), to tell inserts / tapped / dowel holes apart
    key_pns = {k: [r["pn"]] + [pn for pn, _ in r["extra"]] for k, r in J.REGISTRY.items()}
    for i, p in enumerate(parts):
        k = kind(p)
        counts[k] = counts.get(k, 0) + 1
        if k not in ("stock", "sheet"):
            continue
        s = slug(p.name)
        if any(r["slug"] == s for r in rows):
            s = f"{s}_{i}"
        bb = p.shape.BoundingBox()
        cuts = []
        for prefix, lst in J.CUTS.items():
            if p.name.startswith(prefix):
                for key, tool in lst:
                    tb = tool.BoundingBox()
                    cuts.append(dict(key=key, pns=key_pns.get(key, []), bbox=[tb.xmin, tb.xmax, tb.ymin, tb.ymax, tb.zmin, tb.zmax]))
        row = dict(i=i, slug=s, name=p.name, kind=k, mat=p.mat, bom=p.bom, mcm=p.mcm, module=p.module, step=p.step,
                   n_solids=len(p.shape.Solids()), volume_mm3=p.shape.Volume(), area_mm2=p.shape.Area(),
                   bbox=[bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax], cuts=cuts)
        if k == "stock":
            p.shape.exportBrep(str(out / f"{s}.brep"))
            cq.exporters.export(cq.Workplane().add(p.shape), str(out / f"{s}.stl"), tolerance=0.05, angularTolerance=0.15)
        rows.append(row)
        print(f"{k:6s} {s:60s} {p.mat:7s} {bb.xlen:7.1f} x {bb.ylen:7.1f} x {bb.zlen:7.1f}", flush=True)
    meta = dict(module=a.module, counts=counts, built_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                cad=str(a.cad), parts=rows)
    (out / "parts.json").write_text(json.dumps(meta, indent=1))
    print(counts, f"{time.time() - t0:.0f} s total")


if __name__ == "__main__":
    main()
