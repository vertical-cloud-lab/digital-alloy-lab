"""Fit the film corrosion model of the physics-based truth to same-test seawater data, and test how
robust the resulting nickel floor is.

    python phys/fit_corrosion.py      # writes phys/corrosion_fit.json and phys/corrosion_fit.md

Data: phys/corrosion_data.csv, one row per alloy per study (rates as reported; only within-study
ratios are used, so units and absolute levels cancel). Model:

    ln rate_ij = a_i + b_Ni film(Ni_j) + b_Al Al_j + b_Al2 Al_j^2 + b_Fe min(Fe_j, FE_SOL)

with a separate intercept a_i per study, film(Ni) = 1 - exp(-Ni / NI_SCALE) (the protective film
saturates, as the 90-10 / 70-30 comparisons show), compositions in wt%. The quadratic in Al lets a
little Al help (the alumina-rich film of single-phase aluminum bronze) and a lot hurt (the duplex
beta/kappa microstructures of NAB, attacked selectively), which a linear term cannot do: on these data
it made Ni look harmful. Weighted least squares with a weak ridge on the slopes, and the signs that the
film mechanism fixes: nickel and iron in solution can only lower the rate (b_Ni <= 0, b_Fe <= 0).
Mn is not in the model: the immersion node of the network does not see Mn.

The nickel floor is the lowest Ni (wt%) at which some composition inside the proposal's limits is
predicted to corrode no faster than the bar alloy (dense 90-10 or 70-30 Cu-Ni), deposited dense and
free of beta-prime. It is computed on a fine (Ni, Al, Fe) grid at the Mn that minimises the liquidus,
for the base fit and for a set of defensible alternative fits.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
DATA = HERE / "corrosion_data.csv"
OUT = HERE / "corrosion_fit.json"
BASE = {"ni_form": "sat", "ni_scale": 5.0, "fe_sol": 1.5, "ridge": 0.05, "al_form": "quad", "signs": True}
REF_WT = {"C70600": (10.0, 0.0, 1.4), "C71500": (30.0, 0.0, 0.6)}  # Ni, Al, Fe (wt%) of the bars, as in bofn_alloy.REFERENCE


def load(path=DATA):
    rows = []
    for r in csv.DictReader(open(path)):
        if r.get("use", "1").strip() in ("0", "no"):
            continue
        rows.append({"study": r["study"], "alloy": r["alloy"], "ni": float(r["ni"]), "al": float(r["al"]), "fe": float(r["fe"]),
                     "mn": float(r.get("mn") or 0), "rate": float(r["rate"]), "w": float(r.get("weight") or 1.0)})
    return rows


def features(ni, al, fe, cfg):
    """Columns: film(Ni), Al, Al^2 / 10 (zero for the linear-Al variant), Fe in solution."""
    ni, al, fe = (np.asarray(v, dtype=float) for v in (ni, al, fe))
    film = 1 - np.exp(-ni / cfg["ni_scale"]) if cfg["ni_form"] == "sat" else ni / 10.0
    al2 = al**2 / 10.0 if cfg.get("al_form", "quad") == "quad" else np.zeros_like(al)
    return np.stack([film, al, al2, np.minimum(fe, cfg["fe_sol"])], -1)


def fit(rows, cfg=BASE):
    studies = sorted({r["study"] for r in rows})
    X = features([r["ni"] for r in rows], [r["al"] for r in rows], [r["fe"] for r in rows], cfg)
    S = np.array([[1.0 if r["study"] == s else 0.0 for s in studies] for r in rows])
    y = np.log([r["rate"] for r in rows])
    w = np.sqrt([r["w"] for r in rows])
    A = np.concatenate([X, S], 1) * w[:, None]
    b = y * w
    from scipy.optimize import lsq_linear

    lam = cfg["ridge"]
    k = X.shape[1]
    # ridge as extra rows (no penalty on the study intercepts); bounds for the film signs
    A2 = np.concatenate([A, np.concatenate([np.sqrt(lam) * np.eye(k), np.zeros((k, len(studies)))], 1)])
    b2 = np.concatenate([b, np.zeros(k)])
    lo = np.full(k + len(studies), -np.inf)
    hi = np.full(k + len(studies), np.inf)
    if cfg.get("signs", True):
        hi[0], hi[3] = 0.0, 0.0  # nickel and iron in solution only help the film
    if cfg.get("al_form", "quad") != "quad":
        lo[2], hi[2] = -1e-12, 1e-12
    coef = lsq_linear(A2, b2, bounds=(lo, hi)).x
    pred = np.concatenate([X, S], 1) @ coef
    res = y - pred
    return {"coef": {"ni": float(coef[0]), "al": float(coef[1]), "al2": float(coef[2]), "fe": float(coef[3]), "mn": 0.0}, "intercepts": dict(zip(studies, map(float, coef[k:]))),
            "rmse_ln": float(np.sqrt(np.mean(res**2))), "n": len(rows), "n_studies": len(studies), **cfg,
            "residuals": [{"study": r["study"], "alloy": r["alloy"], "ln_obs": float(yy), "ln_fit": float(pp)} for r, yy, pp in zip(rows, y, pred)]}


def ln_rate(f, ni, al, fe):
    c = f["coef"]
    F = features(ni, al, fe, f)
    return c["ni"] * F[..., 0] + c["al"] * F[..., 1] + c.get("al2", 0.0) * F[..., 2] + c["fe"] * F[..., 3]


def floor(f, bar, feasible=None):
    """Lowest Ni (wt%) with some (Al, Fe) inside the limits predicted no worse than the bar alloy."""
    ni = np.linspace(0, 30, 301)
    al = np.linspace(0, 9.5, 96)
    fe = np.linspace(0, 4.5, 46)
    N, A, F = np.meshgrid(ni, al, fe, indexing="ij")
    target = ln_rate(f, *REF_WT[bar])
    ok = ln_rate(f, N, A, F) <= target + 1e-12
    if feasible is not None:
        ok &= feasible(N, A, F)
    hit = ok.any(axis=(1, 2))
    if not hit.any():
        return None, None
    i = int(np.argmax(hit))
    j, k = np.argwhere(ok[i])[0]
    return float(ni[i]), {"ni": float(ni[i]), "al": float(al[j]), "fe": float(fe[k])}


def feasible_fn():
    """The proposal's limits on (Ni, Al, Fe) in wt%, at the Mn that keeps the liquidus lowest (Mn = 0 here,
    which is what the immersion node sees)."""
    sys.path.insert(0, str(HERE.parent))
    import torch

    import truth_phys as TP

    def ok(N, A, F):
        c = torch.tensor(np.stack([N / 30.0, A / 9.5, F / 4.5, np.zeros_like(N)], -1))
        return TP.feasible(c).numpy()

    return ok


VARIANTS = {
    "base: saturating film (Ni scale 5 wt%), quadratic Al, signs fixed": {},
    "linear Al": {"al_form": "lin"},
    "signs free": {"signs": False},
    "linear Al, signs free (the first form tried)": {"al_form": "lin", "signs": False},
    "Ni scale 3 wt%": {"ni_scale": 3.0},
    "Ni scale 8 wt%": {"ni_scale": 8.0},
    "Ni scale 12 wt%": {"ni_scale": 12.0},
    "linear Ni": {"ni_form": "lin"},
    "Fe in solution up to 1.0 wt%": {"fe_sol": 1.0},
    "Fe in solution up to 2.5 wt%": {"fe_sol": 2.5},
    "no ridge": {"ridge": 1e-6},
    "strong ridge (0.5)": {"ridge": 0.5},
    "equal weights": {"_equal_weights": True},
}


def base_floors(out):
    f = out["floors"]
    return ", ".join(f"{'90-10' if b == 'C70600' else '70-30'} bar {('none passes' if v[0] is None else f'{v[0]:.1f} wt% Ni')}" + ("" if v[1] is None else f" (witness Ni {v[1]['ni']:.1f}, Al {v[1]['al']:.1f}, Fe {v[1]['fe']:.1f})") for b, v in f.items())


def main():
    rows = load()
    feas = feasible_fn()
    base = fit(rows)
    out = {"base": base, "floors": {}, "variants": {}}
    for bar in REF_WT:
        out["floors"][bar] = floor(base, bar, feas)
    studies = sorted({r["study"] for r in rows})
    variants = dict(VARIANTS)
    for s in studies:
        variants[f"without {s}"] = {"_drop": s}
    for name, v in variants.items():
        cfg = {**BASE, **{k: x for k, x in v.items() if not k.startswith("_")}}
        rr = [r for r in rows if r["study"] != v.get("_drop")]
        if v.get("_equal_weights"):
            rr = [{**r, "w": 1.0} for r in rr]
        if len({r["study"] for r in rr}) == 0:
            continue
        f = fit(rr, cfg)
        out["variants"][name] = {"coef": f["coef"], "rmse_ln": f["rmse_ln"], "n": f["n"],
                                 **{f"floor_{bar}": floor(f, bar, feas)[0] for bar in REF_WT}}
    OUT.write_text(json.dumps({**base, "floors": out["floors"], "variants": out["variants"]}, indent=1))
    L = ["# Film corrosion model: fit and nickel floor (written by `phys/fit_corrosion.py`)", "",
         f"{base['n']} rates from {base['n_studies']} studies; ln(rate) RMSE {base['rmse_ln']:.2f}. Coefficients per wt% (Ni through the film term): "
         + ", ".join(f"{k} {v:+.3f}" for k, v in base["coef"].items() if k != "mn") + f" (Al2 multiplies Al^2/10). Floors of the base fit: {base_floors(out)}.", "",
         "| Fit | b_Ni (film) | b_Al | b_Al2 (per Al^2/10) | b_Fe | RMSE (ln) | Ni floor, 90-10 bar (wt%) | Ni floor, 70-30 bar (wt%) |", "|---|---|---|---|---|---|---|---|"]
    fmt = lambda x: "none passes" if x is None else f"{x:.1f}"
    for name, v in out["variants"].items():
        L.append(f"| {name} | {v['coef']['ni']:+.2f} | {v['coef']['al']:+.3f} | {v['coef'].get('al2', 0):+.3f} | {v['coef']['fe']:+.3f} | {v['rmse_ln']:.2f} | {fmt(v['floor_C70600'])} | {fmt(v['floor_C71500'])} |")
    fl = [v[f"floor_{b}"] for v in out["variants"].values() for b in ("C70600",) if v[f"floor_{b}"] is not None]
    fl7 = [v["floor_C71500"] for v in out["variants"].values() if v["floor_C71500"] is not None]
    L += ["", f"Across these fits the floor ranges from {fmt(min(fl) if fl else None)} to {fmt(max(fl) if fl else None)} wt% Ni with the 90-10 bar "
          f"and from {fmt(min(fl7) if fl7 else None)} to {fmt(max(fl7) if fl7 else None)} wt% with the 70-30 bar.", "",
          "Residuals of the base fit (ln rate, observed vs fitted, within each study's own intercept):", "", "| Study | Alloy | ln observed | ln fitted |", "|---|---|---|---|"]
    for r in base["residuals"]:
        L.append(f"| {r['study']} | {r['alloy']} | {r['ln_obs']:+.2f} | {r['ln_fit']:+.2f} |")
    (HERE / "corrosion_fit.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
