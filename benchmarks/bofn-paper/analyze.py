"""Aggregate sweep results: curves vs $ spent, cost-to-target and speed-up ratios.

Confidence intervals come from a matched-seed bootstrap: every policy starts a
given seed from the same seed alloys, so seeds are resampled jointly and each
draw compares the policies on the same seeds. The independent-seed bootstrap
behind the MS&T26 numbers (each policy's seeds resampled separately) is still
printed next to it as a sensitivity check.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch

from bofn_alloy import D, AlloyTruth

HERE = Path(__file__).parent
RES = HERE / "results"
GRID = np.arange(0, 100_001, 250.0)
NAMES = {
    "pkgfn": "pKGFN (stage by stage)",
    "kgfn": "KGFN, full pipeline",
    "eifn": "BOFN, full pipeline (EIFN)",
    "tiered": "Tiered screening",
    "ei": "Standard BO (EI)",
    "random": "Random",
}


@lru_cache
def optimum(kappa: float) -> float:
    t = AlloyTruth(kappa)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400_000, D, generator=g)
    y = t.objective(X)
    top = X[y.topk(20).indices]
    best = float(y.max())
    for x0 in top:
        xb, yb = x0, float(t.objective(x0))
        for scale in (0.03, 0.01, 0.003):
            P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
            yp = t.objective(P)
            if float(yp.max()) > yb:
                xb, yb = P[yp.argmax()], float(yp.max())
        best = max(best, yb)
    return best


def load(kappa: float, budget: float | None = None):
    out = {}
    for p in sorted((RES / f"k{kappa:g}").glob("*.json")):
        r = json.loads(p.read_text())
        out.setdefault(r["kind"], []).append(r)
    return out


def curve(rows, metric):
    """Step function of `metric` (running best for best_validated) on GRID."""
    spent = np.array([r["spent"] for r in rows])
    vals = np.array([r[metric] if r[metric] == r[metric] else -np.inf for r in rows])
    if metric == "best_validated":
        vals = np.maximum.accumulate(vals)
    idx = np.searchsorted(spent, GRID, side="right") - 1
    y = np.where(idx >= 0, vals[np.clip(idx, 0, None)], np.nan)
    return y


def curves(runs, metric, ystar):
    return np.stack([curve(r["rows"], metric) for r in runs]) / ystar


def matched(runs_a, runs_b, Ca, Cb):
    """Rows of two policies' curve arrays restricted to their common seeds, in the
    same seed order, so row i of both is seed i (for the matched-seed bootstrap)."""
    ia = {r["seed"]: i for i, r in enumerate(runs_a)}
    ib = {r["seed"]: i for i, r in enumerate(runs_b)}
    seeds = sorted(set(ia) & set(ib))
    return Ca[[ia[s] for s in seeds]], Cb[[ib[s] for s in seeds]], seeds


def cost_to(c, target):
    """First grid cost where a seed's curve reaches target (inf if never)."""
    hit = c >= target
    return np.where(hit.any(1), GRID[hit.argmax(1)], np.inf)


def boot_ratio(a, b, n=4000, seed=0, matched=False):
    """Bootstrap CI of median(a)/median(b) across seeds (inf-aware).

    matched=True resamples seed indices jointly (a[i] and b[i] must be the same
    seed); the default resamples a and b independently (the MS&T26 numbers)."""
    rng = np.random.default_rng(seed)
    ra = []
    for _ in range(n):
        if matched:
            i = rng.integers(0, len(a), len(a))
            ma, mb = np.median(a[i]), np.median(b[i])
        else:
            ma = np.median(rng.choice(a, len(a)))
            mb = np.median(rng.choice(b, len(b)))
        ra.append(ma / mb)
    ra = np.array(ra)
    return np.median(a) / np.median(b), np.percentile(ra, 5), np.percentile(ra, 95)


