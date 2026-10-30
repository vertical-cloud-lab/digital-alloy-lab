"""Parametric CAD for the atomizer-enclosure accessories in issue #231, sized
and oriented for laser powder bed fusion (LPBF) on an AconityMINI.

    python make_parts.py

writes stl/ and step/ (one file per part), previews/ (renders and plate
layouts) and parts-summary.md (volumes, masses, layer counts, overhang check).

Every part is modelled in its print orientation: +Z is the build direction and
the face at z = 0 goes on the build plate (or on block supports). Dimensions
are in mm. Change a number in the dicts below and rerun to regenerate.
"""

import json
import math
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import shapely  # noqa: E402
import trimesh  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402
from shapely import affinity  # noqa: E402
from shapely.geometry import Point, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

HERE = Path(__file__).resolve().parent

# --- Machine and material -------------------------------------------------
PLATE_D = 140.0  # AconityMINI build plate; the Utah AconityMIDI's is 170
PLATE_MARGIN = 5.0  # keep parts this far in from the plate edge
MAX_Z = 190.0  # lowest published AconityMINI build height (others say 200)
LAYER = 0.030  # typical AlSi10Mg layer thickness, for layer counts only
DENSITY = {"AlSi10Mg": 2.67, "316L": 7.98}  # g/cm^3
OVERHANG_DEG = 45.0  # down-facing surfaces flatter than this need support
FONT = "DejaVu Sans"

# --- SEM stub holder (Ronnie's Onshape draft, "stub holder") --------------
STUB = dict(
    body_w=70.0,  # Variable Studio #body_width
    body_d=35.0,  # Variable Studio #body_heigth
    base_h=18.0,  # Bottom / Extrude 1
    pin_d=3.3,  # Bottom / Sketch 2: pin stubs have 3.2 mm (1/8 in) pins
    pin_depth=15.0,  # Bottom / Extrude 2
    pitch_x=17.5,  # Sketch 2 linear pattern (Onshape has it 0.25 mm off centre; centred here)
    pitch_y=16.0,
    nx=4,
    ny=2,
    taper_h=6.0,  # Bottom / Chamfer 1: 6 mm at 10 deg, the seat the lid locates on
    taper_deg=10.0,
    corner_r=2.0,  # vertical corner radius at the foot of the taper
    lid_wall=2.5,  # Top / Sketch 1 is body + 5 mm
    lid_h=15.0,  # Top / Extrude 1
    lid_top=3.0,  # Top / Extrude 2 leaves 3 mm (12 mm pocket)
    clearance=0.25,  # new: per side, lid pocket over the base taper
    pin_chamfer=0.4,  # new: lead-in on each pin hole
    edge_chamfer=0.8,  # new: outer edges, and the V-groove at the parting line
    label_size=6.0,  # new: engraved position numbers on the skirt
    label_depth=0.5,
)

# --- Brush cup ------------------------------------------------------------
CUP = dict(
    od=64.0,
    wall=1.6,
    h=70.0,
    floor=3.0,
    foot_d=80.0,  # wider foot so brushes leaning on the rim don't tip it
    foot_h=3.0,
    divider=1.4,  # cross divider, 4 cells
    divider_drop=10.0,  # dividers stop this far below the rim
    floor_fillet=3.0,
    rim_r=0.6,
)

# --- Glove box bracket (print a left and a right) -------------------------
GLOVE = dict(
    box_len=240.0,  # 100-count nitrile box, about 240 x 125 x 65-75 mm
    box_depth=76.0,  # inside depth, wall to front lip
    grip=28.0,  # how far each bracket reaches along the box end
    side_t=3.0,
    back_t=4.0,
    front_t=3.0,
    floor_t=3.0,
    back_h=60.0,
    front_h=30.0,
    screw_d=4.5,  # M4 or #8
    csk_d=9.0,  # 90 deg countersink
    screw_z=(41.0, 53.0),  # above the front lip so a screwdriver reaches them
)

