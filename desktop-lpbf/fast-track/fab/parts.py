"""Fabrication-ready models of the fast-track machine's made parts MK-01..MK-24, split into the pieces a machinist makes
(#260, PR 294 round 2; ported to CAD v2, the g3 gantry, in round 3).

The assembly model (../cad/ft_model.py, owned by the CAD worker and not edited here) draws each made part as an envelope.
This file rebuilds every piece in its own part frame from ft_model's parameters (P, levels()) and adds what a shop needs:
bolt, tapped and clearance holes at every joint (ISO metric coarse, ISO 273 medium clearances, ISO 4762 / 10642 heads),
O-ring glands (Parker O-Ring Handbook ORD 5700 tables, see GLANDS), drill points on blind holes, corner radii a cutter can
leave, and the stock, route and setups for each piece. Every cut is recorded as a feature (drill, pocket, groove, bore,
opening), with its entry direction and tool, so cam.py (FreeCAD CAM, headless) can program it without guessing.

    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/parts.py      # builds all pieces, writes /tmp/ft-fab/pieces/*.brep,
                                                                    # /tmp/ft-fab/pieces.json (CAM spec), out/pieces.csv
Frames: mm. Each piece's +Z is its first setup's tool axis; "pos" says where its origin sits in ft_model's world frame.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402
import tools as T  # noqa: E402

P = M.P
if "clamp_h" in P or P["deck"][0] != 245.0 or P.get("gantry") != "four_post_braced_front_g3":
    sys.exit("parts.py builds the v2 fab set from ft_model with the g3 gantry (round 3, after e3853cf); this ft_model "
             "is not that model. The v1 set is parts.py at e3853cf.")
V = cq.Vector
IN = 25.4
OUT = HERE / "out"
SCRATCH = pathlib.Path("/tmp/ft-fab")

L_BOX, L_CUBE = M.levels("FT-1"), M.levels("FT-1V")
XC, YC = P["deck_c"]
WX, WY = M.window_centre("FT-1")          # window stack centre in the box (0, -11)
TXB, TYB = M.tube_centre("FT-1")          # beam-tube centre section in the box (0, -17)
LAX, LAY = P["axis_off"]                  # lens axis (0, -30)


def frame():
    """The g3 gantry's numbers, as ft_model.build() computes them (four 45 mm posts, two 30 mm cross-beams at the head
    flange, the head flange plate on the entrance face, its top flange and gussets, the far-side plate)."""
    h = 15.0
    ry = (YC - P["rail_dy"], YC + P["rail_dy"])
    ux = (XC - 260.0, XC + 260.0)
    hb = L_BOX["head_bot"]
    hp = P["post"] / 2
    y_f = ry[0] - h - P["front_post_gap"] - hp
    xe = LAX - P["head_obj_x"]
    z_beam = hb + 90.0
    z_up_top = P["lens_ffl"] + P["dz_cube"] + 90.0 + h + 10.0
    return dict(h=h, ry=ry, ux=ux, hb=hb, hp=hp, y_f=y_f, xe=xe, fl_x0=xe - 12.0, fl_x1=xe, z_beam=z_beam,
                z_up_top=z_up_top, zb=P["bench_z"], z_rail_top=L_BOX["under"], xf0=xe + P["head"][0],
                y_in=LAY - P["head_disp"], z_in=hb + P["head_in_z"], zt=z_beam + h)


FR = frame()

# --------------------------------------------------------------------------------------------------------------------
# O-ring glands, Parker O-Ring Handbook ORD 5700 (values in inches as tabulated; see README "O-ring glands" for the
# table numbers and what was read). AS568 sizes: ID x W, inches.
# --------------------------------------------------------------------------------------------------------------------
AS568 = {"-031": (1.739, 0.070), "-030": (1.614, 0.070), "-112": (0.487, 0.103), "-140": (2.237, 0.103)}
# Parker O-Ring Handbook ORD 5700 (2018), read from the PDF 2026-11-27 (see README "O-ring glands"):
GLANDS = dict(
    # Design Table 5-2 (p. 5-32), 2-112 on a 0.499 +0/-0.002 rod: throat .501 +.001/-0, groove dia A-1 .675 +.002/-0,
    # width G .140 +.005/-0; Design Chart 5-2-a: gland depth L .088-.090, squeeze .010-.018 (10-17 %), R .005-.015
    rod=dict(oring="-112", A1=(0.675, 0.677), G=(0.140, 0.145), L=(0.088, 0.090), R=(0.005, 0.015), rod_B=(0.497, 0.499)),
    # Design Chart 4-3 (p. 4-18), face seals: depth L and the width G for vacuum and gases (narrower than for liquids)
    face_070=dict(L=(0.050, 0.054), G=(0.084, 0.089)),
    face_103=dict(L=(0.074, 0.080), G=(0.120, 0.125)),
)
FACE_ID_FACTOR = 1.005    # external pressure (vacuum): groove ID = mean O-ring ID, tolerance +1 % (Chart 4-3 notes)


def mm(x):
    return x * IN


# --------------------------------------------------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, z1 - z0, V(x, y, z0))


def cylax(r, p0, d, length):
    return cq.Solid.makeCylinder(r, length, V(*p0), V(*d))


def ring(ro, ri, z0, z1, x=0.0, y=0.0):
    return cyl(ro, z0, z1, x, y).cut(cyl(ri, z0 - 1, z1 + 1, x, y))


def rbox(x0, x1, y0, y1, z0, z1, r):
    """box with vertical edges rounded to r"""
    w = cq.Workplane("XY").workplane(offset=z0).center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0)
    s = w.extrude(z1 - z0)
    if r > 0:
        s = s.edges("|Z").fillet(r)
    return s.val()


def slot_xy(x0, x1, y0, y1, z0, z1):
    """obround (full-round ends) in XY"""
    w, h = x1 - x0, y1 - y0
    wp = cq.Workplane("XY").workplane(offset=z0).center((x0 + x1) / 2, (y0 + y1) / 2)
    if w >= h:
        s = wp.slot2D(w, h, 0).extrude(z1 - z0)
    else:
        s = wp.slot2D(h, w, 90).extrude(z1 - z0)
    return s.val()


def polar(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


UNIT = {"-z": (0, 0, -1), "+z": (0, 0, 1), "-x": (-1, 0, 0), "+x": (1, 0, 0), "-y": (0, -1, 0), "+y": (0, 1, 0)}
# setup "up" = the part direction that faces the spindle. A hole drilled along direction d is cut in the setup whose up
# is -d (a hole drilled downward, "-z", is cut with the part's +Z up).
UP_OF = {"-z": "+Z", "+z": "-Z", "-x": "+X", "+x": "-X", "-y": "+Y", "+y": "-Y"}
# rows: setup x, y, z expressed in part coordinates (freecad_cam.py's convention)
ROT = {"+Z": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "-Z": ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
       "+X": ((0, 1, 0), (0, 0, 1), (1, 0, 0)), "-X": ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
       "+Y": ((1, 0, 0), (0, 0, -1), (0, 1, 0)), "-Y": ((-1, 0, 0), (0, 0, -1), (0, -1, 0))}


def to_setup(up, p):
    r = ROT[up]
    return tuple(sum(r[i][k] * p[k] for k in range(3)) for i in range(3))


# --------------------------------------------------------------------------------------------------------------------
# the piece record
# --------------------------------------------------------------------------------------------------------------------
class Piece:
    def __init__(self, pid, mk, name, *, material, qty, route, state, stock, stock_pn="", blank=None, seal=False,
                 pos=""):
        self.pid, self.mk, self.name = pid, mk, name
        self.material, self.qty, self.route, self.state = material, qty, route, state
        self.stock, self.stock_pn, self.blank, self.seal, self.pos = stock, stock_pn, blank, seal, pos
        self.solid = None           # finished piece, part frame
        self.pre = None             # what the mill setups start from if not the blank (turned piece, bought plate)
        self.cam_solid = None       # the piece without the features cut by hand after milling (CAM model, sim target)
        self.lathe_fill = None      # material the mill leaves for the lathe (sim target = solid + this)
        self.features = []          # CAM features
        self.holes = []             # hole table rows
        self.setups = []            # mill setups
        self.lathe = []             # lathe operations (time estimate)
        self.manual = []            # other shop steps: (what, minutes)
        self.tol, self.notes, self.changes = [], [], []
        self.finish = "6061: deburr, break edges 0.2-0.5 x 45 deg; as machined, Ra 3.2 um unless stated"
        self.sheet = None           # sheet-metal flat pattern record
        self.buy = None

    # --- cutting with records -----------------------------------------------------------------------------------
    def cut(self, s):
        self.solid = self.solid.cut(s)

    def hole(self, hid, kind, size, pts, axis="-z", depth=None, through=False, thread=None, note="", tool=None,
             tip=True):
        """kind: tap | clear | cbore | csk | plain | ream | press. pts: hole mouths (x, y, z) in the part frame.
        depth: full-diameter depth (blind). Draws the drilled hole (tapped holes at the tap drill) with a 118 deg
        point on blind holes, plus the counterbore or countersink."""
        d = dict(tap=T.TAP_DRILL.get(size), clear=T.CLEAR.get(size), cbore=T.CLEAR.get(size), csk=T.CLEAR.get(size))
        dd = d.get(kind) if kind in d else float(size)
        if dd is None:
            dd = float(size)
        if tool is None:
            tool = T.drill_tool(dd)
        u = UNIT[axis]
        L = depth if not through else 0.0
        for (x, y, z) in pts:
            if through:
                # through: long enough to leave the part (cut 200 mm), no point
                c = cylax(dd / 2, (x - u[0] * 1.0, y - u[1] * 1.0, z - u[2] * 1.0), u, 300.0)
            else:
                c = cylax(dd / 2, (x - u[0] * 0.01, y - u[1] * 0.01, z - u[2] * 0.01), u, L + 0.01)
                if tip:
                    tipl = dd / 2 / math.tan(math.radians(59.0))
                    c = c.fuse(cq.Solid.makeCone(dd / 2, 0.0, tipl, V(x + u[0] * L, y + u[1] * L, z + u[2] * L), V(*u)))
            self.cut(c)
            if kind == "cbore":
                cd, ch = T.CBORE[size]
                self.cut(cylax(cd / 2, (x - u[0], y - u[1], z - u[2]), u, ch + 1.0))
            if kind == "csk":
                cd = T.CSK[size]
                self.cut(cq.Solid.makeCone(cd / 2 + 1.0, 0.0, cd / 2 + 1.0, V(x - u[0], y - u[1], z - u[2]), V(*u)))
        f = dict(kind="drill", hid=hid, axis=axis, d=dd, tool=tool, pts=[list(p) for p in pts], depth=L, through=through,
                 size=size, hole_kind=kind)
        self.features.append(f)
        if kind == "cbore":
            cd, ch = T.CBORE[size]
            self.features.append(dict(kind="cbore", hid=hid, axis=axis, d=cd, depth=ch, tool=4,
                                      pts=[list(p) for p in pts], hole_d=dd))
        if kind == "csk":
            self.features.append(dict(kind="csk", hid=hid, axis=axis, d=T.CSK[size], tool=7, pts=[list(p) for p in pts]))
        call = {"tap": "%s x %s deep thread, tap drill %.2f x %s" % (size, thread or "-", dd,
                                                                    "through" if through else "%.1f" % L),
                "clear": "%.1f %s clearance %s" % (dd, size, "through" if through else "x %.1f" % L),
                "cbore": "%.1f through, c'bore %.1f x %.1f (%s SHCS)" % (dd, T.CBORE[size][0], T.CBORE[size][1], size)
                if kind == "cbore" else "",
                "csk": "%.1f through, c'sink 90 deg to %.1f (%s flat head)" % (dd, T.CSK.get(size, 0), size)
                if kind == "csk" else "",
                }.get(kind) or ("%.2f %s %s" % (dd, kind, "through" if through else "x %.1f" % L))
        self.holes.append(dict(id=hid, n=len(pts), kind=kind, size=size, callout=call + ((" - " + note) if note else ""),
                               axis=axis, pts=[[round(c, 2) for c in p] for p in pts]))

    def pocket(self, name, solid, probe, axis="-z", tool=3, kind="pocket", note="", z_top=None):
        """cut a pocket, groove or step (solid) and record it: probe = a point on its floor (part frame); z_top = the
        coordinate (along the axis) where the pocket starts, if not the part's face"""
        self.cut(solid)
        self.features.append(dict(kind=kind, name=name, axis=axis, tool=tool, probe=list(probe), note=note,
                                  z_top=z_top))

    def boss(self, name, probe, z_base, axis="-z", tool=2):
        """material round a boss that stands up from a face: Adaptive outside the boss's top face (probe = a point on
        it, part frame) down to z_base (the face round it, along the axis). The piece solid already has the boss."""
        self.features.append(dict(kind="boss", name=name, axis=axis, tool=tool, probe=list(probe), z_base=z_base))

    def opening(self, name, solid, probe, z_exit, axis="-z", tool=3):
        """a through opening (non-round): profiled round its inside. probe = a point on the entry face next to it;
        z_exit = the coordinate along the axis where it leaves the part (part frame)"""
        self.cut(solid)
        self.features.append(dict(kind="opening", name=name, axis=axis, tool=tool, probe=list(probe), z_exit=z_exit))

    def bore(self, name, r, x, y, z_top, z_bot, axis="-z", tool=2, finish=None):
        """round bore over 10 mm: helix-milled (finish by boring head where noted)"""
        u = UNIT[axis]
        if axis in ("-z", "+z"):
            self.cut(cyl(r, min(z_top, z_bot) - 0.01, max(z_top, z_bot) + 0.01, x, y))
        else:
            raise NotImplementedError
        self.features.append(dict(kind="bore", name=name, axis=axis, tool=tool, r=r, xy=[x, y], z_top=z_top,
                                  z_bot=z_bot, finish=finish))

    def setup(self, up, *, face=None, outline=None, label="", hold="", stock_note="", repeat=1):
        """face: (tool, z_to) in the setup frame; outline: (tool, z_to) adaptive outside of the setup's top face;
        repeat: the same program run this many times (an indexed feature)"""
        n = "ABCDEFG"[len(self.setups)]
        self.setups.append(dict(name="%s_%s" % (self.pid, n), up=up, face=face, outline=outline, label=label,
                                hold=hold, stock_note=stock_note, repeat=repeat))

    def lathe_op(self, what, minutes):
        self.lathe.append((what, round(minutes, 2)))

    # --- summary ------------------------------------------------------------------------------------------------
    def n_holes(self):
        return sum(h["n"] for h in self.holes)

    def record(self):
        bb = self.solid.BoundingBox() if self.solid is not None else None
        return dict(pid=self.pid, mk=self.mk, name=self.name, material=self.material, qty=self.qty, route=self.route,
                    state=self.state, stock=self.stock, stock_pn=self.stock_pn, blank=self.blank, seal=self.seal,
                    pos=self.pos, bbox=[round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]
                    if bb else None, volume_cm3=round(self.solid.Volume() / 1000, 2) if self.solid is not None else None,
                    features=self.features, holes=self.holes, setups=self.setups, lathe=self.lathe,
                    manual=self.manual, tol=self.tol, notes=self.notes, changes=self.changes, finish=self.finish,
                    sheet=self.sheet, buy=self.buy, n_holes=self.n_holes())


def raster_gcode(region, z_top, z_floor, tool, step=0.6, stepover=0.4):
    """zig-zag raster and a finishing contour for an open pocket (FreeCAD 1.0.2's Pocket, Adaptive and MillFace do not
    clear a floor face that is open to the side): region = shapely polygon of the pocket in the setup's XY; the tool
    centre stays inside region eroded by its radius. Returns G-code lines in the setup frame (tool already loaded)."""
    import shapely
    from shapely.geometry import LineString
    d = T.TOOLS[tool]["d"]
    f = T.feed_mm_min(tool)
    core = region.buffer(-d / 2 - 0.02)
    lines = []
    zs = []
    z = z_top
    while z > z_floor + 1e-6:
        z = max(z - step, z_floor)
        zs.append(z)
    minx, miny, maxx, maxy = core.bounds
    for z in zs:
        y = miny
        k = 0
        while y <= maxy + 1e-9:
            seg = core.intersection(LineString([(minx - 1, y), (maxx + 1, y)]))
            parts = [g for g in getattr(seg, "geoms", [seg]) if not g.is_empty and g.length > 0]
            for g in sorted(parts, key=lambda g: g.coords[0][0], reverse=bool(k % 2)):
                c = list(g.coords) if k % 2 == 0 else list(g.coords)[::-1]
                lines += ["G0 Z%.3f" % (z_top + 2.0), "G0 X%.3f Y%.3f" % c[0], "G1 Z%.3f F%.1f" % (z, f / 2),
                          "G1 X%.3f Y%.3f F%.1f" % (c[-1][0], c[-1][1], f)]
            y += stepover * d
            k += 1
        for ring in [core.exterior] + list(core.interiors):
            c = list(ring.coords)
            lines += ["G0 Z%.3f" % (z_top + 2.0), "G0 X%.3f Y%.3f" % c[0], "G1 Z%.3f F%.1f" % (z, f / 2)]
            lines += ["G1 X%.3f Y%.3f F%.1f" % (x, y_, f) for x, y_ in c[1:]]
    lines.append("G0 Z%.3f" % (z_top + 5.0))
    return lines


def groove_gcode(p0, p1, w, z_top, z_floor, tool, step=0.5):
    """a straight slot of width w from p0 to p1 (setup XY), cut with a smaller end mill in two offset passes per
    step-down; G-code lines in the setup frame (tool loaded)"""
    d = T.TOOLS[tool]["d"]
    f = T.feed_mm_min(tool)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    off = max(0.0, (w - d) / 2 - 0.02)
    lines, z = [], z_top
    while z > z_floor + 1e-6:
        z = max(z - step, z_floor)
        for k, o in enumerate((-off, off) if off > 0 else (0.0,)):
            a = (p0[0] + nx * o, p0[1] + ny * o)
            b = (p1[0] + nx * o, p1[1] + ny * o)
            if k % 2:
                a, b = b, a
            lines += ["G0 Z%.3f" % (z_top + 2.0), "G0 X%.3f Y%.3f" % a, "G1 Z%.3f F%.1f" % (z, f / 2),
                      "G1 X%.3f Y%.3f F%.1f" % (b[0], b[1], f)]
    lines.append("G0 Z%.3f" % (z_top + 5.0))
    return lines


