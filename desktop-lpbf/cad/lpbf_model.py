"""Parametric CadQuery model of the desktop LPBF concept (issue #260).

Run:  python desktop-lpbf/cad/lpbf_model.py [--glb]   # writes cad/out/desktop-lpbf.step (and a GLB with --glb)
      xvfb-run -a python desktop-lpbf/cad/render.py  # renders the PNGs and GIFs in cad/img/

Units are mm. Origin: centre of the build plate's top face at the start of a build (the powder plane).
+X is the recoat direction (left to right seen from the front), +Y points to the back, +Z up.

Each part records the assembly step it is added in, the direction it flies in from in the assembly GIF,
its line in bom.csv and, for catalogue parts, the McMaster-Carr part number whose product page gave its
dimensions (desktop-lpbf/mcmaster-parts.csv, checked 2026-11-17). Vendor parts are drawn from their listed
dimensions, not from the vendors' CAD files, which are not ours to publish. The galvo head, laser,
chiller, O2 analyzer, blower and electronics are envelopes.
"""
from __future__ import annotations

import math
import pathlib
from dataclasses import dataclass

import cadquery as cq

V = cq.Vector
HERE = pathlib.Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------------
# Parameters. Changing these moves the parts; render.py and the GIFs follow.
# --------------------------------------------------------------------------------------------
P = dict(
    # process chamber (internal), walls, floor and lid
    # walls from 1/2 in. 6061 plate (McMaster 89155K135); floor and lid 3/4 in.
    ch_x=260.0, ch_y=150.0, ch_z=160.0, wall=12.7, floor=19.05, lid=19.05,
    # build cylinder: McMaster 89895K623 304 SS tube, 2-1/4 in. OD x 0.065 in. wall (53.8 mm bore, lap to fit);
    # Ø53 mm plate. McMaster has no honed ~2 in. tube, so the plate grew from the concept's Ø50 mm.
    bore_d=53.8, plate_d=53.0, plate_t=10.0, piston_t=25.0, cyl_od=57.15, cyl_len=130.0,
    z_travel=60.0,
    # powder path along X
    x_dose=-90.0, x_park=-107.0, x_end=88.0, ovf_x0=60.0, ovf_x1=80.0, ovf_y=35.0, dose_y=29.0,
    # recoater drive on the back wall: 15 mm rail (6709K33) + carriage (6709K12), M12 x 10 mm screw (4566N101)
    rc_rail_z=122.0, rc_screw_y=53.0, rc_screw_z=78.0,
    # optics: Thorlabs FTH254-1064 (WD 301.2 mm, flange focal length 348.5 mm, housing Ø120 x 67.8 mm)
    lens_wd=301.2, lens_ffl=348.5, lens_d=120.0, lens_len=67.8, beam_z=420.0,
    # frame (30 mm T-slot): inner faces
    fx0=-345.0, fx1=255.0, fy=175.0, fz_bot=-470.0, fz_top=540.0, deck_z=-31.75,
    galvo_t=12.7,
)
P["cx"] = P["ch_x"] / 2 + P["wall"]          # chamber outer half-width (x)
P["cy"] = P["ch_y"] / 2 + P["wall"]          # chamber outer half-depth (y)
P["lid_z0"] = P["ch_z"]
P["lid_z1"] = P["ch_z"] + P["lid"]

# Colours (sRGB hex) used for the renders and written into the STEP/GLB.
C = dict(
    tslot="#c3c9cf", alu="#b9c0c7", alu_dark="#8e979f", anod="#2d3136", ss="#a2abb3", steel="#6f777e",
    brass="#c9a54a", motor="#25292e", motor_cap="#4a5058", glass="#9fd3ff", laser_glass="#3fbf6a",
    panel="#46535f", powder="#8b8d8f", part="#d9dde0", hot="#ff8a2a", beam="#ff1f1f", rubber="#3a3a3a",
    silicone="#d4553b", pcb="#2f7d4f", din="#c0c4c8", red="#d22b2b", yellow="#f0c419", green="#2bb24c",
    blue="#2b6cd2", fiber="#f08c1a", hose="#7f8890", white="#f2f2f2", wood="#c8b28a", black="#151719",
)


@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: str
    step: int
    explode: tuple = (0.0, 0.0, 0.0)
    group: str = ""          # "recoater" or "piston" parts move in the build-cycle GIF
    bom: str = ""            # line id in bom.csv / mcmaster-parts.csv
    mcm: str = ""            # McMaster-Carr part number, if the part is a catalogue part
    opacity: float = 1.0
    section: bool = False    # cut away in the section views


STEPS = {
    1: "T-slot frame and leveling feet",
    2: "Deck plate and optics rails",
    3: "Z axis: rail, ball screw, supports, servo",
    4: "Build cylinder, piston, build plate, overflow jar",
    5: "Process chamber body and gas plenums",
    6: "Recoater axis: rail, ball screw, carriage, blade, servo",
    7: "Lid: window flange, dose chute, hopper cartridge, camera, sensors",
    8: "Chamber door, hinges and latches",
    9: "Optics: galvo plate, scan head, f-theta lens, shutter, collimator",
    10: "Gas loop and vacuum: filter, blower, hoses, valve, pump, argon, O2 analyzer",
    11: "Electronics and operator panel",
    12: "Fiber laser source and fiber",
    13: "Laser guard panels and door with OD 7+ window",
}


# --------------------------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def rbox(x0, x1, y0, y1, z0, z1, r=3.0, edges="|Z"):
    w = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
    if r > 0:
        w = w.edges(edges).fillet(r)
    return w.val().translate(V(x0, y0, z0))


_AX = {"x": V(1, 0, 0), "y": V(0, 1, 0), "z": V(0, 0, 1), "-x": V(-1, 0, 0), "-y": V(0, -1, 0), "-z": V(0, 0, -1)}


def cyl(r, p0, axis, length):
    d = _AX[axis] if isinstance(axis, str) else V(*axis).normalized()
    return cq.Solid.makeCylinder(r, length, V(*p0), d)


def tube(ro, ri, p0, axis, length):
    return cyl(ro, p0, axis, length).cut(cyl(ri, p0, axis, length))


def sphere(r, p):
    return cq.Solid.makeSphere(r, V(*p), V(0, 0, 1), -90, 90, 360)


def comp(shapes):
    return cq.Compound.makeCompound([s for s in shapes if s is not None])


def place(shape, origin, xdir, normal):
    """Map a shape built in a local frame (x, y, z) onto origin + xdir/normal axes."""
    return shape.moved(cq.Location(cq.Plane(origin=V(*origin), xDir=V(*xdir), normal=V(*normal))))


def polyline_pipe(points, r, smooth=True, n=10):
    """A hose or cable: short cylinders + spheres through a Catmull-Rom-smoothed polyline."""
    pts = [V(*p) for p in points]
    if smooth and len(pts) > 2:
        ext = [pts[0] + (pts[0] - pts[1])] + pts + [pts[-1] + (pts[-1] - pts[-2])]
        sm = []
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for k in range(n):
                t = k / n
                t2, t3 = t * t, t * t * t
                sm.append(p0 * (-0.5 * t3 + t2 - 0.5 * t) + p1 * (1.5 * t3 - 2.5 * t2 + 1)
                          + p2 * (-1.5 * t3 + 2 * t2 + 0.5 * t) + p3 * (0.5 * t3 - 0.5 * t2))  # uniform Catmull-Rom
        sm.append(pts[-1])
        pts = sm
    solids = []
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        L = d.Length
        if L < 1e-6:
            continue
        solids.append(cq.Solid.makeCylinder(r, L, a, d.normalized()))
    for p in pts[1:-1]:
        solids.append(cq.Solid.makeSphere(r, p, V(0, 0, 1), -90, 90, 360))
    return comp(solids)


