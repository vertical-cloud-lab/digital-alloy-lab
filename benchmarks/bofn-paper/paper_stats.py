"""Statistics for the BOFN methods write-ups (issue #121): every comparison with a
matched-seed bootstrap interval.

    python paper_stats.py                 # all three kappas, writes paper-stats/
    python paper_stats.py --check         # also prints which runs are missing

Which runs: the "paper set", i.e. every run written by this port's run_sweep.py
with provenance (settings, git commit, package versions, purchase log):

    kappa = 1    results-rerun/k1 (7 policies x seeds 0-19) + results-kgfn/k1 (KGFN, 0-19)
    kappa = 0.5  results-rerun/k0.5 (7 policies x seeds 0-15) + results-kgfn/k0.5 (KGFN, 0-15)
    kappa = 0    results-rerun/k0 (7 policies x seeds 0-15) + results-kgfn/k0 (KGFN, 0-15)

The stored MS&T26 runs (results/) are not read here: at kappa = 1 the paper set
reproduces them action for action (results-rerun/compare_k1.txt), and at kappa =
0 and 0.5 the overlap is checked in results-rerun/compare_k0.txt and
compare_k0.5.txt. Only seeds that all eight policies have are used, so every
comparison is on the same seeds.

Metric: "best alloy demonstrated", the true objective of the best alloy that has
been printed and tensile-tested, as a fraction of the optimum at that kappa
(analyze.optimum), on a $250 grid of new spend. Per run we take its value at
$25k, $50k and $100k, and its mean over the whole $0-100k grid ("anytime" score,
the normalized area under the curve, which needs no choice of budget).

Intervals: percentile bootstrap over seeds, B = 10,000, numpy seed 0. Because a
seed fixes the starting data for every policy, seeds are resampled jointly: each
draw takes the same seeds for both policies (matched-seed bootstrap). For one
policy's mean the same resampling is applied to its own seeds. 95% intervals are
the default; the speed-up table also gives the 90% interval the MS&T26 numbers
used; its endpoints move by up to about 0.1 between bootstrap seeds (the
statistic is the first $250 grid step a mean curve crosses, so its bootstrap
distribution is lumpy), and the 90% lower end by up to 0.3 at kappa = 1. No
interval is corrected for multiplicity; with 28 pairs x 4 metrics x 3
kappas, read single intervals that only just exclude 0 with care.

Outputs (paper-stats/): policies.csv, pairwise.csv, contrasts.csv, speedup.csv,
allocation.csv, SUMMARY.md (the tables the drafts quote), numbers.tex (one LaTeX
macro per quoted number, so both drafts print the same values) and the LaTeX
tables table-results.tex and table-contrasts.tex.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np

from analyze import GRID, cost_to, curve, first_cost, optimum

HERE = Path(__file__).parent
OUT = HERE / "paper-stats"
KAPPAS = (0.0, 0.5, 1.0)
SOURCES = (HERE / "results-rerun", HERE / "results-kgfn")
POLICIES = ("pkgfn", "kgfn", "eifn_reuse", "eifn", "ei", "tiered", "tiered_naive", "random")
LABEL = {
    "pkgfn": "pKGFN (partial, KG per $)",
    "kgfn": "KGFN (full chain, KG per $)",
    "eifn_reuse": "BOFN + powder reuse (partial, EI per $)",
    "eifn": "BOFN (full chain, EI)",
    "ei": "Standard BO (EI, one GP)",
    "tiered": "Tiered screening",
    "tiered_naive": "Tiered, no powder reuse",
    "random": "Random",
}
SHORT = {
    "pkgfn": "pKGFN", "kgfn": "KGFN", "eifn_reuse": "BOFN+reuse", "eifn": "BOFN",
    "ei": "Std BO", "tiered": "Tiered", "tiered_naive": "Tiered (no reuse)", "random": "Random",
}
AT = (25_000, 50_000, 100_000)
METRICS = ("v25", "v50", "v100", "auc")
MLABEL = {"v25": "$25k", "v50": "$50k", "v100": "$100k", "auc": "anytime ($0-100k)"}
TARGETS = (0.6, 0.7, 0.8)
B = 10_000
SEED_SETS = {1.0: range(20), 0.5: range(16), 0.0: range(16)}
# The 2 x 2 of {KG per $, EI per $} x {partial, full chain}: (name, plus, minus) or a 4-term interaction
CONTRASTS = (
    ("partial - full, KG", ("pkgfn",), ("kgfn",)),
    ("partial - full, EI", ("eifn_reuse",), ("eifn",)),
    ("KG - EI, partial", ("pkgfn",), ("eifn_reuse",)),
    ("KG - EI, full chain", ("kgfn",), ("eifn",)),
    ("interaction (partial gain under KG minus under EI)", ("pkgfn", "eifn"), ("kgfn", "eifn_reuse")),
)


def fmt_kappa(k):
    return f"{k:g}"


def load_paper(kappa, check=False):
    """{policy: {seed: run}} from the paper set; warns about missing runs."""
    runs = {p: {} for p in POLICIES}
    for root in SOURCES:
        for p in sorted((root / f"k{fmt_kappa(kappa)}").glob("*.json")):
            r = json.loads(p.read_text())
            if r["kind"] in runs:
                runs[r["kind"]][r["seed"]] = r
    if check:
        want = set(SEED_SETS[kappa])
        for k, v in runs.items():
            miss = sorted(want - set(v))
            if miss:
                print(f"  kappa={kappa:g} {k}: missing seeds {miss}")
    return runs


def per_run(run, ystar):
    c = curve(run["rows"], "best_validated") / ystar
    out = {f"v{a // 1000}": float(c[int(np.searchsorted(GRID, a))]) for a in AT}
    out["auc"] = float(np.mean(c))
    for t in TARGETS:
        out[f"cost{int(t * 100)}"] = float(cost_to(c[None], t)[0])
    return out, c


def boot_idx(n, rng):
    return rng.integers(0, n, size=(B, n))


def pct(x, level):
    lo = (1 - level) / 2
    return float(np.percentile(x, 100 * lo)), float(np.percentile(x, 100 * (1 - lo)))


def wilcoxon_p(d):
    from scipy.stats import wilcoxon

    d = np.asarray(d)
    return float(wilcoxon(d).pvalue) if np.any(d != 0) else 1.0


def speedup_est(Cp, Cb):
    """analyze.speedup's statistic: spend the baseline's mean curve needs to reach
    its own $100k mean, over the spend the policy's mean curve needs (0 if never)."""
    tgt = np.nanmean(Cb[:, -1])
    cp = first_cost(np.nanmean(Cp, 0), tgt)
    return first_cost(np.nanmean(Cb, 0), tgt) / max(cp, GRID[1]) if np.isfinite(cp) else 0.0


