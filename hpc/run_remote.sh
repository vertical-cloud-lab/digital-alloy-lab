#!/usr/bin/env bash
# hpc/run_remote.sh — Run a command on BYU ORC via the existing master socket.
#
# Usage:
#     bash hpc/run_remote.sh '<command>'
#     bash hpc/run_remote.sh --host orc '<command>'
#
# Requires that `bash hpc/connect.sh` has already established a master SSH
# socket. This script intentionally refuses to re-trigger authentication —
# that has to be a deliberate, operator-supervised step (see hpc/README.md).

set -euo pipefail

HOST="orc"
if [[ "${1:-}" == "--host" ]]; then
    shift
    HOST="${1:?--host requires a value}"
    shift
fi

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 [--host <alias>] '<remote command>'" >&2
    exit 2
fi

if ! ssh -O check "${HOST}" >/dev/null 2>&1; then
    cat >&2 <<EOF
[run_remote.sh] ERROR: no master SSH socket open for '${HOST}'.
[run_remote.sh] Run \`bash hpc/connect.sh\` first (it will prompt you for your
[run_remote.sh] ORC password and 6-digit verification code), then retry.
EOF
    exit 1
fi

# BatchMode=yes guarantees ssh will fail fast if for some reason the master
# socket is unhealthy, rather than silently dropping back to a password
# prompt that would never be answered in a non-interactive context.
exec ssh -o BatchMode=yes "${HOST}" "$@"
