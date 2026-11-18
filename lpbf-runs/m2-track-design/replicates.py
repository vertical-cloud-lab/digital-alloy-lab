"""Repeats or more settings? A simulation of the 84-wall M2 build (issue #100, PR #243, 2026-11-18).

    python replicates.py          # -> out/replicates_sim.csv, out/m2-replicates.png (a few minutes on 4 cores)
    python replicates.py figure   # redraw the figure from the CSV

Sterling asked (PR #243, 2026-11-18) whether to print each condition three times, randomized over the plate, or to
make the four squares identical, since nobody knows yet how far apart two walls at the same setting come out. This
compares those with the build as it stands (wall_sheet.py: 60 settings and the control, 18 settings and the control
printed again on the turned square 4), with Carl's 42-settings-both-ways option, and with 84 settings and no
repeats. Every design is 84 walls, and every design includes the control (370 W, 1350 mm/s).

The truth is unknown, so each trial draws one at random around what Eagar-Tsai and Tang's overlap rule give for
these walls (wall_sheet.py):

- porosity (%) = phi_dense + A s softplus((m L - 1) / s) + B sigmoid((Ke - Ke_kh) / 0.4), where L is Tang's
  lack-of-fusion index at 30 um layers (interpolated from out/wall_regime_grid.csv) and Ke Gan's keyhole number at
  the 130 um spot. m moves the boundary (0.75 to 1.6, log-uniform: absorptivity, layer thickness and Eagar-Tsai's
  conduction-only depth are all uncertain), A is 4-20 % per unit of L, s 0.03-0.15 sets how sharp the boundary is,
  phi_dense is 0.02-0.1 %, and the keyhole term has B 0.1-1 % and Ke_kh 5-7 (the walls reach Ke 6.3).
- each wall's measured ln(porosity) = truth + its square's offset (SD 0.15, for gas flow and spatter) + noise with
  SD sigma at the edges of the window, rising to 2 sigma on the lack-of-fusion boundary, where porosity is most
  erratic. sigma runs 0.15-1.0, so two walls at one setting differ by a factor of about 1.2 to 3.
- turned walls get an orientation offset: none in the main comparison; 0.3 everywhere in "turned +0.3"; and in
  "turned hurts cold walls", 0.5 on the lack-of-fusion side only (the blade or the gas flow matters most there).

Each design is analysed the same way: the orientation offset is estimated from the pairs, where there are any, and
removed; then a Gaussian process (Matern 5/2 with a length scale per axis, plus white noise) is fit to ln(porosity)
in the Sobol unit square (P linear, P/v log), as the BO would be. Scores, on a 41 x 41 grid over the window:

- map_rmse: RMS error of the fitted ln(porosity) against the plate-average truth;
- boundary_wrong: the fraction of the window put on the wrong side of 0.5 % porosity;
- scatter_ratio: the wall-to-wall scatter the design estimates (pooled over its repeats, or the GP's white noise if
  it has none), divided by the true one (the RMS over the window of the noise SD, with the square offsets).
"""
from __future__ import annotations

import csv
import math
import os
import sys
import warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")      # one BLAS thread a worker: 4 workers x 4 threads stalled the GP fits
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))

import wall_sheet as ws                         # noqa: E402  (window, control, Tang's index)
from line_sheet import keyhole_number           # noqa: E402

N_TRIALS = 200
SIGMAS = (0.15, 0.3, 0.6, 1.0)
SQUARE_SD = 0.15
THRESHOLD = 0.5                                  # % porosity: the boundary scored
DESIGNS = ("84 settings", "61 sets (now)", "42 x 2", "28 x 3", "21 x 4")
ORIENT_CASES = {"none": None, "turned +0.3": 0.3, "turned hurts cold walls": "lof"}
ORIENT_DESIGNS = ("61 sets (now)", "61 sets, one copy unturned", "42 x 2")


# --- the truth ---------------------------------------------------------------------------------------------------------
def _interpolators():
    rows = list(csv.DictReader(open(OUT / "wall_regime_grid.csv", encoding="utf-8")))
    Ps = sorted({float(r["P_W"]) for r in rows})
    vs = sorted({float(r["v_mm_s"]) for r in rows})
    W = np.zeros((len(Ps), len(vs)))
    D = np.zeros_like(W)
    for r in rows:
        i, j = Ps.index(float(r["P_W"])), vs.index(float(r["v_mm_s"]))
        W[i, j], D[i, j] = float(r["ET_width_um"]), float(r["ET_depth_um"])
    axes = (np.array(Ps), np.log(vs))
    return RegularGridInterpolator(axes, np.log(W)), RegularGridInterpolator(axes, np.log(D))


IW, ID = _interpolators()


