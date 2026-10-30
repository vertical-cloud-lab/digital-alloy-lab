from pathlib import Path
import os, sys, types, json, math, time
import numpy as np
import pandas as pd
import torch
from scipy.optimize import least_squares, minimize, differential_evolution
from scipy.interpolate import RegularGridInterpolator
from scipy.special import expit
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.chdir(ROOT)
torch.set_num_threads(4)
torch.set_default_dtype(torch.double)
import truth_phys as TP
BASE=TP.CAL.copy()
pkg=types.ModuleType("physics"); pkg.truth_phys=TP; sys.modules["physics"]=pkg
import calibrate_corrosion as CC
OUT=ROOT/"review"


fields=TP.Grid.FIELDS
V=np.stack([TP.grid().V[k].numpy() for k in fields],axis=-1)
interp=RegularGridInterpolator([TP.AXES[k] for k in ["NI","AL","FE","MN"]],V,bounds_error=False,fill_value=None)
FIDX={k:i for i,k in enumerate(fields)}
maxwt=TP.WT_MAX.numpy()
alloys=CC.ALLOY.copy();alloys["Yang2018"]=(7,3,1,1);alloys["YangControl"]=(10,0,1,1)
kn=list(alloys);kid={k:i for i,k in enumerate(kn)}
target=np.array([1.4,3,2.1,3.1,.7,.36,.18,92.4/11.7,55/11.7,44.2/11.7,29/11.7,37/11.7,2])
weights=np.array([1,1,1,1,.7,.7,.7,.5,.5,.5,.5,.5,.7])
lo=np.array([.05,.05,.05,.05,.25*CC.DAY,1e5,.05]);hi=np.array([1.5]*4+[10*CC.DAY,1e9,10])
pbase=np.array([BASE[k] for k in CC.NAMES])
TT=TP.TGRID.numpy()
bounds=[(0,30),(0,9.5),(0,4.5),(0,4),(0,1),(0,1)]
refx={a:TP.reference_m_for(a)[2].numpy() for a in ["C71500","C70600"]}


def np_features(wt,mode='900',ni_shape='linear'):
 wt=np.atleast_2d(wt); vals=interp(wt)
 if mode=='nominal': a=wt.copy()
 else:
  a=np.minimum(wt,np.maximum(vals[:,[FIDX['a'+mode+'_'+e] for e in ['NI','AL','FE','MN']]],0))
 ni=a[:,0]/30
 if ni_shape=='sat10': ni=(1-np.exp(-a[:,0]/10))/(1-np.exp(-3))
 if ni_shape=='sat5': ni=(1-np.exp(-a[:,0]/5))/(1-np.exp(-6))
 return np.array([a[:,1]/7,ni,np.minimum(a[:,2],1.5)/1.5]).T


old_np_features=np_features


def np_features(wt,mode='900',ni_shape='linear'):
 if 'cap' not in mode:return old_np_features(wt,mode,ni_shape)
 mat,cap=mode.split('cap');cap=float(cap);wt=np.atleast_2d(wt);f=old_np_features(wt,mat,ni_shape)
 vv=interp(wt);a=np.minimum(wt[:,2],np.maximum(vv[:,FIDX['a'+mat+'_FE']],0))
 f[:,2]=np.minimum(a,cap)/1.5
 return f


def av_vector(p,t0,t1,features):
 t0=max(t0,1);t=np.logspace(np.log10(t0),np.log10(t1),200)
 fast=p[0]*features[:,0]+p[1]*features[:,1];slow=p[2]*features[:,1]+p[3]*features[:,2]
 q=10**(-fast[:,None]-slow[:,None]*(1-np.exp(-t/p[4])))
 cur=1/(1/30+1/np.sqrt(p[5]*q/(2*t)))+p[6]*q
 return np.trapezoid(cur,t,axis=-1)/(t1-t0)


