"""The hard-wired laser safety chain of FT-1, modelled at the contact level and checked exhaustively.

Wiring (diagrams/interlock-power.png):
  G9SE-201 input 1 (T11-T12): E-stop NC1 - lid A ch1 - lid B ch1 - beam tube ch1 - key NO1 - TS tube 1 - TS window 1
  G9SE-201 input 2 (T21-T22): the same devices' second contacts (TS = bimetal temperature switch, one per channel)
  Manual reset: T31-T32 through the RESET button (feedback loop; no external contactors on the laser side)
  Safety outputs: 13-14 -> laser interlock channel 1 (24-pin guide: pins 1-4), 23-24 -> channel 2 (pins 2-3)
  The laser: diode power only when both channels are closed and START was pressed after they closed; if one channel
  opens, both must open before it can restart (IPG YLR-series user guide, "Interlock Description").
  Emission = laser supply active AND EMON (software, RS-232) AND LASERON (RTC5 gate).

G9SE-201 behaviour (Omron instruction sheet 4022078): outputs need both inputs ON and a manual reset; any input OFF
turns the outputs OFF (<= 15 ms); a mismatch between the inputs is a fault that clears only when both inputs are OFF.

The check:
1. reachability over every combination of the 12 contacts, RESET, START, EMON and LASERON at every step, from power-up
   (16 internal states x 65,536 inputs): emission must imply every contact closed, and the outputs must only close
   through a RESET pulse with both channels closed;
2. single faults (each contact stuck closed, each G9SE output welded): starting armed, opening any set of devices
   must stop emission at once; then, with everything closed again and RESET pressed, the chain either refuses to
   re-arm (the fault is detected) or re-arms (the fault is masked, because another device in the same series opened in
   the same cycle; ISO/TR 24119 'fault masking').
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Dict, List, Tuple

DEVICES = ["estop", "lid_a", "lid_b", "beam_tube", "key", "ts_tube", "ts_window"]
CONTACTS = [(d, ch) for d in DEVICES for ch in (1, 2)]
N_C = len(CONTACTS)


@dataclass
class ChainState:
    g9se: bool = False         # safety outputs 13-14 and 23-24 closed
    g9se_lock: bool = False    # input mismatch latched
    ps: bool = False           # laser main supply active
    laser_lock: bool = False   # laser's own channel mismatch latched

    def key(self):
        return (self.g9se, self.g9se_lock, self.ps, self.laser_lock)


def step(st: ChainState, contacts: Dict[Tuple[str, int], bool], reset: bool, start: bool, emon: bool, laseron: bool,
         welded: Tuple[bool, bool] = (False, False)) -> Tuple[ChainState, bool]:
    """One scan of the chain. contacts[(device, ch)] True = closed. reset/start = a complete button pulse this step."""
    c1 = all(v for (d, ch), v in contacts.items() if ch == 1)
    c2 = all(v for (d, ch), v in contacts.items() if ch == 2)
    g, lock = st.g9se, st.g9se_lock
    if c1 != c2:
        g, lock = False, True
    elif not c1:                    # both inputs off: outputs off, a mismatch clears
        g, lock = False, False
    elif reset and not lock:        # both on, no latched mismatch, a reset pulse
        g = True
    o1, o2 = g or welded[0], g or welded[1]
    ps, llock = st.ps, st.laser_lock
    if o1 != o2:
        ps, llock = False, True
    elif not o1:
        ps, llock = False, False
    elif start and not llock:
        ps = True
    new = ChainState(g, lock, ps, llock)
    return new, bool(new.ps and emon and laseron)


def reachability() -> dict:
    """Every input combination at every step from power-up; properties must hold on every transition."""
    seen = {ChainState().key()}
    frontier = [ChainState()]
    transitions = violations = 0
    emitted = False
    out_without_reset = 0
    while frontier:
        nxt = []
        for st in frontier:
            for bits in range(1 << N_C):
                contacts = {c: bool(bits >> i & 1) for i, c in enumerate(CONTACTS)}
                all_closed = bits == (1 << N_C) - 1
                for reset, start, emon, laseron in itertools.product((False, True), repeat=4):
                    new, em = step(st, contacts, reset, start, emon, laseron)
                    transitions += 1
                    if em:
                        emitted = True
                        if not all_closed:
                            violations += 1
                    if new.g9se and not st.g9se and not reset:
                        out_without_reset += 1
                    if new.key() not in seen:
                        seen.add(new.key())
                        nxt.append(new)
        frontier = nxt
    return dict(states=len(seen), transitions=transitions, emission_reachable=emitted,
                emission_with_a_contact_open=violations, outputs_closed_without_reset=out_without_reset)


def armed(welded=(False, False), contacts_list=None) -> ChainState:
    allc = {c: True for c in (contacts_list or CONTACTS)}
    st = ChainState()
    st, _ = step(st, allc, True, False, False, False, welded)
    st, _ = step(st, allc, False, True, True, True, welded)
    return st


LID_CYCLE = ("lid_a", "lid_b")       # the normal demand: the lid is opened, both lid switches open together


def single_faults(devices=None) -> List[dict]:
    """Each contact stuck closed, each output welded: is the beam stopped on every demand, is the fault detected?"""
    devices = devices or DEVICES
    contacts_list = [(d, ch) for d in devices for ch in (1, 2)]
    rows = []
    faults = [("stuck_closed", c) for c in contacts_list] + [("welded", 0), ("welded", 1)]
    subsets = [x for r in range(1, len(devices) + 1) for x in itertools.combinations(devices, r)]
    lid_cycle = tuple(d for d in LID_CYCLE if d in devices)
    for kind, where in faults:
        welded = (where == 0, where == 1) if kind == "welded" else (False, False)
        unsafe, masked_by = [], []
        for opened in subsets:
            st = armed(welded, contacts_list)
            contacts = {c: (c[0] not in opened) for c in contacts_list}
            if kind == "stuck_closed":
                contacts[where] = True
            st, em = step(st, contacts, False, False, True, True, welded)
            if em:
                unsafe.append(opened)
            allc = {c: True for c in contacts_list}
            st, _ = step(st, allc, True, False, True, True, welded)        # close everything, press RESET
            st, em2 = step(st, allc, False, True, True, True, welded)      # press START
            if em2:
                masked_by.append(opened)
        dev = where[0] if kind == "stuck_closed" else f"G9SE output {'13-14' if where == 0 else '23-24'}"
        alone = (dev,) in masked_by if kind == "stuck_closed" else bool(masked_by)
        rows.append(dict(fault=f"{kind}:{dev}" + (f":ch{where[1]}" if kind == "stuck_closed" else ""),
                         unsafe_demands=len(unsafe), demands=len(subsets),
                         detected_when_operated_alone=not alone,
                         detected_by_lid_cycle=lid_cycle not in masked_by,
                         masked_by_n=len(masked_by),
                         masked_example=masked_by[0] if masked_by else None))
    return rows


def report() -> str:
    r = reachability()
    sf = single_faults()
    one = single_faults([d for d in DEVICES if d != "lid_b"])
    lines = ["FT-1 laser safety chain (G9SE-201 + IPG two-channel interlock), contact-level model", "",
             f"reachability: {r['states']} internal states, {r['transitions']:,} transitions checked",
             f"  emission reachable at all: {r['emission_reachable']}",
             f"  emission with any contact open: {r['emission_with_a_contact_open']}",
             f"  safety outputs closed without a RESET pulse: {r['outputs_closed_without_reset']}", "",
             "single faults, two lid switches in series (each of the 127 combinations of opened devices is one demand):",
             f"{'fault':30s} {'unsafe':>7s} {'detected alone':>15s} {'by lid cycle':>13s} {'masked by':>10s}"]
    for x in sf:
        lines.append(f"{x['fault']:30s} {x['unsafe_demands']:>3d}/{x['demands']:<3d} {str(x['detected_when_operated_alone']):>15s} "
                     f"{str(x['detected_by_lid_cycle']):>13s} {x['masked_by_n']:>10d}")
    lid_one = [x for x in one if x["fault"].startswith("stuck_closed:lid_a")]
    lines += ["", "the same with one lid switch (lid_b removed from the chain):"]
    for x in lid_one:
        lines.append(f"{x['fault']:30s} {x['unsafe_demands']:>3d}/{x['demands']:<3d} {str(x['detected_when_operated_alone']):>15s} "
                     f"{str(x['detected_by_lid_cycle']):>13s} {x['masked_by_n']:>10d}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
