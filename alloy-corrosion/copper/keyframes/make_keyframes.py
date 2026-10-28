"""Keyframes of the copper spot animation, for print. Renders chosen moments of
../render_cubxl_cu.py at 2560 x 1440 without its text (top bar, tool panel, caption, labels,
plot insets, the illustrative Nyquist plot), then lays them out as a reel. The scene, the deck state and the camera at each
moment are the animation's own: this file only picks times and crops.

Writes, next to this file:
- frames/NN-<slug>.png: the full 3D frame at each moment, 2560 x 1440
- reel.png: one strip, 6.5 in wide at 300 dpi; panels (i), (ii), ... and one line each, 8 pt Times New Roman
- reel_2rows.png: the same panels in two rows
- keyframes.json: times, MP4 frame numbers, sub-steps, crops

The animation meshes three STEP files from the electromagnetic capper module, which stayed in
byu-vcl (modules/electromagnetic-capper/cad/); point --capper-cad at a folder holding them.

    xvfb-run -a python make_keyframes.py --capper-cad /tmp/capper-cad   # frames and reels, under a minute
    python make_keyframes.py --reel-only                                  # reels from frames/
    xvfb-run -a python make_keyframes.py --capper-cad /tmp/capper-cad --check   # vs the MP4
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
COPPER = HERE.parent
sys.path.insert(0, str(COPPER))

SCALE = 2  # 2 x the animation's 1280 x 720
FPS = 30  # render_cubxl_cu.FPS
DPI = 300
REEL_W_IN = 6.5
PT = 8  # label size, points
GAP_IN = 0.04
FONT_FILES = ["/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
              "/usr/share/fonts/truetype/msttcorefonts/times.ttf",
              "/Library/Fonts/Times New Roman.ttf", "C:/Windows/Fonts/times.ttf"]

# Each moment: (slug, frame number in cubxl-cu-spot.mp4 (30 fps, so t = n / 30 s), chapter, the
# script's sub-step there, the tool action lit at that moment, the reel's line, crop centre x, y
# and width in the animation's 1280 x 720 pixels). Crops share the panel aspect, PANEL_ASPECT.
PANEL_ASPECT = 4 / 3
KEYS = [
    ("specimens-lids", 449, "placing the modules", "deck module 4 of 14, 'Well lids, FKM O-rings', coming down onto module 2, 'Specimens: Cu–Ni, NAB, DED', and module 3, 'PTFE blank on S4'",
     "", "Specimens, lids", (690, 335, 260)),
    ("seawater-fill", 2236, "one spot", "2  The capper lifts the seawater cap; the P20 builds the well from 135 µL of ASTM D1141 seawater (7 transfers)",
     "P20 pipette: dispenses into well S1, above the meniscus", "Seawater fill", (630, 260, 480)),
    ("electrode-cap", 2805, "one spot", "5  The capper carries the electrode cap (leak-free Ag/AgCl, Pt coil) from its park cup and sets it over S1's boss",
     "Capper: sets the cap over S1's boss", "Electrode cap", (720, 290, 640)),
    ("measure", 3017, "one spot", "6  Measured with the cap on: OCP 20 min, EIS at OCP 10 min (10 mV rms, 100 kHz to 10 mHz, on the requested "
     "potentiostat), LPR ±10 mV, rest 5 min, +50 mV hold 10 min, OCP 5 min. The head is free meanwhile",
     "Potentiostat: OCP, EIS, LPR, hold: the head is free", "OCP, EIS, LPR", (617, 390, 480)),
    ("cap-rinse", 3254, "one spot", "7  The magnet lifts the cap off S1; it is dipped in DI water, then seawater, and parked",
     "Capper: dips the cap in DI water", "Cap rinsed", (550, 240, 420)),
    ("icp-sample", 3510, "one spot", "8  A new tip moves the 150 µL, then a 150 µL DI rinse, into tube 1 for ICP-MS",
     "P20 pipette: dispenses into tube 1", "ICP-MS sample", (560, 370, 560)),
    ("spot-imaged", 3867, "one spot", "10  The head camera images the spot. Next spot: S2",
     "Head camera: images the spot", "Spot imaged", (740, 240, 480)),
]
ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]


def load_renderer(capper_cad, scale):
    """The animation's Renderer, with a bigger window and line widths scaled to match."""
    import render_cubxl_cu as rc
    assert rc.FPS == FPS
    rc.W, rc.H = 1280 * scale, 720 * scale
    if capper_cad:
        rc.CAD = Path(capper_cad).resolve()
    sil = rc.Scene.silhouette

    def silhouette(self, key):
        act = sil(self, key)
        act.GetProperty().SetLineWidth(3.5 * scale)
        return act
    rc.Scene.silhouette = silhouette
    r = rc.Renderer()
    r.scene.actors["wv"].prop.line_width = 1.2 * scale
    return rc, r


