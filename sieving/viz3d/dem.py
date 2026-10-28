"""Soft-sphere DEM for the sieving animation: the powder poured, scooped, sieved and tipped out by the moving CAD parts.

The powder is drawn as coarse-grained parcels: each sphere stands for a lump of real powder, sized by what it holds
(fine < 63 um, coarse 63-250 um, grit > 250 um), plus the unatomized pieces at their real size. Contacts are the usual
linear spring-dashpot normal force with a Cundall-Strack tangential spring capped by Coulomb friction (so a heap stands
still instead of creeping), no particle rotation (which stands in for rolling resistance: heaps stand at 30-35 deg,
about what Al powder does). Walls are analytic: thin revolved shells (a sieve frame, the pan, a jar, the funnel, the
container) given by a centre-line polyline in (r, z), and thin rectangles (the tray, the scoop, the tweezers), each
moving with its part. A sieve's cloth is a disc that a parcel of a size class that fits through it may cross, with a
probability per second of contact that the shaking raises: the mesh openings are far below the parcels' size, so the
macro view can't resolve them (zoom.py does, at real size).

Units: mm, g, s. Everything runs in Numba; one call of DEM.advance() is one animation frame.
"""
from __future__ import annotations

import math

import numpy as np
from numba import njit, prange

G = 9810.0                 # mm/s2
NB = 1 << 14               # hash-grid buckets
MASK = NB - 1
K_HIST = 16                # tangential springs kept per particle (particle contacts)
K_WALL = 6                 # and wall contacts


@njit(inline="always")
def _bucket(ix, iy, iz):
    return ((ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791)) & MASK


@njit(cache=True)
def _grid(x, small, h, cellc):
    n = x.shape[0]
    count = np.zeros(NB + 1, np.int64)
    key = np.full(n, -1, np.int64)
    for i in range(n):
        if small[i]:
            ix = int(math.floor(x[i, 0] / h))
            iy = int(math.floor(x[i, 1] / h))
            iz = int(math.floor(x[i, 2] / h))
            cellc[i, 0] = ix
            cellc[i, 1] = iy
            cellc[i, 2] = iz
            b = _bucket(ix, iy, iz)
            key[i] = b
            count[b + 1] += 1
    for b in range(NB):
        count[b + 1] += count[b]
    order = np.empty(count[NB], np.int64)
    fill = count.copy()
    for i in range(n):
        if key[i] >= 0:
            order[fill[key[i]]] = i
            fill[key[i]] += 1
    return count, order


@njit(inline="always", fastmath=True)
def _tangential(nx, ny, nz, tvx, tvy, tvz, fn, sx, sy, sz, kt, gt, mu, dt):
    """Cundall-Strack: rotate the old spring onto the tangent plane, stretch it by the tangential motion, cap at mu fn."""
    sn = sx * nx + sy * ny + sz * nz
    sx = sx - sn * nx + tvx * dt
    sy = sy - sn * ny + tvy * dt
    sz = sz - sn * nz + tvz * dt
    ftx = -kt * sx - gt * tvx
    fty = -kt * sy - gt * tvy
    ftz = -kt * sz - gt * tvz
    ftm = math.sqrt(ftx * ftx + fty * fty + ftz * ftz)
    lim = mu * fn
    if ftm > lim:
        s = lim / ftm if ftm > 1e-12 else 0.0
        ftx *= s
        fty *= s
        ftz *= s
        sx = -ftx / kt
        sy = -fty / kt
        sz = -ftz / kt
    return ftx, fty, ftz, sx, sy, sz


