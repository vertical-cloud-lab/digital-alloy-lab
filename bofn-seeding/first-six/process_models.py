#!/usr/bin/env python3
"""Cheap process models behind the first-six seed recipes (#275).

Everything here is an estimate meant to set a starting point and its uncertainty, not a prediction
to trust. Each block says what it assumes.

1. Charge recipes: mass balance for a 250 g charge built on 6063 (and 4047 for Si), with Zr from
   an Al-10Zr master alloy, and the composition that results (6063 brings Mg, Si and Fe).
2. Ultrasonic atomization: Lang's capillary-wave relation for the median droplet size at 40 kHz,
   a lognormal spread taken from two published ultrasonic Al powders, and the mass fraction in
   each sieve cut.
3. Droplet cooling and in-flight evaporation of Mg, Zn, Mn and Li (lumped droplet in still argon,
   Sh = Nu = 2), plus the diffusion-limited loss from the crucible surface during the hold.
4. Laser powder bed fusion: Eagar-Tsai melt-pool width and depth for a Gaussian beam, with
   conductivity from the Wiedemann-Franz law and solute resistivity, a lack-of-fusion criterion,
   and a normalized-enthalpy keyhole flag. A published parameter set for each family is
   transferred to the Aconity MIDI (80 um spot) at 30 and 50 um layers by matching melt-pool depth per
   layer and width per hatch.

    python bofn-seeding/first-six/process_models.py            # writes results/process/*.csv
"""
from __future__ import annotations

import csv
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "results" / "process"

MASS = dict(Al=26.9815, Mn=54.938, Cr=51.9961, Zr=91.224, Mg=24.305, Si=28.0855, Cu=63.546, Ti=47.867, Fe=55.845,
            Ni=58.6934, Ce=140.116, Sc=44.9559, Li=6.94, Er=167.259, Zn=65.38, Sn=118.71)

