"""Fetch a time window of a YouTube archive's HLS stream through a SOCKS proxy, segments in parallel.
usage: hls_window_par.py VIDEO_ID FORMAT START_S END_S OUT.ts
Prints t0 (archive time of the first byte)."""
import subprocess, sys, os, tempfile
from concurrent.futures import ThreadPoolExecutor
vid, fmt, a, b, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
PROXY = "socks5h://127.0.0.1:1080"
import time
def curl(url, tries=6):
    for k in range(tries):
        d = subprocess.run(["curl", "-s", "-m", "120", "--retry", "3", "--proxy", PROXY, url], capture_output=True).stdout
        if d:
            return d
        time.sleep(1.5 * (k + 1))
    return d
m3u8 = subprocess.run(["yt-dlp", "--proxy", PROXY, "--js-runtimes", "node", "--no-warnings", "-f", fmt, "-g",
                       "https://www.youtube.com/watch?v=" + vid], capture_output=True, text=True, check=True).stdout.split()[0]
pl = curl(m3u8).decode()
t, segs, dur = 0.0, [], None
for line in pl.splitlines():
    if line.startswith("#EXTINF:"):
        dur = float(line.split(":")[1].split(",")[0])
    elif line.startswith("http") and dur is not None:
        if t + dur > a and t < b:
            segs.append((t, line))
        t += dur; dur = None
print("playlist %.0f s; %d segments; t0 %.2f" % (t, len(segs), segs[0][0] if segs else -1), flush=True)
with ThreadPoolExecutor(4) as ex:
    datas = list(ex.map(lambda s: curl(s[1]), segs))
with open(out, "wb") as f:
    for d in datas:
        f.write(d)
print("bytes", sum(len(d) for d in datas), "empty", sum(1 for d in datas if not d))
print("t0", segs[0][0] if segs else None)
