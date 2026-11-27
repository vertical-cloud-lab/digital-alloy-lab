#!/bin/bash
# README quick smoke runs for PCMOBO (CPU), each in its own results dir under the work copy.
W=/tmp/arroyave/work/pcmobo; B=/tmp/arroyave/venvs/pcmobo/bin; L=/tmp/arroyave/results/bo/logs
run() { name=$1; shift; S=$(date +%s); /tmp/sbx/clean bash -c "cd $W && timeout 300 $*" > $L/PCMOBO-$name.log 2>&1; echo "$name rc=$? t=$(( $(date +%s)-S ))s"; }
run help-synthetic "$B/pcmbo-synthetic --help"
run smoke-synthetic "$B/pcmbo-synthetic --benchmark constrained_branin_currin --policy qlogpof --seeds 1 --iterations 1 --n-init 8 --workers 1 --results-dir runs/synthetic/smoke --device cpu --acq-mc-samples 16 --acq-raw-samples 16 --acq-num-restarts 1"
run smoke-hea "$B/pcmbo-hea --policy pof --seeds 1 --iterations 1 --n-init 2 --workers 1 --results-dir runs/hea_design/smoke --device cpu --acq-mc-samples 16 --acq-raw-samples 16 --acq-num-restarts 1 --acq-batch-eval-size 128"
run smoke-estm "$B/pcmbo-estm --policy qlogpof --seeds 1 --iterations 1 --n-init 3 --workers 1 --results-dir runs/estm_thermoelectric/smoke --device cpu --acq-mc-samples 16 --acq-raw-samples 16 --acq-num-restarts 1 --acq-batch-eval-size 128"
