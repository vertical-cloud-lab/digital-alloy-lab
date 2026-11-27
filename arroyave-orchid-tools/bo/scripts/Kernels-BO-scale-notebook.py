"""Write a scaled-down copy of application/BO_with_Optimized_Kernels.ipynb:
num_trials 5 -> 2 and num_queries 30 -> 10 in the two 1-D benchmark cells; everything else unchanged.
Usage: python -I Kernels-BO-scale-notebook.py <in.ipynb> <out.ipynb>"""
import json, re, sys
nb = json.load(open(sys.argv[1]))
n = 0
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    s2 = re.sub(r"^num_trials = 5$", "num_trials = 2  # scaled down from 5", s, flags=re.M)
    s2 = re.sub(r"^num_queries = 30$", "num_queries = 10  # scaled down from 30", s2, flags=re.M)
    if s2 != s:
        n += 1
        c["source"] = s2
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
json.dump(nb, open(sys.argv[2], "w"), indent=1)
print("cells patched:", n)

# --- second pass (added after the first run): insert cells that dump the best-so-far traces ---
if len(sys.argv) > 3:
    nb = json.load(open(sys.argv[2]))
    dump = ('import json as _j\n_j.dump({"comp_all": [list(map(float, r)) for r in comp_all], '
            '"rbf_all": [list(map(float, r)) for r in rbf_all]}, open("{tag}_traces.json", "w"))\n'
            'plt.gcf(); import matplotlib.pyplot as _p; _p.figure(figsize=(6,4)); '
            '_p.plot(np.array(comp_all).mean(0), label="composite"); _p.plot(np.array(rbf_all).mean(0), label="RBF"); '
            '_p.legend(); _p.xlabel("iteration"); _p.ylabel("best value (mean of trials)"); _p.title("{tag}"); _p.savefig("{tag}_trace.png", dpi=100)\n')
    cells = nb["cells"]
    idx = [i for i, c in enumerate(cells) if c["cell_type"] == "code" and "num_trials = 2" in "".join(c["source"])]
    for k, i in enumerate(sorted(idx, reverse=True)):
        tag = "ackley1d" if i == min(idx) else "dropwave1d"
        cells.insert(i + 1, {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                             "source": dump.replace("{tag}", tag)})
    json.dump(nb, open(sys.argv[3], "w"), indent=1)
    print("dump cells inserted after cells", idx)
