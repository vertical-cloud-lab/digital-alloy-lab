"""First-principles keyhole and melt-pool model, version 2 (PR #249, issue #235).

Version 1 (scripts/keyhole_first_principles.py) listed what it left out. This version adds them, still with
nothing fitted to keyhole or melt-pool data:

1. **Mg and Si in the vapour.** The wall temperature is where the alloy's total vapour pressure,
   sum_i gamma_i x_i p_i°(T), equals the keyhole pressure. p_i° are the pure elements' vapour pressures from
   NIST-JANAF (Kirchhoff integration from each normal boiling point, with the liquid and gas heat capacities);
   gamma_i are activity coefficients in the liquid from pycalphad + MatCalc mc_al
   (scripts/keyhole_fp_liquid_activities_mc_al.py). Mg's vapour pressure is about 200 times Al's, but Mg leaves
   the wall faster than the melt can bring it, so the wall is depleted. Its surface mole fraction follows from a
   mass balance: Mg carried out in the vapour = Mg brought to the wall by the melt flowing past it (potential
   flow around a cylinder, Boussinesq's Sh = 1.128 Pe^1/2) at the keyhole wall, or under the beam (penetration
   theory against the Hertz-Knudsen flux) on the flat surface at keyhole onset.
2. **A tilted keyhole** (scripts/keyhole_fp_shaped.py): a cone whose opening is the beam's 1/e^2 radius, as in
   version 1, with its front wall leaning back at Kaplan's (1994) angle, where the direct beam it catches at
   mid-depth balances its conduction loss (solve_parametric, tilt="kaplan"); the depth from the global balance.
   Every stable depth of that balance is found (cone_roots): above the power where the surface first boils there
   can be a shallow dimple and one or more deeper keyholes. The pool is the shallowest state's (the deepest's in a
   sensitivity run), and a map point is called a keyhole wherever a stable state with Wk/Dk <= 0.7 exists
   (run_maps_v2, v2_class_deep_branch). A free-form shape from Kaplan's point-by-point balance (solve_shaped, the
   `explore` command) was tried and not adopted: it drives the keyhole to a funnel and worsens the X-ray depths.
3. **A powder layer** (scripts/keyhole_fp_powder.py), for the part of the beam that falls ahead of the melt.
4. **Sourced properties** that version 1 took from handbooks: the liquid resistivity of the hypereutectic blend
   and of Gan et al.'s alloys, and the solid conductivity against temperature.
5. **Melt flow** (scripts/keyhole_meltflow.py): a 3D steady-state Navier-Stokes and energy solver in the beam
   frame, with Marangoni shear on the flat surface and the keyhole from item 2 as a fixed cavity at T_w.

Usage (from the repo root):

    python scripts/keyhole_first_principles_v2.py point --alloy blend --P 375 --v 0.4
    python scripts/keyhole_first_principles_v2.py all
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
from scipy import optimize

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import keyhole_first_principles as fp  # noqa: E402
import keyhole_fp_shaped as sh  # noqa: E402

REPO = fp.REPO
V2_DIR = fp.FP_DIR / "v2"
ACT_CSV = V2_DIR / "mc_al-liquid-activity-coefficients.csv"
R = fp.R_GAS
P_AMB = fp.P_AMB

# --- vapour pressure of the pure elements: NIST-JANAF -----------------------------------------------------
# At the "LIQUID <--> IDEAL GAS, FUGACITY = 1 bar" row of each reference-state table: T_b, the liquid and gas
# H - H°(298.15 K) (kJ/mol) and Cp (J/mol/K). Read through the lab's browser route (janaf.nist.gov, tables Al-001,
# Mg-001 and Si-001).
JANAF = {
    "Al": {"T_b": 2790.812, "H_l": 87.665e3, "H_g": 381.667e3, "cp_l": 31.751, "cp_g": 20.795, "M": 26.9815385e-3},
    "Mg": {"T_b": 1366.104, "H_l": 41.431e3, "H_g": 169.298e3, "cp_l": 34.309, "cp_g": 20.786, "M": 24.305e-3},
    "Si": {"T_b": 3504.616, "H_l": 135.673e3, "H_g": 520.221e3, "cp_l": 27.196, "cp_g": 23.023, "M": 28.0855e-3},
}
P_JANAF = 1e5  # JANAF's standard-state pressure, Pa


def p_pure(el: str, T):
    """Vapour pressure of the pure liquid element (Pa): Clausius-Clapeyron integrated with Kirchhoff's law,
    dH_vap(T) = dH_b + dCp (T - T_b), from JANAF's 1-bar boiling point."""
    j = JANAF[el]
    dH = j["H_g"] - j["H_l"]
    dcp = j["cp_g"] - j["cp_l"]
    T = np.asarray(T, dtype=float)
    ln_p = (dH - dcp * j["T_b"]) / R * (1.0 / j["T_b"] - 1.0 / T) + dcp / R * np.log(T / j["T_b"])
    return P_JANAF * np.exp(ln_p)


# --- activity coefficients in the liquid (pycalphad + mc_al) -------------------------------------------
_ACT = None


_GAM: dict = {}


def gammas(alloy: str, T: float) -> dict:
    """gamma_Al, gamma_Si at the bulk composition and gamma_Mg in the dilute limit (a depleted wall), at T.
    Linear in T between the tabulated 100 K steps (1000-3600 K); held constant outside."""
    global _ACT
    if alloy not in _GAM:
        if _ACT is None:
            _ACT = pd.read_csv(ACT_CSV)
        tab = {}
        for el, variant in (("al", "bulk"), ("si", "bulk"), ("mg", "dilute_mg")):
            d = _ACT[(_ACT["alloy"] == alloy) & (_ACT["variant"] == variant)].sort_values("T_K")
            if d.empty or f"gamma_{el}" not in d or d[f"gamma_{el}"].isna().all():
                continue
            tab[el.capitalize()] = (d["T_K"].to_numpy(), d[f"gamma_{el}"].to_numpy())
        _GAM[alloy] = tab
    return {el: float(np.interp(T, tt, gg)) for el, (tt, gg) in _GAM[alloy].items()}


# --- Mg in the liquid: diffusivity --------------------------------------------------------------------------
# No open measurement of Mg in liquid Al was found (Du et al. 2003 is closed). Proxy: Cu in liquid Al80Cu20,
# measured by in-situ X-ray radiography, D0 = 1.3e-7 m^2/s and Q = 0.34 eV (Zhang, Griesche & Meyer 2009,
# Diffusion Fundamentals 11, 100, doi:10.62721/diffusion-fundamentals.11.552). Extrapolated to the wall's 2,850 K.
MG_D0 = 1.3e-7  # m^2/s
MG_Q = 0.34 * 96485.33212  # J/mol
MG_DIFFUSION_SOURCE = "proxy: Cu in liquid Al80Cu20, Zhang, Griesche & Meyer 2009"


def D_mg(T):
    return MG_D0 * math.exp(-MG_Q / (R * T))


@dataclasses.dataclass
class Vapour:
    """The alloy's vapour at the keyhole wall or the flat surface."""
    alloy: str  # key into the activity table
    x: dict  # bulk atomic fractions, e.g. {"Al": .., "Si": .., "Mg": ..}
    rho_l: callable  # liquid density (kg/m^3) at T
    M: float  # mean molar mass of the liquid, kg/mol
    sigma: float  # surface tension at the wall, N/m
    flow_factor: float = 1.0  # melt speed past the wall, in units of the scan speed (1 = potential flow at v)
    use_mg: bool = True

    def partials(self, T, x_mg_s):
        g = gammas(self.alloy, T)
        p = {}
        for el in ("Al", "Si"):
            if self.x.get(el, 0.0) > 0:
                p[el] = g.get(el, 1.0) * self.x[el] * float(p_pure(el, T))
        if self.use_mg and self.x.get("Mg", 0.0) > 0:
            p["Mg"] = g.get("Mg", 1.0) * x_mg_s * float(p_pure("Mg", T))
        return p

    def _x_mg_wall(self, T, p_kh, n_dot, k_m, A_wall):
        """Surface Mg fraction where Mg leaving in the vapour = Mg brought by the melt."""
        xb = self.x.get("Mg", 0.0)
        if not self.use_mg or xb <= 0:
            return 0.0
        c = float(self.rho_l(T)) / self.M
        g = gammas(self.alloy, T).get("Mg", 1.0)
        demand = n_dot * g * float(p_pure("Mg", T)) / p_kh  # mol/s per unit surface mole fraction
        supply = k_m * c * A_wall
        return xb * supply / (supply + demand)

    def wall(self, a0, a_mean, A_wall, v, n_dot_fn):
        """Wall temperature, surface Mg fraction, vapour mole fractions and Mg loss at a keyhole of opening a0,
        mean radius a_mean and wall area A_wall, moving at v. n_dot_fn(T, M_v) is the molar vapour outflow."""
        p_kh = P_AMB + self.sigma / a0
        u = max(self.flow_factor * v, 1e-6)

        def state(T):
            Dm = D_mg(T)
            k_m = 1.128 * math.sqrt(u * Dm / (2 * a_mean))  # Boussinesq: Sh_D = 1.128 Pe_D^1/2
            x_s = self.x.get("Mg", 0.0)
            for _ in range(30):
                p = self.partials(T, x_s)
                tot = sum(p.values())
                y = {k: val / max(tot, 1e-30) for k, val in p.items()}
                M_v = sum(y[k] * JANAF[k]["M"] for k in y)
                n_dot = n_dot_fn(T, M_v)
                x_new = self._x_mg_wall(T, p_kh, n_dot, k_m, A_wall)
                if abs(x_new - x_s) < 1e-12 + 1e-6 * x_new:
                    x_s = x_new
                    break
                x_s = x_new
            p = self.partials(T, x_s)
            return sum(p.values()) - p_kh, x_s, p, n_dot

        T_w = optimize.brentq(lambda T: state(T)[0], 1200.0, 4500.0, xtol=1e-3)
        _, x_s, p, n_dot = state(T_w)
        tot = sum(p.values())
        y = {k: val / tot for k, val in p.items()}
        return {"T_w": T_w, "x_mg_surface": x_s, "x_mg_bulk": self.x.get("Mg", 0.0), "y": y,
                "mg_loss_mol_s": n_dot * y.get("Mg", 0.0), "p_kh": p_kh, "n_dot_mol_s": n_dot}

    def T_at_pressure(self, p, x_mg_s):
        """Temperature at which the vapour over a surface with Mg fraction x_mg_s reaches pressure p."""
        return optimize.brentq(lambda T: sum(self.partials(T, x_mg_s).values()) - p, 1200.0, 6000.0, xtol=1e-3)

    def onset(self, r0, v, p=P_AMB):
        """Boiling temperature of the flat surface under the beam: Mg at the surface depleted by the
        Hertz-Knudsen flux (an upper bound on its loss) against supply by diffusion over the beam's dwell
        (penetration theory, contact time 2 r0 / v)."""
        t_c = 2 * r0 / max(v, 1e-6)

        def f(T):
            xb = self.x.get("Mg", 0.0)
            x_s = 0.0
            if self.use_mg and xb > 0:
                c = float(self.rho_l(T)) / self.M
                k_m = 2 * math.sqrt(D_mg(T) / (math.pi * t_c))
                g = gammas(self.alloy, T).get("Mg", 1.0)
                J = g * float(p_pure("Mg", T)) / math.sqrt(2 * math.pi * JANAF["Mg"]["M"] * R * T)
                x_s = xb * k_m * c / (k_m * c + J)
            return sum(self.partials(T, x_s).values()) - p, x_s

        T = optimize.brentq(lambda T: f(T)[0], 1200.0, 4500.0, xtol=1e-3)
        return T, f(T)[1]


