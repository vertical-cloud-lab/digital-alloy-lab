"""Parametric CAD model of room 154 CB (the atomizer lab) and the Class D extinguisher install.

CadQuery, millimetres. x points east, y north and z up. The origin is where the interior faces of
the west and south walls of room 154 would meet. Closet 158 fills that corner, so the origin
itself sits inside 158.

Where each number comes from (see README.md for the full list):

* Room outline, doors, column, closet 158: BYU Facilities Planning floor plan of CB, 1st floor
  (Revit export, 12/6/2024), as posted in byu-vcl (`cb154.pdf`, `cb154-annotated.pdf`). The
  annotated copy gives the 25.78 ft x 31.38 ft interior, the column 10.29 ft from the north wall
  and 4.67 ft from the west wall, and closet 158 as 8.53 ft wide. Door positions were measured
  off the raster at 0.5 in/px, calibrated to those two room dimensions.
* Inert-gas booth: "the area to the pillar and over to the edge of the red line is about
  14' W x 10' D" (byu-vcl#31). Its contents and its strip-curtain door come from the room-camera
  frame of 2026-10-01 17:01 (byu-vcl docs/stream-cams.md) and the photos of 2026-09-03 and
  2026-09-28 (digital-alloy-lab PR 216). Contents are good to about +/- 1 ft.
* Amerex B570: manufacturer spec sheet (35 in tall, 13 in wide, 8 in deep, 30 lb agent, 53 lb
  shipping weight with the box, "included bracket: wall"). Body diameter and valve layout are
  read from the issue photos.
* Mounting heights: NFPA 10 sec. 6.1.3.8 and the B570 owner's manual: gross weight over 40 lb
  means the top is at most 3.5 ft (42 in) above the floor, and the bottom is at least 4 in above it.

Not measured, and not verifiable remotely (all three lab Pis were offline on 2026-11-19):
ceiling and booth heights, what the column is made of, the booth's framing, and where the
furniture outside the booth stands. All of these are parameters below.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import cadquery as cq

FT = 304.8
IN = 25.4

# --------------------------------------------------------------------------------------------
# Room 154 (interior faces), from the floor plan
# --------------------------------------------------------------------------------------------
ROOM_W = 25.78 * FT          # west face to east face
ROOM_D = 31.38 * FT          # south face to north face
ROOM_H = 10.0 * FT           # assumed: not on the plan
T_CMU = 8 * IN               # north, west and south walls are CMU (the photos show block coursing)
T_PART = 5 * IN              # east wall and closet 158: stud partitions (assumed)

# Doors: (name, wall, start, end) in feet along the wall, measured off the plan.
# hinge: which jamb carries the hinges; swing: "in" (into 154) or "out".
DOORS = {
    "S (main, to corridor 101)": dict(wall="S", a=10.17, b=14.03, hinge="a", swing="in"),
    "154-1 (west)": dict(wall="W", a=13.88, b=17.79, hinge="a", swing="in"),
    "154-2 (north, to 123)": dict(wall="N", a=19.90, b=22.90, hinge="b", swing="in"),
    "E (to 154A)": dict(wall="E", a=16.50, b=19.60, hinge="b", swing="out"),
}

# Structural column ("the pillar"): 4.67 ft from the west wall, its north face 10.29 ft from
# the north wall, about 1.5 ft square on the plan.
COL_X0, COL_X1 = 4.67 * FT, 6.17 * FT
COL_Y1 = ROOM_D - 10.29 * FT
COL_Y0 = COL_Y1 - 1.5 * FT

# Closet 158 in the south-west corner (not part of the lab's ~700 ft2)
C158_X1 = 8.53 * FT
C158_Y1 = 13.30 * FT

# Small chases on the east wall (plan)
CHASES = [(ROOM_W - 1.0 * FT, ROOM_W, 19.6 * FT, 20.9 * FT), (ROOM_W - 1.0 * FT, ROOM_W, 0.0, 1.25 * FT)]

# --------------------------------------------------------------------------------------------
# Inert-gas booth (sheet metal on a frame), NW corner: 14 ft E-W x 10.29 ft N-S
# --------------------------------------------------------------------------------------------
BOOTH_X1 = 14.0 * FT
BOOTH_Y0 = COL_Y1            # south wall runs along the column's north face
BOOTH_H = 8.0 * FT           # assumed
T_BOOTH = 2 * IN
BOOTH_DOOR = (9.75 * FT, 13.5 * FT)   # strip curtain, south wall, east end


# --------------------------------------------------------------------------------------------
# Amerex B570 and its install
# --------------------------------------------------------------------------------------------
B570_H = 35 * IN             # overall height (spec sheet)
B570_W = 13 * IN             # overall width with hose and applicator (spec sheet)
B570_D = 8 * IN              # overall depth (spec sheet)
B570_BODY_D = 7.0 * IN       # cylinder diameter (photos; the 8 in depth includes the hose clip)
B570_BODY_H = 29.0 * IN      # shell incl. top dome (to the neck)
B570_GROSS_LB = 50.0         # ~53 lb shipping weight minus the box
HOOK_BELOW_TOP = 5.5 * IN    # the hook's seat (under the collar flange) is this far below the top

MAX_TOP = 42 * IN            # NFPA 10 6.1.3.8.2 (gross weight > 40 lb)
MIN_BOTTOM = 4 * IN          # NFPA 10 6.1.3.8.3
TOP_Z = 41 * IN              # chosen: 1 in under the limit, so a slightly high hole still passes
BOTTOM_Z = TOP_Z - B570_H    # 6 in
HOOK_Z = TOP_Z - HOOK_BELOW_TOP   # 35.5 in
HOOK_PLATE_Z0 = HOOK_Z - 4.5 * IN  # bottom of the hook's back plate

# Recommended spot: east face of the column, centred on it, outside the booth
MOUNT_FACE_X = COL_X1
MOUNT_Y = (COL_Y0 + COL_Y1) / 2
STANDOFF = 0.4 * IN          # cylinder's back to the column face: it rests against the hook plate
HOOK_REACH = STANDOFF + B570_BODY_D / 2 + 1.3 * IN   # arm length out to the lip, past the collar
HOOK_PLATE_H = 4.5 * IN      # back plate height, below the seat
AXIS_X = MOUNT_FACE_X + STANDOFF + B570_BODY_D / 2

# Alternates, as (x, y, facing) of the wall point and the direction the extinguisher faces
ALTERNATES = {
    "L2 booth south wall, beside the curtain": (8.9 * FT, BOOTH_Y0, (0, -1)),
    "L3 north CMU wall, east of the booth": (16.6 * FT, ROOM_D, (0, -1)),
}

# Existing BYU CO2 extinguisher: the Feb 2026 photo shows it on the latch side of a door,
# read here as door 154-1 (west wall, latch at the north jamb). Not verified.
CO2_POS = (0.0, 18.35 * FT)

# Colours
C_WALL = (0.86, 0.85, 0.80)
C_CMU = (0.90, 0.88, 0.80)
C_FLOOR = (0.80, 0.80, 0.78)
C_BOOTH = (0.72, 0.75, 0.78)
C_CURTAIN = (0.80, 0.90, 0.95)
C_DOOR = (0.65, 0.45, 0.25)
C_COL = (0.78, 0.78, 0.76)
C_YELLOW = (0.98, 0.80, 0.05)
C_RED = (0.80, 0.10, 0.10)
C_BLACK = (0.08, 0.08, 0.08)
C_BLUE = (0.10, 0.20, 0.75)
C_STEEL = (0.75, 0.76, 0.78)
C_ALU = (0.82, 0.83, 0.85)


@dataclass
class Part:
    name: str
    shape: cq.Shape
    color: tuple
    group: str = "room"            # room | booth | equipment | install | marker
    opacity: float = 1.0
    meta: dict = field(default_factory=dict)


def box(x0, y0, z0, x1, y1, z1) -> cq.Shape:
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()


def cyl(r, h, x, y, z, axis=(0, 0, 1)) -> cq.Shape:
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(*axis))


# --------------------------------------------------------------------------------------------
# Room
# --------------------------------------------------------------------------------------------
def _wall_with_openings(wall: str, openings, t, h, x0=None, x1=None):
    """A straight wall on one side of the room, with door openings cut (7 ft tall)."""
    if wall == "N":
        s = box(-T_CMU, ROOM_D, 0, ROOM_W + T_PART, ROOM_D + t, h)
    elif wall == "S":
        s = box(-T_CMU, -t, 0, ROOM_W + T_PART, 0, h)
    elif wall == "W":
        s = box(-t, -T_CMU, 0, 0, ROOM_D + T_CMU, h)
    else:
        s = box(ROOM_W, -T_CMU, 0, ROOM_W + t, ROOM_D + T_CMU, h)
    for a, b in openings:
        if wall in "NS":
            y0, y1 = (ROOM_D - 1, ROOM_D + t + 1) if wall == "N" else (-t - 1, 1)
            s = s.cut(box(a, y0, -1, b, y1, 7 * FT))
        else:
            x0_, x1_ = (-t - 1, 1) if wall == "W" else (ROOM_W - 1, ROOM_W + t + 1)
            s = s.cut(box(x0_, a, -1, x1_, b, 7 * FT))
    return s


def door_leaf(name: str, open_deg: float = 0.0) -> Part:
    """A 36 in x 84 in leaf, hinged on the plan's jamb, rotated `open_deg` toward its swing."""
    d = DOORS[name]
    a, b = d["a"] * FT, d["b"] * FT
    leaf_w, leaf_t = min(36 * IN, b - a - 2 * IN), 1.75 * IN
    hinge = a + 1 * IN if d["hinge"] == "a" else b - 1 * IN
    sgn_along = 1 if d["hinge"] == "a" else -1
    wall = d["wall"]
    # local leaf: from the hinge along +u for leaf_w, thickness along the wall normal
    if wall in "NS":
        y_face = ROOM_D if wall == "N" else 0.0
        leaf = box(0, -leaf_t / 2, 0, leaf_w, leaf_t / 2, 84 * IN)
        base_rot = 0 if sgn_along > 0 else 180
        inward = -1 if wall == "N" else 1
        sw = inward if d["swing"] == "in" else -inward
        rot = base_rot + (open_deg * sw * sgn_along)
        leaf = leaf.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rot).translate((hinge, y_face, 0))
    else:
        x_face = 0.0 if wall == "W" else ROOM_W
        leaf = box(-leaf_t / 2, 0, 0, leaf_t / 2, leaf_w, 84 * IN)
        base_rot = 0 if sgn_along > 0 else 180
        inward = 1 if wall == "W" else -1
        sw = inward if d["swing"] == "in" else -inward
        rot = base_rot - (open_deg * sw * sgn_along)
        leaf = leaf.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rot).translate((x_face, hinge, 0))
    return Part(f"door {name}", leaf, C_DOOR, "room")


