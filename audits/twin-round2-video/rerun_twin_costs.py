"""Re-run the twin's own cost model on the stored runs and compare with the stored summary.

    python audits/twin-round2-video/rerun_twin_costs.py /tmp/byu-vcl/vertical-lab rerun_costs.json

Imports twin/econ.py and twin/accel.py from the byu-vcl checkout (357d149), so unlike recompute.py this is not an
independent check: it shows that out/twin2/econ/econ_summary.json is what that code gives from out/twin2/runs. The
"shared" bases take the per-station utilization stored in the summary. Needs numpy only."""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
import twin.econ as E
import twin.accel as AC
S = json.loads((root / "out/twin2/econ/econ_summary.json").read_text())
rows = E.load_runs([str(root / p) for p in S["inputs"]["runs"]])
G = E.group_runs(rows)
_ev = {}
def events_of(r):
    f = r.get("events_file")
    if not f: return None
    p = root / f
    if not p.exists(): return None
    if str(p) not in _ev: _ev[str(p)] = json.loads(p.read_text())
    return _ev[str(p)]
_sh = {}
def shares_of(r):
    c = r["cfg"]
    key = (c["facility"], E._pol(c["policy"]), c.get("scenario", "historical"), E.variant(c))
    if key not in _sh:
        ev = next((events_of(x) for x in G.get(key, []) if events_of(x) is not None), None)
        _sh[key] = E.shares_from_events(ev) if ev else None
    return _sh[key]
T = S["targets"]["values"]
out = {}
for name in ("vertical lab + bofn_blend vs conventional + bofn", "vertical lab + bofn_blend vs conventional + heuristic"):
    for camp in ("flaime_al", "onr_cu"):
        st = S["acceleration"][name][camp]
        rk, nk = tuple(st["ref"].split("|")), tuple(st["new"].split("|"))
        rk = rk if rk in G else next(k for k in G if "|".join(k) == st["ref"])
        nk = nk if nk in G else next(k for k in G if "|".join(k) == st["new"])
        su = st.get("shared_utilization")
        ref, new = AC.curves_of(G[rk], camp), AC.curves_of(G[nk], camp)
        cc = lambda key, basis, u=None: E.cost_curves(G[key], camp, basis, utilization=u, events_of=events_of, shares_of=shares_of)
        cr, cn = {"cash": cc(rk, "cash")}, {"cash": cc(nk, "cash")}
        for b in ("operating", "full"):
            cr[f"{b}, alone"] = cr[f"{b}, shared"] = cc(rk, b)
            cn[f"{b}, alone"] = cc(nk, b)
            cn[f"{b}, shared"] = cc(nk, b, su or None)
        cmp = AC.compare(ref, new, T[camp], cr, cn, n_boot=2000)
        d, sd = cmp["days"], st["compare"]["days"]
        print(f"{name} | {camp} | days AF rerun {d['af']:.3f} ({d['lo']:.3f}-{d['hi']}) stored {sd['af']} ({sd['lo']}-{sd['hi']})")
        for b, y in cmp["cost"].items():
            sy = st["compare"]["cost"][b]
            print(f"    {b:18s} rerun {y['ratio']:.3f} ({y['lo']:.3f}-{y['hi']:.3f})  stored {sy['ratio']:.3f} ({sy['lo']:.3f}-{sy['hi']:.3f})  medians rerun {y['median_ref']:.0f}/{y['median_new']:.0f}")
            out[f"{name}|{camp}|{b}"] = dict(rerun=y["ratio"], lo=y["lo"], hi=y["hi"], stored=sy["ratio"], median_ref=y["median_ref"], median_new=y["median_new"])
json.dump(out, open(sys.argv[2], "w"), indent=1, default=str)
