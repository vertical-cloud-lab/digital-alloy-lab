#!/usr/bin/env bash
# Fetch the byu-vcl digital twin (round 3, byu-vcl PR 394) at the commit this benchmark was run on, into $TWIN_ROOT
# (default /tmp/byu-vcl). Only vertical-lab/twin/ is checked out: byu-vcl is several GB.
set -euo pipefail
COMMIT=${TWIN_COMMIT:-f1606a93df64da25a99b168c198f5498f08469da}
ROOT=${TWIN_ROOT:-/tmp/byu-vcl}
if [ ! -d "$ROOT/.git" ]; then
  git clone --filter=blob:none --no-checkout https://github.com/vertical-cloud-lab/byu-vcl.git "$ROOT"
fi
cd "$ROOT"
git sparse-checkout init --no-cone
git sparse-checkout set --no-cone '/vertical-lab/twin/' '/vertical-lab/out/twin2/oracle.json'
git fetch --quiet --filter=blob:none origin "$COMMIT"
git checkout --quiet "$COMMIT"
echo "twin at $(git rev-parse --short HEAD): $ROOT/vertical-lab (export TWIN_DIR=$ROOT/vertical-lab)"
