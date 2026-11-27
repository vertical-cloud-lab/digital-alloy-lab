"""The robot shop's clips for the round-7 video, each planned with shop_plan.py's primitives and recorded to
/tmp/robotbuild/traj/shop_<clip>.pkl (issue #260, PR #266). See shop_plan.py for the checks and the frame format.

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/analysis/shop/shop_clips.py [clip ...]
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shop_plan as SP  # noqa: E402
from shop_plan import (C, E, FPS, K, OUT, RHO_AL, S, Body, Clip, Job, Tm, inv, pick_place, record_job, station,  # noqa: E402
                       summarize, tool_passes)
from cell import Group, group_distance, group_hits  # noqa: E402

INCH = 25.4
RESULTS = {}


# ----------------------------------------------------------------------------------------------- chamber setups
def R_of(rots):
    R = np.eye(3)
    for ax, deg in rots:
        R = {"x": E.Rx, "y": E.Ry, "z": E.Rz}[ax](deg) @ R
    return R


_ST = None


def states():
    global _ST
    if _ST is None:
        _ST = json.loads((SP_CACHE / "states.json").read_text())
    return _ST


SP_CACHE = pathlib.Path("/tmp/robotbuild/cache/shop/chamber")     # cad/robotbuild/shop_chamber_cache.py writes it


def state_mesh(part, k):
    import pyvista as pv
    return pv.read(str(SP_CACHE / f"{part}_{k}.vtp"))


def mesh_vf(m):
    m = m.triangulate()
    return np.asarray(m.points, float), m.faces.reshape(-1, 4)[:, 1:].astype(np.int32)


def fixture_parts(fc, M_setup, skip=(), only=None):
    """freecad_cam.FIXTURES[fc] (the boxes and cylinders the CAM and holder_check.py use) as equipment Parts placed by
    M_setup (setup frame -> station frame). The HRT210 comes from equipment.py. Each edge clamp gets its screw head on
    top (the nut runner's target)."""
    out = {}
    cols = {"riser block": "#8e979f", "parallel": "#8e979f", "edge clamp": "#2f5f8a", "dummy-floor plate": "#6f777e",
            "fixture plate": "#6f777e", "port ID clamp": "#3a3f45"}
    n = {}
    for nm, kind, p in states()["fixtures"][fc]["pieces"]:
        if nm in skip or (only is not None and nm not in only) or nm.startswith(("HRT210", "2-1/2")):
            continue
        n[nm] = n.get(nm, 0) + 1
        key = f"{nm} {n[nm]}"
        if kind == "box":
            x0, x1, y0, y1, z0, z1 = p
            if nm == "edge clamp" and fc == "frame_B":   # round 9: the CAM's clamp boxes ran 5 mm into the risers'
                y0, y1 = (y0, min(y1, 74.0)) if y0 > 0 else (max(y0, -74.0), y1)   # (y 75-125): drawn short of them
            if nm == "edge clamp":                       # round 9: 1 mm off the blank's end faces (at 0.05 mm the voxel
                x0, x1 = (max(x0, 159.8), x1) if x0 > 0 else (x0, min(x1, -159.8))   # stock touched both: a sandwich
            m = E.box(x0, x1, y0, y1, z0, z1)
            if nm == "edge clamp":
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                out[f"{key} screw"] = E.Part(E.cyl((cx, cy, z1), (cx, cy, z1 + 10.0), 8.0, res=16), "#2b2f33", M=M_setup)
        elif kind == "vcyl":
            cx, cy, r, z0, z1 = p
            m = E.cyl((cx, cy, z0), (cx, cy, z1), r)
        elif kind == "xcyl":
            cy, cz, r, x0, x1 = p
            m = E.cyl((x0, cy, cz), (x1, cy, cz), r)
        else:
            continue
        out[key] = E.Part(m, cols.get(nm, "#6f777e"), M=M_setup)
    return out


def vf4_setup(fc, table_x=-100.0, k_state=0, part="frame", rots=None, a_deg=0.0, door=1.0, with_vise=False,
              spindle_z=None):
    """The VF-4 with a CAM setup's fixtures and the part (cut state k) on them: (parts, meta, part pose in the station
    frame, setup frame -> station, the state's mesh). Flat setups sit at equipment.TABLE_LAYOUT's fixture position; the
    rotary one on the HRT210's A axis (FCAM's platter face is at setup x = -29.3)."""
    parts, meta = E.vf4(door=door, table_x=table_x, with_vise=with_vise, spindle_z=spindle_z, hrt_a=a_deg)
    tz = meta["table_top"]
    fx = states()["fixtures"][fc]
    xc, yc, _ = meta["table_centre"]
    m = state_mesh(part, k_state)
    R = R_of(rots or [])
    if fc.startswith("frame_C"):
        x_axis = xc + E.TABLE_LAYOUT["hrt_face"] + 29.3
        M_setup = Tm(None, (x_axis, yc, tz - fx["table_z"])) @ Tm(C.rot((1, 0, 0), a_deg))
        P = M_setup @ Tm(R)
    else:
        M_setup = Tm(None, (meta["fixture_centre"][0], meta["fixture_centre"][1], tz - fx["table_z"]))
        rest = max(p[5] for nm, kind, p in fx["pieces"] if nm in ("riser block", "parallel", "dummy-floor plate",
                                                                  "fixture plate") and kind == "box")
        v = np.asarray(m.points) @ R.T
        P = M_setup @ Tm(R, (0.0, 0.0, rest - v[:, 2].min()))
    parts.update(fixture_parts(fc, M_setup))
    return parts, meta, P, M_setup, m


def part_body(name, mesh, color="#cfd4d9"):
    return Body(name, *mesh_vf(mesh), kind="held", color=color)


# A cordless-class nut runner held in the 2F-85 by a 20 mm fin (as P4's cutter): body, then a 1/4 in. hex extension and
# socket, so the bit reaches a clamp screw 20 mm from a part's end face (est. sizes, in the TCP frame along the approach)
NUT_RUNNER = dict(body=(20.0, 160.0, 22.0), ext=(160.0, 262.0, 8.0))


def nut_runner_body(name="nut runner"):
    a = S.cyl(NUT_RUNNER["body"][2], (0, 0, NUT_RUNNER["body"][0]), (0, 0, NUT_RUNNER["body"][1]), n=20)
    b = S.cyl(NUT_RUNNER["ext"][2], (0, 0, NUT_RUNNER["ext"][0]), (0, 0, NUT_RUNNER["ext"][1]), n=12)
    return Body(name, *C.merge([a, b]), kind="held", color="#e0a526")


def mir_state(job):
    return dict(M=job.Mm, arm_dx=job.arm_dx)


def done(name, job, clip, extra=None):
    r = summarize(job, extra)
    r["tightest_transit"] = SP.transit_clearance(job) if job.plan.ok else None
    RESULTS[name] = r
    clip.result = r
    print(name, "ok" if r["ok"] else "FAIL", r["fail"], f"{r['time_s']} s", "audit:", r["fine_audit_0p2deg"][:2],
          "torque", r["worst_torque_frac"], "tightest", (r.get("tightest_transit") or {}).get("clear_mm"), flush=True)
    return r


# ----------------------------------------------------------------------------------------------- VF-4 clips
def clip_vf4_clamps():
    """F-S1: the person has set the blank on the four riser blocks; arm A drives the four edge clamps' screws down with
    a nut runner held in its 2F-85 by a 20 mm fin (like P4's cutter)."""
    row = next(r for r in states()["rows"] if r.get("setup") == "F-S1")
    parts, meta, P, M_setup, m = vf4_setup("frame_B", k_state=0, rots=row["rots"])
    st = station("vf4")
    job = Job("VF-4 F-S1: arm A tightens the four edge clamps (nut runner)", "vf4", parts, x_mir=0.0 - S.ARM_DX)
    blank = part_body("frame blank", m)
    blank.place(st.M @ P)
    job.sc.world.add(blank)
    runner = nut_runner_body()
    heads = []
    for n, p in parts.items():
        if n.endswith("screw"):
            b = p.mesh.bounds
            heads.append((n, (p.M @ np.r_[(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, b[5], 1.0])[:3]))
    heads.sort(key=lambda h: (float(h[1][0]), float(h[1][1])))
    wps = []
    for n, h in heads:
        hw = st.to_world(h)
        Tw = K.T_at(hw + np.array([0.0, 0.0, NUT_RUNNER["ext"][1] + 1.0]), (0, 0, -1), st.R() @ np.array([1.0, 0, 0]))
        wps.append((n.replace(" screw", ""), K.lift(Tw, 90.0), Tw))
    close = job.arm.close_for_gap(20.0)
    tool_passes(job, runner, wps, close, allow=[f"vf4/{n}" for n, _ in heads], dwell=[("tighten to 30 N m", 2.5)] * 4)
    clip = Clip("vf4_clamps", "vf4", "30-machining-chamber")
    r = done("vf4_clamps", job, clip, dict(clamps=len(heads), blank_kg=30.05))
    clip.state["mach"] = dict(station="vf4", door=1.0, table_x=-100.0, table_y=0.0, spindle_z=None, fc="frame_B",
                              setup_rots=row["rots"])
    clip.obj("frame part", st.M @ P, dict(kind="state", part="frame", k=0))
    clip.set_arm("A", job.arm, "nut runner", mir=mir_state(job))
    record_job(clip, job, "A", tool="nut runner", meta_by_seg={"*": dict(
        caption="Arm A drives the four edge clamps' screws down with a nut runner",
        sub="F-S1 fixture (the CAM's frame_B): four 1-1/2 in. risers, four low-profile edge clamps on the blank's x ends; "
            "FCL on meshes, 0.5 deg planning, 0.2 deg audit", who=["robot A"], step="F-S1",
        status="pass" if r["ok"] else "fail")})
    clip.save()
    return clip


def clip_floor_load():
    """P-S1: arm A, with the OnRobot VGP20 vacuum gripper (the blank is dry; VGP20's datasheet rules out wet CNC parts),
    takes the floor plate's blank (12.5 x 9 x 1 in. 6061, 5.0 kg) by its top face off two blocks on its deck and sets it
    on the two parallels between the open edge clamps. (The 2F-85 can't: the plate is 228.6 mm wide, past its 85 mm
    stroke, and held by an edge its 5 kg would sit 114 mm off the fingers.)"""
    row = next(r for r in states()["rows"] if r.get("setup") == "P-S1")
    parts, meta, P, M_setup, m = vf4_setup("floor_A", k_state=0, part="floor", rots=row["rots"])
    st = station("vf4")
    job = Job("VF-4 P-S1: arm A (VGP20) loads the floor plate's blank onto the parallels", "vf4", parts,
              x_mir=0.0 - S.ARM_DX, gripper="VGP20")
    blank = part_body("floor blank", m)
    R = R_of(row["rots"])
    v = np.asarray(m.points) @ R.T
    kg = 317.5 * 228.6 * 25.4 * RHO_AL
    deck_c = job.deck((110.0, 0.0))
    T_deck = Tm(st.R() @ R, deck_c + np.array([0.0, 0.0, 30.0 - v[:, 2].min()]))
    T_to = st.M @ P
    G = inv(Tm(R)) @ Tm(C.frame((0, 0, -1), (1, 0, 0)), (0.0, 0.0, v[:, 2].max()))   # cups on the top face
    blocks = C.merge([S.box(-150, -110, -90, 90, 0, 30), S.box(110, 150, -90, 90, 0, 30)])
    job.add_obstacle("deck blocks", S.xf(blocks, Tm(st.R(), deck_c)))
    res = pick_place(job, blank, kg, T_deck, T_to, G, 0.0, 0.0, allow_from=["mir0/parts deck", "deck blocks"],
                     allow_to=[n for n in job.sc.world.bodies if "parallel" in n or "edge clamp" in n], up_from=80.0, up_to=80.0,
                     release_note="vacuum off; the edge clamps close (nut runner, as F-S1)", grip_note="vacuum on")
    clip = Clip("vf4_floor_load", "vf4", "30-machining-chamber")
    r = done("vf4_floor_load", job, clip, dict(part_kg=round(kg, 2)))
    clip.state["mach"] = dict(station="vf4", door=1.0, table_x=-100.0, table_y=0.0, spindle_z=None, fc="floor_A",
                              setup_rots=row["rots"])
    clip.obj("floor part", T_deck, dict(kind="state", part="floor", k=0))
    clip.obj("deck blocks", Tm(st.R(), deck_c), dict(kind="boxes", boxes=[(-150, -110, -90, 90, 0, 30),
                                                                          (110, 150, -90, 90, 0, 30)], color="#d9b23a"))
    clip.set_arm("A", job.arm, "VGP20", mir=mir_state(job))
    record_job(clip, job, "A", tool="VGP20", meta_by_seg={"*": dict(
        caption="Arm A sets the floor plate's blank (5.0 kg) on the parallels for P-S1 with a vacuum gripper",
        sub="12.5 x 9 x 1 in. 6061, dry from the rack: OnRobot VGP20 (20 kg at low acceleration); FCL-checked, "
            "0.5 deg planning, 0.2 deg audit", who=["robot A"], step="P-S1", status="pass" if r["ok"] else "fail")},
               objs_follow={"floor blank": "floor part"})
    if res:
        clip.obj("floor part", T_to)
        clip.frame(6)
    clip.save()
    return clip


def simple_clip(name, station_key, chapter, job, akey, tool, caption, sub, step, who=("robot A",), objs=None,
                follow=None, end_objs=None, mach=None, extra=None):
    """Record a planned one-arm job as a clip with one caption."""
    clip = Clip(name, station_key, chapter)
    r = done(name, job, clip, extra)
    clip.state["mach"] = dict(station=station_key, **(mach or {}))
    for n, (M, spec) in (objs or {}).items():
        clip.obj(n, M, spec)
    clip.set_arm(akey, job.arm, tool, mir=mir_state(job))
    record_job(clip, job, akey, tool=tool, meta_by_seg={"*": dict(caption=caption, sub=sub, who=list(who), step=step,
                                                                    status="pass" if r["ok"] else "fail")},
               objs_follow=follow)
    for n, M in (end_objs or {}).items():
        clip.obj(n, M)
    clip.frame(6)
    clip.save()
    return clip


# ----------------------------------------------------------------------------------------------- vise, lathe, saw
def clip_vise_part():
    """A typical vise part: the recoater motor bracket's blank (2.5 in. 6061 plate, 2.9 kg; dfm.json) from the deck into
    the Kurt XL6A air vise (jaws along X, opened 20 mm past the blank), gripped across its 63.5 mm thickness."""
    W, L, H = 72.0, 150.0, 63.5                  # a 2.5 in. plate blank: 72 mm between the jaws, 150 mm across them
    kg = W * L * H * RHO_AL
    PAR = 25.4                                   # on a 1 in. parallel, so 44 mm stand above the 1.75 in. jaws
    parts, meta = E.vf4(door=1.0, table_x=-E.TABLE_LAYOUT["vise"], with_vise=True, vise_open=W + 20.0, with_hrt=True)
    st = station("vf4")
    job = Job("VF-4 vise: arm A loads a bracket's 2.5 in. blank into the Kurt XL6A", "vf4", parts, x_mir=0.0 - S.ARM_DX)
    blank = Body("bracket blank", *S.box(-W / 2, W / 2, -L / 2, L / 2, 0, H), kind="held", color="#cfd4d9")
    vx = meta["vise_x_fixed"]                    # the fixed jaw's face (jaws close along x, fixed jaw at -x)
    yv = meta["vise_centre"][1]
    par = S.box(vx + 2.0, vx + W - 2.0, yv - 60.0, yv + 60.0, meta["vise_floor_z"], meta["vise_floor_z"] + PAR)
    job.add_obstacle("vise parallel", S.xf(par, st.M))
    T_to = st.M @ Tm(None, (vx + 1.0 + W / 2, yv, meta["vise_floor_z"] + PAR))
    T_from = Tm(st.R(), job.deck((110.0, 0.0)))
    G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (0.0, 0.0, H - 20.0))    # from above, fingers on the x faces' top 20 mm
    c_open, c_grip = job.arm.close_for_gap(W + 12.0), job.arm.close_for_gap(W)
    res = pick_place(job, blank, kg, T_from, T_to, G, c_open, c_grip, allow_from=["mir0/parts deck"],
                     allow_to=["vise parallel", "vf4/vise fixed jaw", "vf4/vise jaw plates"],
                     release_note="air vise closes (M-code); gripper opens")
    return simple_clip("vf4_vise_part", "vf4", "31-machining-parts", job, "A", "2F-85",
                       "Arm A sets a bracket's blank in the air vise", "Kurt XL6A (6 in. jaws, opens 14.5 in.) on the VF-4; "
                       f"{kg:.1f} kg of 2.5 in. 6061 on a 1 in. parallel; FCL-checked, 0.2 deg audit", "vise class",
                       objs={"bracket blank": (T_from, dict(kind="box", b=(-W / 2, W / 2, -L / 2, L / 2, 0, H),
                                                            color="#cfd4d9")),
                             "vise parallel": (st.M, dict(kind="box", b=(vx + 2.0, vx + W - 2.0, yv - 60.0, yv + 60.0,
                                                                         meta["vise_floor_z"], meta["vise_floor_z"] + PAR),
                                                          color="#8e979f"))},
                       end_objs={"bracket blank": T_to} if res else None,
                       mach=dict(door=1.0, table_x=-E.TABLE_LAYOUT["vise"], table_y=0.0, spindle_z=None, with_vise=True,
                                 vise_open=120.0), extra=dict(part_kg=kg))


def clip_lathe_slug():
    """P2 on the ST-10 (PR 318's fitted outside): a 2-1/8 in. 6061 slug (Ø54 x 100) from a V-cradle on the deck into the
    6.5 in. chuck, the arm coming in from above, through the 588 mm door, then along the spindle axis into the jaws."""
    parts, meta = E.st10(door=1.0, jaw_open=6.0)
    st = station("lathe")
    _, ys, zs = meta["chuck_face"]
    x_arm = 150.0
    job = Job("ST-10: arm A loads a 2-1/8 in. slug into the chuck from above", "lathe", parts, x_mir=x_arm - S.ARM_DX, gap=250.0)
    slug = Body("bar slug", *S.cyl(27.0, (0, 0, 0), (100.0, 0, 0), n=32), kind="held", color="#cfd4d9")
    kg = math.pi * 27.0 ** 2 * 100.0 * RHO_AL
    T_from = Tm(st.R(), job.deck((110.0, 0.0)) + np.array([0, 0, 27.0]))
    T_to = st.M @ Tm(None, (-15.0, ys, zs))             # its end 5 mm off the chuck body; the jaws hold 40 mm of it
    G = Tm(C.frame((0, 0, -1), (0, 1, 0)), (75.0, 0.0, 0.0))
    c_open, c_grip = job.arm.close_for_gap(80.0), job.arm.close_for_gap(54.0)
    # top-down loading (robot-shop.md P2): carried in level with the axis from in front of the door, then pushed along
    # the axis: approach_to = 70 mm out along +x (the jaws' mouth) and the RRT brings it there through the door
    res = pick_place(job, slug, kg, T_from, T_to, G, c_open, c_grip, allow_from=["mir0/parts deck"],
                     allow_to=[f"lathe/chuck jaw {k}" for k in (1, 2, 3)] + ["lathe/chuck (6.5 in.)"],
                     approach_to=(70.0, 0.0, 0.0), via=(0.0, -450.0, 0.0), release_note="chuck closes (M-code); gripper opens", iters=4000)
    return simple_clip("lathe_slug", "lathe", "31-machining-parts", job, "A", "2F-85",
                       "Arm A loads a bar slug into the lathe's chuck, from above", "Haas ST-10 (byu-vcl PR 318's fitted "
                       "model): 588 mm door; coaxial loading fails (P2), top-down passes; FCL, 0.2 deg audit", "lathe class",
                       objs={"bar slug": (T_from, dict(kind="cyl", r=27.0, L=100.0, color="#cfd4d9"))},
                       end_objs={"bar slug": T_to} if res else None, mach=dict(door=1.0, jaw_open=6.0), extra=dict(part_kg=round(kg, 2)))


def clip_lathe_big():
    """The 3FG15 at the lathe: a Ø4.25 in. 316L blank (108 mm, 50 mm long, 3.6 kg: the spigot flange's class), past the
    2F-85's 85 mm stroke. It lies in a V-cradle on the deck; the 3FG15 takes it from above across its axis and loads it
    top-down like P2 (coaxial loading hits the door's jamb), into jaws opened for 108 mm."""
    parts, meta = E.st10(door=1.0, jaw_open=108.0 / 2 - 27.0 + 6.0, jaw_deg=30.0)   # jaws at 30/150/270: none on top
    st = station("lathe")
    _, ys, zs = meta["chuck_face"]
    r_b, L_b = 54.0, 50.0
    kg = math.pi * r_b ** 2 * L_b * 8.0e-6
    for x_arm in (150.0, 250.0, 50.0):
        job = Job("ST-10: arm A (3FG15) loads a Ø4.25 in. blank from above", "lathe", parts, x_mir=x_arm - S.ARM_DX,
                  gripper="3FG15L", gap=350.0)
        blank = Body("round blank", *S.cyl(r_b, (0, 0, 0), (L_b, 0, 0), n=40), kind="held", color="#b8bec4")
        T_from = Tm(st.R(), job.deck((110.0, 0.0)) + np.array([0, 0, r_b + 15.0]))
        T_to = st.M @ Tm(None, (5.0, ys, zs))               # 20 mm of it in the jaws (soft jaws for disc work)
        G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (L_b - 14.0, 0.0, 0.0))   # from above, across the axis, 14 mm from its end:
                                                                         # the fingers stay clear of the jaws
        c_open, c_grip = job.arm.close_for_gap(2 * r_b + 20.0), job.arm.close_for_gap(2 * r_b)
        res = pick_place(job, blank, kg, T_from, T_to, G, c_open, c_grip, allow_from=["mir0/parts deck"],
                         allow_to=[f"lathe/chuck jaw {k}" for k in (1, 2, 3)] + ["lathe/chuck (6.5 in.)"],
                         approach_to=(70.0, 0.0, 0.0), via=(0.0, -320.0, 0.0), release_note="chuck closes; gripper opens",
                         iters=3000)
        if res is not None and job.plan.ok:
            break
        print("lathe_big: no plan with the arm at x", x_arm, job.plan.fail, flush=True)
    return simple_clip("lathe_big", "lathe", "31-machining-parts", job, "A", "3FG15L",
                       "Arm A, with an OnRobot 3FG15, loads a Ø4.25 in. 316L blank", "108 mm is past the 2F-85's 85 mm "
                       "stroke; 3FG15 (4-152 mm, 10 kg) with our 40 mm longer fingertips, the spindle oriented so no jaw is on top",
                       "lathe class (3FG15)",
                       objs={"round blank": (T_from, dict(kind="cyl", r=r_b, L=L_b, color="#b8bec4"))},
                       end_objs={"round blank": T_to} if res else None, mach=dict(door=1.0, jaw_open=33.0),
                       extra=dict(part_kg=round(kg, 2)))


