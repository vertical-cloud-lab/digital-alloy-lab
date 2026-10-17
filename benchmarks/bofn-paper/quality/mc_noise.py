"""Is S_ACQ = 64 enough? Monte-Carlo noise check of the pKGFN decision.

Runs pKGFN normally (one seed, one kappa) but, at chosen iterations, re-scores
the very same candidate sets with (a) five other common-random-number draws at
the production S, to get the MC standard error of every KG estimate, and (b)
S = DIAG_SHI (default 1024) as a near-exact reference. It reports whether the
stage and candidate chosen at the production S are the ones the reference would
choose, and how the KG-per-dollar gap between the best and second-best stage
compares with the MC error. It also counts GP-fit failures (bofn_alloy swallows
them) and summarizes the fitted lengthscales.

    DIAG_ITS=4,12,24,40 BOFN_NO_REC=1 python quality/mc_noise.py <seed> <kappa> <out.json>
"""
import json
import os
import sys
import time
import warnings

import torch

warnings.filterwarnings("ignore")
torch.set_num_threads(1)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import bofn_alloy as BA  # noqa: E402
from bofn_alloy import COSTS, Network, TinyGP  # noqa: E402
import policies as PO  # noqa: E402

DIAG_ITS = {int(v) for v in os.environ.get("DIAG_ITS", "4,12,24,40").split(",")}
S_HI = int(os.environ.get("DIAG_SHI", 1024))
REPS = int(os.environ.get("DIAG_REPS", 5))

# ---- GP fitting: count failures and record lengthscales
fit_stats = {"calls": 0, "failures": 0, "errors": {}, "lengthscales": []}
_orig_fit = BA.fit_gpytorch_mll


def counting_fit(mll):
    fit_stats["calls"] += 1
    try:
        return _orig_fit(mll)
    except Exception as e:  # noqa: BLE001
        fit_stats["failures"] += 1
        fit_stats["errors"][type(e).__name__] = fit_stats["errors"].get(type(e).__name__, 0) + 1
        raise


BA.fit_gpytorch_mll = counting_fit
_orig_gp_init = TinyGP.__init__


def recording_gp_init(self, X, y, noise=1e-6, **kw):
    _orig_gp_init(self, X, y, noise, **kw)
    fit_stats["lengthscales"].append({"n": int(X.shape[0]), "d": int(X.shape[1]), "ls": [round(float(v), 4) for v in self.ls], "ys": round(float(self.ys), 4)})


TinyGP.__init__ = recording_gp_init

# ---- KG: re-score the same candidates with other base samples and with many more
state = {"it": 0, "cur": None, "diag": [], "t_extra": 0.0}
_orig_kg = Network.kg


def kg_wrapper(self, group, Z, Xi, eps, w, ww, chunk=4):
    val = _orig_kg(self, group, Z, Xi, eps, w, ww, chunk)
    if group == "C":  # first group scored in every iteration
        state["it"] += 1
        state["cur"] = {"it": state["it"], "groups": {}}
        if state["it"] in DIAG_ITS:
            state["diag"].append(state["cur"])
    if state["it"] in DIAG_ITS:
        t0 = time.time()
        m, S = Xi.shape[0], eps["s"].shape[-1]
        reps = torch.stack([_orig_kg(self, group, Z, Xi, PO.eps_for(m, S, 900_000 + 1000 * state["it"] + r), w, ww, chunk).clamp_min(0) for r in range(REPS)])
        hi = _orig_kg(self, group, Z, Xi, PO.eps_for(m, S_HI, 800_000 + state["it"]), w, ww, chunk).clamp_min(0)
        state["cur"]["groups"][group] = {
            "cost": COSTS[group], "b": int(Z.shape[0]), "m": int(m), "S": int(S), "S_hi": S_HI,
            "kg": val.clamp_min(0).tolist(), "kg_reps_mean": reps.mean(0).tolist(), "kg_reps_std": reps.std(0).tolist(), "kg_hi": hi.tolist(),
        }
        state["t_extra"] += time.time() - t0
    return val


Network.kg = kg_wrapper


