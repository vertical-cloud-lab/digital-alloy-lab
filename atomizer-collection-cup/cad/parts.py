"""CadQuery parts for the collection cup: the machine's cone outlet, the stock cup, and the lab-built options.

Coordinates: mm, z up, z = 0 at the mid-plane of the cone's outlet joint (the ISO-KF centring ring).
The cup hangs below (z < 0); the mat the machine stands on is at z = -params.Z_JOINT_FACE.
Every size comes from ../params.py. Each function returns a list of (name, solid, colour, material)
so the assembly, the interference check, the mass table and the renders all use the same parts.
"""

import math
import sys
from pathlib import Path

import cadquery as cq
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import params as P  # noqa: E402

STEEL = (0.80, 0.81, 0.83)
STEEL_DK = (0.62, 0.63, 0.66)
STEEL_HOT = (0.72, 0.62, 0.52)
GLASS = (0.70, 0.86, 0.95)
QUARTZ = (0.86, 0.93, 0.97)
FKM = (0.12, 0.12, 0.13)
EPDM = (0.10, 0.10, 0.10)
BLACK = (0.06, 0.06, 0.07)
GREEN = (0.30, 0.68, 0.25)
RED = (0.80, 0.12, 0.10)
COPPER = (0.78, 0.47, 0.30)
YELLOW = (0.95, 0.78, 0.15)
BRASS_TC = (0.85, 0.70, 0.30)


def revolve(profile, angle=360.0):
    """Revolve a closed (r, z) polyline about the z axis."""
    wp = cq.Workplane("XZ").polyline(profile).close()
    return wp.revolve(angle, (0, 0, 0), (0, 1, 0)).val()


def tube(r_out, r_in, z0, z1):
    return revolve([(r_in, z0), (r_out, z0), (r_out, z1), (r_in, z1)])


def kf_flange_profile(kf, face_z, down=True, tube_len=20.0, recess=True):
    """(r, z) profile of an ISO-KF flange with its weld tube. Sealing face at face_z.

    down=True: the flange faces up and its tube runs down (the cup side). down=False: mirror (cone side).
    recess: cut the centring ring's recess into the sealing face (left out of the thermal models).
    """
    s = -1.0 if down else 1.0
    rb, rf, rh, rt = kf.bore / 2, kf.flange_od / 2, kf.hub_od / 2, kf.tube_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    face = [(rb, face_z)]
    if recess and kf.recess_depth:
        rr, rd = kf.recess_d / 2, kf.recess_depth
        face = [(rb, face_z + s * rd), (rr, face_z + s * rd), (rr, face_z)]
    pts = face + [(rf, face_z), (rf, face_z + s * t_edge), (rh, face_z + s * kf.lip),
                  (rt, face_z + s * (kf.lip + 1.5)), (rt, face_z + s * tube_len), (rb, face_z + s * tube_len)]
    return pts


def kf_flange(kf, face_z, down=True, tube_len=20.0, recess=True):
    return revolve(kf_flange_profile(kf, face_z, down, tube_len, recess))


def kf_blank(kf, face_z):
    """KF blank: a flange with no bore, sealing face up at face_z."""
    rf, rh = kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    rr, rd = kf.recess_d / 2, kf.recess_depth
    pts = [(0, face_z - rd), (rr, face_z - rd), (rr, face_z), (rf, face_z), (rf, face_z - t_edge),
           (rh, face_z - kf.lip), (0, face_z - kf.lip)]
    return revolve(pts)


def kf_centring_ring(kf, z_mid):
    """Metal centring ring plus its O-ring (as a squashed torus), centred on z_mid.

    Vendor geometry (Lesker QF50-200-SRV, McMaster 4518K65): the ring's body (ring_id .. ring_body_od) is
    ring_thk + 2 recess_depth thick and sits in the recesses of both faces; a rib out to ring_od (= the
    O-ring's ID) carries the O-ring, which the faces squash to ring_thk.
    """
    h = kf.ring_thk
    hb = h / 2 + kf.recess_depth
    ring = tube(kf.ring_body_od / 2, kf.ring_id / 2, z_mid - hb, z_mid + hb)
    ring = ring.fuse(tube(kf.ring_od / 2, kf.ring_body_od / 2 - 0.01, z_mid - 0.9, z_mid + 0.9))
    a = kf.oring_cs / 2 * 1.12
    r_c = kf.ring_od / 2 + a + 0.05
    oring = (cq.Workplane("XZ").center(r_c, z_mid).ellipse(a, h / 2 * 0.98)
             .revolve(360, (-r_c, 0, 0), (-r_c, 1, 0)).val())
    return ring, oring


def kf_overpressure_ring(z_mid):
    """A&N 4000076 / Lesker QF50-200-OPR: 69.85 OD x 66.55 ID x 3.81 wide, around the O-ring."""
    return tube(69.85 / 2, 66.55 / 2, z_mid - 3.81 / 2, z_mid + 3.81 / 2)


