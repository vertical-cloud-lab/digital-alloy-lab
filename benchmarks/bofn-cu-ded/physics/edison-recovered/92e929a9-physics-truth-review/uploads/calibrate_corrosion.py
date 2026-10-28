"""Fit the constants of the corrosion model (physics/truth_phys.py, CAL) to the measurements that exist.

    python physics/calibrate_corrosion.py     # prints the fitted constants and every residual

No study compares these alloy families in one 30-day test against C71500 (physics/edison/same-test-rates.md).
The fit therefore uses the same-test data that do exist, each as its own ratio or level:
  * Lewis and LaQue 1981 (DOI 10.2172/6255887), reproducing Inco and Wrightsville Beach tests: 90-10 against 70-30
    (0.95 over 30 days at 2 m/s, 2.1 to 2.5 over 62 days at 0.15 m/s, 1.5 over a year); aluminum bronze 2.1 times
    70-30 (one year); the late/early rate ratio over 78 days (days 16-78 against days 0-5): Cu 0.7, Cu-20Ni 0.36,
    Cu-30Ni 0.18.
  * Popplewell, Hart and Ford 1973 (via Lewis and LaQue): Cu-10Ni with 0 and 1.5 wt% Fe, 60 days quiescent 3.4%
    NaCl: 38.4 and 12.2 um/y.
  * Yang 2019 (DOI 10.26190/unsworks/21760): 2-hour polarization in stagnant 3.5% NaCl, um/y: Cu 92.4, Cu-9.3Ni 55.0,
    Cu-18.8Ni 44.2, Cu-28.4Ni 29.0, Cu-7Al 37.0 (11.7 um/y per uA/cm2).
  * 70-30 in quiet seawater averages about 2 uA/cm2 (about 25 um/y) over the first month (Lewis and LaQue 62-day:
    28 um/y).
The O2 limit and the beta-prime rate are not measured anywhere (physics/edison/kinetics-constants.md); they are priors.
"""

import math
import sys
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).parents[1]))
torch.set_default_dtype(torch.double)
from physics import truth_phys as TP  # noqa: E402

DAY = 86400.0
ALLOY = {"C71500": (30, 0, 0.675, 0.8), "C70600": (10, 0, 1.4, 0.8), "Cu": (0, 0, 0, 0), "C61400": (0, 7.0, 2.5, 0),
         "Cu10Ni0Fe": (10, 0, 0, 0), "Cu10Ni1.5Fe": (10, 0, 1.5, 0), "Cu20Ni": (20, 0, 0.5, 0), "Cu30Ni": (30, 0, 0.5, 0),
         "Cu9.3Ni": (9.3, 0, 0, 0), "Cu18.8Ni": (18.8, 0, 0, 0), "Cu28.4Ni": (28.4, 0, 0, 0), "Cu7Al": (0, 7, 0, 0)}
NAMES = ["a_al", "a_ni0", "a_ni", "a_fe", "tau", "K_cu", "i_fl"]
X0 = [0.4, 0.54, 0.56, 0.55, 2.5 * DAY, 4.7e7, 2.0]


def terms():
    """Composition features per alloy (fixed); the constants act on them inside each evaluation."""
    return {k: TP.film_features((torch.tensor(wt) / TP.WT_MAX).unsqueeze(0)) for k, wt in ALLOY.items()}


def with_cal(p):
    TP.CAL.update(dict(zip(NAMES, p)))


def avg(k, T, t0, t1):
    f, s = TP.film_terms(None, T[k])
    t = torch.logspace(math.log10(max(t0, 1.0)), math.log10(t1), 200)
    i = TP.current(t, f, s)
    return float(torch.trapezoid(i, t) / (t1 - max(t0, 1.0)))


def residuals(p, T, verbose=False):
    with_cal(p)
    M = {k: avg(k, T, 0, 30 * DAY) for k in T}
    r = []
    def add(name, model, target, w):
        r.append(w * (math.log(model) - math.log(target)))
        if verbose:
            print(f"  {name:40s} model {model:8.3f}  target {target:8.3f}")
    add("90-10 / 70-30, 30 d", M["C70600"] / M["C71500"], 1.4, 1.0)
    add("Cu / 70-30, 30 d", M["Cu"] / M["C71500"], 3.0, 1.0)
    add("Al bronze (C61400) / 70-30, 30 d", M["C61400"] / M["C71500"], 2.1, 1.0)
    add("Cu-10Ni-0Fe / Cu-10Ni-1.5Fe, 60 d", avg("Cu10Ni0Fe", T, 0, 60 * DAY) / avg("Cu10Ni1.5Fe", T, 0, 60 * DAY), 3.1, 1.0)
    for k, tgt in (("Cu", 0.7), ("Cu20Ni", 0.36), ("Cu30Ni", 0.18)):
        add(f"{k} rate days 16-78 / days 0-5", avg(k, T, 16 * DAY, 78 * DAY) / avg(k, T, 0, 5 * DAY), tgt, 0.7)
    for k, um in (("Cu", 92.4), ("Cu9.3Ni", 55.0), ("Cu18.8Ni", 44.2), ("Cu28.4Ni", 29.0), ("Cu7Al", 37.0)):
        f, s = TP.film_terms(None, T[k])
        add(f"{k} i(2 h), uA/cm2", float(TP.current(torch.tensor(7200.0), f, s)[0]), um / 11.7, 0.5)
    add("70-30 mean current over 30 d, uA/cm2", M["C71500"], 2.0, 0.7)
    return np.array(r)


def main():
    T = terms()
    lo = np.log(np.array([0.05, 0.05, 0.05, 0.05, 0.25 * DAY, 1e5, 0.05]))
    hi = np.log(np.array([1.5, 1.5, 1.5, 1.5, 10 * DAY, 1e9, 10.0]))
    def obj(z):
        z = np.clip(z, lo, hi)
        return float((residuals(np.exp(z), T) ** 2).sum())
    best = None
    for start in (X0, [0.3, 0.4, 0.8, 0.8, 4 * DAY, 1e7, 1.0], [0.5, 0.7, 0.4, 0.4, 1 * DAY, 1e8, 3.0]):
        res = minimize(obj, np.log(start), method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-6})
        if best is None or res.fun < best.fun:
            best = res
    p = np.exp(np.clip(best.x, lo, hi))
    print("loss", round(best.fun, 4))
    print({k: (round(v / DAY, 3) if k == "tau" else float(f"{v:.4g}")) for k, v in zip(NAMES, p)}, "(tau in days)")
    residuals(p, T, verbose=True)


if __name__ == "__main__":
    main()
