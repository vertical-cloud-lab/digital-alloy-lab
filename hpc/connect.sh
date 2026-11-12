#!/usr/bin/env bash
# hpc/connect.sh — Open (or reuse) an interactive master SSH session to BYU ORC.
#
# Usage:
#     bash hpc/connect.sh [host_alias]
#
# host_alias defaults to "orc" (matching hpc/ssh_config.example). The script
# is idempotent: if a healthy master socket already exists for the host, it
# exits 0 without prompting for credentials. Otherwise it invokes ssh in
# foreground mode so the operator can type their password and the 6-digit
# verification code interactively. ControlPersist (set in ssh_config) keeps
# the socket alive for downstream automation after this script exits.
#
# BYU ORC requires two-factor authentication on every fresh login and
# disallows SSH keys; see hpc/README.md for context.

set -euo pipefail

HOST="${1:-orc}"

if ssh -O check "${HOST}" >/dev/null 2>&1; then
    echo "[connect.sh] Master SSH socket to '${HOST}' is already open. Nothing to do." >&2
    exit 0
fi

cat >&2 <<EOF
[connect.sh] Opening master SSH session to '${HOST}' (BYU Office of Research Computing).
[connect.sh] You will be prompted for your ORC password and a 6-digit verification code.
[connect.sh] After authentication, the socket persists per ControlPersist in ~/.ssh/config,
[connect.sh] and downstream commands (run_remote.sh, scp, rsync, sbatch wrappers) will reuse it.

EOF

# -N: do not execute a remote command; -f: background after auth (so the
# master socket persists without holding this terminal). We do NOT use -f
# alone because it would background before the password/2FA prompts; instead
# we use the standard recipe of letting ssh attach to the tty for the prompts
# and then forking once authentication completes.
#
# We deliberately do NOT rely on `set -e` to surface ssh failures here: a
# rejected password, Ctrl-C, or transient network error would otherwise
# abort the script before the explicit post-check below ever ran, denying
# the user the diagnostic message.
if ! ssh -fN "${HOST}"; then
    echo "[connect.sh] ERROR: ssh exited non-zero before backgrounding (auth rejected, Ctrl-C, or network error)." >&2
    exit 1
fi

if ssh -O check "${HOST}" >/dev/null 2>&1; then
    echo "[connect.sh] Master SSH socket to '${HOST}' is now open." >&2
else
    echo "[connect.sh] ERROR: ssh exited but no master socket is present." >&2
    exit 1
fi
