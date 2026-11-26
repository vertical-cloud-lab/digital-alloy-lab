"""Render an assembly chapter in slices while the planner is still running (round 8, issue #260, PR #266).

    /tmp/venv/bin/python asm_slices.py chamber C09f,C14,F05b,F10a,F16,F25,F31,F39,F45,F51,F55 [--results=results_run12.json]
        [--traj=/tmp/robotbuild/traj/run12] [--upto=T01] [--max-running=2] [--max-done=3]

The cut list splits the chapter at those steps: slice k is [cut k-1, cut k) (the first from the chapter's opening, the last to
its end). Slice k is started once the planner has finished its last step (its row is in the results file, which
run_assembly.py rewrites after every step) or the run is over (asm_<chapter>.pkl exists); every slice gets the same ASM_CUTS,
so each boundary is a forced cut and the slices' frames are the chapter's own (asm_render.py). At most --max-running slices
at a time while the planner runs (its 3 GB and two 3 GB renders: 9 GB), --max-done once it is over, and none while a slice of
another chapter is still rendering. Every slice runs with ROBOTBUILD_AUDIT=1 under /tmp/capmem 3G; then merge_parts.py.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "analysis" / "out" / "assembly"


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def main(argv):
    chapter, cuts = argv[0], [c for c in argv[1].split(",") if c]
    opt = {a.split("=")[0][2:]: a.split("=", 1)[1] for a in argv[2:] if a.startswith("--") and "=" in a}
    res = OUT / opt.get("results", "results_run12.json")
    traj = pathlib.Path(opt.get("traj", "/tmp/robotbuild/traj/run12"))
    notes = OUT / "run10_fail_notes.json"
    bounds = [""] + cuts + [""]
    queue = [(k, bounds[k], bounds[k + 1]) for k in range(len(bounds) - 1)]
    only = [int(x) for x in opt.get("slices", "").split(",") if x]
    if only:
        queue = [s for s in queue if s[0] in only]

    def done_steps():
        try:
            return {r["id"] for r in json.loads(res.read_text())["rows"]}
        except Exception:   # noqa: BLE001  (being rewritten)
            return set()

    def planner_done():
        return (traj / f"asm_{chapter}.pkl").exists()

    def other_running():
        other = "module" if chapter == "chamber" else "chamber"
        return bool(subprocess.run(["pgrep", "-f", f"asm_render.py {other}"], capture_output=True, text=True).stdout.split())

    running = {}
    while queue or running:
        for k, p in list(running.items()):
            if p.poll() is not None:
                log(f"slice {k} finished, exit {p.returncode}")
                del running[k]
        limit = int(opt.get("max-done", 3)) if planner_done() else int(opt.get("max-running", 2))
        if queue and len(running) < limit and not other_running():
            k, a, b = queue[0]
            if planner_done() or (b and b in done_steps()):
                queue.pop(0)
                env = dict(os.environ, ROBOTBUILD_AUDIT="1", ASM_TRAJ=str(traj), ASM_STEPS=f"{a}:{b}", ASM_RANGE_IDX=str(k),
                           ASM_CUTS=",".join(cuts), ASM_UPTO=opt.get("upto", "T01"))
                env.pop("ASM_PART", None)
                lf = open(f"/tmp/asm_slice_{chapter}_{k}.log", "w")
                cmd = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24", "/tmp/capmem", "3G", sys.executable, "asm_render.py", chapter]
                if chapter == "chamber" and notes.exists():
                    cmd.append(f"--fail_notes={notes}")
                running[k] = subprocess.Popen(cmd, cwd=str(HERE), env=env, stdout=lf, stderr=subprocess.STDOUT)
                log(f"slice {k} [{a or 'opening'}, {b or 'end'}) started (planner {'done' if planner_done() else 'running'})")
                continue
        time.sleep(20)
    log("all slices done")


if __name__ == "__main__":
    main(sys.argv[1:])
