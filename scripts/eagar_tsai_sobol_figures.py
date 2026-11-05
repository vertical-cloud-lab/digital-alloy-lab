"""Figures for scripts/eagar_tsai_sobol_analysis.py (issue #235). Called by its ``analyse --figures DIR``."""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import eagar_tsai_sobol_alsi10mg as sweep
from eagar_tsai_sobol_analysis import OUT_UM, T0_K, T_BOIL_AL_K, PeakFactor, Surrogate

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
LABEL = {"melt_width_um": "Width W", "melt_depth_um": "Depth D", "melt_length_um": "Length L", "peak_temperature": "Peak temperature"}
INPUT_LABEL = {"beam_diameter_m": "Beam diameter", "power_w": "Power", "velocity_m_s": "Speed", "absorptivity": "Absorptivity"}

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.titlesize": 11,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.labelsize": 9.5,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.frameon": False,
        "legend.fontsize": 8.5,
        "legend.labelcolor": INK2,
        "font.size": 9.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def _rows_for(theta: np.ndarray, p: np.ndarray) -> pd.DataFrame:
    """Any physical rows with the given (Theta, p): AlSi10Mg, v = 1 m/s, A = 1. Only (Theta, p) matter."""
    m = sweep.MATERIAL
    alpha = m["thermal_conductivity_w_mk"] / (m["density_kg_m3"] * m["specific_heat_j_kgk"])
    rho_c = m["density_kg_m3"] * m["specific_heat_j_kgk"]
    s = alpha / (1.0 * p)
    S = theta * (m["liquidus_temperature_k"] - T0_K)
    rows = pd.DataFrame(
        {
            "beam_diameter_m": s * 2.0 / np.sqrt(2.0),
            "power_w": S * np.pi * rho_c * np.sqrt(np.pi * alpha * 1.0 * s**3),
            "velocity_m_s": 1.0,
            "absorptivity": 1.0,
        }
    )
    for k, v in m.items():
        rows[k] = v
    return rows


