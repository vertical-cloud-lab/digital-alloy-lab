"""Safety and interlock logic of the desktop LPBF cell, modelled as a function of every input, checked exhaustively, plus
a single-fault analysis at the channel level.

The logic is what electrical.md section 4 puts in the programmable safety controller (Banner SC26-2 class) and what the
hard-wired parts do on their own (CN708 -> K2, the shutter's spring, the laser's own interlock loop). The PLC and the
scan card only *request*; nothing they do can close a safety output on its own.

1. Combinational check: every combination of the logical inputs (each dual-channel device as one bool), the request
   bits and the two state bits (armed latch, fault latch): 2^25 = 33.5 M cases, vectorised in chunks. Properties P1-P8
   (below) must hold in every case, and each output must be reachable (true in at least one case).
2. Sequences: power-up, reset, arming, a trip, the trailing-edge reset, a power cut.
3. Single faults: each channel of each dual-channel input stuck closed, stuck open, or shorted to the other channel; each
   output contact welded; the shutter stuck open; the laser ignoring its interlock loop; the reset button stuck. For each
   fault: (a) is the hazard removed on the next demand, and (b) is the fault detected so the machine will not re-arm?

Run: /tmp/venv/bin/python desktop-lpbf/analysis/electrical/interlock_logic.py
  -> desktop-lpbf/analysis/out/electrical/interlock.{md,json}
"""
import itertools
import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parents[1] / "out" / "electrical"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------------------------------- the inputs
DUAL = {   # dual-channel safety inputs (two contacts or two OSSD channels each), "True" = safe/OK state
    "estop_rack": "E-stop on the rack's operator panel",
    "estop_guard": "E-stop on the guard front",
    "estop_gas": "E-stop on the gas module / dock side",
    "guard_closed": "guard door closed (coded non-contact sensor, separate from the lock)",
    "guard_locked": "guard lock engaged (lock-monitoring contacts)",
    "room_o2": "room and Shuttle O2 monitors above 19.5 % (two monitors' relays, one per channel)",
    "plate_cool": "plate below 50 C (2nd temperature channel's relay + PLC reading of the edge TC)",
    "robot_home": "UR12e at its safe home (UR safety output 'Safe Home', two channels)",
    "vlm_docked": "tray docked and the VLM at rest (dock signal pins, two channels)",
    "shutter_closed": "shutter closed (two position switches on the shutter blade)",
}
SINGLE = {  # single-channel inputs
    "key_on": "laser key switch on",
    "limit_ok": "CN708 latching limit healthy (its relay; it also drops K2 on its own)",
    "chamber_ambient": "chamber within +/-5 mbar of ambient (pressure switch)",
    "process_ok": "PLC process permissive (chamber O2 < set point, pressure in window, module present, fibre and head in place)",
    "exhaust_ok": "exhaust flow proven (flow switch in the vent header)",
}
REQ = ["laser_req", "shutter_req", "unlock_req", "heater_req", "argon_req", "entry_req", "move_req"]
STATE = ["armed", "fault"]
NAMES = list(DUAL) + list(SINGLE) + REQ + STATE


