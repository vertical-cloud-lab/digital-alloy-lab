#!/usr/bin/env python3
"""Fig. 2 and Fig. 3 from atomizer run records: the repeatability bar (Block A) and Si in powder
against Si in the charge (Block B).

Input: one YAML record per run, in the format of byu-vcl
`atomizer-runs/plan-adv-mater/run-record-template.yaml` (cad4e6d). Fields left null are skipped,
never guessed.

    python tools/atomizer_analysis.py --runs '../atomizer-runs/*/run.yaml' --out figures/
    python tools/atomizer_analysis.py --selftest      # simulated records -> /tmp only

Writes `<out>/fig2-repeatability.{pdf,png}`, `<out>/fig3b-si-fidelity.{pdf,png}` (if Block B
records exist) and `<out>/repeatability-check.md`. The bar below was fixed before the first
counted run (byu-vcl plan-adv-mater README @ cad4e6d); change it only through a logged deviation.
"""
from __future__ import annotations

import argparse
import glob
import math
import random
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402
from scipy import stats  # noqa: E402

# The repeatability bar (plan-adv-mater README @ cad4e6d), as (metric, statistic, limit).
BAR = [
    ("d50_um", "cv_pct", 10.0),
    ("d10_um", "cv_pct", 15.0),
    ("d90_um", "cv_pct", 15.0),
    ("in_range_pct", "sd", 5.0),
    ("powder_pct", "sd", 10.0),
    ("circularity", "sd", 0.02),
    ("powder_o_ppm", "cv_pct", 15.0),
]
MIN_VALID, MIN_VALID_OF_FIRST5, EXTEND_IF_WITHIN = 5, 4, 0.20
MIN_CLOSURE_PCT = 95.0
# Nominal Si of the charge parts for Block B (wt%): 6063 spec 0.2-0.6, 4047 spec 11.0-13.0.
SI_6063, SI_4047 = 0.40, 12.0

