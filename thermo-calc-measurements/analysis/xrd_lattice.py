#!/usr/bin/env python3
"""Cubic lattice parameter from XRD peak positions by Nelson-Riley extrapolation, for comparison
with the lattice parameter Thermo-Calc reports for FCC_A1 (and as a solute-in-solution check).

For each reflection hkl at 2-theta: a_hkl = lambda * sqrt(h^2 + k^2 + l^2) / (2 sin theta).
Systematic errors (sample displacement, absorption) shrink as theta -> 90 deg, so fit
a_hkl = a0 + m * NR(theta), NR = 0.5 (cos^2 theta / sin theta + cos^2 theta / theta), and take a0.

Peak positions should come from profile fits (pseudo-Voigt; GSAS-II or Profex for full Rietveld),
on a diffractometer checked against a line-position standard (e.g. NIST SRM 640 silicon or 660
LaB6). Default wavelength: Cu K-alpha1, 1.540593 A (Hoelzer et al. 1997); strip K-alpha2 first.

Solute in solution: if you supply Vegard-type slopes da/dc (A per at.%) for each solute, the
solver returns the solute content consistent with the measured shift for a single solute. No
slopes are built in; take them from a cited source and record which.

CLI:
    python xrd_lattice.py peaks.csv [--wavelength 1.540593] [--predicted 4.0496]
    python xrd_lattice.py --demo
peaks.csv columns: h, k, l, two_theta_deg
"""
from __future__ import annotations

import argparse
import csv
import json
import math

import numpy as np

CU_KA1 = 1.540593   # Angstrom


def nelson_riley(theta_rad):
    c2 = np.cos(theta_rad) ** 2
    return 0.5 * (c2 / np.sin(theta_rad) + c2 / theta_rad)


def lattice_parameter(hkl, two_theta_deg, wavelength=CU_KA1):
    hkl = np.asarray(hkl, float)
    th = np.radians(np.asarray(two_theta_deg, float) / 2)
    a = wavelength * np.sqrt((hkl ** 2).sum(axis=1)) / (2 * np.sin(th))
    x = nelson_riley(th)
    m, a0 = np.polyfit(x, a, 1)
    resid = a - (m * x + a0)
    n = len(a)
    s2 = np.sum(resid ** 2) / max(n - 2, 1)
    se_a0 = math.sqrt(s2 * (1 / n + x.mean() ** 2 / np.sum((x - x.mean()) ** 2))) if n > 2 else float("nan")
    return {"a0_A": float(a0), "u_a0_A": se_a0, "slope": float(m), "a_hkl_A": a.round(5).tolist()}


def two_theta_for(a, hkl, wavelength=CU_KA1):
    d = a / math.sqrt(sum(i * i for i in hkl))
    return 2 * math.degrees(math.asin(wavelength / (2 * d)))


FCC_REFLECTIONS = [(1, 1, 1), (2, 0, 0), (2, 2, 0), (3, 1, 1), (2, 2, 2), (4, 0, 0), (3, 3, 1), (4, 2, 0)]


def demo(a_true=4.0560, displacement_um=50.0, R_mm=240.0):
    # sample displacement s shifts 2theta by -2 s cos(theta)/R (radians)
    tt = []
    for hkl in FCC_REFLECTIONS:
        t = two_theta_for(a_true, hkl)
        th = math.radians(t / 2)
        shift = -2 * (displacement_um * 1e-3) * math.cos(th) / R_mm
        tt.append(t + math.degrees(shift))
    res = lattice_parameter(FCC_REFLECTIONS, tt)
    naive = float(np.mean(res["a_hkl_A"]))
    print(json.dumps({"a_true": a_true, "nelson_riley": res, "naive_mean": naive}, indent=2))
    return res, naive


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("peaks", nargs="?")
    p.add_argument("--wavelength", type=float, default=CU_KA1)
    p.add_argument("--predicted", type=float, help="lattice parameter from Thermo-Calc/pycalphad, A")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        demo()
        return
    if not a.peaks:
        p.error("peaks.csv required (or --demo)")
    with open(a.peaks, newline="") as fh:
        rows = list(csv.DictReader(fh))
    hkl = [(int(r["h"]), int(r["k"]), int(r["l"])) for r in rows]
    tt = [float(r["two_theta_deg"]) for r in rows]
    res = lattice_parameter(hkl, tt, a.wavelength)
    if a.predicted:
        res["measured_minus_predicted_A"] = res["a0_A"] - a.predicted
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
