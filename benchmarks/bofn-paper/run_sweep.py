"""Run (policy x kappa x seed) cells in parallel; one JSON per cell, resumable.

    python run_sweep.py --kappas 1.0 --seeds 0-19 --kinds pkgfn eifn tiered ei random
    python run_sweep.py --policies ei --kappa 1 --seeds 0 --workers 1 --out /tmp/check   # one cell by hand
    python run_sweep.py --policies eifn --seeds 0-4 --costs L=1000 --noise 0.02 --out results-variants/L1000-noise0.02

The defaults are the stored runs' setup: the abstract's stage costs (C=10 A=1500
L=2500 T=200) and noise-free measurements. `--policies`/`--kinds` and
`--kappa`/`--kappas` are aliases. `--seeds` takes a range, a list or both
(`0-4`, `7`, `0,3,10-12`). `--costs` overrides single stages (`L=1000`).
`--noise` is the sd of Gaussian measurement noise on the three experiments, in
node-output units: one number for all three, or per stage (`A=0.01 L=0.05
T=0.02`); CALPHAD stays deterministic. Runs with non-default costs or noise must
go to their own `--out` folder.

Every JSON records the run's settings, the git commit (and whether tracked files
in this folder had uncommitted changes), the package versions and the command
line. An existing JSON is skipped, unless its recorded settings differ from the
requested ones, which is an error.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
KINDS = ("pkgfn", "pkgfn_la", "pkgfn_free", "kgfn", "eifn", "eifn_reuse", "ei", "tiered", "tiered_pu", "tiered_naive", "random")
STAGES, NOISY_STAGES = ("C", "A", "L", "T"), ("A", "L", "T")
PACKAGES = ("torch", "botorch", "gpytorch", "linear_operator", "numpy", "scipy")


def provenance():
    """Git commit, package versions and platform, read once in the parent process."""
    from importlib.metadata import PackageNotFoundError, version

    def git(*args):
        try:
            r = subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, timeout=30)
        except OSError:
            return None
        return r.stdout.strip() if r.returncode == 0 else None

    commit = git("rev-parse", "HEAD")
    # tracked files only, so result files the sweep itself writes do not count
    status = git("status", "--porcelain", "--untracked-files=no", "--", ".") if commit else None
    versions = {"python": platform.python_version()}
    for p in PACKAGES:
        try:
            versions[p] = version(p)
        except PackageNotFoundError:
            versions[p] = None
    cpu = None
    try:
        with open("/proc/cpuinfo") as f:
            cpu = next((ln.split(":", 1)[1].strip() for ln in f if ln.startswith("model name")), None)
    except OSError:
        pass
    return {
        "git": {"commit": commit, "dirty": None if status is None else bool(status)},
        "versions": versions,
        "platform": {"system": platform.platform(), "machine": platform.machine(), "cpu": cpu or platform.processor() or None},
        "argv": sys.argv[1:],
        "env": {k: v for k, v in os.environ.items() if k.startswith("BOFN_")},
    }


def cell(args):
    kind, kappa, seed, budget, out, costs, noise, prov = args
    warnings.filterwarnings("ignore")
    import torch

    torch.set_num_threads(1)
    import bofn_alloy
    from policies import run, settings

    path = Path(out) / f"k{kappa:g}" / f"{kind}_s{seed}.json"
    if path.exists():
        old = json.loads(path.read_text()).get("settings")
        if old:
            bofn_alloy.set_costs(costs)
            bofn_alloy.set_noise(noise)
            want = settings()
            clash = sorted(k for k in old if k in want and k != "torch_threads" and old[k] != want[k])
            if clash:
                raise RuntimeError(f"{path} exists with different settings ({', '.join(clash)}); use another --out")
        return str(path), 0.0
    t0 = time.time()
    res = run(kind, kappa, seed, budget, costs=costs, noise=noise)
    res["wall_s"] = time.time() - t0
    res["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    res.update(prov)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(res))
    return str(path), res["wall_s"]


def parse_seeds(spec):
    """'0-19', '7' or '0,3,10-12' -> sorted seeds."""
    seeds = set()
    for part in spec.replace(" ", "").split(","):
        lo, _, hi = part.partition("-")
        seeds.update(range(int(lo), int(hi or lo) + 1))
    return sorted(seeds)


def stage_values(items, flag, allowed, bare=None):
    """['L=1000', 'T=100'] -> {'L': 1000.0, 'T': 100.0}; a bare number applies to the stages in `bare`."""
    out = {}
    for item in items or []:
        key, eq, val = item.partition("=")
        if not eq:
            if not bare:
                raise SystemExit(f"{flag}: give stage=value pairs, e.g. {flag} L=1000")
            out.update({s: float(key) for s in bare})
            continue
        key = key.strip().upper()
        if key not in allowed:
            raise SystemExit(f"{flag}: unknown stage {key!r}; stages are {', '.join(allowed)}")
        out[key] = float(val)
    if any(v < 0 for v in out.values()):
        raise SystemExit(f"{flag}: values must be non-negative")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--policies", "--kinds", dest="kinds", nargs="+", default=["pkgfn", "eifn", "tiered", "ei", "random"], choices=KINDS)
    ap.add_argument("--kappas", "--kappa", dest="kappas", nargs="+", type=float, default=[1.0])
    ap.add_argument("--seeds", default="0-19", help="range and/or list, e.g. 0-19, 7 or 0,3,10-12")
    ap.add_argument("--costs", nargs="+", metavar="STAGE=USD", help="stage-cost overrides (default C=10 A=1500 L=2500 T=200)")
    ap.add_argument("--noise", nargs="+", metavar="SD|STAGE=SD", help="measurement-noise sd: one number for A, L and T, or per stage (default 0)")
    ap.add_argument("--budget", type=float, default=100_000)
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=str(OUT), help="results folder (default results/; use another folder for convergence checks)")
    a = ap.parse_args()
    costs = stage_values(a.costs, "--costs", STAGES)
    noise = stage_values(a.noise, "--noise", NOISY_STAGES, bare=NOISY_STAGES)
    if any(v <= 0 for v in costs.values()):
        raise SystemExit("--costs: costs must be positive")
    noise = {k: v for k, v in noise.items() if v > 0}
    if (costs or noise) and Path(a.out).resolve() == OUT.resolve():
        raise SystemExit("non-default --costs/--noise: pass an --out folder of their own, not the stored results/")
    prov = provenance()
    jobs = [(k, kap, s, a.budget, a.out, costs or None, noise or None, prov) for kap in a.kappas for s in parse_seeds(a.seeds) for k in a.kinds]
    with Pool(a.workers) as pool:
        for path, wall in pool.imap_unordered(cell, jobs):
            print(f"{time.strftime('%H:%M:%S')} {path} {wall:.0f}s", flush=True)


if __name__ == "__main__":
    main()
