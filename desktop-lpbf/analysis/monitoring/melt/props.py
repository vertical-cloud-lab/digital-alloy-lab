"""Temperature-dependent properties of the alloys the desktop LPBF screens (issue #260; monitoring/melt-pool.md).

One place for every property the melt-pool scripts use, with its source. Values are SI (K, kg, m, s, W, J, Pa).

Alloys: pure Al (reference), AlSi10Mg, 6061, 7075. What is measured and what is estimated:
  - solidus / liquidus: ASM Handbook Vol. 2 (1990) for 6061 (582 / 652 C) and 7075 (477 / 635 C); AlSi10Mg 557 / 596 C as used
    elsewhere in this repo (preheat-and-plates.md, monitoring.md). Pure Al melts at 933.47 K.
  - solid k(T), cp(T): pure Al from Incropera & DeWitt, Fundamentals of Heat and Mass Transfer, Table A.1 (300-800 K, extended to
    the melting point); the alloys from their room-temperature handbook values (ASM Vol. 2: 6061-T6 167 W/m K, 896 J/kg K;
    7075-T6 130 W/m K, 960 J/kg K) with the temperature trend that solid-solution alloys show (k rises with T because impurity
    scattering dominates; cp follows Al's curve). AlSi10Mg: 150 W/m K, the value for LPBF material aged in place at a 200 C
    plate (as-built material is lower, ~110-130 W/m K; heat-treated higher, ~170). These are estimates good to ~10-15 %.
  - liquid k(T): Wiedemann-Franz, k = L0 T / rho_e(T), with liquid Al's resistivity 24.2 uOhm cm at the melting point rising
    0.0145 uOhm cm/K (Leitner et al. 2017, https://doi.org/10.1007/s11661-017-4053-6, report liquid Al's k ~ 90-100 W/m K near
    melting, which this reproduces). For the alloys the resistivity at the liquidus is raised by the solute (estimates:
    AlSi10Mg 30, 6061 26, 7075 30 uOhm cm), giving 70-87 W/m K at the liquidus.
  - density: room-temperature values (ASM; EOS for AlSi10Mg); liquid Al 2377 - 0.311 (T - 933.47) kg/m3 (Assael et al. 2006,
    https://doi.org/10.1063/1.2149380). The melt-pool models carry a constant mass density (so mass flux is conserved in the moving
    frame) and put the temperature dependence into cp per kg.
  - latent heat of fusion: Al 397 kJ/kg (10.71 kJ/mol). 6061 390 and 7075 380 kJ/kg (mixture estimates). AlSi10Mg 450 kJ/kg: Si's
    latent heat (1.79 MJ/kg) raises it above Al's; published values for Al-(7-12)Si alloys run ~420-500 kJ/kg (estimate).
  - boiling and evaporation: vapour pressures of the pure elements, Al from Alcock, Itkin & Horrigan (1984, Can. Metall. Q. 23:309,
    https://doi.org/10.1179/cmq.1984.23.3.309) liquid equation log10(p/atm) = 5.911 - 16211/T (gives T_b = 2743 K; the CRC Handbook
    lists 2792 K), extrapolated above its 1800 K range; Mg, Zn, Si and Cu by Clausius-Clapeyron from the normal boiling point and
    the enthalpy of vaporisation (CRC Handbook: Mg 1363 K / 127.4 kJ/mol; Zn 1180 K / 115.3 kJ/mol; Si 3538 K / 359 kJ/mol;
    Cu 2835 K / 300.4 kJ/mol). The Zn line matches Alcock's liquid Zn equation (repo's preheat_500.py) to 3 % at 1000 K.
    Partial pressures over the alloy use Raoult's law (activity = mole fraction), an approximation: Mg in liquid Al deviates
    negatively and Zn positively, each by up to a factor of ~2.
  - surface tension: liquid Al 0.914 - 0.35e-3 (T - T_m) N/m (Smithells Metals Reference Book, 7th ed., Brandes & Brook 1992,
    ch. 14). Oxide films and Mg change both numbers; LPBF models of AlSi10Mg use 0.8-0.9 N/m and dsigma/dT -0.2 to -0.35 mN/m K.
  - viscosity: liquid Al log10(mu / mPa s) = -0.7324 + 803.49/T (Assael et al. 2006); used for all alloys.
  - powder bed: 50 % packing (budgets.py), effective k 0.2 W/m K in argon (Al and steel powder beds measure 0.1-0.3 W/m K at room
    temperature, e.g. Rombouts et al. 2005, https://doi.org/10.1063/1.1948509; radiation adds < 0.01 W/m K at the particle size).
  - absorptivity at 1070 nm: see ABSORPTIVITY below (by regime); the melt-pool scripts treat it as the main unknown.
"""
from __future__ import annotations

