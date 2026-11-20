"""Eagar-Tsai for 316L single tracks on BYU's Concept Laser M2 (issue #100, PR #243).

    python eagar_tsai_316l.py            # everything -> out/  (about 5 min on 4 cores)

What it computes, for the track design in README.md:

1. Steady-state melt-pool width W, depth D and length L over the M2's power-speed window, with ArroyaveLab
   eagar-tsai 0.6.0 (`compute_single_point`, 1 um grid), the package PR #238 used.
2. The start and end of a finite track. Same Eagar-Tsai integral (Gaussian surface source on a semi-infinite
   solid, constant properties), but the laser is on only from t = 0 to t_e while the beam runs from x = 0 to
   x = L_track. The fused cross-section at each x comes from that point's maximum temperature over all time,
   so W(x) and D(x) are what a transverse section at x would show if conduction were the only physics.
   The steady-state value is the mid-length one, checked against eagar-tsai's own steady state.
3. A galvo that ramps the beam speed from 0 to v (and back to 0) over t_acc with the laser on, i.e. no
   skywriting. Same integral with the beam's position x_s(t') instead of v t'.
4. Heat reaching a neighbouring track: the temperature rise at a lateral distance d from a finished track,
   at its mid-length, while it is drawn and after it ends.

Everything here is conduction only: no Marangoni flow, no keyhole, no evaporation, no powder, constant
properties. Section 2's numbers are therefore lower bounds on the real start and end zones; README.md says
what the literature adds on top. The material values are a nominal set to check against the Edison report
(edison-trajectories/m2-single-track-design/) and the AM Module's own CALPHAD properties.
"""
from __future__ import annotations

import csv
import json
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
T0 = 298.0  # K, as hard-coded in eagar-tsai

# --- inputs ---------------------------------------------------------------------------------------------------
# 316L, constant properties. Nominal set: means of the solid near the solidus and the liquid near the liquidus
# (alpha = 5.0e-6 m^2/s). The two alternates bracket alpha (3.5e-6, roughly room-temperature solid; 7.0e-6, hot
# solid) at the same rho*cp, to show which conclusions depend on it.
MATERIALS = {
    "nominal": dict(T_liq=1723.0, k=26.0, rho=7300.0, cp=710.0),
    "low_alpha": dict(T_liq=1723.0, k=18.2, rho=7300.0, cp=710.0),
    "high_alpha": dict(T_liq=1723.0, k=36.3, rho=7300.0, cp=710.0),
}
T_BOIL = 3090.0          # K, approximate boiling point of 316L (Fe-based); only used to flag peaks
ABSORPTIVITY = 0.40      # conduction-mode powder-bed value; keyhole tracks absorb more (README)
SPOTS_UM = (54.0, 90.0)  # 1/e^2 (D4sigma) diameters: LLNL's 400 W M2, Empa's 200 W M2. sigma = d/4.

# Representative settings for the finite-track runs (W, m/s): the corners and middle of the plan's window.
SETTINGS = [
    (100, 2.0), (100, 0.5), (100, 0.25),
    (200, 1.0), (200, 0.5),
    (300, 1.5), (300, 0.5),
    (375, 2.0), (375, 0.25),
]
GRID_P = np.array([50, 75, 100, 150, 200, 250, 300, 350, 400], float)
GRID_V = np.array([0.1, 0.15, 0.25, 0.4, 0.6, 1.0, 1.5, 2.0, 3.0])


def params(P, v, spot_um=54.0, mat="nominal", A=ABSORPTIVITY, L_track=None, t_acc=0.0):
    m = MATERIALS[mat]
    rhoc = m["rho"] * m["cp"]
    alpha = m["k"] / rhoc
    return dict(P=P, v=v, A=A, q=A * P, sig=spot_um * 1e-6 / 4.0, alpha=alpha, rhoc=rhoc, k=m["k"],
                T_liq=m["T_liq"], L=L_track, t_acc=t_acc, mat=mat, spot_um=spot_um)


# --- 1. steady state with the eagar-tsai package ----------------------------------------------------------------
def steady_state_pkg(P, v, spot_um=54.0, mat="nominal", A=ABSORPTIVITY, T_liq_shift=0.0):
    from eagar_tsai import BeamParameters, MaterialProperties, SimulationDomain, compute_single_point

    m = MATERIALS[mat]
    mp = MaterialProperties(liquidus_temperature=m["T_liq"] - T_liq_shift, thermal_conductivity=m["k"],
                            density=m["rho"], specific_heat=m["cp"])
    bp = BeamParameters(beam_diameter=spot_um * 1e-6 / 2.0, power=float(P), velocity=float(v), absorptivity=A)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = compute_single_point(bp, mp, SimulationDomain(spatial_resolution_um=1.0), full_field=False)
    return dict(W=r.width * 1e6, D=r.depth * 1e6, L=r.length * 1e6, Tpk=r.peak_temperature)


