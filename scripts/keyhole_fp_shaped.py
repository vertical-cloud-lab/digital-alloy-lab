"""Keyhole shape from the physics: a tilted keyhole from a point-by-point wall energy balance (PR #249).

Part of the first-principles keyhole model's second version (scripts/keyhole_first_principles_v2.py). The first
version fixed the keyhole's shape (a straight cone, or a paraboloid) and found only its depth. Here the shape
comes out of the physics, following Kaplan's (1994) point-by-point balance, with the multiple reflections
ray-traced:

* The keyhole is a stack of circular cross-sections. At depth z its centre is at xc(z) (the beam is at x = 0 and
  moves in +x) and its radius is r(z). The front wall is xf = xc + r and the rear wall xr = xc - r, both piecewise
  linear on a fixed grid in z. The opening at the surface is fixed, as in the first version.
* A Monte Carlo ray tracer (numba) sends the Gaussian beam in, absorbs the unpolarised Fresnel share at every
  hit, and records where the power is absorbed: by depth, by azimuth around the wall, and whether it was the
  beam's first hit (direct) or a reflection.
* The wall loses heat by conduction. Its total, and how it varies with depth, comes from the 3D moving point
  sources of the first version, now placed on the tilted axis. How it splits between the front and the rear
  follows Kaplan 1994, Eq. 10: q(phi) is proportional to cos(phi) + K1(Pe' r)/K0(Pe' r), with Pe' = v / (2 kappa).
* Each wall's local slope is set so that, at each depth, the power it absorbs (direct plus reflected) equals the
  power it loses. A wall absorbs the direct beam in proportion to tan(theta), where theta is its angle from the
  vertical (Kaplan 1994; Fabbro & Chouf 2000: tan(theta) = v / v_drill at high Peclet number). The slopes are
  iterated with the ray tracing until the depth settles. The keyhole ends where the front and rear walls meet.

Lengths inside the ray tracer are in units of the beam's 1/e^2 radius r0.
"""

from __future__ import annotations

import math

import numba as nb
import numpy as np
from scipy import optimize, special


@nb.njit(cache=True)
def fresnel_A(Nr, Ni, cos_i):
    """Unpolarised Fresnel absorptance of a metal with complex index Nr + i Ni at incidence cos_i."""
    N = complex(Nr, Ni)
    c = min(max(cos_i, 0.0), 1.0)
    s = np.sqrt(N * N - (1.0 - c * c))
    rs = (c - s) / (c + s)
    rp = (N * N * c - s) / (N * N * c + s)
    return 1.0 - 0.5 * (abs(rs) ** 2 + abs(rp) ** 2)


