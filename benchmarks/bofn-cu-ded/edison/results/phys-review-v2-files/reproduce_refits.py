"""Independent film-model refit and continuous nickel-floor optimization.
Run: python outputs/reproduce_refits.py [input_directory]
No supplied fitting module is imported. Outputs go to outputs/reproduction/.
"""
from pathlib import Path
import sys, json
import numpy as np
import pandas as pd
from scipy.optimize import lsq_linear, minimize, brentq
from scipy.interpolate import RegularGridInterpolator
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
OUT=ROOT/'outputs'/'reproduction'; OUT.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(ROOT/'corrosion_data.csv')
BASE=dict(ni_scale=5.,ni_form='sat',al_form='quad',fe_sol=1.5,ridge=.05,signs=True)
REF={'C70600':np.array([10.,0.,1.4]),'C71500':np.array([30.,0.,.6])}
grid=pd.read_csv(ROOT/'calphad_grid.csv')
assert len(grid)==864 and (grid.ok==1).all()
axes=[np.sort(grid[c].unique()) for c in ['Ni_wt','Al_wt','Fe_wt','Mn_wt']]
L=RegularGridInterpolator(axes,grid.liquidus_C.fillna(1550).to_numpy().reshape(8,6,6,3),bounds_error=False,fill_value=None)


def feature(c,cfg):
 c=np.asarray(c); n,a,f=np.moveaxis(c,-1,0)
 return np.stack([(-np.expm1(-n/cfg['ni_scale']) if cfg['ni_form']=='sat' else n/10),a,(a*a/10 if cfg['al_form']=='quad' else np.zeros_like(a)),np.minimum(f,cfg['fe_sol'])],axis=-1)

def own_fit(data=df,**opts):
 cfg={**BASE,**opts}; X=feature(data[['ni','al','fe']].to_numpy(),cfg); y=np.log(data.rate.to_numpy()); w=data.weight.to_numpy()
 # Eliminate nuisance intercepts analytically using weighted within-study means.
 xc=X.copy(); yc=y.copy()
 for s in data.study.unique():
  ii=(data.study==s).to_numpy(); xc[ii]-=np.average(X[ii],axis=0,weights=w[ii]); yc[ii]-=np.average(y[ii],weights=w[ii])
 A=np.vstack([xc*np.sqrt(w[:,None]),np.sqrt(cfg['ridge'])*np.eye(4)]); z=np.r_[yc*np.sqrt(w),np.zeros(4)]
 hi=np.array([0,np.inf,np.inf,0]) if cfg['signs'] else np.full(4,np.inf)
 beta=lsq_linear(A,z,bounds=(-np.full(4,np.inf),hi),tol=1e-13,max_iter=500).x
 res=yc-xc@beta
 return dict(cfg=cfg,beta=beta,rmse=np.sqrt(np.mean(res**2)),n=len(data),rank=np.linalg.matrix_rank(xc),objective=float(sum(w*res**2)+cfg['ridge']*sum(beta**2)))

def score(f,c):return feature(c,f['cfg'])@f['beta']

def optimal_af(f):
 b=f['beta']; cand=[0.,9.5]
 if b[2]>1e-12: cand.append(np.clip(-5*b[1]/b[2],0,9.5))
 a=min(cand,key=lambda a:b[1]*a+b[2]*a*a/10)
 fe=f['cfg']['fe_sol'] if b[3]<-1e-9 else 0.
 return a,fe

def margins(c,mn=0):
 n,a,f=c
 return np.array([35-sum(c)-mn,1250-float(L([[n,a,f,mn]])[0]), (n-f if a>7+1e-9 else 100.),(2.3-f if a<1.5-1e-9 else 100.)])

