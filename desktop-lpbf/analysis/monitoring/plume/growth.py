"""How far the condensate grows while it is still in the beam, and what that costs the 1070 nm beam and adds to the coaxial
signal (issue #260; monitoring/plume.md §3.4 and §3.6).

One Lagrangian parcel rides the centreline of the vapour jet, from the depression wall up through the bed's cross-flow and on
into the bed jet, for 1 s. Along the way:

Jet (beam frame; the beam is the vertical line through the source). Top-hat integral jet in a cross-flow (Lee & Cheung 1990,
J. Environ. Eng. 116:1085-1106; Lee & Chu 2003, Turbulent Jets and Plumes: A Lagrangian Approach): mass, x- and z-momentum and
enthalpy fluxes along the trajectory, with entrainment
    dm/ds = 2 pi b rho_a [alpha_s |u - U cos(theta)| + alpha_n U |sin(theta)|]
alpha_s = 0.08 (top-hat; reproduces Ricou & Spalding's measured m/m0 = 0.32 (z/d) (rho_a/rho_j)^0.5, J. Fluid Mech. 11:21-32,
1961) and alpha_n = 0.6 (cross-flow entrainment, Lee & Cheung 1990; Hoult, Fay & Forney 1969). The cross-flow U is the bed jet's
profile at 200 + 40 or 140 + 30 L/min (gas-flow.md §0.5: 2.20 / 2.94 m/s and 1.40 / 2.03 m/s at 1 / 3 mm) combined with the scan
speed (perpendicular scan: |U_rel| = sqrt(U^2 + v^2)). Exit state from worker A's plume_source.json ('wall' Knight jump:
speed, temperature, density); the mass leaving is A's 'best' (measured Mg and Zn losses plus the wall reading's Al), so the
jet's diameter is d0 = sqrt(4 m / (pi rho_v u0)). The enthalpy balance carries the latent heat the condensate releases and the
beam power the particles absorb. Gaussian profiles are 2x the top-hat value on the centreline, with b_g = b / sqrt 2.

Aerosol (discrete-sectional; Wu & Flagan 1988, J. Colloid Interface Sci. 123:339; the volume-conserving
semi-implicit coagulation of Jacobson et al. 1994, Atmos. Environ. 28:1327, as in Jacobson 2005, eq. 15.8). Section 0 is the monomer (the
vapour of the condensate's least volatile species), sections grow by 2x in volume up to ~4 um. Nucleation and condensation are
monomer collisions; clusters lose monomers by Kelvin-enhanced evaporation (capillarity approximation, the particle's own
temperature), so the nucleation rate follows from the cluster's surface tension (liquid Al: 0.871 - 1.55e-4 (T - 933) N/m,
Keene 1993, Int. Mater. Rev. 38:157). Collisions: Fuchs's kernel (Seinfeld & Pandis 2016, Table 13.1) from free-molecular to
continuum, for fractal agglomerates of collision diameter d_c = d_p (n_p / k_f)^(1/D_f), D_f = 1.8, k_f = 1.3 (DLCA;
Sorensen 2011, Aerosol Sci. Technol. 45:765). Primary size: one primary diameter for the whole aerosol, d_p = 6V/A, with the
excess surface area relaxing at the sintering time tau = 3 k T N / (64 pi sigma D) (Koch & Friedlander 1990, J. Colloid
Interface Sci. 140:419; Kruis et al. 1993, Aerosol Sci. Technol. 19:514), D = Al self-diffusion 1.71e-4 exp(-142.3 kJ/RT)
m2/s (Lundy & Murdock 1962, J. Appl. Phys. 33:1671); instant while liquid, with the melting point lowered by
Gibbs-Thomson (sigma_sl 0.15 J/m2, Gunduz & Hunt 1985). The second species (Mg over AlSi10Mg and 6061, Zn over 7075) condenses
on the particles when supersaturated (equilibrium). Oxidation: O2 entrained with the argon reacts on collision with the
particles (gamma = 1 nominal), so it is limited by how much O2 the jet has entrained.

Beam. Each particle in the beam (w0 48 um, M^2 1.1) absorbs C_abs I and loses heat to the argon by free-molecular conduction
(thermal accommodation 0.3, within the 0.1-0.4 of metal and soot particles in Ar/N2 reviewed by Michelsen et al. 2015, Prog.
Energy Combust. Sci. 51:2) and by evaporation; its temperature sets its evaporation, sintering and emission.

Optics. Compact particles: Mie (miepython). Agglomerates: RDG-FA (Dobbins & Megaridis 1991, Appl. Opt. 30:4747; Sorensen 2001,
Aerosol Sci. Technol. 35:648): absorption n_p C_abs(d_p), scattering n_p^2 C_sca(d_p) (1 + 4 k^2 Rg^2 / (3 D_f))^(-D_f/2).
Metallic Al (nominal 'damped'): Rakic 1995 (n, k) plus the Drude damping of electron scattering at the particle's surface
(v_F / r, Kreibig & Vollmer 1995) and, when molten, of liquid Al's 24.2 uOhm cm (Desai et al. 1984, J. Phys. Chem. Ref. Data
13:1131); 'rakic' keeps bulk room-temperature Al. Oxide (Al2O3, MgO, ZnO): n 1.665, k 0 (Boidin et al.
2016), or Wahl et al. 2026's k = 0.019. 7075's Mg/Zn condensate takes aluminium's optics (pessimistic, plume.md §4.2).
The beam's loss is the extinction integrated up the beam axis through the jet; the coaxial emission is the absorption
coefficient times the Planck function at each particle's temperature, integrated the same way. Above the height where the
centreline leaves the beam, the condensate that crosses the beam is heated there too: by default it evaporates during its
transit 2w / v at the Hertz-Knudsen rate (Kelvin included), but only until the gas around it holds the vapour in
equilibrium with the hot particles; 'vacuum' drops that cap, False keeps it all.

Run:  /tmp/capmem 2 env OMP_NUM_THREADS=1 /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/growth.py
Writes analysis/out/monitoring/plume/growth.json, growth_sizes.png and growth_loss.png.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import pathlib
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
SRC = HERE.parents[1] / "out" / "monitoring" / "melt" / "plume_source.json"
RADIO = HERE.parents[1] / "out" / "monitoring" / "optics" / "radiometry.json"

KB, NA, R, ATM = 1.380649e-23, 6.02214076e23, 8.314462, 101325.0
HP, C0, G = 6.62607015e-34, 2.99792458e8, 9.81
M_AR, CP_AR = 39.948e-3, 520.3
M_O2 = 31.998e-3
DEBUG = bool(__import__("os").environ.get("GROWTH_DEBUG"))
P_AMB = 102825.0                                     # +15 mbar argon (plume_source.json p_amb_Pa)

# condensing species: molar mass, solid density, normal boiling point and enthalpy of vaporisation there (CRC Handbook, as in
# plume_jet.py), melting point, liquid surface tension at Tm and its slope (Keene 1993; Mg and Zn to ~10 %), O atoms per atom
# in its oxide, liquid heat capacity
SPECIES = {
    "Al": dict(M=26.982e-3, rho=2700.0, Tb=2792.0, dHv=294.0e3, Tm=933.5, s0=0.871, ds=-1.55e-4, ox=1.5, cp=1180.0),
    "Mg": dict(M=24.305e-3, rho=1740.0, Tb=1363.0, dHv=127.4e3, Tm=923.0, s0=0.559, ds=-1.3e-4, ox=1.0, cp=1360.0),
    "Zn": dict(M=65.38e-3, rho=7140.0, Tb=1180.0, dHv=115.3e3, Tm=692.7, s0=0.782, ds=-1.7e-4, ox=1.0, cp=480.0),
}
SIGMA_SL, DHF_AL = 0.15, 3.97e5                      # Al solid-liquid interface energy (J/m2), heat of fusion (J/kg)
D0_AL, QD_AL = 1.71e-4, 142.3e3                      # Al self-diffusion (Lundy & Murdock 1962)

# Rakic (1995) Al n, k (lambda in um), as in plume_jet.py
AL_NK = np.array([
    (0.61993, 1.3660, 7.4052), (0.65225, 1.5724, 7.7354), (0.68881, 1.8301, 8.0601), (0.72932, 2.1606, 8.3565),
    (0.77491, 2.6154, 8.4914), (0.79478, 2.7675, 8.3866), (0.81569, 2.7668, 8.2573), (0.83774, 2.6945, 8.1878),
    (0.88561, 2.2802, 8.1134), (0.91166, 1.9739, 8.3058), (0.93928, 1.6784, 8.5970), (0.96863, 1.4867, 9.0655),
    (0.99988, 1.4359, 9.4939), (1.0332, 1.3998, 9.8914), (1.1271, 1.3281, 10.969), (1.2399, 1.3157, 12.245)])
BANDS = {"1070": 1.07, "700": 0.70, "900": 0.90, "975": 0.975}   # beam, PD-A 700/40, PD-B 900/40, camera 955-990 nm

# machine (monitoring.md, gas-flow.md §0.5, optics.md)
W0, M2, LAM = 48e-6, 1.1, 1.07e-6                    # beam waist radius (96 um 1/e2 spot), assumed M^2 of a single-mode laser
ZR = math.pi * W0 ** 2 / (M2 * LAM)
FLOWS = {"200+40 L/min": (2.20, 2.94), "140+30 L/min": (1.40, 2.03), "no gas flow": (0.0, 0.0)}
CS_PLATE = 200.0                                     # s/m3: CFD concentration per unit source over the plate, z 0-20 mm (plume.md §1.2: 130-240)
CS_AXIS = (22.0, 270.0)                              # s/m3 along the beam axis, z 20-120 mm, released 0.5-5 / 5-20 mm (plume.md §1.2)

NOMINAL = dict(alpha_s=0.08, alpha_n=0.6, Df=1.8, kf=1.3, stick=1.0, sinter=1.0, sigma_f=1.0, mdot_f=1.0, o2_ppm=100.0,
               gamma_ox=1.0, acc=0.3, optics="damped", ox_k=0.0, Ta=300.0, scan="perpendicular", heating=True,
               jet_mass="best", t_end=1.0, K=44, w0=W0, h_coag=2.0, h_jet=0.05, melt_agg=False, cross_evap=True)


def p_sat(sp, T):
    e = SPECIES[sp]
    return ATM * np.exp(e["dHv"] / R * (1.0 / e["Tb"] - 1.0 / np.asarray(T, float)))


def surf_tension(sp, T):
    e = SPECIES[sp]
    return max(0.2, e["s0"] + e["ds"] * (T - e["Tm"]))


def mu_ar(T):
    return 2.23e-5 * (T / 300.0) ** 0.72             # argon viscosity, power fit to Lemmon & Jacobsen 2004 (300-2000 K, ~3 %)


def k_ar(T):
    return 3.75 * R / M_AR * mu_ar(T)                # monatomic gas: k = (15/4)(R/M) mu


# ---------------------------------------------------------------------------------------------------------------- optics
def al_eps(lam_um):
    n = np.interp(lam_um, AL_NK[:, 0], AL_NK[:, 1])
    k = np.interp(lam_um, AL_NK[:, 0], AL_NK[:, 2])
    return complex(n, k) ** 2


def drude(gamma, w, wp):
    return 1.0 - wp ** 2 / (w ** 2 + 1j * gamma * w)


def al_eps_damped(lam_um, d, molten):
    """Rakic's room-temperature Al plus the extra Drude damping of electron scattering at the surface of a particle of diameter
    d (v_F / r, v_F 2.03e6 m/s, A = 1; Kreibig & Vollmer 1995) and, if molten, of liquid Al's resistivity (24.2 uOhm cm at the
    melting point against 2.65 at 293 K; Desai et al. 1984)."""
    w = 2 * math.pi * C0 / (lam_um * 1e-6)
    wp = 2.25e16                                       # free-electron plasma frequency of Al (3 electrons per atom)
    g_rt = 8.854e-12 * wp ** 2 * 2.65e-8
    g = (8.854e-12 * wp ** 2 * 24.2e-8 if molten else g_rt) + 2.03e6 / max(d / 2, 1e-10)
    return al_eps(lam_um) + drude(g, w, wp) - drude(g_rt, w, wp)


_CACHE = {}


def cached(cls, *args):
    key = (cls.__name__,) + args
    if key not in _CACHE:
        _CACHE[key] = cls(*args)
    return _CACHE[key]


class Optics:
    """Mie efficiencies on a diameter grid for each band: metallic Al (Rakic or hot) and oxide."""

    def __init__(self, kind="damped", ox_k=0.0):
        import miepython
        self.kind = kind
        self.d = np.logspace(math.log10(0.2e-9), math.log10(8e-6), 160)
        self.tab = {}
        for b, lam in BANDS.items():
            for mat in ("metal", "metal_hot", "oxide"):
                qa, qs = np.zeros_like(self.d), np.zeros_like(self.d)
                for i, d in enumerate(self.d):
                    if mat.startswith("metal"):
                        eps = al_eps(lam) if kind == "rakic" else al_eps_damped(lam, d, mat == "metal_hot")
                        m = np.sqrt(eps)
                        m = complex(m.real, -abs(m.imag))
                    else:
                        m = complex(1.665, -ox_k)
                    qe, qsc, _, _ = miepython.efficiencies(m, d * 1e6, lam)
                    qa[i], qs[i] = float(qe - qsc), float(qsc)
                self.tab[(b, mat)] = (qa * math.pi * self.d ** 2 / 4, qs * math.pi * self.d ** 2 / 4)   # cross-sections, m2

    def cs(self, band, mat, d):
        ca, cs = self.tab[(band, mat)]
        ld = np.log(np.clip(d, self.d[0], self.d[-1]))
        return (np.exp(np.interp(ld, np.log(self.d), np.log(np.maximum(ca, 1e-60)))),
                np.exp(np.interp(ld, np.log(self.d), np.log(np.maximum(cs, 1e-60)))))


def section_optics(opt, band, v, dp, f_ox, Df, kf, compact=False, molten=None, melt_agg=False):
    """Absorption and scattering cross-sections (m2) of one particle in each section: compact spheres if v <= v_p, else RDG-FA
    agglomerates of primaries d_p. Metal and oxide mixed by the oxidised volume fraction."""
    d_sph = (6 * v / math.pi) ** (1 / 3)
    vp = math.pi / 6 * dp ** 3
    npri = np.ones_like(v) if compact else np.maximum(v / vp, 1.0)
    lam = BANDS[band] * 1e-6
    k = 2 * math.pi / lam
    out_a, out_s = np.zeros_like(v), np.zeros_like(v)
    for mat, wgt in (("metal", 1.0 - f_ox), ("oxide", f_ox)):
        if wgt <= 0:
            continue
        ca_s, cs_s = opt.cs(band, mat, d_sph)
        ca_p, cs_p = opt.cs(band, mat, np.array([dp]))
        if mat == "metal" and molten is not None and np.any(molten):
            ca_h, cs_h = opt.cs(band, "metal_hot", d_sph)
            ca_s, cs_s = np.where(molten, ca_h, ca_s), np.where(molten, cs_h, cs_s)
        rg = dp / 2 * (npri / kf) ** (1 / Df)
        gfac = (1 + 4 * k * k * rg * rg / (3 * Df)) ** (-Df / 2)
        agg = npri > 1.0 + 1e-9
        if melt_agg and molten is not None:
            agg = agg & ~molten                         # agglomerates heated past melting ball up into spheres
        ca = np.where(agg, npri * ca_p[0], ca_s)
        cs = np.where(agg, npri ** 2 * cs_p[0] * gfac, cs_s)
        out_a += wgt * ca
        out_s += wgt * cs
    return out_a, out_s


def melting_point(sp, d):
    """Melting point of a particle of diameter d (Gibbs-Thomson; Al's interface energy and heat of fusion for every species)."""
    e = SPECIES[sp]
    return e["Tm"] * (1 - 4 * SIGMA_SL / (DHF_AL * e["rho"] * np.maximum(d, 2e-10)))


def planck(lam_um, T):
    lam = lam_um * 1e-6
    x = np.clip(HP * C0 / (lam * KB * np.asarray(T, float)), 1e-6, 700)
    return 2 * HP * C0 ** 2 / lam ** 5 / np.expm1(x)          # W / (m2 sr m)


# ---------------------------------------------------------------------------------------------------------------- aerosol
class Sections:
    def __init__(self, sp, K):
        self.sp = sp
        e = SPECIES[sp]
        self.m1 = e["M"] / NA
        self.v1 = self.m1 / e["rho"]
        self.K = K
        self.v = self.v1 * 2.0 ** np.arange(K)
        self.d = (6 * self.v / math.pi) ** (1 / 3)
        F = np.zeros((K, K, K))
        for i in range(K):
            for j in range(K):
                V = self.v[i] + self.v[j]
                k = int(np.searchsorted(self.v, V, side="right") - 1)
                if k >= K - 1:
                    F[i, j, K - 1] = 1.0
                    continue
                f = (self.v[k + 1] - V) / (self.v[k + 1] - self.v[k]) * self.v[k] / V
                F[i, j, k] = f
                F[i, j, k + 1] = 1.0 - f
        self.F = F
        self.lossF = 1.0 - np.einsum("kjk->kj", F)      # (1 - f_kjk)

    def geometry(self, dp, Df, kf, compact=False):
        """Collision (mobility) diameter and number of primaries per particle in each section (all compact spheres while the
        aerosol is fully sintered)."""
        vp = math.pi / 6 * dp ** 3
        npri = np.ones_like(self.v) if compact else np.maximum(self.v / vp, 1.0)
        dc = np.where(npri > 1.0, np.maximum(dp * (npri / kf) ** (1 / Df), self.d), self.d)
        return dc, npri

    def kernel(self, T, p, dc, stick):
        """Fuchs's coagulation kernel (m3/s) for every pair of sections."""
        rho = SPECIES[self.sp]["rho"]
        mu = mu_ar(T)
        lam_g = 2 * mu / (p * math.sqrt(8 * M_AR / (math.pi * R * T)))
        Kn = 2 * lam_g / dc
        Cc = 1 + Kn * (1.257 + 0.4 * np.exp(-1.1 / Kn))
        D = KB * T * Cc / (3 * math.pi * mu * dc)
        m = rho * self.v
        c = np.sqrt(8 * KB * T / (math.pi * m))
        lp = 8 * D / (math.pi * c)
        g = ((dc + lp) ** 3 - (dc * dc + lp * lp) ** 1.5) / (3 * dc * lp) - dc
        Ds = D[:, None] + D[None, :]
        ds_ = dc[:, None] + dc[None, :]
        gs = np.sqrt(g[:, None] ** 2 + g[None, :] ** 2)
        cs = np.sqrt(c[:, None] ** 2 + c[None, :] ** 2)
        return stick * 2 * math.pi * Ds * ds_ / (ds_ / (ds_ + 2 * gs) + 8 * Ds / (cs * ds_))

    def coagulate(self, n, beta, h):
        """Jacobson's semi-implicit, volume-conserving step. n: number concentrations (m-3)."""
        V_old = n * self.v
        V_new = np.zeros_like(V_old)
        loss = h * (self.lossF * beta) @ n
        for k in range(self.K):
            prod = 0.0
            if k > 0:
                prod = h * (V_new[:k] @ ((self.F[:k, :k + 1, k] * beta[:k, :k + 1]) @ n[:k + 1]))
            V_new[k] = (V_old[k] + prod) / (1.0 + loss[k])
        return V_new / self.v


def particle_temperature(Iw, Tg, p, ca, area, d_evap, sp, sigma_f, acc):
    """Steady temperature of particles in the beam: I C_abs = G (Tp - Tg) + evaporation x latent heat. Vectorised bisection."""
    e = SPECIES[sp]
    m1 = e["M"] / NA
    v1 = m1 / e["rho"]
    cbar = math.sqrt(8 * KB * Tg / (math.pi * M_AR / NA))
    Gfm = acc * p * cbar / (8 * Tg) * 4.0 * area        # (gamma+1)/(gamma-1) = 4 for argon (Filippov & Rosner 2000)
    Gc = 2 * math.pi * k_ar(Tg) * np.sqrt(area / math.pi)
    Gt = 1.0 / (1.0 / Gfm + 1.0 / Gc)
    Pabs = Iw * ca
    lo, hi = np.full_like(ca, Tg), np.full_like(ca, 4500.0)
    lat = e["dHv"] / NA
    for _ in range(26):
        mid = 0.5 * (lo + hi)
        sig = e["s0"] + e["ds"] * (mid - e["Tm"])
        kel = np.exp(np.clip(4 * np.maximum(sig, 0.2) * sigma_f * v1 / (KB * mid * d_evap), 0, 50))
        Ev = area * p_sat(sp, mid) * kel / np.sqrt(2 * math.pi * m1 * KB * mid)
        f = Pabs - Gt * (mid - Tg) - Ev * lat
        lo = np.where(f > 0, mid, lo)
        hi = np.where(f > 0, hi, mid)
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------------------------------------------- source
def source_terms(case, prm):
    """Jet exit and condensable flows from one plume_source.json case."""
    ex = case["exit"].get("wall") or {}
    best = case["best"]
    md = best["m_dot_kg_s"]
    xv = best["vapour_mole_fraction"]
    refr = sum(xv.get(k, 0.0) for k in ("Al", "Si", "Cu"))
    if refr >= 0.3:
        prim, sec = "Al", "Mg"
        m_prim = sum(md.get(k, 0.0) for k in ("Al", "Si", "Cu"))
        m_sec = md.get("Mg", 0.0) + md.get("Zn", 0.0)
    else:
        prim, sec = "Mg", "Zn"
        m_prim = md.get("Mg", 0.0) + sum(md.get(k, 0.0) for k in ("Al", "Si", "Cu"))
        m_sec = md.get("Zn", 0.0)
    f = prm["mdot_f"]
    m_prim, m_sec = m_prim * f, m_sec * f
    m_c = m_prim + m_sec
    m_jet = m_c if prm["jet_mass"] == "best" else case["readings"]["wall"]["m_dot_kg_s"]["total"] * f
    u0 = ex.get("u_m_s") or 0.0
    Tv = ex.get("T_vapour_K") or case["T_wall_K"]
    Mv = (ex.get("M_vapour_g_mol") or 27.0) * 1e-3
    rho_v = P_AMB * Mv / (R * Tv)
    if u0 <= 0:                                        # no Knight jet: the Stefan flow off the beam's spot
        u0 = m_jet / (rho_v * math.pi * prm['w0'] ** 2)
    d0 = math.sqrt(4 * m_jet / (math.pi * rho_v * u0))
    return dict(prim=prim, sec=sec, m_prim=m_prim, m_sec=m_sec, m_c=m_c, m_jet=m_jet, u0=u0, Tv=Tv, Mv=Mv, rho_v=rho_v, d0=d0,
                P_W=case["inputs"]["P_W"], v_scan=case["inputs"]["v_m_s"], alloy=case["inputs"]["alloy"], tag=case["tag"],
                T_wall=case["T_wall_K"])


def cross_flow(z, flow, v_scan, scan):
    u1, u3 = FLOWS[flow]
    if u3 > 0:
        n = math.log(u3 / u1) / math.log(3.0)
        Ug = u3 * min(max(z, 0.2e-3) / 3e-3, 20.0 / 3.0) ** n
    else:
        Ug = 0.0
    if scan == "with flow":
        return abs(Ug - v_scan)
    if scan == "against flow":
        return Ug + v_scan
    return math.hypot(Ug, v_scan)


# ---------------------------------------------------------------------------------------------------------------- run
def run(case, flow="200+40 L/min", P_override=None, **over):
    prm = dict(NOMINAL)
    prm.update(over)
    st = source_terms(case, prm)
    P = P_override or st["P_W"]
    sp, sec = st["prim"], st["sec"]
    S = cached(Sections, sp, prm["K"])
    opt = cached(Optics, prm["optics"], prm["ox_k"])
    w0 = prm["w0"]
    zr = math.pi * w0 ** 2 / (M2 * LAM)
    Ta = prm["Ta"]
    rho_a = P_AMB * M_AR / (R * Ta)
    e, es = SPECIES[sp], SPECIES[sec]
    cp_v = 2.5 * R / st["Mv"]
    x_o2 = prm["o2_ppm"] * 1e-6
    # jet state (top-hat fluxes)
    m = st["m_jet"]
    u0 = st["u0"]
    Fx, Fz = 0.0, m * u0
    x = z = s = 0.0
    m_met = st["m_jet"]                                   # metal in the jet, vapour + condensate (kg/s)
    Hs = m_met * cp_v * (st["Tv"] - Ta) + st["m_c"] * e["dHv"] / e["M"]   # enthalpy flux above Ta, condensable still vapour
    # aerosol, per kg of mixture (top-hat); sections hold all condensed volume, both species
    N = np.zeros(S.K)
    N[0] = st["m_prim"] / st["m_jet"] / S.m1
    Yc = st["m_c"] / st["m_jet"]                          # condensable mass fraction (vapour + condensed)
    Ysv, Ysc = st["m_sec"] / st["m_jet"], 0.0             # second species: vapour, condensed
    nO2, O_used = 0.0, 0.0                                # mol O2 and mol O (in particles) per kg
    ox_need = st["m_prim"] / st["m_jet"] / e["M"] * e["ox"] + st["m_sec"] / st["m_jet"] / es["M"] * es["ox"]
    X = 0.0                                               # excess surface area over the compact-sphere area (m2/kg)
    t, h = 0.0, 2e-11
    rec, snaps = [], []
    t_rec = np.logspace(-8, math.log10(prm["t_end"]), 150)
    t_snap = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0]
    ir = isnap = 0
    phase = "jet"
    absorbed = 0.0
    dp = S.d[1]
    U_gas3 = FLOWS[flow][1]
    cs_bed = CS_PLATE * 2.95 / max(U_gas3, 0.25)          # bed-jet dilution; with no gas flow, ~0.25 m/s of convection
    wall0 = time.time()
    steps = 0
    tp_key, Tp_cache = None, None
    stable = S.d >= 1e-9
    compact = True
    rho, conc_f, Tg, u, b, th, w, in_beam, Iw, f_ox = rho_a, 1.0, st["Tv"], u0, st["d0"] / 2, math.pi / 2, w0, True, 0.0, 0.0
    while t < prm["t_end"] and steps < prm.get("max_steps", 10**9):
        steps += 1
        if DEBUG and steps % 200 == 0:
            print(f"  step {steps} t {t:.3e} h {h:.2e} z {z*1e3:.4f} mm x {x*1e3:.4f} Tg {Tg:.0f} dp {dp*1e9:.2f} phase {phase} N0 {N[0]:.2e} Nsum {N[1:].sum():.2e}", flush=True)
        U = cross_flow(z, flow, st["v_scan"], prm["scan"])
        Vsec = Ysc / es["rho"]
        cond_mass = (float(np.sum(N * S.v * stable)) - Vsec) * e["rho"] + Ysc    # particles of 1 nm and up hold their latent heat
        f_cond = min(max(cond_mass / max(Yc, 1e-30), 0.0), 1.0)
        if phase == "jet":
            m_ar = max(m - m_met, 0.0)
            vap_left = st["m_c"] * (1 - f_cond)
            Tg = max(Ta + (Hs - vap_left * e["dHv"] / e["M"]) / (m_ar * CP_AR + m_met * cp_v), Ta)
            gas_met = m_met - st["m_c"] * f_cond
            M_mix = (m_ar + gas_met) / (m_ar / M_AR + gas_met / st["Mv"])
            rho = P_AMB * M_mix / (R * Tg)
            u = math.hypot(Fx, Fz) / m
            th = math.atan2(Fz, Fx)
            b = math.sqrt(m / (math.pi * rho * max(u, 1e-3)))
            conc_f = 1.0 + min(1.0, s / (6 * st["d0"]))     # top-hat at the exit, Gaussian centreline (2x) past the potential core
        else:
            Tg, rho, u, th, b, conc_f = Ta, rho_a, U, 0.0, 0.0, 1.0
        w = w0 * math.sqrt(1 + (z / zr) ** 2)
        in_beam = phase == "jet" and x < w and prm["heating"]
        Iw = 2 * P / (math.pi * w * w) if in_beam else 0.0
        # time step: coagulation of the populated sections, and the jet's own scale
        n = N * rho * conc_f
        dc, npri = S.geometry(dp, prm["Df"], prm["kf"], compact)
        beta = S.kernel(Tg, P_AMB, dc, prm["stick"])
        vol = n * S.v
        pop = vol > 1e-4 * max(vol.sum(), 1e-300)
        pop[0] = False
        lossr = (S.lossF * beta) @ n                     # rate at which each section's particles leave it
        rate = float(np.max(lossr[pop])) if pop.any() else 0.0
        hmax = prm["h_coag"] / rate if rate > 0 else 1e9
        if vol[0] > 1e-3 * max(vol.sum(), 1e-300):        # monomers still hold vapour worth tracking
            hmax = min(hmax, prm["h_coag"] / max(float(beta[0] @ n), 1e-30))
        if phase == "jet":
            hmax = min(hmax, prm["h_jet"] * max(b, 2e-6) / max(u, 1e-3))
        h = max(min(h * 1.06, hmax, max(t, 1e-9) * 0.08, prm["t_end"] - t + 1e-15), 1e-12)
        # --- jet ---
        ds = 0.0
        if phase == "jet":
            ds = u * h
            E = 2 * math.pi * b * rho_a * (prm["alpha_s"] * abs(u - U * math.cos(th)) + prm["alpha_n"] * U * abs(math.sin(th)))
            m_old = m
            m += E * ds
            Fx += E * ds * U
            Fz += G * (rho_a - rho) * math.pi * b * b * ds
            x += math.cos(th) * ds
            z += math.sin(th) * ds
            s += ds
            dil = m_old / m
            N *= dil
            Yc *= dil
            Ysv *= dil
            Ysc *= dil
            O_used *= dil
            ox_need *= dil
            X *= dil
            nO2 = nO2 * dil + (1 - dil) * x_o2 / M_AR
        # --- coagulation (nucleation and condensation of the monomer are collisions too) ---
        n = N * rho * conc_f
        As0 = float(np.sum(n * math.pi * S.d ** 2 * stable))
        n = S.coagulate(n, beta, h)
        X += max(As0 - float(np.sum(n * math.pi * S.d ** 2 * stable)), 0.0) / (rho * conc_f)
        # --- evaporation (Kelvin) at each section's particle temperature ---
        dc, npri = S.geometry(dp, prm["Df"], prm["kf"], compact)
        area = np.where(npri > 1, npri * math.pi * dp ** 2, math.pi * S.d ** 2)
        d_ev = np.where(npri > 1, dp, S.d)
        a_abs_c = 0.0
        if in_beam:
            molten = (Tp_cache if Tp_cache is not None else np.full(S.K, Tg)) > melting_point(sp, d_ev)
            ca, _ = section_optics(opt, "1070", S.v, dp, f_ox, prm["Df"], prm["kf"], compact, molten)
            key = (Tg, dp, Iw)
            if (tp_key is None or abs(Tg - tp_key[0]) > 3.0 or abs(dp / tp_key[1] - 1) > 0.02
                    or abs(Iw / tp_key[2] - 1) > 0.02):
                Tp_cache = particle_temperature(Iw, Tg, P_AMB, ca, area, d_ev, sp, prm["sigma_f"], prm["acc"])
                tp_key = key
            Tp = Tp_cache.copy()
            Tp[0] = Tg
            a_abs_c = float(np.sum(n[1:] * ca[1:] * (S.d[1:] >= 1e-9)))
        else:
            Tp = np.full(S.K, Tg)
        sig = np.maximum(e["s0"] + e["ds"] * (Tp - e["Tm"]), 0.2) * prm["sigma_f"]
        kel = np.exp(np.clip(4 * sig * S.v1 / (KB * Tp * d_ev), 0, 60))
        Ev = area * p_sat(sp, Tp) * kel / np.sqrt(2 * math.pi * S.m1 * KB * Tp)
        Rk = np.zeros(S.K)
        Rk[1] = Ev[1]
        Rk[2:] = Ev[2:] * S.v1 / (S.v[2:] - S.v[1:-1])
        n_new = n / (1 + h * Rk)
        dn = n - n_new
        n_new[1:-1] += dn[2:]
        n_new[0] += 2 * dn[1] + np.sum(dn[2:] * (S.v[2:] - S.v[1:-1]) / S.v1)
        N = np.maximum(n_new, 0.0) / (rho * conc_f)
        # --- second species: equilibrium condensation onto the particles (volume-conserving split) ---
        if Ysv > 0 and N[1:].sum() > 0 and phase == "jet":
            Yeq = float(p_sat(sec, Tg)) * es["M"] / (R * Tg) / (rho * conc_f)
            dY = max(0.0, Ysv - Yeq)
            if dY > 0:
                wts = N[1:-1] * beta[0, 1:-1]
                if wts.sum() > 0:
                    dV = dY / es["rho"] * wts / wts.sum()
                    Nn = N.copy()
                    with np.errstate(divide="ignore", invalid="ignore"):
                        vnew = S.v[1:-1] + np.where(N[1:-1] > 0, dV / np.maximum(N[1:-1], 1e-300), 0.0)
                    j = np.clip(np.searchsorted(S.v, vnew, side="right") - 1, 1, S.K - 2)
                    a = np.clip((S.v[j + 1] - vnew) / (S.v[j + 1] - S.v[j]), 0.0, 1.0)
                    Nn[1:-1] -= N[1:-1]
                    np.add.at(Nn, j, N[1:-1] * a)
                    np.add.at(Nn, j + 1, N[1:-1] * (1 - a))
                    N = Nn
                    Ysv -= dY
                    Ysc += dY
        # --- oxidation by the entrained O2, on collision with the particles ---
        ox_cap = ox_need
        if Tg < 600.0:                                  # cold Al passivates: a ~1 nm oxide shell (Jeurgens et al. 2002)
            ox_cap = ox_need * min(1.0, 1 - max(dp - 2e-9, 0.0) ** 3 / dp ** 3) if dp > 0 else ox_need
            ox_cap = max(ox_cap, O_used)
        if nO2 > 0 and ox_cap > O_used:
            Atot = float(np.sum(N[1:] * area[1:])) * rho * conc_f
            cO2 = math.sqrt(8 * KB * Tg / (math.pi * M_O2 / NA))
            uptake = prm["gamma_ox"] * nO2 * cO2 / 4 * Atot * h       # mol O2 per kg
            dO2 = min(nO2, uptake, (ox_cap - O_used) / 2)
            nO2 -= dO2
            O_used += 2 * dO2
        f_ox = min(O_used / max(ox_need, 1e-30), 1.0)
        # --- sintering of the primaries ---
        Vtot = float(np.sum(N * S.v * stable))
        As = float(np.sum(N * math.pi * S.d ** 2 * stable))
        Tp_prim = float(Tp[1 + int(np.argmax(N[1:] * S.v[1:]))]) if Vtot > 0 else Tg
        Tm_d = e["Tm"] * (1 - 4 * SIGMA_SL / (DHF_AL * e["rho"] * dp))
        if Tp_prim >= Tm_d:
            tau = 1e-12
        else:
            Thom = Tp_prim * SPECIES["Al"]["Tm"] / e["Tm"]             # homologous temperature for Mg- and Zn-rich condensate
            Dd = D0_AL * math.exp(-QD_AL / (R * Thom))
            Nat = math.pi / 6 * dp ** 3 / S.v1
            tau = 3 * KB * Tp_prim * Nat / (64 * math.pi * surf_tension(sp, Tp_prim) * Dd) / prm["sinter"]
        X *= math.exp(-h / max(tau, 1e-15))
        if Vtot > 0:
            dp = min(max(6 * Vtot / (As + X), 1e-9), 5e-6)
        compact = X < 0.02 * As
        # --- beam power absorbed in the jet heats it ---
        if phase == "jet" and in_beam:
            dE = P * a_abs_c * ds
            Hs += dE
            absorbed += dE
        t += h
        # --- into the bed jet once the jet is no denser than it ---
        if phase == "jet":
            c_now = Yc * rho * conc_f
            c_bed = st["m_c"] * cs_bed
            if (c_now < c_bed and x > 5e-3) or x > 0.08:
                fac = (c_bed / c_now) * rho * conc_f / rho_a
                N *= fac
                Yc *= fac
                Ysc *= fac
                Ysv = 0.0
                O_used *= fac
                ox_need *= fac
                X *= fac
                nO2 = x_o2 / M_AR
                phase = "bed"
                rho, conc_f, Tg = rho_a, 1.0, Ta
        while ir < len(t_rec) and t >= t_rec[ir]:
            rec.append(record(S, opt, N, rho, conc_f, dp, prm, t, s, x, z, b, u, th, Tg, Tp_prim, f_ox, f_cond, in_beam, phase,
                              Ysc, st, P, w, compact))
            ir += 1
        while isnap < len(t_snap) and t >= t_snap[isnap]:
            dc, npri = S.geometry(dp, prm["Df"], prm["kf"], compact)
            nn = N * rho * conc_f
            snaps.append(dict(t_s=t, z_mm=z * 1e3, x_mm=x * 1e3, phase=phase, d_p_nm=dp * 1e9, d_c_nm=list(dc * 1e9),
                              d_v_nm=list(S.d * 1e9), n_m3=list(nn), vol_frac=list(nn * S.v / max(float(np.sum(nn[1:] * S.v[1:])), 1e-300))))
            isnap += 1
    res = dict(source=st, flow=flow, P_W=P, params=prm, records=rec, snapshots=snaps, absorbed_in_jet_W=absorbed,
               cpu_s=time.time() - wall0, steps=steps)
    res["beam"] = beam_integrals(res, opt, S)
    return res


