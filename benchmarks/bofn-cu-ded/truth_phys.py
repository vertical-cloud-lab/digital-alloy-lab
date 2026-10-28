"""Physics-based truth for the copper/DED network (`BOFN_TRUTH=phys`).

The hand-written truth (`bofn_alloy.AlloyTruth`) is kept for every node that has no better source.
Replaced here:

- **CALPHAD node** (s, f, g) from an 864-composition pycalphad grid with the open MatCalc mc_ni
  database (`phys/calphad_grid.py`, `phys/calphad_grid.csv`), interpolated multilinearly:
  - f, the solidification index: the equilibrium freezing range / 200 C (70-30 Cu-Ni is 58 C, NAB 76 C);
  - g, the nucleant: the mole fraction of Fe-rich solid (kappa_I-like bcc, or Fe/Ni-rich fcc in
    Al-free alloys) one degree above the solidus, / 0.045 (NAB's), capped at 1;
  - s, the strengthening potential: a yield-strength estimate from the phase fractions at 600 C
    (Orowan-type square roots of the NiAl/Ni3Al and Fe-rich bcc kappa fractions; the Fe/Ni-rich fcc of
    Al-free Cu-Ni-Fe is not counted) plus solid-solution terms from the composition of alpha at 600 C,
    scaled to [0, 1].
- **h, the conductivity index**: thermal conductivity from the Wiedemann-Franz law on a Matthiessen
  resistivity (solute increments from handbook alloys: C70600, C71500, C61400, C60800), as
  h = 0.6 sqrt(k / k_Cu), so pure copper keeps the hand-written value (0.6) and the lack-of-fusion
  threshold follows the real tenfold drop in conductivity by 10 wt% Ni.
- **m, the 30-day immersion index**: a film model fitted to same-test seawater corrosion data
  (`phys/fit_corrosion.py`, `phys/corrosion_fit.json`): ln(rate) is linear in a saturating nickel film
  term, Al, Al^2 and Fe in solution, with a separate intercept per study, so only within-study ratios
  are used. m = M_LEVEL - SLOPE * (ln rate - ln rate of C71500), minus the hand-written beta-prime and
  porosity terms. The bar ("passes immersion") is the dense 90-10 Cu-Ni (C70600) reference by default
  (`BOFN_BAR=7030` for the 70-30 bar).
- **The proposal's search-space limits** (`feasible`): liquidus at most 1,250 C (from the grid),
  Cu at least 65 wt%, Ni >= Fe when Al > 7 wt%, Fe <= 2.3 wt% when Al < 1.5 wt%. Every candidate pool
  of every policy is filtered by them when this truth is on.

Unchanged from the hand-written truth: q (powder), the process window and crack terms of rho_u and
rho_m, beta (retained beta-prime), U (tensile) and the one-hour screen w.
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import torch

import bofn_alloy as BA

HERE = Path(__file__).parent
GRID_CSV = HERE / "phys" / "calphad_grid.csv"
FIT_JSON = HERE / "phys" / "corrosion_fit.json"
WT_MAX = torch.tensor([30.0, 9.5, 4.5, 4.0])  # scaled [0, 1] -> wt% (Ni, Al, Fe, Mn)
SHAPE = (8, 6, 6, 3)  # grid levels per element; uniform in the scaled coordinates
FIELDS = ["liquidus_C", "solidus_C", "range_C", "kappa_fe_sol", "fcc_feni_sol", "nial_sol", "alpha_600", "beta_600", "kappa_fe_600", "fcc_feni_600", "nial_600",
          "gprime_600", "alpha600_xni", "alpha600_xal", "alpha600_xfe", "alpha600_xmn", "beta_900"]
BAR = os.environ.get("BOFN_BAR", "9010")
F_RANGE = 200.0  # C of equilibrium freezing range per unit of the solidification index
G_REF = 0.045  # NAB's Fe-rich solid fraction just above the solidus
# Matthiessen resistivity increments, micro-ohm cm per wt% in solution (handbook alloys: C70600 is
# 19.1, C71500 37.5, C61400 about 12.3, C60800 about 10.1 micro-ohm cm; copper 1.7). Fe mostly
# precipitates in these alloys, so its effective increment is small.
RHO_CU, D_RHO = 1.70, torch.tensor([1.25, 1.50, 1.00, 3.00])
K_CU = 732.0 / RHO_CU + 5.0  # W/m K: Wiedemann-Franz at 300 K plus a small lattice term (about 435)
LIQ_MAX = 1250.0  # C, the proposal's limit (atomizer and DED feedstock)

_GRID = None
_FIT = None


def load_grid():
    """[8, 6, 6, 3, len(FIELDS)] tensor; failed points filled from the nearest grid neighbours."""
    global _GRID
    if _GRID is not None:
        return _GRID
    rows = list(csv.DictReader(open(GRID_CSV)))
    assert len(rows) == 864, f"{GRID_CSV}: {len(rows)} rows, expected 864"
    vals = torch.full((864, len(FIELDS)), float("nan"))
    for i, r in enumerate(rows):
        if r.get("ok") == "1":
            for j, k in enumerate(FIELDS):
                v = r.get(k, "")
                vals[i, j] = float(v) if v not in ("", "nan") else 0.0
            if r.get("liquidus_C", "") in ("", "nan"):
                # NiAl (B2) still solid at the top of the 1,550 C scan (high Ni with 9.5 wt% Al): the liquidus
                # is at least 1,550 C, far outside the 1,250 C limit; the freezing range is at least that minus the solidus
                vals[i, FIELDS.index("liquidus_C")] = 1550.0
                vals[i, FIELDS.index("range_C")] = 1550.0 - float(r["solidus_C"])
    G = vals.reshape(*SHAPE, len(FIELDS))
    bad = torch.isnan(G[..., 0])
    for idx in bad.nonzero().tolist():  # average of the valid axis neighbours
        nb = []
        for ax in range(4):
            for dlt in (-1, 1):
                j = list(idx)
                j[ax] += dlt
                if 0 <= j[ax] < SHAPE[ax] and not bad[tuple(j)]:
                    nb.append(G[tuple(j)])
        G[tuple(idx)] = torch.stack(nb).mean(0)
    _GRID = G
    return G


def interp(c):
    """Multilinear interpolation of every grid field at scaled compositions c [..., 4] -> [..., F]."""
    G = load_grid()
    c = c.clamp(0, 1)
    out = 0.0
    pos, lo, fr = [], [], []
    for ax, n in enumerate(SHAPE):
        p = c[..., ax] * (n - 1)
        l0 = p.floor().clamp(max=n - 2).long()
        pos.append(p)
        lo.append(l0)
        fr.append(p - l0)
    for corner in range(16):
        bits = [(corner >> ax) & 1 for ax in range(4)]
        w = torch.ones_like(c[..., 0])
        for ax in range(4):
            w = w * (fr[ax] if bits[ax] else 1 - fr[ax])
        v = G[lo[0] + bits[0], lo[1] + bits[1], lo[2] + bits[2], lo[3] + bits[3]]
        out = out + w.unsqueeze(-1) * v
    return out


def field(c, name):
    return interp(c)[..., FIELDS.index(name)]


def wt(c):
    return c[..., :4].clamp(0, 1) * WT_MAX


def feasible(x):
    """The proposal's search-space limits for designs or compositions x [..., >= 4] (scaled)."""
    w = wt(x[..., :4])
    ni, al, fe, mn = w.unbind(-1)
    ok = w.sum(-1) <= 35.0  # Cu >= 65 wt%
    ok = ok & ((al <= 7.0) | (ni >= fe))
    ok = ok & ((al >= 1.5) | (fe <= 2.3))
    return ok & (field(x[..., :4], "liquidus_C") <= LIQ_MAX)


