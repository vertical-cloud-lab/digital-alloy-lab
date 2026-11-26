"""A first-principles keyhole and melt-pool model for laser powder bed fusion (PR #249, issue #235).

Our own implementation, written to replace the Thermo-Calc AM module where eagar-tsai can't: keyholing and
keyhole-mode pool size. Nothing in it is fitted to keyhole or melt-pool data. Its inputs are the beam, the
scan, and measured or tabulated material properties, each cited in PROPERTY_SOURCES (and in the README).

The physics, in order:

1. Optics. The liquid metal's dielectric function from the Drude free-electron model, with the electron
   density from the valence and the liquid density, and the damping from the measured liquid electrical
   resistivity (gamma = eps0 * wp^2 * rho_el). Fresnel absorptance for s and p light at any incidence,
   averaged for an unpolarised fibre laser.
2. Multiple reflections. A Monte Carlo ray tracer (our own) sends a Gaussian beam into a keyhole shaped as a
   paraboloid of revolution r^2 = a0^2 (1 - z/d), bounces every ray off the walls with the Fresnel
   absorptance at its local incidence, and records where the power is absorbed. Light outside the opening
   meets the flat liquid surface at normal incidence.
3. Conduction from the keyhole wall. The wall is held at T_w, the temperature at which the saturated vapour
   pressure equals the ambient pressure plus the Laplace pressure sigma/a0 of the opening. The heat it
   loses is found by collocation: point sources on the keyhole axis (with images, for an adiabatic top
   surface), each the moving point source of Rosenthal, with strengths that hold the azimuthal mean of the
   temperature at each wall circle at T_w. The beam's wings, absorbed outside the opening, enter as known
   surface sources. For a long cylinder this reproduces Kaplan's (1994) moving-cylinder loss
   2 pi k dT Pe K1(Pe)/K0(Pe) per unit depth (checked in test_keyhole_first_principles.py).
4. Evaporation. Vapour leaves through the opening, driven by the Laplace overpressure (Bernoulli, capped at
   choked flow), and carries the enthalpy of vaporisation with it.
5. The keyhole's shape. (a0, d) are the two numbers for which the power absorbed inside the keyhole equals the
   power conducted and evaporated from its wall, and the depth centroid of the absorbed power equals the
   depth centroid of the losses (a two-moment form of Kaplan's point-by-point wall balance).
6. Mode. A keyhole opens if the flat liquid surface, at its own Fresnel absorptance, would reach the boiling
   point under the moving Gaussian beam. Otherwise the track stays in conduction mode.
7. Melt pool. The liquidus (and solidus) isotherm of the same sources: the keyhole's axis sources and the
   surface wings in keyhole mode, or the moving Gaussian surface source (exact time integral) in conduction
   mode.
8. Latent heat and temperature-dependent properties. The linear heat equation is solved in an enthalpy
   variable: rho c_bar theta with c_bar the secant heat capacity (H(T_w) - H(T0)) / (T_w - T0), which includes
   the enthalpy of fusion from CALPHAD (pycalphad + MatCalc mc_al), and k_bar the Kirchhoff mean of the
   solid and liquid conductivities (liquid from the Wiedemann-Franz law and the measured resistivity).
   Isotherms are placed at theta_l = (H(T_l) - H(T0)) / c_bar.

Melt flow is left out: no Marangoni or recoil-driven convection, so pool length is a lower bound.

Usage (from the repo root; about 5 minutes on 4 vCPUs):

    python scripts/keyhole_first_principles.py all --out arroyave-orchid-tools/keyhole-alternatives/first-principles
    python scripts/keyhole_first_principles.py point --alloy blend --P 375 --v 0.4

Requires numpy, scipy, pandas, matplotlib, openpyxl (for Gan et al.'s spreadsheet).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import pathlib
import sys
import time

import numpy as np
import pandas as pd
from scipy import interpolate, optimize, special

REPO = pathlib.Path(__file__).resolve().parent.parent
FP_DIR = REPO / "arroyave-orchid-tools" / "keyhole-alternatives" / "first-principles"
ENTHALPY_CSV = FP_DIR / "mc_al-enthalpy-vs-T.csv"

# --- physical constants (CODATA 2018) -------------------------------------------------------------
R_GAS = 8.314462618
E_CH = 1.602176634e-19
M_E = 9.1093837015e-31
EPS0 = 8.8541878128e-12
C_LIGHT = 299792458.0
N_A = 6.02214076e23
P_AMB = 101325.0
L0_WF = 2.45e-8  # Lorenz number used by Leitner et al. 2017, W Ohm / K^2
LAMBDA = 1.07e-6  # fibre laser wavelength, m

# --- material properties ----------------------------------------------------------------------------
# Every number used below, with where it comes from. The README repeats this table with full citations.
PROPERTY_SOURCES = {
    "al_liquid_resistivity": "Leitner et al. 2017, Metall. Mater. Trans. A 48, 3036 (doi:10.1007/s11661-017-4053-6), "
                             "Table I: rho_VE = 0.097 + 1.681e-4 T uOhm m (volume-corrected, 933-1491 K, +/-4 %)",
    "al_si_liquid_resistivity": "Brandt & Neuer 2007, Int. J. Thermophys. 28, 1429 (doi:10.1007/s10765-006-0144-0), "
                                "Tables I-II: +0.675 uOhm cm per wt% Si (0-12 wt%, 700 C; our linear fit) and "
                                "+0.92 uOhm cm per wt% Mg (AlSi9Mg0.6 vs AlSi9)",
    "al_liquid_density": "Leitner et al. 2017, Table I: D = 2670 - 0.299 T kg/m^3 (933-1680 K, +/-3.8 %)",
    "lorenz_number": "Leitner et al. 2017, Eq. 7: L = 2.45e-8 V^2/K^2",
    "al_boiling_point_and_enthalpy_of_vaporisation": "NIST-JANAF table Al-001: T_b = 2790.812 K, "
                                                      "dH_vap(T_b) = 381.667 - 87.665 = 294.0 kJ/mol",
    "al_vapour_pressure": "Clausius-Clapeyron through the JANAF boiling point with 294.0 kJ/mol. Alcock et al. 1984 "
                          "(Can. Metall. Q. 23, 309; via the CRC Handbook) is valid only to 1800 K and extrapolates to "
                          "1 atm at 2743 K",
    "al_surface_tension": "Leitner et al. 2017, Table I: 993 - 0.127 T mN/m (oxygen-saturated, 933-1550 K); "
                          "Kobatake et al. 2015 (doi:10.1007/s10853-015-8883-6) put Al-Si within 0.1 N/m of it",
    "alloy_enthalpy": "pycalphad 0.11.2 equilibrium with MatCalc mc_al v2.032 (scripts/keyhole_fp_enthalpy_mc_al.py); "
                      "its liquid c_p (1.13-1.16 kJ/kg/K) matches Leitner et al.'s 1.127 for Al",
    "alloy_liquidus_solidus": "MatCalc mc_al v2.032 via pycalphad (arroyave-orchid-tools/pycalphad-al-cu)",
    "solid_conductivity": "110 W/m/K, the AlSi10Mg value used in #238",
    "solid_density": "rule of mixtures from Al 2700, Si 2330 and Mg 1738 kg/m^3",
    "valence": "free electrons per atom: Al 3, Si 4, Mg 2",
    "liquid_al_optics_check": "Krishnan et al. 1993, Metall. Trans. A 24, 67 (doi:10.1007/BF02669604), Table I: "
                              "liquid Al at 632.8 nm and 1800 K, n = 0.91, k = 6.33 (emissivity 0.083)",
}


@dataclasses.dataclass
class Material:
    name: str
    x: dict  # atomic fractions
    T_s: float
    T_l: float
    rho_s: float  # solid density at room temperature, kg/m^3
    k_s: float  # solid conductivity, W/m/K
    M: float  # mean molar mass, kg/mol
    z_val: float  # free electrons per atom
    L_v: float  # enthalpy of vaporisation, J/kg
    sigma: float  # surface tension at the keyhole wall, N/m
    H_table: tuple | None = None  # (T, H) in K and J/kg, from CALPHAD
    cp_const: float | None = None  # used when there is no H table (Gan et al.'s rows)
    L_m: float = 0.0  # enthalpy of fusion when there is no H table, J/kg
    vap_A: float = 5.911  # log10(p_atm) = vap_A - vap_B / T for the volatile element
    vap_B: float = 16211.0
    x_vol: float = 1.0  # mole fraction of the volatile element (Raoult)
    rho_el: tuple = (24.7e-8, 0.0145e-8, 933.47)  # liquid resistivity: rho0 + slope (T - Tref), Ohm m
    rho_l_fn: tuple = (2377.23, 0.311, 933.47)  # liquid density rho0 - slope (T - Tref)
    T_w_fixed: float | None = None  # wall temperature override (Gan et al.'s T_v)
    k_l_fixed: float | None = None  # liquid conductivity override (constant-property runs)

    # thermodynamics
    def H(self, T):
        T = np.asarray(T, dtype=float)
        if self.H_table is None:
            cp = self.cp_const
            f = np.clip((T - self.T_s) / max(self.T_l - self.T_s, 1e-9), 0.0, 1.0)
            return cp * T + self.L_m * f
        Tt, Ht = self.H_table
        slope = (Ht[-1] - Ht[-6]) / (Tt[-1] - Tt[-6])
        return np.where(T <= Tt[-1], np.interp(T, Tt, Ht), Ht[-1] + slope * (T - Tt[-1]))

    def p_sat(self, T):
        """Saturated vapour pressure of the alloy (Raoult on the volatile element), Pa."""
        return self.x_vol * P_AMB * 10.0 ** (self.vap_A - self.vap_B / np.asarray(T, dtype=float))

    def T_boil(self, p=P_AMB):
        return self.vap_B / (self.vap_A - math.log10(p / (P_AMB * self.x_vol)))

    def rho_el_liq(self, T):
        r0, s, Tr = self.rho_el
        return r0 + s * (np.asarray(T, dtype=float) - Tr)

    def rho_liq(self, T):
        r0, s, Tr = self.rho_l_fn
        return r0 - s * (np.asarray(T, dtype=float) - Tr)

    def k(self, T):
        T = np.asarray(T, dtype=float)
        kl = (self.k_l_fixed if self.k_l_fixed is not None
              else L0_WF * np.maximum(T, self.T_l) / self.rho_el_liq(np.maximum(T, self.T_l)))
        f = np.clip((T - self.T_s) / max(self.T_l - self.T_s, 1e-9), 0.0, 1.0)
        return (1 - f) * self.k_s + f * kl

    def means(self, T0, T1):
        """Kirchhoff-mean conductivity and secant heat capacity (with latent heat) over [T0, T1]."""
        Tg = np.linspace(T0, T1, 400)
        kbar = float(np.trapezoid(self.k(Tg), Tg) / (T1 - T0))
        cbar = float((self.H(T1) - self.H(T0)) / (T1 - T0))
        return kbar, cbar

    def electron_density(self, T):
        return self.z_val * self.rho_liq(T) * N_A / self.M


# --- optics -------------------------------------------------------------------------------------------

def drude_index(rho_el, n_e, lam=LAMBDA):
    """Complex refractive index n + ik of a Drude metal with resistivity rho_el and electron density n_e."""
    w = 2 * math.pi * C_LIGHT / lam
    wp2 = n_e * E_CH ** 2 / (EPS0 * M_E)
    gamma = EPS0 * wp2 * rho_el
    eps = 1 - wp2 / (w ** 2 + 1j * gamma * w)
    return np.sqrt(eps)


def drude_from_nk(n, k, lam):
    """Drude plasma frequency squared and damping rate that reproduce a measured n + ik at wavelength lam."""
    w = 2 * math.pi * C_LIGHT / lam
    eps = complex(n, k) ** 2
    ratio = eps.imag / (1 - eps.real)  # = gamma / w
    gamma = ratio * w
    wp2 = (1 - eps.real) * (w ** 2 + gamma ** 2)
    return wp2, gamma


# Krishnan et al. 1993: liquid Al at 632.8 nm and 1800 K, n = 0.91, k = 6.33.
KRISHNAN_AL = {"n": 0.91, "k": 6.33, "lam": 632.8e-9, "T": 1800.0}
OPTICS = "drude-dc"  # or "drude-krishnan": Drude parameters anchored on Krishnan et al.'s measurement


def drude_index_params(wp2, gamma, lam=LAMBDA):
    w = 2 * math.pi * C_LIGHT / lam
    return np.sqrt(1 - wp2 / (w ** 2 + 1j * gamma * w))


def fresnel_absorptance(N, cos_i):
    """Unpolarised Fresnel absorptance of a metal of complex index N at incidence cos_i."""
    cos_i = np.clip(np.asarray(cos_i, dtype=float), 0.0, 1.0)
    sin2 = 1 - cos_i ** 2
    s = np.sqrt(N ** 2 - sin2)
    rs = (cos_i - s) / (cos_i + s)
    rp = (N ** 2 * cos_i - s) / (N ** 2 * cos_i + s)
    return 1 - 0.5 * (np.abs(rs) ** 2 + np.abs(rp) ** 2)


# --- ray tracing in the keyhole ----------------------------------------------------------------------

N_ZBINS = 24
SHAPES = {"cone": 2, "paraboloid": 1}  # r^2 = a0^2 (1 - z/d)^p


def keyhole_radius(a0, d, z, shape="cone"):
    return a0 * np.clip(1 - np.asarray(z) / d, 0.0, 1.0) ** (SHAPES[shape] / 2)


def trace_keyhole(a0, d, N, n_rays=20000, seed=1, max_bounces=400, w_min=1e-7, shape="cone"):
    """Gaussian beam (1/e^2 radius 1) into the keyhole r^2 = a0^2 (1 - z/d)^p, z down. Lengths in beam radii.

    p = 2 is a cone (Lankalapalli et al. 1996), p = 1 a paraboloid. A paraboloid sends every vertical ray
    through its focus and back out after two hits, so it is the low-absorptivity limit; a cone traps light
    in about pi / (4 theta) reflections for a wall angle theta.

    Returns the fraction absorbed inside the keyhole, the fraction absorbed on the flat surface outside the
    opening, the absorbed power in N_ZBINS bins of z/d, and the mean number of wall hits per entering ray.
    """
    p_exp = SHAPES[shape]
    rng = np.random.default_rng(seed)
    r = np.sqrt(-np.log(1.0 - rng.random(n_rays)) / 2.0)
    th = 2 * np.pi * rng.random(n_rays)
    w0 = 1.0 / n_rays
    A_flat = float(fresnel_absorptance(N, 1.0))
    inside = r < a0
    A_surf = A_flat * w0 * np.count_nonzero(~inside)
    zbins = np.zeros(N_ZBINS)
    if d <= 0 or not inside.any():
        return 0.0, A_surf, zbins, 0.0
    c2 = (a0 / d) ** 2
    px, py = r[inside] * np.cos(th[inside]), r[inside] * np.sin(th[inside])
    pz = np.zeros_like(px)
    ux, uy, uz = np.zeros_like(px), np.zeros_like(px), np.ones_like(px)
    w = np.full(px.shape, w0)
    absorbed = 0.0
    hits = 0
    n_enter = px.size
    for _ in range(max_bounces):
        if px.size == 0:
            break
        if p_exp == 1:  # x^2 + y^2 + (a0^2/d) z - a0^2 = 0
            A = ux * ux + uy * uy
            B = 2 * (px * ux + py * uy) + a0 * a0 / d * uz
            C = px * px + py * py + a0 * a0 / d * pz - a0 * a0
        else:  # x^2 + y^2 - c^2 (d - z)^2 = 0
            pw = d - pz
            A = ux * ux + uy * uy - c2 * uz * uz
            B = 2 * (px * ux + py * uy + c2 * pw * uz)
            C = px * px + py * py - c2 * pw * pw
        C = np.minimum(C, 0.0)
        disc = np.maximum(B * B - 4 * A * C, 0.0)
        sq = np.sqrt(disc)
        with np.errstate(divide="ignore", invalid="ignore"):
            lin = np.abs(A) < 1e-14
            t1 = np.where(lin, -C / B, (-B - sq) / (2 * A))
            t2 = np.where(lin, np.inf, (-B + sq) / (2 * A))
            t_exit = np.where(uz < 0, -pz / uz, np.inf)

        def ok(t):
            zt = pz + t * uz
            return np.isfinite(t) & (t > 1e-12) & (zt <= d * (1 + 1e-9))

        t1 = np.where(ok(t1), t1, np.inf)
        t2 = np.where(ok(t2), t2, np.inf)
        t_wall = np.minimum(t1, t2)
        hit = (t_wall < t_exit) & np.isfinite(t_wall)
        if not hit.any():
            break
        px, py, pz = px[hit] + t_wall[hit] * ux[hit], py[hit] + t_wall[hit] * uy[hit], pz[hit] + t_wall[hit] * uz[hit]
        ux, uy, uz, w = ux[hit], uy[hit], uz[hit], w[hit]
        if p_exp == 1:
            nx, ny, nz = 2 * px, 2 * py, np.full_like(px, a0 * a0 / d)
        else:
            nx, ny, nz = 2 * px, 2 * py, 2 * c2 * np.maximum(d - pz, 0.0)
        nn = np.maximum(np.sqrt(nx * nx + ny * ny + nz * nz), 1e-300)
        nx, ny, nz = nx / nn, ny / nn, nz / nn
        cos_i = ux * nx + uy * ny + uz * nz
        Aabs = fresnel_absorptance(N, np.abs(cos_i))
        dep = w * Aabs
        absorbed += dep.sum()
        hits += px.size
        idx = np.clip((pz / d * N_ZBINS).astype(int), 0, N_ZBINS - 1)
        np.add.at(zbins, idx, dep)
        w = w * (1 - Aabs)
        ux, uy, uz = ux - 2 * cos_i * nx, uy - 2 * cos_i * ny, uz - 2 * cos_i * nz
        px, py, pz = px - 1e-9 * nx, py - 1e-9 * ny, np.clip(pz - 1e-9 * nz, 0.0, d)
        keep = w > w_min
        px, py, pz, ux, uy, uz, w = px[keep], py[keep], pz[keep], ux[keep], uy[keep], uz[keep], w[keep]
    return float(absorbed), float(A_surf), zbins, hits / max(n_enter, 1)


class RayTable:
    """trace_keyhole tabulated over d/a0 and a0/r0 for one complex index, for smooth interpolation."""

    S = np.geomspace(0.02, 40.0, 44)
    G = np.geomspace(0.25, 3.0, 18)

    def __init__(self, N, n_rays=12000, shape="cone"):
        self.N = N
        self.shape = shape
        dims = (self.S.size, self.G.size)
        self.Akh = np.zeros(dims)
        self.Asf = np.zeros(dims)
        self.zc = np.zeros(dims)
        self.hits = np.zeros(dims)
        zmid = (np.arange(N_ZBINS) + 0.5) / N_ZBINS
        for i, s in enumerate(self.S):
            for j, g in enumerate(self.G):
                a, sf, zb, h = trace_keyhole(g, s * g, N, n_rays=n_rays, seed=1000 + j, shape=shape)
                self.Akh[i, j], self.Asf[i, j], self.hits[i, j] = a, sf, h
                self.zc[i, j] = float((zb * zmid).sum() / zb.sum()) if zb.sum() > 0 else 0.5
        pts = (np.log(self.S), np.log(self.G))
        kw = dict(bounds_error=False, fill_value=None)
        self._akh = interpolate.RegularGridInterpolator(pts, self.Akh, **kw)
        self._zc = interpolate.RegularGridInterpolator(pts, self.zc, **kw)
        self._hits = interpolate.RegularGridInterpolator(pts, self.hits, **kw)
        self.A_flat = float(fresnel_absorptance(N, 1.0))

    def __call__(self, s, g):
        p = [[math.log(min(max(s, self.S[0]), self.S[-1])), math.log(min(max(g, self.G[0]), self.G[-1]))]]
        A_surf = self.A_flat * math.exp(-2 * g * g)
        return float(self._akh(p)[0]), A_surf, float(self._zc(p)[0]), float(self._hits(p)[0])


# --- conduction ---------------------------------------------------------------------------------------

def point_source_field(xp, yp, zp, src_z, src_q, k, kappa, v, src_x=None, src_y=None, surface=False):
    """Temperature rise at points from moving point sources (beam moving in +x) in a half-space z > 0.

    Sources below the surface get an image above it (adiabatic top surface); surface sources get a factor 2.
    """
    xp, yp, zp = (np.asarray(a, dtype=float)[..., None] for a in (xp, yp, zp))
    sx = np.zeros_like(src_z) if src_x is None else src_x
    sy = np.zeros_like(src_z) if src_y is None else src_y
    dx, dy = xp - sx, yp - sy
    R1 = np.sqrt(dx * dx + dy * dy + (zp - src_z) ** 2)
    R1 = np.maximum(R1, 1e-9)
    th = np.exp(-v * (R1 + dx) / (2 * kappa)) / (4 * math.pi * k * R1)
    if surface:
        th = 2 * th
    else:
        R2 = np.maximum(np.sqrt(dx * dx + dy * dy + (zp + src_z) ** 2), 1e-9)
        th = th + np.exp(-v * (R2 + dx) / (2 * kappa)) / (4 * math.pi * k * R2)
    return (th * src_q).sum(axis=-1)


_S_NODES = np.concatenate([[0.0], np.geomspace(1e-7, math.sqrt(0.08), 700)])


def gaussian_field(xp, yp, zp, Q, r0, k, kappa, v):
    """Temperature rise from a moving Gaussian surface source (1/e^2 radius r0, absorbed power Q), exact
    time integral with t = s^2 (Eagar & Tsai 1983 / Carslaw & Jaeger)."""
    xp, yp, zp = (np.asarray(a, dtype=float)[..., None] for a in (xp, yp, zp))
    s = _S_NODES
    t = s * s
    rho_c = k / kappa
    var = 4 * kappa * t + r0 * r0 / 2
    f = (np.exp(-((xp + v * t) ** 2 + yp ** 2) / var) / (math.pi * var)
         * 2 * np.exp(-zp ** 2 / np.maximum(4 * kappa * t, 1e-300)) / math.sqrt(4 * math.pi * kappa))
    # dt = 2 s ds cancels the 1/sqrt(t) of the vertical kernel, so f carries no 1/sqrt(t) and the weight is 2.
    integ = np.trapezoid(f * 2, s, axis=-1)
    return Q / rho_c * integ


def kaplan_loss_per_depth(a, k, kappa, dT, v):
    """Kaplan 1994: heat lost per unit depth from a cylinder of radius a at dT, moving at v."""
    pe = v * a / (2 * kappa)
    return 2 * math.pi * k * dT * pe * special.k1(pe) / special.k0(pe)


@dataclasses.dataclass
class Thermal:
    k: float
    kappa: float
    rho_c: float
    theta_w: float
    theta_l: float
    theta_s: float
    T_w: float


def thermal_state(m: Material, T0: float, T_w: float) -> Thermal:
    kbar, cbar = m.means(T0, T_w)
    rho_c = m.rho_s * cbar
    th = lambda T: float((m.H(T) - m.H(T0)) / cbar)  # noqa: E731
    return Thermal(k=kbar, kappa=kbar / rho_c, rho_c=rho_c, theta_w=T_w - T0, theta_l=th(m.T_l),
                   theta_s=th(m.T_s), T_w=T_w)


N_SRC = 24
N_AZ = 16


def surface_wing_sources(a0, r0, Q_surf):
    """Point sources on the surface carrying the power absorbed outside the keyhole opening (Gaussian wings)."""
    if Q_surf <= 0:
        return np.zeros(0), np.zeros(0), np.zeros(0)
    # Four rings at the power-weighted radii of four equal-power annuli of the Gaussian beyond a0.
    u0 = math.exp(-2 * a0 ** 2 / r0 ** 2)
    radii = []
    for i in range(4):
        u_mid = u0 * (1 - (i + 0.5) / 4)
        radii.append(r0 * math.sqrt(-math.log(max(u_mid, 1e-300)) / 2))
    phis = np.arange(8) * 2 * math.pi / 8
    xs = np.array([rr * math.cos(p) for rr in radii for p in phis])
    ys = np.array([rr * math.sin(p) for rr in radii for p in phis])
    qs = np.full(xs.size, Q_surf / xs.size)
    return xs, ys, qs


def keyhole_conduction(a0, d, th: Thermal, v, wings, shape="cone"):
    """Point sources on the axis that hold each wall circle's mean temperature at T_w (NNLS collocation)."""
    j = np.arange(N_SRC)
    zs = d * (j + 0.5) / N_SRC  # source depths
    zc = d * (j + 0.5) / N_SRC  # collocation depths
    ac = keyhole_radius(a0, d, zc, shape)
    phi = np.arange(N_AZ) * 2 * math.pi / N_AZ
    X = ac[:, None] * np.cos(phi)[None, :]
    Y = ac[:, None] * np.sin(phi)[None, :]
    Z = np.repeat(zc[:, None], N_AZ, axis=1)
    G = np.zeros((N_SRC, N_SRC))
    for jj in range(N_SRC):
        G[:, jj] = point_source_field(X, Y, Z, np.array([zs[jj]]), np.array([1.0]), th.k, th.kappa, v).mean(axis=1)
    target = np.full(N_SRC, th.theta_w)
    wx, wy, wq = wings
    if wq.size:
        target = target - point_source_field(X, Y, Z, np.zeros_like(wq), wq, th.k, th.kappa, v,
                                             src_x=wx, src_y=wy, surface=True).mean(axis=1)
    target = np.maximum(target, 0.0)
    q, _ = optimize.nnls(G, target, maxiter=2000)
    return zs, q


