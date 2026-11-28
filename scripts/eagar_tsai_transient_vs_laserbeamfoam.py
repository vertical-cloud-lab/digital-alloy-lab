"""eagar-tsai's time-dependent pool against #249's laserbeamFoam runs, at the same absorbed power and time (#235).

#249 (stacked on #238) ran laserbeamFoam at the AM module's melt-pool points: 7 runs, 0.8-1.6 ms of
track each, 15-25 um cells. Its tables compare each run's pool, averaged over the second half of the
run, with eagar-tsai's *steady* pool. But the CFD pools were still growing when the runs stopped, and
eagar-tsai's own pool takes 0.5-2.8 ms to reach its steady length (#238's time-dependent eagar-tsai,
``eagar_tsai_transient_meltpool.py``). This script compares the two at the same time after switch-on.

Everything is set the way the CFD was: the absorbed power each run actually logged (summed over the run's
history, so the 65 uOhm cm run's switch from dimple to keyhole is included), the beam's 1/e^2 radius as
eagar-tsai's ``beam_diameter``, the plate temperature as T0, the same constant k, rho and c_p
(110 W/m/K, 2650 kg/m^3, 1040 J/kg/K), and the CFD's own liquidus and solidus (mc_al). So what differs is
the physics laserbeamFoam adds: latent heat, melt flow, evaporation, a free surface that can open a keyhole,
and its finite domain and mesh.

The beam switches on at X = 0 and never switches off. With absorbed power Q(s) at time s after switch-on,
eagar-tsai's field is linear in power, so

    T - T0 = S1 * sum_k Q_k * integral_{v (tau - s_k,hi) / sigma}^{v (tau - s_k,lo) / sigma} f(t; x, y, z, p) dt

over piecewise-constant bins of Q (50 us; bins within 0.5 % of each other are merged, so a constant-power
run is one bin), with f eagar-tsai's compiled integrand and S1 its prefactor per absorbed watt.

``--self-check`` first reproduces three rows of #238's committed transient history with this code, and
checks that splitting a constant power into bins changes nothing.

    # #249's results, from its branch at cc25b6f (after #249 merges: arroyave-orchid-tools/keyhole-alternatives/cfd)
    git fetch origin claude/issue-235-keyhole-open-alternatives
    mkdir -p /tmp/lbf && git archive cc25b6f arroyave-orchid-tools/keyhole-alternatives/cfd | tar -x -C /tmp/lbf
    python scripts/eagar_tsai_transient_vs_laserbeamfoam.py --self-check \\
        --cfd-dir /tmp/lbf/arroyave-orchid-tools/keyhole-alternatives/cfd \\
        --out arroyave-orchid-tools/eagar-tsai/am-module-inhouse/transient/vs-laserbeamfoam
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from eagar_tsai_transient_meltpool import Model, _grid, pool_dims  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[1]
RUNS = {  # run -> (panel title, mode)
    "alsi10mg-fresnel": ("AlSi10Mg 250 W, 0.9 m/s\nlaserbeamFoam's own Fresnel A (40 µΩ cm)", "conduction"),
    "blend-fresnel": ("Blend 375 W, 0.4 m/s\nlaserbeamFoam's own Fresnel A (40 µΩ cm)", "conduction"),
    "alsi10mg-matchedA": ("AlSi10Mg 250 W, 0.9 m/s\nabsorbed power = AM module's A·P", "dimple"),
    "alsi10mg-350W-matchedA": ("AlSi10Mg 350 W, 0.9 m/s\nabsorbed power = AM module's A·P", "keyhole"),
    "blend-matchedA": ("Blend 375 W, 0.4 m/s\nabsorbed power = AM module's A·P", "keyhole"),
    "blend-matchedA-25um": ("Blend 375 W, 0.4 m/s, 25 µm mesh\nabsorbed power = AM module's A·P", "keyhole"),
    "blend-fresnel-rho65": ("Blend 375 W, 0.4 m/s\nFresnel A at 65 µΩ cm (dimple, then keyhole)", "keyhole"),
}
SOURCES = {"original": "", "rerun": "rerun-2026-11-27"}
DIMS = ("D", "W", "L")
BIN_S = 50e-6
DX = 2e-6


# --------------------------------------------------------------------------------------------
# eagar-tsai with a power history
# --------------------------------------------------------------------------------------------
def model_for(meta: dict) -> Model:
    """eagar-tsai's scalings for a CFD run, per absorbed watt (A = 1, P = 1)."""
    p = meta["props"]
    c = dict(R_um=meta["r0"] * 1e6, P=1.0, v=meta["v"], A=1.0, k=p["k"], rho=p["rho"], cp=p["cp"],
             T_plate=meta["T0"], track_mm=1e6, isotherms=[(meta["T_l"], "liquidus", "-"), (meta["T_s"], "solidus", "--")])
    return Model(c)


