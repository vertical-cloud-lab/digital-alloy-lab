"""Temperatures of the monitoring cameras, photodiodes and Pis in the laser guard, and the cooling that keeps them in their
ratings (issue #260, PR 281; monitoring/cooling.md). Writes analysis/out/monitoring/cooling/cooling.json and cooling.md.

1. The guard's air: a well-mixed node with the heat that is released inside the guard (the galvo, the servos, the Pis, the
   cameras and the chamber's outside), the bare aluminium panels' natural convection and radiation to the Shuttle's air, and,
   with the drawn cooling, the flow two 120 mm exhaust fans pull through the light-trapped inlet and exhaust (fan curve
   against the system's resistance). The supply is the Shuttle's air, or room air from a ventilated dock, or (not drawn) a
   chilled-water fan coil with the vents closed.
2. Each device: its own dissipation to the air round it (natural or forced convection plus radiation to the guard's inner
   surfaces at that air's temperature), radiation from the 60 °C chamber wall or lid it faces, and conduction through its
   mount from the part it is bolted to (chamber floor plate, LP boss on the lid, optics bridge, base plate).
3. The light traps' 1070 nm attenuation (trap_mc.py), against safety.md's OD >= 5.4 for a 500 W beam.

Ratings come from the vendor pages read through the lab tunnel on 2026-11-27 (ratings.csv next to the JSON; URLs and read
times there). Every other number is marked as an estimate where it is one.
Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/cooling/cooling.py   (~1 min; no CAD needed)
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import sys

import numpy as np
from scipy.optimize import brentq

HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parents[2]
OUT = D / "analysis" / "out" / "monitoring" / "cooling"
sys.path.insert(0, str(D / "cad"))
sys.path.insert(0, str(HERE))
import monitoring_cooling as MC  # noqa: E402
import trap_mc  # noqa: E402

SIG = 5.670e-8
RHO_AIR, CP_AIR, K_AIR, NU_AIR, PR = 1.13, 1007.0, 0.0270, 1.70e-5, 0.71      # air near 40 °C


# ================================================================================================ inputs
def shuttle_cases():
    """Shuttle air from analysis/out/tray/tray_budget.json (heat.md §2): a typical build with Shuttle 1 idling, and with
    PR 318's busy case; the worst build (500 W continuous) with the busy case"""
    tb = json.load(open(D / "analysis" / "out" / "tray" / "tray_budget.json"))
    room = tb["shuttle"]["room_c"]
    ph = tb["phases"]
    typ = ph["building, typical (Al at 350 W, beam on 60 %)"]
    worst = ph["building, worst (500 W, beam on continuously)"]
    return room, {
        "typical": dict(T_s=round(room + typ["shuttle_rise_k_with_idle_shuttle"], 1), load="typical",
                        what="typical build, rest of Shuttle 1 idling"),
        "busy": dict(T_s=round(room + typ["shuttle_rise_k_with_busy_shuttle"], 1), load="typical",
                     what="typical build, PR 318's busy Shuttle"),
        "busy_worst": dict(T_s=round(room + worst["shuttle_rise_k_with_busy_shuttle"], 1), load="worst",
                           what="500 W continuous, PR 318's busy Shuttle"),
    }, typ, worst


# heat released inside the guard (W): (typical build, worst build), with the basis
SOURCES = {
    "galvo (basiCube 20)": ((30.0, 69.3), "tray_budget.json loads 'galvo' (estimate 30 W typical; 24 V x 2.6 A rated)"),
    "Z and recoater servos": ((20.0, 20.0), "tray_budget.json 'servos' 30 W for three ClearPath-SD axes, two inside the guard (estimate)"),
    "dosing stepper": ((5.0, 10.0), "NEMA 17 holding current (estimate)"),
    "PB2 (Pi 5, lid sensors, DC-DC)": ((8.0, 12.0), "electrical analysis/out/electrical/power.md §4 'Pi 5 + DC-DC'"),
    "LP camera's Pi 5 (second Pi)": ((5.0, 8.0), "Pi 5 brief: ~4 W bare board active (800 mA at 5 V) + one camera (estimate)"),
    "Chronos 2.1-HD": ((20.0, 40.0), "Kron: 40 W input rating; typical draw not published (half assumed)"),
    "two PDA36A2": ((4.0, 10.0), "Thorlabs: 'actual usage < 5 W' each; 2 W each typical assumed"),
    "IMX296 boards (LP, coaxial)": ((1.5, 2.0), "not published by InnoMaker; ~0.75 W each assumed"),
    "BW 850 nm LED": ((1.0, 5.1), "M850LP1: 5.1 W at 1.5 A CW; pulsed, ~1 W mean assumed"),
    "AE preamp": ((1.0, 2.1), "MISTRAS PreAmp One 28 V: < 1.0 W quiescent, < 2.1 W max"),
    "layer camera (Pi HQ)": ((1.0, 1.5), "estimate"),
    "beam path (collimator, shutter coil, dichroic, beam trap, f-theta)": ((5.0, 12.0), "estimate: ~1 % of the beam plus a held shutter coil"),
    "guard fans (2 x AFB1224SH, 60 mm, 40 mm)": ((0.0, 0.0), "added per configuration from the fan data"),
}


