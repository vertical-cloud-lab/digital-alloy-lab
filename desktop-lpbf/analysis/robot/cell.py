"""A UR12e (the UR10e renamed, byu-vcl notes/ur12e.md) with a Robotiq 2F-85 and a RealSense D405 on a MiR250, parked at
the Kardex opening as byu-vcl PR 318 lays it out, around the low-profile desktop LPBF (cad/lpbf_low.py) on its tray.

Aligned with byu-vcl PR 318 (round 14, commit 11d4410):
  * the arm, its kinematics, its gripper and wrist camera are PR 318's own `ur_arm.py` (vendored here unchanged except the
    cache folder): Universal Robots' and Robotiq's ROS 2 descriptions at pinned commits, closed-form IK;
  * the MiR250 is 800 x 580 x 300 mm with a 480 mm cabinet and a 20 mm mounting plate, so the arm's base is 800 mm above
    the floor (props.py); it parks with the arm's base 240 mm in front of the VLM's front face (animate.py: AMR_XY,
    ARM_LOCAL) and drives along the opening to line up with each job;
  * the VLM is a Kardex Shuttle XP 500 with 2450 x 864 mm trays: access table at 833 mm, presented tray floor at 857 mm,
    the 996 mm opening with the header's underside at 1829 mm (vlm.py), a 25 mm front skin, the tray presented 100 mm
    behind the front face;
  * collisions are checked on meshes with FCL (the arm against itself, and the arm, gripper, tools and what it holds
    against everything else, the MiR and the VLM included), never on convex hulls;
  * joint moves try every IK branch, nearest first, then the straight joint line, then RRT-Connect in joint space
    (edges checked every 1.5 deg, shortcut), with no detour lifting the arm more than 150 mm over the move's ends;
  * the audit is PR 318's round-11 rule: the gripper, its tools and a held part may touch the part being handled and
    that part's fixture around a grasp or release only up to 1.5 mm deep (sampled translational penetration depth, the
    part shrunk 0.3 mm first so drawn zero-clearance fits read as touching), and everything that moves (doors, drawer,
    reservoir, plate, module, the tool itself) is checked against everything else every frame ("movers").

Frames: this module works in the machine frame of cad/lpbf_low.py (mm, z up; plate centre at x = y = 0, the chamber floor's
top at z = 0, the tray's top at z = -212). PR 318's world maps to it by a shift: machine = world + (0, +1030, -1069).
"""
from __future__ import annotations

import functools
import json
import math
import os
import pathlib
import sys
import time

import numpy as np
import fcl

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parents[1] / "cad"
for p in (str(HERE), str(CAD)):
    if p not in sys.path:
        sys.path.insert(0, p)
import ur_arm  # noqa: E402  (byu-vcl PR 318's, vendored)

MODEL = "ur10e"                       # = UR12e: same kinematics, 12.5 kg, 1300 mm (byu-vcl notes/ur12e.md)
UR12E = dict(payload_kg=12.5, reach_mm=1300.0, tau_lim=(330.0, 330.0, 150.0, 56.0, 56.0, 56.0),
             tcp_force_N=(50.0, 250.0), ft_range_N=100.0,
             src="UR12e (UR10e renamed): universal-robots.com/products/ur12e-cb5; joint torque limits as the menagerie "
                 "UR10e; PFL force limit settable 50-250 N in the UR safety configuration; F/T sensor range +-100 N")

# ------------------------------------------------------------------------------------------------ PR 318's layout
WORLD_TO_MACHINE = np.array([0.0, 1030.0, -1069.0])
FLOOR_Z = -1069.0
TRAY_TOP_Z = 857.0 - 1069.0                          # -212, the model's Z_TRAY
VLM = dict(front_y=-1562.0 + 1030.0,                 # -532: outer face of the front skin
           skin=25.0,
           table_z=833.0 - 1069.0,                   # -236: the access table (TH1)
           header_z0=1829.0 - 1069.0,                # 760: underside of the header, 996 mm opening
           header_z1=1924.0 - 1069.0,
           std_header_z0=833.0 + 867.0 - 1069.0,     # 631: the standard opening's header (Kardex renders)
           roof_z=1910.0 - 1069.0,                   # 841: the bay roof
           open_half=1250.0, post=115.0,
           tray_front_y=-432.0, tray_back_y=432.0)
MIR = dict(L=800.0, W=580.0, H=300.0, cab_h=480.0, plate=20.0)
AMR_TOP = MIR["H"] + MIR["cab_h"] + MIR["plate"] + FLOOR_Z          # -269: arm base height in the machine frame
ARM_Y = (-1562.0 - 50.0 - 30.0 - MIR["W"] / 2 + 130.0) + 1030.0      # -772: arm base, 240 mm in front of the face
MIR_Y = ARM_Y - 130.0                                                 # -902: MiR centre (the arm sits 130 mm forward)

STEP_RAD = math.radians(1.5)
CONTAIN = os.environ.get("CELL_CONTAIN", "1") == "1"      # round 10: Checker.collisions also tests containment
DEPTH_MM = 1.5
TOUCH_MM = 0.3
LADDER = (DEPTH_MM, 3.0, 6.0, 12.0, 25.0, 50.0)
DEEP = 999.0
_DIRS = np.array([d for d in __import__("itertools").product((-1, 0, 1), repeat=3) if any(d)], float)
_DIRS /= np.linalg.norm(_DIRS, axis=1)[:, None]
ARM_LINKS = ("base", "shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3")
ADJACENT = {("base", "shoulder"), ("shoulder", "upper_arm"), ("upper_arm", "forearm"), ("forearm", "wrist1"),
            ("wrist1", "wrist2"), ("wrist2", "wrist3"), ("wrist3", "gripper")}
MAX_TRIS = int(os.environ.get("CELL_MAX_TRIS", "6000"))


# ------------------------------------------------------------------------------------------------ small helpers
def Tm(R=None, p=(0.0, 0.0, 0.0)) -> np.ndarray:
    M = np.eye(4)
    if R is not None:
        M[:3, :3] = R
    M[:3, 3] = p
    return M


def inv(M: np.ndarray) -> np.ndarray:
    Mi = np.eye(4)
    Mi[:3, :3] = M[:3, :3].T
    Mi[:3, 3] = -M[:3, :3].T @ M[:3, 3]
    return Mi


def frame(z, x) -> np.ndarray:
    """Rotation whose z axis is `z` (the tool's approach) and whose x axis is `x` made square to it (the direction the
    2F-85's fingers close along)."""
    z = np.asarray(z, float) / np.linalg.norm(z)
    x = np.asarray(x, float) - np.dot(x, z) * z
    x /= np.linalg.norm(x)
    return np.column_stack([x, np.cross(z, x), z])


