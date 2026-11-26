"""Tables and statistics for the clocked benchmark: days and dollars to T1/T2, claim values on the clock, paired
differences, and the chance of reaching a tenth of the conventional baselines.

    python analyze.py            # writes results/summary.md and results/summary.json
"""
from __future__ import annotations

import glob
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

HERE = Path(__file__).parent
RES = HERE / "results"
LABEL = {
    ("conv_lots", "conv"): "Conventional, outside powder lots",
    ("conv_atomizer", "conv"): "Conventional, own atomizer (DAL #256 schedule)",
    ("vertical", "tiered"): "Automated lab, tiered screening",
    ("vertical", "gpbo"): "Automated lab, GP-BO",
    ("vertical", "bofn"): "Automated lab, BOFN",
    ("vertical", "pkgfn"): "Automated lab, pKGFN (fixed)",
    ("vertical", "random"): "Automated lab, random",
    ("nearterm", "tiered"): "Near-term lab, tiered screening",
    ("nearterm", "bofn"): "Near-term lab, BOFN",
    ("vertical_ih", "tiered"): "In-house printer only, tiered screening",
    ("vertical_ih", "bofn"): "In-house printer only, BOFN",
}
ORDER = list(LABEL)
CHECK_DAYS = (30, 45, 60, 90, 180, 365, 730)


def load(exp):
    G = defaultdict(dict)
    for f in sorted(glob.glob(str(RES / exp / "*.json"))):
        r = json.load(open(f))
        G[(r["kappa"], r["fac"], r["pol"], r.get("variant"))][r["seed"]] = r
    return G


def t_hit(r, T):
    h = r["hit"].get(T)
    return (h[0], h[1]) if h else (math.inf, math.inf)


def claim_at(r, day):
    """True value of the campaign's claim at `day`, as a fraction of the optimum (0 before the first claim)."""
    v = 0.0
    for t, _, val in r["score_hist"]:
        if t <= day + 1e-9:
            v = val
    if day > r["t_end"] and not r["hit"].get("T2"):  # the campaign ended (money or horizon): the claim stands
        pass
    return v / r["opt"]


def med(x):
    x = np.sort(np.asarray(x, float))
    m = np.median(x)
    return m


def fmt_days(x, H):
    if not np.isfinite(x):
        return f">{H:.0f}"
    return f"{x:.0f}"


def mean_se(x):
    x = np.asarray(x, float)
    if len(x) < 2:
        return float(np.mean(x)), float("nan")
    return float(np.mean(x)), float(np.std(x, ddof=1) / math.sqrt(len(x)))


def tenth(days_p, days_c_med, rng, days_c_all=None, n_boot=2000):
    """Fraction of P's seeds at or under a tenth of C's median, with a 90 % bootstrap interval over both sets."""
    p = np.asarray(days_p, float)
    est = float(np.mean(p <= days_c_med / 10))
    if days_c_all is None:
        return est, (float("nan"), float("nan"))
    c = np.asarray(days_c_all, float)
    bs = []
    for _ in range(n_boot):
        pb = p[rng.integers(0, len(p), len(p))]
        cb = c[rng.integers(0, len(c), len(c))]
        bs.append(np.mean(pb <= np.median(cb) / 10))
    return est, (float(np.percentile(bs, 5)), float(np.percentile(bs, 95)))


def paired(a, b):
    """Paired difference a - b over matched seeds (censored values at the horizon), Wilcoxon two-sided p."""
    seeds = sorted(set(a) & set(b))
    x = np.array([a[s] for s in seeds], float)
    y = np.array([b[s] for s in seeds], float)
    d = x - y
    if len(d) == 0:
        return None
    nz = d[np.abs(d) > 1e-9]
    p = float(wilcoxon(x, y).pvalue) if len(nz) >= 1 else 1.0
    return dict(n=len(d), mean=float(d.mean()), se=float(d.std(ddof=1) / math.sqrt(len(d))) if len(d) > 1 else float("nan"),
                a_better=int((d < -1e-9).sum()), b_better=int((d > 1e-9).sum()), ties=int((np.abs(d) <= 1e-9).sum()), p=p)


