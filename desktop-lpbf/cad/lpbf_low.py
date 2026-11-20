"""Low-profile ("horizontally distributed") CadQuery model of the desktop LPBF, for a VLM tray (issue #260, PR #266).

Why low: in byu-vcl PR 318 every machine that would not go on a vertical-lift-module tray failed on *height*:
727.5 mm is the only product height Kardex publishes for the Shuttle XP 500, and Modula's bay S is 695 mm. The
tray is 2426 x 840 mm inside its rim, so width is cheap and height is not. This model keeps the whole machine
under 600 mm on a 2450 x 864 mm tray and spreads it sideways into three modules:

  left    laser and controls: a short 19 in. rack (UPS, laser, scan PC, DIN-rail drawer)
  centre  process module: chamber, folded Z stage hung from the chamber floor, recoater, lid with dosing,
          window and camera, optics bridge with an f = 160 mm f-theta and galvo, Class 1 laser guard
  right   gas and vacuum: dry scroll pump, sealed blower, cyclone + HEPA housing, O2 and dew point, argon valves

Run:  python desktop-lpbf/cad/lpbf_low.py                 # STEP + GLB to desktop-lpbf/cad/out/ (git-ignored)
      xvfb-run -a python desktop-lpbf/cad/render_low.py   # PNGs and GIFs

Units mm. Origin: centre of the build plate's top face at the start of a build (the powder plane).
+X is the recoat direction (left to right seen from the front), +Y points to the back, +Z up. The tray top is
at z = Z_TRAY. Every part carries its material key (MAT) so analysis/ can compute masses and run FEA from the
same geometry, and every moving part carries the motion group it belongs to (MOTION).
"""
from __future__ import annotations

import math
import pathlib
import sys
from dataclasses import dataclass, field

import cadquery as cq

import module_params as MP
import modules_low as ML

V = cq.Vector
HERE = pathlib.Path(__file__).resolve().parent

# --------------------------------------------------------------------------------------------
# Envelope (byu-vcl PR 318): tray, opening heights
# --------------------------------------------------------------------------------------------
TRAY = dict(outer=(2450.0, 864.0), inner=(2426.0, 840.0), rim=20.0, t=4.0)
OPENINGS = {"Modula bay S": 695.0, "Kardex Shuttle XP 500 (published)": 727.5, "Kardex, 996 mm used-unit opening (estimate)": 856.5}
# McMaster 5537T983 leveling mounts, to the dimensions measured on McMaster's own model: Ø25 x 7.62 base, a swivel housing
# tapering to Ø15.24 at 15.11, a 12 mm A/F hex from 16 to 20, and an M8 stem 32 long (52 overall). The stem threads up through
# the 15 mm base plate and ends flush with its top, so the plate bottom sits 37 mm above the tray (was 20 mm on a drawn foot).
FOOT = dict(body=20.0, stem=32.0, base_d=25.0)
Z_TRAY = -160.0 - (FOOT["body"] + FOOT["stem"])          # -212.0; base-plate top stays at z = -160

# --------------------------------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------------------------------
P = dict(
    # process chamber (internal) and walls; the 16 mm wall is set by the O-ring groove + M5 bolt line, not stress
    # 190 mm deep (was 150): the Ø75 dose line (+/-50 mm) has to clear the recoater drive on the back wall
    ch_x=280.0, ch_y=190.0, ch_z=120.0, wall=16.0, floor=20.0, lid=16.0,
    # build modules (module_params.py): one floor port takes Ø25, Ø50 and Ø75 heated modules; 40 mm build stroke,
    # 2 mm to the bottom stop, +8 mm plate-exchange overtravel. The recoat, dose and gas geometry is sized for Ø75.
    port_d=MP.PORT_D, stroke=MP.BUILD_STROKE,
    # powder path along X (dose line and blade +/-50 mm for the Ø76.2 plate)
    x_dose=MP.X_DOSE, x_park=MP.X_PARK, x_end=MP.X_END, ovf_x0=MP.OVF_X0, ovf_x1=MP.OVF_X1, dose_y=MP.DOSE_HALF, blade_gap=0.05,
    # recoater drive on the back wall
    rc_rail_z=82.0, rc_screw_y=72.0, rc_screw_z=40.0,
    # O-ring face glands (Parker ORD 5700, design chart 4-3): 3.53 mm FKM cord, depth 2.65 mm (25 % squeeze),
    # width 4.6 mm (the "warm" width, 80 % gland fill) so the seal keeps >= 10 % void at a 200 C plate
    oring_cs=3.53, gland_d=2.65, gland_w=4.6,
    # door: 1.78 mm cord in a half-dovetail groove 1.32 deep (seals.md); analysis/seals/door_seal_fea.py reads the depth from here
    door_gland_d=1.32,
    # optics: f = 160 mm f-theta (Thorlabs FTH160-1064 envelope: WD 182.5, housing Ø90 x 50.2)
    lens_wd=182.5, lens_len=50.2, lens_d=90.0, galvo=115.0, galvo_h=110.0,
    # door
    door_open_deg=95.0,
)
# the default (M50) module's plate and bore, for scripts that read one plate size (render_low's build-cycle GIF)
P["plate_d"], P["bore_d"], P["plate_t"] = MP.MODULES["M50"]["plate_d"], MP.MODULES["M50"]["bore"], MP.PLATE_T
P["ix"], P["iy"] = P["ch_x"] / 2, P["ch_y"] / 2
P["cx"], P["cy"] = P["ix"] + P["wall"], P["iy"] + P["wall"]
P["lid_z0"], P["lid_z1"] = P["ch_z"], P["ch_z"] + P["lid"]
P["z_lens0"] = P["lens_wd"]                              # lens housing bottom
P["z_bridge1"] = P["lens_wd"] + P["lens_len"]            # galvo mounting face = bridge top
P["z_bridge0"] = P["z_bridge1"] - 25.0               # 25 mm: FEA put f1 at 79 Hz with 15 mm + 40 mm posts
P["beam_z"] = P["z_bridge1"] + 45.0
P["z_base1"] = Z_TRAY + FOOT["body"] + FOOT["stem"]     # module base plates (15 mm) on the leveling mounts
P["z_base0"] = P["z_base1"] - 15.0

# Materials: density (kg/m3) plus the properties the FEA uses. Sources are in analysis/README.md.
MAT = {
    "al6061": dict(rho=2700, E=68.9e3, nu=0.33, sy=276.0, su=310.0, fat=96.5, alpha=23.6e-6, label="6061-T6 aluminium"),
    "mic6": dict(rho=2650, E=71.0e3, nu=0.33, sy=105.0, su=165.0, fat=None, alpha=23.4e-6, label="MIC-6 cast tooling plate"),
    "ss304": dict(rho=8000, E=193e3, nu=0.29, sy=215.0, su=505.0, fat=None, alpha=17.3e-6, label="304 stainless"),
    "ss316l": dict(rho=7990, E=193e3, nu=0.30, sy=170.0, su=485.0, fat=None, alpha=16.0e-6, label="316L stainless"),
    "steel": dict(rho=7850, E=205e3, nu=0.29, sy=355.0, su=600.0, fat=None, alpha=11.7e-6, label="bearing / alloy steel"),
    "fused_silica": dict(rho=2201, E=72.7e3, nu=0.16, sy=None, su=50.0, fat=None, alpha=0.55e-6, label="UV fused silica"),
    "fkm": dict(rho=1850, label="FKM (Viton) 75A"),
    "silicone": dict(rho=1150, label="silicone rubber"),
    "ptfe": dict(rho=2160, label="PTFE"),
    "felt": dict(rho=400, label="aramid felt"),
    "macor": dict(rho=2520, E=66.9e3, nu=0.29, sy=None, su=94.0, fat=None, alpha=9.3e-6, label="Macor machinable glass-ceramic"),
    "pc": dict(rho=1200, label="laser-safety polycarbonate"),
    "brass": dict(rho=8500, label="brass"),
    "powder": dict(rho=1350, label="AlSi10Mg powder (~50 % packing)"),
    "rubber": dict(rho=1200, label="rubber"),
    "misc": dict(rho=1000, label="mixed (vendor unit; mass from datasheet or estimate)"),
}

C = dict(
    tslot="#c3c9cf", alu="#b9c0c7", alu_dark="#8e979f", anod="#2d3136", ss="#a2abb3", steel="#6f777e",
    brass="#c9a54a", motor="#25292e", glass="#9fd3ff", laser_glass="#3fbf6a", panel="#46535f",
    powder="#8b8d8f", hot="#ff8a2a", beam="#ff1f1f", silicone="#d4553b", pcb="#2f7d4f", din="#c0c4c8",
    red="#d22b2b", yellow="#f0c419", green="#2bb24c", blue="#2b6cd2", fiber="#f08c1a", hose="#7f8890",
    white="#f2f2f2", black="#151719", tray="#d7dbe0", rack="#3b4148", water="#3aa0d8", argon="#9b7fd1",
)


@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: str
    step: int
    explode: tuple = (0.0, 0.0, 0.0)
    group: str = ""          # motion group (MOTION) the part moves with, "" if fixed
    bom: str = ""
    mcm: str = ""
    mat: str = "al6061"
    mass_kg: float | None = None   # catalogue / datasheet mass overrides volume x density
    opacity: float = 1.0
    module: str = "process"
    section: bool = False
    tags: tuple = field(default_factory=tuple)


STEPS = {
    1: "VLM tray (2426 x 840 mm inside the rim), module base plates and feet",
    2: "Left module: 19 in. rack with UPS, fiber laser, scan PC and DIN-rail drawer",
    3: "Chamber legs and the folded Z stage hung from the chamber floor (pot-magnet coupling)",
    4: "Heated build module (spigot, cylinder, plate, heater block, Macor break, piston head, hollow rod) and overflow",
    5: "Process chamber body, cross-flow plenums and ports",
    6: "Recoater axis: rail, ball screw, carriage, blade, bearings, servo",
    7: "Lid: window, field stop, cover-slide drawer, gas knife, metering base, swappable reservoir, camera, sensors",
    8: "Drop-down chamber door, hinges and toggle latches",
    9: "Optics bridge, f-theta lens, galvo, beam tube, shutter, collimator, fiber",
    10: "Right module: dry scroll pump, sealed blower, cyclone + HEPA housing, O2/dew point, argon valves",
    11: "Gas loop and vacuum hoses",
    12: "Class 1 laser guard: frame, panels, sliding door with OD 7+ window, guard lock, operator panel",
    13: "Tray dock (power, Ethernet, argon, chilled water, exhaust) and umbilicals",
}

# Motion groups: kind, axis/hinge, range. analysis/ sweeps every group through its range.
# drop out of the port, slide forward under the outlet plenum, rise under the door hinges, then over the guard sill
# (since the seals were drawn the gland plate and the rod end are 14 mm deeper: the module rises at y -158 (was -170) so the L75
# handle stays clear of the guard's bottom front rail, and the last rise is to +4 (was -10) so the rod end clears the guard sill)
MODULE_PATH = [(0.0, 0.0, 0.0), (0.0, 0.0, -MP.MODULE_DROP), (0.0, -158.0, -MP.MODULE_DROP), (0.0, -158.0, -22.0), (0.0, -190.0, -22.0),
               (0.0, -190.0, 4.0), (0.0, -330.0, 4.0)]
MOTION = {
    "recoater": dict(kind="tx", lo=0.0, hi=P["x_end"] - P["x_park"], note="blade from park to end of spread"),
    "piston": dict(kind="tz", lo=MP.Z_P_MIN, hi=MP.Z_P_MAX, note="build piston: stroke, bottom stop and +8 mm plate-exchange overtravel"),
    "door": dict(kind="rx", lo=0.0, hi=P["door_open_deg"], note="drop-down door about its bottom hinge"),
    "gdoor": dict(kind="tx", lo=0.0, hi=470.0, note="laser-guard door slides right"),
    "cartridge": dict(kind="ty", lo=-125.0, hi=0.0, note="reservoir slides out to the front"),
    "drawer": dict(kind="ty", lo=-120.0, hi=0.0, note="cover-slide drawer pulls out of the lid's front edge"),
    "zstage": dict(kind="tz", lo=MP.ZSTAGE_RELEASE, hi=0.0, note="Z arm drops away from the rod end (magnet breaks away), piston held by its collar"),
    "module": dict(kind="path", path=MODULE_PATH, lo=0.0, hi=None, base_state={"zstage": MP.ZSTAGE_RELEASE, "gdoor": 470.0},
                   note="build module drops 22 mm out of the floor port, slides forward under the chamber, lifts over the guard sill and out"),
}
MOTION["module"]["hi"] = sum(math.dist(a, b) for a, b in zip(MODULE_PATH[:-1], MODULE_PATH[1:]))
DOOR_HINGE = None   # (y, z) of the door hinge axis (parallel to X); set in build()
_RES = None         # the docked reservoir's screw positions (joints.py)
GLANDS: dict = {}   # every O-ring gland drawn by build(): analysis/seals/seals.py checks each one (Parker squeeze, fill, stretch)

