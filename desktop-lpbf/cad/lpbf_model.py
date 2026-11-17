"""Parametric CadQuery model of the desktop LPBF concept (issue #260).

Run:  python desktop-lpbf/cad/lpbf_model.py            # writes STEP + GLB to desktop-lpbf/cad/out/
      python desktop-lpbf/cad/render.py                 # renders the PNGs and GIFs (needs a display; use xvfb-run)

Units are mm. Origin: centre of the build plate's top face at the start of a build (the powder plane).
+X is the recoat direction (left to right seen from the front), +Y points to the back, +Z up.

Each part records the assembly step it is added in, the direction it flies in from in the assembly GIF,
the BOM line it belongs to (bom.csv / mcmaster-parts.csv) and, where one exists, the McMaster-Carr part
number checked live through the lab Pi. Vendor parts are modelled from their listed dimensions, not from
the vendors' CAD files, which are not ours to publish.
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
    ch_x=260.0, ch_y=150.0, ch_z=160.0, wall=15.0, floor=20.0, lid=20.0,
    # build cylinder: 2 in. ID tube, Ø50 plate
    bore_d=50.8, plate_d=50.0, plate_t=10.0, piston_t=25.0, cyl_od=60.3, cyl_len=130.0,
    z_travel=60.0,
    # powder path along X
    x_dose=-80.0, x_park=-103.0, x_end=88.0, ovf_x0=60.0, ovf_x1=80.0, ovf_y=35.0, dose_y=30.0,
    # recoater drive on the back wall
    rc_rail_z=120.0, rc_screw_y=58.0, rc_screw_z=80.0,
    # optics: Thorlabs FTH254-1064 (WD 301.2 mm, flange focal length 348.5 mm, housing Ø120 x 67.8 mm)
    lens_wd=301.2, lens_ffl=348.5, lens_d=120.0, lens_len=67.8, beam_z=420.0,
    # frame (30 mm T-slot): inner faces
    fx0=-345.0, fx1=255.0, fy=175.0, fz_bot=-470.0, fz_top=540.0, deck_z=-32.0,
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


# ---- T-slot extrusion (30 mm series, 8 mm slot) -------------------------------------------
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
    s = s.push([(0, 0)]).circle(3.4, mode="s").reset()
    return s


def tslot(p0, axis, L):
    """30 mm T-slot rail of length L whose profile centre starts at p0 and runs along axis."""
    s = cq.Workplane("XY").placeSketch(_tslot_sketch()).extrude(L).val()
    if axis == "x":
        s = s.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    elif axis == "y":
        s = s.rotate(V(0, 0, 0), V(1, 0, 0), -90)
    return s.translate(V(*p0))


# ---- Linear guide (MGN-style miniature rail) ------------------------------------------------
def guide_rail(L, w, h):
    """Rail along local +x from 0..L, centred in y, base on z=0."""
    r = cq.Workplane("XY").box(L, w, h, centered=(False, True, False)).edges("|X and >Z").chamfer(0.8).val()
    # mounting holes
    for x in range(int(12.5), int(L), 25):
        r = r.cut(cyl(1.75, (x, 0, h - 3), "z", 3.1)).cut(cyl(3.0, (x, 0, h - 3.5), "z", 3.6))
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
KF = {16: (30.0, 17.2), 25: (40.0, 25.4), 40: (55.0, 41.3), 50: (75.0, 52.0)}


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
    lz0, lz1 = P["lid_z0"], P["lid_z1"]
    fx0, fx1, fy = P["fx0"], P["fx1"], P["fy"]
    zb, zt = P["fz_bot"], P["fz_top"]
    deck = P["deck_z"]
    h = TS / 2

    # ===================== 1. Frame =====================
    ux = (fx0 - h, fx1 + h)        # upright centres
    uy = (-fy - h, fy + h)
    frame = []
    for x in ux:
        for y in uy:
            frame.append(tslot((x, y, zb), "z", zt - zb))
    levels = {"bottom": zb + h, "deck": deck - h, "top": zt - h}
    for lvl, z in levels.items():
        for y in uy:   # X rails (front/back)
            frame.append(tslot((fx0, y, z), "x", fx1 - fx0))
        for x in ux:   # Y rails (sides)
            frame.append(tslot((x, -fy, z), "y", 2 * fy))
    # optics-level side rails + the two X cross members that carry the galvo plate
    z_opt = P["lens_ffl"] - 15 - h
    for x in ux:
        frame.append(tslot((x, -fy, z_opt), "y", 2 * fy))
    for y in (-95.0, 95.0):
        frame.append(tslot((fx0, y, z_opt), "x", fx1 - fx0))
    # extra deck supports under the deck plate
    for x in (-160.0, 130.0):
        frame.append(tslot((x, -fy, deck - h), "y", 2 * fy))
    add("T-slot frame (30 mm)", comp(frame), C["tslot"], 1, (0, 0, 0), bom="F1", mcm="TSLOT")
    brackets = []
    for x in ux:
        for y in uy:
            for z in levels.values():
                sx = 1 if x < 0 else -1
                sy = 1 if y < 0 else -1
                zz = z + (h if z < 0 else -h)
                brackets.append(box(min(x + sx * h, x + sx * (h + 26)), max(x + sx * h, x + sx * (h + 26)),
                                    y - 9, y + 9, min(zz, zz + (26 if z < 0 else -26)), max(zz, zz + (26 if z < 0 else -26))))
    add("Corner brackets", comp(brackets), C["alu_dark"], 1, (0, 0, 0), bom="F2", mcm="TSLOT_BRACKET")
    feet = []
    for x in ux:
        for y in uy:
            feet += [cyl(6, (x, y, zb - 30), "z", 30), cyl(24, (x, y, zb - 40), "z", 10),
                     cq.Solid.makeCone(24, 20, 6, V(x, y, zb - 34), V(0, 0, 1))]
    add("Leveling mounts", comp(feet), C["anod"], 1, (0, 0, -120), bom="F3", mcm="FOOT")

    # ===================== 2. Deck plate and optics rails =====================
    dk = box(fx0, fx1, -fy - TS, fy + TS, deck, deck + 12)
    for (x, y, r) in [(0, 0, 48), (P["ovf_x0"] / 2 + P["ovf_x1"] / 2, 0, 31), (0, -108, 22), (0, 105, 22)]:
        dk = dk.cut(cyl(r, (x, y, deck - 1), "z", 14))
    # deck sits just below the chamber floor: chamber floor underside is at z = -floor
    dk = dk.translate(V(0, 0, -P["floor"] - (deck + 12)))
    add("Deck plate (6061, 12 mm)", dk, C["alu"], 2, (0, 0, 220), bom="F4", mcm="PLATE_DECK")
    z_gp0 = P["lens_ffl"] - 15
    gp = box(fx0, 175, -110, 110, z_gp0, P["lens_ffl"])
    gp = gp.cut(cyl(P["lens_d"] / 2 + 3, (0, 0, z_gp0 - 1), "z", 17))
    add("Galvo plate (6061, 15 mm)", gp, C["alu"], 9, (0, 0, 260), bom="F5", mcm="PLATE_GALVO")

    # ===================== 3. Z axis =====================
    zf = -fl                                  # chamber floor underside
    bx0, bx1, by0, by1 = -110.0, 40.0, 60.0, 72.0
    zbp0 = -415.0
    bp = box(bx0, bx1, by0, by1, zbp0, zf - 12)
    add("Z back plate", bp, C["alu"], 3, (0, 220, 0), bom="M3")
    # rail (MGN15) vertical on the back plate's front face
    rail_x = -40.0
    zr0, zr1 = -385.0, -70.0
    zrail = guide_rail(zr1 - zr0, 15.0, 10.0)
    zrail = place(zrail, (rail_x, by0, zr0), (0, 0, 1), (0, -1, 0))
    add("Z guide rail", zrail, C["steel"], 3, (0, 160, 0), bom="M3", mcm="RAIL_Z")
    z_arm = -235.0                            # lift-arm underside at the start of a build (piston up)
    zc = guide_carriage(58.8, 32.0, 16.0, 4.0, 15.0, 10.0)
    zc = place(zc, (rail_x, by0, z_arm + 20), (0, 0, 1), (0, -1, 0))
    add("Z carriage", zc, C["steel"], 3, (0, 160, 0), group="piston", bom="M3", mcm="CARRIAGE_Z")
    zcp = box(-62, -18, by0 - 16 - 8, by0 - 16, z_arm - 10, z_arm + 50)
    add("Z carriage plate", zcp, C["alu"], 3, (0, 160, 0), group="piston", bom="M3")
    sx, sy = -85.0, 28.0
    arm = rbox(-112, 18, -20, by0 - 24, z_arm, z_arm + 15, 6)
    arm = arm.cut(cyl(6.2, (0, 0, z_arm - 1), "z", 17)).cut(cyl(7, (sx, sy, z_arm - 1), "z", 17))
    add("Z lift arm", arm, C["alu"], 3, (0, -160, 0), group="piston", bom="M3")
    add("Rod clamp", tube(16, 6.1, (0, 0, z_arm - 22), "z", 22), C["alu_dark"], 3, (0, -160, 0), group="piston", bom="M3")
    zscrew = ball_screw(230.0, 12.0, 8.0, 25.0)
    zscrew = place(zscrew, (sx, sy, -420.0), (0, 0, 1), (1, 0, 0))
    add("Z ball screw (12 mm)", zscrew, C["steel"], 3, (0, -200, 0), bom="M3", mcm="SCREW_Z")
    znut = ball_nut(12.0, 24.0, 40.0, 40.0, 10.0, 16.0)
    znut = place(znut, (sx, sy, z_arm - 20), (0, 0, -1), (1, 0, 0))
    add("Z ball nut", znut, C["steel"], 3, (0, -200, 0), group="piston", bom="M3", mcm="NUT_Z")
    add("Z fixed support", box(sx - 30, sx + 30, sy - 25, by0, -215, -190), C["anod"], 3, (0, -200, 0), bom="M3", mcm="SUPPORT_Z_FIXED")
    add("Z floating support", box(sx - 30, sx + 30, sy - 25, by0, -420, -400), C["anod"], 3, (0, -200, 0), bom="M3", mcm="SUPPORT_Z_FLOAT")
    add("Z coupling", place(bellows_coupling(25, 30), (sx, sy, -190), (1, 0, 0), (0, 0, 1)), C["ss"], 3, (0, -200, 0), bom="M3", mcm="COUPLING")
    mm = box(sx - 35, sx + 35, sy - 32, by0, -160, -150).cut(cyl(20, (sx, sy, -161), "z", 12))
    add("Z motor mount", mm, C["alu"], 3, (0, -200, 0), bom="M3")
    zmot = place(servo_nema23(100.0, 20.0), (sx, sy, -150.0), (1, 0, 0), (0, 0, -1))
    add("Z servo (ClearPath-SD, NEMA 23)", zmot, C["motor"], 3, (0, -260, 0), bom="M2")

    # ===================== 4. Build cylinder, piston, plate, overflow =====================
    rcyl, rb = P["cyl_od"] / 2, P["bore_d"] / 2
    cylp = comp([tube(rcyl, rb, (0, 0, zf - P["cyl_len"]), "z", P["cyl_len"]),
                 tube(45, rb, (0, 0, zf - 10), "z", 10),
                 tube(45, 6.5, (0, 0, zf - P["cyl_len"] - 10), "z", 10),
                 tube(18, 6.5, (0, 0, zf - P["cyl_len"] - 22), "z", 12)])
    add("Build cylinder (2 in. ID honed tube, flanged)", cylp, C["ss"], 4, (0, 0, -250), bom="M3", mcm="TUBE_BUILD", section=True)
    pz = 0.0
    plate = cyl(P["plate_d"] / 2, (0, 0, pz - P["plate_t"]), "z", P["plate_t"])
    add("Build plate (Ø50, swappable)", plate, C["alu_dark"], 4, (0, 0, 260), group="piston", bom="M3")
    piston = comp([cyl(rb - 0.4, (0, 0, pz - P["plate_t"] - P["piston_t"]), "z", P["piston_t"])])
    piston = piston.cut(tube(rb, rb - 2.2, (0, 0, pz - P["plate_t"] - 18), "z", 6))
    add("Piston (heater + felt/PTFE seal)", piston, C["alu"], 4, (0, 0, 260), group="piston", bom="M3")
    add("Piston seal ring", tube(rb - 0.05, rb - 2.2, (0, 0, pz - P["plate_t"] - 18), "z", 6), C["white"], 4, (0, 0, 260), group="piston", bom="M3", mcm="SEAL_PISTON")
    rod_top = pz - P["plate_t"] - P["piston_t"]
    add("Piston rod (12 mm, hardened)", cyl(6, (0, 0, z_arm - 20), "z", rod_top - z_arm + 20), C["ss"], 4, (0, 0, 260), group="piston", bom="M3", mcm="ROD")
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    # overflow port welded under the floor slot (flange faces down), and the jar that clamps to it
    ovf = place(kf_stub(40, 16), (ox, 0, zf - 16), (1, 0, 0), (0, 0, -1))
    add("Overflow port (KF-40)", ovf, C["ss"], 5, (0, 0, -150), bom="G7", mcm="KF40_WELD")
    jar = comp([place(kf_stub(40, 70), (ox, 0, zf - 16), (1, 0, 0), (0, 0, 1)),
                cyl(KF[40][1] / 2, (ox, 0, zf - 16 - 72), "z", 2)])
    add("Overflow jar (KF-40 half nipple + blank)", jar, C["ss"], 4, (0, 0, -220), bom="M4", mcm="KF40_NIPPLE")
    add("Overflow clamp", place(kf_clamp(40), (ox, 0, zf - 16), (1, 0, 0), (0, 0, 1)), C["alu_dark"], 4, (0, 0, -220), bom="G7", mcm="KF40_CLAMP")

    # ===================== 5. Chamber body =====================
    ch = rbox(-cx, cx, -cy, cy, -fl, lz0, 8)
    ch = ch.cut(rbox(-ix, ix, -iy, iy, 0, lz0 + 1, 4))
    dz0, dz1 = 44.0, 146.0                    # door opening
    ch = ch.cut(box(-110, 110, -cy - 1, -iy + 1, dz0, dz1))
    ch = ch.cut(box(-35, 35, iy - 1, cy + 1, 4, 12))          # cross-flow inlet slot (70 x 8)
    ch = ch.cut(box(-45, 45, -cy - 1, -iy + 1, 4, 24))        # outlet slot
    ch = ch.cut(cyl(rb + 0.2, (0, 0, -fl - 1), "z", fl + 2))  # build bore
    ch = ch.cut(box(P["ovf_x0"], P["ovf_x1"], -P["ovf_y"], P["ovf_y"], -fl - 1, 1))
    ch = ch.cut(cyl(9, (-cx - 1, P["rc_screw_y"], P["rc_screw_z"]), "x", P["wall"] + 2))
    ch = ch.cut(cyl(9, (ix - 1, P["rc_screw_y"], P["rc_screw_z"]), "x", P["wall"] + 2))
    ch = ch.cut(cyl(12.5, (ix - 1, 0, 115), "x", P["wall"] + 2))          # vacuum port
    ch = ch.cut(cyl(4, (-cx - 1, -30, 130), "x", P["wall"] + 2))         # argon in
    ch = ch.cut(cyl(3, (ix - 1, -40, 18), "x", P["wall"] + 2))           # O2 sample
    add("Process chamber body (6061, ~6.2 L)", ch, C["alu"], 5, (0, 0, 260), bom="G1", mcm="PLATE_CHAMBER", section=True)
    plen_in = rbox(-55, 55, cy, cy + 32, -8, 30, 4).cut(box(-50, 50, cy - 1, cy + 27, -3, 25))
    add("Cross-flow inlet plenum + nozzle", plen_in, C["alu_dark"], 5, (0, 180, 0), bom="G4")
    plen_out = rbox(-60, 60, -cy - 34, -cy, -8, 31, 4).cut(box(-55, 55, -cy - 29, -cy + 1, -3, 26))
    add("Cross-flow outlet plenum", plen_out, C["alu_dark"], 5, (0, -180, 0), bom="G4", section=True)
    add("Inlet plenum KF-25 port", place(kf_stub(25, 30), (0, cy + 16, -38), (1, 0, 0), (0, 0, -1)), C["ss"], 5, (0, 180, 0), bom="G7", mcm="KF25_WELD")
    add("Outlet plenum KF-25 port", place(kf_stub(25, 30), (0, -cy - 17, -38), (1, 0, 0), (0, 0, -1)), C["ss"], 5, (0, -180, 0), bom="G7", mcm="KF25_WELD")
    add("Vacuum port (KF-25)", place(kf_stub(25, 22), (cx + 18, 0, 115), (0, 1, 0), (1, 0, 0)), C["ss"], 5, (180, 0, 0), bom="G7", mcm="KF25_WELD")
    add("Layer-light LED bar", box(ix - 6, ix - 1, -45, 45, 8, 16), C["white"], 5, (0, 0, 120), bom="M6")
    add("Gas knife (cover-slide purge)", box(-32, 32, -40, -33, lz0 - 14, lz0 - 8), C["ss"], 7, (0, 0, 200), bom="L7")

    # ===================== 6. Recoater =====================
    ry, rz = P["rc_screw_y"], P["rc_screw_z"]
    rrail = place(guide_rail(250.0, 12.0, 8.0), (-125, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))
    add("Recoater guide rail", rrail, C["steel"], 6, (0, 0, 220), bom="M1", mcm="RAIL_RC")
    xc = P["x_park"]
    rcar = place(guide_carriage(45.4, 27.0, 13.0, 3.0, 12.0, 8.0), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))
    add("Recoater carriage", rcar, C["steel"], 6, (0, 0, 220), group="recoater", bom="M1", mcm="CARRIAGE_RC")
    cy_front = iy - 13.0
    blk = comp([box(xc - 25, xc + 25, 40, cy_front, 66, 140), box(xc - 25, xc + 25, cy_front, 72, 66, 96)])
    blk = blk.cut(cyl(13, (xc - 26, ry, rz), "x", 52))
    add("Recoater carriage block", blk, C["alu"], 6, (0, 0, 220), group="recoater", bom="M1")
    add("Recoater ball screw (12 mm, 10 mm lead)", place(ball_screw(2 * cx + 10, 12.0, 8.0, 22.0), (-cx - 5, ry, rz), (1, 0, 0), (0, 0, 1)), C["steel"], 6, (0, 0, 220), bom="M1", mcm="SCREW_RC")
    add("Recoater ball nut", place(ball_nut(12.0, 24.0, 40.0, 40.0, 10.0, 15.0), (xc - 25 - 20 + 20, ry, rz), (-1, 0, 0), (0, 0, 1)), C["steel"], 6, (0, 0, 220), group="recoater", bom="M1", mcm="NUT_RC")
    add("Recoater arm", box(xc - 6, xc + 6, 32, 40, 14, 70), C["alu"], 6, (0, 0, 220), group="recoater", bom="M5")
    bar = rbox(xc - 7, xc + 7, -P["dose_y"] - 3, 40, 3, 23, 2, "|Y")
    add("Blade holder", bar, C["anod"], 6, (0, 0, 220), group="recoater", bom="M5")
    add("Silicone-cord blade (3 mm)", cyl(1.6, (xc + 6, -P["dose_y"] - 2, 1.6), "y", 2 * P["dose_y"] + 40), C["silicone"], 6, (0, 0, 220), group="recoater", bom="M5", mcm="CORD_SILICONE")
    bh_l = comp([cyl(25, (-cx - 20, ry, rz), "x", 20), box(-cx - 20, -cx, ry - 25, ry + 25, rz - 25, rz - 18)])
    add("Recoater bearing + shaft-seal housing", bh_l, C["anod"], 6, (-160, 0, 0), bom="M1", mcm="SEAL_SHAFT")
    add("Recoater floating bearing housing", cyl(20, (cx, ry, rz), "x", 14), C["anod"], 6, (160, 0, 0), bom="M1")
    add("Recoater motor standoff", tube(30, 26, (-cx - 60, ry, rz), "x", 40), C["alu_dark"], 6, (-200, 0, 0), bom="M1")
    add("Recoater coupling", place(bellows_coupling(25, 30), (-cx - 55, ry, rz), (0, 1, 0), (1, 0, 0)), C["ss"], 6, (-200, 0, 0), bom="M1", mcm="COUPLING")
    rmot = place(servo_nema23(100.0, 20.0), (-cx - 60, ry, rz), (0, 1, 0), (1, 0, 0))
    add("Recoater servo (ClearPath-SD, NEMA 23)", rmot, C["motor"], 6, (-260, 0, 0), bom="M2")
    add("Recoater motor bracket", box(-cx - 162, -cx - 60, ry - 40, ry + 28, -fl, rz - 28.6), C["alu_dark"], 6, (-260, 0, 0), bom="M1")

    # ===================== 7. Lid and what sits on it =====================
    lid = rbox(-cx, cx, -cy, cy, lz0, lz1, 8)
    lid = lid.cut(cyl(28, (0, 0, lz0 - 1), "z", P["lid"] + 2))
    xd = P["x_dose"]
    lid = lid.cut(box(xd - 6, xd + 6, -P["dose_y"], P["dose_y"], lz0 - 1, lz1 + 1))
    cam_p = V(75, -45, lz1)
    lid = lid.cut(cyl(11, (75, -45, lz0 - 1), "z", P["lid"] + 2))
    for (x, y) in [(100, 50), (110, -62)]:
        lid = lid.cut(cyl(4, (x, y, lz0 - 1), "z", P["lid"] + 2))
    add("Chamber lid (6061, 20 mm)", lid, C["alu"], 7, (0, 0, 300), bom="G1", mcm="PLATE_CHAMBER")
    bolts = []
    for i in range(7):
        x = -cx + 18 + i * (2 * cx - 36) / 6
        for y in (-cy + 9, cy - 9):
            bolts.append(shcs_head((x, y, lz1), "z", 9, 5))
    for y in (-cy / 3, cy / 3):
        for x in (-cx + 9, cx - 9):
            bolts.append(shcs_head((x, y, lz1), "z", 9, 5))
    add("Lid screws (M5 SHCS)", comp(bolts), C["steel"], 7, (0, 0, 340), bom="G1", mcm="SHCS_M5")
    add("Lid O-ring (Viton cord)", rbox(-cx + 4, cx - 4, -cy + 4, cy - 4, lz0 - 0.5, lz0 + 0.5, 6).cut(rbox(-cx + 6, cx - 6, -cy + 6, cy - 6, lz0 - 1, lz0 + 1, 5)),
        C["black"], 7, (0, 0, 280), bom="G8", mcm="ORING_CORD")
    wf = tube(50, 24, (0, 0, lz1), "z", 22).cut(cyl(25.65, (0, 0, lz1 + 10), "z", 13))
    add("Window flange", wf, C["anod"], 7, (0, 0, 360), bom="L7")
    add("Ø2 in. fused-silica window", cyl(25.4, (0, 0, lz1 + 10), "z", 12), C["glass"], 7, (0, 0, 380), bom="L7", opacity=0.45)
    rr = tube(50, 22, (0, 0, lz1 + 22), "z", 5)
    rrb = comp([rr] + [shcs_head((42 * math.cos(math.radians(a)), 42 * math.sin(math.radians(a)), lz1 + 27), "z", 7, 4) for a in range(0, 360, 60)])
    add("Window retaining ring", rrb, C["anod"], 7, (0, 0, 400), bom="L7")
    add("Field-stop aperture", tube(27.9, 18, (0, 0, lz0), "z", 10), C["black"], 7, (0, 0, 300), bom="L7")
    add("Cover-slide holder + slide", comp([tube(35, 27, (0, 0, lz0 - 6), "z", 6), cyl(27, (0, 0, lz0 - 4), "z", 1)]), C["anod"], 7, (0, 0, 220), bom="L7")
    chute = box(xd - 6, xd + 6, -P["dose_y"], P["dose_y"], 26, lz0).cut(box(xd - 4.5, xd + 4.5, -P["dose_y"] + 1.5, P["dose_y"] - 1.5, 25, lz0 + 1))
    add("Dose chute", chute, C["ss"], 7, (0, 0, 260), bom="M4")
    dbk = rbox(xd - 17, xd + 17, -55, 55, lz1, lz1 + 50, 3)
    add("Dosing block (fluted roller inside)", dbk, C["alu"], 7, (0, 0, 300), bom="M4")
    add("Roller shaft seal housing", cyl(15, (xd, 55, lz1 + 25), "y", 10), C["anod"], 7, (0, 0, 300), bom="M4", mcm="SEAL_SHAFT")
    add("Dosing stepper (NEMA 17)", place(stepper_nema17(40), (xd, 65 + 2, lz1 + 25), (1, 0, 0), (0, -1, 0)).translate(V(0, 0, 0)), C["motor"], 7, (0, 160, 300), bom="M4", mcm="STEPPER17")
    hop = rbox(xd - 17, xd + 17, -42, 42, lz1 + 50, lz1 + 112, 3)
    hop = hop.cut(rbox(xd - 15, xd + 15, -40, 40, lz1 + 53, lz1 + 113, 2))
    add("Hopper cartridge (~100 cm3, 316 SS)", hop, C["ss"], 7, (0, 0, 380), bom="M4", mcm="HOPPER")
    add("Hopper powder", box(xd - 15, xd + 15, -40, 40, lz1 + 53, lz1 + 95), C["powder"], 7, (0, 0, 380), bom="M4")
    cap = comp([rbox(xd - 19, xd + 19, -44, 44, lz1 + 112, lz1 + 116, 3), box(xd - 4, xd + 4, -20, 20, lz1 + 116, lz1 + 124)])
    add("Hopper cap", cap, C["anod"], 7, (0, 0, 420), bom="M4")
    add("Load cell (under cartridge)", box(xd - 17, xd + 17, 44, 60, lz1 + 40, lz1 + 52), C["ss"], 7, (0, 0, 380), bom="M4", mcm="LOADCELL")
    # angled camera viewport: tube pointing at the plate centre
    d = (V(0, 0, 0) - cam_p).normalized()
    up = d * -1
    boss = cq.Solid.makeCylinder(16, 40, cam_p, up).cut(cq.Solid.makeCylinder(11, 40, cam_p, up))
    add("Camera viewport boss + Ø1 in. window", boss, C["anod"], 7, (0, 0, 300), bom="M6")
    cam_base = cam_p + up * 40
    cam = comp([cq.Solid.makeCylinder(15, 38, cam_base, up),
                place(box(-19, 19, -19, 19, 0, 8), (cam_base + up * 38).toTuple(), (1, 0, 0) if abs(up.x) < 0.9 else (0, 1, 0), up.toTuple())])
    add("Layer camera (Pi HQ + C-mount lens)", cam, C["black"], 7, (0, 0, 340), bom="M6")
    add("Pressure transducer", comp([cyl(4, (100, 50, lz1), "z", 12), cyl(11, (100, 50, lz1 + 12), "z", 52)]), C["ss"], 7, (0, 0, 300), bom="G7", mcm="TRANSDUCER")
    add("Overpressure relief valve", comp([cyl(4, (110, -62, lz1), "z", 10), cyl(9, (110, -62, lz1 + 10), "z", 28)]), C["brass"], 7, (0, 0, 300), bom="G7", mcm="RELIEF")

    # ===================== 8. Door =====================
    dy0, dy1 = -cy - 15, -cy
    door = rbox(-122, 122, dy0, dy1, dz0 - 12, dz1 + 12, 6)
    add("Chamber door (6061, 15 mm)", door, C["alu"], 8, (0, -240, 0), bom="G1", mcm="PLATE_CHAMBER", section=True)
    add("Door O-ring", rbox(-116, 116, dy1 - 0.2, dy1 + 0.6, dz0 - 6, dz1 + 6, 5, "|Y").cut(rbox(-114, 114, dy1 - 1, dy1 + 1, dz0 - 4, dz1 + 4, 4, "|Y")), C["black"], 8, (0, -200, 0), bom="G8", mcm="ORING_CORD", section=True)
    hinges = []
    for z in (dz0 + 8, dz1 - 22):
        hinges += [box(-cx - 2, -110, dy0 - 3, dy0, z, z + 14), cyl(4, (-cx - 2, dy0 - 3, z), "z", 14)]
    add("Door hinges (SS)", comp(hinges), C["ss"], 8, (0, -240, 0), bom="G1", mcm="HINGE_DOOR", section=True)
    latches = []
    for z in (dz0 + 10, dz1 - 30):
        latches += [box(cx - 8, cx + 4, dy0 - 10, dy0 + 4, z, z + 20), box(105, 122, dy0 - 6, dy0, z + 4, z + 16)]
    add("Draw latches (SS)", comp(latches), C["ss"], 8, (0, -240, 0), bom="G1", mcm="LATCH", section=True)
    handle = comp([cyl(5, (-20, dy0, (dz0 + dz1) / 2), "-y", 30), cyl(5, (40, dy0, (dz0 + dz1) / 2), "-y", 30),
                   cyl(6, (-25, dy0 - 30, (dz0 + dz1) / 2), "x", 70)])
    add("Door handle", handle, C["anod"], 8, (0, -260, 0), bom="G1", section=True)

    # ===================== 9. Optics =====================
    zg0 = P["lens_ffl"]
    lens = comp([cyl(P["lens_d"] / 2, (0, 0, P["lens_wd"]), "z", zg0 - P["lens_wd"]),
                 cyl(42.5, (0, 0, zg0), "z", P["lens_wd"] + P["lens_len"] - zg0),
                 cyl(30, (0, 0, P["lens_wd"] - 1), "z", 1.5)])
    add("f-theta lens, f = 254 mm (FTH254-1064 envelope)", lens, C["black"], 9, (0, 0, 300), bom="L6")
    galvo = rbox(-75, 75, -65, 65, zg0, zg0 + 115, 8)
    galvo = comp([galvo, cyl(17, (-90, 0, P["beam_z"]), "x", 15), box(-60, 60, 65, 72, zg0 + 15, zg0 + 60)])
    add("2-axis galvo scan head (basiCube 20 class)", galvo, C["anod"], 9, (0, 0, 340), bom="L5")
    sh = comp([rbox(-160, -105, -32, 32, P["beam_z"] - 26, P["beam_z"] + 26, 4),
               box(-150, -115, -20, 20, zg0, P["beam_z"] - 26),
               box(-147, -118, 32, 44, P["beam_z"] - 20, P["beam_z"] + 20)])
    add("Safety shutter + beam dump", sh, C["yellow"], 9, (0, 0, 340), bom="L4")
    coll = comp([cyl(20, (-300, 0, P["beam_z"]), "x", 110), cyl(14, (-330, 0, P["beam_z"]), "x", 30),
                 box(-285, -215, -22, 22, zg0, P["beam_z"] - 18)])
    add("Collimator (QBH) on V-mount", coll, C["ss"], 9, (0, 0, 340), bom="L3")

    # ===================== 10. Gas loop and vacuum =====================
    fxc, fyc = 175.0, -95.0
    filt = comp([cyl(45, (fxc, fyc, -300), "z", 170), cyl(48, (fxc, fyc, -140), "z", 12), cyl(48, (fxc, fyc, -300), "z", 12),
                 place(kf_stub(25, 20), (fxc, fyc, -110), (1, 0, 0), (0, 0, 1)),
                 place(kf_stub(25, 20), (fxc, fyc, -320), (1, 0, 0), (0, 0, -1))])
    add("Sealed filter housing (cyclone + HEPA)", filt, C["ss"], 10, (220, 0, 0), bom="G5", mcm="FILTER")
    bl = comp([rbox(fxc - 55, fxc + 55, 40, 130, -265, -175, 8), cyl(30, (fxc, 85, -175), "z", 30),
               cyl(14, (fxc, 40, -220), "-y", 30), cyl(14, (fxc - 40, 130, -220), "y", 25)])
    add("Recirculation blower (sealed)", bl, C["blue"], 10, (220, 0, 0), bom="G4", mcm="BLOWER")
    hoses = [
        [(0, -cy - 17, -60), (0, -cy - 17, -110), (60, -130, -120), (fxc, fyc, -60), (fxc, fyc, -110)],
        [(fxc, fyc, -340), (fxc, fyc - 10, -380), (fxc + 40, 0, -360), (fxc, 10, -235), (fxc, 40 - 30, -220)],
        [(fxc - 40, 155, -220), (fxc - 120, 150, -180), (60, cy + 16, -110), (0, cy + 16, -60)],
    ]
    add("Gas-loop hoses (KF-25 SS bellows)", comp([polyline_pipe(hp, 13) for hp in hoses]), C["hose"], 10, (0, 0, -160), bom="G7", mcm="HOSE_KF25")
    vv = comp([place(kf_clamp(25), (cx + 18, 0, 115), (0, 1, 0), (1, 0, 0)),
               box(cx + 20, cx + 70, -22, 22, 93, 137), cyl(16, (cx + 45, 0, 137), "z", 30), cyl(26, (cx + 45, 0, 167), "z", 8),
               place(kf_stub(25, 15), (cx + 45, 0, 93), (1, 0, 0), (0, 0, -1))])
    add("Vacuum isolation valve (KF-25 angle)", vv, C["ss"], 10, (220, 0, 0), bom="G7", mcm="VALVE_KF25")
    pumpx = 470.0
    pump = comp([rbox(pumpx - 150, pumpx + 150, -80, 80, -510, -440, 6), rbox(pumpx - 140, pumpx + 20, -70, 70, -440, -300, 10),
                 cyl(70, (pumpx + 20, 0, -380), "x", 150), cyl(12, (pumpx - 100, 0, -300), "z", 40)])
    add("Two-stage rotary-vane vacuum pump", pump, C["blue"], 10, (300, 0, 0), bom="G2", mcm="PUMP")
    add("Vacuum hose (KF-25)", polyline_pipe([(cx + 45, 0, 78), (cx + 45, 0, -60), (330, 0, -120), (pumpx - 100, 0, -200), (pumpx - 100, 0, -262)], 13), C["hose"], 10, (220, 0, 0), bom="G7", mcm="HOSE_KF25")
    sol = comp([box(-300, -200, -150, -125, -10, 15)] + [comp([cyl(13, (x, -137.5, 15), "z", 45), box(x - 10, x + 10, -147, -128, 60, 75)]) for x in (-285, -250, -215)])
    add("Argon solenoid manifold (purge / make-up / vent)", sol, C["brass"], 10, (-200, 0, 0), bom="G7", mcm="SOLENOID")
    add("Argon line (1/4 in. SS)", polyline_pipe([(-215, -137, -10), (-215, -137, -20), (-190, -60, -10), (-cx - 30, -30, 130), (-cx, -30, 130)], 3.2), C["ss"], 10, (-200, 0, 0), bom="G7", mcm="TUBE_SS")
    o2 = comp([rbox(-330, -170, -165, -95, -230, -90, 5), box(-300, -200, -166, -165, -130, -100)])
    add("Trace O2 analyzer (Ntron Microx class)", o2, C["white"], 10, (-200, 0, 0), bom="G6")
    add("O2 sample line", polyline_pipe([(ix + 15, -40, 18), (cx + 30, -40, 18), (cx + 40, -140, -10), (0, -168, -60), (-200, -150, -90), (-200, -130, -90)], 3.2), C["ss"], 10, (0, -200, 0), bom="G6", mcm="TUBE_SS")

    # ===================== 11. Electronics + operator panel =====================
    din = []
    elx = fx0 + 2
    for z in (-260.0, -380.0):
        din.append(box(elx, elx + 8, -10, 165, z - 17.5, z + 17.5))
    add("DIN rails", comp(din), C["din"], 11, (-200, 0, 0), bom="C4", mcm="DIN")
    el = []
    el.append(("24 V supply (SDR-480-24)", box(elx + 8, elx + 8 + 128.5, 70, 155.5, -330, -205), C["white"], "C4"))
    el.append(("Safety relay (G9SE-201)", box(elx + 8, elx + 8 + 115, 40, 57.5, -310, -210), C["yellow"], "S1"))
    el.append(("Motion controller (ClearCore)", box(elx + 8, elx + 8 + 30, -5, 35, -330, -190), C["pcb"], "C3"))
    el.append(("Supervisor (Pi 5 in case)", box(elx + 8, elx + 8 + 32, 60, 155, -430, -365), C["red"], "C2"))
    el.append(("Scan + laser controller", box(elx + 8, elx + 8 + 40, -5, 55, -440, -330), C["pcb"], "C1"))
    el.append(("Terminal blocks", box(elx + 8, elx + 8 + 45, 0, 50, -395, -365), C["din"], "C4"))
    for nm, shp, col, b in el:
        add(nm, shp, col, 11, (-220, 0, 0), bom=b)
    pz0 = 120.0
    fyf = -fy - TS - 2.0                      # outer face of the fixed front column
    pnl = rbox(212, 272, fyf - 34, fyf, pz0, pz0 + 200, 4)
    add("Operator panel box", pnl, C["anod"], 11, (0, -200, 0), bom="S4")
    bx = 242.0
    ops = [("E-stop", comp([cyl(20, (bx, fyf - 34, pz0 + 160), "-y", 8), cyl(17, (bx, fyf - 42, pz0 + 160), "-y", 14)]), C["red"], "S3"),
           ("Key switch", comp([cyl(13, (bx, fyf - 34, pz0 + 112), "-y", 6), box(bx - 4, bx + 4, fyf - 48, fyf - 40, pz0 + 109, pz0 + 115)]), C["ss"], "S4"),
           ("Emission indicator", cyl(11, (bx, fyf - 34, pz0 + 72), "-y", 10), C["red"], "S4"),
           ("Reset button", cyl(11, (bx, fyf - 34, pz0 + 35), "-y", 10), C["blue"], "S4")]
    for nm, shp, col, b in ops:
        add(nm, shp, col, 11, (0, -220, 0), bom=b)
    stx, sty = fx1 + h, -fy - h
    stack = comp([cyl(5, (stx, sty, zt), "z", 60), cyl(22, (stx, sty, zt + 60), "z", 6)])
    add("Stack light pole", stack, C["anod"], 11, (0, 0, 220), bom="S4", mcm="STACK")
    for i, col in enumerate(("green", "yellow", "red")):
        add(f"Stack light {col}", cyl(20, (stx, sty, zt + 66 + i * 34), "z", 32), C[col], 11, (0, 0, 220 + 30 * i), bom="S4", opacity=0.9)

    # ===================== 12. Laser source + fiber =====================
    if include_context:
        ly0, ly1 = 330.0, 830.0
        laser = comp([rbox(-560, -80, ly0, ly1, -510, -377, 6), box(-540, -100, ly0 - 3, ly0, -500, -387),
                      cyl(10, (-150, ly0 - 3, -420), "-y", 10)])
        add("Fiber laser source (500 W, 3U)", laser, C["white"], 12, (0, 300, 0), bom="L1")
        add("Chiller (beside the laser)", rbox(-1000, -620, ly0 + 40, ly1 - 60, -510, -60, 8), C["blue"], 12, (0, 300, 0), bom="L2")
        fiber = polyline_pipe([(-150, ly0 - 13, -420), (-150, ly0 - 120, -380), (-250, fy + 60, 0), (-300, fy - 20, P["beam_z"] - 30),
                               (-345, 60, P["beam_z"]), (-345, 10, P["beam_z"]), (-330, 0, P["beam_z"])], 5)
        add("Process fiber (armoured)", fiber, C["fiber"], 12, (0, 300, 0), bom="L1")

    # ===================== 13. Laser guard panels =====================
    pt = 2.0
    pnls = []
    pnls.append(box(fx0 - TS, fx0 - TS + pt, -fy - TS, fy + TS, zb, zt))             # left
    pnls.append(box(fx1 + TS - pt, fx1 + TS, -fy - TS, fy + TS, zb, zt))             # right
    pnls.append(box(fx0 - TS, fx1 + TS, fy + TS - pt, fy + TS, zb, zt))              # back
    pnls.append(box(fx0 - TS, fx1 + TS, -fy - TS, fy + TS, zt, zt + pt))             # top
    pnls.append(box(fx0 - TS, fx1 + TS, -fy - TS - pt, -fy - TS, zb, deck - TS))     # lower front
    add("Laser guard panels (aluminium sheet)", comp(pnls), C["panel"], 13, (0, 0, 0), bom="S9", mcm="SHEET", opacity=0.22, section=True)
    xdoor = 200.0
    pnls2 = [box(xdoor, fx1 + TS, -fy - TS - pt, -fy - TS, deck - TS, zt)]          # fixed control column
    add("Laser guard front column", comp(pnls2), C["panel"], 11, (0, -200, 0), bom="S9", mcm="SHEET", opacity=0.9)
    fd = box(fx0 - TS, xdoor - 2, -fy - TS - pt - 4, -fy - TS - pt, deck - TS, zt)
    wx0, wz0 = -213.0, 20.0
    fd = fd.cut(box(wx0, wx0 + 385.8, -fy - 50, -fy, wz0, wz0 + 304.8))
    add("Front guard door", fd, C["panel"], 13, (0, -260, 0), bom="S9", mcm="SHEET", opacity=0.35, section=True)
    add("OD 7+ laser-safety viewing window (LW1P1/M size)", box(wx0, wx0 + 385.8, -fy - TS - pt - 3, -fy - TS - pt - 1, wz0, wz0 + 304.8), C["laser_glass"], 13, (0, -260, 0), bom="S5", opacity=0.45, section=True)
    gh = comp([box(fx0 - TS + 2, fx0 + 2, -fy - TS - 12, -fy - TS - 4, z, z + 60) for z in (-10.0, 420.0)])
    add("Guard door hinges", gh, C["anod"], 13, (0, -260, 0), bom="F6", mcm="HINGE_TSLOT", section=True)
    add("Guard door handle", comp([cyl(5, (170, -fy - TS - 6, 180), "-y", 30), cyl(5, (170, -fy - TS - 6, 330), "-y", 30), cyl(6, (170, -fy - TS - 36, 172), "z", 166)]), C["anod"], 13, (0, -280, 0), bom="F7", mcm="HANDLE", section=True)
    add("Guard-locking door switch (Omron D4JL)", box(xdoor - 6, xdoor + 10, -fy - TS - 40, -fy - TS - 6, 400, 490), C["yellow"], 13, (0, -280, 0), bom="S2", section=True)

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
        a.export(str(out / "desktop-lpbf.glb"))
        print("wrote", *(p.name for p in out.iterdir()))