@njit(inline="always", fastmath=True)
def _pair(i, j, x, v, r, m, kn, kt, zeta, mu, hj, hs, hn, nj, ns, nn, dt):
    dx = x[i, 0] - x[j, 0]
    dy = x[i, 1] - x[j, 1]
    dz = x[i, 2] - x[j, 2]
    rs = r[i] + r[j]
    d2 = dx * dx + dy * dy + dz * dz
    if d2 >= rs * rs or d2 < 1e-14:
        return 0.0, 0.0, 0.0
    d = math.sqrt(d2)
    nx, ny, nz = dx / d, dy / d, dz / d
    meff = m[i] * m[j] / (m[i] + m[j])
    rvx = v[i, 0] - v[j, 0]
    rvy = v[i, 1] - v[j, 1]
    rvz = v[i, 2] - v[j, 2]
    vn = rvx * nx + rvy * ny + rvz * nz
    gn = 2.0 * zeta * math.sqrt(kn * meff)
    fn = kn * (rs - d) - gn * vn
    if fn < 0.0:
        fn = 0.0
    sx = sy = sz = 0.0
    for t in range(hn[i]):
        if hj[i, t] == j:
            sx, sy, sz = hs[i, t, 0], hs[i, t, 1], hs[i, t, 2]
            break
    ftx, fty, ftz, sx, sy, sz = _tangential(nx, ny, nz, rvx - vn * nx, rvy - vn * ny, rvz - vn * nz, fn,
                                            sx, sy, sz, kt, gn, mu, dt)
    k = nn[i]
    if k < nj.shape[1]:
        nj[i, k] = j
        ns[i, k, 0], ns[i, k, 1], ns[i, k, 2] = sx, sy, sz
        nn[i] = k + 1
    return fn * nx + ftx, fn * ny + fty, fn * nz + ftz


@njit(inline="always", fastmath=True)
def _wall(i, key, nx, ny, nz, delta, rvx, rvy, rvz, m, kn, kt, zeta, mu, wk, ws, wn, nwk, nws, nwn, dt):
    vn = rvx * nx + rvy * ny + rvz * nz
    gn = 2.0 * zeta * math.sqrt(kn * m)
    fn = kn * delta - gn * vn
    if fn < 0.0:
        fn = 0.0
    sx = sy = sz = 0.0
    for t in range(wn[i]):
        if wk[i, t] == key:
            sx, sy, sz = ws[i, t, 0], ws[i, t, 1], ws[i, t, 2]
            break
    ftx, fty, ftz, sx, sy, sz = _tangential(nx, ny, nz, rvx - vn * nx, rvy - vn * ny, rvz - vn * nz, fn,
                                            sx, sy, sz, kt, gn, mu, dt)
    k = nwn[i]
    if k < nwk.shape[1]:
        nwk[i, k] = key
        nws[i, k, 0], nws[i, k, 1], nws[i, k, 2] = sx, sy, sz
        nwn[i] = k + 1
    return fn * nx + ftx, fn * ny + fty, fn * nz + ftz


@njit(parallel=True, cache=True)
def _build(x, r, act, small, bigs, h, rmax_small, skin, count, order, cellc, nbr, nnbr, x0):
    """Verlet lists: every particle within contact distance plus `skin` of an active particle."""
    n = x.shape[0]
    K = nbr.shape[1]
    nbig = bigs.shape[0]
    for i in prange(n):
        nnbr[i] = 0
        x0[i, 0], x0[i, 1], x0[i, 2] = x[i, 0], x[i, 1], x[i, 2]
        if not act[i]:
            continue
        ri = r[i]
        reach = int(math.ceil((ri + rmax_small + skin) / h))
        ix = int(math.floor(x[i, 0] / h))
        iy = int(math.floor(x[i, 1] / h))
        iz = int(math.floor(x[i, 2] / h))
        k = 0
        for qx in range(ix - reach, ix + reach + 1):
            for qy in range(iy - reach, iy + reach + 1):
                for qz in range(iz - reach, iz + reach + 1):
                    b = _bucket(qx, qy, qz)
                    for t in range(count[b], count[b + 1]):
                        j = order[t]
                        if j == i or cellc[j, 0] != qx or cellc[j, 1] != qy or cellc[j, 2] != qz:
                            continue
                        dx, dy, dz = x[i, 0] - x[j, 0], x[i, 1] - x[j, 1], x[i, 2] - x[j, 2]
                        lim = ri + r[j] + skin
                        if dx * dx + dy * dy + dz * dz < lim * lim and k < K:
                            nbr[i, k] = j
                            k += 1
        for t in range(nbig):
            j = bigs[t]
            if j == i:
                continue
            dx, dy, dz = x[i, 0] - x[j, 0], x[i, 1] - x[j, 1], x[i, 2] - x[j, 2]
            lim = ri + r[j] + skin
            if dx * dx + dy * dy + dz * dz < lim * lim and k < K:
                nbr[i, k] = j
                k += 1
        nnbr[i] = k