def device_sum(load):
    i = 0 if load == "typical" else 1
    return sum(v[0][i] for v in SOURCES.values())


# ================================================================================================ guard passive loss
def h_vert(dT, L):
    """laminar natural convection, vertical plate in air (Incropera's simplified 1.42 (dT/L)^0.25)"""
    return 1.42 * (max(abs(dT), 0.1) / L) ** 0.25


def h_rad(eps, T):
    return eps * 4 * SIG * (T + 273.15) ** 3


EPS_PANEL = [0.07]                                     # bare 5052; a sensitivity sets it to 0.9 (painted)


def guard_passive_UA(T_g, T_s):
    """panels (bare 5052, eps 0.07 both faces; the PC viewing window eps 0.9) and the base plate's underside, from the guard's air
    to the Shuttle's air: inside convection, sheet, outside convection + radiation in series"""
    G = MC.GUARD
    H = (G["z1"] - G["z0"]) / 1000
    W, Dp = (G["x1"] - G["x0"]) / 1000, (G["y1"] - G["y0"]) / 1000
    A_side, A_fb, A_top = H * Dp, H * W, W * Dp
    x0, x1, z0, z1 = G["door_window"]
    A_win = (x1 - x0) * (z1 - z0) * 1e-6
    A_al = 2 * A_side + 2 * A_fb - A_win
    dT = max(abs(T_g - T_s), 0.5)                         # the guard may be cooler than the Shuttle (dock air, fan coil)
    Tm = 0.5 * (T_g + T_s)
    eps_al, eps_pc = EPS_PANEL[0], 0.9
    hi = h_vert(dT / 2, H) + h_rad(eps_al, Tm) * 0.5          # inside: convection, little radiation between bare sheets
    ho = h_vert(dT / 2, H) + h_rad(eps_al, Tm)
    U_al = 1 / (1 / hi + 1 / ho)
    U_win = 1 / (1 / (h_vert(dT / 2, H) + h_rad(eps_pc, Tm)) + 0.006 / 0.2 + 1 / (h_vert(dT / 2, H) + h_rad(eps_pc, Tm)))
    Lc = A_top / (2 * (W + Dp))
    Ra = 9.81 / (Tm + 273.15) * (dT / 2) * Lc ** 3 / (NU_AIR * 2.4e-5)
    h_up = 0.54 * Ra ** 0.25 * K_AIR / Lc
    U_top = 1 / (1 / (h_up + h_rad(eps_al, Tm) * 0.5) + 1 / (h_up + h_rad(eps_al, Tm)))
    # base plate (the guard's floor, 15 mm MIC-6): stable layer above it, a heated plate facing down below it
    h_dn = 0.27 * Ra ** 0.25 * K_AIR / Lc
    U_base = 1 / (1 / 1.5 + 1 / (h_dn + h_rad(eps_al, Tm)))
    UA = U_al * A_al + U_win * A_win + U_top * A_top + U_base * A_top
    return UA, dict(A_panels_m2=round(A_al + A_win + A_top, 3), U_panel=round(U_al, 2), U_window=round(U_win, 2), U_top=round(U_top, 2),
                    U_base=round(U_base, 2), UA_W_per_K=round(UA, 2))


# chamber outside: walls 2 x (312 + 222) x 124 mm, lid top 312 x 222, floor plate's underside (less the module port), module below
A_CH = 2 * (0.312 + 0.222) * 0.124 + 0.312 * 0.222 + (0.312 * 0.222 - 0.0064) + 0.03
G_LEGS = 4 * 167.0 * 0.030 * 0.030 / 0.140            # four 30 x 30 6061 legs, 140 mm, to the base plate (lpbf_low.py)


def chamber_release(T_w, T_g, eps_w=0.1, v=0.0):
    """heat the chamber's outside gives the guard (W) at a wall temperature T_w: convection (natural, or mixed with the guard's
    flow at speed v) and radiation (bare 6061, eps 0.1; anodised outside 0.8) to the guard's inner surfaces, which are at the
    air's temperature; plus the legs into the base plate, which gives it to the guard's air"""
    dT = max(T_w - T_g, 0.0)
    h_nat = h_vert(dT, 0.124)
    h_f = 0.664 * (max(v, 1e-6) * 0.3 / NU_AIR) ** 0.5 * PR ** (1 / 3) * K_AIR / 0.3 if v > 0 else 0.0
    h = (h_nat ** 3 + h_f ** 3) ** (1 / 3) + h_rad(eps_w, 0.5 * (T_w + T_g))
    return h * A_CH * dT + G_LEGS * dT * 0.5