def blank_box(x0, x1, y0, y1, z0, z1):
    return dict(type="box", box=[x0, x1, y0, y1, z0, z1])


def blank_cyl(r, z0, z1):
    return dict(type="cyl", r=r, z=[z0, z1])


def blank_solid(b):
    if b["type"] == "box":
        return box(*b["box"])
    return cyl(b["r"], *b["z"])


# --------------------------------------------------------------------------------------------------------------------
# lathe time estimate (this folder's estimate: feeds and lengths, conservative manual-lathe numbers for 6061)
# --------------------------------------------------------------------------------------------------------------------
def turn_min(d_from, d_to, length, rpm=None, f=0.15, doc=1.5, v=150.0):
    """minutes to turn (or bore) a diameter from d_from to d_to over length: radial passes of doc, feed f mm/rev,
    surface speed v m/min at the larger diameter, +20 % for approach and retract"""
    passes = max(1, math.ceil(abs(d_from - d_to) / 2 / doc))
    rpm = rpm or min(2500.0, 1000 * v / (math.pi * max(d_from, d_to)))
    return 1.2 * passes * length / (f * rpm)


def face_min(d_out, d_in=0.0, passes=1, f=0.12, v=150.0):
    rpm = min(2500.0, 1000 * v / (math.pi * d_out))
    return 1.2 * passes * (d_out - d_in) / 2 / (f * rpm)


def drill_min(d, depth, f=None, v=60.0):
    f = f or min(0.15, 0.025 * d)
    rpm = min(2500.0, 1000 * v / (math.pi * d))
    return 1.5 * depth / (f * rpm)          # x1.5 for pecking


def part_min(d, f=0.04, v=100.0):
    rpm = min(2000.0, 1000 * v / (math.pi * d))
    return 1.3 * d / 2 / (f * rpm)


# ====================================================================================================================
# MK-01 deck plate
# ====================================================================================================================
def lsm_base_taps():
    """M3 taps in the deck under the X-LSM100B's base slots (ft_vendor.LSM base_slots: 3.6 wide, 2.75 long, every 20 mm
    at y +-10): eight of the sixteen, at the slots' centres"""
    import ft_vendor as VEN
    pts = []
    for k in (0, 2, 5, 7):
        x = P["rc_x0"] + (9.5 + 20 * k - 78.8) + 1.375
        pts += [(x, P["rc_y"] + sy) for sy in (-10.0, 10.0)]
    assert len(VEN.LSM["base_slots"]) == 16
    return pts


SHIELD_FOOT_X = (-60.0, 10.0, 80.0)         # MK-12's foot screws into the deck (fab), at y = rc_y - 31


def mk01():
    t = P["deck_t"]
    x0, x1 = XC - P["deck"][0] / 2, XC + P["deck"][0] / 2
    y0, y1 = YC - P["deck"][1] / 2, YC + P["deck"][1] / 2
    pc = Piece("MK-01", "MK-01", "Deck plate", material="6061-T651", qty=1, route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate (12.7 +0/+0.69), 255 x 255 cut from a 12 x 24 in. sheet; faced to 10.0",
               stock_pn="McMaster 89155K135 (1/2 x 12 x 24 in., $148.74 read 2026-11-17 in PR 266's mcmaster-parts.csv)",
               blank=blank_box(x0 - 5, x1 + 5, y0 - 5, y1 + 5, -1.35, 11.35),
               pos="part (x, y) = world (x, y); part z 0 = the deck's underside (world z -62.7 in the box)")
    pc.solid = rbox(x0, x1, y0, y1, 0, t, 3.0)
    pc.bore("rod hole", 10.0, 0, 0, t, 0, tool=3)
    # overflow cut-out (model: x 20..62, y +-26 through): R4 corners for a 1/4 in. cutter
    pc.opening("overflow-cup cut-out", rbox(P["ovf_x"][0] - 2, 62, -26, 26, -1, t + 1, 4.0), (40.0, 30.0, t), 0.0,
               tool=3)
    so = P["so_xy"]
    pc.hole("A", "cbore", "M3", [(sx, sy, 0.0) for sx in (-so, so) for sy in (-so, so)], axis="+z", through=True,
            note="well-block standoffs: M3 x 35 SHCS up through the Macor standoff")
    g = P["gland_screw"]
    pc.hole("B", "tap", "M5", [(sx, sy, t) for sx in (-g, g) for sy in (-g, g)], through=True, thread="through",
            note="rod-gland screws from below, inside the gland's face seal (box: through the floor; cube: through "
                 "MK-14). Through, not the model's 8 mm blind: the S1 target stand screws into them from above")
    pc.hole("C", "clear", "M6", [(XC + sx * 112.0, YC + sy * 92.1, t) for sx in (-1, 1) for sy in (-1, 1)],
            through=True, note="cube only: M6 x 16 down into MK-14's blind taps (the box holds the deck with MK-23)")
    pc.hole("D", "tap", "M3", [(x, y, t) for x, y in lsm_base_taps()], through=True, thread="through",
            note="X-LSM100B base: M3 screws down through its base slots (Zaber STEP, ft_vendor.LSM); 8 of the 16 slots")
    pc.hole("E", "tap", "M3", [(x, P["rc_y"] - 31.0, t) for x in SHIELD_FOOT_X], through=True, thread="through",
            note="stage-shield foot (MK-12)")
    pc.setup("-Z", face=(1, 1.35), label="bottom up: face, c'bores and drill every through hole",
             hold="plate in 6 in. vise jaws on the 255 mm blank's margins (or toe clamps), on parallels")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 10.0, rod hole, cut-out, outline through",
             hold="screwed to a sacrificial plate through holes A and B (8 screws), so the outline can go through")
    pc.tol += ["thickness 10.00 +-0.05; flatness 0.1 over the plate (it carries the stage and the well block)",
               "holes A, B, D located +-0.1 from the rod hole (datum)"]
    pc.changes += ["v2: 245 mm square (was 250); X-LSM100B base taps from Zaber's STEP (was the X-LSQ075B's estimate); "
                   "4 x M6 clearance for the cube's deck screws (was 4 x M5 c'bored corner holes); no deck-to-floor "
                   "screws in the box (MK-23 clamps the deck on the panel studs)",
                   "kept from v1: 4 M3 c'bored for the standoffs, gland taps at (+-%.1f, +-%.1f) (v2 took the fab's "
                   "pattern), 3 M3 for the shield foot, cut-out corners R4" % (g, g),
                   "gland taps through (model: 8 mm blind from below): the S1 target stand screws into them"]
    return pc


# ====================================================================================================================
# MK-02 window stack: window ring, retaining flange, inner clamp ring (box), cover-slide holder (base + cover)
# ====================================================================================================================
WR_H, WR_LIP = 12.0, 4.0          # window ring height and lip (model: 10 and 2)
BC_R = 42.0                        # the stack's 8 x M5 bolt circle
TIE_R = 40.0                       # beam-tube tie rods (4 x M4)


def win_groove():
    """face groove under the window for AS568-030 (ID 1.614 x 0.070), sized for vacuum (external pressure): groove ID
    = O-ring ID +0.5 % (Chart 4-3: + 1 %), vacuum width and depth from the 0.070 row"""
    oid, w = AS568["-030"]
    gid = mm(oid) * FACE_ID_FACTOR
    gw = mm(sum(GLANDS["face_070"]["G"]) / 2)
    gd = mm(sum(GLANDS["face_070"]["L"]) / 2)
    return gid / 2, gid / 2 + gw, gd


def base_groove():
    """bottom-face groove of the window ring for AS568-140 (2.237 x 0.103), vacuum sizing"""
    oid, w = AS568["-140"]
    gid = mm(oid) * FACE_ID_FACTOR
    return gid / 2, gid / 2 + mm(sum(GLANDS["face_103"]["G"]) / 2), mm(sum(GLANDS["face_103"]["L"]) / 2)


def mk02_ring():
    pc = Piece("MK-02a", "MK-02", "Window ring", material="6061-T651", qty=1, route="CNC mill", state="S2",
               stock="3/4 in. 6061-T651 plate, 106 x 106 square (faced to 12.0)",
               stock_pn="McMaster 89155K155 (3/4 x 12 x 24 in., $211.96 read 2026-11-22 in audit-prices.csv)",
               blank=blank_box(-53, 53, -53, 53, -3.5, 15.55), seal=True,
               pos="part z 0 = ring underside = box lid top (world z 143.4) or cube top plate top (270.8)")
    pc.solid = cyl(50.0, 0, WR_H)
    pc.bore("beam aperture", 19.0, 0, 0, WR_H, 0, tool=2)
    pc.pocket("window seat bore", cyl(P["window_d"] / 2 + 0.25, WR_LIP, WR_H + 1), (24.0, 0.0, WR_LIP), tool=3,
              kind="pocket")
    r0, r1, gd = win_groove()
    pc.pocket("window O-ring groove (AS568-030)", ring(r1, r0, WR_LIP - gd, WR_LIP + 0.1), ((r0 + r1) / 2, 0, WR_LIP - gd),
              tool=5, kind="groove", z_top=WR_LIP)
    b0, b1, bd = base_groove()
    pc.pocket("base O-ring groove (AS568-140)", ring(b1, b0, -0.1, bd), ((b0 + b1) / 2, 0, bd), axis="+z", tool=5,
              kind="groove")
    pc.hole("A", "clear", "M5", [(*polar(BC_R, 45 * k), WR_H) for k in range(8)], through=True,
            note="8 x M5 flat-head through flange, ring and lid into MK-02c (box) or MK-13 (cube)")
    pc.setup("-Z", face=(2, 3.5 - 0.0), outline=(2, -6.0), label="bottom up: face, base O-ring groove, outline half")
    pc.setup("+Z", face=(2, WR_H), outline=(2, -0.3), label="top up: face to 12.0, aperture, seat, window groove, "
                                                              "holes, rest of the outline", hold="soft jaws on the OD")
    pc.tol += ["window seat floor (z 4): flatness 0.01, Ra 0.4 um (Parker Chart 4-3: 16 RMS for gas and vacuum face seals)",
               "base face (z 0): flatness 0.02, Ra 0.4 um (16 RMS), lay circular", "seat bore 51.30 +0.10/0",
               "O-ring grooves: floor Ra 0.8 um (32 RMS), sides Ra 1.6; floor corner radius 0.13-0.38 (.005-.015 in.)"]
    pc.changes += ["height 10 -> 12 and the lip 2 -> 4 mm: a 2 mm lip cannot carry a 1.32 mm deep O-ring groove",
                   "aperture 44 -> 38 mm so the window groove fits inside the 51.3 seat (the scanned beam at the window "
                   "is 26.8 mm across in the box, 16.8 mm in the cube: 5.6 mm margin)",
                   "added: window face groove (AS568-030) and base face groove (AS568-140), both sized for vacuum",
                   "added: 8 x M5 holes on a 84 mm circle (one bolt circle clamps flange, window, ring and lid)"]
    return pc


SPIG_R, SPIG_H = P["tube_spigot"]            # the beam tube's locating spigots: outer radius 26.5, 3 tall (v2)
SPIG_W = 1.5                                  # spigot wall (ft_model: tube(sp_r, sp_r - 1.5, ...))


def mk02_flange():
    t = 6.0
    sx, sy = TXB - WX, TYB - WY                  # spigot centre = the tube's centre, relative to the window: (0, -6)
    pc = Piece("MK-02b", "MK-02", "Window retaining flange (beam-tube spigot on top)", material="6061-T651", qty=1,
               route="CNC mill", state="S2", stock="3/8 in. 6061 plate (9.53) faced to 9.0, 106 x 106",
               stock_pn="3/8 in. 6061-T651 plate (PN not read)", blank=blank_box(-53, 53, -53, 53, -0.265, 9.265),
               pos="part z 0 = flange underside = ring top (world z 162.0 box / 282.8 cube); the spigot at part "
                   "(%.0f, %.0f) is the beam tube's centre" % (sx, sy))
    sp = ring(SPIG_R, SPIG_R - SPIG_W, t - 0.01, t + SPIG_H, sx, sy)
    pc.solid = cyl(50.0, 0, t).fuse(sp).clean()
    # aperture 38: the spigot's bore comes within 19 mm of the window centre on its +y side, so a 44 aperture would cut
    # it; the scanned beam at the flange is 26.2 across, within 14.8 of the window centre (beam_centre, beam_radius)
    pc.bore("beam aperture 37.6 (from the spigot top)", 18.8, 0, 0, t + SPIG_H, 0, tool=2)
    pc.pocket("window recess (2.2 deep: window + 0.8 mm FKM cushion ring)", cyl(P["window_d"] / 2 + 0.25, -1, 2.2),
              (24.0, 0, 2.2), axis="+z", tool=3)
    pc.boss("beam-tube spigot %.0f x %.1f wall x %.0f tall, centred on the tube (round it: down to the face)"
            % (2 * SPIG_R, SPIG_W, SPIG_H), (sx + SPIG_R - SPIG_W / 2, sy, t + SPIG_H), t, tool=2)
    pc.features.append(dict(kind="pocket", name="inside the spigot, outside the aperture (crescent, down to the face)",
                            axis="-z", tool=3, probe=[sx, sy - SPIG_R + SPIG_W + 1.2, t], note="", z_top=None))
    pc.hole("A", "csk", "M5", [(*polar(BC_R, 45 * k), t) for k in range(8)], through=True,
            note="M5 x 25 (box) / M5 x 20 (cube) flat-head ISO 10642, flush")
    pc.setup("-Z", face=(2, 0.265), label="bottom up: face, window recess")
    pc.setup("+Z", face=(2, t + SPIG_H), outline=(2, -0.3), label="top up: face the spigot top, cut round the spigot "
             "to 6.0, inside it, aperture, c'sinks, outline")
    pc.tol += ["recess depth 2.20 +0.05/0 (sets the cushion's squeeze)",
               "spigot OD %.2f -0.10/0 (the tube's bore is 54): the half-shells slide off it sideways" % (2 * SPIG_R)]
    pc.changes += ["v2: the beam tube's centre section is two half-shells that slide off sideways, so the flange carries "
                   "a %.0f mm spigot inside the tube's bore (ft_model) in place of v1's 60.5 socket and 4 M4 tie rods"
                   % (2 * SPIG_R),
                   "the spigot is centred on the tube, (%.0f, %.0f) from the window in the box; in the cube the model "
                   "puts it (0, -3) from the window. One flange can't do both: made for the box (FT-1); for FT-1V move "
                   "the cube's tube centre to (0, -27) in ft_model, or make a second flange" % (sx, sy),
                   "aperture 44 -> 38 (the window ring's is 38 too): the spigot's bore passes 19 mm from the window "
                   "centre on its +y side",
                   "kept from v1: recess 2.2 mm deep, 8 x M5 countersinks on the 84 mm circle (the model's 6 x M4 flat "
                   "heads at r 40 would have to pass the fab's 8-screw stack)"]
    return pc


def mk02_clamp():
    pc = Piece("MK-02c", "MK-02", "Inner clamp ring (box lid only)", material="6061-T651", qty=1, route="CNC mill",
               state="S2", stock="1/4 in. 6061 plate (6.35) faced to 6.0 on top, 106 x 106",
               stock_pn="1/4 in. 6061 plate (PN not read)", blank=blank_box(-53, 53, -53, 53, 0.0, 6.35),
               pos="part z 0 = underside (world z 135.5), top against the lid sheet")
    t = 6.0
    pc.solid = cyl(50.0, 0, t)
    pc.bore("aperture", 22.0, 0, 0, t, 0, tool=2)
    pc.hole("A", "tap", "M5", [(*polar(BC_R, 45 * k), t) for k in range(8)], through=True, thread="through (6)",
            note="the window stack's screws")
    pc.hole("B", "tap", "M4", [(*polar(30.0, a), t) for a in (90, 180, 270)], through=True,
            thread="through", note="cover-slide holder")
    pc.setup("+Z", face=(2, t), outline=(2, -0.3), label="top up: face, aperture, holes, outline")
    pc.changes += ["added: 8 x M5 tapped (the stack's screws), 3 x M4 tapped for the cover-slide holder"]
    return pc


