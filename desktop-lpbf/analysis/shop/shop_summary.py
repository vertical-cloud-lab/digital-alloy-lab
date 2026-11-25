"""Round 7 summary of the robot shop (issue #260, PR #266): per planned clip the arm time, the worst static joint torque
and PR 318's tip-over margin of its MiR along the recorded motion; every part of setup_plan.json / hours.json given a
motion class, its gripper and who handles it, and its time split into machine, robot and person hours; and the class's
planned motion re-checked with each part's own stock attached (vise and plate classes: FCL along the recorded path).

Reads /tmp/robotbuild/traj/shop_<clip>.pkl (shop_clips.py) and analysis/out/machining/{setup_plan,hours,dfm}.json.
Writes analysis/out/shop/shop_summary.json and /tmp/robotbuild/data/shop.json (for the summary chapter).

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/analysis/shop/shop_summary.py
"""
from __future__ import annotations

import json
import math
import pathlib
import pickle
import re
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shop_plan as SP  # noqa: E402
from shop_plan import C, E, K, S, Tm  # noqa: E402

OUT = HERE.parent / "out" / "shop"
MACH = HERE.parent / "out" / "machining"
TRAJ = pathlib.Path("/tmp/robotbuild/traj")
DATA = pathlib.Path("/tmp/robotbuild/data")
FPS = 12
TOOLS_KG = {"nut runner": 0.9, "box cutter": 0.2, "bracket": 0.8}      # held tools and the deburred part (est.)
RHO = dict(al6061=2.70, mic6=2.66, ss316l=8.0, macor=2.52, ss416=7.75, steel=7.85)

# robot changeover per setup (s): the planned arm motion comes from the class; the rest are estimates as robot-shop.md
# gives them, with Edison r7's 1-3 min per station visit for docking and AprilTag re-registration (2 min used)
CHANGE = dict(station_visit=120.0, door=6.0, air_blast=20.0, wips_probe=60.0, seat_check=5.0)
PERSON_PER_SETUP_MIN = 8.0       # watching each new setup's first minutes (first-article; Edison r7: a person's task)
GAUGE_MIN = dict(plain=4.0, seal=10.0)
LIFT_MIN = 4.0                   # a person's lift with the tube lifter, walk-up to walk-away (est.)


def arm_of(a):
    M = np.asarray(a["base"], float)
    yaw = math.degrees(math.atan2(M[1, 0], M[0, 0]))
    return C.Arm("A", base=tuple(M[:3, 3]), yaw_deg=yaw)


def clip_stats(name):
    p = TRAJ / f"shop_{name}.pkl"
    if not p.exists():
        return None
    clip = pickle.load(open(p, "rb"))
    res = clip.get("result") or {}
    kg_part = float(res.get("part_kg") or 0.0)
    fr = clip["frames"]
    out = dict(ok=res.get("ok"), planned_s=res.get("time_s"), frames=len(fr), video_s=round(len(fr) / FPS, 1),
               gripper=res.get("gripper"), part_kg=kg_part, tightest_transit=res.get("tightest_transit"),
               fine_audit_0p2deg=res.get("fine_audit_0p2deg"), fail=res.get("fail"))
    worst_tau, worst_st = 0.0, None
    arms = {}
    prev = {}
    for i, f in enumerate(fr[::3]):
        for key, a in f["arms"].items():
            arm = arms.get(key) or arm_of(a)
            arms[key] = arm
            # carried: an object whose pose changed since the last sample and sits within 400 mm of the TCP
            tcp = arm.tcp(np.asarray(a["q"], float), a["close"])[:3, 3]
            kg = 0.0
            for o, M in f["objs"].items():
                moved = o in prev and not np.allclose(prev[o], M, atol=0.5)
                if moved and np.linalg.norm(np.asarray(M)[:3, 3] - tcp) < 400.0:
                    kg = TOOLS_KG.get(o, kg_part)
            t = K.tau_frac(arm, np.asarray(a["q"], float), kg)
            if t > worst_tau:
                worst_tau = t
                mir = f["mirs"].get(key)
                if mir is not None:
                    worst_st = K.stability(arm, np.asarray(a["q"], float), np.asarray(mir["M"], float), kg)
        prev = {o: np.asarray(M) for o, M in f["objs"].items()}
    out["worst_torque_frac"] = round(worst_tau, 3)
    if worst_st:
        out["tipover_at_worst_torque"] = dict(restoring_Nm=worst_st["worst"]["restoring_Nm"],
                                              extra_kg_to_tip=worst_st["worst"]["extra_kg_to_tip"],
                                              edge=worst_st["worst"]["edge"], mass_kg=worst_st["mass_kg"])
    return out


