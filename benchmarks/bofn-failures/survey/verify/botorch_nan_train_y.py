"""Does SingleTaskGP (BoTorch 0.18.1) accept NaN in train_Y? And ModelListGP with per-output training sets?"""
import warnings, torch
from botorch.models import SingleTaskGP, ModelListGP
warnings.filterwarnings("ignore")
X = torch.rand(6, 2, dtype=torch.double); Y = X.sum(-1, keepdim=True); Y[2] = float("nan")
try:
    SingleTaskGP(X, Y); print("SingleTaskGP with NaN Y: accepted")
except Exception as e:
    print("SingleTaskGP with NaN Y:", type(e).__name__, str(e)[:80])
ok = ~Y.isnan().squeeze(-1)
m = ModelListGP(SingleTaskGP(X[ok], Y[ok]), SingleTaskGP(X, X[:, :1]))  # per-output training sets (5 vs 6 points)
print("ModelListGP per-output training sets:", [tuple(mm.train_inputs[0].shape) for mm in m.models],
      "posterior event shape", tuple(m.posterior(torch.rand(3, 2, dtype=torch.double)).mean.shape))
