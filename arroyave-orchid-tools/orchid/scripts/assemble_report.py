"""Assemble REPORT.md from sections/*.md: the last '| repo | ... |' row of each section goes into the summary table."""
import os, re
R = "/tmp/arroyave/results/orchid"
order = ["orchid-examples", "orchid-mcp", "orchid-data", "orchid-bench", "orchid-project.org"]
head = open(os.path.join(R, "sections", "_header.md")).read()
bodies, rows = [], []
for name in order:
    lines = open(os.path.join(R, "sections", f"{name}.md")).read().rstrip("\n").split("\n")
    i = max(k for k, l in enumerate(lines) if l.startswith(f"| {name} |"))
    rows.append(lines[i]); bodies.append("\n".join(lines[:i] + lines[i + 1:]).rstrip() + "\n")
table = ["## Summary", "", "| repo | install | tests/examples run | outcome | notes |", "|---|---|---|---|---|"] + rows
files = []
for sub in ("data", "figures", "logs", "scripts"):
    for root, _, fs in os.walk(os.path.join(R, sub)):
        for f in sorted(fs):
            files.append(os.path.relpath(os.path.join(root, f), R))
tail = ["", "## Files", "", "All paths relative to `/tmp/arroyave/results/orchid/` (" + str(len(files)) + " files; `sections/` holds the per-repo sources of this report).", ""]
tail += ["- " + ", ".join(f"`{f}`" for f in sorted(files) if f.startswith(sub + "/")) for sub in ("data", "figures", "logs", "scripts")]
open(os.path.join(R, "REPORT.md"), "w").write(head.rstrip() + "\n\n" + "\n".join(bodies) + "\n" + "\n".join(table) + "\n" + "\n".join(tail) + "\n")
print("REPORT.md", os.path.getsize(os.path.join(R, "REPORT.md")), "bytes;", len(files), "files listed")