def vapour_outflow(a0, sigma, T, M_v):
    """Molar outflow of vapour through the opening (mol/s), driven by the Laplace overpressure sigma / a0
    (Bernoulli, capped at choked flow), as in version 1 but for the vapour's own molar mass."""
    dp = sigma / a0
    p_v = P_AMB + dp
    rho_v = p_v * M_v / (R * T)
    u = math.sqrt(2 * dp / rho_v)
    c = math.sqrt(5.0 / 3.0 * R * T / M_v)
    return rho_v * min(u, c) * math.pi * a0 ** 2 / M_v


def dH_vap(el, T):
    j = JANAF[el]
    return (j["H_g"] - j["H_l"]) + (j["cp_g"] - j["cp_l"]) * (T - j["T_b"])


def evaporation_power_v2(wall_state: dict) -> float:
    T = wall_state["T_w"]
    return wall_state["n_dot_mol_s"] * sum(y * dH_vap(el, T) for el, y in wall_state["y"].items())


# --- materials, version 2 ----------------------------------------------------------------------------------

@dataclasses.dataclass
class MaterialV2(fp.Material):
    """Version 1's Material, plus a solid conductivity that can vary with temperature (k_s_table)."""
    k_s_table: tuple | None = None  # (T in K, k in W/m/K), linear in between, held at the ends

    def k(self, T):
        T = np.asarray(T, dtype=float)
        if self.k_s_table is None:
            return super().k(T)
        Tt, kt = self.k_s_table
        ks = np.interp(np.minimum(T, self.T_s), Tt, kt)
        kl = (self.k_l_fixed if self.k_l_fixed is not None
              else fp.L0_WF * np.maximum(T, self.T_l) / self.rho_el_liq(np.maximum(T, self.T_l)))
        f = np.clip((T - self.T_s) / max(self.T_l - self.T_s, 1e-9), 0.0, 1.0)
        return (1 - f) * ks + f * kl


@dataclasses.dataclass
class Alloy:
    key: str
    m: MaterialV2
    vap: Vapour | None
    optics: str = "drude-dc"

    def N(self, T):
        if self.optics.startswith("anchored-"):
            return anchored_index(self.m, T, float(self.optics.split("-", 1)[1]))
        old = fp.OPTICS
        fp.OPTICS = self.optics
        try:
            return fp.optical_index(self.m, T)
        finally:
            fp.OPTICS = old


def anchored_index(m, T, A_target):
    """Sensitivity only: the liquid's Drude index with its damping scaled so that a flat surface absorbs A_target at
    normal incidence (e.g. 0.24, what NIST measured on bare Al 5182 before its keyhole formed). A stand-in for
    whatever (oxide, ripples) makes a real melt absorb more than the clean liquid's Fresnel value."""
    n_e = float(m.electron_density(T))
    wp2 = n_e * fp.E_CH ** 2 / (fp.EPS0 * fp.M_E)
    g0 = fp.EPS0 * wp2 * float(m.rho_el_liq(T))
    A = lambda s_: float(fp.fresnel_absorptance(fp.drude_index_params(wp2, s_ * g0), 1.0)) - A_target  # noqa: E731
    s_ = optimize.brentq(A, 0.05, 50.0)
    return fp.drude_index_params(wp2, s_ * g0)


# --- one process point -------------------------------------------------------------------------------------

WK_DK_AM = fp.WK_DK_AM


@dataclasses.dataclass
class ResultV2:
    mode: str
    A: float
    A_keyhole: float = 0.0
    A_conduction_flat: float = float("nan")
    beam_on_powder: float = 0.0
    a0_um: float = 0.0
    d_um: float = 0.0
    Wk_over_Dk: float = float("nan")
    T_onset: float = float("nan")
    T_w: float = float("nan")
    T_peak_conduction: float = float("nan")
    mg_wall_over_bulk: float = float("nan")
    y_mg_vapour: float = 0.0
    mg_loss_ug_per_s: float = 0.0
    Q_cond_W: float = 0.0
    Q_evap_W: float = 0.0
    residual: float = 0.0
    converged: bool = True
    front_wall_deg: float = float("nan")
    rear_wall_deg: float = float("nan")
    tip_offset_um: float = float("nan")
    shaft_width_um: float = float("nan")
    bistable: bool = False
    d_deep_um: float = float("nan")
    A_deep: float = float("nan")
    pool_depth_um: float = 0.0
    pool_width_um: float = 0.0
    pool_length_um: float = 0.0
    pool_Dh_um: float = 0.0
    pool_depth_solidus_um: float = 0.0
    pool_width_solidus_um: float = 0.0
    pool_length_solidus_um: float = 0.0


def wall_angles(sol):
    """Mean front- and rear-wall angles from the vertical over the upper 80 % of the depth, the tip's offset
    behind the beam axis, and the shaft width (mean cross-section diameter between 25 and 75 % of the depth)."""
    zn, xcn, rn = sol["zn"], sol["xcn"], sol["rn"]
    xf, xr = xcn + rn, xcn - rn
    d = zn[-1]
    sel = zn <= 0.8 * d + 1e-15
    zz = zn[sel]
    ang_f = math.degrees(math.atan2(xf[sel][0] - xf[sel][-1], zz[-1] - zz[0])) if zz.size > 1 else float("nan")
    ang_r = math.degrees(math.atan2(xr[sel][-1] - xr[sel][0], zz[-1] - zz[0])) if zz.size > 1 else float("nan")
    low = (zn >= 0.25 * d) & (zn <= 0.75 * d)
    shaft = float(2 * rn[low].mean()) if low.any() else float("nan")
    return ang_f, ang_r, float(xcn[-1]), shaft


def keyhole_field(sol, th, v):
    zs, xs, q = sol["zs"], sol["xs"], sol["q"]
    wx, wy, wq = sol["wings"]

    def field(x, y, z):
        out = fp.point_source_field(x, y, z, zs, q, th.k, th.kappa, v, src_x=xs, src_y=np.zeros_like(xs))
        if wq.size:
            out = out + fp.point_source_field(x, y, z, np.zeros_like(wq), wq, th.k, th.kappa, v, src_x=wx,
                                              src_y=wy, surface=True)
        return out
    return field


CURVATURE = False  # wall temperature from each cross-section's own Laplace pressure, sigma / r


def wall_theta_fn(al: Alloy, T0, ws):
    """theta_w(r): the wall's temperature rise where the keyhole's cross-section has radius r. The vapour must
    hold the wall open against sigma / r, so a narrower section boils hotter. Tabulated in log(r)."""
    m = al.m
    radii = np.geomspace(0.2e-6, 2e-3, 60)
    if al.vap is not None:
        x_s = ws["x_mg_surface"] if ws is not None else 0.0
        Ts = np.array([al.vap.T_at_pressure(P_AMB + m.sigma / r, x_s) for r in radii])
    else:
        Ts = np.array([m.T_boil(P_AMB + m.sigma / r) for r in radii])
    lr = np.log(radii)

    def f(r):
        return float(np.interp(math.log(max(r, radii[0])), lr, Ts)) - T0
    return f


