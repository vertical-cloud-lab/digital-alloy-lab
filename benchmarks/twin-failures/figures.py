"""Figures for the failed-vs-abandoned benchmark in the twin (called by ``analyze.py --figs``).

Colours: the dataviz skill's validated categorical slots in a fixed order per strategy (checked with its
``validate_palette.js``: all checks pass in light mode; four slots are under 3:1 against white, so every figure is
direct-labelled and the README carries the tables). Round 3's own rule, ``bad_value``, is the neutral grey.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
TEXT, TEXT2, GRID = "#191919", "#666666", "#e4e4e4"
COL = {"bad_value": "#666666", "drop": "#257de0", "abandon": "#f47230", "retry": "#00b894",
       "viability_x": "#f2a600", "viability_node": "#ee7fac", "viability_node_nodiag": "#008a17",
       "oracle": "#6a4ce2"}
LABEL = {"bad_value": "bad value (round 3)", "drop": "drop (FAILED)", "abandon": "abandon (ABANDONED)",
         "retry": "retry once, then abandon", "viability_x": "viability on x (Ax 1.3)",
         "viability_node": "viability node, lab's diagnosis", "viability_node_nodiag": "viability node, no diagnosis",
         "oracle": "viability node, true cause"}
CAMPS = ("flaime_al", "onr_cu")
CNAME = {"flaime_al": "Aluminium (FLAIME)", "onr_cu": "Copper (ONR)"}


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TEXT2)
    ax.tick_params(colors=TEXT2, labelsize=8)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def _median_curve(curves, days):
    """Best-so-far utility at each day, median and quartiles over seeds (0 before the first new alloy)."""
    M = np.zeros((len(curves), len(days)))
    for i, c in enumerate(curves):
        best, j = 0.0, 0
        pts = sorted(c)
        for k, d in enumerate(days):
            while j < len(pts) and pts[j][0] <= d:
                best = max(best, pts[j][2])
                j += 1
            M[i, k] = best
    return np.median(M, axis=0), np.quantile(M, 0.25, axis=0), np.quantile(M, 0.75, axis=0)


def best_vs_days(raw, regime, strategies, targets, fname, title):
    days = np.arange(0, 366, 1.0)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True)
    for ax, camp in zip(axes, CAMPS):
        ends = []
        for p in strategies:
            rows = raw.get(regime, {}).get(p)
            if not rows:
                continue
            med, lo, hi = _median_curve([r["curve"][camp] for r in rows], days)
            ax.step(days, med, where="post", color=COL[p], lw=2, label=f"{LABEL[p]} (n={len(rows)})")
            ends.append((med[-1], p))
        for t, ls in (("T1", (0, (4, 3))), ("T2", (0, (1, 2)))):
            y = targets[t][camp]
            ax.axhline(y, color=TEXT2, lw=1, ls=ls)
            ax.text(2, y + 0.008, {"T1": "T1: state of the art", "T2": "T2: halfway to the oracle's best"}[t],
                    color=TEXT2, fontsize=7.5, va="bottom")
        # direct labels at the line ends, nudged apart
        ends.sort()
        last = -1.0
        for y, p in ends:
            yy = max(y, last + 0.035)
            ax.text(368, yy, LABEL[p].split(" (")[0].split(",")[0], color=TEXT, fontsize=7, va="center")
            last = yy
        ax.set_xlim(0, 365)
        ax.set_ylim(0, max(0.95, max([e[0] for e in ends] + [0]) + 0.1))
        ax.set_title(CNAME[camp], fontsize=10, color=TEXT, loc="left")
        ax.set_xlabel("simulated day", fontsize=9, color=TEXT2)
        _style(ax)
    axes[0].set_ylabel("best new alloy so far (true utility), median of seeds", fontsize=9, color=TEXT2)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(title, fontsize=11, color=TEXT, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.1, 0.97, 0.95))
    fig.savefig(FIG / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)


def paired_forest(out, regime, strategies, fname, title):
    E = out["regimes"].get(regime, {}).get("paired", {})
    panels = [("flaime_al", "best", "Aluminium: best new alloy\n(difference in utility)"),
              ("flaime_al", "T1_rmst", "Aluminium: days to T1\n(restricted mean; negative is sooner)"),
              ("onr_cu", "best", "Copper: best new alloy"),
              ("onr_cu", "T1_rmst", "Copper: days to T1")]
    rows = [p for p in strategies if p in E]
    if not rows:
        return
    fig, axes = plt.subplots(1, 4, figsize=(12, 0.55 * len(rows) + 1.6), sharey=True)
    for ax, (camp, metric, lab) in zip(axes, panels):
        for i, p in enumerate(rows):
            x = E[p].get(camp, {}).get(metric)
            if not x:
                continue
            y = len(rows) - 1 - i
            ax.plot([x["lo"], x["hi"]], [y, y], color=COL[p], lw=2, solid_capstyle="round")
            sig = x.get("p_holm", 1.0) < 0.05
            ax.plot([x["mean"]], [y], "o", ms=8, mfc=COL[p] if sig else "white", mec=COL[p], mew=2)
        ax.axvline(0, color=TEXT2, lw=1)
        ax.set_title(lab, fontsize=8.5, color=TEXT, loc="left")
        _style(ax)
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(range(len(rows)))
    axes[0].set_yticklabels([LABEL[p] for p in reversed(rows)], fontsize=8, color=TEXT)
    fig.suptitle(title + "\nmean paired difference from bad value (round 3), 95 % bootstrap interval; filled: Holm-"
                 "corrected p < 0.05", fontsize=9.5, color=TEXT, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(FIG / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)


def atomizer_runs(out, regime, strategies, fname, title):
    S = out["regimes"].get(regime, {}).get("strategies", {})
    rows = [p for p in strategies if p in S]
    if not rows:
        return
    cats = [("made powder", "#257de0"), ("failed: transient", "#f47230"), ("failed: the inputs", "#00b894")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 0.5 * len(rows) + 1.8), sharey=True)
    for ax, camp in zip(axes, CAMPS):
        for i, p in enumerate(rows):
            L = S[p][camp]["ledger"]
            vals = [L["runs"] - L["failed"], L["failed_transient"], L["failed_intrinsic"]]
            y, left = len(rows) - 1 - i, 0.0
            for (name, c), v in zip(cats, vals):
                ax.barh(y, v, left=left, color=c, edgecolor="white", linewidth=2, height=0.62,
                        label=name if i == 0 else None)
                left += v
            ax.text(left + 2, y, f"{L['failed']:.0f} of {L['runs']:.0f} failed", fontsize=7.5, color=TEXT,
                    va="center")
        ax.set_title(CNAME[camp] + ": atomizer runs a year (mean of seeds)", fontsize=9.5, color=TEXT, loc="left")
        _style(ax)
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(range(len(rows)))
    axes[0].set_yticklabels([LABEL[p] for p in reversed(rows)], fontsize=8, color=TEXT)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.03))
    fig.suptitle(title, fontsize=10.5, color=TEXT, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.93))
    fig.savefig(FIG / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main(out, data):
    import bench
    FIG.mkdir(exist_ok=True)
    # the raw curves per regime and strategy
    raw = {}
    for name in bench.EXPERIMENTS:
        for r in bench.load(name):
            c = r["cfg"]
            if c["days"] < 365:
                continue
            raw.setdefault(c["regime"], {}).setdefault(c["policy"], {})[c["seed"]] = dict(
                curve={k: r["campaigns"][k]["curve_new"] for k in CAMPS})
    raw = {g: {p: list(s.values()) for p, s in P.items()} for g, P in raw.items()}
    T = out["targets"]
    main_s = ("bad_value", "drop", "abandon", "retry", "viability_x", "viability_node")
    for reg, ttl in (("lab", "The lab's failure record (learning curve, damage): best new alloy against days"),
                     ("lab_region", "With a hidden region that won't atomize"),
                     ("twin", "Round 3's own failure law")):
        if reg in raw:
            strat = [p for p in main_s + ("viability_node_nodiag", "oracle") if p in raw[reg]]
            best_vs_days(raw, reg, strat, T, f"twinfail_{reg}_best_vs_days.png", ttl)
            paired_forest(out, reg, strat, f"twinfail_{reg}_paired.png", ttl)
            atomizer_runs(out, reg, strat, f"twinfail_{reg}_atomizer.png", ttl + ": where the atomizer's runs went")
