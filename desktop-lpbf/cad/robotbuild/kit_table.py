"""The long parts table: every part of the M50 desktop LPBF kitted on common.LONG_TABLE for the two-arm build (issue #260,
PR #266, round 7).

Sterling, 2026-11-25: "the assembly being carried out **by** two UR12e units each on a MiR250 using the full set of parts
spread across a really long table". This module gives every item a slot on that table (hall frame = cell2's world frame):

  * one slot for each item analysis/assembly/sequence.py places (a part, a bought or bench-built sub-assembly such as the
    pre-assembled Z stage, the recoater rail, the drawer or the door; one slot per solid where the step places the solids one
    at a time, one per part where it places them part by part), and one for every other part of the model;
  * grouped by render_build.py's kit categories (CATS: stock, sheet, motion, gas, optics, elec, seal, frame) in that order
    along the table, from the bench end (x = 2600) outward, in assembly order inside a category;
  * each item sits in the orientation it goes on in: its assembled orientation in the sub-assembly's phase (cell2.T_phase:
    the heater stack and the module upside down about y, the chamber upside down about x for chapter 4a), so the arm takes
    it with the grasp it inserts it with and no regrasp. Seals lie flat in the seal trays (their tools take them there);
  * on the half of the table nearest the arm that places it (arm A's items on the front half, y < 0; arm B's on the back),
    in rows along x, >= 50 mm apart (finger room for the 2F-85 is 40 mm), 30 mm in from the edges;
  * on the table top, or, where the item would not stand on its own (taller than 1.3 x its narrow footprint side, or a sheet
    on edge), on a kitting nest: a 12 mm plate with a 15 mm pocket rim round the item's foot. Parts under 40 mm go into
    small-part trays (a compartment each, the walls 20 mm off the part); screws, inserts and pins into labelled bins, one per
    McMaster part number, in the seal-and-fastener zone;
  * heavy items (over a UR12e's 12.5 kg payload: the UPS, the laser, the scroll pump, the rack frame, the power box) and the
    bulky items a person fits (the guard frame and panels, the rack panels, the umbilical duct: over 500 mm) go on EUR pallets
    behind arm B's lane (y 1250-2050), flagged `support == "pallet"`; a person and a pallet jack or lift handles them.

For machined parts (render_build.kind: "stock" and "sheet") each slot also gives the stock blank (render_build.stock_blank /
sheet_blank) at the same place, so the table can be drawn before machining (`meshes(mode="stock")`).

API
    slots()               -> [dict(key, step, part_indices, solids, category, T (4x4: machine frame -> hall), bbox, ...)]
    meshes(mode)          -> [dict(key, name, mesh (pyvista), color)]: the table, nests, trays, bins, pallets and every item,
                             "finished" or "stock" (blanks for the machined parts)
    table_meshes()        -> the table, nests, trays, bins and pallets alone (static furniture)
    slot_for(step_id)     -> the slots of one sequence step
Run as a script it prints the layout and writes analysis/out/assembly/kit_slots.json (committed: small).
"""
from __future__ import annotations

import hashlib
import json
import math
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
CAD = HERE.parent
LPBF = CAD.parent
ASM = LPBF / "analysis" / "assembly"
for p in (str(CAD), str(HERE), str(ASM)):
    if p not in sys.path:
        sys.path.insert(0, p)
import common  # noqa: E402

TAB = common.LONG_TABLE
GAP = 50.0                  # between items (x and y): the 2F-85's fingers need 40 mm
EDGE = 30.0                 # from the table's edges
MID = 20.0                  # half-gap at the centre line between the two arms' halves
PAYLOAD = 12.5              # UR12e payload, kg (UR datasheet)
BULKY = 500.0               # unplaced items over this go to a pallet (a person fits them)
NEST_T, RIM_H, RIM_W = 12.0, 15.0, 8.0
RISER_H = 45.0              # a riser under a low part the gripper takes from above (the fingertips reach 30-40 mm below it)
TRAY_T, TRAY_WALL, TRAY_H, TRAY_MARGIN = 3.0, 2.0, 18.0, 20.0
SMALL = 40.0                # parts with every side under this go into a small-part tray compartment
PALLET = dict(L=1200.0, W=800.0, H=144.0, y0=1250.0, x0=3000.0, gap=300.0)   # EUR pallet 1200 x 800 x 144
OUT_JSON = LPBF / "analysis" / "out" / "assembly" / "kit_slots.json"
CACHE = common.ROOT / "cache"
CAT_ORDER = ["stock", "sheet", "motion", "gas", "optics", "elec", "seal", "frame"]
CAT_COL = dict(stock="#cfd4d9", sheet="#b4bcc4")
NEST_COL, TRAY_COL, BIN_COL, PALLET_COL = "#3d6e9e", "#4f6b7a", "#2f5d8a", "#b08a57"