def analyse(kappa, check=False):
    ystar = optimum(kappa)
    runs = load_paper(kappa, check)
    seeds = sorted(set.intersection(*(set(v) for v in runs.values()))) if all(runs.values()) else []
    if not seeds:
        return None
    rng = np.random.default_rng(0)
    idx = boot_idx(len(seeds), rng)  # one set of resamples per kappa, shared by every statistic
    M, C = {}, {}
    for p in POLICIES:
        vals = [per_run(runs[p][s], ystar) for s in seeds]
        M[p] = {m: np.array([v[0][m] for v in vals]) for m in vals[0][0]}
        C[p] = np.stack([v[1] for v in vals])
    res = {"kappa": kappa, "ystar": ystar, "seeds": seeds, "n": len(seeds), "policies": [], "pairwise": [], "contrasts": [], "speedup": [], "allocation": []}
    for p in POLICIES:
        row = {"kappa": kappa, "policy": p, "n": len(seeds)}
        for m in METRICS:
            x = M[p][m]
            bs = x[idx].mean(1)
            row[f"{m}_mean"] = x.mean()
            row[f"{m}_se"] = x.std(ddof=1) / math.sqrt(len(x))
            row[f"{m}_lo"], row[f"{m}_hi"] = pct(bs, 0.95)
        for t in TARGETS:
            ct = M[p][f"cost{int(t * 100)}"]
            row[f"cost{int(t * 100)}_median"] = float(np.median(ct))
            row[f"cost{int(t * 100)}_reached"] = float(np.isfinite(ct).mean())
        # purchases per stage (new spend only), from the purchase log
        cnt = {g: [] for g in "CALT"}
        for s in seeds:
            pur = runs[p][s].get("purchases") or []
            for g in "CALT":
                cnt[g].append(sum(1 for q in pur if q[0] == g))
        alloc = {"kappa": kappa, "policy": p, "n": len(seeds)}
        for g in "CALT":
            alloc[f"{g}_mean"] = float(np.mean(cnt[g]))
        fb = [sum(1 for r in runs[p][s]["rows"] if r.get("fallback")) for s in seeds]
        nrows = [sum(1 for r in runs[p][s]["rows"] if r["action"] not in ("init", "C-screen")) for s in seeds]
        alloc["fallback_share"] = float(np.sum(fb) / max(np.sum(nrows), 1)) if p in ("pkgfn", "kgfn") else float("nan")
        alloc["gp_fit_failures"] = int(sum((runs[p][s].get("gp_fits") or {}).get("failures", 0) for s in seeds))
        alloc["gp_fits"] = int(sum((runs[p][s].get("gp_fits") or {}).get("calls", 0) for s in seeds))
        alloc["wall_s_mean"] = float(np.mean([runs[p][s].get("wall_s", float("nan")) for s in seeds]))
        res["policies"].append(row)
        res["allocation"].append(alloc)
    for a, b in combinations(POLICIES, 2):
        row = {"kappa": kappa, "a": a, "b": b, "n": len(seeds)}
        for m in METRICS:
            dlt = M[a][m] - M[b][m]
            bs = dlt[idx].mean(1)
            row[f"{m}_diff"] = dlt.mean()
            row[f"{m}_lo"], row[f"{m}_hi"] = pct(bs, 0.95)
            row[f"{m}_wins"], row[f"{m}_ties"] = int((dlt > 1e-12).sum()), int((np.abs(dlt) <= 1e-12).sum())
            row[f"{m}_p"] = wilcoxon_p(dlt)
        res["pairwise"].append(row)
    for name, plus, minus in CONTRASTS:
        row = {"kappa": kappa, "contrast": name, "n": len(seeds)}
        for m in METRICS:
            dlt = sum(M[p][m] for p in plus) - sum(M[p][m] for p in minus)
            bs = dlt[idx].mean(1)
            row[f"{m}_diff"] = dlt.mean()
            row[f"{m}_lo"], row[f"{m}_hi"] = pct(bs, 0.95)
        res["contrasts"].append(row)
    for base in ("tiered", "ei"):
        for p in POLICIES:
            if p == base:
                continue
            est = speedup_est(C[p], C[base])
            bs = np.array([speedup_est(C[p][i], C[base][i]) for i in idx])
            lo95, hi95 = pct(bs, 0.95)
            lo90, hi90 = pct(bs, 0.90)
            res["speedup"].append({"kappa": kappa, "policy": p, "over": base, "n": len(seeds), "target": float(np.nanmean(C[base][:, -1])),
                                   "est": est, "lo95": lo95, "hi95": hi95, "lo90": lo90, "hi90": hi90,
                                   "p_not_reached": float(np.mean(bs == 0)), "p_ge_3x": float(np.mean(bs >= 3))})
    return res


