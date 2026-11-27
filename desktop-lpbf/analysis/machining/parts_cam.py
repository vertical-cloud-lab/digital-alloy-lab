"""CAM for chapter 31's vise part in FreeCAD 1.0's CAM workbench, headless, as freecad_cam.py does for the chamber
(robot-build round 9, issue #260, PR #266). Sterling on round 7: "dummy tool paths instead of real ones"; round 8 gave
chapter 30 (the chamber frame and floor plate) its posted programs, and chapter 31 kept only a clock: "the vise bracket
has no posted program, so its invented path is gone and only the clock runs".

The parts chapter 31 shows (analysis/shop/shop_clips.py)
    * clip_vise_part: arm A sets "a typical vise part: the recoater motor bracket's blank (2.5 in. 6061 plate)" in the
      Kurt XL6A air vise on the VF-4.
    * clip_lathe_slug: arm A loads a 2-1/8 in. 6061 bar slug (54 x 100) into the ST-10's chuck.

The bracket (programmed here)
    Finished geometry, from the model: cad/lpbf_low.py's "Recoater motor bracket", box(x_m0 - 90, x_m0, ry - 30, ry + 30,
    zb1, rz - 29.6): a 90 x 60 x 170.4 mm block of 6061 under the recoater servo (dfm.json: 920.2 cm3, 6 faces, no holes;
    joints.py: its screws are "M4 per the vendor hole patterns; not drawn", so no holes are programmed). Stock, from the
    shop plan (setup_plan.json and dfm.json): "2.5 in. plate, 96 x 176 mm", two 3-axis setups (+z, -z).
    CAM frame ("bracket frame", mm): the block lying flat in the vise as op 1 holds it, its 90 mm along X (across the
    jaws), 170.4 along Y, 60 along Z; origin at the centre of its bottom face (the model's x, z, y). The blank is
    96 x 176 x 63.5, centred, z -1.75 .. 61.75 (1.75 mm to face off each side).
    Workholding (shop_clips.clip_vise_part's vise): the Kurt XL6A's 1.75 in. jaws, the blank on a 1 in. parallel.
      op 1 (bracket_op1.ngc, +z up): gripped across the blank's 96 mm, its bottom 19.05 mm in the jaws. Face the top to
        z 60 (T1), then the outline 90 x 170.4 from z 60 down to z 21 (T2, rough 0.3 mm radial then finish, two 19.5 mm
        passes each): 3.7 mm above the jaws' top (z 17.3).
      op 2 (bracket_op2.ngc, turned over about X, as freecad_cam's setup B): gripped across the finished 90 mm faces.
        Face the bottom to z 0 (60 thick), then the outline from z 0 to z 21.5 (setup z 0 to -21.5), 0.5 mm over op 1's.
    Tools: the chamber's own T1 (2.5 in. face mill) and T2 (3/4 in. 3-flute carbide end mill, tooling-bom A5, 38.1 mm of
    flute, 66 mm out of an ER32 collet chuck), freecad_cam.TOOLS, so the VF-4 in the video carries the same tools.

The slug (not programmed)
    FreeCAD 1.0.2's CAM workbench has no turning operations (its ops are milling, drilling, engraving and probing; the
    lathe addons are not part of the AppImage), so there is no posted program for the lathe. The turned profile drawn in
    chapter 31 stays illustrative.

Run (FreeCAD 1.0.2, the official conda AppImage, sha256 checked against the release's SHA256 file, extracted with
--appimage-extract under /tmp, as freecad_cam.py):
    FREECADCMD=/path/to/squashfs-root/usr/bin/freecadcmd python3 desktop-lpbf/analysis/machining/parts_cam.py
        -> /tmp/parts-cam/gcode/bracket_op1.ngc, bracket_op2.ngc and desktop-lpbf/analysis/out/machining/gcode/parts/
           parts_cam.json (per op: FreeCAD's CycleTime and the G-code recount, freecad_cam.gcode_times)
    Copy the two .ngc files into desktop-lpbf/analysis/out/machining/gcode/parts/ (committed).
    /tmp/venv/bin/python desktop-lpbf/analysis/machining/parts_cam.py --sim [--res 0.5]
        -> parts_sim.json next to them: each program parsed, timed and cut with cad/robotbuild/gcode_sim.py's cutter on
           a voxel grid (minutes against the CAM's, removed volume against blank minus part)
"""
import json
import math
import os
import subprocess
import sys

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:  # exec'd without a file name
    HERE = os.getcwd()
