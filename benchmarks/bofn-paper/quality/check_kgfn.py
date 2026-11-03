"""Brute-force checks of the KGFN acquisition, Network.kg_full.

1. For a few candidate designs, every fantasy is redone by hand: push the
   fantasy normals down the chain, append each node's fantasized observation to
   that node's data (same hyperparameters and standardization), re-solve the GP
   exactly and sample the network on the inner set with the same base samples.
   The resulting KG must equal kg_full's, which uses closed-form rank-one updates.
2. KG is non-negative, and a design that has already been run through the
   whole chain is worth (almost) nothing to run again on noise-free data.

    python quality/check_kgfn.py [seed] [kappa]
"""

import os
import sys
import warnings

import torch

warnings.filterwarnings("ignore")
torch.set_num_threads(1)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bofn_alloy import COMP, D, IPV, LAMBDA, ORDER, SPEC, AlloyTruth, Network, TinyGP, burden, local_perturb, node_input, normal_qmc, sobol  # noqa: E402
from policies import eps_for, initial_data  # noqa: E402


def conditioned(gp, z, y_std):
    """`gp` with one more observation (input z, standardized value y_std), hyperparameters fixed."""
    g = object.__new__(TinyGP)
    g.ls, g.const, g.noise, g.ys, g.ym = gp.ls, gp.const, gp.noise, gp.ys, gp.ym
    X = torch.cat([gp.X, z.unsqueeze(0)])
    Y = torch.cat([(gp.y - gp.ym) / gp.ys, y_std.reshape(1)])
    n = X.shape[0]
    g.X, g.Xs = X, X / g.ls
    K = g._k(g.Xs, g.Xs) + (g.noise + 1e-8) * torch.eye(n)
    K[-1, -1] -= 1e-8  # the fantasy has noise variance g.noise exactly, as in kg_full
    L = torch.linalg.cholesky(K)
    g.Linv = torch.linalg.solve_triangular(L, torch.eye(n), upper=False)
    g.alpha = g.Linv.T @ (g.Linv @ (Y - g.const))
    return g


def kg_by_hand(net, x, Xi, eps, w, ww):
    nus = []
    for k in range(w.shape[0]):
        obs, gps = {}, {}
        for r, n in enumerate(ORDER):
            gp = net.gp[n]
            z = node_input(n, x.unsqueeze(0), {p: v.reshape(1) for p, v in obs.items()})[0]
            mz, vz = gp.post_std(z.unsqueeze(0))
            y_std = mz[0] + (vz[0] + gp.noise).sqrt() * w[k, r]
            obs[n] = y_std * gp.ys + gp.ym
            gps[n] = conditioned(gp, z, y_std)
        vals = {}
        xi = Xi.unsqueeze(-2)
        for n in ORDER:
            inp = node_input(n, xi, vals) if SPEC[n][1] else Xi[..., SPEC[n][0]].unsqueeze(-2).expand(-1, eps[n].shape[-1], -1)
            m, v = gps[n].post_std(inp)
            vals[n] = (m + v.sqrt() * eps[n]) * gps[n].ys + gps[n].ym
        nus.append((vals["U"] - LAMBDA * burden(Xi).unsqueeze(-1)).mean(-1))
    nu = torch.stack(nus)  # [nf, m]
    return float((nu.max(-1).values * ww).sum() - (nu * ww.unsqueeze(-1)).sum(0).max())


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    kappa = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    torch.manual_seed(seed)
    d, lab = initial_data(AlloyTruth(kappa), seed)
    g = torch.Generator().manual_seed(seed)
    for x in torch.rand(3, D, generator=g):  # a little more data: three more full chains and a lone print
        lab.full_eval(x)
    lab.print_(0, torch.rand(2, generator=g))
    net = Network(d)
    # inner-max set anchored on the incumbent, as in the policy (KG is exactly 0 when
    # one inner design wins under every fantasy, so the set needs rivals near the top)
    Xv = torch.stack([x for x, _ in d.full])
    pool = torch.cat([sobol(256, D, seed=seed), local_perturb(Xv, 16, 0.05, g)])
    nu = net.mean(pool, eps_for(pool.shape[0], 32, 5))
    top = pool[nu.argmax()]
    new = torch.rand(D, generator=g)
    near = top.clone()
    near[COMP] = (top[COMP] + 0.05 * torch.randn(len(COMP), generator=g)).clamp(0, 1)  # an alloy never simulated
    reprint = torch.cat([d.lots[1]["c"], torch.tensor([d.lots[1]["a"]]), top[IPV]])  # simulated alloy, model's best (P, v)
    done = d.full[-1][0]
    Xc = torch.stack([new, near, reprint, done])
    Xi = torch.cat([pool[nu.topk(16).indices], local_perturb(top.unsqueeze(0), 16, 0.03, g), Xc])
    eps = eps_for(Xi.shape[0], 32, 123)
    nf = 16
    w = normal_qmc((len(ORDER), nf), seed=0).T.contiguous()
    ww = torch.full((nf,), 1 / nf)
    fast = net.kg_full(Xc, Xi, eps, w, ww)
    hand = torch.tensor([kg_by_hand(net, x, Xi, eps, w, ww) for x in Xc])
    names = ("random new alloy", "new alloy next to the incumbent", "simulated alloy, incumbent's (P, v)", "design already run end to end")
    for name, f, h in zip(names, fast, hand):
        print(f"{name:36s} kg_full {float(f):.6e}  by hand {float(h):.6e}  |diff| {abs(float(f - h)):.1e}")
    assert torch.allclose(fast, hand, rtol=1e-6, atol=1e-9), "kg_full disagrees with brute force"
    assert int((hand > 1e-6).sum()) >= 2, "check is vacuous: too few candidates with positive KG"
    # more designs: non-negativity, and a finished design is worth ~nothing
    P = torch.cat([local_perturb(top.unsqueeze(0), 48, 0.08, g), sobol(16, D, seed=seed + 1), done.unsqueeze(0)])
    Xi2 = torch.cat([Xi, P])
    kg = net.kg_full(P, Xi2, eps_for(Xi2.shape[0], 64, 7), normal_qmc((len(ORDER), 32), seed=0).T.contiguous(), torch.full((32,), 1 / 32))
    print(f"64 designs (48 near the incumbent, 16 space-filling): KG min {float(kg[:-1].min()):.2e}, median {float(kg[:-1].median()):.2e}, "
          f"max {float(kg[:-1].max()):.2e}, positive for {int((kg[:-1] > 0).sum())}; finished design {float(kg[-1]):.2e}")
    assert float(kg.min()) >= -1e-12, "negative KG"
    assert float(kg[-1]) <= 1e-3 * float(kg.max()), "re-running a finished design should be worth ~nothing"
    print("ok")


if __name__ == "__main__":
    main()
