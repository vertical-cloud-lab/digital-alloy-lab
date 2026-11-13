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


def _network_posterior_mean(model, X: Tensor) -> Tensor:
    """Compute posterior mean of the final node output through the network.

    Propagates posterior means through the DAG, handling arbitrary batch shapes
    from fantasy models (where some nodes have fantasy dims and others don't).

    Returns:
        Tensor of shape ``(*batch_shape, n_candidates)`` containing the
        posterior mean of the final node for each candidate.
    """
    n_nodes = model.n_nodes
    nodes_mean = {}
    available = [False] * n_nodes

    for k in model.root_nodes:
        X_k = (
            X[..., model.active_input_indices[k]]
            if model.active_input_indices
            else X
        )
        nodes_mean[k] = model.node_GPs[k].posterior(X_k).mean[..., 0]
        available[k] = True

    while not all(available):
        for k in range(n_nodes):
            parents = model.dag.get_parent_nodes(k)
            if not available[k] and all(available[j] for j in parents):
                # Broadcast parent means to common shape
                parent_means = [nodes_mean[p] for p in parents]
                target_shape = torch.broadcast_shapes(
                    *[m.shape for m in parent_means]
                )
                parent_means = [m.expand(target_shape) for m in parent_means]
                parent_mean = torch.stack(parent_means, dim=-1)

                X_k = X[..., model.active_input_indices[k]]
                # Broadcast X_k to match parent_mean batch dims
                if parent_mean.dim() > X_k.dim():
                    extra = parent_mean.dim() - X_k.dim()
                    for _ in range(extra):
                        X_k = X_k.unsqueeze(0)
                    X_k = X_k.expand(
                        parent_mean.shape[:-1] + X_k.shape[-1:]
                    )
                X_k = torch.cat([X_k, parent_mean], -1)
                nodes_mean[k] = model.node_GPs[k].posterior(X_k).mean[..., 0]
                available[k] = True

    # Return the final node's posterior mean
    return nodes_mean[n_nodes - 1]


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

        for i in range(b):
            x_i = X[i: i + 1]  # (1, q, d_k)
            fantasy_values = []

            # Draw all fantasy observations at once using the Sobol sampler
            # for lower-variance quasi-random samples
            post_k = self.model.node_GPs[k].posterior(x_i.squeeze(1))
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
                    fantasy_model, self.X_fantasies_candidates
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
