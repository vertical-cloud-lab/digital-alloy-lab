"""Parametric CadQuery model of the fast-track machines (FT-0, FT-1, FT-1V) and the states between them (#260).

One model, five states, in the order the parts arrive (``STATES``):

  S1     optics bench: laser, scan head, lens and RTC5 on the T-slot frame, guide laser onto a target on the deck
  S2     the stainless box closed round the beam: window, beam tube, interlocks; full power into a water-cooled dump
  FT-0   single-track bench: heated plate on a fixed rod in the well block, gas, O2 analyzer; layers spread by hand
  FT-1   purge-box LPBF: the rod goes to a Zaber X-VSR20A under the box, a Zaber X-LSQ075B moves a hopper-blade
  FT-1V  the same deck cassette, rod drive and optics moved onto an Ideal Vacuum 12 in cube with a pump-purge kit

Run:  python desktop-lpbf/fast-track/cad/ft_model.py            # builds every state, writes out/ft-*.step
      xvfb-run -a python desktop-lpbf/fast-track/cad/ft_render.py   # renders (img/)
      python desktop-lpbf/fast-track/cad/ft_checks.py               # interference, beam, travel, fit, gas volume

Frame: mm. Origin at the centre of the substrate's top face at the start of a build (the powder plane) in the box
states. +X is the recoat direction, +Y points to the back, +Z up. The bench stays put; in FT-1V the cassette and
the optics sit DZ_CUBE higher, because the cube's floor plate is thicker than the box's sheet floor.

Bought parts are envelopes drawn from the dimensions their makers publish, or estimates where the page gave none
(each is marked in ``P``). Nothing here comes from a vendor CAD file. Every part carries its parts.csv line (L1, M2,
E1, ...) or, for a part we make, an MK number listed in MADE.
"""
from __future__ import annotations

import math
import pathlib
import sys
from dataclasses import dataclass

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "cad"))
from lpbf_model import box, comp, cyl, kf_stub, polyline_pipe, tslot, tube  # noqa: E402

V = cq.Vector
IN = 25.4

# --------------------------------------------------------------------------------------------------
# Parameters. Sources: datasheet (read 2026-11-26), study (fast_track.py / README), or "est." (estimate).
# --------------------------------------------------------------------------------------------------
P = dict(
    # --- the well and the plate (study; plate redrawn here, see MADE MK-04) ---
    deck_t=10.0,                 # 6061 deck plate (study)
    so_l=12.7, so_d=6.35,        # Macor standoffs under the well block (study: McMaster 8489K75 class)
    so_xy=33.0,                  # standoff positions (+-33, +-33), clear of the overflow cup
    well=(80.0, 80.0, 40.0),     # 6061 well block (study)
    bore=40.00, plate_d=39.80,   # 0.1 mm radial clearance, same alloy at the same temperature (study)
    sub_t=6.0,                   # substrate disc (study)
    hp_t=28.0,                   # heater plate: 28 mm so two 1 in. heaters go in axially from below (this model)
    heater_d=6.35, heater_l=25.4,  # plate heaters 1/4 x 1 in. (this model; the study's 3714N36 length is unchecked)
    heater_r=11.5,               # plate heater pitch radius: clear of the rod socket and of the rope groove
    rod_od=12.7, rod_wall=0.89,  # 1/2 in. thin-wall 304 tube: rod, thermal break and wire duct (this model)
    socket=8.0,                  # rod socket depth in the heater plate
    rope=3.0,                    # fibreglass rope wiper groove (study), square
    pz_top=5.0, pz_bot=-15.0,    # plate travel: +5 lifted for removal, -15 at the end of a 15 mm build (20 mm)
    # --- recoater: Zaber X-LSQ075B (datasheet: 75 mm travel; body sizes est.) ---
    rc_travel=75.0, rc_rail_l=185.0, rc_motor_l=56.0,   # body = travel + 110, motor end 56 (est.; X-LSQ150B = 316 long)
    rc_w=75.0, rc_h=35.0, rc_car=(75.0, 75.0, 8.0),       # cross-section and carriage (est.)
    rc_y=95.5,                   # stage centre line, behind the well
    hopper=(20.0, 46.0, 35.0),   # 20 x 46 mm hopper, ~30 cm3 (this model; the study's was ~30 cm3 too)
    cord_d=3.0,                  # silicone cord blade (study, after Heriot-Watt)
    # --- gas on the well block top (study: 45 x 4 mm slot at 2.5 m/s) ---
    nozzle_slot=(45.0, 4.0), ovf_x=(22.0, 29.0), ovf_y=22.0,
    # --- deck cassette: sized to pass the cube's face opening ---
    deck=(250.0, 250.0), deck_c=(-28.0, 45.0),
    # --- the box: 16 x 12 x 8 in. 304 NEMA 4X, 14 ga (study) ---
    box_in=(16 * IN, 12 * IN, 8 * IN), box_t=1.9, gasket=1.0,
    # --- the cube: Ideal Vacuum 12 in. (route-catalogue-chambers.csv: plate 301.8 x 301.8 x 22.9 incl. a 7.6 boss;
    #     11.4 in. plate to plate inside; outside ~336 with plates). Face opening: est. ---
    cube_frame=12 * IN, cube_plate=301.8, cube_plate_t=22.9, cube_boss=7.6, cube_open=266.0,
    # --- the piston stage: Zaber X-VSR20A (datasheet: 73 mm retracted, 20 mm travel; footprint est.) ---
    vs_h=73.0, vs_travel=20.0, vs_foot=(120.0, 80.0), vs_plat=(80.0, 80.0, 12.0),
    clamp_h=25.0, gland_t=12.0,
    # --- optics: LINOS f = 254 mm (working distance est. 300, housing est. 110 x 66); hurrySCAN 25 envelope (est.) ---
    lens_wd=300.0, lens_d=110.0, lens_l=66.0, head=(160.0, 140.0, 115.0), head_in_z=60.0,
    window_d=50.8, window_t=9.53, beam_d=5.0, field_d=40.0,
    # --- frame: 30 mm T-slot (McMaster 5537T101 class, study) ---
    bench_z=-252.6,               # bench top: leaves a 15 mm riser under the piston stage
)
P["bed_floor"] = P["deck_t"] + P["so_l"] + P["well"][2]        # 62.7: powder plane above the enclosure floor
P["dz_cube"] = P["cube_plate_t"] - P["box_t"]                    # 21.0: the cube's floor is this much thicker
P["cube_in"] = P["cube_frame"] - 2 * P["cube_boss"]              # 289.6 plate to plate inside

