"""CAM for the process-chamber frame and the chamber floor plate in FreeCAD 1.0's CAM workbench, headless.

What it does
    Builds one FreeCAD CAM Job per setup (frame B, A, C0, C90, C180, C270; floor A, B), with the stock, tool controllers
    and operations listed in SETUPS below, recomputes them (FreeCAD's own MillFace, Adaptive,
    Profile, PocketShape, Helix and Drilling ops generate the toolpaths), posts each Job to G-code
    with FreeCAD's `linuxcnc` post, and writes per-operation numbers to
    desktop-lpbf/analysis/out/machining/freecad_cam.json:
      * FreeCAD's own cycle-time estimate (op.CycleTime and Job.CycleTime, whole seconds), and
      * a recount from the posted G-code: feed and rapid path length, cutting time = length / F,
        rapid time at the Haas VF-4's 25.4 m/min, canned drill cycles (G81/G83) expanded into
        their moves (pecks retract to R and come back at rapid). Tool changes are counted, not timed.

Inputs (/tmp/chamber-cam, or $CHAMBER_CAM_IN): frame.brep, floor.brep (mm, origin at the chamber's
interior floor centre, +z up), and parts.json. Make them with inventory.py: copy its process_chamber_body_*.brep to
frame.brep, chamber_floor_plate_*.brep to floor.brep, the two .stl files likewise (camotics_sim.py and holder_check.py read
them), and parts.json as it is (its joint cuts name the insert or pin each hole is for; without it, holes fall back to the
older drill rule). Blanks are boxes: frame 317.5 x 228.6 x 127 (z -5.45..121.55, the 274 x 184 core already removed by
waterjet before milling); floor 317.5 x 228.6 x 25.4 (z -22.7..2.7).
Setup B is the part turned 180 deg about the model x axis (bottom up). Frame setup C (since 2026-11-25) is the four walls on
an HRT210 rotary, A along machine X and the frame's z: one job per A index (frame_C0 front, C90 left, C180 back, C270
right), each in the machine frame at that index with work zero on the A axis (ROT_A), joined into one Haas program with
the A moves, gcode/frame_C_haas.nc (haas_rotary_program: Z to machine home, M11, G00 A, M10 before each index).

Run (FreeCAD 1.0.2, the official conda AppImage FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage from the GitHub
release, sha256 e00be00a...904f61 checked against the release's SHA256 file, extracted with --appimage-extract under /tmp):
    FREECADCMD=/path/to/squashfs-root/usr/bin/freecadcmd python3 desktop-lpbf/analysis/machining/freecad_cam.py
  or directly:
    /path/to/freecadcmd -c "import runpy; runpy.run_path('desktop-lpbf/analysis/machining/freecad_cam.py', run_name='__main__')"
G-code goes to /tmp/chamber-cam/gcode/<setup>.ngc.

Approximations (also written to the JSON): FreeCAD 1.0's Adaptive only knows the stock's bounding
box, so the inside of the frame opening is cut with Profile passes (rough 2.7 mm + finish 0.3 mm
radial) rather than Adaptive. Drills: one drill per hole step, the largest of 3.3/4.2/5.0/6.0 mm that
fits; taps, reamers and insert tools are not costed. No lead-in/lead-out dressups.

Checked in CAMotics (camotics_sim.py, 2026-11-22), which led to these fixes: face ops cover their face's
bounding box plus the tool radius, zig-zag along x (with the stock as the boundary and FreeCAD's default
45 deg, corners and patches up to 20 mm in from every edge stayed unfaced, and on the floor plate the
2.2 mm web outside the outline was never faced, so the notch tool ran through it); floor holes are drilled
from the side they open on, nearest step first (two top-side dowel holes were drilled up through the
bottom, and inner steps were drilled before the step above them was open, so the drill rapided into
solid stock); steps whose far end opens at full diameter get ExtraOffset = Drill Tip so the 118 deg point
does not leave a cone in the exit; the floor's port trepan and slots go through the blank in setup A, so
their slugs drop there.

Checked with holder_check.py (2026-11-23: holders, spindle, fixtures, travels), which led to these changes: T2 66 mm
out of an ER32 collet chuck (was 63 mm from a side-lock: its nose had 1.0 mm over the top face at the meet line); the
opening's finish in two passes (A5 has 38.1 mm of flutes); T9 28 mm out (its ER16 nut had 1.8 mm over the floor);
frame setup C's clearance and safe heights at 130 (the dummy-floor plate stands 9 mm proud of the front face); frame B
now runs first, as setup_plan.json's F-S1; floor A cuts the outline only to z -12 and floor B (stock: the whole blank)
cuts the rest of it with the U-notches. FIXTURES below holds each setup's workholding for that check: frame F-S1 and
floor P-S1 on low-profile edge clamps under the deepest cut (toe clamps on end tabs were in the face mill's and T2's
way), floor P-S2 held by a port ID clamp (the centre stud's washer sat on the face P-S2 faces).

2026-11-25: setup C programmed beyond the door opening (wall_ops: the bores and ports helix-milled, the holes drilled with
their tap or STI drill); the drills for insert and dowel holes chosen by part number (PN_DRILL: the lid's M5 STI holes had
a 6.0 mm drill, the insert's major diameter, and the dowel holes 6.0 mm with nothing left to ream); the dummy-floor plate
made flush with the frame (312 x 222; at 330 x 240 it stood 9 mm proud of every wall on the rotary). Checked with
camotics_sim.py (per A index: CAMotics 1.2.0 ignores A) and holder_check.py.
"""
import json
import math
import os
import re
import subprocess
import sys

IN_DIR = os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam")
GCODE_DIR = os.path.join(IN_DIR, "gcode")
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:  # exec'd without a file name
    HERE = os.getcwd()
OUT_JSON = os.environ.get("FREECAD_CAM_JSON") or os.path.normpath(os.path.join(HERE, "..", "out", "machining", "freecad_cam.json"))

RAPID_MM_MIN = 25400.0  # Haas VF-4 rapid, X/Y/Z (1000 in/min)
IN = 25.4

# --- tools (6061-T6, conservative vendor ranges) ------------------------------------------------------
# T5-T7 are the requested carbide drill set (5.0 / 3.3 / 4.2 mm); T8 (6.0 mm drill) and T9 (1/4 in. end
# mill, for the 8 mm slot and 8 mm U-notches that T3 does not fit) are additions.
#   feed (mm/min) = rpm * flutes * chip load (in/tooth) * 25.4 ; drills: rpm * mm/rev
TOOLS = {
    1: dict(name="2.5 in. (63.5 mm) indexable face mill, 4 inserts", shape="endmill", d=63.5, flutes=4,
            rpm=3000, ipt=0.004, length=60.0, edge=8.0),
    # T2 was 63 mm out of a side-lock holder: holder_check.py found its nose 1.0 mm over the top face at the
    # mid-height meet line (frame A z 58, B z -58). Now 66 mm out of an ER32 collet chuck (Haas 04-0010; A5's 4 in. OAL
    # leaves 35.6 mm in the 40 mm collet): 4.0 mm clear. Flute length 1-1/2 in. (A5), so walls go in 31 mm passes.
    2: dict(name="3/4 in. (19.05 mm) 3-flute carbide end mill, 66 mm stick-out, ER32 collet chuck", shape="endmill",
            d=19.05, flutes=3, rpm=5100, ipt=0.005, length=66.0, edge=38.1, holder="04-0010"),
    3: dict(name="1/2 in. (12.7 mm) 3-flute carbide end mill, 38 mm stick-out", shape="endmill", d=12.7,
            flutes=3, rpm=7600, ipt=0.003, length=38.0, edge=32.0),
    4: dict(name="1/8 in. (3.175 mm) 2-flute carbide end mill (O-ring grooves)", shape="endmill", d=3.175,
            flutes=2, rpm=8100, ipt=0.0008, length=12.0, edge=9.5),
    5: dict(name="5.0 mm carbide drill", shape="drill", d=5.0, rpm=5000, mm_rev=0.1, length=40.0),
    6: dict(name="3.3 mm carbide drill (M4 tap drill)", shape="drill", d=3.3, rpm=5000, mm_rev=0.1, length=30.0),
    7: dict(name="4.2 mm carbide drill", shape="drill", d=4.2, rpm=5000, mm_rev=0.1, length=30.0),
    8: dict(name="6.0 mm carbide drill (added: insert counterbores, dowels)", shape="drill", d=6.0, rpm=5000,
            mm_rev=0.1, length=40.0),
    # T9 was 25 mm out: holder_check.py found the ER16 nut 1.8 mm over the floor's top face at the slots' z -23.2. 28 mm
    # out (A2's 2-1/2 in. OAL leaves 35.5 mm in the collet): 4.8 mm clear.
    9: dict(name="1/4 in. (6.35 mm) 3-flute carbide end mill (added: 8 mm slot, U-notches)", shape="endmill",
            d=6.35, flutes=3, rpm=8100, ipt=0.0015, length=28.0, edge=19.0),
    # added for setup C (2026-11-25): the tap drill for the through-beam's M6 x 0.75, a drill for the 3 mm dowel-pin
    # holes (ream 3 mm H7 after, tooling-bom F2; the reamer is not programmed), and the M5 STI drill (tooling-bom D10)
    10: dict(name="5.2 mm carbide drill (added: M6 x 0.75 tap drill)", shape="drill", d=5.2, rpm=5000,
             mm_rev=0.1, length=35.0),
    11: dict(name="2.9 mm carbide drill (added: 3 mm dowel-pin holes, reamed after)", shape="drill", d=2.9, rpm=5000,
             mm_rev=0.08, length=25.0),
    12: dict(name="5.3 mm carbide drill (added: M5 STI drill, tooling-bom D10)", shape="drill", d=5.3, rpm=5000,
             mm_rev=0.1, length=35.0),
    # 2026-11-25: the floor's M6 STI holes and the 6 mm dowel holes (reamed after, tooling-bom F1)
    13: dict(name="6.3 mm carbide drill (added: M6 STI drill, tooling-bom D11)", shape="drill", d=6.3, rpm=5000,
             mm_rev=0.1, length=40.0),
    14: dict(name="5.8 mm carbide drill (added: 6 mm dowel holes, reamed after)", shape="drill", d=5.8, rpm=5000,
             mm_rev=0.1, length=40.0),
}
DRILLS = {6: 3.3, 7: 4.2, 5: 5.0, 8: 6.0}
# Setup C (the walls) drills each hole with its tap or STI drill, by the diameter the model draws at the hole's mouth:
# 3.0 dowel pin -> 2.9 (ream); 4.0 M4 tapped (or a plain 4 mm passage) -> 3.3; 4.908 M4 STI -> 4.2 (tooling-bom D9 is
# 4.22); 6.0 M6 x 0.75 -> 5.2; 6.038 M5 STI -> 5.3 (D10). Setups A and B keep the older rule, the largest of DRILLS
# that fits each step, which drills the lid's M5 STI holes 6.0 then 5.0 mm (the model's two steps): see machining.md.
TAP_DRILL = {3.0: 11, 4.0: 6, 4.908: 7, 5.0: 5, 6.0: 10, 6.038: 12}
SAE4_TAP_DRILL = 25.0 / 64 * 25.4   # 9.92 mm, for the SAE-4 ports' 7/16-20 UNF thread (the port tool finishes it)
# Holes for a helical insert or a dowel pin, found by the part number joints.py cut them for (inventory.py's parts.json,
# copied next to the .brep files): one drill, the insert's STI drill (tooling-bom D9-D11, per McMaster's insert pages) or
# the pin's ream-under drill, from the hole's mouth to its bottom. Until 2026-11-25 every step was drilled with the
# largest drill that fits it, and the model draws an STI hole at the insert's major diameter: the lid's M5 STI holes got
# a 6.0 mm drill (major 6.04: no thread left for the STI tap) and the 6 mm dowel holes a 6.0 mm drill (no reaming stock).
PN_DRILL = {"91732A656": 7, "91732A261": 12, "91732A262": 13, "91732A782": 13,   # M4, M5, M6, M6 STI inserts
            "93600A304": 11, "93600A686": 14}                                   # 3 mm and 6 mm dowel pins
