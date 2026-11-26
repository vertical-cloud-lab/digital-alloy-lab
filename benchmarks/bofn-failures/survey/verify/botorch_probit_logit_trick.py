"""Check: constraint c(f) = log_ndtr(-f) - log_ndtr(f) with eta=1, fat=[False] reproduces Phi(f) per sample."""
import torch
from torch.special import log_ndtr, ndtr
from botorch.utils.objective import compute_smoothed_feasibility_indicator, compute_feasibility_indicator
f = torch.linspace(-30, 30, 13, dtype=torch.double).view(1, 13, 1)  # samples x q x m (one latent output)
c = lambda Z, X=None: log_ndtr(-Z[..., 0]) - log_ndtr(Z[..., 0])
w = compute_smoothed_feasibility_indicator([c], f, eta=1.0, fat=[False])
lw = compute_smoothed_feasibility_indicator([c], f, eta=1.0, fat=[False], log=True)
print("max |w - Phi(f)|:", (w - ndtr(f[..., 0])).abs().max().item())
print("max |log w - log Phi(f)|:", (lw - log_ndtr(f[..., 0])).abs().max().item())
print("hard indicator == (f >= 0):", torch.equal(compute_feasibility_indicator([c], f), f[..., 0] >= 0))
