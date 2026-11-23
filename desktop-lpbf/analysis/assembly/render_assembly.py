"""Renders of the tightest moments of the robotic build (issue #260, PR #266), from run_assembly.py's snapshots.

    xvfb-run -a -s "-screen 0 1600x1200x24" /tmp/venv/bin/python desktop-lpbf/analysis/assembly/render_assembly.py
Reads /tmp/asm/frames.pkl (and frames_M.pkl), rebuilds the cell at each snapshot (both arms with their tools and held
parts, the MiRs at their docks, the fixtures, every part present) and writes PNGs, plus a GIF of the chamber turn-over,
to analysis/out/assembly/.
"""
from __future__ import annotations

import os
import pathlib
import pickle
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cell2 as K  # noqa: E402
import tooling as TL  # noqa: E402
import run_assembly as RA  # noqa: E402

OUT = HERE.parent / "out" / "assembly"
ASM_DIR = pathlib.Path(os.environ.get("ASM_DIR", "/tmp/asm"))


def build():
    run = RA.Run()
    # the temporary tool objects, in the order the run added them (M12 loader, M25 mandrel and pusher)
    (lv, lf), _ = TL.mesh("ring_loader")
    Ml = K.Tm(p=(0.0, 0.0, -96.0)) @ K.Rx(180.0)
    RA.add_temp_obj(run, "Ring loader (tool)", lv @ Ml[:3, :3].T + Ml[:3, 3], lf)
    (mv, mf), _ = TL.mesh("spigot_mandrel")
    RA.add_temp_obj(run, "Spigot mandrel (tool)", mv, mf)
    (pv_, pf), _ = TL.mesh("spigot_pusher")
    RA.add_temp_obj(run, "Spigot pusher (tool)", pv_, pf)
    return run


def draw(run, snap, held, title, path, focus=None, dist=1600.0, az=-60.0, el=25.0, highlight=()):
    import pyvista as pv
    cl, sc = run.cl, run.sc
    p = pv.Plotter(off_screen=True, window_size=(1400, 1000))
    p.set_background("white")

    def add(v, f, M, color, opacity=1.0):
        if v is None or len(f) == 0:
            return
        w = v @ M[:3, :3].T + M[:3, 3]
        faces = np.c_[np.full(len(f), 3), f].ravel()
        p.add_mesh(pv.PolyData(w, faces), color=color, opacity=opacity, smooth_shading=False)
    for n in ("A", "B"):
        a = snap["arms"][n]
        if a["dock"] is not None:
            cl.move_mir(n, a["dock"])
    for nm, b in cl.static.items():
        if nm == "floor":
            continue
        add(b.v, b.f, b.M, b.color, 0.35 if "bench" in nm or "Fixture B" in nm else 1.0)
    for i, M in snap["present"].items():
        i = int(i)
        if i >= len(sc.objs) or sc.objs[i]["V"] is None:
            continue
        o = sc.objs[i]
        col = sc.parts[o["part"]].color if o.get("kind") != "tool" else "#e8c33c"
        if i in highlight:
            col = "#d62728"
        add(o["V"], o["F"], np.asarray(M) @ sc.pose(i, {}), col)
    for n in ("A", "B"):
        a = snap["arms"][n]
        arm = cl.A if n == "A" else cl.B
        tool = a["tool"]
        if tool == "gripper" and a.get("caps"):
            run.set_tool(n, "gripper+caps")
        elif tool in ("screwdriver", "nutrunner"):
            arm.set_tool(tool)
        else:
            run.set_tool(n, tool)
        arm.release()
        arm.place(np.asarray(a["q"]), a["close"])
        for b in arm.bodies():
            col = "#9aa6b2" if b.kind == "arm" else ("#2b2f33" if b.kind == "gripper" else "#c58b2b")
            add(b.v, b.f, b.M, col)
        if a["held"] is not None and a["held"]["name"] in held:
            v, f = held[a["held"]["name"]]
            add(v, f, np.asarray(a["held"]["M"]), "#e0a040")
    if focus is None:
        focus = (K.STATIONS["B"], 0.0, 1150.0)
    f = np.asarray(focus, float)
    az_r, el_r = np.radians(az), np.radians(el)
    eye = f + dist * np.array([np.cos(el_r) * np.cos(az_r), np.cos(el_r) * np.sin(az_r), np.sin(el_r)])
    p.camera_position = [tuple(eye), tuple(f), (0, 0, 1)]
    p.add_text(title, font_size=11, color="black")
    p.show(screenshot=str(path))
    p.close()


