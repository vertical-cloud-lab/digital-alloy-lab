#!/usr/bin/env python3
"""Animated assembly of the three camera units, on the rePowder model.

Each unit is put together part by part along the way it goes together (README, "Assembly, briefly"), then fitted to
its window: the front unit pushed onto AMAZEMET's LED cover, the left one clamped on the door's sight glass, the top
one built up on the blue frame and swung clear of the lid and back onto its detent. The parts are Onshape's
(../exports/onshape_partstudio.step), moved onto the model by units.py; the machine and the Scene framework are
atomizer-training/viz3d's (viz3d/model.py, viz3d/scene.py), so it looks and runs like the atomizer animations.

    xvfb-run -a -s "-screen 0 1920x1080x24" python assembly.py
        # -> ../renders/assembly_steps.gif (800 x 450, 10 fps), assembly_steps.json, assembly_steps_still.png,
        #    ../renders/mp4/assembly_steps.mp4 (1280 x 720, 15 fps)
    PREVIEW=1 xvfb-run -a -s "-screen 0 1920x1080x24" python assembly.py   # last frame of each step -> /tmp
"""
from __future__ import annotations

import numpy as np

import units as U
import model as M          # viz3d/model.py (units.py puts viz3d/ on the path)
import scene as S          # viz3d/scene.py
from render import N_FRONT, OVERALL, POST, UTILITIES, add_units, sight_line_mesh

S.OUT = U.HERE.parent / "renders"        # the Scene writes its GIF, JSON, still and mp4/ here

PORT_F = M.VIEWPORT + N_FRONT * (M.CH_Y[0] - M.VIEWPORT[1]) / N_FRONT[1]     # front port axis at the chamber face
RING_L = U.SIGHT_BASE                                                       # door sight glass, on the door panel
BENCH_F = 240.0           # the front unit is put together this far out along the port axis, then pushed on
BENCH_L = 210.0           # and the left one this far out from the door
PARK = 90.0               # degrees the arm swings to its "parked" dimple (Onshape's `park`)


def cam_at(focal, back, up=(0, 0, 1)):
    f = np.asarray(focal, float)
    return [tuple(f + np.asarray(back, float)), tuple(f), up]


INTRO = OVERALL
FRONT_BENCH = cam_at(PORT_F + N_FRONT * 200 + np.array([0, 0, -20]), (-560, -640, 250))
FRONT_SEAT = cam_at(PORT_F + N_FRONT * 80, (-470, -560, 260))
LEFT_BENCH = cam_at(RING_L + np.array([-150, -10, -10]), (-560, -560, 280))
LEFT_SEAT = cam_at(RING_L + np.array([-50, -20, -10]), (-640, -520, 260))
TOP_BUILD = cam_at((-60, 40, 1700), (-900, -1150, 520))
TOP_ARM = cam_at((-40, -60, 1660), (-1000, -1200, 560))
TOP_LID = cam_at((-80, 0, 1560), (-1250, -1600, 700))


