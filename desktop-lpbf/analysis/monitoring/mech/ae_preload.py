"""The AE waveguide's preload and cold end (issue #260, PR 281; monitoring/mechanics.md §4 and Checks §6).

The design (drawn by cad/monitoring_parts.py `_ae()`, numbers in its `AE_CART`): a Ø3 mm 316 waveguide slides free in its holes
from the plate's spigot down the hollow rod. Its top is a Ø4 head with a domed face; its foot sits on a miniature AE sensor
inside a 316L cartridge that stands on the rod end's bore floor, in the argon. A compression spring under the sensor pushes
sensor and waveguide up, so the force on the plate is set by the spring, not by thermal growth or the plate's seating. A cap on
the cartridge stops the sensor when the plate is off. The sensor's lead runs up the rod to a micro coax plug, and back down to a
weld-in coaxial feedthrough on the rod end's back face, whose inner end opens into the rod end's cross-drilling.

This script checks, for M50 (L75 has the same rod, rod end and stack):
  1. the spring's working stroke: the waveguide's and the stack's thermal growth (thermal.json's M50 cases: 200 C, powder in the
     gaps, 500 C tier B), the plate-to-plate seating tolerance, the set pre-travel, and the spring's own tolerances, against
     10-20 N on the plate at every corner;
  2. the spring itself: solid-height margin, shear stress against 302 stainless's allowable, buckling;
  3. the tip: Hertz pressure of the domed head on 6061 at 200 C against its yield there, and the twist of the bayonet under it;
  4. the acoustic loss of the new path (tip contact with its couplant, Al to 316, the rod, the cold end on the sensor) against the
     rod-end route's 26-52 dB (checks.json);
  5. the sensor's temperature (fin equation to the foot, as mech_monitoring.py check 6) against its rating;
  6. what the force does to the plate's bayonet (hot-swap.md: bare, or with the 97125K111 disc spring) and to the plate swap;
  7. the waveguide as a column.

Run:  /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/mech/ae_preload.py
Writes analysis/out/monitoring/mech/ae_preload.json and ae_preload.md.
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mech_inputs as MI  # noqa: E402
import mech_monitoring as MM  # noqa: E402  (fin_profile, h_annulus)

MP = MI.MP
ROOT = MI.ROOT
OUT = ROOT / "analysis" / "out" / "monitoring" / "mech"
sys.path.insert(0, str(ROOT / "cad"))
import modules_low as ML  # noqa: E402
import monitoring_parts as MPT  # noqa: E402  (AE_CART: the drawn design)

A = MPT.AE_CART
T_ASSEMBLY = 20.0

# ------------------------------------------------------------------------------------------------ bought parts (read on vendor pages)
PARTS = MPT.AE_PARTS

# ------------------------------------------------------------------------------------------------ materials
SS = MI.SS316
AL = dict(MI.AL6061)
AL_200 = dict(E=62_000.0, nu=0.33, sy_hot=103.0,
              src="6061-T6 at 200 C: E 62 GPa (hot-swap FEA, fea_hotswap.md); ~103 MPa yield after 10,000 h at 204 C, 77 MPa at "
                  "225 C (ASM, as hot-swap.md §3.1 uses)")
MACOR_ALPHA = 9.3e-6           # Corning Macor datasheet: 9.3 ppm/K (25-300 C)
SENSOR_ALPHA = 8.0e-6          # assumed: PZT element (2-6 ppm/K) in a stainless case (17); only its 4 mm height counts
S302 = dict(G=69_000.0, alpha=17.3e-6, tau_allow_frac=0.45,
            src="302 stainless spring wire: G 69 GPa (10.0 Mpsi); allowable static shear 45 % of tensile for set-removed "
                "compression springs (Shigley Table 10-6 / Associated Spring practice)")
GREASE = dict(K=1.0e9, h_min_um=1.0, h_flat_um=(2.0, 10.0),
              src="couplant film: bulk modulus ~1 GPa for a PFPE or silicone grease (assumed); minimum film 1 um (the surfaces' "
                  "roughness); a flat greased joint at 10-20 N squeezes to 2-10 um (assumed)")
RUB_DB = (0.0, 1.0)            # the guide touching its holes and the leads in the rod: not estimated, taken as 0-1 dB (assumed)
TOL = dict(delta0=0.10, plate=0.10, L0_frac=0.02, k_frac=0.10,
           src="pre-travel set at assembly to +/-0.10 mm (lap the waveguide to length against a depth gauge from the socket floor); "
               "plate to plate +/-0.10 mm (spigot length +/-0.05 machined, graphite foil +/-0.05); spring free length +/-2 % and rate "
               "+/-10 % (typical catalogue tolerances, assumed)")


def zlev():
    z = ML.zlevels()
    zc = z["zc"]
    zt = z["zb1"] - 4.0                                    # the plate spigot's underside (tip contact), plate on
    seat = zc + A["seat_z"]                                # spring seat (cartridge floor's top)
    cap = seat + A["spring_L_stop"] + A["sensor_h"]        # cap's underside = the sensor's face at the stop
    foot_on = cap - A["delta0"]                            # foot with the plate on
    return dict(z=z, zc=zc, z_tip=zt, seat=seat, cap=cap, foot_on=foot_on, wg_len=zt - foot_on - A["head_t"],
                head_bottom_on=zt - A["head_t"] - A["dome_h"])


# ============================================================================================ 1. thermal growth and the stroke
def rod_profile(t, case, z_lo, z_hi, n=200):
    """the rod's temperature between z_lo and z_hi (piston frame, plate top = 0): T_head at the head's clamp, T_rod_at_gland at the
    gland (z -99 at the start of a build, 40 mm higher at the end), T_rod_end at the rod end"""
    zg = -99.0 + (40.0 if "_end" in case else 0.0)
    pts = sorted([(-46.0, t["T_head"]), (zg, t["T_rod_gland"]), (ML.zlevels()["zc"] + MP.ROD_END_T, t["T_rod_end"])])
    zs = [z_lo + (z_hi - z_lo) * i / n for i in range(n + 1)]
    out = []
    for zz in zs:
        if zz <= pts[0][0]:
            out.append(pts[0][1])
        elif zz >= pts[-1][0]:
            out.append(pts[-1][1])
        else:
            for (za, ta), (zb, tb) in zip(pts, pts[1:]):
                if za <= zz <= zb:
                    out.append(ta + (tb - ta) * (zz - za) / (zb - za))
                    break
    return zs, out


def grow(alpha, L, T):
    return alpha * L * (T - T_ASSEMBLY)


def wg_fin(t, L):
    """fin profile of the waveguide from the tip (plate temperature) to the foot, as mech_monitoring check 6, with the rod segment
    cut at the foot; returns (z from tip mm, T)"""
    d = A["wg_d"]
    rod_seg = L - (MP.BLOCK_T + MP.BREAK_T + MP.HEAD_T)
    segs = [(MP.BLOCK_T, t["T_block"], t["T_block"], MM.h_annulus(d / 2, d / 2 + 0.2, t["T_block"], gas_k=0.024)),
            (MP.BREAK_T, t["T_block"], t["T_head"], MM.h_annulus(d / 2, 4.0, (t["T_block"] + t["T_head"]) / 2, gas_k=0.022)),
            (MP.HEAD_T, t["T_head"], t["T_head"], MM.h_annulus(d / 2, d / 2 + 0.5, t["T_head"], gas_k=0.02)),
            (rod_seg, t["T_rod_gland"], t["T_rod_end"], MM.h_annulus(d / 2, MP.ROD_ID / 2, (t["T_rod_gland"] + t["T_rod_end"]) / 2))]
    z, T, Ts = MM.fin_profile(segs, t["T_plate"], d)
    return z, T


def stroke_cases():
    g = zlev()
    temps = MI.module_temps()
    keep = [k for k in temps if k.startswith("M50") and k.split("_")[1] in ("start", "end") and
            ("_e0.5" in k or "powder" in k or "tierB" in k) and not any(s in k for s in ("scr", "_h2", "mesh", "clear"))]
    rows = []
    for case in keep:
        t = temps[case]
        Tm = (t["T_block"] + t["T_head"]) / 2
        # the loop from the spring seat to the tip contact, through the stack
        zs, Tr = rod_profile(t, case, g["zc"] + MP.ROD_END_T, -46.0)
        L_rod = -46.0 - (g["zc"] + MP.ROD_END_T)
        dL_rod = sum(SS["alpha"] * (L_rod / (len(Tr) - 1)) * (0.5 * (a + b) - T_ASSEMBLY) for a, b in zip(Tr, Tr[1:]))
        L_rodend = MP.ROD_END_T - A["floor_z"]
        dL = dict(block=grow(AL["alpha"], MP.BLOCK_T, t["T_block"]),
                  spigot=-grow(AL["alpha"], 4.0, t["T_plate"]),
                  macor=grow(MACOR_ALPHA, MP.BREAK_T, Tm),
                  head=grow(AL["alpha"] if "tierB" not in case else SS["alpha"], 14.0, t["T_head"]),
                  rod=dL_rod,
                  rod_end=grow(SS["alpha"], L_rodend, t["T_rod_end"]),
                  cartridge=-grow(SS["alpha"], A["seat_z"] - A["floor_z"], t["T_rod_end"]))
        loop = sum(dL.values())
        L_wg = g["wg_len"] + A["head_t"]
        z, T = wg_fin(t, L_wg)
        dz = (z[1] - z[0])
        dL_wg = sum(SS["alpha"] * dz * (0.5 * (a + b) - T_ASSEMBLY) for a, b in zip(T, T[1:]))
        dL_sensor = grow(SENSOR_ALPHA, A["sensor_h"], t["T_rod_end"])
        d_spring = loop - dL_wg - dL_sensor          # + = the spring gets longer (less force)
        rows.append(dict(case=case, T_plate=t["T_plate"], T_block=t["T_block"], T_head=t["T_head"], T_rod_end=t["T_rod_end"],
                         loop_growth_mm=loop, parts_mm=dL, waveguide_growth_mm=dL_wg, sensor_growth_mm=dL_sensor,
                         spring_length_change_mm=d_spring, T_foot=float(T[-1])))
    return rows


# ============================================================================================ 2. spring: force window and stress
def spring_check(rows):
    k, L0, Ls, Lsolid = A["spring_k"], A["spring_L0"], A["spring_L_stop"], A["spring_L_solid"]
    d, Dm = A["spring_wire"], A["spring_od"] - A["spring_wire"]
    d0 = A["delta0"]
    thermal = [r["spring_length_change_mm"] for r in rows]
    corners = []
    for dd0, dpl, dth, fL0, fk in itertools.product((-TOL["delta0"], TOL["delta0"]), (-TOL["plate"], TOL["plate"]),
                                                    (min(thermal), max(thermal), 0.0), (-TOL["L0_frac"], TOL["L0_frac"]),
                                                    (-TOL["k_frac"], TOL["k_frac"])):
        L0_ = L0 * (1 + fL0)
        k_ = k * (1 + fk)
        comp = (L0_ - Ls) + (d0 + dd0 + dpl) - dth          # compression with the plate on
        corners.append(dict(F=k_ * comp, comp=comp, L=L0_ - comp, d0=d0 + dd0, plate=dpl, thermal=dth, L0=L0_, k=k_))
    F = [c["F"] for c in corners]
    Fstop = [k * (1 + fk) * (L0 * (1 + fL0) - Ls) for fL0 in (-TOL["L0_frac"], TOL["L0_frac"]) for fk in (-TOL["k_frac"], TOL["k_frac"])]
    L_min = min(c["L"] for c in corners)
    C = Dm / d
    Kw = (4 * C - 1) / (4 * C - 4) + 0.615 / C
    tau = [Kw * 8 * f * Dm / (math.pi * d ** 3) for f in (max(F), k * (L0 - Lsolid))]
    su = A["spring_su_MPa"]
    nom = k * ((L0 - Ls) + d0)
    return dict(k_N_per_mm=k, L0_mm=L0, L_stop_mm=Ls, L_solid_mm=Lsolid, F_stop_N=(min(Fstop), max(Fstop)),
                F_nominal_N=nom, F_range_N=(min(F), max(F)), pass_window=min(F) >= 10.0 and max(F) <= 20.0,
                min_length_mm=L_min, margin_to_solid_mm=L_min - Lsolid, index_C=C, wahl_K=Kw,
                tau_at_Fmax_MPa=tau[0], tau_solid_MPa=tau[1], tau_allow_MPa=S302["tau_allow_frac"] * su,
                pass_stress=tau[0] <= S302["tau_allow_frac"] * su, safe_at_solid=tau[1] <= S302["tau_allow_frac"] * su,
                thermal_range_mm=(min(thermal), max(thermal)), corners=len(corners), src=S302["src"])


# ============================================================================================ 3. tip: Hertz and the bayonet twist
def hertz(R, F, E1, nu1, E2, nu2):
    Es = 1 / ((1 - nu1 ** 2) / E1 + (1 - nu2 ** 2) / E2)
    a = (3 * F * R / (4 * Es)) ** (1 / 3)
    p0 = 3 * F / (2 * math.pi * a ** 2)
    return a, p0, Es


def tip_check(F_range):
    out = []
    for R in (25.0, 50.0, 100.0):
        for F in (F_range[0], F_range[1], 20.0):
            a, p0, Es = hertz(R, F, SS["E"], SS["nu"], AL_200["E"], AL_200["nu"])
            out.append(dict(R_mm=R, F_N=F, contact_d_um=2 * a * 1e3, p0_MPa=p0, limit_MPa=1.6 * AL_200["sy_hot"],
                            yields_hot_6061=p0 > 1.6 * AL_200["sy_hot"]))
    return out


# ============================================================================================ 4. acoustic loss of the path
def contact_T_dB(f, k):
    Zm = SS["rho"] * math.sqrt(SS["E"] * 1e6 / SS["rho"]) * math.pi * (A["wg_d"] * 1e-3) ** 2 / 4
    x = 2 * math.pi * f * Zm / (2 * k)
    return -10 * math.log10(1 + x ** 2), Zm


def dome_stiffness(R_mm, F, greased):
    a, p0, Es = hertz(R_mm, F, SS["E"], SS["nu"], AL_200["E"], AL_200["nu"])
    kh = 2 * a * 1e-3 * Es * 1e6                                   # Hertz normal contact stiffness (N/m)
    kf = 0.0
    if greased:                                                    # grease film round the contact: dk = K dA / h(r), h = h0 + r^2 / 2R
        R = R_mm * 1e-3
        h0 = GREASE["h_min_um"] * 1e-6
        rmax = A["head_d"] / 2 * 1e-3
        a_ = a * 1e-3
        kf = 2 * math.pi * R * GREASE["K"] * math.log((h0 + rmax ** 2 / (2 * R)) / (h0 + a_ ** 2 / (2 * R)))
    return kh + kf, kh, kf


def loss_budget(F_range):
    att = [a * (zlev()["wg_len"] + A["head_t"]) * 1e-3 for a in MI.AE["attenuation_316_dB_per_m"]]
    Z = MI.AE["Z_MRayl"]
    al316 = -10 * math.log10(4 * Z["6061"] * Z["316"] / (Z["6061"] + Z["316"]) ** 2)
    freqs = (100e3, 300e3, 500e3)
    tip, tip_dry, cold = [], [], []
    for f in freqs:
        ks = [dome_stiffness(A["dome_R"], F, True)[0] for F in F_range]
        kd = [dome_stiffness(A["dome_R"], F, False)[0] for F in F_range]
        tip.append(dict(f_kHz=f / 1e3, dB=[contact_T_dB(f, k)[0] for k in ks], k_N_per_m=ks))
        tip_dry.append(dict(f_kHz=f / 1e3, dB=[contact_T_dB(f, k)[0] for k in kd], k_N_per_m=kd))
        kc = [GREASE["K"] * math.pi * (A["wg_d"] * 1e-3) ** 2 / 4 / (h * 1e-6) for h in GREASE["h_flat_um"]]
        cold.append(dict(f_kHz=f / 1e3, dB=[contact_T_dB(f, k)[0] for k in kc], k_N_per_m=kc))
    worst = lambda rows: max(abs(min(r["dB"])) for r in rows)   # noqa: E731
    best = lambda rows: min(abs(max(r["dB"])) for r in rows)    # noqa: E731
    # the budget: each item (low, high) in dB over 100-500 kHz; the contacts' model values with Edison's couplant range on top
    hi_g = MI.AE["interface_dB"]["greased"][1]                    # a greased contact: the model, up to the 3 dB check 6 used (Edison)
    budget = dict(tip_dome_greased=(best(tip), max(worst(tip), hi_g)), Al_to_316=(al316, al316), waveguide_attenuation=tuple(att),
                  rubbing_in_holes=RUB_DB, cold_end_greased=(best(cold), max(worst(cold), hi_g)))
    tot = (sum(v[0] for v in budget.values()), sum(v[1] for v in budget.values()))
    chk = json.loads((OUT / "checks.json").read_text()) if (OUT / "checks.json").exists() else None
    rod_end = tuple(chk["6"]["total_rod_end_dB"]) if chk else (26.0, 52.0)
    old_wg = tuple(chk["6"]["total_waveguide_dB"]) if chk else (3.0, 9.0)
    dry = (best(tip_dry) + al316 + att[0] + best(cold), worst(tip_dry) + al316 + att[1] + RUB_DB[1] + max(worst(cold), hi_g))
    return dict(freqs_kHz=[f / 1e3 for f in freqs], tip=tip, tip_dry=tip_dry, cold=cold, budget_dB=budget, total_dB=tot,
                tier_b_dry_tip_total_dB=dry, rod_end_route_dB=rod_end, previous_waveguide_budget_dB=old_wg,
                gain_over_rod_end_dB=(rod_end[0] - tot[1], rod_end[1] - tot[0]), src=GREASE["src"],
                method="contacts as normal springs between two rods of the waveguide's impedance (mech_monitoring check 6): a Hertz "
                       "dome plus the couplant film round it (dk = K dA / h, h = h0 + r^2/2R out to the head's edge); the flat cold end "
                       "as a film K A / h; impedance step Al/316 at normal incidence; attenuation 0.1-0.5 dB/m")


# ============================================================================================ 5. temperatures
def temperatures(rows):
    out = []
    for r in rows:
        out.append(dict(case=r["case"], T_plate=r["T_plate"], T_rod_end=r["T_rod_end"], T_sensor_max=r["T_foot"],
                        margin_C=PARTS["sensor"]["t_max_C"] - r["T_foot"]))
    return out


# ============================================================================================ 6. the plate and its swap
def plate_check(F_range):
    jc = json.loads((ROOT / "analysis" / "out" / "hotswap" / "joint_calcs.json").read_text())
    out = {}
    for key in ("M50", "L75"):
        p = jc["plate"][key]
        clamp = p["bayonet_springs"]["target_N"]
        out[key] = dict(weight_N=p["W"], bare_lift_mm=p["bare_lift_mm"], foil_needs_N=p["F_req"], disc_spring_clamp_N=clamp,
                        left_on_foil_N=(clamp - F_range[1], clamp - F_range[0]), still_meets_foil=clamp - F_range[1] >= p["F_req"],
                        lifts_bare_plate=F_range[0] > p["W"], twist_Nm=p["bayonet_springs"]["T_twist_Nm"],
                        ae_twist_Nmm=0.15 * F_range[1] * A["wg_r"], drawbar_clamp_N=p["drawbar"]["F_clamp"])
    out["push_to_seat_N"] = F_range[1]
    out["src"] = "analysis/out/hotswap/joint_calcs.json (hot-swap.md §3.1): plate weight, bare lift, foil's 0.1 MPa, the 97125K111 target"
    return out


# ============================================================================================ 7. the waveguide as a column
def column_check(F_range):
    L = zlev()["wg_len"]
    I = math.pi * A["wg_d"] ** 4 / 64
    Pcr = math.pi ** 2 * SS["E"] * I / L ** 2           # pinned-pinned, no help from the holes
    return dict(length_mm=L, P_cr_N=Pcr, ratio=Pcr / F_range[1])


# ============================================================================================ report
def write_md(R):
    g, s, lb = R["geometry"], R["spring"], R["loss"]
    P = PARTS
    L = ["# AE waveguide preload and cold end (generated by `analysis/monitoring/mech/ae_preload.py`)\n",
         f"Run {R['run_utc']} UTC. M50 thermal cases from thermal.json; L75 has the same rod, rod end and stack. Design numbers from "
         "`cad/monitoring_parts.py` `AE_CART`, parts from `AE_PARTS` (each with its vendor page and read time).\n",
         "## Geometry (plate top at z 0, M50)\n",
         "| Item | Value |", "|---|---|",
         f"| tip contact (spigot underside) | z {g['z_tip']:.2f} |",
         f"| rod end coupling face zc | z {g['zc']:.1f} |",
         f"| spring seat (cartridge floor) | zc + {A['seat_z']:.1f} = z {g['seat']:.2f} |",
         f"| sensor face at the stop (plate off) | z {g['cap']:.2f} |",
         f"| waveguide foot, plate on | z {g['foot_on']:.2f} |",
         f"| waveguide shaft below the head | {g['wg_len']:.1f} mm (+ {A['head_t']:.1f} mm head) |",
         f"| pre-travel with the plate off (head above the seated spigot) | {A['delta0']:.2f} mm |",
         f"| head's underside above its counterbore floor, plate on | {g['head_clear_on']:.2f} mm |", "",
         "## 1. Thermal growth: change in the spring's length from assembly (20 °C), mm (+ = longer, less force)\n",
         "| Case | Plate | Block | Head | Rod end | Stack loop | Waveguide | Spring | Sensor (foot) °C |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in R["stroke"]:
        L.append(f"| {r['case']} | {r['T_plate']:.0f} | {r['T_block']:.0f} | {r['T_head']:.0f} | {r['T_rod_end']:.0f} | "
                 f"{r['loop_growth_mm']:+.3f} | {r['waveguide_growth_mm']:+.3f} | {r['spring_length_change_mm']:+.3f} | {r['T_foot']:.0f} |")
    L += ["",
          "## 2. Spring\n",
          f"{P['spring']['vendor']} {P['spring']['pn']}: {P['spring']['desc']} ([page]({P['spring']['url']}), read {P['spring']['read_utc']}).\n",
          "| Quantity | Value |", "|---|---|",
          f"| rate | {s['k_N_per_mm']:.2f} N/mm |",
          f"| free / at the stop / solid | {s['L0_mm']:.2f} / {s['L_stop_mm']:.2f} / {s['L_solid_mm']:.2f} mm |",
          f"| force at the stop, plate off | {s['F_stop_N'][0]:.1f}-{s['F_stop_N'][1]:.1f} N |",
          f"| force on the plate, nominal | {s['F_nominal_N']:.1f} N |",
          f"| force on the plate over {s['corners']} tolerance corners | **{s['F_range_N'][0]:.1f}-{s['F_range_N'][1]:.1f} N** "
          f"({'inside' if s['pass_window'] else 'OUTSIDE'} 10-20 N) |",
          f"| the same, with the stop force set at assembly (shim, push gauge: 12.5 ± 0.5 N) | {s['F_range_shimmed_N'][0]:.1f}-"
          f"{s['F_range_shimmed_N'][1]:.1f} N |",
          f"| pressing the head down until it bottoms in its counterbore (plate off) | {s['F_head_bottomed_N']:.1f} N at "
          f"{s['L_head_bottomed_mm']:.2f} mm |",
          f"| thermal change in the spring's length | {s['thermal_range_mm'][0]:+.3f} to {s['thermal_range_mm'][1]:+.3f} mm |",
          f"| shortest length in use; margin to solid | {s['min_length_mm']:.2f} mm; {s['margin_to_solid_mm']:.2f} mm |",
          f"| shear stress at the highest force; at solid | {s['tau_at_Fmax_MPa']:.0f}; {s['tau_solid_MPa']:.0f} MPa "
          f"(allowable {s['tau_allow_MPa']:.0f} MPa) |", "",
          f"Tolerances: {TOL['src']}.\n",
          "## 3. Tip on the plate (316 dome on 6061 at 200 °C)\n",
          "| Dome R (mm) | F (N) | Contact Ø (µm) | p0 (MPa) | Yields hot 6061 (1.6 × 103 MPa)? |", "|---:|---:|---:|---:|---|"]
    for h in R["tip"]:
        L.append(f"| {h['R_mm']:.0f} | {h['F_N']:.1f} | {h['contact_d_um']:.0f} | {h['p0_MPa']:.0f} | {'yes' if h['yields_hot_6061'] else 'no'} |")
    L += ["", f"{AL_200['src']}.\n",
          "## 4. Acoustic loss (dB) of the new path\n",
          "| f (kHz) | Tip, dome greased | Tip, dome dry (tier B) | Cold end greased (2-10 µm film) |", "|---:|---|---|---|"]
    for t, d, c in zip(lb["tip"], lb["tip_dry"], lb["cold"]):
        L.append(f"| {t['f_kHz']:.0f} | {min(t['dB']):.2f} to {max(t['dB']):.2f} | {min(d['dB']):.1f} to {max(d['dB']):.1f} | "
                 f"{min(c['dB']):.2f} to {max(c['dB']):.2f} |")
    L += ["", "| Item | Low (dB) | High (dB) |", "|---|---:|---:|"]
    for k, v in lb["budget_dB"].items():
        L.append(f"| {k.replace('_', ' ')} | {v[0]:.2f} | {v[1]:.2f} |")
    L += [f"| **total, tier A (greased tip)** | **{lb['total_dB'][0]:.1f}** | **{lb['total_dB'][1]:.1f}** |",
          f"| total, tier B (dry tip at 500 °C) | {lb['tier_b_dry_tip_total_dB'][0]:.1f} | {lb['tier_b_dry_tip_total_dB'][1]:.1f} |",
          f"| the rod-end route (checks.json) | {lb['rod_end_route_dB'][0]:.1f} | {lb['rod_end_route_dB'][1]:.1f} |",
          f"| the previous waveguide budget (with an end-cap seal and a sensor shoe) | {lb['previous_waveguide_budget_dB'][0]:.1f} | "
          f"{lb['previous_waveguide_budget_dB'][1]:.1f} |", "",
          f"Method: {lb['method']}. {lb['src']}.\n",
          "## 5. Sensor temperature (the waveguide's foot, adiabatic: an upper bound)\n",
          f"Rating: {P['sensor']['t_min_C']:.0f} to {P['sensor']['t_max_C']:.0f} °C ({P['sensor']['vendor']} {P['sensor']['pn']}).\n",
          "| Case | Plate (°C) | Rod end (°C) | Sensor ≤ (°C) | Margin (K) |", "|---|---:|---:|---:|---:|"]
    for r in R["temperatures"]:
        L.append(f"| {r['case']} | {r['T_plate']:.0f} | {r['T_rod_end']:.1f} | {r['T_sensor_max']:.1f} | {r['margin_C']:.0f} |")
    pc = R["plate"]
    L += ["", "## 6. The plate's bayonet and the swaps\n",
          "| Module | Plate weight (N) | Bare bayonet lift (mm) | Foil needs (N) | 97125K111 clamp (N) | Left on the foil with the AE force (N) | Twist (N·m) | AE adds (N·mm) |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for k in ("M50", "L75"):
        p = pc[k]
        L.append(f"| {k} | {p['weight_N']:.2f} | {p['bare_lift_mm']:.2f} | {p['foil_needs_N']:.0f} | {p['disc_spring_clamp_N']:.0f} | "
                 f"{p['left_on_foil_N'][0]:.0f}-{p['left_on_foil_N'][1]:.0f} | {p['twist_Nm']:.2f} | {p['ae_twist_Nmm']:.1f} |")
    c = R["column"]
    L += ["", f"Pushing a plate home takes up to {pc['push_to_seat_N']:.0f} N more over the last {A['delta0']:.1f} mm. "
          f"The waveguide as a pinned column ({c['length_mm']:.0f} mm): P_cr {c['P_cr_N']:.0f} N, {c['ratio']:.0f}x the largest force.\n",
          "## Parts\n", "| Part | Maker, number | What | Page (read) |", "|---|---|---|---|"]
    for key, p in P.items():
        L.append(f"| {key} | {p['vendor']} {p['pn']} | {p['desc']} | [{p['url'].split('/')[2]}]({p['url']}) ({p['read_utc']}) |")
    return "\n".join(L) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g = zlev()
    zb1 = g["z"]["zb1"]
    g["head_clear_on"] = g["head_bottom_on"] - (zb1 - 4.3 - A["cb_depth"])
    rows = stroke_cases()
    s = spring_check(rows)
    # the head bottoms on its counterbore floor before the spring gets near solid: the most anyone can press it (plate off)
    L_bottom = A["spring_L_stop"] - A["delta0"] - g["head_clear_on"]
    s["F_head_bottomed_N"] = A["spring_k"] * (1 + TOL["k_frac"]) * (A["spring_L0"] * (1 + TOL["L0_frac"]) - L_bottom)
    s["L_head_bottomed_mm"] = L_bottom
    # set at assembly instead: shim under the spring so the head lifts off its stop at 12.5 +/- 0.5 N (push gauge, plate off)
    lo = min(r["spring_length_change_mm"] for r in rows)
    hi = max(r["spring_length_change_mm"] for r in rows)
    k = A["spring_k"]
    s["F_range_shimmed_N"] = (12.0 + k * (1 - TOL["k_frac"]) * (A["delta0"] - TOL["delta0"] - TOL["plate"] - hi),
                              13.0 + k * (1 + TOL["k_frac"]) * (A["delta0"] + TOL["delta0"] + TOL["plate"] - lo))
    R = dict(run_utc=time.strftime("%Y-%m-%d %H:%M", time.gmtime()), design=A,
             geometry={k: v for k, v in g.items() if k != "z"}, stroke=rows, spring=s, tip=tip_check(s["F_range_N"]),
             loss=loss_budget(s["F_range_N"]), temperatures=temperatures(rows), plate=plate_check(s["F_range_N"]),
             column=column_check(s["F_range_N"]), parts=PARTS)
    R["pass_"] = bool(s["pass_window"] and s["pass_stress"] and s["margin_to_solid_mm"] >= 0.5 and g["head_clear_on"] > 0.2
                      and all(t["margin_C"] > 20 for t in R["temperatures"])
                      and not any(h["yields_hot_6061"] for h in R["tip"] if h["R_mm"] == A["dome_R"] and h["F_N"] <= s["F_range_N"][1] + 1e-9))
    (OUT / "ae_preload.json").write_text(json.dumps(R, indent=1, default=float))
    (OUT / "ae_preload.md").write_text(write_md(R))
    print(f"force on the plate {s['F_range_N'][0]:.1f}-{s['F_range_N'][1]:.1f} N (stop {s['F_stop_N'][0]:.1f}-{s['F_stop_N'][1]:.1f}); "
          f"thermal {s['thermal_range_mm'][0]:+.3f}..{s['thermal_range_mm'][1]:+.3f} mm; to solid {s['margin_to_solid_mm']:.2f} mm; "
          f"tau {s['tau_at_Fmax_MPa']:.0f}/{s['tau_allow_MPa']:.0f} MPa")
    print(f"loss {R['loss']['total_dB'][0]:.1f}-{R['loss']['total_dB'][1]:.1f} dB vs rod end {R['loss']['rod_end_route_dB'][0]:.0f}-"
          f"{R['loss']['rod_end_route_dB'][1]:.0f}; sensor <= {max(t['T_sensor_max'] for t in R['temperatures']):.1f} C; pass {R['pass_']}")
    return R


if __name__ == "__main__":
    main()