BLUE, ORANGE, AQUA, INK, INK2, GRID_C, GRAY = "#257de0", "#f47230", "#00b894", "#191919", "#666666", "#e6e6e6", "#9c9c9c"
plt.rcParams.update({"font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "legend.frameon": False, "pdf.fonttype": 42, "savefig.dpi": 300})


@dataclass
class Run:
    path: str
    code: str
    order: int | None
    valid: bool | None
    plate: str | None
    halves: dict[str, dict] = field(default_factory=dict)  # 'A'/'B' -> metrics
    in_range_pct: float | None = None
    powder_pct: float | None = None
    closure_pct: float | None = None
    powder_o_ppm: float | None = None
    mass: dict[str, float] = field(default_factory=dict)
    charge_g: float | None = None
    powder_wt_pct: float | None = None
    si_eds: dict[str, tuple] = field(default_factory=dict)  # position -> (n, mean, sd)
    si_icp: float | None = None


def num(x):
    return None if x is None else float(x)


def load(path: str) -> Run:
    d = yaml.safe_load(open(path)) or {}
    r, y = d.get("run", {}), d.get("yields_pct", {}) or {}
    run = Run(path=path, code=str(r.get("code") or ""), order=r.get("run_order"), valid=r.get("valid"),
              plate=(d.get("setup") or {}).get("plate_id"),
              in_range_pct=num(y.get("in_range")), powder_pct=num(y.get("powder")),
              closure_pct=num(y.get("closure")),
              powder_o_ppm=num((d.get("composition") or {}).get("powder_o_ppm")),
              mass={k: float(v) for k, v in (d.get("mass_balance_g") or {}).items() if v is not None},
              charge_g=num((d.get("charge") or {}).get("total_g")),
              powder_wt_pct=num((d.get("charge") or {}).get("powder_wt_pct")))
    for p in d.get("psd") or []:
        run.halves.setdefault(p.get("half"), {}).update({k: num(p.get(k)) for k in ("d10_um", "d50_um", "d90_um")})
    for m in d.get("morphology") or []:
        run.halves.setdefault(m.get("half"), {})["circularity"] = num(m.get("circularity_mean"))
    comp = d.get("composition") or {}
    for pos, v in (comp.get("eds_si_wt_pct") or {}).items():
        if v and v.get("mean") is not None:
            run.si_eds[pos] = (v.get("n"), float(v["mean"]), num(v.get("sd")))
    icp = comp.get("icp_oes")
    if isinstance(icp, dict) and icp.get("si") is not None:
        run.si_icp = float(icp["si"])
    return run


def variance_components(values: list[list[float]]) -> tuple[float, float]:
    """One-way random effects with k splits per run: (run-to-run SD, split-to-split SD)."""
    groups = [g for g in values if len(g) >= 2]
    if len(groups) < 2:
        return math.nan, math.nan
    k = np.mean([len(g) for g in groups])
    grand = np.mean([x for g in groups for x in g])
    msb = sum(len(g) * (np.mean(g) - grand) ** 2 for g in groups) / (len(groups) - 1)
    msw = sum(sum((x - np.mean(g)) ** 2 for x in g) for g in groups) / sum(len(g) - 1 for g in groups)
    return math.sqrt(max(msb - msw, 0) / k), math.sqrt(msw)


def sd_ci(sd: float, n: int, level: float = 0.95) -> tuple[float, float]:
    a = 1 - level
    return (sd * math.sqrt((n - 1) / stats.chi2.ppf(1 - a / 2, n - 1)),
            sd * math.sqrt((n - 1) / stats.chi2.ppf(a / 2, n - 1)))


def run_value(run: Run, metric: str) -> float | None:
    if metric in ("in_range_pct", "powder_pct", "powder_o_ppm"):
        return getattr(run, metric)
    vals = [h[metric] for h in run.halves.values() if h.get(metric) is not None]
    return float(np.mean(vals)) if vals else None


def check_bar(block_a: list[Run]) -> tuple[list[str], dict]:
    attempts = sorted(block_a, key=lambda r: (r.order is None, r.order))
    valid = [r for r in attempts if r.valid]
    lines = ["| Metric | n | Mean | Statistic | Limit | 95 % CI on SD | Split SD / run SD | Pass |", "|---|---|---|---|---|---|---|---|"]
    summary = {"n_valid": len(valid), "n_attempts": len(attempts),
               "valid_of_first5": sum(bool(r.valid) for r in attempts[:5]), "rows": []}
    extend = False
    for metric, stat, limit in BAR:
        xs = [v for v in (run_value(r, metric) for r in valid) if v is not None]
        if len(xs) < 2:
            lines.append(f"| {metric} | {len(xs)} | | {stat} | {limit:g} | | | not yet |")
            continue
        mean, sd = float(np.mean(xs)), float(np.std(xs, ddof=1))
        value = 100 * sd / mean if stat == "cv_pct" else sd
        lo, hi = sd_ci(sd, len(xs))
        splits = [[h[metric] for h in r.halves.values() if h.get(metric) is not None] for r in valid]
        sb, sw = variance_components(splits) if metric in ("d10_um", "d50_um", "d90_um", "circularity") else (math.nan, math.nan)
        ratio = "" if math.isnan(sb) or sb == 0 else f"{sw / sb:.2f}"
        ok = value <= limit
        extend |= ok and value > (1 - EXTEND_IF_WITHIN) * limit
        summary["rows"].append((metric, len(xs), mean, stat, value, limit, ok))
        lines.append(f"| {metric} | {len(xs)} | {mean:.3g} | {stat} = {value:.3g} | {limit:g} | {lo:.3g}–{hi:.3g} | {ratio} | {'yes' if ok else '**no**'} |")
    closures = [r.closure_pct for r in valid if r.closure_pct is not None]
    head = [
        f"- Valid Block A runs: **{summary['n_valid']}** of {summary['n_attempts']} attempts (need ≥ {MIN_VALID});"
        f" valid among the first five attempts: {summary['valid_of_first5']} (need ≥ {MIN_VALID_OF_FIRST5}).",
        f"- Mass-balance closure ≥ {MIN_CLOSURE_PCT:g} %: {sum(c >= MIN_CLOSURE_PCT for c in closures)} of {len(closures)} runs.",
        "- Split SD / run SD should be ≤ 0.5 (measurement noise small next to run-to-run spread).",
        f"- {'**Extend to 8 runs**: a metric is within 20 % of its limit.' if extend else 'No metric within 20 % of its limit.'}",
        "",
    ]
    return head + lines, summary


def fig_repeatability(block_a: list[Run], out: Path) -> None:
    valid = sorted([r for r in block_a if r.valid], key=lambda r: r.order or 0)
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), gridspec_kw={"width_ratios": [1.2, 1.2, 1]})
    ax = axes[0]
    for metric, color, label in (("d10_um", AQUA, "D$_{10}$"), ("d50_um", BLUE, "D$_{50}$"), ("d90_um", ORANGE, "D$_{90}$")):
        for r in valid:
            ys = [h[metric] for h in r.halves.values() if h.get(metric) is not None]
            ax.scatter([r.order] * len(ys), ys, s=14, color=color, zorder=3)
        ax.plot([r.order for r in valid], [run_value(r, metric) for r in valid], color=color, lw=1.4, label=label)
    plates = [r.plate for r in valid]
    for i in range(1, len(valid)):
        if plates[i] != plates[i - 1]:
            ax.axvline((valid[i - 1].order + valid[i].order) / 2, color=GRAY, lw=0.8, ls="--")
    ax.set_xlabel("Run order"); ax.set_ylabel("Particle size (µm)")
    ax.legend(fontsize=7, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    ax.grid(axis="y", color=GRID_C, lw=0.6)
    ax = axes[1]
    parts = ["jar_powder", "cone_sweep_powder", "plate_and_sonotrode_splats", "cup_or_bowl_puddle", "crucible_skull_and_nozzle_globs"]
    colors = [BLUE, "#84b9f3", ORANGE, "#f2a600", GRAY]
    bottom = np.zeros(len(valid))
    for p, c in zip(parts, colors):
        vals = np.array([100 * r.mass.get(p, 0) / r.charge_g if r.charge_g else 0 for r in valid])
        ax.bar(range(len(valid)), vals, bottom=bottom, color=c, edgecolor="white", linewidth=1, label=p.split("_")[0])
        bottom += vals
    ax.set_xticks(range(len(valid)), [r.code for r in valid]); ax.set_ylabel("Share of charge (%)")
    ax.legend(fontsize=6.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12)); ax.set_ylim(0, 105)
    ax = axes[2]
    _, summary = check_bar(block_a)
    rows = [r for r in summary["rows"] if r[3] == "cv_pct"]
    ax.barh([r[0].replace("_um", "").replace("_ppm", "") for r in rows], [r[4] for r in rows], color=BLUE, height=0.5)
    for i, r in enumerate(rows):
        ax.plot([r[5], r[5]], [i - 0.35, i + 0.35], color=INK, lw=1.5)
    ax.set_xlabel("Run-to-run CV (%)  | = bar"); ax.grid(axis="x", color=GRID_C, lw=0.6)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out / f"fig2-repeatability.{ext}", bbox_inches="tight")
    plt.close(fig)


