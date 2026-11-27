"""Lathe CAM for the cup's turned parts, with a 2D stock-removal simulation of every program.

    python cam/lathe_cam.py          # writes cam/gcode/*.nc, cam/out/lathe_sim.json and cam/out/lathe_*.png

Parts (sizes from ../params.py):
  B_bottom_disc  316L, option B's welded floor: OD = the body tube's OD, 1 x 45 deg weld-prep chamfer
  B_puck, A_puck 304 catch pucks
  B_liner        304 tube cut to length: face both ends, chamfer
  B_body_tube    316L 3 in tube: face both ends square for the welds
  C_sleeve       304 entrance sleeve with a lip (option C); turned lip-end first, in the chuck
  C_spacer       316L valve-delete spacer (option C); the tie-rod holes are drilled on the mill (mill_cam.py)

Programs are Haas-style lathe code (G18, X in diameter, G96 constant surface speed with a G50 limit,
G99 feed per rev, G40: the programmed point is the tool's nose centre, so no nose-radius compensation).
Roughing is written out as G1 passes rather than G71 so the simulation runs the exact moves.

Setup 1 holds the part's bottom end (z < 0 in the part frame) and works on the top face, the bore and
the OD from the free end. Setup 2 holds the finished OD in soft jaws and works on the bottom face from
below: face to length, chamfer, and any face groove.

Simulation: the stock is a raster in the (r, z) half-plane, 0.05 mm cells. Each tool removes its nose
circle plus its body on the side it is held from (an OD tool: everything further out and further from
the work face than the nose centre, within a band of the nose width; a boring bar: further in; a
parting blade: further out within its width; a face-grooving blade: further from the face within its
width). So a move that would need an undercut shows up as a gouge, and a rapid that passes through
material shows up as a crash. At the end: gouge = target material removed (deeper than one 0.05 mm cell),
leftover = extra material thicker than 0.06 mm. The bar remnant below the parting cut is ignored.
"""

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from shapely.geometry import LineString, Polygon

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "cad"))
import params as P  # noqa: E402

OUT = HERE / "out"
GC = HERE / "gcode"
OUT.mkdir(exist_ok=True)
GC.mkdir(exist_ok=True)
RES = 0.05
INCH = 25.4


@dataclass
class Tool:
    num: int
    name: str
    nose_r: float = 0.4
    width: float = 0.0
    vc: float = 90.0             # m/min
    f: float = 0.15              # mm/rev
    doc: float = 1.0             # radial depth per roughing pass
    side: str = "od"             # od | bore | part | fgroove | drill


TOOLS = {
    "rough": Tool(1, "CNMG 432 (0.8 mm nose), 95 deg, rough OD/face", 0.8, vc=90, f=0.20, doc=1.5),
    "finish": Tool(2, "VNMG 331 (0.4 mm nose), 93 deg, finish OD/face/chamfers", 0.4, vc=120, f=0.08, doc=0.3),
    "bore": Tool(3, "boring bar 16 mm, CCMT 21.51 (0.4 mm nose)", 0.4, vc=80, f=0.10, doc=1.0, side="bore"),
    "part": Tool(4, "parting blade 3 mm (GTN-3)", 0.2, width=3.0, vc=60, f=0.05, side="part"),
    "drill": Tool(5, "25 mm drill (spot first), centre", 0.0, vc=20, f=0.10, side="drill"),
    "fgroove": Tool(6, "face-grooving tool 3 mm, dia range 40-110", 0.2, width=3.0, vc=50, f=0.03, side="fgroove"),
}


@dataclass
class Part:
    name: str
    material: str
    stock: tuple                 # (r_in, r_out, z0, z1); z0 inside the chuck side, z1 the free end
    section: list                # target half-section polygon, part frame, setup-1 orientation
    ops: list = field(default_factory=list)
    note: str = ""
    blind_z: float = None        # a blind pocket: drill only to this z (part frame) and part off through the centre
    drill_r: float = None        # drill radius for a blind pocket


def liner_length_b():
    """From the puck's top to 3 mm below the reducer's tangent (or, split, below the pot's ferrule face)."""
    b = P.B
    from_floor = b["bottom_t"] + b["puck_h"]
    if b.get("split"):
        to_face = b["stub_len"] + b["reducer_len"] + b["ferrule_len"] + b["gasket_t"]
        return round(b["body_len"] - from_floor - to_face - 3.0 - 0.2, 1)
    z_red_top_tangent = b["stub_len"] + b["reducer_len"] - 8.0
    return round(b["body_len"] - from_floor - z_red_top_tangent - 3.0 - 0.2, 1)