@nb.njit(cache=True)
def trace_shaped(zn, xcn, rn, Nr, Ni, n_rays, seed, nphi, max_bounces, w_min):
    """Gaussian beam (1/e^2 radius 1, vertical, centred on x = y = 0) into a keyhole of circular cross-sections.

    zn: node depths (zn[0] = 0 at the surface, zn[-1] = d); xcn, rn: centre and radius at the nodes, linear
    between them (rn[-1] = 0 closes the tip). Light that misses the opening meets the flat liquid at normal
    incidence. Returns (Qd, Qr, surf, out, hits): power absorbed per segment and azimuth bin on the beam's first
    hit (Qd) and after reflections (Qr), as fractions of the beam; the fraction absorbed on the flat surface
    outside the opening; the fraction reflected back out; and the mean wall hits per entering ray. Azimuth bins
    run over |phi| in [0, pi], phi = 0 at the front wall (+x).
    """
    nseg = zn.size - 1
    Qd = np.zeros((nseg, nphi))
    Qr = np.zeros((nseg, nphi))
    np.random.seed(seed)
    A_flat = fresnel_A(Nr, Ni, 1.0)
    surf = 0.0
    out = 0.0
    w0 = 1.0 / n_rays
    n_hits = 0
    n_in = 0
    for _k in range(n_rays):
        u = np.random.random()
        rr = math.sqrt(-math.log(1.0 - u) / 2.0)
        th = 2.0 * math.pi * np.random.random()
        px = rr * math.cos(th)
        py = rr * math.sin(th)
        pz = 0.0
        if (px - xcn[0]) ** 2 + py * py >= rn[0] ** 2:
            surf += w0 * A_flat
            out += w0 * (1.0 - A_flat)
            continue
        n_in += 1
        ux, uy, uz = 0.0, 0.0, 1.0
        w = w0
        nb_ = 0
        jcur = 0
        while nb_ < max_bounces and w > w_min:
            # Segments are searched in the ray's z direction from its current one: z is monotonic along a
            # straight ray, so the first segment with a valid crossing holds the nearest one.
            tbest = 1e300
            jbest = -1
            step = 1 if uz >= 0 else -1
            j = jcur
            while 0 <= j < nseg:
                z0 = zn[j]
                z1 = zn[j + 1]
                dz = z1 - z0
                b = (xcn[j + 1] - xcn[j]) / dz
                e = (rn[j + 1] - rn[j]) / dz
                X0 = px - xcn[j] - b * (pz - z0)
                X1 = ux - b * uz
                R0 = rn[j] + e * (pz - z0)
                R1 = e * uz
                a = X1 * X1 + uy * uy - R1 * R1
                bb = 2.0 * (X0 * X1 + py * uy - R0 * R1)
                c = X0 * X0 + py * py - R0 * R0
                t1 = -1.0
                t2 = -1.0
                if abs(a) < 1e-14:
                    if abs(bb) > 1e-300:
                        t1 = -c / bb
                else:
                    disc = bb * bb - 4.0 * a * c
                    if disc >= 0.0:
                        sq = math.sqrt(disc)
                        t1 = (-bb - sq) / (2.0 * a)
                        t2 = (-bb + sq) / (2.0 * a)
                for t in (t1, t2):
                    if t > 1e-9 and t < tbest:
                        zt = pz + t * uz
                        if zt >= z0 - 1e-12 and zt <= z1 + 1e-12 and R0 + t * R1 >= -1e-12:
                            tbest = t
                            jbest = j
                if jbest >= 0:
                    break
                j += step
            if uz < 0.0:
                t_exit = -pz / uz
                if t_exit < tbest:
                    out += w
                    w = 0.0
                    break
            if jbest < 0:
                out += w
                w = 0.0
                break
            j = jbest
            z0 = zn[j]
            dz = zn[j + 1] - z0
            b = (xcn[j + 1] - xcn[j]) / dz
            e = (rn[j + 1] - rn[j]) / dz
            px += tbest * ux
            py += tbest * uy
            pz += tbest * uz
            xrel = px - (xcn[j] + b * (pz - z0))
            R = rn[j] + e * (pz - z0)
            nx = xrel
            ny = py
            nz = -xrel * b - R * e
            nn = math.sqrt(nx * nx + ny * ny + nz * nz)
            if nn < 1e-300:
                out += w
                w = 0.0
                break
            nx /= nn
            ny /= nn
            nz /= nn
            cos_i = ux * nx + uy * ny + uz * nz
            A = fresnel_A(Nr, Ni, abs(cos_i))
            phi = math.atan2(abs(py), xrel)
            kb = min(int(phi / math.pi * nphi), nphi - 1)
            if nb_ == 0:
                Qd[j, kb] += w * A
            else:
                Qr[j, kb] += w * A
            w *= 1.0 - A
            ux -= 2.0 * cos_i * nx
            uy -= 2.0 * cos_i * ny
            uz -= 2.0 * cos_i * nz
            px -= 1e-9 * nx
            py -= 1e-9 * ny
            pz -= 1e-9 * nz
            if pz < 0.0:
                pz = 0.0
            jcur = j
            nb_ += 1
            n_hits += 1
        if w > 0.0:
            out += w  # cut off after max_bounces or below w_min: counted as escaping (it is < w_min each)
    return Qd, Qr, surf, out, n_hits / max(n_in, 1)


