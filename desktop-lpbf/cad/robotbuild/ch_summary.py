"""Chapter 60-summary of the robot-built desktop LPBF video: 2-D charts of time and cost (about 80 s).

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_summary.py

Each slide is one matplotlib figure at 1280 x 720 with one message (the caption bar, drawn by compose.py, states it);
bars grow in over a second, then the slide holds. The top 70 px and the bottom 20 px are left for compose.py's caption
bar and progress bar. What each slide reads (whatever is there when it runs; a slide whose data is missing says so):
  1. the video's own clocks: compose.py's counters summed over every chapter rendered so far (frames' proc_s and add);
  2. the kit's cost by category, new against used: the data worker's /tmp/robotbuild/data/hud.json (categories);
  3. when every part is in hand, by buying route: hud.json lead_times.schedule (new as chosen, new with stocked swaps,
     used majors);
  4. time and cost by route (in-house, outsourced, hybrid, robot shop): the route worker's /tmp/robotbuild/data/route.json;
  5. where a person is needed: the assembly worker's /tmp/robotbuild/data/assembly.json (steps whose status is "person"),
     the shop worker's /tmp/robotbuild/data/shop.json if it is there, and sequence.py's tray steps T01-T05;
  6. what had to be redesigned: the same files' "redesign" steps (and any "redesigns" list in them).
Colours: new #257de0 and used #f47230 (the cost and lead panels' pair, the dataviz skill's first two slots); text in
text inks. No project time passes in this chapter (proc_s 0); the clocks are hidden (slide 1 shows their totals).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FPS = common.FPS
NAME, TITLE = "60-summary", "Time and cost: in-house, outsourced, robot shop"
NEW, USED = "#257de0", "#f47230"
INK, INK2, GRID = "#1a1c20", "#5f656c", "#dfe3e8"
BG = common.BG_TOP
TOP, BOTTOM = 76, 26                        # px kept clear for compose.py's caption bar and progress bar
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": "#b9c0c7",
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK, "axes.titlesize": 15})


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def load(name):
    p = common.DATA / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def fig_axes(rect=None):
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    y0 = BOTTOM / common.H + 0.07
    h = 1 - (TOP + BOTTOM) / common.H - 0.12
    ax = fig.add_axes(rect or [0.24, y0, 0.70, h])
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return fig, ax


def to_img(fig):
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    plt.close(fig)
    return img


def note_slide(text, sub=""):
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    fig.text(0.5, 0.55, text, ha="center", va="center", fontsize=22, color=INK, wrap=True)
    if sub:
        fig.text(0.5, 0.45, sub, ha="center", va="center", fontsize=14, color=INK2, wrap=True)
    return to_img(fig)


def money_k(v):
    """$ as text for matplotlib (escaped, so two of them don't start mathtext)."""
    return f"\\${v / 1000:.0f}k" if v >= 10000 else f"\\${v / 1000:.1f}k"


# ------------------------------------------------------------------------------------------------ the slides
def slide_clocks(u):
    """Stat tiles: what the video's clocks added up to over the chapters rendered."""
    import compose as CP
    chs = [c for c in CP.scan(partial=True) if c["card"] is None and c["name"] != NAME]
    end = CP.counters(chs) if chs else {}
    tiles = [("Project time", f"{end.get('t_s', 0) / 3600 / 8:.1f}", "working days of 8 h"),
             ("Machine", f"{end.get('machine_h', 0):.1f}", "hours"), ("Robots", f"{end.get('robot_h', 0):.1f}", "hours"),
             ("People", f"{end.get('person_h', 0):.1f}", "hours"), ("CAM", f"{end.get('cam_h', 0):.1f}", "hours"),
             ("Outsourced", f"{end.get('outsourced_d', 0):.1f}", "days")]
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    for k, (name, val, unit) in enumerate(tiles):
        col, row = k % 3, k // 3
        x0, y0 = 0.06 + col * 0.305, 0.50 - row * 0.32
        a = ease(u * 1.6 - 0.1 * k)
        ax = fig.add_axes([x0, y0, 0.27, 0.26])
        ax.set_axis_off()
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="white", edgecolor="#cfd5db",
                                   alpha=0.9 * a))
        ax.text(0.06, 0.78, name.upper(), transform=ax.transAxes, fontsize=13, color=INK2, alpha=a, weight="bold")
        ax.text(0.06, 0.30, val, transform=ax.transAxes, fontsize=38, color=INK, alpha=a, weight="bold")
        ax.text(0.06, 0.10, unit, transform=ax.transAxes, fontsize=12, color=INK2, alpha=a)
    names = ", ".join(c["name"] for c in chs) if chs else "none"
    fig.text(0.06, 0.12, f"Summed over the chapters rendered in this cut: {names}.", fontsize=11, color=INK2)
    return to_img(fig), len(chs)


