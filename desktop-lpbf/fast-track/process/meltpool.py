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


ALSI10MG = Material("AlSi10Mg", 2670.0, 915.0, 110.0, 563.0, 576.0, 2467.0, 3.96e5,
                    "Tang's AlSi10Mg inputs (thesis Table 12: k 110, c 915, rho 2670, T_m 849 K); DSC solidus 563 C; "
                    "Al boils at 2467 C (T_v 2740 K)")
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
    """King et al. 2014 Eq. 2.6: Delta H / h_s = A P / (h_s sqrt(pi D v sigma^3)), h_s = rho c T_m (T_m in K),
    sigma the Gaussian standard deviation (I ~ exp(-r^2 / 2 sigma^2)), i.e. w0 / 2 for a 1/e2 radius w0."""
    h_s = mat.rho * mat.cp * (mat.T_liq + 273.15)
    sig = w0 / 2
    return A * P / (h_s * np.sqrt(math.pi * mat.alpha * v * sig ** 3))


def keyhole_number(mat: Material, P, v, A, T0=25.0, w0=W0[5.0]):
    """Gan et al. 2021: Ke = A P / ((T_l - T0) pi rho c sqrt(alpha v r0^3)), r0 the 1/e2 radius."""
    return A * P / ((mat.T_liq - T0) * math.pi * mat.rho * mat.cp * np.sqrt(mat.alpha * v * w0 ** 3))


KING_TH = 30.0           # King et al. 2014: keyhole above 30 +- 4 (316L, 50 um powder layer)
KE_TH = 20.0             # Patel et al. 2022 for AlSi10Mg: conduction Ke < 12, transition 12-20, keyhole > 20
KE_COND = 12.0


# --------------------------------------------------------------------------------------------------
# Calibration against published AlSi10Mg single tracks
# --------------------------------------------------------------------------------------------------
DOI = {
    "Bosio 2019": "Bosio et al. 2019, Mater. Des. 181:107949, doi:10.1016/j.matdes.2019.107949 (Table A1; EOSINT M270, "
                  "100 um spot, platform 100 C, one 50 um layer on a 40 mm AlSi10Mg disc)",
    "Kempen 2011": "Kempen et al. 2011, SFF Symp. 484-495, utw10945.utweb.utexas.edu/Manuscripts/2011/2011-37-Kempen.pdf "
                   "(Concept Laser M1, 200 W, ~150 um at 99 % energy = 99 um at 1/e2; width 137 um at 200 W, 1.4 m/s)",
    "Tang thesis": "Tang 2017, CMU thesis, doi:10.1184/R1/6720185.v1, Table 13 (spot and platform temperature not "
                   "given here: 100 um and 35 C assumed)",
}
BOSIO = [(160, .3, 169, 41), (160, .8, 120, 30), (160, 1.5, 91, 28), (180, .3, 168, 48), (180, .8, 155, 39),
         (180, 1.2, 111, 32), (180, 1.5, 108, 22), (195, .3, 187, 90), (195, .6, 148, 53), (195, .8, 156, 47),
         (195, 1.5, 109, 31)]
CAL = [("Bosio 2019", P, v, 50.0, 100.0, W, d) for (P, v, W, d) in BOSIO]
CAL += [("Kempen 2011", 200.0, 1.4, 49.4, 25.0, 137.0, None)]
CAL += [("Tang thesis", 180.0, 0.9, 50.0, 35.0, 156.0, None), ("Tang thesis", 200.0, 1.4, 50.0, 35.0, 170.0, None),
        ("Tang thesis", 360.0, 1.0, 50.0, 35.0, 278.0, None)]
# Bosio's job 1 (5 x 5): 100-130 W unstable ("balling more as speed rose"), 160-195 W regular
BOSIO_GRID_P = (100.0, 130.0, 160.0, 180.0, 195.0)
BOSIO_GRID_V = (0.3, 0.6, 0.8, 1.2, 1.5)


