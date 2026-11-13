#!/usr/bin/env python3
"""Render a stripped, wide-aspect LPBF parameter-space thumbnail for the
Fig.~1 DAG ``inp_p`` node.

Reuses the panel A/B/C draw functions from ``figures/panels/``, but lays
them out 1x3 horizontally with no figure title, no legends, no panel
labels, no callouts, no source attribution. In-panel commentary text
(e.g. the VED equation, ``+31 per material`` bracket, ``Illustrative
partition`` formula box, ``full single-material space`` annotation,
``Schematic coupling map`` footer) is stripped at draw time by
monkey-patching ``Axes.text`` and ``Axes.annotate``.

The standalone proposal figure ``figures/lpbf_parameter_space.png``
(referenced in Section "Approach") is left untouched.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "figures"))
sys.path.insert(0, str(REPO / "figures" / "panels"))

from panels.shared import apply_rcparams  # noqa: E402
from panels.panel_a_parameter_grid import draw_parameter_grid  # noqa: E402
from panels.panel_b_dimensionality import draw_dimensionality_scaling  # noqa: E402
from panels.panel_c_network import draw_interaction_network  # noqa: E402


COMMENTARY_FRAGMENTS = (
    "VED = P",
    "+31",
    "Illustrative partition",
    "full single-",
    "Schematic coupling map",
    "Same VED",
    "collapses 4D",
    "edge weight is qualitative",
)


def _has_commentary(text: str) -> bool:
    return any(frag in text for frag in COMMENTARY_FRAGMENTS)


def _patched_draw(draw_fn, ax):
    """Run a panel draw_fn with text/annotate filtered to drop commentary."""
    real_text = Axes.text
    real_annotate = Axes.annotate

    def filtered_text(self, x, y, s, *args, **kwargs):
        if isinstance(s, str) and _has_commentary(s):
            return real_text(self, 0, 0, "", alpha=0.0)
        return real_text(self, x, y, s, *args, **kwargs)

    def filtered_annotate(self, text, *args, **kwargs):
        if isinstance(text, str) and _has_commentary(text):
            kwargs.pop("arrowprops", None)
            return real_text(self, 0, 0, "", alpha=0.0)
        return real_annotate(self, text, *args, **kwargs)

    Axes.text = filtered_text
    Axes.annotate = filtered_annotate
    try:
        draw_fn(ax)
    finally:
        Axes.text = real_text
        Axes.annotate = real_annotate


def main():
    apply_rcparams()
    fig = plt.figure(figsize=(14.0, 3.5), dpi=200, facecolor="white")
    gs = GridSpec(
        1, 3, figure=fig,
        width_ratios=[2.4, 1.0, 1.0],
        left=0.01, right=0.99, top=0.97, bottom=0.05,
        wspace=0.10,
    )
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[0, 2])

    _patched_draw(draw_parameter_grid, ax_a)
    _patched_draw(draw_dimensionality_scaling, ax_b)
    _patched_draw(draw_interaction_network, ax_c)

    out = HERE / "lpbf_param_thumb.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white",
                pad_inches=0.05)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