sys.path.insert(0, HERE)
import freecad_cam as FC  # noqa: E402  (plain Python at import: TOOLS, feeds, the recount, rot_matrix)

LPBF = os.path.normpath(os.path.join(HERE, "..", ".."))
WORK = os.environ.get("PARTS_CAM_WORK", "/tmp/parts-cam")
GCODE_TMP = os.path.join(WORK, "gcode")
PARTS_DIR = os.path.join(LPBF, "analysis", "out", "machining", "gcode", "parts")
OUT_JSON = os.path.join(PARTS_DIR, "parts_cam.json")
SIM_JSON = os.path.join(PARTS_DIR, "parts_sim.json")

# the finished part (bracket frame) and the blank: (x0, x1, y0, y1, z0, z1)
PART = (-45.0, 45.0, -85.2, 85.2, 0.0, 60.0)
BLANK = (-48.0, 48.0, -88.0, 88.0, -1.75, 61.75)
PLATE_IN = 2.5
JAW_H = 1.75 * FC.IN          # Kurt XL6A jaw height (equipment.kurt_xl6a)
PARALLEL = 1.0 * FC.IN        # the blank on a 1 in. parallel (shop_clips.clip_vise_part)
TOOLS = {t: FC.TOOLS[t] for t in (1, 2)}
Z_MEET = 21.0                 # op 1's outline stops here; op 2's comes up to Z_MEET + 0.5
SETUPS = [
    dict(name="bracket_op1", flip=False, grip_mm=96.0, ops=[
        ("Face the top to z 60", "face", 1, None, dict(face="top", start=61.75, final=60.0, step=1.75)),
        ("Outline 90 x 170.4 rough 0.3 mm radial, z 60 to 21", "profile", 2, None,
         dict(face="top", start=60.0, final=Z_MEET, step=19.5, extra=0.3)),
        ("Outline 90 x 170.4 finish, z 60 to 21", "profile", 2, None,
         dict(face="top", start=60.0, final=Z_MEET, step=19.5, extra=0.0)),
    ]),
    dict(name="bracket_op2", flip=True, grip_mm=90.0, ops=[
        ("Face the bottom to 60 thick", "face", 1, None, dict(face="top", start=1.75, final=0.0, step=1.75)),
        ("Outline rough 0.3 mm radial, the last 21.5 mm", "profile", 2, None,
         dict(face="top", start=0.0, final=-(Z_MEET + 0.5), step=21.5, extra=0.3)),
        ("Outline finish, the last 21.5 mm", "profile", 2, None,
         dict(face="top", start=0.0, final=-(Z_MEET + 0.5), step=21.5, extra=0.0)),
    ]),
]


def rot_of(name):
    """model (bracket frame) -> setup rotation, rows = setup axes (freecad_cam.rot_matrix's convention)"""
    su = next(s for s in SETUPS if s["name"] == name)
    return FC.rot_matrix(dict(flip=su["flip"]))


def vise_pose(name):
    """(x of the part's centre from the fixed jaw's face, z of the part frame's origin above the vise floor), and the
    rotation part frame -> vise frame (z up): op 1 with the blank's bottom on the parallel and its -x side on the fixed
    jaw; op 2 turned over about x, the finished top (z 60) on the parallel and the 90 mm faces in the jaws."""
    if name == "bracket_op1":
        return BLANK[1], PARALLEL - BLANK[4], ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    return PART[1], PARALLEL + PART[5], ((1, 0, 0), (0, -1, 0), (0, 0, -1))


