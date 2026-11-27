"""Bonding and ground leads for the sieving animation: simulated cables, alligator clips and ring lugs.

NFPA 484 / NFPA 77 practice bonds everything conductive that the powder touches (the powder container, the stainless
tray, the sieve pan) to one ground with flexible leads. Each lead here is a green 14 AWG lead simulated as a chain of
nodes about 6 mm apart with position-based dynamics (Mueller et al. 2007), twelve small substeps a frame: gravity, an
implicit (backward-Euler) bending step, inextensible segments solved directly along the chain (a tridiagonal Newton
step, so a long hanging lead does not stretch), velocity damping, Coulomb friction, and collisions with obstacles
that may move. The ends are pinned to the clip and the lug, follow them, and leave along their axes.

Everything is in millimetres, z up from the bench top, the operator stands at -y; a frame is 1/15 s.

    lead = Cable(a, b, length=420)                 # a, b: where the lead leaves the clip and the lug
    lead.settle(a, b, a_dir, b_dir, obstacles)     # let it fall and come to rest
    lead.step(a, b, a_dir, b_dir, obstacles)       # once per frame; moving obstacles pass a new M each frame
    lead.polydata()                                # the tube to draw

Obstacles are ("plane", z0), ("box", M, lo, hi) and ("cyl", M, r, z0, z1), M a 4x4 world-from-local. clip_parts()
and lug_parts() are the hardware at the two ends in local coordinates; clip_matrix() places either, and lead_end()
gives the point and direction the lead leaves it at.

    python cables.py     # demo: three leads; writes /tmp/cables_demo.gif and /tmp/cables_sheet.png
"""
from __future__ import annotations

import math

import numpy as np
import pyvista as pv
from numba import njit
from scipy.spatial.transform import Rotation, Slerp

# ------------------------------------------------------------------------------------------ colours
GREEN = (0.10, 0.55, 0.25)
STEEL = (0.80, 0.81, 0.83)       # nickel-plated steel clip
STEEL_DK = (0.60, 0.62, 0.65)
TIN = (0.82, 0.80, 0.76)         # tinned copper lug
ZINC = (0.72, 0.73, 0.76)        # zinc-plated screw

# ------------------------------------------------------------------------------------------ physics
G = 9810.0                # mm/s^2
ITERS = 3                 # length + collision passes per substep
BEND_LEN = 50.0           # mm, elastogravity length (EI / weight per length)^(1/3): a supple 14 AWG lead
DAMP = 1.2                # 1/s, velocity damping
DAMP_SETTLE = 6.0
MU_S, MU_K = 0.7, 0.5     # PVC / silicone on a bench top
VMAX = 4000.0             # mm/s, clamp against impulses from fast obstacles
SKIN = 0.25               # mm kept clear beyond the radius, so the spline between nodes never dips into anything

# ------------------------------------------------------------------------------------------ hardware
CLIP_LEN = 45.0
CLIP_EXIT = np.array([44.5, 0.0, 0.0])     # the lead leaves the boot along +x (0.5 mm inside it, so no gap shows)
LUG_EXIT = np.array([17.5, 0.0, 2.3])      # ... and the lug's crimp barrel along +x
PIVOT_X = 20.0
OPEN_DEG = 14.0                            # each jaw at open_frac = 1: about 11 mm between the tips


# ===================================================================================== the solver
@njit(cache=True, fastmath=True)
def _push(px, py, pz, kind, prm, M, Mi, r):
    """World-space correction that moves a point out of an obstacle grown by r (zeros if it is clear)."""
    if kind == 0:
        d = prm[0] + r - pz
        if d > 0.0:
            return 0.0, 0.0, d
        return 0.0, 0.0, 0.0
    lx = Mi[0, 0] * px + Mi[0, 1] * py + Mi[0, 2] * pz + Mi[0, 3]
    ly = Mi[1, 0] * px + Mi[1, 1] * py + Mi[1, 2] * pz + Mi[1, 3]
    lz = Mi[2, 0] * px + Mi[2, 1] * py + Mi[2, 2] * pz + Mi[2, 3]
    cx = 0.0
    cy = 0.0
    cz = 0.0
    if kind == 1:                               # box: closest point, or out through the nearest face if inside
        ox = lx - min(max(lx, prm[0]), prm[3])
        oy = ly - min(max(ly, prm[1]), prm[4])
        oz = lz - min(max(lz, prm[2]), prm[5])
        d2 = ox * ox + oy * oy + oz * oz
        if d2 >= r * r:
            return 0.0, 0.0, 0.0
        if d2 > 1e-12:
            d = math.sqrt(d2)
            s = (r - d) / d
            cx, cy, cz = ox * s, oy * s, oz * s
        else:
            best = lx - prm[0]
            cx = -(best + r)
            t = prm[3] - lx
            if t < best:
                best = t
                cx, cy, cz = t + r, 0.0, 0.0
            t = ly - prm[1]
            if t < best:
                best = t
                cx, cy, cz = 0.0, -(t + r), 0.0
            t = prm[4] - ly
            if t < best:
                best = t
                cx, cy, cz = 0.0, t + r, 0.0
            t = lz - prm[2]
            if t < best and prm[6] == 0.0:       # not down through a bottom that stands on the bench
                best = t
                cx, cy, cz = 0.0, 0.0, -(t + r)
            t = prm[5] - lz
            if t < best:
                cx, cy, cz = 0.0, 0.0, t + r
    else:                                       # cylinder about local z, radius prm[0], prm[1] <= z <= prm[2]
        rad, z0, z1 = prm[0], prm[1], prm[2]
        rho = math.sqrt(lx * lx + ly * ly)
        ux, uy = 1.0, 0.0
        if rho > 1e-9:
            ux, uy = lx / rho, ly / rho
        orh = rho - min(rho, rad)
        oz = lz - min(max(lz, z0), z1)
        d2 = orh * orh + oz * oz
        if d2 >= r * r:
            return 0.0, 0.0, 0.0
        if d2 > 1e-12:
            d = math.sqrt(d2)
            s = (r - d) / d
            cx, cy, cz = ux * orh * s, uy * orh * s, oz * s
        else:
            pr, pb, pt = rad - rho, lz - z0, z1 - lz
            if prm[6] != 0.0:
                pb = 1e30
            if pr <= pb and pr <= pt:
                cx, cy = ux * (pr + r), uy * (pr + r)
            elif pb <= pt:
                cz = -(pb + r)
            else:
                cz = pt + r
    return (M[0, 0] * cx + M[0, 1] * cy + M[0, 2] * cz,
            M[1, 0] * cx + M[1, 1] * cy + M[1, 2] * cz,
            M[2, 0] * cx + M[2, 1] * cy + M[2, 2] * cz)


