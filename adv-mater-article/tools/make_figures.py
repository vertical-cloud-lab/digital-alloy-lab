#!/usr/bin/env python3
"""Draft figures for the Advanced Materials article that can already be drawn from existing data.

    python tools/make_figures.py                      # draw from data/*.csv
    python tools/make_figures.py --bofn-dir <path>    # first re-summarize the synthetic benchmark

Outputs (figures/):
  figS-atomizer-runs.{pdf,png}     every atomizer run Oct 2 - Nov 13, 2026, and how it ended
                                   (draft for SI S1/S3), from data/atomizer-runs-2026-11-13.csv
                                   (PR #286, atomizer-runs/runs.csv @ 8320f13)
  fig6-draft-synthetic.{pdf,png}   best alloy demonstrated vs spend, screen wrong (kappa = 1) and
                                   screen right (kappa = 0), from data/bofn-prelim-summary.csv
                                   (benchmarks/bofn-prelim @ 3e2e167 on PR 90's branch, read only).
                                   Layout draft for Fig. 6b; the article's panel will come from
                                   the twin once it is calibrated on lab records.

--bofn-dir needs torch and botorch, because bofn-prelim's analyze.py computes the
true optimum used to normalize scores.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIGS = ROOT / "figures"

# Reference palette (dataviz skill, light mode): categorical slots in fixed order,
# text inks, recessive grid. Baselines that are context, not the comparison, are gray.
BLUE, ORANGE, AQUA = "#257de0", "#f47230", "#00b894"
INK, INK2, GRID_C, GRAY = "#191919", "#666666", "#e6e6e6", "#9c9c9c"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "legend.frameon": False,
    "pdf.fonttype": 42, "savefig.dpi": 300,
})


def save(fig, name: str) -> None:
    FIGS.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGS / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print("wrote", FIGS / f"{name}.pdf")


# --------------------------------------------------------------------------- atomizer runs
# How each run ended. "usable" = made a usable powder lot; "some" = better, but not weighed
# and plate still mispositioned; "little" = little or no powder. From the run table's
# powder_result and outcome columns and the threads cited there (#159, #219).
OUTCOME = {
    "2026-10-02": ("little", "melt overshot the plate"),
    "2026-10-06": ("little", "stream hit the upper sonotrode; vibration late"),
    "2026-10-08": ("little", "drips froze on the plate tip (CF plate, 1.5:1 booster)"),
    "2026-10-21": ("little", "plate in the wrong place until mid-pour"),
    "2026-10-22": ("some", "better; plate still low; not weighed"),
    "2026-10-27": ("usable", "91% of charge < 250 µm (sieved)"),
    "2026-10-28": ("little", "plate never started (~3% usable)"),
    "2026-11-05": ("little", "generator tripped; melt froze in nozzle"),
    "2026-11-10": ("usable", "~75% atomized (estimate)"),
    "2026-11-13": ("little", "no powder; hot shot burned the collection cup (#269)"),
}


def fig_atomizer_runs() -> None:
    rows = list(csv.DictReader(open(DATA / "atomizer-runs-2026-11-13.csv")))
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    n = len(rows)
    for i, r in enumerate(rows):
        y = n - 1 - i
        d = date.fromisoformat(r["date"])
        is_al = r["alloy"].lower().startswith("al")
        color = BLUE if is_al else ORANGE
        kind, why = OUTCOME[r["date"]]
        face = {"usable": color, "some": "white", "little": "white"}[kind]
        hatch = "//////" if kind == "some" else None
        ax.scatter([mdates.date2num(d)], [y], s=70, marker="o" if is_al else "s", facecolor=face,
                   edgecolor=color, linewidth=1.6, hatch=hatch, zorder=3)
        lot = r["lot_or_sample_code"].split(" ")[0] or "—"
        charge = f"{float(r['charge_g']):.0f} g" if r["charge_g"] else "not weighed"
        ax.text(mdates.date2num(date(2026, 11, 16)), y, f"{d:%b %d}  {lot:<7} {charge:>11}   {why}",
                va="center", ha="left", fontsize=7.2, color=INK, family="DejaVu Sans Mono")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(mdates.date2num(date(2026, 9, 30)), mdates.date2num(date(2026, 11, 15)))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.grid(axis="x", color=GRID_C, linewidth=0.6, zorder=0)
    ax.set_ylim(-0.7, n - 0.3)
    handles = [
        plt.Line2D([], [], marker="o", ls="", mfc=BLUE, mec=BLUE, ms=7, label="Al alloy, usable powder"),
        plt.Line2D([], [], marker="o", ls="", mfc="white", mec=BLUE, ms=7, mew=1.6, label="Al alloy, little or none"),
        plt.Line2D([], [], marker="s", ls="", mfc=ORANGE, mec=ORANGE, ms=7, label="C63000 bronze, usable powder"),
        plt.Line2D([], [], marker="s", ls="", mfc="white", mec=ORANGE, ms=7, mew=1.6, label="C63000 bronze, little or none"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=7.5)
    ax.set_title("Every atomizer run so far: 2 of 10 made a usable lot, and no Al powder has been weighed",
                 loc="left", color=INK)
    fig.text(0.01, -0.13, "Hatched: better run, not weighed. Source: PR #286 run table (atomizer-runs/runs.csv @ 8320f13).",
             fontsize=6.8, color=INK2)
    save(fig, "figS-atomizer-runs")


# --------------------------------------------------------------------------- synthetic benchmark
POLICIES = [  # (key, label, color, emphasis)
    ("pkgfn", "Cost-aware network (pKGFN)", BLUE, True),
    ("eifn", "Network BO, full chain", ORANGE, False),
    ("tiered", "Screen, then test", AQUA, True),
    ("ei", "Standard BO", GRAY, False),
    ("random", "Random", "#c4c4c4", False),
]


def summarize_bofn(bofn_dir: Path) -> None:
    sys.path.insert(0, str(bofn_dir))
    import analyze as a  # bofn-prelim's own loader and normalization

    out = DATA / "bofn-prelim-summary.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kappa", "policy", "spent_usd", "mean_pct", "se_pct", "n_seeds"])
        for kap in (0.0, 1.0):
            data = a.load(kap)
            ys = a.optimum(kap)
            for key, *_ in POLICIES:
                if key not in data:
                    continue
                c = a.curves(data[key], "best_validated", ys) * 100
                for j in range(0, len(a.GRID), 4):  # every $1,000
                    col = c[:, j]
                    w.writerow([kap, key, int(a.GRID[j]), f"{col.mean():.3f}",
                                f"{col.std(ddof=1) / np.sqrt(len(col)):.3f}", len(col)])
    print("wrote", out)


def fig6_synthetic() -> None:
    rows = list(csv.DictReader(open(DATA / "bofn-prelim-summary.csv")))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    titles = {1.0: "Screen wrong (κ = 1):\nCALPHAD misses Zr/Sc grain refinement",
              0.0: "Screen right (κ = 0):\nCALPHAD sees what printing sees"}
    for ax, kap in zip(axes, (1.0, 0.0)):
        for key, label, color, emph in POLICIES:
            sel = [r for r in rows if float(r["kappa"]) == kap and r["policy"] == key]
            if not sel:
                continue
            x = np.array([int(r["spent_usd"]) for r in sel]) / 1000
            m = np.array([float(r["mean_pct"]) for r in sel])
            se = np.array([float(r["se_pct"]) for r in sel])
            ax.fill_between(x, m - se, m + se, color=color, alpha=0.15, linewidth=0)
            ax.plot(x, m, color=color, lw=2.0 if emph else 1.4, label=label, zorder=3 if emph else 2)
            if emph:
                short = "Cost-aware" if key == "pkgfn" else "Screen, test"
                ax.text(x[-1] + 2, m[-1], short, color=INK, fontsize=7.0, va="center", clip_on=False)
        ax.set_title(titles[kap], loc="left", color=INK, fontsize=8.3)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Cumulative spend ($k)")
        ax.grid(axis="y", color=GRID_C, linewidth=0.6)
        ax.set_ylim(0, 100)
    axes[0].set_ylabel("Best alloy printed and tested\n(% of true optimum)")
    n1 = {r["policy"]: r["n_seeds"] for r in rows if float(r["kappa"]) == 1.0}
    n0 = {r["policy"]: r["n_seeds"] for r in rows if float(r["kappa"]) == 0.0}
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, fontsize=7.2)
    fig.text(0.01, -0.2,
             f"DRAFT LAYOUT for Fig. 6b. Synthetic, noise-free benchmark (bofn-prelim @ 3e2e167): mean ± 1 s.e. over "
             f"{n1.get('pkgfn')} seeds (κ = 1) and {n0.get('pkgfn')} seeds (κ = 0). Not a result of this article; "
             "the final panel comes from the twin calibrated on lab records.",
             fontsize=6.6, color=INK2, wrap=True)
    fig.subplots_adjust(right=0.88, wspace=0.38)
    save(fig, "fig6-draft-synthetic")


# --------------------------------------------------------------------------- baselines vs burden
def fig5c_benchmarks() -> None:
    """Yield strength against mineral burden: the frame Fig. 5c will fill.

    The comparison campaign 2 is judged on is the front of the industry Sc-free baselines (EOS Al5X1,
    Hoganas Al-HS1) printed and tested in this lab with the candidates. None has been printed here yet, so
    this draft places them at their data-sheet values (data/scfree-baselines-datasheets.csv, checked
    against the vendors' documents 2026-11-27). AlSi10Mg and Scalmalloy rows: data/benchmark-property-
    window.csv (PR #285 @ a25d763). Lab row: Utah Aconity MIDI AlSi10Mg, as built, horizontal, n = 4
    (PR #288). Burden: B = sum w_i NIR_i/100 with the campaign paper's MCS 2026 inputs. Points sit at the
    middle of each alloy's B range; the ranges are drawn in the lower panel. Colour follows the role, not
    the alloy (three categorical slots, scatter): blue = the Sc-free baselines, orange = AlSi10Mg,
    aqua = this lab's measurement, gray = context."""
    sys.path.insert(0, str(ROOT / "tools"))
    from mineral_burden_check import ALLOYS, burden

    bench = list(csv.DictReader(open(DATA / "benchmark-property-window.csv")))
    base = [r for r in csv.DictReader(open(DATA / "scfree-baselines-datasheets.csv")) if r["plotted"] == "yes"]
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 6.0), sharex=True,
                                   gridspec_kw={"height_ratios": [4, 2.1], "hspace": 0.12})

    def heat_treated(cond: str) -> bool:
        return not cond.startswith(("as built", "as printed", "as-built"))

    def mid(key: str) -> float:
        lo, hi = burden(ALLOYS[key])
        return (lo + hi) / 2

    def series(rows, key, color, label, label_xy, ha="left"):
        m = mid(key)
        for i, r in enumerate(rows):
            x = m + (i - (len(rows) - 1) / 2) * 0.06
            ht = heat_treated(r["condition"])
            ax.scatter([x], [float(r["yield_MPa"])], marker="s" if ht else "o", s=34,
                       facecolor="white" if ht else color, edgecolor=color, linewidth=1.4, zorder=3)
        ax.text(*label_xy, label, color=INK, fontsize=7.2, va="center", ha=ha)

    a5 = [r for r in base if r["alloy"] == "Al5X1"]
    hs = [r for r in base if r["alloy"] == "Al-HS1"]
    cp = [r for r in base if r["alloy"] == "Aheadd CP1"]
    si = [r for r in bench if r["alloy"] == "AlSi10Mg"]
    sc = [r for r in bench if r["alloy"].startswith("Scalmalloy")]

    # Draft front: Al5X1 and Al-HS1 at their best aged data-sheet values, this lab's AlSi10Mg (as built)
    # as the floor, stepped at the middle of Al5X1's B range. The pre-registration's test is per baseline
    # (stronger, or lower B by the interval rule); this line is only its picture.
    floor = 228.0
    a5_mid = mid("Al5X1 (EOS, nominal)")
    a5_best = max(float(r["yield_MPa"]) for r in a5)
    x_max = 10.8
    xs, ys = [0, a5_mid, a5_mid, x_max], [floor, floor, a5_best, a5_best]
    ax.fill_between(xs, ys, [560] * 4, color=BLUE, alpha=0.06, linewidth=0, zorder=0)
    ax.plot(xs, ys, color=BLUE, lw=1.6, ls=(0, (5, 2)), zorder=2)
    ax.text(0.15, 522, "Campaign 2 has to land in the shaded region:\nbeyond the front of the Sc-free baselines\n"
            "printed and tested in this lab", fontsize=7, color=INK, va="top")

    series(a5, "Al5X1 (EOS, nominal)", BLUE, "EOS Al5X1 (Al-Mg-Zr-Mn)", (a5_mid, 412), ha="center")
    series(hs, "Al-HS1 (Hoganas, typical)", BLUE, "Höganäs Al-HS1\n(Al-Mn-Cr-Zr)", (mid("Al-HS1 (Hoganas, typical)") + 0.25, 318))
    series(cp, "Aheadd CP1 (nominal)", GRAY, "Aheadd CP1\n(context)", (0.45, 300))
    series(si, "AlSi10Mg (nominal)", ORANGE, "AlSi10Mg\n(data sheets)", (8.25, 300))
    series(sc, "Scalmalloy (nominal)", GRAY, "Scalmalloy\n(contains Sc;\ncontext)", (5.85, 470))

    xm = mid("AlSi10Mg (nominal)")
    ax.errorbar([xm], [floor], yerr=[13], fmt="D", color=INK2, ms=6.5, mfc=AQUA, mec=INK, mew=0.8,
                capsize=2, zorder=4)
    ax.annotate("this lab: AlSi10Mg,\nAconity MIDI, as built,\nn = 4 (the floor)", (xm, floor), (8.3, 196),
                fontsize=7, color=INK, va="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))
    ax.set_ylabel("Yield strength (MPa)")
    ax.set_ylim(120, 540)
    ax.grid(axis="y", color=GRID_C, lw=0.6, zorder=0)
    handles = [
        plt.Line2D([], [], marker="s", ls="", mfc=BLUE, mec=BLUE, ms=6, label="Sc-free baselines (data sheets)"),
        plt.Line2D([], [], marker="s", ls="", mfc=ORANGE, mec=ORANGE, ms=6, label="AlSi10Mg (data sheets)"),
        plt.Line2D([], [], marker="D", ls="", mfc=AQUA, mec=INK, mew=0.8, ms=6, label="this lab's measurement"),
        plt.Line2D([], [], marker="s", ls="", mfc=GRAY, mec=GRAY, ms=6, label="context (data sheets)"),
        plt.Line2D([], [], marker="o", ls="", mfc=INK2, mec=INK2, ms=6, label="as built"),
        plt.Line2D([], [], marker="s", ls="", mfc="white", mec=INK2, mew=1.4, ms=6, label="aged or heat-treated"),
        plt.Line2D([], [], color=BLUE, lw=1.6, ls=(0, (5, 2)), label="draft in-house front"),
    ]
    fig.legend(handles=handles, fontsize=6.8, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.905))

    rows = [("Aheadd CP1 (nominal)", GRAY, "CP1"), ("Al5X1 (EOS, nominal)", BLUE, "Al5X1"),
            ("Al-HS1 (Hoganas, typical)", BLUE, "Al-HS1"), ("Scalmalloy (nominal)", GRAY, "Scalmalloy"),
            ("AlSi10Mg (nominal)", ORANGE, "AlSi10Mg"),
            ("S2 Al-1.9Fe-1.0Mg-1.0Zr", INK2, "seed S2 Al-1.9Fe-1.0Mg-1.0Zr"),
            ("O1 Al-3.6Mg-1.2Zr", INK2, "seed O1 Al-3.6Mg-1.2Zr"),
            ("S3 Al-3.5Si-2.5Mg", INK2, "seed S3 Al-3.5Si-2.5Mg"),
            ("O3 Al-4.8Mn-0.8Cr", INK2, "seed O3 Al-4.8Mn-0.8Cr"),
            ("S1 Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg", INK2, "seed S1 Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg")]
    n = len(rows)
    for j, (key, color, lab) in enumerate(rows):
        lo, hi = burden(ALLOYS[key])
        y = n - 1 - j
        ax2.plot([lo, max(hi, lo + 0.06)], [y, y], color=color, lw=4, solid_capstyle="butt")
        right = max(hi, lo + 0.06) + 0.12
        if right > 8.6:
            ax2.text(lo - 0.12, y, lab, fontsize=6.4, color=INK, va="center", ha="right")
        else:
            ax2.text(right, y, lab, fontsize=6.4, color=INK, va="center")
    ax2.set_yticks([]); ax2.spines["left"].set_visible(False)
    ax2.set_ylim(-0.7, n - 0.3)
    ax2.set_xlim(0, x_max)
    ax2.set_xlabel("Mineral burden B_NIR (wt % of the alloy imported, net; USGS MCS 2026)")
    ax2.text(0.0, 1.0, "B ranges (USGS gives Mg, Si and Zr import reliance as bounds); seeds (#275) have no "
             "strength yet", transform=ax2.transAxes, fontsize=6.8, color=INK2, va="bottom")
    fig.text(0.0, 0.035, "DRAFT for Fig. 5c. Campaign 2 replaces the data-sheet baselines with Al5X1 and Al-HS1 "
             "printed and tested here, beside AlSi10Mg; data sheets stay\nas context. Points sit at the middle of "
             "each alloy's B range. CP1 already lies in the region, so a candidate also has to clear published "
             "alloys to count as new.\nBurden metric not yet frozen (D9).", fontsize=6.2, color=INK2, va="top")
    save(fig, "fig5c-draft-benchmarks")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bofn-dir", type=Path, help="path to benchmarks/bofn-prelim to re-summarize")
    args = ap.parse_args()
    if args.bofn_dir:
        summarize_bofn(args.bofn_dir.resolve())
    fig_atomizer_runs()
    fig6_synthetic()
    fig5c_benchmarks()


if __name__ == "__main__":
    main()
