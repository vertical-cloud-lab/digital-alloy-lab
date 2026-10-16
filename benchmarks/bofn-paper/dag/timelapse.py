"""Timelapse of each policy's purchases on the benchmark network, with its best-vs-spend trace.

    python timelapse.py                          # bofn_dag_timelapse.mp4, .gif and _final.png (seed 0, kappa 1)
    python timelapse.py --seed 3 --policies tiered pkgfn --out /tmp/two

Every purchase in a run's log is a button press on the network: the stage it buys
(its header, its node(s), the edges into them and the input the policy chose)
strikes red and fades back, like a fluorescent tube settling after it switches
on; a new press re-strikes it. The objective box strikes when a tensile test beats
the best alloy so far. Underneath, the same run's best demonstrated alloy is
traced against spend on the y range of the finished plot, one policy after
another, tiered screening first; finished traces stay, in the slide figures'
styles. Video time is proportional to spend, so every run takes as long and a
$10 CALPHAD call is a blink next to a $2,500 print.

Only runs made after the port carry a purchase log (PORT.md, step 1):
../results-rerun (seeds 0-4, identical to the stored runs action for action) and
../quality/kgfn-smoke (KGFN, seeds 0-1). Every policy runs the same seed, so all
start from the same seed alloys. Needs matplotlib, numpy, Pillow, torch (the
true optimum, via analyze.py) and ffmpeg (imageio-ffmpeg's binary will do).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import multiprocessing
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import matplotlib.pyplot as plt  # noqa: E402

import network_dag as nd  # noqa: E402  (Aptos, the palette and the geometry of the static figures)
from analyze import optimum  # noqa: E402
from plot import FADE, SHORT, STYLE  # noqa: E402

ORDER = ["tiered", "tiered_naive", "random", "ei", "eifn", "kgfn", "eifn_reuse", "pkgfn"]
WHAT = {
    "tiered": "Screens 256 compositions with CALPHAD, then tunes the process for the best four, reusing their powders",
    "tiered_naive": "The same screen, but every print gets a freshly atomized powder",
    "random": "Uniform random designs, all four stages for each",
    "ei": "One GP from the seven inputs to the objective, all four stages for each design",
    "eifn": "The network model picks a design by expected improvement, then runs all four stages",
    "kgfn": "The network model picks a design by knowledge gradient per dollar, then runs all four stages",
    "eifn_reuse": "Network expected improvement per dollar, over new designs and reprints of existing powders",
    "pkgfn": "Knowledge gradient per dollar for every stage; buys whichever single stage is worth most",
}
SOURCES = [HERE.parent / "results-rerun", HERE.parent / "quality" / "kgfn-smoke"]
CHOSEN = {"comp": "C", "a": "A", "pv": "L"}  # the input each stage's action chooses

FPS, LEAD_S, RUN_S, HOLD_S, OUTRO_S = 20, 0.4, 7.0, 1.2, 3.0
STRIKE, TAU_STRIKE, TAU_GLOW = 0.7, 0.12, 0.7  # a press: a bright strike that drops fast to a glow that fades slowly
HALO = [(0.04, 0.16), (0.09, 0.10), (0.15, 0.06), (0.22, 0.035)]  # (pad in inches, alpha at full brightness)
LIT_FILL = "#FFE1E1"
TOP_H, TRACE_H = 0.9, 3.9
FIG_H = TOP_H + nd.H + TRACE_H
AX_L, AX_R, AX_B, AX_T = 1.0, 3.0, 0.72, 0.5  # trace axes margins, inches
LABEL_PT = 13


def load_run(kind, seed, kappa):
    for root in SOURCES:
        p = root / f"k{kappa:g}" / f"{kind}_s{seed}.json"
        if p.exists():
            r = json.loads(p.read_text())
            if r.get("purchases"):
                return r
    raise FileNotFoundError(f"no run with a purchase log for {kind}, seed {seed}, kappa {kappa:g}")


def lamp_level(times, t):
    """Brightness at video time t of a lamp pressed at the sorted `times`; each press re-strikes it."""
    k = int(np.searchsorted(times, t, side="right"))
    if k == 0:
        return 0.0
    dt = t - times[k - 1]
    return STRIKE * np.exp(-dt / TAU_STRIKE) + (1 - STRIKE) * np.exp(-dt / TAU_GLOW)


def mix(c0, c1, w):
    return tuple((1 - w) * np.array(to_rgb(c0)) + w * np.array(to_rgb(c1)))


class Run:
    """One run's purchases as presses (video seconds) and its running best as % of the true optimum."""

    def __init__(self, kind, run, ystar):
        self.kind, self.budget = kind, float(run["budget"])
        costs = run["settings"]["costs"]
        stages = [p[0] for p in run["purchases"]]
        ends = np.array([p[1] for p in run["purchases"]])
        starts = ends - np.array([costs[g] for g in stages])
        self.starts, self.ends = starts, ends
        self.press = {g: np.array([s for s, h in zip(starts, stages) if h == g]) / self.budget * RUN_S for g in "CALT"}
        self.x = np.array([r["spent"] for r in run["rows"]])
        self.y = np.maximum.accumulate([r["best_validated"] for r in run["rows"]]) / ystar * 100
        better = np.flatnonzero(np.diff(self.y) > 0) + 1
        self.press["OBJ"] = self.x[better] / self.budget * RUN_S

    def committed(self, s):
        """Money committed once the cursor reaches spend s: every purchase started by then, paid in full."""
        k = int(np.searchsorted(self.starts, s, side="right"))
        return float(self.ends[k - 1]) if k else 0.0

    def trace(self, s):
        k = int(np.searchsorted(self.x, s, side="right"))
        return np.r_[self.x[:k], s] / 1e3, np.r_[self.y[:k], self.y[k - 1]]


