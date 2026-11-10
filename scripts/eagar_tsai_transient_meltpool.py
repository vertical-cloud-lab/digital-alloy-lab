"""Time-dependent eagar-tsai melt pools, drawn like the Thermo-Calc AM module's 3D renders (#235).

Thermo-Calc's account manager sent us two AM-module melt-pool renders (on the ``consolidation-2``
branch, ``figures/thermo-calc-am-module-prelim-results/``): AlSi10Mg at 250 W / 900 mm/s and the
BYU AA1100+Si+AlSi10Mg blend at 375 W / 400 mm/s. Each is a half-domain cut through the track
centre line, coloured by temperature, with the heat-source intensity drawn as a Gaussian above
the beam, the Marangoni velocity field as arrows, and the pool outline as contour lines.

ArroyaveLab/eagar-tsai only returns the quasi-steady field, and only on the surface (z = 0) and
centre-line (y = 0) planes, which are exactly the two faces those renders show. Its temperature
is an integral over the time since each bit of heat was deposited,

    T - T0 = S * integral_0^inf f(t; x, y, z, p) dt,   t = v * (elapsed time) / sigma,

with f the package's own compiled integrand (``eagar_tsai._core._INTEGRAND``). Integrating over
the part of that history when the beam was actually on gives the transient for a beam that
switches on at X = 0, runs along +X at speed v, and switches off at X = L_track:

    beam on  (tau <= tau_off):  t from 0                       to v * tau / sigma
    beam off (tau >  tau_off):  t from v * (tau - tau_off) / sigma  to v * tau / sigma

with x = (v * tau - X) / sigma measured from where the beam would be at time tau. Nothing else
in the model changes: same Gaussian source, constant properties, no latent heat, no fluid flow,
no evaporation, semi-infinite substrate. As tau grows the field converges to the package's
steady state; ``check`` verifies that against ``compute_single_point``.

eagar-tsai fixes the ambient temperature at 298 K. The field is linear in T - T0, so the build
plate temperature is simply used as T0 here (423 K for AlSi10Mg, 303 K for the blend, as in the
AM-module runs). Settings (beam radius, absorptivity read off the AM render's heat-source colour
bar, properties, isotherms) are the ones ``eagar_tsai_vs_am_module_inhouse.py`` uses.

Subcommands::

    python scripts/eagar_tsai_transient_meltpool.py check    --out <dir>   # transient -> steady
    python scripts/eagar_tsai_transient_meltpool.py history  --out <dir>   # W, D, L, peak T vs time
    python scripts/eagar_tsai_transient_meltpool.py replot   --out <dir>   # redraw that from its CSV
    python scripts/eagar_tsai_transient_meltpool.py render   --out <dir> --am-png-dir <dir>
    python scripts/eagar_tsai_transient_meltpool.py animate  --out <dir>
    python scripts/eagar_tsai_transient_meltpool.py all      --out <dir> --am-png-dir <dir>

``--am-png-dir`` must hold the two AM-module renders::

    git show origin/consolidation-2:figures/thermo-calc-am-module-prelim-results/AlSi10Mg-meltpool-250W-900mms.png > ...
    git show origin/consolidation-2:figures/thermo-calc-am-module-prelim-results/BYUMix-meltpool-375W-400mms.png > ...
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib

matplotlib.use("Agg")
import contourpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from PIL import Image
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

from eagar_tsai import BeamParameters, MaterialProperties, SimulationDomain, compute_single_point
from eagar_tsai._core import _INTEGRAND, eagar_tsai_integrand

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from eagar_tsai_vs_am_module_inhouse import MAPS, MATERIALS, MELT_POOLS, T0_ET, inferred_absorptivity  # noqa: E402

# --------------------------------------------------------------------------------------------
# The two AM-module renders and the matching eagar-tsai set-up
# --------------------------------------------------------------------------------------------
_MAT = MATERIALS["alsi10mg"][0]  # k, rho, cp (Edison AlSi10Mg values; the blend has none of its own)

CASES = {
    "alsi10mg": dict(
        title="AlSi10Mg, 250 W, 900 mm/s",
        am_png="AlSi10Mg-meltpool-250W-900mms.png",
        unit="K",
        # isotherms: (temperature in K, label, line style); the first is the pool edge used for W, D, L
        isotherms=[(867.0, "liquidus 867 K", "-"), (842.7, "solidus 843 K", "--")],
        track_mm=1.2,
        # lab-frame window for the animation: X (mm, along the scan), Y (mm, half-width), Z (mm, depth)
        window=dict(x=(-0.15, 1.45), y=0.30, z=0.22),
        dx_um=5.0,
    ),
    "byu-blend": dict(
        title="BYU blend (Al-24.3Si-0.14Mg), 375 W, 400 mm/s",
        am_png="BYUMix-meltpool-375W-400mms.png",
        unit="C",
        isotherms=[(1019.3, "liquidus 1019 K", "-"), (850.0, "eutectic 850 K", "--")],
        track_mm=2.0,
        window=dict(x=(-0.2, 2.3), y=0.36, z=0.40),
        dx_um=7.0,
    ),
}
for _key, _c in CASES.items():
    _mp = MELT_POOLS[_key]
    _c.update(
        P=_mp["P"],
        v=_mp["v_mm_s"] * 1e-3,
        R_um=MAPS[_key]["beam_radius_um"],
        T_plate=MAPS[_key]["preheat_C"] + 273.15,
        A=inferred_absorptivity(_mp, MAPS[_key]["beam_radius_um"]),
        am_T_range_K=(_mp["T_min_K"], _mp["T_peak_K"]),
        am_q_range=(_mp["q_min_W_mm2"], _mp["q_peak_W_mm2"]),
        am_dims_um=dict(L=_mp["L_um"], half_W=_mp["y_extent_um"], D=_mp["D_um"]) if "L_um" in _mp else None,
        k=_MAT["k"],
        rho=_MAT["rho"],
        cp=_MAT["cp"],
    )

# The AM module's temperature colour bar, sampled off its render: an even blue-cyan-green-yellow-red
# rainbow. Its heat-source colour bar is matplotlib's plasma (end colours match to within 2/255).
AM_RAINBOW = LinearSegmentedColormap.from_list(
    "am_rainbow", [(0.0, (0, 0.03, 1)), (0.25, (0, 1, 1)), (0.5, (0, 1, 0)), (0.75, (1, 1, 0)), (1.0, (1, 0.03, 0))]
)
AM_HEAT = plt.get_cmap("plasma")
BG = "#0000c6"  # the AM renders' background blue (0, 0, 198)


# --------------------------------------------------------------------------------------------
# Transient eagar-tsai
# --------------------------------------------------------------------------------------------
class Model:
    """eagar-tsai's scalings for one case, from the package's own BeamParameters/MaterialProperties."""

    def __init__(self, c: dict):
        self.c = c
        self.beam = BeamParameters(beam_diameter=c["R_um"] * 1e-6, power=c["P"], velocity=c["v"], absorptivity=c["A"])
        self.mat = MaterialProperties(
            liquidus_temperature=c["isotherms"][0][0], thermal_conductivity=c["k"], density=c["rho"], specific_heat=c["cp"]
        )
        a, s, v = self.mat.thermal_diffusivity, self.beam.sigma, self.beam.velocity
        self.alpha, self.sigma, self.v = a, s, v
        self.p = a / (v * s)
        self.z_scale = math.sqrt(a * s / v)
        self.S = self.beam.absorptivity * self.beam.power / (
            math.pi * (self.mat.thermal_conductivity / a) * math.sqrt(math.pi * a * v * s**3)
        )
        self.T0 = c["T_plate"]
        self.tau_off = c["track_mm"] * 1e-3 / v  # s
        self.t_unit = s / v  # seconds per unit of eagar-tsai's dimensionless time
        # absorbed peak intensity of eagar-tsai's Gaussian, q0 = A P / (pi sigma^2) = 2 A P / (pi R^2)
        self.q0_W_mm2 = c["A"] * c["P"] / (math.pi * (s * 1e3) ** 2)

    def limits(self, tau: float | None) -> tuple[float, float]:
        """Integration window in eagar-tsai's dimensionless time; tau=None is the steady state."""
        if tau is None:
            return 0.0, math.inf
        t_hi = self.v * tau / self.sigma
        t_lo = max(0.0, self.v * (tau - self.tau_off) / self.sigma)
        return t_lo, t_hi

    def integral(self, x_nd: float, y_nd: float, z_nd: float, t_lo: float, t_hi: float) -> float:
        if t_hi <= t_lo:
            return 0.0
        args = (x_nd, y_nd, z_nd, self.p)
        if math.isinf(t_hi):
            res = quad(_INTEGRAND, t_lo, t_hi, args=args, limit=200, full_output=1)
        else:
            # point QUADPACK at the integrand's peak (heat deposited x_nd ago sits under this point)
            pts = [x_nd] if t_lo + 1e-3 < x_nd < t_hi - 1e-3 and x_nd > 1.0 else None
            res = quad(_INTEGRAND, t_lo, t_hi, args=args, points=pts, limit=200, full_output=1)
        if len(res) == 3:  # converged (a 4th element is QUADPACK's warning message)
            return res[0]
        # rare fallback: substitute t = u^2, which removes the 1/sqrt(t) end-point singularity
        u_hi = math.sqrt(t_hi) if math.isfinite(t_hi) else math.inf
        return quad(lambda u: 2.0 * u * eagar_tsai_integrand(u * u, *args) if u > 0 else
                    2.0 * math.exp(-(y_nd * y_nd + x_nd * x_nd)) * (z_nd == 0.0),
                    math.sqrt(t_lo), u_hi, limit=500)[0]

    def beam_x(self, tau: float | None) -> float:
        """Where the beam is (or would be, after turn-off), in metres along X."""
        return 0.0 if tau is None else self.v * tau

    def planes(self, tau: float | None, X: np.ndarray, Y: np.ndarray, Zd: np.ndarray, xb: float | None = None):
        """Temperature (K) on the surface plane (Y x X) and the centre-line plane (Zd x X).

        X, Y, Zd in metres; Zd is depth (>= 0). For the steady state (tau=None) X is measured from
        the beam centre along the scan direction (beam at X = 0, pool trailing into X < 0).
        """
        t_lo, t_hi = self.limits(tau)
        xb = self.beam_x(tau) if xb is None else xb
        T_top = np.empty((Y.size, X.size))
        T_side = np.empty((Zd.size, X.size))
        for ix, Xi in enumerate(X):
            x_nd = (xb - Xi) / self.sigma
            for iy, Yi in enumerate(Y):
                T_top[iy, ix] = self.integral(x_nd, Yi / self.sigma, 0.0, t_lo, t_hi)
            T_side[0, ix] = T_top[0, ix]
            for iz in range(1, Zd.size):
                T_side[iz, ix] = self.integral(x_nd, 0.0, Zd[iz] / self.z_scale, t_lo, t_hi)
        return self.T0 + self.S * T_top, self.T0 + self.S * T_side

    def peak(self, tau: float | None, X_guess: float, xb: float | None = None) -> tuple[float, float]:
        """Peak surface temperature (K) on the centre line and where it is, refined off the grid."""
        t_lo, t_hi = self.limits(tau)
        xb = self.beam_x(tau) if xb is None else xb

        def neg(Xm):
            return -self.integral((xb - Xm) / self.sigma, 0.0, 0.0, t_lo, t_hi)

        h = 2.0 * self.sigma
        r = minimize_scalar(neg, bounds=(X_guess - h, X_guess + h), method="bounded", options=dict(xatol=1e-8))
        return self.T0 - self.S * r.fun, float(r.x)


