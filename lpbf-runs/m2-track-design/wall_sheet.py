"""Wall-by-wall sheet for Carl's stepped parts on the M2 (issue #100, PR #243, 2026-11-17).

    python wall_sheet.py          # -> out/wall_sheet.csv (84 walls), out/wall_sets.csv (the 61 sets to make),
                                  #    out/wall_regime_grid.csv and out/m2-wall-design.png; seconds when the Eagar-Tsai
                                  #    points are already in out/, many minutes when they are not
    python wall_sheet.py figure   # redraw the figure from the CSVs, no Eagar-Tsai
    python wall_sheet.py fresh    # recompute every Eagar-Tsai point instead of reusing those already in out/

The part (Carl's drawing in PR #243, 2026-11-17): a base about 1.75 x 0.5 in with thin walls standing on it, each
wall running across the 0.5 in width, about 0.3 in tall and 0.05 in (1.27 mm) thick. The second version has 7 walls
a part (Carl, later the same day); with the end walls flush with the base's ends that is a 7.20 mm pitch. Every wall
gets its own parameters.

The build (Carl): 3 parts on each of the 4 squares (the removable panels in Nathan C.'s plate), all in one build, so
84 walls. Carl offered three ways to use them: 84 settings in one orientation, 63 with one square turned to test the
orientation, or 42 with every setting in both orientations. This sheet does a version of the middle one:

- Squares 1-3 carry the map, with the walls along the recoater's travel. Each holds 20 settings from one scrambled
  Sobol sequence (points 0-19, 20-39 and 40-59, so W000-W059 keep the values of the earlier sheets) and one control
  at the 316L hatch (370 W, 1350 mm/s). That is 60 settings and the control: 61 parameter sets to make.
- Square 4 is turned 90 degrees, so its walls run across the recoater's travel. Its part k is a copy of square k's
  part k, with the walls in the same order. So 18 settings and the control (3 times) are printed in both
  orientations, as 21 pairs, and each pair has the same part and wall position in its square. The 6 settings in
  each copied part are picked for spread: maximin distance in the Sobol unit square over all 18 and the control.
- In each of squares 1-3 the other two parts take the remaining 14 settings, dealt in snake order of P/v, so every
  part spans the window. Within each part the settings take random wall positions (seed 100 + square - 1).
- Only the hatch power P and speed v change from wall to wall, on the two WRX Control tabs "Adv. surface area" (the
  hatch) and "Upside surface area" (the upskin). Every other field on every tab stays as in the 316L set, so energy
  per volume follows P/v alone. The trace spacings (0.09 and 0.075 mm), spot sizes (130 um) and offsets to the
  original contour (0.11 and 0.14 mm) are the values in Carl's photos.
- The window is a band in (P, P/v): P from 150 to 370 W, and P/v from 0.09 to 0.55 J/mm, a third to twice the 316L
  hatch's 0.274 J/mm. Speed is capped at 3000 mm/s. 370 W is the most power the photos show. The upper P/v cap keeps
  hot, swollen walls (a recoater risk, more so on the turned square) out of the first build.
- Inside a 1.27 mm wall the hatch, offset 0.11 mm from the outline, fills the middle 1.05 mm: about 13 vectors
  12.5 mm long per layer if it runs along the wall, or about 140 vectors 1.05 mm long if it runs across it.
- For each setting the sheet gives VED at 30 and 50 um layers, Gan et al.'s keyhole number Ke (line_sheet.py),
  the steady-state Eagar-Tsai width W and depth D (130 um spot, absorptivity 0.4, as in eagar_tsai_316l.py), and
  Tang et al.'s overlap rule for lack of fusion, (h/W)^2 + (t/D)^2 <= 1, with h the trace spacing and t the layer
  (Addit. Manuf. 14, 39 (2017), https://doi.org/10.1016/j.addma.2016.12.001). Above 1, the half-elliptical pools
  leave unmelted gaps between tracks and layers. Eagar-Tsai is conduction only, cold substrate, no powder, so
  these regimes are a starting guess for the AM Module to replace, not a prediction.
"""
from __future__ import annotations

import csv
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE))

