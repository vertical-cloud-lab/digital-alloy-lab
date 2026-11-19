#!/usr/bin/env python3
"""Render per-stage test-structure panels for use as Fig. 1 DAG node
thumbnails. Imports draw functions from
``edison-trajectories/fig_test_structures.py`` and saves each panel as a
standalone PNG sized for the DAG slot.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "edison-trajectories"))

import fig_test_structures as fts  # noqa: E402


def render_panel(draw_fn, out_path, dpi=160, figsize=(3.2, 2.2)):
    fig, ax = plt.subplots(figsize=figsize)
    draw_fn(ax, commentary=False)
    ax.axis("off")
    fig.tight_layout(pad=0.05)
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight",
                facecolor="white", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {out_path}")


def main():
    targets = [
        (fts.draw_single_tracks,      HERE / "single_tracks.png"),
        (fts.draw_thin_walls,         HERE / "thin_walls.png"),
        (fts.draw_density_cubes,      HERE / "density_cubes.png"),
        # NOTE: iso52902.png intentionally omitted — that node uses a
        # PI-curated photo of a real ISO/ASTM 52902 benchmark artefact
        # (committed in 5d4c3b8). Regenerating the matplotlib panel would
        # overwrite it. Use draw_geometric_artifact only when explicitly
        # requested as a fallback.
        (fts.draw_tensile_bars,       HERE / "tensile_bars.png"),
    ]
    for fn, out in targets:
        render_panel(fn, out)


def render_panel_no_commentary(draw_fn, out_path, dpi=160, figsize=(3.2, 2.2)):
    """Backwards-compatible alias; render_panel now defaults to commentary=False."""
    return render_panel(draw_fn, out_path, dpi=dpi, figsize=figsize)


if __name__ == "__main__":
    main()