def clip_saw():
    """Arm B sets a 600 mm length of 2-1/8 in. 6061 bar (3.7 kg) on the S-20A's infeed rollers against the shuttle vise;
    the saw cuts; arm B takes the 100 mm slug off the outfeed side."""
    parts, meta = E.s20a(head=1.0)
    st = station("saw")
    job = Job("S-20A: arm B lays a bar on the infeed rollers", "saw", parts, x_mir=-1500.0 - S.ARM_DX, arm_key="B")
    bar = Body("bar 600", *S.cyl(27.0, (0, 0, 0), (600.0, 0, 0), n=32), kind="held", color="#cfd4d9")
    kg = math.pi * 27.0 ** 2 * 600.0 * RHO_AL
    T_from = Tm(st.R(), job.deck((110.0, 0.0)) + np.array([0, 0, 27.0 + 40.0])) @ Tm(None, (-300.0, 0, 0))   # on two 40 mm V-blocks
    T_to = st.M @ Tm(None, (-1820.0, 460.0, meta["bed_z"] + 27.0))           # on the rollers, clear of the raised head
    G = Tm(C.frame((0, 0, -1), (0, 1, 0)), (300.0, 0.0, 0.0))                   # from above at its middle
    c_open, c_grip = job.arm.close_for_gap(80.0), job.arm.close_for_gap(54.0)
    vb = [(-140, -100, -40, 40, 0, 40), (100, 140, -40, 40, 0, 40)]
    M_vb = Tm(st.R(), job.deck((110.0, 0.0)))
    job.add_obstacle("deck blocks", S.xf(C.merge([S.box(*b) for b in vb]), M_vb))
    res = pick_place(job, bar, kg, T_from, T_to, G, c_open, c_grip, allow_from=["mir0/parts deck", "deck blocks"],
                     allow_to=["saw/infeed rollers", "saw/infeed roller table"], release_note="gripper opens")
    return simple_clip("saw_bar", "saw", "31-machining-parts", job, "B", "2F-85",
                       "Arm B lays a bar on the bandsaw's infeed", "Hyd-Mech S-20A (13 x 18 in., table 31 in.): the shuttle "
                       "vise feeds and the saw cuts on its own; 3.7 kg of 2-1/8 in. 6061; FCL, 0.2 deg audit", "saw class",
                       who=("robot B",), objs={"bar 600": (T_from, dict(kind="cyl", r=27.0, L=600.0, color="#cfd4d9")),
                                               "deck blocks": (M_vb, dict(kind="boxes", boxes=vb, color="#d9b23a"))},
                       end_objs={"bar 600": T_to} if res else None, mach=dict(head=1.0), extra=dict(part_kg=round(kg, 2)))