# Real parts drawn to their published dimensions (seal-parts.csv has the part numbers, prices and sources).
# Door: McMaster 1807A61 adjustable-grip draw latch, 304 SS, 800 lb: 5-1/4 in. long including the strike at the longest latching
# distance, 1-3/4 in. wide, 1-1/4 in. projection, latching distance 1-3/8 to 2-1/2 in.
LATCH_1807A61 = dict(L=133.35, W=44.45, H=31.75, body_L=80.0, rating_N=800 * 4.448)
# drawer: quarter-turn cam latch (stud in the drawer plate, receptacle in the lid); envelope from the vendor drawing
QTURN = dict(head_d=14.0, head_t=3.5, stud_d=6.0, rec_d=9.0, rec_l=12.0, label="quarter-turn latch", pn="", rating_N=0.0)
# magnetic-fluid rotary feedthrough envelope (vendor drawing): flange, housing, shafts; for the recoater screw and the roller
# Ferrotec SFL-006-NN (flange mount): 6 mm shaft, Ø28 housing, 82 mm overall with a 15 mm vacuum-side shaft, Ø52 flange with
# 6 x Ø4.5 on a 40 mm circle. It sits on a 9 mm 6061 spacer ring (FKM face O-rings both sides) so its vacuum-side shaft ends in
# the wall's bore, where the clamp coupling joins it to the ball screw. Split of the 82 mm between flange, housing and air shaft
# assumed (6 / 46 / 15) from the overall length.
FERRO = dict(flange_d=52.0, flange_t=6.0, body_d=28.0, body_l=46.0, shaft_d=6.0, air_shaft=15.0, vac_shaft=15.0, spacer=9.0,
             label="magnetic-fluid rotary feedthrough Ferrotec SFL-006-NN", pn="Ferrotec SFL-006-NN", oring="2-024")
# Ferrotec SSL-005-NN (nut mount): 5 mm shaft, Ø16 housing, M8 x 1 nose, 65.5 mm overall with a 12.5 mm vacuum-side shaft
# (nose 8 / housing 35 / air shaft 10 assumed); screws into an M8 x 1 hole in the metering base over a 2-012 FKM face O-ring.
FERRO_S = dict(body_d=16.0, body_l=35.0, nose_d=8.0, nose_l=8.0, shaft_d=5.0, air_shaft=10.0, vac_shaft=12.5,
               label="magnetic-fluid rotary feedthrough Ferrotec SSL-005-NN", pn="Ferrotec SSL-005-NN", oring="2-012")


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


def comp(shapes):
    return cq.Compound.makeCompound([s for s in shapes if s is not None])


def fuse(shapes):
    s = [x for x in shapes if x is not None]
    out = s[0]
    for x in s[1:]:
        out = out.fuse(x)
    return out.clean()


def place(shape, origin, xdir, normal):
    return shape.moved(cq.Location(cq.Plane(origin=V(*origin), xDir=V(*xdir), normal=V(*normal))))


def polyline_pipe(points, r, n=10):
    """Hose or cable through a Catmull-Rom-smoothed polyline: cylinders joined by spheres."""
    pts = [V(*p) for p in points]
    if len(pts) > 2:
        ext = [pts[0] + (pts[0] - pts[1])] + pts + [pts[-1] + (pts[-1] - pts[-2])]
        sm = []
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for k in range(n):
                t = k / n
                t2, t3 = t * t, t * t * t
                sm.append(p0 * (-0.5 * t3 + t2 - 0.5 * t) + p1 * (1.5 * t3 - 2.5 * t2 + 1)
                          + p2 * (-1.5 * t3 + 2 * t2 + 0.5 * t) + p3 * (0.5 * t3 - 0.5 * t2))
        sm.append(pts[-1])
        pts = sm
    solids = []
    for a, b in zip(pts[:-1], pts[1:]):
        d = b - a
        if d.Length < 1e-6:
            continue
        solids.append(cq.Solid.makeCylinder(r, d.Length, a, d.normalized()))
    for p in pts[1:-1]:
        solids.append(cq.Solid.makeSphere(r, p, V(0, 0, 1), -90, 90, 360))
    return comp(solids)


RAIL_HOLES = dict(first=20.0, pitch=60.0, d=4.5, cb_d=7.5, cb_h=5.3)   # McMaster 6709K33: M4, 60 mm c-c, 20 mm from the end


