"""Images for the monitor in the animation's last steps (C5-C7), drawn with matplotlib.

All three are illustrations, and say so on the image: the melt-pool shapes follow a coarse rule of thumb in line
energy P/v (layout.regime and the widths below), and the parity plot's points are made up. Nothing here is a
prediction or a measurement; the AM Module and the pilot's cross-sections replace them.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, Polygon  # noqa: E402

import layout as L  # noqa: E402

SIZE_IN = (16, 10)          # 1600 x 1000 px at 100 dpi: the monitor's 560 x 350 aspect
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
SURFACE = "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"
NOTE = "Illustration only: shapes from a rule of thumb in P/v, not data or predictions"


def pool(E: float):
    """Illustrative melt-pool size in µm for line energy E (J/mm): width, depth below the surface, bead height."""
    w = 300 * np.sqrt(E)
    reg = L.regime(E)
    d = {"balling / lack of fusion": 0.3, "conduction": 0.45, "transition": 0.8, "keyhole": 1.7}[reg] * w
    h = 0.28 * w
    return w, d, h, reg


def outline(w, d, h, reg, n=80):
    """Closed outline of the fused zone (bead above, pool below), x across the track, z up, in µm."""
    t = np.linspace(0, np.pi, n)
    top = np.c_[-w / 2 * np.cos(t), h * np.sin(t)]                    # the bead, left to right over the top
    if reg == "keyhole":
        s = np.linspace(0, 1, n)
        half = w / 2 * (1 - s) ** 0.35 * (0.55 + 0.45 * (1 - s) ** 3) + 0.06 * w
        right = np.c_[half, -d * s]
        bot = right[::-1]
        left = np.c_[-half, -d * s]
        return np.vstack([top, bot, left])
    b = np.c_[w / 2 * np.cos(t), -d * np.sin(t)]                       # half-ellipse below, right to left
    return np.vstack([top, b])


def sem_texture(ax, rng, w_um, h_um, top):
    """A grey SEM-like background: smoothed noise as grains, darker in the mount above the surface."""
    n = 220
    z = rng.normal(size=(n, n))
    k = np.exp(-np.linspace(-2, 2, 9) ** 2)
    k /= k.sum()
    for axis in (0, 1):
        z = np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), axis, z)
    img = 0.55 + 0.10 * z / z.std()
    ax.imshow(img, cmap="gray", vmin=0, vmax=1, extent=(-w_um / 2, w_um / 2, -h_um * (1 - top), h_um * top),
              origin="lower", zorder=0, interpolation="bilinear")
    ax.add_patch(Polygon([(-w_um / 2, 0), (w_um / 2, 0), (w_um / 2, h_um * top), (-w_um / 2, h_um * top)],
                         closed=True, color="#26272a", zorder=1))


def draw_track(ax, t, rng, fov=700.0, aspect=1.3, top=0.25, annotate=False):
    w, d, h, reg = pool(t["E"])
    H = fov * aspect
    sem_texture(ax, rng, fov, H, top)
    xy = outline(w, d, h, reg)
    ax.add_patch(Polygon(xy, closed=True, facecolor="#9a9c9f", edgecolor="#e8e8e8", lw=2.2, zorder=2))
    # solidification striations
    for f in np.linspace(0.25, 0.85, 4):
        ax.plot(xy[:, 0] * f, np.where(xy[:, 1] < 0, xy[:, 1] * f, xy[:, 1] * f), color="#b9bbbe", lw=0.8,
                alpha=0.6, zorder=3)
    if reg == "keyhole":
        ax.add_patch(Circle((0.03 * w, -0.9 * d), 0.07 * w, color="#141414", zorder=4))
    ax.set_xlim(-fov / 2, fov / 2)
    ax.set_ylim(-H * (1 - top), H * top)
    ax.set_aspect("equal")
    ax.axis("off")
    # scale bar
    x0, y0 = fov / 2 - 150, -H * (1 - top) + 30
    ax.plot([x0, x0 + 100], [y0, y0], color="white", lw=4, zorder=5)
    ax.text(x0 + 50, y0 + 14, "100 µm", color="white", ha="center", va="bottom", fontsize=17, zorder=5)
    if annotate:
        kw = dict(color="#ffd34d", lw=2.6, zorder=6)
        ax.annotate("", xy=(-w / 2, 8), xytext=(w / 2, 8), arrowprops=dict(arrowstyle="<->", **kw))
        ax.text(0, h + 18, f"width {w:.0f} µm", color="#ffd34d", ha="center", va="bottom", fontsize=21, zorder=6)
        ax.annotate("", xy=(w / 2 + 25, 0), xytext=(w / 2 + 25, -d), arrowprops=dict(arrowstyle="<->", **kw))
        ax.text(w / 2 + 38, -d / 2, f"depth {d:.0f} µm", color="#ffd34d", ha="left", va="center", fontsize=21,
                zorder=6)
        ax.annotate("", xy=(-w / 2 - 25, 0), xytext=(-w / 2 - 25, h), arrowprops=dict(arrowstyle="<->", **kw))
        ax.text(-w / 2 - 38, h / 2 + 4, f"height {h:.0f} µm", color="#ffd34d", ha="right", va="center", fontsize=21,
                zorder=6)
        ax.plot([-fov / 2, fov / 2], [0, 0], color="#ffd34d", lw=1.2, ls="--", zorder=6)
    return w, d, h, reg


def pick_row_tracks():
    """Insert A, row 1 (the row the animation sections): one track per regime where the map has one."""
    row = [t for t in L.track_map() if t["insert"] == "A" and t["row"] == 1 and t["E"] is not None]
    want = ("conduction", "transition", "keyhole")
    out = []
    for r in want:
        c = [t for t in row if L.regime(t["E"]) == r]
        if c:
            out.append(sorted(c, key=lambda t: t["E"])[len(c) // 2])
    return out[:3]


def sem_tiles(path: Path):
    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=SIZE_IN, dpi=100, facecolor="#101114")
    tracks = pick_row_tracks()
    fig.text(0.03, 0.94, "C5: SEM of insert A, row 1 (3 of its 9 tracks)", color="white", fontsize=30,
             weight="bold", va="center")
    for i, t in enumerate(tracks):
        ax = fig.add_axes([0.03 + i * 0.32, 0.14, 0.30, 0.70])
        draw_track(ax, t, rng, fov=720.0, aspect=1.4, top=0.22)
        ax.text(0.5, 1.03, f"{t['P']} W, {t['v']} mm/s  ({t['E']:.2f} J/mm)", transform=ax.transAxes,
                color="white", ha="center", va="bottom", fontsize=21)
    fig.text(0.03, 0.07, NOTE, color="#c9c9c9", fontsize=21, va="center", style="italic")
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)


def measure(path: Path):
    rng = np.random.default_rng(11)
    fig = plt.figure(figsize=SIZE_IN, dpi=100, facecolor="#101114")
    t = pick_row_tracks()[-1]
    ax = fig.add_axes([0.02, 0.13, 0.60, 0.74])
    w, d, h, reg = draw_track(ax, t, rng, fov=1000.0, aspect=0.74 * 10 / (0.60 * 16), top=0.2, annotate=True)
    fig.text(0.03, 0.94, "C6: measure every track, classify its regime", color="white", fontsize=30,
             weight="bold", va="center")
    rows = [("track", "insert A, row 1"), ("P, v", f"{t['P']} W, {t['v']} mm/s"), ("P/v", f"{t['E']:.2f} J/mm"),
            ("width", f"{w:.0f} µm"), ("depth", f"{d:.0f} µm"), ("height", f"{h:.0f} µm"),
            ("fused area", f"{(np.pi / 4 * w * (d + h)) / 1e3:.0f} x 10³ µm²"), ("regime", reg)]
    for i, (k, v) in enumerate(rows):
        y = 0.80 - i * 0.085
        fig.text(0.65, y, k, color="#a9abb0", fontsize=23, va="center")
        fig.text(0.78, y, v, color="white", fontsize=23, va="center", weight="bold" if k == "regime" else None)
    fig.text(0.03, 0.07, NOTE, color="#c9c9c9", fontsize=21, va="center", style="italic")
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)


def parity(path: Path):
    rng = np.random.default_rng(3)
    fig = plt.figure(figsize=SIZE_IN, dpi=100, facecolor=SURFACE)
    ax = fig.add_axes([0.09, 0.15, 0.50, 0.72])
    sets = L.grid_sets()
    meas = np.array([pool(s["E"])[1] for s in sets])
    pred = meas * np.exp(rng.normal(0, 0.16, len(meas)))
    hold = np.zeros(len(sets), bool)
    hold[rng.choice(len(sets), 5, replace=False)] = True
    lim = (0, max(meas.max(), pred.max()) * 1.1)
    ax.fill_between(lim, [lim[0] * 0.8, lim[1] * 0.8], [lim[0] * 1.2, lim[1] * 1.2], color="#f0efec", zorder=0)
    ax.plot(lim, lim, color=INK2, lw=2, zorder=1)
    ax.scatter(pred[~hold], meas[~hold], s=170, color=BLUE, edgecolor=SURFACE, lw=2, zorder=3,
               label="calibration tracks")
    ax.scatter(pred[hold], meas[hold], s=170, facecolor=SURFACE, edgecolor=ORANGE, lw=3, zorder=4,
               label="held-out tracks")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("AM Module depth, µm (committed before printing)", fontsize=21, color=INK)
    ax.set_ylabel("measured depth, µm", fontsize=21, color=INK)
    ax.tick_params(labelsize=17, colors=INK2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#c3c2b7")
    ax.legend(fontsize=19, frameon=False, loc="upper left")
    ax.text(lim[1] * 0.97, lim[1] * 0.80, "±20 %", color=MUTED, fontsize=17, ha="right")
    fig.text(0.04, 0.94, "C7: AM Module vs. measured (parity)", color=INK, fontsize=30, weight="bold",
             va="center")
    lines = ["1. Commit predictions for all 65", "    settings before the print (A2).",
             "2. Calibrate absorptivity and beam size", "    on part of the tracks.",
             "3. Validate on the held-out rest.", "4. Same for width and regime:",
             "    measured vs. predicted", "    printability map.",
             "5. Size the campaign from the", "    timing log (one run a week?)."]
    for i, t in enumerate(lines):
        fig.text(0.64, 0.82 - i * 0.062, t, color=INK if not t.startswith("    ") else INK2, fontsize=21,
                 va="center")
    fig.text(0.04, 0.05, "Illustration only: made-up points, to show the comparison, not results", color=MUTED,
             fontsize=19, style="italic", va="center")
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)


def make_all(folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    out = {}
    for name, fn in (("sem", sem_tiles), ("measure", measure), ("parity", parity)):
        p = folder / f"screen_{name}.png"
        fn(p)
        out[name] = p
    return out


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    print(make_all(here / ".cache"))
    print([(t["P"], t["v"], round(t["E"], 3), L.regime(t["E"])) for t in pick_row_tracks()])