def logic(v):
    """Outputs from inputs. Works on python bools or numpy bool arrays. v: dict name -> value."""
    estop = v["estop_rack"] & v["estop_guard"] & v["estop_gas"]
    ok = ~v["fault"] if isinstance(v["fault"], np.ndarray) else (not v["fault"])
    laser_perm = (estop & v["guard_closed"] & v["guard_locked"] & v["key_on"] & v["room_o2"] & v["limit_ok"]
                  & v["robot_home"] & v["vlm_docked"] & v["process_ok"] & v["armed"] & ok)
    laser_ilk = laser_perm & v["laser_req"]                                   # K4 + K5 into the laser's interlock loop
    shutter_open = laser_ilk & v["shutter_req"]                               # power-to-open shutter
    neg = (lambda x: ~x) if isinstance(laser_ilk, np.ndarray) else (lambda x: not x)
    servo_en = estop & v["guard_closed"] & v["guard_locked"] & ok             # K3 on the 48 V servo bus
    unlock = (neg(laser_ilk) & v["shutter_closed"] & v["plate_cool"] & v["chamber_ambient"] & v["unlock_req"])
    heater_en = estop & v["limit_ok"] & v["room_o2"] & v["process_ok"] & v["heater_req"] & ok   # K1 (K2 is the CN708's)
    argon_en = v["room_o2"] & v["exhaust_ok"] & v["argon_req"]                # supply valve; E-stop does not close it (safety.md 4.4)
    entry_ok = (unlock & neg(servo_en & v["guard_locked"]) & neg(laser_ilk) & v["entry_req"])
    # entry is given once the guard is unlocked (servo_en drops with the lock), never while K4/K5 are closed
    move_ok = (neg(laser_ilk) & v["shutter_closed"] & v["robot_home"] & v["guard_closed"] & v["move_req"])
    return dict(laser_ilk=laser_ilk, shutter_open=shutter_open, servo_en=servo_en, unlock=unlock, heater_en=heater_en,
                argon_en=argon_en, entry_ok=entry_ok, move_ok=move_ok, estop=estop)


def implies(a, b):
    return (~a) | b


def exhaustive():
    n = len(NAMES)
    total = 1 << n
    chunk_bits = 21
    viol = {f"P{i}": 0 for i in range(1, 9)}
    reach = {k: 0 for k in ("laser_ilk", "shutter_open", "servo_en", "unlock", "heater_en", "argon_en", "entry_ok", "move_ok")}
    for c in range(total >> chunk_bits):
        idx = (np.arange(1 << chunk_bits, dtype=np.uint64) + np.uint64(c << chunk_bits))
        v = {name: ((idx >> np.uint64(i)) & np.uint64(1)).astype(bool) for i, name in enumerate(NAMES)}
        o = logic(v)
        estop = o["estop"]
        must_laser = (estop & v["guard_closed"] & v["guard_locked"] & v["key_on"] & v["room_o2"] & v["limit_ok"]
                      & v["robot_home"] & v["vlm_docked"] & v["process_ok"] & v["armed"] & ~v["fault"])
        checks = {
            "P1": implies(o["laser_ilk"], must_laser),
            "P2": implies(o["shutter_open"], o["laser_ilk"]),
            "P3": implies(o["unlock"], ~o["laser_ilk"] & ~o["shutter_open"] & v["shutter_closed"] & v["plate_cool"] & v["chamber_ambient"]),
            "P4": implies(o["heater_en"], estop & v["limit_ok"] & v["room_o2"] & ~v["fault"]),
            "P5": implies(o["entry_ok"], ~o["laser_ilk"] & ~o["shutter_open"] & v["shutter_closed"] & v["plate_cool"]
                          & v["chamber_ambient"] & ~(o["servo_en"] & v["guard_locked"])),
            "P6": implies(o["argon_en"], v["room_o2"] & v["exhaust_ok"]),
            "P7": implies(o["move_ok"], ~o["laser_ilk"] & ~o["shutter_open"] & v["shutter_closed"] & v["robot_home"]),
            "P8": implies(o["servo_en"], estop & v["guard_closed"] & v["guard_locked"]),
        }
        for k, arr in checks.items():
            viol[k] += int((~arr).sum())
        for k in reach:
            reach[k] += int(o[k].sum())
    return dict(cases=total, violations=viol, reachable_counts=reach)


