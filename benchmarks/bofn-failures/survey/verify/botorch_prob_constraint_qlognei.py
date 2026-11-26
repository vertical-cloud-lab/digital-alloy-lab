"""Check how qLogNEI's incumbent/pruning treats a probability-valued (fat=None) constraint on BoTorch 0.18.1."""
import warnings, torch, botorch
from botorch.models import SingleTaskGP, ModelListGP
from botorch.acquisition.logei import qLogNoisyExpectedImprovement, qLogExpectedImprovement
from botorch.acquisition.utils import compute_feasibility_indicator
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.acquisition.objective import GenericMCObjective
torch.manual_seed(0)
X = torch.rand(12, 2, dtype=torch.double)
y_obj = (X ** 2).sum(-1, keepdim=True)
latent_con = 3.0 * (X[:, :1] - 0.5)   # positive => feasible (prob > 0.5)
model = ModelListGP(SingleTaskGP(X, y_obj), SingleTaskGP(X, latent_con)).eval()
prob_feasible = lambda Z, X=None: torch.sigmoid(Z[..., 1])   # classifier-style: returns P(feasible)
print("botorch", botorch.__version__)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    acqf = qLogNoisyExpectedImprovement(model=model, X_baseline=X, constraints=[prob_feasible], fat=[None],
                                        objective=GenericMCObjective(lambda Z, X=None: Z[..., 0]), prune_baseline=True,
                                        sampler=SobolQMCNormalSampler(torch.Size([128])))
    acqf(torch.rand(5, 1, 2, dtype=torch.double))
    msgs = sorted({str(x.message)[:110] for x in w if "infeasible" in str(x.message).lower()})
print("warnings mentioning infeasible:", msgs)
samples = model.posterior(X).rsample(torch.Size([64]))
hard = compute_feasibility_indicator([prob_feasible], samples)
print("fraction of baseline sample-points counted feasible by compute_feasibility_indicator:",
      round(hard.double().mean().item(), 3), "(true P>0.5 fraction ~", round((latent_con > 0).double().mean().item(), 2), ")")
print("baseline kept after pruning:", acqf.X_baseline.shape[0], "of", X.shape[0])

# Workaround on 0.18.1: pass the classifier's logit as a sigmoid constraint, c = -logit(p), eta=1, fat=[False]
neg_logit = lambda Z, X=None: -Z[..., 1]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    acqf2 = qLogNoisyExpectedImprovement(model=model, X_baseline=X, constraints=[neg_logit], eta=1.0, fat=[False],
                                         objective=GenericMCObjective(lambda Z, X=None: Z[..., 0]), prune_baseline=True,
                                         sampler=SobolQMCNormalSampler(torch.Size([128])))
    acqf2(torch.rand(5, 1, 2, dtype=torch.double))
    msgs = sorted({str(x.message)[:110] for x in w if "infeasible" in str(x.message).lower()})
from botorch.utils.objective import compute_smoothed_feasibility_indicator
s = model.posterior(X).rsample(torch.Size([4]))
same = torch.allclose(compute_smoothed_feasibility_indicator([neg_logit], s, eta=1.0, fat=[False]),
                      compute_smoothed_feasibility_indicator([prob_feasible], s, eta=1.0, fat=[None]))
print("logit trick: warnings:", msgs, "| soft indicator identical to fat=None probabilities:", same,
      "| hard-feasible fraction:", round(compute_feasibility_indicator([neg_logit], samples).double().mean().item(), 3),
      "| baseline kept:", acqf2.X_baseline.shape[0])