def solve_point_v2(al: Alloy, P, v, r0, T0, A_override=None, hatch=None, want_pool=True, powder=None,
                   deep_branch=True, n_rays=20000, log=None, shape_model="cone") -> tuple[ResultV2, dict]:
    """Solve one (P, v) point. Returns the result and the shaped-keyhole solution (or {} in conduction mode)."""
    m = al.m
    if al.vap is not None:
        T_on, _ = al.vap.onset(r0, v)
    else:
        T_on = m.T_w_fixed if m.T_w_fixed is not None else m.T_boil()
    th_b = fp.thermal_state(m, T0, T_on)
    N_on = al.N(T_on)
    A_liq = float(fp.fresnel_absorptance(N_on, 1.0)) if A_override is None else A_override
    A_c, f_pow = A_liq, 0.0
    if powder is not None and A_override is None:
        A_c, f_pow = powder.conduction_absorptance(A_liq, P, v, r0, th_b)
    if A_COND is not None and A_override is None:
        A_c = A_COND  # sensitivity only: the conduction-mode absorptance fixed (the keyhole branch keeps its own)
    xs = np.linspace(-3 * r0, 1.0 * r0, 41)
    theta_peak = float(fp.gaussian_field(xs, 0.0, 0.0, A_c * P, r0, th_b.k, th_b.kappa, v).max())
    res = ResultV2(mode="conduction", A=A_c, A_conduction_flat=A_liq, beam_on_powder=f_pow, T_onset=T_on,
                   T_peak_conduction=T0 + theta_peak)
    if theta_peak < th_b.theta_w:
        if want_pool:
            field = lambda x, y, z: fp.gaussian_field(x, y, z, A_c * P, r0, th_b.k, th_b.kappa, v)  # noqa: E731
            D, W, L, Dh = fp.pool_dimensions(field, th_b.theta_l, r0, hatch)
            res.pool_depth_um, res.pool_width_um, res.pool_length_um, res.pool_Dh_um = D * 1e6, W * 1e6, L * 1e6, Dh * 1e6
            D, W, L, _ = fp.pool_dimensions(field, th_b.theta_s, r0)
            res.pool_depth_solidus_um, res.pool_width_solidus_um, res.pool_length_solidus_um = D * 1e6, W * 1e6, L * 1e6
        return res, {}

    a0 = r0
    # Wall state (temperature, Mg) for a first-guess keyhole two openings deep. It isn't iterated with the depth:
    # the final depth would move the wall by under 3 K for our alloys and up to 10 K for Al 5182 (0.4 % of its rise).
    if al.vap is not None:
        ws = al.vap.wall(a0, 0.5 * a0, math.pi * a0 * math.sqrt(a0 ** 2 + (2 * a0) ** 2), v,
                         lambda T, Mv: vapour_outflow(a0, m.sigma, T, Mv))
        T_w, Q_e = ws["T_w"], evaporation_power_v2(ws)
    else:
        T_w = fp.wall_temperature(m, a0)
        Q_e = fp.evaporation_power(m, a0, T_w)
        ws = None
    th = fp.thermal_state(m, T0, T_w)
    N = al.N(T_w)
    tab = ray_table_N(N)
    f = cone_balance(P, v, r0, a0, th, Q_e, tab, A_override)
    roots = cone_roots(f, a0, r0)
    d = roots["shallow"]
    if deep_branch and roots["deep"] is not None and roots["deep"] > 1.3 * d:
        res.bistable = True
        res.d_deep_um = roots["deep"] * 1e6
        res.A_deep = roots["A_deep"]
        if BRANCH == "deepest":
            d = roots["deep"]  # sensitivity: the track sits on its deepest stable state wherever there are several
    # The tilt: Kaplan's front-wall balance, for a keyhole deeper than its opening is wide
    wing = lambda a0_, Qs: fp.surface_wing_sources(a0_, r0, Qs)  # noqa: E731
    evap = lambda a0_: Q_e  # noqa: E731
    x_tip = 0.0
    if shape_model == "free" and d > 0.3 * a0:
        sol = sh.solve_shaped(P, v, r0, a0, N, th, evap, wing, fp.point_source_field, A_override=A_override,
                              d_init=d, n_rays=n_rays)
        ang_f, ang_r, tip, shaft = wall_angles(sol)
        sol["x_tip"] = tip
    elif TILT and d > a0:
        sol = sh.solve_parametric(P, v, r0, a0, N, th, evap, wing, fp.point_source_field, A_override=A_override,
                                  d_init=d, p_init=1.0, n_rays=n_rays, max_iter=25, tilt="kaplan")
        if abs(sol["d"] - d) > 0.3 * d:  # jumped to another branch: keep the cone's depth, tilt it there
            x_tip = sh.kaplan_tip(P, r0, a0, d, 0.0, N, th, v)
            x_tip = sh.kaplan_tip(P, r0, a0, d, 0.5 * x_tip, N, th, v)
            sol = sh.solve_parametric_eval(P, v, r0, a0, N, th, evap, wing, fp.point_source_field, A_override, d,
                                           1.0, x_tip, 32, n_rays, 11, None)
    else:
        sol = sh.solve_parametric_eval(P, v, r0, a0, N, th, evap, wing, fp.point_source_field, A_override, d, 1.0,
                                       0.0, 32, n_rays, 11, None)
        sol["converged"] = True
    res.mode = "keyhole"
    res.A = sol["A_kh"] + sol["A_sf"]
    res.A_keyhole = sol["A_kh"]
    res.a0_um, res.d_um = a0 * 1e6, sol["d"] * 1e6
    res.Wk_over_Dk = 2 * a0 / sol["d"]
    res.T_w = T_w
    res.Q_cond_W, res.Q_evap_W = sol["Q_c"], sol["Q_e"]
    res.residual = sol["resid"]
    res.converged = bool(sol.get("converged", True)) and roots["ok"]
    if shape_model == "free" and "tan_f" not in sol and d > 0.3 * a0:
        res.front_wall_deg, res.rear_wall_deg, tip, shaft = wall_angles(sol)
        res.tip_offset_um, res.shaft_width_um = tip * 1e6, shaft * 1e6
    else:
        res.front_wall_deg = math.degrees(math.atan2(a0 - sol["x_tip"], sol["d"]))
        res.rear_wall_deg = math.degrees(math.atan2(a0 + sol["x_tip"], sol["d"]))
        res.tip_offset_um = sol["x_tip"] * 1e6
        res.shaft_width_um = a0 * 1e6  # a straight cone: mean width over its middle half is the opening's radius
    if ws is not None:
        A_wall = math.pi * a0 * math.sqrt(a0 ** 2 + sol["d"] ** 2)
        ws = al.vap.wall(a0, 0.5 * a0, A_wall, v, lambda T, Mv: vapour_outflow(a0, m.sigma, T, Mv))
        if ws["x_mg_bulk"] > 0:
            res.mg_wall_over_bulk = ws["x_mg_surface"] / ws["x_mg_bulk"]
        res.y_mg_vapour = ws["y"].get("Mg", 0.0)
        res.mg_loss_ug_per_s = ws["mg_loss_mol_s"] * JANAF["Mg"]["M"] * 1e9
    if want_pool:
        field = keyhole_field(sol, th, v)
        D, W, L, Dh = fp.pool_dimensions(field, th.theta_l, r0, hatch)
        res.pool_depth_um, res.pool_width_um, res.pool_length_um, res.pool_Dh_um = D * 1e6, W * 1e6, L * 1e6, Dh * 1e6
        D, W, L, _ = fp.pool_dimensions(field, th.theta_s, r0)
        res.pool_depth_solidus_um, res.pool_width_solidus_um, res.pool_length_solidus_um = D * 1e6, W * 1e6, L * 1e6
    sol["T_w"], sol["th"] = T_w, th
    return res, sol


TILT = True
A_COND = None  # see run_conduction_sensitivity
BRANCH = "shallowest"  # or "deepest": which stable state sets the pool (see run_branch_sensitivity)
_RT: dict = {}


def ray_table_N(N, shape="cone"):
    key = (round(N.real, 4), round(N.imag, 4), shape)
    if key not in _RT:
        _RT[key] = fp.RayTable(N, shape=shape)
    return _RT[key]


def cone_balance(P, v, r0, a0, th, Q_e, tab, A_override):
    """Version 1's energy balance of a straight cone of depth d: (absorbed - conducted - evaporated) / P."""
    def f(d):
        A_kh, A_sf, _, _ = tab(d / a0, a0 / r0)
        if A_override is not None:
            sc = A_override / max(A_kh + A_sf, 1e-9)
            A_kh, A_sf = A_kh * sc, A_sf * sc
        wings = fp.surface_wing_sources(a0, r0, A_sf * P)
        zs, q = fp.keyhole_conduction(a0, d, th, v, wings, tab.shape)
        return (A_kh * P - float(q.sum()) - Q_e) / P, A_kh + A_sf
    return f


def cone_roots(f, a0, r0, n=60):
    """All roots of the cone's balance from a dimple 2 % of the opening deep to 60 beam radii. A root where the
    balance goes from + to - with depth is stable. Returns the shallowest stable root (the dimple branch, which
    sets the pool) and the deepest (the keyhole branch; run_maps_v2 calls a point a keyhole if that one has
    Wk/Dk <= 0.7). For dimples much shallower than their opening is wide, the axis-source conduction undercounts
    the heat a cavity at T_w loses (it falls below an isothermal disc's 4 k a theta), so their depths are overstated;
    their absorptance, about the flat liquid's, is not."""
    ds = np.geomspace(0.02 * a0, 60 * r0, n)
    fs = np.array([f(d)[0] for d in ds])
    stable = []
    for k in range(n - 1):
        if fs[k] > 0 >= fs[k + 1]:
            stable.append(optimize.brentq(lambda dd: f(dd)[0], ds[k], ds[k + 1], xtol=1e-9, rtol=1e-5))
    if fs[0] <= 0:
        stable.insert(0, ds[0])  # even the smallest dimple loses more than it absorbs
    ok = True
    if not stable:
        stable = [ds[-1]]  # absorbs more than it loses all the way down: capped
        ok = False
    deep = stable[-1] if len(stable) > 1 else None
    return {"shallow": stable[0], "deep": deep, "A_deep": f(deep)[1] if deep is not None else float("nan"),
            "n_stable": len(stable), "ok": ok, "stable": stable}


