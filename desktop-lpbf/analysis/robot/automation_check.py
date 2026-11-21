"""Interference sweep of the robot-tending features (cad/automation.py) against the rest of the model, with
analysis/interference.py's own method (manifold3d mesh booleans at a 0.05 mm chord, confirmed by exact OpenCascade booleans;
FCL gaps for the moving ones). Only pairs that involve an automation part are checked, in interference.py's five static states
and through the full sweep of each motion group an automation part rides on (gdoor, door, drawer, recoater).

Run:  python desktop-lpbf/analysis/robot/automation_check.py [MODULE]   -> analysis/out/robot/automation_interference.{json,md}
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "cad"))
import interference as IF  # noqa: E402
import lpbf_low as M  # noqa: E402

OUT = HERE.parent / "out" / "robot"


def main():
    module = sys.argv[1] if len(sys.argv) > 1 else "M50"
    t0 = time.time()
    md = IF.Model(module)
    N = md.names
    mine = {i for i, p in enumerate(md.parts) if "automation" in p.tags}
    rep = dict(module=module, automation_parts=[N[i] for i in sorted(mine)], states=[], sweeps=[], clearances=[])
    states = {"closed, parked, piston up": {},
              "plate exchange: doors open, plate up 8 mm": {"door": M.MOTION["door"]["hi"], "gdoor": M.MOTION["gdoor"]["hi"],
                                                             "piston": M.MOTION["piston"]["hi"]},
              "doors open, reservoir and drawer out": {"door": M.MOTION["door"]["hi"], "gdoor": M.MOTION["gdoor"]["hi"],
                                                        "cartridge": M.MOTION["cartridge"]["lo"], "drawer": M.MOTION["drawer"]["lo"]},
              "recoater at the end, piston at the bottom stop": {"recoater": M.MOTION["recoater"]["hi"], "piston": M.MOTION["piston"]["lo"]},
              "module swap: arm released, module dropped": {"zstage": M.MOTION["zstage"]["lo"], "module": M.MP.MODULE_DROP,
                                                            "gdoor": M.MOTION["gdoor"]["hi"]}}
    for label, st in states.items():
        n, hits, joints = md.check(st, only=mine)
        rep["states"].append(dict(state=label, pose=st, pairs_checked=n,
                                  interferences=[dict(a=N[i], b=N[j], mesh_mm3=round(v, 2), exact_mm3=round(ve, 2)) for i, j, v, ve in hits]))
        print(f"[{time.time() - t0:5.1f} s] {label}: {n} pairs, {len(hits)} interferences", flush=True)
    groups = sorted({md.parts[i].group for i in mine if md.parts[i].group})
    for g in groups:
        m = M.MOTION[g]
        mov = {i for i, p in enumerate(md.parts) if M.moves_with(p, g)}
        worst, gaps = {}, {}
        for k in range(IF.N_SWEEP + 1):
            v = m["lo"] + (m["hi"] - m["lo"]) * k / IF.N_SWEEP
            st = dict(m.get("base_state", {}))
            st[g] = v
            if g in ("cartridge", "drawer"):
                st["gdoor"] = M.MOTION["gdoor"]["hi"]
            n, hits, _ = md.check(st, only=mov)
            for i, j, vm, ve in hits:
                if i not in mine and j not in mine:
                    continue
                key = (N[i], N[j])
                if key not in worst or ve > worst[key][1]:
                    worst[key] = (v, ve)
            for i, j, d in md.min_gaps(st, g):
                if i not in mine and j not in mine:
                    continue
                key = (N[i], N[j])
                if key not in gaps or d < gaps[key][1]:
                    gaps[key] = (v, d)
        rep["sweeps"].append(dict(group=g, range=[m["lo"], m["hi"]], steps=IF.N_SWEEP + 1,
                                  interferences=[dict(a=a, b=b, at=round(v, 2), exact_mm3=round(ve, 2)) for (a, b), (v, ve) in worst.items()]))
        for (a, b), (v, d) in sorted(gaps.items(), key=lambda kv: kv[1][1])[:8]:
            rep["clearances"].append(dict(group=g, at=round(v, 2), moving=a, other=b, gap_mm=round(d, 3)))
        print(f"[{time.time() - t0:5.1f} s] sweep {g}: {len(worst)} interfering pairs", flush=True)
    rep["runtime_s"] = round(time.time() - t0, 1)
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"automation_interference{'' if module == 'M50' else '-' + module}"
    (OUT / f"{stem}.json").write_text(json.dumps(rep, indent=1))
    L = [f"# Interference check of the robot-tending features ({module})", "",
         f"`analysis/robot/automation_check.py`, {rep['runtime_s']} s: interference.py's mesh + exact booleans for every pair that involves one of "
         f"the {len(mine)} automation parts, in five states and through the sweeps of {', '.join(groups)}.", "",
         "| State or sweep | Interferences |", "|---|---|"]
    for s in rep["states"]:
        L.append(f"| {s['state']} | {len(s['interferences'])} " + "".join(f"<br>{h['a']} / {h['b']}: {h['exact_mm3']} mm³" for h in s["interferences"]) + " |")
    for s in rep["sweeps"]:
        L.append(f"| sweep {s['group']} | {len(s['interferences'])} " + "".join(f"<br>{h['a']} / {h['b']} at {h['at']}: {h['exact_mm3']} mm³" for h in s["interferences"]) + " |")
    L += ["", "Tightest gaps of the moving automation parts:", "", "| Group | At | Moving | Other | Gap (mm) |", "|---|---|---|---|---|"]
    for c in rep["clearances"]:
        L.append(f"| {c['group']} | {c['at']} | {c['moving'][:60]} | {c['other'][:60]} | {c['gap_mm']} |")
    (OUT / f"{stem}.md").write_text("\n".join(L) + "\n")
    print("done", rep["runtime_s"], "s")


if __name__ == "__main__":
    main()