from eagar_tsai_316l import steady_state_pkg  # noqa: E402
from line_sheet import keyhole_number           # noqa: E402

SEED = 243                       # PR #243; a fresh draw (2026-11-19), not the earlier sheets' seed-100 sequence
LAYERS_UM = (30.0, 50.0)         # the 316L set's layer is not in the photos yet: both are shown
P_RANGE = (150.0, 370.0)         # W; 370 W is the 316L hatch, the most the photos show
D_RANGE = (50.0, 200.0)          # um, spot, log-uniform; the 316L set uses 50, 70 and 130 (photos); variable focus 50-500
H_RANGE = (0.06, 0.14)           # mm, trace (hatch) spacing; the 316L hatch is 0.09, its upskin 0.075
EA_RANGE = (1.0, 6.1)            # J/mm^2, P/(v h), log-uniform; the 316L hatch is 3.05. Same caps as before at h = 0.09
V_MAX = 3000.0                   # mm/s
CONTROL = dict(set="C", P=370.0, v=1350.0, d=130.0, h=0.09)    # the 316L hatch ("Adv. surface area")
SPOT_UM, TRACE_MM = CONTROL["d"], CONTROL["h"]                 # the control's, for the figure's reference lines
SQUARES, PARTS, WALLS = 4, 3, 7                # 4 squares (panels), 3 parts a square, 7 walls a part
MAP_SQUARES = 3                                # squares 1-3 carry the settings, walls along the recoater's travel
TURNED = 4                                     # square 4: turned 90 degrees, part k a copy of square k's part k
PER_SQUARE = PARTS * WALLS - 1                 # 20 Sobol settings + 1 control on each of squares 1-3
N_SOBOL = MAP_SQUARES * PER_SQUARE             # 60
ALONG, ACROSS = "along", "turned 90°"


# The part (Carl, 2026-11-17): 0.05 in walls on a 1.75 x 0.5 in base; the pitch assumes flush end walls.
IN = 25.4
WALL_MM = 0.05 * IN                            # 1.27 mm thick
WALL_LEN_MM = 0.5 * IN                         # 12.7 mm, across the base
BASE_LEN_MM = 1.75 * IN                        # 44.45 mm
PITCH_MM = (BASE_LEN_MM - WALL_MM) / (WALLS - 1)   # 7.20 mm
HATCH_OFFSET_MM = 0.11                         # the 316L hatch's offset to the original contour (Carl's photos)


def hatch_vectors() -> dict:
    """Hatch vectors in one layer of one wall, along it or across it."""
    width = WALL_MM - 2 * HATCH_OFFSET_MM
    length = WALL_LEN_MM - 2 * HATCH_OFFSET_MM
    return dict(hatch_width_mm=round(width, 3), along=(round(width / TRACE_MM) + 1, round(length, 2)),
                across=(round(length / TRACE_MM) + 1, round(width, 2)))


def to_settings(u: np.ndarray) -> tuple[np.ndarray, ...]:
    """Unit cube -> (P W, v mm/s, spot um, trace spacing mm). P linear in P_RANGE; spot log-uniform in D_RANGE;
    trace spacing linear in H_RANGE; areal energy E_A = P/(v h) log-uniform between max(EA_lo, P/(V_MAX h)) and
    EA_hi, so no point needs more than V_MAX. Rounded to 1 W, 5 mm/s, 5 um and 0.005 mm."""
    P = np.round(P_RANGE[0] + u[:, 0] * (P_RANGE[1] - P_RANGE[0]))
    d = np.round(np.exp(math.log(D_RANGE[0]) + u[:, 1] * math.log(D_RANGE[1] / D_RANGE[0])) / 5.0) * 5.0
    h = np.round((H_RANGE[0] + u[:, 2] * (H_RANGE[1] - H_RANGE[0])) / 0.005) * 0.005
    lo = np.log(np.maximum(EA_RANGE[0], P / (V_MAX * h)))
    ea = np.exp(lo + u[:, 3] * (math.log(EA_RANGE[1]) - lo))
    return P, np.round(P / (ea * h) / 5.0) * 5.0, d, np.round(h, 3)


