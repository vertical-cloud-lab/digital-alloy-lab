"""Two arms as two hands: where the second arm holds a part while the first drives its screws, and why (round 8, issue #260, PR #266).

Sterling, 2026-11-26: "The thought was also that the two robots would be working in tandem with each other similar to how a
human has two hands, holding something down for example." His byu-vcl lesson (notes/2026-11-26-byu-vcl-video-lessons.md,
lesson 3): use the second arm where a part would move, tip or spring back, put the number behind it, and no decorative holds
("holding the lid down while working the latch seems unnecessary?").

For every candidate step this writes the mechanical reason for or against a hold and what run 12 did:
  * a part placed on a face seal floats on it: the seal needs far more force to squeeze than the part weighs, so until the
    screws engage, the first screw pulls its side down and the ring lifts the other (the part tips and its holes walk off
    the threads). Squeeze force: Lindley's formula as in seals_forces.py (Gent's modulus at 75 Shore A, Parker 2-0xx IDs),
    over the ring's centre line, at 20 % and 25 % squeeze. A hold is used where the squeeze force exceeds the part's weight
    and the other arm can reach the first screws (run_assembly.hold_first: the placing arm keeps its gripper or cup on the
    part while the other arm drives the first two screws, the screws on its side first, spread apart; then it lets go);
  * a part on two dowels in a transition fit (H7/m6) is located and carried by them, and its O-ring is not squeezed until
    the screws pull it in: no hold (round 7 removed the holds on F14, F16 and F23 that way, after the holding wrist met
    the driving arm on every screw; those fixes stay);
  * a part that only sits on a flat or a pilot under its own weight, with no seal and nothing to spring back: no hold;
  * the two-arm carries and the existing holds of round 6 and 7 (rail F18, optics posts F03, cord and spigot seals) are
    listed as they are.

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/two_hands.py [results_run12.json] [assembly_run12.json]
Writes analysis/out/assembly/two_hands.json.
"""
from __future__ import annotations

import glob
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "assembly"
G = 9.81


def gent_E(shore=75.0):
    return 0.0981 * (56 + 7.62336 * shore) / (0.137505 * (254 - 2.54 * shore))


def lindley(cs, e, shore=75.0):
    """N per mm of seal length to squeeze a cross-section cs (mm) by e (seals_forces.py)."""
    return cs * gent_E(shore) * (1.25 * e ** 1.5 + 50 * e ** 6)


# step, what is placed, the screw step it waits for, kind, seal gland (seals_forces.json), masses: kit slot steps summed
CANDS = [
    ("M19", "heater stack, rod and gland plate, the gland plate on its 2-034 face O-ring on the welded collar", "M20", "seal",
     "gland_plate_M50", ["M01", "M03", "M04", "M05", "M06", "M11", "M13"]),
    ("C04", "outlet plenum on its 2-044 face O-ring (chamber upside down: the plenum lies on top)", "C05", "seal", "outlet_plenum", ["C04"]),
    ("F30", "lid on its 3.53 mm cord", "F31", "seal", "lid", ["F30"]),
    ("F33b", "window flange on its 2-036", "F34", "seal", "window_flange", ["F33b"]),
    ("F37b", "window retaining ring on the FKM flat ring, over the window on its 2-031", "F38", "seal", "window_lower", ["F37b"]),
    ("F43", "metering base on its 2-040", "F44", "seal", "metering_base", ["F43"]),
    ("F14", "inlet plenum on the back wall's two Ø3 dowels, its 2-044 not yet squeezed", "F15", "dowel", "inlet_plenum", ["F14"]),
    ("F16", "vacuum-port adapter on the right wall's two dowels, its 2-024 not yet squeezed", "F17", "dowel", "vacuum_port", ["F16"]),
    ("F23", "blind bearing cap on the right wall's two dowels, its 2-019 not yet squeezed", "F24", "dowel", "recoater_cap", ["F23"]),
    ("C00c", "frame lowered onto the floor plate's two dowels, on the floor cord (3.53 mm)", "C00d", "dowel", "floor", ["C00c"]),
    ("C14", "four chamber legs on the floor plate, one M6 down each leg's bore", "C15", "gravity", None, ["C14"]),
    ("C12", "Z mounting flange on the floor plate (chamber upside down)", "C13", "gravity", None, ["C12"]),
    ("M21", "handle slid 15 mm back onto the rod end's sleeves", "M22", "located", None, ["M21"]),
    ("M23", "striker disc on the rod end, three flat-head (countersunk) screws", "M24", "located", None, ["M23"]),
    ("F05b", "chamber assembly (19.6 kg) on the base plate, eight M6 from under the plate", "F06", "gravity", None, []),
    ("F54", "optics bridge (13.3 kg) on the four posts, eight M6 down into them", "F55", "gravity", None, ["F54"]),
    ("F18", "recoater rail with its carriage on the chamber's left wall (held by arm B since round 7)", "F18h", "held", None, ["F18"]),
    ("F03", "optics posts, one at a time, screws from under the base plate (held by the far arm since round 7)", "F03h", "held", None, ["F03"]),
    ("F51", "door with its cord, knuckles in line, before its two hinge pins (F52, F52b)", "F52", "door", None, ["F51"]),
]
MASS_OVERRIDE = {"F05b": 19.6}


