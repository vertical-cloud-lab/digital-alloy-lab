#!/usr/bin/env python3
"""hpc/agent_connect.py — Human-in-the-loop SSH login to BYU ORC.

This script implements the explicit "agent triggers, human supplies 2FA code"
pattern described in the issue that this directory was created to address.

It spawns ``ssh <host>`` (default ``orc``, defined in ``hpc/ssh_config.example``),
watches for the ORC password prompt and the 6-digit verification-code prompt,
asks the operator for each value through whichever channel is configured, and
hands a healthy ``ControlMaster`` socket off to downstream automation.

Why a Python helper at all?
---------------------------
``hpc/connect.sh`` already covers the "human at a TTY" case. ``agent_connect.py``
adds two things that are awkward to do in pure shell:

1. **Programmatic prompt collection.** The agent (e.g. GitHub Copilot, an SDL
   controller, a Slack bot) can plug its own ``CredentialProvider`` into this
   module and have the password / verification code arrive from chat replies,
   a one-shot file written by the operator, an environment variable, etc. —
   instead of being pinned to ``stdin``.
2. **Robust prompt matching.** ORC's prompt wording has shifted over the
   years (``Password:`` vs ``ORC password:`` vs ``Verification code:``). The
   patterns are centralized here so any change is a one-line fix.

The default ``CredentialProvider`` reads from ``stdin`` with ``getpass``, which
makes the script equally usable from a plain terminal::

    python hpc/agent_connect.py
    python hpc/agent_connect.py --host orc --then 'sinfo -s'

Security notes
--------------
* The verification code is short-lived (TOTP-style) and is not persisted.
* The password is read into memory only for as long as the ssh handshake
  takes, then dropped. It is never logged, never echoed, never written to
  disk by this script.
* No SSH key is generated or used — ORC explicitly disallows them.
* The persisted artifact is the OpenSSH ``ControlMaster`` socket file (see
  ``ControlPath`` in ``hpc/ssh_config.example``), which is readable only by
  the local user and automatically reaped by ``ControlPersist``.
"""

from __future__ import annotations

import argparse
import getpass
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

try:
    import pexpect
except ImportError:  # pragma: no cover - import error path
    sys.stderr.write(
        "agent_connect.py requires the 'pexpect' package.\n"
        "Install it with:  pip install pexpect\n"
    )
    raise

DEFAULT_HOST = "orc"

# Patterns are matched case-insensitively (re.IGNORECASE inside pexpect via
# the regex). Order matters only for documentation; pexpect.expect returns
# the index of whichever matches first.
PASSWORD_PROMPTS = [
    r"(?i)password:\s*",
]
VERIFICATION_PROMPTS = [
    r"(?i)verification code:\s*",
    r"(?i)verification\s+code\s*:?\s*",
    r"(?i)one-?time\s+password.*:\s*",
    r"(?i)token\s*:\s*",
]
# First-connection host-key confirmation. When ssh hits this we just send
# "yes" and continue — the alternative is to fail closed and demand the
# operator pre-pin the fingerprint. The accompanying ssh_config.example sets
# `StrictHostKeyChecking accept-new`, which suppresses this prompt entirely
# on most OpenSSH versions, but we still handle it defensively for users
# whose ~/.ssh/config doesn't include that line.
HOST_KEY_PROMPTS = [
    r"(?i)are you sure you want to continue connecting.*\?\s*",
]
SUCCESS_HINTS = [
    r"\$\s*$",  # generic prompt
    r"#\s*$",
    r"Last login:",
    r"Welcome",
]


@dataclass
class CredentialProvider:
    """Pluggable source for password and verification code.

    The defaults read interactively from the controlling TTY using
    :func:`getpass.getpass`, which is appropriate when a human is sitting in
    front of the terminal that launched the agent.  When the agent runs in a
    different process (e.g. background worker, chat bot), supply callables
    that block until the operator replies through whatever channel the agent
    uses (chat reply, polled file, REST endpoint, etc.).
    """

    password: Callable[[str], str] = field(
        default_factory=lambda: lambda host: (
            # Prefer the BYU_HPC_PASSWORD env var (populated from the
            # eponymous GitHub Actions secret in agent runs); fall back to
            # interactive getpass on a workstation. We deliberately do not
            # echo, log, or otherwise surface the value of this env var.
            os.environ.get("BYU_HPC_PASSWORD")
            or getpass.getpass(f"[ORC {host}] password: ")
        )
    )
    verification_code: Callable[[str], str] = field(
        default_factory=lambda: lambda host: getpass.getpass(
            f"[ORC {host}] 6-digit verification code: "
        )
    )


