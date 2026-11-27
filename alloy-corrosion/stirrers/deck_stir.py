"""The copper deck with four compact stir modules in a column, and the two tip racks side by side.

Asked for by Ben on #180 (2026-11-06): put four of byu-vcl#269's stir modules in a line along Y
where the left tip rack (P11) was planned, and move that rack next to his rack 1, so the pipette
tip never passes over a capped vial. On the stir module a vial stands so high that a tipped
pipette doesn't clear its cap (Ben, byu-vcl#269, 2026-11-05).

Two checks, both in plan, in the CubOS deck frame of Ben's 2026-10-02 calibration
(origin front-left-bottom, +X right, +Y away from the operator, mm). Every position is a
proposal to teach on the deck, not a measurement.

1. The rigid-head rule of ../plot_deck_layout.py, through ../copper/deck_cu.py, with the stirrers
   added: for every tool-down event, what the other tool lands on.
2. The moves themselves. CubOS's driver moves X first, then Y, then Z
   (byu-vcl cubos/tools/capped_vial_keepout.py). So a move ends with a Y leg along the
   destination's X. A move into the stirrer column therefore runs along the column, over the
   other stirred vials, unless it starts in the destination vial's own row. This walks one well
   fill per stirred stock and well, with and without a staging move, and measures how close the
   tip (while a tip is on) and the carried vial cap (while the capper holds one) come to every
   capped stirred vial.

    python deck_stir.py      # writes deck-stir-check.json and deck-stir.png
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("deck_cu", HERE.parent / "copper" / "deck_cu.py")
cu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cu)
base = cu.base

# --- the new deck -------------------------------------------------------------------------------
# Stirrer column. Compact stir modules (49 x 44 mm) sit on the PandaDeck slot grid, 25 mm in X and
# 45 mm in Y, two keys in adjacent slot columns. Ben taught the first one's vial at (126, 45)
# (byu-vcl cubos/configs/deck/stir_module_trial.yaml), so two slot pairs further left is x 76.
# At x 101 the capper would sit on stirrer A whenever the pipette fills a tube at x 176.
STIR_X = 76.0
STIR_Y = [45.0, 90.0, 135.0, 180.0]
STIR_NAMES = ["A", "B", "C", "D"]
STIR_BASE = (49.0, 44.0)
STIR_BODY_TOP = 42.0           # base and vial holder, without the vial
STIR_RIM = 63.0 + 4.6          # seated rim 63 (byu-vcl#269 README) + the 4.6 mm spacer; Ben taught 66
STIR_CAP_TOP = STIR_RIM + 15.0  # the gantry file's engage depth; passive_shadow takes 13
STIR_DRAW_Z = STIR_RIM - 20.0  # aspirate at height -20, as stir_module_trial did, clear of the bar
CONTENTS = {
    "A": "ASW (D1141, no heavy metals)",
    "B": "ASW + 0.1 mg/L S",
    "C": "ASW + 10 mg/L S",
    "D": "spare: FeSO4 on non-sulfide nights, or a fourth electrolyte",
}

# Tip rack 2 (P11) moves next to Ben's rack 1, one slot column (25 mm) to its left.
TIP_RACK_2 = {"a1": (291.332 - 25.0, 89.0), "a2": (282.832 - 25.0, 89.0), "pickup_z": 59.0}

# The 9-position holder keeps only the two stocks that need no stirring, at its front positions.
# From y 101 back, drawing from it puts the capper over tip rack 2 (x 252-272, y 85-212).
HOLDER_STOCKS = {"DI water": (cu.HOLDER_X, cu.HOLDER_Y[0]), "1 M HNO3, trace metal": (cu.HOLDER_X, cu.HOLDER_Y[1])}

# Staging: before a tipped pipette, or a capper carrying a vial cap, goes back to stirred vial k,
# send the pipette to (STIR_X + 95, y_k + 11). That puts the capper at (STIR_X + 40, y_k), in the
# vial's own row and clear of the column, so the next move comes in along X.
STAGE_DX, STAGE_DY = 95.0, 11.0

TIP_KEEPOUT = 24.0   # tip axis to a capped vial's axis: 14 mm vial radius + 10 mm, as capped_vial_keepout.py
CAP_R = 14.0         # a carried vial cap, and a stirred vial's cap, in plan
CAP_KEEPOUT = 2 * CAP_R  # carried cap to a capped vial: no overlap in plan

WELLS = {f"S{i}": (x, base.STATION_Y) for i, x in enumerate(base.STATION_X[:3], start=1)}  # S4 is the PTFE blank
TUBE = (base.TUBE_X[0], base.TUBE_Y[0])
TIP_WASTE = cu.TIP_WASTE["c"]
PIP = base.PIP_OFF


def stirred():
    return {n: (STIR_X, y) for n, y in zip(STIR_NAMES, STIR_Y)}


def stage(k):
    x, y = stirred()[k]
    return (x + STAGE_DX, y + STAGE_DY)


# --- check 1: the rigid-head rule, with the stirrers ---------------------------------------------
def apply_layout():
    cu.STOCKS = dict(HOLDER_STOCKS)
    cu.SPARE = {}
    cu.apply()
    base.TIP_RACK_2 = dict(TIP_RACK_2)
    cu_obstacles, cu_events = base.obstacles, base.events

    def obstacles():
        obs = list(cu_obstacles())
        w, h = STIR_BASE
        for n, (x, y) in stirred().items():
            obs.append((f"stirrer {n} body", "rect", (x - w / 2, y - h / 2, x + w / 2, y + h / 2), STIR_BODY_TOP))
            obs.append((f"stirred vial {n}", "circle", (x, y, base.VIAL_R), STIR_CAP_TOP))
        return obs

    def events():
        ev = list(cu_events())
        for n, (x, y) in stirred().items():
            tg = {f"stirred vial {n}", f"stirrer {n} body"}
            ev.append((f"pipette draws stirred vial {n}", "pipette", (x, y), STIR_DRAW_Z, tg, "capper", base.ALL_CAPS))
            # the copper fill opens each stock with the tip already on, so check the tipped pipette too
            ev.append((f"capper decaps stirred vial {n}, tip on", "capper", (x, y), STIR_CAP_TOP, tg, "pipette", base.ALL_CAPS))
            ev.append((f"capper decaps stirred vial {n}, bare", "capper", (x, y), STIR_CAP_TOP, tg, "pipette_bare", base.ALL_CAPS))
        return ev

    base.obstacles, base.events = obstacles, events


# --- check 2: the moves -------------------------------------------------------------------------
def legs(g0, g1):
    """The gantry's X leg, then its Y leg, from g0 to g1 (both are capper positions)."""
    mid = (g1[0], g0[1])
    return [(g0, mid), (mid, g1)]


