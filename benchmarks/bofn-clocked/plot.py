"""Figures for the README (static PNGs; the tables in results/summary.md are the table view).

    python plot.py
"""
from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import analyze as A  # noqa: E402

HERE = A.HERE
TEXT, TEXT2, GRID = "#191919", "#666666", "#e3e3e3"
SLOTS = ["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17", "#6a4ce2", "#ec4647"]
CONFIGS = [("conv_lots", "conv"), ("conv_atomizer", "conv"), ("vertical", "tiered"), ("vertical", "gpbo"),
           ("vertical", "bofn"), ("vertical", "pkgfn"), ("vertical", "random")]
SHORT = {("conv_lots", "conv"): "Conventional, outside lots", ("conv_atomizer", "conv"): "Conventional, own atomizer",
         ("vertical", "tiered"): "Automated, tiered screening", ("vertical", "gpbo"): "Automated, GP-BO",
         ("vertical", "bofn"): "Automated, BOFN", ("vertical", "pkgfn"): "Automated, pKGFN",
         ("vertical", "random"): "Automated, random"}
STYLE = {("conv_lots", "conv"): dict(color="#8a8a8a", ls="-"), ("conv_atomizer", "conv"): dict(color="#8a8a8a", ls="--"),
         ("vertical", "tiered"): dict(color=SLOTS[0], ls="-"), ("vertical", "gpbo"): dict(color=SLOTS[1], ls="-"),
         ("vertical", "bofn"): dict(color=SLOTS[2], ls="-"), ("vertical", "pkgfn"): dict(color=SLOTS[3], ls="-"),
         ("vertical", "random"): dict(color=SLOTS[4], ls="-")}

plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "xtick.color": TEXT2,
                     "ytick.color": TEXT2, "axes.titlecolor": TEXT, "axes.titlesize": 10, "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})


def claim_curve(R, days):
    return np.array([[A.claim_at(r, d) for d in days] for r in R.values()])


def fig_claim(G):
    days = np.unique(np.concatenate([np.arange(0, 120, 0.5), np.arange(120, 1461, 2.0)]))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), sharey=True)
    for ax, kappa in zip(axes, (1.0, 0.0)):
        for key in CONFIGS:
            R = G.get((kappa, *key, None))
            if not R:
                continue
            C = 100 * claim_curve(R, days)
            st = STYLE[key]
            H = next(iter(R.values()))["horizon"]  # automated campaigns end at 1 year: don't draw past it
            keep = days <= H
            ax.plot(np.maximum(days[keep], 1), C.mean(0)[keep], lw=1.6, label=f"{SHORT[key]} (n={len(R)})", **st)
        for frac, name in ((60, "T1"), (80, "T2")):
            ax.axhline(frac, color=TEXT2, lw=0.8, ls=":", zorder=0)
            ax.text(1400, frac + 1.2, name, color=TEXT2, fontsize=8, ha="right")
        ax.axvline(31, color=TEXT2, lw=0.8, ls="--", zorder=0)
        ax.text(29, 92, "no claim before\nday 31 (30-day\nimmersion)", color=TEXT2, fontsize=7.5, ha="right", va="top")
        ax.set_xscale("log")
        ax.set_xlim(7, 1460)
        ax.set_xticks([7, 14, 30, 90, 365, 1460], ["7", "14", "30", "90", "365", "1460"])
        ax.set_ylim(0, 100)
        ax.grid(True, color=GRID, lw=0.6)
        ax.set_xlabel("days from the start of the campaign (log scale)")
        ax.set_title({1.0: "CALPHAD's crack screen misses the inoculant (kappa = 1)",
                      0.0: "CALPHAD's crack screen is right (kappa = 0)"}[kappa], loc="left")
    axes[0].set_ylabel("claimed alloy, true value as % of the optimum\n(mean over seeds; 0 before the first claim;\n"
                       "automated campaigns stop at T2 or after 1 year)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.02), labelcolor=TEXT)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(HERE / "clocked_claim_vs_days.png", dpi=150)
    plt.close(fig)


def fig_days_dollars(G):
    for kappa in (1.0, 0.0):
        keys = [k for k in CONFIGS if (kappa, *k, None) in G]
        if not keys:
            continue
        fig, axes = plt.subplots(2, 2, figsize=(10.5, 5.6), sharey=True)
        for i, T in enumerate(("T1", "T2")):
            for j, what in enumerate(("days", "dollars")):
                ax = axes[i, j]
                for y, key in enumerate(keys[::-1]):
                    R = G[(kappa, *key, None)]
                    vals = [A.t_hit(r, T)[j] for r in R.values()]
                    H = next(iter(R.values()))["horizon"] if j == 0 else next(iter(R.values()))["budget"]
                    fin = np.array([v for v in vals if np.isfinite(v)])
                    n_c = sum(1 for v in vals if not np.isfinite(v))
                    jit = (np.random.default_rng(y).random(len(fin)) - 0.5) * 0.35
                    scale = 1.0 if j == 0 else 1e-3
                    ax.scatter(fin * scale, y + jit, s=14, color=SLOTS[0], alpha=0.75, linewidths=0, zorder=3)
                    if len(fin) > len(vals) / 2:
                        ax.plot([np.median(vals) * scale] * 2, [y - 0.32, y + 0.32], color=TEXT, lw=1.6, zorder=4)
                    if n_c:
                        ax.text(1.0, y, f" {n_c} not reached", transform=ax.get_yaxis_transform(), color=TEXT2,
                                fontsize=7.5, va="center")
                ax.set_xscale("log")
                if j == 0:
                    ax.axvline(31, color=TEXT2, lw=0.8, ls="--", zorder=1)
                    ax.set_xlim(20, 1460)
                    ax.set_xticks([30, 60, 90, 180, 365, 730, 1460], ["30", "60", "90", "180", "365", "730", "1460"])
                    ax.set_xlabel(f"days to {T}")
                else:
                    ax.set_xlim(10, 260)
                    ax.set_xticks([10, 25, 50, 100, 250], ["10", "25", "50", "100", "250"])
                    ax.set_xlabel(f"money spent by {T}, $k")
                ax.set_yticks(range(len(keys)), [SHORT[k] for k in keys[::-1]])
                ax.grid(True, axis="x", color=GRID, lw=0.6)
                ax.tick_params(axis="y", length=0)
        fig.suptitle({1.0: "Days and dollars to T1 (60 %) and T2 (80 %), kappa = 1: dots are seeds, bars medians, dashed line the 30-day-immersion floor",
                      0.0: "Days and dollars to T1 (60 %) and T2 (80 %), kappa = 0: dots are seeds, bars medians, dashed line the 30-day-immersion floor"}[kappa],
                     x=0.01, ha="left", color=TEXT, fontsize=10)
        fig.tight_layout(rect=(0, 0, 0.93, 0.96))
        fig.savefig(HERE / f"clocked_days_dollars_k{kappa:g}.png", dpi=150)
        plt.close(fig)


def main():
    G = A.load("e1")
    if G:
        fig_claim(G)
        fig_days_dollars(G)


if __name__ == "__main__":
    main()
