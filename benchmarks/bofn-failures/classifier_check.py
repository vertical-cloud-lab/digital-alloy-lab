"""How fast does each viability model learn the failure region? (writes classifier_check.json/.md)

    python classifier_check.py            # every cell, each in its own process (about 5 minutes)

H5 says a viability model over the failing stage's own inputs (design variables plus the measured
parent outputs) learns the input-caused failure region faster than one over the whole design,
because the region is simple in the stage inputs (crack severity from f and g, energy density from
P, v and f, powder yield q) and curved in the design. This check isolates that claim from the
campaign: for n random designs, draw each one's blocking-stage outcome (input-caused failures only,
the precondition included), fit the same GP-on-0/1 model `policy.ViabGP` on the design x and on the
stage inputs z, and score both on 4,000 held-out designs against the truth's own failure
probability: AUC for "fails with probability above 0.5", and the Brier score of P(viable).
"""

from __future__ import annotations

import json
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
CELLS = [("al", 1.0), ("al", 0.0), ("cu-toy", 1.0), ("cu-phys", 1.0)]
NS = (15, 30, 60, 120)
REPS = 10


def auc(score, label):
    """Area under the ROC curve (Mann-Whitney), label 1 = viable."""
    s, y = np.asarray(score), np.asarray(label).astype(bool)
    if y.all() or (~y).all():
        return float("nan")
    order = np.argsort(s)
    ranks = np.empty(len(s))
    ranks[order] = np.arange(1, len(s) + 1)
    n1, n0 = y.sum(), (~y).sum()
    return float((ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def stage_data(net, fm, truth, X):
    """True blocking-stage inputs z, and P(input-caused failure) including the powder precondition."""
    from failmodel import Q_MIN

    full = truth.full(X)
    BA = net.BA
    if net.family == "al":
        z = torch.stack([X[:, 5], X[:, 6], full["f"], full["g"], full["q"]], -1)  # the rho node's input
        st = "L"
    else:
        z = torch.stack([X[:, 5], X[:, 6], full["f"], full["g"], full["h"], full["q"], full["rho_u"]], -1)  # rho_m's input
        st = "M"
    p = []
    for i in range(X.shape[0]):
        if float(full["q"][i]) < Q_MIN:
            p.append(1.0)
            continue
        zz = dict(P=float(X[i, 5]), v=float(X[i, 6]), f=float(full["f"][i]), g=float(full["g"][i]))
        if net.family == "cu":
            zz["h"] = float(full["h"][i])
        p.append(fm.p_input(st, zz)[0])
    return z, np.array(p)


def one_cell(name, kappa):
    warnings.filterwarnings("ignore")
    torch.set_num_threads(1)
    sys.path.insert(0, str(HERE))
    from failmodel import FailureModel
    from netload import load
    from policy import ViabGP

    net = load(name)
    truth = net.truth(kappa, 1.0)
    fm = FailureModel(net.family, "mixed", 0, kappa, f_crack=getattr(net.BA, "F_CRACK", 0.56), p_cap=getattr(net.BA, "P_CAP", 0.5))
    g = torch.Generator().manual_seed(123)
    Xte = net.feasible(torch.rand(20_000, net.D, generator=g))[:4000]
    zte, pte = stage_data(net, fm, truth, Xte)
    yte = (pte < 0.5).astype(float)
    out = {"cell": f"{name}-k{kappa:g}", "test_viable_share": float(yte.mean()), "rows": []}
    rng = np.random.default_rng(7)
    for n in NS:
        for rep in range(REPS):
            gt = torch.Generator().manual_seed(1000 * n + rep)
            Xtr = net.feasible(torch.rand(4 * n, net.D, generator=gt))[:n]
            ztr, ptr = stage_data(net, fm, truth, Xtr)
            ytr = (rng.random(len(ptr)) >= ptr).astype(float)  # 1 = viable
            row = {"n": n, "rep": rep, "zeros": int((ytr == 0).sum())}
            if ytr.min() == ytr.max():
                row.update(skipped=True)
                out["rows"].append(row)
                continue
            for key, Ztr, Zte in (("x", Xtr, Xte), ("node", ztr, zte)):
                gp = ViabGP(Ztr, torch.tensor(ytr))
                pv = gp.prob(Zte).numpy()
                row[f"auc_{key}"] = auc(pv, yte)
                row[f"brier_{key}"] = float(np.mean((pv - (1 - pte)) ** 2))
            out["rows"].append(row)
    return out


def main():
    if len(sys.argv) > 1:
        print(json.dumps(one_cell(sys.argv[1], float(sys.argv[2]))))
        return
    res = []
    for name, kappa in CELLS:
        r = subprocess.run([sys.executable, __file__, name, str(kappa)], capture_output=True, text=True, check=True)
        res.append(json.loads(r.stdout.strip().splitlines()[-1]))
    (HERE / "classifier_check.json").write_text(json.dumps(res, indent=1) + "\n")
    lines = ["# Viability models: design space vs stage inputs", "",
             "Held-out AUC (viable vs not, at the truth's 0.5 failure probability) and Brier score of P(viable), mean ± SE over 10 replicates of n random designs. Made by `classifier_check.py`.", "",
             "| Cell | n | AUC, over x | AUC, over stage inputs | Brier, over x | Brier, over stage inputs | runs that failed (mean) |", "|---|---|---|---|---|---|---|"]
    for c in res:
        for n in NS:
            rows = [r for r in c["rows"] if r["n"] == n and not r.get("skipped")]
            if not rows:
                continue
            f = lambda k: (np.mean([r[k] for r in rows]), np.std([r[k] for r in rows], ddof=1) / np.sqrt(len(rows)))
            ax, an, bx, bn = f("auc_x"), f("auc_node"), f("brier_x"), f("brier_node")
            lines.append(f"| {c['cell']} | {n} | {ax[0]:.3f} ± {ax[1]:.3f} | {an[0]:.3f} ± {an[1]:.3f} | {bx[0]:.3f} ± {bx[1]:.3f} | {bn[0]:.3f} ± {bn[1]:.3f} | {np.mean([r['zeros'] for r in rows]):.1f} |")
    (HERE / "classifier_check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