def conductivity(c):
    """W/m K at 300 K: Wiedemann-Franz on a Matthiessen resistivity of the nominal composition."""
    rho = RHO_CU + (wt(c) * D_RHO).sum(-1)
    return 732.0 / rho + 5.0


def strength_mpa(c):
    """Yield-strength estimate (MPa) of the aged or slowly cooled alloy from its CALPHAD phase fractions:
    copper 60 MPa, Orowan-type sqrt terms for the precipitates, linear solid solution in alpha (wt%)."""
    v = interp(c)
    F = lambda n: v[..., FIELDS.index(n)].clamp(min=0)
    ppt = 700.0 * (F("nial_600") + F("gprime_600")).sqrt() + 250.0 * F("kappa_fe_600").sqrt()
    # alpha at 600 C: mole fractions -> approximate wt% (molar masses close to copper's except Al)
    ni_a, al_a, mn_a = 100 * F("alpha600_xni") * 58.7 / 63.5, 100 * F("alpha600_xal") * 27.0 / 63.5, 100 * F("alpha600_xmn") * 54.9 / 63.5
    ss = 3.0 * ni_a + 18.0 * al_a + 9.0 * mn_a
    return 60.0 + ss + ppt


S_SCALE = 650.0  # MPa of strength above copper per unit of s