# ----------------------------------------------------------------------------- seeds
# The six seeds (D1, D2, S1, S2, S3, X1) and the three optional ones (O1, O2, O3). Target compositions in wt%.
# "ref" is the published parameter set the print window is transferred from: power W, speed mm/s, hatch um,
# layer um, 1/e2 spot diameter um, plate C. "calphad" is the id of the matching row in results/calphad/named.csv.
# "plate" is the build-plate temperature to start at, "age" the direct-ageing schedule (no solution treatment).
SEEDS = {
    "D1": dict(name="Al-10Si-0.35Mg (AlSi10Mg-type benchmark)", wt=dict(Si=10.0, Mg=0.35), calphad="D1", plate=35,
               age="none (as built); optional 165 C / 6 h",
               ref=dict(P=370, v=1300, h=190, t=30, spot=100, plate=35, src="EOS M290-class practice; the EOS datasheet gives plate 35 C at 30 um and 100 C at 60 um")),
    "D2": dict(name="Al-4.6Mg-0.66Sc-0.42Zr-0.49Mn (Scalmalloy-type benchmark)", wt=dict(Mg=4.6, Sc=0.66, Zr=0.42, Mn=0.49),
               calphad="D2", plate=200, age="325 C / 4 h",
               ref=dict(P=370, v=1000, h=100, t=30, spot=80, plate=200, src="Aconity MIDI, Schimbaeck et al. 2024, 10.1016/j.msea.2024.146102 (as reported by Edison q7)")),
    "S1": dict(name="Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg (Al-Mn-Cr-Zr with Mg and high Zr)", wt=dict(Mn=4.8, Cr=0.9, Zr=1.1, Mg=1.2),
               calphad="S1", plate=100, age="375 C / 8 h (peak); also 350 C / 4 h (under-aged, for ductility)",
               ref=dict(P=370, v=1300, h=130, t=30, spot=100, plate=25, src="EOS M290, Mehta et al. 2023, 10.1016/j.jallcom.2023.171685")),
    "S2": dict(name="Al-1.9Fe-1.0Mg-1.0Zr (Al-Fe-Mg-Zr)", wt=dict(Fe=1.87, Mg=1.02, Zr=1.03), calphad="S2", plate=100,
               age="400 C / 4 h",
               ref=dict(P=380, v=1800, h=100, t=30, spot=75, plate=25, src="SLM 125HL, Li et al. 2025, 10.1080/17452759.2025.2516663 (spot size assumed)")),
    "S3": dict(name="Al-3.5Si-2.5Mg (AlSi3.5Mg2.5-type)", wt=dict(Si=3.5, Mg=2.5), calphad="S3", plate=50,
               age="170 C / 1 h",
               ref=dict(P=370, v=1200, h=100, t=50, spot=70, plate=50, src="SLM 125HL, Knoop et al. 2020, 10.3390/met10040514; speed and hatch from Solanki et al. 2026, 10.1007/s40964-026-01583-1")),
    "X1": dict(name="Al-6Mg-2.5Si-0.7Ti (Ti as the grain refiner; exploratory)", wt=dict(Mg=6.0, Si=2.5, Ti=0.7), calphad="X1",
               plate=100, age="as built; screen 170 C / 1-2 h",
               ref=dict(P=370, v=1200, h=100, t=50, spot=70, plate=50, src="no parameter set read for this alloy (Wen et al. 2024 seen as abstract only); S3's set is used as the starting point")),
    "O1": dict(name="Al-3.6Mg-1.2Zr (Al-Mg-Zr)", wt=dict(Mg=3.6, Zr=1.2), calphad="S4", plate=100, age="400 C / 8 h",
               ref=dict(P=200, v=200, h=135, t=30, spot=90, plate=25, src="Concept Laser M2, Croteau et al. 2018, 10.1016/j.actamat.2018.04.053")),
    "O2": dict(name="Al-6.4Mg-0.7Mn-0.4Er-1.1Zr (Er in place of Sc)", wt=dict(Mg=6.4, Mn=0.72, Er=0.4, Zr=1.1), calphad="O2-noEr",
               plate=100, age="375 C / 10 h",
               ref=dict(P=350, v=1000, h=130, t=30, spot=80, plate=25, src="SLM 280, Guo et al. 2022, 10.1016/j.matdes.2022.111064 (as reported by Edison q7; spot size assumed)")),
    "O3": dict(name="Al-4.8Mn-0.8Cr (Zr-free Al-Mn-Cr)", wt=dict(Mn=4.8, Cr=0.8), calphad="E1", plate=35,
               age="375 C / 1-4 h (over-ages quickly without Zr)",
               ref=dict(P=170, v=1500, h=100, t=30, spot=40, plate=25, src="EOS M100, Mehta et al. 2022, 10.1016/j.jallcom.2022.165870")),
}

BASE_6063 = dict(Mg=0.55, Si=0.40, Fe=0.20)   # typical 6063 bar (limits: Mg 0.45-0.9, Si 0.2-0.6, Fe <= 0.35)
ROD_4047 = dict(Si=12.0, Fe=0.30)             # Al-12Si rod (Fe <= 0.8)
MASTER = dict(Zr=0.10)                         # Zr as Al-10Zr; every other addition as the element


