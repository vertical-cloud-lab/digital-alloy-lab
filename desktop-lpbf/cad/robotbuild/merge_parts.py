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


def main_keep(name, order):
    """Round 10: join the slices listed in `order` (their folder numbers <chapter>.part<k>, in play order) into <chapter>/,
    renumbering the frames 0, 1, 2, ... in that order, without touching the slice folders: frames hard-linked, each slice's
    audit folder copied as hard links to <chapter>/audit.part<i> (i its place in the order), audit_parts.json giving each its
    first and last frame in the joined chapter and own_first_frame, the frame number it was drawn with (a slice drawn again
    after the recording changed: the frames after it shift; scene_audit.py merge path@offset shifts its pairs' frames, and
    pairs_classify.py maps the frames back). Then move the slice folders out of the frames folder (they would be read again
    by scene_audit.py as unmerged slices)."""
    import os
    import subprocess
    parts = [common.FRAMES / f"{name}.part{k}" for k in order]
    missing = [p.name for p in parts if not (p / "done").exists()]
    if missing:
        sys.exit(f"{name}: slices missing or unfinished: {missing}")
    out = common.FRAMES / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    n = 0
    index = []
    with open(out / "meta.jsonl", "w") as meta:
        for i, p in enumerate(parts):
            pngs = sorted(p.glob("*.png"))
            lines = (p / "meta.jsonl").read_text().splitlines()
            if len(lines) != len(pngs):
                sys.exit(f"{p.name}: {len(pngs)} frames but {len(lines)} meta lines")
            own0 = int(pngs[0].stem) if pngs else n
            for j, f in enumerate(pngs):
                if int(f.stem) != own0 + j:
                    sys.exit(f"{p.name}: frame {f.name} where {own0 + j:05d} was expected")
            first = n
            for f in pngs:
                os.link(f, out / f"{n:05d}.png")
                n += 1
            meta.write("\n".join(lines) + "\n")
            rec = dict(part=i, slice_folder=p.name, first_frame=first, last_frame=n - 1, own_first_frame=own0, audit=None)
            if (p / "audit").is_dir():
                subprocess.run(["cp", "-al", str(p / "audit"), str(out / f"audit.part{i}")], check=True)
                rec["audit"] = f"audit.part{i}"
            if (p / "shots.json").exists():
                shutil.copy(str(p / "shots.json"), str(out / f"shots.part{i}.json"))
            index.append(rec)
    (out / "audit_parts.json").write_text(json.dumps(dict(
        note="Each slice of this chapter was rendered by its own process; audit_rec.py's stream for slice k is in its folder "
             "and starts afresh at first_frame. Round 10: own_first_frame is the frame number the slice was drawn with (it "
             "differs from first_frame for slices after one drawn again on a changed recording).", parts=index), indent=1))
    (out / "done").write_text(str(n))
    keep = common.FRAMES.parent / "slices_joined" / name
    keep.mkdir(parents=True, exist_ok=True)
    for p in parts:
        dst = keep / p.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(p), str(dst))
    print(f"{name}: {n} frames from {len(parts)} slices in the order {list(order)}; shifts "
          f"{[(r['slice_folder'], r['first_frame'] - r['own_first_frame']) for r in index]}; slice folders moved to {keep}")
    return index


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2].startswith("--order="):
        main_keep(sys.argv[1], [int(x) for x in sys.argv[2].split("=", 1)[1].split(",") if x])
    else:
        main(sys.argv[1])
