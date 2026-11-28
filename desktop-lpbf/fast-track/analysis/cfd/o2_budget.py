"""O2 that gets into FT-1's box and FT-1V's cube, and FT-1V's pump-purge, as 0-D balances (issue #260, round 3).

The purge CFD (results.md section 2) has tight walls and pure argon, so the O2 it reaches is the purge's own limit.
This script adds what sets the real floor, as estimates (each input is marked with its source or as an estimate):

  Box (FT-1), well mixed at steady state: x_O2 = x_O2,argon + sum(O2 in) / Q_argon, for
    - the argon's own O2 (grade 5.0 or 4.8);
    - back-diffusion through gaps under the lid gasket against the outflow they carry: a slit of height h across the
      gasket's 8 mm land, along the whole 1.28 m seam (an upper bound for a seated lid) or a 20 mm stretch (a defect).
      1-D advection-diffusion in the slit, outflow u, O2 diffusing in: O2 in = x_air Q_gap / (exp(Pe) - 1),
      Pe = u L / D = h^2 dP / (12 mu D) (plane Poiseuille), the diffusion limit x_air D w h / L at dP = 0;
    - permeation through the silicone sponge gasket (dense PDMS 600 Barrer, a closed-cell sponge up to 5x) and the
      FKM O-rings (Parker's formula, F = 1.7e-8 std cc cm/(cm2 s bar), as round 1's seals.py);
    - polymer feed tubing (2 m of 1/4 in., 1-20 Barrer: stainless or copper has none);
    - air held in the powder in the hopper (diffusion out of a 33 mm deep bed) and in the X-LSM100B's body (a virtual
      leak with an unknown time constant, 5-60 min).
  Cube (FT-1V): the pump-purge (the McMaster 4396K21 in parts.csv E3: 3 cfm, 1e-2 Torr), cycles against base pressure,
  the backfill at the regulator's 33 L/min, and the leak and permeation floor with the cube sealed.

Run (light, < 10 s):  /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/o2_budget.py
Writes analysis/out/cfd/o2_budget.json, o2_floor.png, pump_purge.png.
"""
from __future__ import annotations

import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
import numpy as np                                  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[0] / "out" / "cfd"
X_AIR = 0.2095
MU_AR = 2.26e-5          # Pa s, argon 25 C
D_O2 = 2.0e-5            # m2/s, O2 in Ar, 25 C, 1 atm (as the purge CFD)
P_ATM = 101325.0
BARRER = 1e-10           # cm3(STP) cm / (cm2 s cmHg)
CMHG = 1333.22           # Pa
IN, PSI = 25.4, 6894.76

# ---------------- inputs (sources in SRC) ----------------
GEOM = dict(box_gas_L=23.88, cube_gas_L=22.22,        # geom.py on CAD v2 (round 3); ft_checks: 24.04 / 22.64
            seam_m=1.282, gasket_w_mm=8.0, gasket_h_mm=4.0, gasket_compressed_mm=3.0)
ARGON = {"5.0": dict(O2=2.0, H2O=3.0), "4.8": dict(O2=3.0, H2O=5.0)}   # ppm, supplier maxima [1]
PERM = dict(pdms_O2=600.0, pdms_H2O=36000.0, sponge_factor=5.0,      # Barrer [2, 3]; sponge: estimate
            fkm_O2_F=1.7e-8, tube_O2=(1.0, 20.0))                    # Parker (round 1 seals.py) [4]; tubing: estimate
RH50_PA = 1400.0                                                     # water partial pressure, 23 C, 50 % RH
POWDER = dict(hopper_cm3=30.0, solid_frac=0.55, depth_mm=33.0, tortuosity=1.5)   # P['hopper'] ~30 cm3; estimates
STAGE = dict(void_cm3=(10.0, 40.0), tau_min=(5.0, 60.0))            # X-LSM100B body: estimate
PUMP = dict(S0_L_s=3 * 28.3168 / 60, p_ult_mbar=0.01 * 1.33322,      # McMaster 4396K21: 3 cfm, 1e-2 Torr [5]
            line_d_mm=9.5, line_L_mm=60.0, hose_d_mm=25.0, hose_L_mm=1000.0)       # 1/2 in. flare adapter, KF-25 hose