def main() -> None:
    sc = S.Scene("assembly_steps", "rePowder viewport cameras: assembly")
    S.load_machine(sc, hide=U.HIDE_IN_MODEL + UTILITIES, pipes=False)
    add_units(sc, U.pieces())
    aim, up = U.sight_line()
    sc.add("sight", sight_line_mesh(1.4), (0.85, 0.10, 0.10), "sight", ambient=0.6, specular=0.0, shown=False)

    def names(group):
        return S.names_of(sc, group)

    def hide(*groups):
        for g in groups:
            sc.show(names(g), 0.0)

    def fly(group, vec, t0=0.0, t1=1.0, fade=True):
        """The group's parts appear and move in to where they belong, from `vec` away."""
        ns, v = names(group), np.asarray(vec, float)

        def f(u):
            e = S.window(u, t0, t1)
            if fade:
                sc.show(ns, min(1.0, 4 * e) if e > 0 else 0.0)
            sc.gmat[group] = S.T(v * (1 - e))
        return f

    def move(group, vec, t0=0.0, t1=1.0):
        """The group (already shown) moves from `vec` away to where it belongs."""
        v = np.asarray(vec, float)
        return lambda u: sc.gmat.__setitem__(group, S.T(v * (1 - S.window(u, t0, t1))))

    def ghost(group, a0, a1, t0=0.0, t1=1.0):
        """See-through while parts go in behind it."""
        ns = names(group)

        def f(u):
            e = S.window(u, t0, t1)
            for n in ns:
                sc.base_alpha[n] = a0 + (a1 - a0) * e
        return f

    def seq(*fs):
        def f(u):
            for g in fs:
                g(u)
        return f

    def swing(deg0, deg1, t0=0.0, t1=1.0):
        def f(u):
            a = deg0 + (deg1 - deg0) * S.window(u, t0, t1)
            sc.gmat["top:swing"] = S.R((0, 0, 1), a, (POST[0], POST[1], 0))
        return f

    def lid(deg0, deg1, t0=0.0, t1=1.0):
        def f(u):
            sc.gmat["hood"] = S.R((0, 1, 0), -(deg0 + (deg1 - deg0) * S.window(u, t0, t1)), M.HINGE)
        return f

    def lab(text, xyz, fx, fy):
        return (text, tuple(float(c) for c in xyz), (fx, fy))

    # start: the machine as it is; every unit part waits off screen
    for u_ in U.UNITS:
        for g in {sc.group_of[n] for n in sc.actors if sc.group_of[n].startswith(u_ + ":")}:
            if not g.endswith(":port"):
                hide(g)
    sc.gmat["front:unit"] = S.T(N_FRONT * BENCH_F)
    sc.gmat["left:unit"] = S.T(np.array([-BENCH_L, 0.0, 0.0]))
    sc.cam = INTRO
    win = U.lid_window_model()
    sc.step("0", "Three Raspberry Pi 5 camera units for the rePowder's three windows: the front view port, the door's "
            "sight glass and the furnace lid's window. Each has a small display beside its window as well as the "
            "livestream. The machine is atomizer-training/viz3d's CadQuery model; the units are the Onshape design.",
            3.0, None, hold=1.5,
            labels=[lab("front view port:\nAMAZEMET's LED cover", PORT_F + N_FRONT * 60, 0.97, 0.55),
                    lab("door sight glass", RING_L + np.array([-20, 0, 0]), 0.03, 0.56),
                    lab("furnace lid window", win, 0.03, 0.30)])

    # ------------------------------------------------------------------------------------------- front
    ax = N_FRONT
    sc.step("F.1", "Front port. AMAZEMET's 12-sided LED cover pushes onto the port's threaded nut, with its cable pod at "
            "6 o'clock. The unit clips onto the cover, so the LED ring still lights the chamber and the glass nut is "
            "never loaded.", 2.5, None, cam_to=FRONT_BENCH, hold=1.0,
            labels=[lab("LED cover, 162 across flats", PORT_F + ax * 55 + np.array([60, 0, 40]), 0.97, 0.30),
                    lab("cable pod", PORT_F + ax * 50 + np.array([0, 0, -95]), 0.97, 0.70)])
    sc.step("F.2", "The printed socket and tray (PETG), put together off the machine: a 12-sided socket that slides 15 mm "
            "over the cover's rim, notched for the pod so it goes on one way only.", 2.0,
            fly("front:socket", ax * 60), hold=1.0)
    sc.step("F.3", "HQ Camera (M12 mount) with a 16 mm M12 lens, 15 mm left of the axis: about 65 × 49 mm of the plate. "
            "Four bosses, M2.5 screws from inside the tray, ribbon up through the slot beside them.", 2.5,
            seq(ghost("front:socket", 1.0, 0.3, 0.0, 0.3), fly("front:hq", ax * 150, 0.15, 1.0)), hold=1.0)
    sc.step("F.4", "Camera Module 3 Wide, 18.5 mm right of the axis, for the nozzle, plate and chamber; M2 screws.", 2.0,
            fly("front:wide", ax * 150), hold=1.0)
    sc.step("F.5", "Raspberry Pi 5 with its Active Cooler, on M2.5 heat-set inserts. Both cameras take its two MIPI "
            "ports.", 2.0, seq(ghost("front:socket", 0.3, 1.0, 0.0, 0.4), fly("front:pi", ax * 170)), hold=1.0)
    sc.step("F.6", "5 in HDMI display (800 × 480), facing out along the port axis, about 20° up towards a standing "
            "operator. HDMI, because both MIPI ports carry cameras.", 2.0, fly("front:display", ax * 190), hold=1.0)
    sc.step("F.7", "Face plate (orange here): a push fit with a skirt over the display's edges.", 1.8,
            fly("front:face", ax * 200), hold=1.0)
    sc.step("F.8", "Screw the M6 ball plunger in until the socket goes onto the cover with a firm push. The facets stop "
            "it turning and the cover is concentric with the port, so the cameras point the same way every time.",
            3.0, move("front:unit", ax * BENCH_F), cam_to=FRONT_SEAT, hold=1.5, still=True)

    # -------------------------------------------------------------------------------------------- left
    sc.step("L.1", "Door sight glass: a ring about 65 across, 30 mm proud of the door. This unit rides on the door, above "
            "the ultrasonic stack.", 2.5, None, cam_to=LEFT_BENCH, hold=1.0,
            labels=[lab("sight glass ring", RING_L + np.array([-25, 0, 32]), 0.97, 0.22),
                    lab("ultrasonic stack (45°)", M.on_axis(300), 0.97, 0.80)])
    sc.step("L.2", "Split clamp collar and tray (PETG).", 1.8, fly("left:collar", np.array([-60.0, 0, 0])), hold=0.8)
    sc.step("L.3", "Camera Module 3 Wide on the ring's axis: the side view of nozzle and plate, which shows whether "
            "the stream lands on the plate or on the upper sonotrode (the 6 October failure).", 2.2,
            seq(ghost("left:collar", 1.0, 0.3, 0.0, 0.3), fly("left:cam", np.array([-140.0, 0, 0]), 0.15, 1.0)),
            hold=1.0)
    sc.step("L.4", "Pi 5 behind the camera, then the 5 in Touch Display 2 (DSI) facing the operator, and the face "
            "plate.", 2.8, seq(ghost("left:collar", 0.3, 1.0, 0.0, 0.3), fly("left:pi", np.array([-150.0, 0, 0]), 0.0, 0.45),
                               fly("left:display", np.array([-150.0, 0, 0]), 0.3, 0.75),
                               fly("left:face", np.array([-150.0, 0, 0]), 0.55, 1.0)), hold=1.0)
    sc.step("L.5", "Slide the collar over the ring and clamp it with one M4 screw. It clears the stack by about 60 mm "
            "and the door's hinge and knobs, so it can stay on when the door opens.", 2.8,
            move("left:unit", np.array([-BENCH_L, 0.0, 0.0])), cam_to=LEFT_SEAT, hold=1.5)

    # --------------------------------------------------------------------------------------------- top
    upz = np.array([0.0, 0.0, 1.0])
    arm_dir = U.unit(np.array([0.0, -224.0]) - POST)
    arm3 = np.array([arm_dir[0], arm_dir[1], 0.0])
    sc.step("T.1", "Lid window. The camera has to look down the line from the melt through the window, about 66° "
            "below horizontal, so it hangs from a swing arm. First a switchable magnetic base on the blue frame's "
            "top (painted steel).", 2.5, fly("top:base", upz * 160), cam_to=TOP_BUILD, hold=1.0)
    sc.step("T.2", "A 5/8 in steel post, tapped M8 at one end, screwed into the base.", 2.0,
            fly("top:post", upz * 260), hold=0.8)
    sc.step("T.3", "Detent collar (orange) clamped to the post with an M4 screw, its 'working' dimple under the "
            "camera's position; the hub drops on above it, with an M6 ball plunger, then a shaft collar.", 2.8,
            seq(fly("top:collar", upz * 120, 0.0, 0.5), fly("top:hub", upz * 140, 0.4, 1.0)), hold=1.0)
    sc.step("T.4", "A 2020 extrusion (about 470 mm, cut from 500) slides into the hub's socket; an M5 screw into a "
            "drop-in T-nut holds it.", 2.4, fly("top:arm", arm3 * 300), cam_to=TOP_ARM, hold=0.8)
    sc.step("T.5", "Camera pod: HQ Camera (C/CS) with a 16 mm lens, hot mirror and variable ND, on its saddle on the "
            "extrusion. ASA or PA6-CF, since it is above the furnace.", 2.4, fly("top:pod", arm3 * 160), hold=0.8)
    sc.step("T.6", "Display box on the arm's tip: Pi 5 and a 2.8 in DSI display, tilted 30° down at the operator.",
            2.2, fly("top:box", arm3 * 160), hold=0.8)

    def sight_on(u):
        sc.alpha["sight"] = S.window(u, 0.0, 0.6)
    sc.step("T.7", "The camera sits on the line from the melt through the lid window (red), about 250 mm from the "
            "glass and in front of the lid's edge, out of most of the heat rising off it.", 2.0, sight_on,
            labels=[lab("lid window", win, 0.03, 0.55)], hold=1.5)
    sc.step("T.8", "To load the crucible, swing the arm 90° to its 'parked' dimple, clear of the lid, and open the lid.",
            4.0, seq(lambda u: sc.alpha.__setitem__("sight", 1 - S.window(u, 0.0, 0.15)), swing(0, PARK, 0.0, 0.45),
                     lid(0, 110, 0.5, 1.0)), cam_to=TOP_LID, hold=1.2)
    sc.step("T.9", "Close the lid and swing the arm back: the plunger clicks into the 'working' dimple, and the camera "
            "is back on the same line.", 4.0,
            seq(lid(110, 0, 0.0, 0.45), swing(PARK, 0, 0.5, 0.95),
                lambda u: sc.alpha.__setitem__("sight", S.window(u, 0.9, 1.0))), cam_to=TOP_ARM, hold=1.2)

    # ------------------------------------------------------------------------------------------- end
    sc.step("", "All three on the machine: about 750 g of PETG and ASA, and $1,217.61 of parts at 7 October prices. "
            "Nothing is printed yet; every machine dimension is a frame estimate until it is measured.", 3.0, None,
            cam_to=INTRO, hold=2.5)
    sc.save()


if __name__ == "__main__":
    main()