def write_csv(path, rows):
    if not rows:
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})


def pc(x):
    return f"{100 * x:.0f}"


def pts(x):
    return f"{100 * x:+.1f}"


def ci_pts(lo, hi):
    return f"[{100 * lo:+.1f}, {100 * hi:+.1f}]"


def money(x):
    return ">$100k" if not np.isfinite(x) else f"${x / 1e3:.0f}k"


def summary_md(all_res):
    L = ["# Paper statistics (generated by `paper_stats.py`; do not edit by hand)", ""]
    L.append("Best alloy demonstrated, % of the optimum at that κ. Intervals: 95% percentile bootstrap over seeds "
             "(B = 10,000), seeds resampled jointly across policies. Differences are in percentage points (pp).")
    L.append("")
    for res in all_res:
        k = res["kappa"]
        L.append(f"## κ = {k:g} (y* = {res['ystar']:.4f}; {res['n']} matched seeds: {res['seeds'][0]}–{res['seeds'][-1]})")
        L.append("")
        L.append("### Each policy (mean [95% CI])")
        L.append("")
        L.append("| Policy | $25k | $50k | $100k | anytime | median $ to 60% / 70% / 80% (share of seeds reaching it) |")
        L.append("|---|---|---|---|---|---|")
        for r in res["policies"]:
            cells = [f"{pc(r[f'{m}_mean'])} [{pc(r[f'{m}_lo'])}, {pc(r[f'{m}_hi'])}]" for m in METRICS]
            costs = " / ".join(f"{money(r[f'cost{t}_median'])} ({r[f'cost{t}_reached']:.0%})" for t in (60, 70, 80))
            L.append(f"| {LABEL[r['policy']]} | " + " | ".join(cells) + f" | {costs} |")
        L.append("")
        L.append("### The 2 × 2: {KG per $, EI per $} × {partial, full chain} (difference in pp [95% matched CI])")
        L.append("")
        L.append("| Contrast | $25k | $50k | $100k | anytime |")
        L.append("|---|---|---|---|---|")
        for r in res["contrasts"]:
            L.append(f"| {r['contrast']} | " + " | ".join(f"{pts(r[f'{m}_diff'])} {ci_pts(r[f'{m}_lo'], r[f'{m}_hi'])}" for m in METRICS) + " |")
        L.append("")
        L.append("### Speed-up: spend the baseline needs to reach its own $100k mean ÷ spend the policy needs (matched-seed bootstrap)")
        L.append("")
        L.append("| Policy | over tiered screening: est. [95% CI] (90% CI) | over standard BO: est. [95% CI] (90% CI) |")
        L.append("|---|---|---|")
        sp = {(r["policy"], r["over"]): r for r in res["speedup"]}
        for p in POLICIES:
            cells = []
            for base in ("tiered", "ei"):
                r = sp.get((p, base))
                if r is None:
                    cells.append("—")
                    continue
                e = "not reached" if r["est"] == 0 else f"{r['est']:.1f}×"
                cells.append(f"{e} [{r['lo95']:.1f}, {r['hi95']:.1f}] ({r['lo90']:.1f}, {r['hi90']:.1f})")
            L.append(f"| {LABEL[p]} | " + " | ".join(cells) + " |")
        L.append("")
        L.append("Target levels (baseline's own $100k mean): tiered " + f"{pc(sp[('pkgfn', 'tiered')]['target'])}%, standard BO {pc(sp[('pkgfn', 'ei')]['target'])}%. "
                 "0.0 means the policy's mean curve never reached the target within $100k.")
        L.append("")
        L.append("### Purchases per run (new spend only, mean over seeds)")
        L.append("")
        L.append("| Policy | CALPHAD | atomize | print | tensile | KG flat, EI fallback chose | GP fits failed | mean wall time |")
        L.append("|---|---|---|---|---|---|---|---|")
        for r in res["allocation"]:
            fb = "—" if math.isnan(r["fallback_share"]) else f"{r['fallback_share']:.1%}"
            L.append(f"| {LABEL[r['policy']]} | {r['C_mean']:.1f} | {r['A_mean']:.1f} | {r['L_mean']:.1f} | {r['T_mean']:.1f} | {fb} | {r['gp_fit_failures']} of {r['gp_fits']} | {r['wall_s_mean']:.0f} s |")
        L.append("")
        L.append("### Every pair (A − B, pp [95% matched CI]; wins of A / ties out of n)")
        L.append("")
        L.append("| A | B | $25k | $50k | $100k | anytime |")
        L.append("|---|---|---|---|---|---|")
        for r in res["pairwise"]:
            cells = []
            for m in METRICS:
                cells.append(f"{pts(r[f'{m}_diff'])} {ci_pts(r[f'{m}_lo'], r[f'{m}_hi'])} ({r[f'{m}_wins']}/{r[f'{m}_ties']})")
            L.append(f"| {SHORT[r['a']]} | {SHORT[r['b']]} | " + " | ".join(cells) + " |")
        L.append("")
    return "\n".join(L) + "\n"


