"""Can the scan head still come off for service on the g3 gantry? (round 3, 2026-11-28)

On g3 the hurrySCAN hangs by its entrance (-x) face from the flange plate MK-09 (with its top flange on both cross-beams
and gussets under the head) and a 10 mm support plate presses on its far (+x) face from both cross-beams. The input
turret on the entrance face passes through a Ø52 hole in MK-09 to the 45 deg mirror block, which carries the
collimator (from -y, under the front cross-beam) and the photodiode branch (MON4). The beam tube's half-shells are
off first in every route (as for opening the lid), the head's cables and the fibre are unplugged.

Each route moves a rigid group against every fixed part (python-fcl on the tessellated solids as a first pass; a pair
that fcl flags is then intersected exactly with OpenCascade and counts only above 0.5 mm3, so parts that slide along
each other's faces, such as the head along the far-side pad, are not blocked):

  A  MK-09 with everything on it (head, lens, lens collar and its switch, input stack, photodiode branch) lifted
     straight up after unbolting MK-09's angle brackets and top flange: with the collimator on, and with it off.
  B  the head alone (with its turret, lens, collar) after taking the mirror block off the turret and unbolting the
     head from MK-09: slid +x until the turret is out of MK-09's hole, then lifted: with the far-side plate in place,
     and with it off.
  C  the head alone lifted straight up, mirror block off, far-side plate off (no +x slide).

Run:  python desktop-lpbf/fast-track/cad/ft_head_service.py [FT-1 FT-1V ...]   # out/head-service.json, .md (~2 min)
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402

OUT = HERE / "out"
VOL_TOL = 0.5
HEAD = ("SCANLAB hurrySCAN", "LINOS", "hurrySCAN input turret", "Beam-tube lens collar", "Beam-tube interlock")
MK09 = ("Scan-head flange plate", "Flange-to-beam angle brackets", "Head-plate top flange", "Head-plate gussets")
STACK = ("hurrySCAN 45 deg input-mirror block", "Photodiode branch")
COLL = ("Collimator",)
FAR = ("Head far-side support plate", "Far-side support angle brackets")
GONE = ("Beam tube centre section", "Head cables", "Process fibre", "Surface thermocouples", "Bench top")


def _mesh(shape, tol=0.3):
    vs, ts = shape.tessellate(tol, 0.3)
    return np.array([(v.x, v.y, v.z) for v in vs], float), np.array(ts, np.int32)


def _bvh(V, F):
    import fcl
    g = fcl.BVHModel()
    g.beginModel(len(V), len(F))
    g.addSubModel(np.ascontiguousarray(V, np.float64), np.ascontiguousarray(F, np.int32))
    g.endModel()
    return g


def route(parts, movers_k, removed_k, path, label):
    """Move the parts whose names start with movers_k along path (list of (value, dx, dy, dz)); parts starting with
    removed_k (and GONE) are off. Returns the first blocking pose and pair, and the nearest fixed parts."""
    import fcl
    movers = [p for p in parts if p.name.startswith(movers_k)]
    statics = [p for p in parts if not p.name.startswith(movers_k + removed_k + GONE)]
    st = []
    for s in statics:
        V, F = _mesh(s.shape)
        if len(F):
            st.append((s, fcl.CollisionObject(_bvh(V, F), fcl.Transform()), V.min(0), V.max(0)))
    mv = []
    for p in movers:
        V, F = _mesh(p.shape)
        if len(F):
            mv.append((p, _bvh(V, F), V.min(0), V.max(0)))
    near = {}
    for val, dx, dy, dz in path:
        t = np.array([dx, dy, dz])
        for p, g, lo, hi in mv:
            o = fcl.CollisionObject(g, fcl.Transform(np.eye(3), t))
            for s, so, slo, shi in st:
                if np.any(hi + t + 20 < slo) or np.any(shi < lo + t - 20):
                    continue
                if fcl.collide(o, so, fcl.CollisionRequest(), fcl.CollisionResult()):
                    v = p.shape.translate(M.V(dx, dy, dz)).intersect(s.shape).Volume()
                    if v > VOL_TOL:
                        return dict(route=label, free=False, blocked_at_mm=round(val, 1), mover=p.name, part=s.name,
                                    overlap_mm3=round(v, 1))
                    continue
                d = fcl.distance(o, so, fcl.DistanceRequest(), fcl.DistanceResult())
                k = (p.name, s.name)
                if k not in near or d < near[k][0]:
                    near[k] = (d, val)
    rows = sorted(((d, v, a, b) for (a, b), (d, v) in near.items()))[:4]
    return dict(route=label, free=True, travel_mm=round(path[-1][0], 1),
                nearest=[dict(mover=a, part=b, min_gap_mm=round(d, 2), at_mm=round(v, 1)) for d, v, a, b in rows])


def run(state):
    parts = M.build(state)
    lift = [(z, 0.0, 0.0, z) for z in np.arange(0.0, 160.0 + 1e-9, 2.0)]
    slide = [(x, x, 0.0, 0.0) for x in np.arange(0.0, 46.0 + 1e-9, 2.0)]
    slide_lift = slide + [(46.0 + z, 46.0, 0.0, z) for z in np.arange(2.0, 160.0 + 1e-9, 2.0)]
    out = [route(parts, MK09 + HEAD + STACK + COLL, (), lift,
                 "A1 MK-09 with the head, lens, input stack and collimator lifted straight up"),
           route(parts, MK09 + HEAD + STACK, COLL, lift,
                 "A2 the same with the collimator off the mirror block first"),
           route(parts, HEAD, STACK + COLL, slide_lift,
                 "B1 head alone (mirror block off) slid +x 46 mm then lifted, far-side plate in place"),
           route(parts, HEAD, STACK + COLL + FAR, slide_lift,
                 "B2 the same with the far-side plate and its brackets off first"),
           route(parts, HEAD, STACK + COLL + FAR, lift,
                 "C  head alone lifted straight up (mirror block and far-side plate off)")]
    return out


def main():
    t0 = time.time()
    states = sys.argv[1:] or ["FT-1", "FT-1V"]
    res = {"gantry": M.P["gantry"]}
    for st in states:
        res[st] = run(st)
        for r in res[st]:
            print(st, r["route"], "free" if r["free"] else f"blocked at {r['blocked_at_mm']} mm: {r['mover']} / "
                  f"{r['part']}", f"({time.time() - t0:.0f} s)", flush=True)
    res["runtime_s"] = round(time.time() - t0)
    OUT.mkdir(exist_ok=True)
    (OUT / "head-service.json").write_text(json.dumps(res, indent=1))
    write_md(res, states)
    print(f"wrote out/head-service.json, out/head-service.md in {time.time() - t0:.0f} s")


def write_md(res, states):
    md = ["# Taking the scan head off on the g3 gantry (`ft_head_service.py`, round 3)", "",
          f"Generated from `ft_model.py` (`P['gantry'] = \"{res['gantry']}\"`). Beam-tube half-shells, the head's cables "
          "and the fibre are off in every route. A route is blocked when a moving part overlaps a fixed one by more "
          "than 0.5 mm3 (exact OpenCascade intersection after a python-fcl first pass); 2 mm steps. Parts that touch "
          "face to face at the start (MK-09's top flange on the beams, its plate's ends between them, the head on the "
          "far-side pad) slide apart without counting.", "",
          "| State | Route | Result |", "|---|---|---|"]
    for st in states:
        for r in res[st]:
            if r["free"]:
                md.append(f"| {st} | {r['route']} | free over {r['travel_mm']} mm |")
            else:
                md.append(f"| {st} | {r['route']} | **blocked at {r['blocked_at_mm']} mm**: {r['mover'].split(' (')[0]} "
                          f"meets {r['part'].split(' (')[0]} ({r['overlap_mm3']} mm3) |")
    md += ["", f"Run time {res['runtime_s']} s."]
    (OUT / "head-service.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