def mk02_holder():
    """cover-slide holder split at the slide plane so the slide pocket is a 1.2 mm 2.5D pocket"""
    out = []
    pcb = Piece("MK-02d", "MK-02", "Cover-slide holder, base (slide pocket)", material="6061-T651", qty=1,
                route="CNC mill", state="S2", stock="1/4 in. 6061 plate faced to 5.6, 76 x 76",
                stock_pn="1/4 in. 6061 plate (PN not read)", blank=blank_box(-38, 38, -38, 38, 0.0, 6.35),
                pos="part z 5.6 = slide plane; z 0 = holder bottom (world 124.5 box)")
    h = 5.6
    pcb.solid = cyl(35.0, 0, h)
    pcb.bore("aperture", P["cs_id"] / 2, 0, 0, h, 0, tool=2)
    sl = cyl(25.3, h - 1.2, h + 1).fuse(box(0, 40, -25.3, 25.3, h - 1.2, h + 1))
    pcb.cut(sl)
    from shapely.geometry import Point, box as sbox
    # the 1/4 in. cutter (T3) is wider than the 5.3 mm ring between the aperture (r 20) and the pocket wall (r 25.3),
    # so the region keeps only r < 16.8 out: the tool centre runs at r 20.0-22.1 and its edge overhangs the aperture,
    # which is already cut through. (An exclusion at r 19 left no room for the cutter on the -x side, and the voxel
    # check found the back half of the pocket uncut.)
    reg = Point(0, 0).buffer(25.3, 256).union(sbox(0, -25.3, 40.0, 25.3)).difference(Point(0, 0).buffer(16.8, 256))
    pcb.features.append(dict(kind="custom_gcode", name="slide pocket 50.6 x 1.2 deep, open to +x (raster)", axis="-z",
                             tool=3, late=True, gcode=raster_gcode(reg, h, h - 1.2, 3)))
    pcb.hole("A", "clear", "M4", [(*polar(30.0, a), h) for a in (90, 180, 270)], through=True)
    pcb.setup("+Z", face=(2, h), outline=(2, -0.3), label="top up: face, aperture, slide pocket, holes, outline")
    pcb.tol += ["slide pocket depth 1.20 +0.10/0 for a 1.0 mm cover slide"]
    pcb.changes += ["the model's one-piece holder had a 1.2 mm undercut slot; split at the slide plane into a base "
                    "with an open 2.5D pocket and a plain cover, held by the same 3 x M4 screws",
                    "v2: opening 40 -> %.0f (ft_model cs_id); OD 70 and the pocket as v1" % P["cs_id"]]
    zs = P["cs_z"]                                         # slide's lower face above the bed (box)
    hc = round((L_BOX["roof_in"] - 6.0) - (zs + 1.1), 2)    # from the base's top to the clamp ring (ft_model cs_top)
    pcc = Piece("MK-02e", "MK-02", "Cover-slide holder, cover (%.1f tall)" % hc, material="6061-T651", qty=1,
                route="CNC mill", state="S2", stock="1/2 in. 6061 plate faced to %.1f, 76 x 76" % hc,
                stock_pn="1/2 in. 6061 plate (PN not read)",
                blank=blank_box(-38, 38, -38, 38, 0.0, 12.7), pos="part z 0 = the base's top (stacks on the base)")
    pcc.solid = cyl(35.0, 0, hc)
    pcc.bore("aperture", P["cs_id"] / 2, 0, 0, hc, 0, tool=2)
    pcc.hole("A", "clear", "M4", [(*polar(30.0, a), hc) for a in (90, 180, 270)], through=True,
             note="M4 x 20 into MK-02c (box) or the drop tube MK-02f (cube)")
    pcc.setup("+Z", face=(2, hc), outline=(2, -0.3), label="top up: face, aperture, holes, outline")
    pcc.changes += ["v2: the holder hangs from the clamp ring with no gap (ft_model cs_top = the ring's underside), so "
                    "the cover is %.1f tall (v1 4.4); opening %.0f" % (hc, P["cs_id"]),
                    "in the cube ft_model hangs the holder 2.1 mm lower under the drop tube (MK-02f): the drop tube is "
                    "made 2.1 mm shorter so this holder serves both"]
    return [pcb, pcc]


# ====================================================================================================================
# MK-03 well block (+ Macor standoffs)
# ====================================================================================================================
def mk03():
    bw, bd, bh = P["well"]
    pc = Piece("MK-03", "MK-03", "Well block, 40.00 H7 bore", material="6061-T6511", qty=1, route="CNC mill",
               state="FT-0", stock="6061 bar 1-3/4 x 3-1/2 in. (44.45 x 88.9) sawn 84 long",
               stock_pn="6061 rectangular bar 1-3/4 x 3-1/2 in. (PN not read)",
               blank=blank_box(-42, 42, -44.45, 44.45, -2.2, 42.25), seal=False,
               pos="part (x, y) = world (x, y); part z 0 = block underside (world z -40 box, -19 cube)")
    pc.solid = box(-bw / 2, bw / 2, -bd / 2, bd / 2, 0, bh)
    pc.bore("40.00 H7 bore (rough 39.6 by helix; finish with a boring head)", P["bore"] / 2, 0, 0, bh, 0, tool=2,
            finish="boring head to 40.000-40.025, Ra 0.8")
    x0, x1 = P["ovf_x"]
    oy = P["ovf_y"]
    sl = slot_xy(x0, x1, -oy, oy, -1, bh + 1)
    pc.opening("overflow slot 7 x 44 (top half)", sl, (x1 + 3.0, 0, bh), bh / 2 - 0.5, tool=3)
    pc.features.append(dict(kind="opening", name="overflow slot (bottom half)", axis="+z", tool=3,
                            probe=[x1 + 3.0, 0, 0.0], z_exit=bh / 2 + 0.5))
    hd, hdep = P["heater_hole"]
    pc.hole("A", "plain", "%.1f" % hd, [(-bw / 2, sy, bh / 2) for sy in P["blk_heaters"]], axis="+x", depth=hdep,
            note="block heaters, %g x %g mm cartridges (24 V 50 W): drill %.1f x %g" % (P["heater_d"], P["heater_l"], hd,
                                                                                      hdep))
    pc.hole("B", "plain", "2.0", [(-bw / 2, 0.0, bh - 8.0)], axis="+x", depth=15.0,
            note="block thermocouple, 1/16 in. sheath, 8 mm under the top, between the heaters (model: 1.6)")
    so = P["so_xy"]
    pc.hole("C", "tap", "M3", [(sx, sy, 0.0) for sx in (-so, so) for sy in (-so, so)], axis="+z", depth=8.0,
            thread="6", note="Macor standoffs (screws from under the deck)")
    pc.hole("D", "tap", "M3", [(sx, -33.5, bh) for sx in (-27.0, 27.0)], depth=8.0, thread="6", note="slot nozzle")
    pc.hole("E", "tap", "M3", [(sx, 33.5, bh) for sx in (-29.5, 29.5)], depth=8.0, thread="6",
            note="exhaust collector")
    pc.setup("+Z", face=(2, bh), outline=(2, bh / 2 - 1.0), label="top up: face, outline to mid-height, bore, "
                                                                      "slot half, top holes")
    pc.setup("-Z", face=(2, 0.0), outline=(2, -(bh / 2 + 1.0)), label="bottom up: face to 40.00, outline, slot half, "
                                                                       "standoff taps")
    pc.setup("-X", label="-X face up: four heater holes and the thermocouple hole", hold="vise on the faced Y faces")
    pc.tol += ["bore 40.000 +0.025/0 (H7), cylindricity 0.01, Ra 0.8 um; perpendicular to the top face within 0.02",
               "top face (powder plane): flatness 0.02, Ra 0.8; height 40.00 +-0.02; bore edge sharp (0.1 max)",
               "heater holes 6.10 +0.05/0: a 6 mm cartridge heater wants 0.05-0.1 mm diametral clearance"]
    pc.changes += ["v2: four 6.1 x 21 heater holes from the -x face at y -30, -15, 15, 30 (v1: two 6.40 x 40); the "
                   "thermocouple hole comes from -x too, 8 mm under the top at y 0 (v1: from +y), so the +Y setup goes "
                   "(3 setups, v1 4); it clears the heaters by 11 mm in y and 8 mm in z, and the bore by 5 mm",
                   "thermocouple hole 2.0 for the 1/16 in. (1.59) sheath (model 1.6: a press fit)",
                   "overflow slot drawn with full-round ends (R3.5): cut from both faces with a long 1/4 in. cutter",
                   "added: 4 M3 for the standoffs, 2 M3 for the nozzle, 2 M3 for the collector"]
    mac = Piece("MK-03s", "MK-03", "Macor standoffs (4)", material="Macor (from H4's 5/16 in. rod)", qty=4,
                route="lathe (carbide, slow) or diamond saw + drill", state="FT-0",
                stock="McMaster 8489K75 Macor rod, 5/16 in. x 6 in. (parts.csv H4)", stock_pn="McMaster 8489K75",
                blank=blank_cyl(mm(5 / 16) / 2, -0.5, 13.2))
    mac.solid = ring(mm(5 / 16) / 2, T.CLEAR["M3"] / 2, 0, P["so_l"])
    mac.lathe_op("part off at 13.2 (slow feed, carbide; Macor dust: wet), each", 3.0)
    mac.lathe_op("face both ends to 12.70 +-0.02, each", 2.5)
    mac.lathe_op("drill 3.4 through (carbide, 0.02 mm/rev, pecking), each", 2.5)
    mac.tol += ["length 12.70 +-0.02 (four alike within 0.01, so the block sits level)"]
    mac.changes += ["ft_model draws Ø6.35 (so_d); the H4 rod is 5/16 in. (7.94): set so_d = 7.94 or turn them down",
                    "drilled 3.4 for an M3 304 screw from under the deck. The four screws add ~3 W of conduction at "
                    "200 C (estimate: 304, 7 mm2, 23 mm path); titanium M3 screws would cut that to ~1.2 W"]
    mac.finish = "as cut; no chips left in the bore"
    return [pc, mac]


# ====================================================================================================================
# MK-04 heater plate, MK-05 substrates
# ====================================================================================================================
SOCKET_D = 12.95


def mk04():
    D, H = P["plate_d"], P["hp_t"]
    hd, hdep = P["heater_hole"]
    gw, gd = P["lead_groove"]
    pc = Piece("MK-04", "MK-04", "Heater plate", material="6061-T6511", qty=1, route="lathe + CNC mill", state="FT-0",
               stock="6061 round bar 1-3/4 in. (44.45) sawn 30 long",
               stock_pn="McMaster 1610T family (6061 rod, length chosen on the page; 1610T27 is the 3-1/4 in. size "
                        "in plate-materials.csv); 1-3/4 in. suffix not read",
               blank=blank_cyl(mm(1.75) / 2, -3.0, H + 3.0),
               pos="part z 0 = plate underside (world z -30 at the start of a build, box)")
    turned = cyl(D / 2, 0, H)
    rz0 = H - 7.0
    turned = turned.cut(ring(D / 2 + 1, D / 2 - P["rope"], rz0, rz0 + P["rope"]))
    turned = turned.cut(cyl(SOCKET_D / 2, -0.1, P["socket"]))
    turned = turned.cut(cq.Solid.makeCone(SOCKET_D / 2, 0, SOCKET_D / 2 / math.tan(math.radians(59)),
                                          V(0, 0, P["socket"]), V(0, 0, 1)))
    pc.solid = turned
    pc.pre = turned
    r = P["heater_r"]
    pc.hole("A", "plain", "%.1f" % hd, [(*polar(r, a), 0.0) for a in (30.0, 150.0)], axis="+z", depth=hdep,
            note="plate heaters, %g x %g mm cartridges, leads out of the bottom into the grooves" % (P["heater_d"],
                                                                                                  P["heater_l"]))
    pc.hole("B", "plain", "2.0", [(*polar(r, 270.0), 0.0)], axis="+z", depth=hdep,
            note="plate thermocouple, 1/16 in. sheath (model 1.6; 10 x D: parabolic drill)")
    # lead grooves in the underside, each hole to the socket (ft_model lead_groove): cut after the holes, in the bottom-up
    # setup (setup frame = (x, -y, -z)); the 2 mm cutter in two passes for the 3 mm width
    for k, a in enumerate((30.0, 150.0, 270.0)):
        p0 = polar(SOCKET_D / 2 - 1.0, a)
        p1 = polar(r, a)
        g = box(SOCKET_D / 2 - 1.5, r, -gw / 2, gw / 2, -1, gd)
        pc.cut(g.rotate(V(0, 0, 0), V(0, 0, 1), a))
        pc.features.append(dict(kind="custom_gcode", name="lead groove %d, %.0f x %.1f deep, socket to the %s hole"
                                % (k + 1, gw, gd, "heater" if k < 2 else "thermocouple"), axis="+z", tool=5, late=True,
                                gcode=groove_gcode((p0[0], -p0[1]), (p1[0], -p1[1]), gw, 0.0, -gd, 5)))
    pc.hole("C", "tap", "M2", [(*polar(17.1, 90 + 120 * k), H) for k in range(3)], depth=3.5, thread="3.0",
            note="substrate screws; 0.5 mm above the rope groove: do not deepen")
    pc.hole("D", "tap", "M3", [(D / 2, 0.0, 5.0)], axis="-x", depth=13.0, thread="9 (set screw M3 x 8 dog point, sunk "
                                                                                    "1 mm below the OD)",
            note="holds the rod: the dog point enters a 2.5 hole in the rod")
    pc.lathe_op("face, turn 39.80 x 26 (from 44.45)", face_min(44.45) + turn_min(44.45, D, 26))
    pc.lathe_op("rope groove 3 x 3 (3 mm grooving tool)", 1.2 * 3 / (0.05 * 1000) * 3)
    pc.lathe_op("drill 12 + bore the rod socket 12.95 x 8", drill_min(12.0, 10) + turn_min(12.0, SOCKET_D, 8))
    pc.lathe_op("part off; face to %.2f in a soft-jaw second op" % H, part_min(44.45) + face_min(D) + 3.0)
    pc.setup("-Z", label="bottom up in a 5C collet block: heater and thermocouple holes, three lead grooves",
             hold="5C collet block")
    pc.setup("+Z", label="top up in the collet block: 3 x M2", hold="5C collet block")
    pc.setup("+X", label="collet block on its side: radial M3 set-screw hole", hold="5C collet block, side")
    pc.tol += ["OD 39.80 0/-0.025 (with the 40.000-40.025 bore: 0.200-0.250 mm diametral clearance)",
               "top face flatness 0.02, Ra 1.6; parallel to the bottom within 0.03; length %.2f +-0.05" % H,
               "rod socket 12.95 +0.05/0 x 8.0", "heater holes %.2f +0.05/0" % hd]
    pc.changes += ["v2: %.0f mm thick (v1 28); two %.1f x %g heater holes for %g x %g mm cartridges at r %.1f (v1 6.40 for "
                   "1/4 in.); three %g x %g lead grooves in the underside from the holes to the socket (ft_model)"
                   % (H, hd, hdep, P["heater_d"], P["heater_l"], r, gw, gd),
                   "kept from v1: rod socket 12.95 (model 12.8) with an M3 dog-point set screw, now at z 5 (clear of "
                   "the grooves); thermocouple hole 2.0 (model 1.6); 3 x M2 x 3 for the substrate"]
    pc.finish = "6061 as machined; top face Ra 1.6"
    return pc


def mk05():
    D, H = P["plate_d"], P["sub_t"]
    pc = Piece("MK-05", "MK-05", "Substrate discs (10)", material="6061-T6511", qty=10, route="lathe + CNC mill",
               state="FT-0", stock="6061 round bar 1-3/4 in., one 100 mm length makes ten discs",
               stock_pn="McMaster 1610T family, 1-3/4 in. (suffix not read)", blank=blank_cyl(mm(1.75) / 2, -0.4, 6.4),
               pos="part z 0 = disc underside")
    turned = cyl(D / 2, 0, H)
    pc.pre = turned
    pc.solid = turned
    pc.hole("A", "csk", "M2", [(*polar(17.1, 90 + 120 * k), H) for k in range(3)], through=True,
            note="M2 x 4 flat head ISO 10642; heads 0.1-0.2 below the top")
    pc.lathe_op("turn 39.80 x 70 once for ten discs (from 44.45)", turn_min(44.45, D, 70) / 10)
    pc.lathe_op("face + chamfer + part off at 6.4, each", face_min(D) + part_min(D))
    pc.lathe_op("second op: face to 6.00 in soft jaws, each", face_min(D) + 1.5)
    pc.setup("+Z", label="top up, ten at a time in a fixture plate with ten 39.85 pockets", hold="fixture plate (FX-1)")
    pc.tol += ["OD 39.80 0/-0.025; thickness 6.00 +-0.03; top face flatness 0.02 (powder layer reference)",
               "top face: as faced Ra 1.6, or bead-blasted if the process wants it"]
    pc.changes += ["none: the 3 x M2 countersinks at r 17.1 are the model's"]
    return pc


# ====================================================================================================================
# MK-06 rods, MK-07 gland, MK-17 collar (bought)
# ====================================================================================================================
def rod_length(L):
    return P["socket"] + L["rod_vis"]


def mk06(which):
    L = L_BOX if which == "box" else L_CUBE
    ln = rod_length(L)
    pc = Piece("MK-06" + ("a" if which == "box" else "b"), "MK-06",
               "Piston rod, %s (%.1f long)" % ("box" if which == "box" else "cube, %.0f mm longer" % (
                   rod_length(L_CUBE) - rod_length(L_BOX)), ln),
               material="304 seamless tube 1/2 x 0.035 in.", qty=1, route="cut-off saw + lathe + CNC mill",
               state="FT-0" if which == "box" else "FT-1V",
               stock="seamless 304 tube, 1/2 in. OD x 0.035 in. wall (12.70 x 0.89), cut %.0f long" % (ln + 4),
               stock_pn="McMaster 89895K family ('Smooth-Bore Seamless 304 Stainless Steel Tubing'; 89895K623 is "
                        "the 2-1/4 in. size in mcmaster-parts.csv); 1/2 x 0.035 in. suffix not read",
               blank=blank_cyl(P["rod_od"] / 2, -2.0, ln + 2.0),
               pos="part z 0 = rod bottom end; z %.1f = top end in the plate socket" % ln)
    ro, ri = P["rod_od"] / 2, P["rod_od"] / 2 - P["rod_wall"]
    turned = ring(ro, ri, 0, ln)
    pc.pre = turned
    pc.solid = turned
    gw, gd = P["lead_groove"]
    z0, z1 = ln - P["socket"] - 1.0, ln - P["socket"] + gd        # at the socket mouth, under the plate's lead grooves
    notches = [box(-gw / 2, gw / 2, -ro - 1, -ri + 0.3, z0, z1).rotate(V(0, 0, 0), V(0, 0, 1), a - 270.0)
               for a in (270.0, 30.0, 150.0)]
    pc.cut(notches[0])
    pc.features.append(dict(kind="custom_slot", name="lead notch %.0f x %.1f through one wall (x3: index 120 deg)"
                            % (gw, z1 - z0), axis="+y", tool=4, center=[0.0, -ro, (z0 + z1) / 2],
                            size=[gw, z1 - z0], depth=P["rod_wall"] + 0.6))
    pc.hole("A", "plain", "2.5", [(ro, 0.0, ln - P["socket"] + 5.0)], axis="-x", depth=P["rod_wall"] + 0.3,
            note="set-screw dimple, one wall (the plate's M3 dog point at z 5)", tool=T.drill_tool(2.5))
    pc.cam_solid = pc.solid                   # the CAM model and the voxel check carry the first notch only
    for n in notches[1:]:
        pc.cut(n)
    pc.lathe_op("face both ends to length +-0.1, 0.5 x 15 deg lead-in chamfer at the top end",
                2 * face_min(12.7) + 3.0)
    pc.lathe_op("polish the OD (gland zone) to Ra <= 0.4 um, 320 then 600 grit", 6.0)
    pc.manual.append(("pot the lead plug: %.0f mm of vacuum epoxy in the lower end round the 6 leads (mix, fill, "
                      "cure overnight)" % P["plug_l"], 30.0))
    pc.setup("-Y", label="in a V-block on a 5C indexer: lead notch, then index 120 deg and repeat twice",
             hold="5C collet indexer", repeat=3)
    pc.setup("+X", label="turned 90 deg: set-screw dimple", hold="5C collet indexer")
    pc.tol += ["OD 12.62-12.73 (0.497-0.501 in.), measured: ASTM A269 allows +-0.13, which takes the rod seal "
               "outside Parker's 10-17 % squeeze; gland zone polished to 16 RMS (Ra ~0.4 um; Parker 10-20 uin)",
               "length %.1f +-0.1; ends square within 0.05" % ln,
               "no weld seam: seamless tube only (a welded seam leaks past the rod seal)",
               "notches lined up with the plate's lead grooves (30, 150, 270 deg from the set screw)"]
    pc.changes += ["v2: the 5 x 10 lead window becomes three %.0f x %.1f notches at 120 deg at the socket mouth, under the "
                   "plate's lead grooves (ft_model); the leads run down the rod to a %.0f mm potted plug in its lower "
                   "end" % (gw, z1 - z0, P["plug_l"]),
                   "length %.1f from ft_model's levels (rod_vis %.2f + socket %.0f)" % (ln, L["rod_vis"], P["socket"]),
                   "kept from v1: 2.5 dimple for the plate's set screw (now 5 mm above the socket mouth)"]
    pc.finish = "304: deburr inside and out; polish OD as above; passivate optional"
    return pc