# ------------------------------------------------------------------------------------------------ FreeCAD
def run_cam():
    import FreeCAD
    import Part
    import Path.Main.Job as PathJob
    import Path.Main.Stock as PathStock
    import Path.Op.MillFace
    import Path.Op.Profile
    import Path.Tool.Bit as PathToolBit
    import Path.Tool.Controller as PathToolController
    from Path.Post.scripts import linuxcnc_post

    os.makedirs(GCODE_TMP, exist_ok=True)
    doc = FreeCAD.newDocument("parts_cam")
    x0, x1, y0, y1, z0, z1 = PART
    part = Part.makeBox(x1 - x0, y1 - y0, z1 - z0, FreeCAD.Vector(x0, y0, z0))
    results = []
    for su in SETUPS:
        shp = part.copy()
        if su["flip"]:
            shp.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 180)
        model = doc.addObject("Part::Feature", su["name"] + "_model")
        model.Shape = shp
        doc.recompute()
        job = PathJob.Create("Job_" + su["name"], [model])
        job.PostProcessor = "linuxcnc"
        job.PostProcessorArgs = "--no-show-editor --precision 3"
        for tc in list(job.Tools.Group):
            job.Tools.removeObject(tc)
        bx0, bx1, by0, by1, bz0, bz1 = BLANK
        lo = -bz1 if su["flip"] else bz0
        old = job.Stock
        job.Stock = PathStock.CreateBox(job, FreeCAD.Vector(bx1 - bx0, by1 - by0, bz1 - bz0),
                                        FreeCAD.Placement(FreeCAD.Vector(bx0, by0 if not su["flip"] else -by1, lo),
                                                          FreeCAD.Rotation()))
        doc.removeObject(old.Name)
        base = job.Model.Group[0]
        doc.recompute()
        top = max((("Face%d" % (i + 1), f) for i, f in enumerate(base.Shape.Faces)
                   if abs(f.normalAt(0, 0).z - 1) < 1e-6), key=lambda c: c[1].BoundBox.ZMax)[0]
        tcs = {}
        ops_meta = []
        for label, kind, t, ipt, cfg in su["ops"]:
            label = FC.clean_label(label)
            if t not in tcs:
                spec = TOOLS[t]
                bit = PathToolBit.Factory.Create("T%d" % t, spec["shape"] + ".fcstd")
                bit.Diameter = spec["d"]
                bit.Length = spec["length"]
                bit.CuttingEdgeHeight = spec["edge"]
                tc = PathToolController.Create("TC%d_%s" % (t, su["name"]), bit, t)
                f = FC.feed_mm_min(t, ipt)
                tc.HorizFeed = "%f mm/min" % f
                tc.VertFeed = "%f mm/min" % (0.5 * f)
                tc.HorizRapid = "%f mm/min" % FC.RAPID_MM_MIN
                tc.VertRapid = "%f mm/min" % FC.RAPID_MM_MIN
                tc.SpindleSpeed = spec["rpm"]
                tc.SpindleDir = "Forward"
                job.Proxy.addToolController(tc)
                tcs[t] = tc
            if kind == "face":       # as freecad_cam.py: the face's bounding box plus the tool radius, zig-zag along x
                op = Path.Op.MillFace.Create("Face", parentJob=job)
                op.BoundaryShape = "Boundbox"
                op.StepOver = 70
                op.ClearEdges = True
                op.ZigZagAngle = 0.0
            else:                    # the outline: the top face's outer wire, the tool outside it
                op = Path.Op.Profile.Create("Profile", parentJob=job)
                op.processPerimeter = True
                op.processHoles = False
                op.processCircles = False
                op.Side = "Outside"
                op.OffsetExtra = cfg.get("extra", 0.0)
            op.Base = [(base, [top])]
            op.Label = label
            op.ToolController = tcs[t]
            if hasattr(op, "CoolantMode"):
                op.CoolantMode = "Flood"
            for prop, val in (("StartDepth", cfg["start"]), ("FinalDepth", cfg["final"]), ("StepDown", cfg["step"])):
                op.setExpression(prop, None)
                setattr(op, prop, val)
            ops_meta.append((op, dict(op=op.Name, label=label, kind=kind, tool=t, tool_name=TOOLS[t]["name"],
                                      rpm=TOOLS[t]["rpm"], feed_mm_min=round(FC.feed_mm_min(t, ipt), 1),
                                      start_depth=cfg["start"], final_depth=cfg["final"], step_down=cfg["step"],
                                      offset_extra=cfg.get("extra"))))
        doc.recompute()
        posted, cur = [], None
        for op, meta in ops_meta:
            meta["freecad_cycle_time"] = getattr(op, "CycleTime", None)
            meta["commands"] = len(op.Path.Commands)
            if not meta["commands"]:
                meta["error"] = "operation produced no path"
                continue
            if op.ToolController.ToolNumber != cur:
                posted.append(op.ToolController)
                cur = op.ToolController.ToolNumber
            posted.append(op)
        job.recompute()
        gpath = os.path.join(GCODE_TMP, su["name"] + ".ngc")
        gcode = linuxcnc_post.export(posted, gpath, "--no-show-editor --precision 3")
        if not gcode:
            gcode = open(gpath).read()
        results.append(dict(setup=su["name"], flip=su["flip"], rotation_model_to_setup=[list(r) for r in rot_of(su["name"])],
                            grip_mm=su["grip_mm"], gcode=gpath, freecad_job_cycle_time=getattr(job, "CycleTime", None),
                            ops=[m for _, m in ops_meta], _gcode_text=gcode))
        print("setup", su["name"], "job CycleTime", getattr(job, "CycleTime", None), flush=True)
    return FreeCAD.Version(), results


