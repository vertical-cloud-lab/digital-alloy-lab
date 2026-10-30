"""Copper against aluminum: why the bofn-prelim headline does not carry over.

    python compare/landscape.py      # first: the two truths on random designs (landscape.json)
    python compare/compare.py        # tables.md and the compare_*.png figures

Tables: the two benchmarks' results side by side; the copper network with and without the
immersion gate (compare/results-nogate/, run with BOFN_NOGATE=1); pKGFN at the light Monte Carlo
settings of the first copper sweep (quality/results-light/) against the aluminum production
settings (results/); tiered screening against corrosion-aware tiered screening.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
CU = HERE.parent
AL = CU.parent / "bofn-prelim"
sys.path.insert(0, str(CU))
from analyze import GRID, SHORT, at, cost_to, curve, fmt_cost, optimum  # noqa: E402

AL_OPT = json.loads((HERE / "al_optimum.json").read_text())["kappa1"]
LAND = json.loads((HERE / "landscape.json").read_text())
NOGATE_OPT = next(r["optimum"] for r in LAND if "no immersion gate" in r.get("truth", ""))
CU_OPT = optimum(1.0, 1.0)
AL_SHORT = {"pkgfn": "pKGFN: picks the stage", "pkgfn_free": "pKGFN, any alloy", "eifn": "BOFN, full pipeline", "eifn_reuse": "BOFN + powder (lot) reuse",
            "tiered": "Tiered screening", "tiered_naive": "Tiered, no powder reuse", "ei": "Standard BO", "random": "Random"}


def load_dir(path):
    out = {}
    for p in sorted(Path(path).glob("*.json")):
        r = json.loads(p.read_text())
        out.setdefault(r["kind"], []).append(r)
    for k in out:
        out[k].sort(key=lambda r: r["seed"])
    return out


def curves(runs, ystar):
    return np.stack([curve(r["rows"]) for r in runs]) / ystar


def ms(c, spend):
    v = at(c, spend) * 100
    return f"{np.nanmean(v):.0f}% ± {np.nanstd(v) / np.sqrt(len(v)):.0f}"


def wilcoxon_row(A, B, ystar_a, ystar_b, spends=(25_000, 50_000, 100_000)):
    from scipy.stats import wilcoxon

    a = {r["seed"]: curve(r["rows"]) / ystar_a for r in A}
    b = {r["seed"]: curve(r["rows"]) / ystar_b for r in B}
    seeds = sorted(set(a) & set(b))
    cells = []
    for s_ in spends:
        i = int(np.searchsorted(GRID, s_))
        d = np.array([a[s][i] - b[s][i] for s in seeds])
        p = wilcoxon(d).pvalue if np.any(d != 0) else 1.0
        cells.append(f"{d.mean() * 100:+.0f} points ({(d > 0).sum()}/{(d == 0).sum()}/{(d < 0).sum()}; p = {p:.2g})")
    return len(seeds), cells


def needle_table():
    p = HERE / "needle.json"
    if not p.exists():
        return ""
    n = json.loads(p.read_text())
    a, c = n["aluminum (kappa = 1)"], n["copper (1, 1)"]
    keys = ["optimum composition, random settings: share >= 60%", "optimum composition, random settings: share > 0", "random composition, optimum settings: share >= 60%",
            "random composition, its best of 2,048 settings: share >= 60%", "random composition, its best of 2,048 settings: share > 0"]
    rows = ["| Share of designs (`needle.py`) | Al (kappa = 1) | Cu (1, 1) |", "|---|---|---|"]
    rows += [f"| {k.replace('share >= 60%', 'J at least 60% of J*').replace('share > 0', 'J > 0')} | {a[k]:.1%} | {c[k]:.1%} |" for k in keys]
    rows += [f"| random designs passing immersion | | {c['random designs passing immersion']:.1%} |",
             f"| the same designs, had they deposited fully dense | | {c['random designs that would pass if deposited fully dense']:.1%} |",
             f"| random designs depositing at rho_m >= 0.9 | | {c['random designs with rho_m >= 0.9']:.2%} |"]
    return "\n".join(rows)


def side_by_side():
    al = load_dir(AL / "results" / "k1")
    cu = load_dir(CU / "results" / "k1e1")
    rows = ["| Policy | Al (kappa = 1): n | start | $25k | $50k | $100k | Cu (1, 1): n | start | $25k | $50k | $100k |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in ("pkgfn", "eifn_reuse", "eifn", "ei", "random", "tiered", "tiered_naive", "tiered_ni", "tiered_ni_ref", "pkgfn_free"):
        cells = []
        for data, ystar in ((al, AL_OPT), (cu, CU_OPT)):
            if k not in data:
                cells += ["", "", "", "", ""]
                continue
            c = curves(data[k], ystar)
            cells += [str(len(c)), f"{np.nanmean(c[:, 0]) * 100:.0f}%", ms(c, 25_000), ms(c, 50_000), ms(c, 100_000)]
        rows.append(f"| {SHORT.get(k, AL_SHORT.get(k, k))} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def landscape_table():
    a, c, n = LAND[0], LAND[1], LAND[2]
    seeds = LAND[3]["seed_data"]
    rows = ["| Uniform random designs (10^6 per truth) | Al (kappa = 1) | Cu (1, 1) | Cu (1, 1) without the immersion gate |", "|---|---|---|---|"]
    rows.append(f"| optimum J* | {a['optimum']:.3f} | {c['optimum']:.3f} | {n['optimum']:.3f} |")
    rows.append(f"| median design (% of J*) | {a['quantiles_pct']['50%'] * 100:.0f}% | {c['quantiles_pct']['50%'] * 100:.0f}% | {n['quantiles_pct']['50%'] * 100:.0f}% |")
    for t in ("0%", "50%", "60%", "70%", "80%"):
        lab = "share with J > 0" if t == "0%" else f"share with J at least {t} of J*"
        rows.append(f"| {lab} | {a['share_above'][t]:.3%} | {c['share_above'][t]:.3%} | {n['share_above'][t]:.3%} |")
    for k in ("5", "21", "24", "26", "29"):
        rows.append(f"| expected best of {k} random designs (% of J*) | {a['expected_best_of'][k] * 100:.0f}% | {c['expected_best_of'][k] * 100:.0f}% | {n['expected_best_of'][k] * 100:.0f}% |")
    rows.append(f"| the five shared seed designs: mean best (% of J*), 20 seeds | {seeds['aluminum']['mean_best_seed_pct'] * 100:.0f}% | {seeds['copper']['mean_best_seed_pct'] * 100:.0f}% | |")
    rows.append(f"| share passing immersion (m >= m_ref) | | {c['share_passing_immersion']:.1%} | |")
    return "\n".join(rows)


def gate_table():
    gated = load_dir(CU / "results" / "k1e1")
    nog = load_dir(HERE / "results-nogate" / "k1e1")
    al = load_dir(AL / "results" / "k1")
    rows = ["| Policy | Cu (1, 1) as benchmarked: n | start | $25k | $50k | $100k | Cu without the immersion gate: n | start | $25k | $50k | $100k | Al (kappa = 1) $100k |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in ("eifn_reuse", "eifn", "ei", "random", "pkgfn"):
        cells = []
        for data, ystar in ((gated, CU_OPT), (nog, NOGATE_OPT)):
            if k not in data:
                cells += ["", "", "", "", ""]
                continue
            c = curves(data[k], ystar)
            cells += [str(len(c)), f"{np.nanmean(c[:, 0]) * 100:.0f}%", ms(c, 25_000), ms(c, 50_000), ms(c, 100_000)]
        cells.append(ms(curves(al[k], AL_OPT), 100_000) if k in al else "")
        rows.append(f"| {SHORT[k]} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def fidelity_table():
    light = load_dir(CU / "quality" / "results-light" / "k1e1").get("pkgfn", [])
    hf = load_dir(CU / "results" / "k1e1").get("pkgfn", [])
    if not light or not hf:
        return "", ""
    rows = ["| pKGFN settings | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | KG-flat fallback share | C | A | U | M | S | T | K | I |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, runs in (("light (first sweep): S = 32, 10 candidates, 256 pool, old fallback test", light), ("high fidelity (aluminum production): S = 64, 16 candidates, 512 pool, fixes", hf)):
        c = curves(runs, CU_OPT)
        fb = sum(sum(1 for x in r["rows"][1:] if x.get("fallback")) for r in runs) / sum(len(r["rows"]) - 1 for r in runs)
        cnt = {g: np.mean([r["counts"][g] for r in runs]) for g in "CAUMSTKI"}
        cells = [str(len(c)), ms(c, 25_000), ms(c, 50_000), ms(c, 100_000)] + [f"{fmt_cost(np.median(cost_to(c, t)))} ({np.isfinite(cost_to(c, t)).mean():.0%})" for t in (0.6, 0.7)]
        cells += [f"{fb:.0%}"] + [f"{cnt[g]:.1f}" for g in "CAUMSTKI"]
        rows.append(f"| {name} | " + " | ".join(cells) + " |")
    n, cells = wilcoxon_row(hf, light, CU_OPT, CU_OPT)
    pair = f"Matched seeds, high fidelity minus light (n = {n}; wins/ties/losses; Wilcoxon): $25k {cells[0]}; $50k {cells[1]}; $100k {cells[2]}."
    return "\n".join(rows), pair


def tiered_table():
    cu = load_dir(CU / "results" / "k1e1")
    rows = ["| Policy | n | $25k | $50k | $100k | builds immersed per run | of which pass immersion | builds stopped by the one-hour screen per run | lots retired at Utah per run |", "|---|---|---|---|---|---|---|---|---|"]
    from bofn_alloy import M_REF

    for k in ("tiered", "tiered_ni", "tiered_ni_ref"):
        if k not in cu:
            continue
        runs = cu[k]
        c = curves(runs, CU_OPT)
        imm = [sum(1 for b in r["builds"][5:] if b["m"] is not None) for r in runs]
        ok = [sum(1 for b in r["builds"][5:] if b["m"] is not None and b["m"] >= M_REF) for r in runs]
        stop = [sum(1 for x in r["rows"] if x["action"] == "screen-fail") for r in runs]
        ret = [sum(1 for L in r["lots"][5:] if len(L["utah"]) >= 3 and max(u[2] for u in L["utah"]) < 0.5) for r in runs]
        rows.append(f"| {SHORT[k]} | {len(c)} | {ms(c, 25_000)} | {ms(c, 50_000)} | {ms(c, 100_000)} | {np.mean(imm):.1f} | {np.mean(ok):.1f} | {np.mean(stop):.1f} | {np.mean(ret):.1f} |")
    return "\n".join(rows)


def first_positive_table():
    """How long each policy takes to demonstrate its first alloy with J > 0 (it must pass immersion and
    out-earn its burden), and how often pKGFN's KG was flat before and after that point."""
    cu = load_dir(CU / "results" / "k1e1")
    light = load_dir(CU / "quality" / "results-light" / "k1e1")
    rows = ["| Policy | n | seeds whose shared seed data already holds an alloy with J > 0 | median new spend to the first alloy with J > 0 (seeds that reach it) | KG-flat fallback share before it | after it |", "|---|---|---|---|---|---|"]
    sets = [(k, cu[k]) for k in ("pkgfn", "eifn_reuse", "eifn", "ei", "random", "tiered", "tiered_ni", "tiered_ni_ref") if k in cu]
    if "pkgfn" in light:
        sets.insert(1, ("pkgfn (light settings)", light["pkgfn"]))
    for k, runs in sets:
        start = sum(1 for r in runs if r["rows"][0]["best_validated"] > 0)
        sp, fb_b, fb_a = [], [0, 0], [0, 0]
        for r in runs:
            hit = next((x["spent"] for x in r["rows"] if x["best_validated"] > 0), None)
            sp.append(hit if hit is not None else np.inf)
            for x in r["rows"][1:]:
                if "fallback" not in x:
                    continue
                tgt = fb_b if x["best_validated"] <= 0 else fb_a
                tgt[0] += int(x["fallback"])
                tgt[1] += 1
        sp = np.array(sp)
        fb = (f"{fb_b[0] / fb_b[1]:.0%} of {fb_b[1]}" if fb_b[1] else "", f"{fb_a[0] / fb_a[1]:.0%} of {fb_a[1]}" if fb_a[1] else "")
        name = SHORT.get(k, k)
        rows.append(f"| {name} | {len(runs)} | {start} | {fmt_cost(np.median(sp))} ({np.isfinite(sp).sum()} of {len(sp)}) | {fb[0]} | {fb[1]} |")
    return "\n".join(rows)


