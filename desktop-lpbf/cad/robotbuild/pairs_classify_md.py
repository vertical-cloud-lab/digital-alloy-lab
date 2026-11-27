"""Write the classification of chapters 41's and 40's frame-audit pairs from pairs_classify.py's
/tmp/robotbuild/data/pairs_classify.json (round 9: round9_41_pairs.md; round 10, the default: round10_4x_pairs.md, compared
pair by pair with round 9's audit JSONs).

    /tmp/venv/bin/python pairs_classify_md.py [--round=10] [--prev=<dir with round 9's scene_audit_4x-*.json>] [--out=<md>]

Classes: (a) real clipping a viewer could see, by cause and owner; (b) an artifact of the drawn meshes (re-measured on the
planner's own 0.1 mm meshes the pair is clear); (c) a contact meant to be there but not on the allowed list (fingertips or
pads on the part they hold, at most 5 mm)."""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
VQA = REPO / "desktop-lpbf/analysis/out/videoqa"
OPT = {a.split("=")[0][2:]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
ROUND = int(OPT.get("round", "10"))
PREV = Path(OPT["prev"]) if OPT.get("prev") else None
OUT = Path(OPT["out"]) if OPT.get("out") else VQA / ("round9_41_pairs.md" if ROUND == 9 else f"round{ROUND}_4x_pairs.md")
C = json.loads(Path(OPT.get("json", "/tmp/robotbuild/data/pairs_classify.json")).read_text())
RE_FING = re.compile(r"^[AB]/(gr/.*(finger|pad|knuckle).*|cap/.*)$")
RE_TOOL = re.compile(r"^[AB]/tool/")
RE_LINK = re.compile(r"^[AB]/(base|shoulder|upper_arm|forearm|wrist1|wrist2|wrist3)/")
CHAPTERS = ("41-assembly-chamber", "40-assembly-module")


def kind(nm, is_):
    if nm.startswith("op/"):
        return "person"
    if re.match(r"^o\d+$", nm):
        return (is_ or "part:").split(":")[0]
    if RE_FING.match(nm):
        return "fingers"
    if RE_TOOL.match(nm):
        return "arm tool"
    if RE_LINK.match(nm):
        return "arm link"
    if nm.startswith(("A/", "B/")):
        return "gripper body"
    return nm.split("/")[0]


CAUSE = {
    "staged": ("staged put into the table top", "plan: the dual carry's 'staged' put sets the part at the carry's first pose, "
               "which sinks it into the long table's top; fix: stage it at its table slot (or lift the carry's first pose clear)"),
    "fingers": ("fingers closed past the part (> 5 mm)", "plan: the recorded grasp closes the fingers past the part's surface "
                "(deeper than the pads' compliance); fix: close only to the part's width at the grasp"),
    "person": ("the person (renderer)", "renderer: the person's body or hands in something drawn; fix: asm_render.py's spot "
               "and hand targets (checked against everything drawn since round 10)"),
    "tool": ("tool through the part it works on", "plan: the tool's path passes through the part it works on; fix: check the "
             "tool body against that part in the planner"),
    "link": ("arm link in something", "plan: an arm link through a screw head or a part the step does not work on; fix: add "
             "what is present to the arm check"),
    "seat": ("part just off its seat (<= 6 mm)", "plan or renderer: the part a few mm off its designed pose at the end of a "
             "placement or at a release; fix: insertions that end on the seat, the release put on the seat"),
    "inpart": ("part in part, away from its seat", "plan: parts drawn overlapping away from their designed pose (an insertion "
               "path, a placement or a carry); fix: check part against part along insertion paths"),
    "other": ("other", "plan or model"),
}


def classify(r):
    ka, kb = kind(r["a"], r.get("a_is")), kind(r["b"], r.get("b_is"))
    ks = {ka, kb}
    drawn = 999.0 if r["drawn_mm"] == ">100" else float(r["drawn_mm"])
    pm = r.get("planner_mesh_mm", "n/a")
    pmv = 999.0 if pm is None else (None if pm == "n/a" else float(pm))
    r["kinds"] = f"{ka} x {kb}"
    r["drawn"] = drawn
    if any("screw presenter" in nm for nm in (r["a"], r["b"])) and ks & {"shcs", "fhcs", "set"}:
        # round 10: a screw standing in the MiR's screw presenter at its pick: the presenter is drawn (and checked by the
        # planner) as a solid block, without the slots the screws stand in
        r["cls"], r["cause"] = "b", ("model: a screw standing in the MiR's screw presenter where the bit picks it (1-4 "
                                     "frames); the presenter (vendor not chosen) is drawn, and checked by the planner, as a solid "
                                     "250 x 130 x 150 mm envelope without the nest the screw stands in, so the same pair reads "
                                     "the same depth on the planner's meshes")
        return r
    if pmv is not None and pmv <= 1.5:
        r["cls"], r["cause"] = "b", "drawn mesh: the planner's 0.1 mm mesh is clear (decimation or tessellation of the drawn mesh)"
        return r
    if "fingers" in ks and pmv is not None and pmv <= 5.0:
        r["cls"], r["cause"] = "c", "fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm)"
        return r
    r["cls"] = "a"
    if "person" in ks:
        key = "person"
    elif ka == "kt" or kb == "kt":
        key = "staged"
    elif "fingers" in ks:
        key = "fingers"
    elif "arm tool" in ks:
        key = "tool"
    elif "arm link" in ks or "gripper body" in ks:
        key = "link"
    elif (ks <= {"part", "insert", "shcs", "fhcs", "dowel", "set", "disc", "plunger"} and r.get("rel_offset_mm") is not None and
          r["rel_offset_mm"] <= 6.0 and r.get("rel_rot_deg", 99) <= 2.0):
        key = "seat"
    elif ks <= {"part", "insert", "shcs", "fhcs", "dowel", "set", "disc", "plunger", "st"} or "st" in ks:
        key = "inpart"
    else:
        key = "other"
    r["cause_key"] = key
    r["cause"] = CAUSE[key][1] + (f" ({r['rel_offset_mm']} mm off)" if key == "seat" else "")
    return r


def prev_pairs(ch):
    if PREV is None or not (PREV / f"scene_audit_{ch}.json").exists():
        return None
    return {(p["a"], p["b"]) for p in json.loads((PREV / f"scene_audit_{ch}.json").read_text())["pairs"]}


lines = [f"# Round {ROUND}: the frame audit's pairs over 1.5 mm in chapters 41 and 40, classified (2026-11-27)", "",
         "Every pair the frame audit (scene_audit.py, every drawn frame, translational depth over 1.5 mm) found is sorted into: "
         "**(a)** real clipping a viewer could see, by cause and owner; **(b)** an artifact of the drawn meshes (re-measured "
         "at the pair's worst frame with the planner's own 0.1 mm meshes, as analysis/assembly/rec_check.py does, the pair is "
         "clear); **(c)** a contact that is meant to be there but is not on the allowed list (fingertips or pads on the part "
         "they hold, at most 5 mm). Re-measured with cad/robotbuild/pairs_classify.py, then this file's pairs_classify_md.py "
         "(the same translational depth as scene_audit.py, at the recorded poses).", ""]
summary = []
body = []
for ch in CHAPTERS:
    res = [classify(r) for r in C.get(ch, [])]
    aud = json.loads((VQA / f"scene_audit_{ch}.json").read_text()) if (VQA / f"scene_audit_{ch}.json").exists() else {}
    nfr = int(aud.get("frames_checked", 0))
    cnt = {k: sum(1 for r in res if r.get("cls") == k) for k in ("a", "b", "c")}
    nn = sum(1 for r in res if "cls" not in r)
    by_cause, fr_c = {}, {}
    for r in res:
        if r.get("cls") == "a":
            key = r["cause_key"]
            by_cause[key] = by_cause.get(key, 0) + 1
            fs = fr_c.setdefault(key, set())
            for a_, b_ in r.get("ranges", []):
                fs.update(range(int(a_), int(b_) + 1))
    prev = prev_pairs(ch)
    cmp_txt = ""
    if prev is not None:
        now = {(r["a"], r["b"]) for r in res}
        cmp_txt = (f" Against round {ROUND - 1}'s {len(prev)} pairs: {len(now & prev)} in both, {len(prev - now)} gone, "
                   f"{len(now - prev)} new.")
    summary.append((ch, len(res), cnt, nn, nfr, prev))
    body += [f"## {ch}: {len(res)} pairs", "",
             f"Frames audited: {nfr}.{cmp_txt}", "",
             "| Class | Pairs | What it is |", "|---|---:|---|",
             f"| (a) real clipping | {cnt['a']} | by cause (pairs; distinct frames): " +
             ("; ".join(f"{CAUSE[k][0]} {v} ({len(fr_c[k])} fr)" for k, v in sorted(by_cause.items(), key=lambda kv: -kv[1]))
              or "none") + " |",
             f"| (b) drawn-mesh artifact or model | {cnt['b']} | " +
             (f"{sum(1 for r in res if r['cls'] == 'b' and 'screw presenter' in r['a'] + r['b'])} a screw at its pick in the "
              f"screw presenter, which is modelled as a solid envelope without its nest; "
              f"{sum(1 for r in res if r['cls'] == 'b' and 'screw presenter' not in r['a'] + r['b'])} clear on the planner's "
              f"0.1 mm meshes |"),
             f"| (c) intended contact | {cnt['c']} | fingertips on the part they hold, within 5 mm |"]
    if nn:
        body.append(f"| not re-measured | {nn} | an actor missing at the recorded worst frame |")
    allf = set().union(*fr_c.values()) if fr_c else set()
    da = [r["drawn"] for r in res if r.get("cls") == "a"]
    bands = [(1.5, 5), (5, 10), (10, 20), (20, 1e9)]
    body += ["", "Class (a) by depth: " + ", ".join(
        f"{sum(1 for d in da if lo < d <= hi)} pairs {lo:g}-{hi:g} mm" if hi < 1e9 else f"{sum(1 for d in da if d > lo)} over {lo:g} mm"
        for lo, hi in bands) + "."]
    body += ["", f"Frames with any class-(a) pair: {len(allf)} of {nfr} ({100.0 * len(allf) / max(nfr, 1):.1f} %; frame ranges "
             "are capped at 40 per pair in the audit JSON, so this is a lower bound)."]
    body.append("")
    for k, title in (("a", "(a) real clipping"), ("b", "(b) drawn-mesh artifacts"), ("c", "(c) intended contacts")):
        rows = sorted([r for r in res if r.get("cls") == k], key=lambda r: -r["drawn"])[:12 if k == "a" else 8]
        if not rows:
            continue
        body += [f"### {title}: the largest", "",
                 "| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |", "|---|---|---:|---:|---|---|"]
        for r in rows:
            nm = f"{r['a']} ({(r.get('a_is') or '')[6:40]}) x {r['b']} ({(r.get('b_is') or '')[6:40]})"
            rng = "; ".join(f"{a_}-{b_}" for a_, b_ in r.get("ranges", [])[:3])
            pm = r.get("planner_mesh_mm")
            pm = ">100" if pm is None and "planner_tris" in r else (pm if pm is not None else "n/a")
            body.append(f"| {nm} | {r['kinds']} | {r['drawn_mm']} | {pm} | {r['frames']} ({rng}) | {r.get('cause', '')} |")
        body.append("")
head = ["| Chapter | Frames | Pairs | (a) real | (b) mesh artifact | (c) intended | Round " + str(ROUND - 1) + " pairs |",
        "|---|---:|---:|---:|---:|---:|---:|"]
head += [f"| {ch} | {nfr} | {n} | {cnt['a']} | {cnt['b']} | {cnt['c']} | {len(prev) if prev is not None else '-'} |"
         for ch, n, cnt, nn, nfr, prev in summary]
lines += head + [""] + body
OUT.write_text("\n".join(lines) + "\n")
print(OUT)
for ch, n, cnt, nn, nfr, prev in summary:
    print(ch, n, cnt, nn, nfr)
