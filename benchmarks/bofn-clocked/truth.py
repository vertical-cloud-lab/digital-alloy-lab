"""Synthetic truth for the clocked benchmark. Everything here is invented; nothing is fitted to data.

The core is bofn-prelim's alloy network (`benchmarks/bofn-prelim/bofn_alloy.py`, `AlloyTruth`), ported to numpy
node for node (tests/test_clocked.py checks the port against the original to 1e-12):

    CALPHAD   (c)                 -> s (strengthening phase), f (freezing range), g (primary nucleant)
    Atomize   (a, g)              -> q (powder quality)
    LPBF      (P, v, f, g, q)     -> rho (dense, crack-free fraction)
    Tensile   (s, rho)            -> U (strength)
    objective = U - lam * B(c)    (B: critical-mineral burden, known)

`kappa` is how strongly the nucleant suppresses hot cracking, which a CALPHAD freezing-range screen can't see
(Martin et al., Nature 2017). kappa = 1: the screen misses the effect; kappa = 0: the screen's physics is right.

What this benchmark adds to bofn-prelim's truth (all assumed; see the README's assumptions table):

* **Noise and failures**: powder quality is measured with noise; every build has its own random density offset;
  every coupon's density reading and every tensile bar have their own scatter; an atomizer run can yield no usable
  powder, a build can fail outright, and a bar can break invalidly.
* **Corrosion** (a second output of each coupon): log corrosion rate from composition and porosity. An alloy counts
  as discovered only if its 30-day immersion passes (rate <= r_max). Interim readings at days 1, 3, 7 and 14 come from
  the coupon's own film-growth trajectory: unbiased on average once the lab's mean film factor is divided out, but
  noisier the earlier they are.
* **Routes**: gas-atomized powder (outside supplier) has high quality whatever the atomizer setting but shifts the
  laser-process ridge; the partner's printer has its own ridge offset. The model sees route and machine as inputs.
* **Sites and epochs**: another lab's printer and tensile frames read differently (site offsets), and the lab itself
  drifts between campaigns (epoch offsets). Used by the provenance experiments.
* **Cross-system truth** (`CrossTruth`, stretch): three alloy families in one composition space (see its docstring).
"""
from __future__ import annotations

import math

import numpy as np

LAMBDA = 0.3
NC = 4  # composition dims of the core truth: Zn+Mg, Cu, Zr, Sc

# noise and failure model (assumed; README "Assumptions")
SIG_Q = 0.02  # powder-quality measurement
SIG_BUILD = 0.015  # build-to-build density offset (physical: the whole build)
SIG_COUPON = 0.015  # coupon density reading (Archimedes + optical crack check)
SIG_BAR = 0.025  # bar-to-bar scatter of the strength index (defects, machining)
P_FAIL_ATOMIZE = 0.10  # an ultrasonic run yields too little usable powder
P_FAIL_GAS = 0.02
P_FAIL_BUILD = 0.08  # recoater crash, delamination, support failure: the whole build is lost
P_BAR_INVALID = 0.03  # a bar breaks outside the gauge or slips: no result

# corrosion: ln r = LNR0 + CORR_W . c + CORR_POR * (1 - rho); pass if ln r <= LN_RMAX
LNR0 = 0.0
CORR_W = np.array([0.55, 1.7, -0.5, -0.3])
CORR_POR = 3.0
LN_RMAX = 0.95
IMM_DAYS = (1, 3, 7, 14, 30)
IMM_SIG = {1: 0.45, 3: 0.32, 7: 0.20, 14: 0.12, 30: 0.04}  # spread of the day-d estimate of ln r (incl. film factor)

# route and machine effects on the laser-process ridge (u = P - v - (0.05 + 0.25 f) - shift) and on density
SHIFT = {"us": 0.0, "gas": 0.06, "ih": 0.0, "pt": -0.05}
RHO_OFF = {"ih": 0.0, "pt": 0.01}


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def burden(c):
    c = np.asarray(c, float)
    return 0.15 * c[..., 0] + 0.1 * c[..., 1] + 0.2 * c[..., 2] + 1.0 * c[..., 3]


