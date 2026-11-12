## Edison Scientific

If using Edison Scientific, you may need to wait up until 10 minutes to get the response. If you're an agent, sleep for 10 minutes (to avoid consuming requests unecessarily), and then every 5 minutes after that. Start with a 15 minute wait if using high effort literature query type. If you need to upload files, use analysis query type. See the docs: https://edisonscientific.gitbook.io/edison-cookbook/edison-client. Here is the endpoint you should use: https://api.platform.edisonscientific.com. The API key is EDISON_PLATFORM_API_KEY. Don't expose this secret, e.g., by echoing or grepping it. Pass the API key in explicitly:

```
from edison_client import EdisonClient, JobNames
client = EdisonClient(api_key=EDISON_PLATFORM_API_KEY)
```

Whenever you retrieve results (either during the current agent session or during the next session), make sure to fetch and commit all artifacts associated with a trajectory.

If using Edison Analysis, refer to https://docs.edisonscientific.com/edison-client/file-management#upload for instructions on how to upload files. If able to use Context7, to better inform use of EdisonClient, see https://context7.com/future-house/edison-client-docs/llms.txt?tokens=10000

## GitHub Copilot Cloud Agent

- Include plots directly in your comment reply via `![image name](https://github.com/<user/org>/<repo>/blob/<shortened-commit-hash>/<filename>?raw=true)`. Truncate the commit hash to the first 7 characters only. For example, `https://github.com/AccelerationConsortium/evaluation-metrics/blob/52754e7/scripts/bo_benchmarks/demonstrations/branin_campaign_demonstration_results.png?raw=true`. For provenance, ensure you use the shortened (7-character) commit hash, not the branch name
- If you mention files in your comment reply, add direct hyperlinks based on the shortened (7-character) commit hash
- IMPORTANT: Never echo/grep/print environment secrets. These should never be exposed in your terminal history or other outputs

## BYU HPC (ORC) Access

The BYU Office of Research Computing password is provided to agent runs via the `BYU_HPC_PASSWORD` GitHub Actions secret. It is exposed as the `BYU_HPC_PASSWORD` environment variable.

- Do **not** echo, `cat`, `grep`, `printenv`, `env | grep`, write to a file, log, or otherwise surface the value of `$BYU_HPC_PASSWORD` (or any variable derived from it) anywhere — not in shell output, not in commit messages, not in PR descriptions, not in steering replies, not in source files. Treat it like a secret key.
- Do **not** hard-code the password in scripts, tests, fixtures, or `.env` files.
- Pass it to tooling implicitly via the environment. The default `CredentialProvider` in `hpc/agent_connect.py` already reads `$BYU_HPC_PASSWORD` and feeds it directly into the SSH password prompt without echoing it. Use that path; do **not** read the variable yourself just to pipe it elsewhere.
- **Never** invoke `agent_connect.py` (or the wrapper) with `log_file=sys.stderr`. `pexpect`'s `logfile_read` would echo the password we send back through the transcript and leak `$BYU_HPC_PASSWORD` into shell output. If you absolutely need an SSH transcript for debugging, write to a file under `/tmp/` and shred it immediately.
- The 6-digit 2FA verification code (TOTP) is **not** a secret stored anywhere — it rolls every 30 s. The operator commits the current code to `hpc/tmp/totp.txt` and pushes; the agent ingests it via `git pull` rather than via a steering reply. The supported workflow is:
  1. Write `~/.ssh/config` from `hpc/ssh_config.example`, substituting `$BYU_HPC_USERNAME` for `<your-orc-username>`.
  2. Run `python hpc/connect_with_file_totp.py` (the file-based wrapper). It reads `hpc/tmp/totp.txt` at prompt time, supplies the password from `$BYU_HPC_PASSWORD`, and opens the persistent `ControlMaster` socket (8 h `ControlPersist`).
  3. If the script reports the code was rejected (expired), **do not return control immediately**. Poll `git pull` every ~15 s for at least 5 min; whenever `hpc/tmp/totp.txt` changes, rerun the wrapper. Only escalate to the operator if no fresh code lands in that window. Returning control too quickly forces the operator to spin up a brand new agent session.
  4. Once `ssh -O check orc` succeeds, the master socket covers all follow-up commands (`ssh orc …`, `scp`, `rsync`, `bash hpc/run_remote.sh '…'`) for 8 h with no further authentication.
