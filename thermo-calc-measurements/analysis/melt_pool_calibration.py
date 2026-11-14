#!/usr/bin/env python3
"""Single-track cross-sections -> calibrated absorptivity, regime labels and a parity check
against the Thermo-Calc AM Module (or any other melt-pool model).

Model: the Eagar-Tsai solution for a Gaussian surface heat source moving over a semi-infinite
body with constant properties (conduction only; no Marangoni flow, keyhole or evaporation):

    T - T0 = eta P / (pi rho c sqrt(4 pi alpha)) *
             int_0^inf t^-1/2 / (2 alpha t + sigma^2) *
             exp(-((x + v t)^2 + y^2) / (4 alpha t + 2 sigma^2) - z^2 / (4 alpha t)) dt

with sigma = r0 / 2 for a 1/e^2 beam radius r0. Substituting t = s^2 removes the t^-1/2
singularity. Because T - T0 is linear in eta*P, the field is computed once per track as
Theta = (T - T0) / (eta P), and the melt pool for any eta is the Theta = (T_l - T0)/(eta P)
contour. Fitting eta is then cheap.

It also reports, per track:
- measured depth/width ratio and a regime label (thresholds are arguments; a conduction pool from
  a surface source is at most about semicircular, D/W ~ 0.5);
- the keyhole number Ke = eta P / ((T_l - T0) pi rho c sqrt(alpha v r0^3)) of Gan et al. (2021),
  as used in this repo's keyhole comparison (PR #249). Thresholds on Ke must be calibrated on our
  own tracks; see that PR.

Use it for: heat-source calibration of the AM Module from our own cross-sections (the AM Module
does its own calibration internally; this gives an open, inspectable equivalent), and the parity
plot of measured vs. predicted width and depth.

CLI:
    python melt_pool_calibration.py tracks.csv --material alsi10mg.json \
        [--fit-on conduction|all] [--am-module am_module.csv] [--out prefix]
    python melt_pool_calibration.py --demo

tracks.csv columns: track_id, P_W, v_mm_s, width_um, depth_um  (depth below the substrate surface)
material.json keys: k_W_mK, rho_kg_m3, cp_J_kgK, T_liquidus_K, T0_K, r0_um
am_module.csv (optional): track_id, width_um, depth_um (predicted at the same P, v)

Requires numpy and scipy.
"""
from __future__ import annotations

import argparse
import csv
import json
import math

import numpy as np
from scipy.optimize import minimize_scalar, brentq


# ----------------------------------------------------------------------------- model

class TrackField:
    """Theta = (T - T0)/(eta P) on the surface (x, y) and on the centre plane (x, z)."""

    def __init__(self, v_m_s, r0_m, k, rho, cp, x_range=(-2.0e-3, 0.3e-3), dx=4e-6,
                 ymax=400e-6, dy=2e-6, t_max=None, n_s=700):
        self.v, self.r0 = v_m_s, r0_m
        alpha = k / (rho * cp)
        sigma = r0_m / 2.0
        self.alpha, self.rho, self.cp = alpha, rho, cp
        if t_max is None:
            # long enough for the pool tail (x down to x_range[0]) and for diffusion
            t_max = max(3.0 * abs(x_range[0]) / v_m_s, 50.0 * sigma ** 2 / alpha)
        # s grid: dense near 0, where the kernel varies fastest
        s = np.concatenate([[0.0], np.geomspace(1e-6 * math.sqrt(t_max), math.sqrt(t_max), n_s)])
        self.x = np.arange(x_range[0], x_range[1] + dx / 2, dx)
        self.y = np.arange(0.0, ymax + dy / 2, dy)
        pref = 1.0 / (math.pi * rho * cp * math.sqrt(4 * math.pi * alpha))
        w = np.diff(s)                                  # trapezoid weights on the s grid
        ws = np.zeros_like(s)
        ws[:-1] += w / 2
        ws[1:] += w / 2
        s2 = s ** 2
        denom = 2 * alpha * s2 + sigma ** 2            # (2 alpha t + sigma^2)
        lat = 4 * alpha * s2 + 2 * sigma ** 2          # (4 alpha t + 2 sigma^2)
        X = self.x[:, None, None]
        Y = self.y[None, :, None]
        S2 = s2[None, None, :]
        base = 2.0 / denom[None, None, :]              # t^-1/2 dt = 2 ds
        # surface (z = 0)
        E = np.exp(-((X + self.v * S2) ** 2 + Y ** 2) / lat[None, None, :])
        self.theta_xy = pref * np.sum(base * E * ws[None, None, :], axis=2)
        # centre plane (y = 0), z replaces y
        with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
            Z2 = (self.y ** 2)[None, :, None]
            ez = np.where(S2 > 0, np.exp(-Z2 / (4 * alpha * np.where(S2 > 0, S2, 1.0))), 0.0)
            ez[:, 0, :] = 1.0 * (S2[:, 0, :] >= 0)     # z = 0 row: no z-attenuation
        E2 = np.exp(-((X + self.v * S2) ** 2) / lat[None, None, :]) * ez
        self.theta_xz = pref * np.sum(base * E2 * ws[None, None, :], axis=2)

    @staticmethod
    def _extent(theta, coord, level):
        """max over x of the coordinate where theta first drops below level (linear interp)."""
        best = 0.0
        for row in theta:
            if row[0] < level:
                continue
            idx = np.argmax(row < level)
            if idx == 0:                               # never drops below inside the grid
                return float("inf")
            r0, r1 = row[idx - 1], row[idx]
            c = coord[idx - 1] + (r0 - level) * (coord[idx] - coord[idx - 1]) / (r0 - r1)
            best = max(best, c)
        return best

    def pool(self, eta, P, dT_melt):
        level = dT_melt / (eta * P)
        half_w = self._extent(self.theta_xy, self.y, level)
        depth = self._extent(self.theta_xz, self.y, level)
        return 2 * half_w, depth