def gland_dims():
    """rod groove diameter (Parker A-1, mid tolerance) and width (G, mid)"""
    g = GLANDS["rod"]
    return mm(sum(g["A1"]) / 2), mm(sum(g["G"]) / 2)


THROAT = 12.95


def mk07():
    a, t = 60.0, P["gland_t"]
    pc = Piece("MK-07", "MK-07", "Rod gland plate, 2 x AS568-112 rod seals", material="6061-T651", qty=1,
               route="CNC mill + lathe (4-jaw)", state="FT-0", stock="1/2 in. 6061 plate, 64 x 64 (faced to 12.0)",
               stock_pn="McMaster 89155K135 offcut", blank=blank_box(-32, 32, -32, 32, -0.35, 12.35), seal=True,
               pos="part z 12 = top face, against the box floor's underside (world z -64.6)")
    pc.solid = rbox(-a / 2, a / 2, -a / 2, a / 2, 0, t, 3.0)
    gdia, gw = gland_dims()
    land = (t - 2 * gw) / 3
    lathe_cut = cyl(THROAT / 2, -1, t + 1)
    for k in range(2):
        z0 = land + k * (gw + land)
        lathe_cut = lathe_cut.fuse(cyl(gdia / 2, z0, z0 + gw))
    pc.cut(lathe_cut)
    pc.pre = blank_solid(pc.blank).cut(lathe_cut)      # turned first (4-jaw on the sawn blank), then milled
    # face groove for AS568-031 round rod and bolts (vacuum sizing)
    oid, w = AS568["-031"]
    g0 = mm(oid) * FACE_ID_FACTOR / 2
    g1 = g0 + mm(sum(GLANDS["face_070"]["G"]) / 2)
    gd = mm(sum(GLANDS["face_070"]["L"]) / 2)
    pc.pocket("face O-ring groove (AS568-031)", ring(g1, g0, t - gd, t + 0.1), ((g0 + g1) / 2, 0, t - gd), tool=5,
              kind="groove")
    g = P["gland_screw"]
    pc.hole("A", "cbore", "M5", [(sx, sy, 0.0) for sx in (-g, g) for sy in (-g, g)], axis="+z",
            through=True, note="M5 SHCS with bonded seals up through the floor into the deck (box M5 x 25, cube M5 x 45)")
    pc.hole("B", "tap", "M3", [(sx, -25.0, 0.0) for sx in (-12.0, 12.0)], axis="+z", depth=6.0, thread="5",
            note="FT-0 lead terminal bracket (MK-17b) under the gland")
    pc.setup("+Z", face=(2, t), outline=(2, 3.0), label="top up: face, outline, face O-ring groove")
    pc.setup("-Z", face=(2, 0.0), outline=(2, -t - 0.3), label="bottom up: face to 12.0, rest of outline, c'bores")
    pc.lathe_op("4-jaw on the sawn 64 x 64 blank: face, drill 12, bore the throat 12.95", face_min(64) + drill_min(12.0, 14) +
                turn_min(12.0, THROAT, 13, f=0.08))
    pc.lathe_op("two internal grooves %.2f x %.2f wide (internal grooving tool, 3 mm insert, 2 plunges each)"
                % (gdia, gw), 2 * 2 * 1.2 * (gdia - THROAT) / 2 / (0.03 * 1200))
    pc.lathe_op("chamfer the throat 0.5 x 20 deg both ends (O-ring lead-in)", 2.0)
    pc.tol += ["throat 12.95 +0.05/0 (rod 12.70 +-0.13 as bought)",
               "rod grooves %.2f +0.05/0 dia x %.2f +0.13/0 wide (Parker gland depth %.2f-%.2f mm)"
               % (gdia, gw, mm(GLANDS["rod"]["L"][0]), mm(GLANDS["rod"]["L"][1])),
               "rod grooves: bottom 32 RMS (Ra 0.8), sides 32 RMS; corner radius 0.13-0.38 (Parker p. 5-31)", "top face flatness 0.02, Ra 0.4 um (16 RMS, face seal)",
               "grooves concentric with the throat within 0.03"]
    pc.changes += ["v2 took the fab's gland: 60 x 60 x 12, 4 x M5 at (+-12.5, +-12.5) inside the face seal; added 2 x M3 "
                   "underneath for the FT-0 lead terminal bracket (MK-17b)",
                   "two internal rod grooves for AS568-112 (0.487 x 0.103 in.), 1.6 mm lands in the 12 mm plate",
                   "throat 12.90 -> 12.95 (rod tolerance); face groove for AS568-031 round both the rod and the "
                   "bolts; 4 x M5 c'bored at (+-12.5, +-12.5), inside the face seal, so no bolt hole leaks",
                   "material 6061 (the model colours it stainless): no galling risk at this speed, easier to groove"]
    return pc


def mk17_buy():
    pc = Piece("MK-17", "MK-17", "FT-0 rod collar (buy)", material="aluminium clamp collar", qty=1, route="buy",
               state="FT-0", stock="Ruland MCL-8-A class one-piece clamp collar, 1/2 in. bore (1-1/8 in. OD x 13/32 in.)",
               stock_pn="Ruland MCL-8-A (dimensions as recalled: check Ruland's page; list price not read)")
    pc.solid = ring(mm(1.125) / 2, mm(0.5) / 2, 0, mm(13 / 32))
    pc.buy = "a stock 1/2 in. bore clamp collar does the job of the model's 30 x 10 split collar"
    pc.changes += ["bought instead of made: the model's Ø30 x 10 split collar is a catalogue part"]
    return pc


# ====================================================================================================================
# MK-08 hopper (sheet), cord clamp, arm, carriage bracket
# ====================================================================================================================
SHEET_T = 0.79          # 0.031 in. 304
K_FACTOR = 0.44


def bend_allowance(angle_deg, t=SHEET_T, r=None, k=K_FACTOR):
    r = r if r is not None else t
    return math.radians(angle_deg) * (r + k * t)


def mk08_hopper():
    hl, hw, hh = P["hopper"]
    pcs = []
    for half, ends in (("A", True), ("B", False)):
        pc = Piece("MK-08" + ("a" if half == "A" else "b"), "MK-08",
                   "Hopper wall %s (%s)" % (half, "with both end walls" if ends else "with rivet flanges"),
                   material="304 sheet 0.031 in. (0.79)", qty=1, route="sheet: laser-cut and bent (SendCutSend)",
                   state="FT-1", stock="SendCutSend 304 stainless (0.030-0.031 in. gauge as listed by them)",
                   stock_pn="flat pattern out/dxf/%s.dxf" % ("MK-08a" if ends else "MK-08b"),
                   pos="hopper frame: x across the hopper, y along the slot, z up from the slot")
        # 3D: wall at x = -hl/2 (A) or +hl/2 (B), lip to the slot, end walls (A) or 5 mm flanges (B)
        s = 1 if half == "B" else -1
        t_ = SHEET_T

        def xz_prism(pts, yc, half_len):
            return cq.Workplane("XZ", origin=(0, yc, 0)).polyline(pts).close().extrude(half_len, both=True).val()

        wall_pts = [(s * hl / 2, 6.0), (s * hl / 2, hh), (s * (hl / 2 - t_), hh), (s * (hl / 2 - t_), 6.0)]
        lip_pts = [(s * hl / 2, 6.0), (s * (hl / 2 - t_), 6.0 + 0.6), (s * 1.5, 2.0 + 1.0), (s * 1.5, 2.0)]
        sh = xz_prism(wall_pts, 0.0, hw / 2).fuse(xz_prism(lip_pts, 0.0, hw / 2))
        if ends:
            prof = [(-hl / 2, hh), (hl / 2, hh), (hl / 2, 6.0), (1.5, 2.0), (-1.5, 2.0), (-hl / 2, 6.0)]
            for sy in (-1, 1):
                sh = sh.fuse(xz_prism(prof, sy * (hw / 2 + t_ / 2), t_ / 2))
        else:
            for sy in (-1, 1):
                sh = sh.fuse(box(hl / 2 - 5.0, hl / 2, sy * (hw / 2 - t_ / 2) - t_ / 2, sy * (hw / 2 - t_ / 2) + t_ / 2,
                                 8.0, hh))
        sh = sh.clean()
        pc.solid = sh
        # flat pattern: wall height 29 (6..35), lip 9.39 at 65 deg, ends 20 x 29 (A) or flanges 5 (B)
        lip_len = math.hypot(hl / 2 - 1.5, 4.0)
        lip_ang = math.degrees(math.atan2(hl / 2 - 1.5, 4.0))
        h_wall = hh - 6.0
        bends = [dict(line="lip", angle=round(lip_ang, 1), inside_r=SHEET_T, allowance=round(bend_allowance(lip_ang), 3))]
        if ends:
            bends += [dict(line="end -y", angle=90.0, inside_r=SHEET_T, allowance=round(bend_allowance(90), 3)),
                      dict(line="end +y", angle=90.0, inside_r=SHEET_T, allowance=round(bend_allowance(90), 3))]
        else:
            bends += [dict(line="flange -y", angle=90.0, inside_r=SHEET_T, allowance=round(bend_allowance(90), 3)),
                      dict(line="flange +y", angle=90.0, inside_r=SHEET_T, allowance=round(bend_allowance(90), 3))]
        ba90 = bend_allowance(90)
        # flat outline (u along y, v up the wall; v < 0 = lip). End walls unfold sideways (u beyond +-hw/2).
        pts = []
        v_lip = -(bend_allowance(lip_ang) + lip_len - SHEET_T)
        if ends:
            e = hl - 2 * SHEET_T          # end wall width
            u0, u1 = -hw / 2 - ba90 - e, hw / 2 + ba90 + e
            pts = [(-hw / 2, v_lip), (hw / 2, v_lip), (hw / 2, 0.0), (u1, 0.0), (u1, h_wall), (u0, h_wall), (u0, 0.0),
                   (-hw / 2, 0.0)]
        else:
            u0, u1 = -hw / 2 - ba90 - 4.2, hw / 2 + ba90 + 4.2
            pts = [(-hw / 2, v_lip), (hw / 2, v_lip), (hw / 2, 2.0), (u1, 2.0), (u1, h_wall), (u0, h_wall), (u0, 2.0),
                   (-hw / 2, 2.0)]
        holes = []
        if ends:
            # arm screws on the +y end wall (2 x 3.4) and rivet holes on both end walls (2 x 2.5 each)
            ue = hw / 2 + ba90 + e / 2
            holes += [(ue - 4.0, h_wall - 4.0, 3.4), (ue + 4.0, h_wall - 4.0, 3.4)]
            for uu in (-(hw / 2 + ba90 + e - 2.5), hw / 2 + ba90 + e - 2.5):
                holes += [(uu, 8.0, 2.5), (uu, h_wall - 10.0, 2.5)]
            holes += [(-15.0, 3.0, 2.4), (15.0, 3.0, 2.4)]        # cord-clamp screws (M2) near the wall's bottom
        else:
            for uu in (-(hw / 2 + ba90 + 2.5), hw / 2 + ba90 + 2.5):
                holes += [(uu, 8.0, 2.5), (uu, h_wall - 10.0, 2.5)]
        pc.sheet = dict(thickness=SHEET_T, k_factor=K_FACTOR, outline=[[round(a, 3), round(b, 3)] for a, b in pts],
                        holes=[[round(a, 3), round(b, 3), d] for a, b, d in holes], bends=bends,
                        note="end walls (A) trimmed to the funnel at "
                        "assembly: see drawing" if ends else "flanges riveted to A's end walls")
        pc.manual.append(("rivet the two walls: 4 x 3/32 in. 304 blind rivets, seal the end seams with RTV", 20.0))
        pc.tol += ["bend angles +-1 deg; slot 3.0 +-0.3 after riveting (shim to set)"]
        pc.changes += ["the model's solid hopper is a bent shell: two walls of 0.79 mm 304, A with both end walls, B "
                       "with rivet flanges; 4 blind rivets (no welding). Funnel ends of A's end walls are cut to the "
                       "funnel profile after bending (or laser-cut to it if SendCutSend takes the 3D bend)"]
        pc.finish = "as supplied (2B); deburr the slot edges"
        pcs.append(pc)
    return pcs


def mk08_clamp():
    hl, hw, hh = P["hopper"]
    pc = Piece("MK-08c", "MK-08", "Cord clamp", material="6061-T6511", qty=1, route="CNC mill", state="FT-1",
               stock="6061 bar 1/4 x 1/2 in. sawn 50 long", stock_pn="6061 bar 1/4 x 1/2 in. (PN not read)",
               blank=blank_box(-2.0, 4.35, -25.0, 25.0, -1.5, 11.2),
               pos="part x 0 = face against hopper wall A; z 0 = blade plane (powder plane)")
    # part frame: x from -4 (outer) to 0 (wall side), z 1.5..10.5 (lowered 1.5 so the groove holds the cord centre)
    pc.solid = box(0, 4.0, -hw / 2, hw / 2, 1.5, 10.5)
    pc.pocket("cord slot 3.2 x 1.6 along y", box(0.4, 3.6, -hw / 2 - 1, hw / 2 + 1, 1.0, 3.1), (2.0, 0, 3.1),
              axis="+z", tool=5, kind="pocket", note="the cord sits half in it, bonded with RTV")
    pc.hole("A", "tap", "M2", [(0.0, sy, 6.0) for sy in (-15.0, 15.0)], axis="+x", depth=3.5, thread="3",
            note="M2 x 5 through hopper wall A")
    pc.setup("+Z", face=(2, 10.5), outline=(3, 1.2), label="top up: face, outline")
    pc.setup("-Z", face=(2, -1.5), label="bottom up: face, cord groove")
    pc.setup("-X", label="wall face up: 2 x M2")
    pc.changes += ["clamp lowered 1.5 mm (z 1.5..10.5) with a 3.2 x 1.6 slot underneath, so the cord's centre stays "
                   "at the blade plane + 1.5", "added: 2 x M2 to wall A"]
    return pc


def mk08_arm():
    hl, hw, hh = P["hopper"]
    yr = P["rc_y"]
    y0, y1 = hw / 2, yr - 14.0                  # ft_model: the arm runs from the hopper's end wall to the upright's back
    pc = Piece("MK-08d", "MK-08", "Hopper arm", material="6061-T6511", qty=1, route="CNC mill", state="FT-1",
               stock="6061 bar 3/8 x 3/4 in. sawn %.0f long" % (y1 - y0 + 4), stock_pn="6061 bar 3/8 x 3/4 in. (PN not read)",
               blank=blank_box(-9.53, 9.53, y0 - 2, y1 + 2, -0.76, 8.77),
               pos="part (x, y) = hopper frame; z 0 = arm underside (powder plane + %.0f)" % (hh - 8))
    pc.solid = box(-8, 8, y0, y1, 0, 8)
    pc.hole("A", "cbore", "M3", [(0.0, y1 - 4.0, 8.0)], through=True,
            note="to the bracket's notch")
    pc.hole("C", "tap", "M3", [(sx, y0, 4.0) for sx in (-4.0, 4.0)], axis="+y", depth=8.0, thread="6",
            note="hopper end wall")
    pc.setup("+Z", face=(2, 8.0), outline=(2, -0.3), label="top up: face, outline through (on parallels, tabs "
                                                             "kept by 0.3 skin), c'bores")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face to 8.0")
    pc.setup("-Y", label="hopper end up (vise): 2 x M3")
    pc.changes += ["v2: %.0f long, from the hopper's end wall (y %.0f) to the back of the bracket's upright (y %.0f): the "
                   "X-LSM100B's centre line is at y %.0f (v1 95.5)" % (y1 - y0, y0, y1, yr),
                   "added: 1 M3 c'bored into the bracket notch, 2 M3 tapped into the hopper's end wall; the vibration "
                   "motor is held by a cable tie or hose clamp (not machined)"]
    return pc