# A screw joint's hole drawn at the thread's nominal size is tapped (joints.py draws tapped holes at nominal, clearance
# holes larger): its tap drill, coarse pitch (M4 3.3, M5 4.2, M6 5.0).
NOMINAL_TAP = {4.0: 6, 5.0: 7, 6.0: 5}

# --- setup C: the four walls on the HRT210 (A axis along machine X) -----------------------------------------------
# Machine frame at each index, work zero on the A axis: X = the frame's z (its bottom on the platter side), and the wall
# being cut faces +Z. Rotations model -> machine, as setup_plan.json's F-S3 a_axis.index (A turns the part about +X by
# the right-hand rule: A 90 brings the left wall up). Check the HRT210's direction parameter when setting up.
ROT_A = {0: ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),     # front (-y) up
         90: ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),     # left (-x) up
         180: ((0, 0, 1), (1, 0, 0), (0, 1, 0)),     # back (+y) up
         270: ((0, 0, 1), (0, -1, 0), (1, 0, 0))}    # right (+x) up
WALLS = {0: ("front", 1, -1, 111.0, 95.0), 90: ("left", 0, -1, 156.0, 140.0), 180: ("back", 1, 1, 111.0, 95.0),
         270: ("right", 0, 1, 156.0, 140.0)}         # name, model axis, outward sign, outer and inner face (setup Z)
FRAME_OUTLINE = (-156.0, 156.0, -111.0, 111.0, -3.9, 120.0)   # what A and B leave: the stock setup C starts from


def rot_matrix(su):
    """3 x 3 model -> setup rotation (rows: setup x, y, z in model coordinates)"""
    if "rot" in su:
        return tuple(tuple(r) for r in su["rot"])
    a = su.get("rot_x", 180 if su.get("flip") else 0)
    return {0: ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 180: ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
            -90: ((1, 0, 0), (0, 0, 1), (0, -1, 0))}[a]