def record(S, opt, N, rho, conc_f, dp, prm, t, s, x, z, b, u, th, Tg, Tp, f_ox, f_cond, in_beam, phase, Ysc, st, P, w, compact):
    """State of the parcel, with optics per kg of condensate and per m at the centreline (clusters under 1 nm left out)."""
    e, es = SPECIES[st["prim"]], SPECIES[st["sec"]]
    n = N * rho * conc_f
    ok = (S.d >= 1e-9) & (np.arange(S.K) >= 1)
    Vsec = Ysc * rho * conc_f / es["rho"]
    mass = (float(np.sum(n[1:] * S.v[1:])) - Vsec) * e["rho"] + Ysc * rho * conc_f
    dc, npri = S.geometry(dp, prm["Df"], prm["kf"], compact)
    r = dict(t=t, s_mm=s * 1e3, x_mm=x * 1e3, z_mm=z * 1e3, b_mm=b * 1e3, u=u, T_g=Tg, T_p=Tp, f_ox=f_ox, f_cond=f_cond,
             in_beam=bool(in_beam), phase=phase, d_p_nm=dp * 1e9, C_cond_kg_m3=mass, conc_factor=conc_f, compact=bool(compact))
    wN = n * ok
    r["N_m3"] = float(wN.sum())
    if wN.sum() > 0:
        wM = n * S.v * ok
        r["d_c_mean_nm"] = float(np.exp(np.sum(wN * np.log(dc)) / wN.sum())) * 1e9
        r["d_c_massmedian_nm"] = float(np.exp(np.sum(wM * np.log(dc)) / wM.sum())) * 1e9
        r["n_p_mass_mean"] = float(np.sum(wM * npri) / wM.sum())
        r["d_v_massmean_nm"] = float((np.sum(wM * S.v) / wM.sum() * 6 / math.pi) ** (1 / 3)) * 1e9
    # the particles on the beam axis, heated by the beam there (two passes: molten particles absorb more)
    area = np.where(npri > 1, npri * math.pi * dp ** 2, math.pi * S.d ** 2)
    d_ev = np.where(npri > 1, dp, S.d)
    Iax = 2 * P / (math.pi * w * w) if prm["heating"] else 0.0
    Tm_sec = melting_point(st["prim"], d_ev)
    molten = np.full(S.K, Tg) > Tm_sec
    Tax = np.full(S.K, Tg)
    ma = prm["melt_agg"]
    if Iax > 0 and phase == "jet":
        for _ in range(2):
            ca1070, _ = section_optics(opt, "1070", S.v, dp, f_ox, prm["Df"], prm["kf"], compact, molten, ma)
            if ma:
                sph = molten | (npri <= 1)
                area = np.where(sph, math.pi * S.d ** 2, npri * math.pi * dp ** 2)
                d_ev = np.where(sph, S.d, dp)
            Tax = particle_temperature(Iax, Tg, P_AMB, ca1070, area, d_ev, st["prim"], prm["sigma_f"], prm["acc"])
            molten = Tax > Tm_sec
    r["molten_mass_frac"] = float(np.sum(n * S.v * ok * molten) / max(np.sum(n * S.v * ok), 1e-300))
    # optional: condensate that crosses the beam once the centreline has left it evaporates on the way through. Mass kept,
    # averaged over the transit 2w / v (v: the jet's speed across the beam), for a radius shrinking at the Hertz-Knudsen rate
    # at the particle's temperature (Kelvin included): f = (tau_ev / 4 tau) [1 - (1 - min(tau / tau_ev, 1))^4]
    fsurv = np.ones(S.K)
    if prm["cross_evap"] and phase == "jet" and not in_beam and Iax > 0:
        sig = np.maximum(e["s0"] + e["ds"] * (Tax - e["Tm"]), 0.2) * prm["sigma_f"]
        kel = np.exp(np.clip(4 * sig * S.v1 / (KB * Tax * d_ev), 0, 60))
        rdot = p_sat(st["prim"], Tax) * kel * np.sqrt(e["M"] / (2 * math.pi * R * Tax)) / e["rho"]
        tau_ev = (d_ev / 2) / np.maximum(rdot, 1e-30)
        tau_tr = 2 * w / max(abs(u * math.cos(th)), 0.5)
        x_ = np.minimum(tau_tr / tau_ev, 1.0)
        fsurv = np.clip(tau_ev / (4 * tau_tr) * (1 - (1 - x_) ** 4), 0.0, 1.0)
    r["cross_survival_mass_mean"] = float(np.sum(n * S.v * ok * fsurv) / max(np.sum(n * S.v * ok), 1e-300))
    Tm_ax = max(float(np.sum(n * S.v * ok * Tax) / max(np.sum(n * S.v * ok), 1e-300)), Tg)
    r["rho_vap_eq_axis"] = float(p_sat(st["prim"], Tm_ax)) * math.sqrt(Tg / Tm_ax) * e["M"] / (R * Tg)   # vapour that stops it
    for band in BANDS:
        ca, cs = section_optics(opt, band, S.v, dp, f_ox, prm["Df"], prm["kf"], compact, molten, ma)
        aabs, asca = float(np.sum(n * ca * ok)), float(np.sum(n * cs * ok))
        r[f"a_abs_{band}"], r[f"a_sca_{band}"] = aabs, asca                   # 1/m at the centreline
        r[f"k_abs_{band}"] = aabs / mass if mass > 0 else 0.0                # m2/kg of condensate
        r[f"k_sca_{band}"] = asca / mass if mass > 0 else 0.0
    for band in ("700", "900", "975"):
        ca, _ = section_optics(opt, band, S.v, dp, f_ox, prm["Df"], prm["kf"], compact, molten, ma)
        r[f"j_{band}"] = float(np.sum(n * ca * ok * planck(BANDS[band], Tax)))  # W/(m3 sr m) at the centreline, beam-heated
        r[f"jg_{band}"] = float(np.sum(n * ca * ok * planck(BANDS[band], np.full(S.K, Tg))))   # same particles at the gas temperature
    r["w_mm"] = w * 1e3
    wM = n * S.v * ok
    r["T_axis_mass_mean"] = float(np.sum(wM * Tax) / max(wM.sum(), 1e-300))
    return r


