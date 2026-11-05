"""Build stand-in per-iteration input files for BRAVE's code/bbo_python/main.py and
code/Probability_calculations/main.py. The real campaign files (o{1..5}_GT_y.csv, lhp.csv, tested_alloys.csv,
feasibles.csv, ...) are "available on request" and not in the repo, so this smoke test uses the Year-2 rows of
data/HTMDEC_Y2_db.xlsx as tested alloys and random compositions as the design space.
Usage: python -I BRAVE-make_inputs.py <xlsx> <bbo_dir> <prob_dir> <n_gp> <n_feas> <n_infeas> <n_space_prob>"""
import sys
import numpy as np
import pandas as pd

xlsx, bbo, prob = sys.argv[1:4]
n_gp, n_feas, n_inf, n_space = map(int, sys.argv[4:8])
rng = np.random.default_rng(0)
order = ["Al", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu"]
df = pd.read_excel(xlsx)
df = df[df["Year"] == 2].reset_index(drop=True)
X = df[order].to_numpy(float) / 100.0  # code expects fractions (YS_pb multiplies by 100)

def col(name, scale=1.0, sd=None):
    v = pd.to_numeric(df[name], errors="coerce")
    v = v.fillna(v.median()) * scale
    return v.to_numpy().reshape(-1, 1)

def sdcol(name, ref, scale=1.0, frac=0.1):
    if name is None:
        return np.abs(ref) * frac
    v = pd.to_numeric(df[name], errors="coerce") * scale
    v = v.fillna(pd.Series(np.abs(ref.ravel()) * frac))
    return v.to_numpy().reshape(-1, 1)

def save(a, path):
    pd.DataFrame(np.asarray(a)).to_csv(path, header=None, index=None)

y1 = col("Yield Strength (MPa)"); y1is = col("VarvYS pred(MPa) at 298K")
y2 = col("UTS/YS"); y3 = col("Elong_T (%)", 0.01); y4 = col("Avg HDYN/HQS"); y5 = col("Depth of Penetration (mm) FE_Sim")
for d in (bbo,):
    save(X, f"{d}/tested_alloys.csv")
    save(y1, f"{d}/o1_GT_y.csv"); save(sdcol("SD, YS", y1), f"{d}/o1_GT_sd.csv")
    save(y1is, f"{d}/o1_is1_y.csv"); save(np.full_like(y1is, 50.0), f"{d}/o1_is1_sd.csv")
    save(y2, f"{d}/o2_GT_y.csv"); save(sdcol("SD, UTS/YS", y2), f"{d}/o2_GT_sd.csv")
    save(y3, f"{d}/o3_GT_y.csv"); save(sdcol("SD, Elong%", y3, 0.01), f"{d}/o3_GT_sd.csv")
    save(y4, f"{d}/o4_GT_y.csv"); save(sdcol("Std, Hdyn/Hqs", y4), f"{d}/o4_GT_sd.csv")
    save(y5, f"{d}/o5_GT_y.csv"); save(sdcol(None, y5, frac=0.05), f"{d}/o5_GT_sd.csv")
    save(rng.uniform(0.1, 1.0, size=(n_gp, 8)), f"{d}/lhp.csv")

def rand_comps(n):
    # 5 at.% grid, up to 8 elements, sum to 1
    out = set()
    while len(out) < n:
        w = rng.dirichlet(np.ones(8) * 0.8)
        c = np.round(w * 20) / 20
        c[np.argmax(c)] += 1 - c.sum()
        if c.min() >= 0:
            out.add(tuple(np.round(c, 2)))
    return np.array(sorted(out))

space = rand_comps(n_feas + n_inf)
feas, inf = space[:n_feas], space[n_feas:]
save(feas, f"{bbo}/feasibles.csv"); save(inf, f"{bbo}/infeasibles.csv")
save(rng.uniform(0.5, 1.0, size=(n_inf, 1)), f"{bbo}/probs.csv")
save(space, f"{bbo}/x_test.csv")  # prior_eval.py input; main.py uses space = feasibles + infeasibles minus tested
# Probability_calculations inputs
big = rand_comps(n_space)
save(big[: n_space // 4], f"{prob}/feasibles.csv"); save(big, f"{prob}/all_space.csv"); save(X, f"{prob}/tested_alloys.csv")
print("tested", X.shape, "space", space.shape, "prob all_space", big.shape)
