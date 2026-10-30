# Independent implementation, deliberately BEFORE reading or importing analyze.py.
# Plan: reconstruct right-continuous curves; summarize and pair by explicit seed IDs;
# bootstrap crossing ratios and fixed targets; then compare supplied code/tables;
# audit actions, budgets, validation completeness, sensitivities, and both PNGs.
OPT={(int(t['kappa']),int(t['eta'])):t['optimum'] for t in truth}
GRID=np.arange(0,100001,250,dtype=float)
runs=collections.defaultdict(dict)
for root,override in [('results',None),('quality/results-light','pkgfn_light')]:
 for p in sorted(Path(root).rglob('*.json')):
  r=json.loads(p.read_text());r['_path']=str(p)
  key=(int(r['kappa']),int(r['eta']),override or r['kind'])
  assert r['seed'] not in runs[key]
  runs[key][r['seed']]=r

def independent_curve(run,cell,metric='best_validated',grid=GRID):
 rows=run['rows']; spends=np.array([x['spent'] for x in rows],float)
 assert np.all(np.diff(spends)>=0)
 vals=np.array([x[metric] for x in rows],float)
 assert np.all(np.isfinite(vals))
 vals=np.maximum.accumulate(vals)
 # Shared initial observations are represented by the initial row (checked below).
 idx=np.searchsorted(spends,grid,side='right')-1
 return vals[np.maximum(idx,0)]/OPT[cell]*100

def crossing(curve,target):
 hits=np.flatnonzero(curve>=target)
 return GRID[hits[0]] if len(hits) else np.inf

curves={key:np.array([independent_curve(r,key[:2]) for s,r in sorted(v.items())]) for key,v in runs.items()}
seedids={key:np.array(sorted(v)) for key,v in runs.items()}
rows=[]
for key,a in curves.items():
 row={'cell':str(key[:2]),'policy':key[2],'n':len(a),'start':a[:,0].mean()}
 for b in [25000,50000,100000]:
  v=a[:,int(b/250)];row[f'mean{b}']=v.mean();row[f'se{b}']=st.sem(v) if len(v)>1 else np.nan
 for t in [60,70,80]:
  costs=np.array([crossing(c,t) for c in a]);row[f'median{t}']=np.median(costs);row[f'hit{t}']=np.isfinite(costs).mean()
 rows.append(row)
summary=pd.DataFrame(rows)
summary.to_csv(out/'independent_summary.csv',index=False)
print(summary.to_string(index=False,float_format=lambda x:f'{x:.5f}'))
print('Initial rows',collections.Counter((r['rows'][0]['spent'],r['rows'][0].get('action')) for v in runs.values() for r in v.values()))
