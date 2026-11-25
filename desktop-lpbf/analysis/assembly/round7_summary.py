"""Round 7 summary (issue #260, PR #266): pass/fail before (run 7, results.json) and after (run 9, results_run9.json), the
fetches from the long table, the screw presenter trips, and the per-step real time (/tmp/robotbuild/traj/run9/assembly.json).

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/round7_summary.py [before.json] [after.json] [times.json] [out.json]

Writes analysis/out/assembly/round7.json (or out.json: run 10 against run 9 is round7_run10.json) and prints markdown
tables for assembly.md.
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "assembly"


def checked(rows):
    """Steps whose arm motion was checked (arm PASS, FAIL, PART or ERROR; notes, unchecked seal placements and the held-part
    screw sub-rows, which their step already counts, left out)."""
    return [r for r in rows if str(r.get("arm")) in ("PASS", "FAIL", "PART", "ERROR") and not r["id"].endswith("h")]


def ok(r):
    return str(r.get("arm")) in ("PASS", "-") and str(r.get("sweep")) in ("PASS", "-", "?", "None")


def screws(rows):
    n = sum(int(r.get("n") or 0) for r in rows if r.get("do") == "screws")
    k = sum(int(r.get("n_ok") or 0) for r in rows if r.get("do") == "screws")
    return k, n


def main(argv):
    before = pathlib.Path(argv[0]) if len(argv) > 0 else OUT / "results.json"
    after = pathlib.Path(argv[1]) if len(argv) > 1 else OUT / "results_run9.json"
    times = pathlib.Path(argv[2]) if len(argv) > 2 else pathlib.Path("/tmp/robotbuild/traj/run9/assembly.json")
    rb = json.loads(before.read_text())["rows"]
    ra = json.loads(after.read_text())["rows"]
    cb, ca = checked(rb), checked(ra)
    sb, sa = screws(rb), screws(ra)
    out = dict(before=dict(file=before.name, checked=len(cb), passed=sum(ok(r) for r in cb), screws_ok=sb[0], screws=sb[1]),
               after=dict(file=after.name, checked=len(ca), passed=sum(ok(r) for r in ca), screws_ok=sa[0], screws=sa[1]))
    fetch = [r for r in ra if r.get("fetch")]
    out["fetch"] = dict(steps=len(fetch), passed=sum(1 for r in fetch if r["fetch"] == "PASS"),
                        person=sum(1 for r in fetch if r["fetch"] == "person"),
                        failed=[dict(id=r["id"], why=r.get("fetch_why", "")) for r in fetch if r["fetch"] == "FAIL"])
    pres = [r.get("presenter") for r in ra if r.get("presenter")]
    out["presenter"] = dict(planned=sum(int(p.split("/")[0]) for p in pres), driven=sum(int(p.split("/")[1]) for p in pres))
    out["still_failing"] = [dict(id=r["id"], label=r.get("label", "")[:90], why=(r.get("why") or "")[:200]) for r in ca if not ok(r)]
    b_ids = {r["id"]: ok(r) for r in cb}
    out["fixed"] = [r["id"] for r in ca if ok(r) and r["id"] in b_ids and not b_ids[r["id"]]]
    if times.exists():
        t = json.loads(times.read_text())
        out["time"] = dict(robot_h=t.get("robot_h"), person_h=t.get("person_h"),
                           elapsed_h=round(sum(s["seconds"] for s in t["steps"]) / 3600.0, 2),
                           by_chapter={c: round(sum(s["seconds"] for s in t["steps"] if s.get("chapter") == c) / 3600.0, 2)
                                       for c in ("module", "chamber")})
    (OUT / (argv[3] if len(argv) > 3 else "round7.json")).write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("before", "after", "fetch", "presenter")}, indent=1))
    print("fixed:", out["fixed"])
    for r in out["still_failing"]:
        print(f"| {r['id']} | {r['label']} | {r['why'][:150]} |")
    if "time" in out:
        print("time:", out["time"])


if __name__ == "__main__":
    main(sys.argv[1:])
