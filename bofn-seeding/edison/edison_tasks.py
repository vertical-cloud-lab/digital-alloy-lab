"""Submit, wait for and fetch the Edison Scientific tasks behind bofn-seeding (#275).

Each task lives in its own folder next to this script: ``<name>/query.txt`` holds the
query. ``submit`` writes ``<name>/_task_id.json``; ``fetch`` writes ``answer.md``,
``artifact-NN.md``, ``references.txt`` and the full ``task_verbose.json``.

    python bofn-seeding/edison/edison_tasks.py submit q1-seeding-strategy LITERATURE_HIGH
    python bofn-seeding/edison/edison_tasks.py submit q3-plan-critique ANALYSIS --upload plan.md
    python bofn-seeding/edison/edison_tasks.py wait q1-seeding-strategy q2-seed-alloys-and-data
    python bofn-seeding/edison/edison_tasks.py fetch q1-seeding-strategy

``wait`` blocks in the foreground (Python-side sleep) until every named task finishes or
``--max-minutes`` pass. Run it as one foreground call; never in the background (CLAUDE.md).
The API key is read from ``EDISON_PLATFORM_API_KEY`` and never printed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
DONE = {"success", "fail", "failed", "cancelled", "error"}


def client():
    from edison_client import EdisonClient

    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def submit(name: str, job: str, uploads: list[str]) -> None:
    from edison_client import JobNames, TaskRequest

    folder = HERE / name
    id_file = folder / "_task_id.json"
    if id_file.exists():
        sys.exit(f"{id_file} exists; not resubmitting")
    query = (folder / "query.txt").read_text(encoding="utf-8").strip()
    c = client()
    kwargs = {}
    if uploads:
        kwargs["files"] = [c.upload_file(str(p)) for p in uploads]
    task_id = c.create_task(TaskRequest(name=getattr(JobNames, job), query=query), **kwargs)
    record = {
        "task_id": str(task_id),
        "job": job,
        "submitted_utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if uploads:
        record["uploaded"] = [pathlib.Path(p).name for p in uploads]
    id_file.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(name, "submitted:", record["task_id"], job)


def task_id(name: str) -> str:
    return json.loads((HERE / name / "_task_id.json").read_text())["task_id"]


def wait(names: list[str], max_minutes: float, every: int) -> None:
    c = client()
    t0 = time.time()
    pending = list(names)
    while pending:
        for name in list(pending):
            status = str(c.get_task(task_id=task_id(name)).status)
            print(f"[{(time.time() - t0) / 60:5.1f} min] {name}: {status}", flush=True)
            if status in DONE:
                pending.remove(name)
        if not pending or time.time() - t0 > max_minutes * 60:
            break
        time.sleep(every)
    print("still pending:", pending or "none", flush=True)


def fetch(name: str) -> None:
    folder = HERE / name
    task = client().get_task(task_id=task_id(name), verbose=True)
    data = task.model_dump(mode="json") if hasattr(task, "model_dump") else dict(task)
    (folder / "task_verbose.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    status = data.get("status")
    try:
        answer = data["environment_frame"]["state"]["state"]["response"]["answer"]
    except (KeyError, TypeError):
        answer = None
    if not isinstance(answer, dict):
        print(name, "status:", status, "- no structured answer; saved task_verbose.json only")
        return
    text = answer.get("answer") or answer.get("formatted_answer") or ""
    (folder / "answer.md").write_text(text.rstrip() + "\n", encoding="utf-8")
    if answer.get("references"):
        (folder / "references.txt").write_text(answer["references"].rstrip() + "\n", encoding="utf-8")
    for key, body in sorted((answer.get("artifacts") or {}).items()):
        (folder / f"{key}.md").write_text(f"<!-- Edison artifact key: {key} -->\n{body}".rstrip() + "\n", encoding="utf-8")
    print(name, "status:", status, "answer chars:", len(text), "artifacts:", len(answer.get("artifacts") or {}))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("submit")
    s.add_argument("name")
    s.add_argument("job", choices=["LITERATURE", "LITERATURE_HIGH", "ANALYSIS", "PRECEDENT"])
    s.add_argument("--upload", nargs="*", default=[])
    w = sub.add_parser("wait")
    w.add_argument("names", nargs="+")
    w.add_argument("--max-minutes", type=float, default=50)
    w.add_argument("--every", type=int, default=120)
    f = sub.add_parser("fetch")
    f.add_argument("names", nargs="+")
    a = p.parse_args()
    if a.cmd == "submit":
        submit(a.name, a.job, a.upload)
    elif a.cmd == "wait":
        wait(a.names, a.max_minutes, a.every)
    else:
        for n in a.names:
            fetch(n)


if __name__ == "__main__":
    main()