# ----------------------------------------------------------------------------- 1. recipes
def recipe(target: dict, charge_g: float = 250.0, base: str = "6063", overcharge: dict | None = None) -> dict:
    """Masses to weigh and the composition expected in the melt (before evaporation and recovery)."""
    overcharge = overcharge or {}
    t = {k: float(v) for k, v in target.items()}
    carriers = {}
    for el, w in t.items():
        if el == "Si":
            continue
        carriers[el] = w / 100.0 / MASTER.get(el, 1.0)          # mass fraction of the carrier in the charge
    base_comp = BASE_6063 if base == "6063" else {}
    rest = 1.0 - sum(carriers.values())
    si = t.get("Si", 0.0)
    f47 = 0.0
    if si > base_comp.get("Si", 0.0) * rest + 1e-9:
        f47 = (si / 100.0 - base_comp.get("Si", 0.0) / 100.0 * rest) / ((ROD_4047["Si"] - base_comp.get("Si", 0.0)) / 100.0)
    fb = rest - f47
    out, masses = dict(t), {}
    for el in ("Mg", "Si", "Fe"):
        borne = base_comp.get(el, 0.0) * fb + ROD_4047.get(el, 0.0) * f47
        need = t.get(el, 0.0) - borne
        if el in carriers:
            # the base already brings part of this element: weigh less of it, and give the mass back to the base
            give_back = min(borne, t.get(el, 0.0)) / 100.0
            carriers[el] = max(need, 0.0) / 100.0
            fb += give_back
        out[el] = max(t.get(el, 0.0), borne)
    for el, f in carriers.items():
        m = f * charge_g * (1.0 + overcharge.get(el, 0.0))
        masses[("Al-10Zr master" if el == "Zr" else el)] = round(m, 2)
    masses[base + (" bar/cups" if base == "6063" else " base")] = round(fb * charge_g, 1)
    if f47 > 0:
        masses["4047 rod"] = round(f47 * charge_g, 1)
    return dict(masses=masses, melt_wt={k: round(v, 2) for k, v in out.items() if v > 0.005}, f_base=round(fb, 3), f_4047=round(f47, 3))


# ----------------------------------------------------------------------------- 2. atomization
def melt_props(wt: dict, T_C: float) -> tuple[float, float]:
    """Surface tension (N/m) and density (kg/m3) of the liquid alloy: pure Al with small linear solute shifts.

    Lang's size goes as (sigma/rho)^(1/3), so a 10 % error in either moves the size by about 3 %.
    Shifts per wt% are rough literature slopes (Mg, Zn, Li and Sn lower the surface tension; Si slightly).
    """
    T = T_C + 273.15
    sigma = 0.871 - 1.55e-4 * (T - 933.0)
    sigma += -0.07 * (1 - math.exp(-wt.get("Mg", 0) / 3.0)) - 0.0025 * wt.get("Si", 0) - 0.003 * wt.get("Zn", 0)
    sigma += -0.06 * (1 - math.exp(-wt.get("Li", 0) / 1.0)) - 0.08 * (1 - math.exp(-wt.get("Sn", 0) / 0.5))
    rho_al = 2375.0 - 0.233 * (T - 933.0)
    liq = dict(Mn=5900, Cr=6300, Zr=5800, Mg=1590, Si=2570, Cu=8000, Ti=4100, Fe=7000, Ni=7800, Ce=6550, Sc=2800,
               Li=510, Er=8600, Zn=6570, Sn=6990)
    inv = (1 - sum(wt.values()) / 100.0) / rho_al + sum(w / 100.0 / liq[e] for e, w in wt.items())
    return sigma, 1.0 / inv


def lang_d50(sigma: float, rho: float, f_hz: float = 40e3) -> float:
    """Median droplet diameter in um from Lang (1962): 0.34 * capillary wavelength."""
    return 0.34 * (8 * math.pi * sigma / (rho * f_hz**2)) ** (1 / 3) * 1e6


# Lognormal spread: ln(D90/D10)/2.563. Al-10Cu on a rePOWDER 36/65/78 um -> 0.30; Al-Ni-Zr-Er ultrasonic
# powder 44.5/63.8/91.5 um (Taheri-Mousavi et al.) -> 0.28. Used: 0.29.
SIGMA_LN = 0.29


def cut_fraction(d50: float, lo: float, hi: float, s: float = SIGMA_LN) -> float:
    from math import erf, log, sqrt

    cdf = lambda d: 0.5 * (1 + erf((log(d) - log(d50)) / (s * sqrt(2))))  # noqa: E731
    return cdf(hi) - cdf(lo)


