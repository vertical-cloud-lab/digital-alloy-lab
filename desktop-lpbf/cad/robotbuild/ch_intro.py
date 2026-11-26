"""Chapter 00-intro of the robot-built desktop LPBF video: the hall from above, then seven fixed views of it (about 55 s).

    xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/capmem 3G /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_intro.py

What it shows (hall.py): the robot shop (analysis/shop/shop_cell.py at common.SHOP_IN_HALL), the long table with every
part on it as delivered (kit_table.py, stock mode: machined parts as their blanks), the two-arm assembly bench
(analysis/assembly/cell2.py), the two UR12e arms each on a MiR250 (byu-vcl PR 318's meshes), a person and a soda can.
Only MiR A moves: in one shot under a fixed camera it drives 3.15 m from the parts table to the bench along its own lane,
nose first (a differential-drive MiR250 drives along its heading; round 7 had it reverse 3 m with the camera following it),
on a trapezoid at shop_cell's MiR speed, its arm parked. Each view is a cut, and inside a view the camera only drifts.
No project time passes (proc_s 0; the clocks are hidden). With ROBOTBUILD_AUDIT=1 the frames are recorded for
scene_audit.py (collisions) and walk.py (the MiR's sideways slip and reversing).
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
                   "stock racks", "kitting rack", "TIG welding"]

    def shot(n, cam0, cam1, caption, sub, labels=(), who=(), update=None, va=(30.0, 30.0)):
        for i in range(n):
            u = ease(i / max(1, n - 1))
            if update is not None:
                update(i / max(1, n - 1), i)
            cam = [lerp(cam0[0], cam1[0], u), lerp(cam0[1], cam1[1], u), (0.0, 0.0, 1.0)]
            img = h.sc.render(cam, va[0] + (va[1] - va[0]) * u)
            ch.frame(img, caption, sub=sub, who=list(who), labels=h.labels(labels), **base)

    # Round 8 (Sterling, 2026-11-26: "motion sickness"): every change of place is a CUT, and inside a shot the camera only
    # drifts: no shot sweeps the picture faster than the 7-second panning rule (1/7 of the frame width per second; video_qa.py
    # measures it on the finished file). Round 7 flew from one vantage point to the next in 3 s (the shop to the far end of the
    # table: 10 m and 200 deg of azimuth), and followed a MiR down its lane.
    # 1. the whole hall from high up, turning a little
    F = (7200.0, -3600.0, 0.0)
    c0 = [HL.orbit(F, 25500.0, -24.0, 56.0), F]
    c1 = [HL.orbit(F, 24500.0, -18.0, 53.0), F]
    shot(8 * FPS, c0, c1, "One hall: robot shop, parts table, assembly bench",
         "Two UR12e arms, each on a MiR250, machine the parts and build the machine; a person steps in only where "
         "the arms can't",
         labels=["long table", "assembly bench", "Haas VF-4 + HRT210", "CNC lathe", "bandsaw", "receiving"])
    # 2. cut: the shop, drifting along its north row
    F2 = (6600.0, -5600.0, 900.0)
    F3 = (8600.0, -5600.0, 900.0)
    c2 = [HL.orbit(F2, 9800.0, -4.0, 38.0), F2]
    c3 = [HL.orbit(F3, 9800.0, 2.0, 37.0), F3]
    shot(9 * FPS, c2, c3, "The robot shop beside the bench",
         "Haas VF-4 with an HRT210 4th axis, a Haas ST-10 lathe, a bandsaw, deburr and wash, measuring, TIG welding, "
         "receiving and racks (drawn from published layout drawings; a hypothetical shop)", labels=shop_labels)
    # 3. cut: the long table, in two fixed halves (round 7 ran 9 m along it in 9 s)
    for xa, xb, sub in ((12400.0, 10600.0, "12 m x 0.9 m, 860 mm high, in line with the assembly bench so both MiRs reach it "
                                            "from their own lane"),
                        (6900.0, 5100.0, "Machined parts are still stock blanks; anything over the arm's 12.5 kg waits on a "
                                          "pallet behind lane B for a person and a lift (kit_table.py)")):
        Fa, Fb = (xa, 0.0, 860.0), (xb, 0.0, 860.0)
        ca = [HL.orbit(Fa, 7400.0, 212.0, 36.0), Fa]
        cb = [HL.orbit(Fb, 7400.0, 208.0, 35.0), Fb]
        shot(6 * FPS, ca, cb, "The long table: every part, as it arrives", sub, labels=["long table"])
    # 4. cut: MiR A drives in from the parts table to the bench, nose first along its own lane (round 8: a differential-drive
    #    MiR250 drives along its heading; round 7 followed it reversing 3 m down its lane), then both arms at the bench.
    #    A trapezoid at shop_cell's MiR speed (1 m/s, 0.3 m/s^2) under a fixed camera; the arm stays parked
    d_drive = xa0 - xa1
    T_drive = trap_T(d_drive)
    F6 = (1500.0, -200.0, 800.0)
    c6a = [HL.orbit(F6, 7600.0, -55.0, 38.0), F6]       # high enough to see the whole lane over the shop's VF-4
    c6b = [HL.orbit(F6, 7400.0, -52.0, 37.0), F6]
    t_start = 0.75

    def drive(u, i):
        t = i / FPS - t_start
        h.mir_to("A", xa0 - trap(d_drive, t))
    n4 = int(math.ceil((t_start + T_drive + 1.5) * FPS))
    shot(n4, c6a, c6b, "MiR A drives from the parts table to the bench",
         f"{d_drive / 1000:.1f} m along its own lane, nose first, at 1 m/s with 0.3 m/s² ramps (shop_cell's MiR speed); "
         "the arm stays parked while it drives", update=drive)
    h.mir_to("A", xa1)
    F6 = (500.0, 0.0, 900.0)
    c6a = [HL.orbit(F6, 6400.0, -52.0, 30.0), F6]
    c6b = [HL.orbit(F6, 6100.0, -46.0, 29.0), F6]
    shot(6 * FPS, c6a, c6b, "Two UR12e arms on MiR250s at the bench",
         "Arm A on the front lane, arm B on the back lane (analysis/assembly/cell2.py: trunnion, Fixture B, Fixture P, "
         "the nests); each carries its tools on the MiR", labels=["trunnion", "Fixture B"])
    # 5. cut: scale, the person and the can at the table's first zone
    P = (0.5 * (LT["x0"] - 480.0 + LT["x0"] + 520.0), -130.0, 930.0)   # between the person and the can
    c7 = [HL.orbit(P, 3800.0, 158.0, 14.0), P]          # from behind lane B (the VF-4 stands 2.7 m in front of lane A)
    c8 = [HL.orbit(P, 3700.0, 148.0, 15.0), P]
    shot(7 * FPS, c7, c8, "For scale: a 1.75 m person and a soda can",
         "A 355 ml can on the 860 mm table; MakeHuman's CC0 base mesh, skinned and dressed as in byu-vcl PR 318; safety "
         "glasses in the shop")
    # 6. cut: back out
    F9 = (6500.0, -2000.0, 0.0)
    c9a = [HL.orbit(F9, 16500.0, -40.0, 46.0), F9]
    c9 = [HL.orbit(F9, 17000.0, -40.0, 46.0), F9]
    shot(5 * FPS, c9a, c9, "Next: what the parts cost and when they arrive",
         "New against used, and lead times; then the shop makes the custom parts and the two arms build the machine")
    ch.close()
    print(f"00-intro: {ch.n} frames ({ch.n / FPS:.0f} s) in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