# cell2.T_phase's rotations (machine frame -> world), without importing the cell (FCL, the arm meshes)
_RY180 = np.diag([-1.0, 1.0, -1.0, 1.0])
_RX180 = np.diag([1.0, -1.0, -1.0, 1.0])
PHASE_R = dict(stack_inv=_RY180, body_inv=_RY180, chamber_inv=_RX180, stack_up=np.eye(4), body_up=np.eye(4),
               chamber_up_P=np.eye(4), chamber_up_T=np.eye(4), upright=np.eye(4))
SPLIT = ("Chamber legs", "Optics bridge posts", "Macor standoff rings", "Radiation shields", "Zero-point posts",
         "Zero-point module plates", "Zero-point clamping modules", "Zero-point arms", "Zero-point clamping pins",
         "Door hinge knuckles on the chamber")      # run_assembly.Run.split_parts: one object per solid


def _hash():
    h = hashlib.sha256()
    for f in sorted(CAD.glob("*.py")) + [ASM / "sequence.py", pathlib.Path(__file__)]:
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


_PARTS = None


def model():
    global _PARTS
    if _PARTS is None:
        import lpbf_low as M
        _PARTS = M.build(module="M50")
    return _PARTS


def _bbox(shape):
    b = shape.BoundingBox()
    return np.array([b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax], float)


def _rot_bbox(b, R):
    c = np.array([[x, y, z] for x in b[:2] for y in b[2:4] for z in b[4:]], float) @ R[:3, :3].T
    return np.array([c[:, 0].min(), c[:, 0].max(), c[:, 1].min(), c[:, 1].max(), c[:, 2].min(), c[:, 2].max()])


def _Tt(p):
    T = np.eye(4)
    T[:3, 3] = p
    return T


def _flat_R(b):
    """A rotation that lays a thin item flat: its thinnest side along z (for seals and sheet on edge in the trays)."""
    d = [b[1] - b[0], b[3] - b[2], b[5] - b[4]]
    k = int(np.argmin(d))
    if k == 2:
        return np.eye(4)
    R = np.eye(4)
    if k == 0:          # thin along x: turn 90 deg about y
        R[:3, :3] = [[0, 0, -1], [0, 1, 0], [1, 0, 0]]
    else:               # thin along y: turn 90 deg about x
        R[:3, :3] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
    return R


def _mass(p, frac=1.0):
    import lpbf_low as M
    if p.mass_kg is not None:
        return float(p.mass_kg) * frac
    try:
        v = p.shape.Volume()
    except Exception:
        v = 0.0
    return v * M.MAT.get(p.mat, M.MAT["misc"])["rho"] * 1e-9 * frac


# ------------------------------------------------------------------------------------------------ what goes on the table
def _items(parts):
    """Items in assembly order: dicts(key, step, members [(part, solid or None)], phase R, tool, actor, flags)."""
    import render_build as RB
    import lpbf_low as M
    import sequence as SQ
    names = [p.name for p in parts]
    split_names, nsol = {}, {}
    for i, p in enumerate(parts):
        if any(k in p.name for k in SPLIT) and "fastener" not in p.tags:
            base = p.name.split(" (")[0]
            nsol[i] = len(p.shape.Solids())
            for s in range(nsol[i]):
                split_names[(i, s)] = f"{base} #{s + 1}"
    placed = set()

    def resolve(keys):
        """run_assembly.Run.resolve at the part level: split parts as one member per solid."""
        out = []
        for k in keys:
            if k == "@module":
                out += [(i, None) for i, p in enumerate(parts) if M.moves_with(p, "module")]
            elif k == "@chamberset":
                continue
            elif k in ("@legs", "@posts"):
                key = "Chamber legs" if k == "@legs" else "Optics bridge posts"
                out += [m for m, n in split_names.items() if n.startswith(key)]
            else:
                for i, n in enumerate(names):
                    if k in n:
                        out += [(i, s) for s in range(nsol[i])] if i in nsol else [(i, None)]
                out += [m for m, n in split_names.items() if k in n]
        seen, res = set(), []
        for m in out:
            if m not in seen and "context" not in parts[m[0]].tags:
                seen.add(m)
                res.append(m)
        return res

    items = []
    for st in SQ.steps():
        do = st["do"]
        if do == "screws":            # driven from the screw presenter, which the bins refill: not items of later steps
            placed.update((i, None) for i, p in enumerate(parts) if "fastener" in p.tags and p.tags[1] == st["joint"])
            continue
        if do == "note" and st["id"] in NOTE_KEYS:
            st = dict(st, keys=NOTE_KEYS[st["id"]], phase="upright", actor="person", tool="hand")
            do = "place"
        elif do not in ("place", "dual", "seal"):
            continue
        mem = [m for m in resolve(st.get("keys", [])) if m not in placed and (m[0], None) not in placed
               and not (m[1] is None and any((m[0], s) in placed for s in range(64)))]
        if not mem:
            continue
        R = PHASE_R[st.get("phase", "upright")]
        base = dict(step=st["id"], label=st["label"], tool=st.get("tool", "gripper"), actor=st.get("actor", "A"),
                    phase=st.get("phase", "upright"), R=R, do=do)
        if do == "seal" or (st["id"] in NOTE_KEYS and all(parts[i].mat == "fkm" for i, _ in mem)):
            base.update(R=None, seal=True)     # laid flat in the seal tray
        if st.get("per_solid"):
            for k, m in enumerate(mem):
                items.append(dict(base, key=f"{st['id']}#{k + 1}", members=[m]))
        elif st.get("per_part"):
            by = {}
            for m in mem:
                by.setdefault(m[0], []).append(m)
            for k, (i, ms) in enumerate(by.items()):
                items.append(dict(base, key=f"{st['id']}#{k + 1}", members=ms))
        else:
            items.append(dict(base, key=st["id"], members=mem))
        placed.update(mem)
    # every other part, in model order; fasteners into bins by part number
    bins = {}
    for i, p in enumerate(parts):
        if "context" in p.tags or "calibration" in p.tags:
            continue
        if (i, None) in placed or any((i, s) in placed for s in range(len(p.shape.Solids()))):
            continue
        k = RB.kind(p)
        if k == "fastener":
            bins.setdefault(p.mcm, []).append(i)
            continue
        sols = p.shape.Solids()
        if 1 < len(sols) <= 8 and not any(x in p.name for x in ("rack frame", "Guard frame", "Guard door rail", "Laser guard panels")):
            # a set of separate pieces drawn in place (four levelling mounts, two E-stops...): one slot per piece
            bbs = [_bbox(s) for s in sols]
            whole = _bbox(p.shape)
            if max(whole[1] - whole[0], whole[3] - whole[2]) > 1.6 * max(max(b[1] - b[0], b[3] - b[2]) for b in bbs):
                for s in range(len(sols)):
                    items.append(dict(key=f"P{i:03d}#{s + 1}", step="", label=p.name, tool="", actor="", phase="upright",
                                      R=np.eye(4), do="", members=[(i, s)], unplaced=True))
                continue
        items.append(dict(key=f"P{i:03d}", step="", label=p.name, tool="", actor="", phase="upright", R=np.eye(4), do="",
                          members=[(i, None)], unplaced=True))
    return items, bins