# ----------------------------------------------------------------------------- 3. droplets and evaporation
def p_sat(el: str, T: float) -> float:
    """Vapour pressure (Pa) of the pure liquid element. Mg, Zn, Li: Alcock et al. (1984) fits. Mn: Clausius-Clapeyron
    through its melting-point and boiling-point pressures."""
    if el == "Mg":
        return 10 ** (13.495 - 7813.0 / T - 0.8253 * math.log10(T))
    if el == "Zn":
        return 10 ** (10.384 - 6286.0 / T)
    if el == "Li":
        return 10 ** (10.061 - 8023.0 / T)
    if el == "Mn":
        return 10 ** (10.0 - 12000.0 / T)
    return 0.0


GAMMA = dict(Mg=0.9, Zn=1.4, Li=0.2, Mn=0.03)   # rough activity coefficients in liquid Al at high dilution


def mole_fracs(wt: dict) -> dict:
    n = {e: w / MASS[e] for e, w in wt.items()}
    n["Al"] = (100.0 - sum(wt.values())) / MASS["Al"]
    tot = sum(n.values())
    return {e: v / tot for e, v in n.items()}


def droplet_history(wt: dict, d_um: float, T_melt_C: float, T_liq_C: float, T_sol_C: float, T_gas_C: float = 60.0):
    """Lumped droplet in still argon: cooling to the liquidus, then freezing; returns the cooling rate and the
    fraction of each volatile element lost before it is solid. Nu = Sh = 2 (droplets leave the plate slowly)."""
    d = d_um * 1e-6
    rho, cp, Lf = 2400.0, 1100.0, 3.9e5
    k_gas, D_gas = 0.045, 1.2e-4          # argon near 700 K film temperature; metal vapour in argon
    h = 2 * k_gas / d
    kg = 2 * D_gas / d
    eps, sb = 0.2, 5.67e-8
    x = mole_fracs(wt)
    m0 = rho * math.pi * d**3 / 6
    n_el = {e: m0 * wt[e] / 100.0 / (MASS[e] * 1e-3) for e in GAMMA if e in wt}
    n0 = dict(n_el)
    n_tot = m0 / (sum(x[e] * MASS[e] for e in x) * 1e-3)
    T, Tg, t, dt = T_melt_C + 273.15, T_gas_C + 273.15, 0.0, 2e-5
    fs, rate0 = 0.0, None
    A = math.pi * d**2
    while fs < 1.0 and t < 2.0:
        q = h * (T - Tg) + eps * sb * (T**4 - Tg**4)
        for e in n_el:
            p = GAMMA[e] * (n_el[e] / n_tot) * p_sat(e, T) * (1.0 - fs)   # liquid surface shrinks as it freezes
            n_el[e] = max(n_el[e] - kg * p / (8.314 * T) * A * dt, 0.0)
        if T > T_liq_C + 273.15:
            dT = q * A * dt / (m0 * cp)
            if rate0 is None:
                rate0 = dT / dt
            T -= dT
        else:
            # freezing spread linearly over the liquidus-solidus interval
            span = max(T_liq_C - T_sol_C, 1.0)
            dfs = q * A * dt / (m0 * (Lf + cp * span))
            fs += dfs
            T -= dfs * span
        t += dt
    return dict(cool_rate_K_s=rate0, liquid_time_ms=t * 1e3,
                loss={e: 1.0 - n_el[e] / n0[e] for e in n_el})


def crucible_loss(wt: dict, T_C: float, hold_min: float, charge_g: float = 250.0, area_cm2: float = 3.5,
                  bl_mm: float = 8.0) -> dict:
    """Diffusion-limited evaporation from the melt surface in the crucible under 1 atm argon."""
    T = T_C + 273.15
    x = mole_fracs(wt)
    kg = 1.2e-4 / (bl_mm * 1e-3)
    out = {}
    for e in GAMMA:
        if e in wt:
            p = GAMMA[e] * x[e] * p_sat(e, T)
            g = kg * p / (8.314 * T) * MASS[e] * area_cm2 * 1e-4 * hold_min * 60.0
            out[e] = g / (charge_g * wt[e] / 100.0)
    return out