def beam_integrals(res, opt, S):
    """Integrate the centreline coefficients up the beam axis: the point at height z_P = z_c + x_c / tan(theta) lies in the
    cross-section through s, at r = x_c / sin(theta) from the centreline (Gaussian, b_g = b / sqrt 2)."""
    jr = [r for r in res["records"] if r["phase"] == "jet"]
    if len(jr) < 3:
        return {}
    xs = np.array([r["x_mm"] for r in jr]) * 1e-3
    zs = np.array([r["z_mm"] for r in jr]) * 1e-3
    bs = np.array([max(r["b_mm"], 1e-6) for r in jr]) * 1e-3
    # angle from successive points
    dx, dz = np.gradient(xs), np.gradient(zs)
    th = np.arctan2(dz, np.maximum(dx, 1e-12))
    th = np.where(th <= 1e-6, 1e-6, th)
    zP = zs + xs / np.tan(th)
    rr = xs / np.sin(th)
    wprof = np.exp(-(rr / (bs / math.sqrt(2))) ** 2)
    mode = res["params"]["cross_evap"]
    if mode:
        # condensate crossing the beam after the centreline has left it: mass kept on the axis. 'vacuum': evaporating at the
        # Hertz-Knudsen rate into vapour-free gas; True: capped by the vapour the gas at the axis can hold against the hot
        # particles (rho_eq), so the dense core keeps most of its condensate and the dilute edge loses it
        sv = np.array([r.get("cross_survival_mass_mean", 1.0) for r in jr])
        ceq = np.array([r.get("rho_vap_eq_axis", 0.0) for r in jr])
        cax = np.array([r["C_cond_kg_m3"] for r in jr]) * wprof
        keep = sv if mode == "vacuum" else np.maximum(sv, 1 - ceq / np.maximum(cax, 1e-30))
        keep = np.where([r["in_beam"] for r in jr], 1.0, np.clip(keep, 0.0, 1.0))
        wprof = wprof * keep
    zP = np.maximum.accumulate(zP)
    out = dict(z_axis_mm=list(zP * 1e3))
    for key in ["a_abs_1070", "a_sca_1070", "a_abs_700", "a_abs_900", "a_abs_975", "j_700", "j_900", "j_975"]:
        f = np.array([r[key] for r in jr]) * wprof
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(zP))])
        out[key] = float(cum[-1])
        out["cum_" + key] = list(cum)
    # emission seen coaxially, integrated over the jet's cross-section: the beam-heated core (pi w^2) and the rest of the
    # Gaussian cross-section (pi b_g^2 - pi w^2) at the gas temperature; W/(sr m) per unit wavelength
    ws = np.array([r["w_mm"] for r in jr]) * 1e-3
    for band in ("700", "900", "975"):
        jh = np.array([r[f"j_{band}"] for r in jr])
        jg = np.array([r[f"jg_{band}"] for r in jr])
        core = np.minimum(ws, bs / math.sqrt(2)) ** 2 * math.pi
        rest = np.maximum(math.pi * bs ** 2 / 2 - core, 0.0)
        f = (jh * core + jg * rest) * wprof
        out[f"emission_{band}"] = float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(zP)))
        f2 = jh * wprof
        out[f"radiance_axis_{band}"] = float(np.sum(0.5 * (f2[1:] + f2[:-1]) * np.diff(zP)))
    cm = np.array([r["C_cond_kg_m3"] for r in jr]) * np.exp(-(rr / (bs / math.sqrt(2))) ** 2)
    out["column_kg_m2"] = float(np.sum(0.5 * (cm[1:] + cm[:-1]) * np.diff(zP)))
    out["tau_ext_1070"] = out["a_abs_1070"] + out["a_sca_1070"]
    for lim in (1.0, 3.0, 5.0, 10.0):
        i = int(np.searchsorted(zP * 1e3, lim))
        out[f"tau_ext_1070_below_{lim:g}mm"] = (out["cum_a_abs_1070"][min(i, len(zP) - 1)] + out["cum_a_sca_1070"][min(i, len(zP) - 1)])
    return out