# a person's (or a bench) step's parts get their own slot at that step, so they are not folded into a later robot step
NOTE_KEYS = {
    "M09": ["Bore seal"],
    "C00": ["Overflow funnel block", "Overflow funnel O-ring", "Overflow port"],
    "C09e": ["Zero-point push-in fittings"],
    "C15b": ["Overflow-jar present sensor", "Overflow-jar sensor bracket"],
    "F06b": ["Zero-point release-air line"],
    "F08": ["Overflow clamp"],
    "F12": ["Plate-height through-beam", "Fibre-head O-rings"],
    "F49": ["Pressure transducer", "Overpressure relief valve"],
    "F53": ["f-theta lens", "f-theta focus shims", "f-theta adapter ring"],
    "F58": ["Process fiber"],
}


def _member_shape(parts, m):
    i, s = m
    p = parts[i]
    return p.shape if s is None else p.shape.Solids()[s]


def _classify(parts, it):
    import render_build as RB
    i0 = it["members"][0][0]
    p0 = parts[i0]
    k0 = RB.kind(p0)
    cat = RB.kit_cat(p0, k0) if k0 not in ("fastener", "context") else "seal"
    if it.get("seal"):
        cat = "seal"
    it["category"] = cat
    it["kinds"] = [RB.kind(parts[i]) for i, _ in it["members"]]
    nsol = {i: max(1, len(parts[i].shape.Solids())) for i, _ in it["members"]}
    it["mass_kg"] = round(sum(_mass(parts[i], 1.0 if s is None else 1.0 / nsol[i]) for i, s in it["members"]), 3)
    it["name"] = p0.name.split(" (")[0] if len(it["members"]) == 1 else it.get("label", p0.name)[:90]


