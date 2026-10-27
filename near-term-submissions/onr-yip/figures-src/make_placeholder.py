"""Placeholder for the copper powder figure (Preliminary results).

Sterling's request on PR 134 (Oct 24, 2026): "add this in as a placeholder image so that we can
anticipate the right amount of space. You can make this a 3D diagram that will replace with
something real". Nothing here is data: the particles and the size distribution are drawn from a
made-up log-normal so the figure has the size and layout of the real one (an SEM image of the
first copper lot and its laser-diffraction size distribution). Same 6.5 x 2.6 in footprint as the
CALPHAD figure.

    python make_placeholder.py   # writes cu_powder_placeholder.pdf and .png here
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(19)

plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.linewidth": 0.6})
fig = plt.figure(figsize=(6.5, 2.6))

# (a) 3D sketch of spherical particles on a stub, standing in for the SEM image.
ax = fig.add_axes([0.0, 0.02, 0.5, 0.96], projection="3d", computed_zorder=False)
gx, gy = np.meshgrid([-40, 440], [-40, 440])
ax.plot_surface(gx, gy, np.zeros_like(gx), color="0.85", linewidth=0)
d, xy = [], []
while len(d) < 60:  # non-overlapping monolayer of particles, diameters in um
    di = np.clip(rng.lognormal(np.log(70), 0.35), 30, 160)
    p = rng.uniform(0, 400, 2)
    if all(np.hypot(*(p - q)) > (di + dj) / 2 for q, dj in zip(xy, d)):
        d.append(di)
        xy.append(p)
cam = np.array([np.cos(np.radians(-60)), np.sin(np.radians(-60))])
u, v = np.mgrid[0 : 2 * np.pi : 24j, 0 : np.pi : 12j]
copper = np.array([0.80, 0.50, 0.30])
for (x, y), di in sorted(zip(xy, d), key=lambda t: t[0] @ cam):
    r = di / 2
    xs, ys, zs = x + r * np.cos(u) * np.sin(v), y + r * np.sin(u) * np.sin(v), r + r * np.cos(v)
    shade = 0.55 + 0.45 * np.clip(np.cos(v) * 0.7 + np.cos(u) * np.sin(v) * 0.3, 0, 1)
    ax.plot_surface(xs, ys, zs, facecolors=np.clip(shade[..., None] * copper, 0, 1),
                    linewidth=0, antialiased=True, shade=False)
ax.set(xlim=(-40, 440), ylim=(-40, 440), zlim=(0, 200))
ax.set_box_aspect((1, 1, 0.42))
ax.view_init(elev=32, azim=-60)
ax.set_axis_off()
ax.text2D(0.03, 0.93, "(a)", transform=ax.transAxes, fontsize=9)
ax.text2D(0.5, 0.06, "SEM image of the first copper lot", transform=ax.transAxes,
          ha="center", fontsize=7, color="0.35", style="italic")

# (b) size distribution, standing in for the laser-diffraction result.
bx = fig.add_axes([0.6, 0.18, 0.37, 0.72])
dd = rng.lognormal(np.log(70), 0.35, 4000)
bins = np.geomspace(10, 300, 40)
bx.hist(dd, bins=bins, density=True, color="0.7", edgecolor="white", linewidth=0.3)
bx.set_xscale("log")
bx.set_xlabel(r"Particle diameter ($\mu$m)")
bx.set_ylabel("Volume fraction (a.u.)")
bx.set_yticks([])
bx.axvspan(50, 200, color=copper, alpha=0.15, lw=0)
bx.text(100, bx.get_ylim()[1] * 0.92, "DED cut,\n50 to 200 $\\mu$m", ha="center", va="top",
        fontsize=7, color=copper * 0.7)
for q, ls in zip(np.percentile(dd, [10, 50, 90]), [":", "--", ":"]):
    bx.axvline(q, color="0.3", lw=0.7, ls=ls)
bx.text(-0.22, 1.02, "(b)", transform=bx.transAxes, fontsize=9)

fig.text(0.5, 0.5, "PLACEHOLDER", ha="center", va="center", rotation=12, fontsize=34,
         color="red", alpha=0.18, weight="bold")

for ext in ("pdf", "png"):
    fig.savefig(HERE.parent / "figures-cu-ded" / f"cu_powder_placeholder.{ext}", dpi=300)
