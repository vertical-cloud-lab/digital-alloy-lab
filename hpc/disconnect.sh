#!/usr/bin/env bash
# hpc/disconnect.sh — Tear down the master SSH socket to BYU ORC.
#
# Usage:
#     bash hpc/disconnect.sh [host_alias]

set -euo pipefail

HOST="${1:-orc}"

if ssh -O check "${HOST}" >/dev/null 2>&1; then
    ssh -O exit "${HOST}"
    echo "[disconnect.sh] Closed master SSH socket to '${HOST}'." >&2
else
    echo "[disconnect.sh] No master SSH socket open for '${HOST}'. Nothing to do." >&2
fi
