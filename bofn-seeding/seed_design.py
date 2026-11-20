#!/usr/bin/env python3
"""Pick space-filling seed compositions around the points already chosen (#275).

#275 suggests taking Sobol points but throwing out the ones that land too close to existing
experiments. This script does that, plus two more model-based variants, in the space a GP
with a ``Normalize`` input transform over the design box would see (each element's wt%
divided by its upper bound):

- ``sobol``: the first n feasible points of a scrambled Sobol sequence. Ignores the existing
  points; this is the plain baseline.
- ``sobol-exclusion``: walk the same Sobol sequence and skip any point closer than ``--radius``
  to an existing or already-picked point (the heuristic in #275).
- ``maximin``: greedy maximin augmentation over a large Sobol candidate pool. Each pick is the
  candidate farthest from its nearest existing or picked point.
- ``imse`` (default): greedy integrated-variance reduction. Each pick is the candidate that most
  lowers the average posterior variance of a GP (RBF kernel, fixed length scale) over the whole
  feasible pool, given the existing and picked points. Before any outcome is measured the GP
  variance depends only on where the points are, so this needs no data. Unlike maximin it
  doesn't push every pick into a corner of the box.

The design space follows the finalized element bounds on PR #72 (Edison task ``caec5419``):
Al balance at least 85 wt%, the recommended upper bound per element, a 0.10 wt% floor for any
element that is switched on, and the joint caps (Mn+Cr <= 7, Sc+Zr <= 1.5, Cu+Mg <= 5,
Cu+Li <= 4, Mg+Zn+Li <= 10 wt%). Mg+Si <= 6 is left out on purpose, because AlSi10Mg, the
benchmark, breaks it. Each candidate has at most ``--k-max`` additions (sparse sub-systems)
and at least ``--min-total`` wt% of additions in all (default 3; 6063 has about 1, the
Scalmalloy-type benchmark about 6, AlSi10Mg about 10).

Existing points come from ``seeds.csv`` (baselines, dosing checks, agent picks; use measured
compositions once there are any). The default element set is what is on hand or shipping per
#146 on 2026-11-13: Mn, Cr, Mg, Ti, Er and Zn from ESPI, plus Si through 4047 powder. Sn (cap
0.1 wt%) and Sc (the mineral the campaign is trying to avoid; D2 already covers it) are left
out. Add Zr with ``--elements ... Zr`` once it is on the shelf.

After the CALPHAD screen, pick in descriptor space instead of composition space, since that
is what the downstream nodes take as input:

    python bofn-seeding/seed_design.py --candidates screen.csv --features freezing_range csc

``screen.csv`` needs the feature columns, and an ``existing`` column set to 1 on the rows
that are already chosen (benchmarks, agent picks).

Usage:
    python bofn-seeding/seed_design.py                     # 3 picks, imse, default elements
    python bofn-seeding/seed_design.py --n 4 --method maximin
    python bofn-seeding/seed_design.py --compare           # every method, averaged over scrambles
"""

from __future__ import annotations

import argparse
import csv
import itertools
import pathlib
import sys

import numpy as np
from scipy.stats import qmc

HERE = pathlib.Path(__file__).resolve().parent

PALETTE = ["Mn", "Cr", "Zr", "Mg", "Si", "Cu", "Ti", "Fe", "Ni", "Ce", "Sc", "Li", "Er", "Zn", "Sn"]
# Recommended upper bounds in wt% (PR #72, "02_finalized_bounds_table.md").
UPPER_WT = {
    "Mn": 5.0, "Cr": 3.0, "Zr": 1.0, "Mg": 5.0, "Si": 12.0, "Cu": 4.0, "Ti": 0.5, "Fe": 0.5,
    "Ni": 0.5, "Ce": 6.0, "Sc": 0.8, "Li": 2.0, "Er": 0.5, "Zn": 8.0, "Sn": 0.1,
}
AL_MIN_WT = 85.0
FLOOR_WT = 0.10
JOINT_CAPS = [
    (("Mn", "Cr"), 7.0),
    (("Sc", "Zr"), 1.5),
    (("Cu", "Mg"), 5.0),
    (("Cu", "Li"), 4.0),
    (("Mg", "Zn", "Li"), 10.0),
]
ATOMIC_WEIGHT = {
    "Al": 26.982, "Mn": 54.938, "Cr": 51.996, "Zr": 91.224, "Mg": 24.305, "Si": 28.085,
    "Cu": 63.546, "Ti": 47.867, "Fe": 55.845, "Ni": 58.693, "Ce": 140.116, "Sc": 44.956,
    "Li": 6.94, "Er": 167.259, "Zn": 65.38, "Sn": 118.71,
}
DEFAULT_ELEMENTS = ["Mn", "Cr", "Mg", "Si", "Er", "Ti", "Zn"]
UB = np.array([UPPER_WT[e] for e in PALETTE])
IDX = {e: i for i, e in enumerate(PALETTE)}
METHODS = ["sobol", "sobol-exclusion", "maximin", "imse"]