# ----------------------------------------------------------------------------------------------- per part
def stock_of(p, dfm_by_name):
    """(kind, dims mm, kg) of a part's stock from setup_plan.json's stock string."""
    s = p.get("stock", "")
    rho = RHO.get(p.get("mat", "al6061"), 2.7) * 1e-6
    m = re.match(r"([0-9.]+) in\. plate, ([0-9.]+) x ([0-9.]+) mm", s)
    if m:
        t = float(m.group(1)) * 25.4
        a, b = float(m.group(2)), float(m.group(3))
        return "plate", (min(a, b), max(a, b), t), a * b * t * rho
    m = re.match(r"Ø([0-9.]+) in\. bar x ([0-9.]+) mm", s)
    if m:
        d = float(m.group(1)) * 25.4
        L = float(m.group(2))
        return "bar", (d, L), math.pi * (d / 2) ** 2 * L * rho
    m = re.match(r"([0-9.]+) x ([0-9.]+) x ([0-9.]+) in\. blank", s)
    if m:
        a, b, c = (float(m.group(k)) * 25.4 for k in (1, 2, 3))
        return "block", (b, a, c), a * b * c * rho
    if s.startswith("weldment"):
        return "weldment", None, p.get("mass_kg", 0.0) * 1.6
    return "tube", None, p.get("mass_kg", 0.0) * 1.3


def classify(p, kind, dims, kg):
    """The motion class a part's loading reuses, its gripper and who handles it."""
    name = p["name"]
    if kg > 10.0:
        return "person lift", "person + JumboFlex", "person"         # Edison r7: > ~10 kg is a lifting device's job
    if kind == "bar":
        d = dims[0]
        return ("lathe class (lathe_slug)", "2F-85", "robot") if d <= 82.0 else ("lathe class, 3FG15 (lathe_big)", "3FG15", "robot")
    if kind in ("weldment",):
        return "lathe + TIG (person welds)", "3FG15", "person + robot"
    if kind == "plate":
        w = dims[0]
        if w <= 80.0 and kg <= 5.0:
            return "vise class (vf4_vise_part)", "2F-85", "robot"
        return "plate class (vf4_floor_load + vf4_clamps)", "VGP20 dry / 3FG15 wet", "robot"
    if kind == "block":
        return "person lift", "person + JumboFlex", "person"
    return "saw + vise class", "2F-85", "robot"


def parts_table(clips):
    plan = json.loads((MACH / "setup_plan.json").read_text())
    hours = json.loads((MACH / "hours.json").read_text())
    hp = {h["slug"]: h for h in hours["parts"]}
    rows = []
    t_load = dict(vise=clips.get("vf4_vise_part", {}).get("planned_s") or 10.4,
                  plate=(clips.get("vf4_floor_load", {}).get("planned_s") or 9.1)
                  + (clips.get("vf4_clamps", {}).get("planned_s") or 24.7),
                  lathe=clips.get("lathe_slug", {}).get("planned_s") or 13.0,
                  lathe_big=clips.get("lathe_big", {}).get("planned_s") or 15.0)
    finish_s = sum((clips.get(k, {}).get("planned_s") or 0.0) for k in ("deburr", "wash", "measure", "kit"))
    for slug, p in plan["parts"].items():
        h = hp.get(slug, {})
        kind, dims, kg = stock_of(p, None)
        cls, grip, who = classify(p, kind, dims, kg)
        n_set = int(h.get("setups_4th_axis") or p.get("n4_used") or p.get("n3") or 2)
        machine_h = float(h.get("run_h_vendor") or h.get("run_h") or 0.0)
        arm_s = (t_load["plate"] if "plate" in cls else t_load["lathe_big"] if "3FG15" in cls else
                 t_load["lathe"] if "lathe" in cls else t_load["vise"])
        overhead = sum(CHANGE.values())
        robot_h = 0.0 if who == "person" else n_set * (2 * arm_s + overhead) / 3600.0 + finish_s / 3600.0
        seal = bool(re.search(r"O-ring|gland|seal|FKM|bore", p["name"] + " " + p.get("special", ""), re.I))
        person_h = float(h.get("cam_h") or 0.0) + n_set * PERSON_PER_SETUP_MIN / 60.0 + \
            (GAUGE_MIN["seal"] if seal else GAUGE_MIN["plain"]) / 60.0 + (0.25 if seal else 0.0)
        if who == "person":
            person_h += n_set * 2 * LIFT_MIN / 60.0
        if "TIG" in cls:
            person_h += 1.5                                     # weld + fit-up of the module body (est.)
        rows.append(dict(part=p["name"], slug=slug, stock=p.get("stock"), stock_kind=kind, stock_kg=round(kg, 2),
                         motion_class=cls, gripper=grip, who_loads=who, setups=n_set, machine_h=round(machine_h, 2),
                         robot_h=round(robot_h, 2), person_h=round(person_h, 2), cam_h=h.get("cam_h"),
                         hand_shop_h=h.get("total_h_4th"), sealing_face=seal))
    tot = {k: round(sum(r[k] for r in rows), 1) for k in ("machine_h", "robot_h", "person_h")}
    tot["hand_shop_h"] = round(sum((r["hand_shop_h"] or 0.0) for r in rows), 1)
    tot["cam_h"] = round(sum((r["cam_h"] or 0.0) for r in rows), 1)
    tot["parts"] = len(rows)
    tot["setups"] = sum(r["setups"] for r in rows)
    by_cls = {}
    for r in rows:
        c = by_cls.setdefault(r["motion_class"], dict(parts=0, setups=0, machine_h=0.0, robot_h=0.0, person_h=0.0))
        c["parts"] += 1
        c["setups"] += r["setups"]
        for k in ("machine_h", "robot_h", "person_h"):
            c[k] = round(c[k] + r[k], 2)
    return rows, tot, by_cls, dict(changeover_s=CHANGE, arm_motion_s=t_load, finishing_arm_s=round(finish_s, 1),
                                    person_per_setup_min=PERSON_PER_SETUP_MIN, gauge_min=GAUGE_MIN, lift_min=LIFT_MIN)


