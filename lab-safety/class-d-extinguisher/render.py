"""Renders for the Class D extinguisher install in 154 CB.

    xvfb-run -a python render.py out/          # everything
    xvfb-run -a python render.py out/ --fast   # stills only, no animation

Outputs: plan.png (floor plan, candidate spots, walking paths), elevation.png (mounting heights),
flag_bracket.png (the bent-plate sign bracket, flat pattern and bent), overview.png (3-D),
install.gif / install.mp4 (installation steps), distances.json, and the STEP files from model.py.
"""
from __future__ import annotations

import heapq
import json
import math
import os
import sys

import numpy as np

import model as M
from model import FT, IN

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "out"
FAST = "--fast" in sys.argv
os.makedirs(OUT, exist_ok=True)


# --------------------------------------------------------------------------------------------
# Walking distances on the plan (grid Dijkstra around walls and furniture)
# --------------------------------------------------------------------------------------------
CELL = 2 * IN
CLEAR = 9 * IN          # half a person's width


def obstacle_rects():
    """Footprints (x0, y0, x1, y1) in mm that a person cannot walk through."""
    R = []
    # room boundary (walls), with door gaps
    for w in "NSWE":
        gaps = sorted((M.DOORS[k]["a"] * FT, M.DOORS[k]["b"] * FT) for k in M.DOORS if M.DOORS[k]["wall"] == w)
        L = M.ROOM_W if w in "NS" else M.ROOM_D
        pos, segs = 0.0, []
        for a, b in gaps:
            segs.append((pos, a)); pos = b
        segs.append((pos, L))
        for a, b in segs:
            if w == "N": R.append((a, M.ROOM_D, b, M.ROOM_D + M.T_CMU))
            if w == "S": R.append((a, -M.T_CMU, b, 0))
            if w == "W": R.append((-M.T_CMU, a, 0, b))
            if w == "E": R.append((M.ROOM_W, a, M.ROOM_W + M.T_PART, b))
    R.append((0, 0, M.C158_X1 + M.T_PART, M.C158_Y1 + M.T_PART))
    R.append((M.COL_X0, M.COL_Y0, M.COL_X1, M.COL_Y1))
    for (x0, x1, y0, y1) in M.CHASES:
        R.append((x0, y0, x1, y1))
    d0, d1 = M.BOOTH_DOOR
    R.append((0, M.BOOTH_Y0, d0, M.BOOTH_Y0 + M.T_BOOTH))
    R.append((d1, M.BOOTH_Y0, M.BOOTH_X1 + M.T_BOOTH, M.BOOTH_Y0 + M.T_BOOTH))
    R.append((M.BOOTH_X1, M.BOOTH_Y0, M.BOOTH_X1 + M.T_BOOTH, M.ROOM_D))
    for p in M.equipment_parts():
        if p.name in ("mat",):
            continue
        bb = p.shape.BoundingBox()
        R.append((bb.xmin, bb.ymin, bb.xmax, bb.ymax))
    return R


def build_grid():
    x0, y0 = -M.T_CMU, -M.T_CMU
    nx = int((M.ROOM_W + M.T_PART - x0) / CELL) + 1
    ny = int((M.ROOM_D + M.T_CMU - y0) / CELL) + 1
    blocked = np.zeros((nx, ny), bool)
    xs = x0 + (np.arange(nx) + 0.5) * CELL
    ys = y0 + (np.arange(ny) + 0.5) * CELL
    for (a, b, c, d) in obstacle_rects():
        ix = (xs > a - CLEAR) & (xs < c + CLEAR)
        iy = (ys > b - CLEAR) & (ys < d + CLEAR)
        blocked[np.ix_(ix, iy)] = True
    # outside the room is blocked except just through the door openings
    outside = (xs[:, None] < 0) | (xs[:, None] > M.ROOM_W) | (ys[None, :] < 0) | (ys[None, :] > M.ROOM_D)
    blocked |= outside
    return xs, ys, blocked


XS, YS, BLOCKED = build_grid()


def to_cell(p):
    return int(np.argmin(abs(XS - p[0]))), int(np.argmin(abs(YS - p[1])))


