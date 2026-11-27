#!/bin/bash
# PCMOBO HEA finite-pool campaign (40,553 Nb-Mo-Ta-V-W-Cr candidates): compare fixed and adaptive policies, scaled down.
W=/tmp/arroyave/work/pcmobo; B=/tmp/arroyave/venvs/pcmobo/bin; L=/tmp/arroyave/results/bo/logs
for pol in pof pehvi bandit_ucb_switch; do
  S=$(date +%s)
  /tmp/sbx/clean bash -c "cd $W && timeout 240 $B/pcmbo-hea --policy $pol --seeds 1 --iterations 15 --n-init 10 --workers 1 --results-dir runs/hea_design/cmp_$pol --device cpu --acq-mc-samples 32 --acq-raw-samples 32 --acq-num-restarts 1 --acq-batch-eval-size 512" > $L/PCMOBO-hea-$pol.log 2>&1
  echo "$pol rc=$? t=$(( $(date +%s)-S ))s"
done
