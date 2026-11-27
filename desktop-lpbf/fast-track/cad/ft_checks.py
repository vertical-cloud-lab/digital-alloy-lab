"""Checks on the fast-track model (ft_model.py), state by state (round 2, 2026-11-27).

1. Interference: every pair of parts whose bounding boxes overlap is intersected with OpenCascade's exact boolean;
   shared volume above VOL_TOL is a clash unless the pair is a designed contact (JOINTS, reported separately).
   Run for the five states and for FT-1 with the Thorlabs piston stage.
2. Beam: the scanned-beam envelope (an oblique cone from the scan mirrors on the lens axis at (0, -30) to the Ø40
   field) against every part, with the clearance to the nearest ones.
3. Travel: the hopper-blade swept over the X-LSM100B's full 101.6 mm and the plate over its 20 mm stroke (exact
   booleans at sampled positions), the parks the hopper needs, the gaps at the ends of the stroke.
4. Mesh sweep (python-fcl, after PR 266's scene_audit.py): each moving group tessellated once and moved in fine steps
   (recoater 2.5 mm, piston 1 mm, the box door 1 deg about its hinge) against every static part's BVH mesh: contacts
   and the smallest distance per pair.
5. Fit: the deck through the box's door opening and the cube's face opening (an estimate), the stages that were
   rejected (measured lengths), rod lengths, the window's height and irradiance, the camera and lights.
6. Sight lines: rays from points on the plate to the layer camera's pupil and to each raking light (trimesh), with
   the hopper parked at either end; the camera's resolution and depth of field.
7. Gas: the enclosure's gas volume measured from the model, the purge it implies, and the air temperature rise.

Run:  python desktop-lpbf/fast-track/cad/ft_checks.py     # writes out/checks.json and out/checks.md
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys
import time

import cadquery as cq
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ft_model as M  # noqa: E402
import ft_vendor as VEN  # noqa: E402

OUT = HERE / "out"
VOL_TOL = 0.5      # mm3
P = M.P

JOINTS = [
    ("Gantry uprights", "Gantry cross-beam", "T-slot joint"),
    ("Gantry uprights", "T-slot base", "uprights stand on the support rail"),
    ("Process fibre", "Fibre bend restrictor", "fibre in its bend restrictor"),
    ("Fibre bend restrictor", "IPG YLR", "restrictor on the laser's front panel"),
    ("Process fibre", "Collimator", "fibre connector in the collimator"),
    ("Collimator", "input-mirror block", "collimator in the block's input port"),
    ("input turret", "hurrySCAN 25", "turret on the entrance face"),
    ("input turret", "input-mirror block", "block on the turret"),
    ("input turret", "Scan-head flange plate", "turret through the flange plate"),
    ("Photodiode branch", "input-mirror block", "tube on the block's back port"),
    ("LINOS", "hurrySCAN 25", "lens nose screwed into the head (M85 x 1)"),
    ("Scan-head flange plate", "hurrySCAN 25", "flange on the entrance face"),
    ("Flange-to-beam angle brackets", "Scan-head flange plate", "bolted"),
    ("Flange-to-beam angle brackets", "Gantry cross-beam", "bolted"),
    ("Head cables", "hurrySCAN 25", "plugs on the side face"),
    ("Argon feed tube", "Slot nozzle", "tube fitting in the nozzle's feed boss"),
    ("Argon feed tube", "Saginaw", "bulkhead fitting through the box wall"),
    ("Exhaust hose", "Saginaw", "bulkhead fitting through the box wall"),
    ("Exhaust hose", "Exhaust collector", "hose on the collector's outlet"),
    ("Vibration motor", "Carriage bracket and arm", "motor clamped on the arm"),
    ("Plate heaters", "Heater plate", "heaters in their holes"),
    ("Well-block heaters", "Well block", "heaters in their holes"),
    ("Fibreglass rope wiper", "Heater plate", "rope in its groove"),
    ("Fibreglass rope wiper", "Well block", "rope compressed against the bore: the wiper"),
    ("Piston rod", "Heater plate", "rod in its socket"),
    ("Piston rod", "Rod-end block", "rod in the clamp"),
    ("Piston rod", "FT-0 rod collar", "rod in the collar"),
    ("Lead pigtail", "Potted lead plug", "wires leave the plug"),
    ("Lead pigtail", "Lead terminal block", "wires in the terminal block"),
    ("Lead pigtail", "Rod-end block", "pigtail in the lead pocket"),
    ("Lead pigtail", "FT-0 lead terminal bracket", "pigtail through the bracket"),
    ("Lead pigtail", "Piston rod", "wires leave the rod's end"),
    ("Heater and TC cable", "Lead terminal block", "cable plugged in"),
    ("Lead terminal block", "Rod-end block", "terminal block screwed on"),
    ("Lead terminal block", "FT-0 lead terminal bracket", "terminal block screwed on"),
    ("Dump water lines", "Water-cooled beam dump", "hose on the dump"),
    ("Dump water lines", "Saginaw", "lines through a cable gland"),
    ("KF-25 pump hose", "KF-25 ports", "hose on the pump port"),
    ("KF-25 pump hose", "Rotary-vane pump", "hose on the pump inlet"),
    ("Argon feed tube", "Cube left plate", "bulkhead fitting"),
    ("Exhaust hose", "Cube right plate", "bulkhead fitting"),
    ("Quarter-turn latch", "Saginaw", "latch cam behind the rim's lip"),
    ("Quarter-turn latch", "Box door", "latch through the door"),
    ("Quarter-turn latch", "Poured-in-place door gasket", "latch inside the gasket line"),
    ("Concealed hinges", "Saginaw", "hinge on the body"),
    ("Concealed hinges", "Box door", "hinge on the door"),
    ("Concealed hinges", "Poured-in-place door gasket", "hinge arm under the lip"),
    ("Panel studs", "Saginaw", "studs welded to the floor"),
    ("Deck clamps", "Panel studs", "clamp on the stud"),
    ("Stud nuts", "Panel studs", "nut on the stud"),
    ("IP68 cable glands", "Recoater M8", "cable through the gland"),
    ("IP68 cable glands", "Well-block heater and TC leads", "leads through the gland"),
    ("IP68 cable glands", "Saginaw", "gland in the back wall"),
    ("Recoater M8", "Zaber X-LSM100B", "plug on the stage's connector"),
    ("Recoater M8", "KF-25 ports", "cable on the feedthrough"),
    ("Well-block heater and TC leads", "Well-block heaters", "leads from the heaters"),
    ("Well-block heater and TC leads", "Well block", "leads from the heaters"),
    ("Well-block heater and TC leads", "KF-25 ports", "leads on the feedthrough"),
    ("Plate thermocouple", "Heater plate", "probe in its hole"),
    ("Well-block thermocouple", "Well block", "probe in its hole"),
    ("Box-air thermocouple", "Saginaw", "compression fitting in the back wall"),
    ("Surface thermocouples", "Beam tube", "patch on the tube"),
    ("Surface thermocouples", "Window ring", "patch on the ring"),
    ("Camera port ring", "Box door", "ring on the door"),
    ("Camera port ring", "Cube top plate", "ring on the plate"),
    ("Camera port window", "Camera port ring", "window in its ring"),
    ("Layer camera", "Camera post", "clamp on the camera's mount ring"),
    ("Camera post", "Box door", "foot on the door"),
    ("Camera post", "Cube top plate", "foot on the plate"),
    ("Light port ring", "Saginaw", "ring on the wall"),
    ("Light port ring", "Cube left plate", "ring on the plate"),
    ("Light port ring", "Cube front plate", "ring on the door"),
    ("AE sensor", "Rod-end block", "sensor clamped on the block's face"),
    ("AE cable", "AE sensor", "cable on the sensor"),
    ("Rod clamp screw", "Rod-end block", "screw in the clamp"),
    ("X-VSR20A platform", "Zaber X-VSR20A", "the stage's own lift"),
    ("Rod-end block", "X-VSR20A platform", "block bolted on the platform"),
    ("Piston-stage bracket plate", "Zaber X-VSR20A", "stage on the riser"),
    ("X-VSR20A M8 cable", "Zaber X-VSR20A", "plug on the stage's connector"),
    ("Bracket-plate screws", "Piston-stage bracket plate", "screws"),
    ("Bracket-plate screws", "T-slot base", "screws into T-nuts"),
    ("Gland screws", "Rod gland plate", "screws"),
    ("Deck screws", "Deck plate", "screws"),
    ("Deck screws", "Cube bottom plate", "screws in blind tapped holes"),
    ("Window-stack screws", "Window retaining flange", "screws"),
    ("Beam tube centre section", "Window retaining flange", "section sits on the flange"),
    ("Beam tube centre section", "Beam-tube lens collar", "section in the collar's socket"),
    ("Beam-tube lens collar", "LINOS", "collar clamped on the lens"),
    ("Beam-tube interlock", "Beam-tube lens collar", "switch on the collar"),
    ("Cover-slide drop tube", "Cube top plate", "tube bolted under the plate"),
    ("Cover-slide drop tube", "Cover-slide holder", "holder on the tube"),
    ("Cover-slide holder", "Inner clamp ring", "holder hangs from the ring"),
    ("MTS50 L-arm", "MTS50 carriage", "arm bolted on the carriage"),
    ("MTS50 L-arm", "Rod-end block", "block on the arm"),
    ("MTS50 tower plate", "Thorlabs MTS50", "stage bolted on the tower"),
    ("MTS50 carriage", "Thorlabs MTS50", "the stage's own carriage"),
    ("X-LSM carriage", "Zaber X-LSM100B", "the stage's own carriage"),
    ("Carriage bracket and arm", "X-LSM carriage", "bracket bolted on the carriage"),
    ("Head cables and hoses", "hurrySCAN", "plugs"),
]


def joint(a, b):
    for x, y, why in JOINTS:
        if (x in a and y in b) or (x in b and y in a):
            return why
    return None


def bb_overlap(a, b, pad=0.0):
    return not (a.xmax + pad < b.xmin or b.xmax + pad < a.xmin or a.ymax + pad < b.ymin or b.ymax + pad < a.ymin
                or a.zmax + pad < b.zmin or b.zmax + pad < a.zmin)


def common_volume(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:          # noqa: BLE001  (an OCC failure is reported, not hidden)
        return float("nan")


def interference(parts):
    clashes, contacts = [], []
    bbs = [p.shape.BoundingBox() for p in parts]
    for i, j in itertools.combinations(range(len(parts)), 2):
        if not bb_overlap(bbs[i], bbs[j]):
            continue
        a, b = parts[i], parts[j]
        v = common_volume(a.shape, b.shape)
        if not (v > VOL_TOL or v != v):
            continue
        why = joint(a.name, b.name)
        row = dict(a=a.name, b=b.name, volume_mm3=round(v, 1) if v == v else "OCC failed")
        if why:
            contacts.append({**row, "why": why})
        else:
            clashes.append(row)
    return clashes, contacts


BEAM_OK = ("Window, ", "Cover slide", "LINOS", "Camera port window")


def beam_check(state, parts):
    cone = M.beam_cone(state, 0.0, P["lens_wd"])
    cbb = cone.BoundingBox()
    hits, near = [], []
    for p in parts:
        bb = p.shape.BoundingBox()
        if not bb_overlap(cbb, bb, pad=25.0) or any(k in p.name for k in BEAM_OK):
            continue
        v = common_volume(cone, p.shape)
        if v > VOL_TOL and not p.name.startswith(("Substrate", "Well block")):
            hits.append(dict(part=p.name, volume_mm3=round(v, 1)))
        else:
            try:
                d = cone.distance(p.shape)
            except Exception:  # noqa: BLE001
                d = float("nan")
            near.append(dict(part=p.name, clearance_mm=round(d, 2)))
    near.sort(key=lambda r: r["clearance_mm"])
    return hits, near


def aperture_check(state):
    """Clear radius left around the scanned-beam envelope at the window, the cover slide and the beam tube."""
    L = M.levels(state)
    dz = L["dz"]
    out = {}
    wx, wy = M.window_centre(state)
    z_w0 = L["roof_out"] + 2 - dz
    for name, z, (cx, cy), r_open in (
            ("window (ring ledge / flange Ø44)", z_w0, (wx, wy), 22.0),
            ("window top", z_w0 + P["window_t"], (wx, wy), 22.0),
            ("cover slide holder (Ø44)", P["cs_z"], P["cs_c"], P["cs_id"] / 2),
            ("beam tube lower spigot (Ø50)", L["roof_out"] + 16 - dz, M.tube_centre(state), P["tube_spigot"][0] - 1.5),
            ("beam tube upper spigot (Ø50)", L["lens_bot"] - 10 - P["tube_spigot"][1] - dz, M.tube_centre(state),
             P["tube_spigot"][0] - 1.5)):
        bc = M.beam_centre(z)
        need = math.hypot(bc[0] - cx, bc[1] - cy) + M.beam_radius(z)
        out[name] = dict(height_above_bed_mm=round(z, 1), envelope_r_mm=round(M.beam_radius(z), 2),
                         offset_mm=round(math.hypot(bc[0] - cx, bc[1] - cy), 2), opening_r_mm=r_open,
                         margin_mm=round(r_open - need, 2))
    return out


def recoater_sweep(state, n=13):
    """Move the hopper over the stage's full travel (exact booleans at n positions): clashes and the smallest gaps."""
    half = P["rc_travel"] / 2
    statics = [p for p in M.build(state, hx=P["rc_x0"]) if p.group != "recoater"]
    gaps, clashes = {}, []
    sbbs = [s.shape.BoundingBox() for s in statics]
    for k in range(n):
        hx = P["rc_x0"] - half + 2 * half * k / (n - 1)
        movers = [p for p in M.build(state, hx=hx) if p.group == "recoater"]
        for m_ in movers:
            mbb = m_.shape.BoundingBox()
            for s, sbb in zip(statics, sbbs):
                if not bb_overlap(mbb, sbb, pad=15.0):
                    continue
                if joint(m_.name, s.name):
                    continue
                if ("Well block" in s.name or "Substrate" in s.name) and ("cord" in m_.name or "Hopper" in m_.name):
                    v = common_volume(m_.shape, s.shape)
                    if v > VOL_TOL:
                        clashes.append(dict(hx=round(hx, 1), mover=m_.name, part=s.name, volume_mm3=round(v, 1)))
                    continue
                v = common_volume(m_.shape, s.shape)
                if v > VOL_TOL:
                    clashes.append(dict(hx=round(hx, 1), mover=m_.name, part=s.name, volume_mm3=round(v, 1)))
                    continue
                d = m_.shape.distance(s.shape)
                key = (m_.name, s.name)
                if key not in gaps or d < gaps[key][0]:
                    gaps[key] = (d, hx)
    rows = [dict(mover=a, part=b, min_gap_mm=round(d, 2), at_hx=round(x, 1)) for (a, b), (d, x) in gaps.items()]
    rows.sort(key=lambda r: r["min_gap_mm"])
    return clashes, rows


