#!/usr/bin/env python3
"""Build scheil_susceptibility_combo.png — side-by-side composite for the
tc1 (CALPHAD/Scheil) DAG node thumbnail.

Left:  AlSi10Mg Scheil curves (T vs solid fraction) with hot-tearing band.
Right: Hot-tearing susceptibility index bar chart for the same alloy set.

Both sub-images are reproduced from Riva et al., Metals 2023, 13(4), 716
(https://doi.org/10.3390/met13040716) — see SOURCES.md for provenance.
"""

from pathlib import Path

from PIL import Image

OUT_DIR = Path(__file__).resolve().parent
OUT = OUT_DIR / "scheil_susceptibility_combo.png"

LEFT = OUT_DIR / "AlSi10Mg-scheil-graph-10.3390%2Fmet13040716.png"
RIGHT = OUT_DIR / "susceptibility-index-from-scheil-AlSi10Mg-10.3390%2Fmet13040716.png"

TARGET_H = 600
GAP_PX = 12
BG = (255, 255, 255)


def fit_to_height(img, h):
    img = img.convert("RGB")
    w0, h0 = img.size
    new_w = max(1, int(round(w0 * h / h0)))
    return img.resize((new_w, h), Image.LANCZOS)


def main():
    left = fit_to_height(Image.open(LEFT), TARGET_H)
    right = fit_to_height(Image.open(RIGHT), TARGET_H)
    total_w = left.size[0] + GAP_PX + right.size[0]
    canvas = Image.new("RGB", (total_w, TARGET_H), BG)
    canvas.paste(left, (0, 0))
    canvas.paste(right, (left.size[0] + GAP_PX, 0))
    canvas.save(OUT, optimize=True)
    print(f"wrote {OUT}  ({total_w}x{TARGET_H})")


if __name__ == "__main__":
    main()
