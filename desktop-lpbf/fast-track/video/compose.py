"""Compose the fast-track video: the rendered 3-D frames, the panels drawn over them, one H.264 MP4.

    /tmp/venv/bin/python desktop-lpbf/fast-track/video/compose.py            # every chapter rendered under /tmp/ft-video/frames
    ... compose.py --stills                                                   # also the stills and the contact sheet

Layout (1920 x 1080): the 3-D picture on the left (1440 x 1080) with a caption bar along its top; a 480 px panel on the
right with the calendar (scenario A of ft_progression.py), the state, the running spend (parts.csv), what is being added or
moved (with its parts.csv line or MK number) and how fast the picture runs; a thin progress bar with a tick per chapter
along the bottom. Writes video/out/fast-track-progression.mp4, video/out/chapters.txt and video/out/compose.json, and with
--stills img/video/*.jpg.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine as E  # noqa: E402

FR = Path(os.environ.get("FT_VIDEO", "/tmp/ft-video")) / "frames"
OUT = HERE / "out"
IMG = HERE.parent / "img" / "video"
W, H = 1920, 1080
PW = W - E.W3
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
INK, MUTED, PANEL, ACCENT = "#f2f5f8", "#a9b6c3", "#1f2a36", "#f0a63a"
STATE_COL = {"S1": "#5b7fb5", "S2": "#8e6bbf", "FT-0": "#e08a3c", "FT-1": "#3a9a5b", "FT-1V": "#2a9fb0"}
MILESTONES = [("S1", "S1 guide-laser and scanner checks"), ("S2", "S2 FULL POWER INTO THE DUMP"), ("FT-0", "FT-0 FIRST TRACKS"),
              ("FT-1", "FT-1 FIRST COUPONS"), ("FT-1V", "FT-1V FIRST COUPONS (< 100 ppm)")]
F = {}


def font(size, bold=False):
    k = (size, bold)
    if k not in F:
        F[k] = ImageFont.truetype(BOLD if bold else FONT, size)
    return F[k]


def wrap(d, text, f, width):
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def money(x):
    return f"${x / 1000:.1f}k"


def sched():
    import story as ST
    return {m: ST.sched(m) for _, m in MILESTONES}


def panel(ov, ms, total_hi):
    """The right-hand panel for one overlay state."""
    im = Image.new("RGB", (PW, H), PANEL)
    d = ImageDraw.Draw(im)
    x0, y = 24, 22
    d.text((x0, y), "DESKTOP LPBF FAST TRACK", font=font(15, True), fill=MUTED)
    y += 30
    st = ov.get("state") or ""
    for ln in wrap(d, st, font(19, True), PW - 2 * x0)[:3]:
        d.text((x0, y), ln, font=font(19, True), fill=INK)
        y += 26
    y += 14
    # calendar
    d.line((x0, y, PW - x0, y), fill="#3a4856", width=1)
    y += 12
    d.text((x0, y), "CALENDAR (weeks from the order, scenario A)", font=font(13, True), fill=MUTED)
    y += 24
    cal = ov.get("calendar")
    if cal:
        task, lo, hi, note = cal
        big = "Day 0" if hi == 0 else f"Week {lo / 5:.1f}-{hi / 5:.1f}"
        d.text((x0, y), big, font=font(34, True), fill=ACCENT)
        y += 46
        sub = "the orders go out" if hi == 0 else f"working days {lo}-{hi}: {task}"
        for ln in wrap(d, sub, font(14), PW - 2 * x0)[:2]:
            d.text((x0, y), ln, font=font(14), fill=INK)
            y += 19
        if note:
            for ln in wrap(d, note, font(13), PW - 2 * x0)[:2]:
                d.text((x0, y), ln, font=font(13), fill=MUTED)
                y += 18
        # mini timeline: 0-8 weeks, each milestone's range, the current one outlined
        y += 8
        X = lambda wk: x0 + (PW - 2 * x0) * min(wk, 8.0) / 8.0  # noqa: E731
        for k in range(9):
            d.line((X(k), y + 64, X(k), y + 68), fill=MUTED)
            d.text((X(k) - 4, y + 70), str(k), font=font(11), fill=MUTED)
        for i, (stn, m) in enumerate(MILESTONES):
            a, b = SCHED[m]
            yy = y + 4 + i * 12
            d.rectangle((X(a / 5), yy, X(b / 5), yy + 8), fill=STATE_COL[stn])
            d.text((X(b / 5) + 4, yy - 3), stn, font=font(10), fill=MUTED)
        if hi > 0:
            d.rectangle((X(lo / 5), y, X(hi / 5), y + 64), outline=ACCENT, width=2)
        y += 92
    # spend
    d.line((x0, y, PW - x0, y), fill="#3a4856", width=1)
    y += 12
    d.text((x0, y), "SPENT SO FAR (parts.csv, low-high)", font=font(13, True), fill=MUTED)
    y += 24
    sp = ov.get("spend") or (0, 0, [])
    lo, hi, recent = sp
    d.text((x0, y), f"{money(lo)}-{money(hi)}" if hi else "$0", font=font(30, True), fill=INK)
    y += 42
    bw = PW - 2 * x0
    d.rectangle((x0, y, x0 + bw, y + 10), fill="#334250")
    d.rectangle((x0, y, x0 + bw * min(1.0, hi / total_hi), y + 10), fill="#6f8aa3")
    d.rectangle((x0, y, x0 + bw * min(1.0, lo / total_hi), y + 10), fill="#9fc2e0")
    y += 14
    d.text((x0, y), f"of {money(TOTAL[0])}-{money(TOTAL[1])} for all five states", font=font(12), fill=MUTED)
    y += 22
    for (i, item, a, b) in (recent or [])[-4:]:
        t = f"{i}  {item}"
        ln = wrap(d, t, font(12), bw - 110)[:1]
        d.text((x0, y), (ln[0] if ln else t)[:60], font=font(12), fill=INK)
        cost = f"{money(a)}-{money(b)}" if abs(b - a) > 1 else money(a)
        d.text((PW - x0 - d.textlength(cost, font=font(12)), y), cost, font=font(12), fill=MUTED)
        y += 17
    y += 10
    # now
    d.line((x0, y, PW - x0, y), fill="#3a4856", width=1)
    y += 12
    ad = ov.get("adding")
    if ad:
        verb, items = ad
        d.text((x0, y), verb.upper(), font=font(13, True), fill=ACCENT)
        y += 22
        for (name, pid) in items[:4]:
            for k, ln in enumerate(wrap(d, name, font(15, k == 0), bw)[:2]):
                d.text((x0, y), ln, font=font(15), fill=INK)
                y += 20
            if pid:
                d.text((x0, y), f"[{pid}]", font=font(13, True), fill=MUTED)
                y += 19
            y += 2
    for ln in (ov.get("panel") or [])[:5]:
        for l2 in wrap(d, ln, font(14), bw)[:2]:
            d.text((x0, y), l2, font=font(14), fill=INK)
            y += 19
    # footer: speed and sources
    yb = H - 96
    sp_txt = ov.get("speed") or ""
    if sp_txt:
        for ln in wrap(d, sp_txt, font(14, True), bw)[:2]:
            d.text((x0, yb), ln, font=font(14, True), fill="#ffd27a")
            yb += 19
    if ov.get("scan"):
        for ln in wrap(d, "scan vectors: " + ov["scan"], font(11), bw)[:2]:
            d.text((x0, yb), ln, font=font(11), fill=MUTED)
            yb += 15
    d.text((x0, H - 24), "Model: ft_model.py; bought parts are envelopes (estimates)", font=font(11), fill=MUTED)
    return im


def top_bar(im, ov, title_alpha):
    """Caption bar over the 3-D picture: chapter (number and title), the caption and its numbers."""
    bar = Image.new("RGBA", (E.W3, 92), (18, 26, 34, 205))
    d = ImageDraw.Draw(bar)
    ch = ov.get("chapter") or (0, "")
    d.text((20, 10), f"{ch[0]}  {ch[1]}", font=font(16, True), fill=MUTED)
    cap = ov.get("caption") or ("", "")
    d.text((20, 32), cap[0], font=font(28, True), fill=INK)
    if cap[1]:
        d.text((22, 66), cap[1], font=font(16), fill="#c9d4de")
    im.paste(bar, (0, 0), bar)
    if title_alpha > 0:
        card = Image.new("RGBA", (E.W3, 120), (18, 26, 34, int(215 * title_alpha)))
        d = ImageDraw.Draw(card)
        a = int(255 * title_alpha)
        d.text((40, 22), f"Chapter {ch[0]}", font=font(22, True), fill=(240, 166, 58, a))
        d.text((40, 54), ch[1], font=font(40, True), fill=(242, 245, 248, a))
        im.paste(card, (0, E.H3 - 200), card)


def chapters():
    out = []
    for d in sorted(FR.glob("ch*")):
        if (d / "meta.jsonl").exists():
            n = int(d.name[2:])
            out.append((n, d))
    return sorted(out)


SCHED, TOTAL = {}, (0, 1)


def main():
    global TOTAL
    import story as ST
    SCHED.update({m: ST.sched(m) for _, m in MILESTONES})
    cum = ST.cumulative()
    TOTAL = cum["FT-1V"]
    stills = "--stills" in sys.argv
    chs = chapters()
    metas = []
    for n, d in chs:
        rows = [json.loads(x) for x in open(d / "meta.jsonl")]
        metas.append((n, d, rows))
    total = sum(len(r) for _, _, r in metas)
    OUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUT / "fast-track-progression.mp4"
    ff = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(E.FPS), "-i", "-",
          "-c:v", "libx264", "-preset", "medium", "-crf", os.environ.get("CRF", "24"), "-pix_fmt", "yuv420p",
          "-threads", "2", "-movflags", "+faststart", str(mp4)]
    p = subprocess.Popen(ff, stdin=subprocess.PIPE)
    k = 0
    chap_txt, starts = [], []
    pcache = {}
    shots = []
    t0 = time.time()
    last_img = (None, None)
    sheet = []
    for n, d, rows in metas:
        starts.append(k)
        title = rows[0]["ov"].get("chapter", (n, ""))[1]
        s = k / E.FPS
        chap_txt.append(f"{int(s // 60)}:{int(s % 60):02d} {title}")
        prev_shot = None
        for i, r in enumerate(rows):
            if r["img"] != last_img[0] or d != last_img[1]:
                src = d / f"{r['img']:05d}.jpg"
                base = Image.open(src).convert("RGB")
                last_img = (r["img"], d, base)
            base = last_img[2]
            ov = r["ov"]
            key = hashlib.blake2b(json.dumps({x: ov.get(x) for x in ("state", "calendar", "spend", "adding", "panel", "speed",
                                                                     "scan")}, sort_keys=True).encode(),
                                  digest_size=8).hexdigest()
            if key not in pcache:
                if len(pcache) > 200:
                    pcache.clear()
                pcache[key] = panel(ov, SCHED, TOTAL[1])
            frame = Image.new("RGB", (W, H))
            frame.paste(base, (0, 0))
            frame.paste(pcache[key], (E.W3, 0))
            tt = r["t"]
            ta = 1.0 if tt < 2.5 else max(0.0, 1.0 - (tt - 2.5) / 0.7)
            top_bar(frame, ov, ta)
            dd = ImageDraw.Draw(frame)
            dd.rectangle((0, H - 6, int(W * (k + 1) / total), H), fill="#f0a63a")
            p.stdin.write(frame.tobytes())
            if r["shot"] != prev_shot:
                shots.append(dict(chapter=n, shot=r["shot"], start_s=round(k / E.FPS, 2)))
                prev_shot = r["shot"]
            if stills and (i in (len(rows) // 5, 2 * len(rows) // 5, 3 * len(rows) // 5, 4 * len(rows) // 5 - 1)):
                sheet.append((n, i, frame.copy()))
            k += 1
            if k % 600 == 0:
                print(f"  {k}/{total} frames, {time.time() - t0:.0f} s", flush=True)
    p.stdin.close()
    p.wait()
    (OUT / "chapters.txt").write_text("\n".join(chap_txt) + "\n")
    for i, sh in enumerate(shots):
        sh["seconds"] = round((shots[i + 1]["start_s"] if i + 1 < len(shots) else k / E.FPS) - sh["start_s"], 2)
    durs = [s["seconds"] for s in shots]
    info = dict(file=str(mp4.relative_to(HERE.parents[2])), frames=k, fps=E.FPS, seconds=round(k / E.FPS, 1),
                bytes=mp4.stat().st_size, chapters=chap_txt, shots=shots,
                shot_median_s=float(np.median(durs)) if durs else 0, shot_min_s=min(durs) if durs else 0,
                composed_s=round(time.time() - t0, 1))
    (OUT / "compose.json").write_text(json.dumps(info, indent=1))
    print(f"{mp4}: {k} frames, {k / E.FPS:.1f} s, {mp4.stat().st_size / 1e6:.1f} MB; shots: median {info['shot_median_s']:.1f} s, "
          f"min {info['shot_min_s']:.1f} s", flush=True)
    if stills:
        IMG.mkdir(parents=True, exist_ok=True)
        tw, th = 480, 270
        cols = 4
        rows_ = (len(sheet) + cols - 1) // cols
        cs = Image.new("RGB", (cols * tw, rows_ * th), "#ffffff")
        for j, (n, i, fr) in enumerate(sheet):
            cs.paste(fr.resize((tw, th), Image.LANCZOS), ((j % cols) * tw, (j // cols) * th))
        cs.save(IMG / "contact-sheet.jpg", quality=85)
        picks = {}
        for n, i, fr in sheet:
            picks.setdefault(n, []).append((i, fr))
        for n, lst in picks.items():
            i, fr = lst[min(2, len(lst) - 1)]
            fr.save(IMG / f"still-ch{n}.jpg", quality=86)
        print("wrote stills and contact sheet", flush=True)


if __name__ == "__main__":
    main()
