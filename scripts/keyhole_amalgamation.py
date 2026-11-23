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
CFD_RUNS = {"alsi10mg": ("alsi10mg-fresnel", "alsi10mg-matchedA"), "blend": ("blend-fresnel", "blend-matchedA")}
MESH_CHECK = {"blend": "blend-matchedA-25um"}

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
    keys = ["T_max_K", "keyhole_depth_um", "keyhole_width_surface_um", "keyhole_width_mid_um", "pool_depth_um",
            "pool_width_um", "pool_length_um"]
    outp = {k: float(late[k].mean()) for k in keys if k in late}
    outp.update({f"{k}_last": float(d[k].iloc[-1]) for k in keys if k in d})
    outp["t_end_ms"] = float(d["t_ms"].max())
    outp["A_eff"] = run.get("A_eff_mean_second_half")
    outp["pool_length_still_growing"] = bool(len(d) >= 3 and d["pool_length_um"].iloc[-1]
                                             > 1.05 * d["pool_length_um"].iloc[-3])
    return outp


def render_table(cfd: dict) -> pd.DataFrame:
    et_sum = json.loads(ET_SUMMARY.read_text())
    rows = []
    for key, m in MATERIALS.items():
        r = m["render"]
        A = m["A"]
        r0_um = m["r0"] * 1e6
        Ke = float(keyhole_number(r["P"], r["v"], m))
        Dk = float(gan_depth(Ke, m["r0"]) * 1e6)
        am = {"method": "AM module (Thermo-Calc), read off its render", "A": A,
              "peak_T_K": 3044.0 if key == "alsi10mg" else 3119.15}
        if key == "blend":
            am.update(pool_depth_um=r["pool_depth_um"], pool_width_um=2 * r["pool_halfwidth_um"],
                      pool_length_um=r["pool_length_um"])
            am["class_on_map"] = "keyhole (map boundary at 0.4 m/s: ~180 W)"
        else:
            am["class_on_map"] = "no defect"
        rows.append({"alloy": key, **am})
        slug = "AlSi10Mg, liquidus 867 K" if key == "alsi10mg" else "blend, liquidus 1019 K"
        etm = et_sum[m["slug"]]["variants"][slug]["meltpool_at_A_inferred"]
        rows.append({"alloy": key, "method": "eagar-tsai at the AM module's A (#238)", "A": A,
                     "pool_depth_um": etm["D_um"], "pool_width_um": etm["W_um"], "pool_length_um": etm["L_um"],
                     "peak_T_K": etm["T_peak_K"],
                     "class_on_map": "keyhole (W/D ≤ 2.5)" if etm["W_um"] / etm["D_um"] <= 2.5 else "-"})
        rows.append({"alloy": key, "method": "Gan et al. keyhole number and depth law at the AM module's A", "A": A,
                     "Ke": Ke, "keyhole_depth_um": Dk,
                     "class_on_map": "keyhole mode (Ke > 6); Wk/Dk = %.2f with Wk = 2r0" % (2 * r0_um / Dk)})
        for run_name in CFD_RUNS[key] + ((MESH_CHECK[key],) if key in MESH_CHECK else ()):
            if run_name not in cfd:
                continue
            late = cfd_late(cfd[run_name])
            label = {"fresnel": "laserbeamFoam, own Fresnel absorptivity",
                     "matchedA": "laserbeamFoam, absorbed power fixed at the AM module's A·P"}[
                "matchedA" if "matchedA" in run_name else "fresnel"]
            if run_name.endswith("25um"):
                label += " (25 µm mesh)"
            Wk = late.get("keyhole_width_surface_um", 0.0)
            Dk_c = late.get("keyhole_depth_um", 0.0)
            rows.append({"alloy": key, "method": label, "run": run_name, "A": late["A_eff"],
                         "keyhole_depth_um": Dk_c, "keyhole_width_um": Wk,
                         "pool_depth_um": late["pool_depth_um"], "pool_width_um": late["pool_width_um"],
                         "pool_length_um": late["pool_length_um"], "peak_T_K": late["T_max_K"],
                         "t_end_ms": late["t_end_ms"],
                         "pool_length_still_growing": late["pool_length_still_growing"],
                         "class_on_map": ("keyhole by the AM module's test" if Dk_c > 0 and Wk / Dk_c <= WK_DK_AM
                                          else ("keyhole, but Wk/Dk = %.2f > 0.7" % (Wk / Dk_c) if Dk_c > 2 * r0_um / 4
                                                else "no keyhole"))})
    return pd.DataFrame(rows)


