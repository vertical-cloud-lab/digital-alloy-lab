"""byu-vcl's ``vertical-lab`` (the Kardex Shuttle XP 500 model, the scene framework, the UR10e and the MiR250),
fetched at a pinned commit into ``.cache/`` and put on ``sys.path``, so this glovebox is drawn into the same VLM, in
the same style, as the rest of byu-vcl #303.

Pinned to the head of byu-vcl PR #318 (round 3 of #303). Nothing from it is committed here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
REPO = "https://github.com/vertical-cloud-lab/byu-vcl.git"
SHA = "903eef24ce8de52d7f1f216b929f5e54a89d29e8"       # byu-vcl PR #318 head, claude/issue-303-20261103-1736


def ensure() -> Path:
    dest = CACHE / f"byu-vcl-{SHA[:7]}"
    vl = dest / "vertical-lab"
    if not (vl / "scene.py").exists():
        dest.mkdir(parents=True, exist_ok=True)
        run = lambda *a: subprocess.run(["git", "-C", str(dest), *a], check=True)   # noqa: E731
        run("init", "-q")
        run("remote", "add", "origin", REPO) if not (dest / ".git" / "refs" / "remotes").exists() else None
        run("fetch", "-q", "--depth", "1", "origin", SHA)
        run("checkout", "-q", "FETCH_HEAD")
    for p in (vl, vl / "lab_models"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    return vl
