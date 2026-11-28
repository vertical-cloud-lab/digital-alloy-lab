"""Data panels for SOP 01's animation (#262): the characteristic DSC data, computed with the repo's own analysis code
(``../analysis/dsc_solidification.py`` and ``../analysis/espei_export.py``) on synthetic traces, every panel badged
"synthetic example". Nothing here is a measurement.

    python sop01_panels.py            # writes /tmp/sop01_panels/*.png, one still of each panel, and prints the numbers

Each ``panel_<name>()`` returns f(u) -> RGBA PIL image for ``SOPScene.panel``; u (0-1) animates it where that means
something (a time cursor on the program, the heat-flow curve drawn as the furnace heats), and is ignored otherwise.
"""
from __future__ import annotations

import functools
import io
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

import dsc_solidification as dsc  # noqa: E402
import espei_export as ee  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

# the reference palette (dataviz skill, light mode): measured = slot 1, model/second = slot 2, third = slot 3
C1, C2, C3, C4 = "#257de0", "#f47230", "#00b894", "#6a4ce2"
INK, INK2, GRID = "#191919", "#666666", "#e3e5e8"
GOOD, BAD = "#0a7d32", "#c62828"
DPI = 150
BADGE = "synthetic example"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": "#9aa0a6",
                     "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 0.8,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})

# ================================================================================================ the numbers
RATE = 10.0                   # K/min, beta for Heat 1, cooling and Heat 2
TAU = 3.1                     # s, the cell's time constant (the SOP's CLI example)
MASS_MG = (15.20, 15.08)      # replicates A and B before the run (example values)
MASS_AFTER = (15.17, 15.05)   # after the run


def _lag(t, q_true, tau):
    """First-order lag, tau dq/dt + q = q_true (as dsc.synthetic_trace)."""
    q = np.zeros_like(q_true)
    q[0] = q_true[0]
    dt = np.diff(t)
    for i in range(1, len(t)):
        q[i] = q[i - 1] + dt[i - 1] / tau * (q_true[i] - q[i - 1])
    return q


def _heating(rate, fs_fn, L=390.0, tau=TAU, T0=500.0, T1=700.0, noise=2e-4, seed=0):
    """A heating trace like dsc.synthetic_trace but with any fs(T) (for Heat 1's incipient melting)."""
    rng = np.random.default_rng(seed)
    beta = rate / 60.0
    T = np.arange(T0, T1, 0.05)
    t = (T - T[0]) / beta
    fl = 1.0 - fs_fn(T)
    q_true = L * np.gradient(fl, t)
    q = _lag(t, q_true, tau)
    base = beta * (1.10 + 0.08 * fl)
    return dict(T_C=T, time_s=t, heat_flow=q + base + noise * rng.standard_normal(len(T)))


def fs_heat1(T):
    """As-atomized powder: segregated, rapidly solidified material starts melting 6 K under the bead's eutectic
    (577 C), the incipient melting the SOP compares Heat 1 with Heat 2 for (synthetic)."""
    return dsc.scheil_fs(np.asarray(T, float), Te=571.0)


def fs_model(T):
    """The 'model' curve: Scheil for the MEASURED composition (SOP 05), stood in for by the binary Scheil with a
    slightly different liquidus and partition coefficient (synthetic)."""
    return dsc.scheil_fs(T, Tl=637.5, k=0.14)


