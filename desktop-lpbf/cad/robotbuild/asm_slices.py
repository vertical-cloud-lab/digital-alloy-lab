"""Render the assembly chapters in slices while the planner is still running (round 8; round 9: both chapters from one queue,
under /tmp/memslot; issue #260, PR #266).

    /tmp/venv/bin/python asm_slices.py module:M12,M19,M26 chamber:C09f,C14,F05b,F10a,F16,F25,F31,F39,F45,F51,F55 \\
        [--results=<planner's results_run13.json>] [--traj=/tmp/robotbuild/traj/run13] [--upto=T01] [--max-running=3]
        [--slices=module:1,chamber:4] [--mem=3]

Each chapter's cut list splits it at those steps: slice k is [cut k-1, cut k) (the first from the chapter's opening, the last to
its end). Slice k is started once the planner has finished its last step (the step at cut k has a row in the results file,
which run_assembly.py rewrites after every step) or the chapter's recording is complete (asm_<chapter>.pkl exists, or, for a
run recorded in pieces, the results file has a row for the chapter's last step). Every slice gets its chapter's whole cut list
as ASM_CUTS: each boundary is a soft one (asm_render.py, round 9: no shot-plan decision reaches across it, but the camera may
carry on across it), so each slice's frames are the chapter's own. At most --max-running slices at a time, module slices first;
each runs with ROBOTBUILD_AUDIT=1 under /tmp/memslot <mem> (which waits for room in the runner's shared memory budget, then
caps the slice). Then merge_parts.py.
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
LAST = {"module": "M30", "chamber": None}      # the chapter's last step (None: the chamber ends where --upto says)
# round 10: each chapter's own settings, as round 9's final renders had them (asm_render.py's docstring): the module's person
# at least 1.8 m from the place's tripods, the chamber's short hops between the cell's docks held in the work's shot. Set in
# the environment to override
CHAPTER_ENV = {"module": {"ASM_PERSON_CAM_MIN": "1800"}, "chamber": {"ASM_DRIVE_HOLD": "1"}}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def main(argv):
    specs = [a for a in argv if not a.startswith("--")]
    opt = {a.split("=")[0][2:]: a.split("=", 1)[1] for a in argv if a.startswith("--") and "=" in a}
    res = OUT / opt.get("results", "results_run13.json")
    traj = pathlib.Path(opt.get("traj", "/tmp/robotbuild/traj/run13"))
    upto = opt.get("upto", "T01")
    mem = opt.get("mem", "3")
    notes = pathlib.Path(opt["notes"]) if opt.get("notes") else OUT / "run10_fail_notes.json"     # round 10: --notes=
    only = {}
    for x in opt.get("slices", "").split(","):
        if ":" in x:
            c, k = x.split(":")
            only.setdefault(c, set()).add(int(k))
    queue, cut_of = [], {}
    for spec in specs:
        chapter, _, cl = spec.partition(":")
        cuts = [c for c in cl.split(",") if c]
        cut_of[chapter] = cuts
        bounds = [""] + cuts + [""]
        for k in range(len(bounds) - 1):
            if chapter in only and k not in only[chapter]:
                continue
            queue.append((chapter, k, bounds[k], bounds[k + 1]))

    def done_steps():
        try:
            return {r["id"] for r in json.loads(res.read_text())["rows"]}
        except Exception:   # noqa: BLE001  (being rewritten)
            return set()

    def chapter_done(chapter):
        if (traj / f"asm_{chapter}.pkl").exists():
            return True
        last = LAST.get(chapter) or upto
        return bool(last) and last in done_steps()

    running = {}
    specs_of, tries = {}, {}            # round 10: a slice's queue entry and how often it was started
    while queue or running:
        for key, p in list(running.items()):
            if p.poll() is not None:
                log(f"slice {key} finished, exit {p.returncode}")
                del running[key]
                spec_ = specs_of.get(key)
                if p.returncode != 0 and spec_ is not None and tries.get(key, 0) < 3:
                    queue.insert(0, spec_)  # round 10: a failed slice (an X display race, a crash) is drawn again
                    log(f"slice {key} queued again (try {tries.get(key, 0) + 1})")
        limit = int(opt.get("max-running", 3))
        if opt.get("max-running-file") and os.path.exists(opt["max-running-file"]):
            try:                       # round 10: the limit can be changed while it runs (fewer while another chapter renders)
                limit = int(open(opt["max-running-file"]).read().strip())
            except ValueError:
                pass
        started = False
        if len(running) < limit:
            for qi, (chapter, k, a, b) in enumerate(queue):
                if not (chapter_done(chapter) or (b and b in done_steps())):
                    continue
                queue.pop(qi)
                env = dict(CHAPTER_ENV.get(chapter, {}))
                env.update(os.environ)
                env.update(ROBOTBUILD_AUDIT="1", ASM_TRAJ=str(traj), ASM_STEPS=f"{a}:{b}", ASM_RANGE_IDX=str(k),
                           ASM_CUTS=",".join(cut_of[chapter]), ASM_UPTO=upto, OMP_NUM_THREADS="1", LP_NUM_THREADS="1")
                env.pop("ASM_PART", None)
                env.pop("ASM_RANGE", None)
                lf = open(os.path.join(opt.get("logdir", "/tmp"), f"asm_slice_{chapter}_{k}.log"), "a")
                cmd = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24", "/tmp/memslot", mem, sys.executable, "asm_render.py",
                       chapter]
                if chapter == "chamber" and notes.exists():
                    cmd.append(f"--fail_notes={notes}")
                running[f"{chapter}.{k}"] = subprocess.Popen(cmd, cwd=str(HERE), env=env, stdout=lf, stderr=subprocess.STDOUT)
                specs_of[f"{chapter}.{k}"] = (chapter, k, a, b)
                tries[f"{chapter}.{k}"] = tries.get(f"{chapter}.{k}", 0) + 1
                log(f"slice {chapter}.{k} [{a or 'opening'}, {b or 'end'}) started "
                    f"(chapter recorded: {'yes' if chapter_done(chapter) else 'not yet'})")
                started = True
                break
        if not started:
            time.sleep(20)
        else:
            time.sleep(10)              # round 10: two xvfb-run -a starting together can race for one display number
    log("all slices done")


if __name__ == "__main__":
    main(sys.argv[1:])