def opening_overpressure(m: Material, a0):
    return m.sigma / a0


def wall_temperature(m: Material, a0):
    if m.T_w_fixed is not None:
        return m.T_w_fixed
    return m.T_boil(P_AMB + opening_overpressure(m, a0))


def evaporation_power(m: Material, a0, T_w):
    """Vapour flowing out of the opening, driven by the Laplace overpressure; Bernoulli, capped at choked."""
    p_v = P_AMB + opening_overpressure(m, a0)
    rho_v = p_v * m.M / (R_GAS * T_w)
    u = math.sqrt(2 * (p_v - P_AMB) / rho_v)
    c_sound = math.sqrt(5.0 / 3.0 * R_GAS * T_w / m.M)
    mdot = rho_v * min(u, c_sound) * math.pi * a0 ** 2
    return mdot * m.L_v


# --- one process point ---------------------------------------------------------------------------------

@dataclasses.dataclass
class Result:
    mode: str
    A: float
    A_keyhole: float = 0.0
    a0_um: float = 0.0
    d_um: float = 0.0
    Wk_over_Dk: float = float("nan")
    T_w: float = float("nan")
    T_peak_conduction: float = float("nan")
    Q_cond_W: float = 0.0
    Q_evap_W: float = 0.0
    residual: float = 0.0
    hits_per_ray: float = 0.0
    pool_depth_um: float = 0.0
    pool_width_um: float = 0.0
    pool_length_um: float = 0.0
    pool_Dh_um: float = 0.0
    pool_depth_solidus_um: float = 0.0
    pool_width_solidus_um: float = 0.0
    pool_length_solidus_um: float = 0.0
    zc_abs: float = float("nan")
    zc_loss: float = float("nan")
    converged: bool = True