def room_parts(roof_cut: float = ROOM_H) -> list[Part]:
    h = roof_cut
    op = lambda w: [(DOORS[k]["a"] * FT, DOORS[k]["b"] * FT) for k in DOORS if DOORS[k]["wall"] == w]
    P = [
        Part("floor", box(-T_CMU, -T_CMU, -100, ROOM_W + T_PART, ROOM_D + T_CMU, 0), C_FLOOR, "room"),
        Part("wall N (CMU)", _wall_with_openings("N", op("N"), T_CMU, h), C_CMU, "room"),
        Part("wall S (CMU)", _wall_with_openings("S", op("S"), T_CMU, h), C_CMU, "room"),
        Part("wall W (CMU)", _wall_with_openings("W", op("W"), T_CMU, h), C_CMU, "room"),
        Part("wall E (partition)", _wall_with_openings("E", op("E"), T_PART, h), C_WALL, "room"),
        Part("column", box(COL_X0, COL_Y0, 0, COL_X1, COL_Y1, h), C_COL, "room"),
        Part("closet 158", box(0, 0, 0, C158_X1 + T_PART, C158_Y1 + T_PART, h), C_WALL, "room"),
    ]
    for i, (x0, x1, y0, y1) in enumerate(CHASES):
        P.append(Part(f"chase {i}", box(x0, y0, 0, x1, y1, h), C_WALL, "room"))
    for k in DOORS:
        P.append(door_leaf(k, 0.0))
    return P


