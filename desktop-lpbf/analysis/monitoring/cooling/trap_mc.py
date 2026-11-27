"""1070 nm transmission of a chevron light trap: 2-D Monte Carlo ray trace with weighted rays (monitoring/cooling.md §5).

The trap is a stack of bent sheet blades, periodic across the stack (pitch p) and D deep along the flow. Each blade is a
zigzag through (u, v) = (0, 0), (D/n, A), (2D/n, 0), ... (D, 0 or A): n straight legs of lateral amplitude A. Light enters at
u = 0 (the guard's side) and is counted when it leaves at u = D (the outside); light that comes back out at u = 0 is lost to
the guard. Every surface reflects a fraction rho of what hits it: a fraction s of that specularly, the rest diffusely.

Long blades (the trap is many pitches wide along the blades) make this a 2-D problem: a ray's out-of-plane component only
moves it along the blades, so its in-plane path and its number of bounces are those of its projection. A 3-D Lambertian
surface seen in such a section scatters with p(theta) = cos(theta)/2 about the normal (theta in -90..90 deg), which is what
the diffuse step samples. The trap's end walls (not modelled) only add bounces.

Weighted rays: a ray is never absorbed at random; its weight is multiplied by rho at each hit, and the weight it carries out
at u = D is its contribution to the transmission. Rays are dropped when their weight falls below W_MIN (they can then add at
most W_MIN each, which bounds the error from below and is reported).
"""
from __future__ import annotations

import math

import numpy as np

W_MIN = 1e-18


def blade_segments(D, A, n, p, kmin, kmax):
    """the legs of blades k = kmin..kmax as arrays of (u0, v0, u1, v1)"""
    segs = []
    for k in range(kmin, kmax + 1):
        for j in range(n):
            u0, u1 = j * D / n, (j + 1) * D / n
            v0 = A if j % 2 else 0.0
            v1 = 0.0 if j % 2 else A
            segs.append((u0, v0 + k * p, u1, v1 + k * p))
    return np.array(segs, float)


def trace(D, A, n, p, rho, spec_frac=0.0, n_rays=200_000, source="collimated", theta_deg=0.0, seed=1, max_hits=400):
    """transmission (fraction of the power entering the trap's face that leaves its far face), and diagnostics

    source: "collimated" (all rays at theta_deg from the trap's axis, in the section's plane) or "diffuse" (Lambertian over
    the entrance face).
    """
    rng = np.random.default_rng(seed)
    kspan = int(math.ceil(A / p)) + 2
    S = blade_segments(D, A, n, p, -kspan, kspan)
    su0, sv0, su1, sv1 = S.T
    du, dv = su1 - su0, sv1 - sv0
    L = np.hypot(du, dv)
    # unit normals of each leg (either side; flipped toward the incoming ray at a hit)
    nu, nv = -dv / L, du / L
    N = n_rays
    u = np.zeros(N)
    v = rng.uniform(0.0, p, N)
    if source == "collimated":
        th = np.full(N, math.radians(theta_deg))
    else:
        th = np.arcsin(rng.uniform(-1.0, 1.0, N))          # p(theta) = cos(theta)/2 into the face
    ru, rv = np.cos(th), np.sin(th)
    w = np.ones(N)
    alive = np.ones(N, bool)
    T = 0.0
    R_back = 0.0
    hits_hist = np.zeros(max_hits + 1)
    nh = np.zeros(N, int)
    dropped = 0.0
    eps = 1e-9
    for it in range(max_hits):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        uu, vv, au, av = u[idx], v[idx], ru[idx], rv[idx]
        # fold v into the base period; the segment set covers neighbouring blades
        shift = np.floor(vv / p) * p
        vl = vv - shift
        # ray-segment intersections: uu + t*au = su0 + s*du ; vl + t*av = sv0 + s*dv
        den = au[:, None] * dv[None, :] - av[:, None] * du[None, :]
        with np.errstate(divide="ignore", invalid="ignore"):
            wu = su0[None, :] - uu[:, None]
            wv = sv0[None, :] - vl[:, None]
            t = (wu * dv[None, :] - wv * du[None, :]) / den
            s = (wu * av[:, None] - wv * au[:, None]) / den
        ok = (np.abs(den) > 1e-12) & (t > eps) & (s >= 0.0) & (s <= 1.0)
        t = np.where(ok, t, np.inf)
        j = np.argmin(t, axis=1)
        tmin = t[np.arange(idx.size), j]
        # exits through the faces u = 0 or u = D before any hit
        with np.errstate(divide="ignore", invalid="ignore"):
            t_out = np.where(au > 0, (D - uu) / au, np.where(au < 0, -uu / au, np.inf))
        exit_ = t_out < tmin
        ex_idx = idx[exit_]
        fwd = au[exit_] > 0
        T += w[ex_idx[fwd]].sum()
        R_back += w[ex_idx[~fwd]].sum()
        hits_hist[np.minimum(nh[ex_idx[fwd]], max_hits)] += w[ex_idx[fwd]]
        alive[ex_idx] = False
        hit = ~exit_
        hi = idx[hit]
        if hi.size == 0:
            continue
        jj = j[hit]
        tt = tmin[hit]
        u[hi] = uu[hit] + tt * au[hit]
        v[hi] = vv[hit] + tt * av[hit]
        # normal toward the incoming side
        n_u, n_v = nu[jj], nv[jj]
        flip = (n_u * au[hit] + n_v * av[hit]) > 0
        n_u = np.where(flip, -n_u, n_u)
        n_v = np.where(flip, -n_v, n_v)
        w[hi] *= rho
        nh[hi] += 1
        spec = rng.uniform(size=hi.size) < spec_frac
        # specular: r - 2 (r.n) n
        dot = au[hit] * n_u + av[hit] * n_v
        su_, sv_ = au[hit] - 2 * dot * n_u, av[hit] - 2 * dot * n_v
        # diffuse: angle from the normal with p = cos/2
        a = np.arcsin(rng.uniform(-1.0, 1.0, hi.size))
        tu, tv = -n_v, n_u                                   # tangent
        du_ = np.cos(a) * n_u + np.sin(a) * tu
        dv_ = np.cos(a) * n_v + np.sin(a) * tv
        ru[hi] = np.where(spec, su_, du_)
        rv[hi] = np.where(spec, sv_, dv_)
        # nudge off the surface
        u[hi] += 1e-7 * ru[hi]
        v[hi] += 1e-7 * rv[hi]
        small = w[hi] < W_MIN
        dropped += small.sum() * W_MIN
        alive[hi[small]] = False
    left = alive.sum()
    trans = T / N
    return dict(T=trans, OD=(-math.log10(trans) if trans > 0 else float("inf")), back=R_back / N, dropped_bound=dropped / N,
                unfinished=int(left), n_rays=N,
                min_hits_through=int(np.argmax(hits_hist > 0)) if T > 0 else None)


def porosity(D, A, n, p, t):
    """open fraction of the face, measured across the legs (gap normal to a leg / pitch)"""
    phi = math.atan2(A, D / n)
    gap = p * math.cos(phi) - t
    return max(gap, 0.0) / p, gap, math.degrees(phi)


if __name__ == "__main__":
    import time
    t0 = time.time()
    for rho in (0.05, 0.2):
        r = trace(30.0, 12.0, 4, 10.0, rho, 0.0, 100_000, "diffuse")
        print(rho, r, round(time.time() - t0, 1))
