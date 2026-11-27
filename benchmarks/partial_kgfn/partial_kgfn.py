"""Partial Knowledge Gradient for Function Networks (p-KGFN).

Ported from frazier-lab/partial_kgfn (MIT license) for modern BoTorch (>=0.12).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/acquisition/partial_kgfn.py

This implements the p-KGFN acquisition function from:
  Buathong et al. (2024) "Bayesian Optimization of Function Networks with
  Partial Evaluations", ICML 2024.

Key changes from original:
  - Updated type annotations for Python 3.10+
  - GenericDeterministicModel import path unchanged (still in botorch.models.deterministic)
"""

from __future__ import annotations

from typing import Any

import torch
from botorch.acquisition.cost_aware import CostAwareUtility
from botorch.acquisition.monte_carlo import MCAcquisitionFunction
from botorch.acquisition.objective import MCAcquisitionObjective, PosteriorTransform
from botorch.exceptions.errors import UnsupportedError
from botorch.logging import logger
from botorch.models.deterministic import GenericDeterministicModel
from botorch.models.model import Model
from botorch.sampling import ListSampler, MCSampler, SobolQMCNormalSampler
from botorch.utils.sampling import draw_sobol_samples
from botorch.utils.transforms import t_batch_mode_transform
from torch import Tensor


def _network_posterior_mean(
    model,
    X: Tensor,
    n_saa: int = 64,
    sampler: "MCSampler | None" = None,
) -> Tensor:
    """Monte-Carlo (SAA) estimate of E[g(f(X))] for the final network node.

    The original ``frazier-lab/partial_kgfn`` implementation integrates the
    inner KG value with a Sample Average Approximation (SAA) over the
    fantasy network posterior. Earlier versions of this file deterministically
    propagated posterior means through the DAG (computing ``g(E[f(x)])``),
    which is biased by Jensen's inequality whenever the downstream node
    functions are non-linear and the parent-node posteriors are non-degenerate.

    This routine instead draws ``n_saa`` reparameterised samples through the
    full GP network via :class:`MultivariateNormalNetwork.rsample` and
    averages the final-node value across the SAA dimension, recovering an
    unbiased estimate of ``E[g(f(x))]``.

    To support **common random numbers (CRN)** across the per-candidate /
    per-fantasy inner KG comparisons, callers should pass a single
    :class:`SobolQMCNormalSampler` instance constructed once per outer
    ``forward`` call and reuse it across every ``_network_posterior_mean``
    invocation. The sampler caches its base samples, so identical
    standard-normal draws are reused whenever the posterior shape matches
    — this is what removes the variance-of-difference noise that previously
    made KG ranking dominated by SAA Monte Carlo error.

    Args:
        model: A fitted (possibly fantasised) ``GaussianProcessNetwork``.
        X: ``(*batch, n_candidates, d)`` tensor of network inputs.
        n_saa: Number of SAA Monte Carlo samples (used only when ``sampler``
            is ``None`` and a fresh ``SobolQMCNormalSampler`` is constructed
            on the fly).
        sampler: Optional pre-constructed ``MCSampler`` to use for CRN.

    Returns:
        Tensor of shape ``(*batch, n_candidates)`` with the SAA estimate of
        the final node's posterior mean at each candidate.
    """
    posterior = model.posterior(X)
    if sampler is None:
        # Lazy fallback: a fresh seeded Sobol sampler so single-shot callers
        # at least get reproducible draws within one call. CRN across
        # multiple calls requires the caller to pass a shared sampler.
        sampler = SobolQMCNormalSampler(
            sample_shape=torch.Size([n_saa]), seed=0,
        )
    samples = sampler(posterior)
    # samples shape: (n_saa, *batch, n_candidates, n_nodes)
    return samples[..., -1].mean(dim=0)


