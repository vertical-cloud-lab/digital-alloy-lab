#!/usr/bin/env python3
"""Figure: ORCHID v2026.10 coverage of the Al and Cu systems of interest, from al-cu-coverage.csv.
Left: accepted literature values by evidence class (stacked). Right: accepted experimental invariant reactions.
Usage: python -I orchid_data_coverage_figure.py --csv data/al-cu-coverage.csv --out figures/orchid-data-al-cu-coverage.png
"""
import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = [("lit_acc_experimental", "experimental", "#2a78d6"), ("lit_acc_model", "model (CALPHAD etc.)", "#eb6834"),
          ("lit_acc_dft", "DFT", "#1baf7a"), ("lit_acc_unspecified", "unspecified", "#a3a29c")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    c = pd.read_csv(a.csv)
    c["ylabel"] = c.label + c.group.map(lambda g: "" if g == "requested binary" else "  *")
    c = c.iloc[::-1].reset_index(drop=True)  # first system at the top
    n = len(c)
    plt.rcParams.update({"font.size": 8.5, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
                         "ytick.color": INK, "axes.edgecolor": GRID})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 0.24 * n + 1.9), sharey=True,
                                   gridspec_kw={"width_ratios": [2.2, 1], "wspace": 0.06}, facecolor=SURFACE)
    y = range(n)
    left = pd.Series(0.0, index=c.index)
    for col, name, color in SERIES:
        ax1.barh(y, c[col], left=left, height=0.62, color=color, label=name, edgecolor=SURFACE, linewidth=1.0)
        left += c[col]
    for i, tot in enumerate(c.lit_values_accepted):
        allv = c.lit_values_all[i]
        ax1.text(tot + 6, i, f"{tot} / {allv}", va="center", ha="left", fontsize=7.5, color=INK2)
    ax2.barh(y, c.inv_experimental_accepted, height=0.62, color="#2a78d6", edgecolor=SURFACE, linewidth=1.0)
    for i, v in enumerate(c.inv_experimental_accepted):
        ax2.text(v + 3, i, str(v), va="center", ha="left", fontsize=7.5, color=INK2)
    for ax in (ax1, ax2):
        ax.set_facecolor(SURFACE)
        ax.grid(axis="x", color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="y", length=0)
    ax1.set_yticks(list(y), c.ylabel)
    ax1.set_xlim(0, c.lit_values_accepted.max() * 1.18)
    ax2.set_xlim(0, max(c.inv_experimental_accepted.max(), 1) * 1.2)
    ax1.set_xlabel("accepted literature values (label: accepted / all)")
    ax2.set_xlabel("accepted experimental invariant reactions")
    ax1.legend(loc="lower right", frameon=False, fontsize=7.5, title="evidence class", title_fontsize=7.5)
    fig.suptitle("ORCHID data v2026.10: coverage of Al and Cu systems (literature_values.parquet)",
                 x=0.01, ha="left", fontsize=10, color=INK)
    fig.text(0.01, 0.005, "* subsystem binary, ternary or quaternary of Al–Si–Mg, Al–Mn–Cr–Zr or Cu–Al–Ni–Fe. "
             "Table view: data/al-cu-coverage.csv.", fontsize=7, color=INK2)
    fig.subplots_adjust(left=0.15, right=0.98, top=1 - 0.55 / (0.24 * n + 1.9), bottom=0.95 / (0.24 * n + 1.9))
    fig.savefig(a.out, dpi=130, facecolor=SURFACE)


if __name__ == "__main__":
    main()