class Truth:
    """bofn-prelim's network with noise, routes, corrosion, sites and epochs.

    lam: weight of the mineral burden (the time-machine campaigns change it); ln_rmax: corrosion limit.
    site_shift / site_rho / site_U: another lab's ridge shift and density offset (physical: its printer) and its
    tensile-frame offset (a reading). epoch_rho / epoch_U: the lab's own calibration drift between campaigns (dict
    epoch -> offset), added to density readings and tensile readings; the alloys themselves don't change.
    """

    ncomp = NC

    def __init__(self, kappa=1.0, lam=LAMBDA, ln_rmax=LN_RMAX, site_shift=None, site_rho=None, site_U=None,
                 epoch_rho=None, epoch_U=None):
        self.kappa, self.lam, self.ln_rmax = kappa, lam, ln_rmax
        self.site_shift = site_shift or {}
        self.site_rho = site_rho or {}
        self.site_U = site_U or {}
        self.epoch_rho = epoch_rho or {}
        self.epoch_U = epoch_U or {}

    # ---------------------------------------------------------------- nodes (bofn-prelim, vectorized)
    @staticmethod
    def calphad(c):
        c = np.asarray(c, float)
        c1, c2, c3, c4 = c[..., 0], c[..., 1], c[..., 2], c[..., 3]
        s = (1 - np.exp(-(1.4 * c1 + 0.9 * c2 + 1.5 * c1 * c2)) + 0.1 * c3 + 0.3 * c4) / 1.2
        f = 0.65 * c1 + 0.55 * c2 - 0.25 * c1 * c2 + 0.05 * c3 + 0.03 * c4
        g = (0.6 * np.clip(c3, 0, None) ** 1.5 + 0.9 * np.clip(c4, 0, None) ** 1.2) * (1 + 0.2 * c1) / 1.8
        return s, f, g

    @staticmethod
    def q(a, g, route="us"):
        a, g = np.asarray(a, float), np.asarray(g, float)
        if route == "gas":  # inert-gas atomization: spherical, narrow PSD whatever the ultrasonic setting
            return 0.97 - 0.04 * g + 0 * a
        a_opt = 0.3 + 0.45 * g
        return np.exp(-(((a - a_opt) / 0.28) ** 2)) * (0.9 + 0.1 * (1 - g))

    def rho(self, P, v, f, g, q, machine="ih", route="us", site="own", epoch=0):
        P, v, f, g, q = (np.asarray(t, float) for t in (P, v, f, g, q))
        shift = SHIFT[route] + SHIFT[machine] + self.site_shift.get(site, 0.0)
        u = P - v - (0.05 + 0.25 * f) - shift
        window = np.exp(-((u / 0.2) ** 2)) * (1 - 0.35 * sigmoid((P - 0.85) / 0.05))
        g = np.clip(g, 0, None)
        f_eff = f * (1 - self.kappa * 0.85 * g / (g + 0.12))
        crack = sigmoid((f_eff - 0.38) / 0.05)
        r = window * np.clip(q, 0, None) ** 0.3 * (1 - 0.75 * crack)
        r = r + RHO_OFF[machine] + self.site_rho.get(site, 0.0)
        return np.clip(r, 0.0, 1.0)

    @staticmethod
    def U(s, rho):
        return (0.25 + 0.75 * np.asarray(s, float)) * np.asarray(rho, float)

    @staticmethod
    def ln_corr(c, rho):
        c = np.asarray(c, float)
        return LNR0 + c[..., :NC] @ CORR_W + CORR_POR * (1 - np.asarray(rho, float))

    # ---------------------------------------------------------------- design-level truth
    def design(self, c, a, P, v, route="us", machine="ih"):
        """True (objective, ln corrosion rate, rho) of a design at the process mean (no build or bar noise)."""
        s, f, g = self.calphad(c)
        q = self.q(a, g, route)
        rho = self.rho(P, v, f, g, q, machine, route)
        obj = self.U(s, rho) - self.lam * burden(c)
        return obj, self.ln_corr(c, rho), rho

    def score(self, c, a, P, v, route="us", machine="ih"):
        """What a claimed alloy is worth: its true objective if it truly passes corrosion, else 0."""
        obj, lnr, _ = self.design(c, a, P, v, route, machine)
        return float(obj) if float(lnr) <= self.ln_rmax else 0.0

    # ---------------------------------------------------------------- noisy measurements
    def measure_q(self, q_true, rng):
        return float(q_true + rng.normal(0, SIG_Q))

    def measure_U(self, s, rho_actual, rng, site="own", epoch=0):
        return float(self.U(s, rho_actual) + rng.normal(0, SIG_BAR) + self.site_U.get(site, 0.0)
                     + self.epoch_U.get(epoch, 0.0))

    @staticmethod
    def film_factor(rng):
        """Coupon-specific film-growth amplitude: early mass-loss rates run high, decaying with time."""
        return float(rng.uniform(0.3, 1.7))

    @staticmethod
    def imm_reading(lnr_true, day, amp, rng):
        """The day-d estimate of ln r: the coupon's film factor (minus the lab's mean, which it divides out) plus
        reading noise. Spread shrinks with d; day 30 is the result that counts."""
        film = math.log(1 + amp * math.exp(-day / 4.0)) - math.log(1 + 1.0 * math.exp(-day / 4.0))
        noise_sd = math.sqrt(max(IMM_SIG[day] ** 2 - 0.1 ** 2 * math.exp(-day / 4.0), 0.03 ** 2))
        return float(lnr_true + film + rng.normal(0, noise_sd))


