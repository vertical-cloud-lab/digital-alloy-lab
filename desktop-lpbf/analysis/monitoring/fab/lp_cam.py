"""The steep lid port (LP) programmed: the lid on a sine plate for the bore, flat for the groove and holes (issue #260, PR 281).

LP sits at (-40, 60, 136) on the chamber lid (monitoring_spec.py). Its Ø24 bore runs on the line of sight to the plate centre,
62.1 deg steep, i.e. 27.9 deg off the lid's normal (cad/monitoring_parts.lp_geometry). A vertical tool can't cut that with the
lid flat, and the lid's 4th-axis clamping (along its x, setup_plan.json) takes out only 23.8 deg of it. So the lid goes on a
sine plate set to 27.9 deg, turned on the plate so the plate's hinge is square to the line of sight's horizontal direction:
the bore is then vertical and one helical-bore op cuts it. The face O-ring groove (2-025: the groove ring round the bore's
ellipse on the lid's top face) and the adapter's four M4 holes are normal to the lid, so they go in a flat setup with the lid
top up (the lid's own +z setup; there is no lid program in the repo yet, so this one is new too). Two programs:
  * mon_lid_LP_top.ngc   the lid flat, top up: the groove (2.0 mm end mill, new tool T15: the groove is 2.3 wide) and the
                          four M4 tap holes (T6, 3.3 mm, 8 deep; tapped by hand or a tapping cycle, not programmed);
  * mon_lid_LP_sine.ngc  the lid on the sine plate: the Ø24 bore, one helix with a 1/2 in. end mill with 1-1/2 in. of
                          flutes (new tool T16: there the bore is 33 mm deep along the tool, past T3's 1 in. of flutes).
Work zero in both: the LP centre on the lid's top face (model (-40, 60, 136)), Z up the tool. In the sine setup the machine
frame is the model turned by R = Rx(27.93 deg) Rz(-33.69 deg) about that point: the plate's hinge runs along machine X and
the lid's top face rises toward +Y.

The adapter's screw holes. As drawn (monitoring_parts.lp_adapter_holes: 4 x M4 3.5 mm in from the Ø40.8 adapter's edge) they sit
on r 16.9 from the port centre, inside the O-ring groove (r 15.6-17.9): each tapped hole would open in the groove floor under the
O-ring, and an M4 head there would sit inside the boss body, which leans over the flange. This script programs the holes where
they clear both (LP_BOLT below: Ø48, at +-60 and +-120 deg from the direction away from the lid's centre: 4.1 mm of wall between
each thread and the groove, the heads and a key's path 0.5 mm or more clear of the boss, the flange's lugs 8 mm from the window
flange), and checks the as-drawn ones (cam_monitoring.json "LP" -> "adapter_holes"). The model, the adapter boss and the
blanking cap (flat_parts_dxf.py) need the same change; until monitoring_parts.py has it, the model's lid has the old holes.

Modes (state in $MON_CAM_TMP, default /tmp/fab-e):
  prep     (cadquery) the stock is the lid as drawn without LP (inventory.py's default build, parts/chamber_lid_*.brep); the
           target is that lid minus monitoring_parts' bore and groove and LP_BOLT's holes. Writes both setups' frames: the
           target (FreeCAD finds its faces there), stock and target STLs, the fixtures, lp-cam/geometry.json.
  post     (FreeCAD 1.0.2, freecadcmd) freecad_cam.run_cam() on the two setups, with the same in-memory patch cam_monitoring.py
           makes (ops may name their faces) plus the lid parts. Copies the programs to analysis/out/monitoring/fab/gcode/.
  sim      (CAMotics 1.2.0 in Docker) each program on a box of stock round its features in its own frame; back in the model
           frame on a 0.2 mm grid: the lid stock less both setups' cuts against the target (gouges, leftover, loose pieces).
  holders  holder_check.sweep() (holders, spindle, fixtures; rapids through stock) on each setup, against the in-process
           stock's top surface and the fixtures' (lid on parallels and toe clamps; on the sine plate's top plate on parallels).
  summary  everything into cam_monitoring.json["LP"].
Run:
  P=desktop-lpbf/analysis/monitoring/fab/lp_cam.py
  OMP_NUM_THREADS=1 /tmp/capmem 2 /tmp/venv/bin/python $P prep
  OMP_NUM_THREADS=1 /tmp/capmem 3 env FREECADCMD=<freecadcmd 1.0.2> /tmp/venv/bin/python $P post
  /tmp/heavy 4 sg docker -c "env OMP_NUM_THREADS=1 CAMOTICS_MEM=3g CAMOTICS_CPUS=1 /tmp/venv/bin/python $P sim"
  OMP_NUM_THREADS=1 /tmp/capmem 3 /tmp/venv/bin/python $P holders
  /tmp/venv/bin/python $P summary
"""
from __future__ import annotations

