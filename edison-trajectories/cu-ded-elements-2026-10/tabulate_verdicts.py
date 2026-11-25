"""Collect the VERDICT line from each phase-1 answer into verdicts.md/.json.

Edison was asked to end each per-element answer with
    VERDICT | X | decision=... | family=... | conservative_max_wt=... | ...
This script finds that line (the last one if repeated), parses its fields,
and adds the TCCU7 coverage tier from tccu7_coverage.py. Answers without a
parsable line are listed so that they can be read by hand.

Run: python tabulate_verdicts.py
"""

import json
import pathlib
import re

from elements import ELEMENTS
from tccu7_coverage import row, tier

HERE = pathlib.Path(__file__).resolve().parent
FIELDS = ["decision", "family", "conservative_max_wt", "nonconservative_max_wt",
          "conservative_min_wt", "nonconservative_min_wt", "floor_wt",
          "impurity_max_wt", "evidence"]


def parse(text: str, el: str) -> dict | None:
    answer = text.split("\n---\n", 1)[-1]
    hits = [ln for ln in answer.splitlines()
            if re.search(r"VERDICT\s*\|", ln.replace("*", "").replace("`", ""))]
    if not hits:
        return None
    line = hits[-1].replace("*", "").replace("`", "").strip()
    out = {"raw": line}
    for f in FIELDS:
        m = re.search(rf"\b{f}\s*=\s*([^|]+)", line)
        if m:
            out[f] = m.group(1).strip()
    return out


def main() -> None:
    results, missing = {}, []
    for i, el in enumerate(ELEMENTS, start=1):
        path = HERE / "phase1" / f"el-{i:02d}-{el}.md"
        if not path.exists():
            missing.append(f"{el} (not fetched)")
            continue
        v = parse(path.read_text(), el)
        if v is None:
            missing.append(f"{el} (no VERDICT line)")
            continue
        v["tccu7_tier"] = tier(row(el)) if el != "Cu" else "matrix"
        v["file"] = path.name
        results[el] = v
    (HERE / "verdicts.json").write_text(json.dumps(results, indent=1) + "\n")
    lines = ["# Per-element verdicts as returned by Edison (unedited)", "",
             "Parsed by `tabulate_verdicts.py` from the last line of each answer in "
             "`phase1/`. These are Edison's numbers, before the cross-checks and "
             "decisions in README.md.", "",
             "| Element | Decision | Family | Conservative max (wt%) | "
             "Non-conservative max (wt%) | Floor (wt%) | Impurity max (wt%) | "
             "Evidence | TCCU7 tier |",
             "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |"]
    for el, v in results.items():
        cons = v.get("conservative_max_wt", v.get("conservative_min_wt", ""))
        non = v.get("nonconservative_max_wt", v.get("nonconservative_min_wt", ""))
        if el == "Cu":
            cons, non = f"min {cons}", f"min {non}"
        lines.append(
            f"| [{el}](phase1/{v['file']}) | {v.get('decision', '?')} | "
            f"{v.get('family', '?')} | {cons} | {non} | {v.get('floor_wt', '')} | "
            f"{v.get('impurity_max_wt', '')} | {v.get('evidence', '')} | "
            f"{v['tccu7_tier']} |")
    if missing:
        lines += ["", "Not parsed: " + ", ".join(missing)]
    (HERE / "verdicts.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
