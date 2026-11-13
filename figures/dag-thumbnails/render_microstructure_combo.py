"""Build microstructure_combo.png — a 3-panel horizontal composite for
DAG node 7b (Microstructure SEM/EDS, EBSD, XRD).

Panels (left → right):
  1. SEM micrograph (matched to the EDS overlay; extracted from the EDAX
     report PDF page 1) with the SEM stub photo as a small inset in the
     bottom-right corner — physical sample plus matching microstructure
     in a single panel.
  2. EDS Element Overlay (Al-blue 88%, Si-yellow 6%, O-green 3%,
     Mg-red 2%) with legend, extracted from the EDAX report PDF page 2.
     Tightly cropped to drop white margins.
  3. EDS spectrum (Al, Si, Mg, O peaks) — EDAX Octane Plus.

The SEM in panel 1 is the bottom (greyscale) image on report page 1,
which is the *same field of view* as the element overlay on page 2;
this guarantees the SEM ↔ EDS map registration.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "figures" / "dag-thumbnails" / "microstructure"
OUT = ROOT / "figures" / "dag-thumbnails" / "microstructure_combo.png"

PANEL_H = 720
GAP = 14
BG = (255, 255, 255)


def fit_height(img: Image.Image, h: int) -> Image.Image:
    w = int(img.width * h / img.height)
    return img.resize((w, h), Image.LANCZOS)


def fit_width(img: Image.Image, w: int) -> Image.Image:
    h = int(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)


def label(img: Image.Image, text: str) -> None:
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28
        )
    except OSError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img, "RGBA")
    pad = 8
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box = [pad, pad, pad + tw + 14, pad + th + 10]
    draw.rectangle(box, fill=(255, 255, 255, 230))
    draw.text((pad + 7, pad + 3), text, fill=(0, 0, 0, 255), font=font)


def main() -> None:
    # ---- Panel 1: SEM (matched to EDS overlay) from report PDF p.1 ------
    p1 = Image.open(SRC / "eds_report_p1.png").convert("RGB")
    sem = p1.crop((85, 1217, 770, 1790))   # bottom SEM, same FOV as overlay
    sem = fit_height(sem, PANEL_H)

    # Inset: stub photo, square crop, scaled to ~32% of SEM panel width,
    # placed in the bottom-right with a thin black border.
    stub = Image.open(SRC / "stub.jpg").convert("RGB")
    stub = stub.crop((800, 1500, 2200, 2900))  # 1400x1400
    inset_w = int(sem.width * 0.32)
    stub = fit_width(stub, inset_w)
    inset_pad = 12
    border = 3
    ix = sem.width - stub.width - inset_pad
    iy = sem.height - stub.height - inset_pad
    draw = ImageDraw.Draw(sem)
    draw.rectangle(
        [ix - border, iy - border, ix + stub.width + border, iy + stub.height + border],
        fill=(0, 0, 0),
    )
    sem.paste(stub, (ix, iy))
    label(sem, "SEM + stub (inset)")

    # ---- Panel 2: EDS Element Overlay + legend, tightly cropped ----------
    p2 = Image.open(SRC / "eds_report_p2.png").convert("RGB")
    overlay = p2.crop((85, 200, 1180, 765))  # map + legend, with scale bar
    overlay = fit_height(overlay, PANEL_H)
    label(overlay, "EDS overlay")

    # ---- Panel 3: EDS spectrum, trim status footer -----------------------
    spec = Image.open(SRC / "eds_spectrum.png").convert("RGB")
    spec = spec.crop((0, 0, spec.width, spec.height - 30))
    spec = fit_height(spec, PANEL_H)
    label(spec, "EDS spectrum")

    panels = [sem, overlay, spec]
    total_w = sum(p.width for p in panels) + GAP * (len(panels) - 1)
    combo = Image.new("RGB", (total_w, PANEL_H), BG)
    x = 0
    for p in panels:
        combo.paste(p, (x, 0))
        x += p.width + GAP
    combo.save(OUT, dpi=(300, 300))
    print(f"Wrote {OUT}  size={combo.size}")


if __name__ == "__main__":
    main()