# --- IPA bottle holder ----------------------------------------------------
IPA = dict(
    bottle_d=78.0,  # 500 mL wash bottles are about 74-76 mm across
    wall=2.5,
    back_t=4.0,
    floor_t=3.0,
    cup_h=40.0,
    back_h=62.0,
    screw_d=4.5,
    csk_d=9.0,
    screw_z=52.0,  # above the rim
    screw_dx=20.0,
    rim_r=0.8,
)

# --- Lab coat hook --------------------------------------------------------
HOOK = dict(
    width=18.0,  # printed lying on its side, so this is the build height
    plate_t=6.0,
    plate_h=72.0,
    bend_ri=13.0,  # inside radius of the J
    arm_t=6.0,
    tip_h=14.0,
    screw_d=4.5,
    csk_d=9.0,
    screw_v=(46.0, 64.0),
    edge_chamfer=0.8,
)


# --- Helpers ----------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").add(
        cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))
    )


def rrect_wire(w, d, r, z):
    pts = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    wire = cq.Wire.makePolygon([cq.Vector(x, y, z) for x, y in pts], close=True)
    return wire.fillet2D(r, wire.Vertices())


def teardrop(center, axis, d, length):
    """Horizontal hole with a 45 deg roof pointing up the build (+Z), so its
    top is self-supporting instead of sagging."""
    n = cq.Vector(*axis).normalized()
    xdir = cq.Vector(0, 0, 1).cross(n)
    plane = cq.Plane(origin=center, xDir=xdir, normal=n)
    r = d / 2
    k = r / math.sqrt(2)
    hole = cq.Workplane(plane).circle(r).extrude(length / 2, both=True)
    roof = (
        cq.Workplane(plane)
        .polyline([(-k, k), (0, r * math.sqrt(2)), (k, k), (0, 0)])
        .close()
        .extrude(length / 2, both=True)
    )
    return hole.union(roof)


def countersink(face_pt, into, d_head, extra=0.5):
    """90 deg countersink cone whose rim is d_head across at face_pt."""
    n = cq.Vector(*into).normalized()
    big = d_head / 2 + extra
    start = cq.Vector(*face_pt) - n * extra
    return cq.Workplane("XY").add(cq.Solid.makeCone(big, 0, big, start, n))


def try_fillet(wp, selector, r):
    try:
        return wp.edges(selector).fillet(r)
    except Exception as exc:  # OCCT fillets fail on awkward edge sets
        print(f"  (skipped fillet {selector} r={r}: {exc.__class__.__name__})")
        return wp


# --- Parts ------------------------------------------------------------------
def stub_positions():
    p = STUB
    xs = [(i - (p["nx"] - 1) / 2) * p["pitch_x"] for i in range(p["nx"])]
    ys = [(j - (p["ny"] - 1) / 2) * p["pitch_y"] for j in range(p["ny"])]
    return [(x, y) for y in ys for x in xs]  # front row (-y) is 1-4


def stub_dims():
    p = STUB
    inset = p["taper_h"] * math.tan(math.radians(p["taper_deg"]))
    outer_w = p["body_w"] + 2 * p["lid_wall"]
    outer_d = p["body_d"] + 2 * p["lid_wall"]
    ledge_z = p["base_h"] - p["taper_h"]
    return inset, outer_w, outer_d, ledge_z