def seg_dist(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((cx - ax) * dx + (cy - ay) * dy) / L2))
    return math.hypot(ax + t * dx - cx, ay + t * dy - cy)


def fill(k, well, n_transfers, staged, decap_first=False):
    """One well fill from stirred stock k: the moves, as (label, gantry target, tip_on, cap_held).

    decap_first: open the stock before the tip goes on (as stir_module_trial did), so the
    pipette comes to the vial straight from the tip rack."""
    vx, vy = stirred()[k]
    rack_a1 = TIP_RACK_2["a1"]
    g = lambda p, tool: (p[0] - PIP[0], p[1] - PIP[1]) if tool == "pipette" else p  # noqa: E731
    seq = []
    if decap_first:
        seq += [("decap " + k, g((vx, vy), "capper"), False, True),
                ("pick up tip", g(rack_a1, "pipette"), True, True)]
    else:
        seq += [("pick up tip", g(rack_a1, "pipette"), True, False),
                ("decap " + k, g((vx, vy), "capper"), True, True)]
    first = True
    for i in range(n_transfers):
        if staged and not (first and not decap_first):
            seq.append((f"stage {k}", g(stage(k), "pipette"), True, True))
        seq.append((f"aspirate {k} #{i + 1}", g((vx, vy), "pipette"), True, True))
        seq.append((f"dispense {well} #{i + 1}", g(WELLS[well], "pipette"), True, True))
        first = False
    if staged:
        seq.append((f"stage {k}", g(stage(k), "pipette"), True, True))
    seq.append(("cap " + k, g((vx, vy), "capper"), True, False))
    seq.append(("drop tip", g(TIP_WASTE, "pipette"), False, False))
    return seq


