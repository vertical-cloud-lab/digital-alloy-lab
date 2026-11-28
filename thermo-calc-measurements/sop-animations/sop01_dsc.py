"""SOP 01 (DSC/DTA melting and freezing of atomized powder, #262): an animated walk through every step of
``../sops/01-dsc-solidification.md`` on a modelled bench: the micro riffle splitter, the microbalance, the STA with its
argon and vacuum, the operator, and the data each step produces (synthetic examples from ``../analysis/``).

    python sop01_dsc.py sop01_c1          # one chapter -> out/mp4/sop01_c1.mp4 (PREVIEW=1: a contact sheet in /tmp)
    python sop01_dsc.py join              # out/mp4/sop01.mp4 + out/sop01.json, the step sheet and the preview GIF

Chapters: c1 samples (riffle split, weighing, the record, the chip); c2 equipment and set-up (gas, crucibles, loading,
pump-down and purge); c3 calibration (standards, tau); c4 the program (the run, inside the furnace, rates, baseline,
time); c5 after the run and the analysis; c6 acceptance, the ESPEI export and the open questions.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

import stage as S
from stage import R, T

import audit
import models_dsc as M
import sop01_lib as L
import sop01_panels as P

BH = S.BENCH_H
TITLE = "SOP 01 · DSC melting and freezing of atomized powder"
CHAPTERS = ["sop01_c1", "sop01_c2", "sop01_c3", "sop01_c4", "sop01_c5", "sop01_c6"]
PANEL_R = (0.585, 0.085, 0.40)            # a data panel at the right
PANEL_L = (0.015, 0.085, 0.40)            # ... or the left
ALLOW = [("person*", "jar*"), ("person*", "tweezers*"), ("person*", "spatula*"), ("person*", "riffle_splitter:pan*"),
         ("person*", "bottle*"), ("person*", "microbalance:door*"), ("person*", "dsc_sta:*"), ("tweezers*", "cru*"),
         ("tweezers*", "chip*"), ("spatula*", "cru*"), ("spatula*", "riffle_splitter:*"), ("cru*", "microbalance:*"),
         ("cru*", "dsc_sta:*"), ("cru*", "tray*"), ("jar*", "riffle_splitter:*")]


def ease(u):
    return S.ease(u)


def cam(target, dist, az, el):
    return S.look(target, dist, az, el)


def new(name, sub):
    sc = S.SOPScene(name, f"{TITLE}: {sub}")
    return sc


def finish(sc, au):
    sc.save()
    au.save()


# ================================================================================================ chapter 1: samples
def c1():
    sc = new("sop01_c1", "samples")
    lab = L.Lab(sc)
    op = lab.op
    au = audit.Audit(sc, allow=ALLOW)
    rif = lab.rig["riffle"]
    bal = lab.rig["bal"]
    sc.card(TITLE, ["Checks: liquidus, solidus, incipient melting, freezing range, fs(T), latent heat",
                    "against Thermo-Calc and pycalphad (equilibrium and Scheil)",
                    "Draft SOP: nothing here has been run on our instrument yet"],
            seconds=4.0, label="SOP 01",
            note="Data panels are synthetic examples made with ../analysis/dsc_solidification.py and espei_export.py.")
    # the overview, backed off, then in on the splitter
    sc.cam = cam((-200, 0, BH + 250), 4600, -18, 20)
    sta = lab.rig["sta"]
    sc.step("Overview", "The DSC bench, left to right | splitter, microbalance, STA, PC, argon and pump", 4.0,
            None, hold=1.0,
            labels=[("micro riffle splitter", rif.world((0, 0, 150)), (0.10, 0.25)),
                    ("microbalance", bal.world(M.BAL_POINTS["top"]), (0.30, 0.18)),
                    ("STA (TG-DSC), to 1600 C", sta.world(M.STA_POINTS["furnace_top"]), (0.55, 0.12)),
                    ("Ar >= 99.999 %", lab.rig["gas"].world((0, 0, 1300)), (0.90, 0.22)),
                    ("vacuum pump", lab.rig["pump"].world((0, 0, 220)), (0.88, 0.70))])
    # ---- riffle splitting
    jar = "jar"
    jx, jy = L.JAR
    grip = np.array([L.JAR_D / 2 + 12.0, 0.0, 40.0])             # the right hand on the jar's right side

    def jar_pose(u):
        """the jar from the bench, up over the hopper, tipped to pour (u 0-1)."""
        hop = rif.world(M.RIFFLE_POINTS["hopper_rim"])
        a = T((jx, jy, BH))
        lift = T((jx, jy, BH + 120))
        over = T((hop[0] + 45, hop[1] - 10, hop[2] + 40))
        if u < 0.35:
            return S.blend(a, lift, ease(u / 0.35))
        if u < 0.7:
            return S.blend(lift, over, ease((u - 0.35) / 0.35))
        k = ease((u - 0.7) / 0.3)
        return over @ R((0, 1, 0), -105 * k, (0, 0, L.JAR_H))

    def hand_on_jar(u):
        return (jar_pose(u) @ np.r_[grip, 1.0])[:3]

    lid0 = T((jx, jy, BH + L.JAR_H))
    sc.cam_to = None
    sc.step("Samples", "Take a riffle-split sub-sample | not a scoop off the top", 3.0,
            S.together(op.reach("r", [op.p.rest_hand("r"), hand_on_jar(0)], lean=12.0,
                                look=(jx, jy, BH + 60))),
            hold=0.6, cam_to=cam((L.RIF[0] + 80, L.RIF[1], BH + 120), 1300, -28, 22),
            labels=[("Humboldt H-3971C micro riffle splitter", rif.world((57, 0, 150)), (0.78, 0.20)),
                    ("16 chutes, 3.2 mm", rif.world((20, -32, 84)), (0.80, 0.52)),
                    ("20-63 um sieve cut", (jx, jy - 30, BH + 40), (0.20, 0.62))])

    def pour(u):
        sc.gmat[jar] = jar_pose(u)
        op.reach("r", lambda v: hand_on_jar(u), lean=14.0, look=rif.world((0, 0, 150)))(1.0)
        rif.set(feed=min(1.0, max(0.0, (u - 0.78) / 0.15)))
    sc.step("Samples", "Take a riffle-split sub-sample | not a scoop off the top", 4.0, pour, hold=0.3)
    sc.step("Samples", "Half runs to each pan through alternate chutes", 3.5,
            rif.move({"feed": (1.0, 0.0), "stream": (0.0, 1.0), "split_l": (0.0, 1.0), "split_r": (0.0, 1.0)}),
            hold=0.5, cam_to=cam((L.RIF[0], L.RIF[1], BH + 70), 700, -35, 18))
    sc.step("Samples", "Repeat on one half, down to about 1 g", 3.5,
            S.together(rif.move({"stream": (1.0, 0.0)}), lambda u: (sc.gmat.__setitem__(jar, jar_pose(1 - u)),
                                                                     op.reach("r", lambda v: hand_on_jar(1 - u))(1.0))),
            hold=1.0)
    op.set(hands={"r": None}, lean=0.0)
    sc.save()
    au.save()


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "sop01_c1"
    if which == "join":
        dst = S.join("sop01", CHAPTERS)
        print(dst, S.contact_sheet("sop01"), S.preview_gif("sop01"))
        return
    {"sop01_c1": c1}[which]()


if __name__ == "__main__":
    main()
