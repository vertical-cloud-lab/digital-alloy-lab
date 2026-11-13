"""Manufacturing function network test problem.

Ported from frazier-lab/partial_kgfn (MIT license) for modern BoTorch (>=0.12).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/test_functions/manufacter_gp.py

This is the "Manu" test problem from Buathong et al. (2024), a 4-node function
network where each node is a sample from a GP prior.

DAG structure:
  Node 0: x1, x2 → y0         (root node)
  Node 1: y0 → y1              (depends on node 0)
  Node 2: x3, x4 → y2         (root node)
  Node 3: y1, y2 → y3          (depends on nodes 1, 2)

Key change: FixedNoiseGP → SingleTaskGP (FixedNoiseGP removed in botorch 0.12)
"""

from __future__ import annotations

import torch
from botorch.models import SingleTaskGP
from botorch.sampling.pathwise import get_matheron_path_model
from torch import Tensor

from benchmarks.partial_kgfn.dag import DAG


class ManufacturingGPNetwork:
    """4-node GP-sampled function network test problem.

    Each node function is a single draw from a GP prior with specified
    hyperparameters. The optimal value is known from exhaustive evaluation.
    """

    n_nodes = 4
    node_groups = [[0], [1], [2], [3]]
    parent_nodes = [[], [0], [], [1, 2]]
    dag = DAG(parent_nodes=parent_nodes)

    def __init__(self, node_costs: list[float | int], seed: int = 0) -> None:
        self.dim = 4
        self.node_dims = [2, 1, 2, 2]
        self.bounds = torch.tensor([[-1.0] * 4, [1.0] * 4], dtype=torch.double)
        self.parent_bounds = [
            None,
            torch.tensor([[-2.0], [2.0]], dtype=torch.double),
            None,
            torch.tensor([[-1.0, -1.0], [1.0, 1.0]], dtype=torch.double),
        ]
        self.active_input_indices = [[0, 1], [], [2, 3], []]
        self.node_costs = node_costs

        # Generate node functions from GP priors with fixed seeds
        self._build_node_functions(seed)

    def _build_node_functions(self, seed: int) -> None:
        """Create GP-sampled functions for each node.

        In modern BoTorch (>=0.12), SingleTaskGP uses RBFKernel directly
        (no ScaleKernel wrapper), so lengthscale is set on covar_module
        rather than covar_module.base_kernel.
        Uses get_matheron_path_model for BoTorch >=0.13 compatibility.
        """
        # Seed ALL random ops so the problem is fully deterministic for a
        # given seed, regardless of external random state.
        torch.manual_seed(seed * 7919 + 42)
        X0 = torch.rand(5, 2, dtype=torch.double)
        Y0 = torch.rand(5, 1, dtype=torch.double)
        model0 = SingleTaskGP(train_X=X0, train_Y=Y0)
        torch.manual_seed(88 + seed)
        self.function0 = get_matheron_path_model(model=model0, sample_shape=None)

        X1 = torch.rand(5, 1, dtype=torch.double)
        Y1 = torch.rand(5, 1, dtype=torch.double)
        model1 = SingleTaskGP(train_X=X1, train_Y=Y1)
        model1.covar_module.lengthscale = torch.tensor(
            [[1.0]], dtype=torch.double
        )
        torch.manual_seed(112 + seed)
        self.function1 = get_matheron_path_model(model=model1, sample_shape=None)

        X2 = torch.rand(5, 2, dtype=torch.double)
        Y2 = torch.rand(5, 1, dtype=torch.double)
        model2 = SingleTaskGP(train_X=X2, train_Y=Y2)
        model2.covar_module.lengthscale = torch.tensor(
            [[1.0, 1.0]], dtype=torch.double
        )
        torch.manual_seed(11 + seed)
        self.function2 = get_matheron_path_model(model=model2, sample_shape=None)

        X3 = torch.rand(5, 2, dtype=torch.double)
        Y3 = torch.rand(5, 1, dtype=torch.double)
        model3 = SingleTaskGP(train_X=X3, train_Y=Y3)
        model3.covar_module.lengthscale = torch.tensor(
            [[3.0, 3.0]], dtype=torch.double
        )
        torch.manual_seed(185 + seed)
        self.function3 = get_matheron_path_model(model=model3, sample_shape=None)

    def evaluate(
        self,
        X: Tensor,
        idx: list[int] | None = None,
    ) -> Tensor:
        """Evaluate the function network.

        Args:
            X: Input tensor. Shape depends on whether evaluating full network
               or a single node.
            idx: Node group index (e.g. [0], [1], [2], [3]). If None,
                 evaluate the full network (X should be n×4).

        Returns:
            For full evaluation: n×4 tensor of all node outputs (detached).
            For single node: n×1 tensor of that node's output (detached).
        """
        if idx is None:
            # Full evaluation
            output = torch.empty(
                X.shape[:-1] + torch.Size([self.n_nodes]), dtype=torch.double
            )
            output[..., [0]] = self.function0(X[..., [0, 1]]).detach()
            output[..., [1]] = self.function1(output[..., [0]]).detach()
            output[..., [2]] = self.function2(X[..., [2, 3]]).detach()
            output[..., [3]] = self.function3(output[..., [1, 2]]).detach()
            return output
        elif idx == [0]:
            return self.function0(X).detach()
        elif idx == [1]:
            return self.function1(X).detach()
        elif idx == [2]:
            return self.function2(X).detach()
        elif idx == [3]:
            return self.function3(X).detach()
        else:
            raise ValueError(f"Invalid node index {idx}")
