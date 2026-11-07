"""HTMDEC: running hypervolume of the 5-iteration BBO run vs. a random-batch baseline and the full-space optimum.
Usage: python HTMDEC-convergence.py <bbo_python_dir> <out_csv> <out_png>
Imports the repo's own pareto_maximum/hypervolume from package_BBO_functions in <bbo_python_dir>."""
import sys, os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
d, out_csv, out_png = sys.argv[1:4]
sys.path.insert(0, d); os.chdir(d)
from package_BBO_functions import import_excel, pareto_maximum, hypervolume
outputs = ['PROP RT Density (g/cm3)', 'PROP RT Heat Cap (J/(mol K))']
space = import_excel('compositionSpace_htmdec_1000_withtype.xlsx')
run = import_excel('Test Optimization Iteration/testBOloop_specificmetadata/inputSpace_from1000_size20_iter6.xlsx')
its = sorted(run['Iteration'].unique())
bo = [hypervolume(pareto_maximum(run[run['Iteration'] <= k][outputs].to_numpy())) for k in its]
hv_all = hypervolume(pareto_maximum(space[outputs].to_numpy()))
init = run[run['Iteration'] == its[0]]
rng = np.random.default_rng(0)
key = [c for c in space.columns if c in run.columns and c not in outputs + ['Iteration', 'Alloy', 'hypervolume']]
mask = ~space.set_index(key).index.isin(init.set_index(key).index)
pool = space[mask][outputs].to_numpy()
rand = []
for s in range(30):
    idx = rng.permutation(len(pool))
    hv = [hypervolume(pareto_maximum(init[outputs].to_numpy()))]
    for k in range(1, len(its)):
        pts = np.vstack([init[outputs].to_numpy(), pool[idx[:20 * k]]])
        hv.append(hypervolume(pareto_maximum(pts)))
    rand.append(hv)
rand = np.array(rand)
df = pd.DataFrame({'iteration': its, 'bo_hv': bo, 'random_hv_mean': rand.mean(0), 'random_hv_std': rand.std(0),
                   'full_space_hv': hv_all, 'n_evaluated': [20 * k for k in its]})
df.to_csv(out_csv, index=False); print(df.to_string(index=False))
fig, ax = plt.subplots(figsize=(5.5, 3.8))
ax.plot(its, bo, 'o-', label='BBO (repo, 100 GPs, batch 20)')
ax.errorbar(its, rand.mean(0), yerr=rand.std(0), fmt='s--', capsize=3, label='random batches (30 seeds)')
ax.axhline(hv_all, color='k', lw=0.8, ls=':', label='full-space Pareto HV')
ax.set_xlabel('iteration (20 alloys each)'); ax.set_ylabel('hypervolume (density, heat cap.)')
ax.set_title('HTMDEC bbo_python on 1000-alloy space'); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(out_png, dpi=110)
