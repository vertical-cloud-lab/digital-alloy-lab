#!/usr/bin/env bash
# hpc/bofn_benchmark/fetch_results.sh — pull benchmark outputs from ORC back
# to this workstation, into the local repo tree.
#
# Pulls three things, all keyed by RUN_ID:
#
#   1. Per-cell JSON results        →   benchmarks/results/actions_hpc/<RUN_ID>/
#   2. Combined plot + summary CSV  →   benchmarks/figures/actions_hpc/<RUN_ID>/
#   3. SLURM logs + manifest        →   hpc/runs/<RUN_ID>/
#
# Usage (after `bash hpc/connect.sh`):
#
#     RUN_ID=<run_id> bash hpc/bofn_benchmark/fetch_results.sh
#     RUN_ID=latest    bash hpc/bofn_benchmark/fetch_results.sh   # picks the newest
#
# Environment variables:
#   HOST           ssh alias for ORC                   (default: orc)
#   REMOTE_ROOT    parent dir of the repo on ORC      (default: ~/fsl_groups/fslg_vcl/compute)
#   REPO_NAME      directory name of the repo on ORC  (default: digital-alloy-lab-private)
#   RUN_ID         sweep tag, OR "latest"             (REQUIRED)
#   DRY_RUN        if set, prints rsync commands only

set -euo pipefail

HOST="${HOST:-orc}"
REMOTE_ROOT="${REMOTE_ROOT:-~/fsl_groups/fslg_vcl/compute}"
REPO_NAME="${REPO_NAME:-digital-alloy-lab-private}"
RUN_ID="${RUN_ID:?RUN_ID env var required (or set RUN_ID=latest)}"
DRY_RUN="${DRY_RUN:-}"

if ! ssh -O check "${HOST}" >/dev/null 2>&1; then
    echo "[fetch_results] ERROR: no master SSH socket to '${HOST}'. Run 'bash hpc/connect.sh' (or 'python hpc/agent_connect.py') first." >&2
    exit 1
fi

# Resolve "latest" by inspecting the remote hpc/runs/ directory.
if [[ "${RUN_ID}" == "latest" ]]; then
    RUN_ID="$(ssh "${HOST}" \
        "ls -1t ${REMOTE_ROOT}/${REPO_NAME}/hpc/runs/ 2>/dev/null | head -n1")"
    if [[ -z "${RUN_ID}" ]]; then
        echo "[fetch_results] ERROR: no runs found under ${REMOTE_ROOT}/${REPO_NAME}/hpc/runs/" >&2
        exit 1
    fi
    echo "[fetch_results] resolved RUN_ID=latest → ${RUN_ID}"
fi

LOCAL_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
mkdir -p \
    "${LOCAL_REPO}/benchmarks/results/actions_hpc/${RUN_ID}" \
    "${LOCAL_REPO}/benchmarks/figures/actions_hpc/${RUN_ID}" \
    "${LOCAL_REPO}/hpc/runs/${RUN_ID}"

rsync_opts=(-avz --partial --info=stats1)
if [[ -n "${DRY_RUN}" ]]; then
    rsync_opts+=(--dry-run)
fi

REMOTE_BASE="${REMOTE_ROOT}/${REPO_NAME}"

echo "[fetch_results] pulling per-cell JSONs..."
rsync "${rsync_opts[@]}" \
    "${HOST}:${REMOTE_BASE}/benchmarks/results/actions_hpc/${RUN_ID}/" \
    "${LOCAL_REPO}/benchmarks/results/actions_hpc/${RUN_ID}/"

echo "[fetch_results] pulling combined plot + summary..."
rsync "${rsync_opts[@]}" \
    "${HOST}:${REMOTE_BASE}/benchmarks/figures/actions_hpc/${RUN_ID}/" \
    "${LOCAL_REPO}/benchmarks/figures/actions_hpc/${RUN_ID}/"

echo "[fetch_results] pulling SLURM logs + manifest..."
rsync "${rsync_opts[@]}" \
    "${HOST}:${REMOTE_BASE}/hpc/runs/${RUN_ID}/" \
    "${LOCAL_REPO}/hpc/runs/${RUN_ID}/"

cat <<EOF
[fetch_results] OK. Local outputs:
    ${LOCAL_REPO}/benchmarks/results/actions_hpc/${RUN_ID}/
    ${LOCAL_REPO}/benchmarks/figures/actions_hpc/${RUN_ID}/
    ${LOCAL_REPO}/hpc/runs/${RUN_ID}/    (manifest.txt, submission.env, logs/)

These paths intentionally mirror the GH-Actions output layout
(benchmarks/figures/actions_full/) but with an actions_hpc/<RUN_ID>/ suffix
so multiple sweeps coexist without clobbering each other.
EOF
