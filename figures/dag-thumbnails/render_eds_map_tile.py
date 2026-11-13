"""Build EDS 2x2 map tile + pqc_combo (SEM LHS + 2x2 EDS RHS).

Crops Element Overlay (page 2) and Mg/Al/Si K maps (page 3) from the
AlSi10Mg-40-Micron-Mapping report, tiles 2x2 with element labels, and
composites with the SEM image to produce pqc_combo.png.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
EDS = ROOT / "figures" / "eds-reports"
SEM = ROOT / "figures" / "sem" / "AlSi10Mg_40um_SEM_hires.png"
OUT_DIR = ROOT / "figures" / "dag-thumbnails"
TILE_OUT = OUT_DIR / "eds_maps_2x2.png"
COMBO_OUT = OUT_DIR / "pqc_combo.png"

CELL = 480
LABEL_H = 0  # label burned into image instead of separate row

def crop_panel(img, box):
    return img.crop(box).resize((CELL, CELL), Image.LANCZOS)

def label(img, text, font):
    draw = ImageDraw.Draw(img, "RGBA")
    pad = 8
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box = [pad, pad, pad + tw + 12, pad + th + 8]
    draw.rectangle(box, fill=(255, 255, 255, 220))
    draw.text((pad + 6, pad + 2), text, fill=(0, 0, 0, 255), font=font)

def main():
    p2 = Image.open(EDS / "AlSi10Mg-40-Micron-Mapping-page-2.png").convert("RGB")
    p3 = Image.open(EDS / "AlSi10Mg-40-Micron-Mapping-page-3.png").convert("RGB")
    overlay = crop_panel(p2, (85, 157, 635, 591))
    mg      = crop_panel(p3, (85, 126, 635, 560))
    al      = crop_panel(p3, (85, 570, 635, 1004))
    si      = crop_panel(p3, (85, 1013, 635, 1447))

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except OSError:
        font = ImageFont.load_default()

    label(overlay, "Overlay", font)
    label(al, "Al K", font)
    label(si, "Si K", font)
    label(mg, "Mg K", font)

    GAP = 8
    tile = Image.new("RGB", (2 * CELL + GAP, 2 * CELL + GAP), (255, 255, 255))
    tile.paste(overlay, (0, 0))
    tile.paste(al, (CELL + GAP, 0))
    tile.paste(si, (0, CELL + GAP))
    tile.paste(mg, (CELL + GAP, CELL + GAP))
    tile.save(TILE_OUT, dpi=(300, 300))
    print("Wrote", TILE_OUT, tile.size)

    # ---- pqc_combo: SEM LHS + 2x2 tile RHS, equal H -------------------------
    H = 720
    sem = Image.open(SEM).convert("RGB")
    sem_w = int(sem.width * H / sem.height)
    sem_r = sem.resize((sem_w, H), Image.LANCZOS)
    tile_w = int(tile.width * H / tile.height)
    tile_r = tile.resize((tile_w, H), Image.LANCZOS)
    GAP2 = 14
    combo = Image.new("RGB", (sem_r.width + GAP2 + tile_r.width, H), (255, 255, 255))
    combo.paste(sem_r, (0, 0))
    combo.paste(tile_r, (sem_r.width + GAP2, 0))
    combo.save(COMBO_OUT, dpi=(300, 300))
    print("Wrote", COMBO_OUT, combo.size)

if __name__ == "__main__":
    main()
