"""Aggregate sweep results: curves vs $ spent, cost-to-target and speed-up ratios."""

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


def cost_to(c, target):
    """First grid cost where a seed's curve reaches target (inf if never)."""
    hit = c >= target
    return np.where(hit.any(1), GRID[hit.argmax(1)], np.inf)


def boot_ratio(a, b, n=4000, seed=0):
    """Bootstrap CI of median(a)/median(b) across seeds (inf-aware)."""
    rng = np.random.default_rng(seed)
    ra = []
    for _ in range(n):
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
        for t in targets:
            cp = cost_to(C["pkgfn"], t)
            row = [f"  target {t:.0%}: pKGFN median ${np.median(cp) / 1e3:.0f}k (reached {np.isfinite(cp).mean():.0%})"]
            for k in C:
                if k == "pkgfn":
                    continue
                cb = cost_to(C[k], t)
                r, lo, hi = boot_ratio(cb, cp)
                row.append(f"{k} ${np.median(cb) / 1e3:.0f}k ({np.isfinite(cb).mean():.0%}) x{r:.1f} [{lo:.1f},{hi:.1f}]")
            lines.append(" | ".join(row))
    return "\n".join(lines), C


def first_cost(mean_curve, target):
    hit = mean_curve >= target - 1e-12
    return GRID[hit.argmax()] if hit.any() else np.inf


def speedup(Cp, Cb, n=2000, seed=0):
    """Spend the baseline needs to reach its own final mean level, divided by the
    spend pKGFN needs to reach that level (mean curves; seeds bootstrapped)."""
    rng = np.random.default_rng(seed)

    def one(cp, cb):
        tgt = np.nanmean(cb[:, -1])
        return first_cost(np.nanmean(cb, 0), tgt) / max(first_cost(np.nanmean(cp, 0), tgt), GRID[1])

    est = one(Cp, Cb)
    bs = [one(Cp[rng.integers(0, len(Cp), len(Cp))], Cb[rng.integers(0, len(Cb), len(Cb))]) for _ in range(n)]
    bs = np.array(bs)
    return est, np.percentile(bs, 5), np.percentile(bs, 50), np.percentile(bs, 95), np.mean(np.isfinite(bs) & (bs >= 3))


def speedup_table(kappa, metric="best_validated"):
    ys = optimum(kappa)
    data = load(kappa)
    C = {k: curves(v, metric, ys) for k, v in data.items()}
    lines = []
    for k in C:
        if k == "pkgfn" or "pkgfn" not in C:
            continue
        est, lo, med, hi, p3 = speedup(C["pkgfn"], C[k])
        lines.append(f"  vs {k:13s}: {est:4.1f}x  (90% bootstrap {lo:.1f}-{hi:.1f}; P(>=3x) = {p3:.2f}); n = {len(C['pkgfn'])}/{len(C[k])}")
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
        for b in ("tiered", "tiered_naive", "eifn", "eifn_reuse", "ei", "random", "pkgfn_la", "pkgfn_free"):
            print(paired(kap, b))




def markdown_table(kappa, metric="best_validated", kinds=("pkgfn", "pkgfn_free", "pkgfn_la", "eifn_reuse", "eifn", "ei", "tiered", "tiered_naive", "random")):
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