def travel_needed():
    """Hopper centre positions at the two parks, from the (offset) beam envelope and the overflow slot."""
    hl = P["hopper"][0]
    margin = 3.0
    z_top = P["hopper"][2] + 13.0                      # vibrator top above the bed
    r = M.beam_radius(z_top)
    cx = M.beam_centre(z_top)[0]
    left = cx - (r + margin + max(hl / 2, 5.0))
    blade_x = lambda hx: hx - hl / 2 - 2.0             # noqa: E731  cord centre
    right = max(cx + r + margin + hl / 2 + 4.0, P["ovf_x"][0] + 1.5 - blade_x(0.0))
    lo, hi = P["rc_x0"] - P["rc_travel"] / 2, P["rc_x0"] + P["rc_travel"] / 2
    return dict(beam_r_at_hopper_top_mm=round(r, 2), left_park=round(left, 1), right_park=round(right, 1),
                travel_needed_mm=round(right - left, 1), stage_travel_mm=P["rc_travel"], travel_range=(round(lo, 1), round(hi, 1)),
                spare_left_mm=round(left - lo, 1), spare_right_mm=round(hi - right, 1))


def piston_checks(state, piston="zaber"):
    res = {}
    for pz in (P["pz_bot"], P["pz_top"]):
        parts = M.build(state, pz=pz, piston=piston)
        by = {p.name: p for p in parts}
        movers = [p for p in parts if p.group == "piston"]
        statics = [p for p in parts if p.group != "piston"]
        clash = []
        for m_ in movers:
            mbb = m_.shape.BoundingBox()
            for s in statics:
                if not bb_overlap(mbb, s.shape.BoundingBox()) or joint(m_.name, s.name):
                    continue
                v = common_volume(m_.shape, s.shape)
                if v > VOL_TOL:
                    clash.append(dict(mover=m_.name, part=s.name, volume_mm3=round(v, 1)))
        hp = by["Heater plate Ø39.8 x 28 (MK-04)" if "Heater plate Ø39.8 x 28 (MK-04)" in by else
                [n for n in by if n.startswith("Heater plate")][0]].shape.BoundingBox()
        deck = by["Deck plate (MK-01)"].shape.BoundingBox()
        blk = by["Rod-end block: clamp, lead pocket, AE face (MK-15)"].shape.BoundingBox()
        gland = by["Rod gland plate, 2 O-rings (MK-07)"].shape.BoundingBox()
        res[f"pz={pz:+.0f}"] = dict(clashes=clash, plate_bottom_above_deck_mm=round(hp.zmin - deck.zmax, 2),
                                    block_top_below_gland_mm=round(gland.zmin - blk.zmax, 2),
                                    rope_inside_bore=bool(pz - P["sub_t"] - 7 - P["rope"] > -P["well"][2]))
    rod = [p for p in M.build(state, piston=piston) if p.name.startswith("Piston rod")][0].shape.BoundingBox()
    res["rod_length_mm"] = round(rod.zlen, 1)
    res["stage_stroke_used_mm"] = P["pz_top"] - P["pz_bot"]
    res["stage_travel_mm"] = P["vs_travel"] if piston == "zaber" else VEN.MTS["travel"]
    a_rod = math.pi / 4 * (P["rod_od"] / 1000) ** 2
    res["atm_force_on_rod_N"] = round(101325 * a_rod, 1)
    return res