def planes(m: Model, tau: float | None, bins: list, X: np.ndarray, Y: np.ndarray, Zd: np.ndarray):
    """Surface (Y x X) and centre-line (Zd x X) temperatures at tau after switch-on (None = steady).

    bins: [(s_lo, s_hi, Q_W)], the absorbed power deposited between s_lo and s_hi after switch-on.
    The beam is at X = v * tau; for the steady state (tau None) it is at X = 0 and bins must be one entry.
    """
    T_top = np.zeros((Y.size, X.size))
    T_side = np.zeros((Zd.size, X.size))
    xb = 0.0 if tau is None else m.v * tau
    for s_lo, s_hi, Q in bins:
        if tau is None:
            t_lo, t_hi = 0.0, math.inf
        else:
            if s_lo >= tau:
                break
            t_lo = m.v * (tau - min(s_hi, tau)) / m.sigma
            t_hi = m.v * (tau - s_lo) / m.sigma
        for ix, Xi in enumerate(X):
            x_nd = (xb - Xi) / m.sigma
            for iy, Yi in enumerate(Y):
                T_top[iy, ix] += Q * m.integral(x_nd, Yi / m.sigma, 0.0, t_lo, t_hi)
            for iz in range(1, Zd.size):
                T_side[iz, ix] += Q * m.integral(x_nd, 0.0, Zd[iz] / m.z_scale, t_lo, t_hi)
    T_side[0] = T_top[0]
    return m.T0 + m.S * T_top, m.T0 + m.S * T_side  # m.S is the prefactor per absorbed watt here


def power_bins(q: pd.DataFrame, t_end: float) -> list:
    """Piecewise-constant absorbed power from a run's log, in BIN_S bins, near-equal neighbours merged."""
    q = q.sort_values("t").drop_duplicates("t", keep="last")
    t = q["t"].to_numpy()
    Q = q["Q"].to_numpy()
    seg_lo = np.r_[0.0, t[:-1]]
    edges = np.arange(0.0, t_end + BIN_S, BIN_S)
    out = []
    for lo, hi in zip(edges[:-1], edges[1:], strict=True):
        overlap = np.clip(np.minimum(t, hi) - np.maximum(seg_lo, lo), 0, None)
        if overlap.sum() <= 0:
            continue
        Qb = float((Q * overlap).sum() / overlap.sum())
        if out and abs(Qb - out[-1][2]) <= 0.005 * out[-1][2]:
            out[-1] = (out[-1][0], hi, out[-1][2])  # merge (keeps the first bin's power)
        else:
            out.append((lo, hi, Qb))
    out[-1] = (out[-1][0], math.inf, out[-1][2])  # hold the last power beyond the log
    return out


def _job(args):
    run, source, meta, bins, tau, win = args
    m = model_for(meta)
    if tau is None:
        X = _grid(-win["back"], win["front"], DX)
    else:
        xb = m.v * tau
        X = _grid(xb - win["back"], xb + win["front"], DX)
        X = X[X >= -0.1e-3]  # heat diffuses back past the switch-on point, but not far
    Y = _grid(0.0, win["half_w"], DX)
    Zd = _grid(0.0, win["depth"], DX)
    t0 = time.time()
    Tt, Ts = planes(m, tau, bins, X, Y, Zd)
    Q_now = bins[0][2] if tau is None else next(Q for lo, hi, Q in bins if lo <= tau < hi or hi == math.inf)
    row = dict(run=run, source=source, t_ms=np.inf if tau is None else tau * 1e3, absorbed_W=Q_now,
               seconds=time.time() - t0)
    for tag, T_iso in (("liquidus", meta["T_l"]), ("solidus", meta["T_s"])):
        d = pool_dims(X, Y, Zd, Tt, Ts, T_iso)
        row.update({f"et_{k[0]}_{tag}_um": d[f"{k[0]}_um"] for k in ("L", "W", "D")})
        row[f"et_touches_window_{tag}"] = d["touches_window_edge"]
    return row


