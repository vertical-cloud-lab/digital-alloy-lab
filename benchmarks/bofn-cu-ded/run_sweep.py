"""Run (policy x cell x seed) jobs in parallel; one JSON per job, resumable.

    python run_sweep.py --cells 1,1 --seeds 0-19 --kinds pkgfn eifn eifn_reuse tiered ei random

A cell is (kappa, eta). Results go to results/k<kappa>e<eta>/<kind>_s<seed>.json.
"""

import argparse
import json
import os
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

OUT = Path(__file__).parent / "results"


def cell_dir(kappa, eta):
    return f"k{kappa:g}e{eta:g}"


def job(args):
    kind, kappa, eta, seed, budget, out = args
    warnings.filterwarnings("ignore")
    import torch

    torch.set_num_threads(1)
    from policies import run

    path = Path(out) / cell_dir(kappa, eta) / f"{kind}_s{seed}.json"
    if path.exists():
        return str(path), 0.0
    t0 = time.time()
    res = run(kind, kappa, eta, seed, budget)
    res["wall_s"] = time.time() - t0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(res))
    return str(path), res["wall_s"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="+", default=["1,1"], help="kappa,eta pairs")
    ap.add_argument("--seeds", default="0-19")
    ap.add_argument("--kinds", nargs="+", default=["pkgfn", "eifn", "eifn_reuse", "tiered", "ei", "random"])
    ap.add_argument("--budget", type=float, default=100_000)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=str(OUT), help="results folder (default results/; use another folder for convergence checks)")
    a = ap.parse_args()
    lo, hi = (int(v) for v in a.seeds.split("-"))
    cells = [tuple(float(v) for v in c.split(",")) for c in a.cells]
    jobs = [(k, kap, eta, s, a.budget, a.out) for (kap, eta) in cells for s in range(lo, hi + 1) for k in a.kinds]
    with Pool(a.workers) as pool:
        for path, wall in pool.imap_unordered(job, jobs):
            print(f"{time.strftime('%H:%M:%S')} {path} {wall:.0f}s", flush=True)


if __name__ == "__main__":
    main()
