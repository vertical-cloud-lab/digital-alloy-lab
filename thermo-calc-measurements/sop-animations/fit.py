"""Register our instrument models to frames of the real machines: byu-vcl's register.py, pointed at this folder.

    python fit.py solve dsc_sta                    # fit cameras (+ FREE dimensions) to refs/dsc_sta/*.json -> fit.json
    xvfb-run -a python fit.py draw dsc_sta         # overlays -> out/register/dsc_sta/<view>.jpg
    FRAMES_SOCKS=127.0.0.1:1080 python vl/frames.py storyboard VIDEO_ID   # contact sheets of a YouTube video
    FRAMES_SOCKS=127.0.0.1:1080 python vl/frames.py grab VIDEO_ID 12 31.5 # single 1280x720 frames
    python vl/frames.py grid IMAGE [STEP]          # a copy with labelled pixel lines, to read picks off

A view is refs/<key>/<name>.json next to its frame refs/<key>/<name>.jpg (see vl/register.py's docstring for the
format: "source", optional "video"/"t", "pose", "points", "curves", "lines", "holdout"). Frames from makers' and
others' videos and photos are not committed (.gitignore); their "source" (and "video"/"t") let them be fetched again.
A model publishes its anchors with ANCHORS[key] = (params, fn(params, pose)), FREE[key] and CHECKS[key] in its
models_*.py module, exactly as byu-vcl's instruments do.
"""
from __future__ import annotations

import json
import sys

import stage

import register  # noqa: E402  (vl/ is on the path once stage is imported)

stage._collect_materials()
register.HERE = stage.HERE
register.REFS = stage.HERE / "refs"
register.OUT = stage.OUT / "register"
register.MODULES = [f.stem for f in sorted(stage.HERE.glob("models_*.py"))]
sys.modules["tour"] = stage              # register.build() uses tour.MATS and tour.piece_entries

if __name__ == "__main__":
    cmd, keys = sys.argv[1], sys.argv[2:]
    for key in keys:
        if cmd == "solve":
            res = register.solve(key)
            print(json.dumps({k: res[k] for k in ("free", "start", "params", "lenses") if k in res}, indent=1))
            for n, v in res["views"].items():
                tag = " (held out of the fit)" if v.get("holdout") else ""
                print(f"{n}{tag}: rms {v['rms_px_camera_only']} -> {v['rms_px']} px, f {v['focal_px']} "
                      f"(HFOV {v['hfov_deg']} deg), k1 {v['k1']}")
                worst = sorted(v["residual_px"].items(), key=lambda kv: -kv[1])[:6]
                print("   worst:", ", ".join(f"{a} {b}" for a, b in worst))
        elif cmd == "draw":
            for p in register.draw(key):
                print(p)
        else:
            raise SystemExit(f"unknown command {cmd!r}")
