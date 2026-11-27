#!/bin/bash
# NiTi-alloy-discovery Iter3 smoke test (run inside /tmp/sbx/clean). Work copy excludes the 3 x 122 MB all_space.csv.
# Patches (work copy only): N_GP 1000->3, Batch_size 29->3, joblib n_jobs cpu_count->2,
# and evaluate EHVI on every 20th of the 13,517 feasible candidates (priors subsampled consistently).
set -u
PY=/tmp/arroyave/venvs/NiTi-alloy-discovery/bin/python
cd /tmp/arroyave/work/NiTi-alloy-discovery/Iter3
mkdir -p shipped && cp -n x_query.csv all_improvements.csv all_candidates.csv shipped/ 2>/dev/null
sed -i 's/^N_GP=1000;/N_GP=3;/; s/^Batch_size=29/Batch_size=3/; s/n_jobs=multiprocessing.cpu_count()/n_jobs=2/' main.py
$PY - <<'PYEOF'
import re
src = open("main.py").read()
anchor = "test_priors = [[hys_prior_tests],[ent_prior_tests],[TS_prior_tests]]\n"
assert anchor in src, "anchor not found"
add = ("_sub = np.arange(0, N_test, 20)  # smoke test: every 20th candidate\n"
       "x_test = x_test[_sub]; p_test = p_test[_sub]; N_test = x_test.shape[0]\n"
       "test_priors = [[hys_prior_tests[_sub]],[ent_prior_tests[_sub]],[TS_prior_tests[_sub]]]\n"
       "print('candidates evaluated:', N_test, flush=True)\n")
if "_sub = np.arange" not in src:
    src = src.replace(anchor, anchor + add, 1)
open("main.py", "w").write(src)
PYEOF
grep -nE '^N_GP|^Batch_size|n_jobs=|_sub' main.py
t0=$(date +%s); timeout 300 $PY main.py 2>&1 | tail -5; echo "rc=${PIPESTATUS[0]} wall=$(( $(date +%s)-t0 ))s"
echo "--- smoke-test x_query.csv"; cat x_query.csv; echo "--- all_improvements.csv"; cat all_improvements.csv
