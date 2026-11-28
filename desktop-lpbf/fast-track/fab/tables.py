"""Fill README.md's generated tables (pieces, hours by state, the shop calendar, the voxel check) from out/ (#260).

    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/tables.py
"""
from __future__ import annotations

import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"


def piece_table(h, spec):
    by = {p["pid"]: p for p in spec["pieces"]}
    L = ["| Piece | What | First in | Route | Stock | Setups (mill / lathe) | Cycle min: recount / FreeCAD | Low h "
         "| **Expected h** | High h |", "|---|---|---|---|---|---:|---|---:|---:|---:|"]
    tot = [0, 0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for r in h["pieces"]:
        stock = by[r["pid"]]["stock"].split(";")[0]
        L.append("| %s | %s%s | %s | %s | %s | %d / %d | %.1f / %.1f | %.1f | **%.1f** | %.1f |" % (
            r["pid"], r["name"], (" (x%d)" % r["qty"]) if r["qty"] > 1 and "(" not in r["name"] else "", r["state"],
            r["route"], stock, r["mill_setups"], r["lathe_setups"], r["program_min"], r["freecad_min"], r["low_h"],
            r["total_h"], r["high_h"]))
        for i, k in enumerate(("mill_setups", "lathe_setups", "program_min", "freecad_min", "low_h", "total_h",
                               "high_h")):
            tot[i] += r[k]
    L.append("| **All** | %d pieces | | | | %d / %d | %.0f / %.0f | %.1f | **%.1f** | %.1f |" % (
        len(h["pieces"]), *tot))
    return "\n".join(L)


def state_rows(h):
    st, cu = h["by_state"], h["cumulative"]
    L = ["| State | Pieces | This state, low / expected / high h | Cumulative (the machine), low / **expected** / high h "
         "| Cumulative at $65/h, low / expected / high | Study (`fast_track.py`) | BYU h with sheet and flat plates out, "
         "cumulative (expected) |", "|---|---:|---|---|---|---|---:|"]
    for s in ("S1", "S2", "FT-0", "FT-1", "FT-1V"):
        stu = h["study"].get(s)
        L.append("| %s | %d | %.1f / %.1f / %.1f | %.1f / **%.1f** / %.1f | $%s / %s / %s | %s | %.1f |" % (
            s, st[s]["n"], st[s]["low"], st[s]["h"], st[s]["high"], cu[s]["low"], cu[s]["h"], cu[s]["high"],
            *[format(int(round(cu[s][k] * 65, -1)), ",") for k in ("low", "h", "high")],
            ("%d-%d h" % tuple(stu)) if stu else "-", cu[s]["split"]))
    return "\n".join(L)


def short_table(h):
    cu = h["cumulative"]
    names = {"S1": "S1", "S2": "S1 + S2", "FT-0": "FT-0 (S1 + S2 + FT-0 pieces)", "FT-1": "FT-1", "FT-1V": "FT-1V"}
    L = ["  | Machine (cumulative) | Low | **Expected** | High | Study (`fast_track.py`, parts.csv F2a-c) "
         "| At $65/h, low / expected / high |", "  |---|---:|---:|---:|---:|---|"]
    for s in ("S1", "S2", "FT-0", "FT-1", "FT-1V"):
        stu = h["study"].get(s)
        L.append("  | %s | %.1f h | **%.1f h** | %.1f h | %s | $%s / %s / %s |" % (
            names[s], cu[s]["low"], cu[s]["h"], cu[s]["high"], ("%d-%d h" % tuple(stu)) if stu else "–",
            *[format(int(round(cu[s][k] * 65, -1)), ",") for k in ("low", "h", "high")]))
    return "\n".join(L)


def sim_table(sim, cam):
    tc = {}
    for s in cam["setups"]:
        d = tc.setdefault(s["pid"], [0.0, 0.0, 0])
        d[0] += s["total_min"]
        d[1] += s["freecad_cycle_min"]
        d[2] += 1
    L = ["| Piece | Setups | Voxel mm | Removed of blank - piece, cm³ | Gouge cm³ (deepest mm) | Left cm³ (thickest mm) | "
         "Slugs dropped cm³ | Rapids through the piece | Minutes: recount / from moves / FreeCAD |",
         "|---|---:|---:|---|---|---|---:|---:|---|"]
    tot = [0.0, 0.0, 0.0]
    for r in sorted(sim["pieces"], key=lambda r: r["pid"]):
        mv = sum(s.get("minutes_from_moves", 0.0) for s in r["setups"])
        rc, fc, n = tc.get(r["pid"], [0, 0, 0])
        tot[0] += rc
        tot[1] += mv
        tot[2] += fc
        L.append("| %s | %d | %.2f | %.1f of %.1f (%.1f %%) | %.3f (%.2f) | %.3f (%.2f) | %.1f | %d | %.1f / %.1f / %.1f |" % (
            r["pid"], n, r["res_mm"], r["removed_cm3"], r["expected_removal_cm3"], r["removed_pct_of_expected"],
            r["gouge_deep_cm3"], r["gouge_max_depth_mm"], r["left_thick_cm3"], r["left_max_thickness_mm"],
            r.get("slugs_dropped_cm3", 0.0), sum(h_["rapids_through_target"] for h_ in r["rapid_hits"]), rc, mv, fc))
    n_su = sum(tc.get(r["pid"], [0, 0, 0])[2] for r in sim["pieces"])      # the setups of the pieces simulated
    L.append("| **All** | %d | | | | | | | **%.1f / %.1f / %.1f** |" % (n_su, tot[0], tot[1], tot[2]))
    return "\n".join(L)


def v1v2_table(h):
    """round 3: v1 (round 2, out/v1/hours.json), round 2's estimate of v2 (out/v2/hours.json) and v2 as built in round 3
    with the CAM review's fixes (out/hours.json), cumulative by state"""
    v1 = json.loads((OUT / "v1" / "hours.json").read_text())
    est = json.loads((OUT / "v2" / "hours.json").read_text())
    L = ["| State | Pieces, v1 -> v2 (cumulative) | v1 (round 2), low / expected / high h | v2 estimated in round 2 "
         "| **v2, round 3** (CAM fixed), low / expected / high h | Change from v1, expected |", "|---|---|---|---|---|---:|"]
    n1 = n2 = 0
    for s in ("S1", "S2", "FT-0", "FT-1", "FT-1V"):
        a, e, b = v1["cumulative"][s], est["cumulative"][s], h["cumulative"][s]
        n1 += v1["by_state"][s]["n"]
        n2 += h["by_state"][s]["n"]
        L.append("| %s | %d -> %d | %.1f / %.1f / %.1f | %.1f / %.1f / %.1f | %.1f / **%.1f** / %.1f | +%.1f h (+%.0f %%) |" % (
            s, n1, n2, a["low"], a["h"], a["high"], e["low"], e["h"], e["high"], b["low"], b["h"], b["high"],
            b["h"] - a["h"], 100 * (b["h"] / a["h"] - 1)))
    return "\n".join(L)


def reviewed_table(h):
    """round 3: the reviewed case (hours.py REVIEWED: review-r3.md section 4 per piece), cumulative by state"""
    rv, cu = h["reviewed"]["cumulative"], h["cumulative"]
    L = ["| State | Mill / lathe setups (cumulative) | Machinist, h | Machinist and student, h "
         "| The set's low / expected / high, h |", "|---|---|---|---|---|"]
    for s in ("S1", "S2", "FT-0", "FT-1", "FT-1V"):
        a = rv[s]
        L.append("| %s | %d / %d | %.1f-%.1f | %.1f-%.1f | %.1f / %.1f / %.1f |" % (
            s, a["mill_setups"], a["lathe_setups"], a["machinist_low"], a["machinist_high"], a["student_low"],
            a["student_high"], cu[s]["low"], cu[s]["h"], cu[s]["high"]))
    return "\n".join(L)


def put(text, key, block, indent=""):
    mark = "%s<!-- %s -->\n%s\n%s<!-- /%s -->" % (indent, key, block, indent, key)
    if key in text and "<!-- %s -->" % key not in text:
        return re.sub(r"^[ ]*%s$" % key, lambda m: mark, text, count=1, flags=re.M)
    return re.sub(r"^[ ]*<!-- %s -->.*?<!-- /%s -->" % (key, key), lambda m: mark, text, flags=re.S | re.M)


def main():
    h = json.loads((OUT / "hours.json").read_text())
    spec = json.loads((OUT / "pieces.json").read_text())
    cam = json.loads((OUT / "cam.json").read_text())
    rd = (HERE / "README.md").read_text()
    # Round 3: out/ is CAD v2's now. The round-2 tables in the README (SHORT_TABLE, PIECE_TABLE, STATE_ROWS,
    # PLAN_TABLE, SIM_TABLE, DELTA_TABLE, V2_STATES) describe v1 and stay as round 2 wrote them (v1's hours, plan and
    # voxel check are in out/v1/). Only the round-3 tables are filled. Round 2's calls, for the record:
    #   PIECE_TABLE piece_table(h, spec); STATE_ROWS state_rows(h); SHORT_TABLE short_table(h); PLAN_TABLE plan.md;
    #   SIM_TABLE sim_table(sim, cam); DELTA_TABLE and V2_STATES from out/v2/delta.md
    rd = put(rd, "R3_PIECE_TABLE", piece_table(h, spec))
    rd = put(rd, "R3_STATE_ROWS", state_rows(h))
    if (OUT / "v1" / "hours.json").exists():
        rd = put(rd, "V1V2_TABLE", v1v2_table(h))
    if "reviewed" in h:
        rd = put(rd, "R3_REVIEWED", reviewed_table(h))
    if (OUT / "plan.md").exists():
        rd = put(rd, "R3_PLAN", (OUT / "plan.md").read_text().strip())
    if (OUT / "sim.json").exists():
        rd = put(rd, "R3_SIM", sim_table(json.loads((OUT / "sim.json").read_text()), cam))
    (HERE / "README.md").write_text(rd)
    print("README tables filled")


if __name__ == "__main__":
    main()
