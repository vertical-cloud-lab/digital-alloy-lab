"""Photo tiles and two schematic icons for the workflow figure (Fig. 1).

Crops each source photo to 4:3, resizes it to 680 x 510 px and writes it to
../figures-cu-ded/fig1/. The charge tile joins the powder doser photo to a
drawn section of the cup and plug (after the shop drawing img/cup_plug.png,
without its leader arrows). The tensile and immersion icons are drawn here
(schematics, not data). Sources are listed in img/SOURCES.md and
../figures-cu-ded/README.md.

    python make_fig1_tiles.py                    # everything
    python make_fig1_tiles.py atomizer charge    # only the named tiles/icons
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
from PIL import Image

ONLY = set(sys.argv[1:])  # empty: make everything


def wanted(name):
    return not ONLY or name in ONLY

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # near-term-submissions/onr-yip
IMG = HERE / "img"
OUT = ROOT / "figures-cu-ded" / "fig1"
OUT.mkdir(exist_ok=True)
W, H = 680, 510

# (output name, source, crop box as fractions of width and height: x0, y0, x1, y1)
TILES = [
    ("calphad", ROOT / "pycalphad-cu/cu_panel2.png", (0.0, 0.0, 1.0, 1.0)),
    # The 630 bronze charge rods in the crucible, Oct 27, 2026 run (YouTube 2brsz-90seg at 60 s)
    ("atomizer", IMG / "cu-lot-2026-10-27/run_t060s.png", (0.0, 0.10, 1.0, 0.77)),
    ("utah", IMG / "utah-insstek-mxlab.jpg", (0.06, 0.0, 0.82, 1.0)),
    ("mines", IMG / "mines-formalloy-x2.jpg", (0.0, 0.10, 1.0, 0.77)),
    ("sem", IMG / "byu-emf-apreo.jpg", (0.0, 0.14, 1.0, 0.82)),
    # The CubXL pipetting into a vial (YouTube Short wLhKt2Qzj70, "Mix testing protocol on CubXL", Oct 12, 2026, at 104 s)
    ("screen", IMG / "lab-cubxl-mix.jpg", (0.0, 0.0, 1.0, 1.0)),
    # Repair branch: the polisher that sections a coupon across its fusion line.
    ("repair", IMG / "byu-px300-polisher.jpg", (0.0, 0.10, 1.0, 0.79)),
]


def fit(im, box):
    w, h = im.size
    x0, y0, x1, y1 = (int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))
    im = im.crop((x0, y0, x1, y1))
    # Pad (white) rather than stretch if the crop is not 4:3.
    cw, ch = im.size
    target = W / H
    if abs(cw / ch - target) > 0.01:
        if cw / ch > target:
            nh = int(round(cw / target))
            canvas = Image.new("RGB", (cw, nh), "white")
            canvas.paste(im, (0, (nh - ch) // 2))
        else:
            nw = int(round(ch * target))
            canvas = Image.new("RGB", (nw, ch), "white")
            canvas.paste(im, ((nw - cw) // 2, 0))
        im = canvas
    return im.resize((W, H), Image.LANCZOS)


for name, src, box in TILES:
    if not wanted(name):
        continue
    if not src.exists():  # cu_panel2.png until ../pycalphad-cu/run_calphad.py has run
        print("skipped", name, "(no", src, ")")
        continue
    im = Image.open(src).convert("RGB")
    fit(im, box).save(OUT / f"{name}.jpg", quality=88)
    print("wrote", OUT / f"{name}.jpg")


def cup_section(height_px):
    """The filled cup and plug in section, plug up as in the crucible, drawn clean
    (hatched walls, dotted powder, plug with its vent on the centreline) after the
    "assembled and filled" view of img/cup_plug.png, without the drawing's leader arrows."""
    w_u, h_u = 10.0, 42.0  # drawing units: outer width, total height
    dpi = 300
    fig = plt.figure(figsize=(w_u / h_u * height_px / dpi, height_px / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.3, w_u + 0.3)
    ax.set_ylim(-0.3, h_u + 0.3)
    ax.axis("off")
    plt.rcParams["hatch.linewidth"] = 0.5
    wall = dict(facecolor="white", edgecolor="black", hatch="////", lw=0.9)
    # Cup body: outer profile with a conical end, minus the cavity
    outer = [(0, 4), (0, 34), (10, 34), (10, 4), (5, 0)]
    cavity = [(2, 6), (2, 34), (8, 34), (8, 6), (5, 3)]
    ax.add_patch(Polygon(outer, closed=True, **wall))
    ax.add_patch(Polygon(cavity, closed=True, facecolor="#f4efe6", edgecolor="black",
                         hatch="..", lw=0.9))  # powder fill
    # Plug: closes the cup's mouth and stands proud of it, with an axial vent
    ax.add_patch(Rectangle((0, 34), 10, 8, **wall))
    ax.add_patch(Rectangle((2, 30), 6, 4, **wall))  # the plug's spigot, down into the cup
    ax.add_patch(Rectangle((4.6, 30), 0.8, 12, facecolor="#9cc3e6", edgecolor="black", lw=0.6))
    ax.plot([5, 5], [-0.2, h_u + 0.2], color="black", lw=0.5, ls=(0, (6, 2, 1, 2)))
    fig.canvas.draw()
    im = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    plt.close(fig)
    return im


def charge():
    """The powder doser filling a charge (left), and the cup and plug in section
    standing plug-up, as in the crucible (right)."""
    side = 150  # px of the tile's width given to the section
    pw = W - side
    dos = Image.open(IMG / "lab-powder-doser.jpg").convert("RGB")
    dw, dh = dos.size
    y0, y1 = 0.21, 0.80
    x1 = (y1 - y0) * dh * pw / H  # keeps the photo's share at its own aspect
    photo = dos.crop((0, int(y0 * dh), int(x1), int(y1 * dh))).resize((pw, H), Image.LANCZOS)
    sec = cup_section(H - 30)
    if sec.width > side - 24:
        s = (side - 24) / sec.width
        sec = sec.resize((round(sec.width * s), round(sec.height * s)), Image.LANCZOS)
    tile = Image.new("RGB", (W, H), "white")
    tile.paste(photo, (0, 0))
    tile.paste(sec, (pw + (side - sec.width) // 2, (H - sec.height) // 2))
    return tile


if wanted("charge"):
    charge().save(OUT / "charge.jpg", quality=92)
    print("wrote", OUT / "charge.jpg")

# Schematic icons, 4:3, drawn as vector PDFs.
plt.rcParams.update({"pdf.fonttype": 42})


def icon(name, draw):
    if not wanted(name):
        return
    fig = plt.figure(figsize=(1.6, 1.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)
    ax.axis("off")
    draw(ax)
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.png", dpi=300)
    plt.close(fig)
    print("wrote", OUT / f"{name}.pdf")


def tensile(ax):
    # Axes and a schematic stress-strain curve with a dog-bone specimen.
    ax.plot([0.45, 0.45, 3.75], [2.85, 0.35, 0.35], color="black", lw=1.6)
    import numpy as np
    e = np.linspace(0, 1, 200)
    s = np.where(e < 0.08, e / 0.08 * 0.62, 0.62 + 0.38 * (1 - np.exp(-(e - 0.08) * 5)))
    s = s - 0.12 * np.clip(e - 0.85, 0, None) / 0.15
    ax.plot(0.45 + e * 3.1, 0.35 + s * 2.0, color="#b87333", lw=2.6, solid_capstyle="round")
    # Dog-bone
    x0, y0 = 2.0, 0.75
    ax.add_patch(Rectangle((x0, y0), 0.42, 0.55, color="#7a7a7a"))
    ax.add_patch(Rectangle((x0 + 1.12, y0), 0.42, 0.55, color="#7a7a7a"))
    ax.add_patch(Rectangle((x0 + 0.40, y0 + 0.15), 0.74, 0.25, color="#7a7a7a"))


def immersion(ax):
    # A vial of seawater with a coupon on the bottom.
    ax.add_patch(FancyBboxPatch((1.35, 0.25), 1.3, 2.35, boxstyle="round,pad=0.02,rounding_size=0.18",
                                fc="white", ec="black", lw=1.6))
    ax.add_patch(FancyBboxPatch((1.39, 0.29), 1.22, 1.6, boxstyle="round,pad=0.0,rounding_size=0.14",
                                fc="#cfe3f3", ec="none"))
    ax.add_patch(Rectangle((1.3, 2.45), 1.4, 0.32, fc="#555555", ec="black", lw=1.2))
    ax.add_patch(Rectangle((1.65, 0.36), 0.7, 0.32, fc="#b87333", ec="black", lw=1.0))
    for x, y in [(1.7, 1.2), (2.1, 1.5), (2.3, 1.0)]:
        ax.add_patch(plt.Circle((x, y), 0.06, fc="white", ec="#6f9fc8", lw=0.8))


icon("tensile", tensile)
icon("immersion", immersion)