def walk(seq, open_vial):
    """Closest approach of the tip and of the carried cap to each capped stirred vial."""
    vials = stirred()
    home = (0.0, 0.0)
    worst = {"tip": (1e9, None, None), "carried cap": (1e9, None, None)}
    g0 = home
    tip_on = False
    for label, g1, tip_after, cap_held in seq:
        # the tip counts as on from the pick-up move on, as capped_vial_keepout.py counts it
        tip_now = tip_on or label == "pick up tip"
        for a, b in legs(g0, g1):
            for name, c in vials.items():
                if name == open_vial and cap_held:
                    continue  # its cap is on the capper: the vial is open
                if tip_now:
                    d = seg_dist((a[0] + PIP[0], a[1] + PIP[1]), (b[0] + PIP[0], b[1] + PIP[1]), c)
                    if d < worst["tip"][0]:
                        worst["tip"] = (d, label, name)
                if cap_held and not label.startswith("decap"):
                    d = seg_dist(a, b, c)
                    if d < worst["carried cap"][0]:
                        worst["carried cap"] = (d, label, name)
        tip_on = tip_after
        g0 = g1
    return {k: {"closest_mm": round(v[0], 1), "move": v[1], "capped_vial": v[2]} for k, v in worst.items()}


def move_check():
    rows = []
    for k in STIR_NAMES:
        for well in WELLS:
            for staged in (False, True):
                for decap_first in (False, True):
                    r = walk(fill(k, well, 8, staged, decap_first), k)
                    ok = r["tip"]["closest_mm"] >= TIP_KEEPOUT and r["carried cap"]["closest_mm"] >= CAP_KEEPOUT
                    rows.append({"stock": k, "well": well, "staged": staged, "decap_before_tip": decap_first,
                                 **r, "pass": ok})
    out = {}
    for staged in (False, True):
        sub = [r for r in rows if r["staged"] == staged]
        out["staged" if staged else "unstaged"] = {
            "fills": len(sub),
            "fills_passing": sum(r["pass"] for r in sub),
            "worst_tip": min(sub, key=lambda r: r["tip"]["closest_mm"])["tip"],
            "worst_carried_cap": min(sub, key=lambda r: r["carried cap"]["closest_mm"])["carried cap"],
        }
    return out, rows


# --- figure ------------------------------------------------------------------------------------
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#898781", "#e1e0d9", "#fcfcfb"
BLUE, ORANGE, AQUA, RED, GREEN = "#2a78d6", "#eb6834", "#1baf7a", "#c0392b", "#1e8449"


def tip_path(seq):
    pts, g0 = [], (0.0, 0.0)
    tip_on = False
    for label, g1, tip_after, _ in seq:
        if tip_on:  # from the tip rack on; the move to the rack is not drawn
            for a, b in legs(g0, g1):
                pts.append(((a[0] + PIP[0], a[1] + PIP[1]), (b[0] + PIP[0], b[1] + PIP[1])))
        tip_on = tip_after
        g0 = g1
    return pts