@njit(cache=True, fastmath=True)
def _lengths(p, w, rest, nv, dg, of, rh, cp, dp, lam):
    """Every segment back to its rest length at once: a Newton step on the chain's tridiagonal system
    (J W J^T) dl = -C, solved by the Thomas algorithm, so a long hanging lead does not stretch."""
    m = p.shape[0] - 1
    for j in range(m):
        dx, dy, dz = p[j + 1, 0] - p[j, 0], p[j + 1, 1] - p[j, 1], p[j + 1, 2] - p[j, 2]
        d = max(math.sqrt(dx * dx + dy * dy + dz * dz), 1e-9)
        nv[j, 0], nv[j, 1], nv[j, 2] = dx / d, dy / d, dz / d
        rh[j] = rest - d
        dg[j] = w[j] + w[j + 1] + 1e-5
        if w[j] + w[j + 1] == 0.0:          # both ends pinned: nothing to move
            dg[j], rh[j] = 1.0, 0.0
    for j in range(m - 1):
        of[j] = -w[j + 1] * (nv[j, 0] * nv[j + 1, 0] + nv[j, 1] * nv[j + 1, 1] + nv[j, 2] * nv[j + 1, 2])
    cp[0] = of[0] / dg[0] if m > 1 else 0.0
    dp[0] = rh[0] / dg[0]
    for j in range(1, m):
        den = dg[j] - of[j - 1] * cp[j - 1]
        cp[j] = of[j] / den if j < m - 1 else 0.0
        dp[j] = (rh[j] - of[j - 1] * dp[j - 1]) / den
    lam[m - 1] = dp[m - 1]
    for j in range(m - 2, -1, -1):
        lam[j] = dp[j] - cp[j] * lam[j + 1]
    for j in range(m):
        l = min(max(lam[j], -rest), rest)      # bounded, in case the ends are pulled apart past the length
        for k in range(3):
            p[j, k] -= w[j] * nv[j, k] * l
            p[j + 1, k] += w[j + 1] * nv[j, k] * l


@njit(cache=True, fastmath=True)
def _collide(p, w, kinds, prm, M, Mi, r, dn, cn, co):
    """Push the nodes, then the segment midpoints (so no segment cuts an edge or a corner), out of every obstacle
    whose bounding sphere comes near the lead's bounding box."""
    n = p.shape[0]
    lo0, lo1, lo2, hi0, hi1, hi2 = p[0, 0], p[0, 1], p[0, 2], p[0, 0], p[0, 1], p[0, 2]
    for i in range(n):
        lo0, lo1, lo2 = min(lo0, p[i, 0]), min(lo1, p[i, 1]), min(lo2, p[i, 2])
        hi0, hi1, hi2 = max(hi0, p[i, 0]), max(hi1, p[i, 1]), max(hi2, p[i, 2])
    for o in range(kinds.shape[0]):
        if prm[o, 10] >= 0.0:
            Mo = M[o]
            c0 = Mo[0, 0] * prm[o, 7] + Mo[0, 1] * prm[o, 8] + Mo[0, 2] * prm[o, 9] + Mo[0, 3]
            c1 = Mo[1, 0] * prm[o, 7] + Mo[1, 1] * prm[o, 8] + Mo[1, 2] * prm[o, 9] + Mo[1, 3]
            c2 = Mo[2, 0] * prm[o, 7] + Mo[2, 1] * prm[o, 8] + Mo[2, 2] * prm[o, 9] + Mo[2, 3]
            e0, e1, e2 = max(lo0 - c0, 0.0, c0 - hi0), max(lo1 - c1, 0.0, c1 - hi1), max(lo2 - c2, 0.0, c2 - hi2)
            if e0 * e0 + e1 * e1 + e2 * e2 > (prm[o, 10] + r + 1.0) ** 2:
                continue
        for i in range(n):
            if w[i] == 0.0:
                continue
            cx, cy, cz = _push(p[i, 0], p[i, 1], p[i, 2], kinds[o], prm[o], M[o], Mi[o], r)
            d = math.sqrt(cx * cx + cy * cy + cz * cz)
            if d > 0.0:
                p[i, 0] += cx
                p[i, 1] += cy
                p[i, 2] += cz
                dn[i] += d
                co[i] = o
                cn[i, 0], cn[i, 1], cn[i, 2] = cx / d, cy / d, cz / d
        for i in range(n - 1):
            wi, wj = w[i], w[i + 1]
            if wi + wj == 0.0:
                continue
            cx, cy, cz = _push(0.5 * (p[i, 0] + p[i + 1, 0]), 0.5 * (p[i, 1] + p[i + 1, 1]),
                               0.5 * (p[i, 2] + p[i + 1, 2]), kinds[o], prm[o], M[o], Mi[o], r)
            if cx != 0.0 or cy != 0.0 or cz != 0.0:
                W = 0.25 * (wi + wj)
                fi, fj = 0.5 * wi / W, 0.5 * wj / W
                p[i, 0] += fi * cx
                p[i, 1] += fi * cy
                p[i, 2] += fi * cz
                p[i + 1, 0] += fj * cx
                p[i + 1, 1] += fj * cy
                p[i + 1, 2] += fj * cz