def masses():
    files = sorted(glob.glob("/tmp/robotbuild/cache/kit-slots-*.json"))
    out = {}
    for f in files[-1:]:
        d = json.load(open(f))
        for s in (d["slots"] if isinstance(d, dict) else d):
            out[s.get("step")] = out.get(s.get("step"), 0.0) + float(s.get("mass_kg") or 0.0)
    return out


def main(res_path=None, rec_path=None):
    res = json.loads(pathlib.Path(res_path or OUT / "results_run12.json").read_text())
    rows = {r["id"]: r for r in res["rows"]}
    rec = None
    rp = pathlib.Path(rec_path or "/tmp/robotbuild/data/assembly_run12.json")
    if rp.exists():
        rec = json.loads(rp.read_text())
    seals = {r["gland"]: r for r in json.loads((OUT / "seals_forces.json").read_text())["seals"]["rows"]}
    m = masses()
    cands = []
    for sid, what, jstep, kind, gland, mkeys in CANDS:
        mass = MASS_OVERRIDE.get(sid, sum(m.get(k, 0.0) for k in mkeys))
        W = mass * G
        c = dict(step=sid, part=what, screws_in=jstep, kind=kind, mass_kg=round(mass, 3), weight_N=round(W, 1))
        if gland and gland in seals:
            s = seals[gland]
            cs = float(s["cs"])
            if s.get("centreline_mm"):
                L = float(s["centreline_mm"])
            elif s.get("ring_id"):
                L = math.pi * (float(s["ring_id"]) + cs) * int(s.get("n", 1) or 1)
            else:
                L = float(s.get("inner_perimeter_mm") or 0.0) + math.pi * cs
            c.update(seal=f"{s['ring']} ({cs} mm), {L:.0f} mm of seal", squeeze_N_20pct=round(lindley(cs, 0.20) * L),
                     squeeze_N_25pct=round(lindley(cs, 0.25) * L))
            c["squeeze_over_weight"] = round(c["squeeze_N_20pct"] / max(W, 0.01), 1)
        r = rows.get(sid, {})
        holds = r.get("holds") or []
        sub = rows.get(sid + "h")
        if kind == "seal":
            if sub and sub.get("n_ok"):
                h = holds[0] if holds else {}
                c.update(status="hold used", reason=(
                    f"it floats on its seal: {c['squeeze_N_20pct']:,} N to squeeze it 20 % against {W:.0f} N of weight "
                    f"({c['squeeze_over_weight']}x), so the first screw would tip it"),
                    run12=f"arm {sub.get('holder')} keeps it pressed while arm {sub.get('actor')} drives {sub['n_ok']} of the "
                          f"{h.get('n_joint', '?')} screws ({jstep} drives the rest after it lets go)"
                          + (f"; tried and blocked first: {'; '.join(h.get('fails', []))[:160]}" if h.get("fails") else ""))
            else:
                h = holds[0] if holds else {}
                c.update(status="not possible", reason=(
                    f"needed: {c.get('squeeze_N_20pct', 0):,} N to squeeze the seal 20 % against {W:.0f} N of weight"),
                    run12=("arm " + str(h.get("driver", "?")) + " could not drive a screw while arm " + str(h.get("holder", "?"))
                           + " held it: " + "; ".join(h.get("fails", []))[:240]) if h else
                          ("the placement failed, so no hold was tried" if r.get("arm") == "FAIL" else "no hold recorded"))
        elif kind == "dowel":
            c.update(status="not needed", reason=(
                f"located and carried by two dowels in a transition fit (H7/m6) before its seal is touched; the seal "
                f"({c.get('squeeze_N_20pct', 0):,} N to squeeze 20 %) is pulled in by the screws, which the dowels keep in line"),
                     run12=("round 7 removed this hold: the holding wrist met the driving arm on every screw (run10_fail_notes.json); "
                            "the dowel fix stays") if sid in ("F14", "F16", "F23") else "two-arm carry onto the dowels (C00c), then the screws")
        elif kind == "gravity":
            c.update(status="not needed", reason=(
                f"its {W:.0f} N of weight holds it on a flat seat or a pilot; no seal under it and nothing that springs back; the "
                "screw's torque is taken by the friction of the seat, which grows with the clamp load as the screw tightens"))
        elif kind == "located":
            c.update(status="not needed", reason=(
                f"{W:.1f} N; located by its sleeves or countersinks, which centre it as the screws go in; no seal under it"))
        elif kind == "held":
            st = rows.get(jstep) or {}
            c.update(status="hold used", reason="the part stands on a wall or under a plate: it would slide or fall before its screws are in",
                     run12=f"{st.get('n_ok', '?')} of {st.get('n', '?')} screws driven while it was held" if st else "see the step table")
        elif kind == "door":
            c.update(status="not tried", reason=(
                f"needed: the {W:.0f} N door stands on its knuckles with nothing else holding it until both hinge pins are in, "
                "and the pins need the knuckles in line"),
                run12=("not tried in run 12: arm A places the door and then needs the pin pusher, so the hold would be arm B "
                       "pushing both pins from the back, round the chamber's sides past the recoater motor (left) and the vacuum "
                       "port (right). Next: arm B holds the door while arm A pushes the pins (two tool changes), or the draw "
                       "latches closed first so they hold the door against its cord"))
        cands.append(c)
    # every step where both arms do something (the recording's per-arm robot time)
    both = []
    if rec is not None:
        for s in rec.get("steps", []):
            if float(s.get("robot_A_s", 0.0)) > 0.0 and float(s.get("robot_B_s", 0.0)) > 0.0:
                both.append(s["id"])
    prev = None
    p11 = OUT / "run11_times.json"
    if p11.exists():
        try:
            d11 = json.loads(p11.read_text())
            prev = [s["id"] for s in d11.get("steps", []) if float(s.get("robot_A_s", 0.0)) > 0.0 and float(s.get("robot_B_s", 0.0)) > 0.0]
        except Exception:   # noqa: BLE001
            prev = None
    n_steps = len([s for s in (rec or {}).get("steps", []) if s.get("do") != "note"])
    out = dict(
        note="Two arms as two hands (round 8, run 12): every candidate step, with the number behind a hold or against it. "
             "Squeeze forces are Lindley's formula (seals_forces.py) at 20 and 25 % over the ring's centre line, an estimate; "
             "masses from the parts' CAD (kit_table.py). A UR12e's F/T sensor reads +-100 N (seals_forces.json): the holding "
             "arm keeps the part flat and in place in position control while the first two screws engage; it does not squeeze "
             "the seal, the screws do.",
        candidates=cands,
        counts={k: sum(1 for c in cands if c["status"] == k) for k in ("hold used", "not needed", "not possible", "not tried")},
        new_holds_run12=[c["step"] for c in cands if c["status"] == "hold used" and c["kind"] == "seal"],
        steps_with_both_arms=dict(run12=len(both), run12_steps=both, of_robot_steps=n_steps,
                                  run11=len(prev) if prev is not None else None,
                                  how="steps in which the recording has motion time for both arm A and arm B (holds, two-arm "
                                      "carries, a screw handed to the other arm, a seal fed by one and rolled by the other)"),
    )
    (OUT / "two_hands.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out["counts"]), out["new_holds_run12"], "both arms:", len(both), "of", n_steps, "run 11:",
          len(prev) if prev is not None else None)
    return out


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
