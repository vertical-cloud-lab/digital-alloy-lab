"""How each policy behaves across seeds: what it buys and when, and where it makes alloys.

    python behaviour.py            # bofn_behaviour_{purchases,composition,builds}_k1.png

Static companions to ../dag/timelapse.py, which plays back a single seed:

- purchases: every run is a tape of its purchases against spend, one row per
  seed, with one block per purchase, as wide as its cost and coloured by stage.
  Tensile tests that beat the best alloy so far are tall red ticks. Uses all 20
  stored seeds. The stored runs record each decision's action and the spend
  after it, not the stages one by one, but those follow from the action and the
  spend step: a "full" chain is atomize, print and test, plus a $10 CALPHAD
  call when the alloy is new; "reuse" is print and test; the screen is $10
  calls. `purchases()` rebuilds them this way and checks the result against
  the purchase log wherever a run has one (all 37 such runs match).
- composition: every alloy a policy made into powder or printed, placed by two
  CALPHAD outputs: the freezing-range index f, which is all the tiered screen
  reads, against the nucleant fraction g, which suppresses hot cracking in the
  print and which the screen cannot see. Size is the number of prints on the
  alloy and colour is when it was first made. This needs the inputs of every
  purchase, so it uses only the runs that log them: ../results-rerun (seeds
  0-4, identical to the stored runs action for action) and
  ../quality/kgfn-smoke (KGFN, seeds 0-1).
- builds: every build a policy printed, scored by the true objective of its
  alloy and settings (% of the optimum) against the spend when it was printed,
  filled if it was tensile-tested, with the mean over each $10k of spend. Same
  runs as the composition figure.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import matplotlib.pyplot as plt  # noqa: E402
import torch  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.patheffects import withStroke  # noqa: E402

from analyze import optimum  # noqa: E402
from bofn_alloy import COMP, D, DEFAULT_COSTS, AlloyTruth  # noqa: E402
from plot import INK, MUTED, RED, SHORT  # noqa: E402  (also sets Aptos and the slide rcParams)
from policies import F_SAFE  # noqa: E402

TAPES = [HERE.parent / "results", HERE.parent / "quality" / "kgfn-smoke"]  # first folder with runs of a policy wins
LOGGED = [HERE.parent / "results-rerun", HERE.parent / "quality" / "kgfn-smoke"]
# columns pair each full-pipeline policy with its counterpart that screens, reuses powder or picks the stage;
# the bottom two rows are the paper's 2 x 2, {EI, KG} x {full, partial}
GRID = [("random", "tiered_naive"), ("ei", "tiered"), ("eifn", "eifn_reuse"), ("kgfn", "pkgfn")]
COLUMNS = ("Full pipeline for every alloy", "Screens with CALPHAD, reuses powder, or picks the stage")
STAGES = {  # name, colour (the first three categorical slots plus ink: CVD-safe in every pair)
    "C": ("CALPHAD call", "#1baf7a"),
    "A": ("Atomize a powder", "#eb6834"),
    "L": ("Print a build", "#2a78d6"),
    "T": ("Tensile test", "#262626"),
}
COSTS = DEFAULT_COSTS  # every stored and re-run cell used the abstract's costs
ACTION = {"full": "ALT", "reuse": "LT", "C-screen": "", "C": "C", "A": "A", "L": "L", "T": "T"}
WHEN = LinearSegmentedColormap.from_list("when", ["#86b6ef", "#2a78d6", "#184f95", "#0d366b"])  # sequential blue, 250 -> 700
GRAY, LIGHT, FAINT = "#595959", "#BFBFBF", "#F0F0F0"


def load(kind, kappa, roots):
    for root in roots:
        ps = sorted((root / f"k{kappa:g}").glob(f"{kind}_s*.json"), key=lambda p: int(p.stem.rsplit("_s", 1)[1]))
        if ps:
            return [json.loads(p.read_text()) for p in ps], root
    return [], None


def purchases(run):
    """(stage, spend before, spend after, beat the best) for every purchase after the seed data.

    Rebuilt from the rows (action and spend after each decision); runs that log their
    purchases are checked against the log."""
    out, prev, best = [], 0.0, run["rows"][0]["best_validated"]
    for row in run["rows"][1:]:
        base = ACTION[row["action"]]
        extra = row["spent"] - prev - sum(COSTS[g] for g in base)
        n = round(extra / COSTS["C"])
        if n < 0 or abs(extra - n * COSTS["C"]) > 1e-6:
            raise ValueError(f"{run['kind']} seed {run['seed']}: cannot split ${row['spent'] - prev:,.0f} of {row['action']!r}")
        s, better = prev, row["best_validated"] > best
        seq = "C" * n + base
        for i, g in enumerate(seq):
            out.append((g, s, s + COSTS[g], better and i == len(seq) - 1))
            s += COSTS[g]
        prev, best = row["spent"], max(best, row["best_validated"])
    if run.get("purchases"):
        logged = [(g, round(e, 6)) for g, e, _ in run["purchases"]]
        if logged != [(g, round(e, 6)) for g, _, e, _ in out]:
            raise ValueError(f"{run['kind']} seed {run['seed']}: rebuilt purchases differ from the logged ones")
    return out


def optimum_design(kappa):
    """The argmax behind analyze.optimum (same search, same random numbers)."""
    t = AlloyTruth(kappa)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400_000, D, generator=g)
    y = t.objective(X)
    xbest, best = X[y.argmax()], float(y.max())
    for x0 in X[y.topk(20).indices]:
        xb, yb = x0, float(t.objective(x0))
        for scale in (0.03, 0.01, 0.003):
            P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
            yp = t.objective(P)
            if float(yp.max()) > yb:
                xb, yb = P[yp.argmax()], float(yp.max())
        if yb > best:
            xbest, best = xb, yb
    assert abs(best - optimum(kappa)) < 1e-12
    return xbest


def calphad(comps):
    """CALPHAD's freezing-range index f and nucleant fraction g for compositions [n, 4] (no kappa in either)."""
    c = torch.tensor(np.asarray(comps, dtype=float).reshape(-1, len(COMP)))
    t = AlloyTruth(0.0)
    return t.node("f", c).numpy(), t.node("g", c).numpy()


