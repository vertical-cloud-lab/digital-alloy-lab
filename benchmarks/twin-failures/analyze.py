"""Summary statistics and figures for the failed-vs-abandoned benchmark in the twin (DAL #274).

    python analyze.py            # -> results/summary.json, figures/*.png, and the tables printed as markdown

Per experiment (regime) and strategy, for each campaign: the best new alloy at the horizon (true utility; the
policies never see it), the share of seeds reaching T1 (the state of the art) and T2 (halfway from it to the best the
oracle found) with the Kaplan-Meier median day, the restricted mean days to each target (censored at the horizon), and
where the atomizer's runs went. Each strategy is compared with ``bad_value`` (round 3 as it is) seed by seed: the mean
paired difference, a bootstrap 95 % interval, a paired t-test and an exact sign-flip p-value.

**Endpoints, fixed on 2026-11-26 at 07:45 UTC, when only seed 0 had run:** the primary endpoint is the days to T1
(the state of the art) averaged over the two campaigns (restricted mean, censored at the horizon), the lab's "wall
time to discovery". Its family is each strategy against ``bad_value`` within a regime, with Holm's correction on the
paired t-test. Everything else (T2, the best new alloy, each campaign alone) is reported with unadjusted p-values as
exploratory. With 8 seeds the exact sign-flip test can't go below p = 2/256, which is why it isn't the primary test.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bench  # noqa: E402

# the targets, from the twin's out/twin2/oracle.json at the pinned commit (twin/bench2.py targets())
TARGETS = {"T1": {"flaime_al": 0.4232, "onr_cu": 0.5559}, "T2": {"flaime_al": 0.6393, "onr_cu": 0.6565}}
CAMPS = ("flaime_al", "onr_cu")
CNAME = {"flaime_al": "Aluminium (FLAIME)", "onr_cu": "Copper (ONR)"}
ORDER = ("bad_value", "drop", "abandon", "retry", "viability_x", "viability_node", "viability_node_nodiag", "oracle",
         "heuristic", "random", "gpbo")
BASELINE = "bad_value"
# exploratory contrasts between strategies (a - b), named in the README; unadjusted
CONTRASTS = [("viability_node", "viability_x", "node-level against Ax 1.3's design-level viability"),
             ("viability_node", "drop", "a failure model against none"),
             ("abandon", "drop", "ABANDONED against FAILED, no failure model"),
             ("retry", "abandon", "one rerun before giving up, against giving up at once"),
             ("oracle", "viability_node", "the true cause against the lab's diagnosis"),
             ("viability_node", "viability_node_nodiag", "the lab's diagnosis against none")]


def hit_day(curve, target):
    for d, usd, u in curve:
        if u >= target - 1e-12:
            return d, usd
    return None


def km_median(days, horizon):
    ev = sorted((t if t is not None else horizon + 1e-6, t is not None) for t in days)
    n, s = len(ev), 1.0
    for i, (t, hit) in enumerate(ev):
        if hit:
            s *= 1.0 - 1.0 / (n - i)
            if s <= 0.5:
                return t
    return None


def rmst(day, horizon):
    """Restricted mean time to target: the hit day, or the horizon if never reached."""
    return horizon if day is None else min(day, horizon)


def signflip_p(d):
    d = np.asarray(d, float)
    n = len(d)
    if n == 0 or np.allclose(d, 0):
        return 1.0
    obs = abs(d.mean())
    if n <= 16:
        cnt = 0
        for signs in itertools.product((1, -1), repeat=n):
            cnt += abs((d * np.array(signs)).mean()) >= obs - 1e-12
        return cnt / 2 ** n
    r = np.random.default_rng(0)
    sims = np.abs((d[None, :] * r.choice((1, -1), size=(20000, n))).mean(axis=1))
    return float((sims >= obs - 1e-12).mean())


def boot_ci(d, B=10000, seed=0):
    d = np.asarray(d, float)
    r = np.random.default_rng(seed)
    m = d[r.integers(0, len(d), size=(B, len(d)))].mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def holm(ps):
    order = np.argsort(ps)
    m = len(ps)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (m - rank) * ps[i]))
        adj[i] = run
    return adj


ATOM_DAYS = {"flaime_al": (0, 1, 2, 3), "onr_cu": (4, 5)}     # twin/facility.py ATOMIZER_SPLIT (day 0 is a Monday)


def _days_in(t0, days, dows, horizon):
    """Whole calendar days of the given weekdays inside [t0, t0 + days), within the horizon."""
    a, b = int(math.ceil(t0)), int(math.floor(min(t0 + days, horizon)))
    return sum(1 for d in range(a, b) if d % 7 in dows)


def per_run(r):
    horizon = r["cfg"]["days"]
    out = {}
    for k in CAMPS:
        c = r["campaigns"][k]
        row = dict(best=c["best_new"], n_new=c["n_new_alloys"], spent=c["spent"], ledger=c["ledger"],
                   fcounts=c.get("fcounts", {}))
        for t in ("T1", "T2"):
            h = hit_day(c["curve_new"], TARGETS[t][k])
            row[t] = h[0] if h else None
            row[t + "_usd"] = h[1] if h else None
            row[t + "_rmst"] = rmst(row[t], horizon)
        out[k] = row
    out["both"] = dict(T1_rmst=0.5 * (out["flaime_al"]["T1_rmst"] + out["onr_cu"]["T1_rmst"]),
                       T2_rmst=0.5 * (out["flaime_al"]["T2_rmst"] + out["onr_cu"]["T2_rmst"]),
                       best=0.5 * (out["flaime_al"]["best"] + out["onr_cu"]["best"]))
    out["down_days"] = r["fail"]["down_days"]
    out["n_damage"] = len(r["fail"]["damage"])
    for k in CAMPS:                                     # repairs each campaign's failed runs set off
        dm = [d for d in r["fail"]["damage"] if d["campaign"] == k]
        out[k]["repairs"] = len(dm)
        out[k]["repair_days"] = float(sum(d["days"] for d in dm))
        # the other campaign's atomizer days inside those repairs (the week is split: Al Mon-Thu, Cu Fri-Sat)
        other = ATOM_DAYS["onr_cu" if k == "flaime_al" else "flaime_al"]
        out[k]["other_days_lost"] = float(sum(_days_in(d["t_h"] / 24.0, d["days"], other, horizon) for d in dm))
    out["overlap_h"] = r["fail"].get("overlap_h", 0.0)
    out["atomizer_busy_h"] = r.get("atomizer_busy_h")
    out["seconds"] = r["seconds"]
    return out


def summarize(rows, horizon=365):
    """rows: per-run dicts of one strategy (any seeds)."""
    S = dict(n=len(rows), seeds=sorted(r["seed"] for r in rows))
    for k in CAMPS:
        R = [r[k] for r in rows]
        best = np.array([x["best"] for x in R])
        d = dict(best_mean=float(best.mean()), best_se=float(best.std(ddof=1) / math.sqrt(len(best))) if len(best) > 1
                 else 0.0, n_new=float(np.mean([x["n_new"] for x in R])), spent=float(np.mean([x["spent"] for x in R])))
        for t in ("T1", "T2"):
            days = [x[t] for x in R]
            d[t] = dict(hit=sum(1 for x in days if x is not None), km_median=km_median(days, horizon),
                        rmst=float(np.mean([x[t + "_rmst"] for x in R])))
        L = [x["ledger"] for x in R]
        d["ledger"] = {kk: float(np.mean([l[kk] for l in L])) for kk in L[0]}
        d["repairs"] = float(np.mean([x.get("repairs", 0) for x in R]))
        d["repair_days"] = float(np.mean([x.get("repair_days", 0.0) for x in R]))
        d["other_days_lost"] = float(np.mean([x.get("other_days_lost", 0.0) for x in R]))
        S[k] = d
    S["both"] = {m: float(np.mean([r["both"][m] for r in rows])) for m in ("T1_rmst", "T2_rmst", "best")}
    S["down_days"] = float(np.mean([r["down_days"] for r in rows]))
    S["n_damage"] = float(np.mean([r["n_damage"] for r in rows]))
    S["seconds"] = float(np.mean([r["seconds"] for r in rows]))
    S["overlap_h"] = float(np.mean([r.get("overlap_h", 0.0) for r in rows]))
    return S


def paired(rows_a, rows_b, metric, camp):
    """Seeds both have; differences a - b."""
    A = {r["seed"]: r for r in rows_a}
    B = {r["seed"]: r for r in rows_b}
    seeds = sorted(set(A) & set(B))
    d = np.array([A[s][camp][metric] - B[s][camp][metric] for s in seeds], float)
    if len(d) < 2:
        return None
    lo, hi = boot_ci(d)
    se = float(d.std(ddof=1) / math.sqrt(len(d)))
    from scipy.stats import t as tdist
    p_t = 1.0 if se == 0 else float(2 * tdist.sf(abs(d.mean()) / se, len(d) - 1))
    return dict(n=len(d), mean=float(d.mean()), se=se, lo=lo, hi=hi, p_t=p_t,
                p=signflip_p(d), wins=int((d > 1e-9).sum()), losses=int((d < -1e-9).sum()))


def load_all():
    data = {}
    for name in bench.EXPERIMENTS:
        for r in bench.load(name):
            c = r["cfg"]
            if c["days"] < 365:
                continue
            row = per_run(r)
            row["seed"] = c["seed"]
            data.setdefault(c["regime"], {}).setdefault(c["policy"], {})[c["seed"]] = row   # one row per seed
    # keep only seeds every failure-handling strategy of a regime has finished, so each summary is on the same
    # seeds (a run cut short at the job's limit leaves a partial seed)
    out = {}
    for reg, P in data.items():
        fm = [p for p in P if p not in ("heuristic", "random", "gpbo")]
        common = set.intersection(*[set(P[p]) for p in fm]) if fm else set()
        out[reg] = {p: [r for sd, r in sorted(S.items()) if p not in fm or sd in common] for p, S in P.items()}
    return out


def analyse():
    data = load_all()
    out = dict(targets=TARGETS, regimes={})
    for reg, P in data.items():
        E = dict(strategies={p: summarize(rows) for p, rows in P.items()}, paired={})
        prim = []
        if BASELINE in P:
            for p, rows in P.items():
                if p == BASELINE or p in ("heuristic", "random", "gpbo"):
                    continue
                for camp, metrics in (("both", ("T1_rmst", "T2_rmst", "best")),
                                      ("flaime_al", ("best", "T1_rmst", "T2_rmst")),
                                      ("onr_cu", ("best", "T1_rmst", "T2_rmst"))):
                    for metric in metrics:
                        res = paired(rows, P[BASELINE], metric, camp)
                        if res:
                            E["paired"].setdefault(p, {}).setdefault(camp, {})[metric] = res
                            if camp == "both" and metric == "T1_rmst":
                                prim.append((p, res["p_t"]))
        E["contrasts"] = []
        for a_, b_, why in CONTRASTS:
            if a_ in P and b_ in P:
                row = dict(a=a_, b=b_, why=why)
                for camp, metric in (("both", "T1_rmst"), ("both", "T2_rmst"), ("flaime_al", "best"), ("onr_cu", "best")):
                    row[f"{camp}:{metric}"] = paired(P[a_], P[b_], metric, camp)
                E["contrasts"].append(row)
        if prim:
            adj = holm(np.array([x[1] for x in prim]))
            for (p, _), a in zip(prim, adj):
                E["paired"][p]["both"]["T1_rmst"]["p_holm"] = float(a)
            E["n_primary"] = len(prim)
        out["regimes"][reg] = E
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "summary.json").write_text(json.dumps(out, indent=1, default=float))
    return out, data


def fmt_table(out):
    lines = []
    for reg, E in out["regimes"].items():
        lines.append(f"\n#### Regime `{reg}`\n")
        lines.append("| Strategy | n | Al best new | Al T1 hit, KM median day | Al T2 hit | Cu best new | Cu T1 hit, "
                     "KM median day | Cu T2 hit | Al runs failed (inputs / transient) | Cu runs failed | atomizer down, d | "
                     "repairs set off by Al / Cu | Cu atomizer days lost to Al's repairs |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for p in ORDER:
            if p not in E["strategies"]:
                continue
            s = E["strategies"][p]
            a, c = s["flaime_al"], s["onr_cu"]
            la, lc = a["ledger"], c["ledger"]
            md = lambda x: "-" if x is None else f"{x:.0f}"
            lines.append(
                f"| `{p}` | {s['n']} | {a['best_mean']:.3f} ± {a['best_se']:.3f} | {a['T1']['hit']}/{s['n']}, "
                f"{md(a['T1']['km_median'])} | {a['T2']['hit']}/{s['n']} | {c['best_mean']:.3f} ± {c['best_se']:.3f} | "
                f"{c['T1']['hit']}/{s['n']}, {md(c['T1']['km_median'])} | {c['T2']['hit']}/{s['n']} | "
                f"{la['failed']:.0f} of {la['runs']:.0f} ({la['failed_intrinsic']:.0f} / {la['failed_transient']:.0f}) | "
                f"{lc['failed']:.0f} of {lc['runs']:.0f} | {s['down_days']:.0f} | {a['repairs']:.1f} / {c['repairs']:.1f} | "
                f"{a['other_days_lost']:.0f} |")
        lines.append("\nWhat each strategy spent and made in a year (means over seeds):\n")
        lines.append("| Strategy | Al spent | Al new alloys demonstrated | Al designs atomized | Al designs given up after "
                     "transient failures only | Al repeat failures from the inputs | Cu spent | Cu new alloys |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for p in ORDER:
            if p not in E["strategies"]:
                continue
            a, c = E["strategies"][p]["flaime_al"], E["strategies"][p]["onr_cu"]
            lines.append(f"| `{p}` | ${a['spent'] / 1000:.0f}k | {a['n_new']:.1f} | {a['ledger']['designs']:.0f} | "
                         f"{a['ledger']['given_up_transient']:.1f} | {a['ledger']['repeat_intrinsic']:.1f} | "
                         f"${c['spent'] / 1000:.0f}k | {c['n_new']:.1f} |")
        if E.get("paired"):
            lines.append(f"\nPaired against `{BASELINE}`, seed by seed: mean difference (95 % bootstrap interval) and p. "
                         f"Days are restricted means to the target, censored at day 365, so negative is sooner. The "
                         f"primary endpoint (days to T1, both campaigns) carries Holm's correction over its "
                         f"{E.get('n_primary')} comparisons; the other columns are exploratory, with unadjusted paired "
                         f"t-test p.\n")
            lines.append("| Strategy | **Days to T1, both (primary)** | Days to T2, both | Al best new | Cu best new | "
                         "Al days to T1 | Cu days to T1 | seeds better / worse on the primary |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for p in ORDER:
                if p not in E["paired"]:
                    continue
                Q = E["paired"][p]
                cells = []
                for camp, metric in (("both", "T1_rmst"), ("both", "T2_rmst"), ("flaime_al", "best"),
                                     ("onr_cu", "best"), ("flaime_al", "T1_rmst"), ("onr_cu", "T1_rmst")):
                    x = Q.get(camp, {}).get(metric)
                    if not x:
                        cells.append("-")
                        continue
                    if metric == "best":
                        txt = f"{x['mean']:+.3f} ({x['lo']:+.3f} to {x['hi']:+.3f}), p {x['p_t']:.2f}"
                    else:
                        txt = f"{x['mean']:+.0f} ({x['lo']:+.0f} to {x['hi']:+.0f}), p {x['p_t']:.2f}"
                    if camp == "both" and metric == "T1_rmst":
                        txt += f", Holm {x['p_holm']:.2f}"
                    cells.append(txt)
                x = Q["both"]["T1_rmst"]
                cells.append(f"{x['losses']} / {x['wins']}")     # fewer days is better
                lines.append(f"| `{p}` | " + " | ".join(cells) + " |")
        if E.get("contrasts"):
            lines.append("\nExploratory contrasts between strategies (a minus b, paired by seed, unadjusted t-test p):\n")
            lines.append("| a − b | what it asks | Days to T1, both | Days to T2, both | Al best new | Cu best new |")
            lines.append("|---|---|---|---|---|---|")
            for row in E["contrasts"]:
                cells = []
                for key in ("both:T1_rmst", "both:T2_rmst", "flaime_al:best", "onr_cu:best"):
                    x = row.get(key)
                    if not x:
                        cells.append("-")
                    elif key.endswith("best"):
                        cells.append(f"{x['mean']:+.3f} ({x['lo']:+.3f} to {x['hi']:+.3f}), p {x['p_t']:.2f}")
                    else:
                        cells.append(f"{x['mean']:+.0f} ({x['lo']:+.0f} to {x['hi']:+.0f}), p {x['p_t']:.2f}")
                lines.append(f"| `{row['a']}` − `{row['b']}` | {row['why']} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    out, data = analyse()
    print(fmt_table(out))
    if "--figs" in sys.argv:
        import figures
        figures.main(out, data)
