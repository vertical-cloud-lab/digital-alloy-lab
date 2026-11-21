"""MiR250 tip-over and slide margins for the forces the tending jobs apply (byu-vcl PR 318's alloy_atomize.stability(), ported in
ops.stability(): MiR250 97 kg, control box 12 kg, cabinet 25 kg, 131 kg ballast plate, the UR12e's links at their IK pose, the
gripper and tool at the flange, the payload at the TCP; support rectangle +-325 x +-225 mm about the MiR's centre (estimate, as PR
318); drive wheels carry half the weight at mu 0.6). For each job's largest force: the force that would tip or slide the base, and
the factor over the job's force. Writes analysis/out/robot/tipover.json.

Run: python desktop-lpbf/analysis/robot/tipover.py
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cell as C  # noqa: E402
import ops as O  # noqa: E402

CASES = [  # job, MiR arm x, TCP (machine frame, mm), approach, force on the machine (N), payload (kg), tool kg
    ("guard door slide", 450.0, (-50.0, -318.5, 105.0), (0, 1, 0), (30.0, 0, 0), 0.0, O.GRIPPER_KG),
    ("chamber door pull to 20 deg", -450.0, (0.0, -170.0, 90.0), (0, 1, 0), (0, -15.0, 0), 0.0, O.GRIPPER_KG),
    ("drawer pull", 0.0, (0.0, -260.0, 128.0), (0, 1, 0), (0, -20.0, 0), 0.0, O.GRIPPER_KG),
    ("reservoir pull off the dock", -390.0, (-90.0, -80.0, 252.0), (0, 1, 0), (0, -40.0, 0), 0.37, O.GRIPPER_KG + 0.15),
    ("blade cartridge pull", 0.0, (0.0, -68.0, 22.0), (0, 1, 0), (0, -40.0, 0), 0.15, O.GRIPPER_KG + 0.18),
    ("module out of its port (O-ring 132 N less 26 N weight)", 0.0, (0.0, -46.0, -105.0), (0, 0.766, -0.643), (0, 0, -106.0), 2.7, O.GRIPPER_KG),
    ("module into its port (132 N plus 26 N)", 0.0, (0.0, -46.0, -145.0), (0, 0.766, -0.643), (0, 0, 158.0), 2.7, O.GRIPPER_KG),
    ("module carried at the guard's front (no force)", 0.0, (0.0, -376.0, -101.0), (0, 0.766, -0.643), (0, 0, 0), 2.7, O.GRIPPER_KG),
]


class _J:
    pass


def main():
    out = []
    for name, ax, p, a, F, kg, tool in CASES:
        arm = C.Arm(base=(ax, C.ARM_Y, C.AMR_TOP))
        R = C.frame(a, (1, 0, 0))
        sols = arm.ik_all(C.Tm(R, p), np.radians([-90, -100, 120, -110, -90, 0]))
        if not sols:
            out.append(dict(case=name, error="no IK"))
            continue
        j = _J()
        j.arm, j.arm_x, j.tool_kg = arm, ax, tool
        best = None
        for q in sols:            # the branch that is worst for stability (conservative)
            st = O.stability(j, q, np.asarray(F, float), kg)
            tau = C.static_torques(arm, q, F_world=-np.asarray(F, float), payload_kg=kg, tool_kg=tool)
            pct = float(np.max(np.abs(tau) / np.array(C.UR12E["tau_lim"])) * 100)
            cap = C.max_force(arm, q, np.asarray(F, float) if np.linalg.norm(F) > 0 else (0, 0, 1.0), payload_kg=kg, tool_kg=tool)
            row = dict(case=name, arm_x=ax, force_N=list(F), payload_kg=kg, branches=len(sols), tips_at_N=st["tips_at_N"],
                       tips_about=st["tips_about"], slides_at_N=st["slides_at_N"], factor=st["factor"], cog_margin_mm=st["cog_margin_mm"],
                       mass_kg=st["mass_kg"], peak_torque_pct=round(pct, 1), arm_force_capacity_N=round(cap, 0))
            if best is None or (row["factor"] or 1e9) < (best["factor"] or 1e9):
                best = row
        out.append(best)
        print(best)
    (HERE.parent / "out" / "robot" / "tipover.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
