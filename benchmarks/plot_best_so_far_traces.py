"""Best-so-far traces vs cumulative cost, cropped to pKGFN budget.

Reads per-seed JSONs from benchmarks/results/actions_hpc/<RUN_ID>/ and produces
a 'best-so-far vs cost' plot where every algorithm is cropped to the maximum
budget that pKGFN actually reached (since pKGFN is still running and has used
less of the $2,400 cost cap than the other algorithms).
"""
import json
import glob
import os
import sys
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN_ID = sys.argv[1] if len(sys.argv) > 1 else "pkgfn-noFb2-20260501T071019Z"
REPO = "/home/runner/work/digital-alloy-lab-private/digital-alloy-lab-private"
RESULTS = f"{REPO}/benchmarks/results/actions_hpc/{RUN_ID}"
FIGS = f"{REPO}/benchmarks/figures/actions_hpc/{RUN_ID}"
os.makedirs(FIGS, exist_ok=True)

ALGOS = ["pKGFN", "TSFN", "HighFidOnly", "Random", "Sobol", "LowFidOnly", "Node2Only"]
COLORS = {
    "pKGFN": "tab:red",
    "TSFN": "tab:blue",
    "HighFidOnly": "tab:green",
    "Random": "tab:gray",
    "Sobol": "tab:purple",
    "LowFidOnly": "tab:olive",
    "Node2Only": "tab:brown",
}


def load_traces(algo):
    files = sorted(glob.glob(f"{RESULTS}/{algo}_seed*.json"))
    seeds = []
    init_best = None
    true_max = None
    for f in files:
        d = json.load(open(f))
        bv = np.asarray(d["best_vals"], dtype=float)
        ct = np.asarray(d["cost_trace"], dtype=float)
        if len(bv) == 0:
            continue
        # Reconstruct init point: prepend (cost=init_cost, best=init_best)
        # init_cost = ct[0] - per_iter_cost is unknown, but the first entry is
        # already "after init + 0 iters" if best_vals[0] == init_best with the
        # init cost. The benchmark's convention: best_vals[i] is the best
        # observed up to and including iteration i (init + i optim iters).
        # cost_trace[i] is cumulative cost after i optim iters, *including*
        # init cost. So the first entry corresponds to init only.
        seeds.append((ct, bv))
        init_best = bv[0] if init_best is None else min(init_best, bv[0])
        true_max = d.get("true_max", true_max)
    return seeds, init_best, true_max


# Determine pKGFN cost cap = max final cost across pKGFN seeds.
pkgfn_seeds, init_best, true_max = load_traces("pKGFN")
pkgfn_finals = [s[0][-1] for s in pkgfn_seeds]
COST_CAP = float(max(pkgfn_finals))
COST_MIN_PKGFN = float(min(pkgfn_finals))
print(f"pKGFN final cost: min={COST_MIN_PKGFN:.0f}, max={COST_CAP:.0f}")

# Common cost grid up to pKGFN cap.
COST_MIN = float(min(s[0][0] for s in pkgfn_seeds))  # initial cost
GRID = np.linspace(COST_MIN, COST_CAP, 250)


def interp_seeds(seeds, grid):
    """Step-interpolate (cost, best_so_far) onto a common grid.

    Each trace is monotone non-decreasing in best (best-so-far). We use
    np.searchsorted to find the latest cost <= each grid point.
    """
    rows = []
    for ct, bv in seeds:
        if ct[0] > grid[0]:
            # Pad left with bv[0] back to grid[0]
            ct = np.concatenate([[grid[0]], ct])
            bv = np.concatenate([[bv[0]], bv])
        idx = np.searchsorted(ct, grid, side="right") - 1
        idx = np.clip(idx, 0, len(bv) - 1)
        rows.append(bv[idx])
    return np.asarray(rows)


fig, ax = plt.subplots(figsize=(9, 5.5))
init_init_cost = COST_MIN
ax.axvline(init_init_cost, color="k", ls=":", lw=0.6, alpha=0.5)
ax.text(init_init_cost, ax.get_ylim()[1] if False else 17.05, " init", fontsize=8, color="k", alpha=0.6)

summary_rows = []
for algo in ALGOS:
    seeds, _, _ = load_traces(algo)
    if not seeds:
        continue
    arr = interp_seeds(seeds, GRID)
    mean = arr.mean(axis=0)
    std = arr.std(axis=0)
    final_mean = mean[-1]
    final_std = std[-1]
    summary_rows.append((algo, len(seeds), final_mean, final_std))
    ax.plot(GRID, mean, label=f"{algo} (n={len(seeds)})", color=COLORS.get(algo), lw=1.8)
    ax.fill_between(GRID, mean - std, mean + std, color=COLORS.get(algo), alpha=0.12, lw=0)

ax.axhline(true_max, color="k", ls="--", lw=0.8, alpha=0.6, label=f"true max = {true_max:.3f}")
ax.set_xlabel("Cumulative cost ($)")
ax.set_ylabel("Best-so-far (y5, posterior-mean tracker)")
ax.set_title(
    f"Best-so-far vs cost — all algorithms cropped to pKGFN budget\n"
    f"RUN_ID={RUN_ID}  |  budget cap = ${COST_CAP:.0f} (max pKGFN final cost)"
)
ax.set_xlim(COST_MIN, COST_CAP)
ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
ax.grid(True, alpha=0.3)
out = f"{FIGS}/best_so_far_traces_pkgfn_budget.png"
fig.tight_layout()
fig.savefig(out, dpi=140)
print(f"saved: {out}")

# Print summary table at the cropped budget
print("\nFinal mean ± std at pKGFN budget cap (${:.0f}):".format(COST_CAP))
for algo, n, m, s in sorted(summary_rows, key=lambda r: -r[2]):
    print(f"  {algo:12s} n={n:2d}  {m:.3f} ± {s:.3f}")

# Also dump a JSON
import json as _json
ranking = {
    "run_id": RUN_ID,
    "cost_cap": COST_CAP,
    "cost_min": COST_MIN,
    "true_max": true_max,
    "init_best": init_best,
    "ranking_at_cap": [
        {"algo": a, "n_seeds": n, "final_mean": float(m), "final_std": float(s)}
        for a, n, m, s in sorted(summary_rows, key=lambda r: -r[2])
    ],
}
with open(f"{FIGS}/best_so_far_pkgfn_budget_summary.json", "w") as f:
    _json.dump(ranking, f, indent=2)
print(f"saved: {FIGS}/best_so_far_pkgfn_budget_summary.json")