def _bisect_vec(f, lo, hi, n=48):
    """Vectorised bisection for f(x) = 0 with f(lo) > 0 > f(hi)."""
    lo, hi = np.array(lo, dtype=float), np.array(hi, dtype=float)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        pos = f(mid) > 0
        lo, hi = np.where(pos, mid, lo), np.where(pos, hi, mid)
    return 0.5 * (lo + hi)


def pool_dimensions(field, theta_iso, scale, hatch=None):
    """Depth, width, length (and depth at y = hatch/2) of the isotherm theta_iso of field(x, y, z)."""
    big = 60 * scale
    # Front and rear of the surface isotherm on the centre line.
    xf = _bisect_vec(lambda x: field(x, 0.0, 0.0) - theta_iso, [0.0], [big])[0]
    xr = -_bisect_vec(lambda x: field(-x, 0.0, 0.0) - theta_iso, [0.0], [big])[0]
    if field(np.array([0.0]), 0.0, 0.0)[0] < theta_iso:
        return 0.0, 0.0, 0.0, 0.0
    xs = np.linspace(xr, xf, 81)[1:-1]
    inside_c = field(xs, 0.0, 0.0) > theta_iso
    xs_in = xs[inside_c]
    if xs_in.size == 0:
        return 0.0, 0.0, xf - xr, 0.0
    yw = _bisect_vec(lambda y: field(xs_in, y, 0.0) - theta_iso, np.zeros_like(xs_in), np.full_like(xs_in, big))
    zd = _bisect_vec(lambda z: field(xs_in, 0.0, z) - theta_iso, np.zeros_like(xs_in), np.full_like(xs_in, big))
    dh = 0.0
    if hatch is not None and yw.max() > hatch / 2:
        sel = xs_in[yw > hatch / 2]
        dh = float(_bisect_vec(lambda z: field(sel, hatch / 2, z) - theta_iso, np.zeros_like(sel),
                               np.full_like(sel, big)).max())
    return float(zd.max()), float(2 * yw.max()), float(xf - xr), dh


