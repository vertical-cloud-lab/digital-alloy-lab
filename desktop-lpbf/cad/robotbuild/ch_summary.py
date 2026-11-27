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
  6. what had to be redesigned: the same files' "redesign" steps (and any "redesigns" list in them);
  7. Edison's estimate of the person-hours to commission the cell against building one machine by hand
     (desktop-lpbf/edison/r7-robot-build-review/answer.md section 5: its own estimates, not measurements), and a closing
     card: the video shows what the arms can physically do; it is not a claim that the cell pays for one machine.
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
    if not p.exists() and name == "assembly.json":    # round 9: the planner writes its run's summary as assembly_run<N>.json
        runs = sorted(common.DATA.glob("assembly_run*.json"),
                      key=lambda q: int("".join(c for c in q.stem if c.isdigit()) or 0))
        p = runs[-1] if runs else p
    if not p.exists() and name == "asm_fail_notes.json":   # the notes the assembly chapters draw (asm_render --fail_notes)
        p = common.LPBF / "analysis" / "out" / "assembly" / "run10_fail_notes.json"
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
    R_ = ((load("route.json") or {}).get("routes") or {})
    wk = (R_.get("c_cn") or {}).get("weeks_to_leak_test")
    tiles = [("Calendar", f"{wk[0]:.0f}-{wk[1]:.0f}" if wk else "-", "weeks, PO to first leak test (hybrid)"),
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
        sn, su = c.get("spec_new"), c.get("spec_used")
        if sn is not None:                                       # at spec: one new price, a used range
            n0 = n1 = float(sn if not isinstance(sn, list) else sn[0])
            u0, u1 = (su if isinstance(su, list) else [su, su]) if su is not None else (n0, n1)
        else:
            n0, n1 = c["new"]
            u0, u1 = (c.get("used") or c["new"])
        ax.barh(k + 0.18, n0 * s, height=0.32, color=NEW, edgecolor=BG, linewidth=1.0)
        ax.barh(k + 0.18, (n1 - n0) * s, left=n0 * s, height=0.32, color=NEW, alpha=0.40, edgecolor=BG, linewidth=1.0)
        ax.barh(k - 0.18, u0 * s, height=0.32, color=USED, edgecolor=BG, linewidth=1.0)
        ax.barh(k - 0.18, (u1 - u0) * s, left=u0 * s, height=0.32, color=USED, alpha=0.40, edgecolor=BG, linewidth=1.0)
        if u > 0.8 and n1 > 4000:
            ax.text(n1 * s + 400, k + 0.18, money_k(n0) if abs(n1 - n0) < 1 else f"{money_k(n0)}-{money_k(n1)}",
                    va="center", fontsize=10, color=INK2)
            if (u1 < n1 - 500):
                ax.text(u1 * s + 400, k - 0.18, money_k(u0) if abs(u1 - u0) < 1 else f"{money_k(u0)}-{money_k(u1)}",
                        va="center", fontsize=10, color=INK2)
    ax.set_yticks(y, names)
    ax.set_xlabel("USD at spec: the laser chain as specified, the cheapest listed option elsewhere (pale: the used range)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=NEW, label="new"), Patch(color=USED, label="used where sensible (eBay, surplus)")],
              loc="upper right", frameon=False, fontsize=12)
    return to_img(fig)


def slide_ready(u, hud):
    """Weeks from ordering to every part in hand, and to ready-to-assemble (fabrication included), by buying route."""
    wk = (hud.get("headline") or {}).get("weeks") or {}
    spec = [("All new, as chosen", wk.get("new_as_chosen"), "parts", "ready"),
            ("All new, two slow parts swapped", wk.get("new"), "parts", "ready_split"),
            ("Majors bought used", wk.get("used"), "parts", "ready_split")]
    rows = [(n, r[a], r[b], r.get("set_by", "")) for n, r, a, b in spec if r and r.get(a) and r.get(b)]
    if not rows:
        return slide_lead(u, hud)
    rows = rows[::-1]
    fig, ax = fig_axes([0.30, 0.16, 0.62, 0.66])
    s = ease(u)
    pc, rc = "#9dc8f7", NEW
    for k, (name, parts, ready, by) in enumerate(rows):
        for dy, (lo, hi), col in ((0.19, parts, pc), (-0.19, ready, rc)):
            ax.barh(k + dy, lo * s, height=0.36, color=col, edgecolor=BG)
            ax.barh(k + dy, (hi - lo) * s, left=lo * s, height=0.36, color=col, alpha=0.45, edgecolor=BG)
            if u > 0.8:
                ax.text(hi * s + 0.4, k + dy, f"{lo:.0f}-{hi:.0f} wk", va="center", fontsize=10, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlabel("weeks from ordering (BYU purchase orders included); fabrication on the recommended split")
    ax.set_xlim(0, max(r[2][1] for r in rows) * 1.25)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=pc, label="every part in hand"), Patch(color=rc, label="ready to assemble")],
              loc="lower right", frameon=False)
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