# --------------------------------------------------------------------------- design space
def feasible(W: np.ndarray, min_total: float = 0.0, tol: float = 1e-9) -> np.ndarray:
    """Rows of W (wt% of each palette element) that satisfy the bounds and joint caps."""
    ok = (W <= UB + tol).all(axis=1) & (W >= -tol).all(axis=1)
    ok &= W.sum(axis=1) <= 100.0 - AL_MIN_WT + tol
    ok &= W.sum(axis=1) >= min_total - tol
    ok &= ((W == 0) | (W >= FLOOR_WT - tol)).all(axis=1)
    for elements, cap in JOINT_CAPS:
        ok &= W[:, [IDX[e] for e in elements]].sum(axis=1) <= cap + tol
    return ok


def candidate_pool(elements, k_min, k_max, per_subsystem, seed, min_total=0.0):
    """Feasible sparse compositions, interleaved across sub-systems in Sobol order.

    Every sub-system (k additions out of ``elements``) gets its own scrambled Sobol sequence
    over [floor, upper bound]^k. Round-robin over the sub-systems turns them into one
    sequence, so "the first n Sobol points" is well defined for the sobol methods.
    """
    rng = np.random.default_rng(seed)
    subsystems = [c for k in range(k_min, k_max + 1) for c in itertools.combinations(elements, k)]
    rng.shuffle(subsystems)
    m = int(np.ceil(np.log2(per_subsystem)))
    streams = []
    for sub in subsystems:
        u = qmc.Sobol(d=len(sub), scramble=True, seed=rng).random_base2(m)
        lo = np.full(len(sub), FLOOR_WT)
        hi = np.array([UPPER_WT[e] for e in sub])
        W = np.zeros((len(u), len(PALETTE)))
        W[:, [IDX[e] for e in sub]] = lo + u * (hi - lo)
        streams.append(W[feasible(W, min_total)])
    rows, labels = [], []
    for i in range(max(len(s) for s in streams)):
        for sub, s in zip(subsystems, streams):
            if i < len(s):
                rows.append(s[i])
                labels.append("Al-" + "-".join(sub))
    return np.array(rows), labels