def kf_clamp(kf, z_mid, hinge_angle=180.0, open_deg=0.0):
    """Hinged KF clamp: two segments with an internal V, a hinge and a wing-nut bolt.

    open_deg swings the second segment open about the hinge (for the assembly animation).
    """
    rf = kf.flange_od / 2
    t_edge = kf.lip - (rf - kf.hub_od / 2) * math.tan(math.radians(kf.taper_deg))
    gap = kf.ring_thk / 2
    r_out = kf.clamp_od / 2
    w = kf.clamp_w / 2
    tz = math.tan(math.radians(kf.taper_deg))
    e = gap + t_edge                     # height of each flange's rim corner above/below the mid-plane
    reach = 3.0                        # how far the clamp's lips reach in over the tapers
    prof = [(rf + 0.5, z_mid + e + 0.3), (rf - reach, z_mid + e + reach * tz + 0.3), (rf - reach, z_mid + w),
            (r_out, z_mid + w), (r_out, z_mid - w), (rf - reach, z_mid - w),
            (rf - reach, z_mid - e - reach * tz - 0.3), (rf + 0.5, z_mid - e - 0.3)]
    seg1 = (cq.Workplane("XZ").polyline(prof).close().revolve(172, (0, 0, 0), (0, 1, 0)).val()
            .rotate((0, 0, 0), (0, 0, 1), hinge_angle + 4))
    seg2 = (cq.Workplane("XZ").polyline(prof).close().revolve(172, (0, 0, 0), (0, 1, 0)).val()
            .rotate((0, 0, 0), (0, 0, 1), hinge_angle + 184))
    hinge_xy = (r_out * math.cos(math.radians(hinge_angle)), r_out * math.sin(math.radians(hinge_angle)))
    if open_deg:
        seg2 = seg2.rotate((hinge_xy[0], hinge_xy[1], 0), (hinge_xy[0], hinge_xy[1], 1), open_deg)
    # hinge pin block and the wing-nut bolt on the opposite side
    hinge = (cq.Workplane("XY").cylinder(kf.clamp_w - 6, 4.0).val()
             .translate((hinge_xy[0], hinge_xy[1], z_mid)))
    a = math.radians(hinge_angle + 180)
    bx, by = (r_out + 6) * math.cos(a), (r_out + 6) * math.sin(a)
    lug = cq.Workplane("XY").box(14, 18, kf.clamp_w - 8).val().rotate((0, 0, 0), (0, 0, 1), hinge_angle + 180)
    lug = lug.translate((bx * 0.93, by * 0.93, z_mid))
    bolt = cq.Workplane("XY").cylinder(34, 3.0).val().rotate((0, 0, 0), (1, 0, 0), 90)
    bolt = bolt.rotate((0, 0, 0), (0, 0, 1), hinge_angle + 180).translate((bx, by, z_mid))
    wing = (cq.Workplane("XY").box(30, 5, 12).val().rotate((0, 0, 0), (0, 0, 1), hinge_angle + 180)
            .translate((bx + 22 * math.cos(a + math.pi / 2), by + 22 * math.sin(a + math.pi / 2), z_mid)))
    body = seg1.fuse(seg2).fuse(hinge).fuse(lug)
    if not open_deg:
        body = body.fuse(bolt).fuse(wing)
    return body


# ------------------------------------------------------------------------------------------- machine
def cone_section():
    """The chamber's water-cooled cone and its outlet, down to the KF flange (sealing face at +gap/2).

    Shape from training video 6 (0:24-0:30) and the Nov 13 cleaning video: a polished funnel in a
    square-cornered frame with two green-handled toggle latches, a jacket, and a short outlet spigot.
    """
    kf = P.JOINT
    g = kf.ring_thk / 2
    parts = []
    flange = kf_flange(kf, +g, down=False, tube_len=P.CONE_OUTLET_LEN)
    parts.append(("cone outlet flange", flange, STEEL, "316L"))
    z0 = g + P.CONE_OUTLET_LEN
    r_top = P.CONE_TOP_D / 2
    h = P.CONE_H
    r_bot = kf.tube_od / 2
    wall = 2.0
    inner = [(r_bot - wall, z0), (r_bot, z0), (r_top, z0 + h), (r_top, z0 + h + 12), (r_top - wall, z0 + h + 12),
             (r_bot - wall + 0.01, z0 + 0.5)]
    inner = [(kf.bore / 2, z0), (r_bot, z0), (r_top, z0 + h), (r_top, z0 + h + 12), (r_top - wall, z0 + h + 12),
             (r_top - wall, z0 + h + 1), (kf.bore / 2, z0 + 1.0)]
    parts.append(("cone (water-cooled funnel)", revolve(inner), STEEL, "304"))
    jacket = [(r_bot + 1, z0 - 2), (r_bot + 14, z0 - 2), (r_top + 16, z0 + h - 6), (r_top + 16, z0 + h),
              (r_top + 2, z0 + h), (r_bot + 1, z0 + 2)]
    parts.append(("cone water jacket", revolve(jacket), STEEL_DK, "304"))
    # frame plate at the top of the cone, with the two toggle latches on the front
    frame = (cq.Workplane("XY").rect(P.CONE_TOP_D + 70, P.CONE_TOP_D + 40).extrude(14)
             .edges("|Z").fillet(18).faces(">Z").workplane().hole(P.CONE_TOP_D - 4)
             .val().translate((0, 0, z0 + h)))
    parts.append(("cone frame", frame, STEEL_DK, "304"))
    for sx in (-1, 1):
        x = sx * (P.CONE_TOP_D / 2 - 10)
        y = -(P.CONE_TOP_D / 2 + 22)
        base = cq.Workplane("XY").box(26, 14, 34).val().translate((x, y, z0 + h - 10))
        bar = cq.Workplane("XY").box(8, 8, 70).val().translate((x, y - 10, z0 + h - 52))
        grip = cq.Workplane("XY").cylinder(40, 6).val().translate((x, y - 14, z0 + h - 70))
        parts.append((f"toggle latch {sx:+d}", base.fuse(bar), STEEL, "304"))
        parts.append((f"latch grip {sx:+d}", grip, GREEN, "plastic"))
    for sx in (-1, 1):  # cooling-water hose barbs on the jacket
        barb = (cq.Workplane("YZ").circle(6).extrude(30).val()
                .translate((sx * (r_bot + 40), 0, z0 + 35)))
        if sx < 0:
            barb = barb.translate((-30, 0, 0))
        parts.append((f"jacket water fitting {sx:+d}", barb, STEEL_DK, "304"))
    return parts