def classify(res: ResultV2, layer: float) -> str:
    if res.mode == "keyhole" and res.Wk_over_Dk <= WK_DK_AM:
        return "keyhole"
    if res.pool_depth_um <= layer * 1e6:
        return "lof"
    if res.pool_Dh_um <= layer * 1e6:
        return "lof_hatch"
    return "none"


# --- alloys used in the comparisons ------------------------------------------------------------------------

# Sourced replacements for version 1's handbook numbers. Filled in from the sources in the README; until a
# value is sourced, version 1's number stays (and the README says so).
# Solid conductivity of as-built LPBF AlSi10Mg against temperature: Yang et al. 2018 (J. Mater. Res. 33, 4040,
# doi:10.1557/jmr.2018.405), Fig. 5, first heating run, mean of the X and Z directions as read off the figure.
# The authors put the dip between 175 and 350 C down to the heat capacity of exothermic events, so it is skipped.
# The blend uses the same table: no measured k(T) for a hypereutectic LPBF Al-Si was found.
YANG2018_KS = (np.array([223.15, 273.15, 323.15, 373.15, 423.15, 448.15, 623.15, 673.15, 723.15, 773.15]),
               np.array([93.5, 101.0, 109.0, 114.0, 119.5, 121.5, 153.5, 160.0, 161.5, 162.0]))

PROPS = {
    # liquid resistivity of the blend: None keeps version 1's Leitner + Brandt & Neuer formula, which Sun et al.
    # 2019 (Int. J. Thermophys. 40, 31) confirm to 20 wt% Si (39 uOhm cm at 750 C against the formula's 40.4)
    "blend_rho_el": None,
    "k_s_table": {"alsi10mg": YANG2018_KS, "blend": YANG2018_KS},
    # Gan et al.'s alloys: liquid resistivity at T (Ohm m), corrected for thermal expansion
    "gan_rho_el": {
        # Boivineau et al. 2006 (Int. J. Thermophys. 27, 507): 1.92 uOhm m at the liquidus, corrected; no fit
        # is given for the corrected values, so it is held constant
        "Ti64": lambda T: 1.92e-6,
        # Pichler et al. 2020 (J. Mater. Sci. 55, 4081), Table 3, 316L, corrected: 1.154 + 1.893e-4 T uOhm m
        # (1708-2900 K)
        "SS316": lambda T: (1.154 + 1.893e-4 * T) * 1e-6,
        # no measurement found: Leitner et al. 2017's liquid Al with Brandt & Neuer's Si and Mg increments for
        # 0.6 wt% Si and 1.0 wt% Mg, the same construction as for our alloys
        "Al6061": lambda T: (0.097 + 1.681e-4 * T) * 1e-6 + 0.675e-8 * 0.6 + 0.92e-8 * 1.0,
    },
}


PROPS_DESCRIPTION = {
    "blend_rho_el": "version 1's Leitner et al. 2017 + Brandt & Neuer 2007 formula (checked against Sun et al. 2019 at "
                    "20 wt% Si: 40.4 vs 39 uOhm cm)",
    "k_s_table": "as-built LPBF AlSi10Mg, Yang et al. 2018 Fig. 5 (first heating, mean of X and Z): "
                 + ", ".join(f"{t - 273.15:.0f} C {k:.1f}" for t, k in zip(*YANG2018_KS)) + " W/m/K; blend uses the same",
    "gan_rho_el": "Ti64 1.92 uOhm m (Boivineau et al. 2006, corrected, liquidus); SS316 1.154 + 1.893e-4 T uOhm m "
                  "(Pichler et al. 2020, Table 3, corrected); Al6061 Leitner et al. 2017 Al + Brandt & Neuer 2007 "
                  "increments for 0.6 wt% Si and 1.0 wt% Mg (no measurement found)",
}


def to_v2(m1: fp.Material, k_s_table=None) -> MaterialV2:
    return MaterialV2(**{f.name: getattr(m1, f.name) for f in dataclasses.fields(m1)}, k_s_table=k_s_table)


def make_alloy(key: str, use_mg=True, flow_factor=1.0, optics="drude-dc") -> Alloy:
    if key == "al5182":
        m1 = fp.al5182_material()
        m = to_v2(m1)
        act = "al5182"
    else:
        m1 = fp.alloy_material(key)
        m = to_v2(m1, PROPS["k_s_table"].get(key))
        if key == "blend" and PROPS["blend_rho_el"] is not None:
            r0_, s_ = PROPS["blend_rho_el"]
            m.rho_el = (r0_, s_, 933.47)
        act = key
    vap = Vapour(alloy=act, x=m.x, rho_l=m.rho_liq, M=m.M, sigma=m.sigma, flow_factor=flow_factor, use_mg=use_mg)
    return Alloy(key=key, m=m, vap=vap, optics=optics)


def gan_alloy(row, mat) -> Alloy:
    m1 = fp.gan_material(row, mat)
    m = to_v2(m1)
    rho = PROPS["gan_rho_el"].get(mat)
    if rho is not None:
        m.rho_el = (rho(m.T_w_fixed), 0.0, m.rho_el[2])
    return Alloy(key=mat, m=m, vap=None)


# --- parallel runs -------------------------------------------------------------------------------------------

NPROC = 3
_CACHE: dict = {}
_SPEC_OPTICS = "drude-dc"  # optics for the map and boundary jobs (see run_optics_sensitivity)


def _alloy_cached(spec):
    if spec not in _CACHE:
        kind = spec[0]
        if kind == "alloy":
            _, key, use_mg, ff, optics = spec
            _CACHE[spec] = make_alloy(key, use_mg=use_mg, flow_factor=ff, optics=optics)
    return _CACHE[spec]


def _work(job):
    """One point in a worker process. job: dict with spec or a ready Alloy, P, v, r0, T0, and options."""
    global A_COND, BRANCH
    A_COND = job.get("A_cond")
    BRANCH = job.get("branch", "shallowest")
    al = job["alloy"] if "alloy" in job else _alloy_cached(job["spec"])
    powder = job.get("powder")
    try:
        res, sol = solve_point_v2(al, job["P"], job["v"], job["r0"], job["T0"], A_override=job.get("A_override"),
                                  hatch=job.get("hatch"), want_pool=job.get("want_pool", True), powder=powder,
                                  deep_branch=job.get("deep_branch", True), shape_model=job.get("shape_model", "cone"))
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}", **{k: job[k] for k in ("P", "v")}}
    out = dataclasses.asdict(res)
    if job.get("keep_shape") and sol:
        out["shape"] = {k: np.asarray(sol[k]).tolist() for k in ("zn", "xcn", "rn")}
    return out


def pmap(jobs, nproc=None):
    from concurrent.futures import ProcessPoolExecutor
    nproc = nproc or NPROC
    if nproc <= 1:
        return [_work(j) for j in jobs]
    with ProcessPoolExecutor(max_workers=nproc) as ex:
        return list(ex.map(_work, jobs, chunksize=1))


# --- comparisons ---------------------------------------------------------------------------------------------

def _stats(pred, meas):
    pred, meas = np.asarray(pred, dtype=float), np.asarray(meas, dtype=float)
    err = pred - meas
    return {"MAE_um": round(float(np.abs(err).mean()), 1), "median_ratio": round(float(np.median(pred / meas)), 2),
            "median_abs_rel_err_pct": round(float(np.median(np.abs(err) / meas) * 100), 1),
            "R2": round(float(1 - (err ** 2).sum() / ((meas - meas.mean()) ** 2).sum()), 3)}


def run_gan_v2(out: pathlib.Path, cache: pathlib.Path, log=print, shape_model="cone",
               fname="v2-gan2021-xray-keyhole-depths.csv") -> dict:
    from keyhole_open_models import load_gan  # noqa: E402
    d = load_gan(cache)
    d["material"] = d["group"].str.extract(r"^(\w+)")[0].replace({"Ti6": "Ti64"})
    v1 = pd.read_csv(fp.FP_DIR / "fp-gan2021-xray-keyhole-depths.csv")
    jobs = []
    for i, r in d.iterrows():
        al = gan_alloy(r, r["material"])
        for tag, Aov in (("own_A", None), ("gan_eta", r["eta"])):
            jobs.append({"alloy": al, "P": r["P"], "v": r["V"], "r0": r["r0"], "T0": 293.0, "A_override": Aov,
                         "want_pool": False, "row": i, "tag": tag, "shape_model": shape_model})
    res = pmap(jobs)
    rows = {}
    for j, rr in zip(jobs, res):
        i = j["row"]
        r = d.loc[i]
        row = rows.setdefault(i, {"row": i, "group": r["group"], "material": r["material"], "P_W": r["P"],
                                  "v_m_s": r["V"], "r0_um": r["r0"] * 1e6, "eta_gan": r["eta"],
                                  "keyhole_depth_measured_um": r["e"] * 1e6,
                                  "v1_own_A_depth_um": float(v1.loc[i, "own_A_depth_um"]),
                                  "v1_own_A": float(v1.loc[i, "own_A_A"]),
                                  "gan_law_um": float(v1.loc[i, "gan_law_um"])})
        t = j["tag"]
        if "error" in rr:
            log("error", i, t, rr["error"])
            continue
        row.update({f"{t}_mode": rr["mode"], f"{t}_A": rr["A"], f"{t}_depth_um": rr["d_um"],
                    f"{t}_bistable": rr["bistable"], f"{t}_depth_deep_um": rr["d_deep_um"],
                    f"{t}_front_wall_deg": rr["front_wall_deg"], f"{t}_shaft_width_um": rr["shaft_width_um"],
                    f"{t}_converged": rr["converged"]})
    t = pd.DataFrame(list(rows.values()))
    t.to_csv(out / fname, index=False, float_format="%.5g")
    s = {}
    for mat, gg in list(t.groupby("material", sort=False)) + [("all", t)]:
        meas = gg["keyhole_depth_measured_um"]
        s[mat] = {"n": int(len(gg))}
        for col in ("own_A_depth_um", "gan_eta_depth_um", "v1_own_A_depth_um", "gan_law_um"):
            s[mat][col] = _stats(gg[col], meas)
        # if the track sat on the deep branch wherever it exists
        deep = np.where(gg["own_A_bistable"].astype(bool), gg["own_A_depth_deep_um"], gg["own_A_depth_um"])
        s[mat]["own_A_deep_branch_depth_um"] = _stats(deep, meas)
        s[mat]["own_A_median"] = round(float(gg["own_A_A"].median()), 3)
        s[mat]["bistable_rows"] = int(gg["own_A_bistable"].astype(bool).sum())
        s[mat]["front_wall_deg_median"] = round(float(gg["own_A_front_wall_deg"].median()), 1)
        s[mat]["shaft_width_um_median"] = round(float(gg["own_A_shaft_width_um"].median()), 1)
        s[mat]["unconverged_rows"] = int((~gg["own_A_converged"].astype(bool)).sum())
        log(mat, json.dumps(s[mat]))
    return s