def summary(kappa, metric="best_validated", targets=(0.5, 0.6, 0.7, 0.8, 0.9)):
    ys = optimum(kappa)
    data = load(kappa)
    lines = [f"kappa={kappa}  y*={ys:.4f}  metric={metric}"]
    C = {k: curves(v, metric, ys) for k, v in data.items()}
    for k, c in C.items():
        fin = c[:, -1]
        lines.append(
            f"  {k:7s} n={len(c):2d}  final mean {np.nanmean(fin):.3f} ± {np.nanstd(fin) / np.sqrt(len(fin)):.3f} (SE)"
            f"  median {np.nanmedian(fin):.3f}  @$50k {np.nanmean(c[:, GRID.searchsorted(50_000)]):.3f}"
        )
    if "pkgfn" in C:
        lines.append("  cost-to-target ratio to pKGFN, x ratio [90% matched-seed bootstrap] (independent-seed bootstrap, sensitivity):")
        for t in targets:
            cp = cost_to(C["pkgfn"], t)
            row = [f"  target {t:.0%}: pKGFN median ${np.median(cp) / 1e3:.0f}k (reached {np.isfinite(cp).mean():.0%})"]
            for k in C:
                if k == "pkgfn":
                    continue
                cb = cost_to(C[k], t)
                r, lo, hi = boot_ratio(cb, cp)
                Mp, Mb, seeds = matched(data["pkgfn"], data[k], C["pkgfn"], C[k])
                _, lo_m, hi_m = boot_ratio(cost_to(Mb, t), cost_to(Mp, t), matched=True)
                row.append(f"{k} ${np.median(cb) / 1e3:.0f}k ({np.isfinite(cb).mean():.0%}) x{r:.1f} [{lo_m:.1f},{hi_m:.1f}] ({lo:.1f},{hi:.1f})")
            lines.append(" | ".join(row))
    return "\n".join(lines), C


def first_cost(mean_curve, target):
    hit = mean_curve >= target - 1e-12
    return GRID[hit.argmax()] if hit.any() else np.inf


def speedup(Cp, Cb, n=2000, seed=0, matched=False):
    """Spend the baseline needs to reach its own final mean level, divided by the
    spend pKGFN needs to reach that level (mean curves; seeds bootstrapped).

    matched=True resamples seeds jointly: row i of Cp and Cb must be the same
    seed (see `matched`), and each draw keeps the pairs together. The default
    resamples each policy's seeds independently (the MS&T26 numbers)."""
    rng = np.random.default_rng(seed)

    def one(cp, cb):
        tgt = np.nanmean(cb[:, -1])
        return first_cost(np.nanmean(cb, 0), tgt) / max(first_cost(np.nanmean(cp, 0), tgt), GRID[1])

    est = one(Cp, Cb)
    if matched:
        if len(Cp) != len(Cb):
            raise ValueError("matched bootstrap needs the same seeds in both arrays")
        bs = []
        for _ in range(n):
            i = rng.integers(0, len(Cp), len(Cp))
            bs.append(one(Cp[i], Cb[i]))
    else:
        bs = [one(Cp[rng.integers(0, len(Cp), len(Cp))], Cb[rng.integers(0, len(Cb), len(Cb))]) for _ in range(n)]
    bs = np.array(bs)
    return est, np.percentile(bs, 5), np.percentile(bs, 50), np.percentile(bs, 95), np.mean(np.isfinite(bs) & (bs >= 3))


def speedup_table(kappa, metric="best_validated", ref="pkgfn", over=None):
    """Speed-up of `ref` over every other policy, or with `over` set, of every
    policy over that one (e.g. over="tiered" gives the README's table). The CI is
    the matched-seed bootstrap; the independent-seed one follows as a sensitivity
    check. If the two policies' seed sets differ, the matched bootstrap uses the
    common seeds and its own point estimate on them is shown."""
    ys = optimum(kappa)
    data = load(kappa)
    C = {k: curves(v, metric, ys) for k, v in data.items()}
    lines = []
    pairs = [(k, over) for k in C if k != over] if over else [(ref, k) for k in C if k != ref]
    for a, b in pairs:
        if a not in C or b not in C:
            continue
        est, lo, med, hi, p3 = speedup(C[a], C[b])
        Ma, Mb, seeds = matched(data[a], data[b], C[a], C[b])
        est_m, lo_m, _, hi_m, p3_m = speedup(Ma, Mb, matched=True)
        on = "" if len(seeds) == len(C[a]) == len(C[b]) else f", {est_m:.1f}x on them"
        who = f"{a} over {b}" if over else f"vs {b}"
        lines.append(f"  {who:{24 if over else 16}s}: {est:4.1f}x  (90% matched-seed bootstrap {lo_m:.1f}-{hi_m:.1f}; P(>=3x) = {p3_m:.2f}; {len(seeds)} matched seeds{on})"
                     f"  [independent-seed bootstrap, sensitivity: {lo:.1f}-{hi:.1f}; P(>=3x) = {p3:.2f}]; n = {len(C[a])}/{len(C[b])}")
    return "\n".join(lines)