# ---- T-slot extrusion: McMaster 5537T97, 30 mm, 8 mm slot, 9 mm deep, Ø7 centre hole ------------
TS = 30.0


def _tslot_sketch():
    s = cq.Sketch().rect(TS, TS)
    h = TS / 2
    for ang in (0, 90, 180, 270):
        c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))

        def rot(x, y):
            return (x * c - y * sn, x * sn + y * c)
        # opening (8 wide, 2.2 lip) and the undercut (16 wide, 6.5 deep)
        lip_c, cav_c = rot(0, h - 1.1), rot(0, h - 2.2 - 3.25)
        lw, lh = (8.0, 2.3) if ang in (0, 180) else (2.3, 8.0)
        cw, chh = (16.0, 6.5) if ang in (0, 180) else (6.5, 16.0)
        s = s.push([lip_c]).rect(lw, lh, mode="s").reset()
        s = s.push([cav_c]).rect(cw, chh, mode="s").reset()
    s = s.push([(0, 0)]).circle(3.5, mode="s").reset()
    return s


def tslot(p0, axis, L):
    """30 mm T-slot rail of length L whose profile centre starts at p0 and runs along axis."""
    s = cq.Workplane("XY").placeSketch(_tslot_sketch()).extrude(L).val()
    if axis == "x":
        s = s.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    elif axis == "y":
        s = s.rotate(V(0, 0, 0), V(1, 0, 0), -90)
    return s.translate(V(*p0))


# ---- Linear guide: McMaster 6709K33 rail (15 x 15 mm, holes 60 mm c-c, 20 mm from the end) -----
def guide_rail(L, w, h, pitch=60.0, end=20.0):
    """Rail along local +x from 0..L, centred in y, base on z=0."""
    r = cq.Workplane("XY").box(L, w, h, centered=(False, True, False)).edges("|X and >Z").chamfer(0.8).val()
    x = end
    while x < L:
        r = r.cut(cyl(2.25, (x, 0, h - 5.5), "z", 5.6)).cut(cyl(3.75, (x, 0, h - 4.5), "z", 4.6))
        x += pitch
    return r


def guide_carriage(cl, cw, H, clear, w_rail, h_rail):
    """Carriage centred at local x=0, sitting on a rail of width w_rail/height h_rail, top at z=H."""
    body = cq.Workplane("XY").box(cl - 8, cw, H - clear, centered=(True, True, False)).edges("|X").fillet(1.0).val()
    body = body.translate(V(0, 0, clear))
    ends = [box(-cl / 2, -cl / 2 + 4, -cw / 2 + 1, cw / 2 - 1, clear + 0.5, H - 1.0),
            box(cl / 2 - 4, cl / 2, -cw / 2 + 1, cw / 2 - 1, clear + 0.5, H - 1.0)]
    b = comp([body] + ends)
    chan = box(-cl, cl, -w_rail / 2 - 0.5, w_rail / 2 + 0.5, 0, h_rail + 0.5)
    return b.cut(chan)


# ---- Ball screw ------------------------------------------------------------------------------
def ball_screw(L, d, j_d=8.0, j_l=30.0):
    """Screw along local +x from 0..L (journals j_l long at each end), shallow grooves for the look."""
    core = comp([cyl(j_d / 2, (0, 0, 0), "x", j_l),
                 cyl(d / 2, (j_l, 0, 0), "x", L - 2 * j_l),
                 cyl(j_d / 2, (L - j_l, 0, 0), "x", j_l)])
    return core


def ball_nut(d, body_d=24.0, body_l=40.0, fl_d=40.0, fl_t=10.0, flats=None):
    """Nut centred on local x=0 along x; flange at the -x end."""
    body = tube(body_d / 2, d / 2, (-body_l / 2 + fl_t, 0, 0), "x", body_l - fl_t)
    fl = tube(fl_d / 2, d / 2, (-body_l / 2, 0, 0), "x", fl_t)
    if flats:
        fl = fl.cut(box(-body_l, body_l, flats, fl_d, -fl_d, fl_d)).cut(box(-body_l, body_l, -fl_d, -flats, -fl_d, fl_d))
    return comp([body, fl])


# ---- Motors ----------------------------------------------------------------------------------
def servo_nema23(length=100.0, shaft_l=22.0):
    """ClearPath-style NEMA 23 integrated servo: mount face at local z=0, body toward -z, shaft +z."""
    sq = 57.15
    body = cq.Workplane("XY").box(sq, sq, length - 8, centered=(True, True, False)).edges("|Z").chamfer(4).val()
    body = body.translate(V(0, 0, -length + 8))
    face = cq.Workplane("XY").box(sq, sq, 8, centered=(True, True, False)).edges("|Z").chamfer(6).val().translate(V(0, 0, -8))
    pilot = cyl(19.05, (0, 0, 0), "z", 1.6)
    shaft = cyl(9.525 / 2, (0, 0, 1.6), "z", shaft_l)
    conn = box(-12, 12, sq / 2, sq / 2 + 9, -length + 18, -length + 52)
    fins = [box(-sq / 2 - 1.5, sq / 2 + 1.5, -sq / 2 - 1.5, sq / 2 + 1.5, -length + 14 + i * 9, -length + 17 + i * 9)
            for i in range(int((length - 30) / 9))]
    return comp([body, face, pilot, shaft, conn] + fins)


def stepper_nema17(length=40.0):
    sq = 42.3
    body = cq.Workplane("XY").box(sq, sq, length, centered=(True, True, False)).edges("|Z").chamfer(3.5).val()
    body = body.translate(V(0, 0, -length))
    return comp([body, cyl(11, (0, 0, 0), "z", 2), cyl(2.5, (0, 0, 2), "z", 22)])


# ---- KF (ISO-KF) hardware ---------------------------------------------------------------------
# flange OD, tube OD (mm): KF-25 5786N23 (1.57 in., 1 in. tube), KF-40 5786N25 (2.16 in., 1-1/2 in. tube),
# KF-50 4518K43 (2.95 in., 2 in. tube)
KF = {16: (30.0, 17.2), 25: (39.9, 25.4), 40: (54.9, 38.1), 50: (74.9, 50.8)}


def kf_stub(size, stub=20.0, wall=1.6):
    """Flange face at local z=0, tube runs toward -z. Hollow."""
    fo, to = KF[size]
    fl = cq.Workplane("XY").circle(fo / 2).extrude(-5.5).faces("<Z").chamfer(2.0).val()
    t = cyl(to / 2, (0, 0, -stub), "z", stub - 5.5)
    s = comp([fl, t])
    return s.cut(cyl(to / 2 - wall, (0, 0, -stub - 1), "z", stub + 2))


def kf_clamp(size):
    fo, _ = KF[size]
    ring = tube(fo / 2 + 7, fo / 2 - 1.5, (0, 0, -6), "z", 12)
    knob = cyl(5, (fo / 2 + 6, 0, 0), "x", 14).translate(V(0, 0, 0))
    wing = box(fo / 2 + 18, fo / 2 + 21, -9, 9, -3, 3)
    return comp([ring, knob, wing])


# ---- Small hardware ---------------------------------------------------------------------------
def shcs_head(p, axis="z", d=10.0, k=6.0):
    return cyl(d / 2, p, axis, k).cut(cyl(2.5, p, axis, k + 0.01).translate(_AX[axis] * (k - 3)))