# --------------------------------------------------------------------------------------------
# Booth and what is in it (approximate, from the stream-camera frame)
# --------------------------------------------------------------------------------------------
def booth_parts() -> list[Part]:
    h = BOOTH_H
    d0, d1 = BOOTH_DOOR
    south = box(0, BOOTH_Y0, 0, BOOTH_X1, BOOTH_Y0 + T_BOOTH, h).cut(box(d0, BOOTH_Y0 - 1, -1, d1, BOOTH_Y0 + T_BOOTH + 1, 7 * FT))
    east = box(BOOTH_X1, BOOTH_Y0, 0, BOOTH_X1 + T_BOOTH, ROOM_D, h)
    P = [
        Part("booth wall S (sheet metal)", south, C_BOOTH, "booth"),
        Part("booth wall E (sheet metal)", east, C_BOOTH, "booth"),
    ]
    # strip curtain: 8 in strips with 2 in overlap
    n = int((d1 - d0) // (6 * IN))
    strips = None
    for i in range(n + 1):
        x = d0 + i * (d1 - d0) / (n + 1)
        s = box(x, BOOTH_Y0 + 0.5 * IN, 0.5 * IN, x + 8 * IN, BOOTH_Y0 + 0.6 * IN, 7 * FT)
        strips = s if strips is None else strips.fuse(s)
    P.append(Part("strip curtain", strips, C_CURTAIN, "booth", opacity=0.35))
    return P


def equipment_parts() -> list[Part]:
    P = []
    yN = ROOM_D
    # rePowder atomizer: blue cabinet against the north wall, chamber and furnace in front
    ax0, ax1 = 6.5 * FT, 6.5 * FT + 40 * IN
    P.append(Part("atomizer cabinet", box(ax0, yN - 28 * IN, 0, ax1, yN, 63 * IN), C_BLUE, "equipment"))
    cx = (ax0 + ax1) / 2 - 4 * IN
    P.append(Part("atomizer chamber", box(cx - 9 * IN, yN - 28 * IN - 15 * IN, 14 * IN, cx + 9 * IN, yN - 28 * IN, 44 * IN), C_STEEL, "equipment"))
    P.append(Part("atomizer furnace", cyl(8 * IN, 13 * IN, cx, yN - 28 * IN - 8 * IN, 44 * IN), C_ALU, "equipment"))
    P.append(Part("atomizer HMI", box(ax1 - 2 * IN, yN - 34 * IN, 40 * IN, ax1 + 1 * IN, yN - 20 * IN, 58 * IN), C_BLACK, "equipment"))
    # argon cylinder and its two-cylinder wall rack
    P.append(Part("argon cylinder", cyl(4.6 * IN, 55 * IN, 11.0 * FT, yN - 6 * IN, 0), (0.12, 0.16, 0.35), "equipment"))
    for z in (30 * IN, 48 * IN):
        P.append(Part(f"cylinder rack {z:.0f}", box(10.2 * FT, yN - 3 * IN, z, 12.6 * FT, yN, z + 3 * IN), C_BLACK, "equipment"))
    # induction module, bench, desk, vacuum, bin, chair
    P.append(Part("induction module", box(4.3 * FT, 27.4 * FT, 0, 6.3 * FT, 29.4 * FT, 30 * IN), (0.25, 0.26, 0.28), "equipment"))
    P.append(Part("white bench", box(1.0 * FT, BOOTH_Y0 + 3 * IN, 28 * IN, 7.0 * FT, BOOTH_Y0 + 33 * IN, 30 * IN), (0.95, 0.95, 0.95), "equipment"))
    for x in (1.2 * FT, 6.7 * FT):
        for y in (BOOTH_Y0 + 5 * IN, BOOTH_Y0 + 29 * IN):
            P.append(Part("bench leg", box(x, y, 0, x + 1.5 * IN, y + 1.5 * IN, 28 * IN), (0.9, 0.9, 0.9), "equipment"))
    P.append(Part("sit-stand desk", box(2 * IN, 26.2 * FT, 28 * IN, 32 * IN, 31.2 * FT, 30 * IN), (0.87, 0.75, 0.55), "equipment"))
    P.append(Part("ATEX vacuum", cyl(11 * IN, 40 * IN, 1.4 * FT, 24.6 * FT, 0), C_STEEL, "equipment"))
    P.append(Part("bin", cyl(10 * IN, 30 * IN, 12.4 * FT, 27.3 * FT, 0), C_BLACK, "equipment"))
    P.append(Part("chair", box(11.6 * FT, 23.6 * FT, 17 * IN, 13.2 * FT, 25.0 * FT, 20 * IN), C_RED, "equipment"))
    P.append(Part("mat", box(6.9 * FT, 26.2 * FT, 0, 9.9 * FT, 29.0 * FT, 0.4 * IN), (0.45, 0.46, 0.48), "equipment"))
    # existing BYU CO2 extinguisher by door 154-1 (inferred position)
    x, y = CO2_POS
    P.append(Part("existing CO2 extinguisher", cyl(3.6 * IN, 24 * IN, x + 4.6 * IN, y, 20 * IN), C_RED, "equipment"))
    P.append(Part("existing CO2 horn", cyl(2.0 * IN, 10 * IN, x + 4.6 * IN, y + 6 * IN, 18 * IN), C_BLACK, "equipment"))
    return P


# --------------------------------------------------------------------------------------------
# Extinguisher, bracket, fasteners and signs, in a local frame:
# origin at the wall face on the hook's centreline, at floor level; +u out of the wall,
# +v along the wall (to the right when facing it), z up. place() maps that onto the column face.
# --------------------------------------------------------------------------------------------
def b570_local() -> dict[str, cq.Shape]:
    """Amerex B570 standing on its own base, in the local frame of the mounted position."""
    r = B570_BODY_D / 2
    u0 = STANDOFF + r
    z0 = BOTTOM_Z
    zt = z0 + B570_BODY_H                       # top of the dome
    body = cq.Solid.makeCylinder(r, B570_BODY_H - r * 0.6, cq.Vector(u0, 0, z0))
    dome = cq.Solid.makeSphere(r, cq.Vector(u0, 0, z0 + B570_BODY_H - r * 0.6), angleDegrees1=0, angleDegrees2=90)
    body = body.fuse(dome.scale(1.0) if False else dome)
    neck = cq.Solid.makeCylinder(0.8 * IN, HOOK_Z - zt + 1.0 * IN, cq.Vector(u0, 0, zt - 1.0 * IN))
    flange = cq.Solid.makeCylinder(1.2 * IN, 0.4 * IN, cq.Vector(u0, 0, HOOK_Z))
    valve = cq.Solid.makeCylinder(0.8 * IN, 3.0 * IN, cq.Vector(u0, 0, HOOK_Z + 0.4 * IN))
    collar = neck.fuse(flange)
    # carry handle and squeeze lever, toward the room
    handle = box(u0 - 0.6 * IN, -0.5 * IN, HOOK_Z + 3.4 * IN, u0 + 5.0 * IN, 0.5 * IN, HOOK_Z + 3.9 * IN)
    lever = box(u0 - 0.6 * IN, -0.45 * IN, TOP_Z - 0.5 * IN, u0 + 5.5 * IN, 0.45 * IN, TOP_Z)
    # hose: an arc from the valve down the side, and the soft-flow applicator wand clipped on the side
    hose = None
    v_side = -(B570_W - r) + 1.0 * IN
    pts = []
    for i in range(13):
        t = i / 12
        a = math.pi * t
        pts.append(cq.Vector(u0, v_side * (0.5 - 0.5 * math.cos(a)), HOOK_Z + 1.6 * IN + 5 * IN * math.sin(a) - 4 * IN * t))
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]
        seg = cq.Solid.makeCylinder(0.45 * IN, (q - p).Length, p, (q - p).normalized())
        hose = seg if hose is None else hose.fuse(seg)
    wand_top = pts[-1]
    wand = cq.Solid.makeCylinder(0.55 * IN, 22 * IN, cq.Vector(u0, v_side, z0 + 6 * IN), cq.Vector(0, 0, 1))
    horn = cq.Solid.makeCone(0.6 * IN, 1.6 * IN, 3.5 * IN, cq.Vector(u0, v_side, z0 + 2.5 * IN), cq.Vector(0, 0, 1))
    link = cq.Solid.makeCylinder(0.45 * IN, max(1.0, wand_top.z - (z0 + 28 * IN)), cq.Vector(u0, v_side, z0 + 28 * IN))
    label = box(u0 + r - 0.3 * IN, -2.6 * IN, z0 + 9 * IN, u0 + r + 0.05 * IN, 2.6 * IN, z0 + 19 * IN)
    return {
        "B570 cylinder": body,
        "B570 collar and valve": collar.fuse(valve),
        "B570 handle": handle.fuse(lever),
        "B570 hose": hose.fuse(link),
        "B570 applicator": wand.fuse(horn),
        "B570 label": label,
    }


