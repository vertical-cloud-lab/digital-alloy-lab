#!/usr/bin/env python3
"""Precipitation and transformation kinetics from cheap measurements, for checking TC-PRISMA /
kawin-type predictions.

- Kissinger: DSC peak temperatures Tp at several heating rates beta give an apparent activation
  energy from ln(beta / Tp^2) = -Ea / (R Tp) + const.
- JMAK: fraction transformed f(t) = 1 - exp(-(k t)^n) fitted to an isothermal series (from
  resistivity, hardness or DSC partial areas), with k = k0 exp(-Q / R T) across temperatures.
- Peak-aging times: Arrhenius fit of time-to-peak hardness vs 1/T (a TTP-style check).
- LSW coarsening: mean radius r(t)^3 - r0^3 = K t; with K = 8 gamma c_e Vm^2 D / (9 R T)
  (c_e in mol/m^3, Vm the precipitate molar volume, D the solute diffusivity) the slope gives an
  interfacial energy gamma for a first calibration. This is the dilute-binary LSW form;
  TC-PRISMA and kawin use more general multicomponent expressions.

CLI:
    python kinetics.py --demo
"""
from __future__ import annotations

import argparse
import json

import numpy as np
from scipy.optimize import curve_fit

R = 8.314462618


def kissinger(beta_K_per_min, Tp_K):
    beta = np.asarray(beta_K_per_min, float)
    Tp = np.asarray(Tp_K, float)
    y = np.log(beta / Tp ** 2)
    x = 1.0 / Tp
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    se = np.sqrt(np.sum(resid ** 2) / max(len(x) - 2, 1) / np.sum((x - x.mean()) ** 2))
    return {"Ea_kJ_mol": -slope * R / 1000, "u_Ea_kJ_mol": se * R / 1000}


def jmak(t, k, n):
    return 1.0 - np.exp(-(k * t) ** n)


def fit_jmak(t_s, f):
    t_s, f = np.asarray(t_s, float), np.asarray(f, float)
    t_half = t_s[np.argmin(np.abs(f - 0.5))]
    (k, n), cov = curve_fit(jmak, t_s, f, p0=(np.log(2) / max(t_half, 1e-9), 1.5),
                            bounds=([1e-12, 0.3], [1e6, 5]))
    return {"k_per_s": float(k), "n": float(n), "u_k": float(np.sqrt(cov[0, 0])), "u_n": float(np.sqrt(cov[1, 1]))}


def arrhenius(T_K, rate_or_inverse_time):
    """Fit ln(rate) = ln(A) - Q/(R T). Pass 1/t_peak as the rate for peak-aging times."""
    T = np.asarray(T_K, float)
    y = np.log(np.asarray(rate_or_inverse_time, float))
    slope, intercept = np.polyfit(1.0 / T, y, 1)
    return {"Q_kJ_mol": -slope * R / 1000, "lnA": float(intercept)}


def lsw_rate(t_s, r_m):
    """K (m^3/s) and r0 from r^3 = r0^3 + K t."""
    t, r3 = np.asarray(t_s, float), np.asarray(r_m, float) ** 3
    K, r03 = np.polyfit(t, r3, 1)
    return {"K_m3_s": float(K), "r0_m": float(np.cbrt(max(r03, 0.0)))}


def lsw_gamma(K_m3_s, T_K, D_m2_s, c_e_mol_m3, Vm_m3_mol):
    """gamma (J/m^2) from K = 8 gamma c_e Vm^2 D / (9 R T)."""
    return 9 * R * T_K * K_m3_s / (8 * c_e_mol_m3 * Vm_m3_mol ** 2 * D_m2_s)


def demo():
    Ea = 120e3
    beta = np.array([5, 10, 20, 40.0])
    # generate Tp consistent with Kissinger and A/Ea
    from scipy.optimize import brentq
    C = 20.0
    Tp = np.array([brentq(lambda T: np.log(b / T ** 2) + Ea / (R * T) - C, 300, 1500) for b in beta])
    ks = kissinger(beta, Tp)
    t = np.geomspace(10, 1e5, 30)
    f = jmak(t, 1e-3, 1.2) + np.random.default_rng(0).normal(0, 0.01, t.size)
    jm = fit_jmak(t, f)
    T = np.array([423, 448, 473.0])
    tpk = 3600 * np.exp(90e3 / R * (1 / T - 1 / 448.0))
    ar = arrhenius(T, 1 / tpk)
    tt = np.array([0, 3600, 7200, 14400, 28800.0])
    K = 2e-30
    r = np.cbrt((2e-9) ** 3 + K * tt)
    ls = lsw_rate(tt, r)
    out = {"kissinger": ks, "jmak": jm, "arrhenius_peak_aging": ar, "lsw": ls}
    print(json.dumps(out, indent=2))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        demo()
    else:
        p.print_help()


if __name__ == "__main__":
    main()
