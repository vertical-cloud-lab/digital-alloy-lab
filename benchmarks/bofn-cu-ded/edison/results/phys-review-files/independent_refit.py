import numpy as np, pandas as pd, json
from pathlib import Path
from scipy.optimize import lsq_linear,minimize
from scipy.interpolate import RegularGridInterpolator
HERE=Path(__file__).resolve().parent
D=pd.read_csv(HERE.parent/'corrosion_data.csv');G=pd.read_csv(HERE.parent/'calphad_grid.csv')
axes=[np.linspace(0,30,8),np.linspace(0,9.5,6),np.linspace(0,4.5,6),np.array([0,2,4])]
liquidus=RegularGridInterpolator(axes,G.liquidus_C.fillna(1550).to_numpy().reshape(8,6,6,3),bounds_error=False,fill_value=None)
REFS={'9010':np.array([10.,0.,1.4,.8]),'7030':np.array([30.,0.,.6,.8])}
def features(dat, scale=5., linear=False, quadratic=True, fe_cap=1.5, mn=False, interaction=False):
    n,a,f,m=[np.asarray(dat[k],dtype=float) for k in ['ni','al','fe','mn']]
    X=[n/10 if linear else -np.expm1(-n/scale),a]; names=['ni','al']
    if quadratic: X.append(a*a/10); names.append('al2')
    X.append(np.minimum(f,fe_cap)); names.append('fe')
    if mn: X.append(m); names.append('mn')
    if interaction: X.append(n*a/10); names.append('nial')
    return np.array(X).T,names

def independent_fit(dat=D, scale=5., linear=False, quadratic=True, fe_cap=1.5, mn=False, interaction=False, signs=True, weights='given', label='base', ridge=0.05):
    dat=dat.copy(); X,names=features(dat,scale,linear,quadratic,fe_cap,mn,interaction)
    y=np.log(dat.rate.to_numpy()); w=dat.weight.to_numpy() if weights=='given' else np.ones(len(dat))
    if weights=='study_equal':
        for st in dat.study.unique():
            ix=np.where(dat.study.to_numpy()==st)[0]; w[ix]=1/len(ix)
    Xc=X.copy(); yc=y.copy()
    for st in dat.study.unique():
        ix=np.where(dat.study.to_numpy()==st)[0]
        Xc[ix]-=np.average(X[ix],axis=0,weights=w[ix]); yc[ix]-=np.average(y[ix],weights=w[ix])
    low=np.full(len(names),-np.inf); high=np.full(len(names),np.inf)
    if signs:
        high[names.index('ni')]=0; high[names.index('fe')]=0
    AA=np.vstack([Xc*np.sqrt(w[:,None]),np.sqrt(ridge)*np.eye(len(names))]); yy=np.r_[yc*np.sqrt(w),np.zeros(len(names))]
    sol=lsq_linear(AA,yy,bounds=(low,high),tol=1e-13,max_iter=1000)
    return dict(label=label,coef=dict(zip(names,sol.x)),options=dict(scale=scale,linear=linear,quadratic=quadratic,fe_cap=fe_cap,mn=mn,interaction=interaction),ridge=ridge,sse=float(np.sum(w*(yc-Xc@sol.x)**2)),rank=int(np.linalg.matrix_rank(Xc)),n=len(y),contrasts=len(y)-dat.study.nunique(),singular_values=np.linalg.svd(Xc*np.sqrt(w[:,None]),compute_uv=False).tolist())

def zrate(model,x):
    n,a,f,m=np.asarray(x)
    xx,names=features(dict(ni=n,al=a,fe=f,mn=m),**model['options'])
    return float(xx@np.array([model['coef'][k] for k in names]))

def optimized_floor(model,bar,mn_free=False):
    target=zrate(model,REFS[bar]); results=[]
    for alo,ahi,fcap,nige in [(0,1.5,2.3,False),(1.5,7,4.5,False),(7,9.5,4.5,True)]:
        bounds=[(0,30),(alo,ahi),(0,fcap)]+([(0,4)] if mn_free else [])
        def to4(x): return np.r_[x,0.] if len(x)==3 else np.array(x)
        def cc(x):
            v=to4(x); cons=[35-v.sum(),1250-float(liquidus(v).item()),target-zrate(model,v)]
            if nige: cons.append(v[0]-v[2])
            return np.array(cons)
        starts=[]
        for ni in [0,3,10,20,29]:
            for al in [alo,(alo+ahi)/2,ahi]:
                
                for fe0 in [0.,min(1.5,fcap),fcap]:
                    starts.append([ni,al,fe0]+([0.] if mn_free else []))
        for start in starts:
            r=minimize(lambda x:x[0],start,bounds=bounds,constraints={'type':'ineq','fun':cc},method='SLSQP',options={'ftol':1e-11,'maxiter':300})
            if np.min(cc(r.x))>=-2e-7:
                results.append((r.fun,to4(r.x),np.min(cc(r.x)),bool(r.success)))
    if not results: return dict(floor=None,witness=None)
    # Prefer simpler Fe-free witness for numerical ties by a second optimization at minimum Ni.
    best=min(results,key=lambda r:r[0]); v=best[1]
    return dict(floor=float(max(0,best[0])),witness=v.tolist(),rate_ratio=float(np.exp(zrate(model,v)-target)),liquidus=float(liquidus(v).item()),min_constraint=float(best[2]),successful=best[3])

def algebraic_lower_bound(mod,bar):
    co=mod['coef']; opts=mod['options']; target=zrate(mod,REFS[bar]); bn=co['ni']
    if opts['interaction']: return None
    ba=co['al']; b2=co.get('al2',0)/10
    ac=[0.,9.5]
    if b2>0 and 0<=-ba/(2*b2)<=9.5: ac.append(-ba/(2*b2))
    a=min(ac,key=lambda a:ba*a+b2*a*a)
    f=min(4.5,opts['fe_cap']) if co['fe'] < -1e-10 else 0.
    m=4. if co.get('mn',0)<-1e-10 else 0.
    other=ba*a+b2*a*a+co['fe']*min(f,opts['fe_cap'])+co.get('mn',0)*m
    if other<=target+1e-10: n=0.
    elif bn>=-1e-10: return {'floor':None}
    elif opts['linear']: n=(target-other)/bn*10
    else:
        v=(target-other)/bn
        if v>=1:return {'floor':None}
        n=-opts['scale']*np.log1p(-v)
    v=np.array([n,a,f,m]); return dict(floor=max(0,float(n)),witness=v.tolist(),liquidus=float(liquidus(v).item()),proposal_feasible=bool(v.sum()<=35+1e-8 and (a<=7 or n>=f) and (a>=1.5 or f<=2.3) and float(liquidus(v).item())<=1250))