def figures():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    import plot as PL  # the benchmark's styles and fonts

    # (1) the landscape: share of random designs at or above each fraction of the optimum
    import torch

    sys.path.insert(0, str(HERE))
    from landscape import al, cu  # noqa: F401  (the two truth modules, loaded side by side)

    g = torch.Generator().manual_seed(1)
    ta, tc = al.AlloyTruth(1.0), cu.AlloyTruth(1.0, 1.0)
    Xa, Xc = torch.rand(400_000, al.D, generator=g), torch.rand(400_000, cu.D, generator=g)
    ya = (ta.objective(Xa) / AL_OPT).numpy()
    oc = tc.full(Xc)
    yc = (tc.objective(Xc, oc) / CU_OPT).numpy()
    yn = ((oc["U"] - cu.LAMBDA * cu.burden(Xc)) / NOGATE_OPT).numpy()
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    t = np.linspace(0, 1, 201)
    for y, lab, col, ls in ((ya, "Aluminum LPBF (kappa = 1)", PL.INK, "-"), (yn, "Copper DED, no immersion gate", "#8C8C8C", (0, (4, 2))), (yc, "Copper DED (1, 1), as benchmarked", PL.RED, "-")):
        surv = np.array([(y >= v).mean() for v in t])
        ax.semilogy(t * 100, np.clip(surv, 1e-6, None), color=col, lw=2.6, ls=ls, label=lab)
    ax.set_xlabel("Fraction of the optimum, J / J* (%)")
    ax.set_ylabel("Share of random designs\nat or above it")
    ax.set_xlim(0, 100)
    ax.set_ylim(1e-5, 1)
    ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
    ax.legend(frameon=False, fontsize=13, loc="lower left")
    fig.tight_layout()
    fig.savefig(HERE / "compare_landscape.png")
    plt.close(fig)
    # (2) the two benchmarks side by side
    al_runs = load_dir(AL / "results" / "k1")
    cu_runs = load_dir(CU / "results" / "k1e1")
    nog = load_dir(HERE / "results-nogate" / "k1e1")
    kinds = ("pkgfn", "eifn_reuse", "eifn", "ei", "random", "tiered", "tiered_ni_ref")
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.6), sharey=True)
    x = GRID / 1e3
    for ax, data, ystar, title in ((axes[0], al_runs, AL_OPT, "Aluminum LPBF (kappa = 1)"), (axes[1], cu_runs, CU_OPT, "Copper DED (1, 1), as benchmarked"),
                                   (axes[2], nog, NOGATE_OPT, "Copper DED, no immersion gate")):
        for k in kinds:
            if k not in data:
                continue
            c = curves(data[k], ystar) * 100
            m, se = np.nanmean(c, 0), np.nanstd(c, 0) / np.sqrt(len(c))
            st = PL.STYLE[k]
            ax.fill_between(x, m - se, m + se, color=st["color"], alpha=0.08, lw=0)
            ax.plot(x, m, color=st["color"], lw=st["lw"], ls=st["ls"], label=f"{SHORT[k]} (n = {len(c)})")
            ax.text(101, m[-1], f"{m[-1]:.0f}", fontsize=11, va="center", color=st["color"] if st["color"] != "#D0D0D0" else "#A0A0A0")
        ax.set_title(title, fontsize=15, loc="left", color=PL.INK)
        ax.set_xlim(0, 100)
        ax.set_xlabel("New spend ($k)")
        ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
        ax.axhline(0, color="#BFBFBF", lw=0.8)
    axes[0].set_ylabel("Best alloy demonstrated\n(% of true optimum)")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, [l.split(" (n")[0] for l in labels], loc="lower center", ncol=7, frameon=False, fontsize=12)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(HERE / "compare_al_vs_cu.png")
    plt.close(fig)
    # (3) pKGFN light against high fidelity, every seed
    light = load_dir(CU / "quality" / "results-light" / "k1e1").get("pkgfn", [])
    hf = cu_runs.get("pkgfn", [])
    if light and hf:
        fig, ax = plt.subplots(figsize=(9.5, 5.4))
        for runs, col, lab in ((light, "#BDBDBD", "light (S = 32, 10 candidates)"), (hf, PL.RED, "high fidelity (S = 64, 16 candidates)")):
            c = curves(runs, CU_OPT) * 100
            for row in c:
                ax.plot(x, row, color=col, lw=0.7, alpha=0.5)
            ax.plot(x, np.nanmean(c, 0), color=col if col != "#BDBDBD" else "#7F7F7F", lw=3, label=f"{lab}, mean of {len(c)}")
        ax.plot(x, np.nanmean(curves(cu_runs["eifn"], CU_OPT) * 100, 0), color="#404040", lw=2, ls=(0, (4, 2)), label=f"BOFN, full pipeline, mean of {len(cu_runs['eifn'])}")
        ax.set_xlim(0, 100)
        ax.set_xlabel("New spend ($k)")
        ax.set_ylabel("pKGFN, best alloy demonstrated\n(% of true optimum)")
        ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
        ax.legend(frameon=False, fontsize=12, loc="upper left")
        fig.tight_layout()
        fig.savefig(HERE / "compare_pkgfn_fidelity.png")
        plt.close(fig)