def tex_key(*parts):
    return "-".join(str(p) for p in parts)


def numbers_tex(all_res):
    """\\stat{<key>} macros, e.g. \\stat{k1-pkgfn-v100-mean} -> 84."""
    defs = []

    def put(key, val):
        defs.append(f"\\expandafter\\def\\csname stat@{key}\\endcsname{{{val}}}")

    for res in all_res:
        k = {0.0: "k0", 0.5: "k05", 1.0: "k1"}[res["kappa"]]
        put(tex_key(k, "n"), res["n"])
        for r in res["policies"]:
            for m in METRICS:
                for s in ("mean", "lo", "hi"):
                    put(tex_key(k, r["policy"], m, s), pc(r[f"{m}_{s}"]))
            for t in (60, 70, 80):
                put(tex_key(k, r["policy"], f"cost{t}"), money(r[f"cost{t}_median"]).replace("$", "\\$"))
                put(tex_key(k, r["policy"], f"reach{t}"), f"{100 * r[f'cost{t}_reached']:.0f}")
        for r in res["pairwise"]:
            for m in METRICS:
                put(tex_key(k, r["a"], r["b"], m), f"{100 * r[f'{m}_diff']:+.1f}".replace("+", "$+$").replace("-", "$-$"))
                put(tex_key(k, r["a"], r["b"], m, "ci"), f"{100 * r[f'{m}_lo']:.1f} to {100 * r[f'{m}_hi']:.1f}".replace("-", "$-$"))
                put(tex_key(k, r["a"], r["b"], m, "wins"), r[f"{m}_wins"])
        for i, r in enumerate(res["contrasts"]):
            for m in METRICS:
                put(tex_key(k, "c", i, m), f"{100 * r[f'{m}_diff']:+.1f}".replace("+", "$+$").replace("-", "$-$"))
                put(tex_key(k, "c", i, m, "ci"), f"{100 * r[f'{m}_lo']:.1f} to {100 * r[f'{m}_hi']:.1f}".replace("-", "$-$"))
        for r in res["speedup"]:
            put(tex_key(k, "su", r["policy"], r["over"]), "n.r." if r["est"] == 0 else f"{r['est']:.1f}")
            put(tex_key(k, "su", r["policy"], r["over"], "ci95"), f"{r['lo95']:.1f}--{r['hi95']:.1f}")
            put(tex_key(k, "su", r["policy"], r["over"], "ci90"), f"{r['lo90']:.1f}--{r['hi90']:.1f}")
            put(tex_key(k, "su", r["over"], "target"), pc(r["target"]))
        for r in res["allocation"]:
            for g in "CALT":
                put(tex_key(k, r["policy"], "n" + g), f"{r[f'{g}_mean']:.1f}")
            if not math.isnan(r["fallback_share"]):
                put(tex_key(k, r["policy"], "fallback"), f"{100 * r['fallback_share']:.0f}")
            put(tex_key(k, r["policy"], "fitfail"), r["gp_fit_failures"])
            put(tex_key(k, r["policy"], "fits"), r["gp_fits"])
    head = ["% Generated by benchmarks/bofn-paper/paper_stats.py; do not edit by hand.",
            "% Use \\stat{<key>}, e.g. \\stat{k1-pkgfn-v100-mean}. Keys are listed in paper-stats/SUMMARY.md's tables.",
            "\\makeatletter",
            "\\providecommand{\\stat}[1]{\\@ifundefined{stat@#1}{\\textbf{??#1??}}{\\csname stat@#1\\endcsname}}"]
    return "\n".join(head + sorted(set(defs)) + ["\\makeatother", ""])