def slide_cost(u, hud):
    cats = [c for c in hud.get("categories", []) if c.get("new")]
    if not cats:
        return note_slide("The cost data (hud.json) was not ready for this cut")
    cats = cats[::-1]
    names = [c.get("title", c.get("cat", "")).split(":")[0] for c in cats]
    fig, ax = fig_axes([0.30, 0.10, 0.64, 0.74])
    y = np.arange(len(cats))
    s = ease(u)
    for k, c in enumerate(cats):
        n0, n1 = c["new"]
        u0, u1 = (c.get("used") or c["new"])
        ax.barh(k + 0.18, n0 * s, height=0.32, color=NEW, edgecolor=BG, linewidth=1.0)
        ax.barh(k + 0.18, (n1 - n0) * s, left=n0 * s, height=0.32, color=NEW, alpha=0.40, edgecolor=BG, linewidth=1.0)
        ax.barh(k - 0.18, u0 * s, height=0.32, color=USED, edgecolor=BG, linewidth=1.0)
        ax.barh(k - 0.18, (u1 - u0) * s, left=u0 * s, height=0.32, color=USED, alpha=0.40, edgecolor=BG, linewidth=1.0)
        if u > 0.8 and n1 > 4000:
            ax.text(n1 * s + 400, k + 0.18, f"{money_k(n0)}-{money_k(n1)}", va="center", fontsize=10, color=INK2)
            if (u1 < n1 - 500):
                ax.text(u1 * s + 400, k - 0.18, f"{money_k(u0)}-{money_k(u1)}", va="center", fontsize=10, color=INK2)
    ax.set_yticks(y, names)
    ax.set_xlabel("USD (solid: low end of the BOM range; pale: up to its high end)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=NEW, label="new"), Patch(color=USED, label="used where sensible (eBay, surplus)")],
              loc="upper right", frameon=False, fontsize=12)
    return to_img(fig)


def slide_lead(u, hud):
    sch = ((hud.get("lead_times") or {}).get("schedule") or {}).get("routes") or {}
    rows = []
    label = dict(new="All new, as chosen", new_with_swaps="All new, two slow parts swapped", used="Used majors")
    for key in ("new", "new_with_swaps", "used"):
        r = sch.get(key)
        if not r or not r.get("parts_in_hand_wk"):
            continue
        by = r.get("set_by") or ""
        try:
            import ch_parts as CPT
            by_name = CPT.SHORT.get(by) or (r.get("set_by_item") or by)
        except Exception:                                        # noqa: BLE001
            by_name = r.get("set_by_item") or by
        rows.append((label.get(key, key), r["parts_in_hand_wk"], by_name))
    if not rows:
        return note_slide("The lead-time schedule (hud.json) was not ready for this cut")
    rows = rows[::-1]
    fig, ax = fig_axes([0.30, 0.16, 0.64, 0.66])
    s = ease(u)
    for k, (name, (lo, hi), by) in enumerate(rows):
        col = USED if "Used" in name else NEW
        ax.barh(k, lo * s, height=0.5, color=col, edgecolor=BG)
        ax.barh(k, (hi - lo) * s, left=lo * s, height=0.5, color=col, alpha=0.4, edgecolor=BG)
        if u > 0.8:
            ax.text(hi * s + 0.4, k, f"{lo:.0f}-{hi:.0f} wk; the last part in: {by}", va="center",
                    fontsize=11, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlabel("weeks from ordering to every part in hand (BYU purchase orders included)")
    ax.set_xlim(0, max(r[1][1] for r in rows) * 1.55)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    return to_img(fig)


def slide_shop_hours(u, hud):
    """Person-hours to make the custom parts, step by step: by hand against the robot shop (hud.json times.robot_shop)."""
    rs = (hud.get("times") or {}).get("robot_shop") or {}
    rows = [r for r in rs.get("rows") or [] if (r.get("hand_person_h") or 0) + (r.get("shop_person_h") or 0) > 0.05]
    if not rows:
        return note_slide("The machining time estimates (hud.json) were not ready for this cut")
    rows = rows[::-1]
    fig, ax = fig_axes([0.36, 0.10, 0.58, 0.74])
    s = ease(u)
    hand_col, shop_col = "#7f8a96", common.WHO_COL["robot A"]
    for k, r in enumerate(rows):
        a, b = float(r.get("hand_person_h") or 0), float(r.get("shop_person_h") or 0)
        ax.barh(k + 0.19, a * s, height=0.36, color=hand_col, edgecolor=BG)
        ax.barh(k - 0.19, b * s, height=0.36, color=shop_col, edgecolor=BG)
        if u > 0.8:
            ax.text(a * s + 0.5, k + 0.19, f"{a:.1f}", va="center", fontsize=9, color=INK2)
            ax.text(b * s + 0.5, k - 0.19, f"{b:.1f}", va="center", fontsize=9, color=INK2)
    ax.set_yticks(range(len(rows)), [(r.get("step") or "")[:44] for r in rows], fontsize=11)
    ax.set_xlabel("person-hours")
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=hand_col, label="a person runs the machines"),
                       Patch(color=shop_col, label="the robot shop (a person programs, checks, welds)")],
              loc="lower right", frameon=False, fontsize=11)
    return to_img(fig)


