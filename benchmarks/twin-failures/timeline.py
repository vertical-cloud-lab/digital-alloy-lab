"""One simulated year, run by run: every atomizer booking with its campaign and outcome (made powder, failed from a
transient cause, failed from the inputs), the repair windows, and both campaigns' best new alloy so far, for a few
strategies on the same seed (the 'anatomy of a year' figure).

    TWIN_DIR=/tmp/byu-vcl/vertical-lab python timeline.py run [SEED] [REGIME] STRATEGY ...   # -> results/timeline_*.json
    python timeline.py fig [SEED] [REGIME] STRATEGY ...                                      # -> figures/twinfail_timeline_*.png
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("TWIN_DIR", "/tmp/byu-vcl/vertical-lab"))
sys.path.insert(0, str(HERE))
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")


def one(args):
    strategy, seed, regime = args
    import torch
    torch.set_num_threads(1)
    from twin import bench2 as B2
    from twin import campaign as C
    from twin import spaces as SP
    from twin.opt import policies3 as P3

    import failures as F
    import strategies as ST
    specs = {k: C.Spec(k, B2.BUDGET[k], B2.WIP[k], seed, 1.0, stock="stocked") for k in B2.BUDGET}
    pols = {k: (ST.make(strategy, k, seed) if strategy in ST.FMODES else P3.make3(strategy, k, seed, None))
            for k in specs}
    tw = C.Twin(specs, pols, scenario="historical", facility="vertical_lab", seed=seed, horizon_days=365, mode="async")
    st = F.install(tw, regime, seed=seed)
    s = tw.run()
    fac = next(iter(tw.facilities.values()))
    runs = []
    for (a, b, camp, what, tag) in fac.res["atomizer"].jobs:
        if what != "atomize" or not tag or not str(tag.get("sample", "")).startswith("L"):
            continue
        c = tw.campaigns[camp]
        lid = int(tag["sample"][1:])
        rr = (c._lot_truth.get(lid) or {}).get("runs") or []
        j = tag.get("run")
        r = rr[j] if j is not None and j < len(rr) else {}
        out = "ok" if not r.get("failed") else (r.get("cause") or "intrinsic")
        runs.append(dict(t0=round(a / 24, 3), t1=round(b / 24, 3), campaign=camp, design=tag.get("design"),
                         outcome=out))
    curves = {}
    for k in specs:
        camp = tw.campaigns[k]
        refs = [{e: w.get(e, 0.0) for e in SP.SPACES[k].elements} for w in SP.REFERENCE[k].values()]
        best, cur = 0.0, []
        for d in sorted(s[k]["demonstrated"], key=lambda d: d["t_h"]):
            comp = camp.designs[d["design"]]["composition"]
            if any(all(abs(comp.get(e, 0.0) - r[e]) < 0.06 for e in r) for r in refs):
                continue
            best = max(best, d["u"])
            cur.append((round(d["t_h"] / 24, 3), round(best, 4)))
        curves[k] = cur
    res = dict(strategy=strategy, seed=seed, regime=regime, runs=runs, curves=curves,
               repairs=[dict(t0=round(d["t_h"] / 24, 3), days=d["days"], campaign=d["campaign"]) for d in st["damage"]],
               breakdowns=[(round(a / 24, 3), round(b / 24, 3)) for a, b in fac.res["atomizer"].down
                           if (a, b) not in set(map(tuple, st["windows"]))])
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / f"timeline_{strategy}_{regime}_s{seed}.json").write_text(json.dumps(res))
    return strategy


def fig(seed, regime, strategies):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from figures import CAMPS, CNAME, COL, LABEL, TEXT, TEXT2, _style

    from analyze import TARGETS
    D = [json.loads((HERE / "results" / f"timeline_{p}_{regime}_s{seed}.json").read_text()) for p in strategies]
    OC = {"ok": ("made powder", "#257de0"), "transient": ("failed: transient", "#f47230"),
          "intrinsic": ("failed: the inputs", "#00b894")}
    fig, axes = plt.subplots(3, len(D), figsize=(5.6 * len(D), 7.2), sharex=True,
                             gridspec_kw=dict(height_ratios=(1.0, 2.2, 2.2)))
    if len(D) == 1:
        axes = axes[:, None]
    for j, d in enumerate(D):
        ax = axes[0, j]
        for r in d["repairs"]:
            for i in range(3):
                axes[i, j].axvspan(r["t0"], r["t0"] + r["days"], color="#efefef", lw=0, zorder=0)
        for i, camp in enumerate(CAMPS):
            for oc, (lab, c) in OC.items():
                xs = [r["t0"] for r in d["runs"] if r["campaign"] == camp and r["outcome"] == oc]
                ax.scatter(xs, [1 - i + (0.12 if oc != "ok" else 0)] * len(xs), s=10, marker="|", color=c,
                           linewidths=1.5, label=lab if (i == 0 and j == 0) else None)
        ax.set_yticks([1, 0])
        ax.set_yticklabels(["Al runs", "Cu runs"], fontsize=8, color=TEXT)
        ax.set_ylim(-0.5, 1.6)
        n_rep = len(d["repairs"])
        ax.set_title(f"{LABEL[d['strategy']]}\nseed {seed}, regime '{regime}': {len(d['runs'])} runs, "
                     f"{n_rep} repairs ({sum(r['days'] for r in d['repairs']):.0f} days, shaded)", fontsize=8.5,
                     color=TEXT, loc="left")
        _style(ax)
        ax.grid(False)
        for i, camp in enumerate(CAMPS):
            ax = axes[1 + i, j]
            cur = d["curves"][camp]
            xs = [0] + [c[0] for c in cur] + [365]
            ys = [0] + [c[1] for c in cur] + [cur[-1][1] if cur else 0]
            ax.step(xs, ys, where="post", color=COL.get(d["strategy"], TEXT), lw=2)
            for t, ls in (("T1", (0, (4, 3))), ("T2", (0, (1, 2)))):
                ax.axhline(TARGETS[t][camp], color=TEXT2, lw=1, ls=ls)
                ax.text(3, TARGETS[t][camp] + 0.01, t, fontsize=7, color=TEXT2)
            ax.set_ylim(0, 0.95)
            ax.set_ylabel(CNAME[camp] + "\nbest new alloy", fontsize=8, color=TEXT2)
            _style(ax)
        axes[2, j].set_xlabel("simulated day", fontsize=8.5, color=TEXT2)
        axes[2, j].set_xlim(0, 365)
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.01),
               markerscale=2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    out = HERE / "figures" / f"twinfail_timeline_{regime}_s{seed}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(out)


if __name__ == "__main__":
    cmd, seed, regime, strats = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4:]
    if cmd == "run":
        with ProcessPoolExecutor(min(len(strats), int(os.environ.get("TWIN_WORKERS", "2")))) as ex:
            print(list(ex.map(one, [(p, seed, regime) for p in strats])))
    else:
        fig(seed, regime, strats)