C = dict(
    tslot="#c3c9cf", alu="#b9c0c7", alu_dark="#8e979f", ss="#a8b1b9", ss_dark="#7d868e", macor="#efe6cf",
    hot="#e8894a", sub="#d0d4d8", zaber="#2a2f36", zaber_top="#596470", black="#151719", glass="#9fd3ff",
    head="#3b4046", lens="#5d6268", laser="#e6e8ea", fiber="#f08c1a", rubber="#3a3a3a", silicone="#d4553b",
    pcb="#2f7d4f", red="#d22b2b", yellow="#f0c419", green="#2bb24c", blue="#2b6cd2", wood="#c8b28a",
    hose="#7f8890", white="#f2f2f2", cube="#b4bcc4", powder="#8b8d8f", copper="#c87533", target="#30343a",
    water="#3d8fd1", gas="#6cb6e0",
)


@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: str
    pid: str = ""            # parts.csv line, or MK-nn for a part we make, or "" for context
    sub: str = ""            # optics | frame | enclosure | cassette | drive | recoater | gas | safety | bench
    group: str = ""          # moving group: "piston" or "recoater"
    opacity: float = 1.0


# Parts we make (MK numbers): what each is, from what, and in which states it exists.
MADE = {
    "MK-01": "deck plate, 250 x 250 x 10 mm 6061: carries the whole cassette from box to cube",
    "MK-02": "window ring, retaining flange and (box only) inner clamp ring, 6061",
    "MK-03": "well block, 80 x 80 x 40 mm 6061, Ø40.00 bore, two heater holes, overflow slot",
    "MK-04": "heater plate, Ø39.8 x 28 mm 6061, two axial heater holes, TC hole, rod socket, rope groove",
    "MK-05": "substrate discs, Ø39.8 x 6 mm 6061, three M2 countersunk screws at r = 17.1 mm",
    "MK-06": "piston rods, 1/2 in. thin-wall 304 tube: one for the box, one 21 mm longer for the cube",
    "MK-07": "rod gland plate, two O-rings (rated for rough vacuum so it moves to the cube unchanged)",
    "MK-08": "hopper (bent 304), cord clamp, arm and carriage bracket",
    "MK-09": "scan-head plate, 12 mm 6061, and the collimator saddle",
    "MK-10": "beam tubes with flange and lens collar: long (box), short (cube)",
    "MK-11": "slot nozzle and exhaust collector, 304",
    "MK-12": "stage shield, bent 304 sheet with a slot for the carriage bracket",
    "MK-13": "cube top plate: Ideal Vacuum blank P108171 bored for the window ring",
    "MK-14": "cube bottom plate: blank bored for the rod gland",
    "MK-15": "piston-stage bracket plate and rod clamp",
    "MK-16": "overflow cup, 304",
    "MK-17": "FT-0 rod collar (holds the plate at the powder plane until the stage arrives)",
    "MK-18": "guide-laser target stand (S1), anodised 6061",
}

STATES = ("S1", "S2", "FT-0", "FT-1", "FT-1V")
TITLES = {
    "S1": "S1  optics bench: guide-laser and scanner checks",
    "S2": "S2  box closed round the beam: full power into a dump (Class 1)",
    "FT-0": "FT-0  single-track bench: heated plate, argon, hand-spread layers",
    "FT-1": "FT-1  purge-box LPBF: piston stage under the box, hopper-blade inside",
    "FT-1V": "FT-1V  the same cassette in a 12 in. vacuum cube, pump-purge",
}


# --------------------------------------------------------------------------------------------------
# Derived geometry
# --------------------------------------------------------------------------------------------------
def levels(state):
    """z levels for a state, in the world (bench-fixed) frame."""
    cube = state == "FT-1V"
    dz = P["dz_cube"] if cube else 0.0
    bf = P["bed_floor"]
    L = dict(dz=dz, cube=cube)
    L["floor_top"] = -bf + dz                                    # enclosure inside floor = deck underside
    L["deck_top"] = L["floor_top"] + P["deck_t"]
    L["under"] = -bf - P["box_t"]                                # enclosure underside (same in both: see dz_cube)
    L["gland_bot"] = L["under"] - P["gland_t"]
    if cube:
        c0 = L["floor_top"] - P["cube_boss"] + P["cube_frame"] / 2  # cube centre: boss top = floor_top
        L["cube_c"] = c0
        L["roof_in"] = c0 + P["cube_frame"] / 2 - P["cube_boss"]  # top plate boss underside
        L["roof_out"] = L["roof_in"] + P["cube_plate_t"]
    else:
        L["roof_in"] = L["floor_top"] + P["box_in"][2]           # box rim (gasket face)
        L["roof_out"] = L["roof_in"] + P["gasket"] + P["box_t"]
    L["lens_bot"] = P["lens_wd"] + dz
    L["lens_top"] = L["lens_bot"] + P["lens_l"]
    L["head_bot"] = L["lens_top"]
    # the rod: clamp top 3 mm under the gland at the plate's top position (cassette frame -> world)
    gland_bot_c = L["gland_bot"] - dz
    L["rod_vis"] = -3.0 - gland_bot_c - (P["pz_top"] - 5.0)       # visible rod below the heater plate
    return L


def beam_radius(z_rel):
    """Half-width of the scanned-beam envelope at height z_rel above the powder plane: the chief ray to the Ø40 field
    pivots near the top of the lens (est.), plus the converging beam's own half-width."""
    pivot = P["lens_wd"] + P["lens_l"]
    chief = P["field_d"] / 2 * (pivot - z_rel) / pivot
    return chief + P["beam_d"] / 2 * z_rel / P["lens_wd"] + 0.1