def main():
    fr = pickle.loads((ASM_DIR / "frames.pkl").read_bytes())
    frames, held, dual = fr["frames"], fr["held"], fr.get("dual", {})
    pm = (ASM_DIR / "frames_M.pkl")
    if pm.exists():
        fm = pickle.loads(pm.read_bytes())
        frames.update({k: v for k, v in fm["frames"].items() if k.startswith("M")})
        held.update(fm["held"])
    run = build()
    shots = []
    S = K.STATIONS
    want = [("F05b-mid", "Chamber assembly (15.8 kg) carried upright by both arms, each holding a leg, from the trunnion to Fixture B",
             ((S["T"] + S["B"]) / 2, 0, 1150), 2600, -70, 22),
            ("C01b", "The trunnion has turned the chamber upside down for the under-floor work", (S["T"], 0, 1000), 1800, -60, 25),
            ("M18:1", "Heater stack, rod and gland plate into the bore from the tube's open end, module upside down", (S["body_inv"], 0, 1000), 1100, -60, 25),
            ("M25", "Spigot O-ring: mandrel on the spigot, pusher stroke", (S["body_up"], 0, 1000), 1000, -60, 25),
            ("C10:1", "Build module (upside down) into the floor port, chamber in the trunnion", (S["T"], 0, 1050), 1500, -60, 30)]
    for k in list(frames):
        if k.startswith("F29:"):
            want.append((k, "Lid cord rolled into the body's gland (roller on arm " + k.split(":")[1] + ")", (S["B"], 0, 1300), 1700, -60, 35))
            break
    import json
    res = json.loads((OUT / "results.json").read_text())["rows"]
    for jid, title in (("F06", "Base-plate-to-leg M6 screws from under the plate (inline nutrunner)"),
                       ("F19", "Recoater-rail screws, driven from inside the chamber"),
                       ("F31", "Lid M5 screws (OnRobot Screwdriver, side-mounted)"),
                       ("C15", "Leg-to-floor M6 down the leg's Ø11 bore (150 mm extension)")):
        r = next((x for x in res if x["id"] == jid), None)
        if r and r.get("per_screw"):
            idx = run.sc.find(r["per_screw"][0]["screw"].split(" (")[0])
            for i in idx:
                if f"screw:{i}" in frames:
                    want.append((f"screw:{i}", f"{jid}: {title}", None, 1300, -60, 20))
                    break
    last = list(frames)[-1] if frames else None
    if last:
        frames["__cell__"] = frames[last]
        want.insert(0, ("__cell__", "The cell: two UR12e on MiR250s, the bench with the module nests, Fixture P, the trunnion, and Fixture B "
                        "with the finished process module", (0.0, 0.0, 900.0), 4300, -65, 28))
    for key, title, focus, dist, az, el in want:
        if key not in frames:
            continue
        snap = frames[key]
        if focus is None:
            a = snap["arms"]["A"] if snap["arms"]["A"]["tool"] in ("screwdriver", "nutrunner") else snap["arms"]["B"]
            arm = run.cl.A if a is snap["arms"]["A"] else run.cl.B
            arm.place(np.asarray(a["q"]))
            focus = tuple(arm.tcp()[:3, 3])
        name = "cell" if key == "__cell__" else key.replace(":", "_").replace("-", "_")
        path = OUT / f"render_{name}.png"
        try:
            draw(run, snap, held, title, path, focus, dist, az, el)
            shots.append((path.name, title))
            print("wrote", path, flush=True)
        except Exception as e:  # noqa: BLE001
            print("failed", key, e, flush=True)
    # GIF of the turn-over
    if "F05b" in dual and dual["F05b"]["qsA"]:
        import imageio.v2 as imageio
        d = dual["F05b"]
        imgs = []
        base = frames.get("F05b-mid") or frames.get("F05b")
        n = len(d["qsA"])
        for k in list(range(0, n, max(1, n // 24))) + [n - 1]:
            snap = dict(base)
            snap["arms"] = {x: dict(base["arms"][x]) for x in ("A", "B")}
            snap["arms"]["A"]["q"] = d["qsA"][k]
            snap["arms"]["B"]["q"] = d["qsB"][k]
            snap["arms"]["A"]["held"] = dict(name=d["body"], M=d["frames"][k])
            snap["arms"]["B"]["held"] = None
            pth = (ASM_DIR / f"gif_{k:03d}.png")
            draw(run, snap, held, "Chamber assembly carried by two UR12e (F05b)", pth, ((S["T"] + S["B"]) / 2, 0, 1250), 2700, -70, 22)
            imgs.append(imageio.imread(pth)[::2, ::2])
        imageio.mimsave(OUT / "carry_F05b.gif", imgs, duration=0.25, loop=0)
        shots.append(("carry_F05b.gif", "Chamber assembly carried by both arms from the trunnion to Fixture B (F05b), every few frames of the checked path"))
    import json as _j
    (OUT / "renders.json").write_text(_j.dumps(shots, indent=1))
    print(shots)


if __name__ == "__main__":
    main()
