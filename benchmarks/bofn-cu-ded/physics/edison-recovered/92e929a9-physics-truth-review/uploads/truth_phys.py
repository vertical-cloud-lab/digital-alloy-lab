"""Physics-based truth for the copper/DED network ("phys", v2), selected with BOFN_TRUTH=phys.

Same eleven nodes, the same eight priced stages and the same objective as the hand-written truth in
`bofn_alloy.py`, but the composition dependence comes from simulations where one exists:

* CALPHAD node (s, f, g, h) from pycalphad with the open MatCalc mc_ni v2.036 database, interpolated
  multilinearly on the 9 x 8 x 4 x 3 grid of `physics/calphad_grid.csv` (`physics/calphad_grid.py`):
  - f: Scheil freezing range to 99% solid, / 250 K
  - g: Fe-rich solid (bcc kappa_I-like or fcc gamma-Fe) present in the melt 1 K above the solidus, / 0.05:
    the primary particles that can nucleate alpha
  - s: yield strength estimate from the alpha matrix composition at 700 C (solid solution) and the kappa
    fraction at 700 C (Orowan-type sqrt(f) term), (sigma - 70 MPa) / 700 MPa
  - h: the lack-of-fusion power threshold (scaled power axis, 1 = about 1 kW) from the thermal conductivity:
    Matthiessen's rule on the alpha composition at 900 C plus the Wiedemann-Franz law, times the solidus
    temperature rise, scaled so pure copper needs 0.95
* beta (retained beta-prime): the equilibrium beta fraction at 900 C from the same grid, times the
  hand-written cooling-rate factor of the original truth (fast travel, low power retains it)
* w (one-hour screen) and m (30-day immersion) from a mixed-potential corrosion model:
  - an oxygen-reduction cathode limited by diffusion (30 uA/cm2 in still seawater)
  - copper dissolution through a parabolic Cu2O film, combined as 1/i = 1/i_L + 1/i_film(t),
    i_film = sqrt(K(t) / 2t)
  - K falls with Al in the alpha matrix at once (the Al2O3-rich layer forms in minutes) and with Ni and Fe
    in solution over tau = 3 days (the Ni/Fe-doped film matures over days to weeks)
  - retained beta-prime dissolves selectively at a constant rate after a one-day incubation, which a
    one-hour measurement cannot see
  - porosity adds area
  Integrated over 30 days (mass loss) and evaluated at 1 hour (the screen).
  m = 1 - log10(M / M_LO) / 1.5 on [0, 1], so m_ref (C71500 at its best settings) means
  "mass loss no greater than 70-30 Cu-Ni", the proposal's H5 definition.
  The constants are calibrated to measured values and are listed in CAL (see physics/README.md).
* q, rho_u, rho_m, U: the original forms (they take f, g, h from the CALPHAD node above).

`feasible(x)` returns the proposal's own limits on the search space (Table tab:space and the text
around it): calculated liquidus at most 1,250 C, copper at least 65 wt%, Ni >= Fe above 7 wt% Al,
Fe <= 2.3 wt% below 1.5 wt% Al.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path

import torch

HERE = Path(__file__).parent
GRID_CSV = HERE / "calphad_grid.csv"
WT_MAX = torch.tensor([30.0, 9.5, 4.5, 4.0], dtype=torch.double)  # Ni, Al, Fe, Mn at x = 1
AXES = {"NI": [0, 2.5, 5, 7.5, 10, 15, 20, 25, 30], "AL": [0, 1.5, 3, 4.5, 6, 7, 8, 9.5], "FE": [0, 1.5, 3, 4.5], "MN": [0, 2, 4]}
MW = {"NI": 58.6934, "AL": 26.9815385, "FE": 55.845, "MN": 54.938044, "CU": 63.546}
P_CAP = 0.5
F_CRACK = 0.80  # crack onset on the effective Scheil index (200 K of Scheil range; C71500 has 167 K and deposits dense)
F_SAFE = 0.50  # the CALPHAD crack screen: Scheil range at most 125 K
LIQ_MAX = 1250.0

# corrosion-model constants (units: uA/cm2, seconds, wt%); see physics/README.md for the sources
CAL = {  # fitted by physics/calibrate_corrosion.py to the same-test measurements listed there (residuals in physics/README.md)
    "i_L": 30.0,  # O2 diffusion limit in still, aerated seawater (not measured for these alloys: a prior)
    "K_cu": 1.0e5,  # parabolic film constant of copper (the fit's lower bound: the paralinear term dominates)
    "i_fl": 3.604,  # steady dissolution through copper's film, uA/cm2 (copper's rate barely falls after the first week)
    "a_al": 0.05,  # decades per 7 wt% Al in alpha, at once (the fit's lower bound: Al bronze loses 2x more than 70-30)
    "a_ni0": 0.100,  # decades per 30 wt% Ni in alpha, at once
    "a_ni": 0.513,  # decades per 30 wt% Ni in alpha, as the film matures
    "a_fe": 0.577,  # decades per 1.5 wt% Fe in solution (capped at 1.5), as the film matures
    "tau": 10.0 * 86400.0,  # maturation time of the Ni/Fe-doped film (the fit's upper bound)
    "i_sel": 5.0,  # selective dissolution of retained beta-prime, per unit area fraction (not measured: a prior)
    "t_inc": 86400.0,  # incubation of selective attack (an occluded chemistry has to develop)
    "c_por": 1.0,  # extra mass loss per unit porosity (as sensitive to porosity as the hand-written truth)
    "M_lo": 22.0,  # uA*day/cm2 at m = 1 (mass loss over 30 days; 1 uA*day/cm2 is about 0.3 um of Cu)
    "decades": 1.5,  # m spans 1.5 decades of mass loss, so the gate's 0.05 is a 19% change in mass loss
    "i1h_lo": 1.0,  # uA/cm2 at w = 1
    "w_decades": 1.5,
}
T_DAY = 86400.0
TGRID = torch.logspace(0, math.log10(30 * T_DAY), 80, dtype=torch.double)  # 1 s to 30 days


def sig(z):
    return torch.sigmoid(z)


# --------------------------------------------------------------------------- CALPHAD grid
class Grid:
    """Multilinear interpolation of pycalphad results on the (Ni, Al, Fe, Mn) grid, in wt%."""

    FIELDS = ["T_liq", "T_sol", "sch_range99", "beta_900", "kappa_fe_700", "kappa_nial_700", "sol1_kappa_fe", "sol1_fcc_feni",
              "a700_NI", "a700_AL", "a700_FE", "a700_MN", "a900_NI", "a900_AL", "a900_FE", "a900_MN"]

    def __init__(self, path=GRID_CSV):
        self.ax = [torch.tensor(AXES[k], dtype=torch.double) for k in ("NI", "AL", "FE", "MN")]
        shape = [len(a) for a in self.ax]
        self.V = {f: torch.full(shape, float("nan"), dtype=torch.double) for f in self.FIELDS}
        idx = {k: {float(v): i for i, v in enumerate(AXES[k])} for k in AXES}
        with open(path) as fh:
            for r in csv.DictReader(fh):
                key = (idx["NI"][float(r["Ni"])], idx["AL"][float(r["Al"])], idx["FE"][float(r["Fe"])], idx["MN"][float(r["Mn"])])
                nominal = {"NI": float(r["Ni"]), "AL": float(r["Al"]), "FE": float(r["Fe"]), "MN": float(r["Mn"])}
                for f in self.FIELDS:
                    v = r.get(f, "")
                    try:
                        val = float(v)
                    except ValueError:
                        val = float("nan")
                    if f[:1] == "a" and f[1:4] in ("700", "900") and not math.isfinite(val):
                        val = nominal[f.split("_")[1]]  # no alpha at that temperature: the matrix is beta, use the nominal value
                    if f == "sch_range99" and not math.isfinite(val):
                        val = 2.0 * float(r["eq_range"])
                    self.V[f][key] = val
        self.missing = int(torch.isnan(self.V["T_liq"]).sum())

    def __call__(self, field, wt):
        """wt [..., 4] in wt% (Ni, Al, Fe, Mn) -> [...]"""
        V = self.V[field]
        lo, t = [], []
        for d, a in enumerate(self.ax):
            w = wt[..., d].clamp(float(a[0]), float(a[-1]))
            i = (torch.searchsorted(a, w.contiguous(), right=True) - 1).clamp(0, len(a) - 2)
            lo.append(i)
            t.append(((w - a[i]) / (a[i + 1] - a[i])).clamp(0, 1))
        out = torch.zeros_like(wt[..., 0])
        for corner in range(16):
            b = [(corner >> d) & 1 for d in range(4)]
            wgt = torch.ones_like(out)
            for d in range(4):
                wgt = wgt * (t[d] if b[d] else 1 - t[d])
            out = out + wgt * V[lo[0] + b[0], lo[1] + b[1], lo[2] + b[2], lo[3] + b[3]]
        return out


_GRID = None


def grid():
    global _GRID
    if _GRID is None:
        _GRID = Grid()
    return _GRID


def wt_of(c):
    return c[..., :4].clamp(0, 1) * WT_MAX


def at_pct(wt):
    """wt% (Ni, Al, Fe, Mn; Cu balance) [..., 4] -> at% [..., 4]."""
    m = torch.stack([wt[..., 0] / MW["NI"], wt[..., 1] / MW["AL"], wt[..., 2] / MW["FE"], wt[..., 3] / MW["MN"]], -1)
    cu = (100 - wt.sum(-1)).clamp(min=0) / MW["CU"]
    return 100 * m / (m.sum(-1, keepdim=True) + cu.unsqueeze(-1))


# --------------------------------------------------------------------------- physics of the CALPHAD node
def conductivity(wt_alpha):
    """Thermal conductivity (W/m K, room temperature) from the alpha composition: Matthiessen's rule
    (residual resistivity per at%: Ni 1.1, Al 0.65, Fe 2.0, Mn 2.9 uOhm cm; fitted to the CDA electrical
    conductivities of C71500, C70600, C61400 and C95800 within 20%) and the Wiedemann-Franz law, plus 5 W/m K
    of lattice conduction."""
    x = at_pct(wt_alpha)
    rho = 1.7 + 1.1 * x[..., 0] + 0.65 * x[..., 1] + 2.0 * x[..., 2] + 2.9 * x[..., 3]  # uOhm cm
    return 2.44e-8 * 300.0 / (rho * 1e-8) + 5.0


K_CU = float(conductivity(torch.zeros(4, dtype=torch.double)))


def calphad_node(c):
    """(s, f, g, h) for compositions c [..., 4] on [0, 1]."""
    G, wt = grid(), wt_of(c)
    a7 = torch.stack([G(f"a700_{e}", wt) for e in ("NI", "AL", "FE", "MN")], -1)
    a9 = torch.stack([G(f"a900_{e}", wt) for e in ("NI", "AL", "FE", "MN")], -1)
    fk = (G("kappa_fe_700", wt) + G("kappa_nial_700", wt)).clamp(min=0)
    sigma = 70 + 3.5 * a7[..., 0] + 17 * a7[..., 1] + 12 * a7[..., 2] + 10 * a7[..., 3] + 600 * fk.sqrt()  # MPa
    s = ((sigma - 70) / 700).clamp(0, 1)
    f = (G("sch_range99", wt) / 250).clamp(0, 1)
    g = ((G("sol1_kappa_fe", wt) + G("sol1_fcc_feni", wt)).clamp(min=0) / 0.05).clamp(0, 1)
    h = 0.95 * conductivity(a9) / K_CU * (G("T_sol", wt) - 25) / (1084.6 - 25)
    return s, f, g, h


def liquidus(c):
    return grid()("T_liq", wt_of(c))


NI_MIN = float(os.environ.get("BOFN_NI_MIN", 0.0))  # optional nickel floor (wt%) for the restricted-space runs


def feasible(x):
    """The proposal's own limits (Table tab:space): liquidus <= 1,250 C, Cu >= 65 wt%,
    Ni >= Fe when Al > 7 wt%, Fe <= 2.3 wt% when Al < 1.5 wt%; plus Ni >= BOFN_NI_MIN if set."""
    wt = wt_of(x)
    ni, al, fe = wt[..., 0], wt[..., 1], wt[..., 2]
    ok = (wt.sum(-1) <= 35.0) & (liquidus(x) <= LIQ_MAX) & (ni >= NI_MIN)
    ok = ok & ((al <= 7.0) | (ni >= fe)) & ((al >= 1.5) | (fe <= 2.3))
    return ok


# --------------------------------------------------------------------------- corrosion model
def film_features(c):
    """(Al in alpha / 7, Ni in alpha / 30, Fe in solution / 1.5 capped at 1) for compositions c [..., 4].
    The film reads the alpha solid solution retained from 900 C by the fast cooling of DED. (At 700 C mc_ni
    puts nearly all of NAB's Ni into NiAl, leaving 0.2 wt% in alpha against about 3 wt% measured.)"""
    G, wt = grid(), wt_of(c)
    ni = torch.minimum(wt[..., 0], G("a900_NI", wt).clamp(min=0))
    al = torch.minimum(wt[..., 1], G("a900_AL", wt).clamp(min=0))
    fe = torch.minimum(wt[..., 2], G("a900_FE", wt).clamp(min=0))
    # the measured Ni effect does not saturate by 10 wt% (Yang 2019; Lewis and LaQue 1981), so it is linear
    return al / 7.0, ni / 30.0, fe.clamp(max=1.5) / 1.5


def film_terms(c, feats=None):
    """(fast, slow) reductions of log10 of the film's transport for compositions c [..., 4]."""
    al7, ni30, fe15 = film_features(c) if feats is None else feats
    fast = CAL["a_al"] * al7 + CAL["a_ni0"] * ni30  # at once: the Al2O3-rich layer, and Ni in the metal surface
    slow = CAL["a_ni"] * ni30 + CAL["a_fe"] * fe15  # over days: Ni and Fe enrich the Cu2O film
    return fast, slow


def current(t, fast, slow, doped=None):
    """General corrosion current (uA/cm2) at time t (s); `doped` overrides the film's maturation (0 to 1)."""
    mat = (1 - torch.exp(-t / CAL["tau"])) if doped is None else doped
    q = 10 ** (-(fast + slow * mat))  # film quality: how much the Al2O3 layer and the Ni/Fe doping cut transport
    i_f = (CAL["K_cu"] * q / (2 * t)).sqrt()  # parabolic film growth
    return 1 / (1 / CAL["i_L"] + 1 / i_f) + CAL["i_fl"] * q  # plus steady dissolution of the film (paralinear)


def mass_loss_30d(fast, slow, beta, rho_m):
    """uA*day/cm2 over 30 days: general film-limited corrosion + selective beta-prime attack, times porosity."""
    tt = TGRID.view(*([1] * fast.dim()), -1)
    i = current(tt, fast.unsqueeze(-1), slow.unsqueeze(-1))
    gen = torch.trapezoid(i, tt.expand_as(i), dim=-1) / T_DAY + CAL["i_L"] * float(TGRID[0]) / T_DAY
    sel = beta.clamp(min=0) * CAL["i_sel"] * (30 * T_DAY - CAL["t_inc"]) / T_DAY
    return (gen + sel) * (1 + CAL["c_por"] * (1 - rho_m).clamp(min=0))


def m_index(M):
    return (1 - torch.log10(M / CAL["M_lo"]) / CAL["decades"]).clamp(0, 1)


def w_index(i1h):
    return (1 - torch.log10(i1h / CAL["i1h_lo"]) / CAL["w_decades"]).clamp(0, 1)


# --------------------------------------------------------------------------- the truth
class PhysTruth:
    """Drop-in replacement for bofn_alloy.AlloyTruth (same nodes and inputs under the phys SPEC)."""

    name = "phys"

    def __init__(self, kappa: float = 1.0, eta: float = 1.0, m_ref: float | None = None):
        self.kappa, self.eta = kappa, eta
        self.m_ref = m_ref if m_ref is not None else reference_m()[0]

    def node(self, name, inp):
        if name in ("s", "f", "g", "h"):
            return dict(zip(("s", "f", "g", "h"), calphad_node(inp[..., :4])))[name]
        if name == "q":
            a, mn, f = inp[..., 0], inp[..., 1], inp[..., 2]
            a_opt = 0.35 + 0.40 * f
            return torch.exp(-(((a - a_opt) / 0.28) ** 2)) * (1 - 0.35 * f**2) * (1 - 0.10 * mn)
        if name in ("rho_u", "rho_m"):
            P, v, f, g, h, q = (inp[..., i] for i in range(6))
            u = P - v - (0.05 + 0.25 * f)
            window = torch.exp(-((u / 0.2) ** 2)) * (1 - 0.35 * sig((P - 0.85) / 0.05))
            lof = sig((h - P) / 0.08)
            g = g.clamp(min=0)
            f_eff = f * (1 - self.kappa * 0.85 * g / (g + 0.12))
            crack = sig((f_eff - F_CRACK) / 0.05)
            rho = window * q.clamp(min=0) ** 0.3 * (1 - 0.75 * crack) * (1 - lof)
            if name == "rho_u":
                rho = rho * (0.95 + 0.05 * q.clamp(min=0))
            return rho
        if name == "beta":  # inputs (Ni, Al, Fe, Mn, P, v, rho_m)
            b = grid()("beta_900", wt_of(inp[..., :4])).clamp(0, 1)
            P, v = inp[..., 4], inp[..., 5]
            return b * sig((v - P + 0.2) / 0.15)
        if name == "U":
            s, rho_m, beta = inp[..., 0], inp[..., 1], inp[..., 2]
            return (0.25 + 0.75 * s) * rho_m * (1 + 0.15 * beta)
        if name in ("w", "m"):  # inputs (Ni, Al, Fe, Mn, rho_m, beta[, w])
            c, rho_m, beta = inp[..., :4], inp[..., 4], inp[..., 5]
            fast, slow = film_terms(c)
            if name == "m":
                return m_index(mass_loss_30d(fast, slow, beta, rho_m))
            # one hour on a fresh surface: at eta = 1 the Ni/Fe doping has not formed and selective attack has
            # not started; at eta = 0 the screen reads the mature film and the beta-prime attack (a perfect proxy)
            t1 = torch.tensor(3600.0, dtype=torch.double)
            doped = self.eta * (1 - torch.exp(-t1 / CAL["tau"])) + (1 - self.eta)
            i1 = current(t1, fast, slow, doped=doped) + (1 - self.eta) * beta.clamp(min=0) * CAL["i_sel"]
            return w_index(i1 * (1 + CAL["c_por"] * (1 - rho_m).clamp(min=0)))
        raise KeyError(name)

    def full(self, x):
        out = {}
        s, f, g, h = calphad_node(x[..., :4])
        out.update(s=s, f=f, g=g, h=h)
        out["q"] = self.node("q", torch.stack([x[..., 4], x[..., 3], f], -1))
        Pu = x[..., 5].clamp(max=P_CAP)
        out["rho_u"] = self.node("rho_u", torch.stack([Pu, x[..., 6], f, g, h, out["q"]], -1))
        out["rho_m"] = self.node("rho_m", torch.stack([x[..., 5], x[..., 6], f, g, h, out["q"], out["rho_u"]], -1))
        out["beta"] = self.node("beta", torch.cat([x[..., :4], x[..., 5:7], out["rho_m"].unsqueeze(-1)], -1))
        out["U"] = self.node("U", torch.stack([s, out["rho_m"], out["beta"]], -1))
        cw = torch.cat([x[..., :4], out["rho_m"].unsqueeze(-1), out["beta"].unsqueeze(-1)], -1)
        out["w"] = self.node("w", cw)
        out["m"] = self.node("m", torch.cat([cw, out["w"].unsqueeze(-1)], -1))
        return out

    def objective(self, x, full=None):
        out = full or self.full(x)
        B = (x[..., :4] * torch.tensor([1.0, 0.3, 0.0, 0.2], dtype=x.dtype)).sum(-1)
        return out["U"] * sig((out["m"] - self.m_ref) / 0.05) - 0.3 * B


REFERENCE = {"C71500 (70-30 Cu-Ni)": [1.0, 0.0, 0.15, 0.20], "C70600 (90-10 Cu-Ni)": [0.333, 0.0, 0.31, 0.20], "C95800 (NAB)": [0.15, 0.95, 0.90, 0.30]}
_MREF = None


REF_ALLOY = os.environ.get("BOFN_REF", "C71500")  # the immersion reference: C71500 (H5 as written) or C70600


def reference_m_for(alloy):
    """(m, rho_m, x) of a reference alloy deposited dense at its best (a, P, v), not cached."""
    t = PhysTruth(1.0, 1.0, m_ref=0.0)
    key = next(k for k in REFERENCE if k.startswith(alloy))
    c = torch.tensor(REFERENCE[key], dtype=torch.double)
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=0).draw(16384).double()
    X = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
    out = t.full(X)
    j = out["rho_m"].argmax()
    return float(out["m"][j]), float(out["rho_m"][j]), X[j]


def reference_m():
    """Immersion index of the reference alloy (C71500 by default; BOFN_REF=C70600 for 90-10) deposited dense at its
    best (a, P, v) under the phys truth."""
    global _MREF
    if _MREF is None:
        t = PhysTruth(1.0, 1.0, m_ref=0.0)
        key = next(k for k in REFERENCE if k.startswith(REF_ALLOY))
        c = torch.tensor(REFERENCE[key], dtype=torch.double)
        apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=0).draw(16384).double()
        X = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
        out = t.full(X)
        j = out["rho_m"].argmax()
        _MREF = (float(out["m"][j]), float(out["rho_m"][j]), X[j])
    return _MREF