# ------------------------------------------------------------------------------------------- stock cup
def _stock_z():
    """Heights (z) of the stock cup's interfaces, top to bottom (see stock_cup)."""
    kf, s = P.JOINT, P.STOCK
    z = {"face": -kf.ring_thk / 2}
    z["neck"] = z["face"] - s["neck_len"]
    z["valve_top"] = z["neck"] - s["reducer_len"]
    z["valve_bot"] = z["valve_top"] - s["valve_body_h"]
    z["plate_bot"] = z["valve_bot"] - s["top_plate_t"]          # underside of the top plate
    gk = 2.0                                                     # gasket under each glass end
    z["glass_top"] = z["plate_bot"] + s["seal_groove_d"] - gk
    z["glass_bot"] = z["glass_top"] - s["glass_len"]
    z["bplate_top"] = z["glass_bot"] - gk + s["seal_groove_d"]
    z["bottom"] = z["bplate_top"] - s["bottom_plate_t"]
    return z


def _plate(od, t, z_top, groove_face, bore=0.0):
    """Plate with the glass groove in one face and the four tie-rod holes; groove_face 'top' or 'bottom'."""
    s = P.STOCK
    ro, ri = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]
    g_out, g_in = ro + 1.5, ri - 1.5
    pl = cq.Workplane("XY").circle(od / 2).extrude(t).val().translate((0, 0, z_top - t))
    if bore:
        pl = pl.cut(tube(bore / 2, 0, z_top - t - 1, z_top + 1))
    zg = z_top - s["seal_groove_d"] if groove_face == "top" else z_top - t
    pl = pl.cut(tube(g_out, g_in, zg - 0.01 if groove_face == "bottom" else zg, zg + s["seal_groove_d"] + 0.01))
    for i in range(s["n_tie"]):
        a_ = math.radians(45 + 90 * i)
        pl = pl.cut(cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.5).val()
                    .translate((s["tie_rod_bc"] / 2 * math.cos(a_), s["tie_rod_bc"] / 2 * math.sin(a_), z_top - 100)))
    return pl