TEXNAME = {
    "pkgfn": "pKGFN", "kgfn": "KGFN", "eifn_reuse": "BOFN + powder reuse", "eifn": "BOFN",
    "ei": "Standard BO", "tiered": "Tiered screening", "tiered_naive": "Tiered, no reuse", "random": "Random",
}


def results_table_tex(all_res):
    """Table of every policy's best alloy demonstrated (% of optimum, mean [95% CI]) at each kappa."""
    L = ["% Generated by benchmarks/bofn-paper/paper_stats.py; do not edit by hand.",
         "\\begin{table}[t]", "\\centering", "\\small",
         "\\caption{\\textbf{Best alloy demonstrated, \\% of the optimum (mean and 95\\% bootstrap interval over seeds).} "
         "The anytime score is the mean over the whole \\$0--100k budget.}",
         "\\label{tab:results}",
         "\\begin{tabular}{@{}llllll@{}}", "\\toprule",
         "$\\kappa$ (seeds) & Policy & \\$25k & \\$50k & \\$100k & anytime \\\\", "\\midrule"]
    for res in all_res:
        for i, r in enumerate(res["policies"]):
            head = f"{res['kappa']:g} ({res['n']})" if i == 0 else ""
            cells = [f"{pc(r[f'{m}_mean'])} [{pc(r[f'{m}_lo'])}, {pc(r[f'{m}_hi'])}]" for m in METRICS]
            L.append(f"{head} & {TEXNAME[r['policy']]} & " + " & ".join(cells) + " \\\\")
        L.append("\\midrule" if res is not all_res[-1] else "\\bottomrule")
    L += ["\\end{tabular}", "\\end{table}", ""]
    return "\n".join(L)