# ================================================================================================ fans and the system's resistance
FANS = {  # (m3/h, Pa) points read off the makers' curves by the price reader (price_lookups_round3_cooling.csv)
    "AFB1224SH": dict(curve=[(0, 107), (30, 87), (60, 63), (90, 45), (120, 38), (150, 27), (180, 10), (192, 0)], W=6.72, dBA=46.5,
                      key="CL5", what="Delta AFB1224SH, 120 x 120 x 25.4 mm, 24 V, 3400 rpm"),
    "AFB1224M": dict(curve=[(0, 50.5), (30, 35), (60, 21), (90, 14), (120, 3), (125, 0)], W=2.88, dBA=35.5,
                     key="CL6", what="Delta AFB1224M, 120 mm, 24 V, 2200 rpm"),
}


def fan_dp(name, q_m3h, n_parallel=1):
    pts = np.array(FANS[name]["curve"], float)
    q = q_m3h / n_parallel
    if q >= pts[-1, 0]:
        return -1.0 * (q - pts[-1, 0])
    return float(np.interp(q, pts[:, 0], pts[:, 1]))


def idelchik_bend(delta_deg):
    """sharp bend in a channel (Idelchik, Handbook of Hydraulic Resistance, diagram 6-5: 0.95 sin^2(d/2) + 2.05 sin^4(d/2))"""
    s = math.sin(math.radians(delta_deg) / 2)
    return 0.95 * s * s + 2.05 * s ** 4


def trap_K():
    """loss coefficient of the chevron trap on its passage velocity: n - 1 internal turns of 2*phi, entry and exit turns of phi,
    a x1.5 allowance for the low Reynolds number (~10^3) on Idelchik's high-Re values, laminar friction, contraction and expansion"""
    L = MC.LOUVRE
    por, gap, phi = trap_mc.porosity(L["D"], L["A"], L["n"], L["p"], L["t"])
    K_turns = (L["n"] - 1) * idelchik_bend(2 * phi) + 2 * idelchik_bend(phi)
    Dh = 2 * gap / 1000
    v_ref = 1.5
    Re = v_ref * Dh / NU_AIR
    f = 96 / Re
    Lp = L["D"] / math.cos(math.radians(phi)) / 1000
    K = 1.5 * K_turns + f * Lp / Dh + 0.5 * (1 - por) + (1 - por) ** 2
    return K, por, dict(phi_deg=round(phi, 1), gap_mm=round(gap, 2), porosity=round(por, 3), K_turns=round(K_turns, 2),
                        K_total=round(K, 2), Re_at_1p5=round(Re))


def dp_trap(q_m3h, face_m2):
    K, por, _ = trap_K()
    v = q_m3h / 3600 / (face_m2 * por)
    return K * 0.5 * RHO_AIR * v * v


def dp_filter(q_m3h, face_m2):
    """10 mm G3/G4 pad: ~20 Pa at 1 m/s face velocity, roughly linear (estimate; Qualtek and Orion publish no pressure drop)"""
    return 20.0 * (q_m3h / 3600 / face_m2)


def dp_exhaust_extra(q_m3h, n_fans):
    """plenum contraction onto the fans and the finger guards (K 0.5 + 0.3 on the fans' annulus velocity, estimate)"""
    a = n_fans * (math.pi / 4) * (0.114 ** 2 - 0.04 ** 2)
    v = q_m3h / 3600 / a
    return 0.8 * 0.5 * RHO_AIR * v * v


def operating_point(fan="AFB1224SH", n=2):
    """exhaust fans against the inlet filter + inlet trap + exhaust trap + plenum/guards (seam leakage ignored: it adds flow)"""
    A_in = MC.opening_area_m2("inlet")
    A_ex = MC.opening_area_m2("exhaust")

    def sys_dp(q):
        return dp_filter(q, A_in) + dp_trap(q, A_in) + dp_trap(q, A_ex) + dp_exhaust_extra(q, n)
    q = brentq(lambda q: fan_dp(fan, q, n) - sys_dp(q), 1.0, FANS[fan]["curve"][-1][0] * n - 0.01)
    return q, dict(fan=FANS[fan]["what"], n=n, q_m3h=round(q, 1), dp_Pa=round(sys_dp(q), 1),
                   dp_filter=round(dp_filter(q, A_in), 1), dp_inlet_trap=round(dp_trap(q, A_in), 1),
                   dp_exhaust_trap=round(dp_trap(q, A_ex), 1), dp_plenum_guards=round(dp_exhaust_extra(q, n), 1),
                   inlet_face_m2=A_in, exhaust_face_m2=A_ex, fan_power_W=FANS[fan]["W"] * n)


