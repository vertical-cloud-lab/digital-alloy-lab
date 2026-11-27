"""Assemble REPORT.md from sections/*.md (header + sections in priority order + summary table from TABLE lines)."""
from pathlib import Path
R = Path("/tmp/arroyave/results/bo")
order = ["tamubo", "BAREFOOT-Framework", "PCMOBO", "SupplyRiskAwareDesign", "2026-islam-rhea-mobo",
         "DGP-BO", "Kernels-BO", "constraint-satisfaction", "BRAVE", "HTMDEC", "NiTi-alloy-discovery",
         "Alloy-Color-Optimization", "Initialization", "CatBoost-SMAs"]
body, table = [], []
for name in order:
    txt = (R / "sections" / f"{name}.md").read_text().rstrip("\n").splitlines()
    rows = [l for l in txt if l.startswith("TABLE:")]
    body.append("\n".join(l for l in txt if not l.startswith("TABLE:")).rstrip() + "\n")
    table += [r[len("TABLE:"):].strip() for r in rows]
head = (R / "sections" / "_header.md").read_text()
tail = ["## Summary table", "", "| repo | install | test/demo run | outcome | notes |", "|---|---|---|---|---|"]
tail += [f"| {r} |" for r in table]
files = (R / "sections" / "_footer.md").read_text()
(R / "REPORT.md").write_text(head.rstrip() + "\n\n" + "\n---\n\n".join(body) + "\n---\n\n" + "\n".join(tail) + "\n\n" + files)
print("REPORT.md written", len(table), "table rows")
