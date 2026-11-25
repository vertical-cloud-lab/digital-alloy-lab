"""The aluminum LPBF workflow as a network of photo tiles, for slides.

The aluminum counterpart of the copper/DED Fig. 1 of the ONR YIP proposal
(issue 211, PR 215): the same network of steps, each a tile with its name,
what it passes on and its time per result in italics, the inputs entering
where they are set, the tests branching off at the end, and the dashed return
along the bottom. The steps are the route of the BOFN benchmark
(benchmarks/bofn-prelim/ on claude/onr-yip-fy27) as the lab runs it: CALPHAD,
charge, rePOWDER atomization, sieving, Aconity MIDI printing, density, then
tensile and corrosion tests.

Tiles are the lab's own photographs wherever one exists, and renders from the
vertical-lab animations (byu-vcl PR 318) where none does; those carry a
"render" tag. Sources are in img/SOURCES.md.

    python make_al_lpbf_network.py      # from this folder or anywhere

writes tiles/*.jpg, al-lpbf-network.png and al-lpbf-network.pdf next to this
file. Needs matplotlib and Pillow; uses Aptos (the lab's slide font) from
~/.local/share/fonts/aptos/ when it is there, otherwise Lato or DejaVu Sans.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image

HERE = Path(__file__).resolve().parent
IMG = HERE / "img"
TILES = HERE / "tiles"
TILES.mkdir(exist_ok=True)
TW, TH = 960, 720  # tile pixels, 4:3

# ---------------------------------------------------------------- tiles


def fit(im, box):
    """Crop to a box given as fractions (x0, y0, x1, y1), pad to 4:3 with
    white rather than stretch, and resize to the tile size."""
    w, h = im.size
    im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    cw, ch = im.size
    target = TW / TH
    if abs(cw / ch - target) > 0.01:
        if cw / ch > target:
            nh = round(cw / target)
            canvas = Image.new("RGB", (cw, nh), "white")
            canvas.paste(im, (0, (nh - ch) // 2))
        else:
            nw = round(ch * target)
            canvas = Image.new("RGB", (nw, ch), "white")
            canvas.paste(im, ((nw - cw) // 2, 0))
        im = canvas
    return im.resize((TW, TH), Image.LANCZOS)


def charge_tile():
    """The powder doser filling a charge (left) and the cup and plug in
    section, standing plug-up as in the crucible (right), as in the copper
    figure's charge tile (make_fig1_tiles.py on PR 215)."""
    side = 210  # px of the tile's width given to the section
    pw = TW - side
    dos = Image.open(IMG / "lab-powder-doser.jpg").convert("RGB")
    dw, dh = dos.size
    y0, y1 = 0.21, 0.80
    x1 = (y1 - y0) * dh * pw / TH  # keeps the photo's share at its own aspect
    photo = dos.crop((0, int(y0 * dh), int(x1), int(y1 * dh))).resize((pw, TH), Image.LANCZOS)
    cup = Image.open(IMG / "cup_plug.png").convert("RGB")
    cw, ch = cup.size
    sec = cup.crop((int(0.612 * cw), int(0.200 * ch), int(0.865 * cw), int(0.294 * ch)))
    sec = sec.transpose(Image.Transpose.ROTATE_90)  # plug up
    s = min((side - 30) / sec.width, (TH - 40) / sec.height)
    sec = sec.resize((round(sec.width * s), round(sec.height * s)), Image.LANCZOS)
    tile = Image.new("RGB", (TW, TH), "white")
    tile.paste(photo, (0, 0))
    tile.paste(sec, (pw + (side - sec.width) // 2, (TH - sec.height) // 2))
    return tile


def pulled_bars_tile():
    """The five pulled bars, turned so they lie across the tile. The crop
    starts just below a strip of labelling tape."""
    im = Image.open(IMG / "lab-pulled-bars.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((int(0.205 * w), int(0.262 * h), int(0.735 * w), int(0.752 * h)))
    im = im.transpose(Image.Transpose.ROTATE_90)  # grips to the left
    return fit(im, (0, 0, 1, 1))


# (name, source, crop box as fractions x0, y0, x1, y1, or a function)
TILE_SPECS = [
    ("calphad", "scheil-al-cu-si.png", (0.293, 0.105, 0.70, 0.835)),
    ("charge", charge_tile, None),
    ("atomize", "lab-atomizer-melting.jpg", (0.0, 0.09, 1.0, 0.91)),
    ("sieve", "render-sieve.png", (0.20, 0.25, 0.725, 0.95)),
    ("print", "lab-aconity-plate-bars.jpg", (0.03, 0.25, 0.97, 0.78)),
    ("density", "render-vhx.png", (0.22, 0.12, 0.78, 0.86)),
    ("tensile", pulled_bars_tile, None),
    ("corrosion", "lab-cubxl-gantry.jpg", (0.19, 0.11, 0.90, 0.97)),
]


def make_tiles():
    for name, src, box in TILE_SPECS:
        tile = src() if callable(src) else fit(Image.open(IMG / src).convert("RGB"), box)
        tile.save(TILES / f"{name}.jpg", quality=90)
    print("wrote", len(TILE_SPECS), "tiles to", TILES)


# ---------------------------------------------------------------- figure

# Only the text faces: matplotlib files Aptos Display, Narrow, Serif and Mono
# under the family "Aptos" too (it scans ~/.local/share/fonts by itself), and
# would pick Display for bold and italic.
KEEP = ("Aptos", "Aptos-Bold", "Aptos-Italic", "Aptos-Bold-Italic")
for stem in KEEP:
    f = Path.home() / ".local/share/fonts/aptos" / f"{stem}.ttf"
    if f.exists():
        font_manager.fontManager.addfont(str(f))
font_manager.fontManager.ttflist = [f for f in font_manager.fontManager.ttflist
                                    if f.name != "Aptos" or Path(f.fname).stem in KEEP]
_names = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((n for n in ("Aptos", "Lato", "DejaVu Sans") if n in _names), "DejaVu Sans")
plt.rcParams.update({"font.family": FONT, "pdf.fonttype": 42, "svg.fonttype": "none",
                     "image.composite_image": False})  # one embedded image per tile

INK, MUTED, LINE = "#262626", "#595959", "#7F7F7F"
NAME_PT, BODY_PT, INPUT_PT = 16, 13, 13.5
LH = 1.18 / 72  # line height per point of font size, in inches

W, H = 13.333, 4.1  # inches: the width of a 16:9 slide
TW_IN = 1.30  # tile width in inches
TH_IN = TW_IN * TH / TW
Y_ROW = 2.63  # centre line of the main row
X0 = 0.40  # left edge of the first tile
STEP = 1.66  # tile-to-tile pitch
T_TW = 1.15  # test tiles
T_TH = T_TW * TH / TW


def tile(ax, name, xc, yc, w, h, render=False):
    im = Image.open(TILES / f"{name}.jpg")
    ax.imshow(im, extent=(xc - w / 2, xc + w / 2, yc - h / 2, yc + h / 2), zorder=2,
              interpolation="antialiased")
    ax.add_patch(Rectangle((xc - w / 2, yc - h / 2), w, h, fill=False, ec="#A6A6A6", lw=0.8, zorder=3))
    if render:
        ax.text(xc + w / 2 - 0.05, yc - h / 2 + 0.05, "render", ha="right", va="bottom", fontsize=10,
                color="white", zorder=4,
                bbox=dict(boxstyle="round,pad=0.18,rounding_size=0.12", fc="#404040", ec="none", alpha=0.85))
    return (xc - w / 2, yc - h / 2, xc + w / 2, yc + h / 2)


def block(ax, x, y_top, lines, ha="center"):
    """Lines of (text, kind) stacked down from y_top; kind is 'name',
    'body' or 'time'. Returns the y of the bottom of the block."""
    y = y_top
    for text, kind in lines:
        pt = NAME_PT if kind == "name" else BODY_PT
        y -= pt * LH
        ax.text(x, y, text, ha=ha, va="baseline", fontsize=pt, color=INK if kind != "time" else MUTED,
                fontweight="bold" if kind == "name" else "normal",
                fontstyle="italic" if kind == "time" else "normal", zorder=5)
    return y


def arrow(ax, p, q, dashed=False, lw=1.6, color=LINE, head=True):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>" if head else "-", mutation_scale=15, lw=lw,
                                 color=color, linestyle=(0, (5, 3)) if dashed else "-",
                                 shrinkA=0, shrinkB=0, zorder=1, capstyle="butt", joinstyle="miter"))


def path(ax, pts, dashed=False, lw=1.6, color=LINE):
    """A polyline whose last segment ends in an arrowhead."""
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, ls=(0, (5, 3)) if dashed else "-", zorder=1,
            solid_capstyle="butt", dash_capstyle="butt", solid_joinstyle="miter")
    arrow(ax, pts[-2], pts[-1], dashed=dashed, lw=lw, color=color)