def summarize_e1(G, lines, S, exp_name="E1"):
    rng = np.random.default_rng(0)
    for kappa in sorted({k[0] for k in G}, reverse=True):
        keys = [k for k in ORDER if (kappa, k[0], k[1], None) in G]
        lines += [f"\n### {exp_name}, `kappa = {kappa:g}`\n",
                  "| Lab and policy | n | T1 reached | days to T1, median (mean ± SE, censored at the horizon) | $k to T1, median | "
                  "T2 reached | days to T2, median (mean ± SE) | $k to T2, median | claim at day 45 / 90, % of optimum |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for fac, pol in keys:
            R = G[(kappa, fac, pol, None)]
            H = next(iter(R.values()))["horizon"]
            row = [LABEL[(fac, pol)], str(len(R))]
            S.setdefault(f"k{kappa:g}", {})[f"{fac}/{pol}"] = ent = {}
            for T in ("T1", "T2"):
                d = [min(t_hit(r, T)[0], H) for r in R.values()]
                dd = [t_hit(r, T)[0] for r in R.values()]
                usd = [t_hit(r, T)[1] for r in R.values() if np.isfinite(t_hit(r, T)[1])]
                reached = sum(np.isfinite(dd))
                m, se = mean_se(d)
                row += [f"{reached}/{len(R)}", f"{fmt_days(med(dd), H)} ({m:.0f} ± {se:.0f})",
                        f"{np.median(usd) / 1e3:.0f}" if usd else "–"]
                ent[T] = dict(days={s: t_hit(r, T)[0] for s, r in R.items()}, usd={s: t_hit(r, T)[1] for s, r in R.items()},
                              reached=reached, median_days=med(dd), H=H)
            c45 = mean_se([100 * claim_at(r, 45) for r in R.values()])
            c90 = mean_se([100 * claim_at(r, 90) for r in R.values()])
            row.append(f"{c45[0]:.0f} ± {c45[1]:.0f} / {c90[0]:.0f} ± {c90[1]:.0f}")
            ent["claim"] = {d: [claim_at(r, d) for r in R.values()] for d in CHECK_DAYS}
            ent["spent_end"] = [r["spent"] for r in R.values()]
            lines.append("| " + " | ".join(row) + " |")
        # a tenth of the conventional baselines
        lines += ["", "Chance of reaching a tenth of a conventional baseline (fraction of seeds at or under a tenth of the "
                  "baseline's median; 90 % bootstrap interval over both sets of seeds; a censored baseline counts at its "
                  "4-year horizon, so these are lower bounds on the true chance when the baseline never got there):", "",
                  "| Policy | vs | T1 days | T1 dollars | T2 days | T2 dollars |", "|---|---|---|---|---|---|"]
        for cfac in ("conv_lots", "conv_atomizer"):
            if (kappa, cfac, "conv", None) not in G:
                continue
            C = G[(kappa, cfac, "conv", None)]
            HC = next(iter(C.values()))["horizon"]
            for fac, pol in keys:
                if fac.startswith("conv"):
                    continue
                P = G[(kappa, fac, pol, None)]
                row = [LABEL[(fac, pol)], LABEL[(cfac, "conv")]]
                for T in ("T1", "T2"):
                    for j in (0, 1):
                        cv = [min(t_hit(r, T)[j], HC if j == 0 else r["budget"]) for r in C.values()]
                        cvr = [t_hit(r, T)[j] for r in C.values()]
                        pv = [t_hit(r, T)[j] for r in P.values()]
                        cm = np.median(cv)
                        est, (lo, hi) = tenth(pv, cm, rng, cv)
                        cens = sum(not np.isfinite(x) for x in cvr)
                        row.append(f"{est:.0%} ({lo:.0%}–{hi:.0%})" + ("*" if cens > len(cvr) / 2 else ""))
                lines.append("| " + " | ".join(row) + " |")
        lines.append("\n\\* the baseline's median is censored (it reached the target on half its seeds or fewer), "
                     "so the baseline's time or money is a lower bound.")
        # paired differences against tiered screening on the same lab and between network policies
        pairs = [(("vertical", "bofn"), ("vertical", "tiered")), (("vertical", "pkgfn"), ("vertical", "tiered")),
                 (("vertical", "gpbo"), ("vertical", "tiered")), (("vertical", "bofn"), ("vertical", "gpbo")),
                 (("vertical", "pkgfn"), ("vertical", "bofn")), (("vertical", "random"), ("vertical", "tiered")),
                 (("vertical", "tiered"), ("conv_lots", "conv")), (("vertical", "tiered"), ("conv_atomizer", "conv"))]
        lines += ["", "Paired differences on matched seeds (A − B in days to the target, censored at the horizon; "
                  "two-sided Wilcoxon signed-rank):", "",
                  "| A | B | target | mean A − B ± SE (days) | A sooner / B sooner / tie | p |", "|---|---|---|---|---|---|"]
        for A, B in pairs:
            if (kappa, *A, None) not in G or (kappa, *B, None) not in G:
                continue
            for T in ("T1", "T2"):
                RA, RB = G[(kappa, *A, None)], G[(kappa, *B, None)]
                HA = max(next(iter(RA.values()))["horizon"], next(iter(RB.values()))["horizon"])
                a = {s: min(t_hit(r, T)[0], HA) for s, r in RA.items()}
                b = {s: min(t_hit(r, T)[0], HA) for s, r in RB.items()}
                pr = paired(a, b)
                if pr:
                    lines.append(f"| {LABEL[A]} | {LABEL[B]} | {T} | {pr['mean']:+.0f} ± {pr['se']:.0f} | "
                                 f"{pr['a_better']} / {pr['b_better']} / {pr['ties']} | {pr['p']:.3g} |")
                    S[f"k{kappa:g}"].setdefault("paired", {})[f"{A[0]}/{A[1]} - {B[0]}/{B[1]} {T}"] = pr
    return lines


def summarize_counts(G, lines, kappa):
    keys = [k for k in ORDER if (kappa, k[0], k[1], None) in G]
    lines += ["", "What each campaign bought, to T2 or to its end (mean per campaign; bars count single bars):", "",
              "| Lab and policy | powders | builds | bars | immersions | immersions stopped early | money spent, $k | "
              "pKGFN decisions with every KG flat |", "|---|---|---|---|---|---|---|---|"]
    for fac, pol in keys:
        R = G[(kappa, fac, pol, None)]
        c = lambda k: np.mean([r["counts"].get(k, 0) for r in R.values()])
        flat = ""
        if pol == "pkgfn":
            f = sum(r.get("kg_flat", 0) for r in R.values())
            u = sum(r.get("kg_used", 0) for r in R.values())
            flat = f"{f}/{f + u} ({f / max(f + u, 1):.0%})"
        lines.append(f"| {LABEL[(fac, pol)]} | {c('powder'):.1f} | {c('print'):.1f} | {c('bars'):.1f} | {c('imm'):.1f} | "
                     f"{c('stop'):.1f} | {np.mean([r['spent'] for r in R.values()]) / 1e3:.0f} | {flat} |")


def summarize_e2b(lines, S):
    G = load("e2b")
    if not G:
        return lines
    lines += ["\n### E2b, moving to production powder (`kappa = 1`, BOFN; confirmation = a claim on a gas-atomized lot "
              "printed on the partner's machine)\n",
              "| Ordering rule | n | days to T1 / T2 (median) | days to confirmed T1 / T2 (median; reached) | $k to confirmed T2, median |",
              "|---|---|---|---|---|"]
    D = {}
    for pol in ("bofn_confirm", "bofn_confirm_early"):
        R = G.get((1.0, "vertical", pol, None), {})
        if not R:
            continue
        H = 365.0
        row = [{"bofn_confirm": "order after the claim", "bofn_confirm_early": "order early (3 bars + a passing day-7 reading)"}[pol],
               str(len(R))]
        row.append(" / ".join(fmt_days(med([t_hit(r, T)[0] for r in R.values()]), H) for T in ("T1", "T2")))
        cc = []
        for T in ("T1c", "T2c"):
            dd = [t_hit(r, T)[0] for r in R.values()]
            cc.append(f"{fmt_days(med(dd), H)} ({sum(np.isfinite(dd))}/{len(R)})")
            D[(pol, T)] = {s: min(t_hit(r, T)[0], H) for s, r in R.items()}
        row.append(" / ".join(cc))
        uu = [t_hit(r, "T2c")[1] for r in R.values() if np.isfinite(t_hit(r, "T2c")[1])]
        row.append(f"{np.median(uu) / 1e3:.0f}" if uu else "–")
        lines.append("| " + " | ".join(row) + " |")
    for T in ("T1c", "T2c"):
        if ("bofn_confirm_early", T) in D and ("bofn_confirm", T) in D:
            pr = paired(D[("bofn_confirm_early", T)], D[("bofn_confirm", T)])
            lines.append(f"\nEarly minus after, days to {T} (censored at 365): {pr['mean']:+.0f} ± {pr['se']:.0f}; early sooner on "
                         f"{pr['a_better']}, later on {pr['b_better']}, tied on {pr['ties']} (Wilcoxon p = {pr['p']:.3g}).")
            S.setdefault("e2b", {})[T] = pr
    return lines


def summarize_e3a(lines, S):
    G = load("e3a")
    if not G:
        return lines
    lines += ["\n### E3a, another lab's data (`kappa = 1`, BOFN on the automated lab)\n",
              "| Model | n | T1 reached | days to T1, median (mean ± SE) | T2 reached | days to T2, median (mean ± SE) | "
              "claim at day 45, % of optimum |", "|---|---|---|---|---|---|---|"]
    days = {}
    for v in ("separate", "naive", "site"):
        R = G.get((1.0, "vertical", "bofn", v), {})
        if not R:
            continue
        H = 365.0
        row = [v, str(len(R))]
        for T in ("T1", "T2"):
            dd = [t_hit(r, T)[0] for r in R.values()]
            m, se = mean_se([min(x, H) for x in dd])
            row += [f"{sum(np.isfinite(dd))}/{len(R)}", f"{fmt_days(med(dd), H)} ({m:.0f} ± {se:.0f})"]
            days[(v, T)] = {s: min(t_hit(r, T)[0], H) for s, r in R.items()}
        c = mean_se([100 * claim_at(r, 45) for r in R.values()])
        row.append(f"{c[0]:.0f} ± {c[1]:.0f}")
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "| A | B | target | mean A − B ± SE (days) | A sooner / B sooner / tie | p |", "|---|---|---|---|---|---|"]
    for A, B in (("site", "separate"), ("naive", "separate"), ("site", "naive")):
        for T in ("T1", "T2"):
            if (A, T) in days and (B, T) in days:
                pr = paired(days[(A, T)], days[(B, T)])
                lines.append(f"| {A} | {B} | {T} | {pr['mean']:+.0f} ± {pr['se']:.0f} | {pr['a_better']} / {pr['b_better']} / "
                             f"{pr['ties']} | {pr['p']:.3g} |")
                S.setdefault("e3a", {})[f"{A}-{B} {T}"] = pr
    return lines


