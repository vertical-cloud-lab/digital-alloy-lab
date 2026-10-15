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
     `python hpc/agent_connect.py` — it opens the SSH connection and surfaces
     each prompt to the operator. The default `CredentialProvider` reads the
     password from the `$BYU_HPC_PASSWORD` env var if set (falling back to
     interactive `getpass`) and reads the verification code interactively via
     `getpass`; routing either credential through a different channel (chat
     reply, one-shot file, REST endpoint) requires supplying a custom
     `CredentialProvider` — see the example sketch at the bottom of
     `agent_connect.py`. In Copilot agent runs the password is supplied via
     the `BYU_HPC_PASSWORD` GitHub Actions secret (exposed as the
     `$BYU_HPC_PASSWORD` env var). **Never** echo, log, `cat`, `grep`, or
     otherwise surface the value of that env var. The 6-digit verification
     code is **not** a stored secret — the operator sends it as a steering
     message once per session, and the persisted `ControlMaster` socket
     covers all follow-up commands.
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
  whatever channel the operator is using (stdin, a chat reply, a one-shot
  file, etc.). Once the master socket is up, the agent can fire any number of
  follow-up commands non-interactively.

## Files in this directory

| File | What it does |
| ---- | ---- |
| [`ssh_config.example`](ssh_config.example) | Drop-in `~/.ssh/config` block defining a `Host orc` alias with `ControlMaster auto`, `ControlPersist`, and `ServerAliveInterval`. Mirrors the BYU ORC wiki recommendation. |
| [`connect.sh`](connect.sh) | Opens the master SSH session interactively. Run once per work session. Idempotent — re-running it just verifies the existing master is alive. |
| [`run_remote.sh`](run_remote.sh) | Runs an arbitrary command on `orc` via the existing master socket. Errors out (with a clear message) if no master socket is open. |
| [`disconnect.sh`](disconnect.sh) | Cleanly tears down the master socket (`ssh -O exit orc`). |
| [`agent_connect.py`](agent_connect.py) | Python `pexpect` helper that scripts the human-in-the-loop 2FA flow described above. Suitable for use from automation agents. |
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

The agent should treat `agent_connect.py` (or `connect.sh`) as a one-shot
gate: ask the operator for the password and the current verification code,
let `pexpect` complete the handshake, then issue all downstream work through
`run_remote.sh` (or by SSHing through the established master socket
directly). Example agent prompt template is included in
[`agent_connect.py`](agent_connect.py).

If `connect.sh` is invoked while a healthy master socket already exists, it
exits 0 without prompting — so an agent can call it defensively at the start
of each task.

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