MAIN = [
    ("calphad", [("CALPHAD", "name"), ("strengthening", "body"), ("phase, freezing", "body"),
                 ("range, Al₃Zr and", "body"), ("Al₃Sc nucleants", "body"), ("minutes", "time")], False),
    ("charge", [("Charge", "name"), ("machined cup and", "body"), ("plug, filled by", "body"),
                ("the powder doser", "body"), ("minutes", "time")], False),
    ("atomize", [("Atomize,", "name"), ("rePOWDER", "name"), ("size distribution,", "body"),
                 ("flow, oxygen", "body"), ("a day", "time")], False),
    ("sieve", [("Sieve", "name"), ("powder under", "body"), ("63 µm, and the", "body"),
               ("fraction kept", "body"), ("an hour", "time")], True),
    ("print", [("Print,", "name"), ("Aconity MIDI", "name"), ("cubes, walls,", "body"),
               ("tensile bars,", "body"), ("corrosion coupons", "body"), ("days", "time")], False),
    ("density", [("Density", "name"), ("relative density,", "body"), ("pores, cracks", "body"),
                 ("hours", "time")], True),
]
TESTS = [
    ("tensile", [("Tensile", "name"), ("strength,", "body"), ("elongation", "body"), ("days", "time")], False),
    ("corrosion", [("Corrosion", "name"), ("pitting potential", "body"), ("in 3.5% NaCl", "body"),
                   ("an hour", "time"), ("IGC, salt spray", "body"), ("days to weeks", "time")], False),
]


