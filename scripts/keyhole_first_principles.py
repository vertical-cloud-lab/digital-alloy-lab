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
L0_WF = 2.443e-8  # Sommerfeld value of the Lorenz number, W Ohm / K^2
LAMBDA = 1.07e-6  # fibre laser wavelength, m

# --- material properties ----------------------------------------------------------------------------
# Every number used below, with where it comes from. The README repeats this table with full citations.
PROPERTY_SOURCES = {
    "al_vapour_pressure": "Alcock, Itkin & Horrigan 1984, Can. Metall. Q. 23, 309: log10(p/atm) = 5.911 - 16211/T "
                          "for liquid Al (gives 1 atm at 2743 K)",
    "al_enthalpy_vaporisation": "NIST-JANAF / CRC: 294 kJ/mol at the normal boiling point",
    "al_liquid_resistivity": "Leitner et al. 2017, Metall. Mater. Trans. A 48, 3036 (liquid Al, pulse heating)",
    "al_liquid_density": "Assael et al. 2006, J. Phys. Chem. Ref. Data 35, 285",
    "al_si_surface_tension": "Kobatake et al. 2015, J. Mater. Sci. 50, 3351 (Al-Si liquids)",
    "alloy_enthalpy": "pycalphad 0.11.2 equilibrium with MatCalc mc_al v2.032 (scripts/keyhole_fp_enthalpy_mc_al.py)",
    "alloy_liquidus_solidus": "MatCalc mc_al v2.032 via pycalphad (arroyave-orchid-tools/pycalphad-al-cu)",
    "solid_conductivity": "110 W/m/K, the AlSi10Mg value used in #238",
    "solid_density": "rule of mixtures from Al 2700 and Si 2330 kg/m^3 (CRC Handbook)",
    "valence": "free electrons per atom: Al 3, Si 4, Mg 2",
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
        shape = (self.S.size, self.G.size)
        self.Akh = np.zeros(shape)
        self.Asf = np.zeros(shape)
        self.zc = np.zeros(shape)
        self.hits = np.zeros(shape)
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


def solve_point(m: Material, P, v, r0, T0, table: RayTable, A_override=None, hatch=None, want_pool=True):
    """Solve one (P, v) point. A_override fixes the total absorbed fraction (keeps the ray-traced split)."""
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

    # Keyhole branch.
    def balance(logs):
        a0, d = r0 * math.exp(logs[0]), r0 * math.exp(logs[1])
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
        r2 = zc_abs - zc_loss
        return np.array([r1, r2]), dict(a0=a0, d=d, A_kh=A_kh, A_sf=A_sf, T_w=T_w, th=th, Q_c=Q_c, Q_e=Q_e,
                                        zs=zs, q=q, wings=wings, hits=hits)

    best = None
    for g0, s0 in [(1.0, 1.0), (0.8, 3.0), (1.3, 0.4), (0.6, 8.0)]:
        sol = optimize.least_squares(lambda u: balance(u)[0], x0=[math.log(g0), math.log(g0 * s0)],
                                     bounds=([math.log(0.25), math.log(0.005)], [math.log(3.0), math.log(60.0)]),
                                     xtol=1e-10, ftol=1e-12, max_nfev=200)
        if best is None or sol.cost < best.cost:
            best = sol
        if sol.cost < 1e-8:
            break
    rvec, st = balance(best.x)
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