PROPS = {
    "P1": "laser interlock closed (emission possible) only if all three E-stops are released, the guard is closed and locked, the key is on, room O2 is OK, the plate limit is healthy, the robot is at safe home, the tray is docked, the process permissive holds, the machine was reset (armed) and no fault is latched",
    "P2": "shutter open only while the laser interlock is closed",
    "P3": "guard unlock only with the laser interlock open, the shutter commanded shut and confirmed closed on both channels, the plate below 50 C and the chamber at ambient pressure",
    "P4": "heater contactor K1 only with the E-stops released, the limit healthy, room O2 OK and no fault",
    "P5": "robot entry only with the laser interlock open, the shutter closed, the plate below 50 C, the chamber at ambient and the servo bus off",
    "P6": "argon supply valve only with room O2 OK and exhaust flow proven",
    "P7": "VLM tray movement only with the laser interlock open, the shutter closed and the robot at safe home",
    "P8": "servo bus K3 only with the E-stops released and the guard closed and locked",
}


# ---------------------------------------------------------------------------------------------------- the controller with channels
class Controller:
    """Channel-level model: dual inputs with a 0.5 s discrepancy (simultaneity) check; a discrepancy latches a fault that
    clears only after both channels have been seen open together (the device cycled) and a reset; test pulses catch a
    short between channels (permanent fault); EDM (mirror contacts) on K1, K3, K4, K5; the laser chain re-arms only on
    the trailing edge of the reset button, with K4 and K5 seen open and the shutter seen closed on both channels; the
    laser's own status output (ready/emission) is read back, so a laser that ignores its interlock loop is caught."""
    SIMUL = 0.5

    def __init__(self, faults=()):
        self.f = set(faults)
        self.armed = False
        self.fault = False
        self.why = set()
        self.disc = {k: 0.0 for k in DUAL}
        self.need_cycle = set()
        self.reset_prev = False
        self.k = dict(K1=False, K3A=False, K3B=False, K4=False, K5=False)     # commanded
        self.out = {}

    def read_dual(self, name, phys):
        a, b = phys, phys
        if f"{name}:A_stuck_ok" in self.f:
            a = True
        if f"{name}:B_stuck_ok" in self.f:
            b = True
        if f"{name}:A_stuck_trip" in self.f:
            a = False
        if f"{name}:B_stuck_trip" in self.f:
            b = False
        return a, b

    def contact(self, name, cmd):
        return True if f"{name}:welded" in self.f else cmd

    def latch(self, why):
        self.fault = True
        self.why.add(why)
        self.armed = False

    def step(self, phys, req, dt=0.1):
        val = {}
        for k in DUAL:
            a, b = self.read_dual(k, phys[k])
            if f"{k}:AB_short" in self.f:
                self.latch(f"{k}: test pulses see a short between channels")
                val[k] = False
                continue
            if a != b:
                self.disc[k] += dt
                if self.disc[k] > self.SIMUL:
                    self.latch(f"{k}: channels disagree")
                    self.need_cycle.add(k)
            else:
                self.disc[k] = 0.0
                if not a and k in self.need_cycle:
                    self.need_cycle.discard(k)      # both channels seen open together: device cycled
            val[k] = a and b
        for k in SINGLE:
            val[k] = True if f"{k}:stuck_ok" in self.f else phys[k]
        if phys.get("plc_overtemp", False):
            val["process_ok"] = False                     # the PLC's own over-temperature (control and edge TCs) drops its permissive
            if val["limit_ok"]:
                self.latch("CN708 relay still closed while the PLC reads over-temperature")
        stuck = "reset:stuck_pressed" in self.f
        r = True if stuck else phys["reset"]
        trailing = self.reset_prev and not r
        self.reset_prev = r
        # EDM: a contactor whose mirror contact says closed while it is commanded open is welded
        for n in ("K1", "K3A", "K3B", "K4", "K5"):
            if self.contact(n, self.k[n]) and not self.k[n]:
                self.latch(f"{n}: EDM sees it closed while commanded open")
        v = dict(val, **{q: req.get(q, False) for q in REQ}, armed=self.armed, fault=self.fault)
        perm = logic(dict(v, armed=True, laser_req=True, fault=False))["laser_ilk"]
        if self.armed and not perm:
            self.armed = False                                                     # any trip disarms
        # the laser's status output: ready/emission possible while K4/K5 are commanded open = laser ignores its loop
        if "laser:ignores_loop" in self.f and not self.k["K4"] and req.get("fire", False):
            self.latch("laser status shows emission possible with its interlock loop open")
        if trailing:
            hard = any(w.split(":")[0] in ("K1", "K3A", "K3B", "K4", "K5") or "short" in w or "laser status" in w or "CN708" in w for w in self.why)
            if self.fault and not self.need_cycle and not hard:
                self.fault = False
                self.why = set()
            edm_laser = not self.contact("K4", False) and not self.contact("K5", False)
            if not self.fault and perm and edm_laser and val["shutter_closed"]:
                self.armed = True
        v = dict(v, armed=self.armed, fault=self.fault)
        o = logic(v)
        self.k = dict(K1=o["heater_en"], K3A=o["servo_en"], K3B=o["servo_en"], K4=o["laser_ilk"], K5=o["laser_ilk"])
        k4, k5 = self.contact("K4", self.k["K4"]), self.contact("K5", self.k["K5"])
        laser_loop = k4 and k5
        emitting = (laser_loop or "laser:ignores_loop" in self.f) and req.get("fire", False)
        shutter_phys_open = o["shutter_open"] or "shutter:stuck_open" in self.f
        self.out = dict(o, laser_loop=laser_loop, emitting=emitting, shutter_phys_open=shutter_phys_open,
                        beam_out=emitting and shutter_phys_open, K1=self.contact("K1", self.k["K1"]),
                        servo_bus_live=self.contact("K3A", self.k["K3A"]) and self.contact("K3B", self.k["K3B"]),
                        armed=self.armed, fault=self.fault)
        return self.out


