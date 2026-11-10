#!/bin/bash
# Driver: scaled-down comparison of the constraint-satisfaction campaign scripts.
# Original defaults: seeds 1-200, 100 iterations, 25 workers. Here: seeds 1-2, 20 iterations, 2 workers,
# plots only every 10 iterations. Run inside the scrubbed wrapper:
#   /tmp/sbx/clean bash scripts/constraint-satisfaction-run.sh
set -u
W=/tmp/arroyave/work/constraint-satisfaction
PY=/tmp/arroyave/venvs/constraint-satisfaction/bin/python
cd "$W"
for s in campaign_const_w_priors campaign_const_NO_priors campaign_pehvi campaign_ehvi_pof campaign_random; do
  t0=$(date +%s)
  timeout 300 $PY $s.py --seeds 1-2 --iterations 20 --workers 2 \
      --results-dir results_$s --plots-dir plots_$s --plot-every 10 > log_$s.txt 2>&1
  rc=$?
  echo "$s rc=$rc wall=$(( $(date +%s)-t0 ))s"
done