# ----------------------------------------------------------------------------------------------- finishing
def clip_deburr():
    """Arm A holds a bracket against the brush wheel, then its edges on the ATI compliant spindle (part to tool)."""
    parts, meta = E.wash_deburr()
    st = station("wash")
    job = Job("Deburr: arm A holds a part against the brush and the compliant spindle", "wash", parts,
              x_mir=560.0 - S.ARM_DX)
    L, W, H = 100.0, 72.0, 40.0
    part = Body("bracket", *S.box(-W / 2, W / 2, -L / 2, L / 2, 0, H), kind="held", color="#d6dade")   # round 9: below
    # the TCP (z along the approach), its top in the pads; round 8 had it above, through the fingers' knuckles
    bx, by, bz = meta["brush"]
    tx, ty, tz = meta["deburr_tip"]
    wps = []
    for label, p, z in (("brush, top edge", (bx - 80.0, by, bz + 75.0 + H + 2.0), (0, 0, -1)),
                        ("compliant spindle, the edge", (tx, ty, tz + H + 1.0), (0, 0, -1))):
        Tw = K.T_at(st.to_world(p), st.R() @ np.array(z, float), st.R() @ np.array([1.0, 0, 0]))
        wps.append((label, K.lift(Tw, 80.0), Tw))
    close = job.arm.close_for_gap(W)
    tool_passes(job, part, wps, close, allow=["wash/brush wheel", "wash/ATI compliant deburr spindle"],
                dwell=[("brushing", 6.0), ("deburring the edge", 6.0)], kg=0.8)
    return simple_clip("deburr", "wash", "32-finishing", job, "A", "2F-85", "Arm A deburrs a bracket: brush, then the "
                       "compliant spindle", "part to tool: a brush wheel and an ATI compliant deburring spindle on the bench; "
                       "edges in deep pockets stay a person's job", "deburr class", mach=dict(lid_open=True),
                       objs={"bracket": (np.eye(4), dict(kind="box", b=(-W / 2, W / 2, -L / 2, L / 2, 0, H),
                                                         color="#d6dade"))},
                       follow={"bracket": "bracket"}, extra=dict(part_kg=0.8))


