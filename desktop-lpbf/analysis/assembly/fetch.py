"""Fetching parts from the long table, and screws from the screw presenter on each MiR deck (round 7, issue #260, PR #266).

Used by run_assembly.py when ASM_RECORD is set. For a part: the actor's MiR drives along its lane from the bench to the
item's slot on common.LONG_TABLE (cad/robotbuild/kit_table.py), the arm is planned from park to 70 mm back along its tool
axis from the grasp, comes in on a checked straight line (the fingers open round the item, the item, its nest and its
neighbours in the world), closes, lifts it 90 mm straight up (checked), is planned back to park holding it, and the MiR
drives back to the station dock, the parked arm and the held part swept along the drive against the cell, the table and
everything on it (every robot body's swept box against every other body's box, and the overlapping pairs checked with
FCL every 20 mm). The station planner (run_assembly.arm_place) then takes over from park, holding the part, as before.

Screw presenter (one on each MiR, hung on the cabinet's far face beside the tool stand, its top 20 mm under the deck; run 8 first
had it on the cabinet top, where it took the elbow's room): a vibratory rail presenter, a hopper and a straight rail that presents
one screw head-up at a pick-up nest, as cobot screwdriving cells use. The OnRobot Screwdriver picks its screw from such a
presenter and checks "whether a screw was picked" (onrobot.com/en/products/onrobot-screwdriver, read 2026-11-25; OnRobot leaves
the feeding method to its integrators). No vendor or model is chosen here: the 250 x 130 x 150 mm envelope is an ESTIMATE.
Each screw: from the previous screw's retreat pose the screwdriver is planned to 40 mm above the pick-up nest, goes down 40 mm
and back up (checked), and is planned to the next hole's approach. These trips are recorded and reported separately: they do not change the station results.
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "cad" / "robotbuild"))
import cell as C  # noqa: E402
import cell2 as K  # noqa: E402
from cell import Body, Group, Tm, inv, box_mesh  # noqa: E402

PRESENTER = dict(name="screw presenter (vibratory rail class; vendor not chosen, envelope estimated)",
                 dx=300.0, L=250.0, W=130.0, H=150.0, pick_up=40.0)
DRIVE_STEP = 20.0
PICK_BACK, LIFT = 70.0, 90.0


def presenter_box(x_base, side):
    """World box of the presenter on the MiR of an arm whose base is at x_base (as cell2.mir_bodies draws it: on the
    cabinet's far face beside the tool stand, its top 20 mm under the deck)."""
    ya = -K.ARM_Y if side == "front" else K.ARM_Y
    s = -1.0 if side == "front" else 1.0
    yc = ya + s * K.ARM_OFF
    y_face = yc + s * (K.MIR["W"] / 2 - 30.0)
    z1 = K.MIR["H"] + K.MIR["cab_h"] - 20.0
    y0, y1 = sorted((y_face, y_face + s * 130.0))
    return (x_base + 190.0, x_base + 440.0, y0, y1, z1 - 150.0, z1)


def presenter_pick(x_base, side):
    b = presenter_box(x_base, side)
    # the pick-up nest at the rail's end nearest the arm base, screw head up; the bit comes straight down
    return np.array([b[0] + 30.0, 0.5 * (b[2] + b[3]), b[5]])


class Table:
    """The long table's collision bodies (table top, legs, nests, trays, bins) and the items still on it."""

    def __init__(self, run):
        import kit_table as KT
        self.KT = KT
        self.run = run
        self.slots = [s for s in KT.slots() if s["support"] != "pallet"]
        self.by_member = {}
        for s in self.slots:
            for i in s["part_indices"]:
                sol = [x[1] for x in (s["solids"] or []) if x[0] == i]
                if sol:
                    for so in sol:
                        self.by_member[(i, so)] = s
                else:
                    self.by_member[(i, None)] = s
        t = KT.TAB
        self.static = [Body("long table top", *box_mesh(t["x0"], t["x1"], t["y0"], t["y1"], t["top"] - t["t"], t["top"]), kind="cell")]
        for x in list(np.arange(t["x0"] + 60.0, t["x1"], 1500.0)) + [t["x1"] - 60.0]:
            for y in (t["y0"] + 60.0, t["y1"] - 60.0):
                self.static.append(Body(f"long table leg {x:.0f} {y:.0f}", *box_mesh(x - 25, x + 25, y - 25, y + 25, 0.0, t["top"] - t["t"]),
                                        kind="cell"))
        # round 9: the stretchers (kit_table.stretcher_boxes: a cross rail at each leg pair). Round 8's model had only the top and
        # the legs, so a MiR turning beside the table was drawn 34 mm into the lengthwise rails it then had
        for k, bx in enumerate(KT.stretcher_boxes()):
            self.static.append(Body(f"long table stretcher {k}", *box_mesh(*bx), kind="cell"))
        self.furn = {}                        # slot key -> [Body] (nest or tray: base and four walls)
        for s in self.slots + [b for b in KT.slots() if b["support"] == "bin"]:
            bs = []
            if s["support"] == "riser" and s.get("nest"):
                n = s["nest"]
                bs.append(Body(f"{s['key']} riser", *box_mesh(n[0], n[1], n[2], n[3], n[4], n[5]), kind="fixture"))
            elif s["support"] in ("nest", "tray") and s.get("nest"):
                n = s["nest"]
                if n[5] - n[4] > 0.5:
                    bs.append(Body(f"{s['key']} base", *box_mesh(n[0], n[1], n[2], n[3], n[4], n[5]), kind="fixture"))
                if s["support"] == "nest":
                    ib = s["bbox"]
                    w, h = KT.RIM_W, KT.RIM_H
                    x0, x1, y0, y1 = ib[0] - w - 2.0, ib[1] + w + 2.0, ib[2] - w - 2.0, ib[3] + w + 2.0
                else:
                    w, h = KT.TRAY_WALL, KT.TRAY_H
                    x0, x1, y0, y1 = n[0], n[1], n[2], n[3]
                z = n[5]
                for k, bx in enumerate(((x0, x1, y0, y0 + w), (x0, x1, y1 - w, y1), (x0, x0 + w, y0, y1), (x1 - w, x1, y0, y1))):
                    bs.append(Body(f"{s['key']} rim {k}", *box_mesh(bx[0], bx[1], bx[2], bx[3], z, z + h), kind="fixture"))
            elif s["support"] == "bin":
                b = s["bbox"]
                bs.append(Body(f"{s['key']} bin", *box_mesh(b[0], b[1], b[2], b[3], b[4], b[5]), kind="fixture"))
            for b in bs:
                b.place(np.eye(4))
            self.furn[s["key"]] = bs
        for b in self.static:
            b.place(np.eye(4))
        self.on = {}                          # object index -> its slot
        self._coil = {}                       # slot key -> the coil's box (round 9)
        sc = run.sc
        split_of = {}
        for key, lst in run.split.items():
            for k, i in enumerate(lst):
                split_of[i] = k
        for i, o in enumerate(sc.objs):
            if o.get("V") is None or o.get("kind") == "tool":
                continue
            key = (o["part"], split_of.get(i))
            s = self.by_member.get(key) or (self.by_member.get((o["part"], None)) if split_of.get(i) is None else None)
            if s is not None and o.get("item") is None:
                self.on[i] = s
            elif s is not None and o.get("item") is not None and s["support"] != "bin":
                self.on[i] = s                # inserts and pins already in a part on the table
        self.split_of = split_of

    def slot_of(self, idx):
        for i in idx:
            if i in self.on:
                return self.on[i]
        return None

    def T_item(self, i):
        s = self.on[i]
        return np.asarray(s["T"], float) @ self.run.sc.pose(i, {})

    def remove(self, idx):
        for i in idx:
            self.on.pop(i, None)

    def world(self, x_lo, x_hi, exclude=()):
        """Bodies of the table within x_lo..x_hi: table, legs, nests and trays, and the items still on it."""
        g = Group()
        for b in self.static:
            lo, hi = b.box()
            if hi[0] >= x_lo and lo[0] <= x_hi:
                g.add(b)
        for s in self.slots:
            if s["bbox"][1] < x_lo or s["bbox"][0] > x_hi:
                continue
            for b in self.furn.get(s["key"], []):
                g.add(b)
        ex = set(exclude)
        for i, s in self.on.items():
            if i in ex or s["bbox"][1] < x_lo or s["bbox"][0] > x_hi:
                continue
            if s.get("coil"):
                # round 9: a hose or line lies on the table coiled (kit_table draws the coil, asm_render hides the fitted shape), so
                # its body here is the coil's slot box. Round 8 checked the fitted shape at the slot instead: the release-air line's
                # routed tube reached past the table's edge into lane B, and MiR B's drives at F45 and F45b were not clear
                if s["key"] not in self._coil:
                    bb = s["bbox"]
                    self._coil[s["key"]] = Body(f"{s['key']} coil", *box_mesh(bb[0], bb[1], bb[2], bb[3], bb[4], bb[5]), kind="fixture")
                    self._coil[s["key"]].place(np.eye(4))
                g.add(self._coil[s["key"]])
                continue
            b = self.run.cl.body(i)
            b.place(self.T_item(i))
            g.add(b)
        return g


class _View:
    def __init__(self, world):
        self.world = world


def checker(run, n, groups):
    g = Group()
    for G in groups:
        for b in G.bodies.values():
            g.add(b)
    return C.Checker(_View(g), run.arm(n))


def mir_group(run, n):
    return Group([run.cl.static[k] for k in run.cl.mir[n]])


def frames_line(T0, T1, ds=4.0):
    d = np.linalg.norm(T1[:3, 3] - T0[:3, 3])
    k = max(2, int(math.ceil(d / ds)) + 1)
    out = []
    for s in np.linspace(0.0, 1.0, k):
        T = T0.copy()
        T[:3, 3] = T0[:3, 3] * (1 - s) + T1[:3, 3] * s
        out.append(T)
    return out


def follow(run, n, Ts, close, allow, chk, seed, ik_close=None, strict=False):
    """IK along Ts with one branch held, each frame checked against chk's world. -> (ok, qs, why).
    ik_close: the gripper opening whose TCP the IK places on Ts (the fingers may be checked open, `close`, while the arm already
    stands where the closed fingers' TCP will be: no arm motion when they close). strict: start on the seed's own branch."""
    a = run.arm(n)
    ikc = close if ik_close is None else ik_close
    a.close = ikc
    # strict: the arm is already at the seed, which reaches Ts[0] (the lift starts where the descent ended)
    firsts = [np.asarray(seed, float)] if strict else a.ik_all(Ts[0], seed=seed)
    best = (False, [], "no IK at the start")
    for q0 in firsts[:8]:
        qs, prev, ok, why = [], q0, True, ""
        for k, T in enumerate(Ts):
            a.close = ikc
            sols = [q0] if (strict and k == 0) else a.ik_all(T, seed=prev)
            if not sols:
                ok, why = False, f"no IK {k * 4:.0f} mm along"
                break
            q = sols[0]
            if k and np.abs(q - prev).max() > math.radians(20.0):
                ok, why = False, "IK branch flip"
                break
            c = chk.collisions(q, close, allow, first=True)
            if c:
                ok, why = False, f"{c[0][0].split('/')[-1]} hits {c[0][1][:50]}"
                break
            qs.append(q)
            prev = q
        if ok:
            return True, qs, ""
        if len(qs) > len(best[1]) or (not best[1] and best[2].startswith("no IK at the start")):
            best = (False, qs, why)
    return best


def sweep_drive(run, n, x0, x1, q, close, extra_world=None):
    """The MiR drives its arm (at q, holding whatever it holds) from dock x0 to x1. -> (ok, why). Every robot body's box
    swept along x against every world body's box; overlapping pairs checked with FCL every DRIVE_STEP mm."""
    cl = run.cl
    a = run.arm(n)
    if abs(x1 - x0) < 1e-6:
        return True, ""
    world = cl.world(n)
    for k in list(world.bodies):
        if k.startswith(f"{n} "):          # its own MiR, cabinet, plate and stand move with it
            world.remove(k)
    if extra_world is not None:
        for b in extra_world.bodies.values():
            world.add(b)
    cl.move_mir(n, x0)
    a.place(q, close)
    robot = list(a.bodies()) + [cl.static[k] for k in cl.mir[n]]
    names, lo, hi = world.boxes()
    lo_s, hi_s = [], []
    dx = x1 - x0
    pairs = []
    for b in robot:
        l, h = b.box()
        ls = np.minimum(l, l + np.array([dx, 0, 0]))
        hs = np.maximum(h, h + np.array([dx, 0, 0]))
        ov = np.all((ls[None, :] <= hi) & (lo <= hs[None, :]), axis=1)
        for j in np.nonzero(ov)[0]:
            y = world.bodies[names[j]]
            if y.name == "floor":
                continue
            pairs.append((b, y))
    if not pairs:
        cl.move_mir(n, x1)
        return True, ""
    nstep = max(1, int(math.ceil(abs(dx) / DRIVE_STEP)))
    hit = None
    for s in range(nstep + 1):
        x = x0 + dx * s / nstep
        cl.move_mir(n, x)
        a.place(q, close)
        rb = {b.name: b for b in list(a.bodies()) + [cl.static[k] for k in cl.mir[n]]}
        for b, y in pairs:
            bb = rb.get(b.name, b)
            if C.hit(bb.obj, y.obj):
                hit = f"at x {x:.0f}: {bb.name.split('/')[-1]} hits {y.name[:50]}"
                break
        if hit:
            break
    cl.move_mir(n, x1)
    a.place(q, close)
    return hit is None, hit or ""


def pick_plan(run, n, idx, body, off, G_rel, close, tool, slot):
    """Plan the pick of objects idx (held body `body`, off = TCP -> its machine frame) from the table.
    G_rel: the grasp in the item's machine frame. Returns a dict with the motion pieces, or ok=False and why."""
    cl = run.cl
    a = run.arm(n)
    T_slot = np.asarray(slot["T"], float)
    G = T_slot @ G_rel
    gx = float(G[0, 3])
    T = run.table
    out = dict(ok=False, why="no dock along the table reaches it", slot=slot["key"])
    item_names = [cl.body(i).name for i in idx]
    furn = [b.name for b in T.furn.get(slot["key"], [])]
    allow_tool = frozenset([("tool", nm) for nm in item_names] + [("tool", nm) for nm in furn])
    allow_held = frozenset([("held", nm) for nm in furn + ["long table top"]] + [("tool", nm) for nm in furn + ["long table top"]])
    for xb in (gx - 350.0, gx + 350.0, gx, gx - 600.0, gx + 600.0):
        cl.move_mir(n, xb)
        q_park = a.park_q()
        a.release()
        a.place(q_park, 0.0)
        tw = T.world(xb - 1500.0, xb + 1500.0)
        chk = checker(run, n, [tw, mir_group(run, n), Group([cl.static["floor"]])])
        P0 = G @ Tm(p=(0.0, 0.0, -PICK_BACK))
        c_open = 0.0 if tool.startswith("gripper") else 0.0
        ok, qs_in, why = follow(run, n, frames_line(P0, G), c_open, allow_tool, chk, q_park, ik_close=close)
        if not ok:
            out["why"] = f"in to the grasp: {why}"
            continue
        a.place(q_park, c_open)
        p1, info1 = chk.plan(q_park, qs_in[0], c_open, iters=1200)
        if p1 is None:
            out["why"] = f"park to the item: {info1.get('reason')}"
            continue
        # lift with the item held
        tw2 = T.world(xb - 1500.0, xb + 1500.0, exclude=idx)
        a.hold(body, off)
        chk2 = checker(run, n, [tw2, mir_group(run, n), Group([cl.static["floor"]])])
        Gl = Tm(p=(0.0, 0.0, LIFT)) @ G
        ok, qs_up, why = follow(run, n, frames_line(G, Gl), close, allow_held, chk2, qs_in[-1], strict=True)
        if not ok:
            a.release()
            out["why"] = f"lift: {why}"
            continue
        a.place(qs_up[-1], close)
        p2, info2 = chk2.plan(qs_up[-1], q_park, close, allow=allow_held, iters=1200)
        a.release()
        if p2 is None:
            out["why"] = f"back to park holding it: {info2.get('reason')}"
            continue
        out = dict(ok=True, why="", x=xb, to_item=p1, in_=qs_in, up=qs_up, to_park=p2, close=close, slot=slot["key"])
        break
    return out


def presenter_trip(run, n, q_from, q_to, close=0.0, held=None, allow=frozenset()):
    """Screwdriver from q_from (after the last screw) to the presenter's pick-up nest and on to q_to (the next hole's
    approach). Straight joint lines if clear, else RRT-Connect (200 iterations). -> dict(ok, pieces or why).
    Round 10, held = (screw body, TCP offset): the way up out of the nest and on to q_to carry the screw, so they are checked
    with it (allow: the screw's seat contacts), and the last 12 deg into the hole's mouth every 0.25 deg."""
    cl = run.cl
    a = run.arm(n)
    xb = float(a.base[0, 3])
    pick = presenter_pick(xb, a.side)
    Tp = Tm(p=pick) @ K.Rx(180.0)          # tool z straight down
    chk = K.checker(cl, n)
    best = None
    for roll in (0.0, 90.0, 180.0, 270.0):
        Tr = Tp @ K.Rz(roll)
        above = Tm(p=(0.0, 0.0, PRESENTER["pick_up"])) @ Tr
        ok, qs_dn, why = follow(run, n, frames_line(above, Tr), close, frozenset([("tool", f"{n} screw presenter")]), chk, q_from)
        if not ok:
            best = best or dict(ok=False, why=f"presenter: {why}")
            continue
        a.place(q_from, close)
        p1, i1 = chk.plan(q_from, qs_dn[0], close, iters=200)
        if p1 is None:
            best = dict(ok=False, why=f"to the presenter: {i1.get('reason')}")
            continue
        if held is not None:
            a.hold(*held)
            try:
                chk2 = K.checker(cl, n)
                allow2 = frozenset(allow) | frozenset([("held", f"{n} screw presenter"), ("tool", f"{n} screw presenter")])
                bad = next((q for q in qs_dn if chk2.collisions(q, close, allow2, first=True)), None)
                if bad is not None:
                    best = dict(ok=False, why="up out of the presenter with the screw: blocked")
                    continue
                p2, i2 = chk2.plan(qs_dn[0], q_to, close, allow=allow2, iters=200)
                if p2 is not None and not chk2.tail_free(p2, close, allow2):
                    p2, i2 = None, dict(reason="the screw cuts the hole's edge on the way in")
            finally:
                a.release()
        else:
            p2, i2 = chk.plan(qs_dn[0], q_to, close, iters=200)
        if p2 is None:
            best = dict(ok=False, why=f"presenter to the hole: {i2.get('reason')}")
            continue
        return dict(ok=True, to=p1, down=qs_dn, up=qs_dn[::-1], on=p2)
    return best or dict(ok=False, why="no pose at the presenter")
