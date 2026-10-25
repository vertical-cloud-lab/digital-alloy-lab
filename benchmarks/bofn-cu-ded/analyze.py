"""Aggregate the copper/DED sweep: curves against new spend, cost to target, speed-ups, and the
screen-audit, two-step and funnel tables. Writes tables.md.

    python analyze.py
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch

from bofn_alloy import COSTS, D, M_REF, AlloyTruth

HERE = Path(__file__).parent
RES = HERE / "results"
GRID = np.arange(0, 100_001, 250.0)
CELLS = [(1.0, 1.0), (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
CELL_NAMES = {(1.0, 1.0): "both screens biased", (0.0, 0.0): "both screens right", (1.0, 0.0): "crack screen biased only",
              (0.0, 1.0): "one-hour screen biased only"}
SHORT = {
    "pkgfn": "pKGFN: picks the stage",
    "pkgfn_screen": "pKGFN, trusts the screens",
    "pkgfn_audit": "pKGFN, screens + audit",
    "mines_only": "pKGFN, no Utah stage",
    "eifn": "BOFN, full pipeline",
    "eifn_reuse": "BOFN + lot reuse",
    "tiered": "Tiered screening",
    "funnel": "Fixed top-k funnel",
    "ei": "Standard BO",
    "random": "Random",
}
KINDS = tuple(SHORT)
PKGFN_KINDS = ("pkgfn", "pkgfn_screen", "pkgfn_audit", "mines_only")


def cell_dir(cell):
    return RES / f"k{cell[0]:g}e{cell[1]:g}"


@lru_cache
def optimum(kappa: float, eta: float = 1.0) -> float:
    """J* per cell: read from truth_tables.json (check_truth.py), else the same multi-start search."""
    p = HERE / "truth_tables.json"
    if p.exists():
        for r in json.loads(p.read_text()):
            if (r["kappa"], r["eta"]) == (kappa, eta):
                return r["optimum"]
    t = AlloyTruth(kappa, eta)
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400_000, D, generator=g)
    y = t.objective(X)
    best = float(y.max())
    for x0 in X[y.topk(20).indices]:
        xb, yb = x0, float(t.objective(x0.unsqueeze(0))[0])
        for scale in (0.03, 0.01, 0.003):
            P = (xb + scale * torch.randn(4000, D, generator=g)).clamp(0, 1)
            yp = t.objective(P)
            if float(yp.max()) > yb:
                xb, yb = P[yp.argmax()], float(yp.max())
        best = max(best, yb)
    return best


@lru_cache
def load(cell):
    out = {}
    for p in sorted(cell_dir(cell).glob("*.json")):
        r = json.loads(p.read_text())
        out.setdefault(r["kind"], []).append(r)
    for k in out:
        out[k].sort(key=lambda r: r["seed"])
    return out


def curve(rows, metric="best_validated"):
    """Step function of `metric` on GRID (running best for best_validated)."""
    spent = np.array([r["spent"] for r in rows])
    vals = np.array([r[metric] if r[metric] == r[metric] else -np.inf for r in rows])
    if metric == "best_validated":
        vals = np.maximum.accumulate(vals)
    idx = np.searchsorted(spent, GRID, side="right") - 1
    return np.where(idx >= 0, vals[np.clip(idx, 0, None)], np.nan)


def curves(runs, cell, metric="best_validated"):
    return np.stack([curve(r["rows"], metric) for r in runs]) / optimum(*cell)


def cost_to(c, target):
    """First grid cost where each seed's curve reaches target (inf if never)."""
    hit = c >= target
    return np.where(hit.any(1), GRID[hit.argmax(1)], np.inf)


def first_cost(mean_curve, target):
    hit = mean_curve >= target - 1e-12
    return GRID[hit.argmax()] if hit.any() else np.inf


def _ratio(cp, cb):
    """Spend the baseline needs to reach its own final mean level, over the spend the method needs."""
    tgt = np.nanmean(cb[:, -1])
    return first_cost(np.nanmean(cb, 0), tgt) / max(first_cost(np.nanmean(cp, 0), tgt), GRID[1])


