"""Static figures for the M2 single-track pilot (issue #100).

    python figures.py      # -> out/m2-pilot-design.png, out/m2-schedule.png

Every number comes from ../m2-single-track-schedule.md: the 64 Sobol power-speed settings (layout.pilot_sets(), from
../m2-track-design/design.py) and the insert layout (section 4),
the run sheet (section 5) and the schedule (section 6). The track map in the first figure is an example randomization;
the real one comes from the job file (step A1). Durations are the plan's estimates, not measurements.

Colours follow the dataviz palette used for the repo's charts: surface #fcfcfb, ink #0b0b0b / #52514e / #898781, the
blue sequential ramp for line energy (darker = more energy per mm), and categorical slots 1-3 (blue, orange, aqua) for
the run's phases A (prep), B (machine day) and C (post-processing).
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.cm import ScalarMappable  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, LogNorm  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Polygon, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))
import layout as L  # noqa: E402  (the shared parameter sets and track map; the 3-D animation uses the same)

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
NEUTRAL_FILL = "#f0efec"
STEEL = "#e6e4dd"
BLUE_RAMP = ["#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281",
             "#0d366b"]                                    # sequential blue, steps 250..700
PHASE = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}   # categorical slots 1-3
PHASE_NAME = {"A": "A  prep", "B": "B  machine day", "C": "C  post-processing"}
VIOLET = "#6250d6"                                          # categorical slot 7, only on its own labelled row
CONTROL = INK2

CMAP = LinearSegmentedColormap.from_list("pv_blue", BLUE_RAMP)
NORM = LogNorm(vmin=0.05, vmax=1.5)

SPEEDS = list(L.SPEEDS_MM_S)             # mm/s
POWERS = list(L.POWERS_W)                # W, for a 400 W M2
PILOT_SETS = L.pilot_sets()             # 64 Sobol settings, 16 per panel
ISO_E = [0.05, 0.1, 0.2, 0.4, 0.8, 1.5]  # J/mm


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.9,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.titlesize": 10.5,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "xtick.color": AXIS,
        "ytick.color": AXIS,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",
        "legend.frameon": False,
        "hatch.color": AXIS,
        "hatch.linewidth": 0.8,
    })


# ================================================================================================ figure 1
def panel_grid(ax):
    vmin, vmax, ylo, yhi = 175.0, 2900.0, 40.0, 440.0
    v = np.geomspace(vmin, vmax, 300)
    for E in ISO_E:
        ax.plot(v, E * v, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
        if E * vmax > yhi * 0.95:                # leaves through the top: label just under the top edge
            y = yhi * 0.955
            x = y / E
            ax.text(x, y, f"{E:g} J/mm", ha="center", va="top", fontsize=7.6, color=MUTED, zorder=2,
                    bbox=dict(boxstyle="square,pad=0.15", fc=SURFACE, ec="none"))
        else:                                    # leaves through the right edge
            x = vmax * 0.965
            ax.text(x, E * x, f"{E:g} J/mm", ha="right", va="bottom", fontsize=7.6, color=MUTED, zorder=2,
                    bbox=dict(boxstyle="square,pad=0.15", fc=SURFACE, ec="none"))
    P = np.array([s["P"] for s in PILOT_SETS], float)
    V = np.array([s["v"] for s in PILOT_SETS], float)
    ax.add_patch(Rectangle((250, 100), 2000 - 250, 375 - 100, fill=False, ec=INK2, lw=1.0, ls=(0, (4, 2)), zorder=3))
    ax.scatter(V, P, s=70, c=P / V, cmap=CMAP, norm=NORM, edgecolors=SURFACE, linewidths=1.3, zorder=4)
    ax.text(2000, 66, "likely balling /\nlack of fusion", ha="center", va="center", fontsize=8, color=INK2, zorder=5,
            linespacing=1.15, bbox=dict(boxstyle="square,pad=0.15", fc=SURFACE, ec="none"))
    ax.text(250, 352, "deep\nkeyholes", ha="center", va="top", fontsize=8, color=INK2, zorder=5, linespacing=1.15,
            bbox=dict(boxstyle="square,pad=0.15", fc=SURFACE, ec="none"))
    ax.set_xscale("log", base=2)
    ax.set_xlim(vmin, vmax)
    ax.set_ylim(ylo, yhi)
    ax.set_xticks(SPEEDS)
    ax.set_xticklabels([str(s) for s in SPEEDS])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_yticks(POWERS)
    ax.set_xlabel("scan speed v (mm/s, log scale)")
    ax.set_ylabel("laser power P (W)")
    ax.grid(True, axis="both", zorder=0)
    ax.set_axisbelow(True)
    ax.text(0.0, -0.15, "+ control: the machine's standard stainless set, 2 tracks per panel (values from Josh)",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.3, color=INK2)
    ax.text(0.0, -0.205, "Scrambled Sobol in (P, log v) over the dashed box, for a 400 W M2; one 16-point block per panel.",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.3, color=MUTED)


def panel_tracks(bx, tmap):
    # plate positions as in the animation: A, B at the outlet side (low y), C, D at the inlet side
    origins = {"A": (0.0, 0.0), "B": (32.0, 0.0), "C": (0.0, 32.0), "D": (32.0, 32.0)}
    for ins, (x0, y0) in origins.items():
        bx.add_patch(Rectangle((x0, y0), L.BLOCK, L.BLOCK, fc=STEEL, ec=AXIS, lw=1.0, zorder=1))
        # orientation notch on the left side
        bx.add_patch(Polygon([(x0 - 0.05, y0 + 11.2), (x0 + 1.3, y0 + 12.5), (x0 - 0.05, y0 + 13.8)], closed=True,
                             fc=SURFACE, ec=AXIS, lw=1.0, zorder=2))
        bx.text(x0, y0 + 25.7, f"Panel {ins}", ha="left", va="bottom", fontsize=9.5, fontweight="bold", color=INK)
        for (xa, xb) in L.ROW_X:                    # section planes at each row's mid-length
            xc = (xa + xb) / 2
            bx.plot([x0 + xc, x0 + xc], [y0 + 1.6, y0 + 23.4], color=INK, lw=1.1, ls=(0, (3.2, 2.2)), zorder=5)
        xs = (L.ROW_X[0][1] + L.ROW_X[1][0]) / 2     # bandsaw split between the rows
        bx.plot([x0 + xs, x0 + xs], [y0 - 0.9, y0 + 24.3], color=MUTED, lw=1.4, ls=(0, (0.9, 1.9)), zorder=5,
                dash_capstyle="round")
    for t in tmap:
        x0, y0 = origins[t["insert"]]
        (xa, y), (xb, _) = t["start"], t["end"]
        c = CMAP(NORM(t["E"])) if t["E"] is not None else CONTROL
        bx.add_patch(FancyBboxPatch((x0 + xa, y0 + y - 0.5), xb - xa, 1.0, boxstyle="round,pad=0,rounding_size=0.35",
                                    fc=c, ec="none", zorder=3))
        if t["E"] is None:
            cx = x0 + (xa - 1.45 if t["row"] == 1 else xb + 1.45)
            bx.text(cx, y0 + y, "C", ha="center", va="center", fontsize=6.6, fontweight="bold", color=INK, zorder=4)
    # scan direction, once
    bx.add_patch(FancyArrowPatch((3.0, 63.0), (11.0, 63.0), arrowstyle="-|>", mutation_scale=11, color=INK2, lw=1.3))
    bx.text(12.3, 63.0, "scan direction: the same on every track", ha="left", va="center", fontsize=8.2, color=INK2)
    # gas flow (assumed) and exposure order
    gx = 62.5
    bx.add_patch(FancyArrowPatch((gx, 55.5), (gx, 1.5), arrowstyle="-|>", mutation_scale=13, color=MUTED, lw=1.6))
    bx.text(gx, 57.0, "gas inlet\n(assumed)", ha="center", va="bottom", fontsize=7.8, color=INK2, linespacing=1.1)
    bx.text(gx, 0.0, "gas outlet", ha="center", va="top", fontsize=7.8, color=INK2)
    bx.text(gx + 1.6, 28.5, "gas flow", ha="left", va="center", fontsize=7.8, color=INK2, rotation=-90)
    ex = -5.0
    bx.add_patch(FancyArrowPatch((ex, 1.5), (ex, 55.5), arrowstyle="-|>", mutation_scale=13, color=INK2, lw=1.6))
    bx.text(ex - 1.4, 28.5, "exposure order: A, B, then C, D; each from low y up", ha="right", va="center",
            fontsize=7.8, color=INK2, rotation=90)
    bx.set_xlim(-11, 70)
    bx.set_ylim(-4.5, 66.5)
    bx.set_aspect("equal")
    bx.axis("off")
    handles = [
        Patch(fc=CMAP(NORM(0.3)), ec="none", label="Sobol track, coloured by P/v as in (a)"),
        Patch(fc=CONTROL, ec="none", label="C = control track (standard set)"),
        Line2D([], [], color=INK, lw=1.1, ls=(0, (3.2, 2.2)), label="section plane at each row's mid-length"),
        Line2D([], [], color=MUTED, lw=1.4, ls=(0, (0.9, 1.9)), label="bandsaw split between the two rows"),
    ]
    bx.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.0), ncol=2, fontsize=8.0,
              handlelength=2.4, columnspacing=1.6, labelcolor=INK2, borderaxespad=0.2)
    bx.text(0.0, -0.1, "The 25 mm track block at each panel's centre, as in the animation (layout.py): 8 mm tracks at 2 mm\n"
                       "pitch in two rows. The plan (§4) now has one row of 18 tracks, 10 mm long. Tracks drawn 1 mm wide.",
            transform=bx.transAxes, ha="left", va="top", fontsize=7.6, color=MUTED, linespacing=1.3)


def pilot_design():
    fig = plt.figure(figsize=(13.4, 7.2), dpi=200)
    gs = fig.add_gridspec(1, 4, width_ratios=[1.0, 0.035, 0.10, 1.38], wspace=0.06, left=0.055, right=0.995,
                          top=0.79, bottom=0.165)
    ax = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])
    fig.add_subplot(gs[0, 2]).axis("off")
    bx = fig.add_subplot(gs[0, 3])
    bx.set_anchor("W")                               # equal aspect shrinks the box; keep it at the cell's left edge
    panel_grid(ax)
    cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), cax=cax, ticks=ISO_E)
    cb.ax.set_yticklabels([f"{e:g}" for e in ISO_E])
    cb.ax.minorticks_off()
    cb.outline.set_edgecolor(AXIS)
    cb.ax.tick_params(colors=AXIS, labelcolor=INK2, labelsize=8)
    cb.set_label("line energy P/v (J/mm)", color=INK2)
    panel_tracks(bx, L.track_map())
    ty = 0.875
    fig.text(gs[0, 0].get_position(fig).x0, ty, "(a) 64 Sobol settings + 1 control set (65 per run)", ha="left",
             va="top", fontsize=10.5, fontweight="bold", color=INK)
    bx0 = gs[0, 3].get_position(fig).x0
    fig.text(bx0, ty, "(b) 72 tracks on 4 panels: one Sobol block per panel", ha="left", va="top", fontsize=10.5,
             fontweight="bold", color=INK)
    fig.text(bx0, ty - 0.033, "Example randomization (seed 100); the real map comes from the job file (A1).\n"
                              "Gas-flow direction assumed; tracks are exposed from the outlet side toward the inlet.",
             ha="left", va="top", fontsize=8.2, color=INK2, linespacing=1.35)
    fig.text(0.055, 0.975, "M2 single-track pilot (issue #100): power-speed settings and track layout", ha="left",
             va="top", fontsize=12.5, fontweight="bold", color=INK)
    fig.text(0.055, 0.937, "316L inserts in Nathan C.'s four-insert plate; one powder layer; one run = 72 tracks "
                           "(4 panels x [16 Sobol + 2 control]).", ha="left", va="top", fontsize=9, color=INK2)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "m2-pilot-design.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


# ================================================================================================ figure 2
# (id, short name, phase, first run (lo, hi) h, its text, routine (lo, hi) h, its text), from the section 5 run sheet
STEPS = [
    ("A1", "Job file, slice, vector preview, track map", "A", (4, 8), "4–8 h", (0.5, 1), "0.5–1 h"),
    ("A2", "AM Module predictions (before printing)", "A", (8, 16), "1–2 days of setup", (1, 1), "~1 h"),
    ("A3", "Panels: cut, machine, drill, grind flush", "A", (8, 16), "1–2 days for a batch of 8", (1, 4),
     "1–2 h per panel, 1–2 a run"),
    ("B1", "Machine check: gas, filter, laser power", "B", (0.5, 1), "0.5–1 h", (0.25, 0.5), "15–30 min"),
    ("B2", "Install plate + panels, check flushness", "B", (0.5, 1), "0.5–1 h", (0.5, 0.5), "30 min"),
    ("B3", "Load and sieve powder", "B", (0.5, 1), "0.5–1 h", (0.5, 0.5), "30 min"),
    ("B4", "Close up, inert to O₂ setpoint", "B", (0.5, 1), "0.5–1 h", (0.5, 1), "0.5–1 h"),
    ("B5", "Recoat one layer, expose all tracks", "B", (0, 0.25), "< 15 min", (0, 0.25), "< 15 min"),
    ("B6", "Cool and de-inert", "B", (0.25, 0.5), "15–30 min", (0.25, 0.5), "15–30 min"),
    ("B7", "Depowder, photograph, unscrew panels", "B", (0.5, 1), "0.5–1 h", (0.5, 0.5), "30 min"),
    ("B8", "Clean machine, powder, waste", "B", (1, 2), "1–2 h", (1, 1), "1 h"),
    ("C1", "Top-view images of each panel", "C", (1, 1), "1 h", (0.5, 0.5), "30 min"),
    ("C2", "Bandsaw strip, pieces; fine saw (8)", "C", (3, 5), "3–5 h", (2, 3), "2–3 h"),
    ("C3", "Hot-mount 8 pucks", "C", (2, 3), "2–3 h", (2, 2), "2 h"),
    ("C4", "Grind, polish, etch", "C", (4, 6), "4–6 h", (3, 4), "3–4 h"),
    ("C5", "SEM: 72 tracks x 2 mags (+ EDS)", "C", (4, 5), "4–5 h", (3, 3), "3 h"),
    ("C6", "Measure; classify regime", "C", (3, 4), "3–4 h", (2, 2), "2 h (less once automated)"),
    ("C7", "Upload; compare with predictions", "C", (2, 2), "2 h", (1, 1), "1 h"),
]


def totals():
    out = {}
    for ph in "ABC":
        rows = [s for s in STEPS if s[2] == ph]
        out[ph] = {"first": (sum(r[3][0] for r in rows), sum(r[3][1] for r in rows)),
                   "routine": (sum(r[5][0] for r in rows), sum(r[5][1] for r in rows))}
    return out


def fmt_h(lo, hi):
    f = lambda x: f"{x:g}"   # noqa: E731
    return f"{f(lo)}–{f(hi)} h" if lo != hi else f"{f(lo)} h"


def panel_steps(ax, which, ys, show_labels):
    idx, tidx = (3, 4) if which == "first" else (5, 6)
    for y, s in zip(ys, STEPS):
        lo, hi = s[idx]
        c = PHASE[s[2]]
        if hi > lo:
            ax.barh(y, hi - lo, left=lo, height=0.62, color=c, zorder=3, edgecolor=c, linewidth=0.6,
                    joinstyle="round")
        else:
            ax.scatter([lo], [y], s=62, color=c, edgecolors=SURFACE, linewidths=1.4, zorder=4)
        txt = s[tidx]
        if hi - lo >= 5.5:      # long bar: label inside, white on the fill
            ax.text(lo + 0.3, y, txt, ha="left", va="center", fontsize=7.8, color="#ffffff", zorder=5)
        else:
            ax.text(hi + 0.32, y, txt, ha="left", va="center", fontsize=7.8, color=INK2, zorder=5)
    ax.set_xlim(0, 17)
    ax.set_xticks(range(0, 17, 2))
    ax.grid(True, axis="x", zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel("hours per step (estimate)")
    ax.set_ylim(max(ys) + 0.9, min(ys) - 0.9)
    ax.set_yticks(ys)
    if show_labels:
        ax.set_yticklabels([f"{s[0]}   {s[1]}" for s in STEPS], fontsize=8.4)
    else:
        ax.tick_params(axis="y", labelleft=False, length=0)
        ax.spines["left"].set_visible(False)
    ax.set_title("First run (est.)" if which == "first" else "Routine (est.)", fontsize=10, pad=6)
    t = totals()
    plan = {"first": {"A": "", "B": "  (plan: 4–8 h)", "C": "  (plan: about 2–3 person-days)"},
            "routine": {"A": "", "B": "  (plan: about 4 h)", "C": ""}}[which]
    lines = [f"{ph}1–{ph}{sum(1 for s in STEPS if s[2] == ph)}: {fmt_h(*t[ph][which])}{plan[ph]}" for ph in "ABC"]
    ax.text(0.985, 0.035, "Sum of step ranges\n" + "\n".join(lines), transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.9, color=INK2, linespacing=1.35,
            bbox=dict(boxstyle="round,pad=0.45,rounding_size=0.3", fc=SURFACE, ec=GRID, lw=0.9))


def d(y, m, dd):
    return mdates.date2num(dt.datetime(y, m, dd))


def panel_gantt(g):
    rows = [
        ("Kickoff, safety training, AM Module set-up", (2026, 11, 9), (2026, 11, 13), PHASE["A"]),
        ("Panels, job file + dry run, laser check, predictions", (2026, 11, 16), (2026, 11, 20), PHASE["A"]),
        ("Pilot print (Mon 11/23 or Tue 11/24); section panel A", (2026, 11, 23), (2026, 11, 24), PHASE["B"]),
        ("Metallography on panels A–D; SEM session", (2026, 11, 30), (2026, 12, 4), PHASE["C"]),
        ("Measure, compare with predictions, pilot write-up", (2026, 12, 7), (2026, 12, 11), PHASE["C"]),
        ("Finals and holidays: light work", (2026, 12, 14), (2027, 1, 8), "light"),
        ("Campaign: about 1 run a week", (2027, 1, 11), (2027, 2, 19), "campaign"),
        ("Calibrate + validate, parity plots, talk figures", (2027, 2, 22), (2027, 3, 5), VIOLET),
        ("TMS 2027, Orlando (Mar 14–18)", (2027, 3, 14), (2027, 3, 18), INK2),
    ]
    ys = list(range(len(rows)))
    h = 0.56
    x0, x1 = d(2026, 11, 9) - 0.5, d(2027, 3, 19) + 0.5
    # month gridlines and Thanksgiving
    for m in [(2026, 12, 1), (2027, 1, 1), (2027, 2, 1), (2027, 3, 1)]:
        g.axvline(d(*m), color=GRID, lw=0.8, zorder=0)
    tg = d(2026, 11, 26) + 0.5
    g.axvline(tg, color=AXIS, lw=0.9, zorder=1)
    g.text(tg + 0.6, -0.95, "Thanksgiving (Thu 11/26)", ha="left", va="center", fontsize=7.4, color=MUTED)
    for y, (name, a, b, c) in zip(ys, rows):
        left, width = d(*a), d(*b) + 1 - d(*a)
        if c == "light":
            g.add_patch(Rectangle((left, y - h / 2), width, h, fc=NEUTRAL_FILL, ec=AXIS, lw=0.8, hatch="////",
                                  zorder=2))
            g.text(left + width + 0.8, y, "campaign panels, campaign predictions, automate the measurement",
                   ha="left", va="center", fontsize=7.6, color=INK2)
        elif c == "campaign":
            g.add_patch(Rectangle((left, y - h / 2), width, h, fc=NEUTRAL_FILL, ec=AXIS, lw=0.8, zorder=2))
            for k in range(6):
                tick = d(2027, 1, 12) + 7 * k          # a Tuesday each week; the real day is Josh's slot
                g.add_patch(Rectangle((tick, y - h / 2 + 0.06), 1.0, h - 0.12, fc=PHASE["B"], ec="none", zorder=3))
                g.text(tick + 0.5, y - h / 2 - 0.08, str(k + 1), ha="center", va="bottom", fontsize=7.6,
                       color=INK2)
            g.text(left + width + 0.8, y, "runs 1–2: fill out the grid\nruns 3–5: refine the boundaries (BO)\n"
                                          "run 6: buffer or repeats", ha="left", va="center", fontsize=7.6,
                   color=INK2, linespacing=1.15)
        else:
            g.add_patch(Rectangle((left, y - h / 2), width, h, fc=c, ec="none", zorder=2))
    gates = [(0, (2026, 11, 13), "machine running, plate located"), (1, (2026, 11, 20), "dry run passes"),
             (2, (2026, 11, 24), "72 tracks printed and mapped"), (4, (2026, 12, 11), "go/no-go with Sterling (Fri)")]
    for y, day, text in gates:
        xd = d(*day) + 0.5
        g.scatter([xd], [y], marker="D", s=46, color=INK, edgecolors=SURFACE, linewidths=1.2, zorder=6)
        g.text(xd + 1.3, y, text, ha="left", va="center", fontsize=7.8, color=INK, zorder=6,
               bbox=dict(boxstyle="square,pad=0.12", fc=SURFACE, ec="none"))
    g.set_xlim(x0, x1)
    g.set_ylim(len(rows) - 0.4, -1.4)
    g.set_yticks(ys)
    g.set_yticklabels([r[0] for r in rows], fontsize=8.4)
    ticks = [d(2026, 11, 9), d(2026, 12, 1), d(2027, 1, 1), d(2027, 2, 1), d(2027, 3, 1)]
    g.set_xticks(ticks)
    g.set_xticklabels(["Mon Nov 9, 2026", "Dec 1", "Jan 1, 2027", "Feb 1", "Mar 1"])
    g.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    g.tick_params(axis="x", which="minor", length=3, color=AXIS)
    g.tick_params(axis="y", length=0)
    g.spines["left"].set_visible(False)
    g.set_xlabel("week ticks are Mondays", color=MUTED, fontsize=8)
    handles = [Patch(fc=PHASE["A"], label="prep (A)"), Patch(fc=PHASE["B"], label="machine day (B)"),
               Patch(fc=PHASE["C"], label="post-processing (C)"), Patch(fc=VIOLET, label="analysis + talk"),
               Patch(fc=NEUTRAL_FILL, ec=AXIS, hatch="////", label="light work"),
               Line2D([], [], marker="D", ls="none", color=INK, markeredgecolor=SURFACE, markersize=6.5,
                      label="gate")]
    g.legend(handles=handles, loc="upper right", bbox_to_anchor=(1.0, 1.0), ncol=3, fontsize=8, labelcolor=INK2,
             handlelength=1.6, columnspacing=1.4)


def schedule():
    fig = plt.figure(figsize=(13.4, 12.2), dpi=200)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1.0], hspace=0.30, wspace=0.05, left=0.255, right=0.985,
                          top=0.905, bottom=0.06)
    a1 = fig.add_subplot(gs[0, 0])
    a2 = fig.add_subplot(gs[0, 1])
    g = fig.add_subplot(gs[1, :])
    ys, y = [], 0.0
    for i, s in enumerate(STEPS):
        if i and s[2] != STEPS[i - 1][2]:
            y += 0.55                                # a gap between phases
        ys.append(y)
        y += 1.0
    panel_steps(a1, "first", ys, True)
    panel_steps(a2, "routine", ys, False)
    panel_gantt(g)
    fig.text(0.012, 0.985, "M2 single-track pilot (issue #100): run sheet and schedule", ha="left", va="top",
             fontsize=12.5, fontweight="bold", color=INK)
    fig.text(0.012, 0.962, "(a) Per-run steps from the run sheet: estimated hours for the first run and once routine",
             ha="left", va="top", fontsize=10.5, fontweight="bold", color=INK)
    handles = [Patch(fc=PHASE[p], label=PHASE_NAME[p]) for p in "ABC"] + [
        Line2D([], [], color=INK2, lw=6, solid_capstyle="butt", label="range estimate"),
        Line2D([], [], marker="o", ls="none", color=INK2, markeredgecolor=SURFACE, markersize=7,
               label="single estimate")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.947), ncol=5, fontsize=8.4,
               labelcolor=INK2, handlelength=1.8, columnspacing=1.8)
    bbox = g.get_position()
    fig.text(0.012, bbox.y1 + 0.032, "(b) Provisional schedule to TMS 2027 (re-planned from the pilot's timing log)",
             ha="left", va="bottom", fontsize=10.5, fontweight="bold", color=INK)
    fig.text(0.012, 0.012, "All durations are estimates from the plan, not measurements; replace them with the "
                           "pilot's timing log (m2-run-timing-log.csv). Hours are per step; several B steps take "
                           "two people.", ha="left", va="bottom", fontsize=8.2, color=MUTED)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "m2-schedule.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def main():
    style()
    t = totals()
    for ph in "ABC":
        print(f"{ph}: first run {fmt_h(*t[ph]['first'])}, routine {fmt_h(*t[ph]['routine'])}")
    assert t["B"]["first"] == (3.75, 7.75) and t["B"]["routine"] == (3.5, 4.75)
    assert t["C"]["first"] == (18, 24) and t["C"]["routine"] == (12.5, 14.5)
    for p in (pilot_design(), schedule()):
        print("wrote", p.relative_to(HERE))


if __name__ == "__main__":
    main()