def contrasts_table_tex(all_res):
    """The 2 x 2 contrasts at every kappa (pp, mean difference [95% matched CI])."""
    nice = {"partial - full, KG": "partial $-$ full, under KG (pKGFN $-$ KGFN)",
            "partial - full, EI": "partial $-$ full, under EI (BOFN+reuse $-$ BOFN)",
            "KG - EI, partial": "KG $-$ EI, partial (pKGFN $-$ BOFN+reuse)",
            "KG - EI, full chain": "KG $-$ EI, full chain (KGFN $-$ BOFN)",
            "interaction (partial gain under KG minus under EI)": "interaction (partial gain under KG $-$ under EI)"}
    f = lambda x: f"{100 * x:+.1f}".replace("-", "$-$").replace("+", "$+$")
    L = ["% Generated by benchmarks/bofn-paper/paper_stats.py; do not edit by hand.",
         "\\begin{table}[t]", "\\centering", "\\small",
         "\\caption{\\textbf{The $2\\times2$ contrasts.} Difference in the best alloy demonstrated, percentage points of the optimum, "
         "with 95\\% matched-seed bootstrap intervals.}",
         "\\label{tab:contrasts}",
         "\\begin{tabular}{@{}lllll@{}}", "\\toprule",
         "$\\kappa$ & Contrast & \\$25k & \\$100k & anytime \\\\", "\\midrule"]
    for res in all_res:
        for i, r in enumerate(res["contrasts"]):
            head = f"{res['kappa']:g}" if i == 0 else ""
            cells = [f"{f(r[f'{m}_diff'])} [{f(r[f'{m}_lo'])}, {f(r[f'{m}_hi'])}]" for m in ("v25", "v100", "auc")]
            L.append(f"{head} & {nice[r['contrast']]} & " + " & ".join(cells) + " \\\\")
        L.append("\\midrule" if res is not all_res[-1] else "\\bottomrule")
    L += ["\\end{tabular}", "\\end{table}", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="list missing runs")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    all_res = [r for r in (analyse(k, a.check) for k in KAPPAS) if r]
    for name in ("policies", "pairwise", "contrasts", "speedup", "allocation"):
        write_csv(out / f"{name}.csv", [row for r in all_res for row in r[name]])
    (out / "SUMMARY.md").write_text(summary_md(all_res))
    (out / "numbers.tex").write_text(numbers_tex(all_res))
    (out / "table-results.tex").write_text(results_table_tex(all_res))
    (out / "table-contrasts.tex").write_text(contrasts_table_tex(all_res))
    for r in all_res:
        print(f"kappa={r['kappa']:g}: {r['n']} matched seeds")
    print(f"wrote {out}/")


if __name__ == "__main__":
    main()