def clip_wash():
    """Arm B lifts the parts basket by its handle out of the ultrasonic tank (Crest 7 gal) into the rinse tank."""
    parts, meta = E.wash_deburr(basket_up=0.0)
    st = station("wash")
    tx, ty, _ = meta["tank"]
    rx, ry, rz = meta["rinse"]
    job = Job("Wash: arm B moves the basket from the ultrasonic tank to the rinse", "wash", parts,
              x_mir=(tx + rx) / 2 - S.ARM_DX, arm_key="B")
    basket_parts = {k: v for k, v in parts.items() if k in ("parts basket", "basket handle")}
    for k in basket_parts:
        job.sc.world.remove(f"wash/{k}")
    vf = C.merge([E.fcl_items({k: v}, np.eye(4))[0][1] for k, v in basket_parts.items()])
    basket = Body("basket", *vf, kind="held", color="#9aa3ab")
    T_from = st.M                                                      # the basket's meshes are in the station frame
    T_to = st.M @ Tm(None, (rx - tx, ry - ty, rz + 20.0 - (meta["top_z"] + 80.0)))   # sitting in the rinse tank
    G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (tx, ty, meta["basket_handle_z"]))   # fingers across the handle bar (along y)
    c_open, c_grip = job.arm.close_for_gap(45.0), job.arm.close_for_gap(20.0)
    res = pick_place(job, basket, 4.0, T_from, T_to, G, c_open, c_grip, allow_from=["wash/ultrasonic tank (Crest 7 gal)"],
                     allow_to=["wash/rinse tank"], up_from=280.0, up_to=280.0, release_note="gripper opens")
    return simple_clip("wash", "wash", "32-finishing", job, "B", "2F-85", "Arm B moves the parts basket from the "
                       "ultrasonic tank to the rinse", "Crest Powersonic 7 gal (19.5 x 11.75 x 8 in. tank, heated, 45 kHz); the basket "
                       "and parts about 4 kg; FCL, 0.2 deg audit", "wash class", who=("robot B",),
                       objs={"basket": (T_from, dict(kind="parts", station="wash", names=list(basket_parts)))},
                       end_objs={"basket": T_to} if res else None, mach=dict(lid_open=True), extra=dict(part_kg=4.0))


def clip_measure():
    """Arm A sets a machined bracket (the vise class's part, 1.9 kg) on the granite plate for the person to gauge, 2F-85
    from above. (With the floor plate on the VGP20, RRT-Connect found no carry from three docking positions: the 312 x
    222 plate and the 264 x 184 gripper have to swing over the plate's front edge from an arm base 114 mm below the
    granite's top; the person sets the big plates on the granite.)"""
    parts, meta = E.granite_station()
    st = station("measure")
    W, L, H = 72.0, 150.0, 63.5
    kg = W * L * H * RHO_AL
    for x_arm in (-150.0, 150.0):
        job = Job("Measuring: arm A sets a bracket on the granite", "measure", parts, x_mir=x_arm - S.ARM_DX)
        part = Body("bracket", *S.box(-W / 2, W / 2, -L / 2, L / 2, 0, H), kind="held", color="#d6dade")
        T_from = Tm(st.R(), job.deck((110.0, 0.0)))
        T_to = st.M @ Tm(None, (-60.0, 170.0, meta["top_z"]))
        G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (0.0, 0.0, H - 20.0))
        c_open, c_grip = job.arm.close_for_gap(W + 12.0), job.arm.close_for_gap(W)
        res = pick_place(job, part, kg, T_from, T_to, G, c_open, c_grip, allow_from=["mir0/parts deck"],
                         allow_to=["measure/granite surface plate"], iters=3000, up_from=420.0, up_to=150.0)
        if res is not None and job.plan.ok:
            break
        print("measure: no plan with the arm at x", x_arm, job.plan.fail, flush=True)
    return simple_clip("measure", "measure", "32-finishing", job, "A", "2F-85", "Arm A sets a bracket on the granite "
                       "for gauging", "36 x 24 x 4 in. grade A plate at 36 in.; a person reads the bore and height gauges "
                       "(the arm can't)", "measure class", objs={"bracket": (T_from, dict(kind="box", b=(-W / 2, W / 2, -L / 2, L / 2, 0, H),
                                                                                         color="#d6dade"))},
                       end_objs={"bracket": T_to} if res else None, extra=dict(part_kg=round(kg, 2)))


KIT_SLOTS = SP.LPBF / "analysis" / "out" / "assembly" / "kit_slots.json"   # kit_table.py writes it (committed);
                                                                               # round 9: relative to the repo, not a worktree


def kit_slots():
    if KIT_SLOTS.exists():
        return json.loads(KIT_SLOTS.read_text())
    return None


def clip_kit():
    """Kitting onto the long parts table (kit_table.py's slot C00a, the floor plate's): MiR A docks in its lane (arm base
    on y = -640 in the hall) and arm A sets the plate into its slot (VGP20). Neighbouring slots are boxes."""
    import common as CM
    ks = kit_slots()
    if ks is None:
        RESULTS["kit"] = dict(ok=False, fail="kit_slots.json not found")
        return None
    slot = next(s for s in ks["slots"] if s["key"] == "C00a")
    shop_of_hall = Tm(None, tuple(-np.asarray(CM.SHOP_IN_HALL, float)))
    T_slot = shop_of_hall @ np.asarray(slot["T"], float)          # model frame -> shop
    bx = slot["bbox"]
    xc = (bx[0] + bx[1]) / 2
    LT = CM.LONG_TABLE
    # a station frame on the table's front edge at the slot (hall y = -450), in the shop frame
    st = S.Station("long table", (xc, LT["y0"] - CM.SHOP_IN_HALL[1], 0.0), [], {})
    SP.POSE["long_table"] = st.pose
    parts = {"long table top": E.Part(E.box(-1500, 1500, 0, LT["y1"] - LT["y0"], LT["top"] - LT["t"], LT["top"]), "#d8d2c4"),
             "long table legs": E.Part(E.merge([E.box(x - 30, x + 30, y - 30, y + 30, 0, LT["top"] - LT["t"])
                                                for x in (-1400, 1400) for y in (60, 840)]), "#6b7078")}
    for s in ks["slots"]:
        b = s["bbox"]
        if s["key"] == "C00a" or b[1] < xc - 1500 or b[0] > xc + 1500 or s.get("support") == "pallet":
            continue
        y0, y1 = b[2] - LT["y0"], b[3] - LT["y0"]
        parts[f"slot {s['key']}"] = E.Part(E.box(b[0] - xc, b[1] - xc, y0, y1, b[4], b[5]), "#b0b6bc")
    job = Job("Kitting: arm A sets the floor plate into its slot on the long table", "long_table", parts,
              x_mir=0.0 - S.ARM_DX, gap=30.0, gripper="VGP20")
    m = state_mesh("floor", 16)
    plate = part_body("floor plate", m)
    v = np.asarray(m.points)
    T_from = Tm(st.R(), job.deck((110.0, 0.0)) + np.array([0, 0, 30.0 - v[:, 2].min()]))
    vs = v @ T_slot[:3, :3].T
    G = inv(Tm(T_slot[:3, :3])) @ Tm(C.frame((0, 0, -1), (1, 0, 0)), (0.0, 70.0, vs[:, 2].max()))
    T_from = Tm(st.R(), job.deck((110.0, 0.0))) @ Tm(T_slot[:3, :3], (0, 0, 30.0 - vs[:, 2].min()))
    blocks = C.merge([S.box(-150, -110, -90, 90, 0, 30), S.box(110, 150, -90, 90, 0, 30)])
    job.add_obstacle("deck blocks", S.xf(blocks, Tm(st.R(), job.deck((110.0, 0.0)))))
    res = pick_place(job, plate, 3.03, T_from, T_slot, G, 0.0, 0.0, allow_from=["mir0/parts deck", "deck blocks"],
                     allow_to=["long_table/long table top"], release_note="vacuum off", grip_note="vacuum on")
    return simple_clip("kit", "long_table", "32-finishing", job, "A", "VGP20", "Arm A kits the floor plate into its slot on "
                       "the long table", f"kit_table.py slot C00a ({slot['name'][:40]}...); arm base on lane A (hall y -640)",
                       "kit class", objs={"floor plate": (T_from, dict(kind="state", part="floor", k=16))},
                       end_objs={"floor plate": T_slot} if res else None, extra=dict(part_kg=3.03, slot="C00a"))


