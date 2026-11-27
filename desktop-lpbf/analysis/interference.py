"""Interference and clearance checks on the low-profile model (cad/lpbf_low.py).

Three layers, fastest first:
1. every part is tessellated (0.05 mm chord) into a closed mesh and turned into a manifold3d solid;
2. for each machine state, every pair with overlapping bounding boxes is intersected with manifold3d. Any shared
   volume above VOL_TOL is then re-checked with OpenCascade's exact boolean on the B-rep, so that chord error on
   coaxial fits (a rod in its bore) is not reported as interference;
3. moving parts are swept through their whole range (N_SWEEP steps per motion group) the same way, and the
   minimum distance from each moving part to its neighbours is measured with FCL at every step.

Contacts that are part of the design (a hose clamped onto its KF flange, a nut on its screw) are listed in JOINTS
and reported separately, never silently dropped.

Run:  python desktop-lpbf/analysis/interference.py
Writes analysis/out/interference.json and analysis/out/interference.md.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time

import fcl
import manifold3d as mf
import numpy as np
import trimesh

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
import lpbf_low as M  # noqa: E402

OUT = HERE / "out"
VOL_TOL = 0.5          # mm3, exact-boolean volume above which a pair interferes
GAP_WARN = 3.0         # mm, report moving-part clearances below this
N_SWEEP = 24
TOL = 0.05             # tessellation chord (mm)

# Designed contacts: (substring of part A, substring of part B, why). Order does not matter.
JOINTS = [
    ("hoses", "KF-25", "hose end clamped onto its KF-25 flange"),
    ("hoses", "Vacuum isolation valve", "hose clamped onto the valve's KF-25 port"),
    ("hoses", "Filter", "hose clamped onto the filter's KF-25 port"),
    ("hoses", "Blower", "hose clamped onto the blower's KF-25 port"),
    ("hoses", "Pump inlet", "hose clamped onto the pump's KF-25 inlet"),
    ("Argon line", "Argon solenoid", "tube fitting into the manifold"),
    ("Argon line", "Process chamber body", "tube fitting into the argon port"),
    ("O2 sample line", "Process chamber body", "tube fitting into the sample port"),
    ("O2 sample line", "Trace O2", "tube fitting into the analyzer"),
    ("Argon supply from the dock", "Argon pressure regulator", "tube fitting"),
    ("Argon supply from the dock", "Tray dock", "tube fitting"),
    ("Argon supply from the dock", "Base plate, gas", "line clipped to the plate edge"),
    ("Chilled-water", "Tray dock", "hose fitting"),
    ("Chilled-water", "19 in. rack", "hose fitting at the laser"),
    ("Chilled-water", "Umbilical duct", "lines run in the duct"),
    ("Argon supply from the dock", "Umbilical duct", "line runs in the duct"),
    ("Pump exhaust", "Tray dock", "hose fitting"),
    ("Pump exhaust", "Dry scroll pump", "hose on the exhaust port"),
    ("Pump exhaust", "Umbilical duct", "hose runs in the duct"),
    ("Process fiber", "Collimator", "fiber connector (QBH) in the collimator"),
    ("Process fiber", "Fiber laser source", "fiber leaves the laser's front panel"),
    ("Process fiber", "Laser guard panels", "fiber through a guarded bulkhead in the guard's side panel"),
    ("Process fiber", "Guard frame", "fiber bulkhead"),
    ("Process fiber", "19 in. rack frame", "fiber leaves the rack"),
    ("Recoater ball nut", "Recoater ball screw", "nut on its screw"),
    ("Recoater ball screw", "Recoater fixed bearing", "screw journal in its bearing"),
    ("Recoater ball screw", "Recoater floating bearing", "screw journal in its bearing"),
    ("Recoater ball screw", "Recoater motor standoff", "shaft passes into the coupling"),
    ("Hinge pins", "Door hinge", "pin in its knuckle/block"),
    ("Hollow piston rod", "bottom flange", "rod in its O-ring gland"),
    ("Hollow piston rod", "Piston head", "rod pressed into the head's socket"),
    ("Hollow piston rod", "Rod end", "rod potted into the end cap"),
    ("Striker disc", "Rod end", "striker screwed to the end cap"),
    ("Striker disc", "Pot magnet", "striker held on the magnet face (the coupling)"),
    ("Pot magnet", "Z lift arm", "magnet set in the arm's pocket"),
    ("Z carriage", "Z actuator body", "carriage runs on its actuator"),
    ("Z carriage", "Z lift arm", "arm bolted to the carriage"),
    ("Z servo", "Z bracket", "servo pilot in the housing's pilot bore"),
    ("Z bracket", "Z mounting flange", "bracket bolted to the flange"),
    ("Z actuator body", "Z bracket", "actuator bolted under the bracket"),
    ("Bore seal", "Build module", "seal rides on the honed bore"),
    ("Bore seal", "Piston head", "seal in its groove"),
    ("Build plate", "Heater block", "plate on the block's face, bayonet spigot in its socket"),
    ("Cartridge heaters", "Heater block", "heaters in their holes"),
    ("Type K thermocouples", "Heater block", "thermocouples in their holes"),
    ("Thermal cutoff", "Heater block", "cutoff in its pocket"),
    ("Macor standoffs", "Heater block", "standoff under the block"),
    ("Macor standoffs", "Piston head", "standoff on the head"),
    ("Spigot O-ring", "Process chamber body", "O-ring squeezed against the port wall"),
    ("Spigot O-ring", "Build module", "O-ring in its groove"),
    ("Build module", "Process chamber body", "spigot in the port, flange on the floor's underside"),
    ("Captive M6 thumb screws", "Process chamber body", "screw in its floor insert"),
    ("Locating dowel", "Process chamber body", "dowel pressed into the floor"),
    ("Locating dowel", "Build module", "dowel in the flange's locating hole"),
    ("Plate rim wiper", "Build module", "wiper rides on the honed bore"),
    ("Plate rim wiper", "Build plate", "wiper in its groove"),
    ("Captive M6 thumb screws", "Build module", "screw through the flange tab"),
    ("bottom flange", "Build module", "bottom flange welded to the cylinder"),
    ("handle", "bottom flange", "handle bolted to the bottom flange"),
    ("Piston head", "bottom flange", "head on the bottom stop"),
    ("Reservoir", "Dovetail rails", "reservoir slides on its dovetail"),
    ("Reservoir", "Metering base", "reservoir seats on the dock face"),
    ("NFC reader antenna", "Metering base", "antenna in its pocket"),
    ("Side reservoir port", "Metering base", "port welded to the base"),
    ("Cover-slide drawer", "Chamber lid", "drawer runs in the lid's slot"),
    ("Drawer O-ring", "Chamber lid", "O-ring squeezed against the lid's front face"),
    ("Drawer O-ring", "Cover-slide drawer", "O-ring in the front plate's groove"),
    ("Cover slide (", "Cover-slide drawer", "slide in its pocket"),
    ("Lift-out wall liner", "Process chamber body", "liners clipped to the walls"),
    ("Plate-height through-beam", "Process chamber body", "fibre heads in the side walls"),
    ("Module-present sensor", "Process chamber body", "sensor bracket under the floor"),
    ("Overflow-jar present sensor", "Overflow jar", "sensor beside the jar"),
    ("Drawer-closed sensor", "Chamber lid", "sensor bracket on the lid's front face"),
    ("Reservoir-docked sensor", "Metering base", "sensor bracket on the dock"),
    ("Recoater carriage", "Recoater guide rail", "carriage runs on its rail"),
    ("Sliding guard door", "Guard door rail", "door runs in its rail"),
    ("HSS recoater blade", "Build plate", "blade passes 0.05 mm above the plate"),
    ("HSS recoater blade", "Process chamber body", "blade passes 0.05 mm above the floor"),
    ("Chamber door", "Process chamber body", "closed door seats on the chamber's front face"),
    ("Door O-ring", "Process chamber body", "O-ring squeezed against the front face"),
    ("Lid O-ring", "Chamber lid", "O-ring squeezed by the lid"),
    # the chamber is a through-frame on a bolted floor plate (chamber-construction.md): the floor plate's designed contacts
    ("Spigot O-ring", "Chamber floor plate", "O-ring squeezed against the port wall"),
    ("Build module", "Chamber floor plate", "spigot in the port, flange on the floor plate's underside"),
    ("Captive M6 thumb screws", "Chamber floor plate", "screw in its floor insert"),
    ("Locating dowel", "Chamber floor plate", "dowel pressed into the floor plate"),
    ("Module-present sensor", "Chamber floor plate", "sensor bracket under the floor plate"),
    ("HSS recoater blade", "Chamber floor plate", "blade passes 0.05 mm above the floor"),
    ("Floor O-ring", "Chamber floor plate", "O-ring in the pad's face gland"),
    ("Floor O-ring", "Process chamber body", "O-ring squeezed by the frame's rebate"),
    # electrical parts (cad/electrical_parts.py and the Pirani tee in lpbf_low.py section 10, electrical.md 2026-11-23)
    ("Pirani tee clamp", "Vacuum isolation valve", "KF-25 clamp over the valve / tee flange joint"),
    ("Pirani tee clamp", "Vacuum line Pirani tee (", "KF-25 clamp on the tee's flange"),
    ("Pirani reducer", "Vacuum line Pirani tee (", "reducer clamped onto the tee's branch flange"),
    ("Pirani transmitter", "Pirani reducer", "transmitter clamped onto the reducer's KF-16 flange"),
    ("Vacuum line Pirani tee (", "Vacuum isolation valve", "tee's flange on the valve's pump-side flange"),
    ("Recoater position magnet", "Recoater carriage block", "magnet bonded into a pocket in the block's back face"),
    ("Z sensor flag", "Z carriage", "flag screwed to the carriage's side"),
    ("Z sensor bracket", "Z actuator body", "bracket clamped to the actuator body"),
    ("Z home and lower-limit sensors", "Z sensor bracket", "sensors in their clamp bores"),
    ("Recoater home and over-travel sensors", "Recoater sensor clamps", "sensors in their clamp bores"),
    ("Recoater sensor clamps", "Recoater sensor posts", "clamp on its post"),
    ("Recoater sensor posts to the base plate", "Recoater sensor posts", "screw in the post's tapped core"),
    ("PB1 stand", "Power box PB1", "box bolted on its stand"),
    ("PB1 disconnect handle", "Power box PB1", "handle on the box's side wall, shaft through it"),
    ("PB1 filter fan", "Power box PB1", "fan and grille in the door's cut-outs"),
    ("E-stops IDEC", "E-stop enclosure", "operator in its enclosure's 22 mm hole"),
    ("Dock PE contacts", "Tray dock", "contacts in the dock's face plate"),
    ("Rod end", "Rod end", "feedthroughs welded into the rod-end block's bores"),
    # zero-point clamps (round 6, hot-swap.md §3.2a)
    ("Zero-point release-air line", "Zero-point push-in fittings", "tube pushed into the module's fitting"),
    ("Zero-point release-air line", "Zero-point release valve", "tube in the valve's push-in port"),
    ("Zero-point clamping pins", "Zero-point arms", "pin screwed into its arm"),
    ("Zero-point clamping pins", "Zero-point clamping modules", "pin in the module's bore (clamped)"),
    # in-situ monitoring hardware (cad/monitoring_parts.py, monitoring/mechanics.md; only built with LPBF_MONITORING=1)
    ("LW viewport gasket", "Process chamber body", "gasket on the window seat's floor"),
    ("LW viewport gasket", "LW viewport window", "window between its gasket and flat ring"),
    ("LW viewport gasket", "LW window clamp ring", "clamp ring presses the flat ring"),
    ("LW window clamp ring", "Process chamber body", "clamp ring bottoms on the wall face (4 x M4)"),
    ("LW viewport window", "Process chamber body", "window in its seat"),
    ("LW cover slide", "Lift-out wall liner, left", "slide held against the liner over its hole"),
    ("LW cover-slide clip", "Lift-out wall liner, left", "clip on the liner"),
    ("LW cover-slide clip", "LW cover slide", "clip holds the slide"),
    ("LW purge fitting", "Process chamber body", "fitting in the wall's SAE-4 port"),
    ("LW purge tube", "LW purge fitting", "tube through the bored-through fitting"),
    ("LW purge tube", "LW purge needle valve", "tube in the valve's compression port"),
    ("LW purge tube", "Process chamber body", "tube through the wall's 4 mm passage"),
    ("Side camera filters", "Side camera lens", "filter holder on the lens's filter thread"),
    ("Side camera lens", "Side high-speed camera", "lens in the camera's C-mount"),
    ("Side camera wedge", "Side high-speed camera", "camera screwed to its wedge"),
    ("Side camera wedge", "Side camera bracket", "wedge bolted on the bracket"),
    ("Side camera bracket", "Chamber floor plate", "bracket's root bolted to the floor plate's edge"),
    ("Side camera bracket", "Process chamber body", "bracket's root against the frame's skirt"),
    ("BW window gasket", "Process chamber body", "gasket in the seat"),
    ("BW window gasket", "BW light window", "window between its gaskets"),
    ("BW window gasket", "BW window clamp frame", "frame presses the flat ring"),
    ("BW window clamp frame", "Process chamber body", "frame bottoms on the wall (3 x M4)"),
    ("BW light window", "Process chamber body", "window in its seat"),
    ("BW LED lens tube", "BW LED asphere", "asphere between the tube's two retaining rings"),
    ("BW LED lens tube", "BW LED heat sink", "tube screwed into the heat sink's SM1 thread"),
    ("BW LED (Thorlabs", "BW LED heat sink", "LED board on the bore's floor (thermal tape, 2 x M2)"),
    ("BW LED clamp", "BW LED heat sink", "split clamp on the heat sink's collar"),
    ("BW LED clamp", "BW LED bracket", "clamp screwed under the bracket's arm (2 x M4)"),
    ("BW LED bracket", "Process chamber body", "bracket's flange screwed to the back wall's outer face (2 x M4)"),
    ("LP adapter boss", "Chamber lid", "boss bolted on the lid (4 x M4)"),
    ("LP adapter O-ring", "Chamber lid", "O-ring squeezed on the lid"),
    ("LP adapter O-ring", "LP adapter boss", "O-ring in the boss's face groove"),
    ("LP window", "LP adapter boss", "window in its seat"),
    ("LP window gasket", "LP adapter boss", "gasket in the seat"),
    ("LP window gasket", "LP window", "window between its gaskets"),
    ("LP window gasket", "LP window retaining ring", "ring presses the flat ring"),
    ("LP window retaining ring", "LP adapter boss", "ring threaded into the boss"),
    ("LP cover slide", "LP adapter boss", "slide in its pocket"),
    ("LP camera filters", "LP window retaining ring", "filter holder on the boss's thread"),
    ("LP camera filters", "LP camera lens", "filter holder on the lens"),
    ("LP camera lens", "LP camera (", "lens in the camera's C-mount"),
    ("Coaxial cube 2", "Optics bridge", "post on the bridge"),
    ("Coaxial cube 3", "Optics bridge", "post on the bridge"),
    ("Coaxial lens tubes", "Coaxial-monitoring dichroic", "tube in the cube's SM1 port"),
    ("Coaxial lens tubes", "Coaxial cube", "tube in the cube's SM1 port"),
    ("Cage rods", "Coaxial", "rods in the cubes' and plates' rod holes"),
    ("Cage rods", "Photodiode", "rods in the cage plates"),
    ("Cage rods", "Beam trap", "rods by the trap"),
    ("Coaxial camera arm", "Coaxial cube 2", "tube in the cube's SM1 port"),
    ("Coaxial camera (", "Coaxial camera arm", "board on its cage plate"),
    ("Coaxial camera (", "Optics bridge", "post on the bridge"),
    ("Photodiode B arm", "Coaxial cube 3", "tube in the cube's SM1 port"),
    ("Photodiode B (", "Photodiode B arm", "detector on its tube"),
    ("Photodiode B (", "Optics bridge", "post on the bridge"),
    ("Photodiode A arm", "Coaxial cube 3", "tube in the cube's SM1 port"),
    ("Photodiode A (", "Photodiode A arm", "detector on its tube"),
    ("Photodiode A (", "Optics bridge", "post on the bridge"),
    ("Beam trap on cube 1", "Coaxial-monitoring dichroic", "trap on the cube's far port"),
    ("Beam trap on cube 1", "Optics bridge", "post on the bridge"),
    ("AE waveguide", "Build plate", "polished tip pressed on the plate's spigot"),
    ("AE waveguide", "Rod end", "cold end screwed into the rod end's bore floor"),
    ("AE sensor (", "Rod end", "sensor face on the rod end's back face (couplant)"),
    ("AE sensor strap", "Rod end", "strap screwed to the rod end"),
    ("AE sensor strap", "AE sensor (", "strap over the sensor"),
    ("AE preamplifier", "Base plate, process module", "preamp on the base plate"),
    ("Digitizer PicoScope", "DIN-rail drawer", "digitizer on the drawer's floor (the drawer is drawn as an envelope)"),
    ("Sync breakout box", "DIN-rail drawer", "box on the drawer's floor (the drawer is drawn as an envelope)"),
]

ALLOW_HOSE_THROUGH = ("Laser guard panels", "Guard frame")   # hoses pass the guard through bulkheads


def is_joint(a, b):
    for x, y, why in JOINTS:
        if (x in a and y in b) or (x in b and y in a):
            return why
    for k in ALLOW_HOSE_THROUGH:
        if ("hoses" in a or "line" in a.lower()) and k in b or ("hoses" in b or "line" in b.lower()) and k in a:
            return "line passes the guard through a bulkhead fitting"
    return None


def solids_of(shape):
    return list(shape.Solids()) or [shape]


def to_manifold(shape):
    ms = []
    for s in solids_of(shape):
        vs, ts = s.tessellate(TOL, 0.2)
        if not ts:
            continue
        v = np.array([(p.x, p.y, p.z) for p in vs], dtype=np.float64)
        t = np.array(ts, dtype=np.int64)
        tm = trimesh.Trimesh(v, t, process=True)
        tm.merge_vertices(digits_vertex=4)
        tm.remove_unreferenced_vertices()
        if tm.volume < 0:
            tm.invert()
        m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(tm.vertices, dtype=np.float32), tri_verts=np.asarray(tm.faces, dtype=np.uint32)))
        if m.status() != mf.Error.NoError or m.is_empty():
            # fall back to the convex hull for a mesh manifold3d will not accept (rare; reported)
            m = mf.Manifold.hull_points(np.asarray(tm.vertices, dtype=np.float32))
        ms.append(m)
    if not ms:
        return None
    return mf.Manifold.batch_boolean(ms, mf.OpType.Add) if len(ms) > 1 else ms[0]


def to_fcl(shape):
    vs, ts = shape.tessellate(0.2, 0.3)
    if not ts:
        return None, None
    v = np.array([(p.x, p.y, p.z) for p in vs], dtype=np.float64)
    t = np.array(ts, dtype=np.int64)
    bvh = fcl.BVHModel()
    bvh.beginModel(len(v), len(t))
    bvh.addSubModel(v, t)
    bvh.endModel()
    return bvh, v


def loc_matrix(loc):
    t = loc.wrapped.Transformation()
    m = np.eye(4)
    for i in range(3):
        for j in range(4):
            m[i, j] = t.Value(i + 1, j + 1)
    return m


def bbox_of(man):
    b = man.bounding_box()
    return np.array(b[:3]), np.array(b[3:])


def overlap(b1, b2, tol=0.01):
    return bool(np.all(b1[0] - tol <= b2[1]) and np.all(b2[0] - tol <= b1[1]))


class Model:
    def __init__(self, module="M50", reservoir=None):
        t0 = time.time()
        self.parts = M.build(module=module, reservoir=reservoir)
        self.names = [p.name for p in self.parts]
        self.man, self.fcl, self.bad = [], [], []
        for p in self.parts:
            m = to_manifold(p.shape)
            self.man.append(m)
            self.fcl.append(to_fcl(p.shape)[0])
        self.ctx = [("context" in p.tags) for p in self.parts]
        # calibration fixtures (tagged 'calibration' + 'context', e.g. the power head on the plate) are checked only in states
        # with "_calibration" set; everywhere else they are context, like the tray
        self.cal = [("calibration" in p.tags) for p in self.parts]
        print(f"meshed {len(self.parts)} parts in {time.time() - t0:.1f} s", flush=True)

    def posed(self, state):
        mans, mats = [], []
        for p, m in zip(self.parts, self.man):
            loc = M.part_location(p, state)
            if loc is not None and m is not None:
                T = loc_matrix(loc)
                mans.append(m.transform(T[:3, :].astype(np.float32)))
                mats.append(T)
            else:
                mans.append(m)
                mats.append(np.eye(4))
        return mans, mats

    def exact_volume(self, i, j, state):
        shapes = M.posed([self.parts[i], self.parts[j]], state)
        try:
            c = shapes[0].intersect(shapes[1])
            return float(c.Volume()) if c is not None else 0.0
        except Exception:  # noqa: BLE001
            return float("nan")

    def check(self, state, only=None):
        mans, _ = self.posed(state)
        bbs = [bbox_of(m) if m is not None else None for m in mans]
        hits, joints, n = [], [], 0
        N = len(mans)
        cal = bool(state.get("_calibration"))
        skip = [c and not (cal and k) for c, k in zip(self.ctx, self.cal)]
        for i in range(N):
            if mans[i] is None or skip[i]:
                continue
            for j in range(i + 1, N):
                if mans[j] is None or skip[j]:
                    continue
                if only is not None and (i in only) == (j in only):
                    continue
                if not overlap(bbs[i], bbs[j]):
                    continue
                n += 1
                v = (mans[i] ^ mans[j]).volume()
                if v <= VOL_TOL:
                    continue
                why = is_joint(self.names[i], self.names[j])
                if why:
                    joints.append((i, j, v, why))
                    continue
                ve = self.exact_volume(i, j, state)
                if ve != ve or ve > VOL_TOL:
                    hits.append((i, j, v, ve))
        return n, hits, joints

    def min_gaps(self, state, group, pad=15.0):
        _, mats = self.posed(state)
        mov = [i for i, p in enumerate(self.parts) if M.moves_with(p, group)]
        mans, _ = self.posed(state)
        bbs = [bbox_of(m) if m is not None else None for m in mans]
        out = []
        for i in mov:
            for j, p in enumerate(self.parts):
                if j in mov or self.ctx[j] or self.fcl[j] is None or self.fcl[i] is None:
                    continue
                b1, b2 = bbs[i], bbs[j]
                if not overlap((b1[0] - pad, b1[1] + pad), b2):
                    continue
                if is_joint(self.names[i], self.names[j]):
                    continue
                o1 = fcl.CollisionObject(self.fcl[i], fcl.Transform(mats[i][:3, :3], mats[i][:3, 3]))
                o2 = fcl.CollisionObject(self.fcl[j], fcl.Transform(mats[j][:3, :3], mats[j][:3, 3]))
                req, res = fcl.DistanceRequest(), fcl.DistanceResult()
                d = fcl.distance(o1, o2, req, res)
                out.append((i, j, float(d)))
        return out


def main():
    # usage: interference.py [MODULE [RESERVOIR]]   (default M50 with its M reservoir -> out/interference.*;
    # other variants -> out/variants/interference-<MODULE>-<RESERVOIR>.*)
    module = sys.argv[1] if len(sys.argv) > 1 else "M50"
    reservoir = sys.argv[2] if len(sys.argv) > 2 else None
    t0 = time.time()
    md = Model(module, reservoir)
    N = md.names
    OUT.mkdir(exist_ok=True)
    rep = dict(variant=f"{module} module, {reservoir or M.MP.MODULES[module]['reservoir']} reservoir", vol_tol_mm3=VOL_TOL, chord_mm=TOL, n_parts=len(N),
               states=[], sweeps=[], clearances=[], joints=[])
    seen_joints = {}
    states = {"closed, parked, piston up": {},
              "recoater at end, piston at bottom stop": {"recoater": M.MOTION["recoater"]["hi"], "piston": M.MOTION["piston"]["lo"]},
              "plate exchange: doors open, plate up 8 mm": {"door": M.MOTION["door"]["hi"], "gdoor": M.MOTION["gdoor"]["hi"], "piston": M.MOTION["piston"]["hi"]},
              "doors open, reservoir and drawer out": {"door": M.MOTION["door"]["hi"], "gdoor": M.MOTION["gdoor"]["hi"], "cartridge": M.MOTION["cartridge"]["lo"],
                                                        "drawer": M.MOTION["drawer"]["lo"]},
              "module swap: arm released, module dropped": {"zstage": M.MOTION["zstage"]["lo"], "module": M.MP.MODULE_DROP, "gdoor": M.MOTION["gdoor"]["hi"]},
              # optics calibration (optics.md §4.1): power head on its stand on the plate, chamber door down for its water lines, recoater parked
              "calibration: power head on the plate, chamber door open": {"_calibration": 1.0, "door": M.MOTION["door"]["hi"]}}
    for label, st in states.items():
        n, hits, joints = md.check(st)
        rep["states"].append(dict(state=label, pose=st, pairs_checked=n,
                                  interferences=[dict(a=N[i], b=N[j], mesh_mm3=round(v, 2), exact_mm3=round(ve, 2)) for i, j, v, ve in hits]))
        for i, j, v, why in joints:
            seen_joints[(N[i], N[j])] = why
        print(f"[{time.time() - t0:5.1f} s] {label}: {n} pairs, {len(hits)} interferences, {len(joints)} designed joints", flush=True)
    for g, m in M.MOTION.items():
        mov = {i for i, p in enumerate(md.parts) if M.moves_with(p, g)}
        worst, gaps = {}, {}
        for k in range(N_SWEEP + 1):
            v = m["lo"] + (m["hi"] - m["lo"]) * k / N_SWEEP
            st = dict(m.get("base_state", {}))
            st[g] = v
            if g in ("cartridge", "drawer"):
                st["gdoor"] = M.MOTION["gdoor"]["hi"]
            n, hits, joints = md.check(st, only=mov)
            for i, j, vm, ve in hits:
                key = (N[i], N[j])
                if key not in worst or ve > worst[key][1]:
                    worst[key] = (v, ve)
            for i, j, d in md.min_gaps(st, g):
                key = (N[i], N[j])
                if key not in gaps or d < gaps[key][1]:
                    gaps[key] = (v, d)
        rep["sweeps"].append(dict(group=g, note=m["note"], range=[m["lo"], m["hi"]], steps=N_SWEEP + 1,
                                  interferences=[dict(a=a, b=b, at=round(v, 2), exact_mm3=round(ve, 2)) for (a, b), (v, ve) in worst.items()]))
        for (a, b), (v, d) in sorted(gaps.items(), key=lambda kv: kv[1][1]):
            rep["clearances"].append(dict(group=g, at=round(v, 2), moving=a, other=b, gap_mm=round(d, 3)))
        print(f"[{time.time() - t0:5.1f} s] sweep {g}: {len(worst)} interfering pairs; tightest gap "
              f"{min((d for _, d in gaps.values()), default=float('nan')):.2f} mm", flush=True)
    rep["joints"] = [dict(a=a, b=b, why=w) for (a, b), w in sorted(seen_joints.items())]
    rep["runtime_s"] = round(time.time() - t0, 1)
    out = OUT if (module, reservoir) in (("M50", None), ("M50", "M")) else OUT / "variants"
    stem = "interference" if out == OUT else f"interference-{module}-{reservoir or M.MP.MODULES[module]['reservoir']}"
    if os.environ.get("LPBF_MONITORING", "") not in ("", "0"):      # with the monitoring parts: its own file; the default stays as it was
        out, stem = OUT / "monitoring" / "mech", f"interference-monitoring-{module}-{reservoir or M.MP.MODULES[module]['reservoir']}"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{stem}.json").write_text(json.dumps(rep, indent=1))
    write_md(rep, out / f"{stem}.md")
    print(f"done in {rep['runtime_s']} s")


def write_md(r, path=None):
    L = [f"# Interference and clearance check ({r['n_parts']} parts; {r.get('variant', '')})", "",
         f"Mesh booleans (manifold3d, {r['chord_mm']} mm chord) flag candidate pairs; each is confirmed with an exact OpenCascade "
         f"boolean. Shared volume above {r['vol_tol_mm3']} mm³ counts as interference. Generated by `analysis/interference.py` in {r['runtime_s']} s.", ""]
    L += ["## Static states", "", "| State | Pairs with touching boxes | Interferences |", "|---|---|---|"]
    for s in r["states"]:
        L.append(f"| {s['state']} | {s['pairs_checked']} | {len(s['interferences'])} |")
    L.append("")
    for s in r["states"]:
        for it in s["interferences"]:
            L.append(f"- {s['state']}: **{it['a']}** × **{it['b']}**: {it['exact_mm3']} mm³")
    L += ["", "## Motion sweeps", "", "| Group | Motion | Range | Steps | Interfering pairs | Tightest gap (mm) |", "|---|---|---|---|---|---|"]
    for s in r["sweeps"]:
        gaps = [c["gap_mm"] for c in r["clearances"] if c["group"] == s["group"]]
        L.append(f"| {s['group']} | {s['note']} | {s['range'][0]:g} to {s['range'][1]:g} | {s['steps']} | {len(s['interferences'])} | {min(gaps) if gaps else float('nan'):.2f} |")
    L.append("")
    for s in r["sweeps"]:
        for it in s["interferences"]:
            L.append(f"- {s['group']} at {it['at']}: **{it['a']}** × **{it['b']}**: {it['exact_mm3']} mm³")
    L += ["", f"## Tightest clearances of moving parts (< {GAP_WARN} mm over the whole sweep)", "",
          "| Group | At | Moving part | Other part | Gap (mm) |", "|---|---|---|---|---|"]
    for c in r["clearances"]:
        if c["gap_mm"] < GAP_WARN:
            L.append(f"| {c['group']} | {c['at']:g} | {c['moving']} | {c['other']} | {c['gap_mm']:.2f} |")
    L += ["", "## Designed joints (contact on purpose, listed for review)", "", "| Part | Part | Why |", "|---|---|---|"]
    for j in r["joints"]:
        L.append(f"| {j['a']} | {j['b']} | {j['why']} |")
    (path or OUT / "interference.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
