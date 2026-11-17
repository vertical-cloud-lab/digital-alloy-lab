"""Collision audit of the rendered sieving animation: does any part pass through another in any frame?

steps.py records, for every frame it renders, each group's world matrix and which actors are shown
(``out/audit_frames.pkl``, not committed). This places every shown part's mesh (the whole one, also for halved
parts, so the cutaway can't hide anything) and the clips of the bonding leads, and asks FCL for every pair of parts
that interpenetrate by more than TOL. Pairs that are meant to touch (a sieve resting on the one below, a jar on the
bench, a clip biting its part, the lug on the bus bar) count only if they go deeper than that. The powder needs no
audit of this kind: the DEM keeps every parcel out of every wall (soft contacts overlap by a few % of a radius), and
the leads report their own deepest point (``cable_mm``, from cables.py) for each frame.

    python audit.py      # prints a summary and writes out/audit.json
"""
from __future__ import annotations

import json
import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np
import trimesh
from trimesh.collision import CollisionManager

import model as M

HERE = Path(__file__).resolve().parent
TOL = 0.3          # mm


def part_meshes():
    ms = M.meshes()
    out = {}
    for name, m in ms.items():
        if name.startswith("_") or m["whole"] is None:
            continue
        p = m["whole"].triangulate()
        out[name] = (m["group"], trimesh.Trimesh(np.asarray(p.points), p.faces.reshape(-1, 4)[:, 1:], process=False))
    try:
        import cables as CB
        for k in ("container", "tray", "pan"):
            for nm, mesh, _ in CB.clip_parts(0.25):
                p = mesh.triangulate()
                out[f"clip_{k}_{nm}"] = (f"clip_{k}", trimesh.Trimesh(np.asarray(p.points),
                                                                     p.faces.reshape(-1, 4)[:, 1:], process=False))
    except ImportError:
        pass
    return out


def base(name: str) -> str:
    return name.split(":")[-1].split("#")[0]


def allowed(a: str, b: str) -> bool:
    """Pairs that are built to touch (the bench is checked on its own: nothing may go below z = 0)."""
    pair = {a, b}
    if any(n.startswith("clip_") for n in pair):
        k = [n for n in pair if n.startswith("clip_")][0].split("_")[1]
        other = [n for n in pair if not n.startswith("clip_")]
        return bool(other) and other[0].startswith(k if k != "container" else "container")
    designed = [{"pan", "s230"}, {"s230", "s60"}, {"s60", "cover"}, {"bus_bar", "standoff0"}, {"bus_bar", "standoff1"},
                {"jar_print", "balance_pan"}, {"jar_coarse", "funnel_coarse"}, {"jar_print", "funnel_print"},
                {"jar_coarse", "lid_coarse"}, {"jar_print", "lid_print"}, {"jar_print", "label"}]
    return pair in designed


def depth(a, Ma, b, Mb, n=600) -> float:
    """How far the two placed meshes go into each other: the deepest vertex of either inside the other (mm). FCL's
    own depth is not reliable for two triangle meshes, so this is what is reported."""
    out = 0.0
    for (s, Ms), (t, Mt) in (((a, Ma), (b, Mb)), ((b, Mb), (a, Ma))):
        v = s.vertices
        if len(v) > n:
            v = v[np.linspace(0, len(v) - 1, n).astype(int)]
        q = (np.c_[v, np.ones(len(v))] @ (np.linalg.inv(Mt) @ Ms).T)[:, :3]
        inside = t.contains(q)
        if inside.any():
            _, dist, _ = trimesh.proximity.closest_point(t, q[inside])
            out = max(out, float(dist.max()))
    return out


def main(path=HERE / "out" / "audit_frames.pkl", out=HERE / "out" / "audit.json"):
    rec = pickle.loads(Path(path).read_bytes())
    frames, cable = rec["record"], rec.get("cable_mm", [])
    meshes = part_meshes()
    solid = {}
    for name, (g, tm) in meshes.items():
        tm = tm.copy()
        tm.merge_vertices()
        solid[name] = tm
    cm = CollisionManager()
    for name, (g, tm) in meshes.items():
        if name != "bench":
            cm.add_object(name, tm)
    hits = defaultdict(list)
    n_checked = 0
    for fr in frames:
        shown = {base(s) for s in fr["shown"]}
        for i, (n, (g, tm)) in enumerate(meshes.items()):
            if n == "bench":
                continue
            if n in shown:
                Mw = fr["mats"].get(g, np.eye(4))
                cm.set_transform(n, Mw)
                zmin = float((tm.vertices @ Mw[:3, :3].T + Mw[:3, 3])[:, 2].min())
                if zmin < -TOL:                     # the bench top is z = 0
                    hits[f"bench / {n}"].append((fr["n"], round(-zmin, 2)))
            else:                                   # hidden: park it far away, each in its own place
                far = np.eye(4)
                far[:3, 3] = (1e5 + 1e3 * i, 0.0, 0.0)
                cm.set_transform(n, far)
        n_checked += 1
        hit, pairs = cm.in_collision_internal(return_names=True)
        if not hit:
            continue
        for a, b in pairs:
            a, b = sorted((a, b))
            if meshes[a][0] == meshes[b][0] or allowed(a, b):
                continue                            # one rigid part, or built to touch
            d = depth(solid[a], fr["mats"].get(meshes[a][0], np.eye(4)), solid[b], fr["mats"].get(meshes[b][0],
                                                                                                    np.eye(4)))
            if d > TOL:
                hits[f"{a} / {b}"].append((fr["n"], round(d, 2)))
    by_lead = defaultdict(float)
    for d in cable:
        for k, v in (d.items() if isinstance(d, dict) else [("all", d)]):
            by_lead[k] = max(by_lead[k], v)
    worst_cable = max(by_lead.values()) if by_lead else None
    report = dict(frames=n_checked, tolerance_mm=TOL, pairs={k: dict(frames=len(v), first=v[0][0], last=v[-1][0],
                                                                       max_depth_mm=max(d for _, d in v))
                                                             for k, v in sorted(hits.items())},
                  cable_max_penetration_mm=None if worst_cable is None else round(worst_cable, 2),
                  cable_by_lead_mm={k: round(v, 2) for k, v in by_lead.items()})
    Path(out).write_text(json.dumps(report, indent=1) + "\n")
    print(f"{n_checked} frames checked; {len(hits)} pairs go more than {TOL} mm into each other")
    for k, v in report["pairs"].items():
        print(f"  {k:40s} frames {v['first']}-{v['last']} ({v['frames']}), max {v['max_depth_mm']} mm")
    print("leads: deepest point", report["cable_max_penetration_mm"], "mm", report["cable_by_lead_mm"])
    return report


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
