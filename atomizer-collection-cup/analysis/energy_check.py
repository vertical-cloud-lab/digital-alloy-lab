"""Energy audit of a thermal case: does the pile hold the heat it should, and does what it loses show up in the cup?

    python analysis/energy_check.py B_816       # writes analysis/out/energy_<case>.json

For each saved time: the heat content above 25 C of every region, E = sum over elements of rho * V * int_25^T cp dT
(V = 2 pi r_centroid * area, T = the element's mean nodal temperature, cp(T) the same tables thermal.py gives
CalculiX). Checks:
- the pile's mass and initial heat content against m * (sensible + remaining latent) by hand;
- at each time, the pile's loss against the gain of everything else; the difference is what has left through the
  outside surfaces and the outlet (it must be positive and grow with time).
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import axifea as F  # noqa: E402
import params as P  # noqa: E402
import thermal as TH  # noqa: E402


def tables(pile_k=5.0):
    """{material: (T list, cp list J/kgK, rho kg/m3)} parsed back from thermal.material_cards."""
    names = {"S316L", "S304", "CU", "PILE", "POWDER", "FKM", "EPDM", "BORO", "QUARTZ", "GAP15", "GAP4", "GAP3",
             "CONTACT_RING", "CONTACT_PUCK"}
    txt = TH.material_cards(names, pile_k=pile_k)
    out, cur, mode, T, cp, rho = {}, None, None, [], [], None
    for ln in txt.splitlines():
        if ln.startswith("*MATERIAL"):
            if cur:
                out[cur] = (T, cp, rho)
            cur, T, cp, rho, mode = ln.split("=")[1], [], [], None, None
        elif ln.startswith("*CONDUCTIVITY"):
            mode = "k"
        elif ln.startswith("*DENSITY"):
            mode = "rho"
        elif ln.startswith("*SPECIFIC HEAT"):
            mode = "cp"
        elif mode == "rho":
            rho = float(ln) / F.KG_M3
        elif mode == "cp":
            v, t = [float(x) for x in ln.split(",")]
            cp.append(v / F.J_PER_KGK)
            T.append(t)
    if cur:
        out[cur] = (T, cp, rho)
    return out


def heat(T_e, Tt, cpt):
    """int_25^T cp dT for an array of temperatures (J/kg), piecewise-linear cp as CalculiX interpolates it."""
    grid = np.linspace(25.0, max(1200.0, float(np.max(T_e)) + 1), 4000)
    cpg = np.interp(grid, Tt, cpt)
    cum = np.concatenate([[0.0], np.cumsum((cpg[1:] + cpg[:-1]) / 2 * np.diff(grid))])
    return np.interp(T_e, grid, cum)


def main(case):
    spec = TH.CASES[case]
    extra = dict(spec[3]) if len(spec) > 3 else {}
    ms = extra.pop("mesh_scale", TH.MESH_SCALE)
    regs, cav, probes, info = TH.DESIGNS[spec[0]](spec[1], **spec[2])
    for r in regs:
        r.size *= ms
    m = F.build_mesh(regs, order=1)
    tab = tables(**({"pile_k": extra["pile_k"]} if "pile_k" in extra else {}))
    mat = {r.name: r.material for r in regs}
    els = sorted(m.elems)
    xy = {e: np.array([m.nodes[n] for n in m.elems[e]]) for e in els}
    vol = {}
    for e in els:
        (x1, y1), (x2, y2), (x3, y3) = xy[e]
        area = 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        vol[e] = 2 * math.pi * (x1 + x2 + x3) / 3 * area * 1e-9          # m3
    frd = F.read_frd(TH.OUT / case / "pass2.frd")
    # the initial state as CalculiX sees it: pile nodes (including those it shares with its neighbours) at T0
    T0_reg = {r.name: r.init_T for r in regs if r.init_T is not None}
    hot_nodes = {}
    for name, T_ in T0_reg.items():
        for n in m.region_nodes(name):
            hot_nodes[n] = T_
    init_vals = {n: [hot_nodes.get(n, TH.T_AMB)] for n in m.nodes}
    frd = [(0.0, init_vals)] + list(frd)
    rows = []
    for t, vals in frd:
        if t is None:
            continue
        E = {}
        for reg in set(mat.values()) | {"pile"}:
            pass
        by_region = {}
        for e in els:
            reg = m.elem_region[e]
            T_e = np.mean([vals[n][0] for n in m.elems[e]])
            Tt, cpt, rho = tab[mat[reg]]
            by_region.setdefault(reg, 0.0)
            by_region[reg] += rho * vol[e] * float(heat(np.array([T_e]), Tt, cpt)[0])
        rows.append((t, by_region))
    # the initial state (t = 0) from the initial conditions
    pile_mass = sum(tab[mat["pile"]][2] * vol[e] for e in els if m.elem_region[e] == "pile")
    Tt, cpt, rho = tab[mat["pile"]]
    T0 = next(r.init_T for r in regs if r.name == "pile")
    E0_pile = pile_mass * float(heat(np.array([T0]), Tt, cpt)[0])
    L_left = 0.71 * P.SHOT["L"] if mat["pile"] == "PILE" else 0.0
    E0_hand = spec[1] * 1e-3 * (float(np.trapezoid([480 if x < 940 else 480 for x in np.linspace(25, T0, 50)],
                                                   np.linspace(25, T0, 50))) * 0 + 0)
    sens = float(heat(np.array([T0]), [20, 500, 940, 941], [420, 460, 480, 480])[0])
    E0_hand = spec[1] * 1e-3 * (sens + L_left)
    out = {"case": case, "pile_mass_g_mesh": round(pile_mass * 1e3, 1), "pile_mass_g_nominal": spec[1],
           "E0_pile_kJ_model": round(E0_pile / 1e3, 1), "E0_pile_kJ_by_hand": round(E0_hand / 1e3, 1),
           "times": []}
    Etot0 = None
    for t, br in rows:
        Ep = br.get("pile", 0.0)
        Erest = sum(v for k, v in br.items() if k != "pile")
        if Etot0 is None:
            Etot0, Erest0 = Ep + Erest, Erest
        out["times"].append({"t_s": t, "pile_kJ": round(Ep / 1e3, 2), "rest_kJ": round(Erest / 1e3, 2),
                             "total_kJ": round((Ep + Erest) / 1e3, 2),
                             "left_the_model_kJ": round((Etot0 - Ep - Erest) / 1e3, 2)})
    out["initial_extra_in_neighbours_kJ"] = round(Erest0 / 1e3, 1)
    out["note"] = ("The pile's boundary nodes are shared with the liner and puck, so those start partly hot: the "
                   "model begins with initial_extra_in_neighbours_kJ more heat than the pile's own content "
                   "(conservative). left_the_model is what has gone out through the outside surfaces and the outlet; "
                   "it must start at ~0 and only grow.")
    (HERE / "out" / f"energy_{case}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "times"}, indent=1))
    for r in out["times"]:
        if r["t_s"] in TH.FIELD_TIMES or r["t_s"] in (0.0, 0.5, 1.0, 5.0, 30.0):
            print(r)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "B_816")
