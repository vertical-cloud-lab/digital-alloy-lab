#!/bin/bash
# HTMDEC bbo_python smoke test (run inside /tmp/sbx/clean). Work copy: /tmp/arroyave/work/HTMDEC.
# 1) shipped script as-is (iteration_current = 2 hard-coded); 2) patched: iteration from $ITER and opt_folder
#    defined for iterations > 1; GP count (100) and batch size (20) left at the shipped values.
set -u
PY=/tmp/arroyave/venvs/HTMDEC/bin/python
cd /tmp/arroyave/work/HTMDEC/bbo_python
echo "=== shipped package_BBO_single_iteration.py"
timeout 120 $PY package_BBO_single_iteration.py 2>&1 | tail -4; echo "rc=${PIPESTATUS[0]}"
cp package_BBO_single_iteration.py run_iter.py
$PY - <<'PYEOF'
s = open("run_iter.py").read()
old = "iteration_current = 2\n"
assert old in s
s = s.replace(old, "import os\niteration_current = int(os.environ.get('ITER', '1'))\n"
              "opt_folder = 'Test Optimization Iteration/testBOloop_specificmetadata'  # patch: undefined for ITER>1\n", 1)
open("run_iter.py", "w").write(s)
PYEOF
for it in 1 2 3 4 5; do
  echo "=== ITER=$it ($(date -u +%T))"; t0=$(date +%s)
  ITER=$it timeout 240 $PY run_iter.py 2>&1 | grep -vE '^\s*$' | tail -6; rc=${PIPESTATUS[0]}
  echo "rc=$rc wall=$(( $(date +%s)-t0 ))s"; [ $rc -ne 0 ] && break
done
ls "Test Optimization Iteration/testBOloop_specificmetadata"
# Second patch (applied after the first pass failed at ITER=2 with NameError): guard the early
# print(...data_input...) lines with `if iteration_current == 1:`; then rerun ITER=2..5 (HTMDEC-run2 in the log).
# Third patch (ITER=2 then failed at `dimensions_input_number = data_input[...]`): load
# inputSpace_from1000_size20_iter{ITER}.xlsx right after iteration_current is set; rerun ITER=2..5 (HTMDEC-bbo-run3.log).
