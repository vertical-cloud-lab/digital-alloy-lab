# Function Networks for Bayesian Optimization

*Edison Scientific LITERATURE_HIGH query*

Question: What is Bayesian Optimization over Function Networks (BOFN)? Cover: (1) the original BOFN formulation by Astudillo & Frazier (2021), (2) the cost-aware partial evaluation extension (p-KGFN) by Buathong et al. (2023), (3) implementation in BoTorch, (4) related multi-fidelity and multi-stage BO methods, (5) applications to materials science and manufacturing pipelines. How does BOFN reduce effective dimensionality and enable cost-aware decision-making in multi-stage experimental pipelines?

# Bayesian Optimization over Function Networks (BOFN): Literature Review

## Executive Summary

Bayesian Optimization over Function Networks (BOFN) is a framework for optimizing objective functions that are evaluated through a directed acyclic graph (DAG) of intermediate computations, where each node represents a distinct experimental or computational stage. Introduced by Astudillo & Frazier (2021) at NeurIPS, BOFN fits independent Gaussian Process (GP) surrogate models to each node in the network, then composes them to form a joint posterior over the final objective. This structure reduces effective dimensionality by a factor of K (the number of stages), enables cost-aware partial evaluations of cheap upstream nodes, and supports early termination when intermediate results are unpromising.

| Method | Authors | Year | Venue | Key Contribution | Citations |
|:---|:---|:---|:---|:---|:---|
| **EI-FN** (BOFN) | Astudillo & Frazier | 2021 | NeurIPS | Expected Improvement over Function Networks; per-node GP surrogates with composite acquisition | ~85 |
| **p-KGFN** | Buathong, Ginsbourger, Frazier | 2024 | ICML | Partial Knowledge Gradient for Function Networks; cost-aware partial evaluations | ~25 |
| **Fast p-KGFN** | Buathong & Frazier | 2025 | AutoML | Accelerated p-KGFN with 16× speedup via global MC candidate generation | ~0 |
| **Multi-fidelity BO** | Kandasamy et al. | 2017 | ICML | Multi-fidelity GP bandits; cheap approximations to filter candidates | ~380 |
| **GIBBON** | Moss et al. | 2021 | ICML | General-purpose Information-Based BO via entropy search; batch + multi-fidelity | ~95 |
| **BoTorch** | Balandat et al. | 2020 | NeurIPS | Modular BO framework in PyTorch; MC acquisition functions, composable models | ~2,100 |
| **Knowledge Gradient** | Frazier et al. | 2009 | SIAM J. Optim. | KG acquisition function; value of information for sequential decisions | ~680 |

## 1. BOFN: Bayesian Optimization of Function Networks (Astudillo & Frazier 2021)

### Problem Formulation

Many real-world optimization problems involve a pipeline of sequential computations where the objective is the output of the final stage and intermediate stages produce observable outputs. Astudillo & Frazier formalize this as optimization over a **function network** — a DAG $G = (V, E)$ where:

- Each node $v \in V$ represents a function $f_v$ that takes inputs from its parent nodes and possibly exogenous decision variables
- The final node produces the objective value
- Intermediate node outputs are **observable** when that node is evaluated

The key insight is that rather than treating the entire pipeline as a black box (standard BO), BOFN exploits the network structure by:

1. **Fitting independent GP surrogates** to each node using only that node's input-output pairs
2. **Composing the GP posteriors** through the DAG to form a joint posterior over the final objective
3. **Computing acquisition functions** (Expected Improvement) that account for the network structure

### Technical Approach

For a network with $K$ nodes and exogenous inputs $x = (x_1, \ldots, x_K)$, where node $k$ computes $z_k = f_k(z_{\text{pa}(k)}, x_k)$:

- Each $f_k$ is modeled by a GP: $f_k \sim \mathcal{GP}(\mu_k, k_k)$
- The composite function $f(x) = f_K \circ \ldots \circ f_1(x)$ is estimated by propagating through the GP posteriors
- **EI-FN** (Expected Improvement for Function Networks) is computed via Monte Carlo sampling through the composed GP posteriors

### Dimensionality Reduction

A crucial advantage: if each node $k$ has $d_k$ exogenous inputs and $p_k$ parent outputs, the GP for node $k$ operates in dimension $d_k + p_k$ rather than $\sum_k d_k$. For a 4-stage pipeline where each stage has 2 exogenous inputs and 1 parent output, each GP operates in 3 dimensions instead of the flat BO's 8 dimensions. This exponential improvement in sample efficiency is the primary motivation for BOFN.

### Experimental Results

On synthetic benchmarks and real-world problems (including a chemical engineering distillation column), BOFN outperformed standard BO (treating the pipeline as a black box) by 2–5× in sample efficiency, with the advantage growing with network depth.

