#!/usr/bin/env bash
#SBATCH --job-name=bofn-cell
#SBATCH --nodes=1
#SBATCH --ntasks=1
# All other resource directives (--time, --mem, --cpus-per-task, --array,
# --output, --error, --partition, --export) are supplied by submit.sh so the
# same SLURM script can serve every (algo, seed) cell without editing.
#
# Required env (passed via sbatch --export from submit.sh):
#   RUN_ID         — unique sweep tag
#   MANIFEST       — absolute path to manifest.txt (one "algo<TAB>seed" per line)
#   RESULTS_DIR    — directory for per-cell JSON output
#   PYTHON_MODULE  — module name to `module load` for python
#   REPO_DIR       — repo root on ORC

set -euo pipefail

: "${SLURM_ARRAY_TASK_ID:?run_cell.slurm must be invoked as an array task}"
: "${MANIFEST:?MANIFEST env var required}"
: "${RESULTS_DIR:?RESULTS_DIR env var required}"
: "${REPO_DIR:?REPO_DIR env var required}"

# 1) Look up this cell's (algo, seed) from the manifest.
line=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${MANIFEST}")
if [[ -z "${line}" ]]; then
    echo "[run_cell] ERROR: manifest line ${SLURM_ARRAY_TASK_ID} is empty (${MANIFEST})" >&2
    exit 2
fi
algo="${line%%$'\t'*}"
seed="${line##*$'\t'}"
out="${RESULTS_DIR}/${algo}_seed${seed}.json"

echo "[run_cell] RUN_ID=${RUN_ID} task=${SLURM_ARRAY_TASK_ID} algo=${algo} seed=${seed}"
echo "[run_cell] node=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-1} time=$(date -u +%FT%TZ)"
echo "[run_cell] writing ${out}"

# 2) Activate the shared env. We prefer a venv at
#    $REPO_DIR/.venv (created by setup_env.sh) so every cell sees the exact
#    same dependency set as the one captured in requirements.txt.
cd "${REPO_DIR}"

if command -v module >/dev/null 2>&1 && [[ -n "${PYTHON_MODULE:-}" ]]; then
    # `module` is a shell function on most clusters and may print to stderr;
    # don't let that abort `set -e`.
    set +e
    module load "${PYTHON_MODULE}"
    rc=$?
    set -e
    if [[ "${rc}" -ne 0 ]]; then
        echo "[run_cell] WARN: module load ${PYTHON_MODULE} returned ${rc}; continuing with PATH python." >&2
    fi
fi

if [[ -f "${REPO_DIR}/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${REPO_DIR}/.venv/bin/activate"
else
    echo "[run_cell] WARN: ${REPO_DIR}/.venv not found; using system python. Run hpc/bofn_benchmark/setup_env.sh first." >&2
fi

export PYTHONUNBUFFERED=1

# 3) Run the cell. -u is also set in case .venv overrides PYTHONUNBUFFERED.
mkdir -p "$(dirname "${out}")"
python -u benchmarks/bofn_actions_benchmark.py \
    --mode run \
    --algo "${algo}" \
    --seed "${seed}" \
    --out "${out}"

echo "[run_cell] done at $(date -u +%FT%TZ)"