def fig_reduction(train: pd.DataFrame, peak: PeakFactor, sur: Surrogate, summary: dict, path: pathlib.Path) -> None:
    from eagar_tsai_sobol_analysis import groups

    g = groups(train)
    m = sweep.MATERIAL
    fig, (a, b) = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={"width_ratios": [1, 1.25]})

    p_line = np.logspace(np.log10(g["p"].min()) - 0.1, np.log10(g["p"].max()) + 0.1, 300)
    dev = summary["peak_factor_vs_eagar_tsai_grid"]["max_rel_diff"]
    a.scatter(g["p"], (train["peak_temperature"] - T0_K) / g["S_K"], s=9, color=BLUE, alpha=0.5, linewidths=0, label=f"eagar-tsai, {len(train):,} sweep rows (all within {dev:.2%})")
    a.plot(p_line, peak(p_line), color=INK, lw=1.2, label="max of the eagar-tsai integral, G(p)")
    a.set_xscale("log")
    a.set_xlabel("p = α / (v s)        (s = √2 · beam_diameter / 2)")
    a.set_ylabel("(T_peak − T0) / S")
    a.set_title("Peak temperature: one curve of one number")
    a.legend(loc="upper right")

    # Regime map in (p, Theta).
    colors = {"no_melt": MUTED, "conduction": BLUE, "above_boiling": ORANGE}
    names = {"no_melt": "does not melt", "conduction": "melts, peak below Al boiling point", "above_boiling": "peak above Al boiling point (2743 K)"}
    for key in ("no_melt", "conduction", "above_boiling"):
        sel = train["regime"] == key
        b.scatter(g.loc[sel, "p"], g.loc[sel, "theta"], s=9, color=colors[key], alpha=0.55 if key != "no_melt" else 0.35, linewidths=0, label=f"{names[key]} ({sel.mean():.0%})")
    G = peak(p_line)
    theta_boil = (T_BOIL_AL_K - T0_K) / (m["liquidus_temperature_k"] - T0_K)
    b.plot(p_line, 1.0 / G, color=INK, lw=1.4)
    b.plot(p_line, theta_boil / G, color=INK, lw=1.2, ls=(0, (5, 3)))
    # Keyhole test of eagar-tsai's printability map (W/D <= 2.5), as a curve in (p, Theta).
    pp, tt = np.meshgrid(np.logspace(np.log10(p_line[0]), np.log10(p_line[-1]), 160), np.logspace(np.log10(g["theta"].min()), np.log10(g["theta"].max()), 160))
    pr = sur.predict(_rows_for(tt.ravel(), pp.ravel()))
    ok = (pr["melt_depth_um"] > 0) & ~pr["extrapolated"]  # only where the surrogate interpolates
    wd = (pr["melt_width_um"] / pr["melt_depth_um"]).where(ok).to_numpy().reshape(pp.shape)
    b.contourf(pp, tt, wd, levels=[0, 2.5], colors=[AQUA], alpha=0.12)
    cs = b.contour(pp, tt, wd, levels=[2.5], colors=[AQUA], linewidths=1.4)
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlim(p_line[0], p_line[-1])
    b.set_ylim(g["theta"].min(), g["theta"].max())
    b.set_xlabel("p = α / (v s)")
    b.set_ylabel("Θ = S / (T_liq − T0)")
    b.set_title("Every sweep row, placed by its two numbers")
    i = int(len(p_line) * 0.06)
    b.annotate("melting starts: Θ·G(p) = 1", (p_line[i], 1.0 / G[i]), xytext=(0, -13), textcoords="offset points", color=INK, fontsize=8.5)
    b.annotate("boiling: Θ·G(p) = 4.3", (p_line[i], theta_boil / G[i]), xytext=(0, 5), textcoords="offset points", color=INK, fontsize=8.5)
    handles, labels = b.get_legend_handles_labels()
    if cs.allsegs[0]:
        from matplotlib.patches import Patch

        handles.append(Patch(facecolor=AQUA, alpha=0.3, edgecolor=AQUA))
        labels.append("W/D ≤ 2.5, which eagar-tsai's printability\ntest calls keyhole")
    b.legend(handles, labels, loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_holdout(holdout: pd.DataFrame, summary: dict, path: pathlib.Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.4), layout="constrained")
    err = summary["holdout_error"]
    for ax, c in zip(axes, OUT_UM, strict=True):
        x, y = holdout[c], holdout[f"{c}_surrogate"]
        lim = max(x.max(), y.max()) * 1.04
        ax.plot([0, lim], [0, lim], color=MUTED, lw=1)
        ax.scatter(x, y, s=9, color=BLUE, alpha=0.5, linewidths=0)
        ax.set_xlim(0, lim)
        ax.set_ylim(0, lim)
        ax.set_aspect("equal")
        ax.set_xlabel(f"{LABEL[c]} from eagar-tsai (µm)")
        ax.set_ylabel(f"{LABEL[c]} from the surrogate (µm)")
        e = err[c]
        ax.set_title(LABEL[c])
        ax.text(0.04, 0.96, f"median |error| {e['median_abs']:.1f} µm\n95% within {e['p95_abs']:.1f} µm\nworst {e['max_abs']:.1f} µm", transform=ax.transAxes, va="top", color=INK2, fontsize=8.5)
    fig.suptitle(f"Surrogate against eagar-tsai on {summary['n_holdout']:,} random rows of the 2²⁰ design that were not used to build it", x=0.01, ha="left", color=INK, fontsize=10.5)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_sobol(summary: dict, path: pathlib.Path) -> None:
    sob = summary["sobol_surrogate"]
    outs = list(sob)
    fig, axes = plt.subplots(1, len(outs), figsize=(12, 3.6), sharey=True, layout="constrained")
    inputs = list(INPUT_LABEL)
    y = np.arange(len(inputs))
    for ax, o in zip(axes, outs, strict=True):
        st = np.array([sob[o][x]["ST"] for x in inputs])
        s1 = np.array([sob[o][x]["S1"] for x in inputs])
        ax.barh(y - 0.17, st, height=0.32, color=BLUE, label="total effect")
        ax.barh(y + 0.17, s1, height=0.32, color=ORANGE, label="first order (alone)")
        for yi, v in zip(y, st, strict=True):
            ax.text(v + 0.015, yi - 0.17, f"{v:.2f}", va="center", fontsize=8, color=INK2)
        ax.set_xlim(0, 1.0)
        ax.set_title(LABEL[o])
        ax.set_yticks(y, [INPUT_LABEL[x] for x in inputs])
        ax.invert_yaxis()
        ax.grid(axis="y", visible=False)
        ax.set_xlabel("Sobol index")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper right", ncols=2, fontsize=8.5)
    fig.suptitle("Sobol indices over the sweep box, from the surrogate", x=0.01, ha="left", color=INK, fontsize=10.5)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def make_all(train, holdout, peak, sur, summary, out: pathlib.Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fig_reduction(train, peak, sur, summary, out / "sobol-reduction.png")
    fig_holdout(holdout, summary, out / "sobol-surrogate-holdout.png")
    fig_sobol(summary, out / "sobol-indices.png")
    print(f"figures in {out}")
