#!/bin/bash
# Mesh and solve one case written by make_case.py, in the OpenCFD v2406 Docker image (3 GB, 1.5 CPUs).
#
#   desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/fine            # blockMesh + checkMesh + simpleFoam
#   desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/fine map /tmp/cfd/coarse   # same, starting from a coarser solution
#
# Logs go to <case>/log.*; the solution to <case>/<last iteration>/. Keep cases under /tmp, not in the repo.
set -euo pipefail
CASE=$(realpath "$1")
MODE=${2:-plain}
SRC=${3:-}
IMG=opencfd/openfoam-run:2406
EXTRA=()
CMD='cd /case && blockMesh > log.blockMesh 2>&1 && checkMesh > log.checkMesh 2>&1; '
if [ "$MODE" = map ] && [ -n "$SRC" ]; then
  SRC=$(realpath "$SRC")
  EXTRA=(-v "$SRC":/src:ro)
  CMD+='mapFields /src -consistent -sourceTime latestTime > log.mapFields 2>&1; '
fi
CMD+='simpleFoam > log.simpleFoam 2>&1'
docker run --rm --memory=3g --cpus=1.5 --user "$(id -u):$(id -g)" -e OMP_NUM_THREADS=1 \
  -v "$CASE":/case "${EXTRA[@]}" -w /case "$IMG" bash -c "$CMD"
tail -n 30 "$CASE/log.simpleFoam"
