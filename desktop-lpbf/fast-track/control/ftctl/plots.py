"""Figure of one simulated build: O2, plate and block temperature, and where each layer's time goes.

python -m ftctl plot --height 2 --out ../img/sim-build-2mm.png
Colors: the dataviz reference palette's first three categorical slots (validated: adjacent CVD dE 12.6, normal 28.1;
contrast WARN on orange/aqua, so lines are direct-labelled and the data is in the HDF5 log as a table).
"""
from __future__ import annotations

import pathlib
import tempfile

import numpy as np

from .clock import SimClock
from .config import Config
from .hw.sim import make_sim_machine
from .logger import BuildLog, read_h5
from .supervisor import Supervisor

S1, S2, S3 = "#257de0", "#f47230", "#00b894"
INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"


def simulate(prog, n_layers, out_dir):
    cfg = Config()
    clock = SimClock()
    m = make_sim_machine(cfg, clock, prog.timing())
    log = BuildLog(out_dir, clock, "plotbuild")
    s = Supervisor(m, cfg, prog, log, clock).run(list(range(n_layers)))
    return cfg, s, read_h5(s["files"]["hdf5"])


def figure(prog, n_layers, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with tempfile.TemporaryDirectory() as d:
        cfg, s, h = simulate(prog, n_layers, d)
    sm, lay, ev = h["samples"], h["layers"], h["events"]
    t = sm["t"] / 60.0
    states = [(float(e["t"]) / 60.0, e["code"].decode() if isinstance(e["code"], bytes) else e["code"])
              for e in ev if (e["kind"].decode() if isinstance(e["kind"], bytes) else e["kind"]) == "state"]
    marks = {}
    for tt, code in states:
        if code in ("PURGE", "HEAT", "READY", "COOLDOWN", "VENT", "SAFE_TO_OPEN") and code not in marks:
            marks[code] = tt
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(11, 9.2))
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.05], hspace=0.42)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2])
    for ax in (ax1, ax2):
        ax.grid(True, color=GRID, lw=0.6)
        for code, tt in marks.items():
            ax.axvline(tt, color=INK2, lw=0.6, ls=":")
    for code, tt in marks.items():
        ax1.text(tt, 1.02, code.replace("_", " ").lower(), transform=ax1.get_xaxis_transform(), fontsize=7.5,
                 color=INK2, rotation=0, ha="left", va="bottom")
    # O2
    pct_ppm = sm["o2_pct"] * 1e4
    ax1.semilogy(t, pct_ppm, color=S2, lw=1.6, label="percent sensor (exhaust)")
    trace = np.where(sm["o2_ppm"] < cfg.gas.analyzer_range_ppm * 0.999, sm["o2_ppm"], np.nan)
    if "VENT" in marks:                                   # sample valve closed: the cell is isolated, not measuring
        trace = np.where(t < marks["VENT"], trace, np.nan)
    ax1.semilogy(t, trace, color=S1, lw=1.6, label="trace cell (sampling only below 1.5 %)")
    ax1.axhline(cfg.gas.o2_start_ppm, color=INK2, lw=0.8, ls="--")
    ax1.text(t[-1], cfg.gas.o2_start_ppm * 1.15, "1000 ppm: layers may start", fontsize=7.5, color=INK2, ha="right")
    ax1.axhline(cfg.gas.open_o2_ppm, color=INK2, lw=0.8, ls="--")
    ax1.text(t[-1], cfg.gas.open_o2_ppm * 0.6, "19.5 %: lid may open", fontsize=7.5, color=INK2, ha="right")
    ax1.set_ylabel("box O2 (ppm)")
    ax1.set_ylim(50, 4e5)
    ax1.legend(loc="center right", fontsize=8, frameon=False)
    ax1.set_title(f"Simulated FT-1 build: {n_layers} layers ({n_layers * prog.layer_mm:.2f} mm) of the first-coupon program, "
                  f"start-up to safe-to-open in {s['times_s']['total_s'] / 3600:.2f} h", fontsize=10, color=INK, loc="left",
                  pad=16)
    # temperatures
    ax2.plot(t, sm["plate_C"], color=S1, lw=1.4, label="plate (PID thermocouple)")
    ax2.plot(t, sm["block_C"], color=S2, lw=1.4, label="well block")
    ax2.plot(t, sm["box_air_C"], color=S3, lw=1.4, label="box air")
    sp = cfg.thermal.setpoint_C
    ax2.axhline(sp + cfg.thermal.dwell_band_K, color=INK2, lw=0.8, ls="--")
    ax2.text(t[0], sp + cfg.thermal.dwell_band_K + 3, f"{sp + cfg.thermal.dwell_band_K:.0f} C: dwell above this", fontsize=7.5,
             color=INK2)
    ax2.set_ylabel("temperature (C)")
    ax2.set_xlabel("time from start (min)")
    ax2.legend(loc="center right", fontsize=8, frameon=False)
    # per-layer split
    k = lay["layer"]
    rec, scan, dw = lay["recoat_s"], lay["scan_s"], lay["dwell_s"]
    w = 0.8
    ax3.bar(k, rec, w, color=S1, label="recoat (return, step, spread)", edgecolor="white", linewidth=0.6)
    ax3.bar(k, scan, w, bottom=rec, color=S2, label="scan (RTC5 list)", edgecolor="white", linewidth=0.6)
    ax3.bar(k, dw, w, bottom=rec + scan, color=S3, label="dwell (plate above 205 C)", edgecolor="white", linewidth=0.6)
    ax3.grid(True, axis="y", color=GRID, lw=0.6)
    ax3.set_axisbelow(True)
    ax3.set_xlabel("layer")
    ax3.set_ylabel("time per layer (s)")
    mean = (rec + scan + dw).mean()
    ax3.legend(loc="upper left", fontsize=8, frameon=False, ncol=3)
    ax3.set_ylim(0, max((rec + scan + dw).max() * 1.35, 1))
    ax3.text(k[-1], max((rec + scan + dw).max() * 1.13, 1), f"mean {mean:.1f} s a layer, {dw.mean() / mean * 100:.0f} % of it dwell",
             ha="right", fontsize=8, color=INK)
    out_png = pathlib.Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return s