@njit(parallel=True, fastmath=True, cache=True)
def _forces(x, v, r, m, cls, act, ghost, nbr, nnbr, kn, kt, zeta, mu,
            CM, CMi, CV, ctype, ce0, ce1, cT, cMu, cPass, cRate, cOn, cLo, cHi,
            sa, sb, pc, pu, pv, ph, hj, hs, hn, nj, ns, nn, wk, ws, wn, nwk, nws, nwn, dt, agit, F):
    n = x.shape[0]
    nc = ctype.shape[0]
    for i in prange(n):
        nn[i] = 0
        nwn[i] = 0
        F[i, 0] = 0.0
        F[i, 1] = 0.0
        F[i, 2] = 0.0
        if not act[i]:
            continue
        xi0, xi1, xi2 = x[i, 0], x[i, 1], x[i, 2]
        ri, mi = r[i], m[i]
        f0, f1, f2 = 0.0, 0.0, -mi * G
        for t in range(nnbr[i]):
            a0, a1, a2 = _pair(i, nbr[i, t], x, v, r, m, kn, kt, zeta, mu, hj, hs, hn, nj, ns, nn, dt)
            f0 += a0
            f1 += a1
            f2 += a2
        # walls
        for c in range(nc):
            if not cOn[c]:
                continue
            q0 = CMi[c, 0, 0] * xi0 + CMi[c, 0, 1] * xi1 + CMi[c, 0, 2] * xi2 + CMi[c, 0, 3]
            q1 = CMi[c, 1, 0] * xi0 + CMi[c, 1, 1] * xi1 + CMi[c, 1, 2] * xi2 + CMi[c, 1, 3]
            q2 = CMi[c, 2, 0] * xi0 + CMi[c, 2, 1] * xi1 + CMi[c, 2, 2] * xi2 + CMi[c, 2, 3]
            if ghost[i] == c:         # going through this cloth: free until it is clear of it, above or below
                zm = 0.5 * (cLo[c, 2] + cHi[c, 2])
                if q2 < zm - cT[c] - ri - 0.3 or q2 > zm + cT[c] + ri + 0.6:
                    ghost[i] = -1
                continue
            if (q0 < cLo[c, 0] - ri or q0 > cHi[c, 0] + ri or q1 < cLo[c, 1] - ri or q1 > cHi[c, 1] + ri
                    or q2 < cLo[c, 2] - ri or q2 > cHi[c, 2] + ri):
                continue
            tc = cT[c]
            for e in range(ce0[c], ce1[c]):
                if ctype[c] == 0:                     # revolved shell: segment in (r, z)
                    rr = math.sqrt(q0 * q0 + q1 * q1)
                    ax, az = sa[e, 0], sa[e, 1]
                    ex, ez = sb[e, 0] - ax, sb[e, 1] - az
                    L2 = ex * ex + ez * ez
                    tt = ((rr - ax) * ex + (q2 - az) * ez) / L2
                    tt = min(1.0, max(0.0, tt))
                    px, pz = ax + tt * ex, az + tt * ez
                    dr, dzz = rr - px, q2 - pz
                    dist = math.sqrt(dr * dr + dzz * dzz)
                    delta = tc + ri - dist
                    if delta <= 0.0:
                        continue
                    if dist > 1e-9:
                        nr, nzl = dr / dist, dzz / dist
                    else:
                        nr, nzl = -ez / math.sqrt(L2), ex / math.sqrt(L2)
                    if rr > 1e-9:
                        cx_, cy_ = q0 / rr, q1 / rr
                    else:
                        cx_, cy_ = 1.0, 0.0
                    l0, l1, l2 = nr * cx_, nr * cy_, nzl
                    p0, p1, p2 = px * cx_, px * cy_, pz
                else:                                 # thin rectangle
                    d0, d1, d2 = q0 - pc[e, 0], q1 - pc[e, 1], q2 - pc[e, 2]
                    a = d0 * pu[e, 0] + d1 * pu[e, 1] + d2 * pu[e, 2]
                    bb = d0 * pv[e, 0] + d1 * pv[e, 1] + d2 * pv[e, 2]
                    a = min(ph[e, 0], max(-ph[e, 0], a))
                    bb = min(ph[e, 1], max(-ph[e, 1], bb))
                    p0 = pc[e, 0] + a * pu[e, 0] + bb * pv[e, 0]
                    p1 = pc[e, 1] + a * pu[e, 1] + bb * pv[e, 1]
                    p2 = pc[e, 2] + a * pu[e, 2] + bb * pv[e, 2]
                    w0, w1, w2 = q0 - p0, q1 - p1, q2 - p2
                    dist = math.sqrt(w0 * w0 + w1 * w1 + w2 * w2)
                    delta = tc + ri - dist
                    if delta <= 0.0:
                        continue
                    if dist > 1e-9:
                        l0, l1, l2 = w0 / dist, w1 / dist, w2 / dist
                    else:
                        l0 = pu[e, 1] * pv[e, 2] - pu[e, 2] * pv[e, 1]
                        l1 = pu[e, 2] * pv[e, 0] - pu[e, 0] * pv[e, 2]
                        l2 = pu[e, 0] * pv[e, 1] - pu[e, 1] * pv[e, 0]
                if cPass[c] & (1 << cls[i]):
                    if np.random.random() < cRate[c] * agit * dt:
                        ghost[i] = c
                        break
                n0 = CM[c, 0, 0] * l0 + CM[c, 0, 1] * l1 + CM[c, 0, 2] * l2
                n1 = CM[c, 1, 0] * l0 + CM[c, 1, 1] * l1 + CM[c, 1, 2] * l2
                n2 = CM[c, 2, 0] * l0 + CM[c, 2, 1] * l1 + CM[c, 2, 2] * l2
                nl = math.sqrt(n0 * n0 + n1 * n1 + n2 * n2)
                n0, n1, n2 = n0 / nl, n1 / nl, n2 / nl
                vw0 = CV[c, 0, 0] * p0 + CV[c, 0, 1] * p1 + CV[c, 0, 2] * p2 + CV[c, 0, 3]
                vw1 = CV[c, 1, 0] * p0 + CV[c, 1, 1] * p1 + CV[c, 1, 2] * p2 + CV[c, 1, 3]
                vw2 = CV[c, 2, 0] * p0 + CV[c, 2, 1] * p1 + CV[c, 2, 2] * p2 + CV[c, 2, 3]
                a0, a1, a2 = _wall(i, c * 4096 + e, n0, n1, n2, delta, v[i, 0] - vw0, v[i, 1] - vw1, v[i, 2] - vw2,
                                   mi, kn, kt, zeta, cMu[c], wk, ws, wn, nwk, nws, nwn, dt)
                f0 += a0
                f1 += a1
                f2 += a2
        F[i, 0] = f0
        F[i, 1] = f1
        F[i, 2] = f2


