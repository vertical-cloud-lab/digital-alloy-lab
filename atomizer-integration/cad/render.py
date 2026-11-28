#!/usr/bin/env python3
"""Stills of the #151 integration hardware on the rePowder model, and what each camera sees.

    xvfb-run -a -s "-screen 0 1920x1080x24" python render.py
        # -> ../renders/overview.png, hmi_closeup.png, tap_closeup.png (1600 x 900),
        #    ../renders/hmi_camera_view.png, panel_camera_view.png (1280 x 720, through each camera's lens)
"""
from __future__ import annotations

import json

import numpy as np

import common as C
from common import I, M, S

OUT = C.HERE.parent / "renders"
SIZE = (1600, 900)


def scene(name, title):
    sc = S.Scene(name, title, size=SIZE, gif=False, mp4=False)
    C.load(sc)
    return sc


def lab(text, xyz, fx, fy):
    return (text, tuple(float(c) for c in xyz), (fx, fy), 1.0)


def save(sc, name):
    OUT.mkdir(exist_ok=True)
    sc.snap().convert("RGB").save(OUT / f"{name}.png", optimize=True)
    sc.pl.close()
    print("wrote", name)


def overview():
    sc = scene("overview", "rePowder data capture (#151): everything fitted")
    sc.gmat["door_r"] = C.hinge_open(100)
    sc.cam = C.cam_at((520, 230, 1180), (1900, -2050, 820))
    sc.caption = ("Steps 1-2 (cameras on the HMI and on the GU 500 panel, behind anti-glare film) need nothing from "
                  "AMAZEMET. Steps 3-4 (the switch on the HMI's Ethernet, the STG1 power tap) wait for their OK. "
                  "Interior positions are approximate.")
    sc.labels = [lab("1  HMI camera: CM3 Wide on a super clamp\n   + arm, flip shutter, film on the screen",
                     I.hmi_pt(I.HMI_CAM_C_L), 0.97, 0.10),
                 lab("2  GU 500 camera: CM3 on a magnetic base,\n   film on the LCD", I.PANEL_CAM_C, 0.03, 0.18),
                 lab("panel camera Pi (on magnets)", (485, 236, 1628), 0.03, 0.06),
                 lab("3  switch + HMI camera Pi on the HMI's back", I.hmi_pt((20, 30, -90)), 0.97, 0.47),
                 lab("4  STG1 tap: DB15 pass-through breakout", I.X3_C + np.array([15, 0, -50]), 0.97, 0.62),
                 lab("   isolated ADC box on the DIN rail", (I.ADC_BOX["x"][1], 307, I.ADC_BOX["z"][1]), 0.97, 0.74),
                 lab("SONICTECH STG1", (I.STG1_BOX["x"][1], 520, 1460), 0.03, 0.36),
                 lab("USB from the ADC box to the HMI camera Pi", (I.GLAND[0] + 40, 240, I.FZ1 + 20), 0.03, 0.27)]
    save(sc, "overview")


def hmi_closeup():
    sc = scene("hmi_closeup", "Step 1: HMI camera")
    for g in ("panelcam_base", "panelcam_arm", "panelcam_head", "panelcam_shutter", "panelcam_cable", "fov_panel"):
        sc.show(S.names_of(sc, g), 0.0)
    sc.cam = C.HMI_SIDE
    sc.caption = ("Camera Module 3 Wide 260 mm from the screen, 50° above its normal, on a super clamp + magic arm on the "
                  "HMI's top edge, so it swings with the HMI. Yellow: the screen's active area, 86° × 36° of the "
                  "lens's 102° × 67°.")
    sc.labels = [lab("printed case + flip shutter", I.hmi_pt(I.HMI_CAM_C_L), 0.03, 0.22),
                 lab("magic arm", I.hmi_pt((0, -105, 281)), 0.03, 0.10),
                 lab("super clamp, rubber pads", I.hmi_pt((0, 0, 145)), 0.97, 0.20),
                 lab("matte anti-glare film", I.hmi_pt((-120, -21, -40)), 0.03, 0.62),
                 lab("ribbon to the Pi on the back", I.hmi_pt((0, -60, 158)), 0.97, 0.36)]
    save(sc, "hmi_closeup")


