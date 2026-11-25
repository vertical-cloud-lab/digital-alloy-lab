"""Chapter 00-intro of the robot-built desktop LPBF video: the hall from above, then a fly-over (about 40 s).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_intro.py

What it shows (hall.py): the robot shop (analysis/shop/shop_cell.py at common.SHOP_IN_HALL), the long table with every
part on it as delivered (kit_table.py, stock mode: machined parts as their blanks), the two-arm assembly bench
(analysis/assembly/cell2.py), the two UR12e arms each on a MiR250 (byu-vcl PR 318's meshes), a person and a soda can.
The only motion is MiR A driving along its own lane with its arm parked (cell2's park pose), at the shop's MiR speed
(shop_cell.MIR_DRIVE: 1 m/s, 0.3 m/s^2); no arm moves. No project time passes (proc_s 0; the clocks are hidden).
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402
import hall as HL  # noqa: E402

FPS = common.FPS
LT = common.LONG_TABLE
TITLE = "The hall: two mobile manipulators, one long table"


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return tuple(float(x) + (float(y) - float(x)) * u for x, y in zip(a, b))


def trap(d, t, v=1000.0, a=300.0):
    """Distance covered at time t (s) on a trapezoidal profile over d mm (v mm/s cruise, a mm/s^2)."""
    if d <= 0:
        return 0.0
    ta = v / a
    if d < v * ta:                                   # never reaches cruise
        ta = math.sqrt(d / a)
        v = a * ta
    T = 2 * ta + (d - v * ta) / v
    t = min(max(t, 0.0), T)
    if t < ta:
        return 0.5 * a * t * t
    if t < T - ta:
        return 0.5 * a * ta * ta + v * (t - ta)
    r = T - t
    return d - 0.5 * a * r * r


def trap_T(d, v=1000.0, a=300.0):
    ta = v / a
    if d < v * ta:
        return 2 * math.sqrt(d / a)
    return 2 * ta + (d - v * ta) / v


def main():
    t0 = time.time()
    h = HL.Hall(kit="stock")
    print(f"hall: {len(h.sc.actors)} actors in {time.time() - t0:.0f} s", flush=True)
    if h.person is not None:
        h.person.set(x=LT["x0"] - 480.0, y=40.0, hd=-90.0, amp=0.0, look=(LT["x0"] + 600.0, 0.0, 900.0))
    ch = common.Chapter("00-intro", TITLE)
    xa0, xa1 = LT["x0"] + 900.0, 350.0                     # MiR A: from the table's first zone to the trunnion
    h.mir_to("A", xa0)
    h.mir_to("B", 350.0)
    base = dict(proc_s=0.0, no_clock=True)
    shop_labels = ["Haas VF-4 + HRT210", "CNC lathe", "bandsaw", "deburr + wash", "measuring", "receiving",
                   "stock racks", "kitting rack"]

    def shot(n, cam0, cam1, caption, sub, labels=(), who=(), update=None, va=(30.0, 30.0)):
        for i in range(n):
            u = ease(i / max(1, n - 1))
            if update is not None:
                update(i / max(1, n - 1), i)
            cam = [lerp(cam0[0], cam1[0], u), lerp(cam0[1], cam1[1], u), (0.0, 0.0, 1.0)]
            img = h.sc.render(cam, va[0] + (va[1] - va[0]) * u)
            ch.frame(img, caption, sub=sub, who=list(who), labels=h.labels(labels), **base)

    # 1. the whole hall from high up, turning a little
    F = (7200.0, -3600.0, 0.0)
    c0 = [HL.orbit(F, 25500.0, -28.0, 56.0), F]
    c1 = [HL.orbit(F, 23500.0, -16.0, 50.0), F]
    shot(8 * FPS, c0, c1, "One hall: a robot shop, a 12 m parts table and a two-arm assembly bench",
         "Two UR12e arms, each on a MiR250, machine the parts and build the machine; a person steps in only where "
         "the arms can't",
         labels=["long table", "assembly bench", "Haas VF-4 + HRT210", "CNC lathe", "bandsaw", "receiving"])
    # 2. down over the shop
    F2 = (6200.0, -5600.0, 900.0)
    c2 = [HL.orbit(F2, 9800.0, -10.0, 38.0), F2]
    shot(3 * FPS, c1, c2, "The robot shop beside the bench",
         "Haas VF-4 with an HRT210 4th axis, a CNC lathe, a bandsaw, deburr and wash, measuring, receiving and racks",
         labels=shop_labels)
    F3 = (9200.0, -5600.0, 900.0)
    c3 = [HL.orbit(F3, 9200.0, 8.0, 34.0), F3]
    shot(6 * FPS, c2, c3, "The robot shop beside the bench",
         "Haas VF-4 with an HRT210 4th axis, a CNC lathe, a bandsaw, deburr and wash, measuring, receiving and racks "
         "(analysis/shop/shop_cell.py)", labels=shop_labels)
    # 3. along the long table, from its far end back towards the bench
    F4 = (13200.0, 0.0, 860.0)                           # from behind lane B: MiR A and the shop stay out of view
    c4 = [HL.orbit(F4, 6200.0, 215.0, 36.0), F4]
    shot(3 * FPS, c3, c4, "The long table: every part of one machine, as it arrives",
         "12 m x 0.9 m, 860 mm high, in line with the assembly bench so both MiRs reach it from their own lane",
         labels=["long table"])
    F5 = (4300.0, 0.0, 860.0)
    c5 = [HL.orbit(F5, 6000.0, 205.0, 32.0), F5]
    shot(9 * FPS, c4, c5, "The long table: every part of one machine, as it arrives",
         "Machined parts are still stock blanks; anything over the arm's 12.5 kg waits on a pallet behind lane B "
         "for a person and a lift (kit_table.py)", labels=["long table"])
    # 4. MiR A drives along its lane to the bench, its arm parked; the camera follows
    d = xa0 - xa1
    T = trap_T(d)
    n = int(math.ceil((T + 1.0) * FPS))
    F6a, F6b = (xa0 - 300.0, -600.0, 700.0), (xa1 + 200.0, -300.0, 800.0)
    c6a = [HL.orbit(F6a, 5200.0, -48.0, 26.0), F6a]
    c6b = [HL.orbit(F6b, 5200.0, -40.0, 28.0), F6b]

    def drive(u, i):
        h.mir_to("A", xa0 - trap(d, i / FPS))
    shot(n, (c5[0], c5[1]), (c6b[0], c6b[1]), "Robot A drives along its lane to the bench, its arm parked",
         f"MiR250 at 1 m/s (0.3 m/s^2), {d / 1000:.1f} m in {T:.0f} s; robot B waits at the trunnion on lane B "
         "(analysis/assembly/cell2.py: trunnion, Fixture B, Fixture P, the nests)",
         labels=["trunnion", "Fixture B"], who=["robot A"], update=drive)
    # 5. scale: the person and the can at the table's first zone, then up and away
    P = (0.5 * (LT["x0"] - 480.0 + LT["x0"] + 520.0), -130.0, 930.0)   # between the person and the can
    c7 = [HL.orbit(P, 3800.0, 165.0, 14.0), P]          # from behind lane B (the VF-4 stands 2.7 m in front of lane A)
    shot(3 * FPS, c6b, c7, "For scale: a 1.75 m person and a 355 ml soda can on the 860 mm table",
         "MakeHuman's CC0 base mesh, skinned and dressed as in byu-vcl PR 318; safety glasses in the shop")
    c8 = [HL.orbit(P, 3600.0, 140.0, 15.0), P]
    shot(5 * FPS, c7, c8, "For scale: a 1.75 m person and a 355 ml soda can on the 860 mm table",
         "MakeHuman's CC0 base mesh, skinned and dressed as in byu-vcl PR 318; safety glasses in the shop")
    F9 = (6500.0, -2000.0, 0.0)
    c9 = [HL.orbit(F9, 17000.0, -40.0, 46.0), F9]
    shot(4 * FPS, c8, c9, "Next: what the parts cost, new and used, and how long they take to arrive",
         "Then the shop makes the custom parts and the two arms build the machine")
    ch.close()
    print(f"00-intro: {ch.n} frames ({ch.n / FPS:.0f} s) in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
