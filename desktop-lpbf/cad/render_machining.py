"""Chapter 2 of the build animation, the chamber: the through-frame and the floor plate machined the way a 3-axis VMC
with a 4th-axis rotary would cut them (render_build.py calls chapter_chamber).

What changed from the first animation, after a BYU machinist's review:
  * the chamber is a through-frame cut from 5-1/2 in. plate plus a bolted 20 mm floor plate (chamber-construction.md),
    not a block with a 120 mm deep pocket. The frame's core comes out as one slug (waterjet), so most of the metal is not
    milled;
  * the spindle is always vertical. The part is clamped on the VF-4 table, flipped, or indexed about the horizontal A axis
    of an HRT210 rotary between operations. The first animation moved the cutter round a fixed part, which read as 5-axis;
  * every setup shows its fixture and a soda can for scale, and the stock and the finished part are dimensioned.

Round 6 (2026-11-25): the fixtures are the ones the CAM programs were checked with, read from
analysis/machining/freecad_cam.py's FIXTURES (holder_check.py sweeps every tool against them), so the video can't drift
from the programs: frame F-S1 on riser blocks with low-profile edge clamps on its x ends (no end tabs, no toe clamps);
F-S2 on the 312 x 222 dummy-floor plate; F-S3 on an HRT210 on a 2-1/2 in. riser, indexed A0 front, A90 left, A180 back,
A270 right as in the Haas program (freecad_cam.ROT_A); floor P-S1 on parallels with edge clamps, P-S2 on the dummy-floor
plate with an expanding clamp in the port (no centre stud). Each part rests on its fixture as in the CAM's setup frame.
The blanks are the CAM's footprint (12.5 x 9 in.: no tabs to clamp), at the model's thickness.

The cuts are the model's own: lpbf_low.CHAMBER_OPS keeps each part's saw-cut blank and the solid every machining
operation removes, in order (op ids FR-xx and FP-xx), and joints.CUTS the drilled and tapped holes. The last state is
checked against the model's part by volume. The setups (orientation, fixture, index angles) follow
analysis/out/machining/setup_plan.json when it has an "animation" entry, otherwise DEFAULT_PLAN below.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import cadquery as cq
import numpy as np
import pyvista as pv

import render_scale as RS
import render_vmc as V

HERE = pathlib.Path(__file__).resolve().parent
PLAN_JSON = HERE.parent / "analysis" / "out" / "machining" / "setup_plan.json"
sys.path.insert(0, str(HERE.parent / "analysis" / "machining"))
import freecad_cam as FCAM  # noqa: E402  (plain-Python parts only: FIXTURES, ROT_A, the CAM blanks)

STOCK_COL = "#cfd4d9"
DONE_COL = "#b9c0c7"
FIX_COL = "#6f777e"

# The plan (the chamber study's setups F-S0..F-S3 and P-S0..P-S2, setup_plan.json). rots turn the part (model coordinates)
# so the setup's face is up; "fc" names the freecad_cam setup whose FIXTURES hold it ("jet": waterjet slats). On the rotary,
# rots put the part in its A0 orientation (front up, freecad_cam.ROT_A[0]) and index lists (A angle, ops) about +x. Op keys:
# FR-xx / FP-xx (lpbf_low.CHAMBER_OPS), with a suffix + / - for the half at x > 0 or x < 0, and < / > for the half below
# or above MID_Z; J:<key> for the joints.CUTS holes of that joint; J:* for every joint cut not used yet.
DEFAULT_PLAN = {
    "frame": [
        dict(on="jet", rots=[], ops=["FR-02"],
             title="F-S0, waterjet: a Ø12 start hole, then the core cut out of the 12.5 x 9 x 5.5 in. blank in one piece"),
        dict(on="table", fc="frame_B", rots=[("x", 180)], ops=["FR-01<", "FR-04", "FR-05", "J:floor", "J:floor_dowels"],
             title="F-S1, VF-4, bottom up: four riser blocks, four low-profile edge clamps on the x ends (no tabs); face, "
                   "lower half of the profile, opening, rebate, floor-screw and dowel holes"),
        dict(on="table", fc="frame_A", rots=[], ops=["FR-01>", "FR-03", "FR-06", "J:lid"],
             title="F-S2, VF-4, top up: the frame pulled down onto the 312 x 222 dummy-floor plate by its own 18 floor "
                   "screws; face, profile, opening, lid gland and inserts"),
        dict(on="rotary", fc="frame_C0", rots=[("y", 90), ("x", -90)],
             index=[(0, ["FR-07"]), (90, ["FR-10-", "FR-13-"]),
                    (180, ["FR-08", "FR-09", "J:plenum_in", "J:plenum_in_pins", "J:rail"]),
                    (270, ["FR-10+", "FR-11", "FR-12", "FR-13+", "J:vac_port", "J:vac_port_pins", "J:bearing_cap",
                           "J:bearing_cap_pins", "J:*"])],
             title="F-S3, VF-4 + HRT210: the dummy-floor plate on the platter, the frame's bottom on it; one clamping, "
                   "four walls (A0 front, A90 left, A180 back, A270 right)"),
    ],
    "floor": [
        dict(on="table", fc="floor_A", rots=[], ops=["FP-01>", "FP-02", "FP-03", "FP-04", "FP-05", "FP-06", "J:floor_dowels"],
             title="P-S1, VF-4, top up: 12.5 x 9 x 1 in. blank on parallels, four edge clamps on the x ends; face, the 4 mm "
                   "pad, the outline to z -12, O-ring gland, Ø96 H7 port, slots"),
        dict(on="table", fc="floor_B", rots=[("x", 180)],
             ops=["FP-01<", "J:floor", "FP-07", "J:module_flange", "J:plenum_out", "J:funnel", "J:zmount", "J:legs", "J:*"],
             title="P-S2, VF-4, bottom up: on the dummy-floor plate, two pins and an expanding clamp in the port; face to "
                   "20 mm, the rest of the profile with the U-notches, every under-floor hole"),
    ],
}
# the profile's split between the two flat setups: the frame meets at mid-height (set from lpbf_low at run time); the floor
# plate's top setup cuts the outline to z -12 (freecad_cam.py: the edge clamps sit under z -15)
MID_Z = {"frame": None, "floor": -12.0}
CAM_BLANK = {"frame": FCAM.FRAME_BLANK, "floor": FCAM.FLOOR_BLANK}   # (L, W, z0, z1): the footprint the programs cut
SUPPORTS = ("riser block", "parallel", "dummy-floor plate", "fixture plate")
FIX_COLS = {"riser block": "#8e979f", "parallel": "#8e979f", "edge clamp": "#2f5f8a", "dummy-floor plate": FIX_COL,
            "fixture plate": FIX_COL, "port ID clamp": "#3a3f45", "HRT210 platter": V.COL["platter"],
            "HRT210 housing": V.COL["rotary"], "HRT210 motor box": V.COL["rotary"], "2-1/2 in. riser": "#3e454c"}


# ---------------------------------------------------------------------------------------------------- geometry helpers
def _R(rots):
    R = np.eye(3)
    for ax, deg in rots:
        a = math.radians(deg)
        c, s = math.cos(a), math.sin(a)
        Rk = {"x": [[1, 0, 0], [0, c, -s], [0, s, c]], "y": [[c, 0, s], [0, 1, 0], [-s, 0, c]], "z": [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[ax]
        R = np.array(Rk) @ R
    return R


def xform(shape, rots, t=(0.0, 0.0, 0.0)):
    """cq shape rotated about the origin by rots ([(axis, deg)], in order), then moved by t."""
    for ax, deg in rots:
        shape = shape.rotate(cq.Vector(0, 0, 0), cq.Vector(*{"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[ax]), deg)
    return shape.translate(cq.Vector(*map(float, t)))


def about_a(shape, deg, centre):
    """cq shape turned deg about the A axis (+x through centre)."""
    c = cq.Vector(*map(float, centre))
    return shape.rotate(c, c + cq.Vector(1, 0, 0), deg)


def M4(R, t=(0.0, 0.0, 0.0)):
    m = np.eye(4)
    m[:3, :3] = R
    m[:3, 3] = t
    return m


def bb(shape):
    b = shape.BoundingBox()
    return np.array([b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax])


def split_x(shape, side):
    """The half of a cut solid on one side of x = 0 (side '+' or '-'): one wall of a cut that goes through both."""
    big = 2000.0
    box = cq.Solid.makeBox(big, 2 * big, 2 * big, cq.Vector(0.0 if side == "+" else -big, -big, -big))
    return shape.intersect(box)


def cam_blank(part, blank):
    """the model's saw-cut blank trimmed to the footprint the CAM programs cut (freecad_cam's 317.5 x 228.6: no end tabs,
    since the edge clamps hold the x-end faces), at the model's thickness"""
    L, W = CAM_BLANK[part][0], CAM_BLANK[part][1]
    big = 2000.0
    return blank.intersect(cq.Solid.makeBox(L, W, 2 * big, cq.Vector(-L / 2, -W / 2, -big)))


