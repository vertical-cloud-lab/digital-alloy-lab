"""Transient thermal FEA (CalculiX, axisymmetric): hot bronze shot lands in each cup. How hot do the seals,
the glass and the thermocouple spots get, and how fast?

    python analysis/thermal.py                 # every case in CASES (about 15 min on 4 cores)
    python analysis/thermal.py B_816 A_250     # selected cases

Model (sizes from ../params.py, the same numbers as the CAD):
- The machine's cone outlet flange and spigot, 40 mm of it, its top held at 25 C (the cone is water-cooled).
- The KF joint: the centring ring (with a 0.3 mm contact layer, h = 1000 W/m2K, on each face), the O-ring
  squashed to the ring's thickness, and the argon gap outboard of it. The clamp is left out, which is
  conservative: in the machine it also carries heat from the cup's flange to the cooled cone flange.
- The cup (stock, A, B or C), with its liner, puck and pan, and the argon gaps between them as thin regions
  whose conductivity includes radiation across the gap.
- The pile: the shot that reached the cup, as a packed bed (60 % dense) on the puck/pan/floor, starting at
  1050 C, 70 % liquid (C63000: solidus 1040, liquidus 1054 C); its remaining latent heat (164 kJ/kg) is
  released between 1050 and 950 C (spread over 100 K so that Newton converges). Effective conductivity 5 W/m K (2 and 20 in the sensitivity cases).
  Everything arrives at t = 0, which is the worst case for peaks (in a real pour it takes ~30-90 s).
- Outside: natural convection 8 W/m2K plus radiation (emissivity 0.35 steel, 0.9 glass) to 25 C.
- Inside: the pile's top radiates (emissivity 0.7). Pass 1 gives its radiated power P(t); pass 2 puts
  P(t) on the cavity walls in proportion to Monte-Carlo view factors from the pile top (first hit, all
  absorbed: conservative for the upper walls; whatever leaves through the cone outlet is lost).
  Wall-to-wall radiation and argon convection inside are not modelled.
Results: analysis/out/thermal/<case>/ (deck, temperatures vs time) and analysis/out/thermal_summary.{json,md},
plus plots in analysis/img/.
"""

import json
import math
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.tri as mtri  # noqa: E402
import numpy as np  # noqa: E402
from shapely.geometry import Point, Polygon  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cad"))
import axifea as F  # noqa: E402
import params as P  # noqa: E402

OUT = HERE / "out" / "thermal"
IMG = HERE / "img"
OUT.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)

T_AMB = 25.0
T_SHOT = 1050.0
PILE_FRAC = 0.60          # packed-bed solid fraction
EPS_PILE = 0.7
EPS_STEEL = 0.35
EPS_GLASS = 0.9
H_NAT = 8.0               # W/m2K outside
MESH_SCALE = 1.0          # linear triangles (CAX3): no overshoot at the hot/cold step, so finer
T_END = 3600.0
T_STEP1 = 20.0
TIME_POINTS = sorted(set([round(x, 3) for x in np.geomspace(0.5, T_END, 70)] + [5, 10, 30, 60, 120, 300, 600,
                                                                                  900, 1200, 1800, 2400, 3600]))
FIELD_TIMES = [10.0, 60.0, 300.0, 900.0, 1800.0, 3600.0]


# ------------------------------------------------------------------------------------------ materials
def steel_props():
    T = [20, 100, 200, 300, 400, 500, 600, 800, 1000, 1200]
    k = [14.6, 16.2, 17.6, 19.0, 20.4, 21.6, 22.8, 25.4, 28.0, 30.5]
    cp = [470, 500, 530, 550, 565, 580, 595, 625, 650, 670]
    return T, k, cp, 7950


def gap_k(delta_mm, eps=EPS_STEEL):
    """Effective conductivity of an argon gap of width delta, with radiation across it (W/m K)."""
    T = [20, 200, 400, 600, 800, 1000, 1200]
    out = []
    for t in T:
        Tk = t + 273.15
        k_ar = 0.0177 * (Tk / 300.0) ** 0.72
        k_rad = 4 * 5.67e-8 * Tk ** 3 * (delta_mm * 1e-3) / (2 / eps - 1)
        out.append(k_ar + k_rad)
    return T, out