AM_DIR = fp.AM_DIR


def _powder(on=True, A=None):
    if not on:
        return None
    import keyhole_fp_powder as pw
    return pw.Powder(A_powder=pw.RUBENCHIK_AL_POWDER if A is None else A)


def run_maps_v2(out: pathlib.Path, log=print, powder=True, tag="", A_cond=None, branch="shallowest") -> dict:
    jobs = []
    for key, a in fp.ALLOYS.items():
        g = pd.read_csv(AM_DIR / f"{a['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"].reset_index(drop=True)
        for _, r in g.iterrows():
            jobs.append({"spec": ("alloy", key, True, 1.0, _SPEC_OPTICS), "P": float(r["power_W"]),
                         "v": float(r["speed_mm_s"]) / 1000.0, "r0": a["r0"], "T0": a["T0"], "hatch": a["hatch"],
                         "powder": _powder(powder), "key": key, "am_class": r["am_class"], "A_cond": A_cond,
                         "branch": branch})
    res = pmap(jobs)
    rows = []
    for j, rr in zip(jobs, res):
        if "error" in rr:
            log("error", j["key"], j["P"], j["v"], rr["error"])
            continue
        r = ResultV2(**{k: rr[k] for k in ResultV2.__dataclass_fields__})
        cls = classify(r, fp.ALLOYS[j["key"]]["layer"])
        deep_cls = "keyhole" if (r.bistable and 2 * r.a0_um / r.d_deep_um <= WK_DK_AM) else cls
        rows.append({"alloy": j["key"], "P_W": j["P"], "v_m_s": j["v"], "am_class": j["am_class"], "v2_class": cls,
                     "v2_class_deep_branch": deep_cls, **rr})
    d = pd.DataFrame(rows)
    d.to_csv(out / f"v2-map-classes{tag}.csv", index=False, float_format="%.5g")
    summary = {}
    for key in fp.ALLOYS:
        g = d[d["alloy"] == key]
        am_kh = g["am_class"] == "keyhole"
        s = {"grid_points": int(len(g))}
        for col in ("v2_class", "v2_class_deep_branch"):
            kh = g[col] == "keyhole"
            s[col] = {"agree_all_classes": int((g["am_class"] == g[col]).sum()),
                      "agree_keyhole_or_not": int((am_kh == kh).sum()), "missed_am_keyholes": int((am_kh & ~kh).sum()),
                      "extra_keyholes": int((kh & ~am_kh).sum()),
                      "confusion": pd.crosstab(g["am_class"], g[col]).to_dict()}
        s["bistable_points"] = int(g["bistable"].sum())
        s["keyhole_mode_points"] = int((g["mode"] == "keyhole").sum())
        s["unconverged"] = int((~g["converged"].astype(bool)).sum())
        s["median_beam_on_powder_conduction"] = round(float(g.loc[g["mode"] == "conduction", "beam_on_powder"].median()), 3) if (g["mode"] == "conduction").any() else None
        s["median_A_conduction"] = round(float(g.loc[g["mode"] == "conduction", "A"].median()), 3) if (g["mode"] == "conduction").any() else None
        summary[key] = s
        log(key, tag, json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "confusion"}) for k, v in s.items()}))
    return summary