def op_tools(RB, part, key):
    """The removed solid for an op key: 'FR-07' (CHAMBER_OPS), 'FR-10+' (its +x half), 'J:lid' (joints.CUTS of that joint on this
    part), 'J:*+x' / 'J:*-x' (every remaining joint cut whose centre is on that side), 'J:*' (every remaining joint cut)."""
    M, J = RB.M, RB.J
    name = {"frame": "Process chamber body", "floor": "Chamber floor plate"}[part]
    if key.startswith("J:"):
        k = key[2:]
        cuts = [(kk, t) for kk, t in J.CUTS.get(name, [])]
        if k == "*" or k.startswith("*"):
            return None, cuts                        # resolved by the caller (needs to know what is already used)
        return [t for kk, t in cuts if kk == k], None
    suf = key[-1] if key[-1] in "+-<>" else None
    oid = key[:-1] if suf else key
    if part == "frame" and oid == "FR-02":          # the waterjet cuts through the whole blank, so the slug lifts out
        FR, P = M.FRAME, M.P
        co, ix, iy = FR["core_off"], P["ix"], P["iy"]
        return [M.rbox(-ix + co, ix - co, -iy + co, iy - co, -200.0, 300.0, FR["r_in"] - co)], None
    for o, label, solid in M.CHAMBER_OPS[part]["ops"]:
        if o == oid:
            if suf in ("+", "-"):
                return [split_x(solid, suf)], None
            if suf in ("<", ">"):
                zm = MID_Z[part] if MID_Z[part] is not None else (-M.FRAME["skirt"] + M.P["lid_z0"]) / 2
                big = 2000.0
                box = cq.Solid.makeBox(2 * big, 2 * big, big, cq.Vector(-big, -big, zm - big if suf == "<" else zm))
                return [solid.intersect(box)], None
            return [solid], None
    return [], None


