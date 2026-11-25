#!/bin/bash
# Write and solve the plume-study cases one after another (monitoring/plume.md, "Re-running").
# Each solve is analysis/cfd/run_case.sh: OpenFOAM v2406 in Docker, 4 GB, 2 CPUs, simpleFoam on 2 MPI ranks.
# Cases stay in $C (default /tmp/plume); nothing is written to the repo.
#   p200      : the recommended layout (gas-flow.md §0: screens, 35 mm outlet channel, upper slot), 200 + 40 L/min, LW purge off
#   p200_lw3  : the same with 3 L/min of argon across the LW cover slide (started from p200's field)
#   p140      : 140 + 30 L/min, LW purge off (started from p200's field)
#   p200_lw1  : 200 + 40 L/min with 1 L/min across the LW slide (started from p200_lw3's field)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
D=$(cd "$HERE/../../.." && pwd)                 # desktop-lpbf/
PY=${PY:-/tmp/venv/bin/python}
C=${C:-/tmp/plume}
MK="$PY $HERE/make_case_plume.py --cad-dir $D/cad"
RUN=$D/analysis/cfd/run_case.sh
CASES=${CASES:-"p200 p200_lw3 p140 p200_lw1"}
for c in $CASES; do
  if [ -f "$C/$c/done" ]; then echo "$c: done already"; continue; fi
  case $c in
    p200)     $MK --variant fix --q-lpm 200 --upper-lpm 40 --iters 800 --out $C/p200;                     $RUN $C/p200 ;;
    p200_lw3) $MK --variant fix --q-lpm 200 --upper-lpm 40 --lw-purge-lpm 3 --iters 400 --out $C/p200_lw3; $RUN $C/p200_lw3 map $C/p200 ;;
    p140)     $MK --variant fix --q-lpm 140 --upper-lpm 30 --iters 500 --out $C/p140;                     $RUN $C/p140 map $C/p200 ;;
    p200_lw1) $MK --variant fix --q-lpm 200 --upper-lpm 40 --lw-purge-lpm 1 --iters 300 --out $C/p200_lw1; $RUN $C/p200_lw1 map $C/p200_lw3 ;;
    *) echo "unknown case $c"; exit 1 ;;
  esac
  date -u > "$C/$c/done"
  echo "$c: finished $(date -u +%H:%M:%S)"
done
