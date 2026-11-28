"""Submit, wait for and fetch the Edison queries behind the SOP animations (#262, PR #263).

    python edison_tasks.py submit            # submits every query in QUERIES that has no _task_id.json yet
    python edison_tasks.py wait              # blocks (one foreground call) until every task has finished
    python edison_tasks.py fetch             # writes answer.md, references.txt, task_verbose.json per query

Each query lives in edison/<key>/query.txt. The API key is read from EDISON_PLATFORM_API_KEY and never printed.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "edison"
DONE = {"success", "fail", "failed", "cancelled", "error"}


def client():
    from edison_client import EdisonClient
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def keys():
    return sorted(p.name for p in OUT.iterdir() if (p / "query.txt").exists())


def submit():
    from edison_client import JobNames
    c = client()
    for k in keys():
        tid = OUT / k / "_task_id.json"
        if tid.exists():
            print(k, "already submitted")
            continue
        q = (OUT / k / "query.txt").read_text()
        task_id = c.create_task({"name": JobNames.LITERATURE_HIGH, "query": q})
        tid.write_text(json.dumps({"task_id": str(task_id), "job": "LITERATURE_HIGH",
                                   "submitted_utc": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=2))
        print(k, "submitted", task_id)


def status_all(c):
    out = {}
    for k in keys():
        tid = OUT / k / "_task_id.json"
        if not tid.exists():
            continue
        t = c.get_task(task_id=json.loads(tid.read_text())["task_id"], lite=True)
        out[k] = str(getattr(t, "status", "?"))
    return out


def wait(max_min: float = 55.0):
    c = client()
    t0 = time.time()
    while True:
        st = status_all(c)
        print(time.strftime("%H:%M:%S"), st, flush=True)
        if all(s in DONE for s in st.values()) or time.time() - t0 > max_min * 60:
            return st
        time.sleep(120)


def _jsonable(o):
    try:
        return json.loads(o.model_dump_json())
    except Exception:
        return json.loads(json.dumps(o, default=str))


def fetch():
    c = client()
    for k in keys():
        tid = OUT / k / "_task_id.json"
        if not tid.exists():
            continue
        task_id = json.loads(tid.read_text())["task_id"]
        t = c.get_task(task_id=task_id, verbose=True)
        d = _jsonable(t)
        st = str(d.get("status"))
        print(k, st)
        if st != "success":
            continue
        (OUT / k / "task_verbose.json").write_text(json.dumps(d, indent=1, default=str))
        resp = (((d.get("environment_frame") or {}).get("state") or {}).get("state") or {}).get("response") or {}
        answer = resp.get("answer") or {}
        text = answer.get("formatted_answer") or answer.get("answer") or ""
        if not text:
            text = json.dumps(resp)[:20000]
        (OUT / k / "answer.md").write_text(text)
        refs = answer.get("references") or ""
        if not refs:
            m = re.search(r"\nReferences\n(.*)$", text, re.S)
            refs = m.group(1) if m else ""
        (OUT / k / "references.txt").write_text(refs)
        for name, body in sorted((answer.get("artifacts") or {}).items()):
            (OUT / k / f"{name}.md").write_text(f"<!-- Edison artifact key: {name} -->\n{body}")


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