def rot(axis, deg) -> np.ndarray:
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    t = math.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def slerp(R0, R1, s):
    from scipy.spatial.transform import Rotation, Slerp
    r = Rotation.from_matrix(np.stack([R0, R1]))
    return Slerp([0.0, 1.0], r)([s]).as_matrix()[0]


def box_mesh(x0, x1, y0, y1, z0, z1):
    v = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
    f = np.array([[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6],
                  [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3]], np.int32)
    return v, f


def merge(meshes):
    vs, fs, n = [], [], 0
    for v, f in meshes:
        vs.append(np.asarray(v, float))
        fs.append(np.asarray(f, np.int32) + n)
        n += len(v)
    return np.vstack(vs), np.vstack(fs)


def tess(shape, tol=0.4, ang=0.4):
    vs, fs = shape.tessellate(tol, ang)
    v = np.array([(p.x, p.y, p.z) for p in vs], float)
    f = np.array(fs, np.int32).reshape(-1, 3)
    return v, f


def loc_matrix(loc) -> np.ndarray:
    """4x4 of a cadquery Location."""
    if loc is None:
        return np.eye(4)
    t = loc.wrapped.Transformation()
    return np.array([[t.Value(i, j) for j in range(1, 5)] for i in range(1, 4)] + [[0, 0, 0, 1]], float)


def pv_to_vf(mesh):
    m = mesh.triangulate().clean()
    f = np.asarray(m.faces).reshape(-1, 4)[:, 1:]
    return np.asarray(m.points, float), f.astype(np.int32)


def decimate(v, f, max_tris=MAX_TRIS):
    if len(f) <= max_tris:
        return v, f
    import pyvista as pv
    m = pv.PolyData(v, np.c_[np.full(len(f), 3), f].ravel())
    m = m.decimate(1.0 - max_tris / len(f))
    return pv_to_vf(m)


# ------------------------------------------------------------------------------------------------ bodies
class Body:
    """A rigid mesh for FCL: vertices in its own frame, placed by a 4x4."""

    def __init__(self, name: str, v, f, kind: str, group: str = "", color="#b9c0c7", mat=None):
        self.name, self.kind, self.group, self.color = name, kind, group, color
        self.v = np.ascontiguousarray(v, float)
        self.f = np.ascontiguousarray(f, np.int32)
        g = fcl.BVHModel()
        g.beginModel(len(self.v), len(self.f))
        g.addSubModel(self.v, self.f)
        g.endModel()
        self.geom = g
        self.obj = fcl.CollisionObject(g, fcl.Transform())
        self.M = np.eye(4)
        self.lo, self.hi = self.v.min(0), self.v.max(0)
        self._ero = None
        self.mat = mat

    def place(self, M):
        self.M = np.asarray(M, float)
        self.obj.setTransform(fcl.Transform(self.M[:3, :3], self.M[:3, 3]))

    def box(self):
        c = np.array([[x, y, z] for x in (self.lo[0], self.hi[0]) for y in (self.lo[1], self.hi[1])
                      for z in (self.lo[2], self.hi[2])])
        w = c @ self.M[:3, :3].T + self.M[:3, 3]
        return w.min(0), w.max(0)

    def eroded(self):
        """The mesh shrunk TOUCH_MM along its vertex normals (byu-vcl collide._eroded): zero-clearance fits read as touching."""
        if self._ero is None:
            import trimesh
            m = trimesh.Trimesh(self.v, self.f, process=True)
            try:
                pieces = m.split(only_watertight=False)          # each connected piece by the sign of its own volume (byu-vcl
            except Exception:  # noqa: BLE001                    # collide._eroded): a held composite of several parts shrinks right
                pieces = [m]
            vs, fs, n = [], [], 0
            for pc in (pieces if len(pieces) else [m]):
                try:
                    trimesh.repair.fix_normals(pc)
                except Exception:  # noqa: BLE001
                    pass
                vol = pc.volume if pc.is_volume else 1.0
                sgn = 1.0 if vol >= 0 else -1.0
                vs.append(np.asarray(pc.vertices) - sgn * TOUCH_MM * np.asarray(pc.vertex_normals))
                fs.append(np.asarray(pc.faces) + n)
                n += len(pc.vertices)
            v2, f2 = np.vstack(vs), np.vstack(fs)
            g = fcl.BVHModel()
            g.beginModel(len(v2), len(f2))
            g.addSubModel(np.ascontiguousarray(v2, float), np.ascontiguousarray(f2, np.int32))
            g.endModel()
            self._ero = fcl.CollisionObject(g, fcl.Transform())
        self._ero.setTransform(fcl.Transform(self.M[:3, :3], self.M[:3, 3]))
        return self._ero


def hit(a, b) -> bool:
    return fcl.collide(a, b, fcl.CollisionRequest(), fcl.CollisionResult()) > 0


# ------------------------------------------------------------------------------------------------ containment (round 10)
# FCL's collide() sees two meshes' surfaces crossing. A body lying wholly inside another (a 0.5 mm liner inside the chamber
# body's wall between two samples, a dowel inside the table top) has no crossing, so until round 10 neither the planner nor
# rec_check.py saw it, and depth() could call a pair free once a short translation had pushed a thin part wholly inside the
# other (digital-alloy-lab #260, round 9's frame audit: 73 "part in part" pairs in chapter 41, found by winding numbers).
# inside(): point-in-mesh by ray parity, along two fixed generic directions (a ray along an axis would graze the CAD meshes'
# axis-aligned edges), the triangles binned on a grid across each ray, in numba; a point counts as inside only if both rays
# say so (open seams in a mesh give one wrong ray at most).
_RAYS = None
_INS = {}


def _ray_rots():
    global _RAYS
    if _RAYS is None:
        out = []
        for seed in (11, 23):
            q = np.random.default_rng(seed).normal(size=(3, 3))
            Q, _ = np.linalg.qr(q)
            out.append(np.ascontiguousarray(Q, float))
        _RAYS = out
    return _RAYS