# --------------------------------------------------------------------------------------------------
# Mesh sweep with python-fcl
# --------------------------------------------------------------------------------------------------
def _mesh(shape, tol=0.4):
    vs, ts = shape.tessellate(tol, 0.3)
    if not ts:
        return None
    return np.array([(v.x, v.y, v.z) for v in vs], float), np.array(ts, np.int32)


def _bvh(V_, F_):
    import fcl
    g = fcl.BVHModel()
    g.beginModel(len(V_), len(F_))
    g.addSubModel(np.ascontiguousarray(V_, np.float64), np.ascontiguousarray(F_, np.int32))
    g.endModel()
    return g


def _rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], float)


def fcl_sweep(statics, movers, poses, label, skip=lambda m, s: False):
    """movers: list of Part at the reference pose; poses: list of (value, R 3x3, t 3) applied to the movers. Returns
    per-pair minimum distance and the poses where a pair is in contact (excluding designed contacts)."""
    import fcl
    st = []
    for s in statics:
        m = _mesh(s.shape)
        if m is None:
            continue
        st.append((s, fcl.CollisionObject(_bvh(*m), fcl.Transform()), m[0].min(0), m[0].max(0)))
    mv = []
    for p in movers:
        m = _mesh(p.shape)
        if m is not None:
            mv.append((p, _bvh(*m), m[0]))
    best, hits = {}, []
    for val, R, t in poses:
        tf = fcl.Transform(R, t)
        for p, g, Vm in mv:
            Vw = Vm @ R.T + t
            lo, hi = Vw.min(0) - 30.0, Vw.max(0) + 30.0
            o = fcl.CollisionObject(g, tf)
            for s, so, slo, shi in st:
                if np.any(hi < slo) or np.any(shi < lo) or skip(p, s) or joint(p.name, s.name):
                    continue
                req, res = fcl.CollisionRequest(), fcl.CollisionResult()
                if fcl.collide(o, so, req, res):
                    hits.append(dict(pose=round(val, 2), mover=p.name, part=s.name))
                    key = (p.name, s.name)
                    best[key] = (0.0, val)
                    continue
                d = fcl.distance(o, so, fcl.DistanceRequest(), fcl.DistanceResult())
                key = (p.name, s.name)
                if key not in best or d < best[key][0]:
                    best[key] = (d, val)
    rows = [dict(sweep=label, mover=a, part=b, min_dist_mm=round(d, 2), at=round(v, 2)) for (a, b), (d, v) in best.items()]
    rows.sort(key=lambda r: r["min_dist_mm"])
    return rows, hits


