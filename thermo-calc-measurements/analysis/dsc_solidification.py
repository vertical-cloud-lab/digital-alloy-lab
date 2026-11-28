#!/usr/bin/env python3
"""DSC/DTA melting or freezing trace -> solidus, liquidus, latent heat, fraction solid fs(T),
hot-cracking indices, and a comparison with a Scheil or equilibrium curve.

What it does, in order (see ../sops/01-dsc-solidification.md for the measurement itself):

1. Heat flow to W/g (if given in mW with a sample mass).
2. Optional thermal-lag (Tian) correction, q_true = q + tau * dq/dt, with the time constant tau
   estimated from the trailing edge of a pure-metal melting peak (``estimate_tau``).
3. Baseline between a start and an end temperature: linear, or "sigmoidal" (the baseline moves
   from the extrapolated pre-transition baseline to the extrapolated post-transition one in
   proportion to the fraction transformed; iterated). The sigmoidal baseline handles the change
   in specific heat between solid and liquid.
4. Partial-area integration: fraction liquid fL(T) = cumulative area / total area, fs = 1 - fL.
   Latent heat L = total area integrated over time (J/g).
5. Characteristic temperatures: extrapolated onset (tangent at the steepest leading-edge point
   meets the baseline), peak, end of peak, and the 1 % / 99 % partial-area temperatures.
   With several heating rates, ``extrapolate_to_zero_rate`` fits T(beta) and returns T(0).
6. Hot-cracking indices from fs(T): Kou's max |dT/d(fs^1/2)| over a window of fs^1/2, and the
   Clyne-Davies CSC computed from temperatures (equal to the time ratio at a constant cooling
   rate). Both windows are arguments; check them against the papers cited in the README.
7. Comparison with a model curve (CSV with columns T_C and fs, e.g. from pycalphad's ``scheil``
   package or a Thermo-Calc Scheil export): temperature error at fs = 0.1 ... 0.9, and
   solidus / liquidus / freezing-range differences.

CLI:
    python dsc_solidification.py trace.csv --mass-mg 20 --rate 10 --t1 520 --t2 640 \
        [--baseline sigmoidal] [--tau 4.2] [--model scheil.csv] [--out out_prefix]
    python dsc_solidification.py --demo          # synthetic trace with known answer

The trace CSV needs columns T_C and heat_flow (mW, or W/g with --per-gram), and optionally
time_s. Endothermic should be positive; pass --endo-down if your instrument plots it negative.

Only numpy is required; scipy is not used here. matplotlib is optional (for --out plots).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass, asdict

import numpy as np


# ----------------------------------------------------------------------------- I/O helpers

def read_trace(path: str) -> dict[str, np.ndarray]:
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError(f"{path}: no rows")
    cols = {k: np.array([float(r[k]) for r in rows]) for k in rows[0] if rows[0][k] not in (None, "")}
    for need in ("T_C", "heat_flow"):
        if need not in cols:
            raise ValueError(f"{path}: missing column {need!r} (have {sorted(cols)})")
    return cols


def read_model_curve(path: str) -> tuple[np.ndarray, np.ndarray]:
    """CSV with T_C and fs columns (Scheil or equilibrium), any order."""
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    T = np.array([float(r["T_C"]) for r in rows])
    fs = np.array([float(r["fs"]) for r in rows])
    order = np.argsort(fs)
    return T[order], fs[order]


# ----------------------------------------------------------------------------- core analysis

def _smooth(y: np.ndarray, n: int) -> np.ndarray:
    """Centred moving average over n points (n odd); edges use the available points."""
    if n <= 1:
        return y
    k = np.ones(n) / n
    num = np.convolve(y, k, mode="same")
    den = np.convolve(np.ones_like(y), k, mode="same")
    return num / den


def tian_correction(t: np.ndarray, q: np.ndarray, tau: float, smooth_s: float | None = None) -> np.ndarray:
    """First-order lag correction q_true = q + tau dq/dt (tau in s).

    The derivative amplifies noise, so dq/dt is smoothed over ``smooth_s`` seconds (default tau/2).
    """
    dt = float(np.median(np.diff(t)))
    n = max(1, int(round((smooth_s if smooth_s is not None else tau / 2) / dt)) | 1)
    return q + tau * _smooth(np.gradient(q, t), n)


def estimate_tau(t: np.ndarray, q: np.ndarray, frac_lo: float = 0.1, frac_hi: float = 0.7) -> float:
    """Time constant from the exponential decay after a pure-metal melting peak.

    Fits ln(q - q_base) vs t on the trailing edge between frac_hi and frac_lo of the peak height.
    """
    i_pk = int(np.argmax(q))
    tail_t, tail_q = t[i_pk:], q[i_pk:]
    base = float(np.median(tail_q[-max(5, len(tail_q) // 10):]))
    h = q[i_pk] - base
    sel = (tail_q - base < frac_hi * h) & (tail_q - base > frac_lo * h)
    if sel.sum() < 5:
        raise ValueError("not enough points on the trailing edge to fit tau")
    slope, _ = np.polyfit(tail_t[sel], np.log(tail_q[sel] - base), 1)
    return -1.0 / slope


def _linfit(x, y):
    a, b = np.polyfit(x, y, 1)
    return lambda z: a * np.asarray(z) + b


def baseline(T, q, t1, t2, kind="sigmoidal", fit_width=10.0, n_iter=20):
    """Return baseline array over the full trace, and the boolean mask of the integration window."""
    win = (T >= t1) & (T <= t2)
    pre = (T >= t1 - fit_width) & (T < t1)
    post = (T > t2) & (T <= t2 + fit_width)
    if kind == "linear" or pre.sum() < 3 or post.sum() < 3:
        q1 = np.interp(t1, T, q)
        q2 = np.interp(t2, T, q)
        b = q1 + (q2 - q1) * (T - t1) / (t2 - t1)
        return b, win
    f_pre, f_post = _linfit(T[pre], q[pre]), _linfit(T[post], q[post])
    b = f_pre(T) + (f_post(T) - f_pre(T)) * np.clip((T - t1) / (t2 - t1), 0, 1)
    for _ in range(n_iter):
        sig = np.where(win, q - b, 0.0)
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (sig[1:] + sig[:-1]) * np.diff(T))])
        tot = cum[-1] if cum[-1] != 0 else 1.0
        frac = np.clip(cum / tot, 0, 1)
        b_new = (1 - frac) * f_pre(T) + frac * f_post(T)
        if np.max(np.abs(b_new - b)) < 1e-9 * (np.max(np.abs(q)) + 1e-30):
            b = b_new
            break
        b = b_new
    return b, win


@dataclass
class DSCResult:
    direction: str
    latent_heat_J_per_g: float
    onset_C: float
    peak_C: float
    end_C: float
    T_at_1pct_C: float
    T_at_99pct_C: float
    solidus_C: float
    liquidus_C: float
    freezing_range_K: float
    kou_index_K: float
    kou_window_sqrt_fs: tuple
    csc: float
    tau_s: float | None = None


def partial_area(T, q, b, win, rate_K_per_s, t=None):
    """Cumulative transformed fraction over the window and the latent heat (J/g, q in W/g)."""
    sig = np.where(win, q - b, 0.0)
    x = t if t is not None else T / rate_K_per_s
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (sig[1:] + sig[:-1]) * np.diff(x))])
    total = cum[-1]
    return np.clip(cum / total, 0, 1), abs(total)


def extrapolated_onset(T, q, b, win):
    """Tangent at the steepest leading-edge point intersected with the baseline."""
    s = q - b
    i_pk = int(np.argmax(np.where(win, s, -np.inf)))
    lead = np.where(win)[0]
    lead = lead[lead <= i_pk]
    if len(lead) < 3:
        return float(T[i_pk])
    d = np.gradient(s, T)
    i_max = lead[int(np.argmax(d[lead]))]
    slope = d[i_max]
    return float(T[i_max] - s[i_max] / slope) if slope > 0 else float(T[lead[0]])


def T_at_fraction(T, frac, value):
    """First temperature where the cumulative fraction reaches value (frac monotone in T)."""
    idx = np.searchsorted(frac, value)
    idx = min(max(idx, 1), len(T) - 1)
    f0, f1 = frac[idx - 1], frac[idx]
    if f1 == f0:
        return float(T[idx])
    return float(T[idx - 1] + (value - f0) * (T[idx] - T[idx - 1]) / (f1 - f0))


def kou_index(T_of_fs, fs_grid, window=(0.87, 0.94), step=0.01):
    """max |dT/d(fs^1/2)| for fs^1/2 within the window (Kou 2015).

    Finite differences over steps of ``step`` in fs^1/2, which also smooths measurement noise.
    """
    r = np.arange(window[0], window[1] + 1e-12, step)
    T = np.interp(r ** 2, fs_grid, T_of_fs)
    return float(np.max(np.abs(np.diff(T) / np.diff(r)))) if len(r) > 1 else float("nan")


def csc_index(T_of_fs, fs_grid, v=(0.90, 0.99), r=(0.40, 0.90)):
    """Clyne-Davies CSC = t_V / t_R, written with temperatures (constant cooling rate)."""
    T = lambda f: float(np.interp(f, fs_grid, T_of_fs))
    tv = T(v[0]) - T(v[1])
    tr = T(r[0]) - T(r[1])
    return tv / tr if tr != 0 else float("nan")


def analyse(T, q, rate_K_per_min, t1, t2, *, t=None, tau=None, kind="sigmoidal",
            direction="heating", kou_window=(0.87, 0.94)) -> tuple[DSCResult, dict]:
    T = np.asarray(T, float)
    q = np.asarray(q, float)
    order = np.argsort(T)
    T, q = T[order], q[order]
    if t is not None:
        t = np.asarray(t, float)[order]
    rate = abs(rate_K_per_min) / 60.0
    if tau:
        tt = t if t is not None else T / rate
        q = tian_correction(tt, q, tau)
    b, win = baseline(T, q, t1, t2, kind=kind)
    frac, L = partial_area(T, q, b, win, rate, t=t)
    onset = extrapolated_onset(T, q, b, win)
    peak = float(T[int(np.argmax(np.where(win, q - b, -np.inf)))])
    T1, T99 = T_at_fraction(T, frac, 0.01), T_at_fraction(T, frac, 0.99)
    end = T_at_fraction(T, frac, 0.999)
    # On heating the cumulative fraction is the liquid fraction, so fs = 1 - frac.
    fs = 1.0 - frac
    fs_grid = np.linspace(0.0, 1.0, 1001)
    # T as a function of fs (fs decreases with T on heating): interpolate on the reversed arrays.
    sel = win
    T_w, fs_w = T[sel], fs[sel]
    o = np.argsort(fs_w)
    fs_u, idx = np.unique(fs_w[o], return_index=True)
    T_of_fs = np.interp(fs_grid, fs_u, T_w[o][idx])
    res = DSCResult(
        direction=direction,
        latent_heat_J_per_g=L,
        onset_C=onset, peak_C=peak, end_C=end,
        T_at_1pct_C=T1, T_at_99pct_C=T99,
        solidus_C=onset, liquidus_C=end,
        freezing_range_K=end - onset,
        kou_index_K=kou_index(T_of_fs, fs_grid, kou_window),
        kou_window_sqrt_fs=tuple(kou_window),
        csc=csc_index(T_of_fs, fs_grid),
        tau_s=tau,
    )
    curves = {"T_C": T, "q_corrected": q, "baseline": b, "fs": fs, "fs_grid": fs_grid, "T_of_fs": T_of_fs}
    return res, curves


def compare_with_model(T_of_fs, fs_grid, model_T, model_fs, levels=np.arange(0.1, 0.91, 0.1)):
    """Measured minus model temperature at given solid fractions, plus summary stats."""
    o = np.argsort(model_fs)
    model_fs, model_T = np.asarray(model_fs)[o], np.asarray(model_T)[o]
    meas = np.interp(levels, fs_grid, T_of_fs)
    mod = np.interp(levels, model_fs, model_T)
    d = meas - mod
    return {
        "fs_levels": [round(float(x), 3) for x in levels],
        "dT_meas_minus_model_K": [round(float(x), 2) for x in d],
        "rms_K": float(np.sqrt(np.mean(d ** 2))),
        # liquidus: highest T with any solid; solidus: lowest T that is not yet fully solid
        "model_liquidus_C": float(np.max(model_T[model_fs > 1e-6])),
        "model_solidus_C": float(np.min(model_T[model_fs < 1 - 1e-6])),
    }


def extrapolate_to_zero_rate(rates_K_per_min, temps_C):
    """Linear fit T = T0 + s*beta over several heating rates; returns (T0, slope)."""
    s, T0 = np.polyfit(np.asarray(rates_K_per_min, float), np.asarray(temps_C, float), 1)
    return float(T0), float(s)


# ----------------------------------------------------------------------------- synthetic demo

def scheil_fs(T, Tm=660.4, Tl=640.0, k=0.14, Te=577.0):
    """Binary Scheil fs(T) with a eutectic cut-off: fs = 1 - ((Tm - T)/(Tm - Tl))^(1/(k-1))."""
    T = np.asarray(T, float)
    ratio = np.clip((Tm - T) / (Tm - Tl), 1.0, None)
    fl = np.where(T >= Tl, 1.0, ratio ** (1.0 / (k - 1.0)))
    fl = np.where(T < Te, 0.0, np.clip(fl, 0, 1))
    return 1.0 - fl


def synthetic_trace(rate_K_per_min=10.0, L=390.0, tau=3.0, noise=2e-4, seed=0):
    """Heating trace (W/g) for a Scheil-like Al alloy, lagged by tau, on a sloped baseline."""
    rng = np.random.default_rng(seed)
    beta = rate_K_per_min / 60.0
    T = np.arange(500.0, 700.0, 0.05)
    t = (T - T[0]) / beta
    fs = scheil_fs(T)
    fl = 1.0 - fs
    dfl_dt = np.gradient(fl, t)
    q_true = L * dfl_dt                      # W/g of latent heat
    # first-order lag: tau dq/dt + q = q_true
    q = np.zeros_like(q_true)
    dt = np.diff(t)
    for i in range(1, len(t)):
        q[i] = q[i - 1] + dt[i - 1] / tau * (q_true[i] - q[i - 1])
    cp_s, cp_l = 1.10, 1.18                 # J/g/K, illustrative only
    base = beta * (cp_s + (cp_l - cp_s) * fl)
    return {"T_C": T, "time_s": t, "heat_flow": q + base + noise * rng.standard_normal(len(T))}, fs


def demo():
    tr, fs_true = synthetic_trace()
    res, cur = analyse(tr["T_C"], tr["heat_flow"], 10.0, 560.0, 662.0, t=tr["time_s"], tau=3.0)
    res_nolag, _ = analyse(tr["T_C"], tr["heat_flow"], 10.0, 560.0, 662.0, t=tr["time_s"], tau=None)
    print(json.dumps({"with_tian_correction": asdict(res), "without": asdict(res_nolag)}, indent=2))
    Tm = np.linspace(560, 660, 400)
    cmp = compare_with_model(cur["T_of_fs"], cur["fs_grid"], Tm, scheil_fs(Tm))
    print(json.dumps({"vs_true_scheil": cmp}, indent=2))
    return res, cmp


# ----------------------------------------------------------------------------- CLI

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("trace", nargs="?")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--mass-mg", type=float)
    p.add_argument("--per-gram", action="store_true", help="heat_flow is already W/g")
    p.add_argument("--endo-down", action="store_true", help="endotherms are negative in the file")
    p.add_argument("--rate", type=float, required=False, help="heating/cooling rate, K/min")
    p.add_argument("--t1", type=float, help="integration start, C")
    p.add_argument("--t2", type=float, help="integration end, C")
    p.add_argument("--baseline", choices=["linear", "sigmoidal"], default="sigmoidal")
    p.add_argument("--tau", type=float, help="thermal-lag time constant, s (from estimate_tau on a pure metal)")
    p.add_argument("--kou-window", type=float, nargs=2, default=(0.87, 0.94))
    p.add_argument("--model", help="CSV with T_C, fs from Scheil/equilibrium")
    p.add_argument("--out", help="prefix for JSON/CSV/PNG outputs")
    a = p.parse_args(argv)
    if a.demo:
        demo()
        return
    if not (a.trace and a.rate and a.t1 is not None and a.t2 is not None):
        p.error("trace, --rate, --t1 and --t2 are required (or use --demo)")
    d = read_trace(a.trace)
    q = d["heat_flow"] * (-1 if a.endo_down else 1)
    if not a.per_gram:
        if not a.mass_mg:
            p.error("--mass-mg is required unless --per-gram")
        q = q / a.mass_mg               # mW / mg = W/g
    res, cur = analyse(d["T_C"], q, a.rate, a.t1, a.t2, t=d.get("time_s"), tau=a.tau,
                       kind=a.baseline, kou_window=tuple(a.kou_window))
    out = {"result": asdict(res)}
    if a.model:
        mT, mfs = read_model_curve(a.model)
        out["vs_model"] = compare_with_model(cur["T_of_fs"], cur["fs_grid"], mT, mfs)
    print(json.dumps(out, indent=2))
    if a.out:
        with open(a.out + "_summary.json", "w") as fh:
            json.dump(out, fh, indent=2)
        with open(a.out + "_fs.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["fs", "T_C"])
            for f, T in zip(cur["fs_grid"], cur["T_of_fs"]):
                w.writerow([f"{f:.4f}", f"{T:.3f}"])
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
            ax[0].plot(cur["T_C"], cur["q_corrected"], lw=1, label="heat flow")
            ax[0].plot(cur["T_C"], cur["baseline"], lw=1, ls="--", label="baseline")
            ax[0].set_xlabel("T (°C)"); ax[0].set_ylabel("W/g"); ax[0].legend(frameon=False)
            ax[1].plot(cur["T_of_fs"], cur["fs_grid"], lw=1.5, label="measured")
            if a.model:
                ax[1].plot(mT, mfs, lw=1, ls="--", label="model")
            ax[1].set_xlabel("T (°C)"); ax[1].set_ylabel("fraction solid"); ax[1].legend(frameon=False)
            fig.tight_layout(); fig.savefig(a.out + "_fs.png", dpi=150)
        except ImportError:
            pass


if __name__ == "__main__":
    main()