def stub_base():
    p = STUB
    inset, ow, od, zl = stub_dims()
    r = p["corner_r"]
    c = p["edge_chamfer"]
    # Skirt the lid sits on: a flat stop, so the metal-on-metal taper only
    # centres the lid and can't wedge it.
    skirt = (
        cq.Workplane("XY").rect(ow, od).extrude(zl).edges("|Z").fillet(r + p["lid_wall"])
    )
    skirt = skirt.faces(">Z").chamfer(c).faces("<Z").chamfer(c)
    taper = cq.Workplane("XY").add(
        cq.Solid.makeLoft(
            [
                rrect_wire(p["body_w"], p["body_d"], r, zl),
                rrect_wire(p["body_w"] - 2 * inset, p["body_d"] - 2 * inset, r - inset, p["base_h"]),
            ],
            True,
        )
    )
    taper = try_fillet(taper, ">Z", 0.5)
    base = skirt.union(taper)

    rp = p["pin_d"] / 2
    for x, y in stub_positions():
        pin = cq.Workplane("XY").add(
            cq.Solid.makeCylinder(rp, p["pin_depth"] + 1, cq.Vector(x, y, p["base_h"] - p["pin_depth"]))
        )
        big = rp + p["pin_chamfer"] + 1
        lead = cq.Workplane("XY").add(
            cq.Solid.makeCone(big, 0, big, cq.Vector(x, y, p["base_h"] + 1), cq.Vector(0, 0, -1))
        )
        base = base.cut(pin).cut(lead)

    # Engraved position numbers on the skirt: 1-4 on the front, 5-8 on the back.
    zt = (zl - c) / 2
    for i, (x, y) in enumerate(stub_positions()):
        if y < 0:
            plane = cq.Plane(origin=(x, -od / 2 - 0.1, zt), xDir=(1, 0, 0), normal=(0, -1, 0))
        else:
            plane = cq.Plane(origin=(x, od / 2 + 0.1, zt), xDir=(-1, 0, 0), normal=(0, 1, 0))
        txt = cq.Compound.makeText(
            str(i + 1), p["label_size"], -(p["label_depth"] + 0.1), font=FONT, kind="bold", position=plane
        )
        base = base.cut(txt)
    return base


def stub_lid():
    """Printed upside down: the top of the lid is on the plate and the pocket
    opens upward, so nothing inside needs support."""
    p = STUB
    inset, ow, od, zl = stub_dims()
    r = p["corner_r"]
    c = p["edge_chamfer"]
    cl = p["clearance"]
    lid = cq.Workplane("XY").rect(ow, od).extrude(p["lid_h"]).edges("|Z").fillet(r + p["lid_wall"])
    lid = lid.faces(">Z").chamfer(c).faces("<Z").chamfer(c)
    t = math.tan(math.radians(p["taper_deg"]))
    z_seat = p["lid_h"] - p["taper_h"]
    top = p["lid_h"] + 1.0  # run the cutter past the rim
    w_small, d_small, r_small = p["body_w"] - 2 * inset + 2 * cl, p["body_d"] - 2 * inset + 2 * cl, r - inset + cl
    grow = t * (top - z_seat)
    pocket = cq.Solid.makeLoft(
        [
            rrect_wire(w_small, d_small, r_small, p["lid_top"]),
            rrect_wire(w_small, d_small, r_small, z_seat),
            rrect_wire(w_small + 2 * grow, d_small + 2 * grow, r_small + grow, top),
        ],
        True,
    )
    return lid.cut(cq.Workplane("XY").add(pocket))


def stub_lid_in_place():
    """The lid flipped and seated on the base's skirt, for the fit check."""
    p = STUB
    _, _, _, zl = stub_dims()
    return stub_lid().rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, zl + p["lid_h"]))


