"""Tables and the replay file from run_assembly.py's results (issue #260, PR #266).

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/report.py
Reads analysis/out/assembly/results.json (+ results_M.json if chapter 3 was re-run on its own), seals_forces.json and
/tmp/asm/frames.pkl; writes steps.md (the step table), sequence.json (for render_build.py: parts, insertion waypoints
ending at the identity, tool, arm, clearance, pass/fail, seal method) and push.json (largest push at the force steps'
poses, with link masses loading only the joints upstream of them, as shop_checks.joint_torques).
"""
from __future__ import annotations

import json
import math
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "assembly"
sys.path.insert(0, str(HERE))


def load_rows():
    rows = json.loads((OUT / "results.json").read_text())["rows"]
    pm = OUT / "results_M.json"
    if pm.exists():
        m = {r["id"]: r for r in json.loads(pm.read_text())["rows"]}
        rows = [m.get(r["id"], r) if r["id"].startswith("M") else r for r in rows]
        have = {r["id"] for r in rows}
        rows = [r for r in rows] + [r for k, r in m.items() if k not in have]
        order = {s["id"]: i for i, s in enumerate(__import__("sequence").steps())}
        rows.sort(key=lambda r: (order.get(r["id"].rstrip("h"), 999), r["id"]))
    return rows


# ---------------------------------------------------------------- corrected static torques (shop_checks.joint_torques)
UR_M = [7.369, 13.051, 3.989, 2.1, 1.98, 0.615]
TAU = np.array([330.0, 330.0, 150.0, 56.0, 56.0, 56.0])


def joint_torques(arm, q, payload_kg=0.0, tool_kg=2.0, F_world=None):
    F = arm.fk(q)
    names = ("shoulder", "upper_arm", "forearm", "wrist1", "wrist2", "wrist3")
    W = {k: arm.base @ F[k] for k in names + ("tool0",)}
    o = {k: W[k][:3, 3] for k in W}
    axes = [W[k][:3, 2] for k in names]
    origins = [o[k] for k in names]
    tcp = arm.tcp(q)[:3, 3]
    pts = [(UR_M[0], o["shoulder"], 1), (UR_M[1], (o["upper_arm"] + o["forearm"]) / 2, 2), (UR_M[2], (o["forearm"] + o["wrist1"]) / 2, 3),
           (UR_M[3], o["wrist1"], 4), (UR_M[4], o["wrist2"], 5), (UR_M[5], o["wrist3"], 6), (tool_kg, o["tool0"], 6), (payload_kg, tcp, 6)]
    g = np.array([0.0, 0.0, -9.81])
    tau = np.zeros(6)
    for m, p, n in pts:
        for j in range(n):
            tau[j] += float(np.cross(axes[j], (p - origins[j]) / 1000.0) @ (m * g))
    if F_world is not None:
        for j in range(6):
            tau[j] += float(np.cross(axes[j], (tcp - origins[j]) / 1000.0) @ np.asarray(F_world, float))
    return -tau


def push_limit(arm, q, d, payload_kg=0.0, tool_kg=2.0):
    d = np.asarray(d, float) / np.linalg.norm(d)
    t0 = joint_torques(arm, q, payload_kg, tool_kg)
    t1 = joint_torques(arm, q, payload_kg, tool_kg, F_world=d) - t0
    best = math.inf
    for i in range(6):
        if abs(t1[i]) < 1e-9:
            continue
        room = (TAU[i] - t0[i]) / t1[i] if t1[i] > 0 else (-TAU[i] - t0[i]) / t1[i]
        best = min(best, room)
    return float(best), float(np.max(np.abs(t0) / TAU))


def push_table(frames):
    import cell2 as K
    out = []
    for sid, d, kg in (("C02:1", (0, 0, -1), 0.05), ("C10:1", (0, 0, -1), 2.7), ("F39:1", (0, 1, 0), 0.4), ("F46:1", (0, 1, 0), 0.6),
                       ("M22:1", (0, 0, -1), 1.0), ("M23:1", (0, 0, -1), 0.1), ("F30:1", (0, 0, -1), 2.65)):
        fr = frames.get(sid)
        if not fr:
            continue
        for n in ("A", "B"):
            a = fr["arms"][n]
            if a["held"] is None:
                continue
            arm = K.ArmT(n, a["dock"], "front" if n == "A" else "back")
            arm.set_tool(a["tool"]) if a["tool"] in ("screwdriver", "nutrunner", "vacuum", "roller", "roller_n") else arm.set_tool("gripper")
            q = np.asarray(a["q"], float)
            arm.close = a["close"]
            F, frac = push_limit(arm, q, d, kg)
            out.append(dict(step=sid.split(":")[0], arm=n, direction=d, payload_kg=kg, max_push_N=round(F, 0), holding_torque_frac=round(frac, 2)))
    return out


