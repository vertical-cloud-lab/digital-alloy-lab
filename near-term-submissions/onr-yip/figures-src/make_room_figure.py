"""Fig. enclosure (a): the atomizer room from its stream camera, beside the installed atomizer.

Sterling's Oct 27 review (issue 212): use a stream-camera frame in which no one is in the room.

* Left: the 720p frame the stream camera took on 1 October 2026 at 17:01 (room empty), from
  vertical-cloud-lab/byu-vcl (public), docs/images/stream-cam-picam-ot2-720p-2026-10-01.jpg at
  64b7891, copied to img/stream-cam-room-2026-10-01-1701.jpg (sha256 dc84fefd...0cfa7). Cropped to
  x 300-1280, y 50-720, which drops the timestamp overlay and the curtain.
* Right: img/atomizer-installed-2026-09-28.jpg, resized to the same 670 px height.
* A 24 px white gap between them; JPEG quality 92.

    python make_room_figure.py   # writes ../figures-cu-ded/room-atomizer-2026.jpg
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOM = HERE / "img" / "stream-cam-room-2026-10-01-1701.jpg"
ATOMIZER = HERE / "img" / "atomizer-installed-2026-09-28.jpg"
OUT = HERE.parent / "figures-cu-ded" / "room-atomizer-2026.jpg"
CROP = (300, 50, 1280, 720)  # x0, y0, x1, y1 of the 1280 x 720 frame
GAP = 24

room = Image.open(ROOM).convert("RGB")
assert room.size == (1280, 720), room.size
left = room.crop(CROP)
h = left.height
right = Image.open(ATOMIZER).convert("RGB")
right = right.resize((round(right.width * h / right.height), h), Image.LANCZOS)

fig = Image.new("RGB", (left.width + GAP + right.width, h), "white")
fig.paste(left, (0, 0))
fig.paste(right, (left.width + GAP, 0))
fig.save(OUT, quality=92, optimize=True)
print(f"wrote {OUT.name}: {fig.width} x {fig.height} (left {left.width} x {h}, right {right.width} x {h})")