def normalized_enthalpy(p):
    """King et al. (2014) Delta H / h_s = A P / (pi h_s sqrt(alpha v a^3)), a = 1/e^2 beam radius, h_s = rho c T_liq."""
    a = 2.0 * p["sig"]
    h_s = p["rhoc"] * p["T_liq"]
    return p["q"] / (math.pi * h_s * math.sqrt(p["alpha"] * p["v"] * a ** 3))


# --- 2. finite track: same integral over the finite time the laser is on -----------------------------------------
def t_end(p):
    return p["L"] / p["v"] + p["t_acc"]


def x_source(tp, p):
    """Beam position (m) at time tp (s). Linear speed ramps of duration t_acc at both ends when t_acc > 0."""
    v, L, ta = p["v"], p["L"], p["t_acc"]
    if ta <= 0:
        return v * tp
    te = t_end(p)
    a = v / ta
    return np.where(tp < ta, 0.5 * a * tp ** 2,
                    np.where(tp < te - ta, 0.5 * v * ta + v * (tp - ta), L - 0.5 * a * (te - tp) ** 2))


def t_pass(x, p):
    """Time at which the beam centre passes x."""
    v, L, ta = p["v"], p["L"], p["t_acc"]
    x = np.clip(x, 0.0, L)
    if ta <= 0:
        return x / v
    te = t_end(p)
    a = v / ta
    return np.where(x < 0.5 * v * ta, np.sqrt(2 * x / a),
                    np.where(x < L - 0.5 * v * ta, ta + (x - 0.5 * v * ta) / v, te - np.sqrt(2 * np.clip(L - x, 0, None) / a)))


U = np.linspace(0.0, 1.0, 1601)


def temp_rise(x, y, z, t, p):
    """Temperature rise (K) at points (x, y, z) and times t (1-D arrays of equal length), finite track.

    dT = q / (pi rho c sqrt(4 pi alpha)) * int_0^{min(t, t_e)} dt' exp(-((x - x_s(t'))^2 + y^2) / (4 alpha tau + 2 sig^2)
         - z^2 / (4 alpha tau)) / (sqrt(tau) (2 alpha tau + sig^2)),  tau = t - t'.
    Integrated in s = sqrt(tau) (removes the 1/sqrt(tau)), on s = s_lo + (s_hi - s_lo) u^2 (dense near small tau).
    """
    al, sig = p["alpha"], p["sig"]
    te = t_end(p)
    s_hi = np.sqrt(np.clip(t, 0.0, None))
    s_lo = np.sqrt(np.clip(t - te, 0.0, None))
    span = (s_hi - s_lo)[:, None]
    s = s_lo[:, None] + span * U[None, :] ** 2
    jac = 2.0 * span * U[None, :]
    tau = s * s
    xi = x[:, None] - x_source(t[:, None] - tau, p)
    den = 4.0 * al * tau + 2.0 * sig * sig
    zz = (z * z)[:, None]
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        ez = np.where(tau > 0, zz / (4.0 * al * np.where(tau > 0, tau, 1.0)), np.where(zz > 0, np.inf, 0.0))
        f = np.exp(-(xi * xi + (y * y)[:, None]) / den - ez) * (4.0 / den) * jac
    C = p["q"] / (math.pi * p["rhoc"] * math.sqrt(4.0 * math.pi * al))
    return C * np.trapezoid(f, U, axis=1)


def tmax(x, y, z, p, lags, chunk=24):
    """Max over time of T at each point; times are t_pass(x) + lags."""
    out = np.empty(x.size)
    tp = t_pass(x, p)
    for i in range(0, x.size, chunk):
        sl = slice(i, i + chunk)
        n = x[sl].size
        t = (tp[sl][:, None] + lags[None, :]).ravel()
        rep = lambda a: np.repeat(a[sl], lags.size)  # noqa: E731
        dT = temp_rise(rep(x), rep(y), rep(z), t, p).reshape(n, lags.size)
        out[sl] = T0 + dT.max(axis=1)
    return out


