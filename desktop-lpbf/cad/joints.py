"""Bolted and pinned joints of the low-profile desktop LPBF (issue #260, PR #266), with real McMaster-Carr parts.

lpbf_low.build() calls add_joints() last. For every joint this module
  1. places the real screws, pins, inserts and springs from fasteners.py (each a McMaster part number, recreated in
     CadQuery and checked against McMaster's own CAD by volume: verify_fasteners.py),
  2. cuts their holes into the parts they join: clearance holes (ISO 273 medium), counterbores, tapped holes drawn at
     the thread's nominal diameter (a cosmetic thread, so a screw in its tapped hole touches but does not overlap), and
     helical-insert holes drawn at the insert's installed OD,
  3. records where each fastener goes in REGISTRY, so the animation (render_build.py) drives the same screws.

Every joint is listed in JOINT_NOTES with the reason for its hardware, and in fasteners.csv-style rows (bom_rows()).
Hardware that the model does not draw yet (door hinges and latches, rack units, the gas module's units, the guard) is
listed in NOT_DRAWN with its McMaster part where one was chosen.

Local axial coordinate s along a fastener: s = 0 at its bearing plane (under the head), s > 0 toward the tip.
"""
from __future__ import annotations

import math

import cadquery as cq

import fasteners as FS
import module_params as MP
import modules_low as ML

V = cq.Vector

CLEAR = {2.5: 2.9, 3: 3.4, 4: 4.5, 5: 5.5, 6: 6.6, 8: 9.0}            # ISO 273 medium clearance holes
CBORE = {2.5: (5.0, 2.7), 3: (7.0, 3.4), 4: (8.0, 4.4), 5: (10.0, 5.4), 6: (11.0, 6.4)}  # counterbore dia, depth for ISO 4762
MATKEY = {"ss316": "ss316l", "ss188": "ss304", "ss302": "ss304", "steel": "steel", "steel_zn": "steel", "ni718": "steel"}

REGISTRY: dict[str, dict] = {}     # joint key -> dict(name, pn, items, group, tags, step, bom, extra=[(pn, items)])
CUTS: dict[str, list] = {}         # part-name prefix -> [(joint key, tool)] cut by the last add_joints() (the animation re-machines them)
_KEY = [""]
JOINT_NOTES: dict[str, str] = {}

NOT_DRAWN = [
    ("Door hinges (2 x McMaster 1151A87) to door and chamber", "the hinge's own countersunk holes; screws chosen when the hinge CAD replaces the drawn knuckles"),
    ("Draw latches (2 x 1807A61) and their strikes", "No. 10 screws per the latch's hole pattern; not drawn"),
    ("Camera adapter to lid (3 x M3), camera window retaining ring (3 x M2.5), drawer-latch receptacles", "not drawn"),
    ("Recoater carriage block to carriage (6709K12), ball nut (4566N401) to block, bearing housings, motor bracket", "M4 per the vendor hole patterns; not drawn"),
    ("Z actuator, carriage, arm and servo; recoater and dosing motors", "per the vendor drawings; not drawn"),
    ("Rack units", "standard M6 cage nuts and screws in the rack's EIA-310 holes; not drawn"),
    ("Gas module units (pump, blower, filter housing, O2 box, manifold) to their base plate", "per the vendor drawings; not drawn"),
    ("Laser guard frame and panels", "T-slot hardware as in BOM line S9; not drawn"),
    ("Galvo to the optics bridge, lens to galvo, camera and gauges", "per the vendor drawings / thread; not drawn"),
]


# ------------------------------------------------------------------------------------------------ catalogue lookups
def find(kind, d=None, L=None, **kw):
    """McMaster part number of the catalogue entry with this kind, thread size and length (and any other fields)."""
    hits = []
    for pn, c in FS.CATALOG.items():
        if c.get("kind") != kind:
            continue
        if d is not None and abs(float(c.get("d", -1)) - d) > 1e-6:
            continue
        if L is not None and abs(float(c.get("L", -1)) - L) > 1e-6:
            continue
        if any(c.get(k) != v for k, v in kw.items()):
            continue
        hits.append(pn)
    if not hits:
        raise KeyError(f"no {kind} d={d} L={L} {kw} in fasteners.CATALOG")
    return sorted(hits)[0]


def insert_od(pn):
    c = FS.CATALOG[pn]
    return float(c.get("od_installed", c["d"] + 1.3 * c["P"]))


# ------------------------------------------------------------------------------------------------ geometry helpers
def _pt(p0, n, s):
    return V(*p0) + V(*n) * s


def hole(p0, n, s0, s1, d):
    """Cylinder of diameter d along n from s0 to s1."""
    return cq.Solid.makeCylinder(d / 2.0, s1 - s0, _pt(p0, n, s0), V(*n))


def cone(p0, n, s0, s1, d0, d1):
    return cq.Solid.makeCone(d0 / 2.0, d1 / 2.0, s1 - s0, _pt(p0, n, s0), V(*n))


def slot(p0, n, s0, s1, d, half_len, radial):
    """Stadium of width d, elongated +/- half_len along `radial` (perpendicular to n): a radial slot for thermal growth."""
    r = V(*radial).normalized()
    a = hole(tuple(V(*p0) + r * half_len), n, s0, s1, d)
    b = hole(tuple(V(*p0) - r * half_len), n, s0, s1, d)
    pl = cq.Plane(origin=_pt(p0, n, s0), xDir=r, normal=V(*n))
    box = cq.Workplane(pl).rect(2 * half_len, d).extrude(s1 - s0).val()
    return a.fuse(b).fuse(box).clean()


def cut_parts(parts, prefix, tools, must=True):
    hit = [p for p in parts if p.name.startswith(prefix)]
    if not hit and must:
        raise KeyError(f"no part named '{prefix}...'")
    for p in hit:
        p.shape = p.shape.cut(*tools)
    CUTS.setdefault(prefix, []).extend((_KEY[0], t) for t in tools)
    return hit


def place_all(pn, items, detail=False):
    return cq.Compound.makeCompound([FS.place(pn, P, n, detail=detail) for P, n in items])