def material_cards(names, pile_k=5.0, ring_contact_h=1000.0, puck_contact_h=500.0):
    """CalculiX *MATERIAL cards for every material name used."""
    s = []

    def add(name, T, k, cp, rho):
        s.append(f"*MATERIAL, NAME={name}\n*CONDUCTIVITY\n")
        s.extend(f"{kk:.5g}, {tt}\n" for kk, tt in zip(k, T))
        s.append(f"*DENSITY\n{rho * F.KG_M3:.5e}\n*SPECIFIC HEAT\n")
        s.extend(f"{cc * F.J_PER_KGK:.5e}, {tt}\n" for cc, tt in zip(cp, T))

    T, k, cp, rho = steel_props()
    for nm in ("S316L", "S304"):
        if nm in names:
            add(nm, T, k, cp, rho)
    if "CU" in names:
        add("CU", [20, 400, 800, 1000], [395, 370, 345, 335], [385, 410, 435, 450], 8940)
    if "PILE" in names:
        L_left = 0.71 * P.SHOT["L"]
        cp_mush = 480 + L_left / 100.0          # released between 1050 and 950 C (smoothed for Newton)
        add("PILE", [20, 500, 940, 950, 1050, 1060, 1200], [pile_k] * 7,
            [420, 460, 480, cp_mush, cp_mush, 530, 530], P.SHOT["rho"] * PILE_FRAC)
    if "FKM" in names:
        add("FKM", [20, 600], [0.20, 0.20], [1400, 1400], 1850)
    if "EPDM" in names:
        add("EPDM", [20, 600], [0.25, 0.25], [1800, 1800], 1150)
    if "BORO" in names:
        add("BORO", [20, 200, 400, 600, 800], [1.15, 1.30, 1.45, 1.60, 1.75], [800, 960, 1060, 1150, 1200], 2230)
    if "QUARTZ" in names:
        add("QUARTZ", [20, 200, 400, 600, 800, 1000], [1.38, 1.55, 1.75, 1.95, 2.15, 2.3],
            [740, 920, 1030, 1100, 1150, 1180], 2200)
    for nm, d in (("GAP15", 1.5), ("GAP4", 4.0), ("GAP3", 3.0)):
        if nm in names:
            T2, k2 = gap_k(d)
            add(nm, T2, k2, [520] * len(T2), 1.0)        # argon: negligible heat capacity
    if "CONTACT_RING" in names:      # 0.3 mm layer: k = h * t
        add("CONTACT_RING", [20, 1200], [ring_contact_h * 3e-4] * 2, [500, 500], 7950)
    if "CONTACT_PUCK" in names:      # 0.5 mm layer
        add("CONTACT_PUCK", [20, 1200], [puck_contact_h * 5e-4] * 2, [500, 500], 7950)
    return "".join(s)


# ------------------------------------------------------------------------------------------ geometry
def rect(r0, r1, z0, z1):
    return [(r0, z0), (r1, z0), (r1, z1), (r0, z1)]


def joint_regions(oring_mat="FKM"):
    """Cone outlet flange (machine side), centring ring with contact layers, O-ring, joint gap."""
    import parts as PT
    kf = P.JOINT
    g = kf.ring_thk / 2
    rf = kf.flange_od / 2
    c = 0.3
    ro_or = kf.ring_od / 2 + 4.9
    regs = [
        F.Region("cone_flange", "S316L", PT.kf_flange_profile(kf, +g, down=False, tube_len=P.CONE_OUTLET_LEN, recess=False), 1.5),
        F.Region("ring", "S304", rect(kf.ring_id / 2, kf.ring_od / 2, -g + c, g - c), 0.4),
        F.Region("ring_c_lo", "CONTACT_RING", rect(kf.ring_id / 2, kf.ring_od / 2, -g, -g + c), 0.3),
        F.Region("ring_c_hi", "CONTACT_RING", rect(kf.ring_id / 2, kf.ring_od / 2, g - c, g), 0.3),
        F.Region("oring", oring_mat, rect(kf.ring_od / 2, ro_or, -g, g), 0.5),
        F.Region("joint_gap", "GAP4", rect(ro_or, rf, -g, g), 0.8),
    ]
    return regs


def pile_height(mass_g, radius):
    return mass_g * 1e-3 / (P.SHOT["rho"] * PILE_FRAC * math.pi * (radius * 1e-3) ** 2) * 1e3


def design_B(mass_g, liner=True, puck=True, puck_mat="S304"):
    import parts as PT
    b = P.B
    prof, z = PT.option_b_vessel_profile(recess=False)
    regs = joint_regions()
    regs.append(F.Region("vessel", "S316L", prof, 1.2))
    floor = z["floor"]
    R_i = z["R_i"]
    zz = floor
    if puck:
        regs.append(F.Region("puck_contact", "CONTACT_PUCK", rect(0, b["puck_d"] / 2, floor, floor + 0.5), 0.5))
        regs.append(F.Region("puck", puck_mat, rect(0, b["puck_d"] / 2, floor + 0.5, floor + 0.5 + b["puck_h"]), 2.5))
        regs.append(F.Region("puck_gap", "GAP15", rect(b["puck_d"] / 2, R_i, floor, floor + 0.5 + b["puck_h"]), 0.7))
        zz = floor + 0.5 + b["puck_h"]
    r_pile = R_i
    top_liner = z["z_red"] + 8.0 - 3.0
    if liner:
        lo, li = b["liner_od"] / 2, b["liner_od"] / 2 - b["liner_wall"]
        regs.append(F.Region("liner_contact", "CONTACT_PUCK", rect(li, lo, zz, zz + 0.5), 0.4))
        regs.append(F.Region("liner", "S304", rect(li, lo, zz + 0.5, top_liner), 1.0))
        regs.append(F.Region("liner_gap", "GAP15", rect(lo, R_i, zz, top_liner), 0.7))
        r_pile = li
    h = pile_height(mass_g, r_pile)
    regs.append(F.Region("pile", "PILE", rect(0, r_pile, zz, zz + h), 2.0, init_T=T_SHOT))
    cavity = Polygon([(0, z["z_bot"]), (R_i + 0.01, z["z_bot"]), (R_i + 0.01, z["z_red"] + 8.0),
                      (P.JOINT.bore / 2 + 0.01, z["z_stub"] - 8.0),
                      (P.JOINT.bore / 2 + 0.01, P.JOINT.ring_thk / 2 + P.CONE_OUTLET_LEN), (0, P.JOINT.ring_thk / 2 + P.CONE_OUTLET_LEN)])
    probes = {"TC_top": (P.JOINT.tube_od / 2, z["top"] - P.JOINT.lip - 9.0),
              "TC_bottom": (z["R_o"], floor + 6.0),
              "flange_rim": (P.JOINT.flange_od / 2, -P.JOINT.ring_thk / 2 - 1.0),
              "bottom_centre": (0.0, z["z_bot"])}
    return regs, cavity, probes, dict(pile_top=zz + h, pile_r=r_pile, pile_h=h)