def load_fit():
    global _FIT
    if _FIT is None:
        _FIT = json.loads(FIT_JSON.read_text())
    return _FIT


def ln_rate(c):
    """Fitted ln(30-day corrosion rate) relative to C71500, from the nominal composition."""
    fit = load_fit()
    w = wt(c)
    ni, al, fe, mn = w.unbind(-1)
    b = fit["coef"]
    def z(ni, al, fe):
        film = 1 - torch.exp(-ni / fit["ni_scale"]) if fit.get("ni_form", "sat") == "sat" else ni / 10.0
        return b["ni"] * film + b["al"] * al + b.get("al2", 0.0) * al**2 / 10.0 + b["fe"] * fe.clamp(max=fit.get("fe_sol", 1.5))

    wr = wt(torch.tensor(BA.REFERENCE["C71500 (70-30 Cu-Ni)"]))
    return z(ni, al, fe) - z(wr[0], wr[1], wr[2])


M_LEVEL, SLOPE = 0.85, 0.30  # m of dense C71500, and m per unit of ln(rate)


class PhysTruth(BA.AlloyTruth):
    def node(self, name, inp):
        if name in ("s", "f", "g", "h"):
            c = inp[..., :4]
            if name == "s":
                return ((strength_mpa(c) - 60.0) / S_SCALE).clamp(0, 1)
            if name == "f":
                return (field(c, "range_C") / F_RANGE).clamp(0, 1)
            if name == "g":
                v = interp(c)
                return ((v[..., FIELDS.index("kappa_fe_sol")] + v[..., FIELDS.index("fcc_feni_sol")]) / G_REF).clamp(0, 1)
            return 0.6 * (conductivity(c) / K_CU).sqrt()
        if name == "m":
            ni, al, fe, rho_m, beta = (inp[..., i] for i in range(5))
            c = torch.stack([ni, al, fe, torch.zeros_like(ni)], -1)  # the immersion node does not see Mn (as in the network)
            return (M_LEVEL - SLOPE * ln_rate(c) - 0.60 * al * beta - 0.30 * (1 - rho_m)).clamp(0, 1)
        return super().node(name, inp)


def reference_m(name, kappa=1.0, eta=1.0):
    """Immersion index of a reference alloy deposited at its densest settings in this truth."""
    t = PhysTruth(kappa, eta, m_ref=0.0)
    c = torch.tensor(BA.REFERENCE[name])
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=0).draw(16384).double()
    X = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
    out = t.full(X)
    j = out["rho_m"].argmax()
    return float(out["m"][j]), float(out["rho_m"][j]), X[j]


def phys_m_ref():
    return reference_m("C70600 (90-10 Cu-Ni)" if BAR == "9010" else "C71500 (70-30 Cu-Ni)")