FILL_L_MIN = 33.0        # G1 regulator / flowmeter, 0-70 scfh
SRC = {
    1: "Argon O2/H2O maxima: 5.0 (99.999 %) O2 <= 2 ppm, H2O <= 3 ppm (Linde ICP-grade argon 5.0 datasheet; Messer 5.0); "
       "4.8 (99.998 %) O2 3-4 ppm, H2O 3-5 ppm depending on the supplier (Linde spectrometry 4.8, Messer, Airgas). "
       "Check the cylinder's certificate.",
    2: "Robb (1968), Thin silicone membranes - their permeation properties and some applications, Ann. N.Y. Acad. Sci. "
       "146, 119, https://doi.org/10.1111/j.1749-6632.1968.tb20277.x: silicone rubber O2 ~600 Barrer, H2O ~36,000 Barrer.",
    3: "Merkel et al. (2000), Gas sorption, diffusion, and permeation in poly(dimethylsiloxane), J. Polym. Sci. B 38, 415, "
       "https://doi.org/10.1002/(SICI)1099-0488(20000201)38:3<415::AID-POLB8>3.0.CO;2-Z: PDMS O2 ~800 Barrer at 35 C.",
    4: "Parker O-ring handbook ORD 5700 section 3.12 (leak rate L = 0.7 F D P Q (1-S)^2), FKM O2 F = 1.7e-8 std cc cm/(cm2 s bar); "
       "as desktop-lpbf/analysis/seals/seals.py (round 1).",
    5: "McMaster 4396K21: 3 cfm, ultimate 1e-2 Torr (desktop-lpbf/mcmaster-parts.csv, read 2026-11-17).",
}


# ---------------- box: leaks ----------------
def slit(h_um, w_m, dp_pa, L_mm=GEOM["gasket_w_mm"], q_cap_m3s=None):
    """A slit of height h, width w (along the seam), length L across the gasket land, the box at dp over the room.
    Returns outflow (m3/s), Peclet number, O2 in (m3/s at 1 atm)."""
    h, L = h_um * 1e-6, L_mm * 1e-3
    q = w_m * h ** 3 * dp_pa / (12 * MU_AR * L)
    if q_cap_m3s is not None:
        q = min(q, q_cap_m3s)
    if q <= 0:
        return 0.0, 0.0, X_AIR * D_O2 * w_m * h / L
    u = q / (w_m * h)
    pe = u * L / D_O2
    o2 = X_AIR * q / math.expm1(pe) if pe < 700 else 0.0
    return q, pe, o2


def perm_gasket(P_barrer, dp_partial_pa, seam_m=GEOM["seam_m"]):
    """Permeation through the gasket's cross-section (compressed height x seam) across its 8 mm width, cm3(STP)/s."""
    a_cm2 = seam_m * 100 * GEOM["gasket_compressed_mm"] / 10
    return P_barrer * BARRER * a_cm2 / (GEOM["gasket_w_mm"] / 10) * dp_partial_pa / CMHG


def parker(F, d_id_mm, dp_bar, squeeze=0.25, q=1.27):
    """Parker: L [std cc/s] = 0.7 F D P Q (1-S)^2, D (O-ring ID) in inches, P in psi; Q = 1.27 dry at 25 % squeeze."""
    return 0.7 * F * (d_id_mm / IN) * (dp_bar * 1e5 / PSI) * q * (1 - squeeze) ** 2


# FKM O-rings and seals in the box (IDs in mm, estimates from the model's parts)
BOX_ORINGS = dict(rod_gland_2x=2 * 12.4, gland_face=30.0, window=48.0, window_ring_to_door=55.0,
                  light_ports_2x=2 * (28.0 + 30.0), camera_port=2 * 25.0, cable_glands_2x=2 * (8.0 + 16.0),
                  bulkheads_4x=4 * 10.0)