def add_fasteners(h, add, key, name, pn, items, step, bom, group="", tags=(), explode=(0, 0, 0), color=None, section=False):
    _KEY[0] = key
    c = FS.CATALOG[pn]
    kw = dict(group=group) if group else {}
    add(f"{name} ({len(items)} x McMaster {pn})", place_all(pn, items), color or h.C["steel"], step, explode,
        mat=MATKEY.get(c.get("mat", "ss316"), "ss316l"), mass_kg=len(items) * FS.mass_g(pn) / 1000.0, bom=bom, mcm=pn,
        tags=("fastener", key) + tuple(tags), section=section, **kw)
    REGISTRY.setdefault(key, dict(name=name, items=[], extra=[], step=step, group=group, tags=tuple(tags), bom=bom, pn=pn))
    if REGISTRY[key]["pn"] == pn and not REGISTRY[key]["items"]:
        REGISTRY[key]["items"] = list(items)
    else:
        REGISTRY[key]["extra"].append((pn, list(items)))


def locating_pins(h, parts, add, key, wall, flange, items, name, step, bom, explode):
    """Two Ø3 x 10 316 dowels (ISO 2338 m6, McMaster 93600A304) for a bolted flange (assembly.md patch 9): each item is the pin's outer
    end, 5 mm out from the wall face, and its axis into the wall. Pressed 5 mm into the wall (H7 hole... m6 pin: a light press made in
    the shop, not by the robot, assembly.md patch 4) and a slip hole 6 mm deep in the flange, so the arm that places the flange is
    also the arm that drives its screws."""
    _KEY[0] = key + "_pins"
    pn = find("dowel", 3, 10)
    cut_parts(parts, wall, [hole(p, n, 4.99, 10.5, 3.0) for p, n in items])
    cut_parts(parts, flange, [hole(p, n, -1.0, 5.01, 3.0) for p, n in items])
    add_fasteners(h, add, key + "_pins", f"{name}, Ø3 x 10 316 (pressed 5 mm into the wall, slip fit in the flange)", pn, items, step, bom, explode=explode)
    JOINT_NOTES[key + "_pins"] = ("Two Ø3 m6 dowels locate the flange on its wall (assembly.md patch 9), so one arm places it and drives its screws; "
                                  "the wall's two H7 holes are drilled and reamed in the setup that taps the flange's screw holes.")


