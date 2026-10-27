# Figure sources for the copper/DED technical proposal

Until Oct 27, 2026 these scripts lived only in `sgbaird/byu-finances` (private),
under `proposals/onr-yip-2027/` at `f00a392`. They are copied here so the figure
PRs stacked on `onr-yip-figs-oct27` can regenerate the figures in this repo.
Output paths now point at `../figures-cu-ded/`.

| File | Makes | Was in byu-finances |
|---|---|---|
| `make_fig1_tiles.py` | `../figures-cu-ded/fig1/*.jpg` (680 x 510 photo tiles) and the tensile and immersion icons | `project-description/figures/` |
| `make_search_space_figure.py` | `../figures-cu-ded/cu_search_space_periodic.{pdf,png}` (Fig. search space) | `project-description/figures/` |
| `make_placeholder.py` | `../figures-cu-ded/cu_powder_placeholder.{pdf,png}` (placeholder, not data) | `project-description/copper-powder-placeholder/` |
| `img/` | Source photographs for the tiles, the Facilities and Equipment attachments, and Fig. enclosure; provenance in `img/SOURCES.md` | `attachments/src/img/` and `project-description/figures/` |

`make_fig1_tiles.py` reads the CALPHAD panel from `../pycalphad-cu/cu_panel2.png`,
which `../pycalphad-cu/run_calphad.py` writes. The Utah, Mines and BYU
Electron Microscopy Facility photographs are those institutions' own and are
credited in the captions. No person appears in any of them.

Run with Python 3.12 and `matplotlib`, `numpy` and `pillow`. Times New Roman
must be installed (on Linux, `ttf-mscorefonts-installer`).
