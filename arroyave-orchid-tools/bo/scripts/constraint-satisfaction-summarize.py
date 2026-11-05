"""Summarize the scaled-down constraint-satisfaction campaigns (2 seeds x 20 iterations per method).
Usage: python constraint-satisfaction-summarize.py <work_dir> <out_csv> <out_png>"""
import sys, glob, os
import pandas as pd
import matplotlib.pyplot as plt

work, out_csv, out_png = sys.argv[1:4]
methods = ["campaign_const_w_priors", "campaign_const_NO_priors", "campaign_pehvi", "campaign_ehvi_pof", "campaign_random"]
rows, curves = [], {}
for m in methods:
    dfs = [pd.read_csv(f) for f in sorted(glob.glob(os.path.join(work, f"results_{m}", "campaign_*.csv")))]
    if not dfs:
        continue
    for k, d in enumerate(dfs):
        last = d.iloc[-1]
        rows.append(dict(method=m.replace("campaign_", ""), seed=k + 1, iterations=len(d),
                         hv_scaled_fixed_final=last["Hypervolume_Scaled_FixedRange"],
                         n_measured_bcc_single=int(d["MeasuredObjectives_BCCSingle"].sum()),
                         n_true_feasible_found=int(last["TrueMeasPass_All_With_BCC"]),  # cumulative column; 24 truly feasible points exist in the 40,553-point pool
                         final_F1=last["F1"], final_brier=last["BrierLoss"]))
    cat = pd.concat(dfs)
    curves[m] = cat.groupby("Iteration")["Hypervolume_Scaled_FixedRange"].agg(["mean", "std"])
res = pd.DataFrame(rows)
res.to_csv(out_csv, index=False)
print(res.to_string(index=False))
print(res.groupby("method")[["hv_scaled_fixed_final", "n_true_feasible_found", "final_F1"]].mean().to_string())
fig, ax = plt.subplots(figsize=(6, 4))
for m, c in curves.items():
    ax.plot(c.index, c["mean"], label=m.replace("campaign_", ""))
    ax.fill_between(c.index, c["mean"] - c["std"].fillna(0), c["mean"] + c["std"].fillna(0), alpha=0.15)
ax.set_xlabel("iteration"); ax.set_ylabel("hypervolume (scaled, fixed range)")
ax.set_title("constraint-satisfaction: 2 seeds x 20 iters (scaled down)")
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(out_png, dpi=110)
