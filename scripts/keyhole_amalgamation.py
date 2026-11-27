"""Amalgamate the open keyhole models with the laserbeamFoam runs and score the result against the AM module (#235).

The keyhole write-up (arroyave-orchid-tools/keyhole-alternatives/README.md) recommended a combination of open
methods in place of the Thermo-Calc AM module, each where it is strongest:

* eagar-tsai (#238) with the AM module's own lack-of-fusion tests, D/t <= 1 and Dh/t <= 1;
* the keyhole number Ke of Gan et al. 2021 and their depth law Dk = 0.4 (Ke - 1.4) r0 for the keyhole;
* an open thermal-fluid code (laserbeamFoam) for what no cheap law gives: the keyhole's width, the liquid
  under and around it, keyhole-mode pool width and length, and the absorptivity.

This script puts them together and compares the result with the AM module at every point where we have an
AM-module number: the classes on both in-house maps, and the two 3D melt-pool renders.

The amalgamated classifier at a grid point (P, v) and absorptivity A:
1. keyhole if Gan's keyhole depth Dk satisfies the AM module's keyhole test Wk / Dk <= 0.7, with the
   keyhole width Wk = c_w * 2 r0 and c_w taken from laserbeamFoam's keyhole at the AM module's absorbed power
   (so Ke >= 1.4 + 2 c_w / (0.4 * 0.7));
2. otherwise eagar-tsai's pool at the same A with the AM module's D/t and Dh/t tests (lof, lof_hatch, none).

Usage (from the repo root, after scripts/keyhole_cfd_laserbeamfoam.py post has written the CFD summaries):

    python scripts/keyhole_amalgamation.py --cfd-dir arroyave-orchid-tools/keyhole-alternatives/cfd \
        --out arroyave-orchid-tools/keyhole-alternatives/cfd
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from keyhole_open_models import (  # noqa: E402
    AM_DIR, KE_OFFSET, KE_SLOPE, MATERIALS, WK_DK_AM, gan_depth, keyhole_number,
)

REPO = pathlib.Path(__file__).resolve().parent.parent
ET_SUMMARY = AM_DIR / "summary.json"
LAYER_UM = 30.0
HATCH_UM = {"alsi10mg": 130.0, "blend": 100.0}

INK, INK2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e1"
CLASS_COLOURS = {"keyhole": "#2a78d6", "lof": "#eb6834", "lof_hatch": "#1baf7a", "none": "#b9b8b2"}
CLASS_LABELS = {"keyhole": "keyhole", "lof": "lack of fusion", "lof_hatch": "lack of fusion at hatch",
                "none": "no defect"}


def ke_threshold(c_w: float) -> float:
    """Ke at which Gan's keyhole depth makes Wk / Dk = 0.7 for Wk = c_w * 2 r0."""
    return KE_OFFSET + 2.0 * c_w / (KE_SLOPE * WK_DK_AM)


def et_at(et: pd.DataFrame, A: float) -> pd.DataFrame:
    """eagar-tsai's pool at each grid point for absorptivity A, interpolated linearly between the grid's A values."""
    As = np.sort(et["A"].unique())
    if np.any(np.isclose(As, A, atol=5e-4)):
        return et[np.isclose(et["A"], A, atol=5e-4)].reset_index(drop=True)
    lo, hi = As[As < A].max(), As[As > A].min()
    a = et[np.isclose(et["A"], lo)].reset_index(drop=True)
    b = et[np.isclose(et["A"], hi)].reset_index(drop=True)
    w = (A - lo) / (hi - lo)
    outp = a.copy()
    for col in ["W_um", "D_um", "L_um", "Dh_um", "T_peak_K"]:
        outp[col] = (1 - w) * a[col] + w * b[col]
    outp["A"] = A
    return outp


def lof_class(D_um: float, Dh_um: float) -> str:
    if D_um <= LAYER_UM:
        return "lof"
    if Dh_um <= LAYER_UM:
        return "lof_hatch"
    return "none"


def load_cfd(cfd_dir: pathlib.Path) -> dict:
    runs = {}
    for f in sorted(cfd_dir.glob("*-summary.json")):
        s = json.loads(f.read_text())
        if "run" not in s:
            continue
        pool = pd.read_csv(cfd_dir / f"{s['run']}-pool-vs-time.csv")
        s["pool"] = pool
        runs[s["run"]] = s
    return runs


