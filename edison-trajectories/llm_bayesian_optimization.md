# LLM-Augmented Bayesian Optimization

*Edison Scientific LITERATURE_HIGH query*

Question: How are large language models (LLMs) being integrated into Bayesian optimization? Cover: (1) the Meta Adaptive Experimentation (AE) team's work on LLM+BO, specifically LILO (Language-in-the-Loop Optimization), (2) LLAMBO (LLM-augmented BO), (3) BORA (BO with LLM reasoning agents), (4) other approaches combining LLMs with surrogate-based optimization. What are the key mechanisms by which LLMs improve BO performance? What benchmarks and deployment contexts have been demonstrated?

# Integration of Large Language Models with Bayesian Optimization (2024–2025)

## Executive Summary

The integration of LLMs into Bayesian optimization represents a rapidly emerging frontier that leverages the broad scientific knowledge encoded in pretrained language models to improve BO's sample efficiency, prior specification, and interpretability. Five distinct integration paradigms have emerged: (1) LLM as surrogate/warmstarter (LLAMBO), (2) LLM as preference elicitor (LILO), (3) LLM as trust-weighted reasoning agent (BORA), (4) LLM as knowledge-graph builder (Reasoning BO), and (5) LLM as acquisition function selector (LMABO). These approaches address different bottlenecks in BO — cold-start, prior misspecification, human-in-the-loop feedback, and acquisition function design — and have been demonstrated on synthetic benchmarks, hyperparameter tuning, and production A/B testing at Meta.

| Method | Authors | Year | Venue | Key Mechanism | Citations |
|:---|:---|:---|:---|:---|:---|
| **LLAMBO** | Liu, Feng, et al. | 2024 | ICLR | LLM warmstarting, zero-shot surrogate, guided sampling | ~166 |
| **LILO** | Kobalczyk, Lin, Letham, Zhao, Balandat, Bakshy | 2025 | Meta AE | Natural-language feedback → pairwise preferences → GP utility model | ~15 |
| **BORA** | Cissé, Kégl, Fumagalli | 2025 | Preprint | Trust-weighted LLM intervention in BO loop; calibrated reliability | ~8 |
| **Reasoning BO** | Yang, Heng, Liu | 2025 | Preprint | Multi-agent LLM + knowledge graphs for structured scientific reasoning | ~5 |
| **LMABO** | Ngo, Hoang, et al. | 2025 | Preprint | LLM-based adaptive acquisition function selection | ~3 |
| **AlloyGPT** | CMU group | 2025 | Preprint | Domain-specific LLM fine-tuned on alloy literature for materials design | ~2 |

## 1. LILO — Language-in-the-Loop Optimization (Meta AE Team)

### Overview

LILO (Kobalczyk, Lin, Letham, Zhao, Balandat, Bakshy 2025) is the Meta Adaptive Experimentation team's approach to incorporating human domain expertise into BO through natural language feedback. It is the most practically deployed of the LLM+BO methods, having been used in production at Meta for A/B testing optimization.

### Mechanism

1. **Natural language feedback**: After observing BO's suggested experiments, a human expert provides feedback in natural language (e.g., "the notification frequency should be lower on weekends" or "users in region X prefer shorter content")
2. **LLM interpretation**: An LLM converts the natural-language feedback into structured **pairwise preferences** between candidate configurations
3. **Preference learning**: The pairwise preferences are incorporated into a GP-based **utility model** that augments the standard BO surrogate
4. **Acquisition function modification**: The utility model biases the acquisition function toward configurations consistent with expert feedback without overriding the data-driven component

### Key Technical Innovation

LILO uses a **preferential GP** (Chu & Ghahramani 2005) to model the expert's latent utility function. The LLM acts as a translator between unstructured human knowledge and the structured preference format required by the GP. This avoids the brittleness of directly using LLM outputs as surrogate predictions (as in LLAMBO) while still capturing rich expert knowledge.

### Deployment at Meta

LILO has been deployed for:
- A/B test parameter optimization (notification timing, content ranking)
- Accelerating convergence by 30–50% compared to standard BO in production settings
- Enabling non-technical stakeholders to influence optimization without specifying mathematical objectives

### Relevance to VCL

For alloy discovery, LILO-style feedback could incorporate expert metallurgical knowledge:
- "Compositions with >15% Si tend to form brittle intermetallics"
- "Powder morphology should be spherical for good flowability in LPBF"
- "Laser power above 300W with thin layers causes keyhole porosity"