# ---------------------------------------------------------------------------------------------------------------- driver
def emission_ratios(beam, radio, T_wall):
    """Plume emission against the pool's. Photodiodes: optics.md's plume_tables scale linearly with tau B(T) A over its
    reference (tau 1e-3, 2700 K, a 0.3 mm column); here the column's emission is spread over the beam's area (pi w0^2).
    Camera: plume radiance at the beam centre over the depression's (emissivity 0.12 or 0.35 at T_wall)."""
    out = {}
    A_ref = math.pi * (0.15e-3) ** 2
    for band, key in (("700", "PD-A 700/40 (PDA36A2)"), ("900", "PD-B 900/40 (PDA36A2)")):
        ref = [r for r in radio["plume"] if r["channel"] == key and r["T_plume_K"] == 2700.0 and r["optical_depth"] == 0.001][0]
        em = beam[f"emission_{band}"]
        em_ref = 1e-3 * float(planck(BANDS[band], 2700.0)) * A_ref
        out[f"PD {band}: plume/pool"] = em / em_ref * ref["plume_over_pool"]
    Lp = beam["radiance_axis_975"]
    for eps in (0.12, 0.35):
        out[f"camera 975: plume/depression radiance (eps {eps})"] = Lp / (eps * float(planck(0.975, T_wall)))
    return out


