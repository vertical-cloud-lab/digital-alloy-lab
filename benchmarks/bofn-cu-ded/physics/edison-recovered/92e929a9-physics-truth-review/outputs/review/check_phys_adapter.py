"""Checks of the physics-based truth (BOFN_TRUTH=phys): calibration, reference alloys, landscape, optimum.

    BOFN_TRUTH=phys python physics/check_phys.py     # writes physics/phys_tables.md and physics/phys_tables.json

Compares with the hand-written truth (bofn_alloy.AlloyTruth with its own SPEC), so it imports the
synthetic truth in a subprocess-free way: the hand-written node functions do not depend on SPEC.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["BOFN_TRUTH"] = "phys"
HERE = Path(__file__).parent
sys.path.insert(0, "/workspace")
sys.path.insert(0, str(HERE.parent))
import torch  # noqa: E402

torch.set_default_dtype(torch.double)
torch.set_num_threads(4)
import types
import truth_phys as TP
BA = types.SimpleNamespace(feasible_designs=TP.feasible)
import truth_phys as TP

N_RANDOM = int(os.environ.get("N_RANDOM", 400_000))
SUFFIX = "" if os.environ.get("BOFN_REF", "C71500") == "C71500" else "_" + os.environ["BOFN_REF"].lower()
OUT_MD, OUT_JSON = HERE / f"phys_tables{SUFFIX}.md", HERE / f"phys_tables{SUFFIX}.json"
ALLOYS = {  # wt% (Ni, Al, Fe, Mn), Cu balance
    "Cu (C10100)": (0, 0, 0, 0),
    "C70600 90-10 Cu-Ni": (10, 0, 1.4, 0.8),
    "C71500 70-30 Cu-Ni": (30, 0, 0.675, 0.8),
    "C61400 aluminum bronze": (0, 7.0, 2.5, 0),
    "C95800 NAB": (4.5, 9.0, 4.05, 1.2),
    "Cu-7Ni-3Al-1Fe-1Mn (Yang 2018)": (7, 3, 1, 1),
    "NAB 7Al-7Ni-4Fe-2Mn (Tan 2024)": (7, 7, 4, 2),
    "NAB 9Al-5Ni-4Fe-2Mn (Tan 2024)": (5, 9, 4, 2),
    "v1 optimum (13Ni-5.5Al-2.2Fe)": (12.9, 5.5, 2.25, 0),
}


def scaled(wt):
    return (torch.tensor(wt, dtype=torch.double) / TP.WT_MAX).clamp(0, 1)


def best_settings(truth, c, n=8192, key="J"):
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=0).draw(n).double()
    X = torch.cat([c.expand(n, 4), apv], -1)
    out = truth.full(X)
    J = truth.objective(X, out)
    j = int((J if key == "J" else out["rho_m"]).argmax())
    return X[j], {k: float(v[j]) for k, v in out.items()}, float(J[j])


def electro(c, beta=0.0, rho_m=1.0):
    fast, slow = TP.film_terms(c.unsqueeze(0))
    M = float(TP.mass_loss_30d(fast, slow, torch.tensor([beta]), torch.tensor([rho_m]))[0])
    i = {lab: float(TP.current(torch.tensor(t), fast, slow)[0]) for lab, t in (("1h", 3600.0), ("1d", 86400.0), ("10d", 864000.0), ("30d", 2592000.0))}
    return M, i


def optimum(truth, X, J, starts=20, rounds=60, n=384, seed=0):
    g = torch.Generator().manual_seed(seed)
    order = J.argsort(descending=True)[:starts]
    best_x, best_j = None, -1e9
    for x0 in X[order]:
        x, jx = x0.clone(), float(truth.objective(x0.unsqueeze(0))[0])
        for r in range(rounds):
            scale = 0.08 * (0.93**r)
            cand = (x + scale * torch.randn(n, 7, generator=g)).clamp(0, 1)
            cand = cand[BA.feasible_designs(cand)]
            if len(cand) == 0:
                continue
            jc = truth.objective(cand)
            k = int(jc.argmax())
            if float(jc[k]) > jx:
                x, jx = cand[k], float(jc[k])
        if jx > best_j:
            best_x, best_j = x, jx
    return best_x, best_j


def main():
    G = TP.grid()
    lines = ["# Physics-based truth: checks", "", f"Immersion reference: {TP.REF_ALLOY}. CALPHAD grid: {G.V['T_liq'].numel()} points, {G.missing} missing.", ""]
    res = {"grid_missing": G.missing}
    t11 = TP.PhysTruth(1.0, 1.0)
    m_ref, rho_ref, x_ref = TP.reference_m()
    res["m_ref"] = m_ref
    # ---- calibration table: dense, beta-free coupons
    lines += ["## Corrosion model on dense, beta-free coupons", "",
              "| Alloy | Ni in alpha (900 C) | Al in alpha (900 C) | Fe in solution | 30-day mass loss (uA d/cm2) | ratio to C71500 | mean rate (mm/y) | i at 1 h | 1 d | 10 d | 30 d (uA/cm2) | m | passes |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    M_ref, _ = electro(scaled(ALLOYS["C71500 70-30 Cu-Ni"]))
    cal = {}
    for name, wt in ALLOYS.items():
        c = scaled(wt)
        wtt = TP.wt_of(c.unsqueeze(0))
        ni_a, al_a = float(torch.minimum(wtt[..., 0], G("a900_NI", wtt))[0]), float(torch.minimum(wtt[..., 1], G("a900_AL", wtt))[0])
        fe_s = float(torch.minimum(wtt[..., 2], G("a900_FE", wtt))[0])
        M, i = electro(c)
        m = float(TP.m_index(torch.tensor(M)))
        rate = M / 30 * 0.0117 * 365 / 365  # uA d/cm2 over 30 d -> mean uA/cm2 -> mm/y (n = 2)
        cal[name] = {"M30": M, "ratio": M / M_ref, "mm_per_y": M / 30 * 0.0117, "i": i, "m": m}
        lines.append(f"| {name} | {ni_a:.1f} | {al_a:.1f} | {fe_s:.2f} | {M:.1f} | {M / M_ref:.2f} | {M / 30 * 0.0117:.4f} | {i['1h']:.1f} | {i['1d']:.1f} | {i['10d']:.2f} | {i['30d']:.2f} | {m:.3f} | {'yes' if m >= m_ref - 1e-9 else 'no'} |")
    res["calibration"] = cal
    lines += ["", f"m_ref = {m_ref:.4f} ({TP.REF_ALLOY} dense at its best settings, rho_m = {rho_ref:.3f}; 'passes' compares with it). "
              "Mean rate uses n = 2 (0.0117 mm/y per uA/cm2). The film model reads the alpha composition at 900 C (Fe capped at 1.5 wt%).", ""]
    # ---- reference alloys at their best settings
    lines += ["## Reference alloys at their best settings for J, (kappa, eta) = (1, 1)", "",
              "| Alloy | J | T_liq (C) | Scheil range (K) | beta at 900 C | kappa at 700 C | s | f | g | h | rho_u | rho_m | beta | U | w | m | passes | feasible |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    refs = {}
    for name, wt in ALLOYS.items():
        c = scaled(wt)
        x, o, J = best_settings(t11, c)
        wtt = TP.wt_of(c.unsqueeze(0))
        row = {"x": [round(float(v), 4) for v in x], "J": J, **o, "T_liq": float(G("T_liq", wtt)[0]), "scheil": float(G("sch_range99", wtt)[0]),
               "beta900": float(G("beta_900", wtt)[0]), "kappa700": float(G("kappa_fe_700", wtt)[0] + G("kappa_nial_700", wtt)[0]), "feasible": bool(BA.feasible_designs(c.unsqueeze(0))[0])}
        refs[name] = row
        lines.append(f"| {name} | {J:.3f} | {row['T_liq']:.0f} | {row['scheil']:.0f} | {row['beta900']:.2f} | {row['kappa700']:.3f} | {o['s']:.2f} | {o['f']:.2f} | {o['g']:.2f} | {o['h']:.2f} | {o['rho_u']:.2f} | {o['rho_m']:.2f} | {o['beta']:.2f} | {o['U']:.2f} | {o['w']:.2f} | {o['m']:.3f} | {'yes' if o['m'] >= m_ref else 'no'} | {'yes' if row['feasible'] else 'no'} |")
    res["references"] = refs
    # ---- landscape: random designs, box and feasible space, both truths
    g = torch.Generator().manual_seed(0)
    X = torch.rand(N_RANDOM, 7, generator=g)
    feas = BA.feasible_designs(X)
    out, J = {}, []
    for k in range(0, N_RANDOM, 50_000):
        o = t11.full(X[k : k + 50_000])
        J.append(t11.objective(X[k : k + 50_000], o))
        for n in ("m", "rho_m", "beta"):
            out.setdefault(n, []).append(o[n])
    J = torch.cat(J)
    out = {n: torch.cat(v) for n, v in out.items()}
    xo, Jo = optimum(t11, X[feas], J[feas])
    oo = t11.full(xo.unsqueeze(0))
    res["optimum"] = {"J": Jo, "x": [round(float(v), 4) for v in xo], "wt": [round(float(v), 2) for v in TP.wt_of(xo)], **{k: float(v[0]) for k, v in oo.items()}}
    passes = out["m"] >= m_ref
    ni_wt = X[:, 0] * 30
    lines += ["## Landscape (uniform random designs)", "",
              f"- {N_RANDOM:,} designs; {float(feas.double().mean()):.1%} lie inside the proposal's limits (liquidus <= 1,250 C, Cu >= 65 wt%, Ni >= Fe above 7 wt% Al, Fe <= 2.3 wt% below 1.5 wt% Al).",
              f"- Pass immersion: {float(passes.double().mean()):.1%} of the box, {float(passes[feas].double().mean()):.1%} of the feasible space.",
              f"- J > 0: {float((J > 0).double().mean()):.1%} of the box, {float((J[feas] > 0).double().mean()):.1%} of the feasible space.",
              f"- Within 60% / 80% of the optimum (feasible space): {float((J[feas] >= 0.6 * Jo).double().mean()):.2%} / {float((J[feas] >= 0.8 * Jo).double().mean()):.3%}.",
              f"- Lowest Ni among designs that pass immersion: {float(ni_wt[passes].min()):.2f} wt% (box), {float(ni_wt[passes & feas].min()):.2f} wt% (feasible)." if passes.any() else "- No random design passes immersion.",
              ""]
    sel10 = feas & (ni_wt >= 10)
    lines.append(f"- With a 10 wt% Ni floor ({float(sel10.double().mean()):.0%} of the box): {float(passes[sel10].double().mean()):.1%} pass immersion, "
                 f"{float((J[sel10] > 0).double().mean()):.1%} have J > 0, {float((J[sel10] >= 0.6 * Jo).double().mean()):.2%} are within 60% of the optimum.")
    ni10 = dict(ni10_share=float(sel10.double().mean()), ni10_pass=float(passes[sel10].double().mean()), ni10_Jpos=float((J[sel10] > 0).double().mean()),
                            ni10_within60=float((J[sel10] >= 0.6 * Jo).double().mean()))
    for lo in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20):
        hi = {8: 10, 10: 12, 12: 15, 15: 20, 20: 30}.get(lo, lo + 1)
        sel = feas & (ni_wt >= lo) & (ni_wt < hi)
        if sel.any():
            lines.append(f"  - Ni {lo}-{hi} wt%: {float(passes[sel].double().mean()):.2%} of feasible designs pass immersion")
    res["landscape"] = {"feasible_share": float(feas.double().mean()), "pass_box": float(passes.double().mean()), "pass_feasible": float(passes[feas].double().mean()),
                        "Jpos_box": float((J > 0).double().mean()), "Jpos_feasible": float((J[feas] > 0).double().mean()),
                        "within60_feasible": float((J[feas] >= 0.6 * Jo).double().mean()), "within80_feasible": float((J[feas] >= 0.8 * Jo).double().mean()),
                        "min_ni_pass_box": float(ni_wt[passes].min()) if passes.any() else None, "min_ni_pass_feasible": float(ni_wt[passes & feas].min()) if (passes & feas).any() else None}
    res["landscape"].update(ni10)
    # expected best of n uniform random designs (feasible space), and the five shared seed designs per seed
    Jf = J[feas].sort().values
    N = len(Jf)
    k = torch.arange(1, N + 1, dtype=torch.double)
    for n in (5, 24):
        wts = (k / N) ** n - ((k - 1) / N) ** n
        res["landscape"][f"expected_best_of_{n}"] = float((wts * Jf).sum() / Jo)
    res["landscape"]["seed_designs_best_mean"] = float("nan")  # Not reproducible: bofn_alloy absent.
    lines += [f"- Expected best of 5 / 24 uniform random feasible designs: {res['landscape']['expected_best_of_5']:.0%} / {res['landscape']['expected_best_of_24']:.0%} of the optimum; "
              f"mean best of the five shared seed designs (seeds 0-19): {res['landscape']['seed_designs_best_mean']:.0%}.", ""]
    o = res["optimum"]
    lines += ["", "## Optimum, (kappa, eta) = (1, 1)", "",
              f"J* = {o['J']:.4f} at Ni {o['wt'][0]} wt%, Al {o['wt'][1]}, Fe {o['wt'][2]}, Mn {o['wt'][3]}; a = {o['x'][4]}, P = {o['x'][5]}, v = {o['x'][6]}. "
              f"s = {o['s']:.2f}, f = {o['f']:.2f}, g = {o['g']:.2f}, h = {o['h']:.2f}, q = {o['q']:.2f}, rho_u = {o['rho_u']:.2f}, rho_m = {o['rho_m']:.2f}, beta = {o['beta']:.3f}, U = {o['U']:.2f}, w = {o['w']:.2f}, m = {o['m']:.3f}.", ""]
    OUT_MD.write_text("\n".join(lines) + "\n")
    OUT_JSON.write_text(json.dumps(res, indent=1))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