def cfd_late(run: dict, frac: float = 0.5) -> dict:
    """Mean of each pool and keyhole measure over the writes in the last (1 - frac) of the run."""
    d = run["pool"]
    late = d[d["t_ms"] >= frac * d["t_ms"].max()]
    keys = ["T_max_K", "keyhole_depth_um", "keyhole_width_surface_um", "keyhole_width_q1_um", "keyhole_width_mid_um",
            "pool_depth_um", "pool_width_um", "pool_length_um"]
    outp = {k: float(late[k].mean()) for k in keys if k in late}
    outp.update({f"{k}_last": float(d[k].iloc[-1]) for k in keys if k in d})
    outp.update({f"{k}_max": float(late[k].max()) for k in keys if k in late})
    for k in ["pool_depth_solidus_um", "pool_width_solidus_um", "pool_length_solidus_um"]:
        if k in late:
            outp[k] = float(late[k].mean())
    outp["t_end_ms"] = float(d["t_ms"].max())
    outp["A_eff"] = run.get("A_eff_mean_second_half")
    outp["pool_length_still_growing"] = bool(len(d) >= 3 and d["pool_length_um"].iloc[-1]
                                             > 1.05 * d["pool_length_um"].iloc[-3])
    return outp


# The points where laserbeamFoam ran. Two are the AM module's melt-pool renders; the 350 W one is the next grid point
# the AlSi10Mg map calls keyhole at 0.9 m/s (its boundary there is ~293 W), so the two AlSi10Mg runs bracket it.
POINTS = [
    {"key": "alsi10mg", "alloy": "alsi10mg", "P": 250.0, "v": 0.9, "am_class": "none",
     "am": {"peak_T_K": 3044.0}, "runs": ["alsi10mg-fresnel", "alsi10mg-matchedA"]},
    {"key": "alsi10mg_350W", "alloy": "alsi10mg", "P": 350.0, "v": 0.9, "am_class": "keyhole", "am": {},
     "runs": ["alsi10mg-350W-matchedA"]},
    {"key": "blend", "alloy": "blend", "P": 375.0, "v": 0.4, "am_class": "keyhole",
     "am": {"peak_T_K": 3119.15, "pool_depth_um": 349.0, "pool_width_um": 462.0, "pool_length_um": 1470.0},
     "runs": ["blend-fresnel", "blend-fresnel-rho65", "blend-matchedA", "blend-matchedA-25um"]},
]
RUN_LABELS = {
    "fresnel": "laserbeamFoam, own Fresnel absorptivity (40 µΩ cm)",
    "rho65": "laserbeamFoam, own Fresnel absorptivity (65 µΩ cm, near-boiling liquid)",
    "matchedA": "laserbeamFoam, absorbed power fixed at the AM module's A·P",
}


def run_label(run_name: str) -> str:
    kind = "matchedA" if "matchedA" in run_name else ("rho65" if "rho65" in run_name else "fresnel")
    label = RUN_LABELS[kind]
    if run_name.endswith("25um"):
        label += " (25 µm mesh)"
    return label


def cfd_class(Dk: float, Wk: float, r0_um: float) -> str:
    """The AM module's keyhole test applied to a laserbeamFoam keyhole (Wk across the track at a quarter depth)."""
    if Dk < 0.5 * r0_um:
        return "no keyhole (surface dimple)"
    ratio = Wk / Dk
    return f"keyhole by the AM test (Wk/Dk {ratio:.2f})" if ratio <= WK_DK_AM else f"no keyhole by the AM test (Wk/Dk {ratio:.2f})"


def et_point(m: dict, P: float, v: float, q: float) -> pd.Series | None:
    """eagar-tsai's pool at speed v for absorbed power q (its field depends on A*P only): nearest grid A*P."""
    et = pd.read_csv(AM_DIR / f"{m['slug']}-eagar-tsai-grid-liquidus-{m['T_l']:.0f}K.csv")
    et = et[np.isclose(et["speed_mm_s"], v * 1000)].copy()
    if et.empty:
        return None
    et["q"] = et["A"] * et["power_W"]
    return et.iloc[(et["q"] - q).abs().argsort().iloc[0]]