def hood_flow():
    """the 60 mm hood fan (Delta AFB0624H-A, curve read off Delta's datasheet: price_lookups_round3_cooling.csv CL90) pushes air from
    the plenum behind the inlet trap's right part through the duct into the hood"""
    A_part = (MC.PLENUM["x"][1] - MC.PLENUM["x"][0]) * (MC.INLET["z"][1] - MC.INLET["z"][0]) * 1e-6
    A_d1 = (MC.DUCT1["x"][1] - MC.DUCT1["x"][0] - 2) * (MC.DUCT1["z"][1] - MC.DUCT1["z"][0] - 2) * 1e-6
    K_duct = 1.2 + 1.2 + 1.5 + 1.0 + 1.0        # plenum turn up, turn forward, the fan's bulkhead, the drop into the hood, the hood's exit

    def sys_dp(q):
        v = q / 3600 / A_d1
        return dp_filter(q, A_part) + dp_trap(q, A_part) + K_duct * 0.5 * RHO_AIR * v * v
    fan = [(0, 52.0), (12, 33.0), (20, 16.0), (29, 15.0), (34, 8.0), (40, 0.0)]
    pts = np.array(fan)
    q = brentq(lambda q: float(np.interp(q, pts[:, 0], pts[:, 1])) - sys_dp(q), 0.5, 39.9)
    # the hood's free section along the camera: hood inside 131 x 140 mm less the body (96 x 67.3) and the bracket's share
    A_hood = (MC.HOOD["y"][1] - MC.HOOD["y"][0] - 2) * (MC.HOOD["z"][1] - MC.HOOD["z"][0] - 2) * 1e-6 - 0.096 * 0.0673 - 0.08 * 0.016
    return q, dict(q_m3h=round(q, 1), dp_Pa=round(sys_dp(q), 1), duct_area_m2=round(A_d1, 4), hood_free_area_m2=round(A_hood, 4),
                   v_along_camera_m_s=round(q / 3600 / A_hood, 2), fan="Delta AFB0624H-A, 60 x 60 x 25 mm, 24 V, 2.2 W, 34 dB(A)")


# ================================================================================================ devices
def h_forced(v, L):
    Re = max(v, 1e-6) * L / NU_AIR
    return 0.664 * Re ** 0.5 * PR ** (1 / 3) * K_AIR / L


DEVICES = [
    # name, rating (low, high, basis), P (typ, worst), A_conv m², L m, mount, G_mount W/K (as drawn), G_mount with the break,
    # wall view: (A_rad m², F, eps_eff with a bare / anodised wall), where (zone)
    dict(name="Chronos 2.1-HD (side camera)", rating=(-20, 40, "ambient (Kron: -20 to +40 C; has its own fan)"), P=(20.0, 40.0),
         A=0.0635, L=0.155, mount="chamber floor plate (bracket root)", G_m=1.3, G_m_break=0.10, rad=(0.0065, 0.45),
         zone="hood", own_fan=True, check="air"),
    dict(name="LP camera (IMX296 board in a housing)", rating=(0, 50, "ambient (Pi GS camera brief; InnoMaker publishes none)"),
         P=(0.75, 1.0), A=0.012, L=0.04, mount="LP boss on the lid (filter holder, lens)", G_m=0.4, G_m_break=0.017, rad=(0.004, 0.3),
         zone="upper", check="case"),
    dict(name="Coaxial camera (IMX296 board on the cage)", rating=(0, 50, "ambient (Pi GS camera brief)"), P=(0.75, 1.0), A=0.007,
         L=0.038, mount="optics bridge (cage post)", G_m=1.0, G_m_break=None, rad=None, zone="upper", check="case"),
    dict(name="Alvium 1800 U-030 VSWIR (route B, in the coaxial arm)", rating=(-20, 55, "housing (Allied Vision)"), P=(2.2, 2.2),
         A=0.0055, L=0.029, mount="optics bridge (cage post)", G_m=1.0, G_m_break=None, rad=None, zone="upper", check="case"),
    dict(name="Photodiode PDA36A2 (each)", rating=(10, 40, "not stated ambient or case (Thorlabs)"), P=(2.0, 5.0), A=0.013,
         L=0.071, mount="optics bridge (cage post)", G_m=1.0, G_m_break=None, rad=None, zone="upper", check="air"),
    dict(name="BW 850 nm LED (M850LP1 class)", rating=(0, 40, "ambient (Thorlabs; casing up to +25 K)"), P=(1.0, 5.1), A=0.012,
         L=0.057, mount="free (on its own bracket)", G_m=0.0, G_m_break=None, rad=(0.0013, 0.5), zone="lower", check="air"),
    dict(name="AE preamp (PreAmp One)", rating=(-40, 65, "operating (MISTRAS)"), P=(1.0, 2.1), A=0.04, L=0.15,
         mount="base plate", G_m=0.5, G_m_break=None, rad=None, zone="lower", check="case"),
    dict(name="Galvo basiCube 20 (context)", rating=(15, 35, "operating (SCANLAB: 25 +/- 10 C)"), P=(0.0, 0.0), A=0.12, L=0.155,
         mount="optics bridge", G_m=0.0, G_m_break=None, rad=None, zone="upper", check="air"),
    dict(name="Kowa LM50JC10M lenses", rating=(-10, 50, "Kowa"), P=(0.0, 0.0), A=0.01, L=0.05, mount="(on the cameras)", G_m=0.0,
         G_m_break=None, rad=None, zone="upper", check="air"),
]


