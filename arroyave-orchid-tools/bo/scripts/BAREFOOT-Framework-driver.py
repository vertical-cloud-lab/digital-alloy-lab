"""Scaled-down runs of BAREFOOT sample_code.py configurations on one node.

usage: python BAREFOOT-Framework-driver.py <mode> <iterLimit> <hpCount> <sampleCount> <batchSize> [ray_cpus]
  mode = batch  : sample_code.runBatch settings (reification=False, batch=True)
  mode = reifi  : sample_code.runReifi as shipped (NB: also reification=False, batch=True)
  mode = full   : reification=True, batch=True, multiNode=0 (single-node BAREFOOT; runBAREFOOT needs SLURM)
Run with cwd = a copy of the BAREFOOT repo (imports barefoot.py and sample_code.py from there).
"""
import sys, os, time
import numpy as np
mode, iterLimit, hpCount, sampleCount, batchSize = sys.argv[1], *map(int, sys.argv[2:6])
ray_cpus = int(sys.argv[6]) if len(sys.argv) > 6 else 2
sys.path.insert(0, os.getcwd())
import ray
ray.init(num_cpus=ray_cpus, include_dashboard=False, log_to_driver=False)
from ray.util.multiprocessing import Pool as RayPool
import barefoot as bf_mod
bf_mod.Pool = lambda *a, **k: RayPool(processes=ray_cpus)   # cap workers on the shared box
from sample_code import rom1, rom2, rom3, truth
np.random.seed(0)
reif = mode == "full"
calc = {"batch": "BatchOnly", "reifi": "ReificationOnly", "full": "FullSingleNode"}[mode]
kw = dict(TruthModel=truth, calcInitData=True, multiNode=0, workingDir=".", calculationName=calc + os.environ.get("CALCSUFFIX", ""), nDim=2,
          input_resolution=5, restore_calc=False, updateROMafterTM=False, externalTM=False, acquisitionFunc="EI",
          A=[], b=[], Aeq=[], beq=[], lb=[], ub=[], func=[], keepSubRunning=True, verbose=False, sampleScheme="LHS",
          tmSampleOpt="EI", logname="BAREFOOT", maximize=True, train_func=[], reification=reif, batch=True)
if mode == "batch":
    kw["initDataPathorNum"] = [2]
else:
    kw["ROMModelList"] = [rom1, rom2, rom3]; kw["initDataPathorNum"] = [2, 2, 2, 2]
fw = bf_mod.barefoot(**kw)
modelParam = {'model_l': [[0.1608754, 0.2725361], [0.17094462, 0.28988983], [0.10782092, 0.18832378]],
              'model_sf': [6.95469898, 8.42299498, 2.98009081], 'model_sn': [0.05, 0.05, 0.05],
              'means': [-2.753353101070388e-16, -1.554312234475219e-16, 4.884981308350689e-17],
              'std': [1.2460652976290285, 1.3396622409903254, 1.3429644403939915],
              'err_l': [[0.1, 0.1], [0.1, 0.1], [0.1, 0.1]], 'err_sf': [1, 1, 1], 'err_sn': [0.01, 0.01, 0.01],
              'costs': [1, 1, 1, 1]}
fw.initialize_parameters(modelParam=modelParam, covFunc="M32", iterLimit=iterLimit, sampleCount=sampleCount,
                         hpCount=hpCount, batchSize=batchSize, tmIter=int(os.environ.get("TMITER", "5")), upperBound=1, lowBound=0.0001,
                         fusedPoints=10, fusedHP=[3, 0.1, 0.1])
t0 = time.time(); fw.run_optimization(); print(f"run_optimization wall {time.time()-t0:.1f} s")
print("maxTM", fw.maxTM)
# BAREFOOT catches exceptions inside run_optimization and only logs them, so check the log explicitly.
log = open("BAREFOOT.log").read()
if "Optimization Code Failed" in log:
    print("BAREFOOT reported: Optimization Code Failed (see BAREFOOT.log)"); sys.exit(2)
print("BAREFOOT finished without logged failure")
