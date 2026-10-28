
import logging as _logging

class _KernelLogFormatter(_logging.Formatter):
    def format(self, record):
        import json

        return json.dumps({
            "name": record.name,
            "levelno": record.levelno,
            "levelname": record.levelname,
            "created": record.created,
            "message": super().format(record),
        })

_llm_handler = _logging.FileHandler(
    '/workspace/.kernel_llm_logs_1.jsonl', mode="a", encoding="utf-8"
)
_llm_handler.setFormatter(_KernelLogFormatter())

# Import LiteLLM logging before rebinding handlers so the import-time stderr
# handler it installs gets stripped in the same init step.
try:
    import litellm._logging as _litellm_logging  # noqa: F401
except (ImportError, ModuleNotFoundError):
    _litellm_logging = None

for _logger_name in ("lmi", "LiteLLM", "LiteLLM Router", "litellm", "e14c",):
    _lg = _logging.getLogger(_logger_name)
    _lg.handlers = [_llm_handler]
    _lg.propagate = False

# Delete these so notebook's variables aren't polluted
del _llm_handler, _logger_name, _lg, _litellm_logging, _logging, _KernelLogFormatter

# === NEXT EXECUTED CELL ===


from IPython.core.magic import register_cell_magic
import os
import subprocess
import tempfile
from pathlib import Path
import sys

