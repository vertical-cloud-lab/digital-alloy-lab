from pathlib import Path
import sys,torch,numpy as np,pandas as pd
root=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace');sys.path.insert(0,str(root));out=root/'outputs'
import bofn_alloy as cu,policies as pol
torch.set_num_threads(1);tc=cu.AlloyTruth(1.,1.);shortlists={}
for s in range(20):
 d,l=pol.initial_data(tc,s);cs,*_=pol.calphad_shortlist(d,l,s);shortlists[('tiered',s)]=cs
# Certified rectangle bounds on P,v, with atomizer analytically maximized.
# Each factor uses its supremum/infimum over a cell; dependency is relaxed, so m_upper is conservative.
ed=np.linspace(0,1,129);pl,vl=np.meshgrid(ed[:-1],ed[:-1],indexing='ij');ph=pl+1/128;vh=vl+1/128
from scipy.special import expit
cert=[]
for seed in range(20):
 cs=shortlists[('tiered',seed)];f=tc.node('f',cs);gg=tc.node('g',cs)
 qmax=(1-.35*f**2)*(1-.10*cs[:,3]);crack=cu.sig((f*(1-.85*gg/(gg+.12))-cu.F_CRACK)/.05);pref=(qmax**.3*(1-.75*crack)).numpy()
 hh=tc.node('h',cs).numpy()
 for j,c in enumerate(cs):
  ni,alv,fe,mn=map(float,c);shift=.05+.25*float(f[j]);ulo=pl-vh-shift;uhi=ph-vl-shift;umin=np.where(ulo>0,ulo,np.where(uhi<0,-uhi,0))
  win_up=np.exp(-(umin/.2)**2)*(1-.35*expit((pl-.85)/.05));fusion_up=expit((ph-hh[j])/.08)
  rho_up=win_up*pref[j]*fusion_up;beta_lo=alv**1.5*(1-.5*ni)*expit((vl-ph+.2)/.15)
  const=.3+.55*(1-np.exp(-ni/.15))+.15*alv+.3*min(fe,.4)-.15*max(fe-.5,0)
  mup=const-.6*alv*beta_lo-.3*(1-rho_up)
  cert.append(dict(seed=seed,Ni=30*ni,m_upper=float(mup.max())))
print('Interval-certified m bound max',max(v['m_upper'] for v in cert),'non-excluding',sum(v['m_upper']>=cu.M_REF for v in cert))
pd.DataFrame(cert).to_csv(out/'shortlist_certified_immersion_bounds.csv',index=False)
