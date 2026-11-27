#!/bin/bash
# BRAVE smoke test (run inside /tmp/sbx/clean). Work copy: /tmp/arroyave/work/BRAVE.
set -u
PY=/tmp/arroyave/venvs/BRAVE/bin/python
S=/tmp/arroyave/results/bo/scripts
B=/tmp/arroyave/work/BRAVE/code/bbo_python
P=/tmp/arroyave/work/BRAVE/code/Probability_calculations
step() { echo "=== $1  ($(date -u +%T))"; }
step "make inputs (N_GP=10, 120 feasible + 60 infeasible candidates)"
$PY -I $S/BRAVE-make_inputs.py /tmp/arroyave/work/BRAVE/data/HTMDEC_Y2_db.xlsx $B $P 10 120 60 20000
step "prior_eval.py as shipped"
cd $B && PYTHONPATH=.. timeout 300 $PY prior_eval.py 2>&1 | grep -v -i 'warn' | tail -6; echo "rc=${PIPESTATUS[0]}"
step "patch priors.py column names to match data/HTMDEC_Y2_db.xlsx"
sed -i 's/"YS (MPa)"/"Yield Strength (MPa)"/g; s/"UTS \/ YS"/"UTS\/YS"/g; s/"EL (%)"/"Elong_T (%)"/g' priors.py
t0=$(date +%s); PYTHONPATH=.. timeout 300 $PY prior_eval.py 2>&1 | grep -v -i 'warn' | tail -6; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
step "YS_pb (Peierls-Nabarro-type prior) on x_test"
PYTHONPATH=.. timeout 120 $PY -c "
import numpy as np, pandas as pd
from YS_pb import YS_pb
x = pd.read_csv('x_test.csv', header=None).to_numpy()
v = np.asarray(YS_pb(x)).reshape(-1)
pd.DataFrame(v.reshape(-1,1)).to_csv('YS_pb_prior.csv', header=None, index=None)
print('YS_pb prior: n=%d min=%.1f median=%.1f max=%.1f' % (v.size, v.min(), np.median(v), v.max()))
" 2>&1 | tail -4
step "main.py: N_GP 1000->10, Batch_size 16->4, joblib n_jobs cpu_count->2"
sed -i 's/^N_GP=1000;/N_GP=10;/; s/^Batch_size=16/Batch_size=4/; s/n_jobs=multiprocessing.cpu_count()/n_jobs=2/' main.py
grep -nE '^N_GP|^Batch_size|n_jobs=' main.py
t0=$(date +%s); PYTHONPATH=.. timeout 400 $PY main.py 2>&1 | grep -v -i 'warn' | tail -8; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
ls -la x_query.csv all_candidates.csv all_improvements.csv 2>&1
step "Probability_calculations/main.py on a 20,000-point stand-in all_space.csv"
cd $P && t0=$(date +%s); PYTHONPATH=.. timeout 300 $PY main.py 2>&1 | tail -6; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
