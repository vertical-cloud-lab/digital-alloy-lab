#!/usr/bin/env bash
# hpc/bofn_benchmark/setup_env.sh — one-time per-account setup on ORC.
#
# Creates a Python venv at $REPO_DIR/.venv and installs requirements.txt
# into it. Idempotent: re-running upgrades the existing venv in place.
#
# Run this once (per ORC account) after cloning the repo onto ORC and
# before invoking submit.sh:
#
#     ssh orc
#     cd ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private
#     bash hpc/bofn_benchmark/setup_env.sh
#
# Environment:
#   PYTHON_MODULE  module name for python on ORC (default: python/3.11)

set -euo pipefail

PYTHON_MODULE="${PYTHON_MODULE:-python/3.11}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "${REPO_DIR}"

if command -v module >/dev/null 2>&1; then
    set +e
    module load "${PYTHON_MODULE}"
    set -e
fi

if [[ ! -d .venv ]]; then
    echo "[setup_env] creating ${REPO_DIR}/.venv with $(python --version)"
    python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "[setup_env] OK. python=$(python -V), venv=${REPO_DIR}/.venv"