def stock_cup(glass="borosilicate", valve=True):
    """The AMAZEMET glass cup in the layout measured in dims/README.md: KF-50 flange and neck, conical reducer,
    DN65 butterfly valve (EPDM seat, lever), top plate, glass in a perforated guard, bottom plate, 4 x M12 tie
    rods with hex nuts below and acorn nuts above, and the curved splash plate below the valve seat.
    Sizes in params.STOCK; many are +/- 10 % (dims/). valve=False leaves the valve parts out (option C)."""
    kf, s = P.JOINT, P.STOCK
    z = _stock_z()
    parts = []
    parts.append(("stock: KF flange and neck", kf_flange(kf, z["face"], down=True, tube_len=s["neck_len"]), STEEL, "316L"))
    r1, r2 = kf.tube_od / 2, s["reducer_d2"] / 2
    zr, L = z["neck"], s["reducer_len"]
    red = [(kf.bore / 2, zr), (r1, zr), (r2, zr - L), (r2 - 1.6, zr - L), (kf.bore / 2 + 0.2, zr - 2.0)]
    parts.append(("stock: conical reducer", revolve(red), STEEL, "316L"))
    zt, zb = z["valve_top"], z["valve_bot"]
    zc = (zt + zb) / 2
    if valve:
        vb = tube(s["valve_body_od"] / 2, s["valve_bore"] / 2, zb, zt)
        vb = vb.cut(tube(s["valve_bore"] / 2 + 2.05, s["valve_bore"] / 2 - 1, zc - 10.05, zc + 10.05))
        boss = cq.Workplane("YZ").circle(13).extrude(36).val().translate((s["valve_body_od"] / 2 - 4, 0, zc))
        vb = vb.fuse(boss.cut(tube(s["valve_bore"] / 2 + 2.05, 0.0, zc - 30, zc + 30)))
        for i in range(4):   # body bolts with acorn nuts on top (the bolts clamp the two body halves)
            a_ = math.radians(90 * i)
            vb = vb.cut(cq.Workplane("XY").cylinder(400, 4.5).val()
                        .translate((47.5 * math.cos(a_), 47.5 * math.sin(a_), zc)))
        parts.append(("stock: butterfly valve body (DN65)", vb, STEEL, "316L"))
        parts.append(("stock: valve seat ring (EPDM)", tube(s["valve_bore"] / 2 + 2.0, s["valve_bore"] / 2 - 3.0,
                                                          zc - 10, zc + 10), EPDM, "EPDM"))
        disc = cq.Workplane("YZ").circle(s["valve_bore"] / 2 - 3.2).extrude(4).val().translate((-2, 0, zc))
        parts.append(("stock: valve disc (open, edge-on)", disc, STEEL_DK, "316L"))
        lever = (cq.Workplane("YZ").circle(5).extrude(95).val().rotate((0, 0, 0), (0, 0, 1), -35)
                 .translate((s["valve_body_od"] / 2 + 36.0, 0, zc)))
        lx = s["valve_body_od"] / 2 + 36.0 + 95 * math.cos(math.radians(-35))
        ly = 95 * math.sin(math.radians(-35))
        knob = cq.Workplane("XY").sphere(14).val().translate((lx, ly, zc))
        parts.append(("stock: valve lever", lever.cut(knob), STEEL, "316L"))
        parts.append(("stock: lever knob", knob, BLACK, "plastic"))
        for i in range(4):
            a_ = math.radians(90 * i)
            x, y = 47.5 * math.cos(a_), 47.5 * math.sin(a_)
            bolt = cq.Workplane("XY").cylinder(s["valve_body_h"] + 6, 4.0).val().translate((x, y, zc + 3))
            nut = (cq.Workplane("XY").polygon(6, 13 / math.cos(math.pi / 6)).extrude(6).val().translate((x, y, zt))
                   .fuse(cq.Workplane("XY").sphere(6.0).val().translate((x, y, zt + 6))))
            parts.append((f"stock: valve bolt {i}", bolt, STEEL, "A2"))
            parts.append((f"stock: valve acorn nut {i}", nut.cut(cq.Workplane("XY").cylinder(400, 4.05).val()
                                                              .translate((x, y, zt))), STEEL, "A2"))
        # splash plate: a curved strip just below the seat, across about half the bore
        rs = s["valve_bore"] / 2 - 1.0
        sp = (cq.Workplane("XY").circle(rs).circle(rs - 2.0).extrude(22).val()
              .cut(cq.Workplane("XY").box(200, 200, 60).val().translate((0, -100 + 4, 0))))
        parts.append(("stock: splash plate", sp.translate((0, 0, zb - 12.0)), STEEL, "304"))
    parts.append(("stock: top plate", _plate(s["top_plate_od"], s["top_plate_t"], zb, "bottom",
                                             bore=s["valve_bore"]), STEEL, "316L"))
    ro, ri = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]
    g_out, g_in = ro + 1.5, ri - 1.5
    gl = tube(ro, ri, z["glass_bot"], z["glass_top"])
    gname = "stock: glass tube (borosilicate)" if glass == "borosilicate" else "glass tube (fused quartz)"
    parts.append((gname, gl, GLASS if glass == "borosilicate" else QUARTZ, glass))
    parts.append(("stock: top glass seal", tube(g_out, g_in, z["glass_top"], z["glass_top"] + 2.0), EPDM, "EPDM"))
    parts.append(("stock: bottom glass seal", tube(g_out, g_in, z["glass_bot"] - 2.0, z["glass_bot"]), EPDM, "EPDM"))
    parts.append(("stock: bottom plate", _plate(s["bottom_plate_od"], s["bottom_plate_t"], z["bplate_top"], "top"),
                  STEEL, "316L"))
    zt_rod, zb_rod = zb + 14.0, z["bottom"] - 12.0
    for i in range(s["n_tie"]):
        a_ = math.radians(45 + 90 * i)
        x, y = s["tie_rod_bc"] / 2 * math.cos(a_), s["tie_rod_bc"] / 2 * math.sin(a_)
        rod = cq.Workplane("XY").cylinder(zt_rod - zb_rod, s["tie_rod_d"] / 2).val().translate((x, y, (zt_rod + zb_rod) / 2))
        parts.append((f"stock: tie rod {i}", rod, STEEL, "A2"))
        for zn, name in ((z["bottom"] - 10.0, "nut"), (zb, "acorn nut")):
            nut = cq.Workplane("XY").polygon(6, 18 / math.cos(math.pi / 6)).extrude(10).val().translate((x, y, zn))
            if name == "acorn nut":
                nut = nut.fuse(cq.Workplane("XY").sphere(9.0).val().translate((x, y, zn + 10)))
            nut = nut.cut(cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.05).val().translate((x, y, zn)))
            parts.append((f"stock: {name} {i}", nut, STEEL, "A2"))
    guard = tube(s["guard_od"] / 2, s["guard_od"] / 2 - s["guard_t"], z["bplate_top"] + 0.01, z["plate_bot"] - 0.01)
    n_around, n_up = 14, 4
    h_win = (z["plate_bot"] - z["bplate_top"] - 14) / n_up - 5
    for j in range(n_up):
        zz = z["bplate_top"] + 8 + j * (h_win + 5) + h_win / 2
        for i in range(n_around):
            a_ = 360.0 * i / n_around
            win = cq.Workplane("XY").box(30, 2 * math.pi * s["guard_od"] / 2 / n_around - 6, h_win).val()
            guard = guard.cut(win.translate((s["guard_od"] / 2, 0, zz)).rotate((0, 0, 0), (0, 0, 1), a_))
    parts.append(("stock: perforated guard", guard, STEEL_DK, "304"))
    return parts