def window_for(meta: dict, Q_max: float) -> dict:
    """A plane window that holds eagar-tsai's steady solidus pool at the run's largest absorbed power."""
    m = model_for(meta)
    X = _grid(-2.5e-3, 0.3e-3, 5e-6)
    Y = _grid(0.0, 0.6e-3, 5e-6)
    Zd = _grid(0.0, 0.6e-3, 5e-6)
    Tt, Ts = planes(m, None, [(0.0, math.inf, Q_max)], X, Y, Zd)
    d = pool_dims(X, Y, Zd, Tt, Ts, meta["T_s"])
    assert not d["touches_window_edge"], "steady pool doesn't fit the sizing window"
    pad = 25e-6
    return dict(back=-d["x_back_um"] * 1e-6 * 1.15 + pad, front=max(d["x_front_um"] * 1e-6, 0) + pad,
                half_w=d["W_um"] / 2 * 1e-6 * 1.15 + pad, depth=d["D_um"] * 1e-6 * 1.15 + pad)


# --------------------------------------------------------------------------------------------
# self-check against #238's committed transient history
# --------------------------------------------------------------------------------------------
def self_check() -> None:
    from eagar_tsai_transient_meltpool import CASES

    hist = pd.read_csv(REPO / "arroyave-orchid-tools/eagar-tsai/am-module-inhouse/transient/eagar-tsai-transient-history.csv")
    c = CASES["alsi10mg"]
    meta = dict(r0=c["R_um"] * 1e-6, v=c["v"], T0=c["T_plate"], T_l=c["isotherms"][0][0], T_s=c["isotherms"][1][0],
                props=dict(k=c["k"], rho=c["rho"], cp=c["cp"]))
    m = model_for(meta)
    Q = c["A"] * c["P"]
    h = hist[(hist["case"] == "alsi10mg") & hist["beam_on"]]
    for tau_us in (100.0, 300.0, 1000.0):
        r = h.iloc[(h["tau_us"] - tau_us).abs().argmin()]
        tau = r["tau_us"] * 1e-6
        xb = m.v * tau
        X = _grid(xb - 0.75e-3, xb + 0.2e-3, 2e-6)
        X = X[X >= -0.1e-3]
        Y, Zd = _grid(0, 0.26e-3, 2e-6), _grid(0, 0.22e-3, 2e-6)
        Tt, Ts = planes(m, tau, [(0.0, math.inf, Q)], X, Y, Zd)
        d = pool_dims(X, Y, Zd, Tt, Ts, 867.0)
        diff = max(abs(d["L_um"] - r["L_um_liquidus"]), abs(d["W_um"] - r["W_um_liquidus"]), abs(d["D_um"] - r["D_um_liquidus"]))
        print(f"self-check vs #238's history at {r['tau_us']:.1f} us: L/W/D {d['L_um']:.3f}/{d['W_um']:.3f}/{d['D_um']:.3f} "
              f"against {r['L_um_liquidus']}/{r['W_um_liquidus']}/{r['D_um_liquidus']} (max diff {diff:.4f} um)", flush=True)
        assert diff < 0.01, "doesn't reproduce #238's committed transient history"
    # linearity: a constant power split into four bins must give the same field
    tau = 300e-6
    X = _grid(m.v * tau - 0.3e-3, m.v * tau + 0.05e-3, 10e-6)
    Y, Zd = _grid(0, 0.1e-3, 10e-6), _grid(0, 0.1e-3, 10e-6)
    one = planes(m, tau, [(0.0, math.inf, Q)], X, Y, Zd)
    four = planes(m, tau, [(0.0, 75e-6, Q), (75e-6, 150e-6, Q), (150e-6, 225e-6, Q), (225e-6, math.inf, Q)], X, Y, Zd)
    err = max(float(np.abs(a - b).max()) for a, b in zip(one, four, strict=True))
    print(f"self-check: one bin vs four bins, max |dT| = {err:.2e} K", flush=True)
    assert err < 1e-3