# Edison's review of the two-arm build (desktop-lpbf/edison/r7-robot-build-review/answer.md, section 5): person-hours,
# its own estimates "informed by published evidence, not a measured result"
EDISON = [("Commissioning before\nthe first machine", (1230.0, 2470.0), (140.0, 340.0)),
          ("Building the machine\n(machining, kitting, assembly)", (200.0, 380.0), (220.0, 400.0)),
          ("Total for one machine", (1430.0, 2850.0), (360.0, 740.0))]


def slide_edison(u):
    fig, ax = fig_axes([0.27, 0.14, 0.66, 0.68])
    s = ease(u)
    cell_col, hand_col = common.WHO_COL["robot A"], "#7f8a96"
    rows = EDISON[::-1]
    for k, (name, cell, hand) in enumerate(rows):
        for dy, (lo, hi), col in ((0.19, cell, cell_col), (-0.19, hand, hand_col)):
            ax.barh(k + dy, lo * s, height=0.36, color=col, edgecolor=BG)
            ax.barh(k + dy, (hi - lo) * s, left=lo * s, height=0.36, color=col, alpha=0.4, edgecolor=BG)
            if u > 0.8:
                ax.text(hi * s + 25, k + dy, f"{lo:,.0f}-{hi:,.0f} h", va="center", fontsize=10, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_xlabel("person-hours (Edison's estimate: solid to the low end, pale to the high end)")
    ax.set_xlim(0, 3400)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cell_col, label="the two-arm robot cell"), Patch(color=hand_col, label="by hand")],
              loc="lower right", frameon=False)
    return to_img(fig)


