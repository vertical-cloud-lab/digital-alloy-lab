#!/bin/bash
# BRAVE smoke test, third pass. Work-copy patches already applied by BRAVE-smoke2.sh and by hand:
#  priors.py: column names -> "Yield Strength (MPa)", "UTS/YS", "Elong_T (%)"; .reset_index(drop=True) after each filter
#  main.py:   N_GP=10, Batch_size=4, n_jobs=2, YS_pb stubbed to zeros (table.dat missing)
set -u
PY=/tmp/arroyave/venvs/BRAVE/bin/python
B=/tmp/arroyave/work/BRAVE/code/bbo_python
step() { echo "=== $1  ($(date -u +%T))"; }
cd $B
step "prior_eval.py with patched priors.py"
t0=$(date +%s); PYTHONPATH=.. timeout 300 $PY prior_eval.py 2>&1 | grep -v -i 'warn' | tail -4; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
wc -l YS_prior.csv EUTS_prior.csv UTStoYS_prior.csv
step "main.py"
t0=$(date +%s); PYTHONPATH=.. timeout 400 $PY main.py 2>&1 | grep -v -i 'warn' | tail -8; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
ls -la x_query.csv all_candidates.csv all_improvements.csv x_query_indices.csv 2>&1
