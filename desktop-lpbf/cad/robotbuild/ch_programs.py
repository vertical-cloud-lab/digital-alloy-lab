"""Chapter 31b of the robot-built video (round 9, issue #260, PR #266): the vise bracket cut by its posted programs.

Sterling on round 7: "dummy tool paths instead of real ones". Round 8 gave chapter 30 the chamber's posted programs;
chapter 31 (shop_chapters.py) still had none: "the vise bracket has no posted program, so its invented path is gone and
only the clock runs". This chapter follows 31 under the same chapter title (so the YouTube chapter list gains no entry)
and plays the bracket's two programs the way chapter 30 plays the chamber's:

* the part: chapter 31's vise part, the recoater motor bracket (cad/lpbf_low.py: a 90 x 60 x 170.4 block), from its
  96 x 176 mm blank of 2.5 in. 6061 (setup_plan.json), programmed in FreeCAD 1.0.2's CAM workbench by
  analysis/machining/parts_cam.py: analysis/out/machining/gcode/parts/bracket_op1.ngc and bracket_op2.ngc;
* every cutting frame puts the tool where the program is at that frame's time (gcode_sim's parse and timing,
  parts_cam.program), the table carrying the part in X and Y and the head moving Z (shop_chapters.vf4_for), the stock as
  the program has cut it so far (gcode_sim.Cutter on a 0.75 mm grid) and the last ~0.2 m of path; the program and line
  are in each frame's sub, and every drawn position goes to analysis/out/machining/gcode/parts/parts_frames.json,
  re-checked against the re-parsed program at the end of the render;
* the camera rides on the table (chapter 30's cutting shots): the part stays still and the spindle moves over it;
* the Kurt XL6A is drawn at each program's grip (98 and 92 mm openings: its jaw plates stand 1 mm proud of the jaws),
  the blank on a 1 in. parallel; turning the part over between the programs is not planned, so it is a cut.

Imports shop_chapters.py, shop_scene.py, equipment.py and gcode_sim.py read-only.

Run (ROBOTBUILD_AUDIT=1 records every frame for scene_audit.py):
    ROBOTBUILD_AUDIT=1 OMP_NUM_THREADS=1 /tmp/memslot 3 xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python \
        desktop-lpbf/cad/robotbuild/ch_programs.py
    SHOP_PREVIEW_SUFFIX=-dbg SHOP_ONLY_FRAMES=0,200 ... ch_programs.py      (a few stills into their own folder)
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shop_chapters as SC  # noqa: E402  (read-only: Writer, Shop, VF4, vf4_for, trail_clear, ease)
from shop_scene import CM, E, Mst  # noqa: E402
import gcode_sim as GS  # noqa: E402

sys.path.insert(0, str(CM.LPBF / "analysis" / "machining"))
import parts_cam as PC  # noqa: E402

NAME = "31b-machining-programs"
TITLE = "Machining the other parts: vise, lathe, saw"       # chapter 31's title: no new YouTube chapter
FPS = CM.FPS
RES = 0.75                                                  # mm, the drawn stock's voxels (the check runs at 0.5)
SECONDS = {"bracket_op1": 30.0, "bracket_op2": 20.0}        # screen time per program
OPENING = {"bracket_op1": PC.BLANK[1] - PC.BLANK[0] + 2.0,  # the vise's nominal opening: the jaw plates stand 1 mm
           "bracket_op2": PC.PART[1] - PC.PART[0] + 2.0}    # proud of each jaw (equipment.kurt_xl6a)
CAM_OFF = np.array([270.0, -380.0, 430.0])                  # eye from the blank's centre under the spindle (station)
FRAMES_JSON = CM.LPBF / "analysis" / "out" / "machining" / "gcode" / "parts" / "parts_frames.json"
ROWS = []


def set_vise(vf4, opening):
    """The VF-4's vise group rebuilt at `opening` (VF4 draws it at 92); returns equipment.vf4's meta at table 0."""
    sc = vf4.sc
    for n in sc.members("vf4/vise"):
        sc.remove(n)
    parts, meta = E.vf4(door=1.0, table_x=0.0, with_vise=True, vise_open=opening, with_hrt=True)
    by = {}
    for n, p in parts.items():
        if n.startswith(("vise", "Kurt")):
            by.setdefault((p.color, p.opacity), []).append(p.mesh.transform(p.M, inplace=False))
    for i, ((c, op), ms) in enumerate(by.items()):
        sc.add(f"vf4/vise/{i}", E.merge(ms), c, group="vf4/vise", opacity=op)
    sc.parent["vf4/vise"] = "vf4/table"
    sc.gmat["vf4/vise"] = np.eye(4)
    vf4.set(vise=True)
    return meta


def set_parallel(vf4, meta, width):
    """The 1 in. parallel under the part (shop_clips.clip_vise_part's: 2 mm inside each jaw plate, 120 mm long)."""
    vx, yv, zf = meta["vise_x_fixed"], meta["vise_centre"][1], meta["vise_floor_z"]
    m = E.box(vx + 3.0, vx + 1.0 + width - 2.0, yv - 60.0, yv + 60.0, zf, zf + PC.PARALLEL)
    vf4.sc.add("vf4/fixture/parallel", m, "#8e979f", group="vf4/fixture")


def part_pose(name, meta):
    """bracket frame -> VF-4 station frame at table X 0 / Y 0, for program `name` (parts_cam.vise_pose)"""
    xoff, zoff, R = PC.vise_pose(name)
    M = np.eye(4)
    M[:3, :3] = np.array(R, float)
    M[:3, 3] = (meta["vise_x_fixed"] + 1.0 + xoff, meta["vise_centre"][1], meta["vise_floor_z"] + zoff)
    return M


class Stock:
    """The bracket's in-process stock (bracket frame) on parts_cam's grid."""

    def __init__(self, res=RES):
        self.g, self.occ = PC.grid_and_stock(res)

    def mesh(self, occ=None):
        m = GS.occ_mesh(self.occ if occ is None else occ, self.g)
        return m.compute_normals(split_vertices=False, consistent_normals=False, auto_orient_normals=False)

    def kg(self):
        return float(self.occ.sum()) * self.g.h ** 3 / 1e6 * 2.70


def run_program(w, scn, vf4, stock, name, Q, cap, secs, step):
    """One posted program on the VF-4, as shop_chapters.cut_program plays the chamber's: the cutter at the program's
    position every frame (time-lapse at the real minutes), the table and head as a VMC moves them, the stock cut so far,
    the last ~0.2 m of path; the camera riding on the table. Returns (minutes, camera function)."""
    sc = scn.sc
    g_obj, g_trail = "obj/bracket", "obj/bracket trail"
    prog = PC.program(name)
    T_ = PC.tools_gs()
    ax = Q[:3, :3] @ prog.rot.T @ np.array([0.0, 0.0, 1.0])
    if ax[2] < 0.999:
        raise RuntimeError(f"{name}: tool axis {ax} is not the station's vertical")
    c0 = np.array([(PC.BLANK[0] + PC.BLANK[1]) / 2, (PC.BLANK[2] + PC.BLANK[3]) / 2, (PC.BLANK[4] + PC.BLANK[5]) / 2])
    q0 = Q[:3, :3] @ c0 + Q[:3, 3]
    ref = (-q0[0], E.VF4["spindle_y"] - q0[1])
    Mv = Mst("vf4")
    F = np.array([0.0, E.VF4["spindle_y"], q0[2]])
    cam = [tuple((Mv @ np.r_[F + CAM_OFF, 1.0])[:3]), tuple((Mv @ np.r_[F + np.array([0, 0, 15.0]), 1.0])[:3]), (0, 0, 1)]

    def tcam():
        d = Mv[:3, :3] @ np.array([vf4.state["table_x"] - ref[0], vf4.state["table_y"] - ref[1], 0.0])
        return [tuple(np.asarray(cam[0], float) + d), tuple(np.asarray(cam[1], float) + d), cam[2]]

    cut = GS.Cutter(prog, stock.g, stock.occ)
    n = max(int(round(secs * FPS)), 12)
    factor = prog.total_s / (n / FPS)
    tool_now = None
    for k in range(n):
        t = (k + 1) / n * prog.total_s
        cut.advance(t)
        pos, i = prog.at(t)
        T = int(prog.tool[i])
        if T != tool_now:
            vf4.show_tool(T)
            tool_now = T
        tx, ty, z = SC.vf4_for(Q, prog.rot, pos, T)
        vf4.set(table_x=tx, table_y=ty, z=z)
        sc.set_mesh(g_obj, stock.mesh(cut.occupancy()))
        tr = prog.trail(t)
        if tr is not None:
            tr = SC.trail_clear(tr, pos, T_[T]["d"] / 2)
        if tr is not None:
            tube = SC.SS.pv.lines_from_points(tr @ prog.rot).tube(radius=0.9, n_sides=8)
            if g_trail not in sc.actors:
                sc.add(g_trail, tube, "#ff7a1a", group=g_trail, specular=0.0)
                sc.parent[g_trail] = "vf4/fixture"
            else:
                sc.set_mesh(g_trail, tube)
            sc.gmat[g_trail] = Q
            sc.alpha[g_trail] = 1.0
        elif g_trail in sc.actors:
            sc.alpha[g_trail] = 0.0
        ln = int(prog.line[i])
        label = prog.ops[int(prog.op[i])]
        ROWS.append(dict(chapter=NAME, chapter_frame=w.n_in, program=prog.src, setup=name, line=ln, t_s=round(t, 3),
                         work_xyz=[round(float(c), 4) for c in pos], tool=T, op=label, table_xy=[round(tx, 1), round(ty, 1)],
                         head_z=round(z, 1),
                         in_travel=bool(-635.0 <= tx <= 635.0 and -5.0 <= ty <= 513.0 and -1.0 <= z <= 636.0)))
        w.frame(scn, tcam(), cap, sub=f"{prog.src} line {ln}: T{T}, {label[:58]} | {factor:.1f}x time-lapse of "
                f"{prog.total_s / 60:.2f} min", who=["machine"], step=step, status="pass", proc_s=prog.total_s / n)
    cut.finish()
    occ, freed = GS.drop_free(cut.occupancy())
    stock.occ = occ
    sc.set_mesh(g_obj, stock.mesh())
    if g_trail in sc.actors:
        sc.alpha[g_trail] = 0.0
    z0 = vf4.state["z"]
    for i in range(8):
        vf4.set(z=z0 * (1 - SC.ease((i + 1) / 8)))
        w.frame(scn, tcam(), cap, sub=f"{prog.src}: program end, Z home (rapid)", who=["machine"], step=step,
                status="pass", proc_s=max(z0, 1.0) / (25400.0 / 60.0) / 8)
    return prog.total_s / 60.0, tcam


def setup_state(scn, vf4, stock, name, spec_path):
    """The vise, the parallel and the part for program `name`; the table where the program starts (its first point
    under the spindle), the tool it starts with, the head at Z home."""
    meta = set_vise(vf4, OPENING[name])
    set_parallel(vf4, meta, OPENING[name] - 2.0)
    Q = part_pose(name, meta)
    m = stock.mesh()
    m.save(str(spec_path))
    g_obj = "obj/bracket"
    if g_obj not in scn.sc.actors:
        vf4.part("bracket", dict(kind="file", path=str(spec_path)), Q)
    scn.sc.set_mesh(g_obj, m)
    scn.sc.gmat[g_obj] = Q
    scn.sc.alpha[g_obj] = 1.0
    prog = PC.program(name)
    T = int(prog.tool[0])
    vf4.show_tool(T)
    tx, ty, _ = SC.vf4_for(Q, prog.rot, prog.p0[0], T)
    vf4.set(table_x=tx, table_y=ty, z=0.0)
    return Q, prog


def chapter():
    w = SC.Writer(NAME, TITLE)
    scn = SC.Shop()
    vf4 = SC.VF4(scn)
    vf4.set(door=0.0, front_alpha=0.0)              # doors shut, the front hidden (chapter 30's inside view)
    stock = Stock()
    cache = pathlib.Path("/tmp/robotbuild/cache/shop/gcode")
    cache.mkdir(parents=True, exist_ok=True)
    cam_info = json.loads(pathlib.Path(PC.OUT_JSON).read_text())
    sim = json.loads(pathlib.Path(PC.SIM_JSON).read_text())
    mins = {s["setup"]: s["totals"]["total_min"] for s in cam_info["setups"]}
    kg0 = stock.kg()

    # ---- op 1: the blank in the vise (chapter 31's arm A set it there), the head at Z home, then the program
    Q1, p1 = setup_state(scn, vf4, stock, "bracket_op1", cache / "bracket_0.vtp")
    cap1 = "The vise bracket's program, op 1: bracket_op1.ngc as posted"
    # the camera of the cutting shot, at the program's start (no cut into it)
    c0 = np.array([(PC.BLANK[0] + PC.BLANK[1]) / 2, (PC.BLANK[2] + PC.BLANK[3]) / 2, (PC.BLANK[4] + PC.BLANK[5]) / 2])
    q0 = Q1[:3, :3] @ c0 + Q1[:3, 3]
    ref = (-q0[0], E.VF4["spindle_y"] - q0[1])
    Mv = Mst("vf4")
    F = np.array([0.0, E.VF4["spindle_y"], q0[2]])
    d = Mv[:3, :3] @ np.array([vf4.state["table_x"] - ref[0], vf4.state["table_y"] - ref[1], 0.0])
    cam1 = [tuple((Mv @ np.r_[F + CAM_OFF, 1.0])[:3] + d), tuple((Mv @ np.r_[F + np.array([0, 0, 15.0]), 1.0])[:3] + d),
            (0, 0, 1)]
    for i in range(int(3.0 * FPS)):
        w.frame(scn, cam1, cap1,
                sub=f"the recoater motor bracket, 90 x 60 x 170.4 mm (cad/lpbf_low.py), from a 96 x 176 mm blank of "
                    f"2.5 in. 6061 ({kg0:.1f} kg; setup_plan.json) on a 1 in. parallel; FreeCAD 1.0.2 CAM, "
                    f"{mins['bracket_op1']:.2f} min", who=[], step="vise bracket op 1", status="")
    m1, _ = run_program(w, scn, vf4, stock, "bracket_op1", Q1, cap1, SECONDS["bracket_op1"], "vise bracket op 1")

    # ---- op 2: turned over (a cut: the turn-over is not planned), gripped on the finished 90 mm faces
    Q2, p2 = setup_state(scn, vf4, stock, "bracket_op2", cache / "bracket_1.vtp")
    cap2 = "Op 2: turned over, gripped on its finished faces: bracket_op2.ngc as posted"
    c2 = Q2[:3, :3] @ c0 + Q2[:3, 3]
    ref2 = (-c2[0], E.VF4["spindle_y"] - c2[1])
    F2 = np.array([0.0, E.VF4["spindle_y"], c2[2]])
    d2 = Mv[:3, :3] @ np.array([vf4.state["table_x"] - ref2[0], vf4.state["table_y"] - ref2[1], 0.0])
    cam2 = [tuple((Mv @ np.r_[F2 + CAM_OFF, 1.0])[:3] + d2), tuple((Mv @ np.r_[F2 + np.array([0, 0, 15.0]), 1.0])[:3] + d2),
            (0, 0, 1)]
    for i in range(int(3.0 * FPS)):
        w.frame(scn, cam2, cap2,
                sub="turned over between the programs (not planned for the arms, so not drawn: a cut); the vise at "
                    f"90 mm on the faces op 1 finished, 3 mm of op 1's band still to cut; {mins['bracket_op2']:.2f} min",
                who=[], step="vise bracket op 2", status="")
    m2, tcam2 = run_program(w, scn, vf4, stock, "bracket_op2", Q2, cap2, SECONDS["bracket_op2"], "vise bracket op 2")

    # ---- the part as the programs leave it
    for i in range(int(4.0 * FPS)):
        w.frame(scn, tcam2(), "The bracket as its two programs leave it",
                sub=f"{m1 + m2:.1f} min of cutting; the simulation removed {sim['removed_sim_cm3']:.1f} cm3 against "
                    f"{sim['removed_exact_cm3']:.1f} cm3 of blank minus part ({sim['removed_sim_vs_cad_pct']:+.2f} %); "
                    "the lathe slug has no program (FreeCAD 1.0.2's CAM has no turning)",
                who=[], step="vise bracket", status="pass")
    n = w.close()
    return n, m1 + m2


def verify(rows):
    """Re-parse each program and check that every drawn cutter position lies on the chords of the line its frame names
    (gcode_sim.verify_frames' test, for the part programs)."""
    progs, worst, good = {}, 0.0, 0
    bad = []
    for r in rows:
        p = progs.get(r["setup"]) or progs.setdefault(r["setup"], PC.program(r["setup"]))
        q = np.array(r["work_xyz"], float)
        best = np.inf
        for k in np.nonzero(p.line == r["line"])[0]:
            a, b = p.p0[k], p.p1[k]
            ab = b - a
            t = float(np.clip((q - a) @ ab / max(ab @ ab, 1e-12), 0.0, 1.0))
            best = min(best, float(np.linalg.norm(a + t * ab - q)))
        worst = max(worst, best)
        if best < 1e-3 and 0.0 <= r["t_s"] <= p.total_s + 0.01:
            good += 1
        elif len(bad) < 5:
            bad.append(dict(frame=r["chapter_frame"], program=r["program"], line=r["line"], off_mm=best))
    return dict(frames=len(rows), on_their_program_line=good, worst_off_line_mm=round(worst, 6), problems=bad)


def main():
    t0 = time.time()
    try:
        n, mins = chapter()
    except StopIteration:              # SHOP_ONLY_FRAMES: stills only
        print("stills done", flush=True)
        return
    if SC.EVERY == 1 and not SC.ONLY and not SC.STILL:
        v = verify(ROWS)
        FRAMES_JSON.write_text(json.dumps(dict(
            what="every frame of chapter 31b that draws the VF-4 cutting the bracket: the cutter at the position the "
                 "posted program has at that frame's time (interpolated on the chord of the program line given), the table "
                 "and head at the axes that put it there (shop_chapters.vf4_for); verify: each position re-checked on the "
                 "re-parsed program", chapter=NAME, frames_total=n, minutes=round(mins, 3),
            programs=sorted(set(r["program"] for r in ROWS)), out_of_travel=sum(1 for r in ROWS if not r["in_travel"]),
            lines_per_program={p: len(set(r["line"] for r in ROWS if r["program"] == p))
                               for p in sorted(set(r["program"] for r in ROWS))},
            verify=v, rows=ROWS), indent=0))
        print("verify", v, flush=True)
    print(f"chapter {NAME}: {n} frames, {mins:.2f} min of programs, in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