class Lamp:
    """Everything one stage lights up: boxes with their halos, edges with their glow, texts."""

    def __init__(self):
        self.boxes, self.edges, self.texts = [], [], []

    def set(self, w):
        on = w > 0.01
        for p, (fill0, line0, lw0), halos in self.boxes:
            if fill0:
                p.set_facecolor(mix(fill0, LIT_FILL, w))
            p.set_edgecolor(mix(line0, nd.RED, w))
            p.set_linewidth(lw0 + 1.3 * w)
            for h, a in halos:
                h.set_alpha(a * w)
                h.set_visible(on)
        for e, glows, (col0, lw0) in self.edges:
            e.set_color(mix(col0, nd.RED, w))
            e.set_linewidth(lw0 + 1.0 * w)
            e.set_zorder(2.5 if on else 2)
            for g, a in glows:
                g.set_alpha(a * w)
                g.set_visible(on)
        for t, col0 in self.texts:
            t.set_color(mix(col0, nd.RED, w))


def halos(ax, rect, radius, scale=1.0):
    x, y, w, h = rect
    out = []
    for pad, a in HALO:
        p = FancyBboxPatch((x - pad, y - pad), w + 2 * pad, h + 2 * pad, boxstyle=f"round,pad=0,rounding_size={radius + pad}",
                           fc=nd.RED, ec="none", lw=0, alpha=0, zorder=1.5, visible=False)
        ax.add_patch(p)
        out.append((p, a * scale))
    return out


def edge_with_glow(ax, p0, p1, curved):
    draw = nd.bezier if curved else nd.straight
    glows = [(draw(ax, p0, p1, color=nd.RED, lw=lw, head=False, z=1.6), a) for lw, a in ((9, 0.10), (5, 0.16))]
    for g, _ in glows:
        g.set_alpha(0)
        g.set_visible(False)
    return draw(ax, p0, p1, color=nd.EDGE, lw=1.5), glows


def centred_texts(ax, x, y, runs, size, z=5):
    """nd.centred_runs, returning the text artists."""
    r = ax.figure.canvas.get_renderer()
    texts, cursor = [], x
    for text, color, bold in runs:
        t = ax.text(cursor, y, text, ha="left", va="center", fontsize=size, color=color,
                    fontweight="bold" if bold else "normal", zorder=z)
        cursor = t.get_window_extent(r).transformed(ax.transData.inverted()).x1
        texts.append(t)
    for t in texts:
        px, py = t.get_position()
        t.set_position((px - (cursor - x) / 2, py))
    return texts


