"""Evaporation and vapour-plume source terms from the melt-pool surface fields (issue #260; monitoring/melt-pool.md).

For each solved case (fv3d.py, via run_cases.py), from its surface temperature field T(x, y):
  - per-element evaporation mass flux, Hertz-Knudsen-Langmuir with 18 % recondensing (net 0.82; Anisimov 1968, Knight 1979,
    https://doi.org/10.2514/3.61171), partial pressures by Raoult's law over the bulk composition (props.py);
  - three surface-temperature readings, because the conduction model has a flat surface:
      "flat"   : the field as solved (its peak runs past the boiling point: an upper bound);
      "wall"   : capped at T_wall, where the recoil pressure 0.54 p_sat holds a depression of the beam's radius open against
                 the ambient and surface tension, 0.54 p_sat(T_wall) = p_amb + 2 sigma / r0 (the best estimate);
      "boil"   : capped at the alloy's 1 atm boiling point (a lower bound);
  - vapour exit state from Knight's jump conditions for a monatomic vapour leaving the hottest surface into 1 atm: Mach number
    (sonic once p_sat > 4.87 p_amb), temperature, velocity, density;
  - recoil pressure 0.54 p_sat at the peak (Anisimov 1968);
  - mass loss per mm of track, vapour molar composition, vapour volume flow at the exit state;
  - selective loss: the fraction of each element in the melted cross-section that leaves per pass, and the steady-state shift
    per layer, (m_dot_i / v) / (rho w_i h t) with hatch h 0.10 mm and layer t 30 um. Values above ~1 mean the estimate asks for
    more of the element than reaches the surface: the real loss is then set by mixing in the liquid, not by evaporation.

Run:  python evap.py      -> analysis/out/monitoring/melt/plume_source.json (keys documented in the file's "keys" block)
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np
from scipy.special import erfc

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import props as PR  # noqa: E402

OUT = HERE.parents[1] / "out" / "monitoring" / "melt"
RUNS = pathlib.Path("/tmp/melt_runs")
P_AMB = PR.ATM + 1500.0           # argon at +15 mbar (the chamber runs +5 to +20 mbar)
HATCH, LAYER = 0.10e-3, 30e-6
GAMMA = 5.0 / 3.0

# measured element loss in LPBF (fraction of the element's initial content), for calibration; all via Edison r8-melt-plume or
# heat.md (Velikajne 2026). The HKL estimate asks for far more Mg than reaches the surface, so these are the better rates.
MEASURED_LOSS = {
    "AlSi10Mg": dict(Mg=(0.57, "Li 2024 thesis (via Edison r8-melt-plume), https://doi.org/10.70675/5f083431z1407z40f1z83bfz19a675dc42f6")),
    "6061": dict(Mg=(0.17, "Li 2024 thesis (via Edison r8-melt-plume)")),
    "7075": dict(Mg=(0.12, "Velikajne et al. 2026, https://doi.org/10.3390/ma19050970 (~0.3 of 2.5 wt%; Li 2024 gives 19 %)"),
                 Zn=(0.18, "Velikajne et al. 2026 (~1 of 5.6 wt%; Li 2024 gives 3 %, others ~30 %)")),
}

KEYS = {
    "tag": "case name (alloy, power, speed, plate temperature)",
    "inputs": "alloy, P_W, v_m_s, spot_1e2_um, A (absorptivity), T0_K, f_M (Marangoni k factor)",
    "pool": "melt pool from fv3d.py: L/W/D um (liquidus), liquid cross-section mm2, T_peak_flat_K",
    "T_boil_1atm_K": "alloy's bubble point (Raoult, bulk composition)",
    "T_wall_K": "depression-wall temperature: 0.54 p_sat = p_amb + 2 sigma / r0",
    "readings": "per surface reading (flat / wall / boil): m_dot_kg_s per element and total, loss_ug_per_mm per element and "
                "total, vapour_mole_fraction, evap_power_W, area_hot_mm2 (where p_sat > p_amb), "
                "loss_fraction_per_pass and shift_per_layer_frac per element (see module docstring)",
    "measured": "per element: loss fraction measured in LPBF builds (source), and the mass rate it implies at this case's scan "
                "rate, m_dot = f w rho h t v (kg/s) and per mm of track (ug/mm): use these for Mg and Zn",
    "exit": "Knight jump at the hottest point of each reading: T_surface_K, p_sat_Pa, recoil_Pa (0.54 p_sat), mach, "
            "T_vapour_K, u_m_s, rho_vapour_kg_m3, M_vapour_g_mol, Q_vapour_m3_s (volume flow at the exit state, total)",
}


def knight(p_sat, T_s, M_w, p_amb=P_AMB):
    """Knight (1979) jump for evaporation into a back pressure p_amb: returns Mach, T_v, rho_v, u, net mass flux."""
    Rs = PR.R_GAS / M_w
    rho_s = p_sat / (Rs * T_s)
    g = (GAMMA - 1) / (GAMMA + 1)

    def state(M):
        m = M * math.sqrt(GAMMA / 2)
        tr = (math.sqrt(1 + math.pi * (g * m / 2) ** 2) - math.sqrt(math.pi) * g * m / 2) ** 2
        e = math.exp(m * m) * erfc(m)
        rr = math.sqrt(1 / tr) * ((m * m + 0.5) * e - m / math.sqrt(math.pi)) + 0.5 / tr * (1 - math.sqrt(math.pi) * m * e)
        return tr, rr

    if p_sat <= p_amb:
        return dict(mach=0.0, T_v=T_s, rho_v=rho_s, u=0.0, j=0.0)
    lo, hi = 1e-6, 1.0
    tr, rr = state(hi)
    if rr * tr * p_sat >= p_amb:          # choked: sonic at the Knudsen-layer edge
        M = 1.0
    else:
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            tr, rr = state(mid)
            if rr * tr * p_sat > p_amb:
                lo = mid
            else:
                hi = mid
        M = 0.5 * (lo + hi)
    tr, rr = state(M)
    T_v, rho_v = tr * T_s, rr * rho_s
    u = M * math.sqrt(GAMMA * Rs * T_v)
    return dict(mach=M, T_v=T_v, rho_v=rho_v, u=u, j=rho_v * u)


def T_wall(al, r0):
    target = (P_AMB + 2 * float(al.sigma(2500.0)) / r0) / 0.54
    return al.T_boil(target)


def reading(al, Ts, dA, v, A_cross, name):
    J = al.evap_flux(Ts)
    out = dict(m_dot_kg_s={}, loss_ug_per_mm={}, loss_fraction_per_pass={}, shift_per_layer_frac={})
    tot = 0.0
    nmol = {}
    wt = PR.ALLOYS[al.name]["wt"]
    for el, Ji in J.items():
        md = float((Ji * dA).sum())
        out["m_dot_kg_s"][el] = md
        out["loss_ug_per_mm"][el] = md / v * 1e6                  # kg/m -> ug/mm
        tot += md
        nmol[el] = md / PR.M[el]
        w = wt.get(el, 0.0) / 100.0
        if w > 0:
            out["loss_fraction_per_pass"][el] = (md / v) / (al.rho * w * A_cross) if A_cross > 0 else None
            out["shift_per_layer_frac"][el] = (md / v) / (al.rho * w * HATCH * LAYER)
    out["m_dot_kg_s"]["total"] = tot
    out["loss_ug_per_mm"]["total"] = tot / v * 1e6
    s = sum(nmol.values()) or 1.0
    out["vapour_mole_fraction"] = {el: n / s for el, n in nmol.items()}
    out["evap_power_W"] = float((al.evap_heat_flux(Ts) * dA).sum())
    out["area_hot_mm2"] = float(dA[al.p_total(Ts) > P_AMB].sum() * 1e6) if np.ndim(dA) else None
    return out


def case(row):
    c = row["case"]
    al = PR.Alloy(c["alloy"])
    d = np.load(RUNS / f"{c['tag']}.npz")
    xg, yg = d["xg"] * 1e-6, d["yg"] * 1e-6
    Ts = d["Ts"].astype(float)
    dA = np.full(Ts.shape, (xg[1] - xg[0]) * (yg[1] - yg[0]))
    # liquid cross-section at the widest section (y-z slice saved by run_cases)
    yc, zc, Tyz = d["yc"], d["zc"], d["T_yz"]
    dy = np.diff(np.concatenate([[0.0], 0.5 * (yc[1:] + yc[:-1]), [yc[-1] + 0.5 * (yc[-1] - yc[-2])]]))
    zf = np.concatenate([[0.0], 0.5 * (zc[1:] + zc[:-1]), [zc[-1] - 0.5 * (zc[-2] - zc[-1])]])
    dz = -np.diff(zf)
    A_cross = 2 * float((np.outer(dy, dz) * (Tyz >= al.T_liq)).sum())
    r0 = c["d_spot"] / 2
    v = c["v"]
    Tb, Tw = al.T_boil(P_AMB), T_wall(al, r0)
    res = dict(tag=c["tag"],
               inputs=dict(alloy=c["alloy"], P_W=c["P"], v_m_s=v, spot_1e2_um=c["d_spot"] * 1e6, A=c["A"], T0_K=c["T0"],
                           f_M=c["f_M"]),
               pool=dict(L_um=row["liquid"]["L"] * 1e6, W_um=row["liquid"]["W"] * 1e6, D_um=row["liquid"]["D"] * 1e6,
                         cross_section_mm2=A_cross * 1e6, T_peak_flat_K=row["T_peak"]),
               T_boil_1atm_K=Tb, T_wall_K=Tw, readings={}, exit={})
    res["measured"] = {}
    for el, (f, src) in MEASURED_LOSS.get(al.name, {}).items():
        w = PR.ALLOYS[al.name]["wt"][el] / 100.0
        md = f * w * al.rho * HATCH * LAYER * v
        res["measured"][el] = dict(loss_fraction=f, source=src, m_dot_kg_s=md, loss_ug_per_mm=md / v * 1e6)
    for name, Tcap in (("flat", None), ("wall", Tw), ("boil", Tb)):
        T = Ts if Tcap is None else np.minimum(Ts, Tcap)
        res["readings"][name] = reading(al, T, dA, v, A_cross, name)
        Tpk = float(T.max())
        pp = al.partial_pressures(Tpk)
        p_sat = sum(pp.values())
        M_w = sum(pp[el] * PR.M[el] for el in pp) / p_sat
        kn = knight(p_sat, Tpk, M_w)
        md = res["readings"][name]["m_dot_kg_s"]["total"]
        res["exit"][name] = dict(T_surface_K=Tpk, p_sat_Pa=p_sat, recoil_Pa=0.54 * p_sat, mach=kn["mach"], T_vapour_K=kn["T_v"],
                                 u_m_s=kn["u"], rho_vapour_kg_m3=kn["rho_v"], M_vapour_g_mol=M_w * 1e3,
                                 Q_vapour_m3_s=(md / kn["rho_v"]) if kn["rho_v"] > 0 and kn["u"] > 0 else None)
    return res


def main():
    log = OUT / "fv_cases.jsonl"
    rows = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
    seen, out = set(), []
    for r in rows[::-1]:
        t = r["case"]["tag"]
        if t in seen or not (RUNS / f"{t}.npz").exists() or t.startswith(("sens_", "val_")):
            continue
        seen.add(t)
        out.append(case(r))
    out.sort(key=lambda d: d["tag"])
    doc = dict(about="Evaporation and plume source terms per melt-pool operating point (evap.py; melt-pool.md section 5). "
                     "Upper bound 'flat', best estimate 'wall', lower bound 'boil'. HKL with Raoult activities over the bulk "
                     "composition: Mg and Zn depletion at the surface is not modelled, so element losses are upper bounds.",
               p_amb_Pa=P_AMB, hatch_m=HATCH, layer_m=LAYER, keys=KEYS, cases=out)
    (OUT / "plume_source.json").write_text(json.dumps(doc, indent=1, default=float))
    for d in out:
        w = d["readings"]["wall"]
        e = d["exit"]["wall"]
        print(f"{d['tag']:34s} Tpk {d['pool']['T_peak_flat_K']:5.0f} Tw {d['T_wall_K']:5.0f} | wall: {w['loss_ug_per_mm']['total']:7.3f} ug/mm "
              f"P_ev {w['evap_power_W']:5.2f} W  shift/layer " + " ".join(f"{k} {v:.2f}" for k, v in w['shift_per_layer_frac'].items()
                                                                           if k in ('Mg', 'Zn', 'Al'))
              + f" | exit M {e['mach']:.2f} u {e['u_m_s']:5.0f} m/s Tv {e['T_vapour_K']:5.0f}  x " +
              " ".join(f"{k} {v:.2f}" for k, v in w['vapour_mole_fraction'].items() if v > 0.01))


if __name__ == "__main__":
    main()