CUBE_ORINGS = dict(plates_6x=6 * (4 * 280.0 / math.pi), kf25_6x=6 * 25.0, window=2 * 50.0, rod_gland=2 * 12.4 + 30.0,
                   light_and_camera_ports=3 * 2 * 28.0)


def box_budget():
    ml_min = lambda cm3_s: cm3_s * 60.0                     # cm3/s -> mL/min (STP ~ 1 atm, 25 C here)
    out = {}
    # permeation, mL/min
    o2_dense = ml_min(perm_gasket(PERM["pdms_O2"], X_AIR * P_ATM))
    h2o_dense = ml_min(perm_gasket(PERM["pdms_H2O"], RH50_PA))
    fkm = ml_min(sum(parker(PERM["fkm_O2_F"], d, X_AIR * 1.01325) for d in BOX_ORINGS.values()))
    tube = [ml_min(p * BARRER * 2 * math.pi * 200 / math.log(6.35 / 4.32) * X_AIR * P_ATM / CMHG) for p in PERM["tube_O2"]]
    out["permeation_mL_min"] = dict(gasket_O2_dense_silicone=o2_dense, gasket_O2_sponge_x5=o2_dense * PERM["sponge_factor"],
                                    gasket_H2O_dense_silicone_50pctRH=h2o_dense, fkm_orings_O2=fkm,
                                    feed_tubing_O2_1_to_20_barrer=tube)
    # gaps under the gasket: whole seam (a lid not seated) and a 20 mm defect; dP = 5 and 10 mbar, and 0 (vent open)
    rows = []
    for h in (1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0, 100.0):
        for w, lab in ((GEOM["seam_m"], "whole seam"), (0.020, "20 mm defect")):
            for dp in (0.0, 500.0, 1000.0):
                q, pe, o2 = slit(h, w, dp)
                rows.append(dict(h_um=h, where=lab, dp_mbar=dp / 100, outflow_mL_min=q * 6e7, peclet=pe, O2_in_mL_min=o2 * 6e7))
    out["gaps"] = rows
    # worst gap at 5 mbar: Pe ~ 0.87
    h_star = math.sqrt(0.874 * 12 * MU_AR * D_O2 / 500.0) * 1e6
    out["worst_gap_um_at_5mbar"] = h_star
    out["worst_gap_O2_mL_min_whole_seam_5mbar"] = slit(h_star, GEOM["seam_m"], 500.0)[2] * 6e7
    # powder in the hopper: air in its pores, diffusing out of a bed open at the top (slowest mode)
    v_air = POWDER["hopper_cm3"] * (1 - POWDER["solid_frac"])
    d_eff = D_O2 * (1 - POWDER["solid_frac"]) / POWDER["tortuosity"]
    tau = 4 * (POWDER["depth_mm"] * 1e-3) ** 2 / (math.pi ** 2 * d_eff)
    out["powder"] = dict(air_cm3=v_air, O2_cm3=v_air * X_AIR, D_eff_m2_s=d_eff, tau_s=tau,
                         O2_mL_min_after={f"{t}min": X_AIR * v_air * 8 / math.pi ** 2 * math.exp(-t * 60 / tau) / tau * 60
                                          for t in (5, 10, 20)})
    # the stage's body: a virtual leak
    st = {}
    for v in STAGE["void_cm3"]:
        for tau_m in STAGE["tau_min"]:
            st[f"{v:g}cm3_tau{tau_m:g}min"] = {f"{t}min": X_AIR * v / tau_m * math.exp(-t / tau_m) for t in (10, 30, 60)}
    out["stage_O2_mL_min"] = st
    return out


def floor_ppm(q_lpm, o2_in_ml_min, grade="5.0"):
    return ARGON[grade]["O2"] + o2_in_ml_min / (q_lpm * 1000.0) * 1e6


