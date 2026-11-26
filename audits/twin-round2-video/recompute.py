#!/usr/bin/env python3
"""Recompute the numbers of the twin round-2 video from its stored per-seed runs.

    git clone https://github.com/vertical-cloud-lab/byu-vcl /tmp/byu-vcl && git -C /tmp/byu-vcl checkout 357d149
    python audits/twin-round2-video/recompute.py /tmp/byu-vcl/vertical-lab > audits/twin-round2-video/recomputed.md

Reads only ``out/twin2/runs/*.jsonl`` and ``out/twin2/oracle.json`` (numpy only; none of the twin's code is imported),
so it is an independent check of ``twin/accel.py`` and of ``out/twin2/econ/econ_summary.json``. ``--json FILE`` also
writes every number as JSON.

Definitions (the twin's own, re-implemented here):
* a seed "reaches the target" at the first point of ``curve_new`` (new alloys only: [day, cash spent, best true
  utility]) whose utility is at or above the target; otherwise it is censored at the run's horizon (``cfg.days``);
* the acceleration factor is median(reference) / median(new). ``twin`` medians: the ordinary median when every seed
  reached the target, else the Kaplan-Meier median. ``km`` medians: Kaplan-Meier always (the 6th of 12, where the
  ordinary median averages the 6th and 7th);
* intervals: percentile bootstrap over seeds, resampled within each arm (20,000 resamples here, 2,000 in the twin).

Added here: a two-sided permutation test of each comparison (Gehan's generalised rank statistic, which handles
censored seeds; exact over all 2,704,156 relabellings for 12 seeds against 12, 100,000 random relabellings for larger
arms), the share of seed pairs in which each arm was faster, and Holm's correction over the family of claims the
video makes.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np

CAMPS = ("flaime_al", "onr_cu")
NAME = {"flaime_al": "FLAIME (Al)", "onr_cu": "ONR (Cu)"}
B = 20_000
NPERM = 100_000


# ------------------------------------------------------------------------------------------------ loading
def load(root: Path, exp: str) -> list:
    return [json.loads(l) for l in (root / "out" / "twin2" / "runs" / f"{exp}.jsonl").read_text().splitlines() if l]


def arm(rows: list, **want) -> list:
    out = [r for r in rows if all(r["cfg"].get(k) == v for k, v in want.items())]
    return sorted(out, key=lambda r: r["cfg"]["seed"])


def hits(runs: list, camp: str, target: float, col: int = 0):
    """(x at the first point at or above target, reached?) per seed; col 0 = days, 1 = cash. Censored at the horizon
    (days) or at the run's final spend (cash)."""
    xs, ok = [], []
    for r in runs:
        c = r["campaigns"][camp]
        cur = c.get("curve_new") if c.get("curve_new") is not None else c.get("curve", [])
        h = next((p for p in cur if p[2] >= target - 1e-12), None)
        if h is not None:
            xs.append(float(h[col])); ok.append(True)
        else:
            xs.append(float(r["cfg"]["days"]) if col == 0 else float(c.get("spent", 0.0))); ok.append(False)
    return np.array(xs), np.array(ok, bool)


def final_best(runs: list, camp: str) -> np.ndarray:
    return np.array([float(r["campaigns"][camp].get("best_new", r["campaigns"][camp].get("best", 0.0))) for r in runs])


# ------------------------------------------------------------------------------------------------ statistics
def km_median(t, e) -> float:
    t, e = np.asarray(t, float), np.asarray(e, bool)
    order = np.lexsort((~e, t))
    t, e = t[order], e[order]
    s, at_risk, i, n = 1.0, len(t), 0, len(t)
    while i < n:
        tt, d, c = t[i], 0, 0
        while i < n and t[i] == tt:
            d += int(e[i]); c += int(not e[i]); i += 1
        if d:
            s *= 1.0 - d / at_risk
            if s <= 0.5 + 1e-12:
                return float(tt)
        at_risk -= d + c
    return math.inf


def med(t, e, mode="twin") -> float:
    if mode == "twin" and np.all(e):
        return float(np.median(t))
    return km_median(t, e)


def ratio(a, b) -> float:
    if not np.isfinite(a) and not np.isfinite(b):
        return math.nan
    if not np.isfinite(b):
        return 0.0
    if not np.isfinite(a):
        return math.inf
    return a / b if b > 0 else math.inf