def T_bridge(T_air, load, v=0.0):
    """optics bridge: most of the galvo's heat (70 %: its own 0.12 m2 would need ~40 K to shed 30 W, so it goes down its riser) and
    the beam-path absorbers into a 25 mm 6061 plate (0.605 x 0.37 m, both faces, bare) that also conducts to the base plate through
    four 60 x 60 x 5 posts (371 mm), half of whose conductance is counted (the base plate is itself warm)"""
    i = 0 if load == "typical" else 1
    Q = 0.7 * SOURCES["galvo (basiCube 20)"][0][i] + SOURCES["beam path (collimator, shutter coil, dichroic, beam trap, f-theta)"][0][i]
    A = 2 * 0.605 * 0.37
    h = max(3.5, h_forced(v, 0.4)) + h_rad(0.1, T_air)
    G_posts = 4 * 167.0 * (0.06 ** 2 - 0.05 ** 2) / 0.371
    return T_air + Q / (h * A + 0.5 * G_posts)


def device_T(dev, T_air, T_wall, T_mount, load, v=0.0, brk=False, eps_wall=0.1):
    """steady case (or sensor-board) temperature: P + h A (T_air - T) + G_rad (T_wall - T) + G_m (T_mount - T) = 0"""
    i = 0 if load == "typical" else 1
    P = dev["P"][i]
    h_n = 1.32 * (2.0 / dev["L"]) ** 0.25                                 # small body, laminar, a few K above the air
    h = max(h_n, h_forced(v, dev["L"])) + h_rad(0.85, T_air)              # anodised / painted housings, eps ~0.85
    if dev.get("own_fan"):
        h = max(h, 25.0)                                                  # its fan moves air through the body (estimate)
    Gc = h * dev["A"]
    Gr = 0.0
    if dev["rad"]:
        A_r, F = dev["rad"]
        eps_eff = 1 / (1 / 0.85 + 1 / eps_wall - 1)
        Gr = eps_eff * F * A_r * 4 * SIG * (0.5 * (T_wall + T_air) + 273.15) ** 3
    Gm = dev["G_m_break"] if (brk and dev["G_m_break"] is not None) else dev["G_m"]
    T = (P + Gc * T_air + Gr * T_wall + Gm * T_mount) / (Gc + Gr + Gm)
    return T, dict(P=P, G_air=round(Gc, 3), G_rad=round(Gr, 4), G_mount=round(Gm, 3))


# ================================================================================================ configurations
def guard_air(T_s, load, config, q_ex=0.0, T_in=None, T_w=60.0, eps_w=0.1, T_water=20.0, fan_W=0.0, leak_m3h=0.0):
    """steady guard air (°C) for a configuration; returns T_g, the chamber's release, and the heat balance"""
    Qd = device_sum(load) + fan_W

    def resid(T_g):
        UA, _ = guard_passive_UA(T_g, T_s)
        v = 0.0
        if config in ("vent_shuttle", "vent_dock"):
            v = 0.25                                                      # mean air speed past the chamber with ~150 m3/h (estimate)
        Qc = chamber_release(T_w, T_g, eps_w, v)
        Q_vent = RHO_AIR * CP_AIR * q_ex / 3600 * (T_g - (T_in if T_in is not None else T_s)) if q_ex else 0.0
        Q_coil = 0.0
        if config == "fan_coil":
            Q_coil = 15.0 * (T_g - T_water)                               # 120 mm radiator + fan, UA ~15 W/K (estimate)
        Q_leak = RHO_AIR * CP_AIR * leak_m3h / 3600 * (T_g - T_s)
        return Qd + Qc - UA * (T_g - T_s) - Q_vent - Q_coil - Q_leak
    T_g = brentq(resid, -20.0, 200.0)
    UA, ua = guard_passive_UA(T_g, T_s)
    v = 0.25 if config in ("vent_shuttle", "vent_dock") else 0.0
    Qc = chamber_release(T_w, T_g, eps_w, v)
    return T_g, dict(T_g=round(T_g, 1), Q_devices_W=round(Qd, 1), Q_chamber_W=round(Qc, 1), UA_passive=ua,
                     Q_through_panels_W=round(UA * (T_g - T_s), 1),
                     Q_vent_W=round(RHO_AIR * CP_AIR * q_ex / 3600 * (T_g - (T_in if T_in is not None else T_s)), 1) if q_ex else 0.0,
                     Q_coil_W=round(15.0 * (T_g - T_water), 1) if config == "fan_coil" else 0.0)