def mk08_bracket():
    """X-LSM100B carriage bracket (ft_model: foot 40 x 40 x 6 on the carriage, upright 40 x 8 up to the arm's top).
    Frame: x about the hopper centre, y world, z from the powder plane."""
    import ft_vendor as VEN
    yr = P["rc_y"]
    hh = P["hopper"][2]
    z_car = L_BOX["deck_top"] + P["rc_h"]                 # carriage top above the powder plane: -31.7
    z_top = hh                                            # arm top: +35
    yf0, yf1 = yr - 22.0, yr + 18.0                       # foot (ft_model)
    yw0, yw1 = yr - 22.0, yr - 14.0                       # upright
    H = z_top - z_car
    pc = Piece("MK-08e", "MK-08", "Carriage bracket (L: 6 mm foot on the X-LSM100B carriage, 8 mm upright)",
               material="6061-T6511", qty=1, route="CNC mill", state="FT-1",
               stock="6061 bar 1-3/4 x 3 in. (44.45 x 76.2) sawn 43 long", stock_pn="6061 bar 1-3/4 x 3 in. (PN not read)",
               blank=blank_box(-21.5, 21.5, yf0 - 2.2, yf0 - 2.2 + 44.45, z_car - 4.5, z_car - 4.5 + 76.2),
               pos="part (x, y, z) = hopper frame: x about the hopper centre, y world, z from the powder plane")
    web = box(-20, 20, yw0, yw1, z_car, z_top)
    foot = box(-20, 20, yf0, yf1, z_car, z_car + 6.0)
    s = web.fuse(foot).clean()
    rf = 6.5                         # inside corner = the 1/2 in. cutter's radius + 0.15
    s = s.fuse(box(-20, 20, yw1, yw1 + rf, z_car + 6.0, z_car + 6.0 + rf).cut(
        cylax(rf, (-21, yw1 + rf, z_car + 6.0 + rf), (1, 0, 0), 42)))
    pc.solid = s
    pc.pocket("arm notch 16 x 8", box(-8.05, 8.05, yw0 - 1, yw1 + 1, z_top - 8.0, z_top + 1), (5.0, yr - 18, z_top - 8.0),
              tool=3)
    pc.hole("A", "tap", "M3", [(0.0, yr - 18.0, z_top - 8.0)], depth=8.0, thread="6", note="arm screw")
    car = [(x, yr + y) for (x, y) in VEN.LSM["car_m3"] if abs(x) == 15.0 and y in (-5.0, 15.0)]
    pc.hole("B", "cbore", "M3", [(x, y, z_car + 6.0) for x, y in car], through=True,
            note="to the X-LSM100B carriage's M3 taps (Zaber STEP: ft_vendor.LSM car_m3), heads 0.4 under the foot top: "
                 "the shield clears the foot by 2 mm. Long-reach c'bore (61 mm under the upright's top)")
    pc.setup("+X", face=(2, 20.0), outline=(2, -19.0), label="L profile up (x up): face, outline of the L to x -19",
             hold="bar in the vise, 41 mm out")
    pc.setup("-X", face=(2, 20.0), outline=(2, 18.5), label="flip: face to 40.0 wide, last 1.5 mm of the outline")
    pc.setup("+Z", label="foot down on parallels: arm notch, M3, c'bores", hold="vise on the upright's y faces")
    pc.changes += ["v2: redesigned for the X-LSM100B carriage (ft_model): foot 40 x 40 x 6 on four of the carriage's M3 "
                   "taps (Zaber's STEP), upright 40 x 8, %.1f tall; the shield sits 2 mm over the foot, so v1's 3 mm "
                   "foot is gone" % H,
                   "the arm sits in a 16 x 8 notch in the upright's top"]
    return pc


# ====================================================================================================================
# MK-09 scan-head plate and collimator saddle
# ====================================================================================================================
# g3 gantry pieces. ft_model draws the flange plate up to the head's top (hb + 125), through the top flange; here the
# plate stops under the top flange (hb + 5 .. the beams' tops), which sits on it and on both beams.
GUSSET_Y = P["head_gussets_y_g2"]            # (-100.6, -15, 15): under the head's footprint
GUSSET_Z = (45.0, 85.0)                      # gusset screws up the plate (part y), where the triangle is wide enough
BRK_Y = (10.0, 25.0)                         # angle-bracket screws from each end of a plate


def mk09_plate():
    f = FR
    y0, y1 = f["y_f"] + f["h"], f["ry"][1] - f["h"]       # between the cross-beams' inner faces
    z0, z1 = f["hb"] + 5.0, f["zt"]                        # to the beams' tops (the top flange sits on it)
    Lp, Hp = y1 - y0, z1 - z0
    t = 12.0
    pc = Piece("MK-09a", "MK-09", "Scan-head flange plate (on the head's entrance face, between the cross-beams)",
               material="6061-T651", qty=1, route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate, %.0f x %.0f from a 12 x 24 in. sheet; faced to 12.0" % (Lp + 10, Hp + 10),
               stock_pn="McMaster 89155K135 (second blank from the deck's sheet)",
               blank=blank_box(-5, Lp + 5, -5, Hp + 5, -0.35, 12.35),
               pos="part x = world y - %.2f; part y = world z - %.1f; part z 0 = the face on the head (world x %.1f), "
                   "z 12 = the outer face (-x)" % (y0, z0, f["xe"]))
    pc.solid = rbox(0, Lp, 0, Hp, 0, t, 3.0)
    xi, zi = f["y_in"] - y0, f["z_in"] - z0
    pc.bore("input-turret opening 52", 26.0, xi, zi, t, 0, tool=2)
    # head screws: between the gussets (part x 35, 121, 151) and clear of the bracket taps and the turret opening
    pc.hole("A", "cbore", "M6", [(x, z, t) for x in (50.0, 100.0) for z in (10.0, 70.0)], through=True,
            note="M6 into the hurrySCAN's entrance face: PATTERN EST. (SCANLAB's drawing gives M6 screws and 6 h6 pins, "
                 "no positions): drill to the drawing")
    pc.hole("B", "tap", "M5", [(x, f["z_beam"] - z0, t) for x in (BRK_Y[0], BRK_Y[1], Lp - BRK_Y[1], Lp - BRK_Y[0])],
            through=True, thread="through", note="angle brackets MK-09c to the cross-beams' faces")
    pc.hole("C", "csk", "M5", [(gy - y0, z, 0.0) for gy in GUSSET_Y for z in GUSSET_Z], axis="+z", through=True,
            note="gussets MK-09e: flat heads flush on the head's side, put in before the head")
    pc.hole("D", "tap", "M5", [(x, Hp, t / 2) for x in (40.0, 110.0, 190.0, 260.0)], axis="-y", depth=12.0,
            thread="10", note="top flange MK-09d down into the plate's top edge")
    pc.setup("-Z", face=(1, 0.35), label="head face up: face, gusset c'sinks", hold="vise jaws on the blank's long edges")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="outer face up: face to 12.0, turret opening, c'bores, bracket "
             "taps, outline", hold="screwed down through holes A to a sacrificial plate")
    pc.setup("+Y", label="top edge up: 4 x M5 for the top flange", hold="vise, plate on edge")
    pc.tol += ["thickness 12.0 +-0.05; flatness 0.05 on the head face", "top edge square to the head face within 0.05"]
    pc.changes += ["v2: the head hangs by its entrance face from a %.0f x %.0f x 12 plate between both cross-beams (g3 "
                   "frame), not on a 275 mm horizontal plate" % (Lp, Hp),
                   "ft_model draws the plate %.0f tall, up through the top flange (they overlap by 12 mm); here it stops "
                   "under the flange, which bolts to its top edge (4 x M5). The FEA took them as one piece" % (Hp + 20),
                   "added: turret opening 52 (model), 4 x M6 for the head (pattern est.), 4 x M5 for the angle brackets, "
                   "6 x M5 c'sinks for the gussets, 4 x M5 in the top edge"]
    return pc


def mk09_angles():
    """flange-to-beam (2) and far-side (2) angle brackets: 1-1/2 x 1-1/2 x 3/16 in. 6061 angle, sawn 30 long; leg A on
    the plate, leg B on the cross-beam's face (one M6 into a drop-in T-nut)"""
    t, a, hgt = 4.76, 38.1, 30.0
    pc = Piece("MK-09c", "MK-09", "Angle brackets, plates to the cross-beams (4: 2 flange plate, 2 far-side plate)",
               material="6061-T6 angle", qty=4, route="saw + CNC mill",
               state="S1", stock="6061 angle 1-1/2 x 1-1/2 x 3/16 in. sawn 30 long (4 from one 6 in. length)",
               stock_pn="6061 equal angle 1-1/2 x 3/16 in. (PN not read)",
               pos="part x along leg B, y along leg A, z up the 30 mm height; leg A on the plate, leg B on the beam")
    ang = box(0, t, 0, a, 0, hgt).fuse(box(0, a, 0, t, 0, hgt)).clean()
    pc.pre = ang
    pc.solid = ang
    pc.blank = blank_box(0, a, 0, a, 0, hgt)
    pc.hole("A", "clear", "M5", [(t, y, hgt / 2) for y in (BRK_Y[0] + t, BRK_Y[1] + t)], axis="-x", through=True,
            note="M5 x 10 into the plate's taps")
    pc.hole("B", "clear", "M6", [(22.0, t, hgt / 2)], axis="-y", through=True,
            note="M6 x 12 into a drop-in T-nut in the beam's face slot")
    pc.setup("+X", label="leg B down in the vise: 2 x 5.5 in leg A", hold="vise, four at a time on a stop")
    pc.setup("+Y", label="leg A down: 6.6 in leg B", hold="vise, four at a time")
    pc.changes += ["new in v2 (MK-09 in ft_model): two at the flange plate's ends; g3 adds two at the far-side plate's "
                   "ends. Drawn in ft_model as a corner of three 4 mm plates; made here from standard angle"]
    return pc


def mk09_topflange():
    f = FR
    x0, x1 = f["fl_x0"] - P["head_flange"], f["fl_x1"]
    y0, y1 = f["y_f"] - f["h"], f["ry"][1] + f["h"]
    t = 12.0
    pc = Piece("MK-09d", "MK-09", "Head-plate top flange on both cross-beams", material="6061-T651", qty=1,
               route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate, %.0f x %.0f, faced to 12.0" % (x1 - x0 + 8, y1 - y0 + 8),
               stock_pn="McMaster 89155K135 (offcut of the deck's sheet)",
               blank=blank_box(x0 - 4, x1 + 4, y0 - 4, y1 + 4, -0.35, 12.35),
               pos="part (x, y) = world (x, y); part z 0 = underside, on the cross-beams' tops (world z %.1f)" % f["zt"])
    pc.solid = rbox(x0, x1, y0, y1, 0, t, 3.0)
    pc.hole("A", "cbore", "M6", [(x, y, t) for x in (x0 + 18.0, x0 + 42.0) for y in (f["y_f"], f["ry"][1])],
            through=True, note="M6 x 20 into drop-in T-nuts in both beams' top slots")
    yp0 = f["y_f"] + f["h"]
    pc.hole("B", "cbore", "M5", [((f["fl_x0"] + f["fl_x1"]) / 2, yp0 + x, t) for x in (40.0, 110.0, 190.0, 260.0)],
            through=True, note="M5 x 25 into the flange plate's top edge")
    pc.hole("C", "cbore", "M5", [(x, gy, t) for x in (f["fl_x0"] - 15.0, f["fl_x0"] - 40.0) for gy in GUSSET_Y],
            through=True, note="M5 x 20 into the gussets' top edges")
    pc.setup("-Z", face=(1, 0.35), label="underside up: face", hold="vise on the blank's long edges")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 12.0, c'bores, outline",
             hold="toe clamps; then screwed down through holes A")
    pc.changes += ["new in v2 (g2/g3 frame, ft_model): a %.0f x %.0f x 12 flange on both beams' tops, bolted to the "
                   "flange plate's top edge and the three gussets" % (x1 - x0, y1 - y0)]
    return pc


def mk09_gussets():
    f = FR
    H = f["zt"] - (f["hb"] + 5.0)
    W = P["head_flange"] - 5.0
    t = mm(5 / 16)
    pc = Piece("MK-09e", "MK-09", "Head-plate gussets (3)", material="6061-T651", qty=3, route="CNC mill", state="S1",
               stock="5/16 in. 6061 plate (7.94), %.0f x %.0f each" % (W + 8, H + 8),
               stock_pn="5/16 in. 6061-T651 plate (PN not read)",
               blank=blank_box(-W - 4, 4, -t / 2, t / 2, -4, H + 4),
               pos="part x 0 = the flange plate's outer face (world x %.1f), x < 0 away from the head; z 0 = the plate's "
                   "bottom edge; at world y %s" % (f["fl_x0"], ", ".join("%.1f" % g for g in GUSSET_Y)))
    tri = (cq.Workplane("XZ").polyline([(0.0, 0.0), (0.0, H), (-W, H)]).close().extrude(t / 2, both=True).val())
    pc.solid = tri
    pc.hole("A", "tap", "M5", [(0.0, 0.0, z) for z in GUSSET_Z], axis="-x", depth=12.0, thread="10",
            note="from the flange plate (flat heads on the head side)")
    pc.hole("B", "tap", "M5", [(x, 0.0, H) for x in (-15.0, -40.0)], depth=12.0, thread="10",
            note="from the top flange; 8 mm edge: tap straight")
    pc.setup("+Y", face=(2, t / 2), outline=(2, -t / 2 - 0.3), label="flat up: outline of the triangle",
             hold="screwed to a sacrificial plate, or three from one blank on tabs")
    pc.setup("+X", label="plate edge up (vise): 2 x M5", hold="vise")
    pc.setup("+Z", label="top edge up (vise): 2 x M5", hold="vise")
    pc.changes += ["new in v2 (g2/g3 frame): %.0f x %.0f triangles, 8 mm in ft_model, 5/16 in. (7.94) plate here; "
                   "bolted to the flange plate and the top flange (the model fuses them)" % (W, H)]
    return pc


def mk09_farplate():
    f = FR
    y0, y1 = f["y_f"] + f["h"], f["ry"][1] - f["h"]
    z0, z1 = f["hb"] + 5.0, f["hb"] + 125.0
    Lp, Hp, t = y1 - y0, z1 - z0, 10.0
    pc = Piece("MK-09f", "MK-09", "Head far-side support plate, between both cross-beams (g3)", material="6061-T651",
               qty=1, route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate, %.0f x %.0f, faced to 10.0" % (Lp + 10, Hp + 10),
               stock_pn="McMaster 89155K135 (second sheet)", blank=blank_box(-5, Lp + 5, -5, Hp + 5, -1.35, 11.35),
               pos="part x = world y - %.2f; part y = world z - %.1f; part z 0 = the face on the head's far side "
                   "(world x %.1f)" % (y0, z0, f["xf0"]))
    pc.solid = rbox(0, Lp, 0, Hp, 0, t, 3.0)
    hy = (LAY - P["head_side"][0] + 15.0 - y0, LAY + P["head_side"][1] - 15.0 - y0)
    pc.hole("A", "cbore", "M5", [(x, z, t) for x in hy for z in (20.0, 100.0)], through=True,
            note="into the head's far face: PATTERN EST. (no holes known there: tap the housing or use its cover "
                 "screws; check with SCANLAB)")
    pc.hole("B", "tap", "M5", [(x, f["z_beam"] - z0, t) for x in (BRK_Y[0], BRK_Y[1], Lp - BRK_Y[1], Lp - BRK_Y[0])],
            through=True, thread="through", note="angle brackets MK-09c to the cross-beams")
    pc.setup("-Z", face=(1, 1.35), label="head face up: face", hold="vise jaws on the long edges")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="outer face up: face to 10.0, c'bores, taps, outline",
             hold="screwed down through holes A")
    pc.changes += ["new in v2 (g3, the frame to build: 62 / 101 / 179 Hz in the FEA): a %.0f x %.0f x 10 plate on the "
                   "head's far (+x) face, held at both ends by angle brackets on the cross-beams" % (Lp, Hp),
                   "the head's far face has no published mounting holes: the 4 x M5 here are an estimate"]
    return pc


def mk22_saddle():
    """collimator clamp block hung under the front cross-beam (v1's saddle on the horizontal head plate, MK-09b, has no
    plate to stand on in v2; ft_model draws the collimator unsupported). Part frame = world, rotated so the bore runs
    along part z: part (x, y, z) = world (x, z, -y) ... kept simple: the block is cut from the +Y side."""
    import ft_vendor as VEN
    f = FR
    xb1 = f["xe"] - VEN.HS_IN["turret"][1]
    xbm = xb1 - VEN.HS_IN["block"][0] / 2
    zc = f["z_in"]
    zt = f["z_beam"] - f["h"]                      # the front beam's underside
    zb = zc - 20.0 - 16.0
    th = 25.0
    # part frame: x = world x - xbm, y = world z - zc (the collimator axis at the origin), z = along the collimator,
    # 0 .. th (world y = y_f - th / 2 + z)
    H0, H1 = zb - zc, zt - zc
    pc = Piece("MK-22b", "MK-22", "Collimator clamp block, hung under the front cross-beam", material="6061-T6511",
               qty=1, route="CNC mill + saw slit", state="S1",
               stock="6061 bar 1 x 3-1/2 in. (25.4 x 88.9) sawn %.0f long" % (H1 - H0 + 4),
               stock_pn="6061 bar 1 x 3-1/2 in. (PN not read)",
               blank=blank_box(-44.45, 44.45, H0 - 2, H1 + 2, -0.2, th + 0.2),
               pos="part x = world x - (%.1f); part y = world z - %.1f (the collimator's axis at the origin); part z "
                   "along the collimator (+y world), 0 = world y %.1f" % (xbm, zc, f["y_f"] - th / 2))
    pc.solid = box(-40, 40, H0, H1, 0, th)
    pc.bore("collimator bore 40.10", 20.05, 0.0, 0.0, th, 0.0, tool=2)
    pc.hole("A", "cbore", "M6", [(sx * 30.0, H0, th / 2) for sx in (-1, 1)], axis="+y", through=True,
            note="M6 x 70 up into drop-in T-nuts in the front beam's bottom slot")
    pc.hole("B", "cbore", "M5", [(40.0, H0 + 8.0, th / 2)], axis="-x", through=True,
            note="clamp screw across the slit; the far half tapped M5 by hand after drilling 4.2")
    pc.cam_solid = pc.solid
    pc.cut(box(-0.75, 0.75, H0 - 1, -19.0, -1, th + 1))
    pc.manual.append(("slit 1.5 wide from the bore down through the bottom wall (slitting saw or bandsaw)", 10.0))
    pc.setup("+Z", face=(2, th), outline=(2, -0.3), label="bore face up: face, outline, collimator bore",
             hold="screwed to a sacrificial plate, or vise on the 88.9 bar's edges")
    pc.setup("-Z", face=(2, 0.0), label="flip: face to 25.0", hold="vise")
    pc.setup("-Y", label="bottom up: 2 x M6 c'bores", hold="vise on the z faces")
    pc.setup("+X", label="+x end up: clamp-screw hole", hold="vise on the z faces")
    pc.tol += ["bore 40.10 +0.05/0, its axis %.1f under the beam's underside (the input beam's height)" % (zt - zc)]
    pc.changes += ["v2: the collimator saddle (v1 MK-09b, on the horizontal head plate) becomes a clamp block hung under "
                   "the front cross-beam: v2's head hangs on a vertical plate, and ft_model draws the collimator with no "
                   "support. Its axis follows head_in_z (world z %.1f)" % zc]
    return pc