def render_table(cfd: dict) -> pd.DataFrame:
    et_sum = json.loads(ET_SUMMARY.read_text())
    rows = []
    for pt in POINTS:
        m = MATERIALS[pt["alloy"]]
        P, v, A = pt["P"], pt["v"], m["A"]
        r0_um = m["r0"] * 1e6
        base = {"point": pt["key"], "P_W": P, "v_m_s": v}
        rows.append({**base, "method": "AM module (Thermo-Calc)", "A": A, **pt["am"],
                     "class": {"none": "no defect", "keyhole": "keyhole"}[pt["am_class"]] + " (its map)"})
        if pt["key"] in ("alsi10mg", "blend"):
            slug = "AlSi10Mg, liquidus 867 K" if pt["alloy"] == "alsi10mg" else "blend, liquidus 1019 K"
            etm = et_sum[m["slug"]]["variants"][slug]["meltpool_at_A_inferred"]
            etm = {"D_um": etm["D_um"], "W_um": etm["W_um"], "L_um": etm["L_um"], "T_peak_K": etm["T_peak_K"]}
        else:
            e = et_point(m, P, v, A * P)
            etm = {"D_um": e["D_um"], "W_um": e["W_um"], "L_um": e["L_um"], "T_peak_K": e["T_peak_K"]}
        rows.append({**base, "method": "eagar-tsai at the AM module's A", "A": A, "pool_depth_um": etm["D_um"],
                     "pool_width_um": etm["W_um"], "pool_length_um": etm["L_um"], "peak_T_K": etm["T_peak_K"],
                     "class": "keyhole (its W/D ≤ 2.5 test)" if etm["W_um"] / etm["D_um"] <= 2.5 else "-"})
        Ke = float(keyhole_number(P, v, m))
        Dk = float(gan_depth(Ke, m["r0"]) * 1e6)
        rows.append({**base, "method": "Gan et al. depth law at the AM module's A", "A": A, "Ke": Ke,
                     "keyhole_depth_um": Dk,
                     "class": f"keyhole by the AM test if Wk = 2r0 (Wk/Dk {2 * r0_um / Dk:.2f})"
                     if Dk > 0 and 2 * r0_um / Dk <= WK_DK_AM else "no keyhole by the AM test if Wk = 2r0"})
        for run_name in pt["runs"]:
            if run_name not in cfd:
                continue
            late = cfd_late(cfd[run_name])
            A_r = late["A_eff"]
            if "matchedA" not in run_name and A_r:
                # the cheap models at this run's own absorbed power, like for like
                e = et_point(m, P, v, A_r * P)
                if e is not None:
                    rows.append({**base, "method": f"eagar-tsai at {run_name}'s absorbed power", "A": A_r,
                                 "pool_depth_um": e["D_um"], "pool_width_um": e["W_um"], "pool_length_um": e["L_um"],
                                 "peak_T_K": e["T_peak_K"], "class": f"(grid point {e['power_W']:.0f} W, A {e['A']:.3g})"})
                Ke_r = float(keyhole_number(P, v, m, A=A_r))
                rows.append({**base, "method": f"Gan et al. depth law at {run_name}'s A", "A": A_r, "Ke": Ke_r,
                             "keyhole_depth_um": float(gan_depth(Ke_r, m["r0"]) * 1e6), "class": ""})
            Wk = late.get("keyhole_width_q1_um", 0.0)
            Dk_c = late.get("keyhole_depth_um", 0.0)
            rows.append({**base, "method": run_label(run_name), "run": run_name, "A": A_r,
                         "keyhole_depth_um": Dk_c, "keyhole_depth_max_um": late.get("keyhole_depth_um_max"),
                         "keyhole_width_um": Wk, "keyhole_width_surface_um": late.get("keyhole_width_surface_um"),
                         "keyhole_width_mid_um": late.get("keyhole_width_mid_um"),
                         "pool_depth_um": late["pool_depth_um"], "pool_width_um": late["pool_width_um"],
                         "pool_length_um": late["pool_length_um"],
                         "pool_depth_solidus_um": late.get("pool_depth_solidus_um"),
                         "pool_width_solidus_um": late.get("pool_width_solidus_um"),
                         "pool_length_solidus_um": late.get("pool_length_solidus_um"),
                         "peak_T_K": late["T_max_K"], "t_end_ms": late["t_end_ms"],
                         "pool_length_last_um": late.get("pool_length_um_last"),
                         "pool_length_still_growing": late["pool_length_still_growing"],
                         "class": cfd_class(Dk_c, Wk, r0_um)})
    return pd.DataFrame(rows)