DEFAULT_OPENING = "beam"


def solve_point(m: Material, P, v, r0, T0, table: RayTable, A_override=None, hatch=None, want_pool=True,
                opening=None):
    """Solve one (P, v) point. A_override fixes the total absorbed fraction (keeps the ray-traced split)."""
    opening = opening or DEFAULT_OPENING
    T_b = m.T_w_fixed if m.T_w_fixed is not None else m.T_boil()
    th_b = thermal_state(m, T0, T_b)
    A_flat = table.A_flat if A_override is None else A_override
    # Conduction branch: does the flat surface reach the boiling point?
    xs = np.linspace(-3 * r0, 1.0 * r0, 41)
    theta_c = gaussian_field(xs, 0.0, 0.0, A_flat * P, r0, th_b.k, th_b.kappa, v)
    theta_peak = float(theta_c.max())
    res = Result(mode="conduction", A=A_flat)
    res.T_peak_conduction = T0 + theta_peak
    if theta_peak < th_b.theta_w:
        if want_pool:
            th_l = thermal_state(m, T0, T_b)
            field = lambda x, y, z: gaussian_field(x, y, z, A_flat * P, r0, th_l.k, th_l.kappa, v)  # noqa: E731
            D, W, L, Dh = pool_dimensions(field, th_l.theta_l, r0, hatch)
            res.pool_depth_um, res.pool_width_um, res.pool_length_um, res.pool_Dh_um = D * 1e6, W * 1e6, L * 1e6, Dh * 1e6
            D, W, L, _ = pool_dimensions(field, th_l.theta_s, r0)
            res.pool_depth_solidus_um, res.pool_width_solidus_um, res.pool_length_solidus_um = D * 1e6, W * 1e6, L * 1e6
        return res

    # Keyhole branch. The opening radius a0 is the beam's 1/e^2 radius, as in Lankalapalli et al. 1996
    # (opening="beam", the default). opening="footprint" instead takes the cross-track half-width of the part of
    # the surface that the flat-surface solution would boil. The depth then follows from the wall energy balance.
    if opening == "beam":
        a0 = r0
    else:
        _, W_b, _, _ = pool_dimensions(
            lambda x, y, z: gaussian_field(x, y, z, A_flat * P, r0, th_b.k, th_b.kappa, v), th_b.theta_w, r0)
        a0 = max(W_b / 2, 0.05 * r0)

    def balance(d):
        g, s = a0 / r0, d / a0
        A_kh, A_sf, zc_abs, hits = table(s, g)
        if A_override is not None:
            scale = A_override / max(A_kh + A_sf, 1e-9)
            A_kh, A_sf = A_kh * scale, A_sf * scale
        T_w = wall_temperature(m, a0)
        th = thermal_state(m, T0, T_w)
        wings = surface_wing_sources(a0, r0, A_sf * P)
        zs, q = keyhole_conduction(a0, d, th, v, wings, table.shape)
        Q_c = float(q.sum())
        Q_e = evaporation_power(m, a0, T_w)
        zc_loss = (float((zs * q).sum()) + Q_e * 0.5 * d) / max(Q_c + Q_e, 1e-12) / d
        r1 = (A_kh * P - Q_c - Q_e) / P
        return r1, dict(a0=a0, d=d, A_kh=A_kh, A_sf=A_sf, T_w=T_w, th=th, Q_c=Q_c, Q_e=Q_e, zs=zs, q=q,
                        wings=wings, hits=hits, zc_abs=zc_abs, zc_loss=zc_loss)

    d_lo, d_hi = 1e-3 * a0, 60 * r0
    f_lo, f_hi = balance(d_lo)[0], balance(d_hi)[0]
    if f_lo <= 0:
        d_sol = d_lo
    elif f_hi >= 0:
        d_sol = d_hi
    else:
        d_sol = optimize.brentq(lambda dd: balance(dd)[0], d_lo, d_hi, xtol=1e-9, rtol=1e-6)
    r1, st = balance(d_sol)
    rvec = np.array([r1])
    res.mode = "keyhole"
    res.A = st["A_kh"] + st["A_sf"]
    res.A_keyhole = st["A_kh"]
    res.a0_um, res.d_um = st["a0"] * 1e6, st["d"] * 1e6
    res.Wk_over_Dk = 2 * st["a0"] / st["d"]
    res.T_w = st["T_w"]
    res.Q_cond_W, res.Q_evap_W = st["Q_c"], st["Q_e"]
    res.residual = float(np.abs(rvec).max())
    res.converged = res.residual < 2e-3
    res.hits_per_ray = st["hits"]
    res.zc_abs, res.zc_loss = st["zc_abs"], st["zc_loss"]
    if want_pool:
        th = st["th"]
        wx, wy, wq = st["wings"]
        zs, q = st["zs"], st["q"]

        def field(x, y, z):
            out = point_source_field(x, y, z, zs, q, th.k, th.kappa, v)
            if wq.size:
                out = out + point_source_field(x, y, z, np.zeros_like(wq), wq, th.k, th.kappa, v,
                                               src_x=wx, src_y=wy, surface=True)
            return out

        D, W, L, Dh = pool_dimensions(field, th.theta_l, r0, hatch)
        res.pool_depth_um, res.pool_width_um, res.pool_length_um, res.pool_Dh_um = D * 1e6, W * 1e6, L * 1e6, Dh * 1e6
        D, W, L, _ = pool_dimensions(field, th.theta_s, r0)
        res.pool_depth_solidus_um, res.pool_width_solidus_um, res.pool_length_solidus_um = D * 1e6, W * 1e6, L * 1e6
    return res


# --- materials -------------------------------------------------------------------------------------------


# Liquid Al and Al-Si inputs. Updated from the sources in PROPERTY_SOURCES (see the README for each value).
MW = {"Al": 26.9815385e-3, "Si": 28.0855e-3, "Mg": 24.305e-3}
VALENCE = {"Al": 3, "Si": 4, "Mg": 2}
DENSITY_SOLID = {"Al": 2700.0, "Si": 2330.0, "Mg": 1738.0}

