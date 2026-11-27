"""Open keyhole models vs the Thermo-Calc AM module's keyhole boundary and melt pools (issue #235).

eagar-tsai matched the AM module's lack-of-fusion boundaries but not its keyholing
(arroyave-orchid-tools/eagar-tsai/README.md). This script tests the cheap, published keyhole
models that an open replacement could use:

* the keyhole number of Gan et al. 2021 (Nat. Commun. 12, 2379, doi:10.1038/s41467-021-22704-0),
      Ke = eta P / ((T_l - T0) pi rho c_p sqrt(alpha v r0^3)),
  its keyhole-mode threshold (Ke > 6) and its keyhole-depth law e / r0 = 0.4 (Ke - 1.4);
* the normalized enthalpy of King et al. 2014 (J. Mater. Process. Technol. 214, 2915,
  doi:10.1016/j.jmatprotec.2014.06.005; accepted manuscript at https://www.osti.gov/biblio/1502044),
      dH/h_s = A P / (rho c T_m sqrt(pi D u sigma^3)),  sigma = Gaussian standard deviation,
  with their measured 316L keyhole threshold dH/h_s = 30 +/- 4;
* the Gladush-Smurov keyhole depth as implemented in the open lpbf_map package
  (github.com/ilidio-costa/lpbf_map, GPL-3.0),
      D = A P / (2 pi k T_b) ln((a + alpha / v) / a).

It compares them with three things:

1. the AM module's keyhole boundaries and grid-point classes, digitized from our in-house maps by
   scripts/eagar_tsai_vs_am_module_inhouse.py (arroyave-orchid-tools/eagar-tsai/am-module-inhouse/);
2. the AM module's two 3D melt-pool renders (250 W / 0.9 m/s AlSi10Mg, 375 W / 0.4 m/s blend);
3. the X-ray keyhole depths Gan et al. published as Supplementary Data 1 (Ti-6Al-4V, Al6061, SS316;
   CC BY 4.0). The script downloads that file into a cache directory and checks its sha256; it is
   not committed.

Usage (run from the repo root):

    pip install numpy pandas matplotlib openpyxl
    python scripts/keyhole_open_models.py all --out arroyave-orchid-tools/keyhole-alternatives
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import urllib.request

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
AM_DIR = REPO / "arroyave-orchid-tools" / "eagar-tsai" / "am-module-inhouse"
SOLYAEV_CSV = REPO / "arroyave-orchid-tools" / "eagar-tsai" / "alsi10mg-printability-vs-solyaev2025.csv"

GAN_URL = (
    "https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-22704-0/MediaObjects/"
    "41467_2021_22704_MOESM4_ESM.xlsx"
)
GAN_SHA256 = "b52d9173eb3a6398"  # first 16 hex digits of the file fetched on 2026-11-10

T_BOIL_AL_K = 2743.0  # Al at 1 atm, as in the eagar-tsai comparison

# Thermal properties are the Edison AlSi10Mg values used for the eagar-tsai comparison
# (k 110 W/m/K, rho 2650 kg/m^3, c_p 1040 J/kg/K); the blend has no measured values and gets the same.
# Beam radius r0 is the 1/e^2 radius; A is the absorptivity read off each AM-module render.
MATERIALS = {
    "alsi10mg": {
        "label": "AlSi10Mg, 150 °C plate",
        "slug": "alsi10mg",
        "k": 110.0, "rho": 2650.0, "cp": 1040.0,
        "T_l": 867.0, "T_b": T_BOIL_AL_K, "T0": 423.15,
        "r0": 40e-6, "A": 0.3074,
        "render": {"P": 250.0, "v": 0.9},
    },
    "blend": {
        "label": "BYU blend (Al-24Si), 30 °C plate",
        "slug": "byu-blend",
        "k": 110.0, "rho": 2650.0, "cp": 1040.0,
        "T_l": 1019.3, "T_b": T_BOIL_AL_K, "T0": 303.15,
        "r0": 45e-6, "A": 0.3841,
        "render": {"P": 375.0, "v": 0.4, "pool_depth_um": 349.0, "pool_length_um": 1470.0,
                   "pool_halfwidth_um": 231.0},
    },
}

# Solyaev et al. 2025 (arXiv:2507.23422) AlSi10Mg tracks: keyhole (D/W > 0.75) for P > 220 W and
# v < 0.8 m/s. Beam 2R = 80 um with q ~ exp(-r^2/R^2), i.e. a 1/e^2 radius of sqrt(2) * 40 um;
# A = 0.22 is the study's own conduction-mode fit. Room-temperature plate assumed.
SOLYAEV = {"k": 110.0, "rho": 2650.0, "cp": 1040.0, "T_l": 870.15, "T_b": T_BOIL_AL_K, "T0": 298.15,
           "r0": math.sqrt(2.0) * 40e-6, "A": 0.22, "P_kh": 220.0, "v_kh": 0.8}

KE_KEYHOLE = 6.0  # Gan et al. 2021: keyhole mode for Ke > 6 (transition 1.4-6)
KE_SLOPE, KE_OFFSET = 0.4, 1.4  # e* = e / r0 = 0.4 (Ke - 1.4)
WK_DK_AM = 0.7  # the AM module's keyhole test, Wk / Dk <= 0.7
# Gan's depth law plus a keyhole opening of one beam diameter (Wk = 2 r0) turns Wk/Dk <= 0.7 into a Ke:
KE_WKDK = KE_OFFSET + 2.0 / (KE_SLOPE * WK_DK_AM)
KING_THRESHOLD, KING_SPREAD = 30.0, 4.0  # King et al. 2014, measured for 316L at two beam sizes


# --- the models -----------------------------------------------------------------------------------

def alpha(m: dict) -> float:
    return m["k"] / (m["rho"] * m["cp"])


def keyhole_number(P, v, m: dict, A: float | None = None, T_l: float | None = None):
    """Gan et al. 2021, Eq. 1."""
    A = m["A"] if A is None else A
    T_l = m["T_l"] if T_l is None else T_l
    return A * np.asarray(P) / ((T_l - m["T0"]) * math.pi * m["rho"] * m["cp"]
                                * np.sqrt(alpha(m) * np.asarray(v) * m["r0"] ** 3))


def king_enthalpy(P, v, m: dict, A: float | None = None):
    """King et al. 2014, Eq. 2.6, with sigma = r0 / 2 (their I ~ exp(-r^2 / 2 sigma^2)) and h_s = rho c T_m."""
    A = m["A"] if A is None else A
    sigma = m["r0"] / 2.0
    return A * np.asarray(P) / (m["rho"] * m["cp"] * m["T_l"]
                                * np.sqrt(math.pi * alpha(m) * np.asarray(v) * sigma ** 3))


def boiling_number(P, v, m: dict, A: float | None = None):
    """Ke with the liquidus swapped for the boiling point: A P / ((T_b - T0) pi rho c sqrt(alpha v r0^3))."""
    return keyhole_number(P, v, m, A=A) * (m["T_l"] - m["T0"]) / (m["T_b"] - m["T0"])


def gan_depth(Ke, r0: float):
    """Keyhole depth from e / r0 = 0.4 (Ke - 1.4), zero below Ke = 1.4."""
    return np.clip(KE_SLOPE * (np.asarray(Ke) - KE_OFFSET), 0.0, None) * r0


def gladush_smurov_depth(P, v, m: dict, A: float | None = None):
    """lpbf_map 2.0.1, meltpool._calculate_gladush_smurov_depth (T_b absolute, a = beam radius)."""
    A = m["A"] if A is None else A
    a = m["r0"]
    return A * np.asarray(P) / (2 * math.pi * m["k"] * m["T_b"]) * np.log((a + alpha(m) / np.asarray(v)) / a)


CRITERIA = {
    # name: (label, function(P, v, m) -> value, threshold)
    "gan_ke6": ("Gan Ke > 6 (keyhole mode)", keyhole_number, KE_KEYHOLE),
    "gan_wkdk": (f"Gan depth law + Wk/Dk ≤ 0.7 (Ke > {KE_WKDK:.2f})", keyhole_number, KE_WKDK),
    "king30": ("King ΔH/h_s > 30 (316L, measured)", king_enthalpy, KING_THRESHOLD),
    "gs_2r0": ("Gladush–Smurov depth > 2 r0 (lpbf_map)", lambda P, v, m: gladush_smurov_depth(P, v, m) / m["r0"], 2.0),
}


def boundary_power(fn, threshold: float, v, m: dict):
    """Every criterion is linear in P, so its boundary is threshold / (value per watt)."""
    return threshold / fn(1.0, v, m)


# --- AM-module maps -------------------------------------------------------------------------------

def am_module(out: pathlib.Path) -> dict:
    summary: dict = {}
    rows = []
    for key, m in MATERIALS.items():
        b = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        g = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"].copy()
        v = b["speed_mm_s"].to_numpy() / 1000.0
        P = b["P_keyhole_W"].to_numpy()
        ke = keyhole_number(P, v, m)
        king = king_enthalpy(P, v, m)
        boil = boiling_number(P, v, m)
        for vi, Pi, kei, kgi, bi in zip(v, P, ke, king, boil):
            rows.append({"alloy": key, "speed_m_s": vi, "P_keyhole_am_W": Pi, "Ke": kei, "king_dH_hs": kgi,
                         "boiling_number": bi, "gan_keyhole_depth_um": gan_depth(kei, m["r0"]) * 1e6,
                         "gs_depth_um": gladush_smurov_depth(Pi, vi, m) * 1e6})
        slope = np.polyfit(np.log(v), np.log(P), 1)[0]
        s = {
            "label": m["label"], "A": m["A"], "r0_um": m["r0"] * 1e6, "T_l": m["T_l"], "T0": m["T0"],
            "boundary_speed_m_s": [round(float(v.min()), 3), round(float(v.max()), 3)],
            "boundary_power_W": [round(float(P.min()), 1), round(float(P.max()), 1)],
            "boundary_exponent_P_vs_v": round(float(slope), 3),
            "Ke_along_boundary": _stats(ke),
            "king_along_boundary": _stats(king),
            "boiling_number_along_boundary": _stats(boil),
            "gan_keyhole_depth_on_boundary_um": _stats(gan_depth(ke, m["r0"]) * 1e6),
            "criteria": {},
        }
        # Calibrated: one Ke threshold per map, the median along its boundary.
        ke_cal = float(np.median(ke))
        crit = dict(CRITERIA)
        crit["gan_calibrated"] = (f"Ke > {ke_cal:.1f} (fit to this map)", keyhole_number, ke_cal)
        am_kh = (g["am_class"] == "keyhole").to_numpy()
        for name, (label, fn, thr) in crit.items():
            pb = boundary_power(fn, thr, v, m)
            ratio = pb / P
            pred = fn(g["power_W"].to_numpy(), g["speed_mm_s"].to_numpy() / 1000.0, m) > thr
            s["criteria"][name] = {
                "label": label, "threshold": round(float(thr), 3),
                "boundary_power_over_am": _stats(ratio),
                "rms_power_error_W": round(float(np.sqrt(np.mean((pb - P) ** 2))), 1),
                "grid_points": int(len(g)), "am_keyhole": int(am_kh.sum()),
                "predicted_keyhole": int(pred.sum()),
                "agree": int((pred == am_kh).sum()),
                "missed_am_keyhole": int((~pred & am_kh).sum()),
                "extra_keyhole": int((pred & ~am_kh).sum()),
            }
        # Baseline: eagar-tsai at the same A, from the #238 comparison's grid (W/D <= 2.5, and peak >= boiling).
        et_file = AM_DIR / f"{m['slug']}-eagar-tsai-grid-liquidus-{m['T_l']:.0f}K.csv"
        et = pd.read_csv(et_file)
        et = et[np.isclose(et["A"], m["A"], atol=5e-4) & (et["am_class"] != "hidden")]
        et_am_kh = (et["am_class"] == "keyhole").to_numpy()
        for name, label, pred in [
            ("eagar_tsai_wd2.5", "eagar-tsai W/D ≤ 2.5 (#238)", (et["et_default"] == "keyhole").to_numpy()),
            ("eagar_tsai_boiling", "eagar-tsai peak T ≥ T_b (#238)", et["et_boiling"].astype(bool).to_numpy()),
        ]:
            s["criteria"][name] = {
                "label": label, "grid_points": int(len(et)), "am_keyhole": int(et_am_kh.sum()),
                "predicted_keyhole": int(pred.sum()), "agree": int((pred == et_am_kh).sum()),
                "missed_am_keyhole": int((~pred & et_am_kh).sum()), "extra_keyhole": int((pred & ~et_am_kh).sum()),
            }
        # The render points.
        r = m["render"]
        ke_r = float(keyhole_number(r["P"], r["v"], m))
        s["render"] = {
            "P_W": r["P"], "v_m_s": r["v"], "Ke": round(ke_r, 2),
            "king_dH_hs": round(float(king_enthalpy(r["P"], r["v"], m)), 1),
            "gan_keyhole_depth_um": round(float(gan_depth(ke_r, m["r0"]) * 1e6), 1),
            "gs_depth_um": round(float(gladush_smurov_depth(r["P"], r["v"], m) * 1e6), 1),
        }
        if key == "blend":
            # The same point with the pool edge at the eutectic, and the liquid-free Ke's sensitivity to T_l.
            ke_eu = float(keyhole_number(r["P"], r["v"], m, T_l=850.0))
            s["render"]["Ke_edge_at_eutectic_850K"] = round(ke_eu, 2)
            s["render"]["gan_keyhole_depth_edge_at_eutectic_um"] = round(float(gan_depth(ke_eu, m["r0"]) * 1e6), 1)
            s["render"].update({k: v_ for k, v_ in r.items() if k.endswith("_um")})
            # Absorptivity the depth law needs for the keyhole to reach the AM pool's full depth.
            ke_need = r["pool_depth_um"] / (m["r0"] * 1e6) / KE_SLOPE + KE_OFFSET
            s["render"]["A_for_gan_keyhole_depth_eq_am_pool_depth"] = round(m["A"] * ke_need / ke_r, 3)
        summary[key] = s
    pd.DataFrame(rows).to_csv(out / "am-module-keyhole-boundary-normalized.csv", index=False, float_format="%.5g")
    return summary


def _stats(x) -> dict:
    x = np.asarray(x, dtype=float)
    return {"median": round(float(np.median(x)), 3), "min": round(float(x.min()), 3),
            "max": round(float(x.max()), 3), "n": int(x.size)}


def plot_am(summary: dict, out: pathlib.Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 7.6), constrained_layout=True)
    styles = {
        "gan_ke6": ("#1b7837", "-"), "gan_wkdk": ("#5aae61", "--"), "king30": ("#762a83", "-."),
        "gs_2r0": ("#e08214", ":"), "gan_calibrated": ("#000000", "-"),
    }
    cls_style = {"keyhole": ("#c51b7d", "o"), "none": ("#4d4d4d", "o"), "lof": ("#2166ac", "s"),
                 "lof_hatch": ("#67a9cf", "s")}
    for ax, (key, m) in zip(axes, MATERIALS.items()):
        b = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        g = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"]
        for c, (col, mk) in cls_style.items():
            sel = g[g["am_class"] == c]
            ax.scatter(sel["speed_mm_s"], sel["power_W"], s=34, color=col, marker=mk, alpha=0.85,
                       label=f"AM module grid point: {c}", zorder=3)
        ax.plot(b["speed_mm_s"], b["P_keyhole_W"], color="#c51b7d", lw=4, alpha=0.35,
                label="AM module keyhole boundary (digitized)", zorder=2)
        vv = np.linspace(250, 2500, 200)
        s = summary[key]["criteria"]
        for name, (col, ls) in styles.items():
            fn = keyhole_number if name.startswith("gan") else (king_enthalpy if name == "king30" else
                                                                  (lambda P, v, m: gladush_smurov_depth(P, v, m) / m["r0"]))
            thr = s[name]["threshold"]
            ax.plot(vv, boundary_power(fn, thr, vv / 1000.0, m), color=col, ls=ls, lw=1.8,
                    label=f"{s[name]['label']}: {s[name]['agree']}/{s[name]['grid_points']} points agree")
        lo = boundary_power(king_enthalpy, KING_THRESHOLD - KING_SPREAD, vv / 1000.0, m)
        hi = boundary_power(king_enthalpy, KING_THRESHOLD + KING_SPREAD, vv / 1000.0, m)
        ax.fill_between(vv, lo, hi, color="#762a83", alpha=0.10, lw=0)
        ax.set_xlim(250, 2500)
        ax.set_ylim(50, 500)
        ax.set_xlabel("scan speed (mm/s)")
        ax.set_ylabel("laser power (W)")
        ax.set_title(f"{m['label']}: A = {m['A']:.2f}, 1/e² radius {m['r0'] * 1e6:.0f} µm, "
                     f"T_l {m['T_l']:.0f} K")
        ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, frameon=False)
        ax.grid(alpha=0.25)
    fig.suptitle("Open keyhole criteria drawn on the Thermo-Calc AM module's maps "
                 "(all are linear in P; boundary = threshold / value per watt)", fontsize=11)
    fig.savefig(out / "am-module-maps-with-open-keyhole-criteria.png", dpi=130)
    plt.close(fig)


# --- Gan et al. 2021 X-ray keyhole depths ---------------------------------------------------------

def load_gan(cache: pathlib.Path) -> pd.DataFrame:
    cache.mkdir(parents=True, exist_ok=True)
    f = cache / "gan2021_supplementary_data_1.xlsx"
    if not f.exists():
        req = urllib.request.Request(GAN_URL, headers={"User-Agent": "Mozilla/5.0 (research script)"})
        f.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    if not digest.startswith(GAN_SHA256):
        raise SystemExit(f"unexpected sha256 for {f}: {digest}")
    raw = pd.read_excel(f, header=0)
    raw = raw.rename(columns={raw.columns[0]: "group"})
    raw["group"] = raw["group"].ffill()
    return raw


def gan_check(cache: pathlib.Path, out: pathlib.Path) -> dict:
    d = load_gan(cache)
    d["material"] = d["group"].str.extract(r"^(\w+)")[0].replace({"Ti6": "Ti64"})
    d["T0"] = 293.0
    res = []
    for _, r in d.iterrows():
        m = {"k": r["K"], "rho": r["rho"], "cp": r["cp"], "T_l": r["Tl-T0"] + 293.0, "T0": 293.0,
             "T_b": r["Tv-T0"] + 293.0, "r0": r["r0"], "A": r["eta"]}
        ke = float(keyhole_number(r["P"], r["V"], m))
        res.append({
            "group": r["group"], "material": r["material"], "P_W": r["P"], "v_m_s": r["V"],
            "r0_um": r["r0"] * 1e6, "eta": r["eta"], "Ke": ke,
            "keyhole_depth_measured_um": r["e"] * 1e6,
            "gan_law_um": float(gan_depth(ke, r["r0"]) * 1e6),
            "gladush_smurov_um": float(gladush_smurov_depth(r["P"], r["V"], m) * 1e6),
        })
    t = pd.DataFrame(res)
    t.to_csv(out / "gan2021-xray-keyhole-depths-vs-open-models.csv", index=False, float_format="%.5g")
    # Refit e/r0 = a Ke + b on the rows above Ke = 1.4, to check our Ke against the paper's Eq. 2 (0.4 Ke - 0.56).
    sel = t[t["Ke"] > KE_OFFSET]
    slope, icpt = np.polyfit(sel["Ke"], sel["keyhole_depth_measured_um"] / sel["r0_um"], 1)
    s = {"refit_e_star_vs_Ke": {"slope": round(float(slope), 3), "intercept": round(float(icpt), 3), "n": int(len(sel))}}
    for mat, gg in t.groupby("material", sort=False):
        s[mat] = {"n": int(len(gg)), "P_W": [float(gg.P_W.min()), float(gg.P_W.max())],
                  "v_m_s": [float(gg.v_m_s.min()), float(gg.v_m_s.max())],
                  "measured_um": [round(float(gg.keyhole_depth_measured_um.min())), round(float(gg.keyhole_depth_measured_um.max()))]}
        for col in ("gan_law_um", "gladush_smurov_um"):
            err = gg[col] - gg.keyhole_depth_measured_um
            s[mat][col] = {"MAE_um": round(float(err.abs().mean()), 1), "median_err_um": round(float(err.median()), 1),
                           "max_abs_err_um": round(float(err.abs().max()), 1),
                           "median_rel_err_pct": round(float((err.abs() / gg.keyhole_depth_measured_um).median() * 100), 1),
                           "ratio_pred_over_meas_median": round(float((gg[col] / gg.keyhole_depth_measured_um).median()), 2)}
    return s


def plot_depths(gan_summary: dict, am_summary: dict, out: pathlib.Path) -> None:
    t = pd.read_csv(out / "gan2021-xray-keyhole-depths-vs-open-models.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), constrained_layout=True)
    cols = {"Ti64": "#4575b4", "Al6061": "#d73027", "SS316": "#1a9850"}
    for ax, col, title in [(axes[0], "gan_law_um", "Gan et al. 2021 depth law, e/r0 = 0.4 (Ke − 1.4), fitted to these data"),
                           (axes[1], "gladush_smurov_um", "Gladush–Smurov depth (lpbf_map's formula)")]:
        for mat, gg in t.groupby("material", sort=False):
            st = gan_summary[mat][col]
            ax.scatter(gg.keyhole_depth_measured_um, gg[col], s=26, color=cols.get(mat, "k"), alpha=0.8,
                       label=f"{mat} (n={len(gg)}): MAE {st['MAE_um']:.0f} µm, median ratio {st['ratio_pred_over_meas_median']:.2f}")
        lim = [0, 650]
        ax.plot(lim, lim, color="k", lw=1)
        ax.set_xlim(lim)
        ax.set_ylim(lim)
        ax.set_xlabel("keyhole depth measured by X-ray (µm), Gan et al. 2021 Supplementary Data 1")
        ax.set_ylabel("predicted keyhole depth (µm)")
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.25)
    r = am_summary["blend"]["render"]
    axes[0].axhline(r["pool_depth_um"], color="#984ea3", ls="--", lw=1.2)
    axes[0].text(150, r["pool_depth_um"] - 22,
                 f"AM module blend pool depth, 375 W / 0.4 m/s: {r['pool_depth_um']:.0f} µm; "
                 f"Gan law gives a {r['gan_keyhole_depth_um']:.0f} µm keyhole there", fontsize=7.5, color="#984ea3")
    axes[0].legend(fontsize=7.5, loc="lower right")
    axes[1].legend(fontsize=7.5, loc="upper left")
    fig.suptitle("Two open keyhole-depth models against X-ray keyhole depths "
                 "(each row's own absorptivity, as published)", fontsize=11)
    fig.savefig(out / "open-keyhole-depth-models-vs-xray.png", dpi=130)
    plt.close(fig)


# --- Solyaev et al. 2025 measured AlSi10Mg tracks -------------------------------------------------

def solyaev(out: pathlib.Path) -> dict:
    m = SOLYAEV
    s = {"corner_P_W": m["P_kh"], "corner_v_m_s": m["v_kh"],
         "Ke_at_corner": round(float(keyhole_number(m["P_kh"], m["v_kh"], m)), 2),
         "king_at_corner": round(float(king_enthalpy(m["P_kh"], m["v_kh"], m)), 1),
         "gan_keyhole_depth_at_corner_um": round(float(gan_depth(keyhole_number(m["P_kh"], m["v_kh"], m), m["r0"]) * 1e6), 1),
         "criteria": {}}
    df = pd.read_csv(SOLYAEV_CSV)
    scored = df[df["measured_class"].isin(["keyhole", "stable", "lack_of_fusion"])]
    meas = (scored["measured_class"] == "keyhole").to_numpy()
    for name, (label, fn, thr) in CRITERIA.items():
        pred = fn(scored["power_w"].to_numpy(), scored["velocity_m_s"].to_numpy(), m) > thr
        s["criteria"][name] = {
            "label": label,
            "boundary_power_at_0.8_m_s_W": round(float(boundary_power(fn, thr, 0.8, m)), 1),
            "boundary_power_at_0.335_m_s_W": round(float(boundary_power(fn, thr, 0.335, m)), 1),
            "scored_points": int(len(scored)), "measured_keyhole": int(meas.sum()),
            "predicted_keyhole": int(pred.sum()), "agree": int((pred == meas).sum()),
            "missed": int((~pred & meas).sum()), "extra": int((pred & ~meas).sum()),
        }
    # Baseline: eagar-tsai's own keyhole flag (W/D <= 2.5) on the same points, from the #238 run.
    pred = scored["kh1"].astype(bool).to_numpy()
    s["criteria"]["eagar_tsai_wd2.5"] = {
        "label": "eagar-tsai W/D ≤ 2.5 (#238)", "scored_points": int(len(scored)),
        "measured_keyhole": int(meas.sum()), "predicted_keyhole": int(pred.sum()),
        "agree": int((pred == meas).sum()), "missed": int((~pred & meas).sum()), "extra": int((pred & ~meas).sum()),
    }
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["all"])
    ap.add_argument("--out", type=pathlib.Path, default=REPO / "arroyave-orchid-tools" / "keyhole-alternatives")
    ap.add_argument("--cache", type=pathlib.Path, default=pathlib.Path("/tmp/keyhole-open-models-cache"))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    am = am_module(a.out)
    plot_am(am, a.out)
    gan = gan_check(a.cache, a.out)
    plot_depths(gan, am, a.out)
    sol = solyaev(a.out)
    summary = {
        "constants": {"KE_KEYHOLE": KE_KEYHOLE, "KE_WKDK": round(KE_WKDK, 3), "KING_THRESHOLD": KING_THRESHOLD,
                      "T_BOIL_AL_K": T_BOIL_AL_K},
        "am_module": am, "gan2021_xray_depths": gan, "solyaev2025_alsi10mg": sol,
    }
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
