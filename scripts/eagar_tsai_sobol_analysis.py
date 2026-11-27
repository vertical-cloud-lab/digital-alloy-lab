"""Analyse the eagar-tsai Sobol sweep for AlSi10Mg (issue #235).

Subcommands (run them in this order; each writes into --out):

  holdout     run eagar-tsai on random rows of the 2**20 design that the 2**12 sweep did not cover
  similarity  rerun sweep rows after rescaling the beam, power and speed together (similarity check)
  analyse     regimes, defect classes, the two-number reduction, surrogate error on the holdout rows,
              Sobol indices, figures and summary.json
  materials   check the surrogate on rows with other material properties (AlSi10Mg ranges, pure Cu),
              then 8-D Sobol indices with the AlSi10Mg property ranges (materials_summary.json)
  predict     predict W, D, L and the peak temperature for any parameter CSV from a finished sweep

Why a 2**20 sweep is not needed. eagar-tsai 0.6.0 (``eagar_tsai/_core.py``) computes

    T(x, y, z) = T0 + S * J(x/s, y/s, z/zeta; p)

with s = sqrt(2) * beam_diameter / 2, zeta = sqrt(alpha*s/v), p = alpha/(v*s), T0 = 298 K and
S = A*P / (pi*rho*c*sqrt(pi*alpha*v*s**3)). The melt pool is where T > T_liq, i.e. where
J > 1/Theta with Theta = S/(T_liq - T0). So W/s, L/s, D/zeta and (T_peak - T0)/S depend on
(Theta, p) alone, for any beam, power, speed, absorptivity and material. A and P enter only as A*P.
The script checks this against eagar-tsai itself (holdout, similarity, materials) and then uses it as an
interpolating surrogate: 4,096 eagar-tsai rows give every row of a 2**20 design in about a minute.

    python scripts/eagar_tsai_sobol_alsi10mg.py --m 12 --out sobol-m12
    python scripts/eagar_tsai_sobol_analysis.py holdout --out sobol-m12
    python scripts/eagar_tsai_sobol_analysis.py similarity --out sobol-m12
    python scripts/eagar_tsai_sobol_analysis.py analyse --out sobol-m12 --figures figs/
    python scripts/eagar_tsai_sobol_analysis.py materials --out sobol-m12
    python scripts/eagar_tsai_sobol_analysis.py predict --train sobol-m12/melt_pool_results.csv \
        --rows my_params.csv --pred my_predictions.csv
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator, RBFInterpolator
from scipy.optimize import minimize_scalar
from scipy.spatial import Delaunay

import eagar_tsai_sobol_alsi10mg as sweep

T0_K = 298.0  # eagar_tsai._types._T0_K, the ambient/base-plate temperature eagar-tsai assumes
T_BOIL_AL_K = 2743.0  # boiling point of Al at 1 atm; above it the conduction-only model does not apply
LAYER_UM, HATCH_UM = 30.0, 190.0  # assumed EOS-like values, as in scripts/eagar_tsai_alsi10mg.py
OUT_UM = ["melt_width_um", "melt_depth_um", "melt_length_um"]
INPUTS = list(sweep.BOUNDS)
# For the `materials` check: the AlSi10Mg property ranges in edison-trajectories/eagar-tsai-alsi10mg-inputs/README.md,
# and pure Cu at room-temperature handbook values (only to test the scaling, not a Cu process window).
ALSI10MG_PROPERTY_RANGES = {
    "liquidus_temperature_k": (860.0, 870.0),
    "thermal_conductivity_w_mk": (63.0, 155.0),
    "density_kg_m3": (2500.0, 2700.0),
    "specific_heat_j_kgk": (920.0, 1200.0),
}
CU_PROPERTIES = {
    "liquidus_temperature_k": 1358.0,
    "thermal_conductivity_w_mk": 390.0,
    "density_kg_m3": 8960.0,
    "specific_heat_j_kgk": 385.0,
}


# ---------------------------------------------------------------------------------------------
# The reduction to two numbers
# ---------------------------------------------------------------------------------------------
def groups(df: pd.DataFrame) -> pd.DataFrame:
    """eagar-tsai's scales and dimensionless groups for each row (same formulas as _core.py)."""
    k, rho, c = df["thermal_conductivity_w_mk"], df["density_kg_m3"], df["specific_heat_j_kgk"]
    alpha = k / (rho * c)
    v = df["velocity_m_s"]
    s = math.sqrt(2.0) * df["beam_diameter_m"] / 2.0
    S = df["absorptivity"] * df["power_w"] / (np.pi * rho * c * np.sqrt(np.pi * alpha * v * s**3))
    return pd.DataFrame(
        {
            "s_um": s * 1e6,
            "zeta_um": np.sqrt(alpha * s / v) * 1e6,
            "p": alpha / (v * s),
            "S_K": S,
            "theta": S / (df["liquidus_temperature_k"] - T0_K),
        },
        index=df.index,
    )