def cfd_calibration(cfd: dict) -> dict:
    """What the laserbeamFoam keyhole runs (absorbed power fixed at the AM module's) give the cheap laws.

    c_w: the keyhole's width across the track at a quarter of its depth, over the beam's 1/e^2 diameter: the width
    Gan's depth law lacks. (The opening at the plate surface also takes in any shallow dip of the pool surface around
    the keyhole; it and the width at half depth are reported as bounds.)
    Ke_bracket: where the runs at one speed put the AM module's Wk/Dk = 0.7, interpolated in Ke between runs on
    either side of it.
    """
    outp = {}
    for alloy in MATERIALS:
        m = MATERIALS[alloy]
        r0_um = m["r0"] * 1e6
        pts = []
        for pt in POINTS:
            if pt["alloy"] != alloy:
                continue
            for run_name in pt["runs"]:
                if "matchedA" not in run_name or run_name.endswith("25um") or run_name not in cfd:
                    continue
                late = cfd_late(cfd[run_name])
                Dk, Wk = late["keyhole_depth_um"], late["keyhole_width_q1_um"]
                pts.append({"run": run_name, "Ke": float(keyhole_number(pt["P"], pt["v"], m)), "Dk_um": Dk,
                            "Wk_um": Wk, "Wk_surface_um": late["keyhole_width_surface_um"],
                            "Wk_mid_um": late["keyhole_width_mid_um"],
                            "Wk_over_Dk": Wk / Dk if Dk > 0 else float("inf"),
                            "c_w": Wk / (2 * r0_um), "c_w_surface": late["keyhole_width_surface_um"] / (2 * r0_um),
                            "c_w_mid": late["keyhole_width_mid_um"] / (2 * r0_um),
                            "keyhole": bool(Dk >= 0.5 * r0_um)})
        res = {"runs": pts}
        kh = [p_ for p_ in pts if p_["keyhole"]]
        if kh:
            res["c_w"] = float(np.mean([p_["c_w"] for p_ in kh]))
        pts_sorted = sorted(pts, key=lambda p_: p_["Ke"])
        for a, b in zip(pts_sorted, pts_sorted[1:]):
            ra, rb = a["Wk_over_Dk"], b["Wk_over_Dk"]
            if ra > WK_DK_AM >= rb:
                if np.isfinite(ra):
                    res["Ke_bracket"] = float(a["Ke"] + (ra - WK_DK_AM) / (ra - rb) * (b["Ke"] - a["Ke"]))
                else:
                    res["Ke_bracket"] = float(0.5 * (a["Ke"] + b["Ke"]))
                res["Ke_bracket_between"] = [a["Ke"], b["Ke"]]
        outp[alloy] = res
    return outp