def kaplan_ratio(r, v, kappa):
    """K1/K0 at Pe' r, Pe' = v / (2 kappa) (Kaplan 1994, Eq. 10)."""
    pe = max(v * r / (2 * kappa), 1e-6)
    return float(special.k1(pe) / special.k0(pe))


def kaplan_loss_per_depth(r, k, kappa, dT, v):
    """Kaplan 1994: heat lost per unit depth from a cylinder of radius r at dT above ambient, moving at v."""
    pe = max(v * r / (2 * kappa), 1e-9)
    return 2 * math.pi * k * dT * pe * special.k1(pe) / special.k0(pe)


def front_fraction(r, v, kappa):
    """Share of a circle's conduction loss that leaves through its front half: integral of cos(phi) + K over
    |phi| < pi/2, over the integral over the whole circle (2 pi K)."""
    K = kaplan_ratio(r, v, kappa)
    return 0.5 + 1.0 / (math.pi * K)


def walls_to_nodes(z, xf, xr):
    """Truncate the walls where they meet and return (zn, xcn, rn) for trace_shaped (rn[-1] = 0)."""
    gap = xf - xr
    if np.all(gap > 0):
        d = z[-1]
        zn, xfn, xrn = z.copy(), xf.copy(), xr.copy()
        xm = 0.5 * (xfn[-1] + xrn[-1])
        xfn[-1] = xrn[-1] = xm
        return zn, 0.5 * (xfn + xrn), 0.5 * (xfn - xrn), d
    i = int(np.argmax(gap <= 0))
    # linear interpolation of where the gap closes, between nodes i-1 and i
    g0, g1 = gap[i - 1], gap[i]
    f = g0 / (g0 - g1)
    d = z[i - 1] + f * (z[i] - z[i - 1])
    xm = xf[i - 1] + f * (xf[i] - xf[i - 1])
    zn = np.append(z[:i], d)
    xcn = np.append(0.5 * (xf[:i] + xr[:i]), xm)
    rn = np.append(0.5 * (xf[:i] - xr[:i]), 0.0)
    return zn, xcn, rn, d


# --- the shape iteration ---------------------------------------------------------------------------------

N_SRC = 24
N_AZ = 16
NPHI = 4  # azimuth bins over |phi| in [0, pi]: two front (|phi| < pi/2), two rear


def tilted_conduction(zn, xcn, rn, th, v, wings, point_source_field, n_src=N_SRC, n_az=N_AZ, theta_w_fn=None):
    """Point sources on the keyhole's (tilted) axis whose strengths hold each wall circle's mean temperature at
    T_w (non-negative least squares), as in the first version but with the axis at xc(z). Lengths in metres.
    theta_w_fn(r), if given, is the wall's temperature rise at a cross-section of radius r (its Laplace pressure
    sigma / r raises the boiling point); otherwise the wall is at th.theta_w everywhere."""
    d = zn[-1]
    j = np.arange(n_src)
    zs = d * (j + 0.5) / n_src
    xs = np.interp(zs, zn, xcn)
    ac = np.interp(zs, zn, rn)
    phi = np.arange(n_az) * 2 * math.pi / n_az
    X = xs[:, None] + ac[:, None] * np.cos(phi)[None, :]
    Y = ac[:, None] * np.sin(phi)[None, :]
    Z = np.repeat(zs[:, None], n_az, axis=1)
    G = np.zeros((n_src, n_src))
    for jj in range(n_src):
        G[:, jj] = point_source_field(X, Y, Z, np.array([zs[jj]]), np.array([1.0]), th.k, th.kappa, v,
                                      src_x=np.array([xs[jj]]), src_y=np.array([0.0])).mean(axis=1)
    target = np.full(n_src, th.theta_w) if theta_w_fn is None else np.array([theta_w_fn(r) for r in ac])
    wx, wy, wq = wings
    if wq.size:
        target = target - point_source_field(X, Y, Z, np.zeros_like(wq), wq, th.k, th.kappa, v,
                                             src_x=wx, src_y=wy, surface=True).mean(axis=1)
    target = np.maximum(target, 0.0)
    q, _ = optimize.nnls(G, target, maxiter=4000)
    return zs, xs, q