B570_COLORS = {
    "B570 cylinder": C_YELLOW, "B570 collar and valve": C_ALU, "B570 handle": C_STEEL,
    "B570 hose": C_BLACK, "B570 applicator": C_BLACK, "B570 label": (0.95, 0.95, 0.92),
}


def bracket_local() -> cq.Shape:
    """Amerex wall hook (the red J bracket shipped with the B570): 2 in wide, 0.09 in steel.

    Back plate 2 x 4.5 in below the seat, with a 0.28 in centre hole and two 0.2 in diagonal
    holes. The arm leaves the top of the plate, runs out under the valve's collar flange (a slot
    takes the neck) and turns up in a short lip. Proportions are from the issue photos, not a drawing.
    """
    t, w = 0.09 * IN, 2.0 * IN
    zb = HOOK_PLATE_Z0
    plate = box(0, -w / 2, zb, t, w / 2, HOOK_Z)
    arm = box(0, -w / 2, HOOK_Z - t, HOOK_REACH, w / 2, HOOK_Z)
    # slot in the arm for the neck
    u0 = STANDOFF + B570_BODY_D / 2
    arm = arm.cut(cq.Solid.makeCylinder(0.85 * IN, 1 * IN, cq.Vector(u0, 0, HOOK_Z - 0.5 * IN)))
    arm = arm.cut(box(u0, -0.85 * IN, HOOK_Z - 0.5 * IN, HOOK_REACH + 1, 0.85 * IN, HOOK_Z + 0.5 * IN))
    lip = box(HOOK_REACH - t, -w / 2, HOOK_Z - t, HOOK_REACH, w / 2, HOOK_Z + 0.6 * IN)
    lip = lip.cut(box(HOOK_REACH - 1, -0.85 * IN, HOOK_Z - 1, HOOK_REACH + 1, 0.85 * IN, HOOK_Z + 1 * IN))
    s = plate.fuse(arm).fuse(lip)
    for (v, z, d) in [(0, zb + 2.2 * IN, 0.28 * IN), (-0.6 * IN, zb + 3.5 * IN, 0.2 * IN), (0.6 * IN, zb + 0.9 * IN, 0.2 * IN)]:
        s = s.cut(cq.Solid.makeCylinder(d / 2, 1 * IN, cq.Vector(-0.5 * IN, v, z), cq.Vector(1, 0, 0)))
    return s


