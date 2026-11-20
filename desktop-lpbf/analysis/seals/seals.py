"""Seals, leaks, purge and atmosphere purity of the low-profile desktop LPBF (issue #260, PR #266).

What it does
  1. Inventories every seal and every hole through the gas envelope of cad/lpbf_low.py (chamber, lid, door, drawer,
     window, metering base and reservoir, build module, gas loop), with the seal's real geometry where the model has it.
  2. Checks each O-ring gland against Parker's O-Ring Handbook (ORD 5700): squeeze, gland fill (cold and warm) and
     stretch, with the AS568 cross-section tolerance and +/-0.05 mm on machined gland dimensions.
  3. Works out the force it takes to squeeze each closure seal (Lindley's load-compression relation with Gent's
     Shore-A modulus, bracketed by Parker's Figures 2-4..2-6) and compares it with what holds that closure shut:
     screws, latches, or the atmosphere at vacuum.
  4. Leak and permeation budget (Parker's leak-rate approximation, L = 0.7 F D P Q (1-S)^2), outgassing of the walls,
     seals and powder, and the O2 and H2O they put into the closed argon loop: ppm per hour with no make-up, and the
     make-up flow that holds the targets.
  5. Vacuum purge: pump-down time with the real pump and hoses, the number of purge cycles, and the pumping rate above
     which the gas leaving a powder bed lifts it (Darcy flow with a Klinkenberg slip term against the bed's weight).
  6. The rate-of-rise test that proves the leak budget.

Run:  python desktop-lpbf/analysis/seals/seals.py      ->  desktop-lpbf/analysis/out/seals/seals.{md,json}
Needs CadQuery (reads the model) and numpy.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "cad"))
OUT = ROOT / "analysis" / "out" / "seals"

IN = 25.4
PSI = 6894.76            # Pa per psi
ATM = 101325.0
R_GAS = 8.314
T0 = 296.15              # K, 23 C lab

# ------------------------------------------------------------------------------------------------------------------
# 1. Material and handbook data (sources in SOURCES, numbered as cited)
# ------------------------------------------------------------------------------------------------------------------
SOURCES = {
    1: "Parker O-Ring Handbook ORD 5700: Design Chart 4-3 (face glands), Design Table 4-2 (static radial glands), "
       "§3.11 vacuum sealing and Table 3-20 (finish), §3.12.1 leak-rate approximation and Fig. 3-11 (Q), Table 3-24 "
       "(permeability), Figs. 2-4..2-6 (compression load). https://nfc.arizona.edu/sites/default/files/2022-02/parker_o-ring_handbook.pdf",
    2: "Lindley, P. B. (1967). Compression characteristics of laterally-unrestrained rubber O-rings. J. Inst. Rubber Ind. 1, 209-213 "
       "(F/L = d E (1.25 e^1.5 + 50 e^6)); as used in e.g. https://doi.org/10.1016/j.triboint.2019.106062",
    3: "Gent, A. N. (1958). On the relation between indentation hardness and Young's modulus. Trans. IRI 34, 46-57 "
       "(E [MPa] = 0.0981 (56 + 7.62336 S) / (0.137505 (254 - 2.54 S)))",
    4: "Marco Rubber, O-ring permeation (FKM: H2O 40e-8 std cc cm/cm2 s bar): https://www.marcorubber.com/o-ring-permeation.htm",
    5: "O'Hanlon, J. F. A User's Guide to Vacuum Technology, 3rd ed. (Wiley, 2003), Table 4.5 and App. C.5: outgassing of "
       "unbaked Al ~6e-9 and Viton A ~1e-6 Torr L/s/cm2 after 1 h; and Ch. 2-3 (viscous conductance, C = 135 d^4 p/L for air)",
    6: "Kozeny-Carman permeability k = d^2 e^3 / (180 (1-e)^2); Klinkenberg (1941) slip k_a = k (1 + b/p), b = 4 c lambda p / r "
       "with c ~ 1 (API Drilling and Production Practice, 200-213)",
    7: "Ergun minimum fluidization: U_mf = (rho_p - rho_g) g d^2 e^3 / (150 mu (1 - e)) for small particles (Kunii & Levenspiel, "
       "Fluidization Engineering, 2nd ed., Ch. 3)",
    8: "McMaster-Carr 4396K21 (3 cfm, 1e-2 Torr) and the parts in ../../mcmaster-parts.csv, read through the lab Pi 2026-11-17",
    9: "Airgas/Linde argon 5.0 (UHP) typical limits: O2 <= 1-2 ppm, H2O <= 1-3 ppm",
    10: "Sturm et al. (2004), Permeation of atmospheric gases through polymer O-rings used in flasks for air sampling, J. Geophys. Res. 109, "
        "D04309, https://doi.org/10.1029/2003JD004073: Viton O2 1.0-1.1e-15 and H2O ~220e-15 m2/(s hPa) (= 1.05e-8 and 2.2e-6 std cc cm/(cm2 s bar)); via Edison",
    11: "Lubkowitz et al. (2024): new AlSi10Mg powder 0.015 wt% moisture (Karl Fischer); Van Cauwenbergh et al. (2019): AlSi7Mg0.6 powder "
        "45 +/- 11 ppm H, parts 13 +/- 4 ppm; via Edison, desktop-lpbf/edison/followup-sealing-o2/answer.md",
    12: "Pauzon et al. (2021), control of residual oxygen in LPBF (TruPrint 1000): a zirconia lambda probe read +50 ppm where an electrochemical "
        "cell read +700 ppm (H2 cross-sensitivity); leak-plus-outgassing drift ~1.7 ppm O2/min; via Edison",
}

# FKM 75A (Viton A type)
SHORE_FKM = 75.0
CTE_FKM = 1.6e-4         # 1/K linear, FKM (Parker Table 2-? range 1.6e-4); volume ~3x
CTE_AL = 23.6e-6
CTE_SS = 16.0e-6
# Parker Table 3-24 permeability, std cc cm / (cm2 s bar): O2 1.7e-8 @ 26 C, N2 0.233e-8 @ 30 C and 0.975e-8 @ 50 C,
# He 12.7e-8 @ 25 C and 131e-8 @ 80 C. Temperature scaling: Arrhenius with Ea fitted to the He pair (the N2 pair gives a
# steeper rise, so this is not conservative above ~50 C; we also show N2-pair scaling).
F_O2_26 = 1.7e-8
F_H2O_25 = 40e-8          # [4] lower value
F_H2O_STURM = 220e-8      # [10] measured on Viton O-rings (5.5x higher); used as the main value below
F_N2_30 = 0.233e-8
EA_HE = R_GAS * math.log(131 / 12.7) / (1 / 298.15 - 1 / 353.15)        # ~37 kJ/mol
EA_N2 = R_GAS * math.log(0.975 / 0.233) / (1 / 303.15 - 1 / 323.15)     # ~58 kJ/mol


def f_perm(F_ref, T_ref_C, T_C, Ea):
    return F_ref * math.exp(-Ea / R_GAS * (1 / (T_C + 273.15) - 1 / (T_ref_C + 273.15)))


# Parker Fig. 3-11, factor Q vs squeeze (digitized): dry and lubricated (vacuum grease)
Q_DRY = [(10, 1.70), (15, 1.55), (20, 1.40), (25, 1.27), (30, 1.17), (40, 1.06), (50, 1.00)]
Q_LUBE = [(10, 0.62), (15, 0.66), (20, 0.70), (25, 0.74), (30, 0.79), (40, 0.89), (50, 1.00)]


def q_factor(squeeze, lube=False):
    tab = Q_LUBE if lube else Q_DRY
    return float(np.interp(100 * squeeze, [a for a, _ in tab], [b for _, b in tab]))


def parker_leak(F, d_id_mm, dp_bar, squeeze, lube=False):
    """Parker §3.12.1: L [std cc/s] = 0.7 F D P Q (1-S)^2, D in inches (O-ring ID), P in psi."""
    return 0.7 * F * (d_id_mm / IN) * (dp_bar * 1e5 / PSI) * q_factor(squeeze, lube) * (1 - squeeze) ** 2


def gent_E(shore):
    """Young's modulus (MPa) from Shore A hardness, Gent (1958) [3]."""
    return 0.0981 * (56 + 7.62336 * shore) / (0.137505 * (254 - 2.54 * shore))