def mk22_cage():
    pc = Piece("MK-22a", "MK-22", "Coaxial branch plate: SM1 bore and 30 mm cage on the mirror block's back face",
               material="6061-T651", qty=1, route="CNC mill", state="S1",
               stock="3/8 in. 6061 plate (9.53), 64 x 64, faced to 8.0", stock_pn="3/8 in. 6061 plate (PN not read)",
               blank=blank_box(-32, 32, -32, 32, -0.76, 8.77), pos="part z 0 = the face on the mirror block")
    t = 8.0
    pc.solid = rbox(-30, 30, -30, 30, 0, t, 3.0)
    pc.bore("SM1 bore 25.6 (SM1 thread: Thorlabs SM1 tap)", 12.8, 0, 0, t, 0, tool=3)
    pc.hole("A", "plain", "6.1", [(sx * 15.0, sy * 15.0, t) for sx in (-1, 1) for sy in (-1, 1)], through=True,
            note="30 mm cage rods (6 mm), bonded or held by M3 set screws from the edge")
    pc.hole("B", "cbore", "M4", [(sx * 22.0, sy * 22.0, t) for sx in (-1, 1) for sy in (-1, 1)], through=True,
            note="to the mirror block's back face: PATTERN EST. (the block was drawn from listing photos)")
    pc.setup("-Z", face=(2, 0.76), label="block face up: face", hold="vise")
    pc.setup("+Z", face=(2, t), outline=(2, -0.3), label="top up: face to 8, SM1 bore, cage holes, c'bores, outline")
    pc.changes += ["new in v2 (MK-22 in ft_model, not drawn there): the photodiode branch (MON4) mounts on the input "
                   "mirror block's back port through this plate"]
    return pc


# ====================================================================================================================
# MK-10 beam tubes and lens collar
# ====================================================================================================================
def beam_tube_len(L):
    """centre section: from the window flange's top (the fab's ring is 12 tall, the model's 10) to the collar's floor
    ring (ft_model: cs_len = (lens_bot - 10) - (roof_out + 16))"""
    return (L["lens_bot"] - 10.0) - (L["roof_out"] + WR_H + 6.0)


def mk10_tube(which):
    L = L_BOX if which == "long" else L_CUBE
    ln = beam_tube_len(L)
    split = P["tube_split"]["box" if which == "long" else "cube"]       # the halves slide off along this axis
    sa = "y" if split == "x" else "x"                                   # the seams are on this axis
    pc = Piece("MK-10" + ("a" if which == "long" else "b"), "MK-10",
               "Beam tube centre section, %s (%.1f long), split in two half-shells" % (which, ln),
               material="6061-T6 tube 2-3/8 x 0.125 in.", qty=1,
               route="saw + lathe + CNC mill + slitting saw", state="S2" if which == "long" else "FT-1V",
               stock="6061 round tube 60.3 x 3.18 wall (2-3/8 x 0.125 in.; ID 54)", stock_pn="6061 round tube (PN not read)",
               blank=blank_cyl(30.16, -2.0, ln + 2.0),
               pos="part z 0 = bottom end on the window flange's spigot; the halves slide off along %s" % split)
    turned = ring(30.16, 27.0, 0, ln)
    pc.pre = turned
    pc.solid = turned
    zm = ln / 2
    dz = min(8.0, ln / 2 - 4.0)
    for sgn in (1, -1):
        ax = ("-" if sgn > 0 else "+") + sa
        pts = []
        for o in (-12.0, 12.0):
            for z in (zm - dz, zm + dz):
                c = math.sqrt(30.16 ** 2 - o ** 2)
                pts.append((o, sgn * c, z) if sa == "y" else (sgn * c, o, z))
        pc.hole("A" if sgn > 0 else "B", "tap", "M3", pts, axis=ax, depth=4.5, thread="through the wall",
                note="toggle clamp across the %s%s seam (latch body on one half, catch on the other; bought)"
                % ("+" if sgn > 0 else "-", sa))
    pc.cam_solid = pc.solid
    kerf = box(-0.4, 0.4, -31, 31, -1, ln + 1) if split == "x" else box(-31, 31, -0.4, 0.4, -1, ln + 1)
    pc.cut(kerf)
    pc.lathe_op("saw, face both ends to %.1f +-0.2, deburr" % ln, 2 * face_min(60.3, 54.0) + 4.0)
    pc.manual.append(("slit both seams with a 0.8 mm slitting saw (tube in a fixture), deburr", 25.0))
    pc.manual.append(("bond a 0.5 mm light-baffle strip along the inside of one half's seams", 10.0))
    pc.setup("+" + sa.upper(), label="+%s seam up in V-blocks: 4 x M3 for its toggle clamp" % sa, hold="V-blocks")
    pc.setup("-" + sa.upper(), label="-%s seam up: 4 x M3" % sa, hold="V-blocks")
    pc.tol += ["length %.1f +-0.2; ends square within 0.1 (it butts on the flange and the collar)" % ln,
               "the halves match at the seams within 0.2 (light-tight with the baffle strip)"]
    pc.changes += ["v2: the beam tube's centre section, split lengthwise into two half-shells held by 2 toggle clamps; it "
                   "seats over the window flange's spigot and the collar's (ft_model). %.1f long: ft_model's %.1f less "
                   "the fab's 2 mm taller window ring" % (ln, ln + 2.0),
                   "the tie rods and sockets of v1 are gone"]
    pc.finish = "black anodise inside (stray light) or as is"
    return pc


def mk10_collar():
    lb = L_BOX["lens_bot"]
    tx, ty = TXB - LAX, TYB - LAY                    # the tube's centre from the lens axis: (0, 13)
    ri, ro = P["lens_d"] / 2 + 0.7, 68.0
    H = 40.0                                         # floor 6 + collar 34 (ft_model)
    pc = Piece("MK-10c", "MK-10", "Lens collar with the tube's upper spigot (on the lens)", material="6061-T651", qty=1,
               route="CNC mill", state="S2", stock="1-3/4 in. 6061 plate (44.45), 140 x 140",
               stock_pn="1-3/4 in. 6061-T651 plate (PN not read)",
               blank=blank_box(-70, 70, -70, 70, -3.7, 40.75),
               pos="part (x, y) = from the lens axis; part z 0 = the floor's underside (world z %.1f box); the spigot "
                   "hangs 3 below at (%.0f, %.0f)" % (lb - 10.0, tx, ty))
    body = cyl(ro, 0, H).cut(cyl(ri, 6.0, H + 1))
    body = body.fuse(ring(SPIG_R, SPIG_R - SPIG_W, -SPIG_H, 0.01, tx, ty)).clean()
    body = body.cut(cyl(SPIG_R - SPIG_W, -SPIG_H - 1, 7.0, tx, ty))
    pc.solid = body
    pc.features.append(dict(kind="adaptive", name="lens bore %.1f x 34 (adaptive)" % (2 * ri), axis="-z", tool=2,
                            probe=[ri - 8.0, 0.0, 6.0], note="", z_top=None))
    pc.boss("spigot %.0f x %.1f wall x %.0f, inside the centre section's upper end" % (2 * SPIG_R, SPIG_W, SPIG_H),
            (tx, ty + SPIG_R - SPIG_W / 2, -SPIG_H), 0.0, axis="+z", tool=2)
    pc.bore("tube bore %.0f through the floor and the spigot" % (2 * (SPIG_R - SPIG_W)), SPIG_R - SPIG_W, tx, ty, -SPIG_H,
            6.0, axis="+z", tool=2)
    pc.hole("A", "tap", "M3", [(ro, 0.0, z) for z in (11.0, 23.0)], axis="-x", depth=5.0, thread="4",
            note="beam-tube interlock switch D4NS-2CF (S5) on the +x side (est.)")
    pc.hole("B", "tap", "M4", [(math.sqrt(ro ** 2 - 25.0 ** 2), sy, 30.0) for sy in (-25.0, 25.0)], axis="-x",
            through=True, thread="through the wall", note="nylon-tip set screws onto the lens body")
    pc.setup("+Z", face=(2, H), outline=(2, -SPIG_H - 0.3), label="open end up: face to 40, outline, lens bore",
             hold="blank on parallels, toe clamps")
    pc.setup("-Z", face=(2, SPIG_H), label="floor up: face to the spigot, round the spigot, the 50 bore",
             hold="soft jaws in the lens bore (ID clamp)")
    pc.setup("+X", label="on its side: interlock-switch taps, two set screws", hold="vise, V-block")
    pc.tol += ["lens bore %.1f +0.3/0 (the LINOS lens is 119.8)" % (2 * ri), "spigot OD %.0f -0.10/0" % (2 * SPIG_R)]
    pc.changes += ["v2: bore 112 -> %.1f for the LINOS lens (119.8), OD 136, 34 tall on a 6 mm floor (ft_model); the "
                   "tube's upper spigot hangs under the floor, %.0f mm off the lens axis" % (2 * ri, ty),
                   "ft_model's floor hole (54) is wider than the spigot's bore (50), which leaves the spigot hanging in "
                   "air: here the floor is bored 50, the spigot's bore",
                   "held on the lens body by two nylon-tip M4 set screws (the model says 'clamped on the lens')"]
    return pc


# ====================================================================================================================
# MK-11 slot nozzle and exhaust collector
# ====================================================================================================================
def mk11_nozzle():
    pc = Piece("MK-11a", "MK-11", "Slot nozzle 45 x 4", material="6061-T6511", qty=1, route="CNC mill", state="FT-0",
               stock="6061 bar 3/4 x 1-1/4 in. (19.05 x 31.75) sawn 65 long",
               stock_pn="6061 bar 3/4 x 1-1/4 in. (PN not read)",
               blank=blank_box(-32.5, 32.5, -54.5, -54.5 + 31.75, -3.5, 15.55),
               pos="part (x, y) = world (x, y); part z 0 = well-block top (powder plane)")
    H = 12.0
    body = box(-30.5, 30.5, -46, -27, 0, H)
    boss = box(-5.0, 5.0, -52.0, -45.5, 0.0, H)
    pc.solid = body.fuse(boss).clean()
    pc.pocket("plenum 45 x 10 x 8 (open below, closed by the block top)", rbox(-22.5, 22.5, -39, -29, -1, 8.0, 1.6),
              (0, -34.0, 8.0), axis="+z", tool=4)
    pc.opening("slot exit 45 x 4 through the 2 mm front wall", box(-22.5, 22.5, -29.5, -26.0, 2.0, 6.0),
               (0, -27.0, 9.0), -29.5, axis="-y", tool=4)
    pc.hole("A", "plain", "6.40", [(0.0, -52.0, 6.0)], axis="+y", depth=15.0,
            note="1/4 in. 316 feed tube (89785K824) bonded or pressed in")
    pc.hole("B", "cbore", "M3", [(sx, -33.5, H) for sx in (-27.0, 27.0)], through=True, note="to the well block")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face, plenum", hold="vise")
    pc.setup("+Z", face=(2, H), outline=(2, -0.3), label="top up: face to 12, outline with the boss, c'bores")
    pc.setup("+Y", label="front face up: slot exit (1/8 in. end mill)", hold="vise on the x ends")
    pc.setup("-Y", label="boss up: feed-tube hole", hold="vise on the x ends")
    pc.changes += ["6061 instead of 304 (machined block, argon at <= 200 C)", "12 mm tall (was 8) and 61 long (was 55): "
                   "room for a plenum, the 1/4 in. feed tube and two M3 screws",
                   "feed: a 6.4 mm socket in the model's Ø10 boss, tube bonded in; plenum sealed by the block top"]
    return pc


def mk11_collector():
    pc = Piece("MK-11b", "MK-11", "Exhaust collector", material="6061-T6511", qty=1, route="CNC mill", state="FT-0",
               stock="6061 bar 3/4 x 1-1/4 in. sawn 70 long", stock_pn="6061 bar 3/4 x 1-1/4 in. (PN not read)",
               blank=blank_box(-35.0, 35.0, 26.0, 26.0 + 31.75, -2.5, 16.55),
               pos="part (x, y) = world (x, y); part z 0 = well-block top")
    H = 14.0
    body = box(-33, 33, 27, 40, 0, H)
    boss = box(-8.0, 8.0, 39.5, 48.0, 0.0, H)
    pc.solid = body.fuse(boss).clean()
    pc.pocket("plenum 50 x 7 x 10 (open below)", rbox(-25, 25, 29.0, 36.0, -1, 10.0, 1.6), (0, 32.5, 10.0), axis="+z",
              tool=4)
    pc.opening("inlet window 50 x 6 through the 2 mm front wall", box(-25, 25, 26.0, 29.5, 2.0, 8.0),
               (0, 27.0, 11.0), 29.5, axis="+y", tool=4)
    pc.hole("A", "plain", "9.6", [(0.0, 48.0, 7.0)], axis="-y", depth=13.0,
            note="3/8 in. exhaust tube bonded in, then the hose to the HEPA")
    pc.hole("B", "cbore", "M3", [(sx, 33.5, H) for sx in (-29.5, 29.5)], through=True, note="to the well block")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face, plenum")
    pc.setup("+Z", face=(2, H), outline=(2, -0.3), label="top up: face to 14, outline with the boss, c'bores")
    pc.setup("-Y", label="front face up: inlet window")
    pc.setup("+Y", label="boss up: exhaust-tube hole")
    pc.changes += ["6061 instead of 304", "14 mm tall (was 10) and 66 long (was 60): plenum, a 3/8 in. outlet tube "
                   "and two M3 screws; the outlet's 9.6 bore halves the gas speed of a 1/8 NPT fitting"]
    return pc


# ====================================================================================================================
# MK-12 stage shield (sheet)
# ====================================================================================================================
def mk12():
    yr = P["rc_y"]
    x0, x1 = P["rc_x0"] - 78.0, P["rc_x0"] + 88.0                    # ft_model
    y0, y1 = yr - 25.0, yr + 25.0
    half = P["rc_travel"] / 2
    sx0, sx1 = P["rc_x0"] - half - 22.0, P["rc_x0"] + half + 22.0
    t = 0.91
    pc = Piece("MK-12", "MK-12", "Stage shield", material="304 sheet 0.036 in. (0.91)", qty=1,
               route="sheet: laser-cut and bent (SendCutSend)", state="FT-1",
               stock="SendCutSend 304 stainless, 0.036 in. class (their gauge list not read)",
               stock_pn="flat pattern out/dxf/MK-12.dxf",
               pos="part (x, y) = world (x, y); part z 0 = deck top")
    z_top = P["rc_h"] + 8.0                         # ft_model: shield underside 8 over the carriage top (2 over the foot)
    top = box(x0, x1, y0, y1, z_top, z_top + t)
    top = top.cut(slot_xy(sx0, sx1, yr - 24.0, yr - 12.0, z_top - 1, z_top + 2))
    skirt = box(x0, x1, y0 - 1.0, y0 - 1.0 + t, 0, z_top + t)
    foot = box(x0, x1, y0 - 11.0, y0 - 1.0, 0, t)
    s_ = top.fuse(skirt).fuse(foot)
    for x in SHIELD_FOOT_X:
        s_ = s_.cut(cyl(1.7, -1, 2, x, yr - 31.0))
    pc.solid = s_
    ba = bend_allowance(90, t=t, r=t)
    h_sk = z_top + t
    W = x1 - x0
    v_top = (y1 - y0) - t
    v_sk = h_sk - 2 * t
    pts = [(0, 0), (W, 0), (W, v_top + ba + v_sk + ba + 10.0 - t), (0, v_top + ba + v_sk + ba + 10.0 - t)]
    slot_v = (y1 - (yr - 12.0)) - t / 2
    pc.sheet = dict(thickness=t, k_factor=K_FACTOR, outline=[[round(a, 3), round(b, 3)] for a, b in pts],
                    slot=dict(u0=sx0 - x0, u1=sx1 - x0, v0=slot_v, v1=slot_v + 12.0),
                    holes=[[x - x0, v_top + ba + v_sk + ba + 5.0, 3.4] for x in SHIELD_FOOT_X],
                    bends=[dict(line="top/skirt", v=round(v_top + ba / 2, 3), angle=90.0, inside_r=t,
                                allowance=round(ba, 3)),
                           dict(line="skirt/foot", v=round(v_top + ba + v_sk + ba / 2, 3), angle=90.0, inside_r=t,
                                allowance=round(ba, 3))])
    pc.tol += ["bends +-1 deg; slot 12 +-0.3 wide; holes +-0.2"]
    pc.changes += ["v2: for the X-LSM100B: %.0f x 50 top with a %.1f x 12 slot, a %.0f mm skirt (ft_model)"
                   % (W, sx1 - sx0, h_sk),
                   "added: a 10 mm foot along the skirt with 3 x 3.4 holes to the deck (M3)", "slot ends full round (R6)"]
    pc.finish = "as supplied (2B)"
    return pc


# ====================================================================================================================
# MK-13, MK-14 cube plates (Ideal Vacuum P108171 blanks)
# ====================================================================================================================
def iv_blank(z_out_top=True):
    """the 12 in. blank as ft_model draws it: plate 301.8 square x (22.9 - 7.6) plus a 264 square x 7.6 boss. Part
    frame: centre of the plate, z 0 = the boss face (inside), outside face at z 22.9"""
    pw, pt, bs, op = P["cube_plate"], P["cube_plate_t"], P["cube_boss"], P["cube_open"] - 2.0
    return box(-pw / 2, pw / 2, -pw / 2, pw / 2, bs, pt).fuse(box(-op / 2, op / 2, -op / 2, op / 2, 0, bs))


