"""The on-screen panels of the robot-built desktop LPBF video, drawn with PIL over the 3-D frames (compose.py).

Every panel is a function of one frame's metadata (common.py's docstring lists the keys) plus the running state that
compose.py keeps (clocks, counters, the chapter list), so the panels can change without re-rendering any 3-D.

Layout on the 1280 x 720 frame:
  * top: the caption bar (caption, sub), with who is working and the step's status as badges at its right end;
  * bottom left: the clocks (project working day at 8 h a day, machine, robot, person and CAM hours, outsourced days);
  * right column (x >= 892), when the frame's metadata has them: the cost panel and, under it, the lead-time panel;
  * labels that belong to objects, where the renderer projected them;
  * a thin progress bar along the bottom edge with a tick at each chapter.

Colours: who-badges use common.WHO_COL; the cost and lead panels compare "new" and "used / eBay" in the first two
slots of the dataviz skill's validated categorical order (blue #257de0, orange #f47230); text stays in text inks.
"""
from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import common

W, H = common.W, common.H
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
INK = (25, 27, 31)
INK2 = (96, 101, 108)
INK3 = (150, 155, 162)
PANEL = (255, 255, 255, 226)
RULE = (205, 210, 216, 255)
NEW = (0x25, 0x7d, 0xe0)            # dataviz slot 1 (blue): new
USED = (0xf4, 0x72, 0x30)           # dataviz slot 2 (orange): used / eBay
HILITE = (255, 236, 170, 255)
STATUS = {"pass": ("PASS", common.COL["ok"]), "fail": ("FAIL", common.COL["fail"]),
          "redesign": ("REDESIGN", common.COL["redesign"]), "person": ("PERSON NEEDED", common.WHO_COL["person"])}
RIGHT_X = 892                       # the right column's left edge


def rgb(h):
    if isinstance(h, str):
        return tuple(int(h[k:k + 2], 16) for k in (1, 3, 5))
    return tuple(h)


@lru_cache(maxsize=None)
def font(size, bold=False, mono=False, cond=False):
    if mono:
        name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    elif cond:
        name = "DejaVuSansCondensed-Bold.ttf" if bold else "DejaVuSansCondensed.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(FONT_DIR / name), int(size))


def money(v):
    """$ with k above 10,000: $840, $2,100, $23.0k, $112.9k."""
    if v is None:
        return "-"
    v = float(v)
    if abs(v) >= 10000:
        return f"${v / 1000:.1f}k"
    return f"${v:,.0f}"


def money_range(v):
    """A number or [low, high] as money; equal ends as one number."""
    if isinstance(v, (list, tuple)):
        lo, hi = (float(v[0]), float(v[-1])) if len(v) else (0.0, 0.0)
        if abs(hi - lo) < 0.5:
            return money(lo)
        if lo >= 10000 or hi >= 10000:
            return f"${lo / 1000:.1f}k-{hi / 1000:.1f}k"
        return f"${lo:,.0f}-{hi:,.0f}"
    return money(v)


def lo_hi(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        return (float(v[0]), float(v[-1])) if len(v) else None
    return (float(v), float(v))


def weeks(v):
    """Lead time in weeks as text: 0.4 -> 3 d, 1.5 -> 1.5 wk, [10, 12] -> 10-12 wk."""
    r = lo_hi(v)
    if r is None:
        return "-"
    lo, hi = r

    def one(x):
        if x < 1.0:
            return f"{max(1, round(x * 7))} d"
        return f"{x:g} wk" if x < 10 else f"{x:.0f} wk"
    if abs(hi - lo) < 1e-6:
        return one(lo)
    if hi < 1.0:
        return f"{max(1, round(lo * 7))}-{max(1, round(hi * 7))} d"
    if lo < 1.0:
        return f"{one(lo)}-{one(hi)}"
    return f"{lo:g}-{hi:g} wk"


def fit(d, text, f, width):
    """`text` cut with an ellipsis to fit `width` px in font f."""
    if d.textlength(text, font=f) <= width:
        return text
    while len(text) > 3 and d.textlength(text + "...", font=f) > width:
        text = text[:-1]
    return text.rstrip() + "..."


def wrap(d, text, f, width, max_lines=2):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) > width and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = t
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit(d, lines[-1] + " ...", f, width)
    return lines


