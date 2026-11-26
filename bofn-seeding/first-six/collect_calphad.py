#!/usr/bin/env python3
"""Turn the CALPHAD screen's JSONL output into the CSV tables used by the write-up and by process_models.py.

    python collect_calphad.py /tmp/sim/res            # reads named.jsonl, exploratory.jsonl, grids.jsonl,
                                                      # pool.jsonl and liquidus_cost507.jsonl if present

Melt setpoint rule (one rule for every alloy, as #111 asks for superheat rather than a fixed setpoint):
    setpoint = max(highest liquidus of any phase in either database + 100 C, 820 C), rounded up to 10 C.
The "highest liquidus" matters for Zr, Ti, Cr and Mn: below it the melt holds crystals that can block the
nozzle and that take the grain refiner out of the powder.
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "results" / "calphad"


def load(path):
    if not path.exists():
        return []
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def fmt_wt(wt):
    return "-".join(f"{v:g}{k.capitalize()}" for k, v in sorted(wt.items(), key=lambda kv: -kv[1]))


def main():
    src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sim/res")
    OUT.mkdir(parents=True, exist_ok=True)
    liq2 = {r["name"]: r for r in load(src / "liquidus_cost507.jsonl") if r.get("ok")}
    for extra in sorted(src.glob("liquidus_cost507_*.jsonl")):
        liq2.update({r["name"]: r for r in load(extra) if r.get("ok")})
    named = [r for f in ("named.jsonl", "exploratory.jsonl", "x1.jsonl") for r in load(src / f) if r.get("ok")]
    rows = []
    for r in named:
        t = r.get("tags", {})
        c = liq2.get(r["name"], {})
        l1, l2 = r.get("liquidus_C"), c.get("liquidus_C")
        top = max(x for x in (l1, l2) if x is not None)
        top_phase = r.get("primary_phase") if (l2 is None or (l1 is not None and l1 >= l2)) else c.get("primary_phase")
        setpoint = max(math.ceil((top + 100.0) / 10.0) * 10, 820)
        ph = r.get("phases", {})
        imc = sum(v for k, v in ph.items() if k not in ("FCC_A1",))
        rows.append(dict(
            id=t.get("id", r["name"]), base=t.get("base", ""), group=t.get("group", ""), note=t.get("note", ""),
            composition_wt=fmt_wt(r["wt"]),
            liquidus_C=l1, primary_phase=r.get("primary_phase"),
            liquidus_cost507_C=l2 if l2 is not None else "", primary_phase_cost507=c.get("primary_phase") or "",
            cost507_left_out=" ".join(c.get("left_out", [])),
            highest_liquidus_C=top, highest_liquidus_phase=top_phase, melt_setpoint_C=setpoint,
            T_fcc_start_C=round(r.get("T_fcc_start_C", float("nan")), 1), fs_at_fcc_start=round(r.get("fs_at_fcc_start", float("nan")), 3),
            T_end_C=round(r.get("T_end_C", float("nan")), 1), freezing_range_alpha_K=round(r.get("dT_fcc", float("nan")), 1),
            dT_90_99_K=round(r.get("dT_90_99", float("nan")), 1), dT_80_95_K=round(r.get("dT_80_95", float("nan")), 1),
            kou_index_K=round(r.get("kou_index", float("nan"))), csc=round(r.get("csc", float("nan")), 2),
            f_last_2K=round(r.get("f_last_2K", float("nan")), 3), second_phase_fraction=round(imc, 3),
            scheil_phases="; ".join(f"{k} {v:.3f}" for k, v in sorted(ph.items(), key=lambda kv: -kv[1])),
            eq_400C="; ".join(f"{k} {v:.3f}" for k, v in sorted((r.get("eq", {}).get("400") or {}).items(), key=lambda kv: -kv[1])),
            scheil_status=r.get("scheil_status", ""), seconds=r.get("seconds"),
        ))
    with open(OUT / "scheil_paths.jsonl", "w") as fh:      # coarse curves for the figure
        for r in named:
            t = r.get("tags", {})
            if "scheil_T_at_fs" in r:
                fh.write(json.dumps({"name": f"{t.get('id', r['name'])}|{t.get('base', '')}", "fs_grid": r["fs_grid"],
                                     "scheil_T_at_fs": r["scheil_T_at_fs"]}) + "\n")
    order = {"seed": 0, "extra": 1, "exploratory": 2, "relative": 3, "known-cracker": 4, "baseline": 5}
    rows.sort(key=lambda d: (order.get(d["group"], 9), d["id"], d["base"]))
    if rows:
        with open(OUT / "named.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("named.csv", len(rows))
    # grids and pool
    for name in ("grids", "pool"):
        g = [r for r in load(src / f"{name}.jsonl") if r.get("ok")]
        out = []
        for r in g:
            c = liq2.get(r["name"], {})
            out.append(dict(
                name=r["name"], grid=r.get("tags", {}).get("grid", ""), composition_wt=fmt_wt(r["wt"]),
                **{k.capitalize(): v for k, v in r["wt"].items()},
                liquidus_C=r.get("liquidus_C"), primary_phase=r.get("primary_phase"),
                liquidus_cost507_C=c.get("liquidus_C", ""), primary_phase_cost507=c.get("primary_phase", ""),
                T_fcc_start_C=r.get("T_fcc_start_C", ""), T_end_C=r.get("T_end_C", ""), dT_90_99_K=r.get("dT_90_99", ""),
                kou_index_K=r.get("kou_index", ""), csc=r.get("csc", ""), f_last_2K=r.get("f_last_2K", ""),
                scheil_status=r.get("scheil_status", ""),
            ))
        if out:
            keys = []
            for d in out:
                for k in d:
                    if k not in keys:
                        keys.append(k)
            with open(OUT / f"{name}.csv", "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=keys, restval="")
                w.writeheader()
                w.writerows(out)
            print(f"{name}.csv", len(out))
    # liquidus-only grid from COST 507 (and MatCalc where run)
    lq = [r for r in liq2.values() if r.get("tags", {}).get("grid", "").startswith("liq-")]
    if lq:
        with open(OUT / "liquidus_vs_content.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["grid", "composition_wt", "liquidus_cost507_C", "primary_phase_cost507"])
            for r in sorted(lq, key=lambda r: (r["tags"]["grid"], sum(r["wt"].values()))):
                w.writerow([r["tags"]["grid"], fmt_wt(r["wt"]), r.get("liquidus_C"), r.get("primary_phase")])
        print("liquidus_vs_content.csv", len(lq))


if __name__ == "__main__":
    main()
