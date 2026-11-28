"""Fetch the byu-vcl vertical-lab modules these animations build on, pinned to one commit (#262, PR #263).

    python vl_fetch.py            # -> vl/ (git-ignored), then checks every file's sha256 against VL_FILES

The scene, caption and encoding code (scene.py), the CAD helpers (lab_models/common.py), the Instrument/Joint model
(instruments.py), the registration of a model to real footage (register.py, frames.py), the render-slot guard
(runner_guard.py), and the instrument models we reuse (the lab's LECO PX500 polisher and MX400 mounting press, fitted
to the lab's own SOP videos; the Mitutoyo HM-220 micro-Vickers; the Nabertherm NAT 15/65 furnace; the Labconco fume
hood; the Keyence VHX-7000; the quench tank), come from vertical-cloud-lab/byu-vcl PR 318
(branch claude/issue-303-20261103-1736), at the commit below. Nothing is changed in them; what this folder adds lives
next to them, in its own modules.
"""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

COMMIT = "0425020724ad68c56e3183696ddc0c91ef696c6d"
BASE = f"https://raw.githubusercontent.com/vertical-cloud-lab/byu-vcl/{COMMIT}/vertical-lab/"
HERE = Path(__file__).resolve().parent
DEST = HERE / "vl"
FILES = ["scene.py", "lab_models/common.py", "instruments.py", "instruments_lab.py", "instruments_r7.py",
         "instruments_char.py", "r8_prep.py", "r8_specimens.py", "r8_char.py", "r8_test.py", "r8_store.py",
         "register.py", "frames.py", "runner_guard.py", "openflexure.py", "alloy_models.py", "lab_models/labware.py",
         "lab_models/equipment.py", "lab_models/vendor.py", "people.py", "props.py", "lab.py", "vlm.py"]


def main() -> None:
    DEST.mkdir(exist_ok=True)
    (DEST / "lab_models").mkdir(exist_ok=True)
    for f in FILES:
        dst = DEST / f
        if not dst.exists():
            with urllib.request.urlopen(BASE + f, timeout=60) as r:
                dst.write_bytes(r.read())
        print(f"{hashlib.sha256(dst.read_bytes()).hexdigest()[:16]}  {f}")


if __name__ == "__main__":
    main()
    sys.exit(0)
