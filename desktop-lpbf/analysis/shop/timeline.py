"""Rough timeline for making one desktop LPBF's 37 machined parts by hand vs in the two-arm robot shop
(issue #260, PR #266). Reads the machining review's per-part times (analysis/out/machining/dfm.json) and the robot
cycle times this folder's FCL plans measured (analysis/out/shop/shop_checks.json). Everything not read from those files
is an assumption stated in ASSUME; nothing here is measured on a real shop.

Run:  /tmp/venv/bin/python desktop-lpbf/analysis/shop/timeline.py     (writes analysis/out/shop/timeline.json)
"""
from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "out" / "shop"

ASSUME = dict(
    cam_h=35.0,                    # CAM programming, 30-40 h (machining.md)
    hand_setup_min=20.0,           # per setup by hand: indicate, edge-find, clamp (dfm.py; 40 for the chamber)
    hand_saw_min=5.0, hand_deburr_min=10.0, hand_wash_min=5.0, hand_measure_min=10.0,   # per part, by hand (est)
    hand_unbox_min=10.0, hand_kit_min=2.0,                                                 # per box / per part (est)
    mir_leg_s=25.0,                # one MiR leg between stations: ~6 m at 1 m/s with 0.3 m/s^2 ramps + slow-downs (est)
    dock_s=30.0, register_s=15.0,  # docking to a VL marker, then a D405 look at the station's AprilTag cube (est)
    door_s=6.0,                    # Haas auto door open + close (est; Haas publishes no time)
    air_blast_s=20.0, seat_check_s=5.0,   # chips off the vise / part with the AAG, wrist-camera look at the seating (est)
    probe_s=60.0,                  # WIPS probing of the new setup's work offset (spindle time, est)
    supervise_new_min=8.0,         # a person watching the first run of each new setup (est)
    robot_saw_min=3.0, robot_deburr_min=4.0, robot_wash_min=6.0, robot_measure_min=4.0, robot_kit_min=1.0,
    robot_unbox_min=8.0,
    hours_per_day_hand=8.0, hours_per_day_shop=20.0,     # one machinist's day; the cell runs two shifts unattended
)