def _box_in(rot, box):
    x0, x1, y0, y1, z0, z1 = box
    pts = [[sum(rot[i][k] * c[k] for k in range(3)) for i in range(3)]
           for c in [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return lo, hi


def _stock_box(rot, box=FRAME_OUTLINE):
    lo, hi = _box_in(rot, box)
    return (lo[0], lo[1], lo[2], hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])


def clean_label(s):
    """op label without parentheses: the post writes labels into G-code comments, and a nested "(" or ")" ends the
    comment early (LinuxCNC rejects it; CAMotics logged parse errors and dropped floor B's last two drill ops)"""
    return re.sub(r"\s*\(([^()]*)\)", r", \1", s).replace("(", "").replace(")", "")


def feed_mm_min(t, ipt=None):
    if TOOLS[t]["shape"] == "drill":
        return TOOLS[t]["rpm"] * TOOLS[t]["mm_rev"]
    return TOOLS[t]["rpm"] * TOOLS[t]["flutes"] * (ipt or TOOLS[t]["ipt"]) * IN


# --- the setups -----------------------------------------------------------------------------------
# op = (label, kind, tool, chip-load override or None, settings). Faces are found by geometry (see
# pick_faces) so the face numbers are not hard-coded.
FRAME_BLANK = (317.5, 228.6, -5.45, 121.55)
FLOOR_BLANK = (317.5, 228.6, -22.7, 2.7)
SETUPS = [
    # frame B (bottom up) runs first, as setup_plan.json's F-S1: the blank is held by toe clamps on its end tabs;
    # frame A (top up, F-S2) then sits on the dummy-floor plate, pulled down through the 18 holes B drilled
    dict(name="frame_B", part="frame", flip=True, stock=FRAME_BLANK, ops=[
        ("Face bottom to z -3.9", "face", 1, None, dict(face="top", start=5.45, final=3.9, step=1.55)),
        ("Outside 312x222 R8, adaptive, bottom up to mid-height", "adaptive_out", 2, None,
         dict(face="top", start=3.9, final=-58.0, step=31.0, stepover=10)),
        ("Rebate 8 x 3.9 round the bottom of the opening", "profile_perimeter", 3, None,
         dict(face="rebate", start=3.9, final=0.0, step=3.9)),
        ("Opening from bottom, rough (2.7 mm radial)", "profile_holes", 2, None,
         dict(face="rebate", start=0.0, final=-58.0, step=29.0, extra=0.3)),
        ("Opening from bottom, finish (0.3 mm radial, two 29 mm passes)", "profile_holes", 2, None,
         dict(face="rebate", start=0.0, final=-58.0, step=29.0, extra=0.0)),
        ("Drill 18 M4 tap holes 3.3 mm", "drill", 6, None, dict(holes="bottom_r2.0")),
        ("Drill 2 dowel holes 5.8 mm, ream 6 H7 after", "drill", 14, None, dict(holes="bottom_r3.0")),
    ]),
    dict(name="frame_A", part="frame", flip=False, stock=FRAME_BLANK, ops=[
        ("Face top to z 120", "face", 1, None, dict(face="top", start=121.55, final=120.0, step=1.55)),
        ("Outside 312x222 R8, adaptive, z 120 to 58", "adaptive_out", 2, None,
         dict(face="top", start=120.0, final=58.0, step=31.0, stepover=10)),
        ("Opening 280x190 R10 from top, rough (2.7 mm radial)", "profile_holes", 2, None,
         dict(face="top_inner", start=120.0, final=58.0, step=31.0, extra=0.3)),
        # finish in two 31 mm passes: in one 62 mm pass the shank above A5's 38.1 mm of flutes rubbed the 0.3 mm skin
        ("Opening 280x190 R10 from top, finish (0.3 mm radial, two 31 mm passes)", "profile_holes", 2, None,
         dict(face="top_inner", start=120.0, final=58.0, step=31.0, extra=0.0)),
        ("Lid O-ring gland 4.6 x 2.65", "pocket", 4, None, dict(face="gland", start=120.0, step=0.5)),
        # the M5 STI drill to the bottom of both modelled steps (was 6.0 then 5.0 mm, the steps' own sizes)
        ("Drill 20 M5 STI insert holes 5.3 mm, 10.5 deep", "drill", 12, None, dict(holes="top_r2.5", start=120.0)),
    ]),
    # setup C (F-S3): the four walls in one clamping on the HRT210, one FreeCAD job per A index, each in the machine
    # frame at that index (ROT_A); stock = the finished outline. Posted per index, then joined into one Haas program
    # with the A moves (haas_rotary_program). clear_z: the dummy-floor plate stands 9 mm proud of each wall (Z 120 at
    # front and back, 165 at the sides); FreeCAD's default clearance (stock top + 5) brought the tool down into it on
    # the first move (holder_check.py, 2026-11-23). "wall" expands into the wall's bores, ports and holes, found on the
    # model (wall_ops in run_cam). Programmed 2026-11-25; until then setup C cut only the door opening.
    dict(name="frame_C0", part="frame", rot=ROT_A[0], a_deg=0, rotary="frame_C", stock_box=_stock_box(ROT_A[0]),
         clear_z=130.0, ops=[
        ("Door opening 220x92 R6.5 through the 16 mm front wall, adaptive", "adaptive_in", 3, None,
         dict(edges="door", start=111.0, final=94.5, step=16.5, stepover=10)),
    ]),
    dict(name="frame_C90", part="frame", rot=ROT_A[90], a_deg=90, rotary="frame_C", stock_box=_stock_box(ROT_A[90]),
         clear_z=175.0, ops=[("Left wall: recoater bore, through-beam", "wall", None, None, dict(wall=90))]),
    dict(name="frame_C180", part="frame", rot=ROT_A[180], a_deg=180, rotary="frame_C",
         stock_box=_stock_box(ROT_A[180]), clear_z=130.0, ops=[
        ("Inlet slot 120x8 through the back wall, profile", "profile_holes", 9, None,
         dict(face="wall_back", start=111.0, final=94.5, step=3.0, extra=0.0)),
        ("Back wall: argon port, plenum inserts and pins, rail holes", "wall", None, None, dict(wall=180)),
    ]),
    dict(name="frame_C270", part="frame", rot=ROT_A[270], a_deg=270, rotary="frame_C",
         stock_box=_stock_box(ROT_A[270]), clear_z=175.0,
         ops=[("Right wall: KF-25 and recoater bores, through-beam, O2 port, inserts, pins", "wall", None, None,
               dict(wall=270))]),
    dict(name="floor_A", part="floor", flip=False, stock=FLOOR_BLANK, ops=[
        ("Face top to z 0", "face", 1, None, dict(face="top", start=2.7, final=0.0, step=2.7)),
        ("Step the 4 mm band round the pad (adaptive outside the pad)", "adaptive_out", 2, None,
         dict(face="top", start=0.0, final=-4.0, step=4.0, stepover=10)),
        # only to z -12 (holder_check.py): the blank is held by low edge clamps under z -15, and setup B, held by the
        # port and the pins, cuts the rest of the outline with the U-notches. To z -20.5 it needed toe clamps on end tabs,
        # whose roots the outside passes ran through (the CAM blank has no tabs)
        ("Outside 312x222 R8, adaptive, z -4 to -12", "adaptive_out", 2, None,
         dict(face="band", start=-4.0, final=-12.0, step=8.0, stepover=10)),
        ("Floor O-ring groove 4.6 x 2.65", "pocket", 4, None, dict(face="gland", start=0.0, step=0.5)),
        # port and slots go 0.5 mm past the blank's bottom (z -22.7), so their slugs drop in this setup: at z -20.5
        # a 2.2 mm web held them until setup B, whose fixture needs the port open for its centre stud
        ("Port 96 mm through: helical trepan (slug drops)", "helix", 2, 0.002,
         dict(face="port", start=0.0, final=-23.2, step=1.5)),
        ("Slots 124x8 and 20x104 through, profile", "profile_holes", 9, None,
         dict(face="top_inner", start=0.0, final=-23.2, step=3.0, extra=0.0)),
        # added after the CAMotics check: the blind holes that open on the top side were drilled from below in B
        ("Drill the blind holes that open on top", "drill_top", None, None, dict()),
    ]),
    # floor B: the stock is the 312 x 222 outline box (A cut the outside down to z -20.5), so the notch Adaptive only
    # cuts the notches. The 2.2 mm web left under z -20.5 is faced off by the face op, which now covers its face's
    # bounding box plus the tool radius whatever the stock (with the stock as the boundary it missed the web, and
    # the notch op's tool ran through it).
    # (since holder_check.py: A cuts the outline only to z -12, so B's stock is the whole blank and its outside op
    # cuts the rest of the outline, the ring round it and the U-notches together, with the plate held by the port)
    dict(name="floor_B", part="floor", flip=True, stock=FLOOR_BLANK, ops=[
        ("Face bottom to 20 mm thick", "face", 1, None, dict(face="top", start=22.7, final=20.0, step=2.7)),
        ("Outside below z -12 and the 18 U-notches 8 wide x 8 deep (adaptive outside the outline)", "adaptive_out", 9,
         None, dict(face="top", start=20.0, final=12.0, step=4.0, stepover=15)),
        ("Drill the holes that open on the bottom", "drill_all", None, None, dict()),
    ]),
]


# --- workholding, for holder_check.py (plain Python) -----------------------------------------------------------
# Each setup's fixtures in its own setup frame (mm, z up, the frame freecad_cam programs in), from setup_plan.json's
# fixture notes: (table z, [(name, kind, params)], end tabs). Kinds: box (x0, x1, y0, y1, z0, z1); vcyl (cx, cy, r, z0,
# z1); ycyl, a cylinder along y (cx, cz, r, y0, y1). End tabs (x0, x1, y0, y1, z0, z1) are blank the CAM stock box does
# not have: holder_check.py treats them as stock (the cutter may cut them; nothing else may touch them).
# setup_plan.json: "1 in. at each x end for F-S1's toe clamps", noses 3 mm out along the tab. holder_check.py found the
# face mill (it faces the bounding box plus its radius, to x +-187.9) running into such clamps, and the 3/4 in. end
# mill's outside passes (to x +-175.7) running through the tab roots, which the CAM blank does not have. Neither the
# frame nor the floor plate uses tabs now; toe_clamps() and end_tabs() stay for re-checking that layout.
TAB_LEN = 1.0 * IN
CLAMP_IN = 3.0


def toe_clamps(x_root, top, ys=(-60.0, 60.0)):
    """four strap clamps (1 in. wide x 5/8 in. strap, 5/8-11 stud, 1-1/16 in. flange nut 5/8 in. tall, stud 5 mm proud)
    on end tabs whose root is at |x| = x_root, nose CLAMP_IN out along the tab, heel 100 mm further out"""
    out = []
    for sx in (-1, 1):
        for y in ys:
            xn = x_root + CLAMP_IN
            x0, x1 = (xn, xn + 100.0) if sx > 0 else (-xn - 100.0, -xn)
            out.append(("toe clamp strap", "box", (x0, x1, y - 12.7, y + 12.7, top, top + 15.9)))
            xs = sx * (xn + 30.0)
            out.append(("toe clamp nut and stud", "vcyl", (xs, y, 15.6, top, top + 15.9 + 15.9 + 5.0)))
    return out


def end_tabs(x_root, z0, z1, length):
    return [(-x_root - length, -x_root, -FRAME_BLANK[1] / 2, FRAME_BLANK[1] / 2, z0, z1),
            (x_root, x_root + length, -FRAME_BLANK[1] / 2, FRAME_BLANK[1] / 2, z0, z1)]


def _fixtures():
    fb_top = -FRAME_BLANK[2]          # frame B (bottom up): the blank's bottom face, now on top
    fb_bot = -FRAME_BLANK[3]
    fl_top, fl_bot = FLOOR_BLANK[3], FLOOR_BLANK[2]
    x_root = FRAME_BLANK[0] / 2
    hrt_face = -3.9 - 25.4            # frame C: the platter face, behind the 1 in. dummy-floor plate
    return {
        # F-S1: blank on four 1-1/2 in. risers. setup_plan.json had toe clamps on 1 in. end tabs: holder_check.py found the
        # face mill (it faces the bounding box plus its radius, to x +-187.9) running into the clamps, and the 3/4 in. end
        # mill cutting into the tab roots (its outside passes reach x +-175.7) and its holder and flange passing over the
        # clamps. Now low-profile edge clamps (ASSUMED 40 x 40 mm bodies, on risers) push on the blank's x-end faces
        # below z -63, 5 mm under B's deepest cut (z -58): no tabs, nothing on top.
        "frame_B": (fb_bot - 1.5 * IN, [("riser block", "box", (sx * 150 - 25, sx * 150 + 25, sy * 100 - 25,
                                                                 sy * 100 + 25, fb_bot - 1.5 * IN, fb_bot))
                                         for sx in (-1, 1) for sy in (-1, 1)]
                    + [("edge clamp", "box", (sx * x_root if sx > 0 else -x_root - 40.0, x_root + 40.0 if sx > 0
                                              else -x_root, y - 20.0, y + 20.0, fb_bot - 1.5 * IN, -63.0))
                       for sx in (-1, 1) for y in (-60.0, 60.0)], []),
        # (setup_plan.json's toe clamps on end tabs, kept for the record: toe_clamps(x_root, fb_top), end_tabs(...))
        # F-S2: the dummy-floor plate (1 in. MIC-6) under the frame's skirt face; screws from below. 312 x 222, flush with
        # the frame (was 330 x 240: on the rotary it stood 9 mm proud of every wall, and T9's ER16 holder came within
        # 2.5 mm of it profiling the back wall's inlet slot, holder_check.py 2026-11-25)
        "frame_A": (-3.9 - 25.4, [("dummy-floor plate", "box", (-156, 156, -111, 111, -3.9 - 25.4, -3.9))], []),
        # F-S3, setup C: the dummy-floor plate (1 in. MIC-6, 312 x 222, flush with the frame) on an HRT210 platter, A along machine X and the
        # frame's z, A 215.9 above the table (2-1/2 in. riser), work zero on the A axis; one entry per index, in that
        # index's machine frame (ROT_A). The plate turns with the part; the platter is round about A; the housing,
        # motor box and riser stay put. HRT210 from Haas' layout drawing hrt210_10-2020.pdf (Rev 1, 2019-11-11):
        # platter dia. 210, centre height 152.4, housing 276.4 tall, 124.0 from the platter centre to its side (taken
        # as symmetric), 177.8 deep; motor box beside it to 466.9 overall (side ASSUMED -Y). Platter taken as 15.9 thick.
        **{"frame_C%d" % a: (-215.9, [
            ("dummy-floor plate", "box", tuple(v for lo_hi in zip(*_box_in(ROT_A[a], (-156, 156, -111, 111, hrt_face,
                                                                                         -3.9))) for v in lo_hi)),
            ("HRT210 platter", "xcyl", (0.0, 0.0, 105.0, hrt_face - 15.9, hrt_face)),
            ("HRT210 housing", "box", (hrt_face - 15.9 - 177.8, hrt_face - 15.9, -124.0, 124.0, -152.4, -152.4 + 276.4)),
            ("HRT210 motor box", "box", (hrt_face - 15.9 - 177.8, hrt_face - 15.9, -342.9, -124.0, -152.4,
                                         -152.4 + 276.4)),
            ("2-1/2 in. riser", "box", (hrt_face - 15.9 - 177.8, hrt_face - 15.9, -342.9, 124.0, -215.9, -152.4)),
        ], []) for a in ROT_A},
        # P-S1: blank on 1/2 x 1-1/2 in. parallels along x, clear of the port and slots; toe clamps on the end tabs
        # (since holder_check.py: no tabs; low-profile edge clamps, ASSUMED 40 x 40 mm, on the x-end faces under
        # z -15, 3 mm below A's outside passes, which now stop at z -12)
        "floor_A": (fl_bot - 1.5 * IN, [("parallel", "box", (-150, 150, y0, y0 + 12.7, fl_bot - 1.5 * IN, fl_bot))
                                        for y0 in (-110.7, 98.0)]
                    + [("edge clamp", "box", (x_root if sx > 0 else -x_root - 40.0, x_root + 40.0 if sx > 0 else -x_root,
                                              y - 20.0, y + 20.0, fl_bot - 1.5 * IN, -15.0))
                       for sx in (-1, 1) for y in (-60.0, 60.0)], []),
        # P-S2 (bottom up): fixture plate under the sealing face and 2 dowel pins. setup_plan.json's central M12 stud
        # with a dia. 104 clamp washer sat on the very face this setup faces: holder_check.py found the face mill and
        # the drills of the holes near the port running into it. Now the port is held from inside: an expanding ID
        # clamp (ASSUMED dia. 94, its top 5 mm under the faced bottom at z 20) pulls the plate onto the fixture plate.
        "floor_B": (-25.4, [("fixture plate", "box", (-156, 156, -111, 111, -25.4, 0.0)),  # the dummy-floor plate
                            ("port ID clamp", "vcyl", (0.0, 0.0, 47.0, 0.0, 15.0))], []),
        # (setup_plan.json's version, for the record: a dia. 104 x 3/8 in. washer and M12 nut on the bottom face)
    }


FIXTURES = _fixtures()


# --- FreeCAD side ---------------------------------------------------------------------------------
def run_cam():
    import FreeCAD
    import Part
    import Path
    import Path.Main.Job as PathJob
    import Path.Main.Stock as PathStock
    import Path.Op.Adaptive
    import Path.Op.Drilling
    import Path.Op.Helix
    import Path.Op.MillFace
    import Path.Op.PocketShape
    import Path.Op.Profile
    import Path.Tool.Bit as PathToolBit
    import Path.Tool.Controller as PathToolController
    from Path.Post.scripts import linuxcnc_post

    os.makedirs(GCODE_DIR, exist_ok=True)
    doc = FreeCAD.newDocument("chamber_cam")
    shapes = {}
    for part in ("frame", "floor"):
        s = Part.Shape()
        s.read(os.path.join(IN_DIR, part + ".brep"))
        shapes[part] = s

    def zface(shape, z, up=True, tol=0.01):
        out = []
        for i, f in enumerate(shape.Faces):
            if type(f.Surface).__name__ != "Plane":
                continue
            n = f.normalAt(0, 0)
            if abs(n.z - (1 if up else -1)) < 1e-6 and abs(f.BoundBox.ZMin - z) < tol:
                out.append(("Face%d" % (i + 1), f))
        return out

    def cyl_groups(shape):
        """vertical cylinders grouped per hole step: (x, y, r, zmin, zmax) -> [face names], full turns only"""
        g = {}
        for i, f in enumerate(shape.Faces):
            s = f.Surface
            if type(s).__name__ != "Cylinder" or abs(abs(s.Axis.z) - 1) > 1e-6:
                continue
            u0, u1, _, _ = f.ParameterRange
            key = (round(s.Center.x, 1), round(s.Center.y, 1), round(s.Radius, 3),
                   round(f.BoundBox.ZMin, 2), round(f.BoundBox.ZMax, 2))
            g.setdefault(key, [[], 0.0])
            g[key][0].append("Face%d" % (i + 1))
            g[key][1] += u1 - u0
        return {k: v[0] for k, v in g.items() if v[1] > 2 * math.pi - 1e-3}

    def pick_faces(part, flip, key):
        """face names (same numbering in both setups: setup B only rotates the shape)"""
        s = shapes[part]
        bb = s.BoundBox
        if key == "top":  # the face the tool sees first: model top (A) or model bottom (B)
            cands = zface(s, bb.ZMin, up=False) if flip else zface(s, bb.ZMax, up=True)
            return [max(cands, key=lambda c: c[1].BoundBox.DiagonalLength)[0]]
        if key == "top_inner":  # top face inside the O-ring loop: its inner wires are the through features
            cands = zface(s, bb.ZMax, up=True)
            return [min(cands, key=lambda c: c[1].BoundBox.DiagonalLength)[0]]
        if key == "gland":  # O-ring groove floor: 2.65 below the top, ring with two wires
            cands = [c for c in zface(s, bb.ZMax - 2.65, up=True) if len(c[1].Wires) == 2]
            return [max(cands, key=lambda c: c[1].Area)[0]]
        if key == "rebate":  # frame: rebate ceiling at z 0, facing down
            return [n for n, f in zface(s, 0.0, up=False) if len(f.Wires) == 2]
        if key == "band":  # floor: the 4 mm step band, its outer wire is the plate outline
            return [max(zface(s, -4.0, up=True), key=lambda c: c[1].Area)[0]]
        if key == "port":
            return [names[0] for k, names in cyl_groups(s).items() if abs(k[2] - 48.0) < 0.01]
        if key == "wall_back":  # the back wall's outer face (y = +111): its one non-circular inner wire is the slot
            return ["Face%d" % (i + 1) for i, f in enumerate(s.Faces) if type(f.Surface).__name__ == "Plane"
                    and f.normalAt(0, 0).y > 0.999 and abs(f.BoundBox.YMax - bb.YMax) < 0.01]
        raise KeyError(key)

    def wall_ops(part, a_deg):
        """setup C: the bores, ports and holes of the wall that faces up at index a_deg, from the model: cylinders whose
        axis is the wall's normal, inside the wall, grouped per hole. Steps over r 4.5 are helix-milled (r >= 8 with
        T3: the 18 and 25.4 mm bores; else T9: the through-beam's 10.8 counterbore, and the SAE-4 ports to their
        25/64 in. tap drill), the rest drilled with the tap or STI drill of the step at the hole's mouth (TAP_DRILL),
        from that step's top to the hole's bottom. Returns [(label, kind, tool, ipt, cfg, face names, meta)]."""
        s0 = shapes[part]
        wname, ax, sign, outer, inner = WALLS[a_deg]
        holes_ = {}
        for i, f in enumerate(s0.Faces):
            su_ = f.Surface
            if type(su_).__name__ != "Cylinder" or abs(abs(su_.Axis[ax]) - 1) > 1e-6:
                continue
            lo_, hi_ = (f.BoundBox.XMin, f.BoundBox.XMax) if ax == 0 else (f.BoundBox.YMin, f.BoundBox.YMax)
            zlo, zhi = sorted((sign * lo_, sign * hi_))
            if zlo < inner - 0.01 or zhi > outer + 0.01:
                continue
            u0, u1, _, _ = f.ParameterRange
            c = su_.Center
            loc = (round(c.y if ax == 0 else c.x, 2), round(c.z, 2))
            st = holes_.setdefault(loc, {}).setdefault((round(su_.Radius, 3), round(zlo, 2), round(zhi, 2)), [[], 0.0])
            st[0].append("Face%d" % (i + 1))
            st[1] += u1 - u0

        def air(u, v, z):  # (u, v): the hole's in-wall coordinates; z: setup Z along the normal
            q = [0.0, 0.0, v]
            q[ax] = sign * z
            q[1 - ax] = u
            return not s0.isInside(FreeCAD.Vector(*q), 1e-4, True)

        helix, drill = {}, {}
        for loc, steps in holes_.items():
            steps = sorted(((k, v[0]) for k, v in steps.items() if v[1] > 2 * math.pi - 1e-3), key=lambda kv: -kv[0][2])
            if not steps:
                continue
            bottom = min(k[1] for k, _ in steps)
            through = all(air(loc[0] + 0.5 * steps[-1][0][0] * math.cos(t), loc[1] + 0.5 * steps[-1][0][0] * math.sin(t),
                              bottom - 0.05) for t in (0.3, 1.9, 3.5, 5.1))
            for n, ((r, zlo, zhi), names) in enumerate(steps):
                if r > 4.5:
                    t = 3 if r >= 8.0 else 9
                    if abs(r - 5.555) < 0.01:      # SAE-4 port, 7/16-20: to the tap drill; the port tool does the rest
                        off, what = r - SAE4_TAP_DRILL / 2, "SAE-4 port to the 25/64 in. tap drill"
                    elif r >= TOOLS[t]["d"] - 1e-6:  # single helix right at the centre: keep 0.05 mm so it clears it
                        off, what = 0.05, "bore"
                    else:
                        off, what = 0.0, "bore" if r >= 8.0 else "counterbore"
                    last = n == len(steps) - 1
                    zf = zlo - 0.5 if (last and through) else zlo
                    # the first step starts at the wall face: the SAE ports' chamfer cone sits above their thread step
                    zs = outer if n == 0 else zhi
                    helix.setdefault((t, round(off, 3), zs, zf, what, 2 * r), []).append(names[0])
                    continue
                dkey = min(TAP_DRILL, key=lambda d: abs(d - 2 * r))
                if abs(dkey - 2 * r) > 0.05:
                    raise ValueError("no drill for a %.3f mm hole at %s on the %s wall" % (2 * r, loc, wname))
                drill.setdefault((TAP_DRILL[dkey], zhi, bottom, through, dkey), []).append(names[0])
                break  # one drill from this step's top to the hole's bottom
        out = []
        for (t, off, zs, zf, what, dia), names in sorted(helix.items(), key=lambda kv: (kv[0][0] != 3, -kv[0][2])):
            out.append(("%s wall: %d x %s %.2f mm, helix, z %.2f..%.2f" % (wname.capitalize(), len(names), what, dia,
                                                                         zf, zs),
                        "helix_bore", t, 0.002, dict(start=zs, final=zf, step=1.0, offset=off), names,
                        dict(holes=len(names), wall=wname)))
        for (t, zs, zb, through, dkey), names in sorted(drill.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
            out.append(("%s wall: drill %d x %.1f mm for %.3f mm, z %.2f..%.2f%s" % (
                wname.capitalize(), len(names), TOOLS[t]["d"], dkey, zb, zs, ", through" if through else ""),
                "drill", t, None, dict(through=through, start=zs, final=zb), names,
                dict(holes=len(names), wall=wname, through=through)))
        return out

    def pick_edges(part, key):
        """edge names of the door opening: the inner wire of the frame's outer front face (y = -111)"""
        s = shapes[part]
        assert key == "door"
        front = [f for f in s.Faces if type(f.Surface).__name__ == "Plane" and f.normalAt(0, 0).y < -0.999
                 and abs(f.BoundBox.YMin - s.BoundBox.YMin) < 0.01]
        f = max(front, key=lambda f: f.Area)
        door = [w for w in f.Wires if not w.isSame(f.OuterWire)]
        door = max(door, key=lambda w: w.BoundBox.DiagonalLength)
        names = []
        for e in door.Edges:
            names += ["Edge%d" % (i + 1) for i, e2 in enumerate(s.Edges) if e2.isSame(e)]
        return names

    def holes(part, key):
        g = cyl_groups(shapes[part])
        if key == "top_r3.02":
            return [n[0] for k, n in g.items() if abs(k[2] - 3.019) < 0.01 and k[4] > 119.9]
        if key == "top_r2.5":
            return [n[0] for k, n in g.items() if abs(k[2] - 2.5) < 0.01 and k[3] > 100]
        if key == "bottom_r2.0":
            return [n[0] for k, n in g.items() if abs(k[2] - 2.0) < 0.01 and k[3] < -3.8]
        if key == "bottom_r3.0":
            return [n[0] for k, n in g.items() if abs(k[2] - 3.0) < 0.01 and k[3] < -3.8]
        raise KeyError(key)

    def drill_for(d):
        fits = [(dd, t) for t, dd in DRILLS.items() if dd <= d + 0.05]
        return max(fits)[1] if fits else None

    joints_ = {}
    pj = os.path.join(IN_DIR, "parts.json")
    if os.path.exists(pj):  # inventory.py's joint cuts per part: (key, part numbers, bbox)
        for row in json.load(open(pj))["parts"]:
            for part_, pre in (("frame", "process_chamber_body"), ("floor", "chamber_floor_plate")):
                if row["slug"].startswith(pre):
                    joints_[part_] = [(c["key"], c["pns"], c["bbox"]) for c in row["cuts"]]

    def joint_at(part, x, y, z):
        """(key, part numbers) of the joint cut at (x, y, z), model frame, or None"""
        for key, pns, bb in joints_.get(part, []):
            if bb[0] - 0.05 <= x <= bb[1] + 0.05 and bb[2] - 0.05 <= y <= bb[3] + 0.05 and bb[4] - 0.05 <= z <= bb[5] + 0.05:
                return key, pns
        return None

    def joint_drill(part, x, y, z):
        """the drill for the insert or dowel pin joints.py cut a hole for at (x, y, z), model frame; None if none"""
        for key, pns, bb in joints_.get(part, []):
            if bb[0] - 0.05 <= x <= bb[1] + 0.05 and bb[2] - 0.05 <= y <= bb[3] + 0.05 and bb[4] - 0.05 <= z <= bb[5] + 0.05:
                for pn in pns:
                    if pn in PN_DRILL:
                        return PN_DRILL[pn], key, pn
        return None

    tcs_made = {}

    def tool_controller(job, t, ipt):
        key = (job.Name, t, ipt)
        if key in tcs_made:
            return tcs_made[key]
        spec = TOOLS[t]
        bit = PathToolBit.Factory.Create("T%d" % t, spec["shape"] + ".fcstd")
        bit.Diameter = spec["d"]
        bit.Length = spec["length"]
        if spec["shape"] == "endmill":
            bit.CuttingEdgeHeight = spec["edge"]
        tc = PathToolController.Create("TC%d_%s" % (t, job.Name), bit, t)
        f = feed_mm_min(t, ipt)
        tc.HorizFeed = "%f mm/min" % f
        tc.VertFeed = "%f mm/min" % (f if spec["shape"] == "drill" else 0.5 * f)
        tc.HorizRapid = "%f mm/min" % RAPID_MM_MIN
        tc.VertRapid = "%f mm/min" % RAPID_MM_MIN
        tc.SpindleSpeed = spec["rpm"]
        tc.SpindleDir = "Forward"
        job.Proxy.addToolController(tc)
        tcs_made[key] = tc
        return tc

    def set_depths(op, start=None, final=None, step=None):
        for prop, val in (("StartDepth", start), ("FinalDepth", final), ("StepDown", step)):
            if val is not None and hasattr(op, prop):
                op.setExpression(prop, None)
                setattr(op, prop, val)

    def feed_bbox(path):
        """[xmin, xmax, ymin, ymax, zmin, zmax] over the end points of G1/G2/G3/G8x moves"""
        cur, pts = {"X": 0.0, "Y": 0.0, "Z": 0.0}, []
        for c in path.Commands:
            cur.update({k: v for k, v in c.Parameters.items() if k in cur})
            if c.Name.lstrip("G").lstrip("0") in ("1", "2", "3", "81", "82", "83"):
                pts.append(dict(cur))
        if not pts:
            return None
        return [round(f(p[k] for p in pts), 2) for k in "XYZ" for f in (min, max)]

    results = []
    rotary = {}
    for su in SETUPS:
        part, flip = su["part"], su.get("flip", False)
        rot_x = su.get("rot_x", 180 if flip else 0)
        shp = shapes[part].copy()
        if "rot" in su:  # setup C's A indexes: a general rotation, model -> machine frame at that index
            r = su["rot"]
            shp.transformShape(FreeCAD.Matrix(r[0][0], r[0][1], r[0][2], 0, r[1][0], r[1][1], r[1][2], 0,
                                              r[2][0], r[2][1], r[2][2], 0, 0, 0, 0, 1))
            rot_x = None
        elif rot_x:
            shp.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), rot_x)
        model = doc.addObject("Part::Feature", su["name"] + "_model")
        model.Shape = shp
        doc.recompute()
        job = PathJob.Create("Job_" + su["name"], [model])
        job.PostProcessor = "linuxcnc"
        job.PostProcessorArgs = "--no-show-editor --precision 3"
        for tc in list(job.Tools.Group):  # drop the default tool controller
            job.Tools.removeObject(tc)
        if "stock_box" in su:  # (x0, y0, z0, L, W, H) in setup coordinates
            x0, y0, lo, L, W, H = su["stock_box"]
        else:  # blank centred in x and y; z range flips with the part
            L, W, z0, z1 = su["stock"]
            lo, hi = (-z1, -z0) if flip else (z0, z1)
            x0, y0, H = -L / 2, -W / 2, hi - lo
        old = job.Stock
        job.Stock = PathStock.CreateBox(job, FreeCAD.Vector(L, W, H),
                                        FreeCAD.Placement(FreeCAD.Vector(x0, y0, lo), FreeCAD.Rotation()))
        doc.removeObject(old.Name)
        base = job.Model.Group[0]
        doc.recompute()

        ops_meta = []

        def add(label, kind, t, ipt, cfg, base_subs, extra_meta=None):
            label = clean_label(label)
            tc = tool_controller(job, t, ipt)
            if kind == "face":
                op = Path.Op.MillFace.Create("Face", parentJob=job)
                op.Base = [(base, base_subs)]
                # The face's bounding box grown by the tool radius (ClearEdges only works with "Boundbox"). With
                # "Stock", the tool stayed inside the stock, so the corners were never faced, and FreeCAD's default
                # 45 deg zig-zag touched the edges only at its turns: CAMotics showed unfaced patches up to 20 mm in
                # from every edge. Along x the turns run down the x edges and the outer passes along the y edges.
                op.BoundaryShape = "Boundbox"
                op.StepOver = 70
                op.ClearEdges = True
                op.ZigZagAngle = 0.0
            elif kind == "adaptive_out":
                op = Path.Op.Adaptive.Create("Adaptive", parentJob=job)
                op.Base = [(base, base_subs)]
                op.Side = "Outside"
                op.OperationType = "Clearing"
                op.UseOutline = True
                op.StepOver = cfg["stepover"]
                op.Tolerance = 0.1
            elif kind == "adaptive_in":  # clear inside a closed loop of model edges
                op = Path.Op.Adaptive.Create("Adaptive", parentJob=job)
                op.Base = [(base, base_subs)]
                op.Side = "Inside"
                op.OperationType = "Clearing"
                op.StepOver = cfg["stepover"]
                op.Tolerance = 0.1
            elif kind in ("profile_holes", "profile_perimeter"):
                op = Path.Op.Profile.Create("Profile", parentJob=job)
                op.Base = [(base, base_subs)]
                op.processHoles = kind == "profile_holes"
                op.processPerimeter = kind == "profile_perimeter"
                op.processCircles = False
                op.Side = "Outside" if kind == "profile_holes" else "Inside"
                op.OffsetExtra = cfg.get("extra", 0.0)
            elif kind == "pocket":
                op = Path.Op.PocketShape.Create("Pocket", parentJob=job)
                op.Base = [(base, base_subs)]
                op.OffsetPattern = "Offset"
                op.StepOver = 50
            elif kind == "helix":
                # build the op directly: Helix.Create()/Drilling.Create() call findAllHoles(), which
                # fails headless in 1.0.2 (self.model is None until the first execute)
                op = doc.addObject("Path::FeaturePython", "Helix")
                op.Proxy = Path.Op.Helix.ObjectHelix(op, "Helix", job)
                op.Base = [(base, base_subs)]
                # One helix at the finished radius (48 - D/2), i.e. a trepan: the slug drops out.
                # FreeCAD 1.0.2's helix generator puts a lone helix at (outer + inner)/2
                # (Path/Base/Generator/helix.py), so StartRadius alone lands it 4.76 mm short;
                # OffsetExtra = -D/4 with StartRadius = 48 - D/2 puts it on 48 - D/2.
                d = TOOLS[t]["d"]
                op.StartRadius = 48.0 - d / 2
                op.OffsetExtra = -d / 4
                op.Direction = "CCW"
            elif kind == "helix_bore":  # one helix at r - offset - D/2 (FreeCAD 1.0.2's single-helix mode, r <= D)
                op = doc.addObject("Path::FeaturePython", "Helix")
                op.Proxy = Path.Op.Helix.ObjectHelix(op, "Helix", job)
                op.Base = [(base, base_subs)]
                op.StartRadius = 0.0
                op.OffsetExtra = cfg.get("offset", 0.0)
                op.Direction = "CCW"
            elif kind == "drill":
                op = doc.addObject("Path::FeaturePython", "Drill")
                op.Proxy = Path.Op.Drilling.ObjectDrilling(op, "Drill", job)
                op.Base = [(base, base_subs)]
                op.RetractMode = "G98"  # back to the initial Z between holes
                if cfg.get("through"):  # full diameter out of the far face (the 118 deg point goes 0.3 D past)
                    op.ExtraOffset = "Drill Tip"
                op.PeckEnabled = True
                op.PeckDepth = TOOLS[t]["d"]
            else:
                raise ValueError(kind)
            op.Label = label
            op.ToolController = tc
            if hasattr(op, "CoolantMode"):
                op.CoolantMode = "Flood"
            if kind == "pocket":
                fb = base.Shape.getElement(base_subs[0]).BoundBox.ZMin
                set_depths(op, cfg["start"], fb, cfg["step"])
            elif kind == "drill":
                faces = [base.Shape.getElement(n) for n in base_subs]
                set_depths(op, cfg.get("start", max(f.BoundBox.ZMax for f in faces)),
                           cfg.get("final", min(f.BoundBox.ZMin for f in faces)))
                op.setExpression("RetractHeight", None)
                op.RetractHeight = op.StartDepth.Value + 2.0
            else:
                set_depths(op, cfg.get("start"), cfg.get("final"), cfg.get("step"))
            if su.get("clear_z") is not None:  # above the fixtures, not just the stock
                for prop in ("ClearanceHeight", "SafeHeight"):
                    if hasattr(op, prop):
                        op.setExpression(prop, None)
                        setattr(op, prop, su["clear_z"])
            meta = dict(op=op.Name, label=label, kind=kind, tool=t, tool_name=TOOLS[t]["name"],
                        rpm=TOOLS[t]["rpm"], feed_mm_min=round(feed_mm_min(t, ipt), 1),
                        chip_load_in=ipt or TOOLS[t].get("ipt"), mm_per_rev=TOOLS[t].get("mm_rev"),
                        faces=base_subs if len(base_subs) <= 4 else "%d faces" % len(base_subs),
                        start_depth=round(op.StartDepth.Value, 3), final_depth=round(op.FinalDepth.Value, 3),
                        step_down=round(op.StepDown.Value, 3) if hasattr(op, "StepDown") else None)
            meta.update(extra_meta or {})
            ops_meta.append((op, meta))

        for label, kind, t, ipt, cfg in su["ops"]:
            try:
                if kind == "drill":
                    add(label, kind, t, ipt, cfg, holes(part, cfg["holes"]))
                elif kind in ("drill_all", "drill_top"):
                    # drill_all (part upside down): every hole step that opens downward (through holes too);
                    # drill_top: the blind steps that open only upward. Probed on the model, 0.05 mm past each end.
                    s0 = shapes[part]
                    g = cyl_groups(s0)
                    groups = {}

                    def air(x, y, z):
                        return not s0.isInside(FreeCAD.Vector(x, y, z), 1e-4, True)

                    # insert and dowel holes (PN_DRILL): one drill from the mouth to the bottom of the hole's steps
                    by_loc, done = {}, set()
                    for (x, y, r, zmin, zmax), names in g.items():
                        if r <= 4.5:
                            by_loc.setdefault((x, y), []).append((r, zmin, zmax, names[0]))
                    for (x, y), steps in by_loc.items():
                        steps.sort(key=lambda st: st[1] if kind == "drill_all" else -st[2])
                        r0, z0_, z1_, n0 = steps[0]
                        jd = joint_drill(part, x, y, 0.5 * (z0_ + z1_))
                        if jd is None:
                            continue
                        open_ = air(x, y, z0_ - 0.05) if kind == "drill_all" else air(x, y, z1_ + 0.05)
                        if not open_:
                            continue
                        stack = [steps[0]]
                        for st in steps[1:]:  # contiguous steps, no wider than the one before
                            prev = stack[-1]
                            joined = abs(st[1] - prev[2]) < 0.02 if kind == "drill_all" else abs(st[2] - prev[1]) < 0.02
                            if not joined or st[0] > prev[0] + 1e-6:
                                break
                            stack.append(st)
                        zlo_, zhi_ = min(st[1] for st in stack), max(st[2] for st in stack)
                        rl = stack[-1][0]
                        zfar = zhi_ + 0.05 if kind == "drill_all" else zlo_ - 0.05
                        far_open = all(air(x + 0.9 * rl * math.cos(a), y + 0.9 * rl * math.sin(a), zfar)
                                       for a in (0.3, 1.9, 3.5, 5.1))
                        if kind == "drill_top" and far_open:
                            continue  # through holes are drilled from below (drill_all)
                        # setup B is the part upside down: its depths are the model's negated
                        start_, final_ = (-zlo_, -zhi_) if kind == "drill_all" else (zhi_, zlo_)
                        groups.setdefault(("pn", jd[0], start_, final_, far_open, jd[1]), []).append(stack[-1][3])
                        done.update((x, y, st[0], st[1], st[2]) for st in stack)
                    for (x, y, r, zmin, zmax), names in g.items():
                        if r > 4.5:  # the 96 mm port (setup A); part-turn arcs are already left out
                            continue
                        if (x, y, r, zmin, zmax) in done:
                            continue
                        dt = drill_for(2 * r)
                        if dt is None:
                            continue
                        down, up = air(x, y, zmin - 0.05), air(x, y, zmax + 0.05)
                        if kind == "drill_all" and not down:
                            continue
                        if kind == "drill_top" and (down or not up):
                            continue
                        zfar = zmax + 0.05 if kind == "drill_all" else zmin - 0.05
                        far_open = all(air(x + 0.9 * r * math.cos(a), y + 0.9 * r * math.sin(a), zfar)
                                       for a in (0.3, 1.9, 3.5, 5.1))
                        jt = joint_at(part, x, y, 0.5 * (zmin + zmax)) if joints_ else None
                        nominal = next((d for d in NOMINAL_TAP if abs(2 * r - d) < 0.01), None)
                        if jt is not None and nominal is not None:
                            dt = NOMINAL_TAP[nominal]  # a screw joint's hole at the thread's nominal size: tapped
                        elif jt is None and abs(2 * r - 6.0) < 0.01 and not far_open:
                            # a plain blind 6 mm hole with no joint is a dowel or diamond-pin hole (the floor's FP-07)
                            dt = 14
                        groups.setdefault((dt, zmin, zmax, far_open), []).append(names[0])
                    pn_groups = {k: v for k, v in groups.items() if k[0] == "pn"}
                    groups = {k: v for k, v in groups.items() if k[0] != "pn"}
                    for (_, dt, s_, f_, far_open, key), names in sorted(pn_groups.items(), key=lambda kv: (kv[0][1], kv[0][2])):
                        add("Drill %d x %.1f mm for the %s holes, %s, z %.2f..%.2f (setup)%s" % (
                            len(names), TOOLS[dt]["d"], key, "ream after" if TOOLS[dt]["d"] in (2.9, 5.8) else "STI tap after",
                            f_, s_, ", through" if far_open else ""),
                            "drill", dt, None, dict(through=far_open, start=s_, final=f_), names,
                            dict(holes=len(names), through=far_open, joint=key))
                    # the step nearest the surface the drill enters from goes first: a step below another must
                    # not be drilled before the one above it is open (its R plane would be inside solid stock)
                    order = sorted(groups.items(), key=(lambda kv: (kv[0][1], kv[0][0])) if kind == "drill_all"
                                   else (lambda kv: (-kv[0][2], kv[0][0])))
                    for (dt, zmin, zmax, far_open), names in order:
                        add("Drill %d x %.1f mm step z %.2f..%.2f (model)%s%s" % (
                            len(names), TOOLS[dt]["d"], zmin, zmax, ", through" if far_open else "",
                            ", dowel or diamond-pin holes, ream 6 H7 after" if dt == 14 else ""),
                            "drill", dt, None, dict(through=far_open), names,
                            dict(holes=len(names), through=far_open))
                elif kind == "wall":
                    for lab2, k2, t2, ipt2, cfg2, names, meta2 in wall_ops(part, cfg["wall"]):
                        add(lab2, k2, t2, ipt2, cfg2, names, meta2)
                elif "edges" in cfg:
                    add(label, kind, t, ipt, cfg, pick_edges(part, cfg["edges"]))
                else:
                    add(label, kind, t, ipt, cfg, pick_faces(part, flip, cfg["face"]))
            except Exception as e:  # keep going: record what failed
                ops_meta.append((None, dict(label=label, kind=kind, tool=t, error="%s: %s" % (type(e).__name__, e))))

        doc.recompute()
        posted = []
        cur_tool = None
        for op, meta in ops_meta:
            if op is None:
                continue
            meta["freecad_cycle_time"] = getattr(op, "CycleTime", None)
            meta["commands"] = len(op.Path.Commands)
            meta["feed_move_bbox"] = feed_bbox(op.Path)  # tool-centre end points of cutting moves
            if meta["commands"] == 0:
                meta["error"] = "operation produced no path"
                continue
            if op.ToolController.ToolNumber != cur_tool:
                posted.append(op.ToolController)
                cur_tool = op.ToolController.ToolNumber
            posted.append(op)
        job.recompute()
        gpath = os.path.join(GCODE_DIR, su["name"] + ".ngc")
        gcode = linuxcnc_post.export(posted, gpath, "--no-show-editor --precision 3")
        if not gcode:
            gcode = open(gpath).read()
        if su.get("rotary"):
            rotary.setdefault(su["rotary"], []).append((su["a_deg"], su["name"], gcode))
        results.append(dict(setup=su["name"], part=part, rot_about_x_deg=rot_x,
                            rotation_model_to_setup=[list(r) for r in rot_matrix(su)], a_deg=su.get("a_deg"),
                            rotary=su.get("rotary"),
                            stock_box=su.get("stock") or su.get("stock_box"),
                            gcode=gpath, freecad_job_cycle_time=getattr(job, "CycleTime", None),
                            ops=[m for _, m in ops_meta], _gcode_text=gcode))
        print("setup", su["name"], "job CycleTime", getattr(job, "CycleTime", None), flush=True)
    for name, indexed in rotary.items():  # one Haas program per rotary setup, with the A moves
        path = os.path.join(GCODE_DIR, name + "_haas.nc")
        with open(path, "w") as f:
            f.write(haas_rotary_program(sorted(indexed)))
        for r in results:
            if r.get("rotary") == name:
                r["haas_program"] = path
        print("wrote", path, flush=True)
    return FreeCAD.Version(), results