def body_tube_length_b():
    """From the reducer's 3 in end (or, split, from the pot's ferrule) to the end cap's rim."""
    b = P.B
    L = b["body_len"] - b["stub_len"] - b["reducer_len"] - b["bottom_t"] - b.get("bottom_rim", 0.0)
    if b.get("split"):
        L -= 2 * b["ferrule_len"] + b["gasket_t"]
    return round(L, 2)


def parts():
    b, a, c, s = P.B, P.A, P.C, P.STOCK
    out = []
    R, t = b["body_od"] / 2, b["bottom_t"]
    Ri, fr, H = R - b["body_wall"], b["bottom_fillet"], b["bottom_t"] + b["bottom_rim"]
    arc = [(Ri - fr + fr * math.cos(math.radians(a)), t + fr + fr * math.sin(math.radians(a)))
           for a in np.linspace(0, -90, 10)]
    out.append(Part("B_bottom_cap", "316L", (0, 3.25 * INCH / 2, -10.0, H + 1.0),
                    [(0, 0), (R - 0.5, 0), (R, 0.5), (R, H), (Ri, H)] + arc + [(0, t)],
                    ops=["face", "drill", "bore", "rough_od", "finish_od", "part", "op2_face", "op2_chamfer"],
                    blind_z=t + 1.5, drill_r=12.5,
                    note="3-1/4 in. 316/316L bar. An end cap: 8 mm floor, 12 mm rim the tube's wall (W3 is a square butt "
                         "weld 20 mm up), R6 inside corner (no sharp welded corner where the floor's thermal stress peaks)."))
    for tag, d in (("B", b), ("A", a)):
        R, h, cf = d["puck_d"] / 2, d["puck_h"], d["puck_chamfer"]
        cb = d.get("puck_chamfer_bottom", cf)          # B: 6 x 45 deg underneath, to clear the cap's R6 corner
        bar = (3.0 if R * 2 > 50 else 2.0) * INCH / 2
        out.append(Part(f"{tag}_puck", "304", (0, bar, -10.0, h + 1.0),
                        [(0, 0), (R - cb, 0), (R, cb), (R, h - cf), (R - cf, h), (0, h)],
                        ops=["face", "rough_od", "finish_od", "part", "op2_face", "op2_chamfer"],
                        note=f"{bar * 2 / INCH:.0f} in. 304 bar. Sits loose on the floor; the liner stands on it."))
    if b.get("liner", True):
        ro, ri = b["liner_od"] / 2, b["liner_od"] / 2 - b["liner_wall"]
        L = liner_length_b()
        out.append(Part("B_liner", "304", (ri, ro, -12.0, L + 1.5),
                        [(ri, 0), (ro - 0.3, 0), (ro, 0.3), (ro, L - 0.3), (ro - 0.3, L), (ri, L)],
                        ops=["face", "finish_od_top", "op2_face", "op2_chamfer"],
                        note=f"2-3/4 in. x 0.065 in. 304 tube (McMaster 11116N864), sawn to {L + 3:.0f} mm and faced to {L:.1f} mm; "
                             "held on its OD in a collet or soft jaws with 12 mm out. Deburr the bore by hand."))
    ro, ri = b["body_od"] / 2, b["body_od"] / 2 - b["body_wall"]
    Lb = body_tube_length_b()
    out.append(Part("B_body_tube", "316L", (ri, ro, -12.0, Lb + 1.5), [(ri, 0), (ro, 0), (ro, Lb), (ri, Lb)],
                    ops=["face", "op2_face"],
                    note=f"3 in. x 0.065 in. 316/316L tube, sawn to {Lb + 3:.0f} mm and faced square to {Lb:.1f} mm "
                         "(weld ends square and burr-free, no gap). Spider or plug in the bore against chatter."))
    # B' (next step): the turned KF-50 to 3 in adapter. Part frame: KF face at z = 0 (chuck side in setup 1), tri-clamp
    # face at the free end, so the 72.9 bore, the 45 deg cone and the 47.5 bore are all bored from the TC end.
    import parts as PT
    up, _, _, za = PT.b_adapter_profiles(recess=True)
    top = za["top"]
    sec_a = [(round(r, 4), round(top - zz, 4)) for r, zz in up][::-1]
    Ha = max(zz for _, zz in sec_a)
    out.append(Part("B_adapter", "316L", (0, 4.0 * INCH / 2, -10.0, Ha + 1.0), sec_a,
                    ops=["face", "drill", "bore", "rough_od", "finish_od", "groove_od", "part", "op2_face",
                         "op2_bore_chamfer"],
                    note="4 in. 316/316L bar. B' upper part (concept, sheet 5): TC end first, then the KF face and its "
                         "centring-ring recess on soft jaws. Copy the TC face's gasket groove from a bought ferrule."))
    lip_t, so, sl, sw, sL = 3.0, c["sleeve_od"] / 2, c["sleeve_lip_od"] / 2, c["sleeve_wall"], c["sleeve_len"]
    si = so - sw
    # machined lip-end down (in the chuck side), so the OD steps down toward the free end
    out.append(Part("C_sleeve", "304", (0, 2.75 * INCH / 2, -10.0, sL + 1.0),
                    [(si, 0), (sl - 0.3, 0), (sl, 0.3), (sl, lip_t), (so, lip_t), (so, sL - 0.3), (so - 0.3, sL),
                     (si, sL)],
                    ops=["face", "drill", "bore", "rough_od", "finish_od", "part", "op2_face", "op2_chamfer"],
                    note="2-3/4 in. 304 bar, turned lip-end first (the lip sits toward the chuck). Hangs lip up."))
    Ro, H = s["valve_body_od"] / 2, s["valve_body_h"]
    rb, rc = c["sleeve_od"] / 2 + 0.4, c["sleeve_lip_od"] / 2 + 0.4
    g_out, g_in = s["glass_od"] / 2 + 1.5, s["glass_od"] / 2 - s["glass_wall"] - 1.5
    gd = s["seal_groove_d"]
    out.append(Part("C_spacer", "316L", (0, (s["valve_body_od"] + 8) / 2, -10.0, H + 1.0),
                    [(rb, 0.5), (rb + 0.5, 0), (g_in, 0), (g_in, gd), (g_out, gd), (g_out, 0), (Ro - 1.0, 0),
                     (Ro, 1.0), (Ro, H - 1.0), (Ro - 1.0, H), (rc, H), (rc, H - lip_t), (rb, H - lip_t)],
                    ops=["face", "drill", "bore", "rough_od", "finish_od", "part", "op2_face", "op2_chamfer",
                         "op2_bore_chamfer", "op2_groove"],
                    note="Valve-delete spacer: the stock valve body's height, OD and tie-rod pattern (measure first). "
                         "Bottom-face groove for the glass and its gasket. Tie-rod holes on the mill."))
    return out