# --------------------------------------------------------------------------------------------
# run everything
# --------------------------------------------------------------------------------------------
def load(cfd_dir: pathlib.Path, source: str, run: str):
    d = cfd_dir / SOURCES[source]
    s = json.loads((d / f"{run}-summary.json").read_text())
    return s, pd.read_csv(d / f"{run}-pool-vs-time.csv"), pd.read_csv(d / f"{run}-absorbed-power-vs-time.csv")


def compute(cfd_dir: pathlib.Path, workers: int) -> pd.DataFrame:
    jobs, info = [], {}
    for run in RUNS:
        bins_by_source = {}
        for source in SOURCES:
            s, pool, q = load(cfd_dir, source, run)
            bins_by_source[source] = (power_bins(q, s["t_end_reached_ms"] * 1e-3), pool, s)
        meta = bins_by_source["original"][2]["meta"]
        Q_max = max(b[2] for bins, _, _ in bins_by_source.values() for b in bins)
        win = window_for(meta, Q_max)
        info[run] = dict(window_um={k: round(v * 1e6, 1) for k, v in win.items()}, Q_max_W=round(Q_max, 2))
        (b_o, pool_o, s_o), (b_r, pool_r, _) = bins_by_source["original"], bins_by_source["rerun"]
        # the same power history (to 0.1 %) gives the same eagar-tsai pool, so the rerun reuses the original's
        same = len(b_o) == len(b_r) and all(abs(x[2] - y[2]) <= 1e-3 * x[2] for x, y in zip(b_o, b_r, strict=True))
        t_end = s_o["t_end_reached_ms"] * 1e-3
        taus = set(np.round(pool_o["t_ms"].to_numpy() * 1e-3, 9))
        taus |= set(np.round(np.r_[np.array([10, 20, 35]) * 1e-6, np.linspace(0, t_end, 17)[1:]], 9))  # a smooth line
        if same:
            taus |= set(np.round(pool_r["t_ms"].to_numpy() * 1e-3, 9))
        else:
            jobs += [(run, "rerun", meta, b_r, float(t), win) for t in sorted(set(np.round(pool_r["t_ms"].to_numpy() * 1e-3, 9)))]
        jobs += [(run, "original", meta, b_o, float(t), win) for t in sorted(taus)]
        # steady pool at the second-half mean absorbed power, as #249's tables use
        s0 = bins_by_source["original"][2]
        jobs.append((run, "steady", meta, [(0.0, math.inf, s0["A_eff_mean_second_half"] * meta["P"])], None, win))
        info[run]["bins"] = {src: len(v[0]) for src, v in bins_by_source.items()}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(_job, jobs, chunksize=1))
    print(f"{len(jobs)} eagar-tsai fields in {time.time() - t0:.0f} s on {workers} workers", flush=True)
    return pd.DataFrame(rows), info


def compare(cfd_dir: pathlib.Path, et: pd.DataFrame) -> pd.DataFrame:
    """One row per CFD write: the CFD pool next to eagar-tsai's at the same time."""
    out = []
    for run in RUNS:
        for source in SOURCES:
            s, pool, q = load(cfd_dir, source, run)
            e_src = source if ((et.run == run) & (et.source == source)).any() else "original"
            e = et[(et.run == run) & (et.source == e_src)]
            e = e.set_index(np.round(e["t_ms"].to_numpy(), 6))
            st = et[(et.run == run) & (et.source == "steady")].iloc[0]
            # the log has every few steps, so weight each logged power by the time since the previous entry
            qq = q.sort_values("t").drop_duplicates("t", keep="last")
            energy = np.cumsum(qq["Q"].to_numpy() * np.diff(np.r_[0.0, qq["t"].to_numpy()]))
            for _, r in pool.iterrows():
                er = e.loc[round(r["t_ms"], 6)]
                t_s = r["t_ms"] * 1e-3
                row = dict(run=run, source=source, t_ms=r["t_ms"],
                           absorbed_W_mean_so_far=float(np.interp(t_s, qq["t"], energy) / t_s),
                           keyhole_depth_um=r.get("keyhole_depth_um", np.nan),
                           pool_back_touches_domain_start=bool(r["pool_back_touches_domain_start"]))
                for tag, sfx in (("liquidus", ""), ("solidus", "_solidus")):
                    for dim, col in (("D", "pool_depth"), ("W", "pool_width"), ("L", "pool_length")):
                        cfd = r[f"{col}{sfx}_um"]
                        row[f"cfd_{dim}_{tag}_um"] = cfd
                        row[f"et_{dim}_{tag}_um"] = er[f"et_{dim}_{tag}_um"]
                        row[f"et_steady_{dim}_{tag}_um"] = st[f"et_{dim}_{tag}_um"]
                    row[f"et_touches_window_{tag}"] = bool(er[f"et_touches_window_{tag}"])
                out.append(row)
    return pd.DataFrame(out)