def rail_hole_x(L):
    return [RAIL_HOLES["first"] + k * RAIL_HOLES["pitch"] for k in range(int((L - RAIL_HOLES["first"]) // RAIL_HOLES["pitch"]) + 1)]


def guide_rail(L, w, h):
    """15 mm profile rail along local +x 0..L, centred in y, base on z = 0, with its M4 counterbored holes."""
    r = cq.Workplane("XY").box(L, w, h, centered=(False, True, False)).edges("|X and >Z").chamfer(0.8).val()
    for x in rail_hole_x(L):
        r = r.cut(cyl(RAIL_HOLES["d"] / 2, (x, 0, -1), "z", h + 2)).cut(cyl(RAIL_HOLES["cb_d"] / 2, (x, 0, h - RAIL_HOLES["cb_h"]), "z", RAIL_HOLES["cb_h"] + 1))
    return r


def guide_carriage(cl, cw, H, clear, w_rail, h_rail):
    body = cq.Workplane("XY").box(cl, cw, H - clear, centered=(True, True, False)).edges("|X").fillet(1.0).val()
    body = body.translate(V(0, 0, clear))
    return body.cut(box(-cl, cl, -w_rail / 2 - 0.5, w_rail / 2 + 0.5, 0, h_rail + 0.5))


def ball_screw(L, d, j_d=8.0, j_l=30.0):
    return fuse([cyl(j_d / 2, (0, 0, 0), "x", j_l), cyl(d / 2, (j_l, 0, 0), "x", L - 2 * j_l),
                 cyl(j_d / 2, (L - j_l, 0, 0), "x", j_l)])


def ball_nut(d, body_d=24.0, body_l=40.0, fl_d=40.0, fl_t=10.0, flats=None):
    """Nut on local x, flange at the -x end, bore = screw diameter (contact, not interference)."""
    body = tube(body_d / 2, d / 2, (-body_l / 2 + fl_t, 0, 0), "x", body_l - fl_t)
    fl = tube(fl_d / 2, d / 2, (-body_l / 2, 0, 0), "x", fl_t)
    if flats:
        fl = fl.cut(box(-body_l, body_l, flats, fl_d, -fl_d, fl_d)).cut(box(-body_l, body_l, -fl_d, -flats, -fl_d, fl_d))
    return fuse([body, fl])


def servo_nema23(length=100.0, shaft_l=22.0):
    """ClearPath-style NEMA 23 servo: mount face at local z = 0, body toward -z, shaft +z."""
    sq = 57.15
    body = cq.Workplane("XY").box(sq, sq, length, centered=(True, True, False)).edges("|Z").chamfer(4).val()
    body = body.translate(V(0, 0, -length))
    pilot = cyl(19.05, (0, 0, 0), "z", 1.6)
    shaft = cyl(9.525 / 2, (0, 0, 1.6), "z", shaft_l)
    return fuse([body, pilot, shaft])


def stepper_nema17(length=40.0):
    sq = 42.3
    body = cq.Workplane("XY").box(sq, sq, length, centered=(True, True, False)).edges("|Z").chamfer(3.5).val()
    return fuse([body.translate(V(0, 0, -length)), cyl(11, (0, 0, 0), "z", 2)])


KF = {16: (30.0, 17.2), 25: (40.0, 25.4), 40: (55.0, 41.3), 50: (75.0, 52.0)}


def kf_stub(size, stub=20.0, wall=1.6):
    """Flange face at local z = 0, tube toward -z, hollow."""
    fo, to = KF[size]
    fl = cq.Workplane("XY").circle(fo / 2).extrude(-5.5).faces("<Z").chamfer(2.0).val()
    t = cyl(to / 2, (0, 0, -stub), "z", stub - 5.5)
    return fuse([fl, t]).cut(cyl(to / 2 - wall, (0, 0, -stub - 1), "z", stub + 2))


def kf_clamp(size):
    fo, _ = KF[size]
    return fuse([tube(fo / 2 + 7, fo / 2 + 0.5, (0, 0, -6), "z", 12), box(fo / 2 + 6, fo / 2 + 20, -5, 5, -4, 4)])


def shcs_head(p, axis="z", d=8.5, k=5.0):
    return cyl(d / 2, p, axis, k).cut(cyl(2.0, p, axis, k + 0.01).translate(_AX[axis] * (k - 2.5)))


def ring_loop(axis, c, half_in, width, depth_range, r_in):
    """Rounded-rectangle annulus (a face gland or the O-ring in it). axis: the face normal 'x', 'y' or 'z'; c: centre (3-tuple);
    half_in: half-sizes of the inner wall along the two in-plane axes (in x, y, z order skipping `axis`); depth_range: (a0, a1)
    along `axis`; r_in: inner corner radius."""
    a0, a1 = depth_range
    ax = {"x": 0, "y": 1, "z": 2}[axis]
    other = [k for k in range(3) if k != ax]
    def rr(h0, h1, r):
        lo, hi = [0.0] * 3, [0.0] * 3
        lo[ax], hi[ax] = a0, a1
        for k, hh in zip(other, (h0, h1)):
            lo[k], hi[k] = c[k] - hh, c[k] + hh
        return rbox(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], r, "|" + "XYZ"[ax])
    return rr(half_in[0] + width, half_in[1] + width, r_in + width).cut(rr(half_in[0], half_in[1], r_in))


def loop_perimeter(half_in, r_in):
    """Perimeter of a rounded rectangle with these half-sizes and corner radius (the groove's inner wall)."""
    return 4 * (half_in[0] + half_in[1]) - (8 - 2 * math.pi) * r_in


def fit_loop(hi, r_in, grow_max=3.0, shrink_max=1.0):
    """Lengthen (or shorten) a loop's longer side so that a standard AS568 1.78 mm ring sits on the groove's inner wall at ~2 %
    stretch. Returns (half-sizes, (dash, ID, stretch))."""
    base = loop_perimeter(hi, r_in)
    k = 0 if hi[0] >= hi[1] else 1
    best = None
    for dash, (d, c) in MP.AS568.items():
        if not dash.startswith("2-0") or abs(c - 1.78) > 0.05:
            continue
        delta = (1.02 * math.pi * d - base) / 4.0
        if -shrink_max <= delta <= grow_max and (best is None or abs(delta) < abs(best[1])):
            best = (dash, delta)
    if best is None:
        return tuple(hi), MP.pick_ring(base)
    h2 = list(hi)
    h2[k] += best[1]
    return tuple(h2), MP.pick_ring(loop_perimeter(h2, r_in))


def dovetail_loop(origin, normal, xdir, w_in, h_in, r_in, width=2.3, depth=1.32, deg=24.0):
    """Half-dovetail groove cut into a face: origin on the face, normal pointing out of the face. The inner wall is
    straight; the outer wall is undercut by `deg` so the groove is `width` wide at its bottom and narrower at the face, which
    keeps the cord in the groove when the closure opens (Parker ORD 5700, half-dovetail glands)."""
    n = V(*normal).normalized()
    pl = cq.Plane(origin=V(*origin) - n * depth, xDir=V(*xdir), normal=n)
    outer = (cq.Workplane(pl).sketch().rect(w_in + 2 * width, h_in + 2 * width).vertices().fillet(r_in + width).finalize()
             .extrude(depth + 0.01, taper=deg).val())
    pl2 = cq.Plane(origin=V(*origin) - n * (depth + 0.02), xDir=V(*xdir), normal=n)
    inner = cq.Workplane(pl2).sketch().rect(w_in, h_in).vertices().fillet(r_in).finalize().extrude(depth + 0.1).val()
    return outer.cut(inner)


def tslot20(p0, axis, L):
    """20 mm T-slot (simplified: square with four slot grooves)."""
    s = cq.Workplane("XY").rect(20, 20).extrude(L)
    for dx, dy in ((0, 10), (0, -10), (10, 0), (-10, 0)):
        s = s.cut(cq.Workplane("XY").center(dx, dy).rect(6 if dx == 0 else 4, 4 if dx == 0 else 6).extrude(L))
    s = s.val()
    if axis == "x":
        s = s.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    elif axis == "y":
        s = s.rotate(V(0, 0, 0), V(1, 0, 0), -90)
    return s.translate(V(*p0))


# --------------------------------------------------------------------------------------------
# The machine
# --------------------------------------------------------------------------------------------
def build(include_tray=True, module="M50", reservoir=None, fasteners=True):
    """The machine with one build module (S25, M50 or L75) and one reservoir (S, M or L; default: the module's)."""
    global DOOR_HINGE, _RES
    GLANDS.clear()
    parts: list[Part] = []
    F = MP.FACE_1P78
    sae4 = dict(thread_d=11.11, depth=11.5, csk_d=12.9, csk_depth=1.6, drill_d=4.0)   # SAE J1926-1 / MS16142 size -4 port (7/16-20 UNF)

    def sae_port(shape, p0, axis, wall):
        """SAE J1926 straight-thread O-ring-boss port (-4): thread drawn at its major diameter, 12 deg O-ring chamfer, then a Ø4 drilling."""
        d = _AX[axis]
        shape = shape.cut(cyl(sae4["thread_d"] / 2, p0, axis, sae4["depth"]))
        shape = shape.cut(cq.Solid.makeCone(sae4["csk_d"] / 2, sae4["thread_d"] / 2, sae4["csk_depth"], V(*p0) - d * 0.01, d))
        return shape.cut(cyl(sae4["drill_d"] / 2, tuple(V(*p0) + d * (sae4["depth"] - 0.1)), axis, wall - sae4["depth"] + 1.2))

    def add(name, shape, color, step, explode=(0, 0, 0), **kw):
        parts.append(Part(name, shape, color, step, tuple(float(e) for e in explode), **kw))

    ix, iy, iz = P["ix"], P["iy"], P["ch_z"]
    cx, cy = P["cx"], P["cy"]
    fl = P["floor"]
    lz0, lz1 = P["lid_z0"], P["lid_z1"]
    zb0, zb1 = P["z_base0"], P["z_base1"]
    reservoir = reservoir or MP.MODULES[module]["reservoir"]

    # ===================== 1. Tray, base plates, feet =====================
    if include_tray:
        ox, oy = TRAY["outer"][0] / 2, TRAY["outer"][1] / 2
        inx, iny = TRAY["inner"][0] / 2, TRAY["inner"][1] / 2
        tr = box(-ox, ox, -oy, oy, Z_TRAY - TRAY["t"], Z_TRAY)
        rim = box(-ox, ox, -oy, oy, Z_TRAY, Z_TRAY + TRAY["rim"]).cut(box(-inx, inx, -iny, iny, Z_TRAY - 1, Z_TRAY + TRAY["rim"] + 1))
        add("VLM tray 2450 x 864 mm (context)", fuse([tr, rim]), C["tray"], 1, (0, 0, -200), mat="steel", mass_kg=0.0, module="tray", tags=("context",))
    bases = {"rack": (-990.0, -430.0, -300.0, 300.0), "process": (-370.0, 290.0, -265.0, 215.0), "gas": (400.0, 990.0, -250.0, 300.0)}
    for mod, (x0, x1, y0, y1) in bases.items():
        if mod == "rack":
            continue   # the rack stands on its own frame
        bp = box(x0, x1, y0, y1, zb0, zb1)
        if mod == "process":     # window for the Z stage: arm, actuator and folded servo hang through it toward the tray
            bp = bp.cut(fuse([rbox(-45, 100, -32, 114, zb0 - 1, zb1 + 1, 8), box(-56, 56, y0 - 1, 0, zb0 - 1, zb1 + 1)]))   # + slot for the module's rod end
        add(f"Base plate, {mod} module (MIC-6, 15 mm)", bp, C["alu"], 1, (0, 0, -150), mat="mic6", module=mod, bom="F4")
        feet = []
        for x in (x0 + 30, x1 - 30):
            for y in (y0 + 30, y1 - 30):
                z0 = Z_TRAY
                hexa = cq.Workplane("XY").polygon(6, 12.0 / math.cos(math.pi / 6)).extrude(4.0).val().translate(V(x, y, z0 + 16.0))
                feet += [fuse([cyl(FOOT["base_d"] / 2, (x, y, z0), "z", 7.62),
                               cq.Solid.makeCone(12.5, 8.05, 2.4, V(x, y, z0 + 7.62), V(0, 0, 1)),
                               cyl(7.62, (x, y, z0 + 10.0), "z", 5.11), cyl(5.5, (x, y, z0 + 15.1), "z", 1.0), hexa,
                               cyl(4.0, (x, y, z0 + FOOT["body"]), "z", FOOT["stem"])])]
        add(f"Leveling mounts, {mod} module (McMaster 5537T983: Ø25 base, M8 stem threaded up through the plate)", comp(feet), C["anod"], 1, (0, 0, -200),
            mat="steel", module=mod, bom="F3", mcm="5537T983")

    # ===================== 2. Rack module =====================
    rx0, rx1, ry0, ry1 = bases["rack"]
    rz0, rz1 = Z_TRAY, Z_TRAY + 470.0
    posts = []
    for x in (rx0, rx1 - 25):
        for y in (ry0, ry1 - 25):
            posts.append(box(x, x + 25, y, y + 25, rz0 + 20, rz1 - 20))
    for z in (rz0 + 0, rz1 - 20):
        posts += [box(rx0, rx1, ry0, ry0 + 25, z, z + 20), box(rx0, rx1, ry1 - 25, ry1, z, z + 20),
                  box(rx0, rx0 + 25, ry0 + 25, ry1 - 25, z, z + 20), box(rx1 - 25, rx1, ry0 + 25, ry1 - 25, z, z + 20)]
    add("19 in. rack frame (10U, 470 mm tall)", comp(posts), C["rack"], 2, (0, 0, 0), mat="steel", mass_kg=22.0, module="rack", bom="S9")
    ux0, ux1 = (rx0 + rx1) / 2 - 241.3, (rx0 + rx1) / 2 + 241.3      # 19 in. front panel width
    u = 44.45
    zr = rz0 + 25.0
    units = [("UPS (Eaton 5PX 1500 class, 2U)", 2, C["black"], 25.0, "C6"), ("Fiber laser source, 500 W single-mode (3U)", 3, C["white"], 40.0, "L1"),
             ("Scan + laser controller PC (2U)", 2, C["anod"], 8.0, "C1"), ("DIN-rail drawer: 24 V supply, safety relay, ClearCore, Pi 5 (3U)", 3, C["din"], 9.0, "C3")]
    for nm, nu, col, m, b in units:
        bx = box(ux0 + 18, ux1 - 18, ry0 + 30, ry1 - 40, zr + 1, zr + nu * u - 1)
        face = box(ux0, ux1, ry0 + 26, ry0 + 30, zr + 1, zr + nu * u - 1)
        add(nm, comp([bx, face]), col, 2, (0, -400, 0), mat="misc", mass_kg=m, module="rack", bom=b)
        zr += nu * u
    add("Rack side panels (vented)", comp([box(rx0 - 2, rx0, ry0, ry1, rz0 + 20, rz1), box(rx1, rx1 + 2, ry0, ry1, rz0 + 20, rz1)]), C["panel"], 2, (0, 0, 0), mat="al6061", module="rack", opacity=0.35, bom="S9")

    # ===================== 3. Chamber legs and Z stage =====================
    zf = -fl
    legs = []
    for x in (-cx + 6, cx - 36):
        for y in (-cy + 6, cy - 36):
            legs.append(box(x, x + 30, y, y + 30, zb1, zf))
    add("Chamber legs (6061, 30 x 30)", comp(legs), C["alu_dark"], 3, (0, 0, -120), mat="al6061", bom="G1")
    ML.add_zstage(sys.modules[__name__], add, 3)

    # ===================== 4. Heated build module, overflow =====================
    ML.add_build_module(sys.modules[__name__], add, module, 4)
    ox = (P["ovf_x0"] + P["ovf_x1"]) / 2
    # 316L under the 6061 floor: bolted (4 x M4, joints.py) over an FKM face O-ring round the overflow slot, never welded
    fun = box(ox - 22, ox + 22, -59, 59, zf - 22, zf).cut(box(P["ovf_x0"], P["ovf_x1"], -52, 52, zf - 11, zf + 1)).cut(cyl(19.0, (ox, 0, zf - 23), "z", 13))
    hi_f = fit_loop(((P["ovf_x1"] - P["ovf_x0"]) / 2 + 1.5, 53.5), 1.5, 2.5, 0.0)[0]
    fun = fun.cut(ring_loop("z", (ox, 0, 0), hi_f, 2.3, (zf - 1.32, zf + 0.01), 1.5))
    add("Overflow funnel block (316L, bolted, FKM face O-ring)", fun, C["ss"], 4, (0, 0, -200), mat="ss316l", bom="M4", section=True)
    pk = MP.pick_ring(loop_perimeter(hi_f, 1.5))
    add(f"Overflow funnel O-ring (FKM 75A {pk[0]}, face seal under the floor)", ring_loop("z", (ox, 0, 0), hi_f, 2.0, (zf - 1.32, zf), 1.5), C["black"], 4, (0, 0, -200), mat="fkm", bom="M4")
    GLANDS["overflow_funnel"] = dict(kind="face", ring=pk[0], cs=1.78, depth=1.32, width=2.3, inner_perimeter=loop_perimeter(hi_f, 1.5), groove_mat="ss", T=50.0,
                                     closure="overflow funnel block (316L) under the floor")
    add("Overflow port (KF-40)", place(kf_stub(40, 16), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, -1)), C["ss"], 4, (0, 0, -220), mat="ss304", bom="G7", mcm="KF40_WELD", section=True)
    jar = fuse([place(kf_stub(40, 90), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1)), cyl(KF[40][1] / 2, (ox, 0, zf - 22 - 16 - 92), "z", 2)])
    add("Overflow jar (KF-40 half nipple, 90 mm, ~120 cm3 + blank)", jar, C["ss"], 4, (0, 0, -260), mat="ss304", bom="M4", mcm="KF40_NIPPLE", section=True)
    add("Overflow clamp (KF-40)", place(kf_clamp(40), (ox, 0, zf - 22 - 16), (1, 0, 0), (0, 0, 1)), C["alu_dark"], 4, (0, 0, -260), mat="al6061", bom="G7", mcm="KF40_CLAMP", section=True)
    add("Overflow-jar present sensor (inductive M12, PNP)", cyl(6.0, (ox + 28.0, 0, zf - 22 - 16 - 60), "x", 30.0), C["blue"], 4, (120, 0, 0), mat="misc", mass_kg=0.02, bom="A1")

    # ===================== 5. Chamber body =====================
    ch = rbox(-cx, cx, -cy, cy, -fl, lz0, 8)
    # inside corners: 5 mm on the vertical edges and a 5 mm cove where the walls meet the floor (powder doesn't pack
    # into a cove, and a vacuum nozzle or swab reaches it); the blade path (|y| <= 52) stays flat
    pocket = cq.Workplane("XY").box(2 * ix, 2 * iy, lz0 + 1, centered=False).edges("|Z").fillet(5.0).edges("<Z").fillet(5.0).val()
    ch = ch.cut(pocket.translate(V(-ix, -iy, 0)))
    dz0, dz1 = 8.0, 100.0                                   # door opening: sill 8 mm above the floor
    ch = ch.cut(box(-110, 110, -cy - 1, -iy + 1, dz0, dz1))
    ch = ch.cut(box(-MP.INLET_HALF, MP.INLET_HALF, iy - 1, cy + 1, 4, 12))     # cross-flow inlet slot (120 x 8, for the Ø75 module)
    ch = ch.cut(box(-MP.OUTLET_HALF, MP.OUTLET_HALF, MP.OUTLET_Y[0], MP.OUTLET_Y[1], -fl - 1, 1))   # outlet: floor slot near the door
    ch = ch.cut(cyl(P["port_d"] / 2, (0, 0, -fl - 1), "z", fl + 2))            # module port: every module's spigot fills it
    for sx in (-1, 1):                                                          # helical inserts for the module's thumb screws,
        ch = ch.cut(cyl(3.0, (sx * MP.SCREW_X, 0, -fl - 1), "z", 13.0))          # and the locating dowel / diamond pin holes
        ch = ch.cut(cyl(3.0, (0, sx * MP.DOWEL_Y, -fl - 1), "z", 11.0))
    ch = ch.cut(box(P["ovf_x0"], P["ovf_x1"], -52, 52, -fl - 1, 1))
    for sx in (-1, 1):                                                          # plate-at-exchange-height through-beam (fibre heads):
        ch = ch.cut(cyl(3.0, (sx * (ix - 1), 0, 5.0), "x" if sx > 0 else "-x", P["wall"] + 2))     # M6 x 0.75 tapped through the wall
        ch = ch.cut(cyl(5.4, (sx * (cx - 1.32), 0, 5.0), "x" if sx > 0 else "-x", 1.4).cut(cyl(3.1, (sx * (cx - 1.4), 0, 5.0), "x" if sx > 0 else "-x", 1.6)))   # 2-010 face groove
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    ch = ch.cut(cyl(9, (-cx - 1, ry_, rz_), "x", P["wall"] + 2)).cut(cyl(9, (ix - 1, ry_, rz_), "x", P["wall"] + 2))
    ch = ch.cut(cyl(12.7, (ix - 1, 0, 70), "x", P["wall"] + 2))        # vacuum port (KF-25)
    ch = sae_port(ch, (100, cy, 100), "-y", P["wall"])                  # argon in (back wall): SAE-4 O-ring-boss port, not NPT into 6061
    ch = sae_port(ch, (cx, -40, 18), "-x", P["wall"])                   # O2 sample (right wall): SAE-4 port
    gw, gd = P["gland_w"], P["gland_d"]                                # lid O-ring face gland in the top face
    ch = ch.cut(rbox(-ix - 3 - gw, ix + 3 + gw, -iy - 3 - gw, iy + 3 + gw, lz0 - gd, lz0 + 1, 6).cut(rbox(-ix - 3, ix + 3, -iy - 3, iy + 3, lz0 - gd - 1, lz0 + 2, 4)))
    add("Process chamber body (6061-T6, ~6.4 L)", ch, C["alu"], 5, (0, 0, 260), mat="al6061", bom="G1", mcm="PLATE_CHAMBER", section=True)
    # the cord as squeezed: 2.65 mm tall, ~3.7 mm wide, sitting in the 4.6 mm gland
    add("Lid O-ring (FKM 75A, 3.53 mm cord, 25 % squeeze)", rbox(-ix - 3.3 - 3.7, ix + 3.3 + 3.7, -iy - 3.3 - 3.7, iy + 3.3 + 3.7, lz0 - gd, lz0, 5.6).cut(rbox(-ix - 3.3, ix + 3.3, -iy - 3.3, iy + 3.3, lz0 - gd - 1, lz0 + 1, 4.3)),
        C["black"], 5, (0, 0, 300), mat="fkm", bom="G8", mcm="ORING_CORD", section=True)
    # 316L on 6061 cannot be welded: a 6 mm bolting flange, 8 x M4 (joints.py) and an FKM face O-ring round the opening
    plen_in = fuse([rbox(-65, 65, cy, cy + 32, -8, 30, 4), rbox(-75, 75, cy, cy + 6, -18, 40, 4, "|Y")]).cut(box(-60, 60, cy - 1, cy + 27, -3, 25)).cut(cyl(12.7, (0, cy + 26, 11), "y", 8))
    hi_in, ri_in = fit_loop((61.5, 15.5), 1.5)[0], 1.5                 # groove inner wall: >= 1.5 mm outside the plenum's opening (x +/-60, z -3..25)
    plen_in = plen_in.cut(ring_loop("y", (0, 0, 11), hi_in, F["width"], (cy - 0.01, cy + F["depth"]), ri_in))
    add("Cross-flow inlet plenum + nozzle (316L, bolted flange)", plen_in, C["ss"], 5, (0, 180, 0), mat="ss316l", bom="G4", section=True)
    pk = MP.pick_ring(loop_perimeter(hi_in, ri_in))
    add(f"Inlet plenum O-ring (FKM 75A {pk[0]}, face seal on the back wall)", ring_loop("y", (0, 0, 11), hi_in, F["width"] - 0.3, (cy, cy + F["depth"]), ri_in),
        C["black"], 5, (0, 180, 0), mat="fkm", bom="G8", section=True)
    GLANDS["inlet_plenum"] = dict(kind="face", ring=pk[0], cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=loop_perimeter(hi_in, ri_in),
                                  groove_mat="ss", T=45.0, closure="inlet plenum (316L) on the back wall (6061)")
    add("Inlet plenum port (KF-25)", place(kf_stub(25, 26), (0, cy + 32 + 20, 11), (1, 0, 0), (0, 1, 0)), C["ss"], 5, (0, 200, 0), mat="ss304", bom="G7", mcm="KF25_WELD")
    # flat (16 mm) under the module's path to the front, with a deeper boot at the right end for the KF-25 port
    y0o, y1o = MP.OUTLET_Y
    # 9 mm flanges along the slot carry an FKM face O-ring and 6 counterbored M4 screws up into the floor (joints.py)
    plo = fuse([rbox(-75, 84, y0o - 11, y1o + 11, zf - 16, zf, 3), rbox(72, 100, y0o - 12, y1o + 8, zf - 45, zf, 4)])
    plo = plo.cut(fuse([box(-63, 72, y0o - 1, y1o + 1, zf - 13, zf + 1), box(76, 96, y0o - 8, y1o + 4, zf - 41, zf - 3), box(60, 80, y0o - 1, y1o + 1, zf - 13, zf - 3)]))
    plo = plo.cut(cyl(12.7, (86, (y0o + y1o) / 2, zf - 46), "z", 6))
    hi_o, c_o = fit_loop((69.0, 6.5), 1.5, 2.0, 0.5)[0], (4.5, (y0o + y1o) / 2, 0.0)   # groove inner wall >= 1.5 mm outside the opening (x -63..72, y -95..-85)
    plo = plo.cut(ring_loop("z", c_o, hi_o, F["width"], (zf - F["depth"], zf + 0.01), 1.5))
    add("Cross-flow outlet plenum under the floor (316L, flat over the module path, bolted flange)", plo, C["ss"], 5, (0, 0, -180), mat="ss316l", bom="G4", section=True)
    pk = MP.pick_ring(loop_perimeter(hi_o, 1.5))
    add(f"Outlet plenum O-ring (FKM 75A {pk[0]}, face seal under the floor)", ring_loop("z", c_o, hi_o, F["width"] - 0.3, (zf - F["depth"], zf), 1.5),
        C["black"], 5, (0, 0, -180), mat="fkm", bom="G8", section=True)
    GLANDS["outlet_plenum"] = dict(kind="face", ring=pk[0], cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=loop_perimeter(hi_o, 1.5),
                                   groove_mat="ss", T=45.0, closure="outlet plenum (316L) under the floor (6061)")
    add("Outlet plenum port (KF-25)", place(kf_stub(25, 26), (86, (y0o + y1o) / 2, zf - 45 - 26), (1, 0, 0), (0, 0, 1)), C["ss"], 5, (180, 0, -180), mat="ss304", bom="G7", mcm="KF25_WELD")
    # 304 cannot be welded to the 6061 body: the KF-25 stub is welded into a 304 adapter plate that bolts on (4 x M5, joints.py)
    # over an FKM face O-ring (seals.md item 10)
    add("Vacuum port (KF-25, stub welded into the adapter plate)", place(kf_stub(25, 10), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), C["ss"], 5, (180, 0, 0), mat="ss304", bom="G7", mcm="KF25_WELD")
    vap = box(cx, cx + 8, -28, 28, 42, 98).cut(cyl(11.1, (cx - 1, 0, 70), "x", 10)).cut(tube(16.8, 14.5, (cx - 0.01, 0, 70), "x", F["depth"] + 0.01))
    add("Vacuum port adapter plate (304, 8 mm, FKM face O-ring)", vap, C["ss"], 5, (180, 0, 0), mat="ss304", bom="G7", section=True)
    add("Vacuum port adapter O-ring (FKM 75A 2-024)", tube(16.6, 14.5, (cx, 0, 70), "x", F["depth"]), C["black"], 5, (180, 0, 0), mat="fkm", bom="G8")
    GLANDS["vacuum_port"] = dict(kind="face", ring="2-024", cs=1.78, depth=F["depth"], width=2.3, groove_id=29.0, groove_mat="ss", T=40.0,
                                 closure="KF-25 vacuum-port adapter plate on the right wall")
    add("Layer-light LED bar", box(ix - 6, ix - 1, -45, 45, 30, 38), C["white"], 5, (0, 0, 120), mat="misc", mass_kg=0.05, bom="M6")
    # lift-out wall liners: 0.5 mm 316L held by spring clips; they take the condensate and lift out through the door
    ry_, rz_ = P["rc_screw_y"], P["rc_screw_z"]
    lb = box(-ix + 8, ix - 8, iy - 0.6, iy - 0.1, 16, 72)
    ll = box(-ix + 0.1, -ix + 0.6, -iy + 8, iy - 8, 16, 110).cut(cyl(11, (-ix - 1, ry_, rz_), "x", 3))
    lr = box(ix - 0.6, ix - 0.1, -iy + 8, iy - 8, 16, 110).cut(cyl(11, (ix - 2, ry_, rz_), "x", 3)).cut(cyl(14, (ix - 2, 0, 70), "x", 3)).cut(cyl(4.5, (ix - 2, -40, 18), "x", 3))
    add("Lift-out wall liners (0.5 mm 316L, back + sides, spring clips)", comp([lb, ll, lr]), C["ss"], 5, (0, 0, 160), mat="ss316l", bom="A2", section=True, opacity=0.8)
    # threaded M6 fibre heads screwed into the walls from outside, each sealed by a 2-010 FKM face O-ring under its flange
    fib = comp([fuse([cyl(2.98, (sx * (ix + 1.0), 0, 5.0), "x" if sx > 0 else "-x", P["wall"] - 1.0), cyl(6.5, (sx * cx, 0, 5.0), "x" if sx > 0 else "-x", 2.5),
                      cyl(3.0, (sx * (cx + 2.5), 0, 5.0), "x" if sx > 0 else "-x", 19.5)]) for sx in (-1, 1)])
    add("Plate-height through-beam (M6 threaded fibre heads in the side walls, z +5 mm)", fib, C["blue"], 5, (0, 0, 0), mat="misc", mass_kg=0.03, bom="A1")
    add("Fibre-head O-rings (2 x FKM 75A 2-010, face seals)", comp([tube(5.3, 3.1, ((cx - 1.32) if sx > 0 else -cx, 0, 5.0), "x", 1.32) for sx in (-1, 1)]), C["black"], 5, (0, 0, 0), mat="fkm", bom="A1")
    GLANDS["fibre_heads"] = dict(kind="face", ring="2-010", cs=1.78, depth=1.32, width=2.3, groove_id=6.2, groove_mat="al", T=45.0, n=2,
                                 closure="threaded fibre heads in the side walls")
    th = math.radians(200.0)
    add("Module-present sensor (inductive M12, under the floor, sees the module flange)", cyl(6.0, (52.5 * math.cos(th), 52.5 * math.sin(th), zf - 6.5), (math.cos(th), math.sin(th), 0), 30.0),
        C["blue"], 5, (0, 0, -120), mat="misc", mass_kg=0.02, bom="A1")

    # ===================== 6. Recoater =====================
    rr = place(guide_rail(270.0, 15.0, 15.0), (-135, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0))
    add("Recoater guide rail (15 mm, 270 mm)", rr, C["steel"], 6, (0, 0, 220), mat="steel", bom="M1", mcm="6709K33")
    xc = P["x_park"]
    add("Recoater carriage (15 mm rail)", place(guide_carriage(57.0, 34.0, 28.0, 3.0, 15.0, 15.0), (xc, iy, P["rc_rail_z"]), (1, 0, 0), (0, -1, 0)), C["steel"], 6, (0, 0, 220), group="recoater", mat="steel", bom="M1", mcm="6709K12")
    yc = iy - 28.0                                              # carriage mounting face
    # the Ø75 blade is 104 mm long, so the holder cantilevers ~106 mm from the arm (66 mm before): 18 x 31 instead of
    # 18 x 19 keeps the tip deflection near the 3.4 um the FEA found for the short holder (L^3 / h^3)
    holder = rbox(xc - 9, xc + 9, -P["dose_y"] - 3, iy - 34, 3.0 + P["blade_gap"], 34, 2, "|Y")
    bl = box(xc + 9, xc + 10.5, -P["dose_y"] - 2, P["dose_y"] + 2, P["blade_gap"], 18.0)
    blk = fuse([box(xc - 22, xc + 22, iy - 42, yc, 25, P["rc_rail_z"] + 17), box(xc - 22, xc + 22, yc, iy - 3, 25, P["rc_rail_z"] - 18)])
    blk = blk.cut(cyl(12.0, (xc - 23, ry_, rz_), "x", 46)).cut(holder)
    add("Recoater carriage block (6061)", blk, C["alu"], 6, (0, 0, 220), group="recoater", mat="al6061", bom="M1")
    # the screw now ends inside the left wall's bore, where a clamp coupling joins it to the feedthrough's vacuum-side shaft
    xs0 = -cx + FERRO["vac_shaft"] - FERRO["spacer"]
    add("Recoater ball screw (M12, 10 mm lead)", place(ball_screw(cx + 5 - xs0, 12.0, 8.0, 11.0), (xs0, ry_, rz_), (1, 0, 0), (0, 0, 1)), C["steel"], 6, (0, 0, 220), mat="steel", bom="M1", mcm="4566N101")
    add("Recoater ball nut (flange on the +x face)", place(ball_nut(12.0, 23.0, 43.0, 40.0, 10.0, None), (xc + 10.5, ry_, rz_), (-1, 0, 0), (0, 0, 1)), C["steel"], 6, (0, 0, 220), group="recoater", mat="steel", bom="M1", mcm="4566N401")
    # stiffened after FEA (analysis/out/fea): a 12 x 8 arm and 14 x 11 holder let the blade deflect 17 um under a 10 N
    # spreading load; a 40 x 14 web and an 18 x 19 holder bring it to 3.4 um (< 5 um, 1/6 of a 30 um layer)
    add("Recoater arm (6061, 40 x 14 web)", box(xc - 20, xc + 20, iy - 42, iy - 28, 14, 25).cut(holder).cut(bl), C["alu"], 6, (0, 0, 220), group="recoater", mat="al6061", bom="M5")
    add("Blade holder (6061, 18 x 31, quick-swap)", holder, C["anod"], 6, (0, 0, 220), group="recoater", mat="al6061", bom="M5")
    # default blade: HSS, 1.5 mm, wide (rounded) nose; EOS's standard blade for AlSi10Mg. Compliant FKM or silicone
    # cords and a carbon brush are the swap-in options (silicone only where Si pickup does not matter).
    add("HSS recoater blade (1.5 mm, wide nose)", bl, C["steel"], 6, (0, 0, 220), group="recoater", mat="steel", bom="M5", mcm="9011K104")
    # left: a magnetic-fluid rotary feedthrough (its own bearings take the screw's axial load) flange-mounted on the wall over an FKM
    # face O-ring, instead of a bearing + PTFE V-ring (a V-ring is a dirt excluder, not a vacuum seal: seals.md item 8)
    FT = FERRO
    x_sp = -cx - FT["spacer"]
    x_f = x_sp - FT["flange_t"]
    ft = fuse([cyl(FT["flange_d"] / 2, (x_f, ry_, rz_), "x", FT["flange_t"]), cyl(FT["body_d"] / 2, (x_f - FT["body_l"], ry_, rz_), "x", FT["body_l"]),
               cyl(FT["shaft_d"] / 2, (x_f - FT["body_l"] - FT["air_shaft"], ry_, rz_), "x", FT["air_shaft"]),
               cyl(FT["shaft_d"] / 2, (x_sp, ry_, rz_), "x", FT["vac_shaft"])])
    sp = tube(FT["flange_d"] / 2, 9.0, (x_sp, ry_, rz_), "x", FT["spacer"]).cut(tube(14.5 + 2.3, 14.5, (-cx - 1.35, ry_, rz_), "x", 1.36))
    sp = sp.cut(tube(14.5 + 2.3, 14.5, (x_sp - 0.01, ry_, rz_), "x", 1.36))
    add("Recoater feedthrough spacer ring (6061, 9 mm, FKM face O-rings both sides)", sp, C["anod"], 6, (-160, 0, 0), mat="al6061", bom="M1")
    add(f"Recoater fixed bearing: {FT['label']} on the left wall ({FT['pn'] or 'envelope'}; FKM face O-ring)", ft, C["anod"], 6, (-160, 0, 0), mat="misc", mass_kg=0.45, bom="M1", mcm=FT["pn"])
    add(f"Recoater feedthrough O-rings (2 x FKM 75A {FT['oring']}, spacer to wall and to flange)", comp([tube(16.6, 14.5, (-cx - 1.32, ry_, rz_), "x", 1.32),
        tube(16.6, 14.5, (x_sp, ry_, rz_), "x", 1.32)]), C["black"], 6, (-160, 0, 0), mat="fkm", bom="M1")
    GLANDS["recoater_feedthrough"] = dict(kind="face", ring=FT["oring"], cs=1.78, depth=1.32, width=2.3, groove_id=29.0, groove_mat="ss", T=40.0,
                                          closure="recoater feedthrough flange on the left wall")
    add("Recoater shaft coupling (clamp type, 6 to 8 mm, in the wall bore)", fuse([tube(7.0, FT["shaft_d"] / 2, (xs0 - 7.0, ry_, rz_), "x", 7.0), tube(7.0, 4.0, (xs0, ry_, rz_), "x", 7.0)]),
        C["steel"], 6, (-160, 0, 0), mat="steel", bom="M1")
    # right: the screw's free end runs in a blind bearing cap bolted to the wall over an FKM face O-ring (no rotary seal)
    bcap = cyl(20, (cx, ry_, rz_), "x", 14).cut(cyl(4.0, (cx - 1, ry_, rz_), "x", 11)).cut(tube(12.7, 10.4, (cx - 0.01, ry_, rz_), "x", 1.33))
    add("Recoater floating bearing housing (blind cap, FKM face O-ring)", bcap, C["anod"], 6, (160, 0, 0), mat="al6061", bom="M1")
    add("Recoater bearing-cap O-ring (FKM 75A 2-019)", tube(12.5, 10.4, (cx, ry_, rz_), "x", 1.32), C["black"], 6, (160, 0, 0), mat="fkm", bom="M1")
    GLANDS["recoater_cap"] = dict(kind="face", ring="2-019", cs=1.78, depth=1.32, width=2.3, groove_id=20.8, groove_mat="al", T=40.0,
                                  closure="blind bearing cap on the right wall")
    x_m = x_f - FT["body_l"] - FT["air_shaft"]                         # end of the feedthrough's air-side shaft
    x_m0 = min(x_m - 25.0, -cx - 101.0)                                # servo mount face (was -cx - 60 before the feedthrough)
    add("Recoater motor standoff", tube(30, 26, (x_m0, ry_, rz_), "x", x_m - x_m0), C["alu_dark"], 6, (-200, 0, 0), mat="al6061", bom="M1")
    rmot = place(servo_nema23(100.0, 20.0), (x_m0, ry_, rz_), (0, 1, 0), (1, 0, 0))
    add("Recoater servo (ClearPath-SD, NEMA 23)", rmot, C["motor"], 6, (-260, 0, 0), mat="misc", mass_kg=1.6, bom="M2")
    add("Recoater motor bracket", box(max(x_m0 - 90.0, -347.0), x_m0, ry_ - 30, ry_ + 30, zb1, rz_ - 28.6), C["alu_dark"], 6, (-260, 0, 0), mat="al6061", bom="M1")

    # ===================== 7. Lid =====================
    lid = rbox(-cx, cx, -cy, cy, lz0, lz1, 8)
    lid = lid.cut(cyl(28, (0, 0, lz0 - 1), "z", P["lid"] + 2))
    xd = P["x_dose"]
    lid = lid.cut(box(xd - 6, xd + 6, -P["dose_y"], P["dose_y"], lz0 - 1, lz1 + 1))
    cam_p = V(75, -45, lz1)
    lid = lid.cut(cyl(11, (75, -45, lz0 - 1), "z", P["lid"] + 2))
    for (x, y) in [(100, 50), (40, 70)]:                     # pressure transducer, relief valve: SAE-4 O-ring-boss ports
        lid = sae_port(lid, (x, y, lz1), "-z", P["lid"])
    dz0, dz1 = lz0 + 5.0, lz0 + 11.0                       # cover-slide drawer slot through the lid's front edge
    lid = lid.cut(box(-36, 36, -cy - 1, 35, dz0, dz1))
    QT = QTURN
    x_qt = 51.0                                            # drawer latch receptacles: between the lid screws at x 42 and 60
    for sx in (-1, 1):
        lid = lid.cut(cyl(QT["rec_d"] / 2, (sx * x_qt, -cy - 0.01, lz0 + 8.0), "y", QT["rec_l"] + 0.01))
    add("Chamber lid (6061-T6, 16 mm, cover-slide drawer slot)", lid, C["alu"], 7, (0, 0, 300), mat="al6061", bom="G1", mcm="PLATE_CHAMBER", section=True)
    # lid screws: joints.py (20 x M5 x 25, 316, into helical inserts in the body)
    # window (seals.md item 3): an O-ring sandwich. The window sits on a 2-031 FKM O-ring in a groove in the seat; a 1 mm FKM flat
    # ring on top; the retaining ring's spigot presses that ring to 0.75 mm when the ring bottoms metal-to-metal on the flange, so
    # the squeeze is set by the geometry, not the screw torque. A 2-036 FKM face O-ring seals the flange to the lid.
    zs = lz1 + 12.0                                        # window seat
    wf = tube(50, 21, (0, 0, lz1), "z", 22).cut(cyl(25.6, (0, 0, zs), "z", 11))
    wf = wf.cut(tube(22.45 + F["width"], 22.45, (0, 0, zs - F["depth"]), "z", F["depth"] + 0.01))          # lower window O-ring groove (2-031)
    wf = wf.cut(tube(30.8 + F["width"], 30.8, (0, 0, lz1 - 0.01), "z", F["depth"] + 0.01))                 # flange-to-lid face groove (2-036)
    add("Window flange (6061, two FKM O-ring grooves)", wf, C["anod"], 7, (0, 0, 360), mat="al6061", bom="L7", section=True)
    add("Ø2 in. fused-silica window, 8 mm, AR 1064", cyl(25.4, (0, 0, zs), "z", 8), C["glass"], 7, (0, 0, 380), mat="fused_silica", bom="L7", opacity=0.45, section=True)
    add("Window O-ring, lower (FKM 75A 2-031, under the window)", tube(22.45 + F["width"] - 0.3, 22.45, (0, 0, zs - F["depth"]), "z", F["depth"]), C["black"], 7, (0, 0, 370), mat="fkm", bom="G8", section=True)
    add("Window clamp ring, upper (FKM 75A sheet, 1.0 mm, squeezed to 0.75)", tube(25.3, 22.2, (0, 0, zs + 8.0), "z", 0.75), C["black"], 7, (0, 0, 390), mat="fkm", bom="G8", section=True)
    add("Window-flange O-ring (FKM 75A 2-036, face seal on the lid)", tube(30.8 + F["width"] - 0.3, 30.8, (0, 0, lz1), "z", F["depth"]), C["black"], 7, (0, 0, 350), mat="fkm", bom="G8", section=True)
    GLANDS["window_lower"] = dict(kind="face", ring="2-031", cs=1.78, depth=F["depth"], width=F["width"], groove_id=44.9, groove_mat="al", T=80.0, closure="window on its seat")
    GLANDS["window_flange"] = dict(kind="face", ring="2-036", cs=1.78, depth=F["depth"], width=F["width"], groove_id=61.6, groove_mat="al", T=60.0, closure="window flange on the lid")
    rrb = fuse([tube(50, 22, (0, 0, lz1 + 22), "z", 5), tube(25.4, 22, (0, 0, zs + 8.75), "z", lz1 + 22 - zs - 8.75)])
    add("Window retaining ring (spigot bottoms metal-to-metal: squeeze set by geometry)", rrb, C["anod"], 7, (0, 0, 400), mat="al6061", bom="L7", section=True)
    add("Field-stop aperture (Ø36, passive beam limit)", tube(27.9, 18, (0, 0, dz1), "z", lz1 - dz1), C["black"], 7, (0, 0, 300), mat="al6061", bom="L7", section=True)
    # cover-slide drawer: pulls out of the lid's front edge (a person or the robot through the guard door) without
    # lifting the lid; an FKM O-ring on its front plate seals it against the lid. Only opened at atmosphere.
    drw = box(-35.5, 35.5, -cy, 33.5, dz0 + 0.3, dz1 - 0.3).cut(cyl(25.6, (0, 0, dz0), "z", 7)).cut(cyl(23.0, (0, 0, dz0 - 1), "z", 8))
    # front plate widened to x +/-64 for two quarter-turn latches; 1.78 mm FKM ring in a half-dovetail groove round the slot (item 4)
    fp = rbox(-64, 64, -cy - 8, -cy, lz0 - 2, lz1, 3)                   # top at the lid's top: clears the front lid screws' heads
    hd_r = 1.5
    hd_w, hd_h = [2 * v for v in fit_loop((37.0, 4.5), hd_r, 1.5, 0.5)[0]]   # groove inner wall: >= 1 mm outside the slot (72 x 6, z 125..131)
    fp = fp.cut(dovetail_loop((0, -cy, (dz0 + dz1) / 2), (0, 1, 0), (1, 0, 0), hd_w, hd_h, hd_r, F["width"], F["depth"], MP.DOVETAIL_DEG))
    for sx in (-1, 1):
        fp = fp.cut(cyl(QT["stud_d"] / 2 + 0.25, (sx * x_qt, -cy - 8.01, lz0 + 8.0), "y", 8.02))
    drw = fuse([drw, fp, box(-20, 20, -cy - 20, -cy - 8, dz0 + 1, dz1 - 1), box(-20, -14, -cy - 20, -cy - 8, lz0 + 1, lz1 - 1), box(14, 20, -cy - 20, -cy - 8, lz0 + 1, lz1 - 1)])
    add("Cover-slide drawer (6061, robot pull tab, half-dovetail seal groove)", drw, C["anod"], 7, (0, -200, 0), group="drawer", mat="al6061", bom="A2", section=True)
    add("Cover slide (Ø2 in. x 3 mm fused silica, consumable)", cyl(25.4, (0, 0, dz0 + 1.0), "z", 3.0), C["glass"], 7, (0, -200, 0), group="drawer", mat="fused_silica", bom="A2", opacity=0.5, section=True)
    per = loop_perimeter((hd_w / 2, hd_h / 2), hd_r)
    pk = MP.pick_ring(per)
    add(f"Drawer O-ring (FKM 75A {pk[0]} in a half-dovetail groove, seals on the lid's front face)",
        ring_loop("y", (0, 0, (dz0 + dz1) / 2), (hd_w / 2 + 0.1, hd_h / 2 + 0.1), 1.5, (-cy - F["depth"], -cy), hd_r + 0.1), C["black"], 7, (0, -200, 0), group="drawer", mat="fkm", bom="A2")
    GLANDS["drawer"] = dict(kind="face", ring=pk[0], cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=per, groove_mat="al", T=60.0, dovetail=True,
                            closure="cover-slide drawer on the lid's front face")
    qs = [fuse([cyl(QT["head_d"] / 2, (sx * x_qt, -cy - 8.0 - QT["head_t"], lz0 + 8.0), "y", QT["head_t"]),
                cyl(QT["stud_d"] / 2, (sx * x_qt, -cy - 8.0, lz0 + 8.0), "y", 8.0 + QT["rec_l"] - 1.0)]) for sx in (-1, 1)]
    add(f"Drawer latches: 2 x {QT['label']} studs ({QT['pn'] or 'envelope'})", comp(qs), C["ss"], 7, (0, -200, 0), group="drawer", mat="ss304", mass_kg=0.02, bom="A2", mcm=QT["pn"])
    add(f"Drawer latch receptacles in the lid (2 x {QT['label']})", comp([tube(QT["rec_d"] / 2, QT["stud_d"] / 2, (sx * x_qt, -cy, lz0 + 8.0), "y", QT["rec_l"]) for sx in (-1, 1)]),
        C["ss"], 7, (0, -200, 0), mat="ss304", mass_kg=0.01, bom="A2")
    add("Drawer-closed sensor (inductive M12, on the lid's front face, sees the plate's end)", cyl(6.0, (66.0, -cy - 7.0, lz0 + 8.0), "x", 30.0), C["blue"], 7, (0, -200, 0), mat="misc", mass_kg=0.02, bom="A1")
    add("Gas knife (cover-slide purge, 316L)", box(-32, 32, -42, -36, lz0 - 14, lz0 - 8), C["ss"], 7, (0, 0, 200), mat="ss316l", bom="L7", section=True)
    # chute ends 37 mm above the floor so the deeper (31 mm) blade holder passes under it
    chute = box(xd - 6, xd + 6, -P["dose_y"], P["dose_y"], 37, lz0).cut(box(xd - 4.5, xd + 4.5, -P["dose_y"] + 1.5, P["dose_y"] - 1.5, 36, lz0 + 1))
    add("Dose chute (316L)", chute, C["ss"], 7, (0, 0, 260), mat="ss316l", bom="M4", section=True)
    # metering base (fixed): fluted roller along Y over the full Ø75 dose line, its own shaft seal and stepper; the
    # reservoirs dock on top. Each reservoir's outlet slot (45 / 70 / 95 mm) sets the active dose length.
    zd = lz1 + 44.0                                         # dock face
    dox, doy = MP.DOCK_OPENING
    mb = rbox(xd - 17, xd + 17, -62, 62, lz1, zd, 3).cut(box(xd - dox / 2, xd + dox / 2, -doy / 2, doy / 2, zd - 10, zd + 1))   # dose opening into the roller
    mb = mb.cut(box(xd - 17.01, xd - 14, -28, -8, zd - 22, zd - 3))                     # NFC antenna pocket in the -x side face (outside the seals)
    rzc = lz1 + 28.0
    mb = mb.cut(cyl(4.0, (xd, 62.0 - FERRO_S["nose_l"], rzc), "y", FERRO_S["nose_l"] + 0.5)).cut(cyl(3.0, (xd, 62.0 - 25.0, rzc), "y", 25.0 - FERRO_S["nose_l"] + 0.1))
    mb = mb.cut(tube(4.75 + 2.3, 4.75, (xd, 62.0 - 1.35, rzc), "y", 1.36))           # 2-012 face groove for the roller feedthrough
    mb = fuse([mb, rbox(xd - 17, xd + 17, -72, -60, lz1, lz1 + 8, 3), rbox(xd - 17, xd + 17, 60, 72, lz1, lz1 + 8, 3)])   # screw tabs
    # face O-rings: under the base round the lid's 12 x 100 dose slot, and in the dock face round the dose opening (reservoir seal)
    hi_m = fit_loop((dox / 2 + 1.5, doy / 2 + 1.5), 1.5, 2.0, 0.5)[0]
    mb = mb.cut(ring_loop("z", (xd, 0, 0), hi_m, F["width"], (lz1 - 0.01, lz1 + F["depth"]), 1.5))
    mb = mb.cut(ring_loop("z", (xd, 0, 0), hi_m, F["width"], (zd - F["depth"], zd + 0.01), 1.5))
    add("Metering base (6061, fluted roller over a 100 mm dose line, two FKM face O-rings)", mb, C["alu"], 7, (0, 0, 300), mat="al6061", bom="M4", section=True)
    per = loop_perimeter(hi_m, 1.5)
    pk = MP.pick_ring(per)
    add(f"Metering-base O-ring on the lid (FKM 75A {pk[0]}, round the dose slot)", ring_loop("z", (xd, 0, 0), hi_m, F["width"] - 0.3, (lz1, lz1 + F["depth"]), 1.5),
        C["black"], 7, (0, 0, 300), mat="fkm", bom="M4")
    add(f"Metering-base dock-face O-ring (FKM 75A {pk[0]}, seals the reservoir's base plate)", ring_loop("z", (xd, 0, 0), hi_m, F["width"] - 0.3, (zd - F["depth"], zd), 1.5),
        C["black"], 7, (0, 0, 300), mat="fkm", bom="M4")
    GLANDS["metering_base"] = dict(kind="face", ring=pk[0], cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=per, groove_mat="al", T=45.0,
                                   closure="metering base on the lid (4 x M4)")
    GLANDS["reservoir_dock"] = dict(kind="face", ring=pk[0], cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=per, groove_mat="al", T=45.0,
                                    closure="reservoir base plate on the dock face (wedge rails + detent)")
    add("NFC reader antenna (in the dock's side face, reads the tag on the reservoir plate's edge)", box(xd - 16.5, xd - 14.0, -27.5, -8.5, zd - 21.5, zd - 3.5), C["pcb"], 7, (0, 0, 300), mat="misc", mass_kg=0.01, bom="A1")
    # rails with 2 mm lips over the plate's edges; the lips' undersides carry the 2 deg docking ramps (not drawn: 0.5 mm over 15 mm)
    add("Dovetail rails for the reservoirs (lips pull the plate onto the dock O-ring)",
        comp([fuse([box(xd - 19, xd - 15, -62, 62, zd, zd + 6), box(xd - 19, xd - 13, -62, 62, zd + MP.GATE_T, zd + 6)]),
              fuse([box(xd + 15, xd + 19, -62, 62, zd, zd + 6), box(xd + 13, xd + 19, -62, 62, zd + MP.GATE_T, zd + 6)])]), C["ss"], 7, (0, 0, 320), mat="ss316l", bom="M4")
    rzc = lz1 + 28.0                                        # roller axis; the stepper clears the lid screws
    FS_ = FERRO_S
    yb = 62.0                                                           # metering base back face
    rft = fuse([cyl(FS_["nose_d"] / 2 - 0.02, (xd, yb - FS_["nose_l"], rzc), "y", FS_["nose_l"]), cyl(FS_["body_d"] / 2, (xd, yb, rzc), "y", FS_["body_l"]),
                cyl(FS_["shaft_d"] / 2, (xd, yb + FS_["body_l"], rzc), "y", FS_["air_shaft"]),
                cyl(FS_["shaft_d"] / 2, (xd, yb - FS_["nose_l"] - FS_["vac_shaft"], rzc), "y", FS_["vac_shaft"])])
    add(f"Roller shaft: {FS_['label']} in the metering base (M8 x 1 nose; FKM face O-ring)", rft, C["anod"], 7, (0, 160, 300), mat="misc", mass_kg=0.06, bom="M4", mcm=FS_["pn"])
    add(f"Roller feedthrough O-ring (FKM 75A {FS_['oring']}, under the housing's shoulder)", tube(7.0, 4.75, (xd, yb - 1.32, rzc), "y", 1.32), C["black"], 7, (0, 160, 300), mat="fkm", bom="M4")
    GLANDS["roller_feedthrough"] = dict(kind="face", ring=FS_["oring"], cs=1.78, depth=1.32, width=2.3, groove_id=9.5, groove_mat="al", T=45.0,
                                        closure="roller feedthrough in the metering base")
    ys = yb + FS_["body_l"] + FS_["air_shaft"] + 14.0                    # stepper face: room for a 5 to 5 mm coupling
    add("Roller drive coupling (5 mm to 5 mm)", tube(6.0, 2.5, (xd, yb + FS_["body_l"] + 1.0, rzc), "y", FS_["air_shaft"] + 11.0), C["steel"], 7, (0, 160, 300), mat="steel", bom="M4")
    add("Dosing stepper (NEMA 17)", place(stepper_nema17(40), (xd, ys, rzc), (1, 0, 0), (0, -1, 0)), C["motor"], 7, (0, 160, 300), mat="misc", mass_kg=0.32, bom="M4", mcm="6627T91")
    add("Side reservoir port (KF-16 flange machined in the 6061 base, blanked; reserved for a >= 500 cm3 reservoir beside the chamber with an auger)",
        place(kf_stub(16, 18), (xd - 17 - 18, 35, rzc), (0, 1, 0), (-1, 0, 0)), C["ss"], 7, (-120, 0, 0), mat="ss304", bom="R1")
    add("Reservoir-docked sensor (inductive M12, at the back of the dock)", cyl(6.0, (xd, 60.0, zd + 14.0), "y", 30.0), C["blue"], 7, (0, 160, 300), mat="misc", mass_kg=0.02, bom="A1")
    _RES = dict(ML.add_reservoir(sys.modules[__name__], add, reservoir, xd, zd, 7), key=reservoir)
    add("Load cell (single-point, 2 kg, carries the dock rails: reservoir inventory)", box(xd + 17, xd + 30, -6, 6, lz1, zd), C["ss"], 7, (0, 0, 380), mat="steel", bom="M4", mcm="LOADCELL_SP")
    d = (V(0, 0, 0) - cam_p).normalized()
    up = d * -1
    # camera viewport (item 10): a 2-022 FKM face O-ring under the adapter (4 x M3, joints.py); at the top of the boss a Ø1 in.
    # window on a 2-017 FKM O-ring, held by a screwed retaining ring that bottoms on the boss over a 1 mm FKM flat ring
    # the boss now runs on the line of sight through the lid hole (it was 6.5 mm off it, so the old Ø22 bore broke through its wall)
    adp = cyl(25, (75, -45, lz1), "z", 12).cut(tube(12.9 + F["width"], 12.9, (75, -45, lz1 - 0.01), "z", F["depth"] + 0.01))
    t_b0 = 12.0 / up.z                                     # where the line of sight leaves the adapter's top face
    bl_ = 26.0
    t_top = t_b0 + bl_
    tb = t_b0 - 3.9                                        # the boss starts inside the adapter, clear of the lid
    boss = fuse([adp, cq.Solid.makeCylinder(16, t_top - tb, cam_p + up * tb, up), cq.Solid.makeCylinder(16.5, 6.0, cam_p + up * (t_top - 6.0), up)])
    boss = boss.cut(cq.Solid.makeCylinder(11, 20 + t_top - 8.0, cam_p - up * 20, up))           # Ø22 bore
    boss = boss.cut(cq.Solid.makeCylinder(7.5, 10, cam_p + up * (t_top - 8.5), up))             # Ø15 aperture under the window
    w_top = cam_p + up * t_top
    zw0 = w_top - up * 3.75                                                                      # window seat (3 mm window + 0.75 squeezed ring)
    boss = boss.cut(cq.Solid.makeCylinder(12.8, 3.76, zw0, up))
    boss = boss.cut(cq.Solid.makeCylinder(8.8 + 2.3, 1.33, zw0 - up * 1.32, up).cut(cq.Solid.makeCylinder(8.8, 1.4, zw0 - up * 1.35, up)))   # 2-017 groove
    add("Camera viewport adapter + boss (6061; Ø1 in. window, 1070 nm blocking filter; FKM face O-rings)", boss, C["anod"], 7, (0, 0, 300), mat="al6061", bom="M6")
    add("Camera adapter O-ring (FKM 75A 2-022, face seal on the lid)", tube(12.9 + F["width"] - 0.3, 12.9, (75, -45, lz1), "z", F["depth"]), C["black"], 7, (0, 0, 300), mat="fkm", bom="M6")
    add("Camera window (Ø1 in. x 3 mm fused silica, 1070 nm blocking coating)", cq.Solid.makeCylinder(12.7, 3.0, zw0, up), C["glass"], 7, (0, 0, 330), mat="fused_silica", bom="M6", opacity=0.5)
    add("Camera window O-ring (FKM 75A 2-017, under the window)", cq.Solid.makeCylinder(8.8 + 2.0, 1.32, zw0 - up * 1.32, up).cut(cq.Solid.makeCylinder(8.8, 1.4, zw0 - up * 1.35, up)),
        C["black"], 7, (0, 0, 330), mat="fkm", bom="M6")
    add("Camera window flat ring (FKM 75A sheet, 1.0 mm, squeezed to 0.75)", cq.Solid.makeCylinder(12.6, 0.75, zw0 + up * 3.0, up).cut(cq.Solid.makeCylinder(9.0, 1.0, zw0 + up * 2.9, up)),
        C["black"], 7, (0, 0, 330), mat="fkm", bom="M6")
    rr_c = cq.Solid.makeCylinder(16.5, 3.0, w_top, up).cut(cq.Solid.makeCylinder(9.0, 3.2, w_top - up * 0.1, up))
    add("Camera window retaining ring (bottoms metal-to-metal on the boss)", rr_c, C["anod"], 7, (0, 0, 335), mat="al6061", bom="M6")
    GLANDS["camera_adapter"] = dict(kind="face", ring="2-022", cs=1.78, depth=F["depth"], width=F["width"], groove_id=25.8, groove_mat="al", T=45.0, closure="camera adapter on the lid")
    GLANDS["camera_window"] = dict(kind="face", ring="2-017", cs=1.78, depth=F["depth"], width=F["width"], groove_id=17.6, groove_mat="al", T=45.0, closure="camera window on the boss")
    cam_base = w_top + up * 3.0
    cam = comp([cq.Solid.makeCylinder(15, 38, cam_base, up),
                place(box(-19, 19, -19, 19, 0, 8), (cam_base + up * 38).toTuple(), (0, 1, 0), up.toTuple())])
    add("Layer camera (Pi HQ + C-mount lens)", cam, C["black"], 7, (0, 0, 340), mat="misc", mass_kg=0.15, bom="M6")
    # both screw into SAE-4 (7/16-20) O-ring-boss ports in the lid, each sealed by an AS568-904 FKM O-ring in the port's chamfer
    add("Pressure transducer (7/16-20 SAE-4 O-ring-boss port)", comp([cyl(5.5, (100, 50, lz1 - 9.0), "z", 9.0), cyl(7.9, (100, 50, lz1), "z", 12), cyl(11, (100, 50, lz1 + 12), "z", 52)]), C["ss"], 7, (0, 0, 300), mat="ss316l", bom="G7", mcm="TRANSDUCER")
    add("Overpressure relief valve (316 SS, FKM seat, +34 mbar; SAE-4 O-ring-boss port)", comp([cyl(5.5, (40, 70, lz1 - 9.0), "z", 9.0), cyl(7.9, (40, 70, lz1), "z", 10), cyl(9, (40, 70, lz1 + 10), "z", 28)]), C["ss"], 7, (0, 0, 300), mat="ss316l", bom="G7", mcm="RELIEF")
    GLANDS["sae4_ports"] = dict(kind="sae", ring="3-904", cs=1.83, n=4, closure="SAE-4 O-ring-boss ports: argon in, O2 sample, transducer, relief valve")

    # ===================== 8. Drop-down door =====================
    dy1 = -cy
    dy0 = dy1 - 15.0
    # door seal (item 2): 1.78 mm FKM 75A cord (spliced ring) in a half-dovetail groove, Parker depth 1.32, width 2.3; the
    # groove's centre line is the old 232 x 104 rectangle. Two ears at the top corners carry the draw latches' strikes.
    LT = LATCH_1807A61
    zl_c = 54.0                                            # latch centre line at the seal's centroid height: with floating hinges the
                                                           # latches alone set the squeeze, so they pull the door flat (seals.md)
    door = fuse([rbox(-124, 124, dy0, dy1, -6, 114, 6, "|Y")] + [box(sx * 124.0 if sx > 0 else -cx, cx if sx > 0 else -124.0, dy0, dy1, zl_c - 18.0, zl_c + 18.0) for sx in (-1, 1)])
    dw_in, dh_in, dr_in = 232.0 - 2.3, 104.0 - 2.3, 4.4
    door = door.cut(dovetail_loop((0, dy1, 54.0), (0, 1, 0), (1, 0, 0), dw_in, dh_in, dr_in, F["width"], F["depth"], MP.DOVETAIL_DEG))
    add("Chamber door (6061-T6, 15 mm, drops down; half-dovetail seal groove, latch ears)", door, C["alu"], 8, (0, -240, 0), group="door", mat="al6061", bom="G1", mcm="PLATE_CHAMBER", section=True)
    add("Door O-ring (FKM 75A 1.78 mm cord, vulcanized splice, in a half-dovetail groove)",
        ring_loop("y", (0, 0, 54.0), (dw_in / 2 + 0.1, dh_in / 2 + 0.1), 1.5, (dy1 - F["depth"], dy1), dr_in + 0.1), C["black"], 8, (0, -200, 0), group="door", mat="fkm", bom="G8", mcm="ORING_CORD", section=True)
    GLANDS["door"] = dict(kind="face", ring="cord", cs=1.78, depth=F["depth"], width=F["width"], inner_perimeter=loop_perimeter((dw_in / 2, dh_in / 2), dr_in),
                          groove_mat="al", T=60.0, dovetail=True, closure="chamber door")
    hy, hz = dy0 - 6.0, -12.0                              # hinge axis (parallel to X) in front of the door's bottom edge
    DOOR_HINGE = (hy, hz)
    hx = (-100.0, 80.0)
    leaves = []
    for x in hx:                                           # door leaf + middle knuckle, rotates with the door; the pin hole is a
        # slot +/-0.6 mm across the door (y) so the door floats onto its seal and the latches, not the hinge, set the squeeze
        kslot = fuse([cyl(2.6, (x - 1, hy - 0.6, hz), "x", 22), cyl(2.6, (x - 1, hy + 0.6, hz), "x", 22), box(x - 1, x + 21, hy - 0.6, hy + 0.6, hz - 2.6, hz + 2.6)])
        leaves += [box(x, x + 20, dy0 - 3, dy0, hz + 5, 30), cyl(6, (x, hy, hz), "x", 20).cut(kslot)]
    add("Door hinge leaves + knuckles (304 SS, slotted pin holes: floating hinge)", comp(leaves), C["ss"], 8, (0, -240, 0), group="door", mat="ss304", bom="G1", mcm="1151A87", section=True)
    blocks = []
    for x in hx:                                           # outer knuckles bolted to the chamber's front face
        for xa, xb in ((x - 12.0, x - 0.5), (x + 20.5, x + 32.0)):
            blocks.append(fuse([box(xa, xb, hy, dy1, zf, hz), cyl(6, (xa, hy, hz), "x", xb - xa)]).cut(cyl(2.6, (xa - 1, hy, hz), "x", xb - xa + 2)))
    add("Door hinge knuckles on the chamber (304 SS)", comp(blocks), C["ss"], 8, (0, -240, 0), mat="ss304", bom="G1", mcm="1151A87", section=True)
    add("Hinge pins (Ø5, 316)", comp([cyl(2.5, (x - 12.0, hy, hz), "x", 44) for x in hx]), C["steel"], 8, (0, -240, 0), mat="ss316l", bom="G1", section=True)
    # draw latches (McMaster 1807A61, 800 lb, adjustable grip) on the chamber's side faces at mid-height, pulling strikes on the door's ears straight
    # back (+y): set each to >= 0.4 kN of preload (seals.md). For the robot cell a pneumatic latch clamp takes the same face and strike.
    lb_ = LT["body_L"]
    lat = [box(cx, cx + LT["H"], dy1 + 1.0, dy1 + 1.0 + lb_, zl_c - LT["W"] / 2, zl_c + LT["W"] / 2) if sx > 0 else
           box(-cx - LT["H"], -cx, dy1 + 1.0, dy1 + 1.0 + lb_, zl_c - LT["W"] / 2, zl_c + LT["W"] / 2) for sx in (1, -1)]
    add(f"Draw latches on the chamber's side faces (2 x McMaster 1807A61, 304 SS, {LT['rating_N'] / 1000:.1f} kN rated, preload set >= 0.4 kN)", comp(lat), C["ss"], 8, (0, -240, 0),
        mat="ss304", mass_kg=2 * 0.25, bom="G1", mcm="1807A61", section=True)
    strike = [box(cx, cx + 3.0, dy0, dy1 - 1.0, zl_c - 14.0, zl_c + 14.0) if sx > 0 else box(-cx - 3.0, -cx, dy0, dy1 - 1.0, zl_c - 14.0, zl_c + 14.0) for sx in (1, -1)]
    add("Draw-latch strikes on the door's ears (1807A61 strike plates)", comp(strike), C["ss"], 8, (0, -240, 0), group="door", mat="ss304", mass_kg=2 * 0.03, bom="G1", mcm="1807A61", section=True)
    add("Door handle", comp([cyl(5, (-30, dy0, 95), "-y", 26), cyl(5, (30, dy0, 95), "-y", 26), cyl(6, (-36, dy0 - 26, 95), "x", 72)]), C["anod"], 8, (0, -260, 0), group="door", mat="al6061", bom="G1", section=True)

    # ===================== 9. Optics =====================
    zb0_, zb1_ = P["z_bridge0"], P["z_bridge1"]
    br = box(-360, 245, -190, 180, zb0_, zb1_)
    br = br.cut(cyl(P["lens_d"] / 2 + 3, (0, 0, zb0_ - 1), "z", 27))
    br = br.cut(box(xd - 28, xd + 28, -191, 60, zb0_ - 1, zb1_ + 1))       # slot: the reservoirs (up to 50 x 112 mm) slide out to the front
    br = br.cut(cyl(40, (112, -66, zb0_ - 1), "z", 27))                     # clearance for the layer camera
    add("Optics bridge (6061, 25 mm)", br, C["alu"], 9, (0, 0, 260), mat="al6061", bom="F5")
    pst = []
    for x in (-345.0, 180.0):
        for y in (-185.0, 115.0):
            t_ = box(x, x + 60, y, y + 60, zb1, zb0_).cut(box(x + 5, x + 55, y + 5, y + 55, zb1 + 10, zb0_ - 10))
            pst.append(t_)
    add("Optics bridge posts (60 x 60 x 5 square 6061 tube, 10 mm end caps TIG-welded in)", comp(pst), C["alu_dark"], 9, (0, 0, 200), mat="al6061", bom="F5")
    zl0 = P["z_lens0"]
    lens = fuse([cyl(P["lens_d"] / 2, (0, 0, zl0), "z", P["lens_len"]), cyl(30, (0, 0, zl0 - 1.5), "z", 1.5)])
    add("f-theta lens, f = 160 mm (FTH160-1064 envelope)", lens, C["black"], 9, (0, 0, 300), mat="misc", mass_kg=0.6, bom="L6")
    g = P["galvo"] / 2
    galvo = fuse([rbox(-g, g, -g, g, zb1_, zb1_ + P["galvo_h"], 8), cyl(17, (-g - 15, 0, P["beam_z"]), "x", 15)])
    add("2-axis galvo scan head (basiCube class)", galvo, C["anod"], 9, (0, 0, 340), mat="misc", mass_kg=2.5, bom="L5")
    btube = tube(14, 11, (-140, 0, P["beam_z"]), "x", 140 - g - 15)
    add("Enclosed beam tube", btube, C["anod"], 9, (0, 0, 340), mat="al6061", bom="L4")
    sh = fuse([rbox(-200, -140, -32, 32, P["beam_z"] - 26, P["beam_z"] + 26, 4), box(-190, -150, -20, 20, zb1_, P["beam_z"] - 26)])
    add("Safety shutter + beam dump", sh, C["yellow"], 9, (0, 0, 340), mat="misc", mass_kg=1.2, bom="L4")
    coll = fuse([cyl(16, (-320, 0, P["beam_z"]), "x", 110), cyl(12, (-340, 0, P["beam_z"]), "x", 20),
                 box(-300, -230, -20, 20, zb1_, P["beam_z"] - 16)])
    add("Collimator (QBH, f = 30 mm, D ~ 3.2 mm) on V-mount", coll, C["ss"], 9, (0, 0, 340), mat="misc", mass_kg=0.5, bom="L3")
    fiber = polyline_pipe([(-340, 0, P["beam_z"]), (-380, 0, P["beam_z"]), (-420, -40, 230), (-430, -150, 150), (-460, -220, 60), (-560, -260, 0), (-600, -280, -20)], 5)
    add("Process fiber (armoured, ≥ 100 mm bend radius)", fiber, C["fiber"], 9, (0, 0, 300), mat="misc", mass_kg=0.6, bom="L1", module="rack")

    # ===================== 10. Gas & vacuum module =====================
    g0 = zb1
    pump = fuse([rbox(560, 980, 40, 290, g0, g0 + 270, 10), cyl(16, (640, 165, g0 + 270), "z", 20), cyl(14, (980, 120, g0 + 60), "x", 25)])
    add("Dry scroll pump (≤ 0.3 mbar, 6 m3/h class)", pump, C["blue"], 10, (300, 0, 0), mat="misc", mass_kg=26.0, module="gas", bom="G2", mcm="PUMP")
    add("Pump inlet (KF-25)", place(kf_stub(25, 20), (640, 165, g0 + 290 + 20), (1, 0, 0), (0, 0, 1)), C["ss"], 10, (300, 0, 0), mat="ss304", module="gas", bom="G7", mcm="KF25_WELD")
    filt = fuse([cyl(55, (470, -40, g0 + 20), "z", 220), cyl(58, (470, -40, g0 + 240), "z", 14), cyl(58, (470, -40, g0 + 20), "z", 14),
                 box(440, 500, -70, -10, g0, g0 + 20)])
    add("Sealed cyclone + HEPA housing (316L, valves off for passivation)", filt, C["ss"], 10, (0, -300, 0), mat="ss316l", mass_kg=4.0, module="gas", bom="G5", mcm="FILTER")
    add("Filter inlet (KF-25)", place(kf_stub(25, 20), (470, -40, g0 + 254 + 20), (1, 0, 0), (0, 0, 1)), C["ss"], 10, (0, -300, 0), mat="ss304", module="gas", bom="G7")
    add("Filter outlet (KF-25)", place(kf_stub(25, 20), (470 + 55 + 20, -40, g0 + 60), (0, 1, 0), (1, 0, 0)), C["ss"], 10, (0, -300, 0), mat="ss304", module="gas", bom="G7")
    bl = fuse([rbox(600, 800, -240, -60, g0, g0 + 200, 12), cyl(40, (700, -150, g0 + 200), "z", 30)])
    add("Sealed side-channel blower (gas-tight, ~100 L/min)", bl, C["blue"], 10, (0, -300, 0), mat="misc", mass_kg=9.0, module="gas", bom="G4", mcm="BLOWER")
    add("Blower inlet (KF-25)", place(kf_stub(25, 20), (600 - 20, -150, g0 + 60), (0, 1, 0), (-1, 0, 0)), C["ss"], 10, (0, -300, 0), mat="ss304", module="gas", bom="G7")
    add("Blower outlet (KF-25)", place(kf_stub(25, 20), (700, -150, g0 + 230 + 20), (1, 0, 0), (0, 0, 1)), C["ss"], 10, (0, -300, 0), mat="ss304", module="gas", bom="G7")
    o2 = rbox(830, 980, -240, -80, g0, g0 + 210, 6)
    add("Trace O2 analyzer + dew-point transmitter (panel box)", o2, C["white"], 10, (300, 0, 0), mat="misc", mass_kg=5.0, module="gas", bom="G6")
    man = comp([box(420, 535, 150, 280, g0, g0 + 22)] + [fuse([cyl(13, (x, 215, g0 + 22), "z", 45), box(x - 10, x + 10, 205, 225, g0 + 67, g0 + 82)]) for x in (445, 477, 509)])
    add("Argon solenoid manifold (purge / make-up / vent)", man, C["brass"], 10, (0, 300, 0), mat="brass", mass_kg=2.0, module="gas", bom="G7", mcm="8077K237")
    add("Argon pressure regulator + flowmeter", comp([cyl(22, (500, 120, g0), "z", 60), cyl(14, (500, 120, g0 + 60), "z", 40)]), C["brass"], 10, (0, 300, 0), mat="brass", mass_kg=1.2, module="gas", bom="G3")

    # ===================== 11. Hoses =====================
    vv = comp([place(kf_clamp(25), (cx + 18, 0, 70), (0, 1, 0), (1, 0, 0)), box(cx + 20, cx + 66, -22, 22, 48, 92),
               cyl(14, (cx + 43, 0, 92), "z", 26), place(kf_stub(25, 15), (cx + 43, 0, 48), (1, 0, 0), (0, 0, -1))])
    add("Vacuum isolation valve (KF-25 angle, pneumatic)", vv, C["ss"], 11, (220, 0, 0), mat="ss304", bom="G7", mcm="VALVE_KF25")
    hoses = {
        "Outlet plenum to filter": [(86, -90, zf - 45 - 26), (86, -90, -105), (110, -122, -115), (170, -132, -100), (300, -60, 20), (400, -40, 160), (470, -40, g0 + 294)],
        "Filter to blower": [(470 + 55 + 40, -40, g0 + 60), (560, -100, g0 + 60), (580 - 20, -150, g0 + 60)],
        "Blower to inlet plenum": [(700, -150, g0 + 270), (650, 20, 150), (420, 205, 100), (250, 205, 60), (110, cy + 78, 30), (0, cy + 32 + 46, 11)],
        "Vacuum line to pump": [(cx + 43, 0, 33), (cx + 43, 0, -30), (300, 60, -40), (500, 165, 80), (640, 165, g0 + 330)],
    }
    add("Gas-loop + vacuum hoses (KF-25 SS bellows)", comp([polyline_pipe(h, 13) for h in hoses.values()]), C["hose"], 11, (0, 0, -160), mat="ss316l", mass_kg=3.0, bom="G7", mcm="HOSE_KF25")
    add("Argon line (1/4 in. 316L)", polyline_pipe([(477, 215, g0 + 82), (477, 215, 140), (300, 100, 130), (150, 100, 105), (100, 100, 100), (100, cy + 0.0, 100)], 3.2), C["argon"], 11, (0, 200, 0), mat="ss316l", bom="G7", mcm="TUBE_SS")
    add("O2 sample line (1/8 in. 316L)", polyline_pipe([(cx, -40, 18), (cx + 30, -40, 18), (300, -150, 75), (600, -205, 85), (790, -205, 85), (900, -160, 70), (900, -160, 50)], 2.0), C["ss"], 11, (0, -200, 0), mat="ss316l", bom="G6", mcm="TUBE_SS")

    # ===================== 12. Laser guard =====================
    gx0, gx1, gy0, gy1 = -370.0, 290.0, -265.0, 215.0
    gz0, gz1 = zb1, P["z_bridge1"] + P["galvo_h"] + 25.0
    fr = []
    for x in (gx0 + 10, gx1 - 10):
        for y in (gy0 + 10, gy1 - 10):
            fr.append(tslot20((x, y, gz0), "z", gz1 - gz0))
    for z in (gz0 + 10, gz1 - 10):
        for y in (gy0 + 10, gy1 - 10):
            fr.append(tslot20((gx0 + 20, y, z), "x", gx1 - gx0 - 40))
        for x in (gx0 + 10, gx1 - 10):
            fr.append(tslot20((x, gy0 + 20, z), "y", gy1 - gy0 - 40))
    add("Guard frame (20 mm T-slot)", comp(fr), C["tslot"], 12, (0, 0, 0), mat="al6061", module="process", bom="S9", mcm="TSLOT")
    pt = 1.5
    pn = [box(gx0 - pt, gx0, gy0, gy1, gz0, gz1), box(gx1, gx1 + pt, gy0, gy1, gz0, gz1), box(gx0, gx1, gy1, gy1 + pt, gz0, gz1),
          box(gx0 - pt, gx1 + pt, gy0, gy1 + pt, gz1, gz1 + pt), box(gx0, -320.0, gy0 - pt, gy0, gz0, gz1), box(180.0, gx1, gy0 - pt, gy0, gz0, gz1)]
    add("Laser guard panels (1.5 mm aluminium)", comp(pn), C["panel"], 12, (0, 0, 0), mat="al6061", opacity=0.22, bom="S9", mcm="SHEET", section=True)
    gd = box(-330.0, 190.0, gy0 - pt - 6, gy0 - pt - 2, gz0 + 10, gz1 - 10)
    gd = gd.cut(box(-300.0, 160.0, gy0 - 10, gy0, gz0 + 40, gz1 - 40))
    add("Sliding guard door (aluminium)", gd, C["panel"], 12, (0, -260, 0), group="gdoor", mat="al6061", opacity=0.35, bom="S9", mcm="SHEET", section=True)
    add("OD 7+ viewing window (1070 nm, polycarbonate)", box(-300.0, 160.0, gy0 - pt - 5, gy0 - pt - 3, gz0 + 40, gz1 - 40), C["laser_glass"], 12, (0, -260, 0), group="gdoor", mat="pc", opacity=0.45, bom="S5", section=True)
    add("Guard door rail (top + bottom)", comp([box(-340.0, 680.0, gy0 - pt - 12, gy0 - pt - 7, gz1 - 8, gz1), box(-340.0, 680.0, gy0 - pt - 12, gy0 - pt - 7, gz0, gz0 + 8)]), C["steel"], 12, (0, -260, 0), mat="steel", bom="S9", section=True)
    add("Guard-locking door switch (Omron D4JL)", box(181.0, 200.0, gy0 - pt - 30, gy0 - pt - 13, gz1 - 120, gz1 - 30), C["yellow"], 12, (0, -280, 0), mat="misc", mass_kg=0.4, bom="S2", section=True)
    oy = bases["rack"][2]                                  # rack front plane; the panel hangs on the right-hand post
    pnl = rbox(-470.0, -420.0, oy - 32, oy, Z_TRAY + 140, Z_TRAY + 440, 4)
    add("Operator panel box (on the rack's front post)", pnl, C["anod"], 12, (0, -200, 0), mat="al6061", bom="S4", module="rack")
    bxp, gyp = -445.0, oy - 32
    ops = [("E-stop", comp([cyl(20, (bxp, gyp, Z_TRAY + 400), "-y", 8), cyl(17, (bxp, gyp - 8, Z_TRAY + 400), "-y", 14)]), C["red"], "S3"),
           ("Key switch", comp([cyl(13, (bxp, gyp, Z_TRAY + 345), "-y", 6), box(bxp - 4, bxp + 4, gyp - 14, gyp - 6, Z_TRAY + 342, Z_TRAY + 348)]), C["ss"], "S4"),
           ("Emission indicator", cyl(11, (bxp, gyp, Z_TRAY + 295), "-y", 10), C["red"], "S4"),
           ("Reset button", cyl(11, (bxp, gyp, Z_TRAY + 250), "-y", 10), C["blue"], "S4")]
    for nm, shp, col, b in ops:
        add(nm, shp, col, 12, (0, -220, 0), mat="misc", mass_kg=0.1, bom=b, module="rack")

    # ===================== 13. Dock and umbilicals =====================
    if include_tray:
        dx0, dy0_ = TRAY["inner"][0] / 2 - 110, TRAY["inner"][1] / 2 - 90
        dock = fuse([box(dx0, dx0 + 100, dy0_, dy0_ + 80, Z_TRAY, Z_TRAY + 140), box(dx0 + 100, dx0 + 108, dy0_ + 5, dy0_ + 75, Z_TRAY + 20, Z_TRAY + 130)])
        add("Tray dock (CombiTac-type, mates sideways)", dock, C["yellow"], 13, (200, 0, 0), mat="misc", mass_kg=6.0, module="tray", bom="D1")
        duct = box(-980.0, dx0, 320.0, 380.0, Z_TRAY, Z_TRAY + 50)
        add("Umbilical duct along the back edge", duct, C["anod"], 13, (0, 200, 0), mat="al6061", mass_kg=4.0, module="tray", bom="D1", opacity=0.6)
        cw = [polyline_pipe([(dx0, 350, Z_TRAY + 70), (900, 350, Z_TRAY + 70), (-700, 350, Z_TRAY + 70), (-760, 300, Z_TRAY + 140)], 7),
              polyline_pipe([(dx0, 335, Z_TRAY + 95), (900, 335, Z_TRAY + 95), (-660, 335, Z_TRAY + 95), (-720, 300, Z_TRAY + 160)], 7)]
        add("Chilled-water supply + return to the laser", comp(cw), C["water"], 13, (0, 200, 0), mat="misc", mass_kg=1.5, module="tray", bom="D1")
        add("Argon supply from the dock", polyline_pipe([(dx0, 365, Z_TRAY + 115), (700, 360, Z_TRAY + 115), (548, 300, Z_TRAY + 115), (548, 120, g0 + 30), (522, 120, g0 + 30)], 4), C["argon"], 13, (0, 200, 0), mat="ss316l", module="tray", bom="D1")
        add("Pump exhaust to the dock", polyline_pipe([(1005, 120, g0 + 60), (1060, 200, Z_TRAY + 60), (dx0, 395, Z_TRAY + 60)], 10), C["hose"], 13, (0, 200, 0), mat="misc", mass_kg=0.5, module="tray", bom="D1")

    # ===================== Fasteners: real McMaster-Carr parts, their holes cut into the parts they join =====================
    if fasteners:
        import joints as J
        J.add_joints(sys.modules[__name__], parts, add, module)
    return parts