# ------------------------------------------------------------------------------------------------ the layout
def _footprint(parts, it):
    """Rotate the item into its table orientation and size its support."""
    import render_build as RB
    bbs = [_bbox(_member_shape(parts, m)) for m in it["members"]]
    b = np.array([min(x[0] for x in bbs), max(x[1] for x in bbs), min(x[2] for x in bbs), max(x[3] for x in bbs),
                  min(x[4] for x in bbs), max(x[5] for x in bbs)])
    R = it["R"] if it["R"] is not None else _flat_R(b)
    long_thin = any(x in parts[it["members"][0][0]].name for x in ("hoses", "Argon line", "O2 sample", "Process fiber",
                                                                  "Chilled-water", "Argon supply", "Pump exhaust",
                                                                  "release-air line"))
    it["coil"] = None
    if long_thin:
        nm = parts[it["members"][0][0]].name
        r = 13.0 if "hoses" in nm else 6.0 if "Chilled" in nm else 4.0 if "fiber" in nm else 2.0 if "release-air" in nm else 3.2
        ring = 150.0 if r > 5 else 110.0 if r > 3 else 60.0
        it["coil"] = dict(ring=ring, r=r, turns=3, pitch=2.2 * r)
        rb = np.array([-ring - r, ring + r, -ring - r, ring + r, -r, 3 * 2.2 * r + r])
        R = np.eye(4)
    else:
        rb = _rot_bbox(b, R)
    it["R_table"] = R
    it["rbb"] = rb
    # the stock blanks of its machined members, in the same orientation
    blanks = []
    for m, kd in zip(it["members"], it["kinds"]):
        if kd not in ("stock", "sheet"):
            continue
        p = parts[m[0]]

        class _P:
            pass
        q = _P()
        q.shape, q.name, q.mat = _member_shape(parts, m), p.name, p.mat
        try:
            if kd == "stock":
                shp, lab = RB._blank(q.shape, p.name)
            else:
                shp, lab = RB.sheet_blank(q), "sheet, cut to size"
        except Exception as e:      # noqa: BLE001
            shp, lab = None, f"no blank ({e})"
        if shp is None:
            continue
        bb = _rot_bbox(_bbox(shp), R)
        import lpbf_low as M
        mass = shp.Volume() * M.MAT.get(p.mat, M.MAT["al6061"])["rho"] * 1e-9
        blanks.append(dict(part=m[0], solid=m[1], label=lab, rbb=bb, mass_kg=round(mass, 2), _shape=shp,
                           color=RB.SS_STOCK if p.mat.startswith("ss") or "Striker" in p.name else RB.STOCK_COL))
    it["blanks"] = blanks
    dx, dy, dz = rb[1] - rb[0], rb[3] - rb[2], rb[5] - rb[4]
    # support
    heavy = it["mass_kg"] > PAYLOAD and it.get("do") != "dual"
    bulky = it.get("unplaced") and max(dx, dy) > BULKY
    # the rack, gas-module and tray parts are fitted by a person in chapter 5 (sequence T02-T05), not by the arms at the
    # bench: they wait on the pallets with the heavy units they go with
    bulky = bulky or (it.get("unplaced") and parts[it["members"][0][0]].module in ("rack", "gas", "tray"))
    too_wide = min(dx, dy) > TAB["y1"] - TAB["y0"] - 2 * EDGE
    if heavy or bulky or too_wide:
        it["support"] = "pallet"
    elif it.get("seal") or (max(dx, dy, dz) < SMALL and it["mass_kg"] < 0.2):
        it["support"] = "tray"
    elif it["coil"] is not None:
        it["support"] = "table"
    elif dz > 1.3 * max(min(dx, dy), 1.0) and dz > 30.0:
        it["support"] = "nest"
    else:
        it["support"] = "table"
    # run 8 (round 7): a part the 2F-85 takes from above that stands under 45 mm tall: its fingertips reach below the part,
    # so it sits on a riser (a column half its footprint, RISER_H tall) that the fingertips pass beside, as the stack nest
    if (it["support"] in ("table", "tray") and str(it.get("tool", "")).startswith("gripper") and dz < 45.0
            and it.get("actor") in ("A", "B") and not it.get("seal")):
        it["support"] = "riser"
    fx = max([dx] + [x["rbb"][1] - x["rbb"][0] for x in blanks])
    fy = max([dy] + [x["rbb"][3] - x["rbb"][2] for x in blanks])
    pad = {"nest": 2 * (RIM_W + 2.0) + 20.0, "tray": 2 * (TRAY_MARGIN + TRAY_WALL)}.get(it["support"], 0.0)
    it["fx"], it["fy"] = fx + pad, fy + pad


def _side(it):
    a = it.get("actor") or ""
    if it.get("do") == "dual" or it["fy"] > (TAB["y1"] - TAB["y0"]) / 2 - EDGE - MID:
        return "C"
    return "B" if a == "B" else "A"