def _centreline_J(x: float, p: float) -> float:
    from eagar_tsai._core import _INTEGRAND  # the package's own (compiled) integrand

    return quad(_INTEGRAND, 0.0, np.inf, args=(x, 0.0, 0.0, p))[0]


def _peak_J(p: float) -> float:
    """max_x J(x, 0, 0; p): the peak of the surface centreline, found by scan + bounded Brent."""
    xs = np.linspace(-2.0, 4.0, 61)
    i = int(np.argmax([_centreline_J(x, p) for x in xs]))
    lo, hi = xs[max(i - 1, 0)], xs[min(i + 1, xs.size - 1)]
    return -minimize_scalar(lambda x: -_centreline_J(x, p), bounds=(lo, hi), method="bounded", options={"xatol": 1e-7}).fun


class PeakFactor:
    """G(p) = (T_peak - T0)/S, tabulated once on a log grid and interpolated (PCHIP in log10 p)."""

    def __init__(self, log10_p_min: float = -3.0, log10_p_max: float = 3.0, n: int = 121):
        self.log_p = np.linspace(log10_p_min, log10_p_max, n)
        self.G = np.array([_peak_J(10.0**lp) for lp in self.log_p])
        self._f = PchipInterpolator(self.log_p, np.log(self.G), extrapolate=False)

    def __call__(self, p) -> np.ndarray:
        lp = np.log10(np.asarray(p, dtype=float))
        if np.any((lp < self.log_p[0]) | (lp > self.log_p[-1])):
            raise ValueError(f"p outside the tabulated range 1e{self.log_p[0]:g}..1e{self.log_p[-1]:g}")
        return np.exp(self._f(lp))


class Surrogate:
    """Melt-pool dimensions from finished eagar-tsai rows, by interpolation in (Theta, p).

    Coordinates: x1 = log10(Theta*G(p)) (> 0 means the peak passes the liquidus) and x2 = log10(p).
    Targets: log(Y**2 / (Theta*G - 1)) for Y = W/s, D/zeta, L/s. Each Y grows like sqrt(Theta*G - 1)
    just above the melting threshold, so these targets stay finite and vary slowly. A local
    thin-plate-spline RBF (64 neighbours) with light smoothing averages out eagar-tsai's grid steps
    (W comes in steps of two grid spacings, D and L in steps of one). Chosen by cross-validation on
    the 4,096 sweep rows: it beat linear (Delaunay) and Clough-Tocher interpolation, mostly at the
    edges of the box. Rows outside the convex hull of the training rows are flagged ``extrapolated``.
    """

    SMOOTHING, NEIGHBORS = 0.03, 64

    def __init__(self, train: pd.DataFrame, peak: PeakFactor | None = None):
        self.peak = peak or PeakFactor()
        g = groups(train)
        margin = g["theta"].to_numpy() * self.peak(g["p"])
        y = self._dimensionless(train, g)
        ok = (margin > 1.0) & np.all(y > 0, axis=1) & train[OUT_UM].notna().all(axis=1).to_numpy()
        X = np.column_stack([np.log10(margin[ok]), np.log10(g["p"].to_numpy()[ok])])
        t = np.log(y[ok] ** 2 / (margin[ok, None] - 1.0))
        self.n_train = int(ok.sum())
        self._rbf = RBFInterpolator(X, t, kernel="thin_plate_spline", smoothing=self.SMOOTHING, neighbors=self.NEIGHBORS)
        self._hull = Delaunay(X)

    @staticmethod
    def _dimensionless(df: pd.DataFrame, g: pd.DataFrame) -> np.ndarray:
        return np.column_stack(
            [
                df["melt_width_um"] / g["s_um"],
                df["melt_depth_um"] / g["zeta_um"],
                df["melt_length_um"] / g["s_um"],
            ]
        )

    def predict(self, rows: pd.DataFrame) -> pd.DataFrame:
        g = groups(rows)
        G = self.peak(g["p"])
        margin = g["theta"].to_numpy() * G
        out = pd.DataFrame(index=rows.index)
        out["peak_temperature"] = T0_K + g["S_K"].to_numpy() * G
        melts = margin > 1.0
        X = np.column_stack([np.log10(margin[melts]), np.log10(g["p"].to_numpy()[melts])])
        t = self._rbf(X) if len(X) else np.empty((0, 3))
        outside = self._hull.find_simplex(X) < 0 if len(X) else np.zeros(0, dtype=bool)
        Y = np.zeros((len(rows), 3))
        Y[melts] = np.sqrt(np.exp(t) * (margin[melts, None] - 1.0))
        scale = np.column_stack([g["s_um"], g["zeta_um"], g["s_um"]])
        for j, name in enumerate(OUT_UM):
            out[name] = Y[:, j] * scale[:, j]
        out["extrapolated"] = False
        out.loc[out.index[np.flatnonzero(melts)[outside]], "extrapolated"] = True
        return out