def map_scores(cfd: dict) -> tuple[pd.DataFrame, dict]:
    """Classes at every visible AM-module grid point for the amalgamated model and its pieces."""
    rows = []
    summary = {}
    cal = cfd_calibration(cfd)
    for key, m in MATERIALS.items():
        g = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"].reset_index(drop=True)
        et = pd.read_csv(AM_DIR / f"{m['slug']}-eagar-tsai-grid-liquidus-{m['T_l']:.0f}K.csv")
        et = et[et["am_class"] != "hidden"]
        b = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-boundaries.csv").dropna(subset=["P_keyhole_W"])
        ke_fit = float(np.median(keyhole_number(b["P_keyhole_W"].to_numpy(), b["speed_mm_s"].to_numpy() / 1000.0, m)))
        # variants: name -> (A, Ke threshold)
        variants = {
            "eagar-tsai with the AM module's LOF tests, no keyhole test (#238)": (m["A"], np.inf),
            f"Ke threshold fitted to this map's own boundary (Ke {ke_fit:.1f}; not open)": (m["A"], ke_fit),
            "amalgamated: Gan depth law, Wk = 2r0 (no CFD)": (m["A"], ke_threshold(1.0)),
        }
        c = cal.get(key, {})
        if "c_w" in c:
            variants[f"amalgamated: Gan depth law, Wk from laserbeamFoam (c_w {c['c_w']:.2f})"] = (
                m["A"], ke_threshold(c["c_w"]))
        if "Ke_bracket" in c:
            variants[f"amalgamated: Ke threshold from the laserbeamFoam runs that bracket it (Ke {c['Ke_bracket']:.1f})"] = (
                m["A"], c["Ke_bracket"])
        # fully open: laserbeamFoam's own flat-surface absorptivity (its first step, before any dimple) everywhere,
        # for the lack-of-fusion tests and for Ke alike, with the CFD keyhole width
        thr = c.get("Ke_bracket", ke_threshold(c.get("c_w", 1.0)))
        for suffix, rho in (("fresnel", 40), ("fresnel-rho65", 65)):
            # the flat-surface Fresnel absorptivity depends on the optics only (same for both alloys here), so a run on
            # the other alloy stands in when this one has none
            fres = cfd.get(f"{key}-{suffix}") or next(
                (v_ for k_, v_ in cfd.items() if k_.endswith(f"-{suffix}") and v_.get("A_eff_first_step")), None)
            if fres is not None and fres.get("A_eff_first_step"):
                A_f = float(fres["A_eff_first_step"])
                variants[f"fully open: laserbeamFoam's flat-surface A at {rho} µΩ cm ({A_f:.3f})"] = (A_f, thr)
        s = {"grid_points": int(len(g)), "am_classes": g["am_class"].value_counts().to_dict(),
             "Ke_fit_to_map": ke_fit, "cfd_calibration": c, "variants": {}}
        for name, (A, thr) in variants.items():
            etA = et_at(et, A)
            merged = g.merge(etA[["power_W", "speed_mm_s", "W_um", "D_um", "Dh_um"]], on=["power_W", "speed_mm_s"],
                             how="left")
            Ke = keyhole_number(merged["power_W"].to_numpy(), merged["speed_mm_s"].to_numpy() / 1000.0, m, A=A)
            cls = np.where(Ke >= thr, "keyhole",
                           [lof_class(D, Dh) for D, Dh in zip(merged["D_um"], merged["Dh_um"])])
            agree = cls == merged["am_class"].to_numpy()
            kh_am = merged["am_class"].to_numpy() == "keyhole"
            s["variants"][name] = {
                "A": round(float(A), 4), "Ke_threshold": round(float(thr), 2) if np.isfinite(thr) else None,
                "agree_all_classes": int(agree.sum()),
                "agree_keyhole_vs_not": int(((cls == "keyhole") == kh_am).sum()),
                "agree_on_non_keyhole_points": int(agree[~kh_am].sum()), "non_keyhole_points": int((~kh_am).sum()),
                "missed_am_keyhole": int(((cls != "keyhole") & kh_am).sum()),
                "extra_keyhole": int(((cls == "keyhole") & ~kh_am).sum()),
            }
            for (_, gr), cl in zip(merged.iterrows(), cls):
                rows.append({"alloy": key, "variant": name, "power_W": gr["power_W"], "speed_mm_s": gr["speed_mm_s"],
                             "am_class": gr["am_class"], "predicted": cl})
        # how the agreement moves with the keyhole width, at the AM module's absorptivity
        etA = et_at(et, m["A"])
        merged = g.merge(etA[["power_W", "speed_mm_s", "D_um", "Dh_um"]], on=["power_W", "speed_mm_s"], how="left")
        Ke = keyhole_number(merged["power_W"].to_numpy(), merged["speed_mm_s"].to_numpy() / 1000.0, m)
        lof = np.array([lof_class(D, Dh) for D, Dh in zip(merged["D_um"], merged["Dh_um"])])
        s["agreement_vs_c_w"] = {}
        for cw in (0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5):
            cls = np.where(Ke >= ke_threshold(cw), "keyhole", lof)
            s["agreement_vs_c_w"][f"{cw:.2f}"] = int((cls == merged["am_class"].to_numpy()).sum())
        summary[key] = s
    return pd.DataFrame(rows), summary