def paired(kappa, base, at=(25_000, 50_000, 100_000), metric="best_validated", ref="pkgfn"):
    """Seed-matched comparison (both policies start from the same seed alloys)."""
    from scipy.stats import wilcoxon

    ys = optimum(kappa)
    data = load(kappa)
    if ref not in data or base not in data:
        return ""
    A = {r["seed"]: curve(r["rows"], metric) / ys for r in data[ref]}
    B = {r["seed"]: curve(r["rows"], metric) / ys for r in data[base]}
    seeds = sorted(set(A) & set(B))
    out = [f"  {ref} vs {base} (n={len(seeds)} matched seeds)"]
    for c in at:
        i = int(np.searchsorted(GRID, c))
        a = np.array([A[s][i] for s in seeds])
        b = np.array([B[s][i] for s in seeds])
        dlt = a - b
        p = wilcoxon(dlt).pvalue if np.any(dlt != 0) else 1.0
        out.append(f"    @${c / 1e3:.0f}k: {ref} {a.mean():.1%} vs {b.mean():.1%}; diff {dlt.mean():+.1%} (wins {np.mean(dlt > 0):.0%}, ties {np.mean(dlt == 0):.0%}; Wilcoxon p={p:.3g})")
    for t in (0.6, 0.7, 0.8):
        ca = np.array([cost_to(A[s][None], t)[0] for s in seeds])
        cb = np.array([cost_to(B[s][None], t)[0] for s in seeds])
        out.append(
            f"    cost to {t:.0%}: {ref} median ${np.median(ca) / 1e3:.0f}k (reached {np.isfinite(ca).mean():.0%}), "
            f"{base} median ${np.median(cb) / 1e3:.0f}k (reached {np.isfinite(cb).mean():.0%})"
        )
    return "\n".join(out)


if __name__ == "__main__":
    import sys

    kappas = [float(v) for v in sys.argv[1:]] or [1.0]
    for kap in kappas:
        for m in ("best_validated", "rec_printed", "rec"):
            print(summary(kap, m)[0])
            print(speedup_table(kap, m))
            print()
        print(f"kappa={kap}  speed-up over tiered screening, best_validated")
        print(speedup_table(kap, over="tiered"))
        print()
        for b in ("tiered", "tiered_naive", "eifn", "eifn_reuse", "kgfn", "ei", "random", "pkgfn_la", "pkgfn_free"):
            print(paired(kap, b))




def markdown_table(kappa, metric="best_validated", kinds=("pkgfn", "pkgfn_free", "pkgfn_la", "kgfn", "eifn_reuse", "eifn", "ei", "tiered", "tiered_naive", "random")):
    from plot import SHORT

    ys = optimum(kappa)
    data = load(kappa)
    rows = ["| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |", "|---|---|---|---|---|---|---|---|"]
    for k in kinds:
        if k not in data:
            continue
        c = curves(data[k], metric, ys)
        cells = []
        for at in (25_000, 50_000, 100_000):
            v = c[:, int(np.searchsorted(GRID, at))] * 100
            cells.append(f"{np.nanmean(v):.0f}% ± {np.nanstd(v) / np.sqrt(len(v)):.0f}")
        for t in (0.6, 0.7, 0.8):
            ct = cost_to(c, t)
            med = np.median(ct)
            cells.append(f"{'>$100k' if not np.isfinite(med) else f'${med / 1e3:.0f}k'} ({np.isfinite(ct).mean():.0%} of seeds)")
        rows.append(f"| {SHORT[k]} | {len(c)} | " + " | ".join(cells) + " |")
    return "\n".join(rows)
