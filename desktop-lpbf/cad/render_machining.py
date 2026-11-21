"""Chapter 2 of the build animation, the chamber: the through-frame and the floor plate machined the way a 3-axis VMC
with a 4th-axis rotary would cut them (render_build.py calls chapter_chamber).

What changed from the first animation, after a BYU machinist's review:
  * the chamber is a through-frame cut from 5 in. plate plus a bolted 20 mm floor plate (chamber-construction.md), not a
    block with a 120 mm deep pocket. The frame's core comes out as one slug (waterjet), so most of the metal is not milled;
  * the spindle is always vertical. The part is clamped on the VF-4 table, flipped, or indexed about the horizontal A axis
    of an HRT210 rotary between operations. The first animation moved the cutter round a fixed part, which read as 5-axis;
  * every setup shows its fixture and a soda can for scale, and the stock and the finished part are dimensioned.

The cuts are the model's own: lpbf_low.CHAMBER_OPS keeps each part's saw-cut blank and the solid every machining
operation removes, in order (op ids FR-xx and FP-xx), and joints.CUTS the drilled and tapped holes. The last state is
checked against the model's part by volume. The setups (orientation, fixture, index angles) follow
analysis/out/machining/setup_plan.json when it has them, otherwise DEFAULT_PLAN below.
"""
from __future__ import annotations

import json
import math
import pathlib

import cadquery as cq
import numpy as np
import pyvista as pv

import render_scale as RS
import render_vmc as V

HERE = pathlib.Path(__file__).resolve().parent
PLAN_JSON = HERE.parent / "analysis" / "out" / "machining" / "setup_plan.json"
STOCK_COL = "#cfd4d9"
DONE_COL = "#b9c0c7"
FIX_COL = "#6f777e"

# The plan, from analysis/out/machining/setup_plan.json (the chamber study's setups F-S0..F-S3 and P-S0..P-S2). rots turn the part
# (model coordinates) so the setup's face is up; "on": jet (waterjet slats), tabs (riser blocks, toe clamps on the blank's 1 in.
# end tabs), plate (held down on a "dummy floor" fixture plate by its own floor screws from below), studs (fixture plate, two
# pins and an M12 stud through the port), rotary (A axis along machine +x; the part's mounting face on the dummy-floor plate on
# the platter; index angles about +x). Op keys: FR-xx / FP-xx (lpbf_low.CHAMBER_OPS), with a suffix + / - for the half at x > 0
# or x < 0, and < / > for the half below or above the part's mid-height; J:<key> for the joints.CUTS holes of that joint.
DEFAULT_PLAN = {
    "frame": [
        dict(on="jet", rots=[], ops=["FR-02"], title="F-S0, waterjet: a Ø12 start hole, then the core cut out of the 15 x 9.5 x 5.5 in. blank in one piece"),
        dict(on="tabs", rots=[("x", 180)], ops=["FR-01<", "FR-04", "FR-05", "J:floor", "J:floor_dowels"],
             title="F-S1, VF-4, bottom up: riser blocks, toe clamps on the end tabs; face, lower half of the profile, opening, rebate, floor-screw holes"),
        dict(on="plate", rots=[], ops=["FR-01>", "FR-03", "FR-06", "J:lid"],
             title="F-S2, VF-4, top up: end tabs sawn off; the frame held down on a dummy-floor plate by its own 18 floor screws; "
                   "face, profile, opening, lid gland and inserts"),
        dict(on="rotary", rots=[("y", 90)], index=[(-90, ["FR-07"]), (0, ["FR-10-", "FR-13-"]), (90, ["FR-08", "FR-09", "J:plenum_in", "J:rail"]),
                                                   (180, ["FR-10+", "FR-11", "FR-12", "FR-13+", "J:vac_port", "J:bearing_cap"])],
             title="F-S3, VF-4 + HRT210: the dummy-floor plate on the platter, the frame's bottom on it; one clamping, four walls"),
    ],
    "floor": [
        dict(on="tabs", rots=[], ops=["FP-01>", "FP-02", "FP-03", "FP-04", "FP-05", "FP-06", "J:floor_dowels"],
             title="P-S1, VF-4, top up: 15 x 9.5 x 1 in. blank on parallels, toe clamps on the end tabs; face, the 4 mm pad, O-ring gland, Ø96 H7 port, slots"),
        dict(on="studs", rots=[("x", 180)], ops=["FP-01<", "J:floor", "FP-07", "J:module_flange", "J:plenum_out", "J:funnel", "J:zmount", "J:legs"],
             title="P-S2, VF-4, bottom up: two pins and an M12 stud through the port; face to 20 mm, profile, U-notches, every under-floor hole"),
    ],
}
MID_Z = {"frame": None, "floor": -10.0}      # frame: set from lpbf_low.FRAME at run time


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
                "plenum_in": "7 inlet-plenum insert holes round the slot", "vac_port": "KF-25 adapter insert holes",
                "bearing_cap": "bearing-cap insert holes", "module_flange": "module-screw inserts and dowel holes",
                "plenum_out": "outlet-plenum insert holes", "funnel": "overflow-funnel insert holes", "zmount": "Z-flange insert holes",
                "legs": "leg insert holes"}.get(key[2:], "drill, tap and insert the remaining holes")
    oid = key.rstrip("+-<>")
    for o, label, solid in RB.M.CHAMBER_OPS[part]["ops"]:
        if o == oid:
            return f"{o}: {label}" + (" (this wall)" if key[-1] in "+-" else " (this side)" if key[-1] in "<>" else "")
    return key