def slide_assembly_hours(u, hud):
    """Robot-hours and person-hours of the assembly, by chapter (hud.json times.assembly rows)."""
    rows = ((hud.get("times") or {}).get("assembly") or {}).get("rows") or []
    if not rows:
        return note_slide("The assembly time estimates were not ready for this cut")
    by = {}
    for r in rows:
        ch = (r.get("chapter") or "other").split("-", 1)[-1].replace("-", " ")
        d = by.setdefault(ch, [0.0, 0.0])
        if (r.get("status") or "") != "machine" and (r.get("actor") or "") != "machine":    # T06: the pump's hour
            d[0] += float(r.get("robot_s") or 0) / 3600.0
        d[1] += float(r.get("person_min") or 0) / 60.0
    names = list(by)[::-1]
    fig, ax = fig_axes([0.30, 0.14, 0.62, 0.68])
    s = ease(u)
    for k, n in enumerate(names):
        rh, ph = by[n]
        ax.barh(k + 0.19, rh * s, height=0.36, color=common.WHO_COL["robot A"], edgecolor=BG)
        ax.barh(k - 0.19, ph * s, height=0.36, color=common.WHO_COL["person"], edgecolor=BG)
        if u > 0.8:
            ax.text(rh * s + 0.05, k + 0.19, f"{rh:.1f} h", va="center", fontsize=10, color=INK2)
            ax.text(ph * s + 0.05, k - 0.19, f"{ph:.1f} h", va="center", fontsize=10, color=INK2)
    ax.set_yticks(range(len(names)), names)
    ax.set_xlabel("hours (robots: the arms' recorded motions plus tool changes and docking; people: estimates)")
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=common.WHO_COL["robot A"], label="robots"),
                       Patch(color=common.WHO_COL["person"], label="people")], loc="lower right", frameon=False)
    return to_img(fig)


def _routes(route):
    """[(name, weeks [lo, hi] or None, cost [lo, hi] or None, person_h or None)] from route.json, whatever its keys."""
    out = []
    items = route.get("routes") if isinstance(route, dict) else route
    if isinstance(items, dict):
        items = [dict(name=k, **v) if isinstance(v, dict) else dict(name=k, value=v) for k, v in items.items()]
    for r in items or []:
        if not isinstance(r, dict):
            continue
        name = r.get("label") or r.get("name") or r.get("route") or "?"

        def pick(*keys):
            for k in keys:
                v = r.get(k)
                if v is None:
                    continue
                if isinstance(v, dict):
                    v = [v.get("low", v.get("lo")), v.get("high", v.get("hi"))]
                if isinstance(v, (int, float)):
                    return [float(v), float(v)]
                if isinstance(v, (list, tuple)) and len(v) and v[0] is not None:
                    return [float(v[0]), float(v[-1] if v[-1] is not None else v[0])]
            return None
        wk = pick("weeks", "calendar_weeks", "lead_weeks", "wk")
        if wk is None:
            d = pick("calendar_days", "days")
            wk = [d[0] / 7.0, d[1] / 7.0] if d else None
        cost = pick("cost_usd", "cost", "usd", "total_usd")
        ph = pick("person_h", "labour_h", "labor_h", "hours")
        out.append((name, wk, cost, ph))
    return out


