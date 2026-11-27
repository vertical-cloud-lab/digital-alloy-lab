"""Chapter 38-tools of the robot-built video (issue #260, PR #266, round 7): the custom tools and fixtures the two arms use,
one at a time on a turntable, before the assembly chapters show them in use.

Sterling, 2026-11-25: "it's fine for the robot to grab and use custom tools as desired (you'll need to design, render, and
simulate usage of these, though)". Every mesh here is the one the assembly planner checks for collisions
(analysis/assembly/tooling.py, the same functions and sizes; tooling.export_steps() writes their STEP files to
analysis/out/assembly/tooling/). Their use is in chapters 40 and 41, replayed from the planner's recording. Costs are
assembly-tooling.csv's (materials, labelled estimates; the bought tools' prices are not published).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_tools.py
"""
from __future__ import annotations

import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
for p in (HERE, LPBF / "analysis" / "assembly"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import common  # noqa: E402

NAME, TITLE = "38-tools", "The arms' custom tools and fixtures"
FPS = common.FPS

# (tooling function and args, title, what it does / where, made of and cost, status badge)
# status "redesign": a tool added in round 7 because a step failed without it
TOOLS = [
    (("spigot_mandrel",), "Spigot mandrel",
     "The 2-238 spigot O-ring is pushed down its cone and sleeve, over the spigot's edge, into its groove (M20)",
     "machined acetal, about $40", ""),
    (("spigot_pusher",), "Spigot pusher",
     "Pushes that ring down the mandrel evenly all round, and stops on the mandrel at the groove (M20)",
     "machined acetal tube, about $40", ""),
    (("ring_loader",), "Ring loader",
     "Carries each 2-114 rod O-ring through the Ø15.9 throat into its hidden groove (M12); a person checks with a light",
     "stainless tube and plunger, about $60", ""),
    (("rod_bullet",), "Rod bullet",
     "A PEEK nose in the hollow rod: the rod goes through the two rod O-rings without cutting them (M22)",
     "machined PEEK, about $25", ""),
    (("roller", 3.2), "Roller",
     "A sprung PTFE wheel run round a gland: presses the 3.53 mm cord into the floor and lid grooves (C00b, F29)",
     "end effector, about $250", ""),
    (("ring_caps",), "Pin caps on the gripper's fingertips",
     "Caps with a Ø2 steel pin over the 2F-85's pads: small O-rings, the Macor rings, the disc springs",
     "printed caps, about $15 a set", ""),
    (("nozzle",), "Small-part vacuum nozzle",
     "A Ø5 x 60 mm stem and 4 mm cup on the vacuum gripper: thermocouples, shims, small rings (M05, M07)",
     "about $30 on the bought VGC10", ""),
    (("liner_wand",), "Liner wand (new in round 7)",
     "Two cups on a 300 mm bar: the back liners go in through the door with the wrist outside (F10a-e; fingers met the frame)",
     "bar, two cups, ejector: about $120 (est.)", "redesign"),
    (("ring_pad",), "Ring pad (new in round 7)",
     "A silicone lip on a 100 mm stem: the camera window's 1 mm FKM rings, too narrow for a cup, too deep for fingers (F48b)",
     "printed lip, steel stem: about $60 (est.)", "redesign"),
    (("pin_pusher",), "Pin pusher (new in round 7)",
     "A magnet in a Ø4.5 rod's tip slides each hinge pin along its axis, the wrist outside the door (F52; fingers met the door)",
     "bar, rod, magnet: about $40 (est.); pins 17-4 PH", "redesign"),
    (("screwdriver", 100.0), "OnRobot Screwdriver, 100 mm bit extension",
     "M3-M5 screws; 60, 100 and 160 mm extensions keep its body clear of the part (C05, C15, F15, F19, F27)",
     "bought; extensions about $20 each", ""),
    (("nutrunner_angle",), "Angle-head nutrunner",
     "Every screw driven upward: the floor plate's 18 M4, the posts' and legs' screws from under the base plate",
     "bought, 0.5-10 N m class", ""),
    (("vacuum",), "Vacuum gripper (OnRobot VGC10)",
     "Flat parts the fingers can't span: the frame onto its fixture, the lid, the riser plate, the scan head",
     "bought", ""),
    (("trunnion_stands",), "Trunnion positioner",
     "Turns the chamber over about a 1 m high axis, so both arms work from above (C01b, F05)",
     "stands, shafts, jaws, geared motor: about $900", ""),
    (("fixture_P", 1000.0), "Fixture P",
     "The floor plate's pedestal: the frame is lowered onto its dowels and screwed from below (C00a-C01)",
     "welded steel, about $150", ""),
    (("fixture_B", 1000.0), "Fixture B",
     "Two columns under the base plate, open below so the arms reach the leg and post screws (F01-F59)",
     "welded steel, about $250", ""),
    (("nest_stack",), "Kitting nests",
     "Each part waits in the pose it is assembled in: the heater stack's pedestal, the module body's rings (M01-M27)",
     "printed or machined, about $60 each", ""),
    (("tool_stand",), "Tool stand on each MiR",
     "The tools park here between steps; the ATI QC-21 changer swaps them in about 8 s",
     "about $150 each, plus the changer's tool plates", ""),
]


def tool_polys(fn, args):
    """[PolyData] of a tooling function's shape, from tooling.mesh (the planner's cache)."""
    import pyvista as pv
    import tooling as TL
    r, _ = TL.mesh(fn, *args)
    meshes = list(r.values()) if isinstance(r, dict) else [r]
    out = []
    for v, f in meshes:
        v = np.asarray(v, float)
        f = np.asarray(f, int)
        out.append(pv.PolyData(v, np.c_[np.full(len(f), 3), f].ravel()))
    return out


def _register(sc, name, actor, group):
    """Round 9: put an actor drawn with common.MAT into the pvscene adapter as well, so audit_rec.py can record it
    (ROBOTBUILD_AUDIT=1; round 8 drew this chapter straight to the plotter, so the frame audit never saw it)."""
    sc.actors[name] = actor
    sc.group_of[name] = group
    sc.alpha[name] = 1.0
    sc.base_alpha[name] = 1.0
    sc.gmat.setdefault(group, np.eye(4))
    sc._hold(name, actor)


def main():
    import pvscene
    ch = common.Chapter(NAME, TITLE)
    pl = common.plotter()
    sc = pvscene.PVScene(pl)
    # round 8: 4.8 s a tool (0.8 s still, a 50 deg turn over 3.2 s, 0.8 s still). Round 7's 2.6 s, 150 deg turn and 0.6 s
    # hold failed video_qa.py's camera gate (median shot 3.1 s against 4 s; 95th-percentile speed 0.18 frame widths a second
    # against the 7-second rule's 0.14)
    n_pre, n_turn, n_hold = int(0.8 * FPS), int(3.2 * FPS), int(0.8 * FPS)
    for (spec, title, what, made, status) in TOOLS:
        fn, args = spec[0], spec[1:]
        try:
            polys = tool_polys(fn, args)
        except Exception as e:  # noqa: BLE001
            print(f"skip {fn}: {type(e).__name__}: {e}", flush=True)
            continue
        for nm in list(sc.actors):
            sc.remove(nm)
        pl.clear_actors()
        lo = np.min([p.points.min(0) for p in polys], axis=0)
        hi = np.max([p.points.max(0) for p in polys], axis=0)
        c = 0.5 * (lo + hi)
        size = hi - lo
        col = common.COL["fixture"] if fn.startswith(("fixture", "nest", "trunnion", "tool_stand")) else common.COL["tool"]
        acts = []
        for j, p in enumerate(polys):
            q = p.copy()
            q.points = q.points - c
            acts.append(pl.add_mesh(q, color=col, **common.MAT))
            _register(sc, f"tool/{fn}/{j}", acts[-1], "tool")
        # a 50 mm scale bar on the floor of the bounding box, along x
        import pyvista as pv
        bar = pv.Box(bounds=(-size[0] / 2, -size[0] / 2 + 50.0, -size[1] / 2 - 12.0, -size[1] / 2 - 6.0,
                             -size[2] / 2, -size[2] / 2 + 2.0))
        _register(sc, "scale bar", pl.add_mesh(bar, color="#2b2f33"), "static")
        R = 1.9 * float(np.linalg.norm(size)) + 60.0
        dims = " x ".join(f"{s:.0f}" for s in sorted(size, reverse=True))
        sub = what
        labels = [[70, 600, made], [70, 640, f"{dims} mm overall; the black bar is 50 mm"]]
        for k in range(n_pre + n_turn + n_hold):
            u = min(max(k - n_pre, 0), n_turn) / n_turn
            u = u * u * (3 - 2 * u)              # eased: no jolt where the turn starts and stops
            az = math.radians(-50.0 + 50.0 * u)
            el = math.radians(28.0)
            eye = (R * math.cos(el) * math.cos(az), R * math.cos(el) * math.sin(az), R * math.sin(el))
            pl.camera_position = [eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
            pl.camera.view_angle = 30.0
            pl.reset_camera()            # fit the bounding sphere along this view direction (same distance every frame)
            pl.camera.zoom(1.25)
            sc.apply()
            pvscene._audit(sc)           # round 9: recorded for scene_audit.py (the tool's pieces never move: 0 movers)
            img = pl.screenshot(return_img=True)
            ch.frame(img, title, sub=sub, who=[], status=status, proc_s=0.0, no_clock=True, labels=labels)
        print(f"{fn}: {n_pre + n_turn + n_hold} frames", flush=True)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
