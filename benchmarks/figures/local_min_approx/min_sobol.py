"""Locally approximate the min of the BOFN benchmark surface (y5) and plot
the Sobol-sample distribution. Mirrors the construction used in
benchmarks/bofn_actions_benchmark.py: ExtendedManufacturingGPNetwork with
node_costs=[1,10,10,45,20,30], seed=0, noise_std=0.0 (noiseless), coupling=0.3.
"""
import sys, os, json
sys.path.insert(0, "/home/runner/work/digital-alloy-lab-private/digital-alloy-lab-private")
import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from botorch.utils.sampling import draw_sobol_samples
from benchmarks.partial_kgfn.manufacturing_problem import ExtendedManufacturingGPNetwork

problem = ExtendedManufacturingGPNetwork(
    node_costs=[1, 10, 10, 45, 20, 30], seed=0, noise_std=0.0, coupling=0.3,
)
N = 65536
grid = draw_sobol_samples(bounds=problem.bounds, n=N, q=1, seed=0).squeeze(-2)
with torch.no_grad():
    Y = problem.evaluate(grid, noiseless=True)  # (N, 6)
y5 = Y[..., -1].numpy()

stats = {
    "n_samples": N,
    "min": float(y5.min()),
    "argmin_x": grid[int(y5.argmin())].tolist(),
    "max": float(y5.max()),
    "argmax_x": grid[int(y5.argmax())].tolist(),
    "mean": float(y5.mean()),
    "std": float(y5.std()),
    "median": float(np.median(y5)),
    "p01": float(np.percentile(y5, 1)),
    "p05": float(np.percentile(y5, 5)),
    "p95": float(np.percentile(y5, 95)),
    "p99": float(np.percentile(y5, 99)),
}
print(json.dumps(stats, indent=2))

# Per-node summaries to give a feel for the surface response
print("\nper-node Sobol summary (noiseless):")
print(f"{'node':<6}{'min':>10}{'mean':>10}{'std':>10}{'max':>10}")
for j in range(Y.shape[-1]):
    yj = Y[..., j].numpy()
    print(f"y{j:<5}{yj.min():>10.4f}{yj.mean():>10.4f}{yj.std():>10.4f}{yj.max():>10.4f}")

# Plot: histogram of y5 + per-node KDE-style histograms
fig, axes = plt.subplots(2, 1, figsize=(8, 7))
ax = axes[0]
ax.hist(y5, bins=80, color="C0", edgecolor="k", alpha=0.85)
ax.axvline(stats["min"], color="r", lw=1.5, label=f"min = {stats['min']:.3f}")
ax.axvline(stats["max"], color="g", lw=1.5, label=f"max = {stats['max']:.3f}")
ax.axvline(stats["mean"], color="k", lw=1.0, ls="--", label=f"mean = {stats['mean']:.3f}")
ax.set_xlabel("y5 (terminal node, noiseless)")
ax.set_ylabel(f"count over {N} Sobol samples")
ax.set_title("Sobol-sampled distribution of y5 (BOFN benchmark surface response)")
ax.legend()

ax = axes[1]
for j in range(Y.shape[-1]):
    ax.hist(Y[..., j].numpy(), bins=60, histtype="step", lw=1.4, label=f"y{j}")
ax.set_xlabel("node output value")
ax.set_ylabel("count")
ax.set_title("Per-node Sobol distributions")
ax.legend(ncol=3, fontsize=8)

plt.tight_layout()
out = "/tmp/sobol_y5_distribution.png"
plt.savefig(out, dpi=140)
print(f"\nplot written to {out}")

# Local refinement: multi-start L-BFGS-B from the best K Sobol points,
# minimizing y5 over the 5-D bounded box.
from scipy.optimize import minimize

def f_y5(x_np):
    x = torch.as_tensor(x_np, dtype=torch.double).unsqueeze(0)
    with torch.no_grad():
        return float(problem.evaluate(x, noiseless=True)[..., -1].item())

K = 32
order = np.argsort(y5)[:K]
bounds_np = list(zip(problem.bounds[0].tolist(), problem.bounds[1].tolist()))
best = None
for idx in order:
    x0 = grid[int(idx)].numpy()
    try:
        res = minimize(f_y5, x0, method="L-BFGS-B", bounds=bounds_np,
                       options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 200})
        if best is None or res.fun < best.fun:
            best = res
    except Exception as e:
        print("warn:", e)

print(f"\nlocal-refined min y5 = {best.fun:.6f}")
print(f"  at x* = {best.x.tolist()}")
print(f"  Sobol-only min y5    = {stats['min']:.6f}  (improvement {stats['min']-best.fun:.4f})")