def _master_socket_alive(host: str) -> bool:
    """Return True iff ssh -O check reports a healthy master socket."""
    try:
        result = subprocess.run(
            ["ssh", "-O", "check", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0


def open_master_session(
    host: str = DEFAULT_HOST,
    credentials: Optional[CredentialProvider] = None,
    timeout: int = 60,
    log_file=None,
) -> bool:
    """Open a persistent master SSH session to ``host``.

    Returns True on success, False on failure. Idempotent: if a healthy master
    socket already exists for ``host``, this returns True immediately without
    prompting the operator.

    Parameters
    ----------
    host:
        SSH ``Host`` alias as defined in ``~/.ssh/config`` (default: ``orc``,
        per ``hpc/ssh_config.example``). Must already be configured with
        ``ControlMaster auto`` and ``ControlPersist``.
    credentials:
        :class:`CredentialProvider` describing how to obtain the password and
        verification code. Defaults to interactive ``getpass`` on the
        controlling TTY.
    timeout:
        Per-prompt timeout in seconds.
    log_file:
        Optional file-like object that pexpect will copy the SSH session
        transcript to. Useful for debugging prompt-matching changes; do NOT
        point it at a shared/persistent file in production because the
        transcript may contain banner text.
    """
    if shutil.which("ssh") is None:
        raise RuntimeError("ssh not found on PATH")

    if _master_socket_alive(host):
        sys.stderr.write(
            f"[agent_connect] Master SSH socket to '{host}' already open; "
            "reusing it.\n"
        )
        return True

    creds = credentials or CredentialProvider()

    # -fN cannot be used here because pexpect needs to interact with the ssh
    # process before it backgrounds. Instead, request a no-op remote command
    # ('true') that returns immediately after authentication; ControlMaster
    # auto + ControlPersist keep the multiplexed socket alive afterwards.
    child = pexpect.spawn(
        "ssh",
        [host, "true"],
        timeout=timeout,
        encoding="utf-8",
    )
    if log_file is not None:
        child.logfile = log_file

    try:
        # 0) Optional first-connection host-key prompt. Loop because ssh
        # may also emit other transient banners we want to skim past
        # before reaching the password prompt.
        for _ in range(2):
            idx = child.expect(
                HOST_KEY_PROMPTS
                + PASSWORD_PROMPTS
                + [pexpect.EOF, pexpect.TIMEOUT]
            )
            n_h = len(HOST_KEY_PROMPTS)
            n_p = len(PASSWORD_PROMPTS)
            if idx < n_h:
                child.sendline("yes")
                continue
            break

        # 1) Password prompt.
        if idx >= n_h + n_p:
            # idx points at EOF (n_h + n_p) or TIMEOUT (n_h + n_p + 1).
            is_timeout = idx == n_h + n_p + 1
            reason = "timed out waiting for" if is_timeout else "exited before"
            buffered = (child.before or "").strip()
            tail = f" Last output: {buffered!r}" if buffered else ""
            sys.stderr.write(
                f"[agent_connect] ssh {reason} a password prompt.{tail}\n"
            )
            child.close(force=True)
            return False
        try:
            password = creds.password(host)
        except Exception as exc:
            sys.stderr.write(
                "[agent_connect] credential provider failed to supply a "
                f"password ({type(exc).__name__}: {exc}). When running "
                "non-interactively, set $BYU_HPC_PASSWORD or pass a custom "
                "CredentialProvider.\n"
            )
            child.close(force=True)
            return False
        child.sendline(password)

        # 2) Verification code prompt. Some hosts ask for the password again
        # if the first attempt failed; we surface that to the operator
        # instead of silently retrying.
        idx = child.expect(
            VERIFICATION_PROMPTS
            + PASSWORD_PROMPTS
            + SUCCESS_HINTS
            + [pexpect.EOF, pexpect.TIMEOUT]
        )
        n_v = len(VERIFICATION_PROMPTS)
        n_p = len(PASSWORD_PROMPTS)
        n_s = len(SUCCESS_HINTS)
        if idx < n_v:
            try:
                code = creds.verification_code(host)
            except Exception as exc:
                sys.stderr.write(
                    "[agent_connect] credential provider failed to supply a "
                    f"verification code ({type(exc).__name__}: {exc}).\n"
                )
                child.close(force=True)
                return False
            child.sendline(code)
        elif idx < n_v + n_p:
            sys.stderr.write(
                "[agent_connect] ssh asked for the password again — the first "
                "attempt was rejected. Aborting; please retry.\n"
            )
            child.close(force=True)
            return False
        elif idx < n_v + n_p + n_s:
            # No 2FA prompt — uncommon for ORC, but not an error.
            pass
        else:
            is_timeout = idx == n_v + n_p + n_s + 1
            reason = "timed out waiting for" if is_timeout else "hit EOF before"
            buffered = (child.before or "").strip()
            tail = f" Last output: {buffered!r}" if buffered else ""
            sys.stderr.write(
                f"[agent_connect] ssh {reason} a verification-code prompt.{tail}\n"
            )
            child.close(force=True)
            return False

        # 3) Wait for ssh to finish the no-op command. The master socket
        # outlives this child process thanks to ControlPersist. ORC's
        # response to a rejected 2FA code is to re-display the password
        # prompt, so we watch for that explicitly to surface a clearer
        # error than a generic pexpect timeout.
        idx = child.expect(
            PASSWORD_PROMPTS + [pexpect.EOF, pexpect.TIMEOUT],
            timeout=timeout,
        )
        if idx < n_p:
            sys.stderr.write(
                "[agent_connect] ssh re-prompted for the password after the "
                "verification code was sent — the 2FA code was rejected "
                "(likely expired; TOTPs roll every 30 s). Please retry with "
                "a fresh code.\n"
            )
            child.close(force=True)
            return False
        if idx == n_p + 1:  # TIMEOUT
            buffered = (child.before or "").strip()
            tail = f" Last output: {buffered!r}" if buffered else ""
            sys.stderr.write(
                f"[agent_connect] ssh did not exit after authentication.{tail}\n"
            )
            child.close(force=True)
            return False
        child.close()
    except pexpect.ExceptionPexpect as exc:
        sys.stderr.write(f"[agent_connect] pexpect error: {exc}\n")
        try:
            child.close(force=True)
        except Exception:  # pragma: no cover - defensive
            pass
        return False

    if child.exitstatus not in (0, None):
        sys.stderr.write(
            f"[agent_connect] ssh exited with status {child.exitstatus}; "
            "authentication likely failed.\n"
        )
        return False

    if not _master_socket_alive(host):
        sys.stderr.write(
            "[agent_connect] ssh exited 0 but no master socket is present — "
            "check that ControlMaster/ControlPersist are set in ~/.ssh/config.\n"
        )
        return False

    sys.stderr.write(
        f"[agent_connect] Master SSH socket to '{host}' is now open.\n"
    )
    return True


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Open a master SSH session to BYU ORC using a human-in-the-loop "
            "2FA flow (operator supplies password + 6-digit verification code)."
        ),
    )
    p.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"SSH Host alias from ~/.ssh/config (default: {DEFAULT_HOST}).",
    )
    p.add_argument(
        "--then",
        metavar="CMD",
        default=None,
        help=(
            "Optional remote command to run after the master socket is open. "
            "Equivalent to: bash hpc/run_remote.sh '<CMD>'."
        ),
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Per-prompt timeout in seconds (default: 60).",
    )
    return p


