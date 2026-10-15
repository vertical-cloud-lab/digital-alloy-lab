#!/usr/bin/env bash
# hpc/bofn_benchmark/submit.sh
#
# Submit the BOFN+pKGFN benchmark to BYU ORC (SLURM) as a job array of
# (algo, seed) cells, plus a dependency-chained combine job that aggregates
# every cell's per-(algo,seed) JSON into a single cost-efficiency plot.
#
# This is the SLURM-native equivalent of the GitHub Actions workflow
# `.github/workflows/bofn_benchmark.yaml` (PR #14):
#
#       smoke-test   →   full-test (matrix: algo × seed)   →   combine
#                          ↓                                       ↑
#                 sbatch --array=1-N run_cell.slurm                |
#                          ↓                                       |
#         sbatch --dependency=afterany:$ARRAY_JOBID combine.slurm  ┘
#
# `afterany` mirrors GH-Actions `if: always() && (success || failure)` so a
# partial sweep (e.g. one cell hits its wall-clock cap) still produces a plot
# of the survivors.
#
# Usage (from your workstation, after `bash hpc/connect.sh` so the master
# socket is open):
#
#     bash hpc/bofn_benchmark/submit.sh                # all 7 algos × 20 seeds = 140 cells
#     ALGOS='Random pKGFN' SEEDS='0 1 2' bash hpc/bofn_benchmark/submit.sh
#     RUN_ID=debug-$(date +%s) bash hpc/bofn_benchmark/submit.sh
#
# Or from this directory once already on ORC:
#
#     ssh orc 'cd ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private \
#              && bash hpc/bofn_benchmark/submit.sh'
#
# Environment variables:
#   HOST          ssh alias for ORC                          (default: orc)
#   REMOTE_ROOT   parent dir on ORC for the cloned repo      (default: ~/fsl_groups/fslg_vcl/compute)
#   REPO_NAME     directory name of the repo on ORC          (default: digital-alloy-lab-private)
#   RUN_ID        unique tag for this sweep                  (default: $(git rev-parse --short HEAD)-$(date +%Y%m%dT%H%M%SZ))
#   ALGOS         space-separated algorithm names            (default: Random Sobol LowFidOnly Node2Only HighFidOnly TSFN pKGFN)
#   SEEDS         space-separated integer seeds              (default: 0 .. 19)
#   PARTITION     SLURM partition for cell jobs              (default: empty → cluster default)
#   CELL_TIME     wall-clock per cell                        (default: 06:00:00, mirrors GH-Actions 360-min cap)
#   CELL_MEM      memory per cell                            (default: 8G)
#   CELL_CPUS     cpus-per-task per cell                     (default: 4)
#   PYTHON_MODULE `module load` arg for python               (default: python/3.11)
#   DRY_RUN       if non-empty, print the sbatch lines but   (default: empty)
#                 don't actually submit
#
# Outputs (on ORC, all under $REMOTE_ROOT/$REPO_NAME):
#     hpc/runs/<run_id>/manifest.txt                       — algo,seed per line
#     hpc/runs/<run_id>/logs/cell-<task>.{out,err}         — per-cell SLURM logs
#     hpc/runs/<run_id>/logs/combine.{out,err}             — combine SLURM logs
#     benchmarks/results/actions_hpc/<run_id>/*.json       — per-cell results
#     benchmarks/figures/actions_hpc/<run_id>/*            — combined plot + summary
#
# Pull everything back to the workstation with:
#     RUN_ID=<run_id> bash hpc/bofn_benchmark/fetch_results.sh

set -euo pipefail

HOST="${HOST:-orc}"
REMOTE_ROOT="${REMOTE_ROOT:-~/fsl_groups/fslg_vcl/compute}"
REPO_NAME="${REPO_NAME:-digital-alloy-lab-private}"

# Compute a default RUN_ID locally only if we can; on ORC we let the remote
# shell compute it instead.
SCRIPT_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd 2>/dev/null || echo "")"
if [[ -z "${RUN_ID:-}" ]]; then
    if [[ -n "${SCRIPT_REPO_ROOT}" ]] && git -C "${SCRIPT_REPO_ROOT}" rev-parse --short HEAD >/dev/null 2>&1; then
        sha="$(git -C "${SCRIPT_REPO_ROOT}" rev-parse --short HEAD)"
    else
        sha="nogit"
    fi
    RUN_ID="${sha}-$(date -u +%Y%m%dT%H%M%SZ)"
fi

ALGOS="${ALGOS:-Random Sobol LowFidOnly Node2Only HighFidOnly TSFN pKGFN}"
SEEDS="${SEEDS:-0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19}"

PARTITION="${PARTITION:-}"
CELL_TIME="${CELL_TIME:-06:00:00}"
CELL_MEM="${CELL_MEM:-8G}"
CELL_CPUS="${CELL_CPUS:-4}"
PYTHON_MODULE="${PYTHON_MODULE:-python/3.11}"
DRY_RUN="${DRY_RUN:-}"

