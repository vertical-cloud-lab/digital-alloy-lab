"""Utility functions for constructing observation sets for GP networks.

Ported from frazier-lab/partial_kgfn (MIT license).
Original: https://github.com/frazier-lab/partial_kgfn/blob/main/partial_kgfn/utils/construct_obs_set.py
"""

from __future__ import annotations

import torch
from torch import Tensor


def construct_obs_set(
    X: Tensor,
    Y: Tensor,
    parent_nodes: list[list[int]],
    active_input_indices: list[list[int]],
) -> tuple[list[Tensor], list[Tensor]]:
    """Reconstruct training data into per-node format for the GP network.

    For each node, concatenates:
      - The active input columns from X (the external decision variables)
      - The parent node outputs from Y (the intermediate outputs)

    Args:
        X: ``n x d`` tensor of full network inputs.
        Y: ``n x n_nodes`` tensor of all node outputs.
        parent_nodes: Parent node indices for each node.
        active_input_indices: Active input column indices for each node.

    Returns:
        (train_X, train_Y) — per-node training data lists.
    """
    num_nodes = len(parent_nodes)
    train_X = []
    train_Y = []

    for idx in range(num_nodes):
        has_parents = len(parent_nodes[idx]) > 0
        has_active = len(active_input_indices[idx]) > 0

        if has_parents and has_active:
            active_part = X[..., active_input_indices[idx]]
            if active_part.ndim == 1:
                active_part = active_part.unsqueeze(-1)
            parent_part = Y[..., parent_nodes[idx]]
            if parent_part.ndim == 1:
                parent_part = parent_part.unsqueeze(-1)
            if parent_part.ndim > active_part.ndim:
                shape_list = [1] * parent_part.ndim
                shape_list[0] = parent_part.shape[0]
                active_part = active_part.unsqueeze(0).repeat(torch.Size(shape_list))
            train_X_node = torch.cat((active_part, parent_part), dim=-1)

        elif has_parents and not has_active:
            parent_part = Y[..., parent_nodes[idx]]
            if parent_part.ndim == 1:
                parent_part = parent_part.unsqueeze(-1)
            train_X_node = parent_part

        elif not has_parents and has_active:
            active_part = X[..., active_input_indices[idx]]
            if active_part.ndim == 1:
                active_part = active_part.unsqueeze(-1)
            train_X_node = active_part

        else:
            raise ValueError(f"Node {idx} has no parents and no active inputs.")

        train_X.append(train_X_node)
        train_Y.append(Y[..., idx].unsqueeze(-1))

    return train_X, train_Y


def compute_posterior_mean_network(
    model,
    X: Tensor,
    objective=None,
) -> Tensor:
    """Compute the posterior mean of the network final output.

    Propagates posterior means through the DAG.

    Args:
        model: A GaussianProcessNetwork.
        X: ``n x d`` tensor of candidate inputs.
        objective: Optional objective to apply to the node outputs.

    Returns:
        ``n``-dim tensor of posterior mean final outputs.
    """
    n_nodes = model.n_nodes
    nodes_mean = X.new_empty(
        X.shape[:-1] + torch.Size([n_nodes]),
    )
    available = [False] * n_nodes

    for k in model.root_nodes:
        X_k = (
            X[..., model.active_input_indices[k]]
            if model.active_input_indices
            else X
        )
        nodes_mean[..., k] = model.node_GPs[k].posterior(X_k).mean[..., 0]
        available[k] = True

    while not all(available):
        for k in range(n_nodes):
            parents = model.dag.get_parent_nodes(k)
            if not available[k] and all(available[j] for j in parents):
                parent_mean = nodes_mean[..., parents]
                X_k = X[..., model.active_input_indices[k]]
                X_k = torch.cat([X_k, parent_mean], -1)
                nodes_mean[..., k] = model.node_GPs[k].posterior(X_k).mean[..., 0]
                available[k] = True

    if objective is not None:
        return objective(nodes_mean)
    return nodes_mean[..., -1]