def fig_floor(b, fname):
    q = np.logspace(np.log10(0.5), np.log10(30), 60)
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    ax = axs[0]
    P = b["permeation_mL_min"]
    comps = [("argon 5.0 (O2 <= 2 ppm)", np.full_like(q, ARGON["5.0"]["O2"]), "#257de0", "-"),
             ("argon 4.8 (O2 <= 3 ppm)", np.full_like(q, ARGON["4.8"]["O2"]), "#257de0", "--"),
             ("silicone gasket, permeation (dense / sponge x5)", P["gasket_O2_dense_silicone"] / (q * 1e3) * 1e6, "#f47230", "-"),
             (None, P["gasket_O2_sponge_x5"] / (q * 1e3) * 1e6, "#f47230", "--"),
             ("FKM O-rings, permeation", P["fkm_orings_O2"] / (q * 1e3) * 1e6, "#00b894", "-"),
             ("2 m polymer feed tube (20 Barrer)", P["feed_tubing_O2_1_to_20_barrer"][1] / (q * 1e3) * 1e6, "#6a4ce2", "-"),
             ]
    g = {(r["h_um"], r["where"], r["dp_mbar"]): r for r in b["gaps"]}
    for h, col in ((1.0, "#ee7fac"), (3.0, "#ec4647"), (10.0, "#f2a600")):
        comps.append((f"{h:g} um gap, whole seam, 5 mbar", g[(h, "whole seam", 5.0)]["O2_in_mL_min"] / (q * 1e3) * 1e6, col, "-"))
    st = b["stage_O2_mL_min"]["40cm3_tau60min"]["60min"]
    comps.append(("stage body, 40 cm3 air, tau 60 min, at 1 h", st / (q * 1e3) * 1e6, "#666666", ":"))
    for lab, y, c, ls in comps:
        ax.loglog(q, y, color=c, ls=ls, lw=1.6, label=lab)
    ax.set_xlabel("argon flow (L/min)")
    ax.set_ylabel("O2 it adds, well mixed (ppm)")
    ax.set_ylim(1e-3, 1e3)
    ax.axvspan(20, 27, color="#eeeeee", zorder=0)
    ax.text(21, 4e2, "purge /\ncross-flow", fontsize=7.5, color="#666666")
    ax.set_title("What each source adds to FT-1's box", loc="left")
    ax.legend(fontsize=7, loc="lower left")
    ax = axs[1]
    base = P["gasket_O2_sponge_x5"] + P["fkm_orings_O2"]
    cases = [("tight: argon 5.0 + permeation (sponge)", base, "#257de0"),
             ("+ 1 um gap along the whole seam", base + g[(1.0, "whole seam", 5.0)]["O2_in_mL_min"], "#ee7fac"),
             ("+ 3 um gap along the whole seam (worst size)", base + g[(3.0, "whole seam", 5.0)]["O2_in_mL_min"], "#ec4647"),
             ("+ 30 um gap, whole seam, box at 0 mbar (vent open)", base + g[(30.0, "whole seam", 0.0)]["O2_in_mL_min"], "#f2a600"),
             ("+ stage body (40 cm3, tau 60 min) at 1 h", base + st, "#666666")]
    for lab, s, c in cases:
        ax.loglog(q, [floor_ppm(x, s) for x in q], color=c, lw=1.8, label=lab)
    ax.loglog(q, [floor_ppm(x, base, "4.8") for x in q], color="#257de0", lw=1.2, ls="--", label="tight, argon 4.8")
    ax.axhline(100, color="#999999", lw=0.8, ls=":")
    ax.axhline(1000, color="#999999", lw=0.8, ls=":")
    ax.set_xlabel("argon flow (L/min)")
    ax.set_ylabel("steady O2 in the box (ppm)")
    ax.set_ylim(1, 3e3)
    ax.axvspan(20, 27, color="#eeeeee", zorder=0)
    ax.set_title("The floor: argon + what leaks in, over the flow", loc="left")
    ax.legend(fontsize=7, loc="upper right")
    fig.savefig(OUT / fname, dpi=130)
    plt.close(fig)