def design_A(mass_g, liner=True, puck=True):
    import parts as PT
    kf = P.JOINT
    a = P.A
    g = kf.ring_thk / 2
    L = a["nipple_len"]
    top_face, bot_face = -g, -g - L
    regs = joint_regions()
    up = PT.kf_flange_profile(kf, top_face, down=True, tube_len=L / 2, recess=False)
    lo = PT.kf_flange_profile(kf, bot_face, down=False, tube_len=L / 2, recess=False)
    # one closed outline for the nipple: upper flange down to mid, lower flange up to mid
    rb = kf.bore / 2
    outline = [p for p in up if p[0] > rb + 1e-6]           # outer points of the upper half, top to mid
    outline += [p for p in reversed(lo) if p[0] > rb + 1e-6]  # outer points of the lower half, mid to bottom
    outline += [(rb, bot_face), (rb, top_face)]
    # remove the duplicate mid points
    clean = []
    for p in outline:
        if not clean or abs(p[0] - clean[-1][0]) > 1e-6 or abs(p[1] - clean[-1][1]) > 1e-6:
            clean.append(p)
    regs.append(F.Region("nipple", "S316L", clean, 1.2))
    # bottom joint: ring, O-ring, gap, blank
    zb = bot_face - 2 * g                       # blank's sealing face
    c = 0.3
    ro_or = kf.ring_od / 2 + 4.9
    regs += [F.Region("bring", "S304", rect(kf.ring_id / 2, kf.ring_od / 2, zb + c, bot_face - c), 0.4),
             F.Region("bring_c_lo", "CONTACT_RING", rect(kf.ring_id / 2, kf.ring_od / 2, zb, zb + c), 0.3),
             F.Region("bring_c_hi", "CONTACT_RING", rect(kf.ring_id / 2, kf.ring_od / 2, bot_face - c, bot_face), 0.3),
             F.Region("boring", "FKM", rect(kf.ring_od / 2, ro_or, zb, bot_face), 0.5),
             F.Region("bjoint_gap", "GAP4", rect(ro_or, kf.flange_od / 2, zb, bot_face), 0.8)]
    rf, rh = kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    regs.append(F.Region("blank", "S304", [(0, zb), (rf, zb), (rf, zb - t_edge), (rh, zb - kf.lip), (0, zb - kf.lip)], 1.5))
    zz = zb
    r_in = kf.ring_id / 2          # the puck stands inside the bottom centring ring
    if puck:
        pr = a["puck_d"] / 2
        regs.append(F.Region("puck_contact", "CONTACT_PUCK", rect(0, pr, zb, zb + 0.5), 0.5))
        regs.append(F.Region("puck", "S304", rect(0, pr, zb + 0.5, zb + 0.5 + a["puck_h"]), 2.0))
        regs.append(F.Region("puck_gap", "GAP15", [(pr, zb), (r_in, zb), (r_in, bot_face), (rb, bot_face),
                                                  (rb, zb + 0.5 + a["puck_h"]), (pr, zb + 0.5 + a["puck_h"])], 0.6))
        zz = zb + 0.5 + a["puck_h"]
    r_pile = rb
    if liner:
        lo_, li_ = a["liner_od"] / 2, a["liner_od"] / 2 - a["liner_wall"]
        top_l = top_face - a["liner_gap_top"]
        regs.append(F.Region("liner_contact", "CONTACT_PUCK", rect(li_, lo_, zz, zz + 0.5), 0.4))
        regs.append(F.Region("liner", "S304", rect(li_, lo_, zz + 0.5, top_l), 1.0))
        regs.append(F.Region("liner_gap", "GAP15", rect(lo_, rb, zz, top_l), 0.5))
        r_pile = li_
    h = pile_height(mass_g, r_pile)
    regs.append(F.Region("pile", "PILE", rect(0, r_pile, zz, zz + h), 1.5, init_T=T_SHOT))
    cavity = Polygon([(0, zb), (rb + 0.01, zb), (rb + 0.01, g + P.CONE_OUTLET_LEN), (0, g + P.CONE_OUTLET_LEN)])
    probes = {"TC_top": (kf.tube_od / 2, top_face - kf.lip - 9.0),
              "TC_bottom": (kf.tube_od / 2, bot_face + kf.lip + 9.0),
              "flange_rim": (kf.flange_od / 2, top_face - 1.0),
              "bottom_centre": (0.0, zb - kf.lip)}
    return regs, cavity, probes, dict(pile_top=zz + h, pile_r=r_pile, pile_h=h)


