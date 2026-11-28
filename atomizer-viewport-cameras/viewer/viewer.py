#!/usr/bin/env python3
"""Full-screen live view for a rePowder viewport camera unit (PR 189's design).

Shows one or two Raspberry Pi cameras on the unit's own display: side by side on a landscape panel, stacked on a
portrait one, each with its camera's whole field of view. Nothing is recorded, saved or sent anywhere.

On the Pi, from the desktop or over SSH (install.sh's systemd user service runs it at every boot):
    python3 viewer.py                           # every camera found (up to two), in camera-number order
    python3 viewer.py --cameras imx477 imx708   # pick by sensor model, in left-to-right order
    python3 viewer.py --rotate 90               # a panel mounted in portrait (Touch Display 2, Waveshare 2.8 in)
Without a camera, on any machine with PyQt5 or PyQt6:
    QT_QPA_PLATFORM=offscreen python3 viewer.py --fake 2 --size 800x480 --screenshot shot.png
"""
import argparse
import glob
import os
import signal
import sys
import threading
import time

import numpy as np

STALE_S = 3.0  # a tile says "no frames" once its camera has been silent this long
RESTART_S = 30.0  # a camera that failed or has been silent this long makes the viewer exit, so systemd restarts it


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cameras", nargs="+", metavar="CAM",
                   help="camera numbers or sensor models (imx477 = HQ, imx708 = Module 3), in display order")
    p.add_argument("--labels", nargs="+", metavar="TEXT", help="caption per tile (default: the sensor model)")
    p.add_argument("--fps", type=float, default=30.0)
    p.add_argument("--rotate", type=int, choices=(0, 90, 180, 270), default=0,
                   help="rotate the whole picture clockwise, for a panel mounted on its side or upside down")
    p.add_argument("--rot180", nargs="+", default=[], metavar="CAM",
                   help="turn these cameras' pictures by 180 degrees (a camera mounted upside down)")
    p.add_argument("--control", action="append", default=[], metavar="NAME=VALUE",
                   help="libcamera control for every camera, e.g. ExposureTime=2000 or AnalogueGain=1.5")
    p.add_argument("--no-labels", action="store_true", help="no captions")
    p.add_argument("--size", help="window size WxH instead of full screen (for testing)")
    p.add_argument("--fake", type=int, metavar="N", help="N synthetic cameras instead of real ones (testing)")
    p.add_argument("--screenshot", metavar="PNG", help="save the window after --run-s seconds and quit (testing)")
    p.add_argument("--run-s", type=float, default=2.0, help="seconds before --screenshot")
    p.add_argument("--wait-display-s", type=float, default=120.0,
                   help="how long to wait for the desktop when started at boot")
    return p.parse_args(argv)


