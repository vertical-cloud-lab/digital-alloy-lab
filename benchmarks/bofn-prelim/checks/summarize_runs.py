"""Summarize the stored runs of the aluminum LPBF benchmark (benchmarks/bofn-prelim).

The runs are the 292 per-run JSON files in this repo's benchmarks/bofn-prelim/results/ at
commit 5525f07. This script needs only numpy and scipy. It rebuilds
the "best alloy demonstrated" curves the same way the benchmark's own analyze.py does
($250 spend grid, running maximum, divided by the true optimum), then writes:

  curves_best_so_far.csv   one row per (scenario, method, seed, spend on the $250 grid)
  run_index.csv            one row per run file
  headline_check.txt       the headline numbers, recomputed: mean ± SE at $25k, $50k and
                           $100k, spend ratios with bootstrap intervals, matched-seed tests

Usage:  python summarize_runs.py <results-dir> <out-dir>
        (<results-dir> holds k0/, k0.5/ and k1/ with <method>_s<seed>.json files)
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

GRID = np.arange(0, 100_001, 250.0)  # the benchmark's own spend grid (analyze.GRID)
# True optimum of the objective at each bias level, as supplied to the Oct 5 independent
# re-analysis (benchmarks/bofn-prelim/edison/results/analysis-review.md at 5525f07).
OPTIMUM = {1.0: 0.693739, 0.5: 0.530736, 0.0: 0.484755}
LABEL = {
    "eifn_reuse": "BOFN with powder reuse",
    "pkgfn": "pKGFN (picks one step at a time)",
    "eifn": "BOFN, full chain every time",
    "ei": "Standard BO (one model, full chain)",
    "random": "Random designs (full chain)",
    "tiered": "Tiered screening (screen, then test)",
    "tiered_naive": "Tiered screening, no powder reuse",
    "pkgfn_free": "pKGFN variant: any alloy, with lookahead",
    "pkgfn_la": "pKGFN variant: lookahead, simulated alloys only",
}
ORDER = list(LABEL)


def load(results: Path) -> list[dict]:
    runs = []
    for path in sorted(results.glob("k*/*.json")):
        run = json.loads(path.read_text())
        run["file"] = path.relative_to(results).as_posix()
        runs.append(run)
    return runs


def curve(rows: list[dict], metric: str = "best_validated") -> np.ndarray:
    """Step function of the running best on GRID (same construction as analyze.curve)."""
    spent = np.array([r["spent"] for r in rows])
    vals = np.array([r[metric] if r[metric] == r[metric] else -np.inf for r in rows])
    vals = np.maximum.accumulate(vals)
    idx = np.searchsorted(spent, GRID, side="right") - 1
    return np.where(idx >= 0, vals[np.clip(idx, 0, None)], np.nan)


def first_cost(mean_curve: np.ndarray, target: float) -> float:
    hit = mean_curve >= target - 1e-12
    return GRID[hit.argmax()] if hit.any() else np.inf


def speedup(cm: np.ndarray, cb: np.ndarray, n: int = 2000, seed: int = 0):
    """Spend the baseline's mean curve needs to reach its own $100k mean, divided by the
    spend the method's mean curve needs to reach that level; seeds bootstrapped per policy
    (same estimator and resampling order as analyze.speedup)."""
    rng = np.random.default_rng(seed)

    def one(a, b):
        target = np.nanmean(b[:, -1])
        return first_cost(np.nanmean(b, 0), target) / max(first_cost(np.nanmean(a, 0), target), GRID[1])

    est = one(cm, cb)
    boot = np.array([one(cm[rng.integers(0, len(cm), len(cm))], cb[rng.integers(0, len(cb), len(cb))])
                     for _ in range(n)])
    target = np.nanmean(cb[:, -1])
    return est, np.percentile(boot, 5), np.percentile(boot, 95), first_cost(np.nanmean(cm, 0), target), \
        first_cost(np.nanmean(cb, 0), target), target


def cost_to(c: np.ndarray, target: float) -> np.ndarray:
    hit = c >= target
    return np.where(hit.any(1), GRID[hit.argmax(1)], np.inf)


def main(results: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    runs = load(results)
    C: dict[tuple[float, str], dict[int, np.ndarray]] = {}
    for run in runs:
        C.setdefault((run["kappa"], run["kind"]), {})[run["seed"]] = curve(run["rows"]) / OPTIMUM[run["kappa"]]

    with open(out / "curves_best_so_far.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["kappa", "method", "seed", "spend_usd", "best_share_of_optimum"])
        for (kappa, kind), by_seed in sorted(C.items(), key=lambda kv: (-kv[0][0], ORDER.index(kv[0][1]))):
            for seed_, c in sorted(by_seed.items()):
                for x, y in zip(GRID, c):
                    w.writerow([f"{kappa:g}", kind, seed_, int(x), f"{y:.4f}"])

    i25, i50, i100 = (int(np.searchsorted(GRID, v)) for v in (25_000, 50_000, 100_000))
    with open(out / "run_index.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "kappa", "method", "seed", "decisions", "final_spend_usd",
                    "calphad_calls", "atomizations", "prints", "tensile_tests",
                    "best_share_at_25k", "best_share_at_50k", "best_share_at_100k"])
        for run in runs:
            c = C[(run["kappa"], run["kind"])][run["seed"]]
            k = run["counts"]
            w.writerow([run["file"], f"{run['kappa']:g}", run["kind"], run["seed"], len(run["rows"]) - 1,
                        f"{run['rows'][-1]['spent']:.0f}", k["C"], k["A"], k["L"], k["T"],
                        f"{c[i25]:.4f}", f"{c[i50]:.4f}", f"{c[i100]:.4f}"])

    lines = [f"Run files: {len(runs)}"]
    for kappa in (1.0, 0.5, 0.0):
        lines.append(f"\nkappa = {kappa:g}: best alloy demonstrated, % of optimum, mean ± SE (population SD / sqrt n)")
        lines.append(f"{'method':<44} n   $25k        $50k        $100k       median $ to 80% (share of seeds reaching)")
        for kind in ORDER:
            if (kappa, kind) not in C:
                continue
            arr = np.stack(list(C[(kappa, kind)].values()))
            cells = []
            for i in (i25, i50, i100):
                v = arr[:, i] * 100
                cells.append(f"{v.mean():5.1f} ± {v.std() / np.sqrt(len(v)):4.1f}")
            ct = cost_to(arr, 0.8)
            med = np.median(ct)
            med_s = ">$100k" if not np.isfinite(med) else f"${med / 1e3:.2f}k"
            lines.append(f"{LABEL[kind]:<44} {len(arr):<3} " + "  ".join(cells) + f"  {med_s} ({np.isfinite(ct).mean():.0%})")

    lines.append("\nkappa = 1: spend to reach tiered screening's $100k mean level (mean curves), 90% bootstrap CI")
    cb = np.stack(list(C[(1.0, "tiered")].values()))
    for kind in ("pkgfn", "eifn_reuse", "eifn", "ei", "random"):
        cm = np.stack(list(C[(1.0, kind)].values()))
        est, lo, hi, c_m, c_b, target = speedup(cm, cb)
        lines.append(f"  {LABEL[kind]:<44} reaches {target:.1%} at ${c_m / 1e3:.2f}k vs ${c_b / 1e3:.2f}k for screening:"
                     f" {est:.2f}x (90% CI {lo:.1f} to {hi:.1f})")

    lines.append("\nkappa = 1: the same ratio against fixed targets (mean curves; tiered's spend / the method's spend)")
    mean = {k: np.nanmean(np.stack(list(C[(1.0, k)].values())), 0) for k in ("tiered", "eifn_reuse", "pkgfn", "eifn", "ei")}
    for target in (0.55, 0.60, 0.625):
        c_b = first_cost(mean["tiered"], target)
        cells = [f"{k} ${first_cost(mean[k], target) / 1e3:.2f}k ({c_b / max(first_cost(mean[k], target), GRID[1]):.2f}x)"
                 for k in ("eifn_reuse", "pkgfn", "eifn", "ei")]
        lines.append(f"  target {target:.1%}: tiered ${c_b / 1e3:.2f}k; " + "; ".join(cells))

    lines.append("\nMatched seeds, Wilcoxon signed-rank (scipy default, two-sided), best share at a given spend")
    pairs = [(1.0, "eifn", "ei"), (1.0, "eifn_reuse", "ei"), (1.0, "eifn_reuse", "eifn"), (1.0, "eifn_reuse", "tiered"),
             (1.0, "pkgfn", "tiered"), (0.0, "eifn_reuse", "tiered"), (0.0, "eifn", "tiered"), (0.0, "ei", "tiered")]
    for kappa, a, b in pairs:
        A, B = C[(kappa, a)], C[(kappa, b)]
        seeds = sorted(set(A) & set(B))
        for at, i in (("$25k", i25), ("$50k", i50), ("$100k", i100)):
            x = np.array([A[s][i] for s in seeds])
            y = np.array([B[s][i] for s in seeds])
            d = x - y
            p = wilcoxon(d).pvalue if np.any(d != 0) else 1.0
            lines.append(f"  kappa {kappa:g} {a} vs {b} @{at} (n={len(seeds)}): {x.mean():.1%} vs {y.mean():.1%},"
                         f" wins/ties/losses {int((d > 0).sum())}/{int((d == 0).sum())}/{int((d < 0).sum())}, p = {p:.3g}")

    text = "\n".join(lines) + "\n"
    (out / "headline_check.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