def keyhole_number(eta, P, v, r0, k, rho, cp, dT_melt):
    """Gan et al. (2021): Ke = eta P / ((T_l - T0) pi rho c sqrt(alpha v r0^3))."""
    alpha = k / (rho * cp)
    return eta * P / (dT_melt * math.pi * rho * cp * math.sqrt(alpha * v * r0 ** 3))


def regime(d_over_w, conduction_max=0.5, keyhole_min=0.75):
    if d_over_w < conduction_max:
        return "conduction"
    if d_over_w >= keyhole_min:
        return "keyhole"
    return "transition"


# ----------------------------------------------------------------------------- fitting

def fit_eta(tracks, mat, fit_on="conduction", bounds=(0.05, 0.95), thresholds=(0.5, 0.75)):
    dT = mat["T_liquidus_K"] - mat["T0_K"]
    fields = {}
    for tr in tracks:
        key = tr["v_mm_s"]
        if key not in fields:
            fields[key] = TrackField(tr["v_mm_s"] * 1e-3, mat["r0_um"] * 1e-6,
                                     mat["k_W_mK"], mat["rho_kg_m3"], mat["cp_J_kgK"])
        tr["_field"] = fields[key]
        tr["d_over_w"] = tr["depth_um"] / tr["width_um"]
        tr["regime_measured"] = regime(tr["d_over_w"], *thresholds)
    use = [t for t in tracks if fit_on == "all" or t["regime_measured"] == "conduction"]
    if not use:
        raise ValueError("no tracks to fit on (try --fit-on all)")

    def loss(eta):
        err = 0.0
        for t in use:
            W, D = t["_field"].pool(eta, t["P_W"], dT)
            err += ((W * 1e6 - t["width_um"]) / t["width_um"]) ** 2
            err += ((D * 1e6 - t["depth_um"]) / t["depth_um"]) ** 2
        return err / (2 * len(use))

    res = minimize_scalar(loss, bounds=bounds, method="bounded", options={"xatol": 1e-4})
    eta = float(res.x)
    out = []
    for t in tracks:
        W, D = t["_field"].pool(eta, t["P_W"], dT)

        def wres(e, t=t):
            return t["_field"].pool(e, t["P_W"], dT)[0] * 1e6 - t["width_um"]
        try:
            eta_w = brentq(wres, bounds[0], bounds[1], xtol=1e-4)
        except ValueError:
            eta_w = float("nan")
        Ke = keyhole_number(eta, t["P_W"], t["v_mm_s"] * 1e-3, mat["r0_um"] * 1e-6,
                            mat["k_W_mK"], mat["rho_kg_m3"], mat["cp_J_kgK"], dT)
        out.append({
            "track_id": t["track_id"], "P_W": t["P_W"], "v_mm_s": t["v_mm_s"],
            "width_um": t["width_um"], "depth_um": t["depth_um"],
            "d_over_w": round(t["d_over_w"], 3), "regime_measured": t["regime_measured"],
            "used_in_fit": t in use,
            "width_model_um": round(W * 1e6, 1), "depth_model_um": round(D * 1e6, 1),
            "eta_from_width_alone": round(eta_w, 3) if eta_w == eta_w else None,
            "Ke_at_fitted_eta": round(Ke, 2),
        })
    rms = math.sqrt(res.fun)
    return eta, rms, out