# ---------------------------------------------------------------- display environment
def find_display(wait_s):
    """Fill in WAYLAND_DISPLAY and DISPLAY when started outside the desktop (the systemd user service).

    Waits up to wait_s for the desktop's Wayland or X (Xwayland) socket, since the service can start before it."""
    run = os.environ.setdefault("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    deadline = time.monotonic() + wait_s
    while True:
        way = os.environ.get("WAYLAND_DISPLAY")
        if not (way and os.path.exists(os.path.join(run, way))):
            socks = sorted(s for s in glob.glob(os.path.join(run, "wayland-*")) if not s.endswith(".lock"))
            way = os.path.basename(socks[0]) if socks else None
            if way:
                os.environ["WAYLAND_DISPLAY"] = way
        x = os.environ.get("DISPLAY")
        if not x:
            mine = [s for s in glob.glob("/tmp/.X11-unix/X*") if os.stat(s).st_uid == os.getuid()]
            if mine:
                x = ":" + min(mine, key=lambda s: int(s.rsplit("X", 1)[1] or 0)).rsplit("X", 1)[1]
                os.environ["DISPLAY"] = x
        if way or x or time.monotonic() > deadline:
            return way, x
        time.sleep(1)


def load_qt():
    try:
        from PyQt5 import QtCore, QtGui, QtWidgets
    except ImportError:
        from PyQt6 import QtCore, QtGui, QtWidgets
    return QtCore, QtGui, QtWidgets


def pick_platform(QtCore):
    """Use Qt's Wayland plugin if it is installed, else X11 through Xwayland (PyQt5 on Raspberry Pi OS)."""
    if os.environ.get("QT_QPA_PLATFORM"):
        return
    try:
        plugins = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath)  # Qt 5
    except AttributeError:
        plugins = QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath)  # Qt 6
    if os.environ.get("WAYLAND_DISPLAY") and glob.glob(os.path.join(plugins, "platforms", "libqwayland*")):
        os.environ["QT_QPA_PLATFORM"] = "wayland"
    elif os.environ.get("DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"


# ---------------------------------------------------------------- layout and sensor modes
def tiles(width, height, n):
    """Split a width x height canvas into n equal tiles: columns if landscape, rows if portrait."""
    if width >= height:
        w = width // n
        return [(i * w, 0, w, height) for i in range(n)]
    h = height // n
    return [(0, i * h, width, h) for i in range(n)]


def fit(aspect, box_w, box_h):
    """Largest even-sized w x h with the given aspect ratio that fits in the box."""
    w, h = box_w, round(box_w / aspect)
    if h > box_h:
        w, h = round(box_h * aspect), box_h
    return max(2, w // 2 * 2), max(2, h // 2 * 2)


def pick_mode(modes, pixel_array, fps):
    """The sensor mode to view with: the whole field of view, at least fps, as many pixels as possible.

    IMX708 (Module 3): 2304x1296. IMX477 (HQ): 2028x1520, not the cropped 1332x990 that libcamera would pick for a
    small output."""
    W, H = pixel_array
    full = [m for m in modes if m["crop_limits"][2] >= 0.98 * W and m["crop_limits"][3] >= 0.98 * H]
    fast = [m for m in full if m["fps"] >= fps - 0.5]
    if fast:
        return max(fast, key=lambda m: m["size"][0] * m["size"][1])
    if full:
        return max(full, key=lambda m: m["fps"])
    return max(modes, key=lambda m: m["size"][0] * m["size"][1])


# ---------------------------------------------------------------- frame sources
class Source:
    """Keeps a camera's newest frame for the GUI thread. Frames are h x w x 4 uint8 in B, G, R, X byte order."""

    def __init__(self, label):
        self.label, self.frame, self.t_last, self.count, self.error = label, None, None, 0, None
        self.retry = True  # False for a camera that isn't there at all: restarting won't find it (power off to plug in)

    def put(self, frame):
        self.frame, self.t_last = frame, time.monotonic()
        self.count += 1

    def stop(self):
        pass


class CameraSource(Source):
    def __init__(self, info, box, fps, rot180, controls, label):
        from libcamera import Transform
        from picamera2 import Picamera2
        super().__init__(label or info["Model"])
        self.cam = Picamera2(info["Num"])
        mode = pick_mode(self.cam.sensor_modes, self.cam.camera_properties["PixelArraySize"], fps)
        aspect = mode["size"][0] / mode["size"][1]
        w = max(32, fit(aspect, *box)[0] // 32 * 32)  # a width the ISP needn't pad, so the aspect stays exact
        size = (w, round(w / aspect) // 2 * 2)
        cfg = self.cam.create_video_configuration(
            main={"size": size, "format": "XRGB8888"},
            sensor={"output_size": mode["size"], "bit_depth": mode["bit_depth"]},
            controls={"FrameRate": fps, **controls},
            transform=Transform(hflip=int(rot180), vflip=int(rot180)),
            buffer_count=4)
        self.cam.align_configuration(cfg)
        self.cam.configure(cfg)
        self.cam.post_callback = lambda request: self.put(request.make_array("main"))
        self.cam.start()
        print(f"camera {info['Num']} {info['Model']}: sensor mode {mode['size'][0]}x{mode['size'][1]} "
              f"({mode['fps']:.0f} fps max), shown at {cfg['main']['size'][0]}x{cfg['main']['size'][1]}, "
              f"{fps:g} fps{', turned 180' if rot180 else ''}", flush=True)

    def stop(self):
        self.cam.stop()
        self.cam.close()


class FakeSource(Source):
    """Moving colour bars at a camera's aspect ratio, from a thread, like a real camera's callback."""

    def __init__(self, n, box, fps, label):
        super().__init__(label or f"fake {('4:3', '16:9')[n % 2]}")
        aspect = (4 / 3, 16 / 9)[n % 2]
        self.w, self.h = fit(aspect, *box)
        self.fps, self.running = fps, True
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        bars = np.array([[255, 255, 255], [0, 255, 255], [255, 255, 0], [0, 255, 0],
                         [255, 0, 255], [0, 0, 255], [255, 0, 0], [0, 0, 0]], np.uint8)  # B, G, R
        x = np.arange(self.w)
        while self.running:
            shift = self.count * 4
            img = np.zeros((self.h, self.w, 4), np.uint8)
            img[:, :, :3] = bars[((x + shift) * 8 // self.w) % 8][None, :, :]
            img[self.h // 3:self.h // 3 + 8, :, :3] = 128  # a grey band, so a stretched picture shows
            self.put(img)
            time.sleep(1 / self.fps)

    def stop(self):
        self.running = False


def resolve_cameras(specs, infos):
    """Match --cameras entries (numbers or model names) to libcamera's camera list, in the order given."""
    if not specs:
        return infos[:2]
    chosen = []
    for spec in specs:
        found = [i for i in infos if (spec.isdigit() and i["Num"] == int(spec)) or
                 (not spec.isdigit() and spec.lower() in i["Model"].lower())]
        found = [i for i in found if i not in chosen]
        chosen.append(found[0] if found else {"Num": None, "Model": spec})
    return chosen


def flags(*values):
    """OR Qt flags of different types: PyQt5's are ints, PyQt6's are enums with .value."""
    out = 0
    for v in values:
        out |= int(getattr(v, "value", v))
    return out


def parse_controls(pairs):
    out = {}
    for pair in pairs:
        name, value = pair.split("=", 1)
        try:
            out[name] = int(value)
        except ValueError:
            out[name] = float(value)
    return out


# ---------------------------------------------------------------- the window
def main(argv=None):
    args = parse_args(argv)
    if not os.environ.get("QT_QPA_PLATFORM", "").startswith(("offscreen", "eglfs", "linuxfb", "vnc")):
        find_display(args.wait_display_s)
    QtCore, QtGui, QtWidgets = load_qt()
    pick_platform(QtCore)
    app = QtWidgets.QApplication(sys.argv[:1])
    Qt = QtCore.Qt

    if args.size:
        sw, sh = (int(v) for v in args.size.lower().split("x"))
    else:
        geo = app.primaryScreen().geometry()
        sw, sh = geo.width(), geo.height()
    lw, lh = (sh, sw) if args.rotate in (90, 270) else (sw, sh)  # the canvas before rotating onto the screen

    sources, labels = [], args.labels or []
    if args.fake:
        boxes = tiles(lw, lh, args.fake)
        for n in range(args.fake):
            sources.append(FakeSource(n, boxes[n][2:], args.fps, labels[n] if n < len(labels) else None))
    else:
        from picamera2 import Picamera2
        infos = Picamera2.global_camera_info()
        print("cameras found: " + (", ".join(f"{i['Num']} {i['Model']}" for i in infos) or "none"), flush=True)
        wanted = resolve_cameras(args.cameras, infos) or [{"Num": None, "Model": "camera"}]
        boxes = tiles(lw, lh, len(wanted))
        controls = parse_controls(args.control)
        for n, info in enumerate(wanted):
            label = labels[n] if n < len(labels) else None
            if info["Num"] is None:
                src = Source(label or info["Model"])
                src.error = f"no camera '{info['Model']}' found" if args.cameras else "no camera found"
                src.retry = False
            else:
                rot = any(r == str(info["Num"]) or r.lower() in info["Model"].lower() for r in args.rot180)
                try:
                    src = CameraSource(info, boxes[n][2:], args.fps, rot, controls, label)
                except Exception as e:  # show it on the panel, keep the other camera going
                    src = Source(label or info["Model"])
                    src.error = f"camera {info['Num']} failed: {e}"
            if src.error:
                print(src.error, flush=True)
            sources.append(src)

    class View(QtWidgets.QWidget):
        def paintEvent(self, event):
            p = QtGui.QPainter(self)
            p.fillRect(self.rect(), Qt.GlobalColor.black)
            p.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            cw, ch = (self.height(), self.width()) if args.rotate in (90, 270) else (self.width(), self.height())
            if args.rotate:  # turn the canvas (lw x lh) clockwise onto the widget
                p.translate(*{90: (self.width(), 0), 180: (self.width(), self.height()),
                              270: (0, self.height())}[args.rotate])
                p.rotate(args.rotate)
            font = p.font()
            font.setPixelSize(max(12, min(cw, ch) // 24))
            p.setFont(font)
            now = time.monotonic()
            for src, (x, y, w, h) in zip(sources, tiles(cw, ch, len(sources))):
                frame, msg = src.frame, src.error
                if frame is not None:
                    fh, fw = frame.shape[:2]
                    img = QtGui.QImage(frame.data, fw, fh, frame.strides[0], QtGui.QImage.Format.Format_RGB32)
                    dw, dh = fit(fw / fh, w, h)
                    p.drawImage(QtCore.QRectF(x + (w - dw) / 2, y + (h - dh) / 2, dw, dh), img)
                if not msg and (src.t_last is None or now - src.t_last > STALE_S):
                    msg = "waiting for the camera" if src.t_last is None else \
                        f"no frames for {now - src.t_last:.0f} s"
                if not args.no_labels:
                    self.caption(p, x + 6, y + 6, src.label)
                if msg:
                    p.setPen(QtGui.QColor(255, 80, 80))
                    p.drawText(QtCore.QRectF(x, y, w, h), flags(Qt.AlignmentFlag.AlignCenter, Qt.TextFlag.TextWordWrap),
                               msg)
            p.end()

        def caption(self, p, x, y, text):
            r = p.fontMetrics().boundingRect(text)
            p.fillRect(QtCore.QRectF(x, y, r.width() + 10, r.height() + 6), QtGui.QColor(0, 0, 0, 160))
            p.setPen(QtGui.QColor(255, 255, 255))
            p.drawText(QtCore.QRectF(x + 5, y + 3, r.width() + 2, r.height()), flags(Qt.AlignmentFlag.AlignLeft), text)

    view = View()
    view.setWindowTitle("rePowder viewport")
    view.setCursor(Qt.CursorShape.BlankCursor)
    seen = [None] * len(sources)

    def tick():  # repaint when any source has a new frame, and at least once a second for the "no frames" note
        now = time.monotonic()
        counts = [s.count for s in sources]
        if counts != seen or int(now) != tick.second:
            seen[:] = counts
            tick.second = int(now)
            view.update()
        for s in sources:  # a camera that failed or stalled: exit, and systemd starts the viewer again
            silent = now - (s.t_last or t_start)
            if s.retry and silent > RESTART_S:
                print(f"{s.label}: {s.error or 'no frames'} for {silent:.0f} s; exiting so that it restarts", flush=True)
                app.exit(1)
                return
    tick.second = 0
    t_start = time.monotonic()
    timer = QtCore.QTimer()
    timer.timeout.connect(tick)
    timer.start(max(5, int(1000 / args.fps)))

    stats = {"t": time.monotonic(), "counts": [0] * len(sources)}

    def log_rates():  # once a minute in the journal: frames per second each camera delivered
        t = time.monotonic()
        rates = [(s.count - c) / (t - stats["t"]) for s, c in zip(sources, stats["counts"])]
        print("fps: " + ", ".join(f"{s.label} {r:.1f}" for s, r in zip(sources, rates)), flush=True)
        stats["t"], stats["counts"] = t, [s.count for s in sources]
    stats_timer = QtCore.QTimer()
    stats_timer.timeout.connect(log_rates)
    stats_timer.start(60_000)

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: app.quit())
    if args.size:
        view.resize(sw, sh)
        view.show()
    else:
        view.setGeometry(app.primaryScreen().geometry())  # in case no window manager handles full screen
        view.showFullScreen()
    if args.screenshot:
        def shoot():
            view.grab().save(args.screenshot)
            app.quit()
        QtCore.QTimer.singleShot(int(args.run_s * 1000), shoot)
    code = app.exec() if hasattr(app, "exec") else app.exec_()
    for src in sources:
        try:
            src.stop()
        except Exception as e:  # a camera that has gone away; still close the others
            print(f"{src.label}: {e}", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
