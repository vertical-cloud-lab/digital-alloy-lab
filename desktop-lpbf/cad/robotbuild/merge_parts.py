"""Join a chapter rendered in slices (asm_render.py with ASM_PART=k/n, or ASM_RANGE / ASM_STEPS with ASM_RANGE_IDX=k ->
<chapter>.part<k>/) into <chapter>/: the frames keep their global numbers, the slices' meta.jsonl are joined in order, and the
slice folders are removed.

Round 8: a slice rendered with ROBOTBUILD_AUDIT=1 has its own audit/ folder (audit_rec.py: what every drawn frame showed, a
stream that starts afresh in each slice). Those are kept: <chapter>.part<k>/audit/ moves to <chapter>/audit.part<k>/, and
<chapter>/audit_parts.json lists each slice's folder with its first and last frame, for scene_audit.py. Each slice's
shots.json (the camera rig's statistics) moves to <chapter>/shots.part<k>.json.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/merge_parts.py 41-assembly-chamber
"""
from __future__ import annotations

import json
import shutil
import sys

import common


def _k(p):
    s = p.name.rsplit("part", 1)[1]
    return int(s) if s.isdigit() else None


def main(name):
    parts = sorted((p for p in common.FRAMES.glob(f"{name}.part*") if _k(p) is not None), key=_k)
    if not parts or not all((p / "done").exists() for p in parts):
        sys.exit(f"{name}: slices missing or unfinished: {[p.name for p in parts]}")
    out = common.FRAMES / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    n = 0
    index = []
    with open(out / "meta.jsonl", "w") as meta:
        for p in parts:
            pngs = sorted(p.glob("*.png"))
            lines = (p / "meta.jsonl").read_text().splitlines()
            if len(lines) != len(pngs):
                sys.exit(f"{p.name}: {len(pngs)} frames but {len(lines)} meta lines")
            first = n
            for f in pngs:
                if int(f.stem) != n:
                    sys.exit(f"{p.name}: frame {f.name} where {n:05d} was expected")
                f.rename(out / f.name)
                n += 1
            meta.write("\n".join(lines) + "\n")
            k = _k(p)
            rec = dict(part=k, first_frame=first, last_frame=n - 1, audit=None)
            if (p / "audit").is_dir():
                shutil.move(str(p / "audit"), str(out / f"audit.part{k}"))
                rec["audit"] = f"audit.part{k}"
            if (p / "shots.json").exists():
                shutil.move(str(p / "shots.json"), str(out / f"shots.part{k}.json"))
            index.append(rec)
    (out / "audit_parts.json").write_text(json.dumps(dict(
        note="Each slice of this chapter was rendered by its own process; audit_rec.py's stream for slice k is in its folder "
             "and starts afresh at first_frame (frame numbers are the chapter's own).", parts=index), indent=1))
    (out / "done").write_text(str(n))
    for p in parts:
        shutil.rmtree(p)
    print(f"{name}: {n} frames from {len(parts)} slices; audit folders kept: {[r['audit'] for r in index]}")


if __name__ == "__main__":
    main(sys.argv[1])