def speedup(Cp, Cb, n=2000, seed=0, matched=None):
    """Point estimate, 90% bootstrap CI with seeds resampled independently per policy, and (if
    `matched` gives the row indices of shared seeds) the 90% CI of a matched-seed bootstrap."""
    rng = np.random.default_rng(seed)
    est = _ratio(Cp, Cb)
    bs = np.array([_ratio(Cp[rng.integers(0, len(Cp), len(Cp))], Cb[rng.integers(0, len(Cb), len(Cb))]) for _ in range(n)])
    out = {"est": est, "lo": np.percentile(bs, 5), "hi": np.percentile(bs, 95), "p3": float(np.mean(bs >= 3))}
    if matched is not None:
        ip, ib = matched
        bm = []
        for _ in range(n):
            j = rng.integers(0, len(ip), len(ip))
            bm.append(_ratio(Cp[ip[j]], Cb[ib[j]]))
        out["mlo"], out["mhi"] = np.percentile(bm, 5), np.percentile(bm, 95)
    return out


def at(c, spend):
    return c[:, int(np.searchsorted(GRID, spend))]


def fmt_cost(v):
    return ">$100k" if not np.isfinite(v) else f"${v / 1e3:.0f}k" if v >= 1e3 or v == 0 else f"${v / 1e3:.2f}k"