# ------------------------------------------------------------------------------------------- option A
def option_a(with_liner=True, with_puck=True, explode=0.0):
    """Catalogue cup: KF full nipple, KF blank, centring rings, clamps, liner, catch puck."""
    kf = P.JOINT
    a = P.A
    g = kf.ring_thk / 2
    parts = []
    L = a["nipple_len"]
    top_face = -g - explode
    bot_face = top_face - L
    rb, rt = kf.bore / 2, kf.tube_od / 2
    upper = kf_flange(kf, top_face, down=True, tube_len=L / 2)
    lower = kf_flange(kf, bot_face, down=False, tube_len=L / 2)
    parts.append(("A: KF-50 full nipple", upper.fuse(lower), STEEL, "316L"))
    ring, oring = kf_centring_ring(kf, bot_face - g)
    blank_face = bot_face - 2 * g - 1.5 * explode
    ring = ring.translate((0, 0, -0.5 * explode))
    oring = oring.translate((0, 0, -0.5 * explode))
    parts.append(("A: bottom centring ring (stainless)", ring, STEEL_DK, "304"))
    parts.append(("A: bottom O-ring (FKM)", oring, FKM, "FKM"))
    parts.append(("A: KF-50 blank", kf_blank(kf, blank_face), STEEL, "304"))
    parts.append(("A: bottom clamp", kf_clamp(kf, (bot_face + blank_face) / 2), STEEL, "304"))
    floor = bot_face
    if with_puck:
        z0 = blank_face - kf.recess_depth + 0.2          # on the floor of the blank's recess, inside the ring
        puck = (cq.Workplane("XY").circle(a["puck_d"] / 2).extrude(a["puck_h"])
                .edges().chamfer(a["puck_chamfer"]).val().translate((0, 0, z0 + explode * 0.6)))
        parts.append(("A: catch puck (304)", puck, STEEL_HOT, "304"))
        floor = z0 + a["puck_h"]
    else:
        floor = blank_face
    if with_liner:
        l_len = (top_face - a["liner_gap_top"]) - (floor + 0.2)
        liner = tube(a["liner_od"] / 2, a["liner_od"] / 2 - a["liner_wall"], floor + 0.2 + explode * 1.2,
                     floor + 0.2 + l_len + explode * 1.2)
        parts.append(("A: sacrificial liner (304)", liner, (0.70, 0.72, 0.76), "304"))
    return parts


# ------------------------------------------------------------------------------------------- option B
def option_b_vessel_profile(recess=True):
    """(r, z) outline of the welded vessel, sealing face at z = -gap/2."""
    kf = P.JOINT
    b = P.B
    g = kf.ring_thk / 2
    top = -g
    rb, rt = kf.bore / 2, kf.tube_od / 2
    rf, rh = kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    R_o, R_i = b["body_od"] / 2, b["body_od"] / 2 - b["body_wall"]
    z_stub = top - b["stub_len"]
    z_red = z_stub - b["reducer_len"]
    z_bot = top - b["body_len"]
    tan_len = 8.0   # straight ends of the sanitary reducer
    outer = [(rf, top), (rf, top - t_edge), (rh, top - kf.lip), (rt, top - kf.lip - 1.5), (rt, z_stub - tan_len),
             (R_o, z_red + tan_len), (R_o, z_bot)]
    fl, fr = z_bot + b["bottom_t"], b.get("bottom_fillet", 0.0)
    arc = [(R_i - fr + fr * math.sin(math.radians(a)), fl + fr - fr * math.cos(math.radians(a)))
           for a in np.linspace(0, 90, 10)] if fr else [(R_i, fl)]
    inner = [(0, z_bot), (0, fl)] + arc + [(R_i, z_red + tan_len), (rb, z_stub - tan_len), (rb, top)]
    if recess and kf.recess_depth:
        rr, rd = kf.recess_d / 2, kf.recess_depth
        inner = inner[:-1] + [(rb, top - rd), (rr, top - rd), (rr, top)]
    return outer + inner, dict(top=top, z_stub=z_stub, z_red=z_red, z_bot=z_bot, R_o=R_o, R_i=R_i,
                               floor=z_bot + b["bottom_t"], z_cap=z_bot + b["bottom_t"] + b.get("bottom_rim", 0.0))


