"""Gaussian Process Network model for function networks.

Ported from frazier-lab/partial_kgfn (MIT license) for modern BoTorch (>=0.12).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/models/decoupled_gp_network.py

Key changes from original:
  - FixedNoiseGP → SingleTaskGP (FixedNoiseGP removed in botorch 0.12)
  - fit_gpytorch_model → fit_gpytorch_mll
  - Simplified initialization with SingleTaskGP defaults
"""

from __future__ import annotations

from typing import Any

import torch
from botorch.fit import fit_gpytorch_mll
from botorch.models import SingleTaskGP
from botorch.models.model import Model
from botorch.models.transforms.input import Normalize
from botorch.models.transforms.outcome import Standardize
from botorch.posteriors import TorchPosterior
from botorch.sampling import MCSampler
from gpytorch.mlls import ExactMarginalLogLikelihood
from torch import Tensor
from torch import nn

from benchmarks.partial_kgfn.dag import DAG


class GaussianProcessNetwork(Model):
    """A function network of Gaussian processes.

    Each node in the DAG has its own GP. The network posterior propagates
    samples through the DAG using reparameterised base samples.
    """

    def __init__(
        self,
        train_X: list[Tensor],
        train_Y: list[Tensor],
        dag: DAG,
        active_input_indices: list[list[int]],
        node_groups: list[list[int]] | None = None,
        node_dims: list[int] | None = None,
        train_Yvar: list[Tensor] | None = None,
        node_GPs: list[Model] | None = None,
        noisy: bool = False,
        node_input_bounds: list[Tensor | None] | None = None,
    ) -> None:
        super().__init__()
        self.train_X = train_X
        self.train_Y = train_Y
        self.dag = dag
        self.n_nodes = dag.get_n_nodes()
        self.node_dims = node_dims
        self.root_nodes = dag.get_root_nodes()
        self.active_input_indices = active_input_indices
        self.noisy = noisy
        self.node_groups = node_groups or [[x] for x in range(self.n_nodes)]
        # Optional per-node explicit input bounds for the Normalize input
        # transform. ``None`` (default) preserves the previous dynamic
        # behaviour. Per-entry ``None`` falls back to dynamic per-node
        # bounds — useful for root nodes whose bounds are already ``[-1, 1]``
        # by problem definition.
        self.node_input_bounds = node_input_bounds

        if train_Yvar is not None:
            self.train_Yvar = train_Yvar
        else:
            self.train_Yvar = [
                torch.ones_like(self.train_Y[k]) * 1e-6 for k in range(self.n_nodes)
            ]

        if node_GPs is not None:
            self.node_GPs = nn.ModuleList(node_GPs)
        else:
            gps = []
            for k in range(self.n_nodes):
                bounds_k = (
                    node_input_bounds[k] if node_input_bounds is not None else None
                )
                gp = _initialize_gp(
                    train_X=self.train_X[k],
                    train_Y=self.train_Y[k],
                    noisy=self.noisy,
                    bounds=bounds_k,
                )
                gps.append(gp)
            self.node_GPs = nn.ModuleList(gps)

    @property
    def num_outputs(self) -> int:
        return 1

    @property
    def num_nodes(self) -> int:
        return self.n_nodes

    @property
    def batch_shape(self) -> torch.Size:
        return torch.broadcast_shapes(*[gp.batch_shape for gp in self.node_GPs])

    def posterior(self, X: Tensor, observation_noise: bool = False, **kwargs):
        """Return a MultivariateNormalNetwork posterior."""
        return MultivariateNormalNetwork(
            self.node_GPs, self.dag, X, self.active_input_indices
        )

    def condition_on_observations(
        self,
        X: list[Tensor | None],
        Y: list[Tensor | None],
        Yvar: list[Tensor | None] | None = None,
        **kwargs: Any,
    ) -> GaussianProcessNetwork:
        """Condition the network on new per-node observations."""
        fantasy_models = [None] * self.n_nodes

        for k in range(self.n_nodes):
            if Y[k] is not None:
                Yvar_k = (
                    Yvar[k]
                    if Yvar is not None and Yvar[k] is not None
                    else torch.ones(Y[k].shape[1:], dtype=Y[k].dtype) * 1e-6
                )
                # Ensure cache is populated before conditioning
                _dummy = torch.rand(
                    1,
                    self.train_X[k].shape[-1],
                    dtype=self.train_X[k].dtype,
                    device=self.train_X[k].device,
                )
                _ = self.node_GPs[k].posterior(_dummy)
                # Do NOT call transform_inputs() here — condition_on_observations()
                # applies the input transform internally, so pre-transforming
                # would double-normalize the conditioning point.
                fantasy_model = self.node_GPs[k].condition_on_observations(
                    X=X[k],
                    Y=Y[k],
                    noise=Yvar_k,
                )
                fantasy_models[k] = fantasy_model
            else:
                fantasy_models[k] = self.node_GPs[k]

        return GaussianProcessNetwork(
            dag=self.dag,
            train_X=self.train_X,
            train_Y=self.train_Y,
            train_Yvar=self.train_Yvar,
            active_input_indices=self.active_input_indices,
            node_groups=self.node_groups,
            node_dims=self.node_dims,
            node_GPs=fantasy_models,
            node_input_bounds=self.node_input_bounds,
        )

    def fantasize(
        self,
        X: list[Tensor],
        samplers: list[MCSampler],
        evaluation_mask: Tensor,
        **kwargs: Any,
    ) -> GaussianProcessNetwork:
        """Construct a fantasy model for the selected nodes."""
        if len(X) != int(evaluation_mask.sum()):
            raise ValueError("Length of X must match the number of nodes to fantasize.")

        X_for_cond = [None] * self.n_nodes
        Y_for_cond = [None] * self.n_nodes
        list_idx = 0
        for k in range(self.n_nodes):
            if evaluation_mask[k] == 0:
                continue
            X_node_k = X[list_idx]
            X_for_cond[k] = X_node_k
            posterior_k = self.node_GPs[k].posterior(X_node_k)
            Y_node_k = samplers[list_idx](posterior_k)
            Y_for_cond[k] = Y_node_k
            list_idx += 1

        return self.condition_on_observations(X=X_for_cond, Y=Y_for_cond)


