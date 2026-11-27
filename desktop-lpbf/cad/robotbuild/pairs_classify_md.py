"""Write desktop-lpbf/analysis/out/videoqa/round9_41_pairs.md from pairs_classify.py's /tmp/robotbuild/data/pairs_classify.json."""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
C = json.loads(Path("/tmp/robotbuild/data/pairs_classify.json").read_text())
RE_FING = re.compile(r"^[AB]/(gr/.*(finger|pad|knuckle).*|cap/.*)$")
RE_TOOL = re.compile(r"^[AB]/tool/")
RE_LINK = re.compile(r"^[AB]/(base|shoulder|upper_arm|forearm|wrist1|wrist2|wrist3)/")


def num(x):
    return 999.0 if x in (">100", None) and x == ">100" else (float(x) if x is not None else None)


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


def classify(r):
    ka, kb = kind(r["a"], r.get("a_is")), kind(r["b"], r.get("b_is"))
    ks = {ka, kb}
    drawn = 999.0 if r["drawn_mm"] == ">100" else float(r["drawn_mm"])
    pm = r.get("planner_mesh_mm", "n/a")
    pmv = 999.0 if pm is None else (None if pm == "n/a" else float(pm))
    r["kinds"] = f"{ka} x {kb}"
    r["drawn"] = drawn
    if pmv is not None and pmv <= 1.5:
        r["cls"], r["cause"] = "b", "drawn mesh: the planner's 0.1 mm mesh is clear (decimation or tessellation of the drawn mesh)"
        return r
    if "fingers" in ks and pmv is not None and pmv <= 5.0:
        r["cls"], r["cause"] = "c", "fingertips or pads on the part they hold, within the pads' compliance (<= 5 mm)"
        return r
    r["cls"] = "a"
    if ka == "kt" or kb == "kt":
        r["cause"] = ("plan: the dual carry's 'staged' put sets the part at the carry's first pose, which sinks it into the long "
                      "table's top; fix: stage it at its table slot (or lift the carry's first pose clear of the top)")
    elif "fingers" in ks:
        r["cause"] = ("plan: the recorded grasp closes the fingers past the part's surface (deeper than the pads' compliance); "
                      "fix: close to the part's width at the grasp (record the opening the checker used)")
    elif "person" in ks:
        r["cause"] = ("renderer: the person's hand targets after a failed step reach into the part (people.py's fingers curl "
                      "past the surface); fix: aim the hands at the part's outside, 20 mm off it")
    elif "arm tool" in ks:
        r["cause"] = ("plan: the tool's path (liner wand, ring pad, pin rod, nutrunner) passes through the part it works on; "
                      "fix: check the tool body against that part in the planner (it is excluded as the step's own part)")
    elif "arm link" in ks:
        r["cause"] = "plan: an arm link through a screw head the step does not drive; fix: add the screws present to the arm check"
    elif (ks <= {"part", "insert", "shcs", "fhcs", "dowel", "set", "disc", "plunger"} and r.get("rel_offset_mm") is not None and
          r["rel_offset_mm"] <= 6.0 and r.get("rel_rot_deg", 99) <= 2.0):
        r["cause"] = (f"plan or renderer: the part is {r['rel_offset_mm']} mm off its designed pose, at the end of a placement "
                      "(the insertion's last frames) or left off its seat at a release; fix: the release fix in asm_render.py "
                      "(118a9b3: a held part keeps the grasp's finger closure; 41's slices 0-10 were drawn before it), and "
                      "insertions that end exactly on the seat")
    elif ks <= {"part", "insert", "shcs", "fhcs", "dowel", "set", "disc", "plunger", "st"} or "st" in ks:
        r["cause"] = ("plan: parts drawn overlapping away from their designed pose (an insertion path, a placement or a release "
                      "a few mm off the seat); fix: check part against part along insertion paths, and seat on release")
    else:
        r["cause"] = "plan or model"
    return r


lines = ["# Round 9: the frame audit's pairs over 1.5 mm in chapters 41 and 40, classified (2026-11-27)", "",
         "Chapter 41's audit went from 209 pairs (round 8) to 238, and chapter 40's from 221 to 29. This sorts every pair into: "
         "**(a)** real clipping a viewer could see; **(b)** an artifact of the drawn meshes (the renderer draws each part decimated "
         "to at most 12,000 triangles; re-measured at the pair's worst frame with the planner's own 0.1 mm meshes, as "
         "analysis/assembly/rec_check.py does, the pair is clear); **(c)** a contact that is meant to be there but is not on "
         "the allowed list (fingertips or pads on the part they hold, at most 5 mm, the part moving with the fingers). "
         "Re-measured with cad/robotbuild/pairs_classify.py (then pairs_classify_md.py) (the same translational depth as scene_audit.py, at the recorded poses).", ""]
