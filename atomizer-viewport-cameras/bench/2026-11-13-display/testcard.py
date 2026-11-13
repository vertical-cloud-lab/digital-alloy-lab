"""Draw an 800 x 480 test card for checking a small HDMI panel's mode by eye.

A 1 px border on the outermost pixels, corner marks, a 50 px grid, a circle (round only
if the pixels are square), 1 px and 2 px line pairs, and colour bars.
Usage: python3 testcard.py out.png [WIDTH HEIGHT]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
W, H = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (800, 480)
im = Image.new("RGB", (W, H), (24, 24, 24))
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    small = ImageFont.truetype("DejaVuSans.ttf", 14)
except OSError:
    font = small = ImageFont.load_default()

for x in range(0, W, 50):
    d.line([(x, 0), (x, H - 1)], fill=(60, 60, 60))
for y in range(0, H, 50):
    d.line([(0, y), (W - 1, y)], fill=(60, 60, 60))
bars = [(255, 255, 255), (255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 0, 0), (0, 0, 255), (0, 0, 0)]
bw = W // len(bars)
for i, c in enumerate(bars):
    d.rectangle([i * bw, H - 70, (i + 1) * bw - 1, H - 31], fill=c)
for i in range(W):  # grey ramp
    g = round(255 * i / (W - 1))
    d.line([(i, H - 30), (i, H - 12)], fill=(g, g, g))
r = min(W, H) // 2 - 70
cx, cy = W // 2, (H - 70) // 2 + 10
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255))
d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255))
for k in range(12):  # 1 px on/off pairs, then 2 px
    d.line([(40 + 2 * k, 120), (40 + 2 * k, 200)], fill=(255, 255, 255))
    d.rectangle([90 + 4 * k, 120, 91 + 4 * k, 200], fill=(255, 255, 255))
d.text((40, 205), "1 px   2 px", font=small, fill=(220, 220, 220))
d.rectangle([0, 0, W - 1, H - 1], outline=(255, 0, 0))  # outermost pixels
for (x, y, sx, sy) in [(0, 0, 1, 1), (W - 1, 0, -1, 1), (0, H - 1, 1, -1), (W - 1, H - 1, -1, -1)]:
    d.line([(x, y), (x + 30 * sx, y)], fill=(255, 255, 255), width=1)
    d.line([(x, y), (x, y + 30 * sy)], fill=(255, 255, 255), width=1)
d.text((40, 30), f"{W} x {H} test card", font=font, fill=(255, 255, 255))
d.text((40, 60), "Red 1 px border on all four edges? Circle round?", font=small, fill=(220, 220, 220))
d.text((40, 80), "1 px lines separate? Then the mode is the panel's own.", font=small, fill=(220, 220, 220))
im.save(out)
print(out, im.size)