# --- setup C: one Haas program with the A moves ---------------------------------------------------------------
def haas_rotary_program(indexed, number=2660):
    """Join the per-index LinuxCNC programs [(a_deg, setup name, text)] into one program for a Haas VF-4 with an
    HRT210 as its A axis (3+1 indexing). Each index's body (its operations, without the post's preamble and postamble)
    is preceded by: coolant and spindle off, Z to machine home (G53 G0 Z0.: the frame and the dummy-floor plate swing
    204 mm about A, so no work plane is safe for turning), unclamp (M11), G0 A, clamp (M10). Tool changes become Haas'
    'T M06'; if the tool is already in the spindle the Haas skips the change. Ends back at A0 with M30."""
    out = ["%", "O%05d (DESKTOP LPBF CHAMBER FRAME, SETUP C = F-S3, THE FOUR WALLS ON THE HRT210)" % number,
           "(freecad_cam.py: FreeCAD 1.0.2's linuxcnc post per A index, joined for a Haas with an A axis)",
           "(G54: X0 at the frame's interior floor plane, 3.9 mm above its bottom face; Y0 Z0 on the A axis)",
           "(A0 front wall up, A90 left, A180 back, A270 right; A turns the part about +X, right hand)",
           "(set the HRT210's direction so A90 brings the left wall up; dummy-floor plate on the platter, 2 pins, 18 M4)",
           "G21", "G17 G40 G49 G80 G90", "G54"]
    n_changes = 0
    for a_deg, name, text in indexed:
        lines = text.splitlines()
        i0 = next(i for i, ln in enumerate(lines) if ln.startswith("(begin operation"))
        i1 = next((i for i, ln in enumerate(lines) if ln.startswith("(begin postamble")), len(lines))
        out += ["(index A%d: %s, %s)" % (a_deg, WALLS[a_deg][0] + " wall up", name), "M09", "M05", "G53 G00 Z0.",
                "M11", "G00 A%d." % a_deg, "M10"]
        for ln in lines[i0:i1]:
            m = re.fullmatch(r"\s*M0?6\s+T(\d+)\s*", ln)
            if m:
                out.append("T%d M06" % int(m.group(1)))
                n_changes += 1
                continue
            out.append(ln)
    out += ["M09", "M05", "G53 G00 Z0.", "M11", "G00 A0.", "M10", "M30", "%"]
    haas_rotary_program.tool_changes = n_changes
    return "\n".join(out) + "\n"