def _boundary_job(job):
    """Bisection on power at one speed for one criterion ('dimple' = the shallow branch has Wk/Dk <= 0.7, i.e. the
    dimple has run away; 'deep' = a keyhole branch with Wk/Dk <= 0.7 exists; 'mode' = the surface boils)."""
    al = _alloy_cached(job["spec"])
    a = fp.ALLOYS[job["key"]]
    v, crit = job["v"], job["crit"]

    def test(P):
        r, _ = solve_point_v2(al, P, v, a["r0"], a["T0"], want_pool=False, powder=job.get("powder"),
                              deep_branch=(crit == "deep"), n_rays=8000)
        if crit == "mode":
            return r.mode == "keyhole"
        if r.mode != "keyhole":
            return False
        if crit == "deep" and r.bistable:
            return 2 * r.a0_um / r.d_deep_um <= WK_DK_AM or r.Wk_over_Dk <= WK_DK_AM
        return r.Wk_over_Dk <= WK_DK_AM
    lo, hi = 50.0, 700.0
    if test(lo):
        return lo
    if not test(hi):
        return float("nan")
    for _ in range(11):
        mid = 0.5 * (lo + hi)
        if test(mid):
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def run_boundaries_v2(out: pathlib.Path, log=print, powder=True, tag="") -> dict:
    from concurrent.futures import ProcessPoolExecutor
    jobs = []
    for key, a in fp.ALLOYS.items():
        b = pd.read_csv(AM_DIR / f"{a['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        speeds = np.unique(np.round(np.linspace(b["speed_mm_s"].min(), b["speed_mm_s"].max(), 7), -1)) / 1000.0
        for v in speeds:
            for crit in ("mode", "deep", "dimple"):
                jobs.append({"spec": ("alloy", key, True, 1.0, _SPEC_OPTICS), "key": key, "v": float(v), "crit": crit,
                             "powder": _powder(powder),
                             "P_am": float(np.interp(v * 1000, b["speed_mm_s"], b["P_keyhole_W"]))})
    with ProcessPoolExecutor(max_workers=NPROC) as ex:
        res = list(ex.map(_boundary_job, jobs, chunksize=1))
    rows = {}
    for j, P in zip(jobs, res):
        row = rows.setdefault((j["key"], j["v"]), {"alloy": j["key"], "v_m_s": j["v"], "P_keyhole_am_W": j["P_am"]})
        row[{"mode": "P_surface_boils_W", "deep": "P_keyhole_branch_appears_W", "dimple": "P_dimple_runs_away_W"}[j["crit"]]] = P
    d = pd.DataFrame(list(rows.values()))
    d.to_csv(out / f"v2-keyhole-boundary-vs-am{tag}.csv", index=False, float_format="%.5g")
    s = {}
    for key in fp.ALLOYS:
        g = d[d["alloy"] == key]
        s[key] = {c: [round(float((g[c] / g["P_keyhole_am_W"]).min()), 3), round(float((g[c] / g["P_keyhole_am_W"]).max()), 3)]
                  for c in ("P_surface_boils_W", "P_keyhole_branch_appears_W", "P_dimple_runs_away_W")}
        log(key, json.dumps(s[key]))
    return s


def run_points_v2(out: pathlib.Path, log=print) -> dict:
    pts = [("alsi10mg", 250.0, 0.9), ("alsi10mg", 350.0, 0.9), ("blend", 375.0, 0.4)]
    jobs = []
    for key, P, v in pts:
        a = fp.ALLOYS[key]
        for label, Aov in (("own absorptance", None), ("absorptance fixed at the AM module's", a["A_am"])):
            jobs.append({"spec": ("alloy", key, True, 1.0, "drude-dc"), "P": P, "v": v, "r0": a["r0"], "T0": a["T0"],
                         "hatch": a["hatch"], "A_override": Aov, "powder": _powder(True), "keep_shape": True,
                         "key": key, "label": label})
    res = pmap(jobs)
    rows, shapes = [], {}
    for j, rr in zip(jobs, res):
        shape = rr.pop("shape", None)
        r = ResultV2(**{k: rr[k] for k in ResultV2.__dataclass_fields__})
        rows.append({"alloy": j["key"], "P_W": j["P"], "v_m_s": j["v"], "variant": j["label"],
                     "class": classify(r, fp.ALLOYS[j["key"]]["layer"]), **rr})
        if shape:
            shapes[f"{j['key']}-{int(j['P'])}W-{j['v']}-{'own' if j['label'].startswith('own') else 'amA'}"] = shape
        log(j["key"], j["P"], j["v"], j["label"], {k: (round(x, 3) if isinstance(x, float) else x) for k, x in rr.items() if k in (
            "mode", "A", "d_um", "Wk_over_Dk", "T_w", "front_wall_deg", "tip_offset_um", "bistable", "d_deep_um",
            "pool_depth_um", "pool_width_um", "pool_length_um", "pool_length_solidus_um", "mg_wall_over_bulk")})
    pd.DataFrame(rows).to_csv(out / "v2-render-points.csv", index=False, float_format="%.5g")
    (out / "v2-render-point-shapes.json").write_text(json.dumps(shapes))
    return {"rows": len(rows)}


def run_solyaev_v2(out: pathlib.Path, log=print) -> dict:
    r0, T0 = math.sqrt(2.0) * 40e-6, 298.15
    df = pd.read_csv(fp.SOLYAEV_CSV)
    sc = df[df["measured_class"].isin(["keyhole", "stable", "lack_of_fusion"])].reset_index(drop=True)
    jobs = [{"spec": ("alloy", "alsi10mg", True, 1.0, "drude-dc"), "P": float(r["power_w"]), "v": float(r["velocity_m_s"]),
             "r0": r0, "T0": T0, "powder": _powder(True), "meas": r["measured_class"]} for _, r in sc.iterrows()]
    res = pmap(jobs)
    rows = []
    for j, rr in zip(jobs, res):
        dw = rr["pool_depth_um"] / rr["pool_width_um"] if rr["pool_width_um"] > 0 else 0.0
        rows.append({"P_W": j["P"], "v_m_s": j["v"], "measured_class": j["meas"], "mode": rr["mode"], "A": rr["A"],
                     "keyhole_depth_um": rr["d_um"], "Wk_over_Dk": rr["Wk_over_Dk"], "bistable": rr["bistable"],
                     "keyhole_depth_deep_um": rr["d_deep_um"], "pool_depth_um": rr["pool_depth_um"],
                     "pool_width_um": rr["pool_width_um"], "pool_D_over_W": dw})
    t = pd.DataFrame(rows)
    t.to_csv(out / "v2-solyaev2025-alsi10mg.csv", index=False, float_format="%.5g")
    meas = (t["measured_class"] == "keyhole").to_numpy()
    s = {"scored_points": int(len(t)), "measured_keyhole": int(meas.sum())}
    deep_ok = t["bistable"].astype(bool) & (2 * 40e-6 * math.sqrt(2) * 1e6 / t["keyhole_depth_deep_um"] <= WK_DK_AM)
    for name, pred in [("pool D/W > 0.75 (the study's own test)", (t["pool_D_over_W"] > 0.75).to_numpy()),
                       ("keyhole Wk/Dk <= 0.7, dimple branch", ((t["mode"] == "keyhole") & (t["Wk_over_Dk"] <= WK_DK_AM)).to_numpy()),
                       ("keyhole Wk/Dk <= 0.7 on either branch", (((t["mode"] == "keyhole") & (t["Wk_over_Dk"] <= WK_DK_AM)) | deep_ok).to_numpy()),
                       ("keyhole mode (the surface boils)", (t["mode"] == "keyhole").to_numpy())]:
        s[name] = {"predicted_keyhole": int(pred.sum()), "agree": int((pred == meas).sum()),
                   "missed": int((~pred & meas).sum()), "extra": int((pred & ~meas).sum())}
        log(name, s[name])
    return s


def run_ambench_v2(out: pathlib.Path, log=print) -> dict:
    a = fp.AMB2022
    jobs = []
    for use_mg in (True, False):
        for label, Aov in (("own absorptance", None), ("absorptance fixed at the measured 0.43", a["A_keyhole"])):
            jobs.append({"spec": ("alloy", "al5182", use_mg, 1.0, "drude-dc"), "P": a["P"], "v": a["v"], "r0": a["r0"],
                         "T0": a["T0"], "A_override": Aov, "keep_shape": True, "label": label, "use_mg": use_mg})
    res = pmap(jobs)
    rows = []
    for j, rr in zip(jobs, res):
        rr.pop("shape", None)
        rows.append({"variant": j["label"], "mg_in_vapour": j["use_mg"], **rr})
        log("AM-Bench 2022 Al 5182", j["label"], "Mg" if j["use_mg"] else "no Mg", {k: round(rr[k], 3) for k in (
            "A", "d_um", "Wk_over_Dk", "T_w", "front_wall_deg", "pool_depth_um", "pool_width_um",
            "pool_depth_solidus_um", "pool_width_solidus_um", "mg_wall_over_bulk", "y_mg_vapour")})
    pd.DataFrame(rows).to_csv(out / "v2-ambench2022-al5182.csv", index=False, float_format="%.5g")
    return {"measured": a, "rows": len(rows)}


def run_conduction_sensitivity(out: pathlib.Path, log=print) -> dict:
    """The maps again with the conduction-mode absorptance fixed: at the 0.24 Simonds et al. 2024 measured on bare
    Al 5182 before its keyhole formed, and at the AM module's 0.307 at its AlSi10Mg render. Keyhole points keep
    their own absorptance."""
    return {f"A_cond={a}": run_maps_v2(out, log, tag=f"-A_cond-{a}", A_cond=a) for a in (0.24, 0.307)}


def run_bifurcation(out: pathlib.Path, log=print) -> dict:
    """Every stable keyhole depth, and its absorptance, against power at one speed: AlSi10Mg and the blend at the AM
    module's render speeds (0.9 and 0.4 m/s) and Al 5182 at NIST's AM-Bench speed (0.7 m/s, 122.5 um beam)."""
    rows = []
    cases = [("alsi10mg", 0.9, fp.ALLOYS["alsi10mg"]["r0"], fp.ALLOYS["alsi10mg"]["T0"]),
             ("blend", 0.4, fp.ALLOYS["blend"]["r0"], fp.ALLOYS["blend"]["T0"]),
             ("al5182", fp.AMB2022["v"], fp.AMB2022["r0"], fp.AMB2022["T0"])]
    for key, v, r0, T0 in cases:
        al = make_alloy(key)
        m = al.m
        a0 = r0
        Ps = np.arange(100.0, 601.0, 10.0) if key == "al5182" else np.arange(100.0, 401.0, 5.0)
        for P in Ps:
            T_on, _ = al.vap.onset(r0, v)
            th_b = fp.thermal_state(m, T0, T_on)
            A_liq = float(fp.fresnel_absorptance(al.N(T_on), 1.0))
            xs = np.linspace(-3 * r0, 1.0 * r0, 41)
            peak = float(fp.gaussian_field(xs, 0.0, 0.0, A_liq * P, r0, th_b.k, th_b.kappa, v).max())
            if peak < th_b.theta_w:
                rows.append({"alloy": key, "v_m_s": v, "P_W": P, "state": 0, "mode": "conduction", "d_um": 0.0,
                             "A": A_liq, "Wk_over_Dk": float("inf")})
                continue
            ws = al.vap.wall(a0, 0.5 * a0, math.pi * a0 * math.sqrt(a0 ** 2 + (2 * a0) ** 2), v,
                             lambda T, Mv: vapour_outflow(a0, m.sigma, T, Mv))
            th = fp.thermal_state(m, T0, ws["T_w"])
            tab = ray_table_N(al.N(ws["T_w"]))
            f = cone_balance(P, v, r0, a0, th, evaporation_power_v2(ws), tab, None)
            roots = cone_roots(f, a0, r0, n=120)
            for i, d in enumerate(roots["stable"]):
                rows.append({"alloy": key, "v_m_s": v, "P_W": P, "state": i, "mode": "keyhole", "d_um": d * 1e6,
                             "A": f(d)[1], "Wk_over_Dk": 2 * a0 / d})
        log(key, "states:", sum(1 for r in rows if r["alloy"] == key))
    t = pd.DataFrame(rows)
    t.to_csv(out / "v2-stable-states-vs-power.csv", index=False, float_format="%.5g")
    return {"rows": len(t)}


def run_optics_sensitivity(out: pathlib.Path, log=print, A_target=0.24) -> dict:
    """The maps and keyhole lines again with the liquid's flat absorptance anchored at A_target instead of the clean
    Drude-Fresnel 0.18-0.20 (anchored_index)."""
    optics = f"anchored-{A_target}"
    global _SPEC_OPTICS
    _SPEC_OPTICS = optics
    try:
        s = {"maps": run_maps_v2(out, log, tag=f"-optics-{A_target}"),
             "boundaries": run_boundaries_v2(out, log, tag=f"-optics-{A_target}")}
    finally:
        _SPEC_OPTICS = "drude-dc"
    return s


def run_branch_sensitivity(out: pathlib.Path, log=print) -> dict:
    """The maps with every point on its deepest stable state (where there are several), for the pool as well as the
    class."""
    return run_maps_v2(out, log, tag="-deepest-state", branch="deepest")


def run_powder_check(out: pathlib.Path, log=print) -> dict:
    """The homogenised powder-layer model against Boley et al. 2015 and Rubenchik et al. 2015."""
    import keyhole_fp_powder as pw
    rows = []
    for por in (0.4, 0.45, 0.5):
        for LD in (1.5, 1.8, 2.0):
            a = pw.powder_mc(1.244, 10.0, 1.244, 10.0, -1.0, -1.0, LD, pw.extinction(por, 1.0), 40000, 3)
            rows.append({"case": "Al textbook index (Boley et al. 2015's n = 1.244 + 10i)", "porosity": por,
                         "L_over_D": LD, "A_total": a[0], "A_powder": a[1], "A_substrate": a[2],
                         "published": pw.BOLEY_AL_BILAYER, "published_what": "ray-traced close-packed bilayer on Al"})
    for por in (0.4, 0.5, 0.6):
        for LD in (2.0, 5.0, 20.0):
            a = pw.powder_mc(1.3717, 10.314, 1.3717, 10.314, pw.RUBENCHIK_AL_FLAT, pw.RUBENCHIK_AL_FLAT, LD,
                             pw.extinction(por, 1.0), 40000, 3)
            rows.append({"case": "measured flat Al absorptance 0.20 (Rubenchik et al. 2015)", "porosity": por,
                         "L_over_D": LD, "A_total": a[0], "A_powder": a[1], "A_substrate": a[2],
                         "published": pw.RUBENCHIK_AL_POWDER, "published_what": "measured Al powder, 970 nm"})
    t = pd.DataFrame(rows)
    t.to_csv(out / "v2-powder-check.csv", index=False, float_format="%.4g")
    s = {}
    for case, g in t.groupby("case"):
        s[case] = {"A_total_range": [round(float(g["A_total"].min()), 3), round(float(g["A_total"].max()), 3)],
                   "published": float(g["published"].iloc[0]), "published_what": g["published_what"].iloc[0]}
        log(case, s[case])
    return s


def run_mg_table(out: pathlib.Path, log=print) -> dict:
    """Wall temperature with and without Mg (and with a 10x faster melt past the wall), for each alloy."""
    rows = []
    cases = [("alsi10mg", 40e-6, 0.9), ("blend", 45e-6, 0.4), ("al5182", 61.25e-6, 0.7)]
    for key, r0, v in cases:
        for use_mg, ff in ((False, 1.0), (True, 1.0), (True, 10.0)):
            al = make_alloy(key, use_mg=use_mg, flow_factor=ff)
            m = al.m
            a0 = r0
            d = 3 * a0
            ws = al.vap.wall(a0, 0.5 * a0, math.pi * a0 * math.sqrt(a0 ** 2 + d ** 2), v,
                             lambda T, Mv: vapour_outflow(a0, m.sigma, T, Mv))
            T_on, xs_on = al.vap.onset(r0, v)
            rows.append({"alloy": key, "mg_in_vapour": use_mg, "melt_speed_over_scan_speed": ff, "v_m_s": v,
                         "x_mg_bulk": m.x.get("Mg", 0.0), "T_onset_K": T_on, "T_wall_K": ws["T_w"],
                         "mg_wall_over_bulk": (ws["x_mg_surface"] / ws["x_mg_bulk"]) if ws["x_mg_bulk"] else float("nan"),
                         "y_mg_vapour": ws["y"].get("Mg", 0.0), "y_si_vapour": ws["y"].get("Si", 0.0),
                         "mg_loss_ug_per_s": ws["mg_loss_mol_s"] * JANAF["Mg"]["M"] * 1e9,
                         "T_boil_v1_K": fp.alloy_material(key).T_boil() if key != "al5182" else fp.al5182_material().T_boil()})
            log(rows[-1])
    t = pd.DataFrame(rows)
    t.to_csv(out / "v2-mg-vapour.csv", index=False, float_format="%.5g")
    return {"rows": len(rows)}


def main() -> None:
    global NPROC
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["all", "point", "powder", "mg", "explore", "figures", "meltflow", "conduction",
                                    "states", "optics", "mapflow", "plan"])
    ap.add_argument("--only", default=None)
    ap.add_argument("--drive", action="store_true", help="meltflow: the recoil-driven moving-wall experiment")
    ap.add_argument("--src-tag", default="", help="mapflow: which map-classes CSV to take the absorptance from, "
                                                  "e.g. -optics-0.24")
    ap.add_argument("--out", type=pathlib.Path, default=V2_DIR)
    ap.add_argument("--cache", type=pathlib.Path, default=pathlib.Path("/tmp/keyhole-open-models-cache"))
    ap.add_argument("--alloy", choices=list(fp.ALLOYS) + ["al5182"], default="blend")
    ap.add_argument("--P", type=float, default=375.0)
    ap.add_argument("--v", type=float, default=0.4)
    ap.add_argument("--nproc", type=int, default=3)
    a = ap.parse_args()
    NPROC = a.nproc
    a.out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "point":
        al = make_alloy(a.alloy)
        p = fp.ALLOYS.get(a.alloy, {"r0": fp.AMB2022["r0"], "T0": fp.AMB2022["T0"], "hatch": None, "layer": 30e-6})
        res, _ = solve_point_v2(al, a.P, a.v, p["r0"], p["T0"], hatch=p.get("hatch"), powder=_powder(True))
        print(json.dumps({"class": classify(res, p.get("layer", 30e-6)), **dataclasses.asdict(res)}, indent=1,
                         default=float))
        return
    logf = open(a.out / f"v2-{a.cmd}{'-drive' if getattr(a, 'drive', False) else ''}{a.src_tag}.log", "w")

    def log(*x):
        line = " ".join(str(y) for y in x)
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    t0 = time.time()
    if a.cmd == "figures":
        import keyhole_fp_v2_figures as figs
        figs.main(a.out)
        return
    if a.cmd == "powder":
        run_powder_check(a.out, log)
        return
    if a.cmd == "mg":
        run_mg_table(a.out, log)
        return
    if a.cmd == "plan":
        run_single_track_plan(a.out, log)
        return
    if a.cmd == "mapflow":
        run_maps_meltflow(a.out, log, src_tag=a.src_tag)
        log("done in", round(time.time() - t0), "s")
        return
    if a.cmd == "optics":
        s_ = run_optics_sensitivity(a.out, log)
        (a.out / "v2-optics-sensitivity-summary.json").write_text(json.dumps(s_, indent=1, default=str) + "\n")
        return
    if a.cmd == "states":
        run_bifurcation(a.out, log)
        return
    if a.cmd == "conduction":
        s_ = run_conduction_sensitivity(a.out, log)
        s_["deepest_state"] = run_branch_sensitivity(a.out, log)
        (a.out / "v2-conduction-sensitivity-summary.json").write_text(json.dumps(s_, indent=1, default=str) + "\n")
        return
    if a.cmd == "meltflow":
        run_meltflow_v2(a.out, log, only=a.only, drive=a.drive)
        log("done in", round(time.time() - t0), "s")
        return
    if a.cmd == "explore":
        s = run_gan_v2(a.out, a.cache, log, shape_model="free", fname="v2-explore-free-shape-gan2021.csv")
        (a.out / "v2-explore-free-shape-summary.json").write_text(json.dumps(s, indent=1) + "\n")
        log("done in", round(time.time() - t0), "s")
        return
    summary = {"properties": PROPS_DESCRIPTION, "mg_diffusion": MG_DIFFUSION_SOURCE}
    summary["powder_check"] = run_powder_check(a.out, log)
    summary["mg_vapour"] = run_mg_table(a.out, log)
    summary["gan2021_xray_depths"] = run_gan_v2(a.out, a.cache, log)
    summary["am_maps"] = run_maps_v2(a.out, log)
    summary["am_maps_no_powder"] = run_maps_v2(a.out, log, powder=False, tag="-no-powder")
    summary["am_keyhole_boundary"] = run_boundaries_v2(a.out, log)
    summary["render_points"] = run_points_v2(a.out, log)
    summary["solyaev2025_alsi10mg"] = run_solyaev_v2(a.out, log)
    summary["ambench2022_al5182"] = run_ambench_v2(a.out, log)
    summary["runtime_s"] = round(time.time() - t0, 1)
    (a.out / "v2-summary.json").write_text(json.dumps(summary, indent=1, default=str) + "\n")
    log("done in", summary["runtime_s"], "s")



