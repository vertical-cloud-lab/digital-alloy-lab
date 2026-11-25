"""Cache the chamber frame's and floor plate's cut states for the robot-shop chapters (round 7, issue #260, PR #266).

render_machining.py cuts the model's own parts (lpbf_low.CHAMBER_OPS: each part's saw-cut blank and the solid every
operation removes, in order; joints.CUTS for the drilled and tapped holes) setup by setup, and its last state reproduces
the model's part to 0.000 % in volume. The shop chapters show the same states inside the VF-4, so this script runs that
sequence once (it needs the whole model built, ~1-2 min) and writes each state as a mesh in the model frame:

    /tmp/robotbuild/cache/shop/chamber/<part>_<k>.vtp        (k = 0 is the CAM blank)
    /tmp/robotbuild/cache/shop/chamber/states.json           [{part, k, setup, on, fc, rots, index_deg, key, label, file}]

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/shop_chamber_cache.py
"""
from __future__ import annotations

import json
import pathlib
import sys
import time
import types

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parent
sys.path.insert(0, str(CAD))

import cadquery as cq  # noqa: E402
import numpy as np  # noqa: E402
import pyvista as pv  # noqa: E402

OUT = pathlib.Path("/tmp/robotbuild/cache/shop/chamber")


def tess(shape, tol=0.35, ang=0.35):
    vs, fs = shape.tessellate(tol, ang)
    v = np.array([(p.x, p.y, p.z) for p in vs], float)
    f = np.array(fs, np.int64)
    return pv.PolyData(v, np.c_[np.full(len(f), 3), f].ravel()).clean()