def bellows_coupling(d=25.0, L=30.0):
    """Along local +z from 0..L."""
    parts = [cyl(d / 2, (0, 0, 0), "z", 8), cyl(d / 2, (0, 0, L - 8), "z", 8)]
    for i in range(7):
        z = 8 + i * (L - 16) / 7
        parts.append(cyl(d / 2 - (0 if i % 2 else 3), (0, 0, z), "z", (L - 16) / 7))
    return comp(parts)


def toggle_knob(p, axis="z"):
    return comp([cyl(4, p, axis, 14), cyl(10, V(*p) + _AX[axis] * 14, axis, 10)])


# --------------------------------------------------------------------------------------------
# The machine
# --------------------------------------------------------------------------------------------
def build(include_context=True):
    parts: list[Part] = []

    def add(name, shape, color, step, explode=(0, 0, 0), **kw):
        parts.append(Part(name, shape, color, step, tuple(float(e) for e in explode), **kw))

    cx, cy = P["cx"], P["cy"]
    ix, iy, iz = P["ch_x"] / 2, P["ch_y"] / 2, P["ch_z"]
    fl = P["floor"]
    zf = -fl                                   # chamber floor underside = deck plate top
    lz0, lz1 = P["lid_z0"], P["lid_z1"]
    fx0, fx1, fy = P["fx0"], P["fx1"], P["fy"]
    zb, zt = P["fz_bot"], P["fz_top"]
    deck = P["deck_z"]                         # deck plate underside
    h = TS / 2

    # ===================== 1. Frame: 30 mm T-slot (5537T97), gussets (5537T536), feet (5537T983) ======
    ux = (fx0 - h, fx1 + h)                    # upright centres
    uy = (-fy - h, fy + h)
    frame = []
    for x in ux:
        for y in uy:
            frame.append(tslot((x, y, zb), "z", zt - zb))
    levels = {"bottom": zb + h, "deck": deck - h, "top": zt - h}
    for z in levels.values():
        for y in uy:
            frame.append(tslot((fx0, y, z), "x", fx1 - fx0))
        for x in ux:
            frame.append(tslot((x, -fy, z), "y", 2 * fy))
    z_gp0 = P["lens_ffl"] - P["galvo_t"]       # galvo plate underside
    z_opt = z_gp0 - h
    for x in ux:
        frame.append(tslot((x, -fy, z_opt), "y", 2 * fy))
    for y in (-95.0, 95.0):
        frame.append(tslot((fx0, y, z_opt), "x", fx1 - fx0))
    for x in (-160.0, 130.0):
        frame.append(tslot((x, -fy, deck - h), "y", 2 * fy))
    add("T-slot frame (30 mm, 5537T97)", comp(frame), C["tslot"], 1, bom="S9", mcm="5537T97")
    gus = []
    for x in ux:
        for y in uy:
            sx = 1 if x < 0 else -1
            for z in list(levels.values()) + [z_opt]:
                up = 1 if z == levels["bottom"] else -1
                z0 = z + up * h
                leg = 30.2
                tri = (cq.Workplane("XZ").polyline([(0, 0), (sx * leg, 0), (0, up * leg)]).close().extrude(-9).val())
                gus.append(tri.translate(V(x + sx * h, y - 4.5, z0)))
    add("Gusset brackets (5537T536)", comp(gus), C["alu_dark"], 1, bom="S9", mcm="5537T536")
    feet = []
    for x in ux:
        for y in uy:
            feet += [cyl(4, (x, y, zb - 31.75), "z", 31.75), cyl(12.5, (x, y, zb - 52.4), "z", 8),
                     cq.Solid.makeCone(12.5, 9, 12, V(x, y, zb - 44.4), V(0, 0, 1))]
    add("Leveling mounts (5537T983)", comp(feet), C["anod"], 1, (0, 0, -120), bom="S9", mcm="5537T983")

    # ===================== 2. Deck plate and optics rails =====================
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    dk = box(fx0, fx1, -fy - TS, fy + TS, deck, zf)
    for (x, y, r) in [(0, 0, 48), (ox, 0, 31), (0, -cy - 17, 26), (0, cy + 16, 26)]:
        dk = dk.cut(cyl(r, (x, y, deck - 1), "z", zf - deck + 2))
    add("Deck plate (6061, 1/2 in.)", dk, C["alu"], 2, (0, 0, 220), bom="S9", mcm="89155K135")
    gp = box(fx0, 175, -110, 110, z_gp0, P["lens_ffl"]).cut(cyl(P["lens_d"] / 2 + 3, (0, 0, z_gp0 - 1), "z", P["galvo_t"] + 2))
    add("Galvo plate (6061, 1/2 in.)", gp, C["alu"], 9, (0, 0, 260), bom="S9", mcm="89155K135")

    # ===================== 3. Z axis =====================
    by0, by1 = 60.0, 72.0                      # back plate (y)
    add("Z back plate", box(-130, 40, by0, by1, -395, deck), C["alu"], 3, (0, 220, 0), bom="M3", mcm="89155K135")
    rail_x = -30.0
    zrail = place(guide_rail(280.0, 15.0, 15.0), (rail_x, by0, -385.0), (0, 0, 1), (0, -1, 0))
    add("Z guide rail (6709K33, 280 mm)", zrail, C["steel"], 3, (0, 160, 0), bom="M3", mcm="6709K33")
    z_arm = -232.0                             # lift-arm underside with the piston at the top
    zc = z_arm + 7.5
    zcar = place(guide_carriage(57.0, 34.0, 28.0, 4.0, 15.0, 15.0), (rail_x, by0, zc), (0, 0, 1), (0, -1, 0))
    add("Z carriage (6709K12)", zcar, C["steel"], 3, (0, 160, 0), group="piston", bom="M3", mcm="6709K12")
    add("Z carriage plate", box(-46, -14, 24, 32, zc - 30, zc + 30), C["alu"], 3, (0, 160, 0), group="piston", bom="M3")
    sx, sy = -85.0, 10.0
    arm = rbox(-112, 22, -22, 32, z_arm, z_arm + 15, 6)
    arm = arm.cut(cyl(6.5, (0, 0, z_arm - 1), "z", 17)).cut(cyl(7, (sx, sy, z_arm - 1), "z", 17))
    add("Z lift arm", arm, C["alu"], 3, (0, -160, 0), group="piston", bom="M3")
    add("Rod clamp collar", tube(16, 6.4, (0, 0, z_arm + 15), "z", 20), C["alu_dark"], 3, (0, -160, 0), group="piston", bom="M3")
    zscrew = comp([cyl(4, (sx, sy, -382), "z", 18), cyl(6, (sx, sy, -364), "z", 164), cyl(4, (sx, sy, -200), "z", 38)])
    add("Z ball screw (6638K11, M12 x 2 mm lead, cut to 220 mm)", zscrew, C["steel"], 3, (0, -200, 0), bom="M3", mcm="6638K11")
    znut = place(ball_nut(12.0, 25.0, 30.0, 47.0, 8.0, 14.5), (sx, sy, z_arm - 15), (0, 0, -1), (1, 0, 0))
    add("Z flange ball nut (with 6638K11)", znut, C["steel"], 3, (0, -200, 0), group="piston", bom="M3", mcm="6638K11")
    bk = comp([box(sx - 30, sx + 30, sy - 17, sy + 22, -200, -175), box(sx - 30, sx + 30, sy + 22, by0, -200, -175),
               cyl(11, (sx, sy, -175), "z", 4)])
    add("Z fixed support (BK10 type) + standoff", bk, C["anod"], 3, (0, -200, 0), bom="M3")
    bf = comp([box(sx - 30, sx + 30, sy - 17, sy + 22, -384, -364), box(sx - 30, sx + 30, sy + 22, by0, -384, -364)])
    add("Z floating support (BF10 type) + standoff", bf, C["anod"], 3, (0, -200, 0), bom="M3")
    add("Z bellows coupling (6446K781)", place(bellows_coupling(25.4, 34.1), (sx, sy, -175.1), (1, 0, 0), (0, 0, 1)), C["ss"], 3, (0, -200, 0), bom="M3", mcm="6446K781")
    add("Z motor mount", box(sx - 35, sx + 35, -22, by0, -151, -141).cut(cyl(20, (sx, sy, -152), "z", 12)), C["alu"], 3, (0, -200, 0), bom="M3")
    add("Z servo (ClearPath-SD, NEMA 23)", place(servo_nema23(100.0, 20.0), (sx, sy, -141.0), (1, 0, 0), (0, 0, -1)), C["motor"], 3, (0, -260, 0), bom="M2")

    # ===================== 4. Build cylinder, piston, plate, overflow jar =====================
    rcyl, rb = P["cyl_od"] / 2, P["bore_d"] / 2
    zc0 = zf - P["cyl_len"]
    cylp = comp([tube(rcyl, rb, (0, 0, zc0), "z", P["cyl_len"]),
                 tube(45, rb, (0, 0, zf - 10), "z", 10),
                 tube(45, 6.6, (0, 0, zc0 - 10), "z", 10),
                 tube(18, 6.6, (0, 0, zc0 - 22), "z", 12)])
    add("Build cylinder (89895K623 tube, flanged; rod wiper 1490N11)", cylp, C["ss"], 4, (0, 0, -250), bom="M3", mcm="89895K623")
    add("Build plate (Ø53, swappable)", cyl(P["plate_d"] / 2, (0, 0, -P["plate_t"]), "z", P["plate_t"]), C["alu_dark"], 4, (0, 0, 260), group="piston", bom="M3")
    zp0 = -P["plate_t"] - P["piston_t"]
    piston = cyl(rb - 0.2, (0, 0, zp0), "z", P["piston_t"]).cut(tube(rb, rb - 1.8, (0, 0, zp0 + 5), "z", 6.35))
    add("Piston (heater pocket, wear-ring groove)", piston, C["alu"], 4, (0, 0, 260), group="piston", bom="M3")
    add("Piston wear ring (1465N1, bronze-filled PTFE)", tube(rb - 0.1, rb - 1.8, (0, 0, zp0 + 5), "z", 6.35), C["brass"], 4, (0, 0, 260), group="piston", bom="M3", mcm="1465N1")
    add("Piston rod (1240K129, 1/2 in. 440C, cut)", cyl(6.35, (0, 0, z_arm), "z", zp0 - z_arm), C["ss"], 4, (0, 0, 260), group="piston", bom="M3", mcm="1240K129")
    zk40 = zf - 19.0
    add("Overflow port (KF-40, 5786N25)", place(kf_stub(40, 19.0), (ox, 0, zk40), (1, 0, 0), (0, 0, -1)), C["alu"], 5, (0, 0, -150), bom="G7", mcm="5786N25")
    jar = comp([place(kf_stub(40, 70), (ox, 0, zk40), (1, 0, 0), (0, 0, 1)), cyl(KF[40][1] / 2, (ox, 0, zk40 - 72), "z", 2)])
    add("Overflow jar (KF-40 half nipple + blank)", jar, C["ss"], 4, (0, 0, -220), bom="M4")
    add("Overflow clamp (4518K73)", place(kf_clamp(40), (ox, 0, zk40), (1, 0, 0), (0, 0, 1)), C["alu_dark"], 4, (0, 0, -220), bom="G7", mcm="4518K73")

    # ===================== 5. Chamber body and gas plenums =====================
    ch = rbox(-cx, cx, -cy, cy, zf, lz0, 6)
    ch = ch.cut(rbox(-ix, ix, -iy, iy, 0, lz0 + 1, 4))
    dz0, dz1 = 44.0, 146.0
    ch = ch.cut(box(-110, 110, -cy - 1, -iy + 1, dz0, dz1))                 # door opening
    ch = ch.cut(box(-35, 35, iy - 1, cy + 1, 4, 12))                       # cross-flow inlet slot, 70 x 8
    ch = ch.cut(box(-45, 45, -cy - 1, -iy + 1, 4, 24))                     # outlet slot
    ch = ch.cut(cyl(rb, (0, 0, zf - 1), "z", fl + 2))                       # build bore
    ch = ch.cut(box(P["ovf_x0"], P["ovf_x1"], -P["ovf_y"], P["ovf_y"], zf - 1, 1))
    ry, rz = P["rc_screw_y"], P["rc_screw_z"]
    ch = ch.cut(cyl(9, (-cx - 1, ry, rz), "x", P["wall"] + 2)).cut(cyl(9, (ix - 1, ry, rz), "x", P["wall"] + 2))
    ch = ch.cut(cyl(12.7, (ix - 1, 0, 115), "x", P["wall"] + 2))          # KF-25 vacuum port
    ch = ch.cut(cyl(5.5, (-cx - 1, -30, 130), "x", P["wall"] + 2))        # 1/4 NPT argon in
    ch = ch.cut(cyl(5.5, (ix - 1, -40, 18), "x", P["wall"] + 2))          # 1/4 NPT O2 sample
    add("Process chamber body (welded 1/2 in. 6061, ~6.2 L)", ch, C["alu"], 5, (0, 0, 260), bom="G1", mcm="89155K135")
    add("Cross-flow inlet plenum + nozzle", rbox(-55, 55, cy, cy + 32, -8, 30, 4), C["alu_dark"], 5, (0, 180, 0), bom="G4")
    add("Cross-flow outlet plenum", rbox(-60, 60, -cy - 34, -cy, -8, 26, 4), C["alu_dark"], 5, (0, -180, 0), bom="G4")
    add("Inlet plenum KF-25 port", place(kf_stub(25, 37), (0, cy + 16, -45), (1, 0, 0), (0, 0, -1)), C["alu"], 5, (0, 180, 0), bom="G7", mcm="5786N23")
    add("Outlet plenum KF-25 port", place(kf_stub(25, 37), (0, -cy - 17, -45), (1, 0, 0), (0, 0, -1)), C["alu"], 5, (0, -180, 0), bom="G7", mcm="5786N23")
    add("Vacuum port (KF-25, 5786N23)", place(kf_stub(25, 12.7 + P["wall"]), (cx + 12.7, 0, 115), (0, 1, 0), (1, 0, 0)), C["alu"], 5, (180, 0, 0), bom="G7", mcm="5786N23")
    add("Layer-light LED bar", box(ix - 6, ix - 1, -45, 45, 8, 16), C["white"], 5, (0, 0, 120), bom="M6")

    # ===================== 6. Recoater =====================
    rrail = place(guide_rail(255.0, 15.0, 15.0), (-127.5, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))
    add("Recoater guide rail (6709K33, cut to 255 mm)", rrail, C["steel"], 6, (0, 0, 220), bom="M1", mcm="6709K33")
    xc = P["x_park"]
    rcar = place(guide_carriage(57.0, 34.0, 28.0, 4.0, 15.0, 15.0), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))
    add("Recoater carriage (6709K12)", rcar, C["steel"], 6, (0, 0, 220), group="recoater", bom="M1", mcm="6709K12")
    yb0 = P["dose_y"] + 3.0
    blk = comp([box(xc - 22, xc + 22, yb0, iy - 28, 58, 140), box(xc - 22, xc + 22, iy - 28, iy - 2, 58, 100)])
    blk = blk.cut(cyl(12.5, (xc - 23, ry, rz), "x", 46))
    add("Recoater carriage block", blk, C["alu"], 6, (0, 0, 220), group="recoater", bom="M1")
    add("Recoater ball screw (4566N101, M12 x 10 mm lead, cut)",
        comp([cyl(4, (-cx - 30, ry, rz), "x", 30), cyl(6, (-cx, ry, rz), "x", 2 * cx), cyl(4, (cx, ry, rz), "x", 12)]),
        C["steel"], 6, (0, 0, 220), bom="M1", mcm="4566N101")
    add("Recoater flange ball nut (4566N401)", place(ball_nut(12.0, 23.0, 43.0, 40.0, 10.0), (xc + 10.5, ry, rz), (-1, 0, 0), (0, 0, 1)), C["steel"], 6, (0, 0, 220), group="recoater", bom="M1", mcm="4566N401")
    add("Recoater arm", box(xc - 6, xc + 6, yb0 + 1, yb0 + 9, 14, 58), C["alu"], 6, (0, 0, 220), group="recoater", bom="M5")
    add("Blade holder", rbox(xc - 7, xc + 7, -P["dose_y"] - 4, yb0 + 9, 3, 23, 2, "|Y"), C["anod"], 6, (0, 0, 220), group="recoater", bom="M5")
    add("Silicone-cord blade (1187N14, 3 mm)", cyl(1.5, (xc + 6, -P["dose_y"] - 3, 1.6), "y", 2 * P["dose_y"] + 14), C["silicone"], 6, (0, 0, 220), group="recoater", bom="M5", mcm="1187N14")
    add("Recoater feedthrough + fixed bearing housing", comp([cyl(28, (-cx - 24, ry, rz), "x", 24), box(-cx - 24, -cx, ry - 30, ry + 30, rz - 34, rz - 26)]), C["anod"], 6, (-160, 0, 0), bom="M1")
    add("Recoater floating bearing cap", cyl(22, (cx, ry, rz), "x", 14), C["anod"], 6, (160, 0, 0), bom="M1")
    add("Recoater motor standoff", tube(30, 26, (-cx - 64, ry, rz), "x", 40), C["alu_dark"], 6, (-200, 0, 0), bom="M1")
    add("Recoater bellows coupling (6446K781)", place(bellows_coupling(25.4, 34.1), (-cx - 59, ry, rz), (0, 1, 0), (1, 0, 0)), C["ss"], 6, (-200, 0, 0), bom="M1", mcm="6446K781")
    add("Recoater servo (ClearPath-SD, NEMA 23)", place(servo_nema23(100.0, 20.0), (-cx - 64, ry, rz), (0, 1, 0), (1, 0, 0)), C["motor"], 6, (-260, 0, 0), bom="M2")
    add("Recoater motor bracket", box(-cx - 166, -cx - 64, ry - 34, ry + 34, zf, rz - 28.6), C["alu_dark"], 6, (-260, 0, 0), bom="M1")

    # ===================== 7. Lid and what sits on it =====================
    xd = P["x_dose"]
    lid = rbox(-cx, cx, -cy, cy, lz0, lz1, 6).cut(cyl(28, (0, 0, lz0 - 1), "z", P["lid"] + 2))
    lid = lid.cut(box(xd - 5, xd + 5, -P["dose_y"], P["dose_y"], lz0 - 1, lz1 + 1))
    cam_p = V(75, -45, lz1)
    lid = lid.cut(cyl(11, (75, -45, lz0 - 1), "z", P["lid"] + 2))
    for (x, y) in [(100, 50), (110, -62)]:
        lid = lid.cut(cyl(5.5, (x, y, lz0 - 1), "z", P["lid"] + 2))
    add("Chamber lid (6061, 3/4 in.)", lid, C["alu"], 7, (0, 0, 300), bom="G1")
    bolts = []
    for i in range(7):
        x = -cx + 16 + i * (2 * cx - 32) / 6
        for y in (-cy + 8, cy - 8):
            bolts.append(shcs_head((x, y, lz1), "z", 8.5, 5))
    for y in (-cy / 3, cy / 3):
        for x in (-cx + 8, cx - 8):
            bolts.append(shcs_head((x, y, lz1), "z", 8.5, 5))
    add("Lid screws (M5 SHCS, 91292A126)", comp(bolts), C["steel"], 7, (0, 0, 340), bom="G1", mcm="91292A126")
    add("Lid O-ring (Viton cord, 1165N11)", rbox(-cx + 4, cx - 4, -cy + 4, cy - 4, lz0 - 0.5, lz0 + 0.5, 6).cut(rbox(-cx + 6, cx - 6, -cy + 6, cy - 6, lz0 - 1, lz0 + 1, 5)), C["black"], 7, (0, 0, 280), bom="G8", mcm="1165N11")
    wf = tube(48, 24, (0, 0, lz1), "z", 22).cut(cyl(25.65, (0, 0, lz1 + 10), "z", 13))
    add("Window flange", wf, C["anod"], 7, (0, 0, 360), bom="L7")
    add("Ø2 in. fused-silica window", cyl(25.4, (0, 0, lz1 + 10), "z", 12), C["glass"], 7, (0, 0, 380), bom="L7", opacity=0.45)
    rr = comp([tube(48, 22, (0, 0, lz1 + 22), "z", 5)] + [shcs_head((40 * math.cos(math.radians(a)), 40 * math.sin(math.radians(a)), lz1 + 27), "z", 7, 4) for a in range(0, 360, 60)])
    add("Window retaining ring", rr, C["anod"], 7, (0, 0, 400), bom="L7")
    add("Field-stop aperture", tube(27.9, 18, (0, 0, lz0), "z", 10), C["black"], 7, (0, 0, 300), bom="L7")
    add("Cover-slide holder + slide", comp([tube(35, 27, (0, 0, lz0 - 6), "z", 6), cyl(27, (0, 0, lz0 - 4), "z", 1)]), C["anod"], 7, (0, 0, 220), bom="L7")
    add("Gas knife (cover-slide purge)", box(-32, 32, -42, -36, lz0 - 12, lz0 - 6), C["ss"], 7, (0, 0, 200), bom="L7")
    chute = box(xd - 5, xd + 5, -P["dose_y"], P["dose_y"], 26, lz0).cut(box(xd - 3.5, xd + 3.5, -P["dose_y"] + 1.5, P["dose_y"] - 1.5, 25, lz0 + 1))
    add("Dose chute", chute, C["ss"], 7, (0, 0, 260), bom="M4")
    zdb = lz1 + 40.0
    add("Dosing block (fluted roller inside)", rbox(-128, -52, -55, 55, lz1, zdb, 3), C["alu"], 7, (0, 0, 300), bom="M4")
    add("Dosing KF-50 port", place(kf_stub(50, 6), (xd, 0, zdb), (1, 0, 0), (0, 0, 1)), C["ss"], 7, (0, 0, 300), bom="M4", mcm="4518K43")
    add("Roller shaft seal housing", cyl(15, (xd, 55, lz1 + 22), "y", 10), C["anod"], 7, (0, 0, 300), bom="M4")
    add("Dosing stepper (6627T91, NEMA 17)", place(stepper_nema17(42.0), (xd, 65, lz1 + 22), (1, 0, 0), (0, -1, 0)), C["motor"], 7, (0, 160, 300), bom="M4", mcm="6627T91")
    zh0 = zdb
    cart = comp([place(kf_stub(50, 39.7, 1.65), (xd, 0, zh0), (1, 0, 0), (0, 0, -1)),
                 tube(25.4, 23.75, (xd, 0, zh0 + 39.7), "z", 292 - zh0 - 39.7)])
    add("Hopper cartridge (8989K418 tube + 4518K43 KF-50 ferrule)", cart, C["ss"], 7, (0, 0, 380), bom="M4", mcm="8989K418")
    add("Hopper powder", cyl(23.7, (xd, 0, zh0 + 2), "z", 70), C["powder"], 7, (0, 0, 380), bom="M4")
    add("Hopper cap", comp([cyl(28, (xd, 0, 292), "z", 6), cyl(6, (xd, 0, 298), "z", 10), cyl(9, (xd, 0, 306), "z", 4)]), C["anod"], 7, (0, 0, 420), bom="M4")
    add("KF-50 clamp", place(kf_clamp(50), (xd, 0, zh0), (1, 0, 0), (0, 0, 1)), C["alu_dark"], 7, (0, 0, 380), bom="M4")
    add("Load cell (3487N257 S-beam) + cradle", comp([box(xd - 25.4, xd + 25.4, -70, -57.3, lz1, lz1 + 63.5),
                                                      box(xd - 8, xd + 8, -70, -24, lz1 + 58, lz1 + 64)]), C["ss"], 7, (0, -120, 300), bom="M4", mcm="3487N257")
    d = (V(0, 0, 0) - cam_p).normalized()
    up = d * -1
    boss = cq.Solid.makeCylinder(16, 40, cam_p, up).cut(cq.Solid.makeCylinder(11, 40, cam_p, up))
    add("Camera viewport boss + Ø1 in. window", boss, C["anod"], 7, (0, 0, 300), bom="M6")
    cam_base = cam_p + up * 40
    cam = comp([cq.Solid.makeCylinder(15, 38, cam_base, up),
                place(box(-19, 19, -19, 19, 0, 8), (cam_base + up * 38).toTuple(), (1, 0, 0), up.toTuple())])
    add("Layer camera (Pi HQ + C-mount lens)", cam, C["black"], 7, (0, 0, 340), bom="M6")
    add("Absolute pressure transmitter (3861N11)", comp([cyl(5, (100, 50, lz1), "z", 12), cyl(12, (100, 50, lz1 + 12), "z", 49)]), C["ss"], 7, (0, 0, 300), bom="G7", mcm="3861N11")
    add("Relief valve (4277T52, 0.5 psi)", comp([cyl(5, (110, -62, lz1), "z", 8), cyl(8, (110, -62, lz1 + 8), "z", 17.5)]), C["red"], 7, (0, 0, 300), bom="G7", mcm="4277T52")

    # ===================== 8. Door: hinges 1151A87, draw latches 1807A61 =====================
    dy0, dy1 = -cy - 15, -cy
    dzb0, dzb1 = 27.0, 185.0
    add("Chamber door (6061, 15 mm)", rbox(-cx, cx, dy0, dy1, dzb0, dzb1, 6, "|Y"), C["alu"], 8, (0, -240, 0), bom="G1")
    add("Door O-ring (Viton cord, 1165N11)", rbox(-120, 120, dy1 - 0.2, dy1 + 0.6, dz0 - 6, dz1 + 6, 5, "|Y").cut(rbox(-118, 118, dy1 - 1, dy1 + 1, dz0 - 4, dz1 + 4, 4, "|Y")), C["black"], 8, (0, -200, 0), bom="G8", mcm="1165N11")
    hinges = []
    for z in (dzb0 + 1, dzb1 - 77.2):
        hinges += [box(-cx + 2, -cx + 40, dy0 - 2.4, dy0, z, z + 76.2),
                   box(-cx - 2.4, -cx, dy1 + 2, dy1 + 40, z, z + 76.2),
                   cyl(5, (-cx - 3, dy0 - 3, z), "z", 76.2)]
    add("Door hinges (1151A87, 304 SS lift-off)", comp(hinges), C["ss"], 8, (0, -240, 0), bom="G1", mcm="1151A87")
    latches = []
    for z in (60.0, 150.0):
        latches += [box(cx, cx + 31.8, -84, -26, z - 22, z + 22), box(cx + 18, cx + 26, dy0 + 2, -84, z - 8, z + 8),
                    box(cx, cx + 8, dy0 + 1, dy1 - 1, z - 14, z + 14)]
    add("Draw latches (1807A61, 304 SS)", comp(latches), C["ss"], 8, (0, -240, 0), bom="G1", mcm="1807A61")
    zm = (dz0 + dz1) / 2
    add("Door handle", comp([cyl(5, (-30, dy0, zm), "-y", 30), cyl(5, (30, dy0, zm), "-y", 30), cyl(6, (-36, dy0 - 30, zm), "x", 72)]), C["anod"], 8, (0, -260, 0), bom="G1")

    # ===================== 9. Optics =====================
    zg0 = P["lens_ffl"]
    lens = comp([cyl(P["lens_d"] / 2, (0, 0, P["lens_wd"]), "z", zg0 - P["lens_wd"]),
                 cyl(42.5, (0, 0, zg0), "z", P["lens_wd"] + P["lens_len"] - zg0), cyl(30, (0, 0, P["lens_wd"] - 1), "z", 1.5)])
    add("f-theta lens, f = 254 mm (FTH254-1064 envelope)", lens, C["black"], 9, (0, 0, 300), bom="L6")
    galvo = comp([rbox(-75, 75, -65, 65, zg0, zg0 + 115, 8), cyl(17, (-90, 0, P["beam_z"]), "x", 15), box(-60, 60, 65, 72, zg0 + 15, zg0 + 60)])
    add("2-axis galvo scan head (basiCube 20 class)", galvo, C["anod"], 9, (0, 0, 340), bom="L5")
    sh = comp([rbox(-160, -105, -32, 32, P["beam_z"] - 26, P["beam_z"] + 26, 4), box(-150, -115, -20, 20, zg0, P["beam_z"] - 26),
               box(-147, -118, 32, 44, P["beam_z"] - 20, P["beam_z"] + 20)])
    add("Safety shutter + beam dump", sh, C["yellow"], 9, (0, 0, 340), bom="L4")
    coll = comp([cyl(20, (-300, 0, P["beam_z"]), "x", 110), cyl(14, (-330, 0, P["beam_z"]), "x", 30), box(-285, -215, -22, 22, zg0, P["beam_z"] - 18)])
    add("Collimator (QBH) on V-mount", coll, C["ss"], 9, (0, 0, 340), bom="L3")

    # ===================== 10. Gas loop and vacuum =====================
    hx, hy = 175.0, -95.0
    hepa = comp([cyl(47.6, (hx, hy, -200), "z", 92), cyl(30, (hx, hy, -108), "z", 6), cyl(10, (hx - 47.6, hy, -125), "-x", 18),
                 cyl(10, (hx, hy, -218), "z", 18)])
    add("Recirculation HEPA filter (5169K72 + 9179K14)", hepa, C["anod"], 10, (220, 0, 0), bom="G5", mcm="5169K72")
    bl = comp([rbox(100, 250, 15, 135, -265, -135, 8), cyl(38, (175, 75, -135), "z", 40), cyl(14, (175, 15, -200), "-y", 22), cyl(14, (175, 135, -200), "y", 22)])
    add("Recirculation blower (sealed side-channel, quote)", bl, C["blue"], 10, (220, 0, 0), bom="G4")
    hoses = [[(0, -cy - 17, -52), (0, -cy - 17, -95), (60, -110, -125), (hx - 66, hy, -125)],
             [(hx, hy, -222), (hx, hy - 10, -265), (hx + 50, -40, -250), (175, -7, -200)],
             [(175, 157, -200), (110, 160, -170), (40, cy + 16, -110), (0, cy + 16, -52)]]
    add("Gas-loop hoses (KF-25 SS bellows, 3497N22/23)", comp([polyline_pipe(hp, 18.25) for hp in hoses]), C["hose"], 10, (0, 0, -160), bom="G7", mcm="3497N23")
    vx = 177.0
    vv = comp([place(kf_clamp(25), (cx + 12.7, 0, 115), (0, 1, 0), (1, 0, 0)),
               cyl(12.7, (cx + 12.7, 0, 115), "x", vx - cx - 12.7), sphere(12.7, (vx, 0, 115)),
               cyl(12.7, (vx, 0, 115), "-y", 18), cyl(20, (vx, -18, 115), "-y", 124), sphere(28, (vx, -80, 115)),
               box(vx - 4, vx + 4, -84, -76, 115, 160), box(vx - 6, vx + 6, -80, 57, 160, 166)])
    add("Pump isolation valve (4123K45, KF-25 ball valve)", vv, C["ss"], 10, (220, 0, 0), bom="G7", mcm="4123K45")
    pumpx0 = 380.0
    pump = comp([rbox(pumpx0, pumpx0 + 368, -71.5, 71.5, -510, -495, 4), cyl(62, (pumpx0 + 150, 0, -430), "x", 218),
                 rbox(pumpx0, pumpx0 + 150, -65, 65, -495, -310, 10), cyl(14, (pumpx0 + 70, 0, -310), "z", 30),
                 box(pumpx0 + 40, pumpx0 + 300, -8, 8, -215, -205), box(pumpx0 + 40, pumpx0 + 52, -8, 8, -310, -205), box(pumpx0 + 288, pumpx0 + 300, -8, 8, -368, -205)])
    add("Vacuum pump (4396K21, 1e-2 Torr, 3 cfm)", pump, C["blue"], 10, (300, 0, 0), bom="G2", mcm="4396K21")
    fxp, fyp = 360.0, -150.0
    vfilt = comp([cyl(66.5, (fxp, fyp, -470), "z", 190), place(kf_stub(25, 16), (fxp, fyp, -264), (1, 0, 0), (0, 0, 1)),
                  place(kf_stub(25, 16), (fxp, fyp, -486), (1, 0, 0), (0, 0, -1))])
    add("Pump-line filter (3394N12, KF-25, 8 um)", vfilt, C["ss"], 10, (300, 0, 0), bom="G2", mcm="3394N12")
    add("Pump line (KF-25 hose 3497N23)", comp([polyline_pipe([(vx, -142, 115), (215, -165, 80), (300, -170, -40), (fxp, fyp, -200), (fxp, fyp, -258)], 18.25),
                                                 polyline_pipe([(fxp, fyp, -492), (fxp + 30, fyp + 40, -505), (pumpx0 + 70, -40, -380), (pumpx0 + 70, 0, -282)], 18.25)]),
        C["hose"], 10, (220, 0, 0), bom="G7", mcm="3497N23")
    sol = [rbox(-300, -190, -160, -125, zf, zf + 20, 3)]
    for x in (-280, -240):
        sol += [box(x - 20, x + 20, -163, -122, zf + 20, zf + 40), box(x - 20, x + 20, -163, -122, zf + 40, zf + 85), box(x - 8, x + 8, -170, -163, zf + 60, zf + 80)]
    sol += [cyl(9, (-205, -142.5, zf + 20), "z", 25), cyl(5, (-205, -142.5, zf + 45), "z", 20)]
    add("Argon valves (2 x 8077K237 24 V NC + 7833K76 needle)", comp(sol), C["brass"], 10, (-200, 0, 0), bom="G7", mcm="8077K237")
    add("Argon line (1/4 in. 316 SS, 89785K824)", polyline_pipe([(-205, -142.5, zf + 65), (-205, -142.5, zf + 90), (-190, -60, 100), (-cx - 30, -30, 130), (-cx, -30, 130)], 3.2), C["ss"], 10, (-200, 0, 0), bom="G7", mcm="89785K824")
    o2 = comp([rbox(-335, -175, -170, -100, -250, -110, 5), box(-300, -210, -171, -170, -150, -120)])
    add("Trace O2 analyzer (Ntron Microx class)", o2, C["white"], 10, (-200, 0, 0), bom="G6")
    add("O2 sample line (1/4 in. 316 SS)", polyline_pipe([(ix + 13, -40, 18), (cx + 30, -40, 18), (cx + 40, -150, -10), (0, -168, -60), (-200, -165, -100), (-200, -150, -110)], 3.2), C["ss"], 10, (0, -200, 0), bom="G6", mcm="89785K824")

    # ===================== 11. Electronics (7812K14 enclosure) and operator panel =====================
    ex0, ex1, ey0, ey1, ez0, ez1 = fx0, fx0 + 152.4, -90.0, -90.0 + 254.0, zb + TS + 2, zb + TS + 2 + 304.8
    enc = box(ex0, ex1, ey0, ey1, ez0, ez1).cut(box(ex0 + 1.6, ex1 + 1, ey0 + 1.6, ey1 - 1.6, ez0 + 1.6, ez1 - 1.6))
    add("Controls enclosure (7812K14, cover off)", enc, "#d9dcdf", 11, (-220, 0, 0), bom="C4", mcm="7812K14", opacity=0.9)
    bpx = ex0 + 4.0
    add("Enclosure back panel (7812K54)", box(ex0 + 1.6, bpx, ey0 + 12, ey0 + 12 + 228.6, ez0 + 13, ez0 + 13 + 279.4), C["white"], 11, (-220, 0, 0), bom="C4", mcm="7812K54")
    zr1, zr2 = ez0 + 205.0, ez0 + 85.0
    add("DIN rails (8961K15)", comp([box(bpx, bpx + 7.5, ey0 + 15, ey1 - 15, z - 17.5, z + 17.5) for z in (zr1, zr2)]), C["din"], 11, (-220, 0, 0), bom="C4", mcm="8961K15")
    rx = bpx + 7.5
    el = [("24 V supply (SDR-480-24)", box(rx, rx + 128.5, ey0 + 20, ey0 + 105.5, zr1 - 62.6, zr1 + 62.6), C["white"], "C4"),
          ("Safety relay (G9SE-201)", box(rx, rx + 115, ey0 + 110, ey0 + 127.5, zr1 - 50, zr1 + 50), C["yellow"], "S1"),
          ("Chamber dP transmitter (5539N26)", box(rx, rx + 40, ey0 + 133, ey0 + 180.6, zr1 - 42, zr1 + 42), C["white"], "G7"),
          ("Terminal blocks", box(rx, rx + 45, ey0 + 186, ey0 + 236, zr1 - 22, zr1 + 22), C["din"], "C4"),
          ("Motion controller (ClearCore)", box(rx, rx + 30, ey0 + 20, ey0 + 128, zr2 - 55, zr2 + 55), C["pcb"], "C3"),
          ("Supervisor (Pi 5, DIN case)", box(rx, rx + 32, ey0 + 135, ey0 + 180, zr2 - 45, zr2 + 45), C["red"], "C2"),
          ("Scan + laser controller", box(rx, rx + 40, ey0 + 186, ey0 + 238, zr2 - 50, zr2 + 50), C["pcb"], "C1")]
    for nm, shp, col, b in el:
        add(nm, shp, col, 11, (-220, 0, 0), bom=b, mcm="5539N26" if "5539N26" in nm else "")
    pz0 = 120.0
    fyf = -fy - TS - 2.0
    add("Operator panel box", rbox(212, 272, fyf - 34, fyf, pz0, pz0 + 200, 4), C["anod"], 11, (0, -200, 0), bom="S4")
    bx = 242.0
    ops = [("E-stop (IDEC XA1E)", comp([cyl(20, (bx, fyf - 34, pz0 + 160), "-y", 8), cyl(17, (bx, fyf - 42, pz0 + 160), "-y", 14)]), C["red"], "S3", ""),
           ("Key switch (6749K3)", comp([cyl(15.1, (bx, fyf - 34, pz0 + 112), "-y", 6), box(bx - 4, bx + 4, fyf - 48, fyf - 40, pz0 + 109, pz0 + 115)]), C["ss"], "S4", "6749K3"),
           ("Emission indicator (7545K316 + 7545K7)", cyl(15.1, (bx, fyf - 34, pz0 + 72), "-y", 10), C["red"], "S4", "7545K316"),
           ("Reset button (6749K201)", cyl(15.1, (bx, fyf - 34, pz0 + 35), "-y", 10), C["blue"], "S4", "6749K201")]
    for nm, shp, col, b, m in ops:
        add(nm, shp, col, 11, (0, -220, 0), bom=b, mcm=m)
    stx, sty = fx1 + h, -fy - h
    add("Stack light base (1577T43)", cyl(15.9, (stx, sty, zt), "z", 30), C["anod"], 11, (0, 0, 220), bom="S4", mcm="1577T43")
    for i, col in enumerate(("green", "yellow", "red")):
        add(f"Stack light {col}", cyl(15.9, (stx, sty, zt + 30 + i * 44), "z", 43), C[col], 11, (0, 0, 220 + 30 * i), bom="S4", opacity=0.9)
    add("Laser guard front column", box(200, fx1 + TS, -fy - TS - 2, -fy - TS, deck - TS, zt), C["panel"], 11, (0, -200, 0), bom="S9", mcm="88895K51", opacity=0.9)

    # ===================== 12. Laser source + fiber =====================
    if include_context:
        ly0, ly1 = 330.0, 830.0
        laser = comp([rbox(-560, -80, ly0, ly1, -510, -377, 6), box(-540, -100, ly0 - 3, ly0, -500, -387), cyl(10, (-150, ly0 - 3, -420), "-y", 10)])
        add("Fiber laser source (500 W, 3U)", laser, C["white"], 12, (0, 300, 0), bom="L1")
        add("Chiller (beside the laser)", rbox(-1000, -620, ly0 + 40, ly1 - 60, -510, -60, 8), C["blue"], 12, (0, 300, 0), bom="L2")
        fiber = polyline_pipe([(-150, ly0 - 13, -420), (-150, ly0 - 120, -380), (-250, fy + 60, 0), (-300, fy - 20, P["beam_z"] - 30),
                               (-345, 60, P["beam_z"]), (-345, 10, P["beam_z"]), (-330, 0, P["beam_z"])], 5)
        add("Process fiber (armoured)", fiber, C["fiber"], 12, (0, 300, 0), bom="L1")

    # ===================== 13. Laser guard: 5052 sheet (88895K51), framed door, OD 7+ window =====================
    pt = 1.6
    pnls = [box(fx0 - TS - pt, fx0 - TS, -fy - TS, fy + TS, zb, zt),        # left
            box(fx1 + TS, fx1 + TS + pt, -fy - TS, fy + TS, zb, zt),        # right
            box(fx0 - TS, fx1 + TS, fy + TS, fy + TS + pt, zb, zt),         # back
            box(fx0 - TS, fx1 + TS, -fy - TS, fy + TS, zt, zt + pt),        # top
            box(fx0 - TS, fx1 + TS, -fy - TS - pt, -fy - TS, zb, deck - TS)]  # lower front
    add("Laser guard panels (5052 sheet, 88895K51)", comp(pnls), C["panel"], 13, (0, 0, 0), bom="S9", mcm="88895K51", opacity=0.22)
    dyc = -fy - TS - h                          # door frame rail centre (y)
    dxa, dxb = fx0 - h, 185.0                   # vertical rail centres (x)
    dza, dzb = deck - TS + h, zt - h            # horizontal rail centres (z)
    dframe = [tslot((dxa, dyc, dza - h), "z", dzb - dza + TS), tslot((dxb, dyc, dza - h), "z", dzb - dza + TS),
              tslot((dxa + h, dyc, dza), "x", dxb - dxa - TS), tslot((dxa + h, dyc, dzb), "x", dxb - dxa - TS)]
    add("Guard door frame (5537T97)", comp(dframe), C["tslot"], 13, (0, -260, 0), bom="S9", mcm="5537T97")
    wx0, wz0 = -233.0, 20.0
    dp = box(dxa + h, dxb - h, dyc - 0.8, dyc + 0.8, dza + h, dzb - h).cut(box(wx0, wx0 + 385.8, dyc - 5, dyc + 5, wz0, wz0 + 304.8))
    add("Guard door panel (5052 sheet)", dp, C["panel"], 13, (0, -260, 0), bom="S9", mcm="88895K51", opacity=0.35)
    add("OD 7+ laser-safety viewing window (LW1P1/M size)", box(wx0, wx0 + 385.8, dyc - 3, dyc - 1, wz0, wz0 + 304.8), C["laser_glass"], 13, (0, -260, 0), bom="S5", opacity=0.45)
    gh = comp([box(dxa - h - 3, dxa - h, dyc - 30, dyc + 30, z, z + 58.7) for z in (20.0, 400.0)])
    add("Guard door hinges (5537T847)", gh, C["tslot"], 13, (0, -260, 0), bom="S9", mcm="5537T847")
    hz0 = 250.0
    add("Guard door handle (5537T419)", comp([box(dxb - 6, dxb + 6, dyc - h - 41.3, dyc - h, hz0, hz0 + 12), box(dxb - 6, dxb + 6, dyc - h - 41.3, dyc - h, hz0 + 119.8, hz0 + 131.8),
                                               box(dxb - 6, dxb + 6, dyc - h - 41.3, dyc - h - 29.3, hz0, hz0 + 131.8)]), C["black"], 13, (0, -280, 0), bom="S9", mcm="5537T419")
    add("Guard-locking door switch (Omron D4JL)", box(dxb + h + 2, dxb + h + 30, dyc - 40, dyc - 6, 420, 510), C["yellow"], 13, (0, -280, 0), bom="S2")

    return parts


