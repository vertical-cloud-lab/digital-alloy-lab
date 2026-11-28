"""FT-1's laser-hazard numbers for the day-0 request to BYU's laser safety officer (issue #260, PR 294, round 3).

The method and the MPE values are PR 266's (`desktop-lpbf/safety_calcs.py` section 1: ANSI Z136.1 as tabulated in the
NIU laser safety manual, which cites Z136.1-2000). Only the inputs change, to the fast-track machine's: the used IPG
YLR-400-SM-EOS (400 W, not 500 W), the LINOS f = 254 mm objective (not 160 mm) and the 5 mm collimated beam. These are
the inputs an LSO's own hazard evaluation needs; the LSO's numbers decide, not these.

    python desktop-lpbf/fast-track/day0/lso_numbers.py      # writes day0/lso-numbers.md
"""
from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PI = math.pi

# Inputs (sources in the README of the study and in parts.csv)
LAM = 1070e-9        # m, IPG YLR series
P = 400.0            # W, YLR-400-SM-EOS nominal CW output (parts.csv L1)
M2 = 1.1             # IPG single-mode, M^2 < 1.1
D_COL = 5e-3         # m, IPG's standard collimated beam (README section 3.2; 73-76 um spot at f = 254 mm)
F_FT = 0.254         # m, LINOS F-Theta-Ronar 4401-288-000-20
BARE_DIV = 0.140     # rad full angle, bare fibre output, as PR 266 assumed for an IPG QBH (only if the collimator is off)
R_SPEC = 0.9         # specular reflectance of bare Al at 1070 nm (assumed, as PR 266 and process/README.md)

# MPE at 1070 nm, t >= 10 s (PR 266 safety_calcs.py, from the NIU manual's Z136.1 tables)
CA, CC = 5.0, 1.0
MPE_EYE = 5.0e-3 * CC          # W/cm^2
MPE_SKIN = 0.2 * CA            # W/cm^2
A7 = PI * 0.35 ** 2            # cm^2, 7 mm pupil
AEL1 = MPE_EYE * A7            # W, Class 1 accessible emission ~ MPE x 7 mm pupil (derived)


def nohd(power, phi_full, a_cm=0.0):
    """Z136.1-style NOHD in m: (sqrt(4 P / (pi MPE)) - a) / phi, P in W, MPE in W/cm^2, a the exit diameter in cm."""
    return (math.sqrt(4 * power / (PI * MPE_EYE)) - a_cm) / phi_full / 100.0


def od(power_w):
    """Optical density for the power through a 7 mm pupil: OD = log10(H0 / MPE)."""
    return math.log10(power_w / A7 / MPE_EYE)


def main():
    w_in = D_COL / 2
    w0 = M2 * LAM * F_FT / (PI * w_in)
    zr = PI * w0 ** 2 / (M2 * LAM)
    th = w_in / F_FT
    phi_col = 4 * M2 * LAM / (PI * D_COL)
    rows = [
        ("MPE, eye, t >= 10 s", f"{MPE_EYE * 1e3:.1f} mW/cm²", "Z136.1 via the NIU manual (PR 266)"),
        ("MPE, skin, t >= 10 s", f"{MPE_SKIN:.1f} W/cm²", "same"),
        ("Class 1 accessible emission (MPE x 7 mm pupil)", f"{AEL1 * 1e3:.2f} mW", "derived"),
        ("Focused spot (1/e² diameter), Rayleigh range", f"{2 * w0 * 1e6:.0f} µm, {zr * 1e3:.1f} mm", "Gaussian, M² 1.1"),
        ("Peak irradiance at focus", f"{2 * P / (PI * w0 ** 2) / 1e4:.1e} W/cm²", "same"),
        ("NHZ, collimated 5 mm beam (head off or between collimator and head)",
         f"{nohd(P, phi_col, a_cm=0.5) / 1e3:.1f} km", f"divergence {phi_col * 1e3:.2f} mrad full"),
        ("NHZ, direct beam through the f-theta, from the focus", f"{nohd(P, 2 * th):.0f} m", f"{2 * th * 1e3:.1f} mrad full angle"),
        ("NHZ, specular off a bare Al plate (R 0.9)", f"{nohd(R_SPEC * P, 2 * th):.0f} m", "from the focus"),
        ("NHZ, bare fibre end (collimator off)", f"{nohd(P, BARE_DIV):.0f} m", "140 mrad full angle (PR 266's assumption)"),
    ]
    for rho in (0.1, 0.5):
        rows.append((f"NHZ, diffuse off powder (rho {rho})", f"{math.sqrt(rho * P / (PI * MPE_EYE)) / 100:.2f} m", "Lambertian, normal viewing"))
    for lab, pw in (("Eyewear OD, direct 400 W", P), ("Eyewear OD, specular 0.9 x 400 W", R_SPEC * P),
                    ("Eyewear OD, alignment at 40 W (10 %)", 40.0), ("Eyewear OD, alignment at 4 W (1 %)", 4.0)):
        rows.append((lab, f">= {od(pw):.1f}", "OD = log10(H0/MPE), 7 mm pupil"))
    rows.append(("Window or viewing-panel OD for Class 1 behind it, full 400 W", f">= {math.log10(P / AEL1):.1f}", "derived"))
    for t_ms, lab in ((1, "laser gate (12 µs) and wiring, 1 ms"), (20, "safety relay into the laser's interlock loop, 20 ms"),
                      (100, "a slow path, 100 ms")):
        rows.append((f"Energy on a stationary spot before the beam stops: {lab}", f"{P * t_ms / 1e3:.1f} J", "P x t"))
    lines = ["# FT-1 laser-hazard numbers for the LSO (`lso_numbers.py`)", "",
             f"Inputs: {P:.0f} W CW at {LAM * 1e9:.0f} nm, M² {M2}, {D_COL * 1e3:.0f} mm collimated beam, f = {F_FT * 1e3:.0f} mm. "
             "Method and MPE values: PR 266's `desktop-lpbf/safety_calcs.py` §1 (ANSI Z136.1 via the NIU manual). "
             "Estimates for the request; the LSO's evaluation decides.", "",
             "| Quantity | Value | Basis |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    (HERE / "lso-numbers.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