import math

import numpy as np

R_GAS = 8.314462618
K_B = 1.380649e-23
SIGMA_SB = 5.670374419e-8
ATM = 101325.0
L0_WF = 2.44e-8                 # Sommerfeld Lorenz number, W Ohm / K^2

# molar masses, kg/mol
M = {"Al": 26.9815e-3, "Si": 28.0855e-3, "Mg": 24.305e-3, "Zn": 65.38e-3, "Cu": 63.546e-3, "Fe": 55.845e-3, "Cr": 51.996e-3}

# enthalpy of vaporisation (J/mol) and normal boiling point (K) for Clausius-Clapeyron (CRC Handbook)
VAP_CC = {"Mg": (127.4e3, 1363.0), "Zn": (115.3e3, 1180.0), "Si": (359.0e3, 3538.0), "Cu": (300.4e3, 2835.0)}
AL_ALCOCK = (5.911, -16211.0)   # log10(p/atm) = A + B/T, liquid Al
L_VAP = {"Al": 294.0e3, "Mg": 127.4e3, "Zn": 115.3e3, "Si": 359.0e3, "Cu": 300.4e3}   # J/mol, for the evaporative heat sink


def p_sat(el, T):
    """Equilibrium vapour pressure of the pure liquid element (Pa)."""
    T = np.asarray(T, dtype=float)
    if el == "Al":
        A, B = AL_ALCOCK
        return ATM * 10.0 ** (A + B / T)
    dH, Tb = VAP_CC[el]
    return ATM * np.exp(dH / R_GAS * (1.0 / Tb - 1.0 / T))


# ------------------------------------------------------------------------------------------------------------------ alloys
# k_s: (T K, W/m K) points; cp_s: room-temperature value, scaled onto Al's curve; rho_e_l: liquid resistivity at T_liq (Ohm m)
ALLOYS = {
    # pure Al melts at 933.47 K; the solver spreads it over 928.5-938.5 K
    "Al": dict(label="pure Al", wt={"Al": 100.0}, T_sol=928.5, T_liq=938.5, rho=2700.0, rho_l=2375.0,
               k_s=[(300, 237.0), (400, 240.0), (600, 231.0), (800, 218.0), (933, 211.0)], cp_rt=903.0, cp_l=1177.0,
               L_f=397.0e3, rho_e_l=24.2e-8),
    "AlSi10Mg": dict(label="AlSi10Mg", wt={"Al": 89.45, "Si": 10.0, "Mg": 0.35, "Fe": 0.2}, T_sol=830.15, T_liq=869.15,
                     rho=2670.0, rho_l=2450.0,
                     k_s=[(300, 150.0), (500, 155.0), (700, 158.0), (830, 155.0)], cp_rt=880.0, cp_l=1150.0,
                     L_f=450.0e3, rho_e_l=30.0e-8),
    "6061": dict(label="6061", wt={"Al": 97.72, "Mg": 1.0, "Si": 0.6, "Cu": 0.28, "Cr": 0.2, "Fe": 0.2}, T_sol=855.15,
                 T_liq=925.15, rho=2700.0, rho_l=2390.0,
                 k_s=[(300, 167.0), (400, 177.0), (600, 186.0), (800, 190.0), (855, 189.0)], cp_rt=896.0, cp_l=1170.0,
                 L_f=390.0e3, rho_e_l=26.0e-8),
    "7075": dict(label="7075", wt={"Al": 89.87, "Zn": 5.6, "Mg": 2.5, "Cu": 1.6, "Cr": 0.23, "Fe": 0.2}, T_sol=750.15,
                 T_liq=908.15, rho=2810.0, rho_l=2470.0,
                 k_s=[(300, 130.0), (400, 145.0), (600, 160.0), (750, 163.0)], cp_rt=960.0, cp_l=1150.0,
                 L_f=380.0e3, rho_e_l=30.0e-8),
}

