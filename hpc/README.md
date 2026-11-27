# BYU HPC (Office of Research Computing) — Connection & Setup

Notes and helper scripts for connecting to the BYU Office of Research Computing
(ORC / "RC") supercomputer at <https://rc.byu.edu> from a local workstation or
from an automation agent (e.g. GitHub Copilot, Edison Scientific, an SDL
controller). Used by the FLAIME project for parallel CALPHAD sweeps
(TC-Python, pycalphad), BoTorch / GPyTorch surrogate training, and pKGFN
acquisition runs (see `genesis-mission-proposal/flaime-genesis-proposal.tex`,
"Computing" subsection of Appendix 2).

## TL;DR

1. Get an ORC account at <https://rc.byu.edu/account/create/> (separate from
   your campus NetID — ORC maintains its own credentials).
2. Enroll in ORC's two-factor authentication (separate from campus Duo).
3. Drop [`ssh_config.example`](ssh_config.example) into `~/.ssh/config`
   (replacing `<your-orc-username>`), then either:
   - Run `bash hpc/connect.sh` once per work session — type your password and
     6-digit verification code at the prompts. The master socket persists, so
     subsequent `ssh orc …`, `scp … orc:…`, `rsync … orc:…`, and
     `bash hpc/run_remote.sh '…'` calls require **no** further authentication.
   - Or, when running under an automation agent, use
     [`python hpc/connect_with_file_totp.py`](connect_with_file_totp.py) — it
     reads the 6-digit verification code from the committed file
     [`hpc/tmp/totp.txt`](tmp/totp.txt) and supplies the password from
     `$BYU_HPC_PASSWORD`. The operator pushes a fresh code to that file
     whenever the agent needs to authenticate; the agent `git pull`-s and
     reruns the wrapper. If the code is rejected (TOTPs roll every 30 s),
     the agent should poll for a fresh code for up to ~5 min before
     surfacing the failure to the operator — see
     [`.github/copilot-instructions.md`](../.github/copilot-instructions.md)
     for the full agent-side protocol.
   - The lower-level [`python hpc/agent_connect.py`](agent_connect.py) is
     also available if you need a custom `CredentialProvider` (e.g. routing
     either credential through a chat reply, a different one-shot file, or
     a REST endpoint). The default provider reads the password from
     `$BYU_HPC_PASSWORD` and the verification code interactively via
     `getpass`. **Never** invoke either entry point with
     `log_file=sys.stderr` — `pexpect`'s `logfile_read` echoes the password
     we send back through the transcript and would leak the secret.
4. When you're done: `bash hpc/disconnect.sh` (or just let `ControlPersist`
   time out).

## Why this design

