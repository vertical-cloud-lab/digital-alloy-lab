"""Render the FLAIME composition-design-space thumbnail for DAG node inp_c.

Single-row 1xN strip of element tiles colored by upper weight-fraction bound.
Boxes are sorted by upper bound HIGHEST (left) -> LOWEST (right); the colorbar
is visually flipped to match (dark/high color on the left). Tick marks land on
each unique upper-bound value used by the boxes, plus the 0 and 12 endpoints.

Source data: ./alloy_element_bounds.csv
Output PNG : ../periodic_table_bounds.png  (consumed by figures/flaime_pipeline_dag.py inp_c)
"""

from pathlib import Path
from typing import Dict

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon

HERE = Path(__file__).resolve().parent
BOUNDS_PATH = HERE / "alloy_element_bounds.csv"
OUT_PATH = HERE / "periodic_table_bounds.png"

bounds_df = pd.read_csv(BOUNDS_PATH)
UPPER_BOUNDS: Dict[str, float] = (
    bounds_df.set_index("Element")["Recommended upper bound (wt%)"].astype(float).to_dict()
)
LOWER_BOUNDS: Dict[str, float] = (
    bounds_df.set_index("Element")["Lower bound (wt%)"].astype(float).to_dict()
)

# 15-element palette in HIGH -> LOW order by recommended upper bound.
elements = [el for el in bounds_df["Element"].tolist() if el != "Al"]
elements_sorted = sorted(elements, key=lambda e: UPPER_BOUNDS[e], reverse=True)

# Truncated twilight cmap (matches prior aesthetic).
base_cmap = plt.get_cmap("twilight")
truncated_cmap = LinearSegmentedColormap.from_list(
    "twilight_trunc", base_cmap(np.linspace(0.0, 0.85, 256))
)
# Visual flip of the colorbar: reverse the cmap so dark/high appears on the left.
flipped_cmap = truncated_cmap.reversed()

EPS = 1e-6
norm = mcolors.Normalize(vmin=0.0, vmax=12.0)


def el_color(val: float):
    return truncated_cmap(norm(max(val, EPS)))


CELL = 1.0
GAP = 0.08

fig, ax = plt.subplots(figsize=(18, 10))
ax.set_aspect("equal")
ax.axis("off")

for i, el in enumerate(elements_sorted):
    x = i * (CELL + GAP)
    y = 1.0
    upper_color = el_color(UPPER_BOUNDS[el])

    ax.add_patch(
        plt.Rectangle(
            (x, y),
            CELL,
            CELL,
            facecolor=upper_color,
            edgecolor="white",
            linewidth=0.5,
        )
    )
    ax.text(
        x + CELL / 2,
        y + CELL / 2,
        el,
        ha="center",
        va="center",
        fontsize=15,
        color="white",
        fontweight="bold",
    )

ax.set_xlim(-0.2, len(elements_sorted) * (CELL + GAP))
ax.set_ylim(0, 2)

# Colorbar -------------------------------------------------------------------
unique_upper_vals = sorted({round(UPPER_BOUNDS[el], 4) for el in elements_sorted})
tick_values = sorted(set([0.0, 12.0] + unique_upper_vals))


def _fmt(v: float) -> str:
    if v == 0:
        return "0"
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v))}"
    return f"{v:g}"


pos = ax.get_position()
cbar_ax = fig.add_axes(
    [
        pos.x0 + 0.17 * pos.width,
        pos.y0 + 1.2 * pos.height,
        0.6 * pos.width,
        0.03,
    ]
)
cbar = fig.colorbar(
    ScalarMappable(norm=norm, cmap=flipped_cmap),
    cax=cbar_ax,
    orientation="horizontal",
    ticks=tick_values,
)
# Because the cmap is visually flipped but the data axis still runs 0->12 L->R,
# we need to flip the tick axis so the labels read 12 (left) -> 0 (right) and
# align with the high->low element ordering above.
cbar_ax.invert_xaxis()
cbar.set_ticklabels([_fmt(v) for v in tick_values])
cbar.ax.tick_params(which="both", length=3, labelsize=7)
for lbl in cbar.ax.get_xticklabels():
    lbl.set_rotation(0)
# Hide the redundant "0" label that visually overlaps the 0.1 tick — keep the
# tick mark itself per the user's request to retain a 0 endpoint anchor.
labels = [t.get_text() for t in cbar.ax.get_xticklabels()]
if "0" in labels and "0.1" in labels:
    new_labels = ["" if t == "0" else t for t in labels]
    cbar.ax.set_xticklabels(new_labels)
cbar.ax.set_title("Upper weight-fraction bound (%)", fontsize=11, pad=8)

fig.savefig(OUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved {OUT_PATH}")
