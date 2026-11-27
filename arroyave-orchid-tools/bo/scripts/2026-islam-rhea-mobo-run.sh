#!/bin/bash
# Reproduce the rhea-mobo runs (2026-islam-rhea-mobo). Run from anywhere; uses /tmp/arroyave layout.
set -e
UV=/home/runner/.local/bin/uv; W=/tmp/arroyave/work/rhea-mobo; V=/tmp/arroyave/venvs
cp -r /tmp/arroyave/src/ArroyaveLab__2026-islam-rhea-mobo "$W"
# 1) toy env (README's license-free path), CPU torch
/tmp/sbx/clean $UV venv --python 3.12 $V/rhea-mobo
/tmp/sbx/clean $UV pip install --python $V/rhea-mobo/bin/python --torch-backend cpu -r $W/requirements-toy.txt pytest
/tmp/sbx/clean bash -c "cd $W && PYTHONPATH=src timeout 600 $V/rhea-mobo/bin/python -m rhea_mobo.toy --output toy-output-default"
for s in 42 7; do
  /tmp/sbx/clean bash -c "cd $W && PYTHONPATH=src timeout 400 $V/rhea-mobo/bin/python -m rhea_mobo.toy --output toy-output-it15-s$s --iterations 15 --seed $s"
done
# 2) full project env (do NOT use `uv sync`: uv.lock resolves CUDA torch + nvidia-* wheels on x86_64)
/tmp/sbx/clean $UV venv --python 3.12 $V/rhea-mobo-full
/tmp/sbx/clean $UV pip install --python $V/rhea-mobo-full/bin/python --torch-backend cpu -e $W pytest
/tmp/sbx/clean bash -c "cd $W && timeout 600 $V/rhea-mobo-full/bin/python -m pytest tests/ -v -p no:cacheprovider"
/tmp/sbx/clean bash -c "cd $W && timeout 300 $V/rhea-mobo-full/bin/python scripts/predicted_correlation.py"
/tmp/sbx/clean bash -c "cd $W && timeout 120 $V/rhea-mobo-full/bin/rhea-mobo" || echo "expected: needs licensed tc_python"
# 3) plot
cd $W && /tmp/arroyave/venvs/bo-plot/bin/python /tmp/arroyave/results/bo/scripts/2026-islam-rhea-mobo-plot.py \
  toy-output-it15-s42 "seed 42" toy-output-it15-s7 "seed 7" /tmp/arroyave/results/bo/figures/2026-islam-rhea-mobo-toy-hv.png
