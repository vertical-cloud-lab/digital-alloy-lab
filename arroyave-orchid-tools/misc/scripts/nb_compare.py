"""Compare text outputs of a stored (committed) notebook with a re-executed copy.

Usage: python -I nb_compare.py <stored.ipynb> <executed.ipynb> [max_chars]
Prints, per code cell, the first max_chars of the stored and re-run text output, and flags
cells whose output differs.
"""
import json
import re
import sys

ANSI = re.compile(r"\x1b\[[0-9;]*m")


def texts(path):
    nb = json.load(open(path))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        parts = []
        for o in c.get("outputs", []):
            if "text" in o:
                parts.append("".join(o["text"]))
            elif "data" in o and "text/plain" in o["data"]:
                parts.append("".join(o["data"]["text/plain"]))
            elif o.get("output_type") == "error":
                parts.append(f"ERROR {o['ename']}: {o['evalue']}")
        out.append(ANSI.sub("", "\n".join(parts)))
    return out


a, b = texts(sys.argv[1]), texts(sys.argv[2])
n = int(sys.argv[3]) if len(sys.argv) > 3 else 600
for i, (x, y) in enumerate(zip(a, b)):
    same = x.strip() == y.strip()
    print(f"### code cell {i}: {'IDENTICAL' if same else 'DIFFERS'}")
    if not same:
        print("--- stored:\n" + x[:n])
        print("--- re-run:\n" + y[:n])
