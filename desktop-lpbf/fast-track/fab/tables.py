"""Fill README.md's generated tables (pieces, hours by state, the voxel check) from out/*.json (#260).

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
    L = ["| Piece | What | First in | Route | Stock | Setups (mill / lathe) | Program min | Shop h | Low h |",
         "|---|---|---|---|---|---:|---:|---:|---:|"]
    for r in h["pieces"]:
        stock = by[r["pid"]]["stock"].split(";")[0]
        L.append("| %s | %s%s | %s | %s | %s | %d / %d | %.1f | %.1f | %.1f |" % (
            r["pid"], r["name"], (" (x%d)" % r["qty"]) if r["qty"] > 1 and "(" not in r["name"] else "", r["state"],
            r["route"], stock, r["mill_setups"], r["lathe_setups"], r["program_min"], r["total_h"], r["low_h"]))
    return "\n".join(L)


def state_rows(h):
    st, cu = h["by_state"], h["cumulative"]
    names = {"S1": "S1", "S2": "S1 + S2", "FT-0": "FT-0", "FT-1": "FT-1", "FT-1V": "FT-1V"}
    L = ["| State | Pieces | Shop h | Low h | Machine | Cumulative shop h | Cumulative low h | At $65/h | Study "
         "| BYU h if sheet and plates go out (cumulative) |", "|---|---:|---:|---:|---|---:|---:|---:|---|---:|"]
    for s in ("S1", "S2", "FT-0", "FT-1", "FT-1V"):
        stu = h["study"].get(s)
        L.append("| %s | %d | %.1f | %.1f | %s | **%.1f** | %.1f | $%s-%s | %s | %.1f |" % (
            s, st[s]["n"], st[s]["h"], st[s]["low"], names[s], cu[s]["h"], cu[s]["low"],
            format(int(round(cu[s]["low"] * 65, -1)), ","), format(int(round(cu[s]["h"] * 65, -1)), ","),
            ("%d-%d h" % tuple(stu)) if stu else "-", cu[s]["split"]))
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
    L.append("| **All** | %d | | | | | | | **%.1f / %.1f / %.1f** |" % (len(cam["setups"]), tot[0], tot[1], tot[2]))
    return "\n".join(L)


def put(text, key, block):
    mark = "<!-- %s -->\n%s\n<!-- /%s -->" % (key, block, key)
    if key in text and "<!-- %s -->" % key not in text:
        return text.replace(key, mark)
    return re.sub(r"<!-- %s -->.*?<!-- /%s -->" % (key, key), lambda m: mark, text, flags=re.S)


def main():
    h = json.loads((OUT / "hours.json").read_text())
    spec = json.loads((OUT / "pieces.json").read_text())
    cam = json.loads((OUT / "cam.json").read_text())
    rd = (HERE / "README.md").read_text()
    rd = put(rd, "PIECE_TABLE", piece_table(h, spec))
    rd = put(rd, "STATE_ROWS", state_rows(h))
    if (OUT / "sim.json").exists():
        rd = put(rd, "SIM_TABLE", sim_table(json.loads((OUT / "sim.json").read_text()), cam))
    (HERE / "README.md").write_text(rd)
    print("README tables filled")


if __name__ == "__main__":
    main()