class MultivariateNormalNetwork(TorchPosterior):
    """Posterior of a Gaussian process network.

    Propagates reparameterised samples through the DAG to produce
    joint samples over all nodes.
    """

    def __init__(
        self,
        node_GPs: list[Model],
        dag: DAG,
        X: Tensor,
        indices_X: list[list[int]] | None = None,
    ) -> None:
        self.node_GPs = node_GPs
        self.dag = dag
        self.n_nodes = dag.get_n_nodes()
        self.root_nodes = dag.get_root_nodes()
        self.X = X
        self.active_input_indices = indices_X

    @property
    def device(self) -> torch.device:
        return self.X.device

    @property
    def dtype(self) -> torch.dtype:
        return self.X.dtype

    @property
    def event_shape(self) -> torch.Size:
        shape = torch.Size([self.X.shape[-2], self.n_nodes])
        return self.batch_shape + shape

    @property
    def batch_shape(self) -> torch.Size:
        gp_batch_shape = torch.broadcast_shapes(
            *[gp.batch_shape for gp in self.node_GPs]
        )
        X_batch_shape = self.X.shape[:-2]
        return torch.broadcast_shapes(gp_batch_shape, X_batch_shape)

    @property
    def base_sample_shape(self) -> torch.Size:
        return self.event_shape

    @property
    def batch_range(self) -> tuple[int, int]:
        return (0, -2)

    def rsample(self, sample_shape: torch.Size = torch.Size()) -> Tensor:
        """Draw reparameterised samples through the network.

        Uses the posterior mean propagation approach (deterministic forward pass
        through the DAG) when no base samples are provided.
        """
        nodes_out = self.X.new_empty(
            sample_shape + self.X.shape[:-1] + torch.Size([self.n_nodes]),
        )
        available = [False] * self.n_nodes

        for k in self.root_nodes:
            X_k = (
                self.X[..., self.active_input_indices[k]]
                if self.active_input_indices
                else self.X
            )
            post_k = self.node_GPs[k].posterior(X_k)
            nodes_out[..., k] = post_k.rsample(sample_shape)[..., 0]
            available[k] = True

        while not all(available):
            for k in range(self.n_nodes):
                parents = self.dag.get_parent_nodes(k)
                if not available[k] and all(available[j] for j in parents):
                    parent_samples = nodes_out[..., parents]
                    active_idx = self.active_input_indices[k]
                    if active_idx:
                        X_k = self.X[..., active_idx]
                    else:
                        # Node has no external inputs — use only parent samples
                        X_k = None
                    # Expand X_k to match sample_shape
                    if X_k is not None and sample_shape:
                        expand_shape = list(sample_shape) + [-1] * X_k.ndim
                        X_k = X_k.unsqueeze(0).expand(*expand_shape)
                    if X_k is not None:
                        X_k = torch.cat([X_k, parent_samples], -1)
                    else:
                        X_k = parent_samples
                    post_k = self.node_GPs[k].posterior(X_k)
                    nodes_out[..., k] = post_k.rsample(torch.Size([1]))[0, ..., 0]
                    available[k] = True

        return nodes_out

    def rsample_from_base_samples(
        self,
        sample_shape: torch.Size,
        base_samples: Tensor,
    ) -> Tensor:
        """Sample from the posterior using provided base samples.

        Propagates reparameterised samples through the DAG. For each node,
        uses ``rsample_from_base_samples`` on the node GP's posterior when
        available, otherwise falls back to ``rsample``.
        """
        nodes_samples = base_samples.new_empty(base_samples.shape)
        available = [False] * self.n_nodes
        batch_shape = base_samples.shape[len(sample_shape) : -2]

        if len(batch_shape) > 0:
            X = torch.broadcast_to(self.X, batch_shape + self.X.shape[-2:])
        else:
            X = self.X

        for k in self.root_nodes:
            X_k = (
                X[..., self.active_input_indices[k]] if self.active_input_indices else X
            )
            post_k = self.node_GPs[k].posterior(X_k)
            # Use rsample_from_base_samples — base_samples must be (n_samples, n_points)
            nodes_samples[..., k] = post_k.rsample_from_base_samples(
                sample_shape=sample_shape,
                base_samples=base_samples[..., k],
            )[..., 0]
            available[k] = True

        while not all(available):
            for k in range(self.n_nodes):
                parents = self.dag.get_parent_nodes(k)
                if not available[k] and all(available[j] for j in parents):
                    parent_samples = nodes_samples[..., parents]
                    active_idx = self.active_input_indices[k]
                    if active_idx:
                        X_k = X[..., active_idx]
                        aux_shape = [sample_shape[0]] + [1] * X_k.ndim
                        X_k = X_k.unsqueeze(0).repeat(*aux_shape)
                        X_k = torch.cat([X_k, parent_samples], -1)
                    else:
                        X_k = parent_samples
                    post_k = self.node_GPs[k].posterior(X_k)
                    # For non-root nodes, draw a single sample per existing
                    # outer sample to avoid compounding dimensionality
                    nodes_samples[..., k] = post_k.rsample(
                        sample_shape=torch.Size([1]),
                    )[0, ..., 0]
                    available[k] = True

        return nodes_samples