# --- G-code recount (plain Python) ----------------------------------------------------------------
WORD = re.compile(r"([A-Z])([-+]?\d*\.?\d+)")


def gcode_times(text):
    """Per operation: feed/rapid length and time from the posted G-code (mm, F in mm/min)."""
    pos = {"X": 0.0, "Y": 0.0, "Z": 0.0}
    feed = None
    motion = None
    cycle = None  # canned-cycle state
    retract_mode = "G98"
    ops = {}
    cur = None
    tool_changes = 0
    for raw in text.splitlines():
        m = re.search(r"\(begin operation: (.*)\)", raw)
        if m:
            cur = ops.setdefault(m.group(1), dict(feed_mm=0.0, rapid_mm=0.0, feed_s=0.0, rapid_s=0.0))
            continue
        line = re.sub(r"\(.*?\)", "", raw).strip().upper()
        if not line or cur is None:
            continue
        words = WORD.findall(line)
        g = [float(v) for k, v in words if k == "G"]
        p = {k: float(v) for k, v in words if k != "G"}
        if "M" in p and int(p["M"]) == 6:
            tool_changes += 1
        if "F" in p:
            feed = p["F"]
        for code in g:
            if code in (0, 1, 2, 3):
                motion, cycle = int(code), None
            elif code in (81, 82, 83, 73):
                motion, cycle = None, int(code)
            elif code == 80:
                motion = cycle = None
            elif code in (98, 99):
                retract_mode = "G98" if code == 98 else "G99"

        def move(dist, rapid):
            if rapid:
                cur["rapid_mm"] += dist
                cur["rapid_s"] += dist / RAPID_MM_MIN * 60
            else:
                cur["feed_mm"] += dist
                cur["feed_s"] += dist / feed * 60 if feed else 0.0

        if cycle is not None and ("X" in p or "Y" in p or "Z" in p or "R" in p):
            init_z = pos["Z"]
            x, y = p.get("X", pos["X"]), p.get("Y", pos["Y"])
            r = p.get("R", cur.get("_r", init_z))
            cur["_r"] = r
            z = p.get("Z", cur.get("_z", init_z))
            cur["_z"] = z
            move(math.hypot(x - pos["X"], y - pos["Y"]), True)
            move(abs(init_z - r), True)
            if cycle in (83, 73) and p.get("Q", cur.get("_q")):
                q = p.get("Q", cur.get("_q"))
                cur["_q"] = q
                depth = r
                while depth > z + 1e-9:
                    nxt = max(depth - q, z)
                    move(depth - nxt + (0.254 if depth < r else 0.0), False)  # 0.254: LinuxCNC peck clearance
                    depth = nxt
                    if depth > z + 1e-9:
                        move(r - depth, True)       # out to R (G83) ...
                        move(r - depth - 0.254, True)  # ... and back down
            else:
                move(r - z, False)
            back = init_z if retract_mode == "G98" else r
            move(abs(back - z), True)
            pos.update(X=x, Y=y, Z=back)
            continue
        if motion is None or not any(k in p for k in "XYZ"):
            continue
        new = {k: p.get(k, pos[k]) for k in "XYZ"}
        if motion in (0, 1):
            d = math.dist((pos["X"], pos["Y"], pos["Z"]), (new["X"], new["Y"], new["Z"]))
        else:  # arc in XY (G17), I/J relative to start
            cx, cy = pos["X"] + p.get("I", 0.0), pos["Y"] + p.get("J", 0.0)
            rad = math.hypot(pos["X"] - cx, pos["Y"] - cy)
            a0 = math.atan2(pos["Y"] - cy, pos["X"] - cx)
            a1 = math.atan2(new["Y"] - cy, new["X"] - cx)
            sweep = (a0 - a1) if motion == 2 else (a1 - a0)
            sweep %= 2 * math.pi
            if sweep < 1e-9:
                sweep = 2 * math.pi
            d = math.hypot(rad * sweep, new["Z"] - pos["Z"])
        move(d, motion == 0)
        pos.update(new)
    for v in ops.values():
        for k in [k for k in v if k.startswith("_")]:
            del v[k]
    return ops, tool_changes