def _crossing_extent(coord: np.ndarray, T: np.ndarray, level: float) -> float:
    """Largest coordinate where T > level, linearly interpolated (coord[0] must be inside)."""
    inside = np.where(T > level)[0]
    if inside.size == 0:
        return 0.0
    i = inside[-1]
    if i + 1 >= coord.size:
        return float(coord[-1])
    return float(coord[i] + (T[i] - level) / (T[i] - T[i + 1]) * (coord[i + 1] - coord[i]))


def pool_dims(X, Y, Zd, T_top, T_side, level) -> dict:
    """Pool length, width (2 x half-width) and depth in um from the two planes, interpolated."""
    cl = T_top[0]
    inside = np.where(cl > level)[0]
    if inside.size == 0:
        return dict(L_um=0.0, W_um=0.0, D_um=0.0, x_front_um=np.nan, x_back_um=np.nan, touches_window_edge=False)
    i0, i1 = inside[0], inside[-1]
    x_back = X[i0] if i0 == 0 else X[i0 - 1] + (level - cl[i0 - 1]) / (cl[i0] - cl[i0 - 1]) * (X[i0] - X[i0 - 1])
    x_front = X[i1] if i1 + 1 >= X.size else X[i1] + (cl[i1] - level) / (cl[i1] - cl[i1 + 1]) * (X[i1 + 1] - X[i1])
    cols = np.where((T_top > level).any(axis=0))[0]
    half_w = max(_crossing_extent(Y, T_top[:, j], level) for j in cols)
    cols = np.where((T_side > level).any(axis=0))[0]
    depth = max(_crossing_extent(Zd, T_side[:, j], level) for j in cols) if cols.size else 0.0
    touches = bool(i0 == 0 or i1 == X.size - 1 or (T_top[-1] > level).any() or (T_side[-1] > level).any())
    return dict(L_um=(x_front - x_back) * 1e6, W_um=2 * half_w * 1e6, D_um=depth * 1e6,
                x_front_um=x_front * 1e6, x_back_um=x_back * 1e6, touches_window_edge=touches)


