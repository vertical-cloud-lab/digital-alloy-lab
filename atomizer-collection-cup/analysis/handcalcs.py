"""Closed-form checks for the lab-built cups (textbook formulas, each with its source), and the numbers
taken from the FEA results where a check needs a temperature.

    python analysis/handcalcs.py      # writes analysis/out/handcalcs.{json,md}

Sources:
- Roark's Formulas for Stress and Strain, 8th ed. (Young & Budynas): thin cylinders (Table 13.1),
  flat circular plates under uniform pressure (Table 11.2, cases 10a and 10b).
- ASME BPVC VIII-1 UG-27 (shells under internal pressure), UG-34 (unstayed flat heads), UG-28 / the
  Windenburg-Trilling short-cylinder collapse formula (external pressure).
- Shigley's Mechanical Engineering Design, 10th ed.: power-screw/bolt torque (T = K F d, K ~ 0.2),
  gasketed-joint bolt load.
- V-band / wedge clamp axial force: F_ax = 2 pi T / tan(theta + phi) (radial band load T/R per unit
  length acting on a flank at theta, friction angle phi), as in NASA TM-2006-214468-style V-band analyses.
- Glass thermal stress: sigma = E alpha dT / (1 - nu) (fully restrained surface; Kingery 1955).
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import params as P  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)


def main():
    b, kf = P.B, P.JOINT
    R = {}
    p_des = P.P_DESIGN_INT / 10.0          # bar -> MPa
    p_run = P.P_RUN_G / 10.0
    p_ext = P.P_DESIGN_EXT / 10.0
    S_allow = 115.0                          # MPa, 316L allowable stress (ASME II-D) up to ~300 C
    E = 193000.0
    nu = 0.3

    # 1. shells under internal pressure (UG-27 / Roark thin cylinder)
    shells = {}
    for name, D, t in (("B body 3 in x 0.065", b["body_od"], b["body_wall"]),
                       ("B stub / A nipple 2 in x 0.065", kf.tube_od, kf.tube_wall)):
        r_in = D / 2 - t
        hoop = p_des * r_in / t
        t_req = p_des * r_in / (S_allow * 1.0 - 0.6 * p_des)       # UG-27(c)(1), joint efficiency 1
        shells[name] = dict(hoop_MPa=round(hoop, 2), axial_MPa=round(hoop / 2, 2), t_required_mm=round(t_req, 3),
                            t_actual_mm=t, margin=round(t / t_req, 0))
    R["internal_pressure_shells"] = dict(p_design_MPa=p_des, rows=shells)

    # 2. flat bottom (Roark 11.2 10a/10b; UG-34 with C = 0.33)
    a = b["body_od"] / 2 - b["body_wall"]
    t = b["bottom_t"]
    ss = 3 * (3 + nu) * p_des * a ** 2 / (8 * t ** 2)
    fx = 3 * p_des * a ** 2 / (4 * t ** 2)
    t_ug34 = 2 * a * math.sqrt(0.33 * p_des / S_allow)
    w_ss = 3 * (1 - nu) * (5 + nu) * p_des * a ** 4 / (16 * E * t ** 3) * (1 - nu ** 2) / (1 - nu ** 2)
    R["flat_bottom"] = dict(a_mm=a, t_mm=t, sigma_simply_supported_MPa=round(ss, 2), sigma_fixed_edge_MPa=round(fx, 2),
                            t_required_UG34_mm=round(t_ug34, 2), centre_deflection_ss_um=round(w_ss * 1000, 2))

    # 3. external pressure (vacuum): Windenburg-Trilling short cylinder and the long-tube limit
    rows = {}
    for name, D, t_, L in (("B body", b["body_od"], b["body_wall"], b["body_len"] - b["stub_len"] - b["reducer_len"]),
                           ("A nipple", kf.tube_od, kf.tube_wall, P.A["nipple_len"])):
        for T, E_T in ((25, 193000.0), (400, 166000.0)):
            pcr_wt = 2.42 * E_T * (t_ / D) ** 2.5 / ((1 - nu ** 2) ** 0.75 * (L / D - 0.45 * (t_ / D) ** 0.5))
            pcr_long = 2 * E_T / (1 - nu ** 2) * (t_ / D) ** 3
            rows[f"{name} at {T} C"] = dict(L_mm=round(L, 1), Pcr_short_MPa=round(pcr_wt, 2),
                                            Pcr_long_tube_MPa=round(pcr_long, 2),
                                            safety_factor_vs_1bar=round(pcr_wt / p_ext, 0))
    R["external_pressure"] = rows

    # 4. KF joint: separating force vs the clamp's axial force (wedge on the 15 deg back taper)
    d_seal = kf.ring_od + 4.9                  # O-ring mean diameter, mm
    A_seal = math.pi / 4 * d_seal ** 2
    F_oring = 25.0 * math.pi * d_seal / 10.0   # O-ring squeeze, ~25 N per cm of a 5 mm Shore-75 ring at 20 %
    W_cup = 6.0 * 9.81                          # cup + liner + puck + 1.1 kg of powder, generous
    seps = {}
    for lab, p in (("run +0.15 bar", p_run), ("relief +0.8 bar", P.P_RELIEF_G / 10), ("design +1.2 bar", p_des)):
        seps[lab] = round(p * A_seal + F_oring + W_cup, 0)
    theta, phi = math.radians(kf.taper_deg), math.atan(0.15)
    clamp = {}
    for lab, torque in (("finger-tight 0.3 N m", 0.3), ("snug 1.0 N m", 1.0)):
        T_bolt = torque / (0.2 * 6e-3)             # M6 wing screw, K = 0.2 (Shigley 8-27)
        F_ax = 2 * math.pi * T_bolt / math.tan(theta + phi) / (2 * math.pi) * math.pi   # two half-shells
        clamp[lab] = dict(bolt_tension_N=round(T_bolt, 0), axial_clamp_N=round(F_ax, 0))
    R["kf_joint"] = dict(seal_diameter_mm=round(d_seal, 1), separating_force_N=seps, clamp=clamp,
                         note="Two-segment clamp: radial load = pi * T for a band tension T; axial = radial / "
                              "tan(theta + phi). The vendor's own overpressure rating governs (bom/README.md).")

    # 5. weld at the floor: shear of a full-penetration butt weld carrying the floor's pressure load
    R["bottom_weld"] = dict(shear_MPa=round(p_des * a / (2 * b["body_wall"]), 2),
                            note="Floor load p*pi*a^2 over the weld's ring area 2*pi*a*t")

    # 6. glass thermal stress per kelvin of surface-to-bulk difference
    glass = {}
    for nm, E_g, a_g, nu_g, s_short, s_des in (("borosilicate 3.3", 64000, 3.3e-6, 0.20, 40, 6),
                                                ("fused quartz", 72000, 0.55e-6, 0.17, 50, 7)):
        k = E_g * a_g / (1 - nu_g)
        glass[nm] = dict(MPa_per_K=round(k, 4), dT_to_short_term_K=round(s_short / k, 0),
                         dT_to_design_K=round(s_des / k, 0),
                         stress_at_850K_step_MPa=round(k * 850, 0))
    R["glass_thermal_stress"] = glass

    # 7. tie rods for option C: the load that seats the glass gaskets and holds +1.2 bar
    s = P.STOCK
    g_out, g_in = s["glass_od"] / 2 + 1.5, s["glass_od"] / 2 - s["glass_wall"] - 1.5
    A_g = math.pi * (g_out ** 2 - g_in ** 2)
    y_seat = 1.4                                   # MPa, ASME Table 2-5.1 y for soft elastomer (200 psi)
    m_fac = 0.5
    W = y_seat * A_g + m_fac * p_des * A_g + p_des * math.pi * g_in ** 2
    n = s["n_tie"]
    At = 84.3                                       # mm2, M12 tensile stress area
    glass_area = math.pi * ((s["glass_od"] / 2) ** 2 - (s["glass_od"] / 2 - s["glass_wall"]) ** 2)
    R["tie_rods_C"] = dict(gasket_area_mm2=round(A_g, 0), total_load_N=round(W, 0), per_rod_N=round(W / n, 0),
                           rod_stress_MPa=round(W / n / At, 1), glass_end_compression_MPa=round(W / glass_area, 2),
                           torque_per_rod_Nm=round(0.2 * W / n * 0.012, 2))

    # 8. thermal growth of the liner and puck against the vessel (from the thermal FEA fields)
    R["clearances"] = clearance_from_fea()

    (OUT / "handcalcs.json").write_text(json.dumps(R, indent=1) + "\n")
    md = ["# Hand calculations\n", "Each block names its formula and source in `handcalcs.py`.\n"]
    for k, v in R.items():
        md.append(f"## {k}\n\n```json\n{json.dumps(v, indent=1)}\n```\n")
    (OUT / "handcalcs.md").write_text("\n".join(md))
    print(json.dumps(R, indent=1))


def clearance_from_fea():
    """Radial clearance between the liner/puck and the vessel bore at each saved time of B_816 (mm)."""
    try:
        import axifea as F
        import thermal as TH
    except Exception:  # noqa: BLE001
        sys.path.insert(0, str(HERE))
        import axifea as F
        import thermal as TH
    d = TH.OUT / "B_816" / "pass2.frd"
    if not d.exists():
        return "run thermal.py first"
    spec = TH.CASES["B_816"]
    regs, cav, probes, info = TH.DESIGNS["B"](spec[1], **spec[2])
    for r in regs:
        r.size *= TH.MESH_SCALE
    m = F.build_mesh(regs, order=1)
    frd = [(t, v) for t, v in F.read_frd(d) if t is not None and min(abs(t - ft) for ft in TH.FIELD_TIMES) < 1e-3]
    b = P.B
    a304 = lambda T: (17.3 + 0.0035 * (T - 20)) * 1e-6          # mean CTE from 20 C
    a316 = lambda T: (16.0 + 0.0035 * (T - 20)) * 1e-6
    out = []
    R_i = b["body_od"] / 2 - b["body_wall"]
    for t, vals in frd:
        def mean_T(reg):
            ns = m.region_nodes(reg)
            return float(np.mean([vals[n][0] for n in ns]))
        has_liner = bool(m.elset("liner"))
        T_l = mean_T("liner") if has_liner else None
        T_p, T_v = mean_T("puck"), mean_T("vessel")
        # vessel bore at the puck: use the vessel's mean temperature (conservative: it is hotter at the floor)
        grow_v = R_i * a316(T_v) * (T_v - 20)
        gap_puck = (R_i - b["puck_d"] / 2) + grow_v - b["puck_d"] / 2 * a304(T_p) * (T_p - 20)
        rec = dict(t_s=t, T_puck=round(T_p), T_vessel=round(T_v), puck_gap_mm=round(gap_puck, 3))
        if has_liner:
            rec.update(T_liner=round(T_l), liner_gap_mm=round(
                (R_i - b["liner_od"] / 2) + grow_v - b["liner_od"] / 2 * a304(T_l) * (T_l - 20), 3))
        # the puck must still pass the KF bore (47.5) when it is taken out cold; hot it only has to sit loose
        # the puck and liner must pass the opening they go in through: the pot's ferrule bore (split) or the KF neck
        opening = (b["body_od"] - 2 * b["body_wall"]) if b.get("split") else P.JOINT.bore
        rec["puck_clear_of_opening_mm"] = round(opening - b["puck_d"], 2)
        rec["liner_clear_of_opening_mm"] = round(opening - b["liner_od"], 2)
        out.append(rec)
    return out


if __name__ == "__main__":
    main()