try:
    import numba as _nb

    @_nb.njit(cache=True)
    def _bin_build(Vr, F, y0, z0, dy, dz, ny, nz):
        nt = F.shape[0]
        counts = np.zeros(ny * nz + 1, np.int64)
        for t in range(nt):
            a, b, c = F[t, 0], F[t, 1], F[t, 2]
            ymin = min(Vr[a, 1], min(Vr[b, 1], Vr[c, 1]))
            ymax = max(Vr[a, 1], max(Vr[b, 1], Vr[c, 1]))
            zmin = min(Vr[a, 2], min(Vr[b, 2], Vr[c, 2]))
            zmax = max(Vr[a, 2], max(Vr[b, 2], Vr[c, 2]))
            i0 = max(0, int((ymin - y0) / dy))
            i1 = min(ny - 1, int((ymax - y0) / dy))
            j0 = max(0, int((zmin - z0) / dz))
            j1 = min(nz - 1, int((zmax - z0) / dz))
            for i in range(i0, i1 + 1):
                for j in range(j0, j1 + 1):
                    counts[i * nz + j + 1] += 1
        start = np.cumsum(counts)
        idx = np.empty(start[-1], np.int64)
        fill = start[:-1].copy()
        for t in range(nt):
            a, b, c = F[t, 0], F[t, 1], F[t, 2]
            ymin = min(Vr[a, 1], min(Vr[b, 1], Vr[c, 1]))
            ymax = max(Vr[a, 1], max(Vr[b, 1], Vr[c, 1]))
            zmin = min(Vr[a, 2], min(Vr[b, 2], Vr[c, 2]))
            zmax = max(Vr[a, 2], max(Vr[b, 2], Vr[c, 2]))
            i0 = max(0, int((ymin - y0) / dy))
            i1 = min(ny - 1, int((ymax - y0) / dy))
            j0 = max(0, int((zmin - z0) / dz))
            j1 = min(nz - 1, int((zmax - z0) / dz))
            for i in range(i0, i1 + 1):
                for j in range(j0, j1 + 1):
                    k = i * nz + j
                    idx[fill[k]] = t
                    fill[k] += 1
        return start, idx

    @_nb.njit(cache=True)
    def _parity(P, Vr, F, start, idx, y0, z0, dy, dz, ny, nz):
        out = np.zeros(P.shape[0], np.int64)
        for m in range(P.shape[0]):
            px, py, pz = P[m, 0], P[m, 1], P[m, 2]
            i = int((py - y0) / dy) if py >= y0 else -1
            j = int((pz - z0) / dz) if pz >= z0 else -1
            if i < 0 or i >= ny or j < 0 or j >= nz:
                continue
            k = i * nz + j
            c = 0
            for s in range(start[k], start[k + 1]):
                t = idx[s]
                a, b, cc = F[t, 0], F[t, 1], F[t, 2]
                ay, az = Vr[a, 1], Vr[a, 2]
                e1y, e1z = Vr[b, 1] - ay, Vr[b, 2] - az
                e2y, e2z = Vr[cc, 1] - ay, Vr[cc, 2] - az
                d = e1y * e2z - e2y * e1z
                if d == 0.0:
                    continue
                qy, qz = py - ay, pz - az
                u = (qy * e2z - e2y * qz) / d
                v = (e1y * qz - qy * e1z) / d
                if u < 0.0 or v < 0.0 or u + v > 1.0:
                    continue
                x = Vr[a, 0] + u * (Vr[b, 0] - Vr[a, 0]) + v * (Vr[cc, 0] - Vr[a, 0])
                if x > px:
                    c += 1
            out[m] = c & 1
        return out
    _HAVE_NB = True
except Exception:  # noqa: BLE001
    _HAVE_NB = False


def _ins_index(b: Body):
    key = id(b.v)
    r = _INS.get(key)
    if r is not None and r[0] is b.v:
        return r[1]
    if len(_INS) > 4000:
        _INS.clear()
    F = np.ascontiguousarray(b.f, np.int64)
    out = []
    for R in _ray_rots():
        Vr = np.ascontiguousarray(b.v @ R.T, float)
        lo, hi = Vr.min(0), Vr.max(0)
        ext = np.maximum(hi - lo, 1e-6)
        ny = int(min(256, max(1, math.ceil(ext[1] / 2.0))))
        nz = int(min(256, max(1, math.ceil(ext[2] / 2.0))))
        dy, dz = ext[1] / ny * (1 + 1e-9), ext[2] / nz * (1 + 1e-9)
        start, idx = _bin_build(Vr, F, float(lo[1]), float(lo[2]), float(dy), float(dz), ny, nz)
        out.append((R, Vr, F, start, idx, float(lo[1]), float(lo[2]), float(dy), float(dz), ny, nz))
    _INS[key] = (b.v, out)
    return out


def inside(b: Body, pts_world) -> np.ndarray:
    """Which of the world points lie inside body b (at its placement): both rays' parities odd."""
    P = np.atleast_2d(np.asarray(pts_world, float))
    if not _HAVE_NB or not len(P):
        return np.zeros(len(P), bool)
    loc = (P - b.M[:3, 3]) @ b.M[:3, :3]
    res = np.ones(len(P), bool)
    for (R, Vr, F, start, idx, y0, z0, dy, dz, ny, nz) in _ins_index(b):
        Pr = np.ascontiguousarray(loc @ R.T, float)
        res &= _parity(Pr, Vr, F, start, idx, y0, z0, dy, dz, ny, nz).astype(bool)
        if not res.any():
            break
    return res


def _probe(b: Body, k=5):
    """A few of b's vertices (world), spread over the mesh, to test against another body."""
    n = len(b.v)
    sel = np.unique(np.linspace(0, n - 1, min(n, k)).astype(int))
    return b.v[sel] @ b.M[:3, :3].T + b.M[:3, 3]


def contained(x: Body, y: Body) -> bool:
    """One of x and y wholly inside the other, given that their surfaces do not cross (call after hit() is False): most of a
    few probe vertices of x inside y, or of y inside x. Boxes are checked first."""
    lx, hx = x.box()
    ly, hy = y.box()
    if np.any(lx > hy) or np.any(ly > hx):
        return False
    if np.all(lx >= ly) and np.all(hx <= hy):
        if inside(y, _probe(x)).mean() > 0.5:
            return True
    if np.all(ly >= lx) and np.all(hy <= hx):
        if inside(x, _probe(y)).mean() > 0.5:
            return True
    return False