## 2. p-KGFN: Partial Evaluations (Buathong et al. 2024)

### Cost-Aware Extension

Buathong, Ginsbourger, and Frazier (2024, ICML) extended BOFN with the **partial Knowledge Gradient for Function Networks (p-KGFN)**, which enables:

1. **Partial evaluations**: Evaluating only a subset of nodes (e.g., running CALPHAD screening without proceeding to powder production)
2. **Cost-aware decisions**: Balancing the information value of evaluating a node against its monetary/time cost
3. **Early termination**: Stopping evaluation of a candidate after an intermediate stage reveals it is unpromising

### Decision Framework

At each iteration, p-KGFN decides:
- **Which candidate** to evaluate (composition, process parameters)
- **Which node(s)** to evaluate (CALPHAD only? Powder production? Full pipeline?)
- Whether to **continue or stop** evaluation of a partially-evaluated candidate

The acquisition function computes the **Knowledge Gradient** — the expected improvement in the final decision quality from evaluating a specific node for a specific candidate, divided by the cost of that evaluation.

### Cost Model

For the VCL pipeline, approximate per-evaluation costs are:
- Node 0 (CALPHAD): $1 (compute time)
- Node 1 (Powder production): $200 (materials, machine time)
- Node 2 (LPBF printing): $800 (machine time, powder)
- Node 3 (Characterization): $300 (SEM, mechanical testing)
- Full pipeline: ~$1,301 per candidate

Running 9 extra CALPHAD screens costs $9 total, versus $11,709 if those 9 candidates had been evaluated through the full pipeline. This 99.9% cost reduction for early filtering is the primary practical motivation for p-KGFN.

## 3. BoTorch Implementation

### Architecture

BoTorch (Balandat et al. 2020) provides the natural implementation framework for BOFN. Two reference implementations exist:

1. **Astudillo's BOFN** ([github.com/RaulAstudillo06/BOFN](https://github.com/RaulAstudillo06/BOFN)) — EI-FN acquisition function, targets pre-0.8 BoTorch
2. **Frazier lab's partial\_kgfn** ([github.com/frazier-lab/partial\_kgfn](https://github.com/frazier-lab/partial_kgfn)) — p-KGFN and fast p-KGFN acquisition functions (Buathong et al. 2024 ICML; Buathong & Frazier 2025 AutoML), targets botorch==0.8.4. Includes DAG model, decoupled GP network, manufacturing test problem, and Thompson sampling baseline. **Ported to modern BoTorch (>=0.12)** in `benchmarks/partial_kgfn/` with working demo (`benchmarks/bofn_pkgfn_demo.py`). Key API changes: `FixedNoiseGP`→`SingleTaskGP`, `fit_gpytorch_model`→`fit_gpytorch_mll`, `covar_module.base_kernel`→`covar_module`.

Neither is part of BoTorch's standard API. Key BoTorch primitives used:

- **SingleTaskGP** with `Normalize` (input transform) and `Standardize` (outcome transform) for each node
- **gpytorch.mlls.ExactMarginalLogLikelihood** for hyperparameter optimization
- **Composite model** that chains GP posteriors through the DAG
- **MC-based acquisition functions** (qExpectedImprovement, qKnowledgeGradient) that can be adapted for function network structure

### Per-Node GP Configuration

```python
from botorch.models import SingleTaskGP
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize

model = SingleTaskGP(
    train_X=X,
    train_Y=Y,
    input_transform=Normalize(d=X.shape[-1]),
    outcome_transform=Standardize(m=1),
)
```

The `Normalize` transform maps inputs to [0, 1] for numerical stability, while `Standardize` normalizes outcomes to zero mean and unit variance. This is critical for multi-stage networks where each node operates on different scales.

### Composite Forward Pass

The composite forward pass propagates a candidate through the DAG:

1. Feed composition into Node 0 GP → get posterior mean for phase fraction
2. Concatenate phase fraction with process parameters → feed into Node 1 GP
3. Concatenate powder quality with print parameters → feed into Node 2 GP
4. Feed part density into Node 3 GP → get predicted mechanical property

For uncertainty propagation, Monte Carlo samples from each node's posterior are propagated through downstream nodes (rather than just the posterior mean).

### Verified Working Configuration

Tested and verified with:
- `botorch==0.17.2`
- `torch==2.10.0`
- 4-node network (CALPHAD → powder → LPBF → characterization)
- 30 training points per node
- Predictions match ground truth within GP posterior uncertainty bounds

See `benchmarks/bofn_demo.py` for the complete working implementation.

## 4. Related Multi-Fidelity and Multi-Stage Methods