summary = []
for ch in ("41-assembly-chamber", "40-assembly-module"):
    res = [classify(r) for r in C.get(ch, [])]
    cnt = {k: sum(1 for r in res if r.get("cls") == k) for k in ("a", "b", "c")}
    nn = sum(1 for r in res if "cls" not in r)
    summary.append((ch, len(res), cnt, nn))
    by_cause = {}
    fr_c = {}
    for r in res:
        if r.get("cls") == "a":
            c_ = r["cause"]
            key = ("staged put into the table top" if "staged" in c_ else "fingers closed past the part (> 5 mm)" if "grasp closes"
                   in c_ else "person's hands (renderer)" if c_.startswith("renderer") else "tool through the part it works on"
                   if "tool's path" in c_ else "arm link through a screw" if "arm link" in c_ else "part in part, away from its seat"
                   if "overlapping" in c_ else "part just off its seat (<= 6 mm)" if "off its designed pose" in c_ else "other")
            by_cause[key] = by_cause.get(key, 0) + 1
            fs = fr_c.setdefault(key, set())
            for a_, b_ in r.get("ranges_all", r.get("ranges", [])):
                fs.update(range(int(a_), int(b_) + 1))
    lines += [f"## {ch}: {len(res)} pairs", "",
              "| Class | Pairs | What it is |", "|---|---:|---|",
              f"| (a) real clipping | {cnt['a']} | by cause (pairs; distinct frames): " +
              "; ".join(f"{k} {v} ({len(fr_c[k])} fr)" for k, v in sorted(by_cause.items(), key=lambda kv: -kv[1])) + " |",
              f"| (b) drawn-mesh artifact | {cnt['b']} | clear on the planner's 0.1 mm meshes |",
              f"| (c) intended contact | {cnt['c']} | fingertips on the part they hold, within 5 mm |"]
    if nn:
        lines.append(f"| not re-measured | {nn} | an actor missing at the recorded worst frame |")
    allf = set().union(*fr_c.values()) if fr_c else set()
    da = [r["drawn"] for r in res if r.get("cls") == "a"]
    bands = [(1.5, 5), (5, 10), (10, 20), (20, 1e9)]
    lines += ["", "Class (a) by depth: " + ", ".join(
        f"{sum(1 for d in da if lo < d <= hi)} pairs {lo:g}-{hi:g} mm" if hi < 1e9 else f"{sum(1 for d in da if d > lo)} over {lo:g} mm"
        for lo, hi in bands) + "."]
    nfr = {"41-assembly-chamber": 13640, "40-assembly-module": 2974}.get(ch, 0)
    lines += ["", f"Frames with any class-(a) pair: {len(allf)} of {nfr} ({100.0 * len(allf) / max(nfr, 1):.1f} %; frame ranges "
              "are capped at 40 per pair in the audit JSON, so this is a lower bound). The fixes, by owner: the plan (run_assembly.py "
              "and its checks; W3): stage dual carries at the table slot, check tools and parts against the part being placed along "
              "insertion paths, close grasps only to the part's width; the renderer (asm_render.py; W4): the person's hand targets "
              "20 mm outside the part, and the release fix already in 118a9b3 (re-render 41's slices 0-10 to apply it)."]
    lines.append("")
    for k, title in (("a", "(a) real clipping"), ("b", "(b) drawn-mesh artifacts"), ("c", "(c) intended contacts")):
        rows = sorted([r for r in res if r.get("cls") == k], key=lambda r: -r["drawn"])[:10]
        if not rows:
            continue
        lines += [f"### {title}: the 10 largest", "",
                  "| Pair | Kinds | Drawn (mm) | Planner meshes (mm) | Frames (ranges) | Cause and fix |", "|---|---|---:|---:|---|---|"]
        for r in rows:
            nm = f"{r['a']} ({(r.get('a_is') or '')[6:40]}) x {r['b']} ({(r.get('b_is') or '')[6:40]})"
            rng = "; ".join(f"{a_}-{b_}" for a_, b_ in r.get("ranges", [])[:3])
            pm = r.get("planner_mesh_mm")
            pm = ">100" if pm is None and "planner_tris" in r else (pm if pm is not None else "n/a")
            lines.append(f"| {nm} | {r['kinds']} | {r['drawn_mm']} | {pm} | {r['frames']} ({rng}) | {r.get('cause', '')} |")
        lines.append("")
head = ["| Chapter | Pairs | (a) real | (b) mesh artifact | (c) intended |", "|---|---:|---:|---:|---:|"]
head += [f"| {ch} | {n} | {cnt['a']} | {cnt['b']} | {cnt['c']} |" for ch, n, cnt, nn in summary]
head += ["", "Why 41's count rose (round 8: 209 pairs, 10,325 frames; round 9: 238, 13,640 frames): 138 pairs are in both "
         "rounds; 71 of round 8's are gone (the hoist hook in the build module, 22; parts in parts, 25; fingers in parts, 11; "
         "the wrist and a gripper, the stretchers, the jaws in their stands, the person in MiR A's tool stand); "
         "100 are new, 76 of them fingertips on parts and 22 parts in parts. No pair is a decimation artifact any more: round 9 "
         "draws each part at the scene file's 12,000 triangles (round 8 drew 2,500, which closed bores and counterbores), and "
         "only 11 parts have more than that (hoses, the chamber body, the floor plate, two servos); every pair re-measured on "
         "the planner's own meshes reads the same depth. The fingertip pairs are new partly because the parts are now drawn "
         "with their true surfaces, which the fingertips' closed pads meet, and partly from run 13/14's re-planned grasps "
         "(pick, push home with the fingers closed).", ""]
lines[4:4] = head
p = REPO / "desktop-lpbf/analysis/out/videoqa/round9_41_pairs.md"
p.write_text("\n".join(lines) + "\n")
print(p)
for ch, n, cnt, nn in summary:
    print(ch, n, cnt, nn)