# ------------------------------------------------------------------------------------------------ the caption bar
def badges(d, x_right, y, who, status):
    """Who-badges and the status badge, right-aligned ending at x_right; returns the left edge used."""
    f = font(12, bold=True)
    items = []
    if status in STATUS:
        items.append((STATUS[status][0], rgb(STATUS[status][1])))
    for w_ in (who or []):
        col = common.WHO_COL.get(w_)
        if col is None:
            continue
        items.append((w_.upper(), rgb(col)))
    x = x_right
    for text, col in items:
        tw = d.textlength(text, font=f)
        x0 = x - tw - 16
        d.rounded_rectangle((x0, y, x, y + 22), 11, fill=col + (255,))
        d.text((x0 + 8, y + 4), text, font=f, fill=(255, 255, 255))
        x = x0 - 6
    return x


def caption_bar(d, caption, sub, who, status, chapter_no=None, step=""):
    h = 62 if sub else 44
    d.rectangle((0, 0, W, h), fill=(255, 255, 255, 232))
    d.line([(0, h), (W, h)], fill=(30, 60, 140, 255), width=2)
    left = badges(d, W - 12, 11, who, status)
    if step:
        f = font(11, mono=True)
        d.text((left - d.textlength(step, font=f) - 4, 15), step, font=f, fill=INK2)
        left -= d.textlength(step, font=f) + 10
    room = max(200, left - 24)
    fc = font(21, bold=True)
    cap = caption or ""
    if d.textlength(cap, font=fc) > room:
        fc = font(18, bold=True)
    d.text((14, 8), fit(d, cap, fc, room), font=fc, fill=INK)
    if sub:
        fs = font(14)
        d.text((14, 37), fit(d, sub, fs, W - 28), font=fs, fill=INK2)
    return h


# ------------------------------------------------------------------------------------------------ the clocks
def speed_text(speed):
    """How fast the frame's real-world time runs: "real time", or "time-lapse x60" (two significant figures)."""
    if speed <= 1.5:
        return "real time"
    e = 10 ** max(0, math.floor(math.log10(speed)) - 1)
    return f"time-lapse x{round(speed / e) * e:,.0f}"