# --------------------------------------------------------------------------------- geometry helpers
def envelope(poly, z, outer=True):
    """Largest (outer) or smallest (inner) r of a shapely polygon at height z, or None."""
    minx, miny, maxx, maxy = poly.bounds
    if z < miny or z > maxy:
        return None
    seg = poly.intersection(LineString([(-1, z), (maxx + 10, z)]))
    if seg.is_empty:
        return None
    xs = []
    for g in getattr(seg, "geoms", [seg]):
        xs += [p[0] for p in g.coords]
    return max(xs) if outer else min(xs)


def nose_path(section, rn, z_from, z_to, outer=True, step=0.1):
    """Nose-centre path along the outer (or inner) side of the section, buffered by the nose radius."""
    poly = Polygon(section).buffer(rn, quad_segs=24)
    zs = np.arange(z_from, z_to - 1e-9 if z_to < z_from else z_to + 1e-9, -step if z_to < z_from else step)
    pts = []
    for z in zs:
        r = envelope(poly, z, outer)
        if r is not None:
            pts.append((round(r, 4), round(float(z), 4)))
    return pts


# ---------------------------------------------------------------------------------------- programs
def flat_comments(line):
    """G-code comments do not nest: a "(" inside a comment ends it at the first ")" and the rest of the text is
    read as words. Keep the outer parentheses and turn any inner ones into brackets (found by the milling
    check in mill_cam.py, where a nested comment made CAMotics skip a tool change)."""
    i = line.find("(")
    j = line.rfind(")")
    if i < 0 or j <= i:
        return line
    inner = line[i + 1:j].replace("(", "[").replace(")", "]")
    return line[:i + 1] + inner + line[j:]