def calibrate(mat=ALSI10MG):
    from scipy.optimize import minimize_scalar

    def cost(A, rows):
        return sum(math.log(track(mat, r[1], r[2], A, r[4], r[3] * 1e-6)["W_um"] / r[5]) ** 2 for r in rows)
    out = {}
    for name, rows in (("all", CAL), ("Bosio 2019", CAL[:11])):
        r = minimize_scalar(lambda A: cost(A, rows), bounds=(0.05, 0.9), method="bounded", options=dict(xatol=1e-4))
        out[name] = dict(A=float(r.x), rms_log=math.sqrt(r.fun / len(rows)), n=len(rows))
    A = out["all"]["A"]
    rows = []
    for r in CAL:
        t = track(mat, r[1], r[2], A, r[4], r[3] * 1e-6)
        rows.append(dict(source=r[0], P=r[1], v=r[2], w0_um=r[3], T0=r[4], W_meas=r[5], pen_meas=r[6],
                         W_model=t["W_um"], D_model=t["D_um"], L_model=t["L_um"],
                         NH=float(king_enthalpy(mat, r[1], r[2], A, r[3] * 1e-6)),
                         Ke=float(keyhole_number(mat, r[1], r[2], A, r[4], r[3] * 1e-6))))
    # continuity: E-T depth of Bosio's job-1 tracks, unstable (<= 130 W) against regular (>= 160 W)
    grid = []
    for P in BOSIO_GRID_P:
        for v in BOSIO_GRID_V:
            t = track(mat, P, v, A, 100.0, 50e-6)
            grid.append(dict(P=P, v=v, D=t["D_um"], W=t["W_um"], stable=P >= 160))
    d_unstable = max(g["D"] for g in grid if not g["stable"] and g["v"] >= 0.6)
    d_stable = min(g["D"] for g in grid if g["stable"])
    out.update(A=A, rows=rows, bosio_grid=grid, D_unstable_max=d_unstable, D_stable_min=d_stable,
               D_min=0.5 * (d_unstable + d_stable))
    return out


# --------------------------------------------------------------------------------------------------
# Process map
# --------------------------------------------------------------------------------------------------
def pv_map(mat: Material, A: float, T0: float, t_layer: float, hatch, w0=W0[5.0], D_min=None,
           P_grid=np.arange(100.0, 401.0, 10.0), v_grid=np.round(np.arange(0.1, 3.0001, 0.05), 3)):
    """Arrays on (P, v): W, D, L (um) and the classes. hatch None = single tracks (continuity: D >= D_min, the
    depth that separated Bosio's stable from unstable tracks on a 50 um layer, scaled with the layer); else Tang's
    lack-of-fusion criterion for hatch and layer."""
    nP, nv = len(P_grid), len(v_grid)
    Wm, Dm, Lm = (np.zeros((nP, nv)) for _ in range(3))
    for j, v in enumerate(v_grid):
        pl = pool(mat, w0, v)
        for i, P in enumerate(P_grid):
            W, D, L = pl.dims((mat.T_liq - T0) / (A * P))
            Wm[i, j], Dm[i, j], Lm[i, j] = W * 1e6, D * 1e6, L * 1e6
    PP, VV = np.meshgrid(P_grid, v_grid, indexing="ij")
    NH = king_enthalpy(mat, PP, VV, A, w0)
    Ke = keyhole_number(mat, PP, VV, A, T0, w0)
    with np.errstate(divide="ignore", invalid="ignore"):
        LW = np.where(Wm > 0, Lm / np.maximum(Wm, 1e-9), np.inf)
        if hatch is None:
            tang = np.full(Wm.shape, np.nan)
            d_used = (D_min if D_min is not None else t_layer * 1e3) * (t_layer / 0.050)
            lof = Dm < d_used
        else:
            tang = np.where(Dm > 0, (hatch * 1e3 / np.maximum(Wm, 1e-9)) ** 2 + (t_layer * 1e3 / np.maximum(Dm, 1e-9)) ** 2, np.inf)
            lof = tang > 1.0
    keyhole = NH > KING_TH
    balling = LW > math.pi
    ok = ~lof & ~keyhole & ~balling
    return dict(P=P_grid, v=v_grid, W=Wm, D=Dm, L=Lm, NH=NH, Ke=Ke, tang=tang, LW=LW, lof=lof, keyhole=keyhole,
                balling=balling, ok=ok, T0=T0, t_layer=t_layer, hatch=hatch, A=A,
                D_min_used=(D_min if D_min is not None else t_layer * 1e3) * (t_layer / 0.050) if hatch is None else None)