def main():
    L = ["# Copper against aluminum (written by `compare/compare.py`)", "",
         f"Optima: aluminum (kappa = 1) {AL_OPT:.3f}; copper (1, 1) {CU_OPT:.3f}; copper (1, 1) without the immersion gate {NOGATE_OPT:.3f}. "
         "Every percentage is of the optimum of the truth the runs were scored on.", "",
         "## The two truths on random designs", "", landscape_table(), "",
         "## Composition or process? Where the copper needle is", "", needle_table(), "",
         "## The two benchmarks' results", "", side_by_side(), "",
         "## The copper network without the immersion gate (J = U - 0.3 B; same network, stages, costs and seeds)", "", gate_table(), ""]
    ft, pair = fidelity_table()
    if ft:
        L += ["## pKGFN: light against high-fidelity Monte Carlo settings", "", ft, "", pair, ""]
    L += ["## Tiered screening against corrosion-aware tiered screening", "", tiered_table(), ""]
    L += ["## Finding the feasible region first", "", "The copper objective is gated: an alloy that fails immersion scores minus 0.3 times its burden. "
          "Before a policy has demonstrated an alloy with J > 0, one-step KG has little to improve on.", "", first_positive_table(), ""]
    (HERE / "tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))
    figures()


if __name__ == "__main__":
    main()
