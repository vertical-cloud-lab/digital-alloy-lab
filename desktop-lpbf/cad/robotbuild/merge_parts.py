"""Join a chapter rendered in slices (asm_render.py with ASM_PART=k/n -> <chapter>.part<k>/) into <chapter>/: the frames
keep their global numbers, the slices' meta.jsonl are joined in order, and the slice folders are removed.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/merge_parts.py 41-assembly-chamber
"""
from __future__ import annotations

import shutil
import sys

import common


def main(name):
    parts = sorted(common.FRAMES.glob(f"{name}.part*"), key=lambda p: int(p.name.rsplit("part", 1)[1]))
    if not parts or not all((p / "done").exists() for p in parts):
        sys.exit(f"{name}: slices missing or unfinished: {[p.name for p in parts]}")
    out = common.FRAMES / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    n = 0
    with open(out / "meta.jsonl", "w") as meta:
        for p in parts:
            pngs = sorted(p.glob("*.png"))
            lines = (p / "meta.jsonl").read_text().splitlines()
            if len(lines) != len(pngs):
                sys.exit(f"{p.name}: {len(pngs)} frames but {len(lines)} meta lines")
            for f in pngs:
                if int(f.stem) != n:
                    sys.exit(f"{p.name}: frame {f.name} where {n:05d} was expected")
                f.rename(out / f.name)
                n += 1
            meta.write("\n".join(lines) + "\n")
    (out / "done").write_text(str(n))
    for p in parts:
        shutil.rmtree(p)
    print(f"{name}: {n} frames from {len(parts)} slices")


if __name__ == "__main__":
    main(sys.argv[1])