import glob
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
CAD = REPO / "desktop-lpbf" / "cad"
MACH = REPO / "desktop-lpbf" / "analysis" / "machining"
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "monitoring" / "fab"
TMP = pathlib.Path(os.environ.get("MON_CAM_TMP", "/tmp/fab-e"))
W = TMP / "lp-cam"
LID0 = "parts/chamber_lid_*.brep"            # inventory.py's default build: the lid without LP
LID_MODEL = "parts-mon/chamber_lid_*.brep"   # LPBF_MONITORING=1 build: the lid as monitoring_parts draws it
BOSS_MODEL = "parts-mon/lp_adapter_boss_*.brep"
SETUPS = ("lid_LP_top", "lid_LP_sine")
# the adapter's 4 x M4: on Ø48 at +-60 and +-120 deg from the direction away from the lid's centre (see the docstring)
LP_BOLT = dict(r=24.0, deg=(-120.0, -60.0, 60.0, 120.0), tap_drill_d=3.3, depth=8.0, clear_d=4.5, lug_r=5.5)
LID_Z = (120.0, 136.0)
RES = 0.2                                    # mm, the CAMotics and comparison grid round the port
# T15 is new: the face groove is 2.3 mm wide (module_params.FACE_1P78), narrower than T4 (1/8 in.)
T15 = dict(name="2.0 mm 2-flute carbide end mill (added: the LP face O-ring groove, 2.3 wide)", shape="endmill", d=2.0,
           flutes=2, rpm=8100, ipt=0.0004, length=10.0, edge=6.0)
T15_CUTTER = dict(holder="04-0006", loc=6.0, oal=38.0, bom="2.0 mm 2-flute carbide end mill, 6 mm LOC, 38 mm OAL (new, not in tooling-bom)")
# T16 is new too: on the sine plate the bore runs 33 mm along the tool, from the mouth's high side to the exit's low side, past
# T3's 1 in. of flutes (holder_check put T3's shank 0.01 mm off the wall it had cut). A 1/2 in. end mill with 1-1/2 in. of
# flutes, 50 mm out of the same side-lock holder (Haas 04-0001), keeps the bore at 1.9 x the tool's diameter for the helix
T16 = dict(name="1/2 in. (12.7 mm) 3-flute carbide end mill, 1-1/2 in. LOC, 50 mm stick-out (added: the LP bore)", shape="endmill",
           d=12.7, flutes=3, rpm=7600, ipt=0.003, length=50.0, edge=38.1)
T16_CUTTER = dict(holder="04-0001", loc=38.1, oal=101.6, bom="1/2 x 1-1/2 LOC x 4 OAL 3-flute carbide end mill (new, not in tooling-bom)")
NEW_TOOLS = {15: T15, 16: T16}
NEW_CUTTERS = {15: T15_CUTTER, 16: T16_CUTTER}


def lp():
    sys.path.insert(0, str(CAD))
    import monitoring_parts as MPT
    g = MPT.lp_geometry()
    F = MPT.MP.FACE_1P78
    c, d = np.asarray(g["c"], float), np.asarray(g["d"], float)
    r_g = g["on_axis"]["r_groove"]
    away = math.atan2(c[1], c[0])
    holes = [(float(c[0] + LP_BOLT["r"] * math.cos(away + math.radians(a))), float(c[1] + LP_BOLT["r"] * math.sin(away + math.radians(a))))
             for a in LP_BOLT["deg"]]
    drawn = [tuple(map(float, p)) for p in MPT.lp_adapter_holes(c, g["on_axis"]["r_adapter"])]
    return dict(c=c, d=d, r_b=g["r_bore"], r_g=r_g, r_go=r_g + F["width"], depth=F["depth"], r_a=g["on_axis"]["r_adapter"],
                ring=MPT.MP.pick_ring(2 * math.pi * r_g), holes=holes, holes_drawn=drawn, away_deg=math.degrees(away),
                elevation=g["elevation"])


def sine_rotation(d):
    """R (model -> sine-plate machine frame): a turn about z that brings the line of sight's horizontal part onto +Y, then the
    sine plate's tilt about X that stands the line up. Returns R, the turn psi and the tilt theta (deg)."""
    a = -np.asarray(d, float)
    psi = math.pi / 2 - math.atan2(a[1], a[0])
    th = math.atan2(math.hypot(a[0], a[1]), a[2])
    Rz = np.array([[math.cos(psi), -math.sin(psi), 0], [math.sin(psi), math.cos(psi), 0], [0, 0, 1.0]])
    Rx = np.array([[1.0, 0, 0], [0, math.cos(th), -math.sin(th)], [0, math.sin(th), math.cos(th)]])
    R = Rx @ Rz
    assert np.allclose(R @ a, [0, 0, 1], atol=1e-9)
    return R, math.degrees(psi), math.degrees(th)


def frames(L):
    """{setup: (R, origin)}: machine = R (model - origin)"""
    R, _, _ = sine_rotation(L["d"])
    return {"lid_LP_top": (np.eye(3), L["c"]), "lid_LP_sine": (R, L["c"])}


# ---------------------------------------------------------------------------------------------------------------- prep
def _place(shape, R, o):
    """machine = R (model - o), R = Rx(theta) Rz(psi) (sine_rotation) or the identity"""
    import cadquery as cq
    s = shape.translate(cq.Vector(*(-np.asarray(o, float))))
    if np.allclose(R, np.eye(3)):
        return s
    _, psi, th = sine_rotation(lp()["d"])
    s = s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), psi).rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), th)
    return s


