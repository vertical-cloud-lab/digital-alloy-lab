#!/bin/bash
# Mesh and solve one case written by make_case.py, in the OpenCFD v2406 Docker image (4 GB, 2 CPUs).
#
#   desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/fine            # blockMesh + checkMesh + simpleFoam
#   desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/fine map /tmp/cfd/coarse   # same, starting from a coarser solution
#   NP=1 desktop-lpbf/analysis/cfd/run_case.sh /tmp/cfd/coarse     # serial (as in the 2026-11-20 runs)
#
# NP (default 2) > 1 splits the mesh with decomposePar (scotch), runs simpleFoam on NP MPI ranks and reconstructs the last
# time step, so post.py reads the case as before. Logs go to <case>/log.*; the solution to <case>/<last iteration>/.
# Keep cases under /tmp, not in the repo. On a shared runner, run one case at a time.
set -euo pipefail
CASE=$(realpath "$1")
MODE=${2:-plain}
SRC=${3:-}
NP=${NP:-2}
IMG=opencfd/openfoam-run:2406
EXTRA=()
CMD='cd /case && blockMesh > log.blockMesh 2>&1 && checkMesh > log.checkMesh 2>&1; '
if [ "$MODE" = map ] && [ -n "$SRC" ]; then
  SRC=$(realpath "$SRC")
  EXTRA=(-v "$SRC":/src:ro)
  CMD+='mapFields /src -consistent -sourceTime latestTime > log.mapFields 2>&1; '
fi
if [ "$NP" -gt 1 ]; then
  CMD+="foamDictionary -entry numberOfSubdomains -set $NP system/decomposeParDict > /dev/null && "
  CMD+='rm -rf processor* && decomposePar -force > log.decomposePar 2>&1 && '
  CMD+="mpirun -np $NP simpleFoam -parallel > log.simpleFoam 2>&1; "
  CMD+='reconstructPar -latestTime > log.reconstructPar 2>&1 && rm -rf processor*'
else
  CMD+='simpleFoam > log.simpleFoam 2>&1'
fi
docker run --rm --memory=4g --cpus=2 --shm-size=256m --user "$(id -u):$(id -g)" -e HOME=/tmp -e OMP_NUM_THREADS=1 \
  -e OMPI_MCA_btl_vader_single_copy_mechanism=none -e OMPI_MCA_rmaps_base_oversubscribe=1 \
  -v "$CASE":/case "${EXTRA[@]}" -w /case "$IMG" bash -c "$CMD"
tail -n 30 "$CASE/log.simpleFoam"