# ---------------- cube: pump-purge ----------------
def s_eff(p_mbar):
    """Effective pumping speed at the chamber (L/s): pump S0 (1 - p_ult/p) in series with the line's conductance
    (laminar Poiseuille + molecular, air at 20 C)."""
    S = PUMP["S0_L_s"] * max(1e-6, 1 - PUMP["p_ult_mbar"] / p_mbar)
    eta = 1.8e-5
    c = 0.0
    inv = 0.0
    for d, L in ((PUMP["line_d_mm"], PUMP["line_L_mm"]), (PUMP["hose_d_mm"], PUMP["hose_L_mm"])):
        d_m, L_m = d * 1e-3, L * 1e-3
        c_lam = math.pi * d_m ** 4 / (128 * eta * L_m) * (p_mbar * 100) * 1000       # L/s
        c_mol = 12.1 * (d / 10) ** 3 / (L / 10) / (1 + 4 * d / (3 * L))                # L/s, air, short-tube corrected
        c = c_lam + c_mol
        inv += 1 / c
    return 1 / (1 / S + inv)


def pump_down(V_L, p_to, p0=1013.0, q_load=0.0):
    """Time (s) to pump V from p0 to p_to (mbar) with s_eff(p) and a gas load q_load (mbar L/s)."""
    t, p = 0.0, p0
    while p > p_to:
        S = s_eff(p)
        dpdt = -(S * p - q_load) / V_L
        if dpdt >= 0:
            return math.inf
        dt = min(0.5, 0.01 * p / -dpdt)
        p += dpdt * dt
        t += dt
    return t


def pump_purge(V_L):
    rows = []
    fill = lambda pb: V_L * (1020.0 - pb) / 1013.0 / FILL_L_MIN * 60.0                # s, to +7 mbar
    q_leak = 1e-3 / 60.0 * V_L       # mbar L/s: the rate-of-rise acceptance (1e-3 mbar/min, seals.md section 7)
    for pb in (0.1, 0.5, 1.0, 5.0, 10.0, 20.0, 50.0):
        tp = pump_down(V_L, pb, q_load=q_leak)
        for target in (1000, 100, 10):
            x, n = X_AIR * 1e6, 0
            ar = ARGON["5.0"]["O2"]
            while x > target and n < 8:
                f = pb / 1020.0
                x_leak = X_AIR * 1e6 * min(1.0, q_leak / s_eff(pb) / pb)         # air from the leak in the residual gas
                x = x * f * (1 - min(1.0, q_leak / s_eff(pb) / pb)) + x_leak * f + ar * (1 - f)
                n += 1
            ok = x <= target
            rows.append(dict(base_mbar=pb, target_ppm=target, cycles=n if ok else None, pump_min=tp / 60, fill_min=fill(pb) / 60,
                             total_min=(n * (tp + fill(pb)) / 60) if ok else None, argon_L=(n * V_L * (1020 - pb) / 1013) if ok else None,
                             ppm_after=x))
    return rows


def cube_floor(V_L):
    fkm = sum(parker(PERM["fkm_O2_F"], d, X_AIR * 1.01325) for d in CUBE_ORINGS.values())     # std cc/s
    out = dict(fkm_O2_std_cc_s=fkm, fkm_O2_mL_min=fkm * 60,
               sealed_no_flow_ppm_per_h=fkm * 3600 / (V_L * 1000) * 1e6,
               sealed_no_flow_ppm_per_h_at_60C=fkm * 3.0 * 3600 / (V_L * 1000) * 1e6,
               leak_at_acceptance_ppm_per_h=X_AIR * 1e-3 / 60 * V_L / 1013 * 3600 / V_L * 1e6,
               with_27_L_min_ppm=ARGON["5.0"]["O2"] + fkm * 60 / 27000 * 1e6)
    return out