def decisions(groups):
    """(stage, candidate, ratio) chosen by each estimator, and the stage ranking."""
    out = {}
    for est in ("kg", "kg_hi", "kg_reps_mean"):
        ranked = []
        for g, v in groups.items():
            kg = torch.tensor(v[est])
            j = int(kg.argmax())
            ranked.append((float(kg[j]) / v["cost"], g, j))
        ranked.sort(reverse=True)
        out[est] = {"stage": ranked[0][1], "cand": ranked[0][2], "ratio": ranked[0][0], "ranking": [(g, round(r, 9)) for r, g, _ in ranked]}
    return out


def main():
    seed, kappa, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    t0 = time.time()
    res = PO.run("pkgfn", kappa, seed, 100_000)
    wall = time.time() - t0
    report = {"seed": seed, "kappa": kappa, "S_ACQ": PO.S_ACQ, "N_CAND": PO.N_CAND, "S_hi": S_HI, "reps": REPS,
              "wall_s": wall, "wall_s_diagnostics": state["t_extra"], "final_best_validated": max(r["best_validated"] for r in res["rows"]),
              "fit_calls": fit_stats["calls"], "fit_failures": fit_stats["failures"], "fit_errors": fit_stats["errors"], "iterations": []}
    ls_all = torch.tensor([v for rec in fit_stats["lengthscales"] for v in rec["ls"]])
    report["lengthscales"] = {"n_fits": len(fit_stats["lengthscales"]), "min": float(ls_all.min()), "median": float(ls_all.median()), "max": float(ls_all.max()),
                              "frac_at_lower_bound_0.025": float((ls_all <= 0.0251).float().mean()), "frac_above_10": float((ls_all > 10).float().mean()),
                              "frac_below_0.1": float((ls_all < 0.1).float().mean())}
    for d in state["diag"]:
        dec = decisions(d["groups"])
        best = dec["kg"]
        g, j = best["stage"], best["cand"]
        v = d["groups"][g]
        std_ratio = v["kg_reps_std"][j] / v["cost"]
        gap = best["ranking"][0][1] - (best["ranking"][1][1] if len(best["ranking"]) > 1 else 0.0)
        # how the chosen candidate's KG at S=64 compares with the reference
        rel_err = {gg: (torch.tensor(vv["kg"]) - torch.tensor(vv["kg_hi"])).abs().mean().item() / max(torch.tensor(vv["kg_hi"]).abs().mean().item(), 1e-12) for gg, vv in d["groups"].items()}
        report["iterations"].append({
            "it": d["it"], "chosen_S": (g, j), "chosen_S_hi": (dec["kg_hi"]["stage"], dec["kg_hi"]["cand"]), "same_stage": g == dec["kg_hi"]["stage"], "same_candidate": (g, j) == (dec["kg_hi"]["stage"], dec["kg_hi"]["cand"]),
            "ratio_S": best["ratio"], "ratio_S_hi_of_same": v["kg_hi"][j] / v["cost"], "mc_std_of_chosen_ratio": std_ratio,
            "stage_gap_over_mc_std": gap / std_ratio if std_ratio > 0 else float("inf"), "stage_ranking_S": best["ranking"], "stage_ranking_S_hi": dec["kg_hi"]["ranking"],
            "mean_rel_err_vs_hi_by_stage": rel_err, "candidates_per_stage": {gg: vv["b"] for gg, vv in d["groups"].items()}, "inner_set_m": next(iter(d["groups"].values()))["m"],
        })
    json.dump(report, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "iterations"}, indent=1))
    for it in report["iterations"]:
        print(f"it {it['it']:3d}: chose {it['chosen_S']} at S={PO.S_ACQ}; S={S_HI} would choose {it['chosen_S_hi']} (same stage {it['same_stage']}, same candidate {it['same_candidate']}); "
              f"KG/$ {it['ratio_S']:.3e} (ref {it['ratio_S_hi_of_same']:.3e}), MC std {it['mc_std_of_chosen_ratio']:.3e}, stage gap / MC std = {it['stage_gap_over_mc_std']:.1f}")


if __name__ == "__main__":
    main()