def brush_cup():
    p = CUP
    ro = p["od"] / 2
    ri = ro - p["wall"]
    rf = p["foot_d"] / 2
    h = p["h"]
    cup = cq.Workplane("XY").circle(ro).extrude(h)
    foot = cq.Workplane("XY").circle(rf).extrude(p["foot_h"])
    flare = cq.Workplane("XY").add(  # 45 deg, so it builds without support
        cq.Solid.makeCone(rf, ro, rf - ro, cq.Vector(0, 0, p["foot_h"]), cq.Vector(0, 0, 1))
    )
    cup = cup.union(foot).union(flare)
    cavity = (
        cq.Workplane("XY")
        .circle(ri)
        .extrude(h - p["floor"] + 1)
        .faces("<Z")
        .edges()
        .fillet(p["floor_fillet"])
        .translate((0, 0, p["floor"]))
    )
    cup = cup.cut(cavity)
    cup = try_fillet(cup, ">Z", p["rim_r"])
    length = 2 * (ri + 0.6)
    z1 = h - p["divider_drop"]
    for ang in (0, 90):
        div = (
            box(-length / 2, length / 2, -p["divider"] / 2, p["divider"] / 2, p["floor"] - 0.5, z1)
            .edges("|X and >Z")
            .fillet(p["divider"] / 2 - 0.01)
            .rotate((0, 0, 0), (0, 0, 1), ang)
        )
        cup = cup.union(div)
    return cup


def glove_bracket(side="left"):
    p = GLOVE
    x1 = p["side_t"] + p["grip"]
    y1 = p["back_t"] + p["box_depth"] + p["front_t"]
    floor = box(0, x1, 0, y1, 0, p["floor_t"])
    back = box(0, x1, 0, p["back_t"], 0, p["back_h"]).edges("|X and >Z").fillet(p["back_t"] / 2 - 0.01)
    front = box(0, x1, y1 - p["front_t"], y1, 0, p["front_h"]).edges("|X and >Z").fillet(p["front_t"] / 2 - 0.01)
    wall = (
        cq.Workplane("YZ")
        .polyline([(0, 0), (y1, 0), (y1, p["front_h"]), (0, p["back_h"])])
        .close()
        .extrude(p["side_t"])
    )
    br = floor.union(back).union(front).union(wall)
    x = p["side_t"] + p["grip"] / 2
    for z in p["screw_z"]:
        br = br.cut(teardrop((x, p["back_t"] / 2, z), (0, 1, 0), p["screw_d"], p["back_t"] + 2))
        br = br.cut(countersink((x, p["back_t"], z), (0, -1, 0), p["csk_d"]))
    if side == "right":
        br = br.mirror("YZ").translate((x1, 0, 0))
    return br


def ipa_holder():
    p = IPA
    ri = p["bottle_d"] / 2
    ro = ri + p["wall"]
    yc = p["back_t"] + ri
    back = box(-ro, ro, 0, p["back_t"], 0, p["back_h"]).edges("|Y and >Z").fillet(10.0)
    ring = cq.Workplane("XY").add(cq.Solid.makeCylinder(ro, p["cup_h"], cq.Vector(0, yc, 0)))
    cavity = (
        cq.Workplane("XY")
        .circle(ri)
        .extrude(p["cup_h"])
        .faces("<Z")
        .edges()
        .fillet(3.0)
        .translate((0, yc, p["floor_t"]))
    )
    ring = ring.cut(cavity)
    ring = try_fillet(ring, ">Z", p["rim_r"])
    holder = back.union(ring)
    for sx in (-1, 1):
        x = sx * p["screw_dx"]
        holder = holder.cut(teardrop((x, p["back_t"] / 2, p["screw_z"]), (0, 1, 0), p["screw_d"], p["back_t"] + 2))
        holder = holder.cut(countersink((x, p["back_t"], p["screw_z"]), (0, -1, 0), p["csk_d"]))
    return holder


def coat_hook():
    """A J hook drawn in XY and extruded up Z, so it prints lying on its side
    with every wall vertical. Mounted, X points out of the wall and Y is up."""
    p = HOOK
    w = p["width"]
    t = p["plate_t"]
    ri = p["bend_ri"]
    ro = ri + p["arm_t"]
    uc, vc = t + ri, ro  # centre of the bend; the back plate is its inner leg
    plate = box(0, t, vc, p["plate_h"], 0, w).edges("|Z and >Y").fillet(t / 2 - 0.01)
    bend = (
        cq.Workplane("XY").center(uc, vc).circle(ro).circle(ri).extrude(w)
        .intersect(box(uc - ro - 1, uc + ro + 1, vc - ro - 1, vc, -1, w + 1))
    )
    tip = box(uc + ri, uc + ro, vc, vc + p["tip_h"], 0, w).edges("|Z and >Y").fillet(p["arm_t"] / 2 - 0.01)
    hook = plate.union(bend).union(tip)
    c = p["edge_chamfer"]
    hook = hook.faces(">Z").chamfer(c).faces("<Z").chamfer(c)
    for v in p["screw_v"]:
        hook = hook.cut(teardrop((t / 2, v, w / 2), (1, 0, 0), p["screw_d"], t + 2))
        hook = hook.cut(countersink((t, v, w / 2), (-1, 0, 0), p["csk_d"]))
    return hook


