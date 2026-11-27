"""Melt pool and process window for the fast-track LPBF (FT-0 / FT-1), AlSi10Mg first, 6061 and 7075 noted (#260).

Model
  Eagar and Tsai (1983, Welding J. 62, 346s): quasi-steady temperature field of a Gaussian surface source moving at v
  over a semi-infinite body with constant properties and no latent heat,
      T - T0 = A P / (pi rho c sqrt(4 pi alpha)) * int_0^inf  tau^-1/2 / (2 alpha tau + s^2)
               * exp(-((x + v tau)^2 + y^2) / (4 alpha tau + 2 s^2) - z^2 / (4 alpha tau)) dtau,
  with s = w0 / 2 (w0 = 1/e2 radius of the beam). Integrated with tau = u^2 on a fixed geometric grid; checked against
  scipy.integrate.quad to 3e-5 (scratch check in the README). The melt pool is the region above the liquidus: width W,
  depth D (below the surface the model takes as flat) and length L.

Criteria on the P-v map (each with its source in the README)
  keyhole     King et al. 2014 normalised enthalpy, and Gan et al. 2021 keyhole number Ke (same group of variables)
  lack of     Tang, Pistorius and Beuth 2017: full overlap when (H/W)^2 + (t/D)^2 <= 1 for hatch H and layer t
  fusion      (and, for a single track, D >= t: the pool reaches through the powder layer into the solid below)
  balling     Plateau-Rayleigh: L/W > pi (Yadroitsev et al. 2010)

Units: SI inside (m, s, W, K); tables in mm, um, m/s, W. Run: python desktop-lpbf/fast-track/process/meltpool.py
"""
from __future__ import annotations

import json
import math
import pathlib
from dataclasses import asdict, dataclass

import numpy as np
from scipy.optimize import minimize_scalar

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
IMG = HERE / "img"

# --------------------------------------------------------------------------------------------------
# The beam (optics.py has the derivation; repeated here so this module stands alone)
# --------------------------------------------------------------------------------------------------
LAM = 1.070e-6          # m, IPG YLR-SM centre wavelength
M2 = 1.1                # IPG YLR-SM M2 (max)
F_LENS = 0.254          # m, LINOS F-Theta-Ronar f = 254 mm


def spot_w0(D_coll_mm: float, m2: float = M2, f: float = F_LENS) -> float:
    """1/e2 focal radius (m) of a collimated beam of 1/e2 diameter D_coll focused by f."""
    return 2 * m2 * LAM * f / (math.pi * D_coll_mm * 1e-3)


W0 = {5.0: spot_w0(5.0), 7.5: spot_w0(7.5)}     # 38.1 um and 25.4 um (76 and 51 um spots)


# --------------------------------------------------------------------------------------------------
# Materials (constant effective properties for Eagar-Tsai; sources in the README table)
# --------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Material:
    name: str
    rho: float          # kg/m3
    cp: float           # J/kg K, effective (solid, RT to solidus)
    k: float            # W/m K, effective (between the hot solid and the liquid)
    T_sol: float        # C
    T_liq: float        # C
    T_boil: float       # C (of the most volatile major element where that matters)
    Lf: float           # J/kg latent heat of fusion
    note: str = ""

    @property
    def alpha(self) -> float:
        return self.k / (self.rho * self.cp)


ALSI10MG = Material("AlSi10Mg", 2670.0, 1000.0, 130.0, 557.0, 596.0, 2467.0, 4.23e5,
                    "as-built LPBF k ~110-150 W/mK, liquid ~70-90: 130 effective; Al boils at 2467 C")
AL6061 = Material("6061", 2700.0, 1000.0, 150.0, 582.0, 652.0, 2467.0, 3.96e5,
                  "wrought 6061-T6 k 167 W/mK, lower hot and liquid: 150 effective; hot-crack prone")
AL7075 = Material("7075", 2810.0, 1000.0, 120.0, 477.0, 635.0, 907.0, 3.76e5,
                  "7075-T6 k 130 W/mK; Zn (5.6 %) boils at 907 C, so vapour and keyhole porosity set in earlier")
MATERIALS = {m.name: m for m in (ALSI10MG, AL6061, AL7075)}


