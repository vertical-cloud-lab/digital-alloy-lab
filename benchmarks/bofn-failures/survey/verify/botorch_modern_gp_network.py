"""Minimal modern (BoTorch>=0.11, tested 0.18.1) GP-network posterior: root nodes use
rsample_from_base_samples(sample_shape, base[..., k]) (no trailing dim); child nodes condition on
parent samples, drawing one joint sample per MC path."""
import warnings, torch
from botorch.models import SingleTaskGP
from botorch.models.model import Model
from botorch.posteriors import Posterior
from botorch.sampling.get_sampler import GetSampler
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.acquisition.logei import qLogExpectedImprovement
from botorch.acquisition.objective import GenericMCObjective
from botorch.optim import optimize_acqf
warnings.filterwarnings("ignore")
torch.manual_seed(0)

class NetworkPosterior(Posterior):
    def __init__(self, node_models, parents, X):
        self.node_models, self.parents, self.X = node_models, parents, X
        self.n = len(node_models)
    device = property(lambda self: self.X.device)
    dtype = property(lambda self: self.X.dtype)
    @property
    def base_sample_shape(self):            # one N(0,1) per (batch, q, node)
        return self.X.shape[:-1] + torch.Size([self.n])
    @property
    def batch_range(self):                  # t-batch dims are everything before (q, node)
        return (0, -2)
    def _extended_shape(self, sample_shape=torch.Size()):
        return sample_shape + self.X.shape[:-1] + torch.Size([self.n])
    def rsample(self, sample_shape=None):
        sample_shape = sample_shape or torch.Size([1])
        base = torch.randn(sample_shape + self.base_sample_shape, dtype=self.dtype, device=self.device)
        return self.rsample_from_base_samples(sample_shape, base)
    def rsample_from_base_samples(self, sample_shape, base_samples):
        out = []
        for k, m in enumerate(self.node_models):
            if not self.parents[k]:          # root node: GPyTorchPosterior expects sample_shape x batch x q
                post = m.posterior(self.X)
                out.append(post.rsample_from_base_samples(sample_shape, base_samples[..., k])[..., 0])
            else:                            # child: inputs differ per MC path -> sample dims become batch dims
                par = torch.stack([out[j] for j in self.parents[k]], dim=-1)
                Xk = torch.cat([self.X.expand(*sample_shape, *self.X.shape), par], dim=-1)
                post = m.posterior(Xk)       # batch_shape = sample_shape x batch
                eps = base_samples[..., k].unsqueeze(0)   # one joint draw per path: 1 x sample_shape x batch x q
                out.append(post.rsample_from_base_samples(torch.Size([1]), eps)[0, ..., 0])
        return torch.stack(out, dim=-1)

@GetSampler.register(NetworkPosterior)
def _get_sampler_network(posterior, sample_shape, *, seed=None):
    return SobolQMCNormalSampler(sample_shape=sample_shape, seed=seed)

class GPNetwork(Model):
    def __init__(self, node_models, parents):
        super().__init__(); self.node_models = torch.nn.ModuleList(node_models); self.parents = parents
    num_outputs = property(lambda self: len(self.node_models))
    def posterior(self, X, output_indices=None, observation_noise=False, posterior_transform=None):
        return NetworkPosterior(list(self.node_models), self.parents, X)

# two-stage toy: y1 = f1(x), y2 = f2(x, y1); maximize y2
X = torch.rand(15, 2, dtype=torch.double)
y1 = torch.sin(3 * X[:, :1]); y2 = -(y1 - 0.3) ** 2 + 0.1 * X[:, 1:]
net = GPNetwork([SingleTaskGP(X, y1), SingleTaskGP(torch.cat([X, y1], -1), y2)], parents=[[], [0]])
for m in net.node_models: m.eval()
acqf = qLogExpectedImprovement(net, best_f=y2.max(), objective=GenericMCObjective(lambda Z, X=None: Z[..., -1]))
for q in (1, 3):
    cand, val = optimize_acqf(acqf, bounds=torch.tensor([[0., 0.], [1., 1.]], dtype=torch.double), q=q,
                              num_restarts=4, raw_samples=64)
    print(f"q={q}: optimize_acqf OK, candidate shape {tuple(cand.shape)}, log-acq {val.item():.3f}")
s = net.posterior(torch.rand(4, 3, 2, dtype=torch.double))
print("sample shape", tuple(SobolQMCNormalSampler(torch.Size([8]))(s).shape))