def summarize(cmp_: pd.DataFrame, cfd_dir: pathlib.Path) -> dict:
    """Second-half means (as #249's tables) and the last write, CFD vs eagar-tsai at equal time and steady."""
    res = {}
    for run in RUNS:
        res[run] = {}
        for source in SOURCES:
            s, _, _ = load(cfd_dir, source, run)
            d = cmp_[(cmp_.run == run) & (cmp_.source == source)]
            t_end = d.t_ms.max()
            half = d[d.t_ms > t_end / 2 + 1e-9]
            r = dict(t_end_ms=t_end, absorbed_fraction_second_half=round(s["A_eff_mean_second_half"], 4),
                     second_half_writes=len(half))
            for tag in ("liquidus", "solidus"):
                for dim in DIMS:
                    cfd = half[f"cfd_{dim}_{tag}_um"].mean()
                    et_t = half[f"et_{dim}_{tag}_um"].mean()
                    et_s = half[f"et_steady_{dim}_{tag}_um"].iloc[0]
                    last = d[d.t_ms == t_end].iloc[0]
                    r[f"{dim}_{tag}"] = dict(
                        cfd_second_half_um=round(cfd, 1), et_same_times_um=round(et_t, 1), et_steady_um=round(et_s, 1),
                        cfd_over_et_same_times=round(cfd / et_t, 3), cfd_over_et_steady=round(cfd / et_s, 3),
                        et_same_times_over_steady=round(et_t / et_s, 3),
                        last_write=dict(cfd_um=round(last[f"cfd_{dim}_{tag}_um"], 1), et_um=round(last[f"et_{dim}_{tag}_um"], 1)))
            res[run][source] = r
    return res


# --------------------------------------------------------------------------------------------
# figure
# --------------------------------------------------------------------------------------------
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
COL = {"L": "#2a78d6", "W": "#eb6834", "D": "#1baf7a"}  # as in #238's transient history plot
NAME = {"L": "length", "W": "width", "D": "depth"}


