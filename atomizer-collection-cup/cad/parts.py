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


def kf_flange_profile(kf, face_z, down=True, tube_len=20.0):
    """(r, z) profile of an ISO-KF flange with its weld tube. Sealing face at face_z.

    down=True: the flange faces up and its tube runs down (the cup side). down=False: mirror (cone side).
    """
    s = -1.0 if down else 1.0
    rb, rf, rh, rt = kf.bore / 2, kf.flange_od / 2, kf.hub_od / 2, kf.tube_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    pts = [(rb, face_z), (rf, face_z), (rf, face_z + s * t_edge), (rh, face_z + s * kf.lip),
           (rt, face_z + s * (kf.lip + 1.5)), (rt, face_z + s * tube_len), (rb, face_z + s * tube_len)]
    return pts


def kf_flange(kf, face_z, down=True, tube_len=20.0):
    return revolve(kf_flange_profile(kf, face_z, down, tube_len))


def kf_blank(kf, face_z):
    """KF blank: a flange with no bore, sealing face up at face_z."""
    rf, rh = kf.flange_od / 2, kf.hub_od / 2
    t_edge = kf.lip - (rf - rh) * math.tan(math.radians(kf.taper_deg))
    pts = [(0, face_z), (rf, face_z), (rf, face_z - t_edge), (rh, face_z - kf.lip), (0, face_z - kf.lip)]
    return revolve(pts)