def path(p0, p1):
    """Shortest 8-connected path, returned as (length in ft, list of (x, y) mm)."""
    s, g = to_cell(p0), to_cell(p1)
    nx, ny = BLOCKED.shape
    dist = {s: 0.0}
    prev = {}
    pq = [(0.0, s)]
    steps = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2))]
    blocked = BLOCKED.copy()
    blocked[s] = blocked[g] = False
    while pq:
        d, c = heapq.heappop(pq)
        if c == g:
            break
        if d > dist.get(c, 1e18):
            continue
        for dx, dy, w in steps:
            n = (c[0] + dx, c[1] + dy)
            if not (0 <= n[0] < nx and 0 <= n[1] < ny) or blocked[n]:
                continue
            if dx and dy and (blocked[c[0] + dx, c[1]] or blocked[c[0], c[1] + dy]):
                continue
            nd = d + w
            if nd < dist.get(n, 1e18):
                dist[n] = nd; prev[n] = c
                heapq.heappush(pq, (nd, n))
    if g not in dist:
        return float("nan"), []
    pts, c = [], g
    while c != s:
        pts.append((XS[c[0]], YS[c[1]])); c = prev[c]
    pts.append((XS[s[0]], YS[s[1]]))
    pts = pts[::-1]
    # straighten: keep points where direction changes, then string-pull with line-of-sight checks
    def los(a, b):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) / (CELL / 2)) + 2
        for t in np.linspace(0, 1, n):
            c_ = to_cell((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            if blocked[c_]:
                return False
        return True
    out = [pts[0]]
    i = 0
    while i < len(pts) - 1:
        j = len(pts) - 1
        while j > i + 1 and not los(pts[i], pts[j]):
            j -= 1
        out.append(pts[j]); i = j
    length = sum(math.dist(out[k], out[k + 1]) for k in range(len(out) - 1)) / FT
    return length, out


OPERATOR = (8.2 * FT, 27.0 * FT)              # on the mat, at the atomizer's chamber
SPOTS = {
    "L1 column, east face (recommended)": (M.AXIS_X + 20 * IN, M.MOUNT_Y),
    "L2 booth south wall, beside the curtain": (8.9 * FT, M.BOOTH_Y0 - 20 * IN),
    "L3 north CMU wall, east of the booth": (16.6 * FT, M.ROOM_D - 20 * IN),
    "existing CO2 by door 154-1 (not Class D)": (20 * IN, M.CO2_POS[1]),
}
EXITS = {
    "S door (main)": (12.1 * FT, 1.6 * FT),
    "door 154-1": (1.6 * FT, 15.8 * FT),
    "E door": (24.2 * FT, 18.0 * FT),
    "door 154-2": (21.4 * FT, 29.8 * FT),
}


def distances():
    res = {"operator_xy_ft": [OPERATOR[0] / FT, OPERATOR[1] / FT], "spots": {}}
    for k, p in SPOTS.items():
        d_op, pts = path(OPERATOR, p)
        e = {}
        for ek, ep in EXITS.items():
            d_ex, _ = path(p, ep)
            d_direct, _ = path(OPERATOR, ep)
            e[ek] = {"spot_to_exit_ft": round(d_ex, 1), "detour_ft": round(d_op + d_ex - d_direct, 1)}
        res["spots"][k] = {"from_atomizer_ft": round(d_op, 1), "path_mm": [[round(a), round(b)] for a, b in pts], "exits": e}
    return res


# --------------------------------------------------------------------------------------------
# 2-D drawings (matplotlib)
# --------------------------------------------------------------------------------------------
def plan_png(D):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Arc, Polygon, Circle

    f = 1 / FT
    fig, ax = plt.subplots(figsize=(9.5, 10.5), dpi=150)
    ax.set_aspect("equal")
    wall_c, part_c = "#6b6b6b", "#9a9a9a"

    def rect(x0, y0, x1, y1, **kw):
        ax.add_patch(Rectangle((x0 * f, y0 * f), (x1 - x0) * f, (y1 - y0) * f, **kw))

    for (a, b, c, d) in obstacle_rects()[:0]:
        pass
    # walls
    for w in "NSWE":
        gaps = sorted((M.DOORS[k]["a"] * FT, M.DOORS[k]["b"] * FT) for k in M.DOORS if M.DOORS[k]["wall"] == w)
        L = M.ROOM_W if w in "NS" else M.ROOM_D
        pos, segs = (-M.T_CMU if w in "NS" else -M.T_CMU), []
        for a, b in gaps:
            segs.append((pos, a)); pos = b
        segs.append((pos, L + (M.T_PART if w in "NS" else M.T_CMU)))
        t = M.T_PART if w == "E" else M.T_CMU
        for a, b in segs:
            if w == "N": rect(a, M.ROOM_D, b, M.ROOM_D + t, color=wall_c)
            if w == "S": rect(a, -t, b, 0, color=wall_c)
            if w == "W": rect(-t, a, 0, b, color=wall_c)
            if w == "E": rect(M.ROOM_W, a, M.ROOM_W + t, b, color=part_c)
    # closet 158
    rect(0, 0, M.C158_X1 + M.T_PART, M.C158_Y1 + M.T_PART, facecolor="#e7e7e7", edgecolor=part_c, lw=2)
    ax.text((M.C158_X1 / 2) * f, (M.C158_Y1 / 2) * f, "158\n(closet, not lab)", ha="center", va="center", fontsize=8, color="#666")
    rect(M.COL_X0, M.COL_Y0, M.COL_X1, M.COL_Y1, color="#555")
    ax.annotate("column\n(18 in sq.)", ((M.COL_X0 + M.COL_X1) / 2 * f, M.COL_Y0 * f), (2.6, 17.6), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", color="#555", lw=0.8))
    for (x0, x1, y0, y1) in M.CHASES:
        rect(x0, y0, x1, y1, color=part_c)
    # door swings
    for k, d in M.DOORS.items():
        a, b = d["a"], d["b"]
        r = min(3.0, b - a - 0.15)
        w = d["wall"]
        if w == "S":
            hx, hy = (a + 0.08, 0) if d["hinge"] == "a" else (b - 0.08, 0)
            th0 = 0 if d["hinge"] == "a" else 90
            ax.add_patch(Arc((hx, hy), 2 * r, 2 * r, theta1=th0, theta2=th0 + 90, color="#8a6", lw=1))
            ax.plot([hx, hx], [hy, hy + r], color="#8a6", lw=1.5)
        if w == "N":
            hx = a + 0.08 if d["hinge"] == "a" else b - 0.08
            th0 = 270 if d["hinge"] == "a" else 180
            ax.add_patch(Arc((hx, M.ROOM_D * f), 2 * r, 2 * r, theta1=th0, theta2=th0 + 90, color="#8a6", lw=1))
            ax.plot([hx, hx], [M.ROOM_D * f, M.ROOM_D * f - r], color="#8a6", lw=1.5)
        if w == "W":
            hy = a + 0.08 if d["hinge"] == "a" else b - 0.08
            th0 = 0 if d["hinge"] == "a" else 270
            ax.add_patch(Arc((0, hy), 2 * r, 2 * r, theta1=th0, theta2=th0 + 90, color="#8a6", lw=1))
            ax.plot([0, r], [hy, hy], color="#8a6", lw=1.5)
        if w == "E":
            hy = b - 0.08 if d["hinge"] == "b" else a + 0.08
            xe = (M.ROOM_W + M.T_PART) * f
            th0 = 270 if d["hinge"] == "b" else 0
            ax.add_patch(Arc((xe, hy), 2 * r, 2 * r, theta1=th0, theta2=th0 + 90, color="#8a6", lw=1))
            ax.plot([xe, xe + r], [hy, hy], color="#8a6", lw=1.5)
        lx = {"S": ((a + b) / 2, -1.3), "N": ((a + b) / 2, M.ROOM_D * f + 1.1), "W": (-1.6, (a + b) / 2), "E": (M.ROOM_W * f + 1.7, (a + b) / 2)}[w]
        ax.text(*lx, k.replace(" (", "\n("), fontsize=7, ha="center", va="center", color="#476", rotation=90 if w in "WE" else 0)
    # booth
    d0, d1 = M.BOOTH_DOOR
    rect(0, M.BOOTH_Y0, M.BOOTH_X1 + M.T_BOOTH, M.ROOM_D, facecolor="#fff3e6", edgecolor="none", zorder=0)
    rect(0, M.BOOTH_Y0, d0, M.BOOTH_Y0 + M.T_BOOTH, color="#4a6a8a")
    rect(d1, M.BOOTH_Y0, M.BOOTH_X1 + M.T_BOOTH, M.BOOTH_Y0 + M.T_BOOTH, color="#4a6a8a")
    rect(M.BOOTH_X1, M.BOOTH_Y0, M.BOOTH_X1 + M.T_BOOTH, M.ROOM_D, color="#4a6a8a")
    ax.plot([d0 * f, d1 * f], [M.BOOTH_Y0 * f + 0.08] * 2, color="#7fb8d8", lw=3, ls=(0, (1, 1)))
    ax.text((d0 + d1) / 2 * f, M.BOOTH_Y0 * f + 0.55, "strip curtain", fontsize=7, ha="center", color="#2a5a7a")
    ax.text(0.4, M.ROOM_D * f - 0.6, "inert-gas booth (powder area)\n14 ft x 10.3 ft", fontsize=8.5, va="top", color="#a35a00", weight="bold")
    # equipment footprints
    for p in M.equipment_parts():
        bb = p.shape.BoundingBox()
        if p.name.startswith("bench leg") or p.name.startswith("cylinder rack") or p.name in ("atomizer furnace", "atomizer HMI", "existing CO2 horn"):
            continue
        col = "#%02x%02x%02x" % tuple(int(255 * c) for c in p.color)
        ax.add_patch(Rectangle((bb.xmin * f, bb.ymin * f), (bb.xmax - bb.xmin) * f, (bb.ymax - bb.ymin) * f,
                               facecolor=col, edgecolor="#333", lw=0.5, alpha=0.55 if p.name != "mat" else 0.35))
    labels = {"atomizer cabinet": "rePowder\natomizer", "induction module": "induction\nmodule", "white bench": "bench",
              "sit-stand desk": "desk", "ATEX vacuum": "ATEX\nvac", "argon cylinder": "Ar"}
    for p in M.equipment_parts():
        if p.name in labels:
            bb = p.shape.BoundingBox()
            ax.text((bb.xmin + bb.xmax) / 2 * f, (bb.ymin + bb.ymax) / 2 * f, labels[p.name], fontsize=6.5, ha="center", va="center",
                    color="white" if p.name in ("atomizer cabinet", "induction module", "argon cylinder") else "#222")
    # hazard ring
    ax.add_patch(Circle(((6.5 * FT + 20 * IN) * f, 28.0), 3.2, fill=False, ec="#e07000", lw=1.2, ls="--"))
    # paths
    pal = {"L1": "#1a9850", "L2": "#3a7dc0", "L3": "#8e44ad", "existing": "#c0392b"}
    for k, v in D["spots"].items():
        key = k.split()[0]
        pts = np.array(v["path_mm"]) * f
        ax.plot(pts[:, 0], pts[:, 1], color=pal[key], lw=2.2 if key == "L1" else 1.2, ls="-" if key == "L1" else "--", alpha=0.9)
    ax.plot(*np.array(OPERATOR) * f, "o", color="#e07000", ms=6)
    ax.text(OPERATOR[0] * f + 0.3, OPERATOR[1] * f - 0.6, "operator\nat chamber", fontsize=7, color="#a35a00")
    # spots
    star = dict(L1=(M.MOUNT_FACE_X + 4 * IN, M.MOUNT_Y))
    ax.plot(star["L1"][0] * f, star["L1"][1] * f, marker="*", color="#1a9850", ms=22, mec="k", mew=0.8, zorder=10)
    for k, (x, y, _) in M.ALTERNATES.items():
        key = k.split()[0]
        ax.plot(x * f, (y - 4 * IN if y > M.ROOM_D - 1 else y - 4 * IN) * f, marker="D", color=pal[key], ms=8, mec="k", mew=0.6, zorder=10)
    ax.plot(M.CO2_POS[0] * f + 0.35, M.CO2_POS[1] * f, marker="s", color="#c0392b", ms=7, mec="k", mew=0.6, zorder=10)
    txt = []
    for k, v in D["spots"].items():
        key = k.split()[0]
        txt.append(f"{k}: {v['from_atomizer_ft']:.0f} ft walk from the atomizer")
    ax.text(9.2, 9.0, "Walking distance (shortest path, 9 in clearance):\n" + "\n".join(txt) +
            "\nNFPA 10 limit for Class D: 75 ft. The whole room is inside it.", fontsize=7.2, va="top",
            bbox=dict(boxstyle="round", fc="white", ec="#bbb"))
    ax.annotate("L1 recommended:\ncolumn east face,\noutside the booth", (star["L1"][0] * f, star["L1"][1] * f), (9.6, 14.6), fontsize=8.5,
                color="#0d6b35", weight="bold", arrowprops=dict(arrowstyle="->", color="#1a9850", lw=1.3))
    ax.annotate("L2", (8.9, M.BOOTH_Y0 * f - 0.3), (8.6, 18.3), fontsize=8, color=pal["L2"], arrowprops=dict(arrowstyle="-", color=pal["L2"]))
    ax.annotate("L3", (16.6, M.ROOM_D * f - 0.3), (16.9, 28.6), fontsize=8, color=pal["L3"], arrowprops=dict(arrowstyle="-", color=pal["L3"]))
    ax.annotate("existing CO2\n(inferred spot;\nnever on metal fires)", (M.CO2_POS[0] * f + 0.4, M.CO2_POS[1] * f), (1.0, 21.9 - 2.6),
                fontsize=6.8, color="#c0392b", arrowprops=dict(arrowstyle="-", color="#c0392b"))
    # dims
    ax.annotate("", (0, -2.6), (M.ROOM_W * f, -2.6), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(M.ROOM_W * f / 2, -3.1, "25.78 ft", ha="center", fontsize=8)
    ax.annotate("", (M.ROOM_W * f + 3.0, 0), (M.ROOM_W * f + 3.0, M.ROOM_D * f), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(M.ROOM_W * f + 3.4, M.ROOM_D * f / 2, "31.38 ft", rotation=90, va="center", fontsize=8)
    ax.text(M.ROOM_W * f / 2 + 2, M.ROOM_D * f / 2 + 1.5, "154 CB", fontsize=14, color="#999", ha="center")
    ax.annotate("N", (M.ROOM_W * f + 2.2, M.ROOM_D * f + 2.2), (M.ROOM_W * f + 2.2, M.ROOM_D * f + 0.4), ha="center", fontsize=11, weight="bold",
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="k"))
    ax.set_xlim(-3, M.ROOM_W * f + 4.5)
    ax.set_ylim(-3.6, M.ROOM_D * f + 3)
    ax.set_xlabel("ft east of the west wall"); ax.set_ylabel("ft north of the south wall")
    ax.set_title("154 CB rebuilt from the BYU floor plan, with Class D candidate spots", fontsize=11)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "plan.png"))
    plt.close(fig)


def elevation_png():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon

    fig, axs = plt.subplots(1, 2, figsize=(11, 8), dpi=150, gridspec_kw=dict(width_ratios=[1.25, 1]))
    # --- front: looking west at the column's east face (v to the left is south... show v=-y to the right?)
    ax = axs[0]
    ax.set_aspect("equal")
    i = 1 / IN
    hw = (M.COL_Y1 - M.COL_Y0) / 2 * i
    # looking west, north is to the right
    ax.add_patch(Rectangle((-hw, 0), 2 * hw, 100, color="#cfcfcb"))
    ax.add_patch(Rectangle((hw, 0), 14, 96, color="#b8c3cd"))
    ax.text(hw + 7, 92, "booth S wall\n(runs toward you)", ha="center", va="top", fontsize=7, color="#345")
    ax.plot([-30, 30], [0, 0], color="k", lw=2)
    r = M.B570_BODY_D / 2 * i
    z0 = M.BOTTOM_Z * i
    bh = M.B570_BODY_H * i
    ax.add_patch(FancyBboxPatch((-r, z0), 2 * r, bh - r * 0.3, boxstyle="round,pad=0,rounding_size=2.5", fc="#f9cc0d", ec="k", lw=0.8))
    hz = M.HOOK_Z * i
    ax.add_patch(Rectangle((-0.8, z0 + bh), 1.6, hz - z0 - bh, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((-1.2, hz), 2.4, 0.4, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((-0.8, hz + 0.4), 1.6, 3.0, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((-0.6, M.TOP_Z * i - 0.6), 1.5, 0.6, fc="#999", ec="k", lw=0.6))
    ax.add_patch(Rectangle((-2.6, z0 + 9), 5.2, 10, fc="white", ec="#888", lw=0.5))
    ax.text(0, z0 + 14, "CLASS D\nNaCl\n30 lb", ha="center", va="center", fontsize=5.5)
    vs = -(M.B570_W - M.B570_BODY_D / 2) * i + 1.0      # applicator side (south = left when looking west)
    ax.add_patch(Rectangle((vs - 0.55, z0 + 6), 1.1, 22, fc="#222"))
    ax.add_patch(Polygon([[vs - 1.6, z0 + 2.5], [vs + 1.6, z0 + 2.5], [vs + 0.6, z0 + 6], [vs - 0.6, z0 + 6]], fc="#222"))
    tt = np.linspace(0, math.pi, 30)
    ax.plot(vs * (0.5 - 0.5 * np.cos(tt)), hz + 1.6 + 5 * np.sin(tt) - 4 * tt / math.pi, color="#222", lw=3)
    ax.plot([vs, vs], [z0 + 28, hz + 1.6 - 4], color="#222", lw=3)
    # bracket and screws
    zb = M.HOOK_PLATE_Z0 * i
    ax.add_patch(Rectangle((-1, zb), 2, M.HOOK_PLATE_H * i, fc="#c62828", ec="k", lw=0.6, zorder=5))
    for (v, z, d) in M.bracket_holes_local():
        ax.add_patch(plt.Circle((v * i, z * i), d * i * 0.9, fc="#ddd", ec="k", lw=0.5, zorder=6))
    # sign and flag
    ax.add_patch(Rectangle((-3.5, 60), 7, 10, fc="#f9cc0d", ec="k", lw=0.6))
    ax.text(0, 65, "CLASS D\nfor metal\nfires only", ha="center", va="center", fontsize=5.5, weight="bold")
    ax.add_patch(Rectangle((-3.0, 80), 3.0, 1.5, fc="#bbb", ec="k", lw=0.6))
    ax.text(-3.4, 80.7, "flag bracket\n(sticks out\ntoward you)", ha="right", va="center", fontsize=6.5)
    # dimension lines
    def dim(z, label, x=9.5, c="k", ls="-", dz=0.0):
        ax.plot([-hw - 1, x + 13], [z, z], color=c, lw=0.7, ls=ls)
        ax.text(x + 13.3, z + dz, label, va="center", fontsize=7.5, color=c)
    dim(42, "42 in: highest allowed top (NFPA 10, >40 lb)", c="#c0392b", ls="--", dz=1.3)
    dim(M.TOP_Z * i, f"{M.TOP_Z * i:.0f} in: top of extinguisher (lever)", c="#1a7a40", dz=-1.0)
    dim(M.HOOK_Z * i, f"{M.HOOK_Z * i:.1f} in: hook seat (collar)", c="#1a7a40")
    dim(M.bracket_holes_local()[0][1] * i, f"{M.bracket_holes_local()[0][1] * i:.1f} in: centre screw (1/4 in)", c="#555", ls=":", dz=0.6)
    dim(M.BOTTOM_Z * i, f"{M.BOTTOM_Z * i:.0f} in: bottom of extinguisher", c="#1a7a40", dz=1.0)
    dim(4, "4 in: lowest allowed bottom", c="#c0392b", ls="--", dz=-1.0)
    dim(60, "60-70 in: CLASS D sign, faces the booth door", c="#555", ls=":")
    dim(80, "80 in: flag sign, faces the room", c="#555", ls=":")
    ax.set_xlim(-16, 52); ax.set_ylim(-3, 96)
    ax.set_xlabel("in (looking west at the column's east face)"); ax.set_ylabel("in above the floor")
    ax.set_title("Front elevation at L1", fontsize=10)
    # --- side section
    ax = axs[1]
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((-18, 0), 18, 100, color="#cfcfcb"))
    ax.text(-9, 50, "column", rotation=90, ha="center", va="center", color="#666")
    ax.plot([-20, 30], [0, 0], color="k", lw=2)
    u0 = (M.STANDOFF + M.B570_BODY_D / 2) * i
    ax.add_patch(FancyBboxPatch((u0 - r, z0), 2 * r, bh - r * 0.3, boxstyle="round,pad=0,rounding_size=2.5", fc="#f9cc0d", ec="k", lw=0.8))
    hz = M.HOOK_Z * i
    ax.add_patch(Rectangle((u0 - 0.8, z0 + bh), 1.6, hz - z0 - bh, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((u0 - 1.2, hz), 2.4, 0.4, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((u0 - 0.8, hz + 0.4), 1.6, 3.0, fc="#ccc", ec="k", lw=0.6))
    ax.add_patch(Rectangle((u0 - 0.6, M.TOP_Z * i - 0.5), 6.1, 0.5, fc="#999", ec="k", lw=0.6))
    ax.add_patch(Rectangle((u0 - 0.6, hz + 3.4), 5.6, 0.5, fc="#999", ec="k", lw=0.6))
    # J hook profile: plate on the column, arm out under the collar flange, lip up in front
    t = 0.09
    ua = M.HOOK_REACH * i
    ax.add_patch(Rectangle((0, zb), t * 3, M.HOOK_PLATE_H * i, fc="#c62828", ec="k", lw=0.5, zorder=5))
    ax.add_patch(Rectangle((0, hz - t * 3), ua, t * 3, fc="#c62828", ec="k", lw=0.5, zorder=5))
    ax.add_patch(Rectangle((ua - t * 3, hz - t * 3), t * 3, 0.9, fc="#c62828", ec="k", lw=0.5, zorder=5))
    ax.add_patch(Rectangle((0, zb), t * 3, hz - zb, fc="#c62828", ec="k", lw=0.5, zorder=5))
    for z in [M.bracket_holes_local()[0][1] * i]:
        ax.add_patch(Rectangle((-1.75, z - 0.125), 1.75 + 0.3, 0.25, fc="#777", ec="k", lw=0.4, zorder=6))
    ax.text(-2.2, M.bracket_holes_local()[0][1] * i, "1/4 in x 1-3/4 in\nconcrete screw\n(1-1/4 in min. embed)", ha="right", va="center", fontsize=6.5)
    # flag bracket
    ax.add_patch(Rectangle((0, 80), 11, 1.5, fc="#bbb", ec="k", lw=0.6))
    ax.add_patch(Rectangle((2, 73), 10, 7, fc="#f9cc0d", ec="k", lw=0.6, alpha=0.8))
    ax.text(7, 76.5, "CLASS D", ha="center", va="center", fontsize=6.5, weight="bold")
    ax.add_patch(Rectangle((0, 60), 0.15, 10, fc="#f9cc0d", ec="k", lw=0.6))
    ax.annotate("", (0, 102 - 10), (u0 + r + 6.0, 102 - 10), arrowprops=dict(arrowstyle="<->", lw=0.6))
    ax.text((u0 + r + 6) / 2, 93.5, f"~{(u0 + r + 5.5):.0f} in out from the column", ha="center", fontsize=7)
    ax.set_xlim(-20, 30); ax.set_ylim(-3, 96)
    ax.set_xlabel("in, out from the column face (east)")
    ax.set_title("Side section at L1", fontsize=10)
    fig.suptitle("Amerex B570 (35 in tall, ~50 lb charged) on its wall hook: heights per NFPA 10 sec. 6.1.3.8", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "elevation.png"))
    plt.close(fig)


def flag_bracket_png():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    F = M.FLAG
    i = 1 / IN
    t, w = F["t"] * i, F["w"] * i
    # bend allowance, 90 deg, inside radius R, K = 0.33 (aluminium, air bend)
    R, K = F["bend_r"] * i, 0.33
    BA = math.pi / 2 * (R + K * t)
    setback = R + t
    a_flat = F["wall_leg"] * i - setback
    b_flat = F["flag_leg"] * i - setback
    L = a_flat + BA + b_flat
    fig, axs = plt.subplots(2, 1, figsize=(9, 5.2), dpi=150, gridspec_kw=dict(height_ratios=[1, 1.2]))
    ax = axs[0]
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), L, w, fc="#d9dde2", ec="k"))
    xb = a_flat + BA / 2
    ax.plot([xb, xb], [-0.3, w + 0.3], "k--", lw=0.8)
    ax.text(xb, w + 0.45, f"bend 90° here\n(R {R:.2f} in inside)", ha="center", fontsize=7)
    holes_flat = sorted(F["wall_leg"] * i - hh * i for hh in F["wall_holes"])
    sign_holes = [a_flat + BA + (hu - setback) for hu in [hh * i for hh in F["sign_holes"]]]
    for x in holes_flat + sign_holes:
        ax.add_patch(Circle((x, w / 2), F["hole_d"] * i / 2, fc="white", ec="k"))
    for x in holes_flat + sign_holes:
        ax.text(x, -0.5, f"{x:.2f}", ha="center", fontsize=6.5)
    ax.text(L / 2, -1.05, f"Flat pattern: 1/8 in x 1-1/2 in 6061 aluminium bar, cut to {L:.2f} in. Holes #7 drill (0.201 in) on the centreline, "
            "x from the wall-leg end.", ha="center", fontsize=7)
    ax.set_xlim(-0.6, L + 0.6); ax.set_ylim(-1.4, w + 1.2); ax.axis("off")
    ax = axs[1]
    ax.set_aspect("equal")
    # bent, seen from above (u right, v up): wall leg along -v at u=0, flag leg along +u
    ax.add_patch(Rectangle((-t, -F["wall_leg"] * i), t, F["wall_leg"] * i, fc="#bbb", ec="k"))
    ax.add_patch(Rectangle((-t, -t), F["flag_leg"] * i + t, t, fc="#bbb", ec="k"))
    ax.add_patch(Rectangle((-1.2, -4.0), 1.2 - t, 4.3, fc="#cfcfcb", ec="none"))
    ax.text(-0.65, -3.4, "column", rotation=90, ha="center", fontsize=7, color="#555")
    for hv in F["wall_holes"]:
        ax.plot([-1.0, 0.2], [-hv * i] * 2, color="#555", lw=1.5)
    ax.text(0.3, -2.9, "2x 3/16 in x 1-1/4 in\nconcrete screws", fontsize=7)
    ax.add_patch(Rectangle((2, -0.25 - t), 10, 0.06, fc="#f9cc0d", ec="k"))
    ax.text(7, -0.85, "7 x 10 in double-sided CLASS D sign, hung below on 2x #10-24 screws", ha="center", fontsize=7)
    ax.set_xlim(-1.5, 12.5); ax.set_ylim(-4.2, 1.0); ax.axis("off")
    ax.set_title("Bent (top view): wall leg on the column, flag leg out toward the room", fontsize=8)
    fig.suptitle("Optional prototyping-lab part: flag-sign bracket (2 holes per leg, one 90° bend)", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "flag_bracket.png"))
    plt.close(fig)
    return dict(cut_length_in=round(L, 2), bend_allowance_in=round(BA, 3), holes_from_wall_end_in=[round(x, 2) for x in holes_flat + sign_holes])


# --------------------------------------------------------------------------------------------
# 3-D (PyVista)
# --------------------------------------------------------------------------------------------
def to_pv(shape, tol=1.0, ang=0.25):
    import pyvista as pv
    v, t = shape.tessellate(tol, ang)
    pts = np.array([[p.x, p.y, p.z] for p in v])
    faces = np.hstack([[3, *tri] for tri in t]).astype(np.int64)
    return pv.PolyData(pts, faces)


def make_plotter(size=(960, 540)):
    import pyvista as pv
    pv.OFF_SCREEN = True
    pl = pv.Plotter(off_screen=True, window_size=size, lighting="three lights")
    pl.set_background("#f4f6f8", top="#dfe6ee")
    pl.enable_anti_aliasing("fxaa")
    return pl


def static_actors(pl, roof=M.ROOM_H, cut_SE=True):
    """Room, booth and equipment. With cut_SE the south and east walls are cut low (dollhouse view)."""
    A = {}
    parts = M.room_parts(roof) + M.booth_parts() + M.equipment_parts()
    for p in parts:
        mesh = to_pv(p.shape, tol=2.0)
        op = p.opacity
        if cut_SE and (p.name.startswith("wall S") or p.name.startswith("wall E") or p.name.startswith("closet") or p.name.startswith("chase")):
            mesh = mesh.clip("z", origin=(0, 0, 3.0 * FT), invert=True)
        if p.name.startswith("booth wall"):
            op = 0.38
        if p.name.startswith("door S") or p.name.startswith("door E"):
            mesh = mesh.clip("z", origin=(0, 0, 3.0 * FT), invert=True)
        A[p.name + f"#{len(A)}"] = pl.add_mesh(mesh, color=p.color, opacity=op, smooth_shading=True, split_sharp_edges=True, specular=0.1)
    return A


def install_meshes():
    """Local-frame meshes for the moving install parts (posed later by user_matrix)."""
    out = {}
    for k, s in M.b570_local().items():
        out[k] = (to_pv(s, tol=0.4), M.B570_COLORS[k])
    out["bracket"] = (to_pv(M.bracket_local(), tol=0.2), M.C_RED)
    for j, (v, z, d) in enumerate(M.bracket_holes_local()):
        out[f"screw{j}"] = (to_pv(M.screw_local(v, z, d, driven=1.0), tol=0.2), M.C_STEEL)
    out["sign"] = (to_pv(M.sign_local(), tol=0.5), M.C_YELLOW)
    out["flag"] = (to_pv(M.flag_bracket_local(), tol=0.2), M.C_ALU)
    out["flagsign"] = (to_pv(M.flag_sign_local(), tol=0.5), M.C_YELLOW)
    return out


def T(dx=0.0, dy=0.0, dz=0.0, rz=0.0, about=(0, 0, 0)):
    c, s = math.cos(math.radians(rz)), math.sin(math.radians(rz))
    R = np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    A = np.eye(4); A[:3, 3] = -np.array(about)
    B = np.eye(4); B[:3, 3] = np.array(about) + np.array([dx, dy, dz])
    return B @ R @ A


def world(local_T=np.eye(4)):
    W = np.eye(4); W[:3, 3] = [M.MOUNT_FACE_X, M.MOUNT_Y, 0]
    return W @ local_T


def overview_png(D):
    import pyvista as pv
    pl = make_plotter((1400, 900))
    static_actors(pl)
    for k, (mesh, col) in install_meshes().items():
        a = pl.add_mesh(mesh, color=col, smooth_shading=True, split_sharp_edges=True)
        a.user_matrix = world()
    pts = np.array(D["spots"]["L1 column, east face (recommended)"]["path_mm"], float)
    pts = np.c_[pts, np.full(len(pts), 30.0)]
    pl.add_mesh(pv.lines_from_points(pts).tube(radius=25), color="#1a9850")
    pl.add_point_labels([[M.MOUNT_FACE_X + 300, M.MOUNT_Y, 1500]], ["Class D here (L1)"], font_size=18, point_size=1,
                        shape_color="white", text_color="#0d6b35", always_visible=True)
    pl.add_point_labels([[7.5 * FT, M.ROOM_D - 600, 1900]], ["atomizer (powder hazard)"], font_size=16, point_size=1,
                        shape_color="white", text_color="#a35a00", always_visible=True)
    pl.camera_position = [(17.5 * FT, -4.0 * FT, 22 * FT), (8.5 * FT, 20 * FT, 2.0 * FT), (0, 0, 1)]
    pl.camera.view_angle = 38
    pl.screenshot(os.path.join(OUT, "overview.png"))
    pl.close()


def lerp(a, b, t):
    return tuple(np.array(a) * (1 - t) + np.array(b) * t)


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def animate(D, fps=10, size=(960, 540)):
    import pyvista as pv
    import imageio.v2 as imageio
    pl = make_plotter(size)
    static_actors(pl)
    meshes = install_meshes()
    acts = {k: pl.add_mesh(m, color=c, smooth_shading=True, split_sharp_edges=True) for k, (m, c) in meshes.items()}
    # ghost extinguisher
    ghost = {}
    for k in M.b570_local():
        g = pl.add_mesh(meshes[k][0], color="#9ad0a8", opacity=0.25)
        g.user_matrix = world(); ghost[k] = g
    # marks, holes, laser line, drill, clear zone, path, hazard glow, marker
    holes = M.bracket_holes_local()
    mark_acts, hole_acts = [], []
    for (v, z, d) in holes:
        cross = pv.Box(bounds=(1, 4, v - 18, v + 18, z - 1.2, z + 1.2)).merge(pv.Box(bounds=(1, 4, v - 1.2, v + 1.2, z - 18, z + 18)))
        a = pl.add_mesh(cross, color="k"); a.user_matrix = world(); mark_acts.append(a)
        hd = pv.Cylinder(center=(1.5, v, z), direction=(1, 0, 0), radius=d / 2 * 1.05, height=3, resolution=24)
        h = pl.add_mesh(hd, color="#1b1b1b"); h.user_matrix = world(); hole_acts.append(h)
    laser = pl.add_mesh(pv.Box(bounds=(1, 3, -230, 230, holes[0][1] - 1.5, holes[0][1] + 1.5)), color="#ff2020")
    laser.user_matrix = world()
    drill = pv.Cylinder(center=(-30 + 60, 0, 0), direction=(1, 0, 0), radius=0.09 * IN, height=4.5 * IN).merge(
        pv.Cylinder(center=(4.5 * IN + 30, 0, 0), direction=(1, 0, 0), radius=0.5 * IN, height=1.8 * IN)).merge(
        pv.Box(bounds=(5.4 * IN, 12.5 * IN, -1.4 * IN, 1.4 * IN, -1.6 * IN, 2.2 * IN))).merge(
        pv.Box(bounds=(9.0 * IN, 11.0 * IN, -0.8 * IN, 0.8 * IN, -7.5 * IN, -1.6 * IN)))
    drill_act = pl.add_mesh(drill, color="#d35400")
    zone = pv.Box(bounds=(0, 36 * IN, -18 * IN, 18 * IN, 0.5, 4))
    zone_act = pl.add_mesh(zone, color="#f1c40f", opacity=0.45); zone_act.user_matrix = world()
    pts = np.array(D["spots"]["L1 column, east face (recommended)"]["path_mm"], float)
    pts3 = np.c_[pts, np.full(len(pts), 35.0)]
    seglen = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    hazard = pl.add_mesh(pv.Box(bounds=(6.3 * FT, 6.5 * FT + 42 * IN, M.ROOM_D - 46 * IN, M.ROOM_D, 0, 66 * IN)), color="#ff7f00", opacity=0.18)
    marker = pl.add_mesh(pv.Cone(center=(0, 0, 0), direction=(0, 0, -1), height=320, radius=110, resolution=24), color="#1a9850")
    title = pl.add_text("", position="upper_left", font_size=12, color="#111111")
    sub = pl.add_text("", position="lower_left", font_size=9, color="#333333")

    path_act = [None]

    def set_path(frac):
        if path_act[0] is not None:
            pl.remove_actor(path_act[0]); path_act[0] = None
        if frac <= 0:
            return
        L = seglen[-1] * frac
        k = np.searchsorted(seglen, L)
        p = pts3[:max(k, 1)].tolist()
        if k < len(pts3):
            a, b = pts3[k - 1], pts3[k]
            t = (L - seglen[k - 1]) / max(seglen[k] - seglen[k - 1], 1e-6)
            p.append((a + (b - a) * t).tolist())
        if len(p) >= 2:
            path_act[0] = pl.add_mesh(pv.lines_from_points(np.array(p)).tube(radius=28), color="#1a9850")

    def vis(a, on):
        a.SetVisibility(bool(on))

    def ext_pose(Tl):
        for k in M.b570_local():
            acts[k].user_matrix = world(Tl)

    # camera keyframes: (position, focal, up)
    CAM_ROOM_A = [(26 * FT, -6 * FT, 26 * FT), (10 * FT, 18 * FT, 1 * FT), (0, 0, 1)]
    CAM_ROOM_B = [(15.5 * FT, -5 * FT, 20 * FT), (8.5 * FT, 21 * FT, 2 * FT), (0, 0, 1)]
    CAM_APPROACH = [(15.5 * FT, 13.0 * FT, 7.5 * FT), (7.0 * FT, 20.5 * FT, 3.0 * FT), (0, 0, 1)]
    CAM_FACE = [(M.MOUNT_FACE_X + 3.3 * FT, M.MOUNT_Y - 0.9 * FT, 3.4 * FT), (M.MOUNT_FACE_X, M.MOUNT_Y, 2.85 * FT), (0, 0, 1)]
    CAM_HANG = [(M.MOUNT_FACE_X + 6.0 * FT, M.MOUNT_Y - 3.2 * FT, 4.2 * FT), (M.MOUNT_FACE_X + 0.4 * FT, M.MOUNT_Y - 0.6 * FT, 2.3 * FT), (0, 0, 1)]
    CAM_SIGN = [(M.MOUNT_FACE_X + 7.0 * FT, M.MOUNT_Y - 5.5 * FT, 5.6 * FT), (M.MOUNT_FACE_X + 0.6 * FT, M.MOUNT_Y, 4.0 * FT), (0, 0, 1)]
    CAM_DOOR = [(12.4 * FT, 15.5 * FT, 5.4 * FT), (6.6 * FT, 20.6 * FT, 3.2 * FT), (0, 0, 1)]

    def cam(a, b, t):
        t = ease(t)
        pl.camera_position = [lerp(a[0], b[0], t), lerp(a[1], b[1], t), (0, 0, 1)]
        pl.camera.view_angle = 40

    steps = [
        ("1  Room 154 CB, rebuilt from the BYU floor plan",
         "Booth in the NW corner (orange: atomizer).\nGreen cone: recommended spot L1, the column just outside the booth.", 30),
        ("2  From the atomizer out through the curtain: 10 ft to L1",
         "On the way to door 154-1, in sight of the main door.\nNFPA 10 / OSHA allow up to 75 ft for Class D.", 30),
        ("3  Mark the column's east face: hook seat at 35.5 in",
         "Top then sits at 41 in (max 42 in for >40 lb),\nbottom at 6 in (min 4 in). Green ghost = final position.", 30),
        ("4  Drill three holes with a hammer drill",
         "3/16 in bit for the 1/4 in screw, 5/32 in for the 3/16 in ones.\nIf the column turns out to be steel: stop, use L2 (README).", 36),
        ("5  Screw on the Amerex wall hook (ships with the B570)",
         "1/4 x 1-3/4 in concrete screw in the centre hole,\n3/16 x 1-1/4 in in the two diagonal holes.", 30),
        ("6  Hang the B570 (~50 lb): lift with your legs",
         "Seat the collar in the hook, label out, applicator on the south side.\nPin and tamper seal intact, gauge in the green.", 40),
        ("7  Signs: CLASS D on the column, flag sign on the bent bracket",
         "Flat sign faces the curtain; flag sign faces the room.\n'CLASS D - combustible metals only'.", 30),
        ("8  Keep 36 x 36 in in front clear",
         "Monthly check on the tag, annual service by a contractor.\nView from the strip curtain on the way out.", 34),
    ]
    frames = []
    total = sum(s[2] for s in steps)
    f_global = 0
    # initial visibility
    for a in mark_acts + hole_acts:
        vis(a, False)
    vis(laser, False); vis(drill_act, False); vis(zone_act, False)
    for k in ("bracket", "screw0", "screw1", "screw2", "sign", "flag", "flagsign"):
        vis(acts[k], False)
    for g in ghost.values():
        vis(g, False)
    # extinguisher starts on the floor 3 ft in front of the column, turned
    FLOOR_DX, FLOOR_DY = 16 * IN, -40 * IN
    floor_T = T(dx=FLOOR_DX, dy=FLOOR_DY, dz=-M.BOTTOM_Z, rz=0)
    ext_pose(floor_T)
    acts["bracket"].user_matrix = world()
    for k in ("sign", "flag", "flagsign"):
        acts[k].user_matrix = world()
    for si, (ttl, sbt, n) in enumerate(steps):
        pl.remove_actor(title); title = pl.add_text(ttl, position="upper_left", font_size=15, color="#111111")
        pl.remove_actor(sub); sub = pl.add_text(sbt, position="lower_left", font_size=12, color="#222222")
        for f in range(n):
            t = f / max(n - 1, 1)
            pulse = 0.5 + 0.5 * math.sin(f_global * 0.6)
            marker.user_matrix = T(dx=M.MOUNT_FACE_X + 10 * IN, dy=M.MOUNT_Y, dz=8.6 * FT + 60 * pulse)
            vis(marker, si <= 1)
            hazard.prop.opacity = 0.12 + 0.18 * pulse if si <= 1 else 0.0
            if si == 0:
                cam(CAM_ROOM_A, CAM_ROOM_B, t)
                set_path(0)
            elif si == 1:
                cam(CAM_ROOM_B, CAM_APPROACH, t)
                set_path(min(1.0, t * 1.3))
            elif si == 2:
                if f == 0:
                    set_path(0)
                cam(CAM_APPROACH, CAM_FACE, t * 1.6)
                for g in ghost.values():
                    vis(g, t > 0.15)
                vis(laser, t > 0.35)
                for j, a in enumerate(mark_acts):
                    vis(a, t > 0.5 + 0.12 * j)
            elif si == 3:
                cam(CAM_FACE, CAM_FACE, 0)
                seg = n / 3
                j = min(int(f // seg), 2)
                tt = (f - j * seg) / seg
                v, z, d = holes[j]
                depth = 1.75 * IN
                inn = math.sin(math.pi * min(tt, 1.0))
                vis(drill_act, True)
                drill_act.user_matrix = world(T(dx=12 * IN * (1 - inn) - depth * inn * 0.9 + 4 * IN * 0, dy=v, dz=z))
                for jj in range(3):
                    vis(hole_acts[jj], jj < j or (jj == j and tt > 0.5))
                    vis(mark_acts[jj], not (jj < j or (jj == j and tt > 0.5)))
                if f == n - 1:
                    vis(drill_act, False)
                vis(laser, True)
            elif si == 4:
                vis(drill_act, False); vis(laser, False)
                for g in ghost.values():
                    vis(g, True)
                vis(acts["bracket"], True)
                slide = 1 - ease(min(t * 2.5, 1))
                acts["bracket"].user_matrix = world(T(dx=10 * IN * slide))
                for j in range(3):
                    tj = min(max((t - 0.35 - 0.2 * j) / 0.2, 0), 1)
                    vis(acts[f"screw{j}"], t > 0.35 + 0.2 * j)
                    acts[f"screw{j}"].user_matrix = world(T(dx=1.75 * IN * (1 - tj)))
                for a in hole_acts:
                    vis(a, t < 0.4)
            elif si == 5:
                for g in ghost.values():
                    vis(g, False)
                cam(CAM_FACE, CAM_HANG, t * 2)
                # lift: rise to 1.2 in above the seat, swing in, drop onto the hook
                if t < 0.45:
                    tt = ease(t / 0.45)
                    Tl = T(dx=FLOOR_DX * (1 - tt), dy=FLOOR_DY * (1 - tt), dz=-M.BOTTOM_Z * (1 - tt) + 1.2 * IN * tt)
                elif t < 0.8:
                    Tl = T(dz=1.2 * IN)
                else:
                    tt = ease((t - 0.8) / 0.2)
                    Tl = T(dz=1.2 * IN * (1 - tt))
                ext_pose(Tl)
            elif si == 6:
                cam(CAM_HANG, CAM_SIGN, t * 1.5)
                vis(acts["sign"], t > 0.15)
                acts["sign"].user_matrix = world(T(dx=6 * IN * (1 - ease(min((t - 0.15) / 0.3, 1)))))
                vis(acts["flag"], t > 0.45)
                vis(acts["flagsign"], t > 0.65)
                acts["flag"].user_matrix = world(T(dx=6 * IN * (1 - ease(min((t - 0.45) / 0.25, 1))) * 0))
            elif si == 7:
                vis(zone_act, True)
                zone_act.prop.opacity = 0.25 + 0.25 * pulse
                cam(CAM_SIGN, CAM_DOOR, t * 1.4)
            pl.render()
            img = pl.screenshot(return_img=True)
            frames.append(img)
            f_global += 1
    pl.close()
    # MP4 (sharp) and GIF (for GitHub)
    import imageio_ffmpeg  # noqa: F401
    mp4 = os.path.join(OUT, "install.mp4")
    with imageio.get_writer(mp4, fps=fps, codec="libx264", quality=8, macro_block_size=4, pixelformat="yuv420p") as w:
        for fr in frames:
            w.append_data(fr)
    from PIL import Image
    gif_frames = [Image.fromarray(fr).resize((size[0] * 3 // 4, size[1] * 3 // 4), Image.LANCZOS) for fr in frames]
    # palette from frames sampled across every step, so the yellow, red and green all get entries
    sample = gif_frames[:: max(1, len(gif_frames) // 16)]
    montage = Image.new("RGB", (sample[0].width, sample[0].height * len(sample)))
    for k, im in enumerate(sample):
        montage.paste(im, (0, k * sample[0].height))
    pal = montage.convert("P", palette=Image.ADAPTIVE, colors=192)
    q = [g.quantize(palette=pal, dither=Image.Dither.NONE) for g in gif_frames]
    gif = os.path.join(OUT, "install.gif")
    q[0].save(gif, save_all=True, append_images=q[1:], duration=int(1000 / fps), loop=0, optimize=True)
    # one still per step for the README
    idx, starts = 0, []
    for _, _, n in steps:
        starts.append(idx + n - 1); idx += n
    strip = [Image.fromarray(frames[s]).resize((480, 270), Image.LANCZOS) for s in starts]
    sheet = Image.new("RGB", (480 * 4, 270 * 2), "white")
    for k, im in enumerate(strip):
        sheet.paste(im, ((k % 4) * 480, (k // 4) * 270))
    sheet.save(os.path.join(OUT, "install_steps.png"))
    return dict(frames=len(frames), fps=fps, gif=gif, mp4=mp4)


if __name__ == "__main__":
    D = distances()
    for k, v in D["spots"].items():
        print(f"{k}: {v['from_atomizer_ft']} ft from the atomizer; " + ", ".join(f"{e}: {x['spot_to_exit_ft']} ft (detour {x['detour_ft']})" for e, x in v["exits"].items()))
    plan_png(D)
    elevation_png()
    fb = flag_bracket_png()
    print("flag bracket", fb)
    info = {"distances": D, "flag_bracket": fb}
    print(M.export(OUT))
    overview_png(D)
    if not FAST:
        info["animation"] = animate(D)
        print(info["animation"])
    with open(os.path.join(OUT, "distances.json"), "w") as fh:
        json.dump(info, fh, indent=1)