class Prog:
    def __init__(self, part, setup, flip=False):
        self.part, self.setup, self.flip = part, setup, flip
        self.lines, self.moves, self.pos, self.tool = [], [], None, None

    def header(self):
        p = self.part
        z0txt = "the top face" if not self.flip else "the bottom face (part flipped)"
        self.lines += ["%", f"O{(sum(map(ord, p.name + self.setup)) % 8000) + 1000:04d} ({p.name}, {self.setup})",
                       f"({p.material}; blank r {p.stock[0]:.2f}-{p.stock[1]:.2f} mm; Z0 = {z0txt})",
                       "G21 G18 G40 G80 G99", "G50 S2000"]

    def use(self, key):
        t = TOOLS[key]
        if self.pos is not None:      # leave the work along the clearance radius before the tool change
            r_c = self.clear if TOOLS[self.tool].side != "bore" else min(self.pos[0], 1.0)
            if TOOLS[self.tool].side == "bore":
                self.g0(r_c, self.pos[1])
                self.g0(r_c, self.z_safe)
            else:
                self.g0(r_c, self.pos[1])
                self.g0(r_c, self.z_safe)
            self.g0(self.clear, self.z_safe)
        self.tool = key
        self.lines += ["G28 U0. W0.", f"T{t.num:02d}{t.num:02d} ({t.name})",
                       f"G96 S{t.vc:.0f} M03" if key != "drill" else "G97 S300 M03", "M08"]

    def zp(self, z):
        """part frame -> program frame (setup 2 mirrors z about the bottom face)."""
        return -z if self.flip else z - self.top

    def g0(self, r, z):
        if self.pos is not None:
            self.moves.append(("G0", self.tool, self.pos, (r, z), 0.0, 0.0))
        self.lines.append(f"G00 X{2 * r:.3f} Z{self.zp(z):.3f}")
        self.pos = (r, z)

    def g1(self, r, z, f=None):
        t = TOOLS[self.tool]
        f = f or t.f
        self.moves.append(("G1", self.tool, self.pos, (r, z), f, t.vc))
        self.lines.append(f"G01 X{2 * r:.3f} Z{self.zp(z):.3f} F{f:.3f}")
        self.pos = (r, z)

    def end(self):
        self.lines += ["M09", "G28 U0. W0.", "M05", "M30", "%"]