def build_network(ax):
    """The network of nd.draw_network with handles on everything a stage lights, and a purchase counter
    under each stage header (in place of the burden note; the dashed bypass stays)."""
    anchors = nd.side_anchors()
    lamps = {g: Lamp() for g in ("C", "A", "L", "T", "OBJ")}
    counts = {}
    for c in nd.COLS:
        runs = [(nd.HEADERS[c], nd.INK, False)]
        if c in nd.COSTS:
            runs.append(("  " + nd.fmt_cost(nd.COSTS[c]), nd.INK, True))
        texts = centred_texts(ax, nd.COL_X[c] + nd.BOX_W / 2, nd.HEADER_Y, runs, 20)
        if c in nd.COSTS:
            counts[c] = ax.text(nd.COL_X[c] + nd.BOX_W / 2, nd.HEADER_Y + 0.36, "", ha="center", va="center", fontsize=15,
                                color=nd.GRAY, zorder=5)
            lamps[c].texts += [(t, nd.INK) for t in texts] + [(counts[c], nd.GRAY)]

    cx, cy0, _, _ = nd.rect_of("s")
    _, cy1, _, ch = nd.rect_of("g")
    pad = 0.11
    grp = (cx - pad, cy0 - pad, nd.BOX_W + 2 * pad, cy1 + ch - cy0 + 2 * pad + 0.26)
    lamps["C"].boxes.append((nd.box(ax, grp, fill=None, line=nd.LIGHT, lw=1.1, dashed=True, radius=0.16, z=1), (None, nd.LIGHT, 1.1), []))
    t = ax.text(grp[0] + grp[2] - 0.12, grp[1] + grp[3] - 0.07, "one call", ha="right", va="bottom", fontsize=13, color=nd.GRAY, zorder=4)
    lamps["C"].texts.append((t, nd.GRAY))

    for key, (label, _col, _yc) in nd.NODES.items():
        rect = nd.rect_of(key)
        hs = halos(ax, rect, 0.1)
        p = nd.box(ax, rect)
        ax.text(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2, label, ha="center", va="center",
                fontsize=17 - (1 if label.count("\n") == 2 else 0), color=nd.INK, linespacing=1.0, zorder=5)
        lamps[nd.GROUP_OF[key]].boxes.append((p, (nd.NODE_FILL, nd.NODE_LINE, 1.3), hs))

    rect = nd.rect_of("OBJ")
    hs = halos(ax, rect, 0.1)
    p = nd.box(ax, rect, fill=nd.WHITE, line=nd.INK, lw=1.5)
    ax.text(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2, nd.OBJ[0], ha="center", va="center", fontsize=16, color=nd.INK,
            linespacing=1.05, zorder=5)
    lamps["OBJ"].boxes.append((p, (nd.WHITE, nd.INK, 1.5), hs))

    for key, (label, _col, _yc, _side) in nd.INPUTS.items():
        rect = nd.rect_of(key)
        hs = halos(ax, rect, 0.08, scale=0.6)
        p = nd.box(ax, rect, fill=nd.WHITE, line=nd.LIGHT, lw=1.1, radius=0.08)
        ax.text(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2, label, ha="center", va="center", fontsize=15, color="#404040",
                linespacing=1.0, zorder=5)
        lamps[CHOSEN[key]].boxes.append((p, (nd.WHITE, nd.LIGHT, 1.1), hs))

    for s, d in nd.EDGES:
        e, glows = edge_with_glow(ax, anchors[(s, d, "out")], anchors[(s, d, "in")], curved=True)
        lamps["OBJ" if d == "OBJ" else nd.GROUP_OF[d]].edges.append((e, glows, (nd.EDGE, 1.5)))
    for s, d in nd.INPUT_EDGES:
        if nd.INPUTS[s][3] == "right":
            e, glows = edge_with_glow(ax, anchors[(s, d, "out")], anchors[(s, d, "in")], curved=True)
        else:  # vertical, from the input box up into the node
            x, y, w, h = nd.rect_of(s)
            nx, ny, nw, nh = nd.rect_of(d)
            e, glows = edge_with_glow(ax, (x + w / 2, y), (nx + nw / 2, ny + nh), curved=False)
        lamps[nd.GROUP_OF[d]].edges.append((e, glows, (nd.EDGE, 1.5)))

    x, y, w, h = nd.rect_of("comp")
    ox, oy, ow, oh = nd.rect_of("OBJ")
    pts = [(x + w * 0.5, y), (x + w * 0.5, nd.BYPASS_Y), (ox + ow * 0.5, nd.BYPASS_Y), (ox + ow * 0.5, oy)]
    for a, b in zip(pts[:-1], pts[1:]):
        nd.straight(ax, a, b, color=nd.GRAY, lw=1.2, head=(b == pts[-1]), dashed=True, z=1, head_scale=11)
    return lamps, counts