def si_in_charge(r: Run) -> float | None:
    if r.powder_wt_pct is None:
        return None
    w = r.powder_wt_pct / 100
    return (1 - w) * SI_6063 + w * SI_4047


def fig_fidelity(block_b: list[Run], out: Path) -> list[str]:
    pts = [(si_in_charge(r), np.mean([v[1] for v in r.si_eds.values()]), r.si_icp, r.code)
           for r in block_b if si_in_charge(r) is not None and r.si_eds]
    if len(pts) < 3:
        return ["Block B: fewer than 3 runs with charge and EDS data; no fit yet."]
    x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
    fit = stats.linregress(x, y)
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    lim = [0, max(x.max(), y.max()) * 1.15]
    ax.plot(lim, lim, color=GRAY, lw=1, ls="--", label="1:1")
    ax.scatter(x, y, color=BLUE, s=24, zorder=3, label="EDS (jar mean)")
    icp = [(p[0], p[2]) for p in pts if p[2] is not None]
    if icp:
        ax.scatter(*zip(*icp), marker="s", facecolor="white", edgecolor=ORANGE, s=28, zorder=3, label="ICP-OES")
    ax.set_xlim(lim); ax.set_ylim(lim); ax.set_xlabel("Si in charge (wt%)"); ax.set_ylabel("Si in powder (wt%)")
    ax.legend(fontsize=7); ax.grid(color=GRID_C, lw=0.6)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(out / f"fig3b-si-fidelity.{ext}", bbox_inches="tight")
    plt.close(fig)
    return [f"Block B: slope {fit.slope:.3f} ± {fit.stderr:.3f}, intercept {fit.intercept:.3f} wt%, "
            f"R² {fit.rvalue ** 2:.3f}, n = {len(pts)} (EDS jar means against Si computed from the weighed charge, "
            f"with 6063 at {SI_6063} and 4047 at {SI_4047} wt% Si nominal)."]