def design_C(mass_g, glass="QUARTZ", seal="FKM", sleeve=True, pan=True):
    """Glass rebuild in the stock layout (parts._stock_z): KF flange + neck + reducer, valve-delete spacer,
    top plate with the glass groove, glass, bottom plate, entrance sleeve and bottom pan. Tie rods, the
    perforated guard and the bolts are left out."""
    import parts as PT
    kf, s, c = P.JOINT, P.STOCK, P.C
    g = kf.ring_thk / 2
    z = PT._stock_z()
    regs = joint_regions()
    neck = PT.kf_flange_profile(kf, z["face"], down=True, tube_len=s["neck_len"], recess=False)
    r1, r2 = kf.tube_od / 2, s["reducer_d2"] / 2
    rb = kf.bore / 2
    z_n, z_r = z["neck"], z["valve_top"]
    outline = [pt for pt in neck[:-2]] + [(r1, z_n), (r2, z_r), (r2 - 1.6, z_r), (rb + 0.2, z_n - 2.0), (rb, z_n - 2.0)]
    regs.append(F.Region("neck_reducer", "S316L", outline, 1.0))
    zt_sp, zb_sp = z["valve_top"], z["valve_bot"]
    Ro = s["valve_body_od"] / 2
    rbore = c["sleeve_od"] / 2 + 0.4
    rcb = c["sleeve_lip_od"] / 2 + 0.4
    lip_t = 3.0
    regs.append(F.Region("spacer", "S316L", [(rbore, zb_sp), (Ro, zb_sp), (Ro, zt_sp), (rcb, zt_sp),
                                             (rcb, zt_sp - lip_t), (rbore, zt_sp - lip_t)], 1.5))
    ro_s, ri_s = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]        # the plates' grooves fit the stock glass
    g_out, g_in = ro_s + 1.5, ri_s - 1.5
    gd, gk = s["seal_groove_d"], 2.0
    zp = z["plate_bot"]
    Rp = s["top_plate_od"] / 2
    rpb = s["valve_bore"] / 2
    regs.append(F.Region("top_plate", "S316L", [(rpb, zp), (g_in, zp), (g_in, zp + gd), (g_out, zp + gd), (g_out, zp),
                                                (Rp, zp), (Rp, zb_sp), (rpb, zb_sp)], 1.5))
    ro_g = c["quartz_od"] / 2 if glass == "QUARTZ" else ro_s
    ri_g = ro_g - (c["quartz_wall"] if glass == "QUARTZ" else s["glass_wall"])
    zt_gl, zb_gl = z["glass_top"], z["glass_bot"]
    regs.append(F.Region("seal_top", seal, rect(g_in, g_out, zt_gl, zt_gl + gk), 0.5))
    regs.append(F.Region("glass", glass, rect(ri_g, ro_g, zb_gl, zt_gl), 0.8))
    regs.append(F.Region("seal_bot", seal, rect(g_in, g_out, zb_gl - gk, zb_gl), 0.5))
    zb_pl = z["bplate_top"]
    Rb = s["bottom_plate_od"] / 2
    regs.append(F.Region("bottom_plate", "S316L", [(0, z["bottom"]), (Rb, z["bottom"]), (Rb, zb_pl), (g_out, zb_pl),
                                                   (g_out, zb_pl - gd), (g_in, zb_pl - gd), (g_in, zb_pl), (0, zb_pl)], 2.0))
    zz = zb_pl
    r_pile = ri_g
    if pan:
        pan_r = ri_s - 1.5
        pt = 1.5
        regs.append(F.Region("pan_contact", "CONTACT_PUCK", rect(0, pan_r, zb_pl, zb_pl + 0.5), 0.5))
        regs.append(F.Region("pan", "S304", [(0, zb_pl + 0.5), (pan_r, zb_pl + 0.5), (pan_r, zb_pl + 28.0),
                                             (pan_r - pt, zb_pl + 28.0), (pan_r - pt, zb_pl + 0.5 + pt),
                                             (0, zb_pl + 0.5 + pt)], 1.0))
        zz = zb_pl + 0.5 + pt
        r_pile = pan_r - pt
    h = pile_height(mass_g, r_pile)
    regs.append(F.Region("pile", "PILE", rect(0, r_pile, zz, zz + h), 2.0, init_T=T_SHOT))
    if sleeve:
        so, si = c["sleeve_od"] / 2, c["sleeve_od"] / 2 - c["sleeve_wall"]
        sl_bot = zt_gl - 20.0
        regs.append(F.Region("sleeve", "S304", [(si, sl_bot), (so, sl_bot), (so, zt_sp - lip_t),
                                                (c["sleeve_lip_od"] / 2, zt_sp - lip_t),
                                                (c["sleeve_lip_od"] / 2, zt_sp), (si, zt_sp)], 0.6))
    top = g + P.CONE_OUTLET_LEN
    e = 0.01
    cavity = Polygon([(0, zb_pl), (ri_g + e, zb_pl), (ri_g + e, zt_gl), (g_in + e, zt_gl), (g_in + e, zp),
                      (rpb + e, zp), (rpb + e, zb_sp), (rbore + e, zb_sp), (rbore + e, zt_sp - lip_t),
                      (rcb + e, zt_sp - lip_t), (rcb + e, zt_sp), (r2 - 1.6 + e, z_r), (rb + 0.2 + e, z_n - 2.0),
                      (rb + e, z_n - 2.0), (rb + e, top), (0, top)])
    probes = {"glass_rim_top": (ro_g, zt_gl - 1.0), "glass_bottom_out": (ro_g, zb_gl + 5.0),
              "flange_rim": (kf.flange_od / 2, -g - 1.0), "plate_rim": (Rb, zb_pl - 5.0)}
    return regs, cavity, probes, dict(pile_top=zz + h, pile_r=r_pile, pile_h=h)