def main():
    dfm = json.loads((HERE.parent / "out" / "machining" / "dfm.json").read_text())["parts"]
    chk = json.loads((OUT / "shop_checks.json").read_text())
    A = ASSUME
    n_parts = len(dfm)
    n_pieces = sum(p["n_pieces"] for p in dfm)
    def n_setups(p):            # dfm.json leaves setups empty for parts added after its sweep: 20 min per setup
        return len(p["setups"]) if p.get("setups") else max(1, round(p["time_min"]["setup"] / 20.0))
    setups = sum(n_setups(p) for p in dfm)
    cut_min = sum((p["time_min"]["rough"] + p["time_min"]["finish"] + p["time_min"]["holes"]) * p["n_pieces"] for p in dfm)
    setup_min_hand = sum(p["time_min"]["setup"] for p in dfm)
    # robot changeover per setup: the P1 plan (load) + its mirror (unload), the door, chips, a seating look, probing
    p1 = chk["P1_vf4_single_arm"]["time_s"]
    p2 = chk["P2_lathe"]["time_s"]
    change_s = 2 * p1 + A["door_s"] + A["air_blast_s"] + A["seat_check_s"] + A["probe_s"]
    visit_s = A["mir_leg_s"] + A["dock_s"] + A["register_s"]
    # heavy pieces a person loads with a hoist or lifter: stock over 2 x 11.2 kg, plus the plates that need two arms
    import sys
    sys.path.insert(0, str(HERE))
    import shop_checks                                # the payload table from the same dfm.json this run reads
    cur = [r for r in shop_checks.payload_table()["parts"] if not r.get("version_a")]
    heavy = [r for r in cur if r["verdict"] in ("person + hoist",)]
    two_arm = [r for r in cur if r["verdict"] == "two arms, rigid grasp"]
    rows = []

    def row(step, hand_h, robot_h, person_h_robot, note):
        rows.append(dict(step=step, hand_person_h=round(hand_h, 1), shop_machine_or_robot_h=round(robot_h, 1),
                         shop_person_h=round(person_h_robot, 1), note=note))

    row("CAM programming and simulation", A["cam_h"], 0.0, A["cam_h"], "unchanged: a person writes and proves every program")
    row("unboxing and receiving (11 shipments)", 11 * A["hand_unbox_min"] / 60, 8 * A["robot_unbox_min"] / 60,
        3 * 20 / 60, "3 shipments over 22 kg (block, plate bundle, laser crate) need a person and a pallet jack")
    row("stock prep (saw, about 20 blanks)", 20 * A["hand_saw_min"] / 60, 20 * A["robot_saw_min"] / 60, 0.5,
        "bar blanks only; the chamber block and plates are bought cut to size")
    row("spindle time (rough, finish, holes)", cut_min / 60, cut_min / 60, 0.0,
        f"{cut_min / 60:.1f} h of cutting at machining.md's removal rates, the same in both cases")
    row("setups and part flips", setup_min_hand / 60, setups * (change_s + visit_s) / 3600,
        setups * A["supervise_new_min"] / 60 + (len(heavy) * 2 + len(two_arm)) * 15 / 60,
        f"{setups} setups; robot changeover {change_s + visit_s:.0f} s each (P1 plan {p1:.1f} s x2 + door, chips, "
        f"probing, MiR leg, dock, re-register); a person watches each new setup's first run and loads the heavy pieces")
    row("deburr", n_pieces * A["hand_deburr_min"] / 60, n_pieces * A["robot_deburr_min"] / 60, n_pieces * 2 / 60,
        "robot: edges on the brush and a compliant deburring tool; a person checks and touches up (2 min a part)")
    row("wash", n_pieces * A["hand_wash_min"] / 60, n_pieces * A["robot_wash_min"] / 60, 0.0, "basket in the ultrasonic tank")
    row("measure", n_pieces * A["hand_measure_min"] / 60, n_pieces * A["robot_measure_min"] / 60, n_pieces * 4 / 60,
        "robot places parts; gauging of seal faces and bores stays with a person (bore gauge, height gauge)")
    row("kitting", n_pieces * A["hand_kit_min"] / 60, n_pieces * A["robot_kit_min"] / 60, 0.0, "totes on the rack's upper shelves")
    tot_hand = sum(r["hand_person_h"] for r in rows)
    tot_person_shop = sum(r["shop_person_h"] for r in rows)
    machine_h = sum(r["shop_machine_or_robot_h"] for r in rows if r["step"].startswith(("spindle", "setups")))
    days_hand = tot_hand / A["hours_per_day_hand"]
    # the shop: CAM first (person days), then the cell is limited by its busiest machine (the VF-4 does most cutting)
    vmc_share = sum((p["time_min"]["rough"] + p["time_min"]["finish"] + p["time_min"]["holes"]) * p["n_pieces"]
                    for p in dfm if "lathe" not in p["machine"].lower()) / cut_min
    days_shop = A["cam_h"] / A["hours_per_day_hand"] + (machine_h * vmc_share) / A["hours_per_day_shop"] + 1.0
    # cautious variant: a person watches every first run in full, except the long roughing of the chamber, the two
    # base plates and the optics bridge (simulated in CAM, left to run with tool-breakage detection)
    long_rough = sum(p["time_min"]["rough"] for p in dfm
                     if p["slug"].startswith(("process_chamber", "chamber_floor", "base_plate", "optics_bridge_6061")))
    cautious_extra_h = (cut_min - long_rough) / 60.0
    import os
    res = dict(dfm_json_mtime_utc=__import__("time").strftime("%Y-%m-%dT%H:%MZ", __import__("time").gmtime(
        os.path.getmtime(HERE.parent / "out" / "machining" / "dfm.json"))), assumptions=A, n_parts=n_parts, n_pieces=n_pieces, setups=setups, cut_h=round(cut_min / 60, 1),
               setup_h_hand=round(setup_min_hand / 60, 1), robot_changeover_s=round(change_s + visit_s, 0),
               lathe_load_plan_s=p2, rows=rows, total_hand_person_h=round(tot_hand, 1),
               total_shop_person_h=round(tot_person_shop, 1), shop_machine_h=round(machine_h, 1),
               days_hand=round(days_hand, 1), days_shop=round(days_shop, 1), vmc_share=round(vmc_share, 2),
               cautious_extra_person_h=round(cautious_extra_h, 1),
               total_shop_person_h_cautious=round(tot_person_shop + cautious_extra_h, 1),
               not_included=["commissioning the cell: fixtures and soft jaws, station AprilTag cubes and registration, "
                             "teaching and proving every robot task, the risk assessment and interlocks (likely months "
                             "for the first machine)", "welding, honing (outsourced), heat treatment, bead blasting",
                             "assembly (see the assembly study in this PR)", "queue time at BYU's shops"],
               heavy_parts=[r["part"] for r in heavy], two_arm_parts=[r["part"] for r in two_arm])
    (OUT / "timeline.json").write_text(json.dumps(res, indent=1))
    for r in rows:
        print(f"{r['step'][:42]:42s} hand {r['hand_person_h']:6.1f} h | shop {r['shop_machine_or_robot_h']:6.1f} h machine/robot, "
              f"{r['shop_person_h']:5.1f} h person")
    print(f"total person-h: hand {tot_hand:.1f}, shop {tot_person_shop:.1f} (cautious {tot_person_shop + cautious_extra_h:.1f}); "
          f"days: hand {days_hand:.1f}, shop {days_shop:.1f}")


if __name__ == "__main__":
    main()