class Movie:
    def __init__(self, kinds, seed, kappa, dpi):
        ystar = optimum(kappa)
        self.runs = [Run(k, load_run(k, seed, kappa), ystar) for k in kinds]
        self.seed, self.kappa = seed, kappa
        self.budget = max(r.budget for r in self.runs)
        per = int(round((LEAD_S + RUN_S + HOLD_S) * FPS))
        self.frames = [(i, -LEAD_S + j / FPS) for i in range(len(self.runs)) for j in range(per)]
        self.frames += [(len(self.runs), 0.0)] * int(round(OUTRO_S * FPS))

        self.fig = plt.figure(figsize=(nd.W, FIG_H), dpi=dpi)
        top = self.fig.add_axes([0, 1 - TOP_H / FIG_H, 1, TOP_H / FIG_H])
        top.set_xlim(0, nd.W)
        top.set_ylim(TOP_H, 0)
        top.axis("off")
        self.name = top.text(nd.MARGIN, 0.36, "", ha="left", va="center", fontsize=24, fontweight="bold", color=nd.INK)
        self.what = top.text(nd.MARGIN, 0.74, "", ha="left", va="center", fontsize=14, color=nd.GRAY)
        self.spend = top.text(nd.W - nd.MARGIN, 0.36, "", ha="right", va="center", fontsize=22, color=nd.INK)
        self.spend_of = top.text(nd.W - nd.MARGIN, 0.74, "", ha="right", va="center", fontsize=14, color=nd.GRAY)

        dag = self.fig.add_axes([0, TRACE_H / FIG_H, 1, nd.H / FIG_H])
        dag.set_xlim(0, nd.W)
        dag.set_ylim(nd.H, 0)
        dag.axis("off")
        self.lamps, self.counts = build_network(dag)
        self._trace_axes()

    def _trace_axes(self):
        fig = self.fig
        h_in = TRACE_H - AX_B - AX_T
        ax = fig.add_axes([AX_L / nd.W, AX_B / FIG_H, (nd.W - AX_L - AX_R) / nd.W, h_in / FIG_H])
        self.ax = ax
        ys = np.concatenate([r.y for r in self.runs])
        lo, hi = 5 * np.floor((ys.min() - 4) / 5), 5 * np.ceil((ys.max() + 2) / 5)  # the finished plot's range, fixed throughout
        ax.set_xlim(0, self.budget / 1e3)
        ax.set_ylim(lo, hi)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#8C8C8C")
            ax.spines[side].set_linewidth(0.8)
        ax.tick_params(length=0, labelsize=14, labelcolor="#595959", pad=6)
        ax.yaxis.grid(True, color="#E6E6E6", lw=0.8)
        ax.set_axisbelow(True)
        ax.set_xlabel("New spend on experiments and simulations ($k)", fontsize=15, color="#404040", labelpad=6)
        ax.text(0, 1.04, "Best alloy demonstrated (% of true optimum)", transform=ax.transAxes, ha="left", va="bottom",
                fontsize=15, color="#404040")
        self.cursor = ax.axvline(0, color="#BFBFBF", lw=1.0, ls=(0, (2, 3)), zorder=0.5)
        self.lines = []
        for r in self.runs:
            st = STYLE[r.kind]
            (ln,) = ax.plot([], [], color=st["color"], lw=st["lw"], ls=st["ls"], zorder=st["z"] + 0.5, drawstyle="steps-post",
                            solid_capstyle="round")
            self.lines.append(ln)
        (self.head,) = ax.plot([], [], "o", color=nd.RED, ms=8, mec="white", mew=1.5, zorder=20)
        # labels at the right end, stacked on the finished plot's positions so they never move
        finals = {i: r.y[-1] for i, r in enumerate(self.runs)}
        gap = LABEL_PT * 1.3 / (h_in * 72) * (hi - lo)
        order = sorted(finals, key=finals.get)
        ypos, last = {}, -1e9
        for i in order:
            ypos[i] = max(finals[i], last + gap)
            last = ypos[i]
        shift = np.mean([ypos[i] - finals[i] for i in order])
        xr, xl = self.budget / 1e3, self.budget / 1e3 * 1.032
        self.labels = []
        for i, r in enumerate(self.runs):
            yl = ypos[i] - shift
            lead = ax.plot([xr * 1.003, xl - xr * 0.009], [finals[i], yl], color=FADE.get(STYLE[r.kind]["color"], "#CCCCCC"),
                           lw=1.6, clip_on=False, zorder=1, solid_capstyle="round")[0]
            t = ax.text(xl, yl, SHORT[r.kind], ha="left", va="center", fontsize=LABEL_PT, clip_on=False)
            self.labels.append((lead, t))

    def frame(self, f):
        i, t = self.frames[f]
        n = len(self.runs)
        outro = i == n
        s = 0.0 if outro else min(max(t, 0.0) / RUN_S, 1.0) * self.budget
        for j, (r, ln) in enumerate(zip(self.runs, self.lines)):
            st = STYLE[r.kind]
            done = j < i
            ln.set_visible(j <= i)
            if j == i:  # the run being played
                ln.set_data(*r.trace(s))
                ln.set(color=nd.RED, lw=3.2, ls="-", zorder=10)
                self.head.set_data([s / 1e3], [r.trace(s)[1][-1]])
            elif done:
                ln.set_data(*r.trace(self.budget))
                ln.set(color=st["color"], lw=st["lw"], ls=st["ls"], zorder=st["z"] + 0.5)
            lead, lab = self.labels[j]
            shown = done or (j == i and t >= RUN_S)
            lead.set_visible(shown)
            lab.set_visible(shown)
            red = st["color"] == nd.RED or st["color"] == "#C00000"
            lab.set_color(nd.RED if j == i else (nd.INK if red else "#404040"))
            lab.set_fontweight("bold" if (red and done) else "normal")
        self.head.set_visible(not outro)
        self.cursor.set_visible(not outro)
        self.cursor.set_xdata([s / 1e3, s / 1e3])
        if outro:
            for lamp in self.lamps.values():
                lamp.set(0.0)
            for c in self.counts.values():
                c.set_text("")
            self.name.set_text(f"Seed {self.seed}, κ = {self.kappa:g}: one run per policy")
            self.what.set_text("Every policy starts from the same seed alloys. The slide figures average 20 seeds.")
            self.spend.set_text("")
            self.spend_of.set_text("")
        else:
            r = self.runs[i]
            for g, lamp in self.lamps.items():
                lamp.set(lamp_level(r.press[g], t))
            for g, c in self.counts.items():
                k = int(np.searchsorted(r.press[g], t, side="right"))
                c.set_text(f"×{k}" if k else "")
            self.name.set_text(SHORT[r.kind])
            self.what.set_text(WHAT[r.kind])
            self.spend.set_text(f"${r.committed(s):,.0f}")
            self.spend_of.set_text(f"spent of ${self.budget:,.0f}")
        self.fig.canvas.draw()
        return np.asarray(self.fig.canvas.buffer_rgba())[..., :3].copy()