# --------------------------------------------------------------------------- tables
def markdown_table(cell, metric="best_validated", kinds=KINDS):
    data = load(cell)
    rows = ["| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median $ to 80% |", "|---|---|---|---|---|---|---|---|"]
    for k in kinds:
        if k not in data:
            continue
        c = curves(data[k], cell, metric)
        cells = [f"{np.nanmean(at(c, s)) * 100:.0f}% ± {np.nanstd(at(c, s)) / np.sqrt(len(c)) * 100:.0f}" for s in (25_000, 50_000, 100_000)]
        for t in (0.6, 0.7, 0.8):
            ct = cost_to(c, t)
            cells.append(f"{fmt_cost(np.median(ct))} ({np.isfinite(ct).mean():.0%} of seeds)")
        rows.append(f"| {SHORT[k]} | {len(c)} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def matched_idx(A, B):
    sa, sb = [r["seed"] for r in A], [r["seed"] for r in B]
    common = sorted(set(sa) & set(sb))
    return np.array([sa.index(s) for s in common]), np.array([sb.index(s) for s in common])


def speedup_table(cell, base="tiered", kinds=("pkgfn", "eifn_reuse", "eifn", "ei", "random", "pkgfn_screen", "pkgfn_audit", "mines_only", "funnel")):
    data = load(cell)
    if base not in data:
        return ""
    Cb = curves(data[base], cell)
    tgt = np.nanmean(Cb[:, -1])
    rows = [f"Target: {SHORT[base].lower()}'s mean at $100k, {tgt:.1%} of the optimum, which it first reaches at "
            f"{fmt_cost(first_cost(np.nanmean(Cb, 0), tgt))}.", "",
            "| Method | n | $ to reach the target (mean curve) | speed-up | 90% bootstrap CI (seeds resampled per policy) | 90% CI, matched-seed bootstrap | P(speed-up ≥ 3) |", "|---|---|---|---|---|---|---|"]
    for k in kinds:
        if k not in data or k == base:
            continue
        Cp = curves(data[k], cell)
        s = speedup(Cp, Cb, matched=matched_idx(data[k], data[base]))
        rows.append(f"| {SHORT[k]} | {len(Cp)} | {fmt_cost(first_cost(np.nanmean(Cp, 0), tgt))} | **{s['est']:.1f}×** | {s['lo']:.1f}–{s['hi']:.1f} | {s['mlo']:.1f}–{s['mhi']:.1f} | {s['p3']:.2f} |")
    return "\n".join(rows)


def paired(cell, ref, base, spends=(25_000, 50_000, 100_000)):
    """Seed-matched comparison with the Wilcoxon signed-rank test (both start from the same seed alloys)."""
    from scipy.stats import wilcoxon

    data = load(cell)
    if ref not in data or base not in data:
        return []
    A = {r["seed"]: curve(r["rows"]) / optimum(*cell) for r in data[ref]}
    B = {r["seed"]: curve(r["rows"]) / optimum(*cell) for r in data[base]}
    seeds = sorted(set(A) & set(B))
    out = []
    for s_ in spends:
        i = int(np.searchsorted(GRID, s_))
        a, b = np.array([A[s][i] for s in seeds]), np.array([B[s][i] for s in seeds])
        d = a - b
        p = wilcoxon(d).pvalue if np.any(d != 0) else 1.0
        out.append({"spend": s_, "n": len(seeds), "ref": a.mean(), "base": b.mean(), "diff": d.mean(), "wins": int((d > 0).sum()), "ties": int((d == 0).sum()),
                    "losses": int((d < 0).sum()), "p": p})
    return out


def paired_table(cell, ref="pkgfn", bases=("tiered", "eifn", "eifn_reuse", "ei", "random", "mines_only", "pkgfn_screen", "pkgfn_audit", "funnel")):
    rows = [f"| {SHORT[ref]} against | n | $25k: mean difference (wins/ties/losses; p) | $50k | $100k |", "|---|---|---|---|---|"]
    for b in bases:
        res = paired(cell, ref, b)
        if not res:
            continue
        rows.append(f"| {SHORT[b]} | {res[0]['n']} | " + " | ".join(f"{r['diff'] * 100:+.0f} points ({r['wins']}/{r['ties']}/{r['losses']}; p = {r['p']:.2g})" for r in res) + " |")
    return "\n".join(rows)


def sensitivity_table(spend=100_000, kinds=KINDS):
    rows = ["| Policy | " + " | ".join(f"({c[0]:g}, {c[1]:g}) {CELL_NAMES[c]}" for c in CELLS) + " |", "|---|" + "---|" * len(CELLS)]
    for k in kinds:
        cells = []
        for c in CELLS:
            data = load(c)
            if k not in data:
                cells.append("")
                continue
            v = at(curves(data[k], c), spend) * 100
            cells.append(f"{np.nanmean(v):.0f}% ± {np.nanstd(v) / np.sqrt(len(v)):.0f} (n = {len(v)})")
        if any(cells):
            rows.append(f"| {SHORT[k]} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def allocation_table(cell, kinds=KINDS):
    data = load(cell)
    stages = list(COSTS)
    rows = ["| Policy | n | " + " | ".join(f"{g} (${COSTS[g]:,.0f}{'+' if g == 'M' else ''})" for g in stages) + " | new lots | Mines sessions that paid a scale-up |", "|---|---|" + "---|" * (len(stages) + 2)]
    for k in kinds:
        if k not in data:
            continue
        runs = data[k]
        mean = {g: np.mean([r["counts"][g] for r in runs]) for g in stages}
        lots = np.mean([len(r["lots"]) - 5 for r in runs])
        scale = np.mean([sum(1 for a, b in zip(r["rows"], r["rows"][1:]) if b["action"] == "M" and b["spent"] - a["spent"] > COSTS["M"] + 1) for r in runs]) if k in PKGFN_KINDS else float("nan")
        rows.append(f"| {SHORT[k]} | {len(runs)} | " + " | ".join(f"{mean[g]:.1f}" for g in stages) + f" | {lots:.1f} | {'' if scale != scale else f'{scale:.1f}'} |")
    return "\n".join(rows)


def _m_true(truth, b):
    """True 30-day immersion index of a build (the truth ignores the w coordinate)."""
    ni, al, fe = b["c"][0], b["c"][1], b["c"][2]
    return float(truth.node("m", torch.tensor([ni, al, fe, b["rho_m"], b["beta"], b["w"]])))


def _concordance(w, m):
    """Share of pairs that the one-hour screen and the 30-day immersion order the same way."""
    w, m = np.asarray(w), np.asarray(m)
    i, j = np.triu_indices(len(w), 1)
    s = np.sign(w[i] - w[j]) * np.sign(m[i] - m[j])
    s = s[s != 0]
    return (np.mean(s > 0), len(s)) if len(s) else (np.nan, 0)


def _boot_mean(vals, n=4000, seed=0):
    vals = np.asarray([v for v in vals if v == v])
    if len(vals) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    bs = [np.mean(rng.choice(vals, len(vals))) for _ in range(n)]
    return vals.mean(), np.percentile(bs, 5), np.percentile(bs, 95)


def _wilson(k, n, z=1.645):
    if n == 0:
        return np.nan, np.nan, np.nan
    p = k / n
    den = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return p, max(c - h, 0.0), min(c + h, 1.0)


def audit_summary(cell, kind="pkgfn_audit"):
    """What the audit lets the lab estimate about the one-hour screen, and the same from the truth."""
    data = load(cell)
    if kind not in data:
        return None
    truth = AlloyTruth(*cell)
    conc_seen, conc_true, fr_seen, fr_true, fp_seen = [], [], [0, 0], [0, 0], [0, 0]
    how = {}
    for r in data[kind]:
        imm = [b for b in r["builds"] if b["w"] is not None and b["m"] is not None]
        c, _ = _concordance([b["w"] for b in imm], [b["m"] for b in imm])
        conc_seen.append(c)
        scr = [b for b in r["builds"] if b["w"] is not None]
        c2, _ = _concordance([b["w"] for b in scr], [_m_true(truth, b) for b in scr])
        conc_true.append(c2)
        for e in r.get("events", []):
            how[e["how"]] = how.get(e["how"], 0) + 1
            if not e["screen_pass"]:  # an immersion the screen would have stopped (audit or near the cutoff)
                fr_seen[0] += int(e["immersion_pass"])
                fr_seen[1] += 1
            else:
                fp_seen[0] += int(not e["immersion_pass"])
                fp_seen[1] += 1
        gate = r["w_gate_final"]
        for b in scr:  # oracle: every screened build, judged by its true immersion index against the final gate
            if b["w"] < gate:
                fr_true[0] += int(_m_true(truth, b) >= r["m_ref"])
                fr_true[1] += 1
    return {"n": len(data[kind]), "conc_seen": _boot_mean(conc_seen), "conc_true": _boot_mean(conc_true), "fr_seen": (*_wilson(*fr_seen), fr_seen[1]),
            "fr_true": (*_wilson(*fr_true), fr_true[1]), "fp_seen": (*_wilson(*fp_seen), fp_seen[1]), "how": how}


def audit_table():
    rows = ["| Cell | runs | screen ranks pairs as immersion does: audited builds (90% CI) | same, every screened build judged by the truth | screen-stopped builds that pass immersion: audit estimate (90% CI; n) | same, truth on every screen-stopped build (n) | screen-passed builds that fail immersion (90% CI; n) | why each immersion ran |",
            "|---|---|---|---|---|---|---|---|"]
    for c in CELLS:
        a = audit_summary(c)
        if a is None:
            continue
        cs, ct, fr, ft, fp = a["conc_seen"], a["conc_true"], a["fr_seen"], a["fr_true"], a["fp_seen"]
        rows.append(f"| ({c[0]:g}, {c[1]:g}) | {a['n']} | {cs[0]:.0%} ({cs[1]:.0%}–{cs[2]:.0%}) | {ct[0]:.0%} ({ct[1]:.0%}–{ct[2]:.0%}) | {fr[0]:.0%} ({fr[1]:.0%}–{fr[2]:.0%}; {fr[3]}) | "
                    f"{ft[0]:.0%} ({ft[3]}) | {fp[0]:.0%} ({fp[1]:.0%}–{fp[2]:.0%}; {fp[3]}) | " + ", ".join(f"{k} {v}" for k, v in sorted(a["how"].items())) + " |")
    return "\n".join(rows)


def _mines_to(r, ystar, target):
    """Mines sessions bought before the best alloy demonstrated first reaches `target` (None if never)."""
    n = 0
    for row in r["rows"]:
        if row["action"] in ("M", "full", "reuse", "screen-fail", "utah-fail"):
            n += row["action"] != "utah-fail"
        if row["best_validated"] / ystar >= target:
            return n
    return None


def two_step_table(cell, kinds=("pkgfn", "mines_only", "eifn_reuse", "tiered")):
    data = load(cell)
    ys = optimum(*cell)
    rows = ["| Policy | n | $25k | $50k | $100k | median $ to 60% | median $ to 70% | median Mines sessions to 60% | median Mines sessions to 70% | Utah visits per $100k | Mines sessions per $100k |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in kinds:
        if k not in data:
            continue
        runs = data[k]
        c = curves(runs, cell)
        cells = [f"{np.nanmean(at(c, s)) * 100:.0f}% ± {np.nanstd(at(c, s)) / np.sqrt(len(c)) * 100:.0f}" for s in (25_000, 50_000, 100_000)]
        cells += [fmt_cost(np.median(cost_to(c, t))) for t in (0.6, 0.7)]
        for t in (0.6, 0.7):
            m = [_mines_to(r, ys, t) for r in runs]
            reached = [v for v in m if v is not None]
            med = np.median([v if v is not None else np.inf for v in m])
            cells.append(f"{'never' if not np.isfinite(med) else f'{med:.0f}'} ({len(reached)}/{len(m)} reached)")
        cells += [f"{np.mean([r['counts']['U'] for r in runs]):.1f}", f"{np.mean([r['counts']['M'] for r in runs]):.1f}"]
        rows.append(f"| {SHORT[k]} | {len(runs)} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def funnel_table(cell):
    data = load(cell)
    if "funnel" not in data:
        return ""
    ys = optimum(*cell)
    runs = data["funnel"]
    names = [g["gate"] for g in runs[0]["gates"]]
    rows = [f"Mean over {len(runs)} seeds. A false rejection is a rejected composition (or build) whose best achievable objective, from the truth, beats the best alloy the funnel demonstrated with the whole $100k.", "",
            "| Gate | rule | kept | rejected | false rejections | best rejected candidate's potential (% of optimum) |", "|---|---|---|---|---|---|"]
    for i, name in enumerate(names):
        G = [r["gates"][i] for r in runs]
        best = [g["best_rejected_potential"] for g in G if g["best_rejected_potential"] is not None]
        rows.append(f"| {name} | {G[0]['rule']} | {np.mean([g['n_kept'] for g in G]):.1f} | {np.mean([g['n_rejected'] for g in G]):.1f} | {np.mean([g['false_rejections'] for g in G]):.1f} | "
                    f"{np.mean(best) / ys:.0%} |")
    fin = np.array([r["final_best_validated"] for r in runs]) / ys
    rows += ["", f"Best alloy the funnel demonstrated with the whole $100k: {fin.mean():.0%} ± {fin.std() / np.sqrt(len(fin)):.0%} of the optimum."]
    return "\n".join(rows)


def quality_table():
    rows = ["| Cell | runs | GP fits | fit failures | pKGFN-type purchases chosen by the EI fallback (KG flat) |", "|---|---|---|---|---|"]
    for c in CELLS:
        data = load(c)
        runs = [r for v in data.values() for r in v]
        if not runs:
            continue
        calls = sum(r["gp_fits"]["calls"] for r in runs)
        fails = sum(r["gp_fits"]["failures"] for r in runs)
        fb = [(sum(1 for x in r["rows"][1:] if x.get("fallback")), len(r["rows"]) - 1) for v in data.values() for r in v if r["kind"] in PKGFN_KINDS]
        share = sum(a for a, _ in fb) / max(sum(b for _, b in fb), 1)
        rows.append(f"| ({c[0]:g}, {c[1]:g}) | {len(runs)} | {calls:,} | {fails} | {share:.0%} of {sum(b for _, b in fb):,} |")
    return "\n".join(rows)


def report():
    L = ["# Tables (written by `analyze.py`)", "", "Best alloy demonstrated (deposited at Mines and carried through tensile and immersion), as a percentage of the true optimum of each cell, mean ± SE over seeds. New spend only; the shared seed data is sunk.", ""]
    for c in CELLS:
        if not load(c):
            continue
        L += [f"## Cell (kappa, eta) = ({c[0]:g}, {c[1]:g}): {CELL_NAMES[c]}; optimum J* = {optimum(*c):.3f}", "", markdown_table(c), ""]
        if c == (1.0, 1.0):
            L += ["Scored by the deposited alloy each policy's own model ranks best (`rec_printed`), which credits builds not yet tested:", "", markdown_table(c, "rec_printed"), ""]
        st = speedup_table(c)
        if st:
            L += ["### Speed-up over tiered screening", "", st, ""]
        L += ["### Matched seeds (Wilcoxon signed-rank)", "", paired_table(c), "", "### Purchases per $100k (mean over seeds, new purchases only)", "", allocation_table(c), ""]
        tt = two_step_table(c)
        if "mines_only" in load(c):
            L += ["### What the two-step DED split buys (pKGFN with and without the Utah stage)", "", tt, ""]
        ft = funnel_table(c)
        if ft:
            L += ["### The fixed top-k funnel, gate by gate", "", ft, ""]
    L += ["## Sensitivity over the four cells", "", "At $100k:", "", sensitivity_table(100_000), "", "At $50k:", "", sensitivity_table(50_000), ""]
    L += ["## Screen audit (Advance 5)", "", "From the `pkgfn_audit` runs: about one in ten builds the one-hour screen stops goes on to immersion anyway, plus those within 0.03 of the cutoff. "
          f"`m_ref` = {M_REF:.3f}. The truth columns judge every screened build of the same runs by its true immersion index, which a lab cannot see; they say whether the audit's estimate is right.", "", audit_table(), ""]
    L += ["## Quality: GP fits and the KG fallback", "", quality_table(), ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    md = report()
    (HERE / "tables.md").write_text(md)
    print(md)
