"""Join the robot-built desktop LPBF video's chapters into one MP4, drawing every on-screen panel (panels.py) over the raw
3-D frames that the chapter renderers wrote (common.Chapter: /tmp/robotbuild/frames/<NN-chapter>/<00000>.png plus one
line of meta.jsonl per frame).

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/compose.py                # every finished chapter -> the MP4
    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/compose.py --partial      # also chapters still rendering
    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/compose.py --only 10-parts --out /tmp/robotbuild/parts.mp4

Chapters are taken in folder-name order. A chapter is used when its folder has a `done` file (common.Chapter.close
writes it); with --partial, a chapter that is still rendering is used up to its last complete frame. Every chapter in
the contract (README.md) that has no frames gets a 3 s title card saying it was not rendered in this cut.

What it writes (default: desktop-lpbf/cad/img/robotbuild/):
  robot-build.mp4     H.264, yuv420p, 12 fps, CRF 28 with a bit-rate cap that keeps the file under 95 MB, +faststart.
                      Frames are streamed into ffmpeg one at a time (never all held in memory).
  chapters.txt        the YouTube chapter list, from changes in the frames' "chapter" (each chapter at least 10 s).
  contact-sheet.jpg   four frames of each chapter.
  compose.json        what went in: chapters, frames, seconds, the counters' end values, missing chapters.
  still-*.png         with --stills: chosen frames, each under 400 kB.

The clocks: project time is the sum of every frame's proc_s (shown as 8 h working days); the machine, robot, person and
CAM hours and the outsourced days are the sums of the frames' "add" increments. A chapter none of whose frames has
"add" is counted from "who" instead (each robot, person or machine named counts the frame's proc_s).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402
import panels as P  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

FPS = common.FPS
W, H = common.W, common.H
OUT = common.LPBF / "cad" / "img" / "robotbuild"
MAX_MB = 95.0
EXPECTED = [  # the contract's chapters (README.md), with the title a missing one's card shows
    ("00-intro", "The hall: two mobile manipulators, one long table"),
    ("10-parts", "The parts: cost and lead time"),
    ("20-receiving", "Receiving"),
    ("30-machining-chamber", "Machining the chamber"),
    ("31-machining-parts", "Machining the other parts"),
    ("32-finishing", "Welding, honing, deburring, washing, measuring"),
    ("40-assembly-module", "Assembling the build module"),
    ("41-assembly-chamber", "Assembling the chamber and the process module"),
    ("50-integration", "Onto the VLM tray: rack, gas module, hoses, leak check"),
    ("60-summary", "Time and cost: in-house, outsourced, robot shop"),
]
COUNTERS = ("machine_h", "robot_h", "person_h", "cam_h", "outsourced_d")
CARD_S = 3.0
TITLE_S = 2.6


# ------------------------------------------------------------------------------------------------ pass 1: what's there
def scan(partial=False, only=None):
    names = {n for n, _ in EXPECTED}
    if common.FRAMES.exists():
        names |= {p.name for p in common.FRAMES.iterdir() if p.is_dir() and p.name[:2].isdigit()}
    if only:
        names = {n for n in names if n in only}
    titles = dict(EXPECTED)
    chapters = []
    for name in sorted(names):
        d = common.FRAMES / name
        done = (d / "done").exists()
        meta = []
        if d.exists() and (done or partial) and (d / "meta.jsonl").exists():
            for line in (d / "meta.jsonl").read_text().splitlines():
                try:
                    meta.append(json.loads(line))
                except json.JSONDecodeError:
                    break                                    # a line still being written
            n = len(meta)
            while n and not (d / f"{n - 1:05d}.png").exists():
                n -= 1
            meta = meta[:n]
        if meta:
            chapters.append(dict(name=name, dir=d, meta=meta, done=done, card=None))
        else:
            state = "still rendering" if d.exists() and any(d.glob("*.png")) else "not rendered"
            t = titles.get(name, name)
            card = dict(title=t, lines=[f"This chapter ({name}) was {state} when this cut was made."],
                        note="Robot-built desktop LPBF (issue #260, PR #266)")
            n = int(CARD_S * FPS)
            meta = [dict(caption=t, sub=f"{name}: {state} in this cut", chapter=t, proc_s=0.0) for _ in range(n)]
            chapters.append(dict(name=name, dir=None, meta=meta, done=False, card=card, state=state))
    return chapters


def counters(chapters):
    """Per frame, the running clocks (cumulative), and the YouTube chapter list."""
    run = dict(t_s=0.0, **{k: 0.0 for k in COUNTERS})
    for ch in chapters:
        has_add = any("add" in m for m in ch["meta"])
        states = []
        for m in ch["meta"]:
            ps = float(m.get("proc_s", 1.0 / FPS) or 0.0)
            run["t_s"] += ps
            if has_add:
                for k, v in (m.get("add") or {}).items():
                    if k in run:
                        run[k] += float(v)
            else:
                who = m.get("who") or []
                run["robot_h"] += ps / 3600.0 * sum(1 for w in who if w.startswith("robot"))
                run["person_h"] += ps / 3600.0 * (1 if "person" in who else 0)
                run["machine_h"] += ps / 3600.0 * (1 if "machine" in who else 0)
                run["outsourced_d"] += ps / 86400.0 * (1 if "outsourced" in who else 0)
            states.append(dict(run))
        ch["clock"] = states
    return run


def chapter_list(chapters, min_s=10.0):
    """[(start_frame, title)] from changes in the frames' "chapter"; entries under min_s join the one before."""
    marks, k, prev = [], 0, None
    for ch in chapters:
        for m in ch["meta"]:
            t = m.get("chapter") or ch["name"]
            if t != prev:
                marks.append([k, t])
                prev = t
            k += 1
    total = k
    out = []
    for i, (f0, t) in enumerate(marks):
        f1 = marks[i + 1][0] if i + 1 < len(marks) else total
        if out and (f1 - f0) / FPS < min_s:
            continue                                     # too short: the one before runs on
        if out and out[-1][1] == t:
            continue
        out.append([f0, t])
    # the first must start at 0:00; a too-short first entry is dropped into the next
    if out:
        out[0][0] = 0
    while len(out) > 1 and (out[1][0] - out[0][0]) / FPS < min_s:
        out.pop(0)
        out[0][0] = 0
    return out, total