def clocks(d, st, y_bottom=H - 14, speed=None):
    """st: dict(t_s, machine_h, robot_h, person_h, cam_h, outsourced_d). Project time in 8 h working days; speed: the
    frame's real-world seconds per second of video (proc_s x FPS), shown as "real time" or "time-lapse xN"."""
    t_h = st.get("t_s", 0.0) / 3600.0
    day = int(t_h // 8.0) + 1
    into = t_h - 8.0 * (day - 1)
    hh, mm = int(into), int(round((into - int(into)) * 60))
    if mm == 60:
        hh, mm = hh + 1, 0
    rows = [("machine", st.get("machine_h", 0.0), "h", common.WHO_COL["machine"]),
            ("robots", st.get("robot_h", 0.0), "h", common.WHO_COL["robot A"]),
            ("people", st.get("person_h", 0.0), "h", common.WHO_COL["person"]),
            ("CAM", st.get("cam_h", 0.0), "h", "#34495e"),
            ("outsourced", st.get("outsourced_d", 0.0), "d", common.WHO_COL["outsourced"])]
    fb, fm, fl = font(20, bold=True), font(12, mono=True), font(10)
    w, h = 252, 30 + 16 * 3 + 8
    x0, y0 = 12, y_bottom - h
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 8, fill=PANEL, outline=RULE)
    d.text((x0 + 10, y0 + 5), f"Day {day}", font=fb, fill=INK)
    dw = d.textlength(f"Day {day}", font=fb)
    d.text((x0 + 18 + dw, y0 + 12), f"+{hh}:{mm:02d} h   (8 h working days)", font=fl, fill=INK2)
    if speed is not None and speed > 0:
        t = speed_text(speed)
        ft = font(10, bold=True)
        tw = d.textlength(t, font=ft)
        col = (90, 96, 104) if speed <= 1.5 else (176, 96, 20)
        d.rounded_rectangle((x0 + w - tw - 14, y0 - 20, x0 + w, y0 - 3), 8, fill=(255, 255, 255, 220), outline=RULE)
        d.text((x0 + w - tw - 7, y0 - 18), t, font=ft, fill=col)
    for k, (name, v, unit, col) in enumerate(rows):
        cx = x0 + 10 + (k % 2) * 122
        cy = y0 + 32 + (k // 2) * 16
        d.ellipse((cx, cy + 3, cx + 8, cy + 11), fill=rgb(col) + (255,))
        val = f"{v:.1f}" if v < 100 else f"{v:.0f}"
        d.text((cx + 12, cy), f"{name} {val} {unit}", font=fm, fill=INK)


# ------------------------------------------------------------------------------------------------ the cost panel
def _bar(d, x, y, w, h, frac_lo, frac_hi, col):
    """A bar from 0 to frac_lo solid, frac_lo to frac_hi in a lighter tint (the range of a low-high estimate)."""
    d.rounded_rectangle((x, y, x + w, y + h), 3, fill=(236, 239, 242, 255))
    lo = max(0.0, min(1.0, frac_lo)) * w
    hi = max(0.0, min(1.0, frac_hi)) * w
    if hi > lo + 1:
        tint = tuple(int(c + (255 - c) * 0.55) for c in col)
        d.rounded_rectangle((x, y, x + hi, y + h), 3, fill=tint + (255,))
    if lo > 1:
        d.rounded_rectangle((x, y, x + lo, y + h), 3, fill=col + (255,))


def cost_panel(d, cost, scale, y0=72):
    """cost: {"cat", "cat_no", "n_cats", "new", "used", "run_new", "run_used", "items": [...], "note"}; scale: the
    largest running total in the chapter (the bars' full width). Returns the bottom y."""
    x0, w = RIGHT_X, W - RIGHT_X - 12
    items = cost.get("items") or []
    n_items = min(len(items), 4)
    h = 132 + (22 + 34 * n_items if n_items else 0) + (16 if cost.get("note") else 0)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 8, fill=PANEL, outline=RULE)
    ft, fb, f, fs = font(12, bold=True), font(13, bold=True), font(12), font(11)
    head = "RUNNING COST OF THE KIT"
    if cost.get("cat_no") and cost.get("n_cats"):
        head += f"   ({cost['cat_no']} of {cost['n_cats']} categories)"
    d.text((x0 + 10, y0 + 7), head, font=ft, fill=INK2)
    bx, bw = x0 + 64, w - 74 - 92
    y = y0 + 28
    for lab, key, col in (("New", "run_new", NEW), ("Used", "run_used", USED)):
        r = lo_hi(cost.get(key))
        d.text((x0 + 10, y + 1), lab, font=fb, fill=INK)
        if r is not None:
            _bar(d, bx, y + 2, bw, 13, r[0] / scale, r[1] / scale, col)
            d.text((bx + bw + 6, y), money_range(cost.get(key)), font=f, fill=INK)
        y += 22
    d.text((x0 + 10, y), fit(d, cost.get("foot") or "solid: low end, tint: up to the high end; used = eBay and "
                             "surplus where sensible", font(9), w - 20), font=font(9), fill=INK3)
    y += 18
    d.line([(x0 + 10, y), (x0 + w - 10, y)], fill=RULE, width=1)
    y += 6
    if cost.get("cat"):
        d.text((x0 + 10, y), fit(d, cost["cat"], fb, w - 20), font=fb, fill=INK)
        y += 19
        line = f"new {money_range(cost.get('new'))}"
        if cost.get("used") is not None:
            line += f"   used {money_range(cost.get('used'))}"
        d.text((x0 + 10, y), line, font=f, fill=INK)
        y += 20
    if n_items:
        d.text((x0 + 10, y), "THE BIG ITEMS", font=font(10, bold=True), fill=INK2)
        y += 16
        for it in items[:4]:
            hl = it.get("hl")
            if hl:
                d.rounded_rectangle((x0 + 4, y - 2, x0 + w - 4, y + 32), 5, fill=HILITE)
            name = fit(d, it.get("name", ""), font(12, bold=bool(hl)), w - 24)
            d.text((x0 + 10, y), name, font=font(12, bold=bool(hl)), fill=INK)
            t_new = "new " + money_range(it.get("new"))
            if it.get("lead_new") is not None:
                t_new += ", " + weeks(it["lead_new"])
            parts = [(t_new, NEW)]
            if it.get("used") is not None:
                t_used = (it.get("used_label") or "used") + " " + money_range(it.get("used"))
                if it.get("lead_used") is not None:
                    t_used += ", " + weeks(it["lead_used"])
                parts.append((t_used, USED))
            xx = x0 + 22
            for text, col in parts:
                text = fit(d, text, fs, x0 + w - 8 - xx)
                d.ellipse((xx - 10, y + 20, xx - 3, y + 27), fill=col + (255,))
                d.text((xx, y + 16), text, font=fs, fill=INK)
                xx += d.textlength(text, font=fs) + 18
            y += 34
    if cost.get("note"):
        d.text((x0 + 10, y + 2), fit(d, cost["note"], fs, w - 20), font=fs, fill=INK2)
        y += 16
    return y0 + h