# --------------------------------------------------------------------------------------------
# Motion: poses of each moving group
# --------------------------------------------------------------------------------------------
def path_point(path, s):
    """Point at arc length s along a polyline path."""
    for a, b in zip(path[:-1], path[1:]):
        d = math.dist(a, b)
        if s <= d or b == path[-1]:
            t = 0.0 if d == 0 else min(max(s / d, 0.0), 1.0)
            return tuple(a[k] + t * (b[k] - a[k]) for k in range(3))
        s -= d
    return path[-1]


def group_location(group, value):
    """cq.Location for a motion group at `value` (mm or degrees)."""
    m = MOTION[group]
    if m["kind"] == "path":
        return cq.Location(V(*path_point(m["path"], value)))
    if m["kind"] == "tx":
        return cq.Location(V(value, 0, 0))
    if m["kind"] == "ty":
        return cq.Location(V(0, value, 0))
    if m["kind"] == "tz":
        return cq.Location(V(0, 0, value))
    if m["kind"] == "rx":
        hy, hz = DOOR_HINGE
        # door drops toward -y: positive angle rotates the top edge forward (about +X by -angle)
        t1 = cq.Location(V(0, hy, hz))
        r = cq.Location(V(0, 0, 0), V(1, 0, 0), value)
        t0 = cq.Location(V(0, -hy, -hz))
        return t1 * r * t0
    raise ValueError(group)