def op_label(RB, part, key):
    if key.startswith("J:"):
        return {"lid": "drill and STI-tap the 20 lid-screw holes for M5 helical inserts", "floor": "18 tapped M4 holes in the skirt for the floor screws",
                "floor_dowels": "Ø6 dowel holes", "rail": "4 recoater-rail holes tapped through the back wall from outside (plugged later)",
                "plenum_in": "7 inlet-plenum insert holes round the slot", "plenum_in_pins": "2 Ø3 dowel-pin holes for the inlet plenum",
                "vac_port": "KF-25 adapter insert holes", "vac_port_pins": "2 Ø3 dowel-pin holes for the KF-25 adapter",
                "bearing_cap": "bearing-cap insert holes", "bearing_cap_pins": "2 Ø3 dowel-pin holes for the bearing cap",
                "module_flange": "module-screw inserts and dowel holes", "plenum_out": "outlet-plenum insert holes",
                "funnel": "overflow-funnel insert holes", "zmount": "Z-flange insert holes", "legs": "leg insert holes",
                "zp_posts": "M6 insert holes for the zero-point clamp posts"}.get(key[2:], "drill, tap and insert the remaining holes")
    oid = key.rstrip("+-<>")
    for o, label, solid in RB.M.CHAMBER_OPS[part]["ops"]:
        if o == oid:
            return f"{o}: {label}" + (" (this wall)" if key[-1] in "+-" else " (this side)" if key[-1] in "<>" else "")
    return key