# ----------------------------------------------------------------------------- 4. LPBF
# Solute resistivity in solid solution (micro-ohm cm per wt%), standard handbook values for Al.
RHO_SS = dict(Mn=2.94, Cr=4.0, Zr=1.74, Mg=0.54, Si=1.02, Cu=0.344, Ti=2.88, Fe=2.56, Ni=0.81, Sc=3.4, Zn=0.094,
              Li=3.31, Er=0.5, Ce=0.5, Sn=0.1)
# Fraction of each addition assumed retained in solid solution in the as-printed solid the laser remelts.
RETAINED = dict(Mn=0.8, Cr=0.9, Zr=0.6, Mg=0.9, Si=0.25, Cu=0.5, Ti=0.6, Fe=0.3, Ni=0.1, Sc=0.7, Zn=0.9, Li=0.9,
                Er=0.3, Ce=0.05, Sn=0.2)


def conductivity(wt: dict, T: float = 800.0) -> float:
    """Thermal conductivity (W/m K) of the solid near 800 K from Wiedemann-Franz, then averaged with the liquid."""
    rho_e = (2.65 + 0.0115 * (T - 293.0)) + sum(RHO_SS.get(e, 0) * RETAINED.get(e, 0.5) * w for e, w in wt.items())
    k_solid = 2.44e-8 * T / (rho_e * 1e-8)
    # second-phase network (eutectic Si etc.) blocks heat a little
    k_solid *= 1.0 - 0.012 * wt.get("Si", 0.0)
    return 0.5 * (k_solid + 90.0)


_S = np.logspace(-8.5, -1.8, 140)             # time since the beam passed (s)
_XS = np.linspace(-1.6e-3, 2.5e-4, 180)[:, None]


def _tmax(P, v, sig, a, rho, cp, A, y, z):
    """Peak temperature rise at lateral offset y and depth z (Eagar and Tsai 1983, Gaussian beam)."""
    pref = A * P / (math.pi * rho * cp * math.sqrt(4 * math.pi * a))
    w_t = _S ** -0.5 / (2 * a * _S + sig**2)
    expo = -((_XS + v * _S[None, :]) ** 2 + y**2) / (4 * a * _S[None, :] + 2 * sig**2) - z**2 / (4 * a * _S[None, :])
    return pref * np.trapezoid(w_t[None, :] * np.exp(expo), _S, axis=1).max()


def _root(fun, target, lo, hi, n=15):
    if fun(lo) < target:
        return 0.0
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if fun(mid) >= target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def et_depth(P, v_mm_s, spot_um, k, T_liq_C, A=0.35, T0_C=25.0, rho=2550.0, cp=1050.0):
    """Melt-pool depth (um) for a Gaussian beam moving over a half-space."""
    sig, a = spot_um * 1e-6 / 4.0, k / (rho * cp)        # 1/e2 diameter = 4 sigma
    return _root(lambda z: _tmax(P, v_mm_s * 1e-3, sig, a, rho, cp, A, 0.0, z), T_liq_C - T0_C, 1e-7, 500e-6) * 1e6


def et_width(P, v_mm_s, spot_um, k, T_liq_C, A=0.35, T0_C=25.0, rho=2550.0, cp=1050.0):
    sig, a = spot_um * 1e-6 / 4.0, k / (rho * cp)
    return 2 * _root(lambda y: _tmax(P, v_mm_s * 1e-3, sig, a, rho, cp, A, y, 0.0), T_liq_C - T0_C, 0.0, 500e-6) * 1e6


