"""Check ArroyaveLab/eagar-tsai against AlSi10Mg single tracks and Thermo-Calc AM-module results (#235).

Two subcommands:

``published``
    Runs eagar-tsai's printability map for AlSi10Mg with the inputs of an open single-track
    study that calibrated an Eagar-Tsai model on its own tracks: Solyaev et al., "On the
    influence of powder particle size on single-track formation in laser powder bed fusion of
    AlSi10Mg alloy", arXiv:2507.23422 (2025). The script then draws that study's measured
    boundaries on the map:

    * the beam: 2R = 80 um with q ~ exp(-r^2/R^2), so the Gaussian sigma is R/sqrt(2) and
      eagar-tsai's ``beam_diameter`` (= 2 sigma) is 56.6 um;
    * the properties of the liquid (k = 120 W/m/K, rho = 1800 kg/m^3, c = 1800 J/kg/K), with
      the melt-pool edge taken at the solidus (563 C = 836 K), as that study did;
    * A = 0.22, the absorptivity the study fitted for its standard powder (P0, d50 = 44 um);
    * the measured lack-of-fusion (track-continuity) boundary of P0: E_l = P/v = 88 J/m, which
      the study gives for Pe < 2, i.e. below about 1.13 m/s. Above that speed it switches to a
      constant nominal enthalpy density (8.9 J/mm^3 for P0); rebuilding that branch from the
      paper's formula did not join the E_l branch, so it is left out and the speeds above
      1.13 m/s are not scored for lack of fusion;
    * the measured keyhole region (P > 220 W and v < 0.8 m/s for every powder), which the study
      classed as D/W > 0.75.

    It also reruns three process points with the melt isotherm swept from 820 to 880 K. That
    is the only way a composition change such as a Si-enriched AlSi10Mg reaches eagar-tsai.

``private``
    Runs eagar-tsai on the rows of a CSV exported from Thermo-Calc's AM module (our private
    Genesis Mission results), and writes a parity table and plot. Columns:

    ======================  ========  ===========================================================
    column                  required  meaning
    ======================  ========  ===========================================================
    power_w                 yes       laser power, W
    velocity_m_s            yes       scan speed, m/s
    beam_size_um            yes       beam size in um; say which convention with --beam-convention
    absorptivity            yes       the absorptivity the AM module used (fixed or calculated)
    T_melt_k                no        isotherm for the pool edge (default --T-melt)
    k_w_mk, rho_kg_m3,      no        properties (defaults --k, --rho, --cp); use the AM module's
    cp_j_kgk                          values near the liquidus
    am_width_um,            no        AM-module melt-pool width, depth, length; if present, they
    am_depth_um,                      are compared
    am_length_um
    label                   no        free text carried through, e.g. "stock" or "Si-enriched"
    ======================  ========  ===========================================================

Usage::

    python scripts/eagar_tsai_vs_am_module.py published --out arroyave-orchid-tools/eagar-tsai
    python scripts/eagar_tsai_vs_am_module.py private am_module_results.csv \\
        --beam-convention one_over_e2_radius --out private/eagar-vs-am

Needs ``eagar-tsai`` with its compiled integrand (on Linux: ``pip install --no-binary
eagar-tsai eagar-tsai``), plus pandas and matplotlib.
"""

from __future__ import annotations

import argparse
import math
import pathlib
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eagar_tsai import (
    BeamParameters,
    MaterialProperties,
    PrintabilityParameters,
    SimulationDomain,
    compute_melt_pool,
    compute_printability_map,
    compute_single_point,
)

# --- Solyaev et al. 2025 (arXiv:2507.23422), Table 2, Sec. 2.2 and 2.3, Table 3 -------------------
R_M = 40e-6  # 2R = 80 um, q ~ exp(-r^2 / R^2)
BEAM_DIAMETER_2SIGMA_M = 2.0 * R_M / math.sqrt(2.0)  # sigma = R / sqrt(2) -> 56.6 um
OMEGA_M = math.sqrt(2.0) * R_M  # "effective radius" used for Pe and dH
LIQUID = {"k": 120.0, "rho": 1800.0, "cp": 1800.0}
T_SOLIDUS_K = 563.0 + 273.15
T_LIQUIDUS_K = 597.0 + 273.15
A_P0 = 0.22
LAYER_UM = 60.0  # h = h0 / f = 30 um / 0.5
EL_LOF_J_M = 88.0  # P0, valid for Pe < 2
V_PE2_M_S = 1.13  # "Pe = 2 corresponds to v ~ 1.13 m/s" (Sec. 3.2)
KEYHOLE_P_W, KEYHOLE_V_M_S, KEYHOLE_DW = 220.0, 0.8, 0.75

