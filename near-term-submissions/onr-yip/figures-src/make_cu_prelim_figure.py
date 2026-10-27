"""Copper powder figure (Preliminary results, fig:cupowder): three panels in 6.5 x 2.6 in.

(a) and (b) are placeholders, not data. Sterling's request on PR 134 (Oct 24, 2026): "add this in
as a placeholder image so that we can anticipate the right amount of space. You can make this a 3D
diagram that will replace with something real". His Oct 27 review replaced the size distribution
with an EDS map. (a) is a 3D sketch of copper spheres on a stub where the SEM image of the first
copper lot will go, and (b) a dot map of made-up spheres where its EDS map will go; both draw their
particles from a made-up log-normal and carry the PLACEHOLDER watermark.

(c) is real: copper-nickel powder spread in a groove across a block and melted into a track at the
Colorado School of Mines, photographed by Sam Webster (email of October 21, 2026), cropped here to
the track. Neither the photo nor the email gives a dimension, so (c) has no scale bar.

Same 6.5 x 2.6 in footprint as the CALPHAD figure, so real images for (a) and (b) can replace the
placeholders without moving pages.

    python make_cu_prelim_figure.py   # writes ../figures-cu-ded/cu_prelim.pdf
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image

HERE = Path(__file__).resolve().parent
PHOTO = HERE / "img" / "mines-cuni-track-in-groove.png"
CROP = (235, 0, 670, 483)  # left, top, right, bottom (px): the whole track and the powder beside it
rng = np.random.default_rng(19)

for ttf in sorted(Path("/usr/share/fonts/truetype/msttcorefonts").glob("Times_New_Roman*.ttf")):
    font_manager.fontManager.addfont(str(ttf))
plt.rcParams.update({"font.family": ["Times New Roman", "serif"], "font.size": 8,
                     "axes.linewidth": 0.6, "pdf.fonttype": 42})

W, H, GAP = 6.5, 2.6, 0.08
widths = [2.0, 2.0, W - 4.0 - 2 * GAP]  # (c) takes the rest, 2.34 in, the 0.90 aspect of the crop
lefts = [0, 2.0 + GAP, 4.0 + 2 * GAP]
fig = plt.figure(figsize=(W, H))
copper = np.array([0.80, 0.50, 0.30])


def panel(i, color):
    ax = fig.add_axes([lefts[i] / W, 0, widths[i] / W, 1])
    ax.set_facecolor(color)
    ax.set(xticks=[], yticks=[])
    for s in ax.spines.values():
        s.set_visible(False)
    return ax


def label(ax, s):
    ax.text(0.04, 0.97, s, transform=ax.transAxes, ha="left", va="top", fontsize=9, weight="bold",
            zorder=5, bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.85))


def note(ax, s):
    ax.text(0.5, 0.04, s, transform=ax.transAxes, ha="center", fontsize=7, color="0.35",
            style="italic", zorder=5, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none", alpha=0.85))


def spheres(n, w, h):
    """Non-overlapping monolayer of n particles in a w x h um field, diameters in um."""
    d, xy = [], []
    while len(d) < n:
        di = np.clip(rng.lognormal(np.log(70), 0.35), 30, 160)
        p = rng.uniform(0, 1, 2) * (w, h)
        if all(np.hypot(*(p - q)) > (di + dj) / 2 for q, dj in zip(xy, d)):
            d.append(di)
            xy.append(p)
    return np.array(xy), np.array(d)


# (a) 3D sketch of spherical particles on a stub, standing in for the SEM image.
bg = panel(0, "0.94")
ax = fig.add_axes([lefts[0] / W, 0.12, widths[0] / W, 0.88], projection="3d", computed_zorder=False)
ax.patch.set_alpha(0)
gx, gy = np.meshgrid([-40, 440], [-40, 440])
ax.plot_surface(gx, gy, np.zeros_like(gx), color="0.85", linewidth=0)
xy, d = spheres(60, 400, 400)
cam = np.array([np.cos(np.radians(-60)), np.sin(np.radians(-60))])
u, v = np.mgrid[0 : 2 * np.pi : 24j, 0 : np.pi : 12j]
for (x, y), di in sorted(zip(xy, d), key=lambda t: t[0] @ cam):
    r = di / 2
    xs, ys, zs = x + r * np.cos(u) * np.sin(v), y + r * np.sin(u) * np.sin(v), r + r * np.cos(v)
    shade = 0.55 + 0.45 * np.clip(np.cos(v) * 0.7 + np.cos(u) * np.sin(v) * 0.3, 0, 1)
    ax.plot_surface(xs, ys, zs, facecolors=np.clip(shade[..., None] * copper, 0, 1),
                    linewidth=0, antialiased=True, shade=False)
ax.set(xlim=(-40, 440), ylim=(-40, 440), zlim=(0, 200))
ax.set_box_aspect((1, 1, 0.42), zoom=1.0)
ax.view_init(elev=32, azim=-60)
ax.set_axis_off()
label(bg, "(a)")
note(bg, "SEM image of the first copper lot")

# (b) dot map of spheres, standing in for the EDS map: dot density follows the particle thickness.
bx = panel(1, "white")
um = 1.25  # um per pixel
ny, nx = round(H * 160), round(widths[1] * 160)
xy, d = spheres(45, nx * um, ny * um)
yy, xx = np.mgrid[0:ny, 0:nx] * um
signal = np.zeros((ny, nx))
for (x, y), di in zip(xy, d):
    signal = np.maximum(signal, np.sqrt(np.clip(1 - ((xx - x) ** 2 + (yy - y) ** 2) / (di / 2) ** 2, 0, 1)))
dots = rng.uniform(size=signal.shape) < 0.02 + 0.55 * signal
bx.imshow(np.where(dots[..., None], copper * 0.85, 0.97), interpolation="none", aspect="auto")
label(bx, "(b)")
note(bx, "EDS map of the first copper lot")

fig.text((lefts[1] + widths[1]) / 2 / W, 0.5, "PLACEHOLDER", ha="center", va="center", rotation=12,
         fontsize=30, color="red", alpha=0.3, weight="bold", zorder=10)

# (c) the track photo, cropped to the track.
cx = panel(2, "white")
cx.imshow(np.asarray(Image.open(PHOTO).convert("RGB").crop(CROP)), interpolation="none", aspect="auto")
label(cx, "(c)")

fig.savefig(HERE.parent / "figures-cu-ded" / "cu_prelim.pdf", metadata={"CreationDate": None})