# ---------------------------------------------------------------------------------------------------- fixtures
def parallels_and_clamps(b, z0):
    """Two parallels under the part's footprint b (machine frame) and four toe clamps on its long sides."""
    x0, x1, y0, y1 = b[0], b[1], b[2], b[3]
    h = 25.4
    pieces = [(pv.Box((x0 + 20, x1 - 20, y0 + 15, y0 + 40, z0, z0 + h)), "#8e979f"), (pv.Box((x0 + 20, x1 - 20, y1 - 40, y1 - 15, z0, z0 + h)), "#8e979f")]
    zt = z0 + h
    for x in (x0 + 0.25 * (x1 - x0), x0 + 0.75 * (x1 - x0)):
        for sy in (-1, 1):
            ye = y0 if sy < 0 else y1
            step = pv.Box((x - 18, x + 18, ye + sy * 70, ye + sy * 100, z0, zt + 6))
            bar = pv.Box((x - 13, x + 13, min(ye - sy * 12, ye + sy * 100), max(ye - sy * 12, ye + sy * 100), zt + 6 + (b[5] - b[4]) * 0.0, zt + 22))
            stud = pv.Cylinder(center=(x, ye + sy * 45, (z0 + zt + 40) / 2), direction=(0, 0, 1), radius=6, height=zt + 40 - z0)
            pieces += [(step, "#3e454c"), (stud, "#9aa3ab")]
            pieces.append((bar, "#3a3f45"))
    return pieces, zt


def holding(kind, b):
    """[(mesh, colour)] of what holds the part (bbox b, machine frame, sitting 25.4 mm above the table):
    tabs   four riser blocks under the corners and toe clamps on the blank's end tabs (x ends)
    plate  a 1 in. 'dummy floor' fixture plate under the part (the part is pulled down by its own floor screws from below)
    studs  a fixture plate under the part, and an M12 stud with a Ø104 clamp washer through the Ø96 port"""
    x0, x1, y0, y1, z0, z1 = map(float, b)
    out = []
    if kind == "tabs":
        for x in (x0 + 10, x1 - 50):
            for y in (y0 + 10, y1 - 50):
                out.append((pv.Box((x, x + 40, y, y + 40, 0.0, z0)), "#8e979f"))
        for x in (x0 + 12, x1 - 12):
            for y in (y0 + 0.3 * (y1 - y0), y0 + 0.7 * (y1 - y0)):
                sx = -1 if x < (x0 + x1) / 2 else 1
                out.append((pv.Box((min(x, x + sx * 90), max(x, x + sx * 90), y - 12, y + 12, z1, z1 + 16)), "#3a3f45"))
                out.append((pv.Cylinder(center=(x + sx * 45, y, (z1 + 30) / 2), direction=(0, 0, 1), radius=6, height=z1 + 30), "#9aa3ab"))
                out.append((pv.Box((min(x + sx * 70, x + sx * 100), max(x + sx * 70, x + sx * 100), y - 15, y + 15, 0.0, z1 + 6)), "#3e454c"))
    elif kind in ("plate", "studs"):
        out.append((pv.Box(((x0 + x1) / 2 - 165, (x0 + x1) / 2 + 165, (y0 + y1) / 2 - 120, (y0 + y1) / 2 + 120, 0.0, z0)), "#6f777e"))
        if kind == "studs":
            c = ((x0 + x1) / 2, (y0 + y1) / 2)
            out.append((pv.Cylinder(center=(c[0], c[1], (z0 + z1) / 2 + 20), direction=(0, 0, 1), radius=6, height=z1 - z0 + 40), "#9aa3ab"))
            out.append((pv.Cylinder(center=(c[0], c[1], z1 + 4), direction=(0, 0, 1), radius=52, height=8, resolution=48), "#3a3f45"))
    return out


