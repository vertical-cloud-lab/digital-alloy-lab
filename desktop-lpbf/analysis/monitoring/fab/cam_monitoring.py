"""CAM, CAMotics and the holder check for the monitoring ports in the chamber frame (issue #260, PR 281), with the repo's
own pipeline (analysis/machining: freecad_cam.py, camotics_sim.py, holder_check.py), unchanged.

frame_features.py draws the left-wall viewport (LW) and the back-wall light window (BW) on the frame, in the form setup C
can cut at its existing A indexes. This script programs them and checks the programs:

  post     run 1: freecad_cam.py as it is, on the frame as it was (frame_orig.brep): the six frame setups, i.e. the
           committed programs re-posted (FreeCAD's Adaptive moves ~0.01 mm between posts).
           run 2 (under freecadcmd): freecad_cam.run_cam() on the frame with the ports, for two jobs:
             * frame_C90 as it is. Its "wall" op finds every bore and hole normal to the left wall, so it programs the LW
               port (seat, bore, clamp-ring holes, purge port and passage) with the recoater bore and the through-beam;
             * mon_C180, new: the BW seat and slot (Adaptive inside their outlines) and its three clamp holes. The A180
               job's inlet-slot op profiles every inner wire of the back face, which would now include the seat's
               outline and cut it through the wall, so frame_C180 stays as run 1 posted it and mon_C180 follows it.
             The one change to freecad_cam.py's code, made in memory here and not in the file: an op whose settings carry
             "subs" (face or edge names) uses them instead of freecad_cam's own selectors.
           Joins setup C into one Haas program with the A moves: A0 door; A90 (run 2); A180 (run 1's frame_C180, then
           mon_C180); A270 (in /tmp: it is 0.75 MB, mostly the unchanged door block). The repo keeps the two programs the
           ports change, analysis/out/monitoring/fab/gcode/frame_C90_with_LW.ngc and mon_C180_BW.ngc.
  sim      camotics_sim.main() on the whole chain (frame B, A, C0, C90 with LW, C180, mon_C180, C270) against the frame
           with the ports: gouges, leftover, rapids through stock, CAMotics times. Its outputs go to /tmp, not to
           analysis/out/machining.
  holders  holder_check.main() on the same chain (holders, spindle, fixtures, travels).
  summary  what the ports add: ops, tools, programmed time, CAMotics and holder results, hours -> cam_monitoring.json.

Run (FreeCAD 1.0.2 conda AppImage extracted under /tmp, CAMotics image built from analysis/machining/camotics.Dockerfile):
  P=desktop-lpbf/analysis/monitoring/fab/cam_monitoring.py
  OMP_NUM_THREADS=1 /tmp/capmem 3 env FREECADCMD=/tmp/fab-e/freecad/squashfs-root/usr/bin/freecadcmd /tmp/venv/bin/python $P post
  OMP_NUM_THREADS=1 /tmp/capmem 3 sg docker -c "/tmp/venv/bin/python $P sim"      (CAMOTICS_MEM=3g CAMOTICS_CPUS=1)
  OMP_NUM_THREADS=1 /tmp/capmem 2 /tmp/venv/bin/python $P holders
  /tmp/venv/bin/python $P summary
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import types

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
MACH = REPO / "desktop-lpbf" / "analysis" / "machining"
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "monitoring" / "fab"
TMP = pathlib.Path(os.environ.get("MON_CAM_TMP", "/tmp/fab-e"))
CAM_IN = TMP / "cam-in"          # frame_features.py's output: frame.brep/.stl (with the ports), frame_orig.brep/.stl
RUN1 = TMP / "cam-orig"          # freecad_cam.py on the frame as it was
RUN2 = TMP / "cam-new"           # freecad_cam.run_cam() on the frame with the ports
CHAIN = TMP / "cam-chain"        # every program of the chain, the new frame's STL, and the merged freecad_cam.json
PARTS_JSON = TMP / "parts" / "parts.json"
CHAIN_NAMES = ["frame_B", "frame_A", "frame_C0", "frame_C90", "frame_C180", "mon_C180", "frame_C270"]
FROM_RUN2 = {"frame_C90", "mon_C180"}


def load_fc(patch=False):
    """freecad_cam.py as a module; with patch=True, ops may name their faces or edges ("subs" in their settings)"""
    src = (MACH / "freecad_cam.py").read_text()
    if patch:
        old = ('                if kind == "drill":\n'
               '                    add(label, kind, t, ipt, cfg, holes(part, cfg["holes"]))')
        new = ('                if "subs" in cfg:  # cam_monitoring.py: explicit face or edge names\n'
               '                    add(label, kind, t, ipt, cfg, cfg["subs"])\n'
               '                elif kind == "drill":\n'
               '                    add(label, kind, t, ipt, cfg, holes(part, cfg["holes"]))')
        assert src.count(old) == 1, "freecad_cam.py changed: the op dispatch this script patches is not there"
        src = src.replace(old, new)
    mod = types.ModuleType("freecad_cam")
    mod.__file__ = str(MACH / "freecad_cam.py")
    sys.modules["freecad_cam"] = mod
    exec(compile(src, str(MACH / "freecad_cam.py"), "exec"), mod.__dict__)
    return mod


def mon_c180_setup(FC, features):
    """the BW job at A180, with face and edge names read off the frame with the ports (FreeCAD side)"""
    import FreeCAD  # noqa: F401
    import Part
    s = Part.Shape()
    s.read(str(CAM_IN / "frame.brep"))

    def edge_names(wire):
        out = []
        for e in wire.Edges:
            out += ["Edge%d" % (i + 1) for i, e2 in enumerate(s.Edges) if e2.isSame(e)]
        return out

    planes_y = [(i, f) for i, f in enumerate(s.Faces) if type(f.Surface).__name__ == "Plane" and f.normalAt(0, 0).y > 0.999]
    outer = max((f for i, f in planes_y if abs(f.BoundBox.YMax - 111.0) < 0.01), key=lambda f: f.Area)
    seat_w = [w for w in outer.Wires if not w.isSame(outer.OuterWire) and w.BoundBox.XMax < -80 and w.BoundBox.DiagonalLength > 30]
    assert len(seat_w) == 1, "BW seat outline not found on the back face"
    seat_depth = features["BW"]["seat"]["depth"]
    floor = [f for i, f in planes_y if abs(f.BoundBox.YMax - (111.0 - seat_depth)) < 0.01 and f.BoundBox.XMax < -80]
    assert len(floor) == 1, "BW seat floor not found"
    slot_w = [w for w in floor[0].Wires if not w.isSame(floor[0].OuterWire)]
    assert len(slot_w) == 1, "BW slot outline not found on the seat floor"
    holes = []
    for x, z in features["BW"]["clamp_frame"]["holes_xz"]:
        for i, f in enumerate(s.Faces):
            su = f.Surface
            if type(su).__name__ == "Cylinder" and abs(abs(su.Axis.y) - 1) < 1e-6 and abs(su.Radius - 2.0) < 1e-3 \
                    and abs(su.Center.x - x) < 0.05 and abs(su.Center.z - z) < 0.05:
                holes.append("Face%d" % (i + 1))
                break
    assert len(holes) == len(features["BW"]["clamp_frame"]["holes_xz"]), "BW clamp holes not found"
    sl = features["BW"]["slot"]
    se = features["BW"]["seat"]
    return dict(name="mon_C180", part="frame", rot=FC.ROT_A[180], a_deg=180, rotary="frame_C",
                stock_box=FC._stock_box(FC.ROT_A[180]), clear_z=130.0, ops=[
        ("BW window seat %d x %d R%.0f, %.1f deep, adaptive" % (se["L"], se["W"], se["corner_r"], seat_depth), "adaptive_in", 9,
         None, dict(start=111.0, final=111.0 - seat_depth, step=seat_depth, stepover=15, subs=edge_names(seat_w[0]))),
        # T9 (1/4 in.), not T3: in the 20.5 mm slot a 1/2 in. tool leaves 7.8 mm for the tool centre and FreeCAD's Adaptive
        # found no helix entry ("Start point not found", no path; first post, 2026-11-25)
        ("BW slot %.1f x %.1f obround through, adaptive" % (sl["length"], sl["width"]), "adaptive_in", 9, None,
         dict(start=111.0 - seat_depth, final=94.5, step=6.0, stepover=15, subs=edge_names(slot_w[0]))),
        ("BW clamp-frame holes: drill %d x 3.3 mm, M4 tapped after, 10 deep" % len(holes), "drill", 6, None,
         dict(start=111.0, final=101.0, through=False, subs=holes)),
    ])


def post2():
    """run 2, inside freecadcmd"""
    FC = load_fc(patch=True)
    FC.IN_DIR = str(RUN2)
    FC.GCODE_DIR = str(RUN2 / "gcode")
    features = json.loads((OUT / "frame_features.json").read_text())
    c90 = next(su for su in FC.SETUPS if su["name"] == "frame_C90")
    FC.SETUPS = [c90, mon_c180_setup(FC, features)]
    version, results = FC.run_cam()
    out = FC.summarise(version, results)
    (RUN2 / "freecad_cam_run2.json").write_text(json.dumps(out, indent=1))
    print("run 2 written", flush=True)


def post():
    fcmd = os.environ.get("FREECADCMD")
    if not fcmd:
        sys.exit("set FREECADCMD")
    for d, brep in ((RUN1, CAM_IN / "frame_orig.brep"), (RUN2, CAM_IN / "frame.brep")):
        (d / "gcode").mkdir(parents=True, exist_ok=True)
        shutil.copy(brep, d / "frame.brep")
        shutil.copy(PARTS_JSON, d / "parts.json")
    env = dict(os.environ, CHAMBER_CAM_IN=str(RUN1), FREECAD_CAM_PARTS="frame", FREECAD_CAM_JSON=str(RUN1 / "freecad_cam.json"))
    if not (RUN1 / "freecad_cam.json").exists():
        subprocess.run([sys.executable, str(MACH / "freecad_cam.py")], env=env, check=True)
    code = "import runpy; runpy.run_path(%r, run_name='__main__')" % str(pathlib.Path(__file__).resolve())
    subprocess.run([fcmd, "-c", code], env=dict(os.environ, MON_CAM_MODE="post2"), check=True)
    # the chain: programs, the new frame's STL, and one freecad_cam.json in chain order
    (CHAIN / "gcode").mkdir(parents=True, exist_ok=True)
    j1 = json.loads((RUN1 / "freecad_cam.json").read_text())
    j2 = json.loads((RUN2 / "freecad_cam_run2.json").read_text())
    by = {s["setup"]: s for s in j1["parts"]["frame"]["setups"]}
    by.update({s["setup"]: s for s in j2["parts"]["frame"]["setups"]})
    for n in CHAIN_NAMES:
        shutil.copy((RUN2 if n in FROM_RUN2 else RUN1) / "gcode" / f"{n}.ngc", CHAIN / "gcode" / f"{n}.ngc")
    shutil.copy(CAM_IN / "frame.stl", CHAIN / "frame.stl")
    merged = dict(j1, parts=dict(frame=dict(setups=[by[n] for n in CHAIN_NAMES])))
    fake = CHAIN / "fake" / "out" / "machining"
    fake.mkdir(parents=True, exist_ok=True)
    (fake / "freecad_cam.json").write_text(json.dumps(merged, indent=1))
    # one Haas program for setup C
    sys.path.insert(0, str(MACH))
    FC = load_fc()
    blocks = [(by[n]["a_deg"], n, (CHAIN / "gcode" / f"{n}.ngc").read_text()) for n in CHAIN_NAMES if by[n].get("a_deg") is not None]
    txt = FC.haas_rotary_program(blocks, number=2661)
    txt = txt.replace("SETUP C = F-S3, THE FOUR WALLS ON THE HRT210)", "SETUP C = F-S3, THE FOUR WALLS + MONITORING PORTS LW, BW)")
    (CHAIN / "frame_C_haas_monitoring.nc").write_text(txt)       # 0.75 MB, mostly the unchanged A0 door block: kept in /tmp
    # the repo keeps only the two programs the ports change (the rest is analysis/out/machining/gcode/frame_C_haas.nc)
    (OUT / "gcode").mkdir(parents=True, exist_ok=True)
    for n in sorted(FROM_RUN2):
        shutil.copy(CHAIN / "gcode" / f"{n}.ngc", OUT / "gcode" / f"{n}{'_with_LW' if n == 'frame_C90' else '_BW'}.ngc")
    print("wrote", CHAIN / "frame_C_haas_monitoring.nc", "tool changes", FC.haas_rotary_program.tool_changes)


def chain_setups(FC):
    """the chain's setup dicts (freecad_cam's own, plus mon_C180 rebuilt without FreeCAD: only its frame data is needed)"""
    by = {su["name"]: su for su in FC.SETUPS}
    by["mon_C180"] = dict(name="mon_C180", part="frame", rot=FC.ROT_A[180], a_deg=180, rotary="frame_C",
                          stock_box=FC._stock_box(FC.ROT_A[180]), clear_z=130.0, ops=[])
    FC.FIXTURES["mon_C180"] = FC.FIXTURES["frame_C180"]
    return [by[n] for n in CHAIN_NAMES]


def sim():
    sys.path.insert(0, str(MACH))
    os.environ.setdefault("CAMOTICS_MEM", "3g")
    os.environ.setdefault("CAMOTICS_CPUS", "1")
    os.environ["CHAMBER_CAM_IN"] = str(CHAIN)
    os.environ["CAMOTICS_WORK"] = str(TMP / "cam-sim")
    FC = load_fc()
    import camotics_sim as CS
    FC.SETUPS = chain_setups(FC)
    CS.FC = FC
    CS.IN_DIR = CHAIN
    CS.WORK = TMP / "cam-sim"
    CS.OUT = TMP / "cs-out"
    CS.HERE = CHAIN / "fake" / "machining"        # camotics_sim reads and updates HERE/../out/machining/freecad_cam.json
    CS.DOCKER_MEM = os.environ["CAMOTICS_MEM"]
    CS.DOCKER_CPUS = os.environ["CAMOTICS_CPUS"]
    sys.argv = ["camotics_sim.py", "--parts", "frame"]
    CS.main()


def holders():
    sys.path.insert(0, str(MACH))
    os.environ["CHAMBER_CAM_IN"] = str(CHAIN)
    os.environ["CAMOTICS_WORK"] = str(TMP / "cam-sim")
    FC = load_fc()
    import camotics_sim as CS
    import holder_check as HC
    FC.SETUPS = chain_setups(FC)
    CS.FC = FC
    HC.FC = FC
    HC.IN_DIR = CHAIN
    sys.argv = ["holder_check.py", "--parts", "frame", "--out", str(TMP / "holder_check_monitoring.json")]
    HC.main()


def summary():
    feats = json.loads((OUT / "frame_features.json").read_text())
    j1 = json.loads((RUN1 / "freecad_cam.json").read_text())
    j2 = json.loads((RUN2 / "freecad_cam_run2.json").read_text())
    cs = json.loads((TMP / "cs-out" / "camotics_sim.json").read_text()) if (TMP / "cs-out" / "camotics_sim.json").exists() else None
    hc = json.loads((TMP / "holder_check_monitoring.json").read_text()) if (TMP / "holder_check_monitoring.json").exists() else None
    s1 = {s["setup"]: s for s in j1["parts"]["frame"]["setups"]}
    s2 = {s["setup"]: s for s in j2["parts"]["frame"]["setups"]}
    old90 = {m["label"] for m in s1["frame_C90"]["ops"]}
    new_ops = [dict(setup="frame_C90", **{k: m.get(k) for k in ("label", "kind", "tool", "tool_name", "feed_mm_min", "start_depth",
                                                               "final_depth", "cut_time_min", "rapid_time_min", "error")})
               for m in s2["frame_C90"]["ops"] if m["label"] not in old90]
    new_ops += [dict(setup="mon_C180", **{k: m.get(k) for k in ("label", "kind", "tool", "tool_name", "feed_mm_min", "start_depth",
                                                                "final_depth", "cut_time_min", "rapid_time_min", "error")})
                for m in s2["mon_C180"]["ops"]]
    t_old90 = s1["frame_C90"]["totals"]["total_min"]
    t_new90 = s2["frame_C90"]["totals"]["total_min"]
    t_c180 = s2["mon_C180"]["totals"]["total_min"]
    res = dict(
        what="the LW and BW ports programmed in setup C (frame_features.py's geometry), FreeCAD 1.0.2 + CAMotics 1.2.0 + "
             "holder_check.py, all from analysis/machining, unchanged",
        recount=dict(frame_C90_before_min=t_old90, frame_C90_with_LW_min=t_new90, LW_added_min=round(t_new90 - t_old90, 2),
                     mon_C180_BW_min=t_c180, tool_changes_C90_before=s1["frame_C90"]["totals"]["tool_changes"],
                     tool_changes_C90_with_LW=s2["frame_C90"]["totals"]["tool_changes"],
                     tool_changes_mon_C180=s2["mon_C180"]["totals"]["tool_changes"]),
        new_ops=new_ops, features=dict(LW=feats["LW"], BW=feats["BW"], checks=feats["checks"]))
    if cs:
        res["camotics"] = dict(
            part=cs["parts"].get("frame"),
            setups={n: dict(removed_cm3=v["removed_cm3"], n_rapids_through_stock=v["n_rapids_through_stock"],
                            rapids=v["rapids_through_stock"][:10], time=v["time"], drills=v["drills"],
                            pieces_free_after_setup_cm3=v["pieces_free_after_setup_cm3"])
                    for n, v in cs["setups"].items()})
    if hc:
        res["holder_check"] = dict(
            setups={n: dict(n_collisions=v["n_collisions"], collisions=v["collisions"][:10],
                            tools={t: dict(stock=tv["min_clearance_to_stock_mm"], fixtures=tv["min_clearance_to_fixtures_mm"],
                                           holder=tv["holder"], stick_out_mm=tv["stick_out_mm"], tight=tv["tight"])
                                   for t, tv in v["tools"].items()}, travel=v["travel"])
                    for n, v in hc["setups"].items() if n in FROM_RUN2},
            stock_vs_model=hc.get("stock_vs_model"), stock_vs_camotics=hc.get("stock_vs_camotics"))
    (OUT / "cam_monitoring.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res["recount"], indent=1))
    for m in new_ops:
        print(m["setup"], m["label"], m.get("cut_time_min"), m.get("rapid_time_min"), m.get("error") or "")
    if cs:
        print("CAMotics frame:", {k: v for k, v in cs["parts"]["frame"].items() if k not in ("gouges", "leftovers", "loose_pieces")})
    if hc:
        for n, v in res["holder_check"]["setups"].items():
            print("holders", n, v["n_collisions"], {t: (x["stock"]["c"], x["fixtures"]["c"]) for t, x in v["tools"].items()})


if __name__ == "__main__":
    mode = os.environ.get("MON_CAM_MODE") or (sys.argv[1] if len(sys.argv) > 1 else "")
    dict(post=post, post2=post2, sim=sim, holders=holders, summary=summary)[mode]()
