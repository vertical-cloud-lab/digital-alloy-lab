"""What the CAD v2 model (commit e6efa1c) changes in the fab pieces, and an estimate of the v2 shop hours (#260).

v2 was read, not merged: parts.py, the CAM, the voxel check and the drawings in this folder are still the v1 set
(ft_model at d117ba8). For each v1 piece this file records what v2 changes and the counts the v2 piece would have
(mill and lathe setups, holes, tapped holes, programmed minutes, lathe and hand minutes, sealing face, blank size).
New v2 pieces (MK-02f, MK-09c, MK-17b, MK-19 to MK-23) get counts by analogy with the v1 piece named in "basis".
The hours then come from hours.py's own piece_hours() with the same low, expected and high allowances, so the v1 and
v2 totals differ only by the pieces. Program minutes of changed or new pieces are estimates (no CAM was posted);
unchanged pieces keep their posted programs' minutes.

    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/v2_delta.py   -> out/v2/hours.json, out/v2/delta.md
    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/plan.py out/v2/hours.json out/v2   -> out/v2/plan.md
    /tmp/venv/bin/python desktop-lpbf/fast-track/fab/plan.py out/v2/monitoring-later/hours.json out/v2/monitoring-later
"""
from __future__ import annotations

import sys as _sys

if __name__ == "__main__":
    _sys.exit("v2_delta.py estimated the v2 hours from the v1 set (round 2). Round 3 ported the set itself to CAD v2, so "
              "out/hours.json, cam.json and pieces.json are now v2; out/v2/ (delta.md, hours.json, plan.md) is kept as the "
              "record of the estimate. To reproduce it, run this file at commit e3853cf.")

import copy
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hours as H  # noqa: E402

OUT = HERE / "out"
V2 = OUT / "v2"