def predictions(p,features):
 m=av_vector(p,0,30*CC.DAY,features); a=av_vector(p,0,60*CC.DAY,features)
 e=av_vector(p,0,5*CC.DAY,features);l=av_vector(p,16*CC.DAY,78*CC.DAY,features)
 get=lambda arr,k: arr[kid[k]]
 f=p[0]*features[:,0]+p[1]*features[:,1];s=p[2]*features[:,1]+p[3]*features[:,2]
 q=10**(-f-s*(1-np.exp(-7200/p[4])))
 i=1/(1/30+1/np.sqrt(p[5]*q/(2*7200)))+p[6]*q
 return np.array([get(m,'C70600')/get(m,'C71500'),get(m,'Cu')/get(m,'C71500'),get(m,'C61400')/get(m,'C71500'), get(a,'Cu10Ni0Fe')/get(a,'Cu10Ni1.5Fe'),*[get(l,k)/get(e,k) for k in ['Cu','Cu20Ni','Cu30Ni']],*[get(i,k) for k in ['Cu','Cu9.3Ni','Cu18.8Ni','Cu28.4Ni','Cu7Al']],get(m,'C71500')])


def fit_model(label,mode='900',shape='linear',target_=None,weights_=None,lo_=None,hi_=None,fix=None,yang=False):
 ft=np_features(list(alloys.values()),mode,shape)
 tar=target.copy() if target_ is None else target_; w=weights.copy() if weights_ is None else weights_
 lower=lo.copy() if lo_ is None else lo_; upper=hi.copy() if hi_ is None else hi_
 fix=fix or {}; free=[i for i in range(7) if i not in fix]
 def unpack(z):
  p=pbase.copy();p[free]=np.exp(z)
  for i,v in fix.items():p[i]=v
  return p
 def res(z):
  p=unpack(z);r=w*np.log(predictions(p,ft)/tar)
  if yang:
   a=av_vector(p,0,10*CC.DAY,ft);r=np.r_[r,np.log(a[kid['Yang2018']]/a[kid['C70600']]/.6)]
  return r
 best=None
 for start in [pbase,np.array(CC.X0)]:
  z=np.log(np.clip(start[free],lower[free]*1.00001,upper[free]/1.00001))
  rr=least_squares(res,z,bounds=(np.log(lower[free]),np.log(upper[free])),max_nfev=700,ftol=1e-10,xtol=1e-10,gtol=1e-9)
  if best is None or sum(rr.fun**2)<sum(best.fun**2):best=rr
 return {'label':label,'p':unpack(best.x),'loss':sum(best.fun**2),'mode':mode,'shape':shape,'pred':predictions(unpack(best.x),ft)}