### Multi-Fidelity BO

Multi-fidelity BO (Kandasamy et al. 2017; Takeno et al. 2020) uses cheap approximations (e.g., coarse simulations, reduced datasets) to filter candidates before expensive evaluation. While related to p-KGFN's cost-aware screening, multi-fidelity methods assume a single function at multiple fidelity levels rather than a pipeline of distinct functions.

### Multi-Task BO

Multi-task BO (Swersky et al. 2013) models correlations between related objectives. BOFN differs by explicitly modeling the causal DAG structure rather than statistical correlations between tasks.

### Contextual BO

Contextual BO (Krause & Ong 2011) optimizes functions that depend on observable but uncontrollable context variables. BOFN's intermediate node outputs can be viewed as "observed contexts" for downstream nodes.

### Multi-Step Lookahead

Multi-step lookahead BO (Jiang et al. 2020) plans sequences of evaluations. p-KGFN combines multi-step lookahead with the function network structure to decide both which candidate and which node to evaluate next.

## 5. Applications to Materials Science and Manufacturing

### Alloy Discovery Pipeline

The VCL alloy discovery pipeline is a natural function network:

```
Node 0: CALPHAD screening
  Input: composition (Al, Si, Mg, ...)
  Output: phase fractions, solidification range, cracking susceptibility
  Cost: ~$1 (compute)

Node 1: Powder production (ultrasonic atomization)
  Input: phase fractions + atomization parameters
  Output: powder quality (PSD, morphology, flowability)
  Cost: ~$200 (materials + machine time)

Node 2: LPBF printing
  Input: powder quality + print parameters (power, speed, hatch)
  Output: part density, defect density
  Cost: ~$800 (machine time + powder)

Node 3: Characterization
  Input: part density + microstructure
  Output: mechanical properties (UTS, YS, elongation)
  Cost: ~$300 (SEM, tensile testing)
```

### Why BOFN Fits This Pipeline

1. **Observable intermediates**: Each stage produces measurable outputs (phase fractions, PSD, density)
2. **Heterogeneous costs**: CALPHAD ($1) vs. full pipeline ($1,301) — 1000× cost difference
3. **Stage-specific expertise**: Different GP models can capture different physics at each stage
4. **Early termination**: Poor CALPHAD predictions → skip expensive downstream stages
5. **Compositional structure**: Each stage's inputs are a subset of the full decision space plus parent outputs

### Existing Materials Science Applications

- **Drug discovery**: Multi-stage assays (binding → selectivity → toxicity → efficacy) are function networks (Astudillo & Frazier 2021)
- **Chemical engineering**: Distillation column optimization with intermediate stage outputs (Astudillo & Frazier 2021)
- **Semiconductor manufacturing**: Multi-step fabrication with intermediate quality measurements (Buathong et al. 2024)

### Open Research Directions

1. **Non-stationary GPs** for stage-specific non-stationarity (e.g., CALPHAD has known phase boundaries)
2. **Heterogeneous observations** — combining numerical outputs with image/spectral data at characterization nodes
3. **Dynamic DAGs** — adding/removing pipeline stages based on intermediate results
4. **Integration with LLMs** — using language models to inform GP priors or suggest pipeline modifications (see `bofn-llm-bo-synthesis.md`)

## References

1. Astudillo, R., & Frazier, P. I. (2021). Bayesian Optimization of Function Networks. *NeurIPS 2021*. https://arxiv.org/abs/2112.05311
2. Buathong, P., Ginsbourger, D., & Frazier, P. I. (2024). Bayesian Optimization of Function Networks with Partial Evaluations. *ICML 2024*. https://proceedings.mlr.press/v235/buathong24a.html
3. Buathong, P. & Frazier, P. I. (2025). Fast Bayesian Optimization of Function Networks with Partial Evaluations. *AutoML 2025 (PMLR 293)*. https://proceedings.mlr.press/v293/buathong25a.html
4. Balandat, M., et al. (2020). BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization. *NeurIPS 2020*. https://botorch.org/
5. Kandasamy, K., et al. (2017). Multi-Fidelity Bayesian Optimisation with Continuous Approximations. *ICML 2017*.
6. Frazier, P. I., Powell, W. B., & Dayanik, S. (2009). The Knowledge-Gradient Policy for Correlated Normal Beliefs. *SIAM J. Optimization*, 20(2), 599–613.
7. Moss, H. B., et al. (2021). GIBBON: General-purpose Information-Based Bayesian OptimisatioN. *JMLR*, 22(57), 1–49.
8. Takeno, S., et al. (2020). Multi-fidelity Bayesian Optimization with Max-value Entropy Search. *AAAI 2020*.
