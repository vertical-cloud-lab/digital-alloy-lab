"""
Process-representative draft blocks for the LPBF parameter-space figure.

The first isometric draft used generic colored cuboids.  This module replaces
those placeholders with reusable, individual block concepts that visually map
to the LPBF process domains they represent:

* Beam / Energy: laser head, beam cone, melt pool, scan direction
* Scan Strategy: hatch vectors, contour pass, rotation/skywriting
* Layer / Build: build plate, stacked layers, supports, orientation
* Powder / Feedstock: particle-size spread, powder bed, recycling/moisture
* Atmosphere: chamber, gas flow, O2 sensor, pressure gauge
* Thermal Mgmt: preheated plate, heat plume, dwell clock, build height
* Machine-Specific: recoater blade, dosing hopper, carriage motion

Run standalone:
    python figures/panels/panel_process_block_drafts.py
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import colors as mcolors
from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    FancyArrowPatch,
    FancyBboxPatch,
    PathPatch,
    Polygon,
    Rectangle,
)
from matplotlib.path import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import apply_rcparams, CAT_COLORS, CATEGORIES, TOTAL_PARAMS  # noqa: E402


OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "process_blocks")


@dataclass(frozen=True)
class BlockSpec:
    title: str
    key: str
    tagline: str
    params: tuple[str, ...]


BLOCKS: tuple[BlockSpec, ...] = (
    BlockSpec("Beam / Energy", "beam", "laser–melt-pool physics",
              ("P", "v", "spot", "profile", "pulse", "osc.")),
    BlockSpec("Scan Strategy", "scan", "toolpath geometry + timing",
              ("hatch", "pattern", "rotation", "vector", "contour")),
    BlockSpec("Layer / Build", "layer", "part orientation + layer stack",
              ("layer", "orient.", "support", "plate")),
    BlockSpec("Powder / Feedstock", "powder", "particle bed state",
              ("PSD", "shape", "flow", "pack", "H₂O", "reuse")),
    BlockSpec("Atmosphere", "atmosphere", "chamber chemistry + flow",
              ("gas", "flow", "O₂", "pressure")),
    BlockSpec("Thermal Mgmt", "thermal", "heat history + dwell",
              ("preheat", "dwell", "height")),
    BlockSpec("Machine-Specific", "machine", "hardware delivery limits",
              ("blade", "speed", "dose")),
)


def _mix(color: str, other: str = "#FFFFFF", weight: float = 0.5) -> str:
    """Blend two colors."""
    c1 = mcolors.to_rgb(color)
    c2 = mcolors.to_rgb(other)
    mixed = tuple((1 - weight) * a + weight * b for a, b in zip(c1, c2))
    return mcolors.to_hex(mixed)


def _text_outline(color: str = "white", lw: float = 2.0):
    return [pe.withStroke(linewidth=lw, foreground=color)]


def _block_base(ax, color: str, title: str, subtitle: str):
    """Draw a shallow pseudo-isometric base block."""
    front = _mix(color, "#FFFFFF", 0.78)
    top = _mix(color, "#FFFFFF", 0.62)
    side = _mix(color, "#000000", 0.18)
    edge = _mix(color, "#000000", 0.40)

    # Front, top, and right faces.
    ax.add_patch(Rectangle((0.13, 0.18), 0.68, 0.45,
                           facecolor=front, edgecolor=edge, linewidth=1.0))
    ax.add_patch(Polygon([(0.13, 0.63), (0.26, 0.76), (0.94, 0.76), (0.81, 0.63)],
                         closed=True, facecolor=top, edgecolor=edge, linewidth=1.0))
    ax.add_patch(Polygon([(0.81, 0.18), (0.94, 0.31), (0.94, 0.76), (0.81, 0.63)],
                         closed=True, facecolor=side, edgecolor=edge, linewidth=1.0))

    ax.text(0.04, 0.965, title, ha="left", va="top", fontsize=10.5,
            color="#172B4D", weight="semibold", transform=ax.transAxes)
    ax.text(0.04, 0.905, subtitle, ha="left", va="top", fontsize=7.4,
            color="#5A6B79", transform=ax.transAxes)


def _arrow(ax, start, end, color="#172B4D", lw=1.2, ms=9, **kwargs):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=ms,
                                 linewidth=lw, color=color, shrinkA=0, shrinkB=0,
                                 **kwargs))


def _param_chips(ax, labels: tuple[str, ...], color: str):
    """Small chips along the bottom edge, packed into one or two rows."""
    x0 = 0.15
    x = x0
    y = 0.045
    row_h = 0.052
    for label in labels:
        w = max(0.050, 0.012 * len(label) + 0.040)
        if x + w > 0.91:
            x = x0
            y += row_h
        ax.add_patch(FancyBboxPatch((x, y), w, 0.055,
                                    boxstyle="round,pad=0.004,rounding_size=0.012",
                                    facecolor=_mix(color, "#FFFFFF", 0.86),
                                    edgecolor=_mix(color, "#000000", 0.34),
                                    linewidth=0.55))
        ax.text(x + 0.012, y + 0.028, label, ha="left", va="center",
                fontsize=6.4, color="#1A1A1A")
        x += w + 0.012


def _beam_energy(ax, color):
    # Build plate and melt track.
    ax.add_patch(Polygon([(0.24, 0.35), (0.64, 0.35), (0.77, 0.48), (0.37, 0.48)],
                         closed=True, facecolor="#D8E1E8", edgecolor="#6A7E8D", linewidth=0.8))
    ax.add_patch(Ellipse((0.52, 0.43), 0.18, 0.055, angle=12,
                         facecolor="#F28E2B", edgecolor="#8C3F00", linewidth=0.8))
    ax.add_patch(Ellipse((0.53, 0.43), 0.08, 0.026, angle=12,
                         facecolor="#FFD166", edgecolor="none", alpha=0.95))

    # Laser head and beam cone.
    ax.add_patch(Rectangle((0.42, 0.68), 0.15, 0.065,
                           facecolor="#4A5568", edgecolor="#1A202C", linewidth=0.8))
    ax.add_patch(Rectangle((0.455, 0.61), 0.08, 0.07,
                           facecolor="#718096", edgecolor="#1A202C", linewidth=0.8))
    ax.add_patch(Polygon([(0.494, 0.61), (0.43, 0.45), (0.57, 0.45)],
                         closed=True, facecolor="#E85D04", edgecolor="#BA3B00",
                         linewidth=0.7, alpha=0.52))
    _arrow(ax, (0.36, 0.39), (0.70, 0.47), color="#C92A2A", lw=1.2, ms=8)
    ax.text(0.30, 0.36, "scan v", fontsize=7, color="#172B4D")
    ax.text(0.60, 0.58, "P / spot / pulse", fontsize=7, color="#172B4D")


def _scan_strategy(ax, color):
    # Hatch field.
    ax.add_patch(Polygon([(0.22, 0.31), (0.67, 0.31), (0.82, 0.46), (0.36, 0.46)],
                         closed=True, facecolor="#F3F6F8", edgecolor="#6A7E8D", linewidth=0.8))
    for i in range(6):
        y0 = 0.335 + i * 0.023
        if i % 2:
            _arrow(ax, (0.68, y0 + 0.105), (0.27, y0), color=color, lw=1.1, ms=7)
        else:
            _arrow(ax, (0.27, y0), (0.68, y0 + 0.105), color=color, lw=1.1, ms=7)
    # Contour pass and rotation arc.
    ax.add_patch(Polygon([(0.26, 0.33), (0.67, 0.33), (0.77, 0.43), (0.36, 0.43)],
                         closed=True, facecolor="none", edgecolor="#172B4D", linewidth=1.0))
    ax.add_patch(Arc((0.51, 0.61), 0.28, 0.18, angle=0, theta1=20, theta2=300,
                     edgecolor="#172B4D", linewidth=1.1))
    ax.add_patch(Circle((0.51, 0.61), 0.012, facecolor="#172B4D", edgecolor="none"))
    _arrow(ax, (0.60, 0.57), (0.63, 0.60), color="#172B4D", lw=1.0, ms=7)
    ax.text(0.28, 0.52, "hatch spacing", fontsize=7, color="#172B4D")
    ax.plot([0.34, 0.39], [0.49, 0.53], color="#172B4D", linewidth=0.7)
    ax.text(0.58, 0.67, "rotation", fontsize=7, color="#172B4D")


def _layer_build(ax, color):
    # Build plate, layers, and supports.
    ax.add_patch(Rectangle((0.22, 0.29), 0.50, 0.05,
                           facecolor="#7A869A", edgecolor="#344563", linewidth=0.8))
    for i in range(5):
        # Slightly tilted layer stack so the "orientation" parameter has a
        # visual referent, rather than a flat horizontal pile.
        tilt = 0.014 * i
        ax.add_patch(Polygon([(0.28 + tilt, 0.34 + i * 0.045),
                              (0.56 + tilt, 0.35 + i * 0.045),
                              (0.67 + tilt, 0.41 + i * 0.045),
                              (0.38 + tilt, 0.40 + i * 0.045)],
                             closed=True, facecolor=_mix(color, "#FFFFFF", 0.55 + i * 0.05),
                             edgecolor=_mix(color, "#000000", 0.35), linewidth=0.65))
    # Tree-support silhouettes: vertical stems with fan branches, avoiding
    # the X-zigzag that could be mistaken for hatch/infill.
    for x in (0.34, 0.47, 0.60):
        ax.plot([x, x], [0.31, 0.47], color="#5A6B79", linewidth=1.0)
        ax.plot([x, x - 0.045], [0.45, 0.50], color="#5A6B79", linewidth=1.0)
        ax.plot([x, x + 0.045], [0.45, 0.50], color="#5A6B79", linewidth=1.0)
        ax.add_patch(Circle((x, 0.45), 0.010, facecolor="#5A6B79", edgecolor="none"))
    _arrow(ax, (0.77, 0.30), (0.77, 0.66), color="#172B4D", lw=1.2, ms=8)
    ax.text(0.79, 0.49, "build height", fontsize=7, color="#172B4D",
            rotation=90, va="center")
    ax.text(0.25, 0.56, "tilted orientation", fontsize=7, color="#172B4D")


def _powder_feedstock(ax, color):
    # Powder bed + particles of varied size.
    ax.add_patch(Polygon([(0.20, 0.28), (0.69, 0.28), (0.84, 0.43), (0.34, 0.43)],
                         closed=True, facecolor="#DDE6EA", edgecolor="#455A64", linewidth=0.8))
    particles = [
        (0.30, 0.34, 0.018), (0.36, 0.36, 0.012), (0.42, 0.35, 0.024),
        (0.49, 0.38, 0.015), (0.55, 0.36, 0.020), (0.62, 0.39, 0.011),
        (0.66, 0.34, 0.018), (0.73, 0.40, 0.014),
    ]
    for x, y, r in particles:
        ax.add_patch(Circle((x, y), r, facecolor="#425A66", edgecolor="#1F2D33", linewidth=0.45))
    # PSD curve and recycling arrow.
    xs = [0.23, 0.29, 0.35, 0.42, 0.49, 0.56]
    ys = [0.58, 0.62, 0.70, 0.66, 0.60, 0.57]
    ax.plot(xs, ys, color="#172B4D", linewidth=1.2)
    ax.text(0.22, 0.72, "PSD", fontsize=7.2, color="#172B4D")
    ax.add_patch(Arc((0.69, 0.61), 0.18, 0.15, theta1=40, theta2=330,
                     color=color, linewidth=1.2))
    _arrow(ax, (0.76, 0.56), (0.79, 0.59), color=color, lw=1.0, ms=7)
    ax.text(0.62, 0.70, "reuse", fontsize=7, color="#172B4D")
    # Moisture is shown as a labeled particle in the powder bed, not as an
    # external droplet/spillage cue.
    ax.add_patch(Circle((0.61, 0.34), 0.030, facecolor="#D9F0FB",
                        edgecolor="#136F9B", linewidth=0.7))
    ax.text(0.61, 0.34, "H₂O", ha="center", va="center",
            fontsize=5.9, color="#084A6C")


def _atmosphere(ax, color):
    # Chamber and flow.
    ax.add_patch(FancyBboxPatch((0.22, 0.30), 0.55, 0.34,
                                boxstyle="round,pad=0.006,rounding_size=0.02",
                                facecolor="#F7F7FB", edgecolor="#5A4A78", linewidth=1.0))
    for y in (0.40, 0.48, 0.56):
        _arrow(ax, (0.25, y), (0.73, y), color=color, lw=1.2, ms=8, alpha=0.8)
    # Tiny build plate + part silhouette anchors the chamber as LPBF.
    ax.add_patch(Rectangle((0.43, 0.33), 0.18, 0.020,
                           facecolor="#7A869A", edgecolor="#344563", linewidth=0.55))
    ax.add_patch(Polygon([(0.48, 0.35), (0.56, 0.35), (0.59, 0.43), (0.46, 0.43)],
                         closed=True, facecolor="#E0E7EC", edgecolor="#344563",
                         linewidth=0.55))
    ax.add_patch(Circle((0.38, 0.51), 0.04, facecolor="#FFFFFF",
                        edgecolor="#344563", linewidth=0.8))
    ax.text(0.38, 0.51, "O₂", ha="center", va="center", fontsize=7.5, color="#172B4D")
    ax.add_patch(Circle((0.66, 0.36), 0.046, facecolor="#FFFFFF",
                        edgecolor="#344563", linewidth=0.8))
    ax.plot([0.66, 0.685], [0.36, 0.385], color="#344563", linewidth=0.8)
    ax.text(0.61, 0.29, "pressure", fontsize=7, color="#172B4D")
    ax.text(0.30, 0.66, "shielding gas flow", fontsize=7, color="#172B4D")


def _thermal_mgmt(ax, color):
    # Heat plate and plume.
    for i, c in enumerate(["#FEF0D9", "#FDD49E", "#FDBB84", "#FC8D59", "#D7301F"]):
        ax.add_patch(Rectangle((0.24 + i * 0.09, 0.29), 0.09, 0.06,
                               facecolor=c, edgecolor="none"))
    ax.add_patch(Rectangle((0.24, 0.29), 0.45, 0.06,
                           facecolor="none", edgecolor="#7A3B00", linewidth=0.8))
    for x, h in ((0.34, 0.30), (0.46, 0.38), (0.58, 0.26)):
        ax.add_patch(FancyArrowPatch((x, 0.37), (x, 0.37 + h),
                                     arrowstyle="simple", mutation_scale=15,
                                     color=color, alpha=0.24))
    # Clock/dwell and build height arrow.
    ax.add_patch(Circle((0.73, 0.57), 0.065, facecolor="#FFFFFF",
                        edgecolor="#344563", linewidth=0.9))
    ax.plot([0.73, 0.73], [0.57, 0.61], color="#344563", linewidth=0.8)
    ax.plot([0.73, 0.76], [0.57, 0.55], color="#344563", linewidth=0.8)
    ax.text(0.62, 0.67, "inter-layer dwell", fontsize=7, color="#172B4D")
    _arrow(ax, (0.20, 0.31), (0.20, 0.63), color="#172B4D", lw=1.0, ms=8)
    ax.text(0.22, 0.62, "heat history", fontsize=7, color="#172B4D")
    ax.text(0.33, 0.23, "preheated baseplate", fontsize=7, color="#172B4D")


def _machine_specific(ax, color):
    # Powder bed, recoater blade, hopper.
    ax.add_patch(Polygon([(0.22, 0.28), (0.70, 0.28), (0.83, 0.40), (0.35, 0.40)],
                         closed=True, facecolor="#E9EEF2", edgecolor="#5A6B79", linewidth=0.8))
    ax.add_patch(Polygon([(0.31, 0.49), (0.72, 0.49), (0.79, 0.55), (0.38, 0.55)],
                         closed=True, facecolor=color, edgecolor="#3C5A15", linewidth=0.9))
    ax.add_patch(Rectangle((0.35, 0.55), 0.34, 0.035,
                           facecolor=_mix(color, "#000000", 0.18),
                           edgecolor="#3C5A15", linewidth=0.8))
    motion_color = "#172B4D"
    _arrow(ax, (0.25, 0.61), (0.77, 0.61), color=motion_color, lw=1.2, ms=8)
    ax.text(0.40, 0.64, "recoater motion", fontsize=7, color="#172B4D")
    ax.add_patch(Polygon([(0.22, 0.70), (0.36, 0.70), (0.32, 0.58), (0.26, 0.58)],
                         closed=True, facecolor="#FFFFFF", edgecolor="#344563", linewidth=0.8))
    ax.add_patch(FancyArrowPatch((0.29, 0.58), (0.35, 0.44),
                                 arrowstyle="-|>", mutation_scale=8,
                                 linewidth=1.1, color=motion_color,
                                 linestyle=(0, (1.0, 1.5))))
    ax.text(0.18, 0.73, "dosing", fontsize=7, color="#172B4D")
    ax.text(0.55, 0.22, "→ motion · ⋯→ powder", fontsize=6.2,
            color="#172B4D", ha="center")


DRAWERS = {
    "beam": _beam_energy,
    "scan": _scan_strategy,
    "layer": _layer_build,
    "powder": _powder_feedstock,
    "atmosphere": _atmosphere,
    "thermal": _thermal_mgmt,
    "machine": _machine_specific,
}


def draw_process_block(ax, spec: BlockSpec, show_chips: bool = True):
    """Draw one process-representative block draft."""
    color = CAT_COLORS[spec.key]
    _block_base(ax, color, spec.title, spec.tagline)
    DRAWERS[spec.key](ax, color)
    if show_chips:
        _param_chips(ax, spec.params, color)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    return ax


def draw_process_block_grid(fig=None, ncols: int = 4):
    """Draw all process block drafts as small multiples."""
    apply_rcparams()
    if fig is None:
        fig = plt.figure(figsize=(11.2, 6.3), dpi=300, facecolor="white")

    nrows = math.ceil(len(BLOCKS) / ncols)
    for i, spec in enumerate(BLOCKS, start=1):
        ax = fig.add_subplot(nrows, ncols, i)
        draw_process_block(ax, spec)

    fig.suptitle(
        "Draft process blocks: each category now depicts its LPBF mechanism",
        fontsize=13, weight="semibold", color="#172B4D", y=0.985,
    )
    fig.text(
        0.99, 0.018,
        f"{TOTAL_PARAMS} controllable LPBF parameters · visual draft blocks for proposal figure",
        ha="right", va="bottom", fontsize=7.5, color="#5A6B79", style="italic",
    )
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.07,
                        wspace=0.18, hspace=0.22)
    return fig


def save_individual_blocks(out_dir: str = OUT_DIR) -> list[str]:
    """Save a standalone PNG for each block draft."""
    apply_rcparams()
    os.makedirs(out_dir, exist_ok=True)
    paths: list[str] = []
    for spec in BLOCKS:
        fig, ax = plt.subplots(figsize=(3.25, 3.25), dpi=300, facecolor="white")
        draw_process_block(ax, spec)
        path = os.path.join(out_dir, f"process_block_{spec.key}.png")
        fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        paths.append(path)
    return paths


def main(out_path: str | None = None):
    paths = save_individual_blocks()
    fig = draw_process_block_grid()
    if out_path is None:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "out",
            "panel_process_block_drafts.png",
        )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"wrote {out_path}")
    for path in paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
