If using Edison Scientific, you may need to wait up until 10 minutes to get the response. If you're an agent, sleep for 10 minutes (to avoid consuming requests unecessarily), and then every 5 minutes after that. Start with a 15 minute wait if using high effort literature query type. If you need to upload files, use analysis query type. See the docs: https://edisonscientific.gitbook.io/edison-cookbook/edison-client. Here is the endpoint you should use: https://api.platform.edisonscientific.com. The API key is EDISON_PLATFORM_API_KEY. Don't expose this secret, e.g., by echoing or grepping it. Pass the API key in explicitly:

```
from edison_client import EdisonClient, JobNames
client = EdisonClient(api_key=EDISON_PLATFORM_API_KEY)
```

If using Edison Analysis, refer to https://docs.edisonscientific.com/edison-client/file-management#upload for instructions on how to upload files. If able to use Context7, to better inform use of EdisonClient, see https://context7.com/future-house/edison-client-docs/llms.txt?tokens=10000

## LaTeX Proposal Build

There is a single source file: `genesis-mission-proposal/flaime-genesis-proposal.tex`. Do NOT create a separate `-clean.tex` copy. Use the Makefile:

- `make draft` — annotated PDF with DRAFT watermark and todonotes (all sections)
- `make clean-pdf` — clean PDF (no watermark, no notes, all sections still present)
- `make final` — submission-ready Field 8 PDF (also removes abstract, biosketch, budget)
- `make all` — all three

Build toggles are controlled at build time via `\def\cleanbuild{}` and `\def\submissionbuild{}`; do not manually edit `\drafttrue`/`\draftfalse` or `\submissiontrue`/`\submissionfalse`.

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