def layout(parts=None):
    """Compute every slot (no meshes). Returns (slots, bins, pallets)."""
    parts = model() if parts is None else parts
    items, bins = _items(parts)
    for it in items:
        _classify(parts, it)
        _footprint(parts, it)
    order = {c: k for k, c in enumerate(CAT_ORDER)}
    seq = {id(it): k for k, it in enumerate(items)}
    items.sort(key=lambda it: (order.get(it["category"], 99), seq[id(it)]))
    # ---- pack each category along x: front half (arm A), back half (arm B), centre items (dual carries, wide items) span both
    half = (TAB["y1"] - TAB["y0"]) / 2 - EDGE - MID          # usable depth of one half
    x = TAB["x0"] + EDGE
    zones = []
    for cat in CAT_ORDER:
        its = [it for it in items if it["category"] == cat and it["support"] != "pallet"]
        if not its:
            continue
        x_zone = x
        # Columns along x shared by the two halves: arm A's items fill a column from the front edge, arm B's from the back
        # edge, each up to the centre line. A two-arm or wide item sits across the centre line (as on its station: both arms
        # reach it from their own side) and opens a column whose two halves keep the depth left beside it. First fit: an item
        # goes into the first column it fits, so small parts fill the space deep ones leave and the order along x stays close
        # to the assembly order.
        cols = []
        D = TAB["y1"] - TAB["y0"] - 2 * EDGE

        def new_col(w):
            x0 = cols[-1]["x"] + cols[-1]["w"] + GAP if cols else x
            c = dict(x=x0, w=w, A=0.0, B=0.0, cap=half)
            cols.append(c)
            return c

        def place_in(side, it):
            for c in cols:
                if (it["fx"] <= c["w"] or c is cols[-1]) and c[side] + it["fy"] <= c["cap"]:
                    break
            else:
                c = new_col(it["fx"])
            c["w"] = max(c["w"], it["fx"])
            if side == "A":
                it["cx"], it["cy"] = c["x"] + it["fx"] / 2, TAB["y0"] + EDGE + c["A"] + it["fy"] / 2
            else:
                it["cx"], it["cy"] = c["x"] + it["fx"] / 2, TAB["y1"] - EDGE - c["B"] - it["fy"] / 2
            c[side] += it["fy"] + GAP

        lens = {"A": 0.0, "B": 0.0}
        for it in its:
            s = _side(it)
            if s == "C":
                c = new_col(it["fx"])
                c["cap"] = max(0.0, (D - it["fy"]) / 2 - GAP)
                it["cx"], it["cy"] = c["x"] + it["fx"] / 2, 0.5 * (TAB["y0"] + TAB["y1"])
                it["side"] = "C"
                continue
            if it.get("actor") not in ("A", "B"):     # a person's or an unassigned item: the half with less on it so far
                s = "A" if lens["A"] <= lens["B"] else "B"
            it["side"] = s
            lens[s] += (it["fx"] + GAP) * (it["fy"] + GAP)
            place_in(s, it)
        x = (cols[-1]["x"] + cols[-1]["w"] if cols else x) + 2 * GAP
        zones.append(dict(category=cat, x0=x_zone, x1=x - 2 * GAP))
    # ---- bins (one per part number) after the seal zone's items, in rows of 60-120 mm cells
    import render_build as RB
    import fasteners as FS
    bin_slots = []
    seal_zone = next((z for z in zones if z["category"] == "seal"), None)
    bx = (seal_zone["x1"] if seal_zone else x) + GAP
    by_row = [TAB["y0"] + EDGE, None]
    row_d = 0.0
    y_cur = TAB["y0"] + EDGE
    x_cur = bx
    col_w = 0.0
    for pn, idx in sorted(bins.items(), key=lambda kv: kv[0]):
        n = sum(len(parts[i].shape.Solids()) for i in idx)
        try:
            shp = FS.shape(pn)
            b = shp.BoundingBox()
            sp = max(b.xlen, b.ylen) + 3.0
            cols_n = max(1, math.ceil(math.sqrt(n)))
            w = cols_n * sp + 16.0
            d = math.ceil(n / cols_n) * sp + 16.0
            h = b.zlen
        except Exception:
            w = d = 70.0
            h = 20.0
        w, d = max(w, 60.0), max(d, 60.0)
        if y_cur + d > TAB["y1"] - EDGE:
            x_cur += col_w + 20.0
            y_cur, col_w = TAB["y0"] + EDGE, 0.0
        bin_slots.append(dict(key=f"BIN-{pn}", step="", part_indices=idx, solids=None, category="seal", support="bin",
                              name=f"{pn}: {n} x {parts[idx[0]].name.split(' (')[0][:50]}", count=n, pn=pn,
                              bbox=[x_cur, x_cur + w, y_cur, y_cur + d, TAB["top"], TAB["top"] + max(h + 10.0, 30.0)],
                              T=_Tt((x_cur, y_cur, TAB["top"])).tolist(), nest=None, actor="", tool="screw presenter",
                              mass_kg=0.0, two_arm=False, heavy=False, coil=None, stock=[], kinds=["fastener"],
                              label=f"{pn} x{n}", side="A" if y_cur + d / 2 < 0 else "B"))
        y_cur += d + 20.0
        col_w = max(col_w, w)
    if bin_slots:
        x = max(x, x_cur + col_w + 2 * GAP)
        if seal_zone:
            seal_zone["x1"] = x_cur + col_w
    # ---- pallets behind arm B's lane
    pal_items = sorted([it for it in items if it["support"] == "pallet"], key=lambda it: -it["fy"])
    pallets = []
    px = PALLET["x0"]

    def new_pallet(L):
        nonlocal px
        p = dict(key=f"PALLET-{len(pallets) + 1}", x0=px, x1=px + L, y0=PALLET["y0"], y1=PALLET["y0"] + PALLET["W"],
                 top=PALLET["H"], rows=[], items=[])
        pallets.append(p)
        px += L + PALLET["gap"]
        return p
    for it in pal_items:
        placed_ = False
        for p in pallets:                       # first fit: a row with room, or a new row on a pallet with depth left
            for r in p["rows"]:
                if r["x"] + it["fx"] <= p["x1"] - 20.0 and it["fy"] <= r["d"]:
                    it["cx"], it["cy"] = r["x"] + it["fx"] / 2, r["y"] + it["fy"] / 2
                    r["x"] += it["fx"] + 40.0
                    placed_ = True
                    break
            if not placed_:
                y_used = sum(r["d"] + 40.0 for r in p["rows"])
                if p["y0"] + 20.0 + y_used + it["fy"] <= p["y1"] - 20.0 and p["x0"] + 20.0 + it["fx"] <= p["x1"] - 20.0:
                    r = dict(x=p["x0"] + 20.0, y=p["y0"] + 20.0 + y_used, d=it["fy"])
                    p["rows"].append(r)
                    it["cx"], it["cy"] = r["x"] + it["fx"] / 2, r["y"] + it["fy"] / 2
                    r["x"] += it["fx"] + 40.0
                    placed_ = True
            if placed_:
                p["items"].append(it["key"])
                break
        if not placed_:
            p = new_pallet(max(PALLET["L"], it["fx"] + 40.0))
            r = dict(x=p["x0"] + 20.0, y=p["y0"] + 20.0, d=it["fy"])
            p["rows"].append(r)
            it["cx"], it["cy"] = r["x"] + it["fx"] / 2, r["y"] + it["fy"] / 2
            r["x"] += it["fx"] + 40.0
            p["items"].append(it["key"])
        it["side"] = "pallet"
    for p in pallets:
        p.pop("rows", None)
    # ---- transforms
    slots = []
    for it in items:
        rb, R = it["rbb"], it["R_table"]
        if it["support"] == "pallet":
            pal = next(p for p in pallets if it["key"] in p["items"])
            z0 = pal["top"]
        else:
            z0 = TAB["top"] + {"nest": NEST_T, "tray": TRAY_T, "riser": RISER_H}.get(it["support"], 0.0)
        c = np.array([(rb[0] + rb[1]) / 2, (rb[2] + rb[3]) / 2, rb[4]])
        T = _Tt((it["cx"] - c[0], it["cy"] - c[1], z0 - c[2])) @ R
        bb = [it["cx"] - (rb[1] - rb[0]) / 2, it["cx"] + (rb[1] - rb[0]) / 2, it["cy"] - (rb[3] - rb[2]) / 2,
              it["cy"] + (rb[3] - rb[2]) / 2, z0, z0 + rb[5] - rb[4]]
        stock = []
        for bl in it["blanks"]:
            # the blank stands where its part will (blanks are built round the part's own box), dropped onto the support
            Tb = T.copy()
            Tb[2, 3] += z0 - (bl["rbb"][4] + T[2, 3])
            stock.append(dict(part=bl["part"], solid=bl["solid"], label=bl["label"], mass_kg=bl["mass_kg"], T=Tb.tolist(),
                              heavy=bl["mass_kg"] > PAYLOAD, color=bl["color"]))
        nest = None
        if it["support"] == "riser":
            fx0, fy0 = (rb[1] - rb[0]), (rb[3] - rb[2])
            wx, wy = max(8.0, 0.45 * fx0), max(8.0, 0.45 * fy0)
            nest = [it["cx"] - wx / 2, it["cx"] + wx / 2, it["cy"] - wy / 2, it["cy"] + wy / 2, TAB["top"], z0]
        if it["support"] in ("nest", "tray"):
            m = (RIM_W + 2.0 + 10.0) if it["support"] == "nest" else (TRAY_MARGIN + TRAY_WALL)
            fx0, fy0 = (rb[1] - rb[0]), (rb[3] - rb[2])
            nest = [it["cx"] - fx0 / 2 - m, it["cx"] + fx0 / 2 + m, it["cy"] - fy0 / 2 - m, it["cy"] + fy0 / 2 + m,
                    TAB["top"], z0]
        slots.append(dict(key=it["key"], step=it["step"], name=it["name"], part_indices=sorted({i for i, _ in it["members"]}),
                          solids=[[i, s] for i, s in it["members"] if s is not None] or None, category=it["category"],
                          T=T.tolist(), bbox=[round(float(v), 2) for v in bb], support=it["support"], nest=nest,
                          side=it["side"], actor=it["actor"], tool=it["tool"], mass_kg=it["mass_kg"],
                          two_arm=it.get("do") == "dual", heavy=it["support"] == "pallet", coil=it["coil"],
                          stock=stock, kinds=it["kinds"], label=it["name"][:40]))
    for p in pallets:
        p.pop("used", None)
    return slots + bin_slots, zones, pallets


