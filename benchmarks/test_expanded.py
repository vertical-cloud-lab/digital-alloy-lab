"""Quick test for the expanded LPBF problem class."""

import sys

sys.path.insert(0, ".")

import torch
from benchmarks.partial_kgfn.expanded_problem import ExpandedLPBFProblem

p = ExpandedLPBFProblem()
print(f"Nodes: {p.n_nodes}, Dim: {p.dim}")
print(f"DAG root nodes: {p.dag.get_root_nodes()}")
print(f"Node groups: {p.node_groups}")
print(f"Full cost: ${sum(p._group_costs)}")

# Test full evaluation
X = torch.rand(5, 13, dtype=torch.double)
X[:, :3] = X[:, :3] / X[:, :3].sum(dim=1, keepdim=True)
Y = p.evaluate(X)
print(f"\nFull eval shape: {Y.shape}")
for i in range(5):
    ys = Y[i, -1].item()
    print(f"  Row {i}: YS={ys:.4f}")

# Per-node partial evaluation
print("\nPartial evaluation test:")
for k in range(p.n_nodes):
    x_k = torch.rand(3, p.node_dims[k], dtype=torch.double)
    y_k = p.evaluate(x_k, idx=[k])
    print(
        f"  Node {k:2d} ({p.node_names[k]:>16s}): dim={p.node_dims[k]}, out_shape={y_k.shape}"
    )

# Optimal value
opt = p.optimal_value
print(f"\nOptimal YS (10k grid): {opt:.4f}")

# Group mapping
print("\nGroup mapping:")
for k in range(p.n_nodes):
    cost, group = p.get_group_for_node(k)
    print(f"  Node {k} -> group cost=${cost}, co-nodes={group}")

print("\nAll tests passed!")
