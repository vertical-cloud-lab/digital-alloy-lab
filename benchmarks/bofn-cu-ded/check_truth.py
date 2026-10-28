"""Required properties of the copper/DED truth, per (kappa, eta) cell; writes truth_tables.md.

    python check_truth.py            # all four cells
    python check_truth.py 1 1        # one cell
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

from bofn_alloy import D, F_SAFE, M_REF, ORDER, REFERENCE, RHO_REF, X_REF, AlloyTruth, burden

HERE = Path(__file__).parent
CELLS = [(1.0, 1.0), (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
N_RANDOM = 400_000


def refine(t, x0, g, mask=None):
    """Multi-start local search from x0 [k, D] (random perturbations at three scales)."""
    best_x, best_y = None, -1e9
    for x in x0:
        xb, yb = x, float(t.objective(x.unsqueeze(0))[0])
        for scale in (0.03, 0.01, 0.003):
            P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
            yp = t.objective(P)
            if mask is not None:
                yp = torch.where(mask(t, P), yp, torch.full_like(yp, -9.0))
            if float(yp.max()) > yb:
                xb, yb = P[yp.argmax()], float(yp.max())
        if yb > best_y:
            best_x, best_y = xb, yb
    return best_x, best_y


def dense_w_gate(t, X, out, q=0.75):
    """The one-hour screen gate a tiered lab would face: the top quartile by w of dense candidates
    (rho_m >= 0.5) that passed the CALPHAD crack screen."""
    dense = (out["rho_m"] >= 0.5) & (out["f"] <= F_SAFE)
    return float(out["w"][dense].quantile(q)), dense


def cell_report(kappa, eta):
    t = AlloyTruth(kappa, eta)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(N_RANDOM, D, generator=g)
    out = t.full(X)
    y = t.objective(X, out)
    top = X[y.topk(20).indices]
    xs, ys = refine(t, top, g)
    ns = {k: float(v) for k, v in t.full(xs.unsqueeze(0)).items()}
    w_gate, dense = dense_w_gate(t, X, out)
    w_rank = float((out["w"][dense] <= ns["w"]).double().mean())
    # best design that passes the CALPHAD crack screen, and the best that passes both screens
    okf = out["f"] <= F_SAFE
    xf, yf = refine(t, X[torch.where(okf, y, torch.full_like(y, -9.0)).topk(10).indices], g, mask=lambda tt, P: tt.full(P)["f"] <= F_SAFE)
    okb = okf & (out["w"] >= w_gate)
    xb, yb = refine(t, X[torch.where(okb, y, torch.full_like(y, -9.0)).topk(10).indices], g,
                    mask=lambda tt, P: (lambda o: (o["f"] <= F_SAFE) & (o["w"] >= w_gate))(tt.full(P)))
    if yb > yf:  # a design passing both screens also passes the first one
        xf, yf = xb, yb
    # ridge in (P, v): fraction of a 101 x 101 grid within 0.5% of the optimum, with the other inputs fixed
    Pg, vg = torch.meshgrid(torch.linspace(0, 1, 101), torch.linspace(0, 1, 101), indexing="ij")
    Xg = xs.expand(101 * 101, D).clone()
    Xg[:, 5], Xg[:, 6] = Pg.reshape(-1), vg.reshape(-1)
    yg = t.objective(Xg)
    ridge = {}
    for tol in (0.005, 0.01, 0.02):
        near = yg >= ys - tol * abs(ys)
        ridge[f"{tol:.1%}"] = {"frac_of_grid": float(near.double().mean()), "n_points": int(near.sum()),
                               "P_range": [float(Xg[near, 5].min()), float(Xg[near, 5].max())], "v_range": [float(Xg[near, 6].min()), float(Xg[near, 6].max())],
                               "P_minus_v_range": [float((Xg[near, 5] - Xg[near, 6]).min()), float((Xg[near, 5] - Xg[near, 6]).max())]}
    # reference alloys at their best settings for J (and NAB deposited fast and cool: on the ridge at low power)
    refs = {}
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=1).draw(16384).double()
    for name, c in REFERENCE.items():
        Xr = torch.cat([torch.tensor(c).expand(apv.shape[0], 4), apv], -1)
        o = t.full(Xr)
        yr = t.objective(Xr, o)
        j = yr.argmax()
        jd = o["rho_m"].argmax()
        refs[name] = {"J": float(yr[j]), "pct_of_optimum": float(yr[j] / ys), "rho_m": float(o["rho_m"][j]), "U": float(o["U"][j]), "beta": float(o["beta"][j]),
                      "m": float(o["m"][j]), "w": float(o["w"][j]), "f": float(o["f"][j]), "passes_immersion": bool(o["m"][j] >= M_REF),
                      "passes_calphad_screen": bool(o["f"][j] <= F_SAFE), "burden": float(burden(Xr[j])), "x": [round(v, 3) for v in Xr[j].tolist()],
                      "densest": {"rho_m": float(o["rho_m"][jd]), "m": float(o["m"][jd]), "beta": float(o["beta"][jd]), "U": float(o["U"][jd]),
                                  "passes_immersion": bool(o["m"][jd] >= M_REF), "x": [round(v, 3) for v in Xr[jd].tolist()]}}
    # the Utah power cap: copper-rich compositions cannot fuse at Utah but can at Mines
    rich = (X[:, 0] <= 0.07) & (X[:, 1] <= 0.2)
    Xc = X[rich][:2000]
    cap = {}
    for name, c in (("copper-rich (Ni <= 0.07, Al <= 0.2, i.e. under about 2 wt% Ni and 2 wt% Al)", None),):
        res_u, res_m = [], []
        for xi in Xc[:200]:
            Xr = torch.cat([xi[:4].expand(apv.shape[0], 4), apv], -1)
            o = t.full(Xr)
            res_u.append(float(o["rho_u"].max()))
            res_m.append(float(o["rho_m"].max()))
        ru, rm = torch.tensor(res_u), torch.tensor(res_m)
        cap[name] = {"n": len(res_u), "median_best_rho_u": float(ru.median()), "median_best_rho_m": float(rm.median()),
                     "frac_rho_u_below_0.3": float((ru < 0.3).double().mean()), "frac_rho_m_above_0.7": float((rm > 0.7).double().mean()),
                     "frac_rho_u_passing_utah_gate_0.5": float((ru >= 0.5).double().mean())}
    # the same for the optimum's composition
    Xr = torch.cat([xs[:4].expand(apv.shape[0], 4), apv], -1)
    o = t.full(Xr)
    cap["optimum composition"] = {"best_rho_u": float(o["rho_u"].max()), "best_rho_m": float(o["rho_m"].max())}
    return {
        "kappa": kappa, "eta": eta, "optimum": ys, "x_opt": [round(v, 3) for v in xs.tolist()], "nodes_opt": {k: round(v, 3) for k, v in ns.items()},
        "burden_opt": float(burden(xs)), "optimum_fails_calphad_screen": bool(ns["f"] > F_SAFE), "F_SAFE": F_SAFE,
        "w_gate_top_quartile_of_dense": w_gate, "optimum_w_percentile_among_dense": w_rank, "optimum_below_top_quartile": bool(ns["w"] < w_gate),
        "best_passing_calphad_screen": {"J": yf, "pct": yf / ys, "x": [round(v, 3) for v in xf.tolist()], "nodes": {k: round(float(v), 3) for k, v in t.full(xf.unsqueeze(0)).items()}},
        "best_passing_both_screens": {"J": yb, "pct": yb / ys, "x": [round(v, 3) for v in xb.tolist()], "nodes": {k: round(float(v), 3) for k, v in t.full(xb.unsqueeze(0)).items()}},
        "ridge": ridge, "reference_alloys": refs, "utah_cap": cap,
    }


def markdown(reports):
    L = ["# Truth tables (written by `check_truth.py`)", "",
         f"`m_ref` = {M_REF:.3f}: the immersion index of C71500 (70-30 Cu-Ni) deposited dense (rho_m = {RHO_REF:.2f}) at its best settings "
         f"(a, P, v) = ({X_REF[4]:.2f}, {X_REF[5]:.2f}, {X_REF[6]:.2f}) in the headline world, fixed for every cell. "
         f"CALPHAD crack screen: f <= {F_SAFE}. One-hour screen gate: top quartile by w of the dense candidates (rho_m >= 0.5) that passed the CALPHAD screen, which is what a tiered lab would be ranking.", ""]
    L += ["## The optimum per cell (multi-start local search from the best of 400,000 random designs)", "",
          "| (kappa, eta) | J* | Ni | Al | Fe | Mn | a | P | v | s | f | g | h | q | rho_u | rho_m | beta | U | w | m | burden |", "|---|" + "---|" * 20]
    for r in reports:
        x = r["x_opt"]
        n = r["nodes_opt"]
        L.append(f"| ({r['kappa']:g}, {r['eta']:g}) | **{r['optimum']:.3f}** | " + " | ".join(f"{v:.2f}" for v in x) + " | " + " | ".join(f"{n[k]:.2f}" for k in ORDER) + f" | {r['burden_opt']:.2f} |")
    L += ["", "## Required property 1: what the screens do to the optimum", "",
          "| (kappa, eta) | optimum's f (screen keeps f <= " + str(F_SAFE) + ") | fails CALPHAD screen | optimum's w percentile among dense candidates | below the top quartile | best design passing the CALPHAD screen (% of J*) | best passing both screens (% of J*) |", "|---|---|---|---|---|---|---|"]
    for r in reports:
        L.append(f"| ({r['kappa']:g}, {r['eta']:g}) | {r['nodes_opt']['f']:.2f} | {'yes' if r['optimum_fails_calphad_screen'] else 'no'} | {r['optimum_w_percentile_among_dense']:.0%} | {'yes' if r['optimum_below_top_quartile'] else 'no'} | {r['best_passing_calphad_screen']['pct']:.0%} | {r['best_passing_both_screens']['pct']:.0%} |")
    L += ["", "## Required property 2: the reference alloys at their best settings for J", ""]
    for r in reports:
        L += [f"**({r['kappa']:g}, {r['eta']:g})**", "", "| Alloy | J | % of J* | U | rho_m | beta | m | passes immersion (m >= m_ref) | w | f | passes CALPHAD screen | burden | densest build: rho_m, beta, m, passes |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for name, v in r["reference_alloys"].items():
            dd = v["densest"]
            L.append(f"| {name} | {v['J']:.3f} | {v['pct_of_optimum']:.0%} | {v['U']:.2f} | {v['rho_m']:.2f} | {v['beta']:.2f} | {v['m']:.2f} | {'yes' if v['passes_immersion'] else 'no'} | {v['w']:.2f} | {v['f']:.2f} | {'yes' if v['passes_calphad_screen'] else 'no'} | {v['burden']:.2f} | {dd['rho_m']:.2f}, {dd['beta']:.2f}, {dd['m']:.2f}, {'yes' if dd['passes_immersion'] else 'no'} |")
        L.append("")
    L += ["## Required property 3: the optimum is a ridge in (P, v)", "", "| (kappa, eta) | grid points within 0.5% of J* (of 10,201) | P range | v range | P - v range |", "|---|---|---|---|---|"]
    for r in reports:
        rr = r["ridge"]["0.5%"]
        L.append(f"| ({r['kappa']:g}, {r['eta']:g}) | {rr['n_points']} ({rr['frac_of_grid']:.1%}) | {rr['P_range'][0]:.2f} to {rr['P_range'][1]:.2f} | {rr['v_range'][0]:.2f} to {rr['v_range'][1]:.2f} | {rr['P_minus_v_range'][0]:.2f} to {rr['P_minus_v_range'][1]:.2f} |")
    L += ["", "## Required property 4: the Utah power cap binds for copper-rich compositions", "", "| (kappa, eta) | compositions | median best rho_u (Utah, P <= 0.5) | median best rho_m (Mines) | share with best rho_u < 0.3 | share passing the Utah gate (rho_u >= 0.5) | share with best rho_m > 0.7 | optimum's composition: best rho_u, best rho_m |", "|---|---|---|---|---|---|---|---|"]
    for r in reports:
        c = r["utah_cap"]
        k = next(k for k in c if k != "optimum composition")
        v, o = c[k], c["optimum composition"]
        L.append(f"| ({r['kappa']:g}, {r['eta']:g}) | {k} (first {v['n']}) | {v['median_best_rho_u']:.2f} | {v['median_best_rho_m']:.2f} | {v['frac_rho_u_below_0.3']:.0%} | {v['frac_rho_u_passing_utah_gate_0.5']:.0%} | {v['frac_rho_m_above_0.7']:.0%} | {o['best_rho_u']:.2f}, {o['best_rho_m']:.2f} |")
    return "\n".join(L) + "\n"


def assert_properties(reports):
    """The required properties (README), asserted rather than only printed (Edison F7). Returns the
    checks that ran, so the tables can say which held."""
    done = []

    def check(ok, what):
        assert ok, f"required property failed: {what}"
        done.append(what)

    by = {(r["kappa"], r["eta"]): r for r in reports}
    if (1.0, 1.0) in by:
        r = by[(1.0, 1.0)]
        # 1: the screens cut the optimum off in the headline world
        check(r["optimum_fails_calphad_screen"] or r["optimum_below_top_quartile"], "1. at (1, 1) the optimum fails the CALPHAD screen or the one-hour screen")
        # 2: the reference alloys
        ref = r["reference_alloys"]
        c715, c706, nab = ref["C71500 (70-30 Cu-Ni)"], ref["C70600 (90-10 Cu-Ni)"], ref["C95800 (NAB)"]
        check(c715["m"] >= M_REF - 1e-6, "2a. C71500 passes immersion (m_ref is its index)")
        check(nab["U"] > max(c715["U"], c706["U"]), "2b. NAB is the strongest reference alloy")
        check(not nab["passes_immersion"] and nab["beta"] > 0.1, "2c. NAB, deposited at its best settings for J, carries beta-prime and fails immersion")
        check(c706["passes_immersion"] and c706["U"] < nab["U"] and c706["burden"] < c715["burden"], "2d. C70600 is weaker than NAB, uses less nickel than C71500, and passes")
    if (0.0, 0.0) in by:
        check(by[(0.0, 0.0)]["best_passing_both_screens"]["pct"] >= 0.85, "1. at (0, 0) the screens keep at least 85% of the optimum")
    for r in reports:
        cell = f"({r['kappa']:g}, {r['eta']:g})"
        rr = r["ridge"]["0.5%"]
        # 3: a ridge, not a point: several grid points within 0.5% of J*, spread along P
        check(rr["n_points"] >= 5 and rr["P_range"][1] - rr["P_range"][0] >= 0.05, f"3. {cell} the optimum is a ridge in (P, v)")
        c = r["utah_cap"]
        v = c[next(k for k in c if k != "optimum composition")]
        # 4: Utah's cap binds for the median copper-rich composition (not for every one; the share that
        # still passes the Utah density gate is reported in the tables), and Mines can fuse them
        check(v["median_best_rho_u"] < 0.5 and v["frac_rho_u_passing_utah_gate_0.5"] < 0.5 and v["median_best_rho_m"] >= 0.7,
              f"4. {cell} Utah's power cap keeps the median copper-rich composition below the density gate, Mines fuses it")
    return done


if __name__ == "__main__":
    cells = [(float(sys.argv[1]), float(sys.argv[2]))] if len(sys.argv) > 2 else CELLS
    reports = [cell_report(*c) for c in cells]
    (HERE / "truth_tables.json").write_text(json.dumps(reports, indent=1))
    md = markdown(reports)
    (HERE / "truth_tables.md").write_text(md)
    print(md)
    for what in assert_properties(reports):
        print("holds:", what)