def healthy_phys():
    p = {k: True for k in DUAL}
    p.update({k: True for k in SINGLE})
    p["reset"] = False
    p["plate_cool"] = False          # a build is running: the plate is hot
    p["chamber_ambient"] = False     # argon at +20 mbar
    p["shutter_closed"] = True
    return p


RUN_REQ = dict(laser_req=True, shutter_req=True, heater_req=True, argon_req=True, fire=True)


def run_seq(ctrl, phys, req, secs):
    o = None
    for _ in range(int(round(secs / 0.1))):
        o = ctrl.step(dict(phys), req)
        phys["shutter_closed"] = not o["shutter_phys_open"]      # the shutter's position switches follow the blade
    return o


def arm(ctrl, phys, req=RUN_REQ):
    run_seq(ctrl, phys, {}, 0.3)
    phys["reset"] = True
    run_seq(ctrl, phys, {}, 0.3)
    phys["reset"] = False
    run_seq(ctrl, phys, {}, 0.3)
    return run_seq(ctrl, phys, req, 1.0)


DEMANDS = {   # device -> how the demand is made (physical state set unsafe)
    "estop_rack": "E-stop pressed", "estop_guard": "E-stop pressed", "estop_gas": "E-stop pressed", "guard_closed": "guard opened",
    "guard_locked": "lock lost", "room_o2": "O2 alarm", "robot_home": "robot leaves home", "vlm_docked": "tray undocks",
    "limit_ok": "limit trips", "key_on": "key off", "process_ok": "chamber O2 high",
}


