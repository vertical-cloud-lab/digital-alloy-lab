"""Scaled-down, runnable reproduction of ArroyaveLab/Initialization's walkthrough.

The repo's script_for_datasets_and_features.py raises ValueError when run, and it is
written to be read rather than executed. This driver takes only its imports and function
definitions (through ast, so its top-level 1000x loops never run) and then repeats the
workflow the docstrings describe, on the 'htmdec single system' dataset
(System_Type == 4). It compares four ways of choosing a 20-alloy first batch:
  RAND      random sampling
  MED-EL    k-medoids on the element fractions only
  MED-EL+S  k-medoids on the elements plus the Sconf class, the 'additional dimension'
  PERFECT   k-medoids on the (normally unknown) outputs, the 'unrealistic' upper bound
For each batch it computes the script's features: bounding-box area and mean distance to
the centroid in output space. It also records whether the batch contains a Pareto point.

Usage: python -I Initialization-driver.py <repo_dir> <out_dir> [n_rand] [n_med]
"""
import ast
import json
import sys
import time

import numpy as np
import pandas as pd

repo, out = sys.argv[1], sys.argv[2]
N_RAND = int(sys.argv[3]) if len(sys.argv) > 3 else 200
N_MED = int(sys.argv[4]) if len(sys.argv) > 4 else 30
BATCH = 20
rng = np.random.default_rng(0)
np.random.seed(0)

# Pull only the imports and function definitions out of the walkthrough script
src = open(f"{repo}/script_for_datasets_and_features.py").read()
tree = ast.parse(src)
keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
ns = {"__name__": "initialization_walkthrough"}
exec(compile(ast.Module(body=keep, type_ignores=[]), "walkthrough_defs", "exec"), ns)
print("functions loaded:", sorted(k for k, v in ns.items() if callable(v) and getattr(v, "__module__", None) is None or k in
      ["import_data", "add_pareto_as_col_to_df", "pareto_maximum", "assign_clusters", "extract_elements",
       "calculate_medoids_with_clusters", "get_medoids", "calculate_medoids_with_clusters_normalized"]))

# Data prep exactly as the walkthrough describes
outputs = ["PROP RT Density (g/cm3)", "Solidification Range (K)"]
phase_space = ns["import_data"](f"{repo}/Datasets/dataset_htmdec_single_type")
phase_space = phase_space[phase_space["System_Type"] == 4].drop("V", axis=1)
phase_space = ns["add_pareto_as_col_to_df"](data=phase_space, outputs=outputs)
phase_space["Sconf_class"] = pd.cut(phase_space["Sconf"], bins=[-float("inf"), 1.368, float("inf")],
                                    labels=[1, 2], right=True).astype(int)
data_main = phase_space.loc[:, list(phase_space.columns[list(range(0, 5)) + [6, 11]]) + outputs + ["Pareto"] + ["Sconf_class"]]
print("data_main shape:", data_main.shape, "| Pareto points:", int(data_main["Pareto"].sum()),
      "| Sconf_class counts:", data_main["Sconf_class"].value_counts().to_dict())

elements = ns["extract_elements"](phase_space)
ns["elements"] = elements          # global used inside calculate_medoids_with_clusters
ns["batch_size"] = BATCH           # global used inside calculate_medoids_with_clusters_normalized
print("elements:", elements)


def features(sel):
    o = sel[outputs].to_numpy()
    bbox = float(np.ptp(o[:, 0]) * np.ptp(o[:, 1]))
    mean_dist = float(np.mean(np.linalg.norm(o - o.mean(0), axis=1)))
    return {"BoundingBoxArea": bbox, "MeanDistance": mean_dist, "HasPareto": bool(sel["Pareto"].any()),
            "n_selected": int(len(sel))}


rows = []
timing = {}
t0 = time.time()
for i in range(N_RAND):
    idx = np.random.choice(len(data_main), BATCH, replace=False)
    rows.append({"strategy": "RAND", "rep": i, **features(data_main.iloc[idx])})
timing["RAND"] = time.time() - t0

for label, dims in [("MED-EL", elements), ("MED-EL+S", elements + ["Sconf_class"])]:
    t0 = time.time()
    for i in range(N_MED):
        df = ns["calculate_medoids_with_clusters"](data_main, dims, BATCH, int(np.random.randint(0, 1e7)), "k-medoids++")
        rows.append({"strategy": label, "rep": i, **features(df[df["Medoid"]])})
    timing[label] = time.time() - t0
    print(f"{label}: {N_MED} k-medoid batches in {timing[label]:.1f} s", flush=True)

t0 = time.time()
for i in range(N_MED):
    df = ns["get_medoids"](data_main, outputs, BATCH)
    rows.append({"strategy": "PERFECT", "rep": i, **features(df[df["Medoid"]])})
timing["PERFECT"] = time.time() - t0
print(f"PERFECT: {N_MED} output-space k-medoid batches in {timing['PERFECT']:.1f} s", flush=True)

res = pd.DataFrame(rows)
res.to_csv(f"{out}/data/Initialization-batch-features.csv", index=False)
summ = res.groupby("strategy").agg(n=("rep", "size"), bbox_median=("BoundingBoxArea", "median"),
                                   bbox_mean=("BoundingBoxArea", "mean"), meandist_median=("MeanDistance", "median"),
                                   frac_with_pareto=("HasPareto", "mean"), n_selected_mean=("n_selected", "mean"))
summ = summ.reindex(["RAND", "MED-EL", "MED-EL+S", "PERFECT"])
print(summ.to_string())
summ.to_csv(f"{out}/data/Initialization-summary.csv")
json.dump({"timing_s": timing, "N_RAND": N_RAND, "N_MED": N_MED, "batch": BATCH,
           "n_candidates": int(len(data_main))}, open(f"{out}/data/Initialization-run.json", "w"), indent=1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
colors = {"RAND": "#4C72B0", "MED-EL": "#DD8452", "MED-EL+S": "#55A868", "PERFECT": "#C44E52"}
for s, c in colors.items():
    v = np.sort(res.loc[res.strategy == s, "BoundingBoxArea"].to_numpy())
    ax[0].plot(v, np.arange(1, len(v) + 1) / len(v), color=c, lw=2, label=f"{s} (n={len(v)})")
    w = np.sort(res.loc[res.strategy == s, "MeanDistance"].to_numpy())
    ax[1].plot(w, np.arange(1, len(w) + 1) / len(w), color=c, lw=2, label=s)
ax[0].set_xlabel("bounding-box area of 20-pt batch in output space\n(density g/cm3 x solidification range K)")
ax[1].set_xlabel("mean distance to batch centroid (raw output units)")
for a in ax:
    a.set_ylabel("CDF over repeated batches")
    a.grid(alpha=0.3)
ax[0].legend(fontsize=8)
fig.suptitle("Initialization: spread of first batches, HTMDEC single system (System_Type 4, 3842 alloys)", fontsize=10)
fig.tight_layout()
fig.savefig(f"{out}/figures/Initialization-batch-spread-cdf.png", dpi=110)
print("done")