# ---------------------------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------------------------
def regime(df: pd.DataFrame) -> pd.Series:
    """no melt / conduction (peak below Al boiling) / above boiling."""
    lab = np.where(df["melt_width_um"] > 0, "conduction", "no_melt")
    lab = np.where((df["melt_width_um"] > 0) & (df["peak_temperature"] > T_BOIL_AL_K), "above_boiling", lab)
    return pd.Series(lab, index=df.index)


def defect_class(df: pd.DataFrame) -> pd.Series:
    """eagar-tsai's own five-criterion classification (Sheikh et al. 2024), 30 um layer, 190 um hatch."""
    from eagar_tsai._api import _classify_defect  # private; used so the criteria match the package exactly

    return pd.Series(
        [
            _classify_defect(ln, w, d, LAYER_UM, HATCH_UM)[0]
            for ln, w, d in zip(df["melt_length_um"], df["melt_width_um"], df["melt_depth_um"], strict=True)
        ],
        index=df.index,
    )


def fractions(s: pd.Series) -> dict[str, float]:
    return {k: round(float(v), 4) for k, v in s.value_counts(normalize=True).sort_index().items()}


# ---------------------------------------------------------------------------------------------
# Direct eagar-tsai runs
# ---------------------------------------------------------------------------------------------
def cmd_holdout(args) -> None:
    design = sweep.sobol_design(args.design_m, args.seed)
    rng = np.random.default_rng(args.rng_seed)
    idx = np.sort(rng.choice(np.arange(2**args.train_m, len(design)), size=args.n, replace=False))
    rows = design.iloc[idx].reset_index(drop=True)
    print(f"holdout: {len(rows)} random rows of the 2**{args.design_m} design, beyond row {2**args.train_m}", flush=True)
    res = sweep.run_rows(rows, args.resolution_um)
    res.to_csv(args.out / "holdout_results.csv", index=False)
    print(f"wrote {args.out / 'holdout_results.csv'}", flush=True)


def cmd_similarity(args) -> None:
    """Scale beam diameter and power by f and divide speed by f: Theta and p stay fixed, so every
    length should scale by f and the peak temperature should not change. Also trade A against P."""
    train = pd.read_csv(args.out / "melt_pool_results.csv")
    pick = train[(train["melt_width_um"].between(80, 260)) & (train["melt_depth_um"] >= 20)]
    base = pick.sample(n=args.n, random_state=args.rng_seed).sort_values("sample_id")[["sample_id", *INPUTS, *sweep.MATERIAL]]
    variants = []
    for f in (1.0, 0.5, 2.0):
        v = base.copy()
        v["beam_diameter_m"] *= f
        v["power_w"] *= f
        v["velocity_m_s"] /= f
        v.insert(1, "variant", f"scale_{f:g}")
        variants.append(v)
    trade = base.copy()
    trade["absorptivity"] *= 0.8
    trade["power_w"] /= 0.8
    trade.insert(1, "variant", "A*0.8,P/0.8")
    variants.append(trade)
    rows = pd.concat(variants, ignore_index=True)
    print(f"similarity: {len(rows)} rows ({args.n} base rows x 4 variants) at {args.resolution_um} um", flush=True)
    res = sweep.run_rows(rows.drop(columns="variant"), args.resolution_um)
    res.insert(1, "variant", rows["variant"])
    res.to_csv(args.out / "similarity_results.csv", index=False)
    print(f"wrote {args.out / 'similarity_results.csv'}", flush=True)