def depth(x: Body, y: Body, upto=None, contain=True) -> float:
    """byu-vcl collide.depth(): the sampled translational penetration depth of x into y, rounded up to LADDER
    (0 = no contact, TOUCH_MM = only touching, DEEP = nothing up to 50 mm frees it). Round 10 (contain=True): a pose where x
    lies wholly inside y (or y inside x) is not free either, both at the start (a body inside another with no surface
    crossing is in contact, not clear) and at each trial translation (round 9 could call a 0.5 mm liner free once 1.5 mm
    had pushed it wholly inside the chamber body's wall)."""
    h = hit(x.obj, y.obj)
    if not h and not (contain and contained(x, y)):
        return 0.0
    xo = x.obj
    if h:
        try:
            e = x.eroded()
            if not hit(e, y.obj) and not (contain and contained(x, y)):
                return TOUCH_MM
            xo = e
        except Exception:  # noqa: BLE001
            pass
    lx, hx = x.box()
    ly, hy = y.box()
    c = (lx + hx - ly - hy) * 0.5
    n = float(np.linalg.norm(c))
    order = np.argsort(-(_DIRS @ (c / n))) if n > 1e-9 else np.arange(len(_DIRS))
    R, p = x.M[:3, :3].copy(), x.M[:3, 3].copy()
    M0 = x.M.copy()

    def free(q):
        xo.setTransform(fcl.Transform(R, q))
        if hit(xo, y.obj):
            return False
        if not contain:
            return True
        M = M0.copy()
        M[:3, 3] = q
        x.M = M                      # (the FCL object is restored in finally; contained() reads x.M only)
        return not contained(x, y)
    try:
        for k, t in enumerate(LADDER):
            for i in order:
                if free(p + t * _DIRS[i]):
                    return float(t)
            if upto is not None and t >= upto:
                return float(LADDER[k + 1]) if k + 1 < len(LADDER) else DEEP
        return DEEP
    finally:
        x.M = M0
        xo.setTransform(fcl.Transform(R, p))
        if xo is not x.obj:
            x.obj.setTransform(fcl.Transform(R, p))


class Group:
    """A set of bodies. Broad phase by world-frame bounding boxes (numpy), narrow phase by FCL on the meshes.
    (python-fcl's managers hand their callbacks new wrapper objects, so a body can't be told from its callback.)"""

    def __init__(self, bodies=()):
        self.bodies: dict[str, Body] = {}
        for b in bodies:
            self.add(b)

    def add(self, b: Body):
        self.bodies[b.name] = b

    def remove(self, name):
        self.bodies.pop(name, None)

    def boxes(self):
        names = list(self.bodies)
        lo = np.empty((len(names), 3))
        hi = np.empty((len(names), 3))
        for i, n in enumerate(names):
            lo[i], hi[i] = self.bodies[n].box()
        return names, lo, hi


def group_hits(A: Group, B: Group, first=False, margin=0.0, missed=None):
    """Pairs (a, b) of bodies of A and B whose meshes intersect. Round 10: `missed`, a list, gets the pairs whose boxes overlap
    but whose meshes do not cross (for the containment test), unless `first` stopped early."""
    na, la, ha = A.boxes()
    nb, lb, hb = B.boxes()
    ov = np.all((la[:, None, :] - margin <= hb[None, :, :]) & (lb[None, :, :] <= ha[:, None, :] + margin), axis=2)
    out = []
    for i, j in zip(*np.nonzero(ov)):
        a, b = A.bodies[na[i]], B.bodies[nb[j]]
        if hit(a.obj, b.obj):
            out.append((a, b))
            if first:
                return out
        elif missed is not None:
            missed.append((a, b))
    return out


def group_contained(A: Group, B: Group, kinds=("held", "tool", "gripper"), skip=(), pairs=None):
    """Round 10: pairs (a, b), a of one of `kinds`, whose boxes overlap and surfaces do not cross but one lies wholly inside the
    other (FCL's group_hits misses them). `pairs`: group_hits' `missed` list (box overlap, no crossing), else computed here."""
    if pairs is None:
        pairs = []
        group_hits(A, B, missed=pairs)
    out = []
    for a, b in pairs:
        if a.kind not in kinds or (a.name, b.name) in skip:
            continue
        if contained(a, b):
            out.append((a, b))
    return out


def group_distance(A: Group, B: Group, margin=60.0):
    """(distance, a, b): the closest pair of bodies within `margin` of each other (inf if none); <= 0 if touching."""
    na, la, ha = A.boxes()
    nb, lb, hb = B.boxes()
    ov = np.all((la[:, None, :] - margin <= hb[None, :, :]) & (lb[None, :, :] <= ha[:, None, :] + margin), axis=2)
    best = (math.inf, None, None)
    for i, j in zip(*np.nonzero(ov)):
        a, b = A.bodies[na[i]], B.bodies[nb[j]]
        if hit(a.obj, b.obj):
            return (0.0, a, b)
        d = fcl.distance(a.obj, b.obj, fcl.DistanceRequest(), fcl.DistanceResult())
        if d < best[0]:
            best = (d, a, b)
    return best


# ------------------------------------------------------------------------------------------------ the arm
@functools.lru_cache(maxsize=None)
def _arm_geometry():
    links = {}
    for k, lst in ur_arm.arm_meshes(MODEL).items():
        links[k] = decimate(*merge([pv_to_vf(m) for m, _, _ in lst]))
    grip = {}
    for k, lst in ur_arm.gripper_meshes().items():
        grip[k] = decimate(*merge([pv_to_vf(m) for m, _, _ in lst]), max_tris=4000)
    return links, grip


