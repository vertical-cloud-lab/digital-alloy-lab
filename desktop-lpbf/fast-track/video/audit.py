"""Audit of every drawn frame of the fast-track video for interpenetration (the method of PR 266's scene_audit.py).

render.py records, for every image it draws, each actor's drawn state (shown or not, translation, per-axis scale, the
fibre's blended vertices) and the solid effects (the coupons). This replays the recording and checks everything that moves
against everything drawn that is solid and at least 30 % opaque in the model (OPAQUE; a part faded for a cutaway view still
counts): python-fcl BVH collision on the drawn triangles, the mover shrunk 0.3 mm, the translational penetration depth
over 26 directions on the 1.5 mm ladder, containment by winding numbers (collide.py). A pair deeper than 1.5 mm is a
violation unless it is on the short ALLOWED list below. A pair whose relative pose never changes in the chapter is how the
model is drawn (the CAD's own overlap) and is listed apart as "rigid".

    /tmp/tools/capmem 2 /tmp/venv/bin/python desktop-lpbf/fast-track/video/audit.py 1 2 3     # -> video/out/audit.json
"""
from __future__ import annotations

import json
import pickle
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import collide as C  # noqa: E402
import scene as S  # noqa: E402

FR = S.SCRATCH / "frames"
OUT = HERE / "out"
OPAQUE = 0.3

# (label pattern a, label pattern b, depth it may reach (mm) or None for any, reason)
ALLOWED = [
    (r"^KF-25 pump hose", r"^KF-25 ports", 6.0,
     "the hose's clamp end is drawn over its KF-25 port's flange (the model's hose ends in the flange)"),
    (r"^KF-25 pump hose", r"^Rotary-vane pump", 15.0,
     "the hose's other end is drawn down into the pump's inlet on its top face"),
]


def allowed(la, lb):
    for pa, pb, lim, why in ALLOWED:
        if (re.search(pa, la) and re.search(pb, lb)) or (re.search(pa, lb) and re.search(pb, la)):
            return lim, why
    return None


