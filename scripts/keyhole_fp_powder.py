"""Laser absorptance of a powder layer, for the first-principles keyhole model's version 2 (PR #249).

Version 1 had no powder: in conduction mode the beam met the flat liquid at its Fresnel absorptance (0.18-0.20),
and the model called lack of fusion where the AM module didn't. Here the part of the beam that falls ahead of the
melt meets a powder layer instead.

The layer is treated as a homogeneous scattering medium on a flat substrate (Gusarov & Kruth 2005, Int. J. Heat
Mass Transf. 48, 3423): a ray travels a free path drawn from the extinction coefficient for a packed bed of
opaque spheres, beta = 3 (1 - eps) / (2 eps D), with eps the porosity and D the particle diameter (their
Eqs. 20-22: beta = S/4 with S the particle surface per unit pore volume). At the end of each path it meets a
sphere at a random impact parameter, absorbs the sphere's absorptance at that incidence, and is reflected
specularly (deflection pi - 2 theta_i, random azimuth). At the bottom it meets the substrate. Rays that leave
through the top are lost. Monte Carlo, numba.

Particle optics, two ways:
* "fresnel": the clean metal's Fresnel absorptance from its measured n + ik (Rakic 1995 for solid Al at 1.07 um,
  n = 1.372, k = 10.31, absorptance 0.049 at normal incidence).
* "measured-flat": an angle-independent absorptance equal to the measured flat-surface value of real, oxidised Al
  (over 0.20 at 1 um; Rubenchik et al. 2015, Appl. Opt. 54, 7230).

How it compares (`python scripts/keyhole_first_principles_v2.py powder`): the homogenised layer over-traps light.
With Al's textbook index it gives 0.37-0.46 for a layer 1.5-2 particles thick, against the 0.22 Boley et al. 2015
ray-traced for a close-packed bilayer of real spheres; with the measured flat absorptance it gives 0.67-0.72 for
2-20 particles, against the 0.51-0.55 Rubenchik et al. 2015 measured for Al powder by calorimetry. So version 2 uses the measured powder
value (Powder(A_powder=...)), and these two numbers bracket it.

Boley, Khairallah & Rubenchik 2015, Appl. Opt. 54, 2477 (OSTI accepted manuscript), Table 1: Al, n = 1.244 + 10i,
flat 0.047, close-packed bilayer on Al 0.22. Rubenchik et al. 2015, Appl. Opt. 54, 7230 (OSTI accepted manuscript),
Fig. 5c: Al powder (Goodfellow, 99.9 %) at 970 nm, 0.51-0.55 from 40 to 450 C, read off the figure.
"""

from __future__ import annotations

import math

import numba as nb
import numpy as np
from scipy import special

from keyhole_fp_shaped import fresnel_A

BOLEY_AL_BILAYER = 0.22
RUBENCHIK_AL_POWDER = 0.53  # mid-range of 0.51-0.55, read off their Fig. 5c
RAKIC_AL_1070 = (1.3717, 10.314)  # refractiveindex.info, Rakic 1995, interpolated at 1.070 um
RUBENCHIK_AL_FLAT = 0.20  # measured flat Al at 1 um, "over 20%" (Rubenchik et al. 2015)