def main(argv: Optional[list] = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    ok = open_master_session(host=args.host, timeout=args.timeout)
    if not ok:
        return 1

    if args.then:
        # Reuse the master socket via plain ssh in BatchMode so a missing
        # socket fails fast instead of triggering a (silent) password prompt.
        rc = subprocess.call(
            ["ssh", "-o", "BatchMode=yes", args.host, args.then],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        return rc

    return 0


# ---------------------------------------------------------------------------
# Reference: example agent prompt template
# ---------------------------------------------------------------------------
# When invoking this module from an automation agent that talks to the
# operator over a side channel (chat, web UI, etc.), supply a custom
# CredentialProvider whose callbacks block until the operator replies.
# A minimal sketch:
#
#     from hpc.agent_connect import CredentialProvider, open_master_session
#
#     def ask_operator_password(host):
#         return chat.ask(
#             f"Please send your BYU ORC password for `{host}` (it will be "
#             "used once for ssh authentication and immediately discarded)."
#         )
#
#     def ask_operator_otp(host):
#         return chat.ask(
#             f"Please send the current 6-digit verification code for "
#             f"BYU ORC `{host}`."
#         )
#
#     creds = CredentialProvider(
#         password=ask_operator_password,
#         verification_code=ask_operator_otp,
#     )
#     assert open_master_session(host="orc", credentials=creds)
#
# After this returns True, the agent can shell out to `ssh orc …`,
# `bash hpc/run_remote.sh '…'`, or `rsync … orc:…` without further
# operator interaction (until ControlPersist expires).
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    sys.exit(main())
