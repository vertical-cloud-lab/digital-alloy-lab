"""Independent truth checks. Run python outputs/truth_checks.py /workspace.
Requires torch, botorch, gpytorch; no GP fitting or comparison implementation is used.
"""
from pathlib import Path
import sys,importlib.util,json
import torch,numpy as np,pandas as pd
root=Path(sys.argv[1] if len(sys.argv)>1 else '/workspace');sys.path.insert(0,str(root))
import bofn_alloy as cu
spec=importlib.util.spec_from_file_location('al_truth_check',root/'al_bofn_alloy.py');al=importlib.util.module_from_spec(spec);spec.loader.exec_module(al)
torch.set_num_threads(1)
out=root/'outputs'/'reproduced';out.mkdir(exist_ok=True)
aopt=json.loads((root/'al_optimum.json').read_text())['kappa1'];copt=json.loads((root/'truth_tables.json').read_text())[0]['optimum'];nopt=json.loads((root/'landscape.json').read_text())[2]['optimum']
ta,tc=al.AlloyTruth(1.),cu.AlloyTruth(1.,1.);g=torch.Generator().manual_seed(641207)
parts=[]
for i in range(10):
 X=torch.rand(100000,7,generator=g);oc=tc.full(X)
 ya=ta.objective(X)/aopt;yc=tc.objective(X,oc)/copt;yn=(oc['U']-.3*cu.burden(X))/nopt
 z=cu.node_input('m',X,oc).clone();z[:,3]=1.;md=tc.node('m',z)
 parts.append(np.column_stack([ya.numpy(),yc.numpy(),yn.numpy(),oc['m'].numpy(),md.numpy(),oc['rho_m'].numpy(),X[:,0].numpy()]))
R=np.concatenate(parts)
rows=[]
for j,name in enumerate(['Al','Cu','No-gate']):
 y=R[:,j];rows.append(dict(truth=name,median_pct=100*np.median(y),positive_pct=100*(y>0).mean(),above60_pct=100*(y>=.6).mean(),above80_pct=100*(y>=.8).mean()))
pd.DataFrame(rows).to_csv(out/'fresh_truth_audit.csv',index=False)
print(pd.DataFrame(rows).to_string(index=False));print('Immersion pass / fully dense / rho>=.9:',100*(R[:,3]>=cu.M_REF).mean(),100*(R[:,4]>=cu.M_REF).mean(),100*(R[:,5]>=.9).mean())
# Re-evaluate hidden outcomes only as a diagnostic, never as purchased observations.
rows=[]
for folder in ['results/k1e1','quality/results-light/k1e1']:
 for p in (root/folder).glob('*.json'):
  r=json.loads(p.read_text())
  for j,b in enumerate(r['builds']):
   x=torch.tensor(b['c']+[b['a']]+b['pv']);o=tc.full(x)
   rows.append(dict(policy=r['kind'],seed=r['seed'],build=j,new=j>=5,w=float(o['w']),m=float(o['m']),J=float(tc.objective(x,o)),Ni=30*b['c'][0],immersed=b['m'] is not None,complete=b['J'] is not None,pass_immersion=float(o['m'])>=cu.M_REF))
pd.DataFrame(rows).to_csv(out/'build_truth_rescore.csv',index=False)
