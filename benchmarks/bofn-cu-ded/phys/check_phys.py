"""The physics-based truth at a glance: optimum, reference alloys, the share of the space that passes
immersion, and the nickel floor (optimized, not sampled), under both bars. Writes phys/phys_tables.md
and phys/phys_tables.json.

    BOFN_TRUTH=phys python phys/check_phys.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("BOFN_TRUTH", "phys")
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

import torch  # noqa: E402

import bofn_alloy as BA  # noqa: E402
import truth_phys as TP  # noqa: E402

D = BA.D
N_RANDOM = 200_000


def best_settings(t, c, mask_m=None):
    """Best J over (a, P, v) for a composition c [4]."""
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=1).draw(16384).double()
    X = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
    o = t.full(X)
    y = t.objective(X, o)
    j = y.argmax()
    return float(y[j]), {k: float(v[j]) for k, v in o.items()}, X[j]


def refine(t, x0, g, ok):
    """Multi-start local search over designs inside the limits."""
    best_x, best_y = None, -1e9
    for x in x0:
        xb, yb = x, float(t.objective(x.unsqueeze(0))[0])
        for scale in (0.05, 0.02, 0.006, 0.002):
            P = (xb + scale * torch.randn(3000, D, generator=g)).clamp(0, 1)
            P = P[ok(P)]
            if not len(P):
                continue
            yp = t.objective(P)
            if float(yp.max()) > yb:
                xb, yb = P[yp.argmax()], float(yp.max())
        if yb > best_y:
            best_x, best_y = xb, yb
    return best_x, best_y


def ni_floor(t, m_ref, g, n=200_000):
    """Lowest Ni (wt%) of a design inside the limits whose immersion index reaches m_ref: sampled, then
    pushed down by a local search that keeps m >= m_ref (the sampled minimum overstates the floor)."""
    X = torch.rand(n, D, generator=g)
    X = X[TP.feasible(X)]
    m = t.full(X)["m"]
    ok = m >= m_ref
    if not ok.any():
        return None, None, float(ok.double().mean())
    share = float(ok.double().mean())
    start = X[ok][X[ok][:, 0].argsort()[:20]]
    best = None
    for x in start:
        xb = x.clone()
        for scale in (0.05, 0.02, 0.008, 0.003, 0.001):
            for _ in range(3):
                P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
                P = P[TP.feasible(P)]
                P = P[t.full(P)["m"] >= m_ref]
                if len(P) and float(P[:, 0].min()) < float(xb[0]):
                    xb = P[P[:, 0].argmin()]
        if best is None or float(xb[0]) < float(best[0]):
            best = xb
    return float(best[0]) * 30.0, best, share


def wtstr(x):
    w = (x[:4] * TP.WT_MAX).tolist()
    return f"Ni {w[0]:.1f}, Al {w[1]:.1f}, Fe {w[2]:.1f}, Mn {w[3]:.1f}"


def main():
    g = torch.Generator().manual_seed(0)
    out = {"bar": TP.BAR, "m_ref": BA.M_REF}
    t = BA.make_truth(1.0, 1.0)
    X = torch.rand(N_RANDOM, D, generator=g)
    okX = TP.feasible(X)
    out["share_of_box_inside_limits"] = float(okX.double().mean())
    X = X[okX]
    o = t.full(X)
    y = t.objective(X, o)
    xs, ys = refine(t, X[y.topk(20).indices], g, TP.feasible)
    ns = {k: float(v) for k, v in t.full(xs.unsqueeze(0)).items()}
    out["optimum"] = {"J": ys, "x": xs.tolist(), "wt": wtstr(xs), "nodes": ns, "strength_MPa": float(TP.strength_mpa(xs[:4])),
                      "range_C": float(TP.field(xs[:4], "range_C")), "liquidus_C": float(TP.field(xs[:4], "liquidus_C")),
                      "k_W_mK": float(TP.conductivity(xs[:4])), "fails_calphad_screen": ns["f"] > BA.F_SAFE}
    okf = o["f"] <= BA.F_SAFE
    xf, yf = refine(t, X[torch.where(okf, y, torch.full_like(y, -9.0)).topk(10).indices], g, lambda P: TP.feasible(P) & (t.full(P)["f"] <= BA.F_SAFE))
    out["best_passing_calphad_screen"] = {"J": yf, "pct": yf / ys, "wt": wtstr(xf)}
    out["share_passing_immersion_dense_best"] = None
    refs = {}
    for name, c in BA.REFERENCE.items():
        c = torch.tensor(c)
        J, nodes, xr = best_settings(t, c)
        refs[name] = {"J": J, "pct": J / ys, "inside_limits": bool(TP.feasible(c.unsqueeze(0))[0]), "strength_MPa": float(TP.strength_mpa(c)),
                      "range_C": float(TP.field(c, "range_C")), "liquidus_C": float(TP.field(c, "liquidus_C")), "k_W_mK": float(TP.conductivity(c)),
                      "ln_rate_vs_C71500": float(TP.ln_rate(torch.cat([c[:3], torch.zeros(1)]))), **{k: nodes[k] for k in ("s", "f", "g", "h", "rho_m", "beta", "U", "w", "m")},
                      "passes_immersion": nodes["m"] >= BA.M_REF}
    out["reference_alloys"] = refs
    # the share of designs inside the limits that pass immersion, and the nickel floor, for both bars
    floors = {}
    for bar, name in (("9010", "C70600 (90-10 Cu-Ni)"), ("7030", "C71500 (70-30 Cu-Ni)")):
        m_bar = TP.reference_m(name)[0]
        fl, xfl, share = ni_floor(t, m_bar, g)
        floors[bar] = {"m_bar": m_bar, "share_passing": share, "ni_floor_wt": fl, "witness": None if xfl is None else {"x": xfl.tolist(), "wt": wtstr(xfl), "m": float(t.full(xfl.unsqueeze(0))["m"][0])}}
    out["immersion"] = floors
    (HERE / "phys_tables.json").write_text(json.dumps(out, indent=1, default=float))
    L = [f"# Physics-based truth (`BOFN_TRUTH=phys`, bar {TP.BAR}): written by `phys/check_phys.py`", "",
         f"- Inside the proposal's limits: {out['share_of_box_inside_limits']:.0%} of the box.",
         f"- Bar: m_ref = {BA.M_REF:.3f} ({'dense 90-10 Cu-Ni' if TP.BAR == '9010' else 'dense 70-30 Cu-Ni'}).",
         f"- Optimum at (1, 1): J* = {ys:.3f} at {out['optimum']['wt']} wt%, a = {xs[4]:.2f}, P = {xs[5]:.2f}, v = {xs[6]:.2f}; "
         f"strength estimate {out['optimum']['strength_MPa']:.0f} MPa, freezing range {out['optimum']['range_C']:.0f} C, liquidus {out['optimum']['liquidus_C']:.0f} C, "
         f"k = {out['optimum']['k_W_mK']:.0f} W/m K; rho_m {ns['rho_m']:.2f}, beta {ns['beta']:.2f}, U {ns['U']:.2f}, m {ns['m']:.3f}; "
         f"{'fails' if out['optimum']['fails_calphad_screen'] else 'passes'} the CALPHAD crack screen (f = {ns['f']:.2f}).",
         f"- Best design passing the CALPHAD crack screen: {yf / ys:.0%} of J* ({out['best_passing_calphad_screen']['wt']} wt%).", "",
         "| Reference alloy | inside limits | J (% of J*) | yield estimate (MPa) | freezing range (C) | liquidus (C) | k (W/m K) | ln rate vs C71500 | rho_m | beta | U | m | passes |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in refs.items():
        L.append(f"| {name} | {'yes' if r['inside_limits'] else 'no'} | {r['J']:.3f} ({r['pct']:.0%}) | {r['strength_MPa']:.0f} | {r['range_C']:.0f} | {r['liquidus_C']:.0f} | {r['k_W_mK']:.0f} | {r['ln_rate_vs_C71500']:+.2f} | {r['rho_m']:.2f} | {r['beta']:.2f} | {r['U']:.2f} | {r['m']:.3f} | {'yes' if r['passes_immersion'] else 'no'} |")
    L += ["", "| Bar | m_ref | share of designs inside the limits passing immersion | Ni floor (optimized), wt% | witness |", "|---|---|---|---|---|"]
    for bar, f in floors.items():
        L.append(f"| {'90-10' if bar == '9010' else '70-30'} | {f['m_bar']:.3f} | {f['share_passing']:.1%} | {'none passes' if f['ni_floor_wt'] is None else f'{f["ni_floor_wt"]:.1f}'} | {'' if f['witness'] is None else f['witness']['wt']} |")
    (HERE / "phys_tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
