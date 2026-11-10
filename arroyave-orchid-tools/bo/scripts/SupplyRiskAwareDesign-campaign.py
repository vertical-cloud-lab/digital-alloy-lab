"""Small supply-risk-aware batch MOBO campaign on Mo-Nb-Ti-V-W using the repo's own models (sradd).

Ground truth = the repo's analytical models (Curtin-Maresca YS at 1300 C, Pugh ratio from weighted elastic constants,
weighted supply-risk index), evaluated on a 5 at.% grid (each element >= 5 at.%), filtered by the repo's
rule-of-mixtures melting-point constraint. Two scenarios as in the paper: objectives with SR (YS max, Pugh max, SR min)
and without SR (YS max, Pugh max). Scaled down: 10 initial alloys, 4 batches of 5, n_gp=10, num_random_points=400.
usage: python SupplyRiskAwareDesign-campaign.py <out_dir> [seed]
"""
import itertools, json, sys, time
from pathlib import Path
import numpy as np, pandas as pd
from sradd import data as D
from sradd.properties import curtin_maresca_yield_strength, weighted_elastic_summary
from sradd.constraints.rule_of_mixtures import melting_point_from_elemental_properties, passes_melting_point_constraint
from sradd.supply_risk import alloy_supply_risk_index
from sradd.mobbo import suggest_batch, Pareto_finder, HV_Calc

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
EL = ["Mo", "Nb", "Ti", "V", "W"]
ec, vol, props, sr = D.load_elastic_constants(), D.load_bcc_volumes(), D.load_elemental_properties(), D.load_supply_risk_scores()
grid = [np.array(c) / 20 for c in itertools.product(range(1, 17), repeat=4) if 1 <= 20 - sum(c)]
grid = np.array([np.append(g, 1 - g.sum()) for g in grid])
t0 = time.time(); rows = []
for x in grid:
    comp = dict(zip(EL, x))
    tm = melting_point_from_elemental_properties(comp, props)
    rows.append([curtin_maresca_yield_strength(comp, ec, vol).yield_strength_mpa,
                 weighted_elastic_summary(comp, ec)["pugh_ratio"], alloy_supply_risk_index(comp, sr), tm,
                 passes_melting_point_constraint(tm)])
truth = pd.DataFrame(rows, columns=["YS_MPa", "Pugh", "SR", "Tm_K", "feasible"]); truth[EL] = grid
print(f"grid {len(grid)} alloys, {int(truth.feasible.sum())} pass Tm constraint; truth eval {time.time()-t0:.1f}s")
truth.to_csv(out / "truth_grid.csv", index=False)
feas = truth[truth.feasible].reset_index(drop=True); X = feas[EL].to_numpy()
summary = {"grid": len(grid), "feasible": len(feas), "seed": seed}
for scen, cols, goal, ref in [("with_SR", ["YS_MPa", "Pugh", "SR"], [1, 1, 0], [0.0, 0.0, 70.0]),
                              ("without_SR", ["YS_MPa", "Pugh"], [1, 1], [0.0, 0.0])]:
    goal = np.array([goal]); ref_min = np.array([ref])
    Y = feas[cols].to_numpy()
    rng = np.random.default_rng(seed); idx = list(rng.choice(len(X), 10, replace=False))
    hv_true = float(HV_Calc(goal, ref_min, Pareto_finder(Y, goal)[0]).reshape(-1)[0])
    hist = []
    for it in range(5):
        pf, pidx = Pareto_finder(Y[idx], goal)
        hv = float(HV_Calc(goal, ref_min, pf).reshape(-1)[0])
        sel = np.array(idx)[pidx]
        hist.append({"iteration": it, "n_eval": len(idx), "hv": hv, "hv_frac": hv / hv_true,
                     "pareto_mean_SR": float(feas.SR.iloc[sel].mean()), "pareto_min_SR": float(feas.SR.iloc[sel].min()),
                     "best_YS": float(feas.YS_MPa.iloc[idx].max())})
        print(scen, hist[-1], flush=True)
        if it == 4: break
        t1 = time.time()
        s = suggest_batch(X[idx], Y[idx], X, goal, ref_min, batch_size=5, n_gp=10, num_random_points=400, random_state=seed + it)
        for b in s.selected_batch:
            j = int(np.argmin(np.abs(X - b).sum(1)))
            if j not in idx: idx.append(j)
        print(f"  suggest_batch {time.time()-t1:.1f}s", flush=True)
    pd.DataFrame(hist).to_csv(out / f"history_{scen}.csv", index=False)
    feas.iloc[idx].assign(order=range(len(idx))).to_csv(out / f"evaluated_{scen}.csv", index=False)
    summary[scen] = {"true_hv": hv_true, **hist[-1]}
json.dump(summary, open(out / "summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