# ---------------------------------------------------------------------------------------------------- fixtures
def fixture_meshes(name, shift, skip=(), only=None):
    """[(mesh, colour)] of freecad_cam.FIXTURES[name] (that setup's frame) moved by shift. Kinds: box (x0, x1, y0, y1, z0,
    z1); vcyl (cx, cy, r, z0, z1); ycyl (cx, cz, r, y0, y1); xcyl (cy, cz, r, x0, x1)."""
    sx, sy, sz = map(float, shift)
    out = []
    for nm, kind, p in FCAM.FIXTURES[name][1]:
        if nm in skip or (only is not None and nm not in only):
            continue
        if kind == "box":
            x0, x1, y0, y1, z0, z1 = p
            m = pv.Box((x0 + sx, x1 + sx, y0 + sy, y1 + sy, z0 + sz, z1 + sz))
        elif kind == "vcyl":
            cx, cy, r, z0, z1 = p
            m = pv.Cylinder(center=(cx + sx, cy + sy, (z0 + z1) / 2 + sz), direction=(0, 0, 1), radius=r, height=z1 - z0, resolution=48)
        elif kind == "ycyl":
            cx, cz, r, y0, y1 = p
            m = pv.Cylinder(center=(cx + sx, (y0 + y1) / 2 + sy, cz + sz), direction=(0, 1, 0), radius=r, height=y1 - y0, resolution=48)
        elif kind == "xcyl":
            cy, cz, r, x0, x1 = p
            m = pv.Cylinder(center=((x0 + x1) / 2 + sx, cy + sy, cz + sz), direction=(1, 0, 0), radius=r, height=x1 - x0, resolution=64)
        else:
            raise ValueError(kind)
        out.append((m, FIX_COLS.get(nm, FIX_COL)))
    return out


def rest_z(name):
    """setup-frame z of the face the part rests on: the top of the supports under it (risers, parallels, plates)"""
    return max(p[5] for nm, kind, p in FCAM.FIXTURES[name][1] if nm in SUPPORTS and kind == "box")


def jet_bed(cx, cy, w=900.0, d=700.0):
    slats = [pv.Box((cx - w / 2, cx + w / 2, y - 1.5, y + 1.5, -60, 0)) for y in np.arange(cy - d / 2, cy + d / 2, 50.0)]
    tank = pv.Box((cx - w / 2 - 30, cx + w / 2 + 30, cy - d / 2 - 30, cy + d / 2 + 30, -260, -60))
    water = pv.Box((cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, -64, -40))
    return [(slats[0].merge(slats[1:]), "#6f777e"), (tank, "#3e454c"), (water, "#7fb5d8")]


def jet_head():
    return [(pv.Cylinder(center=(0, 0, 70), direction=(0, 0, 1), radius=9, height=100), "#3a3f45"),
            (pv.Cone(center=(0, 0, 12), direction=(0, 0, -1), height=24, radius=8), "#9aa3ab"),
            (pv.Line((0, 0, 0), (0, 0, -40)).tube(radius=0.9), "#7fd3ff")]


# ---------------------------------------------------------------------------------------------------- the chapter
def load_plan():
    try:
        d = json.loads(PLAN_JSON.read_text())
        if isinstance(d, dict) and d.get("animation"):
            return d["animation"]
    except Exception:  # noqa: BLE001
        pass
    return DEFAULT_PLAN