# --------------------------------------------------------------------------------------------------
# Eagar-Tsai kernel
# --------------------------------------------------------------------------------------------------
class Pool:
    """Temperature per absorbed watt, F(x, y, z) in K/W, for one material, spot and speed; melt-pool sizes for any
    absorbed power and preheat follow from one threshold F_th = (T_liq - T0) / (A P)."""

    def __init__(self, mat: Material, w0: float, v: float, n: int = 1200, x_back: float = 6e-3):
        self.mat, self.w0, self.v = mat, w0, v
        a = mat.alpha
        self.s2 = (w0 / 2) ** 2
        smax = max(math.sqrt(x_back / v) * 1.6, 8 * math.sqrt(4 * a) / v)
        self.u = np.concatenate([[0.0], np.geomspace(1e-7, smax, n)])
        self.pre = 1.0 / (math.pi * mat.rho * mat.cp * math.sqrt(4 * math.pi * a))
        U2 = self.u ** 2
        self._d1 = 2 * a * U2 + self.s2               # 2 alpha tau + s^2
        self._d2 = 4 * a * U2 + 2 * self.s2           # 4 alpha tau + 2 s^2
        self._d3 = 4 * a * U2                          # 4 alpha tau
        self._vu2 = v * U2
        self.x_back = x_back
        self._tab = None

    def F(self, x, y, z):
        x, y, z = (np.atleast_1d(np.asarray(q, float))[:, None] for q in (x, y, z))
        with np.errstate(divide="ignore", invalid="ignore"):
            zt = np.where(self._d3 > 0, z ** 2 / np.where(self._d3 > 0, self._d3, 1.0), np.where(z == 0, 0.0, np.inf))
        g = 2.0 / self._d1 * np.exp(-((x + self._vu2) ** 2 + y ** 2) / self._d2 - zt)
        return self.pre * np.trapezoid(g, self.u, axis=1)

    def _line_max(self, y=0.0, z=0.0):
        f = lambda x: -float(self.F(x, y, z)[0])
        r = minimize_scalar(f, bounds=(-self.x_back * 0.8, 3 * self.w0), method="bounded",
                            options=dict(xatol=2e-8))
        return -r.fun, r.x

    def tables(self):
        if self._tab is None:
            yz = np.geomspace(2e-7, 3e-3, 70)
            Gy = np.array([self._line_max(y=y)[0] for y in yz])
            Gz = np.array([self._line_max(z=z)[0] for z in yz])
            xc = np.concatenate([-np.geomspace(1e-7, self.x_back * 0.95, 700)[::-1], [0.0], np.geomspace(1e-7, 4 * self.w0, 200)])
            Fc = self.F(xc, 0.0, 0.0)
            self._tab = dict(yz=yz, Gy=Gy, Gz=Gz, xc=xc, Fc=Fc, Fpeak=float(max(Gy[0], Fc.max())))
        return self._tab

    def dims(self, F_th):
        """(W, D, L) in m for the isotherm F = F_th (K/W). Zero if nothing melts."""
        t = self.tables()
        if F_th >= t["Fpeak"]:
            return 0.0, 0.0, 0.0
        yz = t["yz"]

        def inv(G):
            # G decreasing in yz; interpolate log(yz) against log(G)
            if F_th >= G[0]:
                return 0.0
            if F_th <= G[-1]:
                return float(yz[-1])
            lg, ly = np.log(G[::-1]), np.log(yz[::-1])
            return float(np.exp(np.interp(math.log(F_th), lg, ly)))

        half_w, depth = inv(t["Gy"]), inv(t["Gz"])
        xc, Fc = t["xc"], t["Fc"]
        inside = np.where(Fc >= F_th)[0]
        if len(inside) == 0:
            length = 0.0
        else:
            i0, i1 = inside[0], inside[-1]

            def cross(ia, ib):
                fa, fb = Fc[ia], Fc[ib]
                return xc[ia] + (F_th - fa) * (xc[ib] - xc[ia]) / (fb - fa) if fb != fa else xc[ia]
            x0 = cross(i0 - 1, i0) if i0 > 0 else xc[0]
            x1 = cross(i1, i1 + 1) if i1 < len(xc) - 1 else xc[-1]
            length = float(x1 - x0)
        return 2 * half_w, depth, length


_POOLS: dict = {}


def pool(mat: Material, w0: float, v: float) -> Pool:
    key = (mat.name, round(w0 * 1e9), round(v * 1e4))
    if key not in _POOLS:
        _POOLS[key] = Pool(mat, w0, v)
    return _POOLS[key]