@njit(parallel=True, fastmath=True, cache=True)
def _integrate(x, v, F, m, act, held, dt, drag, vmax, x0, disp):
    for i in prange(x.shape[0]):
        disp[i] = 0.0
        if not act[i]:
            continue
        if held[i]:
            for k in range(3):
                x[i, k] += v[i, k] * dt
            d0, d1, d2 = x[i, 0] - x0[i, 0], x[i, 1] - x0[i, 1], x[i, 2] - x0[i, 2]
            disp[i] = d0 * d0 + d1 * d1 + d2 * d2
            continue
        s = 0.0
        for k in range(3):
            v[i, k] = (v[i, k] + F[i, k] / m[i] * dt) * (1.0 - drag * dt)
            s += v[i, k] * v[i, k]
        if s > vmax * vmax:
            f = vmax / math.sqrt(s)
            for k in range(3):
                v[i, k] *= f
        for k in range(3):
            x[i, k] += v[i, k] * dt
        d0, d1, d2 = x[i, 0] - x0[i, 0], x[i, 1] - x0[i, 1], x[i, 2] - x0[i, 2]
        disp[i] = d0 * d0 + d1 * d1 + d2 * d2


@njit(cache=True)
def _inv3x4(M, out):
    a, b, c = M[0, 0], M[0, 1], M[0, 2]
    d, e, f = M[1, 0], M[1, 1], M[1, 2]
    g, h, k = M[2, 0], M[2, 1], M[2, 2]
    A, B, C = e * k - f * h, -(d * k - f * g), d * h - e * g
    det = a * A + b * B + c * C
    inv = np.empty((3, 3))
    inv[0, 0], inv[1, 0], inv[2, 0] = A / det, B / det, C / det
    inv[0, 1] = -(b * k - c * h) / det
    inv[1, 1] = (a * k - c * g) / det
    inv[2, 1] = -(a * h - b * g) / det
    inv[0, 2] = (b * f - c * e) / det
    inv[1, 2] = -(a * f - c * d) / det
    inv[2, 2] = (a * e - b * d) / det
    for i in range(3):
        for j in range(3):
            out[i, j] = inv[i, j]
        out[i, 3] = -(inv[i, 0] * M[0, 3] + inv[i, 1] * M[1, 3] + inv[i, 2] * M[2, 3])