DESIGNS = {"A": design_A, "B": design_B, "C": design_C}
CASES = {
    "B_100": ("B", 100, {}), "B_400": ("B", 400, {}), "B_816": ("B", 816, {}),
    "B_816_k2": ("B", 816, {}, {"pile_k": 2.0}), "B_816_k20": ("B", 816, {}, {"pile_k": 20.0}),
    "B_816_noliner": ("B", 816, {"liner": False}), "B_816_cupuck": ("B", 816, {"puck_mat": "CU"}),
    "A_100": ("A", 100, {}), "A_250": ("A", 250, {}), "A_400": ("A", 400, {}),
    "C_400": ("C", 400, {}), "C_816": ("C", 816, {}),
    "C_400_boro": ("C", 400, {"glass": "BORO"}),
}
SEAL_SETS = {"A": ["oring", "boring"], "B": ["oring"], "C": ["oring", "seal_top", "seal_bot"]}
GLASS_SETS = {"C": ["glass"]}


# ------------------------------------------------------------------------------------- view factors
def cavity_faces(m, cavity, exclude_regions=("pile",)):
    faces = []
    for e in m.edges:
        if e["mid"][0] < 1e-6 and abs(e["normal"][0] + 1) < 1e-6:
            continue
        probe = e["mid"] + 0.3 * e["normal"]
        if cavity.contains(Point(*probe)) and e["region"] not in exclude_regions:
            faces.append(e)
    return faces


def view_factors(m, faces, pile_r, pile_top, n_rays=200000, seed=1):
    """Monte-Carlo view factors from the pile's top disk to each cavity face (first hit)."""
    rng = np.random.default_rng(seed)
    segs = np.array([[m.nodes[f["n"][0]][0], m.nodes[f["n"][0]][1], m.nodes[f["n"][1]][0], m.nodes[f["n"][1]][1]]
                     for f in faces])
    hits = np.zeros(len(faces))
    escaped = 0
    chunk = 4000
    for k0 in range(0, n_rays, chunk):
        n = min(chunk, n_rays - k0)
        rr = pile_r * np.sqrt(rng.random(n))
        ph = 2 * np.pi * rng.random(n)
        o = np.stack([rr * np.cos(ph), rr * np.sin(ph), np.full(n, pile_top + 1e-6)], 1)
        u1, u2 = rng.random(n), rng.random(n)
        st = np.sqrt(u1)
        d = np.stack([st * np.cos(2 * np.pi * u2), st * np.sin(2 * np.pi * u2), np.sqrt(1 - u1)], 1)
        best = np.full(n, np.inf)
        idx = np.full(n, -1)
        r1, z1, r2, z2 = segs[:, 0], segs[:, 1], segs[:, 2], segs[:, 3]
        horiz = np.abs(z2 - z1) < 1e-9
        # cones / cylinders
        nz = ~horiz
        if nz.any():
            b = np.zeros_like(r1)
            b[nz] = (r2[nz] - r1[nz]) / (z2[nz] - z1[nz])
            a = r1 - b * z1
            ox, oy, oz = o[:, 0:1], o[:, 1:2], o[:, 2:3]
            dx, dy, dz = d[:, 0:1], d[:, 1:2], d[:, 2:3]
            A = dx ** 2 + dy ** 2 - (b ** 2) * dz ** 2
            B = 2 * (ox * dx + oy * dy - (a + b * oz) * b * dz)
            C = ox ** 2 + oy ** 2 - (a + b * oz) ** 2
            disc = B ** 2 - 4 * A * C
            ok = disc >= 0
            sq = np.sqrt(np.where(ok, disc, 0))
            with np.errstate(divide="ignore", invalid="ignore"):
                for sgn in (-1, 1):
                    t = np.where(np.abs(A) > 1e-12, (-B + sgn * sq) / (2 * A), -C / np.where(B == 0, 1e-30, B))
                    zz = oz + t * dz
                    zlo, zhi = np.minimum(z1, z2), np.maximum(z1, z2)
                    good = ok & (t > 1e-6) & (zz >= zlo - 1e-9) & (zz <= zhi + 1e-9) & ((a + b * zz) >= 0) & nz[None, :]
                    tt = np.where(good, t, np.inf)
                    j = np.argmin(tt, axis=1)
                    tm = tt[np.arange(n), j]
                    better = tm < best
                    best[better] = tm[better]
                    idx[better] = j[better]
        if horiz.any():
            hz = np.where(horiz)[0]
            with np.errstate(divide="ignore", invalid="ignore"):
                t = (z1[hz][None, :] - o[:, 2:3]) / d[:, 2:3]
            px = o[:, 0:1] + t * d[:, 0:1]
            py = o[:, 1:2] + t * d[:, 1:2]
            rad = np.hypot(px, py)
            lo, hi = np.minimum(r1[hz], r2[hz]), np.maximum(r1[hz], r2[hz])
            good = (t > 1e-6) & (rad >= lo[None, :] - 1e-9) & (rad <= hi[None, :] + 1e-9)
            tt = np.where(good, t, np.inf)
            j = np.argmin(tt, axis=1)
            tm = tt[np.arange(n), j]
            better = tm < best
            best[better] = tm[better]
            idx[better] = hz[j[better]]
        np.add.at(hits, idx[idx >= 0], 1)
        escaped += int((idx < 0).sum())
    return hits / n_rays, escaped / n_rays