# ----------------------------------------------------------------------------------------------- receiving
RECV_BOX = ("seals, fasteners, inserts (McMaster)", 300.0, 250.0, 150.0, 4.0)


def recv_box_parts(flaps=0.0):
    """The box on the receiving lift table, in the receiving station's frame (round 9: on its own, so a chapter can
    swap the shut box for the opened one without touching the table)."""
    name, L, W, H, kg = RECV_BOX
    bp = E.box_mesh_with_tape(L, W, H, flaps)
    return E.placed(bp, Tm(None, (0.0, 420.0, 760.0)), "box: ")


def recv_parts(flaps=0.0):
    """The receiving lift table (Vestil SCTAB, top at 760 mm) with a box on it, in the receiving station's frame
    (robot at -y)."""
    parts = E.placed(E.lift_table(760.0), Tm(None, (0.0, 520.0, 0.0)))
    parts.update(recv_box_parts(flaps))
    return parts


def clip_recv_tape():
    """P4 on the new receiving table: a spring-retracting safety knife in a holder (20 mm fin) in arm A's 2F-85 runs
    along the box's tape seam; only the holder is collision-checked (the blade is meant to cut)."""
    parts = recv_parts(0.0)
    st = station("receiving")
    name, L, W, H, kg = RECV_BOX
    job = Job("Receiving: arm A cuts the tape", "receiving", parts, x_mir=0.0 - S.ARM_DX)
    cutter = Body("box cutter", *S.box(-10, 10, -8, 8, -38, 42), kind="held", color="#e63946")
    top = 760.0 + H
    p0, p1 = st.to_world((-L / 2 + 15.0, 420.0, top)), st.to_world((L / 2 - 15.0, 420.0, top))
    seam = (p1 - p0) / np.linalg.norm(p1 - p0)
    xax = np.cross([0, 0, 1.0], seam)
    T0 = K.T_at(p0 + np.array([0, 0, 52.0]), (0, 0, -1), xax)
    T1 = K.T_at(p1 + np.array([0, 0, 52.0]), (0, 0, -1), xax)
    close = job.arm.close_for_gap(20.0)
    arm = job.arm
    # tool in hand above the seam's start, plunge, cut along, lift
    q0 = None
    for qc in arm.ik_all(K.lift(T0, 200.0), job.home(close)):
        arm.place(qc, close)
        held = K.attach(arm, cutter, arm.tcp())
        if not job.chk.collisions(qc, close, frozenset()):
            q0 = qc
            break
        K.detach(arm)
    if q0 is None:
        RESULTS["recv_tape"] = dict(ok=False, fail="no start pose")
        return None
    allow = frozenset({("held", "receiving/box: box"), ("held", "receiving/box: tape"), ("held", "receiving/box: flaps")})
    qs1, i1 = K.cart(job.chk, arm, K.line(K.lift(T0, 200.0), T0), close, allow, q0)
    job.plan.add("linear", qs1 or [], close, "down to the seam (blade 8 mm in)", ok=qs1 is not None, info=i1, held=held, t=1.5)
    if qs1:
        qs2, i2 = K.cart(job.chk, arm, K.line(T0, T1), close, allow, qs1[-1])
        job.plan.add("linear", qs2 or [], close, f"cut along the {L - 30:.0f} mm seam", ok=qs2 is not None, info=i2,
                     held=held, t=(L - 30.0) / 100.0)
        if qs2:
            qs3, i3 = K.cart(job.chk, arm, K.line(T1, K.lift(T1, 200.0)), close, allow, qs2[-1])
            job.plan.add("linear", qs3 or [], close, "lift clear", ok=qs3 is not None, info=i3, held=held, t=1.5)
    job.payload = {k: 0.3 for k in range(len(job.plan.segments))}
    return simple_clip("recv_tape", "receiving", "20-receiving", job, "A", "cutter", "Arm A cuts a box's tape with a "
                       "safety knife", "spring-retracting knife in a holder in the 2F-85 (P4): the box on the receiving lift "
                       "table at 760 mm", "receiving", objs={}, extra=dict(box=name))


def clip_recv_unbox():
    """Arm B lifts the tray of seals and fasteners (4.0 kg) out of the opened box onto its MiR's deck (2F-85 on the
    tray's handle fin)."""
    parts = recv_parts(1.0)
    st = station("receiving")
    name, L, W, H, kg = RECV_BOX
    job = Job("Receiving: arm B lifts the tray out of the box", "receiving", parts, x_mir=0.0 - S.ARM_DX + 0.0, arm_key="B")
    tray = Body("tray", *C.merge([E.fcl_items({"t": E.Part(E.open_box(-L / 2 + 15, L / 2 - 15, -W / 2 + 15, W / 2 - 15, 0,
                                                                         90, 3.0))}, np.eye(4))[0][1],
                                  S.box(-10, 10, -40, 40, 90, 150)]), kind="held", color="#2b6cb0")
    T_from = st.M @ Tm(None, (0.0, 420.0, 760.0 + 12.0))
    T_to = Tm(st.R(), job.deck((110.0, 0.0)))
    G = Tm(C.frame((0, 0, -1), (1, 0, 0)), (0.0, 0.0, 130.0))     # fingers across the 20 mm fin
    c_open, c_grip = job.arm.close_for_gap(45.0), job.arm.close_for_gap(20.0)
    res = pick_place(job, tray, kg, T_from, T_to, G, c_open, c_grip, allow_from=["receiving/box: box", "receiving/box: flaps"],
                     allow_to=["mir0/parts deck"], up_from=220.0, up_to=60.0, release_note="gripper opens")
    return simple_clip("recv_unbox", "receiving", "20-receiving", job, "B", "2F-85", "Arm B lifts the tray of seals and "
                       "fasteners out of the box onto its deck", "4.0 kg tray with a 20 mm handle fin; the flaps folded back "
                       "by both arms (not planned: cardboard is deformable)", "receiving", who=("robot B",),
                       objs={"tray": (T_from, dict(kind="tray", L=L - 30, W=W - 30, H=90.0, color="#2b6cb0"))},
                       end_objs={"tray": T_to} if res else None, mach=dict(flaps=1.0), extra=dict(part_kg=kg))


# ----------------------------------------------------------------------------------------------- MiR drives (round 9)
# Sterling on round 7: "moonwalk". Round 9 (P1): a MiR drives between the shop's stations as a differential-drive base
# does (as analysis/assembly/mir_route.py does for the assembly): pivot on the spot to the heading of the straight line
# to the next dock, drive forward along it (trapezoid, 0.3 m/s^2, 1.0 m/s: the MiR250 datasheet's, shop_cell.MIR_DRIVE),
# pivot to the dock's heading. Every pose is swept with FCL: the MiR's body, cabinet, plate and deck and the parked arm
# with its gripper, against the stations near the path as the chapter draws them; pivots every 2 deg, the line every
# 20 mm. Then the arm goes from the transport pose it drove in to the next clip's first pose (a joint-space line checked
# every 0.5 deg).
PIV_RATE, PIV_RAMP = 30.0, 0.5            # deg/s, s: an ESTIMATE (MiR publishes no pivot rate; mir_route.py's)
DRV_V, DRV_A = 1000.0, 300.0              # mm/s, mm/s^2 (MiR250 datasheet, shop_cell.MIR_DRIVE)


def _wrap180(a):
    return (a + 180.0) % 360.0 - 180.0


def _yaw(M):
    return math.degrees(math.atan2(M[1, 0], M[0, 0]))