def crack_line(kappa, g):
    """f at which the print is 50% cracked for nucleant fraction g: the crack term of AlloyTruth.node('rho'),
    f_eff = f (1 - kappa 0.85 g / (g + 0.12)) = 0.38."""
    return 0.38 / (1 - kappa * 0.85 * g / (g + 0.12))


def stats(runs, ystar):
    n = Counter()
    for r in runs:
        n.update(g for g, *_ in purchases(r))
    k = len(runs)
    best = np.mean([max(row["best_validated"] for row in r["rows"]) for r in runs]) / ystar * 100
    parts = [f"{n['A'] / k:.0f} powders", f"{n['L'] / k:.0f} prints", f"{n['T'] / k:.0f} tests"]
    if n["C"]:
        parts.append(f"{n['C'] / k:.0f} CALPHAD calls")
    return "Per run, on average: " + ", ".join(parts), f"best alloy at $100k: {best:.0f}% of the optimum"


# --------------------------------------------------------------------------- purchases
def figure_purchases(kappa, out):
    ystar = optimum(kappa)
    budget = 100_000
    n_rows = 20
    W, PW, L, R = 15.5, 6.75, 0.5, 0.25
    row_h, head_h, gap_h, top_h, bot_h = 0.095, 0.56, 0.34, 1.55, 0.62
    panel_h = n_rows * row_h
    H = top_h + 4 * (head_h + panel_h) + 3 * gap_h + bot_h
    fig = plt.figure(figsize=(W, H))
    fig.text(L / W, 1 - 0.32 / H, "What each policy buys, run by run", fontsize=22, fontweight="bold", color=INK, va="center")
    fig.text(L / W, 1 - 0.68 / H, f"κ = {kappa:g}, $100k of new spend per run. Each row is one seed; each block is one purchase, as wide as "
             "its cost. Every policy starts a seed from the same five seed alloys.", fontsize=13.5, color=GRAY, va="center")
    handles = [Patch(fc=c, ec="none", label=f"{name} (${COSTS[g]:,.0f})") for g, (name, c) in STAGES.items()]
    handles.append(Line2D([], [], color=RED, lw=0, marker="|", ms=13, mew=3.2, label="Test that beat the best alloy so far"))
    fig.legend(handles=handles, loc="center left", bbox_to_anchor=(L / W - 0.006, 1 - 1.04 / H), ncol=5, frameon=False,
               fontsize=13, handlelength=1.2, handleheight=0.9, columnspacing=1.6)
    gx = (W - 2 * PW - L - R)  # gap between the two columns
    for j, text in enumerate(COLUMNS):
        fig.text((L + j * (PW + gx)) / W, 1 - (top_h - 0.12) / H, text, fontsize=14, color=INK, va="bottom")
        fig.add_artist(Line2D([(L + j * (PW + gx)) / W, (L + j * (PW + gx) + PW) / W], [1 - (top_h - 0.06) / H] * 2,
                              color=LIGHT, lw=0.8))
    min_w = budget / (PW * 200) * 1.6  # 1.6 px at the saved 200 dpi: $10 calls and $200 tests stay visible
    for i, pair in enumerate(GRID):
        y_top = top_h + i * (head_h + panel_h + gap_h) + head_h
        for j, kind in enumerate(pair):
            runs, root = load(kind, kappa, TAPES)
            x0 = L + j * (PW + gx)
            ax = fig.add_axes([x0 / W, 1 - (y_top + panel_h) / H, PW / W, panel_h / H])
            ax.set_xlim(0, budget)
            ax.set_ylim(n_rows - 0.5, -0.5)
            ax.set_yticks([])
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_color(LIGHT)
            ax.set_xticks(np.arange(0, budget + 1, 25_000))
            ax.set_xticklabels([f"${v / 1e3:.0f}k" for v in ax.get_xticks()] if i == len(GRID) - 1 else [])
            ax.tick_params(labelsize=12, pad=4)
            for v in ax.get_xticks()[1:-1]:
                ax.axvline(v, color="#EDEDED", lw=0.7, zorder=0)
            bold = kind == "pkgfn"
            counts, end = stats(runs, ystar)
            ax.text(0, 1 + 0.30 / panel_h, SHORT[kind], transform=ax.transAxes, fontsize=15.5, color=INK,
                    fontweight="bold" if bold else "normal", va="bottom")
            ax.text(1, 1 + 0.30 / panel_h, end, transform=ax.transAxes, fontsize=12.5, color=INK, ha="right", va="bottom")
            ax.text(0, 1 + 0.06 / panel_h, counts, transform=ax.transAxes, fontsize=12, color=MUTED, va="bottom")
            h = 0.74
            for row, r in enumerate(runs[:n_rows]):
                segs = defaultdict(list)
                for g, s, e, better in purchases(r):
                    segs["best" if better else g].append((s, max(e - s, min_w)))
                for g in "ALCT":
                    if segs[g]:
                        lined = g in "AL"  # a white hairline between back-to-back blocks, e.g. pKGFN's runs of prints
                        ax.broken_barh(segs[g], (row - h / 2, h), facecolors=STAGES[g][1], edgecolors="white" if lined else "none",
                                       linewidth=0.45 if lined else 0, zorder=3 + (g in "CT"))
                if segs["best"]:
                    ax.broken_barh([(s - min_w * 0.4, max(w, min_w) + min_w * 0.8) for s, w in segs["best"]],
                                   (row - h * 0.82, h * 1.64), facecolors=RED, edgecolors="none", zorder=5)
            if len(runs) < n_rows:
                ax.text(0.5, (len(runs) + (n_rows - len(runs)) / 2) / n_rows, f"{len(runs)} smoke-test seeds only "
                        f"({root.relative_to(HERE.parent)}); the 20-seed grid has not been run",
                        transform=ax.transAxes, ha="center", va="center", fontsize=12.5, color=MUTED)
    fig.text(L / W, 0.18 / H, "New spend on experiments and simulations", fontsize=13, color="#404040", va="center")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- composition