def lindley(cs_mm, squeeze, shore=SHORE_FKM):
    """Compression load per unit length (N/mm) of an O-ring cord, Lindley [2]."""
    return cs_mm * gent_E(shore) * (1.25 * squeeze ** 1.5 + 50 * squeeze ** 6)


# Parker Figs 2-4..2-6, 70A-80A bars read at 20 % and 30 % compression, interpolated (geometric) to 25 %, lb/in.
PARKER_LOAD_25 = {1.78: (7.6, 21.0), 2.62: (16.6, 31.0), 3.53: (12.8, 55.0)}

# AS568 cross-section tolerances (Parker): .070 +/-.003, .103 +/-.003, .139 +/-.004 in
CS_TOL = {1.78: 0.076, 2.62: 0.076, 3.53: 0.102}
MACH_TOL = 0.05           # +/- on gland depth and width


# ------------------------------------------------------------------------------------------------------------------
# 2. Geometry read from the model
# ------------------------------------------------------------------------------------------------------------------
def model_geometry():
    import lpbf_low as L
    import module_params as MP
    parts = L.build(module="M50", reservoir="M")
    by = {p.name: p for p in parts}

    def find(prefix):
        for n, p in by.items():
            if n.startswith(prefix):
                return p
        raise KeyError(prefix)

    def ring_path(p, cs_area):
        """Centre-line length of a drawn seal ring = its volume / its drawn cross-section area."""
        return p.shape.Volume() / cs_area

    g = {}
    # lid O-ring: drawn 2.65 tall x 3.7 wide (squeezed section); door: 2.8 x 3.2; spigot: 2.6 x 3.0; drawer 1.6 x 1.8
    g["lid_path"] = ring_path(find("Lid O-ring"), 2.65 * 3.7)
    g["door_path"] = ring_path(find("Door O-ring"), 2.8 * 3.2)
    g["drawer_path"] = ring_path(find("Drawer O-ring"), 1.6 * 1.8)
    g["spigot_path"] = math.pi * (MP.PORT_D - 2.9)
    g["gland_plate_path"] = ring_path(find("Module M50 gland-plate O-ring"), 1.3 * 2.2)
    ch = find("Process chamber body")
    bb = ch.shape.BoundingBox()
    P = L.P
    g["chamber_inside"] = (P["ch_x"], P["ch_y"], P["ch_z"])
    g["door_opening"] = (220.0, 92.0)
    g["door_seal_rect"] = (232.0, 104.0)        # centre line of the door O-ring (fea.py uses the same)
    g["lid_seal_rect"] = (2 * (P["ix"] + 3 + P["gland_w"] / 2), 2 * (P["iy"] + 3 + P["gland_w"] / 2))
    g["window_d"] = 50.8
    # gas envelope volume pieces
    ix, iy, iz = P["ch_x"], P["ch_y"], P["ch_z"]
    g["v_chamber_L"] = ix * iy * iz * 1e-6
    filt = find("Sealed cyclone + HEPA housing").shape.BoundingBox()
    g["v_filter_L"] = math.pi / 4 * filt.xlen ** 2 * filt.zlen * 1e-6 * 0.85
    g["bore_d"] = MP.MODULES["M50"]["bore"]
    g["stroke"] = MP.BUILD_STROKE
    g["res"] = MP.RESERVOIRS
    g["slot_w"] = MP.SLOT_W
    g["rod_od"] = MP.ROD_OD
    # chamber wetted area (walls, floor, lid underside), cm2
    g["area_walls_cm2"] = 2 * (ix * iy + ix * iz + iy * iz) / 100.0
    g["n_parts"] = len(parts)
    return g


# ------------------------------------------------------------------------------------------------------------------
# 3. Gland checks
# ------------------------------------------------------------------------------------------------------------------
def gland(cs, depth, width, T_service=23.0, groove_mat="al", stretch=0.0, kind="face"):
    """Squeeze and fill (nominal / worst) for an O-ring of cross-section cs in a gland depth x width.
    stretch reduces the cross-section (Parker: d_reduced ~ cs * (1 - 0.43 * stretch) for stretch < 3 %)."""
    tol = CS_TOL[min(CS_TOL, key=lambda k: abs(k - cs))]
    cs_eff = cs * (1 - 0.43 * stretch)
    area = lambda d: math.pi / 4 * d ** 2
    sq_nom = (cs_eff - depth) / cs_eff
    sq_min = ((cs_eff - tol) - (depth + MACH_TOL)) / (cs_eff - tol)
    sq_max = ((cs_eff + tol) - (depth - MACH_TOL)) / (cs_eff + tol)
    fill_nom = area(cs_eff) / (depth * width)
    fill_max = area(cs_eff + tol) / ((depth - MACH_TOL) * (width - MACH_TOL))
    dT = T_service - 23.0
    a_g = CTE_AL if groove_mat == "al" else CTE_SS
    fill_hot = fill_max * (1 + 3 * CTE_FKM * dT) / (1 + 2 * a_g * dT)
    return dict(cs=cs, depth=depth, width=width, stretch_pct=100 * stretch, squeeze_nom=100 * sq_nom, squeeze_min=100 * sq_min,
                squeeze_max=100 * sq_max, fill_nom=100 * fill_nom, fill_max_cold=100 * fill_max, fill_max_hot=100 * fill_hot,
                T_service=T_service, kind=kind)