def run():
    room, cases, typ, worst = shuttle_cases()
    q_ex, op = operating_point("AFB1224SH", 2)
    q_hood, hood = hood_flow()
    fan_W = op["fan_power_W"] + 2.16 + 1.08                                 # 2 x AFB1224SH + AFB0624H-A (2.16 W) + NF-A4x10 24V (1.08 W max)
    configs = {
        "as_drawn": dict(what="as drawn before this round: closed guard, no fans, no breaks", q=0.0, T_in=None, brk=False, hood=False),
        "vent_shuttle": dict(what="drawn cooling, supply from the Shuttle's air", q=q_ex, T_in="T_s", brk=True, hood=True),
        "vent_dock": dict(what="drawn cooling, supply ducted from the room through a ventilated dock (22 C)", q=q_ex, T_in=room, brk=True, hood=True),
        "fan_coil": dict(what="not drawn: vents closed, a chilled-water fan coil (20 C water, UA 15 W/K) in the guard", q=0.0, T_in=None, brk=True,
                         hood=False),
    }
    res = {}
    for ck, c in cases.items():
        T_s = c["T_s"]
        for gk, g in configs.items():
            T_in = T_s if g["T_in"] == "T_s" else g["T_in"]
            fw = fan_W if gk in ("vent_shuttle", "vent_dock") else (6.0 if gk == "fan_coil" else 0.0)
            T_g, bal = guard_air(T_s, c["load"], gk, g["q"], T_in, fan_W=fw)
            v_bulk = 0.25 if gk in ("vent_shuttle", "vent_dock") else 0.0
            Tbr = T_bridge(T_g, c["load"], v_bulk)
            rows = []
            for dev in DEVICES:
                if dev["zone"] == "hood" and g["hood"]:
                    T_air = T_in + 0.5                                     # duct air, picks up ~0.5 K on its way (estimate)
                    v = hood["v_along_camera_m_s"]
                else:
                    T_air = T_g
                    v = v_bulk
                if "floor plate" in dev["mount"]:
                    T_m = 60.0
                elif "LP boss" in dev["mount"]:
                    T_m = 60.0
                elif "bridge" in dev["mount"]:
                    T_m = Tbr
                else:
                    T_m = T_g
                T_dev, terms = device_T(dev, T_air, 60.0, T_m, c["load"], v, g["brk"])
                lo, hi, basis = dev["rating"]
                checked = T_air if dev["check"] == "air" else T_dev
                rows.append(dict(device=dev["name"], rating_c=[lo, hi], rating_basis=basis, air_c=round(T_air, 1), case_c=round(T_dev, 1),
                                 checked_c=round(checked, 1), margin_k=round(hi - checked, 1), ok=bool(checked <= hi), mount_c=round(T_m, 1),
                                 terms=terms))
            # PB2 box and the Pis
            pb2 = pb2_and_pis(T_g, c["load"], vented=(gk != "as_drawn"))
            pb2["pb2_sealed_box_air_c"] = pb2_and_pis(T_g, c["load"], vented=False)["pb2_box_air_c"]
            pb2["pb2_sealed_soc_c"] = pb2_and_pis(T_g, c["load"], vented=False)["pb2_soc_c"]
            res[f"{ck}/{gk}"] = dict(shuttle=c, config=g["what"], T_in=round(T_in, 1) if T_in is not None else None, guard=bal,
                                     bridge_c=round(Tbr, 1), devices=rows, pis=pb2)
    # sensitivities of the closed guard (typical case): painted panels (eps 0.9 both faces), and seams leaking 5 or 15 m3/h
    sens = {}
    T_s0 = cases["typical"]["T_s"]
    EPS_PANEL[0] = 0.9
    sens["painted panels (eps 0.9)"] = round(guard_air(T_s0, "typical", "as_drawn")[0], 1)
    EPS_PANEL[0] = 0.07
    for lk in (5.0, 15.0):
        sens[f"seams leaking {lk:.0f} m3/h"] = round(guard_air(T_s0, "typical", "as_drawn", leak_m3h=lk)[0], 1)
    sens["chamber wall anodised outside (eps 0.8), vented, Shuttle air"] = round(guard_air(T_s0, "typical", "vent_shuttle", q_ex, T_s0, eps_w=0.8,
                                                                                         fan_W=fan_W)[0], 1)
    traps = trap_results()
    alt = {}
    for nm in ("AFB1224M",):
        try:
            alt[nm] = operating_point(nm, 2)[1]
        except ValueError:
            alt[nm] = "no operating point"
    shuttle_k_per_W = 1.0 / (5.5 * 55.9)                                  # tray_budget.json's still-air Shuttle: 5.5 W/m2K x 55.9 m2
    budget = {}
    for ck in cases:
        b = {}
        for gk in ("vent_shuttle", "vent_dock", "fan_coil"):
            g = res[f"{ck}/{gk}"]["guard"]
            if gk == "vent_shuttle":
                b[gk] = dict(added_W=round(fan_W, 1), removed_W=0.0, note="the guard's heat stays in the Shuttle; only the fans are new")
            elif gk == "vent_dock":
                b[gk] = dict(added_W=round(fan_W, 1), removed_W=round(g["Q_vent_W"], 1),
                             shuttle_change_K=round((fan_W - g["Q_vent_W"]) * shuttle_k_per_W, 2), air_m3h=round(q_ex, 0))
            else:
                b[gk] = dict(added_W=6.0, removed_W=round(g["Q_coil_W"], 1), shuttle_change_K=round((6.0 - g["Q_coil_W"]) * shuttle_k_per_W, 2),
                             chiller_load_W=round(g["Q_coil_W"], 1))
        budget[ck] = b
    return dict(cases=cases, room_c=room, operating_point=op, alternative_fans=alt, sensitivity_typical_guard_air_c=sens, hood=hood, trap=traps, results=res, shuttle_budget=budget,
                sources={k: dict(W_typical=v[0][0], W_worst=v[0][1], basis=v[1]) for k, v in SOURCES.items()},
                chamber=dict(A_out_m2=round(A_CH, 3), G_legs_W_per_K=round(G_LEGS, 2), T_wall_c=60.0,
                             note="the 60 C wall is thermal.json's hot-chamber bound, not a result: a typical build puts ~300 W into the "
                                  "chamber (heaters ~97 W + 210 W of beam), more than a 60 C outside passes to the guard"))