def _trap(d, v=DRV_V, a=DRV_A):
    """Time (s) and the distance at time t of a trapezoid move of length d."""
    d = abs(float(d))
    if d < 1e-6:
        return 0.0, (lambda t: 0.0)
    if d >= v * v / a:
        T = d / v + v / a
        ta = v / a

        def s(t):
            t = min(max(t, 0.0), T)
            if t < ta:
                return 0.5 * a * t * t
            if t > T - ta:
                return d - 0.5 * a * (T - t) ** 2
            return 0.5 * a * ta * ta + v * (t - ta)
        return T, s
    T = 2.0 * math.sqrt(d / a)

    def s2(t):
        t = min(max(t, 0.0), T)
        return 0.5 * a * t * t if t < T / 2 else d - 0.5 * a * (T - t) ** 2
    return T, s2


def drive_legs(M0, M1):
    """[(kind, M at s in [0, 1] as a function, seconds)] for pivot, drive, pivot from dock pose M0 to dock pose M1."""
    p0, p1 = M0[:3, 3].copy(), M1[:3, 3].copy()
    h0, h1 = _yaw(M0), _yaw(M1)
    d = p1 - p0
    dist = float(np.hypot(d[0], d[1]))
    hd = math.degrees(math.atan2(d[1], d[0])) if dist > 1.0 else h0
    legs = []

    def pose(x, y, h):
        return Tm(C.rot((0, 0, 1), h), (x, y, 0.0))

    for a0, a1, at in ((h0, hd, p0), (None, None, None), (hd, h1, p1)):
        if a0 is None:
            T, s = _trap(dist)
            if T > 0:
                legs.append(("drive", (lambda u, s=s, T=T: pose(*(p0[:2] + (d[:2] / dist) * s(u * T)), hd)), T,
                             dist))
            continue
        dth = _wrap180(a1 - a0)
        if abs(dth) < 0.05:
            continue
        T = abs(dth) / PIV_RATE + PIV_RAMP
        legs.append(("pivot", (lambda u, a0=a0, dth=dth, at=at: pose(at[0], at[1], a0 + dth * ease(u))), T, abs(dth)))
    return legs


def ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(u, 0.0), 1.0))


def mir_bodies(arm_dx):
    return [Body(f"mir/{name}", *vf, kind="robot", color=col) for name, vf, col in S.mir_items(arm_dx)]


def arm_base_of(M, arm_dx):
    p = (M @ np.r_[arm_dx, S.ARM_DY, S.ARM_Z, 1.0])[:3]
    return p, _yaw(M)


def clip_drive(name, chapter, akey, from_clip, to_clip, world_parts, caption, sub, step, to_last=False):
    """Record MiR `akey` driving from the last frame of clip `from_clip` to the first of `to_clip` (both recorded),
    checked with FCL against world_parts [(station key, parts)]. The arm first turns to a transport pose (the clip's
    last pose turned about the base joint, the smallest turn whose whole drive is clear), the MiR pivots, drives and
    pivots, then the arm turns to the next clip's first pose; every arm move is a joint-space line checked every 0.5 deg.
    The clip fails (and the chapter keeps its cut) if no transport pose clears."""
    import pickle
    a = pickle.load(open(SP.TRAJ / f"shop_{from_clip}.pkl", "rb"))
    b = pickle.load(open(SP.TRAJ / f"shop_{to_clip}.pkl", "rb"))
    fa, fb = a["frames"][-1], b["frames"][-1 if to_last else 0]
    M0, M1 = np.asarray(fa["mirs"][akey]["M"], float), np.asarray(fb["mirs"][akey]["M"], float)
    arm_dx = fa["mirs"][akey]["arm_dx"]
    q0, q1 = np.asarray(fa["arms"][akey]["q"], float), np.asarray(fb["arms"][akey]["q"], float)
    c0, c1 = float(fa["arms"][akey]["close"]), float(fb["arms"][akey]["close"])
    tool0, tool1 = fa["arms"][akey]["tool"], fb["arms"][akey]["tool"]
    items = []
    for key, parts in world_parts:
        items += SP.shop_world(key, parts)
    world = Group([Body(n, *vf, kind="cell", color=col) for n, vf, col in items])
    base, yaw = arm_base_of(M0, arm_dx)
    arm = SP.make_arm(akey, base, yaw, "2F-85")
    robot = Group(mir_bodies(arm_dx))
    for bb in arm.bodies():
        robot.add(bb)
    mb = [bb for bb in robot.bodies.values() if bb.name.startswith("mir/")]
    # what the arm still holds at the end of the first clip (its pose fixed to tool0 over the last frames)
    arm.base = np.asarray(fa["arms"][akey]["base"], float)
    arm.place(q0, c0)
    W0 = arm.base @ arm.fk()["tool0"]
    held = {}
    if tool0 in ("nut runner", "cutter"):          # round 9: the tool in the gripper is swept too (the nut runner's
        tb = nut_runner_body() if tool0 == "nut runner" else Body("box cutter", *S.box(-10, 10, -8, 8, -38, 42),
                                                                  kind="held")
        robot.add(tb)                              # extension went through the MiR's finger stand as the arm turned)
        held["__tool"] = (arm.tcp_off(c0), tb)
    # round 10 (scene_audit, chapter 30: MiR A's base 25 mm through the deck blocks it left behind): what rests on the
    # MiR's deck rides with it (recorded every frame at the MiR's pose) and is swept as part of the robot
    Minv0 = np.linalg.inv(M0)
    deck = {}
    for o, Mo in fa["objs"].items():
        spec = a["objects"].get(o)
        if spec is None or spec.get("kind") not in ("box", "boxes"):
            continue
        rel = np.linalg.inv(W0) @ np.asarray(Mo, float)
        bxs = [spec["b"]] if spec["kind"] == "box" else list(spec["boxes"])
        if spec["kind"] == "box" and np.linalg.norm(rel[:3, 3]) < 300.0:
            hb_ = Body(f"held/{o}", *C.merge([S.box(*b_) for b_ in bxs]), kind="held")
            robot.add(hb_)
            held[o] = (rel, hb_)
            continue
        relm = Minv0 @ np.asarray(Mo, float)              # on the deck: inside the MiR's footprint, above its body
        if abs(relm[0, 3]) <= S.MIR["L"] / 2 and abs(relm[1, 3]) <= S.MIR["W"] / 2 and relm[2, 3] >= S.MIR["H"]:
            db_ = Body(f"deck/{o}", *C.merge([S.box(*b_) for b_ in bxs]), kind="robot")
            robot.add(db_)
            deck[o] = (relm, db_)
    # round 10 (chapter 30: the nut runner's extension 8.6 mm into the MiR's own finger stand as the arm turned): the
    # arm beyond its shoulder, the gripper, the tool and what it holds against the MiR's own bodies (robot against
    # world never tested those: both are in `robot`)
    own = Group([bb for k_, bb in arm.links.items() if k_ not in ("base", "shoulder")] + list(arm.grip.values())
                + list(arm.caps.values()) + [hb_ for _, hb_ in held.values()])
    mirg = Group(mb + [db_ for _, db_ in deck.values()])

    def place(M, q, close):
        for bb in mb:
            bb.place(M)
        for o, (relm, db_) in deck.items():
            db_.place(M @ relm)
        p, y = arm_base_of(M, arm_dx)
        arm.base = Tm(C.rot((0, 0, 1), y), p)
        arm.place(q, close)
        W = arm.base @ arm.fk()["tool0"]
        for o, (rel, hb_) in held.items():
            hb_.place(W @ rel)

    def first_hit(M, q, close):
        place(M, q, close)
        h = group_hits(robot, world, first=True) or group_hits(own, mirg, first=True)
        return None if not h else (h[0][0].name, h[0][1].name)

    legs = drive_legs(M0, M1)

    def lift_q(M, q, close, dz):
        """Round 10: q with the TCP raised dz mm, its orientation kept (the IK branch nearest q); None if out of reach or
        on another branch."""
        if dz <= 0.0:
            return q
        place(M, q, close)
        T = arm.tcp(q, close)
        T2 = T.copy()
        T2[2, 3] += dz
        sols = arm.ik_all(T2, q)
        if not sols or float(np.abs(sols[0] - q).max()) > math.radians(60.0):
            return None
        return np.asarray(sols[0], float)

    def sweep(segs_out, qt, segs_in):
        """None if the drive with the arm at qt and the arm moves (segments at the start and end docks) are clear, else
        the first hit."""
        n = 0
        for qa, qb, M in [(a_, b_, M0) for a_, b_ in segs_out] + [(a_, b_, M1) for a_, b_ in segs_in]:
            k_n = max(2, int(math.degrees(float(np.abs(qb - qa).max())) / 0.5) + 1)
            for k in range(k_n):
                u = k / (k_n - 1)
                h = first_hit(M, qa + (qb - qa) * u, c0)
                n += 1
                if h:
                    return ("arm", round(u, 3)) + h, n
        for kind, f, T, amount in legs:
            k_n = max(2, int(amount / (2.0 if kind == "pivot" else 20.0)) + 1)
            for k in range(k_n):
                h = first_hit(f(k / (k_n - 1)), qt, c0)
                n += 1
                if h:
                    return (kind, round(k / (k_n - 1), 3)) + h, n
        return None, n

    # round 10: with a long tool in the gripper (the nut runner's extension reaches ~260 mm under the TCP, down to the
    # sill trim's and the finger stand's height at the park pose) the tool is first lifted straight up, then turned
    tried, qt, checked, plan = [], None, 0, None
    lifts = (0.0, 150.0, 250.0) if "__tool" in held else (0.0,)
    for dz in lifts:
        q0L, q1L = lift_q(M0, q0, c0, dz), lift_q(M1, q1, c0, dz)
        if q0L is None or q1L is None:
            tried.append(dict(lift_mm=dz, hit="no IK for the lift"))
            continue
        for turn in (0.0, 30.0, -30.0, 60.0, -60.0, 90.0, -90.0, 120.0, -120.0, 150.0, -150.0, 180.0):
            cand = q0L.copy()
            cand[0] = q0L[0] + math.radians(turn)
            segs_out = [(q0, q0L), (q0L, cand)] if dz else [(q0, cand)]
            segs_in = [(cand, q1L), (q1L, q1)] if dz else [(cand, q1)]
            h, n = sweep(segs_out, cand, segs_in)
            checked += n
            tried.append(dict(lift_mm=dz, turn_deg=turn, hit=h))
            if h is None:
                qt, plan = cand, (segs_out, segs_in)
                break
        if qt is not None:
            break
    clip = Clip(name, "aisle", chapter)
    clip.meta.update(caption=caption, sub=sub, who=[f"robot {akey}"], step=step, status="pass")
    for o, Mo in fa["objs"].items():
        clip.obj(o, Mo, a["objects"].get(o))
    ok = qt is not None
    clear = math.inf
    t_drive = 0.0

    def arm_move(M, qa, qb, ca, cb, label):
        T = max(1.0, math.degrees(float(np.abs(qb - qa).max())) / 45.0)
        nf = max(1, int(round(T * FPS)))
        for k in range(nf):
            u = ease((k + 1) / nf)
            place(M, qa + (qb - qa) * u, ca + (cb - ca) * u)
            for o, (rel, hb_) in held.items():
                if o != "__tool":
                    clip.obj(o, hb_.M)
            for o, (relm, db_) in deck.items():
                clip.obj(o, db_.M)
            clip.set_arm(akey, arm, tool1 if (label == "in" and u > 0.5) else tool0, mir=dict(M=M.copy(), arm_dx=arm_dx))
            clip.frame(1, sub=f"{sub} | " + ("the arm to its transport pose" if label == "out" else
                                               "the arm to its working pose"))
        return T

    if ok:
        t_out = sum(arm_move(M0, a_, b_, c0, c0, "out") for a_, b_ in plan[0])
        for kind, f, T, amount in legs:
            nf = max(1, int(round(T * FPS)))
            for k in range(nf):
                M = f((k + 1) / nf)
                place(M, qt, c0)
                for o, (rel, hb_) in held.items():
                    if o != "__tool":
                        clip.obj(o, hb_.M)
                for o, (relm, db_) in deck.items():
                    clip.obj(o, db_.M)
                if k % 6 == 0:
                    d, _, _ = group_distance(robot, world, margin=300.0)
                    clear = min(clear, d)
                clip.set_arm(akey, arm, tool0, mir=dict(M=M.copy(), arm_dx=arm_dx))
                clip.frame(1, sub=f"{sub} | {kind} " + (f"{amount:.1f} deg" if kind == "pivot" else f"{amount / 1000:.2f} m"))
            t_drive += T
        t_in = 0.0
        for j_, (a_, b_) in enumerate(plan[1]):           # the gripper closes to the next clip's on the last segment
            last = j_ == len(plan[1]) - 1
            t_in += arm_move(M1, a_, b_, c0, c1 if last else c0, "in" if last else "in-lift")
    res = dict(ok=ok, fail=None if ok else f"no transport pose clears: {tried[-1]}", poses_checked=checked,
               transport_turn_deg=tried[-1]["turn_deg"] if ok else None, transport_lift_mm=tried[-1].get("lift_mm") if ok
               else None, tried=tried,
               legs=[dict(kind=k_, seconds=round(T_, 2), amount=round(a_, 1)) for k_, _, T_, a_ in legs],
               drive_s=round(t_drive, 2), clear_mm=round(clear, 1) if clear < math.inf else None,
               reverse_mm=0.0, sideways_mm=0.0, time_s=round(t_drive + (t_out + t_in if ok else 0.0), 2))
    RESULTS[name] = res
    clip.result = res
    clip.save()
    print(name, "ok" if ok else "FAIL", res["fail"], "poses", checked, "clear", res["clear_mm"], "turn",
          res["transport_turn_deg"], "s", res["time_s"], flush=True)
    return clip