def gen(part):
    r_in, R, z0, z1 = part.stock
    sec = part.section
    poly = Polygon(sec)
    zmin, zmax = poly.bounds[1], poly.bounds[3]
    r_out_max = poly.bounds[2]
    r_bore_min = min(r for r, _ in sec)
    clear = R + 3.0
    progs = []
    p = Prog(part, "setup 1")
    p.top = zmax
    p.clear, p.z_safe = clear, zmax + 5.0
    p.header()
    # facing: rough to +0.25, finish to size
    tr, tf = TOOLS["rough"], TOOLS["finish"]
    x_in = (r_in - 0.6) if r_in > 0 else -0.6
    if "face" in part.ops:
        p.use("rough")
        for zf in list(np.arange(z1 - 1.0, zmax + 0.25, -1.0)) + [zmax + 0.25]:
            p.g0(clear, zf + tr.nose_r)
            p.g1(x_in, zf + tr.nose_r)
            p.g0(x_in, zf + tr.nose_r + 1.0)
            p.g0(clear, zf + tr.nose_r + 1.0)
        p.use("finish")
        p.g0(clear, zmax + tf.nose_r)
        p.g1(x_in, zmax + tf.nose_r)
        p.g0(x_in, zmax + 2.0)
    r_hole = r_in
    if "drill" in part.ops and r_in == 0:
        p.use("drill")
        dd = part.drill_r if part.drill_r else min(r_bore_min - 1.5, 12.5)
        z_end = part.blind_z if part.blind_z is not None else zmin - 2.5
        p.lines.append(f"(drill Ø{2 * dd:.1f} {'to z %.1f' % z_end if part.blind_z is not None else 'through'}, "
                       f"5 mm pecks; spot drill first)")
        p.g0(0, zmax + 3)
        zd = zmax
        while zd > z_end:
            zd = max(zd - 5.0, z_end)
            p.g1(0, zd, 0.10)
            p.g0(0, zmax + 3)
        p.moves.append(("DRILL", "drill", (0, zmax + 3), (dd, z_end), 0.10, 20))
        r_hole = dd
    if "bore" in part.ops:
        tb = TOOLS["bore"]
        p.use("bore")
        inner = Polygon(sec).buffer(tb.nose_r, quad_segs=24)
        r_cur = r_hole
        while True:
            r_next = r_cur + tb.doc
            rc = r_next - tb.nose_r
            # run down from the top while the bore's inner envelope (finish allowance 0.2) stays outside rc
            z_stop = zmin - 1.0
            for z in np.arange(zmax + 1.0, zmin - 1.0, -0.1):
                env = envelope(inner, z, outer=False)
                if env is not None and env - 0.2 < rc:
                    z_stop = z + 0.2
                    break
            if z_stop >= zmax:
                break
            p.g0(rc - 0.6 if rc > 1 else 0.3, zmax + 2.0)
            p.g0(rc, zmax + 2.0)
            p.g1(rc, z_stop)
            p.g1(rc - 0.4, z_stop + 0.4)
            p.g0(rc - 0.4, zmax + 2.0)
            r_cur = r_next
        path = nose_path(sec, tb.nose_r, zmax + tb.nose_r + 0.3, zmin - 0.5, outer=False)
        path = [q for q in path if q[1] >= zmin - tb.nose_r - 0.5]
        r_lo, keep = path[0][0] if path else 0, []
        for r_, z_ in path:
            if r_ > r_lo + 0.02 and z_ < zmax - 1.0:
                break                          # the bore widens toward the chuck: a back-cut, done in setup 2
            r_lo = min(r_lo, r_)
            keep.append((r_, z_))
        path = keep
        if path:
            p.g0(path[0][0] - 0.5, zmax + 2.0)
            p.g0(path[0][0], zmax + 2.0)
            p.g1(path[0][0], path[0][1], 0.2)
            for r_, z_ in path:
                p.g1(r_, z_, 0.08)
            p.g1(path[-1][0] - 0.4, path[-1][1] + 0.4, 0.08)
            p.g0(path[-1][0] - 0.4, zmax + 2.0)
    z_od_end = zmin - TOOLS["part"].width - 0.8 if "part" in part.ops else zmin
    if "rough_od" in part.ops:
        p.use("rough")
        outer = Polygon(sec).buffer(tr.nose_r + 0.3, quad_segs=24)   # 0.3 mm finish allowance
        r_cur = R
        while r_cur > r_bore_min:
            r_next = r_cur - tr.doc
            rc = r_next + tr.nose_r
            z_stop = z_od_end
            for z in np.arange(zmax + 1.0, z_od_end, -0.1):
                env = envelope(outer, z, outer=True)
                if env is not None and env > rc:
                    z_stop = z + 0.1
                    break
            if z_stop >= zmax + 0.5:
                break
            p.g0(clear, zmax + 2.0)
            p.g0(rc, zmax + 2.0)
            p.g1(rc, z_stop)
            p.g1(rc + 0.6, z_stop + 0.6)
            p.g0(clear, z_stop + 0.6)
            r_cur = r_next
    if "finish_od" in part.ops or "finish_od_top" in part.ops:
        p.use("finish")
        z_end = (zmax - 3.0) if "finish_od_top" in part.ops else (zmin - 0.8 if "part" in part.ops else zmin)
        path = nose_path(sec, tf.nose_r, zmax + tf.nose_r, z_end)
        # an edge that faces the chuck (r shrinking as z goes down) can't be cut from the free end: stop at it
        # and leave it to setup 2. Small dips under 0.02 mm are the buffer's rounding, not an edge.
        r_hi = path[0][0]
        cut = []
        for r_, z_ in path:
            if r_ < r_hi - 0.02 and z_ < zmax - 1.0:
                break
            r_hi = max(r_hi, r_)
            cut.append((r_, z_))
        path = cut
        p.g0(path[0][0], zmax + 2.0)
        for r_, z_ in path:
            p.g1(r_, z_)
        p.g1(path[-1][0] + 0.5, path[-1][1], 0.2)
        p.g0(clear, path[-1][1])
    if "groove_od" in part.ops:
        # Between two flanges (edges facing each other): plunge-rough with the 3 mm blade, then trace the profile.
        # At each blade position the tip goes to the highest point of the section (plus the nose radius) under the
        # blade's whole width, so the blade never enters the part, and on a wall that leans away from the groove
        # one of its corners follows the wall.
        tp = TOOLS["part"]
        p.use("part")
        # the section's outer edge as r(z), sampled finely and at every vertex (a steep flange back changes r by
        # ~4 mm per mm of z, so coarse samples would miss its corners)
        zs_env = np.unique(np.r_[np.arange(zmin, zmax, 0.005), [z for _, z in sec], zmax])
        rs_env = np.array([envelope(poly, z, outer=True) or 0.0 for z in zs_env])

        def tip_r(zc, allow=0.0):
            m = (zs_env >= zc - tp.width / 2 - 1e-9) & (zs_env <= zc + tp.width / 2 + 1e-9)
            return (float(rs_env[m].max()) if m.any() else r_hole) + tp.nose_r + allow
        zc_hi, zc_lo = zmax - tp.width / 2, zmin + tp.width / 2
        p.lines.append(f"(groove between the flanges, z {zmin:.1f} to {zmax:.1f}: plunges every "
                       f"{0.8 * tp.width:.1f} mm leaving 0.3, then the profile at 0.05 mm steps)")
        for zc in list(np.arange(zc_hi, zc_lo, -0.8 * tp.width)) + [zc_lo]:
            p.g0(clear, zc)
            p.g1(tip_r(zc, 0.3), zc, tp.f)
            p.g0(clear, zc)
        prof = [(tip_r(zc), zc) for zc in np.arange(zc_hi, zc_lo - 1e-9, -0.05)]
        p.g0(clear, zc_hi)
        p.g1(prof[0][0], zc_hi, tp.f)
        for r_, z_ in prof:
            p.g1(r_, z_, 0.04)
        p.g0(clear, prof[-1][1])
    if "part" in part.ops:
        p.use("part")
        tp = TOOLS["part"]
        zc = zmin - tp.width / 2 - 0.3
        r_stop = -0.3 if (part.blind_z is not None or r_hole <= 0) else r_hole - 0.5
        p.g0(clear, zc)
        p.g1(r_stop, zc, tp.f)
        p.g0(clear, zc)
    p.end()
    progs.append(p)
    # ------------------------------------------------------------------- setup 2: the bottom face
    q = Prog(part, "setup 2 (flipped)", flip=True)
    q.top = zmax
    q.clear, q.z_safe = clear, zmin - 5.0
    q.header()
    q.use("finish")
    x_in2 = (r_bore_min - 0.6) if r_bore_min > 0.5 else -0.6
    if "op2_face" in part.ops:
        zs = [zmin - 0.6, zmin - 0.3, zmin] if "part" in part.ops else list(np.arange(z0 + 1.0, zmin, 1.0)) + [zmin]
        for zf in zs:
            q.g0(clear, zf - tf.nose_r)
            q.g1(x_in2, zf - tf.nose_r)
            q.g0(x_in2, zf - tf.nose_r - 1.0)
            q.g0(clear, zf - tf.nose_r - 1.0)
    if "op2_chamfer" in part.ops:
        path = nose_path(sec, tf.nose_r, zmin - tf.nose_r, zmin + 7.0)      # up to a 6 mm chamfer
        r_hi, keep = path[0][0], []
        for r_, z_ in path:           # stop where the OD steps back in (an edge facing the free end of setup 2)
            if r_ < r_hi - 0.02 and z_ > zmin + 1.0:
                break
            r_hi = max(r_hi, r_)
            keep.append((r_, z_))
        path = keep
        q.g0(path[0][0] - 0.3 if path[0][0] > 1 else 0.0, zmin - 2.0)
        q.g0(path[0][0], path[0][1])
        for r_, z_ in path:
            q.g1(r_, z_)
        q.g1(path[-1][0] + 0.6, path[-1][1] - 0.3, 0.2)
        q.g0(clear, path[-1][1] - 0.3)
        q.g0(clear, zmin - 5.0)
    if "op2_bore_chamfer" in part.ops:
        tb = TOOLS["bore"]
        q.use("bore")
        path = nose_path(sec, tb.nose_r, zmin - tb.nose_r, zmin + 2.0, outer=False, step=0.02)
        r_lo, keep = path[0][0], []
        for r_, z_ in path:
            if r_ > r_lo + 0.02 and z_ > zmin + 0.8:
                break
            r_lo = min(r_lo, r_)
            keep.append((r_, z_))
        path = keep
        q.g0(path[0][0] - 1.0, zmin - 2.0)
        q.g0(path[0][0], zmin - 2.0)
        q.g1(path[0][0], path[0][1], 0.2)            # feed the last 1.6 mm: the face is only 0.4 mm away
        for r_, z_ in path:
            q.g1(r_, z_, 0.06)
        q.g1(path[-1][0] - 1.0, path[-1][1] - 0.4, 0.2)
        q.g0(path[-1][0] - 1.0, zmin - 5.0)
    if "op2_groove" in part.ops:
        tg = TOOLS["fgroove"]
        q.use("fgroove")
        gd = P.STOCK["seal_groove_d"]
        g_out, g_in = P.STOCK["glass_od"] / 2 + 1.5, P.STOCK["glass_od"] / 2 - P.STOCK["glass_wall"] - 1.5
        q.lines.append(f"(face groove r {g_in:.2f}-{g_out:.2f} mm, {gd:.1f} mm deep, plunges 1 mm)")
        centres = list(np.arange(g_in + tg.width / 2, g_out - tg.width / 2, tg.width * 0.8)) + [g_out - tg.width / 2]
        for rc_ in centres:
            q.g0(rc_, zmin - 1.0)
            zz = zmin
            while zz < zmin + gd - 1e-6:
                zz = min(zz + 1.0, zmin + gd)
                q.g1(rc_, zz, tg.f)
                q.g0(rc_, zmin - 1.0)
                if zz < zmin + gd:
                    q.g0(rc_, zz - 0.2)
        q.g0(clear, zmin - 3.0)
    q.end()
    progs.append(q)
    return progs


