"""Round 10 (2026-11-27): make <chapter>.part<new_k> from <chapter>.part<k>'s frames from global frame <f0> on (the slice's later
steps, unchanged), so that only the steps before f0 need drawing again. PNGs and meshes.pkl hard-linked; meta.jsonl lines
from f0 on; audit/frames.pkl starts with one record holding the full drawn state at f0 (the replay of every record up to it),
then the slice's own records after it, so scene_audit.py replays the same state from f0 on.

    /tmp/venv/bin/python split_part.py /tmp/robotbuild/frames/41-assembly-chamber.part4 9382 \
        /tmp/robotbuild/frames/41-assembly-chamber.part42      # round 10: F40-F51 kept when F39 was drawn again

Then merge_parts.py <chapter> --order=... with the new folder in its place (its frames keep their numbers; the join
renumbers them and audit_parts.json records the shift for scene_audit.py merge path@offset)."""
import os, pickle, shutil, sys
from pathlib import Path
src, f0, dst = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
pngs = sorted(src.glob("*.png"))
own0 = int(pngs[0].stem)
lines = (src / "meta.jsonl").read_text().splitlines()
assert len(lines) == len(pngs), (len(lines), len(pngs))
assert own0 <= f0 <= own0 + len(pngs) - 1
if dst.exists():
    shutil.rmtree(dst)
(dst / "audit").mkdir(parents=True)
keep = [p for p in pngs if int(p.stem) >= f0]
for p in keep:
    os.link(p, dst / p.name)
(dst / "meta.jsonl").write_text("\n".join(lines[f0 - own0:]) + "\n")
if (src / "shots.json").exists():
    shutil.copy(src / "shots.json", dst / "shots.json")
os.link(src / "audit" / "meshes.pkl", dst / "audit" / "meshes.pkl")
n0 = f0                                       # audit_rec numbers a record by its PNG frame number
state, wrote = {}, 0
with open(src / "audit" / "frames.pkl", "rb") as f, open(dst / "audit" / "frames.pkl", "wb") as g:
    first = True
    while True:
        try:
            r = pickle.load(f)
        except EOFError:
            break
        n = int(r["n"])
        if n <= n0:
            for a in r.get("removed", ()):
                state.pop(a, None)
            for a, v in r["changed"].items():
                state[a] = v
            if n == n0:
                pickle.dump(dict(n=n0, changed=dict(state), removed=[]), g)
                wrote += 1
            continue
        pickle.dump(r, g)
        wrote += 1
(dst / "done").write_text(str(len(keep)))
print(f"{dst.name}: frames {f0}..{int(keep[-1].stem)} ({len(keep)}), audit records {wrote}, first record {len(state)} actors")