def mesh_sweeps(state):
    """Recoater over its full travel (2.5 mm steps), piston over its stroke (1 mm), with python-fcl."""
    out = {}
    half = P["rc_travel"] / 2
    ref = M.build(state, hx=P["rc_x0"], pz=0.0)
    statics = [p for p in ref if p.group != "recoater"]
    movers = [p for p in ref if p.group == "recoater"]
    poses = [(dx, np.eye(3), np.array([dx, 0.0, 0.0])) for dx in np.arange(-half, half + 1e-6, 2.5)]
    skip_r = lambda m, s: ("cord" in m.name and ("Well block" in s.name or "Substrate" in s.name))  # noqa: E731
    rows, hits = fcl_sweep(statics, movers, poses, "recoater", skip_r)
    out["recoater"] = dict(poses=len(poses), contacts=hits[:20], n_contacts=len(hits), nearest=rows[:10])
    ref = M.build(state, pz=0.0)                    # hopper parked while the plate moves
    statics = [p for p in ref if p.group != "piston"]
    movers = [p for p in ref if p.group == "piston"]
    poses = [(dz_, np.eye(3), np.array([0.0, 0.0, dz_])) for dz_ in np.arange(P["pz_bot"], P["pz_top"] + 1e-6, 1.0)]
    # the stage's own lift: its platform is a mover; the fixed body is static (they slide by design)
    rows, hits = fcl_sweep(statics, movers, poses, "piston")
    out["piston"] = dict(poses=len(poses), contacts=hits[:20], n_contacts=len(hits), nearest=rows[:10])
    return out


def tube_removal(state="FT-1", travel=60.0, step=2.0):
    """The beam tube's centre section split in the y-z plane through its axis; each half-shell slid straight out
    sideways (-x, +x) with no lift against every fixed part (python-fcl), 0.2 mm off its end faces so that sliding on
    the flange is not counted: contacts and the nearest parts. The spigots sit inside the bore, so they must not hold
    a half-shell."""
    parts = M.build(state)
    sec = [p for p in parts if p.name.startswith("Beam tube centre section")][0]
    tx, ty = M.tube_centre(state)
    ax = P["tube_split"]["cube" if state == "FT-1V" else "box"]
    bb = sec.shape.BoundingBox()
    statics = [p for p in parts if p is not sec and not p.name.startswith(("Surface thermocouples", "Bench top"))]
    out = {"slide_axis": ax}
    for sgn, lab in ((-1, f"-{ax} half-shell"), (1, f"+{ax} half-shell")):
        lo, hi = (bb.xmin - 1, bb.xmax + 1) if ax == "x" else (bb.ymin - 1, bb.ymax + 1)
        c = tx if ax == "x" else ty
        a0, a1 = (c, hi) if sgn > 0 else (lo, c)
        cut = (M.box(a0, a1, bb.ymin - 1, bb.ymax + 1, bb.zmin + 0.2, bb.zmax - 0.2) if ax == "x" else
               M.box(bb.xmin - 1, bb.xmax + 1, a0, a1, bb.zmin + 0.2, bb.zmax - 0.2))
        half = sec.shape.intersect(cut)
        mover = M.Part(f"Tube section {lab}", half, sec.color)
        vec = np.array([1.0, 0.0, 0.0]) if ax == "x" else np.array([0.0, 1.0, 0.0])
        poses = [(d, np.eye(3), sgn * d * vec) for d in np.arange(0.0, travel + 1e-6, step)]
        rows, hits = fcl_sweep(statics, [mover], poses, "tube")
        out[lab] = dict(poses=len(poses), travel_mm=travel, n_contacts=len(hits), contacts=hits[:6],
                        nearest=[{k: v for k, v in r.items() if k != "sweep"} for r in rows[:4]])
    out["section_length_mm"] = round(bb.zlen, 1)
    return out