def plot_maps(classes: pd.DataFrame, summary: dict, out_png: pathlib.Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURFACE)
    for ax, (key, m) in zip(axes, MATERIALS.items()):
        ax.set_facecolor(SURFACE)
        b = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-boundaries.csv")
        bk = b.dropna(subset=["P_keyhole_W"])
        ax.plot(bk["speed_mm_s"] / 1000, bk["P_keyhole_W"], color=INK, lw=2, label="AM module keyhole boundary")
        v = np.linspace(0.3, 2.4, 200)
        names = [n for n in summary[key]["variants"] if n.startswith("amalgamated")]
        styles = [(0, (1.5, 1.5)), (0, (6, 2)), "-"][-len(names):]
        for name, ls in zip(names, styles):
            var = summary[key]["variants"][name]
            P = var["Ke_threshold"] / keyhole_number(1.0, v, m, A=var["A"])
            label = name.replace("amalgamated: ", "amalgamated keyhole line: ").split(" (c_w")[0]
            ax.plot(v, P, color="#eb6834", lw=2, ls=ls, label=label)
        # grid points: fill = AM module class; ring = the CFD-calibrated amalgamated model disagrees
        best = names[-1]
        d = classes[(classes["alloy"] == key) & (classes["variant"] == best)]
        for cl, sub in d.groupby("am_class"):
            ax.scatter(sub["speed_mm_s"] / 1000, sub["power_W"], s=46, color=CLASS_COLOURS[cl], zorder=3,
                       edgecolors=SURFACE, linewidths=1.5, label=f"AM module: {CLASS_LABELS[cl]}")
        bad = d[d["am_class"] != d["predicted"]]
        ax.scatter(bad["speed_mm_s"] / 1000, bad["power_W"], s=150, facecolors="none", edgecolors=INK, linewidths=1.2,
                   zorder=4, label="amalgamated model disagrees")
        for pt in POINTS:
            if pt["alloy"] != key:
                continue
            ax.scatter([pt["v"]], [pt["P"]], marker="*", s=180, color=INK, zorder=5, label="laserbeamFoam runs")
            note = summary.get("cfd_point_classes", {}).get(pt["key"])
            if note:
                ax.annotate(note, xy=(pt["v"], pt["P"]), xytext=(9, -3), textcoords="offset points", fontsize=7,
                            color=INK, zorder=6,
                            bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec=GRID, alpha=0.95))
        ax.set_xlabel("scan speed (m/s)", fontsize=8, color=INK2)
        ax.set_ylabel("power (W)", fontsize=8, color=INK2)
        cw = summary[key]["cfd_calibration"].get("c_w")
        cw_txt = f" (c_w {cw:.2f})" if cw else ""
        ax.set_title(f"{m['label']}: {summary[key]['variants'][best]['agree_all_classes']} of "
                     f"{summary[key]['grid_points']} points agree{cw_txt}", fontsize=9, loc="left", color=INK)
        ax.tick_params(labelsize=7, colors=INK2)
        ax.grid(color=GRID, lw=0.5)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_xlim(0.25, 2.45)
        ax.set_ylim(50, 420)
    h, lab = axes[1].get_legend_handles_labels()
    h0, lab0 = axes[0].get_legend_handles_labels()
    seen = {}
    for hh, ll in list(zip(h0, lab0)) + list(zip(h, lab)):
        key_ = ll.split(" (c_w")[0]
        if key_ not in seen:
            seen[key_] = (hh, ll)
    fig.legend([v_[0] for v_ in seen.values()], [v_[1] for v_ in seen.values()], loc="lower center", ncol=3,
               fontsize=7.5, frameon=False)
    fig.tight_layout(rect=(0, 0.17, 1, 1))
    fig.savefig(out_png, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cfd-dir", type=pathlib.Path, required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    args = ap.parse_args()
    cfd = load_cfd(args.cfd_dir)
    table = render_table(cfd)
    table.to_csv(args.out / "amalgamation-render-points.csv", index=False, float_format="%.4g")
    classes, summary = map_scores(cfd)
    notes = {}
    for pt in POINTS:
        mrows = table[(table["point"] == pt["key"]) & table["method"].str.contains("A·P", regex=False)
                      & ~table["method"].str.contains("25 µm", regex=False)]
        if not mrows.empty:
            r_ = mrows.iloc[0]
            notes[pt["key"]] = (f"laserbeamFoam at AM A·P: {r_['class'].replace(' by the AM test', '')}")
    summary["cfd_point_classes"] = notes
    classes.to_csv(args.out / "amalgamation-map-classes.csv", index=False)
    summary["render_points"] = json.loads(table.to_json(orient="records"))
    (args.out / "amalgamation-summary.json").write_text(json.dumps(summary, indent=2))
    plot_maps(classes, summary, args.out / "amalgamation-maps-vs-am-module.png")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(table.drop(columns=[c for c in ["run"] if c in table]).round(3).to_string())
    for key in MATERIALS:
        print(key, json.dumps({k: v for k, v in summary[key].items() if k != "variants"}))
        for name, var in summary[key]["variants"].items():
            print("   ", name, json.dumps(var))


if __name__ == "__main__":
    main()