def polar(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


# ------------------------------------------------------------------------------------------------ the joints
def add_joints(h, parts, add, module="M50"):
    REGISTRY.clear()
    CUTS.clear()
    P, C = h.P, h.C
    ix, iy, cx, cy = P["ix"], P["iy"], P["cx"], P["cy"]
    lz0, lz1 = P["lid_z0"], P["lid_z1"]
    zf = -P["floor"]
    zb0, zb1 = P["z_base0"], P["z_base1"]
    Z = (0.0, 0.0, 1.0)
    mZ = (0.0, 0.0, -1.0)

    # ---------------- 1. lid: 20 x M5 x 25 into M5 x 7.5 helical inserts in the chamber body ----------------
    _KEY[0] = "lid"
    pn, ins = find("shcs", 5, 25), find("insert", 5, 7.5)
    by = iy + 11.8                                 # midway between the lid O-ring gland and the outer wall: 1.2 mm each side
    items = []
    for x in (-140.0, -100.0, -60.0, -20.0, 20.0, 60.0, 100.0, 140.0):
        for y in (-by, by):
            xx = math.copysign(42.0, x) if (y < 0 and abs(x) < 40) else x     # clear of the cover-slide drawer slot
            items.append(((xx, y, lz1), mZ))
    for x in (-(ix + 11.8), ix + 11.8):
        for y in (-35.6, 35.6):
            items.append(((x, y, lz1), mZ))
    od = insert_od(ins)
    cut_parts(parts, "Chamber lid", [hole(p, n, -1, P["lid"] + 0.01, CLEAR[5]) for p, n in items])
    cut_parts(parts, "Process chamber body", [hole(p, n, P["lid"], P["lid"] + 7.5, od) for p, n in items] +
              [hole(p, n, P["lid"] + 7.5 - 0.01, P["lid"] + 10.5, 5.0) for p, n in items])
    add_fasteners(h, add, "lid", "Lid screws, M5 x 25 316 socket head", pn, items, 7, "G1", explode=(0, 0, 340))
    add_fasteners(h, add, "lid", "Lid screw helical inserts, M5 x 7.5 18-8, in the chamber body", ins,
                  [(tuple(_pt(p, n, P["lid"])), n) for p, n in items], 5, "G1", explode=(0, 0, 260))
    JOINT_NOTES["lid"] = ("Opened only for maintenance, and it must squeeze the lid O-ring evenly and hold it at vacuum, so "
                          "screws are right here. Inserts because the lid comes off many times over the machine's life and "
                          "6061 threads wear; 1.2 mm of metal each side between the gland and the outer wall.")

    # ---------------- 1b. floor plate to frame: 18 x M4 x 16 up into tapped holes in the frame's skirt; 2 dowels ----------------
    # chamber-construction.md: screws on the skirt's centre line (12 mm outside the inner faces, outboard of the floor O-ring), heads in
    # 8 mm deep U-notches in the plate's underside so they clear the under-floor mounts (outlet plenum, Z flange) and stay reachable.
    # Kept clear of: the door sill (front: tapped holes end at z +5.5, sill at +8), the inlet slot (back, |x| < 64), the inlet-plenum
    # inserts (x +/-71), the Z-flange inserts (x -33/40/94), the through-beam (y 0), the legs (corners) and the door-hinge blocks.
    _KEY[0] = "floor"
    FR = h.FRAME
    sk, bt, nd = FR["skirt"], FR["bolt_t"], FR["notch"]
    xb, yb = ix + bt, iy + bt
    pts = ([(x, -yb, (0.0, -1.0)) for x in (-116.0, -66.0, -22.0, 22.0, 66.0, 116.0)] + [(x, yb, (0.0, 1.0)) for x in (-110.0, -82.0, 82.0, 110.0)]
           + [(sx * xb, y, (sx, 0.0)) for sx in (-1.0, 1.0) for y in (-62.0, -20.0, 20.0, 62.0)])
    zn = zf + nd                                              # -12: the head bears on the notch's roof
    pn4f = find("shcs", 4, 16)
    Ls = float(FS.CATALOG[pn4f]["L"])
    items = [((x, y, zn), Z) for x, y, _ in pts]
    notches = []
    for x, y, (ox_, oy_) in pts:
        notches.append(hole((x, y, zn), Z, -nd - 1.0, 0.0, 8.0))
        if ox_:
            x0_ = x if ox_ > 0 else x - 10.0
            notches.append(cq.Solid.makeBox(10.0, 8.0, nd + 1.0, V(x0_, y - 4.0, zf - 1.0)))
        else:
            y0_ = y if oy_ > 0 else y - 10.0
            notches.append(cq.Solid.makeBox(8.0, 10.0, nd + 1.0, V(x - 4.0, y0_, zf - 1.0)))
    cut_parts(parts, "Chamber floor plate", notches + [hole(p, n, -0.01, (-FR["pad"] - zn) + 0.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Process chamber body", [hole(p, n, (-sk - zn) - 0.01, Ls + 1.5, 4.0) for p, n in items])
    add_fasteners(h, add, "floor", "Floor-plate screws, M4 x 16 316, up through U-notches in the plate's edge into tapped holes in the frame's skirt",
                  pn4f, items, 5, "G1", explode=(0, 0, -150))
    _KEY[0] = "floor_dowels"                                  # so joints.CUTS files the dowel holes under their own key
    dw = find("dowel", 6, 20)
    zt = -sk + 9.9                                            # dowel top, 9.9 mm up in the frame; 10 mm pressed into the plate
    ditems = [((sx * 148.2, sx * 103.2, zt), mZ) for sx in (-1.0, 1.0)]
    cut_parts(parts, "Process chamber body", [hole(p, n, -0.5, 9.9 + 0.01, 6.0) for p, n in ditems])
    cut_parts(parts, "Chamber floor plate", [hole(p, n, 9.9 + 0.1 - 0.01, 20.5, 6.0) for p, n in ditems])
    add_fasteners(h, add, "floor_dowels", "Floor-plate dowels, Ø6 x 20 316 (pressed into the plate, slip fit in the frame), front-left and back-right corners",
                  dw, ditems, 5, "G1", explode=(0, 0, -150))
    JOINT_NOTES["floor"] = ("Opened only for major maintenance, so plain tapped M4 threads in the 6061 frame (an insert would leave 1 mm webs in the "
                            "8 mm skirt). 18 screws at ~1.1 N m (Shigley, chamber-construction.md: separation factor >= 4 with the stiffest O-ring "
                            "and +50 mbar); the screws pull the pad's top face onto the frame metal to metal, so the O-ring squeeze is the groove "
                            "depth and the 1.5 mm crevice at the floor's edge stays closed. Two dowels make it go back in the same place.")

    # ---------------- 2. build module flange: 2 captive M6 screws, inserts, a dowel and a diamond pin ----------------
    _KEY[0] = "module_flange"
    cap, ret, ins6 = "95966A705", "91065A610", find("insert", 6, 12)
    zfl = zf - MP.FLANGE_T
    items = [((s * MP.SCREW_X, 0.0, zfl), Z) for s in (-1, 1)]
    cut_parts(parts, f"Build module {module}", [hole((s * MP.SCREW_X, 0, zf), Z, -1.0, 0.0, 8.6) for s in (-1, 1)])   # retainer recess
    cut_parts(parts, "Chamber floor plate", [hole(p, n, MP.FLANGE_T - 0.01, MP.FLANGE_T + 12.0, insert_od(ins6)) for p, n in items] +
              [hole(p, n, MP.FLANGE_T + 12.0 - 0.01, MP.FLANGE_T + 13.5, 6.0) for p, n in items])
    add_fasteners(h, add, "module_flange", "Captive M6 panel screws on the module flange (knurled, 18-8)", cap, items, 4, "B2",
                  group="module", explode=(0, -320, -60))
    add_fasteners(h, add, "module_flange", "Captive-screw retainers (18-8)", ret, [((p[0], p[1], zf - 0.5), mZ) for p, n in items], 4, "B2",
                  group="module", explode=(0, -320, -60))
    add_fasteners(h, add, "module_flange", "Helical inserts for the module screws, M6 x 12 18-8, in the floor", ins6,
                  [((p[0], p[1], zf), Z) for p, n in items], 5, "B2", explode=(0, 0, -40))
    dw = find("dowel", 6, 20)
    add_fasteners(h, add, "module_dowels", "Locating dowel (round, +y) and diamond pin (-y: the same dowel with two flats ground "
                  "to 2 mm lands across x), Ø6 x 20 316, pressed into the floor", dw,
                  [((0.0, s * MP.DOWEL_Y, zf + 10.0), mZ) for s in (1, -1)], 3, "B2", explode=(0, 0, -40))
    dp = [p for p in parts if p.name.startswith("Locating dowel")][-1]
    dp.shape = dp.shape.cut(*[cq.Solid.makeBox(20, 10, 30, V(-10, -MP.DOWEL_Y + s, zf - 25)) for s in (1.0, -11.0)])
    JOINT_NOTES["module_flange"] = ("Swapped by a person between campaigns. The dowel and diamond pin locate the module; the "
                                    "screws only hold it up (the loads are < 0.2 kN against ~6 kN of preload). "
                                    "See hot-swap.md for the robot-swap alternatives.")

    # ---------------- 3. heater stack: block - Macor rings and shields - piston head ----------------
    key = module
    _KEY[0] = f"stack_{key}"
    m = MP.MODULES[key]
    L = ML.block_layout(key)
    zl = ML.zlevels()
    zb0_, zh0, zk0 = zl["zb0"], zl["zh0"], zl["zk0"]
    if key == "S25":
        d, Ls, cbd, cbh, ins_pn = 2.5, 30, 4.6, 3.2, find("insert", 2.5, 3.8)
    else:
        d, Ls, cbd, cbh, ins_pn = 3.0, 25, 7.0, 6.5, find("insert", 3, 4.5)
    spn = find("shcs", d, Ls)
    # a light 302 disc spring (McMaster 9713K5x, ~50 N at 0.1 mm), not a stiff 718 one: the head must be able to slide in its
    # slot under the spring as the block grows (hot-swap.md §4; a held M3 would be bent past yield by the 43-64 um growth)
    light = [q for q, c in FS.CATALOG.items() if c.get("kind") == "disc" and q.startswith("9713K")
             and float(c.get("id", 0)) >= d + 0.1 and float(c.get("od", 99)) <= cbd - 0.4]
    spring = light[0] if light else None
    hs = float(FS.CATALOG[spring].get("H", FS.CATALOG[spring]["t"] + FS.CATALOG[spring]["h0"])) if spring else 0.0
    if key == "S25":
        spring, hs = None, 0.0        # no disc spring fits a Ø5 counterbore on the Ø24.8 head
    items, slots_cb, slots_sh, ins_holes, tip_holes, ins_items = [], [], [], [], [], []
    for r, a in L["standoffs"]:
        x, y = polar(r, a)
        p = (x, y, zh0 + cbh - hs)
        items.append((p, Z))
        rad = (math.cos(math.radians(a)), math.sin(math.radians(a)), 0.0)
        # radial slots in the cool head let the hot block grow (~42 um at the M50 screw circle) without bending the screw
        slots_cb.append(slot(p, Z, -(cbh - hs) - 0.01, hs, cbd, 0.3, rad))
        slots_sh.append(slot(p, Z, hs - 0.01, hs + (MP.HEAD_T - cbh) + 0.01, CLEAR[d], 0.3, rad))
        s_blk = (zb0_ - p[2])                       # s at the block's bottom face
        ins_holes.append(hole(p, Z, s_blk - 0.01, s_blk + float(FS.CATALOG[ins_pn]["L"]), insert_od(ins_pn)))
        tip_holes.append(hole(p, Z, s_blk + float(FS.CATALOG[ins_pn]["L"]) - 0.01, Ls + 1.0, d))
        ins_items.append(((x, y, zb0_), Z))
    cut_parts(parts, f"Piston head {key}", slots_cb + slots_sh)
    cut_parts(parts, f"Heater block {key}", ins_holes + tip_holes)
    tg = dict(group="piston", tags=("in_module",))
    add_fasteners(h, add, f"stack_{key}", f"Heater-stack screws {key}, M{d:g} x {Ls} 316, up through slotted counterbores in the piston head",
                  spn, items, 4, "H1", explode=(0, 0, 170), section=True, **tg)
    add_fasteners(h, add, f"stack_{key}", f"Heater-block helical inserts {key}, M{d:g} 18-8", ins_pn, ins_items, 4, "H1",
                  explode=(0, 0, 250), section=True, **tg)
    if spring:
        add_fasteners(h, add, f"stack_{key}", f"Disc springs under the stack screws {key}", spring,
                      [((p[0], p[1], zh0 + cbh), Z) for p, n in items], 4, "H1", explode=(0, 0, 170), section=True, **tg)
    JOINT_NOTES[f"stack_{key}"] = ("Replaces M3 screws threaded into Macor (too weak). The screw runs from the cool piston head "
                                   "through three Macor rings, with the two shields clamped between them, into a helical insert in "
                                   "the hot block. Radial slots in the head let the block grow; a disc spring keeps the preload "
                                   "through heat cycles. Heat through the three screws: hot-swap.md.")

    # ---------------- 4. gland plate: 6 x M4 x 16 into the welded collar ----------------
    R, W = m["bore"] / 2, m["wall"]
    _KEY[0] = f"gland_{key}"
    rc = R + W + MP.COLLAR_W
    rbc = R + W + 6.5
    zst = zl["z_stop"]
    pn4 = find("shcs", 4, 16)
    pn4g = find("shcs", 4, 20)                      # 14 mm gland plate (two rod glands) + 6 mm into the collar
    items = [((*polar(rbc, 30.0 + 60.0 * k), zst - MP.BOT_FLANGE_T), Z) for k in range(6)]
    cut_parts(parts, f"Module {key} bottom flange", [hole(p, n, -0.01, MP.BOT_FLANGE_T + 0.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, f"Build module {key}", [hole(p, n, MP.BOT_FLANGE_T - 0.01, MP.BOT_FLANGE_T + MP.COLLAR_T + 0.01, 4.0) for p, n in items])
    add_fasteners(h, add, f"gland_{key}", f"Gland-plate screws {key}, M4 x 20 316, into the welded collar", pn4g, items, 4, "B1",
                  group="module", explode=(0, -320, -60))

    # handle: 2 x M4 x 10 up into the gland plate
    hx = min(19.0, 0.47 * rc)
    pn4s = find("shcs", 4, 10)
    items = [((s * hx, -rc + 7.0, zst - MP.BOT_FLANGE_T - 4.0), Z) for s in (-1, 1)]
    cut_parts(parts, f"Module {key} handle", [hole(p, n, -0.01, 4.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, f"Module {key} bottom flange", [hole(p, n, 3.99, 12.0, 4.0) for p, n in items])
    add_fasteners(h, add, f"handle_{key}", f"Handle screws {key}, M4 x 10 316", pn4s, items, 4, "B1", group="module", explode=(0, -320, -60))
    JOINT_NOTES[f"gland_{key}"] = ("Replaces a welded bottom flange. A 316L collar welded round the tube end takes 6 x M4; the plate "
                                   "seals on the tube end and collar with a 1.78 mm FKM face O-ring. Take the piston out of the top, "
                                   "then the plate comes off to replace the rod O-rings or clean out powder that passed the bore seal.")

    # ---------------- 5. rod in the piston head: 2 cup-point set screws; striker on the rod end: 3 flat-head screws ----------------
    rod_od = (MP.ROD_S25 if key == "S25" else (MP.ROD_OD, MP.ROD_ID))[0]
    Rb = m["block_d"] / 2
    ss = find("set", 4, 6 if key == "S25" else 16)
    Lss = float(FS.CATALOG[ss]["L"])
    zss = zh0 + 3.5
    angs = (0.0, 180.0) if key == "S25" else (90.0, 270.0)
    items = []
    for a in angs:
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        ro = rod_od / 2 + Lss
        items.append(((ro * ca, ro * sa, zss), (-ca, -sa, 0.0)))
    cut_parts(parts, f"Piston head {key}", [hole(p, n, -(Rb - (rod_od / 2 + Lss)) - 1.0, Lss + 0.5, 4.0) for p, n in items])
    add_fasteners(h, add, f"rod_{key}", f"Rod set screws {key}, M4 cup point 316", ss, items, 4, "B1", explode=(0, 0, 140), section=True, **tg)

    fh = find("fhcs", 3, 10)
    zc = zl["zc"]
    items = [((*polar(8.75, a), zc), Z) for a in (0.0, 120.0, 240.0)]
    dk = float(FS.CATALOG[fh].get("dk", 6.0))
    mg = float(FS.CATALOG[fh].get("margin", 0.1)) + 0.05            # the head's short cylindrical band, plus clearance
    csk = mg + (dk + 0.2 - CLEAR[3]) / 2                             # 90 deg countersink from dk + 0.2 down to the clearance hole
    cut_parts(parts, f"Striker disc {key}", [hole(p, n, -0.01, mg, dk + 0.2) for p, n in items] +
              [cone(p, n, mg - 0.001, csk, dk + 0.2, CLEAR[3]) for p, n in items] + [hole(p, n, csk - 0.01, 5.01, CLEAR[3]) for p, n in items])
    cut_parts(parts, f"Rod end {key}", [hole(p, n, 4.99, 11.0, 3.0) for p, n in items])
    add_fasteners(h, add, f"striker_{key}", f"Striker screws {key}, M3 x 10 316 flat head (flush on the magnet face)", fh, items, 4, "B2",
                  explode=(0, 0, 110), section=True, **tg)

    # ---------------- 6. recoater rail: 4 x M4 x 16 from inside into M4 holes tapped THROUGH the back wall from outside ----------------
    # A hole in the back wall's inside face could only be drilled through the door opening, 206 mm from the front face (a long drill
    # and tap: what the machinist objected to). Tapped through from outside instead (standard drill and tap, in the same back-face
    # setup as the inlet slot); the rail screws go in from inside, and each hole's outer end is closed by an M4 x 10 plug screw on a
    # bonded seal washer: 4 small extra face seals (chamber-construction.md). Rarely taken apart, so plain 6061 threads, no inserts.
    _KEY[0] = "rail"
    xs = [-130.0 + x for x in h.rail_hole_x(260.0) if x <= 255.0]       # 260 mm rail (lpbf_low: clears the frame's R10 corners): x -110, -50, 10, 70
    zr_ = P["rc_rail_z"]
    yb = iy - (15.0 - h.RAIL_HOLES["cb_h"])
    items = [((x, yb, zr_), (0.0, 1.0, 0.0)) for x in xs]
    ins4 = find("insert", 4, 6)
    cut_parts(parts, "Process chamber body", [hole((x, iy, zr_), (0.0, 1.0, 0.0), -0.01, P["wall"] + 0.01, 4.0) for x in xs])
    add_fasteners(h, add, "rail", "Recoater rail screws, M4 x 16 316, into M4 holes tapped through the back wall", pn4, items, 6, "M1", explode=(0, 0, 220))
    tw_ = 1.5                                                  # bonded washer: 316 ring with an FKM lip, 1.5 thick
    add_fasteners(h, add, "rail_plugs", "Rail-hole plug screws, M4 x 10 316, on bonded seal washers (outer face of the back wall)", find("shcs", 4, 10),
                  [((x, cy + tw_, zr_), (0.0, -1.0, 0.0)) for x in xs], 5, "M1", explode=(0, 200, 0))
    add("Rail-hole bonded seal washers (4 x M4, 316 ring + FKM lip, Dowty type; seal the through-tapped rail holes)",
        h.comp([h.tube(4.75, 2.15, (x, cy, zr_), "y", tw_) for x in xs]), C["black"], 5, (0, 190, 0), mat="fkm", bom="M1", tags=("rail_plugs",))
    JOINT_NOTES["rail"] = ("Rail screws from inside into M4 holes tapped through the back wall from outside; M4 x 10 plug screws on bonded seal washers "
                           "close the holes' outer ends (the screw tips are 1.2 mm apart). No tool reaches the inside face of the back wall.")

    # ---------------- 7. recoater blade: 2 x M3 x 8 through the blade into the holder, heads above the powder heap ----------------
    xc = P["x_park"]
    items = [((xc + 10.5, y, 14.0), (-1.0, 0.0, 0.0)) for y in (-30.0, 30.0)]
    pn3 = find("shcs", 3, 8)
    cut_parts(parts, "HSS recoater blade", [hole(p, n, -0.01, 1.51, CLEAR[3]) for p, n in items])
    cut_parts(parts, "Blade holder", [hole(p, n, 1.49, 9.0, 3.0) for p, n in items])
    add_fasteners(h, add, "blade", "Blade screws, M3 x 8 316 (heads 11-17 mm above the plate, over the powder heap)", pn3, items, 6, "M5",
                  group="recoater", explode=(0, 0, 220))

    # ---------------- 7b. blade cartridge in the arm's pocket: 2 x Ø3 dowels and 2 ball plungers, no screws (robot-ops.md patch 5) ----------------
    # The cartridge (holder + blade + grip fin) slides 8 mm into the arm's pocket from the front (the holder's back end, y 53..61). Two
    # Ø3 x 10 316 dowels pressed 5.5 mm into the pocket's back wall (y 61..67) enter slip holes in the holder's back face and take the
    # blade's 50 N strike in shear; two M6 ball plungers in the pocket's side walls drop into 0.8 mm dimples in the holder's sides
    # and hold it home (~40 N straight pull to release, as the reservoir's detents). The blade's own two M3 stay: it is changed on
    # the bench in a spare cartridge, so neither the robot nor a person needs a screwdriver at the machine.
    _KEY[0] = "blade_cartridge"
    yb_c, zc_ = P["iy"] - 34.0, 19.5                            # holder back face; arm mid-height (arm z 14..25)
    dw3 = find("dowel", 3, 10)
    ditems = [((xc + s * 4.5, yb_c + 5.5, zc_), (0.0, -1.0, 0.0)) for s in (-1, 1)]
    cut_parts(parts, "Recoater arm", [hole(p, n, -0.01, 5.5 + 0.01, 3.0) for p, n in ditems])
    cut_parts(parts, "Blade holder", [hole(p, n, 5.49, 10.6, 3.0) for p, n in ditems])
    add_fasteners(h, add, "blade_cartridge", "Blade-cartridge dowels, Ø3 x 10 316 (pressed into the arm's pocket, slip fit in the holder's back face)", dw3,
                  ditems, 6, "M5", group="recoater", explode=(0, 0, 220))
    pl = "85015A47"
    c_pl = FS.CATALOG[pl]
    yp = yb_c - 4.0                                             # 4 mm in front of the holder's back face, inside the pocket
    xr = c_pl["L"] + c_pl["travel"] - 0.8                       # top of the plunger from the holder's side face: ball 0.8 mm into its dimple
    pitems = [((xc + s * (9.0 + xr), yp, zc_), (-s, 0.0, 0.0)) for s in (-1, 1)]
    cut_parts(parts, "Recoater arm", [hole(p, n, -3.5, xr + 0.01, c_pl["d"]) for p, n in pitems])          # M6 tapped through the pocket wall
    rb = c_pl["ball_d"] / 2
    cut_parts(parts, "Blade holder", [cq.Solid.makeSphere(rb + 0.05, V(xc + s * (9.0 - 0.8 + rb), yp, zc_), angleDegrees1=-90, angleDegrees2=90)
                                      for s in (-1, 1)])                       # full sphere (makeSphere's default is a hemisphere)
    add_fasteners(h, add, "blade_cartridge", "Blade-cartridge ball plungers, M6 x 1 18-8 with 440C ball, in the arm's pocket walls (detents in the holder's sides)",
                  pl, pitems, 6, "M5", group="recoater", explode=(0, 0, 220))
    JOINT_NOTES["blade_cartridge"] = ("Swapped at every alloy change by the robot (or a hand) with a 40 N straight pull: no screwdriver at the machine. The "
                                      "dowels locate the holder to the arm (H7 holes; pressed in the arm, slip in the holder) and take the blade's 50 N "
                                      "strike in shear; the plungers' balls sit in 0.8 mm dimples (hot-swap.md 3.3; robot-ops.md patch 5).")

    # ---------------- 8. window: flange to lid (6 x M4 x 16, M4 x 4 inserts: the drawer slot is 5 mm under the lid top) ----------------
    ins44 = find("insert", 4, 4)
    items = [((*polar(40.0, 60.0 * k), lz1 + 12.0), mZ) for k in range(6)]
    cut_parts(parts, "Window flange", [hole(p, n, -10.01, 0.0, CBORE[4][0]) for p, n in items] + [hole(p, n, -0.01, 12.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Chamber lid", [hole(p, n, 12.0, 16.0, insert_od(ins44)) for p, n in items] + [hole(p, n, 15.99, 16.5, 4.0) for p, n in items])
    add_fasteners(h, add, "window", "Window-flange screws, M4 x 16 316", pn4, items, 7, "L7", explode=(0, 0, 360))
    add_fasteners(h, add, "window", "Window-flange helical inserts, M4 x 4 18-8, in the lid", ins44,
                  [((p[0], p[1], lz1), mZ) for p, n in items], 7, "L7", explode=(0, 0, 300))
    items = [((*polar(32.0, 30.0 + 60.0 * k), lz1 + 27.0), mZ) for k in range(6)]
    pn310 = find("shcs", 3, 10)
    cut_parts(parts, "Window retaining ring", [hole(p, n, -0.01, 5.01, CLEAR[3]) for p, n in items])
    cut_parts(parts, "Window flange", [hole(p, n, 4.99, 11.5, 3.0) for p, n in items])
    add_fasteners(h, add, "window_ring", "Window retaining-ring screws, M3 x 10 316", pn310, items, 7, "L7", explode=(0, 0, 400))

    # ---------------- 9. metering base: 4 x M4 x 16 through its tabs into the lid ----------------
    xd = P["x_dose"]
    items = [((xd + sx * 9.0, sy * 66.0, lz1 + 8.0), mZ) for sx in (-1, 1) for sy in (-1, 1)]
    cut_parts(parts, "Metering base", [hole(p, n, -0.01, 8.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Chamber lid", [hole(p, n, 8.0, 14.0, insert_od(ins4)) for p, n in items] + [hole(p, n, 13.99, 17.0, 4.0) for p, n in items])
    add_fasteners(h, add, "dose", "Metering-base screws, M4 x 16 316", pn4, items, 7, "M4", explode=(0, 0, 300))
    add_fasteners(h, add, "dose", "Metering-base helical inserts, M4 x 6 18-8, in the lid", ins4,
                  [((p[0], p[1], lz1), mZ) for p, n in items], 7, "M4", explode=(0, 0, 300))

    # ---------------- 9b. seals: screws that set the face O-rings' squeeze metal-to-metal (seals.md item 10) ----------------
    _KEY[0] = "plenum_in"
    yb_ = cy + 6.0
    # 7 screws (was 9): the frame ends at z -3.9, so the four below the old floor line moved to the sides, outside the O-ring loop
    items = [((x, yb_, z), (0.0, -1.0, 0.0)) for x, z in ((-71.0, 4.5), (71.0, 4.5), (-71.0, 22.0), (71.0, 22.0), (-40.0, 34.0), (40.0, 34.0), (0.0, 34.0))]
    cut_parts(parts, "Cross-flow inlet plenum", [hole(p, n, -0.01, 6.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Process chamber body", [hole(p, n, 6.0, 12.0, insert_od(ins4)) for p, n in items] + [hole(p, n, 11.99, 17.5, 4.0) for p, n in items])
    add_fasteners(h, add, "plenum_in", "Inlet-plenum screws, M4 x 16 316 (clear of the Z flange's screws)", pn4, items, 5, "G4", explode=(0, 180, 0))
    add_fasteners(h, add, "plenum_in", "Inlet-plenum helical inserts, M4 x 6 18-8, in the back wall", ins4, [((p[0], cy, p[2]), n) for p, n in items], 5, "G4", explode=(0, 180, 0))
    JOINT_NOTES["plenum_in"] = "316L plenum on the 6061 back wall: bolted over an FKM face O-ring, never welded (dissimilar metals)."
    # locating pins (assembly.md patch 9, 2026-11-23): two Ø3 x 10 316 dowels pressed 5 mm into the back wall, slip holes through the flange,
    # so the arm that places the plenum also drives its screws (F14). Between the side screws at x +/-71, at the O-ring loop's mid-height.
    locating_pins(h, parts, add, "plenum_in", "Process chamber body", "Cross-flow inlet plenum", [((s * 71.0, cy + 5.0, 13.25), (0.0, -1.0, 0.0)) for s in (-1, 1)],
                  "Inlet-plenum locating dowels", 5, "G4", (0, 180, 0))

    _KEY[0] = "plenum_out"
    y0o, y1o = MP.OUTLET_Y
    pn412 = find("shcs", 4, 12)
    items = [((x, y, zf - 6.0), Z) for x in (-50.0, 0.0, 45.0) for y in (y0o - 7.0, y1o + 7.0)]
    cut_parts(parts, "Cross-flow outlet plenum", [hole(p, n, -10.01, 0.0, CBORE[4][0]) for p, n in items] + [hole(p, n, -0.01, 6.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Chamber floor plate", [hole(p, n, 6.0, 12.0, insert_od(ins4)) for p, n in items] + [hole(p, n, 11.99, 13.5, 4.0) for p, n in items])
    add_fasteners(h, add, "plenum_out", "Outlet-plenum screws, M4 x 12 316, counterbored", pn412, items, 5, "G4", explode=(0, 0, -180))
    add_fasteners(h, add, "plenum_out", "Outlet-plenum helical inserts, M4 x 6 18-8, in the floor", ins4, [((p[0], p[1], zf), Z) for p, n in items], 5, "G4", explode=(0, 0, -40))
    JOINT_NOTES["plenum_out"] = "316L plenum under the 6061 floor plate: bolted over an FKM face O-ring; counterbored so the heads stay clear of the module's path."

    _KEY[0] = "funnel"
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    items = [((x, y, zf - 6.0), Z) for x in (ox - 17.0, ox + 17.0) for y in (-40.0, 40.0)]
    cut_parts(parts, "Overflow funnel block", [hole(p, n, -16.01, 0.0, CBORE[4][0]) for p, n in items] + [hole(p, n, -0.01, 6.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Chamber floor plate", [hole(p, n, 6.0, 12.0, insert_od(ins4)) for p, n in items] + [hole(p, n, 11.99, 13.5, 4.0) for p, n in items])
    add_fasteners(h, add, "funnel", "Overflow-funnel screws, M4 x 12 316, counterbored", pn412, items, 4, "M4", explode=(0, 0, -200))
    add_fasteners(h, add, "funnel", "Overflow-funnel helical inserts, M4 x 6 18-8, in the floor", ins4, [((p[0], p[1], zf), Z) for p, n in items], 4, "M4", explode=(0, 0, -40))

    _KEY[0] = "vac_port"
    pn520 = find("shcs", 5, 20)
    items = [((cx + 8.0, y, z), (-1.0, 0.0, 0.0)) for y in (-23.0, 23.0) for z in (47.0, 93.0)]
    cut_parts(parts, "Vacuum port adapter plate", [hole(p, n, -0.01, 8.01, CLEAR[5]) for p, n in items])
    cut_parts(parts, "Process chamber body", [hole(p, n, 8.0, 15.5, od) for p, n in items] + [hole(p, n, 15.49, 20.5, 5.0) for p, n in items])
    add_fasteners(h, add, "vac_port", "Vacuum-port adapter screws, M5 x 20 316", pn520, items, 5, "G7", explode=(180, 0, 0))
    add_fasteners(h, add, "vac_port", "Vacuum-port adapter helical inserts, M5 x 7.5 18-8, in the right wall", ins, [((cx, p[1], p[2]), n) for p, n in items], 5, "G7", explode=(180, 0, 0))
    # locating pins (assembly.md patch 9): above and below the bore on the plate's centre line, outside the 2-024 groove (F16)
    locating_pins(h, parts, add, "vac_port", "Process chamber body", "Vacuum port adapter plate", [((cx + 5.0, 0.0, z), (-1.0, 0.0, 0.0)) for z in (47.0, 93.0)],
                  "Vacuum-port adapter locating dowels", 5, "G7", (180, 0, 0))

    _KEY[0] = "bearing_cap"
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    pn420 = find("shcs", 4, 20)
    items = [((cx + 14.0, ry_ + 16.0 * math.cos(math.radians(a)), rz_ + 16.0 * math.sin(math.radians(a))), (-1.0, 0.0, 0.0)) for a in (45.0, 135.0, 225.0, 315.0)]
    cut_parts(parts, "Recoater floating bearing housing", [hole(p, n, -0.01, 14.01, CLEAR[4]) for p, n in items])
    cut_parts(parts, "Process chamber body", [hole(p, n, 14.0, 20.0, insert_od(ins4)) for p, n in items] + [hole(p, n, 19.99, 21.5, 4.0) for p, n in items])
    add_fasteners(h, add, "bearing_cap", "Bearing-cap screws, M4 x 20 316", pn420, items, 6, "M1", explode=(160, 0, 0))
    add_fasteners(h, add, "bearing_cap", "Bearing-cap helical inserts, M4 x 6 18-8, in the right wall", ins4, [((cx, p[1], p[2]), n) for p, n in items], 6, "M1", explode=(160, 0, 0))
    # locating pins (assembly.md patch 9): on the 16 mm screw circle at 90 deg (front) and 270 deg (back), between the screws, outside the 2-019 groove (F23)
    locating_pins(h, parts, add, "bearing_cap", "Process chamber body", "Recoater floating bearing housing",
                  [((cx + 5.0, ry_ + s * 16.0, rz_), (-1.0, 0.0, 0.0)) for s in (-1, 1)], "Bearing-cap locating dowels", 6, "M1", (160, 0, 0))

    _KEY[0] = "res_lid"
    res = getattr(h, "_RES", None)
    if res:
        pn38 = find("shcs", 3, 8)
        items = [((x, y, z), mZ) for x, y, z in res["lid_screws"]]
        cut_parts(parts, f"Reservoir {res['key']} lid", [hole(p, n, -0.01, 4.01, CLEAR[3]) for p, n in items])
        cut_parts(parts, f"Reservoir {res['key']} (", [hole(p, n, 3.99, 8.0, 3.0) for p, n in items])
        add_fasteners(h, add, "res_lid", f"Reservoir {res['key']} lid screws, M3 x 8 316 (blind tapped holes in the top frame, outside the seal)", pn38, items, 7, "R1",
                      group="cartridge", explode=(0, 0, 420))
    JOINT_NOTES["seals"] = ("Every face O-ring added for seals.md is squeezed metal-to-metal: the screws pull the parts together until the lands touch, "
                            "so the squeeze is the groove depth, not the torque.")

    # ---------------- 10. Z mounting flange: 4 x M5 x 12, counterbored, into M5 x 7.5 inserts in the floor ----------------
    _KEY[0] = "zmount"
    items = [((x, y, zf - 4.5), Z) for x, y in ((-33.0, 70.0), (-33.0, 100.0), (40.0, 102.0), (94.0, 102.0))]
    pn512 = find("shcs", 5, 12)
    cut_parts(parts, "Z mounting flange", [hole(p, n, -5.51, 0.0, CBORE[5][0]) for p, n in items] + [hole(p, n, -0.01, 4.51, CLEAR[5]) for p, n in items])
    cut_parts(parts, "Chamber floor plate", [hole(p, n, 4.5, 12.0, insert_od(ins)) for p, n in items] + [hole(p, n, 11.99, 13.5, 5.0) for p, n in items])
    add_fasteners(h, add, "zmount", "Z-flange screws, M5 x 12 316, counterbored", pn512, items, 3, "M3", explode=(0, 120, 0))
    add_fasteners(h, add, "zmount", "Z-flange helical inserts, M5 x 7.5 18-8, in the floor", ins, [((p[0], p[1], zf), Z) for p, n in items], 3, "M3",
                  explode=(0, 0, -40))

    # ---------------- 11. chamber legs: 1 x M6 x 25 up the leg's bore into the floor; 2 x M6 x 25 up through the base plate ----------------
    _KEY[0] = "legs"
    pn625, ins69 = find("shcs", 6, 25), find("insert", 6, 9)
    tops, bots, cb_tools, base_tools, leg_taps, top_ins = [], [], [], [], [], []
    for x0 in (-cx + 6, cx - 36):
        for y0 in (-cy + 6, cy - 36):
            xc_, yc_ = x0 + 15.0, y0 + 15.0
            p = (xc_, yc_, zf - 15.0)
            tops.append((p, Z))
            cb_tools += [hole(p, Z, -(zf - 15.0 - zb1) - 0.01, 0.0, 11.0), hole(p, Z, -0.01, 15.01, CLEAR[6])]
            base_tools.append(hole((xc_, yc_, zb0), Z, -0.01, 15.01, 11.0))           # hex-key access to the top screw
            top_ins.append(((xc_, yc_, zf), Z))
            for sx, sy in ((1, -1), (-1, 1)):
                q = (xc_ + sx * 8.5, yc_ + sy * 8.5, zb0)
                bots.append((q, Z))
                base_tools.append(hole(q, Z, -0.01, 15.01, CLEAR[6]))
                leg_taps.append(hole(q, Z, 14.99, 27.0, 6.0))
    cut_parts(parts, "Chamber legs", cb_tools + leg_taps)
    cut_parts(parts, "Base plate, process", base_tools)
    cut_parts(parts, "Chamber floor plate", [hole(p, n, 15.0, 24.0, insert_od(ins69)) for p, n in tops] + [hole(p, n, 23.99, 26.0, 6.0) for p, n in tops])
    add_fasteners(h, add, "legs", "Leg-to-floor screws, M6 x 25 316, up each leg's Ø11 bore", pn625, tops, 3, "G1", explode=(0, 0, -120))
    add_fasteners(h, add, "legs", "Leg helical inserts, M6 x 9 18-8, in the floor", ins69, top_ins, 3, "G1", explode=(0, 0, -40))
    add_fasteners(h, add, "legs_base", "Base-plate-to-leg screws, M6 x 25 316", pn625, bots, 3, "G1", explode=(0, 0, -150))

    # ---------------- 12. optics bridge: 2 x M6 x 35 down into each post's top cap; 2 x M6 x 25 up into its bottom cap ----------------
    pn635 = find("shcs", 6, 35)
    zt_, zb_ = P["z_bridge1"], P["z_bridge0"]
    tops, bots = [], []
    for x in (-345.0, 180.0):
        for y in (-185.0, 115.0):
            xc_, yc_ = x + 30.0, y + 30.0
            tops += [((xc_ + s * 15.0, yc_, zt_), mZ) for s in (-1, 1)]
            bots += [((xc_, yc_ + s * 15.0, zb0), Z) for s in (-1, 1)]
    cut_parts(parts, "Optics bridge (", [hole(p, n, -0.01, 25.01, CLEAR[6]) for p, n in tops])
    cut_parts(parts, "Optics bridge posts", [hole(p, n, 24.99, 35.5, 6.0) for p, n in tops] + [hole(p, n, 14.99, 25.5, 6.0) for p, n in bots])
    cut_parts(parts, "Base plate, process", [hole(p, n, -0.01, 15.01, CLEAR[6]) for p, n in bots])
    add_fasteners(h, add, "bridge", "Optics-bridge screws, M6 x 35 316", pn635, tops, 9, "F5", explode=(0, 0, 260))
    add_fasteners(h, add, "bridge_base", "Optics-post base screws, M6 x 25 316", pn625, bots, 9, "F5", explode=(0, 0, -150))

    # ---------------- 13. leveling mounts: the 5537T983's M8 stem threads up through each base plate ----------------
    for nm in ("Base plate, process", "Base plate, gas"):
        bp = [p for p in parts if p.name.startswith(nm)][0]
        b = bp.shape.BoundingBox()
        x0, x1, y0, y1 = b.xmin, b.xmax, b.ymin, b.ymax
        bp.shape = bp.shape.cut(*[hole((x, y, zb0), Z, -0.01, 15.01, 8.0) for x in (x0 + 30, x1 - 30) for y in (y0 + 30, y1 - 30)])
    JOINT_NOTES["feet"] = "The leveling mounts' M8 stems thread into tapped M8 holes in the 15 mm base plates and end flush with the top."
    return REGISTRY


def bom_rows():
    """(joint, McMaster PN, description, qty, unit price, sold as) for every fastener placed by the last add_joints()."""
    rows = []
    for key, r in REGISTRY.items():
        for pn, items in [(r["pn"], r["items"])] + r["extra"]:
            c = FS.CATALOG[pn]
            rows.append((key, pn, c.get("desc", ""), len(items), c.get("price_usd"), c.get("sold_as"), c.get("url")))
    return rows