def slide_routes(u, route):
    rows = _routes(route) if route else []
    rows = [r for r in rows if r[1] or r[2]]
    if not rows:
        return note_slide("Time and cost by route (route.json) were not ready for this cut",
                          "In-house, outsourced, hybrid and robot shop: see desktop-lpbf/robot-build/ when they land")
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    s = ease(u)
    names = [r[0] for r in rows][::-1]
    for j, (idx, xlabel, fmt) in enumerate(((1, "calendar weeks to a working machine", lambda v: f"{v:.0f} wk"),
                                            (2, "cost of the machine by this route (USD)", money_k))):
        ax = fig.add_axes([0.20 + j * 0.42, 0.12, 0.33, 0.70])
        ax.set_facecolor(BG)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        vals = [r[idx] for r in rows][::-1]
        for k, v in enumerate(vals):
            if not v:
                continue
            col = common.WHO_COL["robot A"] if "robot" in names[k].lower() else "#7f8a96"
            ax.barh(k, v[0] * s, height=0.55, color=col, edgecolor=BG)
            ax.barh(k, (v[1] - v[0]) * s, left=v[0] * s, height=0.55, color=col, alpha=0.4, edgecolor=BG)
            if u > 0.8:
                ax.text(v[1] * s, k, "  " + (fmt(v[0]) if abs(v[1] - v[0]) < 1e-6 else f"{fmt(v[0])}-{fmt(v[1])}"),
                        va="center", fontsize=10, color=INK2)
        ax.set_yticks(range(len(names)), names if j == 0 else [""] * len(names))
        ax.set_xlabel(xlabel)
        mx = max((v[1] for v in vals if v), default=1.0)
        ax.set_xlim(0, mx * 1.45)
        if idx == 2:
            ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
        ax.grid(axis="x", color=GRID)
        ax.set_axisbelow(True)
    return to_img(fig)


def _steps(kind):
    """[(id, what, why)] of the steps whose status is `kind` ("person" or "redesign") in the workers' summaries."""
    out = []
    for name in ("assembly.json", "shop.json"):
        d = load(name)
        if not d:
            continue
        for s in d.get("steps") or []:
            st = (s.get("status") or "").lower()
            who = s.get("who") or []
            if st == kind or (kind == "person" and st == "" and "person" in who and len(who) == 1):
                out.append((s.get("id", ""), s.get("label", ""), s.get("why", "")))
        for r in d.get("redesigns" if kind == "redesign" else "person_steps") or []:
            if isinstance(r, dict):
                out.append((r.get("id", ""), r.get("label") or r.get("what", ""), r.get("why", "")))
            else:
                out.append(("", str(r), ""))
    if kind == "person":
        for sid, what, why in (("T01", "Process module (84 kg) onto the VLM tray", "3.4 x two UR12e payloads: lift table"),
                               ("T02", "Rack units: UPS 23 kg, laser 40 kg", "over the 12.5 kg payload: lift"),
                               ("T03", "Gas module: scroll pump 26 kg", "over the payload: lift"),
                               ("T04", "KF bellows, argon and O2 lines", "deformable hoses, wing-nut clamps"),
                               ("T05", "Tray dock and umbilicals", "cable and hose routing")):
            out.append((sid, what, why))
    return out


def slide_list(u, kind):
    rows = _steps(kind)
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    if not rows:
        fig.text(0.5, 0.5, "None recorded in this cut" if kind == "redesign" else "No person steps recorded",
                 ha="center", fontsize=22, color=INK)
        return to_img(fig), 0
    n_show = min(len(rows), 16)
    shown = int(math.ceil(n_show * ease(u * 1.3)))
    col_w = 0.47
    for k, (sid, what, why) in enumerate(rows[:shown]):
        c, r = k // 8, k % 8
        x, y = 0.04 + c * (col_w + 0.02), 0.82 - r * 0.093
        fig.text(x, y, sid, fontsize=12, color=common.WHO_COL["person"] if kind == "person" else common.COL["redesign"],
                 weight="bold", family="DejaVu Sans Mono")
        fig.text(x + 0.055, y, (what[:58] + "...") if len(what) > 60 else what, fontsize=12, color=INK)
        if why:
            fig.text(x + 0.055, y - 0.032, (why[:72] + "...") if len(why) > 74 else why, fontsize=10, color=INK2)
    if len(rows) > n_show:
        fig.text(0.04, 0.06, f"... and {len(rows) - n_show} more (see desktop-lpbf/robot-build/)", fontsize=11, color=INK2)
    return to_img(fig), len(rows)