def removal_numbers():
    """What has to move before the box comes off the frame (FT-1 -> FT-1V), from the model's levels."""
    L = M.levels("FT-1")
    parts = M.build("FT-1", pz=P["pz_top"])
    rod = [p for p in parts if p.name.startswith("Piston rod")][0].shape.BoundingBox()
    blk = [p for p in parts if p.name.startswith("Rod-end block")][0].shape.BoundingBox()
    gl = [p for p in parts if p.name.startswith("Rod gland plate")][0].shape.BoundingBox()
    rail_top = L["under"]
    Lc = M.levels("FT-1V")
    return dict(gland_bottom_below_rail_tops_mm=round(rail_top - gl.zmin, 1),
                rod_in_rod_end_block_mm=round(blk.zmax - rod.zmin, 1),
                rod_length_box_mm=round(rod.zlen, 1), rod_length_cube_mm=round(rod.zlen + Lc["dz"], 1),
                rod_bottom_below_block_top_at_pz_top_mm=round(0.0 - rod.zmin, 1),
                lift_to_free_rod_from_bore_mm=round(0.0 - rod.zmin + 2.0, 1),
                block_top_below_gland_at_pz_top_mm=round(gl.zmin - blk.zmax, 1),
                block_top_below_gland_at_pz_bot_mm=round(gl.zmin - blk.zmax + (P["pz_top"] - P["pz_bot"]), 1))


DOOR_GROUP = M.DOOR_GROUP


def door_swing(state="FT-1", max_deg=90, step=1.0, camera=True):
    """The box door (lid) and everything on it rotated about the concealed hinges' axis (est.: the door's back top
    edge), with the beam tube's centre section removed; the first angle at which anything on the door touches a fixed
    part, and what. camera=False: the layer camera unclipped from its post first."""
    parts = M.build(state)
    y_h, z_h = M.door_hinge(state)
    door = [p for p in parts if p.name.startswith(DOOR_GROUP) and (camera or not p.name.startswith("Layer camera"))]
    skip_names = ("Beam tube centre section", "Surface thermocouples", "Concealed hinges", "Poured-in-place", "Saginaw",
                  "Coded lid switches", "Bench top", "Layer camera")
    statics = [p for p in parts if p not in door and not p.name.startswith(skip_names)]
    pivot = np.array([0.0, y_h, z_h])
    poses = []
    for k in range(0, int(max_deg / step) + 1):
        R = _rot_x(-math.radians(k * step))
        poses.append((k * step, R, pivot - R @ pivot))
    rows, hits = fcl_sweep(statics, door, poses, "door")
    first = None
    if hits:
        a0 = min(h["pose"] for h in hits)
        first = dict(angle_deg=float(a0), contacts=[h for h in hits if h["pose"] == a0][:6])
    last = (first["angle_deg"] - step) if first else max_deg
    return dict(hinge_axis_y=round(y_h, 1), hinge_axis_z=round(z_h, 1), camera_on_door=camera, first_contact=first,
                last_free_deg=last, front_edge_rise_mm=round(VEN.SAG["door"][1] * math.sin(math.radians(last)), 1))


# --------------------------------------------------------------------------------------------------
# Sight lines (trimesh ray casting)
# --------------------------------------------------------------------------------------------------
def _scene_mesh(parts, exclude):
    import trimesh
    ms = []
    for p in parts:
        if any(k in p.name for k in exclude):
            continue
        m = _mesh(p.shape, 0.6)
        if m is not None:
            ms.append(trimesh.Trimesh(vertices=m[0], faces=m[1], process=False))
    return trimesh.util.concatenate(ms)


def _plate_points(n_r=6, n_t=24, r=19.0):
    pts = [(0.0, 0.0)]
    for i in range(1, n_r + 1):
        rr = r * i / n_r
        for j in range(int(n_t * i / n_r) + 4):
            a = 2 * math.pi * j / (int(n_t * i / n_r) + 4)
            pts.append((rr * math.cos(a), rr * math.sin(a)))
    return pts


def _visible(mesh, pts, target):
    origins = np.array(pts, float)
    d = np.array(target, float) - origins
    L_ = np.linalg.norm(d, axis=1)
    dirs = d / L_[:, None]
    origins = origins + dirs * 0.3
    locs, idx, _ = mesh.ray.intersects_location(origins, dirs, multiple_hits=False)
    blocked = np.zeros(len(pts), bool)
    for loc, i in zip(locs, idx):
        if np.linalg.norm(loc - origins[i]) < L_[i] - 1.0:
            blocked[i] = True
    return 1.0 - blocked.mean(), blocked


def sight_lines(state):
    """Fraction of the plate (Ø38 sampled) the camera sees and each light reaches, with the hopper at both parks."""
    out = {}
    L = M.levels(state)
    zb = L["dz"]
    tr = travel_needed()
    cam = M.camera_geometry(state)
    pupil = tuple(cam["W"][i] + 30.0 * cam["u"][i] for i in range(3))   # lens front ~30 mm along the axis
    lights = M.light_geometry(state)
    pts = [(x, y, zb) for (x, y) in _plate_points()]
    for park, hx in (("right park", P["hx_default"]), ("left park", tr["left_park"] - 2.0)):
        parts = M.build(state, hx=hx)
        mesh = _scene_mesh(parts, ("Window, ", "Cover slide", "Camera port window", "Substrate", "Layer camera",
                                   "Raking light", "Light port ring", "Bench top"))
        f_cam, _ = _visible(mesh, pts, pupil)
        row = dict(camera_sees_pct=round(100 * f_cam, 1))
        for k, lg in lights.items():
            src = tuple(lg["port_in"][i] + 30.0 * lg["u"][i] for i in range(3))
            f, _ = _visible(mesh, pts, src)
            row[f"{k}_lights_pct"] = round(100 * f, 1)
        out[f"hopper at the {park} (hx {hx:.1f})"] = row
    return out


def camera_numbers(state):
    c = M.camera_geometry(state)
    N, coc = 2.8, 2 * 1.55e-3                       # f/2.8, two pixels
    m = c["m"]
    dof = 2 * N * coc * (1 + m) / m ** 2
    depth = 40.0 * math.sin(math.radians(c["tilt_deg"]))
    airy = 1.22 * 0.55e-3 * N / m * 1000             # Rayleigh radius at 550 nm, referred to the plate, um
    return dict(lens_f_mm=c["f_mm"], tilt_deg=round(c["tilt_deg"], 1), distance_mm=round(c["dist_mm"], 1),
                um_per_px_across=round(c["um_px_across"], 1), um_per_px_along=round(c["um_px_along"], 1),
                field_mm=[round(v, 1) for v in c["field_mm"]], scheimpflug_deg=round(c["scheimpflug_deg"], 2),
                dof_mm_f2_8=round(dof, 2), plate_depth_range_mm=round(depth, 1), rayleigh_um_f2_8=round(airy, 1),
                video_2028x1520_40fps_um_px=round(c["um_px_across"] * 2, 1))


