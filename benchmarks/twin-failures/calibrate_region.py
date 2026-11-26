"""Where the hidden 'won't atomize' region sits against the truth (for the ``lab_region`` regime).

For random designs of each space (the twin's own sampler) at the default atomizer settings and a few process
settings, the true utility from ``twin/oracle.py``; then, for each threshold s0 of ``failures.region_score``, the share
of all designs and of the best 5 % that fall in the region (region_p >= 0.45, half of its maximum). The chosen s0
puts about a third of the best designs inside: the optimum sits at the region's edge, as the toy in
``bofn-failed-vs-abandoned.md`` §5 assumed.

    TWIN_DIR=/tmp/byu-vcl/vertical-lab python calibrate_region.py      # -> results/region_calibration.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, os.environ.get("TWIN_DIR", "/tmp/byu-vcl/vertical-lab"))
sys.path.insert(0, str(HERE))


def main(n=500, n_proc=6):
    from twin import oracle as O

    import failures as F
    out = {}
    for key in ("flaime_al", "onr_cu"):
        camp = O._camp(key, 0)
        sp = camp.space
        procs = O.proc_grid(key, n_proc, np.random.default_rng(1))
        ds = sp.sample(n, seed=11)
        us = np.array([O.true_utility(camp, d, procs, np.random.default_rng(3))[0] for d in ds])
        comps = [sp.composition(d) for d in ds]
        s = np.array([F.region_score(key, c) for c in comps])
        top = us >= np.quantile(us, 0.95)
        rows = []
        for s0 in np.round(np.arange(0.1, 2.01, 0.05), 3):
            inside = s >= s0
            rows.append(dict(s0=float(s0), all=float(inside.mean()), top5=float(inside[top].mean()),
                             positive=float(inside[us > 0].mean()) if (us > 0).any() else None))
        cur = F.REGION[key]["s0"]
        out[key] = dict(n=n, frac_positive=float((us > 0).mean()), q95=float(np.quantile(us, 0.95)),
                        current_s0=cur, table=rows,
                        current=dict(all=float((s >= cur).mean()), top5=float((s >= cur)[top].mean())),
                        top5_scores=sorted(np.round(s[top], 3).tolist()))
        print(key, "s0", cur, out[key]["current"], "positive", round(out[key]["frac_positive"], 3), flush=True)
        for r in rows:
            if abs(r["top5"] - 1 / 3) < 0.2:
                print("   ", r, flush=True)
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "region_calibration.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