def _smooth(a, n=1):
    a = np.asarray(a, dtype=float)
    for _ in range(n):
        b = a.copy()
        b[1:-1] = 0.25 * a[:-2] + 0.5 * a[1:-1] + 0.25 * a[2:]
        a = b
    return a


def solve_shaped(P, v, r0, a0, N, th, Q_evap_fn, wing_sources, point_source_field, A_override=None, d_init=None,
                 n_seg=40, n_rays=20000, seed=11, max_iter=40, tol=0.005, relax=0.5, log=None, shape_init=None,
                 theta_w_fn=None):
    """Free-form keyhole: the depth from the global energy balance and the shape from Kaplan's point-by-point one.

    The walls are defined on s = z/d in n_seg segments by their slopes, tan(theta_f) and tan(theta_r) (front wall
    leaning back, rear wall leaning forward), scaled so that the walls meet at depth d. Each iteration:
    1. ray-traces the current keyhole;
    2. moves d towards the root of (absorbed in the keyhole) - (conducted + evaporated), by secant steps
       inside a bracket (the first version's condition, now for the shaped keyhole);
    3. moves each segment's slope towards the one at which the direct beam it absorbs makes up what the
       reflections leave short of its loss: tan(theta) * (L - R) / D, segment by segment, front and rear
       (Kaplan 1994's balance, A I tan(theta) = q, with the reflected light added).
    Used as an exploration (`explore` in keyhole_first_principles_v2.py): it drives the keyhole to a funnel.
    th: thermal state (k, kappa, theta_w) at the wall temperature; lengths in metres in and out.
    """
    s_nodes = np.linspace(0.0, 1.0, n_seg + 1)
    ds = 1.0 / n_seg
    wf = np.ones(n_seg) if shape_init is None else np.array(shape_init[0], dtype=float)
    wr = np.ones(n_seg) if shape_init is None else np.array(shape_init[1], dtype=float)
    avg = []
    d = d_init if d_init and d_init > 0 else 2.0 * a0
    lo = hi = None
    hist = []
    out = None
    for it in range(max_iter):
        norm = 2.0 * a0 / (d * np.sum((wf + wr) * ds))
        tf, tr = wf * norm, wr * norm
        zn_m = s_nodes * d
        xf = a0 - np.concatenate([[0.0], np.cumsum(tf * d * ds)])
        xr = -a0 + np.concatenate([[0.0], np.cumsum(tr * d * ds)])
        xm = 0.5 * (xf[-1] + xr[-1])
        xf[-1] = xr[-1] = xm
        xcn_m, rn_m = 0.5 * (xf + xr), np.maximum(0.5 * (xf - xr), 0.0)
        Qd, Qr, surf, esc, hits = trace_shaped(zn_m / r0, xcn_m / r0, rn_m / r0, N.real, N.imag, n_rays, seed,
                                               NPHI, 400, 1e-7)
        A_kh = Qd.sum() + Qr.sum()
        scale = A_override / max(A_kh + surf, 1e-12) if A_override is not None else 1.0
        Qd, Qr, surf_s = Qd * scale, Qr * scale, surf * scale
        A_kh_s = A_kh * scale
        wings = wing_sources(a0, surf_s * P)
        zs, xs, q = tilted_conduction(zn_m, xcn_m, rn_m, th, v, wings, point_source_field, theta_w_fn=theta_w_fn)
        Q_c = float(q.sum())
        Q_e = float(Q_evap_fn(a0))
        resid = (A_kh_s * P - Q_c - Q_e) / P
        dzs = np.diff(zn_m)
        rmid = 0.5 * (rn_m[:-1] + rn_m[1:])
        thw = [th.theta_w if theta_w_fn is None else theta_w_fn(max(r, 1e-9)) for r in rmid]
        kap = np.array([kaplan_loss_per_depth(max(r, 1e-9), th.k, th.kappa, tw, v) for r, tw in zip(rmid, thw)]) * dzs
        kap *= Q_c / max(kap.sum(), 1e-30)
        slant = np.sqrt(dzs ** 2 + np.diff(rn_m) ** 2)
        area = 2 * math.pi * rmid * slant
        evap = Q_e * area / max(area.sum(), 1e-30)
        ff = np.array([front_fraction(max(r, 1e-9), v, th.kappa) for r in rmid])
        L_f, L_r = kap * ff + 0.5 * evap, kap * (1 - ff) + 0.5 * evap
        D_f, D_r = Qd[:, :2].sum(1) * P, Qd[:, 2:].sum(1) * P
        R_f, R_r = Qr[:, :2].sum(1) * P, Qr[:, 2:].sum(1) * P
        hist.append((it, d * 1e6, A_kh_s + surf_s, resid))
        if log:
            log(f"  it {it}: d {d * 1e6:.1f} um, A {A_kh_s + surf_s:.3f}, resid {resid:+.4f}")
        out = dict(zn=zn_m, xcn=xcn_m, rn=rn_m, d=d, A_kh=A_kh_s, A_sf=surf_s, Q_c=Q_c, Q_e=Q_e, zs=zs, xs=xs,
                   q=q, wings=wings, hits=hits, resid=resid, iterations=it + 1, history=hist, converged=False,
                   d_spread=0.0)
        if max_iter == 1:
            return out
        fac_f = np.where(L_f > R_f, np.clip((L_f - R_f) / np.maximum(D_f, 1e-12 * P), 0.25, 4.0), 0.25)
        fac_r = np.where(L_r > R_r, np.clip((L_r - R_r) / np.maximum(D_r, 1e-12 * P), 0.25, 4.0), 0.25)
        wf_new = _smooth(wf * fac_f ** relax, 2)
        wr_new = _smooth(wr * fac_r ** relax, 2)
        c = np.sum((wf_new + wr_new) * ds) / 2.0
        wf_new, wr_new = wf_new / c, wr_new / c
        dw = max(np.max(np.abs(np.log(wf_new / wf))), np.max(np.abs(np.log(wr_new / wr))))
        wf, wr = wf_new, wr_new
        if dw > 0.05:
            lo = hi = None
            d_new = d * (1.0 + float(np.clip(2.0 * resid, -0.3, 0.5)))
        else:
            if resid > 0:
                lo = (d, resid)
            else:
                hi = (d, resid)
            if lo is not None and hi is not None:
                d_sec = lo[0] + (hi[0] - lo[0]) * lo[1] / (lo[1] - hi[1])
                d_new = d_sec if min(lo[0], hi[0]) < d_sec < max(lo[0], hi[0]) else 0.5 * (lo[0] + hi[0])
            else:
                d_new = d * (1.0 + float(np.clip(2.0 * resid, -0.3, 0.5)))
        d_new = max(d_new, 1e-3 * a0)
        if it >= max_iter // 2:
            avg.append((d, wf.copy(), wr.copy()))
        if abs(d_new - d) < tol * d and dw < 0.05 and abs(resid) < 0.01:
            out["converged"] = True
            break
        d = d_new
    if not out["converged"] and len(avg) >= 3:
        ds_ = np.array([a[0] for a in avg])
        out2 = solve_shaped(P, v, r0, a0, N, th, Q_evap_fn, wing_sources, point_source_field, A_override=A_override,
                            d_init=float(ds_.mean()), n_seg=n_seg, n_rays=n_rays, seed=seed, max_iter=1,
                            shape_init=(np.mean([a[1] for a in avg], axis=0), np.mean([a[2] for a in avg], axis=0)),
                            theta_w_fn=theta_w_fn)
        out2["converged"] = bool(ds_.std() < 0.05 * ds_.mean())
        out2["d_spread"] = float(ds_.std() / ds_.mean())
        out2["iterations"] = max_iter
        out2["history"] = hist
        out = out2
    return out