# --------------------------------------------------------------------------------------------------
# Fit, gas, purge, heat
# --------------------------------------------------------------------------------------------------
def fit_checks():
    L_box, L_cube = M.levels("FT-1"), M.levels("FT-1V")
    ext = VEN.x_lsm100_extent()
    out = dict(deck_mm=P["deck"], box_inside_mm=[round(v, 1) for v in P["box_in"]],
               box_door_opening_mm_est=[round(v, 1) for v in VEN.saginaw_16el1208sslp()["opening"]],
               deck_in_box_margins_mm=[round((P["box_in"][0] - P["deck"][0]) / 2, 1),
                                       round((P["box_in"][1] - P["deck"][1]) / 2, 1)],
               cube_inside_mm=round(P["cube_in"], 1), cube_face_opening_mm_est=P["cube_open"],
               deck_through_opening_margin_mm=round(P["cube_open"] - max(P["deck"]), 1),
               cube_opening_needed_mm=round(max(P["deck"]) + 2.0, 1),
               lesker_bx1212s_inside_mm=304.8, deck_in_lesker_margin_mm=round((304.8 - max(P["deck"])) / 2, 1))
    stages = {"X-LSM100B-E03 (used)": ext[1] - ext[0], "X-LSQ075B-E01 (rejected)": VEN.LSQ["X-LSQ075B-E01"][0],
              "X-LSQ150B-E01 (rejected)": VEN.LSQ["X-LSQ150B-E01"][0]}
    for k, v in stages.items():
        out[f"{k}_length_mm"] = round(v, 2)
        out[f"{k}_fits_deck"] = v <= P["deck"][0]
        out[f"{k}_fits_cube_inside"] = v <= P["cube_in"] - 2 * 5.0
    for name, st in (("box", "FT-1"), ("cube", "FT-1V")):
        parts = M.build(st)
        w = [p for p in parts if p.name.startswith("Window, ")][0].shape.BoundingBox()
        L = M.levels(st)
        h = w.zmin - L["dz"]
        d = P["beam_d"] * h / P["efl"]
        out[f"window_above_bed_{name}_mm"] = round(h, 1)
        out[f"beam_at_window_{name}_mm"] = round(d, 2)
        out[f"window_irradiance_{name}_kW_cm2_at_400W"] = round(400 / (math.pi / 4 * (d / 10) ** 2) / 1000, 1)
        out[f"cover_slide_above_bed_{name}_mm"] = P["cs_z"]
    parts = M.build("FT-1V")
    cas = [p for p in parts if p.sub in ("cassette", "recoater") or p.name.startswith(("Slot nozzle", "Exhaust collector"))]
    top = max(p.shape.BoundingBox().zmax for p in cas)
    out["cassette_height_above_floor_mm"] = round(top - L_cube["floor_top"], 1)
    out["cube_inside_height_mm"] = round(L_cube["roof_in"] - L_cube["floor_top"], 1)
    out["box_inside_height_mm"] = round(L_box["roof_in"] - L_box["floor_top"], 1)
    out["head_top_above_bed_box_mm"] = round(L_box["head_bot"] + P["head"][2], 1)
    out["head_top_above_bed_cube_mm"] = round(L_cube["head_bot"] + P["head"][2] - L_cube["dz"], 1)
    for size, head in (("M3", 6.0), ("M2.5", 5.0), ("M2", 4.0)):
        r = 15.0 + head / 2
        out[f"substrate_{size}_head_outer_r_mm"] = round(r + head / 2, 2)
        out[f"substrate_{size}_fits"] = r + head / 2 <= P["plate_d"] / 2
    out["plate_heater_holes_mm"] = f"2 x Ø{P['heater_hole'][0]} x {P['heater_hole'][1]} deep in a {P['hp_t']} mm plate"
    return out


def inside_volume(state, parts):
    """Gas volume: the enclosure's inside less the parts (or their parts) inside it."""
    L = M.levels(state)
    xc, yc = P["deck_c"]
    if state == "FT-1V":
        s = P["cube_in"] / 2
        region = M.box(xc - s, xc + s, yc - s, yc + s, L["floor_top"], L["roof_in"])
        frame = [p for p in parts if p.name.startswith("Ideal Vacuum 12")][0].shape
        region = region.cut(frame)
        vendor = 22.6e6
    else:
        bx, by, _ = P["box_in"]
        rim = L["rim"]
        dx, dy = VEN.SAG["door"]
        region = M.box(xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2, L["floor_top"], rim)
        g = VEN.SAG["gasket"][0] + 4.0
        region = region.fuse(M.box(xc - dx / 2 + g, xc + dx / 2 - g, yc - dy / 2 + g, yc + dy / 2 - g, rim, L["roof_in"]))
        lip = VEN.SAG["lip"]
        region = region.cut(M.box(xc - bx / 2, xc + bx / 2, yc - by / 2, yc + by / 2, rim - P["box_t"], rim).cut(
            M.box(xc - bx / 2 + lip, xc + bx / 2 - lip, yc - by / 2 + lip, yc + by / 2 - lip, rim - 3, rim + 1)))
        vendor = None
    v_in = region.Volume()
    rbb = region.BoundingBox()
    v_parts = 0.0
    skip = ("Ideal Vacuum 12", "Saginaw", "Box door", "Poured-in-place", "Cube ")
    for p in parts:
        if any(k in p.name for k in skip):
            continue
        if not bb_overlap(rbb, p.shape.BoundingBox()):
            continue
        v_parts += common_volume(region, p.shape)
    return dict(inside_L=round(v_in / 1e6, 2), vendor_L=vendor and vendor / 1e6, parts_inside_L=round(v_parts / 1e6, 2),
                gas_L=round((v_in - v_parts) / 1e6, 2))


