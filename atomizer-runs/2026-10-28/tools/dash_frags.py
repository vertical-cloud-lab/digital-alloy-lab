"""Fetch DASH fragments url&sq=N (2 s each from the broadcast start) through the SOCKS proxy, in parallel.
usage: dash_frags.py FMT.json FORMAT_ID OUTDIR FIRST LAST"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
info = json.load(open(sys.argv[1])); fid = sys.argv[2]; out = sys.argv[3]; a, b = int(sys.argv[4]), int(sys.argv[5])
f = [x for x in info["formats"] if x["format_id"] == fid][0]
url, hdr = f["url"], f.get("http_headers", {})
os.makedirs(out, exist_ok=True)
H = sum((["-H", f"{k}: {v}"] for k, v in hdr.items()), [])
def one(n):
    p = os.path.join(out, "%06d.mp4" % n)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return 0
    for k in range(6):
        d = subprocess.run(["curl", "-s", "-m", "90", "--proxy", "socks5h://127.0.0.1:1080", *H, url + "&sq=%d" % n],
                           capture_output=True).stdout
        if d and not d.startswith(b"<"):
            open(p, "wb").write(d); return len(d)
        time.sleep(1.5 * (k + 1))
    return -1
with ThreadPoolExecutor(5) as ex:
    sizes = list(ex.map(one, range(a, b + 1)))
print("fragments", len(sizes), "bad", [a + i for i, s in enumerate(sizes) if s < 0][:20], "MB", round(sum(s for s in sizes if s > 0) / 1e6, 1))
