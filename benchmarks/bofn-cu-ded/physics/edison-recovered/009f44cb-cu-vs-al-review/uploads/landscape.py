"""Why the copper results differ from the aluminum ones: the two truths side by side.

    python compare/landscape.py            # writes compare/landscape.json and prints a summary
    python compare/landscape.py --maps     # compare/compare_landscape_maps.png: composition slices through each optimum

For each truth (aluminum `../bofn-prelim` at kappa = 1; copper at (kappa, eta) = (1, 1), with and
without the immersion gate) it samples uniform random designs and reports how much of the design
space is good, what the seed data and a random search should reach, and how the copper truth's
dense, crack-free index splits into its factors.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent
CU = HERE.parent
AL = CU.parent / "bofn-prelim"
N = 1_000_000


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


al = load(AL / "bofn_alloy.py", "al_alloy")
cu = load(CU / "bofn_alloy.py", "cu_alloy")
torch.set_default_dtype(torch.double)


def refine(f, x0, g, D, rounds=3):
    """Multi-start local search: perturbations at four scales around each start, repeated `rounds` times."""
    best_x, best_y = None, -1e9
    for x in x0:
        xb, yb = x, float(f(x.unsqueeze(0))[0])
        for _ in range(rounds):
            for scale in (0.03, 0.01, 0.003, 0.001):
                P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
                yp = f(P)
                if float(yp.max()) > yb:
                    xb, yb = P[yp.argmax()], float(yp.max())
        if yb > best_y:
            best_x, best_y = xb, yb
    return best_x, best_y


def best_of(y, n, reps=20000, g=None):
    """Expected best of n uniform random designs (as a fraction of the values in y)."""
    idx = torch.randint(0, y.shape[0], (reps, n), generator=g)
    return float(y[idx].max(1).values.mean())


def summary(name, f, D, opt, g, extra=None):
    X = torch.rand(N, D, generator=g)
    y = f(X) / opt
    q = torch.tensor([0.5, 0.9, 0.99, 0.999])
    out = {"truth": name, "optimum": opt, "mean_pct": float(y.mean()), "quantiles_pct": dict(zip(["50%", "90%", "99%", "99.9%"], [float(v) for v in y.quantile(q)])),
           "share_above": {f"{t:.0%}": float((y >= t).double().mean()) for t in (0.0, 0.5, 0.6, 0.7, 0.8, 0.9)},
           "expected_best_of": {str(n): best_of(y, n, g=g) for n in (5, 10, 21, 24, 26, 29)}}
    if extra:
        out.update(extra(X))
    return out


def main():
    g = torch.Generator().manual_seed(0)
    res = []
    # aluminum, kappa = 1 (the bofn-prelim headline), normalized by bofn-prelim's own optimum (analyze.optimum)
    ta = al.AlloyTruth(1.0)
    fa = lambda X: ta.objective(X)
    opt_a = json.loads((HERE / "al_optimum.json").read_text())["kappa1"]
    res.append(summary("aluminum LPBF (kappa = 1)", fa, al.D, opt_a, g))
    # copper, (1, 1), as benchmarked, normalized by truth_tables.json (check_truth.py), as in analyze.py
    tc = cu.AlloyTruth(1.0, 1.0)
    fc = lambda X: tc.objective(X)
    opt_c = next(r["optimum"] for r in json.loads((CU / "truth_tables.json").read_text()) if (r["kappa"], r["eta"]) == (1.0, 1.0))

    def cu_extra(X):
        o = tc.full(X)
        passes = o["m"] >= tc.m_ref
        return {"share_passing_immersion": float(passes.double().mean()), "share_dense_rho_m_0.7": float((o["rho_m"] >= 0.7).double().mean()),
                "share_passing_immersion_given_Ni_below_0.2": float(passes[X[:, 0] < 0.2].double().mean()),
                "share_with_J_above_zero": float((tc.objective(X, o) > 0).double().mean())}

    res.append(summary("copper DED (1, 1), immersion-gated objective", fc, cu.D, opt_c, g, cu_extra))
    # copper without the immersion gate: J = U - 0.3 B (same network, same costs)
    fn = lambda X: (lambda o: o["U"] - cu.LAMBDA * cu.burden(X))(tc.full(X))
    X = torch.rand(400_000, cu.D, generator=g)
    xn, opt_n = refine(fn, X[fn(X).topk(50).indices], g, cu.D)
    r = summary("copper DED (1, 1), no immersion gate (J = U - 0.3 B)", fn, cu.D, opt_n, g)
    r["x_opt"] = [round(v, 3) for v in xn.tolist()]
    r["gated_J_at_nogate_optimum_pct"] = float(fc(xn.unsqueeze(0))[0] / opt_c)
    res.append(r)
    # the seed data each benchmark starts from (5 random designs per seed, generator 2000 + seed)
    seeds = {}
    for nm, mod, t in (("aluminum", al, ta), ("copper", cu, tc)):
        vals = []
        for s in range(20):
            gg = torch.Generator().manual_seed(2000 + s)
            Xs = torch.rand(5, mod.D, generator=gg)
            vals.append(float(t.objective(Xs).max()))
        opt = opt_a if nm == "aluminum" else opt_c
        seeds[nm] = {"mean_best_seed_pct": sum(vals) / len(vals) / opt, "per_seed_pct": [round(v / opt, 3) for v in vals]}
    res.append({"seed_data": seeds})
    (HERE / "landscape.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__" and "--maps" not in sys.argv:
    main()


def maps(n=61):
    """Best objective over (a, P, v) on a composition slice through each optimum, as % of that optimum."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sys.path.insert(0, str(CU))
    import plot as PL  # noqa: F401  (the benchmark's fonts)

    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=3).draw(2048).double()
    opt_a = json.loads((HERE / "al_optimum.json").read_text())["kappa1"]
    opt_c = next(r["optimum"] for r in json.loads((CU / "truth_tables.json").read_text()) if (r["kappa"], r["eta"]) == (1.0, 1.0))
    ta, tc = al.AlloyTruth(1.0), cu.AlloyTruth(1.0, 1.0)
    g = torch.linspace(0, 1, n)
    panels = [("Aluminum LPBF (kappa = 1)", ta, opt_a, (0, 1), "Zn + Mg (scaled)", "Cu (scaled)", [None, None, 1.0, 0.0], None),
              ("Copper DED (1, 1)", tc, opt_c, (0, 1), "Ni, wt%", "Al, wt%", [None, None, 0.5, 0.0], (30.0, 9.5))]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    for ax, (title, t, opt, _, xl, yl, comp, scale) in zip(axes, panels):
        Z = torch.empty(n, n)
        for i, a in enumerate(g):
            c = torch.tensor([[float(a), float(b), comp[2], comp[3]] for b in g])  # [n, 4]
            X = torch.cat([c.unsqueeze(1).expand(n, apv.shape[0], 4), apv.unsqueeze(0).expand(n, -1, -1)], -1).reshape(-1, 7)
            Z[:, i] = (t.objective(X).reshape(n, -1).max(1).values / opt)
        ext = [0, scale[0], 0, scale[1]] if scale else [0, 1, 0, 1]
        im = ax.imshow(Z.numpy() * 100, origin="lower", extent=ext, aspect="auto", cmap="RdGy_r", vmin=-100, vmax=100)
        ax.contour(torch.linspace(ext[0], ext[1], n).numpy(), torch.linspace(ext[2], ext[3], n).numpy(), Z.numpy() * 100, levels=[0, 60], colors=["#262626", "#262626"],
                   linewidths=[1.0, 1.8], linestyles=["--", "-"])
        ax.set_title(title, fontsize=15, loc="left")
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        share = float((Z >= 0.6).double().mean())
        ax.text(0.98, 0.03, f"{share:.0%} of this slice\nwithin 60% of J*", transform=ax.transAxes, ha="right", va="bottom", fontsize=12,
                bbox=dict(fc="white", ec="none", alpha=0.8))
    cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
    cb.set_label("best over atomizer, power, speed (% of J*)")
    axes[0].text(0.02, 0.97, "Zr = 1, Sc = 0", transform=axes[0].transAxes, va="top", fontsize=12)
    axes[1].text(0.02, 0.97, "Fe = 2.25 wt%, Mn = 0", transform=axes[1].transAxes, va="top", fontsize=12)
    fig.savefig(HERE / "compare_landscape_maps.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__" and "--maps" in sys.argv:
    maps()