def pb2_and_pis(T_g, load, vented):
    """PB2 (Hammond 1554JGY, 160 x 90 x 60.5 mm polycarbonate, IP66): sealed as drawn, or vented by a 40 mm fan (Noctua NF-A4x10 24V:
    8.9 m3/h free air, 19 Pa; ~5 m3/h through its Ø38 hole and a filtered vent, estimate). SoC: Geekworm's P573 test (passive aluminium case, 4-core stress for 20 min) rose 35 K over a 26.9 C
    ambient; the Active Cooler is taken as the same at full load (estimate), half that at the Pi's typical camera-and-supervisor load"""
    i = 0 if load == "typical" else 1
    P_box = (8.0, 12.0)[i]
    A_box = 2 * (0.16 * 0.09 + 0.16 * 0.0605 + 0.09 * 0.0605)
    Tm = T_g + 10
    U = 1 / (1 / (4.0 + h_rad(0.9, Tm)) + 0.003 / 0.2 + 1 / (4.0 + h_rad(0.9, Tm)))
    if vented:
        q = 5.0
        T_box = T_g + P_box / (U * A_box + RHO_AIR * CP_AIR * q / 3600)
    else:
        T_box = T_g + P_box / (U * A_box)
    rise_full, rise_typ = 35.0, 17.5
    soc_pb2 = T_box + (rise_typ if load == "typical" else rise_full)
    soc_pi2 = T_g + (rise_typ if load == "typical" else rise_full)
    return dict(pb2_box_air_c=round(T_box, 1), pb2_vented=vented, pb2_UA_sealed=round(U * A_box, 3),
                pi5_rating_c=[0, 70], soc_throttle_c=80, pb2_soc_c=round(soc_pb2, 1), pi2_case_air_c=round(T_g, 1), pi2_soc_c=round(soc_pi2, 1),
                pb2_box_ok=bool(T_box <= 70), pb2_soc_ok=bool(soc_pb2 < 80), pi2_soc_ok=bool(soc_pi2 < 80))


def trap_results():
    L = MC.LOUVRE
    K, por, kd = trap_K()
    out = dict(geometry=dict(L), flow=kd, cases=[])
    # reflectances at 1064-1070 nm: Thorlabs BKF12 black foil 5.5 % (Thorlabs' graph, 8 deg AOI); black hard ('Duranodic') anodise
    # 0.11-0.20 diffuse (NASA TP-3595, 1995, Fig. 3, two integrating spheres); dyed black anodise ~0.29 above 700 nm (Anoplate's
    # chart); Thorlabs' black flocked paper 0.65-0.67 shows how bright a visibly black surface can be at 1 um. Anodise keeps some
    # specular reflection from the rolled sheet under it: 30 % of what it reflects is taken as specular
    for label, rho, s in [("Thorlabs BKF12 foil lining", 0.055, 0.0), ("black hard anodise, NASA TP-3595 (low reading)", 0.12, 0.3),
                          ("black hard anodise, NASA TP-3595 (high reading)", 0.20, 0.3), ("dyed black anodise, Anoplate chart", 0.29, 0.3),
                          ("rho 0.40", 0.40, 0.3), ("rho 0.50", 0.50, 0.3), ("black flocked paper, Thorlabs", 0.66, 0.0)]:
        rd = trap_mc.trace(L["D"], L["A"], L["n"], L["p"], rho, s, 120_000, "diffuse", seed=11)
        worst = None
        for th in range(-85, 86, 5):
            rc = trap_mc.trace(L["D"], L["A"], L["n"], L["p"], rho, s, 30_000, "collimated", th, seed=200 + th)
            if worst is None or rc["OD"] < worst[1]:
                worst = (th, rc["OD"])
        out["cases"].append(dict(surface=label, rho=rho, specular_fraction=s, OD_diffuse=round(rd["OD"], 2), OD_collimated_worst=round(worst[1], 2),
                                 worst_angle_deg=worst[0], min_bounces=rd["min_hits_through"], back_to_guard=round(rd["back"], 3)))
    # seed spread on the cited case
    sp = [trap_mc.trace(L["D"], L["A"], L["n"], L["p"], 0.055, 0.0, 60_000, "diffuse", seed=s)["OD"] for s in (21, 22, 23)]
    out["seed_spread_OD_BKF12"] = [round(x, 2) for x in sp]
    out["required_OD"] = dict(class1_500W=5.4, margin=7.0, basis="safety.md §4.2: guard window or filter OD for Class 1 behind it, "
                                                                     "direct 500 W; OD 7 passes 50 uW")
    return out