def beam_cone(state, z0=0.0, z1=None):
    L = levels(state)
    z1 = P["lens_wd"] if z1 is None else z1
    r0, r1 = beam_radius(z0), beam_radius(z1)
    s = cq.Solid.makeCone(r0, r1, z1 - z0, V(0, 0, z0 + L["dz"]), V(0, 0, 1))
    return s


# --------------------------------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------------------------------
def build(state="FT-1", pz=0.0, hx=None, lid_open=False):
    """Parts for a state. pz: substrate top (0 = start of a build); hx: hopper centre x (None = right park)."""
    assert state in STATES, state
    L = levels(state)
    dz = L["dz"]
    i_state = STATES.index(state)
    has_box = state in ("S2", "FT-0", "FT-1")
    has_cassette = i_state >= STATES.index("FT-0")
    has_stages = state in ("FT-1", "FT-1V")
    if not has_stages:
        pz = 0.0
    hx = P["rc_travel"] / 2 if hx is None else hx
    parts: list[Part] = []

    def add(name, shape, color, pid="", sub="", group="", opacity=1.0):
        if shape is not None:
            parts.append(Part(name, shape, color, pid, sub, group, opacity))

    xc, yc = P["deck_c"]
    zb = P["bench_z"]
    h = 15.0                                          # half T-slot

    # ---------------- bench and frame (S1 on) ----------------
    add("Bench top", box(-860, 600, -360, 430, zb - 40, zb), C["wood"], "", "bench", opacity=1.0)
    ry = (yc - 115.0, yc + 115.0)                     # rails along X
    ux = (xc - 260.0, xc + 260.0)                     # gantry upright centres
    z_rail_top = L["under"]                           # support rails carry the enclosure (same height for both)
    frame = []
    for y in ry:
        frame.append(tslot((xc - 290, y, zb + h), "x", 580))              # base rails
        frame.append(tslot((xc - 290, y, z_rail_top - h), "x", 580))      # support rails
    for x in (xc - 275, xc + 275):
        frame.append(tslot((x, ry[0] + h, zb + h), "y", ry[1] - ry[0] - 2 * h))
        for y in ry:
            frame.append(tslot((x, y, zb + 2 * h), "z", z_rail_top - zb - 4 * h))
    add("T-slot base and support rails", comp(frame), C["tslot"], "E4", "frame")
    # gantry: two uprights at y = yc + 115 (on the base rail), tall enough for the cube; a cross-beam carrying the head
    # plate, clamped at the height that puts the lens its working distance above the bed (21 mm higher for the cube)
    z_beam = L["head_bot"] + h                         # cross-beam centre: its underside on the head plate top
    z_up_top = P["lens_wd"] + P["dz_cube"] + P["lens_l"] + 60.0
    ups = [tslot((x, ry[1], z_rail_top), "z", z_up_top - z_rail_top) for x in ux]
    add("Gantry uprights", comp(ups), C["tslot"], "E4", "frame")
    add("Gantry cross-beam (clamped at the lens height)", tslot((ux[0] + h, ry[1], z_beam), "x", ux[1] - ux[0] - 2 * h),
        C["tslot"], "E4", "frame")

    # ---------------- optics (S1 on): head plate, hurrySCAN 25, lens, collimator, fibre, laser ----------------
    hb = L["head_bot"]
    hp = box(-100, 100, -90, ry[1] + h, hb - 12, hb).cut(cyl(P["lens_d"] / 2 + 3, (0, 0, hb - 13), "z", 14))
    add("Scan-head plate (MK-09)", hp, C["alu"], "MK-09", "optics")
    hw, hd, hh = P["head"]
    head = box(-hw / 2, hw / 2, -hd / 2, hd / 2, hb, hb + hh)
    head = head.fuse(cyl(18, (-hw / 2 - 12, 0, hb + P["head_in_z"]), "x", 12))       # input port
    add("SCANLAB hurrySCAN 25 (envelope)", head, C["head"], "L3", "optics")
    lens = cyl(P["lens_d"] / 2, (0, 0, L["lens_bot"]), "z", P["lens_l"] - 4).fuse(
        cyl(P["lens_d"] / 2 - 18, (0, 0, L["lens_top"] - 4), "z", 4))
    add("f-theta lens f = 254 mm (envelope)", lens, C["lens"], "L4", "optics")
    zc_in = hb + P["head_in_z"]
    coll = cyl(20, (-hw / 2 - 12 - 110, 0, zc_in), "x", 110)
    add("Collimator (L2 if the fibre has none)", coll, C["ss"], "L2", "optics")
    las = box(-800, -350, -170, 390, zb, zb + 175)
    las = las.fuse(box(-800, -350, -170, -150, zb + 15, zb + 160))
    add("IPG YLR-400-SM-EOS (envelope, est.)", las, C["laser"], "L1", "optics")
    fib = polyline_pipe([(-420, 120, zb + 172), (-420, 120, zb + 260), (-390, 70, zc_in + 50),
                         (-320, 20, zc_in + 20), (-hw / 2 - 12 - 110, 0, zc_in)], 3.0)
    add("Process fibre", fib, C["fiber"], "L1", "optics")
    add("PC with the RTC5 (tower, est.)", box(420, 590, -20, 400, zb, zb + 380), C["black"], "C1", "bench")
    add("+-15 V supply for the head (DIN, est.)", box(ux[1] - 15 - 60, ux[1] - 15, ry[1] - 15 - 30, ry[1] - 15,
                                                     hb - 120, hb - 30), C["alu_dark"], "L6", "optics")

    # ---------------- S1: target on the deck plate, the deck on the support rails ----------------
    deck_x0, deck_x1 = xc - P["deck"][0] / 2, xc + P["deck"][0] / 2
    deck_y0, deck_y1 = yc - P["deck"][1] / 2, yc + P["deck"][1] / 2
    deck_z0 = L["floor_top"] if has_box or state == "FT-1V" else z_rail_top
    deck = box(deck_x0, deck_x1, deck_y0, deck_y1, deck_z0, deck_z0 + P["deck_t"])
    deck = deck.cut(cyl(10.0, (0, 0, deck_z0 - 1), "z", P["deck_t"] + 2))
    deck = deck.cut(box(P["ovf_x"][0] - 2, 62, -26, 26, deck_z0 - 1, deck_z0 + P["deck_t"] + 1))
    add("Deck plate (MK-01)", deck, C["alu"], "MK-01", "cassette")
    if state == "S1":
        st = box(-30, 30, -30, 30, deck_z0 + P["deck_t"], -3.0)
        add("Guide-laser target stand (MK-18)", st, C["alu_dark"], "MK-18", "cassette")
        add("Anodised target, 80 x 80 x 3 mm", box(-40, 40, -40, 40, -3.0, 0.0), C["target"], "MK-18", "cassette")
    if state == "S2":
        d = cyl(40, (0, 0, L["deck_top"]), "z", 50).cut(cyl(12, (0, 0, L["deck_top"] + 30), "z", 21))
        add("Water-cooled beam dump, 500 W (Thorlabs LB2L/M class, envelope)", d, C["black"], "L9", "cassette")
        w = polyline_pipe([(30, 25, L["deck_top"] + 25), (90, 60, L["deck_top"] + 20),
                           (xc + P["box_in"][0] / 2 - 5, 60, L["deck_top"] + 20)], 3.0, smooth=True)
        add("Dump water lines", w, C["water"], "L9", "cassette")

    # ---------------- enclosure: the box (S2, FT-0, FT-1) ----------------
    bx, by, bz = P["box_in"]
    t = P["box_t"]
    x0, x1, y0, y1 = xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2
    if has_box:
        z0 = L["floor_top"]
        body = box(x0 - t, x1 + t, y0 - t, y1 + t, z0 - t, z0 + bz).cut(box(x0, x1, y0, y1, z0, z0 + bz + 1))
        body = body.cut(cyl(10.0, (0, 0, z0 - t - 1), "z", t + 2))                    # rod hole
        for p0, ax in (((x0 - t - 1, -60.0, 4.0), "x"), ((x1 - 1, 47.0, 5.0), "x")):
            body = body.cut(cyl(6.5, p0, ax, t + 2))                                     # gas bulkheads
        add("304 NEMA 4X box, 16 x 12 x 8 in. (body)", body, C["ss"], "E1", "enclosure", opacity=0.35)
        zr = L["roof_in"]
        gk = box(x0 - t, x1 + t, y0 - t, y1 + t, zr, zr + P["gasket"]).cut(
            box(x0 + 6, x1 - 6, y0 + 6, y1 - 6, zr - 1, zr + 2))
        add("Lid gasket, FKM cord", gk, C["rubber"], "E1", "enclosure")
        lid_z0 = zr + P["gasket"]
        lid = box(x0 - t - 3, x1 + t + 3, y0 - t - 3, y1 + t + 3, lid_z0, lid_z0 + t)
        sk = box(x0 - t - 3, x1 + t + 3, y0 - t - 3, y1 + t + 3, lid_z0 - 15, lid_z0).cut(
            box(x0 - t - 1, x1 + t + 1, y0 - t - 1, y1 + t + 1, lid_z0 - 16, lid_z0 + 1))
        lid = lid.fuse(sk).cut(cyl(26.5, (0, 0, lid_z0 - 1), "z", t + 2))
        add("Box lid (the door), window bore", lid, C["ss"], "E1", "enclosure", opacity=0.35)
        add("Continuous hinge", cyl(4.0, (x0 - t - 3, y1 + t + 7, lid_z0 + 1), "x", bx + 2 * t + 6), C["ss_dark"], "E1",
            "enclosure")
        cl = []
        for (cx_, cy_) in ((xc - 120, y0 - t - 9), (xc + 120, y0 - t - 9)):
            cl.append(box(cx_ - 12, cx_ + 12, cy_ - 6, cy_ + 6, lid_z0 - 40, lid_z0 - 16))
        for x_ in (x0 - t - 9, x1 + t + 9):
            cl.append(box(x_ - 6, x_ + 6, yc - 12, yc + 12, lid_z0 - 40, lid_z0 - 16))
        add("Lid clamps (4)", comp(cl), C["ss_dark"], "E1", "enclosure")
        # window stack on the thin lid: inner clamp ring, window ring, window, retaining flange, cover slide
        top = lid_z0 + t
        add("Inner clamp ring (MK-02)", tube(50, 22, (0, 0, lid_z0 - 6), "z", 6), C["alu"], "MK-02", "enclosure")
        win_ring_z = top
    else:
        win_ring_z = L["roof_out"] if state == "FT-1V" else None

    # ---------------- enclosure: the cube (FT-1V) ----------------
    if state == "FT-1V":
        F, pt, bs, op = P["cube_frame"], P["cube_plate_t"], P["cube_boss"], P["cube_open"]
        cz = L["cube_c"]
        fr = box(xc - F / 2, xc + F / 2, yc - F / 2, yc + F / 2, cz - F / 2, cz + F / 2)
        for ax in ("x", "y", "z"):
            dx_, dy_, dz_ = ((F + 2, op, op) if ax == "x" else (op, F + 2, op) if ax == "y" else (op, op, F + 2))
            fr = fr.cut(box(xc - dx_ / 2, xc + dx_ / 2, yc - dy_ / 2, yc + dy_ / 2, cz - dz_ / 2, cz + dz_ / 2))
        add("Ideal Vacuum 12 in. cube frame P107540", fr, C["cube"], "E2", "enclosure", opacity=0.45)
        pw, bw = P["cube_plate"], op - 2.0

        def plate(axis, sign, name, pid, holes=(), op_=0.45):
            body = box(-pw / 2, pw / 2, -pw / 2, pw / 2, 0, pt - bs).fuse(box(-bw / 2, bw / 2, -bw / 2, bw / 2, -bs, 0))
            for (hx_, hy_, hr) in holes:
                body = body.cut(cyl(hr, (hx_, hy_, -bs - 1), "z", pt + 2))
            # local z = outward normal; boss toward the inside. Place on the face.
            if axis == "z":
                sh = body if sign > 0 else body.rotate(V(0, 0, 0), V(1, 0, 0), 180)
                sh = sh.translate(V(xc, yc, cz + sign * F / 2))
            elif axis == "x":
                sh = body.rotate(V(0, 0, 0), V(0, 1, 0), 90 * sign).translate(V(xc + sign * F / 2, yc, cz))
            else:
                sh = body.rotate(V(0, 0, 0), V(1, 0, 0), -90 * sign).translate(V(xc, yc + sign * F / 2, cz))
            add(name, sh, C["cube"], pid, "enclosure", opacity=op_)

        plate("z", +1, "Cube top plate, bored for the window ring (MK-13)", "MK-13", holes=((-xc, -yc, 26.5),))
        plate("z", -1, "Cube bottom plate, bored for the rod gland (MK-14)", "MK-14", holes=((-xc, yc, 10.0),))
        plate("y", -1, "Cube front plate = door (hinge kit P106868)", "E2")
        plate("y", +1, "Cube back plate (KF-25 feedthroughs)", "E2")
        plate("x", -1, "Cube left plate (pump and gauge ports)", "E2")
        plate("x", +1, "Cube right plate (argon in, exhaust, vent)", "E2")
        hinge = cyl(5.0, (xc - pw / 2, yc - F / 2 - (pt - bs) - 6, cz - pw / 2 + 20), "x", pw)
        add("Door hinges (hinge kit)", hinge, C["ss_dark"], "E2", "enclosure")
        # KF-25 ports
        kfs = []
        sx = xc - F / 2 - (pt - bs)
        for (yy, zz) in ((yc - 60, cz - 60), (yc + 60, cz - 60)):
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(0, 1, 0), -90).translate(V(sx - 30, yy, zz)))
        sx1 = xc + F / 2 + (pt - bs)
        for (yy, zz) in ((yc - 60, cz - 60), (yc + 60, cz - 60)):
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(0, 1, 0), 90).translate(V(sx1 + 30, yy, zz)))
        sy1 = yc + F / 2 + (pt - bs)
        for xx in (xc - 60, xc + 60):
            kfs.append(kf_stub(25, 30).rotate(V(0, 0, 0), V(1, 0, 0), -90).translate(V(xx, sy1 + 30, cz - 60)))
        add("KF-25 ports: pump, Pirani, argon, exhaust, 2 electrical feedthroughs", comp(kfs), C["ss"], "E3", "enclosure")
        pump = box(-820, -440, -345, -185, zb, zb + 230)
        add("Rotary-vane pump (McMaster 4396K21 class, envelope est.)", pump, C["blue"], "E3", "gas")
        hose = polyline_pipe([(sx - 30, yc - 60, cz - 60), (sx - 120, yc - 90, cz - 90), (-470, -250, zb + 250),
                              (-560, -250, zb + 230)], 13.0)
        add("KF-25 pump hose and valve", hose, C["hose"], "E3", "gas")

    # ---------------- window stack (S2 on) ----------------
    if win_ring_z is not None:
        z = win_ring_z
        ring = tube(50, 22, (0, 0, z), "z", 10).cut(cyl(P["window_d"] / 2 + 0.25, (0, 0, z + 2), "z", 9))
        add("Window ring (MK-02)", ring, C["alu"], "MK-02", "enclosure")
        add("Window, Ø50.8 x 9.53 fused silica, 1064 V-coat", cyl(P["window_d"] / 2, (0, 0, z + 2), "z", P["window_t"]),
            C["glass"], "L8", "enclosure", opacity=0.5)
        fl = tube(50, 22, (0, 0, z + 10), "z", 6).cut(cyl(P["window_d"] / 2 + 0.25, (0, 0, z + 10 - 0.1), "z", 1.8))
        add("Window retaining flange (MK-02)", fl, C["alu"], "MK-02", "enclosure")
        cs_top = (L["roof_in"] - (6.0 if has_box else 0.0))
        holder = tube(35, 20, (0, 0, cs_top - 10), "z", 10).cut(cyl(25.3, (0, 0, cs_top - 5.6), "z", 1.2))
        holder = holder.cut(box(0, 40, -25.3, 25.3, cs_top - 5.6, cs_top - 4.4))      # slide goes in from +x
        add("Cover-slide holder (MK-02)", holder, C["alu"], "MK-02", "enclosure")
        add("Cover slide, Ø50 x 1 mm", cyl(25, (0, 0, cs_top - 5.5), "z", 1.0), C["glass"], "L8", "enclosure", opacity=0.5)
        # beam tube from the flange to a collar round the lens
        t0 = z + 16
        col_z0 = L["lens_bot"] - 14
        bt = tube(30, 27, (0, 0, t0), "z", col_z0 - 6 - t0).fuse(tube(50, 27, (0, 0, t0), "z", 6))
        bt = bt.fuse(tube(62, 27, (0, 0, col_z0 - 6), "z", 6)).fuse(tube(62, P["lens_d"] / 2 + 1, (0, 0, col_z0), "z", 26))
        long = state != "FT-1V"
        add("Beam tube, long, with lens collar (MK-10)" if long else "Beam tube, short, with lens collar (MK-10)",
            bt, C["alu_dark"], "MK-10", "enclosure", opacity=0.7)
        add("Beam-tube interlock switch", box(62, 86, -10, 10, col_z0 + 4, col_z0 + 22), C["yellow"], "S1", "safety")

    # ---------------- cassette (FT-0 on) ----------------
    if has_cassette:
        z0 = L["floor_top"] + P["deck_t"]                                  # deck top
        bw_, bd_, bh_ = P["well"]
        zb0 = z0 + P["so_l"]                                               # well block bottom
        zbed = zb0 + bh_                                                   # powder plane (= dz)
        sos = [cyl(P["so_d"] / 2, (sx_, sy_, z0), "z", P["so_l"]) for sx_ in (-P["so_xy"], P["so_xy"])
               for sy_ in (-P["so_xy"], P["so_xy"])]
        add("Macor standoffs under the well block (4)", comp(sos), C["macor"], "H4", "cassette")
        blk = box(-bw_ / 2, bw_ / 2, -bd_ / 2, bd_ / 2, zb0, zbed).cut(cyl(P["bore"] / 2, (0, 0, zb0 - 1), "z", bh_ + 2))
        blk = blk.cut(box(P["ovf_x"][0], P["ovf_x"][1], -P["ovf_y"], P["ovf_y"], zb0 - 1, zbed + 1))
        for sy_ in (-30.0, 30.0):
            blk = blk.cut(cyl(P["heater_d"] / 2 + 0.05, (-bw_ / 2 - 1, sy_, zb0 + bh_ / 2), "x", 41))
        blk = blk.cut(cyl(0.8, (-30, bd_ / 2 + 1, zb0 + bh_ / 2), "-y", 31))
        add("Well block, Ø40.00 bore (MK-03)", blk, C["hot"], "MK-03", "cassette")
        if has_stages:
            hs = [cyl(P["heater_d"] / 2, (-bw_ / 2 - 2, sy_, zb0 + bh_ / 2), "x", 40) for sy_ in (-30.0, 30.0)]
            add("Well-block heaters, 2 x 50 W", comp(hs), C["copper"], "H1", "cassette")
        # plate stack: substrate on the heater plate on the rod (moves with pz)
        zt = zbed + pz
        sub = cyl(P["plate_d"] / 2, (0, 0, zt - P["sub_t"]), "z", P["sub_t"])
        for k in range(3):
            a = math.radians(90 + 120 * k)
            p_ = (17.1 * math.cos(a), 17.1 * math.sin(a))
            sub = sub.cut(cyl(1.1, (p_[0], p_[1], zt - P["sub_t"] - 1), "z", P["sub_t"] + 2))
            sub = sub.cut(cq.Solid.makeCone(1.1, 2.1, 1.0, V(p_[0], p_[1], zt - 1.0), V(0, 0, 1)))
        add("Substrate disc Ø39.8 x 6 (MK-05)", sub, C["sub"], "MK-05", "cassette", "piston")
        hp_z0 = zt - P["sub_t"] - P["hp_t"]
        hpl = cyl(P["plate_d"] / 2, (0, 0, hp_z0), "z", P["hp_t"])
        hpl = hpl.cut(tube(P["plate_d"] / 2 + 1, P["plate_d"] / 2 - P["rope"], (0, 0, zt - P["sub_t"] - 7), "z", P["rope"]))
        hpl = hpl.cut(cyl(P["rod_od"] / 2 + 0.05, (0, 0, hp_z0 - 1), "z", P["socket"] + 1))
        for k in range(3):
            a = math.radians(30 + 120 * k)
            p_ = (P["heater_r"] * math.cos(a), P["heater_r"] * math.sin(a))
            r_ = P["heater_d"] / 2 + 0.05 if k < 2 else 0.8
            hpl = hpl.cut(cyl(r_, (p_[0], p_[1], hp_z0 - 1), "z", P["heater_l"] + 1.5))
        add("Heater plate Ø39.8 x 28 (MK-04)", hpl, C["hot"], "MK-04", "cassette", "piston")
        rope = tube(P["plate_d"] / 2 + 0.08, P["plate_d"] / 2 - P["rope"], (0, 0, zt - P["sub_t"] - 7), "z", P["rope"])
        add("Fibreglass rope wiper", rope, C["white"], "H4", "cassette", "piston")
        ph = []
        for k in range(2):
            a = math.radians(30 + 120 * k)
            ph.append(cyl(P["heater_d"] / 2, (P["heater_r"] * math.cos(a), P["heater_r"] * math.sin(a), hp_z0),
                          "z", P["heater_l"]))
        add("Plate heaters, 2 x 1/4 x 1 in.", comp(ph), C["copper"], "H1", "cassette", "piston")
        # rod: thin-wall tube from the socket down through the deck, floor and gland; wires run inside it
        rod_vis = L["rod_vis"]
        rod_top = hp_z0 + P["socket"]
        rod_bot = hp_z0 - rod_vis
        rod = tube(P["rod_od"] / 2, P["rod_od"] / 2 - P["rod_wall"], (0, 0, rod_bot), "z", rod_top - rod_bot)
        add("Piston rod, long, for the cube (MK-06)" if state == "FT-1V" else "Piston rod (MK-06)", rod, C["ss"],
            "MK-06", "drive", "piston")
        gl = box(-30, 30, -30, 30, L["gland_bot"], L["under"]).cut(cyl(P["rod_od"] / 2 + 0.1, (0, 0, L["gland_bot"] - 1),
                                                                         "z", P["gland_t"] + 2))
        add("Rod gland plate, 2 O-rings (MK-07)", gl, C["ss_dark"], "MK-07", "drive")
        if state == "FT-0":
            coll = tube(15, P["rod_od"] / 2, (0, 0, z0), "z", 10).cut(box(-0.75, 0.75, 4, 16, z0 - 1, z0 + 11))
            add("FT-0 rod collar (MK-17)", coll, C["black"], "MK-17", "cassette")
        # overflow cup (in the deck pocket, on the floor)
        cup = box(P["ovf_x"][0] - 0.5, P["ovf_x"][1] + 0.5, -24, 24, L["floor_top"], zb0 - 1.0)
        cup = cup.cut(box(P["ovf_x"][0], P["ovf_x"][1], -23.5, 23.5, L["floor_top"] + 1, zb0))
        add("Overflow cup (MK-16)", cup, C["ss"], "MK-16", "cassette")
        # gas: slot nozzle (front) and exhaust collector (back) on the block top
        sw, sh_ = P["nozzle_slot"]
        nz = box(-27.5, 27.5, -46, -27, zbed, zbed + 8).cut(box(-sw / 2, sw / 2, -28, -26.5, zbed + 2, zbed + 2 + sh_))
        nz = nz.fuse(cyl(5, (0, -46, zbed + 4), "-y", 6))
        add("Slot nozzle 45 x 4 mm (MK-11)", nz, C["ss"], "MK-11", "gas")
        ex = box(-30, 30, 27, 40, zbed, zbed + 10).cut(box(-25, 25, 26.5, 28, zbed + 2, zbed + 8))
        add("Exhaust collector (MK-11)", ex, C["ss"], "MK-11", "gas")
        x_wall_in = (xc - P["box_in"][0] / 2) if has_box else (xc - P["cube_in"] / 2)
        x_wall_out = (xc + P["box_in"][0] / 2) if has_box else (xc + P["cube_in"] / 2)
        feed = polyline_pipe([(0, -52, zbed + 4), (0, -60, zbed + 4), (-40, -60, zbed + 4), (x_wall_in + 2, -60, zbed + 4)],
                             3.2, smooth=False)
        add("Argon feed tube to the nozzle", feed, C["gas"], "G3", "gas")
        exh = polyline_pipe([(0, 40, zbed + 5), (0, 47, zbed + 5), (40, 47, zbed + 5), (x_wall_out - 2, 47, zbed + 5)],
                            6.0, smooth=False)
        add("Exhaust hose to the HEPA", exh, C["gas"], "G3", "gas")
        if state == "FT-0":
            app = box(-80, -55, -35, 35, L["deck_top"], L["deck_top"] + 18).fuse(
                cyl(6, (-67.5, -35, L["deck_top"] + 24), "z", 14)).fuse(cyl(6, (-67.5, 35, L["deck_top"] + 24), "z", 14))
            app = app.translate(V(-35, 0, 0))
            add("Film applicator, parked (M4)", app, C["ss_dark"], "M4", "cassette")

    # ---------------- recoater (FT-1, FT-1V) ----------------
    if has_stages:
        z0 = L["floor_top"] + P["deck_t"]
        zbed = z0 + P["so_l"] + P["well"][2]
        yr, rw, rh = P["rc_y"], P["rc_w"], P["rc_h"]
        rl, ml = P["rc_rail_l"], P["rc_motor_l"]
        st = box(-rl / 2, rl / 2, yr - rw / 2, yr + rw / 2, z0, z0 + rh)
        st = st.fuse(box(-rl / 2 - ml, -rl / 2, yr - rw / 2 + 5, yr + rw / 2 - 5, z0, z0 + rh + 4))
        add("Zaber X-LSQ075B-E01 recoater stage (body est.)", st, C["zaber"], "M1b", "recoater")
        cl_, cw_, ct_ = P["rc_car"]
        car = box(hx - cl_ / 2, hx + cl_ / 2, yr - cw_ / 2, yr + cw_ / 2, z0 + rh, z0 + rh + ct_)
        add("X-LSQ carriage", car, C["zaber_top"], "M1b", "recoater", "recoater")
        ztop_car = z0 + rh + ct_
        hl, hw_, hh_ = P["hopper"]
        arm_z0 = zbed + hh_ - 8
        brk = box(hx - 20, hx + 20, yr - 24, yr - 16, ztop_car, arm_z0 + 8)
        arm = box(hx - 8, hx + 8, hw_ / 2, yr - 16, arm_z0, arm_z0 + 8)
        add("Carriage bracket and arm (MK-08)", comp([brk, arm]), C["alu"], "MK-08", "recoater", "recoater")
        sh = box(-rl / 2 - ml - 2, rl / 2 + 2, yr - rw / 2 - 3, yr + rw / 2 + 3, ztop_car + 3, ztop_car + 4)
        sh = sh.cut(box(-rl / 2 + 2, rl / 2 - 2, yr - 26, yr - 14, ztop_car + 2, ztop_car + 5))
        sh = sh.fuse(box(-rl / 2 - ml - 2, rl / 2 + 2, yr - rw / 2 - 4, yr - rw / 2 - 3, z0, ztop_car + 4))
        add("Stage shield (MK-12)", sh, C["ss"], "MK-12", "recoater", opacity=0.55)
        hop = (cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (hl / 2, hh_), (-hl / 2, hh_)]).close()
               .extrude(hw_).val())
        hop = hop.fuse(cq.Workplane("XZ").polyline([(-hl / 2, 6), (hl / 2, 6), (1.5, 2.0), (-1.5, 2.0)]).close()
                       .extrude(hw_).val())
        hop = hop.cut(box(-hl / 2 + 0.8, hl / 2 - 0.8, -hw_ + 0.8, -0.8, 7, hh_ + 1))
        hop = hop.translate(V(hx, hw_ / 2, zbed))
        add("Hopper, ~30 cm3 (MK-08)", hop, C["ss"], "MK-08", "recoater", "recoater")
        cord = cyl(P["cord_d"] / 2, (hx - hl / 2 - 2.0, -hw_ / 2, zbed + P["cord_d"] / 2), "y", hw_)
        add("Silicone-cord blade, 3 mm", cord, C["silicone"], "M3", "recoater", "recoater")
        clamp = box(hx - hl / 2 - 4, hx - hl / 2, -hw_ / 2, hw_ / 2, zbed + P["cord_d"], zbed + 12)
        add("Cord clamp (MK-08)", clamp, C["ss_dark"], "MK-08", "recoater", "recoater")
        vib = cyl(5, (hx, hw_ / 2 + 4, arm_z0 + 8), "y", 22)
        add("Vibration motor", vib, C["black"], "M3", "recoater", "recoater")

    # ---------------- piston drive (FT-1, FT-1V) ----------------
    if has_stages:
        s = pz - P["pz_bot"]                                         # stage stroke 0..20
        zt = (L["floor_top"] + P["deck_t"] + P["so_l"] + P["well"][2]) + pz
        rod_bot = zt - P["sub_t"] - P["hp_t"] - L["rod_vis"]
        plat_top = rod_bot - 2.0
        base = plat_top - s - P["vs_h"]
        fx, fy = P["vs_foot"]
        px_, py_, pt_ = P["vs_plat"]
        body = box(-fx / 2, fx / 2, -fy / 2, fy / 2, base, base + P["vs_h"] - pt_ - 2)
        add("Zaber X-VSR20A-E01 piston stage (footprint est.)", body, C["zaber"], "M2", "drive")
        plat = box(-px_ / 2, px_ / 2, -py_ / 2, py_ / 2, plat_top - pt_, plat_top)
        add("X-VSR20A platform", plat, C["zaber_top"], "M2", "drive", "piston")
        col = box(-25, 25, -25, 25, base + P["vs_h"] - pt_ - 2, plat_top - pt_)
        add("X-VSR20A lift column", col, C["zaber_top"], "M2", "drive", "piston")
        clamp = box(-15, 15, -15, 15, plat_top, plat_top + P["clamp_h"]).cut(
            cyl(P["rod_od"] / 2 + 0.05, (0, 0, plat_top - 1), "z", P["clamp_h"] + 2)).cut(
            box(-2, 2, 0, 16, plat_top + 2, plat_top + 10))
        add("Rod clamp (MK-15)", clamp, C["alu_dark"], "MK-15", "drive", "piston")
        bp = box(-90, 90, ry[0] - h, ry[1] + h, zb + 2 * h, zb + 2 * h + 10)
        riser = box(-fx / 2, fx / 2, -fy / 2, fy / 2, zb + 2 * h + 10, base)
        add("Piston-stage bracket plate and riser (MK-15)", comp([bp, riser]), C["alu"], "MK-15", "drive")

    # ---------------- gas, O2 and safety outside (FT-0 on for gas; S2 on for safety) ----------------
    if i_state >= STATES.index("S2"):
        add("Safety relay box: E-stop, key switch (S1)", box(330, 470, -330, -230, zb, zb + 70), C["yellow"], "S1",
            "safety")
        add("E-stop", cyl(18, (360, -280, zb + 70), "z", 22), C["red"], "S1", "safety")
        add("Key switch", cyl(10, (420, -280, zb + 70), "z", 14), C["black"], "S1", "safety")
        add("Emission lamp", cyl(14, (ux[1], ry[1], P["lens_wd"] + P["dz_cube"] + P["lens_l"] + 60.0), "z", 40), C["red"], "S1", "safety")
    if has_box:
        z_lid = L["roof_in"] + P["gasket"]
        sw_ = []
        for xx in (xc - 160, xc + 160):
            sw_.append(box(xx - 18, xx + 18, yc - by / 2 - t - 16, yc - by / 2 - t, z_lid - 48, z_lid - 22))
        add("Coded lid switches (2)", comp(sw_), C["yellow"], "S1", "safety")
    if state == "FT-1V":
        F = P["cube_frame"]
        sw_ = []
        for xx in (xc - 110, xc + 110):
            fz_ = yc - F / 2 - (P["cube_plate_t"] - P["cube_boss"])
            sw_.append(box(xx - 18, xx + 18, fz_ - 16, fz_, L["cube_c"] + 60, L["cube_c"] + 86))
        add("Coded lid switches (2)", comp(sw_), C["yellow"], "S1", "safety")
    if has_cassette:
        add("Argon regulator and solenoid valve panel", box(-330, -230, -330, -250, zb, zb + 160), C["alu_dark"], "G1",
            "gas")
        add("Exhaust HEPA housing and check valve", cyl(45, (300, -170, zb), "z", 190), C["white"], "G4", "gas")
        add("Trace O2 analyzer (Alpha Omega 3000, envelope)", box(250, 400, 250, 410, zb, zb + 140),
            C["white"], "G5", "gas")
    if state == "FT-1":
        fx_ = xc - P["box_in"][0] / 2 - P["box_t"]
        add("120 mm fan blowing on the enclosure", box(fx_ - 30, fx_ - 5, yc - 60, yc + 60, -50, 70), C["black"], "E4",
            "enclosure")
    if state == "FT-1V":
        fy_ = yc + P["cube_frame"] / 2 + P["cube_plate_t"] - P["cube_boss"]
        cz_ = L["cube_c"]
        add("120 mm fan blowing on the enclosure", box(xc - 60, xc + 60, fy_ + 5, fy_ + 30, cz_ - 5, cz_ + 115), C["black"],
            "E4", "enclosure")
    return parts