def eagar_tsai(P, v_mm_s, spot_um, k, T_liq_C, A=0.35, T0_C=25.0, rho=2550.0, cp=1050.0):
    """Melt-pool width and depth (um). Conduction only: it cannot show keyholing."""
    return (et_width(P, v_mm_s, spot_um, k, T_liq_C, A, T0_C, rho, cp),
            et_depth(P, v_mm_s, spot_um, k, T_liq_C, A, T0_C, rho, cp))


def norm_enthalpy(P, v_mm_s, spot_um, k, T_liq_C, A=0.35, rho=2550.0, cp=1050.0):
    """Normalized enthalpy A P / (rho cp Tm sqrt(pi a v r^3)), r = 1/e2 radius (Hann et al. 2011; King et al. 2014)."""
    r = spot_um * 1e-6 / 2
    a = k / (rho * cp)
    return A * P / (rho * cp * (T_liq_C + 273.15) * math.sqrt(math.pi * a * v_mm_s * 1e-3 * r**3))


def lof_ok(w, d, h, t):
    """Tang et al. (2017) lack-of-fusion criterion: (h/w)^2 + (t/d)^2 <= 1."""
    return w > 0 and d > 0 and (h / w) ** 2 + (t / d) ** 2 <= 1.0


def speed_for_depth(P, depth_um, spot, k, T_liq_C, T0_C=25.0, lo=200.0, hi=3500.0):
    """Scan speed (mm/s) that gives a target conduction-mode depth at power P (depth falls as speed rises)."""
    if et_depth(P, lo, spot, k, T_liq_C, T0_C=T0_C) < depth_um:
        return lo
    if et_depth(P, hi, spot, k, T_liq_C, T0_C=T0_C) > depth_um:
        return hi
    for _ in range(11):
        mid = math.sqrt(lo * hi)
        if et_depth(P, mid, spot, k, T_liq_C, T0_C=T0_C) >= depth_um:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def transfer(wt, T_liq_C, ref, spot=80.0, layer=50.0, P=350.0, plate_C=25.0):
    """Move a published parameter set to the MIDI's 80 um spot and our layer thickness.

    Rule: keep the melt-pool depth of the published set (at least two layers deep), at 350 W, which leaves
    headroom below the 400 W laser; then set the hatch from the lack-of-fusion criterion with a margin,
    (h/w)^2 + (t/d)^2 = 0.7, and never wider than the published hatch-to-width ratio.
    """
    k = conductivity(wt)
    w0, d0 = eagar_tsai(ref["P"], ref["v"], ref["spot"], k, T_liq_C, T0_C=ref.get("plate", 25))
    target = max(d0, 2.0 * layer)
    v = speed_for_depth(P, target, spot, k, T_liq_C, T0_C=plate_C)
    v = round(v / 50.0) * 50.0
    w, d = eagar_tsai(P, v, spot, k, T_liq_C, T0_C=plate_C)
    room = 0.7 - (layer / d) ** 2 if d > 0 else 0.0
    h_lof = w * math.sqrt(room) if room > 0 else 0.0
    h_ref = w * ref["h"] / w0 if w0 > 0 else h_lof
    h = max(60.0, math.floor(min(h_lof, h_ref) / 10.0) * 10.0)
    return dict(k=round(k), ref_w=round(w0), ref_d=round(d0), ref_d_per_layer=round(d0 / ref["t"], 2),
                ref_enthalpy=round(norm_enthalpy(ref["P"], ref["v"], ref["spot"], k, T_liq_C), 1),
                ref_ved=round(ref["P"] / (ref["v"] * ref["h"] * 1e-3 * ref["t"] * 1e-3)),
                P=P, v=v, h=h, t=layer, w=round(w), d=round(d), d_per_layer=round(d / layer, 2),
                lof=round((h / w) ** 2 + (layer / d) ** 2, 2) if w > 0 and d > 0 else float("nan"),
                enthalpy=round(norm_enthalpy(P, v, spot, k, T_liq_C), 1),
                ved=round(P / (v * h * 1e-3 * layer * 1e-3)))


