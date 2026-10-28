"""The first copper-alloy powder lot (Preliminary results, fig:cupowder), 6.5 x 2.42 in.

Real data throughout. Sterling's Oct 27 review replaced the placeholders with the first copper run
of the ultrasonic atomizer (Gage Erickson, Oct 27, 2026, powder code k7m2q9, DAL #219) and Ronnie
Guymon's SEM and EDS of that powder (BYU Apreo, Oct 27, Box `Baird_S_SEM/Ronnie Guymon/Bronze`).
The alloy is 630 bronze (UNS C63000, a nickel-aluminum bronze), not the "Cu70/Ni30" of the run log
(Sterling, #219, Oct 28). Sam Webster's Mines tracks moved to the Facilities attachment (Fig. 3c),
since that powder is not ours.

Top row, (a) the run, frames of BYU VCL YouTube 2brsz-90seg ("10/27/2026 Atomizer Run ... Video 5
of atomizer and furnace ports", public) at 60, 240, 330 and 571 s: the charge rods in the crucible,
the rods slumping, the melt pool around the stopper rod, and the stream on the plate through the
chamber window. (b) the lot, Gage's photograph of the jar (DAL #219).
Bottom row, (c) SEM at 200x (HFW 2.07 mm, databar removed), (d) one particle at 2,548x (HFW 163 um),
(e) the EDS spectrum at 20 kV and 3.2 nA, re-plotted from Ronnie's export ("USE THIS ONE").

Inputs are in img/cu-lot-2026-10-27/ (see its README.md).

    python make_cu_prelim_figure.py   # writes ../figures-cu-ded/cu_prelim.pdf and .png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image

HERE = Path(__file__).resolve().parent
IMG = HERE / "img" / "cu-lot-2026-10-27"
OUT = HERE.parent / "figures-cu-ded" / "cu_prelim"

for ttf in sorted(Path("/usr/share/fonts/truetype/msttcorefonts").glob("Times_New_Roman*.ttf")):
    font_manager.fontManager.addfont(str(ttf))
plt.rcParams.update({"font.family": ["Times New Roman", "serif"], "font.size": 8,
                     "axes.linewidth": 0.6, "pdf.fonttype": 42})

W, GAP = 6.5, 0.06
H1, H2 = 1.18, 1.18                      # top row (run, lot), bottom row (SEM, EDS)
H = H1 + GAP + H2
UM_PER_PX = {"sem_200x.png": 2070 / 1800, "sem_2548x_particle.png": 163 / 3072}  # HFW / width (px)

fig = plt.figure(figsize=(W, H))


def axes(x, y, w, h):
    ax = fig.add_axes([x / W, y / H, w / W, h / H])
    ax.set(xticks=[], yticks=[])
    for s in ax.spines.values():
        s.set_visible(False)
    return ax


def label(ax, s, color="black", bg="white"):
    ax.text(0.04, 0.96, s, transform=ax.transAxes, ha="left", va="top", fontsize=8, weight="bold",
            color=color, zorder=5, bbox=dict(boxstyle="square,pad=0.15", fc=bg, ec="none", alpha=0.85))


def show(ax, name):
    im = Image.open(IMG / name)
    ax.imshow(im, cmap="gray" if im.mode == "L" else None, aspect="auto", interpolation="lanczos")
    return im


def scalebar(ax, im, name, um, text):
    px = um / UM_PER_PX[name]
    w, h = im.size
    x1, y = w * 0.95, h * 0.93
    ax.plot([x1 - px, x1], [y, y], color="white", lw=2.2, solid_capstyle="butt")
    ax.text(x1 - px / 2, y - h * 0.03, text, color="white", ha="center", va="bottom", fontsize=7.5)


# Top row: (a) four run frames, (b) the jar; five equal panels
w1 = (W - 4 * GAP) / 5
y1 = H2 + GAP
# Frames re-cropped Oct 28 so the crucible rim sits at the same place in (i)-(iii); the time is
# from the start of the run video (2brsz-90seg).
for k, (name, sub, t) in enumerate([("run_t060s.png", "i", 60), ("run_t240s.png", "ii", 240),
                                    ("run_t330s.png", "iii", 330), ("run_t571s.png", "iv", 571)]):
    ax = axes(k * (w1 + GAP), y1, w1, H1)
    show(ax, name)
    label(ax, f"(a{sub})" if k == 0 else f"({sub})")
    ax.text(0.96, 0.04, f"t = {t} s", transform=ax.transAxes, ha="right", va="bottom", fontsize=7,
            color="white", zorder=5, bbox=dict(boxstyle="square,pad=0.15", fc="black", ec="none", alpha=0.55))
ax = axes(4 * (w1 + GAP), y1, w1, H1)
show(ax, "lot_jar.jpg")
label(ax, "(b)")

# Bottom row: (c) SEM 200x, (d) one particle, (e) EDS
sem = Image.open(IMG / "sem_200x.png")
wc = H2 * sem.size[0] / sem.size[1]
wd = H2
we = W - wc - wd - 2 * GAP
ax = axes(0, 0, wc, H2)
im = show(ax, "sem_200x.png")
scalebar(ax, im, "sem_200x.png", 500, "500 µm")
label(ax, "(c)")
ax = axes(wc + GAP, 0, wd, H2)
im = show(ax, "sem_2548x_particle.png")
scalebar(ax, im, "sem_2548x_particle.png", 20, "20 µm")
label(ax, "(d)")

e, c = np.loadtxt(IMG / "eds_20kV_3p2nA.csv", delimiter=",", unpack=True)
keep = e <= 10.0
ax = fig.add_axes([(wc + wd + 2 * GAP + 0.36) / W, 0.30 / H, (we - 0.40) / W, (H2 - 0.36) / H])
ax.fill_between(e[keep], c[keep] / 1000, color="#b87333", lw=0)
ax.plot(e[keep], c[keep] / 1000, color="#6b3d17", lw=0.5)
ax.set_xlim(0, 10)
ax.set_ylim(0, c[keep].max() / 1000 * 1.12)
ax.set_xlabel("Energy (keV)", labelpad=1)
ax.set_ylabel("Counts (×10³)", labelpad=1)
ax.tick_params(length=2, width=0.5, labelsize=7, pad=1.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
peaks = [("C", 0.277), ("Cu L, Ni L", 0.93), ("Al", 1.487), ("Fe", 6.404), ("Ni", 7.478),
         ("Cu Kα", 8.048), ("Cu Kβ", 8.905)]
for name, kev in peaks:
    i = np.argmin(abs(e - kev))
    top = c[max(i - 4, 0):i + 5].max() / 1000
    ax.annotate(name, (kev, top), xytext=(0, 2), textcoords="offset points", ha="center",
                va="bottom", fontsize=6.5)
fig.text((wc + wd + 2 * GAP + 0.04) / W, (H2 - 0.02) / H, "(e)", ha="left", va="top", fontsize=8, weight="bold")

if __name__ == "__main__":
    # dpi matters for the PDF too: matplotlib resamples imshow images to it (default 100 dpi,
    # which left the photos and SEM images about 120-150 px across in print).
    fig.savefig(OUT.with_suffix(".pdf"), dpi=600, metadata={"CreationDate": None})
    fig.savefig(OUT.with_suffix(".png"), dpi=200)
    print("wrote", OUT.with_suffix(".pdf"))