def parker_face_rule(cs):
    """Parker Design Chart 4-3, face glands: depth and width (vacuum/gas and liquid columns), mm."""
    tab = {1.78: dict(depth=(1.27, 1.37), w_gas=(2.13, 2.26), w_liq=(2.57, 2.72), sq=(19, 32)),
           2.62: dict(depth=(1.88, 2.03), w_gas=(3.05, 3.18), w_liq=(3.45, 3.61), sq=(20, 30)),
           3.53: dict(depth=(2.57, 2.72), w_gas=(4.01, 4.17), w_liq=(4.50, 4.75), sq=(20, 30))}
    return tab[cs]


# ------------------------------------------------------------------------------------------------------------------
# 4. Powder beds under a pressure change (Darcy + Klinkenberg) and the reservoir's open path
# ------------------------------------------------------------------------------------------------------------------
POWDER = dict(d50=38e-6, eps=0.50, rho_true=2670.0, mu_ar=2.25e-5, mu_air=1.81e-5)


def k_kozeny(d=POWDER["d50"], eps=POWDER["eps"]):
    return d ** 2 * eps ** 3 / (180 * (1 - eps) ** 2)


def mean_free_path(p_pa, T=T0, d_mol=3.7e-10):
    return 1.380649e-23 * T / (math.sqrt(2) * math.pi * d_mol ** 2 * p_pa)


def k_app(p_pa, d=POWDER["d50"], eps=POWDER["eps"]):
    """Apparent permeability with Klinkenberg slip; pore radius ~ d eps / (3 (1-eps)) (hydraulic radius)."""
    r_pore = d * eps / (3 * (1 - eps))
    lam = mean_free_path(p_pa)
    return k_kozeny(d, eps) * (1 + 4 * lam / r_pore)


def bed_lift_ratio(h_bed, tau, p_pa, mu=POWDER["mu_air"]):
    """Pressure drop across a powder bed of depth h whose gas expands as the chamber pumps down with time constant tau,
    over the bed's weight per area. Gas generated uniformly in the bed (porosity eps) leaves through the top: the
    superficial velocity at depth z is eps (h - z) / tau and dp/dz = mu u / k, so dp = mu eps h^2 / (2 k tau)."""
    eps = POWDER["eps"]
    dp = mu * eps * h_bed ** 2 / (2 * k_app(p_pa) * tau)
    w = (1 - eps) * POWDER["rho_true"] * 9.81 * h_bed
    return dp / w, dp, w


def tau_min_for(h_bed, ratio_allowed=0.3, p_pa=ATM):
    """Smallest pump-down time constant V/S that keeps dp/weight below ratio_allowed (worst at high pressure, where
    slip is negligible and the gas is most viscous)."""
    r1, dp1, w = bed_lift_ratio(h_bed, 1.0, p_pa)
    return r1 / ratio_allowed


def pu_t_rest(V, s_eff, p0=100.0, p1=1.0):
    ps = np.logspace(math.log10(p0), math.log10(p1), 200)
    return sum(V * (a - b) / (s_eff(math.sqrt(a * b)) * math.sqrt(a * b)) for a, b in zip(ps[:-1], ps[1:]))


def u_mf(d=POWDER["d50"], eps=0.5, mu=POWDER["mu_ar"], rho_g=1.7):
    return (POWDER["rho_true"] - rho_g) * 9.81 * d ** 2 * eps ** 3 / (150 * mu * (1 - eps))