def doe(wt, T_liq_C, centre, spot=80.0, plate_C=25.0):
    """Sixteen cubes around the centre: 2 powers x 4 speeds x 2 hatches, with the model's read of each."""
    k = conductivity(wt)
    rows = []
    for P in (centre["P"] - 60.0, centre["P"] + 30.0):
        for fv in (0.7, 0.85, 1.0, 1.25):
            v = round(centre["v"] * fv / 50.0) * 50.0
            w, d = eagar_tsai(P, v, spot, k, T_liq_C, T0_C=plate_C)
            for h in (centre["h"], centre["h"] + 30.0):
                lof = (h / w) ** 2 + (centre["t"] / d) ** 2 if w > 0 and d > 0 else float("nan")
                rows.append(dict(P_W=int(P), v_mm_s=int(v), hatch_um=int(h), layer_um=int(centre["t"]), pool_w_um=round(w),
                                 pool_d_um=round(d), lof_index=round(lof, 2),
                                 enthalpy=round(norm_enthalpy(P, v, spot, k, T_liq_C), 1),
                                 ved_J_mm3=round(P / (v * h * 1e-3 * centre["t"] * 1e-3))))
    return rows


# ----------------------------------------------------------------------------- driver
# Liquidus, alpha-Al start, Scheil end and the melt setpoint come from the CALPHAD screen
# (results/calphad/named.csv). Er is not in either database: O2 uses its Er-free composition.
def load_calphad():
    p = HERE / "results" / "calphad" / "named.csv"
    out = {}
    if p.exists():
        for r in csv.DictReader(open(p)):
            out[r["id"] + "|" + r["base"]] = r
    return out


