"""Chapter 15-estimates of the robot-built desktop LPBF video: the time estimates, right after the parts tour, so the scale
is known before the machining chapters (about 30 s).

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/ch_estimates.py

Three slides (2-D, matplotlib, through ch_summary.py's helpers; one message each, stated in the caption bar):
  1. making the custom parts: 287 shop hours, by activity (CAM, setups, cutting, deburr and inspection): the data
     worker's hud.json headline.machining_h (from analysis/out/machining/hours.csv, the 4th-axis plan);
  2. which route: BYU hours, cost and weeks to the first leak test for each way of making them: the route worker's
     route.json (routes; labour at BYU's $65/h); the robot shop's numbers are Edison's estimate and run off the scale;
  3. the assembly: steps, robot-hours, person-hours, the steps the arms failed and the person's steps: hud.json
     headline.assembly.
No project time passes here (proc_s 0; the clocks are hidden).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common  # noqa: E402
import ch_summary as S  # noqa: E402
from ch_summary import plt, matplotlib  # noqa: E402

FPS = common.FPS
NAME, TITLE = "15-estimates", "Time estimates: machining, routes, assembly"
ACT_COL = ["#257de0", "#f47230", "#00b894", "#f2a600"]      # the dataviz skill's first four slots, in order


def slide_machining(u, hud):
    m = (hud.get("headline") or {}).get("machining_h") or {}
    acts = [("CAM programming", m.get("cam")), ("setups (4th axis)", m.get("setups_4th")),
            ("cutting", m.get("cutting")), ("deburr and inspect", m.get("deburr_inspect"))]
    acts = [(n, float(v)) for n, v in acts if v]
    if not acts:
        return S.note_slide("The machining estimate (hud.json) was not ready for this cut")
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=S.BG)
    ax = fig.add_axes([0.06, 0.44, 0.88, 0.16])
    ax.set_axis_off()
    total = sum(v for _, v in acts)
    s = S.ease(u)
    x = 0.0
    for k, (n, v) in enumerate(acts):
        w = v * s
        ax.barh(0, w, left=x, height=0.8, color=ACT_COL[k], edgecolor=S.BG, linewidth=2)
        if u > 0.8:                                  # narrow segments alternate above and below the bar
            above = (k % 2 == 0) or v / total > 0.25
            ax.text(x + w / 2, 0.75 if above else -0.75, f"{n}\n{v:.0f} h", ha="center",
                    va="bottom" if above else "top", fontsize=13, color=S.INK)
        x += w
    ax.set_xlim(0, total * 1.02)
    ax.set_ylim(-1.9, 1.9)
    fig.text(0.06, 0.30, f"{total:.0f} h for {m.get('parts', '')} parts with the HRT210 4th axis "
             f"({m.get('three_axis', 0):.0f} h on three axes)", fontsize=15, color=S.INK)
    fig.text(0.06, 0.24, "CAM and setups are paid once; a second machine later adds 155 h, two together take 344 h "
             "(route.json)", fontsize=12, color=S.INK2)
    fig.text(0.06, 0.12, "Sources: analysis/out/machining/hours.csv, machining.md, hud.json, route.json",
             fontsize=10, color=S.INK2)
    return S.to_img(fig)


ROUTE_ORDER = [("a1", "All at BYU, 1 machinist"), ("a3", "All at BYU, shop shared 20 h/wk"),
               ("b_cn", "All outsourced (JLCCNC)"), ("b_us", "All outsourced (US shops)"),
               ("c_cn", "Hybrid (recommended)"), ("d", "Robot shop, first machine")]


def _pair(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return [float(v), float(v)]
    return [float(v[0]), float(v[-1])]


def slide_routes(u, route):
    R = (route or {}).get("routes") or {}
    rows = [(lab, R[k]) for k, lab in ROUTE_ORDER if k in R]
    if not rows:
        return S.note_slide("Time and cost by route (route.json) were not ready for this cut")
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=S.BG)
    s = S.ease(u)
    names = [r[0] for r in rows][::-1]
    specs = [("BYU person-hours", lambda r: _pair(r.get("labour_h")), lambda v: f"{v:,.0f}", " h"),
             ("cost, labour at $65/h (USD)", lambda r: _pair(r.get("total_usd_at_65")), S.money_k, ""),
             ("weeks to the first leak test", lambda r: _pair(r.get("weeks_to_leak_test")), lambda v: f"{v:.0f}", " wk")]
    for j, (xlabel, get, fmt, unit) in enumerate(specs):
        ax = fig.add_axes([0.25 + j * 0.255, 0.14, 0.20, 0.66])
        ax.set_facecolor(S.BG)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        vals = [get(r[1]) for r in rows][::-1]
        normal = [v[1] for n, v in zip(names, vals) if v and "Robot" not in n]
        cap = max(normal) * 1.35 if normal else 1.0
        for k, v in enumerate(vals):
            if not v:
                continue
            robot = "Robot" in names[k]
            col = common.WHO_COL["robot A"] if robot else ("#2a9d8f" if "Hybrid" in names[k] else "#8a949e")
            lo, hi = min(v[0], cap), min(v[1], cap)
            ax.barh(k, lo * s, height=0.6, color=col, edgecolor=S.BG)
            if hi > lo:
                ax.barh(k, (hi - lo) * s, left=lo * s, height=0.6, color=col, alpha=0.4, edgecolor=S.BG)
            if u > 0.8:
                a_, b_ = fmt(v[0]), fmt(v[1])
                txt = (a_ if a_ == b_ else f"{a_}-{b_}") + unit
                if v[1] > cap:
                    ax.text(cap * 0.98, k, txt + " >", ha="right", va="center", fontsize=9, color="white",
                            weight="bold")
                else:
                    ax.text(hi * s + cap * 0.02, k, txt, va="center", fontsize=9, color=S.INK2)
        ax.set_xlim(0, cap * 1.05)
        ax.set_yticks(range(len(names)), names if j == 0 else [""] * len(names), fontsize=11)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.tick_params(axis="x", labelsize=9)
        if j == 1:
            ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"\\${v / 1000:.0f}k"))
        ax.grid(axis="x", color=S.GRID)
        ax.set_axisbelow(True)
    fig.text(0.25, 0.04, "The robot shop runs off the scale (\">\"): Edison's estimate of commissioning the cell, "
             "and \\$329k of equipment.", fontsize=10, color=S.INK2)
    return S.to_img(fig)


def assembly_numbers(hud):
    """hud.json's assembly headline, with the robot-hours re-summed from times.assembly rows without the machine's
    (the leak check's pump hour is not robot time)."""
    a = dict((hud.get("headline") or {}).get("assembly") or {})
    rows = ((hud.get("times") or {}).get("assembly") or {}).get("rows") or []
    if rows:
        a["robot_h"] = sum(float(r.get("robot_s") or 0) for r in rows
                           if (r.get("status") or "") != "machine" and (r.get("actor") or "") != "machine") / 3600.0
    return a


def slide_assembly(u, hud):
    a = assembly_numbers(hud)
    if not a:
        return S.note_slide("The assembly estimate (hud.json) was not ready for this cut")
    tiles = [("Steps", f"{a.get('steps', 0)}", "in the build sequence"),
             ("Robots", f"{a.get('robot_h', 0):.1f}", (f"hours, + {a['mir_fetch_h']:.1f} h of MiR fetching"
                                                       if float(a.get("mir_fetch_h") or 0) >= 0.05 else
                                                       "hours, the MiRs' drives included")),
             ("People", f"{a.get('person_h', 0):.1f}", "hours (estimates per step)"),
             ("Failed or partial", f"{a.get('failed_or_partial', 0)}", "steps for the arms"),
             ("Person or shop", f"{a.get('person_or_shop_steps', 0)}", "steps")]
    fig = plt.figure(figsize=(common.W / 100, common.H / 100), dpi=100, facecolor=S.BG)
    for k, (name, val, unit) in enumerate(tiles):
        col, row = k % 3, k // 3
        x0, y0 = 0.06 + col * 0.305, 0.50 - row * 0.32
        al = S.ease(u * 1.6 - 0.1 * k)
        ax = fig.add_axes([x0, y0, 0.27, 0.26])
        ax.set_axis_off()
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="white", edgecolor="#cfd5db",
                                   alpha=0.9 * al))
        ax.text(0.06, 0.78, name.upper(), transform=ax.transAxes, fontsize=13, color=S.INK2, alpha=al, weight="bold")
        ax.text(0.06, 0.30, val, transform=ax.transAxes, fontsize=38, color=S.INK, alpha=al, weight="bold")
        ax.text(0.06, 0.10, unit, transform=ax.transAxes, fontsize=12, color=S.INK2, alpha=al)
    import textwrap
    note = ("Robot time: the arms' recorded, collision-checked motions plus tool changes and docking; "
            + str(a.get("basis", "")))
    fig.text(0.06, 0.15, "\n".join(textwrap.wrap(note, 150)[:2]), fontsize=11, color=S.INK2, va="top")   # round 9: wrapped
    return S.to_img(fig)


