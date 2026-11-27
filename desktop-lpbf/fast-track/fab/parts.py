"""Fabrication-ready models of the fast-track machine's made parts MK-01..MK-18, split into the pieces a machinist makes
(#260, PR 294 round 2).

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
if "clamp_h" not in P or P["deck"][0] != 250.0:
    sys.exit("parts.py builds the v1 fab set from ft_model at d117ba8; the CAD v2 model (e6efa1c) changes or removes "
             "parameters it reads. Port it first: README.md, 'CAD v2', and v2_delta.py list what changes.")
V = cq.Vector
IN = 25.4
OUT = HERE / "out"
SCRATCH = pathlib.Path("/tmp/ft-fab")

L_BOX, L_CUBE = M.levels("FT-1"), M.levels("FT-1V")
XC, YC = P["deck_c"]

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

    def setup(self, up, *, face=None, outline=None, label="", hold="", stock_note=""):
        """face: (tool, z_to) in the setup frame; outline: (tool, z_to) adaptive outside of the setup's top face"""
        n = "ABCDEFG"[len(self.setups)]
        self.setups.append(dict(name="%s_%s" % (self.pid, n), up=up, face=face, outline=outline, label=label,
                                hold=hold, stock_note=stock_note))

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
def mk01():
    t = P["deck_t"]
    x0, x1 = XC - P["deck"][0] / 2, XC + P["deck"][0] / 2
    y0, y1 = YC - P["deck"][1] / 2, YC + P["deck"][1] / 2
    pc = Piece("MK-01", "MK-01", "Deck plate", material="6061-T651", qty=1, route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate (12.7 +0/+0.69), 260 x 260 cut from a 12 x 24 in. sheet; faced to 10.0",
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
    g = 12.5
    pc.hole("B", "tap", "M5", [(sx, sy, t) for sx in (-g, g) for sy in (-g, g)], through=True, thread="through",
            note="rod-gland screws from below (box: through the floor sheet; cube: through MK-14)")
    cx = [(XC + sx * 115, YC + sy * 115, t) for sx in (-1, 1) for sy in (-1, 1)]
    pc.hole("C", "cbore", "M5", cx, through=True, note="deck to enclosure floor (box: M5 nuts under the floor; "
                                                         "cube: MK-14 tapped)")
    # recoater stage X-LSQ075B (pattern est.: Zaber's drawing not read) and shield foot
    yr = P["rc_y"]
    pc.hole("D", "tap", "M4", [(x, y, t) for x in (-120.0, 60.0) for y in (yr - 25, yr + 25)], through=True,
            thread="through", note="X-LSQ075B base: PATTERN EST., drill to Zaber's drawing")
    pc.hole("E", "tap", "M3", [(x, 49.0, t) for x in (-130.0, -28.0, 74.0)], through=True, thread="through",
            note="stage-shield foot (MK-12)")
    pc.setup("-Z", face=(1, 1.35), label="bottom up: face, c'bores and drill every through hole",
             hold="plate in 6 in. vise jaws on the 260 mm blank's margins (or toe clamps), on parallels")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 10.0, rod hole, cut-out, outline through",
             hold="screwed to a sacrificial plate through holes A and B (8 screws), so the outline can go through")
    pc.tol += ["thickness 10.00 +-0.05; flatness 0.1 over the plate (it carries the stage and the well block)",
               "holes A, B, D located +-0.1 from the rod hole (datum)"]
    pc.changes += ["added: 4 M3 c'bored holes for the well-block standoffs, 4 M5 tapped for the rod gland at "
                   "(+-12.5, +-12.5), 4 M5 c'bored corner holes, 4 M4 for the X-LSQ075B (pattern est.), 3 M3 for the "
                   "shield foot", "cut-out corners R4 (model sharp): a 1/4 in. end mill leaves R3.2",
                   "10 mm from faced 1/2 in. plate; 3/8 in. (9.53) plate would skip the facing and could go to "
                   "SendCutSend: then deck_t = 9.525 in ft_model"]
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