def control_unit() -> np.ndarray:
    """The control's place in the same unit cube."""
    c = CONTROL
    lo = math.log(max(EA_RANGE[0], c["P"] / (V_MAX * c["h"])))
    return np.array([(c["P"] - P_RANGE[0]) / (P_RANGE[1] - P_RANGE[0]),
                     math.log(c["d"] / D_RANGE[0]) / math.log(D_RANGE[1] / D_RANGE[0]),
                     (c["h"] - H_RANGE[0]) / (H_RANGE[1] - H_RANGE[0]),
                     (math.log(c["P"] / (c["v"] * c["h"])) - lo) / (math.log(EA_RANGE[1]) - lo)])


def sobol(n: int, seed: int = SEED) -> np.ndarray:
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")      # n = 60 is not a power of 2; fine for a prefix of the sequence
        return qmc.Sobol(d=4, scramble=True, seed=seed).random(n)


def pick_copied(u: np.ndarray) -> list[tuple[int, ...]]:
    """For each of squares 1-3, the WALLS - 1 settings of the part that is copied onto square 4: the largest
    smallest distance in the unit square over all three picks and the control, ties broken by the ten closest
    pairs. Found by exchanging one square's pick at a time until nothing changes."""
    pts = np.vstack([u, control_unit()])
    D = np.linalg.norm(pts[:, None] - pts[None], axis=-1)
    ctrl, k = len(u), WALLS - 1
    blocks = [list(range(s * PER_SQUARE, (s + 1) * PER_SQUARE)) for s in range(MAP_SQUARES)]

    def best_for(block: list[int], fixed: list[int]) -> tuple[int, ...]:
        inner = np.array([D[a, b] for a, b in combinations(fixed, 2)])
        best, best_key = None, None
        for c in combinations(block, k):
            d = np.concatenate([inner, D[np.ix_(c, fixed)].ravel(), [D[a, b] for a, b in combinations(c, 2)]])
            key = (round(float(d.min()), 9), float(np.log(np.partition(d, 9)[:10]).sum()))
            if best_key is None or key > best_key:
                best, best_key = c, key
        return best

    picks = [best_for(b, [ctrl]) for b in blocks]
    for _ in range(6):
        changed = False
        for j, b in enumerate(blocks):
            fixed = [i for jj, c in enumerate(picks) if jj != j for i in c] + [ctrl]
            new = best_for(b, fixed)
            changed |= new != picks[j]
            picks[j] = new
        if not changed:
            break
    return picks


