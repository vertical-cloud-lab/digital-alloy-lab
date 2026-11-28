"""Camera gate on a finished MP4: how often the picture cuts and how much the camera moves (round 8, PR #266).

Sterling, 2026-11-26, on the round-7 robot-build video: "moonwalk, motion sickness, collisions and interference, dummy tool
paths instead of real ones". The renderers have their own gates on what they draw (camera_rig.py, scene_audit.py, walk.py,
gcode_sim.py). This one looks only at the pixels of the final file, so it also measures the old video, whose frames are gone,
and it cannot be fooled by a renderer's own metadata.

What it measures, on the video scaled to 320 x 180 grey, inside the picture area only (the caption bar, the clocks and the
right-hand panels are masked out):
  jumps           a frame whose masked picture differs from the last one by more than CUT_MAD grey levels on average AND whose
                  tracked corners mostly fail to follow: a cut, or a change too large to follow by eye (a whip pan, a
                  time-lapsed arm filling the frame). Consecutive jump frames count as one jump; the stretch between two
                  jumps is a "steady run" (a shot)
  camera motion   corners tracked from each frame to the next (Shi-Tomasi + pyramidal Lucas-Kanade), a similarity transform
                  fitted to them with RANSAC: its translation is the background's shift. With a fixed camera the background
                  corners don't move, so the fitted shift is ~0 even while arms move in front of it. Reported as frame-widths
                  per second; a frame "moves" above MOVE_FW_S.
Per chapter (from a YouTube-style chapters.txt) and overall: jumps per minute, the share of frames that are jump frames, steady
runs (median, share under 2 s), the share of frames in which the camera moves, the mean and 95th-percentile camera speed.

Limits (set here; the last is the cinematographers' 7-second panning rule, the rest are this project's choices): at most 10
jumps a minute in a chapter, at most 3 % of frames jumping, a median steady run of at least 4 s, no more than 15 % of steady
runs under 2 s (where a chapter has six or more jumps), and a 95th-percentile camera speed of at most 1/7 of the frame width
per second (a point takes at least 7 s to cross the picture). The share of frames in which the camera moves at all is
reported but not limited: a slow drift is fine.
Title cards and 2-D chart chapters pass trivially.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/video_qa.py VIDEO.mp4 [--chapters chapters.txt] [--out out.json] [--tag old]

Needs ffmpeg on PATH or FFMPEG=<path> (imageio-ffmpeg's binary works).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

W, H = 320, 180
CUT_MAD = 18.0            # mean absolute grey-level change of the masked picture that can be a cut
CUT_TRACK = 0.35          # ... if fewer than this share of corners can be followed across it
MOVE_FW_S = 0.02          # camera counts as moving above this many frame-widths per second
LIMITS = dict(jumps_per_min=10.0, jump_frame_share=0.03, median_run_s=4.0, short_run_share=0.15, p95_speed_fw_s=round(1 / 7, 3))
# picture area: below the caption bar, above the progress bar, left of the right-hand panels
X0, X1, Y0, Y1 = int(0.03 * W), int(0.74 * W), int(0.09 * H), int(0.80 * H)


def ffmpeg():
    f = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not f:
        import imageio_ffmpeg
        f = imageio_ffmpeg.get_ffmpeg_exe()
    return f


def probe_fps(path):
    out = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)], capture_output=True, text=True).stderr
    for tok in out.split(","):
        tok = tok.strip()
        if tok.endswith(" fps"):
            return float(tok.split()[0])
    return 12.0


def frames(path):
    p = subprocess.Popen([ffmpeg(), "-v", "error", "-i", str(path), "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         stdout=subprocess.PIPE)
    n = W * H
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W)
    p.wait()


def read_chapters(path, total_s):
    ch = []
    if path and Path(path).exists():
        for line in Path(path).read_text().splitlines():
            line = line.strip()
            if not line or not line[0].isdigit():
                continue
            t, _, title = line.partition(" ")
            parts = [int(x) for x in t.split(":")]
            s = sum(v * 60 ** i for i, v in enumerate(reversed(parts)))
            ch.append([s, title])
    if not ch:
        ch = [[0, "whole video"]]
    return [(s, (ch[i + 1][0] if i + 1 < len(ch) else total_s), title) for i, (s, title) in enumerate(ch)]


def exact_chapters(compose_json, total_s):
    """Round 9: chapter windows from compose.json's exact frame counts. chapters.txt rounds each start to the nearest whole
    second, so a window could begin up to 0.5 s early and count the previous chapter's last fraction of a second as a short run
    (chapter 30's 0.5 s run in round 9's first check was 318.5 s rounded to 5:18)."""
    d = json.loads(Path(compose_json).read_text())
    fps = d.get("fps", 12)
    yt = [(sum(int(v) * 60 ** i for i, v in enumerate(reversed(c["at"].split(":")))), c["title"]) for c in d["youtube_chapters"]]
    starts, t, k = [], 0.0, 0
    for c in d["chapters"]:
        if k < len(yt) and abs(t - yt[k][0]) <= 1.0:
            starts.append((t, yt[k][1])); k += 1
        t += c["frames"] / fps
    return [(s0, (starts[i + 1][0] if i + 1 < len(starts) else total_s), title) for i, (s0, title) in enumerate(starts)]


def measure(path):
    import cv2
    fps = probe_fps(path)
    lk = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.03))
    prev = None
    mad, shift, track = [], [], []
    for g in frames(path):
        roi = g[Y0:Y1, X0:X1]
        if prev is None:
            prev = roi
            mad.append(0.0)
            shift.append(0.0)
            track.append(1.0)
            continue
        mad.append(float(np.mean(np.abs(roi.astype(np.int16) - prev.astype(np.int16)))))
        p0 = cv2.goodFeaturesToTrack(prev, maxCorners=160, qualityLevel=0.01, minDistance=6)
        sh, tr = 0.0, 1.0
        if p0 is not None and len(p0) >= 8:
            p1, st, err = cv2.calcOpticalFlowPyrLK(prev, roi, p0, None, **lk)
            ok = (st.ravel() == 1) & (err.ravel() < 12.0)
            tr = float(ok.mean())
            if ok.sum() >= 8:
                M, inl = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=1.0)
                if M is not None and inl is not None and inl.sum() >= 6:
                    # shift of the picture centre under the fitted similarity (pan and tilt, plus zoom and roll about the centre)
                    c = np.array([(X1 - X0) / 2.0, (Y1 - Y0) / 2.0, 1.0])
                    d = M @ c - c[:2]
                    zoom = abs(float(np.hypot(M[0, 0], M[1, 0])) - 1.0) * (X1 - X0) / 2.0     # edge shift from zoom, px
                    sh = float(np.hypot(*d)) + zoom
        shift.append(sh)
        track.append(tr)
        prev = roi
    mad, shift, track = np.array(mad), np.array(shift), np.array(track)
    cut = (mad > CUT_MAD) & (track < CUT_TRACK)
    cut[0] = False
    speed = shift / W * fps                      # frame-widths per second
    speed[cut] = 0.0
    return dict(fps=fps, n=len(mad), cut=cut, speed=speed)


def stats(m, a, b):
    fps = m["fps"]
    i0, i1 = int(round(a * fps)), min(int(round(b * fps)), m["n"])
    if i1 - i0 < 2:
        return None
    cut, speed = m["cut"][i0:i1], m["speed"][i0:i1]
    # consecutive jump frames are one jump; the steady runs are what lies between them
    starts = np.flatnonzero(cut & ~np.r_[False, cut[:-1]])
    steady = ~cut
    edges = np.flatnonzero(np.diff(np.r_[0, steady.astype(np.int8), 0]))
    runs = (edges[1::2] - edges[0::2]) / fps
    if len(runs) == 0:
        runs = np.array([0.0])
    dur = (i1 - i0) / fps
    out = dict(seconds=round(dur, 1), jumps=int(len(starts)), jumps_per_min=round(len(starts) / dur * 60.0, 1),
               jump_frame_share=round(float(cut.mean()), 3),
               median_run_s=round(float(np.median(runs)), 1), min_run_s=round(float(runs.min()), 2),
               short_run_share=round(float(np.mean(runs < 2.0)), 3),
               moving_share=round(float(np.mean(speed > MOVE_FW_S)), 3),
               mean_speed_fw_s=round(float(speed.mean()), 4), p95_speed_fw_s=round(float(np.percentile(speed, 95)), 3))
    fails = []
    if out["jumps_per_min"] > LIMITS["jumps_per_min"]:
        fails.append("jumps_per_min")
    if out["jump_frame_share"] > LIMITS["jump_frame_share"]:
        fails.append("jump_frame_share")
    if out["median_run_s"] < LIMITS["median_run_s"] and out["jumps"] > 1:
        fails.append("median_run_s")
    if out["short_run_share"] > LIMITS["short_run_share"] and out["jumps"] >= 6:
        fails.append("short_run_share")
    if out["p95_speed_fw_s"] > LIMITS["p95_speed_fw_s"]:
        fails.append("p95_speed_fw_s")
    out["fails"] = fails
    out["pass"] = not fails
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--chapters", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--compose-json", default="", help="exact chapter starts from compose.json's frame counts (round 9)")
    a = ap.parse_args(argv)
    m = measure(a.video)
    total = m["n"] / m["fps"]
    rows = []
    windows = exact_chapters(a.compose_json, total) if a.compose_json else read_chapters(a.chapters, total)
    for s, e, title in windows:
        st = stats(m, s, e)
        if st:
            rows.append(dict(chapter=title, start_s=s, **st))
    overall = stats(m, 0.0, total)
    res = dict(video=str(a.video), tag=a.tag, fps=m["fps"], frames=m["n"], seconds=round(total, 1), limits=LIMITS,
               method="320x180 grey, picture area only; jump = large change with lost corner tracks (a cut or a change too large "
                      "to follow), consecutive jump frames merged; camera speed = shift of the RANSAC similarity fitted to tracked "
                      "corners, in frame-widths per second",
               overall=overall, chapters=rows)
    print(f"{a.video}: {m['n']} frames, {total:.0f} s")
    print(f"{'chapter':50s} {'s':>6s} {'jumps/min':>9s} {'jump fr':>7s} {'med run':>8s} {'<2 s':>6s} {'moving':>7s} {'p95 fw/s':>8s}  result")
    for r in rows + [dict(chapter="OVERALL", **overall)]:
        print(f"{r['chapter'][:50]:50s} {r['seconds']:6.0f} {r['jumps_per_min']:9.1f} {100 * r['jump_frame_share']:6.1f}% "
              f"{r['median_run_s']:8.1f} {100 * r['short_run_share']:5.0f}% {100 * r['moving_share']:6.0f}% {r['p95_speed_fw_s']:8.3f}  "
              f"{'pass' if r['pass'] else 'FAIL: ' + ', '.join(r['fails'])}")
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
