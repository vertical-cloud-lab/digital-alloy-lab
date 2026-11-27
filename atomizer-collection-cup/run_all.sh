#!/usr/bin/env bash
# Re-run everything in this folder, in dependency order. Needs: Python 3.12 with cadquery, gmsh, pyvista, numpy,
# scipy, shapely, matplotlib, imageio(+ffmpeg), trimesh, manifold3d; CalculiX ccx 2.21; xvfb-run; Docker with
# the camotics:1.2.0 image (desktop-lpbf/analysis/machining/camotics.Dockerfile on PR #266) for the mill check.
# Times are on a 4-core runner.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python}

$PY params.py                                   # capacities (seconds)
$PY cad/build.py                                # STEP + interference/mass/fit checks (~2 min)
$PY cam/lathe_cam.py                            # lathe G-code + stock-removal simulation (~1 min)
xvfb-run -a -s "-screen 0 1600x1000x24" $PY cam/mill_cam.py      # fixture G-code + CAMotics check (~1 min)
$PY cad/drawings.py                             # shop drawings (seconds)
$PY analysis/verify_axifea.py                   # CalculiX vs closed-form answers (seconds)
THERMAL_JOBS=4 $PY analysis/thermal.py          # all 20 thermal cases (~40 min)
$PY analysis/thermal_report.py                  # summary, limits, alarm timing, plots
$PY analysis/structural.py                      # B pressure / vacuum / hot field, glass stress (~10 min)
$PY analysis/handcalcs.py                       # closed-form checks and hot clearances
xvfb-run -a -s "-screen 0 2400x1600x24" $PY cad/render.py lineup b a c
xvfb-run -a -s "-screen 0 1920x1080x24" $PY cad/build_gif.py     # collision sweep + animation (~5 min)
$PY bom/make_bom.py                             # BOM.md from the catalogue lookups
if [ -d "${VENDOR_STEP_DIR:-/tmp/bomwork}" ]; then $PY cad/vendor_check.py; fi   # needs the vendors' STEP files
echo "done"
