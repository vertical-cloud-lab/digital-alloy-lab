"""Submit, wait for, and fetch the copper/DED element queries (PR #117).

Usage (from repo root):
    python edison-trajectories/cu-ded-elements-2026-10/run_elements.py submit <phase>
    python edison-trajectories/cu-ded-elements-2026-10/run_elements.py wait <phase> [max_minutes]
    python edison-trajectories/cu-ded-elements-2026-10/run_elements.py fetch
    python edison-trajectories/cu-ded-elements-2026-10/run_elements.py status

Phase 1 is in queries.py. Later phases (ANALYSIS jobs with uploaded files) are
in analysis_prompts.py; their entries carry an "uploads" list of paths
relative to this directory, uploaded before the task is created.

`fetch` writes one markdown file per finished task (phaseN/<name>.md, the
question first, then Edison's answer) and the gzipped verbose trajectory
(raw/<name>.json.gz). Adapted from ../cu-ded-2026-10/edison_cu_ded.py.

Requires: pip install edison-client ; EDISON_PLATFORM_API_KEY in the env.
"""

import gzip
import json
import os
import pathlib
import sys
import time
from datetime import datetime, timezone

from edison_client import EdisonClient, JobNames, TaskRequest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from queries import PHASES  # noqa: E402

try:
    from analysis_prompts import LATER_PHASES  # noqa: E402
    PHASES.update(LATER_PHASES)
except ImportError:
    pass

PHASE_DIRS = {1: "phase1", 2: "phase2", 3: "phase3", 4: "electrochem"}
TASK_FILE = HERE / "_task_ids.json"
RAW_DIR = HERE / "raw"
TERMINAL = {"success", "fail", "failed", "cancelled", "error", "truncated"}


def client() -> EdisonClient:
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load() -> dict:
    return json.loads(TASK_FILE.read_text()) if TASK_FILE.exists() else {}


def save(records: dict) -> None:
    TASK_FILE.write_text(json.dumps(records, indent=2) + "\n")


def submit(phase: int) -> None:
    records = load()
    c = client()
    for name, spec in PHASES[phase].items():
        if name in records:
            print(f"{name}: already submitted ({records[name]['task_id']})", flush=True)
            continue
        req = TaskRequest(name=getattr(JobNames, spec["job"]), query=spec["query"])
        files = None
        if spec.get("uploads"):
            files = []
            for rel in spec["uploads"]:
                files.append(c.upload_file(str(HERE / rel)))
            print(f"{name}: uploaded {len(files)} files", flush=True)
        for attempt in range(5):
            try:
                if files:
                    task_id = str(c.create_task(task_data=req, files=files))
                else:
                    task_id = str(c.create_task(task_data=req))
                break
            except Exception as exc:  # rate limits or transient errors
                print(f"{name}: submit error {type(exc).__name__}: {exc}; retrying",
                      flush=True)
                time.sleep(20 * (attempt + 1))
        else:
            print(f"{name}: giving up", flush=True)
            continue
        records[name] = {"phase": phase, "task_id": task_id, "job": spec["job"],
                         "submitted": now()}
        save(records)
        print(f"{name}: {spec['job']} -> {task_id}", flush=True)
        time.sleep(2)


def poll(c: EdisonClient, records: dict, names: list) -> dict:
    statuses = {}
    for name in names:
        try:
            statuses[name] = str(c.get_task(task_id=records[name]["task_id"]).status)
        except Exception as exc:  # transient API errors: keep polling
            statuses[name] = f"poll-error: {type(exc).__name__}"
    return statuses


def wait(phase: int, max_minutes: float = 40.0, interval: int = 120) -> None:
    c = client()
    records = load()
    mine = [n for n, r in records.items() if r["phase"] == phase and "fetched" not in r]
    start = time.time()
    while True:
        statuses = poll(c, records, mine)
        elapsed = (time.time() - start) / 60
        done = sum(s in TERMINAL for s in statuses.values())
        pending = sorted(n for n, s in statuses.items() if s not in TERMINAL)
        print(f"[{now()} +{elapsed:.1f} min] phase {phase}: {done}/{len(mine)} done; "
              f"{len(pending)} pending: {', '.join(pending)[:400]}", flush=True)
        if not pending or elapsed > max_minutes:
            break
        time.sleep(interval)


def fetch() -> None:
    c = client()
    records = load()
    RAW_DIR.mkdir(exist_ok=True)
    for name, rec in records.items():
        if "fetched" in rec:
            continue
        try:
            task = c.get_task(task_id=rec["task_id"])
        except Exception as exc:
            print(f"{name}: poll error {type(exc).__name__}", flush=True)
            continue
        status = str(task.status)
        rec["status"] = status
        if status not in TERMINAL:
            print(f"{name}: still {status}", flush=True)
            continue
        verbose = c.get_task(task_id=rec["task_id"], verbose=True)
        with gzip.open(RAW_DIR / f"{name}.json.gz", "wt", encoding="utf-8") as fh:
            json.dump({"task": task.model_dump(mode="json"),
                       "verbose": verbose.model_dump(mode="json")}, fh)
        answer = (getattr(task, "formatted_answer", None)
                  or getattr(task, "answer", None)
                  or "(no answer returned)")
        rec["fetched"] = now()
        out_dir = HERE / PHASE_DIRS.get(rec["phase"], f"phase{rec['phase']}")
        out_dir.mkdir(exist_ok=True)
        header = (
            "<!--\n"
            f"Edison Scientific {rec['job']} task (phase {rec['phase']})\n"
            f"- Task ID: {rec['task_id']}\n"
            f"- Submitted: {rec['submitted']}\n"
            f"- Fetched: {rec['fetched']} (status: {status})\n"
            f"- Raw trajectory JSON: ../raw/{name}.json.gz\n"
            "- Synthesis: ../README.md\n"
            "-->\n\n"
        )
        query = PHASES[rec["phase"]][name]["query"].strip()
        body = f"Question:\n\n{query}\n\n---\n\n{answer.strip()}\n"
        (out_dir / f"{name}.md").write_text(header + body)
        print(f"{name}: {status}, {len(answer)} chars -> {out_dir.name}/{name}.md",
              flush=True)
        save(records)
    save(records)


def status() -> None:
    c = client()
    records = load()
    st = poll(c, records, [n for n, r in records.items() if "fetched" not in r])
    print(json.dumps(st, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "submit":
        submit(int(sys.argv[2]))
    elif cmd == "wait":
        wait(int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 40.0)
    elif cmd == "fetch":
        fetch()
    elif cmd == "status":
        status()