T_B_AL_JANAF = 2790.812  # K
DH_VAP_AL = 294.0e3  # J/mol at T_b
_VAP_B = DH_VAP_AL / (R_GAS * math.log(10))
AL_LIQ = {
    "rho_el": ((0.097 + 1.681e-4 * 933.47) * 1e-6, 1.681e-10, 933.47),  # Leitner 2017 rho_VE, Ohm m
    "drho_el_per_wt_si": 0.675e-8,              # Brandt & Neuer 2007, Ohm m per wt% Si
    "drho_el_per_wt_mg": 0.92e-8,               # Brandt & Neuer 2007, Ohm m per wt% Mg
    "rho_l": (2670.0 - 0.299 * 933.47, 0.299, 933.47),  # Leitner 2017
    "sigma": (0.993, -0.127e-3),                # Leitner 2017, N/m: a + b T
    "L_v": DH_VAP_AL / MW["Al"],
    "vap": (_VAP_B / T_B_AL_JANAF, _VAP_B),     # log10(p/atm) = A - B/T through JANAF's T_b
}

ALLOYS = {
    "alsi10mg": {"label": "AlSi10Mg, 150 °C plate", "slug": "alsi10mg", "wt": {"Al": 89.675, "Si": 10.0, "Mg": 0.325},
                 "T_s": 842.7, "T_l": 868.6, "T0": 423.15, "r0": 40e-6, "hatch": 130e-6, "layer": 30e-6,
                 "A_am": 0.3074, "render": {"P": 250.0, "v": 0.9}},
    "blend": {"label": "BYU blend (Al-24Si), 30 °C plate", "slug": "byu-blend", "wt": {"Al": 75.56, "Si": 24.30, "Mg": 0.14},
              "T_s": 846.7, "T_l": 1019.3, "T0": 303.15, "r0": 45e-6, "hatch": 100e-6, "layer": 30e-6,
              "A_am": 0.3841, "render": {"P": 375.0, "v": 0.4}},
}


def at_fractions(wt):
    n = {e: w / MW[e] for e, w in wt.items()}
    s = sum(n.values())
    return {e: n[e] / s for e in n}


def alloy_material(key: str) -> Material:
    a = ALLOYS[key]
    x = at_fractions(a["wt"])
    wsum = sum(a["wt"].values())
    rho_s = 1.0 / sum((w / wsum) / DENSITY_SOLID[e] for e, w in a["wt"].items())
    M = sum(x[e] * MW[e] for e in x)
    d = pd.read_csv(ENTHALPY_CSV)
    g = d[d["alloy"] == key].sort_values("T_K")
    r0_, s_, Tr = AL_LIQ["rho_el"]
    r0_ = r0_ + AL_LIQ["drho_el_per_wt_si"] * a["wt"]["Si"] + AL_LIQ["drho_el_per_wt_mg"] * a["wt"]["Mg"]
    T_b = AL_LIQ["vap"][1] / (AL_LIQ["vap"][0] - math.log10(1.0 / x["Al"]))
    sigma = AL_LIQ["sigma"][0] + AL_LIQ["sigma"][1] * T_b
    return Material(name=key, x=x, T_s=a["T_s"], T_l=a["T_l"], rho_s=rho_s, k_s=110.0, M=M,
                    z_val=sum(x[e] * VALENCE[e] for e in x), L_v=AL_LIQ["L_v"], sigma=sigma,
                    H_table=(g["T_K"].to_numpy(), g["H_J_per_kg"].to_numpy()),
                    vap_A=AL_LIQ["vap"][0], vap_B=AL_LIQ["vap"][1], x_vol=x["Al"],
                    rho_el=(r0_, s_, Tr), rho_l_fn=AL_LIQ["rho_l"])


# Gan et al. 2021's materials. Thermal properties, T_v, L_v and L_m are their own (Supplementary Data 1);
# the optics need a liquid resistivity near boiling and a valence, which are ours (README).
GAN_OPTICS = {
    "Ti64": {"rho_el": 1.75e-6, "z": 4.0, "M": 46.0e-3, "sigma": 1.4},
    "Al6061": {"rho_el": 0.50e-6, "z": 3.0, "M": 27.0e-3, "sigma": 0.70},
    "SS316": {"rho_el": 1.35e-6, "z": 2.0, "M": 55.9e-3, "sigma": 1.5},
}


def gan_material(row, mat: str) -> Material:
    o = GAN_OPTICS[mat]
    T0 = 293.0
    T_l, T_v = row["Tl-T0"] + T0, row["Tv-T0"] + T0
    vap_B = row["Lv"] * o["M"] / (R_GAS * math.log(10))
    return Material(name=mat, x={}, T_s=T_l - 1.0, T_l=T_l, rho_s=row["rho"], k_s=row["K"], M=o["M"], z_val=o["z"],
                    L_v=row["Lv"], sigma=o["sigma"], cp_const=row["cp"], L_m=row["Lm"], vap_A=vap_B / T_v,
                    vap_B=vap_B, x_vol=1.0, rho_el=(o["rho_el"], 0.0, T_v), rho_l_fn=(row["rho"], 0.0, T_v),
                    T_w_fixed=T_v, k_l_fixed=row["K"])


_TABLES: dict = {}


def optical_index(m: Material, T):
    """Complex index of the liquid at T: Drude from the DC resistivity (default, as the AM module and
    laserbeamFoam do), or with Drude parameters anchored on Krishnan et al.'s measured liquid Al and scaled to
    this alloy and temperature by its resistivity and electron density."""
    if OPTICS == "drude-krishnan" and "Al" in m.x:
        wp2_k, g_k = drude_from_nk(KRISHNAN_AL["n"], KRISHNAN_AL["k"], KRISHNAN_AL["lam"])
        al = Material(name="Al", x={"Al": 1.0}, T_s=933.47, T_l=933.47, rho_s=2700.0, k_s=237.0, M=MW["Al"],
                      z_val=3.0, L_v=AL_LIQ["L_v"], sigma=0.6, rho_el=AL_LIQ["rho_el"], rho_l_fn=AL_LIQ["rho_l"])
        Tk = KRISHNAN_AL["T"]
        gamma = g_k * float(m.rho_el_liq(T)) / float(al.rho_el_liq(Tk))
        wp2 = wp2_k * float(m.electron_density(T)) / float(al.electron_density(Tk))
        return drude_index_params(wp2, gamma)
    return drude_index(float(m.rho_el_liq(T)), float(m.electron_density(T)))


def ray_table(m: Material, shape="cone") -> RayTable:
    T_ref = m.T_w_fixed if m.T_w_fixed is not None else m.T_boil()
    N = optical_index(m, T_ref)
    key = (round(N.real, 4), round(N.imag, 4), shape)
    if key not in _TABLES:
        _TABLES[key] = RayTable(N, shape=shape)
    return _TABLES[key]


# --- AM-module comparisons ---------------------------------------------------------------------------

AM_DIR = REPO / "arroyave-orchid-tools" / "eagar-tsai" / "am-module-inhouse"
CFD_DIR = REPO / "arroyave-orchid-tools" / "keyhole-alternatives" / "cfd"
WK_DK_AM = 0.7


def classify(res: Result, layer: float) -> str:
    if res.mode == "keyhole" and res.Wk_over_Dk <= WK_DK_AM:
        return "keyhole"
    if res.pool_depth_um <= layer * 1e6:
        return "lof"
    if res.pool_Dh_um <= layer * 1e6:
        return "lof_hatch"
    return "none"


def run_maps(out: pathlib.Path, shape="cone", log=print) -> dict:
    summary = {}
    rows = []
    for key, a in ALLOYS.items():
        m = alloy_material(key)
        tab = ray_table(m, shape)
        g = pd.read_csv(AM_DIR / f"{a['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"].reset_index(drop=True)
        for _, r in g.iterrows():
            res = solve_point(m, r["power_W"], r["speed_mm_s"] / 1000.0, a["r0"], a["T0"], tab, hatch=a["hatch"])
            cls = classify(res, a["layer"])
            rows.append({"alloy": key, "P_W": r["power_W"], "v_m_s": r["speed_mm_s"] / 1000.0, "am_class": r["am_class"],
                         "fp_class": cls, **dataclasses.asdict(res)})
        d = pd.DataFrame([rr for rr in rows if rr["alloy"] == key])
        am_kh = d["am_class"] == "keyhole"
        fp_kh = d["fp_class"] == "keyhole"
        summary[key] = {
            "grid_points": int(len(d)), "A_flat": round(tab.A_flat, 4), "T_boil_K": round(m.T_boil(), 1),
            "agree_all_classes": int((d["am_class"] == d["fp_class"]).sum()),
            "agree_keyhole_or_not": int((am_kh == fp_kh).sum()),
            "am_keyholes": int(am_kh.sum()), "fp_keyholes": int(fp_kh.sum()),
            "missed_am_keyholes": int((am_kh & ~fp_kh).sum()), "extra_keyholes": int((fp_kh & ~am_kh).sum()),
            "keyhole_mode_points": int((d["mode"] == "keyhole").sum()),
            "confusion": pd.crosstab(d["am_class"], d["fp_class"]).to_dict(),
            "unconverged": int((~d["converged"]).sum()),
        }
        log(key, json.dumps({k: v for k, v in summary[key].items() if k != "confusion"}))
    pd.DataFrame(rows).to_csv(out / f"fp-map-classes{'' if shape == 'cone' else '-' + shape}.csv", index=False,
                              float_format="%.5g")
    return summary


