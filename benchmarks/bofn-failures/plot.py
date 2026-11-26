"""Figures for the failure benchmark (reads the same runs as analyze.py; writes figures/*.png).

    python plot.py

Colors follow the strategy's family, not its rank: no failure model (drop, abandon, partial) in
orange, imputation in aqua, a viability model (viab_x, viab_x_partial, viab_node) in blue, and the
no-failure reference in gray. Strategy names are always printed beside the marks, and every
number is also in tables.md. The three hues pass the colorblind checks of the dataviz validator
(worst pair deltaE 12.6 deutan, 28.1 normal vision).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import analyze as A

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
INK, INK2, GRID, AXIS = "#191919", "#666666", "#e7e7e7", "#c2c2c2"
BLUE, ORANGE, AQUA, GRAY, LIGHT = "#257de0", "#f47230", "#00b894", "#666666", "#c9c9c9"
FAMILY = {"nofail": GRAY, "drop": ORANGE, "abandon": ORANGE, "partial": ORANGE, "keep": ORANGE, "impute": AQUA, "impute_extreme": AQUA, "viab_x": BLUE, "viab_x_partial": BLUE,
          "viab_node": BLUE, "viab_node_ec": BLUE}
SHORT = {"nofail": "no failures (reference)", "drop": "drop: all FAILED (Ax 1.2.2–1.2.3)", "abandon": "abandon: all ABANDONED", "partial": "partial, pending (Ax ≥ 1.2.4)",
         "keep": "partial, nothing pending", "impute": "impute the worst value", "impute_extreme": "impute far below the worst", "viab_x": "viability on x (Ax 1.3)",
         "viab_x_partial": "viability on x + fit_abandoned",
         "viab_node": "node-level viability", "viab_node_ec": "node-level + failure-priced EI"}
CELLS = ["al-k1", "al-k0", "cu-toy-k1", "cu-phys-k1"]
FULL = ["al-k1-full", "cu-toy-k1-full"]

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 9, "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "axes.titlesize": 10,
    "axes.titlecolor": INK, "axes.titleweight": "bold", "axes.titlelocation": "left", "figure.dpi": 150, "savefig.dpi": 200,
    "savefig.bbox": "tight", "savefig.facecolor": "white", "legend.frameon": False, "legend.fontsize": 8.5, "text.parse_math": False,
})


def style(ax, xgrid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def mean_se(v):
    v = np.asarray(v, dtype=float)
    return v.mean(), (v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else 0.0)


def dot_panel(ax, cell, S, metric, xlabel, strategies):
    ys, missing = [], []
    for k, st in enumerate(strategies):
        y = len(strategies) - 1 - k
        if st not in S or not S[st]:
            missing.append(y)
            continue
        R = S[st]
        v = [metric(R[s], cell) for s in sorted(R)]
        m, se = mean_se(v)
        ax.plot([m - se, m + se], [y, y], color=FAMILY[st], lw=2, solid_capstyle="round", zorder=2)
        ax.scatter([m], [y], s=42, color=FAMILY[st], edgecolor="white", linewidth=1.6, zorder=3)
        ax.text(m + se, y, f"  {m:.0f}", color=INK2, fontsize=7.5, va="center", ha="left")
        ys.append(y)
    lo = ax.get_xlim()[0]
    for y in missing:
        ax.text(lo, y, "  not run in this cell", color=INK2, fontsize=7.5, va="center", ha="left", style="italic")
    ax.set_yticks(range(len(strategies)))
    ax.set_yticklabels([SHORT[s] for s in reversed(strategies)])
    ax.set_ylim(-0.7, len(strategies) - 0.3)
    ax.set_xlabel(xlabel)
    style(ax)


def fig_final(runs, scen="mixed", budget=100_000, name="final"):
    cells = [c for c in CELLS if c in runs and scen in runs[c]]
    fig, axes = plt.subplots(len(cells), 1, figsize=(6.4, 2.35 * len(cells)), sharex=False)
    axes = np.atleast_1d(axes)
    for ax, cell in zip(axes, cells):
        S = runs[cell][scen]
        n = min(len(S[s]) for s in A.ORDER if s in S and S[s])
        dot_panel(ax, cell, S, lambda r, c: A.pct(r, c, budget), "best alloy demonstrated, % of the true optimum (mean ± SE)", A.ORDER)
        ax.set_title(f"{A.CELL_NAME[cell]}: after ${budget // 1000}k ({n}+ seeds)")
    fig.tight_layout(h_pad=1.6)
    fig.savefig(FIG / f"bofn_failures_{name}.png")
    plt.close(fig)


def fig_failed_spend(runs, scen="mixed"):
    cells = [c for c in CELLS if c in runs and scen in runs[c]]
    strategies = [s for s in A.ORDER if s != "nofail"]
    fig, axes = plt.subplots(len(cells), 2, figsize=(9.6, 2.2 * len(cells)), sharey="row")
    axes = np.atleast_2d(axes)
    for row, cell in zip(axes, cells):
        S = runs[cell][scen]
        dot_panel(row[0], cell, S, lambda r, c: r["spent_on_failed_stages"] / 1000, "spend on failed stages, $k of $100k (mean ± SE)", strategies)
        dot_panel(row[1], cell, S, lambda r, c: r["input_failures"], "input-caused failures per campaign (mean ± SE)", strategies)
        row[0].set_title(A.CELL_NAME[cell])
    fig.tight_layout(h_pad=1.4, w_pad=1.2)
    fig.savefig(FIG / "bofn_failures_failed_spend.png")
    plt.close(fig)


def curve(R, cell, grid):
    out = []
    for s in sorted(R):
        out.append([A.pct(R[s], cell, b) for b in grid])
    out = np.array(out)
    return out.mean(0), out.std(0, ddof=1) / np.sqrt(len(out))


def fig_curves(runs, scen="mixed", highlight=("nofail", "drop", "impute", "viab_node")):
    cells = [c for c in CELLS if c in runs and scen in runs[c]]
    grid = np.arange(0, 100_001, 1000)
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 6.4))
    colors = {st: FAMILY[st] for st in highlight}  # one strategy per family, in the family's color
    for ax, cell in zip(axes.flat, cells):
        S = runs[cell][scen]
        for st in A.ORDER:
            if st in highlight or st not in S or not S[st]:
                continue
            m, _ = curve(S[st], cell, grid)
            ax.plot(grid / 1000, m, color=LIGHT, lw=1.2, zorder=1)
        for st in highlight:
            if st not in S or not S[st]:
                continue
            m, se = curve(S[st], cell, grid)
            ax.fill_between(grid / 1000, m - se, m + se, color=colors[st], alpha=0.10, lw=0, zorder=2)
            ax.plot(grid / 1000, m, color=colors[st], lw=2, zorder=3, label=SHORT[st])
        ax.set_title(A.CELL_NAME[cell])
        ax.set_xlabel("new spend, $k")
        ax.set_ylabel("best alloy demonstrated, % of optimum")
        ax.set_xlim(0, 100)
        style(ax)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
    h, l = axes.flat[0].get_legend_handles_labels()
    h.append(plt.Line2D([], [], color=LIGHT, lw=1.2))
    l.append("the other strategies (table and dot plot)")
    fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05))
    fig.tight_layout()
    fig.savefig(FIG / "bofn_failures_curves.png")
    plt.close(fig)


def fig_scenarios(runs, budget=100_000):
    """Mixed vs 30% mislabelled vs transient-only, per strategy, for the cells that have them."""
    cells = [c for c in CELLS if c in runs and ("mislabel" in runs[c] or "transient" in runs[c])]
    if not cells:
        return
    strategies = [s for s in A.ORDER if s != "nofail"]
    # scenarios in grays with distinct markers, so blue, orange and aqua keep meaning strategy families
    scen_style = [("mixed", "#191919", "o", "both kinds, labelled correctly"), ("mislabel", "#6e6e6e", "D", "both kinds, 30% of labels wrong"),
                  ("transient", "#a3a3a3", "s", "transient failures only"), ("edge", "#3d3d3d", "^", "failure boundary next to the optimum")]
    fig, axes = plt.subplots(len(cells), 1, figsize=(6.4, 2.6 * len(cells)))
    axes = np.atleast_1d(axes)
    for ax, cell in zip(axes, cells):
        for j, (scen, col, mk, lab) in enumerate(scen_style):
            S = runs[cell].get(scen)
            if not S:
                continue
            for k, st in enumerate(strategies):
                if st not in S or not S[st]:
                    continue
                v = [A.pct(S[st][s], cell, budget) for s in sorted(S[st])]
                m, se = mean_se(v)
                y = len(strategies) - 1 - k + (0.27 - 0.18 * j)
                ax.plot([m - se, m + se], [y, y], color=col, lw=1.6, solid_capstyle="round", zorder=2)
                ax.scatter([m], [y], s=30, marker=mk, color=col, edgecolor="white", linewidth=1.2, zorder=3, label=lab if k == 0 else None)
        ref = runs[cell]["mixed"].get("nofail")
        if ref:
            m, _ = mean_se([A.pct(ref[s], cell, budget) for s in sorted(ref)])
            ax.axvline(m, color=AXIS, lw=1, zorder=1)
            ax.text(m, len(strategies) - 0.35, " no failures", color=INK2, fontsize=7.5, va="bottom")
        ax.set_yticks(range(len(strategies)))
        ax.set_yticklabels([SHORT[s] for s in reversed(strategies)])
        ax.set_ylim(-0.7, len(strategies) - 0.1)
        ax.set_xlabel(f"best alloy demonstrated after ${budget // 1000}k, % of optimum (mean ± SE)")
        ax.set_title(A.CELL_NAME[cell])
        style(ax)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.05))
    fig.tight_layout(h_pad=1.6)
    fig.savefig(FIG / "bofn_failures_scenarios.png")
    plt.close(fig)


def fig_classifier():
    """AUC of the viability model against the number of labelled designs, over x and over the stage inputs."""
    import json

    path = HERE / "classifier_check.json"
    if not path.exists():
        return
    res = json.loads(path.read_text())
    names = {"al-k1": A.CELL_NAME["al-k1"], "al-k0": A.CELL_NAME["al-k0"], "cu-toy-k1": A.CELL_NAME["cu-toy-k1"], "cu-phys-k1": A.CELL_NAME["cu-phys-k1"]}
    fig, axes = plt.subplots(1, len(res), figsize=(2.6 * len(res), 2.9), sharey=True)
    for ax, c in zip(axes, res):
        ns = sorted({r["n"] for r in c["rows"]})
        for key, col, lab in (("node", BLUE, "over the stage's inputs (node level)"), ("x", ORANGE, "over the design x (Ax's AddExecutionViability)")):
            m, se = [], []
            for n in ns:
                v = np.array([r[f"auc_{key}"] for r in c["rows"] if r["n"] == n and not r.get("skipped")])
                m.append(v.mean())
                se.append(v.std(ddof=1) / np.sqrt(len(v)))
            m, se = np.array(m), np.array(se)
            ax.fill_between(ns, m - se, m + se, color=col, alpha=0.10, lw=0)
            ax.plot(ns, m, color=col, lw=2, marker="o", ms=5, mec="white", mew=1.2, label=lab)
        ax.set_xscale("log", base=2)
        ax.set_xticks(ns)
        ax.set_xticklabels([str(n) for n in ns])
        ax.set_title(names[c["cell"]], fontsize=9)
        ax.set_xlabel("labelled designs")
        style(ax)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
    axes[0].set_ylabel("held-out AUC of P(viable)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    fig.savefig(FIG / "bofn_failures_classifier.png")
    plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True)
    fig_classifier()
    runs = A.load()
    fig_final(runs)
    fig_final(runs, budget=50_000, name="final_50k")
    fig_failed_spend(runs)
    fig_curves(runs)
    fig_scenarios(runs)
    print("figures written to", FIG)


if __name__ == "__main__":
    main()