BEAM_CONVENTIONS = {
    # value in um -> eagar-tsai beam_diameter (2 sigma) in m
    "two_sigma": lambda d_um: d_um * 1e-6,
    "one_over_e2_radius": lambda r_um: r_um * 1e-6,  # 1/e^2 radius = 2 sigma
    "one_over_e2_diameter": lambda d_um: 0.5 * d_um * 1e-6,  # 1/e^2 diameter = 4 sigma
    "one_over_e_radius": lambda r_um: math.sqrt(2.0) * r_um * 1e-6,  # exp(-r^2/R^2): 2 sigma = sqrt(2) R
}


def _liquid_material(t_iso: float) -> MaterialProperties:
    return MaterialProperties(
        liquidus_temperature=t_iso,
        thermal_conductivity=LIQUID["k"],
        density=LIQUID["rho"],
        specific_heat=LIQUID["cp"],
    )


def _lof_boundary_power(v: np.ndarray) -> np.ndarray:
    """Measured P0 lack-of-fusion power at speed v: E_l = 88 J/m below Pe = 2, NaN above."""
    v = np.asarray(v, dtype=float)
    return np.where(v < V_PE2_M_S, EL_LOF_J_M * v, np.nan)


def plot_published(df: pd.DataFrame, out: pathlib.Path) -> None:
    """Map of eagar-tsai's default classes with the measured boundaries on top."""
    powers = np.sort(df["power_w"].unique())
    vels = np.sort(df["velocity_m_s"].unique())

    def piv(col: str, frame: pd.DataFrame = df) -> np.ndarray:
        return frame.pivot(index="power_w", columns="velocity_m_s", values=col).loc[powers, vels].to_numpy(dtype=float)

    dw = piv("depth_over_width")
    depth = piv("melt_depth_um")
    cls_map = {"defect_free": 0, "balling": 1, "lack_of_fusion": 2, "keyhole": 3}
    cls = piv("c", df.assign(c=df["defect"].map(cls_map)))
    fig, ax = plt.subplots(figsize=(7.0, 5.0), dpi=150)
    cmap = matplotlib.colors.ListedColormap(["#e8f1e4", "#f3e6c8", "#dde6f3", "#f2d9d9"])
    ax.pcolormesh(vels, powers, cls, cmap=cmap, vmin=-0.5, vmax=3.5, shading="nearest")
    ax.axvspan(V_PE2_M_S, vels.max(), color="0.45", alpha=0.18, lw=0, label="LOF not scored (Pe > 2)")
    cs1 = ax.contour(vels, powers, dw, levels=[0.4], colors="#9b2226", linestyles="--", linewidths=1.2)
    cs3 = ax.contour(vels, powers, depth, levels=[LAYER_UM], colors="#1d4e89", linestyles="--", linewidths=1.2)
    ax.clabel(cs1, fmt={0.4: "D/W = 0.4"}, fontsize=7)
    ax.clabel(cs3, fmt={LAYER_UM: "D = 60 um"}, fontsize=7)
    vv = np.linspace(vels.min(), V_PE2_M_S, 100)
    ax.plot(vv, _lof_boundary_power(vv), color="#1d4e89", lw=2.4, label="measured LOF boundary, P0 (E_l = 88 J/m)")
    ax.add_patch(plt.Rectangle((vels.min(), KEYHOLE_P_W), KEYHOLE_V_M_S - vels.min(), powers.max() - KEYHOLE_P_W,
                               fill=False, ec="#9b2226", lw=2.4, label="measured keyhole region (D/W > 0.75)"))
    ax.plot([], [], color="#9b2226", ls="--", lw=1.2, label="eagar-tsai W/D = 2.5 (its keyhole test)")
    ax.plot([], [], color="#1d4e89", ls="--", lw=1.2, label="eagar-tsai depth = 60 um layer (its LOF1)")
    for name, colour in [("defect-free", "#e8f1e4"), ("balling", "#f3e6c8"), ("lack of fusion", "#dde6f3"),
                         ("keyhole", "#f2d9d9")]:
        ax.fill_between([], [], color=colour, label=f"eagar-tsai class: {name}")
    ax.set_xlabel("scan speed (m/s)")
    ax.set_ylabel("laser power (W)")
    ax.set_xlim(vels.min(), vels.max())
    ax.set_ylim(powers.min(), powers.max())
    ax.set_title("AlSi10Mg: eagar-tsai 0.6.0 vs measured single tracks (arXiv:2507.23422)\n"
                 "2R = 80 um, A = 0.22, liquid properties, solidus isotherm; eagar-tsai never reaches D/W = 0.75",
                 fontsize=8.5)
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), framealpha=0.95)
    fig.savefig(out / "alsi10mg-printability-vs-solyaev2025.png", bbox_inches="tight")
    plt.close(fig)


