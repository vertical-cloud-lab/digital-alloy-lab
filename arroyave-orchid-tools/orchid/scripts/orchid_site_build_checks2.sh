#!/bin/bash
# More offline --check modes of orchid-project.org's builders (fresh in-memory build compared with the files on disk).
# Same sibling layout as orchid_site_build_checks.sh (copies only); 240 s timeout each.
S=/tmp/arroyave/work/site_siblings
cd $S/orchid-project.org
PY=/tmp/arroyave/venvs/orchid-site/bin/python
export OMP_NUM_THREADS=1 ORCHID_DATA=$S/orchid-data PYTHONDONTWRITEBYTECODE=1
run() {
  local name=$1; shift
  local t0=$(date +%s.%N)
  timeout 240 "$@" > /tmp/arroyave/work/site_test_logs/build-$name.log 2>&1; local rc=$?
  local dt=$(python3 -c "print(round($(date +%s.%N)-$t0,1))")
  echo "$name | exit=$rc | ${dt}s | $(grep -vE '^\s*$' /tmp/arroyave/work/site_test_logs/build-$name.log | tail -2 | tr '\n' ' ' | cut -c1-400)"
}
run add_cite_as            $PY tools/add_cite_as.py --data $S/orchid-data --check
run phase_aliases          $PY tools/phase_aliases.py --data $S/orchid-data --check
run phase_registry         $PY tools/build_phase_registry.py --data $S/orchid-data --check
run bibliography           $PY tools/build_bibliography.py --data $S/orchid-data --check
run espei_bundle           $PY tools/build_espei_bundle.py --data $S/orchid-data --check
run dft_parity             $PY tools/build_dft_parity.py --check
run kim2017_crosscheck     $PY tools/kim2017_crosscheck.py --check
run precision_sample       $PY tools/build_precision_sample.py --check
run assessed_assemblages   $PY tools/build_assessed_assemblages.py --data $S/orchid-data --check
run export_literature      $PY tools/export_literature_data.py --data $S/orchid-data --check