def tap_closeup():
    sc = scene("tap_closeup", "Step 4: STG1 power tap (right-hand side door open)")
    sc.gmat["door_r"] = C.hinge_open(100)
    for n in S.names_of(sc, "adc_lid"):
        sc.base_alpha[n] = 0.25
    sc.cam = C.cam_at((395, 400, 1140), (720, -300, 260))
    sc.caption = ("The breakout passes all 15 pins of X3 straight through to the existing cable, and its terminals give "
                  "the power-out and 0 V lines. The box holds the divider, ADS1115, MCP2221A and USB isolator (lid "
                  "shown see-through). Positions inside the door are approximate.")
    sc.labels = [lab("STG1 (SONICTECH, 40 kHz)", (I.STG1_BOX["x"][1], 500, 1420), 0.97, 0.12),
                 lab("X3 (DB15) with the pass-through breakout", I.X3_C + np.array([12, 0, -40]), 0.97, 0.32),
                 lab("existing X3 cable, now in the breakout", I.X3_C + np.array([0, 0, -150]), 0.97, 0.50),
                 lab("power out + 0 V", (I.X3_C[0] + 50, 382, 1148), 0.03, 0.30),
                 lab("isolated ADC box", (I.ADC_BOX["x"][1], 290, I.ADC_BOX["z"][1]), 0.03, 0.55),
                 lab("PLC (model unknown)", (I.BACK_X + 78, 470, 1000), 0.97, 0.68),
                 lab("USB out", (I.ADC_BOX["x"][1] + 20, I.ADC_BOX["y"][0] + 10, I.ADC_BOX["z"][0] - 30), 0.03, 0.76)]
    save(sc, "tap_closeup")


def camera_view(name, title, eye, d, fov, hide, caption):
    """Render through a camera's lens: its position, axis and vertical field of view, at its 16:9 frame."""
    sc = S.Scene(name, title, size=(1280, 720), gif=False, mp4=False)
    C.load(sc)
    for g in hide:
        sc.show(S.names_of(sc, g), 0.0)
    ex, ey, ez = I.cam_axes(d)
    sc.cam = [tuple(eye), tuple(eye + ey * 300.0), tuple(ez)]
    sc.view_angle = fov[1]
    sc.caption = caption
    save(sc, name)


if __name__ == "__main__":
    overview()
    hmi_closeup()
    tap_closeup()
    f = I.framing()
    camera_view("hmi_camera_view", "Through the HMI camera (CM3 Wide)", I.hmi_pt(I.HMI_CAM_C_L + I.HMI_CAM_DIR_L * 2),
                I.hmi_vec(I.HMI_CAM_DIR_L), I.WIDE_FOV,
                ("hmicam_head", "hmicam_shutter", "hmicam_arm", "fov_hmi", "fov_panel"),
                f"From 260 mm and 50° above: the screen spans {f['hmi_screen_wide']['h_used']:.0f}° × "
                f"{f['hmi_screen_wide']['v_used']:.0f}° of the 102° × 67° frame. Software straightens the keystone "
                "before reading numbers.")
    camera_view("panel_camera_view", "Through the GU 500 camera (CM3)", I.PANEL_CAM_C + I.PANEL_CAM_DIR * 2,
                I.PANEL_CAM_DIR, I.STD_FOV,
                ("panelcam_head", "panelcam_shutter", "panelcam_arm", "fov_hmi", "fov_panel"),
                f"From 200 mm and 30° above: the LCD spans {f['gu500_lcd_std']['h_used']:.0f}° × "
                f"{f['gu500_lcd_std']['v_used']:.0f}° of the 66° × 41° frame; the keypad's top rows are in view too.")
    (OUT / "framing.json").write_text(json.dumps(f, indent=1) + "\n")
    print("wrote framing.json")