def summarize_e3b(lines, S):
    files = sorted(glob.glob(str(RES / "e3b" / "chain_s*.json")))
    if not files:
        return lines
    rows = [dict(seed=json.load(open(f))["seed"], **r) for f in files for r in json.load(open(f))["rows"]]
    lines += ["\n### E3b, a time machine (`kappa = 1`, BOFN; campaign 0 is shared, campaigns 1 and 2 change the goal)\n",
              "| History | campaign | n | T1 reached | days to T1, median (mean ± SE) | $k to T1, median | T2 reached | "
              "days to T2, median (mean ± SE) | $k to T2, median |", "|---|---|---|---|---|---|---|---|---|"]
    D = {}
    for hist, camp in (("all", 0), ("none", 1), ("documented", 1), ("poor", 1), ("none", 2), ("documented", 2), ("poor", 2)):
        R = [r for r in rows if r["history"] == hist and r["campaign"] == camp]
        if not R:
            continue
        row = [hist if camp else "(any)", str(camp), str(len(R))]
        for T in ("T1", "T2"):
            dd = [t_hit(r, T)[0] for r in R]
            uu = [t_hit(r, T)[1] for r in R if np.isfinite(t_hit(r, T)[1])]
            m, se = mean_se([min(x, 365.0) for x in dd])
            row += [f"{sum(np.isfinite(dd))}/{len(R)}", f"{fmt_days(med(dd), 365)} ({m:.0f} ± {se:.0f})",
                    f"{np.median(uu) / 1e3:.0f}" if uu else "–"]
            D[(hist, camp, T)] = {r["seed"]: min(t_hit(r, T)[0], 365.0) for r in R}
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "| A | B | campaign | target | mean A − B ± SE (days) | A sooner / B sooner / tie | p |",
              "|---|---|---|---|---|---|---|"]
    for camp in (1, 2):
        for A, B in (("documented", "none"), ("poor", "none"), ("documented", "poor")):
            for T in ("T1", "T2"):
                if (A, camp, T) in D and (B, camp, T) in D:
                    pr = paired(D[(A, camp, T)], D[(B, camp, T)])
                    lines.append(f"| {A} | {B} | {camp} | {T} | {pr['mean']:+.0f} ± {pr['se']:.0f} | {pr['a_better']} / "
                                 f"{pr['b_better']} / {pr['ties']} | {pr['p']:.3g} |")
                    S.setdefault("e3b", {})[f"{A}-{B} c{camp} {T}"] = pr
    return lines