def np_outputs(X,p=pbase,mode='900',shape='linear',cpor=1,isel=5,knuc=1):
 X=np.atleast_2d(X);wt=X[:,:4]*maxwt;v=interp(wt)
 get=lambda f:v[:,FIDX[f]]
 a7=v[:,[FIDX['a700_'+e] for e in ['NI','AL','FE','MN']]]
 a9=v[:,[FIDX['a900_'+e] for e in ['NI','AL','FE','MN']]]
 f=np.clip(get('sch_range99')/250,0,1);g=np.clip((get('sol1_kappa_fe')+get('sol1_fcc_feni'))/.05,0,1)
 moles=a9/np.array([TP.MW[e] for e in ['NI','AL','FE','MN']]);cu=(100-a9.sum(axis=-1))/TP.MW['CU']
 at=100*moles/(moles.sum(axis=-1)+cu)[:,None]
 conductivity=732/(1.7+at@np.array([1.1,.65,2,2.9]))+5
 h=.95*conductivity/TP.K_CU*(get('T_sol')-25)/(1084.6-25)
 q=np.exp(-((X[:,4]-(.35+.4*f))/.28)**2)*(1-.35*f*f)*(1-.1*X[:,3])
 P=X[:,5];vel=X[:,6];u=P-vel-(.05+.25*f)
 window=np.exp(-(u/.2)**2)*(1-.35*expit((P-.85)/.05))
 feff=f*(1-knuc*.85*g/(g+.12))
 rho=window*q**.3*(1-.75*expit((feff-.8)/.05))*(1-expit((h-P)/.08))
 beta=np.clip(get('beta_900'),0,1)*expit((vel-P+.2)/.15)
 feat=np_features(wt,mode,shape);fast=p[0]*feat[:,0]+p[1]*feat[:,1];slow=p[2]*feat[:,1]+p[3]*feat[:,2]
 film=10**(-fast[:,None]-slow[:,None]*(1-np.exp(-TT/p[4])))
 current=1/(1/30+1/np.sqrt(p[5]*film/(2*TT)))+p[6]*film
 M=(np.trapezoid(current,TT,axis=-1)/CC.DAY+30/CC.DAY+beta*isel*29)*(1+cpor*(1-rho))
 feas=(wt.sum(axis=-1)<=35+1e-9)&(get('T_liq')<=1250)&((wt[:,1]<=7)|(wt[:,0]>=wt[:,2]))&((wt[:,1]>=1.5)|(wt[:,2]<=2.3))
 return dict(M=M,rho=rho,beta=beta,feas=feas,f=f,g=g,h=h)


def candidate(z):
 wt=np.atleast_2d(z)[...,:4];vs=interp(wt);f=np.clip(vs[:,FIDX['sch_range99']]/250,0,1)
 return np.column_stack([wt/maxwt,.35+.4*f,np.atleast_2d(z)[:,4:6]])


def robust_floor(model,alloy,bar='deposited',extra=None,seed=73):
 p=model['p'];mode=model['mode'];shape=model['shape'];extra=extra or {}
 oo=np_outputs(refx[alloy],p,mode,shape,**extra); Mr=oo['M'][0]
 if bar=='wrought':Mr/=1+extra.get('cpor',1)*(1-oo['rho'][0])
 best=None
 for region in range(3):
  bb=bounds.copy()
  bb[1]=[(0,1.5),(1.5,7),(7,9.5)][region]
  if region==0:bb[2]=(0,2.3)
  def con(z):
   z=np.atleast_2d(z);o=np_outputs(candidate(z),p,mode,shape,**extra);vals=interp(z[:,:4])
   return np.column_stack([1-o['M']/Mr,(35-z[:,:4].sum(axis=1))/10,(1250-vals[:,FIDX['T_liq']])/100, (z[:,0]-z[:,2])/5 if region==2 else np.ones(len(z))])
  def obj(z):
   zs=np.atleast_2d(z.T) if np.ndim(z)==2 else np.atleast_2d(z)
   co=con(zs);a=zs[:,0]+1e5*np.square(np.minimum(co,0)).sum(axis=1)
   return a if np.ndim(z)==2 else a[0]
  de=differential_evolution(obj,bb,seed=seed,popsize=12,maxiter=170,tol=1e-8,polish=False,vectorized=True,updating='deferred')
  starts=[de.x,np.clip([15,3,1.5,0,.58,.48],*np.array(bb).T),np.clip([0,7,4.5,0,.6,.5],*np.array(bb).T)]
  for zz in starts:
   rr=minimize(lambda z:z[0],zz,bounds=bb,constraints=[{'type':'ineq','fun':lambda z:con(z)[0]}],method='SLSQP',options={'maxiter':250,'ftol':1e-10})
   if min(con(rr.x)[0])>=-1e-7 and (best is None or rr.fun<best.fun):best=rr
 if best is None:return {'floor':None,'barM':Mr}
 z=best.x; XX=candidate(z);oo=np_outputs(XX,p,mode,shape,**extra)
 return {'floor':z[0],'wt':z[:4].tolist(),'P':z[4],'v':z[5],'x':XX[0].tolist(),'barM':Mr,'M':oo['M'][0],'rho':oo['rho'][0],'beta':oo['beta'][0],'success':best.success}


