#!/bin/bash
# sqscal's FCC branch run step by step (works around the silent sqscal failure; see REPORT.md).
# Usage (via wrapper): HOME=/tmp/arroyave/home /tmp/sbx/clean bash PhaseForge-manual_sqscal_fcc.sh <workdir> <El1,El2> <level>
set -u; WD=$1; EL=$2; LV=$3
export PATH=/tmp/arroyave/results/phaseforge/scripts/PhaseForge-shim:/tmp/arroyave/venvs/paipai/bin:/tmp/arroyave/work/PhaseForge/install/bin:/tmp/arroyave/atat/bin:$PATH
export OMP_NUM_THREADS=2 TF_NUM_INTRAOP_THREADS=2 TF_NUM_INTEROP_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2 CUDA_VISIBLE_DEVICES=""
mkdir -p "$WD" && cd "$WD"
t0=$(date +%s)
sqs2tdb -cp -sp="$EL" -l=FCC_A1 -lv="$LV" < /dev/null; sqs2tdb -cp -sp="$EL" -l=FCC_A1 -lv="$LV" < /dev/null
cd FCC_A1; t1=$(date +%s)
csh -fc "foreachfile str.out pwd \; runstruct_MLIP -mlip=Grace -model=GRACE-2L-OMAT" < /dev/null
t2=$(date +%s)
printf '1,0\n2,0\n' > terms.in; sqs2tdb -fit < /dev/null; cd ..; sqs2tdb -tdb -oc < /dev/null; t3=$(date +%s)
echo "TIMING copy_sqs=$((t1-t0))s mlip_relax=$((t2-t1))s fit_tdb=$((t3-t2))s"
for d in FCC_A1/sqs_lev*; do echo "ENERGY $d $(cat $d/energy 2>/dev/null)"; done