def summarise(version, results):
    out = dict(
        what="chapter 31's vise part, the recoater motor bracket, programmed in FreeCAD's CAM workbench "
             "(analysis/machining/parts_cam.py); the lathe slug is not programmed (FreeCAD 1.0.2 has no turning ops)",
        tool="FreeCAD %s (%s), CAM workbench, run headless with freecadcmd" % (".".join(version[:3]), version[3]),
        post="linuxcnc (--precision 3), mm; programs in analysis/out/machining/gcode/parts/",
        machine="Haas VF-4, Kurt XL6A air vise (1.75 in. jaws), the blank on a 1 in. parallel",
        material="6061-T6",
        part=dict(name="Recoater motor bracket", model="cad/lpbf_low.py: box 90 x 60 x 170.4 (no holes drawn)",
                  frame="bracket frame: 90 along X, 170.4 along Y, 60 along Z, origin at the bottom face's centre",
                  box_mm=PART, volume_cm3=round((PART[1] - PART[0]) * (PART[3] - PART[2]) * (PART[5] - PART[4]) / 1000, 1)),
        blank=dict(spec="2.5 in. 6061 plate, 96 x 176 mm (setup_plan.json, dfm.json)", box_mm=BLANK,
                   volume_cm3=round((BLANK[1] - BLANK[0]) * (BLANK[3] - BLANK[2]) * (BLANK[5] - BLANK[4]) / 1000, 1)),
        tools={("T%d" % t): dict(v, feed_mm_min=round(FC.feed_mm_min(t), 1)) for t, v in TOOLS.items()},
        assumptions=[
            "Feeds as freecad_cam.py: mm/min = rpm x flutes x chip load x 25.4; plunge at half the horizontal feed.",
            "Face: BoundaryShape Boundbox with ClearEdges (the face's box plus the tool radius), 70 % step-over, "
            "zig-zag along x.",
            "Outline: Profile on the top face's outer wire, the tool outside; rough with 0.3 mm left, then finish, "
            "each in two 19.5 mm steps (op 1) or one 21.5 mm step (op 2), inside T2's 38.1 mm of flute.",
            "No lead-in or lead-out dressups (the profile plunges at its start point, outside the part, in the 3 mm "
            "of stock round it); no chamfers or deburring; the model's screw holes are not drawn, so none are cut.",
            "Times: the G-code recount (feeds as programmed, rapids at 25.4 m/min); tool changes counted, not timed.",
        ],
        setups=[],
    )
    for r in results:
        times, ntc = FC.gcode_times(r.pop("_gcode_text"))
        tot = dict(feed_mm=0.0, rapid_mm=0.0, feed_s=0.0, rapid_s=0.0)
        fc_total = 0
        for m in r["ops"]:
            g = times.get(m["label"]) or times.get(m["op"])
            if g:
                m["path_feed_mm"] = round(g["feed_mm"], 1)
                m["path_rapid_mm"] = round(g["rapid_mm"], 1)
                m["cut_time_min"] = round(g["feed_s"] / 60, 2)
                m["rapid_time_min"] = round(g["rapid_s"] / 60, 2)
                for k in tot:
                    tot[k] += g[k]
            ct = m.get("freecad_cycle_time")
            if ct and ct.count(":") == 2:
                h, mi, s = (int(x) for x in ct.split(":"))
                fc_total += 3600 * h + 60 * mi + s
        r["gcode"] = "analysis/out/machining/gcode/parts/" + os.path.basename(r["gcode"])
        r["totals"] = dict(path_feed_mm=round(tot["feed_mm"], 1), path_rapid_mm=round(tot["rapid_mm"], 1),
                           cut_time_min=round(tot["feed_s"] / 60, 2), rapid_time_min=round(tot["rapid_s"] / 60, 2),
                           total_min=round((tot["feed_s"] + tot["rapid_s"]) / 60, 2), tool_changes=ntc,
                           freecad_sum_of_op_cycle_times_min=round(fc_total / 60, 2))
        out["setups"].append(r)
    out["total_min"] = round(sum(r["totals"]["total_min"] for r in out["setups"]), 2)
    return out


