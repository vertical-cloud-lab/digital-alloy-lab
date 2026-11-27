#!/usr/bin/env bash
#SBATCH --job-name=bofn-combine
#SBATCH --nodes=1
#SBATCH --ntasks=1
# All other resource directives are supplied by submit.sh.
#
# Required env (via sbatch --export):
#   RUN_ID        — sweep tag (also written into the output filenames)
#   RESULTS_DIR   — directory of per-cell JSONs (input to combine)
#   FIGURES_DIR   — directory for the combined plot + summary CSV/JSON (output)
#   PYTHON_MODULE — module to `module load`
#   REPO_DIR      — repo root on ORC

set -euo pipefail

: "${RESULTS_DIR:?RESULTS_DIR env var required}"
: "${FIGURES_DIR:?FIGURES_DIR env var required}"
: "${REPO_DIR:?REPO_DIR env var required}"

cd "${REPO_DIR}"

if command -v module >/dev/null 2>&1 && [[ -n "${PYTHON_MODULE:-}" ]]; then
    set +e
    module load "${PYTHON_MODULE}"
    set -e
fi

if [[ -f "${REPO_DIR}/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${REPO_DIR}/.venv/bin/activate"
fi

export PYTHONUNBUFFERED=1

mkdir -p "${FIGURES_DIR}"

n_results=$(find "${RESULTS_DIR}" -maxdepth 1 -name '*.json' | wc -l)
echo "[combine] RUN_ID=${RUN_ID} found ${n_results} per-cell JSONs in ${RESULTS_DIR}"

if [[ "${n_results}" -eq 0 ]]; then
    echo "[combine] ERROR: no per-cell JSONs to combine. Did every array task fail?" >&2
    exit 3
fi

python -u benchmarks/bofn_actions_benchmark.py \
    --mode combine \
    --input-dir "${RESULTS_DIR}" \
    --out-dir "${FIGURES_DIR}"

echo "[combine] OK; outputs in ${FIGURES_DIR}"
ls -lh "${FIGURES_DIR}"
