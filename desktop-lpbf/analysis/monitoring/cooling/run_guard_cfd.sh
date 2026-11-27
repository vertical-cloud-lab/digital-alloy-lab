#!/bin/bash
# Solve one case written by guard_cfd.py (monitoring/cooling.md §4.2) in the OpenCFD v2406 Docker image, 2 MPI ranks.
#   desktop-lpbf/analysis/monitoring/cooling/run_guard_cfd.sh /tmp/guard-cfd/typ12            # checkMesh + buoyantSimpleFoam + age
#   desktop-lpbf/analysis/monitoring/cooling/run_guard_cfd.sh /tmp/guard-cfd/busy12 /tmp/guard-cfd/typ12   # start from typ12's field
# On the shared runner wrap it in the heavy-job queue: /tmp/heavy 4 <this script> <case>. Keep cases under /tmp, not in the repo.
set -euo pipefail
CASE=$(realpath "$1")
SRC=${2:-}
NP=${NP:-2}
IMG=opencfd/openfoam-run:2406
EXTRA=()
CMD='cd /case && checkMesh > log.checkMesh 2>&1; '
if [ -n "$SRC" ]; then
  SRC=$(realpath "$SRC")
  EXTRA=(-v "$SRC":/src:ro)
  CMD+='mapFields /src -consistent -sourceTime latestTime > log.mapFields 2>&1; '
fi
CMD+="foamDictionary -entry numberOfSubdomains -set $NP system/decomposeParDict > /dev/null && "
CMD+='rm -rf processor* && decomposePar -force > log.decomposePar 2>&1 && '
CMD+="mpirun -np $NP buoyantSimpleFoam -parallel > log.buoyantSimpleFoam 2>&1; "
CMD+='reconstructPar -latestTime > log.reconstructPar 2>&1 && rm -rf processor* && '
CMD+='buoyantSimpleFoam -postProcess -dict system/ageDict -latestTime > log.age 2>&1'
docker run --rm --memory=4g --cpus=2 --shm-size=256m --user "$(id -u):$(id -g)" -e HOME=/tmp -e OMP_NUM_THREADS=1 \
  -e OMPI_MCA_btl_vader_single_copy_mechanism=none -e OMPI_MCA_rmaps_base_oversubscribe=1 \
  -v "$CASE":/case "${EXTRA[@]}" -w /case "$IMG" bash -c "$CMD"
tail -n 12 "$CASE/log.buoyantSimpleFoam"
