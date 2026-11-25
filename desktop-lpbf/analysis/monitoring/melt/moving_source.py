"""Closed-form moving heat sources: Rosenthal's point source and the Eagar-Tsai Gaussian (issue #260; monitoring/melt-pool.md).

Beam frame: the beam centre is at the origin and moves in +x; z <= 0 is depth below the surface; constant properties
(k, rho*c, a = k / rho c), no latent heat, no powder layer.

  Rosenthal (1946):  T - T0 = A P / (2 pi k R) * exp(-v (R + x) / (2 a))
  Eagar & Tsai (1983, Weld. J. 62:346s), Gaussian I = A P / (2 pi s^2) exp(-r^2 / 2 s^2), s = w / 2 (w the 1/e^2 radius):
      T - T0 = 2 A P / (pi rho c sqrt(4 pi a)) * Int_0^inf tau^-1/2 / (2 s^2 + 4 a tau)
                   * exp(-((x + v tau)^2 + y^2) / (2 s^2 + 4 a tau) - z^2 / (4 a tau)) dtau
  (the factor 2 is the image source of the insulated surface; the s -> 0 limit is Rosenthal, checked in __main__).
"""
from __future__ import annotations

import math

import numpy as np


def rosenthal(x, y, z, AP, v, k, a, T0):
    R = np.sqrt(x * x + y * y + z * z)
    R = np.maximum(R, 1e-9)
    return T0 + AP / (2 * math.pi * k * R) * np.exp(-v * (R + x) / (2 * a))


def _s_nodes(n=400, s_max=None, a=6e-5, L=0.02):
    # tau = s^2; integrate s from 0 to sqrt(tau_max), tau_max ~ L^2 / a (diffusion across the far field)
    s_max = s_max or math.sqrt(L * L / a)
    # dense near 0 (the beam's own dwell), log-spaced beyond
    s = np.concatenate([np.linspace(0, 1e-4, 60, endpoint=False), np.geomspace(1e-4, s_max, n)])
    return s


def eagar_tsai(x, y, z, AP, v, rho_c, a, T0, w, n=500, L=0.02):
    """Eagar-Tsai temperature at points (x, y, z) (arrays, m). w: 1/e^2 beam radius (m). Memory ~ npoints x n."""
    x, y, z = (np.asarray(t, float) for t in np.broadcast_arrays(x, y, z))
    shp = x.shape
    x, y, z = x.ravel(), y.ravel(), z.ravel()
    s2 = (w / 2.0) ** 2
    s = _s_nodes(n, a=a, L=L)
    out = np.empty(x.size)
    pref = 2 * AP / (math.pi * rho_c * math.sqrt(4 * math.pi * a))
    chunk = max(1, int(2e6 // s.size))
    tau = s * s
    den = 2 * s2 + 4 * a * tau
    for i0 in range(0, x.size, chunk):
        xi, yi, zi = x[i0:i0 + chunk, None], y[i0:i0 + chunk, None], z[i0:i0 + chunk, None]
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            ez = np.where(tau > 0, zi * zi / (4 * a * np.maximum(tau, 1e-300)), np.where(np.abs(zi) > 0, np.inf, 0.0))
            f = 2.0 / den * np.exp(-((xi + v * tau) ** 2 + yi * yi) / den - ez)      # 2 ds = tau^-1/2 dtau
        f = np.nan_to_num(f)
        out[i0:i0 + chunk] = np.trapezoid(f, s, axis=1)
    return (T0 + pref * out).reshape(shp)


def _cross_max(prof, coord, Tm):
    """Largest coordinate where prof >= Tm, linearly interpolated (prof sampled on increasing coord)."""
    above = prof >= Tm
    if not above.any():
        return 0.0
    i = np.where(above)[0][-1]
    if i + 1 >= len(prof):
        return float(coord[i])
    t = (prof[i] - Tm) / (prof[i] - prof[i + 1])
    return float(coord[i] + t * (coord[i + 1] - coord[i]))


def pool_dims_et(AP, v, rho_c, a, T0, w, T_melt, k=None, n=150):
    """Melt-pool length, width, depth (m) and peak surface temperature from Eagar-Tsai, read off sampled grids (vectorised)."""
    def ET(x, y, z):
        return eagar_tsai(x, y, z, AP, v, rho_c, a, T0, w, n=n)

    # centreline: find the peak and the front/back crossings, growing the window until the back is cold
    span = 8 * w
    while True:
        xs = np.linspace(-span, max(2.5 * w, 0.25 * span), 400)
        Ts = ET(xs, 0 * xs, 0 * xs)
        if Ts[0] < T_melt or span > 0.05:
            break
        span *= 2
    i = int(np.argmax(Ts))
    T_pk, x_pk = float(Ts[i]), float(xs[i])
    if T_pk < T_melt:
        return dict(L=0.0, W=0.0, D=0.0, T_peak=T_pk, x_peak=x_pk)
    x_front = _cross_max(Ts[i:], xs[i:], T_melt)
    x_back = -_cross_max(Ts[:i + 1][::-1], -xs[:i + 1][::-1], T_melt)
    L = x_front - x_back
    xg = np.linspace(x_back, x_front, 36)
    ext = max(2 * w, 0.6 * L)
    while True:
        yg = np.linspace(0, ext, 70)
        X, Y = np.meshgrid(xg, yg, indexing="ij")
        T2 = ET(X, Y, 0 * X)
        if (T2[:, -1] < T_melt).all() or ext > 0.05:
            break
        ext *= 1.6
    W = max(_cross_max(T2[j], yg, T_melt) for j in range(len(xg)))
    ext = max(2 * w, 0.6 * L)
    while True:
        zg = np.linspace(0, ext, 70)
        X, Z = np.meshgrid(xg, zg, indexing="ij")
        T3 = ET(X, 0 * X, -Z)
        if (T3[:, -1] < T_melt).all() or ext > 0.05:
            break
        ext *= 1.6
    D = max(_cross_max(T3[j], zg, T_melt) for j in range(len(xg)))
    return dict(L=L, W=2 * W, D=D, T_peak=T_pk, x_peak=x_pk, x_front=x_front, x_back=x_back)


if __name__ == "__main__":
    # check: Eagar-Tsai -> Rosenthal as the beam shrinks
    AP, v, k, rc = 100.0, 1.0, 150.0, 2.7e6
    a = k / rc
    pts = np.array([[-200e-6, 0, -30e-6], [50e-6, 40e-6, -20e-6], [-500e-6, 100e-6, -80e-6]])
    for w in (48e-6, 10e-6, 2e-6):
        et = eagar_tsai(pts[:, 0], pts[:, 1], pts[:, 2], AP, v, rc, a, 300.0, w)
        ro = rosenthal(pts[:, 0], pts[:, 1], pts[:, 2], AP, v, k, a, 300.0)
        print(f"w {w * 1e6:5.1f} um  ET {np.round(et, 1)}  Rosenthal {np.round(ro, 1)}")
    # energy check: stationary Gaussian peak (v -> 0 limit) = AP / (2 sqrt(2 pi) s k)
    w = 48e-6
    print("stationary peak, ET with v=1e-4:", float(eagar_tsai(np.array([0.0]), np.array([0.0]), np.array([0.0]), AP, 1e-4, rc, a, 0.0, w,
                                                                 L=0.5)[0]),
          " exact:", AP / (2 * math.sqrt(2 * math.pi) * (w / 2) * k))