def dense_floor(model,alloy,bar='deposited',extra=None,seed=73,dmin=.95):
 p=model['p'];mode=model['mode'];shape=model['shape'];extra=extra or {}
 oo=np_outputs(refx[alloy],p,mode,shape,**extra); Mr=oo['M'][0]
 if bar=='wrought':Mr/=1+extra.get('cpor',1)*(1-oo['rho'][0])
 best=None
 for region in range(3):
  bb=bounds.copy()
  bb[1]=[(0,1.5),(1.5,7),(7,9.5)][region]
  if region==0:bb[2]=(0,2.3)
  def con(z):
   z=np.atleast_2d(z);o=np_outputs(candidate(z),p,mode,shape,**extra);vals=interp(z[:,:4])
   return np.column_stack([1-o['M']/Mr,(35-z[:,:4].sum(axis=1))/10,(1250-vals[:,FIDX['T_liq']])/100, (z[:,0]-z[:,2])/5 if region==2 else np.ones(len(z)),o['rho']-dmin])
  def obj(z):
   zs=np.atleast_2d(z.T) if np.ndim(z)==2 else np.atleast_2d(z)
   co=con(zs);a=zs[:,0]+1e5*np.square(np.minimum(co,0)).sum(axis=1)
   return a if np.ndim(z)==2 else a[0]
  de=differential_evolution(obj,bb,seed=seed,popsize=12,maxiter=170,tol=1e-8,polish=False,vectorized=True,updating='deferred')
  starts=[de.x,np.clip([15,3,1.5,0,.58,.48],*np.array(bb).T),np.clip([0,7,4.5,0,.6,.5],*np.array(bb).T)]
  for zz in starts:
   rr=minimize(lambda z:z[0],zz,bounds=bb,constraints=[{'type':'ineq','fun':lambda z:con(z)[0]}],method='SLSQP',options={'maxiter':250,'ftol':1e-10})
   if min(con(rr.x)[0])>=-1e-7 and (best is None or rr.fun<best.fun):best=rr
 if best is None:return {'floor':None,'barM':Mr}
 z=best.x; XX=candidate(z);oo=np_outputs(XX,p,mode,shape,**extra)
 return {'floor':z[0],'wt':z[:4].tolist(),'P':z[4],'v':z[5],'x':XX[0].tolist(),'barM':Mr,'M':oo['M'][0],'rho':oo['rho'][0],'beta':oo['beta'][0],'success':best.success}


def fit_yang_matched():
 ft=np_features(list(alloys.values()))
 def res(z):
  p=np.exp(z);ar=av_vector(p,0,10*CC.DAY,ft)
  return np.r_[weights*np.log(predictions(p,ft)/target),np.log((ar[kid['Yang2018']]/ar[kid['YangControl']])/(.0215/.0359))]
 rr=least_squares(res,np.log(np.clip(pbase,lo*1.0001,hi/1.0001)),bounds=(np.log(lo),np.log(hi)),max_nfev=800,ftol=1e-11,xtol=1e-11,gtol=1e-9)
 return {'label':'Add Yang 2018, source-matched Fe1 Mn1 control','p':np.exp(rr.x),'loss':sum(rr.fun**2),'mode':'900','shape':'linear','pred':predictions(np.exp(rr.x),ft)}


def jsondefault(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,np.generic):return x.item()
 raise TypeError(type(x).__name__)



if __name__ == "__main__":
    m=fit_model("Original targets/bounds")
    print("Fitted constants",dict(zip(CC.NAMES,m["p"])))
    for a in refx:
        print(a,"refitted",robust_floor(m,a))
        print(a,"as supplied",robust_floor(dict(p=pbase,mode="900",shape="linear"),a))
        print(a,"wrought bar",robust_floor(dict(p=pbase,mode="900",shape="linear"),a,bar="wrought"))