def read_existing(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    W = np.array([[float(r.get(e) or 0) for e in PALETTE] for r in rows])
    return W, rows


# --------------------------------------------------------------------------- selection
def _sqdist(A, B):
    return np.maximum((A * A).sum(1)[:, None] + (B * B).sum(1)[None, :] - 2 * A @ B.T, 0.0)


def _rbf(A, B, ell):
    return np.exp(-0.5 * _sqdist(A, B) / ell**2)


def select_sobol(Xc, Xe, n, **_):
    return list(range(min(n, len(Xc))))


def select_exclusion(Xc, Xe, n, radius, **_):
    picked = []
    design = Xe.copy()
    for i, x in enumerate(Xc):
        if len(design) == 0 or np.sqrt(_sqdist(x[None], design).min()) >= radius:
            picked.append(i)
            design = np.vstack([design, x])
            if len(picked) == n:
                break
    return picked


def select_maximin(Xc, Xe, n, **_):
    dmin = np.sqrt(_sqdist(Xc, Xe).min(1)) if len(Xe) else np.full(len(Xc), np.inf)
    picked = []
    for _ in range(n):
        i = int(np.argmax(dmin))
        picked.append(i)
        dmin = np.minimum(dmin, np.sqrt(_sqdist(Xc, Xc[i : i + 1])[:, 0]))
    return picked


def posterior_var(Xr, Xd, ell, jitter=1e-6):
    """Prior-unit GP posterior variance at Xr given noise-free points Xd (locations only)."""
    if len(Xd) == 0:
        return np.ones(len(Xr))
    L = np.linalg.cholesky(_rbf(Xd, Xd, ell) + jitter * np.eye(len(Xd)))
    V = np.linalg.solve(L, _rbf(Xd, Xr, ell))
    return np.clip(1.0 - (V * V).sum(0), 0.0, 1.0)


def select_imse(Xc, Xe, n, ell, n_ref=1500, seed=0, jitter=1e-6, **_):
    rng = np.random.default_rng(seed)
    Xr = Xc[rng.choice(len(Xc), size=min(n_ref, len(Xc)), replace=False)]
    picked = []
    for _ in range(n):
        Xd = np.vstack([Xe] + [Xc[picked]]) if (len(Xe) or picked) else np.zeros((0, Xc.shape[1]))
        Krc = _rbf(Xr, Xc, ell)
        if len(Xd):
            L = np.linalg.cholesky(_rbf(Xd, Xd, ell) + jitter * np.eye(len(Xd)))
            A = np.linalg.solve(L, _rbf(Xd, Xc, ell))  # (d, M)
            B = np.linalg.solve(L, _rbf(Xd, Xr, ell))  # (d, R)
            cov = Krc - B.T @ A
            var_c = np.clip(1.0 - (A * A).sum(0), 1e-12, None)
        else:
            cov, var_c = Krc, np.ones(len(Xc))
        gain = (cov * cov).mean(0) / var_c
        gain[picked] = -np.inf
        picked.append(int(np.argmax(gain)))
    return picked


SELECT = {"sobol": select_sobol, "sobol-exclusion": select_exclusion, "maximin": select_maximin, "imse": select_imse}


def coverage(Xe, Xn, Xr, ell):
    """How well existing + new points cover a reference pool of feasible points."""
    D = np.vstack([Xe, Xn])
    near = np.sqrt(_sqdist(Xr, D).min(1))
    gap_existing = np.sqrt(_sqdist(Xn, Xe).min()) if len(Xe) else np.nan
    gap_new = np.sqrt(_sqdist(Xn, Xn)[np.triu_indices(len(Xn), 1)].min()) if len(Xn) > 1 else np.nan
    return {
        "nearest_to_existing": gap_existing,
        "nearest_new_pair": gap_new,
        "fill_distance": near.max(),
        "mean_nearest": near.mean(),
        "mean_post_var": posterior_var(Xr, D, ell).mean(),
    }


# --------------------------------------------------------------------------- output
def at_percent(w):
    mol = {e: w[IDX[e]] / ATOMIC_WEIGHT[e] for e in PALETTE if w[IDX[e]] > 0}
    mol["Al"] = (100.0 - w.sum()) / ATOMIC_WEIGHT["Al"]
    tot = sum(mol.values())
    return {e: 100.0 * v / tot for e, v in mol.items()}


def label(w):
    parts = [f"{w[IDX[e]]:.2f}{e}" for e in PALETTE if w[IDX[e]] > 0]
    return "Al-" + "-".join(parts) if parts else "Al"


def run_composition(args):
    We, rows = read_existing(args.existing)
    Wc, subs = candidate_pool(args.elements, args.k_min, args.k_max, args.per_subsystem, args.seed, args.min_total)
    Xc, Xe = Wc / UB, We / UB
    rng = np.random.default_rng(args.seed + 1)
    Wr, _ = candidate_pool(args.elements, args.k_min, args.k_max, 256, args.seed + 1000, args.min_total)
    Xr = Wr / UB
    Xr = Xr[rng.choice(len(Xr), size=min(3000, len(Xr)), replace=False)]
    print(f"design space: Al + {args.k_min}-{args.k_max} of {', '.join(args.elements)}, "
          f"total additions {args.min_total:g}-{100 - AL_MIN_WT:g} wt%; "
          f"{len(Xc)} feasible candidates; {len(Xe)} existing points from {args.existing.name}")

    if args.compare:
        compare(Xc, Xe, Xr, args)
        return
    picked = SELECT[args.method](Xc, Xe, args.n, radius=args.radius, ell=args.ell, seed=args.seed)
    Wn = Wc[picked]
    assert feasible(Wn, args.min_total).all()
    cov = coverage(Xe, Xc[picked], Xr, args.ell)
    out = []
    for j, i in enumerate(picked):
        d = np.sqrt(_sqdist(Xc[i : i + 1], Xe)[0]) if len(Xe) else np.array([np.nan])
        k = int(np.argmin(d))
        atp = at_percent(Wc[i])
        out.append({
            "code": f"SF{j + 1}", "strategy": "space-filling", "method": args.method,
            "subsystem": subs[i], "wt_pct": label(Wc[i]),
            "at_pct": "Al-" + "-".join(f"{atp[e]:.2f}{e}" for e in PALETTE if e in atp),
            "nearest_existing": rows[k]["code"] if len(Xe) else "", "distance": round(float(d[k]), 3),
            **{e: round(float(Wc[i, IDX[e]]), 3) for e in PALETTE},
        })
    print(f"\n{args.method}: {args.n} picks (normalized distance; each element scaled by its upper bound)")
    for r in out:
        print(f"  {r['code']}: {r['wt_pct']:<36} wt%   nearest existing {r['nearest_existing']} at {r['distance']}")
    print("  coverage: " + ", ".join(f"{k} {v:.3f}" for k, v in cov.items()))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
        print(f"wrote {args.out}")


def compare(Xc, Xe, Xr, args):
    """Average coverage of every method over several scrambles of the Sobol pool."""
    results = {m: [] for m in METHODS}
    for s in range(args.repeats):
        Wc, _ = candidate_pool(args.elements, args.k_min, args.k_max, args.per_subsystem, args.seed + 17 * s, args.min_total)
        Xc_s = Wc / UB
        for m in METHODS:
            picked = SELECT[m](Xc_s, Xe, args.n, radius=args.radius, ell=args.ell, seed=s)
            results[m].append(coverage(Xe, Xc_s[picked], Xr, args.ell))
    keys = list(results[METHODS[0]][0])
    print(f"\n{args.n} new points, mean over {args.repeats} scrambles (higher is better for the first two, lower for the rest)")
    print(f"{'method':<16}" + "".join(f"{k:>21}" for k in keys))
    for m in METHODS:
        print(f"{m:<16}" + "".join(f"{np.nanmean([r[k] for r in results[m]]):>21.3f}" for k in keys))
    base = posterior_var(Xr, Xe, args.ell).mean()
    print(f"{'(existing only)':<16}" + f"{'':>21}{'':>21}"
          f"{np.sqrt(_sqdist(Xr, Xe).min(1)).max():>21.3f}{np.sqrt(_sqdist(Xr, Xe).min(1)).mean():>21.3f}{base:>21.3f}")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["method", *keys])
            for m in METHODS:
                w.writerow([m, *(round(float(np.nanmean([r[k] for r in results[m]])), 4) for k in keys)])
        print(f"wrote {args.out}")


