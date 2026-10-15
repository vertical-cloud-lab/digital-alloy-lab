"""Thompson sampling acquisition function for function networks.

Ported from frazier-lab/partial_kgfn (MIT license) for modern BoTorch (>=0.12).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/acquisition/tsfn.py

Changes from original:
  - Migrated from get_gp_samples to get_matheron_path_model
    (botorch.sampling.pathwise) for BoTorch >=0.13 compatibility
"""

from __future__ import annotations

import torch
from botorch.acquisition import AcquisitionFunction
from botorch.acquisition.objective import GenericMCObjective
from botorch.models.model import Model
from botorch.sampling.pathwise import get_matheron_path_model
from torch import Tensor


class ThompsonSamplingFN(AcquisitionFunction):
    """Thompson sampling over a function network.

    Draws one GP sample per node and evaluates the composed network
    to score candidate inputs.
    """

    def __init__(
        self,
        model: Model,
        objective: GenericMCObjective | None = None,
    ) -> None:
        super().__init__(model=model)
        self.objective = objective
        self.GP_samples = []
        for i in range(model.n_nodes):
            self.GP_samples.append(
                get_matheron_path_model(
                    model=model.node_GPs[i],
                    sample_shape=None,
                )
            )

    def forward(self, X: Tensor) -> Tensor:
        """Evaluate the TS acquisition value over the function network."""
        nodes_samples = X.new_empty(
            X.shape[:-1] + torch.Size([self.model.n_nodes]),
        )
        available = [False] * self.model.n_nodes

        for k in self.model.root_nodes:
            X_k = (
                X[..., self.model.active_input_indices[k]]
                if self.model.active_input_indices
                else X
            )
            nodes_samples[..., [k]] = self.GP_samples[k].posterior(X_k).mean
            available[k] = True

        while not all(available):
            for k in range(self.model.n_nodes):
                parents = self.model.dag.get_parent_nodes(k)
                if not available[k] and all(available[j] for j in parents):
                    parent_samples = nodes_samples[..., parents]
                    X_k = X[..., self.model.active_input_indices[k]]
                    X_k = torch.cat([X_k, parent_samples], -1)
                    nodes_samples[..., [k]] = self.GP_samples[k].posterior(X_k).mean
                    available[k] = True

        if self.objective is not None:
            output = self.objective(nodes_samples)
        else:
            output = nodes_samples[..., -1]
        if output.ndim != 1:
            output = output.squeeze(-1)
        return output
