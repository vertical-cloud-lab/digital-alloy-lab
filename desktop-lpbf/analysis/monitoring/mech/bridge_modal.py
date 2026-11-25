"""Optics bridge with a cut-out for the steep lid camera (LP): does the camera need one, and what does it do to the modes?

The steep camera (monitoring_spec LP + LID_CAMERA) sits on the lid port's sight line, outside the lid. Its body can reach the
25 mm optics bridge (z_bridge0..z_bridge1 in lpbf_low.P). This script
  1. puts the camera envelope (a cylinder on the sight line from the lens front to the camera's back, radius = the body's
     half-diagonal + 3 mm) at each LP candidate in monitoring_spec and measures how much of it falls in the bridge, in the
     reservoir slot (which the reservoirs slide out through) and in the plate itself;
  2. cuts the bridge with that envelope where it hits the plate, and re-runs fea.py's case 6 (bridge + posts, the galvo,
     lens, shutter, collimator and tap as rigid masses, post feet fixed; modes with SPOOLES) on the cut bridge, against the
     same case on the uncut bridge with the same mesh.

It drives fea.py's own case6 (no copy of its masses or constraints): the bridge part is swapped for the cut one.

Run:  OMP_NUM_THREADS=2 xvfb-run -a -s "-screen 0 1280x960x24" /tmp/venv/bin/python \
          desktop-lpbf/analysis/monitoring/mech/bridge_modal.py [--mesh 12,3,6] [--only spec,back]
Needs ccx (CalculiX 2.21: apt install calculix-ccx). Scratch in /tmp/mech-fea-run; results in
analysis/out/monitoring/mech/bridge_modal.json (+ mode-1 PNGs in analysis/out/monitoring/mech/bridge_fea/).
Memory: ~2-3 GB at hmax 12 (SPOOLES); cap it (prlimit or /tmp/capmem).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                                   # desktop-lpbf
OUT = ROOT / "analysis" / "out" / "monitoring" / "mech"
os.environ.setdefault("FEA_RUN", "/tmp/mech-fea-run")
sys.path.insert(0, str(ROOT / "analysis" / "fea"))
sys.path.insert(0, str(ROOT / "cad"))
sys.path.insert(0, str(HERE))
import cadquery as cq  # noqa: E402
import fea as F  # noqa: E402
import monitoring_spec as MS  # noqa: E402
import mech_inputs as MI  # noqa: E402

M = F.M
P = M.P


def lp_envelope(centre, clearance=3.0, standoff=None):
    """Camera + lens envelope on the LP sight line: (solid, dict of the numbers used)."""
    e = MI.lp_camera_envelope(centre, standoff)
    u = cq.Vector(*e["axis_out"])
    p0 = cq.Vector(*e["front_xyz"])
    solid = cq.Solid.makeCylinder(e["radius_mm"] + clearance, e["length_mm"], p0, u)
    return solid, e


def slab(z0, z1):
    return cq.Solid.makeBox(2000, 2000, z1 - z0, cq.Vector(-1000, -1000, z0))


def vol(s):
    try:
        return float(s.Volume())
    except Exception:
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mesh", default=os.environ.get("FEA_C6_MESH", "12,3,6"))
    ap.add_argument("--only", default="base,spec,back")
    ap.add_argument("--sweep", action="store_true", help="only the envelope vs lens-front standoff sweep (no FEA): bridge_sweep.json")
    a = ap.parse_args()
    os.environ["FEA_C6_MESH"] = a.mesh
    os.environ["FEA_C6_ONLY"] = "b"
    OUT.mkdir(parents=True, exist_ok=True)
    F.OUT = OUT / "bridge_fea"
    F.OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    parts = M.build()
    print(f"model built in {time.time() - t0:.0f} s")
    br = F.part(parts, "Optics bridge (")
    zb0, zb1 = P["z_bridge0"], P["z_bridge1"]
    xd = P["x_dose"]
    slot = cq.Solid.makeBox(56.0, 251.0, zb1 - zb0 + 2, cq.Vector(xd - 28, -191, zb0 - 1))   # lpbf_low: the reservoir slot
    cands = {"spec": tuple(MS.VIEWPORTS["LP"]["centre"])}
    back = [c for c in MS.VIEWPORTS["LP"].get("candidates", []) if c[1] > 0]
    if back:
        cands["back"] = tuple(back[0])
    if a.sweep:
        sw = dict(run_utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), model_commit=F.model_commit(), rows=[])
        for tag, c in cands.items():
            for so in (5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0):
                env, e = lp_envelope(c, standoff=so)
                in_slab = env.intersect(slab(zb0, zb1))
                sw["rows"].append(dict(candidate=tag, centre=c, standoff_mm=so, back_z=e["back_xyz"][2],
                                       in_bridge_level_cm3=vol(in_slab) / 1e3,
                                       in_slot_cm3=(vol(in_slab.intersect(slot)) / 1e3) if vol(in_slab) > 0 else 0.0,
                                       in_plate_cm3=vol(env.intersect(br.shape)) / 1e3))
                print(sw["rows"][-1])
        (OUT / "bridge_sweep.json").write_text(json.dumps(sw, indent=1, default=float))
        return
    res = dict(mesh=a.mesh, run_utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), model_commit=F.model_commit(),
               bridge=dict(z=(zb0, zb1), slot_x=(xd - 28, xd + 28), slot_y=(-191, 60)), candidates={}, variants={})
    for tag, c in cands.items():
        env, e = lp_envelope(c)
        in_slab = env.intersect(slab(zb0, zb1))
        in_plate = env.intersect(br.shape)
        in_slot = in_slab.intersect(slot) if vol(in_slab) > 0 else None
        bb = in_plate.BoundingBox() if vol(in_plate) > 0 else None
        res["candidates"][tag] = dict(centre=c, envelope=e, vol_in_bridge_level_cm3=vol(in_slab) / 1e3,
                                      vol_in_reservoir_slot_cm3=(vol(in_slot) / 1e3) if in_slot is not None else 0.0,
                                      vol_in_plate_cm3=vol(in_plate) / 1e3,
                                      cut_bbox_xy=None if bb is None else [round(bb.xmin, 1), round(bb.xmax, 1), round(bb.ymin, 1), round(bb.ymax, 1)])
        print(tag, c, {k: v for k, v in res["candidates"][tag].items() if k != "envelope"})
    only = a.only.split(",")
    shapes = {"base": br.shape}
    for tag in cands:
        if res["candidates"][tag]["vol_in_plate_cm3"] > 0.01:
            env, _ = lp_envelope(cands[tag])
            shapes[tag] = br.shape.cut(env).clean()
    for tag, shp in shapes.items():
        if tag not in only:
            continue
        p2 = [dataclasses.replace(p, shape=shp) if p is br else p for p in parts]
        R = {}
        t1 = time.time()
        F.case6(p2, R)
        v = R["6"]["variants"][0]
        res["variants"][tag] = dict(removed_cm3=(vol(br.shape) - vol(shp)) / 1e3, nodes=v["nodes"],
                                    f_hz=[m_["f_hz"] for m_ in v["modes"]], modes=v["modes"], gravity=v["gravity"],
                                    seconds=round(time.time() - t1))
        png = OUT / "bridge_fea" / "c6b_bridge_mode1.png"
        if png.exists():
            png.rename(OUT / "bridge_fea" / f"bridge_mode1_{tag}.png")
        (OUT / "bridge_modal.json").write_text(json.dumps(res, indent=1, default=float))
        print(f"{tag}: f = {[round(x, 1) for x in res['variants'][tag]['f_hz']]} Hz ({time.time() - t1:.0f} s)")
    (OUT / "bridge_modal.json").write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