def _initialize_gp(
    train_X: Tensor,
    train_Y: Tensor,
    noisy: bool = False,
    bounds: Tensor | None = None,
) -> SingleTaskGP:
    """Initialize and fit a SingleTaskGP for a function network node.

    Args:
        train_X: Per-node training inputs ``(*batch, n, d_k)``.
        train_Y: Per-node training outputs ``(*batch, n, 1)``.
        noisy: Reserved for API compatibility.
        bounds: Optional ``2 x d_k`` tensor of explicit input bounds. When
            provided, the ``Normalize`` input transform is constructed with
            these fixed bounds. This prevents non-stationary lengthscale
            learning on intermediate-node GPs whose ``train_X`` includes
            parent-``y`` columns (which can drift across iterations as new
            extreme parent values are observed and would otherwise cause the
            ``Normalize`` transform to silently rescale on every refit).
    """
    dim = train_X.shape[-1]
    batch_shape = train_X.shape[:-2]
    output_dim = train_Y.shape[-1]

    if bounds is not None:
        input_transform = Normalize(d=dim, bounds=bounds)
    else:
        input_transform = Normalize(d=dim)

    model = SingleTaskGP(
        train_X=train_X,
        train_Y=train_Y,
        outcome_transform=Standardize(m=output_dim, batch_shape=batch_shape),
        input_transform=input_transform,
    )
    return model


def fit_gp_network(model: GaussianProcessNetwork, idx: int | None = None) -> None:
    """Fit one or all node GPs in the network."""
    if idx is None:
        for k in range(model.n_nodes):
            mll = ExactMarginalLogLikelihood(
                model.node_GPs[k].likelihood, model.node_GPs[k]
            )
            fit_gpytorch_mll(mll)
    else:
        mll = ExactMarginalLogLikelihood(
            model.node_GPs[idx].likelihood, model.node_GPs[idx]
        )
        fit_gpytorch_mll(mll)
