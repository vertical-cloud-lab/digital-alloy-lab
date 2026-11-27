#!/bin/bash
# Run tamubo examples/bo/minimization_2d.py for the three frameworks on CPU (config edited in the work copy).
W=/tmp/arroyave/work/tamubo; PY=/tmp/arroyave/venvs/tamubo/bin/python; L=/tmp/arroyave/results/bo/logs
for fw in botorch_optimize_ei botorch_grid_ei sklearn_grid_ei; do
  cat > $W/examples/bo/minimization_2d_config.json <<JSON
{"framework": "$fw", "max_iters": 10, "grid_resolution": 101, "num_restarts": 10, "raw_samples": 128,
 "gp_sk": true, "maxiter": 200, "device": "cpu", "validation": false, "verbose": true,
 "log_filename": "cpu_$fw.json"}
JSON
  S=$(date +%s)
  /tmp/sbx/clean bash -c "cd $W && timeout 300 $PY examples/bo/minimization_2d.py" > $L/tamubo-bo-$fw.log 2>&1
  echo "$fw rc=$? t=$(( $(date +%s)-S ))s"
done