def walls() -> list[dict]:
    """The 84 walls in square, part, wall order, with their settings (no model columns yet)."""
    u = sobol(N_SOBOL)
    P, v, d, h = to_settings(u)
    picks = pick_copied(u)
    ea = P / (v * h)

    def setting(i: int) -> dict:
        return dict(set=f"W{i:03d}", sobol_index=i, P=float(P[i]), v=float(v[i]), d=float(d[i]), h=float(h[i]))

    rows, copied = [], {}
    for s in range(MAP_SQUARES):
        rest = sorted((i for i in range(s * PER_SQUARE, (s + 1) * PER_SQUARE) if i not in picks[s]),
                      key=lambda i: ea[i])
        others = [k for k in range(PARTS) if k != s]          # square s+1's part s+1 is the one copied
        parts = {k: [] for k in range(PARTS)}
        parts[s] = [setting(i) for i in picks[s]] + [dict(CONTROL, sobol_index="")]
        for r, i in enumerate(rest):                           # snake order over the other two: a b b a a b b ...
            parts[others[r % 2 if (r // 2) % 2 == 0 else 1 - r % 2]].append(setting(i))
        rng = np.random.default_rng(SEED + s)
        for k in range(PARTS):
            sets = sorted(parts[k], key=lambda r: r["P"] / (r["v"] * r["h"]))
            placed = [dict(square=s + 1, part=k + 1, wall=pos + 1, orientation=ALONG, copy_of="", **sets[j])
                      for pos, j in enumerate(rng.permutation(len(sets)))]
            rows += placed
            if k == s:
                copied[k] = placed
    for k in range(PARTS):
        rows += [dict(r, square=TURNED, orientation=ACROSS, copy_of=f"{k + 1}.{k + 1}") for r in copied[k]]
    return sorted(rows, key=lambda r: (r["square"], r["part"], r["wall"]))


def _et(args):
    P, v, d = args
    r = steady_state_pkg(P, v * 1e-3, spot_um=d)
    return r["W"], r["D"]


ET_CACHE = OUT / "wall_et_cache.csv"


def et_values(keys: list[tuple[float, float, float]]) -> dict:
    """Eagar-Tsai (W, D) in um for each (P, v, spot). Points already in out/wall_et_cache.csv are reused, since
    Eagar-Tsai at 1 um takes many minutes; the rest are computed and added to it. `fresh` recomputes them all."""
    known: dict = {}
    if "fresh" not in sys.argv[1:] and ET_CACHE.exists():
        for r in csv.DictReader(open(ET_CACHE, encoding="utf-8")):
            known[(float(r["P_W"]), float(r["v_mm_s"]), float(r["spot_um"]))] = (float(r["W_um"]), float(r["D_um"]))
    missing = sorted(set(keys) - set(known))
    if missing:
        with ProcessPoolExecutor() as ex:
            known.update(zip(missing, ex.map(_et, missing)))
        write(ET_CACHE, [dict(P_W=k[0], v_mm_s=k[1], spot_um=k[2], W_um=round(w, 1), D_um=round(dd, 1))
                         for k, (w, dd) in sorted(known.items())])
    return {k: known[k] for k in keys}


def lof_index(W_um: float, D_um: float, t_um: float, h_mm: float) -> float:
    """Tang et al. (2017): (h/W)^2 + (t/D)^2; above 1 means lack of fusion."""
    return (h_mm * 1e3 / W_um) ** 2 + (t_um / D_um) ** 2


def regime(lof: float, ke: float) -> str:
    if lof > 1.0:
        return "lack of fusion"
    return "keyhole mode" if ke >= 6.0 else "dense"


def set_name(r: dict) -> str:
    """ID first: WRX Control's job tree cuts names off after about ten characters."""
    return f"{r['set']}_{int(r['P'])}W_{int(r['v'])}_{int(r['d'])}um_h{round(r['h'] * 1000):03d}"


def with_model(rows: list[dict], et: bool = True) -> list[dict]:
    """Adds energy, Ke and (unless et is False) Eagar-Tsai width and depth and the overlap-rule regimes."""
    W_D = et_values(sorted({(r["P"], r["v"], r["d"]) for r in rows})) if et else {}
    out = []
    for r in rows:
        ke = keyhole_number(r["P"], r["v"], r["d"])
        el = r["P"] / r["v"]
        row = dict(square=r["square"], part=r["part"], wall=r["wall"], orientation=r["orientation"],
                   copy_of=r["copy_of"], set=r["set"], set_name=set_name(r), sobol_index=r["sobol_index"],
                   power_W=int(r["P"]), speed_mm_s=int(r["v"]), spot_um=int(r["d"]), trace_spacing_mm=r["h"],
                   P_over_v_J_mm=round(el, 4), E_area_J_mm2=round(el / r["h"], 2),
                   VED_30um_J_mm3=round(el / (r["h"] * 0.030), 1), VED_50um_J_mm3=round(el / (r["h"] * 0.050), 1),
                   Ke=round(ke, 2))
        if et:
            W, D = W_D[(r["P"], r["v"], r["d"])]
            lof = {t: lof_index(W, D, t, r["h"]) for t in LAYERS_UM}
            row.update(ET_width_um=round(W, 1), ET_depth_um=round(D, 1), LoF_index_30um=round(lof[30.0], 2),
                       LoF_index_50um=round(lof[50.0], 2), regime_30um=regime(lof[30.0], ke),
                       regime_50um=regime(lof[50.0], ke))
        out.append(row)
    return out


TABS = ("Adv. surface area", "Upside surface area")


def sets_table(sheet: list[dict]) -> list[dict]:
    """One row per parameter set to make, in WRX Control's own field names, and the walls that use it. Both tabs
    (hatch and upskin) get the same four values; the offset to the original contour stays as in the 316L set."""
    by_set: dict[str, list[dict]] = {}
    for r in sheet:
        by_set.setdefault(r["set"], []).append(r)
    rows = []
    for s in sorted(by_set, key=lambda s: (s != "C", s)):
        r0 = by_set[s][0]
        row = {"Set name": r0["set_name"]}
        for tab in TABS:
            row[f"{tab}: Power (W)"] = r0["power_W"]
            row[f"{tab}: Speed (mm/s)"] = r0["speed_mm_s"]
            row[f"{tab}: Trace spacing (mm)"] = r0["trace_spacing_mm"]
            row[f"{tab}: Spot size (µm)"] = r0["spot_um"]
        row["Walls (square.part.wall)"] = " ".join(f"{r['square']}.{r['part']}.{r['wall']}" for r in by_set[s])
        rows.append(row)
    return rows


# --- figure ---------------------------------------------------------------------------------------------------------
INK, INK2, MUTED, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#fcfcfb"
SQUARE_STYLE = {1: ("#2a78d6", "o"), 2: ("#eb6834", "s"), 3: ("#1baf7a", "^")}  # categorical slots 1-3 + shape
TINT = {1: "#d5e4f7", 2: "#fbe0d5", 3: "#d2efe4"}
ZONE = {"lof": "#ece9e2", "keyhole": "#dfe9f6"}


def figure(sheet: list[dict], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

    plt.rcParams.update({"font.size": 9.5, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                         "ytick.color": INK2, "axes.titlesize": 10.5})
    fig = plt.figure(figsize=(15.2, 8.6), constrained_layout=True)
    fig.set_facecolor(SURFACE)
    gs = fig.add_gridspec(2, 2, width_ratios=[0.9, 1.1])
    turned = {r["set"] for r in sheet if int(r["square"]) == TURNED}
    f = lambda r, k: float(r[k])  # noqa: E731
    panels = [(fig.add_subplot(gs[0, 0]), "speed_mm_s", "power_W", "Speed (mm/s, log scale)", "Power (W)", True,
               f"(a) Power and speed. {N_SOBOL} Sobol settings on squares 1–3, the control (★);\n"
               "ringed: also on square 4, turned 90°"),
              (fig.add_subplot(gs[1, 0]), "spot_um", "trace_spacing_mm", "Spot size (µm, log scale)",
               "Trace spacing (mm)", True, "(b) Spot size and trace spacing, the same settings")]
    for ax, xk, yk, xl, yl, logx, title in panels:
        ax.set_facecolor(SURFACE)
        for square in range(1, MAP_SQUARES + 1):
            c, m = SQUARE_STYLE[square]
            rs = [r for r in sheet if int(r["square"]) == square and r["set"] != "C"]
            ax.scatter([f(r, xk) for r in rs], [f(r, yk) for r in rs], s=46 if m != "^" else 54, marker=m, c=c,
                       edgecolors=SURFACE, linewidths=1.4, zorder=4)
            rt = [r for r in rs if r["set"] in turned]
            ax.scatter([f(r, xk) for r in rt], [f(r, yk) for r in rt], s=190, marker="o", facecolors="none",
                       edgecolors=INK, linewidths=1.3, zorder=5)
        c0 = next(r for r in sheet if r["set"] == "C")
        ax.scatter([f(c0, xk)], [f(c0, yk)], s=230, marker="*", c=INK, edgecolors=SURFACE, linewidths=1.2, zorder=6)
        if logx:
            ax.set_xscale("log")
        ax.minorticks_off()
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.set_title(title, loc="left", color=INK)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    ax0, ax1 = panels[0][0], panels[1][0]
    ax0.set_xticks([250, 500, 1000, 2000, 3000])
    ax0.set_xticklabels(["250", "500", "1000", "2000", "3000"])
    ax1.set_xticks([50, 70, 100, 130, 200])
    ax1.set_xticklabels(["50", "70", "100", "130", "200"])
    handles = [Line2D([], [], ls="none", marker=SQUARE_STYLE[p][1], ms=7.5, mfc=SQUARE_STYLE[p][0], mec=SURFACE,
                      label=f"square {p}") for p in range(1, MAP_SQUARES + 1)]
    handles += [Line2D([], [], ls="none", marker="*", ms=13, mfc=INK, mec=SURFACE,
                       label="control: the 316L hatch (370 W, 1350 mm/s, 130 µm, 0.09 mm)"),
                Line2D([], [], ls="none", marker="o", ms=12, mfc="none", mec=INK, label="also on square 4, turned")]
    ax1.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False, fontsize=8.2)

    # (c) the four squares from above, with every wall's set (positions of the squares on the plate are placeholders)
    bx = fig.add_subplot(gs[:, 1])
    bx.set_facecolor(SURFACE)
    bx.set_aspect("equal")
    bx.axis("off")
    S, GAP, SPACE = 88.0, 10.0, 24.0
    origin = {1: (0.0, S + GAP), 2: (S + GAP, S + GAP), 3: (0.0, 0.0), 4: (S + GAP, 0.0)}
    lab = {(int(r["square"]), int(r["part"]), int(r["wall"])): r for r in sheet}
    for sq, (ox, oy) in origin.items():
        bx.add_patch(FancyBboxPatch((ox, oy), S, S, boxstyle="round,pad=0,rounding_size=5", fc="#efeee9", ec=MUTED,
                                    lw=0.9))
        title = f"square {sq}" + (": turned 90°" if sq == TURNED else "")
        bx.text(ox + 3, oy + S - 3, title, ha="left", va="top", fontsize=9, color=INK, fontweight="bold")
        for k in range(PARTS):
            copiedpart = sq == TURNED or k + 1 == sq
            fill = TINT[k + 1] if copiedpart else "#d9d8d2"
            box = dict(boxstyle="square,pad=0.12", fc=fill, ec="none")
            if sq != TURNED:          # walls along the blade's travel (x): bases stand along y, wall 1 at the top
                cx, cy = ox + S / 2 + (k - 1) * SPACE, oy + S / 2 - 3
                top = cy + BASE_LEN_MM / 2
                bx.add_patch(Rectangle((cx - WALL_LEN_MM / 2, cy - BASE_LEN_MM / 2), WALL_LEN_MM, BASE_LEN_MM,
                                       fc=fill, ec=INK2, lw=0.7))
                bx.add_patch(Polygon([(cx - 2.2, top + 3.2), (cx + 2.2, top + 3.2), (cx, top + 0.8)], closed=True,
                                     fc=INK2, ec="none"))
                bx.text(cx, cy - BASE_LEN_MM / 2 - 1.4, f"part {k + 1}", ha="center", va="top", fontsize=7.2,
                        color=INK2)
                for w in range(1, WALLS + 1):
                    y = top - WALL_MM / 2 - (w - 1) * PITCH_MM
                    r = lab[(sq, k + 1, w)]
                    bx.add_patch(Rectangle((cx - WALL_LEN_MM / 2, y - WALL_MM / 2), WALL_LEN_MM, WALL_MM,
                                           fc=INK if r["set"] == "C" else "#8f8e88", ec="none"))
                    bx.text(cx, y, r["set"], ha="center", va="center", fontsize=5.6, color=INK, bbox=box)
            else:                     # turned: bases lie along x, walls across the blade's travel, wall 1 at the left
                cx, cy = ox + S / 2, oy + S / 2 - 6 + (1 - k) * SPACE
                left = cx - BASE_LEN_MM / 2
                bx.add_patch(Rectangle((left, cy - WALL_LEN_MM / 2), BASE_LEN_MM, WALL_LEN_MM, fc=fill, ec=INK2,
                                       lw=0.7))
                bx.add_patch(Polygon([(left - 3.2, cy - 2.2), (left - 3.2, cy + 2.2), (left - 0.8, cy)], closed=True,
                                     fc=INK2, ec="none"))
                bx.text(cx, cy + WALL_LEN_MM / 2 + 1.0, f"part {k + 1}: a copy of square {k + 1}'s part {k + 1}",
                        ha="center", va="bottom", fontsize=7.0, color=INK2)
                for w in range(1, WALLS + 1):
                    x = left + WALL_MM / 2 + (w - 1) * PITCH_MM
                    r = lab[(sq, k + 1, w)]
                    bx.add_patch(Rectangle((x - WALL_MM / 2, cy - WALL_LEN_MM / 2), WALL_MM, WALL_LEN_MM,
                                           fc=INK if r["set"] == "C" else "#8f8e88", ec="none"))
                    bx.text(x, cy, r["set"], ha="center", va="center", fontsize=5.6, color=INK, rotation=90, bbox=box)
    bx.add_patch(FancyArrowPatch((0.0, -9.0), (2 * S + GAP, -9.0), arrowstyle="-|>", mutation_scale=12, color=INK2,
                                 lw=1.1))
    bx.text(S + GAP / 2, -11.0, "the blade's travel, in this drawing (check which way it runs on the M2)",
            ha="center", va="top", fontsize=7.8, color=INK2)
    bx.text(0.0, -17.5,
            f"Walls 0.05 in ({WALL_MM:.2f} mm) thick at a {PITCH_MM:.2f} mm pitch; black walls are the control. "
            "▲/▶ marks the wall-1 end.\nTinted parts are printed twice: square k's part k, and its copy on square 4, "
            "part k, turned 90° with the walls in the same order.\nWhich panel is which square doesn't matter; "
            "write it down. Sets: out/wall_sets.csv; walls: out/wall_sheet.csv.",
            ha="left", va="top", fontsize=7.6, color=INK2, linespacing=1.25)
    bx.set_xlim(-2, 2 * S + GAP + 2)
    bx.set_ylim(-32, 2 * S + GAP + 2)
    bx.set_title("(c) The four squares from above: every wall's set (not to scale between squares)", loc="left",
                 color=INK)
    fig.suptitle("Carl's stepped parts on the M2: 7 walls a part, 3 parts a square, 4 squares; a fresh 4-D Sobol design "
                 "in power, speed, spot size and trace spacing", x=0.01, ha="left", fontsize=12, color=INK)
    fig.savefig(path, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if sys.argv[1:] == ["figure"]:
        figure(list(csv.DictReader(open(OUT / "wall_sheet.csv", encoding="utf-8"))), OUT / "m2-wall-design.png")
        sys.exit()
    et = "noet" not in sys.argv[1:]
    sheet = with_model(walls(), et=et)
    write(OUT / "wall_sheet.csv", sheet)
    write(OUT / "wall_sets.csv", sets_table(sheet))
    figure([{k: str(x) for k, x in r.items()} for r in sheet], OUT / "m2-wall-design.png")

    sets = {r["set"] for r in sheet}
    print(f"{len(sheet)} walls, {len(sets)} parameter sets ({len(sets) - 1} Sobol settings and the control)")
    for square in range(1, SQUARES + 1):
        rs = [r for r in sheet if r["square"] == square]
        sob = [r for r in rs if r["set"] != "C"]
        line = (f"square {square}: {len(sob)} settings, {len(rs) - len(sob)} controls; "
                f"P {min(r['power_W'] for r in sob)}-{max(r['power_W'] for r in sob)} W, "
                f"v {min(r['speed_mm_s'] for r in sob)}-{max(r['speed_mm_s'] for r in sob)} mm/s, "
                f"spot {min(r['spot_um'] for r in sob)}-{max(r['spot_um'] for r in sob)} um, "
                f"h {min(r['trace_spacing_mm'] for r in sob)}-{max(r['trace_spacing_mm'] for r in sob)} mm, "
                f"Ke {min(r['Ke'] for r in sob)}-{max(r['Ke'] for r in sob)}")
        if et:
            line += " " + str({t: {g: sum(r[f"regime_{t}"] == g for r in sob)
                                   for g in ("lack of fusion", "dense", "keyhole mode")} for t in ("30um", "50um")})
        print(line)
    sob = [r for r in sheet if r["square"] <= MAP_SQUARES and r["set"] != "C"]
    for col in ("power_W", "speed_mm_s", "spot_um", "trace_spacing_mm"):
        print(col, "distinct", len({r[col] for r in sob}))