_SLOTS = None


def slots(parts=None):
    """Every slot (cached under /tmp/robotbuild/cache by the model's and the sequence's source hash)."""
    global _SLOTS
    if _SLOTS is None:
        CACHE.mkdir(parents=True, exist_ok=True)
        f = CACHE / f"kit-slots-{_hash()}.json"
        if f.exists():
            d = json.loads(f.read_text())
        else:
            s, z, p = layout(parts)
            d = dict(slots=s, zones=z, pallets=p)
            f.write_text(json.dumps(d))
        _SLOTS = d
    return _SLOTS["slots"]


def zones():
    slots()
    return _SLOTS["zones"]


def pallets():
    slots()
    return _SLOTS["pallets"]


def slot_for(step_id):
    return [s for s in slots() if s["step"] == step_id]


def slot_of_part(i):
    return [s for s in slots() if i in s["part_indices"]]


# ------------------------------------------------------------------------------------------------ meshes
def _box(x0, x1, y0, y1, z0, z1):
    import pyvista as pv
    return pv.Box(bounds=(x0, x1, y0, y1, z0, z1)).triangulate()


def _frame(b, wall, h, z0):
    """An open rectangular rim (four walls) round footprint b = (x0, x1, y0, y1)."""
    import pyvista as pv
    x0, x1, y0, y1 = b
    ws = [_box(x0, x1, y0, y0 + wall, z0, z0 + h), _box(x0, x1, y1 - wall, y1, z0, z0 + h),
          _box(x0, x0 + wall, y0, y1, z0, z0 + h), _box(x1 - wall, x1, y0, y1, z0, z0 + h)]
    return pv.merge(ws)