def part_location(p, state):
    """cq.Location of part p in `state` = {group: value}, or None if it doesn't move.
    The Z stage follows the piston (its own value is an offset, used to drop the arm away from the rod end);
    parts tagged 'in_module' (plate, heater stack, rod) also ride along when the 'module' group moves."""
    loc = None
    g = p.group
    if g == "zstage":
        v = state.get("zstage", 0.0) + state.get("piston", 0.0)
        if v != 0.0:
            loc = cq.Location(V(0, 0, v))
    elif g and state.get(g, 0.0) != 0.0:
        loc = group_location(g, state[g])
    if "in_module" in p.tags and state.get("module", 0.0) != 0.0:
        mloc = group_location("module", state["module"])
        loc = mloc if loc is None else mloc * loc
    return loc


def moves_with(p, group):
    """True if part p moves when `group` moves (for sweeps)."""
    return p.group == group or (group == "piston" and p.group == "zstage") or (group == "module" and "in_module" in p.tags)


def posed(parts, state):
    """Shapes moved to `state` = {group: value}; missing groups stay at 0 (recoater parked, piston up, doors shut)."""
    out = []
    for p in parts:
        loc = part_location(p, state)
        out.append(p.shape if loc is None else p.shape.moved(loc))
    return out


def to_assembly(parts):
    a = cq.Assembly(name="desktop_lpbf_low")
    for i, p in enumerate(parts):
        r, g, b = (int(p.color[k:k + 2], 16) / 255 for k in (1, 3, 5))
        nm = "".join(ch if ch.isalnum() else "_" for ch in p.name)[:60] + f"_{i:03d}"
        a.add(p.shape, name=nm, color=cq.Color(r, g, b, p.opacity))
    return a


def envelope(parts, skip_context=True):
    bb = None
    for p in parts:
        if skip_context and "context" in p.tags:
            continue
        b = p.shape.BoundingBox()
        bb = b if bb is None else bb.add(b)
    return bb


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    parts = build()
    print(f"{len(parts)} parts built in {time.time() - t0:.1f} s")
    bb = envelope(parts)
    print(f"machine envelope: x {bb.xmin:.0f}..{bb.xmax:.0f} ({bb.xlen:.0f}), y {bb.ymin:.0f}..{bb.ymax:.0f} ({bb.ylen:.0f}), "
          f"z {bb.zmin:.0f}..{bb.zmax:.0f}; height above tray {bb.zmax - Z_TRAY:.1f} mm")
    if "--no-export" not in sys.argv:
        out = HERE / "out"
        out.mkdir(exist_ok=True)
        a = to_assembly(parts)
        a.export(str(out / "desktop-lpbf-low.step"))
        a.export(str(out / "desktop-lpbf-low.glb"))
        print("wrote", *(p.name for p in out.iterdir()))
