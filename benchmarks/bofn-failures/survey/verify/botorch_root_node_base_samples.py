"""Reproduce the GP-network root-node base-sample shape problem on the installed BoTorch."""
import warnings, torch, botorch, gpytorch
from botorch.models import SingleTaskGP
from botorch.sampling.normal import SobolQMCNormalSampler
warnings.filterwarnings("ignore")
torch.manual_seed(0)
print("botorch", botorch.__version__, "gpytorch", gpytorch.__version__, "torch", torch.__version__)
X = torch.rand(10, 2, dtype=torch.double); Y = (X.sum(-1, keepdim=True)).sin()
gp = SingleTaskGP(X, Y).eval()
n_nodes = 3
for batch, q in [((4,), 1), ((4,), 3), ((), 1)]:
    Xt = torch.rand(*batch, q, 2, dtype=torch.double)
    post = gp.posterior(Xt)
    S = torch.Size([16])
    # network-level base samples, one standard-normal column per node: S x batch x q x n_nodes
    net_base = torch.randn(*S, *batch, q, n_nodes, dtype=torch.double)
    print(f"\nbatch={batch} q={q}: root posterior base_sample_shape={tuple(post.base_sample_shape)}, "
          f"_extended_shape={tuple(post._extended_shape(S))}")
    # (a) legacy BOFN pattern: rsample(sample_shape, base_samples=unsqueeze(base[...,k], -1))
    try:
        post.rsample(S, base_samples=net_base[..., 0].unsqueeze(-1))
        print("  (a) rsample(..., base_samples=...)       OK")
    except Exception as e:
        print(f"  (a) rsample(..., base_samples=...)       {type(e).__name__}: {str(e)[:110]}")
    # (b) mechanical port: rsample_from_base_samples with the trailing singleton dim kept
    try:
        out = post.rsample_from_base_samples(S, net_base[..., 0].unsqueeze(-1))
        print(f"  (b) rsample_from_base_samples(unsqueezed) OK shape={tuple(out.shape)}")
    except Exception as e:
        print(f"  (b) rsample_from_base_samples(unsqueezed) {type(e).__name__}: {str(e)[:110]}")
    # (c) modern pattern: drop the trailing dim -> sample_shape x base_sample_shape
    out = post.rsample_from_base_samples(S, net_base[..., 0])
    print(f"  (c) rsample_from_base_samples(base[...,k]) OK shape={tuple(out.shape)} -> take [...,0]")
