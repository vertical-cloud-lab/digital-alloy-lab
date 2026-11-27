"""The robot-build video's audit table (round 10, issue #260, PR #266): one row per chapter, from the frame audit
(scene_audit.py: pairs deeper than 1.5 mm) and the walk check (walk.py: people's stance feet, gliding, the MiRs), with an
earlier round's numbers beside them for comparison.

    python desktop-lpbf/cad/robotbuild/audit_table.py [--base 40c71a0] [--out table.md]

Reads desktop-lpbf/analysis/out/videoqa/scene_audit_<chapter>.json and walk_<chapter>.json as they are now, and the same
files at the git revision --base (round 9's: 40c71a0). Writes a Markdown table (stdout or --out) and, with --json, the
numbers behind it.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LPBF = HERE.parents[1]
QA = LPBF / "analysis" / "out" / "videoqa"
REPO = LPBF.parent
CHAPTERS = ["00-intro", "10-parts", "20-receiving", "29-stock", "30-machining-chamber", "31-machining-parts",
            "31b-machining-programs", "32-finishing", "38-tools", "40-assembly-module", "41-assembly-chamber",
            "50-integration"]


def load_now(name):
    p = QA / name
    return json.loads(p.read_text()) if p.exists() else None


def load_at(rev, name):
    rel = (QA / name).relative_to(REPO).as_posix()
    try:
        out = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{rel}"], capture_output=True, text=True, check=True)
        return json.loads(out.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def audit_row(d):
    if not d:
        return None
    pairs = d.get("pairs") or []
    largest = sorted(pairs, key=lambda p: -float(p.get("worst_mm") or 0))[:2]
    return dict(frames_checked=d.get("frames_checked"), frames_recorded=d.get("frames_recorded"),
                pairs=int(d.get("violations", len(pairs))), worst=float(d.get("worst_mm") or 0.0),
                largest=[f"{p['a']} / {p.get('b_is') or p['b']} ({p['worst_mm']:.1f} mm, {p.get('frames', 0)} fr)"
                         for p in largest])


def walk_row(d):
    if not d:
        return None
    people = d.get("people") or []
    mirs = d.get("mirs") or []
    slip = {p["person"]: float((p.get("slip_per_stance_mm") or {}).get("max") or 0.0) for p in people}
    glide = sum(int(p.get("gliding_frames") or p.get("glide_frames") or 0) for p in people)
    rev = {m["mir"]: (float(m.get("reverse_mm") or 0.0) / 1000.0, int(m.get("longest_reverse_leg_mm") or 0)) for m in mirs}
    side = {m["mir"]: float((m.get("sideways_mm") or {}).get("max_frame") or 0.0) for m in mirs}
    return dict(slip=slip, glide=glide, reverse=rev, sideways=side)


def fmt_slip(w):
    if not w or not w["slip"]:
        return "-"
    return ", ".join(f"{k} {v:.0f}" for k, v in w["slip"].items())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="40c71a0", help="the earlier round's revision (round 9: 40c71a0)")
    ap.add_argument("--out", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args(argv)
    rows, data = [], {}
    head = ("| Chapter | Frames audited | Pairs over 1.5 mm (round 9) | Worst, mm (round 9) | The largest | "
            "Stance-foot slip, max per stance, mm (round 9) | Gliding frames | MiR reversing | MiR sideways, max per frame, mm |")
    rows += [head, "|" + "---|" * 9]
    for ch in CHAPTERS:
        now, old = audit_row(load_now(f"scene_audit_{ch}.json")), audit_row(load_at(a.base, f"scene_audit_{ch}.json"))
        wn, wo = walk_row(load_now(f"walk_{ch}.json")), walk_row(load_at(a.base, f"walk_{ch}.json"))
        data[ch] = dict(audit=now, audit_base=old, walk=wn, walk_base=wo)
        if now is None:
            rows.append(f"| {ch} | not audited | ({old['pairs'] if old else '-'}) | | | | | | |")
            continue
        fr = f"{now['frames_checked']:,} of {now['frames_recorded']:,}"
        pairs = f"{now['pairs']} ({old['pairs'] if old else 'new'})"
        worst = f"{now['worst']:.1f} ({old['worst']:.1f})" if old else f"{now['worst']:.1f}"
        largest = "; ".join(now["largest"]) if now["pairs"] else ""
        slip = f"{fmt_slip(wn)} ({fmt_slip(wo)})" if wn else "-"
        glide = str(wn["glide"]) if wn else "-"
        rev = ", ".join(f"{k} {v[0]:.1f} m (longest {v[1]} mm)" for k, v in (wn or {}).get("reverse", {}).items()) or "-"
        side = ", ".join(f"{k} {v:.1f}" for k, v in (wn or {}).get("sideways", {}).items()) or "-"
        rows.append(f"| {ch} | {fr} | {pairs} | {worst} | {largest} | {slip} | {glide} | {rev} | {side} |")
    md = "\n".join(rows) + "\n"
    if a.out:
        Path(a.out).write_text(md)
    else:
        print(md)
    if a.json:
        Path(a.json).write_text(json.dumps(data, indent=1))


if __name__ == "__main__":
    main()