def kf_centring_ring(kf, z_mid):
    """Metal centring ring plus its O-ring (as a squashed torus), centred on z_mid."""
    h = kf.ring_thk
    ring = tube(kf.ring_od / 2, kf.ring_id / 2, z_mid - h / 2, z_mid + h / 2)
    # small outer lip that holds the O-ring
    r_c = kf.ring_od / 2 + kf.oring_cs * 0.56 + 0.05
    oring = (cq.Workplane("XZ").center(r_c, z_mid).ellipse(kf.oring_cs / 2 * 1.12, h / 2 * 0.98)
             .revolve(360, (-r_c, 0, 0), (-r_c, 1, 0)).val())
    return ring, oring


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
def stock_cup(glass="borosilicate"):
    """The AMAZEMET glass cup as seen in the videos (rough sizes in params.STOCK until measured)."""
    kf = P.JOINT
    s = P.STOCK
    g = kf.ring_thk / 2
    parts = []
    z = -g
    parts.append(("stock: KF flange and neck", kf_flange(kf, z, down=True, tube_len=s["neck_len"]), STEEL, "316L"))
    z -= s["neck_len"]
    r1, r2 = kf.tube_od / 2, s["reducer_d2"] / 2
    red = [(kf.bore / 2, z), (r1, z), (r2, z - s["reducer_len"]), (r2 - 1.6, z - s["reducer_len"]),
           (kf.bore / 2 - 0.5, z - 1.5)]
    red = [(kf.bore / 2, z), (r1, z), (r2, z - s["reducer_len"]), (r2 - 1.6, z - s["reducer_len"]),
           (kf.bore / 2 + 0.2, z - 2.0)]
    parts.append(("stock: conical reducer", revolve(red), STEEL, "316L"))
    z -= s["reducer_len"]
    # valve body = thick top block with a flap valve and a side lever
    vb = (cq.Workplane("XY").circle(s["valve_body_od"] / 2).circle(s["valve_bore"] / 2)
          .extrude(s["valve_body_h"]).val().translate((0, 0, z - s["valve_body_h"])))
    for i in range(s["n_tie"]):
        a = math.radians(45 + 90 * i)
        hole = (cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.5).val()
                .translate((s["tie_rod_bc"] / 2 * math.cos(a), s["tie_rod_bc"] / 2 * math.sin(a), z - 100)))
        vb = vb.cut(hole)
    parts.append(("stock: valve body / top block", vb, STEEL, "316L"))
    zc = z - s["valve_body_h"] / 2
    seat = tube(s["valve_bore"] / 2 + 2.0, s["valve_bore"] / 2 - 3.0, zc - 10, zc + 10)
    vb = vb.cut(tube(s["valve_bore"] / 2 + 2.05, s["valve_bore"] / 2 - 1, zc - 10.05, zc + 10.05))
    parts[-1] = ("stock: valve body / top block", vb, STEEL, "316L")
    parts.append(("stock: valve seat ring (EPDM)", seat, EPDM, "EPDM"))
    disc = (cq.Workplane("YZ").circle(s["valve_bore"] / 2 - 3.2).extrude(4).val()
            .translate((-2, 0, zc)))
    parts.append(("stock: valve flap (open, edge-on)", disc, STEEL_DK, "316L"))
    boss = (cq.Workplane("YZ").circle(13).extrude(36).val().translate((s["valve_body_od"] / 2 - 4, 0, zc)))
    lever = (cq.Workplane("YZ").circle(5).extrude(95).val().rotate((0, 0, 0), (0, 0, 1), -35)
             .translate((s["valve_body_od"] / 2 + 35, 0, zc)))
    knob = cq.Workplane("XY").sphere(14).val()
    lx = s["valve_body_od"] / 2 + 35 + 95 * math.cos(math.radians(-35))
    ly = 95 * math.sin(math.radians(-35))
    knob = knob.translate((lx, ly, zc))
    vb = vb.fuse(boss.cut(tube(s["valve_bore"] / 2 + 2.05, 0.0, zc - 30, zc + 30)))
    parts[[q[0] for q in parts].index("stock: valve body / top block")] = (
        "stock: valve body / top block", vb, STEEL, "316L")
    lever = lever.cut(knob)
    parts.append(("stock: valve lever", lever, STEEL, "316L"))
    parts.append(("stock: lever knob", knob, BLACK, "plastic"))
    z -= s["valve_body_h"]
    # glass, seals, bottom plate: each glass end sits on a 2 mm gasket at the bottom of a groove
    ro, ri = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]
    gd, gk = s["seal_groove_d"], 2.0
    g_out, g_in = ro + 1.5, ri - 1.5
    vb_groove = tube(g_out, g_in, z - 0.01, z + gd)
    i_vb = [q[0] for q in parts].index("stock: valve body / top block")
    parts[i_vb] = ("stock: valve body / top block", parts[i_vb][1].cut(vb_groove), STEEL, "316L")
    zt = z + gd - gk                      # top end of the glass
    zg = zt - s["glass_len"]              # bottom end of the glass
    gl = tube(ro, ri, zg, zt)
    gname = "stock: glass tube (borosilicate)" if glass == "borosilicate" else "glass tube (fused quartz)"
    parts.append((gname, gl, GLASS if glass == "borosilicate" else QUARTZ, glass))
    parts.append(("stock: top glass seal", tube(g_out, g_in, zt, zt + gk), EPDM, "EPDM"))
    parts.append(("stock: bottom glass seal", tube(g_out, g_in, zg - gk, zg), EPDM, "EPDM"))
    zb = zg - gk + gd                     # top face of the bottom plate
    bp = cq.Workplane("XY").circle(s["bottom_plate_od"] / 2).extrude(s["bottom_plate_t"]).val()
    bp = bp.translate((0, 0, zb - s["bottom_plate_t"]))
    bp = bp.cut(tube(g_out, g_in, zb - gd, zb + 0.01))
    for i in range(s["n_tie"]):
        a = math.radians(45 + 90 * i)
        hole = (cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.5).val()
                .translate((s["tie_rod_bc"] / 2 * math.cos(a), s["tie_rod_bc"] / 2 * math.sin(a), zb - 100)))
        bp = bp.cut(hole)
    parts.append(("stock: bottom plate", bp, STEEL, "316L"))
    z_bot = zb - s["bottom_plate_t"]
    z_top = z + s["valve_body_h"]
    for i in range(s["n_tie"]):
        a = math.radians(45 + 90 * i)
        x, y = s["tie_rod_bc"] / 2 * math.cos(a), s["tie_rod_bc"] / 2 * math.sin(a)
        rod = cq.Workplane("XY").cylinder(z_top - z_bot + 22, s["tie_rod_d"] / 2).val()
        rod = rod.translate((x, y, (z_top + z_bot) / 2 + 2))
        parts.append((f"stock: tie rod {i}", rod, STEEL, "A2"))
        for zn, name in ((z_bot - 5.0, "nut"), (z_top + 6.0, "acorn nut")):
            nut = cq.Workplane("XY").polygon(6, s["tie_rod_d"] * 1.5 / math.cos(math.pi / 6)).extrude(10).val()
            nut = nut.translate((x, y, zn - 5))
            if name == "acorn nut":
                nut = nut.fuse(cq.Workplane("XY").sphere(s["tie_rod_d"] * 0.75).val().translate((x, y, zn + 5)))
            nut = nut.cut(cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.05).val().translate((x, y, zn)))
            parts.append((f"stock: {name} {i}", nut, STEEL, "A2"))
    # perforated guard around the glass (square windows), standing on the bottom plate
    guard = tube(s["guard_od"] / 2, s["guard_od"] / 2 - s["guard_t"], zb + 0.01, z - 0.01)
    n_around, n_up = 14, 4
    h_win = (z - zb - 14) / n_up - 5
    for j in range(n_up):
        zz = zb + 8 + j * (h_win + 5) + h_win / 2
        for i in range(n_around):
            a = 360.0 * i / n_around
            win = cq.Workplane("XY").box(30, 2 * math.pi * s["guard_od"] / 2 / n_around - 6, h_win).val()
            win = win.translate((s["guard_od"] / 2, 0, zz)).rotate((0, 0, 0), (0, 0, 1), a)
            guard = guard.cut(win)
    parts.append(("stock: perforated guard", guard, STEEL_DK, "304"))
    # splash plate: a curved strip hooked in the reducer's bore
    rs = kf.bore / 2 - 1.0
    sp = (cq.Workplane("XY").circle(rs).circle(rs - 2.0).extrude(22).val()
          .cut(cq.Workplane("XY").box(200, 200, 60).val().translate((0, -100 + 4, 0))))
    parts.append(("stock: splash plate", sp.translate((0, 0, -g - 30)), STEEL, "304"))
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
        puck = (cq.Workplane("XY").circle(a["puck_d"] / 2).extrude(a["puck_h"])
                .edges().chamfer(a["puck_chamfer"]).val().translate((0, 0, blank_face + 0.2 + explode * 0.6)))
        parts.append(("A: catch puck (304)", puck, STEEL_HOT, "304"))
        floor = blank_face + 0.2 + a["puck_h"]
    else:
        floor = blank_face
    if with_liner:
        l_len = (top_face - a["liner_gap_top"]) - (floor + 0.2)
        liner = tube(a["liner_od"] / 2, a["liner_od"] / 2 - a["liner_wall"], floor + 0.2 + explode * 1.2,
                     floor + 0.2 + l_len + explode * 1.2)
        parts.append(("A: sacrificial liner (304)", liner, (0.70, 0.72, 0.76), "304"))
    return parts