def b_split_profiles(recess=True):
    """B split at a 3 in tri-clamp where the reducer meets the tube. Returns (upper, pot, gasket, z):
    upper = KF-50 stub + 3x2 reducer + ferrule A (face down); pot = ferrule B (face up) + 3 in tube + end cap."""
    kf, tc, b = P.JOINT, P.TC3, P.B
    full, z = option_b_vessel_profile(recess)
    top, z_stub, z_red = z["top"], z["z_stub"], z["z_red"]
    rb, rt, rf, rh = kf.bore / 2, kf.tube_od / 2, kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    R_o, R_i = z["R_o"], z["R_i"]
    tan_len = 8.0
    fl = b["ferrule_len"]
    trf, trh = tc.flange_od / 2, tc.hub_od / 2
    t_edge3 = tc.lip - (trf - trh) * math.tan(math.radians(tc.taper_deg))
    z_fA = z_red - fl                      # ferrule A's face (down)
    z_fB = z_fA - b["gasket_t"]            # ferrule B's face (up)
    z_tt = z_fB - fl                       # tube top (ferrule B's tube end): weld W2b
    upper = [(rf, top), (rf, top - t_edge), (rh, top - kf.lip), (rt, top - kf.lip - 1.5), (rt, z_stub - tan_len),
             (R_o, z_red + tan_len), (R_o, z_fA + tc.lip + 1.5), (trh, z_fA + tc.lip), (trf, z_fA + t_edge3),
             (trf, z_fA), (R_i, z_fA), (R_i, z_red + tan_len), (rb, z_stub - tan_len), (rb, top)]
    if recess and kf.recess_depth:
        rr, rd = kf.recess_d / 2, kf.recess_depth
        upper = upper[:-1] + [(rb, top - rd), (rr, top - rd), (rr, top)]
    flr, fr = z["floor"], b.get("bottom_fillet", 0.0)
    arc = [(R_i - fr + fr * math.sin(math.radians(a)), flr + fr - fr * math.cos(math.radians(a)))
           for a in np.linspace(0, 90, 10)] if fr else [(R_i, flr)]
    pot = [(trf, z_fB), (trf, z_fB - t_edge3), (trh, z_fB - tc.lip), (R_o, z_fB - tc.lip - 1.5), (R_o, z["z_bot"]),
           (0, z["z_bot"]), (0, flr)] + arc + [(R_i, z_fB)]
    gasket = [(R_i, z_fB), (trf, z_fB), (trf, z_fA), (R_i, z_fA)]
    z = dict(z, z_fA=z_fA, z_fB=z_fB, z_tt=z_tt, z_joint=(z_fA + z_fB) / 2)
    return upper, pot, gasket, z


def b_adapter_profiles(recess=True):
    """Next-step variant of B's upper part (concept, not drawn or CAM'd): one turned 316L adapter from 4 in bar,
    KF-50 flange on top, a neck for the KF clamp, an internal 45 deg cone from the 47.5 bore to the 72.9 bore, and
    a 3 in tri-clamp ferrule face at the bottom, 32.7 mm below the KF face. The pot is the same as in
    b_split_profiles but its tube is longer, so the joint sits about 100 mm higher above the pile."""
    kf, tc, b = P.JOINT, P.TC3, P.B
    full, z = option_b_vessel_profile(recess)
    top = z["top"]
    rb, rf, rh = kf.bore / 2, kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    R_o, R_i = z["R_o"], z["R_i"]
    trf, trh = tc.flange_od / 2, tc.hub_od / 2
    t_edge3 = tc.lip - (trf - trh) * math.tan(math.radians(tc.taper_deg))
    z_neck = top - 16.0                                  # below the KF clamp's lower lip
    z_hub3 = z_neck - (trh - rh)                         # 45 deg out to the ferrule's hub
    z_fA = z_hub3 - tc.lip                               # ferrule face
    z_cone0 = top - 18.0
    z_cone1 = z_cone0 - (R_i - rb)                       # 45 deg inside, 47.5 -> 72.9
    up = [(rf, top), (rf, top - t_edge), (rh, top - kf.lip), (rh, z_neck), (trh, z_hub3), (trf, z_fA + t_edge3),
          (trf, z_fA), (R_i, z_fA), (R_i, z_cone1), (rb, z_cone0), (rb, top)]
    if recess and kf.recess_depth:
        rr, rd = kf.recess_d / 2, kf.recess_depth
        up = up[:-1] + [(rb, top - rd), (rr, top - rd), (rr, top)]
    z_fB = z_fA - b["gasket_t"]
    flr, fr = z["floor"], b.get("bottom_fillet", 0.0)
    arc = [(R_i - fr + fr * math.sin(math.radians(a)), flr + fr - fr * math.cos(math.radians(a)))
           for a in np.linspace(0, 90, 10)] if fr else [(R_i, flr)]
    pot = [(trf, z_fB), (trf, z_fB - t_edge3), (trh, z_fB - tc.lip), (R_o, z_fB - tc.lip - 1.5), (R_o, z["z_bot"]),
           (0, z["z_bot"]), (0, flr)] + arc + [(R_i, z_fB)]
    gasket = [(R_i, z_fB), (trf, z_fB), (trf, z_fA), (R_i, z_fA)]
    z = dict(z, z_fA=z_fA, z_fB=z_fB, z_tt=z_fB - b["ferrule_len"], z_joint=(z_fA + z_fB) / 2,
             z_cone0=z_cone0, z_cone1=z_cone1)
    return up, pot, gasket, z