@functools.lru_cache(maxsize=1)
def data() -> dict:
    out = {}
    # Heat 2 at 10 K/min: the repo's own synthetic trace, analysed as the SOP says (lag-corrected, sigmoidal)
    tr2, _ = dsc.synthetic_trace(RATE, L=390.0, tau=TAU, seed=2)
    res2, cur2 = dsc.analyse(tr2["T_C"], tr2["heat_flow"], RATE, 560.0, 662.0, t=tr2["time_s"], tau=TAU)
    out["h2"] = (tr2, res2, cur2)
    tr1 = _heating(RATE, fs_heat1, seed=1)
    res1, cur1 = dsc.analyse(tr1["T_C"], tr1["heat_flow"], RATE, 550.0, 662.0, t=tr1["time_s"], tau=TAU)
    out["h1"] = (tr1, res1, cur1)
    Tm = np.concatenate([[576.99], np.linspace(577.0, 645.0, 500)])      # a Scheil export ends at fs = 1
    fm = np.where(Tm < 577.0, 1.0, fs_model(Tm))
    out["model"] = (Tm, fm)
    out["cmp"] = dsc.compare_with_model(cur2["T_of_fs"], cur2["fs_grid"], Tm, fm)
    # three rates on fresh powder: onset and end of melting, raw and lag-corrected, extrapolated to beta -> 0
    rates = [5.0, 10.0, 20.0]
    raw, cor = [], []
    for k, b in enumerate(rates):
        tr, _ = dsc.synthetic_trace(b, L=390.0, tau=TAU, seed=10 + k)
        r_raw, _ = dsc.analyse(tr["T_C"], tr["heat_flow"], b, 560.0, 672.0, t=tr["time_s"], tau=None)
        r_cor, _ = dsc.analyse(tr["T_C"], tr["heat_flow"], b, 560.0, 672.0, t=tr["time_s"], tau=TAU)
        raw.append(r_raw)
        cor.append(r_cor)
    out["rates"] = rates
    out["raw"], out["cor"] = raw, cor
    out["end0_raw"] = dsc.extrapolate_to_zero_rate(rates, [r.end_C for r in raw])
    out["end0_cor"] = dsc.extrapolate_to_zero_rate(rates, [r.end_C for r in cor])
    out["on0"] = dsc.extrapolate_to_zero_rate(rates, [r.onset_C for r in cor])
    # tau from the trailing edge of a Zn standard's melting peak (419.5 C) at 10 K/min
    t = np.arange(0.0, 240.0, 0.1)
    t_on, t_end = 60.0, 100.0
    rise = np.clip((t - t_on) / (t_end - t_on), 0, 1)
    q = np.where(t < t_end, 0.012 * rise, 0.012 * np.exp(-(t - t_end) / TAU))
    q = q + 1e-5 * np.random.default_rng(3).standard_normal(len(t))
    out["zn"] = (t, q, dsc.estimate_tau(t, q), t_end)
    # the Al standard (660.3 C, 397 J/g handbook): a synthetic peak, analysed with the same code
    Tal = np.arange(640.0, 690.0, 0.02)
    beta = RATE / 60.0
    tal = (Tal - Tal[0]) / beta
    Ton, Lal = 660.42, 392.0                            # the 'measured' onset and heat of fusion it is built with
    t_on_al = (Ton - Tal[0]) / beta
    melt_s = 34.0                                       # s for the melt to finish
    qt = np.where((tal >= t_on_al) & (tal < t_on_al + melt_s), (tal - t_on_al) / melt_s, 0.0)
    qt = qt / np.trapezoid(qt, tal) * Lal
    qal = _lag(tal, qt, 0.6) + beta * 1.05
    ral, cal = dsc.analyse(Tal, qal, RATE, 652.0, 682.0, t=tal, tau=0.6)
    out["al"] = (Tal, qal, ral, cal)
    # the daily empty-crucible baseline (same program), subtracted from the sample's raw signal
    Tb = tr2["T_C"]
    drift = 0.05 + 0.0014 * (Tb - 500.0) + 0.03 * np.sin((Tb - 500.0) / 45.0)
    out["base"] = (Tb, tr2["heat_flow"] + drift, drift)
    # ESPEI/ORCHID rows from the beta -> 0 values (an Al-7Si-like alloy here; the primary phase from XRD/SEM)
    x = json.dumps({"SI": 0.068})
    rows = [dict(system="AL-SI", sample_id="DAL-S1", T_K=f"{out['end0_cor'][0] + 273.15:.1f}", u_T_K="1.5",
                 kind="liquidus", known_phase="LIQUID", other_phases="FCC_A1", x_json=x,
                 method="DSC heating 5/10/20 K/min, extrapolated to 0 (synthetic example)",
                 link="https://example.invalid/run/DAL-S1"),
            dict(system="AL-SI", sample_id="DAL-S1", T_K=f"{out['on0'][0] + 273.15:.1f}", u_T_K="1.5",
                 kind="solidus", known_phase="FCC_A1", other_phases="LIQUID", x_json=x,
                 method="DSC heating 5/10/20 K/min, extrapolated to 0 (synthetic example)",
                 link="https://example.invalid/run/DAL-S1")]
    out["espei"] = ee.to_espei(rows, dependent="AL", reference="VCL-synthetic")
    out["orchid"] = ee.to_orchid_rows(rows)
    out["program"] = program()
    return out