def purge_table(gas):
    """Flow purge (box) and pump-purge (cube) from the measured gas volumes (estimates as marked)."""
    rows = []
    air = 209_000
    for st in ("FT-0", "FT-1"):
        V_ = gas[st]["gas_L"]
        for tgt in (1000, 100):
            n = math.log(air / tgt)
            ideal = n * V_ / 20.0
            rows.append(dict(state=st, method="flow purge at 20 L/min", target_ppm=tgt, minutes=f"{ideal:.1f} ideal, "
                             f"{2 * ideal:.0f}-{5 * ideal:.0f} expected", argon_L=f"{2 * n * V_:.0f}-{5 * n * V_:.0f}"))
    V_ = gas["FT-1V"]["gas_L"]
    S = 1.0            # L/s effective pump speed through the KF-25 hose (estimate: McMaster 4396K21 class)
    for pb_mbar in (1.0, 5.0):
        for tgt in (100, 10):
            n = math.ceil(math.log(air / tgt) / math.log(1013 / pb_mbar))
            t_pump = V_ / S * math.log(1013 / pb_mbar) / 60
            mins = n * (t_pump + 1.0)
            rows.append(dict(state="FT-1V", method=f"pump to {pb_mbar:g} mbar, backfill argon", target_ppm=tgt,
                             minutes=f"{n} cycles x ({t_pump:.1f} min pump + ~1 min fill) = {mins:.0f}",
                             argon_L=f"{n * V_:.0f}"))
    return rows


def heat_table():
    """Enclosure air rise for the same heat load as fast_track.py (heater load + laser), by enclosure area."""
    sys.path.insert(0, str(HERE.parent))
    import fast_track as F
    h = F.heat()
    q = h["heater_load_W"]
    lo, hi = (float(x) for x in h["laser_avg_W"].split("-"))
    o = P["box_out"]
    box_a = 2 * (o[0] * o[1] + o[0] * o[2] + o[1] * o[2]) / 1e6
    cube_a = 6 * ((P["cube_frame"] + 2 * (P["cube_plate_t"] - P["cube_boss"])) / 1000) ** 2
    rows = []
    for name, a in (("box (FT-0, FT-1)", box_a), ("cube (FT-1V)", cube_a)):
        for hb, lab in ((F.H_BOX_STILL, "still air"), (F.H_BOX_FAN, "fan")):
            r = [(q + w) / (hb * a) for w in (lo, hi)]
            rows.append(dict(enclosure=name, area_m2=round(a, 3), cooling=lab, rise_K=f"{r[0]:.0f}-{r[1]:.0f}",
                             air_C=f"{F.T_AMB + r[1]:.0f}", stage_limit_C=F.STAGE_MAX_C))
    return rows


def md_table(rows):
    if not rows:
        return "none\n"
    cols = list(rows[0])
    return ("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
            + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in rows))


def main():
    OUT.mkdir(exist_ok=True)
    t0 = time.time()
    only = sys.argv[1:]
    res = dict(states={})
    gas = {}
    runs = [(s, "zaber") for s in M.STATES] + [("FT-1", "thorlabs")]
    for st, pist in runs:
        key = st if pist == "zaber" else f"{st} (Thorlabs piston)"
        parts = M.build(st, piston=pist)
        clashes, contacts = interference(parts)
        hits, near = beam_check(st, parts) if st != "S1" else ([], [])
        res["states"][key] = dict(n_parts=len(parts), clashes=clashes, contacts=contacts, beam_hits=hits,
                                  beam_nearest=near[:8])
        if st in ("FT-0", "FT-1", "FT-1V") and pist == "zaber":
            gas[st] = inside_volume(st, parts)
        print(f"{key}: {len(parts)} parts, {len(clashes)} clashes, {len(contacts)} designed contacts, "
              f"{len(hits)} beam hits ({time.time() - t0:.0f} s)", flush=True)
    for st in ("S2", "FT-1", "FT-1V"):
        res["states"][st]["apertures"] = aperture_check(st)
    for st in ("FT-1", "FT-1V"):
        c, g = recoater_sweep(st)
        res["states"][st]["recoater_clashes"] = c
        res["states"][st]["recoater_gaps"] = g[:10]
        res["states"][st]["piston"] = piston_checks(st)
        res["states"][st]["mesh"] = mesh_sweeps(st)
        res["states"][st]["sight"] = sight_lines(st)
        print(f"{st}: recoater sweep {len(c)} clashes; fcl {res['states'][st]['mesh']['recoater']['n_contacts']} / "
              f"{res['states'][st]['mesh']['piston']['n_contacts']} contacts ({time.time() - t0:.0f} s)", flush=True)
    res["states"]["FT-1 (Thorlabs piston)"]["piston"] = piston_checks("FT-1", "thorlabs")
    res["states"]["FT-0"]["sight"] = sight_lines("FT-0")
    res["tube_removal"] = {st: tube_removal(st) for st in ("FT-1", "FT-1V")}
    res["removal"] = removal_numbers()
    print("tube removal", {k: sum(h["n_contacts"] for n, h in v.items() if n.endswith("half-shell"))
                           for k, v in res["tube_removal"].items()}, flush=True)
    res["door"] = door_swing("FT-1")
    res["door_no_camera"] = door_swing("FT-1", camera=False)
    print("door swing", res["door"]["last_free_deg"], flush=True)
    res["camera"] = {st: camera_numbers(st) for st in ("FT-0", "FT-1V")}
    res["travel"] = travel_needed()
    res["fit"] = fit_checks()
    res["gas"] = gas
    res["purge"] = purge_table(gas)
    res["heat"] = heat_table()
    res["runtime_s"] = round(time.time() - t0)
    (OUT / "checks.json").write_text(json.dumps(res, indent=1, default=str))
    write_md(res)
    print(f"wrote out/checks.json, out/checks.md in {time.time() - t0:.0f} s")