# name -> (builder, how many to print, short description)
PARTS = {
    "stub_holder_base": (stub_base, 1, "SEM stub holder base, 8 pin stubs (12.7 mm)"),
    "stub_holder_lid": (stub_lid, 1, "SEM stub holder lid, printed upside down"),
    "coat_hook": (coat_hook, 2, "Lab coat hook, 2 screws, printed on its side"),
    "brush_cup": (brush_cup, 1, "Brush cup with a 4-cell divider"),
    "glove_bracket_left": (lambda: glove_bracket("left"), 1, "Glove box bracket, left"),
    "glove_bracket_right": (lambda: glove_bracket("right"), 1, "Glove box bracket, right"),
    "ipa_bottle_holder": (ipa_holder, 1, "IPA wash bottle holder (78 mm bottle)"),
}


# --- Checks -----------------------------------------------------------------
def overhang_area(mesh, max_deg=OVERHANG_DEG):
    """Area of down-facing surface flatter than max_deg, ignoring the plate face."""
    nz = mesh.face_normals[:, 2]
    zc = mesh.triangles_center[:, 2]
    bad = (nz < -math.cos(math.radians(max_deg)) - 1e-3) & (zc > mesh.bounds[0, 2] + 0.05)
    return float(mesh.area_faces[bad].sum())


def footprint(mesh):
    """XY outline of the part, as a shapely polygon."""
    tris = mesh.triangles[:, :, :2]
    keep = np.abs(mesh.face_normals[:, 2]) > 1e-3
    polys = [Polygon(t) for t in tris[keep]]
    poly = unary_union([q for q in polys if q.area > 1e-6]).buffer(0.05)
    return poly if poly.geom_type == "Polygon" else poly.convex_hull


# --- Plate layout -----------------------------------------------------------
def pack(items, gap=5.0, step=2.5):
    """Lay the parts out on as few AconityMINI plates as possible. Parts go in
    largest first, each at the first free spot under a placement rule; a part
    that fits on no open plate starts a new build. Both rules are tried and
    the layout with fewer builds is kept. Short parts share plates with tall
    ones: plate area is the scarce thing, and a short part adds no layers."""
    from shapely.prepared import prep

    r_use = PLATE_D / 2 - PLATE_MARGIN
    usable = prep(Point(0, 0).buffer(r_use, 256))
    grid = [(x, y) for x in np.arange(-r_use, r_use + 1e-9, step)
            for y in np.arange(-r_use, r_use + 1e-9, step) if math.hypot(x, y) <= r_use]
    rules = {
        "edge": lambda x, y: -math.hypot(x, y) + 1e-3 * (math.atan2(y, x) % (2 * math.pi)),
        "bottom-left": lambda x, y: y + 1e-2 * x,
    }
    best_layout = None
    for rule in rules.values():
        builds = []
        for name, poly in sorted(items, key=lambda it: -it[1].area):
            poly = affinity.translate(poly, -poly.centroid.x, -poly.centroid.y)
            rots = [(a, affinity.rotate(poly, a, origin=(0, 0))) for a in range(0, 360, 15)]
            for b in builds + [[]]:
                taken = prep(unary_union([q.buffer(gap) for _, q, *_ in b])) if b else None
                best = None
                for x, y in sorted(grid, key=lambda g: rule(*g)):
                    if best is not None:
                        break
                    for a, pr in rots:
                        cand = affinity.translate(pr, x, y)
                        if usable.contains(cand) and (taken is None or not taken.intersects(cand)):
                            best = (cand, float(x), float(y), a)
                            break
                if best is not None:
                    if not b:
                        builds.append(b)
                    b.append((name, *best))
                    break
            else:
                raise RuntimeError(f"{name} does not fit on the plate")
        if best_layout is None or len(builds) < len(best_layout):
            best_layout = builds
    return best_layout


