"""Hot-swappable joints of the desktop LPBF (issue #260, PR #266): textbook sizing of every option.

Interfaces
  a. build module <-> chamber floor  (M50, L75): captive screws, zero-point modules, magnets, kinematic coupling
  b. build plate  <-> heater block   (S25, M50, L75) at 200-225 C: bare bayonet, bayonet + disc springs, drawbar,
                                       screws (EOS style), magnets
  c. heater-stack joint: M3 (M2.5 on S25) screws through Macor standoffs, with and without a disc spring
  d. reservoir on its dovetail (ball-plunger detents) and the recoater blade in its holder

Every number is printed with the equation it comes from and where that equation or value comes from:
  textbook  = Shigley 10th ed. (Budynas & Nisbett 2015), Roark 8th ed., Johnson "Contact Mechanics" (1985),
              DIN EN 16984 (Almen-Laszlo disc springs), Parker O-Ring Handbook ORD 5700, Maxwell pull F = B^2 A / 2 mu0
  vendor    = a vendor page or datasheet, URL given (collected 2026-11-19, see VENDOR below)
  assumed   = an engineering assumption, flagged as such
Geometry and masses: module_params.py and the model at commit REV (so the numbers do not move while the model is edited);
thermal results: analysis/out/thermal/thermal.json.

Run:  python desktop-lpbf/analysis/hotswap/joint_calcs.py
Out:  desktop-lpbf/analysis/out/hotswap/joint_calcs.md, joint_calcs.json
"""
from __future__ import annotations

import json
import math
import pathlib
import subprocess
import types

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]                       # desktop-lpbf/
REPO = ROOT.parent
OUT = ROOT / "analysis" / "out" / "hotswap"
REV = "1c7a977"                              # model snapshot the geometry is read from


