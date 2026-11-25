"""Write decisions_table.md: Edison's verdict next to the final decision, per element."""
import json
import pathlib

from decisions import DECISIONS
from elements import ELEMENTS
from tccu7_coverage import row, tier

HERE = pathlib.Path(__file__).resolve().parent
v = json.loads((HERE / "verdicts.json").read_text())
lines = ["| Element | Edison | Decision | Reason | TCCU7 tier |",
         "| --- | --- | --- | --- | --- |"]
for i, el in enumerate(ELEMENTS, start=1):
    d, why = DECISIONS[el]
    e = v.get(el, {}).get("decision", "?")
    t = "matrix" if el == "Cu" else tier(row(el)).split(" ")[0]
    lines.append(f"| [{el}](phase1/el-{i:02d}-{el}.md) | {e} | {d} | {why} | {t} |")
(HERE / "decisions_table.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