# ------------------------------------------------------------------------------------------------------------------
# 5. Main
# ------------------------------------------------------------------------------------------------------------------
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    g = model_geometry()
    R = dict(geometry=g, sources=SOURCES)
    E75 = gent_E(SHORE_FKM)

    # ---------------- seal inventory: every closure and penetration of the gas envelope ----------------
    # status: OK, CHECK (works, but a number to fix), FIX (will not seal or not hold as drawn), MISSING (no seal drawn)
    inv = [
        dict(key="lid", seal="Lid O-ring, FKM 75A 3.53 mm cord in a face gland 2.65 x 4.6 in the body's top face",
             held_by="20 x M5 316 into helical inserts (metal-to-metal)", status="OK",
             note="cord spliced into a ring: specify a vulcanized (hot) splice or a molded ring, never a glued joint, for vacuum"),
        dict(key="door", seal="Door O-ring, 3.53 mm cord, groove on the door face 2.8 deep x 4.0 wide as drawn",
             held_by="2 draw latches (McMaster 1807A61) at the top corners + 2 fixed hinges at the bottom; atmosphere under vacuum",
             status="FIX", note="gland is not the 2.65 x 4.6 the notes specify; latches were sized for +50 mbar only, not for squeezing the cord (see clamp table)"),
        dict(key="window", seal="Window O-ring under the Ø50.8 x 8 fused-silica window; retaining ring 2 mm above the window top",
             held_by="nothing at +20 mbar: the window is 'unclamped' and floats up to 2 mm", status="FIX",
             note="+20 mbar lifts the window (3.2 N against its 0.35 N weight); needs an O-ring sandwich clamped to a metal stop"),
        dict(key="window_flange", seal="Window flange to lid: 6 x M4, no seal drawn", held_by="6 x M4", status="MISSING",
             note="needs a face O-ring (or make the flange part of the lid)"),
        dict(key="drawer", seal="Cover-slide drawer front plate, ~1.78 mm cord on the lid's front face", held_by="nothing (a detent)",
             status="FIX", note="at +20 mbar the drawer is pushed out; the cord needs ~0.3-0.5 kN to squeeze: a cam or toggle clamp"),
        dict(key="metering_base", seal="Metering base to lid over the 12 x 100 mm dose slot: 4 x M4, no seal drawn", held_by="4 x M4",
             status="MISSING", note="needs a face O-ring round the slot"),
        dict(key="reservoir", seal="Reservoir on the dock face (dovetail, spring shutter); reservoir lid is a loose plate",
             held_by="nothing", status="FIX",
             note="an open path from room air through the powder column and the roller clearance into the chamber (flow table below)"),
        dict(key="roller_shaft", seal="Metering-roller shaft: PTFE V-ring (McMaster 9572K33)", held_by="-", status="CHECK",
             note="a V-ring is an excluder, not a vacuum seal; use a magnetic-fluid feedthrough or a magnetic coupling through a can"),
        dict(key="recoater_left", seal="Recoater screw through the left wall (Ø18 hole): fixed bearing + PTFE V-ring", held_by="-", status="CHECK",
             note="same as the roller shaft"),
        dict(key="recoater_right", seal="Recoater screw through the right wall (Ø18 hole): floating bearing housing, open bore", held_by="-",
             status="MISSING", note="the housing's Ø8 bore is open to the room: make it a blind cap with a face O-ring"),
        dict(key="vac_port", seal="KF-25 vacuum port, KF-25 inlet/outlet plenum ports, KF-40 overflow, KF-16 blank", held_by="KF clamps",
             status="OK", note="Al centering ring + FKM; the stubs are 304 and the body 6061: the stub-to-body joint needs its own O-ring"),
        dict(key="plenums", seal="Inlet plenum (back wall) and outlet plenum (under the floor), 316L on 6061", held_by="M4/M5 (not drawn)",
             status="MISSING", note="joints.py lists them as 'each with an FKM O-ring', not drawn; dissimilar metals, so bolted + O-ring, never welded"),
        dict(key="threaded_ports", seal="Argon in (back wall), O2 sample (side wall), pressure transducer and relief valve (lid): 1/4 NPT parts",
             held_by="pipe threads", status="CHECK",
             note="NPT into 6061 leaks at vacuum and galls; use SAE/ISO straight-thread O-ring-boss ports or KF/VCR adapters"),
        dict(key="fibre_heads", seal="Through-beam fibre heads in Ø3.2 holes through both side walls (z = +5)", held_by="-",
             status="MISSING", note="needs O-ring-sealed threaded heads or a window; they also sit in the condensate and spatter zone"),
        dict(key="camera", seal="Camera viewport adapter with a Ø1 in. window over a Ø22 hole in the lid", held_by="screws (not drawn)",
             status="MISSING", note="two seals needed: adapter to lid, window to adapter"),
        dict(key="spigot", seal="Module spigot in the Ø96 floor port: FKM 2-238 radial (male gland)", held_by="radial; 2 captive M6",
             status="CHECK", note="groove as drawn (root Ø90.2, 3.6 mm wide) is overfilled at worst tolerance (101 %) and light on squeeze (13-21 %); root Ø90.5 x 4.8 wide gives 17-25 % and <= 81 %"),
        dict(key="gland_plate", seal="Gland plate on the welded collar: 1.78 mm cord face seal", held_by="6 x M4", status="CHECK",
             note="groove 2.4 wide: fill > 90 % at worst tolerance; widen to 2.6"),
        dict(key="rod", seal="Hollow rod through the gland plate: 'double FKM 2-114 rod gland' (grooves not drawn)", held_by="-",
             status="MISSING", note="draw two 2-114 grooves (Ø20.0 groove, Ø15.93 throat) and specify a seamless, polished rod; friction counts against the Z coupling"),
        dict(key="rod_end", seal="Rod end: heater and thermocouple leads potted in Torr Seal", held_by="-", status="FIX",
             note="stranded leads wick gas along the strands through any potting; use a hermetic (glass-to-metal) feedthrough or solid pins"),
        dict(key="gas_loop", seal="Blower, cyclone + HEPA housing, valves, hoses (KF-25 bellows)", held_by="KF clamps", status="CHECK",
             note="the HEPA housing in the BOM (McMaster 5169K72) is 1/2 NPSC threaded and its gas-tightness is not stated; the blower must be specified gas-tight"),
        dict(key="o2_sample", seal="O2 analyser sample loop", held_by="fittings", status="CHECK",
             note="extractive analysers often have polymer tubing inside; return the sample to the loop, 316L lines, leak-check the analyser"),
    ]
    R["inventory"] = inv

    # ---------------- gland checks ----------------
    glands = {}
    glands["lid"] = gland(3.53, 2.65, 4.6, T_service=70.0, groove_mat="al")
    glands["door_as_drawn"] = gland(3.53, 2.8, 4.0, T_service=60.0, groove_mat="al")
    glands["door_spec"] = gland(3.53, 2.65, 4.6, T_service=60.0, groove_mat="al")
    glands["door_1p78_halfdovetail"] = gland(1.78, 1.32, 2.30, T_service=60.0, groove_mat="al")
    glands["window_1p78"] = gland(1.78, 1.32, 2.30, T_service=80.0, groove_mat="al")
    glands["drawer_1p78"] = gland(1.78, 1.32, 2.30, T_service=60.0, groove_mat="al")
    # spigot 2-238 (ID 88.49 mm) on a Ø90.2 groove root in a Ø96 port; stretch 1.9 %
    st_238 = (90.2 - 88.49) / 88.49
    glands["spigot_as_drawn"] = gland(3.53, (96.0 - 90.2) / 2, 3.6, T_service=60.0, groove_mat="ss", stretch=st_238, kind="radial")
    st_238b = (90.5 - 88.49) / 88.49
    glands["spigot_groove_90p5_w4p8"] = gland(3.53, (96.0 - 90.5) / 2, 4.8, T_service=60.0, groove_mat="ss", stretch=st_238b, kind="radial")
    glands["gland_plate_as_drawn"] = gland(1.78, 1.3, 2.4, T_service=60.0, groove_mat="ss")
    glands["gland_plate_2p6"] = gland(1.78, 1.3, 2.6, T_service=60.0, groove_mat="ss")
    # 2-114 rod gland (female): Parker Table 4-2 groove Ø0.787 in on a 0.625 in rod -> depth 2.06 mm
    glands["rod_2_114"] = gland(2.62, (19.99 - 15.875) / 2, 3.6, T_service=110.0, groove_mat="ss", kind="rod")
    for k, v in glands.items():
        v["parker"] = parker_face_rule(v["cs"]) if v["kind"] == "face" else None
    R["glands"] = glands

    # ---------------- clamp forces ----------------
    def seal_force(cs, path_mm, squeeze):
        lo, hi = PARKER_LOAD_25.get(cs, (None, None))
        f_l = lindley(cs, squeeze)
        return dict(cs=cs, path_mm=path_mm, squeeze=100 * squeeze, N_per_mm=f_l, total_N=f_l * path_mm,
                    parker_range_N=(lo * 4.448 / IN * path_mm, hi * 4.448 / IN * path_mm) if lo and squeeze == 0.25 else None)

    dw, dh = g["door_seal_rect"]
    lw, lh = g["lid_seal_rect"]
    clamps = {}
    a_door = dw * dh * 1e-6
    a_lid = lw * lh * 1e-6
    clamps["E_75A_MPa"] = E75
    clamps["door_3p53_25"] = seal_force(3.53, g["door_path"], 0.25)
    clamps["door_3p53_15"] = seal_force(3.53, g["door_path"], 0.15)
    clamps["door_1p78_25"] = seal_force(1.78, g["door_path"], 0.25)
    clamps["door_1p78_15"] = seal_force(1.78, g["door_path"], 0.15)
    clamps["door_vacuum_force_N"] = ATM * a_door
    clamps["door_overpressure_20mbar_N"] = 2000.0 * a_door
    clamps["lid_3p53_25"] = seal_force(3.53, g["lid_path"], 0.25)
    clamps["lid_vacuum_force_N"] = ATM * a_lid
    clamps["lid_screws_preload_N"] = 20 * 0.75 * 14.2 * 450 * 0.5      # A4-70 M5, 75 % of proof, halved for the insert/torque scatter
    clamps["drawer_1p78_25"] = seal_force(1.78, g["drawer_path"], 0.25)
    clamps["drawer_out_force_20mbar_N"] = 2000.0 * (84e-3 * 14e-3)
    w_path = math.pi * (46.0 - 1.78) + 0.0
    clamps["window_1p78_25"] = seal_force(1.78, w_path, 0.25)
    clamps["window_lift_20mbar_N"] = 2000.0 * math.pi / 4 * (46e-3) ** 2
    clamps["window_weight_N"] = 2200 * math.pi / 4 * (50.8e-3) ** 2 * 8e-3 * 9.81
    clamps["latch_rating_N"] = 800 * 4.448
    R["clamps"] = clamps

    # ---------------- permeation and leak budget ----------------
    T_seal = {"lid": 50.0, "door": 45.0, "window": 60.0, "drawer": 50.0, "spigot": 56.0, "gland_plate": 60.0, "kf": 35.0, "rod": 117.0}
    # (name, O-ring ID mm equivalent, cross-section, squeeze, count, T)
    oring_set = [
        ("lid", g["lid_path"] / math.pi - 3.53, 3.53, 0.25, 1),
        ("door", g["door_path"] / math.pi - 1.78, 1.78, 0.25, 1),
        ("window (sandwich, inner ring)", 46.0 - 1.78, 1.78, 0.25, 1),
        ("window flange to lid", 80.0, 1.78, 0.25, 1),
        ("camera adapter + its window", 2 * 30.0, 1.78, 0.25, 1),
        ("metering base to lid", 2 * (100 + 12) / math.pi * 1.2, 1.78, 0.25, 1),
        ("reservoir dock face (proposed)", 2 * (95 + 48) / math.pi, 1.78, 0.25, 1),
        ("reservoir lid (proposed)", 2 * (110 + 48) / math.pi, 1.78, 0.25, 1),
        ("drawer", g["drawer_path"] / math.pi - 1.78, 1.78, 0.25, 1),
        ("plenums (2)", 2 * (130 + 40) / math.pi, 1.78, 0.25, 2),
        ("KF-25 (7) + KF-40 (2) + KF-16 (1) centering rings", None, None, None, 0),
        ("spigot 2-238", 88.49, 3.53, 0.20, 1),
        ("gland plate", 2 * 28.6 - 1.78, 1.78, 0.25, 1),
        ("rod gland 2 x 2-114 (in tandem: the outer one carries the gradient)", 15.54, 2.62, 0.20, 1),
    ]
    T_of = lambda name: next((v for k, v in T_seal.items() if name.startswith(k)), 45.0)
    perm = []
    p_o2 = 0.2095 * 1.013            # bar, O2 partial pressure difference (inside ~0)
    p_h2o = 0.5 * 0.0281            # bar, 50 % RH at 23 C
    for name, d_id, cs, sq, n in oring_set:
        if d_id is None:
            # KF: Al centering ring with an FKM ring, ID ~ 26 / 41 / 18 mm, squeeze set by the ring (~25 %)
            L_o2 = sum(m * parker_leak(f_perm(F_O2_26, 26, 35, EA_HE), d, p_o2, 0.25) for d, m in ((26.0, 7), (41.0, 2), (18.0, 1)))
            L_h2o = sum(m * parker_leak(f_perm(F_H2O_STURM, 25, 35, EA_HE), d, p_h2o, 0.25) for d, m in ((26.0, 7), (41.0, 2), (18.0, 1)))
            perm.append(dict(seal=name, T_C=35, O2_sccs=L_o2, H2O_sccs=L_h2o))
            continue
        T = T_of(name.split(" ")[0])
        Fo = f_perm(F_O2_26, 26, T, EA_HE)
        Fw = f_perm(F_H2O_STURM, 25, T, EA_HE)
        perm.append(dict(seal=name, T_C=T, O2_sccs=n * parker_leak(Fo, d_id, p_o2, sq), H2O_sccs=n * parker_leak(Fw, d_id, p_h2o, sq)))
    tot_o2 = sum(p["O2_sccs"] for p in perm)
    tot_h2o = sum(p["H2O_sccs"] for p in perm)
    R["permeation"] = dict(items=perm, total_O2_sccs=tot_o2, total_H2O_sccs=tot_h2o, Ea_He_kJ=EA_HE / 1000, Ea_N2_kJ=EA_N2 / 1000)

    # dynamic and other leak sources (mbar L/s of air at 1 atm differential); ranges from vendor data, see the note
    other = [
        dict(src="2 rotary shafts through elastomer V-rings / lip seals (recoater screw, metering roller)", air_mbarLs=(1e-5, 1e-3),
             fix="magnetic-fluid feedthrough (helium leak < 1e-10 mbar L/s class) or a magnetic coupling through a can (zero leak)"),
        dict(src="rod gland, 2 x 2-114 reciprocating", air_mbarLs=(1e-6, 1e-4), fix="edge-welded bellows over the rod"),
        dict(src="potted stranded leads at the rod end", air_mbarLs=(1e-5, 1e-2), fix="glass-to-metal hermetic connector or KF feedthrough"),
        dict(src="threaded NPT ports (5-8 joints)", air_mbarLs=(1e-6, 1e-3), fix="O-ring boss / VCR / KF"),
        dict(src="gas-tight side-channel blower, shaft seal", air_mbarLs=(1e-4, 1e-3), fix="hermetic (canned / magnetic-drive) blower"),
    ]
    R["other_leaks"] = other

    # envelope volume
    v_hoses = 5 * math.pi / 4 * 2.5 ** 2 * 61 / 1000.0          # 5 x 24 in KF-25 bellows, L
    V = g["v_chamber_L"] + 0.6 + v_hoses + g["v_filter_L"] + 0.5      # chamber, plenums, hoses, filter housing, blower
    R["envelope_L"] = dict(chamber=g["v_chamber_L"], plenums=0.6, hoses=v_hoses, filter=g["v_filter_L"], blower=0.5, total=V)
    p_op = ATM + 2000.0
    sccs_to_ppm_h = lambda q: q * 3600 / (V * 1000 * p_op / ATM) * 1e6

    # O2: during a build the overpressure stops bulk inflow through a leak, but O2 still back-diffuses through it.
    # For a leak channel at +20 mbar outflow, back-diffusion is suppressed when the outflow Peclet number is >> 1; we take the
    # inflow equal to the O2 share of the room-air leak rate at 1 atm as an upper bound during vacuum hold, and 1 % of it during
    # the overpressured build (an assumption, stated in the note).
    o2_perm_ppm_h = sccs_to_ppm_h(tot_o2)
    h2o_perm_ppm_h = sccs_to_ppm_h(tot_h2o)

    # outgassing (unbaked, after ~1 h): Al 6e-9 Torr L/s/cm2 -> mbar L/s/cm2 x 1.333 ; FKM 1e-6 Torr L/s/cm2 on its exposed area
    a_al = g["area_walls_cm2"] + 2 * 2 * (270 * 56 + 2 * 174 * 94) / 100.0 + 500.0      # walls + both faces of the liners + misc
    a_fkm_exposed = (g["lid_path"] * 1.0 + g["door_path"] * 0.6 + 400.0) / 100.0
    q_al = 6e-9 * 1.333 * a_al
    q_fkm = 1e-6 * 1.333 * a_fkm_exposed
    # 1 mbar L/s at 23 C = 0.987 std cc/s ... (1 std cc = 1.013 mbar L)
    mbarLs_to_sccs = 1 / 1.01325
    h2o_out_ppm_h = sccs_to_ppm_h((q_al + q_fkm) * mbarLs_to_sccs)
    # powder moisture: new AlSi10Mg 150 ppm by mass (Lubkowitz 2024, Karl Fischer [11]); aged or humid-stored powder higher
    w_powder = 150.0
    mg_h2o = [w_powder * x * 1e-6 * 1000 for x in (150, 300)]
    scc_h2o = [m / 18.015 * 22414 / 1000 for m in mg_h2o]
    ppm_if_released = [s / (V * 1000) * 1e6 for s in scc_h2o]
    R["budget"] = dict(V_L=V, O2_permeation_ppm_per_h=o2_perm_ppm_h, H2O_permeation_ppm_per_h=h2o_perm_ppm_h,
                       area_al_cm2=a_al, area_fkm_cm2=a_fkm_exposed, q_al_mbarLs=q_al, q_fkm_mbarLs=q_fkm,
                       H2O_outgassing_ppm_per_h_1h=h2o_out_ppm_h, powder_H2O_mg=mg_h2o, powder_H2O_ppm_if_released=ppm_if_released)

    # make-up flow to hold targets: x_ss = q_in / f
    targets = dict(O2_ppm=10.0, H2O_ppm=128.0)       # -40 C dew point = 128 ppmv
    q_o2_sccm = tot_o2 * 60
    q_h2o_sccm = ((q_al + q_fkm) * mbarLs_to_sccs + tot_h2o) * 60
    R["makeup"] = dict(O2_in_sccm=q_o2_sccm, H2O_in_sccm=q_h2o_sccm,
                       f_for_O2_10ppm_sccm=q_o2_sccm / (targets["O2_ppm"] * 1e-6 - 1e-6),
                       f_for_H2O_minus40C_sccm=q_h2o_sccm / (targets["H2O_ppm"] * 1e-6 - 2e-6))

    # ---------------- vacuum purge ----------------
    S_pump = 3 * 28.317 / 60.0                 # L/s, 3 cfm free-air displacement (McMaster 4396K21)
    d_cm, L_cm = 2.2, 2 * 61.0                 # effective bore of KF-25 bellows (corrugation) and two hoses to the pump
    C_visc = lambda p_mbar: 135 * d_cm ** 4 * p_mbar / L_cm * 0.6          # L/s, x0.6 for the bellows corrugation
    def s_eff(p):
        s = S_pump * (1 - (1.3e-2 / max(p, 1.4e-2)))        # displacement falls to 0 at the 1e-2 Torr ultimate
        c = C_visc(p)
        return s * c / (s + c)
    # integrate dt = -V dp / (S_eff p)
    ps = np.logspace(math.log10(1013.0), math.log10(1.0), 400)
    t = 0.0
    for a, b in zip(ps[:-1], ps[1:]):
        pm = math.sqrt(a * b)
        t += V * (a - b) / (s_eff(pm) * pm)
    tau_hi = V / s_eff(800.0)
    # purge cycles: ideal dilution from air with Ar 5.0 backfill
    x = 0.2095e6
    cyc = []
    for n in range(1, 5):
        x = x * (1.0 / 1013.0) + 1.0 * (1 - 1.0 / 1013.0)
        cyc.append(dict(cycle=n, O2_ppm_ideal=x))
    R["purge"] = dict(S_pump_Ls=S_pump, S_eff_at_800mbar_Ls=s_eff(800.0), S_eff_at_10mbar_Ls=s_eff(10.0), S_eff_at_1mbar_Ls=s_eff(1.0),
                      t_to_1mbar_s=t, tau_at_atm_s=tau_hi, cycles=cyc)

    # ---------------- powder beds during pump-down ----------------
    beds = {"reservoir L (56 mm of powder)": 0.056, "build cylinder, end of build (40 mm)": 0.040,
            "overflow jar (90 mm)": 0.090, "reservoir M (40 mm)": 0.040}
    lift = {}
    for name, h in beds.items():
        r_atm, dp, w = bed_lift_ratio(h, tau_hi, ATM)
        r_10, _, _ = bed_lift_ratio(h, tau_hi, 1000.0)
        lift[name] = dict(h_mm=1000 * h, dp_over_weight_at_atm=r_atm, dp_over_weight_at_10mbar=r_10, dp_Pa=dp, weight_Pa=w,
                          tau_needed_s_for_0p3=tau_min_for(h, 0.3))
    R["powder_lift"] = dict(tau_s=tau_hi, k_m2=k_kozeny(), beds=lift, u_mf_mm_s=1000 * u_mf())
    # soft pump: the slowest bed (overflow jar, 90 mm) needs tau >= tau_needed; a metering valve in parallel with the main valve
    # limits the flow until ~100 mbar. Choked air flow through a valve of flow coefficient Cv (Swagelok gas sizing):
    # q [std L/min] = 6950 Cv P1 [bar] * 0.471 * sqrt(1 / (Gg T1)), Gg = 1, T1 = 293 K
    tau_need = max(v["tau_needed_s_for_0p3"] for v in lift.values())
    s_soft = V / tau_need                                   # L/s at ~1 atm
    q_soft = s_soft * 60.0                                  # std L/min at 1 atm
    cv = q_soft / (6950 * 1.013 * 0.471 * math.sqrt(1 / 293.0))
    t_soft = tau_need * math.log(1013 / 100.0)
    R["soft_pump"] = dict(tau_needed_s=tau_need, S_soft_Ls=s_soft, q_std_L_min=q_soft, Cv=cv, t_to_100mbar_s=t_soft,
                          t_total_to_1mbar_s=t_soft + pu_t_rest(V, s_eff),
                          note="metering valve with Cv >= this in parallel with the KF-25 valve; open the main valve below ~100 mbar. "
                               "Back-fill through the same limit (the flowmeter-regulator 78595A5 set <= 25 L/min) and a sintered diffuser")

    # reservoir open path as drawn: Darcy flow through the powder column (M reservoir: slot 8 x 70, 40 mm of powder)
    A_slot = g["slot_w"] * 70.0 * 1e-6
    k = k_kozeny()
    q_20mbar = k * A_slot * 2000.0 / (POWDER["mu_ar"] * 0.040)          # m3/s of argon out through the reservoir
    q_vac = k * A_slot * ATM / (POWDER["mu_air"] * 0.040) / 2           # m3/s of air in (mean over a linear pressure drop)
    R["reservoir_open_path"] = dict(argon_out_at_20mbar_sccm=q_20mbar * 1e6 * 60, superficial_mm_s=1000 * q_20mbar / A_slot,
                                    u_mf_mm_s=1000 * u_mf(), air_in_at_vacuum_sccm=q_vac * 1e6 * 60)

    # ---------------- rate-of-rise acceptance test ----------------
    # Leak budget: room air through real leaks <= 1e-4 mbar L/s keeps O2 < 1 ppm/h at vacuum hold; outgassing dominates after 1 h.
    q_budget = 1e-4
    R["rate_of_rise"] = dict(V_L=V, leak_budget_mbarLs=q_budget, rise_mbar_per_min_leak=q_budget * 60 / V,
                             rise_mbar_per_min_outgassing=(q_al + q_fkm) * 60 / V,
                             note="isolate at <= 1 mbar after >= 1 h pumping; read a Pirani or capacitance gauge for 10 min")

    (OUT / "seals.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
    write_md(R)
    print(json.dumps(dict(V=V, t_pump=t, tau=tau_hi, o2_ppm_h=o2_perm_ppm_h, h2o_ppm_h=h2o_perm_ppm_h, h2o_out=h2o_out_ppm_h,
                          door_force=clamps["door_3p53_25"]["total_N"], door_vac=clamps["door_vacuum_force_N"],
                          res_out=R["reservoir_open_path"]), default=float, indent=1))


def fmt(x, nd=2):
    if x is None:
        return "–"
    if isinstance(x, (tuple, list)):
        return "–".join(fmt(v, nd) for v in x)
    if abs(x) >= 1000 or (abs(x) < 0.01 and x != 0):
        return f"{x:.2e}"
    return f"{x:.{nd}f}"


def write_md(R):
    g = R["geometry"]
    L = ["# Seals, leaks and purge: results (from `analysis/seals/seals.py`)", "",
         "Model: `cad/lpbf_low.build('M50', 'M')`. All forces in N, leaks in std cc/s (sccs) unless noted. Sources are listed at the end.", ""]
    L += ["## Seal inventory", "", "| Seal / penetration | Held by | Status | Note |", "|---|---|---|---|"]
    for s in R["inventory"]:
        L.append(f"| {s['seal']} | {s['held_by']} | **{s['status']}** | {s['note']} |")
    L += ["", "## Gland checks (Parker ORD 5700, AS568 tolerance, ±0.05 mm machining)", "",
          "| Gland | CS | depth × width | stretch | squeeze nom (min–max) % | fill nom / worst cold / worst warm % | Parker face rule |",
          "|---|---|---|---|---|---|---|"]
    for k, v in R["glands"].items():
        pr = v["parker"]
        rule = f"depth {pr['depth'][0]}–{pr['depth'][1]}, width {pr['w_gas'][0]}–{pr['w_gas'][1]} (gas) / {pr['w_liq'][0]}–{pr['w_liq'][1]} (liquid)" if pr else v["kind"]
        L.append(f"| {k} | {v['cs']} | {v['depth']:.2f} × {v['width']:.2f} | {v['stretch_pct']:.1f} % | {v['squeeze_nom']:.0f} ({v['squeeze_min']:.0f}–{v['squeeze_max']:.0f}) | "
                 f"{v['fill_nom']:.0f} / {v['fill_max_cold']:.0f} / {v['fill_max_hot']:.0f} at {v['T_service']:.0f} °C | {rule} |")
    c = R["clamps"]
    L += ["", f"## Closure forces (FKM 75A: E = {c['E_75A_MPa']:.2f} MPa from Gent; Lindley load per length)", "",
          "| Closure | Seal | Squeeze force | Parker Fig. 2-x range at 25 % | Available |", "|---|---|---|---|---|"]
    def row(name, s, avail):
        pr = s.get("parker_range_N")
        L.append(f"| {name} | {s['cs']} mm, {s['path_mm']:.0f} mm long, {s['squeeze']:.0f} % | {s['total_N']:.0f} N ({s['N_per_mm']:.2f} N/mm) | "
                 f"{fmt(pr[0], 0)}–{fmt(pr[1], 0)} N |" if pr else f"| {name} | {s['cs']} mm, {s['path_mm']:.0f} mm long, {s['squeeze']:.0f} % | {s['total_N']:.0f} N ({s['N_per_mm']:.2f} N/mm) | – |")
        L[-1] += f" {avail} |"
    row("Lid", c["lid_3p53_25"], f"20 × M5: ≥ {c['lid_screws_preload_N'] / 1000:.0f} kN; vacuum {c['lid_vacuum_force_N']:.0f} N")
    row("Door, as drawn (3.53 mm)", c["door_3p53_25"], f"vacuum {c['door_vacuum_force_N']:.0f} N; 2 latches rated {c['latch_rating_N']:.0f} N each")
    row("Door, 3.53 mm at 15 %", c["door_3p53_15"], f"+20 mbar pushes out {c['door_overpressure_20mbar_N']:.0f} N")
    row("Door, 1.78 mm at 25 %", c["door_1p78_25"], f"vacuum {c['door_vacuum_force_N']:.0f} N")
    row("Door, 1.78 mm at 15 %", c["door_1p78_15"], "latch preload needed at +20 mbar")
    row("Drawer", c["drawer_1p78_25"], f"+20 mbar pushes out {c['drawer_out_force_20mbar_N']:.1f} N; nothing clamps it")
    row("Window (sandwich)", c["window_1p78_25"], f"+20 mbar lifts {c['window_lift_20mbar_N']:.1f} N vs weight {c['window_weight_N']:.2f} N")
    p = R["permeation"]
    L += ["", "## Permeation (Parker §3.12.1) into the argon loop", "",
          f"Arrhenius temperature scaling with E_a = {p['Ea_He_kJ']:.0f} kJ/mol (Parker's He pair; the N₂ pair gives {p['Ea_N2_kJ']:.0f}).", "",
          "| Seal | T (°C) | O₂ (sccs) | H₂O (sccs) |", "|---|---|---|---|"]
    for it in p["items"]:
        L.append(f"| {it['seal']} | {it['T_C']:.0f} | {fmt(it['O2_sccs'])} | {fmt(it['H2O_sccs'])} |")
    b = R["budget"]
    L.append(f"| **Total** | | **{fmt(p['total_O2_sccs'])}** | **{fmt(p['total_H2O_sccs'])}** |")
    env = R["envelope_L"]
    L += ["", f"Gas envelope {b['V_L']:.1f} L (chamber {env['chamber']:.1f}, hoses {env['hoses']:.1f}, filter housing {env['filter']:.1f}, plenums and blower {env['plenums'] + env['blower']:.1f}).",
          f"Permeation alone adds **{b['O2_permeation_ppm_per_h']:.2f} ppm O₂/h** and {b['H2O_permeation_ppm_per_h']:.2f} ppm H₂O/h with no make-up flow.",
          f"Outgassing of {b['area_al_cm2']:.0f} cm² of bare Al and {b['area_fkm_cm2']:.0f} cm² of exposed FKM after ~1 h: {fmt(b['q_al_mbarLs'])} + {fmt(b['q_fkm_mbarLs'])} mbar·L/s, "
          f"**{b['H2O_outgassing_ppm_per_h_1h']:.0f} ppm H₂O/h**, falling roughly as 1/t.",
          f"150 g of powder holding 150 ppm (new, Karl Fischer [11]) to 300 ppm water by mass carries {b['powder_H2O_mg'][0]:.0f}–{b['powder_H2O_mg'][1]:.0f} mg: "
          f"**{b['powder_H2O_ppm_if_released'][0]:.0f}–{b['powder_H2O_ppm_if_released'][1]:.0f} ppmv** in the loop if a 200 °C plate drives it off.", ""]
    mk = R["makeup"]
    L += [f"Make-up argon to hold the targets at steady state: {mk['f_for_O2_10ppm_sccm']:.1f} sccm for 10 ppm O₂ against permeation; "
          f"{mk['f_for_H2O_minus40C_sccm']:.0f} sccm for a −40 °C dew point against wall and seal outgassing.", ""]
    L += ["Other leak sources (air at 1 atm, mbar·L/s; vendor-typical ranges):", "", "| Source | Range | Fix |", "|---|---|---|"]
    for o in R["other_leaks"]:
        L.append(f"| {o['src']} | {fmt(o['air_mbarLs'][0])}–{fmt(o['air_mbarLs'][1])} | {o['fix']} |")
    pu = R["purge"]
    L += ["", "## Vacuum purge", "",
          f"Pump 4396K21: {pu['S_pump_Ls']:.2f} L/s displacement; through two KF-25 bellows S_eff = {pu['S_eff_at_800mbar_Ls']:.2f} L/s at 800 mbar, "
          f"{pu['S_eff_at_10mbar_Ls']:.2f} at 10 mbar, {pu['S_eff_at_1mbar_Ls']:.2f} at 1 mbar. **Pump-down to 1 mbar: {pu['t_to_1mbar_s'] / 60:.1f} min**; "
          f"time constant at atmosphere {pu['tau_at_atm_s']:.1f} s.", "",
          "| Cycle (pump to 1 mbar, back-fill Ar 5.0) | O₂, ideal (ppm) |", "|---|---|"]
    for cy in pu["cycles"]:
        L.append(f"| {cy['cycle']} | {fmt(cy['O2_ppm_ideal'])} |")
    pl = R["powder_lift"]
    L += ["", f"### Powder beds while pumping (Kozeny–Carman k = {pl['k_m2']:.2e} m², Klinkenberg slip; U_mf = {pl['u_mf_mm_s']:.1f} mm/s)", "",
          "| Bed | depth (mm) | Δp / bed weight at 1 atm | at 10 mbar | τ = V/S needed for ≤ 0.3 (s) |", "|---|---|---|---|---|"]
    for n, v in pl["beds"].items():
        L.append(f"| {n} | {v['h_mm']:.0f} | {v['dp_over_weight_at_atm']:.2f} | {v['dp_over_weight_at_10mbar']:.2f} | {v['tau_needed_s_for_0p3']:.0f} |")
    sp = R["soft_pump"]
    L += ["", f"**Soft pump:** the overflow jar needs τ ≥ {sp['tau_needed_s']:.0f} s, i.e. ≤ {sp['S_soft_Ls']:.2f} L/s ({sp['q_std_L_min']:.0f} std L/min) "
          f"until ~100 mbar: a metering valve of Cv ≥ {sp['Cv']:.2f} beside the main valve. Pump-down then takes ~{sp['t_total_to_1mbar_s'] / 60:.1f} min to 1 mbar. {sp['note']}.", ""]
    ro = R["reservoir_open_path"]
    L += ["", f"Reservoir as drawn (open to the room through the powder column): at +20 mbar, **{ro['argon_out_at_20mbar_sccm']:.0f} sccm of argon leaves through the powder** "
          f"at {ro['superficial_mm_s']:.1f} mm/s superficial velocity, against a minimum fluidization velocity of {ro['u_mf_mm_s']:.1f} mm/s. Pumping down, "
          f"room air comes in at ~{ro['air_in_at_vacuum_sccm']:.0f} sccm.", ""]
    rr = R["rate_of_rise"]
    L += ["## Rate-of-rise acceptance test", "",
          f"Leak budget {fmt(rr['leak_budget_mbarLs'])} mbar·L/s in {rr['V_L']:.1f} L is a rise of {fmt(rr['rise_mbar_per_min_leak'])} mbar/min; "
          f"outgassing after ~1 h adds {fmt(rr['rise_mbar_per_min_outgassing'])} mbar/min. {rr['note']}.", "", "## Sources", ""]
    for k, v in R["sources"].items():
        L.append(f"{k}. {v}")
    (OUT / "seals.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