def clamp_bars_on_top(b, ztop):
    """Toe-clamp bars resting on the part's top face at its long sides (for setups after the profile is cut)."""
    pieces = []
    for x in (b[0] + 0.25 * (b[1] - b[0]), b[0] + 0.75 * (b[1] - b[0])):
        for sy in (-1, 1):
            ye = b[2] if sy < 0 else b[3]
            pieces.append((pv.Box((x - 13, x + 13, min(ye - sy * 10, ye + sy * 80), max(ye - sy * 10, ye + sy * 80), ztop, ztop + 16)), "#3a3f45"))
    return pieces


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
    nf, ease, tess = RB.nf, RB.ease, RB.tess
    cap = "2  Machining the chamber: a through-frame from 5.5 in. plate and a 20 mm floor plate (spindle always vertical)"
    table_top = 0.0
    st.add_multi("vmc-table", V.table(table_top))
    results = {}
    for part in ("frame", "floor"):
        info = M.CHAMBER_OPS[part]
        final = st.parts[st.find("Process chamber body" if part == "frame" else "Chamber floor plate")[0]].shape
        state = info["blank"]
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
                   f"({state.Volume() * 2.7e-6:.1f} kg); a 12 oz can for scale")
        for f in range(nf(10)):
            st.cam(tuple(((b0[0::2] + b0[1::2]) / 2)), 1100 if part == "frame" else 950, -32 + 1.2 * f, 30)
            st.shot()
        RS.remove_dims(st, "ch-dims")
        for su in plan[part]:
            R = su.get("rots", [])
            jobs = [(0.0, su["ops"])] if su["on"] != "rotary" else su["index"]
            if su["on"] == "rotary":
                state, used_j = _rotary_setup(st, RB, part, su, state, used_j, cap)
                continue
            for _, keys in jobs:
                for key in keys:
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
                   + (" (the core slug, 274 x 184 x 127 mm, is reusable stock)" if part == "frame" else ""))
        for f in range(nf(10)):
            st.cam(tuple(((b1[0::2] + b1[1::2]) / 2)), 950, -30 + 4 * f, 28)
            st.shot()
        RS.remove_dims(st, "ch-dims")
        st.remove("ch-part")
        RS.remove_refs(st, "ch-can")
    st.remove("vmc-table")
    return results


def _place_on_table(shape_m, table_top, lift=25.4):
    """Translation that puts a shape (already rotated) centred over the table with its bottom `lift` above the top."""
    b = bb(shape_m)
    return np.array([-(b[0] + b[1]) / 2, -(b[2] + b[3]) / 2, table_top + lift - b[4]])