def compare_am_module(results, am_rows):
    am = {r["track_id"]: r for r in am_rows}
    pairs = [(r, am[r["track_id"]]) for r in results if r["track_id"] in am]
    if not pairs:
        return None
    dw = np.array([float(a["width_um"]) - r["width_um"] for r, a in pairs])
    dd = np.array([float(a["depth_um"]) - r["depth_um"] for r, a in pairs])
    return {"n": len(pairs),
            "width_bias_um": float(dw.mean()), "width_rmse_um": float(np.sqrt((dw ** 2).mean())),
            "depth_bias_um": float(dd.mean()), "depth_rmse_um": float(np.sqrt((dd ** 2).mean()))}


# ----------------------------------------------------------------------------- I/O, demo, CLI

def read_tracks(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    return [{"track_id": r["track_id"], "P_W": float(r["P_W"]), "v_mm_s": float(r["v_mm_s"]),
             "width_um": float(r["width_um"]), "depth_um": float(r["depth_um"])} for r in rows]


DEMO_MATERIAL = {   # illustrative AlSi10Mg-like inputs, as used in PR #249 (not measured values)
    "k_W_mK": 110.0, "rho_kg_m3": 2650.0, "cp_J_kgK": 1040.0,
    "T_liquidus_K": 867.0, "T0_K": 423.15, "r0_um": 40.0,
}


def demo(eta_true=0.31, seed=1):
    rng = np.random.default_rng(seed)
    mat = DEMO_MATERIAL
    dT = mat["T_liquidus_K"] - mat["T0_K"]
    tracks = []
    for i, (P, v) in enumerate([(150, 600), (200, 800), (250, 1000), (300, 1200), (200, 1400), (350, 1600)]):
        f = TrackField(v * 1e-3, mat["r0_um"] * 1e-6, mat["k_W_mK"], mat["rho_kg_m3"], mat["cp_J_kgK"])
        W, D = f.pool(eta_true, P, dT)
        tracks.append({"track_id": f"T{i+1}", "P_W": P, "v_mm_s": v,
                       "width_um": W * 1e6 * (1 + 0.03 * rng.standard_normal()),
                       "depth_um": D * 1e6 * (1 + 0.05 * rng.standard_normal())})
    eta, rms, out = fit_eta(tracks, mat, fit_on="all")
    print(json.dumps({"eta_true": eta_true, "eta_fit": round(eta, 4), "rms_rel_error": round(rms, 4),
                      "tracks": out}, indent=2))
    return eta


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tracks", nargs="?")
    p.add_argument("--material")
    p.add_argument("--fit-on", choices=["conduction", "all"], default="conduction")
    p.add_argument("--thresholds", type=float, nargs=2, default=(0.5, 0.75),
                   help="D/W limits: conduction below the first, keyhole at or above the second")
    p.add_argument("--am-module", help="CSV of AM Module predictions (track_id, width_um, depth_um)")
    p.add_argument("--out")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        demo()
        return
    if not (a.tracks and a.material):
        p.error("tracks and --material are required (or --demo)")
    mat = json.load(open(a.material))
    tracks = read_tracks(a.tracks)
    eta, rms, out = fit_eta(tracks, mat, fit_on=a.fit_on, thresholds=tuple(a.thresholds))
    summary = {"eta_fit": eta, "rms_rel_error": rms, "fit_on": a.fit_on, "material": mat}
    if a.am_module:
        with open(a.am_module, newline="") as fh:
            summary["am_module_vs_measured"] = compare_am_module(out, list(csv.DictReader(fh)))
    print(json.dumps(summary, indent=2))
    if a.out:
        with open(a.out + "_tracks.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
        with open(a.out + "_summary.json", "w") as fh:
            json.dump(summary, fh, indent=2)


if __name__ == "__main__":
    main()