# --- Rendering --------------------------------------------------------------
def render(ax, mesh, color=(0.62, 0.66, 0.72)):
    light = np.array([0.4, -0.6, 0.7])
    light /= np.linalg.norm(light)
    shade = 0.45 + 0.55 * np.clip(mesh.face_normals @ light, 0, 1)
    cols = np.clip(np.outer(shade, color), 0, 1)
    pc = Poly3DCollection(mesh.triangles, facecolors=cols, edgecolors="none", linewidths=0)
    ax.add_collection3d(pc)
    lo, hi = mesh.bounds
    ctr = (lo + hi) / 2
    span = (hi - lo).max() / 2
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=28, azim=-60)
    ax.set_axis_off()


def main():
    out_stl = HERE / "stl"
    out_step = HERE / "step"
    out_prev = HERE / "previews"
    for d in (out_stl, out_step, out_prev):
        d.mkdir(exist_ok=True)

    meshes, rows, items, part_of = {}, [], [], {}
    for name, (build, qty, desc) in PARTS.items():
        print("building", name)
        wp = build()
        stl = out_stl / f"{name}.stl"
        cq.exporters.export(wp, str(stl), tolerance=0.01, angularTolerance=0.1)
        cq.exporters.export(wp, str(out_step / f"{name}.step"))
        mesh = trimesh.load(stl)
        meshes[name] = mesh
        lo, hi = mesh.bounds
        r_max = float(np.hypot(mesh.vertices[:, 0] - (lo[0] + hi[0]) / 2, mesh.vertices[:, 1] - (lo[1] + hi[1]) / 2).max())
        rows.append(
            dict(
                name=name, qty=qty, desc=desc,
                size=[round(float(v), 1) for v in (hi - lo)],
                volume_cm3=round(mesh.volume / 1000, 1),
                mass_g={m: round(mesh.volume / 1000 * rho) for m, rho in DENSITY.items()},
                layers=math.ceil((hi[2] - lo[2]) / LAYER),
                watertight=bool(mesh.is_watertight),
                overhang_mm2=round(overhang_area(mesh), 1),
                fits=bool(2 * r_max <= PLATE_D - 2 * PLATE_MARGIN and hi[2] - lo[2] <= MAX_Z),
            )
        )
        outline = footprint(mesh)
        for k in range(qty):
            copy = name if qty == 1 else f"{name}_{k + 1}"
            part_of[copy] = name
            items.append((copy, outline))

        fig = plt.figure(figsize=(4, 4), dpi=150)
        render(fig.add_subplot(projection="3d"), mesh)
        fig.savefig(out_prev / f"{name}.png", bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)

    # Stub holder fit: the lid seated on the skirt must not touch the base.
    base, lid = stub_base(), stub_lid_in_place()
    clash = base.intersect(lid)
    clash_mm3 = sum(s.Volume() for s in clash.solids().vals()) if clash.solids().size() else 0.0
    inset, _, _, zl = stub_dims()
    headroom = (zl + STUB["lid_h"] - STUB["lid_top"]) - STUB["base_h"]
    cq.exporters.export(base.union(lid), str(out_stl / "_stub_holder_assembled.stl"), tolerance=0.02)
    asm = trimesh.load(out_stl / "_stub_holder_assembled.stl")
    fig = plt.figure(figsize=(4, 4), dpi=150)
    render(fig.add_subplot(projection="3d"), asm)
    fig.savefig(out_prev / "stub_holder_assembled.png", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    (out_stl / "_stub_holder_assembled.stl").unlink()

    # Plate layouts, short parts and tall parts in separate builds.
    builds = pack(items)
    layout = []
    for bi, b in enumerate(builds, 1):
        fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=150)
        ax.add_patch(plt.Circle((0, 0), PLATE_D / 2, fc="#eceff3", ec="#5b6573", lw=1.2))
        ax.add_patch(plt.Circle((0, 0), PLATE_D / 2 - PLATE_MARGIN, fc="none", ec="#9aa3ae", lw=0.8, ls="--"))
        height = 0.0
        for name, poly, x, y, rot in b:
            base_name = part_of[name]
            height = max(height, float(meshes[base_name].bounds[1, 2]))
            xs, ys = poly.exterior.xy
            ax.fill(xs, ys, fc="#8fa3bf", ec="#2f3b4c", lw=0.8)
            ax.text(poly.centroid.x, poly.centroid.y, name.replace("_", "\n"), ha="center", va="center", fontsize=5.5)
            layout.append(dict(build=bi, part=base_name, copy=name, x=round(x, 1), y=round(y, 1), rot_deg=rot))
        ax.set_title(f"Build {bi}: {height:.0f} mm tall, {math.ceil(height / LAYER)} layers at 30 µm", fontsize=8)
        ax.set_xlim(-PLATE_D / 2 - 3, PLATE_D / 2 + 3)
        ax.set_ylim(-PLATE_D / 2 - 3, PLATE_D / 2 + 3)
        ax.set_aspect("equal")
        ax.set_xlabel("x (mm)", fontsize=7)
        ax.set_ylabel("y (mm)", fontsize=7)
        ax.tick_params(labelsize=6)
        fig.savefig(out_prev / f"build_{bi}.png", bbox_inches="tight")
        plt.close(fig)
    (HERE / "layout.json").write_text(json.dumps(layout, indent=1) + "\n")

    # Overview of every part.
    fig = plt.figure(figsize=(12, 6.2), dpi=130)
    shown = list(meshes.items()) + [("stub_holder_assembled", asm)]
    for i, (name, mesh) in enumerate(shown):
        ax = fig.add_subplot(2, 4, i + 1, projection="3d")
        render(ax, mesh)
        ax.set_title(name.replace("_", " "), fontsize=9)
    fig.tight_layout()
    fig.savefig(out_prev / "all_parts.png", bbox_inches="tight")
    plt.close(fig)

    lines = [
        "<!-- generated by make_parts.py; do not edit by hand -->",
        "",
        "| Part | Qty | Size X × Y × Z (mm) | Volume (cm³) | AlSi10Mg (g) | 316L (g) | Layers @ 30 µm | Overhang < 45° (mm²) | Watertight | Fits Ø140 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| `{r['name']}` | {r['qty']} | {' × '.join(f'{v:g}' for v in r['size'])} | {r['volume_cm3']} | "
            f"{r['mass_g']['AlSi10Mg']} | {r['mass_g']['316L']} | {r['layers']} | {r['overhang_mm2']} | "
            f"{'yes' if r['watertight'] else 'NO'} | {'yes' if r['fits'] else 'NO'} |"
        )
    lines += [
        "",
        f"Stub holder fit: lid seated on the skirt overlaps the base by {clash_mm3:.3f} mm³; "
        f"{STUB['clearance']} mm clearance per side on the {STUB['taper_deg']:g}° seat; "
        f"{headroom:.1f} mm headroom above the base for stub heads and samples.",
        "",
        "| Build | Part | x (mm) | y (mm) | Rotation (°) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in layout:
        lines.append(f"| {item['build']} | `{item['copy']}` | {item['x']} | {item['y']} | {item['rot_deg']} |")
    (HERE / "parts-summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