# ------------------------------------------------------------------------------------------- option B
def option_b_vessel_profile():
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
    inner = [(0, z_bot), (0, z_bot + b["bottom_t"]), (R_i, z_bot + b["bottom_t"]), (R_i, z_red + tan_len),
             (rb, z_stub - tan_len), (rb, top)]
    return outer + inner, dict(top=top, z_stub=z_stub, z_red=z_red, z_bot=z_bot, R_o=R_o, R_i=R_i,
                               floor=z_bot + b["bottom_t"])


def option_b(with_liner=True, with_puck=True, explode=0.0, tcs=True):
    """Welded 316L cup: KF stub + 2x3 in reducer + 3 in tube + 8 mm bottom disc; liner, puck, thermocouples."""
    kf = P.JOINT
    b = P.B
    prof, z = option_b_vessel_profile()
    vessel = revolve(prof).translate((0, 0, -explode))
    parts = [("B: welded 316L vessel", vessel, STEEL, "316L")]
    # weld beads (visual only, not separate parts in the interference check)
    for zz, rr in ((z["z_stub"] - 8.0, kf.tube_od / 2), (z["z_red"] + 8.0, z["R_o"]), (z["z_bot"], z["R_o"])):
        bead = (cq.Workplane("XZ").center(rr + 0.2, zz - explode).circle(1.6)
                .revolve(360, (-(rr + 0.2), 0, 0), (-(rr + 0.2), 1, 0)).val())
        parts.append((f"B: weld bead z={zz:.0f}", bead, STEEL_HOT, "weld"))
    floor = z["floor"] - explode
    if with_puck:
        puck = (cq.Workplane("XY").circle(b["puck_d"] / 2).extrude(b["puck_h"])
                .edges().chamfer(b["puck_chamfer"]).val().translate((0, 0, floor + 0.2 - explode * 0.4)))
        parts.append(("B: catch puck (304)", puck, STEEL_HOT, "304"))
        floor = floor + 0.2 + b["puck_h"]
    if with_liner:
        top = z["z_red"] + 8.0 - 3.0 - explode
        liner = tube(b["liner_od"] / 2, b["liner_od"] / 2 - b["liner_wall"], floor + 0.2 - explode * 0.8,
                     top - explode * 0.8)
        parts.append(("B: sacrificial liner (304)", liner, (0.70, 0.72, 0.76), "304"))
    if tcs:
        for zz, rr, nm in ((z["top"] - kf.lip - 9.0, kf.tube_od / 2, "top"), (z["floor"] + 6.0, z["R_o"], "bottom")):
            band = tube(rr + 1.6, rr + 0.05, zz - 6 - explode, zz + 6 - explode)
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
            ("joint: KF clamp", kf_clamp(kf, 0.0, open_deg=open_deg), STEEL, "304")]