# ------------------------------------------------------------------------------------------------ the chapter
def main():
    ch = common.Chapter(NAME, TITLE)
    hud = load("hud.json") or {}
    route = load("route.json")
    base = dict(proc_s=0.0, no_clock=True, who=[])

    def run(make, caption, sub, hold_s=9.0, build_s=1.2):
        n_build = int(build_s * FPS)
        img = None
        for i in range(n_build):
            img = make(i / max(1, n_build - 1))
            ch.frame(img, caption, sub=sub, **base)
        img = make(1.0)
        for _ in range(int(hold_s * FPS)):
            ch.frame(img, caption, sub=sub, **base)

    img, n_ch = slide_clocks(1.0)
    run(lambda u: slide_clocks(u)[0], "What the video's clocks add up to",
        f"Real time for the robots' motions, time-lapse for machining and waiting; summed over {n_ch} chapters", 8.0)
    tot = (hud.get("totals") or {}).get("scenarios") or {}
    if tot.get("new") and tot.get("used"):
        cap = (f"The kit: ${tot['new'][0] / 1000:.0f}k-{tot['new'][1] / 1000:.0f}k new, "
               f"${tot['used'][0] / 1000:.0f}k-{tot['used'][1] / 1000:.0f}k with used parts where it makes sense")
    else:
        cap = "The kit's cost by category, new against used"
    run(lambda u: slide_cost(u, hud), cap, "Most of the saving is the laser chain and the gas module; "
        "prices from bom.csv and eBay / surplus listings (hud.json, cost/used-options.csv)", 10.0)
    sch = ((hud.get("lead_times") or {}).get("schedule") or {}).get("routes") or {}
    if sch.get("new") and sch.get("used"):
        cap = (f"Every part in hand: {sch['new']['parts_in_hand_wk'][1]:.0f} weeks as chosen, "
               f"{sch['used']['parts_in_hand_wk'][1]:.0f} with the majors bought used")
    else:
        cap = "When every part is in hand, by how it is bought"
    run(lambda u: slide_lead(u, hud), cap, "The slowest parts are not the laser: a guard switch (27 wk) and a "
        "temperature relay (19 wk) have stocked swaps (hud.json lead_times)", 10.0)
    rs = (hud.get("times") or {}).get("robot_shop") or {}
    if rs.get("total_hand_person_h"):
        cap = (f"Making the custom parts: {rs['total_hand_person_h']:.0f} person-hours by hand, "
               f"{rs.get('total_shop_person_h', 0):.0f}-{rs.get('total_shop_person_h_cautious', 0):.0f} with the robot shop")
        sub = (f"{rs.get('n_parts', '')} parts, {rs.get('setups', '')} setups; the spindle time ({rs.get('cut_h', 0):.0f} h) "
               "is the same either way; the arms take the setups and flips (hud.json, robot-shop.md)")
    else:
        cap, sub = "Making the custom parts: person-hours, by hand against the robot shop", "hud.json times.robot_shop"
    run(lambda u: slide_shop_hours(u, hud), cap, sub, 10.0)
    arows = ((hud.get("times") or {}).get("assembly") or {}).get("rows") or []
    if arows:
        rh = sum(float(r.get("robot_s") or 0) for r in arows
                 if (r.get("status") or "") != "machine" and (r.get("actor") or "") != "machine") / 3600.0
        ph = sum(float(r.get("person_min") or 0) for r in arows) / 60.0
        cap = f"Assembly: {rh:.1f} robot-hours and {ph:.1f} person-hours over {len(arows)} steps"
    else:
        cap = "Assembly: robot-hours and person-hours"
    run(lambda u: slide_assembly_hours(u, hud), cap, "The arms' time is their recorded, collision-checked motions plus "
        "tool changes and docking; a person's time is an estimate per step (hud.json times.assembly)", 9.0)
    run(lambda u: slide_routes(u, route), "Time and cost by route: in-house, outsourced, hybrid, robot shop",
        "route.json (the route worker): labour, services and calendar time for each way of making the custom parts", 10.0)
    _, n_p = slide_list(1.0, "person")
    run(lambda u: slide_list(u, "person")[0], f"Where a person is needed: {n_p} steps",
        "Heavy lifts over the UR12e's 12.5 kg, deformable seals and hoses, and the welding and honing", 10.0)
    _, n_r = slide_list(1.0, "redesign")
    run(lambda u: slide_list(u, "redesign")[0], f"What had to be redesigned for the arms: {n_r}",
        "Steps the arms failed until a part, a fixture or a tool changed (assembly and shop summaries)", 8.0)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