def state_offsets(recoater_x=None, piston_dz=0.0):
    """Translations for the moving groups: recoater blade to x = recoater_x, piston down by piston_dz."""
    off = {}
    if recoater_x is not None:
        off["recoater"] = (recoater_x - P["x_park"], 0.0, 0.0)
    off["piston"] = (0.0, 0.0, -piston_dz)
    return off


def to_assembly(parts):
    a = cq.Assembly(name="desktop_lpbf")
    for i, p in enumerate(parts):
        r, g, b = (int(p.color[k:k + 2], 16) / 255 for k in (1, 3, 5))
        nm = "".join(ch if ch.isalnum() else "_" for ch in p.name)[:60] + f"_{i:03d}"
        a.add(p.shape, name=nm, color=cq.Color(r, g, b, p.opacity))
    return a


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    parts = build()
    print(f"{len(parts)} parts built in {time.time() - t0:.1f} s")
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    if "--no-export" not in sys.argv:
        a = to_assembly(parts)
        a.export(str(out / "desktop-lpbf.step"))
        if "--glb" in sys.argv:
            from cadquery.occ_impl.exporters.assembly import exportGLTF
            exportGLTF(a, str(out / "desktop-lpbf.glb"), binary=True, tolerance=0.4, angularTolerance=0.35)
        print("wrote", *(p.name for p in out.iterdir()))