def stamp(frames):
    s = int(round(frames / FPS))
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


# ------------------------------------------------------------------------------------------------ pass 2: the frames
def lead_rows(hud):
    rows = []
    for r in (hud or {}).get("lead", []):
        rows.append(dict(name=r["name"], new=r.get("new"), used=r.get("used"), long=bool(r.get("long"))))
    rows.sort(key=lambda r: -(P.lo_hi(r["new"]) or (0, 0))[1])
    return rows


def load_hud():
    """The lead-time rows the lead panel draws: data/hud_panel.json (written by ch_parts.py from the data worker's
    hud.json, or from bom.csv until that exists)."""
    for p in (common.DATA / "hud_panel.json",):
        if p.exists():
            try:
                return json.loads(p.read_text())
            except json.JSONDecodeError:
                pass
    return {}


def overlay(base, m, clock, frac, ticks, ch_title, ch_alpha, cost_scale, rows):
    img = base.convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay, "RGBA")
    P.caption_bar(d, m.get("caption", ""), m.get("sub", ""), m.get("who"), m.get("status", ""), step=m.get("step", ""))
    y = 72
    if m.get("cost"):
        y = P.cost_panel(d, m["cost"], cost_scale) + 8
    if m.get("chart"):
        y = P.chart_panel(d, m["chart"], y0=y) + 8
    if m.get("lead"):
        lr = m["lead"].get("rows") or rows
        P.lead_panel(d, lr, m["lead"].get("highlight"), y0=y)
    P.labels(d, m.get("labels"))
    if not m.get("no_clock"):
        P.clocks(d, clock)
    P.chapter_title(d, ch_title, ch_alpha)
    P.progress(d, frac, ticks)
    img.alpha_composite(lay)
    return img.convert("RGB")


def encoder(path, crf, maxrate_k):
    path.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
         "-maxrate", f"{maxrate_k}k", "-bufsize", f"{2 * maxrate_k}k", "-pix_fmt", "yuv420p", "-threads", "2",
         "-movflags", "+faststart", str(path)], stdin=subprocess.PIPE)