# ------------------------------------------------------------------------------------------------ the lead-time panel
def lead_panel(d, rows, highlight, y0, max_rows=11, y_max=H - 20):
    """rows: [{"name", "new": [lo, hi] wk, "used": [lo, hi] wk or None, "long": bool}], longest first; highlight: names
    to mark. Horizontal bars on one axis (weeks), new and used side by side."""
    if not rows:
        return y0
    x0, w = RIGHT_X, W - RIGHT_X - 12
    hl = set(highlight or [])
    # keep the highlighted rows in view: the longest, plus any highlighted ones further down
    keep = rows[:max_rows]
    extra = [r for r in rows[max_rows:] if r["name"] in hl]
    if extra:
        keep = keep[:max_rows - len(extra)] + extra
    row_h = 21
    h = 46 + row_h * len(keep) + 16
    if y0 + h > y_max:
        keep = keep[:max(3, (y_max - y0 - 62) // row_h)]
        h = 46 + row_h * len(keep) + 16
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 8, fill=PANEL, outline=RULE)
    d.text((x0 + 10, y0 + 7), "LEAD TIME, WEEKS (ORDER TO DOOR)", font=font(12, bold=True), fill=INK2)
    lx = x0 + 10
    for text, col in (("new", NEW), ("used / eBay", USED)):
        d.rectangle((lx, y0 + 28, lx + 10, y0 + 36), fill=col + (255,))
        d.text((lx + 14, y0 + 25), text, font=font(11), fill=INK)
        lx += d.textlength(text, font=font(11)) + 30
    d.ellipse((lx - 6, y0 + 29, lx - 1, y0 + 34), fill=rgb(common.COL["fail"]) + (255,))
    d.text((lx + 2, y0 + 25), "long lead", font=font(11), fill=INK)
    wmax = max(1.0, max(max((lo_hi(r.get("new")) or (0, 0))[1], (lo_hi(r.get("used")) or (0, 0))[1]) for r in keep))
    wmax = max(4.0, math.ceil(wmax / 2.0) * 2.0)
    name_w = 128
    bx, bw = x0 + 10 + name_w, w - 20 - name_w - 4
    y = y0 + 44
    for r in keep:
        on = r["name"] in hl
        if on:
            d.rounded_rectangle((x0 + 4, y - 2, x0 + w - 4, y + row_h - 3), 4, fill=HILITE)
        fnm = font(11, bold=on, cond=True)
        d.text((x0 + 10, y + 2), fit(d, r["name"], fnm, name_w - 6), font=fnm, fill=INK)
        for k, (key, col) in enumerate((("new", NEW), ("used", USED))):
            v = lo_hi(r.get(key))
            yy = y + 2 + k * 8
            if v is None:
                continue
            lo, hi = v
            x_lo, x_hi = bx + bw * lo / wmax, bx + bw * hi / wmax
            d.rectangle((bx, yy, max(bx + 2, x_lo), yy + 6), fill=col + (255,))
            if x_hi > x_lo + 1:
                tint = tuple(int(c + (255 - c) * 0.55) for c in col)
                d.rectangle((x_lo, yy, x_hi, yy + 6), fill=tint + (255,))
        if r.get("long"):
            d.ellipse((x0 + 3, y + 6, x0 + 8, y + 11), fill=rgb(common.COL["fail"]) + (255,))
        y += row_h
    # the axis: a tick every 2 weeks
    d.line([(bx, y), (bx + bw, y)], fill=INK3, width=1)
    step = 2 if wmax <= 16 else 4
    for t in range(0, int(wmax) + 1, step):
        tx = bx + bw * t / wmax
        d.line([(tx, y), (tx, y + 3)], fill=INK3, width=1)
        d.text((tx - 4, y + 3), str(t), font=font(9), fill=INK2)
    return y0 + h


# ------------------------------------------------------------------------------------------------ a small line chart
def chart_panel(d, spec, y0=72, h=250):
    """A line chart in the right column, drawn up to the frame's point: spec = {"title", "x" (list), "y" (list), "now"
    (index drawn up to), "ylog" (bool), "xlabel", "ylabel", "xticks", "ref" (a horizontal reference value), "ref_label",
    "value" (text shown big), "verdict" ("pass" | "fail" | "")}. One series, one axis."""
    import math as _m
    x0, w = RIGHT_X, W - RIGHT_X - 12
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 8, fill=PANEL, outline=RULE)
    d.text((x0 + 10, y0 + 7), spec.get("title", "").upper(), font=font(12, bold=True), fill=INK2)
    if spec.get("value"):
        fv = font(18, bold=True)
        d.text((x0 + 10, y0 + 25), spec["value"], font=fv, fill=INK)
        if spec.get("verdict") in STATUS:
            t, col = STATUS[spec["verdict"]]
            tw = d.textlength(t, font=font(12, bold=True))
            d.rounded_rectangle((x0 + w - tw - 26, y0 + 27, x0 + w - 10, y0 + 49), 11, fill=rgb(col) + (255,))
            d.text((x0 + w - tw - 18, y0 + 31), t, font=font(12, bold=True), fill=(255, 255, 255))
    xs, ys = list(spec.get("x") or []), list(spec.get("y") or [])
    if len(xs) < 2:
        return y0 + h
    now = int(spec.get("now", len(xs) - 1))
    ylog = bool(spec.get("ylog"))
    f = (lambda v: _m.log10(max(v, 1e-12))) if ylog else (lambda v: v)
    fy = [f(v) for v in ys]
    lo, hi = min(fy), max(fy)
    if spec.get("ref") is not None:
        lo, hi = min(lo, f(spec["ref"])), max(hi, f(spec["ref"]))
    if ylog:
        lo, hi = _m.floor(lo), _m.ceil(hi)
    if hi - lo < 1e-9:
        hi = lo + 1.0
    px0, px1 = x0 + 58, x0 + w - 14
    py0, py1 = y0 + 62, y0 + h - 34
    xmin, xmax = xs[0], xs[-1]

    def X(v):
        return px0 + (px1 - px0) * (v - xmin) / max(xmax - xmin, 1e-9)

    def Y(v):
        return py1 - (py1 - py0) * (f(v) - lo) / (hi - lo)
    ft = font(9)
    if ylog:                                                      # a gridline and a label every decade
        for e in range(int(lo), int(hi) + 1):
            yy = py1 - (py1 - py0) * (e - lo) / (hi - lo)
            d.line([(px0, yy), (px1, yy)], fill=(225, 229, 234, 255), width=1)
            d.text((x0 + 8, yy - 6), f"1e{e}" if e not in (0, 1, 2, 3) else str(10 ** e), font=ft, fill=INK2)
    d.line([(px0, py1), (px1, py1)], fill=INK3, width=1)
    d.line([(px0, py0), (px0, py1)], fill=INK3, width=1)
    for t in spec.get("xticks") or []:
        tx = X(t)
        d.line([(tx, py1), (tx, py1 + 3)], fill=INK3, width=1)
        lab = f"{t:g}"
        d.text((tx - d.textlength(lab, font=ft) / 2, py1 + 4), lab, font=ft, fill=INK2)
    if spec.get("xlabel"):
        d.text((px1 - d.textlength(spec["xlabel"], font=ft), py1 + 16), spec["xlabel"], font=ft, fill=INK2)
    if spec.get("ylabel"):
        d.text((x0 + 8, py0 - 14), spec["ylabel"], font=ft, fill=INK2)
    if spec.get("ref") is not None:
        ry = Y(spec["ref"])
        for xx in range(int(px0), int(px1), 8):
            d.line([(xx, ry), (min(xx + 4, px1), ry)], fill=rgb(common.COL["fail"]) + (255,), width=1)
        if spec.get("ref_label"):
            d.text((px0 + 4, ry - 13), spec["ref_label"], font=ft, fill=rgb(common.COL["fail"]))
    pts = [(X(xs[k]), Y(ys[k])) for k in range(min(now + 1, len(xs)))]
    if len(pts) >= 2:
        d.line(pts, fill=NEW + (255,), width=2)
    if pts:
        cx, cy = pts[-1]
        d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=NEW + (255,), outline=(255, 255, 255, 255))
    return y0 + h