def clip_drive_vf4c_lathe():
    """Chapter 30: MiR A from the VF-4 after the F-S1 clamps to the lathe, so the doors can shut behind it."""
    row = next(r for r in states()["rows"] if r.get("setup") == "F-S1")
    parts, meta, P, M_setup, m = vf4_setup("frame_B", k_state=0, rots=row["rots"])
    return clip_drive("drive_vf4c_lathe", "30-machining-chamber", "A", "vf4_clamps", "lathe_slug",
                      [("vf4", parts), ("lathe", E.st10(door=1.0, jaw_open=6.0)[0])],
                      "Arm A's MiR drives on to the lathe; the doors shut behind it",
                      "pivot, drive forward, pivot (a differential-drive base: no sliding sideways); 1.0 m/s, 0.3 m/s2; "
                      "every pose swept with FCL", "F-S1")


def clip_drive_vf4f_lathe():
    """Chapter 30: MiR A from the VF-4 after loading the floor plate (P-S1) to the lathe."""
    row = next(r for r in states()["rows"] if r.get("setup") == "P-S1")
    parts, meta, P, M_setup, m = vf4_setup("floor_A", k_state=0, part="floor", rots=row["rots"])
    return clip_drive("drive_vf4f_lathe", "30-machining-chamber", "A", "vf4_floor_load", "lathe_slug",
                      [("vf4", parts), ("lathe", E.st10(door=1.0, jaw_open=6.0)[0])],
                      "Arm A's MiR drives on to the lathe; the doors shut behind it",
                      "pivot, drive forward, pivot; every pose swept with FCL", "P-S1")


def clip_drive_deburr_measure():
    """Chapter 32: MiR A from the deburr spindle to the measuring station, along the north row."""
    return clip_drive("drive_deburr_measure", "32-finishing", "A", "deburr", "measure",
                      [("wash", E.wash_deburr()[0]), ("measure", E.granite_station()[0])],
                      "Arm A's MiR drives on to the measuring station",
                      "pivot, drive forward, pivot (a differential-drive base: no sliding sideways); 1.0 m/s, 0.3 m/s2; "
                      "every pose swept with FCL", "measure class")