def _grid(lo, hi, d):
    n = int(round((hi - lo) / d)) + 1
    return np.linspace(lo, hi, n)


# --------------------------------------------------------------------------------------------
# check: long-time transient -> eagar-tsai's own steady state
# --------------------------------------------------------------------------------------------
def check(out: pathlib.Path) -> pd.DataFrame:
    rows = []
    for key, c in CASES.items():
        m = Model(c)
        m.tau_off = math.inf  # beam stays on: the start-up transient only
        # this script: steady (t -> inf) and the field tau after switch-on, beam at X = 0, 2 um grid
        X = _grid(-1.1e-3, 0.12e-3, 2e-6)
        Y = _grid(0, 0.26e-3, 2e-6)
        Zd = _grid(0, 0.22e-3, 2e-6)
        fields = {}
        for n in (None, 10, 20, 50, 100, 200):
            tau = None if n is None else n * m.t_unit
            t0 = time.time()
            fields[n] = (m.planes(tau, X, Y, Zd, xb=0.0), time.time() - t0)
        for T_iso, label, _ in c["isotherms"]:
            # the package's own steady state, 1 um grid; its T0 is 298 K, so shift the isotherm by the preheat
            mat = MaterialProperties(liquidus_temperature=T_iso - (c["T_plate"] - T0_ET), thermal_conductivity=c["k"],
                                     density=c["rho"], specific_heat=c["cp"])
            t0 = time.time()
            r = compute_single_point(m.beam, mat, SimulationDomain(x_length_um=600, y_length_um=250, z_depth_um=250,
                                                                   spatial_resolution_um=1.0))
            rows.append(dict(case=key, isotherm=label, source="eagar-tsai compute_single_point, steady, 1 um grid",
                             tau_us=np.inf, L_um=r.length * 1e6, W_um=r.width * 1e6, D_um=r.depth * 1e6,
                             peak_K=r.peak_temperature + c["T_plate"] - T0_ET, seconds=time.time() - t0))
            for n, ((Tt, Ts), secs) in fields.items():
                tau = None if n is None else n * m.t_unit
                d = pool_dims(X, Y, Zd, Tt, Ts, T_iso)
                pk, _ = m.peak(tau, X[np.argmax(Tt[0])], xb=0.0)
                rows.append(dict(case=key, isotherm=label,
                                 source="this script, steady (t to inf), 2 um grid" if n is None
                                 else f"this script, {n} sigma/v after switch-on, 2 um grid",
                                 tau_us=np.inf if n is None else tau * 1e6, L_um=d["L_um"], W_um=d["W_um"], D_um=d["D_um"],
                                 peak_K=pk, seconds=secs))
    df = pd.DataFrame(rows)
    out.mkdir(parents=True, exist_ok=True)
    df.round(3).to_csv(out / "transient-check-vs-compute_single_point.csv", index=False)
    print(df.round(2).to_string())
    return df