def stream(path):
    with open(path, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                return


def placed(meshes, name, st, cache):
    """(Geom, translation) of an actor as drawn: its mesh (or blended mesh), scaled about its own z0, translated."""
    m = meshes[name]
    key = (name, st.get("morph"))
    g = cache.get(key)
    if g is None:
        V = st["V"] if st.get("V") is not None else m["V"]
        g = cache[key] = C.Geom(V, m["F"])
    off = np.asarray(st["off"], float)
    sc = st.get("scale")
    if sc is not None and not np.allclose(sc[:3], 1.0):
        sx, sy, sz, z0 = sc
        g = g.scaled((sx, sy, sz))
        off = off + np.array([0.0, 0.0, z0 * (1.0 - sz)])
    return g, off


def run(ch):
    d = FR / f"ch{ch}"
    meshes = pickle.load(open(d / "meshes.pkl", "rb"))
    t0 = time.time()
    # pass 1: who moves
    seen = {}
    for rec in stream(d / "audit.pkl"):
        for name, st in rec["changed"].items():
            k = (tuple(st["off"]), st["scale"], st["morph"])
            seen.setdefault(name, set()).add(k if st["vis"] else ("hidden",))
    movers = {n for n, s in seen.items() if len(s) > 1 and meshes[n]["kind"] in ("part",)}
    solid = {n for n, m in meshes.items() if m["solid"] and m["opacity"] >= OPAQUE}
    cur = {}
    fx = {}
    cache, gcache = {}, {}
    viol, rigid_rel, allow_hits = {}, {}, {}
    frames = 0
    for rec in stream(d / "audit.pkl"):
        frames += 1
        n = rec["n"]
        for name, st in rec["changed"].items():
            cur[name] = st
        for fname, (key, data, op) in rec["fx"].items():
            if data is not None:
                fx[fname] = (key, C.Geom(data[0], data[1]))
            elif fname not in fx:
                continue
        live = {}
        for name, st in cur.items():
            if st["vis"] and name in solid:
                live[name] = placed(meshes, name, st, gcache)
        for fname in rec["fx"]:
            if fname in fx:
                live["fx:" + fname] = (fx[fname][1], np.zeros(3))
        names = list(live)
        lo = np.array([live[k][0].lo + live[k][1] for k in names])
        hi = np.array([live[k][0].hi + live[k][1] for k in names])
        mv = [i for i, k in enumerate(names) if k in movers or k.startswith("fx:")]
        done = set()
        for i in mv:
            ov = np.all((lo[i] <= hi) & (lo <= hi[i]), axis=1)
            ov[i] = False
            for j in np.nonzero(ov)[0]:
                a, b = names[i], names[j]
                pair = (a, b) if a < b else (b, a)
                if pair in done:
                    continue
                done.add(pair)
                ga, ta = live[a]
                gb, tb = live[b]
                rel = tuple(np.round(tb - ta, 2))
                sig = (id(ga), id(gb), rel)
                dep = cache.get(sig)
                if dep is None:
                    dep = cache[sig] = C.depth(ga, ta, gb, tb)
                la = meshes[a]["label"] if a in meshes else a
                lb = meshes[b]["label"] if b in meshes else b
                al = allowed(la, lb)
                lim = al[0] if al else C.DEPTH_MM
                if dep > 0 and al:
                    h = allow_hits.setdefault(al[1], dict(pairs=set(), frames=0, worst=0.0))
                    h["pairs"].add(f"{la} / {lb}")
                    h["frames"] += 1
                    h["worst"] = max(h["worst"], dep)
                if dep > lim:
                    v = viol.setdefault(pair, dict(worst=0.0, frame=n, frames=[], labels=(la, lb), lim=lim))
                    v["frames"].append(n)
                    if dep > v["worst"]:
                        v["worst"], v["frame"] = dep, n
                    rigid_rel.setdefault(pair, set()).add(rel)
    rows, rigid = [], []
    for pair, v in sorted(viol.items(), key=lambda kv: -kv[1]["worst"]):
        r = dict(a=v["labels"][0], b=v["labels"][1], worst_mm=round(v["worst"], 1) if v["worst"] < C.DEEP else ">100",
                 worst_frame=v["frame"], frames=len(v["frames"]), first=v["frames"][0], last=v["frames"][-1])
        (rigid if len(rigid_rel[pair]) == 1 and _both_move_together(pair, seen) else rows).append(r)
    out = dict(chapter=ch, frames_checked=frames, movers=len(movers), threshold_mm=C.DEPTH_MM, opaque_min=OPAQUE,
               violations=len(rows), worst_mm=rows[0]["worst_mm"] if rows else 0.0, pairs=rows[:60], rigid_pairs=rigid[:40],
               allowed=[dict(reason=k, pairs=sorted(h["pairs"])[:6], pair_frames=h["frames"], worst_mm=round(h["worst"], 1))
                        for k, h in allow_hits.items()],
               seconds=round(time.time() - t0, 1))
    print(f"ch{ch}: {frames} drawn frames, {len(movers)} movers, {len(rows)} violating pairs "
          f"(worst {out['worst_mm']}), {len(rigid)} rigid, {out['seconds']} s", flush=True)
    for r in rows[:12]:
        print(f"   {r['worst_mm']!s:>6} mm  {r['a'][:45]}  x  {r['b'][:45]}  frames {r['frames']} ({r['first']}-{r['last']})",
              flush=True)
    return out


def _both_move_together(pair, seen):
    """Both actors of a pair have the same history of drawn states (they move as one group)."""
    a, b = pair
    return seen.get(a) is not None and seen.get(a) == seen.get(b)


if __name__ == "__main__":
    chs = [int(x) for x in sys.argv[1:]] or [int(p.name[2:]) for p in sorted(FR.glob("ch*")) if (p / "audit.pkl").exists()]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "audit.json"
    res = json.loads(path.read_text()) if path.exists() else {}
    for c in chs:
        if (FR / f"ch{c}" / "audit.pkl").exists():
            res[f"ch{c}"] = run(c)
    path.write_text(json.dumps(res, indent=1, default=str) + "\n")