def map_scores(cfd: dict) -> tuple[pd.DataFrame, dict]:
    """Classes at every visible AM-module grid point for the amalgamated model and its pieces."""
    rows = []
    summary = {}
    for key, m in MATERIALS.items():
        g = pd.read_csv(AM_DIR / f"{m['slug']}-am-module-grid-points.csv")
        g = g[g["am_class"] != "hidden"].reset_index(drop=True)
        et = pd.read_csv(AM_DIR / f"{m['slug']}-eagar-tsai-grid-liquidus-{m['T_l']:.0f}K.csv")
        et = et[et["am_class"] != "hidden"]
        # the keyhole width ratio c_w from each laserbeamFoam keyhole run at the AM module's absorbed power
        c_ws = {}
        for run_name in (f"{key}-matchedA",):
            if run_name in cfd:
                late = cfd_late(cfd[run_name])
                if late.get("keyhole_depth_um", 0) > 0:
                    c_ws[run_name] = late["keyhole_width_surface_um"] / (2 * m["r0"] * 1e6)
        c_w_all = {**{f"cw_{k}": v for k, v in c_ws.items()}}
        variants = {"amalgamated, Wk = 2r0 (no CFD)": (m["A"], 1.0)}
        for run_name, cw in c_ws.items():
            variants[f"amalgamated, Wk from {run_name} (c_w = {cw:.2f})"] = (m["A"], cw)
        # the same, with laserbeamFoam's own (Fresnel) absorptivity in place of the AM module's
        fres = cfd.get(f"{key}-fresnel")
        if fres is not None and fres.get("A_eff_mean_second_half"):
            A_f = float(fres["A_eff_mean_second_half"])
            cw = next(iter(c_ws.values()), 1.0)
            variants[f"fully open: laserbeamFoam's Fresnel A = {A_f:.3f}, c_w = {cw:.2f}"] = (A_f, cw)
        s = {"grid_points": int(len(g)), "am_classes": g["am_class"].value_counts().to_dict(), **c_w_all,
             "variants": {}}
        for name, (A, cw) in variants.items():
            etA = et_at(et, A)
            merged = g.merge(etA[["power_W", "speed_mm_s", "W_um", "D_um", "Dh_um"]], on=["power_W", "speed_mm_s"],
                             how="left")
            Ke = keyhole_number(merged["power_W"].to_numpy(), merged["speed_mm_s"].to_numpy() / 1000.0, m, A=A)
            thr = ke_threshold(cw)
            cls = np.where(Ke >= thr, "keyhole",
                           [lof_class(D, Dh) for D, Dh in zip(merged["D_um"], merged["Dh_um"])])
            agree = cls == merged["am_class"].to_numpy()
            kh_am = merged["am_class"].to_numpy() == "keyhole"
            s["variants"][name] = {
                "A": round(A, 4), "c_w": round(cw, 3), "Ke_threshold": round(thr, 2),
                "agree_all_classes": int(agree.sum()),
                "agree_keyhole_vs_not": int(((cls == "keyhole") == kh_am).sum()),
                "agree_on_non_keyhole_points": int(agree[~kh_am].sum()), "non_keyhole_points": int((~kh_am).sum()),
                "missed_am_keyhole": int(((cls != "keyhole") & kh_am).sum()),
                "extra_keyhole": int(((cls == "keyhole") & ~kh_am).sum()),
            }
            for (_, gr), cl in zip(merged.iterrows(), cls):
                rows.append({"alloy": key, "variant": name, "power_W": gr["power_W"], "speed_mm_s": gr["speed_mm_s"],
                             "am_class": gr["am_class"], "predicted": cl})
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
        styles = [(0, (1.5, 1.5)), "-"]
        for name, ls in zip(names, styles):
            var = summary[key]["variants"][name]
            P = var["Ke_threshold"] / keyhole_number(1.0, v, m, A=var["A"])
            ax.plot(v, P, color="#eb6834", lw=2, ls=ls, label=name.replace("amalgamated, ", "amalgamated keyhole line, "))
        # grid points: fill = AM module class; ring = the CFD-calibrated amalgamated model disagrees
        best = names[-1]
        d = classes[(classes["alloy"] == key) & (classes["variant"] == best)]
        for cl, sub in d.groupby("am_class"):
            ax.scatter(sub["speed_mm_s"] / 1000, sub["power_W"], s=46, color=CLASS_COLOURS[cl], zorder=3,
                       edgecolors=SURFACE, linewidths=1.5, label=f"AM module: {CLASS_LABELS[cl]}")
        bad = d[d["am_class"] != d["predicted"]]
        ax.scatter(bad["speed_mm_s"] / 1000, bad["power_W"], s=150, facecolors="none", edgecolors=INK, linewidths=1.2,
                   zorder=4, label="amalgamated model disagrees")
        r = m["render"]
        ax.scatter([r["v"]], [r["P"]], marker="*", s=180, color=INK, zorder=5, label="laserbeamFoam runs")
        ax.set_xlabel("scan speed (m/s)", fontsize=8, color=INK2)
        ax.set_ylabel("power (W)", fontsize=8, color=INK2)
        ax.set_title(f"{m['label']}: {summary[key]['variants'][best]['agree_all_classes']} of "
                     f"{summary[key]['grid_points']} points agree", fontsize=9, loc="left", color=INK)
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