# --------------------------------------------------------------------------------------- simulation
def apply_tool(stock, tool, rc, zc, rr, zz, flip, test=False):
    """Clear (or, with test=True, count) the cells the tool occupies with its nose centre at (rc, zc):
    the nose circle plus the tool body on the side it is held from. Works on index slices (fast)."""
    t = TOOLS[tool]
    rn = max(t.nose_r, RES)
    away = -1 if flip else 1          # setup 1: the body is above the nose (+z); setup 2: below
    nz, nr = stock.shape
    iz = lambda z: int(np.clip(np.floor((z - zz[0]) / RES + 0.5), 0, nz))  # noqa: E731
    ir = lambda r: int(np.clip(np.floor(r / RES + 0.5), 0, nr))  # noqa: E731
    count = 0
    regions = []
    if t.side == "part":
        regions.append((iz(zc - t.width / 2), iz(zc + t.width / 2), ir(rc - t.nose_r), nr))
    elif t.side == "fgroove":
        r0, r1 = ir(rc - t.width / 2), ir(rc + t.width / 2)
        # the programmed point is the blade's tip: the blade occupies everything behind it
        regions.append((iz(zc), nz, r0, r1) if away > 0 else (0, iz(zc), r0, r1))
    else:
        b = rn * 0.95
        if t.side == "od":
            regions.append((iz(zc - b), iz(zc + b), ir(rc), nr))
        elif t.side == "bore":
            regions.append((iz(zc - b), iz(zc + b), 0, ir(rc)))
        if away > 0:
            regions.append((iz(zc), nz, ir(rc - b), ir(rc + b)))
        else:
            regions.append((0, iz(zc), ir(rc - b), ir(rc + b)))
        z0, z1, r0, r1 = iz(zc - rn) , iz(zc + rn) + 1, ir(rc - rn), ir(rc + rn) + 1
        if z1 > z0 and r1 > r0:
            sub = stock[z0:z1, r0:r1]
            d2 = (rr[None, r0:r1] - rc) ** 2 + (zz[z0:z1, None] - zc) ** 2
            m = d2 <= rn ** 2
            if test:
                count += int((sub & m).sum())
            else:
                sub &= ~m
    for z0, z1, r0, r1 in regions:
        if z1 <= z0 or r1 <= r0:
            continue
        if test:
            count += int(stock[z0:z1, r0:r1].sum())
        else:
            stock[z0:z1, r0:r1] = False
    return count