def draw(path_png):
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.6), dpi=130)
    titles = ["Without staging: back to stock A from well S2", "With a staging move first (STAGE A)"]
    for ax, staged, title in zip(axes, (False, True), titles):
        ax.set_facecolor(SURFACE)
        ax.add_patch(Rectangle((base.GANTRY["x"][0], base.GANTRY["y"][0]), base.GANTRY["x"][1], base.GANTRY["y"][1],
                               fill=False, ec=GRID, lw=1, ls="--"))
        x0, y0, x1, y1 = base.TRAY["rect"]
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#f3d9cc", ec=ORANGE, lw=1))
        for i, sx in enumerate(base.STATION_X, start=1):
            ax.add_patch(Circle((sx, base.STATION_Y), 8, fc="white", ec=ORANGE, lw=1))
            ax.text(sx, base.STATION_Y, f"S{i}", ha="center", va="center", fontsize=6.5)
        for rack, lab in ((base.TIP_RACK_1, "tip rack 1"), (TIP_RACK_2, "tip rack 2")):
            x0, y0, x1, y1 = base.rack_rect(rack)
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#dfe9f7", ec=BLUE, lw=1))
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, lab, ha="center", va="center", fontsize=6.5, color=BLUE, rotation=90)
        x0, y0, x1, y1 = base.TUBE_RACK["rect"]
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#eeeeee", ec=MUTED, lw=1))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, "tube rack", ha="center", va="center", fontsize=6.5)
        x0, y0, x1, y1 = cu.HOLDER_RECT
        ax.add_patch(Rectangle((x0, y0), x1 - x0, min(y1, 290) - y0, fc="#eeeeee", ec=MUTED, lw=1))
        for (n, (hx, hy)) in HOLDER_STOCKS.items():
            ax.add_patch(Circle((hx, hy), base.VIAL_R, fc="white", ec=BLUE, lw=1))
            ax.text(hx + 18, hy, n.split(",")[0], ha="left", va="center", fontsize=6)
        for (cn, (cx, cy)) in cu.CUPS.items():
            ax.add_patch(Circle((cx, cy), 13, fc="white", ec=MUTED, lw=1))
        ax.text(60, 262, "cups", ha="center", va="bottom", fontsize=6.5, color=MUTED)
        ax.add_patch(Circle(TIP_WASTE, 15, fc="white", ec=MUTED, lw=1))
        ax.text(TIP_WASTE[0], TIP_WASTE[1], "tip\nwaste", ha="center", va="center", fontsize=6)
        w, h = STIR_BASE
        for n, (sx, sy) in stirred().items():
            ax.add_patch(Rectangle((sx - w / 2, sy - h / 2), w, h, fc="#d8f1e6", ec=AQUA, lw=1))
            ax.add_patch(Circle((sx, sy), TIP_KEEPOUT, fc="none", ec=RED, lw=0.8, ls=":"))
            ax.add_patch(Circle((sx, sy), base.VIAL_R, fc="white", ec=AQUA, lw=1.2))
            ax.text(sx, sy, n, ha="center", va="center", fontsize=7, weight="bold")
            if staged:
                st = stage(n)
                ax.plot(*st, marker="x", color=GREEN, ms=5, mew=1.2)
                ax.text(st[0] + 3, st[1] + 2, f"stage {n}", fontsize=5.8, color=GREEN)
        seq = fill("A", "S2", 2, staged)
        col = GREEN if staged else RED
        for (a, b) in tip_path(seq):
            ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=col, lw=1.1, shrinkA=0, shrinkB=0))
        ax.set_xlim(-10, 420)
        ax.set_ylim(-10, 300)
        ax.set_aspect("equal")
        ax.set_xlabel("deck x, mm")
        ax.set_ylabel("deck y, mm")
        ax.set_title(title, fontsize=9.5, loc="left")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.text(0.01, 0.01, "Tip path (tip on), from the tip rack: decap A, two transfers A to S2, cap A, drop tip. CubOS moves X, "
             "then Y. Dotted red: 24 mm keep-out round each stirred vial while capped. Proposal; teach every position.",
             fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path_png)
    plt.close(fig)


def main():
    apply_layout()
    summary = base.check()
    moves, rows = move_check()
    problems = [r for r in summary["events"] if r["problems"]]
    result = {
        "layout": {
            "stirrers": {n: {"vial_xy": list(p), "holds": CONTENTS[n], "stage_xy": list(stage(n))} for n, p in stirred().items()},
            "stirrer_base_mm": STIR_BASE, "stirred_vial_rim_z": STIR_RIM, "stirred_cap_top_z": STIR_CAP_TOP,
            "tip_rack_1": base.TIP_RACK_1, "tip_rack_2": TIP_RACK_2,
            "tip_rack_2_rect": base.rack_rect(TIP_RACK_2),
            "holder_stocks": HOLDER_STOCKS,
        },
        "rigid_head_check": {k: v for k, v in summary.items() if k != "events"},
        "rigid_head_problems": problems,
        "move_check": moves,
        "move_check_keepouts_mm": {"tip": TIP_KEEPOUT, "carried cap": CAP_KEEPOUT},
        "move_check_fills": rows,
    }
    (HERE / "deck-stir-check.json").write_text(json.dumps(result, indent=1) + "\n")
    draw(HERE / "deck-stir.png")
    print(json.dumps({"rigid_head": {k: v for k, v in result["rigid_head_check"].items() if k in ("events_checked", "events_with_problems", "tightest_pass_mm")},
                      "problems": [(p["event"], p["problems"]) for p in problems],
                      "moves": moves}, indent=1))


if __name__ == "__main__":
    main()
