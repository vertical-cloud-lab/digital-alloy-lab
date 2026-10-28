"""pKGFN at the light Monte Carlo settings of the first sweep (quality/results-light/) against the same
seeds at the aluminum production settings with the Edison fixes F2 and F4 (results/). Writes
quality/compare_light_hq.md.

    python quality/compare_light_hq.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from analyze import GRID, curve, optimum  # noqa: E402

CELL = (1.0, 1.0)


def load(folder):
    return {json.loads(p.read_text())["seed"]: json.loads(p.read_text()) for p in sorted(folder.glob("pkgfn_s*.json"))}


def main():
    light = load(HERE / "results-light" / "k1e1")
    hq = load(HERE.parent / "results" / "k1e1")
    seeds = sorted(set(light) & set(hq))
    J = optimum(*CELL)
    L = ["# pKGFN: light vs production Monte Carlo settings, matched seeds (written by `quality/compare_light_hq.py`)", "",
         f"Light: S = {light[seeds[0]]['settings']['S_ACQ'] if seeds else '?'} base samples, {light[seeds[0]]['settings']['N_CAND'] if seeds else '?'} candidates, a {light[seeds[0]]['settings']['N_POOL'] if seeds else '?'} pool. "
         f"Production: S = {hq[seeds[0]]['settings']['S_ACQ'] if seeds else '?'}, {hq[seeds[0]]['settings']['N_CAND'] if seeds else '?'} candidates, a {hq[seeds[0]]['settings']['N_POOL'] if seeds else '?'} pool, with the F2 and F4 fixes. "
         "Best alloy demonstrated, % of the optimum.", "",
         "| Seed | light $25k | production $25k | light $50k | production $50k | light $100k | production $100k | purchases (light / production) | made by the fallback (light / production) | wall time, min (production) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    diffs = []
    for s in seeds:
        a, b = curve(light[s]["rows"]) / J, curve(hq[s]["rows"]) / J
        i25, i50, i100 = (int(np.searchsorted(GRID, v)) for v in (25_000, 50_000, 100_000))
        fa = sum(1 for r in light[s]["rows"][1:] if r.get("fallback"))
        fb = sum(1 for r in hq[s]["rows"][1:] if r.get("fallback"))
        L.append(f"| {s} | {a[i25]:.0%} | {b[i25]:.0%} | {a[i50]:.0%} | {b[i50]:.0%} | {a[i100]:.0%} | {b[i100]:.0%} | {len(light[s]['rows']) - 1} / {len(hq[s]['rows']) - 1} | "
                 f"{fa} / {fb} | {hq[s].get('wall_s', float('nan')) / 60:.0f} |")
        diffs.append(b[i100] - a[i100])
    if seeds:
        L += ["", f"Mean change at $100k on these {len(seeds)} seeds: {np.mean(diffs):+.0%} of the optimum (production minus light)."]
    (HERE / "compare_light_hq.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
