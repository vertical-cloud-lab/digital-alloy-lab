"""Insertion and removal paths for the parts of the fast-track video, checked for collisions before anything is drawn.

A part (or a group that travels together, such as the box's lid with its window stack) comes in from outside the scene
along a short list of straight legs and stops at its place in the model; a part that leaves goes the same way out. Each
path is sampled every STEP_MM along every leg and every sample is checked against everything already in the scene, with
collide.py's test (shrunk mover, translational depth, 1.5 mm limit). `plan()` tries the candidate approaches in order and
returns the first clear one; `check()` checks a path given by hand.

Waypoints are offsets from the part's place in the model, from the start (outside the scene) to (0, 0, 0).
"""
from __future__ import annotations

import numpy as np

import collide as C

STEP_MM = 2.0
FAR = 1500.0                     # a start this far along an axis is outside every shot used here
HEIGHTS = (3, 6, 10, 15, 20, 30, 45, 60, 80, 100, 130, 150, 160, 170, 175, 180, 183, 186, 190, 195, 200, 205, 210,
           215, 225, 240, 260, 280, 330, 400)


class World:
    """Bodies (name -> Geom) at translations, for checking paths."""

    def __init__(self):
        self.g, self.t = {}, {}

    def put(self, name, V, F, t=(0.0, 0.0, 0.0)):
        self.g[name] = C.Geom(V, F)
        self.t[name] = np.asarray(t, float)

    def drop(self, name):
        self.g.pop(name, None)
        self.t.pop(name, None)

    def move(self, name, t):
        self.t[name] = np.asarray(t, float)

    def names(self):
        return list(self.g)

    def hits(self, group, off, ignore=(), need=C.DEPTH_MM):
        """Pairs (mover, other, depth) deeper than `need` with the group shifted by `off`."""
        off = np.asarray(off, float)
        grp = set(group)
        out = []
        others = [n for n in self.g if n not in grp and n not in ignore]
        if not others:
            return out
        lo = np.array([self.g[n].lo + self.t[n] for n in others])
        hi = np.array([self.g[n].hi + self.t[n] for n in others])
        for m in group:
            gm, tm = self.g[m], self.t[m] + off
            mlo, mhi = gm.lo + tm, gm.hi + tm
            ov = np.all((mlo <= hi) & (lo <= mhi), axis=1)
            for j in np.nonzero(ov)[0]:
                n = others[j]
                d = C.depth(gm, tm, self.g[n], self.t[n], need=need)
                if d > need:
                    out.append((m, n, d))
        return out


def samples(way, step=STEP_MM):
    """Offsets along the legs of a path, every `step` mm, ending at the last waypoint."""
    pts = [np.asarray(way[0], float)]
    for a, b in zip(way[:-1], way[1:]):
        a, b = np.asarray(a, float), np.asarray(b, float)
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / step)))
        for k in range(1, n + 1):
            pts.append(a + (b - a) * k / n)
    return pts


def check(world, group, way, ignore=(), first=True):
    """Collisions along a path: [] when clear, else [(offset, mover, other, depth)] (only the first when first=True)."""
    out = []
    for off in samples(way):
        for m, n, d in world.hits(group, off, ignore):
            out.append((tuple(np.round(off, 1)), m, n, d))
            if first:
                return out
    return out


def candidates(prefs=None):
    """Approach paths, most natural first: straight down from above; in from the front, a side or the back at a height,
    then down (or up); straight in along an axis; and three-leg paths that step over a wall and then go under something."""
    H = FAR
    dirs = {"front": (0, -1, 0), "right": (1, 0, 0), "left": (-1, 0, 0), "back": (0, 1, 0)}
    out = []
    order = prefs or ["down", "front-down", "right-down", "left-down", "back-down", "front", "right", "left", "back",
                      "front-up", "right-up", "left-up", "front-step", "right-step", "left-step"]
    for p in order:
        if p == "down":
            out.append((p, [(0, 0, H), (0, 0, 0)]))
        elif p.endswith("-down") or p.endswith("-up"):
            d, kind = p.rsplit("-", 1)
            v = np.array(dirs[d], float) * FAR
            for h in HEIGHTS:
                hz = h if kind == "down" else -h
                out.append((f"{p} {h}", [tuple(v + (0, 0, hz)), (0, 0, hz), (0, 0, 0)]))
        elif p.endswith("-step"):
            d = p.split("-")[0]
            u = np.array(dirs[d], float)
            for s in (60, 80, 100, 120, 150, 180):
                for h1 in (183, 186, 190, 195, 200, 205, 215, 240, 280, 330):
                    for h2 in (0, 30, 60, 100, 130, 160):
                        if h2 >= h1:
                            continue
                        out.append((f"{p} s{s} h{h1}/{h2}", [tuple(u * FAR + (0, 0, h1)), tuple(u * s + (0, 0, h1)),
                                                             tuple(u * s + (0, 0, h2)), (0, 0, h2), (0, 0, 0)]))
        else:
            out.append((p, [tuple(np.array(dirs[p], float) * FAR), (0, 0, 0)]))
    return out


def plan(world, group, prefs=None, ignore=(), extra=()):
    """The first clear path for a group: hand-given ones (`extra`, tried first), then candidates(prefs). Every path ends
    at the place itself (offset 0), so when the place is already taken it fails at once rather than after sampling all
    ~1300 candidates to their last point (which took minutes per part)."""
    at = world.hits(group, (0.0, 0.0, 0.0), ignore)
    if at:
        raise RuntimeError(f"no clear path for {group[:3]}...: the place itself is taken: {at[0]}")
    tried = []
    for name, way in list(extra) + candidates(prefs):
        bad = check(world, group, way, ignore)
        if not bad:
            return name, [tuple(map(float, w)) for w in way]
        tried.append((name, bad[0]))
    raise RuntimeError(f"no clear path for {group[:3]}...: last tries {tried[-3:]}")