def main():
    t0 = time.time()
    import joints as J
    import lpbf_low as M
    import render_machining as RM
    parts = M.build(module="M50")
    print(f"model: {len(parts)} parts in {time.time() - t0:.0f} s", flush=True)
    RB = types.SimpleNamespace(M=M, J=J)
    plan = RM.load_plan()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    final = {p.name.split(" (")[0]: p.shape for p in parts if p.name.startswith(("Process chamber body", "Chamber floor plate"))}
    for part in ("frame", "floor"):
        info = M.CHAMBER_OPS[part]
        state = RM.cam_blank(part, info["blank"])
        k = 0
        tess(state).save(OUT / f"{part}_{k}.vtp")
        rows.append(dict(part=part, k=k, setup="blank", on="", fc="", rots=[], index_deg=None, key="", label="CAM blank",
                         file=f"{part}_{k}.vtp", cm3=round(state.Volume() / 1000, 2)))
        used_j = set()
        for su in plan[part]:
            sid = su["title"].split(",")[0]
            seq = [(None, su["ops"])] if su["on"] != "rotary" else [(a, ks) for a, ks in su["index"]]
            for ang, keys in seq:
                for key in keys:
                    tools, cuts = RM.op_tools(RB, part, key)
                    if cuts is not None:
                        cand = [(kk, tt) for kk, tt in cuts if kk not in used_j]
                        tools = [tt for _, tt in cand]
                        used_j |= {kk for kk, _ in cand}
                    elif key.startswith("J:"):
                        used_j.add(key[2:])
                    if not tools:
                        continue
                    after = state.cut(*tools)
                    removed = state.Volume() - after.Volume()
                    state = after
                    k += 1
                    tess(state).save(OUT / f"{part}_{k}.vtp")
                    rows.append(dict(part=part, k=k, setup=sid, on=su["on"], fc=su.get("fc", ""), rots=su.get("rots", []),
                                     index_deg=ang, key=key, label=RM.op_label(RB, part, key), file=f"{part}_{k}.vtp",
                                     cm3=round(state.Volume() / 1000, 2), removed_cm3=round(removed / 1000, 2)))
                    print(part, k, sid, ang, key, round(removed / 1000, 1), "cm3", f"{time.time() - t0:.0f} s", flush=True)
        name = "Process chamber body" if part == "frame" else "Chamber floor plate"
        fin = next(v for n, v in final.items() if n.startswith(name))
        dv = abs(state.Volume() - fin.Volume()) / fin.Volume()
        rows.append(dict(part=part, check_volume_frac=dv))
        print(f"{part}: last state vs the model's part {100 * dv:.3f} % in volume", flush=True)
    # The robot shop's variant of the frame (round 7): no waterjet in the shop, so the core is trepanned on the VF-4 with
    # the 3/4 in. end mill from both sides (setup_plan.json's F-S0 lists "trepanned from both sides with the 3/4 in. end
    # mill" as the alternative to the waterjet): the lower half of a 19.05 mm kerf inside the 274 x 184 slug outline in
    # F-S1, the upper half in F-S2, which frees a 235.9 x 145.9 mm core. The rest is the plan's ops. Saved as frameT_<k>
    # plus frameT_core.vtp, and checked against the model's part like the plan.
    FR, P = M.FRAME, M.P
    co, ix, iy = FR["core_off"], P["ix"], P["iy"]
    zm = (-FR["skirt"] + P["lid_z0"]) / 2
    kerf = 19.05
    outer = M.rbox(-ix + co, ix - co, -iy + co, iy - co, -200.0, 300.0, FR["r_in"] - co)
    cx, cy = ix - co - kerf, iy - co - kerf
    core_box = cq.Solid.makeBox(2 * cx, 2 * cy, 500.0, cq.Vector(-cx, -cy, -200.0))
    ring = outer.cut(core_box)
    big = 2000.0
    lower = cq.Solid.makeBox(2 * big, 2 * big, big, cq.Vector(-big, -big, zm - big))
    upper = cq.Solid.makeBox(2 * big, 2 * big, big, cq.Vector(-big, -big, zm))
    variant = [("F-S1", ["TR<", "FR-01<", "FR-04", "FR-05", "J:floor", "J:floor_dowels"]),
               ("F-S2", ["TR>", "FR-01>", "FR-03", "FR-06", "J:lid"])]
    rows_t = []
    state = RM.cam_blank("frame", M.CHAMBER_OPS["frame"]["blank"])
    k = 0
    tess(state).save(OUT / f"frameT_{k}.vtp")
    rows_t.append(dict(part="frameT", k=0, setup="blank", key="", label="CAM blank", file="frameT_0.vtp",
                       cm3=round(state.Volume() / 1000, 2)))
    used_j = set()
    core = None
    for sid, keys in variant:
        su = next(s for s in plan["frame"] if s["title"].startswith(sid))
        for key in keys:
            if key in ("TR<", "TR>"):
                tools = [ring.intersect(lower if key == "TR<" else upper)]
                label = (f"trepan the core with the 3/4 in. end mill, {'lower' if key == 'TR<' else 'upper'} half: a 19.05 mm "
                         f"kerf inside the slug's 274 x 184 outline (robot-shop variant of FR-02)")
            else:
                tools, cuts = RM.op_tools(RB, "frame", key)
                if cuts is not None:
                    cand = [(kk, tt) for kk, tt in cuts if kk not in used_j]
                    tools = [tt for _, tt in cand]
                    used_j |= {kk for kk, _ in cand}
                elif key.startswith("J:"):
                    used_j.add(key[2:])
                label = RM.op_label(RB, "frame", key)
                if core is None and key in ("FR-03", "FR-04", "FR-05"):   # the opening finish and the rebate skin the walls, not the core
                    tools = [t.cut(core_box) for t in tools]
            if not tools:
                continue
            after = state.cut(*tools)
            removed = state.Volume() - after.Volume()
            state = after
            if key == "TR>":                      # the core is free: split it off
                core = state.intersect(core_box)
                state = state.cut(core_box)
                tess(core).save(OUT / "frameT_core.vtp")
            k += 1
            tess(state).save(OUT / f"frameT_{k}.vtp")
            rows_t.append(dict(part="frameT", k=k, setup=sid, on="table", fc=su.get("fc", ""), rots=su.get("rots", []),
                               key=key, label=label, file=f"frameT_{k}.vtp", cm3=round(state.Volume() / 1000, 2),
                               removed_cm3=round(removed / 1000, 2)))
            print("frameT", k, sid, key, round(removed / 1000, 1), "cm3", flush=True)
    # F-S3 as planned, then the check
    su3 = next(s for s in plan["frame"] if s["title"].startswith("F-S3"))
    for ang, keys in su3["index"]:
        for key in keys:
            tools, cuts = RM.op_tools(RB, "frame", key)
            if cuts is not None:
                cand = [(kk, tt) for kk, tt in cuts if kk not in used_j]
                tools = [tt for _, tt in cand]
                used_j |= {kk for kk, _ in cand}
            elif key.startswith("J:"):
                used_j.add(key[2:])
            if not tools:
                continue
            after = state.cut(*tools)
            removed = state.Volume() - after.Volume()
            state = after
            k += 1
            tess(state).save(OUT / f"frameT_{k}.vtp")
            rows_t.append(dict(part="frameT", k=k, setup="F-S3", on="rotary", fc=su3.get("fc", ""), rots=su3.get("rots", []),
                               index_deg=ang, key=key, label=RM.op_label(RB, "frame", key), file=f"frameT_{k}.vtp",
                               cm3=round(state.Volume() / 1000, 2), removed_cm3=round(removed / 1000, 2)))
    fin = next(v for n, v in final.items() if n.startswith("Process chamber body"))
    dvt = abs(state.Volume() - fin.Volume()) / fin.Volume()
    print(f"frameT (trepan variant): last state vs the model's part {100 * dvt:.3f} % in volume; core "
          f"{core.Volume() / 1000:.1f} cm3", flush=True)
    rows_t.append(dict(part="frameT", check_volume_frac=dvt, core_cm3=round(core.Volume() / 1000, 1),
                       core_mm=[round(2 * cx, 1), round(2 * cy, 1)], kerf_mm=kerf, mid_z=zm))
    rows += rows_t
    # the CAM setups' fixtures (freecad_cam.FIXTURES), in their own setup frames, for the renderer
    import freecad_cam as FCAM
    fx = {k: dict(table_z=v[0], pieces=[[nm, kind, list(p)] for nm, kind, p in v[1]]) for k, v in FCAM.FIXTURES.items()}
    (OUT / "states.json").write_text(json.dumps(dict(rows=rows, fixtures=fx, rot_a={str(k): v for k, v in FCAM.ROT_A.items()},
                                                     frame_blank=FCAM.FRAME_BLANK, floor_blank=FCAM.FLOOR_BLANK,
                                                     plan={p: [dict(title=s["title"], on=s["on"], fc=s.get("fc", ""),
                                                                    rots=s.get("rots", []), index=s.get("index"),
                                                                    ops=s.get("ops")) for s in plan[p]] for p in plan},
                                                     run_s=round(time.time() - t0, 1)), indent=1))
    print("wrote", OUT, f"{time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