# v1 piece -> (status, what v2 changes, count overrides). Status: same | re-dimensioned | redesigned | moved
CHANGES = {
    "MK-01": ("re-dimensioned", "outline 250 -> 245 square; X-LSM100B hole pattern (Zaber's STEP, in ft_vendor.py) in "
              "place of the X-LSQ075B's estimate; gland M5 taps at (+-21, +-21); 4 x M6 clearance at (+-112, +-92.1) "
              "for the cube's deck screws; no floor screws in the box (MK-23 clamps on the panel studs)",
              dict(prog=16.2, fc=22.4, dims=(255, 255, 12.7))),
    "MK-02a": ("same", "v2 still draws a 2 mm lip and a 10 mm ring; the fab's 4 mm lip and 12 mm height stand", {}),
    "MK-02b": ("same", "unchanged (6 x M4 at r 40)", {}),
    "MK-02c": ("same", "unchanged; on the Saginaw box's 1.9 mm door the ring's window bore moves to (0, -11)", {}),
    "MK-02d": ("re-dimensioned", "opening 40 -> 44, OD 70, slide pocket 50.6 x 1.2 from +x; centred at (0, -11)", {}),
    "MK-02e": ("re-dimensioned", "opening 40 -> 44, OD 70", {}),
    "MK-03": ("re-dimensioned", "4 heater holes 6.1 x 21 from the -x face at y +-15, +-30 (v1: 2); TC hole 1.6, 8 mm "
              "under the top from +y at x -30, clear of the heaters (v2's answer to the v1 clash)",
              dict(holes=13, prog=11.5, fc=16.8)),
    "MK-03s": ("same", "unchanged", {}),
    "MK-04": ("re-dimensioned", "28 -> 24 thick; heater holes 6.1 x 21 for 6 x 20 mm cartridges (v1 6.40 for 1/4 in.); "
              "TC hole 1.6 x 21; three 3 x 2.5 lead grooves in the underside from the holes to the socket",
              dict(prog=2.0, fc=3.0, lathe=4.5)),
    "MK-05": ("same", "unchanged", {}),
    "MK-06a": ("redesigned", "the 5 x 10 lead window becomes 3 notches 3 x 3.5 at 120 deg at the socket mouth (one "
               "indexed setup); a 15 mm vacuum-epoxy plug potted in the lower end (the leads leave through it)",
               dict(manual=30.0)),
    "MK-06b": ("redesigned", "as MK-06a", dict(manual=30.0)),
    "MK-07": ("re-dimensioned", "4 x M5 at (+-21, +-21), outside the face groove, with bonded-seal screws (v2), in "
              "place of the fab's (+-12.5, +-12.5) inside it; the deck needs M5 taps there (v2 does not draw them)", {}),
    "MK-08a": ("same", "unchanged", {}),
    "MK-08b": ("same", "unchanged", {}),
    "MK-08c": ("same", "unchanged", {}),
    "MK-08d": ("re-dimensioned", "13.5 mm shorter (stage centre line y 95.5 -> 82)", {}),
    "MK-08e": ("redesigned", "for the X-LSM100B carriage: foot 40 x 40 x 6 on Zaber's carriage holes, upright 40 x 8, "
               "taller (carriage top 21 mm over the deck); the shield sits 2 mm over the 6 mm foot, so the fab's 3 mm "
               "foot problem is gone", dict(prog=6.5, fc=11.5)),
    "MK-09a": ("redesigned", "becomes the scan-head flange plate: 278 x 120 x 12, standing on the head's entrance face "
               "(SCANLAB's drawing), a 52 bore for the input turret, hung from the gantry cross-beam by MK-09c",
               dict(holes=10, taps=4, prog=18.0, fc=27.0, dims=(288, 130, 12.7))),
    "MK-09b": ("moved", "the collimator saddle moves to MK-22 (coaxial branch adapter); same piece, its height follows "
               "the input axis (head_in_z 60 -> 43.5)", dict(pid="MK-22b", mk="MK-22")),
    "MK-10a": ("redesigned", "the long tube becomes a centre section 60 x 54 split lengthwise into two half-shells "
               "with 2 toggle clamps, seated on the window flange and in the collar's socket", "SPLIT"),
    "MK-10b": ("redesigned", "as MK-10a, short", "SPLIT"),
    "MK-10c": ("redesigned", "bore 110 -> 121.2 for the LINOS lens (119.8), OD 136, 34 tall plus a 6 mm floor ring "
               "with the 62 socket 13 mm off the lens axis; clamped on the lens", dict(prog=36.0, fc=52.0, holes=8,
                                                                                         taps=3, dims=(146, 146, 44.5))),
    "MK-11a": ("same", "v2 keeps the 55 x 19 x 8 envelope; the fab's 61 x 19 x 12 stands", {}),
    "MK-11b": ("same", "as MK-11a", {}),
    "MK-12": ("re-dimensioned", "flat pattern for the X-LSM100B: 166 x 50 top with a 145.6 x 12 slot, a 30 mm skirt", {}),
    "MK-13": ("redesigned", "window bore 53 at (0, -21) (the window stack's centre in the cube); a 26 camera bore "
              "along the camera's line of sight (a tilted setup); the drop tube's M4s",
              dict(ms=3, holes=15, taps=15, prog=9.0, fc=11.0)),
    "MK-14": ("re-dimensioned", "M5 gland taps at (+-21, +-21); 4 x M6 blind taps for the deck at (+-112, +-92.1)",
              dict(holes=12, taps=8, prog=4.6, fc=6.2)),
    "MK-15a": ("re-dimensioned", "296.7 x 180 x 10 across the base rails (4 x M6 at (+-70, rails)); the riser's holes",
               dict(prog=12.0, fc=12.2, dims=(306.7, 190, 12.7))),
    "MK-15b": ("re-dimensioned", "64 x 64 x 10 under the X-VSR20A (its foot measured from the STEP: 88 x 101; check "
               "that the riser carries its bolt pattern)", dict(prog=2.5, fc=3.0, dims=(74, 74, 12.7))),
    "MK-15c": ("redesigned", "becomes the rod-end block 64 x 40 x 40: rod clamp (1.5 slit, M4 across), a 16 x 29 x 12 "
               "lead pocket open to -y for the potted plug's pigtail, 4 x M6 counterbored into the X-VSR20A platform, "
               "a flat AE face at +x", dict(ms=4, holes=7, taps=3, prog=12.0, fc=17.0, manual=0.0,
                                           dims=(70, 46, 44.5), name="Rod-end block (clamp, lead pocket, AE face)")),
    "MK-16": ("same", "unchanged", {}),
    "MK-17": ("same", "buy the collar, as v1", {}),
    "MK-18a": ("re-dimensioned", "height follows v2's levels (deck top to 3 mm under the powder plane)", {}),
    "MK-18b": ("same", "unchanged", {}),
}

