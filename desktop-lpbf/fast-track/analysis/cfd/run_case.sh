#!/bin/bash
# Mesh and solve one case written by make_case.py, in the OpenCFD v2406 Docker image (4 GB, 2 CPUs), one container.
#
#   run_case.sh <case> mesh solve                 # blockMesh, snappyHexMesh, ports, checkMesh, then simpleFoam (2 ranks)
#   run_case.sh <case> mesh                       # mesh only
#   run_case.sh <case> copymesh <src> solve       # take <src>'s mesh (constant/polyMesh), then solve
#   run_case.sh <case> scalar <src>               # scalarTransportFoam on <src>'s mesh and its last U and phi
#   run_case.sh <case> copymesh <src> buoyant     # rhoReactingBuoyantFoam on <src>'s mesh
#   run_case.sh <case> map <src> pimple           # pimpleFoam (time-averaged) from <src>'s steady solution
#   run_case.sh <case> recon                      # reconstruct the time directories left in <case>/processor*
#
# Wrap it in the memory ledger:  /tmp/tools/capmem 4 bash run_case.sh ...  (capmem drops the docker group, so the
# client runs under sudo -n). Logs go to <case>/log.*. Keep cases under /tmp, not in the repo.
set -euo pipefail
CASE=$(realpath "$1"); shift
NP=${NP:-2}
IMG=opencfd/openfoam-run:2406
MOUNTS=(-v "$CASE":/case)
CMD='set -e; cd /case; '
par() {  # $1 = solver
  CMD+="foamDictionary -entry numberOfSubdomains -set $NP system/decomposeParDict > /dev/null; "
  CMD+='rm -rf processor*; decomposePar -force > log.decomposePar 2>&1; '
  CMD+="mpirun -np $NP $1 -parallel > log.$1 2>&1 || true; "
  CMD+='reconstructPar > log.reconstructPar 2>&1; rm -rf processor*; '      # every written time (snapshots)
}
while [ $# -gt 0 ]; do
  case "$1" in
    mesh)
      CMD+='blockMesh > log.blockMesh 2>&1; surfaceFeatureExtract > log.surfaceFeatureExtract 2>&1; '
      CMD+='snappyHexMesh -overwrite > log.snappyHexMesh 2>&1; topoSet > log.topoSet 2>&1; '
      CMD+='createPatch -overwrite > log.createPatch 2>&1; checkMesh > log.checkMesh 2>&1 || true; '
      shift ;;
    copymesh)
      SRC=$(realpath "$2"); MOUNTS+=(-v "$SRC":/src:ro)
      CMD+='rm -rf constant/polyMesh; cp -r /src/constant/polyMesh constant/; '
      shift 2 ;;
    solve)
      par simpleFoam; shift ;;
    map)        # start from <src>'s last solution (same mesh), then run pimpleFoam
      SRC=$(realpath "$2"); MOUNTS+=(-v "$SRC":/src:ro)
      CMD+='rm -rf constant/polyMesh; cp -r /src/constant/polyMesh constant/; '
      CMD+='T=$(foamListTimes -case /src -latestTime | tail -1); cp /src/$T/U /src/$T/p /src/$T/phi 0/; '
      shift 2 ;;
    pimple)
      par pimpleFoam; shift ;;
    scalar)
      SRC=$(realpath "$2"); MOUNTS+=(-v "$SRC":/src:ro)
      CMD+='rm -rf constant/polyMesh; cp -r /src/constant/polyMesh constant/; '
      CMD+='T=$(foamListTimes -case /src -latestTime | tail -1); cp /src/$T/U /src/$T/phi 0/; '
      par scalarTransportFoam; shift 2 ;;
    buoyant)
      par rhoReactingBuoyantFoam; shift ;;
    recon)
      CMD+='reconstructPar > log.reconstructPar.recon 2>&1; rm -rf processor*; '; shift ;;
    *) echo "unknown step $1"; exit 2 ;;
  esac
done
sudo -n docker run --rm --memory=4g --cpus=2 --shm-size=256m --user "$(id -u):$(id -g)" -e HOME=/tmp -e OMP_NUM_THREADS=1 \
  -e OMPI_MCA_btl_vader_single_copy_mechanism=none -e OMPI_MCA_rmaps_base_oversubscribe=1 \
  "${MOUNTS[@]}" -w /case "$IMG" bash -c "$CMD"
ls "$CASE"
