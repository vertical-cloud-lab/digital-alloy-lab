#!/usr/bin/env python3
"""Archimedes density of printed cubes and coupons -> relative density and porosity, with
uncertainty, plus an image-based porosity estimate from a polished cross-section.

Archimedes (ASTM B962-type, water as the immersion fluid):

    rho = m_air * (rho_w - rho_air) / (m_air - m_wet) + rho_air

m_air: mass in air; m_wet: apparent mass immersed (the balance reading with the sample hanging in
water, after taring the wire/basket in water). rho_air ~ 0.0012 g/cm^3. Water density comes from
the Tanaka et al. (2001) formula for air-free water at the measured temperature.

Relative density = rho / rho_ref, where rho_ref is the reference ("theoretical") density. For a new
alloy, use the gas-pycnometer density of its powder or a Thermo-Calc / pycalphad density at 20 C;
report which. Porosity = 1 - relative density.

Image porosity: Otsu threshold on a grayscale micrograph (pores dark), area fraction of pores.
By the Delesse principle, an area fraction on a random section estimates the volume fraction.

CLI:
    python density_porosity.py archimedes --m-air 2.5134 --m-wet 1.5751 --T-water 21.3 --rho-ref 2.670
    python density_porosity.py image section.png [--invert]
    python density_porosity.py --demo
"""
from __future__ import annotations

import argparse
import json
import math

import numpy as np

RHO_AIR = 0.0012   # g/cm^3, near room conditions


def water_density(T_C: float) -> float:
    """Density of air-free water, g/cm^3, Tanaka et al. (2001), valid 0-40 C."""
    a1, a2, a3, a4, a5 = -3.983035, 301.797, 522528.9, 69.34881, 999.974950
    rho = a5 * (1 - (T_C + a1) ** 2 * (T_C + a2) / (a3 * (T_C + a4)))
    return rho / 1000.0


def archimedes(m_air, m_wet, T_water, rho_ref=None, u_mass=0.0002, u_T=0.5, rho_air=RHO_AIR):
    """Density (g/cm^3) and, with rho_ref, relative density and porosity, with 1-sigma uncertainty.

    u_mass: standard uncertainty of each weighing (g); u_T: of the water temperature (K).
    """
    rw = water_density(T_water)
    rho = m_air * (rw - rho_air) / (m_air - m_wet) + rho_air
    # numerical propagation
    def f(ma, mw, T):
        r = water_density(T)
        return ma * (r - rho_air) / (ma - mw) + rho_air
    h = 1e-6
    d_ma = (f(m_air + h, m_wet, T_water) - f(m_air - h, m_wet, T_water)) / (2 * h)
    d_mw = (f(m_air, m_wet + h, T_water) - f(m_air, m_wet - h, T_water)) / (2 * h)
    d_T = (f(m_air, m_wet, T_water + 1e-3) - f(m_air, m_wet, T_water - 1e-3)) / 2e-3
    u = math.sqrt((d_ma * u_mass) ** 2 + (d_mw * u_mass) ** 2 + (d_T * u_T) ** 2)
    out = {"rho_g_cm3": rho, "u_rho_g_cm3": u, "rho_water_g_cm3": rw}
    if rho_ref:
        out.update({"relative_density": rho / rho_ref, "porosity": 1 - rho / rho_ref,
                    "u_relative_density": u / rho_ref})
    return out


def otsu_threshold(img: np.ndarray, nbins: int = 256) -> float:
    hist, edges = np.histogram(img.ravel(), bins=nbins)
    centres = 0.5 * (edges[:-1] + edges[1:])
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m0 = np.cumsum(hist * centres) / np.maximum(w0, 1)
    m1 = (np.sum(hist * centres) - np.cumsum(hist * centres)) / np.maximum(w1, 1)
    between = w0 * w1 * (m0 - m1) ** 2
    return float(centres[int(np.argmax(between))])


def image_porosity(img: np.ndarray, invert: bool = False) -> dict:
    g = img.astype(float)
    if g.ndim == 3:
        g = g[..., :3].mean(axis=2)
    if invert:
        g = g.max() - g
    t = otsu_threshold(g)
    pores = g < t
    return {"threshold": t, "pore_area_fraction": float(pores.mean())}


def demo():
    # A 1 cm^3 cube of rho 2.670 with 1.0 % porosity, weighed at 21.3 C.
    rho_true, por = 2.670, 0.010
    rw = water_density(21.3)
    V = 1.0
    M = rho_true * (1 - por) * V              # true mass
    m_air = M - RHO_AIR * V                    # balance reading in air (air buoyancy)
    m_wet = M - rw * V                         # balance reading immersed in water
    r = archimedes(m_air, m_wet, 21.3, rho_ref=rho_true)
    rng = np.random.default_rng(0)
    img = rng.normal(200, 10, (400, 400))
    yy, xx = np.mgrid[:400, :400]
    mask = np.zeros(img.shape, bool)
    for cx, cy, rr in [(100, 100, 12), (300, 220, 8), (200, 320, 10)]:
        mask |= (xx - cx) ** 2 + (yy - cy) ** 2 < rr ** 2
    img[mask] = 40
    ip = image_porosity(img)
    true_frac = float(mask.mean())
    print(json.dumps({"archimedes": r, "true_porosity": por, "image": ip,
                      "image_true_fraction": true_frac}, indent=2))
    return r, ip, true_frac


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--demo", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    a1 = sub.add_parser("archimedes")
    a1.add_argument("--m-air", type=float, required=True)
    a1.add_argument("--m-wet", type=float, required=True)
    a1.add_argument("--T-water", type=float, required=True)
    a1.add_argument("--rho-ref", type=float)
    a1.add_argument("--u-mass", type=float, default=0.0002)
    a2 = sub.add_parser("image")
    a2.add_argument("path")
    a2.add_argument("--invert", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        demo()
    elif a.cmd == "archimedes":
        print(json.dumps(archimedes(a.m_air, a.m_wet, a.T_water, a.rho_ref, a.u_mass), indent=2))
    elif a.cmd == "image":
        import matplotlib.image as mpimg
        print(json.dumps(image_porosity(mpimg.imread(a.path), a.invert), indent=2))
    else:
        p.print_help()


if __name__ == "__main__":
    main()