def boundary(x, p, lags, along="z", hi=None, iters=15):
    """Fusion-boundary extent at each x: depth on the centreline (along='z') or surface half-width (along='y')."""
    zero = np.zeros_like(x)
    melted = tmax(x, zero, zero, p, lags) >= p["T_liq"]
    lo_b = np.zeros_like(x)
    hi_b = np.full_like(x, hi)
    for _ in range(iters):
        mid = 0.5 * (lo_b + hi_b)
        if along == "z":
            T = tmax(x, zero, mid, p, lags)
        else:
            T = tmax(x, mid, zero, p, lags)
        ok = T >= p["T_liq"]
        lo_b = np.where(ok, mid, lo_b)
        hi_b = np.where(ok, hi_b, mid)
    return np.where(melted, 0.5 * (lo_b + hi_b), 0.0)


def first_steady(x, f, f_ss, frac):
    """Smallest x after which f stays >= frac * f_ss (start side)."""
    ok = f >= frac * f_ss
    bad = np.where(~ok)[0]
    return float(x[0]) if bad.size == 0 else float(x[min(bad[-1] + 1, x.size - 1)])


def finite_track(P, v, spot_um=54.0, mat="nominal", t_acc=0.0, A=ABSORPTIVITY):
    ss = steady_state_pkg(P, v, spot_um, mat, A)
    L_ss, W_ss, D_ss = ss["L"] * 1e-6, ss["W"] * 1e-6, ss["D"] * 1e-6
    L_track = max(3e-3, 10 * L_ss + 20 * v * t_acc)
    p = params(P, v, spot_um, mat, A, L_track=L_track, t_acc=t_acc)
    sig = p["sig"]
    lags = np.linspace(-4 * sig / v, (1.6 * L_ss + 8 * sig) / v + 2 * t_acc, 181)
    span_s = min(L_track / 2 - 1e-4, 3.0 * L_ss + 0.4e-3 + 2 * v * t_acc)
    span_e = min(L_track / 2 - 1e-4, 2.0 * L_ss + 0.3e-3 + 2 * v * t_acc)
    xs = np.concatenate([np.linspace(0, span_s, 64), [L_track / 2],
                         np.linspace(L_track - span_e, L_track + 2 * sig, 48)])
    D = boundary(xs, p, lags, "z", hi=2.5 * D_ss + 20e-6)
    hw = boundary(xs, p, lags, "y", hi=1.5 * W_ss + 20e-6)
    W = 2 * hw
    imid = 64
    D_mid, W_mid = D[imid], W[imid]
    s_idx = slice(0, imid + 1)
    e_x, e_D, e_W = xs[imid:][::-1], D[imid:][::-1], W[imid:][::-1]   # from the end inward
    res = dict(P=P, v=v, spot_um=spot_um, mat=mat, t_acc_ms=t_acc * 1e3, E_J_mm=P / (v * 1e3),
               dH_hs=normalized_enthalpy(p), L_track_mm=L_track * 1e3,
               W_ss_pkg=ss["W"], D_ss_pkg=ss["D"], L_ss_pkg=ss["L"], Tpk_pkg=ss["Tpk"],
               W_mid=W_mid * 1e6, D_mid=D_mid * 1e6)
    for frac in (0.95, 0.99):
        tag = int(round(frac * 100))
        res[f"start_D{tag}_um"] = first_steady(xs[s_idx], D[s_idx], D_mid, frac) * 1e6
        res[f"start_W{tag}_um"] = first_steady(xs[s_idx], W[s_idx], W_mid, frac) * 1e6
        res[f"end_D{tag}_um"] = (L_track - first_steady(e_x, e_D, D_mid, frac)) * 1e6
        res[f"end_W{tag}_um"] = (L_track - first_steady(e_x, e_W, W_mid, frac)) * 1e6
    res["D_max_over_mid"] = float(D.max() / D_mid) if D_mid > 0 else float("nan")
    res["W_max_over_mid"] = float(W.max() / W_mid) if W_mid > 0 else float("nan")
    res["D_at_start_over_mid"] = float(D[0] / D_mid) if D_mid > 0 else float("nan")
    prof = dict(x_um=(xs * 1e6).tolist(), D_um=(D * 1e6).tolist(), W_um=(W * 1e6).tolist(),
                L_track_um=L_track * 1e6)
    return res, prof