def write_md(res):
    md = ["# Checks on the fast-track model (`ft_checks.py`, round 2)", "",
          "Generated from `ft_model.py` (2026-11-27). The stages are drawn from Zaber's and Thorlabs' STEP files, the box,",
          "head and lens from their makers' drawings (`ft_vendor.py`, `out/vendor-verify.json`); other bought parts are",
          "envelopes (sizes marked in `ft_model.P`). A clash with an envelope means 'check the maker's drawing'.", ""]
    md += ["## 1. Interference and the beam, by state", "",
           "| State | Parts | Clashes | Designed contacts | Beam envelope hits | Nearest parts to the beam (mm) |",
           "|---|---:|---:|---:|---:|---|"]
    for st, r in res["states"].items():
        near = ", ".join(f"{n['part'].split(' (')[0]} {n['clearance_mm']}" for n in r["beam_nearest"][:4]) or "-"
        md.append(f"| {st} | {r['n_parts']} | {len(r['clashes'])} | {len(r['contacts'])} | {len(r['beam_hits'])} | {near} |")
    for st, r in res["states"].items():
        if r["clashes"] or r["beam_hits"]:
            md += ["", f"**{st} clashes:**", "", md_table(r["clashes"] + [dict(a="beam envelope", b=h["part"],
                                                                               volume_mm3=h["volume_mm3"])
                                                                          for h in r["beam_hits"]])]
    md += ["", "Designed contacts (FT-1):", "", md_table(res["states"]["FT-1"]["contacts"])]
    md += ["**Apertures round the scanned beam** (lens axis at (0, -30); envelope = chief rays from the mirrors, est. "
           f"{P['pivot']:.1f} mm above the bed, to the Ø40 field, plus the beam's own half-width):", ""]
    rows = []
    for st in ("S2", "FT-1", "FT-1V"):
        for k, v in res["states"][st]["apertures"].items():
            rows.append(dict(state=st, element=k, **v))
    md += [md_table(rows)]
    md += ["## 2. Recoater and piston travel", "", "Hopper parks and the travel it needs (cassette frame, mm):", "",
           md_table([res["travel"]])]
    for st in ("FT-1", "FT-1V"):
        r = res["states"][st]
        md += [f"**{st}**: recoater swept over its {P['rc_travel']} mm (exact booleans, 13 positions), "
               f"{len(r['recoater_clashes'])} clashes. Smallest gaps:", "", md_table(r["recoater_gaps"][:6])]
        pc = r["piston"]
        md += [f"Piston ({st}): rod {pc['rod_length_mm']} mm; stroke {pc['stage_stroke_used_mm']} of "
               f"{pc['stage_travel_mm']} mm; 1 atm on the rod = {pc['atm_force_on_rod_N']} N.", ""]
        md.append(md_table([dict(position=k, **{kk: (len(vv) if kk == "clashes" else vv) for kk, vv in v.items()})
                            for k, v in pc.items() if k.startswith("pz=")]))
    pc = res["states"]["FT-1 (Thorlabs piston)"]["piston"]
    md += ["Piston, Thorlabs MTS50/M-Z8 on end (FT-1):", "",
           md_table([dict(position=k, **{kk: (len(vv) if kk == "clashes" else vv) for kk, vv in v.items()})
                     for k, v in pc.items() if k.startswith("pz=")])]
    md += ["## 3. Mesh sweep with python-fcl", "",
           "Each moving group tessellated once (0.4 mm) and moved in fine steps against every static part's BVH mesh;",
           "designed contacts and the cord on the block top are left out.", ""]
    for st in ("FT-1", "FT-1V"):
        m = res["states"][st]["mesh"]
        for g in ("recoater", "piston"):
            md += [f"**{st}, {g}**: {m[g]['poses']} poses, {m[g]['n_contacts']} contacts. Nearest pairs:", "",
                   md_table([{k: v for k, v in r.items() if k != "sweep"} for r in m[g]["nearest"][:6]])]
    for key, lab in (("door", "with the layer camera on its post"), ("door_no_camera", "with the camera unclipped")):
        d = res[key]
        md += [f"**Box door (FT-1) opened about its hinges, {lab}** (axis est. at y {d['hinge_axis_y']}, "
               f"z {d['hinge_axis_z']}; the beam tube's centre section off): free to **{d['last_free_deg']} deg**, the "
               f"front edge then {d['front_edge_rise_mm']} mm up.", ""]
        if d["first_contact"]:
            md += [f"First contact at {d['first_contact']['angle_deg']} deg:", "",
                   md_table([{k: v for k, v in c.items()} for c in d["first_contact"]["contacts"]])]
    tr = res["tube_removal"]
    md += ["**Beam tube's centre section, the two half-shells slid straight out sideways with no lift** (python-fcl, "
           "2 mm steps over 60 mm (a half-shell is 30 mm wide) against every fixed part; both locating spigots are inside "
           "the bore, and the window-stack screws are countersunk flush):", "",
           md_table([dict(state=st, half_shell=h, contacts=v[h]["n_contacts"], section_length_mm=v["section_length_mm"],
                          nearest=", ".join(f"{n['part'].split(' (')[0]} {n['min_dist_mm']}" for n in v[h]["nearest"][:3]))
                     for st, v in tr.items() for h in v if h.endswith("half-shell")])]
    md += ["**Taking the box off the frame (FT-1 -> FT-1V)**, numbers from the model (plate at the top of its stroke):", "",
           md_table([dict(check=k, value=v) for k, v in res["removal"].items()])]
    md += ["## 4. Sight lines and the layer camera", "",
           "Rays from 133 points on the plate (Ø38) to the camera's lens front and to each light's port; a ray is blocked if"
           " it meets any part (windows, the camera and the lights themselves excluded).", ""]
    rows = []
    for st in ("FT-0", "FT-1", "FT-1V"):
        for k, v in res["states"][st]["sight"].items():
            rows.append(dict(state=st, hopper=k, **v))
    md += [md_table(rows)]
    md += ["Camera (IMX477, 1.55 um pixels; f/2.8; circle of confusion two pixels):", "",
           md_table([dict(state=k, **v) for k, v in res["camera"].items()])]
    md += ["## 5. Fit", "", md_table([dict(check=k, value=v) for k, v in res["fit"].items()])]
    md += ["## 6. Gas volume from the model, and purging", "", md_table([dict(state=k, **v) for k, v in res["gas"].items()]),
           md_table(res["purge"]),
           "Pump speed (1 L/s effective) and base pressures are estimates; the floor is set by leaks, outgassing and the "
           "argon's own O2, which the analyzer measures.", ""]
    md += ["## 7. Enclosure air temperature (same load as `fast_track.py`)", "", md_table(res["heat"])]
    md += [f"Run time {res['runtime_s']} s."]
    (OUT / "checks.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