def bracket_holes_local() -> list[tuple[float, float, float]]:
    """(v, z, diameter) of the three holes in the hook's back plate."""
    zb = HOOK_PLATE_Z0
    return [(0, zb + 2.2 * IN, 0.25 * IN), (-0.6 * IN, zb + 3.5 * IN, 0.1875 * IN), (0.6 * IN, zb + 0.9 * IN, 0.1875 * IN)]


def screw_local(v, z, d, length=1.75 * IN, driven=1.0) -> cq.Shape:
    """A hex-washer-head concrete screw (Tapcon-style). driven=0 sits out of the hole, 1 is seated."""
    out = (1 - driven) * length
    head = cq.Solid.makeCylinder(d * 1.1, 0.16 * IN, cq.Vector(0.09 * IN + out, v, z), cq.Vector(1, 0, 0))
    shank = cq.Solid.makeCylinder(d / 2, length, cq.Vector(0.09 * IN + out - length, v, z), cq.Vector(1, 0, 0))
    return head.fuse(shank)


def sign_local(z_bottom=60 * IN, w=7 * IN, h=10 * IN) -> cq.Shape:
    """Flat 'CLASS D' sign on the column face above the extinguisher (rigid plastic, 0.06 in)."""
    return box(0.02 * IN, -w / 2, z_bottom, 0.08 * IN, w / 2, z_bottom + h)


