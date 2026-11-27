"""Fast-track alternatives for the desktop LPBF (2026-11-26): sizing, cost and schedule.

Sterling asked on 2026-11-26 (PR 266) for alternative designs that simplify the process and give a working
machine in about 3-6 weeks from start to finish. This script backs the numbers in README.md:

1. Sizing for the recommended fast-track machine (FT-1): argon purge and use, the heat budget of the heated
   well, the box's temperature rise, spot size and depth of focus for the used optics, powder per build.
2. Cost of each alternative from parts.csv (low and high, and how much needs a purchase order).
3. A forward-pass schedule for each alternative (working days, low and high), its milestones, and a Gantt chart.

    python desktop-lpbf/fast-track/fast_track.py          # writes out/*.csv, out/summary.md, img/*.png

Every input is a named constant with its source or the word "estimate". Nothing here is measured.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
IMG = HERE / "img"

# --------------------------------------------------------------------------------------------------
# 1. Sizing
# --------------------------------------------------------------------------------------------------
IN = 0.0254
AIR_O2_PPM = 209_000

# Box: a 16 x 12 x 8 in 304 stainless NEMA 4X enclosure (catalogue size; internal ~ outside for a 14 ga box).
BOX_IN = (16, 12, 8)
BOX_L = BOX_IN[0] * BOX_IN[1] * BOX_IN[2] * IN**3 * 1000          # litres
INTERNALS_L = 1.7                                                   # deck, well, plate, stage, hopper: measured in the CAD model (cad/ft_checks.py, FT-1)
GAS_L = BOX_L - INTERNALS_L
BOX_AREA_M2 = 2 * (BOX_IN[0] * BOX_IN[1] + BOX_IN[0] * BOX_IN[2] + BOX_IN[1] * BOX_IN[2]) * IN**2

# Purging: perfect mixing gives C = C0 exp(-V_purged / V). Real boxes with dead zones and porous powder take
# longer; the factor below is a placeholder until the O2 log of the first purge (estimate).
MIXING_PENALTY = (2.0, 5.0)
PURGE_LPM = 20.0                       # argon during the purge (estimate; the 78595A5 regulator reads to 70 scfh = 33 L/min)
TARGETS_PPM = (1000, 500, 100)

# Cross-flow over the plate, once-through from the cylinder (no blower): slot nozzle.
NOZZLE_W_MM, NOZZLE_H_MM, NOZZLE_V = 45.0, 4.0, 2.5   # m/s at the slot (gas-flow.md's target is 2.5 m/s over the plate)
CYLINDER_M3 = 9.5                                      # size-300 cylinder of argon (route-catalogue-chambers.csv)
ARGON_USD_PER_M3 = (11.0, 32.0)                        # estimate (route-catalogue-chambers.csv, unsourced range)

# Build: one Ø40 mm plate, 30 µm layers, AlSi10Mg at 50 % bed packing, 1.8x dose (budgets.py's factors).
PLATE_D_MM = 40.0
LAYER_UM = 30.0
BUILD_H_MM = (10.0, 15.0)
RHO_ALSI10MG = 2.67     # g/cm3
PACKING = 0.50
DOSE_FACTOR = 1.8
SCAN_FILL = 0.30        # fraction of the plate scanned per layer (a few coupons), estimate
HATCH_MM = 0.10
SCAN_V_MM_S = 1000.0
SPREAD_S = (8.0, 15.0)  # dose + spread + return per layer (estimate; Heriot-Watt found spreading dominated)

# Heat: the plate and the well block are both heated to 200 °C, so their clearance doesn't change (same alloy,
# same temperature). They sit on ceramic standoffs on the deck. Lumped losses (estimate): convection h and
# radiation (emissivity of oxidised Al / powder) from the exposed surfaces, plus conduction through the standoffs.
T_HOT, T_AMB = 200.0, 25.0
H_CONV = 8.0            # W/m2K, natural convection in argon (estimate)
EMISSIVITY = 0.3        # oxidised 6061 and powder (estimate)
SIGMA = 5.670e-8
WELL_BLOCK_MM = (80.0, 80.0, 40.0)        # 6061 block with the Ø40 bore
STANDOFF = dict(n=4 + 3, d_mm=6.35, L_mm=12.7, k=1.46)  # Macor (k 1.46 W/mK), 4 under the block, 3 under the plate
HEATERS_W = 4 * 50.0                      # 4 x McMaster 3714N36 (24 V, 50 W): 2 in the plate, 2 in the block
DECK_T_MM = 10.0                          # 6061 deck plate on the box floor
BED_Z_MM = DECK_T_MM + STANDOFF["L_mm"] + WELL_BLOCK_MM[2]   # powder plane = top of the well block
WINDOW_ABOVE_BED_MM = BOX_IN[2] * IN * 1000 - BED_Z_MM      # window in the lid (the box's door)
# The box sheds the heat through its walls; with a fan on the outside the wall coefficient rises (estimates).
H_BOX_STILL, H_BOX_FAN = 6.0, 20.0        # W/m2K overall, inside-to-outside, per box area
ABSORPTIVITY = (0.3, 0.6)                 # share of the beam absorbed by Al powder in LPBF, conduction to keyhole (estimate)
STAGE_MAX_C = 50.0                        # Zaber X-LSQ075B and X-VSR20A operating range 0-50 C (datasheets, read 2026-11-26)

# Optics: used IPG YLR-400-SM (M2 <= 1.1, 1.07 µm) with IPG's standard collimators, through a used
# hurrySCAN 25 (25 mm aperture) and a LINOS f = 254 mm F-Theta-Ronar.
M2, LAMBDA_UM, F_MM = 1.1, 1.07, 254.0
BEAMS_MM = (5.0, 7.5)                     # IPG's standard collimated beam diameters (IPG quote of 2026-11-18)
P_LASER_W = 400.0


def purge():
    rows = []
    vol_changes = {t: math.log(AIR_O2_PPM / t) for t in TARGETS_PPM}
    for t, n in vol_changes.items():
        ideal_min = n * GAS_L / PURGE_LPM
        rows.append(dict(target_ppm=t, volume_changes=round(n, 2), ideal_min=round(ideal_min, 1),
                         real_min_low=round(ideal_min * MIXING_PENALTY[0], 1),
                         real_min_high=round(ideal_min * MIXING_PENALTY[1], 1),
                         argon_L_low=round(n * GAS_L * MIXING_PENALTY[0]), argon_L_high=round(n * GAS_L * MIXING_PENALTY[1])))
    return rows


def build_time_and_gas():
    area_mm2 = math.pi / 4 * PLATE_D_MM**2
    scan_s = SCAN_FILL * area_mm2 / HATCH_MM / SCAN_V_MM_S * 1.3   # +30 % for jumps and delays (estimate)
    out = []
    for h in BUILD_H_MM:
        layers = h * 1000 / LAYER_UM
        t_h = [layers * (scan_s + s) / 3600 for s in SPREAD_S]
        nozzle_lpm = NOZZLE_W_MM * NOZZLE_H_MM * 1e-6 * NOZZLE_V * 60_000
        purge_L = purge()[-1]["argon_L_high"]
        gas_m3 = [(nozzle_lpm * 60 * t + purge_L) / 1000 for t in t_h]
        powder_g = area_mm2 * h * 1e-3 * RHO_ALSI10MG * PACKING * DOSE_FACTOR
        out.append(dict(build_mm=h, layers=round(layers), scan_s_per_layer=round(scan_s, 1),
                        hours_low=round(t_h[0], 2), hours_high=round(t_h[1], 2), nozzle_L_min=round(nozzle_lpm, 1),
                        argon_m3_low=round(gas_m3[0], 2), argon_m3_high=round(gas_m3[1], 2),
                        builds_per_cylinder=f"{CYLINDER_M3 / gas_m3[1]:.1f}-{CYLINDER_M3 / gas_m3[0]:.1f}",
                        argon_usd=f"{gas_m3[0] * ARGON_USD_PER_M3[0]:.0f}-{gas_m3[1] * ARGON_USD_PER_M3[1]:.0f}",
                        powder_g=round(powder_g)))
    return out


def heat():
    dT = T_HOT - T_AMB
    a, b, c = (x / 1000 for x in WELL_BLOCK_MM)
    block_area = 2 * (a * b + a * c + b * c) - 2 * math.pi / 4 * (PLATE_D_MM / 1000) ** 2
    top_area = math.pi / 4 * (PLATE_D_MM / 1000) ** 2           # powder or part surface on the plate
    h_rad = EMISSIVITY * SIGMA * ((T_HOT + 273.15) ** 4 - (T_AMB + 273.15) ** 4) / dT
    q_surf = (H_CONV + h_rad) * (block_area + top_area) * dT
    s = STANDOFF
    g_standoff = s["n"] * s["k"] * math.pi / 4 * (s["d_mm"] / 1000) ** 2 / (s["L_mm"] / 1000)
    q_cond = g_standoff * dT
    q = q_surf + q_cond
    # The laser adds its absorbed power, averaged over a layer (scan time over scan + spread time).
    area_mm2 = math.pi / 4 * PLATE_D_MM**2
    scan_s = SCAN_FILL * area_mm2 / HATCH_MM / SCAN_V_MM_S * 1.3
    duty = scan_s / (scan_s + SPREAD_S[0])
    laser_w = [P_LASER_W * a * duty for a in ABSORPTIVITY]
    total = [q + w for w in laser_w]
    rise = {name: [t / (hb * BOX_AREA_M2) for t in total] for name, hb in (("still", H_BOX_STILL), ("fan", H_BOX_FAN))}
    return dict(surface_W=round(q_surf, 1), standoffs_W=round(q_cond, 1), heater_load_W=round(q, 1), heaters_W=HEATERS_W,
                margin=round(HEATERS_W / q, 2), laser_avg_W=f"{laser_w[0]:.0f}-{laser_w[1]:.0f}",
                box_area_m2=round(BOX_AREA_M2, 3),
                box_rise_still_K=f"{rise['still'][0]:.0f}-{rise['still'][1]:.0f}",
                box_rise_fan_K=f"{rise['fan'][0]:.0f}-{rise['fan'][1]:.0f}",
                box_air_C_still_vs_stage_max=f"{T_AMB + rise['still'][1]:.0f} vs {STAGE_MAX_C:.0f}",
                box_air_C_fan=f"{T_AMB + rise['fan'][1]:.0f}")


def optics():
    rows = []
    for d in BEAMS_MM:
        spot_um = 4 * M2 * LAMBDA_UM * F_MM / (math.pi * d)
        w0_m = spot_um / 2 * 1e-6
        zr_mm = math.pi * w0_m**2 / (M2 * LAMBDA_UM * 1e-6) * 1000
        beam_at_window_mm = d * WINDOW_ABOVE_BED_MM / F_MM
        irr_kw_cm2 = P_LASER_W / (math.pi / 4 * (beam_at_window_mm / 10) ** 2) / 1000
        grow_5mm = math.sqrt(1 + (5 / zr_mm) ** 2)
        rows.append(dict(beam_mm=d, spot_um=round(spot_um), rayleigh_mm=round(zr_mm, 2),
                         spot_growth_at_5mm_defocus=round(grow_5mm, 2), beam_at_window_mm=round(beam_at_window_mm, 2),
                         window_kW_per_cm2_at_400W=round(irr_kw_cm2, 1)))
    return rows


# --------------------------------------------------------------------------------------------------
# 2. Cost from parts.csv
# --------------------------------------------------------------------------------------------------
OPTIONS = ("FT0", "FT1", "FT1V")
PO_LIMIT = 3500.0   # BYU: a PO for a single-vendor order of $3,500 or more (capstone.byu.edu, read 2026-11-25)


def costs():
    rows = list(csv.DictReader(open(HERE / "parts.csv")))
    res = {}
    for opt in OPTIONS:
        lo = hi = 0.0
        by_vendor: dict[str, float] = {}
        groups: dict[str, list[float]] = {}
        for r in rows:
            q = float(r[opt] or 0)
            if not q:
                continue
            ul, uh = float(r["unit_low"]), float(r["unit_high"])
            lo += q * ul
            hi += q * uh
            g = groups.setdefault(r["group"], [0.0, 0.0])
            g[0] += q * ul
            g[1] += q * uh
            if r["part_number"] != "(labour)":          # internal shop time is not a purchase
                by_vendor[r["vendor"]] = by_vendor.get(r["vendor"], 0.0) + q * uh
        po = {v: round(t) for v, t in by_vendor.items() if t >= PO_LIMIT}
        res[opt] = dict(low=round(lo), high=round(hi), groups={k: (round(a), round(b)) for k, (a, b) in groups.items()},
                        po_vendors=po)
    return rows, res


# --------------------------------------------------------------------------------------------------
# 3. Schedule: working days from the decision (day 0), low and high. Each task lists what it waits for.
#    Durations are vendor statements read on 2026-11-25/26 converted to working days, or estimates (marked).
# --------------------------------------------------------------------------------------------------
# Shop time per state from fab/ (FreeCAD CAM + PR 266's allowances; fab/out/hours.json, round 2). The early estimate
# uses the low hours (robot-shop.md's smaller allowances) at SHOP_H_PER_DAY[0]; the late one the full hours at
# SHOP_H_PER_DAY[1]. Shop hours a working day are an estimate: one machinist full time plus a student (8 h/day) or one
# person at most of a day (5 h/day). Parts are made in state order, so S1's parts are ready first.
SHOP_H_PER_DAY = (8.0, 5.0)


def shop_days(state):
    try:
        h = json.load(open(HERE / "fab" / "out" / "hours.json"))["by_state"][state]
        lo, hi = float(h["low"]), float(h["h"])
    except Exception:                       # fab/ not run: round 1's estimates
        lo, hi = dict(S1=3, S2=3, **{"FT-0": 6, "FT-1": 12, "FT-1V": 6}).get(state, 5), 15
    return (round(lo / SHOP_H_PER_DAY[0], 1), round(hi / SHOP_H_PER_DAY[1], 1)), (lo, hi)


def shop_tasks(upto):
    order = ["S1", "S2", "FT-0", "FT-1", "FT-1V"]
    out, prev = {}, ["McMaster stock and hardware"]
    for st in order[: order.index(upto) + 1]:
        d, (lo, hi) = shop_days(st)
        name = f"{st} parts made"
        out[name] = (d, list(prev), f"fab/out/hours.json: {lo:.1f}-{hi:.1f} shop h at {SHOP_H_PER_DAY[0]:g}-{SHOP_H_PER_DAY[1]:g} h a working day (estimate)")
        prev = [name]
    return out


COMMON = {
    # procurement (PCard orders go out on day 0)
    "used optics chain arrives": ((3, 8), [], "eBay windows to 84602 read 2026-11-27 (Nov 30-Dec 3) and LTL freight for the laser (estimate)"),
    "McMaster stock and hardware": ((1, 2), [], "McMaster: most orders arrive same or next day"),
    "safety parts and eyewear": ((2, 5), [], "Digi-Key in stock (D4NS-2CF 360 in stock, 2026-11-27) / Thorlabs LG1 'Available: Today'"),
    "O2 analyzers arrive": ((4, 10), [], "eBay window Dec 1-7 (Alpha Omega Series 3000, read 2026-11-27); Kele OX-6 lead time not read (estimate)"),
    "argon cylinder and regulator": ((2, 5), [], "estimate (gas supplier delivery; McMaster regulator next day)"),
    "RTC4 card + PC and software": ((3, 7), [], "eBay 366737163447 'Estimated between Wed, Dec 2 and Tue, Dec 8' (read 2026-11-27); lab PC with a PCIe slot"),
    "208/240 V circuit for the laser": ((3, 15), [], "estimate: a Physical Facilities work order, unless the room already has a 208/240 V outlet (check on day 0)"),
    # approvals, started on day 0 (unknown durations: estimates)
    "LSO registration and SOP": ((5, 15), [], "estimate: BYU's laser-safety pages need a login; start on day 0"),
    "EHS review (Al powder)": ((5, 15), [], "estimate: dust hazard analysis scope, start on day 0"),
}
BENCH = ((2, 4), ["used optics chain arrives", "RTC4 card + PC and software", "LSO registration and SOP", "safety parts and eyewear",
                  "S1 parts made", "208/240 V circuit for the laser"], "estimate")

ALTERNATIVES = {
    "FT-0 single-track bench": {
        **COMMON, **shop_tasks("FT-0"),
        "enclosure arrives": ((3, 8), [], "estimate: distributor stock (Saginaw SCE-16EL1208SSLP, $694.24, stock not stated), ground"),
        "bench check of laser + scan head": BENCH,
        "assemble box, heater, gas": ((1, 2), ["FT-0 parts made", "enclosure arrives"], "estimate"),
        "purge and heat commissioning": ((1, 2), ["assemble box, heater, gas", "O2 analyzers arrive", "argon cylinder and regulator"], "estimate"),
        "FIRST TRACKS": ((1, 2), ["bench check of laser + scan head", "purge and heat commissioning", "EHS review (Al powder)"], "milestone"),
        "hand-spread single layers and pads": ((2, 4), ["FIRST TRACKS"], "estimate"),
    },
    "FT-1 purge-box LPBF (stages on one PO)": {
        **COMMON, **shop_tasks("FT-1"),
        "Zaber stages arrive (PO)": ((11, 20), [], "BYU PO 10-14 days (capstone.byu.edu) + Zaber 'Lead Time: 1-5 Days' + transit"),
        "enclosure arrives": ((3, 8), [], "estimate: distributor stock, ground"),
        "bench check of laser + scan head": BENCH,
        "assemble mechanism in the box": ((3, 5), ["FT-1 parts made", "Zaber stages arrive (PO)", "enclosure arrives"], "estimate"),
        "purge and heat commissioning": ((1, 3), ["assemble mechanism in the box", "O2 analyzers arrive", "argon cylinder and regulator"], "estimate"),
        "interlock commissioning": ((1, 2), ["assemble mechanism in the box", "safety parts and eyewear"], "estimate"),
        "FIRST TRACKS": ((1, 2), ["bench check of laser + scan head", "purge and heat commissioning", "interlock commissioning", "EHS review (Al powder)"], "milestone"),
        "powder layers: dose, spread, pads": ((3, 5), ["FIRST TRACKS"], "estimate"),
        "FIRST COUPONS": ((2, 5), ["powder layers: dose, spread, pads"], "milestone"),
    },
    "FT-1 purge-box LPBF (stages on PCards)": {
        **COMMON, **shop_tasks("FT-1"),
        "stages arrive (PCard)": ((3, 10), [], "Zaber X-LSM100B 'Lead Time: 1-5 Days' + transit; Thorlabs MTS50/M-Z8 + KDC101 'Available: Today'"),
        "enclosure arrives": ((3, 8), [], "estimate: distributor stock, ground"),
        "bench check of laser + scan head": BENCH,
        "assemble mechanism in the box": ((3, 5), ["FT-1 parts made", "stages arrive (PCard)", "enclosure arrives"], "estimate"),
        "purge and heat commissioning": ((1, 3), ["assemble mechanism in the box", "O2 analyzers arrive", "argon cylinder and regulator"], "estimate"),
        "interlock commissioning": ((1, 2), ["assemble mechanism in the box", "safety parts and eyewear"], "estimate"),
        "FIRST TRACKS": ((1, 2), ["bench check of laser + scan head", "purge and heat commissioning", "interlock commissioning", "EHS review (Al powder)"], "milestone"),
        "powder layers: dose, spread, pads": ((3, 5), ["FIRST TRACKS"], "estimate"),
        "FIRST COUPONS": ((2, 5), ["powder layers: dose, spread, pads"], "milestone"),
    },
    "FT-1V same, in a stock vacuum chamber": {
        **COMMON, **shop_tasks("FT-1V"),
        "Zaber stages arrive (PO)": ((11, 20), [], "BYU PO + Zaber 1-5 days + transit"),
        "chamber frame and plates arrive (PO)": ((11, 16), [], "Ideal Vacuum P107540 frame and P108171 plates 'Available now' (2026-11-25) + BYU PO + LTL"),
        "pump, KF parts, Pirani": ((2, 7), [], "McMaster 4396K21 next day, or used IDP-3 (eBay window Dec 2-8, read 2026-11-27)"),
        "bench check of laser + scan head": BENCH,
        "assemble mechanism in the chamber": ((3, 6), ["FT-1V parts made", "Zaber stages arrive (PO)", "chamber frame and plates arrive (PO)"], "estimate"),
        "leak check, pump-purge, heat": ((2, 4), ["assemble mechanism in the chamber", "pump, KF parts, Pirani", "O2 analyzers arrive", "argon cylinder and regulator"], "estimate"),
        "interlock commissioning": ((1, 2), ["assemble mechanism in the chamber", "safety parts and eyewear"], "estimate"),
        "FIRST TRACKS": ((1, 2), ["bench check of laser + scan head", "leak check, pump-purge, heat", "interlock commissioning", "EHS review (Al powder)"], "milestone"),
        "powder layers: dose, spread, pads": ((3, 5), ["FIRST TRACKS"], "estimate"),
        "FIRST COUPONS": ((2, 5), ["powder layers: dose, spread, pads"], "milestone"),
    },
}


def forward(tasks):
    done: dict[str, tuple[float, float, float, float]] = {}

    def finish(name):
        if name in done:
            return done[name]
        (dl, dh), deps, _ = tasks[name]
        sl = max((finish(d)[2] for d in deps), default=0)
        sh = max((finish(d)[3] for d in deps), default=0)
        done[name] = (sl, sh, sl + dl, sh + dh)
        return done[name]

    for n in tasks:
        finish(n)
    return done


def schedule():
    out = {}
    for alt, tasks in ALTERNATIVES.items():
        out[alt] = forward(tasks)
    return out


def gantt(sched):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    alts = list(sched)
    fig, axes = plt.subplots(len(alts), 1, figsize=(11.5, 2.6 + 0.36 * sum(len(sched[a]) for a in alts)),
                             gridspec_kw=dict(height_ratios=[len(sched[a]) for a in alts]))
    for ax, alt in zip(axes, alts):
        tasks = ALTERNATIVES[alt]
        names = sorted(sched[alt], key=lambda n: (sched[alt][n][2], sched[alt][n][3]))
        for i, n in enumerate(names):
            sl, sh, fl, fh = sched[alt][n]
            milestone = n.isupper()
            approval = n in ("LSO registration and SOP", "EHS review (Al powder)")
            color = "#b2182b" if milestone else ("#999999" if approval else "#2166ac")
            ax.barh(i, fl - sl, left=sl, color=color, alpha=0.9, height=0.55)
            ax.barh(i, fh - fl, left=fl, color=color, alpha=0.30, height=0.55)
            if milestone:
                ax.text(fh + 0.4, i, f"{fl / 5:.1f}-{fh / 5:.1f} wk", va="center", fontsize=8, color=color, weight="bold")
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=7.5)
        ax.invert_yaxis()
        ax.set_xlim(0, 60)
        ax.set_xticks(range(0, 61, 5))
        ax.set_xticklabels([f"{d // 5}" for d in range(0, 61, 5)], fontsize=8)
        ax.axvspan(15, 30, color="#4daf4a", alpha=0.06)
        ax.set_title(alt, fontsize=9.5, loc="left")
        ax.grid(axis="x", color="#dddddd", lw=0.6)
        ax.set_axisbelow(True)
    axes[-1].set_xlabel("weeks from the decision (5 working days a week); dark = earliest, light = up to the late estimate; "
                        "green band = 3-6 weeks", fontsize=8)
    fig.suptitle("Fast-track alternatives: forward-pass schedule (estimates; approvals grey, milestones red)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    fig.savefig(IMG / "gantt.png", dpi=130)
    plt.close(fig)


def layout():
    """To-scale side section of FT-1 (x along the box's 16 in axis, z up, mm). A sketch for agreeing the layout,
    not a model: sizes are from the parts' listings where known and marked estimates otherwise."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon, Circle

    L, H = BOX_IN[0] * 25.4, BOX_IN[2] * 25.4        # 406 x 203 mm inside
    wall = 2.0
    deck_t = DECK_T_MM
    standoff = STANDOFF["L_mm"]
    block_w, block_h = WELL_BLOCK_MM[0], WELL_BLOCK_MM[2]
    cx = L / 2
    block_z0 = deck_t + standoff
    bed_z = BED_Z_MM
    plate_stack = 18.0                                    # 12 mm heater plate + 6 mm substrate disc
    lens_wd = 300.0                                       # LINOS f = 254 mm working distance (estimate; check the lens)
    lens_z0 = bed_z + lens_wd
    win_z = H
    fig, ax = plt.subplots(figsize=(9.5, 8.6))

    def box(x, z, w, h, fc, ec="k", lw=0.8, ls="-", a=1.0, label=None, fs=7, lx=None, lz=None, ha="center"):
        ax.add_patch(Rectangle((x, z), w, h, fc=fc, ec=ec, lw=lw, ls=ls, alpha=a))
        if label:
            ax.text(lx if lx is not None else x + w / 2, lz if lz is not None else z + h / 2, label, fontsize=fs,
                    ha=ha, va="center")

    # stainless box (on its back: the hinged door is the lid)
    box(-wall, -wall, L + 2 * wall, wall, "#9aa5b1")
    box(-wall, 0, wall, H, "#9aa5b1")
    box(L, 0, wall, H, "#9aa5b1")
    box(-wall, H, cx - 32 + wall, wall, "#9aa5b1")
    box(cx + 32, H, L - cx - 32 + wall, wall, "#9aa5b1")
    ax.text(L - 4, H - 50, "16 x 12 x 8 in 304 box,\nlid = its hinged door", fontsize=7, ha="right")
    # window and ring clamp, cover slide
    box(cx - 25.4, H - 4.8, 50.8, 9.53, "#cfe8ff", label=None)
    box(cx - 38, H + wall, 76, 8, "#c9c9c9", label="window ring", fs=6.5)
    box(cx - 28, H - 14, 56, 1.5, "#e6f3ff")
    ax.text(cx + 40, H - 14, "cover slide", fontsize=6.5, va="center")
    # deck, standoffs, well block, plate
    box(8, 0, L - 16, deck_t, "#c7ccd1", label="deck plate (6061, 10 mm)", fs=6.5, lx=70)
    for dx in (-30, 30):
        box(cx + dx - 3.2, deck_t, 6.4, standoff, "#f2e6c9")
    box(cx - block_w / 2, block_z0, (block_w - PLATE_D_MM) / 2, block_h, "#e8a87c")
    box(cx + PLATE_D_MM / 2, block_z0, (block_w - PLATE_D_MM) / 2, block_h, "#e8a87c")
    ax.text(cx - block_w / 2 - 3, block_z0 + block_h / 2, "well block\n200 °C", fontsize=6.5, ha="right", va="center")
    box(cx - PLATE_D_MM / 2 + 0.2, bed_z - plate_stack, PLATE_D_MM - 0.4, 6, "#d0d0d0")
    box(cx - PLATE_D_MM / 2 + 0.2, bed_z - plate_stack - 12 + 6, PLATE_D_MM - 0.4, 12, "#e8a87c")
    ax.text(cx + block_w / 2 + 3, bed_z - 4, "Ø40 plate + substrate, 200 °C", fontsize=6.5, va="center")
    for dx in (-12, 12):
        box(cx + dx - 3.2, bed_z - plate_stack - 12 - standoff + 6, 6.4, standoff, "#f2e6c9")
    # rod, gland, stage below
    rod_top = bed_z - plate_stack - 12 - standoff + 6
    box(cx - 5, -120, 10, rod_top + 120, "#b0b7bf")
    box(cx - 22, -wall - 10, 44, 10, "#c7ccd1", label="rod O-ring gland", fs=6.5, lx=cx + 26, ha="left")
    box(cx - 40, -205, 80, 70, "#5b7fb5", label="Zaber X-VSR20A\n(20 mm, outside)", fs=6.5)
    box(cx - 30, -135, 60, 15, "#7f9cc9")
    # recoater stage (behind the section plane) and hopper-blade
    box(30, deck_t + 2, 330, 26, "#5b7fb5", ls="--", a=0.35)
    ax.annotate("Zaber X-LSQ075B recoater stage\n(behind the well, under a shield;\nits arm reaches over the bed)", xy=(80, deck_t + 20),
                xytext=(-185, -70), fontsize=6.5, arrowprops=dict(arrowstyle="->", lw=0.6))
    hx = cx - PLATE_D_MM / 2 - 38
    ax.add_patch(Polygon([(hx, bed_z + 45), (hx + 30, bed_z + 45), (hx + 18, bed_z + 6), (hx + 12, bed_z + 6)],
                         closed=True, fc="#d9d9d9", ec="k", lw=0.8))
    box(hx + 21, bed_z, 3, 7, "#333333")
    ax.text(hx + 15, bed_z + 52, "hopper + silicone-cord blade\n(moves with the stage)", fontsize=6.5, ha="center")
    ax.annotate("", xy=(hx + 70, bed_z + 30), xytext=(hx + 35, bed_z + 30), arrowprops=dict(arrowstyle="->", lw=0.8))
    # overflow cup
    box(cx + block_w / 2 + 6, deck_t, 30, 45, "#eeeeee")
    ax.annotate("overflow cup", xy=(cx + block_w / 2 + 21, deck_t + 30), xytext=(cx + 95, 25), fontsize=6.5,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    # gas
    box(0, bed_z + 2, 40, 5, "#9ecae1")
    ax.annotate("argon slot nozzle\n45 x 4 mm, 2.5 m/s", xy=(40, bed_z + 4.5), xytext=(12, bed_z + 105), fontsize=6.5,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("", xy=(cx + 60, bed_z + 6), xytext=(45, bed_z + 6), arrowprops=dict(arrowstyle="->", color="#3182bd", lw=1.2))
    box(L - 2, bed_z - 6, 16, 14, "#c9c9c9")
    ax.text(L + 18, bed_z + 40, "exhaust -> HEPA ->\ncheck valve (+5-10 mbar)\n-> building exhaust", fontsize=6.5, va="center")
    # fan on the box
    ax.add_patch(Circle((L + 30, -40), 24, fc="#eeeeee", ec="k", lw=0.8))
    ax.text(L + 30, -40, "fan on\nthe box", fontsize=6, ha="center", va="center")
    # optics: lens, head, collimator, beam tube, beam cone
    box(cx - 60, lens_z0, 120, 62, "#7d7d7d", label="LINOS f = 254 mm", fs=6.5)
    box(cx - 70, lens_z0 + 62, 140, 120, "#4d4d4d", label="", fs=6.5)
    ax.text(cx, lens_z0 + 122, "hurrySCAN 25", fontsize=7, ha="center", va="center", color="white")
    box(cx + 70, lens_z0 + 110, 90, 26, "#999999", label="collimator <- fibre", fs=6.5)
    box(cx - 30, H + wall + 8, 60, lens_z0 - H - wall - 8, "#eeeeee", a=0.6)
    ax.text(cx + 34, (H + lens_z0) / 2, "beam tube\n(interlocked)", fontsize=6.5, va="center")
    ax.add_patch(Polygon([(cx - 10, lens_z0), (cx + 10, lens_z0), (cx + PLATE_D_MM / 2, bed_z), (cx - PLATE_D_MM / 2, bed_z)],
                         closed=True, fc="#ff6b6b", ec="none", alpha=0.35))
    # T-slot frame
    for x in (-60, L + 60 - 20):
        box(x, -wall, 20, lens_z0 + 200, "#b9c0c7", a=0.6)
    box(-60, lens_z0 + 182, L + 140, 20, "#b9c0c7", a=0.6, label="T-slot frame (head height set by the lens working distance)", fs=6.5)
    # dimensions
    ax.annotate("", xy=(-90, bed_z), xytext=(-90, lens_z0), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(-95, (bed_z + lens_z0) / 2, f"~{lens_wd:.0f} mm\nworking\ndistance\n(estimate)", fontsize=6.5, ha="right", va="center")
    ax.annotate("", xy=(-30, bed_z), xytext=(-30, H), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text(-34, (bed_z + H) / 2, f"{H - bed_z:.0f} mm\nbed to window", fontsize=6.5, ha="right", va="center")
    ax.plot([-60, L + 60], [bed_z, bed_z], color="#999999", lw=0.5, ls=":")
    ax.set_xlim(-190, L + 150)
    ax.set_ylim(-215, lens_z0 + 215)
    ax.set_aspect("equal")
    ax.set_xlabel("mm")
    ax.set_title("FT-1 purge-box LPBF: side section, to scale (sketch, not a model)", fontsize=10)
    fig.tight_layout()
    fig.savefig(IMG / "ft1-section.png", dpi=140)
    plt.close(fig)
    return dict(bed_z=bed_z, bed_to_window=H - bed_z, lens_z0=lens_z0, overall_height_mm=lens_z0 + 200 + 205)


def md_table(rows, cols):
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows)


def main():
    OUT.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    lines = ["# fast_track.py output", ""]
    p = purge()
    lines += [f"Box {BOX_IN[0]} x {BOX_IN[1]} x {BOX_IN[2]} in: {BOX_L:.1f} L, gas volume ~{GAS_L:.1f} L; purge at {PURGE_LPM:.0f} L/min.", "",
              md_table(p, list(p[0]))]
    b = build_time_and_gas()
    lines += ["Build time, argon and powder:", "", md_table(b, list(b[0]))]
    h = heat()
    lines += ["Heat budget at 200 °C (well block + plate on Macor standoffs):", "", md_table([h], list(h))]
    o = optics()
    lines += ["Optics (f = 254 mm, M2 1.1):", "", md_table(o, list(o[0]))]
    rows, c = costs()
    lines += ["Cost by alternative (parts.csv):", ""]
    for opt, v in c.items():
        m = v["groups"].get("Monitoring", (0, 0))
        lines.append(f"- **{opt}**: ${v['low']:,}-{v['high']:,} (without the monitoring group: ${v['low'] - m[0]:,}-{v['high'] - m[1]:,}); "
                     f"vendors at or over ${PO_LIMIT:,.0f} (PO): "
                     + (", ".join(f"{k} (${t:,})" for k, t in v["po_vendors"].items()) or "none"))
        for g, (a, bb) in v["groups"].items():
            lines.append(f"  - {g}: ${a:,}-{bb:,}")
    s = schedule()
    lines += ["", "Milestones (working days -> weeks):", ""]
    sched_rows = []
    for alt, d in s.items():
        for n, (sl, sh, fl, fh) in d.items():
            sched_rows.append(dict(alternative=alt, task=n, start_low_d=sl, start_high_d=sh, finish_low_d=fl, finish_high_d=fh,
                                   basis=ALTERNATIVES[alt][n][2]))
            if n.isupper():
                lines.append(f"- {alt}: {n} at {fl:.0f}-{fh:.0f} working days = {fl / 5:.1f}-{fh / 5:.1f} weeks")
    # sensitivity: shop hours a working day against FT-1's first coupons (stages on PCards)
    global SHOP_H_PER_DAY
    keep, alt = SHOP_H_PER_DAY, "FT-1 purge-box LPBF (stages on PCards)"
    lines += ["", f"Shop throughput against {alt}: FIRST COUPONS (early with the low hours, late with the full hours):", ""]
    for hpd in (5.0, 8.0, 12.0):
        SHOP_H_PER_DAY = (hpd, hpd)
        tasks = dict(ALTERNATIVES[alt])
        tasks.update(shop_tasks("FT-1"))
        fl, fh = forward(tasks)["FIRST COUPONS"][2:]
        lines.append(f"- {hpd:g} shop h a working day: {fl / 5:.1f}-{fh / 5:.1f} weeks")
    SHOP_H_PER_DAY = keep
    with open(OUT / "schedule.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(sched_rows[0]))
        w.writeheader()
        w.writerows(sched_rows)
    for name, data in (("purge", p), ("build", b), ("optics", o)):
        with open(OUT / f"{name}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    gantt(s)
    lay = layout()
    lines.append(f"\nLayout sketch: bed {lay['bed_z']:.0f} mm above the box floor, {lay['bed_to_window']:.0f} mm below the window; "
                 f"lens {lay['lens_z0']:.0f} mm above the floor; overall ~{lay['overall_height_mm']:.0f} mm with the stage below.")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