def simulate(part, progs):
    r_in, R, z0, z1 = part.stock
    nr = int(math.ceil((R + 4) / RES))
    nz = int(math.ceil((z1 - z0 + 8) / RES))
    rr = (np.arange(nr) + 0.5) * RES
    zz = z0 - 4 + (np.arange(nz) + 0.5) * RES
    stock = (rr[None, :] >= r_in) & (rr[None, :] <= R) & (zz[:, None] >= z0) & (zz[:, None] <= z1)
    from matplotlib.path import Path as MPath
    Rg, Zg = np.meshgrid(rr, zz)
    target = MPath(np.array(part.section)).contains_points(np.c_[Rg.ravel(), Zg.ravel()]).reshape(Rg.shape)
    zmin = Polygon(part.section).bounds[1]
    crashes, t_cut = [], 0.0
    for prog in progs:
        if prog.flip:
            # the remnant left below the parting cut is gone; setup 2 holds the part by its OD
            stock &= zz[:, None] >= zmin - 0.31
        for kind, tool, a, b, f, vc in prog.moves:
            if kind == "DRILL":
                dd, zb = b
                stock &= ~((rr[None, :] <= dd) & (zz[:, None] >= zb))
                t_cut += (a[1] - zb) / (f * 300.0) * 60.0
                continue
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(2, int(L / (RES * 0.7)) + 1)
            hit = False
            for s in np.linspace(0, 1, n):
                rc, zc = a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1])
                if kind == "G0":
                    if apply_tool(stock, tool, rc, zc, rr, zz, prog.flip, test=True) > 2:
                        hit = True
                        break
                else:
                    apply_tool(stock, tool, rc, zc, rr, zz, prog.flip)
            if kind == "G0" and hit:
                crashes.append({"program": prog.setup, "tool": tool, "from": [round(v, 2) for v in a],
                                "to": [round(v, 2) for v in b]})
            if kind == "G1":
                rpm = min(2000.0, vc * 1000 / (2 * math.pi * max(abs(a[0] + b[0]) / 2, 3.0)))
                t_cut += L / (f * rpm) * 60.0
    material = stock & (zz[:, None] >= zmin - 0.05)
    gouge = target & ~material
    left = material & ~target
    from scipy.ndimage import distance_transform_edt
    d_out = distance_transform_edt(~target) * RES
    d_in = distance_transform_edt(target) * RES
    gouge_deep = gouge & (d_in > 0.06)     # more than one 0.05 mm cell
    left_thick = left & (d_out > 0.06)
    res = {"part": part.name, "material": part.material,
           "gouge_area_mm2": round(float(gouge_deep.sum() * RES ** 2), 3),
           "gouge_max_mm": round(float(d_in[gouge].max()) if gouge.any() else 0.0, 3),
           "leftover_area_mm2": round(float(left_thick.sum() * RES ** 2), 3),
           "leftover_max_mm": round(float(d_out[left].max()) if left.any() else 0.0, 3),
           "rapids_through_stock": len(crashes), "crashes": crashes[:5],
           "cut_time_min": round(float(t_cut) / 60.0, 1), "programs": [pp.setup for pp in progs]}
    return res, (rr, zz, stock, target, gouge_deep, left_thick)