def mk13():
    pt = P["cube_plate_t"]
    pc = Piece("MK-13", "MK-13", "Cube top plate (Ideal Vacuum P108171 blank: window ring, drop tube, camera port)",
               material="6061 (Ideal Vacuum blank)", qty=1, route="CNC mill + tilted setup", state="FT-1V",
               stock="Ideal Vacuum P108171 blank plate (E2)", stock_pn="Ideal Vacuum P108171 (parts.csv E2)",
               blank=blank_box(-150.9, 150.9, -150.9, 150.9, 0, pt), seal=True,
               pos="part z 0 = boss face (inside); part (x, y) = world (x, y) - (%.0f, %.0f)" % (XC, YC))
    s_ = iv_blank()
    pc.pre = s_
    pc.solid = s_
    wx, wy = (c - d for c, d in zip(M.window_centre("FT-1V"), (XC, YC)))
    dx, dy = (c - d for c, d in zip(DROP_C, (XC, YC)))
    cam = M.camera_geometry("FT-1V")
    cx, cy = cam["W"][0] - XC, cam["W"][1] - YC
    pc.pocket("spot face 104 x 0.3 for the window ring's O-ring (Ra 0.8)", cyl(52.0, pt - 0.3, pt + 1, wx, wy),
              (wx + 45.0, wy, pt - 0.3), tool=2)
    pc.bore("window bore 53", 26.5, wx, wy, pt, 0, tool=2)
    pc.hole("A", "tap", "M5", [(wx + c[0], wy + c[1], pt - 0.3) for c in [polar(BC_R, 45 * k) for k in range(8)]],
            depth=12.0, thread="10", note="window stack (blind: no leak path)")
    pc.hole("B", "tap", "M4", [(dx + c[0], dy + c[1], 0.0) for c in [polar(38.5, 22.5 + 90 * k) for k in range(4)]],
            axis="+z", depth=9.0, thread="7", note="cover-slide drop tube MK-02f, inside")
    pc.hole("C", "tap", "M3", [(cx + c[0], cy + c[1], pt) for c in [polar(21.5, 45 + 90 * k) for k in range(4)]],
            depth=8.0, thread="6", note="camera port ring MK-19 (blind)")
    pc.manual.append(("camera bore 26 along the line of sight, %.1f deg from vertical: plate on a tilting table or sine "
                      "plate, helix-milled through (a tilted setup: 45 min to set up, 15 min to cut; estimate)"
                      % cam["tilt_deg"], 60.0))
    pc.cam_solid = pc.solid
    pc.cut(_tilted_bore(13.0, (cx, cy, pt), cam["u"]))
    pc.setup("+Z", label="outside face up: spot face, window bore, 8 x M5, 4 x M3", hold="toe clamps on the plate edge")
    pc.setup("-Z", label="boss face up: 4 x M4 for the drop tube", hold="toe clamps; the boss on parallels")
    pc.tol += ["spot face 104 x 0.3: flatness 0.02, Ra 0.4 um (window ring's AS568-140 seal)",
               "bore 53 +0.2/0, true position 0.2 to the plate centre; the plate's own O-ring face untouched",
               "camera bore: +-0.5 deg on its tilt (it only has to clear the camera's view cone)"]
    pc.changes += ["v2: window bore at the cube's window centre (%.0f, %.0f from the plate centre); a 26 camera bore "
                   "along the camera's line of sight (%.1f deg, a tilted setup: estimated, not programmed); 4 x M4 "
                   "inside for the cover-slide drop tube" % (wx, wy, cam["tilt_deg"]),
                   "kept from v1: 104 spot face for the ring's face seal, 8 x M5 blind"]
    return pc


def _tilted_bore(r, p, u, length=120.0):
    return M._place_axis(cq.Solid.makeCylinder(r, length, V(0, 0, -length / 2), V(0, 0, 1)), p, u)


def mk14():
    pt = P["cube_plate_t"]
    pc = Piece("MK-14", "MK-14", "Cube bottom plate (P108171 blank, bored for the rod gland)",
               material="6061 (Ideal Vacuum blank)", qty=1, route="CNC mill", state="FT-1V",
               stock="Ideal Vacuum P108171 blank plate (E2)", stock_pn="Ideal Vacuum P108171 (parts.csv E2)",
               blank=blank_box(-150.9, 150.9, -150.9, 150.9, 0, pt), seal=True,
               pos="part z 0 = boss face (inside, the deck sits on it); rod at part (x, y) = (-xc, -yc)")
    s_ = iv_blank()
    pc.pre = s_
    pc.solid = s_
    rx, ry = -XC, -YC
    g = P["gland_screw"]
    pc.bore("rod hole 20", 10.0, rx, ry, 0.0, pt, axis="+z", tool=3)
    pc.pocket("spot face 56 x 0.3 for the gland's AS568-031 (Ra 0.8)", cyl(28.0, pt - 0.3, pt + 1, rx, ry),
              (rx + 24.0, ry, pt - 0.3), axis="-z", tool=3)
    pc.hole("A", "clear", "M5", [(rx + sx, ry + sy, pt - 0.3) for sx in (-g, g) for sy in (-g, g)],
            through=True, note="gland screws into the deck, inside the gland's face seal")
    pc.hole("B", "tap", "M6", [(sx * 112.0, sy * 92.1, 0.0) for sx in (-1, 1) for sy in (-1, 1)], axis="+z", depth=12.0,
            thread="10", note="deck screws (blind), ft_model's (+-112, +-92.1)")
    pc.setup("+Z", label="outside face up: spot face, gland holes", hold="toe clamps on the plate edge")
    pc.setup("-Z", label="boss face up: rod hole, deck taps", hold="toe clamps; the boss on parallels")
    pc.tol += ["spot face 56 x 0.3: flatness 0.02, Ra 0.4 um", "holes A +-0.1 to the rod hole"]
    pc.changes += ["v2: the deck screws are 4 x M6 blind at (+-112, +-92.1) about the cube centre (v1 4 x M5 at the "
                   "corners); the gland holes stay inside the gland's face seal at (+-%.1f, +-%.1f)" % (g, g)]
    return pc


# ====================================================================================================================
# MK-15 stage bracket plate, riser, rod clamp
# ====================================================================================================================
RISER_TAPS = [(sx * 15.0, sy * 15.0) for sx in (-1, 1) for sy in (-1, 1)]     # plate to riser, M5 from below


def mk15_plate():
    h = 15.0
    ry = FR["ry"]
    y0, y1 = ry[0] - h, ry[1] + h                                  # ft_model: across both base rails
    pc = Piece("MK-15a", "MK-15", "Piston-stage bracket plate", material="6061-T651", qty=1, route="CNC mill",
               state="FT-1", stock="1/2 in. 6061-T651 plate, 190 x %.0f, faced to 10.0" % (y1 - y0 + 10),
               stock_pn="McMaster 89155K135 (second sheet)", blank=blank_box(-95, 95, y0 - 5, y1 + 5, -1.35, 11.35),
               pos="part (x, y) = world (x, y); part z 0 = underside, on the base rails (world z %.1f)"
                   % (P["bench_z"] + 2 * h))
    t = 10.0
    pc.solid = rbox(-90, 90, y0, y1, 0, t, 5.0)
    pc.hole("A", "clear", "M6", [(sx * 70.0, y, t) for sx in (-1, 1) for y in ry], through=True,
            note="M6 x 16 into drop-in T-nuts (5278N47) in the base rails (ft_model)")
    pc.hole("B", "cbore", "M5", [(x, y, 0.0) for x, y in RISER_TAPS], axis="+z", through=True,
            note="riser screws from below")
    pc.setup("-Z", face=(1, 1.35), label="bottom up: face, c'bores, drill through")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 10, outline", hold="screwed down through A")
    pc.changes += ["v2: 180 x %.1f across both base rails (ft_model; v1 190 x 270)" % (y1 - y0),
                   "added: 4 x M6 to the base rails at (+-70, rails), 4 x M5 c'bored for the riser"]
    return pc


def mk15_riser():
    import ft_vendor as VEN

    L = L_BOX
    base = (0 - P["sub_t"] - P["hp_t"] - L["rod_vis"]) - P["rod_end_z"] - P["vs_h"] - (0 - P["pz_bot"])
    h = base - (P["bench_z"] + 2 * 15.0 + 10.0)
    pc = Piece("MK-15b", "MK-15", "Piston-stage riser", material="6061-T651", qty=1, route="CNC mill", state="FT-1",
               stock="1 in. 6061 plate (25.4), 70 x 70, faced to %.1f" % h, stock_pn="1 in. 6061 plate (PN not read)",
               blank=blank_box(-35, 35, -35, 35, -2.5, 22.9),
               pos="part z 0 = underside, on the bracket plate (world z %.1f)" % (P["bench_z"] + 40.0))
    pc.solid = rbox(-32, 32, -32, 32, 0, h, 3.0)
    pc.hole("A", "tap", "M5", [(x, y, 0.0) for x, y in RISER_TAPS], axis="+z", depth=10.0, thread="8",
            note="from the bracket plate")
    pc.hole("B", "tap", "M6", [(x, y, h) for x, y in VEN.VSR["base_holes"]], depth=14.0, thread="12",
            note="X-VSR20A base: M6 clearance holes on a 50 mm square (Zaber STEP, ft_vendor.VSR base_holes)")
    pc.setup("+Z", face=(2, h), outline=(2, -0.3), label="top up: face to %.1f, outline, stage taps" % h)
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face, riser taps")
    pc.changes += ["v2: 64 x 64 x %.1f under the X-VSR20A (ft_model; its 64 x 64 base face, from Zaber's STEP); the stage's "
                   "4 x M6 on a 50 mm square are now read, not estimated" % h]
    return pc


def mk15_clamp():
    """rod-end block (ft_model): 64 x 40 x 40 on the X-VSR20A platform; rod clamp with a 1.5 slit to +y and an M4 across
    it, a lead pocket open to -y under the rod, 4 x M6 c'bored into the platform's M6 grid, the AE face at +x"""
    bh = P["blk_h"]
    z_rod = 16.0                                     # ft_model: the rod bore from 16 up; the rod's end at rod_end_z
    pc = Piece("MK-15c", "MK-15", "Rod-end block: rod clamp, lead pocket, AE face", material="6061-T6511", qty=1,
               route="CNC mill + saw slit", state="FT-1",
               stock="6061 bar 1-3/4 x 2-3/4 in. (44.45 x 69.85) sawn 43 long",
               stock_pn="6061 bar 1-3/4 x 2-3/4 in. (PN not read)", blank=blank_box(-34.9, 34.9, -22.2, 22.2, -1.5, 41.5),
               pos="part z 0 = underside on the X-VSR20A platform; the rod on the z axis")
    pc.solid = box(-32, 32, -20, 20, 0, bh)
    pc.bore("rod bore 12.95", THROAT / 2, 0, 0, bh, z_rod, tool=3)
    pc.pocket("lead pocket 16 x 28 x 12, open to -y", box(-8, 8, -21, 8, 4, z_rod), (0, 8.0, 10.0), axis="+y", tool=3)
    pc.hole("A", "cbore", "M6", [(sx * 25.0, sy * 12.5, bh) for sx in (-1, 1) for sy in (-1, 1)], through=True,
            note="M6 x 35 into the X-VSR20A platform's M6 grid (Zaber STEP)")
    pc.hole("B", "cbore", "M4", [(32.0, 12.0, 30.0)], axis="-x", through=True,
            note="clamp screw across the slit (ft_model); the far half tapped M4 by hand after drilling 3.3")
    pc.cam_solid = pc.solid
    pc.cut(box(-0.75, 0.75, 0, 21, 20.0, bh + 1))
    pc.manual.append(("slit 1.5 wide from the bore to +y, z 20 to the top (slitting saw or bandsaw)", 10.0))
    pc.setup("+Z", face=(2, bh), outline=(2, -0.3), label="top up: face, outline, rod bore, c'bores",
             hold="vise on the blank's y faces, on parallels")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face to 40", hold="vise")
    pc.setup("-Y", label="-y face up: lead pocket", hold="vise on the x ends")
    pc.setup("+X", label="+x (AE) face up: clamp-screw hole", hold="vise on the y faces")
    pc.tol += ["rod bore 12.95 +0.05/0, perpendicular to the base within 0.02 (the rod must run true in the gland)",
               "+x face flat within 0.02, Ra 1.6 (acoustic-emission sensor couplant)"]
    pc.changes += ["v2: the rod clamp becomes the rod-end block (ft_model): 64 x 40 x 40, a lead pocket open to -y for the "
                   "potted plug's pigtail, 4 x M6 into the stage's platform (read from Zaber's STEP), a flat AE face",
                   "kept from v1: rod bore 12.95 (model 12.8), the slit 1.5 wide sawn by hand"]
    return pc


# ====================================================================================================================
# v2 pieces: MK-02f drop tube, MK-17b FT-0 lead bracket, MK-19 port rings (camera and light ports), MK-20 camera foot
# and Scheimpflug wedges, MK-21c the cube plates' light-port bores, MK-23 deck clamps
# ====================================================================================================================
DROP_C = P["cs_c"]          # the fab centres the drop tube on the holder (0, -11); ft_model puts it at cs_drop_c (0, -16)


def mk02_drop():
    L = L_CUBE
    zs = L["dz"] + P["cs_z"]
    ln = round(L["roof_in"] - (zs + 10.0) - 2.1, 2)        # ft_model's length less 2.1: the box's holder fits it
    pc = Piece("MK-02f", "MK-02", "Cover-slide drop tube from the cube top plate (%.1f long, two flanges)" % ln,
               material="6061-T6511", qty=1, route="lathe + CNC mill", state="FT-1V",
               stock="6061 round bar 3-1/2 in. (88.9) sawn %.0f long" % (ln + 6), stock_pn="6061 round bar 3-1/2 in. (PN not read)",
               blank=blank_cyl(88.9 / 2, -3.0, ln + 3.0),
               pos="part z 0 = bottom flange's underside (the holder hangs from it); z %.1f = top flange's top, on MK-13's "
                   "boss face; axis at world (%.0f, %.0f)" % (ln, DROP_C[0], DROP_C[1]))
    tb = ring(32.0, 27.0, 0, ln).fuse(ring(44.0, 27.0, ln - 5.0, ln)).fuse(ring(38.0, 27.0, 0, 5.0)).clean()
    pc.pre = tb
    pc.solid = tb
    pc.hole("A", "clear", "M4", [(*polar(38.5, 22.5 + 90 * k), ln) for k in range(4)], depth=5.0, through=True,
            note="M4 x 12 up into MK-13's blind taps")
    pc.hole("B", "tap", "M4", [(*polar(30.0, a), 0.0) for a in (90, 180, 270)], axis="+z", depth=5.0, thread="through "
            "the flange", note="the cover-slide holder (its 3 x M4 at r 30)")
    pc.lathe_op("face, turn the flanges 88 and 76 and the tube 64 between them", face_min(88.9) + turn_min(88.9, 64.0, ln - 10))
    pc.lathe_op("drill 25, bore 54 through", drill_min(25.0, ln) + turn_min(25.0, 54.0, ln))
    pc.lathe_op("part off, face to length in a second op", part_min(88.9) + face_min(88.9, 54.0) + 3.0)
    pc.setup("-Z", label="bottom flange up: 3 x M4", hold="soft jaws on the tube")
    pc.setup("+Z", label="top flange up: 4 x 4.5", hold="soft jaws on the tube")
    pc.changes += ["new in v2 (ft_model MK-02, FT-1V): the cover-slide holder hangs %.0f mm under the cube's top plate "
                   "on this tube" % ln,
                   "centred on the holder (0, -11), not ft_model's (0, -16): there two of the holder's three screws "
                   "miss the tube's wall. The beam still clears: within 18 mm of (0, -11) at the plate and the holder",
                   "a bottom flange (76) for the holder's screws; made 2.1 mm shorter than drawn so the box's holder "
                   "(11.0 cover) fits"]
    return pc


def mk17_bracket():
    t = 2.03
    hw, ht, hv, hs = 40.0, 14.0, 60.0, 20.0           # width, top tab, upright, shelf (ft_model: 40 wide, 60 tall, 20)
    zb = L_BOX["gland_bot"]
    pc = Piece("MK-17b", "MK-17", "FT-0 lead terminal bracket under the gland (bent sheet)",
               material="5052-H32 aluminium sheet 0.080 in. (2.03)", qty=1,
               route="sheet: laser-cut and bent (SendCutSend)", state="FT-0",
               stock="SendCutSend 5052-H32, 0.080 in.", stock_pn="flat pattern out/dxf/MK-17b.dxf",
               pos="part (x, y) = world; part z 0 = the gland's underside (world z %.1f)" % zb)
    top = box(-hw / 2, hw / 2, -34.0, -34.0 + ht, -t, 0)
    up = box(-hw / 2, hw / 2, -34.0, -34.0 + t, -hv, 0)
    sh = box(-hw / 2, hw / 2, -34.0 - hs, -34.0 + t, -hv, -hv + t)
    s_ = top.fuse(up).fuse(sh)
    for x in (-12.0, 12.0):
        s_ = s_.cut(cyl(1.7, -5, 1, x, -25.0))
    s_ = s_.cut(box(-7.0, 7.0, -40, -28, -hv + 14.0, -hv + 26.0))
    for x in (-10.0, 10.0):
        s_ = s_.cut(cyl(1.7, -hv - 1, -hv + 3, x, -34.0 - hs / 2))
    pc.solid = s_
    ba = bend_allowance(90, t=t, r=t)
    v1 = ht - t
    v2 = v1 + ba + hv - 2 * t
    v3 = v2 + ba + hs - t
    pc.sheet = dict(thickness=t, k_factor=K_FACTOR, outline=[[-hw / 2, 0], [hw / 2, 0], [hw / 2, round(v3, 3)],
                                                             [-hw / 2, round(v3, 3)]],
                    holes=[[x, round(v1 - 9.0 + t, 3), 3.4] for x in (-12.0, 12.0)] +
                          [[x, round(v2 + ba + hs / 2 - t, 3), 3.4] for x in (-10.0, 10.0)],
                    slot=dict(u0=-7.0 + hw / 2 - hw / 2, u1=7.0, v0=round(v1 + ba + 34.0, 3), v1=round(v1 + ba + 46.0, 3)),
                    bends=[dict(line="tab/upright", v=round(v1 + ba / 2, 3), angle=90.0, inside_r=t, allowance=round(ba, 3)),
                           dict(line="upright/shelf", v=round(v2 + ba / 2, 3), angle=90.0, inside_r=t,
                                allowance=round(ba, 3))])
    pc.tol += ["bends +-1 deg; holes +-0.2"]
    pc.changes += ["new in v2 (ft_model MK-17, FT-0): a Z of 0.080 in. 5052 sheet: a tab under the gland (2 x M3 into "
                   "MK-07), a 60 mm upright with a 14 x 12 window for the pigtail, a 20 mm shelf for the terminal block. "
                   "ft_model's 4 mm L touches the gland only at an edge: the tab gives it screws"]
    pc.finish = "as supplied"
    return pc