def fixture_solids(L):
    """the workholding in the model frame, per setup: [(name, solid)]"""
    import cadquery as cq
    V = cq.Vector

    def box(x0, x1, y0, y1, z0, z1):
        return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
    lz0, lz1 = LID_Z
    clamps = [("toe clamp", box(*((-156.0, -131.0) if sx < 0 else (131.0, 156.0)), sy * 70.0 - 15.0, sy * 70.0 + 15.0, lz1, lz1 + 18.0))
              for sx in (-1, 1) for sy in (-1, 1)]
    par = [("parallel", box(-150.0, 150.0, y0, y0 + 12.7, lz0 - 25.4, lz0)) for y0 in (-105.0, 92.0)]
    top = clamps + par
    # the sine plate: the lid on two 1 in. parallels on its top plate (a 25 mm plate, drawn 400 x 400 so it is under the
    # whole lid whichever way the lid is turned on it); the bore's exit (x -48..-22, y 40..66 at the underside) is over air.
    # On 1/2 in. parallels the plate, which rises with the lid, came within 0.75 mm of the tool's end under the bore's high side
    sp = [("parallel", box(-150.0, 150.0, y0, y0 + 12.7, lz0 - 25.4, lz0)) for y0 in (-105.0, 92.0)]
    sp.append(("sine plate top plate", box(-200.0, 200.0, -200.0, 200.0, lz0 - 25.4 - 25.0, lz0 - 25.4)))
    sine = clamps + sp
    return {"lid_LP_top": top, "lid_LP_sine": sine}