@njit(cache=True, fastmath=True)
def _run(x, v, w, rest, F, P, K, KP, A, B, DA, DB, pin_a, pin_b, kinds, prm, mats, invs, h, iters, r, damp, mu_s,
         mu_k):
    """Advance the chain x (velocities v) through len(A) substeps of h. A, B: the ends per substep; DA, DB: the
    directions the lead leaves them along (used when pin_a / pin_b). F, P: free and pinned nodes; K, KP: the implicit
    bending step for the free ones. mats / invs: obstacle matrices per substep, index 0 being the previous frame's."""
    n = x.shape[0]
    p = x.copy()
    dn = np.zeros(n)                 # normal push this substep, for friction
    cn = np.zeros((n, 3))
    co = np.zeros(n, np.int64)
    ws = w.copy()                    # w with the nodes held by static friction pinned
    nv = np.zeros((n, 3))
    dg, of, rh, cp, dp, lam = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    rhs = np.zeros(n)
    for s in range(A.shape[0]):
        M = mats[s + 1]
        Mi = invs[s + 1]
        for i in range(n):
            if w[i] > 0.0:
                v[i, 2] -= G * h
                sp = math.sqrt(v[i, 0] ** 2 + v[i, 1] ** 2 + v[i, 2] ** 2)
                f = damp
                if sp * damp > VMAX:
                    f = VMAX / sp
                for k in range(3):
                    v[i, k] *= f
                    p[i, k] = x[i, k] + v[i, k] * h
        for k in range(3):
            p[0, k] = A[s, k]
            p[n - 1, k] = B[s, k]
            if pin_a:
                p[1, k] = A[s, k] + DA[s, k] * rest
            if pin_b:
                p[n - 2, k] = B[s, k] + DB[s, k] * rest
        for i in range(n):
            dn[i] = 0.0
            co[i] = -1
        # bending, implicitly: (I + beta L^T L) p = p_predicted for the free nodes, the pinned ones as boundary values
        for k in range(3):
            for a in range(F.shape[0]):
                acc = p[F[a], k]
                for b in range(P.shape[0]):
                    acc += KP[a, b] * p[P[b], k]
                rhs[a] = acc
            for a in range(F.shape[0]):
                acc = 0.0
                for b in range(F.shape[0]):
                    acc += K[a, b] * rhs[b]
                p[F[a], k] = acc
        for it in range(iters):
            _lengths(p, w, rest, nv, dg, of, rh, cp, dp, lam)
            _collide(p, w, kinds, prm, M, Mi, r, dn, cn, co)
        # Coulomb friction, relative to the surface the node touches (which may be moving); a node that sticks is
        # held for the final length pass
        for i in range(n):
            ws[i] = w[i]
            o = co[i]
            if w[i] == 0.0 or o < 0:
                continue
            ux = uy = uz = 0.0
            if kinds[o] != 0:
                Pi = invs[s, o]
                Pn = mats[s + 1, o]
                lx = Pi[0, 0] * x[i, 0] + Pi[0, 1] * x[i, 1] + Pi[0, 2] * x[i, 2] + Pi[0, 3]
                ly = Pi[1, 0] * x[i, 0] + Pi[1, 1] * x[i, 1] + Pi[1, 2] * x[i, 2] + Pi[1, 3]
                lz = Pi[2, 0] * x[i, 0] + Pi[2, 1] * x[i, 1] + Pi[2, 2] * x[i, 2] + Pi[2, 3]
                ux = Pn[0, 0] * lx + Pn[0, 1] * ly + Pn[0, 2] * lz + Pn[0, 3] - x[i, 0]
                uy = Pn[1, 0] * lx + Pn[1, 1] * ly + Pn[1, 2] * lz + Pn[1, 3] - x[i, 1]
                uz = Pn[2, 0] * lx + Pn[2, 1] * ly + Pn[2, 2] * lz + Pn[2, 3] - x[i, 2]
            rx, ry, rz = p[i, 0] - x[i, 0] - ux, p[i, 1] - x[i, 1] - uy, p[i, 2] - x[i, 2] - uz
            rn = rx * cn[i, 0] + ry * cn[i, 1] + rz * cn[i, 2]
            tx, ty, tz = rx - rn * cn[i, 0], ry - rn * cn[i, 1], rz - rn * cn[i, 2]
            t = math.sqrt(tx * tx + ty * ty + tz * tz)
            if t <= mu_s * dn[i]:
                f = 1.0
                ws[i] = 0.0
            else:
                f = min(1.0, mu_k * dn[i] / t)
            p[i, 0] -= f * tx
            p[i, 1] -= f * ty
            p[i, 2] -= f * tz
        _lengths(p, ws, rest, nv, dg, of, rh, cp, dp, lam)
        _collide(p, ws, kinds, prm, M, Mi, r, dn, cn, co)
        for i in range(n):
            for k in range(3):
                v[i, k] = (p[i, k] - x[i, k]) / h
                x[i, k] = p[i, k]


@njit(cache=True, fastmath=True)
def _depth(pts, kinds, prm, mats, invs, r):
    """Deepest a tube of radius r about the points goes into any obstacle."""
    worst = 0.0
    for o in range(kinds.shape[0]):
        for i in range(pts.shape[0]):
            cx, cy, cz = _push(pts[i, 0], pts[i, 1], pts[i, 2], kinds[o], prm[o], mats[o], invs[o], r)
            worst = max(worst, math.sqrt(cx * cx + cy * cy + cz * cz))
    return worst


