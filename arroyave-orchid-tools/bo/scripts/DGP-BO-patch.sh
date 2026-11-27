#!/bin/bash
# Make CPU, small-budget copies of the DGP-BO scripts (run inside a copy of the repo's code/ dir).
# Changes: BO loop 'for k in range(500)' -> NBO env var; EHVI joblib n_jobs=cpu_count() -> NJOBS env var (default 2);
# strip '.cuda()' calls. Nothing else is modified.
for f in gp-tec-MO-11 mtgp-tec-MO-11 dgp-iso-tec-MO-11; do
  sed -e 's/for k in range(500):/for k in range(int(__import__("os").environ.get("NBO","500"))):/' \
      -e 's/n_jobs=multiprocessing.cpu_count()/n_jobs=int(__import__("os").environ.get("NJOBS","2"))/' \
      -e 's/\.cuda()//g' $f.py > $f-cpusmall.py
done
sed -e "s/\.cuda()//g" -e "s/n_jobs=multiprocessing.cpu_count()/n_jobs=2/" dgp-het-tec-MO-11-cuda.py > dgp-het-tec-MO-11-cpu.py   # capsule entry, CPU copy; its own BO loop is range(2)
# Seeded copies (same initial design for all three surrogates): prepend one seeding line to each *-cpusmall.py
for f in gp-tec-MO-11 mtgp-tec-MO-11 dgp-iso-tec-MO-11; do
  { echo 'import numpy as _np, torch as _t, random as _r; _S=int(__import__("os").environ.get("SEED","0")); _np.random.seed(_S); _t.manual_seed(_S); _r.seed(_S)'; cat $f-cpusmall.py; } > $f-seeded.py
done