def alloys(run):
    """Per composition the policy atomized or printed: the spend when it was first made and its number of
    prints; and the compositions it only simulated."""
    made, sims = {}, set()
    for g, end, inp in run["purchases"]:
        key = tuple(round(v, 6) for v in inp[: len(COMP)])
        if g == "C":
            sims.add(key)
        elif g in "AL":
            m = made.setdefault(key, {"first": end, "prints": 0})
            m["prints"] += g == "L"
    return made, sims - set(made)


def size(prints):
    return 14 + 15 * np.asarray(prints, dtype=float)


def figure_composition(kappa, out):
    xo = optimum_design(kappa)
    fo, go = (float(v[0]) for v in calphad(xo[COMP].numpy()))
    W, H = 15.5, 9.4
    fig, axes = plt.subplots(2, 4, figsize=(W, H), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.065, right=0.985, top=0.80, bottom=0.085, wspace=0.08, hspace=0.30)
    fig.text(0.065, 0.955, "Where each policy makes alloys", fontsize=22, fontweight="bold", color=INK, va="center")
    fig.text(0.065, 0.903, "Every alloy a policy atomized or printed, placed by what CALPHAD predicts for it. The screen keeps only "
             f"f ≤ {F_SAFE:g}, but enough nucleant lets an alloy", fontsize=13.5, color=GRAY, va="center")
    fig.text(0.065, 0.873, f"with a wider freezing range print without cracking. The optimum (red star) has f = {fo:.2f} and "
             f"g = {go:.2f}. Seeds 0–4 pooled (KGFN: seeds 0–1, a smoke test), κ = {kappa:g}.", fontsize=13.5, color=GRAY,
             va="center")
    gg = np.linspace(0, 1.0, 200)
    fc = crack_line(kappa, gg)
    for j in range(4):
        for i in range(2):
            kind = GRID[j][i]
            ax = axes[i, j]
            ax.fill_betweenx(gg, fc, 1.1, color=FAINT, lw=0, zorder=0)
            ax.plot(fc, gg, color=LIGHT, lw=1.2, zorder=1)
            ax.axvline(F_SAFE, color=GRAY, lw=1.1, ls=(0, (4, 3)), zorder=1)
            runs, root = load(kind, kappa, LOGGED)
            pts, sims = [], []
            for r in runs:
                made, only = alloys(r)
                pts += [(k, m["first"], m["prints"]) for k, m in made.items()]
                sims += list(only)
            if sims:
                f, g = calphad(sims)
                ax.scatter(f, g, s=4, color="#C8C8C8", lw=0, zorder=2)
            if pts:
                pts.sort(key=lambda p: p[1])  # late alloys on top
                f, g = calphad([p[0] for p in pts])
                when = np.array([p[1] for p in pts]) / 100_000
                ax.scatter(f, g, s=size([p[2] for p in pts]), c=WHEN(when), ec="white", lw=0.6, zorder=3, alpha=0.95)
            ax.plot([fo], [go], marker="*", ms=17, color=RED, mec="white", mew=1.0, zorder=6, ls="none")
            ax.set_xlim(0, 1.05)
            ax.set_ylim(0, 1.0)
            ax.set_xticks([0, F_SAFE, 0.5, 0.75, 1.0])
            ax.set_xticklabels(["0", f"{F_SAFE:g}", "0.5", "0.75", "1"])
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
            ax.tick_params(labelsize=11.5)
            ax.set_title(SHORT[kind], loc="left", fontsize=14.5, color=INK, fontweight="bold" if kind == "pkgfn" else "normal", pad=22)
            n_seeds = len(runs)
            ax.text(0, 1.035, f"{len(pts)} alloys made, {len(sims)} only simulated ({n_seeds} seeds)", transform=ax.transAxes,
                    fontsize=11.5, color=MUTED, va="bottom")
            if i == 1:
                ax.set_xlabel("freezing-range index f", fontsize=12.5)
            if j == 0:
                ax.set_ylabel("nucleant fraction g", fontsize=12.5)
    a = axes[0, 0]
    a.text(F_SAFE - 0.02, 0.97, "screen\nkeeps", ha="right", va="top", fontsize=11, color=GRAY, linespacing=1.0)
    a.text(1.03, 0.04, "cracks in\nthe print", ha="right", va="bottom", fontsize=11, color=GRAY, linespacing=1.0)
    a.annotate("optimum", (fo, go), xytext=(1.0, 0.93), fontsize=11.5, color=RED, ha="right", va="center",
               path_effects=[withStroke(linewidth=3, foreground="white")],
               arrowprops=dict(arrowstyle="-", color="#E39A9A", lw=1.0, shrinkA=2, shrinkB=7))
    # legends: when an alloy was first made, and prints per alloy
    cax = fig.add_axes([0.555, 0.948, 0.15, 0.016])
    cax.imshow(np.linspace(0, 1, 256)[None, :], aspect="auto", cmap=WHEN, extent=(0, 100, 0, 1))
    cax.set_yticks([])
    cax.set_xticks([0, 50, 100])
    cax.set_xticklabels(["$0", "$50k", "$100k"], fontsize=11)
    cax.tick_params(length=0, pad=2)
    for s in cax.spines.values():
        s.set_visible(False)
    cax.set_title("first made at", fontsize=11.5, color=GRAY, loc="left", pad=3)
    hs = [Line2D([], [], ls="none", marker="o", ms=np.sqrt(size(n)), mfc="#8C8C8C", mec="white", label=f"{n}") for n in (1, 5, 15)]
    hs.append(Line2D([], [], ls="none", marker="o", ms=2.2, mfc="#C8C8C8", mec="none", label="simulated only"))
    fig.legend(handles=hs, loc="center left", bbox_to_anchor=(0.73, 0.957), ncol=4, frameon=False, fontsize=11.5,
               title="prints on the alloy", title_fontsize=11.5, handletextpad=0.3, columnspacing=1.0, alignment="left")
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def check(kappa):
    """Rebuild the purchases of every run that logs them; purchases() raises on any difference."""
    n = 0
    for root in LOGGED:
        for p in sorted((root / f"k{kappa:g}").glob("*.json")):
            purchases(json.loads(p.read_text()))
            n += 1
    print(f"{n} runs with a purchase log: the purchases rebuilt from their actions match it")