def opt_floor(f,bar,mn=0):
 # Global unconstrained lower bound: exactly minimize separable Al and Fe terms,
 # then solve monotone Ni constraint; if its witness satisfies limits, it certifies the global floor.
 a,fe=optimal_af(f); target=score(f,REF[bar]); bn=f['beta'][0]
 def fun(n):return score(f,[n,a,fe])-target
 if fun(0)<=1e-10:n=0.
 elif bn<0 and fun(30)<=1e-10:n=brentq(fun,0,30,xtol=1e-12) if fun(30)<0 else 30.
 else:n=None
 if n is not None and min(margins([n,a,fe],mn))>=-1e-6:
  c=np.array([n,a,fe]);return dict(floor=n,witness=c.tolist(),mn=mn,liquidus=float(L([[*c,mn]])[0]),slack=float(target-score(f,c)),certificate='separable lower bound attained')
 # General fallback: optimize all continuous variables over each conditional branch.
 # Not needed for the base; report if used.
 sols=[]
 for amin,amax,fmax,couple in [(0,1.5,2.3,False),(1.5,7,4.5,False),(7,9.5,4.5,True)]:
  bounds=[(0,30),(amin,amax),(0,fmax)]
  def con(x):return np.r_[target-score(f,x),35-sum(x)-mn,1250-L([[*x,mn]])[0],x[0]-x[2] if couple else 100]
  for seed in range(10):
   rng=np.random.default_rng(seed);x0=np.array([rng.uniform(*bb) for bb in bounds])
   r=minimize(lambda x:x[0],x0,method='SLSQP',bounds=bounds,constraints=[{'type':'ineq','fun':con}],options={'ftol':1e-11,'maxiter':500})
   if r.success and min(con(r.x))>=-1e-7:sols.append(r)
 if not sols:return dict(floor=None,certificate='no feasible optimization result')
 r=min(sols,key=lambda s:s.fun);return dict(floor=r.fun,witness=r.x.tolist(),mn=mn,liquidus=float(L([[*r.x,mn]])[0]),slack=float(target-score(f,r.x)),certificate='multistart piecewise SLSQP')

specs=[('Base',{},df),('Linear Al',{'al_form':'lin'},df),('Signs free',{'signs':False},df),('Linear Al, signs free',{'al_form':'lin','signs':False},df),
 ('Ni scale 3',{'ni_scale':3},df),('Ni scale 8',{'ni_scale':8},df),('Ni scale 12',{'ni_scale':12},df),('Linear Ni',{'ni_form':'lin'},df),
 ('Fe cap 1.0',{'fe_sol':1},df),('Fe cap 2.5',{'fe_sol':2.5},df),('No ridge',{'ridge':0},df),('Ridge 0.5',{'ridge':.5},df),('Equal row weights',{},df.assign(weight=1.))]
for s in sorted(df.study.unique()):specs.append(('Drop '+s,{},df[df.study!=s]))
weak_new=['CohenWhitted1971','Wheatfall1967_123d','Wheatfall1967_surface']
specs += [('Drop hot brine + both Wheatfall blocks',{},df[~df.study.isin(weak_new)]),
 ('Drop unspecified bronze rows',{},df[~((df.study=='LewisLaQue1981_1y') & df.alloy.str.contains('generic'))]),
 ('Drop hot/deep/local + unspecified bronze + Zhao',{},df[~df.study.isin(weak_new+['Zhao2022']) & ~((df.study=='LewisLaQue1981_1y')&df.alloy.str.contains('generic'))]),
 ('Weight each study equally',{},df.assign(weight=df.weight/df.groupby('study').weight.transform('sum')))]
more=[]
for name,rates in [('Wheatfall1967_751d',(3.78,2.75)),('Wheatfall1967_1064d',(2.65,3.08))]:
 for ni,rate in zip([0.,30.],rates):
  row=df[(df.study=='Wheatfall1967_123d')&(df.ni==ni)].iloc[0].copy();row['study']=name;row['rate']=rate;more.append(row)
df_wheat=pd.concat([df,pd.DataFrame(more)],ignore_index=True)
prune=['Tan2024','Qian2025','Zhao2022','LewisLaQue1981_quiet',*weak_new]
dclean=df[~df.study.isin(prune)&~((df.study=='LewisLaQue1981_1y')&df.alloy.str.contains('generic'))]
extra_specs=[('Add omitted 751d + 1064d Wheatfall blocks',{},df_wheat),('Drop all Wheatfall exposures',{},df[~df.study.str.startswith('Wheatfall')]),('Exposure-rate only, conservative exclusions (9 rows)',{},dclean),('Same exclusions, no 10d Yang (7 rows)',{},dclean[dclean.study!='Yang2018'])]

specs+=extra_specs
results=[]
for name,opts,dat in specs:
 f=own_fit(dat,**opts)
 rr=dict(model=name,n=f['n'],rank=int(f['rank']),rmse_ln=float(f['rmse']),coef=f['beta'].tolist())
 for bar in REF:rr[bar]=opt_floor(f,bar)
 results.append(rr)
(OUT/'refits.json').write_text(json.dumps(results,indent=2))
print('Computed',len(results),'optimized scenarios')
for r in results:print(r['model'],r['C70600']['floor'],r['C71500']['floor'])
