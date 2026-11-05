"""Sobol sweep of ArroyaveLab/eagar-tsai for AlSi10Mg, in SI units (issue #235).

A corrected version of the sweep that failed with
``Unable to allocate 762. GiB for an array with shape (301, 339693421)``.
It changes five things:

1. ``beam_diameter_m`` is in metres (25e-6 to 250e-6). The failed run passed the
   micrometre values 25 to 250, so eagar-tsai built a grid for a 25 to 250 m beam:
   it starts the grid 1.5 beam diameters ahead of the beam at 1 um spacing, which
   is 339,693,421 points for row 5 (226.46 "m"). ``check_units`` now refuses
   anything outside 1 um to 1 mm.
2. ``return_field=False``. The default (True) keeps both temperature planes for
   every row, about 3.3 MB per row at 1 um, which is 3.5 TB for 2**20 rows.
3. A 2 um grid (``--resolution-um``) instead of the default 1 um. That makes it 4x
   faster, and widths, depths and lengths change by at most 2.6 um (64-row check).
4. Rows run in resumable batches of ``--batch`` rows, with 32-row chunks inside
   each batch, instead of 2**20 one-row chunks and one CSV per row. Rerunning
   the script skips batches that are already on disk.
5. Rows whose domain expansion does not converge (the small-beam, slow, hot,
   high-absorptivity corner) are run again on a larger starting domain.
   Pass 1 logs an "Error in chunk ..." line for each of those rows.

On Linux, install eagar-tsai from source. The manylinux wheels of 0.6.0 link
``__exp_finite``, which current glibc does not export, so the C integrand fails to
import and eagar-tsai quietly uses its pure-Python integrand, about 20x slower.
The Windows, macOS and musllinux wheels are fine. This script warns if it hits that.

    python -m venv /tmp/etvenv
    /tmp/etvenv/bin/pip install --no-binary eagar-tsai eagar-tsai pandas scipy
    /tmp/etvenv/bin/python scripts/eagar_tsai_sobol_alsi10mg.py --m 12 --out sobol-m12

Measured on a 4-vCPU GitHub runner with the compiled integrand, the mean is
0.73 s per row at 2 um (1,024 rows), so --m 12 takes about 12 minutes and
--m 20 about 2.2 days on 4 workers.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import time

import numpy as np
import pandas as pd
from eagar_tsai import SimulationDomain, compute_melt_pool
from scipy.stats import qmc

# Sweep ranges from edison-trajectories/eagar-tsai-alsi10mg-inputs/README.md
# (branch claude/issue-235-20261104-1949), in eagar-tsai's SI units. The order
# matches the original script, so --m 20 --seed 42 reproduces its Sobol points.
BOUNDS = {
    "beam_diameter_m": (25e-6, 250e-6),  # 2*sigma = half the 1/e^2 spot. METRES.
    "power_w": (50.0, 400.0),
    "velocity_m_s": (0.1, 2.5),
    "absorptivity": (0.05, 0.7),
}
MATERIAL = {  # Edison's recommended AlSi10Mg values, held fixed
    "liquidus_temperature_k": 867.0,
    "thermal_conductivity_w_mk": 110.0,
    "density_kg_m3": 2650.0,
    "specific_heat_j_kgk": 1040.0,
}
# Starting domain (um) for rows that fail pass 1. The largest pool in the box
# (25 um beam, 400 W, 0.1 m/s, A = 0.7) is 900 x 450 x 1032 um (W x D x L).
RETRY_DOMAIN_UM = {"x_length_um": 1500.0, "y_length_um": 600.0, "z_depth_um": 500.0}
OUTPUTS = ["melt_length_um", "melt_width_um", "melt_depth_um", "peak_temperature"]


def sobol_design(m: int, seed: int) -> pd.DataFrame:
    """2**m scrambled Sobol points scaled to BOUNDS, with MATERIAL held fixed."""
    points = qmc.Sobol(d=len(BOUNDS), scramble=True, seed=seed).random_base2(m=m)
    low, high = zip(*BOUNDS.values(), strict=True)
    design = pd.DataFrame(qmc.scale(points, low, high), columns=list(BOUNDS))
    for name, value in MATERIAL.items():
        design[name] = value
    design.insert(0, "sample_id", np.arange(len(design)))
    return design


def check_units(design: pd.DataFrame) -> None:
    """Stop before eagar-tsai sizes a grid from a value in the wrong unit."""
    d = design["beam_diameter_m"]
    if not d.between(1e-6, 1e-3).all():
        raise ValueError(
            f"beam_diameter_m spans {d.min():g} to {d.max():g}; it must be in metres "
            "(e.g. 40e-6 for a 40 um 2-sigma beam, i.e. an 80 um 1/e^2 spot)."
        )
    if not design["velocity_m_s"].between(1e-3, 50).all():
        raise ValueError("velocity_m_s must be in m/s (e.g. 1.0, not 1000 mm/s).")
    if not design["absorptivity"].between(0, 1, inclusive="right").all():
        raise ValueError("absorptivity must be in (0, 1].")


def warn_if_slow_integrand() -> None:
    from scipy import LowLevelCallable

    try:
        from eagar_tsai._core import _INTEGRAND  # private; used only for this check
    except ImportError:
        return
    if not isinstance(_INTEGRAND, LowLevelCallable):
        print(
            "WARNING: eagar-tsai is using its pure-Python integrand (about 20x slower). On Linux run\n"
            "  pip install --force-reinstall --no-deps --no-binary eagar-tsai eagar-tsai\n"
            "(needs a C compiler and the Python headers).",
            flush=True,
        )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--m", type=int, default=12, help="run 2**m Sobol points (default 12 = 4,096)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--resolution-um", type=float, default=2.0, help="grid spacing (eagar-tsai default 1.0)")
    ap.add_argument("--batch", type=int, default=4096, help="rows per resumable batch file")
    ap.add_argument("--chunk-size", type=int, default=32, help="rows per worker task")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("eagar-tsai-sobol"))
    args = ap.parse_args()

    warn_if_slow_integrand()
    design = sobol_design(args.m, args.seed)
    check_units(design)
    batch_dir = args.out / "batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    design.to_csv(args.out / "sobol_params_si.csv", index=False)

    domain = SimulationDomain(spatial_resolution_um=args.resolution_um)
    # Keep at least 4 tasks per worker per batch, so a few slow rows don't idle the pool.
    chunk = max(1, min(args.chunk_size, min(args.batch, len(design)) // (4 * args.workers)))
    run = dict(chunk_size=chunk, workers=args.workers, return_field=False, show_progress=False)
    starts = range(0, len(design), args.batch)
    print(f"{len(design)} rows in {len(starts)} batch(es), {args.resolution_um} um grid, {args.workers} workers", flush=True)

    # Pass 1: resumable batches on the default-size domain.
    t_start, done_rows = time.perf_counter(), 0
    for b, start in enumerate(starts):
        path = batch_dir / f"batch_{b:05d}.csv"
        if path.exists():
            continue
        rows = design.iloc[start : start + args.batch]
        res = compute_melt_pool(rows, domain=domain, **run)
        res.to_csv(path.with_suffix(".tmp"), index=False)
        path.with_suffix(".tmp").replace(path)
        done_rows += len(rows)
        rate = (time.perf_counter() - t_start) / done_rows
        left_min = (len(design) - start - len(rows)) * rate / 60
        eta = f"{left_min:.0f} min" if left_min < 120 else f"{left_min / 60:.1f} h"
        print(f"batch {b + 1}/{len(starts)}: {rate:.2f} s/row wall, about {eta} left", flush=True)

    results = pd.concat([pd.read_csv(p) for p in sorted(batch_dir.glob("batch_*.csv"))], ignore_index=True)
    results = results.sort_values("sample_id").reset_index(drop=True)

    # Pass 2: rows whose domain expansion did not converge, on a larger start domain.
    failed = results["melt_width_um"].isna()
    if failed.any():
        print(f"pass 2: retrying {failed.sum()} row(s) on a larger domain", flush=True)
        retry_domain = SimulationDomain(spatial_resolution_um=args.resolution_um, **RETRY_DOMAIN_UM)
        retry = compute_melt_pool(results.loc[failed, design.columns], domain=retry_domain, **run)
        results.loc[failed, retry.columns] = retry.set_index(results.index[failed])

    results.to_csv(args.out / "melt_pool_results.csv", index=False)
    melted = results["melt_width_um"] > 0
    print(
        f"wrote {args.out / 'melt_pool_results.csv'}: {melted.sum()} melted, {(results['melt_width_um'] == 0).sum()} "
        f"below the liquidus, {results['melt_width_um'].isna().sum()} failed; "
        f"{(results.loc[melted, 'peak_temperature'] > 2743).sum()} melted rows peak above Al's boiling point (2743 K)",
        flush=True,
    )


if __name__ == "__main__":
    main()