def prep():
    import cadquery as cq
    V = cq.Vector
    W.mkdir(parents=True, exist_ok=True)
    L = lp()
    lid0 = cq.importers.importBrep(sorted(glob.glob(str(TMP / LID0)))[0]).val()
    c, d = L["c"], L["d"]
    lz0, lz1 = LID_Z
    bore = cq.Solid.makeCylinder(L["r_b"], 40.0, V(*(c + 30.0 * d)), V(*(-d)))           # as monitoring_parts._lp cuts it
    groove = cq.Solid.makeCylinder(L["r_go"], L["depth"] + 0.01, V(c[0], c[1], lz1 - L["depth"]), V(0, 0, 1)).cut(
        cq.Solid.makeCylinder(L["r_g"], L["depth"] + 0.01, V(c[0], c[1], lz1 - L["depth"]), V(0, 0, 1)))
    holes = [cq.Solid.makeCylinder(LP_BOLT["tap_drill_d"] / 2, LP_BOLT["depth"] + 0.1, V(x, y, lz1 - LP_BOLT["depth"]), V(0, 0, 1))
             for x, y in L["holes"]]
    target = lid0.cut(bore).cut(groove)
    for h_ in holes:
        target = target.cut(h_)
    target = target.clean()
    stock1 = lid0.cut(groove)                    # after the flat setup
    for h_ in holes:
        stock1 = stock1.cut(h_)
    stock1 = stock1.clean()
    # the bore against the lid: does it meet anything inside the lid (the cover-slide drawer slot)?
    full = bore.intersect(cq.Solid.makeBox(400, 400, lz1 - lz0, V(-200, -200, lz0)))
    in_lid = bore.intersect(lid0)
    geo = dict(port_centre=c.tolist(), line_of_sight=d.round(5).tolist(), elevation_deg=round(L["elevation"], 2),
               off_lid_normal_deg=round(90 - L["elevation"], 2), bore_d=2 * L["r_b"],
               groove=dict(id=round(2 * L["r_g"], 2), od=round(2 * L["r_go"], 2), depth=L["depth"], o_ring=L["ring"][0]),
               adapter_d=round(2 * L["r_a"], 2), away_from_lid_centre_deg=round(L["away_deg"], 2),
               holes_programmed=[[round(x, 2), round(y, 2)] for x, y in L["holes"]],
               holes_as_drawn=[[round(x, 2), round(y, 2)] for x, y in L["holes_drawn"]],
               bore_volume_in_lid_mm3=round(in_lid.Volume(), 1), bore_volume_in_a_solid_16_mm_plate_mm3=round(full.Volume(), 1),
               lid_cm3=dict(stock=round(lid0.Volume() / 1e3, 3), target=round(target.Volume() / 1e3, 3)))
    fx = fixture_solids(L)
    fr = frames(L)
    for su, (R, o) in fr.items():
        t_m = _place(target, R, o)
        t_m.exportBrep(str(W / f"{su}.brep"))                  # FreeCAD's model in this setup's frame
        bb = t_m.BoundingBox()
        geo.setdefault("setups", {})[su] = dict(R=R.round(6).tolist(), origin=o.tolist(),
                                                bbox=[round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)])
        st = lid0 if su == "lid_LP_top" else stock1
        cq.exporters.export(cq.Workplane().add(_place(st, R, o)), str(W / f"{su}_stock.stl"), tolerance=0.02, angularTolerance=0.1)
        for k, (nm, sol) in enumerate(fx[su]):
            cq.exporters.export(cq.Workplane().add(_place(sol, R, o)), str(W / f"{su}_fix{k}.stl"), tolerance=0.05, angularTolerance=0.2)
        geo["setups"][su]["fixtures"] = [nm for nm, _ in fx[su]]
    _, psi, th = sine_rotation(d)
    geo["sine_plate"] = dict(tilt_deg=round(th, 3), turn_on_plate_deg=round(psi, 2),
                             gauge_blocks_mm_for_a_127_mm_plate=round(127.0 * math.sin(math.radians(th)), 3),
                             gauge_blocks_in_for_a_5_in_plate=round(5.0 * math.sin(math.radians(th)), 4))
    # the model frame STLs for the comparison
    cq.exporters.export(cq.Workplane().add(lid0), str(W / "lid_stock_model.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(cq.Workplane().add(target), str(W / "lid_target_model.stl"), tolerance=0.02, angularTolerance=0.1)
    # the model's own lid (as monitoring_parts draws it): what differs from the target is the holes
    mf = sorted(glob.glob(str(TMP / LID_MODEL)))
    if mf:
        lidm = cq.importers.importBrep(mf[0]).val()
        geo["model_lid_vs_target_mm3"] = dict(only_in_model=round(lidm.cut(target).Volume(), 1), only_in_target=round(target.cut(lidm).Volume(), 1))
        # the as-drawn holes against the groove: volume of each Ø3.3 hole inside the groove ring, and the head in the boss
        g_ring = groove
        ah = []
        boss = cq.importers.importBrep(sorted(glob.glob(str(TMP / BOSS_MODEL)))[0]).val() if glob.glob(str(TMP / BOSS_MODEL)) else None
        for (x, y), lab in [(p, "drawn") for p in L["holes_drawn"]] + [(p, "programmed") for p in L["holes"]]:
            hole = cq.Solid.makeCylinder(2.0, 8.1, V(x, y, lz1 - 8.0), V(0, 0, 1))      # the M4 thread's major diameter
            rec = dict(which=lab, xy=[round(x, 2), round(y, 2)], r_from_port_mm=round(math.hypot(x - c[0], y - c[1]), 2),
                       thread_in_groove_mm3=round(hole.intersect(g_ring).Volume(), 2),
                       thread_wall_to_groove_mm=round(max(math.hypot(x - c[0], y - c[1]) - 2.0 - L["r_go"], L["r_g"] - 2.0 - math.hypot(x - c[0], y - c[1])), 2))
            if boss is not None:
                head = cq.Solid.makeCylinder(3.5 + 0.5, 4.0, V(x, y, lz1 + 8.0), V(0, 0, 1))      # M4 SHCS head Ø7 x 4, +0.5
                key = cq.Solid.makeCylinder(3.5, 40.0, V(x, y, lz1 + 12.0), V(0, 0, 1))
                rec.update(head_in_boss_mm3=round(head.intersect(boss).Volume(), 1), key_path_in_boss_mm3=round(key.intersect(boss).Volume(), 1))
            ah.append(rec)
        geo["adapter_holes"] = ah
    (W / "geometry.json").write_text(json.dumps(geo, indent=1))
    print(json.dumps({k: v for k, v in geo.items() if k != "setups"}, indent=1))
    for su, v in geo["setups"].items():
        print(su, v["bbox"])


# ---------------------------------------------------------------------------------------------------------------- post
def load_fc():
    """freecad_cam.py as a module, with cam_monitoring.py's patch (ops may name their faces) and the lid's two setup frames as parts"""
    sys.path.insert(0, str(HERE))
    import cam_monitoring as CM
    src = (MACH / "freecad_cam.py").read_text()
    old = '    for part in ("frame", "floor"):\n'
    assert src.count(old) == 1, "freecad_cam.py changed: the part loader this script patches is not there"
    src = src.replace(old, '    for part in ("frame", "floor", "lid_LP_top", "lid_LP_sine"):  # lp_cam.py: the lid in its two setups\n')
    old2 = ('                if kind == "drill":\n'
            '                    add(label, kind, t, ipt, cfg, holes(part, cfg["holes"]))')
    assert src.count(old2) == 1
    src = src.replace(old2, '                if "subs" in cfg:  # cam_monitoring.py / lp_cam.py: explicit face or edge names\n'
                            '                    add(label, kind, t, ipt, cfg, cfg["subs"])\n'
                            '                elif kind == "drill":\n'
                            '                    add(label, kind, t, ipt, cfg, holes(part, cfg["holes"]))')
    import types
    mod = types.ModuleType("freecad_cam")
    mod.__file__ = str(MACH / "freecad_cam.py")
    sys.modules["freecad_cam"] = mod
    exec(compile(src, str(MACH / "freecad_cam.py"), "exec"), mod.__dict__)
    mod.TOOLS.update({k: dict(v) for k, v in NEW_TOOLS.items()})
    del CM
    return mod


def lid_setups(FC):
    """the two jobs, with face names read off each setup's shape (FreeCAD side)"""
    import Part
    geo = json.loads((W / "geometry.json").read_text())
    out = []
    for su in SETUPS:
        s = Part.Shape()
        s.read(str(W / f"{su}.brep"))
        bb = s.BoundBox
        stock = (bb.XMin, bb.YMin, bb.ZMin, bb.XLength, bb.YLength, bb.ZLength)
        if su == "lid_LP_top":
            floor = [i for i, f in enumerate(s.Faces) if type(f.Surface).__name__ == "Plane" and f.normalAt(0, 0).z > 0.999
                     and abs(f.BoundBox.ZMax + geo["groove"]["depth"]) < 0.01 and f.BoundBox.DiagonalLength < 60]
            assert len(floor) == 1, "groove floor not found: %s" % floor
            holes = []
            for x, y in geo["holes_programmed"]:
                xm, ym = x - geo["port_centre"][0], y - geo["port_centre"][1]
                k = [i for i, f in enumerate(s.Faces) if type(f.Surface).__name__ == "Cylinder" and abs(f.Surface.Radius - 1.65) < 1e-3
                     and abs(f.Surface.Center.x - xm) < 0.05 and abs(f.Surface.Center.y - ym) < 0.05]
                assert k, "hole at %s not found" % ((x, y),)
                holes.append("Face%d" % (k[0] + 1))
            out.append(dict(name=su, part=su, stock_box=stock, clear_z=25.0, ops=[
                ("LP face O-ring groove %s: ID %.2f, %.1f wide, %.2f deep, pocket" % (geo["groove"]["o_ring"], geo["groove"]["id"],
                                                                                    (geo["groove"]["od"] - geo["groove"]["id"]) / 2, geo["groove"]["depth"]),
                 "pocket", 15, None, dict(start=0.0, step=0.5, subs=["Face%d" % (floor[0] + 1)])),
                ("LP adapter holes: drill 4 x 3.3 mm, M4 tapped after, %.0f deep" % LP_BOLT["depth"], "drill", 6, None,
                 dict(start=0.0, final=-LP_BOLT["depth"], through=False, subs=holes)),
            ]))
        else:
            k = [i for i, f in enumerate(s.Faces) if type(f.Surface).__name__ == "Cylinder" and abs(f.Surface.Radius - 12.0) < 1e-3
                 and abs(abs(f.Surface.Axis.z) - 1) < 1e-6 and math.hypot(f.Surface.Center.x, f.Surface.Center.y) < 0.05]
            assert k, "the bore's face not found"
            z_top = max(s.Faces[i].BoundBox.ZMax for i in k)
            z_bot = min(s.Faces[i].BoundBox.ZMin for i in k)
            geo["setups"][su]["bore_faces"] = len(k)
            geo["setups"][su]["bore_z"] = [round(z_bot, 3), round(z_top, 3)]
            out.append(dict(name=su, part=su, stock_box=stock, clear_z=round(z_top + 25.0, 1), ops=[
                ("LP bore 24.0 mm on the line of sight, helix, lid on a %.2f deg sine plate, z %.2f..%.2f" % (
                    geo["sine_plate"]["tilt_deg"], z_bot - 0.5, z_top + 1.0),
                 "helix_bore", 16, 0.002, dict(start=round(z_top + 1.0, 3), final=round(z_bot - 0.5, 3), step=1.0, offset=0.0,
                                               subs=["Face%d" % (k[0] + 1)])),
            ]))
    (W / "geometry.json").write_text(json.dumps(geo, indent=1))
    return out


def post2():
    FC = load_fc()
    FC.IN_DIR = str(W)
    FC.GCODE_DIR = str(W / "gcode")
    FC.SETUPS = lid_setups(FC)
    version, results = FC.run_cam()
    out = FC.summarise(version, results)
    (W / "freecad_cam_lp.json").write_text(json.dumps(out, indent=1))
    print("lp post written", flush=True)


def post():
    fcmd = os.environ.get("FREECADCMD")
    if not fcmd:
        sys.exit("set FREECADCMD")
    (W / "gcode").mkdir(parents=True, exist_ok=True)
    code = "import runpy; runpy.run_path(%r, run_name='__main__')" % str(pathlib.Path(__file__).resolve())
    subprocess.run([fcmd, "-c", code], env=dict(os.environ, MON_CAM_MODE="post2"), check=True)
    (OUT / "gcode").mkdir(parents=True, exist_ok=True)
    for su in SETUPS:
        shutil.copy(W / "gcode" / f"{su}.ngc", gcode_name(su))


def gcode_name(su):
    return OUT / "gcode" / ("mon_lid_LP_top.ngc" if su == "lid_LP_top" else "mon_lid_LP_sine.ngc")


# ---------------------------------------------------------------------------------------------------------------- sim
class Grid:
    def __init__(self, lo, hi, h):
        self.lo, self.hi, self.h = np.asarray(lo, float), np.asarray(hi, float), h
        self.n = np.round((self.hi - self.lo) / h).astype(int)
        self.c = [self.lo[a] + (np.arange(self.n[a]) + 0.5) * h for a in range(3)]


def camsim_box(name, cam_text, lo, hi, res):
    """CAMotics on a box of stock [lo, hi] (this setup's frame): the STL of what is left, triangles in the setup frame"""
    sys.path.insert(0, str(MACH))
    import camotics_sim as CS
    import freecad_cam as FC0  # noqa: F401
    d = W / "sim" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.ngc").write_text(cam_text)
    tools = {str(t): dict(units="metric", shape="cylindrical", length=s["length"], diameter=s["d"], description=s["name"])
             for t, s in {**CS.FC.TOOLS, **NEW_TOOLS}.items()}
    proj = {"units": "metric", "resolution-mode": "manual", "resolution": res, "tools": tools,
            "workpiece": {"automatic": False, "margin": 0,
                          "bounds": {"min": [lo[0], lo[1], lo[2] - CS.SHIFT], "max": [hi[0], hi[1], hi[2] - CS.SHIFT]}},
            "files": [f"{name}.ngc"]}
    (d / f"{name}.camotics").write_text(json.dumps(proj, indent=1))
    mem = os.environ.get("CAMOTICS_MEM", "3g")
    cmd = ["docker", "run", "--rm", f"--memory={mem}", f"--memory-swap={mem}", f"--cpus={os.environ.get('CAMOTICS_CPUS', '1')}",
           "-v", f"{d}:/work", CS.IMAGE, "sh", "-c", f"camsim -v --binary --threads 1 {name}.camotics {name}.stl; echo exit=$?"]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    log = [ln for ln in (p.stdout + p.stderr).splitlines() if not ln.startswith(("/work", "Progress"))]
    (d / f"{name}.log").write_text("\n".join(log))
    tris = CS.read_stl(str(d / f"{name}.stl"))
    tris[..., 2] += CS.SHIFT
    errs = [ln for ln in log if "ERROR" in ln or "Not implemented" in ln]
    return tris, dict(seconds=round(time.time() - t0, 1), errors=errs[:10], log_tail=log[-3:])


def sim():
    sys.path.insert(0, str(MACH))
    import camotics_sim as CS
    from scipy import ndimage
    geo = json.loads((W / "geometry.json").read_text())
    L = lp()
    fr = frames(L)
    c = L["c"]
    # comparison grid round the port, model frame
    grid = Grid((c[0] - 36.0, c[1] - 36.0, LID_Z[0] - 3.0), (c[0] + 36.0, c[1] + 36.0, LID_Z[1] + 1.0), RES)
    X, Y, Z = np.meshgrid(*grid.c, indexing="ij")
    P = np.stack([X, Y, Z], -1).reshape(-1, 3)
    del X, Y, Z
    stock = CS.voxelize(CS.read_stl(str(W / "lid_stock_model.stl")), grid)
    target = CS.voxelize(CS.read_stl(str(W / "lid_target_model.stl")), grid)
    removed = np.zeros(stock.shape, bool)
    res = dict(grid=dict(lo=grid.lo.tolist(), hi=grid.hi.tolist(), res=RES), setups={})
    for su in SETUPS:
        R, o = fr[su]
        text, moves = CS.expand(gcode_name(su).read_text())
        cut = [m for m in moves if not m["rapid"]]
        pts = np.concatenate([CS.segments(m) for m in cut])           # arcs sampled, not just their end points
        rmax = max({**CS.FC.TOOLS, **NEW_TOOLS}[m["tool"]]["d"] for m in cut) / 2
        lo = pts.min(0) - [rmax + 2, rmax + 2, 1.0]
        hi = pts.max(0) + [rmax + 2, rmax + 2, 0.0]
        lo[2] = min(lo[2], -40.0)
        hi[2] = min(hi[2], 45.0 if su == "lid_LP_sine" else 0.5)       # the stock box stops at the lid's top (flat) / above the mouth
        tris, info = camsim_box(su, text, lo, hi, RES)
        # back to the model frame: p = R^T m + o
        tm = tris @ R + o
        left = CS.voxelize(tm, grid)
        Pm = (P - o) @ R.T                                               # voxel centres in this setup's frame
        inbox = np.all((Pm >= lo) & (Pm <= hi), axis=1).reshape(stock.shape)
        rem = inbox & ~left
        res["setups"][su] = dict(camotics=info, box_lo=np.round(lo, 2).tolist(), box_hi=np.round(hi, 2).tolist(),
                                 removed_from_stock_mm3=round(float((rem & stock & ~removed).sum()) * RES ** 3, 1),
                                 camotics_time=CS.camotics_times(moves))
        removed |= rem
        del tm, left, inbox, rem, Pm
    final = stock & ~removed
    gouge = target & removed
    leftover = final & ~target

    def deep(mask):
        if not mask.any():
            return dict(volume_mm3=0.0, max_depth_mm=0.0, deeper_than_0p5_mm3=0.0, deeper_than_1_mm3=0.0, regions=[])
        dist = ndimage.distance_transform_edt(mask, sampling=RES)
        lab, n = ndimage.label(mask & (dist >= 0.5))
        regs = []
        for k, sl in enumerate(ndimage.find_objects(lab), 1):
            m = lab[sl] == k
            dd = np.where(m, dist[sl], 0)
            w = np.unravel_index(np.argmax(dd), dd.shape)
            regs.append(dict(volume_mm3=round(float(m.sum()) * RES ** 3, 2), max_depth_mm=round(float(dd.max()), 2),
                             at=[round(float(grid.c[a][sl[a].start + w[a]]), 2) for a in range(3)]))
        regs.sort(key=lambda r: -r["volume_mm3"])
        return dict(volume_mm3=round(float(mask.sum()) * RES ** 3, 1), max_depth_mm=round(float(dist.max()), 2),
                    deeper_than_0p5_mm3=round(float((dist >= 0.5).sum()) * RES ** 3, 2),
                    deeper_than_1_mm3=round(float((dist >= 1.0).sum()) * RES ** 3, 2), regions=regs[:10])
    lab, n = ndimage.label(final)
    sizes = ndimage.sum(np.ones_like(final), lab, range(1, n + 1)) if n else []
    res.update(stock_mm3=round(float(stock.sum()) * RES ** 3, 1), target_mm3=round(float(target.sum()) * RES ** 3, 1),
               final_mm3=round(float(final.sum()) * RES ** 3, 1), gouge=deep(gouge), leftover=deep(leftover),
               pieces=[round(float(s) * RES ** 3, 1) for s in sorted(sizes, reverse=True)[:5]],
               note="the grid holds the lid within 36 mm of the port centre; its edges cut the lid, so 'pieces' counts the "
                    "lid's own piece in the window first (a slug would show as a second piece)")
    (W / "sim.json").write_text(json.dumps(res, indent=1))
    _render(grid, target, final, gouge, leftover)
    print(json.dumps({k: v for k, v in res.items() if k != "setups"}, indent=1))
    for su, v in res["setups"].items():
        print(su, v["camotics"], v["removed_from_stock_mm3"])


def _render(grid, target, final, gouge, leftover):
    """a section along the line of sight's vertical plane through the port centre, model beside CAMotics"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    L = lp()
    c, d = L["c"], L["d"]
    u = np.array([d[0], d[1], 0.0]) / math.hypot(d[0], d[1])
    s = np.linspace(-34, 34, 341)
    z = grid.c[2]
    S, Zg = np.meshgrid(s, z, indexing="ij")
    Xq, Yq = c[0] + S * u[0], c[1] + S * u[1]
    ix = np.clip(np.round((Xq - grid.lo[0]) / grid.h - 0.5).astype(int), 0, grid.n[0] - 1)
    iy = np.clip(np.round((Yq - grid.lo[1]) / grid.h - 0.5).astype(int), 0, grid.n[1] - 1)
    iz = np.clip(np.round((Zg - grid.lo[2]) / grid.h - 0.5).astype(int), 0, grid.n[2] - 1)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    for a_, arr, ttl in ((ax[0], target, "model (target)"), (ax[1], final, "CAMotics, both programs")):
        img = arr[ix, iy, iz].astype(float)
        a_.imshow(img.T, origin="lower", extent=[s[0], s[-1], z[0], z[-1]], cmap="Greys", vmin=0, vmax=1.6, aspect="equal")
        if arr is final:
            for m, col in ((gouge, "red"), (leftover, "orange")):
                mm = m[ix, iy, iz]
                if mm.any():
                    a_.contour(S, Zg, mm.astype(float), levels=[0.5], colors=col, linewidths=0.8)
        a_.plot(s, c[2] + s * d[2] / math.hypot(d[0], d[1]), ":", color="tab:blue", lw=0.8)
        a_.set_ylim(z[0], z[-1])
        a_.set_title(ttl, fontsize=9)
        a_.set_xlabel("along the line of sight's horizontal direction (mm)", fontsize=8)
    ax[0].set_ylabel("z (mm)", fontsize=8)
    fig.suptitle("LP in the lid: the Ø24 bore on the line of sight (27.9° off the lid's normal) and the face groove", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "camotics_lid_LP.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------------- holders
def holders():
    sys.path.insert(0, str(MACH))
    import camotics_sim as CS
    import holder_check as HC
    CS.FC.TOOLS.update({k: dict(v) for k, v in NEW_TOOLS.items()})
    HC.CUTTERS.update({k: dict(v) for k, v in NEW_CUTTERS.items()})
    geo = json.loads((W / "geometry.json").read_text())
    h = 0.5
    out = dict(resolution_mm=h, setups={})
    for su in SETUPS:
        text, moves = CS.expand(gcode_name(su).read_text())
        xs = [p[0] for m in moves for p in (m["p0"], m["p1"])]
        ys = [p[1] for m in moves for p in (m["p0"], m["p1"])]
        pad = 110.0
        x0, x1 = min(xs) - pad, max(xs) + pad
        y0, y1 = min(ys) - pad, max(ys) + pad
        stl = CS.read_stl(str(W / f"{su}_stock.stl"))
        zlo = float(stl[..., 2].min()) - 1.0
        zhi = float(stl[..., 2].max()) + 1.0
        fx = [CS.read_stl(str(p)) for p in sorted(W.glob(f"{su}_fix*.stl"), key=lambda q: int(q.stem.split("fix")[1]))]
        for t in fx:
            zlo, zhi = min(zlo, float(t[..., 2].min()) - 1), max(zhi, float(t[..., 2].max()) + 1)
        grid = Grid((x0, y0, zlo), (x1, y1, zhi), h)

        def top(tris):
            occ = CS.voxelize(tris, grid)
            any_ = occ.any(axis=2)
            k = occ.shape[2] - 1 - np.argmax(occ[:, :, ::-1], axis=2)
            return np.where(any_, grid.c[2][k] + h / 2, -np.inf).astype(np.float32)
        stock_top = top(stl)
        ftops = [top(t) for t in fx]
        names = geo["setups"][su]["fixtures"]
        fix_top = np.max(np.stack(ftops), axis=0) if ftops else np.full(stock_top.shape, -np.inf, np.float32)
        fix_lab = np.argmax(np.stack(ftops), axis=0) if ftops else np.zeros(stock_top.shape, int)
        zc = np.full(stock_top.shape, np.inf, np.float32)
        t0 = time.time()
        per_tool, hits = HC.sweep(None, moves, stock_top, fix_top, fix_lab, names, grid.lo[0] + h / 2, grid.lo[1] + h / 2, h, zc)
        hits = HC.merge_hits(hits)
        tools = {}
        for t, rec in per_tool.items():
            segs, gl = HC.assembly(t)
            tools["T%d" % t] = dict(stock=rec["stock"], fixture=rec["fixture"], by_part=rec["by_part"], gauge_length_mm=round(gl, 2),
                                    holder=HC.CUTTERS[t]["holder"], stick_out_mm=HC.CUTTERS[t].get("stick", CS.FC.TOOLS[t]["length"]))
        out["setups"][su] = dict(moves=len(moves), seconds=round(time.time() - t0, 1), n_collisions=len(hits), collisions=hits[:10],
                                 rapids_through_stock=[x for x in hits if x["rapid"] and x["part"] == "flutes" and x["against"] == "stock"],
                                 tools=tools)
        print(su, len(moves), "moves", len(hits), "collisions", {k: (v["stock"]["c"], v["stock"]["part"], v["fixture"]["c"], v["fixture"].get("what"))
                                                                for k, v in tools.items()}, flush=True)
    (W / "holders.json").write_text(json.dumps(out, indent=1, default=float))


# ---------------------------------------------------------------------------------------------------------------- summary
def summary():
    geo = json.loads((W / "geometry.json").read_text())
    fc = json.loads((W / "freecad_cam_lp.json").read_text())
    sim_ = json.loads((W / "sim.json").read_text()) if (W / "sim.json").exists() else None
    hc = json.loads((W / "holders.json").read_text()) if (W / "holders.json").exists() else None
    setups = {}
    for s in fc["parts"].values():
        for r in s["setups"]:
            setups[r["setup"]] = dict(program=str(gcode_name(r["setup"]).relative_to(REPO)), totals=r["totals"],
                                      ops=[{k: m.get(k) for k in ("label", "kind", "tool", "tool_name", "feed_mm_min", "start_depth",
                                                                  "final_depth", "cut_time_min", "rapid_time_min", "error")} for m in r["ops"]])
    res = dict(what="LP in the chamber lid (lp_cam.py): the Ø24 bore on the line of sight on a sine plate, the face groove and the "
                    "adapter's M4 holes flat; FreeCAD 1.0.2, CAMotics 1.2.0 and holder_check.sweep(), the repo's own code",
               geometry={k: v for k, v in geo.items() if k != "setups"}, frames={k: dict(R=v["R"], origin=v["origin"], bbox=v["bbox"],
                                                                                        fixtures=v["fixtures"], bore_z=v.get("bore_z"))
                                                                                for k, v in geo["setups"].items()},
               setups=setups, new_tools={"T%d" % k: dict(v, cutter=NEW_CUTTERS[k]) for k, v in NEW_TOOLS.items()})
    if sim_:
        res["camotics"] = {k: v for k, v in sim_.items() if k != "setups"}
        res["camotics"]["setups"] = {k: dict(seconds=v["camotics"]["seconds"], errors=v["camotics"]["errors"],
                                             removed_from_stock_mm3=v["removed_from_stock_mm3"]) for k, v in sim_["setups"].items()}
    if hc:
        res["holder_check"] = hc
    cmj = OUT / "cam_monitoring.json"
    cm = json.loads(cmj.read_text())
    cm["LP"] = res
    cmj.write_text(json.dumps(cm, indent=1))
    print(json.dumps({k: (v["totals"]["total_min"], v["totals"]["tool_changes"]) for k, v in setups.items()}))
    if sim_:
        print("CAMotics", {k: res["camotics"][k] for k in ("stock_mm3", "target_mm3", "final_mm3", "pieces")},
              "gouge", {k: v for k, v in res["camotics"]["gouge"].items() if k != "regions"},
              "leftover", {k: v for k, v in res["camotics"]["leftover"].items() if k != "regions"})
    if hc:
        for k, v in hc["setups"].items():
            print("holders", k, v["n_collisions"], {t: (x["stock"]["c"], x["fixture"]["c"]) for t, x in v["tools"].items()})


if __name__ == "__main__":
    mode = os.environ.get("MON_CAM_MODE") or (sys.argv[1] if len(sys.argv) > 1 else "")
    dict(prep=prep, post=post, post2=post2, sim=sim, holders=holders, summary=summary)[mode]()
