"""Is S_ACQ = 32 enough? Monte-Carlo noise check of the pKGFN decision (copper/DED network).

Runs pKGFN normally (one seed, one cell) but, at chosen iterations, re-scores the very same
candidate sets with (a) five other common-random-number draws at the production S, to get the MC
standard error of every KG estimate, and (b) S = DIAG_SHI (default 1024) as a near-exact
reference. It reports whether the stage (or test bundle) and candidate chosen at the production S
are the ones the reference would choose, and how the KG-per-dollar gap between the best and
second-best stage compares with the MC error. It also summarizes the fitted lengthscales.

    DIAG_ITS=4,12,24,40 python quality/mc_noise.py <seed> <kappa> <eta> <out.json>
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
import policies as PO  # noqa: E402
from bofn_alloy import TinyGP  # noqa: E402

DIAG_ITS = {int(v) for v in os.environ.get("DIAG_ITS", "4,12,24,40").split(",")}
S_HI = int(os.environ.get("DIAG_SHI", 1024))
REPS = int(os.environ.get("DIAG_REPS", 5))

lengthscales = []
_orig_gp_init = TinyGP.__init__


def recording_gp_init(self, X, y, noise=1e-6):
    _orig_gp_init(self, X, y, noise)
    lengthscales.append([float(v) for v in self.ls])


TinyGP.__init__ = recording_gp_init
state = {"diag": {}, "t_extra": 0.0}


def hook(it, grp, net, kg_grp, Z, Xi, eps, w, ww, cv, kg):
    if it not in DIAG_ITS:
        return
    t0 = time.time()
    m, S = Xi.shape[0], eps["s"].shape[-1]
    reps = torch.stack([net.kg(kg_grp, Z, Xi, PO.eps_for(m, S, 900_000 + 1000 * it + r), w, ww).clamp_min(0) for r in range(REPS)])
    hi = net.kg(kg_grp, Z, Xi, PO.eps_for(m, S_HI, 800_000 + it), w, ww).clamp_min(0)
    state["diag"].setdefault(it, {})[grp] = {"cost": cv.tolist(), "b": int(Z.shape[0]), "m": int(m), "S": int(S), "kg": kg.tolist(),
                                             "kg_reps_mean": reps.mean(0).tolist(), "kg_reps_std": reps.std(0).tolist(), "kg_hi": hi.tolist()}
    state["t_extra"] += time.time() - t0


PO.KG_HOOK = hook


def decisions(groups):
    """(stage, candidate, ratio) chosen by each estimator, and the stage ranking."""
    out = {}
    for est in ("kg", "kg_hi", "kg_reps_mean"):
        ranked = []
        for g, v in groups.items():
            r = torch.tensor(v[est]) / torch.tensor(v["cost"])
            j = int(r.argmax())
            ranked.append((float(r[j]), g, j))
        ranked.sort(reverse=True)
        out[est] = {"stage": ranked[0][1], "cand": ranked[0][2], "ratio": ranked[0][0], "ranking": [(g, r) for r, g, _ in ranked]}
    return out


def main():
    seed, kappa, eta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    t0 = time.time()
    res = PO.run("pkgfn", kappa, eta, seed, 100_000)
    ls_all = torch.tensor([v for rec in lengthscales for v in rec])
    report = {"seed": seed, "kappa": kappa, "eta": eta, "S_ACQ": PO.S_ACQ, "N_CAND": PO.N_CAND, "S_hi": S_HI, "reps": REPS, "wall_s": time.time() - t0,
              "wall_s_diagnostics": state["t_extra"], "final_best_validated": max(r["best_validated"] for r in res["rows"]), "gp_fits": res["gp_fits"],
              "lengthscales": {"n_fits": len(lengthscales), "min": float(ls_all.min()), "median": float(ls_all.median()), "max": float(ls_all.max()),
                               "frac_at_lower_bound_0.025": float((ls_all <= 0.0251).double().mean()), "frac_above_10": float((ls_all > 10).double().mean())},
              "chosen_at_iteration": {r_: row["action"] for r_, row in enumerate(res["rows"]) if r_ in DIAG_ITS}, "iterations": []}
    for it, groups in sorted(state["diag"].items()):
        dec = decisions(groups)
        best = dec["kg"]
        g, j = best["stage"], best["cand"]
        v = groups[g]
        std_ratio = v["kg_reps_std"][j] / v["cost"][j]
        gap = best["ranking"][0][1] - (best["ranking"][1][1] if len(best["ranking"]) > 1 else 0.0)
        rel_err = {gg: (torch.tensor(vv["kg"]) - torch.tensor(vv["kg_hi"])).abs().mean().item() / max(torch.tensor(vv["kg_hi"]).abs().mean().item(), 1e-12) for gg, vv in groups.items()}
        report["iterations"].append({
            "it": it, "chosen_S": (g, j), "chosen_S_hi": (dec["kg_hi"]["stage"], dec["kg_hi"]["cand"]), "same_stage": g == dec["kg_hi"]["stage"],
            "same_candidate": (g, j) == (dec["kg_hi"]["stage"], dec["kg_hi"]["cand"]), "ratio_S": best["ratio"], "ratio_S_hi_of_same": v["kg_hi"][j] / v["cost"][j],
            "mc_std_of_chosen_ratio": std_ratio, "stage_gap_over_mc_std": gap / std_ratio if std_ratio > 0 else float("inf"), "stage_ranking_S": best["ranking"],
            "stage_ranking_S_hi": dec["kg_hi"]["ranking"], "mean_rel_err_vs_hi_by_stage": rel_err, "kg_flat_at_S": best["ratio"] < 1e-10,
        })
    json.dump(report, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "iterations"}, indent=1))
    for it in report["iterations"]:
        print(f"it {it['it']:3d}: chose {it['chosen_S']} at S={PO.S_ACQ}; S={S_HI} would choose {it['chosen_S_hi']} (same stage {it['same_stage']}, same candidate {it['same_candidate']}); "
              f"KG/$ {it['ratio_S']:.3e} (ref {it['ratio_S_hi_of_same']:.3e}), MC std {it['mc_std_of_chosen_ratio']:.3e}, stage gap / MC std = {it['stage_gap_over_mc_std']:.1f}")


if __name__ == "__main__":
    main()