# --- 4. heat reaching a neighbour --------------------------------------------------------------------------------
def neighbour_heating(P, v, spot_um=54.0, mat="nominal", L_track=10e-3, ds_mm=(0.25, 0.5, 1.0, 2.0, 3.0)):
    p = params(P, v, spot_um, mat, L_track=L_track)
    te = t_end(p)
    rows = []
    for d in ds_mm:
        y = d * 1e-3
        ts = np.concatenate([np.linspace(L_track / 2 / v, te, 60), te + np.geomspace(1e-5, 0.5, 120)])
        n = ts.size
        dT = temp_rise(np.full(n, L_track / 2), np.full(n, y), np.zeros(n), ts, p)
        after = lambda dt: float(np.interp(te + dt, ts, dT))  # noqa: E731
        rows.append(dict(P=P, v=v, L_track_mm=L_track * 1e3, d_mm=d, dT_peak_K=float(dT.max()),
                         t_peak_ms=float((ts[dT.argmax()] - L_track / 2 / v) * 1e3),
                         dT_at_end_K=after(0.0), dT_1ms_after_K=after(1e-3), dT_10ms_after_K=after(1e-2),
                         dT_100ms_after_K=after(0.1)))
    return rows


def depth_per_kelvin(P, v, spot_um=54.0):
    """Relative change in steady-state depth per K of preheat (eagar-tsai: preheat = lower T_liq)."""
    a = steady_state_pkg(P, v, spot_um)
    b = steady_state_pkg(P, v, spot_um, T_liq_shift=50.0)
    return dict(P=P, v=v, D=a["D"], D_plus50K=b["D"], dD_pct_per_10K=(b["D"] / a["D"] - 1) * 100 / 5,
                W=a["W"], W_plus50K=b["W"], dW_pct_per_10K=(b["W"] / a["W"] - 1) * 100 / 5)


# --- driver ------------------------------------------------------------------------------------------------------
def _grid_job(args):
    P, v, spot = args
    r = steady_state_pkg(P, v, spot)
    p = params(P, v, spot)
    return dict(P=P, v=v, spot_um=spot, E_J_mm=P / (v * 1e3), dH_hs=normalized_enthalpy(p), **r)


def _ft_job(args):
    t = time.time()
    res, prof = finite_track(*args)
    res["seconds"] = round(time.time() - t, 1)
    return res, prof


def write_csv(path, rows):
    keys = list(rows[0].keys())
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def main(which=("grid", "finite", "neighbour")):
    OUT.mkdir(exist_ok=True)
    with ProcessPoolExecutor(max_workers=4) as ex:
        if "finite" in which:
            jobs = [(P, v, 54.0, "nominal", 0.0) for P, v in SETTINGS]
            jobs += [(P, v, 90.0, "nominal", 0.0) for P, v in [(200, 1.0), (375, 0.25), (100, 2.0)]]
            jobs += [(P, v, 54.0, m, 0.0) for m in ("low_alpha", "high_alpha") for P, v in [(200, 1.0), (375, 0.25)]]
            jobs += [(P, v, 54.0, "nominal", 0.3e-3) for P, v in [(200, 1.0), (100, 2.0), (375, 0.25)]]
            out = list(ex.map(_ft_job, jobs))
            write_csv(OUT / "finite_track_summary.csv", [r for r, _ in out])
            profiles = {f"{r['P']}W_{r['v']}mps_{r['spot_um']:.0f}um_{r['mat']}_tacc{r['t_acc_ms']:.1f}ms": pr
                        for r, pr in out}
            (OUT / "finite_track_profiles.json").write_text(json.dumps(profiles))
            print("finite tracks done", flush=True)
        if "grid" in which:
            jobs = [(P, v, s) for s in SPOTS_UM for P in GRID_P for v in GRID_V]
            rows = list(ex.map(_grid_job, jobs, chunksize=4))
            write_csv(OUT / "steady_state_grid.csv", rows)
            print("grid done", flush=True)
    if "neighbour" in which:
        rows = []
        for P, v in [(375, 0.25), (300, 0.5), (200, 1.0), (100, 2.0)]:
            rows += neighbour_heating(P, v)
        write_csv(OUT / "neighbour_heating.csv", rows)
        sens = [depth_per_kelvin(P, v) for P, v in [(375, 0.25), (200, 1.0), (100, 2.0)]]
        write_csv(OUT / "preheat_sensitivity.csv", sens)
        print("neighbour done", flush=True)


if __name__ == "__main__":
    main(tuple(sys.argv[1:]) or ("grid", "finite", "neighbour"))