# --------------------------------------------------------------------------- builds
def builds(run, truth, ystar):
    """(spend after, true objective % of the optimum, tested) of every build the run printed."""
    tested = Counter(tuple(round(v, 6) for v in inp) for g, _, inp in run["purchases"] if g == "T")
    out = []
    for g, end, inp in run["purchases"]:
        if g == "L":
            key = tuple(round(v, 6) for v in inp)
            y = float(truth.objective(torch.tensor(inp))) / ystar * 100
            out.append((end, y, tested[key] > 0))
            if tested[key]:
                tested[key] -= 1  # one test per build
    return out


def figure_builds(kappa, out):
    ystar, truth = optimum(kappa), AlloyTruth(kappa)
    budget, step = 100_000, 10_000
    fig, axes = plt.subplots(4, 2, figsize=(15.5, 13.0), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.835, bottom=0.06, wspace=0.07, hspace=0.42)
    fig.text(0.07, 0.965, "How good are the builds each policy prints?", fontsize=22, fontweight="bold", color=INK, va="center")
    fig.text(0.07, 0.937, "Every build printed, scored by the true objective of its alloy and settings, against the spend when it "
             "was printed. Filled: tensile-tested; open: printed,", fontsize=13.5, color=GRAY, va="center")
    fig.text(0.07, 0.917, f"never tested. The line is the mean over each $10k of spend. Seeds 0–4 pooled (KGFN: seeds 0–1, a smoke "
             f"test), κ = {kappa:g}. The burden penalty puts poor alloys below zero.", fontsize=13.5, color=GRAY, va="center")
    for j, text in enumerate(COLUMNS):
        fig.text(0.07 + j * 0.4625, 0.888, text, fontsize=14, color=INK, va="bottom")
        fig.add_artist(Line2D([0.07 + j * 0.4625, 0.07 + j * 0.4625 + 0.4525], [0.885] * 2, color=LIGHT, lw=0.8))
    edges = np.arange(0, budget + 1, step)
    for i, pair in enumerate(GRID):
        for j, kind in enumerate(pair):
            ax = axes[i, j]
            runs, _ = load(kind, kappa, LOGGED)
            b = np.array([x for r in runs for x in builds(r, truth, ystar)])
            spend, y, tested = b[:, 0], b[:, 1], b[:, 2].astype(bool)
            ax.axhline(100, color=RED, lw=0.9, ls=(0, (4, 3)), zorder=1)
            ax.axhline(0, color=LIGHT, lw=0.8, zorder=1)
            ax.scatter(spend[tested] / 1e3, y[tested], s=16, color="#8C8C8C", lw=0, zorder=2)
            ax.scatter(spend[~tested] / 1e3, y[~tested], s=16, facecolors="none", edgecolors="#8C8C8C", lw=0.8, zorder=2)
            k = np.digitize(spend, edges[1:-1])
            mean = np.array([y[k == m].mean() if (k == m).any() else np.nan for m in range(len(edges) - 1)])
            ax.plot((edges[:-1] + step / 2) / 1e3, mean, color=RED if kind == "pkgfn" else INK, lw=2.6, zorder=3,
                    solid_capstyle="round", marker="o", ms=4.5)
            late = y[spend > budget - 2 * step]
            ax.set_title(SHORT[kind], loc="left", fontsize=15, color=INK, fontweight="bold" if kind == "pkgfn" else "normal",
                         pad=24)
            ax.text(0, 1.04, f"{len(y) / len(runs):.0f} builds per run, {tested.mean():.0%} tested; builds in the last $20k "
                    f"average {late.mean():.0f}%", transform=ax.transAxes, fontsize=12, color=MUTED, va="bottom")
            ax.set_xlim(0, budget / 1e3)
            ax.set_ylim(-66, 105)
            ax.set_yticks([-50, 0, 50, 100])
            ax.yaxis.grid(True, color="#EDEDED", lw=0.7)
            ax.set_axisbelow(True)
            ax.tick_params(labelsize=12)
            if i == len(GRID) - 1:
                ax.set_xlabel("New spend ($k)", fontsize=12.5)
            if j == 0:
                ax.set_ylabel("% of the optimum", fontsize=12.5)
    axes[0, 0].text(99, 97, "optimum", ha="right", va="top", fontsize=11.5, color=RED)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--kappa", type=float, default=1.0)
    a = ap.parse_args()
    check(a.kappa)
    for f in (figure_purchases, figure_composition, figure_builds):
        name = f.__name__.split("_", 1)[1]
        print(f(a.kappa, HERE / f"bofn_behaviour_{name}_k{a.kappa:g}.png"))


if __name__ == "__main__":
    main()
