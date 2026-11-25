# Source images for the aluminum LPBF network

The figure script crops and resizes these into `../tiles/`. No person appears
in any of them. Lab photographs are used wherever one exists. The sieve and the
density step have none yet, so their tiles are renders from the vertical-lab
animations, tagged "render" on the figure.

| File | Tile | Source |
|---|---|---|
| `scheil-al-cu-si.png` | CALPHAD | The lab's Scheil calculation for an Al-Cu-Si alloy (TC-Python), from earlier proposal work: `figures/dag-thumbnails/scheil-graph-for-Al-Cu-Si.png` on `consolidation-2`. It is not one of the Zn-Mg-Cu-Zr-Sc alloys of the route, and the credit line on the figure says so |
| `lab-powder-doser.jpg` | Charge (left) | BYU VCL YouTube `prj_xgeuQtM` ("Atomizer charge prep (Sep 29): dosing AlSi10Mg", public), frame at 34:27, as committed for the copper figure on PR #215 (`near-term-submissions/onr-yip/figures-src/img/`) |
| `cup_plug.png` | Charge (right) | The lab's shop drawing of the atomizer charge cup and plug, `atomizer-charge/drawing/cup_plug.png` on PR #179, as committed on PR #215. The tile uses its "assembled and filled" section, standing plug-up |
| `lab-atomizer-melting.jpg` | Atomize | Aluminum rods melting in the lab's rePOWDER, from the in-house atomizer photo strip (`figures/al-melting-rods.png` in the private repo), as committed on PR #215 |
| `render-sieve.png` | Sieve (render) | byu-vcl PR 318, `vertical-lab/out/instruments/sieve.png` (commit `4ca0312`): the vertical lab's sieve shaker |
| `lab-aconity-plate-bars.jpg` | Print | The lab's tensile bars as built on the plate of the University of Utah's Aconity MIDI, a lab photograph of 2026-04-27 (byu-vcl issue 77): `figures/dag-thumbnails/tensile-bars-photo.jpg` on `consolidation-2`, re-saved without metadata |
| `render-vhx.png` | Density (render) | byu-vcl PR 318, `vertical-lab/out/instruments/vhx.png` (commit `3626a12`): the Keyence VHX digital microscope that images polished sections for pores and cracks |
| `lab-pulled-bars.jpg` | Tensile | The lab's pulled LPBF AlSi10Mg bars (the in-house tensile test), `figures/dag-thumbnails/in-house-tensile-data/585796705-….jpg` on `consolidation-2`, downsized from 4284 × 5712 to 1500 × 2000 px. The tile is turned 90° and cropped below a strip of labelling tape |
| `lab-cubxl-gantry.jpg` | Corrosion | BYU VCL YouTube `lmQbUWNqTmM` ("Pipette test on CubXL", public), 1080p frame at 3:00, as committed on PR #215 |

byu-vcl PR 318's branch was `claude/issue-303-20261103-1736` at `e3667f8` when
the renders were copied (2026-11-25).