def clip_lathe_park():
    """Chapter 31: arm A turns to a transport pose while the lathe's door shuts, the lathe runs and the door opens (the
    door's handle sweeps through the upper arm at its home pose), then back for the unload. The two joint-space moves
    are checked with FCL every 0.5 deg against the ST-10 with its door open; the transport pose against the door at 0,
    0.25, 0.5, 0.75 and 1 open as well."""
    import pickle
    a = pickle.load(open(SP.TRAJ / "shop_lathe_slug.pkl", "rb"))
    fa = a["frames"][-1]
    akey = "A"
    M0 = np.asarray(fa["mirs"][akey]["M"], float)
    arm_dx = fa["mirs"][akey]["arm_dx"]
    q0, c0 = np.asarray(fa["arms"][akey]["q"], float), float(fa["arms"][akey]["close"])
    tool0 = fa["arms"][akey]["tool"]
    open_items = SP.shop_world("lathe", E.st10(door=1.0, jaw_open=6.0)[0])
    door_items = []
    for d in (0.0, 0.25, 0.5, 0.75):
        door_items += [(f"{n} at {d:.2f}", vf, col) for n, vf, col in
                       SP.shop_world("lathe", {k: v for k, v in E.st10(door=d, jaw_open=6.0)[0].items()
                                               if k.startswith("door")})]
    w_open = Group([Body(n, *vf, kind="cell") for n, vf, col in open_items])
    w_all = Group([Body(n, *vf, kind="cell") for n, vf, col in open_items + door_items])
    base, yaw = arm_base_of(M0, arm_dx)
    arm = SP.make_arm(akey, base, yaw, "2F-85")
    arm.base = np.asarray(fa["arms"][akey]["base"], float)
    robot = Group(arm.bodies())

    def hit(q, world):
        arm.place(q, c0)
        h = group_hits(robot, world, first=True)
        return None if not h else (h[0][0].name, h[0][1].name)

    qt, tried, checked = None, [], 0
    for turn in (-30.0, 30.0, -60.0, 60.0, -90.0, 90.0, -120.0, 120.0, -150.0, 150.0, 180.0):
        cand = q0.copy()
        cand[0] = q0[0] + math.radians(turn)
        h = hit(cand, w_all)
        checked += 1
        if h is None:
            n = max(2, int(abs(turn) / 0.5) + 1)
            for k in range(n):
                h = hit(q0 + (cand - q0) * (k / (n - 1)), w_open)
                checked += 1
                if h:
                    break
        tried.append(dict(turn_deg=turn, hit=h))
        if h is None:
            qt = cand
            break
    clip = Clip("lathe_park", "lathe", "31-machining-parts")
    clip.meta.update(caption="Arm A clears the lathe's door", sub="its transport pose while the door shuts; FCL-checked",
                     who=["robot A"], step="lathe class", status="pass")
    for o, Mo in fa["objs"].items():
        clip.obj(o, Mo, a["objects"].get(o))
    ok = qt is not None
    if ok:
        for qa, qb, label in ((q0, qt, "the arm to its transport pose, clear of the door"),
                              (qt, q0, "the arm back to the door")):
            T = max(1.0, math.degrees(float(np.abs(qb - qa).max())) / 45.0)
            nf = max(1, int(round(T * FPS)))
            for k in range(nf):
                u = ease((k + 1) / nf)
                arm.place(qa + (qb - qa) * u, c0)
                clip.set_arm(akey, arm, tool0, mir=dict(M=M0.copy(), arm_dx=arm_dx))
                clip.frame(1, sub=label)
    res = dict(ok=ok, fail=None if ok else f"no transport pose clears: {tried[-1]}", poses_checked=checked, tried=tried,
               transport_turn_deg=tried[-1]["turn_deg"] if ok else None)
    RESULTS["lathe_park"] = res
    clip.result = res
    clip.save()
    print("lathe_park", "ok" if ok else "FAIL", res["fail"], "turn", res["transport_turn_deg"], flush=True)
    return clip


def clip_drive_vf4_lathe():
    """Chapter 31: MiR A from the VF-4 (after the vise part) to the lathe (before the slug), along the north row."""
    vf4p, _ = E.vf4(door=1.0, table_x=-E.TABLE_LAYOUT["vise"], with_vise=True, vise_open=120.0, with_hrt=True)
    return clip_drive("drive_vf4_lathe", "31-machining-parts", "A", "vf4_vise_part", "lathe_slug",
                      [("vf4", vf4p), ("lathe", E.st10(door=1.0, jaw_open=6.0)[0])],
                      "Arm A's MiR drives on to the lathe",
                      "pivot, drive forward, pivot (a differential-drive base: no sliding sideways); 1.0 m/s, 0.3 m/s2; "
                      "every pose swept with FCL", "lathe class")


def clip_hrt_bolts():
    """F-S3 (round 9, P1): arm A drives the four M8 screws that hold the dummy-floor plate (with the frame on it) to the
    HRT210's platter, through the frame's opening, with the nut runner held by its fin; round 8 left them to a person,
    not shown. The rotary at A 90 (the loading index), the table at TABLE_LAYOUT's hrt_load_x as chapter 30 has it
    (round 10: 220, with the rotary 180 mm further left on the table; round 9's 40)."""
    a_deg = 90.0
    row = next(r for r in states()["rows"] if r.get("setup") == "F-S3" and r.get("part") == "frameT")
    parts, meta, P, M_setup, m = vf4_setup("frame_C0", table_x=E.TABLE_LAYOUT["hrt_load_x"], k_state=row["k"], part="frameT", rots=row["rots"],
                                           a_deg=a_deg)
    heads = []
    for k, (yy, zz) in enumerate(((55.0, 55.0), (-55.0, 55.0), (-55.0, -55.0), (55.0, -55.0))):
        nm = f"platter screw {k + 1}"
        parts[nm] = E.Part(E.cyl((-3.9, yy, zz), (4.1, yy, zz), 6.5, res=20), "#2b2f33", M=M_setup)
        heads.append((nm, (M_setup @ np.r_[4.1, yy, zz, 1.0])[:3]))
    st = station("vf4")
    job = Job("VF-4 F-S3: arm A drives the platter screws through the frame's opening (nut runner)", "vf4", parts,
              x_mir=0.0 - S.ARM_DX)
    frame = part_body("frame on the rotary", m)
    frame.place(st.M @ P)
    job.sc.world.add(frame)
    runner = nut_runner_body()
    ax = st.R() @ np.array([1.0, 0.0, 0.0])            # the A axis (station +x) in the world
    up = np.array([0.0, 0.0, 1.0])
    wps = []
    for n, h in heads:
        hw = st.to_world(h)
        Tw = K.T_at(hw + ax * (NUT_RUNNER["ext"][1] + 1.0), -ax, up)
        Ta = K.lift(Tw, dz=0.0, dx=float(ax[0] * 90.0), dy=float(ax[1] * 90.0))
        wps.append((n, Ta, Tw))
    close = job.arm.close_for_gap(20.0)
    tool_passes(job, runner, wps, close, allow=[f"vf4/{n}" for n, _ in heads] + ["frame on the rotary"],
                dwell=[("tighten to 25 N m", 2.5)] * 4)
    clip = Clip("hrt_bolts", "vf4", "30-machining-chamber")
    r = done("hrt_bolts", job, clip, dict(screws=len(heads)))
    clip.state["mach"] = dict(station="vf4", door=1.0, table_x=E.TABLE_LAYOUT["hrt_load_x"], table_y=0.0, spindle_z=None, fc="frame_C0",
                              a_deg=a_deg)
    clip.set_arm("A", job.arm, "nut runner", mir=mir_state(job))
    record_job(clip, job, "A", tool="nut runner", meta_by_seg={"*": dict(
        caption="Arm A drives the four screws that hold the plate to the 4th axis",
        sub="M8 screws through the frame's opening into the HRT210's platter; nut runner held by its fin; FCL on meshes, "
            "0.5 deg planning, 0.2 deg audit", who=["robot A"], step="F-S3", status="pass" if r["ok"] else "fail")})
    clip.save()
    return clip


def clip_drive_bolts_lathe():
    """Chapter 30: MiR A from the VF-4 after the platter screws to the lathe."""
    row = next(r for r in states()["rows"] if r.get("setup") == "F-S3" and r.get("part") == "frameT")
    parts, meta, P, M_setup, m = vf4_setup("frame_C0", table_x=E.TABLE_LAYOUT["hrt_load_x"], k_state=row["k"], part="frameT", rots=row["rots"],
                                           a_deg=90.0)
    return clip_drive("drive_bolts_lathe", "30-machining-chamber", "A", "hrt_bolts", "lathe_slug",
                      [("vf4", parts), ("lathe", E.st10(door=1.0, jaw_open=6.0)[0])],
                      "Arm A's MiR drives on to the lathe; the doors shut behind it",
                      "pivot, drive forward, pivot; every pose swept with FCL", "F-S3")


CLIPS = dict(vf4_clamps=clip_vf4_clamps, vf4_floor_load=clip_floor_load, vf4_vise_part=clip_vise_part,
             lathe_slug=clip_lathe_slug, lathe_big=clip_lathe_big, saw_bar=clip_saw, deburr=clip_deburr, wash=clip_wash,
             measure=clip_measure, kit=clip_kit, recv_tape=clip_recv_tape, recv_unbox=clip_recv_unbox,
             drive_vf4_lathe=clip_drive_vf4_lathe, drive_vf4c_lathe=clip_drive_vf4c_lathe,
             drive_vf4f_lathe=clip_drive_vf4f_lathe, drive_deburr_measure=clip_drive_deburr_measure,
             hrt_bolts=clip_hrt_bolts, drive_bolts_lathe=clip_drive_bolts_lathe, lathe_park=clip_lathe_park)


def main(argv):
    want = argv or list(CLIPS)
    t0 = time.time()
    for name in want:
        t1 = time.time()
        try:
            CLIPS[name]()
        except Exception as e:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            RESULTS[name] = dict(ok=False, fail=f"exception: {e!r}"[:300])
        print(f"  {name}: {time.time() - t1:.0f} s", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "shop_plan.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    old.setdefault("clips", {}).update(RESULTS)
    old["run_utc"] = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
    path.write_text(json.dumps(old, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
    print("wrote", path, f"{time.time() - t0:.0f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