# ---------------------------------------------------------------------------------------- the deck
def nearest_node(m, p, nodes=None):
    best, bn = 1e9, None
    for n in (nodes or m.nodes):
        r, z = m.nodes[n]
        d = (r - p[0]) ** 2 + (z - p[1]) ** 2
        if d < best:
            best, bn = d, n
    return bn


def write_deck(path, m, regs, cavity, probes, pile_info, extra, rad=None, design="B"):
    kf = P.JOINT
    fixed_z = kf.ring_thk / 2 + P.CONE_OUTLET_LEN
    mats = sorted({r.material for r in regs})
    cav = cavity_faces(m, cavity, exclude_regions=())
    cav_ids = {(f["elem"], f["face"]) for f in cav}
    ext, fixed_nodes, pile_top = [], set(), []
    for e in m.edges:
        r, z = e["mid"]
        if r < 1e-6 and abs(e["normal"][0] + 1) < 1e-6:
            continue                                            # on the axis
        if abs(z - fixed_z) < 1e-6:
            fixed_nodes.update(e["n"])
            continue
        if (e["elem"], e["face"]) in cav_ids:
            if e["region"] == "pile" and e["normal"][1] > 0.5:
                pile_top.append(e)
            continue
        ext.append(e)
    with open(path, "w") as f:
        f.write("*HEADING\ncollection cup thermal\n")
        F.write_mesh(f, m)
        F.write_set(f, "NSET", "FIXED", sorted(fixed_nodes))
        for nm, p in probes.items():
            F.write_set(f, "NSET", nm.upper(), [nearest_node(m, p)])
        seal_sets = [s for s in SEAL_SETS.get(design, []) if m.elset(s)]
        for s in seal_sets:
            F.write_set(f, "NSET", "N_" + s.upper(), m.region_nodes(s))
        for s in GLASS_SETS.get(design, []):
            if m.elset(s):
                F.write_set(f, "NSET", "N_" + s.upper(), m.region_nodes(s))
        F.write_set(f, "NSET", "N_PILE", m.region_nodes("pile"))
        F.write_set(f, "NSET", "N_PILETOP", sorted({n for e in pile_top for n in e["n"]}))
        f.write(material_cards(set(mats), **extra))
        for reg in regs:
            if m.elset(reg.name):
                f.write(f"*SOLID SECTION, ELSET=E_{reg.name}, MATERIAL={reg.material}\n")
        f.write(f"*PHYSICAL CONSTANTS, ABSOLUTE ZERO={F.ABS0}, STEFAN BOLTZMANN={F.SIGMA}\n")
        f.write(f"*INITIAL CONDITIONS, TYPE=TEMPERATURE\nNALL, {T_AMB}\n")
        hot = m.region_nodes([r.name for r in regs if r.init_T is not None])
        for n in hot:
            f.write(f"{n}, {T_SHOT}\n")
        f.write("*TIME POINTS, NAME=TP, TIME=TOTAL TIME\n" + "\n".join(f"{t}," for t in TIME_POINTS) + "\n")
        f.write("*TIME POINTS, NAME=TF, TIME=TOTAL TIME\n" + "\n".join(f"{t}," for t in FIELD_TIMES) + "\n")
        if rad is not None:
            f.write("*AMPLITUDE, NAME=PRAD, TIME=TOTAL TIME\n")
            for t, a in zip(rad["t"], rad["a"]):
                f.write(f"{t:.4f}, {a:.6e}\n")
        prints = ["N_PILE", "N_PILETOP"] + [p.upper() for p in probes] + ["N_" + s.upper() for s in seal_sets]
        prints += ["N_" + s.upper() for s in GLASS_SETS.get(design, []) if m.elset(s)]
        # two steps: CalculiX will not cut an increment below 1e-6 of the step, and the first seconds
        # (the hot/cold step at the pile's contact faces) need increments of ~1e-4 s
        for k, (t_step, dt0, dtmin, dtmax) in enumerate(((T_STEP1, 1e-3, 2e-5, 2.0),
                                                       (T_END - T_STEP1, 0.5, 4e-3, 30.0))):
            f.write(f"*STEP, INC=100000\n*HEAT TRANSFER, DELTMX=25\n{dt0}, {t_step}, {dtmin}, {dtmax}\n")
            if k == 0:
                f.write(f"*BOUNDARY\nFIXED, 11, 11, {T_AMB}\n*FILM\n")
                for e in ext:
                    f.write(f"{e['elem']}, F{e['face']}, {T_AMB}, {H_NAT * F.W_M2K:.6e}\n")
                f.write("*RADIATE\n")
                for e in ext:
                    eps = EPS_GLASS if m.elem_region[e["elem"]] == "glass" else EPS_STEEL
                    f.write(f"{e['elem']}, R{e['face']}, {T_AMB}, {eps}\n")
                for e in pile_top:
                    f.write(f"{e['elem']}, R{e['face']}, {T_AMB}, {EPS_PILE}\n")
                if rad is not None:
                    f.write("*DFLUX, AMPLITUDE=PRAD\n")
                    for (el, fc), q in rad["faces"].items():
                        if q > 0:
                            f.write(f"{el}, S{fc}, {q:.6e}\n")
            for s_ in prints:
                f.write(f"*NODE PRINT, NSET={s_}, TIME POINTS=TP\nNT\n")
            f.write("*NODE FILE, TIME POINTS=TF\nNT\n*END STEP\n")
    return dict(ext=len(ext), cav=len(cav), pile_top=pile_top, fixed=len(fixed_nodes))


