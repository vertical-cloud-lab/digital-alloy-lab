"""Fetch results for the 4 LITERATURE_HIGH scan-parameter queries and
save them as markdown under edison-trajectories/results/scanparams/.
"""
import json
import os
import pathlib
import sys

from edison_client import EdisonClient

REPO = pathlib.Path("/workspaces/digital-alloy-lab-private")
MANIFEST = REPO / "edison-trajectories" / "scripts" / "results" / "scanparams_task_ids.json"
OUT_DIR = REPO / "edison-trajectories" / "results" / "scanparams"
OUT_DIR.mkdir(parents=True, exist_ok=True)

client = EdisonClient(api_key=os.environ["EDISON_API_KEY"])
manifest = json.loads(MANIFEST.read_text())

for row in manifest:
    slug = row["slug"]
    task_id = row["task_id"]
    title = row["title"]
    print(f"[{slug}] fetching {task_id} ...", flush=True)
    task = client.get_task(task_id=task_id)
    status = getattr(task, "status", None)
    print(f"  status={status}")
    answer = getattr(task, "answer", None)
    # Persist raw task dump for debugging regardless of status.
    try:
        raw = task.model_dump() if hasattr(task, "model_dump") else task.__dict__
    except Exception:
        raw = {"repr": repr(task)}
    (OUT_DIR / f"{slug}.raw.json").write_text(json.dumps(raw, indent=2, default=str))
    if answer:
        md = f"# {title}\n\n_Edison task_id: `{task_id}`  \n_status: {status}_\n\n---\n\n{answer}\n"
        (OUT_DIR / f"{slug}.md").write_text(md)
        print(f"  wrote {OUT_DIR / f'{slug}.md'}")
    else:
        print(f"  NO answer field; see {slug}.raw.json", file=sys.stderr)

print("\nDone.")
