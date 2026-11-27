"""pairs_classify.py <chapter>...; then pairs_classify_md.py. Classify the final frame-audit pairs of chapters 40 and 41 (round 9): re-measure each pair at its worst frame, and at a few
frames over its ranges, with the planner's own meshes (run_assembly.Run, 0.1 mm tessellation) where a side is a part, and test
whether a fingertip pair holds its part (relative pose constant while the gripper moves)."""
import json
import os
import pickle
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scene_audit as SA  # noqa: E402

REPO = HERE.parents[2]
ASM = REPO / "desktop-lpbf" / "analysis" / "assembly"
sys.path.insert(0, str(ASM))
sys.path.insert(0, str(REPO / "desktop-lpbf" / "analysis" / "robot"))
os.chdir(ASM)
import run_assembly as RA  # noqa: E402

run = RA.Run()
FULL = {}


def full(i):
    if i not in FULL:
        o = run.sc.objs[i] if i < len(run.sc.objs) else {}
        FULL[i] = (np.asarray(o["V"], np.float32), np.asarray(o["F"], np.int32)) if o.get("V") is not None else None
    return FULL[i]


fcl = SA._fcl()
out = {}
for ch in sys.argv[1:]:
    root = Path("/tmp/robotbuild/frames") / ch
    parts = json.loads((root / "audit_parts.json").read_text())["parts"]
    aud = json.loads((REPO / "desktop-lpbf/analysis/out/videoqa" / f"scene_audit_{ch}.json").read_text())
    pairs = aud["pairs"]
    # frames to look at per pair: the worst, and the first, middle and last of its ranges
    want = {}
    for idx, p in enumerate(pairs):
        fr = {int(p["worst_frame"])}
        for a_, b_ in p.get("frame_ranges", [])[:6]:
            fr |= {a_, (a_ + b_) // 2, b_}
        for f in fr:
            want.setdefault(f, []).append(idx)
    names = {p["a"] for p in pairs} | {p["b"] for p in pairs}
    snap = {}                                   # (idx, frame) -> (Ma, Mb, (Va, Fa), (Vb, Fb))
    for pr in parts:
        if not pr.get("audit"):
            continue
        lo, hi, own0 = pr["first_frame"], pr["last_frame"], pr.get("own_first_frame", pr["first_frame"])
        frames_here = sorted(f for f in want if lo <= f <= hi)
        if not frames_here:
            continue
        own = {f - lo + own0: f for f in frames_here}
        rp = SA.Replay([(f"{ch}.part{pr['part']}", root / pr["audit"])], want=lambda nm: nm in names)
        for tag, n, actors, dirty in rp.frames():
            if n not in own:
                continue
            f = own[n]
            for idx in want[f]:
                p = pairs[idx]
                A, B = actors.get(p["a"]), actors.get(p["b"])
                if A is None or B is None or A.geom is None or B.geom is None:
                    continue
                snap[(idx, f)] = (A.M.astype(float).copy(), B.M.astype(float).copy(), (A.geom.V, A.geom.F), (B.geom.V, B.geom.F))
    res = []
    for idx, p in enumerate(pairs):
        r = dict(a=p["a"], b=p["b"], a_is=p.get("a_is", ""), b_is=p.get("b_is", ""), drawn_mm=p["worst_mm"],
                 worst_frame=p["worst_frame"], frames=p["frames"], ranges=p.get("frame_ranges", [])[:4])
        w = snap.get((idx, int(p["worst_frame"])))
        if w is None:
            r["note"] = "not re-measured (actor missing at the worst frame)"
            res.append(r)
            continue
        Ma, Mb, ga, gb = w
        rel0 = np.linalg.inv(Ma) @ Mb
        r["rel_offset_mm"] = round(float(np.linalg.norm(rel0[:3, 3])), 2)
        r["rel_rot_deg"] = round(float(np.degrees(np.arccos(np.clip((np.trace(rel0[:3, :3]) - 1) / 2, -1, 1)))), 2)
        meshes = []
        for nm, g in ((p["a"], ga), (p["b"], gb)):
            if nm[0] == "o" and nm[1:].isdigit() and full(int(nm[1:])) is not None:
                meshes.append(full(int(nm[1:])))
            else:
                meshes.append(g)
        GA = SA.Geom(meshes[0][0], meshes[0][1], "a")
        GB = SA.Geom(meshes[1][0], meshes[1][1], "b")
        x, Mx, y, My = (GA, Ma, GB, Mb) if GA.ntri <= GB.ntri else (GB, Mb, GA, Ma)
        ox = fcl.CollisionObject(x.ero(), fcl.Transform(Mx[:3, :3], Mx[:3, 3]))
        oy = fcl.CollisionObject(y.model(), fcl.Transform(My[:3, :3], My[:3, 3]))
        lo_x, hi_x = SA.world_box(x.corners, Mx)
        lo_y, hi_y = SA.world_box(y.corners, My)
        d = SA.tdepth(fcl, ox, Mx, oy, 0.5 * (lo_x + hi_x), 0.5 * (lo_y + hi_y), ga=x, gb=y, Mb=My)
        r["planner_mesh_mm"] = None if d >= SA.DEEP else round(float(d), 1)
        r["planner_tris"] = [len(meshes[0][1]), len(meshes[1][1])]
        r["drawn_tris"] = [len(ga[1]), len(gb[1])]
        # held: the relative pose constant over the sampled frames while the pair moved
        rels, moves = [], []
        for f in sorted({k[1] for k in snap if k[0] == idx}):
            M1, M2 = snap[(idx, f)][0], snap[(idx, f)][1]
            rels.append(np.linalg.inv(M1) @ M2)
            moves.append(M1[:3, 3])
        if len(rels) >= 2:
            dr = max(float(np.linalg.norm(R[:3, 3] - rels[0][:3, 3])) for R in rels)
            dm = max(float(np.linalg.norm(m - moves[0])) for m in moves)
            r["rel_change_mm"], r["moved_mm"] = round(dr, 1), round(dm, 1)
        res.append(r)
    out[ch] = res
    print(ch, len(res), "pairs re-measured", flush=True)
Path("/tmp/robotbuild/data/pairs_classify.json").write_text(json.dumps(out, indent=1, default=float))
print("done")