def series(blocks, setname, how="max"):
    key = next((k for k in blocks if k[1] == setname.upper()), None)
    if key is None:
        return None, None
    ts, vs = [], []
    for t, vals in blocks[key]:
        arr = np.array([v[0] for v in vals.values()])
        ts.append(t)
        vs.append(arr.max() if how == "max" else arr.mean())
    return np.array(ts), np.array(vs)


def pile_power(m, blocks, pile_top):
    """Radiated power of the pile top vs time (mW, full 360 deg) from its node temperatures."""
    key = next(k for k in blocks if k[1] == "N_PILETOP")
    out_t, out_p = [], []
    for t, vals in blocks[key]:
        P_ = 0.0
        for e in pile_top:
            Tm = np.mean([vals[n][0] for n in e["n"] if n in vals]) + 273.15
            P_ += EPS_PILE * F.SIGMA * (Tm ** 4 - (T_AMB + 273.15) ** 4) * F.ring_area(e, m.nodes)
        out_t.append(t)
        out_p.append(P_)
    return np.array(out_t), np.array(out_p)


def run_case(name, spec):
    design, mass, kw = spec[0], spec[1], spec[2]
    extra = spec[3] if len(spec) > 3 else {}
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    regs, cavity, probes, info = DESIGNS[design](mass, **kw)
    t0 = time.time()
    for r in regs:
        r.size *= MESH_SCALE
    m = F.build_mesh(regs, order=1)
    deck1 = write_deck(d / "pass1.inp", m, regs, cavity, probes, info, extra, None, design)
    F.run_ccx("pass1", d, threads=1)
    b1 = F.read_dat_blocks(d / "pass1.dat")
    tP, Pw = pile_power(m, b1, deck1["pile_top"])
    faces = cavity_faces(m, cavity)
    faces = [f for f in faces if f["mid"][1] > info["pile_top"] - 1e-6 and f["region"] != "pile"]
    Fv, esc = view_factors(m, faces, info["pile_r"], info["pile_top"])
    Pref = max(Pw.max(), 1e-9)
    rad = {"t": [0.0] + list(tP), "a": [Pw[0] / Pref] + list(Pw / Pref), "faces": {}}
    for fc, fv in zip(faces, Fv):
        if fv > 0:
            rad["faces"][(fc["elem"], fc["face"])] = Pref * fv / F.ring_area(fc, m.nodes)
    write_deck(d / "pass2.inp", m, regs, cavity, probes, info, extra, rad, design)
    F.run_ccx("pass2", d, threads=1)
    b2 = F.read_dat_blocks(d / "pass2.dat")
    res = {"design": design, "mass_g": mass, "options": kw, "extra": extra, "nodes": len(m.nodes),
           "elements": len(m.elems), "pile_h_mm": round(info["pile_h"], 1),
           "pile_top_mm_below_joint": round(-info["pile_top"], 1),
           "view_factor_to_walls": round(float(Fv.sum()), 3), "escaped_through_outlet": round(esc, 3),
           "pile_radiated_peak_W": round(float(Pw.max()) / 1e3, 1), "series": {}, "peaks": {},
           "runtime_s": None}
    sets = ["N_PILE"] + [p.upper() for p in probes] + ["N_" + s.upper() for s in SEAL_SETS.get(design, [])]
    sets += ["N_" + s.upper() for s in GLASS_SETS.get(design, [])]
    for s in sets:
        ts, vs = series(b2, s, "mean" if s == "N_PILE" else "max")
        if ts is None:
            continue
        res["series"][s] = {"t": [round(x, 3) for x in ts], "T": [round(x, 1) for x in vs]}
        k = int(np.argmax(vs))
        res["peaks"][s] = {"T_max": round(float(vs[k]), 1), "t_at_max_s": round(float(ts[k]), 1),
                           "T_at_60s": round(float(np.interp(60, ts, vs)), 1),
                           "T_at_300s": round(float(np.interp(300, ts, vs)), 1),
                           "T_at_3600s": round(float(vs[-1]), 1)}
        # first time above the seal limits (for the O-ring sets)
        for lim in (100, 150, 200):
            above = np.where(vs >= lim)[0]
            res["peaks"][s][f"t_first_{lim}C_s"] = round(float(ts[above[0]]), 1) if len(above) else None
    # glass: largest temperature difference across the glass at any time (thermal-shock indicator)
    if design == "C":
        key = next(k for k in b2 if k[1] == "N_GLASS")
        dts = [(t, max(v[0] for v in vals.values()) - min(v[0] for v in vals.values())) for t, vals in b2[key]]
        tm, dm = max(dts, key=lambda x: x[1])
        res["peaks"]["glass_dT"] = {"dT_max": round(dm, 1), "t_s": round(tm, 1)}
    res["runtime_s"] = round(time.time() - t0, 1)
    (d / "result.json").write_text(json.dumps(res, indent=1) + "\n")
    # field plot at the time of the O-ring peak (or 300 s)
    try:
        plot_field(m, d, regs, name, res)
    except Exception as ex:  # noqa: BLE001
        print("plot failed", name, ex)
    return res