def track(mat: Material, P: float, v: float, A: float, T0: float = 25.0, w0: float = W0[5.0]):
    """Melt-pool width, depth, length (um) and the peak surface temperature (C) of one track."""
    pl = pool(mat, w0, v)
    W, D, L = pl.dims((mat.T_liq - T0) / (A * P))
    return dict(W_um=W * 1e6, D_um=D * 1e6, L_um=L * 1e6, T_peak_C=T0 + A * P * pl.tables()["Fpeak"])


# --------------------------------------------------------------------------------------------------
# Dimensionless keyhole measures
# --------------------------------------------------------------------------------------------------
def king_enthalpy(mat: Material, P, v, A, w0=W0[5.0]):
    """King et al. 2014: Delta H / h_s = A P / (pi h_s sqrt(D v w^3)), h_s = rho c T_m (T_m in K), w the beam radius."""
    h_s = mat.rho * mat.cp * (mat.T_liq + 273.15)
    return A * P / (math.pi * h_s * np.sqrt(mat.alpha * v * w0 ** 3))


def keyhole_number(mat: Material, P, v, A, T0=25.0, w0=W0[5.0]):
    """Gan et al. 2021: Ke = A P / ((T_l - T0) pi rho c sqrt(alpha v r0^3)), r0 the 1/e2 radius."""
    return A * P / ((mat.T_liq - T0) * math.pi * mat.rho * mat.cp * np.sqrt(mat.alpha * v * w0 ** 3))


KING_TH = 30.0           # King et al. 2014 transition for 316L (+-4); its transfer to Al is checked against data below
KE_TH = 6.0              # Gan et al. 2021: keyhole above Ke ~ 6 (their aspect ratio e* = depth / r0 crosses ~2)


# --------------------------------------------------------------------------------------------------
# Process map
# --------------------------------------------------------------------------------------------------
def pv_map(mat: Material, A: float, T0: float, t_layer: float, hatch: float, w0=W0[5.0],
           P_grid=np.arange(100.0, 401.0, 10.0), v_grid=np.round(np.arange(0.1, 3.0001, 0.05), 3)):
    """Arrays on (P, v): W, D, L (um), and the classification flags."""
    nP, nv = len(P_grid), len(v_grid)
    Wm, Dm, Lm = (np.zeros((nP, nv)) for _ in range(3))
    for j, v in enumerate(v_grid):
        pl = pool(mat, w0, v)
        for i, P in enumerate(P_grid):
            W, D, L = pl.dims((mat.T_liq - T0) / (A * P))
            Wm[i, j], Dm[i, j], Lm[i, j] = W * 1e6, D * 1e6, L * 1e6
    PP, VV = np.meshgrid(P_grid, v_grid, indexing="ij")
    Ke = keyhole_number(mat, PP, VV, A, T0, w0)
    NH = king_enthalpy(mat, PP, VV, A, w0)
    with np.errstate(divide="ignore", invalid="ignore"):
        tang = np.where(Dm > 0, (hatch * 1e3 / np.maximum(Wm, 1e-9)) ** 2 + (t_layer * 1e3 / np.maximum(Dm, 1e-9)) ** 2, np.inf)
        LW = np.where(Wm > 0, Lm / np.maximum(Wm, 1e-9), np.inf)
    no_bond = Dm < t_layer * 1e3
    lof = (tang > 1.0) | no_bond
    keyhole = Ke > KE_TH
    balling = LW > math.pi
    ok = ~lof & ~keyhole & ~balling
    return dict(P=P_grid, v=v_grid, W=Wm, D=Dm, L=Lm, Ke=Ke, NH=NH, tang=tang, LW=LW,
                no_bond=no_bond, lof=lof, keyhole=keyhole, balling=balling, ok=ok)


def main():
    import time
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    rows = []
    for v in (0.25, 0.5, 1.0, 1.5, 2.0, 3.0):
        for P in (100, 200, 300, 400):
            for T0 in (25.0, 200.0):
                r = track(ALSI10MG, P, v, 0.4, T0)
                rows.append(dict(P=P, v=v, T0=T0, **{k: round(x, 1) for k, x in r.items()},
                                 Ke=round(float(keyhole_number(ALSI10MG, P, v, 0.4, T0)), 2),
                                 NH=round(float(king_enthalpy(ALSI10MG, P, v, 0.4)), 2)))
    print(f"{len(rows)} tracks in {time.time() - t0:.1f} s")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