def raw_frame(rc, r, t):
    """Renderer.frame(t) for the placement and run chapters, without the 2D overlays."""
    v, s = r.v, r.v.story
    kind = v.kind(t)
    if kind == "place":
        return r.render3d(v.place.state(t), rc.interp_cam(v.place.cams(), t))
    if kind == "run":
        st = rc.run_state(s, t)
        m0, m1 = s.measure
        st["closeup"] = m0 + 0.8 <= t <= m1 + 0.1
        return r.render3d(st, rc.interp_cam(s.cams, t))
    raise ValueError(f"t = {t} s is in the {kind} chapter, which has no 3D scene to re-render")


def tnr(px):
    for f in FONT_FILES:
        if Path(f).exists():
            return ImageFont.truetype(f, px), f
    sys.exit("Times New Roman not found: install ttf-mscorefonts-installer (or add its path to FONT_FILES)")


def crop(img, box, scale):
    cx, cy, w = box
    h = w / PANEL_ASPECT
    x0, y0 = int(round((cx - w / 2) * scale)), int(round((cy - h / 2) * scale))
    return img.crop((x0, y0, x0 + int(round(w * scale)), y0 + int(round(h * scale))))


def reel(panels, labels, cols, out):
    """Panels in rows of `cols` (a short last row is centred), 6.5 in wide at 300 dpi, one
    8 pt line under each. Fails if two neighbouring lines come closer than 0.04 in."""
    W = int(round(REEL_W_IN * DPI))
    gap = int(round(GAP_IN * DPI))
    px = PT / 72 * DPI  # 8 pt = 33.3 px at 300 dpi
    fnt, _ = tnr(px)
    pw = (W - gap * (cols - 1)) // cols
    ph = int(round(pw / PANEL_ASPECT))
    pad = int(round(0.3 * px))
    rows = math.ceil(len(panels) / cols)
    row_h = ph + pad + int(round(px * 1.15))
    H = rows * row_h + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    spans = []
    for i, (p, lab) in enumerate(zip(panels, labels)):
        r_, c_ = divmod(i, cols)
        n_row = min(cols, len(panels) - r_ * cols)
        x = (W - (pw * n_row + gap * (n_row - 1))) // 2 + c_ * (pw + gap)
        y = r_ * (row_h + gap)
        sheet.paste(p.resize((pw, ph), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + pw - 1, y + ph - 1], outline=(200, 198, 192), width=1)
        text = f"({ROMAN[i]}) {lab}"
        tw = d.textlength(text, font=fnt)
        spans.append((r_, x + pw / 2 - tw / 2, x + pw / 2 + tw / 2))
        d.text((x + pw / 2, y + ph + pad), text, font=fnt, fill="black", anchor="ma")
    clear = min((b[1] - a[2] for a, b in zip(spans, spans[1:]) if a[0] == b[0]), default=W)
    if clear < gap:
        sys.exit(f"{out.name}: two labels are {clear:.0f} px apart; shorten one")
    sheet.save(out, dpi=(DPI, DPI), optimize=True)
    return {"file": out.name, "px": [W, H], "in": [round(W / DPI, 3), round(H / DPI, 3)], "panel_px": [pw, ph],
            "label_px": round(px, 2), "min_label_clearance_px": round(clear, 1),
            "widest_label_vs_panel_px": [round(max(s[2] - s[1] for s in spans), 1), pw]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capper-cad", default="", help="folder with the capper module's three STEP files (from byu-vcl)")
    ap.add_argument("--reel-only", action="store_true", help="re-lay out the reels from frames/, no rendering")
    ap.add_argument("--probe", default="", help="comma-separated times: render full frames to /tmp/kf_probe_<t>.png and stop")
    ap.add_argument("--check", action="store_true", help="re-render each moment with the overlays at 1280 x 720 and compare with the MP4")
    args = ap.parse_args()
    frames_dir = HERE / "frames"
    frames_dir.mkdir(exist_ok=True)

    if args.check:
        return check(args.capper_cad)
    if args.probe:
        rc, r = load_renderer(args.capper_cad, SCALE)
        for t in (float(x) for x in args.probe.split(",")):
            Image.fromarray(raw_frame(rc, r, t)).save(f"/tmp/kf_probe_{t:06.2f}.png")
            print("probe", t, flush=True)
        return

    files = [frames_dir / f"{i + 1:02d}-{k[0]}.png" for i, k in enumerate(KEYS)]
    if not args.reel_only:
        rc, r = load_renderer(args.capper_cad, SCALE)
        for f in frames_dir.glob("*.png"):
            f.unlink()
        for (slug, n, *_), f in zip(KEYS, files):
            Image.fromarray(raw_frame(rc, r, n / FPS)).save(f, optimize=True)
            print("frame", f.name, flush=True)
    frames = [Image.open(f).convert("RGB") for f in files]
    scale = frames[0].size[0] / 1280
    panels = [crop(im, k[6], scale) for im, k in zip(frames, KEYS)]
    labels = [k[5] for k in KEYS]
    out = {"reels": [reel(panels, labels, len(KEYS), HERE / "reel.png"),
                     reel(panels, labels, math.ceil(len(KEYS) / 2), HERE / "reel_2rows.png")],
           "font": tnr(10)[1], "fps": FPS, "frame_px": list(frames[0].size), "panel_aspect": PANEL_ASPECT, "frames": []}
    for i, ((slug, n, chapter, step, action, label, box), f) in enumerate(zip(KEYS, files)):
        out["frames"].append({"panel": f"({ROMAN[i]})", "file": f"frames/{f.name}", "mp4_frame": n, "t_s": round(n / FPS, 3),
                              "chapter": chapter, "sub_step": step, "lit_action": action, "label": label,
                              "crop_1280x720": {"cx": box[0], "cy": box[1], "w": box[2], "h": round(box[2] / PANEL_ASPECT, 1)}})
    (HERE / "keyframes.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for rl in out["reels"]:
        print(rl["file"], rl["px"], rl["in"], "panel", rl["panel_px"], "label clearance", rl["min_label_clearance_px"], flush=True)


def check(capper_cad):
    """Each moment's full animation frame (with overlays), re-rendered at 1280 x 720, vs the MP4."""
    import subprocess
    import imageio_ffmpeg
    rc, r = load_renderer(capper_cad, 1)
    mp4 = COPPER / "cubxl-cu-spot.mp4"
    res = []
    for slug, n, *_ in KEYS:
        mine = np.asarray(Image.fromarray(r.frame(n / FPS)).convert("RGB"), float)
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", str(mp4), "-vf",
                              f"select=between(n\\,{n - 1}\\,{n + 1})", "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             check=True, capture_output=True).stdout
        vids = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3).astype(float)
        psnr = []
        for vid in vids:  # MP4 frames n - 1, n, n + 1: the match should peak at n
            mse = float(np.mean((mine - vid) ** 2))
            psnr.append(round(10 * math.log10(255 ** 2 / mse), 1) if mse else float("inf"))
        res.append({"slug": slug, "mp4_frame": n, "psnr_db_vs_frames_n-1_n_n+1": psnr})
        Image.fromarray(np.hstack([mine, vids[1]]).astype(np.uint8)).save(f"/tmp/kf_check_{slug}.png")
        print(slug, n, "PSNR (dB) vs MP4 frames n-1, n, n+1:", psnr, flush=True)
    (HERE / "check_vs_mp4.json").write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