def bom_by_state():
    """{state: {part name: pid}} for the progression tables."""
    out = {}
    for s in STATES:
        out[s] = {p.name: p.pid for p in build(s)}
    return out


def diff_states(a, b, tol=0.5):
    """Parts added, moved and removed going from state a to state b (by name; moved = bounding box shifted)."""
    def bbs(parts):
        out = {}
        for p in parts:
            bb = p.shape.BoundingBox()
            out[p.name] = (p.pid, (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
        return out
    pa, pb = bbs(build(a)), bbs(build(b))
    added = [(n, pb[n][0]) for n in pb if n not in pa]
    removed = [(n, pa[n][0]) for n in pa if n not in pb]
    moved = [(n, pb[n][0]) for n in pb if n in pa and max(abs(x - y) for x, y in zip(pa[n][1], pb[n][1])) > tol]
    return dict(added=added, moved=moved, removed=removed, kept=len(pb) - len(added) - len(moved))


def to_assembly(parts, name):
    a = cq.Assembly(name=name)
    for i, p in enumerate(parts):
        r, g, b = (int(p.color[k:k + 2], 16) / 255 for k in (1, 3, 5))
        nm = "".join(ch if ch.isalnum() else "_" for ch in p.name)[:60] + f"_{i:03d}"
        a.add(p.shape, name=nm, color=cq.Color(r, g, b, p.opacity))
    return a


if __name__ == "__main__":
    import time
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for s in STATES:
        t0 = time.time()
        parts = build(s)
        print(f"{s}: {len(parts)} parts in {time.time() - t0:.1f} s")
        if "--no-export" not in sys.argv and s in ("FT-0", "FT-1", "FT-1V"):
            to_assembly(parts, s.replace("-", "_")).export(str(out / f"{s.lower()}.step"))
