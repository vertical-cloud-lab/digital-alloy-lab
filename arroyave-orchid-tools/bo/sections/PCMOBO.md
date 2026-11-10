## PCMOBO

**What it is.** `pcmbo` 0.1.0: constrained multi-objective BO with *portfolio-based acquisition switching* (fixed
BoTorch policies qLogPoF / qLogEHVI / qLogNParEGO / qUCB, or pEHVI/PoF on finite pools, chosen per iteration by a
bandit-UCB rule or by an LLM "arbiter" through LangGraph + OpenAI). Ships synthetic benchmarks (constrained
Branin-Currin, C2-DTLZ2, disc brake) and two finite-pool materials case studies: a 40,553-alloy Nb-Mo-Ta-V-W-Cr HEA
design space (max solidus, yield strength, Pugh ratio; min density; BCC screen) and a 3,138-candidate thermoelectric pool.
Three console entry points; no test suite, but the README gives CPU smoke commands.

**Commands** (scripts: `scripts/PCMOBO-smoke.sh`, `scripts/PCMOBO-hea-compare.sh` (seed 2 rerun: same command with `--seeds 2`), `scripts/PCMOBO-plot.py`)

```bash
cp -r /tmp/arroyave/src/ArroyaveLab__PCMOBO /tmp/arroyave/work/pcmobo
/tmp/sbx/clean uv venv --python 3.12 /tmp/arroyave/venvs/pcmobo
/tmp/sbx/clean uv pip install --python /tmp/arroyave/venvs/pcmobo/bin/python --torch-backend cpu -e "/tmp/arroyave/work/pcmobo[dev]"
# README smoke runs verbatim (1 iteration each)
pcmbo-synthetic --benchmark constrained_branin_currin --policy qlogpof --seeds 1 --iterations 1 --n-init 8 --workers 1 --device cpu --acq-mc-samples 16 --acq-raw-samples 16 --acq-num-restarts 1 --results-dir runs/synthetic/smoke
pcmbo-hea  --policy pof     --seeds 1 --iterations 1 --n-init 2 ... --acq-batch-eval-size 128 --results-dir runs/hea_design/smoke
pcmbo-estm --policy qlogpof --seeds 1 --iterations 1 --n-init 3 ... --acq-batch-eval-size 128 --results-dir runs/estm_thermoelectric/smoke
# scaled-up HEA comparison: 10 initial + 15 iterations, 1 seed, 32 MC/raw samples, for pof, pehvi, bandit_ucb_switch
pcmbo-hea --policy <pol> --seeds 1 --iterations 15 --n-init 10 --workers 1 --device cpu --acq-mc-samples 32 --acq-raw-samples 32 --acq-num-restarts 1 --acq-batch-eval-size 512
```

**Outcome: PASS.** Install and all three README smoke runs succeed on CPU; the scaled HEA campaign runs for two fixed
policies and the bandit switcher. The `llm_switch` policy was not run (needs an OpenAI key; out of scope here).

| Step | Result | Wall time |
|---|---|---|
| install (torch 2.15.0+cpu, botorch 0.18.1, gpytorch 1.15.2, langchain 1.4.9, langgraph 1.2.20) | OK | 2 s (cache warm) |
| `pcmbo-synthetic --help` | OK | 2 s |
| smoke synthetic (constrained Branin-Currin, qLogPoF) | OK: 6 feasible, HV 316.6 after 1 iteration | 45 s |
| smoke HEA (PoF, n-init 2) | OK (`InputDataWarning ... std = tensor([0.])`: both initial points share the label) | 4 s |
| smoke thermoelectric (qLogPoF, n-init 3) | OK, 0 feasible after 1 iteration | 36 s |
| HEA 10 + 15 iterations: PoF / pEHVI / bandit-UCB switch | OK / OK / OK | 49 s / 41 s / 71 s |

**Key numbers** (HEA pool, seeds 1 and 2, `figures/PCMOBO-hea-feasible.png`, `data/PCMOBO-hea-campaigns.csv`).
Cumulative feasible alloys after 15 iterations:

| Policy | Seed 1 | Seed 2 | Notes |
|---|---|---|---|
| PoF | **12** | **14** | |
| bandit-UCB switch | **8** | **8** | same arm mix in both seeds: PoF 9, pEHVI 2, qLogNParEGO 2, qUCB 2; it tries every arm before exploiting |
| pEHVI | **0** | **0** | |

The feasible region is very small, so feasibility-first acquisition dominates and the bandit learns to favour it, at the
cost of its warm-start exploration. The logged scaled hypervolume stays near 1e-5 because so few feasible points exist.
The seed-2 reruns took 34 s, 37 s and 59 s.

**Problems found**
1. Namespace pollution: `pyproject.toml` installs generic top-level modules `core`, `paths`, `cli`, `engine`, `policy`,
   `benchmarks`, `acq`, `studies`, `llm_runtime` into site-packages; these can shadow or be shadowed by other packages
   (we kept it in its own venv for that reason).
2. `langchain`, `langchain-openai` and `langgraph` are hard dependencies even though only `llm_switch` uses them.
3. Torch is not declared directly (pulled via botorch), so a plain `pip install -e .` fetches the default CUDA wheel on
   Linux; use `--torch-backend cpu` or the CPU index.
4. README smoke HEA run uses `--n-init 2`, which gives a constant training label: `InputDataWarning: Data (outcome observations)
   is not standardized (std = tensor([0.], dtype=torch.float64), mean = tensor([1.], dtype=torch.float64))`.
5. `--seeds` defaults to `"1-5"`, so forgetting the flag runs five campaigns.
6. Cosmetic: `FutureWarning: torch.jit.script is deprecated` on torch 2.15.

**Relevance to us: high.** The policy-switching layer (bandit over qLogPoF/qLogEHVI/qLogNParEGO/qUCB) and the
finite-pool constrained MOBO runners are clean modern BoTorch code that could wrap our Al-alloy composition x LPBF
process candidate pools, with printability/cracking as constraints. It is single-fidelity, mostly q = 1 on the
pool studies, and has no cost or supply-risk weighting, so we would bolt on a cost-aware arm (e.g. the rhea-mobo
`CostAwareEHVI` idea) or a BOFN model.

TABLE: PCMOBO | OK (CPU torch; pulls langchain/langgraph; generic top-level module names) | 3 README smokes + HEA 10+15 for PoF, pEHVI, bandit switch | PASS (llm_switch not run, needs OpenAI key) | HEA feasible found in 15 iters (seeds 1/2): PoF 12/14, bandit 8/8, pEHVI 0/0
