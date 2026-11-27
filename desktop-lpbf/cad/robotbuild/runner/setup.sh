#!/bin/bash
# Round 9 (2026-11-27): set up a fresh GitHub Actions runner for the robot-build video in ~5 min.
#   bash desktop-lpbf/cad/robotbuild/runner/setup.sh
# - /tmp/venv: Python 3.12 (the runner's default python3 is 3.14, which cadquery 2.8 has no wheels for) with
#   desktop-lpbf/analysis/requirements.txt, numba, and the YouTube client;
# - /tmp/memslot: the shared memory ledger every heavy job queues on (first come, first served; 14 GB of the runner's 15);
# - /tmp/capmem: runs its command uncapped. Round 9 capped with `systemd-run --user --scope -p MemoryMax=...`, but after
#   about 4.5 h of uptime processes inside a scope could no longer reach Xvfb ("Render window is not current"), so the
#   ledger is the only guard. Round 8's frames and plans die with the runner: every round re-plans and re-renders.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
PY=$(ls -d /opt/hostedtoolcache/Python/3.12.*/x64/bin/python3 | tail -1)
[ -x /tmp/venv/bin/python ] || "$PY" -m venv /tmp/venv
/tmp/venv/bin/pip install -q --upgrade pip
/tmp/venv/bin/pip install -q -r "$REPO/desktop-lpbf/analysis/requirements.txt" numba google-api-python-client google-auth google-auth-oauthlib
sudo apt-get install -y -q libglu1-mesa > /dev/null 2>&1 || true
install -m 755 "$HERE/memslot.py" /tmp/memslot
sed -i "1s|.*|#!$PY|" /tmp/memslot
install -m 755 "$HERE/capmem.sh" /tmp/capmem
mkdir -p /tmp/memslots /tmp/r9
/tmp/venv/bin/python -c "import cadquery, pyvista, fcl, trimesh, mujoco; print('venv ok')"