def run_features(args):
    with open(args.candidates, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    F = np.array([[float(r[c]) for c in args.features] for r in rows])
    lo, hi = F.min(0), F.max(0)
    X = (F - lo) / np.where(hi > lo, hi - lo, 1.0)
    is_existing = np.array([str(r.get("existing", "0")).strip() in {"1", "true", "True", "yes"} for r in rows])
    Xe, Xc = X[is_existing], X[~is_existing]
    cand_rows = [r for r, e in zip(rows, is_existing) if not e]
    picked = SELECT[args.method](Xc, Xe, args.n, radius=args.radius, ell=args.ell, seed=args.seed)
    print(f"{len(Xc)} candidates, {len(Xe)} existing; {args.method} in ({', '.join(args.features)}) space:")
    for i in picked:
        d = np.sqrt(_sqdist(Xc[i : i + 1], Xe).min()) if len(Xe) else float("nan")
        print(f"  {cand_rows[i].get('code', i)}: " + ", ".join(f"{c}={cand_rows[i][c]}" for c in args.features)
              + f"  (nearest existing {d:.3f})")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(cand_rows[0]))
            w.writeheader()
            w.writerows(cand_rows[i] for i in picked)
        print(f"wrote {args.out}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=3, help="how many space-filling points to add")
    p.add_argument("--method", choices=METHODS, default="imse")
    p.add_argument("--elements", nargs="+", default=DEFAULT_ELEMENTS, choices=PALETTE)
    p.add_argument("--k-min", type=int, default=1, help="fewest additions per alloy")
    p.add_argument("--k-max", type=int, default=3, help="most additions per alloy")
    p.add_argument("--min-total", type=float, default=3.0,
                   help="least total wt%% of additions; keeps picks out of the dilute corner near 6063 "
                        "(about 1 wt%%), which can't be strong. 0 turns it off")
    p.add_argument("--per-subsystem", type=int, default=256, help="Sobol points per sub-system (rounded up to 2^m)")
    p.add_argument("--existing", type=pathlib.Path, default=HERE / "seeds.csv")
    p.add_argument("--radius", type=float, default=0.5, help="exclusion radius for sobol-exclusion (normalized units)")
    p.add_argument("--ell", type=float, default=0.5, help="RBF length scale for imse and the coverage metric (normalized units)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--compare", action="store_true", help="compare all methods instead of picking")
    p.add_argument("--repeats", type=int, default=10, help="scrambles to average over with --compare")
    p.add_argument("--candidates", type=pathlib.Path, help="CSV of screened candidates (descriptor-space mode)")
    p.add_argument("--features", nargs="+", help="feature columns of --candidates to space-fill in")
    p.add_argument("--out", type=pathlib.Path, help="write the picks (or the comparison) to this CSV")
    args = p.parse_args(argv)
    if args.candidates:
        if not args.features:
            sys.exit("--candidates needs --features")
        run_features(args)
    else:
        run_composition(args)


if __name__ == "__main__":
    main()