# ---------------------------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------------------------
def error_stats(pred: pd.DataFrame, true: pd.DataFrame) -> dict:
    out = {}
    ok = true[OUT_UM].notna().all(axis=1).to_numpy()
    for name in [*OUT_UM, "peak_temperature"]:
        e = (pred[name] - true[name]).to_numpy()[ok]
        a = np.abs(e)
        out[name] = {
            "mean": round(float(e.mean()), 3),
            "median_abs": round(float(np.median(a)), 3),
            "p95_abs": round(float(np.quantile(a, 0.95)), 3),
            "p99_abs": round(float(np.quantile(a, 0.99)), 3),
            "max_abs": round(float(a.max()), 3),
        }
    return out


def first_order_given_data(df: pd.DataFrame, outputs: list[str], bins: int = 32) -> pd.DataFrame:
    """S1 from the sweep rows directly: Var(E[y | x_i bin]) / Var(y), equal-count bins."""
    rows = {}
    for x in INPUTS:
        b = pd.qcut(df[x], bins, labels=False)
        rows[x] = {y: float(df.groupby(b)[y].mean().var(ddof=0) / df[y].var(ddof=0)) for y in outputs}
    return pd.DataFrame(rows).T


def sobol_on_surrogate(sur: Surrogate, n: int, seed: int, bounds: dict | None = None, fixed: dict | None = None) -> dict:
    """Saltelli/Jansen Sobol indices of the surrogate over a box (default: the sweep box, fixed AlSi10Mg)."""
    from scipy.stats import sobol_indices, uniform

    bounds = bounds or sweep.BOUNDS
    fixed = sweep.MATERIAL if fixed is None else fixed
    inputs = list(bounds)
    dists = [uniform(lo, hi - lo) for lo, hi in bounds.values()]
    names = ["melt_width_um", "melt_depth_um", "melt_length_um", "peak_temperature"]

    def f(x: np.ndarray) -> np.ndarray:
        rows = pd.DataFrame(x.T, columns=inputs)
        for k, v in fixed.items():
            rows[k] = v
        p = sur.predict(rows)
        return np.vstack([p[c].to_numpy() for c in names])

    res = sobol_indices(func=f, n=n, dists=dists, rng=np.random.default_rng(seed))
    boot = res.bootstrap(confidence_level=0.95, n_resamples=200)
    out = {}
    for i, name in enumerate(names):
        out[name] = {
            x: {
                "S1": round(float(res.first_order[i, j]), 4),
                "S1_ci": [round(float(boot.first_order.confidence_interval.low[i, j]), 4), round(float(boot.first_order.confidence_interval.high[i, j]), 4)],
                "ST": round(float(res.total_order[i, j]), 4),
                "ST_ci": [round(float(boot.total_order.confidence_interval.low[i, j]), 4), round(float(boot.total_order.confidence_interval.high[i, j]), 4)],
            }
            for j, x in enumerate(inputs)
        }
    return out


