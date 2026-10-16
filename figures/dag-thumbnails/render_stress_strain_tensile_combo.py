#!/usr/bin/env python3
"""Build stress_strain_tensile_combo.png — side-by-side composite for the
ch4 (tensile) DAG node thumbnail.

Left:  In-house BYU AlSi10Mg engineering stress-strain curve with sample
       inset (`stress-strain-sample-5-image-inset.png`).
Right: MTS Landmark 100-kip axial-torsional load frame photo
       (`genesis-mission-proposal/figures/equipment/tensile-100kip.jpg`).
"""

from pathlib import Path

from PIL import Image, ImageChops

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

OUT = HERE / "stress_strain_tensile_combo.png"
LEFT = HERE / "in-house-tensile-data" / "stress-strain-sample-5-image-inset.png"
RIGHT = REPO_ROOT / "genesis-mission-proposal" / "figures" / "equipment" / "tensile-100kip.jpg"

TARGET_H = 720
GAP_PX = 12
BG = (255, 255, 255)


def trim_white(img, pad=4):
    bbox = ImageChops.difference(img, Image.new("RGB", img.size, BG)).getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img.size[0], x1 + pad)
    y1 = min(img.size[1], y1 + pad)
    return img.crop((x0, y0, x1, y1))


def fit_to_height(img, h):
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, BG)
        bg.paste(img, mask=img.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")
    img = trim_white(img)
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
