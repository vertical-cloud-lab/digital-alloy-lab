#!/usr/bin/env python3
"""Build phase2_applications_combo.png — 5 equal-height square tiles
horizontally composited for the ph2 (Phase II) node thumbnail.

All 5 tiles are real LPBF-Al component photos sourced from public
manufacturer/operator imagery, illustrating the breadth of commercial
applications targeted by the Phase II production pipeline.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent
PARTS_DIR = OUT_DIR / "commercial-am-parts"
OUT = OUT_DIR / "phase2_applications_combo.png"

REAL_TILES = [
    PARTS_DIR / "A20X-with-logo.png",
    PARTS_DIR / "scalmalloy-(probably)-antenna-support-bracket.png",
    PARTS_DIR / "AlSi40-athermal-mirror-with-logo.png",
    PARTS_DIR / "AlSi10Mg-Dalian-1-frame-with-logo.png",
    PARTS_DIR / "AlSi7Mg-with-logo.png",
]
N_PLACEHOLDERS = 0

TILE_PX = 512
GAP_PX = 12
BG = (255, 255, 255)
PLACEHOLDER_FILL = (232, 232, 232)
PLACEHOLDER_EDGE = (170, 170, 170)
PLACEHOLDER_TEXT = (120, 120, 120)


def _load_font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_to_square(img, size, bg=BG):
    """Resize preserving aspect ratio, paste centered onto square bg."""
    img = img.convert("RGB")
    w, h = img.size
    scale = size / max(w, h)
    new_w, new_h = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    img_r = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (size, size), bg)
    canvas.paste(img_r, ((size - new_w) // 2, (size - new_h) // 2))
    return canvas


def make_placeholder(size):
    canvas = Image.new("RGB", (size, size), PLACEHOLDER_FILL)
    draw = ImageDraw.Draw(canvas)
    # dashed border
    dash, gap = 14, 8
    inset = 6
    for x in range(inset, size - inset, dash + gap):
        draw.line([(x, inset), (min(x + dash, size - inset), inset)],
                  fill=PLACEHOLDER_EDGE, width=2)
        draw.line([(x, size - inset), (min(x + dash, size - inset), size - inset)],
                  fill=PLACEHOLDER_EDGE, width=2)
    for y in range(inset, size - inset, dash + gap):
        draw.line([(inset, y), (inset, min(y + dash, size - inset))],
                  fill=PLACEHOLDER_EDGE, width=2)
        draw.line([(size - inset, y), (size - inset, min(y + dash, size - inset))],
                  fill=PLACEHOLDER_EDGE, width=2)
    font = _load_font(int(size * 0.085))
    text = "(future\napplication)"
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=6)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        text, fill=PLACEHOLDER_TEXT, font=font, align="center", spacing=6,
    )
    return canvas


def main():
    tiles = []
    for p in REAL_TILES:
        if not p.exists():
            raise FileNotFoundError(p)
        tiles.append(fit_to_square(Image.open(p), TILE_PX))
    for _ in range(N_PLACEHOLDERS):
        tiles.append(make_placeholder(TILE_PX))

    n = len(tiles)
    total_w = n * TILE_PX + (n - 1) * GAP_PX
    combo = Image.new("RGB", (total_w, TILE_PX), BG)
    for i, t in enumerate(tiles):
        combo.paste(t, (i * (TILE_PX + GAP_PX), 0))
    combo.save(OUT, dpi=(300, 300))
    print(f"Wrote {OUT} {combo.size}")


if __name__ == "__main__":
    main()