# pure Al cp (Incropera Table A.1), J/kg K: the shape used for every alloy
_CP_AL = [(300, 903.0), (400, 949.0), (600, 1033.0), (800, 1146.0), (933, 1200.0)]

ABSORPTIVITY = {
    # A at 1070 nm, by regime. Ranges; the scripts sweep them.
    "flat_melt": (0.06, 0.10, "liquid Al, normal incidence (Drude estimate; Gan et al. 2021's eta_m concept)"),
    "powder_conduction": (0.15, 0.30, "Al powder layer before a vapour depression forms (multiple scattering roughly doubles the flat value; "
                                      "Trapp et al. 2017, https://doi.org/10.1016/j.apmt.2017.08.006, saw ~2x for powder vs bare at low power)"),
    "transition": (0.30, 0.50, "vapour depression forming"),
    "keyhole": (0.50, 0.70, "keyhole: multiple reflection; Gan et al. 2021 Eq. 6 saturates at 0.7"),
}


def mole_fractions(alloy):
    wt = ALLOYS[alloy]["wt"]
    n = {el: w / M[el] for el, w in wt.items()}
    s = sum(n.values())
    return {el: v / s for el, v in n.items()}


def mean_molar_mass(alloy):
    x = mole_fractions(alloy)
    return sum(x[el] * M[el] for el in x)


