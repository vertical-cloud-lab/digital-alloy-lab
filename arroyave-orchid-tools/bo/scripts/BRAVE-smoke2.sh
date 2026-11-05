#!/bin/bash
# BRAVE smoke test, second pass (after `uv pip install "setuptools<81"` so CBFV can import pkg_resources).
# Shows the shipped priors.py failing on column names, applies the column-name patch (which then hits the
# index-alignment CatBoostError; fixed by hand afterwards with .reset_index(drop=True), see BRAVE-smoke3.sh),
# stubs YS_pb (table.dat missing) and shrinks main.py (N_GP=10, Batch_size=4 from BRAVE-smoke.sh).
set -u
PY=/tmp/arroyave/venvs/BRAVE/bin/python
B=/tmp/arroyave/work/BRAVE/code/bbo_python
step() { echo "=== $1  ($(date -u +%T))"; }
cd $B
cp /tmp/arroyave/src/ArroyaveLab__BRAVE/code/bbo_python/priors.py priors.py
step "prior_eval.py as shipped (180 candidate compositions)"
PYTHONPATH=.. timeout 300 $PY prior_eval.py 2>&1 | grep -v -i 'warn' | tail -4; echo "rc=${PIPESTATUS[0]}"
step "patch priors.py column names to match data/HTMDEC_Y2_db.xlsx"
sed -i 's/"YS (MPa)"/"Yield Strength (MPa)"/g; s/"UTS \/ YS"/"UTS\/YS"/g; s/"EL (%)"/"Elong_T (%)"/g' priors.py
t0=$(date +%s); PYTHONPATH=.. timeout 300 $PY prior_eval.py 2>&1 | grep -v -i 'warn' | tail -4; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
step "stub YS_pb (table.dat missing): zeros prior"
$PY -c "import pandas as pd, numpy as np; n=len(pd.read_csv('x_test.csv',header=None)); pd.DataFrame(np.zeros((n,1))).to_csv('YS_pb_prior.csv',header=None,index=None)"
sed -i 's/^from YS_pb import YS_pb/YS_pb = lambda x: np.zeros(len(x))  # smoke-test stub: table.dat is not in the repo/' main.py
step "main.py"
t0=$(date +%s); PYTHONPATH=.. timeout 400 $PY main.py 2>&1 | grep -v -i 'warn' | tail -8; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
# Then (by hand): sed -i -E 's/^(df = df\[\(df\[.*\] != 0\)\])$/\1.reset_index(drop=True)/' priors.py ; run BRAVE-smoke3.sh
# Final passing run: sed N_GP=2, Batch_size=2 in main.py; PYTHONPATH=.. timeout 330 python main.py  (log: BRAVE-main-NGP2.log)