def small_png(im, path, limit=400_000):
    """Save a still under `limit` bytes: full size first, then fewer colours, then smaller."""
    im = im.convert("RGB")
    for colors, scale in ((None, 1.0), (256, 1.0), (192, 1.0), (256, 0.75), (160, 0.75), (128, 0.6)):
        x = im if scale == 1.0 else im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
        if colors:
            x = x.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        x.save(path, optimize=True)
        if path.stat().st_size <= limit:
            return path
    return path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT / "robot-build.mp4"))
    ap.add_argument("--partial", action="store_true", help="also use chapters that are still rendering")
    ap.add_argument("--only", default="", help="comma-separated chapter folders")
    ap.add_argument("--crf", type=int, default=28)
    ap.add_argument("--stills", default="", help="comma-separated chapter:fraction, e.g. 10-parts:0.4,50-integration:0.7")
    ap.add_argument("--no-cards", action="store_true", help="leave missing chapters out instead of a title card")
    a = ap.parse_args(argv)
    only = set(a.only.split(",")) - {""} or None
    out = Path(a.out)
    odir = out.parent
    odir.mkdir(parents=True, exist_ok=True)
    chapters = scan(a.partial, only)
    if a.no_cards or only:
        chapters = [c for c in chapters if c["card"] is None]
    if not chapters:
        print("nothing to compose")
        return 1
    end = counters(chapters)
    marks, total = chapter_list(chapters)
    starts, k = [], 0
    for ch in chapters:
        starts.append(k)
        k += len(ch["meta"])
    ticks = [s / total for s in starts[1:]]
    cost_scale = 1.0
    for ch in chapters:
        for m in ch["meta"]:
            for key in ("run_new", "run_used"):
                r = P.lo_hi((m.get("cost") or {}).get(key))
                if r:
                    cost_scale = max(cost_scale, r[1])
    rows = lead_rows(load_hud())
    dur = total / FPS
    maxrate = int(min(4000, MAX_MB * 0.92 * 8e3 / max(dur, 1.0)))
    print(f"{len(chapters)} chapters, {total} frames, {dur:.0f} s; crf {a.crf}, maxrate {maxrate} kb/s", flush=True)
    enc = encoder(out, a.crf, maxrate)
    thumbs, stills = [], {}
    want = {}
    for s in a.stills.split(","):
        if ":" in s:
            c, f = s.split(":")
            want.setdefault(c, []).append(float(f))
    t0 = time.time()
    k = 0
    last = None
    for ci, ch in enumerate(chapters):
        n = len(ch["meta"])
        card = P.title_card(ch["card"]["title"], ch["card"]["lines"], ch["card"]["note"]) if ch["card"] else None
        pick = {int(n * f) for f in (0.12, 0.38, 0.62, 0.88)} if card is None else {n // 2}   # one thumb for a card
        title = ch["meta"][0].get("chapter") or ch["name"]
        for i, m in enumerate(ch["meta"]):
            if card is not None:
                base = card
            else:
                p = ch["dir"] / f"{i:05d}.png"
                try:
                    base = Image.open(p).convert("RGB")
                    if base.size != (W, H):
                        base = base.resize((W, H))
                    last = base
                except Exception:
                    base = last if last is not None else Image.new("RGB", (W, H), "white")
            t = i / FPS
            alpha = 0.0 if card is not None else (min(1.0, t / 0.4) if t < TITLE_S - 0.6 else max(0.0, (TITLE_S - t) / 0.6))
            frame = overlay(base, m, ch["clock"][i], (k + 1) / total, ticks, title, alpha, cost_scale, rows) \
                if card is None else base
            enc.stdin.write(frame.tobytes())
            if i in pick:
                thumbs.append((ch["name"], frame.resize((320, 180), Image.LANCZOS)))
            for f in want.get(ch["name"], []):
                if i == min(n - 1, int(n * f)):
                    stills[f"{ch['name']}-{int(f * 100):02d}"] = frame
            k += 1
            if k % 600 == 0:
                print(f"  {k}/{total} frames, {time.time() - t0:.0f} s", flush=True)
    enc.stdin.close()
    enc.wait()
    size = out.stat().st_size / 1e6
    print(f"{out}: {size:.1f} MB, {dur:.0f} s, {time.time() - t0:.0f} s to compose", flush=True)
    # the YouTube chapter list
    if out.name == "robot-build.mp4" or a.only == "":
        (odir / "chapters.txt").write_text("".join(f"{stamp(f0)} {t}\n" for f0, t in marks))
    # the contact sheet: four frames a chapter, four columns
    if thumbs:
        cols = 4
        rows_n = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 320, rows_n * 180), "white")
        for j, (_, im) in enumerate(thumbs):
            sheet.paste(im, ((j % cols) * 320, (j // cols) * 180))
        sheet_path = odir / (out.stem.replace("robot-build", "contact-sheet") + ".jpg"
                             if out.stem != "robot-build" else "contact-sheet.jpg")
        sheet.save(sheet_path, quality=78, optimize=True)
    for key, im in stills.items():
        small_png(im, odir / f"still-{key}.png")
    rep = dict(mp4=str(out.relative_to(common.REPO)) if out.is_relative_to(common.REPO) else str(out),
               mb=round(size, 1), seconds=round(dur, 1), frames=total, fps=FPS, crf=a.crf, maxrate_kbps=maxrate,
               chapters=[dict(folder=c["name"], frames=len(c["meta"]), seconds=round(len(c["meta"]) / FPS, 1),
                              finished=c["done"], card=c["card"] is not None, state=c.get("state", "rendered"))
                         for c in chapters],
               youtube_chapters=[dict(at=stamp(f0), title=t) for f0, t in marks],
               counters={k: round(v, 2) for k, v in end.items()},
               composed_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()))
    (odir / (out.stem + ".json" if out.stem != "robot-build" else "compose.json")).write_text(
        json.dumps(rep, indent=1) + "\n")
    print(json.dumps(rep["youtube_chapters"], indent=0))
    if size > MAX_MB:
        print(f"WARNING: {size:.1f} MB is over {MAX_MB} MB: re-run with a higher --crf", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