@register_cell_magic
def Rscript(line, cell):
    """Execute R code via Rscript subprocess.

    Usage:
        %%Rscript
        library(tidyverse)
        df <- read_csv("data.csv")
        summary(df)

    Data exchange: Use Arrow/Parquet files for Python<->R data sharing.
        Python: df.to_parquet("data.parquet")
        R: df <- arrow::read_parquet("data.parquet")
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".R", delete=False) as f:
        f.write(cell)
        script_path = f.name
    try:
        r_env_path = os.getenv("R_ENV_PATH", "/app/r_env")
        result = subprocess.run(
            [f"{r_env_path}/bin/Rscript", script_path],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode != 0:
            raise RuntimeError(
                f"R script failed with exit code {result.returncode}")
    finally:
        Path(script_path).unlink(missing_ok=True)

# === NEXT EXECUTED CELL ===

import os
from pathlib import Path
print(os.getcwd())
print('\n'.join(str(p) for p in Path('/workspace').glob('*')))
print('\nPrompts:', list(Path('/workspace/.prompts').glob('*')))

# === NEXT EXECUTED CELL ===

from e14c.subagents import submit_task
outdir=Path('/workspace/outputs'); outdir.mkdir(exist_ok=True)
q1='''Independently audit primary sources for /workspace/corrosion_data.csv, focusing Tan2024 DOI 10.3390/ma17061330, Yang2018 10.3390/ma11091777, Zhao2022 10.3390/met12050781. Verify EACH row numerical rate/composition/test; determine same-test comparability and constructed values. Find missed same-study alloys in these papers. Retrieve full text where possible. Save source extracts, row audit, exact added usable numeric data with provenance to /workspace/outputs/audit_mdpi.md and added_mdpi.csv. Do not invent values or trust uploaded provenance line labels. Save full BibTeX via e14c citation APIs for sources used. This is an independent review: report access failures and exact tables. No modeling needed.'''
q2='''Find PRIMARY measured same-test seawater or 3.5% NaCl corrosion comparisons pure Cu or Cu-2Ni/Cu-5Ni vs 10-30Ni, plus low-Ni aluminum bronze / NAB / Cu-Ni-Al. Urgent key evidence missing in /workspace/corrosion_data.csv. Also audit Qian2025 DOI 10.1007/s42114-024-01174-0 and LewisLaQue1981 DOI 10.2172/6255887 rows in that file against actual sources (rates, grades, durations). Prefer immersion mass loss, but report Tafel separately. Save exact numeric rates AND compositions, test and source/table/page to /workspace/outputs/audit_lowNi.md and added_lowNi.csv. Distinguish measured vs constructed, product-form mismatch, no guessed grades. Save full BibTeX via e14c APIs. Seek zero-Ni bridge within same study, not cross-study absolute comparisons. No fitting needed.'''
taskids=[]
for q in [q1,q2]:
    taskids.append(await submit_task(q, agent_type='data-retrieval', project_id=os.environ.get('PROJECT_ID')))
print(taskids)
print('Plan: independently reconstruct within-study fitting and constrained floor optimization before inspecting fit_corrosion.py; audit evidence in parallel; then compare implementation, CALPHAD mappings, and full-truth limits.')

# === NEXT EXECUTED CELL ===

import numpy as np, pandas as pd, scipy
from scipy.optimize import lsq_linear, minimize
from scipy.interpolate import RegularGridInterpolator
D=pd.read_csv('corrosion_data.csv'); G=pd.read_csv('calphad_grid.csv')
print(D.groupby('study').size()); print(G.shape); print(G.ok.value_counts()); print(G.isna().sum()[lambda x:x>0]); print(G.columns.tolist())
print('installed:', {x: __import__('importlib').util.find_spec(x) is not None for x in ['pycalphad','torch','botorch']})
# Independent fit: weighted, within-study centered response/design removes study intercepts exactly.
def features(dat, scale=5., linear=False, quadratic=True, fe_cap=1.5, mn=False, interaction=False):
    n,a,f,m=[np.asarray(dat[k],dtype=float) for k in ['ni','al','fe','mn']]
    X=[n/10 if linear else -np.expm1(-n/scale),a]; names=['ni','al']
    if quadratic: X.append(a*a/10); names.append('al2')
    X.append(np.minimum(f,fe_cap)); names.append('fe')
    if mn: X.append(m); names.append('mn')
    if interaction: X.append(n*a/10); names.append('nial')
    return np.array(X).T,names

def independent_fit(dat=D, scale=5., linear=False, quadratic=True, fe_cap=1.5, mn=False, interaction=False, signs=True, weights='given', label='base'):
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
    sol=lsq_linear(Xc*np.sqrt(w[:,None]),yc*np.sqrt(w),bounds=(low,high),tol=1e-13,max_iter=1000)
    return dict(label=label,coef=dict(zip(names,sol.x)),options=dict(scale=scale,linear=linear,quadratic=quadratic,fe_cap=fe_cap,mn=mn,interaction=interaction),sse=float(np.sum(w*(yc-Xc@sol.x)**2)),rank=int(np.linalg.matrix_rank(Xc)),n=len(y),contrasts=len(y)-dat.study.nunique(),singular_values=np.linalg.svd(Xc*np.sqrt(w[:,None]),compute_uv=False).tolist())
ind=independent_fit()
print('FIRST independent fit, before inspecting fitting script:',ind)
(outdir/'independent_first_fit.json').write_text(__import__('json').dumps(ind,indent=2))

# === NEXT EXECUTED CELL ===

# Persist the independent regression and optimization implementation as a reusable output script.
import inspect, json
# Add ridge only after initial independent unpenalized result was saved.
src=inspect.getsource(independent_fit).replace("label='base')", "label='base', ridge=0.05)")
src=src.replace("sol=lsq_linear(Xc*np.sqrt(w[:,None]),yc*np.sqrt(w),", "AA=np.vstack([Xc*np.sqrt(w[:,None]),np.sqrt(ridge)*np.eye(len(names))]); yy=np.r_[yc*np.sqrt(w),np.zeros(len(names))]\n    sol=lsq_linear(AA,yy,")
src=src.replace("sse=float", "ridge=ridge,sse=float")
exec(src)
base=independent_fit()
print('Independent ridge fit:',base)
# Match grid handling but use exact unrounded axis levels, as truth_phys does.
axes=[np.linspace(0,30,8),np.linspace(0,9.5,6),np.linspace(0,4.5,6),np.array([0,2,4])]
liq=G.liquidus_C.fillna(1550).to_numpy().reshape(8,6,6,3)
liquidus=RegularGridInterpolator(axes,liq,bounds_error=False,fill_value=None)
def zrate(model,x):
    n,a,f,m=np.asarray(x)
    xx,names=features(dict(ni=n,al=a,fe=f,mn=m),**model['options'])
    return float(xx@np.array([model['coef'][k] for k in names]))
REFS={'9010':np.array([10.,0.,1.4,.8]), '7030':np.array([30.,0.,.6,.8])}
# Optimize all three continuous variables, partitioning discontinuous domain restrictions.
# Mn is fixed at zero for comparability, but optimized as a fourth coordinate for models with Mn.
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
                starts.append([ni,al,min(1.5,fcap)]+([0.] if mn_free else []))
        for start in starts:
            r=minimize(lambda x:x[0],start,bounds=bounds,constraints={'type':'ineq','fun':cc},method='SLSQP',options={'ftol':1e-11,'maxiter':300})
            if np.min(cc(r.x))>=-2e-7:
                results.append((r.fun,to4(r.x),np.min(cc(r.x)),bool(r.success)))
    if not results: return dict(floor=None,witness=None)
    # Prefer simpler Fe-free witness for numerical ties by a second optimization at minimum Ni.
    best=min(results,key=lambda r:r[0]); v=best[1]
    return dict(floor=float(max(0,best[0])),witness=v.tolist(),rate_ratio=float(np.exp(zrate(model,v)-target)),liquidus=float(liquidus(v).item()),min_constraint=float(best[2]),successful=best[3])
print('Optimized independent base floors:',{b:optimized_floor(base,b) for b in REFS})
impl='import numpy as np, pandas as pd\nfrom scipy.optimize import lsq_linear,minimize\nfrom scipy.interpolate import RegularGridInterpolator\n'+inspect.getsource(features)+'\n'+src+'\n'+inspect.getsource(zrate)+'\n'+inspect.getsource(optimized_floor)
(outdir/'independent_refit.py').write_text(impl)

# === NEXT EXECUTED CELL ===

import asyncio
from e14c.web import web_search
searches=await asyncio.gather(*[web_search(q,num_results=5) for q in ['Matcalc mc_ni v2.036 thermodynamic database download','copper nickel seawater corrosion 2% 5% pure copper immersion comparative corrosion rate','copper nickel aluminum bronze corrosion 3.5 NaCl Cu pure copper immersion comparative']])
for query,rs in zip(['database','lowNi','bronze'],searches):
    print('\n',query)
    for r in rs: print(r['title'],r['url'],r.get('snippet','')[:800])
(outdir/'search_initial.json').write_text(json.dumps(searches,indent=2))

# === NEXT EXECUTED CELL ===

# Run a complete independent sensitivity suite. Floors are continuous optimizations, never sample minima.
variants=[('Base',{}),('No ridge',{'ridge':0}),('Ridge 0.5',{'ridge':.5}),('Linear Al',{'quadratic':False}),('Free signs',{'signs':False}),('Linear Al; free signs',{'quadratic':False,'signs':False}),('Ni scale 3',{'scale':3}),('Ni scale 8',{'scale':8}),('Ni scale 12',{'scale':12}),('Linear Ni',{'linear':True}),('Fe cap 1.0',{'fe_cap':1.}),('Fe cap 2.5',{'fe_cap':2.5}),('Fe nominal (no cap)',{'fe_cap':100}),('Equal row weights',{'weights':'equal'}),('Equal study weights',{'weights':'study_equal'}),('Add Mn',{'mn':True}),('Add Ni x Al',{'interaction':True})]
for st in D.study.unique(): variants.append(('Drop '+st,{'dat':D[D.study!=st]}))
variants += [('Drop Lewis + Zhao (weak rows)',{'dat':D[~D.study.str.startswith(('Lewis','Zhao'))]}),('Only Tan + Yang',{'dat':D[D.study.isin(['Tan2024','Yang2018'])]})]
models={}; floorresults=[]
import time, warnings
warnings.filterwarnings('ignore',message='Values in x were outside bounds')
t0=time.time()
for name,kw in variants:
    mod=independent_fit(label=name,**kw); models[name]=mod
    row={'fit':name,'n':mod['n'],'sse':mod['sse'],**{f'b_{k}':v for k,v in mod['coef'].items()}}
    for bar in REFS:
        row[bar]=optimized_floor(mod,bar,mn_free=mod['options']['mn'])
    floorresults.append(row)
    print(name, *[f'{b}: {row[b]["floor"]:.4f}' for b in REFS])
print('Seconds:',time.time()-t0)
(outdir/'refits.json').write_text(json.dumps({'models':models,'floors':floorresults},indent=2))
flat=pd.DataFrame([{**{k:v for k,v in r.items() if k not in REFS},**{f'{b}_{k}':v for b in REFS for k,v in r[b].items()}} for r in floorresults]);flat.to_csv(outdir/'refits.csv',index=False)

# === NEXT EXECUTED CELL ===

# Run a complete independent sensitivity suite. Floors are continuous optimizations, never sample minima.
variants=[('Base',{}),('No ridge',{'ridge':0}),('Ridge 0.5',{'ridge':.5}),('Linear Al',{'quadratic':False}),('Free signs',{'signs':False}),('Linear Al; free signs',{'quadratic':False,'signs':False}),('Ni scale 3',{'scale':3}),('Ni scale 8',{'scale':8}),('Ni scale 12',{'scale':12}),('Linear Ni',{'linear':True}),('Fe cap 1.0',{'fe_cap':1.}),('Fe cap 2.5',{'fe_cap':2.5}),('Fe nominal (no cap)',{'fe_cap':100}),('Equal row weights',{'weights':'equal'}),('Equal study weights',{'weights':'study_equal'}),('Add Mn',{'mn':True}),('Add Ni x Al',{'interaction':True})]
for st in D.study.unique(): variants.append(('Drop '+st,{'dat':D[D.study!=st]}))
variants += [('Drop Lewis + Zhao (weak rows)',{'dat':D[~D.study.str.startswith(('Lewis','Zhao'))]}),('Only Tan + Yang',{'dat':D[D.study.isin(['Tan2024','Yang2018'])]})]
models={}; floorresults=[]
import time, warnings
warnings.filterwarnings('ignore',message='Values in x were outside bounds')
t0=time.time()
for name,kw in variants:
    mod=independent_fit(label=name,**kw); models[name]=mod
    row={'fit':name,'n':mod['n'],'sse':mod['sse'],**{f'b_{k}':v for k,v in mod['coef'].items()}}
    for bar in REFS:
        row[bar]=optimized_floor(mod,bar,mn_free=mod['options']['mn'])
    floorresults.append(row)
    print(name, *[f'{b}: {row[b]["floor"]}' for b in REFS])
print('Seconds:',time.time()-t0)
(outdir/'refits.json').write_text(json.dumps({'models':models,'floors':floorresults},indent=2))
flat=pd.DataFrame([{**{k:v for k,v in r.items() if k not in REFS},**{f'{b}_{k}':v for b in REFS for k,v in r[b].items()}} for r in floorresults]);flat.to_csv(outdir/'refits.csv',index=False)

# === NEXT EXECUTED CELL ===

print(models['Linear Al; free signs'])
for b in REFS:
    m=models['Linear Al; free signs']; print(b,zrate(m,REFS[b]),zrate(m,[0,0,0,0]),float(liquidus([0,0,0,0]).item()))
print(G.iloc[0].to_string())
import importlib.util
spec=importlib.util.spec_from_file_location('supplied_fit','/workspace/fit_corrosion.py'); supplied=importlib.util.module_from_spec(spec);spec.loader.exec_module(supplied)
sf=supplied.fit(supplied.load())
print('Independent vs supplied coefficient differences:',{k:base['coef'][k]-sf['coef'][k] for k in base['coef']})
print('Direct supplied fitting function executed; grid floor function not executed.')
# pycalphad install, standard dependencies (CPU only)
import subprocess
p=subprocess.run(['python','-m','pip','install','pycalphad','botorch','--quiet'],capture_output=True,text=True,timeout=240)
print('pip:',p.returncode,p.stderr[-1000:])

# === NEXT EXECUTED CELL ===

# Strengthen multistart optimizer with exact zero-solute corners; previous free-sign case
# exposed a local solver failure, not an infeasible model. Re-run rather than treating it as science.
srcfloor=inspect.getsource(optimized_floor)
srcfloor=srcfloor.replace("starts.append([ni,al,min(1.5,fcap)]+([0.] if mn_free else []))", "\n                for fe0 in [0.,min(1.5,fcap),fcap]:\n                    starts.append([ni,al,fe0]+([0.] if mn_free else []))")
exec(srcfloor)
# Closed-form relaxed lower bound over the FULL box (not the proposal's constraints),
# providing a global certificate whenever its witness also satisfies proposal constraints.
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
for r in floorresults:
    mod=models[r['fit']]
    for b in REFS:
        cert=algebraic_lower_bound(mod,b)
        if cert and cert.get('proposal_feasible'):
            r[b]['certificate']=cert
            if r[b]['floor'] is None or abs(r[b]['floor']-cert['floor'])>1e-6:
                r[b]=optimized_floor(mod,b,mn_free=mod['options']['mn']);r[b]['certificate']=cert
                print('repaired',r['fit'],b,r[b])
        elif cert: print('No feasible relaxed certificate',r['fit'],b,cert)
(outdir/'refits.json').write_text(json.dumps({'models':models,'floors':floorresults},indent=2))
# Save complete standalone runner with inputs resolved relative to script.
header="""import numpy as np, pandas as pd, json
from pathlib import Path
from scipy.optimize import lsq_linear,minimize
from scipy.interpolate import RegularGridInterpolator
HERE=Path(__file__).resolve().parent
D=pd.read_csv(HERE.parent/'corrosion_data.csv');G=pd.read_csv(HERE.parent/'calphad_grid.csv')
axes=[np.linspace(0,30,8),np.linspace(0,9.5,6),np.linspace(0,4.5,6),np.array([0,2,4])]
liquidus=RegularGridInterpolator(axes,G.liquidus_C.fillna(1550).to_numpy().reshape(8,6,6,3),bounds_error=False,fill_value=None)
REFS={'9010':np.array([10.,0.,1.4,.8]),'7030':np.array([30.,0.,.6,.8])}
"""
impl=header+inspect.getsource(features)+'\n'+src+'\n'+inspect.getsource(zrate)+'\n'+srcfloor+'\n'+inspect.getsource(algebraic_lower_bound)
(outdir/'independent_refit.py').write_text(impl)
print('Global relaxed-bound certificates:',sum('certificate' in r[b] for r in floorresults for b in REFS),'of',2*len(floorresults))

# === NEXT EXECUTED CELL ===

from e14c.web import scrape, cite_doi, save_citation
import requests, hashlib
maturl='https://www.matcalc.at/index.php/databases/open-databases'
matpage=await scrape(maturl)
(outdir/'matcalc_open_databases.md').write_text(matpage)
print(matpage[:11000])
save_citation(r'''@online{MatCalc2026open, author={{MatCalc Engineering}}, title={Open databases}, url={https://www.matcalc.at/index.php/databases/open-databases}, urldate={2026-10-12}}''')
u='https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2.036.tdb'
rr=requests.get(u,timeout=60); print(rr.status_code,len(rr.content),hashlib.sha256(rr.content).hexdigest()); print(rr.text[:2000])
if rr.status_code==200: (outdir/'mc_ni_v2.036.tdb').write_bytes(rr.content)

# === NEXT EXECUTED CELL ===

from e14c.web import scrape, cite_doi, save_citation
import requests, hashlib
maturl='https://www.matcalc.at/index.php/databases/open-databases'
try:
    matpage=await scrape(maturl)
except Exception as ex:
    print('Scraper unavailable:',type(ex).__name__)
    req=requests.get(maturl,timeout=60);matpage=req.text;print('Direct HTTP:',req.status_code)
(outdir/'matcalc_open_databases.txt').write_text(matpage)
print(matpage[:1000])
save_citation(r'''@online{MatCalc2026open, author={{MatCalc Engineering}}, title={Open databases}, url={https://www.matcalc.at/index.php/databases/open-databases}, urldate={2026-10-12}}''')
u='https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2.036.tdb'
rr=requests.get(u,timeout=60); print(rr.status_code,len(rr.content),hashlib.sha256(rr.content).hexdigest()); print(rr.text[:2000])
if rr.status_code==200: (outdir/'mc_ni_v2.036.tdb').write_bytes(rr.content)

# === NEXT EXECUTED CELL ===

from e14c.web import scrape, cite_doi, save_citation
import requests, hashlib, datetime
# This is a projectless run: give citation storage a local namespace, not a platform project identity.
os.environ.setdefault('PROJECT_ID','local-copper-review'); os.environ.setdefault('WORKSPACE_PATH','/workspace'); os.environ.setdefault('TRAJECTORY_ID','independent-review')
maturl='https://www.matcalc.at/index.php/databases/open-databases'
req=requests.get(maturl,timeout=60);matpage=req.text;print('Direct HTTP:',req.status_code)
(outdir/'matcalc_open_databases.txt').write_text(matpage)
print('Access date:',datetime.date.today())
save_citation('''@online{MatCalc2026open, author={{MatCalc Engineering}}, title={Open databases}, url={https://www.matcalc.at/index.php/databases/open-databases}, urldate={'''+str(datetime.date.today())+'''}}''')
u='https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2.036.tdb'
rr=requests.get(u,timeout=60); print(rr.status_code,len(rr.content),hashlib.sha256(rr.content).hexdigest()); print(rr.text[:2500])
if rr.status_code==200: (outdir/'mc_ni_v2.036.tdb').write_bytes(rr.content)

# === NEXT EXECUTED CELL ===

from bs4 import BeautifulSoup
soup=BeautifulSoup(matpage,'html.parser')
for a in soup.find_all('a',href=True):
    if any(x in a['href'].lower() for x in ['.tdb','mc_ni','database']): print(a.get_text(' ',strip=True),a['href'])
# Search current URLs rather than silently substituting another database.
rrs=await web_search('"mc_ni_v2.036"',num_results=8)
for r in rrs: print(r['title'],r['url'],r.get('snippet','')[:1200])
(outdir/'mcni_search.json').write_text(json.dumps(rrs,indent=2))
print('Current task status:')
from e14c.subagents import check_task
for tid in taskids:
    st=await check_task(tid); print(tid,st.status,st.runtime_minutes)

# === NEXT EXECUTED CELL ===

u='https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2036.tdb'
rr=requests.get(u,timeout=60); sha=hashlib.sha256(rr.content).hexdigest();print(rr.status_code,len(rr.content),sha)
if rr.status_code==200:(outdir/'mc_ni_v2.036.tdb').write_bytes(rr.content)
print(rr.text[:4000])
print('Ternary Cu parameters:',[ln for ln in rr.text.splitlines() if 'PARAMETER' in ln.upper() and 'CU' in ln.upper() and 'AL' in ln.upper() and 'NI' in ln.upper()][:30])
from pycalphad import Database
try:
    db=Database(str(outdir/'mc_ni_v2.036.tdb')); print('parsed',len(db.phases))
except Exception as e: print('Raw parser failure:',type(e).__name__,str(e)[:2500])
save_citation('''@online{PovodenKaradeniz2024mcni, author={Erwin Povoden-Karadeniz}, title={MatCalc Ni database mc\_ni v2.036}, date={2024-08-24}, url={'''+u+'''}, urldate={2026-10-28}}''')

# === NEXT EXECUTED CELL ===

tdbraw=rr.content.decode('latin1')
try:
    db=Database(tdbraw); print('parsed',len(db.phases))
except Exception as ex: print(type(ex).__name__,str(ex)[:5000])
print('\nMatcalc special commands:')
for line in tdbraw.splitlines():
    if line.strip() and not line.strip().startswith('$') and any(x in line.upper() for x in ['TYPE_DEFINITION','DATABASE_INFO','DEFAULT_COMMAND','REFERENCE_FILE']):print(line[:180])

# === NEXT EXECUTED CELL ===

import re
# Drop only non-thermodynamic MatCalc metadata records, keep every Gibbs-energy parameter.
clean='\n'.join(l.split('$')[0] for l in tdbraw.splitlines())
cmds=clean.split('!')
from collections import Counter
print(Counter(c.strip().split()[0].upper() for c in cmds if c.strip()))
print([c.strip()[:300] for c in cmds if c.strip() and c.strip().split()[0].upper() not in ['ELEMENT','FUNCTION','PHASE','CONSTITUENT','PARAMETER','TYPE_DEFINITION']][:100])

# === NEXT EXECUTED CELL ===

print('\n'.join(c.strip() for c in cmds if c.strip().startswith(('PHASE BCC','PHASE NIAL','PHASE GAMMA_PRIME','PHASE FCC','CONSTITUENT BCC','CONSTITUENT NIAL','CONST GAMMA_PRIME','CONST FCC','PHASE LIQUID','CONSTITUENT GAMMA_PRIME'))))
# Restrict parsing to the assessed Cu-Ni-Al-Fe-Mn-compatible phases and all functions/parameters;
# remove metadata, reference listing, and MatCalc-specific preferred-constituent markers.
keep=[]
for c in cmds:
    s=c.strip()
    if not s:continue
    token=s.split()[0].upper()
    if token in ['REFERENCE_ELEMENT','ATTACH_CONTRIBUTION','ADD_COMPOSITION_SET']:continue
    if token not in ['ELEMENT','FUNCTION','PHASE','CONSTITUENT','PARAMETER','TYPE_DEFINITION','CONST','PARAM']:continue
    s=re.sub(r'^CONST\s','CONSTITUENT ',s);s=re.sub(r'^PARAM\s','PARAMETER ',s)
    if s.startswith('CONSTITUENT '):s=s.replace('%','')
    # Convert MatCalc REF: annotations to bare TDB reference indices.
    s=re.sub(r'REF:\s*(\d+)',r'\1',s)
    keep.append(s+' !')
adapted='\n'.join(keep)
try:
    db=Database(adapted);print('Parsed:',len(db.phases))
except Exception as ex:print(type(ex).__name__,str(ex)[:3500])

# === NEXT EXECUTED CELL ===

keep2=[];skipped=Counter()
for s in keep:
    if s.startswith('PHASE '):s=s.split('>')[0].strip()+' !'
    if s.startswith('PARAMETER '):
        kind=re.match(r'PARAMETER\s+([^ (]+)',s).group(1)
        if kind not in ['G','L','TC','BMAGN']:
            skipped[kind]+=1;continue
    keep2.append(s)
adapted='\n'.join(keep2)
try:
    db=Database(adapted);print('Parsed:',len(db.phases),list(db.phases))
except Exception as ex: print(type(ex).__name__,str(ex)[:3500])
print('Skipped non-Gibbs parameter types:',skipped)
(outdir/'mcni_pycalphad_adapted.tdb').write_text(adapted)

# === NEXT EXECUTED CELL ===

adapted=adapted.replace('6000.00.00','6000.00')
try:
    db=Database(adapted); print('Parsed',len(db.phases))
except Exception as ex: print(type(ex).__name__,str(ex)[:3500])
(outdir/'mcni_pycalphad_adapted.tdb').write_text(adapted)

# === NEXT EXECUTED CELL ===

# Additional targeted retrieval: independent zero-Ni bridge candidates found in my search.
q3='''Retrieve exact numeric same-test primary data from (1) Corrosion of Cu and Cu-Ni Alloys in 0.5M NaCl and in Synthetic Seawater DOI 10.5006/1.3582011, (2) COMPARISON OF CORROSION BEHAVIOR OF COPPER AND COPPER ALLOYS IN AQUEOUS CHLORIDE SOLUTION, CICEQ 2021 pdf https://www.ache-pub.org.rs/CICEQ/2021/No4/CICEQ_No4_2021/08_4854_2021.pdf , (3) tropical copper 16y exposure DOI 10.21236/ad0644930 if accessible. Goal connect pure Cu / Cu5Ni to 10-30Ni or Cu-Al/CuAlNi with same-test rates. Extract composition/rate/method/duration table with exact values (do not digitize by eye), report relevance and uncertainty if only figures. Save /workspace/outputs/audit_bridges.md and added_bridges.csv; full BibTeX via e14c APIs. Existing model uses log ratios within a study; no fitting needed. Other agents cover Yang/Tan/Zhao/Qian/Lewis, so focus these new targets.''' 
# Do not pass the local citation namespace as a platform project ID.
taskids.append(await submit_task(q3,agent_type='data-retrieval'))
print(taskids[-1])
# Exact grid verification and missing-data checks
print('Grid ordering max coordinate error:',np.max(np.abs(G[['Ni_wt','Al_wt','Fe_wt','Mn_wt']].values-np.array(list(__import__('itertools').product(*axes))))))
for temp in ['sol','900','600']:
    cols=[f'{p}_{temp}' for p in ['liquid','alpha','beta','kappa_fe','fcc_feni','nial','gprime','other']]
    sums=G[cols].sum(axis=1); print(temp,'phase sums min/max:',sums.min(),sums.max(),'other nonzero',int((G[f'other_{temp}']>0).sum()))
print('Missing liquidus by Ni,Al:',G[G.liquidus_C.isna()].groupby(['Ni_wt','Al_wt']).size().to_string())
print('zero alpha:',G[G.alpha_600==0][['Ni_wt','Al_wt','Fe_wt','Mn_wt','alpha_600','beta_600','nial_600','gprime_600']].to_string(index=False))
print('Phase keys',db.phases['NIAL'].constituents, db.phases['GAMMA_PRIME'].constituents)

# === NEXT EXECUTED CELL ===

# Additional targeted retrieval of exact zero-Ni bridge candidates.
q3='''Retrieve exact numeric same-test primary data from (1) Corrosion of Cu and Cu-Ni Alloys in 0.5M NaCl and in Synthetic Seawater DOI 10.5006/1.3582011, (2) COMPARISON OF CORROSION BEHAVIOR OF COPPER AND COPPER ALLOYS IN AQUEOUS CHLORIDE SOLUTION, CICEQ 2021 pdf https://www.ache-pub.org.rs/CICEQ/2021/No4/CICEQ_No4_2021/08_4854_2021.pdf , (3) tropical copper 16y exposure DOI 10.21236/ad0644930 if accessible. Goal connect pure Cu / Cu5Ni to 10-30Ni or Cu-Al/CuAlNi with same-test rates. Extract composition/rate/method/duration table with exact values (do not digitize by eye), report relevance and uncertainty if only figures. Save /workspace/outputs/audit_bridges.md and added_bridges.csv; full BibTeX via e14c APIs. Existing model uses log ratios within a study; no fitting needed. Other agents cover Yang/Tan/Zhao/Qian/Lewis, so focus these new targets.'''
localnamespace=os.environ.pop('PROJECT_ID',None)
try: taskids.append(await submit_task(q3,agent_type='data-retrieval'))
finally:
    if localnamespace:os.environ['PROJECT_ID']=localnamespace
print(taskids[-1])
print('Grid ordering max coordinate error:',np.max(np.abs(G[['Ni_wt','Al_wt','Fe_wt','Mn_wt']].values-np.array(list(__import__('itertools').product(*axes))))))
for temp in ['sol','900','600']:
    cols=[f'{p}_{temp}' for p in ['liquid','alpha','beta','kappa_fe','fcc_feni','nial','gprime','other']]
    sums=G[cols].sum(axis=1); print(temp,'phase sums min/max:',sums.min(),sums.max(),'other nonzero',int((G[f'other_{temp}']>0).sum()))
print('Missing liquidus by Ni,Al:',G[G.liquidus_C.isna()].groupby(['Ni_wt','Al_wt']).size().to_string())
print('zero alpha:',G[G.alpha_600==0][['Ni_wt','Al_wt','Fe_wt','Mn_wt','alpha_600','beta_600','nial_600','gprime_600']].to_string(index=False))

# === NEXT EXECUTED CELL ===

import torch
# Preserve supplied files, overriding only flattened-upload resource paths in memory.
import truth_phys as TP
TP.GRID_CSV=Path('/workspace/calphad_grid.csv');TP.FIT_JSON=Path('/workspace/corrosion_fit.json')
BA=TP.BA
torch.set_num_threads(4)
print('Imported full truth; runtime path overrides:',TP.GRID_CSV,TP.FIT_JSON)
print('Dense-reference Sobol values:',{b:TP.reference_m(k)[:2] for b,k in [('9010','C70600 (90-10 Cu-Ni)'),('7030','C71500 (70-30 Cu-Ni)')]})
print('Grid all-zero phase sum above solidus:',G.loc[G.filter(regex='_sol$').sum(axis=1)<.5,['Ni_wt','Al_wt','Fe_wt','Mn_wt','solidus_C','liquidus_C']].to_string(index=False))
# Direct phase-equilibrium spot checks with all compatible phases; excludes order-disorder BCC_B2
# (no Al/Cu constituents; tailored to NiTi in database) and duplicate ordered precipitates only if impossible.
from pycalphad import equilibrium, variables as v
masses={'CU':63.546,'NI':58.6934,'AL':26.9815385,'FE':55.845,'MN':54.938044}
comps=['AL','CU','FE','MN','NI','VA']
from pycalphad.core.utils import filter_phases
phases=filter_phases(db,comps)
print('Compatible phases:',phases)
def eq_at(w,temp,phase_list=phases):
    wt={'NI':w[0],'AL':w[1],'FE':w[2],'MN':w[3],'CU':100-sum(w)}
    amt={el:wt[el]/masses[el] for el in masses}; tot=sum(amt.values())
    cond={v.N:1,v.P:101325,v.T:np.atleast_1d(temp)+273.15}
    # Trace amounts avoid singular solution at exactly absent elements; use reduced active components instead.
    active=[el for el in ['AL','CU','FE','MN','NI'] if wt[el]>0]
    if len(active)==1: activecomp=active+['VA'];phase_list=filter_phases(db,activecomp)
    else: activecomp=active+['VA'];phase_list=filter_phases(db,activecomp)
    for el in active:
        if el!='CU':cond[v.X(el)]=amt[el]/tot
    eq=equilibrium(db,activecomp,phase_list,cond,calc_opts={'pdens':1000})
    return eq
sample_eq=eq_at([0,0,0,0],[600,1084,1085])
print(sample_eq[['Phase','NP']])

# === NEXT EXECUTED CELL ===

# Direct checks at exact grid compositions, not interpolation points.
checkids=[0, G.index[(G.Ni_wt.between(29.99,30.01))&(G.Al_wt==0)&(G.Fe_wt==.9)&(G.Mn_wt==0)][0],G.index[(G.Ni_wt.between(4.28,4.29))&(G.Al_wt==9.5)&(G.Fe_wt==3.6)&(G.Mn_wt==0)][0],G.index[(G.Ni_wt.between(8.57,8.58))&(G.Al_wt==1.9)&(G.Fe_wt==2.7)&(G.Mn_wt==4)][0]]
eqchecks=[]
for idx in checkids:
    row=G.loc[idx];w=row[['Ni_wt','Al_wt','Fe_wt','Mn_wt']].to_numpy(float)
    # recover unrounded Ni used in generating grid
    w[0]=axes[0][int(round(w[0]/30*7))]
    temps=[600,row.solidus_C+1]+([row.liquidus_C-1,row.liquidus_C+1] if np.isfinite(row.liquidus_C) else [])
    tt=time.time();eq=eq_at(w,np.unique(temps));eq.to_netcdf(outdir/f'eq_grid_{idx}.nc')
    items=[]
    for ti,T in enumerate(eq.T.values):
        pt=eq.isel(T=ti); p=np.array(pt.Phase).ravel(); amounts=np.array(pt.NP).ravel(); xs=np.array(pt.X).reshape(-1,len(eq.component))
        rec={'temp_C':float(T-273.15),'phases':[]}
        for phase,frac,x in zip(p,amounts,xs):
            if phase and np.isfinite(frac):rec['phases'].append({'phase':str(phase),'fraction':float(frac),'composition':dict(zip(map(str,eq.component.values),map(float,x)))})
        items.append(rec)
    eqchecks.append({'grid_index':int(idx),'wt':w.tolist(),'stored':row.to_dict(),'equilibria':items})
    print(idx,w.tolist(),'seconds',round(time.time()-tt,2),json.dumps(items))
(outdir/'calphad_spotchecks.json').write_text(json.dumps(eqchecks,indent=2))

# === NEXT EXECUTED CELL ===

# The missing run_calphad.py controls phase selection. Unrestricted mc_ni produces
# an unphysical beta-Mn field even in Mn-free Cu-Ni; use the five grid-represented phases.
restricted=['LIQUID','FCC_A1','BCC_A2','NIAL','GAMMA_PRIME']
srceq=inspect.getsource(eq_at).replace("phase_list=filter_phases(db,activecomp)","phase_list=[p for p in filter_phases(db,activecomp) if p in restricted]")
exec(srceq)
eqchecks2=[]
for idx in checkids:
    row=G.loc[idx];w=row[['Ni_wt','Al_wt','Fe_wt','Mn_wt']].to_numpy(float);w[0]=axes[0][int(round(w[0]/30*7))]
    temps=[600,row.solidus_C+1]+([row.liquidus_C-1,row.liquidus_C+1] if np.isfinite(row.liquidus_C) else [])
    eq=eq_at(w,np.unique(temps));eq.to_netcdf(outdir/f'eq_restricted_grid_{idx}.nc')
    items=[]
    for ti,T in enumerate(eq.T.values):
        pt=eq.isel(T=ti);p=np.array(pt.Phase).ravel();am=np.array(pt.NP).ravel();xs=np.array(pt.X).reshape(-1,len(eq.component))
        rec={'temp_C':float(T-273.15),'phases':[]}
        for phase,frac,x in zip(p,am,xs):
            if phase and np.isfinite(frac):rec['phases'].append({'phase':str(phase),'fraction':float(frac),'composition':dict(zip(map(str,eq.component.values),map(float,x)))})
        items.append(rec)
    eqchecks2.append({'grid_index':int(idx),'wt':w.tolist(),'stored':row.to_dict(),'equilibria':items})
    print(idx,json.dumps(items))
(outdir/'calphad_spotchecks_restricted.json').write_text(json.dumps(eqchecks2,indent=2))
print('Stored comparison:');print(G.loc[checkids,['Ni_wt','Al_wt','Fe_wt','Mn_wt','alpha_600','fcc_feni_600','kappa_fe_600','nial_600','gprime_600','liquid_sol','alpha_sol','fcc_feni_sol','kappa_fe_sol','nial_sol']].to_string(index=False))

# === NEXT EXECUTED CELL ===

print(G.loc[210].to_string())
w=[30/7,9.5,3.6,0]
for temp in [1044.82,1045.82,1046.82,1050,1060,1080]:
    eq=eq_at(w,temp)
    print(temp,list(zip(eq.Phase.values.ravel(),np.round(eq.NP.values.ravel(),6))))
# Grid-wide evidence of implausible liquid fractions near claimed solidus.
print(G.liquid_sol.describe(percentiles=[.5,.9,.95,.99]))
print('near-solidus liquid >0.5:',(G.liquid_sol>.5).sum(),'excluding pure copper:',((G.liquid_sol>.5)&(G.index!=0)).sum())
print(G.nlargest(15,'liquid_sol')[['Ni_wt','Al_wt','Fe_wt','Mn_wt','liquidus_C','solidus_C','range_C','liquid_sol']].to_string(index=False))
# Read user/project procedure memory before storing a concise procedural convention.
print(Path('.prompts/MEMORY.md').read_text())

# === NEXT EXECUTED CELL ===

# Full-truth minima include the inherited process-density and retained-beta penalties.
fullfloor=[]
truth=TP.PhysTruth(m_ref=0)
fullrefs={b:TP.reference_m(k) for b,k in [('9010','C70600 (90-10 Cu-Ni)'),('7030','C71500 (70-30 Cu-Ni)')]}
def full_constraints_jac(x,mbar,nige):
    xx=torch.tensor(x,requires_grad=True);out=truth.full(xx)
    ww=TP.wt(xx[:4]); cons=[35-ww.sum(),(1250-TP.field(xx[:4],'liquidus_C'))/100,mbar*0+out['m']-mbar]
    if nige:cons.append((ww[0]-ww[2])/30)
    C=torch.stack(cons);J=torch.stack([torch.autograd.grad(c,xx,retain_graph=True)[0] for c in C]);return C.detach().numpy(),J.detach().numpy()
for b in REFS:
    mbar=fullrefs[b][0];sols=[];t0=time.time()
    for alo,ahi,fcap,nige in [(0,1.5,2.3,False),(1.5,7,4.5,False),(7,9.5,4.5,True)]:
        bounds=[(0,1),(alo/9.5,ahi/9.5),(0,fcap/4.5),(0,1),(0,1),(0,1),(0,1)]
        for nw,aw,fw in [(1.5,2.1,3.7),(3,2.6,1.5),(10,0,1.4),(15,4,3),(25,8,4)]:
            x0=np.array([nw/30,np.clip(aw,alo,ahi)/9.5,min(fw,fcap)/4.5,0,.38,.7,.55])
            rr2=minimize(lambda x:30*x[0],x0,jac=lambda x:np.array([30,0,0,0,0,0,0]),bounds=bounds,constraints={'type':'ineq','fun':lambda x:full_constraints_jac(x,mbar,nige)[0],'jac':lambda x:full_constraints_jac(x,mbar,nige)[1]},method='SLSQP',options={'maxiter':200,'ftol':1e-10})
            cs=full_constraints_jac(rr2.x,mbar,nige)[0]
            if cs.min()>-1e-7:sols.append(rr2)
    best=min(sols,key=lambda r:r.fun);x=best.x;vals=truth.full(torch.tensor(x))
    rec={'bar':b,'floor':best.fun,'wt':(x[:4]*[30,9.5,4.5,4]).tolist(),'apv':x[4:].tolist(),'outputs':{k:float(v) for k,v in vals.items()},'mbar':mbar,'success':bool(best.success)};fullfloor.append(rec)
    print(rec,'seconds',time.time()-t0)
(outdir/'full_truth_floors.json').write_text(json.dumps(fullfloor,indent=2))

# === NEXT EXECUTED CELL ===

# Full-truth minima include the inherited process-density and retained-beta penalties.
# Finite-difference Jacobian: uploaded transform uses an in-place operation incompatible with autograd.
fullfloor=[]
truth=TP.PhysTruth(m_ref=0)
fullrefs={b:TP.reference_m(k) for b,k in [('9010','C70600 (90-10 Cu-Ni)'),('7030','C71500 (70-30 Cu-Ni)')]}
def full_constraints(x,mbar,nige):
    xx=torch.tensor(x);out=truth.full(xx)
    ww=TP.wt(xx[:4]);cons=[35-ww.sum(),(1250-TP.field(xx[:4],'liquidus_C'))/100,out['m']-mbar]
    if nige:cons.append((ww[0]-ww[2])/30)
    return torch.stack(cons).numpy()
for b in REFS:
    mbar=fullrefs[b][0];sols=[];t0=time.time()
    for alo,ahi,fcap,nige in [(0,1.5,2.3,False),(1.5,7,4.5,False),(7,9.5,4.5,True)]:
        bounds=[(0,1),(alo/9.5,ahi/9.5),(0,fcap/4.5),(0,1),(0,1),(0,1),(0,1)]
        for nw,aw,fw in [(1.5,2.1,3.7),(3,2.6,1.5),(10,0,1.4),(15,4,3),(25,8,4)]:
            x0=np.array([nw/30,np.clip(aw,alo,ahi)/9.5,min(fw,fcap)/4.5,0,.38,.7,.55])
            rr2=minimize(lambda x:30*x[0],x0,jac=lambda x:np.array([30,0,0,0,0,0,0]),bounds=bounds,constraints={'type':'ineq','fun':lambda x:full_constraints(x,mbar,nige)},method='SLSQP',options={'maxiter':200,'ftol':1e-10})
            cs=full_constraints(rr2.x,mbar,nige)
            if cs.min()>-1e-7:sols.append(rr2)
    best=min(sols,key=lambda r:r.fun);x=best.x;vals=truth.full(torch.tensor(x))
    rec={'bar':b,'floor':best.fun,'wt':(x[:4]*[30,9.5,4.5,4]).tolist(),'apv':x[4:].tolist(),'outputs':{k:float(v) for k,v in vals.items()},'mbar':mbar,'success':bool(best.success)};fullfloor.append(rec)
    print(rec,'seconds',time.time()-t0)
(outdir/'full_truth_floors.json').write_text(json.dumps(fullfloor,indent=2))

# === NEXT EXECUTED CELL ===

# Full-truth minima include the inherited process-density and retained-beta penalties.
# Finite differences avoid an in-place operation in the uploaded torch transform.
fullfloor=[];truth=TP.PhysTruth(m_ref=0)
fullrefs={b:TP.reference_m(k) for b,k in [('9010','C70600 (90-10 Cu-Ni)'),('7030','C71500 (70-30 Cu-Ni)')]}
def full_constraints(x,mbar,nige):
    xx=torch.tensor(x,dtype=torch.float64);out=truth.full(xx);ww=TP.wt(xx[:4])
    cons=[35-ww.sum(),(1250-TP.field(xx[:4],'liquidus_C'))/100,out['m']-mbar]
    if nige:cons.append((ww[0]-ww[2])/30)
    return torch.stack(cons).numpy().astype(np.float64)
for b in REFS:
    mbar=fullrefs[b][0];sols=[];t0=time.time()
    for alo,ahi,fcap,nige in [(0,1.5,2.3,False),(1.5,7,4.5,False),(7,9.5,4.5,True)]:
        bounds=[(0,1),(alo/9.5,ahi/9.5),(0,fcap/4.5),(0,1),(0,1),(0,1),(0,1)]
        for nw,aw,fw in [(1.5,2.1,3.7),(3,2.6,1.5),(10,0,1.4),(15,4,3),(25,8,4)]:
            x0=np.array([nw/30,np.clip(aw,alo,ahi)/9.5,min(fw,fcap)/4.5,0,.38,.7,.55],dtype=np.float64)
            rr2=minimize(lambda x:30*x[0],x0,jac=lambda x:np.array([30.,0.,0.,0.,0.,0.,0.]),bounds=bounds,constraints={'type':'ineq','fun':lambda x:full_constraints(x,mbar,nige)},method='SLSQP',options={'maxiter':200,'ftol':1e-10})
            if full_constraints(rr2.x,mbar,nige).min()>-1e-7:sols.append(rr2)
    best=min(sols,key=lambda r:r.fun);x=best.x;vals=truth.full(torch.tensor(x))
    rec={'bar':b,'floor':best.fun,'wt':(x[:4]*[30,9.5,4.5,4]).tolist(),'apv':x[4:].tolist(),'outputs':{k:float(v) for k,v in vals.items()},'mbar':mbar,'success':bool(best.success)};fullfloor.append(rec)
    print(rec,'seconds',time.time()-t0)
(outdir/'full_truth_floors.json').write_text(json.dumps(fullfloor,indent=2))

# === NEXT EXECUTED CELL ===

# Model diagnostics: the Ni form controls an extrapolated effect, not a well-measured low-Ni boundary.
for b in [base,models['Ni scale 3'],models['Ni scale 8'],models['Ni scale 12'],models['Linear Ni']]:
    print(b['label'],'90-10/70-30 predicted dense rate ratio',np.exp(zrate(b,REFS['9010'])-zrate(b,REFS['7030'])), 'SSE',b['sse'])
print('Observed within-pair ratios: Qian',D.iloc[6].rate/D.iloc[7].rate,'Lewis one-year',30.5/20.3,'Yang7Ni/90-10',.0215/.0359)
# Conductivity back-check against the handbook resistivities quoted in truth_phys.py itself.
for name,w,rho in [('Cu',[0,0,0,0],1.7),('C70600',[10,0,1.4,.8],19.1),('C71500',[30,0,.6,.8],37.5),('C61400',[0,7,2.5,0],12.3),('C60800',[0,6,0,0],10.1)]:
    c=torch.tensor(w)/TP.WT_MAX;k=float(TP.conductivity(c));print(name,'rho_model',1.7+np.dot(w,[1.25,1.5,1,3]),'rho_quoted',rho,'k_model',k,'h',.6*np.sqrt(k/TP.K_CU))
# Reference definition and soft-gate audit.
for b,(mref,rhoref,xref) in fullrefs.items():
    o=truth.full(xref);J=truth.objective(xref);U=float(o['U']);bur=.3*float(BA.burden(xref));
    print(b,'mref',mref,'actual objective at own reference using mref=0 truth:',float(J),'at specified reference gate:',float(BA.objective_from(o['U'],o['m'],xref,mref)),'U',U,'burden penalty',bur)
# Crisp statements about whether the limits are enforced at objective evaluation.
x_bad=torch.tensor([1.,1.,1.,1.,.4,.7,.5]);print('infeasible objective still finite:',bool(TP.feasible(x_bad)),float(truth.objective(x_bad)))
for tid in taskids:
    st=await check_task(tid);print(tid,st.status,st.runtime_minutes)
print('Available output files:',[p.name for p in outdir.iterdir()])

# === NEXT EXECUTED CELL ===

st=await check_task(taskids[0]);print(st.answer)
print('Task output refs',st.output_files)
print('audit files on shared filesystem',list(outdir.glob('*audit*')))

# === NEXT EXECUTED CELL ===

from e14c.subagents import get_task_messages
msgs=await get_task_messages(taskids[0])
print(type(msgs),len(msgs))
for i,m in enumerate(msgs):
    print(i,m.keys(),str(m)[:220],len(str(m)))
(outdir/'mdpi_agent_messages.json').write_text(json.dumps(msgs,default=str,indent=2))

# === NEXT EXECUTED CELL ===

for i in [31,33,35,37,39,41,43,45,47,49,52]:
    if i<len(msgs) and msgs[i]['role']=='tool':
        print('\n=== MESSAGE',i,'===\n',msgs[i].get('content','')[:16000])
# Print candidate reconstruction code to inspect rather than execute opaque agent code.
for i in [55,59]:
    print('\n=== CODE',i,'===')
    for tc in msgs[i].get('tool_calls',[]):
        if tc['function']['name']=='run_cell':print(json.loads(tc['function']['arguments'])['code'][:18000])

# === NEXT EXECUTED CELL ===

from e14c.web import fetch_paper
sources=outdir/'sources';sources.mkdir(exist_ok=True)
dois={'Tan2024':'10.3390/ma17061330','Yang2018':'10.3390/ma11091777','Zhao2022':'10.3390/met12050781','Qian2025':'10.1007/s42114-024-01174-0','LewisLaQue1981':'10.2172/6255887'}
async def getsource(key,doi):
    try:
        bib=await cite_doi(doi);(sources/f'{key}.bib').write_text(bib)
        paper=await fetch_paper(doi=doi);(sources/f'{key}.json').write_text(json.dumps(paper,indent=2))
        txt='\n\n'.join(f'=== PAGE {p.get("page",i+1)} ===\n'+p.get('text','') for i,p in enumerate(paper.get('pages',[])))
        (sources/f'{key}.txt').write_text(txt);return key,len(txt)
    except Exception as ex:return key,str(ex)
print(await asyncio.gather(*[getsource(k,d) for k,d in dois.items()]))
print('Source files:',list(sources.glob('*')))
# Recover excerpts into local evidence files, explicitly labeled as delegated tool output.
for i in [52]:
    (outdir/f'mdpi_tables_delegated_{i}.txt').write_text(msgs[i]['content'])
print(msgs[52]['content'][:16000])

# === NEXT EXECUTED CELL ===

texts={k:(sources/f'{k}.txt').read_text() for k in dois}
for k,terms in {'Qian2025':['Table 1','5401','10050','Table 4','B10','7 days'],'LewisLaQue1981':['43.2','150','Table III','TABLE III','0.6','Aluminum Bronze'],'Zhao2022':['Table 3','Area1','Area 1','Table 5','N-3','11.2'],'Yang2018':['0.0359','GB/T 2059','Figure 8']}.items():
    print('\n###',k)
    for term in terms:
        at=texts[k].lower().find(term.lower());print('\n',term,'index',at,'\n',texts[k][max(0,at-500):at+2300] if at>=0 else '')

# === NEXT EXECUTED CELL ===

for k,term,window in [('Qian2025','Table 2',3500),('Qian2025','Table\u202f2',3500),('Qian2025','10050',3200),('Zhao2022','Area1',2800),('Zhao2022','Area 1',2800),('Zhao2022','Table 3.',5000),('LewisLaQue1981','43.2',4000),('LewisLaQue1981','150',1000)]:
    at=texts[k].lower().find(term.lower());print('\n###',k,term,at);print(texts[k][max(0,at-500):at+window] if at>=0 else '')
# Store compact source passages for every row.
audit_extract=[]
for k,terms in {'Tan2024':['Table 1.','Table 3.'],'Yang2018':['Table 1.','0.0359'],'Qian2025':['11.266','5401','10050'],'Zhao2022':['Table 3.','Table 5.'],'LewisLaQue1981':['43.2','TABLE III']}.items():
    for term in terms:
        at=texts[k].lower().find(term.lower())
        audit_extract.append(f'## {k}: {term}\n'+(texts[k][max(0,at-600):at+5000] if at>=0 else 'not located by literal text search'))
(outdir/'source_passages.md').write_text('\n\n'.join(audit_extract))

# === NEXT EXECUTED CELL ===

def findall_snip(k,term,n=4,before=100,after=1400):
    hits=list(re.finditer(re.escape(term),texts[k],re.I)); print(k,repr(term),'matches',len(hits))
    for mm in hits[-n:]:print('\n'+texts[k][max(0,mm.start()-before):mm.end()+after])
findall_snip('LewisLaQue1981','TABLE XIII',2,100,4300)
findall_snip('LewisLaQue1981','TABLE III',2,100,4500)
findall_snip('Qian2025','11.266',2,800,1000)
findall_snip('Zhao2022','Area1',2,500,1800)
findall_snip('Zhao2022','Area 1',2,500,1800)

# === NEXT EXECUTED CELL ===

k='LewisLaQue1981'
for term in ['TABLE XIV','TABLE III','Quiet','Al Bronze','Ni Al Bronze']:
    hits=list(re.finditer(re.escape(term),texts[k],re.I));
    mm=hits[-1] if term.startswith('TABLE') else (hits[-1] if hits else None)
    print('\n###',term)
    if mm:print(texts[k][max(0,mm.start()-200):mm.start()+6000])
# Reference figure, NAB interpolation to direct equilibrium spot checks.
w=[4.5,9.025,4.05,1.2];c=torch.tensor(w)/TP.WT_MAX
print('NAB interpolated', {f:float(TP.field(c,f)) for f in ['liquidus_C','solidus_C','range_C','kappa_fe_sol','nial_sol','beta_900','alpha_600']})
print('g distribution grid:',G.eval('(kappa_fe_sol+fcc_feni_sol)/.045').describe(percentiles=[.5,.9,.95,.99]).to_string())

# === NEXT EXECUTED CELL ===

p=json.loads((sources/'LewisLaQue1981.json').read_text())
for page in p['pages']:
    if int(page.get('page',0)) in [44,45,46,47,48,59,60]:
        print('\n### PAGE',page['page'],'\n',page['text'][:14000])

# === NEXT EXECUTED CELL ===

# Compare supplied alternatives numerically with the independent implementation.
comp=[]
variant_map={'Base':{},'Linear Al':{'al_form':'lin'},'Free signs':{'signs':False},'Linear Al; free signs':{'al_form':'lin','signs':False},'Ni scale 3':{'ni_scale':3},'Ni scale 8':{'ni_scale':8},'Ni scale 12':{'ni_scale':12},'Linear Ni':{'ni_form':'lin'},'Fe cap 1.0':{'fe_sol':1.0},'Fe cap 2.5':{'fe_sol':2.5},'No ridge':{'ridge':0},'Ridge 0.5':{'ridge':.5}}
for name,cfg in variant_map.items():
    sf=supplied.fit(supplied.load(),{**supplied.BASE,**cfg}); dif=max(abs(models[name]['coef'].get(k,0)-sf['coef'][k]) for k in ['ni','al','al2','fe'])
    comp.append({'fit':name,'max_coefficient_difference':dif})
print(pd.DataFrame(comp).to_string(index=False));(outdir/'supplied_fit_crosscheck.json').write_text(json.dumps(comp,indent=2))
# Construct exact, traceable additions. Do not force unknown compositions into numeric fitting columns.
adds=[]
def add(study,alloy,ni,al,fe,mn,rate,unit,test,source,use='sensitivity',**extra):
    adds.append(dict(study=study,alloy=alloy,ni=ni,al=al,fe=fe,mn=mn,rate=rate,unit=unit,test=test,weight=.5,use=use,source=source,**extra))
for i,r in D.iloc[:4].iterrows():
    add('Tan2024_10d',r.alloy,r.ni,r.al,r.fe,r.mn,[.50,1.34,1.77,2.16][i],'uA/cm2','10-day 3.5% NaCl; Tafel','10.3390/ma17061330 Table 3',use='replace_30d_not_independent_replication')
add('Tan2024_massloss30d','ZCuAl7-7-4-2',6.82,6.94,4.10,1.72,.00267,'mm/y','30-day 3.5% NaCl; mass loss','10.3390/ma17061330 abstract/Section 3.3',use='singleton_no_within_study_slope_information')
add('Zhao2022_N3','N-3',10.8,10.9,4.1,np.nan,4.09,'uA/cm2','3.5% NaCl; 20-min OCP then polarization','10.3390/met12050781 Tables 3,5',use='exclude_unmodeled_Cr1.9wt_and_layer_confound',Cr=1.9)
for alloy,ni,fe,mn,rates in [('B10',11.266,1.751,.725,[149.94,231.95,196.57,49.077,234.52]),('B30',30.05,.726,.718,[17.655,25.498,6.3465,18.453,28.7])]:
    for t,rate in zip(['3h','1d','3d','5d','7d'],rates):add('Qian2025_Tafel_'+t,alloy,ni,0,fe,mn,rate,'uA/cm2',f'artificial seawater; Tafel at {t}','10.1007/s42114-024-01174-0 Tables 4,5',use='replace_EIS_not_independent_replication')
# Author-reported grade shorthand: retained as nominal assumption, not measured assay.
for name,ni,fe,mn,rates in [('C70600',10,1.4,.8,[93.9,84.9]),('C71500',30,.6,.6,[95.1,89.5])]:
    for rep,rate in enumerate(rates,1):add('LewisLaQue1981_30d',name+f'_rep{rep}',ni,0,fe,mn,rate,'um/y','30-day clean seawater; 2m/s; uncoupled','10.2172/6255887 Table XVII printed p46',use='nominal_grade_composition_sensitivity')
# Fe-content data: use Ni-Fe values explicitly specified; Mn unreported.
for period,rrates in [('62d',[.0023,.0027,.0011]),('132d',[.0009,.0009,.0005])]:
    for ni,fe,rate in zip([10,10,30],[.7,1.5,.4],rrates):add('LewisLaQue1981_untreated_'+period,f'Cu-{ni}Ni-{fe}Fe',ni,0,fe,np.nan,rate,'inch/y',f'untreated seawater; 0.5ft/s; {period}','10.2172/6255887 Table XV printed p44',use='specified_Ni_Fe_Mn_unknown_sensitivity')
A=pd.DataFrame(adds);A.to_csv(outdir/'additional_data.csv',index=False)
print('Added exact candidate observations:',len(A))
# Correct known nominal Yang composition; no claim of a measured bulk assay.
Dc=D.copy(); Dc.loc[Dc.study.eq('Yang2018')&Dc.alloy.str.startswith('C70600'),['fe','mn']]=[1.,1.]
Dc.to_csv(outdir/'original_data_nominal_corrected.csv',index=False)

# === NEXT EXECUTED CELL ===

for tid in taskids[1:]:
    st=await check_task(tid); print(tid,st.status,st.runtime_minutes)
    if st.status=='success':
        (outdir/f'agent_{tid}_answer.md').write_text(st.answer);print(st.answer[:25000])
# Local source-derived fitting sensitivities, clearly separated from trusted 30-day immersion inference.
A=pd.read_csv(outdir/'additional_data.csv'); A['weight']=.5
scenarios=[]
def scenario(name,dat,**opts):
    mod=independent_fit(dat=dat,label=name,**opts);models[name]=mod
    row={'fit':name,'n':mod['n'],'sse':mod['sse'],**{f'b_{k}':v for k,v in mod['coef'].items()}}
    for b in REFS:
        row[b]=optimized_floor(mod,b,mn_free=mod['options']['mn']); row[b]['certificate']=algebraic_lower_bound(mod,b)
    scenarios.append(row);print(name,[(b,row[b]['floor']) for b in REFS])
scenario('Yang nominal corrected',Dc)
scenario('No unconfirmed Yang comparator',Dc[~Dc.study.eq('Yang2018')])
scenario('Replace Qian EIS by 7d Tafel',pd.concat([Dc[~Dc.study.eq('Qian2025')],A[A.study.eq('Qian2025_Tafel_7d')]],ignore_index=True))
scenario('Add Lewis 30d clean-water pair',pd.concat([Dc,A[A.study.eq('LewisLaQue1981_30d')]],ignore_index=True))
scenario('Add Lewis untreated 62d/132d pairs',pd.concat([Dc,A[A.study.str.startswith('LewisLaQue1981_untreated')]],ignore_index=True))
scenario('Replace Tan30d by Tan10d',pd.concat([Dc[~Dc.study.eq('Tan2024')],A[A.study.eq('Tan2024_10d')]],ignore_index=True))
scenario('Mn excluding unreported Zhao',Dc[~Dc.study.eq('Zhao2022')],mn=True)
(outdir/'source_sensitivity.json').write_text(json.dumps(scenarios,indent=2));(outdir/'refits.json').write_text(json.dumps({'models':models,'floors':floorresults+scenarios},indent=2))

# === NEXT EXECUTED CELL ===

# Verify precise passing witnesses just above the full-truth numerical boundaries.
for rec in fullfloor:
    w=np.array(rec['wt']);w[0]=np.ceil(w[0]*10000)/10000+0.0001;w[2]=3.6
    x=torch.tensor(np.r_[w/[30,9.5,4.5,4],rec['apv']]);o=truth.full(x)
    rec['strict_witness_wt']=w.tolist();rec['strict_witness_m']=float(o['m']);rec['strict_witness_feasible']=bool(TP.feasible(x));rec['m_minus_bar']=float(o['m'])-rec['mbar']
    print(rec['bar'],w,'passmargin',rec['m_minus_bar'],'feasible',rec['strict_witness_feasible'])
# Optimize reference process density continuously and compare the finite reference search.
refchecks=[]
for b,name in [('9010','C70600 (90-10 Cu-Ni)'),('7030','C71500 (70-30 Cu-Ni)')]:
    c=np.array(BA.REFERENCE[name]); start=fullrefs[b][2][4:].numpy()
    def loss(p):return -float(truth.full(torch.tensor(np.r_[c,p]))['rho_m'])
    opt=minimize(loss,start,bounds=[(0,1)]*3,method='SLSQP',options={'ftol':1e-13,'maxiter':100})
    out=truth.full(torch.tensor(np.r_[c,opt.x]));ideal=.85-.3*float(TP.ln_rate(torch.tensor(c)))
    refchecks.append(dict(bar=b,nominal_wt=(c*[30,9.5,4.5,4]).tolist(),sobol_m=fullrefs[b][0],sobol_rho=fullrefs[b][1],optimized_m=float(out['m']),optimized_rho=float(out['rho_m']),physically_dense_m=ideal,apv=opt.x.tolist()))
print(pd.DataFrame(refchecks).to_string(index=False))
(outdir/'reference_checks.json').write_text(json.dumps(refchecks,indent=2));(outdir/'full_truth_floors.json').write_text(json.dumps(fullfloor,indent=2))
# Quantify melt-fraction conservation defects and missing-range handling.
badrows=G[G[[f'{p}_sol' for p in ['liquid','alpha','beta','kappa_fe','fcc_feni','nial','gprime','other']]].sum(axis=1)<.99]
print('Nonconserving sol points:',badrows.index.tolist())
(outdir/'grid_integrity.json').write_text(json.dumps({'n':len(G),'ok':int(G.ok.sum()),'missing_liquidus':int(G.liquidus_C.isna().sum()),'zero_phase_sum_sol':badrows.index.tolist(),'missing_alpha600_compositions':int(G.alpha600_xni.isna().sum()),'sha256_mcni':sha},indent=2))
# Persist only project workflow conventions, not findings.
Path('.prompts/MEMORY.md').write_text('''# Project Memory\n\n## Context\n- Independent copper-alloy benchmark reviews are delivered as `outputs/report.md`, with source extracts and machine-readable analysis outputs alongside it.\n\n## Notes\n- Reports distinguish executed calculations, inspected code/data, and delegated evidence checks; include severity-tagged findings, optimized floor/witness tables, uncertainty, and discretionary decisions.\n- Establish an independent fitting implementation before comparing supplied fit code. Do not silently overwrite uploaded inputs.\n- In this deployment, data-retrieval subagents did not see parent workspace files despite the shared-workspace guide; pass essential input content and recover evidence through returned messages or registered artifacts.\n''')

# === NEXT EXECUTED CELL ===

# Inspect substantive progress of bridge agents without blocking further local checks.
for tid in taskids[1:]:
    ms=await get_task_messages(tid)
    (outdir/f'agent_{tid}_messages.json').write_text(json.dumps(ms,default=str,indent=2))
    print('\nTASK',tid,'messages',len(ms))
    for m in ms[-8:]:
        if m.get('role')=='tool':print(str(m.get('content',''))[:10000])

# === NEXT EXECUTED CELL ===

# Retrieve final answers, preserving delegated provenance.
for tid in taskids[1:]:
    st=await check_task(tid)
    print('\nTASK',tid,st.status)
    if st.status=='success':
        (outdir/f'agent_{tid}_answer.md').write_text(st.answer); print(st.answer)

# === NEXT EXECUTED CELL ===

# Fetch complete exact table transcription from bridge-agent notebook messages.
ms=await get_task_messages(taskids[2]);(outdir/'bridge_agent_messages.json').write_text(json.dumps(ms,default=str,indent=2))
for i,m in enumerate(ms):
    c=str(m.get('content',''))
    if m['role']=='tool' and any(s in c for s in ['13.95','5.07','Cu-Al-Ni','transcriptions','3.77']):print('\nMESSAGE',i,'\n',c[:24000])

# === NEXT EXECUTED CELL ===

# Recover exact JSON transcription from the bridge-agent's executed code, not inferred prose.
for i,m in enumerate(ms):
    for tc in m.get('tool_calls',[]) or []:
        if tc['function']['name']=='run_cell':
            code=json.loads(tc['function']['arguments']).get('code','')
            if 'transcrip' in code or '13.95' in code or '5.07' in code:
                (outdir/f'bridge_code_{i}.py').write_text(code)
                print('\nCODE',i,'\n',code[:18000])

# === NEXT EXECUTED CELL ===

# Download newly found primary PDFs locally and cite each source before using its data.
newdoi={'Gudic2021':'10.2298/CICEQ200701007G','Southwell1966':'10.21236/ad0644930','Dhar1985':'10.5006/1.3582011'}
for k,doi in newdoi.items():
    try:(sources/f'{k}.bib').write_text(await cite_doi(doi))
    except Exception as ex:print('citation',k,type(ex).__name__)
for k,url in {'Gudic2021':'https://www.ache-pub.org.rs/CICEQ/2021/No4/CICEQ_No4_2021/08_4854_2021.pdf','Southwell1966':'https://archive.org/download/DTIC_AD0644930/DTIC_AD0644930.pdf'}.items():
    res=requests.get(url,timeout=120); print(k,res.status_code,len(res.content))
    if res.status_code==200 and res.content.startswith(b'%PDF'):
        (sources/f'{k}.pdf').write_bytes(res.content)
        subprocess.run(['pdftotext','-layout',str(sources/f'{k}.pdf'),str(sources/f'{k}.txt')],check=True)
# Parse literal transcription assignment via ast.literal_eval, without executing external code.
import ast
code=(outdir/'bridge_code_89.py').read_text(); tree=ast.parse(code)
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='transcription' for t in node.targets): trans=ast.literal_eval(node.value)
(outdir/'bridge_exact_transcription.json').write_text(json.dumps(trans,indent=2))
print((sources/'Gudic2021.txt').read_text()[5000:16000])

# === NEXT EXECUTED CELL ===

# Recover full low-Ni audit final and numerical transcription (isolated workspace).
st=await check_task(taskids[1]);print(st.status);(outdir/f'agent_{taskids[1]}_answer.md').write_text(st.answer)
print(st.answer[:29000])
lowmsgs=await get_task_messages(taskids[1]);(outdir/'lowNi_agent_messages.json').write_text(json.dumps(lowmsgs,default=str,indent=2))
for i,m in enumerate(lowmsgs):
    for tc in m.get('tool_calls',[]) or []:
        if tc['function']['name']=='run_cell':
            co=json.loads(tc['function']['arguments']).get('code','')
            if any(term in co for term in ['1.6,','1.6, ','NCEL','13.95','99.90','1968','0.012']):
                (outdir/f'lowNi_code_{i}.py').write_text(co)
                if 'add(' in co or 'ncel' in co.lower() or 'rows=' in co:print('\nCODE',i,'\n',co[:27000])

# === NEXT EXECUTED CELL ===

# Print specific low-Ni transcription code only (avoid the lengthy prose report).
for pth in sorted(outdir.glob('lowNi_code_*.py')):
    co=pth.read_text()
    if ('6.25' in co or 'NCEL' in co) and ('records' in co or 'ncel' in co.lower()):
        print('\nFILE',pth.name,'LEN',len(co),'\n',co[:36000])

# === NEXT EXECUTED CELL ===

co=(outdir/'lowNi_code_152.py').read_text()
print(co[5000:12500])
# Download exact original report for independent table checks.
url68='https://archive.org/download/corrosionofmater04rein/corrosionofmater04rein.pdf'
rr68=requests.get(url68,timeout=120);print('report',rr68.status_code,len(rr68.content))
if rr68.content.startswith(b'%PDF'):
    (sources/'Reinhart1968.pdf').write_bytes(rr68.content);subprocess.run(['pdftotext','-layout',str(sources/'Reinhart1968.pdf'),str(sources/'Reinhart1968.txt')],check=True)
# Save a full primary-report citation verified from retrieval.
save_citation('''@techreport{Reinhart1968hydrospace,
 author={Reinhart, Fred M.}, title={Corrosion of Materials in Hydrospace. Part IV. Copper and Copper Alloys}, institution={Naval Civil Engineering Laboratory}, address={Port Hueneme, California}, number={Technical Note N-961}, year={1968}, url={https://archive.org/details/corrosionofmater04rein}, note={Original report downloaded and tables inspected, accessed 2026-10-28}}
''')

# === NEXT EXECUTED CELL ===

# Recreate historical source records from inspected, bounded code section only.
co=(outdir/'lowNi_code_152.py').read_text();histcode=co[:co.index("print('Historical primary rows'")]
ns={'json':json};exec(histcode,ns);Hraw=pd.DataFrame(ns['rows'])
H=[]
for r in ns['rows']:
    c=json.loads(r['composition_wt_pct'])
    H.append(dict(study=r['test_group'],alloy=r['alloy_label'],ni=c.get('Ni',0),al=c.get('Al',0),fe=c.get('Fe',0),mn=c.get('Mn',0),rate=r['rate_value'],weight=.5,unit=r['rate_unit'],source=r['source_url']+' '+r['table_or_section']+' p'+str(r['printed_page']),test=r['environment']+' '+str(r['test_duration_days'])+'d',use=1,attack=r['attack_as_reported'],participant=r['participant'],censored=r['rate_qualifier']!='='))
H=pd.DataFrame(H);H.to_csv(outdir/'historical_bridge_data.csv',index=False);Hraw.to_csv(outdir/'historical_bridge_metadata.csv',index=False)
print('Original source historical rows',H.shape)
# Check original table text and retain source pages, not just returned delegated records.
htxt=(sources/'Reinhart1968.txt').read_text();hpages=htxt.split('\f')
for pn in [29,30,45,49,58,61,62,63,64]:
    (sources/f'Reinhart1968_page{pn}.txt').write_text(hpages[pn-1])
print('Original composition table page 61\n',hpages[60][:15000])
print('Rate table page62\n',hpages[61][:15000])
print('Chronology page 30\n',hpages[29][:15000])

# === NEXT EXECUTED CELL ===

# Rotate original scanned tabular pages for verifiable local inspection (no graph digitization).
from PIL import Image
for pn in [30,61,62,63,64]:
    prefix=sources/f'Reinhart1968_p{pn}'
    subprocess.run(['pdftoppm','-f',str(pn),'-l',str(pn),'-scale-to','2800','-png','-singlefile',str(sources/'Reinhart1968.pdf'),str(prefix)],check=True,capture_output=True)
    im=Image.open(str(prefix)+'.png'); print(pn,im.size);im.rotate(90,expand=True).save(sources/f'Reinhart1968_p{pn}_rotated.png')
# Bridge sensitivity variants: isolate one matched deployment, then a whole-program influence-capped fit.
B=H[H.study.eq('Reinhart1968_I-3_123d_W_NCEL')].copy()
print('Matched 123d NCEL bridge\n',B.to_string(index=False))
scenario('Add 123d Cu/CuNi-only bridge',pd.concat([Dc,B[B.al==0]],ignore_index=True))
scenario('Add 123d Cu/CuNi/Al bronze bridge',pd.concat([Dc,B],ignore_index=True))
# Whole historic report total weight=2, rather than 71 independent equal-weight study observations.
HC=H[~H.censored].copy();HC['weight']=2/len(HC)
scenario('Add all historical bridges; report weight2',pd.concat([Dc,HC],ignore_index=True))
HN=HC[HC.al==0].copy();HN['weight']=2/len(HN)
scenario('Add all historical Cu/CuNi; report weight2',pd.concat([Dc,HN],ignore_index=True))
scenario('Strict data +123d Cu/CuNi bridge',pd.concat([Dc[Dc.study.isin(['Tan2024','Qian2025'])],B[B.al==0]],ignore_index=True))
# New zero-Ni Cu-Al controls outside the binary series: low-weight sensitivity, not target-domain validation.
C=[]
for comp,rate in zip(trans['ciceq']['table1_compositions_wt_percent'],trans['ciceq']['table2_icorr_uA_cm2']):
    C.append(dict(study='Gudic2021',alloy=comp['material'],ni=float(comp.get('Ni',0)),al=float(comp.get('Al',0)),fe=0,mn=float(comp.get('Mn',0)),rate=float(rate),weight=.5,unit='uA/cm2',test='0.5M NaCl; 20C; OCP60min+EIS then polarization',source='10.2298/CICEQ200701007G Tables1,2',use=1))
C=pd.DataFrame(C);C.to_csv(outdir/'gudic_bridge_data.csv',index=False)
scenario('Add Gudic Cu/CuAl pair only',pd.concat([Dc,C.iloc[:2]],ignore_index=True))
scenario('Add Gudic all alloys (outside box)',pd.concat([Dc,C],ignore_index=True))
(outdir/'source_sensitivity.json').write_text(json.dumps(scenarios,indent=2));(outdir/'refits.json').write_text(json.dumps({'models':models,'floors':floorresults+scenarios},indent=2))

# === NEXT EXECUTED CELL ===

for pn in [30,61,62,63,64]:
    im=Image.open(sources/f'Reinhart1968_p{pn}.png');im.rotate(-90,expand=True).save(sources/f'Reinhart1968_p{pn}_upright.png')

# === NEXT EXECUTED CELL ===

# Share passing is a measure on design distribution, not volume in composition alone.
# Execute an independently seeded uniform design diagnostic, not the missing check_phys.py.
X=torch.quasirandom.SobolEngine(7,scramble=True,seed=2728).draw(262144).double();vv=truth.full(X);feas=TP.feasible(X)
share=[]
for b in REFS:
    passed=vv['m']>=fullrefs[b][0]
    share.append(dict(bar=b,n=len(X),feasible_fraction=float(feas.double().mean()),pass_fraction_given_feasible=float(passed[feas].double().mean()),pass_fraction_box=float((passed&feas).double().mean()),seed=2728))
print(share)
# Optimize smooth soft-gated objective with constrained SLSQP from the best screened Sobol points.
mb=fullrefs['9010'][0];J=BA.objective_from(vv['U'],vv['m'],X,mb);J[~feas]=-1e5
idxs=torch.topk(J,8).indices;candidate=[]
for ix in idxs:
    x0=X[ix].numpy();
    def obj(x):
        xx=torch.tensor(x);o=truth.full(xx);return -float(BA.objective_from(o['U'],o['m'],xx,mb))
    def limits(x):
        xx=torch.tensor(x);w=TP.wt(xx[:4]);n,a,f,m=w.tolist()
        return np.array([35-w.sum(),(1250-TP.field(xx[:4],'liquidus_C'))/100, (n-f)/30 if a>7 else 1.,(2.3-f)/4.5 if a<1.5 else 1.],float)
    op=minimize(obj,x0,bounds=[(0,1)]*7,constraints={'type':'ineq','fun':limits},method='SLSQP',options={'ftol':1e-10,'maxiter':200})
    if limits(op.x).min()>-1e-7:candidate.append(op)
best=min(candidate,key=lambda r:r.fun);xx=torch.tensor(best.x);outs=truth.full(xx)
optrec={'J':-float(best.fun),'wt':(best.x[:4]*[30,9.5,4.5,4]).tolist(),'apv':best.x[4:].tolist(),'outputs':{k:float(v) for k,v in outs.items()},'strength_MPa':float(TP.strength_mpa(xx[:4])),'liquidus':float(TP.field(xx[:4],'liquidus_C')),'successful':bool(best.success)}
print(optrec)
(outdir/'independent_design_diagnostics.json').write_text(json.dumps({'shares':share,'optimum_found':optrec},indent=2))

# === NEXT EXECUTED CELL ===

# Inspect all resource references and truth-switch logic; do not infer absent policy enforcement.
lines=Path('bofn_alloy.py').read_text().splitlines()
for i,l in enumerate(lines):
    if any(s in l for s in ['truth_phys','BOFN_TRUTH','feasible(','phys_m_ref','TRUTH ==','m_ref']):
        print(i+1,'\n'+'\n'.join(lines[max(0,i-2):min(len(lines),i+5)]))
# Save coefficients and witnesses in compact extractable tables.
def witness(r,b):
    cert=r[b].get('certificate')
    if cert and cert.get('proposal_feasible') and cert.get('witness') is not None:return cert['witness']
    return r[b]['witness']
for r in floorresults+scenarios:
    if r['fit'] in ['Base','Free signs','Linear Al','Add Mn','Add Ni x Al','Drop Lewis + Zhao (weak rows)','Strict data +123d Cu/CuNi bridge','Add 123d Cu/CuNi-only bridge','Add 123d Cu/CuNi/Al bronze bridge']:
        print(r['fit'], models[r['fit']]['coef'])
        print([(b,r[b]['floor'],witness(r,b)) for b in REFS])
# Store current notebook cell sources as a transparent execution log.
history=get_ipython().history_manager.input_hist_raw
(outdir/'executed_analysis_cells.py').write_text('\n\n# === NEXT EXECUTED CELL ===\n\n'.join(history[1:]))