def figure(cmp_: pd.DataFrame, et: pd.DataFrame, out: pathlib.Path, tag: str = "liquidus") -> None:
    fig, axes = plt.subplots(2, 4, figsize=(16, 8.6))
    fig.patch.set_facecolor(SURF)
    for ax, run in zip(axes.flat, RUNS, strict=False):
        ax.set_facecolor(SURF)
        e = et[(et.run == run) & (et.source == "original")].sort_values("t_ms")
        st = et[(et.run == run) & (et.source == "steady")].iloc[0]
        t_end = e.t_ms.max()
        for dim in ("L", "W", "D"):
            c = COL[dim]
            ax.plot(np.r_[0.0, e.t_ms], np.r_[0.0, e[f"et_{dim}_{tag}_um"]], color=c, lw=2, solid_capstyle="round", zorder=3)
            ax.plot([t_end * 0.8, t_end * 1.04], [st[f"et_{dim}_{tag}_um"]] * 2, color=c, lw=1.2, ls=(0, (2, 2)), zorder=2)
            for source, face in (("original", c), ("rerun", SURF)):
                d = cmp_[(cmp_.run == run) & (cmp_.source == source)]
                ax.plot(d.t_ms, d[f"cfd_{dim}_{tag}_um"], ls="none", marker="o", ms=6.5, mfc=face, mec=c, mew=1.6,
                        zorder=4 if source == "original" else 5)
            y_end = e[f"et_{dim}_{tag}_um"].iloc[-1]
            ax.annotate(dim, (e.t_ms.iloc[-1], y_end), xytext=(10, 0), textcoords="offset points", va="center",
                        color=INK, fontsize=10, fontweight="bold")
        title, _mode = RUNS[run]
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
        ax.set_xlim(0, t_end * 1.12)
        ax.set_ylim(0, None)
        ax.grid(True, color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(INK2)
        ax.tick_params(colors=INK2, labelsize=8.5)
        ax.set_xlabel("time since switch-on (ms)", fontsize=8.5, color=INK2)
        ax.set_ylabel(f"pool at the {tag} (µm)", fontsize=8.5, color=INK2)
        note = (f"absorbed {st['absorbed_W']:.0f} W\n(second-half mean; {e['absorbed_W'].iloc[0]:.0f} W at first)"
                if run.endswith("rho65") else f"absorbed {st['absorbed_W']:.0f} W")
        ax.text(0.02, 0.97, note, transform=ax.transAxes, va="top", fontsize=8.5, color=INK2)
    lg = axes.flat[-1]
    lg.axis("off")
    from matplotlib.lines import Line2D

    handles = [Line2D([], [], color=INK2, lw=2, label="eagar-tsai, time-dependent (#238)"),
               Line2D([], [], color=INK2, lw=1.2, ls=(0, (2, 2)), label="eagar-tsai, steady"),
               Line2D([], [], ls="none", marker="o", ms=6.5, mfc=INK2, mec=INK2, label="laserbeamFoam (#249)"),
               Line2D([], [], ls="none", marker="o", ms=6.5, mfc=SURF, mec=INK2, mew=1.6, label="laserbeamFoam rerun, 2026-11-27"),
               ] + [Line2D([], [], color=COL[d], lw=2, label=f"{d}: pool {NAME[d]}") for d in ("L", "W", "D")]
    lg.legend(handles=handles, loc="upper left", frameon=False, fontsize=9.5, labelcolor=INK)
    lg.text(0.0, 0.32, "Same absorbed power (the run's own log), beam,\nplate temperature, k, ρ, c_p and liquidus.\n"
            "eagar-tsai has no latent heat, flow, evaporation\nor keyhole; laserbeamFoam has all four.",
            transform=lg.transAxes, va="top", fontsize=8.8, color=INK2)
    fig.suptitle(f"Melt pool at the {tag} against time: #249's laserbeamFoam runs and eagar-tsai at the same absorbed power",
                 x=0.01, ha="left", fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out / f"eagar-tsai-vs-laserbeamfoam-{tag}.png", dpi=130, facecolor=SURF)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cfd-dir", type=pathlib.Path, required=True, help="#249's arroyave-orchid-tools/keyhole-alternatives/cfd")
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--replot", action="store_true", help="redraw from the committed CSVs only")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    if a.replot:
        et = pd.read_csv(a.out / "eagar-tsai-at-laserbeamfoam-times.csv")
        cmp_ = pd.read_csv(a.out / "laserbeamfoam-vs-eagar-tsai-per-write.csv")
    else:
        if a.self_check:
            self_check()
        et, info = compute(a.cfd_dir, a.workers)
        et.round(3).to_csv(a.out / "eagar-tsai-at-laserbeamfoam-times.csv", index=False)
        cmp_ = compare(a.cfd_dir, et)
        cmp_.round(3).to_csv(a.out / "laserbeamfoam-vs-eagar-tsai-per-write.csv", index=False)
        summ = dict(cfd_source="#249 branch claude/issue-235-keyhole-open-alternatives at cc25b6f, cfd/ and cfd/rerun-2026-11-27/",
                    eagar_tsai="0.6.0, compiled integrand, 2 um planes; power history in 50 us bins", runs=info,
                    any_eagar_tsai_pool_touching_window=bool(cmp_.filter(like="et_touches_window").any().any()),
                    any_cfd_pool_touching_domain_start=bool(cmp_["pool_back_touches_domain_start"].any()),
                    comparison=summarize(cmp_, a.cfd_dir))
        (a.out / "summary.json").write_text(json.dumps(summ, indent=1))
    for tag in ("liquidus", "solidus"):
        figure(cmp_, et, a.out, tag)


if __name__ == "__main__":
    main()