@nb.njit(cache=True)
def powder_mc(Np_r, Np_i, Ns_r, Ns_i, alpha_p, alpha_s, L, beta, n_rays, seed):
    """Absorbed fractions (total, in the powder, in the substrate) of a normally incident beam.

    Np, Ns: complex indices of particles and substrate, used when alpha_p / alpha_s < 0; otherwise those constant
    absorptances are used. L: layer thickness; beta: extinction coefficient (1/length, same units)."""
    np.random.seed(seed)
    a_pow = 0.0
    a_sub = 0.0
    for _ in range(n_rays):
        w = 1.0
        z = 0.0
        ux, uy, uz = 0.0, 0.0, 1.0
        for _b in range(2000):
            s = -math.log(1.0 - np.random.random()) / beta
            z_new = z + s * uz
            if z_new < 0.0:
                break
            if z_new >= L:
                cos_i = abs(uz)
                A = alpha_s if alpha_s >= 0 else fresnel_A(Ns_r, Ns_i, cos_i)
                a_sub += w * A
                w *= 1.0 - A
                z = L
                uz = -uz
                if w < 1e-6:
                    break
                continue
            z = z_new
            b = math.sqrt(np.random.random())
            cos_t = math.sqrt(max(1.0 - b * b, 0.0))
            A = alpha_p if alpha_p >= 0 else fresnel_A(Np_r, Np_i, cos_t)
            a_pow += w * A
            w *= 1.0 - A
            if w < 1e-6:
                break
            # specular reflection off the sphere: deflection chi = pi - 2 theta_i, random azimuth
            chi = math.pi - 2.0 * math.asin(min(b, 1.0))
            phi = 2.0 * math.pi * np.random.random()
            sc, cc = math.sin(chi), math.cos(chi)
            if abs(uz) > 0.99999:
                ux_n = sc * math.cos(phi)
                uy_n = sc * math.sin(phi)
                uz_n = cc * (1.0 if uz > 0 else -1.0)
            else:
                den = math.sqrt(1.0 - uz * uz)
                ux_n = sc * (ux * uz * math.cos(phi) - uy * math.sin(phi)) / den + ux * cc
                uy_n = sc * (uy * uz * math.cos(phi) + ux * math.sin(phi)) / den + uy * cc
                uz_n = -sc * math.cos(phi) * den + uz * cc
            nn = math.sqrt(ux_n * ux_n + uy_n * uy_n + uz_n * uz_n)
            ux, uy, uz = ux_n / nn, uy_n / nn, uz_n / nn
    return (a_pow + a_sub) / n_rays, a_pow / n_rays, a_sub / n_rays


def extinction(porosity, D):
    """Gusarov & Kruth 2005: beta = 3 (1 - eps) / (2 eps D)."""
    return 3.0 * (1.0 - porosity) / (2.0 * porosity * D)


def layer_absorptance(L, D, porosity, optics="fresnel", N_sub=None, n_rays=40000, seed=7):
    """Absorptance of a powder layer L thick (particles D, porosity eps) on a substrate of the same metal (or of
    complex index N_sub). Returns (total, powder, substrate)."""
    beta = extinction(porosity, D)
    nr, ni = RAKIC_AL_1070
    if optics == "fresnel":
        sr, si = (nr, ni) if N_sub is None else (N_sub.real, N_sub.imag)
        return powder_mc(nr, ni, sr, si, -1.0, -1.0, L, beta, n_rays, seed)
    a = RUBENCHIK_AL_FLAT
    return powder_mc(nr, ni, nr, ni, a, a, L, beta, n_rays, seed)


class Powder:
    """Powder layer ahead of the melt in conduction mode. The beam's share ahead of the melt front (the liquidus
    on the centre line) meets powder; the rest meets the liquid."""

    def __init__(self, A_powder=None, layer=30e-6, packing=0.5, D=35e-6, optics="measured-flat"):
        """A_powder: the layer's absorptance; if None, from the homogenised model above. The powder over a
        consolidated layer is about layer / packing thick once the build is steady."""
        self.L = layer / packing
        self.D = D
        self.porosity = 1.0 - packing
        self.optics = optics
        self.A_powder = (float(layer_absorptance(self.L, D, self.porosity, optics)[0]) if A_powder is None
                         else float(A_powder))

    def conduction_absorptance(self, A_liq, P, v, r0, th, n_iter=4):
        """Effective absorptance and the share of the beam on powder, iterated with the melt front's position."""
        import keyhole_first_principles as fp
        A = A_liq
        f = 0.0
        for _ in range(n_iter):
            xs = np.linspace(-0.5 * r0, 4 * r0, 91)
            th_x = fp.gaussian_field(xs, 0.0, 0.0, A * P, r0, th.k, th.kappa, v)
            above = th_x > th.theta_l
            if not above.any():
                x_m = -10 * r0  # nothing melts: the whole beam is on powder
            else:
                x_m = float(xs[np.nonzero(above)[0].max()])
            f = 0.5 * float(special.erfc(math.sqrt(2.0) * x_m / r0))
            A = f * self.A_powder + (1 - f) * A_liq
        return A, f