def table_meshes():
    """[(name, mesh, color)] of the table, its legs, the nests, trays, bins and the pallets."""
    import pyvista as pv
    t = TAB
    out = [("long table top", _box(t["x0"], t["x1"], t["y0"], t["y1"], t["top"] - t["t"], t["top"]), common.COL["table"])]
    legs = []
    for x in np.arange(t["x0"] + 60.0, t["x1"], 1500.0).tolist() + [t["x1"] - 60.0]:
        for y in (t["y0"] + 60.0, t["y1"] - 60.0):
            legs.append(_box(x - 25, x + 25, y - 25, y + 25, 0.0, t["top"] - t["t"]))
    out.append(("long table legs", pv.merge(legs), common.COL["table_leg"]))
    rails = [_box(t["x0"] + 40, t["x1"] - 40, y - 15, y + 15, 180.0, 220.0) for y in (t["y0"] + 60.0, t["y1"] - 60.0)]
    out.append(("long table stretchers", pv.merge(rails), common.COL["table_leg"]))
    nests, trays = [], []
    for s in slots():
        if s["support"] == "riser" and s["nest"]:
            n = s["nest"]
            nests.append(_box(n[0], n[1], n[2], n[3], n[4], n[5]))
        elif s["support"] == "nest" and s["nest"]:
            n = s["nest"]
            nests.append(_box(n[0], n[1], n[2], n[3], n[4], n[5]))
            ib = s["bbox"]
            nests.append(_frame((ib[0] - RIM_W - 2.0, ib[1] + RIM_W + 2.0, ib[2] - RIM_W - 2.0, ib[3] + RIM_W + 2.0), RIM_W, RIM_H, n[5]))
        elif s["support"] == "tray" and s["nest"]:
            n = s["nest"]
            trays.append(_box(n[0], n[1], n[2], n[3], n[4], n[5]))
            trays.append(_frame((n[0], n[1], n[2], n[3]), TRAY_WALL, TRAY_H, n[5]))
        elif s["support"] == "bin":
            b = s["bbox"]
            trays.append(_box(b[0], b[1], b[2], b[3], b[4], b[4] + TRAY_T))
            trays.append(_frame((b[0], b[1], b[2], b[3]), TRAY_WALL, b[5] - b[4], b[4] + TRAY_T))
    if nests:
        out.append(("kitting nests", pv.merge(nests), NEST_COL))
    if trays:
        out.append(("trays and bins", pv.merge(trays), TRAY_COL))
    pal = []
    for p in pallets():
        for k in range(3):       # three deck boards over three blocks: drawn as boards and runners
            y = p["y0"] + k * (PALLET["W"] - 100.0) / 2
            pal.append(_box(p["x0"], p["x1"], y, y + 100.0, 0.0, 100.0))
        for k in range(7):
            x = p["x0"] + k * (PALLET["L"] - 140.0) / 6
            pal.append(_box(x, x + 140.0, p["y0"], p["y1"], 100.0, PALLET["H"]))
    if pal:
        out.append(("pallets", pv.merge(pal), PALLET_COL))
    return out


_MESH = {}


def _tess(shape):
    import render_low as R
    try:
        return R.tess(shape, 0.3, 0.4)
    except Exception:
        return None