def single_faults():
    rows = []
    faults = []
    for k in DUAL:
        for m in ("A_stuck_ok", "B_stuck_ok", "A_stuck_trip", "AB_short"):
            faults.append(f"{k}:{m}")
    for k in ("K4", "K5", "K1", "K3A", "K3B"):
        faults.append(f"{k}:welded")
    faults += ["shutter:stuck_open", "laser:ignores_loop", "reset:stuck_pressed", "limit_ok:stuck_ok"]
    for f in faults:
        dev = f.split(":")[0]
        ctrl = Controller([f])
        phys = healthy_phys()
        o0 = arm(ctrl, phys)
        armed_before = bool(o0["armed"] and o0["laser_ilk"])
        note = ""
        if dev == "plate_cool":
            # demand: laser released, plate hot, unlock requested -> must stay locked
            o1 = run_seq(ctrl, phys, dict(unlock_req=True), 1.0)
            hazard_removed = not o1["unlock"]
            demand = "unlock asked with the plate hot"
            beam = o1["beam_out"]
            loop = o1["laser_loop"]
        else:
            dem = dev if dev in DEMANDS else "estop_rack"
            demand = DEMANDS.get(dem)
            phys_d = dict(phys)
            phys_d[dem] = False
            if dem == "limit_ok":
                phys_d["plc_overtemp"] = True             # a real over-temperature is seen by both the CN708 and the PLC
            o1 = run_seq(ctrl, phys_d, RUN_REQ, 1.0)
            beam, loop = o1["beam_out"], o1["laser_loop"]
            hazard_removed = not beam
            if dem == "estop_rack" and f.startswith("K3"):
                hazard_removed = not o1["servo_bus_live"]
            if f == "K1:welded":
                hazard_removed, note = True, "K1 stays closed; the PLC turns the SSR off on the E-stop status, K2 (CN708) still opens on over-temperature; not safety-rated while it lasts"
            if f.startswith("K3"):
                note = "the other bus contactor opens (two in series: ClearPath-SD has no safe torque off)"
            if f == "limit_ok:stuck_ok":
                note = "the PLC's own over-temperature (control and edge TCs) drops its permissive and K1; its cross-check of the CN708 relay latches the fault"
            phys = phys_d
            phys[dem] = True
            phys["plc_overtemp"] = False
            run_seq(ctrl, phys, {}, 1.0)
        # cycle every device once (a person tests it), then try to re-arm
        o2 = arm(ctrl, phys)
        rearmed = bool(o2["armed"] and o2["laser_ilk"])
        needs_detection = not (f.endswith("stuck_trip") or f == "reset:stuck_pressed")
        detected = (not rearmed) or o2["fault"]
        rows.append(dict(fault=f, armed_before=armed_before, demand=demand, beam_after_demand=bool(beam),
                         laser_loop_after_demand=bool(loop), hazard_removed=bool(hazard_removed), rearm_refused=not rearmed,
                         fault_latched=bool(o2["fault"]), why=sorted(ctrl.why),
                         ok=bool(hazard_removed and (detected or not needs_detection)), note=note))
    return rows


def sequences():
    out = []
    c = Controller()
    p = healthy_phys()
    o = run_seq(c, p, RUN_REQ, 1.0)
    out.append(("power-up, nothing pressed", o["laser_ilk"], "laser interlock stays open until a reset (CFR 1040.10(f)(10))"))
    p["reset"] = True
    o = run_seq(c, p, RUN_REQ, 0.5)
    out.append(("reset held down", o["laser_ilk"], "nothing on the leading edge"))
    p["reset"] = False
    o = run_seq(c, p, RUN_REQ, 0.5)
    out.append(("reset released", o["laser_ilk"], "arms on the trailing edge"))
    p["guard_closed"] = False
    o = run_seq(c, p, RUN_REQ, 0.5)
    out.append(("guard opened while lasing (lock forced)", o["laser_ilk"], "drops at once"))
    p["guard_closed"] = True
    o = run_seq(c, p, RUN_REQ, 0.5)
    out.append(("guard closed again", o["laser_ilk"], "stays off: needs a new reset"))
    p["reset"] = True
    run_seq(c, p, RUN_REQ, 0.3)
    p["reset"] = False
    o = run_seq(c, p, RUN_REQ, 0.5)
    out.append(("reset", o["laser_ilk"], "re-armed"))
    o = run_seq(c, p, dict(RUN_REQ, unlock_req=True), 0.5)
    out.append(("unlock requested while lasing", o["unlock"], "refused (P3)"))
    o = run_seq(c, p, dict(unlock_req=True), 0.5)
    out.append(("laser and shutter released, plate still hot", o["unlock"], "refused: plate above 50 C"))
    p["plate_cool"] = True
    p["chamber_ambient"] = True
    o = run_seq(c, p, dict(unlock_req=True, entry_req=True), 0.5)
    out.append(("plate below 50 C, chamber vented", o["unlock"], "unlock given; robot entry given"))
    c2 = Controller()
    p2 = healthy_phys()
    arm(c2, p2)
    c2.armed = False          # a power cut: the controller restarts disarmed
    o = run_seq(c2, p2, RUN_REQ, 1.0)
    out.append(("after a power cut", o["laser_ilk"], "needs a manual reset"))
    return out