@njit(cache=True)
def _run(nsub, dt, x, v, F, r, m, cls, act, held, ghost, small, bigs, cellc, h, rmax_small, skin, nbr, nnbr, x0,
         kn, kt, zeta, mu,
         M0, M1, ctype, ce0, ce1, cT, cMu, cPass, cRate, cOn, cLo, cHi, sa, sb, pc, pu, pv, ph,
         hj, hs, hn, nj, ns, nn, wk, ws, wn, nwk, nws, nwn, agit, drag, vmax):
    nc = M0.shape[0]
    CM = np.empty((nc, 3, 4))
    CMi = np.empty((nc, 3, 4))
    CV = np.empty((nc, 3, 4))
    T = nsub * dt
    disp = np.zeros(x.shape[0])
    rebuild = True
    for c in range(nc):
        for a in range(3):
            for b in range(4):
                CV[c, a, b] = (M1[c, a, b] - M0[c, a, b]) / T
    for s in range(nsub):
        u = (s + 1.0) / nsub
        for c in range(nc):
            for a in range(3):
                for b in range(4):
                    CM[c, a, b] = M0[c, a, b] + (M1[c, a, b] - M0[c, a, b]) * u
            _inv3x4(CM[c], CMi[c])
        if rebuild:
            count, order = _grid(x, small, h, cellc)
            _build(x, r, act, small, bigs, h, rmax_small, skin, count, order, cellc, nbr, nnbr, x0)
        _forces(x, v, r, m, cls, act, ghost, nbr, nnbr, kn, kt, zeta, mu,
                CM, CMi, CV, ctype, ce0, ce1, cT, cMu, cPass, cRate, cOn, cLo, cHi, sa, sb, pc, pu, pv, ph,
                hj, hs, hn, nj, ns, nn, wk, ws, wn, nwk, nws, nwn, dt, agit, F)
        _integrate(x, v, F, m, act, held, dt, drag, vmax, x0, disp)
        rebuild = disp.max() > 0.25 * skin * skin
        # the new contact lists become the old ones (swap the buffers, copy back once at the end if needed)
        hj, nj = nj, hj
        hs, ns = ns, hs
        hn, nn = nn, hn
        wk, nwk = nwk, wk
        ws, nws = nws, ws
        wn, nwn = nwn, wn
    if nsub % 2 == 1:
        nj[:, :] = hj
        ns[:, :, :] = hs
        nn[:] = hn
        nwk[:, :] = wk
        nws[:, :, :] = ws
        nwn[:] = wn