# Detect whether we're already on ORC. If not, re-exec via ssh so the rest of
# the script runs in the cluster shell (where sbatch / module live).
if ! command -v sbatch >/dev/null 2>&1; then
    echo "[submit.sh] Local invocation; re-running on ${HOST} via the existing master SSH socket." >&2
    if ! ssh -O check "${HOST}" >/dev/null 2>&1; then
        echo "[submit.sh] ERROR: no master SSH socket to '${HOST}'. Run 'bash hpc/connect.sh' (or 'python hpc/agent_connect.py') first." >&2
        exit 1
    fi
    # Forward the relevant env vars and run submit.sh remotely.
    ssh "${HOST}" \
        "cd ${REMOTE_ROOT}/${REPO_NAME} \
         && RUN_ID='${RUN_ID}' \
            ALGOS='${ALGOS}' \
            SEEDS='${SEEDS}' \
            PARTITION='${PARTITION}' \
            CELL_TIME='${CELL_TIME}' \
            CELL_MEM='${CELL_MEM}' \
            CELL_CPUS='${CELL_CPUS}' \
            PYTHON_MODULE='${PYTHON_MODULE}' \
            DRY_RUN='${DRY_RUN}' \
         bash hpc/bofn_benchmark/submit.sh"
    exit $?
fi

# --- below this line we are running on ORC ---

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUN_DIR="${REPO_DIR}/hpc/runs/${RUN_ID}"
LOG_DIR="${RUN_DIR}/logs"
RESULTS_DIR="${REPO_DIR}/benchmarks/results/actions_hpc/${RUN_ID}"
FIGURES_DIR="${REPO_DIR}/benchmarks/figures/actions_hpc/${RUN_ID}"

mkdir -p "${LOG_DIR}" "${RESULTS_DIR}" "${FIGURES_DIR}"

manifest="${RUN_DIR}/manifest.txt"
: > "${manifest}"
for algo in ${ALGOS}; do
    for seed in ${SEEDS}; do
        printf '%s\t%s\n' "${algo}" "${seed}" >> "${manifest}"
    done
done
N=$(wc -l < "${manifest}")
if [[ "${N}" -eq 0 ]]; then
    echo "[submit.sh] ERROR: empty manifest (ALGOS or SEEDS unset)." >&2
    exit 1
fi

echo "[submit.sh] RUN_ID=${RUN_ID}"
echo "[submit.sh] manifest: ${manifest} (${N} cells)"
echo "[submit.sh] results : ${RESULTS_DIR}"
echo "[submit.sh] figures : ${FIGURES_DIR}"
echo "[submit.sh] logs    : ${LOG_DIR}"

partition_arg=()
if [[ -n "${PARTITION}" ]]; then
    partition_arg=(--partition="${PARTITION}")
fi

# 1) Submit the per-(algo, seed) array job.
array_cmd=(
    sbatch
    --parsable
    --job-name="bofn-cell-${RUN_ID}"
    --array="1-${N}"
    --time="${CELL_TIME}"
    --mem="${CELL_MEM}"
    --cpus-per-task="${CELL_CPUS}"
    --output="${LOG_DIR}/cell-%a.out"
    --error="${LOG_DIR}/cell-%a.err"
    --export="ALL,RUN_ID=${RUN_ID},MANIFEST=${manifest},RESULTS_DIR=${RESULTS_DIR},PYTHON_MODULE=${PYTHON_MODULE},REPO_DIR=${REPO_DIR}"
    "${partition_arg[@]}"
    "${REPO_DIR}/hpc/bofn_benchmark/run_cell.slurm"
)

if [[ -n "${DRY_RUN}" ]]; then
    printf '[dry-run] %q ' "${array_cmd[@]}"; echo
    array_jid="DRYRUN_ARRAY"
else
    array_jid="$("${array_cmd[@]}")"
    echo "[submit.sh] submitted array job ${array_jid} (${N} cells)"
fi

# 2) Submit the combine job, dependent on the array. `afterany` waits for
#    every array task to terminate (success OR failure), mirroring the
#    GH-Actions `if: always() && (success || failure)` semantics.
combine_cmd=(
    sbatch
    --parsable
    --job-name="bofn-combine-${RUN_ID}"
    --dependency="afterany:${array_jid}"
    --kill-on-invalid-dep=yes
    --time="00:30:00"
    --mem=4G
    --cpus-per-task=2
    --output="${LOG_DIR}/combine.out"
    --error="${LOG_DIR}/combine.err"
    --export="ALL,RUN_ID=${RUN_ID},RESULTS_DIR=${RESULTS_DIR},FIGURES_DIR=${FIGURES_DIR},PYTHON_MODULE=${PYTHON_MODULE},REPO_DIR=${REPO_DIR}"
    "${partition_arg[@]}"
    "${REPO_DIR}/hpc/bofn_benchmark/combine.slurm"
)

if [[ -n "${DRY_RUN}" ]]; then
    printf '[dry-run] %q ' "${combine_cmd[@]}"; echo
    combine_jid="DRYRUN_COMBINE"
else
    combine_jid="$("${combine_cmd[@]}")"
    echo "[submit.sh] submitted combine job ${combine_jid} (depends on ${array_jid})"
fi

# 3) Persist the manifest + job IDs so fetch_results.sh can correlate things
#    and so the operator has an audit trail.
cat > "${RUN_DIR}/submission.env" <<EOF
RUN_ID=${RUN_ID}
ARRAY_JOBID=${array_jid}
COMBINE_JOBID=${combine_jid}
N_CELLS=${N}
ALGOS=${ALGOS}
SEEDS=${SEEDS}
SUBMITTED_AT=$(date -u +%Y%m%dT%H%M%SZ)
SUBMITTED_BY=${USER:-unknown}@${HOSTNAME:-unknown}
EOF

cat <<EOF
[submit.sh] OK. To monitor:
    ssh ${HOST} 'squeue -u \$USER'
    ssh ${HOST} 'tail -f ${LOG_DIR}/cell-1.out'
[submit.sh] To pull results back to your workstation once the combine job
            finishes:
    RUN_ID=${RUN_ID} bash hpc/bofn_benchmark/fetch_results.sh
EOF