# new v2 pieces: counts by analogy (basis); prog/fc in minutes for the whole piece
NEW = [
    dict(pid="MK-02f", mk="MK-02", name="Cover-slide drop tube from the cube top plate", state="FT-1V", qty=1,
         route="lathe + CNC mill", ms=1, ls=2, holes=4, taps=0, prog=2.0, fc=3.0, lathe=15.0, manual=0.0, seal=False,
         dims=None, stock="3-1/2 in. 6061 round bar", basis="64 x 54 tube with a 90 x 5 flange; lathe time as MK-10a "
                                                           "x 3.5 (bored 54 through)"),
    dict(pid="MK-09c", mk="MK-09", name="Flange-to-beam angle brackets (2)", state="S1", qty=2, route="saw + CNC mill",
         ms=1, ls=0, holes=4, taps=0, prog=2.0, fc=3.0, lathe=0.0, manual=0.0, seal=False, dims=(45, 45, 45),
         stock="1-1/2 x 1-1/2 x 1/8 in. 6061 angle", basis="two drilled angles, one batch setup"),
    dict(pid="MK-17b", mk="MK-17", name="FT-0 lead terminal bracket", state="FT-0", qty=1, route="CNC mill", ms=2,
         ls=0, holes=6, taps=2, prog=4.0, fc=6.0, lathe=0.0, manual=0.0, seal=False, dims=(50, 60, 25),
         stock="1-1/2 in. 6061 angle or 1/4 in. plate", basis="an L with a slot: as MK-08d"),
    dict(pid="MK-19", mk="MK-19", name="Camera port ring (window 25.4 x 3, cover slide)", state="FT-0", qty=1,
         route="lathe + CNC mill", ms=1, ls=2, holes=4, taps=0, prog=2.0, fc=3.0, lathe=6.0, manual=0.0, seal=True,
         dims=None, stock="2 in. 6061 round bar", basis="44 x 7 ring, window seat 26 x 6: as MK-02a on a lathe"),
    dict(pid="MK-20", mk="MK-20", name="Camera post, foot, arm and Scheimpflug wedges (2.9 and 1.9 deg)",
         state="FT-0", qty=1, route="lathe + CNC mill", ms=1, ls=4, holes=4, taps=3, prog=4.0, fc=6.0, lathe=15.0,
         manual=0.0, seal=False, dims=None, stock="1/2 in. and 1-1/2 in. 6061 round bar",
         basis="three turned bits and two wedges cut on a sine vise"),
    dict(pid="MK-21", mk="MK-21", name="Light-port window rings (2, box walls)", state="FT-0", qty=2,
         route="lathe + CNC mill", ms=1, ls=2, holes=8, taps=0, prog=3.0, fc=4.5, lathe=10.0, manual=0.0, seal=True,
         dims=None, stock="2 in. 6061 round bar", basis="44 x 6 rings with a 30 bore: as MK-19, a batch of 2"),
    dict(pid="MK-21c", mk="MK-21", name="Light-port bores in the cube's left plate and door (E2 plates)",
         state="FT-1V", qty=1, route="CNC mill", ms=2, ls=0, holes=10, taps=8, prog=4.0, fc=5.0, lathe=0.0,
         manual=0.0, seal=True, dims=(301.8, 301.8, 22.9), stock="Ideal Vacuum plates (bought with the cube)",
         basis="a 24 bore at 15 and 30 deg on two bought plates, one tilted setup each: as MK-13"),
    dict(pid="MK-22a", mk="MK-22", name="Coaxial branch cage-cube plate on the head flange", state="S1", qty=1,
         route="CNC mill", ms=2, ls=0, holes=8, taps=2, prog=4.0, fc=6.0, lathe=0.0, manual=0.0, seal=False,
         dims=(70, 70, 12.7), stock="1/2 in. 6061 plate", basis="not drawn in v2; a 60 x 60 plate with 4 cage-rod "
                                                                  "holes and 4 bolts: as MK-02b"),
    dict(pid="MK-23", mk="MK-23", name="Deck clamps on the box's panel studs (4)", state="S2", qty=4,
         route="saw + CNC mill", ms=1, ls=0, holes=1, taps=0, prog=1.0, fc=1.5, lathe=0.0, manual=0.0, seal=False,
         dims=(40, 20, 4.8), stock="3/16 x 3/4 in. 6061 flat bar", basis="40 x 18 x 4 bars with a 5.2 hole for the #10 panel stud, a batch"),
]