- **The ORC working directory is NOT a git repo.** `~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private/` is a plain copy with no `.git`, so `git pull` on the remote will fail. Sync the latest code from the local clone with `rsync -az --delete --exclude='.git' --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='hpc/runs' --exclude='benchmarks/results' --exclude='benchmarks/figures' ./ orc:fsl_groups/fslg_vcl/compute/digital-alloy-lab-private/` before invoking `bash hpc/bofn_benchmark/submit.sh`. **`--exclude='.venv'` is mandatory** — the agent clone has no `.venv`, so without the exclude `rsync --delete` silently wipes every file inside the remote `.venv` (leaving only empty directory shells like `.venv/lib/python3.11/site-packages/`), which then makes `run_cell.slurm` fall back to `module load python/3.11` (no torch) and every cell fails immediately with `ModuleNotFoundError: No module named 'torch'`. For this group's setup (`fslg_vcl`), `~/fsl_groups/fslg_vcl/compute/` is a regular directory on the user's HOME filesystem (`/home/$USER/...` on `vip-ib.vast.rc.byu.edu`, 2 TB quota, daily backup + snapshots, **no auto-deletion** per [rc.byu.edu/wiki/?id=Storage](https://rc.byu.edu/wiki/?id=Storage)) — **not** the standard `/lustre/scratch/...` symlink that would be subject to the 12-week scratch purge. So venv loss here is always our own rsync wiping it, never an ORC-side purge. After such a wipe, rebuild with `ssh orc 'bash -lc "cd ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private && rm -rf .venv && bash hpc/bofn_benchmark/setup_env.sh"'` (~5 min).
- ORC's non-interactive SSH shell does **not** include `sbatch` / `module` / Conda / TC-Python / etc. on `PATH` — those are only set up by `~/.bash_profile` (login shell). **Always wrap remote commands with `bash -lc "…"`** (login shell) so SLURM, the module system, and any user-installed tooling load. For example: `ssh orc "bash -lc \"cd … && bash hpc/bofn_benchmark/submit.sh\""`. Without `-lc`, `submit.sh` falls into its "no `sbatch`" branch and tries to re-exec via SSH back to itself, failing with "no master SSH socket"; `module load python/3.11` will likewise fail with "module: command not found". This applies to every `ssh orc '…'`, `ssh orc bash`, `bash hpc/run_remote.sh '…'` invocation — it is a property of the SSH session, not of any one script. (The persistent `ControlMaster` socket multiplexes the *connection*, not the shell type, so each `ssh orc '…'` still spawns a fresh non-login shell unless you ask for a login shell explicitly.)
- Always redact `$BYU_HPC_PASSWORD` from any captured SSH output before reading it back into the agent context: pipe through `sed "s|${BYU_HPC_PASSWORD}|<REDACTED>|g"`. If a transcript ever does capture the password, `shred -u` (or `rm -f`) the file immediately.
- If you ever need to verify the secret is present, check `[ -n "${BYU_HPC_PASSWORD:-}" ]` — never print its contents or length.

## Thermo-Calc on ORC

Thermo-Calc (2024a, with TC-Python 2024.1) is installed by Xavier in the **`grp_vertical_cloud_lab` group home**, not under `fslg_vcl`. You must be on an ORC account that is a member of `grp_vertical_cloud_lab` to see it — check with `groups`. The previous `fslg_vcl`-only account could not find Thermo-Calc; that was an account/group issue, not a missing install.

- **Install path / env setup:** `/grphome/grp_vertical_cloud_lab/software/Thermo-Calc`. A setup script at `/grphome/grp_vertical_cloud_lab/thermo-calc_setup.sh` exports the needed variables. The essentials are:
  - `export TC24A_HOME=/grphome/grp_vertical_cloud_lab/software/Thermo-Calc`
  - `export LSHOST=linuxlic4.et.byu.edu` (Sentinel RMS license server, **port 5093** — *not* FlexLM/27000)
  - The conda env with TC-Python lives at `/grphome/grp_vertical_cloud_lab/.conda/envs/thermo-calc_env`.
- **`mamba activate thermo-calc_env` does NOT work** from a normal account: mamba/conda looks in the user's own `~/.conda/envs/`, not the group prefix, so activation fails. **Workaround: call the env's Python by full path** instead of activating:
  - `/grphome/grp_vertical_cloud_lab/.conda/envs/thermo-calc_env/bin/python your_script.py`
- **Login-node use works fully.** With `TC24A_HOME` + `LSHOST` set and the full-path Python, all TC-Python workflows run on the login node: single equilibrium, Scheil, PRISMA precipitation, and multi-component (e.g. quaternary Al-Mn-Cr-Zr) screens. Key databases present: **TCAL8** (Al thermo), **MOBAL7** (Al mobility), **MOBFE7/MOBFE8** (20 databases total). Note the Al₃Zr phase label in TCAL8 is `AL3ZR_D023` (D0₂₃), and the Al thermo database is TCAL8 (not TCAL10).
- **Compute-node (SLURM) use currently HANGS — known unresolved blocker.** A `TCPython()` startup inside an `sbatch`/`srun` job hangs for minutes at the py4j Java↔Python gateway handshake, then dies with `java.lang.reflect.UndeclaredThrowableException` (empty message). Diagnosis so far:
  - It is **not** a license problem: `license-diagnostics-linux.exe` retrieves all 9 features and TCP 5093 to `linuxlic4` is reachable from compute nodes (verified on `m8-*`).
  - The JavaEntryPoint correctly advertises `address=127.0.0.1` on both login and compute nodes, and plain loopback TCP (127.0.0.1, localhost, ::1) self-connect works on compute nodes — so the advertised address is not the cause.
  - A `kill -3` thread dump shows the Java side blocked in `JavaEntryPoint.main` (`BufferedReader.readLine()` on stdin) with a `ServerSocket.accept()` thread waiting — i.e. the Python client never completes the gateway connection. `-Djava.net.preferIPv4Stack=true` / `preferIPv4Addresses=true` did **not** fix it; `LSPROTOCOL=TCP` did not either.
  - Note: on compute nodes `getent hosts $(hostname)` returns a **link-local IPv6** (`fe80::…`) and `localhost` resolves to `::1` first; this remains the leading (unconfirmed) suspect for the handshake hang. `jstack`/`gdb` are unusable because **ptrace is disabled** on ORC nodes — use `kill -3` for JVM thread dumps.
  - **Until this is resolved, run Thermo-Calc/TC-Python on the login node**, or escalate the compute-node networking issue to ORC support. Use `/nobackup/autodelete/grp/grp_vertical_cloud_lab/` for job working directories (group compute/scratch, mounted on compute nodes; the group home is backed up but the `/nobackup` space is not).