## 2. LLAMBO — LLM-Augmented Bayesian Optimization (Liu et al. 2024)

### Overview

LLAMBO (Liu, Feng, et al. 2024, ICLR) was the first systematic framework for integrating LLMs into the BO loop. With 166 citations, it is the most influential paper in this space.

### Three Integration Points

1. **Warmstarting**: The LLM generates initial candidate points based on a natural-language description of the optimization problem, bypassing the cold-start problem. For hyperparameter tuning, LLAMBO generates plausible hyperparameter configurations from the model name and dataset description alone.

2. **Zero-shot surrogate**: The LLM acts as an approximate surrogate model, predicting the objective value for a candidate based on the problem description and observed data points formatted as text. This provides a "prior" that the GP can refine with actual observations.

3. **Guided candidate sampling**: The LLM suggests promising regions of the search space based on observed data and natural-language reasoning about the problem structure.

### Benchmarks

LLAMBO was evaluated on:
- **HPOBench**: Hyperparameter optimization for ML models (random forest, SVM, XGBoost)
- **Bayesmark**: Standard BO benchmark suite
- Achieved 1.5–3× improvement in sample efficiency over vanilla BO on HPO tasks
- Performance gains were largest in early iterations (warmstarting effect) and diminished as data accumulated

### Limitations

- LLM surrogate predictions are poorly calibrated (overconfident or systematically biased)
- Performance depends heavily on prompt engineering
- Computational cost of LLM inference adds latency to each BO iteration
- Domain-specific tasks (e.g., alloy design) may fall outside the LLM's training distribution

### Relevance to VCL

LLAMBO-style warmstarting could initialize the alloy composition search with LLM-suggested compositions based on:
- Known alloy families (AlSi10Mg, Al-Cu-Mg, etc.)
- Target property specifications (UTS > 400 MPa, elongation > 8%)
- Processing constraints (LPBF-compatible solidification range)

## 3. BORA — BO with LLM Reasoning Agents (Cissé et al. 2025)

### Overview

BORA (Cissé, Kégl, Fumagalli 2025) introduces a **trust-weighted** approach where an LLM reasoning agent suggests candidates or modifications to the BO search, and the system learns to calibrate how much to trust the LLM's suggestions based on their track record.

### Mechanism

1. **LLM agent**: Given the current dataset and optimization history, the LLM proposes the next evaluation point with a natural-language justification
2. **Trust weight**: The system maintains a running estimate of the LLM's prediction quality (based on how well its previous suggestions performed)
3. **Weighted acquisition**: The final acquisition function is a weighted combination of the standard GP-based acquisition and the LLM-suggested point, with the weight determined by the trust score
4. **Calibration**: The trust weight is updated after each evaluation, increasing when LLM suggestions lead to improvement and decreasing otherwise

### Key Innovation

The trust-weighting mechanism makes BORA robust to LLM hallucinations or domain-specific errors — if the LLM's suggestions are consistently poor, the system gracefully falls back to standard BO. This is critical for materials science where LLMs may have limited knowledge of specific alloy systems.

### Benchmarks

- Synthetic functions (Branin, Hartmann)
- Hyperparameter optimization (matching LLAMBO benchmarks)
- Showed that trust-weighted intervention outperforms both pure-LLM and pure-BO baselines

### Relevance to VCL

BORA-style trust weighting could be applied to LLM suggestions for:
- Which pipeline stage to evaluate next (CALPHAD vs. powder vs. LPBF)
- Whether to continue or abandon a partially-evaluated candidate
- Suggested composition modifications based on intermediate results

## 4. Reasoning BO — Multi-Agent LLM with Knowledge Graphs (Yang et al. 2025)

### Overview

Reasoning BO (Yang, Heng, Liu 2025) uses a **multi-agent LLM architecture** combined with **knowledge graphs** to structure scientific reasoning for BO. Different LLM agents handle different aspects of the optimization:

1. **Hypothesis agent**: Generates scientific hypotheses about the objective function
2. **Experiment design agent**: Proposes specific candidates based on hypotheses
3. **Analysis agent**: Interprets results and updates the knowledge graph
4. **Synthesis agent**: Combines insights across iterations

### Knowledge Graph Integration

The knowledge graph stores structured relationships between:
- Input variables and their known effects on the objective
- Observed correlations from experimental data
- Domain constraints and physical laws
- Hypotheses and their supporting/contradicting evidence

