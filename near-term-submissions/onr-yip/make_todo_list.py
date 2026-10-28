"""Collect the \\todo{...} notes of the copper/DED proposal into todo-list.tex.

The proposal prints each \\todo as a small red "TODO" marker, so the notes no longer take space in
the counted pages; this list, input after everything else, carries their text, in order, with the
section each sits in. Run before xelatex (project-description/build_latest.sh in sgbaird/byu-finances
does this):

    python make_todo_list.py [onr-yip-technical-proposal-cu-ded.tex]
"""
import re
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("onr-yip-technical-proposal-cu-ded.tex"))
text = src.read_text(encoding="utf-8")
body = text[text.index(r"\begin{document}"):]

items, section = [], "front matter"
i = 0
heading = re.compile(r"\\(sub)*section\*?\{([^}]*)\}|\\textbf\{([^}]*)\}")
pos = 0
while True:
    j = body.find(r"\todo{", i)
    if j < 0:
        break
    # the nearest preceding heading or run-in bold head
    for m in heading.finditer(body, pos, j):
        section = (m.group(2) or m.group(3)).strip().rstrip(".")
    pos = j
    # skip commented-out uses and the macro's own definition
    line_start = body.rfind("\n", 0, j) + 1
    if "%" in body[line_start:j]:
        i = j + 6
        continue
    depth, k = 1, j + 6
    while depth and k < len(body):
        depth += {"{": 1, "}": -1}.get(body[k], 0) if body[k - 1] != "\\" else 0
        k += 1
    items.append((section, " ".join(body[j + 6:k - 1].split())))
    i = k

out = [r"\clearpage", r"\section*{Open TODOs for Sterling}",
       r"\noindent Not part of the submission or the page count; each is marked \textcolor{red}{\textsuperscript{TODO}} in the text, and the list is rebuilt from the source by \texttt{make\_todo\_list.py}.",
       r"\begin{enumerate}\setlength{\itemsep}{2pt}"]
out += [rf"\item \textbf{{{s}.}} {t}" for s, t in items]
out += [r"\end{enumerate}", ""]
src.with_name("todo-list.tex").write_text("\n".join(out), encoding="utf-8")
print(f"wrote todo-list.tex: {len(items)} TODOs")
