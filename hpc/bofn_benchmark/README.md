# BOFN benchmark on BYU ORC (SLURM)

SLURM-native equivalent of the GitHub Actions workflow in
`.github/workflows/bofn_benchmark.yaml` (PR #14). Submits the
`benchmarks/bofn_actions_benchmark.py` sweep — `(algo × seed)` matrix → combine
— to BYU's Office of Research Computing (ORC, "RC") instead of GitHub-hosted
runners, using SLURM job arrays + `--dependency=afterany:` to chain the
combine step.

## Why move it off GitHub Actions

- **No 360-min wall-clock cap.** GH-Actions kills any single job at 6 h.
  pKGFN with `n_fantasies=64, n_raw=128` reliably brushes that cap on hosted
  runners (see PR #14, commit `47e8968`); ORC nodes can run the same cell
  for 24 h+ on a partition that allows it.
- **Bigger boxes.** GH-Actions runners are 4 vCPU / 16 GB. ORC nodes routinely
  have 32–128 cores and ≥256 GB; pKGFN inner KG can vectorise across many
  more fantasies.
- **No artifact size limits.** Hosted-runner artifact upload caps at 10 GB
  per artifact; on ORC results just live on group storage.
- **GPU-ready.** Switching to a GPU partition is a one-line change (`PARTITION=gpu`)
  whereas GH-Actions has no first-class GPU runners on the free tier.

## Architecture mirror

```
GitHub Actions (.github/workflows/bofn_benchmark.yaml):
    smoke-test  →  full-test (matrix: algo × seed)  →  combine-results
                       (one runner per cell)               (if: always() && ...)

BYU ORC (this directory):
    [optional] smoke run on a single cell on a login node OR --array=1-1
        ↓
    sbatch --array=1-N run_cell.slurm     (one SLURM task per cell)
        ↓
    sbatch --dependency=afterany:$JID combine.slurm
                                  ^^^^^^^^
                       afterany ⇔ if: always() && (success || failure)
```

`afterany` runs the combine job once *every* array task has terminated,
regardless of exit code. This gives the same partial-plot behaviour as the
GH-Actions workflow's `if: always() && (needs.full-test.result == 'success'
|| needs.full-test.result == 'failure')`. Use `afterok:` instead if you'd
rather skip the plot when any cell failed.

## Files

| File | Role |
| ---- | ---- |
| [`submit.sh`](submit.sh) | Builds a manifest of `(algo, seed)` cells, `sbatch`'s the array job, then `sbatch`'s the combine job with `--dependency=afterany:`. Idempotent — pass `RUN_ID` to label / re-run. Auto-tunnels through the existing master SSH socket if invoked from a workstation. |
| [`run_cell.slurm`](run_cell.slurm) | Single-cell SLURM script. Reads its `(algo, seed)` from `manifest.txt` keyed by `$SLURM_ARRAY_TASK_ID`; writes one JSON to `benchmarks/results/actions_hpc/<RUN_ID>/`. |
| [`combine.slurm`](combine.slurm) | Aggregates every per-cell JSON into the combined cost-efficiency plot + summary CSV in `benchmarks/figures/actions_hpc/<RUN_ID>/`. |
| [`setup_env.sh`](setup_env.sh) | One-time per-account setup: creates `$REPO_DIR/.venv` and `pip install -r requirements.txt` (which now includes `pexpect>=4.9` and the BoTorch / GPyTorch / Torch stack). |
| [`fetch_results.sh`](fetch_results.sh) | `rsync` the per-cell JSONs, combined plots, manifest, and SLURM logs back from ORC into the local repo tree. Resolves `RUN_ID=latest` via `ls -1t`. |

## End-to-end workflow

### One-time, per ORC account

```bash
# 1. Open the master SSH socket (HITL 2FA — see ../README.md).
bash hpc/connect.sh

# 2. Clone the repo onto ORC group storage. Done once per account.
ssh orc 'mkdir -p ~/fsl_groups/fslg_vcl/compute && cd ~/fsl_groups/fslg_vcl/compute \
         && git clone https://github.com/vertical-cloud-lab/digital-alloy-lab-private.git'

# 3. Build the shared Python venv.
ssh orc 'cd ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private \
         && bash hpc/bofn_benchmark/setup_env.sh'
```

### Per sweep

```bash
# 1. Sync the latest commit to ORC.
ssh orc 'cd ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private && git pull'

# 2. Submit. submit.sh detects whether you're on ORC or your workstation:
#    - From your workstation: it re-execs itself over the master SSH socket.
#    - From an ORC login node: it sbatches directly.
RUN_ID=demo-$(date +%Y%m%dT%H%M%SZ) \
ALGOS='Random Sobol pKGFN' \
SEEDS='0 1 2' \
bash hpc/bofn_benchmark/submit.sh

# 3. (Optional) monitor.
ssh orc 'squeue -u $USER'
ssh orc 'tail -f ~/fsl_groups/fslg_vcl/compute/digital-alloy-lab-private/hpc/runs/<RUN_ID>/logs/cell-1.out'

# 4. Once the combine job finishes, pull everything back.
RUN_ID=<RUN_ID> bash hpc/bofn_benchmark/fetch_results.sh
#   - benchmarks/results/actions_hpc/<RUN_ID>/*.json
#   - benchmarks/figures/actions_hpc/<RUN_ID>/bofn_actions_cost_efficiency.png + summary
#   - hpc/runs/<RUN_ID>/{manifest.txt, submission.env, logs/}
```

The full default sweep (7 algos × 20 seeds = **140 cells**) submits in one
`sbatch --array=1-140`; the combine job sits in the queue with
`Reason=Dependency` until every cell finishes.

## Tuning knobs (env vars on `submit.sh`)

| Var | Default | Notes |
| --- | ------- | ----- |
| `ALGOS` | `Random Sobol LowFidOnly Node2Only HighFidOnly TSFN pKGFN` | Same set as the GH-Actions matrix. |
| `SEEDS` | `0 1 2 ... 19` | 20 seeds matches PR #14's full run. |
| `CELL_TIME` | `06:00:00` | Mirrors the GH-Actions 360-min cap. Bump to e.g. `24:00:00` once you're off the hosted-runner cap. |
| `CELL_MEM` | `8G` | Per-cell. pKGFN with bigger inner KG batches needs more — try `16G` if you raise `n_fantasies`. |
| `CELL_CPUS` | `4` | BoTorch/Torch are mostly single-threaded for these problem sizes. |
| `PARTITION` | (cluster default) | Set e.g. `PARTITION=gpu` once the GPU build is wired up. |
| `PYTHON_MODULE` | `python/3.11` | Adjust to whatever `module avail python` shows on ORC. |
| `DRY_RUN` | (unset) | If non-empty, prints the `sbatch` lines instead of submitting. |

## Triggering from GitHub Actions

`.github/workflows/bofn_benchmark_hpc.yaml` exposes a `workflow_dispatch`
that opens a master SSH socket via `hpc/agent_connect.py`, then runs
`submit.sh` over it. **It is human-in-the-loop**: ORC's 2FA cannot be
satisfied from a fully-headless runner, so the workflow pauses on a
`workflow_dispatch.inputs.verification_code` field that the operator fills
in (the 6-digit TOTP code is short-lived, so dispatch the workflow and
then immediately set the input).

If you'd rather skip GH-Actions entirely, just run `submit.sh` from your
workstation — the result is identical.

## Cross-reference

- GH-Actions workflow this mirrors: `.github/workflows/bofn_benchmark.yaml` (PR #14)
- Benchmark script: `benchmarks/bofn_actions_benchmark.py`
- ORC connection toolkit: [`../README.md`](../README.md)
- BYU ORC SLURM docs: <https://rc.byu.edu/wiki/?id=SLURM+Commands>
- BYU ORC SSH multiplexing: <https://rc.byu.edu/wiki/index.php?page=SSH+Multiplexing>