# Fabricated flag-sign bracket: 1/8 in x 1-1/2 in aluminium flat bar, one 90 deg bend.
FLAG = dict(t=0.125 * IN, w=1.5 * IN, wall_leg=3.5 * IN, flag_leg=11.0 * IN, bend_r=0.19 * IN,
            wall_holes=[1.25 * IN, 2.75 * IN], sign_holes=[3.0 * IN, 10.0 * IN], hole_d=0.201 * IN)


def flag_bracket_local(z0=80 * IN) -> cq.Shape:
    """L bracket: the wall leg is screwed to the column's east face, the flag leg sticks out east.

    Holes: two #7 (0.201 in) in the wall leg for 3/16 in concrete screws, two in the flag leg for
    #10-24 screws through a double-sided 7 x 10 in sign. Flat length = legs - 2t + bend
    allowance; see README for the flat pattern.
    """
    t, w, a, b = FLAG["t"], FLAG["w"], FLAG["wall_leg"], FLAG["flag_leg"]
    wall_leg = box(0, -a, z0, t, 0, z0 + w)                 # runs along -v on the face
    flag_leg = box(0, -t, z0, b, 0, z0 + w)                 # sticks out along +u
    s = wall_leg.fuse(flag_leg)
    for hv in FLAG["wall_holes"]:
        s = s.cut(cq.Solid.makeCylinder(FLAG["hole_d"] / 2, 1 * IN, cq.Vector(-0.5 * IN, -hv, z0 + w / 2), cq.Vector(1, 0, 0)))
    for hu in FLAG["sign_holes"]:
        s = s.cut(cq.Solid.makeCylinder(FLAG["hole_d"] / 2, 1 * IN, cq.Vector(hu, -0.5 * IN, z0 + w / 2), cq.Vector(0, 1, 0)))
    return s