_MOVIE = None


def _init(args):
    global _MOVIE
    _MOVIE = Movie(*args)


def _render(job):
    from PIL import Image

    f, path = job
    Image.fromarray(_MOVIE.frame(f)).save(path, compress_level=1)
    return f


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def encode(frames, stem, gif_width, gif_fps, colors):
    """MP4 at full size and frame rate; a GIF with flat colours (dithering would defeat its compression)."""
    ff, pattern = ffmpeg(), str(frames / "%05d.png")
    common = [ff, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", pattern]
    subprocess.run(common + ["-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{stem}.mp4"], check=True)
    scale = f"fps={gif_fps},scale={gif_width}:-1:flags=lanczos"
    palette = frames / "palette.png"
    subprocess.run(common + ["-vf", f"{scale},palettegen=max_colors={colors}:stats_mode=full", str(palette)], check=True)
    subprocess.run(common + ["-i", str(palette), "-lavfi", f"[0:v]{scale}[v];[v][1:v]paletteuse=dither=none:diff_mode=rectangle",
                             "-loop", "0", f"{stem}.gif"], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--policies", nargs="+", default=ORDER)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--kappa", type=float, default=1.0)
    ap.add_argument("--dpi", type=int, default=120)
    ap.add_argument("--gif-width", type=int, default=800)
    ap.add_argument("--gif-fps", type=int, default=6)
    ap.add_argument("--gif-colors", type=int, default=64)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--out", type=Path, default=HERE / "bofn_dag_timelapse")
    ap.add_argument("--frames-dir", type=Path, help="keep the PNG frames here (default: a temporary directory)")
    a = ap.parse_args()
    cfg = (a.policies, a.seed, a.kappa, a.dpi)
    n = len(Movie(*cfg).frames)
    with tempfile.TemporaryDirectory() as tmp:
        frames = a.frames_dir or Path(tmp)
        frames.mkdir(parents=True, exist_ok=True)
        jobs = [(f, frames / f"{f:05d}.png") for f in range(n)]
        # spawn, not fork: the parent has already started torch's thread pool (the true optimum)
        with multiprocessing.get_context("spawn").Pool(a.workers, initializer=_init, initargs=(cfg,)) as pool:
            for k, _ in enumerate(pool.imap_unordered(_render, jobs, chunksize=8), 1):
                if k % 200 == 0 or k == n:
                    print(f"  {k}/{n} frames", flush=True)
        shutil.copy(jobs[-1][1], f"{a.out}_final.png")
        encode(frames, a.out, a.gif_width, a.gif_fps, a.gif_colors)
    for ext in (".mp4", ".gif", "_final.png"):
        p = Path(f"{a.out}{ext}")
        print(f"{p.name}: {p.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
