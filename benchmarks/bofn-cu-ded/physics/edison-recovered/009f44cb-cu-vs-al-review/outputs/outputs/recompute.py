"""Independent JSON re-analysis. Run: python outputs/recompute.py /workspace"""
from pathlib import Path
import json,sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
root=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace')
out=root/'outputs'/'reproduced';out.mkdir(parents=True,exist_ok=True)
opt_a=json.loads((root/'al_optimum.json').read_text())['kappa1']
opt_c=next(x['optimum'] for x in json.loads((root/'truth_tables.json').read_text()) if (x['kappa'],x['eta'])==(1,1))
opt_n=next(x['optimum'] for x in json.loads((root/'landscape.json').read_text()) if 'no immersion' in x.get('truth',''))
paths={'Al':('k1',opt_a),'Cu':('results/k1e1',opt_c),'Cu-light':('quality/results-light/k1e1',opt_c),'No-gate':('compare/results-nogate/k1e1',opt_n)}
records=[];runs={}
for group,(folder,opt) in paths.items():
 for p in sorted((root/folder).glob('*.json')):
  r=json.loads(p.read_text());runs[(group,r['kind'],r['seed'])]=r
  assert all(b['spent']>=a['spent'] for a,b in zip(r['rows'],r['rows'][1:]))
  for budget in [0,25000,50000,100000]:
   row=[v for v in r['rows'] if v['spent']<=budget+1e-7][-1]
   records.append({'group':group,'policy':r['kind'],'seed':r['seed'],'budget':budget,'score':row['best_validated'],'pct':row['best_validated']/opt*100})
df=pd.DataFrame(records).sort_values(['group','policy','seed','budget'])
df.to_csv(out/'scores.csv',index=False)
agg=df.groupby(['group','policy','budget']).pct.agg(['count','mean','std'])
agg['sample_SEM']=agg['std']/np.sqrt(agg['count'])
agg['authors_SE']=agg['sample_SEM']*np.sqrt((agg['count']-1)/agg['count'])
agg.to_csv(out/'summary.csv')
paired=[]
for a,b in [('pkgfn','eifn'),('pkgfn','eifn_reuse'),('pkgfn','ei'),('pkgfn','random'),('pkgfn','tiered_ni_ref'),('tiered_ni_ref','tiered_ni'),('tiered_ni','tiered')]:
 for budget in [25000,50000,100000]:
  av=df[(df.group==('Cu-light' if a=='pkgfn' else 'Cu'))&(df.policy==a)&(df.budget==budget)].set_index('seed').pct
  bv=df[(df.group==('Cu-light' if b=='pkgfn' else 'Cu'))&(df.policy==b)&(df.budget==budget)].set_index('seed').pct
  ss=av.index.intersection(bv.index);d=(av.loc[ss]-bv.loc[ss]).values
  paired.append(dict(A=a,B=b,budget=budget,n=len(d),difference=d.mean(),wins=(d>0).sum(),ties=(d==0).sum(),losses=(d<0).sum(),p=wilcoxon(d).pvalue if np.any(d) else 1.))
pd.DataFrame(paired).to_csv(out/'paired.csv',index=False)
light={s:r for (g,k,s),r in runs.items() if g=='Cu-light' and k=='pkgfn'}
high={s:r for (g,k,s),r in runs.items() if g=='Cu' and k=='pkgfn'}
print('Fidelity overlap:',sorted(light.keys()&high.keys()),'; no matched test possible' if not high else '')
print(agg.loc[(slice(None),slice(None),100000),:].to_string())