class Arm:
    """One UR12e + 2F-85 (+ D405) on a MiR250 whose arm base is at `base` (machine frame). Finger caps (tools that slip
    over the 2F-85's fingertips) and a held part ride along."""

    def __init__(self, name="ur", base=(0.0, ARM_Y, AMR_TOP), yaw_deg=0.0, caps=None):
        self.name = name
        self.base = Tm(rot((0, 0, 1), yaw_deg), base)
        links, grip = _arm_geometry()
        self.links = {k: Body(f"{name}/{k}", *links[k], kind="arm", group=k, color="#9aa6b2") for k in ARM_LINKS}
        self.grip = {k: Body(f"{name}/gr/{k}", *grip[k], kind="gripper", group="gripper", color="#2b2f33")
                     for k in grip}
        self.caps = {}            # fingertip name -> Body in that fingertip's frame
        self.cap_spec = None
        if caps:
            self.set_caps(caps)
        self.held = None          # (Body, offset from TCP)
        self.q = np.radians([-90.0, -100.0, 120.0, -110.0, -90.0, 0.0])
        self.close = 0.0
        self.robot = Group(list(self.links.values()) + list(self.grip.values()))
        self._acm = None

    # ---- tools
    def set_caps(self, spec):
        """spec: dict(name, meshes={"left_finger_tip": (v, f), "right_finger_tip": (v, f)}, grasp_z=..., inner_x=...,
        color=...). The grasp point is the midpoint of the two caps' inner faces at z = grasp_z in the fingertip frames."""
        for b in self.caps.values():
            self.robot.remove(b.name) if hasattr(self, "robot") else None
        self.caps = {}
        self.cap_spec = spec
        if spec is None:
            return
        for tip, (v, f) in spec["meshes"].items():
            b = Body(f"{self.name}/cap/{tip}", v, f, kind="tool", group="gripper", color=spec.get("color", "#d9b23a"))
            self.caps[tip] = b
            if hasattr(self, "robot"):
                self.robot.add(b)

    def tcp_mm(self, close=None) -> float:
        c = self.close if close is None else close
        if not self.cap_spec:
            return ur_arm.tcp_mm(c)
        G = ur_arm.gripper_fk(c)
        zg, xi = self.cap_spec["grasp_z"], self.cap_spec["inner_x"]
        pl = (G["left_finger_tip"] @ np.array([-xi, 0, zg, 1.0]))[:3]
        pr = (G["right_finger_tip"] @ np.array([xi, 0, zg, 1.0]))[:3]
        return float((pl[2] + pr[2]) / 2)

    def gap_mm(self, close=None) -> float:
        """Distance between the gripping faces (stock pads, or the caps' inner faces)."""
        c = self.close if close is None else close
        G = ur_arm.gripper_fk(c)
        if not self.cap_spec:
            xi, zg = 25.26, 31.9
        else:
            xi, zg = self.cap_spec["inner_x"], self.cap_spec["grasp_z"]
        pl = (G["left_finger_tip"] @ np.array([-xi, 0, zg, 1.0]))[:3]
        pr = (G["right_finger_tip"] @ np.array([xi, 0, zg, 1.0]))[:3]
        return float(np.linalg.norm(pl - pr))

    def close_for_gap(self, gap) -> float:
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if self.gap_mm(mid) > gap:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    # ---- kinematics
    def fk(self, q=None):
        return ur_arm.fk(MODEL, self.q if q is None else q)

    def grasp_y(self) -> float:
        """Offset (mm) of the grasp point along tool0's y axis: 0 for the stock pads and straight caps; the drop of cranked
        caps (eoat.py's plate fingers), whose blades step sideways from the pads to reach under a sill."""
        return float(self.cap_spec.get("grasp_y", 0.0)) if self.cap_spec else 0.0

    def tcp_off(self, close=None) -> np.ndarray:
        """tool0 -> TCP (the grasp point), 4x4."""
        return Tm(p=(0.0, self.grasp_y(), self.tcp_mm(close)))

    def tcp(self, q=None, close=None) -> np.ndarray:
        F = self.fk(q)
        return self.base @ F["tool0"] @ self.tcp_off(close)

    def place(self, q=None, close=None):
        if q is not None:
            self.q = np.asarray(q, float)
        if close is not None:
            self.close = float(close)
        F = self.fk()
        for k, b in self.links.items():
            b.place(self.base @ F[k])
        G = ur_arm.gripper_fk(self.close)
        Wt = self.base @ F["tool0"]
        for k, b in self.grip.items():
            b.place(Wt @ G[k])
        for tip, b in self.caps.items():
            b.place(Wt @ G[tip])
        if self.held is not None:
            hb, off = self.held
            hb.place(Wt @ self.tcp_off() @ off)
        return F

    def ik_all(self, T_tcp_world, seed=None):
        """Every IK branch for a TCP pose (machine frame), nearest the seed first (byu-vcl collide.ik_all)."""
        seed = self.q if seed is None else np.asarray(seed, float)
        off = inv(self.tcp_off())
        T06 = inv(self.base) @ np.asarray(T_tcp_world, float) @ off
        out = []
        for s in ur_arm._ik_analytic(MODEL, T06, q6_free=float(seed[5])):
            q = ur_arm._polish(MODEL, ur_arm._wrap_near(s, seed), T06)
            e = ur_arm._pose_err(ur_arm.fk(MODEL, q)["tool0"], T06)
            if np.linalg.norm(e[:3]) < 1e-3 and np.linalg.norm(e[3:]) < 1e-6:
                q = ur_arm._wrap_near(q, seed)
                if np.all(np.abs(q) <= ur_arm._LIMIT + 1e-9) and all(np.abs(q - o).max() > 1e-4 for o in out):
                    out.append(q)
        out.sort(key=lambda q: float(np.sum((q - seed) ** 2)))
        return out

    def reach_margin(self, q=None) -> float:
        F = self.fk(q)
        d = np.linalg.norm(F["wrist1"][:3, 3] - F["shoulder"][:3, 3]) if "shoulder" in F else 0.0
        return float(612.7 + 571.55 - d)

    # ---- self-collision pairs (MoveIt's "always touching" pairs left out, as byu-vcl does)
    def self_pairs(self):
        if self._acm is None:
            cache = pathlib.Path(os.environ.get("CELL_ACM_CACHE", "/tmp/cell_acm.json"))
            if cache.exists():
                always = {tuple(p) for p in json.loads(cache.read_text())}
            else:
                rng = np.random.default_rng(7)
                names = list(ARM_LINKS) + ["gripper"]
                counts = {}
                n = 300
                q0, c0 = self.q.copy(), self.close
                for _ in range(n):
                    self.place(rng.uniform(-math.pi, math.pi, 6), float(rng.uniform(0, 1)))
                    grp = {k: [self.links[k]] for k in ARM_LINKS}
                    grp["gripper"] = list(self.grip.values())
                    for i, a in enumerate(names):
                        for b in names[i + 1:]:
                            if any(hit(x.obj, y.obj) for x in grp[a] for y in grp[b]):
                                counts[(a, b)] = counts.get((a, b), 0) + 1
                self.place(q0, c0)
                always = {p for p, c in counts.items() if c > 0.9 * n}
                cache.write_text(json.dumps(sorted(always)))
            names = list(ARM_LINKS) + ["gripper"]
            skip = ADJACENT | always
            self._acm = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]
                         if (a, b) not in skip and (b, a) not in skip]
        return self._acm

    def self_hits(self):
        out = []
        grp = {k: [self.links[k]] for k in ARM_LINKS}
        grp["gripper"] = list(self.grip.values()) + list(self.caps.values()) + ([self.held[0]] if self.held else [])
        for a, b in self.self_pairs():
            for x in grp[a]:
                for y in grp[b]:
                    if hit(x.obj, y.obj):
                        out.append((x.name, y.name))
        return out

    def bodies(self):
        yield from self.links.values()
        yield from self.grip.values()
        yield from self.caps.values()
        if self.held is not None:
            yield self.held[0]