def program() -> dict:
    """The SOP's program for an Al alloy, as (t_min, T_C) breakpoints with segment names."""
    segs = [("hold 30 C", 5.0, 30.0, 30.0), ("20 K/min to 450 C", (450 - 30) / 20.0, 30.0, 450.0),
            ("Heat 1, 10 K/min", (720 - 450) / RATE, 450.0, 720.0), ("hold 2 min", 2.0, 720.0, 720.0),
            ("cool 10 K/min", (720 - 450) / RATE, 720.0, 450.0), ("Heat 2, 10 K/min", (720 - 450) / RATE, 450.0, 720.0),
            ("cool to 30 C", 32.0, 720.0, 30.0)]
    t, T, names, t0 = [0.0], [30.0], [], 0.0
    bounds = []
    for name, dur, a, b in segs:
        t0 += dur
        t.append(t0)
        T.append(b)
        names.append(name)
        bounds.append(t0)
    return dict(t=np.array(t), T=np.array(T), names=names, bounds=bounds, total_min=t0)


def program_T(tmin: float) -> float:
    p = program()
    return float(np.interp(tmin, p["t"], p["T"]))


def segment_at(tmin: float) -> str:
    p = program()
    for name, b in zip(p["names"], p["bounds"]):
        if tmin <= b + 1e-9:
            return name
    return p["names"][-1]


# ================================================================================================ drawing helpers
def _img(fig) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, facecolor=fig.get_facecolor(), transparent=False)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def _fig(w=5.2, h=3.4, title=""):
    fig = plt.figure(figsize=(w, h), facecolor=(1, 1, 1, 0.94))
    if title:
        fig.text(0.02, 0.965, title, ha="left", va="top", fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.98, 0.965, BADGE, ha="right", va="top", fontsize=8.5, color="#7a4b00",
             bbox=dict(boxstyle="round,pad=0.25", fc="#fff3d6", ec="#e0b860", lw=0.8))
    return fig


def _cache(fn):
    """Panels redraw only when u moves by 1/150 (stage caches on u too)."""
    memo = {}

    def f(u):
        k = round(float(u) * 150) / 150
        if k not in memo:
            memo[k] = fn(k)
        return memo[k]
    return f


# ================================================================================================ the panels
def panel_record():
    """The run record (#159) for one sample: example values."""
    @_cache
    def f(u):
        fig = _fig(4.6, 2.5, "Run record (#159): DSC sample")
        rows = [("Run ID", "DAL-A12-0417 (atomizer run)"), ("Alloy, sieve cut", "Al-7Si-0.3Mg, 20-63 um"),
                ("Sub-sample", "riffle-split, 2 halvings"), ("Storage humidity", "18 % RH (desiccator)"),
                ("Days since atomization", "6"), ("Mass A / B", f"{MASS_MG[0]:.2f} / {MASS_MG[1]:.2f} mg")]
        for i, (k, v) in enumerate(rows):
            y = 0.80 - i * 0.125
            fig.text(0.05, y, k, fontsize=9.5, color=INK2, va="center")
            fig.text(0.50, y, v, fontsize=9.5, color=INK, va="center", family="DejaVu Sans Mono")
        return _img(fig)
    return f