def tang_value(W, D, H, t):
    return (H / W) ** 2 + (t / D) ** 2


def recommend(mat, A, D_min, w0=W0[5.0], v_cap=1.25):
    """Starting sets for each rung of the commissioning ladder (README section 2)."""
    rec = {}
    # rung 4, cubes at 200 C, 30 um: the hatch speed at the scanner's marking speed (1.27 m/s at f = 254.4); the
    # power that keeps King's number 25 % under 30; the widest hatch (0.01 mm steps) that keeps Tang's sum <= 0.6
    v = v_cap
    for P in np.arange(400.0, 99.0, -5.0):
        if king_enthalpy(mat, P, v, A, w0) <= 0.75 * KING_TH:
            break
    t = track(mat, P, v, A, 200.0, w0)
    t2 = track(mat, P, v, A, 25.0, w0)
    H_wide = math.floor(t["W_um"] * math.sqrt(max(0.6 - (30.0 / t["D_um"]) ** 2, 0.05)) / 10 + 1e-9) / 100.0
    H = math.floor(t2["W_um"] * math.sqrt(max(0.75 - (30.0 / t2["D_um"]) ** 2, 0.05)) / 10 + 1e-9) / 100.0
    H = min(H, H_wide)
    rec["cubes, 200 C, 30 um"] = dict(P=float(P), v=v, hatch=H, hatch_wide=H_wide, layer=0.030, T0=200.0, **t,
                                      NH=float(king_enthalpy(mat, P, v, A, w0)),
                                      Ke=float(keyhole_number(mat, P, v, A, 200.0, w0)),
                                      tang=tang_value(t["W_um"], t["D_um"], H * 1e3, 30.0),
                                      tang_wide=tang_value(t["W_um"], t["D_um"], H_wide * 1e3, 30.0),
                                      Ev_J_mm3=P / (v * 1e3 * H * 0.030))
    rec["cubes, 25 C, 30 um (same set)"] = dict(P=float(P), v=v, hatch=H, layer=0.030, T0=25.0, **t2,
                                                NH=float(king_enthalpy(mat, P, v, A, w0)),
                                                tang=tang_value(t2["W_um"], t2["D_um"], H * 1e3, 30.0),
                                                tang_wide=tang_value(t2["W_um"], t2["D_um"], H_wide * 1e3, 30.0))
    # the slower variant of the first build (cube C)
    ts = track(mat, P, 1.0, A, 200.0, w0)
    rec["cubes, 200 C, slower variant"] = dict(P=float(P), v=1.0, hatch=H, **ts, NH=float(king_enthalpy(mat, P, 1.0, A, w0)),
                                               tang=tang_value(ts["W_um"], ts["D_um"], H * 1e3, 30.0))
    tc = track(mat, 150.0, 0.8, A, 200.0, w0)
    rec["contour, 200 C"] = dict(P=150.0, v=0.8, **tc, NH=float(king_enthalpy(mat, 150.0, 0.8, A, w0)))
    # rung 1: bare 6061 plate at room temperature; flat Al absorbs ~0.05 (Boley 2016 ray tracing), bead-blasted more
    bare = []
    for Ab in (0.1, 0.2):
        for Pi in (100.0, 200.0, 300.0, 400.0):
            for vi in (0.25, 0.5, 1.0, 2.0):
                tb = track(AL6061, Pi, vi, Ab, 25.0, w0)
                bare.append(dict(A=Ab, P=Pi, v=vi, W_um=tb["W_um"], D_um=tb["D_um"]))
    rec["bare 6061 plate, 25 C"] = dict(rows=bare)
    # single tracks: a 5 x 5 matrix round the cube set
    for T0 in (25.0, 200.0):
        Ps = [P - 100, P - 50, P, P + 50, P + 100]
        vs = [round(x, 2) for x in (0.5 * v, 0.75 * v, v, 1.4 * v, 2.0 * v)]
        rows = []
        for Pi in Ps:
            for vi in vs:
                ti = track(mat, Pi, vi, A, T0, w0)
                nh = float(king_enthalpy(mat, Pi, vi, A, w0))
                rows.append(dict(P=float(Pi), v=vi, **ti, NH=nh, continuous=ti["D_um"] >= D_min, keyhole=nh > KING_TH))
        rec[f"single tracks, {T0:.0f} C, one 50 um layer"] = dict(P_list=Ps, v_list=vs, T0=T0, layer=0.050, rows=rows)
    return rec