def _animate_op(st, RB, su, R, before, after, key, part, cap):
    """One operation in a table, flip or jet setup: the part rotated by R and sitting on its fixture; the tool from above."""
    nf = RB.nf
    bm = xform(before, R)
    t = _place_on_table(bm, 0.0, 25.4 if su["on"] != "jet" else 0.5)
    bm = xform(before, R, t)
    am = xform(after, R, t)
    b = bb(bm)
    st.clear_extra("fx-")
    if su["on"] == "jet":
        st.show_extra("vmc-table", False)
        st.add_multi("fx-jet", jet_bed(0.0, 0.0))
    else:
        st.show_extra("vmc-table", True)
        st.add_multi("fx-hold", holding(su["on"], b))
    c = (b[0::2] + b[1::2]) / 2
    tool = "jet" if su["on"] == "jet" else ("drill" if key.startswith("J:") else "mill")

    def cam(u):
        st.cam(tuple(c + np.array([0, 0, 30.0])), 900, -34 + 14 * u, 34)
    RB.machine_op(st, "ch-part", bm, am, "-z", tool, nf(12), STOCK_COL, cap, su["title"] + " | " + op_label(RB, part, key), cam)
    if key == "FR-02":       # the slug lifts out in one piece
        slug = bm.cut(am)
        st.add("fx-slug", RB.tess(slug), STOCK_COL, edges=True)
        for f in range(nf(8)):
            u = RB.ease((f + 1) / nf(8))
            st.move("fx-slug", RB.T((0, -330.0 * u, 160.0 * math.sin(math.pi * u) + 0.0)))
            st.caption(cap, "The core lifts out as one 274 x 184 x 127 mm slug (~17 kg of 6061): reusable stock, not chips")
            cam(1.0)
            st.shot()
    st.show_extra("vmc-table", True)


def _rotary_setup(st, RB, part, su, state, used_j, cap):
    """The frame on the HRT210: the part rotated by su['rots'] onto a fixture plate on the platter (A axis along +x), then
    indexed to each angle in su['index'] for its operations. Returns the new state and the joint cuts used."""
    nf, ease, tess = RB.nf, RB.ease, RB.tess
    R0 = su.get("rots", [])
    s0 = xform(state, R0)
    b = bb(s0)
    plate_t = 19.05
    riser = max(0.0, (math.hypot(b[3] - b[2], b[5] - b[4]) / 2 + 12.0) - V.HRT210["centre_h"])
    riser = math.ceil(riser / 25.4) * 25.4 if riser > 0 else 0.0
    ax0 = np.array([-420.0, 0.0, 0.0])                        # platter face centre projected on the table
    zc = V.HRT210["centre_h"] + riser
    tail_x = ax0[0] + plate_t + (b[1] - b[0]) + 60.0
    # the part: its mounting face (min x after R0) on the fixture plate, centred on the A axis
    t = np.array([ax0[0] + plate_t - b[0], -(b[2] + b[3]) / 2, zc - (b[4] + b[5]) / 2])
    centre = np.array([ax0[0], 0.0, zc])
    fixed, turning, _ = V.rotary((ax0[0], ax0[1], riser), 0.0, tail_x=None)
    pieces = fixed + ([(pv.Box((ax0[0] - 260, ax0[0] + 20, -160, 160, 0.0, riser)), "#3e454c")] if riser else [])
    st.clear_extra("fx-")
    st.add_multi("fx-rotary", pieces)
    plate = pv.Box((ax0[0], ax0[0] + plate_t, t[1] + b[2] - 10, t[1] + b[3] + 10, zc - (b[5] - b[4]) / 2 - 10, zc + (b[5] - b[4]) / 2 + 10))
    st.add_multi("fx-turn", turning + [(plate, FIX_COL)])
    title = su["title"] + (f" (on a {riser:.0f} mm riser: the frame's {math.hypot(b[3] - b[2], b[5] - b[4]) / 2:.0f} mm swing radius is more than the "
                           f"152.4 mm centre height)" if riser else "")
    angle = 0.0
    for ang, keys in su["index"]:
        # index the A axis from the current angle to ang
        n = nf(8)
        for f in range(n):
            a = angle + (ang - angle) * ease((f + 1) / n)
            Mrot = V.rot_about_x(a, centre)
            st.add("ch-part", tess(xform(state, R0, t)), STOCK_COL, edges=True)
            st.move("ch-part", Mrot)
            st.move("fx-turn", Mrot)
            st.caption(cap, f"{title} | A axis to {ang:+.0f} deg")
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
                    cand = [(kk, tt) for kk, tt in cand if sgn * (bb(tt)[0] + bb(tt)[1]) / 2 > (b[1] - b[0]) * 0.0 + 120.0]
                tools = [tt for _, tt in cand]
            elif key.startswith("J:"):
                used_j.add(key[2:])
            if not tools:
                continue
            after = state.cut(*tools)
            bm, am = about_a(xform(state, R0, t), ang, centre), about_a(xform(after, R0, t), ang, centre)
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