# --------------------------------------------------------------------------------------------
# history: W, D, L and peak T vs time along one track (beam on, then off)
# --------------------------------------------------------------------------------------------
def _history_one(args):
    key, tau, dx = args
    c = CASES[key]
    m = Model(c)
    xb_eff = m.v * min(tau, m.tau_off)
    X = _grid(xb_eff - 0.75e-3, xb_eff + 0.2e-3, dx)
    X = X[X >= -0.1e-3]
    Y = _grid(0, 0.26e-3, dx)
    Zd = _grid(0, 0.22e-3, dx)
    Tt, Ts = m.planes(tau, X, Y, Zd)
    row = dict(case=key, tau_us=tau * 1e6, beam_on=tau <= m.tau_off, beam_x_mm=m.v * tau * 1e3)
    j = int(np.argmax(Tt[0]))
    pk, xpk = m.peak(tau, X[j])
    row.update(peak_K=pk, peak_x_mm=xpk * 1e3)
    for T_iso, label, _ in c["isotherms"]:
        d = pool_dims(X, Y, Zd, Tt, Ts, T_iso)
        tag = label.split()[0]
        row.update({f"{k}_{tag}": v for k, v in d.items()})
    return row


def history(out: pathlib.Path, workers: int = 4) -> pd.DataFrame:
    jobs = []
    for key, c in CASES.items():
        m = Model(c)
        t_end = m.tau_off * 1.0
        taus = list(np.geomspace(1e-6, t_end / 120, 8)[:-1]) + list(np.linspace(0, t_end, 121)[1:])
        # after turn-off, until the pool has frozen (it takes about 0.1 ms for AlSi10Mg, 0.3 ms for the blend)
        taus += list(t_end + np.linspace(0, 0.6e-3 if key == "byu-blend" else 0.25e-3, 61)[1:])
        jobs += [(key, float(t), 2e-6) for t in taus]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(_history_one, jobs, chunksize=4))
    df = pd.DataFrame(rows)
    out.mkdir(parents=True, exist_ok=True)
    df.round(3).to_csv(out / "eagar-tsai-transient-history.csv", index=False)
    return df


def summarize_history(df: pd.DataFrame, steady: dict) -> dict:
    """Times to reach the steady pool after switch-on, and to freeze after switch-off."""
    res = {}
    for key, c in CASES.items():
        m = Model(c)
        d = df[df.case == key].sort_values("tau_us")
        on, off = d[d.beam_on], d[~d.beam_on]
        r = dict(track_mm=c["track_mm"], beam_on_us=round(m.tau_off * 1e6, 1), sigma_over_v_us=round(m.t_unit * 1e6, 2))
        tag = c["isotherms"][0][1].split()[0]
        for s_ in ("L", "W", "D"):
            y = on[f"{s_}_um_{tag}"].to_numpy()
            for frac in (0.9, 0.95, 0.99):
                k = np.argmax(y >= frac * steady[key][s_])
                r[f"{s_}_{int(frac * 100)}pct_after_us"] = round(float(on.tau_us.iloc[k]), 1) if y[k] >= frac * steady[key][s_] else None
                if frac == 0.95:
                    r[f"{s_}_95pct_track_mm"] = round(float(on.beam_x_mm.iloc[k]), 3)
        for T_iso, label, _ in c["isotherms"]:
            t_ = label.split()[0]
            z = off[off[f"L_um_{t_}"] == 0]
            r[f"frozen_at_{t_}_us_after_off"] = round(float(z.tau_us.iloc[0] - m.tau_off * 1e6), 1) if len(z) else None
        b = off[off.peak_K < 2743.0]
        r["peak_below_boiling_us_after_off"] = round(float(b.tau_us.iloc[0] - m.tau_off * 1e6), 1) if len(b) else None
        r["peak_K_at_first_sample"] = [round(float(on.tau_us.iloc[0]), 2), round(float(on.peak_K.iloc[0]), 0)]
        r["any_pool_touching_window_edge"] = bool(d.filter(like="touches_window_edge").fillna(False).astype(bool).any().any())
        res[key] = r
    return res