def summarize_e5(lines, S):
    files = sorted(glob.glob(str(RES / "e5" / "*.json")))
    if not files:
        return lines
    R = defaultdict(dict)
    for f in files:
        r = json.load(open(f))
        R[r["variant"]][r["seed"]] = r
    lines += ["\n### E5, one search across alloy families (stretch; `CrossTruth`, BOFN)\n",
              "| Campaign | n | claim at day 60 / 120 / 180, % of the cross-family optimum | T1 reached | T2 reached | spent, $k |",
              "|---|---|---|---|---|---|"]
    best_fam = {}
    for v in ("global", "7xxx", "AlSi", "AlMgSc"):
        if v not in R:
            continue
        cs = [mean_se([100 * claim_at(r, d) for r in R[v].values()]) for d in (60, 120, 180)]
        lines.append(f"| {v} | {len(R[v])} | " + " / ".join(f"{m:.0f} ± {se:.0f}" for m, se in cs) +
                     f" | {sum(1 for r in R[v].values() if 'T1' in r['hit'])}/{len(R[v])} | "
                     f"{sum(1 for r in R[v].values() if 'T2' in r['hit'])}/{len(R[v])} | "
                     f"{np.mean([r['spent'] for r in R[v].values()]) / 1e3:.0f} |")
    seeds = sorted(set(R.get("global", {})) & set.intersection(*[set(R[f]) for f in ("7xxx", "AlSi", "AlMgSc") if f in R]))
    if seeds:
        for d in (60, 120, 180):
            g = {s: claim_at(R["global"][s], d) for s in seeds}
            b = {s: max(claim_at(R[f][s], d) for f in ("7xxx", "AlSi", "AlMgSc") if f in R) for s in seeds}
            pr = paired(g, b)
            best_fam[d] = pr
            lines.append(f"\nDay {d}: global minus the best of the three family campaigns, paired: "
                         f"{100 * pr['mean']:+.1f} ± {100 * pr['se']:.1f} points; global ahead on {pr['b_better']}, "
                         f"behind on {pr['a_better']}, tied on {pr['ties']} (Wilcoxon p = {pr['p']:.3g}).")
            # `paired` counts a - b < 0 as "a_better" (fewer days); for claim values higher is better, hence the swap
        S["e5"] = {str(k): v for k, v in best_fam.items()}
    return lines


def main():
    lines, S = ["# bofn-clocked: results (generated by analyze.py)"], {}
    G = load("e1")
    if G:
        summarize_e1(G, lines, S)
        for kappa in (1.0, 0.0):
            summarize_counts(G, lines, kappa)
    G2 = load("e2")
    if G2:
        for k, v in load("e1").items():
            if k[1] == "vertical" and k[2] in ("tiered", "bofn") and k[0] == 1.0:
                G2[k] = v
        lines.append("\n## E2, routes")
        summarize_e1(G2, lines, S.setdefault("e2", {}), "E2")
    summarize_e2b(lines, S)
    summarize_e3a(lines, S)
    summarize_e3b(lines, S)
    summarize_e5(lines, S)
    (RES / "summary.md").write_text("\n".join(lines) + "\n")
    json.dump(S, open(RES / "summary.json", "w"), indent=1,
              default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