def boundary_power(m, v, a, tab, P_lo=50.0, P_hi=700.0, test="keyhole", n=14):
    """Lowest power at speed v where the model's class becomes `test` ('keyhole' or 'mode')."""
    def is_kh(P):
        res = solve_point(m, P, v, a["r0"], a["T0"], tab, want_pool=False)
        if test == "mode":
            return res.mode == "keyhole"
        return res.mode == "keyhole" and res.Wk_over_Dk <= WK_DK_AM
    if is_kh(P_lo):
        return P_lo
    if not is_kh(P_hi):
        return float("nan")
    for _ in range(n):
        mid = 0.5 * (P_lo + P_hi)
        if is_kh(mid):
            P_hi = mid
        else:
            P_lo = mid
    return 0.5 * (P_lo + P_hi)


def run_boundaries(out: pathlib.Path, log=print) -> dict:
    res = {}
    rows = []
    for key, a in ALLOYS.items():
        m = alloy_material(key)
        tab = ray_table(m)
        b = pd.read_csv(AM_DIR / f"{a['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        speeds = np.unique(np.round(np.linspace(b["speed_mm_s"].min(), b["speed_mm_s"].max(), 8), -1)) / 1000.0
        for v in speeds:
            P_mode = boundary_power(m, v, a, tab, test="mode")
            P_kh = boundary_power(m, v, a, tab, test="keyhole")
            P_am = float(np.interp(v * 1000, b["speed_mm_s"], b["P_keyhole_W"]))
            rows.append({"alloy": key, "v_m_s": v, "P_keyhole_mode_onset_W": P_mode, "P_keyhole_defect_W": P_kh,
                         "P_keyhole_am_W": P_am})
            log(key, v, round(P_mode, 1), round(P_kh, 1), round(P_am, 1))
        d = pd.DataFrame([r for r in rows if r["alloy"] == key])
        ratio = d["P_keyhole_defect_W"] / d["P_keyhole_am_W"]
        ratio_on = d["P_keyhole_mode_onset_W"] / d["P_keyhole_am_W"]
        res[key] = {"defect_over_am": [round(float(ratio.min()), 3), round(float(ratio.max()), 3)],
                    "onset_over_am": [round(float(ratio_on.min()), 3), round(float(ratio_on.max()), 3)]}
    pd.DataFrame(rows).to_csv(out / "fp-keyhole-boundary-vs-am.csv", index=False, float_format="%.5g")
    return res


def run_points(out: pathlib.Path, log=print) -> dict:
    """The AM module's two renders and the 350 W laserbeamFoam point, against everything else we have."""
    pts = [("alsi10mg", 250.0, 0.9), ("alsi10mg", 350.0, 0.9), ("blend", 375.0, 0.4)]
    rows = []
    for key, P, v in pts:
        a = ALLOYS[key]
        m = alloy_material(key)
        for shape in ("cone", "paraboloid"):
            tab = ray_table(m, shape)
            for label, Aov in [("own absorptivity", None), ("absorptivity fixed at the AM module's", a["A_am"])]:
                res = solve_point(m, P, v, a["r0"], a["T0"], tab, A_override=Aov, hatch=a["hatch"])
                row = {"alloy": key, "P_W": P, "v_m_s": v, "shape": shape, "variant": label,
                       "class": classify(res, a["layer"]), **dataclasses.asdict(res)}
                rows.append(row)
                log(key, P, v, shape, label, {k: (round(val, 3) if isinstance(val, float) else val)
                                              for k, val in row.items() if k in (
                    "mode", "A", "a0_um", "d_um", "Wk_over_Dk", "T_w", "pool_depth_um", "pool_width_um",
                    "pool_length_um", "pool_length_solidus_um", "Q_evap_W", "residual", "class")})
    d = pd.DataFrame(rows)
    d.to_csv(out / "fp-render-points.csv", index=False, float_format="%.5g")
    return {"rows": len(d)}


# --- Gan et al. 2021 X-ray keyhole depths ----------------------------------------------------------------

LANKALAPALLI_C = (2.1995, 6.2962, -0.4994, 0.0461)  # g(Pe) = C1 + C2 Pe + C3 Pe^2 + C4 Pe^3, 0 <= Pe <= 5


def lankalapalli_depth(P_abs, v, a0, k, alpha, dT):
    """Lankalapalli, Tu & Gartner 1996 (J. Phys. D 29, 1831), Eq. 18: depth of a conical keyhole of top radius a0."""
    pe0 = v * a0 / (2 * alpha)
    s = sum(c / (i + 1) * pe0 ** i for i, c in enumerate(LANKALAPALLI_C))
    return P_abs / (k * dT * s)


def run_gan(out: pathlib.Path, cache: pathlib.Path, log=print) -> dict:
    sys.path.insert(0, str(REPO / "scripts"))
    from keyhole_open_models import load_gan  # noqa: E402  (downloads Supplementary Data 1, checks sha256)
    d = load_gan(cache)
    d["material"] = d["group"].str.extract(r"^(\w+)")[0].replace({"Ti6": "Ti64"})
    gan_law = pd.read_csv(REPO / "arroyave-orchid-tools" / "keyhole-alternatives"
                          / "gan2021-xray-keyhole-depths-vs-open-models.csv")
    rows = []
    for i, r in d.iterrows():
        m = gan_material(r, r["material"])
        tab = ray_table(m)
        out_row = {"row": i, "group": r["group"], "material": r["material"], "P_W": r["P"], "v_m_s": r["V"],
                   "r0_um": r["r0"] * 1e6, "eta_gan": r["eta"], "keyhole_depth_measured_um": r["e"] * 1e6,
                   "gan_law_um": float(gan_law.loc[i, "gan_law_um"]), "A_flat_own": tab.A_flat}
        for tag, Aov in [("gan_eta", r["eta"]), ("own_A", None)]:
            res = solve_point(m, r["P"], r["V"], r["r0"], 293.0, tab, A_override=Aov, want_pool=False)
            out_row.update({f"{tag}_mode": res.mode, f"{tag}_A": res.A, f"{tag}_depth_um": res.d_um,
                            f"{tag}_a0_um": res.a0_um, f"{tag}_T_peak_conduction": res.T_peak_conduction})
            out_row[f"lankalapalli_{tag}_um"] = 1e6 * lankalapalli_depth(
                res.A * r["P"], r["V"], r["r0"], r["K"], r["alpha"], r["Tv-T0"])
        rows.append(out_row)
    t = pd.DataFrame(rows)
    t.to_csv(out / "fp-gan2021-xray-keyhole-depths.csv", index=False, float_format="%.5g")
    s = {}
    for mat, gg in list(t.groupby("material", sort=False)) + [("all", t)]:
        meas = gg["keyhole_depth_measured_um"]
        s[mat] = {"n": int(len(gg))}
        for col in ("gan_eta_depth_um", "own_A_depth_um", "lankalapalli_gan_eta_um", "lankalapalli_own_A_um",
                    "gan_law_um"):
            err = gg[col] - meas
            s[mat][col] = {"MAE_um": round(float(err.abs().mean()), 1),
                           "median_ratio": round(float((gg[col] / meas).median()), 2),
                           "median_abs_rel_err_pct": round(float((err.abs() / meas).median() * 100), 1),
                           "R2": round(float(1 - (err ** 2).sum() / ((meas - meas.mean()) ** 2).sum()), 3)}
        s[mat]["own_A_median"] = round(float(gg["own_A_A"].median()), 3)
        s[mat]["eta_gan_median"] = round(float(gg["eta_gan"].median()), 3)
        s[mat]["own_A_vs_eta_median_ratio"] = round(float((gg["own_A_A"] / gg["eta_gan"]).median()), 2)
        s[mat]["conduction_mode_rows_gan_eta"] = int((gg["gan_eta_mode"] == "conduction").sum())
        s[mat]["conduction_mode_rows_own_A"] = int((gg["own_A_mode"] == "conduction").sum())
        log(mat, json.dumps(s[mat]))
    return s


# --- Solyaev et al. 2025 measured AlSi10Mg tracks --------------------------------------------------------

SOLYAEV_CSV = REPO / "arroyave-orchid-tools" / "eagar-tsai" / "alsi10mg-printability-vs-solyaev2025.csv"


def run_solyaev(out: pathlib.Path, log=print) -> dict:
    """Solyaev et al. 2025 (arXiv:2507.23422): keyhole-shaped pools (D/W > 0.75) for P > 220 W and v < 0.8 m/s.

    Beam 2R = 80 um with q ~ exp(-r^2/R^2), so a 1/e^2 radius of sqrt(2) * 40 um; room-temperature plate."""
    m = alloy_material("alsi10mg")
    tab = ray_table(m)
    r0, T0 = math.sqrt(2.0) * 40e-6, 298.15
    df = pd.read_csv(SOLYAEV_CSV)
    sc = df[df["measured_class"].isin(["keyhole", "stable", "lack_of_fusion"])].reset_index(drop=True)
    rows = []
    for _, r in sc.iterrows():
        res = solve_point(m, r["power_w"], r["velocity_m_s"], r0, T0, tab)
        dw = res.pool_depth_um / res.pool_width_um if res.pool_width_um > 0 else 0.0
        rows.append({"P_W": r["power_w"], "v_m_s": r["velocity_m_s"], "measured_class": r["measured_class"],
                     "mode": res.mode, "A": res.A, "keyhole_depth_um": res.d_um, "Wk_over_Dk": res.Wk_over_Dk,
                     "pool_depth_um": res.pool_depth_um, "pool_width_um": res.pool_width_um, "pool_D_over_W": dw})
    t = pd.DataFrame(rows)
    t.to_csv(out / "fp-solyaev2025-alsi10mg.csv", index=False, float_format="%.5g")
    meas = (t["measured_class"] == "keyhole").to_numpy()
    s = {"scored_points": int(len(t)), "measured_keyhole": int(meas.sum())}
    for name, pred in [("pool D/W > 0.75 (the study's own test)", (t["pool_D_over_W"] > 0.75).to_numpy()),
                       ("keyhole Wk/Dk <= 0.7 (the AM module's test)",
                        ((t["mode"] == "keyhole") & (t["Wk_over_Dk"] <= WK_DK_AM)).to_numpy()),
                       ("keyhole mode (flat surface reaches boiling)", (t["mode"] == "keyhole").to_numpy())]:
        s[name] = {"predicted_keyhole": int(pred.sum()), "agree": int((pred == meas).sum()),
                   "missed": int((~pred & meas).sum()), "extra": int((pred & ~meas).sum())}
        log(name, s[name])
    return s


# --- NIST AM-Bench 2022: bare Al 5182 plate, measured absorptance and pool ----------------------------------

AMB2022 = {"P": 473.0, "v": 0.7, "r0": 122.5e-6 / 2, "T0": 293.0, "A_before_keyhole": 0.24, "A_keyhole": 0.43,
           "pool_depth_um": 88.8, "pool_width_um": 326.0}


def al5182_material() -> Material:
    """Al 5182 (Al-4.5Mg): our liquid-Al data with Brandt & Neuer's Mg increment; c_p and L_m from Leitner et al.
    2017; solidus 850 K, liquidus 911 K and k_s 120 W/m/K are approximate handbook values. Mg's own vapour is
    ignored, although at 5 at% it would lower the wall temperature."""
    wt = {"Al": 95.5, "Mg": 4.5}
    x = at_fractions(wt)
    r0_, s_, Tr = AL_LIQ["rho_el"]
    T_b = AL_LIQ["vap"][1] / (AL_LIQ["vap"][0] - math.log10(1.0 / x["Al"]))
    return Material(name="Al5182", x=x, T_s=850.0, T_l=911.0, rho_s=1 / (0.955 / 2700 + 0.045 / 1738), k_s=120.0,
                    M=sum(x[e] * MW[e] for e in x), z_val=sum(x[e] * VALENCE[e] for e in x), L_v=AL_LIQ["L_v"],
                    sigma=AL_LIQ["sigma"][0] + AL_LIQ["sigma"][1] * T_b, cp_const=1127.0, L_m=360e3,
                    vap_A=AL_LIQ["vap"][0], vap_B=AL_LIQ["vap"][1], x_vol=x["Al"],
                    rho_el=(r0_ + AL_LIQ["drho_el_per_wt_mg"] * wt["Mg"], s_, Tr), rho_l_fn=AL_LIQ["rho_l"])


def run_ambench(out: pathlib.Path, log=print) -> dict:
    """Simonds et al. 2024 (doi:10.1007/s40192-023-00336-0), AM-Bench 2022: 473 W, 0.7 m/s, 122.5 um 1/e^2
    diameter, bare plate. Measured absorptance about 0.24 before and 0.43 during the keyhole (read off their
    Fig. 8, +/- 0.01); pool 88.8 +/- 0.4 um deep and 326 +/- 16 um wide (stated in the text)."""
    m = al5182_material()
    a = AMB2022
    rows = []
    for shape in ("cone", "paraboloid"):
        tab = ray_table(m, shape)
        for label, Aov in [("own absorptance", None), ("absorptance fixed at the measured 0.43", a["A_keyhole"])]:
            res = solve_point(m, a["P"], a["v"], a["r0"], a["T0"], tab, A_override=Aov)
            rows.append({"shape": shape, "variant": label, **dataclasses.asdict(res)})
            log("AM-Bench 2022 Al 5182", shape, label, {k: round(rows[-1][k], 3) for k in (
                "A", "d_um", "Wk_over_Dk", "pool_depth_um", "pool_width_um", "pool_depth_solidus_um",
                "pool_width_solidus_um")})
    pd.DataFrame(rows).to_csv(out / "fp-ambench2022-al5182.csv", index=False, float_format="%.5g")
    return {"measured": a, "rows": len(rows)}


# --- figures ----------------------------------------------------------------------------------------------

INK, INK2, GRIDC = "#0b0b0b", "#52514e", "#e6e5e1"
CLASS_COLOURS = {"keyhole": "#2a78d6", "lof": "#eb6834", "lof_hatch": "#1baf7a", "none": "#b9b8b2"}
CLASS_LABELS = {"keyhole": "keyhole", "lof": "lack of fusion", "lof_hatch": "lack of fusion at hatch",
                "none": "no defect"}
MAT_COLOURS = {"Ti64": "#2a78d6", "Al6061": "#eb6834", "SS316": "#1baf7a"}
MAT_MARKERS = {"Ti64": "o", "Al6061": "s", "SS316": "^"}


def _style(ax):
    ax.grid(True, color=GRIDC, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8.5)


def figures(out: pathlib.Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # 1. Absorptance against keyhole aspect ratio, for the two shapes and both alloys' optics.
    fig, ax = plt.subplots(figsize=(7.2, 5.0), constrained_layout=True)
    for key, ls in [("blend", "-"), ("alsi10mg", ":")]:
        m = alloy_material(key)
        for shape, col in [("cone", "#2a78d6"), ("paraboloid", "#eb6834")]:
            tab = ray_table(m, shape)
            j = int(np.argmin(np.abs(tab.G - 1.0)))
            ax.plot(tab.S / 2, tab.Akh[:, j] + tab.Asf[:, j], ls=ls, color=col, lw=2,
                    label=f"{shape}, {ALLOYS[key]['label'].split(',')[0]} (flat {tab.A_flat:.2f})")
    ti = Material(name="Ti64", x={}, T_s=1878.0, T_l=1923.0, rho_s=3920.0, k_s=33.4, M=GAN_OPTICS["Ti64"]["M"],
                  z_val=GAN_OPTICS["Ti64"]["z"], L_v=9.255e6, sigma=1.4, cp_const=830.0,
                  rho_el=(GAN_OPTICS["Ti64"]["rho_el"], 0.0, 3560.0), rho_l_fn=(3920.0, 0.0, 3560.0), T_w_fixed=3560.0)
    tab = ray_table(ti, "cone")
    j = int(np.argmin(np.abs(tab.G - 1.0)))
    ax.plot(tab.S / 2, tab.Akh[:, j] + tab.Asf[:, j], color=INK2, lw=1.5, label=f"cone, Ti-6Al-4V (flat {tab.A_flat:.2f})")
    ax.axhspan(0.66, 0.84, color=GRIDC, alpha=0.7, lw=0)
    ax.text(0.012, 0.815, "Simonds et al. 2021: Ti-6Al-4V keyholes, measured 0.66–0.84", color=INK2, fontsize=7.5)
    ax.scatter([0.012], [0.33], marker="s", s=30, color=INK2, zorder=5)
    ax.text(0.015, 0.30, "measured, Ti-6Al-4V conduction (0.33)", color=INK2, fontsize=7.5)
    ax.scatter([211 / 102], [0.658], marker="D", s=60, color=INK, zorder=5, label="laserbeamFoam, blend, 65 µΩ cm")
    ax.axhline(0.384, color=INK2, lw=1, ls="--")
    ax.text(0.012, 0.395, "AM module's A at the blend render (0.38)", color=INK2, fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("keyhole depth / opening width, d / (2 a0)", color=INK)
    ax.set_ylabel("absorbed fraction of the beam", color=INK)
    ax.set_ylim(0, 1)
    _style(ax)
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    ax.set_title("Ray-traced absorptance of a Gaussian beam in the keyhole (a0 = r0)", fontsize=10, color=INK)
    fig.savefig(out / "fp-absorptance-vs-aspect-ratio.png", dpi=150)
    plt.close(fig)

    # 2. Gan et al.'s X-ray keyhole depths against the model.
    t = pd.read_csv(out / "fp-gan2021-xray-keyhole-depths.csv")
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 9.4), constrained_layout=True, sharex=True, sharey=True)
    axes = axes.ravel()
    for ax, (col, title) in zip(axes, [("own_A_depth_um", "This model, its own ray-traced absorptance"),
                                       ("gan_eta_depth_um", "This model, given Gan et al.'s absorptivity"),
                                       ("lankalapalli_gan_eta_um", "Lankalapalli et al. 1996 (2D slices), Gan's absorptivity"),
                                       ("gan_law_um", "Gan et al.'s depth law (fitted to these data)")]):
        for mat in ("Ti64", "Al6061", "SS316"):
            g = t[t["material"] == mat]
            ax.scatter(g["keyhole_depth_measured_um"], g[col], s=26, marker=MAT_MARKERS[mat],
                       color=MAT_COLOURS[mat], edgecolor="white", lw=0.6, label=mat, zorder=3)
        lim = [5, 1500]
        ax.plot(lim, lim, color=INK2, lw=1)
        ax.fill_between(lim, [x / 1.5 for x in lim], [x * 1.5 for x in lim], color=GRIDC, alpha=0.5, lw=0)
        ax.set_xscale("log"), ax.set_yscale("log"), ax.set_xlim(lim), ax.set_ylim(lim)
        ax.set_title(title, fontsize=9.5, color=INK)
        ax.set_xlabel("measured keyhole depth (µm, X-ray)", color=INK)
        _style(ax)
    for ax in (axes[0], axes[2]):
        ax.set_ylabel("predicted keyhole depth (µm)", color=INK)
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.suptitle("Gan et al. 2021 X-ray keyhole depths; the grey band is within a factor 1.5", fontsize=10, color=INK)
    fig.savefig(out / "fp-gan2021-xray-depths.png", dpi=130)
    plt.close(fig)

    # 3. The AM module's maps, with this model's classes and keyhole boundary.
    d = pd.read_csv(out / "fp-map-classes.csv")
    bnd = pd.read_csv(out / "fp-keyhole-boundary-vs-am.csv") if (out / "fp-keyhole-boundary-vs-am.csv").exists() else None
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.0), layout="constrained")
    for ax, key in zip(axes, ALLOYS):
        g = d[d["alloy"] == key]
        for cls, col in CLASS_COLOURS.items():
            sel = g[g["fp_class"] == cls]
            ax.scatter(sel["v_m_s"] * 1000, sel["P_W"], s=120, color=col, edgecolor="white", lw=0.8, zorder=3,
                       label=f"this model: {CLASS_LABELS[cls]}")
        dis = g[g["fp_class"] != g["am_class"]]
        ax.scatter(dis["v_m_s"] * 1000, dis["P_W"], s=26, marker="x", color=INK, lw=1.1, zorder=4,
                   label="AM module disagrees")
        b = pd.read_csv(AM_DIR / f"{ALLOYS[key]['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        ax.plot(b["speed_mm_s"], b["P_keyhole_W"], color=INK, lw=2, label="AM module keyhole boundary")
        if bnd is not None:
            bb = bnd[bnd["alloy"] == key]
            ax.plot(bb["v_m_s"] * 1000, bb["P_keyhole_defect_W"], color="#2a78d6", lw=2, ls="--",
                    label="this model: Wk/Dk = 0.7")
            ax.plot(bb["v_m_s"] * 1000, bb["P_keyhole_mode_onset_W"], color=INK2, lw=1.2, ls=":",
                    label="this model: surface reaches boiling")
        ax.set_xlabel("scan speed (mm/s)", color=INK)
        ax.set_ylabel("laser power (W)", color=INK)
        ax.set_title(ALLOYS[key]["label"], fontsize=10, color=INK)
        _style(ax)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="outside lower center", ncol=4, frameon=False, fontsize=8)
    fig.savefig(out / "fp-maps-vs-am-module.png", dpi=140)
    plt.close(fig)