def puck_profile_b(z0=0.0):
    """B's catch puck: 2 x 45 deg on top, 6 x 45 deg underneath so it clears the cap's R6 inside corner."""
    b = P.B
    R, h, c, cb = b["puck_d"] / 2, b["puck_h"], b["puck_chamfer"], b.get("puck_chamfer_bottom", b["puck_chamfer"])
    return [(0, z0), (R - cb, z0), (R, z0 + cb), (R, z0 + h - c), (R - c, z0 + h), (0, z0 + h)]


def option_b(with_liner=None, with_puck=True, explode=0.0, tcs=True, adapter=False):
    """Welded 316L cup: KF stub + 2x3 in reducer + 3 in tube + 8 mm bottom disc; liner, puck, thermocouples.
    adapter=True: the next-step variant, a turned KF-50 to 3 in adapter in place of the welded upper part (concept)."""
    kf = P.JOINT
    b = P.B
    if with_liner is None:
        with_liner = b.get("liner", True)
    prof, z = option_b_vessel_profile()
    z_liner_top = (b_split_profiles()[3]["z_fB"] - 3.0) if b.get("split") else z["z_red"] + 8.0 - 3.0
    if adapter:
        up, pot, gk, z = b_adapter_profiles()
        parts = [("B': turned KF-50 to 3 in adapter (316L)", revolve(up), STEEL, "316L"),
                 ("B': tri-clamp gasket 3 in (PTFE)", revolve(gk).translate((0, 0, -explode * 0.5)), FKM, "FKM"),
                 ("B': pot (3 in ferrule + tube + end cap), welded", revolve(pot).translate((0, 0, -explode)),
                  STEEL, "316L"),
                 ("B': 3 in tri-clamp", kf_clamp(P.TC3, z["z_joint"]), STEEL_DK, "304")]
    elif b.get("split"):
        up, pot, gk, z = b_split_profiles()
        parts = [("B: upper (KF-50 stub + 3x2 reducer + 3 in ferrule), welded", revolve(up), STEEL, "316L"),
                 ("B: tri-clamp gasket 3 in (FKM)", revolve(gk).translate((0, 0, -explode * 0.5)), FKM, "FKM"),
                 ("B: lower pot (3 in ferrule + tube + end cap), welded", revolve(pot).translate((0, 0, -explode)),
                  STEEL, "316L"),
                 ("B: 3 in tri-clamp", kf_clamp(P.TC3, z["z_joint"]), STEEL_DK, "304")]
    else:
        vessel = revolve(prof).translate((0, 0, -explode))
        parts = [("B: welded 316L vessel", vessel, STEEL, "316L")]
    # weld beads (visual only, not separate parts in the interference check)
    # W1: stub's tube end to the reducer's 2 in end; W2: reducer's 3 in end to the tube; W3: tube end to the disc
    welds = [(z["z_stub"], kf.tube_od / 2), (z["z_red"], z["R_o"]), (z["z_cap"], z["R_o"])]
    if b.get("split"):
        welds.append((z["z_tt"], z["R_o"]))
    if adapter:
        welds = [(z["z_tt"], z["R_o"]), (z["z_cap"], z["R_o"])]
    for zz, rr in welds:
        bead = (cq.Workplane("XZ").center(rr + 0.2, zz - explode).circle(1.6)
                .revolve(360, (-(rr + 0.2), 0, 0), (-(rr + 0.2), 1, 0)).val())
        parts.append((f"B: weld bead z={zz:.0f}", bead, STEEL_HOT, "weld"))
    floor = z["floor"] - explode
    if with_puck:
        puck = revolve(puck_profile_b()).translate((0, 0, floor + 0.2 - explode * 0.4))
        parts.append(("B: catch puck (304)", puck, STEEL_HOT, "304"))
        floor = floor + 0.2 + b["puck_h"]
    if with_liner:
        top = z_liner_top - explode
        liner = tube(b["liner_od"] / 2, b["liner_od"] / 2 - b["liner_wall"], floor + 0.2 - explode * 0.8,
                     top - explode * 0.8)
        parts.append(("B: sacrificial liner (304)", liner, (0.70, 0.72, 0.76), "304"))
    if tcs:
        # 9 mm stainless bands. Top: on the stub's 12.6 mm of straight tube, clear of the hub and of weld W1 at the
        # stub's end. Bottom: on the end cap's rim, 13.5 mm up from the bottom face, clear of W3 at 20 mm.
        z_tc = (z["top"] - kf.lip - 1.5 + z["z_stub"]) / 2
        r_tc = kf.tube_od / 2
        if adapter:                       # on the adapter's neck, between the KF flange's hub and the 45 deg shoulder
            z_tc, r_tc = z["top"] - (kf.lip + 16.0) / 2, kf.hub_od / 2
        for zz, rr, nm, hw in ((z_tc, r_tc, "top", 4.5), (z["z_bot"] + 13.5, z["R_o"], "bottom", 4.5)):
            band = tube(rr + 1.6, rr + 0.05, zz - hw - explode, zz + hw - explode)
            parts.append((f"B: thermocouple band clamp ({nm})", band, STEEL_DK, "304"))
            tc = (cq.Workplane("YZ").circle(1.6).extrude(60).val().translate((rr + 1.2, 0, zz - explode)))
            parts.append((f"B: type K thermocouple ({nm})", tc, BRASS_TC, "TC"))
    return parts