def welding_case(case_al, mdot=7e-6):
    """A welding-like Al case to set against Wahl et al. 2026 (EN AW-5083, full penetration, 1 atm air): the beam in its own
    plume with no cross-flow beyond the weld speed. Their power, speed and keyhole weren't retrievable, so the inputs are
    assumed: the same exit state as LPBF's depression wall, 7 mg/s of Al vapour (~2 % of 4 kW into evaporation, as A finds
    ~2 % at 320 W, melt-pool.md §5), a 0.3 mm beam waist, 0.05 m/s."""
    c = copy.deepcopy(case_al)
    md = c["best"]["m_dot_kg_s"]
    scale = mdot / md["total"]
    for k in md:
        md[k] *= scale
    c["inputs"]["P_W"] = 4000.0
    c["inputs"]["v_m_s"] = 0.05
    c["tag"] = f"welding-like (assumed inputs): Al, 4 kW, {mdot * 1e6:.0f} mg/s of vapour, 0.05 m/s, still air"
    return c


def old_plume(r, flow, part_w=10e-3):
    """Condensate from earlier tracks still over the part. Each track's plume is carried downstream at the gas speed, so the
    beam at mid-part sees the column m_c / (2 U W) (part W wide across the flow; with no gas flow, ~0.25 m/s of convection
    over the 200 C plate, assumed), aged L / (2U); plus the chamber background along the beam axis above 20 mm from the CFD
    (C/S 22-270 s/m3, plume.md §1.2), aged ~1 s; plus, with no gas flow, the chamber filling at m_c H / V per second."""
    st = r["source"]
    U = FLOWS[flow][1] if FLOWS[flow][1] > 0 else 0.25
    sig_old = st["m_c"] / (2 * U * part_w)
    age = 5e-3 / U

    def kap(t):
        rec = min(r["records"], key=lambda q: abs(math.log(q["t"] / t)))
        return rec["k_abs_1070"], rec["k_sca_1070"], rec.get("d_c_massmedian_nm"), rec["f_ox"]

    ka, ks, dmm, fox = kap(age)
    out = dict(U_m_s=U, part_width_mm=part_w * 1e3, column_old_kg_m2=sig_old, age_s=age, k_abs=ka, k_sca=ks,
               d_c_massmedian_nm=dmm, f_ox=fox, tau_old=sig_old * (ka + ks))
    ka1, ks1, dmm1, fox1 = kap(1.0)
    scale = 2.95 / U if FLOWS[flow][1] > 0 else None
    cs = [c * (scale or 1.0) for c in CS_AXIS]
    sig_bg = [st["m_c"] * c * 0.10 for c in cs]
    out.update(CS_axis_s_m3=cs, column_bg_kg_m2=sig_bg, k_abs_1s=ka1, k_sca_1s=ks1, d_c_massmedian_1s_nm=dmm1, f_ox_1s=fox1,
               tau_bg=[sg * (ka1 + ks1) for sg in sig_bg])
    if FLOWS[flow][1] == 0:
        V_ch, H = 6.4e-3, 0.126                                  # chamber ~280 x 190 x 120 mm, beam path to the slide
        rate = st["m_c"] * H / V_ch                              # kg/m2 per second of lasing, well mixed, nothing removed
        out.update(no_flow_column_rate_kg_m2_per_min=rate * 60, no_flow_tau_per_min=rate * 60 * (ka1 + ks1))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true", help="nominal AlSi10Mg only")
    ap.add_argument("--t-end", type=float, default=1.0)
    a = ap.parse_args()
    src = json.loads(SRC.read_text())
    cases = {c["tag"]: c for c in src["cases"]}
    radio = json.loads(RADIO.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    res = dict(about="growth.py: condensate growth in the vapour jet and the bed jet, beam loss and coaxial emission (plume.md §3.6)",
               source_file="analysis/out/monitoring/melt/plume_source.json", nominal_params=NOMINAL,
               runs={}, edges={}, sensitivity={}, convergence={}, welding={}, risk2={})
    full = {}

    def go(case, flow="200+40 L/min", **over):
        over.setdefault("t_end", a.t_end)
        r = run(case, flow, **over)
        if r["beam"]:
            r["beam"]["emission_ratio"] = emission_ratios(r["beam"], radio, case["T_wall_K"])
        b = r["beam"]
        print(f"{case['tag'][:44]:44s} {flow:13s} {str({k: v for k, v in over.items() if k != 't_end'})[:44]:44s} "
              f"tau {100 * b.get('tau_ext_1070', float('nan')):6.3f} % (abs {100 * b.get('a_abs_1070', 0):.3f}, "
              f"sca {100 * b.get('a_sca_1070', 0):.4f}) col {1e6 * b.get('column_kg_m2', 0):6.1f} mg/m2 "
              f"PD700 {100 * b.get('emission_ratio', {}).get('PD 700: plume/pool', 0):6.2f} % steps {r['steps']} "
              f"cpu {r['cpu_s']:.1f} s", flush=True)
        return r

    nominal = {"AlSi10Mg": "ref_AlSi10Mg_320W_1.1ms_200C", "6061": "ref_6061_320W_1.1ms_200C", "7075": "map_7075_320W_1.1ms"}
    if a.quick:
        nominal = {"AlSi10Mg": nominal["AlSi10Mg"]}
    for alloy, tag in nominal.items():
        for flow in FLOWS:
            r = go(cases[tag], flow)
            r["old_plume"] = old_plume(r, flow)
            full[(alloy, flow)] = r
            res["runs"][f"{alloy} | {flow}"] = slim(r, full=(flow == "200+40 L/min"))
    if not a.quick:
        edges = {"AlSi10Mg 200 W, 1.1 m/s": "map_AlSi10Mg_200W_1.1ms", "AlSi10Mg 400 W, 1.1 m/s": "map_AlSi10Mg_400W_1.1ms",
                 "AlSi10Mg 320 W, 0.6 m/s": "ref_AlSi10Mg_320W_0.6ms_200C", "6061 200 W, 1.1 m/s": "map_6061_200W_1.1ms",
                 "6061 400 W, 1.1 m/s": "map_6061_400W_1.1ms", "6061 320 W, 0.6 m/s": "ref_6061_320W_0.6ms_200C",
                 "7075 320 W, depleted surface (fvol 0.1)": "map_7075_320W_1.1ms_fvol0.1", "7075 320 W, 0.6 m/s": "map_7075_320W_0.6ms",
                 "AlSi10Mg over loose powder (overhang)": "ovh_AlSi10Mg_320W_1.1ms_powder150um", "pure Al 320 W": "map_Al_320W_1.1ms"}
        for lab, tag in edges.items():
            for flow in ("200+40 L/min", "no gas flow"):
                r = go(cases[tag], flow)
                r["old_plume"] = old_plume(r, flow)
                res["edges"][f"{lab} | {flow}"] = slim(r, full=False)
        # 500 W: A's file stops at 400 W; scale its 400 W AlSi10Mg case's power (same vapour, beam heating at 500 W)
        r = go(cases["map_AlSi10Mg_400W_1.1ms"], "200+40 L/min", P_override=500.0)
        r["old_plume"] = old_plume(r, "200+40 L/min")
        res["edges"]["AlSi10Mg 500 W (400 W source, 500 W beam) | 200+40 L/min"] = slim(r, full=False)
        sens = {
            "D_f 1.6": dict(Df=1.6), "D_f 2.2": dict(Df=2.2), "k_f 1.0": dict(kf=1.0), "k_f 2.4": dict(kf=2.4),
            "sticking x0.5": dict(stick=0.5), "sticking x2 (van der Waals)": dict(stick=2.0),
            "sintering x0.1": dict(sinter=0.1), "sintering x10": dict(sinter=10.0),
            "nucleation slower (surface tension x1.2)": dict(sigma_f=1.2), "nucleation faster (surface tension x0.8)": dict(sigma_f=0.8),
            "vapour rate x0.5": dict(mdot_f=0.5), "vapour rate x2": dict(mdot_f=2.0),
            "O2 10 ppm": dict(o2_ppm=10.0), "O2 1000 ppm": dict(o2_ppm=1000.0), "O2 1000 ppm, oxide k 0.019 (Wahl)": dict(o2_ppm=1000.0, ox_k=0.019),
            "scan with the flow": dict(scan="with flow"), "scan against the flow": dict(scan="against flow"),
            "jet entrainment alpha_s x0.5": dict(alpha_s=0.04), "jet entrainment alpha_s x2": dict(alpha_s=0.16),
            "cross-flow entrainment alpha_n 0.3": dict(alpha_n=0.3), "cross-flow entrainment alpha_n 1.0": dict(alpha_n=1.0),
            "jet carries the wall reading's vapour (momentum x2.3)": dict(jet_mass="wall"),
            "bulk Al optics (Rakic, no size or temperature damping)": dict(optics="rakic"),
            "no laser heating of particles": dict(heating=False),
            "condensate crossing the beam doesn't evaporate": dict(cross_evap=False),
            "crossing agglomerates melt into spheres, don't evaporate": dict(melt_agg=True, cross_evap=False),
            "crossing agglomerates melt into spheres and evaporate": dict(melt_agg=True),
            "crossing condensate evaporates into vapour-free gas": dict(cross_evap="vacuum"),
            "thermal accommodation 0.1": dict(acc=0.1), "thermal accommodation 1.0": dict(acc=1.0),
            "gas at 473 K (200 C plate)": dict(Ta=473.0),
            "upper bound: slow mixing + vapour x2 + scan with the flow + no evaporation on crossing":
                dict(alpha_s=0.04, alpha_n=0.3, mdot_f=2.0, scan="with flow", cross_evap=False),
            "lower bound: vapour x0.5 + crossing condensate evaporates into vapour-free gas": dict(mdot_f=0.5, cross_evap="vacuum"),
        }
        for lab, over in sens.items():
            r = go(cases[nominal["AlSi10Mg"]], "200+40 L/min", **over)
            res["sensitivity"][lab] = slim(r, full=False)
        # numerical convergence on the nominal case: 4x finer coagulation steps with a 5x finer jet step, and more sections
        res["convergence"] = {}
        for lab, over in (("nominal (h_coag 2, h_jet 0.05, K 44)", {}), ("h_coag 0.5, h_jet 0.01", dict(h_coag=0.5, h_jet=0.01)),
                          ("K 48 (sections to ~6 um)", dict(K=48))):
            r = go(cases[nominal["AlSi10Mg"]], "200+40 L/min", **over)
            res["convergence"][lab] = dict(tau_ext_1070=r["beam"]["tau_ext_1070"], column_kg_m2=r["beam"]["column_kg_m2"], steps=r["steps"])
        # welding-like comparison (Wahl et al. 2026's shape: share of the loss within 5 and 10 mm)
        for mdot in (2e-6, 7e-6, 2e-5):
            wc = welding_case(cases["map_Al_320W_1.1ms"], mdot)
            for o2, gox, lab in ((210000.0, 1.0, "air"), (210000.0, 0.0, "air, oxidation off"), (100.0, 1.0, "argon, 100 ppm O2")):
                r = go(wc, "no gas flow", o2_ppm=o2, gamma_ox=gox, w0=150e-6, t_end=0.05)
                b = r["beam"]
                z = np.array(b["z_axis_mm"])
                cum = np.array(b["cum_a_abs_1070"]) + np.array(b["cum_a_sca_1070"])
                prof = {f"{h:g} mm": float(np.interp(h, z, cum)) for h in (1, 2, 5, 10, 25, 50, 100, 370)}
                res["welding"][f"{mdot * 1e6:.0f} mg/s | {lab}"] = dict(tag=wc["tag"], o2_ppm=o2, tau_by_height=prof,
                                                                        tau_ext=b["tau_ext_1070"], tau_abs=b["a_abs_1070"],
                                                                        tau_sca=b["a_sca_1070"], column_kg_m2=b["column_kg_m2"])
    # risk 2: what separates the cases on this machine
    for alloy in nominal:
        rows = {}
        for flow in FLOWS:
            r = full[(alloy, flow)]
            b, op = r["beam"], r["old_plume"]
            tau_fresh = b["tau_ext_1070"]
            tau_tot = tau_fresh + op["tau_old"] + op["tau_bg"][1]
            # transverse optical depth of the plume at 900 nm (an 850-900 nm light through BW into LW), at several heights
            jr = [q for q in r["records"] if q["phase"] == "jet"]
            trans = {}
            for hgt in (0.25, 0.5, 1.0, 2.0, 3.0):
                q = min(jr, key=lambda qq: abs(qq["z_mm"] - hgt))
                bg = q["b_mm"] * 1e-3 / math.sqrt(2)
                trans[f"{hgt:g} mm"] = (q["a_abs_900"] + q["a_sca_900"]) * math.sqrt(math.pi) * bg
            # the beam's own column seen from the side (LW camera, 850-900 nm): laser-heated condensate on the beam axis, against
            # the depression's radiance (emissivity 0.12 at T_wall); and the height holding 90 % of that glow
            zP = np.array(b["z_axis_mm"])
            cum = np.array(b["cum_j_900"])
            z90 = float(np.interp(0.9 * cum[-1], cum, zP)) if cum[-1] > 0 else 0.0
            peak_side = 0.0
            for q in jr:
                if q["in_beam"]:
                    peak_side = max(peak_side, q["j_900"] * 2 * W0)
            side_ratio = peak_side / (0.12 * float(planck(0.90, r["source"]["T_wall"])))
            rows[flow] = dict(tau_fresh=tau_fresh, tau_old=op["tau_old"], tau_bg_high=op["tau_bg"][1], tau_total=tau_tot,
                              glow_height_90pct_mm=z90, side_view_glow_over_pool_radiance=side_ratio,
                              track_width_change=-tau_tot / 2, photodiode_change_P2=-2 * tau_tot,
                              plume_emission_PD700=b["emission_ratio"]["PD 700: plume/pool"],
                              plume_emission_PD900=b["emission_ratio"]["PD 900: plume/pool"],
                              transverse_tau_900=trans)
        res["risk2"][alloy] = rows
    json.dump(rounded(res), open(OUT / "growth.json", "w"), indent=1, default=float)
    figures(full, res)


def rounded(o, sig=4):
    """Round floats to 4 significant figures for the JSON."""
    if isinstance(o, dict):
        return {k: rounded(v, sig) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [rounded(v, sig) for v in o]
    if isinstance(o, (float, np.floating)):
        return float(f"{float(o):.{sig}g}") if math.isfinite(float(o)) else None
    return o


def slim(r, full=True):
    out = {k: v for k, v in r.items() if k not in ("records", "snapshots")}
    keep = ("t", "s_mm", "x_mm", "z_mm", "b_mm", "u", "T_g", "T_p", "T_axis_mass_mean", "f_ox", "f_cond", "in_beam", "phase",
            "compact", "molten_mass_frac", "d_p_nm", "d_c_mean_nm", "d_c_massmedian_nm", "d_v_massmean_nm", "n_p_mass_mean", "N_m3", "C_cond_kg_m3",
            "a_abs_1070", "a_sca_1070", "k_abs_1070", "k_sca_1070", "a_abs_900", "a_sca_900", "j_900", "jg_900", "w_mm")
    recs = r["records"] if full else r["records"][::5]
    out["records"] = [{k: rr.get(k) for k in keep} for rr in recs]
    if full:
        out["snapshots"] = r["snapshots"]
    b = dict(out.get("beam", {}))
    if not full:
        for k in list(b):
            if k.startswith("cum_") or k == "z_axis_mm":
                b.pop(k)
    out["beam"] = b
    return out


def figures(full, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = {"AlSi10Mg": "#2a78d6", "6061": "#1baf7a", "7075": "#eb6834"}
    ink, grid = "#0b0b0b", "#e8e8e4"
    # --- figure 1: growth of the AlSi10Mg condensate along the plume, 200 + 40 L/min ---
    r = full[("AlSi10Mg", "200+40 L/min")]
    rec = [q for q in r["records"] if q.get("d_c_massmedian_nm")]
    t = np.array([q["t"] for q in rec])
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.3), constrained_layout=True)
    ax = axs[0]
    ax.loglog(t * 1e3, [q["d_p_nm"] for q in rec], color=cols["AlSi10Mg"], lw=2, label="primary particle d_p")
    ax.loglog(t * 1e3, [q["d_c_massmedian_nm"] for q in rec], color=cols["7075"], lw=2, label="agglomerate, mass-median collision d")
    tb = max([q["t"] for q in rec if q["in_beam"]] or [1e-8])
    ax.axvspan(t[0] * 1e3, tb * 1e3, color=grid, zorder=0)
    ax.text(t[0] * 1.4e3, 1.0, "centreline in the beam:\nmolten, ~2,100-2,200 K", fontsize=7.5, color=ink, va="bottom")
    ax.axhline(300, color="#52514e", lw=0.7, ls=":")
    ax.text(2.0, 360, "300 nm: the old upper bound", fontsize=7, color="#52514e")
    for tt in (1e-3, 1e-2, 0.1, 1.0):
        q = min(rec, key=lambda qq: abs(math.log(qq["t"] / tt)))
        if q["phase"] == "jet":
            ax.annotate(f"z {q['z_mm']:.1f} mm\nx {q['x_mm']:.1f} mm", (tt * 1e3, q["d_c_massmedian_nm"]), fontsize=6.5,
                        textcoords="offset points", xytext=(-10, 12), color="#52514e")
    ax.set_xlabel("time since leaving the depression wall (ms)")
    ax.set_ylabel("diameter (nm)")
    ax.set_ylim(0.8, 2000)
    ax.set_title("AlSi10Mg, 320 W, 1.1 m/s, 200 + 40 L/min: how big it gets", fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.88))
    ax = axs[1]
    shades = ["#c6dbf5", "#94bdee", "#5f9de4", "#2a78d6", "#1d5aa3", "#123d70", "#0b0b0b"]
    for sn, c in zip(r["snapshots"], shades):
        d = np.array(sn["d_c_nm"])
        vf = np.array(sn["vol_frac"])
        ok = (np.arange(len(d)) >= 1) & (np.array(sn["d_v_nm"]) >= 1.0)
        dl = np.log10(2.0) / 3                                       # sections are 2x in volume
        ts = sn["t_s"]
        lab = f"{ts * 1e6:.0f} µs" if ts < 1e-4 else (f"{ts * 1e3:.1f} ms" if ts < 1e-3 else (f"{ts * 1e3:.0f} ms" if ts < 0.99 else f"{ts:.0f} s"))
        ax.semilogx(d[ok], vf[ok] / dl, color=c, lw=1.6, label=lab + (" (bed jet)" if sn["phase"] == "bed" else ""))
    ax.set_xlim(1, 3000)
    ax.set_xlabel("collision diameter (nm)")
    ax.set_ylabel("volume fraction per decade of volume")
    ax.set_title("Size distribution by mass at 1 µs to 1 s", fontsize=9)
    ax.legend(fontsize=7, frameon=False)
    ax = axs[2]
    jr = [q for q in r["records"] if q["phase"] == "jet"]
    zz = np.array([q["z_mm"] for q in jr])
    ax.semilogx(zz, [q["T_g"] for q in jr], color=cols["AlSi10Mg"], lw=2, label="gas, top-hat mean")
    ax.semilogx(zz, [q["T_p"] if q["in_beam"] else np.nan for q in jr], color=cols["7075"], lw=2, label="particles in the beam (centreline)")
    ax.axhline(933, color="#52514e", lw=0.7, ls=":")
    ax.text(zz[2], 960, "Al melts (933 K)", fontsize=7, color="#52514e")
    ax.set_xlabel("height of the jet's centreline above the plate (mm)")
    ax.set_ylabel("temperature (K)")
    ax.set_title("Cooling by mixing, held up by condensation and by the beam", fontsize=9)
    ax.legend(fontsize=7, frameon=False)
    for ax in axs:
        ax.grid(color=grid, lw=0.6)
    fig.savefig(OUT / "growth_sizes.png", dpi=110)
    plt.close(fig)
    # --- figure 2: beam loss ---
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), constrained_layout=True, gridspec_kw=dict(width_ratios=[1, 1, 1.3]))
    ax = axs[0]
    for alloy, c in cols.items():
        if (alloy, "200+40 L/min") not in full:
            continue
        b = full[(alloy, "200+40 L/min")]["beam"]
        z = np.array(b["z_axis_mm"])
        cum = 100 * (np.array(b["cum_a_abs_1070"]) + np.array(b["cum_a_sca_1070"]))
        ok = z > 1e-3
        ax.semilogx(z[ok], cum[ok], color=c, lw=2, label=alloy)
        dy = {"AlSi10Mg": 0.008, "7075": -0.022, "6061": 0.008}[alloy]
        ax.text(2.0, cum[ok][-1] + dy, f"{alloy}: {cum[ok][-1]:.2f} %", fontsize=7.5, color=ink)
    ax.set_xlim(0.003, 50)
    ax.set_ylim(0, None)
    ax.set_xlabel("height up the beam axis (mm)")
    ax.set_ylabel("beam lost below that height (%)")
    ax.set_title("Fresh plume, 320 W, 1.1 m/s, 200 + 40 L/min", fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax = axs[1]
    flows = list(FLOWS)
    xs = np.arange(len(flows))
    wbar = 0.26
    for i, (alloy, c) in enumerate(cols.items()):
        if (alloy, flows[0]) not in full:
            continue
        fresh = [100 * full[(alloy, f)]["beam"]["tau_ext_1070"] for f in flows]
        old = [100 * (full[(alloy, f)]["old_plume"]["tau_old"] + full[(alloy, f)]["old_plume"]["tau_bg"][1]) for f in flows]
        ax.bar(xs + (i - 1) * wbar, fresh, wbar * 0.92, color=c, label=f"{alloy}: fresh plume")
        ax.bar(xs + (i - 1) * wbar, old, wbar * 0.92, bottom=fresh, color=c, alpha=0.45, hatch="///", edgecolor="white",
               label=f"{alloy}: older condensate")
    ax.set_xticks(xs, [f.replace(" L/min", "\nL/min") for f in flows])
    ax.set_ylabel("beam lost at 1070 nm (%)")
    ax.set_title("By cross-flow (no gas flow: before the chamber fills)", fontsize=9)
    ax.legend(fontsize=6.5, frameon=False, ncol=1)
    ax = axs[2]
    base = 100 * full[("AlSi10Mg", "200+40 L/min")]["beam"]["tau_ext_1070"]
    items = sorted(res["sensitivity"].items(), key=lambda kv: kv[1]["beam"].get("tau_ext_1070", 0))
    labels = [k if len(k) <= 46 else k[:44] + "…" for k, _ in items]
    vals = [100 * v["beam"].get("tau_ext_1070", 0) for _, v in items]
    ax.barh(np.arange(len(vals)), np.array(vals) - base, left=base, color=[cols["7075"] if v > base else cols["AlSi10Mg"] for v in vals],
            height=0.7)
    ax.axvline(base, color=ink, lw=0.8)
    ax.set_yticks(np.arange(len(vals)), labels, fontsize=6.2)
    ax.set_xlim(0, max(vals) * 1.05)
    ax.set_xlabel("fresh-plume loss (%); line: nominal")
    ax.set_title("Sensitivity, one input at a time", fontsize=9)
    for ax in axs:
        ax.grid(color=grid, lw=0.6)
    fig.savefig(OUT / "growth_loss.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