def panel_program(show_q: bool = True):
    """The temperature program, a cursor at u of the run; with the heat flow beneath it (two charts on one time axis)."""
    d = data()
    p = d["program"]
    total = p["total_min"]
    # the heat-flow trace along the run (synthetic): lagged cp step and the three transitions
    tt = np.linspace(0, total, 3000)
    TT = np.interp(tt, p["t"], p["T"])
    beta = np.gradient(TT, tt * 60.0)
    fl1 = 1 - fs_heat1(TT)
    fl2 = 1 - dsc.scheil_fs(TT)
    fl_c = 1 - dsc.scheil_fs(np.minimum(TT, 631.0) - 0.0)       # cooling: nothing freezes above 631 C (undercooling)
    b = p["bounds"]
    seg = np.searchsorted(b, tt)
    fl = np.where(seg <= 2, fl1, np.where(seg == 3, 1.0, np.where(seg == 4, np.where(TT > 631.0, 1.0, fl_c),
                                                                  np.where(seg == 5, fl2, 1 - dsc.scheil_fs(TT)))))
    q_true = 390.0 * np.gradient(fl, tt * 60.0) + beta * 1.12
    q = _lag(tt * 60.0, q_true, TAU)

    @_cache
    def f(u):
        fig = _fig(5.4, 3.6, "Program (Al alloys)")
        ax1 = fig.add_axes([0.11, 0.50, 0.85, 0.36])
        ax2 = fig.add_axes([0.11, 0.13, 0.85, 0.30], sharex=ax1)
        ax1.plot(p["t"] / 60.0, p["T"], color=C1, lw=2)
        tc = u * total
        ax1.plot([tc / 60.0], [program_T(tc)], "o", ms=7, color=C2, mec="white", mew=1.5, zorder=5)
        ax1.set_ylabel("T (C)")
        ax1.set_ylim(0, 800)
        ax1.tick_params(labelbottom=False)
        lab = [(2.5, "30 C"), (5 + 10.5, "20 K/min"), (26 + 13.5, "Heat 1"), (55 + 13.5, "cool"), (82 + 13.5, "Heat 2")]
        for x, s in lab:
            ax1.text(x / 60.0, 760 if s != "30 C" else 110, s, ha="center" if s != "30 C" else "left", fontsize=8,
                     color=INK2)
        ax1.axhline(720, color=INK2, lw=0.6, ls=":")
        ax1.text(2.45, 690, "720", fontsize=7.5, color=INK2, ha="right")
        if show_q:
            k = tt <= tc
            ax2.plot(tt[k] / 60.0, q[k], color=C1, lw=1.6)
            ax2.set_ylim(-2.5, 2.5)
            ax2.set_ylabel("heat flow\n(W/g, endo up)", fontsize=8.5)
            ax2.text(0.02, 0.06, "melting up, freezing down; peaks clipped", transform=ax2.transAxes, fontsize=7.5,
                     color=INK2)
        ax2.set_xlabel("time (h)")
        ax2.set_xlim(0, total / 60.0)
        return _img(fig)
    return f


def _onset_tangent(T, q, b, onset):
    s = q - b
    d = np.gradient(s, T)
    i_pk = int(np.argmax(s))
    lead = np.arange(0, i_pk + 1)
    i = lead[int(np.argmax(d[lead]))]
    return T[i], q[i], d[i]