# ----------------------------------------------------------------------------------------------- class re-check
def class_recheck(rows):
    """The vise class's recorded path with each vise part's own stock attached (same grasp height below its top), and
    the plate class's with each plate's: FCL of the part against the VF-4, its fixtures and the MiR, every 2nd frame."""
    out = []
    for cls, clipname, key in (("vise class", "vf4_vise_part", "bracket blank"), ("plate class", "vf4_floor_load", "floor part")):
        p = TRAJ / f"shop_{clipname}.pkl"
        if not p.exists():
            continue
        clip = pickle.load(open(p, "rb"))
        mach = clip["frames"][0]["mach"]
        if cls == "vise class":
            parts, meta = E.vf4(door=1.0, table_x=mach.get("table_x", -300.0), with_vise=True, vise_open=92.0,
                                with_hrt=True)
        else:
            import shop_clips as SCL
            parts, meta, P, M_setup, m = SCL.vf4_setup("floor_A", k_state=0, part="floor", rots=[])
        items = SP.shop_world("vf4", parts)
        mir = clip["frames"][0]["mirs"].get("A")
        if mir is not None:
            items += [(f"mir/{n}", S.xf(vf, np.asarray(mir["M"])), c) for n, vf, c in S.mir_items(mir["arm_dx"])]
        W = C.Group([C.Body(n, *vf, kind="cell") for n, vf, c in items])
        poses = []
        last = None
        for f in clip["frames"]:
            M = f["objs"].get(key)
            if M is None:
                continue
            M = np.asarray(M)
            if last is not None and not np.allclose(last, M, atol=0.5):
                poses.append(M)
            last = M
        for r in rows:
            if not r["motion_class"].startswith(cls):
                continue
            kind, dims = r["stock_kind"], None
            m_ = re.match(r"([0-9.]+) in\. plate, ([0-9.]+) x ([0-9.]+) mm", r["stock"] or "")
            if not m_:
                continue
            t = float(m_.group(1)) * 25.4
            a, b = sorted((float(m_.group(2)), float(m_.group(3))))
            if cls == "vise class":            # planned: 72 (between the jaws) x 150 x 63.5, grasped 20 mm below the top
                vf = S.box(-a / 2, a / 2, -b / 2, b / 2, 63.5 - t, 63.5)
            else:                              # planned: the floor plate (its own state mesh): 317.5 x 228.6 x 25.4
                vf = S.box(-b / 2, b / 2, -a / 2, a / 2, -22.7, -22.7 + t)
            body = C.Body("part", *vf, kind="held")
            hits, best = [], math.inf
            allow = ("vise", "parallel", "edge clamp", "deck", "fixture")
            for k, M in enumerate(poses[::2]):
                body.place(M)
                for x, y in C.group_hits(C.Group([body]), W):
                    if not any(s in y.name for s in allow):
                        hits.append(y.name)
                d, _, y = C.group_distance(C.Group([body]), C.Group([b for n, b in W.bodies.items()
                                                                      if not any(s in n for s in allow)]), margin=120.0)
                best = min(best, d)
            out.append(dict(part=r["part"], motion_class=cls, stock=r["stock"], ok=not hits,
                            contacts=sorted(set(hits))[:4], clear_mm=round(best, 1) if best < math.inf else None,
                            gripper_ok=(a <= 82.0) if cls == "vise class" else True,
                            note="" if cls != "vise class" or a <= 82.0 else "wider than the 2F-85's stroke: plate class"))
    return out