def boot_ratio(tr, er, tn, en, mode="twin", seed=1):
    rng = np.random.default_rng(seed)
    out = np.empty(B)
    for k in range(B):
        i = rng.integers(len(tr), size=len(tr)); j = rng.integers(len(tn), size=len(tn))
        out[k] = ratio(med(tr[i], er[i], mode), med(tn[j], en[j], mode))
    out = out[~np.isnan(out)]
    lo, hi = np.quantile(out, [0.025, 0.975], method="closest_observation")
    return float(lo), float(hi), float(np.mean(out <= 1.0))


def gehan_matrix(tr, er, tn, en) -> np.ndarray:
    """+1 where the new arm's seed is known to be faster than the reference's, -1 where known slower, 0 where the
    order is not determined (both censored, or one censored before the other's time)."""
    t = np.concatenate([tr, tn]); e = np.concatenate([er, en])
    less = (t[:, None] < t[None, :]) & e[:, None]          # i is known to be before j: i reached it, at an earlier x
    return less.astype(int) - less.T.astype(int)           # U[i, j] = +1 if i before j, -1 if j before i


_Z = {}


def assignments(n: int, k: int, rng) -> tuple:
    """(Z, exact): every way to label k of n seeds as the new arm (exact, when there are at most 3 million), else
    NPERM random labellings. Z is a 0/1 matrix, one labelling a row."""
    if math.comb(n, k) <= 3_000_000:
        if (n, k) not in _Z:
            C = math.comb(n, k)
            idx = np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(n), k)), dtype=np.int64,
                              count=C * k).reshape(C, k)
            Z = np.zeros((C, n), dtype=np.int8)
            np.put_along_axis(Z, idx, 1, axis=1)
            _Z[(n, k)] = Z
        return _Z[(n, k)], True
    Z = np.zeros((NPERM, n), dtype=np.int8)
    np.put_along_axis(Z, np.argsort(rng.random((NPERM, n)), axis=1)[:, :k], 1, axis=1)
    return Z, False


def gehan_test(tr, er, tn, en, seed=2):
    U = gehan_matrix(tr, er, tn, en).astype(np.float32)
    n_r, n = len(tr), len(tr) + len(tn)
    z = np.zeros(n, dtype=np.float32); z[n_r:] = 1.0       # 1 = new arm
    obs = float((z @ U) @ (1.0 - z))                       # sum of U[i, j] over i in new, j in reference
    Z, exact = assignments(n, len(tn), np.random.default_rng(seed))
    cnt = 0
    for i in range(0, len(Z), 200_000):
        Zc = Z[i:i + 200_000].astype(np.float32)
        cnt += int((np.abs(((Zc @ U) * (1.0 - Zc)).sum(axis=1)) >= abs(obs) - 1e-6).sum())
    pairs = U[n_r:, :n_r]
    tot = pairs.size
    return dict(p=cnt / len(Z) if exact else (cnt + 1) / (len(Z) + 1), exact=exact,
                new_faster=float((pairs > 0).sum() / tot), ref_faster=float((pairs < 0).sum() / tot),
                undetermined=float((pairs == 0).sum() / tot))


def perm_mean_diff(a, b, seed=3):
    rng = np.random.default_rng(seed)
    z = np.concatenate([a, b]); obs = a.mean() - b.mean()
    Z, exact = assignments(len(z), len(a), rng)
    cnt = 0
    for i in range(0, len(Z), 200_000):
        Zc = Z[i:i + 200_000].astype(float)
        d = (Zc @ z) / len(a) - ((1.0 - Zc) @ z) / len(b)
        cnt += int((np.abs(d) >= abs(obs) - 1e-12).sum())
    bs = a[rng.integers(len(a), size=(B, len(a)))].mean(axis=1) - b[rng.integers(len(b), size=(B, len(b)))].mean(axis=1)
    lo, hi = np.quantile(bs, [0.025, 0.975])
    return dict(diff=float(obs), lo=float(lo), hi=float(hi), p=cnt / len(Z) if exact else (cnt + 1) / (len(Z) + 1),
                exact=exact)


