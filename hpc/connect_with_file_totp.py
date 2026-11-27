#!/usr/bin/env python3
"""Open the BYU ORC SSH master session, reading the 6-digit TOTP from
``hpc/tmp/totp.txt`` instead of via interactive prompt or steering reply.

This is the agent-facing entry point for the file-based TOTP ingestion
workflow. The operator commits a fresh 6-digit code to ``hpc/tmp/totp.txt``
and pushes; the agent ``git pull``-s and runs this script. The wrapper
reads the file at SSH-prompt time so a new code that arrives while the
script is launching is still seen.

If the code is rejected (expired — TOTPs roll every 30 s) the script exits
non-zero. The agent should poll (``git pull``) for a fresh value and rerun
within a ~5-minute window before returning control to the operator (see
``.github/copilot-instructions.md``).

The password is supplied via the ``BYU_HPC_PASSWORD`` env var (read by the
default :class:`agent_connect.CredentialProvider`); the SSH transcript is
NOT logged anywhere so the password prompt is never echoed.
"""
import sys
from pathlib import Path

HPC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HPC_DIR))
from agent_connect import CredentialProvider, open_master_session  # noqa: E402

TOTP_FILE = HPC_DIR / "tmp" / "totp.txt"


def read_totp(host: str) -> str:
    code = TOTP_FILE.read_text().strip().split()[0]
    print(
        f"[wrapper] supplying TOTP from {TOTP_FILE.relative_to(HPC_DIR.parent)} "
        f"(length={len(code)})",
        flush=True,
    )
    return code


if __name__ == "__main__":
    creds = CredentialProvider(verification_code=read_totp)
    # NB: deliberately no log_file=sys.stderr — pexpect's logfile_read echoes
    # the password we send back, which would leak $BYU_HPC_PASSWORD to logs.
    ok = open_master_session(host="orc", credentials=creds)
    sys.exit(0 if ok else 1)
