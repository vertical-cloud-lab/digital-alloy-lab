"""Where the copper needle is: composition or process? (compare/needle.json)

For each truth: (1) at the optimum's composition, the share of random (a, P, v) settings within 60% of
the optimum; (2) at the optimum's settings, the share of random compositions; (3) the share of random
compositions whose best settings (over 2,048) reach 60%; and for copper the share of random designs whose
deposit is dense enough to pass immersion if the composition allowed it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from landscape import CU, al, cu  # noqa: E402

torch.set_default_dtype(torch.double)


def main():
    g = torch.Generator().manual_seed(7)
    opt_a = json.loads((HERE / "al_optimum.json").read_text())["kappa1"]
    tt = json.loads((CU / "truth_tables.json").read_text())
    r11 = next(r for r in tt if (r["kappa"], r["eta"]) == (1.0, 1.0))
    opt_c, x_c = r11["optimum"], torch.tensor(r11["x_opt"])
    ta, tc = al.AlloyTruth(1.0), cu.AlloyTruth(1.0, 1.0)
    # aluminum optimum (bofn-prelim README): Zn+Mg 0.65, Cu 0.60, Zr 1.00, Sc 0, a 0.47, P 0.23, v 0
    x_a = torch.tensor([0.65, 0.60, 1.00, 0.0, 0.47, 0.23, 0.0])
    out = {}
    for name, t, x0, opt in (("aluminum (kappa = 1)", ta, x_a, opt_a), ("copper (1, 1)", tc, x_c, opt_c)):
        n = 200_000
        apv = torch.rand(n, 3, generator=g)
        comp = torch.rand(n, 4, generator=g)
        y_proc = t.objective(torch.cat([x0[:4].expand(n, 4), apv], -1)) / opt  # optimum composition, random settings
        y_comp = t.objective(torch.cat([comp, x0[4:].expand(n, 3)], -1)) / opt  # random composition, optimum settings
        grid = torch.quasirandom.SobolEngine(3, scramble=True, seed=5).draw(2048).double()
        best = []
        for c in comp[:3000]:
            best.append(float(t.objective(torch.cat([c.expand(grid.shape[0], 4), grid], -1)).max() / opt))
        best = torch.tensor(best)
        out[name] = {"value_at_optimum_check": float(t.objective(x0.unsqueeze(0))[0] / opt),
                     "optimum composition, random settings: share >= 60%": float((y_proc >= 0.6).double().mean()),
                     "optimum composition, random settings: share > 0": float((y_proc > 0).double().mean()),
                     "random composition, optimum settings: share >= 60%": float((y_comp >= 0.6).double().mean()),
                     "random composition, its best of 2,048 settings: share >= 60%": float((best >= 0.6).double().mean()),
                     "random composition, its best of 2,048 settings: share > 0": float((best > 0).double().mean())}
    # copper: is it the composition or the deposit that fails immersion?
    X = torch.rand(400_000, cu.D, generator=g)
    o = tc.full(X)
    m_dense = (o["m"] + 0.30 * (1 - o["rho_m"])).clamp(0, 1)  # the same build had it deposited fully dense (beta unchanged)
    out["copper (1, 1)"]["random designs passing immersion"] = float((o["m"] >= tc.m_ref).double().mean())
    out["copper (1, 1)"]["random designs that would pass if deposited fully dense"] = float((m_dense >= tc.m_ref).double().mean())
    out["copper (1, 1)"]["random designs with rho_m >= 0.9"] = float((o["rho_m"] >= 0.9).double().mean())
    out["copper (1, 1)"]["immersion index lost per 0.1 of rho_m (gate scale 0.05)"] = 0.03
    (HERE / "needle.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
