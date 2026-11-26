"""The clocked lab: stations, routes, calendars, money and the event loop. Synthetic; every number is an assumption
listed with its source in the README.

Time is in days from a Monday 00:00. A *station* has units, a calendar (round the clock, a day shift, or fixed start
slots like the atomizer's), an optional booking lead and a cap on starts per period, and a turnaround after the work.
Units are booked first come, first served. An *action* (make a powder, print a build, test bars, immerse a coupon,
stop an immersion) books one or two station steps, pays its cost when admitted, and schedules its results as events.

This is deliberately the method-level model: one campaign, the stations it needs, no robots or people as separate
resources, no shared atomizer, no spending plan beyond a hard budget. byu-vcl's twin (round 3, PR 394) is the
facility-level model; where the two overlap, the numbers here are its numbers (README, "Shared with byu-vcl").
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

import numpy as np

from truth import IMM_DAYS, P_BAR_INVALID, SIG_BUILD, SIG_COUPON, burden

HOUR = 1.0 / 24.0


# --------------------------------------------------------------------------- calendars
def _open_day(t, days):
    """Next time >= t inside 08:00-17:00 on one of `days` (weekday numbers, Monday = 0)."""
    while True:
        d = math.floor(t)
        wd, h = d % 7, (t - d) * 24
        if wd in days and h < 17 - 1e-9:
            return d + max(h, 8.0) / 24
        t = d + 1


def _advance_day(t, hours, days):
    """End time of `hours` of work on a day-shift calendar that starts at t (spills over to later shifts)."""
    t = _open_day(t, days)
    while hours > 1e-9:
        d = math.floor(t)
        left = 17 / 24 + d - t
        use = min(left * 24, hours)
        t += use / 24
        hours -= use
        if hours > 1e-9:
            t = _open_day(d + 1, days)
    return t


WEEKDAYS, WEEK6 = (0, 1, 2, 3, 4), (0, 1, 2, 3, 4, 5)


@dataclass
class Station:
    name: str
    units: int = 1
    cal: str = "always"  # always | day (Mon-Fri 08-17) | day6 (Mon-Sat) | slots | thu (Thursdays, day shift)
    slots: tuple = ()  # (weekday, hour) start slots for cal == "slots"
    lead: float = 0.0  # booking lead, days
    per_period: tuple | None = None  # (max starts, period in days)
    turnaround: float = 0.0  # days from the end of the work to the result
    free_at: list = field(default_factory=list)
    starts: list = field(default_factory=list)
    busy_h: float = 0.0

    def __post_init__(self):
        self.free_at = [0.0] * self.units

    def _days(self):
        return {"day": WEEKDAYS, "day6": WEEK6, "thu": (3,), "mon_thu": (0, 1, 2, 3)}.get(self.cal)

    def _next_start(self, t):
        for _ in range(10_000):
            if self.cal == "always":
                s = t
            elif self.cal == "slots":
                s = None
                d = math.floor(t)
                for k in range(15):
                    for wd, h in sorted(self.slots, key=lambda x: x[1]):
                        if (d + k) % 7 == wd and d + k + h / 24 >= t - 1e-9:
                            s = d + k + h / 24
                            break
                    if s is not None:
                        break
            else:
                s = _open_day(t, self._days())
            if self.per_period:
                n, per = self.per_period
                k = math.floor(s / per)
                if sum(1 for x in self.starts if math.floor(x / per) == k) >= n:
                    t = (k + 1) * per
                    continue
            return s
        raise RuntimeError("no start found")

    def _end(self, s, hours):
        if self.cal in ("always", "slots"):
            return s + hours * HOUR
        return _advance_day(s, hours, self._days())

    def quote(self, t_ready, hours, now):
        """Earliest (start, end, unit) for a job ready at t_ready, booked at `now`."""
        t0 = max(t_ready, now + self.lead)
        best = None
        for u in range(self.units):
            s = self._next_start(max(t0, self.free_at[u]))
            if best is None or s < best[0]:
                best = (s, self._end(s, hours), u)
        return best

    def commit(self, q, hours):
        s, e, u = q
        self.free_at[u] = e
        self.starts.append(s)
        self.busy_h += hours

    def release(self, unit, t):
        self.free_at[unit] = min(self.free_at[unit], t)


# --------------------------------------------------------------------------- facilities (routes per stage)
ATOMIZER_SLOTS = tuple((d, h) for d in range(5) for h in (8.0, 10.5, 13.0)) + ((5, 9.0),)  # byu-vcl / FLAIME App. 2
DAL256_SLOTS = tuple((d, 8.0) for d in range(4))  # DAL #256: one run a day Mon-Thu at 08:00


def facility(name):
    """Stations and routes of one facility scenario. Returns (stations, routes, settings)."""
    S = {}

    def st(*a, **k):
        S[a[0]] = Station(*a, **k)

    R = {}
    if name in ("vertical", "vertical_ih", "nearterm"):
        # in-house ultrasonic atomizer: 3 starts a weekday and 1 on Saturday, 2.5 h a run (byu-vcl round 3)
        if name == "nearterm":
            st("atomizer", 1, "slots", slots=DAL256_SLOTS, turnaround=1.0)
        else:
            st("atomizer", 1, "slots", slots=ATOMIZER_SLOTS, turnaround=1.0)
        R["us"] = dict(stage="powder", steps=[("atomizer", 2.5)], cost=1500.0, uses=2, p_fail=0.10)
        # outside gas atomization: 30-day booking, 21-day turnaround, one run a month (byu-vcl's assumption)
        st("gas", 1, "day", lead=30.0, per_period=(1, 30.0), turnaround=21.0)
        R["gas"] = dict(stage="powder", steps=[("gas", 8.0)], cost=20000.0, uses=999, p_fail=0.02)
        if name in ("vertical", "vertical_ih"):
            # in-house LPBF (PR 318's Aconity MIDI): round the clock, 5 h a build + 3 h to cool, depowder, check
            st("printer_ih", 1, "always")
            R["ih"] = dict(stage="print", steps=[("printer_ih", 8.0)], cost=500.0, coupons=6, p_fail=0.08)
        if name in ("vertical", "nearterm"):
            # partner LPBF (Utah core facility): <= 3 builds a week, 7-day booking lead, results 2 days after
            st("printer_pt", 1, "day", lead=7.0, per_period=(3, 7.0), turnaround=2.0)
            R["pt"] = dict(stage="print", steps=[("printer_pt", 8.0)], cost=2500.0, coupons=6, p_fail=0.08)
        if name == "nearterm":
            # today's lab: bars cut by an outside EDM service (7 days), pulled on the in-house frame on a day shift
            st("edm", 4, "day", turnaround=7.0)
            st("tensile", 1, "day")
            R["bars"] = dict(stage="bars", steps=[("edm", 1.0), ("tensile", 0.5)], cost_per=200.0)
        else:
            # in-house wire EDM + two frames, round the clock (PR 318)
            st("tensile", 2, "always")
            R["bars"] = dict(stage="bars", steps=[("tensile", 0.75)], cost_per=50.0)
        st("vials", 24, "always")  # 24 immersion positions (byu-vcl round 1-3)
        R["imm"] = dict(stage="imm", steps=[("vials", 30 * 24.0)], cost=100.0, interim=True)
        settings = dict(admit_window=0.5, decide_every=0.25, rounds=False)
    elif name in ("conv_lots", "conv_atomizer"):
        if name == "conv_lots":
            # custom powder lots from an outside supplier: median 6 weeks, lognormal (assumed; README)
            st("supplier", 8, "day")
            R["custom"] = dict(stage="powder", steps=[("supplier", 1.0)], cost=6000.0, uses=999, p_fail=0.02,
                               lead_lognormal=(42.0, 1.3))
        else:
            # DAL's own lab on DAL #256's schedule: one atomizer run a day, Mon-Thu, a person attending
            st("atomizer", 1, "slots", slots=DAL256_SLOTS, turnaround=2.0)
            R["us"] = dict(stage="powder", steps=[("atomizer", 2.5)], cost=1500.0, uses=2, p_fail=0.10)
        st("printer_pt", 1, "day", lead=7.0, per_period=(3, 7.0), turnaround=2.0)
        R["pt"] = dict(stage="print", steps=[("printer_pt", 8.0)], cost=2500.0, coupons=6, p_fail=0.08)
        st("edm", 4, "day", turnaround=7.0)  # outside EDM service, 7 days (byu-vcl facility.py)
        st("tensile", 1, "thu" if name == "conv_atomizer" else "day")
        R["bars"] = dict(stage="bars", steps=[("edm", 1.0), ("tensile", 0.5)], cost_per=200.0)
        st("vials", 24, "always")
        R["imm"] = dict(stage="imm", steps=[("vials", 30 * 24.0)], cost=100.0, interim=False)
        settings = dict(admit_window=1e9, decide_every=7.0, rounds=True)
    else:
        raise KeyError(name)
    return S, R, settings


# --------------------------------------------------------------------------- the lab
class Lab:
    """State of one campaign: what exists, what is in flight, money, and the claim."""

    def __init__(self, truth, fac, seed, budget, horizon, targets, site="own", epoch=0):
        self.truth, self.fac = truth, fac
        self.stations, self.routes, self.settings = facility(fac)
        self.rng = np.random.default_rng(seed)
        self.budget, self.horizon = budget, horizon
        self.targets = targets  # dict name -> absolute objective level
        self.site, self.epoch = site, epoch
        self.comps = {}  # key -> dict(c, s, f, g)
        self.lots, self.builds, self.coupons = [], [], []
        self.spent, self.now = 0.0, 0.0
        self.events, self._seq = [], 0
        self.inflight = []  # (kind, ref, t_result)
        self.log = []  # (t, kind, cost)
        self.claim = None  # coupon id of the campaign's claimed alloy
        self.score_hist = [(0.0, 0.0, 0.0)]  # (t, spent, true value of the claim)
        self.hit = {}  # target -> (t, spent)
        self.counts = {}

    # ------------------------------------------------------------ helpers
    def key(self, c):
        return tuple(round(float(x), 6) for x in c)

    def calphad(self, c, pay=True):
        k = self.key(c)
        if k not in self.comps:
            s, f, g = self.truth.calphad(np.asarray(c, float))
            self.comps[k] = dict(c=np.asarray(c, float), s=float(s), f=float(f), g=float(g))
            if pay:
                self.spent += 10.0
                self.counts["calphad"] = self.counts.get("calphad", 0) + 1
        return self.comps[k]

    def push(self, t, kind, payload):
        self._seq += 1
        heapq.heappush(self.events, (t, self._seq, kind, payload))

    def objective_meas(self, cp):
        """Measured objective of a coupon: mean of its valid bars minus the (known) mineral burden."""
        if not cp["bars"]:
            return None
        lam = self.truth.lam
        bx = self.truth.burden_x(cp["c"]) if hasattr(self.truth, "burden_x") else burden(cp["c"])
        return float(np.mean(cp["bars"]) - lam * bx)

    # ------------------------------------------------------------ admission
    def plan(self, act, now):
        """Bookings, cost and result time of an action, or None if it can't be done."""
        k = act["kind"]
        if k == "powder":
            r = self.routes.get(act["route"])
            if r is None:
                return None
            cost = r["cost"] + (0.0 if self.key(act["c"]) in self.comps else 10.0)
            ready = now
        elif k == "print":
            r = self.routes.get(act["machine"])
            lot = self.lots[act["lot"]]
            if r is None or lot["failed"] or lot["uses_left"] <= 0 or lot["t_ready"] is None:
                return None
            cost = r["cost"]
            ready = max(now, lot["t_ready"])
        elif k == "bars":
            r = self.routes["bars"]
            cp = self.coupons[act["coupon"]]
            n = min(act["n"], cp["bars_left"])
            if n <= 0 or cp["rho_meas"] is None:
                return None
            cost = r["cost_per"] * n
            ready = now
        elif k == "imm":
            r = self.routes["imm"]
            cp = self.coupons[act["coupon"]]
            if cp["imm"] is not None or cp["rho_meas"] is None:
                return None
            cost = r["cost"]
            ready = now
        else:
            raise KeyError(k)
        t = ready
        books = []
        for j, (sname, hours) in enumerate(r["steps"]):
            stn = self.stations[sname]
            h = hours + (0.5 * (act.get("n", 1) - 1) if k == "bars" and j == len(r["steps"]) - 1 else 0.0)
            q = stn.quote(t, h, now)
            books.append((stn, q, h))
            t = q[1] + stn.turnaround
        if "lead_lognormal" in r:
            med, gsd = r["lead_lognormal"]
            t += float(med * math.exp(self.rng.normal(0, math.log(gsd))))
        stn0 = books[0][0]
        wait = books[0][1][0] - max(ready, now + stn0.lead)  # queueing beyond the booking lead
        return dict(cost=cost, books=books, t_result=t, first_start=books[0][1][0], wait=wait)

    def submit(self, act, now, window=None):
        """Admit an action if its first step can start within the window and the money is there."""
        if act["kind"] == "stop":
            return self._stop(act["coupon"], now)
        p = self.plan(act, now)
        if p is None:
            return False
        window = self.settings["admit_window"] if window is None else window
        if p["wait"] > window + 1e-9 or self.spent + p["cost"] > self.budget + 1e-6:
            return False
        for stn, q, h in p["books"]:
            stn.commit(q, h)
        self.spent += p["cost"]
        self.log.append((now, act["kind"], p["cost"]))
        self.counts[act["kind"]] = self.counts.get(act["kind"], 0) + (act.get("n", 1) if act["kind"] == "bars" else 1)
        self._start(act, now, p)
        return True

    # ------------------------------------------------------------ starting actions
    def _start(self, act, now, p):
        k, t_res = act["kind"], p["t_result"]
        if k == "powder":
            cal = self.calphad(act["c"], pay=False)
            route = act["route"]
            r = self.routes[route]
            a = float(act.get("a", 0.5))
            q_true = float(self.truth.q(a, cal["g"], "gas" if route in ("gas", "custom") else "us"))
            lot = dict(id=len(self.lots), c=np.asarray(act["c"], float), key=self.key(act["c"]),
                       route="gas" if route in ("gas", "custom") else "us", a=a if route == "us" else None,
                       q_true=q_true, q_meas=None, uses_left=r["uses"], t_ready=None,
                       failed=bool(self.rng.random() < r["p_fail"]), t_order=now, epoch=self.epoch)
            self.lots.append(lot)
            self.inflight.append(("powder", lot["id"], t_res))
            self.push(t_res, "lot", lot["id"])
        elif k == "print":
            lot = self.lots[act["lot"]]
            lot["uses_left"] -= 1
            r = self.routes[act["machine"]]
            cal = self.comps[lot["key"]]
            b = dict(id=len(self.builds), lot=lot["id"], machine=act["machine"], coupons=[], t_order=now,
                     failed=bool(self.rng.random() < r["p_fail"]), epoch=self.epoch)
            off = float(self.rng.normal(0, SIG_BUILD))
            for (P, v) in act["pv"][: r["coupons"]]:
                rho_true = float(self.truth.rho(P, v, cal["f"], cal["g"], lot["q_true"], act["machine"], lot["route"],
                                                self.site))
                cp = dict(id=len(self.coupons), build=b["id"], lot=lot["id"], c=lot["c"], key=lot["key"],
                          a=lot["a"], route=lot["route"], machine=act["machine"], P=float(P), v=float(v),
                          rho_actual=float(np.clip(rho_true + off, 0, 1)), rho_meas=None, bars=[], bars_left=3,
                          bars_pending=0, imm=None, imm_read={}, imm_final=None, amp=self.truth.film_factor(self.rng),
                          epoch=self.epoch)
                self.coupons.append(cp)
                b["coupons"].append(cp["id"])
            self.builds.append(b)
            self.inflight.append(("print", b["id"], t_res))
            self.push(t_res, "build", b["id"])
        elif k == "bars":
            cp = self.coupons[act["coupon"]]
            n = min(act["n"], cp["bars_left"])
            cp["bars_left"] -= n
            cp["bars_pending"] += n
            self.inflight.append(("bars", cp["id"], t_res))
            self.push(t_res, "bars", (cp["id"], n))
        elif k == "imm":
            cp = self.coupons[act["coupon"]]
            stn, q, _ = p["books"][0]
            start = q[0]
            cp["imm"] = dict(state="running", start=start, unit=q[2], t_end=start + 30.0)
            lnr = float(self.truth.ln_corr(cp["c"], cp["rho_actual"]))
            cp["lnr_true"] = lnr
            for d in IMM_DAYS:
                if d < 30 and not self.routes["imm"]["interim"]:
                    continue
                self.push(start + d, "imm", (cp["id"], d))
            self.inflight.append(("imm", cp["id"], start + 30.0))

    def _stop(self, cid, now):
        cp = self.coupons[cid]
        im = cp["imm"]
        if im is None or im["state"] != "running":
            return False
        im["state"] = "stopped"
        im["t_stop"] = now
        self.stations["vials"].release(im["unit"], now)
        self.counts["stop"] = self.counts.get("stop", 0) + 1
        self.inflight = [x for x in self.inflight if not (x[0] == "imm" and x[1] == cid)]
        return True

    # ------------------------------------------------------------ results
    def apply(self, t, kind, payload):
        self.now = t
        if kind == "lot":
            lot = self.lots[payload]
            self.inflight = [x for x in self.inflight if not (x[0] == "powder" and x[1] == payload)]
            if lot["failed"]:
                lot["uses_left"] = 0
                lot["q_meas"] = None
            else:
                lot["q_meas"] = self.truth.measure_q(lot["q_true"], self.rng)
                lot["t_ready"] = t
            return True
        if kind == "build":
            b = self.builds[payload]
            self.inflight = [x for x in self.inflight if not (x[0] == "print" and x[1] == payload)]
            b["t_done"] = t
            for cid in b["coupons"]:
                cp = self.coupons[cid]
                if b["failed"]:
                    cp["bars_left"] = 0
                    cp["failed"] = True
                else:
                    cp["rho_meas"] = float(np.clip(cp["rho_actual"] + self.rng.normal(0, SIG_COUPON)
                                                   + self.truth.epoch_rho.get(self.epoch, 0.0), 0, 1))
            return True
        if kind == "bars":
            cid, n = payload
            cp = self.coupons[cid]
            cal = self.comps[cp["key"]]
            for _ in range(n):
                if self.rng.random() < P_BAR_INVALID:
                    cp["bars_left"] += 0  # the bar is gone; no result
                    continue
                cp["bars"].append(self.truth.measure_U(cal["s"], cp["rho_actual"], self.rng, self.site, self.epoch))
            cp["bars_pending"] -= n
            self.inflight = [x for x in self.inflight if not (x[0] == "bars" and x[1] == cid and x[2] <= t + 1e-9)]
            self._update_claim(t)
            return True
        if kind == "imm":
            cid, d = payload
            cp = self.coupons[cid]
            if cp["imm"] is None or cp["imm"]["state"] != "running":
                return False
            cp["imm_read"][d] = self.truth.imm_reading(cp["lnr_true"], d, cp["amp"], self.rng)
            if d == 30:
                cp["imm"]["state"] = "done"
                cp["imm_final"] = cp["imm_read"][30]
                self.inflight = [x for x in self.inflight if not (x[0] == "imm" and x[1] == cid)]
                self._update_claim(t)
            return True
        raise KeyError(kind)

    # ------------------------------------------------------------ the claim
    def claimable(self, cp):
        return (len(cp["bars"]) >= 3 and cp["imm_final"] is not None and cp["imm_final"] <= self.truth.ln_rmax)

    def claimed_value_meas(self):
        if self.claim is None:
            return None
        return self.objective_meas(self.coupons[self.claim])

    def _update_claim(self, t):
        best, bid = None, None
        for cp in self.coupons:
            if self.claimable(cp):
                m = self.objective_meas(cp)
                if best is None or m > best:
                    best, bid = m, cp["id"]
        if bid is None:
            return
        self.claim = bid
        cp = self.coupons[bid]
        val = self.truth.score(cp["c"], cp["a"] if cp["a"] is not None else 0.5, cp["P"], cp["v"], cp["route"],
                               cp["machine"])
        if val != self.score_hist[-1][2]:
            self.score_hist.append((t, self.spent, val))
        for name, lvl in self.targets.items():
            if name not in self.hit and val >= lvl - 1e-12:
                self.hit[name] = (t, self.spent)

    # ------------------------------------------------------------ the loop
    def run(self, policy, stop_at=None, max_decisions=100_000):
        """Event loop. The policy is asked for a ranked list of actions at every decision time and the lab admits
        them in order. Asynchronous facilities decide when results come back (at most every `decide_every` days) and
        at 08:00 each day; round-based (conventional) ones on Mondays at 09:00. stop_at: the target whose hit ends
        the campaign (the benchmark measures the time to it)."""
        st = self.settings
        next_dec, last_dec, n_dec, idle = 0.0, -math.inf, 0, 0
        while True:
            t_ev = self.events[0][0] if self.events else math.inf
            if next_dec <= t_ev:
                t = next_dec
                if t > self.horizon or n_dec >= max_decisions:
                    break
                self.now = t
                n_dec += 1
                n_before = len(self.log)
                for a in policy.decide(self, t):
                    self.submit(a, t)
                last_dec = t
                admitted = len(self.log) > n_before
                if st["rounds"]:
                    next_dec = (math.floor((t - 9 * HOUR) / 7.0) + 1) * 7.0 + 9 * HOUR
                else:
                    next_dec = math.floor(t) + 1 + 8 * HOUR
                if not self.events and not admitted:
                    idle += 1
                    if idle >= 3:  # nothing in flight and nothing the policy wants or can afford
                        break
                else:
                    idle = 0
            else:
                t, _, kind, payload = heapq.heappop(self.events)
                if t > self.horizon:
                    break
                self.apply(t, kind, payload)
                if not st["rounds"]:
                    next_dec = min(next_dec, max(t, last_dec + st["decide_every"]))
            if stop_at and stop_at in self.hit:
                break
        return self.result(n_dec)

    def result(self, n_dec):
        return dict(hit={k: list(v) for k, v in self.hit.items()}, spent=self.spent, t_end=self.now,
                    score_hist=[list(x) for x in self.score_hist], counts=self.counts, decisions=n_dec,
                    n_lots=len(self.lots), n_builds=len(self.builds),
                    busy_h={k: round(s.busy_h, 1) for k, s in self.stations.items()})