# ------------------------------------------------------------------------------------------------ the scene
def vlm_and_mir_bodies(arm_x=0.0, mir_y=MIR_Y, header="996", deck=False):
    """The parts of the VLM round the opening and the MiR250 + cabinet under the arm (byu-vcl vlm.py, props.mir250)."""
    out = []
    fy, sk = VLM["front_y"], VLM["skin"]
    hz0 = VLM["header_z0"] if header == "996" else VLM["std_header_z0"]
    oh, po = VLM["open_half"], VLM["post"]
    out.append(("VLM front skin under the opening", box_mesh(-oh - po, oh + po, fy, fy + sk, FLOOR_Z, VLM["table_z"])))
    out.append(("VLM access table", box_mesh(-oh, oh, fy + sk, VLM["tray_front_y"] - 2.0, VLM["table_z"] - 20.0,
                                              VLM["table_z"])))
    out.append(("VLM header", box_mesh(-oh - po, oh + po, fy, VLM["tray_front_y"] - 2.0, hz0, VLM["header_z1"])))
    for s in (-1, 1):
        out.append((f"VLM side post {'+x' if s > 0 else '-x'}",
                    box_mesh(min(s * oh, s * (oh + po)), max(s * oh, s * (oh + po)), fy, VLM["tray_front_y"],
                             VLM["table_z"], hz0)))
    L, W, H, C = MIR["L"], MIR["W"], MIR["H"], MIR["cab_h"]
    x0, y0, z0 = arm_x, mir_y, FLOOR_Z
    out.append(("MiR250 body", box_mesh(x0 - L / 2, x0 + L / 2, y0 - W / 2, y0 + W / 2, z0 + 30, z0 + H)))
    out.append(("MiR250 cabinet (UR control box)", box_mesh(x0 - L / 2 + 40, x0 + L / 2 - 40, y0 - W / 2 + 30,
                                                             y0 + W / 2 - 30, z0 + H, z0 + H + C)))
    out.append(("MiR250 mounting plate", box_mesh(x0 - 170, x0 + 170, y0 - W / 2 + 30, y0 + W / 2 - 30, z0 + H + C,
                                                   z0 + H + C + MIR["plate"])))
    if deck:
        out += mir_deck_bodies(x0, y0)
    return out


# PR 318 round 9: a 131 kg steel ballast plate, 760 x 550 x 40 mm, on the MiR250's deck under the cabinet (alloy_atomize.BALLAST)
BALLAST = dict(L=760.0, W=550.0, T=40.0, kg=7.85e-6 * 760.0 * 550.0 * 40.0)


def mir_deck_bodies(x0, y0):
    """The MiR250's own fixtures (MiR-local layout, our design): the ballast plate at the cabinet's foot; on the cabinet top,
    beside the arm's mounting plate, the fork stand that holds the plate-finger caps (eoat.PLATE_FINGERS; the arm slides its
    fingertips into them and the forks strip them off, as byu-vcl PR 318's specimen fingers) and the cradle the vacuum wand
    rests in (its hose runs down to the ATEX vacuum beside the VLM). Names start with "MiR250" so move_mir() carries them."""
    H, C = MIR["H"], MIR["cab_h"]
    z0 = FLOOR_Z
    top = z0 + H + C
    L, W, T = BALLAST["L"], BALLAST["W"], BALLAST["T"]
    out = [("MiR250 ballast plate (131 kg steel)", box_mesh(x0 - L / 2, x0 + L / 2, y0 - W / 2, y0 + W / 2, z0 + H, z0 + H + T))]
    # cap stand: two forks 60 mm apart in x on a 70 mm post, right of the arm's plate; the caps hang in the forks, open side up
    sx = x0 + 250.0
    stand = [box_mesh(sx - 50, sx + 50, y0 - 40, y0 + 40, top, top + 12),          # foot
             box_mesh(sx - 8, sx + 8, y0 - 8, y0 + 8, top + 12, top + 82)]         # post
    for dx in (-30.0, 30.0):                                                       # forks: two prongs each, 16 mm apart in y
        for dy in (-12.0, 8.0):
            stand.append(box_mesh(sx + dx - 3, sx + dx + 3, y0 + dy, y0 + dy + 4, top + 82, top + 112))
        stand.append(box_mesh(sx + dx - 9, sx + dx + 9, y0 - 12, y0 + 12, top + 76, top + 82))
    out.append(("MiR250 cap stand (forks for the plate fingers)", merge(stand)))
    # wand cradle: two U-blocks on the cabinet's left part, under the wand's tube behind its collar and ahead of it (eoat.WAND: the
    # wand points at the VLM, its axis 39 mm over the cabinet top)
    wx = x0 - 260.0
    cr = []
    for yy in (y0 - 62.0, y0 + 125.0):          # the wand's axis 75 mm over the cabinet top, so its bent crevice tool clears the front edge
        cr += [box_mesh(wx - 35, wx - 25, yy - 15, yy + 15, top, top + 96), box_mesh(wx + 25, wx + 35, yy - 15, yy + 15, top, top + 96),
               box_mesh(wx - 35, wx + 35, yy - 15, yy + 15, top, top + 56)]
    out.append(("MiR250 wand cradle", merge(cr)))
    return out


class Scene:
    """The machine (posed for a motion state), the VLM, the MiR, the robot(s) and tools; collision queries and the audit."""

    def __init__(self, parts, region=None, tol=0.4, header="996", arm_x=0.0, mir_y=MIR_Y, extra=(), skip=(), deck=False):
        import lpbf_low as M
        self.M = M
        self.parts = parts
        self.state = {}
        self.world = Group()
        self.machine = {}          # name -> (Body, Part)
        t0 = time.time()
        for p in parts:
            if "context" in p.tags and not p.name.startswith("VLM tray"):
                continue
            if any(s in p.name for s in skip):
                continue
            bb = p.shape.BoundingBox()
            if region is not None:
                (x0, x1), (y0, y1), (z0, z1) = region
                if bb.xmax < x0 or bb.xmin > x1 or bb.ymax < y0 or bb.ymin > y1 or bb.zmax < z0 or bb.zmin > z1:
                    continue
            v, f = tess(p.shape, tol)
            if len(f) == 0:
                continue
            b = Body(p.name, v, f, kind="machine", group=p.group, color=p.color, mat=p.mat)
            self.world.add(b)
            self.machine[p.name] = (b, p)
        self.static_names = set()
        self.arm_x = arm_x
        for name, (v, f) in vlm_and_mir_bodies(arm_x, mir_y, header, deck=deck):
            b = Body(name, v, f, kind="cell", color="#6f777e" if name.startswith("VLM") else "#3b4148")
            self.world.add(b)
        for name, (v, f), color in extra:
            self.world.add(Body(name, v, f, kind="fixture", color=color))
        self.tess_s = time.time() - t0
        self.set_state({})

    def move_mir(self, arm_x):
        """Drive the MiR along the opening so the arm's base is at x = arm_x (the arm's own base is set by the caller)."""
        dx = arm_x - self.arm_x
        for name in [n for n in self.world.bodies if n.startswith("MiR250")]:
            b = self.world.bodies[name]
            b.place(Tm(p=(b.M[0, 3] + dx, b.M[1, 3], b.M[2, 3])))
        self.arm_x = arm_x

    def set_state(self, state, overrides=None):
        """Pose the machine for a motion state {group: value}. overrides {part name: 4x4} put a part somewhere else
        (applied on top of its group's pose): a plate lifted off its block, a jar carried off its flange."""
        self.state = dict(state)
        ov = overrides or {}
        prev = getattr(self, "overrides", {})
        for name, (b, p) in self.machine.items():
            if p.group or "in_module" in p.tags or name in ov or name in prev:
                Mg = loc_matrix(self.M.part_location(p, self.state))
                b.place(ov[name] @ Mg if name in ov else Mg)
        self.overrides = dict(ov)
        return self

    def moved_since(self, prev_state):
        """Names of machine bodies whose pose differs between prev_state and the current state."""
        out = []
        for name, (b, p) in self.machine.items():
            if not (p.group or "in_module" in p.tags):
                continue
            Ma = loc_matrix(self.M.part_location(p, prev_state))
            if not np.allclose(Ma, b.M, atol=1e-6):
                out.append(name)
        return out