class Alloy:
    """Property functions for one alloy. Arrays in, arrays out."""

    def __init__(self, name, k_liquid_factor=1.0):
        d = ALLOYS[name]
        self.name, self.d = name, d
        self.label = d["label"]
        self.T_sol, self.T_liq = d["T_sol"], d["T_liq"]
        self.rho, self.rho_l = d["rho"], d["rho_l"]
        self.L_f = d["L_f"]
        self.cp_l = d["cp_l"]
        self.f_kl = k_liquid_factor
        self._kT = np.array([p[0] for p in d["k_s"]], float)
        self._kv = np.array([p[1] for p in d["k_s"]], float)
        cpT = np.array([p[0] for p in _CP_AL], float)
        cpv = np.array([p[1] for p in _CP_AL], float) * d["cp_rt"] / _CP_AL[0][1]
        self._cpT, self._cpv = cpT, cpv
        self.x = mole_fractions(name)
        self.M_mean = mean_molar_mass(name)
        # liquid conductivity (Wiedemann-Franz) at T_liq
        self.k_l_liq = L0_WF * self.T_liq / d["rho_e_l"]
        # enthalpy table (J/kg, 0 at 298.15 K) on a fine grid for H(T) and its inverse
        self._Tg = np.linspace(250.0, 6000.0, 23001)
        self._Hg = self._build_H(self._Tg)

    # ---- solid / liquid pieces
    def cp_solid(self, T):
        T = np.asarray(T, float)
        Tc = np.clip(T, self._cpT[0], self.T_sol)
        out = np.interp(Tc, self._cpT, self._cpv)
        # beyond the table (alloys whose solidus is below 933 K use the table up to it; Al's table ends at 933 K)
        return out

    def fl(self, T):
        """Liquid fraction between solidus and liquidus: a smooth step (3s^2 - 2s^3), so the apparent heat capacity is continuous
        at both ends (the melt-pool solver's Newton iteration needs that). The lever rule is linear; Scheil-type solidification
        puts more of the latent heat near the liquidus. Either is an assumption."""
        T = np.asarray(T, float)
        s = np.clip((T - self.T_sol) / (self.T_liq - self.T_sol), 0.0, 1.0)
        return s * s * (3.0 - 2.0 * s)

    def k_solid(self, T):
        T = np.asarray(T, float)
        return np.interp(np.clip(T, self._kT[0], self._kT[-1]), self._kT, self._kv)

    def k_liquid(self, T, factor=None):
        f = self.f_kl if factor is None else factor
        T = np.maximum(np.asarray(T, float), self.T_liq)
        rho_e = self.d["rho_e_l"] + 0.0145e-8 * (T - self.T_liq)
        return f * L0_WF * T / rho_e

    def k(self, T, factor=None):
        """Bulk conductivity, with the Marangoni enhancement factor applied to the liquid (T > T_liq) only and ramped across the
        mushy zone by liquid fraction (so it is continuous)."""
        T = np.asarray(T, float)
        fl = self.fl(T)
        ks = self.k_solid(np.minimum(T, self.T_sol))
        kl = self.k_liquid(np.maximum(T, self.T_liq), factor)
        return (1 - fl) * ks + fl * kl

    def cp_sensible(self, T):
        T = np.asarray(T, float)
        return np.where(T <= self.T_sol, self.cp_solid(T),
                        np.where(T >= self.T_liq, self.cp_l,
                                 (1 - self.fl(T)) * self.cp_solid(self.T_sol) + self.fl(T) * self.cp_l))

    def _build_H(self, Tg):
        cp = self.cp_sensible(Tg)
        # latent heat spread over the mushy zone (lever rule); pure Al has a 1 K interval
        dfl = np.gradient(self.fl(Tg), Tg)
        c_app = cp + self.L_f * dfl
        H = np.concatenate([[0.0], np.cumsum(0.5 * (c_app[1:] + c_app[:-1]) * np.diff(Tg))])
        H -= np.interp(298.15, Tg, H)
        return H

    def H(self, T):
        """Specific enthalpy (J/kg) relative to 298.15 K, latent heat included."""
        return np.interp(np.asarray(T, float), self._Tg, self._Hg)

    def T_of_H(self, H):
        return np.interp(np.asarray(H, float), self._Hg, self._Tg)

    def c_app(self, T):
        """Apparent heat capacity dH/dT (J/kg K)."""
        T = np.asarray(T, float)
        return np.interp(T, self._Tg, np.gradient(self._Hg, self._Tg))

    def alpha(self, T):
        return self.k(T) / (self.rho * self.cp_sensible(T))

    # ---- averaged ("sensible") properties for the analytical models
    def mean_props(self, T0, T_hi=None):
        """Properties averaged from T0 to T_hi (default the liquidus): k, cp and diffusivity, plus the enthalpy to melt."""
        T_hi = self.T_liq if T_hi is None else T_hi
        Tg = np.linspace(T0, T_hi, 400)
        k = float(np.trapezoid(self.k(Tg), Tg) / (T_hi - T0))
        cp = float((self.H(T_hi) - self.H(T0) - (self.L_f if T_hi >= self.T_liq else 0.0)) / (T_hi - T0))
        return dict(k=k, cp=cp, alpha=k / (self.rho * cp), dH_melt=float(self.H(self.T_liq) - self.H(T0)))

    # ---- surface physics
    def sigma(self, T):
        return 0.914 - 0.35e-3 * (np.asarray(T, float) - 933.47)

    dsigma_dT = -0.35e-3

    def mu(self, T):
        return 1e-3 * 10.0 ** (-0.7324 + 803.49 / np.asarray(T, float))

    def partial_pressures(self, T, f_vol=1.0):
        """Raoult's-law partial pressures (Pa) of the volatile elements over the liquid alloy. f_vol scales the surface activity of
        Mg and Zn (1 = bulk composition; < 1 = a surface depleted of them)."""
        out = {}
        for el, xi in self.x.items():
            if el in ("Fe", "Cr"):
                continue
            out[el] = xi * p_sat(el, T) * (f_vol if el in ("Mg", "Zn") else 1.0)
        return out

    def p_total(self, T, f_vol=1.0):
        return sum(self.partial_pressures(T, f_vol).values())

    def T_boil(self, p=ATM, f_vol=1.0):
        """Temperature at which the alloy's total vapour pressure (Raoult) reaches p: its effective boiling point."""
        lo, hi = 800.0, 4000.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if self.p_total(mid, f_vol) > p:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    def evap_flux(self, T, beta=0.82, f_vol=1.0):
        """Hertz-Knudsen-Langmuir mass flux of each element (kg/m2 s) with the fraction (1 - beta) recondensing (Anisimov 1968:
        ~18 % return in strong evaporation, so beta = 0.82). An upper bound below the boiling point, where vapour has to diffuse
        out through the argon."""
        T = np.asarray(T, float)
        pp = self.partial_pressures(T, f_vol)
        return {el: beta * p * np.sqrt(M[el] / (2 * math.pi * R_GAS * T)) for el, p in pp.items()}

    def evap_heat_flux(self, T, beta=0.82, f_vol=1.0):
        J = self.evap_flux(T, beta, f_vol)
        return sum(J[el] / M[el] * L_VAP[el] for el in J)

    def recoil_pressure(self, T):
        """Anisimov (1968): recoil pressure ~0.54 of the saturated vapour pressure in strong evaporation."""
        return 0.54 * self.p_total(T)