def chapter_totals():
    """Per rendered chapter (meta.jsonl): frames, video seconds, the hours its frames add (common.py's counters), and the
    seconds of video per status and per who."""
    out = {}
    for ch in ("20-receiving", "30-machining-chamber", "31-machining-parts", "32-finishing"):
        p = pathlib.Path("/tmp/robotbuild/frames") / ch / "meta.jsonl"
        if not p.exists():
            continue
        tot = dict(frames=0, video_s=0.0, real_s=0.0)
        add, by_status, by_who, steps = {}, {}, {}, []
        for line in open(p):
            m = json.loads(line)
            tot["frames"] += 1
            tot["video_s"] += 1.0 / FPS
            tot["real_s"] += m.get("proc_s", 1.0 / FPS)
            for k, v in (m.get("add") or {}).items():
                add[k] = add.get(k, 0.0) + v
            st = m.get("status") or "-"
            by_status[st] = by_status.get(st, 0.0) + 1.0 / FPS
            for w_ in m.get("who") or ["-"]:
                by_who[w_] = by_who.get(w_, 0.0) + 1.0 / FPS
            if m.get("caption") and (not steps or steps[-1]["caption"] != m["caption"]):
                steps.append(dict(caption=m["caption"], step=m.get("step"), status=m.get("status"), who=m.get("who")))
        out[ch] = dict(frames=tot["frames"], video_s=round(tot["video_s"], 1), real_h=round(tot["real_s"] / 3600.0, 2),
                       add={k: round(v, 3) for k, v in add.items()},
                       video_s_by_status={k: round(v, 1) for k, v in by_status.items()},
                       video_s_by_who={k: round(v, 1) for k, v in by_who.items()}, scenes=steps)
    return out


def main():
    names = ["recv_tape", "recv_unbox", "vf4_clamps", "vf4_floor_load", "vf4_vise_part", "lathe_slug", "lathe_big",
             "saw_bar", "deburr", "wash", "measure", "kit"]
    clips = {}
    for n in names:
        st = clip_stats(n)
        if st is not None:
            clips[n] = st
            print(n, st.get("ok"), st.get("planned_s"), "torque", st.get("worst_torque_frac"),
                  "tip", (st.get("tipover_at_worst_torque") or {}).get("restoring_Nm"), flush=True)
    rows, tot, by_cls, assumptions = parts_table(clips)
    recheck = class_recheck(rows)
    person = {}
    pj = OUT / "shop_person.json"
    if pj.exists():
        person = json.loads(pj.read_text())
    chapters = chapter_totals()
    res = dict(clips=clips, parts=rows, totals=tot, by_class=by_cls, assumptions=assumptions, class_recheck=recheck,
               person_lifts=person, chapters={k: {kk: vv for kk, vv in v.items() if kk != "scenes"} for k, v in chapters.items()})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "shop_summary.json").write_text(json.dumps(res, indent=1, default=str))
    DATA.mkdir(parents=True, exist_ok=True)
    frames = {}
    fj = DATA / "shop_frames.json"
    if fj.exists():
        frames = json.loads(fj.read_text())
    (DATA / "shop.json").write_text(json.dumps(dict(
        note="robot shop (shop worker): per chapter and clip who works, pass/fail and the hours the frames stand for; "
             "per part the machine / robot / person hours (estimates as robot-shop.md round 7 states them)",
        chapters=chapters, clips_in_chapters=frames,
        clips={k: dict(ok=v.get("ok"), gripper=v.get("gripper"), arm_s=v.get("planned_s"),
                                         worst_torque_frac=v.get("worst_torque_frac"),
                                         tipover=v.get("tipover_at_worst_torque")) for k, v in clips.items()},
        totals=tot, by_class=by_cls, person_lifts=person), indent=1, default=str))
    print("totals", tot)
    print("recheck", sum(1 for r in recheck if r["ok"]), "of", len(recheck), "clear")
    print("wrote", OUT / "shop_summary.json")


if __name__ == "__main__":
    main()