MONITORING = {"MK-19", "MK-20", "MK-21", "MK-22a"}


def synth(p1, cam1, ov):
    """A v2 piece dict and cam setups from a v1 piece and count overrides."""
    p = copy.deepcopy(p1)
    cs = copy.deepcopy(cam1)
    for k in ("pid", "mk", "name", "state", "route", "stock"):
        if k in ov:
            p[k] = ov[k]
    if "ms" in ov:
        n = ov["ms"]
        tmpl = cs[0] if cs else dict(total_min=0.0, tool_changes=0, freecad_cycle_min=0.0)
        cs = [dict(tmpl) for _ in range(n)]
        p["setups"] = [dict(up="+Z") for _ in range(n)]
    if "prog" in ov and cs:
        tc = sum(c["tool_changes"] for c in cs) or 3 * len(cs)
        for c in cs:
            c["total_min"] = ov["prog"] / len(cs)
            c["freecad_cycle_min"] = ov.get("fc", ov["prog"] * 1.4) / len(cs)
            c["tool_changes"] = tc / len(cs)
    if "holes" in ov or "taps" in ov:
        holes = ov.get("holes", p["n_holes"])
        taps = ov.get("taps", sum(h["n"] for h in p["holes"] if h["kind"] == "tap"))
        p["n_holes"] = holes
        p["holes"] = [dict(kind="tap", n=taps), dict(kind="drill", n=max(holes - taps, 0))]
    if "lathe" in ov:
        p["lathe"] = [("turn (v2 estimate)", ov["lathe"])]
    if "manual" in ov:
        p["manual"] = [m for m in p["manual"]] + ([("pot the lead plug (vacuum epoxy)", ov["manual"])]
                                                  if ov["manual"] else [])
        if p["pid"].startswith("MK-15"):
            p["manual"] = []
    if "dims" in ov and ov["dims"]:
        x, y, z = ov["dims"]
        p["blank"] = dict(type="box", box=[-x / 2, x / 2, -y / 2, y / 2, 0.0, z])
    return p, cs


def new_piece(d):
    p = dict(pid=d["pid"], mk=d["mk"], name=d["name"], state=d["state"], qty=d["qty"], route=d["route"],
             stock=d["stock"], stock_pn="PN not read", seal=d["seal"], setups=[dict(up="+Z")] * d["ms"],
             n_holes=d["holes"], holes=[dict(kind="tap", n=d["taps"]), dict(kind="drill", n=d["holes"] - d["taps"])],
             lathe=[("turn (v2 estimate)", d["lathe"])] if d["lathe"] else [],
             manual=[("hand (v2 estimate)", d["manual"])] if d["manual"] else [],
             blank=(dict(type="box", box=[-d["dims"][0] / 2, d["dims"][0] / 2, -d["dims"][1] / 2, d["dims"][1] / 2, 0,
                                          d["dims"][2]]) if d["dims"] else dict(type="cyl")))
    cs = [dict(total_min=d["prog"] / d["ms"], freecad_cycle_min=d["fc"] / d["ms"], tool_changes=3)
          for _ in range(d["ms"])]
    return p, cs