def cmd_analyse(args) -> None:
    train = pd.read_csv(args.out / "melt_pool_results.csv")
    holdout = pd.read_csv(args.out / "holdout_results.csv")
    summary: dict = {"n_train": len(train), "n_holdout": len(holdout)}
    for name, df in (("train", train), ("holdout", holdout)):
        summary[f"failed_rows_{name}"] = int(df[OUT_UM].isna().any(axis=1).sum())
        df["regime"] = regime(df)
        df["defect"] = defect_class(df)
        summary[f"regimes_{name}"] = fractions(df["regime"])
        summary[f"defects_{name}"] = fractions(df["defect"])
        summary[f"defect_free_and_below_boiling_{name}"] = round(float(((df["defect"] == "defect_free") & (df["regime"] == "conduction")).mean()), 4)

    peak = PeakFactor()
    g = groups(train)
    G = peak(g["p"])
    measured_G = (train["peak_temperature"] - T0_K) / g["S_K"]
    summary["peak_factor_vs_eagar_tsai_grid"] = {
        "max_rel_diff": round(float(np.max(np.abs(measured_G / G - 1))), 5),
        "median_rel_diff": round(float(np.median(np.abs(measured_G / G - 1))), 5),
    }
    melt = train["melt_width_um"] > 0
    summary["melt_threshold_misclassified"] = int(((g["theta"] * G > 1) != melt).sum())

    sur = Surrogate(train, peak)
    pred = sur.predict(holdout)
    summary["surrogate_train_rows"] = sur.n_train
    summary["holdout_extrapolated_rows"] = int(pred["extrapolated"].sum())
    summary["holdout_error"] = error_stats(pred, holdout)
    pred["regime"], pred["defect"] = regime(pred), defect_class(pred)
    summary["holdout_regime_agreement"] = round(float((pred["regime"] == holdout["regime"]).mean()), 4)
    summary["holdout_defect_agreement"] = round(float((pred["defect"] == holdout["defect"]).mean()), 4)
    for c in [*OUT_UM, "peak_temperature"]:
        holdout[f"{c}_surrogate"] = pred[c]
    holdout["surrogate_extrapolated"] = pred["extrapolated"]

    sim_path = args.out / "similarity_results.csv"
    if sim_path.exists():
        sim = pd.read_csv(sim_path)
        base = sim[sim["variant"] == "scale_1"].set_index("sample_id")
        rows = []
        for variant, f in (("scale_0.5", 0.5), ("scale_2", 2.0), ("A*0.8,P/0.8", 1.0)):
            v = sim[sim["variant"] == variant].set_index("sample_id").loc[base.index]
            rows.append(
                {
                    "variant": variant,
                    **{f"max_abs_diff_{c}": round(float(np.max(np.abs(v[c] / f - base[c]))), 3) for c in OUT_UM},
                    "max_rel_diff_peak_T": round(float(np.max(np.abs(v["peak_temperature"] / base["peak_temperature"] - 1))), 5),
                }
            )
        summary["similarity"] = rows

    summary["sobol_surrogate"] = sobol_on_surrogate(sur, args.sobol_n, args.seed)
    s1 = first_order_given_data(train, [*OUT_UM, "peak_temperature"])
    summary["sobol_S1_given_data_train"] = {y: {x: round(float(s1.loc[x, y]), 4) for x in INPUTS} for y in s1.columns}

    # The whole 2**design_m design, from the surrogate.
    design = sweep.sobol_design(args.design_m, args.seed)
    full = design.join(sur.predict(design))
    full["regime"], full["defect"] = regime(full), defect_class(full)
    summary[f"surrogate_2^{args.design_m}"] = {
        "rows": len(full),
        "extrapolated_rows": int(full["extrapolated"].sum()),
        "regimes": fractions(full["regime"]),
        "defects": fractions(full["defect"]),
        "defect_free_and_below_boiling": round(float(((full["defect"] == "defect_free") & (full["regime"] == "conduction")).mean()), 4),
    }

    args.out.joinpath("summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    holdout.to_csv(args.out / "holdout_results_with_surrogate.csv", index=False)
    train.to_csv(args.out / "melt_pool_results_classified.csv", index=False)
    print(json.dumps(summary, indent=2))
    if args.figures:
        import eagar_tsai_sobol_figures as figs

        figs.make_all(train, holdout, peak, sur, summary, args.figures)


def cmd_materials(args) -> None:
    """Does the surrogate, built from fixed-property AlSi10Mg rows, hold when the material changes?

    (a) an 8-D Sobol design: the sweep box plus the AlSi10Mg property ranges; (b) pure Cu over the sweep box.
    Both are run directly with eagar-tsai and compared with the surrogate; then 8-D Sobol indices.
    """
    from scipy.stats import qmc

    box = {**sweep.BOUNDS, **ALSI10MG_PROPERTY_RANGES}
    pts = qmc.Sobol(d=len(box), scramble=True, seed=args.rng_seed).random_base2(m=args.m)
    a = pd.DataFrame(qmc.scale(pts, *zip(*box.values(), strict=True)), columns=list(box))
    a.insert(0, "sample_id", np.arange(len(a)))
    b = sweep.sobol_design(args.m, args.rng_seed)
    for k, v in CU_PROPERTIES.items():
        b[k] = v
    rows = pd.concat([a.assign(case="AlSi10Mg_property_ranges"), b[a.columns].assign(case="pure_Cu")], ignore_index=True)
    print(f"materials: {len(a)} AlSi10Mg rows with varied properties + {len(b)} pure-Cu rows", flush=True)
    res = sweep.run_rows(rows.drop(columns="case"), args.resolution_um)
    res.insert(1, "case", rows["case"])

    train = pd.read_csv(args.out / "melt_pool_results.csv")
    sur = Surrogate(train)
    pred = sur.predict(res)
    for c in [*OUT_UM, "peak_temperature"]:
        res[f"{c}_surrogate"] = pred[c]
    res["surrogate_extrapolated"] = pred["extrapolated"]
    res.to_csv(args.out / "materials_results.csv", index=False)

    check = {}
    for case, df in res.groupby("case"):
        g = groups(df)
        melt = df["melt_width_um"] > 0
        entry = {
            "rows": len(df),
            "melting_rows": int(melt.sum()),
            "melt_threshold_misclassified": int(((g["theta"] * sur.peak(g["p"]) > 1) != melt).sum()),
            "p_range": [round(float(g["p"].min()), 4), round(float(g["p"].max()), 4)],
            "extrapolated_rows": int(df["surrogate_extrapolated"].sum()),
        }
        for label, sel in (("inside_hull", ~df["surrogate_extrapolated"]), ("extrapolated", df["surrogate_extrapolated"])):
            sub = df[sel]
            if len(sub):
                pr = sub[[f"{c}_surrogate" for c in [*OUT_UM, "peak_temperature"]]].rename(columns=lambda c: c.removesuffix("_surrogate"))
                entry[f"error_{label}"] = error_stats(pr, sub)
        check[case] = entry
    out = {
        "materials_check": check,
        "sobol_surrogate_8d_alsi10mg_property_ranges": sobol_on_surrogate(sur, args.sobol_n, args.seed, bounds=box, fixed={}),
    }
    args.out.joinpath("materials_summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


# Column names of the original sobol_params.csv in issue #235 -> eagar-tsai's names.
SHORT_NAMES = {
    "beam_diameter": "beam_diameter_m",
    "power": "power_w",
    "velocity": "velocity_m_s",
    "liquidus_temperature": "liquidus_temperature_k",
    "thermal_conductivity": "thermal_conductivity_w_mk",
    "density": "density_kg_m3",
    "specific_heat": "specific_heat_j_kgk",
}


def cmd_predict(args) -> None:
    sur = Surrogate(pd.read_csv(args.train))
    rows = pd.read_csv(args.rows).rename(columns=SHORT_NAMES)
    sweep.check_units(rows)  # refuses a beam diameter in um, as in the original sobol_params.csv
    out = rows.join(sur.predict(rows))
    out.to_csv(args.pred, index=False)
    print(f"wrote {args.pred}: {len(out)} rows, {int(out['extrapolated'].sum())} outside the training rows' hull (extrapolated)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("holdout", "similarity", "analyse", "materials"):
        p = sub.add_parser(name)
        p.add_argument("--out", type=pathlib.Path, required=True, help="sweep output folder (has melt_pool_results.csv)")
        p.add_argument("--seed", type=int, default=42, help="Sobol seed of the sweep")
        p.add_argument("--rng-seed", type=int, default=235)
        p.add_argument("--design-m", type=int, default=20, help="the full design is 2**design_m rows")
        p.add_argument("--train-m", type=int, default=12, help="the sweep ran the first 2**train_m rows")
    hp = sub.choices["holdout"]
    hp.add_argument("--n", type=int, default=2048)
    hp.add_argument("--resolution-um", type=float, default=2.0)
    sp = sub.choices["similarity"]
    sp.add_argument("--n", type=int, default=16)
    sp.add_argument("--resolution-um", type=float, default=1.0)
    an = sub.choices["analyse"]
    an.add_argument("--sobol-n", type=int, default=2**14, help="Saltelli base sample size for the surrogate")
    an.add_argument("--figures", type=pathlib.Path, default=None)
    mp = sub.choices["materials"]
    mp.add_argument("--m", type=int, default=9, help="2**m rows for each case")
    mp.add_argument("--resolution-um", type=float, default=2.0)
    mp.add_argument("--sobol-n", type=int, default=2**13)
    pr = sub.add_parser("predict")
    pr.add_argument("--train", type=pathlib.Path, required=True)
    pr.add_argument("--rows", type=pathlib.Path, required=True)
    pr.add_argument("--pred", type=pathlib.Path, required=True)
    args = ap.parse_args()
    {"holdout": cmd_holdout, "similarity": cmd_similarity, "analyse": cmd_analyse, "materials": cmd_materials, "predict": cmd_predict}[args.cmd](args)


if __name__ == "__main__":
    main()