# ------------------------------------------------------------------------------------------------ the simulation
def _sim_modules():
    rb = os.path.join(LPBF, "cad", "robotbuild")
    if rb not in sys.path:
        sys.path.insert(0, rb)
    import camotics_sim as CS
    import gcode_sim as GS
    lo = (BLANK[0] - 3.0, BLANK[2] - 3.0, BLANK[4] - 3.0)
    hi = (BLANK[1] + 3.0, BLANK[3] + 3.0, BLANK[5] + 3.0)
    CS.GRID_LO.setdefault("bracket", lo)       # camotics_sim.Grid takes its box by part name
    CS.GRID_HI.setdefault("bracket", hi)
    return CS, GS


def tools_gs():
    """T -> dict(d, length, shape, name), gcode_sim.tools()'s format"""
    return {t: dict(d=float(v["d"]), length=float(v["length"]), shape=v["shape"], name=v["name"]) for t, v in TOOLS.items()}


def program(name):
    """gcode_sim.Program for a posted part program (gcode_sim.Program reads the chamber's freecad_cam.json; this builds
    the same object, same parse and timing, from this file's setups and tools)"""
    import numpy as np
    CS, GS = _sim_modules()
    p = GS.Program.__new__(GS.Program)
    p.name = name
    p.rot = np.array(rot_of(name), float)
    p.src = "parts/%s.ngc" % name
    p.text = open(os.path.join(PARTS_DIR, name + ".ngc")).read()
    p.a_deg, p.index_lines = None, None
    _, moves = CS.expand(p.text)
    T = tools_gs()
    p0, p1, dur, rapid, tool, line, op = [], [], [], [], [], [], []
    p.ops = []
    opi = {}
    for mv in moves:
        if mv["tool"] is None:
            continue
        pts = CS.segments(mv, chord=GS.CHORD)
        o = opi.setdefault(mv["op"], len(opi))
        if o == len(p.ops):
            p.ops.append(mv["op"])
        for a_, b_ in zip(pts[:-1], pts[1:]):
            d = float(np.linalg.norm(b_ - a_))
            if d < 1e-9:
                continue
            v = GS.RAPID if mv["rapid"] else (mv["feed"] or GS.RAPID)
            p0.append(a_)
            p1.append(b_)
            dur.append(d / v * 60.0)
            rapid.append(mv["rapid"])
            tool.append(mv["tool"])
            line.append(mv["src_line"])
            op.append(o)
    p.p0, p.p1 = np.array(p0), np.array(p1)
    p.dur = np.array(dur)
    p.t1 = np.cumsum(p.dur)
    p.t0 = p.t1 - p.dur
    p.len = np.linalg.norm(p.p1 - p.p0, axis=1)
    p.s1 = np.cumsum(p.len)
    p.rapid = np.array(rapid, bool)
    p.tool = np.array(tool, int)
    p.line = np.array(line, int)
    p.op = np.array(op, int)
    p.total_s = float(p.t1[-1])
    p.radius = np.array([T[t]["d"] / 2 for t in p.tool])
    p.cone = np.array([GS.DRILL_K if T[t]["shape"] == "drill" else 0.0 for t in p.tool])
    p.T = T
    return p


def grid_and_stock(res=0.5):
    CS, GS = _sim_modules()
    g = GS.make_grid("bracket", res)
    return g, g.box(*BLANK)


