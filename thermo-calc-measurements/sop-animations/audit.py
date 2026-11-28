"""A per-frame collision audit for the SOP animations: does anything that moves pass through anything else? (#262)

Sterling's most repeated complaint about earlier lab videos was parts "passing through other things like ghosts".
This checks the meshes as drawn, every frame (or every `every`-th), with FCL (python-fcl; triangle BVHs, OBB-RSS):

* the movers are the actors whose world matrix changed since the last check, and the deforming meshes (the operator,
  people.Person: re-posed every frame, so their BVHs are rebuilt from the current vertices);
* each mover is checked against every other visible actor (opacity above 0.05), movers included, except actors of
  its own group and pairs that match ``allow`` (fnmatch patterns on the actor names, either order), which is where an
  intended contact goes: a crucible on its sensor, a hand on what it holds, a cube in the basket;
* a contact counts when FCL reports a penetration deeper than ``depth_mm`` (1.5 mm by default; FCL's depth is an
  estimate, so a shallow touch at rest is not flagged).

    import audit
    au = audit.Audit(sc, allow=[("tweezers*", "crucible*"), ("person*glove*", "*")])
    ...  # the scene's steps
    sc.save(); au.save()        # -> out/collisions/<scene>.json: frames, pairs, sub-step labels, and a summary

``AUDIT_EVERY`` (env) checks every N-th frame (default 2).
"""
from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _faces(poly) -> np.ndarray:
    import pyvista as pv
    p = pv.wrap(poly)
    if not p.is_all_triangles:
        p = p.triangulate()
    f = np.asarray(p.faces).reshape(-1, 4)[:, 1:]
    return np.asarray(p.points, float), f.astype(np.int32)


class Audit:
    def __init__(self, sc, allow=(), depth_mm: float = 1.5, every: int | None = None, skip=("floor*", "wall*",
                 "shadow*", "*shadow*")):
        import fcl
        self.fcl = fcl
        self.sc = sc
        self.allow = [(a, b) for a, b in allow]
        self.depth = depth_mm
        self.every = every or int(os.environ.get("AUDIT_EVERY", "2"))
        self.skip = skip
        self.models: dict = {}            # actor -> (BVHModel, n_points, deforming)
        self.last: dict = {}              # actor -> world matrix bytes at the last check
        self.hits: list = []              # (frame, label, a, b, depth)
        self.k = 0
        sc.frame_hooks.append(self)

    # ----------------------------------------------------------------------------------------- geometry
    def _poly(self, name):
        keep = self.sc.__dict__.get("_keep", {}).get(name)
        if keep is not None and keep[2] is not None:
            return keep[2]
        return self.sc.actors[name].GetMapper().GetInput()

    def _deforming(self, name) -> bool:
        return "person" in name or "/skin" in name or "_body" in self.sc.group_of.get(name, "")

    def _model(self, name):
        rec = self.models.get(name)
        deform = self._deforming(name)
        if rec is not None and not deform:
            return rec[0]
        P, F = _faces(self._poly(name))
        if len(F) == 0:
            return None
        m = self.fcl.BVHModel()
        m.beginModel(len(P), len(F))
        m.addSubModel(P, F)
        m.endModel()
        self.models[name] = (m, len(P), deform)
        return m

    def _allowed(self, a, b) -> bool:
        for p, q in self.allow:
            if (fnmatch.fnmatch(a, p) and fnmatch.fnmatch(b, q)) or (fnmatch.fnmatch(a, q) and fnmatch.fnmatch(b, p)):
                return True
        return False

    def _skip(self, name) -> bool:
        return any(fnmatch.fnmatch(name, s) for s in self.skip)

    # ----------------------------------------------------------------------------------------- per frame
    def __call__(self, sc):
        self.k += 1
        if self.k % self.every:
            return
        vis, world = [], {}
        for name in sc.actors:
            if self._skip(name):
                continue
            if sc.alpha.get(name, 1.0) * sc.base_alpha.get(name, 1.0) <= 0.05:
                continue
            w = sc.world(sc.group_of[name])
            world[name] = w
            vis.append(name)
        movers = [n for n in vis if self._deforming(n) or self.last.get(n) != world[n].tobytes()]
        for n in vis:
            self.last[n] = world[n].tobytes()
        if not movers:
            return
        objs = {}

        def obj(n):
            if n not in objs:
                m = self._model(n)
                if m is None:
                    objs[n] = None
                else:
                    w = world[n]
                    objs[n] = self.fcl.CollisionObject(m, self.fcl.Transform(w[:3, :3], w[:3, 3]))
            return objs[n]
        req = self.fcl.CollisionRequest(num_max_contacts=8, enable_contact=True)
        seen = set()
        label = getattr(sc, "label", "")
        for a in movers:
            oa = obj(a)
            if oa is None:
                continue
            ga = sc.group_of[a]
            for b in vis:
                if b == a or sc.group_of[b] == ga or (b, a) in seen or self._allowed(a, b):
                    continue
                seen.add((a, b))
                ob = obj(b)
                if ob is None:
                    continue
                res = self.fcl.CollisionResult()
                if self.fcl.collide(oa, ob, req, res):
                    d = max((c.penetration_depth for c in res.contacts), default=0.0)
                    if d > self.depth:
                        self.hits.append((sc.n, label, a, b, round(float(d), 2)))

    # ----------------------------------------------------------------------------------------- report
    def save(self) -> Path:
        out = HERE / "out" / "collisions"
        out.mkdir(parents=True, exist_ok=True)
        pairs: dict = {}
        for f, label, a, b, d in self.hits:
            key = f"{a} | {b}"
            r = pairs.setdefault(key, dict(frames=0, first=f, last=f, max_depth_mm=0.0, steps=set()))
            r["frames"] += 1
            r["last"] = f
            r["max_depth_mm"] = max(r["max_depth_mm"], d)
            r["steps"].add(label)
        for r in pairs.values():
            r["steps"] = sorted(r["steps"])
        frames = sorted({h[0] for h in self.hits})
        rep = dict(scene=self.sc.name, checked_every=self.every, depth_threshold_mm=self.depth,
                   frames_in_collision=len(frames), allow=[list(p) for p in self.allow],
                   pairs=dict(sorted(pairs.items(), key=lambda kv: -kv[1]["frames"])))
        path = out / f"{self.sc.name}.json"
        path.write_text(json.dumps(rep, indent=1) + "\n")
        print(f"audit {self.sc.name}: {len(frames)} frames with a collision deeper than {self.depth} mm, "
              f"{len(pairs)} pairs -> {path.name}", flush=True)
        return path
