#!/bin/bash
# /tmp/capmem <limit> cmd...  (11:58: systemd --user scopes stopped reaching X displays after ~11:30, so commands now run
# without a cgroup cap; /tmp/memslot's ledger still keeps the reserved total under the runner's RAM)
shift
exec "$@"