def chapter_chamber(st, RB):
    """Frame then floor plate, setup by setup. RB: the render_build module (its helpers and the model)."""
    M = RB.M
    plan = load_plan()
    nf, tess = RB.nf, RB.tess
    cap = "2  Machining the chamber: a through-frame from 5.5 in. plate and a 20 mm floor plate (spindle always vertical)"
    table_top = 0.0
    st.add_multi("vmc-table", V.table(table_top))
    results = {}
    for part in ("frame", "floor"):
        info = M.CHAMBER_OPS[part]
        final = st.parts[st.find("Process chamber body" if part == "frame" else "Chamber floor plate")[0]].shape
        state = cam_blank(part, info["blank"])
        used_j = set()
        # stock first, with dimensions and a can
        sb = bb(state)
        off = np.array([0.0, 0.0, table_top + 25.4 - sb[4]])
        st.add("ch-part", tess(state.translate(cq.Vector(*off))), STOCK_COL, edges=True)
        b0 = sb + np.repeat(off, 2)
        RS.add_dims(st, "ch-dims", RS.box_dims(b0, pad=60.0))
        can = RS.soda_can((b0[1] + 90.0, b0[3] - 40.0, table_top))
        RS.add_refs(st, "ch-can", can)
        bx, by, bz = (sb[1] - sb[0]) / 25.4, (sb[3] - sb[2]) / 25.4, (sb[5] - sb[4]) / 25.4
        st.caption(cap, f"{'Frame' if part == 'frame' else 'Floor plate'} blank: {bx:.1f} x {by:.1f} x {bz:.2f} in. 6061-T651, saw-cut "
                   f"({state.Volume() * 2.7e-6:.1f} kg; no clamping tabs: edge clamps hold its ends); a 12 oz can for scale")
        for f in range(nf(10)):
            st.cam(tuple(((b0[0::2] + b0[1::2]) / 2)), 1100 if part == "frame" else 950, -32 + 1.2 * f, 30)
            st.shot()
        RS.remove_dims(st, "ch-dims")
        for su in plan[part]:
            R = su.get("rots", [])
            if su["on"] == "rotary":
                state, used_j = _rotary_setup(st, RB, part, su, state, used_j, cap)
                continue
            for key in su["ops"]:
                tools, cuts = op_tools(RB, part, key)
                if cuts is not None:              # J:* style: every joint cut not used yet
                    tools = [t for kk, t in cuts if kk not in used_j]
                    used_j |= {kk for kk, _ in cuts}
                elif key.startswith("J:"):
                    used_j.add(key[2:])
                if not tools:
                    continue
                after = state.cut(*tools)
                _animate_op(st, RB, su, R, state, after, key, part, cap)
                state = after
        # check: the last state is the model's part
        try:
            dv = abs(state.Volume() - final.Volume()) / final.Volume()
        except Exception:  # noqa: BLE001
            dv = float("nan")
        results[part] = dv
        print(f"chamber {part}: ops reproduce the model's part to {100 * dv:.3f} % in volume")
        fb = bb(final)
        offf = np.array([0.0, 0.0, table_top + 25.4 - fb[4]])
        st.add("ch-part", tess(final.translate(cq.Vector(*offf))), DONE_COL, edges=True)
        st.clear_extra("fx-")
        b1 = fb + np.repeat(offf, 2)
        RS.add_dims(st, "ch-dims", RS.box_dims(b1, pad=60.0))
        st.caption(cap, f"{'Frame' if part == 'frame' else 'Floor plate'} done: {final.Volume() * 2.7e-6:.2f} kg"
                   + (" (the core slug is reusable stock)" if part == "frame" else ""))
        for f in range(nf(10)):
            st.cam(tuple(((b1[0::2] + b1[1::2]) / 2)), 950, -30 + 4 * f, 28)
            st.shot()
        RS.remove_dims(st, "ch-dims")
        st.remove("ch-part")
        RS.remove_refs(st, "ch-can")
    st.remove("vmc-table")
    return results


def _animate_op(st, RB, su, R, before, after, key, part, cap):
    """One operation in a table, flip or jet setup: the part rotated by R and sitting on its fixture; the tool from above.
    On the table the part sits as in freecad_cam's setup frame (centred on the model origin in x and y), on the top of
    its supports, with FIXTURES[su['fc']] drawn round it and the table under them."""
    nf = RB.nf
    bm = xform(before, R)
    b = bb(bm)
    st.clear_extra("fx-")
    if su["on"] == "jet":
        t = np.array([-(b[0] + b[1]) / 2, -(b[2] + b[3]) / 2, 0.5 - b[4]])
        st.show_extra("vmc-table", False)
        st.add_multi("fx-jet", jet_bed(0.0, 0.0))
    else:
        table_z = FCAM.FIXTURES[su["fc"]][0]
        lift = np.array([0.0, 0.0, -table_z])                     # setup frame -> scene (table top at z 0)
        t = lift + np.array([0.0, 0.0, rest_z(su["fc"]) - b[4]])   # the part's lowest face on its supports
        st.show_extra("vmc-table", True)
        st.add_multi("fx-hold", fixture_meshes(su["fc"], lift))
    bm = xform(before, R, t)
    am = xform(after, R, t)
    b = bb(bm)
    c = (b[0::2] + b[1::2]) / 2
    tool = "jet" if su["on"] == "jet" else ("drill" if key.startswith("J:") else "mill")

    def cam(u):
        st.cam(tuple(c + np.array([0, 0, 30.0])), 900, -34 + 14 * u, 34)
    RB.machine_op(st, "ch-part", bm, am, "-z", tool, nf(12), STOCK_COL, cap, su["title"] + " | " + op_label(RB, part, key), cam)
    if key == "FR-02":       # the slug lifts out in one piece
        slug = bm.cut(am)
        sbb = bb(slug)
        st.add("fx-slug", RB.tess(slug), STOCK_COL, edges=True)
        for f in range(nf(8)):
            u = RB.ease((f + 1) / nf(8))
            st.move("fx-slug", RB.T((0, -330.0 * u, 160.0 * math.sin(math.pi * u) + 0.0)))
            st.caption(cap, f"The core lifts out as one {sbb[1] - sbb[0]:.0f} x {sbb[3] - sbb[2]:.0f} x {sbb[5] - sbb[4]:.0f} mm slug "
                       f"(~{slug.Volume() * 2.7e-6:.0f} kg of 6061): reusable stock, not chips")
            cam(1.0)
            st.shot()
    st.show_extra("vmc-table", True)


