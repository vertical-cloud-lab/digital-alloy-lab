"""Compare higher-fidelity pKGFN re-runs with the stored production runs, seed by seed.

    python quality/compare_hq.py quality/results-hq/sacq256-ncand16 [quality/results-hq/sacq128-ncand32 ...]

For every folder, the seeds that finished are matched with results/k1/pkgfn_s<seed>.json
(the stored runs at S_ACQ = 64, N_CAND = 16). Prints the best-validated score at
$25k, $50k and $100k for both, paired differences with a Wilcoxon test, purchase
counts and GP-fit failures, and draws quality/fidelity_k1.png: mean curves of the
matched seeds at both fidelities, with tiered screening on the same seeds for scale.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from scipy.stats import wilcoxon  # noqa: E402

from analyze import GRID, curve, first_cost, optimum  # noqa: E402

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "results" / "k1"
ys = optimum(1.0)
AT = (25_000, 50_000, 100_000)


def load_dir(d):
    out = {}
    for p in sorted(Path(d).glob("**/pkgfn_s*.json")):
        r = json.loads(p.read_text())
        out[r["seed"]] = r
    return out


def summarize(label, hq):
    stored = {s: json.loads((RES / f"pkgfn_s{s}.json").read_text()) for s in hq}
    seeds = sorted(hq)
    if not seeds:
        print(f"{label}: no finished runs yet")
        return None
    A = np.stack([curve(stored[s]["rows"], "best_validated") for s in seeds]) / ys * 100
    B = np.stack([curve(hq[s]["rows"], "best_validated") for s in seeds]) / ys * 100
    st = hq[seeds[0]].get("settings", {})
    print(f"\n=== {label}: {len(seeds)} matched seeds {seeds}; settings {st}; "
          f"mean wall {np.mean([r['wall_s'] for r in hq.values()])/60:.1f} min vs {np.mean([stored[s]['wall_s'] for s in seeds])/60:.1f} min stored")
    print(f"  GP fits: {sum(r.get('gp_fits', {}).get('calls', 0) for r in hq.values())} calls, {sum(r.get('gp_fits', {}).get('failures', 0) for r in hq.values())} failures")
    rows = []
    for metric in ("best_validated", "rec_printed"):
        Am = np.stack([curve(stored[s]["rows"], metric) for s in seeds]) / ys * 100
        Bm = np.stack([curve(hq[s]["rows"], metric) for s in seeds]) / ys * 100
        print(f"  metric {metric} ({'printed and tested' if metric == 'best_validated' else 'best printed alloy by the model, tested or not'}):")
        for at in AT:
            i = int(np.searchsorted(GRID, at))
            a, b = Am[:, i], Bm[:, i]
            d = b - a
            p = wilcoxon(d).pvalue if np.any(d != 0) else 1.0
            if metric == "best_validated":
                rows.append((at, a.mean(), a.std() / np.sqrt(len(a)), b.mean(), b.std() / np.sqrt(len(b)), d.mean(), int((d > 0).sum()), int((d == 0).sum()), int((d < 0).sum()), p))
            print(f"    @${at/1e3:>3.0f}k: stored {a.mean():5.1f} ± {a.std()/np.sqrt(len(a)):.1f}   high-fidelity {b.mean():5.1f} ± {b.std()/np.sqrt(len(b)):.1f}   diff {d.mean():+5.1f} pts (HQ better on {int((d>0).sum())}, ties {int((d==0).sum())}, worse on {int((d<0).sum())}; Wilcoxon p = {p:.2f})")
    for name, runs in (("stored", stored), ("high-fidelity", hq)):
        cnt = {g: np.mean([runs[s]["counts"][g] for s in seeds]) - (5 if g != "C" else 37) for g in ("C", "A", "L", "T")}
        print(f"  new purchases per run, {name:13s}: " + ", ".join(f"{g} {v:.1f}" for g, v in cnt.items()))
    # cost to screening's level on these seeds
    tiered = np.stack([curve(json.loads((RES / f"tiered_s{s}.json").read_text())["rows"], "best_validated") for s in seeds]) / ys * 100
    tgt = np.nanmean(tiered[:, -1])
    ca, cb, ct = (first_cost(np.nanmean(X, 0), tgt) for X in (A, B, tiered))
    print(f"  on these seeds, screening's $100k level is {tgt:.1f}%, first reached at ${ct/1e3:.1f}k; stored pKGFN at ${ca/1e3:.1f}k ({ct/ca:.2f}x), high-fidelity pKGFN at ${cb/1e3:.1f}k ({ct/cb:.2f}x)")
    return seeds, A, B, tiered, rows


def figure(results, out):
    for f in (Path.home() / ".local/share/fonts/aptos").glob("Aptos*.ttf"):
        matplotlib.font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({"font.family": "Aptos", "font.size": 16, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#8C8C8C"})
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(7.2 * n, 5.2), squeeze=False)
    x = GRID / 1e3
    for ax, (label, (seeds, A, B, T, _)) in zip(axes[0], results.items()):
        series = ((T, "#8C8C8C", 2.0, "Tiered screening"), (A, "#E6B3B3", 2.6, "pKGFN, stored\n(64 base samples, 16 candidates)"), (B, "#C00000", 2.6, "pKGFN, " + label))
        finals = {name: float(np.nanmean(arr, 0)[-1]) for arr, _, _, name in series}
        # stack the end labels so they do not collide (two-line labels need more room)
        order = sorted(finals, key=lambda k: finals[k])
        ypos, last = {}, -1e9
        for k in order:
            ypos[k] = max(finals[k], last + (7.5 if "\n" in k else 5.5))
            last = ypos[k]
        for arr, col, lw, name in series:
            m = np.nanmean(arr, 0)
            ax.plot(x, m, color=col, lw=lw)
            tc = col if col != "#E6B3B3" else "#B07070"
            ax.plot([100.3, 102.2], [m[-1], ypos[name]], color=col, lw=1.2, alpha=0.6, clip_on=False)
            ax.text(103, ypos[name], name, color=tc, va="center", ha="left", fontsize=14, linespacing=0.95, clip_on=False)
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 100])
        lo, hi = float(np.nanmean(A, 0)[0]), float(max(np.nanmean(A, 0)[-1], np.nanmean(B, 0)[-1]))
        ax.set_yticks([lo, hi], [f"{lo:.0f}", f"{hi:.0f}"])
        for side in ("left", "bottom"):
            ax.spines[side].set_position(("outward", 10))
        ax.spines["left"].set_bounds(lo, hi)
        ax.set_xlabel("New spend ($k)")
        ax.text(-0.08, 1.02, f"Best alloy demonstrated\n(% of optimum), {len(seeds)} matched seeds", transform=ax.transAxes, ha="left", va="bottom", fontsize=16, color="#404040")
    fig.subplots_adjust(left=0.08, right=0.78, top=0.84, bottom=0.17, wspace=1.3)
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")


if __name__ == "__main__":
    results = {}
    for d in sys.argv[1:]:
        label = Path(d).name.replace("sacq", "S=").replace("-ncand", ", candidates=")
        r = summarize(label, load_dir(d))
        if r:
            results[label] = r
    if results:
        figure(results, HERE / "fidelity_k1.png")
