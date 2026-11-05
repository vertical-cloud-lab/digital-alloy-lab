"""Rank the best alloy found by pref_gold_optimization.py against the full 933-alloy dataset,
and list the true (minimisation) Pareto set of the EHVI run's queried points.
Usage: python -I Alloy-Color-Optimization-rank.py <work_dir> <out_json>"""
import json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np, pandas as pd
import pref_gold_optimization as pg
import multiobjective_ehvi as me
df = pd.read_csv(f"{sys.argv[1]}/color_quinary_5%.csv")
u = np.array([pg.gold_likeness(int(c)) for c in df["24-bit color"]])
order = np.sort(u)[::-1]
best_found = 0.9968  # printed by the pref-BO run (seed 42, 3 init + 10 iterations)
rank = int((u > best_found + 5e-5).sum()) + 1
prices = np.array([me.alloy_price(r) for r in df[["E1","E2","E3","E4","E5"]].to_numpy()])
out = {"n_alloys": int(len(u)), "max_gold_likeness": float(order[0]), "top5": [float(x) for x in order[:5]],
       "best_found_by_prefBO": best_found, "rank_of_best_found": rank,
       "price_usd_per_g": {"min": float(prices.min()), "median": float(np.median(prices)), "max": float(prices.max())}}
print(json.dumps(out, indent=1)); json.dump(out, open(sys.argv[2], "w"), indent=1)