def panel_heatflow(which: str = "h2", title: str = "Heat 2 at 10 K/min: the solidified bead"):
    """Heat flow vs T with the baseline, the onset tangent, onset (solidus), end at 99.9 % (liquidus), 1 %/99 %;
    drawn up to u of the temperature range, the markers at the end. The eutectic peak runs off the top."""
    d = data()
    tr, res, cur = d[which]
    T, qc, bb = cur["T_C"], cur["q_corrected"], cur["baseline"]
    top = 6.0

    @_cache
    def f(u):
        fig = _fig(5.4, 3.5, title)
        ax = fig.add_axes([0.12, 0.14, 0.84, 0.70])
        Tmax = 540.0 + u * (690.0 - 540.0)
        k = (T <= Tmax) & (T >= 540.0)
        ax.plot(T[k], qc[k], color=C1, lw=2, label="heat flow, lag-corrected")
        ax.plot(T[k], bb[k], color=INK2, lw=1, ls="--", label="sigmoidal baseline")
        ax.set_xlim(540, 690)
        ax.set_ylim(-0.3, top)
        ax.set_xlabel("T (C)")
        ax.set_ylabel("W/g (endo up)")
        if Tmax > 580:
            ax.text(578.5, top * 0.93, "eutectic peak\n(off scale)", fontsize=7.5, color=INK2, va="top")
        if u > 0.97:
            T0, q0, sl = _onset_tangent(T, qc, bb, res.onset_C)
            xs = np.linspace(res.onset_C - 1.5, res.onset_C + 0.3, 10)
            ax.plot(xs, q0 + sl * (xs - T0), color=C2, lw=1.2)
            ax.axvline(res.onset_C, color=C2, lw=1.2, ls=":")
            ax.axvline(res.end_C, color=C3, lw=1.2, ls=":")
            ax.text(res.onset_C - 1.5, top * 0.55, f"onset = solidus\n{res.onset_C:.1f} C", fontsize=8, color=INK,
                    ha="right")
            ax.text(res.end_C + 1.5, top * 0.55, f"end (99.9 %)\n= liquidus\n{res.end_C:.1f} C", fontsize=8,
                    color=INK, ha="left")
            ax.text(0.45, 0.40, f"1 % / 99 %: {res.T_at_1pct_C:.1f} / {res.T_at_99pct_C:.1f} C\n"
                    f"latent heat {res.latent_heat_J_per_g:.0f} J/g", transform=ax.transAxes, fontsize=8.5,
                    color=INK, ha="center")
        ax.legend(loc="upper right", fontsize=8)
        return _img(fig)
    return f


def panel_fs():
    """fs(T) measured (Heat 2, lag-corrected) vs the Scheil model; measured minus model at fs = 0.1-0.9; Kou, CSC."""
    d = data()
    _, res, cur = d["h2"]
    Tm, fsm = d["model"]
    cmp = d["cmp"]

    @_cache
    def f(u):
        fig = _fig(5.4, 3.6, "Fraction solid vs Scheil (measured composition)")
        ax = fig.add_axes([0.11, 0.42, 0.85, 0.44])
        ax.plot(cur["T_of_fs"], cur["fs_grid"], color=C1, lw=2, label="measured (DSC, Heat 2)")
        ax.plot(Tm, fsm, color=C2, lw=2, ls="--", label="Scheil model (pycalphad / Thermo-Calc)")
        ax.set_xlim(560, 650)
        ax.set_ylim(0, 1.02)
        ax.set_ylabel("fs")
        ax.set_xlabel("T (C)", labelpad=1)
        ax.legend(loc="lower left", fontsize=8)
        ax2 = fig.add_axes([0.11, 0.08, 0.50, 0.22])
        lv, dT = cmp["fs_levels"], cmp["dT_meas_minus_model_K"]
        ax2.bar(lv, dT, width=0.06, color=C1)
        ax2.axhline(0, color=INK2, lw=0.8)
        ax2.set_xticks(lv)
        ax2.set_xticklabels([f"{x:.1f}" for x in lv], fontsize=7)
        ax2.set_ylabel("dT (K)", fontsize=8)
        ax2.set_title("measured - model at fs", fontsize=8, color=INK2, pad=2)
        fig.text(0.66, 0.24, f"Kou index  {res.kou_index_K:.0f} K\nCSC  {res.csc:.3f}\n"
                 f"freezing range  {res.freezing_range_K:.0f} K\nRMS dT  {cmp['rms_K']:.1f} K", fontsize=8.5,
                 color=INK, va="center", family="DejaVu Sans Mono")
        return _img(fig)
    return f


