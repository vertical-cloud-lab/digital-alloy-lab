"""Where the failure regions sit relative to each network's optimum (writes optima.json).

    python calibrate.py al 1.0        # one cell
    python calibrate.py all           # every cell the sweep uses (each in its own process)

For each cell: the true optimum (random search plus local refinement, as in the source
benchmarks), the share of random designs whose stages would fail because of their inputs, and
the best design that no stage rejects ("viable optimum"), which is the most a campaign can
demonstrate once failures exist.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
CELLS = [("al", 1.0, 1.0), ("al", 0.0, 1.0), ("cu-toy", 1.0, 1.0), ("cu-phys", 1.0, 1.0)]


def stage_risks(net, fm, truth, X):
    """Per-design P(input-caused failure) at each failure-prone stage, and q, for designs X [n, D]."""
    full = truth.full(X)
    out = {"q": full["q"].numpy()}
    n = X.shape[0]
    if net.family == "al":
        P, v = X[:, 5].numpy(), X[:, 6].numpy()
        f, g = full["f"].numpy(), full["g"].numpy()
        out["L"] = np.array([fm.p_input("L", dict(P=P[i], v=v[i], f=f[i], g=g[i]))[0] for i in range(n)])
    else:
        P, v = X[:, 5].numpy(), X[:, 6].numpy()
        f, g, h = full["f"].numpy(), full["g"].numpy(), full["h"].numpy()
        for st in ("U", "M"):
            out[st] = np.array([fm.p_input(st, dict(P=P[i], v=v[i], f=f[i], g=g[i], h=h[i]))[0] for i in range(n)])
    return out


def viable_mask(net, risks, thr=0.5):
    from failmodel import Q_MIN

    ok = risks["q"] >= Q_MIN
    for st in ("L", "U", "M"):
        if st in risks:
            ok &= risks[st] < thr
    return ok


def one_cell(name, kappa, eta):
    sys.path.insert(0, str(HERE))
    from failmodel import FailureModel, Q_MIN
    from netload import load

    net = load(name)
    truth = net.truth(kappa, eta)
    fm = FailureModel(net.family, "mixed", 0, kappa, f_crack=getattr(net.BA, "F_CRACK", 0.56), p_cap=getattr(net.BA, "P_CAP", 0.5))
    g = torch.Generator().manual_seed(0)
    X = net.feasible(torch.rand(200_000, net.D, generator=g))
    J = truth.objective(X)
    risks = stage_risks(net, fm, truth, X)
    ok = viable_mask(net, risks)

    def refine(X0, mask_fn=None, iters=400, scale=0.02, seed=1):
        gen = torch.Generator().manual_seed(seed)
        best = X0.clone()
        bJ = truth.objective(best)
        for it in range(iters):
            s = scale * (0.995**it)
            Y = (best + s * torch.randn(best.shape, generator=gen)).clamp(0, 1)
            if net.family == "cu" and net.BA.FEASIBLE is not None:
                keep = net.BA.FEASIBLE(Y)
            else:
                keep = torch.ones(Y.shape[0], dtype=torch.bool)
            JY = truth.objective(Y)
            if mask_fn is not None:
                keep &= torch.as_tensor(mask_fn(Y))
            better = keep & (JY > bJ)
            best[better], bJ[better] = Y[better], JY[better]
        return best, bJ

    top = J.topk(20).indices
    Xo, Jo = refine(X[top])
    jo = int(Jo.argmax())
    x_opt, J_opt = Xo[jo], float(Jo[jo])

    def vmask(Y):
        r = stage_risks(net, fm, truth, Y)
        return viable_mask(net, r)

    Jv = J.clone()
    Jv[~torch.as_tensor(ok)] = -9
    topv = Jv.topk(20).indices
    Xv, Jvv = refine(X[topv], mask_fn=vmask, iters=300)
    jv = int(Jvv.argmax())
    x_v, J_v = Xv[jv], float(Jvv[jv])
    r_opt = stage_risks(net, fm, truth, x_opt.unsqueeze(0))
    near = X[(J >= 0.6 * J_opt)]
    r_near = stage_risks(net, fm, truth, near)
    res = {
        "cell": f"{name} kappa={kappa:g} eta={eta:g}",
        "J_opt": J_opt,
        "x_opt": [round(float(v), 4) for v in x_opt],
        "risk_at_opt": {k: round(float(v[0]), 4) for k, v in r_opt.items()},
        "J_viable_opt": J_v,
        "viable_opt_pct": 100 * J_v / J_opt,
        "x_viable_opt": [round(float(v), 4) for v in x_v],
        "share_random_q_below_min": float((risks["q"] < Q_MIN).mean()),
        "share_random_input_fail": {k: float((risks[k] >= 0.5).mean()) for k in risks if k != "q"},
        "share_random_viable": float(ok.mean()),
        "n_random_within_60pct": int(near.shape[0]),
        "share_within_60pct_viable": float(viable_mask(net, r_near).mean()) if near.shape[0] else None,
        "share_within_60pct_input_fail": {k: float((r_near[k] >= 0.5).mean()) for k in r_near if k != "q"},
    }
    return res


def main():
    if sys.argv[1] == "all":
        out = {}
        for name, kappa, eta in CELLS:
            r = subprocess.run([sys.executable, __file__, name, str(kappa), str(eta)], capture_output=True, text=True, check=True)
            res = json.loads(r.stdout.strip().splitlines()[-1])
            out[res["cell"]] = res
            print(json.dumps(res, indent=1), flush=True)
        (HERE / "optima.json").write_text(json.dumps(out, indent=1) + "\n")
        return
    name, kappa = sys.argv[1], float(sys.argv[2])
    eta = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    print(json.dumps(one_cell(name, kappa, eta)))


if __name__ == "__main__":
    main()