# ------------------------------------------------------------------------------------------- option C
def option_c():
    """Glass rebuild: the stock cup with a fused-quartz tube and FKM seals, the valve replaced by a
    machined 316L spacer of the same height and tie-rod pattern, a 304 sleeve hung in the spacer that
    reaches past the top glass seal, and a 304 pan on the bottom plate that covers the bottom seal."""
    s = P.STOCK
    c = P.C
    kf = P.JOINT
    out = []
    for name, solid, col, mat in stock_cup(glass="fused_quartz"):
        if any(k in name for k in ("valve seat", "valve flap", "valve lever", "lever knob")):
            continue
        if "valve body" in name:
            continue
        if "seal" in name and "glass" in name:
            out.append((name.replace("stock: ", "C: ") + " (FKM)", solid, FKM, "FKM"))
        else:
            out.append((name, solid, col, mat))
    g = kf.ring_thk / 2
    z_top = -g - s["neck_len"] - s["reducer_len"]       # top face of the old valve body
    z_bot = z_top - s["valve_body_h"]
    lip_t = 3.0
    sp = (cq.Workplane("XY").circle(s["valve_body_od"] / 2).circle(c["sleeve_od"] / 2 + 0.4)
          .extrude(s["valve_body_h"]).val().translate((0, 0, z_bot)))
    sp = sp.cut(tube(c["sleeve_lip_od"] / 2 + 0.4, 0, z_top - lip_t, z_top + 1))     # counterbore for the lip
    ro, ri = s["glass_od"] / 2, s["glass_od"] / 2 - s["glass_wall"]
    sp = sp.cut(tube(ro + 1.5, ri - 1.5, z_bot - 0.01, z_bot + s["seal_groove_d"]))  # glass groove
    for i in range(s["n_tie"]):
        a = math.radians(45 + 90 * i)
        sp = sp.cut(cq.Workplane("XY").cylinder(400, s["tie_rod_d"] / 2 + 0.5).val()
                    .translate((s["tie_rod_bc"] / 2 * math.cos(a), s["tie_rod_bc"] / 2 * math.sin(a), z_bot)))
    out.append(("C: valve-delete spacer (316L, machined)", sp, STEEL, "316L"))
    z_glass_top = z_bot + s["seal_groove_d"] - 2.0
    sl_bot = z_glass_top - 20.0
    sleeve = tube(c["sleeve_od"] / 2, c["sleeve_od"] / 2 - c["sleeve_wall"], sl_bot, z_top - lip_t)
    sleeve = sleeve.fuse(tube(c["sleeve_lip_od"] / 2, c["sleeve_od"] / 2 - c["sleeve_wall"], z_top - lip_t, z_top))
    out.append(("C: 304 entrance sleeve", sleeve, (0.70, 0.72, 0.76), "304"))
    z_glass_bot = z_glass_top - s["glass_len"]
    z_plate_top = z_glass_bot - 2.0 + s["seal_groove_d"]
    pan_od = 2 * ri - 3.0
    pan = (cq.Workplane("XY").circle(pan_od / 2).extrude(28.0).faces(">Z").shell(-1.5).val()
           .translate((0, 0, z_plate_top + 0.05)))
    out.append(("C: 304 bottom pan", pan, STEEL_HOT, "304"))
    return out