def summary_table():
    rows = []
    for name in ALLOYS:
        a = Alloy(name)
        mp = a.mean_props(298.15)
        rows.append(dict(alloy=name, T_sol_C=a.T_sol - 273.15, T_liq_C=a.T_liq - 273.15, freezing_range_K=a.T_liq - a.T_sol,
                         T_boil_alloy_C=a.T_boil() - 273.15, k_s_300=float(a.k_solid(300.0)), k_s_sol=float(a.k_solid(a.T_sol)),
                         k_l_liq=a.k_l_liq, cp_rt=float(a.cp_solid(300.0)), L_f_kJkg=a.L_f / 1e3,
                         dH_melt_from_25C_kJkg=mp["dH_melt"] / 1e3, k_mean=mp["k"], cp_mean=mp["cp"], alpha_mean=mp["alpha"],
                         x=a.x))
    return rows


if __name__ == "__main__":
    for r in summary_table():
        print(f"{r['alloy']:9s} sol {r['T_sol_C']:6.1f} C liq {r['T_liq_C']:6.1f} C (dT {r['freezing_range_K']:5.1f} K)  "
              f"T_boil(alloy, Raoult) {r['T_boil_alloy_C']:7.1f} C  k_s 300K {r['k_s_300']:5.0f}  k_s(sol) {r['k_s_sol']:5.0f}  "
              f"k_l(liq) {r['k_l_liq']:5.1f}  H_melt {r['dH_melt_from_25C_kJkg']:6.0f} kJ/kg  k_mean {r['k_mean']:5.0f} "
              f"cp_mean {r['cp_mean']:5.0f} alpha {r['alpha_mean'] * 1e6:5.1f} mm2/s")
    a = Alloy("Al")
    for T in (1500, 2000, 2500, 2743, 3000):
        print(T, {el: f"{p / ATM:.3g} atm" for el, p in {e: p_sat(e, T) for e in ("Al", "Mg", "Zn", "Si", "Cu")}.items()})
