"""Summarize the bofn-prelim pKGFN diagnosis runs (diagnose.py outputs) into a table.

    python summarize.py <dir with pkgfn_k0_s*.json and pkgfn_la_k0_s*.json>
"""
import glob
import json
import sys

import numpy as np

D = sys.argv[1]
out = {}
for kind in ("pkgfn", "pkgfn_la"):
    runs = [json.load(open(f)) for f in sorted(glob.glob(f"{D}/{kind}_k0_s*.json"))]
    if not runs:
        continue
    best = np.array([r["final_best_validated"] for r in runs])
    ceil0 = np.array([r["iters"][0]["ceiling"] for r in runs])
    ceilN = np.array([r["iters"][-1]["ceiling"] for r in runs])
    nT = sum(it["kg_T_scored"] for r in runs for it in r["iters"])
    zT = sum(it["kg_T_zero"] for r in runs for it in r["iters"])
    its = [it for r in runs for it in r["iters"][1:]]
    kgA0 = np.mean([it["kg_max"].get("A", 0.0) <= 1e-12 for it in its if "A" in it["kg_max"]])
    kgC0 = np.mean([it["kg_max"].get("C", 0.0) <= 1e-12 for it in its if "C" in it["kg_max"]])
    kgL0 = np.mean([it["kg_max"].get("L", 0.0) <= 1e-12 for it in its if "L" in it["kg_max"]])
    fb = np.mean([it["fallback"] for it in its])
    buys = {g: np.mean([sum(1 for a in r["actions"][1:] if a == g) for r in runs]) for g in ("C", "A", "L", "T")}
    out[kind] = dict(n=len(runs), best_mean=float(best.mean()), best_se=float(best.std(ddof=1) / np.sqrt(len(best))),
                     best=[round(float(b), 3) for b in best], ceiling_start=float(ceil0.mean()), ceiling_end=float(ceilN.mean()),
                     ceiling_min=float(ceilN.min()), kgT_zero_frac=zT / max(nT, 1), kgT_scored=nT, kgA_zero_frac=float(kgA0),
                     kgC_zero_frac=float(kgC0), kgL_zero_frac=float(kgL0), fallback_frac=float(fb), buys=buys,
                     seeds=[r["seed"] for r in runs])
    print(f"{kind}: n={len(runs)} best {100 * best.mean():.1f} ± {100 * best.std(ddof=1) / np.sqrt(len(best)):.1f}% "
          f"(per seed {np.round(100 * best).astype(int).tolist()}); restricted ceiling {100 * ceil0.mean():.1f}% at the start, "
          f"{100 * ceilN.mean():.1f}% at the end (min {100 * ceilN.min():.1f}%)")
    print(f"   KG of a tensile test exactly 0 for {zT}/{nT} scored candidates ({zT / max(nT, 1):.0%}); best KG of atomizing "
          f"0 on {kgA0:.0%} of steps, of CALPHAD 0 on {kgC0:.0%}, of printing 0 on {kgL0:.0%}; fallback on {fb:.0%}")
    print(f"   new purchases per run: " + ", ".join(f"{g} {v:.1f}" for g, v in buys.items()))
json.dump(out, open(f"{D}/summary.json", "w"), indent=1)
if "pkgfn" in out and "pkgfn_la" in out:
    a = {s: b for s, b in zip(out["pkgfn"]["seeds"], out["pkgfn"]["best"])}
    b = {s: x for s, x in zip(out["pkgfn_la"]["seeds"], out["pkgfn_la"]["best"])}
    common = sorted(set(a) & set(b))
    from scipy.stats import wilcoxon
    d = np.array([b[s] - a[s] for s in common])
    print(f"pkgfn_la - pkgfn on {len(common)} matched seeds: {100 * d.mean():+.1f} ± {100 * d.std(ddof=1) / np.sqrt(len(d)):.1f} points, "
          f"ahead on {(d > 0).sum()}, behind on {(d < 0).sum()}, p = {wilcoxon(d).pvalue:.3g}")