OVERCHARGE = dict(Mg=0.05, Zn=0.15)      # relative extra to weigh in, until the first ICP result says otherwise


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cal = load_calphad()
    rows_r, rows_a, rows_l, rows_d = [], [], [], []
    for sid, s in SEEDS.items():
        wt = s["wt"]
        for base in ("6063", "pure Al"):
            r = recipe(wt, base=base, overcharge=OVERCHARGE)
            rows_r.append(dict(seed=sid, alloy=s["name"], base=base, charge_g=250,
                               weigh="; ".join(f"{k} {v} g" for k, v in r["masses"].items()),
                               melt_wt="-".join(f"{v:g}{k}" for k, v in sorted(r["melt_wt"].items(), key=lambda kv: -kv[1]))))
        melt = recipe(wt, base="6063")["melt_wt"]
        c = cal.get(f"{s['calphad']}|6063") or cal.get(f"{s['calphad']}|pureAl") or {}
        if not c:
            print("no CALPHAD row for", sid, "- using defaults")
        num = lambda key, default: float(c[key]) if c.get(key) not in (None, "", "nan") else default  # noqa: E731
        T_top = num("highest_liquidus_C", 660.0)        # first solid of any kind, either database
        T_fcc = num("T_fcc_start_C", 650.0)
        T_end = num("T_end_C", T_fcc - 40.0)
        T_set = num("melt_setpoint_C", max(T_top + 100.0, 820.0))
        sig, rho = melt_props(melt, T_set)
        d50 = lang_d50(sig, rho)
        dh60 = droplet_history(melt, 60.0, T_set, T_fcc, T_end)
        dh30 = droplet_history(melt, 30.0, T_set, T_fcc, T_end)
        cl = crucible_loss(melt, T_set, hold_min=15.0)
        rows_a.append(dict(
            seed=sid, alloy=s["name"], highest_liquidus_C=round(T_top), highest_liquidus_phase=c.get("highest_liquidus_phase", ""),
            alpha_start_C=round(T_fcc), melt_setpoint_C=round(T_set),
            surface_tension_N_m=round(sig, 3), density_kg_m3=round(rho), lang_d50_um=round(d50, 1),
            d50_20kHz_um=round(lang_d50(sig, rho, 20e3), 1), d50_60kHz_um=round(lang_d50(sig, rho, 60e3), 1),
            frac_below_45=round(cut_fraction(d50, 1, 45), 2), frac_20_63=round(cut_fraction(d50, 20, 63), 2),
            frac_20_75=round(cut_fraction(d50, 20, 75), 2), frac_63_150=round(cut_fraction(d50, 63, 150), 2),
            cool_rate_60um_K_s=f"{dh60['cool_rate_K_s']:.1e}", cool_rate_30um_K_s=f"{dh30['cool_rate_K_s']:.1e}",
            liquid_time_60um_ms=round(dh60["liquid_time_ms"], 1),
            flight_loss_60um="; ".join(f"{e} {100 * v:.1f}%" for e, v in dh60["loss"].items()) or "none",
            crucible_loss_15min="; ".join(f"{e} {100 * v:.2f}%" for e, v in cl.items()) or "none",
        ))
        for layer in (30.0, 50.0):
            tr = transfer(melt, T_fcc, s["ref"], layer=layer, plate_C=s["plate"])
            rows_l.append(dict(seed=sid, alloy=s["name"], layer_um=int(layer), plate_C=s["plate"], k_W_mK=tr["k"],
                               ref=f"{s['ref']['P']} W, {s['ref']['v']} mm/s, {s['ref']['h']} um hatch, {s['ref']['t']} um layer, {s['ref']['spot']} um spot",
                               ref_pool_d_um=tr["ref_d"], ref_depth_per_layer=tr["ref_d_per_layer"], ref_enthalpy=tr["ref_enthalpy"],
                               ref_ved_J_mm3=tr["ref_ved"], midi_P_W=int(tr["P"]), midi_v_mm_s=int(tr["v"]), midi_hatch_um=int(tr["h"]),
                               pool_w_um=tr["w"], pool_d_um=tr["d"], depth_per_layer=tr["d_per_layer"], lof_index=tr["lof"],
                               enthalpy=tr["enthalpy"], ved_J_mm3=tr["ved"], direct_age=s["age"], ref_source=s["ref"]["src"]))
            if layer == 50.0:
                for row in doe(melt, T_fcc, tr, plate_C=s["plate"]):
                    rows_d.append(dict(seed=sid, plate_C=s["plate"], **row))
    for name, rows in (("recipes.csv", rows_r), ("atomization.csv", rows_a), ("lpbf_window.csv", rows_l), ("lpbf_doe.csv", rows_d)):
        with open(OUT / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("wrote", name, len(rows))
    for r in rows_r:
        if r["base"] == "6063":
            print(r["seed"], "|", r["weigh"], "| melt:", r["melt_wt"])
    for r in rows_a:
        print(r["seed"], "top liquidus", r["highest_liquidus_C"], r["highest_liquidus_phase"], "set", r["melt_setpoint_C"], "d50", r["lang_d50_um"],
              "<45:", r["frac_below_45"], "20-63:", r["frac_20_63"], "flight", r["flight_loss_60um"], "| crucible", r["crucible_loss_15min"], "| cool", r["cool_rate_60um_K_s"], r["liquid_time_60um_ms"], "ms")
    for r in rows_l:
        print(r["seed"], r["layer_um"], "um: k", r["k_W_mK"], "ref d", r["ref_pool_d_um"], "H", r["ref_enthalpy"], "VED", r["ref_ved_J_mm3"], "->", r["midi_P_W"], "W",
              r["midi_v_mm_s"], "mm/s hatch", r["midi_hatch_um"], "| w", r["pool_w_um"], "d", r["pool_d_um"], "LOF", r["lof_index"], "H", r["enthalpy"], "VED", r["ved_J_mm3"])


if __name__ == "__main__":
    main()