def run_published(out: pathlib.Path, n_power: int, n_velocity: int, workers: int, res_um: float,
                  sens_res_um: float) -> None:
    out.mkdir(parents=True, exist_ok=True)
    material = _liquid_material(T_SOLIDUS_K)
    params = PrintabilityParameters(
        beam_diameter_m=BEAM_DIAMETER_2SIGMA_M,
        absorptivity=A_P0,
        layer_thickness_m=LAYER_UM * 1e-6,
        hatch_spacing_m=100e-6,  # single tracks: only enters eagar-tsai's LOF2 test
    )
    t0 = time.time()
    df = compute_printability_map(
        params,
        material,
        power_range=(40.0, 400.0),
        velocity_range=(0.1, 2.0),
        n_power=n_power,
        n_velocity=n_velocity,
        domain=SimulationDomain(spatial_resolution_um=res_um),
        workers=workers,
        show_progress=False,
    )
    elapsed = time.time() - t0
    df["depth_over_width"] = df["melt_depth_um"] / df["melt_width_um"].replace(0.0, np.nan)
    df["E_l_J_m"] = df["power_w"] / df["velocity_m_s"]
    df["measured_lof_power_w"] = _lof_boundary_power(df["velocity_m_s"].to_numpy())
    df["measured_class"] = np.select(
        [
            (df["power_w"] > KEYHOLE_P_W) & (df["velocity_m_s"] < KEYHOLE_V_M_S),
            df["velocity_m_s"] >= V_PE2_M_S,
            df["power_w"] < df["measured_lof_power_w"],
        ],
        ["keyhole", "not_scored_pe_gt_2", "lack_of_fusion"],
        default="stable",
    )
    df["eagar_kh_dw075"] = df["depth_over_width"] > KEYHOLE_DW
    df.to_csv(out / "alsi10mg-printability-vs-solyaev2025.csv", index=False, float_format="%.6g")

    # --- agreement summary -------------------------------------------------------------------
    lines = [f"grid {n_power} x {n_velocity}, {res_um} um, {workers} workers: {elapsed:.0f} s"]
    meas_kh = df["measured_class"] == "keyhole"
    for name, pred in [
        ("eagar-tsai default keyhole (W/D <= 2.5)", df["defect"] == "keyhole"),
        ("eagar-tsai D/W > 0.75 (study's rule)", df["eagar_kh_dw075"]),
    ]:
        tp = int((pred & meas_kh).sum())
        fp = int((pred & ~meas_kh).sum())
        fn = int((~pred & meas_kh).sum())
        lines.append(f"{name}: flags {int(pred.sum())} of {len(df)} points; "
                     f"{tp} of {int(meas_kh.sum())} measured-keyhole points, {fp} outside it, {fn} missed")
    scored = df["velocity_m_s"] < V_PE2_M_S
    meas_lof = df["measured_class"] == "lack_of_fusion"
    lines.append(f"lack of fusion scored only below {V_PE2_M_S} m/s ({int(scored.sum())} points):")
    for name, pred in [
        ("eagar-tsai default LOF (LOF1 or LOF2)", (df["defect"] == "lack_of_fusion") & scored),
        (f"eagar-tsai depth <= {LAYER_UM:.0f} um (LOF1 only)", (df["melt_depth_um"] <= LAYER_UM) & scored),
    ]:
        tp = int((pred & meas_lof).sum())
        fp = int((pred & ~meas_lof).sum())
        fn = int((~pred & meas_lof).sum())
        lines.append(f"  {name}: flags {int(pred.sum())} points; "
                     f"{tp} of {int(meas_lof.sum())} measured-LOF points, {fp} outside it, {fn} missed")
    lines.append(f"largest eagar-tsai D/W on the grid: {df['depth_over_width'].max():.2f}")
    counts = df["defect"].value_counts().to_dict()
    lines.append(f"eagar-tsai default classes: {counts}")
    lines.append(f"measured classes: {df['measured_class'].value_counts().to_dict()}")
    # depth eagar-tsai predicts on the measured LOF boundary
    near = df[(df["velocity_m_s"] <= 1.0) & (np.abs(df["E_l_J_m"] - EL_LOF_J_M) / EL_LOF_J_M < 0.15)]
    if len(near):
        lines.append(
            f"on the measured LOF line (E_l = 88 J/m +/-15%, v <= 1 m/s, {len(near)} points): eagar-tsai depth "
            f"{near['melt_depth_um'].min():.0f}-{near['melt_depth_um'].max():.0f} um, width "
            f"{near['melt_width_um'].min():.0f}-{near['melt_width_um'].max():.0f} um (layer h = 60 um)"
        )
    # D/W at the keyhole cross-section condition shown in the study (P = 328 W, v = 0.335 m/s)
    single = compute_single_point(
        BeamParameters(beam_diameter=BEAM_DIAMETER_2SIGMA_M, power=328.0, velocity=0.335, absorptivity=A_P0),
        material,
        SimulationDomain(spatial_resolution_um=res_um),
    )
    lines.append(
        f"P = 328 W, v = 0.335 m/s (the study's keyhole cross-sections): eagar-tsai W = {single.width_um:.0f} um, "
        f"D = {single.depth_um:.0f} um, D/W = {single.depth_um / single.width_um:.2f}, "
        f"peak T = {single.peak_temperature:.0f} K"
    )
    (out / "alsi10mg-printability-vs-solyaev2025-summary.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    plot_published(df, out)

    # --- isotherm sensitivity (how a composition change reaches eagar-tsai) ---------------------
    rows = []
    for p, v in [(200.0, 1.0), (300.0, 1.0), (370.0, 1.3)]:
        for t_iso in [820.0, 836.15, 850.0, 870.15, 880.0]:
            r = compute_single_point(
                BeamParameters(beam_diameter=BEAM_DIAMETER_2SIGMA_M, power=p, velocity=v, absorptivity=A_P0),
                _liquid_material(t_iso),
                SimulationDomain(spatial_resolution_um=sens_res_um),
            )
            rows.append({"power_w": p, "velocity_m_s": v, "T_iso_k": t_iso, "width_um": r.width_um,
                         "depth_um": r.depth_um, "length_um": r.length_um, "peak_T_k": r.peak_temperature})
    sens = pd.DataFrame(rows)
    sens.to_csv(out / "alsi10mg-isotherm-sensitivity.csv", index=False, float_format="%.4g")
    print(sens.to_string(index=False))


def run_private(csv: pathlib.Path, out: pathlib.Path, convention: str, t_melt: float, k: float, rho: float,
                cp: float, workers: int, res_um: float) -> None:
    out.mkdir(parents=True, exist_ok=True)
    src = pd.read_csv(csv)
    missing = {"power_w", "velocity_m_s", "beam_size_um", "absorptivity"} - set(src.columns)
    if missing:
        raise SystemExit(f"{csv} lacks required columns {sorted(missing)}")
    to_m = BEAM_CONVENTIONS[convention]
    df = pd.DataFrame({
        "power_w": src["power_w"].astype(float),
        "velocity_m_s": src["velocity_m_s"].astype(float),
        "beam_diameter_m": [to_m(float(b)) for b in src["beam_size_um"]],
        "absorptivity": src["absorptivity"].astype(float),
        "liquidus_temperature_k": src.get("T_melt_k", pd.Series(t_melt, index=src.index)).astype(float),
        "thermal_conductivity_w_mk": src.get("k_w_mk", pd.Series(k, index=src.index)).astype(float),
        "density_kg_m3": src.get("rho_kg_m3", pd.Series(rho, index=src.index)).astype(float),
        "specific_heat_j_kgk": src.get("cp_j_kgk", pd.Series(cp, index=src.index)).astype(float),
    })
    if not df["beam_diameter_m"].between(1e-6, 1e-3).all():
        raise SystemExit("beam diameters outside 1 um - 1 mm: check beam_size_um units and --beam-convention")
    res = compute_melt_pool(df, domain=SimulationDomain(spatial_resolution_um=res_um), return_field=False,
                            workers=workers, chunk_size=8, show_progress=False)
    res = res.rename(columns={"melt_width_um": "et_width_um", "melt_depth_um": "et_depth_um",
                              "melt_length_um": "et_length_um"})
    keep = [c for c in src.columns if c.startswith("am_") or c == "label"]
    merged = pd.concat([src[keep].reset_index(drop=True), res.reset_index(drop=True)], axis=1)
    pairs = [(q, f"am_{q}_um", f"et_{q}_um") for q in ("width", "depth", "length")]
    for q, am, et in pairs:
        if am in merged:
            merged[f"delta_{q}_um"] = merged[et] - merged[am]
            merged[f"ratio_{q}"] = merged[et] / merged[am]
    merged.to_csv(out / "eagar-tsai-vs-am-module.csv", index=False, float_format="%.5g")
    present = [(q, am, et) for q, am, et in pairs if am in merged]
    if not present:
        print(f"no am_* columns: wrote eagar-tsai predictions for {len(merged)} rows")
        return
    fig, axes = plt.subplots(1, len(present), figsize=(3.6 * len(present), 3.6), dpi=150, squeeze=False)
    for ax, (q, am, et) in zip(axes[0], present):
        ax.scatter(merged[am], merged[et], s=14)
        lim = [0, 1.05 * float(np.nanmax(merged[[am, et]].to_numpy()))]
        ax.plot(lim, lim, color="0.5", lw=1)
        ax.set_xlim(lim)
        ax.set_ylim(lim)
        ax.set_xlabel(f"AM module {q} (um)")
        ax.set_ylabel(f"eagar-tsai {q} (um)")
        mae = float(np.nanmean(np.abs(merged[et] - merged[am])))
        ax.set_title(f"{q}: MAE {mae:.1f} um", fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "eagar-tsai-vs-am-module-parity.png")
    print(merged.describe().T.to_string())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    pub = sub.add_parser("published", help="AlSi10Mg map vs Solyaev et al. 2025 single tracks")
    pub.add_argument("--out", type=pathlib.Path, default=pathlib.Path("eagar-tsai-check"))
    pub.add_argument("--n-power", type=int, default=21)
    pub.add_argument("--n-velocity", type=int, default=20)
    pub.add_argument("--workers", type=int, default=max(1, (len(__import__("os").sched_getaffinity(0)) or 1)))
    pub.add_argument("--resolution-um", type=float, default=2.0)
    pub.add_argument("--sens-resolution-um", type=float, default=1.0, help="grid for the isotherm sweep")
    pub.add_argument("--plot-only", action="store_true", help="redraw the map from the CSV already in --out")
    pri = sub.add_parser("private", help="compare with an AM-module CSV")
    pri.add_argument("csv", type=pathlib.Path)
    pri.add_argument("--out", type=pathlib.Path, default=pathlib.Path("eagar-vs-am"))
    pri.add_argument("--beam-convention", choices=sorted(BEAM_CONVENTIONS), required=True)
    pri.add_argument("--T-melt", type=float, default=867.0, help="pool-edge isotherm, K (default AlSi10Mg liquidus)")
    pri.add_argument("--k", type=float, default=110.0)
    pri.add_argument("--rho", type=float, default=2650.0)
    pri.add_argument("--cp", type=float, default=1040.0)
    pri.add_argument("--workers", type=int, default=4)
    pri.add_argument("--resolution-um", type=float, default=2.0)
    a = ap.parse_args()
    if a.cmd == "published" and a.plot_only:
        plot_published(pd.read_csv(a.out / "alsi10mg-printability-vs-solyaev2025.csv"), a.out)
    elif a.cmd == "published":
        run_published(a.out, a.n_power, a.n_velocity, a.workers, a.resolution_um, a.sens_resolution_um)
    else:
        run_private(a.csv, a.out, a.beam_convention, a.T_melt, a.k, a.rho, a.cp, a.workers, a.resolution_um)


if __name__ == "__main__":
    main()