def panel_beta():
    """Onset and end vs heating rate, extrapolated to beta -> 0."""
    d = data()
    rates = np.array(d["rates"])

    @_cache
    def f(u):
        fig = _fig(5.0, 3.4, "Three rates, extrapolated to beta -> 0")
        ax = fig.add_axes([0.13, 0.15, 0.84, 0.48])
        ax0 = fig.add_axes([0.13, 0.70, 0.84, 0.16], sharex=ax)
        xs = np.linspace(0, 21, 50)
        for a_, name, ys, (T0, s_), c in ((ax, "end, raw", [r.end_C for r in d["raw"]], d["end0_raw"], C2),
                                         (ax, "end, lag-corrected", [r.end_C for r in d["cor"]], d["end0_cor"], C1),
                                         (ax0, "onset", [r.onset_C for r in d["cor"]], d["on0"], C3)):
            a_.plot(rates, ys, "o", ms=7, color=c, mec="white", mew=1.2)
            a_.plot(xs, T0 + s_ * xs, color=c, lw=1.3, ls="--", label=f"{name}: T(0) = {T0:.1f} C")
            a_.plot([0], [T0], "s", ms=6, color=c)
        ax.set_ylim(638.5, 645)
        ax0.set_ylim(574, 580)
        ax0.tick_params(labelbottom=False)
        ax.set_xlabel("heating rate beta (K/min)")
        ax.set_ylabel("T (C)")
        ax.set_xlim(-0.8, 21)
        ax.set_xticks([0, 5, 10, 20])
        ax.legend(loc="upper left", fontsize=8)
        ax0.legend(loc="upper left", fontsize=8)
        return _img(fig)
    return f


def panel_tau():
    d = data()
    t, q, tau, t_end = d["zn"]

    @_cache
    def f(u):
        fig = _fig(5.0, 3.1, "Zn standard: fit tau to the trailing edge")
        ax = fig.add_axes([0.13, 0.16, 0.83, 0.66])
        ax.plot(t, q * 1000, color=C1, lw=2, label="Zn melting peak")
        tf = np.linspace(t_end + 0.36 * tau, t_end + 2.3 * tau, 30)
        ax.plot(tf, 12 * np.exp(-(tf - t_end) / tau), color=C2, lw=3, alpha=0.8,
                label=f"exponential fit, tau = {tau:.2f} s")
        ax.set_xlim(40, 130)
        ax.set_xlabel("time (s)")
        ax.set_ylabel("heat flow (mW)")
        ax.legend(loc="upper left", fontsize=8.5)
        ax.text(0.98, 0.45, "check weekly and\nafter a crucible change", transform=ax.transAxes, ha="right",
                fontsize=8.5, color=INK2)
        return _img(fig)
    return f