def fig_pump(V_L, rows, fname):
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    ax = axs[0]
    p = np.logspace(np.log10(0.02), np.log10(1013), 200)
    ax.semilogx(p, [s_eff(x) for x in p], color="#257de0", lw=1.8, label="at the cube (pump + 1/2 in. adapter + 1 m KF-25 hose)")
    ax.semilogx(p, [PUMP["S0_L_s"] * max(0, 1 - PUMP["p_ult_mbar"] / x) for x in p], color="#666666", lw=1.0, ls="--",
                label="pump alone (3 cfm, 1e-2 Torr)")
    ax.set_xlabel("pressure (mbar)")
    ax.set_ylabel("pumping speed (L/s)")
    ax.set_title(f"Pump-down of FT-1V's {V_L:.1f} L", loc="left")
    ax2 = ax.twinx()
    ts = [pump_down(V_L, x) / 60 for x in p[p < 1000]]
    ax2.semilogx(p[p < 1000], ts, color="#f47230", lw=1.8, label="time from 1 atm (min)")
    ax2.set_ylabel("time from 1 atm (min)", color="#f47230")
    ax2.spines["right"].set_visible(True)
    ax.legend(fontsize=7, loc="center left")
    ax = axs[1]
    for tgt, c in ((1000, "#257de0"), (100, "#f47230"), (10, "#00b894")):
        rr = [r for r in rows if r["target_ppm"] == tgt and r["total_min"] is not None]
        ax.semilogx([r["base_mbar"] for r in rr], [r["total_min"] for r in rr], "o-", color=c, lw=1.6, label=f"to {tgt} ppm")
        for r in rr:
            ax.annotate(f"{r['cycles']}", (r["base_mbar"], r["total_min"]), textcoords="offset points", xytext=(3, 4), fontsize=7, color=c)
    ax.set_xlabel("base pressure of each cycle (mbar)")
    ax.set_ylabel("pump + backfill time (min); label: cycles")
    ax.set_title("Cycles and time to an O2 level (argon 5.0)", loc="left")
    ax.legend(fontsize=7.5)
    fig.savefig(OUT / fname, dpi=130)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    b = box_budget()
    fig_floor(b, "o2_floor.png")
    # well-mixed table: ppm against flow for the leak classes
    flows = (1.0, 2.0, 5.0, 10.0, 20.0, 27.0)
    g = {(r["h_um"], r["where"], r["dp_mbar"]): r for r in b["gaps"]}
    P = b["permeation_mL_min"]
    base = P["gasket_O2_sponge_x5"] + P["fkm_orings_O2"]
    classes = {
        "tight (argon 5.0, permeation: sponge gasket + FKM)": base,
        "tight, dense silicone gasket": P["gasket_O2_dense_silicone"] + P["fkm_orings_O2"],
        "1 um gap along the whole seam, +5 mbar": base + g[(1.0, "whole seam", 5.0)]["O2_in_mL_min"],
        "3 um gap along the whole seam, +5 mbar (worst size)": base + g[(3.0, "whole seam", 5.0)]["O2_in_mL_min"],
        "10 um gap along the whole seam, +5 mbar": base + g[(10.0, "whole seam", 5.0)]["O2_in_mL_min"],
        "3 um gap, 20 mm defect, +5 mbar": base + g[(3.0, "20 mm defect", 5.0)]["O2_in_mL_min"],
        "30 um gap, whole seam, 0 mbar (vent open)": base + g[(30.0, "whole seam", 0.0)]["O2_in_mL_min"],
        "100 um gap, 20 mm defect, 0 mbar (vent open)": base + g[(100.0, "20 mm defect", 0.0)]["O2_in_mL_min"],
        "stage body 40 cm3, tau 60 min, at 1 h": base + b["stage_O2_mL_min"]["40cm3_tau60min"]["60min"],
        "stage body 10 cm3, tau 5 min, at 30 min": base + b["stage_O2_mL_min"]["10cm3_tau5min"]["30min"],
    }
    table = []
    for lab, s in classes.items():
        table.append(dict(case=lab, O2_in_mL_min=s, **{f"{q:g}_L_min_ppm_5.0": floor_ppm(q, s, "5.0") for q in flows},
                          **{f"{q:g}_L_min_ppm_4.8": floor_ppm(q, s, "4.8") for q in (2.0, 27.0)}))
    V = GEOM["cube_gas_L"]
    pp = pump_purge(V)
    fig_pump(V, pp, "pump_purge.png")
    res = dict(sources=SRC, inputs=dict(geom=GEOM, argon_ppm=ARGON, permeability=PERM, powder=POWDER, stage=STAGE, pump=PUMP,
                                        box_orings_id_mm=BOX_ORINGS, cube_orings_id_mm=CUBE_ORINGS),
               box=b, box_floor_table=table, cube_pump_purge=pp, cube_floor=cube_floor(V),
               cube_pump_down_min={f"{p:g}mbar": pump_down(V, p) / 60 for p in (100, 10, 1, 0.5, 0.1, 0.05)},
               s_eff_L_s={f"{p:g}mbar": s_eff(p) for p in (1000, 100, 10, 1, 0.1, 0.05)})
    (OUT / "o2_budget.json").write_text(json.dumps(res, indent=1, default=float))
    # markdown tables for results.md
    print("| source | O2 in (mL/min) | adds at 27 L/min (ppm) | at 2 L/min (ppm) |\n|---|---|---|---|")
    for k, v in P.items():
        vv = v if not isinstance(v, list) else v[1]
        print(f"| {k} | {vv:.2e} | {vv / 27000 * 1e6:.3g} | {vv / 2000 * 1e6:.3g} |")
    print()
    hdr = "| case | O2 in (mL/min) | " + " | ".join(f"{q:g} L/min" for q in flows) + " | 2 / 27 L/min, Ar 4.8 |"
    print(hdr + "\n|" + "---|" * (len(flows) + 3))
    for r in table:
        print(f"| {r['case']} | {r['O2_in_mL_min']:.2e} | " + " | ".join(f"{r[f'{q:g}_L_min_ppm_5.0']:.3g}" for q in flows)
              + f" | {r['2_L_min_ppm_4.8']:.3g} / {r['27_L_min_ppm_4.8']:.3g} |")
    print()
    print("| h (um) | where | dP (mbar) | outflow (mL/min) | Peclet | O2 in (mL/min) |\n|---|---|---|---|---|---|")
    for r in b["gaps"]:
        if r["where"] == "whole seam":
            print(f"| {r['h_um']:g} | {r['where']} | {r['dp_mbar']:g} | {r['outflow_mL_min']:.3g} | {r['peclet']:.3g} | {r['O2_in_mL_min']:.2e} |")
    print()
    print(json.dumps(dict(worst_gap=b["worst_gap_um_at_5mbar"], worst=b["worst_gap_O2_mL_min_whole_seam_5mbar"],
                          powder=b["powder"], cube_floor=res["cube_floor"], pump_down=res["cube_pump_down_min"],
                          s_eff=res["s_eff_L_s"]), indent=1, default=float))
    print("| base (mbar) | target (ppm) | cycles | pump (min) | fill (min) | total (min) | argon (L) | ppm after |\n|---|---|---|---|---|---|---|---|")
    for r in pp:
        f = lambda v, n=2: "-" if v is None else (f"{v:.{n}g}" if isinstance(v, float) else str(v))
        print(f"| {r['base_mbar']:g} | {r['target_ppm']} | {f(r['cycles'])} | {r['pump_min']:.2f} | {r['fill_min']:.2f} | "
              f"{f(r['total_min'], 3)} | {f(r['argon_L'], 3)} | {r['ppm_after']:.3g} |")


if __name__ == "__main__":
    main()
