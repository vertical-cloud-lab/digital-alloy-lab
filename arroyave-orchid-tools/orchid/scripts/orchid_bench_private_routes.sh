#!/bin/bash
# Try every orchid-bench stage that needs the private orchid-pipeline (or tesseract/OpenCV/camelot) and record the
# first error line. Run from the work copy; ORCHID_PIPELINE points at a path that does not exist (the repo is private).
cd /tmp/arroyave/work/orchid-bench
export ORCHID_PIPELINE=/nonexistent/orchid-pipeline OMP_NUM_THREADS=1 MPLBACKEND=Agg
export ORCHID_TDB_DIR=/tmp/arroyave/src/orchid-calphad__orchid-project.org/data/databases/sgte-binary
export ORCHID_PD_DIR=/tmp/arroyave/src/orchid-calphad__orchid-data/phase-diagrams/sgte
export OPEN_TDB=/tmp/arroyave/src/orchid-calphad__orchid-project.org/data/databases
PY=/tmp/arroyave/venvs/orchid-bench/bin/python
for s in baselines/ocr_cache.py baselines/vector_figures.py baselines/assessed_pd_raster.py baselines/ocr_pdf.py \
         baselines/tdb_topology.py baselines/raster_pd.py baselines/tables_camelot.py baselines/tables_ocr.py \
         baselines/raster_xy.py ai/prepare.py ai/map_outputs.py showcase/build.py; do
  t0=$(date +%s.%N)
  out=$(timeout 300 $PY bench/$s 2>&1 >/dev/null); rc=$?
  dt=$(python3 -c "print(round($(date +%s.%N)-$t0,1))")
  last=$(printf '%s\n' "$out" | grep -E 'Error|error|Exception|No such' | tail -1)
  echo "$s | exit=$rc | ${dt}s | ${last:0:300}"
done