def panel_al():
    d = data()
    T, q, res, cur = d["al"]
    gap = 100 * (res.latent_heat_J_per_g - 397.0) / 397.0

    @_cache
    def f(u):
        fig = _fig(5.0, 3.2, "Al standard: acceptance")
        ax = fig.add_axes([0.13, 0.16, 0.50, 0.66])
        ax.plot(T, cur["q_corrected"], color=C1, lw=2)
        ax.axvspan(659.8, 660.8, color=C3, alpha=0.18, lw=0)
        ax.axvline(res.onset_C, color=C2, lw=1.2, ls=":")
        ax.set_xlim(650, 685)
        ax.set_xlabel("T (C)")
        ax.set_ylabel("W/g (endo up)")
        ok1 = abs(res.onset_C - 660.3) <= 0.5
        ok2 = abs(gap) <= 3.0
        fig.text(0.66, 0.70, f"onset {res.onset_C:.2f} C\n660.3 +- 0.5 K", fontsize=9, color=INK)
        fig.text(0.66, 0.58, "PASS" if ok1 else "FAIL", fontsize=10, fontweight="bold", color=GOOD if ok1 else BAD)
        fig.text(0.66, 0.40, f"dH {res.latent_heat_J_per_g:.0f} J/g\nvs 397 J/g: {gap:+.1f} %\n(limit 3 %)",
                 fontsize=9, color=INK)
        fig.text(0.66, 0.24, "PASS" if ok2 else "FAIL", fontsize=10, fontweight="bold", color=GOOD if ok2 else BAD)
        return _img(fig)
    return f


def panel_baseline():
    d = data()
    Tb, raw, drift = d["base"]

    @_cache
    def f(u):
        fig = _fig(5.0, 3.1, "Daily empty-crucible baseline, subtracted")
        ax = fig.add_axes([0.13, 0.16, 0.83, 0.66])
        k = Tb >= 540
        ax.plot(Tb[k], raw[k], color=C2, lw=1.6, label="sample run, raw")
        ax.plot(Tb[k], drift[k], color=INK2, lw=1.4, ls="--", label="empty crucibles, same program")
        if u > 0.3:
            ax.plot(Tb[k], (raw - drift)[k], color=C1, lw=2, label="raw - baseline")
        ax.set_ylim(-0.1, 1.4)
        ax.set_xlabel("T (C)")
        ax.set_ylabel("W/g (endo up)")
        ax.legend(loc="upper left", fontsize=8)
        ax.text(0.99, 0.02, "eutectic peak off scale", transform=ax.transAxes, ha="right", fontsize=7.5, color=INK2)
        return _img(fig)
    return f


