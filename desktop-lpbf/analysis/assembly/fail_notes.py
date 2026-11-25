"""The assembly's failure notes for the robot-built video (issue #260, PR #266, round 7): what failed in an earlier run (run 7
in round 6, run 9 in round 7) and the fix, kept for the steps that pass in run 10. asm_render.py shows each as a 3 s card
before the redesigned step (--fail_notes), and ch_summary.py lists them on its redesign slide (asm_fail_notes.json).

    python desktop-lpbf/analysis/assembly/fail_notes.py /tmp/robotbuild/data/asm_fail_notes.json      # from the repo root
"""
import json, pathlib, sys
OUT = pathlib.Path("desktop-lpbf/analysis/out/assembly")
r10 = {r["id"]: r for r in json.loads((OUT / "results_run10.json").read_text())["rows"]}
def ok(r):
    return r is not None and str(r.get("arm")) in ("PASS", "-") and str(r.get("sweep")) in ("PASS", "-", "?", "None")
notes = {
 "F10a": "the stock fingers met the module handle in the door opening. Round 7: the liner wand, two suction cups on a 300 mm bar",
 "F10b": "the stock fingers met the frame in the door opening. Round 7: the liner wand, two suction cups on a 300 mm bar",
 "F10d": "the stock fingers met the module handle in the door opening. Round 7: the liner wand",
 "F10e": "the stock fingers met the frame in the door opening. Round 7: the liner wand",
 "F14": "arm A had no pose behind the back wall; its holding wrist met arm B's driver. Round 7: the plenum hangs on two dowels; arm B places it and drives",
 "F16": "arm B's driver met arm A's holding wrist on all four screws. Round 7: the adapter hangs on two dowels; no holding arm",
 "F23": "arm B's driver met arm A's holding wrist on all four screws. Round 7: the cap hangs on two dowels; no holding arm",
 "F18": "on a held-part screw, arm B's upper arm met the base plate, then arm A's driver met the chamber body. Round 7: roles swapped, a 60 mm bit extension",
 "F25": "the motor bracket, brought in along -x, started inside the trunnion's stands. Round 7: the bracket is lowered from above (F25b)",
 "F26": "the blade holder met the frame under the door opening, then stood 5 mm outside it. Round 7: in 9 mm high and 6 mm right, then slid left inside",
 "F27": "the driver met the module's spigot, then the arm met Fixture B. Round 7: arm B from the back, with a 100 mm bit extension",
 "F45": "the diagonal path swept the threaded nose through the base, then arm A met the base plate. Round 7: along its own axis, by arm B",
 "F45b": "arm A's upper arm met the base plate. Round 7: by arm B from the back",
 "F45c": "arm A found no pose to start from. Round 7: by arm B from the back",
 "F48b": "the window stack moved off the tilted line of sight, then the pad's body met the boss. Round 7: along the line of sight, the ring pad on a 100 mm stem",
 "F52": "the fingertips holding the pin's end met the door's face, 6 mm behind the hinge axis. Round 7: the pin pusher, a magnet in a Ø4.5 rod's tip",
 "F52b": "the fingertips holding the pin's end met the door's face. Round 7: the pin pusher, a magnet in a Ø4.5 rod's tip",
 "F03": "arm A could not reach the back posts' screws under the plate. Round 7: the far arm holds each post, the near arm drives",
 "F54": "no pair of arm poses 260 mm above the posts. Round 7: lowered the last 80 mm only, a hoist takes the 14.3 kg",
 "F56b": "no IK at the start, 340 mm up. Round 7: from 60 mm above",
 "F57": "the three tubes as one 107 mm part, then the dichroic met a tube placed first. Round 7: one piece at a time, the cubes before the tubes",
}
keep, still = {}, {}
for k, v in notes.items():
    (keep if ok(r10.get(k)) else still)[k] = v if ok(r10.get(k)) else (r10.get(k) or {}).get("why", "")[:160]
json.dump(keep, open(sys.argv[1], "w"), indent=1)
print("redesign notes kept:", sorted(keep))
print("still failing in run 10:", json.dumps(still, indent=1))