class Collider:
    """A wall that moves with a scene group. kind "lathe": a thin revolved shell, `elems` the centre line as (r, z)
    points about the local z axis; kind "plates": thin rectangles (centre, u axis, v axis, half u, half v). `base` is
    the 4x4 from those local coordinates to the part's model coordinates; `half` the half thickness. A cloth is a
    one-segment lathe that classes in `pass_mask` may cross at `rate` per second of contact (times the shaking)."""

    def __init__(self, name, group, kind, elems, half, base=None, mu=0.45, pass_mask=0, rate=0.0, on=True):
        self.name, self.group, self.kind, self.elems, self.half = name, group, kind, elems, half
        self.base = np.eye(4) if base is None else np.asarray(base, float)
        self.mu, self.pass_mask, self.rate, self.on = mu, pass_mask, rate, on


class DEM:
    def __init__(self, x, r, cls, rho=2.7e-3, kn=1.2e5, mu=0.45, zeta=0.30, drag=0.4, vmax=2500.0):
        self.x = np.ascontiguousarray(x, float)
        n = len(self.x)
        self.v = np.zeros((n, 3))
        self.F = np.zeros((n, 3))
        self.r = np.ascontiguousarray(r, float)
        self.m = rho * 4.0 / 3.0 * math.pi * self.r ** 3
        self.cls = np.ascontiguousarray(cls, np.int64)
        self.act = np.ones(n, np.bool_)
        self.held = np.zeros(n, np.bool_)
        self.ghost = np.full(n, -1, np.int64)
        rs = np.sort(np.unique(self.r))
        self.rmax_small = float(rs[rs <= 2.6].max()) if (rs <= 2.6).any() else float(rs.min())
        self.small = self.r <= self.rmax_small + 1e-9
        self.bigs = np.nonzero(~self.small)[0].astype(np.int64)
        self.h = 2.0 * self.rmax_small
        self.cellc = np.zeros((n, 3), np.int64)
        self.skin = 0.35
        self.nbr = np.zeros((n, 48), np.int64)
        self.nnbr = np.zeros(n, np.int64)
        self.x0 = self.x.copy()
        self.kn, self.kt, self.zeta, self.mu, self.drag, self.vmax = kn, kn * 2.0 / 7.0, zeta, mu, drag, vmax
        mmin = self.m.min() / 2.0
        self.dt = 0.18 * math.sqrt(mmin / kn)
        self.hj = np.zeros((n, K_HIST), np.int64)
        self.hs = np.zeros((n, K_HIST, 3))
        self.hn = np.zeros(n, np.int64)
        self.nj, self.ns, self.nn = self.hj.copy(), self.hs.copy(), self.hn.copy()
        self.wk = np.zeros((n, K_WALL), np.int64)
        self.ws = np.zeros((n, K_WALL, 3))
        self.wn = np.zeros(n, np.int64)
        self.nwk, self.nws, self.nwn = self.wk.copy(), self.ws.copy(), self.wn.copy()
        self.colliders: list[Collider] = []
        self.M_prev = None
        self.t = 0.0

    def add(self, c: Collider):
        self.colliders.append(c)
        return c

    def compile(self):
        cs = self.colliders
        nc = len(cs)
        self.ctype = np.array([0 if c.kind == "lathe" else 1 for c in cs], np.int64)
        self.ce0 = np.zeros(nc, np.int64)
        self.ce1 = np.zeros(nc, np.int64)
        sa, sb, pc, pu, pv, ph = [], [], [], [], [], []
        lo, hi = np.zeros((nc, 3)), np.zeros((nc, 3))
        for k, c in enumerate(cs):
            if c.kind == "lathe":
                pts = np.asarray(c.elems, float)
                self.ce0[k] = len(sa)
                for a, b in zip(pts[:-1], pts[1:]):
                    sa.append(a)
                    sb.append(b)
                self.ce1[k] = len(sa)
                rm = pts[:, 0].max() + c.half
                lo[k] = (-rm, -rm, pts[:, 1].min() - c.half)
                hi[k] = (rm, rm, pts[:, 1].max() + c.half)
            else:
                self.ce0[k] = len(pc)
                corners = []
                for cc, u, vv, hu, hv in c.elems:
                    cc, u, vv = (np.asarray(a_, float) for a_ in (cc, u, vv))
                    u, vv = u / np.linalg.norm(u), vv / np.linalg.norm(vv)
                    pc.append(cc)
                    pu.append(u)
                    pv.append(vv)
                    ph.append((hu, hv))
                    for su in (-1, 1):
                        for sv in (-1, 1):
                            corners.append(cc + su * hu * u + sv * hv * vv)
                self.ce1[k] = len(pc)
                corners = np.array(corners)
                lo[k] = corners.min(0) - c.half
                hi[k] = corners.max(0) + c.half
        z2 = lambda a, w: np.ascontiguousarray(np.array(a, float).reshape(-1, w)) if len(a) else np.zeros((1, w))
        self.sa, self.sb = z2(sa, 2), z2(sb, 2)
        self.pc, self.pu, self.pv, self.ph = z2(pc, 3), z2(pu, 3), z2(pv, 3), z2(ph, 2)
        self.cLo, self.cHi = lo, hi
        self.cT = np.array([c.half for c in cs], float)
        self.cMu = np.array([c.mu for c in cs], float)
        self.cPass = np.array([c.pass_mask for c in cs], np.int64)
        self.cRate = np.array([c.rate for c in cs], float)
        self.index = {c.name: k for k, c in enumerate(cs)}

    def matrices(self, world: dict) -> np.ndarray:
        """3x4 world-from-local matrices of every collider, from the scene's group matrices."""
        out = np.empty((len(self.colliders), 3, 4))
        for k, c in enumerate(self.colliders):
            out[k] = (world.get(c.group, np.eye(4)) @ c.base)[:3]
        return out

    def advance(self, seconds: float, world: dict, agitation: float = 0.0):
        """Advance by `seconds` of simulated time while every collider moves from its last pose to `world`'s."""
        M1 = self.matrices(world)
        if self.M_prev is None:
            self.M_prev = M1.copy()
        on = np.array([c.on for c in self.colliders], np.bool_)
        if seconds > 0 and self.act.any():
            nsub = max(1, int(math.ceil(seconds / self.dt)))
            _run(nsub, seconds / nsub, self.x, self.v, self.F, self.r, self.m, self.cls, self.act, self.held,
                 self.ghost, self.small, self.bigs, self.cellc, self.h, self.rmax_small, self.skin, self.nbr,
                 self.nnbr, self.x0, self.kn, self.kt, self.zeta,
                 self.mu, self.M_prev, M1, self.ctype, self.ce0, self.ce1, self.cT, self.cMu, self.cPass, self.cRate,
                 on, self.cLo, self.cHi, self.sa, self.sb, self.pc, self.pu, self.pv, self.ph, self.hj, self.hs,
                 self.hn, self.nj, self.ns, self.nn, self.wk, self.ws, self.wn, self.nwk, self.nws, self.nwn,
                 float(agitation), self.drag, self.vmax)
            self.t += seconds
        self.M_prev = M1

    def speed(self) -> np.ndarray:
        return np.linalg.norm(self.v, axis=1)
