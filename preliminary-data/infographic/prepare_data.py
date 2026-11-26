"""Rebuild the compact inputs in data/ from the branches they come from.

    git fetch origin
    python prepare_data.py

The commit each input was read at is pinned below, so the output does not change when those
branches move on. data/atomizer_runs.csv is written by hand from the run table (see README.md),
so it is not rebuilt here.
"""

import io
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

PSD = ("8dbae748fc4c343b08533cae1bb47ffcbd760d8a",  # PR #226
       "atomizer-runs/2026-10-27-nab-k7m2q9/psd/results/particles.csv")
BOFN = ("8401bbe61531fbd5461501e95a57d173538787bf",  # PR #122
        "benchmarks/bofn-paper/results/k1")
AG = [("253763da1b4afd61392b11a5928e2621772dff63",  # PR #192
       "scripts/airgradient/cb154_full_history_20260205_20260718.csv.gz"),
      ("c25f602352dd48713781c517ed964b1bad86a443",  # PR #188
       "scripts/airgradient/cb154_5min_20260718_20261003.csv.gz")]
OPTIMUM_K1 = 0.694  # objective at the kappa = 1 optimum (benchmarks/bofn-paper/README.md)
POLICIES = ["pkgfn", "eifn_reuse", "eifn", "tiered", "ei", "random"]


def show(sha, path):
    return subprocess.check_output(["git", "show", f"{sha}:{path}"])


def particles():
    p = pd.read_csv(io.BytesIO(show(*PSD)))
    p = p[p["included"]]  # the 5,937 counted particles (counted + flagged)
    cols = ["field", "ecd_um", "weight", "circularity", "aspect_ratio"]
    p[cols].round(4).to_csv(DATA / "k7m2q9_particles.csv", index=False)


def bofn():
    grid = np.linspace(0, 100_000, 401)
    out = {}
    for pol in POLICIES:
        curves = []
        for seed in range(20):
            d = json.loads(show(BOFN[0], f"{BOFN[1]}/{pol}_s{seed}.json"))
            spent = np.array([r["spent"] for r in d["rows"]])
            best = np.maximum.accumulate(np.nan_to_num(
                np.array([r["best_validated"] for r in d["rows"]], dtype=float), nan=0.0))
            idx = np.clip(np.searchsorted(spent, grid, side="right") - 1, 0, None)
            curves.append(best[idx] / OPTIMUM_K1 * 100)
        c = np.array(curves)
        out[f"{pol}_mean"] = c.mean(0).round(3)
        out[f"{pol}_se"] = (c.std(0, ddof=1) / np.sqrt(len(c))).round(3)
    cols = [f"{p}_mean" for p in POLICIES] + [f"{p}_se" for p in POLICIES]
    pd.DataFrame({"spend_usd": grid, **{k: out[k] for k in cols}}).to_csv(
        DATA / "bofn_k1_best_vs_spend.csv", index=False)


def airgradient():
    use = ["timestamp", "pm02_corrected", "atmp_corrected", "rhum_corrected", "rco2_corrected"]
    ag = pd.concat([pd.read_csv(io.BytesIO(show(*src)), compression="gzip", usecols=use)
                    for src in AG])
    ag["timestamp"] = pd.to_datetime(ag["timestamp"], utc=True)
    ag = ag.drop_duplicates("timestamp").sort_values("timestamp").set_index("timestamp")
    d = ag.resample("1D").agg(["mean", "min", "max", "count"])
    d.columns = ["_".join(c) for c in d.columns]
    d = d[d["rhum_corrected_count"] > 0]
    keep = ["rhum_corrected_mean", "rhum_corrected_min", "rhum_corrected_max",
            "atmp_corrected_mean", "pm02_corrected_mean", "pm02_corrected_max",
            "rco2_corrected_mean", "rhum_corrected_count"]
    d[keep].round(2).to_csv(DATA / "airgradient_cb154_daily.csv")


if __name__ == "__main__":
    particles()
    bofn()
    airgradient()
