"""Vacuum tightness of the frame + floor plate against the old solid block, and the purge with the pump the BOM now names.

Written 2026-11-23 for PR #266 (issue #260), in answer to:
  "How does the ability to hold a vacuum and reduce air ingress get affected by no longer using the solid block for the
   chamber? Also, in this system do we do a vacuum followed by inert gas backfilling? If so, is it a turbo or a roughing
   pump? How is that going to affect the prints?"

It reuses seals.py's committed results (analysis/out/seals/seals.json: every seal's permeation, the 11.3 L envelope, the
outgassing load) and its Parker leak-rate function, so the two stay consistent. It adds:

  1. Block vs frame + floor plate: what the floor joint adds by permeation (O2, N2, H2O) during a build and at vacuum, and
     the make-up argon to hold 10 ppm O2.
  2. Real leaks: the flow through a defect channel across a seal land (a scratch, a powder grain, a hair), inward at
     vacuum and outward at +20 mbar, with the Peclet number that says whether O2 can diffuse in against the outflow.
  3. Virtual leaks: the hairline crevice at the floor joint and the plugged rail holes, and how fast they empty.
  4. The purge with the Edwards nXDS6i dry scroll (BOM G2 since 2026-11-22; seals.py still sizes the old McMaster
     4396K21 rotary vane): pump-down time through the hoses, base pressure, O2 after each cycle for base pressures from
     1 mbar down to a turbo's 1e-5 mbar, with the argon's own impurity as the floor.
  5. Water after the purge: wall outgassing (falls as 1/t) and the powder's water, which no pump removes at room
     temperature.

Run:  python desktop-lpbf/analysis/seals/vacuum_purge.py   (numpy only; ~1 s)
Out:  desktop-lpbf/analysis/out/seals/vacuum_purge.{json,md}
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seals as S  # noqa: E402  (parker_leak, f_perm, permeability constants)

ROOT = HERE.parents[1]
OUT = ROOT / "analysis" / "out" / "seals"
R0 = json.loads((OUT / "seals.json").read_text())
TAU_SOFT = float(R0.get("soft_pump", {}).get("tau_needed_s", 25.3))   # seals.py: the deepest powder bed sets it (16 s since the jar got shorter)

ATM_MBAR = 1013.25
P_OP_MBAR = ATM_MBAR + 20.0             # build: +20 mbar of argon
V_L = R0["envelope_L"]["total"]         # 11.3 L: chamber, plenums, hoses, filter housing, blower
T_K = 293.15
MBARL_PER_SCC = 1.01325                 # 1 std cc = 1.013 mbar L
MU_AIR, MU_AR = 1.81e-5, 2.25e-5        # Pa s
D_O2_AR = 2.0e-5                        # m2/s, O2 in Ar at 1 atm, 20 C (Chapman-Enskog order of magnitude)
X_O2_AIR, X_N2_AIR = 0.2095, 0.7808
RH, P_SAT_H2O = 0.5, 28.1               # 50 % RH at 23 C: p_H2O = 14 mbar

SOURCES = {
    1: "Parker O-Ring Handbook ORD 5700 §3.12.1 (leak rate L = 0.7 F D P Q (1-S)^2) and Table 3-24 (permeability); via seals.py",
    2: "Sturm et al. (2004) J. Geophys. Res. 109, D04309, https://doi.org/10.1029/2003JD004073: water permeation of Viton O-rings; via seals.py",
    3: "O'Hanlon, A User's Guide to Vacuum Technology, 3rd ed. (Wiley 2003): viscous and molecular conductance (C = 135 d^4 p / L, "
       "C = 12.1 d^3 / L for air, d and L in cm), outgassing of unbaked Al and Viton after 1 h, falling ~1/t",
    4: "Edwards nXDS6i dry scroll pump (BOM G2, A73501983): peak pumping speed 6.2 m3/h (displacement 6.8 m3/h), ultimate "
       "0.020 mbar, maximum continuous inlet pressure 200 mbar; Marshall Scientific spec sheet "
       "https://marshallscientific.com/v/vspfiles/specs/Edwards%20nXDS%20Dry%20Scroll%20Pump%20-%20Marshall%20Scientific.pdf "
       "(read 2026-11-23); the BOM's 6.8 m3/h is the displacement",
    5: "Shah & London (1978): laminar flow in a square duct, Q = 0.03514 a^4 dp / (mu L)",
    6: "Airgas/Linde argon 5.0 (UHP): O2 <= 1-2 ppm, H2O <= 1-3 ppm (seals.py source 9)",
}


# ------------------------------------------------------------------ 1. permeation: block vs frame + floor plate
def permeation():
    items = R0["permeation"]["items"]
    floor = next(p for p in items if p["seal"].startswith("floor"))
    tot_o2 = R0["permeation"]["total_O2_sccs"]
    tot_h2o = R0["permeation"]["total_H2O_sccs"]
    # N2 through the same seals: Parker's N2 coefficient at 30 C (0.233e-8) against O2's at 26 C (1.7e-8), times the
    # partial-pressure ratio; both scaled with the same Arrhenius factor, so the ratio carries over seal by seal
    n2_per_o2 = (S.F_N2_30 * X_N2_AIR) / (S.F_O2_26 * X_O2_AIR)
    # the 4 rail-hole plug screws' bonded washers: an M4 bonded seal's rubber ring (~ID 4.4, ~1.5 mm section), 25 %
    # squeeze, 40 C: modelled as an O-ring of that ID in Parker's formula
    washer_o2 = 4 * S.parker_leak(S.f_perm(S.F_O2_26, 26, 40, S.EA_HE), 4.4, X_O2_AIR * 1.013, 0.25)
    washer_h2o = 4 * S.parker_leak(S.f_perm(S.F_H2O_STURM, 25, 40, S.EA_HE), 4.4, RH * P_SAT_H2O / 1000.0, 0.25)

    def ppm_h(sccs):
        return sccs * 3600 / (V_L * 1000 * P_OP_MBAR / ATM_MBAR) * 1e6

    def row(name, o2, h2o):
        n2 = o2 * n2_per_o2
        gas_mbarLs = (o2 + n2 + h2o) * MBARL_PER_SCC
        return dict(design=name, O2_sccs=o2, N2_sccs=n2, H2O_sccs=h2o,
                    O2_ppm_per_h_build=ppm_h(o2), H2O_ppm_per_h_build=ppm_h(h2o),
                    makeup_sccm_for_10ppm_O2=o2 * 60 / (10e-6 - 1e-6),
                    vacuum_hold_gas_mbarLs=gas_mbarLs, rate_of_rise_mbar_per_min=gas_mbarLs * 60 / V_L)

    # seals.json is the frame as drawn (it has the floor cord, but not the washers): the block is that minus the floor cord
    block = row("solid block (no floor joint, rail inserts blind in the wall)", tot_o2 - floor["O2_sccs"], tot_h2o - floor["H2O_sccs"])
    frame = row("frame + floor plate (as drawn)", tot_o2 + washer_o2, tot_h2o + washer_h2o)
    joint = row("the floor joint alone (947 mm cord at 60 C + 4 bonded washers)", floor["O2_sccs"] + washer_o2,
                floor["H2O_sccs"] + washer_h2o)
    # the floor cord's share at a cooler 40 C (it sits under the walls, away from the module)
    f40 = S.f_perm(S.F_O2_26, 26, 40, S.EA_HE) / S.f_perm(S.F_O2_26, 26, 60, S.EA_HE)
    return dict(block=block, frame=frame, floor_joint=joint, n2_per_o2=n2_per_o2, floor_T_C=floor["T_C"],
                floor_share_at_40C=f40, washers_O2_sccs=washer_o2,
                frame_over_block_O2=frame["O2_sccs"] / block["O2_sccs"])


# ------------------------------------------------------------------ 2. real leaks through a defect across a seal land
def defect_leaks(land_mm=2.0):
    """Square channel of side a across a seal land of length land_mm: viscous (Poiseuille) flow of an ideal gas,
    Q_pV = 0.03514 a^4 (p1^2 - p2^2) / (2 mu L)  [Pa m3/s]. At these sizes the mean free path at 1 atm (68 nm) is
    << a, so the viscous form holds over most of the channel; slip near the vacuum end adds a little."""
    out = []
    L = land_mm * 1e-3
    for a_um in (2, 5, 10, 20, 45):
        a = a_um * 1e-6
        k = 0.03514 * a ** 4 / (2 * L)
        p1 = ATM_MBAR * 100
        q_in = k * (p1 ** 2 - 100.0 ** 2) / MU_AIR * 10.0          # mbar L/s of air at the 1 mbar hold
        p_in = P_OP_MBAR * 100
        q_out = k * (p_in ** 2 - p1 ** 2) / MU_AR * 10.0             # mbar L/s of argon out at +20 mbar
        v = (q_out / 10.0) / (a * a * p1)                            # m/s at the outlet
        pe = v * L / D_O2_AR
        # O2 diffusing in against the outflow, steady 1-D advection-diffusion with c = c_room outside and ~0 inside:
        # net inward flux j = v c_room / (exp(Pe) - 1), which tends to D c_room / L as Pe -> 0
        c_room = X_O2_AIR * p1 / (8.314 * T_K)                         # mol/m3
        j = v * c_room / math.expm1(min(pe, 700.0)) if pe > 1e-9 else D_O2_AR * c_room / L
        o2_in_build_sccs = j * a * a * 22414.0                          # std cc/s
        o2_ppm_h_vac = q_in * X_O2_AIR / ATM_MBAR / V_L * 3600 * 1e6 * (ATM_MBAR / P_OP_MBAR)
        out.append(dict(a_um=a_um, air_in_at_vacuum_mbarLs=q_in, argon_out_at_20mbar_sccm=q_out / MBARL_PER_SCC * 60,
                        exit_velocity_m_s=v, peclet=pe, o2_backdiffusion_factor=math.exp(-min(pe, 700.0)),
                        o2_in_during_build_sccs=o2_in_build_sccs,
                        rate_of_rise_mbar_per_min=q_in * 60 / V_L, o2_ppm_per_h_if_it_leaked_in=o2_ppm_h_vac))
    return out


# ------------------------------------------------------------------ 3. virtual leaks
def virtual_leaks():
    vbar = math.sqrt(8 * 8.314 * T_K / (math.pi * 0.029))           # m/s, air
    # (a) the floor joint's hairline crevice inside the O-ring: 1.5 mm deep to the cord, 940 mm long, <= 25 um open
    h, depth, W = 25e-6, 1.5e-3, 0.940
    clausing = (h / depth) * (0.5 + math.log(depth / h))             # long slit, Clausing's approximation
    c_crev = vbar / 4 * W * h * clausing * 1000                      # L/s, molecular (the worst case for emptying)
    v_crev = 1.5 * 0.025 * 940 * 1e-6                                # L (35 mm3)
    # (b) each rail hole tapped through the back wall: the space between the rail screw's tip and the plug screw's
    # tip (1.2 mm) plus the thread clearance, vented to the chamber along the rail screw's thread (helical gap
    # ~0.05 x 0.3 mm over ~12 mm of engagement = ~17 turns x pi x 3.6 mm)
    v_hole = (math.pi / 4 * 3.3 ** 2 * 1.2 + 10.0) * 1e-6           # L, ~20 mm3
    A, B, Lh = 0.05e-3 * 0.3e-3, 2 * (0.05e-3 + 0.3e-3), 17 * math.pi * 3.6e-3
    c_hole = 4.0 / 3.0 * vbar * A ** 2 / (B * Lh) * 1000             # L/s, molecular, long channel
    res = {}
    for name, v, c, n in (("floor crevice", v_crev, c_crev, 1), ("plugged rail hole", v_hole, c_hole, 4)):
        tau = v / c
        gas_mbarL = n * v * ATM_MBAR                                   # if it held air at 1 atm when the pump started
        res[name] = dict(volume_mm3=v * 1e6, n=n, conductance_Ls=c, tau_s_molecular=tau,
                         air_content_mbarL=gas_mbarL,
                         o2_ppm_if_released_after_backfill=gas_mbarL * X_O2_AIR / (V_L * P_OP_MBAR) * 1e6)
    return res


# ------------------------------------------------------------------ 4. purge with the nXDS6i
S0 = 6.2 / 3.6                    # L/s, peak pumping speed (6.8 m3/h is the displacement)
P_ULT = 0.02                      # mbar, listed ultimate
D_CM, L_CM, CORR = 2.2, 2 * 61.0, 0.6      # two 24 in. KF-25 bellows to the pump (as seals.py), corrugation factor


def conductance(p):
    c_visc = 135 * D_CM ** 4 * p / L_CM
    c_mol = 12.1 * D_CM ** 3 / L_CM
    return CORR * (c_visc + c_mol)


def s_eff(p):
    s = S0 * max(0.0, 1 - P_ULT / max(p, 1.0001 * P_ULT))
    c = conductance(p)
    return s * c / (s + c) if s > 0 else 0.0


def pump_down(p_to, tau_soft=TAU_SOFT, p_soft=100.0, q_gas=0.0):
    """Seconds from 1013 mbar to p_to: soft pump (V/S = tau_soft) to p_soft, then the pump through the hoses, against a
    constant gas load q_gas (mbar L/s)."""
    t = tau_soft * math.log(ATM_MBAR / p_soft)
    ps = np.logspace(math.log10(p_soft), math.log10(p_to), 600)
    for a, b in zip(ps[:-1], ps[1:]):
        pm = math.sqrt(a * b)
        net = s_eff(pm) * pm - q_gas
        if net <= 0:
            return math.inf
        t += V_L * (a - b) / net
    return t


def purge_cycles(p_base, x_ar_ppm, n=3, leak_mbarLs=1e-4, hold_s=120.0):
    """O2 (ppm) after each pump-and-backfill cycle: what is left at p_base is diluted by argon (impurity x_ar_ppm) to
    P_OP, plus room air that leaks in during the hold."""
    x = X_O2_AIR * 1e6
    out = []
    for _ in range(n):
        left = x * p_base / P_OP_MBAR
        leak_o2 = leak_mbarLs * hold_s * X_O2_AIR / (V_L * P_OP_MBAR) * 1e6
        x = left + x_ar_ppm * (1 - p_base / P_OP_MBAR) + leak_o2
        out.append(x)
    return out


def purge():
    q_out_1h = R0["budget"]["q_al_mbarLs"] + R0["budget"]["q_fkm_mbarLs"]        # mbar L/s after 1 h
    rows = []
    for t_min in (5, 15, 60):
        q = q_out_1h * 60.0 / t_min                                                  # ~1/t
        p_floor = P_ULT + q / s_eff(0.05)
        rows.append(dict(minutes_after_closing=t_min, outgassing_mbarLs=q, base_pressure_mbar=p_floor))
    times = {f"to_{p:g}_mbar_s": pump_down(p, q_gas=q_out_1h * 60.0 / 5) for p in (100, 10, 1, 0.1, 0.05)}
    cyc = {}
    for label, pb in (("1 mbar (the plan)", 1.0), ("0.1 mbar", 0.1), ("0.05 mbar (scroll near its ultimate)", 0.05),
                      ("1e-5 mbar (with a turbo)", 1e-5)):
        cyc[label] = dict(p_base=pb, ar_1ppm=purge_cycles(pb, 1.0), ar_2ppm=purge_cycles(pb, 2.0))
    t_cycle = pump_down(1.0, q_gas=q_out_1h * 60.0 / 5) + 120.0 + V_L * P_OP_MBAR / ATM_MBAR / 25.0 * 60.0
    return dict(S0_Ls=S0, p_ult_mbar=P_ULT, S_eff_Ls={f"{p:g}": s_eff(p) for p in (800, 100, 10, 1, 0.1, 0.05)},
                pump_down_s=times, base_pressure=rows, cycles=cyc,
                one_cycle_s=t_cycle, three_cycles_min=3 * t_cycle / 60.0,
                note=f"soft pump at V/S = {TAU_SOFT:.0f} s to 100 mbar (seals.py), then full speed; 2 min hold; back-fill at 25 L/min")


# ------------------------------------------------------------------ 5. water after the purge
def water():
    q1h = R0["budget"]["q_al_mbarLs"] + R0["budget"]["q_fkm_mbarLs"]
    out = {}
    for hold_min in (10, 30, 60):
        t0 = hold_min * 60.0
        mbarL = q1h * 3600.0 * math.log((t0 + 3600.0) / t0)       # released in the first hour after back-fill
        out[f"hold_{hold_min}_min"] = dict(wall_water_first_hour_mbarL=mbarL,
                                           ppm_without_makeup=mbarL / (V_L * P_OP_MBAR) * 1e6)
    mg = R0["budget"]["powder_H2O_mg"]
    out["powder"] = dict(powder_H2O_mg=mg, mbarL=[m * 1e-3 / 18.015 * 8.314 * T_K * 10.0 for m in mg],
                         ppm_if_released=R0["budget"]["powder_H2O_ppm_if_released"])
    return out


def fmt(x, nd=2):
    if x == 0:
        return "0"
    if math.isinf(x):
        return "never"
    return f"{x:.{nd}e}" if (abs(x) < 1e-2 or abs(x) >= 1e4) else f"{x:.{nd}f}"


def write_md(R):
    P, D, VL, PU, W = R["permeation"], R["defects"], R["virtual"], R["purge"], R["water"]
    L = ["# Vacuum tightness of the frame + floor plate, and the purge with the dry scroll pump", "",
         "From [`analysis/seals/vacuum_purge.py`](../../seals/vacuum_purge.py), which reads `seals.json` from "
         "[`seals.py`](../../seals/seals.py). The question and the conclusions are in [`vacuum-and-purge.md`](../../../vacuum-and-purge.md).", "",
         f"Gas envelope {V_L:.1f} L; build at +20 mbar of argon. sccs = std cc/s.", "",
         "## 1. Permeation: the old block against the frame + floor plate", "",
         "| Design | O₂ (sccs) | N₂ (sccs) | H₂O (sccs) | O₂ during a build (ppm/h) | H₂O during a build (ppm/h) | Ar make-up for 10 ppm O₂ (sccm) | Rate of rise at vacuum (mbar/min) |",
         "|---|---|---|---|---|---|---|---|"]
    for k in ("block", "frame", "floor_joint"):
        r = P[k]
        L.append(f"| {r['design']} | {fmt(r['O2_sccs'])} | {fmt(r['N2_sccs'])} | {fmt(r['H2O_sccs'])} | {r['O2_ppm_per_h_build']:.2f} | "
                 f"{r['H2O_ppm_per_h_build']:.1f} | {r['makeup_sccm_for_10ppm_O2']:.1f} | {fmt(r['rate_of_rise_mbar_per_min'])} |")
    L += ["", f"The frame lets in {100 * (P['frame_over_block_O2'] - 1):.0f} % more O₂ by permeation than the block did. "
          f"The floor cord is taken at {P['floor_T_C']:.0f} °C; at 40 °C its share would be {P['floor_share_at_40C']:.2f}× that. "
          f"N₂/O₂ = {P['n2_per_o2']:.2f} through FKM (Parker). The 4 bonded washers add {fmt(P['washers_O2_sccs'])} sccs of O₂.", "",
          "## 2. Real leaks: one defect channel across a 2 mm seal land", "",
          "| Channel (µm square) | Air in at vacuum (mbar·L/s) | Rate of rise (mbar/min) | Argon out at +20 mbar (sccm) | Exit velocity (m/s) | Péclet | O₂ in against the outflow during a build (sccs) |",
          "|---|---|---|---|---|---|---|"]
    for d in D:
        L.append(f"| {d['a_um']} | {fmt(d['air_in_at_vacuum_mbarLs'])} | {fmt(d['rate_of_rise_mbar_per_min'])} | {fmt(d['argon_out_at_20mbar_sccm'])} | "
                 f"{d['exit_velocity_m_s']:.2f} | {d['peclet']:.1f} | {fmt(d['o2_in_during_build_sccs'])} |")
    L += ["", f"For comparison, permeation through every seal brings in {fmt(P['frame']['O2_sccs'])} sccs of O₂ during a build."]
    L += ["", "The leak budget in `seals.md` is 1e-4 mbar·L/s in all, a rise of 5e-4 mbar/min; the acceptance test passes under 1e-3 mbar/min.", "",
          "## 3. Virtual leaks", "", "| Volume | Size | n | Conductance, molecular (L/s) | τ = V/C (s) | Air it held (mbar·L) | O₂ if all released after back-fill (ppm) |",
          "|---|---|---|---|---|---|---|"]
    for k, v in VL.items():
        L.append(f"| {k} | {v['volume_mm3']:.0f} mm³ | {v['n']} | {fmt(v['conductance_Ls'])} | {fmt(v['tau_s_molecular'])} | {fmt(v['air_content_mbarL'])} | {fmt(v['o2_ppm_if_released_after_backfill'])} |")
    L += ["", "## 4. Purge with the Edwards nXDS6i dry scroll (BOM G2)", "",
          f"Listed {PU['S0_Ls'] * 3.6:.1f} m³/h peak pumping speed ({PU['S0_Ls']:.2f} L/s), ultimate {PU['p_ult_mbar']} mbar; two KF-25 bellows (1.2 m). "
          "Effective speed at the chamber (L/s): " + ", ".join(f"{k} mbar {v:.2f}" for k, v in PU["S_eff_Ls"].items()) + ".", "",
          f"Pump-down from 1013 mbar with the soft-pump start (V/S = {TAU_SOFT:.0f} s to 100 mbar), against the walls' outgassing 5 min after closing: "
          + ", ".join(f"{k.replace('to_', '').replace('_mbar_s', ' mbar')}: {v / 60:.1f} min" for k, v in PU["pump_down_s"].items()) + ".", "",
          "| Minutes after closing | Wall + seal outgassing (mbar·L/s) | Base pressure (mbar) |", "|---|---|---|"]
    for r in PU["base_pressure"]:
        L.append(f"| {r['minutes_after_closing']} | {fmt(r['outgassing_mbarLs'])} | {fmt(r['base_pressure_mbar'], 3)} |")
    L += ["", f"O₂ after each cycle (pump to the base pressure, 2 min hold with a 1e-4 mbar·L/s leak, back-fill to +20 mbar). One cycle takes ~{PU['one_cycle_s'] / 60:.1f} min, three ~{PU['three_cycles_min']:.0f} min.", "",
          "| Base pressure | Ar 5.0 at 1 ppm O₂: cycles 1 / 2 / 3 (ppm) | at 2 ppm O₂ (ppm) |", "|---|---|---|"]
    for k, v in PU["cycles"].items():
        L.append(f"| {k} | {' / '.join(f'{x:.2f}' if x < 100 else f'{x:.0f}' for x in v['ar_1ppm'])} | {' / '.join(f'{x:.2f}' if x < 100 else f'{x:.0f}' for x in v['ar_2ppm'])} |")
    L += ["", "## 5. Water after the purge", "", "| Hold before back-fill | Wall + seal water released in the first hour after (mbar·L) | ppm in the loop with no make-up |", "|---|---|---|"]
    for k, v in W.items():
        if k.startswith("hold"):
            L.append(f"| {k.split('_')[1]} min | {v['wall_water_first_hour_mbarL']:.2f} | {v['ppm_without_makeup']:.0f} |")
    pw = W["powder"]
    L += ["", f"Powder: {pw['powder_H2O_mg'][0]:.1f}–{pw['powder_H2O_mg'][1]:.1f} mg of water in 150 g ({pw['mbarL'][0]:.0f}–{pw['mbarL'][1]:.0f} mbar·L), "
          f"{pw['ppm_if_released'][0]:.0f}–{pw['ppm_if_released'][1]:.0f} ppmv if the hot plate drives it all off.", "", "## Sources", ""]
    L += [f"{k}. {v}" for k, v in SOURCES.items()]
    (OUT / "vacuum_purge.md").write_text("\n".join(L) + "\n")


def main():
    R = dict(permeation=permeation(), defects=defect_leaks(), virtual=virtual_leaks(), purge=purge(), water=water(),
             sources=SOURCES)
    (OUT / "vacuum_purge.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    write_md(R)
    p = R["permeation"]
    print(json.dumps(dict(block_O2_ppm_h=p["block"]["O2_ppm_per_h_build"], frame_O2_ppm_h=p["frame"]["O2_ppm_per_h_build"],
                          ratio=p["frame_over_block_O2"], pump=R["purge"]["pump_down_s"], cycles=R["purge"]["cycles"],
                          defects=[(d["a_um"], d["air_in_at_vacuum_mbarLs"], d["peclet"]) for d in R["defects"]],
                          virtual=R["virtual"]), indent=1, default=float))


if __name__ == "__main__":
    main()
