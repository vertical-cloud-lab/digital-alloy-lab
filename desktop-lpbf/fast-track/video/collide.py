"""Interpenetration of drawn triangle meshes: the method of PR 266's scene_audit.py (round 8), shared by the path planner
(plan.py) and the frame audit (audit.py).

* Narrow phase: python-fcl BVH (OBBRSS) models of the drawn triangles. The moving mesh is shrunk TOUCH_MM (0.3 mm) along
  its vertex normals first, so a part drawn sitting on its seat or in a bore at zero clearance reads as touching.
* Depth: the translational penetration depth, the shortest translation of one mesh over 26 directions (cube faces, edges
  and corners) on the ladder 1.5, 3, 6, 12, 25, 50, 100 mm that frees it, refined by bisection. A pair freed by 1.5 mm is
  within the limit (DEPTH_MM).
* Containment: a mesh wholly inside another (no surfaces crossing) is found by generalised winding numbers of one vertex
  per connected piece.

Only rigid translations and per-axis scales occur in this video, so poses are 4x4 matrices applied to the vertices; a pose
with a scale gets its own BVH (cached by the scale).
"""
from __future__ import annotations

import math
import os
from itertools import product

import numpy as np

DEPTH_MM = 1.5
TOUCH_MM = 0.3
LADDER = (1.5, 3.0, 6.0, 12.0, 25.0, 50.0, 100.0)
DEEP = 999.0
_DIRS = np.array([d for d in product((-1, 0, 1), repeat=3) if any(d)], float)
_DIRS /= np.linalg.norm(_DIRS, axis=1)[:, None]


def _fcl():
    import fcl
    return fcl


def eroded(V, F, mm=TOUCH_MM):
    """V moved mm inwards along the vertex normals, each connected piece by the sign of its own volume (scene_audit.py)."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    V = np.asarray(V, float)
    if not len(F):
        return V
    key = np.round(V * 1000.0).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    W = V[first]
    Fw = inv[np.asarray(F, np.int64)]
    a, b, c = W[Fw[:, 0]], W[Fw[:, 1]], W[Fw[:, 2]]
    fn = np.cross(b - a, c - a)
    e = np.r_[Fw[:, [0, 1]], Fw[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(W), len(W)))
    nc, lab = connected_components(g, directed=False)
    vol = np.bincount(lab[Fw[:, 0]], weights=np.einsum("ij,ij->i", a, np.cross(b, c)), minlength=nc)
    sgn = np.where(vol >= 0.0, 1.0, -1.0)
    # angle-weighted vertex normals (scene_audit.py weights by area): with area weights, the end cap of a long extrusion
    # hardly moves, because its rim vertices are dominated by the long side faces, so two extrusions drawn end to face
    # read as interpenetrating
    un = fn / np.maximum(np.linalg.norm(fn, axis=1), 1e-12)[:, None]
    vn = np.zeros_like(W)
    P = (a, b, c)
    for k in range(3):
        e1 = P[(k + 1) % 3] - P[k]
        e2 = P[(k + 2) % 3] - P[k]
        cosang = np.einsum("ij,ij->i", e1, e2) / np.maximum(np.linalg.norm(e1, axis=1) * np.linalg.norm(e2, axis=1), 1e-12)
        ang = np.arccos(np.clip(cosang, -1.0, 1.0))
        np.add.at(vn, Fw[:, k], un * ang[:, None])
    vn /= np.maximum(np.linalg.norm(vn, axis=1), 1e-12)[:, None]
    Wm = W - mm * sgn[lab][:, None] * vn
    return Wm[inv]


def bvh(V, F):
    fcl = _fcl()
    g = fcl.BVHModel()
    g.beginModel(len(V), len(F))
    g.addSubModel(np.ascontiguousarray(V, np.float64), np.ascontiguousarray(F, np.int32))
    g.endModel()
    return g


def reps(V, F, k=8):
    """One vertex in each of the k largest connected pieces of a mesh."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    if not len(F):
        return np.asarray(V[:1], float)
    e = np.r_[F[:, [0, 1]], F[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(V), len(V)))
    nc, lab = connected_components(g, directed=False)
    used = np.zeros(len(V), bool)
    used[F.ravel()] = True
    cnt = np.bincount(lab[used], minlength=nc)
    out = []
    for c in np.argsort(-cnt)[:k]:
        if cnt[c] == 0:
            break
        out.append(V[np.nonzero((lab == c) & used)[0][0]])
    return np.asarray(out, float)


_WIND = []


def _wind_impl():
    os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba_cache")
    import numba

    @numba.njit(cache=True)
    def wind(P, V, F):
        out = np.zeros(P.shape[0])
        for k in range(P.shape[0]):
            s = 0.0
            for t in range(F.shape[0]):
                ax = V[F[t, 0], 0] - P[k, 0]
                ay = V[F[t, 0], 1] - P[k, 1]
                az = V[F[t, 0], 2] - P[k, 2]
                bx = V[F[t, 1], 0] - P[k, 0]
                by = V[F[t, 1], 1] - P[k, 1]
                bz = V[F[t, 1], 2] - P[k, 2]
                cx = V[F[t, 2], 0] - P[k, 0]
                cy = V[F[t, 2], 1] - P[k, 1]
                cz = V[F[t, 2], 2] - P[k, 2]
                la = math.sqrt(ax * ax + ay * ay + az * az)
                lb = math.sqrt(bx * bx + by * by + bz * bz)
                lc = math.sqrt(cx * cx + cy * cy + cz * cz)
                det = ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)
                div = la * lb * lc + (ax * bx + ay * by + az * bz) * lc + (bx * cx + by * cy + bz * cz) * la + \
                    (cx * ax + cy * ay + cz * az) * lb
                s += 2.0 * math.atan2(det, div)
            out[k] = s / (4.0 * math.pi)
        return out
    return wind


