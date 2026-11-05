#!/bin/bash
# Driver: run PhaseForge sqscal for a binary at a given SQS level with GRACE via MaterialsFramework.
# Usage: PhaseForge-run_sqscal.sh <workdir> <elements e.g. Cu,Ni> <lattices e.g. FCC_A1> <level>
# Run it through the scrubbed wrapper with HOME=/tmp/arroyave/home (ATAT's .atat.rc and the GRACE model cache live there):
#   HOME=/tmp/arroyave/home /tmp/sbx/clean bash PhaseForge-run_sqscal.sh /tmp/arroyave/work/pf-CuNi Cu,Ni FCC_A1 1
set -u
WD=$1; EL=$2; LAT=$3; LV=$4
export PATH=${PF_SHIM:+$PF_SHIM:}/tmp/arroyave/venvs/paipai/bin:/tmp/arroyave/work/PhaseForge/install/bin:/tmp/arroyave/atat/bin:$PATH
export OMP_NUM_THREADS=2 TF_NUM_INTRAOP_THREADS=2 TF_NUM_INTEROP_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2 CUDA_VISIBLE_DEVICES=""
mkdir -p "$WD" && cd "$WD"
echo "start $(date -u +%T)"
/usr/bin/time -v sqscal -e "$EL" -l "$LAT" -lv "$LV" -mlip Grace -model GRACE-2L-OMAT
rc=$?
echo "sqscal rc=$rc end $(date -u +%T)"
# per-structure timings: python runs leave 'energy' files; list their mtimes
find . -name energy -printf '%TT %p\n' | sort