# ------------------------------------------------------------------------------------------------ checker + planner
class Checker:
    """What the arm (links, gripper, caps, held part) touches at a joint pose, under the audit's rules."""

    def __init__(self, scene: Scene, arm: Arm):
        self.sc, self.arm = scene, arm

    def collisions(self, q, close=None, allow=frozenset(), first=False, depth_limit=DEPTH_MM):
        """[(robot body, world body, depth)] at q. Pairs in `allow` (robot-side name prefix or 'held', world body name)
        count only if deeper than depth_limit."""
        a = self.arm
        a.place(q, close)
        out = []
        robot = a.robot
        # round 9 (digital-alloy-lab #260): the bodies an arm subclass keeps on the flange outside `grip` (cell2.ArmT's wrist camera
        # and tool changer, in `fixed`) are its own too. Until round 9 they were dropped from the group here on the first check,
        # so the assembly planner never checked the D405 or the changer against the world (round 9's recording check found arm
        # A's camera 50 mm into the chamber floor plate on a planned move to park, C00d)
        fixed = getattr(a, "fixed", None) or {}
        own = ({b.name for b in a.links.values()} | {b.name for b in a.grip.values()} | {b.name for b in a.caps.values()} |
               {b.name for b in fixed.values()})
        for nm in [n for n in robot.bodies if n not in own and (a.held is None or n != a.held[0].name)]:
            robot.remove(nm)          # a part held earlier and since let go must not ride along at its old pose
        for b in fixed.values():
            if b.name not in robot.bodies:
                robot.add(b)
        if a.held is not None and a.held[0].name not in robot.bodies:
            robot.add(a.held[0])
        missed = [] if CONTAIN else None
        hits = group_hits(robot, self.sc.world, missed=missed)
        for x, y in hits:
            key = ("held" if (a.held is not None and x is a.held[0]) else
                   ("tool" if x.kind in ("gripper", "tool") else "arm"), y.name)
            if key[0] != "arm" and ("soft", y.name) in allow:
                continue              # a seal the handled part slides over or squeezes (byu-vcl collide: sc.soft)
            if x.group == "base" and y.name.startswith("MiR250"):
                continue              # the arm's base and the plate it is bolted to (byu-vcl collide: always allowed)
            if key in allow or (key[0] == "tool" and ("tool", "*") in allow and y.kind == "fixture"):
                d = depth(x, y, upto=depth_limit)
                if d <= depth_limit:
                    continue
                out.append((x.name, y.name, d))
            else:
                out.append((x.name, y.name, None))
            if first:
                return out
        if CONTAIN:
            # round 10: the held part, the tool and the gripper wholly inside something present (or it inside them), which
            # group_hits cannot see; counted like a crossing deeper than the allowance (a touch that only reads as inside
            # comes out of depth() at 1.5 mm or less and passes)
            for x, y in group_contained(robot, self.sc.world, pairs=missed):
                key = ("held" if (a.held is not None and x is a.held[0]) else "tool", y.name)
                if ("soft", y.name) in allow or ("inside", y.name) in allow:
                    continue
                if x.group == "base" and y.name.startswith("MiR250"):
                    continue
                d = depth(x, y, upto=depth_limit)
                if d <= depth_limit:
                    continue
                out.append((x.name, y.name, d))
                if first:
                    return out
        for xn, yn in a.self_hits():
            out.append((xn, yn, "self"))
            if first:
                return out
        return out

    def free(self, q, close=None, allow=frozenset()):
        return not self.collisions(q, close, allow, first=True)

    def top(self, q):
        F = self.arm.fk(q)
        return max(float((self.arm.base @ F[k])[2, 3]) for k in ("forearm", "wrist1", "wrist2", "wrist3"))

    def segment_free(self, qa, qb, close, allow, zmax=None):
        n = max(1, int(math.ceil(np.abs(qb - qa).max() / STEP_RAD)))
        for i in range(1, n + 1):
            q = qa + (qb - qa) * (i / n)
            if zmax is not None and self.top(q) > zmax:
                return False
            if not self.free(q, close, allow):
                return False
        return True

    def plan(self, q0, q1, close, allow=frozenset(), seed=0, iters=3000, step=0.3):
        """byu-vcl collide.plan_joint_move: the straight joint line if clear, otherwise RRT-Connect, shortcut."""
        q0, q1 = np.asarray(q0, float), np.asarray(q1, float)
        b0 = self.collisions(q0, close, allow)
        b1 = self.collisions(q1, close, allow)
        if b0 or b1:
            return None, dict(reason="end pose in collision", start=b0[:3], goal=b1[:3])
        if self.segment_free(q0, q1, close, allow):
            return [q0, q1], dict(planned=False)
        zmax = max(self.top(q0), self.top(q1)) + 150.0
        rng = np.random.default_rng(seed)
        lim = ur_arm._LIMIT
        lo = np.maximum(np.minimum(q0, q1) - math.pi, -lim)
        hi = np.minimum(np.maximum(q0, q1) + math.pi, lim)

        def ok(q):
            return self.top(q) <= zmax and self.free(q, close, allow)

        def extend(tree, parent, q_to):
            d = np.linalg.norm(np.asarray(tree) - q_to, axis=1)
            i = int(np.argmin(d))
            qn = tree[i]
            v = q_to - qn
            L = float(np.linalg.norm(v))
            q_new = q_to if L <= step else qn + v * (step / L)
            if not ok(q_new) or not self.segment_free(qn, q_new, close, allow, zmax):
                return None
            tree.append(q_new)
            parent.append(i)
            return len(tree) - 1

        def connect(tree, parent, q_to):
            last = None
            while True:
                k = extend(tree, parent, q_to)
                if k is None:
                    return last, False
                last = k
                if np.linalg.norm(tree[k] - q_to) < 1e-9:
                    return k, True

        A, pa, B, pb = [q0], [-1], [q1], [-1]
        swapped = False
        for it in range(iters):
            q_rand = q1 if rng.random() < 0.1 else rng.uniform(lo, hi)
            k = extend(A, pa, q_rand)
            if k is not None:
                j, okc = connect(B, pb, A[k])
                if okc:
                    def trace(tree, parent, idx):
                        out = []
                        while idx >= 0:
                            out.append(tree[idx])
                            idx = parent[idx]
                        return out
                    path = trace(A, pa, k)[::-1] + trace(B, pb, j)[1:]
                    if swapped:
                        path = path[::-1]
                    path = self.shortcut(path, close, allow, rng, zmax)
                    return path, dict(planned=True, iterations=it + 1, nodes=len(A) + len(B), waypoints=len(path))
            A, pa, B, pb = B, pb, A, pa
            swapped = not swapped
        return None, dict(reason=f"no path in {iters} iterations")

    def shortcut(self, path, close, allow, rng, zmax, rounds=100):
        path = [np.asarray(p, float) for p in path]
        for _ in range(rounds):
            if len(path) <= 2:
                break
            i, j = sorted(rng.choice(len(path), 2, replace=False))
            if j - i < 2:
                continue
            if self.segment_free(path[i], path[j], close, allow, zmax):
                path = path[:i + 1] + path[j:]
        k = 1
        while k < len(path) - 1:
            if self.segment_free(path[k - 1], path[k + 1], close, allow, zmax):
                path.pop(k)
            else:
                k += 1
        return path