def snapshot_module(name):
    src = subprocess.run(["git", "show", f"{REV}:desktop-lpbf/cad/{name}.py"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType(name)
    exec(compile(src, f"{REV}:{name}.py", "exec"), mod.__dict__)
    return mod


MP = snapshot_module("module_params")
THERMAL = json.loads((ROOT / "analysis" / "out" / "thermal" / "thermal.json").read_text())

G = 9.81
MU0 = 4e-7 * math.pi
LBF = 4.44822
INCH = 25.4

# --------------------------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------------------------
SRC = {
    "shig": "Shigley's Mechanical Engineering Design, 10th ed. (Budynas & Nisbett, 2015), ch. 8",
    "shig_t81": "Shigley Table 8-1 (tensile-stress area A_t, minor-diameter area A_r)",
    "shig_817": "Shigley Eq. 8-17 (bolt stiffness k_b = A_d A_t E / (A_d l_t + A_t l_d))",
    "shig_820": "Shigley Eq. 8-20 (frustum member stiffness, 30 deg cone)",
    "shig_823": "Shigley Eq. 8-23 + Table 8-8 (Wileman member stiffness k_m = E d A exp(B d / l))",
    "shig_824": "Shigley Eq. 8-24/8-25 (joint constant C = k_b / (k_b + k_m); F_b = C P + F_i)",
    "shig_827": "Shigley Eq. 8-27 + Table 8-15 (T = K F_i d; K = 0.30 non-plated/dry, 0.18 lubricated)",
    "shig_829": "Shigley Eq. 8-29 (load factor against separation n_0 = F_i / (P (1 - C)))",
    "shig_831": "Shigley Eq. 8-31 (F_i = 0.75 F_p for reusable joints; F_p = A_t S_p)",
    "shig_thread": "Shigley Sec. 8-2, Eq. 8-8 (thread root shear tau = 3 F / (pi d n_t p), nut: d = major dia)",
    "shig_hertz": "Shigley Sec. 3-19 / Johnson, Contact Mechanics (1985) ch. 4: sphere on flat, a = (3 F R / 4 E*)^(1/3), p0 = 3 F / (2 pi a^2), delta = a^2 / R",
    "johnson_yield": "Johnson (1985) Sec. 6.2: first yield in a Hertz point contact at p0 = 1.60 Y (nu = 0.3)",
    "hamrock": "Hamrock & Brewe (1983), elliptical-contact approximations (Hamrock, Fundamentals of Fluid Film Lubrication, ch. 17)",
    "roark": "Roark's Formulas for Stress and Strain, 8th ed., Table 8.1 (guided cantilever: M = 6 E I delta / L^2)",
    "almen": "DIN EN 16984:2017 (Almen-Laszlo disc-spring equations, ex DIN 2092), no contact flats",
    "parker": "Parker O-Ring Handbook ORD 5700, Sec. 5 (dynamic friction F = f_c L_p + f_h A_p); f_c read from its compression-friction chart, approximate",
    "maxwell": "Maxwell pull F = B^2 A / (2 mu0) per pole face; magnetic circuit Phi = MMF / sum(R)",
    "slocum": "Slocum, Kinematic couplings: a review, Int. J. Mach. Tools Manuf. 50 (2010) 310-327, doi:10.1016/j.ijmachtools.2009.10.006",
    "asm6061": "ASM / Aluminum Association typical properties of 6061-T6 at temperature after 10,000 h exposure (also on MatWeb): "
               "YS 262 / 214 / 103 / 34 MPa at 100 / 149 / 204 / 260 C",
    "corning": "Corning Macor datasheet: compressive strength 345 MPa, k 1.46 W/m K, alpha 9.3e-6 /K, E 66.9 GPa",
    "smi": "Schnorr / SMI spring-material temperature limits: 1.4310 (301/302) to ~200-250 C, 17-7 PH to ~300 C, Inconel 718 / X-750 to ~600 C",
}

# vendor facts (all collected 2026-11-19; the research notes are in the PR thread, numbers are the vendors' claims)
VENDOR = {
    "schunk_nse_am": dict(name="SCHUNK NSE-AM mini 78-20", d_mm=78, h_mm=20, pull_in_N=1500, repeat_um=5, t_max_C=200,
                          note="spring-locked, air (6 bar) to open; sealed; inert-gas rated; for SLM set-up",
                          url="https://www.magazine-industry-usa.com/news/21351-clamping-module-minimizes-set-up-times-in-3d-printing"),
    "schunk_nse_ht": dict(name="SCHUNK NSE-HT mini 88-20", d_mm=88, h_mm=20, pull_in_N=500, pull_in_turbo_N=2500, repeat_um=5, t_max_C=200,
                          mass_kg=1.0, note="spring assembly, air only to open; used on a DMG MORI LASERTEC 30 Dual SLM with a 200 C bed",
                          url="https://schunk.com/us/en/p/000000000001460874"),
    "schunk_nse_mini90": dict(name="SCHUNK NSE mini 90 (manual NSE-M mini 90: $1,430)", d_mm=90, h_mm=20, pull_in_N=500, pull_in_turbo_N=1500,
                              repeat_um=5, mass_kg=1.0, price_usd=1430, url="https://www.mrosupply.com/machining/6171221_435140_schunk/"),
    "stark_d085": dict(name="STARK.easyclick D085", d_mm=85, h_mm=19, clamp_N=5000, retention_N=10000, lateral_N=2500, repeat_um=10,
                       t_max_C=150, mass_kg=0.62, note="FKM 'ET' version to 150 C (NBR to 80 C); 4-6 bar release; +/-0.4 mm capture",
                       url="https://www.carrlane.com/Portals/0/Media/e89c4c29-6e4d-4f1d-929f-f1624b55509c.pdf"),
    "zimmer_spn062": dict(name="Zimmer SPN062", pull_in_N=2000, repeat_um=5, t_max_C=70, mass_kg=0.39,
                          url="https://www.zimmer-group.com/fileadmin/pim/MER/GD/PG/MER_GD_PG_SPN062E6SD-B__SEN__APD__V1.pdf"),
    "erowa_its50": dict(name="EROWA ITS Chuck 50 RSA", pull_in_N=2800, repeat_um=2, url="https://www.erowa.com/en/products/chuck-50-rsa/pd/008186"),
    "mcm_5679K95": dict(name="McMaster 5679K95 NdFeB pot magnet, Ø25 x 7", pull_N=44 * LBF, t_max_C=79, url="https://www.mcmaster.com/5679K95/"),
    "kendrion_pem2525a": dict(name="Kendrion PEM2525A fail-safe holding magnet, Ø25 x 25", pull_N=140, coil_class="E (120 C)", duty="15 % ED",
                              url="https://www.kendrion.com/fileadmin/user_upload/Product_Finder/Solenoid_Technology/Solenoids_DS_EW/Datasheets/Permanent-Haftmagnet-1266251-DB.PDF"),
    "kendrion_d55": dict(name="Kendrion D55 permanent electro holding magnet, Ø55", pull_N=420, coil_class="E (120 C)", duty="25 % ED",
                         url="https://www.kendrion.com/en/productfinder/group/product/holding-magnets/01050002"),
    "kendrion_gtb040": dict(name="Kendrion GTB040 plain electro holding magnet, Ø40", pull_N=475, coil_class="B (130 C)", duty="100 % ED, 5.1 W",
                            note="drops the part when power is off",
                            url="https://www.kendrion.com/en/productfinder/group/product/holding-magnets/gtb040100001"),
    "ms_gmh": dict(name="Magnet-Schultz G MH plain holding magnets (force vs air gap, N)",
                   gaps_mm=[0.0, 0.1, 0.16, 0.25, 0.4, 1.0],
                   d25=[135, 36.3, 18.2, 9.8, 3.5, 0.9], d40=[470, 275, 157, 80, 30, 6.2], d50=[720, 569, 373, 216, 93, 18],
                   url="https://astat.pl/pliki/Komponenty_automatyki_przemyslowej/Elektromagnesy_mocujace/karta-katalogowa-GMH_GZZ.pdf"),
    "magswitch_ppe30": dict(name="Magswitch PPe30 (switchable PM, 536 N)", gaps_mm=[0.0, 0.2, 0.3, 0.5, 1.0], frac=[1.0, 0.58, 0.53, 0.39, 0.25],
                            shear_frac=0.22, t_max_C=80, url="https://downloads.magswitch.com/products/81401683-PPe30-Spec-Sheet-1101911.pdf"),
    "eclipse_epm_chuck": dict(name="Eclipse electro-permanent chuck (large poles)", gaps_mm=[0.0, 0.2, 0.5, 0.7, 1.0], frac=[1.0, 0.88, 0.62, 0.50, 0.41],
                              url="https://www.eclipsemagnetics.com/site/assets/files/2396/magnetic_workholding_brochure.pdf"),
    "goudsmit_430": dict(name="430 stainless target: 60-75 % of low-carbon steel force (Goudsmit), 65 % (SCHUNK); 316 and Al: 0 %",
                         frac=0.65, url="https://www.goudsmitmagnetics.com/uploads/pdf/en_GMSD_IM_HGE_4223.pdf"),
    "magnet_temps": dict(name="Magnet grades: max operating temp (C) and reversible Br coefficient (%/K)",
                         grades={"NdFeB N": (80, -0.12), "NdFeB H": (120, -0.12), "NdFeB SH": (150, -0.12), "NdFeB UH": (180, -0.12),
                                 "NdFeB EH": (200, -0.12), "NdFeB AH": (230, -0.12), "SmCo5": (250, -0.04), "Sm2Co17": (300, -0.03),
                                 "AlNiCo (cast)": (550, -0.02)},
                         url="https://www.adamsmagnetic.com/wp-content/uploads/ADAMS-Materials-Chart-of-Properties-7-25.pdf"),
    "mcm_85015A47": dict(name="McMaster 85015A47 ball-nose spring plunger M6, 2 lbf extended / 2.9 lbf compressed, Ø3.5 ball",
                         f_ext_N=2.0 * LBF, f_comp_N=2.9 * LBF, url="https://www.mcmaster.com/85015A47/"),
    "mcm_95966A705": dict(name="McMaster 95966A705 captive panel screw M6 x 20, 18-8, 6 mm thread, Ø4.2 reduced shank, Ø10 knurled head",
                          url="https://www.mcmaster.com/95966A705/"),
    "mcm_97125K111": dict(name="McMaster 97125K111 718-nickel disc spring for 0.138 in. shaft: ID 0.142, OD 0.281, t 0.021, ht 0.033 in.; "
                               "95 lbf at 0.004 in. deflection, 135 lbf flat; to 1100 F", di=0.142 * INCH, de=0.281 * INCH, t=0.021 * INCH,
                          l0=0.033 * INCH, work_N=95 * LBF, s_work=0.004 * INCH, flat_N=135 * LBF, price_usd=1.69,
                          url="https://www.mcmaster.com/97125K111/"),
    "mcm_9713K53": dict(name="McMaster 9713K53 302-stainless disc spring for 1/8 in. shaft: ID 0.125, OD 0.25, t 0.009, ht 0.017 in.; "
                             "11 lbf at 0.004 in., 17 lbf flat", di=0.125 * INCH, de=0.25 * INCH, t=0.009 * INCH, l0=0.017 * INCH,
                        work_N=11 * LBF, s_work=0.004 * INCH, flat_N=17 * LBF, url="https://www.mcmaster.com/9713K53/"),
    "carrlane_blp6": dict(name="Carr Lane 6 mm ball-lock pin: pull-out ~230 lb, double shear 4,000 lb (2:1 SF stated)",
                          pullout_N=230 * LBF, shear_N=4000 * LBF,
                          url="https://www.carrlane.com/engineering-resources/technical-information/ball-lock-pins-engineering-application/ball-lock-pin-strength-data"),
    "onrobot_sd": dict(name="OnRobot Screwdriver: 0.15-5 N m, M1.6-M6, magnetic screws only", t_max_Nm=5.0,
                       url="https://onrobot.com/storage/datasheets/screwdriver/datasheet_screwdriver_v1.7_en.pdf"),
}

# --------------------------------------------------------------------------------------------
# materials (room temperature unless noted)
# --------------------------------------------------------------------------------------------
MAT = {
    "al6061": dict(E=68.9e3, nu=0.33, Sy=276.0, Su=310.0, alpha=23.6e-6, k=167.0, Sy_200=103.0, Sy_225=77.0, E_200=62.0e3),
    "ss316": dict(E=193e3, nu=0.30, Sy=170.0, alpha=16.5e-6, k=17.0),            # 316L annealed; alpha mean 20-200 C
    "a4_50": dict(E=193e3, nu=0.30, Sp=210.0, Su=500.0, alpha=16.5e-6, k=17.0, Sp_200=160.0),   # ISO 3506 class 50 (Rp0.2 = 210)
    "a2_50": dict(E=193e3, nu=0.30, Sp=210.0, Su=500.0, alpha=17.3e-6, k=16.2),
    "ti64": dict(E=114e3, nu=0.34, Sp=830.0, Su=900.0, alpha=9.2e-6, k=7.5, Sp_200=650.0),
    "macor": dict(E=66.9e3, nu=0.29, Sc=345.0, alpha=9.3e-6, k=1.46),
    "ss440c": dict(E=200e3, nu=0.28, Sy=1900.0),
    "si3n4": dict(E=310e3, nu=0.27),
    "ph17_4_h900": dict(E=196e3, nu=0.27, Sy=1170.0),
    "inconel718": dict(E=200e3, nu=0.29),
    "ss302_spring": dict(E=193e3, nu=0.30),
}
THREAD = {  # d, pitch, A_t, A_r (mm^2), minor dia d3 -- Shigley Table 8-1 / ISO 724
    "M2.5": dict(d=2.5, p=0.45, At=3.39, Ar=2.98, d3=1.948),
    "M3": dict(d=3.0, p=0.50, At=5.03, Ar=4.47, d3=2.387),
    "M4": dict(d=4.0, p=0.70, At=8.78, Ar=7.75, d3=3.141),
    "M5": dict(d=5.0, p=0.80, At=14.2, Ar=12.7, d3=4.019),
    "M6": dict(d=6.0, p=1.00, At=20.1, Ar=17.9, d3=4.773),
}
K_DRY, K_LUBE = 0.30, 0.18          # Shigley Table 8-15 (dry stainless taken as 'non-plated'); nickel/MoS2 anti-seize ~ 'lubricated'

R = []                               # report lines
J = {}                               # json


def h(title, level=2):
    R.append(f"\n{'#' * level} {title}\n")


def line(s=""):
    R.append(s)


def table(rows, head):
    R.append("| " + " | ".join(head) + " |")
    R.append("|" + "---|" * len(head))
    for r in rows:
        R.append("| " + " | ".join(str(x) for x in r) + " |")
    R.append("")


def f(x, n=1):
    return f"{x:,.{n}f}"


# --------------------------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------------------------
def e_star(m1, m2):
    a, b = MAT[m1], MAT[m2]
    return 1.0 / ((1 - a["nu"] ** 2) / a["E"] + (1 - b["nu"] ** 2) / b["E"])


def hertz_sphere_flat(F, R_ball, Es):
    a = (3 * F * R_ball / (4 * Es)) ** (1 / 3)
    p0 = 3 * F / (2 * math.pi * a ** 2)
    d = a ** 2 / R_ball
    return dict(a=a, p0=p0, delta=d, k=2 * Es * a)     # k = dF/d(delta)


def hertz_elliptic(F, Rx, Ry, Es):
    """Hamrock & Brewe approximations; Rx <= Ry effective radii (mm), F (N), Es (MPa)."""
    Rr = 1.0 / (1.0 / Rx + 1.0 / Ry)
    alpha_r = Ry / Rx
    k = alpha_r ** (2 / math.pi)
    Ek = 1 + (math.pi / 2 - 1) / alpha_r
    Fk = math.pi / 2 + (math.pi / 2 - 1) * math.log(alpha_r)
    a = (6 * k ** 2 * Ek * F * Rr / (math.pi * Es)) ** (1 / 3)      # semi-major (along y)
    b = (6 * Ek * F * Rr / (math.pi * k * Es)) ** (1 / 3)
    p0 = 3 * F / (2 * math.pi * a * b)
    delta = Fk * (9 / (2 * Ek * Rr) * (F / (math.pi * k * Es)) ** 2) ** (1 / 3)
    return dict(a=a, b=b, p0=p0, delta=delta)


def frustum_k(E, d, D, t):
    """Shigley Eq. 8-20: one frustum, 30 deg half-angle, bolt dia d, bearing dia D, thickness t."""
    num = 0.5774 * math.pi * E * d
    den = math.log((1.155 * t + D - d) * (D + d) / ((1.155 * t + D + d) * (D - d)))
    return num / den


def wileman(E, d, l, mat):
    A, B = {"steel": (0.78715, 0.62873), "al": (0.79670, 0.63816)}[mat]
    return E * d * A * math.exp(B * d / l)


def disc_spring(De, Di, t, h0, E, nu, s):
    """DIN EN 16984 (Almen-Laszlo), no contact flats: force and stresses at deflection s (mm)."""
    dl = De / Di
    K1 = (1 / math.pi) * ((dl - 1) / dl) ** 2 / ((dl + 1) / (dl - 1) - 2 / math.log(dl))
    K2 = (6 / math.pi) * ((dl - 1) / math.log(dl) - 1) / math.log(dl)
    K3 = (3 / math.pi) * (dl - 1) / math.log(dl)
    c = 4 * E / (1 - nu ** 2)
    Fv = c * t ** 4 / (K1 * De ** 2) * (s / t) * ((h0 / t - s / t) * (h0 / t - s / (2 * t)) + 1)
    sOM = -c * t ** 2 / (K1 * De ** 2) * (s / t) * 3 / math.pi
    sII = -c * t ** 2 / (K1 * De ** 2) * (s / t) * (K2 * (h0 / t - s / (2 * t)) - K3)
    sIII = -c * t ** 2 / (K1 * De ** 2) * (1 / dl) * (s / t) * ((K2 - 2 * K3) * (h0 / t - s / (2 * t)) - K3)
    return dict(F=Fv, sOM=sOM, sII=sII, sIII=sIII)


def gap_interp(gaps, vals, g):
    """log-linear interpolation of a force-vs-gap curve (vendor table)."""
    if g <= gaps[0]:
        return vals[0]
    for (g0, v0), (g1, v1) in zip(zip(gaps, vals), zip(gaps[1:], vals[1:])):
        if g <= g1:
            t = (g - g0) / (g1 - g0)
            return math.exp(math.log(v0) + t * (math.log(v1) - math.log(v0)))
    return vals[-1]


# --------------------------------------------------------------------------------------------
# a. build module <-> chamber floor
# --------------------------------------------------------------------------------------------
def module_masses(key):
    """Module body (spigot + flange + tube), gland flange, piston stack: from module_params (316L 7990, 6061 2700 kg/m3).
    Checked against analysis/out/mass.json for M50: body 1.579 kg there, 1.62 kg here."""
    m = MP.MODULES[key]
    Rb = m["bore"] / 2
    pr = MP.PORT_D / 2 - MP.SPIGOT_FIT
    zf = -MP.FLOOR_T
    z_stop = MP.Z_P_MIN - MP.STACK
    V_sp = math.pi * (pr ** 2 - Rb ** 2) * MP.FLOOR_T
    V_fl = (math.pi * (MP.FLANGE_D / 2) ** 2 - math.pi * Rb ** 2) * MP.FLANGE_T + 2 * (MP.TAB_X - MP.FLANGE_D / 2 + 2) * 24 * MP.FLANGE_T
    V_tb = math.pi * ((Rb + m["wall"]) ** 2 - Rb ** 2) * ((zf - MP.FLANGE_T) - z_stop)
    V_bf = math.pi * ((Rb + m["wall"] + 6) ** 2 - (MP.ROD_OD / 2) ** 2) * MP.BOT_FLANGE_T
    body = (V_sp + V_fl + V_tb) * 7.99e-6
    gland = V_bf * 7.99e-6
    Rp, Rbk = m["plate_d"] / 2, m["block_d"] / 2
    al = (math.pi * Rp ** 2 * MP.PLATE_T + math.pi * Rbk ** 2 * MP.BLOCK_T + 0.85 * math.pi * Rbk ** 2 * MP.HEAD_T) * 2.70e-6
    rod = 0.083                       # rod, rod end, striker, heaters, thermocouples (mass.json M50 values; same for all)
    return dict(body=body, gland=gland, piston=al + rod, total=body + gland + al + rod + 0.03)


def module_loads(key):
    m = module_masses(key)
    W = m["total"] * G
    # Parker ORD 5700: dynamic O-ring friction F_c = f_c * L_p; f_c ~ 2.5 lbf/in for 0.139 in. CS, 15-20 % squeeze, 70-80 Shore A
    fc = 2.5 * LBF / INCH                                      # N/mm  (assumed reading of Parker's chart)
    gland_run = 2 * fc * math.pi * MP.ROD_OD                   # two 2-114 O-rings on the 5/8 in. rod
    gland_break = 2.0 * gland_run                              # break-out after rest ~2x running (assumed, Parker Sec. 5)
    bore_seal = {"S25": 6.0, "M50": 10.0, "L75": 15.0}[key]    # felt + PTFE scraper drag (assumed)
    port_oring = fc * math.pi * MP.PORT_D                      # 2-238 in the Ø96 port: insertion / extraction
    A_seal = math.pi / 4 * MP.PORT_D ** 2 - math.pi / 4 * MP.ROD_OD ** 2
    over = 0.002 * A_seal                                      # +20 mbar = 0.002 MPa, pushes the module down (separating)
    vac = 0.101325 * A_seal                                    # full vacuum inside: pushes the module up (seating)
    magnet = VENDOR["mcm_5679K95"]["pull_N"]                   # Z-arm magnet breaking away while the collar holds the piston
    cases = {
        "LC1 build stroke at break-out (+20 mbar)": W + bore_seal + gland_break + over,
        "LC2 Z-magnet release, piston held by its collar": W + magnet,
        "LC3 transit, +3 m/s2 down": m["total"] * (G + 3.0),
        "LC4 full vacuum (seating, negative)": W - vac,
    }
    shear = m["total"] * 2.0
    return dict(m=m, W=W, gland_run=gland_run, gland_break=gland_break, bore_seal=bore_seal, port_oring=port_oring,
                over=over, vac=vac, magnet=magnet, cases=cases, P_sep=max(cases.values()),
                P_sep_no_magnet=max(v for k, v in cases.items() if "LC2" not in k), shear=shear)


def captive_screws(P_total, n=2):
    """Option (i): 95966A705 captive M6 (18-8, A2-50) into 91732A782 M6x12 helical inserts in the 6061 floor."""
    th = THREAD["M6"]
    mat = MAT["a2_50"]
    A_red = math.pi / 4 * 4.2 ** 2                              # reduced shank Ø4.2 (McMaster)
    Fp_thread = th["At"] * mat["Sp"]
    Fp_shank = A_red * mat["Sp"]
    Fp = min(Fp_thread, Fp_shank)
    Fi = 0.75 * Fp                                               # Shigley Eq. 8-31
    # stiffness: 10 mm 316L flange under the Ø10 head; 14 mm reduced shank, d/2 = 3 mm effective thread (tapped member)
    l_d, l_t = 14.0, 3.0
    kb = mat["E"] / (l_d / A_red + l_t / th["At"])              # Shigley Eq. 8-17 form, reduced shank
    lp = MP.FLANGE_T + th["d"] / 2                              # effective grip, tapped joint (Shigley Table 8-7)
    k1 = frustum_k(MAT["ss316"]["E"], th["d"], 10.0, lp / 2)    # 316L flange, from the head
    k2a = frustum_k(MAT["ss316"]["E"], th["d"], 1.5 * th["d"] + 2 * 0.5774 * 3.0, lp / 2 - 3.0)
    k2b = frustum_k(MAT["al6061"]["E"], th["d"], 1.5 * th["d"], 3.0)
    km = 1 / (1 / k1 + 1 / k2a + 1 / k2b)
    km_wil_steel = wileman(MAT["ss316"]["E"], th["d"], lp, "steel")
    km_wil_al = wileman(MAT["al6061"]["E"], th["d"], lp, "al")
    C = kb / (kb + km)
    P = P_total / n
    n0 = Fi / (P * (1 - C))                                       # Shigley Eq. 8-29
    np_ = Fp / (C * P + Fi)                                       # yielding factor (Shigley Eq. 8-28 form)
    T_dry, T_lube = K_DRY * Fi * th["d"] / 1000, K_LUBE * Fi * th["d"] / 1000
    # thread stripping: only 6 mm of the screw's thread is in the 12 mm insert (McMaster); insert in 6061 at STI major ~ d + 1.3P
    Le = 6.0
    D_sti = th["d"] + 2 * 0.6495 * th["p"]
    tau_al = 3 * (Fi + C * P) / (math.pi * D_sti * Le)
    tau_ins = 3 * (Fi + C * P) / (math.pi * th["d"] * Le)
    tau_root = 3 * (Fi + C * P) / (math.pi * th["d3"] * Le)
    # thermal preload change, 20 -> 85 C: members 10 mm 316L + 3 mm 6061, bolt (18-8) over l' = 13 mm
    dT = 65.0
    d_mem = (MAT["ss316"]["alpha"] * 10.0 + MAT["al6061"]["alpha"] * 3.0) * dT
    d_bolt = mat["alpha"] * lp * dT
    dF_th = (d_mem - d_bolt) * kb * km / (kb + km)
    return dict(Fp=Fp, Fp_thread=Fp_thread, Fp_shank=Fp_shank, Fi=Fi, kb=kb, km=km, km_wil_steel=km_wil_steel, km_wil_al=km_wil_al,
                C=C, P=P, n0=n0, np=np_, T_dry=T_dry, T_lube=T_lube, tau_al=tau_al, tau_ins=tau_ins, tau_root=tau_root,
                tau_al_allow=0.577 * MAT["al6061"]["Sy"], tau_ss_allow=0.577 * mat["Sp"], dF_th=dF_th, D_sti=D_sti, lp=lp)


def kinematic(Fp_total, D_ball, ball, groove, particle_um=(20, 30, 63), Hp=1300.0):
    """Three-groove coupling, 90 deg vees: 6 contacts, each normal at 45 deg to the preload."""
    N = Fp_total / (3 * 2 * math.cos(math.radians(45)))
    Es = e_star(ball, groove)
    hz = hertz_sphere_flat(N, D_ball / 2, Es)
    allow = 1.60 * MAT[groove].get("Sy", 1e9)
    kz = 6 * hz["k"] * math.cos(math.radians(45)) ** 2         # vertical stiffness of the coupling, N/mm
    out = dict(N=N, Es=Es, a=hz["a"], p0=hz["p0"], p0_allow=allow, delta_um=hz["delta"] * 1e3, kz_N_um=kz / 1e3, n_yield=allow / hz["p0"])
    # trapped Al powder grain flattened between steel surfaces until the local (flat-punch) indentation pressure equals its
    # hardness: t^3 = V pi H^2 / (4 E*^2), r = 2 E* t / (pi H); estimate of the residual offset (assumed H = 1.3 GPa)
    errs = {}
    for s in particle_um:
        V = math.pi / 6 * (s * 1e-3) ** 3
        t = (V * math.pi * Hp ** 2 / (4 * Es ** 2)) ** (1 / 3)
        r = 2 * Es * t / (math.pi * Hp)
        errs[s] = dict(t_um=t * 1e3, r_um=r * 1e3, F_crush_N=Hp * math.pi * r ** 2)
    out["particle"] = errs
    return out


def magnet_effective(pull_N, gap_mm, curve, T_C, grade, target_frac):
    """Rated pull x target-material factor x gap factor (vendor curve) x reversible temperature factor (Br^2)."""
    gaps, vals = curve
    gf = gap_interp(gaps, vals, gap_mm) / vals[0]
    tmax, a_br = VENDOR["magnet_temps"]["grades"][grade]
    tf = (1 + a_br / 100 * (T_C - 20)) ** 2
    return dict(F=pull_N * target_frac * gf * tf, gap_factor=gf, temp_factor=tf, over_temp=T_C > tmax, t_max=tmax)


# --------------------------------------------------------------------------------------------
# b. plate <-> heater block
# --------------------------------------------------------------------------------------------
BAYONET_R = 6.0


def plate_geom(key):
    m = MP.MODULES[key]
    Rp, Rb = m["plate_d"] / 2, m["block_d"] / 2
    r_sock = BAYONET_R + 2.9
    A_face = math.pi * (Rb ** 2 - r_sock ** 2)
    mass = math.pi * Rp ** 2 * MP.PLATE_T * 2.70e-6
    return dict(Rp=Rp, Rb=Rb, A_face=A_face, mass=mass, W=mass * G)


def plate_options(key, p_contact=0.10):
    g = plate_geom(key)
    F_req = p_contact * g["A_face"]                       # graphite-foil contact pressure (assumed 0.1 MPa)
    drag, strike, z_lever = 10.0, 50.0, MP.PLATE_T        # recoater loads act at the plate top, 10 mm above the face
    # tipping about the far edge of the face: preload (central) must exceed n * F * z / R
    F_tip_drag = 3 * drag * z_lever / g["Rb"]
    F_tip_strike = 2 * strike * z_lever / g["Rb"]
    # (i) bare bayonet: gravity only; lugs 0.2 mm under the ledge -> worst edge lift if it tips about the far edge
    lug_r = BAYONET_R + 1.0
    lift_edge = 0.2 * (2 * g["Rb"]) / (g["Rb"] + lug_r)
    out = dict(F_req=F_req, A_face=g["A_face"], W=g["W"], F_tip_drag=F_tip_drag, F_tip_strike=F_tip_strike, bare_lift_mm=lift_edge,
               bare_pressure_kPa=g["W"] / g["A_face"] * 1e3)
    # (ii) bayonet + disc springs (718, 97125K111 geometry; E 200 GPa at RT, ~190 GPa at 225 C)
    v = VENDOR["mcm_97125K111"]
    h0 = v["l0"] - v["t"]
    sp_check = disc_spring(v["de"], v["di"], v["t"], h0, MAT["inconel718"]["E"], MAT["inconel718"]["nu"], v["s_work"])
    sp_flat = disc_spring(v["de"], v["di"], v["t"], h0, MAT["inconel718"]["E"], MAT["inconel718"]["nu"], h0)
    target = max(F_req, F_tip_strike) * 1.25
    # one spring per column, columns in parallel; deflection for the target force per column (bisection)
    n_par = max(1, math.ceil(target / (0.75 * v["work_N"])))
    Fc = target / n_par
    lo, hi = 0.0, h0
    for _ in range(60):
        mid = (lo + hi) / 2
        if disc_spring(v["de"], v["di"], v["t"], h0, 190e3, 0.29, mid)["F"] < Fc:
            lo = mid
        else:
            hi = mid
    s_need = lo
    st = disc_spring(v["de"], v["di"], v["t"], h0, 190e3, 0.29, s_need)
    # twist torque on ramps: rise 0.4 mm over 40 deg at the lug radius, friction 0.3 (dry, 200 C)
    r_m = BAYONET_R + 1.25
    tan_a = 0.4 / (r_m * math.radians(40))
    T_twist = target * r_m / 1000 * math.tan(math.atan(tan_a) + math.atan(0.3))
    # lug: 6 x 1.8 mm cantilever, projecting 2.5 mm from the spigot, load at mid-projection
    Mlug = target / 3 * 1.25
    s_lug = Mlug / (6 * 1.8 ** 2 / 6)
    out["bayonet_springs"] = dict(spring="McMaster 97125K111 (718 Ni)", check_F_at_work=sp_check["F"], vendor_work_N=v["work_N"],
                                  check_flat=sp_flat["F"], vendor_flat_N=v["flat_N"], target_N=target, n_parallel=n_par, s_mm=s_need,
                                  sOM=st["sOM"], sII=st["sII"], sIII=st["sIII"], T_twist_Nm=T_twist, tan_ramp=tan_a,
                                  lug_bending_MPa=s_lug, lug_allow_200=MAT["al6061"]["Sy_200"], lug_allow_225=MAT["al6061"]["Sy_225"])
    # (iii) drawbar: 6 balls Ø4 (Si3N4) in a conforming groove (r_g = 0.54 D) on a 17-4 PH H900 pull stud collar Ø8
    Nb = target / (6 * math.cos(math.radians(45)))
    Rx = 1 / (1 / 2.0 + 1 / 4.0)                          # ball 2 mm against the Ø8 collar (convex)
    Ry = 1 / (1 / 2.0 - 1 / (0.54 * 4.0))                 # ball 2 mm in a 2.16 mm groove (conforming)
    hz_b = hertz_elliptic(Nb, Rx, Ry, e_star("si3n4", "ph17_4_h900"))
    hz_flat = hertz_sphere_flat(Nb, 2.0, e_star("si3n4", "ph17_4_h900"))
    G_316 = MAT["ss316"]["k"] * math.pi / 4 * 4.0 ** 2 * 1e-6 / 0.130
    G_ti = MAT["ti64"]["k"] * math.pi / 4 * 4.0 ** 2 * 1e-6 / 0.130
    out["drawbar"] = dict(F_clamp=target, N_ball=Nb, p0_groove=hz_b["p0"], p0_flat=hz_flat["p0"], p0_allow_17_4=1.6 * MAT["ph17_4_h900"]["Sy"],
                          release_push_N=1.2 * target + 20.0, Q_316_W=G_316 * (225 - 65), Q_ti_W=G_ti * (225 - 65))
    # (iv) 3 x M4 316 (A4-50) through the plate into M4x6 helical inserts in the block
    th = THREAD["M4"]
    sc = MAT["a4_50"]
    Fi = 0.75 * th["At"] * sc["Sp"]
    l_eff = (MP.PLATE_T - 4.5) + th["d"] / 2
    kb = th["At"] * sc["E"] / l_eff
    km = wileman(MAT["al6061"]["E"], th["d"], l_eff, "al")
    k_eff = kb * km / (kb + km)
    dF = (MAT["al6061"]["alpha"] - sc["alpha"]) * 180.0 * l_eff * k_eff
    F_hot = Fi + dF
    A_bear = math.pi / 4 * (7.0 ** 2 - 4.5 ** 2)
    out["screws_M4"] = dict(Fi=Fi, total=3 * Fi, T_dry=K_DRY * Fi * th["d"] / 1000, T_lube=K_LUBE * Fi * th["d"] / 1000,
                            dF_200=dF, F_hot=F_hot, s_screw_hot=F_hot / th["At"], Sp_200=sc["Sp_200"], bearing_hot=F_hot / A_bear,
                            Sy_al_200=MAT["al6061"]["Sy_200"], k_eff=k_eff)
    # (v) magnet at 225 C: Sm2Co17 pot, scaled from the NdFeB 5679K95 rating by (Br ratio)^2, 430 insert, foil gap 0.13 mm
    base = VENDOR["mcm_5679K95"]["pull_N"] * (1.05 / 1.20) ** 2
    t_f = (1 - 0.0003 * (225 - 20)) ** 2
    gap_f = gap_interp(VENDOR["ms_gmh"]["gaps_mm"], VENDOR["ms_gmh"]["d25"], 0.13) / VENDOR["ms_gmh"]["d25"][0]
    F1 = base * t_f * VENDOR["goudsmit_430"]["frac"] * gap_f
    out["magnet"] = dict(F_per_magnet=F1, n_needed=math.ceil(target / F1), gap_factor=gap_f, temp_factor=t_f)
    return out


# --------------------------------------------------------------------------------------------
# c. heater stack joint
# --------------------------------------------------------------------------------------------
def heat_cell(hs):
    """Heat across the break through Macor + screws at build start: FEA where thermal.json has the screws, else the hand estimate."""
    hand = f"{hs['Q_mac_bored'] + hs['Q_316']:.2f} (316) / {hs['Q_mac_bored'] + hs['Q_ti']:.2f} (Ti)"
    if hs.get("fea_316") is None:
        return f"{hs['Q_fea']:.2f} → {hand}"
    return f"{hs['Q_fea']:.2f} → {hs['fea_316']:.2f} (316) / {hs['fea_ti']:.2f} (Ti); hand estimate {hand}"


def stack_joint(key):
    m = MP.MODULES[key]
    rb = m["block_d"] / 2
    r_so = m["standoff_r"]                     # screw circle of the model snapshot REV (9.4 / 20.1 / 30.2; now 9.0 / 18 / 30.2)
    thr = THREAD["M2.5" if key == "S25" else "M3"]
    D_so = 5.0 if key == "S25" else 8.0
    bore = thr["d"] + 0.4
    A_mac = math.pi / 4 * (D_so ** 2 - bore ** 2)
    A_mac_full = math.pi / 4 * D_so ** 2
    st = THERMAL["steady"]
    T_blk = st[f"{key}_start_ch25_e0.5"]["T_block_max"]                 # thermal.md block max at 200 C plate (build start)
    T_head_start = st[f"{key}_start_ch25_e0.5"]["T_head_mean"]
    T_head_end = st[f"{key}_end_ch25_e0.5"]["T_head_mean"]
    # solid Macor, no screws: thermal_module's "_scrnone" case since it models the screws (2026-11-23); the base case before
    Q_mac_fea = st.get(f"{key}_start_ch25_e0.5_scrnone", st[f"{key}_start_ch25_e0.5"])["exit_W"]["through_macor"]
    fea = {sm: st.get(f"{key}_start_ch25_e0.5{suf}", {}).get("exit_W", {}) for sm, suf in (("a4_50", ""), ("ti64", "_scrTI"))}
    fea = {sm: (x["through_macor"] + x["through_screws"] if "through_screws" in x else None) for sm, x in fea.items()}
    L_free = 7.5 + MP.BREAK_T                                          # head bearing (counterbore floor) to insert top
    L_cond = L_free
    I = math.pi * thr["d3"] ** 4 / 64
    c = thr["d3"] / 2
    rows = {}
    for case, T_head in (("build start", T_head_start), ("build end", T_head_end)):
        d_rad = MAT["al6061"]["alpha"] * (T_blk - T_head) * r_so            # block grows relative to the head at the standoff circle
        for sm in ("a4_50", "ti64"):
            E = MAT[sm]["E"]
            sig = 6 * E * d_rad * c / L_free ** 2                         # Roark: guided cantilever
            F_lat = 12 * E * I * d_rad / L_free ** 3
            rows[(case, sm)] = dict(d_rad_um=d_rad * 1e3, sigma_b=sig, F_lat=F_lat, Sp_200=MAT[sm]["Sp_200"])
    # slip-limited preload for 316 screws: block slides on the Macor before the screw bends past 0.6 Sp(200 C)
    E = MAT["a4_50"]["E"]
    s_all = 0.6 * MAT["a4_50"]["Sp_200"]
    d_all = s_all * L_free ** 2 / (6 * E * c)
    F_lat_all = 12 * E * I * d_all / L_free ** 3
    F_slip_max = F_lat_all / 0.3
    # axial differential expansion (screw at the local member temperature; conservative)
    kb = {sm: MAT[sm]["E"] * thr["At"] / (L_free + 2.25) for sm in ("a4_50", "ti64")}
    k_mac = MAT["macor"]["E"] * A_mac / MP.BREAK_T
    k_blk = wileman(MAT["al6061"]["E"], thr["d"], 7.5, "al")
    km = 1 / (1 / k_mac + 1 / k_blk + 1 / 1.0e6)     # head side ~1,000 kN/mm
    axial = {}
    for case, T_head in (("build end, steady", T_head_end), ("heat-up, block hot, rest cold", 20.0)):
        T_mac = (T_blk + T_head) / 2 if "steady" in case else 20.0
        for sm in ("a4_50", "ti64"):
            a_s = MAT[sm]["alpha"]
            T_s_blk = T_blk if "steady" in case else 20.0
            dl = ((MAT["al6061"]["alpha"] * (T_blk - 20) - a_s * (T_s_blk - 20)) * 7.5
                  + (MAT["macor"]["alpha"] - a_s) * (T_mac - 20) * MP.BREAK_T
                  + (MAT["al6061"]["alpha"] - a_s) * (T_head - 20) * 2.25)
            k_rigid = kb[sm] * km / (kb[sm] + km)
            axial[(case, sm)] = dict(dl_um=dl * 1e3, dF_rigid=dl * k_rigid, dF_spring_302=dl * 490.0, dF_spring_718=dl * 4200.0,
                                     Fp=MAT[sm]["Sp"] * thr["At"])
    G_mac = MAT["macor"]["k"] * A_mac * 1e-6 / (MP.BREAK_T * 1e-3)
    G_mac_full = MAT["macor"]["k"] * A_mac_full * 1e-6 / (MP.BREAK_T * 1e-3)
    G_s = {sm: MAT[sm]["k"] * thr["At"] * 1e-6 / (L_cond * 1e-3) for sm in ("a4_50", "ti64")}
    dT = Q_mac_fea / (3 * G_mac_full)                                   # the break's effective dT, from the FEA's Macor heat
    heat = dict(Q_fea=Q_mac_fea, dT=dT, Q_mac_bored=3 * G_mac * dT, Q_316=3 * G_s["a4_50"] * dT, Q_ti=3 * G_s["ti64"] * dT,
                fea_316=fea["a4_50"], fea_ti=fea["ti64"])
    return dict(r_so=r_so, thread="M2.5" if key == "S25" else "M3", D_so=D_so, A_mac=A_mac, T_blk=T_blk, T_head_start=T_head_start,
                T_head_end=T_head_end, bend=rows, F_slip_max=F_slip_max, d_all_um=d_all * 1e3, axial=axial, heat=heat,
                bearing_302=VENDOR["mcm_9713K53"]["work_N"] / A_mac, bearing_718=(VENDOR["mcm_97125K111"]["work_N"] + 100) / A_mac)


# --------------------------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    line("# Hot-swappable joints: textbook sizing")
    line()
    line(f"Generated by [`analysis/hotswap/joint_calcs.py`](../../hotswap/joint_calcs.py). Geometry from `module_params.py` at commit {REV}; "
         "temperatures and heat flows from [`thermal.json`](../thermal/thermal.json). Units: N, mm, MPa, °C. "
         "Every result names its equation and source; **assumed** marks an engineering assumption, **vendor** a vendor claim (URL in the json).")

    # ---------------- a. module ----------------
    h("a. Build module ↔ chamber floor")
    for key in ("M50", "L75"):
        L = module_loads(key)
        J[f"module_{key}_loads"] = {k: (v if not isinstance(v, dict) else v) for k, v in L.items()}
        line(f"**{key} loads.** Module {f(L['m']['total'], 2)} kg in all (body {f(L['m']['body'], 2)}, gland flange {f(L['m']['gland'], 2)}, "
             f"piston stack {f(L['m']['piston'], 2)}). Weight {f(L['W'])} N. Rod gland, two 2-114 FKM on Ø15.9: {f(L['gland_run'])} N running, "
             f"{f(L['gland_break'])} N break-out (Parker ORD 5700, f_c ≈ 2.5 lbf/in, **assumed** reading; break-out 2× **assumed**). "
             f"Bore seal {f(L['bore_seal'])} N (**assumed**). Port O-ring 2-238 in Ø96: {f(L['port_oring'])} N to push in or pull out. "
             f"+20 mbar on the sealed area: {f(L['over'])} N down; full vacuum: {f(L['vac'])} N up (seats the module).")
        line()
        table([[k, f(v)] for k, v in L["cases"].items()] + [["horizontal transit shear, 2 m/s²", f(L["shear"])]],
              ["load case (separating +)", "N"])
    L50, L75 = module_loads("M50"), module_loads("L75")
    P_sep = max(L50["P_sep"], L75["P_sep"])
    P_sep_nm = max(L50["P_sep_no_magnet"], L75["P_sep_no_magnet"])
    line(f"The largest separating load is **LC2, {f(P_sep)} N**: today the Z arm pulls its pot magnet (44 lbf rated) off the striker while the "
         f"rod collar holds the piston on the gland flange, so the whole break-away force goes through the module joint. Without it the "
         f"worst case is {f(P_sep_nm)} N (LC1). An electro-permanent or switched coupling on the Z arm (released before the arm drops) "
         "would remove LC2.")

    h("(i) Two captive M6 screws (today)", 3)
    cs = captive_screws(P_sep)
    J["module_captive_screws"] = cs
    table([
        ["proof load F_p", f"{f(cs['Fp_thread'], 0)} N on A_t; {f(cs['Fp_shank'], 0)} N on the Ø4.2 reduced shank → {f(cs['Fp'], 0)} N governs", SRC["shig_831"] + "; A2-50 Rp0.2 = 210 MPa"],
        ["preload F_i = 0.75 F_p", f"{f(cs['Fi'], 0)} N per screw, {f(2 * cs['Fi'], 0)} N total", SRC["shig_831"]],
        ["torque T = K F_i d", f"{f(cs['T_dry'], 1)} N·m dry (K 0.30); {f(cs['T_lube'], 1)} N·m with anti-seize (K 0.18)", SRC["shig_827"]],
        ["bolt stiffness k_b", f"{f(cs['kb'] / 1e3, 0)} kN/mm", SRC["shig_817"]],
        ["member stiffness k_m (frusta: 316L flange + 6061 floor)", f"{f(cs['km'] / 1e3, 0)} kN/mm (Wileman, all-steel {f(cs['km_wil_steel'] / 1e3, 0)}, all-Al {f(cs['km_wil_al'] / 1e3, 0)})", SRC["shig_820"] + "; " + SRC["shig_823"]],
        ["joint constant C", f"{cs['C']:.3f}", SRC["shig_824"]],
        ["load per screw P (LC2 / 2)", f"{f(cs['P'], 0)} N", "above"],
        ["load factor against separation n_0", f"{f(cs['n0'], 0)}", SRC["shig_829"]],
        ["yield factor n_p", f"{cs['np']:.2f}", "Shigley Eq. 8-28"],
        ["thread shear, 6 mm engaged: 6061 at STI Ø" + f"{cs['D_sti']:.1f}", f"{f(cs['tau_al'])} MPa vs {f(cs['tau_al_allow'], 0)} (0.577 S_y)", SRC["shig_thread"]],
        ["thread shear: insert (18-8) / screw root", f"{f(cs['tau_ins'])} / {f(cs['tau_root'])} MPa vs {f(cs['tau_ss_allow'], 0)}", SRC["shig_thread"]],
        ["preload change 20 → 85 °C", f"{cs['dF_th']:+.0f} N", "VDI 2230-1 (thermal change of preload): ΔF = (Σα_m l_m − α_b l_b) ΔT k_b k_m/(k_b+k_m)"],
    ], ["quantity", "value", "source"])
    line(f"Strength is not the issue: the joint holds {f(cs['n0'], 0)}× the worst separating load. What counts against screws for a robot "
         f"is the rest: {f(cs['T_dry'], 1)} N·m on an 18-8 screw in an 18-8 insert is the galling pair (Pencom, ASSDA), the cobot "
         f"screwdrivers top out at 4–5 N·m and need magnetic screws (**vendor**, {VENDOR['onrobot_sd']['url']}), and no source uses robot "
         "screwdriving to exchange fixtures. For a person swapping modules between campaigns, the screws are fine; give them an "
         "MoS₂- or silver-plated screw or a Nitronic 60 insert, and 1.5D of engaged thread instead of 6 mm.")

    h("(ii) Spring-locked, air-released zero-point modules", 3)
    zp = [VENDOR[k] for k in ("schunk_nse_am", "schunk_nse_ht", "stark_d085", "zimmer_spn062", "erowa_its50")]
    table([[z["name"], z.get("d_mm", "–"), z.get("pull_in_N", z.get("clamp_N")), f"{z.get('pull_in_N', z.get('clamp_N')) / P_sep:.1f}",
            z.get("repeat_um", "–"), z.get("t_max_C", "–"), z["url"]] for z in zp],
          ["module (vendor)", "Ø mm", "pull-in N", f"× LC2 ({f(P_sep, 0)} N)", "repeat. µm", "max °C", "source"])
    line("Every one of them clamps several times the worst load with one module, repeats to 2–10 µm, holds on air loss and is sold for "
         "robot loading. Two problems here: (1) temperature: the flange runs ≤ 56 °C with a 25 °C chamber and 84 °C with a 60 °C chamber "
         "(thermal.md), so only the FKM/AM versions qualify (STARK ET 150 °C, SCHUNK NSE-AM/HT 200 °C); (2) size: the smallest are Ø78–90 mm, "
         "and the flange tabs carry the screws at x = ±58 mm next to a Ø96 port, so two modules do not fit under the floor where the screws are. "
         "They would need flange arms out to x ≈ ±95 mm and space beside the overflow funnel (x 68–112).")

    h("(iii) Magnets on a 430 strike plate", 3)
    rows = []
    mag_json = {}
    curve25 = (VENDOR["ms_gmh"]["gaps_mm"], VENDOR["ms_gmh"]["d25"])
    curve50 = (VENDOR["ms_gmh"]["gaps_mm"], VENDOR["ms_gmh"]["d50"])
    for name, pull, curve, grade, fail_safe in (
            ("McMaster 5679K95 NdFeB pot Ø25 (permanent; no release)", VENDOR["mcm_5679K95"]["pull_N"], curve25, "NdFeB N", "n/a (always on)"),
            ("Kendrion PEM2525A Ø25 (power to release)", VENDOR["kendrion_pem2525a"]["pull_N"], curve25, "NdFeB SH", "holds"),
            ("Kendrion D55 Ø55 (power to release)", VENDOR["kendrion_d55"]["pull_N"], curve50, "NdFeB SH", "holds"),
            ("Kendrion GTB040 Ø40 (power to hold)", VENDOR["kendrion_gtb040"]["pull_N"], (VENDOR["ms_gmh"]["gaps_mm"], VENDOR["ms_gmh"]["d40"]), "AlNiCo (cast)", "drops it")):
        for T in (56.0, 84.0):
            for gap in (0.0, 0.05, 0.1, 0.2):
                e = magnet_effective(pull, gap, curve, T, grade, VENDOR["goudsmit_430"]["frac"])
                mag_json[f"{name} | {T} C | {gap} mm"] = e
                if gap in (0.0, 0.05, 0.1) and T == 84.0 or (gap == 0.0 and T == 56.0):
                    rows.append([name, f"{T:.0f}", f"{gap:.2f}", f(e["F"], 0), f"{e['F'] / P_sep:.2f}", f"{math.ceil(3 * P_sep / max(e['F'], 1e-9))}",
                                 "**over max temp**" if e["over_temp"] else f"≤ {e['t_max']} °C", fail_safe])
    J["module_magnets"] = mag_json
    table(rows, ["magnet", "flange °C", "gap mm", "N on 430", "× LC2", "needed for 3×", "grade limit", "power off"])
    line("Method: rated pull (**vendor**) × 0.65 for a 430 target (Goudsmit 60–75 %, SCHUNK 65 %) × the vendor's own force-vs-gap curve "
         "(Magnet-Schultz G MH, same pole size) × (1 + α_Br ΔT)² for the reversible loss (Adams chart). A Ø25 pole keeps 27 % at 0.1 mm "
         "and 7 % at 0.25 mm, so a powder grain or a 0.05 mm flatness error costs more than half the force. Vendors rate magnetic holding "
         "with a factor of 3 (Goudsmit, EN 13155) to 5 (Magswitch). Magnets are weak in shear (22–35 % of pull), so the dowels or a "
         "kinematic seat must take all lateral load. **For the module, magnets would need 3–12 units to reach 3× LC2 and are not a good "
         "fit**; even with LC2 removed it takes two Ø55 fail-safe magnets per module at zero gap.")

    h("(iv) Three-groove kinematic coupling (balls on the flange, vees under the floor)", 3)
    kin_rows = []
    kin = {}
    for Fp, label in ((3 * P_sep, "3× LC2"), (3 * P_sep_nm, "3× LC1 (Z magnet released first)")):
        for D in (10.0, 16.0):
            for ball, groove in (("si3n4", "al6061"), ("ss440c", "ss316"), ("si3n4", "ph17_4_h900"), ("ss440c", "ss440c"), ("si3n4", "ss440c")):
                k = kinematic(Fp, D, ball, groove)
                kin[f"{label} | D{D:.0f} | {ball}/{groove}"] = k
                kin_rows.append([label, f"{f(Fp, 0)}", f"Ø{D:.0f}", f"{ball} / {groove}", f(k["N"], 0), f(k["p0"], 0), f(k["p0_allow"], 0),
                                 f"{k['n_yield']:.2f}", f(k["delta_um"], 1), f(k["kz_N_um"], 0)])
    J["module_kinematic"] = kin
    table(kin_rows, ["preload", "F_p N", "ball", "ball / groove", "N per contact", "p0 MPa", "1.6 S_y", "margin", "δ µm", "k_z N/µm"])
    pk = kin[f"3× LC2 | D16 | si3n4/ph17_4_h900"]["particle"]
    line(f"Hertz sphere-on-flat for each flank (Shigley 3-19 / Johnson), first yield at p0 = 1.6 S_y (Johnson 6.2). 6061 and 316L "
         "grooves yield at these preloads: the vees need hardened inserts (17-4 PH H900 or 440C) and Ø16 balls, or canoe contacts. "
         "Repeatability (Slocum 2010 review, **measured** by others): Si₃N₄ on steel ~50 nm; steel on steel sub-µm, fretting to ~10 µm after "
         "several hundred cycles; 50–110 µm at a robot's tool point with dirt and variable preload (Hart 2004). **Trapped Al grain**, "
         f"flattened at H ≈ 1.3 GPa (**assumed**) between Si₃N₄ and 17-4: 20 / 30 / 63 µm grains leave {pk[20]['t_um']:.1f} / {pk[30]['t_um']:.1f} / "
         f"{pk[63]['t_um']:.1f} µm thick discs of Ø{2 * pk[30]['r_um']:.0f} µm (30 µm grain) and need only {pk[30]['F_crush_N']:.0f} N to crush, "
         "so the offset is ~1–2 µm, not the grain size (estimate: flat-punch indentation, t³ = V π H² / 4E*²). A hard spatter or oxide "
         "particle would not crush and would offset the seat by its full size. The six contacts cover ~1 mm² against ~3,000 mm² for "
         "today's flange face, so a stray grain is far less likely to land in a contact at all.")

    # ---------------- b. plate ----------------
    h("b. Build plate ↔ heater block (200–225 °C)")
    prow, pj = [], {}
    for key in ("S25", "M50", "L75"):
        o = plate_options(key)
        pj[key] = o
        b, d, s, mg = o["bayonet_springs"], o["drawbar"], o["screws_M4"], o["magnet"]
        prow.append([key, f(o["A_face"], 0), f(o["F_req"], 0), f(o["F_tip_strike"], 0), f"{o['bare_pressure_kPa']:.2f} kPa; edge lift ≤ {o['bare_lift_mm']:.2f} mm",
                     f"{f(b['target_N'], 0)} N: {b['n_parallel']} × 97125K111 at {b['s_mm'] * 1e3:.0f} µm; twist {b['T_twist_Nm']:.2f} N·m; lug {f(b['lug_bending_MPa'], 0)} MPa",
                     f"{f(d['N_ball'], 0)} N/ball, p0 {f(d['p0_groove'], 0)} MPa (flat {f(d['p0_flat'], 0)}); push {f(d['release_push_N'], 0)} N; leak {d['Q_316_W']:.2f} W (Ti {d['Q_ti_W']:.2f})",
                     f"F_i {f(s['Fi'], 0)} → {f(s['F_hot'], 0)} N hot; {f(s['s_screw_hot'], 0)} MPa vs {f(s['Sp_200'], 0)}; under head {f(s['bearing_hot'], 0)} vs {f(s['Sy_al_200'], 0)}",
                     f"{f(mg['F_per_magnet'], 0)} N each → {mg['n_needed']} magnets"])
    J["plate"] = pj
    table(prow, ["module", "face mm²", "F for 0.1 MPa", "F vs 50 N strike (2×)", "(i) bare bayonet", "(ii) bayonet + disc springs",
                 "(iii) drawbar (6 × Ø4 Si₃N₄)", "(iv) 3 × M4 316 screws", "(v) SmCo + 430 insert"])
    v = VENDOR["mcm_97125K111"]
    b = pj["M50"]["bayonet_springs"]
    line(f"- **Contact pressure (assumed 0.1 MPa).** The thermal FEA used h = 5,000 W/m²K (2 K·cm²/W) under the plate. Flexible graphite reaches "
         "well under 1 K·cm²/W at a few tenths of a MPa in published joint-conductance work (e.g. Marotta, Mazzuca & Norley, IEEE TCPT 28(1), 2005), "
         "so 0.1 MPa is taken as enough; no vendor curve was read in this pass. That sets the preload: "
         + ", ".join(f"{k} {f(pj[k]['F_req'], 0)} N" for k in pj) + ". The recoater (10 N drag, 50 N strike, 10 mm above the face) needs much less.")
    line(f"- **(i) Bare bayonet:** only the plate's weight presses it on the foil ({pj['M50']['bare_pressure_kPa']:.2f} kPa for M50), and a "
         f"strike can tip it until a lug meets the ledge, lifting the far edge up to {pj['M50']['bare_lift_mm']:.2f} mm. It needs a preload.")
    line(f"- **(ii) Bayonet + disc springs:** Almen–László for McMaster 97125K111 (718 nickel, to 593 °C, $1.69) gives {f(b['check_F_at_work'], 0)} N at "
         f"its 0.10 mm working deflection (McMaster: {f(v['work_N'], 0)} N), within 7 %, but {f(b['check_flat'], 0)} N flat where McMaster lists "
         f"{f(v['flat_N'], 0)} N: catalogue heights are maxima and real discs have edge radii, so the ideal equation overstates the stiff end; "
         f"size from the catalogue working point and keep s ≤ 0.10 mm. Stress at the working point σ_OM {f(b['sOM'], 0)} MPa. The ramps (0.4 mm over 40°, μ 0.3) need "
         f"{b['T_twist_Nm']:.2f} N·m to turn (self-locking: tan α = {b['tan_ramp']:.3f} < μ). The 6061 lugs see {f(b['lug_bending_MPa'], 0)} MPa "
         f"(M50) and {f(pj['L75']['bayonet_springs']['lug_bending_MPa'], 0)} MPa (L75) in bending against 103 MPa (204 °C) and ~77 MPa (225 °C) "
         "after long exposure (ASM): L75 needs thicker lugs or a 17-4 cup (CalculiX H1).")
    d = pj["L75"]["drawbar"]
    line(f"- **(iii) Drawbar (machine-tool style):** a pull stud in the plate, six Ø4 balls in a conforming groove, the disc-spring stack and "
         f"the release at the cold rod end. Ball contact p0 {f(d['p0_groove'], 0)} MPa in a 0.54-conformity groove (L75) vs "
         f"{f(d['p0_flat'], 0)} MPa on a flat, so the groove must conform; 17-4 H900 allows {f(d['p0_allow_17_4'], 0)} MPa at first yield. "
         f"Release push {f(d['release_push_N'], 0)} N (a Ø32 cylinder at 6 bar gives ~480 N). The Ø4 drawbar carries {d['Q_316_W']:.2f} W "
         f"(316) or {d['Q_ti_W']:.2f} W (Ti-6Al-4V) down the rod: negligible. Only passive parts sit in the 225 °C block, which is how the "
         "research says to get past the 200 °C rating of every actuated zero-point module.")
    s = pj["M50"]["screws_M4"]
    line(f"- **(iv) 3 × M4 316 screws (EOS style):** {f(s['Fi'], 0)} N each at {s['T_dry']:.1f} N·m dry. Heating 20 → 200 °C adds "
         f"{f(s['dF_200'], 0)} N per screw (Al grows {(MAT['al6061']['alpha'] - MAT['a4_50']['alpha']) * 1e6:.1f} µm/m/K more than 316 over a "
         f"{(MP.PLATE_T - 4.5) + 2:.1f} mm grip), so the screw reaches {f(s['s_screw_hot'], 0)} MPa against ~{f(s['Sp_200'], 0)} MPa at 200 °C and the "
         f"6061 under the head {f(s['bearing_hot'], 0)} MPa against 103 MPa: both yield, the joint loses preload every cycle, and 6061-T6 overages "
         "at 200 °C. Add to that galling and a robot screwdriver in powder.")
    mg = pj["L75"]["magnet"]
    line(f"- **(v) Magnet:** no small switchable magnet is rated near 225 °C; Sm2Co17 would be needed, every plate would need a 430 insert "
         f"(α 10.4 vs 23.6 µm/m/K in an Al plate), and the graphite foil is itself a 0.13 mm gap. One Ø25 pot gives ~{f(mg['F_per_magnet'], 0)} N, "
         f"so L75 needs ~{mg['n_needed']}. Not viable.")

    # ---------------- c. heater stack ----------------
    h("c. Heater-stack joint (screws through the Macor standoffs)")
    crow, cj = [], {}
    for key in ("S25", "M50", "L75"):
        sj = stack_joint(key)
        cj[key] = {k: (v if not isinstance(v, dict) else {str(kk): vv for kk, vv in v.items()}) for k, v in sj.items()}
        b_s = sj["bend"][("build start", "a4_50")]
        b_t = sj["bend"][("build start", "ti64")]
        b_e = sj["bend"][("build end", "a4_50")]
        ax = sj["axial"][("heat-up, block hot, rest cold", "a4_50")]
        ax_t = sj["axial"][("build end, steady", "ti64")]
        crow.append([key, f"{sj['thread']} in Ø{sj['D_so']:.0f} Macor at r {sj['r_so']:.1f}",
                     f"{b_e['d_rad_um']:.0f} / {b_s['d_rad_um']:.0f}",
                     f"{f(b_e['sigma_b'], 0)} / {f(b_s['sigma_b'], 0)} vs {f(b_s['Sp_200'], 0)}",
                     f"{f(b_t['sigma_b'], 0)} vs {f(b_t['Sp_200'], 0)}",
                     f"≤ {f(sj['F_slip_max'], 0)} N",
                     f"{ax['dl_um']:.0f} µm → {f(ax['dF_rigid'], 0)} N rigid (F_p {f(ax['Fp'], 0)}); {f(ax['dF_spring_302'], 0)} N with 9713K53",
                     f"{ax_t['dl_um']:+.0f} µm → {f(ax_t['dF_rigid'], 0)} N rigid; {f(ax_t['dF_spring_718'], 0)} N with 97125K111",
                     heat_cell(sj["heat"])])
    J["stack"] = cj
    table(crow, ["module", "joint", "block growth at the screw, µm (end / start)", "316 screw bending if it can't slip, MPa (end / start) vs S_p 200 °C",
                 "Ti-6Al-4V bending at start vs S_p", "316: preload that lets the block slide (μ 0.3)", "316 axial, heat-up transient",
                 "Ti axial, steady (Ti grows less)", "heat through the Macor and screws at build start, W: solid Macor (FEA) → with screws"])
    sj = stack_joint("M50")
    dTs = (sj["T_blk"] - sj["T_head_end"], sj["T_blk"] - sj["T_head_start"])
    sbs = (sj["bend"][("build end", "a4_50")]["sigma_b"], sj["bend"][("build start", "a4_50")]["sigma_b"])
    line(f"- **Radial growth:** the block runs {dTs[0]:.0f}–{dTs[1]:.0f} K hotter than the head (M50), so at the screw circle it grows {sj['bend'][('build end', 'a4_50')]['d_rad_um']:.0f}–"
         f"{sj['bend'][('build start', 'a4_50')]['d_rad_um']:.0f} µm (M50) relative to it. A slot or a clearance hole only helps if the block can "
         "actually slide; the friction under the screw head (μ·F) holds it unless the preload is small. Bending a guided M3 316 screw "
         f"(Roark: M = 6EIδ/L², L = {7.5 + MP.BREAK_T:.1f} mm) by that much gives {sbs[0]:.0f}–{sbs[1]:.0f} MPa, past its ~160 MPa yield at 200 °C. So either "
         f"**keep the 316 screw's spring preload ≤ {f(sj['F_slip_max'], 0)} N** (McMaster 9713K53, 302 stainless, ~49 N at 0.1 mm) so the block "
         "slides on the Macor first, or **use Ti-6Al-4V screws**, which take the full growth elastically (E 114 GPa, S_p ~650 MPa at 200 °C) "
         "and carry less heat.")
    line("- **Axial:** in a heat-up the block reaches temperature before the screw. Without a spring that stretches an M3 by ~30 µm, "
         "which is past its proof load; a disc spring under the head turns it into a few newtons. With Ti screws the steady-state "
         "growth is larger still (Ti expands less than Al), so Ti screws need the stiffer 718 spring (97125K111) and a set deflection.")
    hs = sj["heat"]
    if hs.get("fea_316") is not None:
        P50 = THERMAL["steady"]["M50_start_ch25_e0.5"]["P_heater_W"]
        line(f"- **Heat:** the thermal FEA (thermal_module.py, which models the screws since 2026-11-23) puts {hs['Q_fea']:.2f} W through the "
             f"three solid Macor standoffs at build start (M50, no screws); through the bored Macor and the screws, {hs['fea_316']:.2f} W with 316 "
             f"screws and {hs['fea_ti']:.2f} W with Ti-6Al-4V, against {P50:.0f} W of heater power. The hand estimate (screw conduction over "
             f"{7.5 + MP.BREAK_T:.1f} mm at the FEA's break ΔT) gave {hs['Q_mac_bored'] + hs['Q_316']:.2f} and {hs['Q_mac_bored'] + hs['Q_ti']:.2f} W.")
    else:
        line(f"- **Heat:** the FEA puts {hs['Q_fea']:.2f} W through the three solid Macor standoffs at build start (M50). Boring them for the "
             f"screw and adding 316 screws gives {hs['Q_mac_bored'] + hs['Q_316']:.2f} W; Ti screws give "
             f"{hs['Q_mac_bored'] + hs['Q_ti']:.2f} W (hand estimate).")
    line(f"- **Macor bearing:** {sj['bearing_302']:.1f} MPa (302 spring) to {sj['bearing_718']:.1f} MPa (718 spring + 100 N) on the standoff "
         "annulus against 345 MPa compressive strength (Corning).")

    # ---------------- d. reservoir, blade ----------------
    h("d. Reservoir detents and recoater blade")
    pl = VENDOR["mcm_85015A47"]
    mu, beta = 0.2, 45.0
    F_det = pl["f_ext_N"] * math.tan(math.radians(beta) + math.atan(mu))
    m_res = 1.0
    rows = [["reservoir, 3 × 85015A47 in 90° detents (μ 0.2)", f"{f(3 * F_det, 0)} N along the slide", f"transit {m_res * 2.0:.0f} N (1 kg × 2 m/s²)",
             f"{3 * F_det / (m_res * 2.0):.0f}×", "the robot pulls ~40 N to remove it: fine"]]
    th = THREAD["M3"]
    Fi3 = 0.75 * th["At"] * MAT["a4_50"]["Sp"]
    rows.append(["blade, 2 × M3 316 screws", f"friction {f(0.2 * 2 * Fi3, 0)} N (F_i {f(Fi3, 0)} N each, μ 0.2)", "50 N strike",
                 f"{0.2 * 2 * Fi3 / 50:.1f}×", "needs a screwdriver for every alloy change"])
    F_mag = 2 * 20.0 * 0.6
    rows.append(["blade, 2 dowels + 2 Ø10 × 3 NdFeB discs", f"pull ~{f(F_mag, 0)} N (1.5 mm HSS saturates: ~60 % of thick-steel rating, **assumed** from OnRobot/Magswitch thickness curves)",
                 "drag pushes the blade into the holder face; return-stroke drag ~1 N", f"{F_mag / 1.0:.0f}× on the return stroke; {F_mag / 50:.1f}× on a 50 N strike",
                 "tool-free swap; a crash knocks the blade off (a fuse)"])
    rows.append(["blade, 1 × Ø6 ball-lock pin", f"pull-out {f(VENDOR['carrlane_blp6']['pullout_N'], 0)} N, double shear {f(VENDOR['carrlane_blp6']['shear_N'], 0)} N (**vendor**)",
                 "50 N strike", f"{VENDOR['carrlane_blp6']['pullout_N'] / 50:.0f}×", "push-button: a gripper finger can press it"])
    table(rows, ["joint", "holding", "load", "factor", "note"])
    J["reservoir_detent_N"] = 3 * F_det

    (OUT / "joint_calcs.md").write_text("\n".join(R) + "\n")

    def clean(x):
        if isinstance(x, dict):
            return {str(k): clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [clean(v) for v in x]
        if isinstance(x, float):
            return round(x, 6)
        return x
    J["sources"] = SRC
    J["vendor"] = VENDOR
    J["rev"] = REV
    (OUT / "joint_calcs.json").write_text(json.dumps(clean(J), indent=1))
    print("wrote", OUT / "joint_calcs.md")


if __name__ == "__main__":
    main()