BYU ORC has three properties that constrain how automation can talk to it
([source](https://rc.byu.edu/wiki/?id=Two-Factor+Authentication)):

1. **Two-factor authentication is mandatory** for every login (NIST SP 800-171
   compliance for federal contracts).
2. **SSH keys are disallowed.** ORC explicitly rejects them as single-factor.
3. **ORC runs its own 2FA system, not campus Duo** — there is no
   push-notification "click approval"; the second factor is always a
   short-lived 6-digit verification code (TOTP-style) that must be typed in.

Together these mean a fully unattended SSH session is impossible. The closest
practical pattern is:

- Authenticate **once** per work session, interactively, with a human
  supplying the verification code.
- Use OpenSSH's [`ControlMaster` / `ControlPersist`](https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing)
  to keep that authenticated channel open, and route every later command
  (whether issued by a human, a script, or an LLM agent) through the same
  socket. This is the pattern ORC themselves recommend on their
  [SSH Multiplexing](https://rc.byu.edu/wiki/index.php?page=SSH+Multiplexing)
  wiki page.
- For agent-driven workflows, expose the prompt-and-collect step as a small
  human-in-the-loop interaction: the agent triggers the login, surfaces each
  prompt to the operator, and ingests the password + 6-digit code from
  whatever channel the operator is using (env var for the password,
  committed `hpc/tmp/totp.txt` file for the verification code, etc.). Once
  the master socket is up, the agent can fire any number of follow-up
  commands non-interactively.

## Files in this directory

| File | What it does |
| ---- | ---- |
| [`ssh_config.example`](ssh_config.example) | Drop-in `~/.ssh/config` block defining a `Host orc` alias with `ControlMaster auto`, `ControlPersist`, and `ServerAliveInterval`. Mirrors the BYU ORC wiki recommendation. |
| [`connect.sh`](connect.sh) | Opens the master SSH session interactively. Run once per work session. Idempotent — re-running it just verifies the existing master is alive. |
| [`run_remote.sh`](run_remote.sh) | Runs an arbitrary command on `orc` via the existing master socket. Errors out (with a clear message) if no master socket is open. |
| [`disconnect.sh`](disconnect.sh) | Cleanly tears down the master socket (`ssh -O exit orc`). |
| [`agent_connect.py`](agent_connect.py) | Python `pexpect` helper that scripts the human-in-the-loop 2FA flow. Default `CredentialProvider` reads `$BYU_HPC_PASSWORD` for the password and prompts interactively (via `getpass`) for the verification code. Suitable as a building block for custom credential channels. |
| [`connect_with_file_totp.py`](connect_with_file_totp.py) | Agent-facing wrapper around `agent_connect.py` that reads the 6-digit verification code from `tmp/totp.txt` instead of prompting interactively. The committed `hpc/tmp/totp.txt` file is the supported channel for delivering TOTPs to automation agents (operator pushes a fresh code, agent `git pull`-s and runs the wrapper, polls for fresh codes if rejected). |
| [`tmp/totp.txt`](tmp/totp.txt) | Single-line file holding the operator-supplied TOTP for the current login attempt. Overwritten frequently; never read for any purpose other than the next SSH login. |
| [`bofn_benchmark/`](bofn_benchmark/README.md) | SLURM-native port of the `bofn_benchmark.yaml` GitHub Actions sweep — `sbatch --array=1-N` over `(algo, seed)` cells, then `sbatch --dependency=afterany:` to combine. Includes `setup_env.sh`, `submit.sh`, `run_cell.slurm`, `combine.slurm`, and `fetch_results.sh`. |

## Typical workflow from a workstation

```bash
# One-time:
cat hpc/ssh_config.example >> ~/.ssh/config
# Then edit ~/.ssh/config and replace `<your-orc-username>` with your ORC
# login name. `sed -i` works for this but its syntax differs between GNU
# (Linux) and BSD (macOS) sed:
#     # Linux:
#     sed -i 's/<your-orc-username>/sgbaird/' ~/.ssh/config
#     # macOS (BSD sed requires an empty backup-suffix string after -i):
#     sed -i '' 's/<your-orc-username>/sgbaird/' ~/.ssh/config
# Or just edit the file in your preferred editor to avoid the portability
# wrinkle altogether.

# Per work session:
bash hpc/connect.sh                       # type password + 6-digit code once

bash hpc/run_remote.sh 'sinfo -s'         # check cluster status
bash hpc/run_remote.sh 'squeue -u $USER'  # list your jobs
rsync -avz ./calphad_sweep orc:fsl_groups/fslg_vcl/compute/   # copy inputs
bash hpc/run_remote.sh 'cd fsl_groups/fslg_vcl/compute/calphad_sweep && sbatch run.slurm'

# When done (optional — ControlPersist will reap on its own):
bash hpc/disconnect.sh
```

## Typical workflow from an automation agent

The agent should treat `connect_with_file_totp.py` (or `agent_connect.py`,
or `connect.sh`) as a one-shot gate. With the file-based wrapper:

1. Operator pushes the current 6-digit code to `hpc/tmp/totp.txt`.
2. Agent `git pull`-s (to pick up the fresh code) and runs
   `python hpc/connect_with_file_totp.py`.
3. If the wrapper reports the code was rejected (TOTPs roll every 30 s),
   the agent polls `git pull` every ~15 s for at least 5 min, retrying the
   wrapper whenever `tmp/totp.txt` changes. **Returning control to the
   operator before that 5-min window expires forces them to spin up a
   brand-new agent session, so always poll first.**
4. Once `ssh -O check orc` succeeds, every downstream command — `ssh orc …`,
   `scp`, `rsync`, `bash hpc/run_remote.sh '…'`, `bash hpc/bofn_benchmark/submit.sh`
   — reuses the master socket without re-authenticating, for the full
   `ControlPersist` window (8 h).

If `connect.sh` (or the wrapper) is invoked while a healthy master socket
already exists, it exits 0 without prompting — so an agent can call it
defensively at the start of each task.

## Storage layout on ORC

Group storage for the FLAIME project lives under
`~/fsl_groups/fslg_vcl/` (path subject to confirmation when the group is
provisioned). Use `compute/` for active runs, `nobackup/` for scratch, and
`groupfs/` for shared inputs (CALPHAD databases, surrogate checkpoints).

## Software stack

- **Scheduler**: SLURM. See <https://rc.byu.edu/wiki/?id=SLURM+Commands>.
- **Modules**: `module avail`, `module load python/3.11`, etc.
- **Conda / venvs**: install user-level under
  `~/fsl_groups/fslg_vcl/groupfs/envs/` so all FLAIME team members share the
  same surrogate-training stack (BoTorch, GPyTorch, pycalphad, TC-Python).
- **Thermo-Calc**: TCAL10 + TCMG6 + AM Module licenses (commitment letter
  from Thermo-Calc AB, see proposal Appendix 2 / Appendix 7). Coordinate
  license-server access with ORC staff before first batch run.

## Troubleshooting

- **"`ControlSocket … already exists, disabling multiplexing`"** — a stale
  socket from a crashed session. Run `bash hpc/disconnect.sh` (or
  `rm ~/.ssh/master-*.socket`) and retry.
- **Verification code rejected** — codes are time-based; check that your
  workstation clock is synced (NTP). Try the next code rather than retyping
  the same one.
- **Long-running command killed on a login node** — login nodes kill
  most processes after ~1 hour. Submit a SLURM job (`sbatch`) or use an
  interactive allocation (`salloc`).

## References

- ORC main site: <https://rc.byu.edu>
- Logging In: <https://rc.byu.edu/wiki/?id=Logging+In>
- Two-Factor Authentication: <https://rc.byu.edu/wiki/?id=Two-Factor+Authentication>
- SSH Multiplexing: <https://rc.byu.edu/wiki/index.php?page=SSH+Multiplexing>
- SLURM Commands: <https://rc.byu.edu/wiki/?id=SLURM+Commands>
- Open OnDemand (browser-based alternative): <https://rc.byu.edu/wiki/?id=Open+OnDemand>