def main():
    spec = {p["pid"]: p for p in json.loads((OUT / "pieces.json").read_text())["pieces"]}
    cam = {}
    for s in json.loads((OUT / "cam.json").read_text())["setups"]:
        cam.setdefault(s["pid"], []).append(s)
    v1 = {r["pid"]: r for r in json.loads((OUT / "hours.json").read_text())["pieces"]}
    rows, delta = [], []
    for pid, p1 in spec.items():
        status, what, ov = CHANGES[pid]
        if ov == "SPLIT":
            ov = dict(ms=1, holes=8, taps=8, prog=6.0, fc=8.5, dims=None, route="saw + lathe + CNC mill (split)")
            H.LATHE_SETUPS[pid] = 2
        p, cs = synth(p1, cam.get(pid, []), ov)
        if p["pid"] != pid:
            H.LATHE_SETUPS[p["pid"]] = H.LATHE_SETUPS.get(pid, 0)
        r = H.piece_hours(p, cs)
        r["v2_status"], r["v2_change"], r["v1_pid"] = status, what, pid
        rows.append(r)
        delta.append((pid, p["pid"], status, what, v1[pid], r))
    for d in NEW:
        p, cs = new_piece(d)
        H.LATHE_SETUPS[d["pid"]] = d["ls"]
        r = H.piece_hours(p, cs)
        r["v2_status"], r["v2_change"], r["v1_pid"] = "new", d["basis"], ""
        rows.append(r)
        delta.append(("", d["pid"], "new", d["name"] + ": " + d["basis"], None, r))
    order = {s: i for i, s in enumerate(H.STATES)}
    rows.sort(key=lambda r: (order[r["state"]], r["pid"]))
    st = {s: dict(h=0.0, low=0.0, high=0.0, split=0.0, prog=0.0, cam=0.0, n=0) for s in H.STATES}
    for r in rows:
        d = st[r["state"]]
        d["h"] += r["total_h"]
        d["low"] += r["low_h"]
        d["high"] += r["high_h"]
        d["split"] += r["byu_h_split"]
        d["prog"] += r["program_min"]
        d["cam"] += r["cam_h"]
        d["n"] += 1
    cum, c = {}, dict(h=0.0, low=0.0, high=0.0, split=0.0, cam=0.0)
    for s in H.STATES:
        for k in c:
            c[k] += st[s][k]
        cum[s] = dict(c)
    V2.mkdir(exist_ok=True)
    out = dict(method=__doc__.split("\n\n")[1], rate_usd_h=65.0, pieces=rows,
               by_state={s: {k: round(v, 2) for k, v in st[s].items()} for s in H.STATES},
               cumulative={s: {k: round(v, 2) for k, v in cum[s].items()} for s in H.STATES}, study=H.STUDY)
    (V2 / "hours.json").write_text(json.dumps(out, indent=1))
    # variant for the calendar: the monitoring pieces (no track needs them) made after FT-0's others, before FT-1's
    later = copy.deepcopy(out)
    for r in later["pieces"]:
        if r["pid"] in MONITORING:
            r["state"] = "FT-1"
    (V2 / "monitoring-later").mkdir(exist_ok=True)
    (V2 / "monitoring-later" / "hours.json").write_text(json.dumps(later, indent=1))
    L = ["| v1 piece | v2 piece | First in (v2) | Status | What v2 changes | v1 expected h | v2 low / expected / high h |",
         "|---|---|---|---|---|---:|---|"]
    for a, b, status, what, r1, r in delta:
        L.append("| %s | %s | %s | %s | %s | %s | %.1f / %.1f / %.1f |" % (
            a or "–", b, r["state"], status, what, ("%.1f" % r1["total_h"]) if r1 else "–", r["low_h"], r["total_h"],
            r["high_h"]))
    L += ["", "| State | v1 cumulative low / expected / high h | v2 cumulative low / expected / high h | v2 pieces |",
          "|---|---|---|---:|"]
    h1 = json.loads((OUT / "hours.json").read_text())["cumulative"]
    for s in H.STATES:
        L.append("| %s | %.1f / %.1f / %.1f | %.1f / **%.1f** / %.1f | %d |" % (
            s, h1[s]["low"], h1[s]["h"], h1[s]["high"], cum[s]["low"], cum[s]["h"], cum[s]["high"],
            sum(st[x]["n"] for x in H.STATES[:H.STATES.index(s) + 1])))
    (V2 / "delta.md").write_text("\n".join(L) + "\n")
    n_status = {}
    for _, _, status, *_ in delta:
        n_status[status] = n_status.get(status, 0) + 1
    print("v2 pieces", len(rows), n_status)
    for s in H.STATES:
        print("%-6s cumulative v2 %.1f / %.1f / %.1f h  (v1 %.1f / %.1f / %.1f)" % (
            s, cum[s]["low"], cum[s]["h"], cum[s]["high"], h1[s]["low"], h1[s]["h"], h1[s]["high"]))


if __name__ == "__main__":
    main()