def parametric_nodes(a0, d, p, x_tip, n_seg=32):
    """Keyhole of opening radius a0 and depth d with radius r = a0 (1 - s)^p and a straight axis tilted so the
    tip sits x_tip from the opening's centre (s = z/d). p = 1 is a cone, p = 1/2 a paraboloid."""
    s = np.linspace(0.0, 1.0, n_seg + 1)
    return s * d, x_tip * s, a0 * (1 - s) ** p


def solve_parametric(P, v, r0, a0, N, th, Q_evap_fn, wing_sources, point_source_field, A_override=None,
                     d_init=None, p_init=1.0, n_seg=32, n_rays=20000, seed=11, max_iter=45, log=None,
                     theta_w_fn=None, fix_shape=False, tilt="free"):
    """The keyhole's depth, tilt and profile from three moments of the wall energy balance.

    The free-form point-by-point balance (Kaplan 1994) with reflections is ill-posed here, so the shape is a
    family with three parameters, each set by one condition:
      d      total power absorbed in the keyhole = conducted + evaporated (the first version's condition);
      x_tip  power absorbed on the front half of the wall = the front half's loss (Kaplan's cos(phi) + K1/K0
             split of the conduction), which tilts the keyhole back until the front wall is in balance;
      p      depth centroid of the absorbed power = depth centroid of the loss, which picks between a cone
             (p = 1), a paraboloid (p = 1/2) and anything near them.
    fix_shape keeps p = p_init and x_tip = 0 (version 1's straight cone or paraboloid).
    tilt="kaplan" keeps p = p_init and sets the tilt from the front wall's own balance instead (Kaplan 1994,
    Fabbro & Chouf 2000): the front wall leans back until the direct beam it catches, A(theta) I tan(theta) per
    unit depth and arc, equals its conduction loss, k theta_w Pe' (1 + K1(Pe' r)/K0(Pe' r)), at mid-depth.
    """
    p, x_tip = p_init, 0.0
    d = d_init if d_init and d_init > 0 else 2.0 * a0
    lo = hi = None
    hist = []
    out = None
    avg = []
    for it in range(max_iter):
        zn_m, xcn_m, rn_m = parametric_nodes(a0, d, p, x_tip, n_seg)
        Qd, Qr, surf, esc, hits = trace_shaped(zn_m / r0, xcn_m / r0, rn_m / r0, N.real, N.imag, n_rays, seed,
                                               NPHI, 400, 1e-7)
        A_kh = Qd.sum() + Qr.sum()
        scale = A_override / max(A_kh + surf, 1e-12) if A_override is not None else 1.0
        Qd, Qr, surf_s = Qd * scale, Qr * scale, surf * scale
        A_kh_s = A_kh * scale
        wings = wing_sources(a0, surf_s * P)
        zs, xs, q = tilted_conduction(zn_m, xcn_m, rn_m, th, v, wings, point_source_field, theta_w_fn=theta_w_fn)
        Q_c = float(q.sum())
        Q_e = float(Q_evap_fn(a0))
        dzs = np.diff(zn_m)
        rmid = 0.5 * (rn_m[:-1] + rn_m[1:])
        zmid = 0.5 * (zn_m[:-1] + zn_m[1:])
        thw = [th.theta_w if theta_w_fn is None else theta_w_fn(max(r, 1e-9)) for r in rmid]
        kap = np.array([kaplan_loss_per_depth(max(r, 1e-9), th.k, th.kappa, tw, v) for r, tw in zip(rmid, thw)]) * dzs
        kap *= Q_c / max(kap.sum(), 1e-30)
        slant = np.sqrt(dzs ** 2 + np.diff(rn_m) ** 2)
        area = 2 * math.pi * rmid * slant
        evap = Q_e * area / max(area.sum(), 1e-30)
        ff = np.array([front_fraction(max(r, 1e-9), v, th.kappa) for r in rmid])
        L_f, L_r = kap * ff + 0.5 * evap, kap * (1 - ff) + 0.5 * evap
        Abs = (Qd + Qr).sum(1) * P
        Abs_f = (Qd + Qr)[:, :2].sum(1) * P
        Ltot = L_f + L_r
        r1 = (A_kh_s * P - Q_c - Q_e) / P
        r2 = (Abs_f.sum() - L_f.sum()) / max(Abs.sum(), 1e-12)
        zc_abs = float((Abs * zmid).sum() / max(Abs.sum(), 1e-12)) / d
        zc_loss = float((Ltot * zmid).sum() / max(Ltot.sum(), 1e-12)) / d
        r3 = zc_abs - zc_loss
        hist.append((it, d * 1e6, A_kh_s + surf_s, r1, r2, r3, p, x_tip * 1e6))
        if log:
            log(f"  it {it}: d {d * 1e6:.1f} um, A {A_kh_s + surf_s:.3f}, p {p:.3f}, x_tip {x_tip * 1e6:.1f} um, "
                f"r1 {r1:+.4f} r2 {r2:+.4f} r3 {r3:+.4f}")
        out = dict(zn=zn_m, xcn=xcn_m, rn=rn_m, d=d, p=p, x_tip=x_tip, A_kh=A_kh_s, A_sf=surf_s, Q_c=Q_c, Q_e=Q_e,
                   zs=zs, xs=xs, q=q, wings=wings, hits=hits, resid=r1, resid_front=r2, resid_centroid=r3,
                   iterations=it + 1, history=hist, converged=False, d_spread=0.0, zc_abs=zc_abs, zc_loss=zc_loss)
        done = abs(r1) < 0.004 and (fix_shape or (abs(r2) < 0.01 and abs(r3) < 0.01)
                                    or (tilt == "kaplan" and it > 2 and abs(hist[-2][7] - x_tip * 1e6) < 0.2))
        if done or max_iter == 1:
            out["converged"] = bool(done)
            break
        # shape: tilt and profile (skipped with fix_shape)
        moved = 0.0
        if tilt == "kaplan" and not fix_shape:
            x_new = kaplan_tip(P, r0, a0, d, x_tip, N, th, v, theta_w_fn)
            x_new = x_tip + 0.5 * (x_new - x_tip)
            moved = abs(x_new - x_tip) / a0
            x_tip = x_new
        elif not fix_shape:
            dx = float(np.clip(1.5 * r2, -0.15, 0.15)) * a0
            x_new = float(np.clip(x_tip + dx, -4.0 * a0, 0.5 * a0))
            p_new = float(np.clip(p * math.exp(float(np.clip(3.0 * r3, -0.15, 0.15))), 0.25, 4.0))
            moved = max(abs(x_new - x_tip) / a0, abs(math.log(p_new / p)))
            x_tip, p = x_new, p_new
        # depth: secant steps in a bracket once the shape has settled
        if moved > 0.03:
            lo = hi = None
            d_new = d * (1.0 + float(np.clip(2.0 * r1, -0.3, 0.5)))
        else:
            if r1 > 0:
                lo = (d, r1)
            else:
                hi = (d, r1)
            if lo is not None and hi is not None:
                d_sec = lo[0] + (hi[0] - lo[0]) * lo[1] / (lo[1] - hi[1])
                d_new = d_sec if min(lo[0], hi[0]) < d_sec < max(lo[0], hi[0]) else 0.5 * (lo[0] + hi[0])
            else:
                d_new = d * (1.0 + float(np.clip(2.0 * r1, -0.3, 0.5)))
        if it >= max_iter * 2 // 3:
            avg.append((d, p, x_tip))
        d = max(d_new, 1e-3 * a0)
    if not out["converged"] and len(avg) >= 3:
        arr = np.array(avg)
        out2 = solve_parametric_eval(P, v, r0, a0, N, th, Q_evap_fn, wing_sources, point_source_field, A_override,
                                     float(arr[:, 0].mean()), float(arr[:, 1].mean()), float(arr[:, 2].mean()),
                                     n_seg, n_rays, seed, theta_w_fn)
        out2["converged"] = bool(arr[:, 0].std() < 0.05 * arr[:, 0].mean())
        out2["d_spread"] = float(arr[:, 0].std() / arr[:, 0].mean())
        out2["iterations"] = max_iter
        out2["history"] = hist
        out = out2
    return out