def flag_sign_local(z0=80 * IN) -> cq.Shape:
    """Double-sided 7 x 10 in sign hanging below the flag leg (landscape, 10 in along u)."""
    return box(2.0 * IN, -0.25 * IN, z0 - 7 * IN, 12.0 * IN, -0.19 * IN, z0)


def place(shape: cq.Shape, face_x=MOUNT_FACE_X, y=MOUNT_Y) -> cq.Shape:
    """Local (u out of the face, v along it, z) to world, for the column's east face (+x)."""
    # u -> +x, v -> -y would mirror; keep right-handed: u -> +x, v -> +y
    return shape.translate(cq.Vector(face_x, y, 0))


def install_parts(stage: str = "done") -> list[Part]:
    """The finished install on the column's east face."""
    P = []
    for k, s in b570_local().items():
        P.append(Part(k, place(s), B570_COLORS[k], "install"))
    P.append(Part("Amerex wall bracket", place(bracket_local()), C_RED, "install"))
    for (v, z, d) in bracket_holes_local():
        P.append(Part("concrete screw", place(screw_local(v, z, d)), C_STEEL, "install"))
    P.append(Part("CLASS D sign", place(sign_local()), C_YELLOW, "install"))
    P.append(Part("flag bracket (fabricated)", place(flag_bracket_local()), C_ALU, "install"))
    P.append(Part("flag sign", place(flag_sign_local()), C_YELLOW, "install"))
    return P


def scene(include_install=True) -> list[Part]:
    P = room_parts() + booth_parts() + equipment_parts()
    if include_install:
        P += install_parts()
    return P


def export(outdir: str) -> dict:
    """STEP of the whole scene (one solid per part, named) and of the fabricated bracket."""
    import os
    os.makedirs(outdir, exist_ok=True)
    asm = cq.Assembly(name="CB154_class_D_install")
    for i, p in enumerate(scene()):
        asm.add(p.shape, name=f"{i:03d} {p.name}", color=cq.Color(*p.color, p.opacity))
    scene_step = os.path.join(outdir, "cb154_class_d_install.step")
    asm.save(scene_step)
    br = flag_bracket_local(z0=0).translate(cq.Vector(0, 0, 0))
    br_step = os.path.join(outdir, "flag_sign_bracket.step")
    cq.exporters.export(cq.Workplane().add(br), br_step)
    ext = cq.Assembly(name="B570_on_bracket")
    for k, s in b570_local().items():
        ext.add(s, name=k, color=cq.Color(*B570_COLORS[k]))
    ext.add(bracket_local(), name="Amerex wall bracket", color=cq.Color(*C_RED))
    ext_step = os.path.join(outdir, "b570_on_wall_bracket.step")
    ext.save(ext_step)
    return {"scene": scene_step, "flag_bracket": br_step, "extinguisher": ext_step}


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    print(export(out))
    print(f"top {TOP_Z / IN:.1f} in (max {MAX_TOP / IN:.0f}), bottom {BOTTOM_Z / IN:.1f} in (min {MIN_BOTTOM / IN:.0f}), hook {HOOK_Z / IN:.1f} in")