def hms(s):
    return "%d:%02d:%02d" % (s // 3600, s % 3600 // 60, s % 60)


def summarise(version, results):
    out = dict(
        tool="FreeCAD %s (%s), CAM workbench, run headless with freecadcmd" % (".".join(version[:3]), version[3]),
        post="linuxcnc (FreeCAD's Path/Post/scripts/linuxcnc_post.py, --precision 3), mm, G-code in "
             + GCODE_DIR,
        machine="Haas VF-4 (CT40, 8100 rpm, 22.4 kW), 3-axis; setup C 3+1 on an HRT210 (A); rapids 25.4 m/min for "
                "the recount (A index moves not timed)",
        material="6061-T6",
        tools={("T%d" % t): dict(v, feed_mm_min=round(feed_mm_min(t), 1)) for t, v in TOOLS.items()},
        assumptions=[
            "Feeds: mm/min = rpm x flutes x chip load (in/tooth) x 25.4; drills rpm x 0.1 mm/rev, peck = 1 x D.",
            "T2 chip load 0.005 in/tooth (middle of 0.004-0.006) for adaptive and profile, 0.002 for the helical "
            "port trepan; plunge/ramp feed = half the horizontal feed for end mills.",
            "T1 at 3000 rpm (spindle-limited choice), 70 % step-over zig-zag over the whole stock.",
            "Frame stock = 317.5 x 228.6 x 127 blank with the 274 x 184 core already waterjet/bandsawn out: "
            "the outside is cut by Adaptive (stock box), the opening by Profile only (3 mm radial).",
            "Setup A cuts outside and opening to z 58, setup B from the bottom to z 58 (meet line at mid-height).",
            "Floor setup B stock = 312 x 222 outline box (outside already cut in A, down to z -20.5) so the "
            "Adaptive only cuts the U-notches (and four corner slivers); the 2.2 mm web under z -20.5 is faced off.",
            "Face ops: BoundaryShape Boundbox with ClearEdges (the face's bounding box plus the tool radius) and "
            "ZigZagAngle 0, so the turns run along the x edges and the outer passes along the y edges.",
            "Floor port trepan and slots: final depth z -23.2, 0.5 mm past the blank, so the slugs drop in A.",
            "Slots 124 x 8 and 20 x 104 both on a 1/4 in. end mill (T9): T3 1/2 in. does not fit an 8 mm slot.",
            "Drills: largest of 3.3/4.2/5.0/6.0 mm that fits each hole step; taps, reamers, insert tools, "
            "chamfers and deburring are not costed. Tool changes are counted, not timed. Floor holes: those "
            "that open on top (and not on the bottom) are drilled in setup A, the rest from below in B; the "
            "step nearest the entry face first. Steps whose far end opens at full diameter (through) get "
            "ExtraOffset = Drill Tip; blind steps stop with the drill tip at the model's flat floor, so their "
            "full diameter ends 0.3 x D short.",
            "Setup C (F-S3, since 2026-11-25): the four walls on an HRT210, one FreeCAD job per A index in the machine "
            "frame at that index (A along machine X, work zero on the A axis), joined into one Haas program with the A "
            "moves (gcode/frame_C_haas.nc). A0 front: the door opening, T3 adaptive through the 16 mm wall. A90 left and "
            "A270 right: the 18 mm recoater bores and the 25.4 mm KF-25 bore helix-milled with T3; the through-beam's "
            "10.8 mm counterbore and the SAE-4 O2 port (to its 9.92 mm tap drill) with T9; the holes drilled with their "
            "tap or STI drill (TAP_DRILL). A180 back: the 120 x 8 inlet slot profiled with T9, the argon SAE-4 port, "
            "the plenum inserts, pins and rail holes. Taps, STI taps, reamers and the SAE port tool are not programmed.",
        ],
        freecad_notes=[
            "Primary times are the G-code recount (cut_time_min, rapid_time_min). FreeCAD's own estimate "
            "(freecad_cycle_time per op, Job CycleTime) is whole seconds and, tested on single moves in 1.0.2, "
            "times any move that changes Z at the vertical (plunge) feed over its full 3D length, ignores the F "
            "words, and does not expand G81/G83 cycles; so it reads high for ramps, helices and pocket entries.",
            "Drilling.Create()/Helix.Create() raise TypeError headless in 1.0.2 (findAllHoles runs before the "
            "op has a model); the ops are built from ObjectDrilling/ObjectHelix directly.",
            "Helix generator in 1.0.2 puts a single helix at (outer+inner)/2; worked around (see the script) so "
            "the port trepan runs on radius 48 - D/2.",
        ],
        camotics=dict(ran=True, script="desktop-lpbf/analysis/machining/camotics_sim.py",
                      results="desktop-lpbf/analysis/out/machining/camotics/camotics_sim.json",
                      how="CAMotics 1.2.0 camsim in Docker on ubuntu:18.04 (camotics.Dockerfile); the summary "
                          "is written here by camotics_sim.py after each run"),
        parts={},
    )
    for r in results:
        times, ntc = gcode_times(r.pop("_gcode_text"))
        tot = dict(feed_mm=0.0, rapid_mm=0.0, feed_s=0.0, rapid_s=0.0)
        fc_total = 0
        for m in r["ops"]:
            if "error" in m:
                continue
            g = times.get(m["label"]) or times.get(m["op"])
            if g:
                m["path_feed_mm"] = round(g["feed_mm"], 1)
                m["path_rapid_mm"] = round(g["rapid_mm"], 1)
                m["cut_time_min"] = round(g["feed_s"] / 60, 2)
                m["rapid_time_min"] = round(g["rapid_s"] / 60, 2)
                for k in tot:
                    tot[k] += g[k]
            ct = m.get("freecad_cycle_time")
            if ct and re.fullmatch(r"\d+:\d\d:\d\d", ct):
                h, mi, s = (int(x) for x in ct.split(":"))
                fc_total += 3600 * h + 60 * mi + s
        r["totals"] = dict(path_feed_mm=round(tot["feed_mm"], 1), path_rapid_mm=round(tot["rapid_mm"], 1),
                           cut_time_min=round(tot["feed_s"] / 60, 2), rapid_time_min=round(tot["rapid_s"] / 60, 2),
                           total_min=round((tot["feed_s"] + tot["rapid_s"]) / 60, 2),
                           total_hms=hms(tot["feed_s"] + tot["rapid_s"]), tool_changes=ntc,
                           freecad_sum_of_op_cycle_times_min=round(fc_total / 60, 2))
        p = out["parts"].setdefault(r["part"], dict(setups=[], total_min=0.0, freecad_total_min=0.0))
        p["setups"].append(r)
        p["total_min"] = round(p["total_min"] + r["totals"]["total_min"], 2)
        p["freecad_total_min"] = round(p["freecad_total_min"] + r["totals"]["freecad_sum_of_op_cycle_times_min"], 2)
    for p in out["parts"].values():
        p["total_hms"] = hms(p["total_min"] * 60)
    return out


def main():
    try:
        import FreeCAD  # noqa: F401
    except ImportError:  # plain python: re-run under freecadcmd
        exe = os.environ.get("FREECADCMD") or (sys.argv[1] if len(sys.argv) > 1 else None)
        if not exe:
            sys.exit("set FREECADCMD=/path/to/freecadcmd (FreeCAD 1.0.x) or pass it as the first argument")
        code = "import runpy; runpy.run_path(%r, run_name='__main__')" % os.path.abspath(__file__)
        sys.exit(subprocess.call([exe, "-c", code]))
    version, results = run_cam()
    out = summarise(version, results)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    for name, p in out["parts"].items():
        for r in p["setups"]:
            print(name, r["setup"], r["totals"])
            for m in r["ops"]:
                print("   ", m.get("label"), "|", m.get("error") or (m.get("cut_time_min"), m.get("rapid_time_min"),
                      m.get("freecad_cycle_time"), m.get("feed_move_bbox")))
        print(name, "total", p["total_hms"])
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