def item_meshes(parts=None, mode="finished"):
    """[dict(key, name, mesh, color, part_indices)] for every slot's contents (meshes cached per model hash)."""
    import pyvista as pv
    import render_build as RB
    parts = model() if parts is None else parts
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"kit-meshes-{mode}-{_hash()}.pkl"
    if f.exists():
        raw = pickle.loads(f.read_bytes())
    else:
        raw = []
        for s in slots():
            T = np.asarray(s["T"], float)
            if s["support"] == "bin":
                try:
                    pile = RB.fastener_pile(parts[s["part_indices"][0]])
                    # all of this part number's screws: one pile of `count`
                    import fasteners as FS
                    import cadquery as cq
                    shp = FS.shape(s["pn"])
                    bb = shp.BoundingBox()
                    sp = max(bb.xlen, bb.ylen) + 3.0
                    n = s["count"]
                    cols = max(1, math.ceil(math.sqrt(n)))
                    b = s["bbox"]
                    pile = cq.Compound.makeCompound([shp.translate(cq.Vector(b[0] + 8.0 + sp / 2 + (k % cols) * sp,
                                                                              b[2] + 8.0 + sp / 2 + (k // cols) * sp,
                                                                              b[4] + TRAY_T - bb.zmin)) for k in range(n)])
                    m = _tess(pile)
                except Exception:
                    m = None
                if m is not None:
                    raw.append((s["key"], s["name"], m, "#a9b1b9", s["part_indices"]))
                continue
            if mode == "stock" and s["stock"]:
                for bl in s["stock"]:
                    p = parts[bl["part"]]
                    shp = p.shape if bl["solid"] is None else p.shape.Solids()[bl["solid"]]

                    class _P:
                        pass
                    q = _P()
                    q.shape, q.name, q.mat = shp, p.name, p.mat
                    kd = RB.kind(p)
                    b_shape = RB._blank(shp, p.name)[0] if kd == "stock" else RB.sheet_blank(q)
                    m = _tess(b_shape)
                    if m is not None:
                        raw.append((s["key"], f"{s['name']} (blank: {bl['label']})", m.transform(np.asarray(bl["T"], float), inplace=False),
                                    bl["color"], [bl["part"]]))
                if all(k in ("stock", "sheet") for k in s["kinds"]):
                    continue
            for i in s["part_indices"]:
                if mode == "stock" and s["stock"] and RB.kind(parts[i]) in ("stock", "sheet"):
                    continue
                p = parts[i]
                if s.get("coil"):
                    c = s["coil"]
                    m = RB.coil(c["ring"], c["r"], c["turns"], c["pitch"])
                    b = s["bbox"]
                    m = m.translate((0.5 * (b[0] + b[1]), 0.5 * (b[2] + b[3]), b[4] + c["r"]), inplace=False)
                    raw.append((s["key"], s["name"], m, p.color, [i]))
                    continue
                sols = [x for x in (s["solids"] or []) if x[0] == i]
                shp = p.shape if not sols else (p.shape.Solids()[sols[0][1]] if len(sols) == 1 else
                                                __import__("cadquery").Compound.makeCompound([p.shape.Solids()[x[1]] for x in sols]))
                m = _tess(shp)
                if m is None:
                    continue
                raw.append((s["key"], p.name, m.transform(T, inplace=False), p.color, [i]))
        f.write_bytes(pickle.dumps(raw))
    return [dict(key=k, name=n, mesh=m, color=c, part_indices=pi) for k, n, m, c, pi in raw]


def meshes(parts=None, mode="finished"):
    """Everything on and beside the table: [dict(key, name, mesh, color)]; mode "finished" or "stock" (before machining)."""
    out = [dict(key="table", name=n, mesh=m, color=c, part_indices=[]) for n, m, c in table_meshes()]
    return out + item_meshes(parts, mode)


def summary():
    s = slots()
    by = {}
    for x in s:
        by.setdefault((x["category"], x["support"]), 0)
        by[(x["category"], x["support"])] += 1
    return by


if __name__ == "__main__":
    import time
    t0 = time.time()
    ss = slots()
    print(f"{len(ss)} slots in {time.time() - t0:.0f} s")
    for z in zones():
        print(f"  {z['category']:7s} x {z['x0']:7.0f} - {z['x1']:7.0f}  ({(z['x1'] - z['x0']) / 1000:.2f} m)")
    print("pallets:", [(p["key"], p["items"]) for p in pallets()])
    for k, v in sorted(summary().items()):
        print(" ", k, v)
    over = [x["key"] for x in ss if x["support"] != "pallet" and (x["bbox"][1] > TAB["x1"] or x["bbox"][0] < TAB["x0"])]
    print("off the table:", over)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    keep = ("key", "step", "name", "part_indices", "solids", "category", "T", "bbox", "support", "side", "actor", "tool",
            "mass_kg", "two_arm", "heavy", "label")
    OUT_JSON.write_text(json.dumps(dict(note="kit_table.py: every item's slot on common.LONG_TABLE (hall frame, mm); T maps the "
                                             "item's machine-frame geometry onto the table", table=TAB, zones=zones(),
                                        pallets=pallets(),
                                        slots=[{k: (np.round(np.asarray(x[k]), 2).tolist() if k == "T" else x[k]) for k in keep}
                                               for x in ss]), indent=0))
    print("wrote", OUT_JSON)