def fisher_two_sided(a, n1, b, n2) -> float:
    """Fisher's exact test for a of n1 against b of n2."""
    k, N = a + b, n1 + n2
    pr = lambda x: math.comb(n1, x) * math.comb(n2, k - x) / math.comb(N, k)
    p0 = pr(a)
    return float(min(1.0, sum(pr(x) for x in range(max(0, k - n2), min(k, n1) + 1) if pr(x) <= p0 * (1 + 1e-9))))


def holm(ps: dict) -> dict:
    keys = sorted(ps, key=lambda k: ps[k])
    m, out, run = len(keys), {}, 0.0
    for i, k in enumerate(keys):
        run = max(run, min(1.0, (m - i) * ps[k]))
        out[k] = run
    return out


def f(v, d=1):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "n/a"
    if not np.isfinite(v):
        return "unbounded"
    return f"{v:.{d}f}"


def pv(p) -> str:
    return "< 0.0001" if p < 0.0001 else f"{p:.4f}"


def af_txt(r, key="af") -> str:
    """The ratio, or why there is none: an arm whose median is unbounded reached the target in under half its seeds."""
    mr, mn = r["median_ref"], r["median_new"]
    if not np.isfinite(mn) and not np.isfinite(mr):
        return "none (neither arm's median is bounded)"
    if not np.isfinite(mn):
        return "none (new arm's median unbounded)"
    if not np.isfinite(mr):
        return "unbounded (reference's median unbounded)"
    return f(r[key], 2)


def compare(ref, new, camp, target, col=0, mode="twin"):
    tr, er = hits(ref, camp, target, col)
    tn, en = hits(new, camp, target, col)
    mr, mn = med(tr, er, mode), med(tn, en, mode)
    lo, hi, tail = boot_ratio(tr, er, tn, en, mode)
    g = gehan_test(tr, er, tn, en)
    return dict(median_ref=mr, median_new=mn, af=ratio(mr, mn), lo=lo, hi=hi, boot_share_af_le_1=tail,
                hit_ref=int(er.sum()), hit_new=int(en.sum()), n_ref=len(tr), n_new=len(tn), **g,
                x_ref=[round(float(x), 1) if o else None for x, o in zip(tr, er)],
                x_new=[round(float(x), 1) if o else None for x, o in zip(tn, en)])