def plot_field(m, d, regs, name, res):
    frd = F.read_frd(d / "pass2.frd")
    if not frd:
        return
    corner = sorted({n for ns in m.elems.values() for n in ns[:3]})
    idx = {n: i for i, n in enumerate(corner)}
    xy = np.array([m.nodes[n] for n in corner])
    tri = np.array([[idx[n] for n in ns[:3]] for ns in m.elems.values()])
    fig, axes = plt.subplots(1, len(frd), figsize=(2.3 * len(frd), 6.5), sharey=True)
    vmax = 1050
    for ax, (t, vals) in zip(np.atleast_1d(axes), frd):
        T = np.array([vals[n][0] for n in corner])
        tr = mtri.Triangulation(np.concatenate([xy[:, 0], -xy[:, 0]]), np.concatenate([xy[:, 1], xy[:, 1]]),
                                np.concatenate([tri, tri + len(xy)]))
        cs = ax.tripcolor(tr, np.concatenate([T, T]), cmap="inferno", vmin=20, vmax=vmax, shading="gouraud")
        ax.set_aspect("equal")
        ax.set_title(f"t = {t:g} s\nmax {T.max():.0f} C", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.set_xlabel("r (mm)", fontsize=7)
    np.atleast_1d(axes)[0].set_ylabel("z (mm), 0 = joint", fontsize=8)
    fig.colorbar(cs, ax=axes, shrink=0.6, label="T (C)")
    fig.suptitle(f"{name}: {res['mass_g']} g of shot at {T_SHOT:.0f} C", fontsize=10)
    fig.savefig(d / "field.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def summary(results):
    rows = []
    lines = ["# Thermal FEA summary (CalculiX, axisymmetric)\n",
             "Shot lands all at once at t = 0 at 1050 C. Peak temperatures over the first hour. "
             "Seal limits used: FKM 200 C continuous / 230 C short; EPDM 150 / 175 C; FFKM 240 / 325 C.\n",
             "| Case | Pile height (mm) | Pile top below joint (mm) | Top O-ring max (C) [time s] | "
             "Other seal max (C) | TC top max (C) | TC bottom max (C) | Glass dT max (K) |",
             "|---|---:|---:|---|---|---:|---:|---:|"]
    for name, r in results.items():
        pk = r["peaks"]
        top = pk.get("N_ORING", {})
        others = []
        for s in ("N_BORING", "N_SEAL_TOP", "N_SEAL_BOT"):
            if s in pk:
                others.append(f"{s[2:].lower()} {pk[s]['T_max']:.0f} [{pk[s]['t_at_max_s']:.0f}]")
        tct = pk.get("TC_TOP", {}).get("T_max", float("nan"))
        tcb = pk.get("TC_BOTTOM", {}).get("T_max", float("nan"))
        gd = pk.get("glass_dT", {}).get("dT_max", "")
        lines.append(f"| {name} | {r['pile_h_mm']} | {r['pile_top_mm_below_joint']} | {top.get('T_max', 0):.0f} "
                     f"[{top.get('t_at_max_s', 0):.0f}] | {'; '.join(others)} | {tct:.0f} | {tcb:.0f} | {gd} |")
        rows.append(name)
    (HERE / "out" / "thermal_summary.md").write_text("\n".join(lines) + "\n")
    (HERE / "out" / "thermal_summary.json").write_text(json.dumps(
        {k: {kk: vv for kk, vv in v.items() if kk != "series"} for k, v in results.items()}, indent=1) + "\n")


def plot_seals(results):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, des in zip(axes, ("A", "B", "C")):
        for name, r in results.items():
            if r["design"] != des:
                continue
            for s, ls in (("N_ORING", "-"), ("N_BORING", "--"), ("N_SEAL_BOT", "--"), ("N_SEAL_TOP", ":")):
                if s in r["series"]:
                    ser = r["series"][s]
                    ax.plot(ser["t"], ser["T"], ls, label=f"{name} {s[2:].lower()}")
        for lim, lab in ((150, "EPDM"), (200, "FKM"), (240, "FFKM")):
            ax.axhline(lim, color="grey", lw=0.8, ls="-.")
            ax.text(1.0, lim + 3, lab, fontsize=7, color="grey")
        ax.set_xscale("log")
        ax.set_xlim(1, T_END)
        ax.set_xlabel("time after the shot lands (s)")
        ax.set_ylabel("seal temperature, max over the seal (C)")
        ax.set_title({"A": "A: KF nipple + blank", "B": "B: welded 316L", "C": "C: quartz rebuild"}[des])
        ax.legend(fontsize=6.5, loc="upper left")
        ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMG / "thermal_seals.png", dpi=120)
    plt.close(fig)


def _one(name):
    try:
        return name, run_case(name, CASES[name])
    except Exception as ex:  # noqa: BLE001
        return name, repr(ex)[:400]


def main(argv):
    names = argv or list(CASES)
    results = {}
    old = HERE / "out" / "thermal_summary.json"
    from multiprocessing import Pool
    with Pool(int(__import__("os").environ.get("THERMAL_JOBS", "4"))) as pool:
        for name, res in pool.imap_unordered(_one, names):
            if isinstance(res, dict):
                results[name] = res
                print(time.strftime("%H:%M:%S"), name, {k: v["T_max"] for k, v in res["peaks"].items()
                                                         if "T_max" in v}, flush=True)
            else:
                print(time.strftime("%H:%M:%S"), "FAILED", name, res, flush=True)
    # merge with earlier results so a partial run keeps the rest
    allres = {}
    for name in CASES:
        p = OUT / name / "result.json"
        if p.exists():
            allres[name] = json.loads(p.read_text())
    summary(allres)
    plot_seals(allres)


if __name__ == "__main__":
    main(sys.argv[1:])