# --- command line ----------------------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["all", "point", "figures", "ambench"])
    ap.add_argument("--out", type=pathlib.Path, default=FP_DIR)
    ap.add_argument("--cache", type=pathlib.Path, default=pathlib.Path("/tmp/keyhole-open-models-cache"))
    ap.add_argument("--alloy", choices=list(ALLOYS), default="blend")
    ap.add_argument("--P", type=float, default=375.0)
    ap.add_argument("--v", type=float, default=0.4)
    ap.add_argument("--shape", choices=list(SHAPES), default="cone")
    ap.add_argument("--opening", choices=["beam", "footprint"], default="beam")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "point":
        al = ALLOYS[a.alloy]
        m = alloy_material(a.alloy)
        res = solve_point(m, a.P, a.v, al["r0"], al["T0"], ray_table(m, a.shape), hatch=al["hatch"], opening=a.opening)
        print(json.dumps({"class": classify(res, al["layer"]), **dataclasses.asdict(res)}, indent=1))
        return
    if a.cmd == "figures":
        figures(a.out)
        return
    if a.cmd == "ambench":
        run_ambench(a.out)
        return
    t0 = time.time()
    logf = open(a.out / "fp-run.log", "w")

    def log(*x):
        line = " ".join(str(y) for y in x)
        print(line, flush=True)
        logf.write(line + "\n")

    summary = {"property_sources": PROPERTY_SOURCES, "materials": {}}
    for key in ALLOYS:
        m = alloy_material(key)
        T_b = m.T_boil()
        N = drude_index(float(m.rho_el_liq(T_b)), float(m.electron_density(T_b)))
        kb, cb = m.means(ALLOYS[key]["T0"], T_b)
        summary["materials"][key] = {
            "T_boil_K": round(T_b, 1), "rho_el_liquid_at_T_boil_uOhm_cm": round(float(m.rho_el_liq(T_b)) * 1e8, 1),
            "n_plus_ik": [round(N.real, 3), round(N.imag, 3)], "A_flat": round(float(fresnel_absorptance(N, 1.0)), 4),
            "k_bar_W_m_K": round(kb, 1), "c_bar_J_kg_K": round(cb, 1), "rho_s_kg_m3": round(m.rho_s, 1),
            "valence": round(m.z_val, 3), "x_Al": round(m.x["Al"], 4)}
        log(key, summary["materials"][key])
    summary["gan2021_xray_depths"] = run_gan(a.out, a.cache, log)
    summary["am_maps"] = run_maps(a.out, log=log)
    summary["am_keyhole_boundary"] = run_boundaries(a.out, log=log)
    run_points(a.out, log=log)
    summary["solyaev2025_alsi10mg"] = run_solyaev(a.out, log=log)
    summary["ambench2022_al5182"] = run_ambench(a.out, log=log)
    # Sensitivity: the other opening closure, on the X-ray depths and the maps.
    global DEFAULT_OPENING, OPTICS
    sens = a.out / "sensitivity-footprint-opening"
    sens.mkdir(exist_ok=True)
    DEFAULT_OPENING = "footprint"
    try:
        summary["sensitivity_footprint_opening"] = {"gan2021_xray_depths": run_gan(sens, a.cache, log),
                                                    "am_maps": run_maps(sens, log=log)}
    finally:
        DEFAULT_OPENING = "beam"
    # Sensitivity: optics anchored on Krishnan et al.'s measured liquid Al instead of the DC resistivity.
    sens = a.out / "sensitivity-measured-optics"
    sens.mkdir(exist_ok=True)
    OPTICS = "drude-krishnan"
    try:
        mats = {}
        for key in ALLOYS:
            m = alloy_material(key)
            N = optical_index(m, m.T_boil())
            mats[key] = {"n_plus_ik": [round(N.real, 3), round(N.imag, 3)],
                         "A_flat": round(float(fresnel_absorptance(N, 1.0)), 4)}
        log("measured-optics", mats)
        summary["sensitivity_measured_optics"] = {"materials": mats, "am_maps": run_maps(sens, log=log),
                                                  "am_keyhole_boundary": run_boundaries(sens, log=log)}
        run_points(sens, log=log)
    finally:
        OPTICS = "drude-dc"
    figures(a.out)
    summary["runtime_s"] = round(time.time() - t0, 1)
    (a.out / "fp-summary.json").write_text(json.dumps(summary, indent=1, default=str) + "\n")
    log("done in", summary["runtime_s"], "s")


if __name__ == "__main__":
    main()