def make_figure():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")

    boxes = {}
    for i, (name, lines, render) in enumerate(MAIN):
        xc = X0 + TW_IN / 2 + i * STEP
        boxes[name] = tile(ax, name, xc, Y_ROW, TW_IN, TH_IN, render)
        block(ax, xc, Y_ROW - TH_IN / 2 - 0.06, lines)
    names = [m[0] for m in MAIN]
    for a, b in zip(names, names[1:]):
        arrow(ax, (boxes[a][2] + 0.04, Y_ROW), (boxes[b][0] - 0.04, Y_ROW))

    # Tests: tensile above the row's centre line, corrosion below, labels to the right
    xt = boxes["density"][2] + 0.47 + T_TW / 2
    yts = [Y_ROW + 0.70, Y_ROW - 0.70]
    xb = boxes["density"][2] + 0.20  # where the branch turns
    for (name, lines, render), yt in zip(TESTS, yts):
        boxes[name] = tile(ax, name, xt, yt, T_TW, T_TH, render)
        block(ax, boxes[name][2] + 0.10, boxes[name][3] + 0.03, lines, ha="left")
        path(ax, [(boxes["density"][2] + 0.04, Y_ROW), (xb, Y_ROW), (xb, yt), (boxes[name][0] - 0.04, yt)])

    # Inputs, entering where they are set
    y_in = Y_ROW + TH_IN / 2 + 0.44  # baseline of the last input line
    y_bar = Y_ROW + TH_IN / 2 + 0.22

    def inputs(xc, lines):
        n = len(lines)
        for k, t in enumerate(lines):
            ax.text(xc, y_in + (n - 1 - k) * INPUT_PT * LH, t, ha="center", va="baseline",
                    fontsize=INPUT_PT, fontstyle="italic", color=INK)

    xs = [(boxes[n][0] + boxes[n][2]) / 2 for n in names]
    top = Y_ROW + TH_IN / 2 + 0.04
    xm = (xs[0] + xs[1]) / 2
    inputs(xm, ["composition:", "Zn+Mg, Cu, Zr, Sc"])
    ax.plot([xm, xm], [y_in - 0.1, y_bar], color=LINE, lw=1.6, zorder=1)
    for x in xs[:2]:
        path(ax, [(xm, y_bar), (x, y_bar), (x, top)])
    inputs(xs[2], ["atomizer", "setting"])
    arrow(ax, (xs[2], y_in - 0.1), (xs[2], top))
    inputs(xs[4], ["laser power,", "scan speed"])
    arrow(ax, (xs[4], y_in - 0.1), (xs[4], top))

    # Each result updates the models, which choose the next step
    y_fb = 0.38
    x_fb = 0.16
    corr = boxes["corrosion"]
    x_down = (corr[0] + corr[2]) / 2
    path(ax, [(x_down, corr[1] - 0.04), (x_down, y_fb), (x_fb, y_fb), (x_fb, Y_ROW),
              (boxes["calphad"][0] - 0.04, Y_ROW)], dashed=True)
    ax.text((x_fb + x_down) / 2, y_fb, "each result updates the models, which choose the next step by "
            "expected gain per cost", ha="center", va="center", fontsize=BODY_PT, fontstyle="italic",
            color=INK, zorder=5, bbox=dict(fc="white", ec="none", pad=4))

    ax.text(W - 0.1, 0.06, "Photographs: our laboratory (the plate was printed on the University of "
            "Utah's Aconity MIDI). Sieve and density: renders from byu-vcl PR 318. "
            "CALPHAD: our Thermo-Calc Scheil calculation for an Al-Cu-Si alloy.", ha="right",
            va="bottom", fontsize=9.5, color="#8C8C8C")

    for ext, kw in (("png", dict(dpi=220)), ("pdf", dict(dpi=400))):
        out = HERE / f"al-lpbf-network.{ext}"
        fig.savefig(out, facecolor="white", **kw)
        print("wrote", out)
    plt.close(fig)


if __name__ == "__main__":
    make_tiles()
    make_figure()