# --- melt flow: our own 3D beam-frame solver (scripts/keyhole_meltflow.py) at version 2's states -------------

MELTFLOW_CASES = [
    # (label, alloy, P, v, A_override or None)
    ("alsi10mg-250W-0.9-own", "alsi10mg", 250.0, 0.9, None),
    ("alsi10mg-250W-0.9-A_am", "alsi10mg", 250.0, 0.9, 0.3074),
    ("alsi10mg-350W-0.9-own", "alsi10mg", 350.0, 0.9, None),
    ("blend-375W-0.4-own", "blend", 375.0, 0.4, None),
    ("blend-375W-0.4-A_am", "blend", 375.0, 0.4, 0.3841),
    ("al5182-473W-0.7-own", "al5182", 473.0, 0.7, None),
    ("al5182-473W-0.7-A_measured", "al5182", 473.0, 0.7, 0.43),
]


def depth_at_offset(g, T, T_iso, y_off):
    """Deepest point of the T_iso isotherm in the plane y = y_off (linear in y between cell centres and in z)."""
    yc, zc = g.yc, g.zc
    j = int(np.searchsorted(yc, y_off)) - 1
    if j < 0 or j + 1 >= yc.size:
        return 0.0
    f = (y_off - yc[j]) / (yc[j + 1] - yc[j])
    Ty = (1 - f) * T[:, j, :] + f * T[:, j + 1, :]
    best = 0.0
    for i in range(Ty.shape[0]):
        col = Ty[i]
        hot = np.nonzero(col > T_iso)[0]
        if hot.size == 0 or hot[0] != 0:
            continue
        k = hot[-1]
        if k + 1 < zc.size:
            zk = zc[k] + (zc[k + 1] - zc[k]) * (col[k] - T_iso) / max(col[k] - col[k + 1], 1e-12)
        else:
            zk = zc[k]
        best = max(best, zk)
    return float(best)