def _rotary_setup(st, RB, part, su, state, used_j, cap):
    """The frame on the HRT210, as freecad_cam programs and checks it: the part turned by su['rots'] into its A0
    orientation (checked against freecad_cam.ROT_A[0]), in the machine frame of FIXTURES[su['fc']] (A along +x through the
    origin, the table at FIXTURES' table z); the platter and the dummy-floor plate turn with it, the housing, motor box and
    riser stay put. Then indexed to each angle in su['index'] for its operations. Returns the new state and the joint cuts
    used."""
    nf, ease, tess = RB.nf, RB.ease, RB.tess
    R0 = su.get("rots", [])
    if not np.allclose(_R(R0), np.array(FCAM.ROT_A[0], float), atol=1e-9):
        raise ValueError("the rotary setup's rots don't give freecad_cam.ROT_A[0]: %s" % (R0,))
    name = su.get("fc", "frame_C0")
    table_z, pieces, _ = FCAM.FIXTURES[name]
    lift = np.array([0.0, 0.0, -table_z])                          # machine frame -> scene (table top at z 0)
    centre = lift.copy()                                          # the A axis: through the setup origin, along +x
    turn_names = ("HRT210 platter", "dummy-floor plate")
    st.clear_extra("fx-")
    st.add_multi("fx-rotary", fixture_meshes(name, lift, skip=turn_names))
    st.add_multi("fx-turn", fixture_meshes(name, lift, only=turn_names))
    riser = next((p[5] - p[4] for nm, kind, p in pieces if "riser" in nm), 0.0)
    plate = next(p for nm, kind, p in pieces if nm == "dummy-floor plate")
    title = su["title"] + (f" (A {-table_z:.1f} mm above the table on a {riser:.1f} mm riser; the plate "
                           f"{plate[3] - plate[2]:.0f} x {plate[5] - plate[4]:.0f})")
    angle = 0.0
    for ang, keys in su["index"]:
        # index the A axis from the current angle to ang
        n = nf(8)
        for f in range(n):
            a = angle + (ang - angle) * ease((f + 1) / n)
            Mrot = V.rot_about_x(a, centre)
            st.add("ch-part", tess(xform(state, R0, lift)), STOCK_COL, edges=True)
            st.move("ch-part", Mrot)
            st.move("fx-turn", Mrot)
            st.caption(cap, f"{title} | A axis to {ang:.0f} deg")
            st.cam(tuple(centre + np.array([160.0, 0, 20.0])), 1300, 38, 24)
            st.shot()
        angle = ang
        for key in keys:
            tools, cuts = op_tools(RB, part, key)
            if cuts is not None:
                side = key[3:] if key.startswith("J:*") else ""
                cand = [(kk, tt) for kk, tt in cuts if kk not in used_j]
                if side in ("+x", "-x"):
                    sgn = 1 if side == "+x" else -1
                    cand = [(kk, tt) for kk, tt in cand if sgn * (bb(tt)[0] + bb(tt)[1]) / 2 > 120.0]
                tools = [tt for _, tt in cand]
                used_j |= {kk for kk, _ in cand}
            elif key.startswith("J:"):
                used_j.add(key[2:])
            if not tools:
                continue
            after = state.cut(*tools)
            bm, am = about_a(xform(state, R0, lift), ang, centre), about_a(xform(after, R0, lift), ang, centre)
            st.move("ch-part", np.eye(4))
            st.move("fx-turn", V.rot_about_x(ang, centre))
            bk = bb(bm)
            ck = (bk[0::2] + bk[1::2]) / 2

            def cam(u, ck=ck):
                st.cam(tuple(ck + np.array([0, 0, 30.0])), 1100, 34 + 10 * u, 30)
            RB.machine_op(st, "ch-part", bm, am, "-z", "drill" if key.startswith("J:") else "mill", nf(10), STOCK_COL, cap,
                          title + " | " + op_label(RB, part, key), cam)
            state = after
    st.remove("fx-rotary")
    st.remove("fx-turn")
    return state, used_j