@njit(cache=True, fastmath=True)
def _frames(c):
    """Parallel-transport normals along the polyline c."""
    m = c.shape[0]
    t = np.empty((m, 3))
    for i in range(m):
        a, b = max(i - 1, 0), min(i + 1, m - 1)
        d = c[b] - c[a]
        t[i] = d / max(math.sqrt((d * d).sum()), 1e-12)
    nrm = np.empty((m, 3))
    ref = np.array([0.0, 0.0, 1.0]) if abs(t[0, 2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = ref - (ref * t[0]).sum() * t[0]
    nrm[0] = u / math.sqrt((u * u).sum())
    for i in range(1, m):
        u = nrm[i - 1] - (nrm[i - 1] * t[i]).sum() * t[i]
        nrm[i] = u / max(math.sqrt((u * u).sum()), 1e-12)
    return t, nrm


# ------------------------------------------------------------------------------------- helpers
def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _pack(obstacles):
    """Obstacles as arrays for the solver. prm[6] flags a solid standing upright on a plane: a node found inside it
    is never pushed out through its bottom (into the bench), only through its top or sides."""
    planes = [o[1] for o in obstacles if o[0] == "plane"]
    kinds, prm, mats = [], [], []
    for o in obstacles:
        if o[0] == "plane":
            kinds.append(0), prm.append([o[1], 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]), mats.append(np.eye(4))
            continue
        M = np.asarray(o[1], float)
        zb = o[2][2] if o[0] == "box" else o[3]
        down = float(M[2, 2] > 0.999 and any(M[2, 3] + zb <= z0 + 0.5 for z0 in planes))
        if o[0] == "box":
            lo, hi = np.asarray(o[2], float), np.asarray(o[3], float)
            kinds.append(1), prm.append([*lo, *hi, down, *(lo + hi) / 2, np.linalg.norm(hi - lo) / 2])
        elif o[0] == "cyl":
            r, z0, z1 = o[2], o[3], o[4]
            kinds.append(2), prm.append([r, z0, z1, 0, 0, 0, down, 0, 0, (z0 + z1) / 2, math.hypot(r, (z1 - z0) / 2)])
        else:
            raise ValueError(f"unknown obstacle {o[0]!r}")
        mats.append(M)
    return (np.array(kinds, np.int64), np.array(prm, float).reshape(-1, 11),
            np.array(mats, float).reshape(-1, 4, 4))


def _rigid_inv(M):
    out = np.zeros_like(M)
    Rt = np.swapaxes(M[..., :3, :3], -1, -2)
    out[..., :3, :3] = Rt
    out[..., :3, 3] = -np.einsum("...ij,...j->...i", Rt, M[..., :3, 3])
    out[..., 3, 3] = 1.0
    return out


def _interp(M0, M1, ts):
    """Rigid transforms from M0 to M1 at fractions ts: the relative rotation turned through t of its angle about
    its axis (a slerp), the origin moved linearly."""
    out = np.repeat(M1[None], len(ts), 0)
    if np.array_equal(M0, M1):
        return out
    R0 = M0[:3, :3]
    Rr = M1[:3, :3] @ R0.T
    ang = math.acos(min(1.0, max(-1.0, (np.trace(Rr) - 1.0) / 2.0)))
    if ang > 1e-9:
        if ang > 3.0:                          # near a half turn the skew part loses the axis
            out[:, :3, :3] = Slerp([0.0, 1.0], Rotation.from_matrix([R0, M1[:3, :3]]))(ts).as_matrix()
        else:
            ax = np.array([Rr[2, 1] - Rr[1, 2], Rr[0, 2] - Rr[2, 0], Rr[1, 0] - Rr[0, 1]]) / (2 * math.sin(ang))
            Kx = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
            a = ang * ts[:, None, None]
            out[:, :3, :3] = (np.eye(3) + np.sin(a) * Kx + (1 - np.cos(a)) * (Kx @ Kx)) @ R0
    out[:, :3, 3] = M0[:3, 3] + (M1[:3, 3] - M0[:3, 3]) * ts[:, None]
    return out


def _dirs(d0, d1, ts):
    if d1 is None:
        return np.zeros((len(ts), 3))
    d1 = _unit(d1)
    if d0 is None:
        return np.repeat(d1[None], len(ts), 0)
    d = d0 + (d1 - d0) * ts[:, None]
    return d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-9)


def _catmull(P, k):
    """Uniform Catmull-Rom through the points P, k samples per segment (the segments are near equal length)."""
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    t = np.arange(k) / k
    t2, t3 = t * t, t * t * t
    p0, p1, p2, p3 = Q[:-3, None], Q[1:-2, None], Q[2:-1, None], Q[3:, None]
    c = 0.5 * (2 * p1 + (p2 - p0) * t[:, None] + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2[:, None]
               + (3 * p1 - p0 - 3 * p2 + p3) * t3[:, None])
    return np.vstack([c.reshape(-1, 3), P[-1:]])


_FACES: dict = {}


def _tube_faces(m, ns):
    """Triangles of a capped tube with m rings of ns points (plus a centre and a ring for each cap)."""
    key = (m, ns)
    if key not in _FACES:
        tris = []
        for j in range(m - 1):
            for i in range(ns):
                a, b = j * ns + i, j * ns + (i + 1) % ns
                tris += [(a, b, b + ns), (a, b + ns, a + ns)]      # wound outward, to match the normals
        base = m * ns
        for cap, (c, ring, flip) in enumerate([(base, base + 2, True), (base + 1, base + 2 + ns, False)]):
            for i in range(ns):
                a, b = ring + i, ring + (i + 1) % ns
                tris.append((c, b, a) if flip else (c, a, b))
        f = np.asarray(tris, np.int64)
        _FACES[key] = np.hstack([np.full((len(f), 1), 3), f]).ravel()
    return _FACES[key]


# ===================================================================================== the cable
class Cable:
    """A flexible lead from a to b, `length` long (longer than |a - b|, so it sags), radius `radius`."""

    def __init__(self, a, b, length, n=None, radius=1.6, seed=0):
        a, b = np.asarray(a, float), np.asarray(b, float)
        self.length, self.radius = float(length), float(radius)
        self.n = n = int(n) if n else max(8, int(round(self.length / 6.0)) + 1)
        self.rest = self.length / (n - 1)
        self.nodes = self._initial(a, b, seed)
        self.vel = np.zeros_like(self.nodes)
        self._ops: dict = {}
        self._a, self._b, self._da, self._db = a, b, None, None
        self._kinds = self._mats = None

    def _initial(self, a, b, seed):
        """A bowed curve from a to b about `length` long (the seed picks the bow), above the bench."""
        rng = np.random.default_rng(seed)
        t = np.linspace(0.0, 1.0, 4 * self.n)[:, None]
        ch = b - a
        hz = np.array([ch[0], ch[1], 0.0])
        side = np.cross([0.0, 0.0, 1.0], hz / np.linalg.norm(hz) if np.linalg.norm(hz) > 1e-6 else [1.0, 0.0, 0.0])
        c1, c2 = rng.choice([-1.0, 1.0]) * rng.uniform(0.7, 1.0), rng.uniform(-0.45, 0.45)
        shape = side * (c1 * np.sin(np.pi * t) + c2 * np.sin(2 * np.pi * t)) - [0, 0, 0.5] * np.sin(np.pi * t)

        def curve(amp):
            c = a + ch * t + amp * shape
            c[:, 2] = np.maximum(c[:, 2], self.radius)
            return c

        lo, hi = 0.0, 4.0 * self.length
        for _ in range(50):                    # the amplitude that makes it `length` long
            mid = 0.5 * (lo + hi)
            L = np.linalg.norm(np.diff(curve(mid), axis=0), axis=1).sum()
            lo, hi = (mid, hi) if L < self.length else (lo, mid)
        c = curve(lo)
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
        u = np.linspace(0.0, s[-1], self.n)
        return np.column_stack([np.interp(u, s, c[:, k]) for k in range(3)])

    def _weights(self, pin_a, pin_b):
        w = np.ones(self.n)
        w[[0, -1]] = 0.0
        if pin_a:
            w[1] = 0.0
        if pin_b:
            w[-2] = 0.0
        return w

    def _bending(self, w, h):
        """Backward-Euler bending for one substep h. The energy is EI / (2 s^3) |p[i-1] - 2 p[i] + p[i+1]|^2,
        so with node mass mu s the step is (I + beta L^T L) p = p_predicted, beta = g h^2 BEND_LEN^3 / s^4.
        Pinned nodes are boundary values (two at a clip: a clamped end). Cached per pin set and h."""
        key = (tuple(w == 0.0), round(h, 9))
        if key not in self._ops:
            n = self.n
            L = np.zeros((n - 2, n))
            for i in range(n - 2):
                L[i, i:i + 3] = (1.0, -2.0, 1.0)
            Q = G * h * h * BEND_LEN ** 3 / self.rest ** 4 * (L.T @ L)
            F, P = np.flatnonzero(w > 0.0), np.flatnonzero(w == 0.0)
            K = np.linalg.inv(np.eye(len(F)) + Q[np.ix_(F, F)])
            self._ops[key] = (F, P, np.ascontiguousarray(K), np.ascontiguousarray(-Q[np.ix_(F, P)]))
        return self._ops[key]

    def step(self, a, b, a_dir=None, b_dir=None, obstacles=(), dt=1 / 15, substeps=12, _damp=DAMP) -> None:
        """Move the ends to a and b (interpolated over the substeps) and advance the cable by dt. a_dir / b_dir:
        optional unit vectors along which the cable leaves each end (the clip's axis), so it doesn't kink there."""
        a, b = np.asarray(a, float), np.asarray(b, float)
        ts = np.arange(1, substeps + 1) / substeps
        A = self._a + (a - self._a) * ts[:, None]
        B = self._b + (b - self._b) * ts[:, None]
        DA, DB = _dirs(self._da, a_dir, ts), _dirs(self._db, b_dir, ts)
        kinds, prm, mats = _pack(obstacles)
        same = self._kinds is not None and np.array_equal(kinds, self._kinds)
        prev = self._mats if same else mats
        allm = np.empty((substeps + 1, len(kinds), 4, 4))
        allm[0] = prev
        for o in range(len(kinds)):
            allm[1:, o] = _interp(prev[o], mats[o], ts)
        h = dt / substeps
        w = self._weights(a_dir is not None, b_dir is not None)
        _run(self.nodes, self.vel, w, self.rest, *self._bending(w, h), A, B, DA, DB, a_dir is not None, b_dir is not None, kinds, prm, allm, _rigid_inv(allm), h, ITERS,
             self.radius + SKIN, math.exp(-_damp * h), MU_S, MU_K)
        self._a, self._b = a, b
        self._da = None if a_dir is None else _unit(a_dir)
        self._db = None if b_dir is None else _unit(b_dir)
        self._kinds, self._mats = kinds, mats

    def settle(self, a, b, a_dir=None, b_dir=None, obstacles=(), seconds=3.0) -> None:
        """Relax with the ends fixed (heavier damping), so the first frame starts at rest."""
        for _ in range(int(round(seconds * 15))):
            self.step(a, b, a_dir, b_dir, obstacles, _damp=DAMP_SETTLE)
        self.vel[:] = 0.0

    def curve(self, per_seg=3) -> np.ndarray:
        """The smooth centreline drawn: a Catmull-Rom spline through the nodes."""
        return _catmull(self.nodes, per_seg)

    def polydata(self, n_sides=12) -> pv.PolyData:
        """The lead as a capped tube about the spline through the nodes, with point normals."""
        c = self.curve()
        t, nrm = _frames(c)
        bi = np.cross(t, nrm)
        ang = 2 * np.pi * np.arange(n_sides) / n_sides
        ring = np.cos(ang)[None, :, None] * nrm[:, None] + np.sin(ang)[None, :, None] * bi[:, None]
        pts = (c[:, None] + self.radius * ring).reshape(-1, 3)
        caps = [c[:1], c[-1:], pts[:n_sides], pts[-n_sides:]]
        normals = np.vstack([ring.reshape(-1, 3), -t[:1], t[-1:], np.repeat(-t[:1], n_sides, 0),
                             np.repeat(t[-1:], n_sides, 0)])
        poly = pv.PolyData(np.vstack([pts] + caps), _tube_faces(len(c), n_sides))
        poly.point_data["Normals"] = normals
        poly.point_data.active_normals_name = "Normals"
        return poly

    def penetration(self, obstacles) -> float:
        """Deepest the drawn tube (radius about the spline) goes into any obstacle, mm."""
        kinds, prm, mats = _pack(obstacles)
        if not len(kinds):
            return 0.0
        return float(_depth(self.curve(4), kinds, prm, mats, _rigid_inv(mats), self.radius))

    def stretch(self) -> float:
        """Length along the nodes over the rest length, minus 1."""
        return float(np.linalg.norm(np.diff(self.nodes, axis=0), axis=1).sum() / self.length - 1.0)


# ===================================================================================== hardware
def _solid(rings, feature=40.0) -> pv.PolyData:
    """A closed loft: loops of points (same count) joined in order, capped at both ends, with split normals."""
    rings = [np.asarray(r, float) for r in rings]
    k, m = len(rings[0]), len(rings)
    pts = np.vstack(rings + [rings[0].mean(0)[None], rings[-1].mean(0)[None]])
    tris = []
    for j in range(m - 1):
        for i in range(k):
            a, b = j * k + i, j * k + (i + 1) % k
            tris += [(a, b, b + k), (a, b + k, a + k)]
    for i in range(k):
        tris += [(m * k, (i + 1) % k, i), (m * k + 1, (m - 1) * k + i, (m - 1) * k + (i + 1) % k)]
    f = np.asarray(tris, np.int64)
    poly = pv.PolyData(pts, np.hstack([np.full((len(f), 1), 3), f]).ravel())
    return poly.compute_normals(split_vertices=True, feature_angle=feature, auto_orient_normals=True)


def _box(x0, x1, y0, y1, z0, z1) -> pv.PolyData:
    return _solid([[(x, y0, z0), (x, y1, z0), (x, y1, z1), (x, y0, z1)] for x in (x0, x1)])


def _ring(r, k, axis="z", at=0.0, c=(0.0, 0.0)):
    """k points on a circle of radius r about an axis through c, at `at` along it."""
    a = 2 * np.pi * (np.arange(k) + 0.5) / k
    u, v = c[0] + r * np.cos(a), c[1] + r * np.sin(a)
    at = np.full(k, at)
    return {"z": np.column_stack([u, v, at]), "y": np.column_stack([u, at, v]), "x": np.column_stack([at, u, v])}[axis]


def _annulus(ri, ro, z0, z1, k=18) -> pv.PolyData:
    a = 2 * np.pi * np.arange(k) / k
    cs = np.column_stack([np.cos(a), np.sin(a)])
    rings = [np.column_stack([cs * r, np.full(k, z)]) for r, z in ((ro, z0), (ro, z1), (ri, z1), (ri, z0))]
    pts = np.vstack(rings)
    tris = []
    for j in range(4):
        jn = (j + 1) % 4
        for i in range(k):
            a0, b0 = j * k + i, j * k + (i + 1) % k
            a1, b1 = jn * k + i, jn * k + (i + 1) % k
            tris += [(a0, b0, b1), (a0, b1, a1)]
    f = np.asarray(tris, np.int64)
    poly = pv.PolyData(pts, np.hstack([np.full((len(f), 1), 3), f]).ravel())
    return poly.compute_normals(split_vertices=True, feature_angle=40.0, auto_orient_normals=True)


def _merge(polys) -> pv.PolyData:
    return pv.merge(polys, merge_points=False)


def _rot_y(poly, deg, about):
    m = np.eye(4)
    t = math.radians(deg)
    m[:3, :3] = [[math.cos(t), 0, math.sin(t)], [0, 1, 0], [-math.sin(t), 0, math.cos(t)]]
    p = np.asarray(about, float)
    m[:3, 3] = p - m[:3, :3] @ p
    return poly.transform(m, inplace=False)


def _lever(sign, open_frac):
    """One jaw and its handle (sign +1 upper, -1 lower), with its teeth and the ears around the pivot."""
    st = [(0.0, 1.5, 0.75, 1.9), (4.0, 2.0, 0.75, 2.1), (13.0, 3.0, 0.75, 2.6), (18.0, 3.4, 1.7, 3.6),
          (23.0, 3.4, 2.3, 4.2), (30.0, 3.0, 2.0, 3.8), (36.0, 2.6, 1.6, 3.2)]
    parts = [_solid([[(x, -hw, sign * zb), (x, hw, sign * zb), (x, hw, sign * zt), (x, -hw, sign * zt)]
                     for x, hw, zb, zt in st])]
    pitch = 2.4
    for k in range(5):                         # teeth, staggered half a pitch between the jaws
        x0 = 0.6 + pitch * k + (0.0 if sign > 0 else 1.2)
        hw = np.interp(x0 + pitch / 2, [s[0] for s in st], [s[1] for s in st]) - 0.1
        tri = [(x0, sign * 0.8), (x0 + pitch, sign * 0.8), (x0 + pitch / 2, -sign * 0.05)]
        parts.append(_solid([[(x, y, z) for x, z in tri] for y in (-hw, hw)]))
    yi, yo = (3.4, 3.85) if sign > 0 else (2.95, 3.4)
    z0, z1 = (-1.3, 2.4) if sign > 0 else (-2.4, 1.3)
    for s in (-1, 1):
        parts.append(_box(17.0, 23.0, *sorted((s * yi, s * yo)), z0, z1))
    jaw = _merge(parts)
    return _rot_y(jaw, sign * OPEN_DEG * open_frac, (PIVOT_X, 0.0, 0.0))


def clip_parts(open_frac: float = 0.0) -> list:
    """A ~45 mm insulated alligator clip in local coordinates: jaw tip at the origin, body along +x, jaws opening in
    the x-z plane, the lead leaving the boot at x = 45 along +x. open_frac 0..1 opens the jaws."""
    f = float(np.clip(open_frac, 0.0, 1.0))
    jaws = _merge([_lever(1, f), _lever(-1, f)])
    pivot = _merge([_solid([_ring(1.25, 10, "y", y, (PIVOT_X, 0.0)) for y in (-4.25, 4.25)]),
                    _solid([_ring(1.9, 12, "y", y, (PIVOT_X, 0.0)) for y in (-2.6, 2.6)])])
    st = [(21.0, 4.8, 5.5), (23.5, 5.0, 5.8), (29.0, 4.8, 5.4), (34.0, 4.2, 4.6), (38.5, 3.2, 3.4),
          (42.0, 2.4, 2.5), (45.0, 2.0, 2.0)]
    a = 2 * np.pi * (np.arange(16) + 0.5) / 16
    c, s = np.cos(a), np.sin(a)
    e = 2.0 / 2.6                              # a rounded-rectangle (superellipse) section
    sy, sz = np.sign(c) * np.abs(c) ** e, np.sign(s) * np.abs(s) ** e
    boot = _solid([np.column_stack([np.full(16, x), ry * sy, rz * sz]) for x, ry, rz in st], 50.0)
    return [("clip_jaws", jaws, STEEL), ("clip_pivot", pivot, STEEL_DK), ("clip_boot", boot, GREEN)]


def clip_matrix(p, axis, up) -> np.ndarray:
    """World-from-local placing a clip's jaw tip at p, its body along `axis`, its jaws opening toward `up`.
    It places a lug the same way (ring centre at p, barrel along `axis`, `up` the screw's axis)."""
    x = _unit(axis)
    z = np.asarray(up, float) - np.dot(up, x) * x
    z = _unit(z)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, np.cross(z, x), z, p
    return M


def lead_end(M, lug=False):
    """The point and direction a lead leaves a clip (or a lug) placed by M: the a / a_dir to pass to Cable.step."""
    q = LUG_EXIT if lug else CLIP_EXIT
    return (M @ np.append(q, 1.0))[:3], M[:3, 0].copy()


def lug_parts() -> list:
    """A tinned-copper ring lug (M4, for 14 AWG) under a washer and a hex screw head, local coordinates: ring centre
    at the origin lying on z = 0, the crimp barrel along +x, the lead leaving it at LUG_EXIT."""
    ring = _merge([_annulus(2.2, 4.6, 0.0, 0.8), _box(3.6, 9.5, -2.4, 2.4, 0.0, 0.8),
                   _solid([_ring(2.3, 14, "x", x, (0.0, 2.3)) for x in (8.5, 18.0)])])
    hexa = [_ring(r, 6, "z", z) for r, z in ((4.04, 1.4), (4.04, 3.8), (3.6, 4.25))]
    screw = _merge([_annulus(2.2, 4.5, 0.8, 1.4), _solid(hexa, 35.0)])
    return [("lug_ring", ring, TIN), ("lug_screw", screw, ZINC)]


# ===================================================================================== the demo
def _T(v):
    m = np.eye(4)
    m[:3, 3] = v
    return m


def _Ry(deg, pivot):
    m = np.eye(4)
    t = math.radians(deg)
    m[:3, :3] = [[math.cos(t), 0, math.sin(t)], [0, 1, 0], [-math.sin(t), 0, math.cos(t)]]
    m[:3, 3] = pivot - m[:3, :3] @ pivot
    return m


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


TRAY_C, TRAY = np.array([-120.0, 15.0]), (280.0, 220.0, 18.0)
STACK_C, STACK_R, STACK_H = np.array([170.0, 10.0]), 101.5, 160.0
CONT_C, CONT_R, CONT_H = np.array([-430.0, 60.0]), 65.0, 202.0
BAR = (-380.0, 230.0, 225.0, 245.0, 0.0, 6.0)


def _m_stack(t):
    a = 2 * np.pi * 2.0 * t                              # +-5 mm orbit at 2 Hz
    return _T([STACK_C[0] + 5 * math.cos(a), STACK_C[1] + 5 * math.sin(a), 0.0])


def _m_cont(t):
    u = _ease((t - 0.5) / 2.0) - _ease((t - 3.5) / 2.0)   # out over 2 s, hold 1 s, back over 2 s
    return _T([CONT_C[0] + 200 * u, CONT_C[1], 150 * u]) @ _Ry(130 * u, np.array([0.0, 0.0, CONT_H / 2]))


_M_TRAY = _T([*TRAY_C, 0.0])


def _obstacles(t):
    return [("plane", 0.0), ("box", _M_TRAY, (-TRAY[0] / 2, -TRAY[1] / 2, 0.0), (TRAY[0] / 2, TRAY[1] / 2, TRAY[2])),
            ("box", np.eye(4), BAR[0::2], BAR[1::2]),
            ("cyl", _m_stack(t), STACK_R, 0.0, STACK_H), ("cyl", _m_cont(t), CONT_R, 0.0, CONT_H)]


# clips in each part's local frame (part matrix, clip matrix); lugs on the bus bar, barrels toward the front
_RAD = np.array([math.cos(math.radians(20.0)), math.sin(math.radians(20.0)), 0.0])
_CLIPS = {
    "tray": (lambda t: _M_TRAY, clip_matrix([-80.0, TRAY[1] / 2, TRAY[2] - 6], [0, 0.9, 0.44], [0, 1, 0])),
    "pan": (_m_stack, clip_matrix(STACK_R * _RAD + [0, 0, 32.0], _RAD + [0, 0, -0.25], [0, 0, 1])),
    "cont": (_m_cont, clip_matrix([0.0, CONT_R, CONT_H - 7], [0, 0.6, 0.8], [0, 1, 0])),
}
_LUGS = {k: clip_matrix([x, 235.0, BAR[5]], [0, -1, 0], [0, 0, 1])
         for k, x in (("tray", -150.0), ("pan", 150.0), ("cont", -320.0))}
_LENGTHS = {"tray": 150.0, "pan": 300.0, "cont": 480.0}


def _ends(k, t):
    mpart, mloc = _CLIPS[k]
    Mc = mpart(t) @ mloc
    a, ad = lead_end(Mc)
    b, bd = lead_end(_LUGS[k], lug=True)
    return Mc, a, ad, b, bd


def _demo_leads():
    leads = {}
    for i, k in enumerate(_CLIPS):
        _, a, ad, b, bd = _ends(k, 0.0)
        leads[k] = Cable(a, b, _LENGTHS[k], seed=i)
        leads[k].settle(a, b, ad, bd, _obstacles(0.0), seconds=3.0)
    return leads


_XDISPLAY = None


def _wait_for_x(timeout=60.0):
    """Xvfb can still be starting when xvfb-run hands over (as in scene.py): wait until it takes a connection, and
    keep that connection open, since an X server resets when its last client leaves and VTK would connect mid-reset."""
    global _XDISPLAY
    import ctypes
    import os
    import time
    if not os.environ.get("DISPLAY") or _XDISPLAY:
        return
    x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
    x11.XOpenDisplay.restype = ctypes.c_void_p
    t0 = time.time()
    while time.time() - t0 < timeout:
        _XDISPLAY = x11.XOpenDisplay(None)
        if _XDISPLAY:
            return
        time.sleep(0.5)


def _demo():
    import time
    from PIL import Image, ImageDraw

    _wait_for_x()

    FPS, N = 15, 90
    clips, lugs = _CLIPS, _LUGS
    t0 = time.perf_counter()
    leads = _demo_leads()
    print(f"settled in {time.perf_counter() - t0:.1f} s (includes the JIT compile)")

    pl = pv.Plotter(off_screen=True, window_size=(960, 540), lighting="light kit")
    pl.set_background("white")
    pl.enable_anti_aliasing("ssaa")
    style = dict(smooth_shading=True, specular=0.35, specular_power=20, ambient=0.18, diffuse=0.85)
    pl.add_mesh(pv.Box((-650, 450, -330, 380, -20, 0)), color=(0.92, 0.91, 0.88), specular=0.05)
    pl.add_mesh(pv.Box((TRAY_C[0] - TRAY[0] / 2, TRAY_C[0] + TRAY[0] / 2, TRAY_C[1] - TRAY[1] / 2,
                        TRAY_C[1] + TRAY[1] / 2, 0, TRAY[2])), color=STEEL, **style)
    pl.add_mesh(pv.Box(BAR), color=(0.78, 0.50, 0.28), **style)
    a_stack = pl.add_mesh(pv.Cylinder(center=(0, 0, STACK_H / 2), direction=(0, 0, 1), radius=STACK_R,
                                      height=STACK_H, resolution=60),
                          color=STEEL_DK, **style)
    a_cont = pl.add_mesh(pv.Cylinder(center=(0, 0, CONT_H / 2), direction=(0, 0, 1), radius=CONT_R,
                                     height=CONT_H, resolution=60),
                         color=STEEL, **style)
    tube = {k: pl.add_mesh(c.polydata(), color=GREEN, **style) for k, c in leads.items()}
    clip_actors = {k: [pl.add_mesh(m, color=col, **style) for _, m, col in clip_parts(0.0)] for k in clips}
    for k, M in lugs.items():
        for _, m, col in lug_parts():
            pl.add_mesh(m, color=col, **style).user_matrix = M
    views = {"front": [(-110, -800, 700), (-110, 100, 60), (0, 0, 1)],
             "back": [(-80, 980, 680), (-80, 60, 60), (0, 0, 1)]}
    pl.camera.view_angle = 32.0

    frames, backs, worst, times, stretch = [], [], 0.0, [], 0.0
    for f in range(N):
        t = f / FPS
        obs = _obstacles(t)
        e = {k: _ends(k, t) for k in clips}
        t1 = time.perf_counter()
        for k, c in leads.items():
            _, a, ad, b, bd = e[k]
            c.step(a, b, ad, bd, obs)
        ms = 1000 * (time.perf_counter() - t1)
        times.append(ms)
        pen = max(c.penetration(obs) for c in leads.values())
        st = max(c.stretch() for c in leads.values())
        worst, stretch = max(worst, pen), max(stretch, st)
        print(f"frame {f:3d}  t {t:4.2f} s  step {ms:5.2f} ms (3 leads)  penetration {pen:5.3f} mm  "
              f"stretch {100 * st:5.2f} %")
        a_stack.user_matrix = _m_stack(t)
        a_cont.user_matrix = _m_cont(t)
        for k, c in leads.items():
            tube[k].GetMapper().SetInputData(c.polydata())
            for actor in clip_actors[k]:
                actor.user_matrix = e[k][0]
        for name, out in (("front", frames), ("back", backs)):
            if name == "back" and f % 6:
                continue
            pl.camera_position = views[name]
            pl.render()
            out.append(Image.fromarray(pl.screenshot(return_img=True)))
    pl.close()
    print(f"step time: mean {np.mean(times):.2f} ms, max {np.max(times):.2f} ms per frame for all three leads")
    print(f"max penetration {worst:.3f} mm, max stretch {100 * stretch:.2f} %")

    small = [im.resize((640, 360), Image.LANCZOS) for im in frames]
    small[0].save("/tmp/cables_demo.gif", save_all=True, append_images=small[1:], duration=1000 // FPS, loop=0)
    tw, th = 480, 270
    for path, ims in (("/tmp/cables_sheet.png", frames[::6]), ("/tmp/cables_sheet_back.png", backs)):
        sheet = Image.new("RGB", (5 * tw, 3 * th), "white")
        for j, im in enumerate(ims):
            f = 6 * j
            im = im.resize((tw, th), Image.LANCZOS)
            ImageDraw.Draw(im).text((8, 6), f"frame {f}  t = {f / FPS:.2f} s", fill=(0, 0, 0))
            sheet.paste(im, ((j % 5) * tw, (j // 5) * th))
        sheet.save(path)
    for f in (0, 30, 45, 75):
        frames[f].save(f"/tmp/cables_f{f:02d}.png")
    print("wrote /tmp/cables_demo.gif, /tmp/cables_sheet.png, /tmp/cables_sheet_back.png")


if __name__ == "__main__":
    _demo()
