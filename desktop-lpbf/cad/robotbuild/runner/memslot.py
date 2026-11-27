#!/usr/bin/env python3
"""/tmp/memslot <GB> <cmd...>: wait until the GB reserved by running memslot jobs plus <GB> fits in the runner's budget
(14.0 GB of 15; raised from 12.5 at 09:58 because jobs peak well under their caps), then run <cmd> under /tmp/capmem <GB>. First come, first served (09:20): a job waits while an older
waiter is queued, so a big job (chapter 30's 6 GB) can't be starved by a stream of small ones."""
import fcntl, os, subprocess, sys, time
BUDGET = float(os.environ.get("MEMSLOT_BUDGET", "14.0"))
D = "/tmp/memslots"; os.makedirs(D, exist_ok=True)
gb = float(sys.argv[1].rstrip("Gg")); cmd = sys.argv[2:]
me = f"{D}/{os.getpid()}-{gb}"
ticket = f"{D}/.wait-{time.time():017.3f}-{os.getpid()}-{gb}"
def alive(p):
    try: os.kill(p, 0); return True
    except OSError: return False
waited = 0.0
open(ticket, "w").write(" ".join(cmd)[:300])
try:
    while True:
        with open(f"{D}/.lock", "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            used = 0.0; waiters = []
            for f in os.listdir(D):
                if f.startswith(".wait-"):
                    _, ts, pid, g = f.split("-", 3)
                    if alive(int(pid)): waiters.append(f)
                    else: os.unlink(f"{D}/{f}")
                    continue
                if f.startswith("."): continue
                pid, g = f.split("-", 1)
                if alive(int(pid)): used += float(g)
                else: os.unlink(f"{D}/{f}")
            first = sorted(waiters)[0] == os.path.basename(ticket) if waiters else True
            if first and (used + gb <= BUDGET or used == 0):
                open(me, "w").write(" ".join(cmd)[:300])
                os.unlink(ticket)
                break
        if waited == 0: print(f"memslot: waiting for {gb} GB ({used:.1f} of {BUDGET} reserved, {len(waiters)} queued)", file=sys.stderr, flush=True)
        time.sleep(5); waited += 5
finally:
    if os.path.exists(ticket): os.unlink(ticket)
try:
    rc = subprocess.call(["/tmp/capmem", str(gb)] + cmd)
finally:
    try: os.unlink(me)
    except OSError: pass
sys.exit(rc)