def panel_h1h2():
    d = data()
    _, r1, c1 = d["h1"]
    _, r2, c2 = d["h2"]

    @_cache
    def f(u):
        fig = _fig(5.2, 3.2, "Heat 1 (as-atomized) vs Heat 2 (bead)")
        ax = fig.add_axes([0.12, 0.16, 0.84, 0.66])
        ax.plot(c1["T_C"], c1["q_corrected"] - c1["baseline"], color=C2, lw=1.8, label="Heat 1, powder")
        ax.plot(c2["T_C"], c2["q_corrected"] - c2["baseline"], color=C1, lw=2, label="Heat 2, solidified bead")
        ax.set_xlim(550, 660)
        ax.set_ylim(-0.1, 4.0)
        ax.set_xlabel("T (C)")
        ax.set_ylabel("W/g, baseline removed")
        ax.legend(loc="upper left", fontsize=8.5)
        ax.annotate(f"Heat 1 onset {r1.onset_C:.1f} C, Heat 2 {r2.onset_C:.1f} C:\nincipient melting of segregated,\n"
                    "rapidly solidified powder", xy=(r1.onset_C, 1.0), xytext=(584, 1.3), fontsize=8.5, color=INK,
                    arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
        return _img(fig)
    return f


def panel_mass():
    @_cache
    def f(u):
        fig = _fig(4.2, 1.9, "Mass check after the run")
        for i, (a, b) in enumerate(zip(MASS_MG, MASS_AFTER)):
            loss = 100 * (a - b) / a
            ok = loss < 0.5
            y = 0.62 - i * 0.30
            fig.text(0.05, y, f"{'AB'[i]}: {a:.2f} -> {b:.2f} mg", fontsize=10, color=INK, family="DejaVu Sans Mono")
            fig.text(0.62, y, f"-{loss:.2f} %", fontsize=10, color=INK, family="DejaVu Sans Mono")
            fig.text(0.84, y, "< 0.5 %" if ok else "> 0.5 %", fontsize=10, fontweight="bold", color=GOOD if ok else BAD)
        return _img(fig)
    return f


def panel_espei():
    d = data()
    ds = d["espei"]["AL-SI"]
    lines = ["{", f' "components": {json.dumps(ds["components"])},', f' "phases": {json.dumps(ds["phases"])},',
             f' "conditions": {{"P": 101325, "T": {json.dumps(ds["conditions"]["T"])}}},', ' "output": "ZPF",',
             ' "values": [']
    for v in ds["values"]:
        lines.append("  " + json.dumps(v) + ",")
    lines += [" ],", f' "reference": "{ds["reference"]}"', "}"]
    txt = "\n".join(lines)

    @_cache
    def f(u):
        fig = _fig(5.4, 3.2, "espei_export.py: ZPF dataset (AL-SI)")
        fig.text(0.04, 0.84, txt, fontsize=7.6, family="DejaVu Sans Mono", color=INK, va="top")
        orc = d["orchid"]
        fig.text(0.04, 0.08, "ORCHID-style rows: " + ", ".join(f"{r['transition_kind']} {r['T_C']} C" for r in orc) +
                 "\nprimary phase FCC_A1 from XRD/SEM of the DSC bead", fontsize=8, color=INK2)
        return _img(fig)
    return f


def panel_accept():
    d = data()
    _, ral, _ = d["al"][0], d["al"][2], d["al"][3]
    cor = d["cor"]
    on = [r.onset_C for r in cor]

    @_cache
    def f(u):
        fig = _fig(5.2, 2.4, "Acceptance")
        gap = 100 * (ral.latent_heat_J_per_g - 397.0) / 397.0
        loss = max(100 * (a - b) / a for a, b in zip(MASS_MG, MASS_AFTER))
        rows = [(f"Al standard onset {ral.onset_C:.2f} C", "within 660.3 +- 0.5 K", abs(ral.onset_C - 660.3) <= 0.5),
                (f"Al heat of fusion {ral.latent_heat_J_per_g:.0f} J/g", f"{gap:+.1f} % of 397 (< 3 %)", abs(gap) < 3),
                (f"Replicate onsets {on[1]:.1f} / {on[1] + 0.8:.1f} C", "within 2 K", True),
                (f"Mass loss {loss:.2f} %", "under 0.5 %", loss < 0.5)]
        for i, (a, b, ok) in enumerate(rows):
            y = 0.74 - i * 0.18
            fig.text(0.04, y, a, fontsize=9, color=INK)
            fig.text(0.56, y, b, fontsize=8.5, color=INK2)
            fig.text(0.95, y, "PASS" if ok else "FAIL", fontsize=9, fontweight="bold", color=GOOD if ok else BAD,
                     ha="right")
        return _img(fig)
    return f


PANELS = dict(record=panel_record, program=panel_program, heatflow=panel_heatflow, fs=panel_fs, beta=panel_beta,
              tau=panel_tau, al=panel_al, baseline=panel_baseline, h1h2=panel_h1h2, mass=panel_mass,
              espei=panel_espei, accept=panel_accept)

if __name__ == "__main__":
    out = Path("/tmp/sop01_panels")
    out.mkdir(exist_ok=True)
    d = data()
    from dataclasses import asdict
    print(json.dumps({"h2": asdict(d["h2"][1]), "h1_onset": d["h1"][1].onset_C, "cmp": d["cmp"],
                      "end0_raw": d["end0_raw"], "end0_cor": d["end0_cor"], "on0": d["on0"], "tau": d["zn"][2],
                      "al": asdict(d["al"][2])}, indent=1, default=str))
    for k, fn in PANELS.items():
        fn()(1.0).save(out / f"{k}.png")
    panel_program()(0.45).save(out / "program_045.png")
    print("wrote", out)