def simulate(res=0.5):
    import time
    import numpy as np
    from scipy import ndimage
    CS, GS = _sim_modules()
    t0 = time.time()
    cam = json.load(open(OUT_JSON))
    g, stock = grid_and_stock(res)
    initial = stock.copy()
    tgt = g.box(*PART)
    v3 = res ** 3 / 1000.0
    rows = {}
    for su in SETUPS:
        p = program(su["name"])
        c = GS.Cutter(p, g, stock)
        c.finish()
        new, freed = GS.drop_free(c.occupancy())
        ref = next(s for s in cam["setups"] if s["setup"] == su["name"])["totals"]
        rc = p.recount()
        rows[su["name"]] = dict(program="analysis/out/machining/gcode/parts/%s.ngc" % su["name"], **rc,
                                parts_cam_json_min=ref["total_min"],
                                freecad_estimate_min=ref["freecad_sum_of_op_cycle_times_min"],
                                timeline_vs_recount_min=round(rc["timeline_min"] - ref["total_min"], 3),
                                removed_cm3=round(float((stock & ~new).sum()) * v3, 2),
                                gouge_cm3=round(float((stock & ~new & tgt).sum()) * v3, 3),
                                tools=sorted(set(int(t) for t in p.tool)),
                                pieces_dropped_cm3=[round(v * v3, 2) for v in freed])
        print(su["name"], rows[su["name"]], flush=True)
        stock = new
    out = dict(what="the bracket's two posted programs parsed, timed and cut (parts_cam.py --sim, gcode_sim.py's "
                    "Cutter: flat-ended cylinders swept along every move, the tool axis the setup's z)",
               resolution_mm=res, setups=rows,
               blank_cm3_exact=round(np.prod([BLANK[1] - BLANK[0], BLANK[3] - BLANK[2], BLANK[5] - BLANK[4]]) / 1000, 2),
               part_cm3_exact=round(np.prod([PART[1] - PART[0], PART[3] - PART[2], PART[5] - PART[4]]) / 1000, 2))
    out["removed_exact_cm3"] = round(out["blank_cm3_exact"] - out["part_cm3_exact"], 2)
    out["initial_voxels_cm3"] = round(float(initial.sum()) * v3, 2)
    out["final_voxels_cm3"] = round(float(stock.sum()) * v3, 2)
    out["removed_sim_cm3"] = round(out["initial_voxels_cm3"] - out["final_voxels_cm3"], 2)
    out["removed_cad_voxels_cm3"] = round(float((initial & ~tgt).sum()) * v3, 2)
    out["removed_sim_vs_cad_pct"] = round(100.0 * (out["removed_sim_cm3"] - out["removed_cad_voxels_cm3"])
                                          / out["removed_cad_voxels_cm3"], 2)
    out["leftover_cm3"] = round(float((stock & ~tgt).sum()) * v3, 3)
    out["gouge_cm3"] = round(float((~stock & tgt).sum()) * v3, 3)
    far = stock & ~ndimage.binary_dilation(tgt, iterations=2)
    out["leftover_beyond_%gmm_cm3" % (2 * res)] = round(float(far.sum()) * v3, 3)
    deep = ndimage.binary_erosion(tgt, iterations=2) & ~stock
    out["gouge_beyond_%gmm_cm3" % (2 * res)] = round(float(deep.sum()) * v3, 3)
    out["minutes"] = dict(timeline=round(sum(r["timeline_min"] for r in rows.values()), 2),
                          recount=round(sum(r["recount_min"] for r in rows.values()), 2),
                          freecad_estimate=round(sum(r["freecad_estimate_min"] for r in rows.values()), 2))
    out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(SIM_JSON, "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "setups"}, indent=1))
    return out


def main():
    if "--sim" in sys.argv:
        res = float(sys.argv[sys.argv.index("--res") + 1]) if "--res" in sys.argv else 0.5
        simulate(res)
        return
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
    os.makedirs(PARTS_DIR, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    for r in out["setups"]:
        print(r["setup"], r["totals"])
        for m in r["ops"]:
            print("   ", m.get("label"), "|", m.get("error") or (m.get("cut_time_min"), m.get("rapid_time_min"),
                  m.get("freecad_cycle_time"), m.get("commands")))
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main()