def main():
    ch = common.Chapter(NAME, TITLE)
    hud = S.load("hud.json") or {}
    route = S.load("route.json")
    base = dict(proc_s=0.0, no_clock=True, who=[])

    def run(make, caption, sub, hold_s=9.0, build_s=1.2):
        n_build = int(build_s * FPS)
        for i in range(n_build):
            ch.frame(make(i / max(1, n_build - 1)), caption, sub=sub, **base)
        img = make(1.0)
        for _ in range(int(hold_s * FPS)):
            ch.frame(img, caption, sub=sub, **base)

    m = (hud.get("headline") or {}).get("machining_h") or {}
    if m:
        cap = (f"Making the custom parts: {m.get('with_4th_axis', 0):.0f} shop hours: CAM {m.get('cam', 0):.0f}, "
               f"setups {m.get('setups_4th', 0):.0f}, cutting {m.get('cutting', 0):.0f}, "
               f"deburr and inspect {m.get('deburr_inspect', 0):.0f}")
    else:
        cap = "Making the custom parts: shop hours"
    run(lambda u: slide_machining(u, hud), cap, "The estimate behind the machining chapters' clocks (hud.json, "
        "machining.md); the chamber's frame and floor are 25 h of it (9 %)", 9.0)
    c = ((route or {}).get("routes") or {}).get("c_cn") or {}
    if c:
        cap = (f"The recommended hybrid route: {c.get('labour_h', 0):.0f} hours at BYU, "
               f"{c['weeks_to_leak_test'][0]:.0f}-{c['weeks_to_leak_test'][1]:.0f} weeks to the first leak test")
    else:
        cap = "Which route: BYU hours, cost and weeks to the first leak test"
    run(lambda u: slide_routes(u, route), cap, "Make the seal and module parts, buy 12 catalogue swaps, outsource the "
        "rest; set by the honing loop (route.json, manufacturing-route.md)", 10.0)
    a = assembly_numbers(hud)
    cap = (f"Assembly: {a.get('steps', '')} steps, {a.get('robot_h', 0):.1f} robot-hours and "
           f"{a.get('person_h', 0):.1f} person-hours") if a else "Assembly: robot-hours and person-hours"
    run(lambda u: slide_assembly(u, hud), cap, "What the next chapters show, step by step (hud.json from the assembly "
        "worker's run)", 8.0)
    ch.close()
    print(f"{NAME}: {ch.n} frames ({ch.n / FPS:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