def main():
    import time
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    t0 = time.time()
    cal = calibrate()
    A = cal["A"]
    print(f"calibration: A = {A:.3f} (all, rms log {cal['all']['rms_log']:.3f}); Bosio only {cal['Bosio 2019']['A']:.3f}; "
          f"D_min {cal['D_min']:.1f} um (unstable max {cal['D_unstable_max']:.1f}, stable min {cal['D_stable_min']:.1f})")
    rec = recommend(ALSI10MG, A, cal["D_min"])
    cube = rec["cubes, 200 C, 30 um"]
    maps = {
        "single tracks, 25 C, 50 um": pv_map(ALSI10MG, A, 25.0, 0.050, None, D_min=cal["D_min"]),
        "single tracks, 200 C, 50 um": pv_map(ALSI10MG, A, 200.0, 0.050, None, D_min=cal["D_min"]),
        f"cubes, 200 C, 30 um, hatch {cube['hatch']:.2f} mm": pv_map(ALSI10MG, A, 200.0, 0.030, cube["hatch"]),
        f"cubes, 200 C, 30 um, hatch {cube['hatch'] * 0.67:.3f} mm, 7.5 mm beam (51 um spot)":
            pv_map(ALSI10MG, A, 200.0, 0.030, cube["hatch"] * 0.67, w0=W0[7.5]),
    }
    band = {a: pv_map(ALSI10MG, a, 200.0, 0.030, cube["hatch"]) for a in (0.16, 0.25)}
    other = {}
    for m in (AL6061, AL7075):
        tt = track(m, cube["P"], cube["v"], A, 200.0)
        other[m.name] = dict(**tt, NH=float(king_enthalpy(m, cube["P"], cube["v"], A)),
                             tang=tang_value(tt["W_um"], tt["D_um"], cube["hatch"] * 1e3, 30.0))
    summary = {k: dict(window_cells=int(m["ok"].sum()), cells=int(m["ok"].size)) for k, m in maps.items()}
    res = dict(material=asdict(ALSI10MG), other_materials={m.name: asdict(m) for m in (AL6061, AL7075)},
               spot_w0_um={str(k): v * 1e6 for k, v in W0.items()}, calibration=cal, recommended=rec,
               at_cube_set_other_alloys=other, map_summary=summary, sources=DOI,
               criteria=dict(KING_TH=KING_TH, KE_COND=KE_COND, KE_TH=KE_TH, balling="L/W > pi"))
    (OUT / "process_window.json").write_text(json.dumps(res, indent=1, default=float))
    figure(maps, band, rec, cal)
    print(f"done in {time.time() - t0:.1f} s")
    for k, v in rec.items():
        if "rows" not in v:
            print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})
    print(other)
    return res


