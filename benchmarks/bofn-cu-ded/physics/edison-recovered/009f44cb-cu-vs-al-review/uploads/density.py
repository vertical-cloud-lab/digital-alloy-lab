"""What the "dense index" of the copper truth is, and why copper-rich alloys read 0.40 at Utah.

    python compare/density.py        # writes compare/density.json and compare/density_factors.png

The deposition nodes are rho = window * q^0.3 * (1 - 0.75 crack) * (1 - lof) (times 0.95 + 0.05 q
at Utah): a product of four factors in [0, 1], not a relative density. This script takes the
README's 200 copper-rich compositions (Ni <= 0.07, Al <= 0.2 on the scaled axes), finds each one's
best Utah and Mines settings, and reports every factor at those settings. It also reads the index
as the tensile knockdown exp(-b * porosity) of a porous metal (b = 4, 7, 10) to show what relative
density each value would correspond to if it were read that way.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from bofn_alloy import P_CAP, AlloyTruth, D, sig  # noqa: E402

torch.set_default_dtype(torch.double)


def factors(t, X, utah):
    o = t.full(X)
    P = X[:, 5].clamp(max=P_CAP) if utah else X[:, 5]
    v, f, g, h, q = X[:, 6], o["f"], o["g"].clamp(min=0), o["h"], o["q"].clamp(min=0)
    u = P - v - (0.05 + 0.25 * f)
    window = torch.exp(-((u / 0.2) ** 2)) * (1 - 0.35 * sig((P - 0.85) / 0.05))
    f_eff = f * (1 - t.kappa * 0.85 * g / (g + 0.12))
    crack = sig((f_eff - 0.56) / 0.05)
    lof = sig((h - P) / 0.08)
    out = {"window": window, "powder q^0.3": q**0.3, "crack factor 1 - 0.75 crack": 1 - 0.75 * crack, "fusion 1 - lof": 1 - lof, "h": h, "P": P}
    out["rho"] = o["rho_u"] if utah else o["rho_m"]
    if utah:
        out["thin wall 0.95 + 0.05 q"] = 0.95 + 0.05 * q
    return out


def main():
    t = AlloyTruth(1.0, 1.0)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400_000, D, generator=g)
    rich = (X[:, 0] <= 0.07) & (X[:, 1] <= 0.2)
    comps = X[rich][:200, :4]
    apv = torch.quasirandom.SobolEngine(3, scramble=True, seed=1).draw(16384).double()
    rows = {"Utah (P capped at 0.5)": [], "Mines (full power)": []}
    for c in comps:
        Xr = torch.cat([c.expand(apv.shape[0], 4), apv], -1)
        for name, utah in (("Utah (P capped at 0.5)", True), ("Mines (full power)", False)):
            fa = factors(t, Xr, utah)
            j = int(fa["rho"].argmax())
            rows[name].append({k: float(v[j]) for k, v in fa.items()})
    summary = {}
    for name, rr in rows.items():
        keys = rr[0].keys()
        med = {k: float(torch.tensor([r[k] for r in rr]).median()) for k in keys}
        summary[name] = {"median_at_best_settings": med, "n": len(rr)}
    # reading the index as a porosity knockdown of strength: index = exp(-b phi) -> relative density 1 - phi
    reading = {}
    for idx in (0.30, 0.40, 0.50, 0.70, 0.88, 0.93, 0.99):
        reading[f"{idx:.2f}"] = {f"b = {b}": round(1 + math.log(idx) / b, 3) for b in (4, 7, 10)}
    out = {"copper_rich": summary, "relative_density_if_read_as_exp(-b*porosity)": reading}
    (HERE / "density.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    # figure: the median factor at each site's best settings
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    import plot as PL  # noqa: F401  (the benchmark's fonts and styles)

    names = ["window", "powder q^0.3", "crack factor 1 - 0.75 crack", "fusion 1 - lof", "rho"]
    labels = ["process\nwindow", "powder\nq$^{0.3}$", "crack\nfactor", "fusion\n1 - lof", "index\n(product)"]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    wdt = 0.38
    for k, (name, col) in enumerate((("Utah (P capped at 0.5)", PL.RED), ("Mines (full power)", "#8C8C8C"))):
        vals = [summary[name]["median_at_best_settings"][n] for n in names]
        bars = ax.bar([i + (k - 0.5) * wdt for i in range(len(names))], vals, wdt, color=col, label=name)
        for b_, v in zip(bars, vals):
            ax.text(b_.get_x() + b_.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=12, color=PL.INK)
    ax.set_xticks(range(len(names)), labels, fontsize=13)
    ax.set_ylim(0, 1.32)
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_ylabel("Median over 200\ncompositions", fontsize=13)
    ax.tick_params(axis="y", labelsize=12)
    ax.set_title("Copper-rich alloys (Ni and Al under 2 wt%), each at its best settings", fontsize=14, loc="left", color=PL.INK)
    ax.legend(fontsize=12, frameon=False, loc="upper center", ncol=2)
    fig.tight_layout()
    fig.savefig(HERE / "density_factors.png")


if __name__ == "__main__":
    main()