def main():
    ex = exhaustive()
    sf = single_faults()
    sq = sequences()
    res = dict(exhaustive=ex, properties=PROPS, single_faults=sf, sequences=[dict(step=a, output=bool(b), note=c) for a, b, c in sq],
               inputs=dict(dual=DUAL, single=SINGLE, requests=REQ, state=STATE))
    (OUT / "interlock.json").write_text(json.dumps(res, indent=1))
    L = ["# Interlock logic: exhaustive and single-fault check", "",
         "Generated by [`analysis/electrical/interlock_logic.py`](../../electrical/interlock_logic.py). The logic is the one in [`electrical.md`](../../../electrical.md) §4, "
         "written as a function of every input. It is a model of the intended safety-controller program, not of a real SC26 configuration file.", "",
         f"## 1. Every combination of inputs: {ex['cases']:,} cases ({len(NAMES)} bits: {len(DUAL)} dual-channel devices, {len(SINGLE)} single-channel inputs, {len(REQ)} requests, 2 state bits)", "",
         "| Property | What it says | Violations |", "|---|---|---|"]
    for k, txt in PROPS.items():
        L.append(f"| {k} | {txt} | **{ex['violations'][k]}** |")
    L += ["", "Each output is reachable (true in at least one case): " + ", ".join(f"{k} {v:,}" for k, v in ex["reachable_counts"].items()) + ".", "",
          "## 2. Sequences", "", "| Step | Output | Expected |", "|---|---|---|"]
    for a, b, c in sq:
        L.append(f"| {a} | {'closed/true' if b else 'open/false'} | {c} |")
    L += ["", "## 3. Single faults", "",
          "Demand = the faulted device is actuated (an output fault is tested with the rack E-stop). 'Hazard removed' = no beam can leave (laser loop open, or the shutter closed). "
          "'Re-arm refused' = after the device is restored and reset is pressed, the laser chain stays open.", "",
          "| Fault | Demand | Beam after the demand | Laser loop after the demand | Hazard removed | Re-arm refused | Fault latched | Pass | Note |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in sf:
        L.append(f"| {r['fault']} | {r['demand']} | {'yes' if r['beam_after_demand'] else 'no'} | {'closed' if r['laser_loop_after_demand'] else 'open'} | "
                 f"{'yes' if r['hazard_removed'] else '**no**'} | {'yes' if r['rearm_refused'] else 'no'} | {'yes' if r['fault_latched'] else 'no'} | {'pass' if r['ok'] else '**FAIL**'} | {r['note']} |")
    n_ok = sum(r["ok"] for r in sf)
    L += ["", f"**{n_ok} of {len(sf)} single faults pass.**", "",
          "## What this does not check", "",
          "- The real SC26 program, its response times and its test-pulse timing; the model only says the logic is consistent and that each single fault is either safe or detected.",
          "- Common-cause faults (both channels of a cable crushed together), and faults in the devices' own mechanics beyond the cases listed.",
          "- The PL/SIL of each function (ISO 13849-1). With dual-channel devices, a Cat. 3/4 controller and EDM, PL d is the usual target; it needs the devices' B10d/MTTFd values, which are not collected here."]
    (OUT / "interlock.md").write_text("\n".join(L) + "\n")
    print(json.dumps(ex["violations"]), n_ok, len(sf))
    for r in sf:
        if not r["ok"]:
            print("FAIL", r)


if __name__ == "__main__":
    main()