class PartialKnowledgeGradientFN(MCAcquisitionFunction):
    r"""Batch Discrete Knowledge Gradient for Function Networks with partial evaluations.

    Computes the p-KGFN acquisition value: the expected increase in the
    best achievable network output after fantasizing an observation at a
    selected node.
    """

    def __init__(
        self,
        model: Model,
        d: int,
        q: int,
        node_dim: int,
        problem_bounds: Tensor,
        X_fantasies_candidates: Tensor | None = None,
        X_evaluation_mask: Tensor | None = None,
        num_fantasies: int | None = None,
        sampler: list[MCSampler] | None = None,
        use_posterior_mean: bool = True,
        objective: MCAcquisitionObjective | None = None,
        posterior_transform: PosteriorTransform | None = None,
        inner_sampler: MCSampler | None = None,
        current_value: Tensor | None = None,
        cost_aware_utility: CostAwareUtility | None = None,
        cost_sampler: MCSampler | None = None,
        **kwargs: Any,
    ) -> None:
        r"""Discrete Knowledge Gradient for function network with partial evaluations.

        Args:
            model: A fitted GaussianProcessNetwork model.
            d: The original problem dimension (full network input).
            q: Number of points to fantasize (currently only q=1 supported).
            node_dim: Input dimension at the node of interest.
            problem_bounds: A ``2 x d`` tensor of bounds.
            X_fantasies_candidates: Discretized candidates for inner optimisation.
            X_evaluation_mask: Binary tensor indicating which node to fantasize.
            num_fantasies: Number of fantasy samples for outer expectation.
            sampler: MC sampler(s) for fantasy observations.
            use_posterior_mean: Whether to use posterior mean for inner value
                (retained for API compatibility with original p-KGFN).
            objective: MC objective for combining intermediate outputs.
            posterior_transform: Optional posterior transform
                (retained for API compatibility with original p-KGFN).
            inner_sampler: Sampler for inner MC expectation
                (retained for API compatibility with original p-KGFN).
            current_value: Current best network output (for computing KG value).
            cost_aware_utility: Cost-aware utility function
                (retained for API compatibility; cost weighting is done in
                the outer loop via per-node cost division).
            cost_sampler: Sampler for cost model
                (retained for API compatibility with original p-KGFN).
        """
        if sampler is None:
            if num_fantasies is None:
                raise ValueError(
                    "Must specify `num_fantasies` if no `sampler` is provided."
                )
            sampler = [
                SobolQMCNormalSampler(sample_shape=torch.Size([num_fantasies]))
                for _ in range(int(X_evaluation_mask.sum()))
            ]
        elif num_fantasies is not None:
            if isinstance(sampler, ListSampler):
                sample_shape = sampler.samplers[0].sample_shape
            elif isinstance(sampler, list):
                if len(sampler) == 0:
                    raise ValueError("`sampler` list must be non-empty.")
                sample_shape = sampler[0].sample_shape
            else:
                sample_shape = sampler.sample_shape
            if sample_shape != torch.Size([num_fantasies]):
                raise ValueError(
                    f"Sampler shape must match num_fantasies={num_fantasies}."
                )
        else:
            if isinstance(sampler, ListSampler):
                num_fantasies = sampler.samplers[0].sample_shape[0]
            elif isinstance(sampler, list):
                if len(sampler) == 0:
                    raise ValueError("`sampler` list must be non-empty.")
                num_fantasies = sampler[0].sample_shape[0]
            else:
                num_fantasies = sampler.sample_shape[0]

        super().__init__(model=model, objective=objective)

        if isinstance(objective, MCAcquisitionObjective) and inner_sampler is None:
            inner_sampler = SobolQMCNormalSampler(sample_shape=torch.Size([128]))

        if objective is None and model.num_outputs != 1:
            if posterior_transform is None:
                raise UnsupportedError(
                    "Must specify an objective or posterior_transform for multi-output."
                )

        if X_fantasies_candidates is None:
            self.X_fantasies_candidates = draw_sobol_samples(
                bounds=problem_bounds, n=50 * d, q=1
            ).squeeze(-2)
        else:
            self.X_fantasies_candidates = X_fantasies_candidates

        self.objective = objective
        self.posterior_transform = posterior_transform
        self.inner_sampler = inner_sampler
        self.num_fantasies = num_fantasies
        self.current_value = current_value
        self.cost_aware_utility = cost_aware_utility
        self.use_posterior_mean = use_posterior_mean
        self.cost_sampler = cost_sampler
        self.sampler = sampler
        self.X_evaluation_mask = X_evaluation_mask
        self.d = d
        self.q = q
        self.node_dim = node_dim

    @t_batch_mode_transform()
    def forward(self, X: Tensor, verbose: bool = False) -> Tensor:
        r"""Evaluate p-KGFN on candidate set ``X``.

        Processes each candidate independently to avoid complex batch shape
        interactions between the fantasy model and the network posterior.

        Args:
            X: ``b x q x d_k`` tensor of candidates at the selected node.

        Returns:
            A ``b``-dim tensor of p-KGFN values.
        """
        # Identify which node to fantasize
        nonzero_idx = (self.X_evaluation_mask == 1).nonzero().squeeze()
        k = int(nonzero_idx.item()) if nonzero_idx.dim() == 0 else int(nonzero_idx[0].item())

        b = X.shape[0]
        values = torch.zeros(b, dtype=torch.double)

        # CRN: a single seeded SAA sampler reused across every candidate i
        # and every fantasy f. As long as the inner posterior shape matches,
        # the same standard-normal base samples are reused, so the
        # KG-difference between candidates/fantasies is dominated by the
        # mean change rather than fresh Monte-Carlo noise.
        n_saa = int(getattr(self, "n_inner_saa", 64))
        saa_seed = int(getattr(self, "saa_seed", 12345))
        inner_saa_sampler = SobolQMCNormalSampler(
            sample_shape=torch.Size([n_saa]), seed=saa_seed,
        )

        for i in range(b):
            x_i = X[i: i + 1]  # (1, q, d_k)
            fantasy_values = []

            # Draw all fantasy observations at once using the Sobol sampler
            # for lower-variance quasi-random samples. Pass
            # ``observation_noise=True`` to match the upstream
            # frazier-lab/partial_kgfn behaviour: when the problem has
            # observation noise, fantasies must include it, otherwise KG
            # over-values noiseless fantasy observations.
            post_k = self.model.node_GPs[k].posterior(
                x_i.squeeze(1), observation_noise=True
            )
            all_y_fantasies = self.sampler[0](post_k)  # (num_fantasies, 1, 1)

            for f in range(self.num_fantasies):
                y_fantasy = all_y_fantasies[f]  # (1, 1) — matches X_cond shape

                # Condition node k on the fantasy observation
                X_cond = [None] * self.model.n_nodes
                Y_cond = [None] * self.model.n_nodes
                X_cond[k] = x_i.squeeze(1)  # (1, d_k)
                Y_cond[k] = y_fantasy

                fantasy_model = self.model.condition_on_observations(
                    X=X_cond, Y=Y_cond
                )

                # Compute the best posterior mean of the fantasy model at grid
                grid_vals = _network_posterior_mean(
                    fantasy_model,
                    self.X_fantasies_candidates,
                    sampler=inner_saa_sampler,
                )  # (n_grid,)
                fantasy_values.append(grid_vals.max().item())

            # Average over fantasies
            values[i] = sum(fantasy_values) / self.num_fantasies

        if self.current_value is not None:
            values = values - self.current_value

        if verbose:
            logger.info(f"p-KGFN values: {values}")
        return values

    def get_augmented_q_batch_size(self, q: int) -> int:
        return 1