# ------------------------------------------------------------------------------------------------ labels, progress, titles
def labels(d, labs):
    f = font(12)
    for lab in labs or []:
        try:
            x, y, text = float(lab[0]), float(lab[1]), str(lab[2])
        except Exception:
            continue
        if not (0 <= x <= W and 0 <= y <= H):
            continue
        tw = d.textlength(text, font=f)
        tx, ty = x + 14, y - 26
        if tx + tw + 12 > W - 4:
            tx = x - 14 - tw - 12
        ty = max(70, ty)
        d.line([(x, y), (tx if tx > x else tx + tw + 12, ty + 10)], fill=(55, 60, 68, 230), width=1)
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(40, 40, 46, 255), outline=(255, 255, 255, 255))
        d.rounded_rectangle((tx, ty, tx + tw + 12, ty + 20), 4, fill=(255, 255, 255, 225), outline=(140, 145, 152, 255))
        d.text((tx + 6, ty + 3), text, font=f, fill=INK)


def progress(d, frac, ticks, chapter_fracs=None):
    y = H - 5
    d.rectangle((0, y, W, H), fill=(210, 214, 219, 255))
    d.rectangle((0, y, int(W * max(0.0, min(1.0, frac))), H), fill=(30, 60, 140, 255))
    for t in ticks:
        x = int(W * t)
        d.rectangle((x - 1, y - 3, x + 1, H), fill=(255, 255, 255, 255))