# ---------------------------------------------------------------- the replay file
def sequence_json(rows, dual=None):
    import sequence as SQ
    dual = dual or {}
    parts = json.loads(pathlib.Path("/tmp/asm/parts.json").read_text())
    names = [p["name"] for p in parts]
    expl = {p["name"]: p["explode"] for p in parts}

    def match(keys, exclude=(), screws=False):
        out = []
        for k in keys:
            if k == "@module":
                out += [p["name"] for p in parts if p["group"] in ("module", "piston")]
            elif k == "@legs":
                out += [n for n in names if n.startswith("Chamber legs")]
            elif k == "@posts":
                out += [n for n in names if n.startswith("Optics bridge posts")]
            elif k == "@chamberset":
                out.append("(everything in the chamber sub-assembly: chamber body, inserts, outlet plenum, funnel, module, Z stage, legs and their screws)")
            else:
                out += [n for n in names if k in n and not any(x in n for x in exclude) and (screws or "x McMaster" not in n or "insert" in n.lower())]
        seen, res = set(), []
        for n in out:
            if n not in seen:
                seen.add(n)
                res.append(n)
        return res
    by = {r["id"]: r for r in rows}
    seq = []
    for st in SQ.steps():
        r = by.get(st["id"], {})
        e = dict(id=st["id"], label=st["label"], do=st["do"], arm=st.get("actor"), holder=st.get("holder"), tool=st.get("tool"),
                 status=dict(sweep=r.get("sweep"), arm=r.get("arm")), min_gap_mm=r.get("gap"), gap_with=r.get("gap_with"),
                 arm_clearance_mm=r.get("arm_clear"), arm_clearance_with=r.get("arm_clear_with"), why=r.get("why"))
        if st["do"] in ("place", "seal", "dual"):
            ps = match(st.get("keys", []), st.get("exclude", ()))
            e["parts"] = ps
            path = st.get("path")
            if path == "explode" and ps:
                ex = expl.get(ps[0], [0, 0, 0])
                path = [(0, 0, 0), tuple(ex)]
            if isinstance(path, list):
                wp = [list(map(float, p)) for p in path[::-1]]
                e["waypoints"] = wp                                  # translations from the final pose, ending at [0, 0, 0]
                if st.get("rot"):
                    e["rotation"] = dict(axis=[0, 0, 1], deg=float(st["rot"]), note="turned this much about z before the path; "
                                                                                    "turned back to 0 at the seat (bayonet)")
            if st["do"] == "seal":
                e["seal_method"] = r.get("method")
            if st["do"] == "dual" and st.get("flip"):
                import cell2 as K2
                import run_assembly as RA
                Fs = RA.carry_frames(K2.Cell(None), st)
                d = dict(frames=Fs)
                if Fs:
                    Fs = [np.asarray(f, float) for f in Fs]
                    Fe = np.linalg.inv(Fs[-1])
                    e["frames_checked"] = len(dual.get(st["id"], {}).get("frames", []))
                    e["frames_total"] = len(Fs)
                    ks = list(range(0, len(Fs), max(1, len(Fs) // 30))) + [len(Fs) - 1]
                    e["waypoints_4x4"] = [np.round(Fe @ Fs[k], 3).tolist() for k in ks]
                    e.pop("waypoints", None)
                e["note"] = ("turned over 180 deg about y between two fixtures, carried by both arms by two legs or two side walls: "
                             "waypoints_4x4 are the part's pose relative to its final pose (model frame), ending at the identity")
        elif st["do"] == "screws":
            e["joint"] = st["joint"]
            e["pn"] = st.get("pn")
            e["driver"] = r.get("driver")
            e["torque_Nm"] = st.get("torque_Nm")
            e["per_screw"] = [dict(screw=p["screw"], ok=p["ok"], clearance=p.get("clear")) for p in r.get("per_screw", [])]
        elif st["do"] == "flip":
            e["note"] = f"sub-assembly '{st['grp']}' turned over 180 deg about y by one arm (wrist roll), from {st['frm']} to {st['to']}"
        elif st["do"] == "note":
            e["who"] = st["who"]
            e["why"] = st["why"]
        seq.append(e)
    (OUT / "sequence.json").write_text(json.dumps(dict(
        frame="model (machine) coordinates of lpbf_low.py; waypoints are translations of the part from its final pose, in "
              "insertion order, ending at [0, 0, 0]", steps=seq), indent=1, default=str))
    return seq


def fmt(x, nd=1):
    if x is None or x == "":
        return ""
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def steps_md(rows, seals, push):
    import sequence as SQ
    lab = {s["id"]: s for s in SQ.steps()}
    L = ["# Robotic build of the M50 desktop LPBF: every step checked", "",
         "Generated by `report.py` from `run_assembly.py`. Sweep: the part along its insertion path against what is already in its "
         "sub-assembly (FCL on 0.1 mm meshes, OpenCascade booleans to confirm a block); gap = smallest clearance on the way. Arm: "
         "IK at every 3 mm of the path on one branch, FCL each frame for both arms, tools, D405, changer and held part, the approach "
         "planned (RRT-Connect), 1.5 mm depth limit at the seat (byu-vcl PR 318). Clearance = smallest distance from the tool, "
         "wrist, forearm and held part to anything they are not meant to touch.", "",
         "| Step | What | Tool | Arm | Sweep | Gap (mm) | Arms | Arm clearance (mm) | Force / torque | Notes |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    fneed = {f["step"]: f for f in (seals or {}).get("forces", []) if f.get("step", "").startswith(("C", "M", "F"))}
    pmax = {p["step"]: p["max_push_N"] for p in (push or []) if "max_push_N" in p}
    for r in rows:
        st = lab.get(r["id"].rstrip("h"), {})
        tool = r.get("driver") and "/".join(r["driver"]) or r.get("tool") or ""
        who = r.get("who", "")
        note = r.get("why") or ""
        if r.get("do") == "screws" and r.get("n"):
            note = f"{r.get('n_ok')}/{r.get('n')} screws; " + note
        if r.get("mass_kg"):
            note = f"{r['mass_kg']} kg; " + note
        arm = r.get("actor") or ""
        if r.get("holder"):
            arm += f" (holds: {r['holder']})"
        if who:
            arm = who
        sid = r["id"].rstrip("h")
        force = ""
        if r.get("do") == "screws":
            tq = st.get("torque_Nm") or next((x.get("torque_Nm") for x in SQ.steps() if x.get("joint") == r.get("joint")), None)
            force = f"{tq} N m" if tq else ""
        elif sid in fneed:
            f = fneed[sid]
            force = f"needs {f['need_N']:.0f} N" + (f" (peak {f['peak_N']:.0f})" if f.get("peak_N") else "")
            if sid in pmax:
                force += f"; arm can push {pmax[sid]:.0f} N"
                if f["need_N"] > pmax[sid]:
                    note = "TOO MUCH FORCE for the arm: " + f["robot"][:120] + "; " + note
                elif (f.get("peak_N") or 0) > pmax[sid]:
                    note = "peak beyond the arm: " + f["robot"][:120] + "; " + note
        elif r.get("mass_kg"):
            force = f"{r['mass_kg']} kg, {r['mass_kg'] / 2:.1f} kg per arm"
        L.append(f"| {r['id']} | {r['label'][:110]} | {tool} | {arm} | {r.get('sweep', '')} | {fmt(r.get('gap'), 2)} | {r.get('arm', '')} | "
                 f"{fmt(r.get('arm_clear'))} | {force} | {note[:260].replace('|', '/')} |")
    (OUT / "steps.md").write_text("\n".join(L) + "\n")
    return L


def main():
    rows = load_rows()
    frames = {}
    fp = pathlib.Path("/tmp/asm/frames.pkl")
    if fp.exists():
        frames = pickle.loads(fp.read_bytes()).get("frames", {})
    try:
        push = push_table(frames)
    except Exception as e:  # noqa: BLE001
        push = [dict(error=str(e))]
    (OUT / "push.json").write_text(json.dumps(push, indent=1))
    sf = OUT / "seals_forces.json"
    seals = json.loads(sf.read_text()) if sf.exists() else {}
    steps_md(rows, seals, push)
    dual = {}
    if fp.exists():
        dual = pickle.loads(fp.read_bytes()).get("dual", {})
    sequence_json(rows, dual)
    n = dict(place=0, pass_=0, fail=0)
    tot = {}
    for r in rows:
        k = (r.get("do"), r.get("arm"))
        tot[k] = tot.get(k, 0) + 1
    print(json.dumps({f"{a}:{b}": c for (a, b), c in tot.items()}, indent=1))
    print(json.dumps(push, indent=1))


if __name__ == "__main__":
    main()
