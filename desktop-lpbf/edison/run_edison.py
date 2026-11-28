"""Submit, wait for and fetch the Edison tasks kept in folders under desktop-lpbf/edison/.

Each folder holds a query.txt. `submit` writes _task_id.json; `fetch` writes the full trajectory
(task_verbose.json), the formatted answer (answer.md), the reference list (references.txt) and any
artifacts (artifact-NN.md).

    python desktop-lpbf/edison/run_edison.py submit <folder> LITERATURE|LITERATURE_HIGH
    python desktop-lpbf/edison/run_edison.py wait <folder> [<folder> ...] [--max-minutes 45]
    python desktop-lpbf/edison/run_edison.py fetch <folder>

`wait` blocks in Python (time.sleep), polls every 2 min, fetches each task as it finishes and
returns when all are done or the time limit is reached. Run it as one foreground call.
The API key is read from EDISON_PLATFORM_API_KEY and never printed.
"""

import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

from edison_client import EdisonClient, JobNames

HERE = Path(__file__).resolve().parent
DONE = {"success", "fail", "failed", "cancelled", "error"}


def client():
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def folder(name):
    path = HERE / name
    if not (path / "query.txt").exists():
        sys.exit(f"{path}/query.txt not found")
    return path


def submit(name, job):
    path = folder(name)
    query = (path / "query.txt").read_text().strip()
    task_id = client().create_task({"name": getattr(JobNames, job), "query": query})
    record = {"task_id": task_id, "job": job, "submitted_utc": dt.datetime.now(dt.UTC).isoformat()}
    (path / "_task_id.json").write_text(json.dumps(record, indent=2) + "\n")
    print(name, job, task_id)


def status(c, task_id):
    return str(c.get_task(task_id=task_id).status)


def fetch(name, c=None):
    c = c or client()
    path = folder(name)
    task_id = json.loads((path / "_task_id.json").read_text())["task_id"]
    task = c.get_task(task_id=task_id, verbose=True)
    data = task.model_dump(mode="json") if hasattr(task, "model_dump") else dict(task)
    (path / "task_verbose.json").write_text(json.dumps(data, indent=1) + "\n")
    answer = (((data.get("environment_frame") or {}).get("state") or {}).get("state") or {})
    answer = ((answer.get("response") or {}).get("answer")) or {}
    (path / "answer.md").write_text((answer.get("formatted_answer") or answer.get("answer") or "") + "\n")
    (path / "references.txt").write_text((answer.get("references") or "") + "\n")
    for key, text in sorted((answer.get("artifacts") or {}).items()):
        (path / f"{key}.md").write_text(str(text) + "\n")
    print(name, "fetched:", data.get("status"), len(answer.get("formatted_answer") or ""), "chars")


def wait(names, max_minutes):
    c = client()
    ids = {n: json.loads((folder(n) / "_task_id.json").read_text())["task_id"] for n in names}
    pending = set(names)
    deadline = time.time() + 60 * max_minutes
    while pending:
        for name in sorted(pending):
            s = status(c, ids[name])
            print(dt.datetime.now(dt.UTC).strftime("%H:%M:%S"), name, s, flush=True)
            if s in DONE:
                fetch(name, c)
                pending.discard(name)
        if not pending or time.time() > deadline:
            break
        time.sleep(120)
    print("still pending:", sorted(pending) or "none", flush=True)


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    if cmd == "submit":
        submit(rest[0], rest[1])
    elif cmd == "fetch":
        fetch(rest[0])
    elif cmd == "wait":
        limit = 45.0
        if "--max-minutes" in rest:
            i = rest.index("--max-minutes")
            limit = float(rest[i + 1])
            rest = rest[:i] + rest[i + 2 :]
        wait(rest, limit)
    else:
        sys.exit(__doc__)
