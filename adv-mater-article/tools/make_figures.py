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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bofn-dir", type=Path, help="path to benchmarks/bofn-prelim to re-summarize")
    args = ap.parse_args()
    if args.bofn_dir:
        summarize_bofn(args.bofn_dir.resolve())
    fig_atomizer_runs()
    fig6_synthetic()


if __name__ == "__main__":
    main()