def mk02_flange():
    pc = Piece("MK-02b", "MK-02", "Window retaining flange (beam-tube socket on top)", material="6061-T651", qty=1,
               route="CNC mill", state="S2", stock="1/4 in. 6061 plate (6.35) faced to 6.0 both sides, 106 x 106",
               stock_pn="1/4 in. 6061-T651 plate (PN not read)", blank=blank_box(-53, 53, -53, 53, -0.175, 6.175),
               pos="part z 0 = flange underside = ring top (world z 155.4 box / 282.8 cube)")
    t = 6.0
    pc.solid = cyl(50.0, 0, t)
    pc.bore("beam aperture", 22.0, 0, 0, t, 0, tool=2)
    pc.pocket("window recess (2.2 deep: window + 0.8 mm FKM cushion ring)", cyl(P["window_d"] / 2 + 0.25, -1, 2.2),
              (24.0, 0, 2.2), axis="+z", tool=3)
    pc.pocket("beam-tube socket 60.5 x 2", cyl(30.25, t - 2.0, t + 1), (28.0, 0, t - 2.0), tool=3)
    pc.hole("A", "csk", "M5", [(*polar(BC_R, 45 * k), t) for k in range(8)], through=True,
            note="M5 x 25 (box) / M5 x 20 (cube) flat-head ISO 10642, flush so the beam tube sits on the face")
    pc.hole("B", "tap", "M4", [(*polar(TIE_R, 22.5 + 90 * k), t) for k in range(4)], through=True, thread="through",
            note="beam-tube tie rods (M4 304 threaded rod)")
    pc.setup("-Z", face=(2, 1.75), label="bottom up: face, window recess")
    pc.setup("+Z", face=(2, t), outline=(2, -0.3), label="top up: face to 6.0, aperture, socket, holes, outline")
    pc.tol += ["recess depth 2.20 +0.05/0 (sets the cushion's squeeze)", "socket 60.50 +0.10/0"]
    pc.changes += ["recess 1.8 -> 2.2 mm deep: room for a 0.8 mm FKM cushion ring over the window (15 % squeeze)",
                   "the beam tube's bottom flange is merged into this flange: a 2 mm socket on its top holds the tube, "
                   "and four M4 tie rods from here to the lens collar hold the tube (no bonding, tube swappable)",
                   "added: 8 x M5 countersinks (flush), 4 x M4 tapped for the tie rods"]
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
    pcb.bore("aperture", 20.0, 0, 0, h, 0, tool=2)
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
                    "with an open 2.5D pocket and a plain cover, held by the same 3 x M4 screws"]
    pcc = Piece("MK-02e", "MK-02", "Cover-slide holder, cover", material="6061-T651", qty=1, route="CNC mill",
                state="S2", stock="3/16 in. 6061 plate faced to 4.4, 76 x 76", stock_pn="3/16 in. 6061 plate (PN not read)",
                blank=blank_box(-38, 38, -38, 38, 0.0, 4.76), pos="part z 0 = slide plane (stacks on the base)")
    hc = 4.4
    pcc.solid = cyl(35.0, 0, hc)
    pcc.bore("aperture", 20.0, 0, 0, hc, 0, tool=2)
    pcc.hole("A", "clear", "M4", [(*polar(30.0, a), hc) for a in (90, 180, 270)], through=True,
             note="M4 x 12 into MK-02c (box, + a 1 mm washer: see changes) or MK-13 (cube)")
    pcc.setup("+Z", face=(2, hc), outline=(2, -0.3), label="top up: face, aperture, holes, outline")
    pcc.changes += ["in the box the model leaves a 1 mm gap between holder and clamp ring (cs_top = roof_in - 6, "
                    "ring bottom = roof_in - 5): close it in ft_model or stack a 1 mm washer on each screw"]
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
    pc.hole("A", "plain", "6.40", [(-bw / 2, sy, bh / 2) for sy in (-30.0, 30.0)], axis="+x", depth=40.0,
            note="block heaters 1/4 x 1-1/2 in.: drill 6.40 (ream 6.35 +0.03 if the heater maker asks)")
    pc.hole("B", "plain", "2.0", [(-30.0, bd / 2, 10.0)], axis="-y", depth=31.0,
            note="block thermocouple, 1/16 in. sheath: 15 x D, parabolic drill, 0.5 mm pecks")
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
    pc.setup("-X", label="-X face up: heater holes", hold="vise on the faced Y faces")
    pc.setup("+Y", label="+Y face up: thermocouple hole", hold="vise on the X faces")
    pc.tol += ["bore 40.000 +0.025/0 (H7), cylindricity 0.01, Ra 0.8 um; perpendicular to the top face within 0.02",
               "top face (powder plane): flatness 0.02, Ra 0.8; height 40.00 +-0.02; bore edge sharp (0.1 max)",
               "heater holes 6.40 +0.05/0: a cartridge heater wants 0.05-0.1 mm diametral clearance"]
    pc.changes += ["block thermocouple hole moved from z 20 to z 10 and opened to 2.0 mm: at z 20 the model's hole "
                   "(x -30, along -y) runs straight through the y = +30 heater hole",
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
    pc = Piece("MK-04", "MK-04", "Heater plate", material="6061-T6511", qty=1, route="lathe + CNC mill", state="FT-0",
               stock="6061 round bar 1-3/4 in. (44.45) sawn 34 long",
               stock_pn="McMaster 1610T family (6061 rod, length chosen on the page; 1610T27 is the 3-1/4 in. size "
                        "in plate-materials.csv); 1-3/4 in. suffix not read",
               blank=blank_cyl(mm(1.75) / 2, -3.0, H + 3.0),
               pos="part z 0 = plate underside (world z -34 at the start of a build, box)")
    turned = cyl(D / 2, 0, H)
    rz0 = H - 7.0
    turned = turned.cut(ring(D / 2 + 1, D / 2 - P["rope"], rz0, rz0 + P["rope"]))
    turned = turned.cut(cyl(SOCKET_D / 2, -0.1, P["socket"]))
    turned = turned.cut(cq.Solid.makeCone(SOCKET_D / 2, 0, SOCKET_D / 2 / math.tan(math.radians(59)),
                                          V(0, 0, P["socket"]), V(0, 0, 1)))
    pc.solid = turned
    pc.pre = turned
    pc.hole("A", "plain", "6.40", [(*polar(P["heater_r"], a), 0.0) for a in (30.0, 150.0)], axis="+z",
            depth=P["heater_l"] + 0.5, note="plate heaters 1/4 x 1 in., leads out of the bottom")
    pc.hole("B", "plain", "2.0", [(*polar(P["heater_r"], 270.0), 0.0)], axis="+z", depth=P["heater_l"] + 0.5,
            note="plate thermocouple, 1/16 in. sheath (13 x D: parabolic drill)")
    pc.hole("C", "tap", "M2", [(*polar(17.1, 90 + 120 * k), H) for k in range(3)], depth=3.5, thread="3.0",
            note="substrate screws; 0.5 mm above the rope groove: do not deepen")
    pc.hole("D", "tap", "M3", [(D / 2, 0.0, 4.0)], axis="-x", depth=13.0, thread="9 (set screw M3 x 8 dog point, sunk "
                                                                                    "1 mm below the OD)",
            note="holds the rod: the dog point enters a 2.5 hole in the rod")
    pc.lathe_op("face, turn 39.80 x 30 (from 44.45)", face_min(44.45) + turn_min(44.45, D, 30))
    pc.lathe_op("rope groove 3 x 3 (3 mm grooving tool)", 1.2 * 3 / (0.05 * 1000) * 3)
    pc.lathe_op("drill 12 + bore the rod socket 12.95 x 8", drill_min(12.0, 10) + turn_min(12.0, SOCKET_D, 8))
    pc.lathe_op("part off; face to 28.00 in a soft-jaw second op", part_min(44.45) + face_min(D) + 3.0)
    pc.setup("-Z", label="bottom up in a 5C collet block: heater and thermocouple holes", hold="5C collet block")
    pc.setup("+Z", label="top up in the collet block: 3 x M2", hold="5C collet block")
    pc.setup("+X", label="collet block on its side: radial M3 set-screw hole", hold="5C collet block, side")
    pc.tol += ["OD 39.80 0/-0.025 (with the 40.000-40.025 bore: 0.200-0.250 mm diametral clearance)",
               "top face flatness 0.02, Ra 1.6; parallel to the bottom within 0.03; length 28.00 +-0.05",
               "rod socket 12.95 +0.05/0 x 8.0"]
    pc.changes += ["rod socket 12.80 -> 12.95: seamless 1/2 in. tube is 12.70 +-0.13 (ASTM A269), so 12.80 may "
                   "not take the rod; the rod is located by an M3 dog-point set screw instead of the fit",
                   "plate thermocouple hole 1.6 -> 2.0 (1/16 in. sheath)",
                   "added: 3 x M2 x 3 tapped for the substrate (3.0 thread leaves 0.5 mm above the rope groove; moving "
                   "the groove 2 mm down would allow a 1.5 x D thread)", "added: radial M3 set screw at z 4"]
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
               "Piston rod, %s (%.1f long)" % ("box" if which == "box" else "cube, 21 mm longer", ln),
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
    zt = ln
    win = box(-2.5, 2.5, -ro - 1, 0, zt - 19.0, zt - 9.0)
    pc.cut(win)
    pc.features.append(dict(kind="custom_slot", name="lead window 5 x 10 through one wall", axis="+y", tool=4,
                            center=[0.0, -ro, zt - 14.0], size=[5.0, 10.0], depth=P["rod_wall"] + 0.6))
    pc.hole("A", "plain", "2.5", [(ro, 0.0, zt - 4.0)], axis="-x", depth=P["rod_wall"] + 0.3,
            note="set-screw dimple, one wall", tool=T.drill_tool(2.5))
    pc.lathe_op("face both ends to length +-0.1, 0.5 x 15 deg lead-in chamfer at the top end",
                2 * face_min(12.7) + 3.0)
    pc.lathe_op("polish the OD (gland zone) to Ra <= 0.4 um, 320 then 600 grit", 6.0)
    pc.setup("-Y", label="in a V-block: lead window (1/8 in. end mill, through one wall)", hold="V-block")
    pc.setup("+X", label="turned 90 deg in the V-block: set-screw dimple", hold="V-block")
    pc.tol += ["OD 12.62-12.73 (0.497-0.501 in.), measured: ASTM A269 allows +-0.13, which takes the rod seal "
               "outside Parker's 10-17 % squeeze; gland zone polished to 16 RMS (Ra ~0.4 um; Parker 10-20 uin)", "length %.1f +-0.1; ends square within 0.05" % ln,
               "no weld seam: seamless tube only (a welded seam leaks past the rod seal)"]
    pc.changes += ["added: 5 x 10 lead window just under the plate (leads from the heaters into the rod); it stays "
                   "2.7 mm above the floor at the bottom of the stroke", "added: 2.5 dimple for the plate's set screw",
                   "the rod's lower end is potted (not a machining step)"]
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
    pc.hole("A", "cbore", "M5", [(sx, sy, 0.0) for sx in (-12.5, 12.5) for sy in (-12.5, 12.5)], axis="+z",
            through=True, note="M5 SHCS up through the floor into the deck (box M5 x 25, cube M5 x 45)")
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
    pc.changes += ["two internal rod grooves for AS568-112 (0.487 x 0.103 in.), 1.6 mm lands in the 12 mm plate",
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
    y0, y1 = hw / 2, yr - 16
    pc = Piece("MK-08d", "MK-08", "Hopper arm", material="6061-T6511", qty=1, route="CNC mill", state="FT-1",
               stock="6061 bar 3/8 x 3/4 in. sawn 60 long", stock_pn="6061 bar 3/8 x 3/4 in. (PN not read)",
               blank=blank_box(-9.53, 9.53, y0 - 2, y1 + 2, -0.76, 8.77),
               pos="part (x, y) = hopper frame; z 0 = arm underside (powder plane + 27)")
    pc.solid = box(-8, 8, y0, y1, 0, 8)
    pc.hole("A", "cbore", "M3", [(0.0, y1 - 4.0, 8.0)], through=True,
            note="to the bracket's notch")
    pc.hole("C", "tap", "M3", [(sx, y0, 4.0) for sx in (-4.0, 4.0)], axis="+y", depth=8.0, thread="6",
            note="hopper end wall")
    pc.setup("+Z", face=(2, 8.0), outline=(2, -0.3), label="top up: face, outline through (on parallels, tabs "
                                                             "kept by 0.3 skin), c'bores")
    pc.setup("-Z", face=(2, 0.0), label="bottom up: face to 8.0")
    pc.setup("-Y", label="hopper end up (vise): 2 x M3")
    pc.changes += ["added: 2 M3 c'bored into the bracket notch, 2 M3 tapped into the hopper's end wall; the vibration "
                   "motor is held by a cable tie or hose clamp (not machined)"]
    return pc


def mk08_bracket():
    yr = P["rc_y"]
    z_car = P["rc_h"] + P["rc_car"][2] - P["so_l"] - P["well"][2]      # carriage top, powder-plane frame: -9.7
    z_top = P["hopper"][2]                                            # arm top: +35
    pc = Piece("MK-08e", "MK-08", "Carriage bracket (L: 3 mm foot under the shield, 8 mm web)", material="6061-T6511",
               qty=1, route="CNC mill", state="FT-1", stock="6061 bar 2 x 2 in. (50.8) sawn 43 long",
               stock_pn="6061 square bar 2 in. (PN not read)",
               blank=blank_box(-21.5, 21.5, yr - 26.0, yr - 26.0 + 50.8, z_car - 3.0, z_car - 3.0 + 50.8),
               pos="part (x, y, z) = hopper frame: x about the hopper centre, z from the powder plane")
    web = box(-20, 20, yr - 24, yr - 16, z_car, z_top)
    foot = box(-20, 20, yr - 24, yr + 16, z_car, z_car + 3.0)
    s = web.fuse(foot).clean()
    rf = 6.5                         # inside corner = the 1/2 in. cutter's radius + 0.15
    s = s.fuse(box(-20, 20, yr - 16, yr - 16 + rf, z_car + 3.0, z_car + 3.0 + rf).cut(
        cylax(rf, (-21, yr - 16 + rf, z_car + 3.0 + rf), (1, 0, 0), 42)))
    pc.solid = s
    pc.pocket("arm notch 16 x 8", box(-8.05, 8.05, yr - 25, yr - 15, z_top - 8.0, z_top + 1), (5.0, yr - 20, z_top - 8.0),
              tool=3)
    pc.hole("A", "tap", "M3", [(0.0, yr - 20.0, z_top - 8.0)], depth=8.0, thread="6", note="arm screw")
    pc.hole("B", "csk", "M3", [(sx, yr + 8.0, z_car + 3.0) for sx in (-12.0, 12.0)], through=True,
            note="to the X-LSQ carriage: PATTERN EST., drill to Zaber's drawing; flat heads under the shield's 3 mm gap")
    pc.setup("+X", face=(2, 20.0), outline=(2, -19.0), label="L profile up (x up): face, outline of the L to x -19",
             hold="2 in. bar in the vise, 41 mm out")
    pc.setup("-X", face=(2, 20.0), outline=(2, 18.5), label="flip: face to 40.0 wide, last 1.5 mm of the outline")
    pc.setup("+Z", label="foot down on parallels: arm notch, M3, c'sinks", hold="vise on the web's y faces")
    pc.changes += ["the model's bracket is a plain plate standing on the carriage; it needs a foot to bolt down. The "
                   "shield leaves 3.0 mm over the carriage, so the foot is 3 mm thick with flat-head screws. A 4-6 mm "
                   "foot would be stiffer: raise the shield by 3 mm in ft_model to allow it",
                   "arm sits in a 16 x 8 notch in the web's top (the model's boxes overlap there)"]
    return pc


# ====================================================================================================================
# MK-09 scan-head plate and collimator saddle
# ====================================================================================================================
def mk09_plate():
    y1 = YC + 115 + 15
    pc = Piece("MK-09a", "MK-09", "Scan-head plate", material="6061-T651", qty=1, route="CNC mill", state="S1",
               stock="1/2 in. 6061-T651 plate, 210 x 275 from a 12 x 24 in. sheet; faced to 12.0",
               stock_pn="McMaster 89155K135 (second blank from the deck's sheet)",
               blank=blank_box(-105, 105, -95, y1 + 5, -0.35, 12.35),
               pos="part (x, y) = world (x, y); part z 0 = underside (world z 354 box, 375 cube)")
    t = 12.0
    pc.solid = rbox(-100, 100, -90, y1, 0, t, 5.0)
    pc.bore("lens opening 116", P["lens_d"] / 2 + 3, 0, 0, t, 0, tool=2)
    pc.hole("A", "clear", "M6", [(x, YC + 115, t) for x in (-60.0, 0.0, 60.0)], through=True,
            note="M6 x 20 up into drop-in T-nuts (McMaster 5278N47) in the cross-beam")
    pc.hole("B", "tap", "M5", [(sx * 65.0, sy * 55.0, t) for sx in (-1, 1) for sy in (-1, 1)], through=True,
            thread="through", note="hurrySCAN 25 base: PATTERN EST., drill to SCANLAB's drawing")
    pc.hole("C", "tap", "M5", [(-94.0, sy * 9.0, t) for sy in (-1, 1)], depth=10.0, thread="8",
            note="collimator saddle (MK-09b)")
    pc.setup("-Z", face=(1, 0.35 * 0 + 0.0), label="bottom up: face 0.35", hold="vise jaws on the blank's long edges")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 12.0, lens opening, holes, outline",
             hold="screwed down through holes B to a sacrificial plate")
    pc.tol += ["thickness 12.0 +-0.1; flatness 0.05 under the head", "lens opening 116 +0.5/0 (clearance only)"]
    pc.changes += ["added: 3 x M6 to the cross-beam's T-nuts, 4 x M5 for the head (pattern est.), 2 x M5 for the "
                   "saddle", "corners R5"]
    return pc


def mk09_saddle():
    zc = P["head_in_z"]
    rc = 20.0                       # collimator radius (envelope in ft_model: cyl(20))
    w_slot = 30.0                   # the collimator rests on the slot's two top edges
    z_top = zc - math.sqrt(rc ** 2 - (w_slot / 2) ** 2)        # 46.77: the edges at the contact height
    W = 44.0
    pc = Piece("MK-09b", "MK-09", "Collimator saddle", material="6061-T6511", qty=1, route="CNC mill", state="S1",
               stock="6061 bar 1-3/4 x 2 in. (44.45 x 50.8) sawn 88 long",
               stock_pn="6061 rectangular bar 1-3/4 x 2 in. (PN not read)",
               blank=blank_box(-174.0, -86.0, -22.225, 22.225, -2.0, 48.8),
               pos="part (x, y) = world (x, y); part z 0 = head-plate top (world z 366 box)")
    prof = cq.Workplane("XZ").polyline([(-88.0, 0.0), (-88.0, 12.0), (-100.0, 12.0), (-100.0, z_top), (-172.0, z_top),
                                        (-172.0, 0.0)]).close().extrude(W / 2, both=True).val()
    pc.solid = prof
    pc.pocket("collimator slot 30 wide x 8 deep along x (the collimator sits on its edges)",
              box(-173.0, -100.0, -w_slot / 2, w_slot / 2, z_top - 8.0, z_top + 1), (-136.0, 0.0, z_top - 8.0), tool=2,
              kind="adaptive")
    pc.hole("A", "cbore", "M5", [(-94.0, sy * 9.0, 12.0) for sy in (-1, 1)], through=True, note="to the head plate")
    pc.hole("B", "tap", "M4", [(x, sy * 18.5, z_top) for x in (-165.0, -107.0) for sy in (-1, 1)], depth=8.0,
            thread="6", note="strap over the collimator (est.)")
    pc.setup("+Y", face=(2, W / 2), outline=(2, -6.5), label="profile plane up (part +y): face, L outline to y -6.5",
             hold="vise, bar standing 44.45 tall")
    pc.setup("-Y", face=(2, W / 2), outline=(2, 6.0), label="flip: face to 44.0, rest of the L outline")
    pc.setup("+Z", label="slot up: collimator slot, holes A and B", hold="vise on the y faces")
    pc.tol += ["slot edges at z %.2f +-0.05 above the plate: they set the collimator axis at z %.1f" % (z_top, zc),
               "slot 30.00 +-0.05 wide, its edges broken 0.3 x 45 deg (line contact)"]
    pc.changes += ["new piece (the model has no saddle): an L bracket on the head plate's -x end; the Ø40 collimator "
                   "rests on the two edges of a 30 mm slot (2.5D from the top) instead of a round cradle along its "
                   "axis, which no 3-axis setup reaches; strap holes est."]
    return pc


# ====================================================================================================================
# MK-10 beam tubes and lens collar
# ====================================================================================================================
def beam_tube_len(L):
    z = L["roof_out"] if L["cube"] else L["roof_out"]
    z_flange_top = z + WR_H + 6.0
    col_z0 = L["lens_bot"] - 14.0
    return (col_z0 - 6.0 + 3.0) - (z_flange_top - 2.0)


def mk10_tube(which):
    L = L_BOX if which == "long" else L_CUBE
    ln = beam_tube_len(L)
    pc = Piece("MK-10" + ("a" if which == "long" else "b"), "MK-10",
               "Beam tube, %s (%.1f long)" % (which, ln), material="6061-T6 tube 2-3/8 x 0.125 in.", qty=1,
               route="saw + lathe", state="S2" if which == "long" else "FT-1V",
               stock="6061 round tube 60.3 x 3.18 wall (2-3/8 x 0.125 in.); if not stocked, 2-1/2 x 1/8 in. and "
                     "open the sockets to 63.6", stock_pn="6061 round tube (PN not read)",
               blank=blank_cyl(30.16, -2.0, ln + 2.0), pos="part z 0 = bottom end in the flange socket")
    pc.solid = ring(30.16, 27.0, 0, ln)
    pc.lathe_op("saw, face both ends to %.1f +-0.2, deburr" % ln, 2 * face_min(60.3, 54.0) + 4.0)
    pc.tol += ["length %.1f +-0.2 (the tie rods take up the rest); ends square within 0.2" % ln]
    pc.changes += ["tube clamped between the flange socket and the collar socket by 4 M4 tie rods instead of being "
                   "fused to a flange (model): light-tight, and the long tube swaps for the short one"]
    pc.finish = "black anodise inside (stray light) or as is"
    return pc


def mk10_collar():
    H = mm(1.25)
    pc = Piece("MK-10c", "MK-10", "Lens collar", material="6061-T651", qty=1, route="CNC mill", state="S2",
               stock="1-1/4 in. 6061 plate (31.75), 130 x 130", stock_pn="1-1/4 in. 6061-T651 plate (PN not read)",
               blank=blank_box(-65, 65, -65, 65, 0, H), pos="part z 0 = collar floor underside (world z 280 box)")
    ro, ri = 62.0, P["lens_d"] / 2 + 1.0
    pc.solid = cyl(ro, 0, H)
    pc.pocket("lens bore 112 x 25.75", cyl(ri, 6.0, H + 1), (ri - 6.0, 0, 6.0), tool=2, kind="pocket")
    pc.bore("tube bore 54", 27.0, 0, 0, 6.0, 0, axis="+z", tool=2)
    pc.pocket("tube socket 60.5 x 3", cyl(30.25, -1, 3.0), (29.0, 0, 3.0), axis="+z", tool=3)
    pc.hole("A", "clear", "M4", [(*polar(TIE_R, 22.5 + 90 * k), 6.0) for k in range(4)], through=True,
            note="tie rods; nuts inside the collar")
    pc.hole("B", "tap", "M3", [(ro, 0.0, z) for z in (13.0, 23.0)], axis="-x", depth=5.0, thread="4",
            note="beam-tube interlock switch (est.)")
    pc.setup("+Z", outline=(2, 1.0), label="open end up: outline, lens bore", hold="blank on parallels, toe clamps")
    pc.setup("-Z", outline=(2, -H - 0.3), label="floor up: tube bore, socket, tie-rod holes, rest of the outline",
             hold="soft jaws in the lens bore (ID clamp)")
    pc.setup("+X", label="on its side: 2 x M3 for the interlock switch", hold="vise, V-block")
    pc.tol += ["lens bore 112 +0.5/0 (lens envelope 110 est.: measure the lens first)", "socket 60.50 +0.10/0"]
    pc.changes += ["collar height 32 -> 31.75 (1-1/4 in. plate, wall 25.75): no effect on fit",
                   "added: 4 x M4 tie-rod holes, socket for the tube, 2 x M3 for the interlock switch (est.)",
                   "light seal: a felt or foam ring in the 1 mm gap round the lens (not machined)"]
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
    yr, rw = P["rc_y"], P["rc_w"]
    rl, ml = P["rc_rail_l"], P["rc_motor_l"]
    x0, x1 = -rl / 2 - ml - 2, rl / 2 + 2
    y0, y1 = yr - rw / 2 - 3, yr + rw / 2 + 3
    t = 0.91
    pc = Piece("MK-12", "MK-12", "Stage shield", material="304 sheet 0.036 in. (0.91)", qty=1,
               route="sheet: laser-cut and bent (SendCutSend)", state="FT-1",
               stock="SendCutSend 304 stainless, 0.036 in. class (their gauge list not read)",
               stock_pn="flat pattern out/dxf/MK-12.dxf",
               pos="part (x, y) = world (x, y); part z 0 = deck top")
    z_top = P["rc_h"] + P["rc_car"][2] + 3.0         # shield top underside above the deck
    top = box(x0, x1, y0, y1, z_top, z_top + t)
    top = top.cut(slot_xy(-rl / 2 + 2, rl / 2 - 2, yr - 26, yr - 14, z_top - 1, z_top + 2))
    skirt = box(x0, x1, y0 - 1.0, y0 - 1.0 + t, 0, z_top + t)
    foot = box(x0, x1, y0 - 11.0, y0 - 1.0, 0, t)
    s = top.fuse(skirt).fuse(foot)
    for x in (-130.0, -28.0, 74.0):
        s = s.cut(cyl(1.7, -1, 2, x, 49.0))
    pc.solid = s
    ba = bend_allowance(90, t=t, r=t)
    h_sk = z_top + t
    # flat: top (depth y1-y0) | bend | skirt (h) | bend | foot 10
    W = x1 - x0
    v_top = (y1 - y0) - t
    v_sk = h_sk - 2 * t
    pts = [(0, 0), (W, 0), (W, v_top + ba + v_sk + ba + 10.0 - t), (0, v_top + ba + v_sk + ba + 10.0 - t)]
    slot_v = (y1 - (yr - 14)) - t / 2
    pc.sheet = dict(thickness=t, k_factor=K_FACTOR, outline=[[round(a, 3), round(b, 3)] for a, b in pts],
                    slot=dict(u0=(-rl / 2 + 2) - x0, u1=(rl / 2 - 2) - x0, v0=slot_v, v1=slot_v + 12.0),
                    holes=[[x - x0, v_top + ba + v_sk + ba + 5.0, 3.4] for x in (-130.0, -28.0, 74.0)],
                    bends=[dict(line="top/skirt", v=round(v_top + ba / 2, 3), angle=90.0, inside_r=t,
                                allowance=round(ba, 3)),
                           dict(line="skirt/foot", v=round(v_top + ba + v_sk + ba / 2, 3), angle=90.0, inside_r=t,
                                allowance=round(ba, 3))])
    pc.tol += ["bends +-1 deg; slot 12 +-0.3 wide; holes +-0.2"]
    pc.changes += ["added: a 10 mm foot along the front skirt with 3 x 3.4 holes to the deck (M3)",
                   "slot ends full round (R6)"]
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
    pc = Piece("MK-13", "MK-13", "Cube top plate (Ideal Vacuum P108171 blank, bored for the window ring)",
               material="6061 (Ideal Vacuum blank)", qty=1, route="CNC mill", state="FT-1V",
               stock="Ideal Vacuum P108171 blank plate (E2)", stock_pn="Ideal Vacuum P108171 (parts.csv E2)",
               blank=blank_box(-150.9, 150.9, -150.9, 150.9, 0, pt), seal=True,
               pos="part z 0 = boss face (inside); window at part (x, y) = (-xc, -yc) = (28, -45)")
    s = iv_blank()
    pc.pre = s
    pc.solid = s
    wx, wy = -XC, -YC
    pc.pocket("spot face 104 x 0.3 for the window ring's O-ring (Ra 0.8)", cyl(52.0, pt - 0.3, pt + 1, wx, wy),
              (wx + 45.0, wy, pt - 0.3), tool=2)
    pc.bore("window bore 53", 26.5, wx, wy, pt, 0, tool=2)
    pc.hole("A", "tap", "M5", [(wx + c[0], wy + c[1], pt - 0.3) for c in [polar(BC_R, 45 * k) for k in range(8)]],
            depth=12.0, thread="10", note="window stack (blind: no leak path)")
    pc.hole("B", "tap", "M4", [(wx + c[0], wy + c[1], 0.0) for c in [polar(30.0, a) for a in (90, 180, 270)]],
            axis="+z", depth=10.0, thread="8", note="cover-slide holder, inside")
    pc.setup("+Z", label="outside face up: spot face, bore, 8 x M5", hold="toe clamps on the plate edge")
    pc.setup("-Z", label="boss face up: 3 x M4", hold="toe clamps; the boss on parallels")
    pc.tol += ["spot face 104 x 0.3: flatness 0.02, Ra 0.4 um (window ring's AS568-140 seal)",
               "bore 53 +0.2/0, true position 0.2 to the plate centre; the plate's own O-ring face untouched"]
    pc.changes += ["added: 104 mm spot face for the ring's face seal, 8 x M5 blind (no through holes in the vacuum "
                   "wall), 3 x M4 blind inside for the cover-slide holder"]
    return pc


def mk14():
    pt = P["cube_plate_t"]
    pc = Piece("MK-14", "MK-14", "Cube bottom plate (P108171 blank, bored for the rod gland)",
               material="6061 (Ideal Vacuum blank)", qty=1, route="CNC mill", state="FT-1V",
               stock="Ideal Vacuum P108171 blank plate (E2)", stock_pn="Ideal Vacuum P108171 (parts.csv E2)",
               blank=blank_box(-150.9, 150.9, -150.9, 150.9, 0, pt), seal=True,
               pos="part z 0 = boss face (inside, the deck sits on it); rod at part (x, y) = (-xc, -yc)")
    s = iv_blank()
    pc.pre = s
    pc.solid = s
    rx, ry = -XC, -YC
    pc.bore("rod hole 20", 10.0, rx, ry, 0.0, pt, axis="+z", tool=3)
    pc.pocket("spot face 56 x 0.3 for the gland's AS568-031 (Ra 0.8)", cyl(28.0, pt - 0.3, pt + 1, rx, ry),
              (rx + 24.0, ry, pt - 0.3), axis="-z", tool=3)
    pc.hole("A", "clear", "M5", [(rx + sx, ry + sy, pt - 0.3) for sx in (-12.5, 12.5) for sy in (-12.5, 12.5)],
            through=True, note="gland screws into the deck, inside the gland's face seal")
    pc.hole("B", "tap", "M5", [(sx * 115.0, sy * 115.0, 0.0) for sx in (-1, 1) for sy in (-1, 1)], axis="+z", depth=12.0, thread="10", note="deck corners (blind)")
    pc.setup("+Z", label="outside face up: spot face, gland holes", hold="toe clamps on the plate edge")
    pc.setup("-Z", label="boss face up: rod hole, deck-corner taps", hold="toe clamps; the boss on parallels")
    pc.tol += ["spot face 56 x 0.3: flatness 0.02, Ra 0.4 um", "holes A +-0.1 to the rod hole"]
    pc.changes += ["added: 56 mm spot face, 4 x 5.5 gland holes inside the gland's seal, 4 x M5 blind at the deck "
                   "corners (+-115 from the cube centre)"]
    # the rod hole sits at the world origin; deck corners about the cube centre (part 0, 0)
    return pc


# ====================================================================================================================
# MK-15 stage bracket plate, riser, rod clamp
# ====================================================================================================================
def mk15_plate():
    h = 15.0
    ry0, ry1 = YC - 115, YC + 115
    pc = Piece("MK-15a", "MK-15", "Piston-stage bracket plate", material="6061-T651", qty=1, route="CNC mill",
               state="FT-1", stock="1/2 in. 6061-T651 plate, 190 x 270, faced to 10.0",
               stock_pn="McMaster 89155K135 (second sheet)", blank=blank_box(-95, 95, ry0 - h - 5, ry1 + h + 5, -1.35, 11.35),
               pos="part (x, y) = world (x, y); part z 0 = underside, on the base rails (world z -222.6)")
    t = 10.0
    pc.solid = rbox(-90, 90, ry0 - h, ry1 + h, 0, t, 5.0)
    pc.hole("A", "clear", "M6", [(sx * 60.0, y, t) for sx in (-1, 1) for y in (ry0, ry1)], through=True,
            note="M6 x 16 into drop-in T-nuts (5278N47) in the base rails")
    pc.hole("B", "cbore", "M5", [(sx * 50.0, sy * 30.0, 0.0) for sx in (-1, 1) for sy in (-1, 1)], axis="+z",
            through=True, note="riser screws from below")
    pc.setup("-Z", face=(1, 1.35), label="bottom up: face, c'bores, drill through")
    pc.setup("+Z", face=(1, t), outline=(2, -0.3), label="top up: face to 10, outline", hold="screwed down through A")
    pc.changes += ["added: 4 x M6 to the base rails, 4 x M5 c'bored for the riser"]
    return pc


def mk15_riser():
    fx, fy = P["vs_foot"]
    pc = Piece("MK-15b", "MK-15", "Piston-stage riser", material="6061-T651", qty=1, route="CNC mill", state="FT-1",
               stock="5/8 in. 6061 plate (15.88), 126 x 86, faced to 15.0", stock_pn="5/8 in. 6061 plate (PN not read)",
               blank=blank_box(-63, 63, -43, 43, -0.44, 15.44),
               pos="part z 0 = underside (world z -212.6)")
    h = 15.0
    pc.solid = box(-fx / 2, fx / 2, -fy / 2, fy / 2, 0, h)
    pc.hole("A", "tap", "M5", [(sx * 50.0, sy * 30.0, 0.0) for sx in (-1, 1) for sy in (-1, 1)], axis="+z", depth=10.0,
            thread="8", note="from the bracket plate")
    pc.hole("B", "tap", "M6", [(sx * 40.0, sy * 20.0, h) for sx in (-1, 1) for sy in (-1, 1)], through=True,
            thread="through", note="X-VSR20A base: PATTERN EST., drill to Zaber's drawing")
    pc.setup("+Z", face=(2, h), outline=(2, 1.0), label="top up: face, outline, stage holes")
    pc.setup("-Z", face=(2, 0.0), outline=(2, -h - 0.3), label="bottom up: face to 15, riser taps")
    pc.changes += ["added: 4 x M5 from the plate, 4 x M6 for the stage (pattern est.)"]
    return pc


def mk15_clamp():
    ch = P["clamp_h"]
    pc = Piece("MK-15c", "MK-15", "Rod clamp (split)", material="6061-T6511", qty=1, route="CNC mill + saw slit",
               state="FT-1", stock="6061 bar 1-1/4 in. square (31.75) sawn 28 long",
               stock_pn="6061 square bar 1-1/4 in. (PN not read)", blank=blank_box(-15.9, 15.9, -15.9, 15.9, -1.5, 26.5),
               pos="part z 0 = clamp underside on the X-VSR20A platform")
    pc.solid = box(-15, 15, -15, 15, 0, ch)
    pc.bore("rod bore 12.95", THROAT / 2, 0, 0, ch, 0, tool=3)
    pc.pocket("lead exit 6 x 6 toward -y", box(-3, 3, -16, 0, -1, 6.0), (0, -11.0, 6.0), axis="+z", tool=4,
              kind="adaptive")
    pc.manual.append(("slit 1.5 wide from the bore to +y, full height (slitting saw or bandsaw)", 10.0))
    pc.hole("A", "cbore", "M4", [(sx * 10.5, -10.5, ch) for sx in (-1, 1)], through=True, note="to the stage platform "
                                                                                              "(pattern est.)")
    pc.hole("B", "cbore", "M3", [(-15.0, 10.75, z) for z in (8.0, 18.0)], axis="+x", through=True,
            note="clamp screws across the slit; the far half is tapped M3 by hand after drilling 2.5")
    pc.cam_solid = pc.solid
    pc.cut(box(-0.75, 0.75, 0, 16, -1, ch + 1))
    pc.setup("+Z", face=(2, ch), outline=(2, 1.0), label="top up: face, outline, rod bore, c'bores")
    pc.setup("-Z", face=(2, 0.0), outline=(2, -ch - 0.3), label="bottom up: face to 25, lead exit")
    pc.setup("-X", label="-X face up: clamp-screw holes", hold="vise on the y faces")
    pc.tol += ["rod bore 12.95 +0.05/0, perpendicular to the base within 0.02 (the rod must run true in the gland)"]
    pc.changes += ["slit 4 -> 1.5 mm and through the full height, two M3 clamp screws (the model's 8 mm tall slit "
                   "would not close)", "added: 6 x 6 lead exit at the bottom (the rod's leads leave here)",
                   "added: 2 x M4 to the platform (pattern est.)"]
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
    pcs = [mk01(), mk02_ring(), mk02_flange(), mk02_clamp(), *mk02_holder(), *mk03(), mk04(), mk05(), mk06("box"),
           mk06("cube"), mk07(), *mk08_hopper(), mk08_clamp(), mk08_arm(), mk08_bracket(), mk09_plate(), mk09_saddle(),
           mk10_tube("long"), mk10_tube("short"), mk10_collar(), mk11_nozzle(), mk11_collector(), mk12(), mk13(), mk14(),
           mk15_plate(), mk15_riser(), mk15_clamp(), mk16(), mk17_buy(), *mk18()]
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