### Relevance to VCL

Knowledge graphs could encode:
- Phase diagram relationships (composition → stable phases)
- Process-structure-property linkages (laser power → grain size → strength)
- Literature-derived correlations (Si content → cracking susceptibility)

## 5. LMABO — LLM-Based Adaptive Acquisition Function Selection (Ngo et al. 2025)

### Overview

LMABO (Ngo, Hoang, et al. 2025) uses an LLM to **dynamically select which acquisition function** to use at each BO iteration, based on the current state of the optimization (exploration vs. exploitation balance, dimensionality, noise level, budget remaining).

### Mechanism

The LLM receives:
- Current dataset statistics (number of observations, best value, variance)
- Optimization metadata (iteration number, budget, dimensionality)
- Descriptions of available acquisition functions (EI, UCB, PI, Thompson Sampling, KG)

And outputs:
- Selected acquisition function with parameters (e.g., UCB with β=2.0)
- Natural-language justification

### Relevance to VCL

In a function network, different nodes may benefit from different acquisition strategies:
- Exploration (UCB with high β) for CALPHAD screening where evaluation is cheap
- Exploitation (EI) for LPBF printing where evaluation is expensive
- Knowledge Gradient for deciding which node to evaluate next

## 6. AlloyGPT — Domain-Specific Materials LLM (CMU 2025)

### Overview

AlloyGPT is a domain-specific LLM fine-tuned on alloy design literature, patents, and materials databases. While not directly a BO integration, it provides the domain-specific LLM that could power LLAMBO/BORA/LILO for alloy discovery.

### Capabilities

- Generate alloy compositions for target properties
- Predict qualitative process-structure-property relationships
- Summarize literature on specific alloy systems
- Suggest experimental strategies based on prior work

## Synthesis: Integration Mechanisms

### How LLMs Improve BO

| Mechanism | Methods | When It Helps | Risk |
|:---|:---|:---|:---|
| **Warmstarting** | LLAMBO | Cold-start, few initial data | Biased initialization if LLM wrong |
| **Prior specification** | LLAMBO, BORA | When domain knowledge exists but isn't formalized | Overconfident priors can harm exploration |
| **Preference elicitation** | LILO | Expert knowledge available in natural language | Expert biases propagated |
| **Trust-weighted intervention** | BORA | LLM has partial domain knowledge | Trust calibration requires iterations |
| **Knowledge structuring** | Reasoning BO | Complex multi-factor problems | Knowledge graph maintenance overhead |
| **Acquisition selection** | LMABO | No single acquisition function dominates | LLM may not understand BO theory deeply |

### Common Benchmarks

Most LLM+BO papers benchmark on:
1. **Synthetic functions**: Branin, Hartmann-6, Ackley, Rosenbrock
2. **HPOBench**: Hyperparameter optimization (most common; leverages LLMs' knowledge of ML)
3. **Design-Bench**: Offline design optimization tasks
4. **Production systems**: Meta's A/B testing (LILO only)

### Gap: No Materials Science Benchmarks

None of the published LLM+BO papers include materials science benchmarks. This represents an opportunity for VCL to define the benchmark task for LLM-augmented materials optimization (see `bofn-llm-bo-synthesis.md` §4).

## References

1. Liu, T., Feng, S., et al. (2024). Large Language Models to Enhance Bayesian Optimization. *ICLR 2024*. https://arxiv.org/abs/2402.03921
2. Kobalczyk, M., Lin, L., Letham, B., Zhao, S., Balandat, M., & Bakshy, E. (2025). Language-in-the-Loop Optimization: Incorporating Human Feedback into Bayesian Optimization with LLMs. *Meta AI Technical Report*.
3. Cissé, I., Kégl, B., & Fumagalli, F. (2025). BORA: Bayesian Optimization with LLM Reasoning Agents. *arXiv preprint*.
4. Yang, Z., Heng, J., & Liu, S. (2025). Reasoning Bayesian Optimization with Multi-Agent LLMs and Knowledge Graphs. *arXiv preprint*.
5. Ngo, T., Hoang, T. N., et al. (2025). LMABO: Language-Model-Assisted Bayesian Optimization. *arXiv preprint*.
6. Chu, W., & Ghahramani, Z. (2005). Preference Learning with Gaussian Processes. *ICML 2005*.
7. Balandat, M., et al. (2020). BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization. *NeurIPS 2020*.