def winding(P, V, F):
    if not _WIND:
        _WIND.append(_wind_impl())
    return _WIND[0](np.ascontiguousarray(P, np.float64), np.ascontiguousarray(V, np.float64),
                    np.ascontiguousarray(F, np.int64))


class Geom:
    """One mesh (local coordinates): its BVH, its shrunk BVH, corners and representative points, built lazily."""
    __slots__ = ("V", "F", "lo", "hi", "_m", "_e", "_r", "_scaled", "_ve", "_er")

    def __init__(self, V, F):
        self.V = np.asarray(V, np.float64)
        self.F = np.asarray(F, np.int32)
        self.lo, self.hi = self.V.min(0), self.V.max(0)
        self._m = self._e = self._r = self._ve = self._er = None
        self._scaled = {}

    def model(self):
        if self._m is None:
            self._m = bvh(self.V, self.F)
        return self._m

    def ve(self):
        if self._ve is None:
            self._ve = eroded(self.V, self.F)
        return self._ve

    def emodel(self):
        if self._e is None:
            self._e = bvh(self.ve(), self.F)
        return self._e

    def rep(self):
        if self._r is None:
            self._r = reps(self.V, self.F)
        return self._r

    def erep(self):
        """The representative points taken from the shrunk mesh (0.3 mm inside the drawn surface)."""
        if self._er is None:
            self._er = reps(self.ve(), self.F)
        return self._er

    def scaled(self, s):
        """A copy scaled per axis about the origin (the lift column, a growing coupon), cached by the rounded scale."""
        key = tuple(np.round(s, 4))
        g = self._scaled.get(key)
        if g is None:
            g = self._scaled[key] = Geom(self.V * np.asarray(key), self.F)
        return g


def split(M):
    """A 4x4 pose -> (per-axis scale, translation); poses here are diag(scale) then a translation."""
    M = np.asarray(M, float)
    s = np.array([M[0, 0], M[1, 1], M[2, 2]])
    return s, M[:3, 3].copy()


def geom_at(g, M):
    """(geom, translation) for a pose: the geom itself if the pose has no scale."""
    s, t = split(M)
    if np.allclose(s, 1.0, atol=1e-6):
        return g, t
    return g.scaled(s), t


def world_box(g, t):
    return g.lo + t, g.hi + t


def _collide(oa, ob):
    fcl = _fcl()
    return fcl.collide(oa, ob, fcl.CollisionRequest(), fcl.CollisionResult()) > 0


def _contained(ga, ta, gb, tb):
    """A piece of a (shrunk) wholly inside b, or a piece of b inside the shrunk a (their surfaces apart). Using the shrunk
    mesh on a's side keeps two parts drawn face to face from reading as one inside the other."""
    for P, (V, F), ty in ((ga.erep() + ta, (gb.V, gb.F), tb), (gb.rep() + tb, (ga.ve(), ga.F), ta)):
        lo, hi = V.min(0) + ty, V.max(0) + ty
        P = P[np.all((P >= lo) & (P <= hi), axis=1)]
        if not len(P):
            continue
        if np.any(winding(P - ty, V, F) > 0.5):
            return True
    return False


def depth(ga, ta, gb, tb, need=DEPTH_MM):
    """Translational penetration depth of mesh a (shrunk TOUCH_MM, at translation ta) into mesh b (at tb): 0 if apart,
    <= need if a translation of `need` frees it, else the refined smallest freeing translation (DEEP past 100 mm)."""
    fcl = _fcl()
    oa = fcl.CollisionObject(ga.emodel(), fcl.Transform(np.eye(3), np.asarray(ta, float)))
    ob = fcl.CollisionObject(gb.model(), fcl.Transform(np.eye(3), np.asarray(tb, float)))

    def hit(t, inside=True):
        oa.setTransform(fcl.Transform(np.eye(3), np.asarray(t, float)))
        if _collide(oa, ob):
            return True
        return inside and _contained(ga, t, gb, tb)
    lo_a, hi_a = ga.lo + ta, ga.hi + ta
    lo_b, hi_b = gb.lo + tb, gb.hi + tb
    nest = bool(np.all(lo_a >= lo_b) and np.all(hi_a <= hi_b)) or bool(np.all(lo_b >= lo_a) and np.all(hi_b <= hi_a))
    if not hit(ta, nest):
        return 0.0
    c = 0.5 * (lo_a + hi_a) - 0.5 * (lo_b + hi_b)
    n = float(np.linalg.norm(c))
    order = np.argsort(-(_DIRS @ (c / n))) if n > 1e-9 else np.arange(len(_DIRS))
    prev = 0.0
    for step in LADDER:
        free = []
        for i in order:
            if not hit(np.asarray(ta) + step * _DIRS[i]):
                free.append(i)
                if step <= need or len(free) >= 4:
                    break
        if free:
            if step <= need:
                return step if step > need - 1e-9 else step
            best = step
            for i in free:
                lo, hi = prev, step
                for _ in range(4):
                    mid = 0.5 * (lo + hi)
                    if hit(np.asarray(ta) + mid * _DIRS[i]):
                        lo = mid
                    else:
                        hi = mid
                best = min(best, hi)
            return float(best)
        prev = step
    return DEEP