def write_md(r):
    L = []
    op, hd = r["operating_point"], r["hood"]
    L.append("# Cooling: guard air, device temperatures and light traps (generated by cooling.py)\n")
    L.append(f"Shuttle air (tray_budget.json): " + "; ".join(f"{k} {v['T_s']} °C ({v['what']})" for k, v in r["cases"].items()) + f"; room {r['room_c']} °C.\n")
    L.append(f"Exhaust: {op['n']} x {op['fan']} -> **{op['q_m3h']} m³/h at {op['dp_Pa']} Pa** (filter {op['dp_filter']}, inlet trap "
             f"{op['dp_inlet_trap']}, exhaust trap {op['dp_exhaust_trap']}, plenum and guards {op['dp_plenum_guards']} Pa). "
             f"Hood branch: {hd['q_m3h']} m³/h, {hd['v_along_camera_m_s']} m/s along the camera.\n")
    L.append("| Case | Configuration | Supply (°C) | Guard air (°C) | Devices + fans (W) | Chamber (W) | Bridge (°C) | Over its rating |")
    L.append("|---|---|---:|---:|---:|---:|---:|---|")
    for k, v in r["results"].items():
        bad = [d["device"].split(" (")[0] + f" {d['checked_c']}/{d['rating_c'][1]}" for d in v["devices"] if not d["ok"]]
        if not v["pis"]["pb2_soc_ok"]:
            bad.append(f"PB2 SoC {v['pis']['pb2_soc_c']}/80")
        if not v["pis"]["pb2_box_ok"]:
            bad.append(f"PB2 box {v['pis']['pb2_box_air_c']}/70")
        g = v["guard"]
        L.append(f"| {k.split('/')[0]} ({v['shuttle']['T_s']}) | {k.split('/')[1]} | {v['T_in'] if v['T_in'] is not None else '-'} | {g['T_g']} | "
                 f"{g['Q_devices_W']} | {g['Q_chamber_W']} | {v['bridge_c']} | {'; '.join(bad) if bad else 'none'} |")
    L.append("\nPB2 sealed (as drawn) / with its 40 mm fan, box air and SoC (°C): " + "; ".join(
        f"{k}: {v['pis']['pb2_sealed_box_air_c']} / {v['pis']['pb2_box_air_c']}, SoC {v['pis']['pb2_sealed_soc_c']} / {v['pis']['pb2_soc_c']}"
        for k, v in r["results"].items() if not k.endswith("as_drawn")) + "\n")
    L.append("\n## Devices\n")
    for k, v in r["results"].items():
        L.append(f"**{k}**: " + "; ".join(f"{d['device'].split(' (')[0]} air {d['air_c']} / case {d['case_c']} (≤ {d['rating_c'][1]})"
                                          for d in v["devices"]) + f"; PB2 box {v['pis']['pb2_box_air_c']}, SoC {v['pis']['pb2_soc_c']}; "
                 f"LP Pi SoC {v['pis']['pi2_soc_c']}\n")
    L.append("\n## Light traps (1070 nm)\n")
    t = r["trap"]
    L.append(f"Chevron: {t['geometry']}; flow {t['flow']}. Required OD {t['required_OD']['class1_500W']} ({t['required_OD']['basis']}).\n")
    L.append("| Surface | rho | specular share | OD, diffuse light | OD, worst collimated beam (angle) | fewest bounces through |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for c in t["cases"]:
        L.append(f"| {c['surface']} | {c['rho']} | {c['specular_fraction']} | {c['OD_diffuse']} | {c['OD_collimated_worst']} ({c['worst_angle_deg']}°) | {c['min_bounces']} |")
    L.append(f"\nSeed spread, BKF12 diffuse: {t['seed_spread_OD_BKF12']}.\n")
    (OUT / "cooling.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    r = run()
    json.dump(r, open(OUT / "cooling.json", "w"), indent=1, default=float)
    write_md(r)
    print((OUT / "cooling.md").read_text())
