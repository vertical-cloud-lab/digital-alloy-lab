"""Recompute the copper/DED headline numbers from the stored copper runs (benchmarks/bofn-cu-ded).

The runs are this repo's benchmarks/bofn-cu-ded/results/k1e1/ at commit 0f1817c (148 files in
results/, 146 of them in the headline cell k1e1). The optimum J* = 0.492187251856002 is
benchmarks/bofn-cu-ded/truth_tables.json at the same commit.

It prints each method's mean ± SE at $100k and, for each baseline, the spend at which each
network method's MEAN curve first reaches that baseline's $100k mean. "4.2x less spend" is
full-chain BOFN (eifn) reaching standard BO's (ei) $100k level at $24k: 100/24 = 4.17.
It is a ratio of mean curves with no confidence interval.

Usage:  python copper_ratio_check.py <dir with the k1e1 *.json files>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

GRID = np.arange(0, 100_001, 250.0)
J_STAR = 0.492187251856002


def curve(rows: list[dict]) -> np.ndarray:
    spent = np.array([r["spent"] for r in rows])
    vals = np.array([r["best_validated"] if r["best_validated"] == r["best_validated"] else -np.inf for r in rows])
    vals = np.maximum.accumulate(vals)
    idx = np.searchsorted(spent, GRID, side="right") - 1
    return np.where(idx >= 0, vals[np.clip(idx, 0, None)], np.nan)


def first_cost(mean_curve: np.ndarray, target: float) -> float:
    hit = mean_curve >= target - 1e-12
    return GRID[hit.argmax()] if hit.any() else np.inf


def main(folder: Path) -> None:
    C: dict[str, list[np.ndarray]] = {}
    for path in sorted(folder.glob("*.json")):
        run = json.loads(path.read_text())
        C.setdefault(run["kind"], []).append(curve(run["rows"]) / J_STAR)
    M = {k: np.nanmean(np.stack(v), 0) for k, v in C.items()}
    for k, v in sorted(C.items()):
        a = np.stack(v)[:, -1] * 100
        print(f"{k:14s} n={len(a):2d}  $100k: {a.mean():5.1f} ± {a.std() / np.sqrt(len(a)):.1f} % of optimum")
    for base in ("ei", "random", "tiered"):
        target = M[base][-1]
        own = first_cost(M[base], target)
        cells = [f"{k} at ${first_cost(M[k], target) / 1e3:.2f}k ({own / max(first_cost(M[k], target), GRID[1]):.2f}x)"
                 for k in ("eifn", "eifn_reuse", "pkgfn") if k in M]
        print(f"reach {base}'s $100k mean ({target:.1%}; its own curve gets there at ${own / 1e3:.2f}k): " + "; ".join(cells))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