# ------------------------------------------------------------------------------------------------ report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("twin", type=Path, help="path to byu-vcl/vertical-lab at 357d149")
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    root = a.twin
    oracle = json.loads((root / "out" / "twin2" / "oracle.json").read_text())
    T1 = {c: float(oracle[c]["sota_utility"]) for c in CAMPS}
    summ = json.loads((root / "out" / "twin2" / "bench2_summary.json").read_text())
    T2 = {c: float(summ["targets"]["T2"][c]) for c in CAMPS}

    main_, conv = load(root, "main"), load(root, "conventional")
    stock, seeded, d256 = load(root, "stock"), load(root, "seeded"), load(root, "seeded_dal256")
    hidden, cu_seeds, cu_money = load(root, "cu_hidden"), load(root, "cu_seeds"), load(root, "cu_money")
    V = {p: arm(main_, policy=p) for p in ("bofn_blend", "bofn", "heuristic", "tiered", "gpbo", "random", "sobol",
                                           "cost_aware")}
    C = {p: arm(conv, policy=p) for p in ("bofn", "heuristic", "tiered", "gpbo", "random", "sobol")}
    VL = {p: arm(stock, policy=p) for p in ("bofn", "heuristic")}
    VS = {p: arm(seeded, policy=p) for p in ("bofn", "gpbo", "random")}
    D = {p: arm(d256, policy=p) for p in ("bofn", "gpbo", "random")}
    H = {p: arm(hidden, policy=p) for p in ("bofn_blend", "bofn", "tiered", "heuristic", "gpbo", "random")}
    out = dict(targets=dict(T1=T1, T2=T2), arms={}, time={}, cash={}, final={}, replay={}, t2={})
    P = print

    P("# Recomputed from the stored runs (byu-vcl 357d149)\n")
    P("Written by `recompute.py`; see its docstring for the definitions. Days are days since the campaign started.\n")
    P(f"Targets: T1 (the video's \"state of the art\") = {T1}; T2 (the harder target in `bench2_summary.json`) = {T2}.\n")

    # ---- every arm
    P("## 1. Every arm: seeds that reached T1, and when\n")
    P("| Arm (file) | Campaign | Reached T1 | Median days (twin) | KM median | Earliest to latest | Mean final best |")
    P("|---|---|---|---|---|---|---|")
    arms = [("automated, stocked", "main", V), ("conventional, lean, 3 y", "conventional", C),
            ("automated, lean", "stock", VL), ("automated, stocked, DAL 275 seeds", "seeded", VS),
            ("DAL 256 schedule, lean, DAL 275 seeds", "seeded_dal256", D), ("automated, hidden Cu effect", "cu_hidden", H)]
    for lab, fn, grp in arms:
        for pol, runs in grp.items():
            for camp in CAMPS:
                if fn == "cu_hidden" and camp != "onr_cu":
                    continue
                t, e = hits(runs, camp, T1[camp])
                fb = final_best(runs, camp)
                row = dict(n=len(t), hit=int(e.sum()), median=med(t, e), km=km_median(t, e),
                           lo=float(t[e].min()) if e.any() else None, hi=float(t[e].max()) if e.any() else None,
                           final_mean=float(fb.mean()), final_se=float(fb.std(ddof=1) / math.sqrt(len(fb))),
                           days=[round(float(x), 1) if o else None for x, o in zip(t, e)])
                out["arms"][f"{fn}|{pol}|{camp}"] = row
                P(f"| {lab}, `{pol}` (`{fn}.jsonl`) | {NAME[camp]} | {row['hit']}/{row['n']} | {f(row['median'])} | "
                  f"{f(row['km'])} | {f(row['lo'])} to {f(row['hi'])} | {row['final_mean']:.3f} ± {row['final_se']:.3f} |")
    P()

    # ---- time to target
    comps = [
        ("video headline: automated `bofn_blend` vs conventional `bofn`", C["bofn"], V["bofn_blend"], True),
        ("same optimizer on both: automated `bofn` vs conventional `bofn`", C["bofn"], V["bofn"], False),
        ("video footer: automated `bofn_blend` vs conventional `heuristic`", C["heuristic"], V["bofn_blend"], True),
        ("heuristic on both: automated `heuristic` vs conventional `heuristic`", C["heuristic"], V["heuristic"], False),
        ("automated `tiered` vs conventional `tiered`", C["tiered"], V["tiered"], False),
        ("automated `gpbo` vs conventional `gpbo`", C["gpbo"], V["gpbo"], False),
        ("stocking removed: automated lean `bofn` vs conventional lean `bofn`", C["bofn"], VL["bofn"], False),
        ("stocking removed: automated lean `heuristic` vs conventional lean `heuristic`", C["heuristic"],
         VL["heuristic"], False),
        ("stocking alone: automated stocked `bofn` vs automated lean `bofn`", VL["bofn"], V["bofn"], False),
        ("today's schedule: automated seeded `bofn` vs DAL 256 schedule seeded `bofn`", D["bofn"], VS["bofn"], False),
        ("optimizer alone, automated lab: `heuristic` (ref) vs `bofn_blend`", V["heuristic"], V["bofn_blend"], True),
        ("optimizer alone, automated lab: `gpbo` (ref) vs `bofn`", V["gpbo"], V["bofn"], False),
        ("optimizer alone, automated lab: `random` (ref) vs `bofn`", V["random"], V["bofn"], False),
        ("optimizer alone, conventional lab: `heuristic` (ref) vs `bofn`", C["heuristic"], C["bofn"], False),
    ]
    P("## 2. Time to T1: acceleration factors, intervals and tests\n")
    P("AF = median days of the reference arm ÷ median days of the new arm. `new faster` / `ref faster` are shares of "
      "the seed pairs (one seed from each arm) whose order is known. p: two-sided permutation test, Gehan statistic.\n")
    P("| Comparison (reference → new) | Campaign | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap "
      "interval | AF with KM medians | new faster / ref faster / unknown | p |")
    P("|---|---|---|---|---|---|---|---|---|")
    fam = {}
    for lab, ref, new, in_video in comps:
        for camp in CAMPS:
            r = compare(ref, new, camp, T1[camp])
            k = compare(ref, new, camp, T1[camp], mode="km")
            r["af_km"], r["km_lo"], r["km_hi"] = k["af"], k["lo"], k["hi"]
            out["time"][f"{lab}|{camp}"] = r
            if in_video:
                fam[f"time|{lab}|{camp}"] = r["p"]
            P(f"| {lab} | {NAME[camp]} | {r['hit_ref']}/{r['n_ref']}, {r['hit_new']}/{r['n_new']} | "
              f"{f(r['median_ref'])}, {f(r['median_new'])} | {af_txt(r)} | {f(r['lo'], 2)} to {f(r['hi'], 2)} | "
              f"{af_txt(k)} ({f(k['lo'], 2)} to {f(k['hi'], 2)}) | "
              f"{r['new_faster']:.0%} / {r['ref_faster']:.0%} / {r['undetermined']:.0%} | {pv(r['p'])} |")
    P()

    # ---- cash to target
    P("## 3. Cash to T1 (\"the campaigns' own spending\")\n")
    P("Ratio = median cash the new arm had spent when it reached T1 ÷ the reference's. Below 1: the new arm spent less.\n")
    P("| Comparison (reference → new) | Campaign | Median cash (ref, new) | Ratio new ÷ ref | 95% bootstrap interval | p |")
    P("|---|---|---|---|---|---|")
    for lab, ref, new, in_video in comps[:4]:
        for camp in CAMPS:
            r = compare(ref, new, camp, T1[camp], col=1)
            inv = lambda v: (math.inf if v == 0 else (0.0 if not np.isfinite(v) else 1.0 / v))
            y = dict(ratio=inv(r["af"]), lo=inv(r["hi"]), hi=inv(r["lo"]), p=r["p"], median_ref=r["median_ref"],
                     median_new=r["median_new"])
            out["cash"][f"{lab}|{camp}"] = y
            if in_video:
                fam[f"cash|{lab}|{camp}"] = r["p"]
            ytxt = f(y['ratio'], 2) if np.isfinite(r['median_new']) and np.isfinite(r['median_ref']) else "none (a median is unbounded)"
            P(f"| {lab} | {NAME[camp]} | ${f(r['median_ref'], 0)}, ${f(r['median_new'], 0)} | {ytxt} | "
              f"{f(y['lo'], 2)} to {f(y['hi'], 2)} | {pv(r['p'])} |")
    P()

    # ---- final best
    P("## 4. Best alloy at the end of the year (mean true utility over seeds)\n")
    P("| Comparison (a against b) | Campaign | Seeds | Mean a | Mean b | a - b | 95% bootstrap interval | p (permutation) |")
    P("|---|---|---|---|---|---|---|---|")
    t24 = arm(main_, policy="tiered") + arm(cu_seeds, policy="tiered")
    b24 = arm(main_, policy="bofn_blend") + arm(cu_seeds, policy="bofn_blend")
    finals = [
        ("Cu: `tiered` against `bofn_blend`, main (seeds 0-11)", V["tiered"], V["bofn_blend"], "onr_cu", True),
        ("Cu: `tiered` against `bofn_blend`, seeds 12-23 only (`cu_seeds.jsonl`)", arm(cu_seeds, policy="tiered"),
         arm(cu_seeds, policy="bofn_blend"), "onr_cu", False),
        ("Cu: `tiered` against `bofn_blend`, all 24 seeds", t24, b24, "onr_cu", False),
        ("Cu, hidden effect: `tiered` against `bofn_blend`", H["tiered"], H["bofn_blend"], "onr_cu", True),
        ("Cu, hidden effect: `bofn_blend` against `bofn`", H["bofn_blend"], H["bofn"], "onr_cu", False),
        ("Cu: `bofn_blend` against `bofn`", V["bofn_blend"], V["bofn"], "onr_cu", False),
        ("Cu, triple the money: `tiered` against `bofn_blend` (`cu_money.jsonl`)", arm(cu_money, policy="tiered"),
         arm(cu_money, policy="bofn_blend"), "onr_cu", False),
        ("Al: `bofn_blend` against `heuristic`", V["bofn_blend"], V["heuristic"], "flaime_al", True),
        ("Al: `bofn` against `gpbo`", V["bofn"], V["gpbo"], "flaime_al", False),
        ("Al: `bofn` against `random`", V["bofn"], V["random"], "flaime_al", False),
        ("Cu: `bofn` against `gpbo`", V["bofn"], V["gpbo"], "onr_cu", False),
        ("Cu: `bofn` against `random`", V["bofn"], V["random"], "onr_cu", False),
        ("Al, seeded: `bofn` against `gpbo`", VS["bofn"], VS["gpbo"], "flaime_al", False),
        ("Cu, seeded: `bofn` against `gpbo`", VS["bofn"], VS["gpbo"], "onr_cu", False),
    ]
    for lab, x, y, camp, in_video in finals:
        fa, fb = final_best(x, camp), final_best(y, camp)
        r = perm_mean_diff(fa, fb)
        r.update(mean_a=float(fa.mean()), mean_b=float(fb.mean()), n_a=len(fa), n_b=len(fb),
                 a=[round(float(v), 3) for v in fa], b=[round(float(v), 3) for v in fb])
        out["final"][lab] = r
        if in_video:
            fam[f"final|{lab}"] = r["p"]
        P(f"| {lab} | {NAME[camp]} | {len(fa)}, {len(fb)} | {fa.mean():.3f} | {fb.mean():.3f} | {r['diff']:+.3f} | "
          f"{r['lo']:+.3f} to {r['hi']:+.3f} | {pv(r['p'])} |")
    P()

    # ---- Holm
    adj = holm(fam)
    out["holm"] = {k: dict(p=fam[k], p_holm=adj[k]) for k in fam}
    P(f"## 5. Holm's correction over the {len(fam)} comparisons the video states\n")
    P("The family: the two headline speed-ups, the two against the heuristic, the two cash ratios shown in the results "
      "frame (the other cost bases are sums of the same cash and a time-proportional charge, so they are tested "
      "through days and cash), the heuristic-against-BOFN order on aluminium, and the three final-alloy comparisons "
      "of the description.\n")
    P("| Claim | p | Holm-adjusted p | Survives at 0.05 |")
    P("|---|---|---|---|")
    for k in sorted(fam, key=lambda k: fam[k]):
        P(f"| {k.replace('|', ': ')} | {pv(fam[k])} | {pv(adj[k])} | {'yes' if adj[k] < 0.0495 else ('on the line' if adj[k] < 0.0505 else 'no')} |")
    P()

    # ---- the replayed seed
    P("## 6. The replayed seed (seed 0 of automated `bofn_blend`) against the 12 seeds\n")
    P("| Campaign | Seed 0 reached T1 on day | Rank among 12 (1 = earliest) | Median of 12 | Seed 0 final best | Rank "
      "(1 = best) | Mean of 12 |")
    P("|---|---|---|---|---|---|---|")
    for camp in CAMPS:
        t, e = hits(V["bofn_blend"], camp, T1[camp])
        fb = final_best(V["bofn_blend"], camp)
        r = dict(day=float(t[0]), rank=int((t < t[0]).sum()) + 1, median=float(np.median(t)), final=float(fb[0]),
                 final_rank=int((fb > fb[0]).sum()) + 1, final_mean=float(fb.mean()))
        out["replay"][camp] = r
        P(f"| {NAME[camp]} | {r['day']:.1f} | {r['rank']} | {r['median']:.1f} | {r['final']:.3f} | {r['final_rank']} | "
          f"{r['final_mean']:.3f} |")
    P()

    # ---- the harder target
    P("## 7. The same headline at the harder target T2\n")
    P("| Comparison | Campaign | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap interval |")
    P("|---|---|---|---|---|---|")
    for lab, ref, new, _ in comps[:4]:
        for camp in CAMPS:
            r = compare(ref, new, camp, T2[camp])
            out["t2"][f"{lab}|{camp}"] = r
            P(f"| {lab} | {NAME[camp]} | {r['hit_ref']}/{r['n_ref']}, {r['hit_new']}/{r['n_new']} | "
              f"{f(r['median_ref'])}, {f(r['median_new'])} | {af_txt(r)} | {f(r['lo'], 2)} to {f(r['hi'], 2)} |")
    P()

    # ---- first results and budgets
    P("## 8. When each lab had its first new alloy, and what the year cost in cash\n")
    P("| Arm | Campaign | Median day of the first new alloy tested | Median new alloys tested by the end | Median cash "
      "spent (budget) |")
    P("|---|---|---|---|---|")
    for lab, runs in (("automated, stocked, `bofn_blend` (1 year)", V["bofn_blend"]),
                      ("automated, lean, `bofn` (1 year)", VL["bofn"]),
                      ("conventional, lean, `bofn` (3 years)", C["bofn"]),
                      ("DAL 256 schedule, lean, seeded `bofn` (1 year)", D["bofn"])):
        for camp in CAMPS:
            first = [r["campaigns"][camp]["curve_new"][0][0] for r in runs if r["campaigns"][camp].get("curve_new")]
            n = [len(r["campaigns"][camp].get("curve_new") or []) for r in runs]
            sp = [r["campaigns"][camp]["spent"] for r in runs]
            bud = runs[0]["campaigns"][camp].get("budget")
            out.setdefault("first", {})[f"{lab}|{camp}"] = dict(first=float(np.median(first)) if first else None,
                                                                n=float(np.median(n)), spent=float(np.median(sp)),
                                                                budget=bud)
            P(f"| {lab} | {NAME[camp]} | {f(float(np.median(first)) if first else None)} | {np.median(n):.0f} | "
              f"${np.median(sp):,.0f} (${bud:,.0f}) |")
    P()
    # ---- copper with all 24 automated seeds
    P("## 9. Copper with all 24 automated seeds (`main.jsonl` seeds 0-11 plus `cu_seeds.jsonl` seeds 12-23)\n")
    P("The conventional lab has 12 seeds. The video's copper headline uses automated seeds 0-11 only.\n")
    P("| Comparison (reference → new) | Reached (ref, new) | Median days (ref, new) | AF | 95% bootstrap interval | p |")
    P("|---|---|---|---|---|---|")
    for lab, ref, new in (("conventional `bofn` → automated `bofn_blend`, seeds 0-11 (the video's)", C["bofn"], V["bofn_blend"]),
                          ("conventional `bofn` → automated `bofn_blend`, seeds 12-23", C["bofn"], arm(cu_seeds, policy="bofn_blend")),
                          ("conventional `bofn` → automated `bofn_blend`, all 24", C["bofn"], b24),
                          ("conventional `heuristic` → automated `bofn_blend`, all 24", C["heuristic"], b24),
                          ("conventional `tiered` → automated `bofn_blend`, all 24", C["tiered"], b24),
                          ("conventional `tiered` → automated `tiered`, all 24", C["tiered"], t24)):
        r = compare(ref, new, "onr_cu", T1["onr_cu"])
        out.setdefault("cu24", {})[lab] = r
        P(f"| {lab} | {r['hit_ref']}/{r['n_ref']}, {r['hit_new']}/{r['n_new']} | {f(r['median_ref'])}, "
          f"{f(r['median_new'])} | {af_txt(r)} | {f(r['lo'], 2)} to {f(r['hi'], 2)} | {pv(r['p'])} |")
    P()

    # ---- the same one-year window in both labs
    P("## 10. Seeds at T1 within the first 365 days, both labs on the same window\n")
    P("The conventional runs last three years; this counts only their first year. p: Fisher's exact test, two-sided.\n")
    P("| Policy (conventional, automated) | Campaign | Conventional by day 365 | Automated by day 365 | p |")
    P("|---|---|---|---|---|")
    for pc, pa in (("bofn", "bofn_blend"), ("bofn", "bofn"), ("heuristic", "heuristic"), ("tiered", "tiered"),
                   ("gpbo", "gpbo"), ("random", "random"), ("sobol", "sobol")):
        for camp in CAMPS:
            tc, ec = hits(C[pc], camp, T1[camp]); ta, ea = hits(V[pa], camp, T1[camp])
            hc, ha = int((ec & (tc <= 365.0)).sum()), int((ea & (ta <= 365.0)).sum())
            pf = fisher_two_sided(hc, len(tc), ha, len(ta))
            out.setdefault("year1", {})[f"{pc}|{pa}|{camp}"] = dict(conv=hc, auto=ha, n_conv=len(tc), n_auto=len(ta), p=pf)
            P(f"| `{pc}`, `{pa}` | {NAME[camp]} | {hc}/{len(tc)} | {ha}/{len(ta)} | {pf:.3f} |")
    P()
    if a.json:
        a.json.write_text(json.dumps(out, indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else o))


if __name__ == "__main__":
    main()