def simulate(tmp: Path, seed: int = 1) -> None:
    """Write simulated records for the self-test. Never used for the paper."""
    rng = random.Random(seed)
    for i in range(1, 8):
        valid = i != 3
        halves = []
        d50 = rng.gauss(48, 3)
        for h in "AB":
            halves.append({"half": h, "d10_um": d50 * 0.62 + rng.gauss(0, 0.6), "d50_um": d50 + rng.gauss(0, 0.8),
                           "d90_um": d50 * 1.55 + rng.gauss(0, 1.2)})
        mass = {"jar_powder": rng.gauss(150, 10), "cone_sweep_powder": rng.gauss(20, 3),
                "plate_and_sonotrode_splats": rng.gauss(30, 5), "cup_or_bowl_puddle": rng.gauss(30, 6),
                "crucible_skull_and_nozzle_globs": rng.gauss(15, 3)}
        rec = {"run": {"code": f"A{i}", "run_order": i, "valid": valid},
               "setup": {"plate_id": "P1" if i < 5 else "P2"},
               "charge": {"total_g": 250, "powder_wt_pct": 0},
               "mass_balance_g": mass,
               "yields_pct": {"powder": 68 + rng.gauss(0, 4), "in_range": 30 + rng.gauss(0, 3), "closure": 98},
               "psd": halves,
               "morphology": [{"half": h, "circularity_mean": 0.9 + rng.gauss(0, 0.01)} for h in "AB"],
               "composition": {"eds_si_wt_pct": {"top": {"n": 30, "mean": 0.4 + rng.gauss(0, 0.05), "sd": 0.1}}}}
        (tmp / f"a{i}.yaml").write_text(yaml.safe_dump(rec))
    for j, w in enumerate([0, 7.5, 15, 22.5, 30], start=1):
        si = (1 - w / 100) * SI_6063 + w / 100 * SI_4047
        rec = {"run": {"code": f"B{j}", "run_order": 7 + j, "valid": True}, "charge": {"total_g": 250, "powder_wt_pct": w},
               "composition": {"eds_si_wt_pct": {p: {"n": 30, "mean": si * 0.95 + rng.gauss(0, 0.1), "sd": 0.3}
                                                 for p in ("top", "middle", "bottom")}}}
        (tmp / f"b{j}.yaml").write_text(yaml.safe_dump(rec))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", help="glob of run.yaml records")
    ap.add_argument("--out", type=Path, default=Path("figures"))
    ap.add_argument("--selftest", action="store_true", help="simulated records; outputs to /tmp only")
    a = ap.parse_args()
    if a.selftest:
        tmp = Path(tempfile.mkdtemp(prefix="atomizer-selftest-"))
        simulate(tmp)
        a.runs, a.out = str(tmp / "*.yaml"), tmp
        print("SELF-TEST on simulated records in", tmp)
    if not a.runs:
        ap.error("--runs or --selftest")
    runs = [load(p) for p in sorted(glob.glob(a.runs))]
    block_a = [r for r in runs if r.code.startswith("A")]
    block_b = [r for r in runs if r.code.startswith("B")]
    a.out.mkdir(parents=True, exist_ok=True)
    lines, _ = check_bar(block_a)
    report = ["# Repeatability check (Block A) and Si fidelity (Block B)", "",
              f"{len(runs)} records read from `{a.runs}`.", ""] + lines + [""] + fig_fidelity(block_b, a.out)
    if block_a:
        fig_repeatability(block_a, a.out)
    (a.out / "repeatability-check.md").write_text("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