def port_groove():
    """face groove under the port ring for AS568-026 (1.237 x 0.070 in.), vacuum sizing (Chart 4-3)"""
    gid = mm(1.237) * FACE_ID_FACTOR
    return gid / 2, gid / 2 + mm(sum(GLANDS["face_070"]["G"]) / 2), mm(sum(GLANDS["face_070"]["L"]) / 2)


def mk19_ring():
    H, R = 7.0, 25.0
    pc = Piece("MK-19", "MK-19", "Port ring: camera port (MK-19) and the two light ports (MK-21), one design (x3)",
               material="6061-T651", qty=3, route="CNC mill", state="FT-0", seal=True,
               stock="3/8 in. 6061 plate (9.53) faced to 7.0, 56 x 56 each", stock_pn="3/8 in. 6061 plate (PN not read)",
               blank=blank_box(-28, 28, -28, 28, -1.27, 8.26),
               pos="part z 0 = the face on the enclosure (box door or wall; MK-13 or the cube's plates in FT-1V)")
    pc.solid = cyl(R, 0, H)
    pc.bore("aperture 20", 10.0, 0, 0, H, 0, tool=3)
    pc.pocket("window seat 25.6 x 4.1 (25.4 x 3 window over a 1.0 cover slide)", cyl(12.8, H - 4.1, H + 1),
              (11.5, 0, H - 4.1), tool=3)
    g0, g1, gd = port_groove()
    pc.pocket("face O-ring groove (AS568-026)", ring(g1, g0, -0.1, gd), ((g0 + g1) / 2, 0, gd), axis="+z", tool=5,
              kind="groove")
    pc.hole("A", "clear", "M3", [(*polar(21.5, 45 + 90 * k), H) for k in range(4)], through=True,
            note="M3 to the door or wall (nuts or PEM studs inside, within the O-ring) / MK-13's taps")
    pc.setup("-Z", face=(2, 1.27), label="face side up: face, O-ring groove", hold="vise, three at a time")
    pc.setup("+Z", face=(2, H), outline=(2, -0.3), label="top up: face to 7, aperture, window seat, holes, outline",
             hold="screwed to a sacrificial plate through holes A")
    pc.tol += ["seat floor flatness 0.02 (the cover slide and window rest on it)",
               "face (z 0): flatness 0.02, Ra 0.4 um (16 RMS) inside the groove"]
    pc.changes += ["new in v2 (ft_model MK-19 and MK-21): ft_model draws a 44 x 7 ring whose 26 bore lets the 25.4 "
                   "window fall through and has no seal; here OD 50, a 20 aperture under a 25.6 x 4.1 seat (window and "
                   "cover slide, bonded with RTV at the top edge), an AS568-026 face groove round the enclosure's 28 "
                   "hole, 4 x M3",
                   "the camera port and the two light ports take the same ring: one program, three pieces"]
    return pc


def mk20_parts():
    """camera foot (turned) and the two Scheimpflug wedges (turned, C-mount threads, wedge face on a sine vise). The
    post and the right-angle clamp are bought (Thorlabs 12 mm post and post clamp class)."""
    cb = M.camera_geometry("FT-1")["scheimpflug_deg"]
    cc = M.camera_geometry("FT-1V")["scheimpflug_deg"]
    foot = Piece("MK-20a", "MK-20", "Camera post foot (bonded to the door or the top plate)", material="6061-T6511",
                 qty=1, route="lathe", state="FT-0", stock="6061 round bar 1-1/4 in. (31.75) sawn 12 long",
                 stock_pn="6061 round bar 1-1/4 in. (PN not read)", blank=blank_cyl(15.875, -1.0, 7.0),
                 pos="part z 0 = the face bonded to the enclosure")
    foot.solid = cyl(15.0, 0, 6.0).cut(cyl(2.5, 1.0, 7.0))
    foot.lathe_op("face, turn 30, drill 5.0 x 5, tap M6 (the post's thread), chamfer, part off",
                  face_min(31.75) + turn_min(31.75, 30.0, 8) + drill_min(5.0, 6) + 2.0 + part_min(31.75))
    foot.lathe_op("second op: face to 6.0, scuff the face for the epoxy", face_min(30.0) + 1.5)
    foot.changes += ["new in v2 (ft_model MK-20): a foot bonded with structural epoxy, so the door gets no more holes; "
                     "post (12 mm, M6) and right-angle clamp bought (Thorlabs class)"]
    wd = Piece("MK-20c", "MK-20", "Scheimpflug wedges, C-mount (2: %.2f deg box, %.2f deg cube)" % (cb, cc),
               material="6061-T6511, black anodised", qty=2, route="lathe + sine vise", state="FT-0",
               stock="6061 round bar 1-3/4 in. (44.45), 12 long each", stock_pn="6061 round bar 1-3/4 in. (PN not read)",
               blank=blank_cyl(22.2, -1.0, 9.0), pos="part z 0 = the lens side")
    w = cyl(19.0, 0, 6.0).cut(cyl(11.0, -1, 8.0))
    wd.solid = w.cut(box(-20, 20, -20, 20, 6.0 - 1.0, 9.0).rotate(V(0, 0, 6.0), V(1, 0, 6.0), -cb))
    wd.lathe_op("face, turn 38, bore 22, single-point the C-mount (1-32 UN) inside, each", face_min(44.45) +
                turn_min(44.45, 38.0, 8) + turn_min(22.0, 24.5, 6) + 12.0)
    wd.lathe_op("second op: the male C-mount thread on the other side, each", 12.0 + face_min(38.0))
    wd.manual.append(("wedge face on a sine vise: %.2f and %.2f deg, a facing pass each (set-up 20 min, 5 min each)"
                      % (cb, cc), 30.0))
    wd.changes += ["new in v2 (ft_model MK-20): the Scheimpflug angles from camera_geometry: %.2f deg (box, 16 mm "
                   "lens) and %.2f deg (cube, 25 mm)" % (cb, cc)]
    wd.finish = "black anodise (outside service), or black-out paint"
    return [foot, wd]


def mk21_cube():
    pt = P["cube_plate_t"]
    lg = M.light_geometry("FT-1V")
    pc = Piece("MK-21c", "MK-21", "Light-port bores in the cube's left plate and door (2 Ideal Vacuum E2 plates)",
               material="6061 (Ideal Vacuum plates)", qty=2, route="tilted setup on the mill", state="FT-1V", seal=True,
               stock="the cube's left plate and its door (parts.csv E2)", stock_pn="Ideal Vacuum (parts.csv E2)",
               pos="plate frame as MK-13: z 0 = the boss face (inside)")
    s_ = iv_blank()
    el = math.radians(P["light_el"][0])
    s_ = s_.cut(_tilted_bore(12.0, (-45.0, -35.8, pt), (0.0, -math.sin(el), math.cos(el))))
    pc.solid = s_
    pc.manual.append(("per plate: on a tilting table or sine plate at the light's elevation (%g deg left, %g deg door), "
                      "helix-mill a 24 bore through (45 min to set up, 15 min to cut), then 4 x M3 x 8 blind for the port "
                      "ring on the outside face (10 min); estimate, not programmed" % tuple(P["light_el"]), 2 * 70.0))
    pc.changes += ["new in v2 (ft_model MK-21): 24 bores along the raking lights' lines (left plate %g deg, door %g deg) "
                   "with a port ring (MK-19) on each; tilted, so estimated, not programmed" % tuple(P["light_el"])]
    pc.tol += ["bore direction +-0.5 deg; the port ring's face is the plate's own outside face (flat, O-ring land)"]
    return pc


def mk23_clamps():
    import ft_vendor as VEN
    sx_ = VEN.SAG["studs"][0] / 2
    xs, xd0 = XC + sx_, XC + (P["deck"][0] / 2 - 8.0)
    ln = abs(xs - xd0) + 12.0
    pc = Piece("MK-23", "MK-23", "Deck clamps on the box's panel studs (4)", material="6061-T6511", qty=4,
               route="saw + CNC mill", state="S2", stock="6061 bar 3/16 x 3/4 in. (4.76 x 19.05) sawn %.0f long" % (ln + 2),
               stock_pn="6061 bar 3/16 x 3/4 in. (PN not read)",
               blank=blank_box(-1.0, ln + 1.0, -9.525, 9.525, 0.0, 4.76),
               pos="part x 0 = the stud end; the deck end presses on the deck's top 14 mm in from its edge")
    pc.solid = rbox(0, ln, -9.0, 9.0, 0, 4.76, 3.0)
    pc.hole("A", "clear", "M5", [(6.0, 0.0, 4.76)], through=True,
            note="the #10 panel stud (4.8); a 10 mm spacer under this end (the stud stands on the floor, the deck "
                 "10 mm higher)")
    pc.setup("+Z", outline=(2, -0.3), label="four in the vise: hole, outline (ends rounded R3)", hold="vise, on a stop")
    pc.changes += ["new in v2 (ft_model MK-23): %.0f x 18 x 4.76 bars (model 4 thick: 3/16 in. bar as sawn) holding the "
                   "deck on the box's four panel studs, so the floor gets no screw holes" % ln]
    return pc


# ====================================================================================================================
# MK-16 overflow cup, MK-18 target stand and target
# ====================================================================================================================
def mk16():
    h = P["so_l"] + P["deck_t"] - 1.0
    pc = Piece("MK-16", "MK-16", "Overflow cup", material="6061-T6511", qty=1, route="CNC mill", state="FT-0",
               stock="6061 bar 1/2 x 2 in. (12.7 x 50.8) sawn 25 long", stock_pn="6061 bar 1/2 x 2 in. (PN not read)",
               blank=blank_box(19.15, 31.85, -25.4, 25.4, -1.5, h + 1.8),
               pos="part (x, y) = world (x, y); part z 0 = enclosure floor top")
    pc.solid = rbox(20.25, 30.75, -24.75, 24.75, 0, h, 1.0)
    pc.pocket("cup 7.5 x 46.5 x %.1f deep" % (h - 1.0), rbox(21.75, 29.25, -23.25, 23.25, 1.0, h + 1, 3.3),
              (25.5, 0, 1.0), tool=3)
    pc.setup("+Z", face=(2, h), outline=(2, -0.3), label="top up: face, outline, pocket")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face to height")
    pc.changes += ["6061 machined instead of 304 sheet: walls 1.5 (model 0.5), powder-tight corners, no welding; "
                   "outer 10.5 x 49.5 still fits the deck cut-out"]
    return pc


def mk18():
    deck_top = M.levels("S1")["under"] + P["deck_t"]
    ht = mm(0.125)
    h = -3.0 - deck_top - (ht - 3.0)
    stand = Piece("MK-18a", "MK-18", "Guide-laser target stand", material="6061-T6511", qty=1, route="CNC mill",
                  state="S1", stock="6061 square bar 2-1/2 in. (63.5) sawn 55 long",
                  stock_pn="6061 square bar 2-1/2 in. (PN not read)", blank=blank_box(-31.75, 31.75, -31.75, 31.75, -1.7, h + 1.7),
                  pos="part (x, y) = world; part z 0 = deck top in S1")
    stand.solid = box(-30, 30, -30, 30, 0, h)
    stand.hole("A", "clear", "M5", [(sx * 12.5, sy * 12.5, 0.0) for sx in (-1, 1) for sy in (-1, 1)], axis="+z",
               through=True, note="M5 x 20 down into the deck's gland taps")
    stand.hole("W", "plain", "10.0", [(sx * 12.5, sy * 12.5, h) for sx in (-1, 1) for sy in (-1, 1)], depth=h - 12.0 - 3.0,
               note="screw wells, 10 x D: peck; the M5 head sits on the drill point 12 above the base (washer)")
    stand.hole("B", "tap", "M3", [(sx * 24.0, sy * 24.0, h) for sx in (-1, 1) for sy in (-1, 1)], depth=8.0, thread="6",
               note="target plate")
    stand.setup("+Z", face=(2, h), outline=(2, 1.0), label="top up: face, outline, wells, M3")
    stand.setup("-Z", face=(2, 0.0), outline=(2, -h - 0.3), label="bottom up: face to height, holes A")
    stand.tol += ["height %.2f +-0.05 (puts the target's top at the powder plane, z 0)" % h,
                  "top parallel to the base within 0.03"]
    stand.changes += ["height %.2f (model 51.6) for a 1/8 in. (3.18) target plate instead of 3.0" % h,
                      "added: 4 x M5 to the deck through deep wells, 4 x M3 for the target"]
    tg = Piece("MK-18b", "MK-18", "Target plate 80 x 80 x 1/8 in., black anodised", material="6061-T6 sheet 1/8 in.",
               qty=2, route="sheet: laser-cut (SendCutSend) or bandsaw + mill; anodise outside", state="S1",
               stock="1/8 in. 6061 sheet (SendCutSend stock)", stock_pn="flat pattern out/dxf/MK-18b.dxf",
               pos="part z 0 = underside on the stand")
    tg.solid = box(-40, 40, -40, 40, 0, ht)
    for sx in (-1, 1):
        for sy in (-1, 1):
            tg.solid = tg.solid.cut(cyl(1.7, -1, ht + 1, sx * 24.0, sy * 24.0)).cut(
                cq.Solid.makeCone(0.0, 3.6, 3.6, V(sx * 24.0, sy * 24.0, ht - 3.6 + 0.0), V(0, 0, 1)))
    tg.sheet = dict(thickness=ht, k_factor=None, outline=[[-40, -40], [40, -40], [40, 40], [-40, 40]],
                    holes=[[sx * 24.0, sy * 24.0, 3.4] for sx in (-1, 1) for sy in (-1, 1)], bends=[])
    tg.manual.append(("countersink 4 holes by hand (M3 flat head)", 6.0))
    tg.changes += ["two plates (one spare): the S1 checks mark them"]
    tg.finish = "black anodise (type II), outside service; not read"
    return [stand, tg]


# ====================================================================================================================
def build_all():
    pcs = [mk01(), mk02_ring(), mk02_flange(), mk02_clamp(), *mk02_holder(), mk02_drop(), *mk03(), mk04(), mk05(),
           mk06("box"), mk06("cube"), mk07(), *mk08_hopper(), mk08_clamp(), mk08_arm(), mk08_bracket(), mk09_plate(),
           mk09_angles(), mk09_topflange(), mk09_gussets(), mk09_farplate(), mk10_tube("long"), mk10_tube("short"),
           mk10_collar(), mk11_nozzle(), mk11_collector(), mk12(), mk13(), mk14(), mk15_plate(), mk15_riser(),
           mk15_clamp(), mk16(), mk17_buy(), mk17_bracket(), *mk18(), mk19_ring(), *mk20_parts(), mk21_cube(),
           mk22_cage(), mk22_saddle(), mk23_clamps()]
    return pcs


def export_dxf(pc, path):
    """flat pattern outline and holes (cut layer only; bend lines go on the drawing, not in the cut file)"""
    import ezdxf
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    s = pc.sheet
    msp.add_lwpolyline([tuple(q) for q in s["outline"]], close=True)
    for x, y, d in s.get("holes", []):
        msp.add_circle((x, y), d / 2)
    if s.get("slot"):
        sl = s["slot"]
        r = (sl["v1"] - sl["v0"]) / 2
        msp.add_line((sl["u0"] + r, sl["v0"]), (sl["u1"] - r, sl["v0"]))
        msp.add_line((sl["u0"] + r, sl["v1"]), (sl["u1"] - r, sl["v1"]))
        msp.add_arc((sl["u0"] + r, sl["v0"] + r), r, 90, 270)
        msp.add_arc((sl["u1"] - r, sl["v0"] + r), r, -90, 90)
    doc.saveas(str(path))


def export(pcs):
    import time
    (OUT / "dxf").mkdir(parents=True, exist_ok=True)
    for pc in pcs:
        if pc.sheet and pc.sheet.get("outline"):
            export_dxf(pc, OUT / "dxf" / (pc.pid + ".dxf"))
    (SCRATCH / "pieces").mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    recs = []
    for pc in pcs:
        rec = pc.record()
        if pc.solid is not None:
            cs = pc.cam_solid if pc.cam_solid is not None else pc.solid
            cs.exportBrep(str(SCRATCH / "pieces" / (pc.pid + ".brep")))
            pc.solid.exportBrep(str(SCRATCH / "pieces" / (pc.pid + "_draw.brep")))
            cq.exporters.export(cq.Workplane().add(cs), str(SCRATCH / "pieces" / (pc.pid + ".stl")),
                                tolerance=0.02, angularTolerance=0.1)
        start = pc.pre if pc.pre is not None else (blank_solid(pc.blank) if pc.blank else None)
        if start is not None:
            start.exportBrep(str(SCRATCH / "pieces" / (pc.pid + "_start.brep")))
            cq.exporters.export(cq.Workplane().add(start), str(SCRATCH / "pieces" / (pc.pid + "_start.stl")),
                                tolerance=0.02, angularTolerance=0.1)
            rec["start_volume_cm3"] = round(start.Volume() / 1000, 2)
        if pc.lathe_fill is not None:
            bb = pc.solid.BoundingBox()
            tgt = pc.solid.fuse(pc.lathe_fill.intersect(box(bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)))
            cq.exporters.export(cq.Workplane().add(tgt), str(SCRATCH / "pieces" / (pc.pid + "_target.stl")),
                                tolerance=0.02, angularTolerance=0.1)
            rec["has_target"] = True
        recs.append(rec)
    spec = dict(made=time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), pieces=recs)
    (SCRATCH / "pieces.json").write_text(json.dumps(spec, indent=1))
    (OUT / "pieces.json").write_text(json.dumps(spec, indent=1))
    return recs


if __name__ == "__main__":
    import time
    t0 = time.time()
    pcs = build_all()
    for pc in pcs:
        v = pc.solid.Volume() / 1000 if pc.solid is not None else 0
        print("%-7s %-55s vol %7.2f cm3 holes %3d setups %d valid %s" % (pc.pid, pc.name[:55], v, pc.n_holes(),
                                                                         len(pc.setups), pc.solid.isValid()))
    recs = export(pcs)
    print("built and exported %d pieces in %.1f s" % (len(pcs), time.time() - t0))
