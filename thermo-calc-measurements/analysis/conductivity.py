#!/usr/bin/env python3
"""Electrical conductivity (eddy current, %IACS, or four-point probe) -> resistivity, thermal
conductivity, and the comparison with Thermo-Calc's electrical-resistivity output.

- %IACS <-> resistivity: 100 % IACS is 1.7241 microohm-cm (58.0 MS/m) at 20 C, so
  rho [microohm-cm] = 172.41 / %IACS.
- Temperature: measure at 20 +/- 1 C, or correct with a slope you supply (dRho/dT, microohm-cm/K).
  Eddy-current meters usually compensate internally; record whether that was on.
- Thermal conductivity from electrical (Wiedemann-Franz): k = L0 T / rho, with the Sommerfeld
  value L0 = 2.443e-8 W ohm K^-2. The lattice (phonon) part is not included, so alloys deviate.
  The Smith-Palmer form k = A * L0 T / rho + B fixes that with two constants. Fit A and B once
  on a few alloys whose k you measured by laser flash (k = alpha rho cp), then use the cheap
  eddy-current reading for the rest (``fit_smith_palmer``). No published constants are built in.
- Four-point probe on a thin flat sample (thickness t << probe spacing s, large sample):
  rho = (pi / ln 2) * t * V / I (geometry corrections for finite samples are not applied).
- Aging and solute tracking: resistivity is additive over solute in solution (Matthiessen), so
  the drop in resistivity during aging tracks solute leaving solution. ``aging_fraction`` turns
  a resistivity series into a fraction transformed, f = (rho_0 - rho(t)) / (rho_0 - rho_inf).

CLI:
    python conductivity.py iacs 34.5 --T 23.0 --slope 0.0114
    python conductivity.py wf 34.5 --T-K 293.15
    python conductivity.py --demo
"""
from __future__ import annotations

import argparse
import json
import math

import numpy as np

IACS_RHO_UOHM_CM = 1.7241     # 100 % IACS at 20 C
L0 = 2.443e-8                  # W ohm K^-2, Sommerfeld value pi^2/3 (k_B/e)^2


def iacs_to_resistivity(iacs_pct: float) -> float:
    """microohm-cm"""
    return 100.0 * IACS_RHO_UOHM_CM / iacs_pct


def resistivity_to_iacs(rho_uohm_cm: float) -> float:
    return 100.0 * IACS_RHO_UOHM_CM / rho_uohm_cm


def to_20C(rho_uohm_cm: float, T_C: float, slope_uohm_cm_per_K: float) -> float:
    """Matthiessen-style correction: only the temperature-dependent part shifts."""
    return rho_uohm_cm - slope_uohm_cm_per_K * (T_C - 20.0)


def wiedemann_franz_k(rho_uohm_cm: float, T_K: float = 293.15, A: float = 1.0, B: float = 0.0) -> float:
    """Thermal conductivity, W/m/K. A = 1, B = 0 is plain Wiedemann-Franz."""
    rho_ohm_m = rho_uohm_cm * 1e-8
    return A * L0 * T_K / rho_ohm_m + B


def fit_smith_palmer(rho_uohm_cm, k_measured, T_K=293.15):
    """Least-squares A, B in k = A L0 T / rho + B from paired measurements."""
    x = L0 * T_K / (np.asarray(rho_uohm_cm, float) * 1e-8)
    A, B = np.polyfit(x, np.asarray(k_measured, float), 1)
    return float(A), float(B)


def four_point_probe_thin(V, I, t_m):
    """rho (microohm-cm) for a thin, large sample: (pi/ln2) t V/I."""
    return math.pi / math.log(2) * t_m * V / I * 1e8


def aging_fraction(rho_series, rho_0=None, rho_inf=None):
    r = np.asarray(rho_series, float)
    r0 = r[0] if rho_0 is None else rho_0
    rinf = r[-1] if rho_inf is None else rho_inf
    return (r0 - r) / (r0 - rinf)


def demo():
    out = {}
    out["iacs_100_rho"] = iacs_to_resistivity(100.0)
    rho = iacs_to_resistivity(34.5)
    out["rho_34.5_IACS"] = rho
    out["k_WF_34.5_IACS"] = wiedemann_franz_k(rho)
    # synthetic Smith-Palmer recovery
    rhos = np.array([3.5, 4.2, 5.0, 6.1])
    k = 0.92 * L0 * 293.15 / (rhos * 1e-8) + 9.0
    out["smith_palmer_fit"] = fit_smith_palmer(rhos, k)
    print(json.dumps(out, indent=2))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--demo", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    a1 = sub.add_parser("iacs")
    a1.add_argument("value", type=float)
    a1.add_argument("--T", type=float, help="measurement temperature, C")
    a1.add_argument("--slope", type=float, help="d rho/dT, microohm-cm/K, for correction to 20 C")
    a2 = sub.add_parser("wf")
    a2.add_argument("value", type=float, help="%%IACS")
    a2.add_argument("--T-K", type=float, default=293.15)
    a2.add_argument("--A", type=float, default=1.0)
    a2.add_argument("--B", type=float, default=0.0)
    a = p.parse_args(argv)
    if a.demo:
        demo()
    elif a.cmd == "iacs":
        rho = iacs_to_resistivity(a.value)
        res = {"rho_uohm_cm": rho}
        if a.T is not None and a.slope is not None:
            res["rho_20C_uohm_cm"] = to_20C(rho, a.T, a.slope)
        print(json.dumps(res, indent=2))
    elif a.cmd == "wf":
        rho = iacs_to_resistivity(a.value)
        print(json.dumps({"rho_uohm_cm": rho, "k_W_mK": wiedemann_franz_k(rho, a.T_K, a.A, a.B)}, indent=2))
    else:
        p.print_help()


if __name__ == "__main__":
    main()