def features(u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Tang's index at 30 um layers and Ke at 130 um, for points in the Sobol unit square."""
    P, v = ws.to_pv(np.clip(u, 0.0, 1.0))
    pts = np.column_stack([P, np.log(v)])
    W, D = np.exp(IW(pts)), np.exp(ID(pts))
    L = (ws.TRACE_MM * 1e3 / W) ** 2 + (30.0 / D) ** 2
    ke = np.array([keyhole_number(p, s, ws.SPOT_UM) for p, s in zip(P, v)])
    return L, ke


def draw_truth(rng: np.random.Generator) -> dict:
    return dict(m=math.exp(rng.uniform(math.log(0.75), math.log(1.6))), A=rng.uniform(4, 20),
                s=rng.uniform(0.03, 0.15), phi0=math.exp(rng.uniform(math.log(0.02), math.log(0.1))),
                B=rng.uniform(0.1, 1.0), ke_kh=rng.uniform(5.0, 7.0))


def ln_phi(t: dict, L: np.ndarray, ke: np.ndarray) -> np.ndarray:
    x = (t["m"] * L - 1.0) / t["s"]
    softplus = np.logaddexp(0.0, x)
    keyhole = 1.0 / (1.0 + np.exp(-(ke - t["ke_kh"]) / 0.4))
    return np.log(t["phi0"] + t["A"] * t["s"] * softplus + t["B"] * keyhole)


def noise_sd(t: dict, L: np.ndarray, sigma: float) -> np.ndarray:
    return sigma * (1.0 + np.exp(-(((t["m"] * L) - 1.0) / 0.2) ** 2))


# --- the designs -------------------------------------------------------------------------------------------------------
def sobol(n: int, seed: int) -> np.ndarray:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return qmc.Sobol(d=2, scramble=True, seed=seed).random(n)


def design(name: str, seed: int) -> dict:
    """Walls as arrays: u (n x 2), square (1-4), turned (0/1), setting id, and pair id for settings printed both
    ways (-1 otherwise). The control is setting 0 and sits at ws.control_unit()."""
    rng = np.random.default_rng(seed)
    C = ws.control_unit()

    def pts(n):                                   # n settings: the control and n - 1 Sobol points
        return np.vstack([C, sobol(n - 1, seed)])

    u, sq, turned, sid = [], [], [], []

    def add(i, p, s, t):
        u.append(p); sq.append(s); turned.append(t); sid.append(i)

    if name == "84 settings":
        P = pts(84)
        for i, s in enumerate(rng.permutation(np.repeat([1, 2, 3, 4], 21))):
            add(i, P[i], s, 0)
    elif name.startswith("61 sets"):
        P = pts(61)                               # 0 = control, 1-60 = W000-W059
        blocks = [list(range(1 + 20 * b, 21 + 20 * b)) for b in range(3)]
        for b, blk in enumerate(blocks):
            for i in blk + [0]:
                add(i, P[i], b + 1, 0)
        unturned_copy = name.endswith("unturned")
        for b, blk in enumerate(blocks):          # square 4: a copy of square b+1's part b+1 (6 settings + control)
            for i in list(rng.choice(blk, 6, replace=False)) + [0]:
                add(i, P[i], 4, 0 if (unturned_copy and b == 2) else 1)
    elif name == "42 x 2":                        # every setting along (squares 1-2) and turned (squares 3-4)
        P = pts(42)
        for i in range(42):
            add(i, P[i], 1 + i % 2, 0)
            add(i, P[i], 3 + (i + 1) % 2, 1)
    elif name == "28 x 3":                        # each setting on 3 of the 4 squares, 21 walls a square
        P = pts(28)
        for k, i in enumerate(rng.permutation(28)):
            for s in [s for s in (1, 2, 3, 4) if s != 1 + k % 4]:
                add(i, P[i], s, 0)
    elif name == "21 x 4":                        # the four squares identical
        P = pts(21)
        for i in range(21):
            for s in (1, 2, 3, 4):
                add(i, P[i], s, 0)
    else:
        raise ValueError(name)
    u, sq, turned, sid = map(np.array, (u, sq, turned, sid))
    assert len(u) == 84, (name, len(u))
    return dict(u=u, square=sq, turned=turned, sid=sid)


# --- the analysis ------------------------------------------------------------------------------------------------------
def orientation_offset(d: dict, y: np.ndarray) -> float:
    """Mean difference turned minus along, over the settings printed both ways."""
    diffs = []
    for i in np.unique(d["sid"][d["turned"] == 1]):
        a = y[(d["sid"] == i) & (d["turned"] == 0)]
        b = y[(d["sid"] == i) & (d["turned"] == 1)]
        if len(a) and len(b):
            diffs.append(b.mean() - a.mean())
    return float(np.mean(diffs)) if diffs else 0.0


def pooled_sd(d: dict, y: np.ndarray, pure_only: bool = False) -> tuple[float, int]:
    """Pooled SD over walls at the same setting (after the orientation offset is removed), and its degrees of
    freedom. With pure_only, only walls at the same setting AND orientation count."""
    ss, df = 0.0, 0
    keys = zip(d["sid"], d["turned"]) if pure_only else zip(d["sid"], np.zeros_like(d["sid"]))
    keys = np.array(list(keys))
    for k in np.unique(keys, axis=0):
        g = y[(keys == k).all(axis=1)]
        if len(g) > 1:
            ss += float(((g - g.mean()) ** 2).sum())
            df += len(g) - 1
    if df and not pure_only and d["turned"].any():
        df -= 1                                   # one df went to the orientation offset
    return (math.sqrt(ss / df) if df > 0 else float("nan")), df


def fit_gp(u: np.ndarray, y: np.ndarray, grid: np.ndarray) -> tuple[np.ndarray, float]:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel

    kernel = (ConstantKernel(1.0, (1e-3, 1e3)) * Matern([0.3, 0.3], (0.03, 5.0), nu=2.5)
              + WhiteKernel(0.05, (1e-5, 2.0)))
    gp = GaussianProcessRegressor(kernel, normalize_y=True, n_restarts_optimizer=2, random_state=0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gp.fit(u, y)
    noise = gp.kernel_.k2.noise_level * float(np.std(y)) ** 2
    return gp.predict(grid), math.sqrt(noise)


def grid_points(n: int = 41) -> np.ndarray:
    g = (np.arange(n) + 0.5) / n
    return np.array([(a, b) for a in g for b in g])


GRID = grid_points()
GRID_L, GRID_KE = features(GRID)


def trial(args) -> list[dict]:
    t_idx, sigma, case, names = args
    rng = np.random.default_rng(1000 + t_idx)
    t = draw_truth(rng)
    f_grid = ln_phi(t, GRID_L, GRID_KE)
    sd_grid = noise_sd(t, GRID_L, sigma)
    true_scatter = math.sqrt(float(np.mean(sd_grid ** 2)) + SQUARE_SD ** 2)
    offsets = rng.normal(0.0, SQUARE_SD, 5)
    rows = []
    for name in names:
        d = design(name, 2000 + t_idx)
        L, ke = features(d["u"])
        f = ln_phi(t, L, ke)
        if ORIENT_CASES[case] == "lof":
            orient = 0.5 / (1.0 + np.exp(-(t["m"] * L - 1.0) / 0.1))
        else:
            orient = np.full(len(f), ORIENT_CASES[case] or 0.0)
        y = (f + offsets[d["square"]] + orient * d["turned"]
             + rng.normal(0.0, 1.0, len(f)) * noise_sd(t, L, sigma))
        y_adj = y - orientation_offset(d, y) * d["turned"]
        pred, gp_noise = fit_gp(d["u"], y_adj, GRID)
        scatter, df = pooled_sd(d, y_adj)
        pure, pure_df = pooled_sd(d, y, pure_only=True)
        if not df:
            scatter = gp_noise
        rows.append(dict(trial=t_idx, sigma=sigma, orientation=case, design=name,
                         settings=len(np.unique(d["sid"])), repeat_df=df, pure_repeat_df=pure_df,
                         map_rmse=round(float(np.sqrt(np.mean((pred - f_grid) ** 2))), 4),
                         boundary_wrong=round(float(np.mean((pred > math.log(THRESHOLD))
                                                            != (f_grid > math.log(THRESHOLD)))), 4),
                         scatter_ratio=round(scatter / true_scatter, 4),
                         pure_scatter_ratio=round(pure / true_scatter, 4) if pure_df else "",
                         true_scatter=round(true_scatter, 4)))
    return rows


def run() -> list[dict]:
    jobs = [(k, s, "none", DESIGNS) for s in SIGMAS for k in range(N_TRIALS)]
    jobs += [(k, s, case, ORIENT_DESIGNS) for case in ("turned +0.3", "turned hurts cold walls")
             for s in (0.3, 0.6) for k in range(N_TRIALS)]
    with Pool() as pool:
        rows = [r for rs in pool.imap_unordered(trial, jobs, chunksize=4) for r in rs]
    rows.sort(key=lambda r: (r["orientation"], r["sigma"], r["design"], r["trial"]))
    with open(OUT / "replicates_sim.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def summary(rows: list[dict]) -> list[dict]:
    out = []
    keys = sorted({(r["orientation"], float(r["sigma"]), r["design"]) for r in rows})
    for case, sigma, name in keys:
        rs = [r for r in rows if r["orientation"] == case and float(r["sigma"]) == sigma and r["design"] == name]
        col = lambda k: np.array([float(r[k]) for r in rs if r[k] != ""])
        ratio = col("scatter_ratio")
        pure = col("pure_scatter_ratio")
        out.append(dict(orientation=case, sigma=sigma, design=name, settings=rs[0]["settings"],
                        repeat_df=rs[0]["repeat_df"], pure_repeat_df=rs[0]["pure_repeat_df"],
                        map_rmse=round(float(np.median(col("map_rmse"))), 3),
                        boundary_wrong_pct=round(100 * float(np.median(col("boundary_wrong"))), 1),
                        scatter_ratio_median=round(float(np.median(ratio)), 2),
                        scatter_ratio_p10=round(float(np.percentile(ratio, 10)), 2),
                        scatter_ratio_p90=round(float(np.percentile(ratio, 90)), 2),
                        pure_ratio_median=round(float(np.median(pure)), 2) if len(pure) else "",
                        pure_ratio_p10=round(float(np.percentile(pure, 10)), 2) if len(pure) else "",
                        pure_ratio_p90=round(float(np.percentile(pure, 90)), 2) if len(pure) else ""))
    return out


# --- figure ------------------------------------------------------------------------------------------------------------
STYLE = {"84 settings": ("#2a78d6", "o"), "61 sets (now)": ("#eb6834", "s"), "42 x 2": ("#1baf7a", "^"),
         "28 x 3": ("#eda100", "D"), "21 x 4": ("#e87ba4", "v")}        # categorical slots 1-5, fixed order
LABEL = {"84 settings": "84 settings, no repeats", "61 sets (now)": "60 settings + control, 21 pairs (now)",
         "42 x 2": "42 settings x 2", "28 x 3": "28 settings x 3", "21 x 4": "21 settings x 4 (identical squares)"}


def figure(summ: list[dict], path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = [r for r in summ if r["orientation"] == "none"]
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), constrained_layout=True)
    panels = (("map_rmse", "(a) Map error: RMS of ln(porosity)", None),
              ("boundary_wrong_pct", "(b) Window on the wrong side of 0.5 % porosity (%)", None),
              ("scatter_ratio", "(c) Scatter it estimates ÷ true scatter", None))
    xs = np.array(SIGMAS)
    for ax, (key, title, _) in zip(axes, panels):
        for name in DESIGNS:
            rs = sorted((r for r in base if r["design"] == name), key=lambda r: r["sigma"])
            color, marker = STYLE[name]
            if key == "scatter_ratio":
                med = np.array([r["scatter_ratio_median"] for r in rs])
                lo = np.array([r["scatter_ratio_p10"] for r in rs])
                hi = np.array([r["scatter_ratio_p90"] for r in rs])
                off = (DESIGNS.index(name) - 2) * 0.012
                ax.errorbar(xs + off, med, yerr=[med - lo, hi - med], color=color, marker=marker, ms=7,
                            lw=2, capsize=0, elinewidth=1.5, label=LABEL[name])
            else:
                ax.plot(xs, [r[key] for r in rs], color=color, marker=marker, ms=7, lw=2, label=LABEL[name])
        ax.set_title(title, fontsize=10.5, loc="left")
        ax.set_xlabel("wall-to-wall scatter σ in ln(porosity) (doubles on the boundary)", fontsize=9)
        ax.set_xticks(xs)
        ax.grid(color="#e6e5e0", lw=0.8)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[2].axhline(1.0, color="#8a8984", lw=1, ls="--", zorder=0)
    axes[2].set_ylabel(f"median, 10th–90th percentile of {N_TRIALS} trials", fontsize=9)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=5, frameon=False, fontsize=9)
    fig.text(0.5, -0.03, "Each design is 84 walls. Simulated truths around Eagar–Tsai + Tang's overlap rule "
             f"(boundary moved ×0.75–1.6), square offsets SD 0.15, GP fit as for the BO; medians of {N_TRIALS} trials. "
             "An illustration of the trade-off, not a prediction of the M2's scatter.",
             ha="center", fontsize=8.5, color="#55544f")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if "figure" in sys.argv[1:]:
        rows = list(csv.DictReader(open(OUT / "replicates_sim.csv", encoding="utf-8")))
    else:
        rows = run()
    summ = summary(rows)
    with open(OUT / "replicates_summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summ[0]))
        w.writeheader()
        w.writerows(summ)
    figure(summ, OUT / "m2-replicates.png")
    for r in summ:
        print(r)


if __name__ == "__main__":
    main()
