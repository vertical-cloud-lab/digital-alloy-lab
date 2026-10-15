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
- The 2FA verification code is provided by the operator via the tracked file `hpc/tmp/totp.txt` (updated best-effort during the session). Fresh-session workflow: (1) recreate `~/.ssh/config` from `hpc/ssh_config.example`, substituting `$BYU_HPC_USERNAME`; (2) start `python hpc/agent_connect.py --host orc` in an **async** bash session so it blocks at the `6-digit verification code:` prompt; (3) **only then** `git pull` and `tr -d '[:space:]' < hpc/tmp/totp.txt` to read the current code; (4) `write_bash` the 6 digits into the async session immediately. TOTPs expire every ~30 s, so reading the file must happen after the prompt appears, not before. If `agent_connect` reports "2FA code was rejected (likely expired)", do **not** retry the same code — poll `hpc/tmp/totp.txt` (via repeated `git pull`) until the committed value **differs** from the rejected one, then reopen `agent_connect` and inject the new code.
- If you ever need to verify the secret is present, check `[ -n "${BYU_HPC_PASSWORD:-}" ]` — never print its contents or length.
- The `ControlMaster` socket (`ControlPath ~/.ssh/master-%r@%h:%p.socket`, `ControlPersist 8h`) is persisted on disk at `~/.ssh/master-<user>@ssh.rc.byu.edu:22.socket`. Once `agent_connect.py` succeeds, **do not reconnect** for subsequent commands. Every later `ssh orc ...`, `scp ... orc:...`, and `rsync ... orc:...` in the same runner home will reuse that socket (confirm with `ssh -O check orc` → "Master running"). If a later call returns `Permission denied (keyboard-interactive)`, that means the socket is genuinely gone (e.g. new runner, socket file deleted, or server-side idle timeout) — only then reopen `agent_connect`. Treat spurious reconnects as a bug: `ssh -v orc 'echo hi' 2>&1 | grep -E "(auto-mux|Permission)"` will show `auto-mux: Trying existing master` when multiplexing is actually working.

### Running commands on ORC login nodes

- Non-interactive `ssh orc '...'` **does not source `/etc/profile`**, so `module`, `sbatch`, `squeue`, `srun`, and the Lmod init are all missing from `PATH`. Always invoke remote work through a login shell: `ssh orc 'bash -l -c "..."'` (or start scripts with `#!/usr/bin/env bash -l`). The Lmod init path is `/apps/lmod/lmod/init/`; `sbatch` lives at `/apps/slurm/latest/bin/sbatch`. See <https://rc.byu.edu/wiki/?id=Environment+Modules>.
- Available Lmod module families that matter here: `python/3.11`, `python/3.12` (default), `miniforge3/25.3.1-0` (mamba/conda — BYU's recommended path for PyTorch per <https://rc.byu.edu/wiki/?page=PyTorch>), and `cuda` (GPU jobs only — see <https://rc.byu.edu/wiki/?page=Getting+Started+with+GPUs>). Some modules (e.g. `cudnn`) live behind a hierarchy and only `module avail` after a parent module (`cuda`) is loaded.
- `hpc/bofn_benchmark/setup_env.sh` and `run_cell.slurm` default to `module load python/3.11` + `pip install -r requirements.txt`. That works but installs the default (CUDA) PyTorch wheel, which is large and warns about driver mismatch on login nodes. The benchmark runs CPU-only (SLURM cells request no GPU), so the warning is benign. If you want to follow BYU's recommended path exactly, switch to `miniforge3` + `mamba install pytorch=<ver>=cpu_mkl_py311_<hash>` per the wiki; do not change the existing flow without a reason.
- If `import torch` fails with `libtorch_global_deps.so: cannot open shared object file`, the pip install was interrupted or NFS ate a file — `pip install --force-reinstall --no-cache-dir torch` inside the existing `.venv` is the fastest fix. Do not `rm -rf .venv` first; a force-reinstall is enough and saves ~10 min of other deps.
- ORC cannot `git clone` this **private** repo: the login node has no GitHub credentials and its `~/.ssh/id_rsa` is not registered as a deploy key. Deploying the repo from the agent runner: `git archive --format=tar HEAD -o /tmp/repo.tar && scp /tmp/repo.tar orc:<remote>/repo.tar && ssh orc 'cd <remote> && tar xf repo.tar && rm repo.tar'`. Do **not** try to fix this by editing `~/.ssh/authorized_keys` or publishing keys — coordinate with the operator instead.
- Remote repo root convention: `~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private`.
- BOFN benchmark wall-clock: only **pKGFN** needs the long default (≥6h, 12h is safe); every other algorithm (Random, Sobol, LowFidOnly, Node2Only, HighFidOnly, TSFN) finishes in well under an hour. Split the sweep: the 6 non-pKGFN algos with `CELL_TIME=01:00:00`, pKGFN alone with `CELL_TIME=12:00:00`. Each `submit.sh` invocation creates its own array+combine pair, so two sweeps = two combine jobs.
