"""Partial KGFN — ported from frazier-lab/partial_kgfn for modern BoTorch.

Port of the p-KGFN acquisition function and supporting infrastructure from
Buathong et al. (2024) "Bayesian Optimization of Function Networks with Partial
Evaluations" (ICML 2024) and Buathong & Frazier (2025) "Fast Bayesian
Optimization of Function Networks with Partial Evaluations" (AutoML 2025).

Original: https://github.com/frazier-lab/partial_kgfn  (botorch==0.8.4)
This port: botorch>=0.12.0; torch>=2.0

Key changes from the original:
  - FixedNoiseGP replaced with SingleTaskGP (FixedNoiseGP removed in botorch 0.12)
  - fit_gpytorch_model → fit_gpytorch_mll
  - get_gp_samples replaced with get_matheron_path_model
    (botorch.sampling.pathwise); migration complete as of this port
  - Type annotations updated for Python 3.10+
"""