def plot_history(df: pd.DataFrame, steady: dict, out: pathlib.Path):
    """Start-up (time since switch-on), cool-down (time since switch-off) and peak temperature."""
    ink, ink2, surf = "#0b0b0b", "#52514e", "#fcfcfb"
    series = [("L", "length L", "#2a78d6"), ("W", "width W", "#eb6834"), ("D", "depth D", "#1baf7a")]
    fig, axes = plt.subplots(3, 2, figsize=(11, 10.5), gridspec_kw=dict(height_ratios=[1.3, 1.0, 0.9]))
    fig.patch.set_facecolor(surf)
    for j, (key, c) in enumerate(CASES.items()):
        m = Model(c)
        d = df[df.case == key].sort_values("tau_us")
        tag = c["isotherms"][0][1].split()[0]
        on = d[d.beam_on]
        off = d[~d.beam_on]
        t_on = np.r_[0.0, on.tau_us.to_numpy()] / 1e3  # ms since switch-on; the pool starts from nothing
        t_off = np.r_[0.0, off.tau_us.to_numpy() - m.tau_off * 1e6]  # us since switch-off
        ax, axc, axT = axes[0, j], axes[1, j], axes[2, j]
        for s_, lab, col in series:
            ss = steady[key][s_]
            y_on = np.r_[0.0, on[f"{s_}_um_{tag}"].to_numpy()]
            y_off = np.r_[on[f"{s_}_um_{tag}"].to_numpy()[-1], off[f"{s_}_um_{tag}"].to_numpy()]
            ax.plot(t_on, y_on, color=col, lw=2, label=lab)
            ax.axhline(ss, color=col, lw=1, ls=":")
            ax.annotate(f"steady {ss:.0f} µm", (0.55 * t_on[-1], ss), xytext=(0, 3), textcoords="offset points",
                        ha="left", va="bottom", fontsize=8.5, color=ink2)
            axc.plot(t_off, y_off, color=col, lw=2, label=lab)
        ax.set_title(c["title"], fontsize=11, color=ink, loc="left")
        ax.set_ylabel(f"pool at the {c['isotherms'][0][1]} (µm)", color=ink2)
        ax.set_xlabel("time since the beam switched on (ms)", color=ink2)
        ax.legend(frameon=False, fontsize=9, loc="lower center", ncols=3)
        axc.set_ylabel(f"pool at the {c['isotherms'][0][1]} (µm)", color=ink2)
        axc.set_xlabel(f"time since the beam switched off at {c['track_mm']:.1f} mm (µs)", color=ink2)
        axc.legend(frameon=False, fontsize=9, loc="lower left")
        frozen = off[off[f"L_um_{c['isotherms'][1][1].split()[0]}"] == 0]
        if len(frozen):
            tf = frozen.tau_us.iloc[0] - m.tau_off * 1e6
            axc.axvline(tf, color=ink2, lw=1, ls="--")
            axc.annotate(f"everything below the\n{c['isotherms'][1][1]} by {tf:.0f} µs", (tf, axc.get_ylim()[1] * 0.97),
                         xytext=(4, 0), textcoords="offset points", ha="left", va="top", fontsize=8.5, color=ink2)
            axc.set_xlim(right=min(t_off[-1], 1.6 * tf))
        tt = np.r_[on.tau_us.to_numpy(), off.tau_us.to_numpy()] / 1e3
        axT.plot(tt, np.r_[on.peak_K.to_numpy(), off.peak_K.to_numpy()], color="#e34948", lw=2)
        for val, lab, ls in ((c["am_T_range_K"][1], f"AM-module peak {c['am_T_range_K'][1]:.0f} K", "--"),
                             (2743.0, "Al boils 2743 K", ":")):
            axT.axhline(val, color=ink2, lw=1, ls=ls)
            axT.annotate(lab, (0.3 * tt[-1], val), xytext=(0, 3 if ls == "--" else -3), textcoords="offset points",
                         ha="left", va="bottom" if ls == "--" else "top", fontsize=8.5, color=ink2)
        axT.axvline(m.tau_off * 1e3, color=ink2, lw=1)
        axT.annotate("beam off", (m.tau_off * 1e3, axT.get_ylim()[1]), xytext=(-4, -4), textcoords="offset points",
                     ha="right", va="top", fontsize=8.5, color=ink2)
        axT.set_ylabel("eagar-tsai peak surface T (K)", color=ink2)
        axT.set_xlabel("time since the beam switched on (ms)", color=ink2)
        for a_ in (ax, axc, axT):
            a_.set_facecolor(surf)
            for sp in ("top", "right"):
                a_.spines[sp].set_visible(False)
            a_.tick_params(colors=ink2)
            a_.grid(alpha=0.25, lw=0.6)
            a_.set_ylim(bottom=0)
    fig.suptitle("eagar-tsai along one track: start-up after the beam switches on, cool-down after it switches off",
                 fontsize=11.5, color=ink, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(out / "eagar-tsai-transient-history.png", dpi=130, facecolor=surf)
    plt.close(fig)


# --------------------------------------------------------------------------------------------
# AM-style 3D render
# --------------------------------------------------------------------------------------------
def _to_unit(T_K, unit):
    return T_K - 273.15 if unit == "C" else T_K


def _quads_xy(X, Y, z=0.0):
    Xg, Yg = np.meshgrid(X, Y)
    v00 = np.stack([Xg[:-1, :-1], Yg[:-1, :-1], np.full_like(Xg[:-1, :-1], z)], -1)
    v10 = np.stack([Xg[:-1, 1:], Yg[:-1, 1:], np.full_like(Xg[:-1, 1:], z)], -1)
    v11 = np.stack([Xg[1:, 1:], Yg[1:, 1:], np.full_like(Xg[1:, 1:], z)], -1)
    v01 = np.stack([Xg[1:, :-1], Yg[1:, :-1], np.full_like(Xg[1:, :-1], z)], -1)
    return np.stack([v00, v10, v11, v01], -2).reshape(-1, 4, 3)


def _quads_xz(X, Z):
    Xg, Zg = np.meshgrid(X, Z)
    zero = np.zeros_like(Xg[:-1, :-1])
    v00 = np.stack([Xg[:-1, :-1], zero, Zg[:-1, :-1]], -1)
    v10 = np.stack([Xg[:-1, 1:], zero, Zg[:-1, 1:]], -1)
    v11 = np.stack([Xg[1:, 1:], zero, Zg[1:, 1:]], -1)
    v01 = np.stack([Xg[1:, :-1], zero, Zg[1:, :-1]], -1)
    return np.stack([v00, v10, v11, v01], -2).reshape(-1, 4, 3)


def _cell_mean(F):
    return 0.25 * (F[:-1, :-1] + F[1:, :-1] + F[:-1, 1:] + F[1:, 1:])


def draw_scene(ax, m: Model, X, Y, Zd, T_top, T_side, beam_X, *, show_beam=True, rulers=None, am_rulers=None,
               src_height_mm=None, label_size=9, elev=22, azim=-112, zoom=1.0):
    """Draw one AM-style half-domain scene in mm. X, Y, Zd in metres; beam_X in metres or None."""
    c = m.c
    ax.computed_zorder = False  # planes, then pool outlines, then the heat source, then rulers
    unit = c["unit"]
    lo, hi = (_to_unit(T, unit) for T in c["am_T_range_K"])
    norm = Normalize(lo, hi)
    Xm, Ym, Zm = X * 1e3, Y * 1e3, -Zd * 1e3
    top = _quads_xy(Xm, Ym)
    fc_top = AM_RAINBOW(norm(_to_unit(_cell_mean(T_top), unit)).clip(0, 1)).reshape(-1, 4)
    side = _quads_xz(Xm, Zm)
    fc_side = AM_RAINBOW(norm(_to_unit(_cell_mean(T_side), unit)).clip(0, 1)).reshape(-1, 4)
    pc = Poly3DCollection(np.concatenate([top, side]), facecolors=np.concatenate([fc_top, fc_side]),
                          edgecolors=np.concatenate([fc_top, fc_side]), linewidths=0.25)
    pc.set_zorder(1)
    ax.add_collection3d(pc)

    # faint outline of the two faces, so the geometry reads where both are at the plate temperature
    x0, x1, y1, z1 = Xm.min(), Xm.max(), Ym.max(), Zm.min()
    edges = [[(x0, 0, 0), (x1, 0, 0)], [(x0, y1, 0), (x1, y1, 0)], [(x0, 0, z1), (x1, 0, z1)],
             [(x0, 0, 0), (x0, y1, 0)], [(x1, 0, 0), (x1, y1, 0)], [(x0, 0, 0), (x0, 0, z1)], [(x1, 0, 0), (x1, 0, z1)]]
    oc = Line3DCollection(edges, colors=[(1, 1, 1, 0.45)], linewidths=0.7)
    oc.set_zorder(2)
    ax.add_collection3d(oc)

    # pool outline(s): isotherm contours on both faces
    segs, styles = [], []
    for T_iso, _label, ls in c["isotherms"]:
        g = contourpy.contour_generator(x=Xm, y=Ym, z=T_top)
        for line in g.lines(T_iso):
            segs.append(np.column_stack([line[:, 0], line[:, 1], np.zeros(len(line))]))
            styles.append(ls)
        g = contourpy.contour_generator(x=Xm, y=Zm, z=T_side)
        for line in g.lines(T_iso):
            segs.append(np.column_stack([line[:, 0], np.zeros(len(line)), line[:, 1]]))
            styles.append(ls)
    for ls in ("-", "--"):
        s = [seg for seg, st in zip(segs, styles) if st == ls]
        if s:
            lc = Line3DCollection(s, colors="white", linewidths=1.1 if ls == "-" else 0.9,
                                  linestyles="solid" if ls == "-" else (0, (3, 2)))
            lc.set_zorder(2)
            ax.add_collection3d(lc)

    # heat source: the absorbed Gaussian out to the 1/e^2 radius, as in the AM renders
    zmax = Zm.min()
    h = src_height_mm if src_height_mm is not None else 0.55 * abs(zmax)
    if show_beam and beam_X is not None:
        R = c["R_um"] * 1e-3
        r = np.linspace(0, R, 18)
        th = np.linspace(0, 2 * np.pi, 49)
        rr, tt = np.meshgrid(r, th)
        qn = np.exp(-2 * rr**2 / R**2)  # q/q0
        xs = beam_X * 1e3 + rr * np.cos(tt)
        ys = rr * np.sin(tt)
        zs = h * qn
        q = m.q0_W_mm2 * qn
        qlo, qhi = c["am_q_range"]
        verts = np.stack([np.stack([xs[:-1, :-1], ys[:-1, :-1], zs[:-1, :-1]], -1),
                          np.stack([xs[:-1, 1:], ys[:-1, 1:], zs[:-1, 1:]], -1),
                          np.stack([xs[1:, 1:], ys[1:, 1:], zs[1:, 1:]], -1),
                          np.stack([xs[1:, :-1], ys[1:, :-1], zs[1:, :-1]], -1)], -2).reshape(-1, 4, 3)
        fq = AM_HEAT(Normalize(qlo, qhi)(_cell_mean(q)).clip(0, 1)).reshape(-1, 4)
        bell = Poly3DCollection(verts, facecolors=fq, edgecolors=fq, linewidths=0.2)
        bell.set_zorder(3)
        ax.add_collection3d(bell)

    def ruler(p0, p1, text, colour, ls="-", off=(0, 0, 0), ha="center"):
        ax.plot(*zip(p0, p1), color=colour, lw=1.4, ls=ls, zorder=4)
        mid = [(a + b) / 2 + o for a, b, o in zip(p0, p1, off)]
        ax.text(*mid, text, color=colour, fontsize=label_size, ha=ha, va="center", zorder=5, fontstyle="italic")

    if rulers:  # eagar-tsai's own pool, from its tail corner, like the AM module's axis rulers
        xb, L, hw, D = rulers
        ruler((xb, 0, 0), (xb + L, 0, 0), f"{L:.3f} mm", "yellow", off=(0, 0, 0.02 * abs(zmax) + 0.01))
        ruler((xb, 0, 0), (xb, hw, 0), f"{hw:.3f} mm", "yellow", off=(-0.05, 0, 0), ha="right")
        ruler((xb, 0, 0), (xb, 0, -D), f"{D:.3f} mm", "yellow", off=(-0.02, 0, 0), ha="right")
    if am_rulers:  # the AM module's pool, for scale, drawn from the same beam position
        xf, L, hw, D = am_rulers
        mag = "#ff66ff"
        ruler((xf - L, 0, 0), (xf, 0, 0), "", mag, ls=(0, (4, 2)))
        ruler((xf - L, 0, 0), (xf - L, hw, 0), f"AM {hw:.3f} mm", mag, ls=(0, (4, 2)), off=(-0.04, 0, 0.0), ha="right")
        ruler((xf - L, 0, 0), (xf - L, 0, -D), f"AM {D:.3f} mm", mag, ls=(0, (4, 2)), off=(-0.03, 0, 0), ha="right")
        ax.text(xf - 0.62 * L, 0, 0.03 * abs(Zd.max() * 1e3) + 0.012, f"AM {L:.3f} mm", color=mag, fontsize=label_size,
                ha="center", va="bottom", zorder=5, fontstyle="italic")

    ax.set_xlim(Xm.min(), Xm.max())
    ax.set_ylim(0, Ym.max())
    ax.set_zlim(zmax, h * 1.05)
    ax.set_box_aspect((Xm.max() - Xm.min(), Ym.max(), h * 1.05 - zmax), zoom=zoom)
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type("persp", focal_length=2.0)
    ax.set_axis_off()
    ax.set_facecolor(BG)
    # mplot3d draws into a square box; let the (wide) scene spill out of it instead of being clipped
    for art in [*ax.collections, *ax.lines, *ax.texts]:
        art.set_clip_on(False)
    return norm


def _colourbars(fig, m: Model, rect_T, rect_q):
    c = m.c
    unit = c["unit"]
    lo, hi = (_to_unit(T, unit) for T in c["am_T_range_K"])
    for rect, cmap, (a, b), lab in ((rect_T, AM_RAINBOW, (lo, hi), f"Temperature ({'K' if unit == 'K' else '°C'})"),
                                   (rect_q, AM_HEAT, c["am_q_range"], "Heat source intensity (W/mm²)")):
        cax = fig.add_axes(rect)
        cb = fig.colorbar(ScalarMappable(Normalize(a, b), cmap), cax=cax, ticks=np.linspace(a, b, 8))
        cb.ax.set_yticklabels([f"{t:.0f}" for t in np.linspace(a, b, 8)], color="white", fontsize=8, fontweight="bold")
        cb.set_label(lab, color="white", fontsize=9, fontstyle="italic")
        cb.outline.set_visible(False)
        cb.ax.tick_params(length=0)


def steady_scene(key: str):
    """Steady eagar-tsai field in the beam frame, on a window sized like the AM render."""
    c = CASES[key]
    m = Model(c)
    if key == "alsi10mg":
        X = _grid(-0.80e-3, 0.10e-3, 3e-6)
        Y = _grid(0, 0.24e-3, 3e-6)
        Zd = _grid(0, 0.20e-3, 3e-6)
    else:  # wide enough to show the AM module's 1.47 mm x 0.349 mm pool for scale
        X = _grid(-1.75e-3, 0.12e-3, 5e-6)
        Y = _grid(0, 0.30e-3, 5e-6)
        Zd = _grid(0, 0.40e-3, 5e-6)
    Tt, Ts = m.planes(None, X, Y, Zd, xb=0.0)
    return m, X, Y, Zd, Tt, Ts


def render(out: pathlib.Path, am_png_dir: pathlib.Path) -> dict:
    """Steady AM-style renders and the side-by-side figure with the AM module's own renders."""
    out.mkdir(parents=True, exist_ok=True)
    info = {}
    panels = []
    for key, c in CASES.items():
        m, X, Y, Zd, Tt, Ts = steady_scene(key)
        T_iso = c["isotherms"][0][0]
        d = pool_dims(X, Y, Zd, Tt, Ts, T_iso)
        pk, _ = m.peak(None, X[np.argmax(Tt[0])])
        info[key] = dict(A=round(c["A"], 4), q0_W_mm2=round(m.q0_W_mm2), peak_K=round(pk, 1),
                         **{k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()})
        fig = plt.figure(figsize=(11.0, 5.6), facecolor=BG)
        ax = fig.add_axes([0.03, -0.06, 0.74, 1.0], projection="3d")
        tail = d["x_back_um"] * 1e-3
        am = None
        if c["am_dims_um"]:
            a = c["am_dims_um"]
            # the AM pool's front sits just ahead of the beam centre, like eagar-tsai's
            am = (d["x_front_um"] * 1e-3, a["L"] * 1e-3, a["half_W"] * 1e-3, a["D"] * 1e-3)
        draw_scene(ax, m, X, Y, Zd, Tt, Ts, 0.0,
                   rulers=(tail, d["L_um"] * 1e-3, d["W_um"] / 2e3, d["D_um"] * 1e-3), am_rulers=am,
                   zoom=1.45)
        _colourbars(fig, m, [0.915, 0.07, 0.02, 0.46], [0.795, 0.07, 0.02, 0.46])
        txt = (f"eagar-tsai, steady state\n{c['title']}\nA = {c['A']:.3f}, 1/e² radius {c['R_um']:.0f} µm, "
               f"plate {c['T_plate'] - 273.15:.0f} °C\npeak {pk:.0f} K (colours stop at the AM module's {c['am_T_range_K'][1]:.0f} K)\n"
               f"white: {c['isotherms'][0][1]} (solid), {c['isotherms'][1][1]} (dashed)\n"
               "no velocity arrows: eagar-tsai has no fluid flow")
        if am:
            txt += "\nmagenta dashes: the AM module's pool (L 1.470, half-width 0.231, D 0.349 mm)"
        fig.text(0.02, 0.97, txt, color="white", fontsize=9, va="top", family="monospace")
        p = out / f"eagar-tsai-meltpool-{key}-steady.png"
        fig.savefig(p, dpi=110, facecolor=BG)
        plt.close(fig)
        panels.append((key, am_png_dir / c["am_png"], p))

    # side by side: the AM module's render | eagar-tsai's, both alloys
    fig, axes = plt.subplots(2, 2, figsize=(15, 11.6), facecolor="white",
                             gridspec_kw=dict(wspace=0.02, hspace=0.08))
    for i, (key, am_png, et_png) in enumerate(panels):
        c = CASES[key]
        for j, (png, who) in enumerate(((am_png, "Thermo-Calc AM module"), (et_png, "eagar-tsai (this script)"))):
            ax = axes[i, j]
            ax.imshow(Image.open(png).convert("RGB"))
            ax.set_axis_off()
            ax.set_title(f"{who}: {c['title']}", fontsize=11, loc="left")
    fig.savefig(out / "am-module-vs-eagar-tsai-meltpools.png", dpi=90, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    (out / "transient-render-summary.json").write_text(json.dumps(info, indent=2))
    print(json.dumps(info, indent=2))
    return info


# --------------------------------------------------------------------------------------------
# Animation: one track in the lab frame
# --------------------------------------------------------------------------------------------
def _frame_job(args):
    key, i, tau, frames_dir, steady_dims = args
    c = CASES[key]
    m = Model(c)
    w = c["window"]
    dx = c["dx_um"] * 1e-6
    X = _grid(w["x"][0] * 1e-3, w["x"][1] * 1e-3, dx)
    Y = _grid(0, w["y"] * 1e-3, dx)
    Zd = _grid(0, w["z"] * 1e-3, dx)
    Tt, Ts = m.planes(tau, X, Y, Zd)
    T_iso = c["isotherms"][0][0]
    d = pool_dims(X, Y, Zd, Tt, Ts, T_iso)
    beam_on = tau <= m.tau_off
    fig = plt.figure(figsize=(10.0, 5.4), facecolor=BG)
    ax = fig.add_axes([0.03, -0.12, 0.76, 1.16], projection="3d")
    draw_scene(ax, m, X, Y, Zd, Tt, Ts, m.v * tau if beam_on else None, show_beam=beam_on,
               src_height_mm=0.5 * w["z"], label_size=8, zoom=1.3)
    _colourbars(fig, m, [0.915, 0.08, 0.016, 0.40], [0.80, 0.08, 0.016, 0.40])
    pk = float(Tt[0].max())
    status = "beam on" if beam_on else f"beam off {1e6 * (tau - m.tau_off):.0f} µs ago"
    txt = (f"eagar-tsai  {c['title']}\n"
           f"t = {tau * 1e3:5.3f} ms   {status}\n"
           f"pool at the {c['isotherms'][0][1]}: L {d['L_um']:4.0f}  W {d['W_um']:4.0f}  D {d['D_um']:4.0f} µm\n"
           f"steady state:                    L {steady_dims['L']:4.0f}  W {steady_dims['W']:4.0f}  D {steady_dims['D']:4.0f} µm\n"
           f"peak {pk:5.0f} K (colours stop at {c['am_T_range_K'][1]:.0f} K)")
    fig.text(0.015, 0.975, txt, color="white", fontsize=8.5, va="top", family="monospace")
    p = frames_dir / f"{key}-{i:03d}.png"
    fig.savefig(p, dpi=88, facecolor=BG)
    plt.close(fig)
    return str(p)


def animate(out: pathlib.Path, workers: int = 4, steady: dict | None = None, n_on: int = 54, n_off: int = 24):
    out.mkdir(parents=True, exist_ok=True)
    frames_dir = pathlib.Path("/tmp/eagar-tsai-transient-frames")
    frames_dir.mkdir(parents=True, exist_ok=True)
    for key, c in CASES.items():
        m = Model(c)
        t_cool = 0.2e-3 if key == "alsi10mg" else 0.5e-3  # both pools have frozen by then (see history)
        taus = list(np.linspace(0, m.tau_off, n_on + 1)[1:]) + list(m.tau_off + np.linspace(0, t_cool, n_off + 1)[1:])
        sd = steady[key] if steady else dict(L=np.nan, W=np.nan, D=np.nan)
        jobs = [(key, i, float(t), frames_dir, sd) for i, t in enumerate(taus)]
        with ProcessPoolExecutor(max_workers=workers) as ex:
            paths = list(ex.map(_frame_job, jobs))
        imgs = [Image.open(p).convert("RGB") for p in paths]
        pal = imgs[len(imgs) // 2].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in imgs]
        durations = [90] * len(q)
        durations[-1] = 1500
        durations[n_on - 1] = 600
        gif = out / f"eagar-tsai-meltpool-{key}-transient.gif"
        q[0].save(gif, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True)
        print(key, gif, f"{gif.stat().st_size / 1e6:.2f} MB", len(q), "frames")


# --------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["check", "history", "replot", "render", "animate", "all"])
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("arroyave-orchid-tools/eagar-tsai/am-module-inhouse/transient"))
    ap.add_argument("--am-png-dir", type=pathlib.Path, default=pathlib.Path("arroyave-orchid-tools/eagar-tsai/am-module-inhouse"))
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    t0 = time.time()
    steady = None
    if a.cmd in ("check", "all"):
        check(a.out)
    if a.cmd in ("render", "all"):
        info = render(a.out, a.am_png_dir)
        steady = {k: dict(L=v["L_um"], W=v["W_um"], D=v["D_um"]) for k, v in info.items()}
    if a.cmd in ("history", "replot", "all"):
        df = history(a.out, a.workers) if a.cmd != "replot" else pd.read_csv(a.out / "eagar-tsai-transient-history.csv")
        if steady is None:
            info = json.loads((a.out / "transient-render-summary.json").read_text())
            steady = {k: dict(L=v["L_um"], W=v["W_um"], D=v["D_um"]) for k, v in info.items()}
        plot_history(df, steady, a.out)
        summ = summarize_history(df, steady)
        (a.out / "eagar-tsai-transient-history-summary.json").write_text(json.dumps(summ, indent=2))
        print(json.dumps(summ, indent=2))
    if a.cmd in ("animate", "all"):
        if steady is None:
            info = json.loads((a.out / "transient-render-summary.json").read_text())
            steady = {k: dict(L=v["L_um"], W=v["W_um"], D=v["D_um"]) for k, v in info.items()}
        animate(a.out, a.workers, steady)
    print(f"done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