def plot(part, data, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rr, zz, stock, target, gouge, left = data
    fig, ax = plt.subplots(figsize=(4.6, 4.0), dpi=110)
    img = np.ones(stock.shape + (3,))
    img[stock] = (0.80, 0.82, 0.86)
    img[target & stock] = (0.52, 0.58, 0.68)
    img[gouge] = (0.85, 0.10, 0.10)
    img[left] = (0.95, 0.62, 0.10)
    ax.imshow(img, origin="lower", extent=[0, rr[-1] + RES / 2, zz[0] - RES / 2, zz[-1] + RES / 2], aspect="equal")
    sec = np.array(part.section + [part.section[0]])
    ax.plot(sec[:, 0], sec[:, 1], color="k", lw=0.7)
    ax.set_xlabel("r (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_title(f"{part.name}: gouge {res['gouge_area_mm2']} mm2, leftover {res['leftover_area_mm2']} mm2, "
                 f"rapid hits {res['rapids_through_stock']}", fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / f"lathe_{part.name}.png")
    plt.close(fig)


def main():
    results = []
    for part in parts():
        progs = gen(part)
        for prog in progs:
            tag = "op1" if not prog.flip else "op2"
            (GC / f"{part.name}_{tag}.nc").write_text("\n".join(flat_comments(ln) for ln in prog.lines) + "\n")
        res, data = simulate(part, progs)
        res["note"] = part.note
        results.append(res)
        plot(part, data, res)
        print(part.name, {k: res[k] for k in ("gouge_area_mm2", "gouge_max_mm", "leftover_area_mm2",
                                              "leftover_max_mm", "rapids_through_stock", "cut_time_min")},
              flush=True)
    (OUT / "lathe_sim.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
