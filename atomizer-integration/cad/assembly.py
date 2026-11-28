#!/usr/bin/env python3
"""Animated assembly of the #151 integration steps on the rePowder model: the HMI camera, the GU 500 panel camera,
the HMI's Ethernet and the STG1 power tap, in the order they would go on (least to most intrusive).

    xvfb-run -a -s "-screen 0 1920x1080x24" python assembly.py
        # -> ../renders/integration_steps.gif (800 x 450, 8 fps), integration_steps.json, integration_steps_still.png,
        #    ../renders/mp4/integration_steps.mp4 (1280 x 720, 15 fps)
    PREVIEW=1 xvfb-run -a -s "-screen 0 1920x1080x24" python assembly.py   # last frame of each step -> /tmp
"""
from __future__ import annotations

import numpy as np

import common as C
from common import I, M, S

S.OUT = C.HERE.parent / "renders"
S.GIF_FPS = 8        # scene.py's default is 10; at 8 the 79 s GIF stays under 5 MB


def main() -> None:
    sc = S.Scene("integration_steps", "rePowder data capture (#151): assembly")
    C.load(sc)

    def names(group):
        return S.names_of(sc, group)

    def hide(*groups):
        for g in groups:
            sc.show(names(g), 0.0)

    def fade(group, a0, a1, t0=0.0, t1=1.0):
        ns = names(group)
        return lambda u: sc.show(ns, a0 + (a1 - a0) * S.window(u, t0, t1))

    def fly(group, vec, t0=0.0, t1=1.0):
        ns, v = names(group), np.asarray(vec, float)

        def f(u):
            e = S.window(u, t0, t1)
            sc.show(ns, min(1.0, 4 * e) if e > 0 else 0.0)
            sc.gmat[group] = S.T(v * (1 - e))
        return f

    def ghost(group, a0, a1, t0=0.0, t1=1.0):
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

    def door(d0, d1, t0=0.0, t1=1.0):
        return lambda u: sc.gmat.__setitem__("door_r", C.hinge_open(d0 + (d1 - d0) * S.window(u, t0, t1)))

    def shutter(prefix, d0, d1, t0=0.0, t1=1.0):
        return lambda u: sc.gmat.__setitem__(prefix + "_shutter",
                                             C.shutter_pose(prefix, d0 + (d1 - d0) * S.window(u, t0, t1)))

    def plug(z0, z1, t0=0.0, t1=1.0):
        return lambda u: sc.gmat.__setitem__("x3_plug", S.T((0, 0, z0 + (z1 - z0) * S.window(u, t0, t1))))

    def lab(text, xyz, fx, fy):
        return (text, tuple(float(c) for c in xyz), (fx, fy))

    hv = I.hmi_vec
    # start: the machine as it is today; every new part waits off screen, the door is shut
    for g in ("film_hmi", "hmicam_clamp", "hmicam_arm", "hmicam_head", "hmicam_shutter", "hmicam_cable", "hmipi",
              "film_panel", "panelcam_base", "panelcam_arm", "panelcam_head", "panelcam_shutter", "panelcam_cable",
              "panelpi", "switch", "eth_moved", "patch_hmi", "patch_pi", "breakout", "wires", "adc", "adc_lid", "usb",
              "fov_hmi", "fov_panel"):
        hide(g)
    sc.cam = C.INTRO
    sc.step("0", "Getting settings and readings off the rePowder, in four add-ons from least to most intrusive. "
            "Steps 1 and 2 only watch screens, so they need nothing from AMAZEMET. Steps 3 and 4 connect to AMAZEMET's "
            "controls, so they wait for AMAZEMET's OK.", 3.2, None, hold=1.6,
            labels=[lab("HMI: Weintek cMT2166X, 15.6 in", I.hmi_pt((150, -20, 100)), 0.97, 0.18),
                    lab("GU 500 furnace panel", I.LCD_C, 0.97, 0.36),
                    lab("right-hand side door:\nPLC, STG1 ultrasonic generator", (C.I.FX1, 420, 1200), 0.97, 0.58),
                    lab("main switch", M.SWITCH_C, 0.03, 0.62)])

    # -------------------------------------------------------------------------------------- 1 HMI camera
    sc.step("1.1", "HMI camera. Clean the glass and lay a matte anti-glare film (15.6 in, 16:9, 344 × 194 mm) over the "
            "screen. Use plain matte film, not privacy film, which would black out a camera looking from above.",
            2.6, fly("film_hmi", hv((0, -70, 0))), cam_to=C.HMI_FRONT, hold=1.0,
            labels=[lab("matte anti-glare film", I.hmi_pt((-120, -21, -60)), 0.03, 0.70)])
    sc.step("1.2", "A super clamp on the HMI's own top edge, rubber pads on both jaws, nothing drilled. The camera then "
            "swings with the HMI and stays framed wherever the arm is turned.", 2.4,
            fly("hmicam_clamp", (0, 0, 120)), hold=1.0,
            labels=[lab("super clamp on the 28 mm top edge", I.hmi_pt((0, 0, 140)), 0.97, 0.30)])
    sc.step("1.3", "Articulating arm, then the printed case with a Camera Module 3 Wide (102° × 67°) about 260 mm from "
            "the screen and 50° above it. The whole screen fills 86° × 36° of the frame, and the camera is above the "
            "operator's line of sight.", 3.0,
            seq(fly("hmicam_arm", hv((0, -40, 120)), 0.0, 0.55), fly("hmicam_head", hv((0, -90, 120)), 0.35, 1.0),
                fly("hmicam_shutter", (0, 0, 0), 0.35, 1.0)), cam_to=C.HMI_SIDE, hold=1.0,
            labels=[lab("Camera Module 3 Wide,\nprinted case", I.hmi_pt(I.HMI_CAM_C_L), 0.03, 0.30)])
    sc.step("1.4", "Its flat cable runs over the top edge to the HMI camera Pi (the existing one), in a case on the "
            "HMI's back.", 2.6, seq(fly("hmipi", hv((0, 120, 0)), 0.0, 0.7), fade("hmicam_cable", 0, 1, 0.4, 1.0)),
            cam_to=C.HMI_BACK, hold=1.0,
            labels=[lab("HMI camera Pi", I.hmi_pt((92, 44, 60)), 0.97, 0.30)])
    sc.step("1.5", "What the camera has to see (yellow): the screen's corners are at most 43° left and right of its "
            "axis and 18° above and below, inside the Wide's 51° and 33.5°.", 2.4, fade("fov_hmi", 0, 1),
            cam_to=C.HMI_SIDE, hold=1.2)
    sc.step("1.6", "Before anyone types a password on the HMI, flip the shutter down. Flip it up afterwards. The "
            "stream itself can stay public.", 3.6,
            seq(fade("fov_hmi", 1, 0, 0.0, 0.2), shutter("hmicam", C.SHUTTER_OPEN, 0, 0.1, 0.45),
                shutter("hmicam", 0, C.SHUTTER_OPEN, 0.7, 1.0)), hold=1.0,
            labels=[lab("flip shutter", I.hmi_pt(I.HMI_CAM_C_L + I.HMI_CAM_DIR_L * 3), 0.03, 0.30)])

    # -------------------------------------------------------------------------------- 2 GU 500 panel camera
    sc.step("2.1", "Furnace panel camera. The GU 500's LCD gets a piece of the same film, cut a little larger than the "
            "display.", 2.4, fly("film_panel", (0, -60, 0)), cam_to=C.PANEL, hold=1.0,
            labels=[lab("film on the GU 500 LCD", I.LCD_C + np.array([40, -2, 0]), 0.97, 0.50)])
    sc.step("2.2", "The cabinet is painted steel, so a switchable magnetic base holds a short arm, with nothing "
            "drilled. A Camera Module 3 (66°) in the same printed case sits about 200 mm from the LCD, 30° above it.",
            3.0, seq(fly("panelcam_base", (0, -80, 0), 0.0, 0.4), fly("panelcam_arm", (0, -80, 40), 0.25, 0.7),
                     fly("panelcam_head", (0, -90, 60), 0.5, 1.0), fly("panelcam_shutter", (0, -90, 60), 0.5, 1.0)),
            hold=1.0, labels=[lab("magnetic base", (485, 136, 1528), 0.97, 0.22),
                              lab("Camera Module 3", I.PANEL_CAM_C, 0.03, 0.30)])
    sc.step("2.3", "The panel camera Pi (the existing one) sits on the cabinet's top on magnets. The LCD's corners fall "
            "within 17° and 8° of the camera's axis.", 2.6,
            seq(fly("panelpi", (0, 0, 120), 0.0, 0.6), fade("panelcam_cable", 0, 1, 0.4, 0.9),
                fade("fov_panel", 0, 1, 0.5, 1.0)), hold=1.2,
            labels=[lab("panel camera Pi", (485, 236, 1628), 0.97, 0.22)])

    # ------------------------------------------------------------------------------------- 3 HMI Ethernet
    sc.step("3.1", "HMI Ethernet, if AMAZEMET agrees. The HMI has one Ethernet port. If it is free, one patch cable "
            "from the Pi is enough. If it already goes to the PLC (likely), a 5-port switch goes on that link, on the "
            "HMI's back.", 3.0, seq(fade("fov_panel", 1, 0, 0.0, 0.2), fly("switch", hv((0, 120, 0)), 0.1, 0.9)),
            cam_to=C.HMI_BACK, hold=1.0,
            labels=[lab("existing HMI cable", I.hmi_pt((-150, 62, -92)), 0.03, 0.62),
                    lab("5-port switch, USB-C powered", I.hmi_pt((20, 35, -100)), 0.97, 0.66)])
    sc.step("3.2", "Move the HMI's cable to the switch, then patch the switch to the HMI and to the Pi. The Pi joins "
            "the HMI's subnet on its Ethernet port only. Its Wi-Fi stays on the lab network, and it routes nothing "
            "between the two.", 3.2,
            seq(fade("eth_old", 1, 0, 0.0, 0.35), fade("eth_moved", 0, 1, 0.25, 0.6), fade("patch_hmi", 0, 1, 0.5, 0.8),
                fade("patch_pi", 0, 1, 0.65, 1.0)), hold=1.0,
            labels=[lab("patch to the HMI", I.hmi_pt((-60, 40, -60)), 0.03, 0.40),
                    lab("patch to the Pi", I.hmi_pt((40, 50, -15)), 0.97, 0.40)])
    sc.step("3.3", "With a History-level password from AMAZEMET: VNC in view-only monitor mode (port 5900) gives a "
            "pixel-exact copy of the screen, and EasyWeb 2.0 or FTP exports the HMI's data, event and operation logs.",
            2.0, None, hold=2.4,
            labels=[lab("VNC :5900, monitor mode\nEasyWeb :80, FTP :21", I.hmi_pt((-30, 36, -90)), 0.97, 0.66)])

    # --------------------------------------------------------------------------------- 4 STG1 power tap
    sc.step("4.1", "STG1 power tap, if AMAZEMET agrees. Main switch off, then open the right-hand side door. The STG1 "
            "ultrasonic generator is at the top, with the PLC and terminals on DIN rails. Positions are approximate, "
            "from training video 1 at 9:58.", 3.4, door(0, 100, 0.25, 1.0), cam_to=C.DOOR, hold=1.2,
            labels=[lab("SONICTECH STG1 (40 kHz)", (I.STG1_BOX["x"][1], 510, 1440), 0.97, 0.22),
                    lab("PLC on DIN rail", (I.BACK_X + 78, 470, 1000), 0.97, 0.52)])
    drop = I.BREAKOUT_DROP
    sc.step("4.2", "Unplug the cable from the STG1's DB15 port (X3), fit the DB15 pass-through breakout, and plug the "
            "cable back into its other end. Every pin still goes straight through, so the PLC sees exactly what it "
            "did before.", 3.6,
            seq(plug(0, -drop - 70, 0.0, 0.3), fly("breakout", (0, 0, -90), 0.3, 0.65), plug(-drop - 70, -drop, 0.7, 1.0)),
            cam_to=C.TAP, hold=1.0,
            labels=[lab("X3, DB15", I.X3_C + np.array([0, -20, -3]), 0.03, 0.30),
                    lab("pass-through breakout", I.X3_C + np.array([12, 0, -45]), 0.97, 0.40)])
    sc.step("4.3", "Two wires from the breakout's power-out and 0 V terminals (pins per the STG1 manual) to the "
            "isolated ADC box, which clips on the DIN rail.", 3.0,
            seq(fly("adc", (60, 0, 0), 0.0, 0.6), fly("adc_lid", (0, 0, 0), 0.0, 0.6), fade("wires", 0, 1, 0.5, 1.0)),
            hold=1.0, labels=[lab("isolated ADC box", (I.ADC_BOX["x"][1], 307, I.ADC_BOX["z"][1]), 0.03, 0.62)])
    sc.step("4.4", "Inside the box: a 200 k / 100 k divider (0–10 V to 0–3.3 V), an ADS1115 16-bit ADC, an MCP2221A "
            "USB-to-I2C bridge and a USB isolator. The input side floats on the STG1's 0 V. The red line marks the "
            "isolation barrier.", 3.6, seq(ghost("adc_lid", 1.0, 0.2, 0.0, 0.3), ghost("adc_lid", 0.2, 1.0, 0.8, 1.0)),
            hold=0.8, labels=[lab("ADS1115 + divider", (I.ADC_BOX["x"][0] + 8, 336, 1000), 0.97, 0.36),
                              lab("USB isolator", (I.ADC_BOX["x"][0] + 8, 280, 1000), 0.03, 0.40)])
    sc.step("4.5", "A USB cable leaves the cabinet through an existing cable entry (AMAZEMET to say which) to the HMI "
            "camera Pi, which can then log ultrasonic power at any rate. Close the door.", 3.4,
            seq(fade("usb", 0, 1, 0.0, 0.45), door(100, 0, 0.55, 1.0)), cam_to=C.INTRO, hold=1.0,
            labels=[lab("USB to the HMI camera Pi", (I.GLAND[0] + 60, 230, I.FZ1 + 20), 0.97, 0.22)])

    # ------------------------------------------------------------------------------------------------ end
    sc.step("", "All four on the machine. Nothing is bought or printed yet, and AMAZEMET's positions are estimates. The "
            "three viewport camera units (front, left, top) are in PR #189, with their own assembly animation.", 2.0,
            None, hold=2.6, still=True,
            labels=[lab("HMI camera + film", I.hmi_pt(I.HMI_CAM_C_L), 0.97, 0.14),
                    lab("GU 500 camera + film", I.PANEL_CAM_C, 0.97, 0.32),
                    lab("switch + Pi on the HMI's back", I.hmi_pt((40, 40, -40)), 0.97, 0.50),
                    lab("STG1 tap (behind the door)", (I.FX1 + 4, 470, 1180), 0.97, 0.66)])
    sc.save()


if __name__ == "__main__":
    main()