def solve_parametric_eval(P, v, r0, a0, N, th, Q_evap_fn, wing_sources, point_source_field, A_override, d, p, x_tip,
                          n_seg, n_rays, seed, theta_w_fn):
    """Evaluate one fixed shape (d, p, x_tip): ray tracing, conduction and the three residuals."""
    zn_m, xcn_m, rn_m = parametric_nodes(a0, d, p, x_tip, n_seg)
    Qd, Qr, surf, esc, hits = trace_shaped(zn_m / r0, xcn_m / r0, rn_m / r0, N.real, N.imag, n_rays, seed, NPHI,
                                           400, 1e-7)
    A_kh = Qd.sum() + Qr.sum()
    scale = A_override / max(A_kh + surf, 1e-12) if A_override is not None else 1.0
    Qd, Qr, surf_s = Qd * scale, Qr * scale, surf * scale
    wings = wing_sources(a0, surf_s * P)
    zs, xs, q = tilted_conduction(zn_m, xcn_m, rn_m, th, v, wings, point_source_field, theta_w_fn=theta_w_fn)
    Q_c, Q_e = float(q.sum()), float(Q_evap_fn(a0))
    return dict(zn=zn_m, xcn=xcn_m, rn=rn_m, d=d, p=p, x_tip=x_tip, A_kh=A_kh * scale, A_sf=surf_s, Q_c=Q_c,
                Q_e=Q_e, zs=zs, xs=xs, q=q, wings=wings, hits=hits, resid=(A_kh * scale * P - Q_c - Q_e) / P,
                resid_front=float("nan"), resid_centroid=float("nan"), iterations=1, history=[], converged=False,
                d_spread=0.0)


def kaplan_tip(P, r0, a0, d, x_tip, N, th, v, theta_w_fn=None):
    """Tip offset of a cone whose front wall leans back at Kaplan's angle at mid-depth (see solve_parametric)."""
    r_mid = 0.5 * a0
    tw = th.theta_w if theta_w_fn is None else theta_w_fn(r_mid)
    pe = v / (2 * th.kappa)
    q_f = th.k * tw * pe * (1 + kaplan_ratio(r_mid, v, th.kappa))
    x_f = 0.5 * (a0 + x_tip)  # the front wall at mid-depth
    I = 2 * P / (math.pi * r0 ** 2) * math.exp(-2 * x_f ** 2 / r0 ** 2)
    t = 0.3
    for _ in range(50):
        th_ang = math.atan(t)
        A = fresnel_A(N.real, N.imag, math.sin(th_ang))  # incidence 90 deg - theta from the wall normal
        t_new = q_f / max(A * I, 1e-30)
        if abs(t_new - t) < 1e-6 * t:
            t = t_new
            break
        t = 0.5 * (t + t_new)
    t = min(t, 50.0)
    return a0 - d * t
