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


class ExtendedManufacturingGPNetwork(ManufacturingGPNetwork):
    """6-node extension of the Manufacturing DAG with optional noise.

    Adds two downstream nodes to make the problem harder and deeper:

        Node 4: (x4, y3) → y4      (1 active input + 1 parent)
        Node 5: (y3, y4) → y5      (2 parents, no active input)

    Full DAG: 0 → 1, 2, (1,2) → 3, (x4, 3) → 4, (3, 4) → 5. The final
    optimisation target is y5. Per-node input ordering follows
    ``construct_obs_set`` (active-part first, then parent-part), so node 4's
    input vector is ``[x4, y3]``.

    The ``noise_std`` argument adds i.i.d. Gaussian observation noise to
    every ``evaluate()`` call, simulating the kind of measurement/simulator
    noise a real pipeline would have. Set ``noise_std=0.0`` (default) for
    the noiseless regime used by the legacy tests.

    Use ``compute_true_max(n_samples=...)`` for a Sobol-grid estimate of the
    true maximum of the final node (noiseless), which the benchmark plots as
    a dashed upper reference.
    """

    # These must override the class-level attrs on ManufacturingGPNetwork.
    # We bind them as instance attrs in __init__ so both classes can coexist.

    def __init__(
        self,
        node_costs: list[float | int],
        seed: int = 0,
        noise_std: float = 0.0,
        coupling: float = 0.0,
    ) -> None:
        if len(node_costs) != 6:
            raise ValueError(
                f"ExtendedManufacturingGPNetwork expects 6 node costs, "
                f"got {len(node_costs)}"
            )

        # Instance-level DAG topology (shadows class-level 4-node attrs).
        self.n_nodes = 6
        self.node_groups = [[0], [1], [2], [3], [4], [5]]
        self.parent_nodes = [[], [0], [], [1, 2], [3], [3, 4]]
        self.dag = DAG(parent_nodes=self.parent_nodes)

        self.dim = 5
        self.node_dims = [2, 1, 2, 2, 2, 2]
        self.bounds = torch.tensor([[-1.0] * 5, [1.0] * 5], dtype=torch.double)
        self.parent_bounds = [
            None,
            torch.tensor([[-2.0], [2.0]], dtype=torch.double),
            None,
            torch.tensor([[-1.0, -1.0], [1.0, 1.0]], dtype=torch.double),
            # Node 4: active x4 in [-1,1], parent y3 in [-2,2]
            torch.tensor([[-1.0, -2.0], [1.0, 2.0]], dtype=torch.double),
            # Node 5: parents y3, y4 each in [-2,2]
            torch.tensor([[-2.0, -2.0], [2.0, 2.0]], dtype=torch.double),
        ]
        self.active_input_indices = [[0, 1], [], [2, 3], [], [4], []]
        self.node_costs = list(node_costs)
        self.noise_std = float(noise_std)
        # Physics-inspired parent→child coupling: fraction of each non-root
        # node's output that is a direct linear passthrough of its inputs
        # (rather than the Matheron GP draw). ``coupling=0.0`` reproduces
        # the pure-GP-prior 6-node problem; ``coupling=0.5`` mixes 50/50
        # GP vs. linear passthrough, dramatically increasing parent→child
        # (and hence root→terminal) R². Motivation: in a real LPBF/CALPHAD
        # pipeline, freezing range / solidus / grain-refiner efficacy
        # computed at the CALPHAD root passes through each downstream
        # stage as a deterministic "physics gate" (Edison literature
        # retrievals on alloy-property sensitivity, 2026-04-21).
        self.coupling = float(coupling)

        self._build_node_functions(seed)

    def _build_node_functions(self, seed: int) -> None:
        # Re-use parent's 4-node construction (sets self.function0..function3).
        # Note: parent uses self.dim / self.bounds only for documentation, but
        # the GP-prior draws are independent of those, so it's fine that we
        # carry 5-dim bounds while function0/function2 still take 2-dim inputs.
        super()._build_node_functions(seed)

        # Node 4: 2-dim input (x4, y3), moderate lengthscale.
        torch.manual_seed(seed * 7919 + 231)
        X4 = torch.rand(5, 2, dtype=torch.double)
        Y4 = torch.rand(5, 1, dtype=torch.double)
        model4 = SingleTaskGP(train_X=X4, train_Y=Y4)
        model4.covar_module.lengthscale = torch.tensor(
            [[1.5, 1.0]], dtype=torch.double
        )
        torch.manual_seed(seed * 7919 + 232)
        self.function4 = get_matheron_path_model(model=model4, sample_shape=None)

        # Node 5: 2-dim input (y3, y4), longer lengthscale → smoother readout.
        torch.manual_seed(seed * 7919 + 311)
        X5 = torch.rand(5, 2, dtype=torch.double)
        Y5 = torch.rand(5, 1, dtype=torch.double)
        model5 = SingleTaskGP(train_X=X5, train_Y=Y5)
        model5.covar_module.lengthscale = torch.tensor(
            [[2.0, 2.0]], dtype=torch.double
        )
        torch.manual_seed(seed * 7919 + 312)
        self.function5 = get_matheron_path_model(model=model5, sample_shape=None)

    def _add_noise(self, output: Tensor) -> Tensor:
        if self.noise_std > 0.0:
            return output + self.noise_std * torch.randn_like(output)
        return output

    def _couple(self, y_gp: Tensor, x_input: Tensor) -> Tensor:
        """Add a linear passthrough of inputs to the GP output.

        ``coupling=0`` returns ``y_gp`` unchanged (pure GP prior, original
        Buathong 2024 Manu problem). ``coupling=alpha > 0`` adds a
        deterministic parent-mean signal:

            y = y_gp + alpha * mean(x_input)

        Additive (not blended) — the GP variance is preserved and each
        non-root node's output picks up a monotone correlation with its
        parents, which chains down the DAG so that CALPHAD-root signal
        survives to the terminal node. Motivation: in a real LPBF/CALPHAD
        pipeline, freezing range / solidus / grain-refiner efficacy
        computed at the CALPHAD root passes through each downstream
        stage as a deterministic "physics gate" (Edison alloy-property-
        sensitivity literature retrievals, 2026-04-21).
        """
        if self.coupling == 0.0:
            return y_gp
        passthrough = x_input.mean(dim=-1, keepdim=True)
        return y_gp + self.coupling * passthrough

    def evaluate(
        self,
        X: Tensor,
        idx: list[int] | None = None,
        noiseless: bool = False,
    ) -> Tensor:
        if idx is None:
            output = torch.empty(
                X.shape[:-1] + torch.Size([self.n_nodes]), dtype=torch.double
            )
            output[..., [0]] = self.function0(X[..., [0, 1]]).detach()
            y1_gp = self.function1(output[..., [0]]).detach()
            output[..., [1]] = self._couple(y1_gp, output[..., [0]])
            output[..., [2]] = self.function2(X[..., [2, 3]]).detach()
            y3_in = output[..., [1, 2]]
            y3_gp = self.function3(y3_in).detach()
            output[..., [3]] = self._couple(y3_gp, y3_in)
            # Node 4 input order = (active x4, parent y3) per construct_obs_set.
            node4_in = torch.cat([X[..., [4]], output[..., [3]]], dim=-1)
            y4_gp = self.function4(node4_in).detach()
            output[..., [4]] = self._couple(y4_gp, node4_in)
            # Node 5 input order = (parent y3, parent y4) — no active inputs.
            node5_in = torch.cat([output[..., [3]], output[..., [4]]], dim=-1)
            y5_gp = self.function5(node5_in).detach()
            output[..., [5]] = self._couple(y5_gp, node5_in)
        elif idx == [0]:
            output = self.function0(X).detach()
        elif idx == [1]:
            y_gp = self.function1(X).detach()
            output = self._couple(y_gp, X)
        elif idx == [2]:
            output = self.function2(X).detach()
        elif idx == [3]:
            y_gp = self.function3(X).detach()
            output = self._couple(y_gp, X)
        elif idx == [4]:
            y_gp = self.function4(X).detach()
            output = self._couple(y_gp, X)
        elif idx == [5]:
            y_gp = self.function5(X).detach()
            output = self._couple(y_gp, X)
        else:
            raise ValueError(f"Invalid node index {idx}")

        return output if noiseless else self._add_noise(output)

    def compute_true_max(self, n_samples: int = 16384, seed: int = 0) -> float:
        """Sobol-grid estimate of max(final-node) over the full design space.

        Uses noiseless evaluations so the returned value is an upper
        reference for all noisy-campaign best-so-far traces.
        """
        from botorch.utils.sampling import draw_sobol_samples

        grid = draw_sobol_samples(
            bounds=self.bounds, n=n_samples, q=1, seed=seed
        ).squeeze(-2)
        with torch.no_grad():
            y = self.evaluate(grid, noiseless=True)
        return float(y[..., -1].max().item())
