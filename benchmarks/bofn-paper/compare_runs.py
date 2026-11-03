"""Check re-runs against stored runs, action for action.

    python compare_runs.py results/k1 results-rerun/k1              # every <policy>_s<seed>.json in both
    python compare_runs.py results/k1/ei_s0.json /tmp/check/k1/ei_s0.json

A pair matches action for action when the rows record the same purchases in
the same order: the same `action` (stage, or "full"/"reuse" for the
whole-pipeline policies) at the same cumulative `spent`, with the same
per-stage `counts`. Because the stored runs do not log the purchased designs,
the scores recorded after every purchase are compared too: `best_validated` and
`rec_printed` are true-objective values of designs the run actually bought, so a
different design almost always shows up in them even when the stage label is
the same. `rec` (and its design `x_rec`) is the arg max of the network mean over
a random pool; it is reported but not part of the match, since it does not
feed back into any decision. Runs written by this version of run_sweep.py also
log every purchase's inputs (`purchases`), and those are compared when both
sides have them. Runs where a side skipped the recommender (BOFN_NO_REC) have
NaN `rec`; the NaN-vs-number pairs are skipped.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

TOL = 1e-9  # scores within this are treated as equal (the stored runs are noise-free)


def _maxdiff(a, b):
    """Largest |a - b| over paired values, skipping pairs where either side is NaN."""
    m = 0.0
    for u, v in zip(a, b):
        if isinstance(u, list):
            m = max(m, _maxdiff(u, v))
        elif not (math.isnan(u) or math.isnan(v)):
            m = max(m, abs(u - v))
    return m


def compare(pa: Path, pb: Path) -> dict:
    A, B = json.loads(pa.read_text()), json.loads(pb.read_text())
    ra, rb = A["rows"], B["rows"]
    seq = lambda rows: [(r["action"], r["spent"]) for r in rows]  # noqa: E731
    sa, sb = seq(ra), seq(rb)
    first = next((i for i, (u, v) in enumerate(zip(sa, sb)) if u != v), None)
    if first is None and len(sa) != len(sb):
        first = min(len(sa), len(sb))
    out = {
        "kind": A["kind"], "seed": A["seed"], "rows": (len(ra), len(rb)),
        "same_actions": first is None and A["counts"] == B["counts"], "first_divergence": first,
        "d_best_validated": _maxdiff([r["best_validated"] for r in ra], [r["best_validated"] for r in rb]),
        "d_rec_printed": _maxdiff([r["rec_printed"] for r in ra], [r["rec_printed"] for r in rb]),
        "d_rec": _maxdiff([r["rec"] for r in ra], [r["rec"] for r in rb]),
        "d_x_rec": _maxdiff([r["x_rec"] for r, q in zip(ra, rb) if not (math.isnan(r["rec"]) or math.isnan(q["rec"]))],
                            [q["x_rec"] for r, q in zip(ra, rb) if not (math.isnan(r["rec"]) or math.isnan(q["rec"]))]),
        "final": (ra[-1]["best_validated"], rb[-1]["best_validated"]),
        "wall_s": (A.get("wall_s"), B.get("wall_s")),
        "d_purchases": None,
    }
    if "purchases" in A and "purchases" in B:
        pa_, pb_ = A["purchases"], B["purchases"]
        same = len(pa_) == len(pb_) and all(u[0] == v[0] and u[1] == v[1] for u, v in zip(pa_, pb_))
        out["d_purchases"] = _maxdiff([u[2] for u in pa_], [v[2] for v in pb_]) if same else math.inf
    out["match"] = (out["same_actions"] and out["d_best_validated"] <= TOL and out["d_rec_printed"] <= TOL
                    and (out["d_purchases"] is None or out["d_purchases"] <= TOL))
    return out


def pairs(a: Path, b: Path):
    if a.is_file():
        return [(a, b)]
    return [(p, b / p.name) for p in sorted(a.glob("*.json")) if (b / p.name).exists()]


def table(results) -> str:
    """One markdown row per policy."""
    by = defaultdict(list)
    for r in results:
        by[r["kind"]].append(r)
    lines = ["| policy | seeds | match action for action | first divergence (row) | max abs diff, best validated | max abs diff, rec_printed | max abs diff, rec |",
             "|---|---|---|---|---|---|---|"]
    for k, rs in by.items():
        rs.sort(key=lambda r: r["seed"])
        n_ok = sum(r["match"] for r in rs)
        div = ", ".join(f"s{r['seed']}: {r['first_divergence']}" for r in rs if r["first_divergence"] is not None) or "none"
        f = lambda key: f"{max(r[key] for r in rs):.1e}"  # noqa: E731
        lines.append(f"| {k} | {','.join(str(r['seed']) for r in rs)} | {n_ok}/{len(rs)} | {div} | {f('d_best_validated')} | {f('d_rec_printed')} | {f('d_rec')} |")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = Path(sys.argv[1]), Path(sys.argv[2])
    results = [compare(pa, pb) for pa, pb in pairs(a, b)]
    if not results:
        sys.exit(f"no common run files in {a} and {b}")
    for r in results:
        verdict = "MATCH" if r["match"] else ("same stages, scores differ" if r["same_actions"] else f"diverges at row {r['first_divergence']}")
        print(f"{r['kind']:>13s} s{r['seed']:<3d} {verdict:28s} rows {r['rows'][0]}/{r['rows'][1]}  "
              f"max|d| best_validated {r['d_best_validated']:.1e}  rec_printed {r['d_rec_printed']:.1e}  rec {r['d_rec']:.1e}  x_rec {r['d_x_rec']:.1e}"
              + (f"  purchases {r['d_purchases']:.1e}" if r["d_purchases"] is not None else "")
              + f"  final {r['final'][0]:.4f}/{r['final'][1]:.4f}")
    print()
    print(table(results))
    sys.exit(0 if all(r["match"] for r in results) else 1)


if __name__ == "__main__":
    main()
