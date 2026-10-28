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
            for nm, mesh, _ in CB.clip_parts():
                p = mesh.triangulate()
                out[f"clip_{k}_{nm}"] = (f"clip_{k}", trimesh.Trimesh(np.asarray(p.points),
                                                                     p.faces.reshape(-1, 4)[:, 1:], process=False))
    except ImportError:
        pass
    return out


def base(name: str) -> str:
    return name.split(":")[-1].split("#")[0]


def allowed(a: str, b: str) -> bool:
    """Pairs that are designed to touch."""
    pair = {a, b}
    if "bench" in pair:
        return True
    if any(n.startswith("clip_") for n in pair):
        k = [n for n in pair if n.startswith("clip_")][0].split("_")[1]
        other = [n for n in pair if not n.startswith("clip_")]
        return bool(other) and other[0].startswith(k if k != "container" else "container")
    designed = [{"pan", "s230"}, {"s230", "s60"}, {"s60", "cover"}, {"bus_bar", "standoff0"}, {"bus_bar", "standoff1"},
                {"jar_print", "balance_pan"}, {"jar_coarse", "funnel_coarse"}, {"jar_print", "funnel_print"},
                {"jar_coarse", "lid_coarse"}, {"jar_print", "lid_print"}, {"jar_print", "label"}]
    return pair in designed


def main():
    rec = pickle.loads((HERE / "out" / "audit_frames.pkl").read_bytes())
    frames, cable = rec["record"], rec.get("cable_mm", [])
    meshes = part_meshes()
    cm = CollisionManager()
    for name, (g, tm) in meshes.items():
        cm.add_object(name, tm)
    hits = defaultdict(list)
    n_checked = 0
    for fr in frames:
        shown = {base(s) for s in fr["shown"]}
        for i, (n, (g, _)) in enumerate(meshes.items()):
            if n in shown:
                cm.set_transform(n, fr["mats"].get(g, np.eye(4)))
            else:                           # hidden: park it far away, each in its own place
                far = np.eye(4)
                far[:3, 3] = (1e5 + 1e3 * i, 0.0, 0.0)
                cm.set_transform(n, far)
        hit, pairs, data = cm.in_collision_internal(return_names=True, return_data=True)
        n_checked += 1
        if not hit:
            continue
        depth = defaultdict(float)
        for d in data:
            a, b = sorted(d.names)
            depth[(a, b)] = max(depth[(a, b)], float(d.depth))
        for (a, b), dep in depth.items():
            if meshes[a][0] == meshes[b][0]:
                continue                    # the same group: one rigid part
            if dep <= TOL or (allowed(a, b) and dep <= 1.0):
                continue
            hits[f"{a} / {b}"].append((fr["n"], round(dep, 2)))
    worst_cable = max(cable) if cable else None
    report = dict(frames=n_checked, tolerance_mm=TOL, pairs={k: dict(frames=len(v), first=v[0][0], last=v[-1][0],
                                                                       max_depth_mm=max(d for _, d in v))
                                                             for k, v in sorted(hits.items())},
                  cable_max_penetration_mm=worst_cable)
    (HERE / "out" / "audit.json").write_text(json.dumps(report, indent=1) + "\n")
    print(f"{n_checked} frames checked; {len(hits)} interpenetrating pairs beyond {TOL} mm")
    for k, v in report["pairs"].items():
        print(f"  {k:40s} frames {v['first']}-{v['last']} ({v['frames']}), max {v['max_depth_mm']} mm")
    print("leads: deepest point", worst_cable, "mm")
    return report


if __name__ == "__main__":
    main()