# ---------------------------------------------------------------- optimum and screen ceiling
def optimum(truth: Truth, n=200_000, seed=0, constrained=True, comp_filter=None):
    """Best design by random search plus coordinate refinement (in-house printer, ultrasonic powder).

    Returns (value, design[7]). constrained: corrosion must pass. comp_filter(c, s, f, g) -> bool mask, e.g. the
    CALPHAD screen, gives the screen's ceiling."""
    rng = np.random.default_rng(seed)
    nc = truth.ncomp
    X = rng.random((n, nc + 3))

    def val(X):
        c, a, P, v = X[:, :nc], X[:, nc], X[:, nc + 1], X[:, nc + 2]
        obj, lnr, _ = truth.design(c, a, P, v)
        ok = np.ones(len(X), bool)
        if constrained:
            ok &= lnr <= truth.ln_rmax
        if comp_filter is not None:
            ok &= comp_filter(c, *truth.calphad(c))
        return np.where(ok, obj, -9.0)

    y = val(X)
    Xt = X[np.argsort(y)[-60:]].copy()  # coordinate search from the 60 best, all at once
    yt = val(Xt)
    step = 0.05
    while step > 1e-4:
        improved = False
        for j in range(Xt.shape[1]):
            for sgn in (1, -1):
                Xn = Xt.copy()
                Xn[:, j] = np.clip(Xn[:, j] + sgn * step, 0, 1)
                yn = val(Xn)
                better = yn > yt + 1e-12
                if better.any():
                    Xt[better], yt[better], improved = Xn[better], yn[better], True
        if not improved:
            step /= 2
    k = int(np.argmax(yt))
    best_y, best_x = yt[k], Xt[k]
    return float(best_y), best_x


def screen_filter(f_safe=0.25):
    """Tiered screening's CALPHAD criterion: predicted crack-free (freezing-range index <= f_safe)."""
    return lambda c, s, f, g: f <= f_safe


# ---------------------------------------------------------------- stretch: three alloy families in one space
class CrossTruth(Truth):
    """Stretch: one composition space spanning three families whose boundaries blur.

    Composition (6 dims, all on [0, 1]): Zn+Mg, Cu, Zr, Sc, Si, extra Mg. The three families are corners of it:
    7xxx-like (Zn+Mg+Cu; crack-prone, rescued by Zr as in the core truth), Al-Si (Si narrows the freezing range and
    feeds cracks with eutectic, so it prints; modest strength), and Al-Mg-Sc (Mg solid solution plus Al3Sc; strong and
    printable but Sc carries the heaviest mineral burden). The best alloys sit between the families: a 7xxx base with
    some Si to heal cracks, or Mg-rich 7xxx with a little Sc. A campaign that searches each family's corner on its own
    can't reach them.
    """

    ncomp = 6
    WC = np.array([0.55, 1.7, -0.5, -0.3, -0.4, 0.3])

    @staticmethod
    def calphad(c):
        c = np.asarray(c, float)
        c1, c2, c3, c4, c5, c6 = (c[..., i] for i in range(6))
        s = (1 - np.exp(-(1.4 * c1 + 0.9 * c2 + 1.5 * c1 * c2 + 0.5 * c6 + 0.8 * c1 * c6)) + 0.1 * c3 + 0.3 * c4
             + 0.12 * c5 + 0.25 * c4 * c6) / 1.3
        f = (0.65 * c1 + 0.55 * c2 - 0.25 * c1 * c2 + 0.05 * c3 + 0.03 * c4 + 0.25 * c6) * (1 - 0.55 * c5)
        g = (0.6 * np.clip(c3, 0, None) ** 1.5 + 0.9 * np.clip(c4, 0, None) ** 1.2) * (1 + 0.2 * c1) / 1.8
        return s, f, g

    def rho(self, P, v, f, g, q, machine="ih", route="us", site="own", epoch=0, si=None):
        r = super().rho(P, v, f, g, q, machine, route, site, epoch)
        return r

    @classmethod
    def ln_corr(cls, c, rho):
        c = np.asarray(c, float)
        return LNR0 + c[..., :6] @ cls.WC + CORR_POR * (1 - np.asarray(rho, float))

    @staticmethod
    def burden_x(c):
        c = np.asarray(c, float)
        return 0.15 * c[..., 0] + 0.1 * c[..., 1] + 0.2 * c[..., 2] + 1.0 * c[..., 3] + 0.05 * c[..., 4] + 0.08 * c[..., 5]

    def design(self, c, a, P, v, route="us", machine="ih"):
        s, f, g = self.calphad(c)
        q = self.q(a, g, route)
        rho = self.rho(P, v, f, g, q, machine, route)
        obj = self.U(s, rho) - self.lam * self.burden_x(c)
        return obj, self.ln_corr(c, rho), rho


FAMILIES = {  # the corner each family's own campaign searches (dims it may vary; the rest held at 0)
    "7xxx": [0, 1, 2, 3],
    "AlSi": [4, 5, 2],
    "AlMgSc": [5, 3, 2],
}
