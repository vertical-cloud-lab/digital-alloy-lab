#!/bin/bash
# Offline build checks of orchid-project.org's release tooling (--check modes: rebuild in memory, compare, write nothing).
# Layout: /tmp/arroyave/work/site_siblings/{orchid-project.org (copy), orchid-data (full 1.6 GB copy), open-tdb -> site data}
# so any accidental write lands in copies. No network, no publish/deploy (zenodo bundle/writeback are NOT run).
S=/tmp/arroyave/work/site_siblings
cd $S/orchid-project.org
PY=/tmp/arroyave/venvs/orchid-site/bin/python
export OMP_NUM_THREADS=1 ORCHID_DATA=$S/orchid-data PYTHONDONTWRITEBYTECODE=1
run() {  # name, command...
  local name=$1; shift
  local t0=$(date +%s.%N)
  timeout 900 "$@" > /tmp/arroyave/work/site_test_logs/build-$name.log 2>&1; local rc=$?
  local dt=$(python3 -c "print(round($(date +%s.%N)-$t0,1))")
  echo "$name | exit=$rc | ${dt}s | $(grep -vE '^\s*$' /tmp/arroyave/work/site_test_logs/build-$name.log | tail -2 | tr '\n' ' ' | cut -c1-400)"
}
run static_pages      $PY tools/build_static_pages.py --data $S/orchid-data --site $S/orchid-project.org --check
run site_numbers      $PY tools/build_site_numbers.py --data $S/orchid-data --check
run parquet           $PY tools/build_parquet.py --data $S/orchid-data --check
run zenodo_plan       $PY tools/zenodo_release.py --data $S/orchid-data plan
run zenodo_scan       $PY tools/zenodo_release.py --data $S/orchid-data scan
run zenodo_manifest   $PY tools/zenodo_release.py --data $S/orchid-data manifest --check
run zenodo_metadata   $PY tools/zenodo_release.py --data $S/orchid-data metadata --check
run zenodo_card       $PY tools/zenodo_release.py --data $S/orchid-data card --check
