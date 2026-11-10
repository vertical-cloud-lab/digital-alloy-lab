"""Compare kept quick-path outputs (check_quick_paths.py --keep) with the committed files:
sha256 equality, PNG pixel RMS (same formula as tests/check_quick_paths.py), JSON diff of leaves."""
import glob, hashlib, json, os, sys
import numpy as np
from matplotlib import image
ROOT = sys.argv[1]
cfg = {k: v for k, v in json.load(open(os.path.join(ROOT, "tests", "examples.json"))).items() if not k.startswith("_")}
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rms(a, b):
    x, y = image.imread(a), image.imread(b)
    if x.shape != y.shape: return float("inf"), x.shape, y.shape
    return float(np.sqrt(np.mean((x.astype(float) - y.astype(float)) ** 2)) * 255), x.shape, y.shape
def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from leaves(v, f"{p}[{i}]")
    else: yield p, o
rows = []
for name, c in cfg.items():
    dirs = sorted(glob.glob(f"/tmp/orchid-{name}-*"), key=os.path.getmtime)
    if not dirs: print("no kept dir for", name); continue
    out = dirs[-1]
    for f, ref in c["outputs"].items():
        got, want = os.path.join(out, f), os.path.join(ROOT, name, ref)
        same = sha(got) == sha(want)
        line = f"{name}/{f}: {'identical' if same else 'DIFFERS'} size got={os.path.getsize(got)} want={os.path.getsize(want)}"
        if f.endswith(".png") and not same:
            d, s1, s2 = rms(got, want); line += f" pixel RMS={d:.3f} shape={s1} vs {s2}"
        if f.endswith(".json") and not same:
            a, b = dict(leaves(json.load(open(got)))), dict(leaves(json.load(open(want))))
            diffs = [(k, b.get(k), a.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
            line += f" json leaves differing={len(diffs)}"
            for k, w, g in diffs[:15]: line += f"\n      {k}: committed={w!r} regenerated={g!r}"
        if f.endswith(".pdf") and not same:
            import subprocess
            line += f" (cmp: {subprocess.run(['cmp', '-l', got, want], capture_output=True, text=True).stdout.count(chr(10))} bytes differ)"
        print(line)
