#!/usr/bin/env bash
# Re-run every check of the desktop LPBF on the current model, one after another, each under a memory cap
# (the runner has 4 cores and 15 GB; one run on this branch died of OOM with several simulations at once).
#
#   bash desktop-lpbf/analysis/rerun_all.sh [step ...]      # default: all steps, in the order below
#
# Needs the environment in low-profile.md ("Re-running"): /tmp/venv (Python 3.12 + analysis/requirements.txt), CalculiX,
# LIGGGHTS, Docker with opencfd/openfoam-run:2406, xvfb-run, and /tmp/capmem (a memory-cap wrapper: systemd-run --scope
# with MemoryMax, or ulimit -v). Logs go to /tmp/rerun/<step>.log; a one-line result per step to /tmp/rerun/summary.tsv.
set -u
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
PY=/tmp/venv/bin/python
D=desktop-lpbf
A=$D/analysis
LOG=/tmp/rerun
mkdir -p "$LOG"
X="xvfb-run -a -s '-screen 0 1920x1080x24'"

declare -A STEP=(
  [interference_M50]="$PY $A/interference.py M50"
  [interference_S25]="$PY $A/interference.py S25 S"
  [interference_L75]="$PY $A/interference.py L75 L"
  [mass]="$PY $A/mass_budget.py"
  [tray]="$PY $A/tray/tray_budget.py"
  [seals]="$PY $A/seals/seals.py"
  [door_seal_fea]="OMP_NUM_THREADS=2 $PY $A/seals/door_seal_fea.py"
  [mech]="$PY $A/mech/mech_checks.py"
  [joint_calcs]="$PY $A/hotswap/joint_calcs.py"
  [hotswap_fea]="OMP_NUM_THREADS=2 $X $PY $A/hotswap/hotswap_fea.py"
  [fea]="OMP_NUM_THREADS=2 $X $PY $A/fea/fea.py"
  [thermal_module]="OMP_NUM_THREADS=2 $PY $A/thermal_module.py"
  [thermal_laser]="OMP_NUM_THREADS=1 $PY $A/thermal_laser.py"
  [mujoco]="OMP_NUM_THREADS=1 $PY $A/mujoco_check.py"
  [ops_M50]="OMP_NUM_THREADS=1 $X $PY $A/ops/run_ops.py $D/cad M50"
  [ops_S25]="OMP_NUM_THREADS=1 $PY $A/ops/run_ops.py $D/cad S25 --no-png --only=S1,S2,S3,U1,U4"
  [ops_L75]="OMP_NUM_THREADS=1 $PY $A/ops/run_ops.py $D/cad L75 --no-png --only=S1,S2,S3,U1,U4"
  [cfd_coarse]="mkdir -p /tmp/cfd && $PY $A/cfd/make_case.py --res coarse --iters 1500 --out /tmp/cfd/coarse --cad-dir $D/cad && $A/cfd/run_case.sh /tmp/cfd/coarse"
  [dem_baseline]="OMP_NUM_THREADS=1 $PY $A/powder/dem_spread.py run --gap 100 --speed 50 --coh low"
)
ORDER=(interference_M50 interference_S25 interference_L75 mass tray seals door_seal_fea mech joint_calcs hotswap_fea fea
       thermal_module thermal_laser mujoco ops_M50 ops_S25 ops_L75 cfd_coarse dem_baseline)
CAP=(); declare -A CAPGB=([fea]=5 [hotswap_fea]=4 [thermal_module]=5 [door_seal_fea]=4 [mujoco]=4 [ops_M50]=4 [cfd_coarse]=4)

want=("$@")
[ ${#want[@]} -eq 0 ] && want=("${ORDER[@]}")
for s in "${want[@]}"; do
  cmd=${STEP[$s]:-}
  [ -z "$cmd" ] && { echo "unknown step $s"; continue; }
  gb=${CAPGB[$s]:-3}
  t0=$(date +%s)
  echo "$(date -u +%H:%M:%S) start $s (cap ${gb} GB)"
  bash -c "/tmp/capmem $gb bash -c \"$cmd\"" > "$LOG/$s.log" 2>&1
  rc=$?
  dt=$(( $(date +%s) - t0 ))
  printf '%s\t%s\t%ss\t%s\n' "$s" "$rc" "$dt" "$(tail -n 1 "$LOG/$s.log" | cut -c1-160)" | tee -a "$LOG/summary.tsv"
done
