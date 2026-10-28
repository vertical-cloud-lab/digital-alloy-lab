"""Reproduce local constrained full-truth immersion-floor searches.
Run: python outputs/reproduce_full_truth.py [input_directory]
Requires torch and botorch; does not change uploaded inputs.
These middle-Al-branch multistart solutions are NOT global certificates.
"""
from pathlib import Path
import sys,os,json,time
import numpy as np
import torch
from scipy.optimize import minimize
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT));os.environ['BOFN_TRUTH']='toy'
import bofn_alloy as BA
import truth_phys as TP
TP.GRID_CSV=ROOT/'calphad_grid.csv';TP.FIT_JSON=ROOT/'corrosion_fit.json'
TP._GRID=None;TP._FIT=None
torch.set_num_threads(2)
truth=TP.PhysTruth(m_ref=0.)
pt=json.loads((ROOT/'phys_tables.json').read_text())
REF=['C70600','C71500']
names=['C70600 (90-10 Cu-Ni)','C71500 (70-30 Cu-Ni)']
refs={b:TP.reference_m(n) for b,n in zip(REF,names)}
class EvalTruth:
 def __init__(self,bar,beta_mult=1.,porosity_mult=1.):self.bar=bar;self.beta_mult=beta_mult;self.porosity_mult=porosity_mult
 def fun(self,x):
  t=torch.tensor(x);o=truth.full(t)
  m=(TP.M_LEVEL-TP.SLOPE*TP.ln_rate(t[:4])-.60*t[1]*o['beta']*self.beta_mult-.30*(1-o['rho_m'])*self.porosity_mult)
  return np.array([float(m)-self.bar, (35.-float((t[:4]*TP.WT_MAX).sum()))/35.,(1250.-float(TP.field(t[:4],'liquidus_C')))/100.])

def full_floor(bar,starts=6,beta_mult=1.,porosity_mult=1.,seed=12):
 ev=EvalTruth(bar,beta_mult,porosity_mult);sols=[]
 # The relevant low-floor branch has 1.5 <= Al <= 7; these local results are not global certificates.
 bounds=[(0,1),(1.5/9.5,7/9.5),(0,1),(0,1),(0,1),(0,1),(0,1)]
 rng=np.random.default_rng(seed)
 x0s=[np.array(pt['immersion'][b]['witness']['x']) for b in ['9010','7030']]
 for j in range(starts-2):
  x=x0s[j%2].copy();x[:4]+=rng.normal(0,.08,4);x[4:]+=rng.normal(0,.04,3)
  x=np.clip(x,np.array(bounds)[:,0],np.array(bounds)[:,1]);x0s.append(x)
 for x0 in x0s:
  r=minimize(lambda x:x[0]*30,x0,jac=lambda x:np.array([30.,0,0,0,0,0,0]),method='SLSQP',bounds=bounds,constraints=[{'type':'ineq','fun':ev.fun}],options={'maxiter':200,'ftol':1e-10})
  if r.success and ev.fun(r.x).min()>-1e-7:sols.append(r)
 if not sols:return {'failed':True}
 r=min(sols,key=lambda r:r.fun);xx=torch.tensor(r.x);o=truth.full(xx)
 return {'ni':r.fun,'x':r.x.tolist(),'wt':TP.wt(xx).tolist(),'m_original':float(o['m']),'rho':float(o['rho_m']),'beta':float(o['beta']),'constraint_margin':ev.fun(r.x).tolist(),'successes':len(sols),'local_ni_values':[float(s.fun) for s in sols]}
result={b:full_floor(refs[b][0],starts=6) for b in REF}
for b in REF:
 c=torch.tensor(BA.REFERENCE[names[REF.index(b)]])
 dense=float(TP.M_LEVEL-TP.SLOPE*TP.ln_rate(c))
 result[b+'_ideal_dense_ref']=full_floor(dense,starts=3)
for label,bm,pm in [('No beta penalty',0,1),('Double beta penalty',2,1),('No porosity penalty',1,0),('Double porosity penalty',1,2)]:
 result[label]={b:full_floor(refs[b][0],starts=3,beta_mult=bm,porosity_mult=pm) for b in REF}
out=ROOT/'outputs'/'reproduction';out.mkdir(parents=True,exist_ok=True)
(out/'full_truth_optimizations.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