# ------------------------------------------------------------------------------------------- the joint
def joint_hardware(open_deg=0.0, drop=0.0):
    """The cone joint's own centring ring, O-ring and clamp (existing machine hardware), at z = 0."""
    kf = P.JOINT
    ring, oring = kf_centring_ring(kf, 0.0)
    return [("joint: centring ring", ring.translate((0, 0, -drop)), STEEL_DK, "304"),
            ("joint: O-ring (FKM)", oring.translate((0, 0, -drop)), FKM, "FKM"),
            ("joint: over-pressure ring", kf_overpressure_ring(0.0).translate((0, 0, -drop)), STEEL_DK, "304"),
            ("joint: KF clamp", kf_clamp(kf, 0.0, open_deg=open_deg), STEEL, "304")]


# ------------------------------------------------------------------------------------------- option C
def option_c():
    """Glass rebuild (schematic: it assumes the valve can be unbolted from the reducer and the top plate,
    which has not been checked): the stock cup with a fused-quartz tube and FKM seals, the valve replaced
    by a machined 316L spacer of the same OD and height, a 304 sleeve hung in the spacer that reaches 20 mm
    past the top glass seal, and a 304 pan on the bottom plate that keeps the pile off the bottom seal."""
    s, c, kf = P.STOCK, P.C, P.JOINT
    z = _stock_z()
    out = []
    for name, solid, col, mat in stock_cup(glass="fused_quartz", valve=False):
        if "seal" in name and "glass" in name:
            out.append((name.replace("stock: ", "C: ") + " (FKM)", solid, FKM, "FKM"))
        else:
            out.append((name, solid, col, mat))
    zt, zb = z["valve_top"], z["valve_bot"]
    lip_t = 3.0
    sp = tube(s["valve_body_od"] / 2, c["sleeve_od"] / 2 + 0.4, zb, zt)
    sp = sp.cut(tube(c["sleeve_lip_od"] / 2 + 0.4, 0, zt - lip_t, zt + 1))      # counterbore for the lip
    for i in range(4):
        a_ = math.radians(90 * i)
        sp = sp.cut(cq.Workplane("XY").cylinder(400, 4.5).val().translate((47.5 * math.cos(a_), 47.5 * math.sin(a_), zb)))
    out.append(("C: valve-delete spacer (316L, machined)", sp, STEEL, "316L"))
    sl_bot = z["glass_top"] - 20.0
    sleeve = tube(c["sleeve_od"] / 2, c["sleeve_od"] / 2 - c["sleeve_wall"], sl_bot, zt - lip_t)
    sleeve = sleeve.fuse(tube(c["sleeve_lip_od"] / 2, c["sleeve_od"] / 2 - c["sleeve_wall"], zt - lip_t, zt))
    out.append(("C: 304 entrance sleeve", sleeve, (0.70, 0.72, 0.76), "304"))
    ri = s["glass_od"] / 2 - c["quartz_wall"]
    pan_od = 2 * (s["glass_od"] / 2 - s["glass_wall"]) - 3.0
    pan = (cq.Workplane("XY").circle(pan_od / 2).extrude(28.0).faces(">Z").shell(-1.5).val()
           .translate((0, 0, z["bplate_top"] + 0.05)))
    out.append(("C: 304 bottom pan", pan, STEEL_HOT, "304"))
    return out