def figure(maps, band, rec, cal):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    C_LOF, C_KH, C_BALL = "#257de0", "#f47230", "#00b894"
    INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
    plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
    keys = list(maps)
    fig, axs = plt.subplots(2, 2, figsize=(11.5, 8.8), sharex=True, sharey=True)
    for ax, k in zip(axs.ravel(), keys):
        m = maps[k]
        V, P = np.meshgrid(m["v"], m["P"])
        if m["hatch"] is None:
            dlim = m["D_min_used"]
            ax.contourf(V, P, m["D"], levels=[-1.0, dlim], colors=[C_LOF], alpha=0.30)
        else:
            ax.contourf(V, P, np.nan_to_num(m["tang"], posinf=99.0), levels=[1.0, 1e9], colors=[C_LOF], alpha=0.30)
        ax.contourf(V, P, m["NH"], levels=[KING_TH, 1e9], colors=[C_KH], alpha=0.35)
        if m["balling"].any():
            ax.contourf(V, P, m["balling"].astype(float), levels=[0.5, 1.5], colors=[C_BALL], alpha=0.35)
        ax.contour(V, P, m["NH"], levels=[26, 34], colors=[C_KH], linestyles=":", linewidths=1.0)
        cd = ax.contour(V, P, m["D"], levels=[40, 60, 80, 100, 150], colors=INK2, linewidths=0.6)
        ax.clabel(cd, fmt=lambda x: f"D {x:.0f}", fontsize=6.5)
        cw = ax.contour(V, P, m["W"], levels=[100, 150, 200, 250], colors=INK2, linewidths=0.6, linestyles="--")
        ax.clabel(cw, fmt=lambda x: f"W {x:.0f}", fontsize=6.5)
        if "hatch" in k and "7.5" not in k:
            for a, mb in band.items():
                ax.contour(V, P, mb["lof"].astype(float), levels=[0.5], colors=[C_LOF], linewidths=0.8, linestyles=":")
        ax.set_title(k, fontsize=9.5, color=INK, loc="left")
        ax.grid(color=GRID, lw=0.5)
        ax.text(0.15, 390, "keyhole (King ΔH/h_s > 30)", color=INK, fontsize=7.5, va="top")
        ax.text(2.95, 108, "lack of fusion (Tang)" if m["hatch"] is not None else "pool too shallow: tracks break up",
                color=INK, fontsize=7.5, ha="right")
    c = rec["cubes, 200 C, 30 um"]
    for ax, k in zip(axs.ravel(), keys):
        if k.startswith("cubes") and "7.5" not in k:
            ax.plot(c["v"], c["P"], "o", ms=8, mfc=INK, mec="white", mew=1.5)
            ax.annotate(f"cube set: {c['P']:.0f} W, {c['v']:.2f} m/s,\nhatch {c['hatch']:.2f} mm", (c["v"], c["P"]),
                        xytext=(12, -22), textcoords="offset points", fontsize=7.5, color=INK)
        if k.startswith("single"):
            T0 = 25 if "25 C" in k else 200
            r = rec[f"single tracks, {T0} C, one 50 um layer"]
            vv, pp = np.meshgrid(r["v_list"], r["P_list"])
            ax.plot(vv.ravel(), pp.ravel(), "s", ms=4.5, mfc="white", mec=INK, mew=1.0)
            ax.text(r["v_list"][-1] + 0.06, r["P_list"][-1] - 6, "5 x 5 track matrix", fontsize=7.5, color=INK, va="top")
    for ax in axs[1]:
        ax.set_xlabel("scan speed v (m/s)")
    for ax in axs[:, 0]:
        ax.set_ylabel("laser power P (W)")
    handles = [Patch(fc=C_LOF, alpha=0.3, label="lack of fusion (Tang 2017) or pool too shallow for the layer"),
               Patch(fc=C_KH, alpha=0.35, label="keyhole (King 2014 ΔH/h_s > 30; dotted 26 and 34)"),
               Patch(fc="white", ec=INK2, label="process window")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8)
    fig.suptitle(f"AlSi10Mg, 76 um spot (5 mm beam, f = 254.4 mm) unless noted. Eagar-Tsai, A = {cal['A']:.2f} fitted to "
                 f"published tracks\n(dotted blue: lack-of-fusion edge at A 0.16 and 0.25). Contours: pool depth D and "
                 f"width W in um", fontsize=9, color=INK, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(IMG / "pv-map.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