def densify(path, step=STEP_RAD):
    out = [np.asarray(path[0], float)]
    for a, b in zip(path[:-1], path[1:]):
        n = max(1, int(math.ceil(np.abs(b - a).max() / step)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return out


# ------------------------------------------------------------------------------------------------ statics
# UR10e/UR12e link masses (kg) and centres of mass in the DH link frames (m), Universal Robots' published DH and
# dynamics table ("DH parameters for calculations of kinematics and dynamics", UR10e column).
UR10E_DYN = dict(m=[7.369, 13.051, 3.989, 2.1, 1.98, 0.615],
                 com=[(0.021, 0.000, 0.027), (0.38, 0.000, 0.158), (0.24, 0.000, 0.068), (0.000, 0.007, 0.018),
                      (0.000, 0.007, 0.018), (0.0, 0.0, -0.026)])


def jacobian(arm: Arm, q, p_world):
    """Geometric Jacobian (6 x 6, mm and rad) of a point fixed to the flange, by finite differences."""
    q = np.asarray(q, float)
    T0 = arm.base @ arm.fk(q)["tool0"]
    p_local = inv(T0) @ np.r_[p_world, 1.0]
    J = np.zeros((6, 6))
    for i in range(6):
        dq = np.zeros(6)
        dq[i] = 1e-6
        T1 = arm.base @ arm.fk(q + dq)["tool0"]
        J[:3, i] = ((T1 @ p_local)[:3] - (T0 @ p_local)[:3]) / 1e-6
        dR = T1[:3, :3] @ T0[:3, :3].T
        J[3:, i] = np.array([dR[2, 1] - dR[1, 2], dR[0, 2] - dR[2, 0], dR[1, 0] - dR[0, 1]]) / 2 / 1e-6
    return J


def link_coms(arm: Arm, q):
    """World centres of mass (mm) of the six moving links, placed geometrically as byu-vcl PR 318's stability() does: the
    shoulder at its joint, the upper arm and forearm at the middle of their tubes (the upper arm's tube offset 158 mm along its
    joint axis, UR's dynamics table), the three wrist links at their joints."""
    F = arm.fk(q)
    W = {k: arm.base @ F[k] for k in ("shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3", "tool0")}
    o = {k: W[k][:3, 3] for k in W}
    z_ua = W["upper_arm"][:3, 2]
    return [o["shoulder"], (o["upper_arm"] + o["forearm"]) / 2 + 158.0 * z_ua, (o["forearm"] + o["wrist1"]) / 2,
            o["wrist1"], o["wrist2"], o["wrist3"]], W


def static_torques(arm: Arm, q, F_world=(0, 0, 0), p_world=None, payload_kg=0.0, tool_kg=1.3):
    """Joint torques (N m) the motors need to hold pose q against gravity (the links' masses from UR's UR10e/UR12e table at
    link_coms(), the 2F-85 + coupling + camera and caps as tool_kg at the flange, the payload at the TCP) and against a force
    F_world (N, acting on the robot) at p_world (mm, default the TCP). Joint j turns about the z axis of its child frame, so
    tau_j = z_j . sum over everything outboard of j of (r - o_j) x F. (Fixed 2026-11-20: the earlier version moved every link's
    centre of mass with the flange, which loaded the wrists with the whole arm's weight.)"""
    q = np.asarray(q, float)
    g = np.array([0.0, 0.0, -9.81])
    coms, W = link_coms(arm, q)
    names = ["shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3"]
    tcp = arm.tcp(q)[:3, 3]
    loads = [(i, coms[i], UR10E_DYN["m"][i] * g) for i in range(6)]          # (first joint it does NOT hang outboard of, point, force)
    loads.append((6, W["tool0"][:3, 3], tool_kg * g))
    loads.append((6, tcp, payload_kg * g))
    if p_world is None:
        p_world = tcp
    loads.append((6, np.asarray(p_world, float), np.asarray(F_world, float)))
    tau = np.zeros(6)
    for j in range(6):
        oj, zj = W[names[j]][:3, 3], W[names[j]][:3, 2]
        for i, r, Fv in loads:
            if i >= j:
                tau[j] += float(zj @ np.cross((np.asarray(r) - oj) / 1000.0, Fv))
    return -tau          # the motors' torque that balances the loads


def max_force(arm: Arm, q, direction, p_world=None, payload_kg=0.0, tool_kg=1.3, frac=1.0):
    """Largest force (N) the arm can push along `direction` at p_world before a joint reaches frac x its torque limit."""
    d = np.asarray(direction, float) / np.linalg.norm(direction)
    lim = np.array(UR12E["tau_lim"]) * frac
    t0 = static_torques(arm, q, payload_kg=payload_kg, tool_kg=tool_kg)
    t1 = static_torques(arm, q, F_world=d, p_world=p_world, payload_kg=payload_kg, tool_kg=tool_kg) - t0
    best = math.inf
    for i in range(6):
        if abs(t1[i]) < 1e-9:
            continue
        room = (lim[i] - t0[i]) / t1[i] if t1[i] > 0 else (-lim[i] - t0[i]) / t1[i]
        best = min(best, room)
    return float(best)
