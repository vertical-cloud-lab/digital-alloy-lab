"""Re-run the orchid-examples quickstart notebook for another binary system (full ORCHID release via ORCHID_DATA).
The notebook hard-codes SYSTEM = "CU-ZR" and the export TDB name "CuZr-94Zen-LB"; this driver substitutes both in a
copy of the notebook (written next to the original so ../common resolves), executes it with nbclient
(allow_errors=True, so failing cells are recorded instead of aborting), and prints every cell's text output.

  python orchid_examples_quickstart_system.py QUICKSTART_DIR SYSTEM TDB_NAME OUT_DIR
"""
import os, sys, time
import nbformat
from nbclient import NotebookClient

qs, system, tdb, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
nb = nbformat.read(os.path.join(qs, "quickstart.ipynb"), as_version=4)
n_sub = 0
for c in nb.cells:
    if c.cell_type == "code":
        s = c.source
        s2 = s.replace('SYSTEM = "CU-ZR"', f'SYSTEM = "{system}"').replace("CuZr-94Zen-LB", tdb)
        n_sub += s != s2
        c.source = s2
print(f"system={system} tdb={tdb} cells modified={n_sub}")
os.environ["QUICKSTART_OUT"] = os.path.join(out, "figures")
os.environ["QUICKSTART_EXPORT"] = os.path.join(out, "export")
t0 = time.time()
NotebookClient(nb, timeout=600, kernel_name="python3", allow_errors=True,
               resources={"metadata": {"path": qs}}).execute()
print(f"executed in {time.time() - t0:.1f} s")
for i, c in enumerate(nb.cells):
    if c.cell_type != "code":
        continue
    for o in c.get("outputs", []):
        if o.output_type == "stream":
            txt = o.text
        elif o.output_type in ("execute_result", "display_data"):
            txt = o.get("data", {}).get("text/plain", "")
        elif o.output_type == "error":
            txt = f"ERROR {o.ename}: {o.evalue}"
        else:
            continue
        print(f"--- cell {i} [{o.output_type}]\n{txt[:3000]}")
nbformat.write(nb, os.path.join(out, f"quickstart_{system}.ipynb"))
