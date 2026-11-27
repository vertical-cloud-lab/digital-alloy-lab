"""Scaled-down run of Kernels-BO's main/input_space.ipynb pipeline (kernel grammar ->
expected sqrt-JS distance through QMC over hyperparameters -> classical MDS -> diagnostics),
checked against the shipped 15-D embedding output/kernels_JS.csv.

Same calls as the notebook, but on a random subset of the 237 depth-2 grammar kernels
and with fewer QMC samples per pair (the notebook uses 237 kernels and n_samples=128).
Usage: python -I Kernels-BO-input-space-driver.py <repo_work_dir> <out_dir> [n_kernels] [n_samples]
"""
import json
import sys
import time

repo, out = sys.argv[1], sys.argv[2]
N_K = int(sys.argv[3]) if len(sys.argv) > 3 else 40
N_S = int(sys.argv[4]) if len(sys.argv) > 4 else 32
sys.path.insert(0, repo)

import numpy as np
import pandas as pd
import torch
from kernels.grammar import generate_kernel_set
from kernels.builders import build_module
from distances.expectations import expected_sqrtjs_distance_squared
from embedding.mds import mds_from_squared_distance
from analysis.diagnostics import mds_reconstruction_error, parity_metrics

torch.set_default_dtype(torch.double)
torch.manual_seed(0)
X_ref = torch.linspace(0, 1, 20).unsqueeze(-1)

t0 = time.time()
all_exprs = generate_kernel_set(max_depth=2)
print(f"Generated {len(all_exprs)} kernels (notebook output: 237)")
rng = np.random.default_rng(0)
sel = sorted(rng.choice(len(all_exprs), size=N_K, replace=False).tolist())
exprs = [all_exprs[i] for i in sel]
n = len(exprs)

D = torch.zeros(n, n)
t1 = time.time()
for i in range(n):
    for j in range(i + 1, n):
        ki = lambda: build_module(exprs[i])
        kj = lambda: build_module(exprs[j])
        D[i, j] = D[j, i] = expected_sqrtjs_distance_squared(ki, kj, X_ref, n_samples=N_S)
t_pairs = time.time() - t1
n_pairs = n * (n - 1) // 2
per_sample = t_pairs / (n_pairs * N_S)
full_est_s = per_sample * (len(all_exprs) * (len(all_exprs) - 1) // 2) * 128
print(f"{n_pairs} pairs x {N_S} QMC samples in {t_pairs:.1f} s -> {1e3*per_sample:.2f} ms/sample; "
      f"full notebook run (237 kernels, 128 samples) est. {full_est_s/3600:.2f} h on this core")

k = min(15, n - 1)
X_feat, evals = mds_from_squared_distance(D, k=k)
err, rel = mds_reconstruction_error(D, X_feat)
r2, rmse, mae = parity_metrics(D, X_feat)
print(f"MDS (k={k}) mean abs error {err:.3e} | relative error {rel:.3e} | parity R2/RMSE/MAE {r2:.4f}, {rmse:.4f}, {mae:.4f}")

# Compare with the shipped embedding: squared Euclidean distances between the same kernels
ship = pd.read_csv(f"{repo}/output/kernels_JS.csv")
ship = ship.set_index("kernel")
names = [str(e) for e in exprs]
missing = [s for s in names if s not in ship.index]
cols = [c for c in ship.columns if c.startswith("C")]
Xs = ship.loc[[s for s in names if s in ship.index], cols].to_numpy()
iu = np.triu_indices(len(Xs), 1)
D_ship = ((Xs[:, None, :] - Xs[None, :, :]) ** 2).sum(-1)[iu]
present = [i for i, s in enumerate(names) if s in ship.index]
D_ours = D.numpy()[np.ix_(present, present)][iu]
pear = float(np.corrcoef(D_ours, D_ship)[0, 1])
from scipy.stats import spearmanr
spear = float(spearmanr(D_ours, D_ship).correlation)
print(f"vs shipped kernels_JS.csv: {len(present)}/{n} kernels found; pairwise D Pearson r={pear:.4f}, Spearman={spear:.4f}; "
      f"mean D ours={D_ours.mean():.4f} shipped={D_ship.mean():.4f}")

# Diagnostic: identical-spectrum pairs (distance ~0 although the kernels differ)
zero_pairs = int((D.numpy()[np.triu_indices(n, 1)] < 1e-10).sum())
print(f"pairs with D < 1e-10 (indistinguishable under the spectrum-based JS): {zero_pairs}/{n_pairs}")

res = {"n_kernels_total": len(all_exprs), "n_kernels_used": n, "qmc_samples": N_S, "pairs": n_pairs,
       "pair_time_s": round(t_pairs, 1), "ms_per_sample": round(1e3 * per_sample, 3),
       "full_run_estimate_h": round(full_est_s / 3600, 2), "mds_k": k, "mds_mean_abs_err": err, "mds_rel_err": rel,
       "parity_r2": r2, "parity_rmse": rmse, "parity_mae": mae, "shipped_found": len(present),
       "pearson_vs_shipped": pear, "spearman_vs_shipped": spear, "zero_distance_pairs": zero_pairs,
       "kernels": names}
json.dump(res, open(f"{out}/data/Kernels-BO-input-space.json", "w"), indent=1, default=float)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].scatter(D_ship, D_ours, s=6, alpha=0.5)
ax[0].set_xlabel("squared distance in shipped 15-D embedding")
ax[0].set_ylabel(f"recomputed E[sqrt-JS]^2 ({N_S} QMC samples)")
ax[0].set_title(f"{len(present)} kernels, Spearman {spear:.3f}", fontsize=9)
ev = evals.detach().cpu().numpy() if hasattr(evals, "detach") else np.asarray(evals)
ax[1].bar(np.arange(1, len(ev) + 1), ev)
ax[1].set_xlabel("MDS component")
ax[1].set_ylabel("eigenvalue")
ax[1].set_title("classical MDS spectrum", fontsize=9)
fig.tight_layout()
fig.savefig(f"{out}/figures/Kernels-BO-input-space.png", dpi=110)
print(f"total {time.time()-t0:.1f} s")