def chapter_title(d, title, alpha):
    """The chapter's title as a lower third for its first seconds (alpha 0-1)."""
    if alpha <= 0.02:
        return
    a = int(255 * alpha)
    f = font(30, bold=True)
    tw = d.textlength(title, font=f)
    x0, y0 = 40, H - 168
    d.rectangle((x0 - 14, y0 - 10, x0 + tw + 20, y0 + 46), fill=(20, 32, 64, int(200 * alpha)))
    d.rectangle((x0 - 14, y0 - 10, x0 - 8, y0 + 46), fill=(242, 193, 78, a))
    d.text((x0 + 4, y0), title, font=f, fill=(255, 255, 255, a))


def title_card(title, lines=(), note=""):
    """A full frame: a title and a few lines of text (missing chapters, the end card)."""
    im = Image.new("RGB", (W, H), rgb(common.BG_TOP))
    d = ImageDraw.Draw(im, "RGBA")
    for yy in range(H):                                      # the shared background's gradient
        t = yy / (H - 1)
        c0, c1 = rgb(common.BG_TOP), rgb(common.BG_BOTTOM)
        d.line([(0, yy), (W, yy)], fill=tuple(int(a + (b - a) * t) for a, b in zip(c0, c1)))
    f = font(36, bold=True)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, H / 2 - 90), title, font=f, fill=INK)
    fy = H / 2 - 30
    for ln in lines:
        fl = font(19)
        lw = d.textlength(ln, font=fl)
        d.text(((W - lw) / 2, fy), ln, font=fl, fill=INK2)
        fy += 30
    if note:
        fn = font(14)
        nw = d.textlength(note, font=fn)
        d.text(((W - nw) / 2, H - 70), note, font=fn, fill=INK3)
    return im