def run_single_track_plan(out: pathlib.Path, log=print) -> dict:
    """Grid points where single tracks would discriminate: version 2 and the AM module disagree, or the point sits
    in the band with more than one stable keyhole. Each row carries the AM module's class and version 2's
    predictions (analytic, melt-flow solver, and with the 0.24 optics)."""
    d = pd.read_csv(out / "v2-map-classes.csv")
    mf_ = pd.read_csv(out / "v2-map-classes-meltflow.csv")
    keys = ["alloy", "P_W", "v_m_s"]
    t = d[keys + ["am_class", "v2_class_deep_branch", "mode", "A", "d_um", "Wk_over_Dk", "bistable", "d_deep_um",
                  "pool_depth_um", "pool_width_um", "pool_Dh_um"]].merge(
        mf_[keys + ["mf_class", "mf_pool_depth_um", "mf_pool_width_um", "mf_pool_Dh_um"]], on=keys, how="left")
    opt = out / "v2-map-classes-optics-0.24.csv"
    if opt.exists():
        o = pd.read_csv(opt)[keys + ["v2_class_deep_branch", "A", "pool_depth_um", "pool_width_um"]].rename(
            columns={"v2_class_deep_branch": "class_optics_0.24", "A": "A_optics_0.24",
                     "pool_depth_um": "pool_depth_optics_0.24_um", "pool_width_um": "pool_width_optics_0.24_um"})
        t = t.merge(o, on=keys, how="left")
    t = t.rename(columns={"v2_class_deep_branch": "v2_class"})
    t["why"] = np.where(t["am_class"] != t["v2_class"], "classes disagree",
                        np.where(t["bistable"].astype(bool), "two stable keyholes", ""))
    plan = t[t["why"] != ""].sort_values(keys)
    plan.to_csv(out / "v2-single-track-plan.csv", index=False, float_format="%.4g")
    s = {k: {"points": int(len(g)), "disagree": int((g["why"] == "classes disagree").sum()),
             "bistable_only": int((g["why"] == "two stable keyholes").sum())} for k, g in plan.groupby("alloy")}
    log(s)
    return s


def run_maps_meltflow(out: pathlib.Path, log=print, src_tag="") -> dict:
    """The AM maps' non-keyhole points again with the melt-flow solver (Marangoni flow, k(T) and H(T) resolved).
    Each point gets version 2's own absorbed fraction (flat liquid, powder share, or the dimple's) as a Gaussian
    surface flux; a dimple only 10-35 um deep isn't resolved as a cavity at r0/8. Keyhole points keep their class."""
    import keyhole_meltflow as mf
    d = pd.read_csv(out / f"v2-map-classes{src_tag}.csv")
    rows = []
    t0 = time.time()
    for n, r in d.iterrows():
        key = r["alloy"]
        a = fp.ALLOYS[key]
        row = {"alloy": key, "P_W": r["P_W"], "v_m_s": r["v_m_s"], "am_class": r["am_class"],
               "v2_class": r["v2_class_deep_branch"], "A": r["A"]}
        if r["v2_class_deep_branch"] == "keyhole":
            rows.append({**row, "mf_class": "keyhole"})
            continue
        al = make_alloy(key)
        mu0, E = mf.VISCOSITY[key]
        pr = mf.props_from_material(al.m, mu0=mu0, E_mu=E, dsigma_dT=mf.DSIGMA_DT_DEFAULT,
                                    C_darcy=mf.C_DARCY_DEFAULT, evaporation=True)
        r0 = a["r0"]
        g = mf.grid_for(r0, pool_D=max(1.6 * r["pool_depth_solidus_um"], 80.0) * 1e-6,
                        pool_W=max(1.8 * r["pool_width_solidus_um"], 200.0) * 1e-6,
                        pool_L_rear=max(1.6 * r["pool_length_solidus_um"], 400.0) * 1e-6, h_fine=r0 / 8)
        case = mf.Case(label=f"{key}-{r['P_W']:.0f}W-{r['v_m_s']}", props=pr, P=float(r["P_W"]), v=float(r["v_m_s"]),
                       r0=r0, T0=a["T0"], A=float(r["A"]), keyhole=None, grid=g)
        o, T, st, kh = mf.solve_case(case, flow=True, log=lambda *x: None)
        D = o["pool_depth_liquidus_um"]
        Dh = depth_at_offset(g, T, pr.T_l, a["hatch"] / 2) * 1e6
        layer = a["layer"] * 1e6
        cls = "lof" if D <= layer else ("lof_hatch" if Dh <= layer else "none")
        rows.append({**row, "mf_class": cls, "mf_pool_depth_um": D, "mf_pool_width_um": o["pool_width_liquidus_um"],
                     "mf_pool_length_um": o["pool_length_liquidus_um"], "mf_pool_Dh_um": Dh,
                     "analytic_pool_depth_um": r["pool_depth_um"], "analytic_pool_width_um": r["pool_width_um"],
                     "analytic_pool_Dh_um": r["pool_Dh_um"], "mf_u_surface_max_m_s": o["u_surface_max_rel_m_s"],
                     "mf_T_peak_K": o["T_peak_K"], "mf_runtime_s": o["runtime_s"]})
        log(f"{n} {key} {r['P_W']:.0f} W {r['v_m_s']} m/s A {r['A']:.3f}: AM {r['am_class']}, v2 {r['v2_class_deep_branch']}"
            f" -> melt flow {cls} (D {D:.0f}, W {o['pool_width_liquidus_um']:.0f}, Dh {Dh:.0f} um; "
            f"{o['runtime_s']:.0f} s, total {time.time() - t0:.0f} s)")
    t = pd.DataFrame(rows)
    t.to_csv(out / f"v2-map-classes{src_tag}-meltflow.csv", index=False, float_format="%.5g")
    s = {}
    for key, g_ in t.groupby("alloy"):
        s[key] = {"agree_all_classes_meltflow": int((g_["am_class"] == g_["mf_class"]).sum()),
                  "agree_all_classes_analytic": int((g_["am_class"] == g_["v2_class"]).sum()),
                  "confusion_meltflow": pd.crosstab(g_["am_class"], g_["mf_class"]).to_dict()}
        log(key, json.dumps({k: v for k, v in s[key].items() if not k.startswith("confusion")}))
    (out / f"v2-map-classes{src_tag}-meltflow-summary.json").write_text(json.dumps(s, indent=1) + "\n")
    return s


def run_meltflow_v2(out: pathlib.Path, log=print, only=None, drive=False) -> dict:
    """Each case's keyhole (shape, T_w, power outside the opening) from solve_point_v2, then the melt-flow solver
    with Marangoni off and on. The materials are version 2's (sourced k(T)); viscosities as in keyhole_meltflow."""
    import keyhole_meltflow as mf
    rows, fields = [], {}
    for label, key, P, v, Aov in MELTFLOW_CASES:
        if only and only not in label:
            continue
        al = make_alloy(key)
        if key == "al5182":
            r0, T0, hatch = fp.AMB2022["r0"], fp.AMB2022["T0"], None
        else:
            a = fp.ALLOYS[key]
            r0, T0, hatch = a["r0"], a["T0"], a["hatch"]
        res, sol = solve_point_v2(al, P, v, r0, T0, A_override=Aov, hatch=hatch)
        mu0, E = mf.VISCOSITY[key]
        pr = mf.props_from_material(al.m, mu0=mu0, E_mu=E, dsigma_dT=mf.DSIGMA_DT_DEFAULT, C_darcy=mf.C_DARCY_DEFAULT,
                                    evaporation=True)
        kh = None
        if sol:
            kh = dict(z=np.asarray(sol["zn"]), xc=np.asarray(sol["xcn"]), r=np.asarray(sol["rn"]), T_w=sol["T_w"],
                      P_wings=float(sol["A_sf"] * P), a0=res.a0_um * 1e-6)
        g = mf.grid_for(r0, pool_D=max(1.3 * res.pool_depth_solidus_um, 120.0) * 1e-6,
                        pool_W=max(1.5 * res.pool_width_solidus_um, 250.0) * 1e-6,
                        pool_L_rear=max(1.2 * res.pool_length_solidus_um, 500.0) * 1e-6,
                        keyhole_d=(res.d_um * 1e-6 if sol else 0.0), h_fine=r0 / 8)
        if drive and kh is None:
            continue
        if drive and res.d_um < 2 * res.a0_um:
            continue  # the recoil-driven experiment only for keyholes deeper than their opening is wide
        case = mf.Case(label=label, props=pr, P=P, v=v, r0=r0, T0=T0, A=res.A, keyhole=kh, grid=g,
                       wall_drive=drive, wall_sigma=al.m.sigma)
        log(f"{label}: v2 keyhole d {res.d_um:.0f} um, A {res.A:.3f}; grid {g.shape} = {g.n} cells")
        for flow in ((True,) if drive else (False, True)):
            o, T, st, khm = mf.solve_case(case, flow=flow, log=log)
            r = {"case": label, "alloy": key, "P_W": P, "v_m_s": v, "A": res.A, "A_fixed": Aov is not None,
                 "keyhole_depth_um": res.d_um if sol else 0.0, "front_wall_deg": res.front_wall_deg,
                 "analytic_pool_depth_um": res.pool_depth_um, "analytic_pool_width_um": res.pool_width_um,
                 "analytic_pool_length_um": res.pool_length_um,
                 "analytic_pool_length_solidus_um": res.pool_length_solidus_um, "analytic_Q_cond_W": res.Q_cond_W,
                 "wall_drive": drive, "wall_speed_max_m_s": o.get("wall_speed_max_m_s", 0.0), **mf._row(case, o)}
            rows.append(r)
            log(json.dumps({k: (round(x, 2) if isinstance(x, float) else x) for k, x in r.items()}))
            if flow:
                fields[label] = (case, T, st, khm)
    t = pd.DataFrame(rows)
    tag = ("-recoil-driven" if drive else "") + ("-" + only if only else "")
    t.to_csv(out / f"v2-meltflow-runs{tag}.csv", index=False, float_format="%.5g")
    for label, (case, T, st, khm) in fields.items():
        if label in ("blend-375W-0.4-own", "al5182-473W-0.7-A_measured"):
            mf.figure(case, T, st, khm, out / f"v2-meltflow-{label}{'-recoil-driven' if drive else ''}.png")
    return {"rows": len(rows)}


if __name__ == "__main__":
    main()
