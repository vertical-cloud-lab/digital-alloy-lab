"""Figures for the M2 track design (issue #100, PR #243).

    python figures.py     # needs out/ from eagar_tsai_316l.py and design.py
    -> out/m2-track-transients.png   start and end of a track (Eagar-Tsai, finite track)
    -> out/m2-sobol-vs-grid.png      the pilot's Sobol blocks vs. the old 4 x 4 grid, on Eagar-Tsai depth

Palette as in ../m2-viz/figures.py (the repo's dataviz palette): surface #fcfcfb, ink #0b0b0b / #52514e / #898781,
the blue sequential ramp for line energy P/v (darker = more energy per mm), categorical slots 1-4 for panels A-D.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, LogNorm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
import design  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
NEUTRAL_FILL = "#f0efec"
BLUE_RAMP = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281",
             "#0d366b"]
SEQ_FILL = ["#f0efec", "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6",
            "#256abf", "#1c5cab", "#184f95"]
PANEL_C = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a", "D": "#eda100"}   # categorical slots 1-4
ORANGE = "#eb6834"
CMAP = LinearSegmentedColormap.from_list("pv_blue", BLUE_RAMP)
NORM = LogNorm(vmin=0.05, vmax=1.5)


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.9, "axes.labelcolor": INK2, "axes.titlecolor": INK,
        "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "xtick.color": AXIS, "ytick.color": AXIS, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
        "axes.spines.top": False, "axes.spines.right": False,
        "grid.color": GRID, "grid.linewidth": 0.8, "legend.frameon": False,
    })


def read_csv(name):
    with open(OUT / name) as fh:
        return [{k: (float(v) if k not in ("mat",) and v not in ("",) and _isnum(v) else v) for k, v in r.items()}
                for r in csv.DictReader(fh)]


def _isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# ================================================================================================ figure 1
def transients():
    prof = json.loads((OUT / "finite_track_profiles.json").read_text())
    summ = read_csv("finite_track_summary.csv")
    fig, axs = plt.subplots(1, 3, figsize=(13.2, 5.0), gridspec_kw=dict(width_ratios=[1.25, 0.8, 1.05], wspace=0.28))
    base = [r for r in summ if r["spot_um"] == 54 and r["mat"] == "nominal" and r["t_acc_ms"] == 0]
    imid = 64

    def key(r, tacc=0.0):
        return f"{int(r['P'])}W_{r['v']}mps_54um_nominal_tacc{tacc:.1f}ms"

    # (a) start, (b) end: every representative setting, coloured by P/v
    for ax, side in ((axs[0], "start"), (axs[1], "end")):
        for r in sorted(base, key=lambda r: r["E_J_mm"]):
            p = prof[key(r)]
            x = np.array(p["x_um"]) / 1000
            D = np.array(p["D_um"])
            Dm = D[imid]
            if side == "start":
                xs, ys = x[:imid + 1], D[:imid + 1] / Dm
            else:
                xs, ys = p["L_track_um"] / 1000 - x[imid:], D[imid:] / Dm
            ax.plot(xs, ys, color=CMAP(NORM(r["E_J_mm"])), lw=2.0, zorder=3, solid_capstyle="round")
        ax.axhspan(0.99, 1.01, color=NEUTRAL_FILL, zorder=0)
        ax.axhline(1.0, color=AXIS, lw=0.9, zorder=1)
        ax.set_ylim(0.0, 1.12)
        ax.grid(True, axis="y")
        ax.set_axisbelow(True)
    axs[0].set_xlim(0, 0.6)
    axs[0].set_xlabel("distance from the start of the track (mm)")
    axs[0].set_ylabel("melt-pool depth / steady-state depth")
    axs[0].set_title("(a) Start of a track: conduction only")
    axs[1].set_xlim(0.4, 0.0)
    axs[1].set_xlabel("distance before the end of the track (mm)")
    axs[1].set_title("(b) End of a track")
    s1 = max(r["start_D99_um"] for r in base) / 1000
    e1 = max(r["end_D99_um"] for r in base) / 1000
    axs[0].annotate(f"every setting within 1% of steady\nstate by {s1:.2f} mm (9 settings,\n100–375 W, 0.25–2 m/s)",
                    xy=(s1, 0.99), xytext=(0.33, 0.42), fontsize=8.2, color=INK2, ha="left",
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    axs[1].annotate(f"within 1% up to\n{e1:.2f} mm from the end", xy=(e1, 0.99), xytext=(0.37, 0.42), fontsize=8.2,
                    color=INK2, ha="left", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    sm = plt.cm.ScalarMappable(norm=NORM, cmap=CMAP)
    cax = fig.add_axes([0.075, 0.075, 0.34, 0.025])
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cb.ax.text(1.02, 0.5, "line colour: line energy P/v (J/mm, log scale)", transform=cb.ax.transAxes, va="center",
               ha="left", fontsize=8.6, color=INK2)
    cb.outline.set_edgecolor(AXIS)
    cb.set_ticks([0.05, 0.1, 0.2, 0.4, 0.8, 1.5])
    cb.set_ticklabels(["0.05", "0.1", "0.2", "0.4", "0.8", "1.5"])

    # (c) a galvo that ramps speed with the laser on (no skywriting), 0.3 ms ramp
    ax = axs[2]
    cases = [(100, 2.0), (200, 1.0), (375, 0.25)]
    for (P, v), ls in zip(cases, ("-", "-", "-")):
        r = next(r for r in base if r["P"] == P and r["v"] == v)
        c = CMAP(NORM(r["E_J_mm"]))
        for tacc, lw, dash in ((0.0, 1.4, (0, (3, 2))), (0.3, 2.2, None)):
            p = prof[key(r, tacc)]
            x = np.array(p["x_um"]) / 1000
            D = np.array(p["D_um"])
            kw = dict(color=c, lw=lw, zorder=3)
            if dash:
                kw["ls"] = dash
            ax.plot(x[:imid + 1], D[:imid + 1] / D[imid], **kw)
        rr = next(q for q in summ if q["P"] == P and q["v"] == v and q["t_acc_ms"] == 0.3)
        lx, ly = (0.075, rr["D_max_over_mid"] + 0.05) if P != 375 else (0.13, 0.80)
        ax.text(lx, ly, f"{P} W, {v:g} m/s (P/v {P / (v * 1000):.2g} J/mm)", fontsize=8.2, color=INK2,
                va="bottom" if P != 375 else "top", ha="left")
    ax.axhline(1.0, color=AXIS, lw=0.9, zorder=1)
    ax.set_xlim(0, 0.6)
    ax.set_ylim(0.0, 2.05)
    ax.grid(True, axis="y")
    ax.set_axisbelow(True)
    ax.set_xlabel("distance from the start of the track (mm)")
    ax.set_ylabel("melt-pool depth / steady-state depth")
    ax.set_title("(c) Galvo ramp with the laser on (0.3 ms)")
    ax.legend(handles=[Line2D([], [], color=INK2, lw=2.2, label="0.3 ms speed ramp, no skywriting"),
                       Line2D([], [], color=INK2, lw=1.4, ls=(0, (3, 2)), label="instant start (as in a, b)")],
              loc="lower right", fontsize=8.0, labelcolor=INK2, handlelength=2.4)
    fig.text(0.055, 0.985, "How far a single 316L track is from steady state: Eagar–Tsai over the time the laser is on",
             ha="left", va="top", fontsize=12, fontweight="bold", color=INK)
    fig.text(0.055, 0.935, "Conduction only, 54 µm spot (1/e²), absorptivity 0.4, constant 316L properties (α = 5.0e-6 m²/s)."
             " Depth on the track's centre line at each transverse section. Keyhole start-up, powder and laser"
             " on/off delays are not in the model.", ha="left", va="top", fontsize=8.6, color=INK2, wrap=True)
    fig.subplots_adjust(left=0.055, right=0.985, top=0.83, bottom=0.25)
    fig.savefig(OUT / "m2-track-transients.png", dpi=160)
    plt.close(fig)


# ================================================================================================ figure 2
def sobol_vs_grid():
    grid = [r for r in read_csv("steady_state_grid.csv") if r["spot_um"] == 54]
    Ps = sorted({r["P"] for r in grid})
    Vs = sorted({r["v"] for r in grid})
    Dm = np.array([[next(r["D"] for r in grid if r["P"] == P and r["v"] == v) for v in Vs] for P in Ps])
    sets = design.pilot_sets()
    fig, axs = plt.subplots(1, 2, figsize=(12.6, 5.9), gridspec_kw=dict(wspace=0.2))
    VV = np.array(Vs) * 1000.0   # mm/s
    levels = [0, 15, 30, 45, 60, 80, 100, 125, 150, 200, 250, 300]
    for ax, which in ((axs[0], "grid"), (axs[1], "sobol")):
        cs = ax.contourf(VV, Ps, Dm, levels=levels, colors=SEQ_FILL[:len(levels) - 1], zorder=0)
        cl = ax.contour(VV, Ps, Dm, levels=[30, 60, 100, 150, 200], colors=[MUTED], linewidths=0.7, zorder=1)
        ax.clabel(cl, fmt="%d µm", fontsize=7.2, colors=INK2)
        ax.add_patch(plt.Rectangle((design.V_RANGE[0], design.P_RANGE[0]), design.V_RANGE[1] - design.V_RANGE[0],
                                   design.P_RANGE[1] - design.P_RANGE[0], fill=False, ec=INK2, lw=1.0, ls=(0, (4, 2)),
                                   zorder=2))
        if which == "grid":
            P = [p for p in (100, 200, 300, 375) for _ in range(4)]
            V = [v for _ in range(4) for v in (250, 500, 1000, 2000)]
            ax.scatter(V, P, s=90, c=INK, edgecolors=SURFACE, linewidths=1.5, zorder=4)
            ax.set_title("(a) The old plan: 4 × 4 grid, repeated on every panel")
            ax.text(0.02, 0.02, "4 powers × 4 speeds; each panel repeats the same 16", transform=ax.transAxes,
                    fontsize=8.3, color=INK2, bbox=dict(boxstyle="square,pad=0.25", fc=SURFACE, ec="none"))
        else:
            for k in design.PANELS:
                b = [s for s in sets if s["panel"] == k]
                ax.scatter([s["v"] for s in b], [s["P"] for s in b], s=58, c=PANEL_C[k], edgecolors=SURFACE,
                           linewidths=1.4, zorder=4, label=f"panel {k}: Sobol points {design.PANELS.index(k) * 16}–"
                                                          f"{design.PANELS.index(k) * 16 + 15}")
            ax.set_title("(b) Pilot: 64 scrambled-Sobol points, one 16-point block per panel")
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=8.2, labelcolor=INK2,
                      handletextpad=0.3, columnspacing=1.6)
        ax.set_xscale("log")
        ax.set_xlim(150, 3000)
        ax.set_ylim(50, 400)
        ax.set_xticks([250, 500, 1000, 2000])
        ax.set_xticklabels(["250", "500", "1000", "2000"])
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.set_xlabel("scan speed v (mm/s, log scale)")
        ax.set_ylabel("laser power P (W)")
    cbar = fig.colorbar(cs, cax=fig.add_axes([0.915, 0.235, 0.012, 0.6]))
    cbar.set_label("Eagar–Tsai steady-state depth (µm)", color=INK2)
    cbar.outline.set_edgecolor(AXIS)
    rep = design.discrepancy_report(sets)
    fig.text(0.055, 0.985, "Sampling the pilot's power–speed window: Sobol blocks instead of a grid", ha="left",
             va="top", fontsize=12, fontweight="bold", color=INK)
    fig.text(0.055, 0.945, f"Each panel's 16 points cover the whole box (centred discrepancy {rep['sobol_panel_A']:.4f}"
             f" vs. {rep['grid_4x4']:.4f} for the grid); all 64 give {rep['distinct_P_levels_sobol']} powers and "
             f"{rep['distinct_v_levels_sobol']} speeds. Plus 2 controls per panel (the machine's standard set).\n"
             "Background: Eagar–Tsai steady-state depth for 316L, absorptivity 0.4, 54 µm spot. Dashed box: the "
             "sampled window, 100–375 W and 250–2000 mm/s (log scale).",
             ha="left", va="top", fontsize=8.6, color=INK2, linespacing=1.45)
    fig.subplots_adjust(left=0.055, right=0.9, top=0.84, bottom=0.235)
    fig.savefig(OUT / "m2-sobol-vs-grid.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    style()
    which = sys.argv[1:] or ["transients", "sobol"]
    if "transients" in which:
        transients()
    if "sobol" in which:
        sobol_vs_grid()