def slide_closing(u):
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=BG)
    a = ease(u * 1.5)
    lines = [("What this video is", 24, INK, "bold"),
             ("A feasibility study of what two UR12e arms on MiR250s can physically do: every arm motion shown", 15, INK, "normal"),
             ("is a collision-checked plan, and every step they can't do goes to a person.", 15, INK, "normal"),
             ("", 10, INK, "normal"),
             ("What it is not", 24, INK, "bold"),
             ("A claim that the cell pays for one machine. Edison's review puts commissioning the cell at 1,230-2,470", 15, INK, "normal"),
             ("person-hours, more than the 360-740 of building one by hand; it pays back only over 5-10 machines.", 15, INK, "normal"),
             ("", 10, INK, "normal"),
             ("Its recommendation: build the first machine mostly by hand, with the arms as material handlers", 15, INK2, "normal"),
             ("and CNC tenders on the long mill runs, and treat robot assembly as a testbed.", 15, INK2, "normal")]
    y = 0.80
    for text, size, col, w in lines:
        fig.text(0.07, y, text, fontsize=size, color=col, weight=w, alpha=a)
        y -= 0.062 if size < 20 else 0.075
    fig.text(0.07, 0.07, "Sources: desktop-lpbf/robot-build/ (this round's notes), desktop-lpbf/edison/r7-robot-build-review/answer.md",
             fontsize=10, color=INK2, alpha=a)
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
    if route and isinstance(route.get("routes"), dict) and any("labour_h" in v for v in route["routes"].values()):
        import ch_estimates                                     # the route worker's schema: the same chart as 15
        return ch_estimates.slide_routes(u, route)
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
            want = (kind,) if kind != "redesign" else ("redesign", "fail", "partial")
            if st in want or (kind == "person" and st == "" and "person" in who and len(who) == 1):
                out.append((s.get("id", ""), s.get("label", ""), s.get("why", "")))
        for r in d.get("redesigns" if kind == "redesign" else "person_steps") or []:
            if isinstance(r, dict):
                out.append((r.get("id", ""), r.get("label") or r.get("what", ""), r.get("why", "")))
            else:
                out.append(("", str(r), ""))
    if kind == "person":                                       # the shop's person lifts (shop.json)
        pl = (load("shop.json") or {}).get("person_lifts") or {}
        if isinstance(pl.get("lifts"), dict):                  # round 8: two-person lifts by hand, no lifter
            g = (pl.get("guideline") or {}).get("team_of_two_kg", 30.7)
            for name, r in pl["lifts"].items():
                if not isinstance(r, dict):
                    continue
                out.append(("shop", f"{r.get('caption') or name} ({float(r.get('kg', 0)):.1f} kg)",
                            f"two people by hand; guideline for two {g:.1f} kg (NIOSH 23 kg x 2 x 2/3, HSE L23)"))
        else:                                                  # round 7's format
            for name, r in pl.items():
                if isinstance(r, dict):
                    out.append(("shop", f"Chamber blank at the VF-4: {name}, {float(r.get('kg', 0)):.1f} kg",
                                "a person with the vacuum lifter on the jib (the shop worker's person lifts)"))
    if kind == "redesign":                                     # the assembly's failed steps and their round-7 fixes
        notes = load("asm_fail_notes.json") or {}
        have = {o[0] for o in out}
        asm = load("assembly.json") or {}
        failing = {s.get("id") for s in asm.get("steps") or [] if (s.get("status") or "").lower() in ("fail", "partial")}
        if asm.get("steps"):                                   # round 9: only the notes of steps that fail in this run
            notes = {k: v for k, v in notes.items() if k in failing}
        for sid, note in notes.items():
            if sid in have:
                out = [o for o in out if o[0] != sid]
            what, _, fix = str(note).partition("Round 7:")
            out.append((sid, "Failed: " + what.strip().rstrip("."), ("Fix: " + fix.strip()) if fix else ""))
        # the shop worker's summary keeps each chapter's clips in "clips_in_chapters" ("chapters" holds the chapter totals)
        shop = load("shop.json") or {}
        for chname, clips in (shop.get("clips_in_chapters") or {}).items():
            for clip, c in clips.items():
                if isinstance(c, dict) and "fail" in (c.get("status") or []):
                    out.append(("shop", f"{clip} ({chname}): failed for the arm", "shown with its fix in that chapter"))
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
    hl = hud.get("headline") or {}
    sp, bom, cw = hl.get("cost_at_spec") or {}, (hl.get("cost_bom_range") or {}).get("new"), hl.get("cw_chain") or {}
    if sp.get("new") and sp.get("used"):
        cap = (f"The machine at spec: ${sp['new'] / 1000:.1f}k new, ${sp['used'][0] / 1000:.1f}k-{sp['used'][1] / 1000:.1f}k "
               "with used parts where it makes sense")
        sub = ((f"The laser chain alone: ${cw['new'] / 1000:.1f}k new, ${cw['used'][0] / 1000:.1f}k-"
                f"{cw['used'][1] / 1000:.1f}k used. " if cw.get("new") else "") +
               (f"BOM range, cheapest to premium option on every line: ${bom[0] / 1000:.1f}k-{bom[1] / 1000:.1f}k new"
                if bom else ""))
    else:
        cap, sub = "The kit's cost by category, new against used", "hud.json"
    run(lambda u: slide_cost(u, hud), cap, sub, 10.0)
    wk = hl.get("weeks") or {}
    if (wk.get("new") or {}).get("ready_split") and (wk.get("used") or {}).get("ready_split"):
        a, b = wk["new"]["ready_split"], wk["used"]["ready_split"]
        cap = f"Ready to assemble: {a[0]:.0f}-{a[1]:.0f} weeks bought new, {b[0]:.0f}-{b[1]:.0f} with the majors used"
        sub = ("Bought new, the laser sets the date; bought used, fabrication does. As chosen, a $123 guard switch "
               "(27 wk) would set it: swap it and the K8DT relay for stocked parts")
    else:
        cap, sub = "When every part is in hand, by how it is bought", "hud.json lead_times"
    run(lambda u: slide_ready(u, hud), cap, sub, 10.0)
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
    R = (route or {}).get("routes") or {}
    if all(k in R for k in ("b_cn", "c_cn", "d")):
        cap = (f"Routes: outsourced costs least (\u0024{R['b_cn']['total_usd_at_65'][0] / 1000:.0f}k), the hybrid is "
               f"recommended (\u0024{R['c_cn']['total_usd_at_65'][0] / 1000:.0f}k, {R['c_cn']['labour_h']:.0f} BYU hours), "
               "the robot shop costs most")
    else:
        cap = "Time and cost by route: in-house, outsourced, hybrid, robot shop"
    run(lambda u: slide_routes(u, route), cap, "BYU hours, cost (labour at $65/h) and weeks to the first leak test for "
        "each way of making the custom parts (route.json, manufacturing-route.md)", 10.0)
    _, n_p = slide_list(1.0, "person")
    run(lambda u: slide_list(u, "person")[0], f"Where a person is needed: {n_p} steps",
        "Heavy lifts over the UR12e's 12.5 kg, deformable seals and hoses, and the welding and honing", 10.0)
    _, n_r = slide_list(1.0, "redesign")
    run(lambda u: slide_list(u, "redesign")[0], f"Where the arms failed or a part was redesigned: {n_r} steps",
        "Each failed step goes to a redesign (a part, a fixture or a tool) or to a person (assembly and shop summaries)",
        8.0)
    run(slide_edison, "Edison's estimate: for one machine, setting up the robot cell costs more than the build",
        "Commissioning: 1,230-2,470 person-hours (end-effectors, ~90 assembly programs, vision, safety, debugging) vs "
        "140-340 by hand; it pays back over 5-10 machines",
        11.0)
    run(slide_closing, "A feasibility study, not a business case",
        "The robots' part of this build is a testbed for skills that pay off if the lab builds more machines", 9.0)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
